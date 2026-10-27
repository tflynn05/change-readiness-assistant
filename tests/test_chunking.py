from cra.chunking import _split_oversized, chunk_document
from cra.corpus import Document


def doc(text, title="Guide"):
    return Document("src/guide", title, text, "src", "Source", "https://example.org", "CC0")


def test_heading_path_is_kept():
    text = "# Guide\n\nIntro paragraph with enough words to count as content here.\n\n" \
           "## Roles\n\n### Sponsor\n\nThe sponsor delivers the why in person and names the coalition early."
    chunks = chunk_document(doc(text))
    assert chunks[0].section == "Guide"                     # repeated H1 dropped, falls back to title
    assert chunks[-1].section == "Roles › Sponsor"
    assert chunks[-1].label == "Guide › Roles › Sponsor"


def test_blocks_stay_paragraph_sized_for_citations():
    text = "## A\n\n" + "\n\n".join(f"Paragraph {i} " + "word " * 30 for i in range(3))
    chunk = chunk_document(doc(text))[0]
    assert len(chunk.blocks) == 3


def test_long_sections_split_near_target():
    text = "## A\n\n" + "\n\n".join("sentence " * 60 for _ in range(10))
    chunks = chunk_document(doc(text), target_words=220, max_words=350)
    assert len(chunks) >= 3
    assert all(len(c.text.split()) <= 350 for c in chunks)


def test_oversized_table_repeats_header():
    rows = "\n".join(f"| cause {i} | " + "action " * 20 + "|" for i in range(30))
    table = "| Cause | Action |\n|---|---|\n" + rows
    parts = _split_oversized(table, max_words=120)
    assert len(parts) > 1
    assert all(p.startswith("| Cause | Action |\n|---|---|") for p in parts)


def test_empty_sections_dropped():
    text = "## Empty\n\n## Real\n\nThis section has real content that should become a chunk."
    chunks = chunk_document(doc(text))
    assert [c.section for c in chunks] == ["Real"]


def test_fenced_code_headings_ignored():
    text = "## Run it\n\n```\n# not a heading\npython run.py\n```\n\nThen read the output carefully."
    chunks = chunk_document(doc(text))
    assert all(c.section == "Run it" for c in chunks)
