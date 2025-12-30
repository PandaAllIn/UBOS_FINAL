#!/usr/bin/env python3
"""Broadcast Announcement Helper for COMMS_HUB.

Usage:
  broadcast_announcement.py --message "Text..." [--category news|query|report|status|emergency] [--from captain]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone


def send(from_vessel: str, message: str, category: str) -> None:
    payload = {
        "message": message,
        "sender": from_vessel,
        "category": category,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    cmd = [
        "/usr/bin/env",
        "python3",
        "/srv/janus/02_FORGE/scripts/comms_hub_send.py",
        "--from",
        from_vessel,
        "--to",
        "broadcast",
        "--type",
        "broadcast",
        "--payload",
        json.dumps(payload),
    ]
    subprocess.run(cmd, check=False)


def main() -> int:
    ap = argparse.ArgumentParser(description="Broadcast a COMMS_HUB announcement")
    ap.add_argument("--message", required=True, help="Message text")
    ap.add_argument("--category", default="news", choices=["news", "query", "report", "status", "emergency"]) 
    ap.add_argument("--from", dest="from_vessel", default="captain", help="Sender vessel name")
    args = ap.parse_args()
    send(args.from_vessel, args.message, args.category)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

