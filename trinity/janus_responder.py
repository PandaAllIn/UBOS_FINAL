#!/usr/bin/env python3
"""Janus coordinator responder that routes COMMS_HUB activity."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from comms_hub_client import CommsHubClient
from trinity_event_stream import TrinityEventStream

POLL_INTERVAL_SECONDS = int(os.getenv("COMMS_POLL_INTERVAL_SECONDS", "30"))
HEALTH_WINDOW_SECONDS = int(os.getenv("JANUS_STATUS_WINDOW_SECONDS", "3600"))
SKILLS_ROOT = Path(os.getenv("TRINITY_SKILLS_PATH", "/srv/janus/trinity/skills"))
MESSAGE_SCRIPT = Path("/srv/janus/02_FORGE/scripts/comms_hub_send.py")
EMERGENCY_FLAG = Path("/srv/janus/EMERGENCY_STOP")
RESPONDERS = ("claude", "gemini", "groq")


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
    script_path = Path(script) if script and Path(script).is_absolute() else SKILLS_ROOT / skill / "scripts" / (script or "main.py")
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


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class JanusResponder:
    """Coordinates responder state and relays messages across the Trinity."""

    def __init__(self) -> None:
        self.events = TrinityEventStream()
        self.comms = CommsHubClient("janus", event_stream=self.events)
        self.running = True
        self.last_results: Dict[str, Dict[str, Any]] = {}
        signal.signal(signal.SIGTERM, self._stop)
        signal.signal(signal.SIGINT, self._stop)

    def _stop(self, _signum: int, _frame: Any) -> None:
        self.running = False

    def _record_result(self, message: Dict[str, Any]) -> None:
        origin = message.get("from_vessel")
        if not origin:
            return
        payload = message.get("payload", {})
        self.last_results[origin] = {
            "timestamp": message.get("timestamp", _utc_now()),
            "payload": payload,
        }

    def _handle_status_request(self, message: Dict[str, Any]) -> None:
        recipient = message.get("from_vessel")
        if not recipient:
            return

        cutoff = time.time() - HEALTH_WINDOW_SECONDS
        status: Dict[str, Any] = {
            "generated_at": _utc_now(),
            "responders": {},
        }
        for responder in RESPONDERS:
            details = self.last_results.get(responder)
            if not details:
                status["responders"][responder] = {"state": "unknown"}
                continue
            ts = details.get("timestamp")
            age_ok = False
            if ts:
                try:
                    age_ok = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp() >= cutoff
                except ValueError:
                    age_ok = False
            status["responders"][responder] = {
                "state": "recent" if age_ok else "stale",
                "last_message": details,
            }

        priority = str(message.get("priority", "normal")).lower()
        _send_message("janus", recipient, "response", status, priority)

    def _handle_task(self, message: Dict[str, Any]) -> None:
        payload = message.get("payload", {})
        action = payload.get("action")
        priority = str(message.get("priority", "normal")).lower()

        if action == "broadcast":
            target = payload.get("target", "broadcast")
            body = payload.get("data", {})
            message_type = payload.get("message_type", "broadcast")
            _send_message("janus", target, message_type, body, priority)
            return

        if action == "skill":
            skill = payload.get("skill")
            script = payload.get("script")
            args = payload.get("args", [])
            if not isinstance(args, list):
                args = [str(args)]
            result = _execute_skill(skill or "", script, [str(arg) for arg in args])
            recipient = message.get("from_vessel")
            if recipient:
                response_payload = {
                    "skill": skill,
                    "script": script,
                    "result": result,
                    "original_message": message.get("message_id"),
                }
                _send_message("janus", recipient, "task_complete", response_payload, priority)
            return

        if action == "emergency_stop":
            EMERGENCY_FLAG.touch(exist_ok=True)
            notice = {
                "issued_at": _utc_now(),
                "reason": payload.get("reason", "Triggered by Janus responder"),
            }
            _send_message("janus", "broadcast", "broadcast", {"emergency": notice}, "high")
            return

        self.events.log_event(
            source="janus_responder",
            event_type="unknown_task",
            data={"message_id": message.get("message_id"), "payload": payload},
        )

    def _handle_broadcast(self, message: Dict[str, Any]) -> None:
        self.events.log_event(
            source="janus_responder",
            event_type="broadcast_received",
            data={"message_id": message.get("message_id"), "payload": message.get("payload", {})},
        )

    def _process_message(self, message: Dict[str, Any]) -> None:
        msg_type = message.get("message_type") or message.get("type")
        if msg_type == "task_complete":
            self._record_result(message)
            return

        if msg_type == "status_request":
            self._handle_status_request(message)
            return

        if msg_type == "task_assignment":
            self._handle_task(message)
            return

        if msg_type == "broadcast":
            self._handle_broadcast(message)
            return

        self.events.log_event(
            source="janus_responder",
            event_type="message_ignored",
            data={"message_id": message.get("message_id"), "message_type": msg_type},
        )

    def run(self) -> None:
        self.events.log_event(source="janus_responder", event_type="started", data={})
        while self.running:
            try:
                messages = self.comms.unpack(mark_as_read=True)
                for message in messages:
                    self._process_message(message)
            except Exception as exc:  # pragma: no cover - main loop guard
                self.events.log_event(
                    source="janus_responder",
                    event_type="loop_error",
                    data={"error": str(exc)},
                )
            time.sleep(POLL_INTERVAL_SECONDS)
        self.events.log_event(source="janus_responder", event_type="stopped", data={})


def main() -> None:
    responder = JanusResponder()
    responder.run()


if __name__ == "__main__":
    main()
