from __future__ import annotations

import json
import time
import uuid
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence, Dict
from tempfile import NamedTemporaryFile


@dataclass(frozen=True)
class RhythmDefinition:
    """Describes how a rhythm should be transmitted and detected."""

    name: str
    repeat_count: int
    cadence_seconds: float
    detection_window_seconds: float
    filename_prefix: str
    description: str


# Canonical rhythm catalogue for Phase 1.
RHYTHMS: Dict[str, RhythmDefinition] = {
    "standard": RhythmDefinition(
        name="standard",
        repeat_count=1,
        cadence_seconds=0.0,
        detection_window_seconds=5.0,
        filename_prefix="msg",
        description="Single write, default priority.",
    ),
    "urgent_burst": RhythmDefinition(
        name="urgent_burst",
        repeat_count=3,
        cadence_seconds=0.3,
        detection_window_seconds=1.0,
        filename_prefix="burst",
        description="Triple tap within one second signalling urgent attention.",
    ),
    "heartbeat": RhythmDefinition(
        name="heartbeat",
        repeat_count=1,
        cadence_seconds=0.0,
        detection_window_seconds=5.0,
        filename_prefix="heartbeat",
        description="Periodic keep-alive, typically emitted hourly.",
    ),
    "constitutional_alarm": RhythmDefinition(
        name="constitutional_alarm",
        repeat_count=5,
        cadence_seconds=0.1,
        detection_window_seconds=1.0,
        filename_prefix="alarm",
        description="Five rapid strikes (0.1s cadence) indicating sanctuary breach conditions.",
    ),
}


@dataclass(frozen=True)
class RhythmDetection:
    """Result returned when the detector recognises a pattern."""

    pattern: str
    message_id: str
    files: List[Path]
    first_timestamp: float
    last_timestamp: float


class TalkingDrumTransmitter:
    """Filesystem-based transmitter for Holographic Puck rhythms."""

    def __init__(
        self,
        agent_name: str,
        *,
        comms_root: Path | str = Path("03_OPERATIONS/COMMS_HUB"),
        rhythm_log_path: Optional[Path | str] = None,
    ) -> None:
        self.agent_name = agent_name
        self.comms_root = Path(comms_root)
        self.outbox_path = self.comms_root / agent_name / "outbox"
        self.outbox_path.mkdir(parents=True, exist_ok=True)

        if rhythm_log_path is None:
            rhythm_log_path = self.comms_root / "logs" / "rhythm_log.jsonl"
        self.rhythm_log_path = Path(rhythm_log_path)
        self.rhythm_log_path.parent.mkdir(parents=True, exist_ok=True)

    def transmit(
        self,
        puck: Mapping[str, Any],
        *,
        recipient: str,
        rhythm: str = "standard",
        symbols_used: Optional[Sequence[str]] = None,
        tone: Optional[str] = None,
    ) -> List[Path]:
        """
        Emit a puck to the recipient inbox using the requested rhythm.

        The puck is first archived in the sender's outbox to preserve provenance.
        """
        rhythm_def = self._get_rhythm(rhythm)

        message_id = self._generate_message_id(rhythm_def)
        payload_hash = self._hash_payload(puck)

        outbox_file = self.outbox_path / f"{message_id}.{rhythm_def.name}.json"
        self._write_json(outbox_file, puck)

        inbox_path = self.comms_root / recipient / "inbox"
        inbox_path.mkdir(parents=True, exist_ok=True)

        written_files: List[Path] = []
        for index in range(rhythm_def.repeat_count):
            suffix = (
                f"{index + 1:02d}of{rhythm_def.repeat_count}"
                if rhythm_def.repeat_count > 1
                else "single"
            )
            filename = (
                f"{message_id}.{rhythm_def.name}.{suffix}.json"
            )
            destination = inbox_path / filename
            self._write_json(destination, puck)
            written_files.append(destination)

            if (
                index < rhythm_def.repeat_count - 1
                and rhythm_def.cadence_seconds > 0.0
            ):
                time.sleep(rhythm_def.cadence_seconds)

        self._append_log(
            event="transmit",
            data={
                "agent": self.agent_name,
                "recipient": recipient,
                "rhythm": rhythm_def.name,
                "message_id": message_id,
                "tone": tone,
                "symbols": list(symbols_used or []),
                "files": [str(path) for path in written_files],
                "payload_hash": payload_hash,
                "repeat_count": rhythm_def.repeat_count,
                "cadence_seconds": rhythm_def.cadence_seconds,
                "timestamp": self._utc_now(),
            },
        )

        return written_files

    @staticmethod
    def detect_rhythm(inbox_path: Path, lookback_seconds: float = 2.0) -> Optional[RhythmDetection]:
        """
        Inspect the inbox and attempt to classify the most recent transmission.
        """
        inbox_path = Path(inbox_path)
        if not inbox_path.exists():
            return None

        now = time.time()
        candidates = sorted(
            (f for f in inbox_path.glob("*.json") if f.is_file()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )

        grouped: Dict[str, List[Path]] = {}
        for file_path in candidates:
            stem_parts = file_path.stem.split(".")
            if len(stem_parts) < 2:
                continue
            message_id = stem_parts[0]
            pattern = stem_parts[1]
            if now - file_path.stat().st_mtime > lookback_seconds:
                continue
            grouped.setdefault((message_id, pattern), []).append(file_path)

        for (message_id, pattern), files in grouped.items():
            rhythm_def = RHYTHMS.get(pattern)
            if rhythm_def is None:
                continue
            if len(files) < rhythm_def.repeat_count:
                continue

            recent_files = sorted(files, key=lambda path: path.stat().st_mtime)
            timestamps = [path.stat().st_mtime for path in recent_files[: rhythm_def.repeat_count]]
            if (
                rhythm_def.repeat_count == 1
                or timestamps[-1] - timestamps[0] <= rhythm_def.detection_window_seconds
            ):
                detection = RhythmDetection(
                    pattern=pattern,
                    message_id=message_id,
                    files=recent_files[: rhythm_def.repeat_count],
                    first_timestamp=timestamps[0],
                    last_timestamp=timestamps[rhythm_def.repeat_count - 1],
                )
                TalkingDrumTransmitter._append_static_log(
                    rhythm_log_path=inbox_path.parent.parent / "logs" / "rhythm_log.jsonl",
                    event="detect",
                    data={
                        "recipient": inbox_path.parent.name,
                        "pattern": pattern,
                        "message_id": message_id,
                        "files": [str(path) for path in detection.files],
                        "first_timestamp": detection.first_timestamp,
                        "last_timestamp": detection.last_timestamp,
                        "timestamp": TalkingDrumTransmitter._utc_now(),
                    },
                )
                return detection

        return None

    # Internal helpers -----------------------------------------------------

    def _get_rhythm(self, rhythm: str) -> RhythmDefinition:
        try:
            return RHYTHMS[rhythm]
        except KeyError as exc:
            raise ValueError(f"Unknown rhythm '{rhythm}'. Known rhythms: {', '.join(RHYTHMS)}") from exc

    def _generate_message_id(self, rhythm_def: RhythmDefinition) -> str:
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        slug = uuid.uuid4().hex[:8]
        return f"{self.agent_name}-{rhythm_def.filename_prefix}-{timestamp}-{slug}"

    @staticmethod
    def _hash_payload(puck: Mapping[str, Any]) -> str:
        digest = hashlib.sha256(json.dumps(puck, sort_keys=True).encode("utf-8")).hexdigest()
        return digest

    def _write_json(self, destination: Path, payload: Mapping[str, Any]) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(destination.parent)) as temp_file:
            json.dump(payload, temp_file, ensure_ascii=False, separators=(",", ":"))
            temp_file.flush()
        Path(temp_file.name).replace(destination)

    def _append_log(self, event: str, data: Mapping[str, Any]) -> None:
        self.rhythm_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.rhythm_log_path.open("a", encoding="utf-8") as handle:
            record = {"event": event, **data}
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    @staticmethod
    def _append_static_log(rhythm_log_path: Path, event: str, data: Mapping[str, Any]) -> None:
        rhythm_log_path.parent.mkdir(parents=True, exist_ok=True)
        with rhythm_log_path.open("a", encoding="utf-8") as handle:
            record = {"event": event, **data}
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(tz=timezone.utc).isoformat()
