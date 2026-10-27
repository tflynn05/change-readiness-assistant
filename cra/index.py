"""Build the searchable index from the knowledge base folders."""
from __future__ import annotations

from collections import Counter

from .chunking import Chunk, chunk_documents
from .config import Settings
from .corpus import load_documents
from .retrieve import Retriever


def load_chunks(settings: Settings, errors: list | None = None) -> list[Chunk]:
    docs = load_documents(settings.public_dir, settings.private_dirs, errors)
    if not docs:
        raise RuntimeError(f"No documents in {settings.public_dir}. Run: python scripts/build_corpus.py")
    return chunk_documents(docs)


def build_retriever(settings: Settings, mode: str | None = None) -> Retriever:
    mode = mode or settings.mode
    chunks = load_chunks(settings)
    return Retriever.build(chunks, settings, need_embeddings=mode in ("embed", "hybrid"))


def describe(chunks: list[Chunk]) -> str:
    by_source = Counter(c.source_id for c in chunks)
    docs = len({c.doc_id for c in chunks})
    words = sum(len(c.text.split()) for c in chunks)
    lines = [f"{docs} documents, {len(chunks)} chunks, {words:,} words"]
    lines += [f"  {source:28s} {n:4d} chunks" for source, n in sorted(by_source.items())]
    return "\n".join(lines)
