from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

import pytest

from trinity.config import APIKeys
from trinity.oracle_bridge import OracleBridge, OracleError
from trinity.oracle_cache import OracleCache


class DummyGroq:
    def __init__(self) -> None:
        self.web_search = mock.Mock()
        self.fast_think = mock.Mock()
        self.wolfram = mock.Mock()
        self.available = True

    def is_available(self) -> bool:
        return self.available


def build_bridge(
    *,
    tmp_path: Path,
    groq: DummyGroq | None = None,
    perplexity: mock.Mock | None = None,
    data_commons: mock.Mock | None = None,
) -> OracleBridge:
    groq_client = groq or DummyGroq()
    cache = OracleCache(tmp_path / "oracle-cache")
    error_log = tmp_path / "oracle-errors.jsonl"
    return OracleBridge(
        APIKeys(perplexity="token", groq="token"),
        cache=cache,
        error_log_path=error_log,
        groq_client=groq_client,
        perplexity_client=perplexity,
        data_commons=data_commons,
        wolfram_client=None,
    )


def test_research_prefers_perplexity(tmp_path: Path) -> None:
    groq = DummyGroq()
    groq.web_search.return_value = {"results": []}
    perplexity = mock.Mock()
    perplexity.research.return_value = "Perplexity success"

    bridge = build_bridge(tmp_path=tmp_path, groq=groq, perplexity=perplexity)

    result = bridge.research("test query")

    assert "Perplexity success" in result
    perplexity.research.assert_called_once()
    assert groq.web_search.call_count == 0


def test_research_falls_back_to_groq(tmp_path: Path) -> None:
    groq = DummyGroq()
    groq.web_search.return_value = {
        "results": [
            {"title": "Example", "url": "https://example.com", "snippet": "Sample snippet"},
        ]
    }
    perplexity = mock.Mock()
    perplexity.research.side_effect = RuntimeError("service down")

    bridge = build_bridge(tmp_path=tmp_path, groq=groq, perplexity=perplexity)

    result = bridge.research("fallback query")

    assert "[Fallback: Groq web]" in result
    groq.web_search.assert_called_once()


def test_research_uses_cache_on_subsequent_calls(tmp_path: Path) -> None:
    groq = DummyGroq()
    groq.web_search.return_value = {"results": []}
    perplexity = mock.Mock()
    perplexity.research.return_value = "Cached success"

    bridge = build_bridge(tmp_path=tmp_path, groq=groq, perplexity=perplexity)

    first = bridge.research("cache me")
    assert "Cached success" in first

    # Modify behaviour to ensure we hit the cache on second call
    perplexity.research.side_effect = AssertionError("Perplexity should not be called again")

    second = bridge.research("cache me")
    assert second == first


def test_query_economics_fallback_to_groq(tmp_path: Path) -> None:
    groq = DummyGroq()
    groq.web_search.return_value = {
        "results": [
            {"title": "GDP", "url": "https://example.com/gdp", "snippet": "GDP per capita 45k (2024)"},
        ]
    }
    groq.fast_think.return_value = "GDP per capita: €45K (2024) — source example.com"

    data_commons = mock.Mock()
    data_commons.query_economics.return_value = "Data Commons economics unavailable for test."

    bridge = build_bridge(tmp_path=tmp_path, groq=groq, data_commons=data_commons)

    result = bridge.query_economics("country/ROU")

    assert "Groq economic synthesis" in result
    groq.fast_think.assert_called_once()


def test_oracle_error_logged_when_all_fail(tmp_path: Path) -> None:
    groq = DummyGroq()
    groq.available = False
    groq.web_search.side_effect = RuntimeError("groq down")

    perplexity = mock.Mock()
    perplexity.research.side_effect = RuntimeError("perplexity down")

    bridge = build_bridge(tmp_path=tmp_path, groq=groq, perplexity=perplexity)

    with pytest.raises(OracleError) as exc:
        bridge.research("complete failure")

    assert "All research oracles failed" in str(exc.value)

    error_log = tmp_path / "oracle-errors.jsonl"
    assert error_log.exists()
    lines = error_log.read_text(encoding="utf-8").strip().splitlines()
    assert lines
    payload = json.loads(lines[-1])
    assert payload["oracle"] == "perplexity"
    assert "Perplexity" in "\n".join(payload["attempts"])
