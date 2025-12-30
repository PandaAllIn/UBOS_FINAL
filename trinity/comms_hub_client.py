from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

from config import TrinityPaths, load_configuration


@dataclass
class CommsHubClient:
    resident: str
    event_stream: Any | None = None

    def __init__(self, resident: str, event_stream: Any | None = None) -> None:
        self.resident = resident
        self.event_stream = event_stream
        self.paths, _ = load_configuration()

    def pack(self, *, recipient: str, payload: dict[str, Any], priority: str = "normal", tone: str = "") -> str:
        script = Path("/srv/janus/02_FORGE/scripts/comms_hub_send.py")
        cmd = [
            "/usr/bin/env",
            "python3",
            str(script),
            "--from",
            self.resident,
            "--to",
            recipient,
            "--type",
            "response",
            "--payload",
            json.dumps({"tone": tone, **payload}, ensure_ascii=True),
            "--priority",
            priority,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if self.event_stream:
            self.event_stream.log_event(source=self.resident, event_type="comms.pack", data={"recipient": recipient, "ok": proc.returncode == 0})
        return "ok" if proc.returncode == 0 else "error"

    def unpack(self, *, mark_as_read: bool = True) -> List[dict]:
        inbox = self.paths.comms_hub / self.resident / "inbox"
        msgs: List[dict] = []
        if not inbox.exists():
            return msgs
        for f in sorted(inbox.glob("*.msg.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                msgs.append(data)
                if mark_as_read:
                    archive = inbox.parent / "archive"
                    archive.mkdir(parents=True, exist_ok=True)
                    f.rename(archive / f.name)
            except Exception:
                continue
        if self.event_stream:
            self.event_stream.log_event(source=self.resident, event_type="comms.unpack", data={"count": len(msgs)})
        return msgs

