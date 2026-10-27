"""Optional dense retrieval with a local sentence-transformers model.

Install with `pip install -e ".[embed]"`. The default model (bge-small-en-v1.5)
runs on a laptop CPU and downloads about 130 MB the first time. Nothing is
sent to a third party: embeddings are computed and cached locally.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

QUERY_PREFIX = {"BAAI/bge-small-en-v1.5": "Represent this sentence for searching relevant passages: "}


class Embedder:
    def __init__(self, model_name: str):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "Embedding retrieval needs sentence-transformers: pip install -e \".[embed]\"") from exc
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, batch_size=32, normalize_embeddings=True,
                                 show_progress_bar=len(texts) > 200).astype(np.float32)

    def embed_query(self, text: str) -> np.ndarray:
        prefix = QUERY_PREFIX.get(self.model_name, "")
        return self.model.encode([prefix + text], normalize_embeddings=True)[0].astype(np.float32)


def cached_document_embeddings(embedder, texts: list[str], cache_dir: Path) -> np.ndarray:
    """Embed the corpus once; reuse the cached matrix until the text or model changes."""
    key = hashlib.sha256((embedder.model_name + "\x00" + "\x00".join(texts)).encode()).hexdigest()[:16]
    path = cache_dir / f"embeddings-{key}.npy"
    if path.exists():
        return np.load(path)
    cache_dir.mkdir(parents=True, exist_ok=True)
    matrix = embedder.embed_documents(texts)
    np.save(path, matrix)
    return matrix
