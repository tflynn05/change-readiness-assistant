"""Command line: cra index | search | ask | eval | mcp"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import Settings
from .index import build_retriever, describe, load_chunks


def _settings(args) -> Settings:
    s = Settings()
    if getattr(args, "mode", None):
        s.mode = args.mode
    if getattr(args, "k", None):
        s.top_k = args.k
    if getattr(args, "public_only", False):
        s.include_private = False
    return s


def cmd_index(args) -> int:
    s = _settings(args)
    errors: list[str] = []
    chunks = load_chunks(s, errors)
    print(describe(chunks))
    private = [c for c in chunks if c.private]
    for d in s.private_dirs:
        print(f"  private folder: {d}" + ("" if d.exists() else "  (not found)"))
    if private:
        from collections import Counter
        by_file = Counter(c.source_url.removeprefix("private:") for c in private)
        words = {}
        for c in private:
            key = c.source_url.removeprefix("private:")
            words[key] = words.get(key, 0) + len(c.text.split())
        print(f"  private documents: {len(by_file)}, {len(private)} chunks")
        for name, n in sorted(by_file.items()):
            print(f"    {n:4d} chunks {words[name]:7,d} words  {name}")
    else:
        print("  private chunks: 0 (add files to corpus/private/, or set CRA_PRIVATE_DIR)")
    for e in errors:
        print(f"  skipped {e}")
    if s.mode in ("embed", "hybrid"):
        build_retriever(s)
        print(f"Embeddings cached in {s.index_dir}")
    return 0


def cmd_search(args) -> int:
    s = _settings(args)
    retriever = build_retriever(s)
    result = retriever.search(args.query)
    print(f"mode={result.mode} best_bm25={result.top_bm25:.3f} grounded={result.grounded}\n")
    for h in result.hits:
        c = h.chunk
        lock = " [private]" if c.private else ""
        print(f"{h.rank}. {c.label}{lock}\n   {c.source_url}  (bm25 {h.bm25:.3f}"
              + (f", cosine {h.cosine:.3f}" if result.mode != "bm25" else "") + ")")
        preview = " ".join(c.text.split())[:240]
        print(f"   {preview}...\n")
    return 0


def cmd_ask(args) -> int:
    from .answer import ask
    s = _settings(args)
    retriever = build_retriever(s)
    answer = ask(args.question, retriever, s)
    if args.json:
        print(json.dumps(answer.to_dict(), indent=2, default=str))
    else:
        print(answer.render_markdown())
        if args.verbose:
            print(f"\n[{answer.model} | {answer.latency_s:.1f}s | {answer.usage} | "
                  f"citation coverage {answer.checks.citation_coverage:.0%} | flags {answer.checks.flags}]")
    return 0


def cmd_eval(args) -> int:
    from . import evaluate as ev
    s = _settings(args)
    s.include_private = args.include_private
    questions = ev.load_questions(Path(args.questions)) if args.questions else ev.load_questions()
    if args.limit:
        questions = questions[: args.limit]
    chunks = load_chunks(s)
    corpus_line = describe(chunks).splitlines()[0]
    modes = [m.strip() for m in args.modes.split(",")]

    from .retrieve import Retriever
    retriever = Retriever.build(chunks, s, need_embeddings=any(m != "bm25" for m in modes))
    print(f"Retrieval evaluation over {len(questions)} questions ({corpus_line})")
    results = [ev.retrieval_metrics(retriever, questions, m) for m in modes]
    for r in results:
        print(f"  {r['mode']:7s} hit@1 {r['hit@1']:.0%}  hit@3 {r['hit@3']:.0%}  hit@6 {r['hit@6']:.0%}  "
              f"MRR {r['mrr@10']:.2f}")
    gate = ev.gate_sweep(retriever, questions)
    print(f"  gate: answerable min {gate['min_answerable_score']:.3f}, off-topic max "
          f"{gate['max_off_topic_score']:.3f}, recommended threshold {gate['recommended']}")
    suffix = "-private" if args.include_private else ""
    j, m = ev.write(f"retrieval{suffix}", {"retrieval": results, "gate": gate},
                    ev.retrieval_report(results, gate, s, corpus_line))
    print(f"  wrote {m.relative_to(ev.ROOT)}")
    if args.retrieval_only:
        return 0

    mode = args.answer_mode or modes[0]
    print(f"\nEnd-to-end evaluation: answer model {s.model}, judge {s.judge_model}, retrieval {mode}")
    rows = ev.run_end_to_end(retriever, questions, s, mode)
    summary = ev.summarize(rows)
    j, m = ev.write(f"end-to-end{suffix}-{mode}", {"summary": summary, "rows": rows},
                    ev.end_to_end_report(rows, summary, s, mode, corpus_line))
    for key, value in summary.items():
        print(f"  {key:24s} {value}")
    print(f"  wrote {m.relative_to(ev.ROOT)}")
    return 0


def cmd_mcp(args) -> int:
    from .mcp_server import main
    main()
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="cra", description="Change-readiness assistant")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--mode", choices=["bm25", "embed", "hybrid"], help="retrieval method")
        p.add_argument("-k", type=int, help="number of passages to retrieve")
        p.add_argument("--public-only", action="store_true", help="ignore corpus/private/")

    p = sub.add_parser("index", help="load and chunk the knowledge base; cache embeddings if needed")
    common(p)
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("search", help="show what retrieval returns for a query (no API call)")
    p.add_argument("query")
    common(p)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("ask", help="answer a question with citations (needs ANTHROPIC_API_KEY)")
    p.add_argument("question")
    p.add_argument("--json", action="store_true", help="print the full result as JSON")
    p.add_argument("-v", "--verbose", action="store_true")
    common(p)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("eval", help="run the evaluation pipeline")
    p.add_argument("--retrieval-only", action="store_true", help="stage 1 only; no API key needed")
    p.add_argument("--modes", default="bm25", help="retrieval modes to compare, e.g. bm25,embed,hybrid")
    p.add_argument("--answer-mode", help="retrieval mode for the end-to-end run (default: first of --modes)")
    p.add_argument("--questions", help="question file (default eval/questions.yaml)")
    p.add_argument("--limit", type=int, help="run only the first N questions")
    p.add_argument("--include-private", action="store_true",
                   help="include corpus/private/ (results are written with a -private suffix; git ignores them)")
    p.set_defaults(func=cmd_eval)

    p = sub.add_parser("mcp", help="run the MCP server over stdio")
    p.set_defaults(func=cmd_mcp)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
