#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


HISTORY_DIRS = [
    Path("/home/balaur/.config/Code/User/History"),
    Path("/home/balaur/.vscode-server/data/User/History"),
]


@dataclass
class HistoryEntry:
    folder: Path
    resource: str
    entry_id: str
    timestamp: int


def iter_history_entries() -> list[HistoryEntry]:
    items: list[HistoryEntry] = []
    for base in HISTORY_DIRS:
        if not base.exists():
            continue
        for entries in base.glob("*/entries.json"):
            try:
                data = json.loads(entries.read_text(encoding="utf-8"))
            except Exception:
                continue
            resource = data.get("resource") or ""
            entries_list = data.get("entries") or []
            for e in entries_list:
                eid = e.get("id")
                ts = int(e.get("timestamp") or 0)
                if not eid:
                    continue
                items.append(HistoryEntry(folder=entries.parent, resource=resource, entry_id=eid, timestamp=ts))
    return items


def restore(dry_run: bool, only_missing: bool, under: str) -> int:
    entries = iter_history_entries()
    # Group by resource
    by_res: dict[str, list[HistoryEntry]] = {}
    for e in entries:
        if under and under not in e.resource:
            continue
        by_res.setdefault(e.resource, []).append(e)

    restored = 0
    for res, lst in by_res.items():
        # Only handle file:/// paths
        if not res.startswith("file://"):
            continue
        # We care primarily about /srv/janus
        target_path = Path(res.replace("file://", ""))
        if under and not str(target_path).startswith(under):
            continue
        # pick the latest by timestamp
        lst.sort(key=lambda x: x.timestamp, reverse=True)
        latest = lst[0]
        src_file = latest.folder / latest.entry_id
        if not src_file.exists():
            continue
        if only_missing and target_path.exists():
            continue
        ts_human = datetime.utcfromtimestamp(latest.timestamp/1000).isoformat() + "Z"
        if dry_run:
            print(f"DRY-RUN restore {src_file} -> {target_path} (ts {ts_human})")
            restored += 1
            continue
        # ensure directory
        target_path.parent.mkdir(parents=True, exist_ok=True)
        # if exists, write .restored copy
        if target_path.exists():
            suffix = f".restored-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
            target_path = Path(str(target_path) + suffix)
        data = src_file.read_bytes()
        target_path.write_bytes(data)
        print(f"Restored {res} from {src_file} -> {target_path}")
        restored += 1
    return restored


def main() -> int:
    ap = argparse.ArgumentParser(description="Restore files from VS Code Local History")
    ap.add_argument("--dry-run", action="store_true", help="Only print intended actions")
    ap.add_argument("--only-missing", action="store_true", help="Skip files that already exist at target path")
    ap.add_argument("--under", default="/srv/janus", help="Restrict restores to paths under this prefix")
    args = ap.parse_args()
    count = restore(dry_run=args.dry_run, only_missing=args.only_missing, under=args.under)
    print(f"Total candidates: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

