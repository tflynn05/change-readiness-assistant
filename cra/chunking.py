"""Heading-aware chunking.

Each chunk stays inside one section of one document and carries its heading
path ("Desire is the barrier" under "Root causes by element"), so a retrieved
chunk is readable on its own. A chunk keeps its paragraphs as separate blocks:
the Claude API cites whole blocks, so paragraph-sized blocks give paragraph-sized
citations instead of chunk-sized ones.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .corpus import Document

HEADING = re.compile(r"^(#{1,4})\s+(.+?)\s*#*\s*$")


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    section: str
    blocks: list[str]
    source_id: str
    source_url: str
    license: str
    private: bool = False
    meta: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n\n".join(self.blocks)

    @property
    def search_text(self) -> str:
        """What retrieval sees: title and heading path, then the body."""
        return f"{self.title}\n{self.section}\n\n{self.text}"

    @property
    def label(self) -> str:
        return f"{self.title} › {self.section}" if self.section and self.section != self.title else self.title


def _words(text: str) -> int:
    return len(text.split())


def _split_blocks(lines: list[str]) -> list[str]:
    """Paragraphs separated by blank lines; tables and fenced code stay whole."""
    blocks, current, in_fence = [], [], False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not line.strip() and not in_fence:
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return [b for b in blocks if b]


def _split_oversized(block: str, max_words: int) -> list[str]:
    """Break a block that is too long: tables by rows (repeating the header), prose by sentences."""
    if _words(block) <= max_words:
        return [block]
    lines = block.splitlines()
    if len(lines) > 2 and all(l.lstrip().startswith("|") for l in lines):
        header, rows = lines[:2], lines[2:]
        parts, current = [], []
        for row in rows:
            if current and _words("\n".join(header + current + [row])) > max_words:
                parts.append("\n".join(header + current))
                current = []
            current.append(row)
        if current:
            parts.append("\n".join(header + current))
        return parts
    sentences = re.split(r"(?<=[.!?])\s+", block)
    parts, current = [], []
    for sentence in sentences:
        if current and _words(" ".join(current + [sentence])) > max_words:
            parts.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        parts.append(" ".join(current))
    return parts


def _sections(text: str) -> list[tuple[list[str], list[str]]]:
    """Return (heading path, body lines) for each section, in document order."""
    path: list[tuple[int, str]] = []
    sections: list[tuple[list[str], list[str]]] = []
    body: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else HEADING.match(line)
        if m:
            sections.append(([h for _, h in path], body))
            level, heading = len(m.group(1)), m.group(2).strip()
            path = [(l, h) for l, h in path if l < level] + [(level, heading)]
            body = []
        else:
            body.append(line)
    sections.append(([h for _, h in path], body))
    return sections


def chunk_document(doc: Document, target_words: int = 220, max_words: int = 350,
                   min_section_words: int = 8) -> list[Chunk]:
    chunks: list[Chunk] = []
    for headings, lines in _sections(doc.text):
        blocks = []
        for block in _split_blocks(lines):
            blocks.extend(_split_oversized(block, max_words))
        if sum(_words(b) for b in blocks) < min_section_words:
            continue
        # Drop a leading H1 that only repeats the document title.
        if headings and headings[0].strip().lower() == doc.title.strip().lower():
            headings = headings[1:]
        section = " › ".join(headings) if headings else doc.title
        current: list[str] = []
        for block in blocks:
            if current and _words("\n\n".join(current + [block])) > target_words \
                    and _words("\n\n".join(current)) >= target_words // 3:
                chunks.append(_make(doc, section, current, len(chunks)))
                current = []
            current.append(block)
        if current:
            chunks.append(_make(doc, section, current, len(chunks)))
    return chunks


def _make(doc: Document, section: str, blocks: list[str], n: int) -> Chunk:
    return Chunk(
        chunk_id=f"{doc.doc_id}#{n}",
        doc_id=doc.doc_id,
        title=doc.title,
        section=section,
        blocks=list(blocks),
        source_id=doc.source_id,
        source_url=doc.source_url,
        license=doc.license,
        private=doc.private,
    )


def chunk_documents(docs: list[Document], **kwargs) -> list[Chunk]:
    out: list[Chunk] = []
    for doc in docs:
        out.extend(chunk_document(doc, **kwargs))
    return out
