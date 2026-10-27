"""Context expansion: search small chunks, send the surrounding section."""
from cra.chunking import chunk_document
from cra.config import Settings
from cra.corpus import Document
from cra.retrieve import Retriever


def build(text, budget=600):
    doc = Document("src/guide", "Guide", text, "src", "Source", "https://example.org", "CC0")
    s = Settings()
    s.include_private, s.context_words = False, budget
    chunks = chunk_document(doc, target_words=60, max_words=120)
    return Retriever(chunks, s), chunks


def words(n, w="filler"):
    return " ".join([w] * n)


SECTIONED = (
    "Short opening that names the headline three metrics.\n\n"
    "## The headline three\n\n| Metric | Definition |\n|---|---|\n| Active users | " + words(40) + " |\n\n"
    "## Lessons\n\n### 1. First lesson\n\nOne " + words(40) + "\n\n### 2. Second lesson\n\nTwo " + words(40)
    + "\n\n### 3. Third lesson\n\nThree " + words(40) + "\n\n## Unrelated\n\n" + words(80, "other")
)


def test_short_intro_pulls_in_the_following_section():
    r, chunks = build(SECTIONED)
    intro = next(i for i, c in enumerate(chunks) if c.section == "Guide")
    ctx = [chunks[i].section for i in r.expand(intro)]
    assert "The headline three" in ctx


def test_subsection_match_returns_whole_section_when_it_fits():
    r, chunks = build(SECTIONED)
    second = next(i for i, c in enumerate(chunks) if "Second lesson" in c.section)
    sections = {chunks[i].section for i in r.expand(second)}
    assert {"Lessons › 1. First lesson", "Lessons › 2. Second lesson", "Lessons › 3. Third lesson"} <= sections
    assert "Unrelated" not in sections


def test_budget_limits_expansion_and_keeps_the_match():
    r, chunks = build(SECTIONED, budget=90)
    second = next(i for i, c in enumerate(chunks) if "Second lesson" in c.section)
    ctx = r.expand(second)
    assert second in ctx
    assert sum(len(chunks[i].text.split()) for i in ctx) <= 90


def test_zero_budget_disables_expansion():
    r, chunks = build(SECTIONED, budget=0)
    assert r.expand(3) == [3]


def test_overlapping_matches_merge_into_one_passage():
    r, _ = build(SECTIONED)
    hits = r.search("first second third lesson", k=3).hits
    lesson_passages = [h for h in hits if any("lesson" in c.section for c in h.context)]
    assert len(lesson_passages) == 1


def test_passage_blocks_follow_document_order(retriever):
    for h in retriever.search("What does adopted mean for a group?").hits:
        positions = [int(cid.split("#")[1]) for cid in h.chunk_ids]
        assert positions == sorted(positions)
        assert h.chunk.chunk_id in h.chunk_ids


def test_regression_metric_table_reaches_the_model(retriever):
    """Run 1 failure a15: the heading naming the headline three was found, the table was not."""
    hits = retriever.search("What are the headline adoption metrics for a platform rollout?").hits
    assert any("tflynn-adoption-metrics/docs__metric-definitions#1" in h.chunk_ids for h in hits)
