"""Readers for the private knowledge base: PowerPoint, Excel, CSV, Word, and the
CRA_PRIVATE_DIR setting. Office readers are skipped if their package is missing."""
from pathlib import Path

import pytest

from cra.corpus import load_documents, load_private, private_files


def test_csv_becomes_table(tmp_path: Path):
    (tmp_path / "scores.csv").write_text("Corner,Score\nSuccess,15\nSponsorship,14\n")
    doc = load_private(tmp_path)[0]
    assert doc.title == "scores"
    assert "| Corner | Score |" in doc.text and "| Sponsorship | 14 |" in doc.text


def test_hidden_and_unsupported_files_skipped(tmp_path: Path):
    (tmp_path / ".DS_Store").write_bytes(b"\x00")
    (tmp_path / "~$lockfile.docx").write_bytes(b"\x00")
    (tmp_path / "shot.png").write_bytes(b"\x89PNG")
    (tmp_path / "clip.textClipping").write_bytes(b"x")
    (tmp_path / "notes.txt").write_text("Real notes about sponsor coalitions and reinforcement.")
    assert [p.name for p in private_files(tmp_path)] == ["notes.txt"]


def test_bad_file_is_reported_not_fatal(tmp_path: Path):
    pytest.importorskip("pptx")
    (tmp_path / "broken.pptx").write_bytes(b"not really a pptx")
    (tmp_path / "ok.txt").write_text("Usable text about readiness assessments.")
    errors = []
    docs = load_private(tmp_path, errors=errors)
    assert [d.doc_id for d in docs] == ["private/ok"]
    assert errors and errors[0].startswith("broken.pptx")


def test_pptx_slides_titles_bullets_and_notes(tmp_path: Path):
    pptx = pytest.importorskip("pptx")
    prs = pptx.Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Resistance types"
    body = slide.placeholders[1].text_frame
    body.text = "Loss of control"
    p = body.add_paragraph()
    p.text = "Overrides by default"
    p.level = 1
    slide.notes_slide.notes_text_frame.text = "Tie each type to a root cause."
    prs.save(tmp_path / "deck.pptx")
    doc = load_private(tmp_path)[0]
    assert "## Slide 1: Resistance types" in doc.text
    assert "Loss of control" in doc.text and "- Overrides by default" in doc.text
    assert "Speaker notes: Tie each type to a root cause." in doc.text


def test_xlsx_sheets_become_tables(tmp_path: Path):
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sponsor plan"
    ws.append(["Timing", "Sponsor action", None])
    ws.append(["Kickoff", "Deliver the why, live", None])
    ws.append([None, None, None])
    wb.save(tmp_path / "plan.xlsx")
    doc = load_private(tmp_path)[0]
    assert "## Sheet: Sponsor plan" in doc.text
    assert "| Timing | Sponsor action |" in doc.text and "| Kickoff | Deliver the why, live |" in doc.text


def test_docx_headings_and_tables(tmp_path: Path):
    docx = pytest.importorskip("docx")
    d = docx.Document()
    d.add_heading("Working file", level=1)
    d.add_paragraph("Notes on the sponsor conversation.")
    t = d.add_table(rows=2, cols=2)
    t.cell(0, 0).text, t.cell(0, 1).text = "Group", "Barrier"
    t.cell(1, 0).text, t.cell(1, 1).text = "Channel managers", "Desire"
    d.save(tmp_path / "work.docx")
    doc = load_private(tmp_path)[0]
    assert doc.title == "Working file"
    assert "## Working file" in doc.text and "| Channel managers | Desire |" in doc.text


def test_extra_private_dir_keeps_folder_name(tmp_path: Path):
    public = tmp_path / "public"
    public.mkdir()
    default, extra = tmp_path / "private", tmp_path / "Prosci"
    default.mkdir(), extra.mkdir()
    (extra / "notes.txt").write_text("Course notes on reinforcement and sustainment after go-live.")
    docs = load_documents(public, [default, extra])
    assert [(d.doc_id, d.source_url, d.private) for d in docs] == \
        [("private/Prosci/notes", "private:Prosci/notes.txt", True)]


def test_private_dir_setting_resolves_relative_to_project(monkeypatch):
    from cra import config
    monkeypatch.setenv("CRA_PRIVATE_DIR", "../Certifications/Prosci")
    dirs = config._extra_private_dirs()
    assert dirs == [(config.ROOT / "../Certifications/Prosci").resolve()]
