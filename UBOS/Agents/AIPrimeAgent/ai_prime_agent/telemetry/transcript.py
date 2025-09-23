"""
UBOS Blueprint: Transcript Logging (JSONL)

Philosophy: Systems Over Willpower + Environmental Leverage
Strategic Purpose: Persist bus transcripts for auditing, debugging, and
post‑mortems without changing orchestration code.
System Design: Simple JSONL appender with a serializer for bus TranscriptEntry.
Feedback Loops: Transcript data powers reflection and metrics later.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from ai_prime_agent.bus.inproc_bus import TranscriptEntry


def entry_to_dict(entry: TranscriptEntry) -> Dict[str, Any]:
    msg = entry.message
    return {
        "direction": entry.direction,
        "message": {
            "protocol_version": msg.protocol_version,
            "message_id": msg.message_id,
            "correlation_id": msg.correlation_id,
            "timestamp_utc": msg.timestamp_utc,
            "source_agent_id": msg.source_agent_id,
            "destination_agent_id": msg.destination_agent_id,
            "task": msg.task,
            "payload": msg.payload,
            "metadata": msg.metadata,
        },
        "result": entry.result,
        "error": entry.error,
    }


class TranscriptLogger:
    """Append-only JSONL transcript logger."""

    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, entry: TranscriptEntry) -> None:
        payload = entry_to_dict(entry)
        line = json.dumps(payload, ensure_ascii=False)
        with self._path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


__all__ = ["TranscriptLogger", "entry_to_dict"]

