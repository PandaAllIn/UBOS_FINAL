from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, MutableMapping

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class SkillPaths:
    repo_root: Path
    skill_root: Path
    assemblies_root: Path
    state_path: Path
    log_path: Path
    assets_dir: Path
    references_dir: Path
    comms_root: Path


def resolve_paths() -> SkillPaths:
    skill_root = Path(__file__).resolve().parents[1]
    repo_root = Path(__file__).resolve().parents[4]
    assemblies_root = repo_root / "03_OPERATIONS" / "grant_assembly"
    return SkillPaths(
        repo_root=repo_root,
        skill_root=skill_root,
        assemblies_root=assemblies_root,
        state_path=assemblies_root / "state.json",
        log_path=repo_root / "logs" / "grant_assembly.jsonl",
        assets_dir=skill_root / "assets",
        references_dir=skill_root / "references",
        comms_root=repo_root / "03_OPERATIONS" / "COMMS_HUB",
    )


PATHS = resolve_paths()


def ensure_directories(paths: SkillPaths = PATHS) -> None:
    paths.assemblies_root.mkdir(parents=True, exist_ok=True)
    paths.log_path.parent.mkdir(parents=True, exist_ok=True)
    (paths.comms_root / "logs").mkdir(parents=True, exist_ok=True)


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def load_state(paths: SkillPaths = PATHS) -> dict[str, Any]:
    ensure_directories(paths)
    if not paths.state_path.exists():
        default = {"assemblies": []}
        save_state(default, paths=paths)
        return default
    try:
        with paths.state_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        LOGGER.warning("Unable to load grant assembly state (%s); regenerating", exc)
        default = {"assemblies": []}
        save_state(default, paths=paths)
        return default


def save_state(state: Mapping[str, Any], *, paths: SkillPaths = PATHS) -> None:
    ensure_directories(paths)
    try:
        with paths.state_path.open("w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
    except OSError as exc:
        LOGGER.warning("Unable to persist grant assembly state: %s", exc)


def append_log(event: str, payload: Mapping[str, Any], *, paths: SkillPaths = PATHS) -> None:
    ensure_directories(paths)
    record = {
        "timestamp": utc_now().isoformat(),
        "event": event,
        "payload": payload,
    }
    try:
        with paths.log_path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")
    except OSError as exc:
        LOGGER.warning("Unable to write grant assembly log: %s", exc)


def slugify(value: str) -> str:
    filtered = ("".join(ch.lower() if ch.isalnum() else "-" for ch in value)).strip("-")
    return "-".join(filter(None, filtered.split("-")))


def load_pipeline(paths: SkillPaths = PATHS) -> dict[str, Any]:
    pipeline_path = paths.repo_root / "01_STRATEGY" / "grant_pipeline" / "pipeline_state.json"
    if not pipeline_path.exists():
        return {"opportunities": []}
    try:
        with pipeline_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        LOGGER.warning("Unable to parse pipeline_state.json: %s", exc)
        return {"opportunities": []}


def get_opportunity(opportunity_id: str, *, paths: SkillPaths = PATHS) -> dict[str, Any] | None:
    pipeline = load_pipeline(paths)
    for entry in pipeline.get("opportunities", []):
        if entry.get("opportunity_id") == opportunity_id:
            return entry
    return None


def find_assembly(state: Mapping[str, Any], assembly_id: str) -> dict[str, Any] | None:
    for entry in state.get("assemblies", []):
        if entry.get("id") == assembly_id:
            return entry
    return None


def register_assembly(state: MutableMapping[str, Any], assembly: Mapping[str, Any]) -> None:
    assemblies: list[dict[str, Any]] = state.setdefault("assemblies", [])  # type: ignore[assignment]
    assemblies = [item for item in assemblies if item.get("id") != assembly.get("id")]
    assemblies.append(dict(assembly))
    state["assemblies"] = assemblies


def assembly_path(assembly_id: str, *, paths: SkillPaths = PATHS) -> Path:
    path = paths.assemblies_root / assembly_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return default


def compute_progress(phases: Mapping[str, Mapping[str, Any]]) -> float:
    checkpoints: Iterable[str] = (
        "intelligence",
        "narratives",
        "budget",
        "partners",
        "compliance",
        "packaging",
    )
    total = len(tuple(checkpoints))
    if total == 0:
        return 0.0
    completed = sum(1 for key in checkpoints if phases.get(key, {}).get("status") == "complete")
    return round((completed / total) * 100, 1)
