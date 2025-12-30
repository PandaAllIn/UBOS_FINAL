from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List

from config import TrinityPaths, load_configuration


@dataclass
class TrinityEventStream:
    def __init__(self) -> None:
        paths, _ = load_configuration()
        self.paths: TrinityPaths = paths
        self.log_file: Path = self.paths.log_dir / "events.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, *, source: str, event_type: str, data: dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": source,
            "event_type": event_type,
            "data": data,
        }
        try:
            with self.log_file.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=True) + "\n")
        except Exception:
            pass

    def get_recent_events(self, limit: int = 50) -> List[dict]:
        try:
            lines = self.log_file.read_text(encoding="utf-8").splitlines()[-limit:]
            return [json.loads(line) for line in lines if line.strip()]
        except Exception:
            return []

