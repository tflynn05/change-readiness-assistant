"""Checks that run around every answer.

Before the model call: the grounding gate (in retrieve.py) and a scan of the
question for prompt-injection phrasing. After the call: how much of the answer
carries citations, which sentences do not, and whether any passage from a
private (licensed) source was quoted at length.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

INJECTION_PATTERNS = [
    r"ignore (all |any |the )?(previous|prior|above|earlier) (instructions|rules|prompts?)",
    r"disregard (your|the|all) (instructions|rules|guidelines)",
    r"(reveal|print|show|repeat) (your|the) (system )?(prompt|instructions)",
    r"you are now\b", r"act as (an? )?(?!change|product)", r"developer mode", r"jailbreak",
    r"pretend (to be|you are)", r"new instructions?:",
]


@dataclass
class CheckResult:
    citation_coverage: float = 1.0
    uncited: list[str] = field(default_factory=list)
    private_quote_words: int = 0
    injection_signals: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


def injection_signals(text: str) -> list[str]:
    lowered = text.lower()
    return [p for p in INJECTION_PATTERNS if re.search(p, lowered)]


def is_substantive(text: str) -> bool:
    """A segment that makes a claim: enough letters, and not only a heading or a connector."""
    stripped = text.strip().strip("*#-:•").strip()
    letters = sum(ch.isalpha() for ch in stripped)
    if letters < 25:
        return False
    if re.fullmatch(r"#+ .*", text.strip()):
        return False
    return True


def citation_coverage(segments) -> tuple[float, list[str]]:
    """Share of substantive answer text (by characters) that carries at least one citation."""
    total = cited = 0
    uncited = []
    for seg in segments:
        if not is_substantive(seg.text):
            continue
        n = len(seg.text.strip())
        total += n
        if seg.citations:
            cited += n
        else:
            uncited.append(seg.text.strip())
    return (cited / total if total else 1.0), uncited


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def longest_shared_run(a: str, b: str) -> int:
    """Length in words of the longest word sequence that appears in both texts."""
    x, y = _words(a), _words(b)
    if not x or not y:
        return 0
    best, prev = 0, [0] * (len(y) + 1)
    for i in range(1, len(x) + 1):
        cur = [0] * (len(y) + 1)
        xi = x[i - 1]
        for j in range(1, len(y) + 1):
            if xi == y[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def run_checks(answer_text: str, segments, hits, question: str, settings) -> CheckResult:
    result = CheckResult()
    result.citation_coverage, result.uncited = citation_coverage(segments)
    if result.citation_coverage < settings.min_citation_coverage:
        result.flags.append("low_citation_coverage")
    private_texts = [c.text for h in hits for c in getattr(h, "context", [h.chunk]) if c.private]
    if private_texts:
        result.private_quote_words = max(longest_shared_run(answer_text, t) for t in private_texts)
        if result.private_quote_words > settings.max_private_quote_words:
            result.flags.append("private_quote_limit_exceeded")
    result.injection_signals = injection_signals(question)
    if result.injection_signals:
        result.flags.append("possible_prompt_injection")
    return result
