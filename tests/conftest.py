"""Shared fixtures. FakeClient stands in for the Claude API so the full pipeline
(answer parsing, guardrails, judging, reports) is testable without a key."""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from cra.config import Settings
from cra.index import build_retriever


@pytest.fixture(scope="session")
def settings() -> Settings:
    s = Settings()
    s.include_private = False
    s.mode = "bm25"
    return s


@pytest.fixture(scope="session")
def retriever(settings):
    return build_retriever(settings)


def _usage():
    return SimpleNamespace(input_tokens=1200, output_tokens=180)


def text_block(text, citations=None):
    return SimpleNamespace(type="text", text=text, citations=citations)


def citation(index, source, title, cited_text):
    return SimpleNamespace(type="search_result_location", search_result_index=index, source=source,
                           title=title, cited_text=cited_text, start_block_index=0, end_block_index=1)


class FakeClient:
    """Records calls; answers with one cited sentence, declines on request, judges generously."""

    def __init__(self, decline_when=("limerick", "kotter"), uncited=False):
        self.decline_when = decline_when
        self.uncited = uncited
        self.calls = []
        self.messages = SimpleNamespace(create=self.create)

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if "format" in kwargs.get("output_config", {}):    # judge call (structured output)
            schema = kwargs["output_config"]["format"]["schema"]
            if "claims" in schema["properties"]:
                prompt = kwargs["messages"][0]["content"]
                points = [l[2:] for l in prompt.split("KEY POINTS:")[1].split("SOURCE PASSAGES:")[0].splitlines()
                          if l.startswith("- ")]
                verdict = {"claims": [{"claim": "c1", "supported": True}, {"claim": "c2", "supported": True}],
                           "key_points": [{"point": p, "covered": True} for p in points]}
            else:
                verdict = {"passed": True, "reason": "Rule held."}
            return SimpleNamespace(content=[text_block(json.dumps(verdict))], usage=_usage())

        content = kwargs["messages"][0]["content"]
        question = content[-1]["text"].lower()
        results = [b for b in content if b["type"] == "search_result"]
        if any(w in question for w in self.decline_when):
            return SimpleNamespace(content=[text_block("INSUFFICIENT_SOURCES: the sources do not cover this.")],
                                   usage=_usage())
        first = results[0]
        cite = None if self.uncited else [citation(0, first["source"], first["title"], first["content"][0]["text"])]
        blocks = [
            text_block("Start with the barrier point and resolve it before scheduling anything else", cite),
            text_block(". "),
            text_block("This sentence makes a claim with no citation attached to it at all."),
        ]
        return SimpleNamespace(content=blocks, usage=_usage())


@pytest.fixture
def fake_client():
    return FakeClient()
