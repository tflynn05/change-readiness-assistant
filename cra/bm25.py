"""Okapi BM25 keyword retrieval, written out in full so it is easy to inspect.

No dependencies. Scores are also reported normalized to 0..1 against the best
score the query could earn, which is what the grounding gate thresholds on.
"""
from __future__ import annotations

import math
import re
from collections import Counter

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been before being below
between both but by can could did do does doing down during each few for from further had has have
having he her here hers herself him himself his how i if in into is it its itself just me more most
my myself no nor not now of off on once only or other our ours ourselves out over own same she should
so some such than that the their theirs them themselves then there these they this those through to
too under until up very was we were what when where which while who whom why will with would you your
yours yourself yourselves us also may might must shall get gets got make makes made use used using
one two three way ways thing things
""".split())


def _stem(token: str) -> str:
    """A light suffix stripper: enough to match 'sponsors' to 'sponsor' and 'training' to 'train'."""
    for suffix, min_len in (("ations", 7), ("ation", 6), ("ingly", 7), ("ings", 6), ("ing", 5),
                            ("ies", 5), ("edly", 6), ("ed", 5), ("ly", 5), ("es", 5), ("s", 4)):
        if token.endswith(suffix) and len(token) >= min_len:
            stem = token[: -len(suffix)]
            if suffix == "ies":
                stem += "y"
            return stem
    return token


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())
    return [_stem(t) for t in tokens if t not in STOPWORDS and len(t) > 1]


class BM25:
    def __init__(self, documents: list[str], k1: float = 1.4, b: float = 0.75):
        self.k1, self.b = k1, b
        self.doc_tokens = [tokenize(d) for d in documents]
        self.doc_len = [len(t) for t in self.doc_tokens]
        self.avgdl = sum(self.doc_len) / max(len(self.doc_len), 1)
        self.tf = [Counter(t) for t in self.doc_tokens]
        df = Counter()
        for tokens in self.doc_tokens:
            df.update(set(tokens))
        n = len(documents)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def _term_score(self, term: str, i: int) -> float:
        f = self.tf[i].get(term, 0)
        if not f:
            return 0.0
        denom = f + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avgdl)
        return self.idf[term] * f * (self.k1 + 1) / denom

    def scores(self, query: str) -> list[float]:
        terms = [t for t in set(tokenize(query)) if t in self.idf]
        return [sum(self._term_score(t, i) for t in terms) for i in range(len(self.doc_tokens))]

    def max_possible(self, query: str) -> float:
        """Upper bound on any document's score for this query, counting unseen terms too.

        A term that appears nowhere in the corpus gets the largest idf, so a question
        about something the knowledge base never mentions normalizes to a low score.
        """
        max_idf = max(self.idf.values(), default=1.0)
        return sum(self.idf.get(t, max_idf) * (self.k1 + 1) for t in set(tokenize(query))) or 1.0

    def normalized(self, query: str, raw_score: float) -> float:
        return raw_score / self.max_possible(query)
