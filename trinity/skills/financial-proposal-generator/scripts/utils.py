from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class SkillPaths:
    repo_root: Path
    skill_root: Path
    assemblies_root: Path
    validation_log: Path


def resolve_paths() -> SkillPaths:
    skill_root = Path(__file__).resolve().parents[1]
    repo_root = Path(__file__).resolve().parents[4]
    assemblies_root = repo_root / "03_OPERATIONS" / "grant_assembly"
    return SkillPaths(
        repo_root=repo_root,
        skill_root=skill_root,
        assemblies_root=assemblies_root,
        validation_log=repo_root / "logs" / "grant_narrative_validation.jsonl",
    )


PATHS = resolve_paths()


def ensure_directories(paths: SkillPaths = PATHS) -> None:
    paths.assemblies_root.mkdir(parents=True, exist_ok=True)
    paths.validation_log.parent.mkdir(parents=True, exist_ok=True)


def log_jsonl(path: Path, payload: dict[str, Any]) -> None:
    ensure_directories()
    record = {"timestamp": datetime.now(tz=timezone.utc).isoformat(), **payload}
    try:
        with path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")
    except OSError as exc:
        LOGGER.warning("Unable to append log %s: %s", path, exc)


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in text.split() if token]


def extract_numbers(text: str) -> list[str]:
    tokens: list[str] = []
    current: list[str] = []
    for ch in text:
        if ch.isdigit() or ch in {",", "."}:
            current.append(ch)
        else:
            if current:
                tokens.append("".join(current).strip(","))
                current = []
    if current:
        tokens.append("".join(current).strip(","))
    return [token for token in tokens if token]
