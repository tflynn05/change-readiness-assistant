from cra.answer import SYSTEM_PROMPT, ask, search_result_blocks
from tests.conftest import FakeClient


def test_search_results_sent_as_cited_blocks(retriever, settings, fake_client):
    ask("How should managers handle the job-impact conversation?", retriever, settings, client=fake_client)
    call = fake_client.calls[0]
    assert call["system"] == SYSTEM_PROMPT
    assert call["output_config"] == {"effort": settings.effort}
    assert call["max_tokens"] >= 4000          # thinking counts toward the limit
    content = call["messages"][0]["content"]
    results = [b for b in content if b["type"] == "search_result"]
    assert len(results) == settings.top_k
    assert all(r["citations"] == {"enabled": True} for r in results)   # API requires all-or-nothing
    assert all(r["content"] and all(c["type"] == "text" for c in r["content"]) for r in results)
    assert content[-1] == {"type": "text", "text": "How should managers handle the job-impact conversation?"}


def test_answer_parses_citations_and_renders_sources(retriever, settings, fake_client):
    answer = ask("What is the barrier point in a readiness assessment?", retriever, settings, client=fake_client)
    assert not answer.declined
    assert answer.cited_chunk_ids == [answer.retrieval.hits[0].chunk.chunk_id]
    md = answer.render_markdown()
    assert "[1]" in md and "Sources:" in md
    assert answer.retrieval.hits[0].chunk.source_url in md


def test_gate_declines_without_calling_the_model(retriever, settings, fake_client):
    answer = ask("What's the weather in Chicago tomorrow?", retriever, settings, client=fake_client)
    assert answer.declined and answer.decline_stage == "retrieval_gate"
    assert fake_client.calls == []


def test_model_decline_is_detected(retriever, settings):
    client = FakeClient(decline_when=("kotter",))
    answer = ask("What are the eight steps of Kotter's change model for sponsors?", retriever, settings, client=client)
    assert answer.declined and answer.decline_stage == "model"
    assert "do not cover" in answer.decline_reason


def test_uncited_answer_is_flagged(retriever, settings):
    client = FakeClient(uncited=True)
    answer = ask("What does adopted mean for a group?", retriever, settings, client=client)
    assert "low_citation_coverage" in answer.checks.flags
    assert "treat uncited sentences with care" in answer.render_markdown()


def test_to_dict_is_serializable(retriever, settings, fake_client):
    import json
    answer = ask("What does adopted mean for a group?", retriever, settings, client=fake_client)
    json.dumps(answer.to_dict(), default=str)


def test_blocks_helper_matches_hits(retriever):
    retrieval = retriever.search("sponsor roadmap", k=3)
    blocks = search_result_blocks(retrieval)
    assert [b["source"] for b in blocks] == [h.chunk.source_url for h in retrieval.hits]
