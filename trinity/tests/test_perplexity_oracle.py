from __future__ import annotations

import pytest

from perplexity_oracle import PerplexityOracle


class FakeAgent:
    def __init__(self, response: object) -> None:
        self.response = response
        self.calls: list[dict[str, object]] = []

    def research(self, **kwargs):  # type: ignore[override]
        self.calls.append(kwargs)
        # Return deep copy-like structure when dict to avoid mutation side effects
        if isinstance(self.response, dict):
            return dict(self.response)
        return self.response


def build_oracle(response: object) -> tuple[PerplexityOracle, FakeAgent]:
    agent = FakeAgent(response)
    oracle = PerplexityOracle(api_key="test", agent=agent)
    return oracle, agent


def success_payload(model: str = "sonar-pro") -> dict:
    return {
        "content": "Summary of findings",
        "model_used": model,
        "research_id": "abc123",
        "citations": ["https://example.com"],
        "usage": {"tokens": 42},
    }


def error_payload(message: str = "boom") -> dict:
    return {"error": True, "error_type": "BoomError", "error_message": message, "suggestions": ["Retry later"]}


def test_quick_research_uses_quick_model() -> None:
    oracle, fake = build_oracle(success_payload("sonar"))
    text = oracle.quick_research("latest news")
    assert "Perplexity" in text
    assert fake.calls[0]["depth"] == "quick"
    assert fake.calls[0]["model"] == oracle._mode_to_model["quick"]


def test_deep_research_uses_deep_model() -> None:
    oracle, fake = build_oracle(success_payload("sonar-deep-research"))
    text = oracle.deep_research("complex topic")
    assert "Perplexity" in text
    assert fake.calls[0]["depth"] == "deep"
    assert fake.calls[0]["model"] == oracle._mode_to_model["deep"]


def test_reason_research_uses_reason_model() -> None:
    oracle, fake = build_oracle(success_payload("sonar-reasoning"))
    text = oracle.reason("why is the sky blue")
    assert "Perplexity" in text
    assert fake.calls[0]["depth"] == "medium"
    assert fake.calls[0]["model"] == oracle._mode_to_model["reason"]


def test_research_unknown_mode_defaults_to_auto() -> None:
    oracle, fake = build_oracle(success_payload("auto"))
    text = oracle.research("question", mode="mystery")
    assert "Perplexity" in text
    assert fake.calls[0]["model"] is None


def test_research_json_returns_raw_payload() -> None:
    payload = success_payload()
    oracle, _ = build_oracle(payload)
    result = oracle.research_json("topic", mode="auto")
    assert result == payload


def test_quick_research_json_handles_missing_agent_gracefully() -> None:
    oracle, _ = build_oracle(success_payload())
    oracle._agent = None  # simulate unavailable integration
    result = oracle.quick_research_json("topic")
    assert isinstance(result, str)
    assert "unavailable" in result.lower()


def test_execute_formats_success_payload_with_citations() -> None:
    payload = success_payload()
    oracle, _ = build_oracle(payload)
    text = oracle.quick_research("topic")
    assert "Sources:" in text
    assert "Usage:" in text


def test_execute_formats_error_payload() -> None:
    oracle, fake = build_oracle(error_payload("Rate limited"))
    text = oracle.quick_research("topic")
    assert "BoomError" in text
    assert "Rate limited" in text
    # Ensure agent was invoked once
    assert len(fake.calls) == 1
