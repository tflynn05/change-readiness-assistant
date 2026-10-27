import numpy as np
import pytest

from cra.bm25 import BM25, tokenize
from cra.retrieve import reciprocal_rank_fusion


@pytest.mark.parametrize("query, expected_doc", [
    ("What does adopted mean for a group?", "tflynn-adoption-metrics/docs__metric-definitions"),
    ("Who should deliver the why message and who explains job impact?",
     "tflynn-change-management/change-management__references__comms-training-plan"),
    ("How do I run a hopes and fears exercise?", "18f-methods/methods__discover__hopes-and-fears"),
    ("single product owner authority accountable for the service", "usds-playbook/_plays__06"),
])
def test_expected_document_in_top_three(retriever, query, expected_doc):
    hits = retriever.search(query, k=3).hits
    assert any(h.chunk.doc_id == expected_doc for h in hits), [h.chunk.doc_id for h in hits]


@pytest.mark.parametrize("query", ["What's the weather in Chicago tomorrow?", "Which bank stock should I buy?"])
def test_gate_stops_off_topic(retriever, query):
    assert retriever.search(query).grounded is False


def test_gate_passes_on_topic(retriever):
    assert retriever.search("What should the sponsor do after go-live?").grounded is True


def test_tokenizer_stems_and_drops_stopwords():
    assert tokenize("The sponsors are training managers") == ["sponsor", "train", "manager"]


def test_bm25_prefers_matching_document():
    bm = BM25(["sponsor coalition roadmap", "weather forecast rain", "coalition of unit leaders"])
    scores = bm.scores("coalition sponsor")
    assert scores.index(max(scores)) == 0
    assert 0 < bm.normalized("coalition sponsor", max(scores)) < 1


def test_unknown_terms_lower_normalized_score():
    bm = BM25(["sponsor coalition roadmap", "weather forecast rain", "coalition leaders"])
    s_known = bm.normalized("sponsor", max(bm.scores("sponsor")))
    s_mixed = bm.normalized("sponsor limerick", max(bm.scores("sponsor limerick")))
    assert s_mixed < s_known


def test_reciprocal_rank_fusion_rewards_agreement():
    a = np.array([0, 1, 2, 3])          # item 0 ranked first
    b = np.array([1, 0, 3, 2])          # item 1 ranked first
    fused = reciprocal_rank_fusion([a, b])
    assert set(np.argsort(-fused)[:2]) == {0, 1}
    assert fused[0] == pytest.approx(fused[1])
