"""Embedding and hybrid modes, with a deterministic fake embedder (no model download)."""
import hashlib

import numpy as np

from cra.retrieve import Retriever


class FakeEmbedder:
    model_name = "fake"

    def _vec(self, text):
        v = np.zeros(64, dtype=np.float32)
        for word in text.lower().split():
            v[int(hashlib.md5(word.encode()).hexdigest(), 16) % 64] += 1
        n = np.linalg.norm(v)
        return v / n if n else v

    def embed_documents(self, texts):
        return np.stack([self._vec(t) for t in texts])

    def embed_query(self, text):
        return self._vec(text)


def make(retriever, settings):
    emb = FakeEmbedder()
    return Retriever(retriever.chunks, settings, emb, emb.embed_documents([c.search_text for c in retriever.chunks]))


def test_embed_and_hybrid_modes_return_ranked_hits(retriever, settings):
    r = make(retriever, settings)
    for mode in ("embed", "hybrid"):
        result = r.search("What does adopted mean for a group?", k=5, mode=mode)
        assert len(result.hits) == 5
        assert [h.rank for h in result.hits] == [1, 2, 3, 4, 5]
        assert all(-1.0 <= h.cosine <= 1.0 for h in result.hits)
        assert result.top_cosine > 0


def test_hybrid_gate_uses_either_signal(retriever, settings):
    r = make(retriever, settings)
    assert r.passes_gate("hybrid", top_bm25=0.0, top_cosine=0.99)
    assert r.passes_gate("hybrid", top_bm25=0.99, top_cosine=0.0)
    assert not r.passes_gate("hybrid", top_bm25=0.0, top_cosine=0.0)


def test_bm25_only_retriever_refuses_embed_mode(retriever):
    import pytest
    with pytest.raises(RuntimeError):
        retriever.search("anything", mode="embed")
