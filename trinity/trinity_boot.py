#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

def main() -> int:
    # Ensure PYTHONPATH includes Trinity path
    trinity_dir = Path(__file__).parent
    os.environ.setdefault("PYTHONPATH", f"{trinity_dir.parent}:{trinity_dir}")

    # Load configuration to validate env
    try:
        from config import load_configuration
        paths, keys = load_configuration()
        # Create basic runtime directories
        paths.memory_dir.mkdir(parents=True, exist_ok=True)
        paths.log_dir.mkdir(parents=True, exist_ok=True)
        (paths.log_dir / "events.jsonl").touch(exist_ok=True)
        # Quick sanity imports for residents/oracle bridge
        import oracle_bridge  # noqa: F401
    except Exception as e:
        # Non-zero exit triggers systemd failure as intended
        print(f"Trinity boot failed: {e}")
        return 2

    print("Trinity residents boot: configuration loaded; paths prepared.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

