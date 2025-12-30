from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from config import load_configuration
from mission_queue_manager import MissionQueueManager, isoformat_now


class SchedulerError(Exception):
    pass


def load_template(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schedule(template: dict[str, Any]) -> None:
    schedule = template.get("schedule")
    if not isinstance(schedule, dict):
        raise SchedulerError("Template missing schedule metadata")
    required_keys = {"type", "frequency", "time_utc"}
    missing = required_keys.difference(schedule)
    if missing:
        raise SchedulerError(f"Template schedule missing fields: {', '.join(sorted(missing))}")


def queue_template(manager: MissionQueueManager, template_path: Path, *, source: str) -> dict[str, Any]:
    template = load_template(template_path)
    validate_schedule(template)
    template["source_template"] = source
    template.pop("mission_id", None)
    template["created_at"] = isoformat_now()
    template["scheduled_run"] = isoformat_now()
    destination = manager.queue_mission(template)
    return manager.load_mission(destination)


def log_event(log_path: Path, event: str, payload: dict[str, Any]) -> None:
    record = {
        "timestamp": isoformat_now(),
        "event": event,
        **payload,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        json.dump(record, handle)
        handle.write("\n")


def resolve_templates(root: Path, selection: Iterable[str] | None) -> list[tuple[str, Path]]:
    if selection:
        resolved = []
        for name in selection:
            path = root / f"{name}.json"
            if not path.exists():
                raise SchedulerError(f"Template not found: {path}")
            resolved.append((name, path))
        return resolved
    return sorted((path.stem, path) for path in root.glob("*.json"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mission scheduler entrypoint")
    parser.add_argument(
        "--template",
        action="append",
        dest="templates",
        help="Template name to queue (can be provided multiple times)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List scheduled missions without queuing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    paths, _ = load_configuration()
    templates_root = Path(paths.base_dir) / "mission_templates"
    log_path = paths.log_dir / "scheduler.jsonl"
    manager = MissionQueueManager()

    try:
        templates = resolve_templates(templates_root, args.templates)
    except SchedulerError as exc:
        parser.error(str(exc))
        return 2

    if args.dry_run:
        for template_name, _ in templates:
            print(f"Would queue template: {template_name}")
        return 0

    exit_code = 0
    for template_name, template_path in templates:
        try:
            mission = queue_template(manager, template_path, source=template_name)
            log_event(
                log_path,
                "mission_queued",
                {
                    "template": template_name,
                    "mission_id": mission.get("mission_id"),
                    "priority": mission.get("priority"),
                },
            )
            print(f"Queued mission {mission.get('mission_id')} from template {template_name}")
        except (SchedulerError, json.JSONDecodeError) as exc:
            log_event(
                log_path,
                "error",
                {
                    "template": template_name,
                    "message": str(exc),
                },
            )
            print(f"Failed to queue template {template_name}: {exc}", file=sys.stderr)
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
