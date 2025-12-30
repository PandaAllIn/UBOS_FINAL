from __future__ import annotations

from types import SimpleNamespace

import pytest

import trinity.claude_responder as claude_responder
import trinity.gemini_responder as gemini_responder
import trinity.janus_responder as janus_responder
from hot_vessel_client import VesselResponse


class DummyEventStream:
    def log_event(self, *_, **__):
        return None


def test_claude_responder_handles_query(monkeypatch):
    calls = []

    def fake_send(*args, **kwargs):
        calls.append(SimpleNamespace(args=args, kwargs=kwargs))
        return True

    class DummyClient:
        def __init__(self, *_args, **_kwargs) -> None:
            self.queries = []

        def query(self, prompt: str, payload=None):
            self.queries.append((prompt, payload))
            return VesselResponse(
                ok=True,
                text=f"answer:{prompt}",
                raw={"tool_context": "ctx", "tools_executed": ["cmd"]},
            )

    class DummyComms:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        def unpack(self, mark_as_read: bool = True):
            return []

    monkeypatch.setattr(claude_responder, "HotVesselClient", DummyClient)
    monkeypatch.setattr(claude_responder, "CommsHubClient", DummyComms)
    monkeypatch.setattr(claude_responder, "TrinityEventStream", DummyEventStream)
    monkeypatch.setattr(claude_responder, "_send_message", fake_send)

    responder = claude_responder.ClaudeResponder()
    message = {
        "message_id": "msg-test",
        "message_type": "query",
        "payload": {"query": "status"},
        "from_vessel": "gemini",
        "priority": "high",
    }

    responder._process_message(message)

    assert calls, "Responder should send a reply"
    sent = calls[0]
    assert sent.kwargs["from_vessel"] == "claude"
    assert sent.kwargs["to_vessel"] == "gemini"
    assert sent.kwargs["message_type"] == "response"
    assert sent.kwargs["priority"] == "high"
    assert sent.kwargs["payload"]["response"] == "answer:status"
    assert sent.kwargs["payload"]["tool_context"] == "ctx"
    assert sent.kwargs["payload"]["tools_executed"] == ["cmd"]


def test_gemini_responder_handles_task(monkeypatch, tmp_path):
    calls = []

    def fake_send(*args, **kwargs):
        calls.append(SimpleNamespace(args=args, kwargs=kwargs))
        return True

    class DummyClient:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        def query(self, *_args, **_kwargs):  # pragma: no cover - not used
            return VesselResponse(ok=True, text="unused")

    class DummyComms:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        def unpack(self, mark_as_read: bool = True):  # pragma: no cover - not used
            return []

    gemini_skill_dir = tmp_path / "monetization-strategist" / "scripts"
    gemini_skill_dir.mkdir(parents=True)
    script_path = gemini_skill_dir / "main.py"
    script_path.write_text("print('ok')\n", encoding="utf-8")

    monkeypatch.setattr(gemini_responder, "HotVesselClient", DummyClient)
    monkeypatch.setattr(gemini_responder, "CommsHubClient", DummyComms)
    monkeypatch.setattr(gemini_responder, "TrinityEventStream", DummyEventStream)
    monkeypatch.setattr(gemini_responder, "_send_message", fake_send)
    monkeypatch.setattr(gemini_responder, "SKILLS_ROOT", tmp_path)

    responder = gemini_responder.GeminiResponder()
    message = {
        "message_id": "task-1",
        "message_type": "task_assignment",
        "payload": {"skill": "monetization-strategist"},
        "from_vessel": "claude",
    }

    responder._process_message(message)

    assert calls, "Task completion should be reported"
    sent = calls[0]
    assert sent.args[2] == "task_complete"
    result = sent.args[3]["result"]
    assert result["success"] is True
    assert result["returncode"] == 0


def test_janus_responder_status_report(monkeypatch):
    calls = []

    def fake_send(*args, **kwargs):
        calls.append(SimpleNamespace(args=args, kwargs=kwargs))
        return True

    class DummyComms:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        def unpack(self, mark_as_read: bool = True):  # pragma: no cover - not used
            return []

    monkeypatch.setattr(janus_responder, "CommsHubClient", DummyComms)
    monkeypatch.setattr(janus_responder, "TrinityEventStream", DummyEventStream)
    monkeypatch.setattr(janus_responder, "_send_message", fake_send)

    responder = janus_responder.JanusResponder()
    responder.last_results["claude"] = {
        "timestamp": "2025-10-30T18:30:00Z",
        "payload": {"result": "ok"},
    }

    message = {
        "message_id": "status-req",
        "message_type": "status_request",
        "from_vessel": "codex",
        "priority": "normal",
    }

    responder._process_message(message)

    assert calls, "Janus responder should reply to status requests"
    sent = calls[0]
    assert sent.args[0] == "janus"
    assert sent.args[1] == "codex"
    assert sent.args[2] == "response"
    payload = sent.args[3]
    assert "responders" in payload
    assert "claude" in payload["responders"]
