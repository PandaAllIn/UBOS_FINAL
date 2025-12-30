from __future__ import annotations

import json
import logging
import random
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class SkillPaths:
    repo_root: Path
    skill_root: Path
    data_root: Path
    reports_dir: Path
    dashboards_dir: Path
    log_path: Path


def resolve_paths() -> SkillPaths:
    skill_root = Path(__file__).resolve().parents[1]
    repo_root = Path(__file__).resolve().parents[4]
    data_root = repo_root / "03_OPERATIONS" / "eufm_monetization"
    return SkillPaths(
        repo_root=repo_root,
        skill_root=skill_root,
        data_root=data_root,
        reports_dir=data_root / "reports",
        dashboards_dir=data_root / "dashboards",
        log_path=repo_root / "logs" / "eufm_monetization.jsonl",
    )


PATHS = resolve_paths()


def ensure_directories(paths: SkillPaths = PATHS) -> None:
    paths.data_root.mkdir(parents=True, exist_ok=True)
    paths.reports_dir.mkdir(parents=True, exist_ok=True)
    paths.dashboards_dir.mkdir(parents=True, exist_ok=True)
    paths.log_path.parent.mkdir(parents=True, exist_ok=True)


def log_event(event: str, payload: Mapping[str, Any], *, paths: SkillPaths = PATHS) -> None:
    ensure_directories(paths)
    record = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "event": event,
        "payload": payload,
    }
    try:
        with paths.log_path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")
    except OSError as exc:
        LOGGER.warning("Unable to write monetization log: %s", exc)


def save_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def random_seed(seed: int | None = None) -> random.Random:
    rng = random.Random(seed)
    return rng
