"""The evaluation pipeline.

Stage 1, retrieval (no API key needed): for every answerable question, where
does the expected source rank? And how well does the grounding gate separate
answerable questions from off-topic ones at each threshold?

Stage 2, end to end (needs ANTHROPIC_API_KEY): run every question through the
assistant, then grade it. Answerable questions are graded on grounding (share of
claims supported by the retrieved passages), key-point coverage, and citation
coverage. Unanswerable and off-topic questions pass if the assistant declines.
Adversarial questions pass if the rule held.

Results are written as JSON and as a markdown report to eval/results/.
"""
from __future__ import annotations

import json
import statistics
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .answer import ask, make_client
from .config import ROOT, Settings
from .guardrails import longest_shared_run
from .judge import judge_grounding, judge_rule
from .retrieve import Retriever

QUESTIONS = ROOT / "eval" / "questions.yaml"
RESULTS = ROOT / "eval" / "results"

# List prices per million tokens (input, output), October 2026. Update if they change.
PRICES = {"claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0), "claude-haiku-5-5": (0.10, 0.50),
          "claude-fable-5-1": (10.0, 50.0)}


@dataclass
class Question:
    id: str
    type: str
    question: str
    expected_sources: list[str]
    key_points: list[str]
    attack: str = ""
    pass_if: str = ""


def load_questions(path: Path = QUESTIONS) -> list[Question]:
    raw = yaml.safe_load(path.read_text())["questions"]
    return [Question(q["id"], q["type"], q["question"], q.get("expected_sources", []),
                     q.get("key_points", []), q.get("attack", ""), q.get("pass_if", "")) for q in raw]


def matches(doc_id: str, expected: list[str]) -> bool:
    return any(doc_id.startswith(e) for e in expected)


# ---------------------------------------------------------------------------- retrieval
def retrieval_metrics(retriever: Retriever, questions: list[Question], mode: str, depth: int = 10) -> dict:
    ranks, per_q = [], []
    for q in questions:
        if not q.expected_sources:
            continue
        hits = retriever.search(q.question, k=depth, mode=mode).hits
        rank = next((h.rank for h in hits if matches(h.chunk.doc_id, q.expected_sources)), None)
        ranks.append(rank)
        per_q.append({"id": q.id, "rank": rank, "top": hits[0].chunk.doc_id if hits else None})
    n = len(ranks)
    hit_at = lambda k: sum(1 for r in ranks if r and r <= k) / n
    return {
        "mode": mode, "questions": n,
        "hit@1": hit_at(1), "hit@3": hit_at(3), "hit@6": hit_at(6), "hit@10": hit_at(10),
        "mrr@10": sum(1 / r for r in ranks if r) / n,
        "per_question": per_q,
    }


def gate_sweep(retriever: Retriever, questions: list[Question]) -> dict:
    """For each BM25 threshold: how many answerable questions pass, and how many off-topic ones are stopped."""
    scores = {q.id: retriever.search(q.question, k=1, mode="bm25").top_bm25 for q in questions}
    should_pass = [q.id for q in questions if q.type == "answerable" or (q.type == "adversarial" and q.expected_sources)]
    should_stop = [q.id for q in questions if q.type == "out_of_scope"]
    rows = []
    for t in [round(0.10 + 0.02 * i, 2) for i in range(21)]:
        passed = sum(scores[i] >= t for i in should_pass) / len(should_pass)
        stopped = sum(scores[i] < t for i in should_stop) / len(should_stop)
        unans = [q.id for q in questions if q.type == "unanswerable"]
        rows.append({"threshold": t, "answerable_pass": passed, "off_topic_stopped": stopped,
                     "unanswerable_stopped": sum(scores[i] < t for i in unans) / len(unans)})
    safe = [r for r in rows if r["answerable_pass"] == 1.0]
    best = max(safe, key=lambda r: (r["off_topic_stopped"], r["threshold"])) if safe else None
    return {"scores": scores, "sweep": rows, "recommended": best["threshold"] if best else None,
            "min_answerable_score": min(scores[i] for i in should_pass),
            "max_off_topic_score": max(scores[i] for i in should_stop)}


# --------------------------------------------------------------------------- end to end
def cost(model: str, usage: dict) -> float:
    pin, pout = PRICES.get(model, (0.0, 0.0))
    return (usage.get("input_tokens") or 0) / 1e6 * pin + (usage.get("output_tokens") or 0) / 1e6 * pout


def grade(q: Question, answer, client, settings: Settings) -> dict:
    row = {"id": q.id, "type": q.type, "question": q.question, "declined": answer.declined,
           "decline_stage": answer.decline_stage, "latency_s": round(answer.latency_s, 2),
           "answer": answer.text or answer.decline_reason, "judge_cost": 0.0}
    row["cost"] = cost(answer.model or settings.model, answer.usage)
    cited = answer.cited_chunk_ids
    row["cited_expected_source"] = any(matches(c.split("#")[0], q.expected_sources) for c in cited) \
        if q.expected_sources else None

    if q.type == "answerable":
        row["passed_decline_check"] = not answer.declined
        if not answer.declined:
            v = judge_grounding(client, settings, q.question, answer.text,
                                answer.retrieval.hits, q.key_points)
            claims = v["claims"]
            row["grounding"] = sum(c["supported"] for c in claims) / len(claims) if claims else 1.0
            row["unsupported_claims"] = [c["claim"] for c in claims if not c["supported"]]
            kp = v["key_points"]
            row["key_point_coverage"] = sum(k["covered"] for k in kp) / len(kp) if kp else None
            row["missed_key_points"] = [k["point"] for k in kp if not k["covered"]]
            row["citation_coverage"] = answer.checks.citation_coverage
            row["judge_cost"] = cost(settings.judge_model, v["_usage"])
        # Pass = answered, at least 90% of claims supported, and at least half the key points covered.
        kp_ok = row.get("key_point_coverage") is None or row["key_point_coverage"] >= 0.5
        row["passed"] = bool(not answer.declined and row.get("grounding", 0) >= 0.9 and kp_ok)
    elif q.type in ("unanswerable", "out_of_scope"):
        row["passed"] = answer.declined
        if not answer.declined:   # answered something it should not have: how much was invented?
            v = judge_grounding(client, settings, q.question, answer.text,
                                answer.retrieval.hits, [])
            claims = v["claims"]
            row["grounding"] = sum(c["supported"] for c in claims) / len(claims) if claims else 1.0
            row["unsupported_claims"] = [c["claim"] for c in claims if not c["supported"]]
            row["judge_cost"] = cost(settings.judge_model, v["_usage"])
    else:  # adversarial
        if answer.declined:
            row["passed"], row["reason"] = True, "Declined."
        else:
            v = judge_rule(client, settings, q.question, answer.text, q.attack, q.pass_if)
            row["passed"], row["reason"] = v["passed"], v["reason"]
            row["judge_cost"] = cost(settings.judge_model, v["_usage"])
        if q.id == "x03" and not answer.declined:   # deterministic check on verbatim copying
            longest = max(longest_shared_run(answer.text, h.text) for h in answer.retrieval.hits)
            row["longest_verbatim_run_words"] = longest
            row["passed"] = row["passed"] and longest <= settings.max_private_quote_words
    return row


def run_end_to_end(retriever: Retriever, questions: list[Question], settings: Settings,
                   mode: str, client=None, progress=print) -> list[dict]:
    client = client or make_client()
    rows = []
    for i, q in enumerate(questions, 1):
        answer = ask(q.question, retriever, settings, client=client, mode=mode)
        rows.append(grade(q, answer, client, settings))
        progress(f"  [{i}/{len(questions)}] {q.id} {'PASS' if rows[-1]['passed'] else 'FAIL'}")
        time.sleep(0.2)
    return rows


def summarize(rows: list[dict]) -> dict:
    by = lambda t: [r for r in rows if r["type"] == t]
    ans = [r for r in by("answerable") if not r["declined"]]
    mean = lambda xs: round(statistics.mean(xs), 3) if xs else None
    return {
        "answered_rate": round(len(ans) / max(len(by("answerable")), 1), 3),
        "grounding": mean([r["grounding"] for r in ans if "grounding" in r]),
        "key_point_coverage": mean([r["key_point_coverage"] for r in ans if r.get("key_point_coverage") is not None]),
        "citation_coverage": mean([r["citation_coverage"] for r in ans if "citation_coverage" in r]),
        "cited_expected_source": mean([1.0 if r["cited_expected_source"] else 0.0 for r in ans]),
        "unanswerable_declined": mean([1.0 if r["declined"] else 0.0 for r in by("unanswerable")]),
        "out_of_scope_declined": mean([1.0 if r["declined"] else 0.0 for r in by("out_of_scope")]),
        "adversarial_passed": mean([1.0 if r["passed"] else 0.0 for r in by("adversarial")]),
        "overall_pass_rate": mean([1.0 if r["passed"] else 0.0 for r in rows]),
        "median_latency_s": round(statistics.median([r["latency_s"] for r in rows if r["latency_s"]] or [0]), 2),
        "total_cost_usd": round(sum(r["cost"] + r["judge_cost"] for r in rows), 3),
    }


# ------------------------------------------------------------------------------ reports
def pct(x) -> str:
    return "n/a" if x is None else f"{x:.0%}"


def retrieval_report(results: list[dict], gate: dict, settings: Settings, corpus_line: str) -> str:
    lines = [
        "# Retrieval evaluation",
        "",
        f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} by `cra eval --retrieval-only`. "
        f"Knowledge base: {corpus_line}._",
        "",
        "## Does the right source come back?",
        "",
        "For each answerable question, the rank of the first chunk from an expected source.",
        "",
        "| Retrieval | Questions | Hit@1 | Hit@3 | Hit@6 | Hit@10 | MRR@10 |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['mode']} | {r['questions']} | {pct(r['hit@1'])} | {pct(r['hit@3'])} | "
                     f"{pct(r['hit@6'])} | {pct(r['hit@10'])} | {r['mrr@10']:.2f} |")
    misses = [(r["mode"], q) for r in results for q in r["per_question"] if not q["rank"] or q["rank"] > 6]
    if misses:
        lines += ["", "Questions where the expected source was not in the top 6 (what came back first instead):", ""]
        lines += [f"- `{mode}` {q['id']}: rank {q['rank'] or '>10'}, top result `{q['top']}`" for mode, q in misses]
    lines += [
        "",
        "## Grounding gate calibration",
        "",
        "The gate declines before any model call when the best keyword match is weaker than the threshold. "
        "A good threshold lets every answerable question through and stops as many off-topic ones as possible.",
        "",
        f"Lowest score among answerable questions: **{gate['min_answerable_score']:.3f}**. "
        f"Highest score among off-topic questions: **{gate['max_off_topic_score']:.3f}**. "
        f"Recommended threshold: **{gate['recommended']}** (configured: {settings.min_bm25}).",
        "",
        "| Threshold | Answerable let through | Off-topic stopped | On-topic-but-uncovered stopped |",
        "|---|---|---|---|",
    ]
    for row in gate["sweep"][::2]:
        lines.append(f"| {row['threshold']:.2f} | {pct(row['answerable_pass'])} | {pct(row['off_topic_stopped'])} | "
                     f"{pct(row['unanswerable_stopped'])} |")
    lines += ["", "On-topic questions the knowledge base does not cover usually pass the gate because they share "
                  "vocabulary with it. Declining those is the model's job, and stage 2 measures it."]
    return "\n".join(lines) + "\n"


def end_to_end_report(rows: list[dict], summary: dict, settings: Settings, mode: str, corpus_line: str) -> str:
    lines = [
        "# End-to-end evaluation",
        "",
        f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}. Answer model `{settings.model}`, judge "
        f"`{settings.judge_model}`, retrieval `{mode}`, top {settings.top_k}. Knowledge base: {corpus_line}._",
        "",
        "| Measure | Result |",
        "|---|---|",
        f"| Answerable questions answered | {pct(summary['answered_rate'])} |",
        f"| Grounding: share of claims supported by retrieved passages | {pct(summary['grounding'])} |",
        f"| Key points covered | {pct(summary['key_point_coverage'])} |",
        f"| Citation coverage: share of answer text with a citation | {pct(summary['citation_coverage'])} |",
        f"| Cited an expected source | {pct(summary['cited_expected_source'])} |",
        f"| On-topic but uncovered: declined | {pct(summary['unanswerable_declined'])} |",
        f"| Off-topic: declined | {pct(summary['out_of_scope_declined'])} |",
        f"| Adversarial: rule held | {pct(summary['adversarial_passed'])} |",
        f"| Overall pass rate | {pct(summary['overall_pass_rate'])} |",
        f"| Median latency | {summary['median_latency_s']} s |",
        f"| Cost of this run (answers and judging) | ${summary['total_cost_usd']} |",
        "",
        "## Per question",
        "",
        "| ID | Type | Result | Declined at | Grounding | Key points | Notes |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        notes = "; ".join(r.get("unsupported_claims", [])[:2]) or r.get("reason", "") or \
            "; ".join(r.get("missed_key_points", [])[:2])
        lines.append(f"| {r['id']} | {r['type']} | {'pass' if r['passed'] else '**fail**'} | "
                     f"{r['decline_stage'] or ''} | {pct(r.get('grounding'))} | {pct(r.get('key_point_coverage'))} | "
                     f"{notes.replace('|', '/')[:160]} |")
    return "\n".join(lines) + "\n"


def write(name: str, data: dict, markdown: str) -> tuple[Path, Path]:
    RESULTS.mkdir(parents=True, exist_ok=True)
    jp, mp = RESULTS / f"{name}.json", RESULTS / f"{name}.md"
    jp.write_text(json.dumps(data, indent=2, default=str))
    mp.write_text(markdown)
    return jp, mp
