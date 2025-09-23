"""Tests for the Librarian HTTP adapter using a mocked requests session."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import InProcBus
from ai_prime_agent.registry import AgentRegistry
from ai_prime_agent.adapters.librarian_http import register_http_with_prime


class DummyResp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_librarian_http_adapter(monkeypatch):
    reg = AgentRegistry()
    bus = InProcBus(reg)

    # Monkeypatch requests.Session.post inside adapter module
    import ai_prime_agent.adapters.librarian_http as http_mod

    class DummySession:
        def __init__(self):
            self.headers = {}

        def post(self, url, json=None, timeout=None):  # pylint: disable=redefined-builtin
            assert url.endswith("/consult")
            assert "summary" in json
            return DummyResp({
                "recommendations": [{"title": "Blueprint Thinking"}],
                "ubos_alignment_notes": ["Aligned"],
                "confidence": 0.8,
                "mermaid_diagram": "graph TD; A-->B;",
            })

    monkeypatch.setattr(http_mod.requests, "Session", DummySession)

    record = register_http_with_prime(
        agent_id="A-ml-http",
        registry=reg,
        register_handler=lambda agent_id, task, handler: bus.register_handler(agent_id, task, handler),
        base_url="http://localhost:5000",
    )

    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id=record.agent_id,
        task="librarian.consult",
        payload={"summary": "Test consult"},
    )
    ack = bus.dispatch(msg)
    assert getattr(ack, "status", "") == "ACK"
    result = bus.last_result_for(msg.message_id)
    assert result and result["recommendations"] and result.get("mermaid")
