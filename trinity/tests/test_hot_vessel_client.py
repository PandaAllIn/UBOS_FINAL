from __future__ import annotations

from types import SimpleNamespace
from urllib import error

import pytest

from hot_vessel_client import HotVesselClient


class DummyResponse:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self.headers = SimpleNamespace(get_content_charset=lambda: "utf-8")

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> "DummyResponse":  # pragma: no cover - trivial
        return self

    def __exit__(self, *exc_info) -> None:  # pragma: no cover - trivial
        return None


def test_hot_vessel_client_parses_success(monkeypatch):
    recorded = {}

    def fake_urlopen(request, timeout=0):
        recorded["timeout"] = timeout
        return DummyResponse(b'{"response": "ok"}')

    monkeypatch.setattr("hot_vessel_client.request.urlopen", fake_urlopen)

    client = HotVesselClient("http://example.com", prompt_field="prompt", endpoint="/inference")
    result = client.query("hello", {"task_type": "fast"})

    assert result.ok is True
    assert result.text == "ok"
    assert recorded["timeout"] == client.timeout


def test_hot_vessel_client_handles_failure(monkeypatch):
    def fake_urlopen(*_args, **_kwargs):
        raise error.URLError("boom")

    monkeypatch.setattr("hot_vessel_client.request.urlopen", fake_urlopen)

    client = HotVesselClient("http://example.com", prompt_field="prompt")
    result = client.query("hello")

    assert result.ok is False
    assert result.error == "boom"
    assert result.text == ""
