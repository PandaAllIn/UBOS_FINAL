from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Set

from trinity.config import load_configuration
from trinity.intelligence_tools import IntelligenceDatabase
from trinity.mission_queue_manager import MissionQueueManager

RULES: list[dict[str, Any]] = [
    {
        "name": "high_fit_grant_assembly",
        "trigger": {
            "category": "grants",
            "conditions": {"fit_score": ">=4.5", "deadline_days": "<=45", "status": "new"},
        },
        "action": {
            "spawn_mission": "grant_assembly",
            "assigned_to": "openai",
            "priority": 3,
            "payload": {"grant_id": "{intelligence.id}"},
        },
    },
    {
        "name": "warm_contact_outreach",
        "trigger": {
            "category": "contacts",
            "conditions": {"connection": "warm", "days_since_contact": ">14"},
        },
        "action": {
            "spawn_mission": "contact_followup",
            "assigned_to": "claude",
            "priority": 2,
        },
    },
    {
        "name": "revenue_lead_qualification",
        "trigger": {
            "category": "revenue",
            "conditions": {"stage": "lead", "probability": ">0.3"},
        },
        "action": {
            "spawn_mission": "lead_qualification",
            "assigned_to": "gemini",
            "priority": 2,
        },
    },
]

CACHE_DIR = Path("/srv/janus/03_OPERATIONS/vessels/balaur/intel_cache/intelligence")
STATE_FILE = CACHE_DIR / "action_generator_state.json"
LOG_PATH = Path("/srv/janus/logs/intelligence_actions.jsonl")


def _utc_now() -> datetime:
    return datetime.now(UTC)


class IntelligenceActionGenerator:
    """Evaluates intelligence rules to spawn follow-on missions."""

    def __init__(
        self,
        *,
        db_path: Path | None = None,
        queue_manager: MissionQueueManager | None = None,
        state_file: Path | None = None,
        log_path: Path | None = None,
    ) -> None:
        paths, _ = load_configuration()
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            pass
        self.db = IntelligenceDatabase(db_path=db_path)
        self.mission_queue = queue_manager or MissionQueueManager()
        self.state_path = Path(state_file or STATE_FILE).resolve()
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            pass
        self.log_path = Path(log_path or LOG_PATH).resolve()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.processed = self._load_state()

    def run(self, *, dry_run: bool = False) -> list[dict[str, Any]]:
        generated: list[dict[str, Any]] = []
        for rule in RULES:
            category = rule["trigger"]["category"]
            filters = self._filterable_conditions(category, rule["trigger"]["conditions"])
            candidates = self.db.query(category, filters, None, limit=100, sort_by="recency")
            for record in candidates:
                if not self._matches(rule["trigger"]["conditions"], category, record):
                    continue
                processed = self.processed.setdefault(rule["name"], set())
                if record["id"] in processed:
                    continue
                mission_payload = self._build_mission(rule, record)
                generated.append({"rule": rule["name"], "mission": mission_payload})
                if not dry_run:
                    self.mission_queue.queue_mission(mission_payload)
                    processed.add(record["id"])
                    self._log_action(rule["name"], record["id"], mission_payload)
        if not dry_run and generated:
            self._write_state()
        return generated

    def _matches(self, conditions: dict[str, Any], category: str, record: dict[str, Any]) -> bool:
        for key, condition in conditions.items():
            if category == "grants" and key == "deadline_days":
                if not _compare_deadline(record.get("deadline"), condition):
                    return False
                continue
            if category == "contacts" and key == "days_since_contact":
                if not _compare_days_since_contact(record.get("last_contact"), condition):
                    return False
                continue
            field = self._map_field(category, key)
            if field not in record:
                return False
            value = record.get(field)
            if not _compare_generic(value, condition):
                return False
        return True

    def _map_field(self, category: str, key: str) -> str:
        if category == "grants":
            mapping = {"fit_score": "fit_score", "status": "status"}
        elif category == "contacts":
            mapping = {"connection": "connection_strength"}
        elif category == "revenue":
            mapping = {"stage": "stage", "probability": "probability", "channel": "channel"}
        else:
            mapping = {}
        return mapping.get(key, key)

    def _filterable_conditions(self, category: str, conditions: dict[str, Any]) -> dict[str, Any]:
        ignored_keys = {"deadline_days", "days_since_contact"}
        return {self._map_field(category, key): value for key, value in conditions.items() if key not in ignored_keys}

    def _build_mission(self, rule: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
        action = rule["action"]
        payload_template = action.get("payload", {})
        payload = {key: value.format(intelligence=SimpleNamespace(**record)) if isinstance(value, str) else value for key, value in payload_template.items()}

        tags = [rule["name"], record["id"], action["spawn_mission"]]
        mission = {
            "assigned_to": action["assigned_to"],
            "priority": action.get("priority", 2),
            "objective": f"Auto-generated mission '{action['spawn_mission']}' for intelligence {record['id']}.",
            "deliverable": {
                "type": "comms_hub_message",
                "recipient": "captain",
                "message_type": action["spawn_mission"],
            },
            "metadata": {
                "generated_by": "intelligence_action_generator",
                "rule": rule["name"],
                "related_intel_ids": [record["id"]],
                "tags": tags,
            },
            "payload": payload,
            "queued_via": "intelligence_action_generator",
        }
        return mission

    def _load_state(self) -> dict[str, Set[str]]:
        if not self.state_path.exists():
            return {}
        try:
            raw = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return {rule: set(ids) for rule, ids in raw.items()}

    def _write_state(self) -> None:
        serialisable = {rule: sorted(ids) for rule, ids in self.processed.items()}
        tmp = self.state_path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(serialisable, handle, indent=2, sort_keys=True)
        tmp.replace(self.state_path)

    def _log_action(self, rule_name: str, intelligence_id: str, mission: dict[str, Any]) -> None:
        record = {
            "timestamp": _utc_now().isoformat(),
            "rule": rule_name,
            "intelligence_id": intelligence_id,
            "mission": mission,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")


def _compare_deadline(deadline: Any, condition: str) -> bool:
    if not deadline:
        return False
    try:
        deadline_dt = datetime.fromisoformat(str(deadline).replace("Z", "+00:00"))
    except ValueError:
        return False
    op, value = _parse_operator(condition)
    threshold = float(value)
    delta = (deadline_dt - _utc_now()).total_seconds() / 86400
    return _compare_numbers(delta, op, threshold)


def _compare_days_since_contact(last_contact: Any, condition: str) -> bool:
    if not last_contact:
        return False
    try:
        contact_dt = datetime.fromisoformat(str(last_contact).replace("Z", "+00:00"))
    except ValueError:
        return False
    op, value = _parse_operator(condition)
    threshold = float(value)
    days = (_utc_now() - contact_dt).total_seconds() / 86400
    return _compare_numbers(days, op, threshold)


def _compare_generic(value: Any, condition: Any) -> bool:
    op, operand = _parse_operator(condition)
    if isinstance(value, (int, float)) or _looks_numeric(value):
        try:
            left = float(value)
            right = float(operand)
        except (TypeError, ValueError):
            return False
        return _compare_numbers(left, op, right)
    if op == "=":
        return str(value).lower() == str(operand).lower()
    if op == "!=":
        return str(value).lower() != str(operand).lower()
    return False


def _compare_numbers(lhs: float, operator: str, rhs: float) -> bool:
    if operator == ">":
        return lhs > rhs
    if operator == "<":
        return lhs < rhs
    if operator == ">=":
        return lhs >= rhs
    if operator == "<=":
        return lhs <= rhs
    if operator == "!=":
        return lhs != rhs
    return lhs == rhs


def _parse_operator(condition: Any) -> tuple[str, Any]:
    if isinstance(condition, str):
        condition = condition.strip()
        for op in (">=", "<=", "!=", ">", "<"):
            if condition.startswith(op):
                return op, condition[len(op) :].strip()
    return "=", condition


def _looks_numeric(value: Any) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


class SimpleNamespace:
    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate missions based on intelligence rules.")
    parser.add_argument("--dry-run", action="store_true", help="Print proposed missions without queuing.")
    parser.add_argument("--db", type=Path, help="Override intelligence database path (testing).")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    generator = IntelligenceActionGenerator(db_path=args.db)
    missions = generator.run(dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(missions, indent=2))


if __name__ == "__main__":
    main()
