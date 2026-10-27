from pathlib import Path

from cra import evaluate as ev
from cra.config import ROOT
from cra.corpus import PRIVATE_LICENSE, load_private, load_public


def test_public_documents_carry_provenance():
    docs = load_public(ROOT / "corpus" / "public")
    assert len(docs) > 50
    for d in docs:
        assert d.license != "unknown", d.doc_id
        assert d.source_url.startswith("https://"), d.doc_id


def test_private_loader_marks_documents_private(tmp_path: Path):
    (tmp_path / "notes.md").write_text("# Sponsor notes\n\nOur sponsor playbook says to meet weekly.")
    (tmp_path / "plain.txt").write_text("Plain text guidance about reinforcement and recognition.")
    (tmp_path / "README.md").write_text("ignored")
    docs = load_private(tmp_path)
    assert {d.doc_id for d in docs} == {"private/notes", "private/plain"}
    assert all(d.private and d.license == PRIVATE_LICENSE for d in docs)
    assert next(d for d in docs if d.doc_id == "private/notes").title == "Sponsor notes"


def test_private_folder_is_git_ignored():
    ignore = (ROOT / ".gitignore").read_text()
    assert "corpus/private/*" in ignore
    assert "!corpus/private/README.md" in ignore


def test_question_file_is_well_formed():
    qs = ev.load_questions()
    assert len({q.id for q in qs}) == len(qs)
    assert {q.type for q in qs} == {"answerable", "unanswerable", "out_of_scope", "adversarial"}
    docs = {d.doc_id for d in load_public(ROOT / "corpus" / "public")}
    for q in qs:
        for prefix in q.expected_sources:
            assert any(d.startswith(prefix) for d in docs), f"{q.id}: {prefix} matches no document"
        if q.type == "answerable":
            assert q.expected_sources and q.key_points, q.id


def test_end_to_end_pipeline_with_fake_client(retriever, settings):
    from tests.conftest import FakeClient
    qs = [q for q in ev.load_questions() if q.id in {"a01", "u03", "o01", "x01"}]
    rows = ev.run_end_to_end(retriever, qs, settings, "bm25", client=FakeClient(), progress=lambda *_: None)
    by_id = {r["id"]: r for r in rows}
    assert by_id["a01"]["passed"] and by_id["a01"]["grounding"] == 1.0
    assert by_id["a01"]["key_point_coverage"] == 1.0
    assert by_id["u03"]["declined"] and by_id["u03"]["decline_stage"] == "model"
    assert by_id["o01"]["decline_stage"] == "retrieval_gate"
    summary = ev.summarize(rows)
    report = ev.end_to_end_report(rows, summary, settings, "bm25", "test corpus")
    assert "| a01 | answerable | pass |" in report


def test_retrieval_metrics_shape(retriever):
    qs = [q for q in ev.load_questions() if q.type == "answerable"][:5]
    m = ev.retrieval_metrics(retriever, qs, "bm25")
    assert m["questions"] == 5 and 0 <= m["mrr@10"] <= 1
