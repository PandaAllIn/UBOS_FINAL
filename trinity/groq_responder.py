#!/usr/bin/env python3
"""Groq responder daemon for high-speed Trinity tasks via the hot vessel API."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from comms_hub_client import CommsHubClient
from trinity_event_stream import TrinityEventStream
from groq_resident import GroqResident # Import the local GroqResident class

POLL_INTERVAL_SECONDS = int(os.getenv("COMMS_POLL_INTERVAL_SECONDS", "30"))
SKILLS_ROOT = Path(os.getenv("TRINITY_SKILLS_PATH", "/srv/janus/trinity/skills"))
MESSAGE_SCRIPT = Path("/srv/janus/02_FORGE/scripts/comms_hub_send.py")


def _float_env(var: str, default: str) -> float:
    try:
        return float(os.getenv(var, default))
    except (TypeError, ValueError):
        return float(default)


def _int_env(var: str, default: str) -> int:
    try:
        return int(float(os.getenv(var, default)))
    except (TypeError, ValueError):
        return int(default)


def _send_message(from_vessel: str, to_vessel: str, message_type: str, payload: Dict[str, Any], priority: str) -> bool:
    cmd = [
        sys.executable,
        str(MESSAGE_SCRIPT),
        "--from",
        from_vessel,
        "--to",
        to_vessel,
        "--type",
        message_type,
        "--payload",
        json.dumps(payload, ensure_ascii=True),
        "--priority",
        priority,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.returncode == 0


def _execute_skill(skill: str, script: str | None, args: List[str]) -> Dict[str, Any]:
    script_path = (
        Path(script)
        if script and Path(script).is_absolute()
        else SKILLS_ROOT / skill / "scripts" / (script or "main.py")
    )
    if not script_path.exists():
        return {
            "success": False,
            "returncode": 127,
            "stdout": "",
            "stderr": f"Skill script not found: {script_path}",
        }

    proc = subprocess.run(
        [sys.executable, str(script_path), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    max_len = int(os.getenv("COMMS_MAX_LOG_CHARS", "4000"))
    return {
        "success": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-max_len:],
        "stderr": proc.stderr[-max_len:],
    }


class GroqResponder:
    """Processes COMMS_HUB messages directed at the Groq vessel."""

    def __init__(self) -> None:
        self.events = TrinityEventStream()
        # Initialize ResidentGroq directly
        self.resident = GroqResident()
        self.comms = CommsHubClient("groq", event_stream=self.events)
        self.running = True
        signal.signal(signal.SIGTERM, self._stop)
        signal.signal(signal.SIGINT, self._stop)

    def _stop(self, _signum: int, _frame: Any) -> None:
        self.running = False

    def _handle_query(self, message: Dict[str, Any], payload: Dict[str, Any]) -> None:
        query = payload.get("query")
        recipient = message.get("from_vessel")
        if not query or not recipient:
            return

        # Use resident.route_and_respond directly
        response_data = self.resident.route_and_respond("comms_hub_query", query)
        response_text = response_data.get("answer", "Groq resident returned no content.")
        
        # Log event for monitoring
        self.events.log_event(
            source="groq_responder",
            event_type="resident_response",
            data={
                "ok": True, # Assume ok if answer is returned
                "model": response_data.get("model"),
                "task": response_data.get("task"),
                "preview": response_text[:100],
            },
        )

        response_payload: Dict[str, Any] = {
            "query": query,
            "response": response_text,
            "original_message": message.get("message_id"),
        }
        # Add any tool context or other data from route_and_respond if available
        if "tool_context" in response_data:
            response_payload["tool_context"] = response_data["tool_context"]
        if "tools_executed" in response_data:
            response_payload["tools_executed"] = response_data["tools_executed"]

        priority = str(message.get("priority", "normal")).lower()
        _send_message(
            from_vessel="groq",
            to_vessel=recipient,
            message_type="response",
            payload=response_payload,
            priority=priority,
        )

    def _handle_task(self, message: Dict[str, Any], payload: Dict[str, Any]) -> None:
        skill = payload.get("skill")
        recipient = message.get("from_vessel")
        if not skill or not recipient:
            return

        script = payload.get("script")
        args = payload.get("args", [])
        if not isinstance(args, list):
            args = [str(args)]

        result = _execute_skill(skill, script, [str(arg) for arg in args])
        priority = str(message.get("priority", "normal")).lower()
        response_payload = {
            "skill": skill,
            "script": script,
            "result": result,
            "original_message": message.get("message_id"),
        }
        _send_message("groq", recipient, "task_complete", response_payload, priority)

    def _process_message(self, message: Dict[str, Any]) -> None:
        msg_type = message.get("message_type") or message.get("type")
        payload = message.get("payload", {})

        if msg_type == "query":
            self._handle_query(message, payload)
        elif msg_type == "task_assignment":
            self._handle_task(message, payload)
        else:
            self.events.log_event(
                source="groq_responder",
                event_type="message_ignored",
                data={"message_id": message.get("message_id"), "message_type": msg_type},
            )

    def run(self) -> None:
        self.events.log_event(source="groq_responder", event_type="started", data={})
        while self.running:
            try:
                messages = self.comms.unpack(mark_as_read=True)
                for message in messages:
                    self._process_message(message)
            except Exception as exc:  # pragma: no cover - main loop guard
                self.events.log_event(
                    source="groq_responder",
                    event_type="loop_error",
                    data={"error": str(exc)},
                )
            time.sleep(POLL_INTERVAL_SECONDS)
        self.events.log_event(source="groq_responder", event_type="stopped", data={})


def main() -> None:
    responder = GroqResponder()
    responder.run()


if __name__ == "__main__":
    main()
