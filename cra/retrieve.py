"""Retrieval: keyword (BM25), embedding, or hybrid; context expansion; the grounding gate.

Search small, read big. Chunks are kept small so scoring is precise, but the
answer to a question often sits next to the passage that matched it: a heading
that names "the headline three" is followed by the table that lists them. So
each match is expanded to its surrounding section (up to CRA_CONTEXT_WORDS)
before it goes to the model, and matches that overlap merge into one passage.

Hybrid mode merges the keyword and embedding rankings with reciprocal rank
fusion, which needs no score calibration between methods. The grounding gate
decides whether the best match is strong enough to answer from at all; if not,
the assistant declines before spending a model call.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .bm25 import BM25
from .chunking import Chunk
from .config import Settings

MODES = ("bm25", "embed", "hybrid")


@dataclass
class Hit:
    chunk: Chunk                      # the best-ranked chunk in this passage
    rank: int
    score: float                      # fused or single-method score used for ranking
    bm25: float = 0.0                 # normalized 0..1
    cosine: float = 0.0
    context: list = field(default_factory=list)   # chunks sent to the model, in document order

    def __post_init__(self):
        if not self.context:
            self.context = [self.chunk]

    @property
    def blocks(self) -> list[str]:
        return [b for c in self.context for b in c.blocks]

    @property
    def text(self) -> str:
        return "\n\n".join(self.blocks)

    @property
    def label(self) -> str:
        tops = {_top_section(c) for c in self.context}
        if len(tops) == 1 and None not in tops:
            return f"{self.chunk.title} › {tops.pop()}"
        return self.chunk.title

    @property
    def chunk_ids(self) -> list[str]:
        return [c.chunk_id for c in self.context]


@dataclass
class Retrieval:
    query: str
    mode: str
    hits: list[Hit]
    top_bm25: float                   # best normalized BM25 among all chunks
    top_cosine: float                 # best cosine among all chunks (0 when not computed)
    grounded: bool                    # passed the grounding gate


def _top_section(chunk: Chunk) -> str | None:
    """The top-level section a chunk belongs to; None for a document's opening text."""
    if not chunk.section or chunk.section == chunk.title:
        return None
    return chunk.section.split(" › ")[0]


def _words(chunk: Chunk) -> int:
    return len(chunk.text.split())


class Retriever:
    def __init__(self, chunks: list[Chunk], settings: Settings, embedder=None,
                 embeddings: np.ndarray | None = None):
        self.chunks = chunks
        self.settings = settings
        self.bm25 = BM25([c.search_text for c in chunks])
        self.embedder = embedder
        self.embeddings = embeddings
        # Position of every chunk within its document, for context expansion.
        self._doc_chunks: dict[str, list[int]] = {}
        for i, c in enumerate(chunks):
            self._doc_chunks.setdefault(c.doc_id, []).append(i)
        self._pos: dict[int, tuple[str, int]] = {}
        for doc_id, idxs in self._doc_chunks.items():
            for n, i in enumerate(idxs):
                self._pos[i] = (doc_id, n)

    @classmethod
    def build(cls, chunks: list[Chunk], settings: Settings, need_embeddings: bool = False) -> "Retriever":
        embedder = embeddings = None
        if need_embeddings:
            from .embeddings import Embedder, cached_document_embeddings
            embedder = Embedder(settings.embed_model)
            embeddings = cached_document_embeddings(
                embedder, [c.search_text for c in chunks], Path(settings.index_dir))
        return cls(chunks, settings, embedder, embeddings)

    # -- scoring ---------------------------------------------------------------------------
    def _bm25_scores(self, query: str) -> np.ndarray:
        raw = np.array(self.bm25.scores(query), dtype=np.float64)
        return raw / self.bm25.max_possible(query)

    def _cosine_scores(self, query: str) -> np.ndarray:
        if self.embedder is None or self.embeddings is None:
            raise RuntimeError("This retriever was built without embeddings; use mode='bm25' "
                               "or build with need_embeddings=True.")
        return self.embeddings @ self.embedder.embed_query(query)

    # -- context expansion -----------------------------------------------------------------
    def expand(self, i: int, budget: int | None = None) -> list[int]:
        """Chunk indices to send for a match on chunk i, in document order.

        1. The whole top-level section the chunk sits in, if it fits the budget;
           otherwise the chunk plus its nearest neighbors in that section.
        2. If the match is a document's opening text or a section that is little more
           than a heading, and the passage is under half the budget, continue into
           the chunks that follow.
        """
        budget = self.settings.context_words if budget is None else budget
        if budget <= 0:
            return [i]
        doc_id, n = self._pos[i]
        idxs = self._doc_chunks[doc_id]
        top = _top_section(self.chunks[i])
        lo = hi = n
        while lo > 0 and _top_section(self.chunks[idxs[lo - 1]]) == top:
            lo -= 1
        while hi < len(idxs) - 1 and _top_section(self.chunks[idxs[hi + 1]]) == top:
            hi += 1
        section = list(range(lo, hi + 1))
        size = lambda ns: sum(_words(self.chunks[idxs[k]]) for k in ns)
        if size(section) <= budget:
            window = section
        else:                                   # grow outward from the match, next side first
            window, left, right = [n], n - 1, n + 1
            while True:
                grew = False
                for side in ("right", "left"):
                    k = right if side == "right" else left
                    if lo <= k <= hi and size(window + [k]) <= budget:
                        window.append(k)
                        if side == "right":
                            right += 1
                        else:
                            left -= 1
                        grew = True
                if not grew:
                    break
            window.sort()
        # A document's opening text, or a section that is little more than a heading, usually
        # leads into what follows ("the headline three are below"), so continue into it.
        lead_in = top is None or size(section) < 60
        nxt = window[-1] + 1
        while lead_in and size(window) < budget // 2 and nxt < len(idxs) and size(window + [nxt]) <= budget:
            window.append(nxt)
            nxt += 1
        return [idxs[k] for k in window]

    # -- search ----------------------------------------------------------------------------
    def search(self, query: str, k: int | None = None, mode: str | None = None) -> Retrieval:
        k = k or self.settings.top_k
        mode = mode or self.settings.mode
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        bm = self._bm25_scores(query)
        cos = self._cosine_scores(query) if mode in ("embed", "hybrid") else np.zeros(len(self.chunks))

        if mode == "bm25":
            ranking = np.argsort(-bm, kind="stable")
            score = bm
        elif mode == "embed":
            ranking = np.argsort(-cos, kind="stable")
            score = cos
        else:
            score = reciprocal_rank_fusion([np.argsort(-bm, kind="stable"), np.argsort(-cos, kind="stable")])
            ranking = np.argsort(-score, kind="stable")

        # Walk the ranking, expanding each match; a match already inside an earlier
        # passage merges into it instead of taking a slot.
        passages: list[tuple[int, list[int]]] = []     # (best chunk, chunk indices)
        for i in ranking:
            i = int(i)
            if any(i in idx for _, idx in passages):
                continue
            ctx = self.expand(i)
            overlap = [p for p in passages if set(p[1]) & set(ctx)]
            if overlap:
                first = overlap[0]
                merged = sorted(set(first[1]) | set(ctx), key=lambda j: self._pos[j][1])
                passages[passages.index(first)] = (first[0], merged)
                continue
            passages.append((i, ctx))
            if len(passages) == k:
                break

        hits = [Hit(chunk=self.chunks[i], rank=r + 1, score=float(score[i]), bm25=float(bm[i]),
                    cosine=float(cos[i]), context=[self.chunks[j] for j in ctx])
                for r, (i, ctx) in enumerate(passages)]
        top_bm, top_cos = float(bm.max(initial=0)), float(cos.max(initial=0))
        return Retrieval(query, mode, hits, top_bm, top_cos, self.passes_gate(mode, top_bm, top_cos))

    def passes_gate(self, mode: str, top_bm25: float, top_cosine: float) -> bool:
        if mode == "bm25":
            return top_bm25 >= self.settings.min_bm25
        if mode == "embed":
            return top_cosine >= self.settings.min_cosine
        return top_bm25 >= self.settings.min_bm25 or top_cosine >= self.settings.min_cosine


def reciprocal_rank_fusion(rankings: list[np.ndarray], k: int = 60) -> np.ndarray:
    """Sum of 1/(k + rank) across rankings; k=60 is the value from the original RRF paper."""
    n = len(rankings[0])
    fused = np.zeros(n)
    for ranking in rankings:
        ranks = np.empty(n)
        ranks[ranking] = np.arange(1, n + 1)
        fused += 1.0 / (k + ranks)
    return fused
