"""Structured logging utilities for Janus agent harness."""
from __future__ import annotations

import json
import queue
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


@dataclass(slots=True)
class LogEvent:
    """Structured event emitted by the agent harness."""

    timestamp: str
    level: str
    vessel: str
    event: str
    data: dict[str, Any]

    @classmethod
    def create(
        cls,
        level: str,
        vessel: str,
        event: str,
        data: Optional[dict[str, Any]] = None,
    ) -> "LogEvent":
        return cls(
            timestamp=datetime.now(timezone.utc).strftime(ISO_FORMAT),
            level=level.upper(),
            vessel=vessel,
            event=event,
            data=data or {},
        )


class AuditLogger:
    """Async-ish audit logger using a background writer thread.

    This keeps I/O off the execution path for agent actions while guaranteeing the
    log file exists immediately for tailing and Fluent Bit ingestion.
    """

    def __init__(self, log_path: Path, flush_interval: float = 1.0) -> None:
        self.log_path = log_path
        self.flush_interval = flush_interval
        self._queue: "queue.Queue[LogEvent]" = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, name="AuditLogger", daemon=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._thread.start()

    def _run(self) -> None:
        buffer: list[LogEvent] = []
        while not self._stop_event.is_set():
            try:
                event = self._queue.get(timeout=self.flush_interval)
                buffer.append(event)
            except queue.Empty:
                pass

            if buffer:
                self._write(buffer)
                buffer.clear()

    def _write(self, events: Iterable[LogEvent]) -> None:
        with self.log_path.open("a", encoding="utf-8") as handle:
            for event in events:
                json.dump(asdict(event), handle, separators=(",", ":"))
                handle.write("\n")

    def emit(self, event: LogEvent) -> None:
        self._queue.put(event)

    def close(self) -> None:
        self._stop_event.set()
        self._thread.join(timeout=self.flush_interval * 2)
        if not self._queue.empty():
            self._write(list(self._queue.queue))

    def __enter__(self) -> "AuditLogger":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        self.close()


def log_exception(logger: AuditLogger, vessel: str, event: str, exc: BaseException) -> None:
    logger.emit(
        LogEvent.create(
            level="error",
            vessel=vessel,
            event=event,
            data={"error": repr(exc)},
        )
    )
