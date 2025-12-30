from __future__ import annotations

import json
import logging
import math
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from trinity.pucklib.comms import TalkingDrumTransmitter  # type: ignore  # noqa: E402

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class SkillPaths:
    repo_root: Path
    skill_root: Path
    ops_dir: Path
    briefings_dir: Path
    dashboard_path: Path
    state_path: Path
    revenue_log: Path
    spending_log: Path
    general_log: Path
    emergency_log: Path
    comms_root: Path
    assets_dir: Path


DEFAULT_STATE: dict[str, Any] = {
    "timeline": {
        "start_date": "2025-11-10",
        "days_elapsed": 0,
        "last_report_date": None,
    },
    "capital": {
        "total": 1500.0,
        "remaining": 1500.0,
        "additional_inflows": 0.0,
    },
    "metrics": {
        "burn_rate": 35.0,
        "runway_days": 43.0,
    },
    "cascade": {
        "research": {"allocation": 300.0, "spent": 0.0},
        "emergency": {"allocation": 150.0, "spent": 0.0},
        "operations": {"allocation": 225.0, "spent": 0.0},
        "projects": {"allocation": 600.0, "spent": 0.0},
        "strategic": {"allocation": 225.0, "spent": 0.0},
    },
    "spending_log": [],
    "revenue": {
        "streams": {
            "agent-as-a-service": 0.0,
            "intel-services": 0.0,
            "proposal-consultation": 0.0,
        },
        "history": [],
    },
    "health": {
        "last_score": None,
        "last_breakdown": {},
        "last_updated": None,
    },
}


def resolve_paths() -> SkillPaths:
    skill_root = Path(__file__).resolve().parents[1]
    repo_root = Path(__file__).resolve().parents[4]
    ops_dir = repo_root / "03_OPERATIONS" / "malaga_embassy"
    return SkillPaths(
        repo_root=repo_root,
        skill_root=skill_root,
        ops_dir=ops_dir,
        briefings_dir=ops_dir / "briefings",
        dashboard_path=ops_dir / "dashboard.html",
        state_path=ops_dir / "state.json",
        revenue_log=ops_dir / "revenue_log.jsonl",
        spending_log=ops_dir / "spending_log.jsonl",
        general_log=repo_root / "logs" / "malaga_embassy.jsonl",
        emergency_log=repo_root / "logs" / "malaga_emergency.jsonl",
        comms_root=repo_root / "03_OPERATIONS" / "COMMS_HUB",
        assets_dir=skill_root / "assets",
    )


PATHS = resolve_paths()


def ensure_directories(paths: SkillPaths = PATHS) -> None:
    paths.ops_dir.mkdir(parents=True, exist_ok=True)
    paths.briefings_dir.mkdir(parents=True, exist_ok=True)
    paths.general_log.parent.mkdir(parents=True, exist_ok=True)
    paths.emergency_log.parent.mkdir(parents=True, exist_ok=True)
    (paths.comms_root / "logs").mkdir(parents=True, exist_ok=True)


def load_state(paths: SkillPaths = PATHS) -> dict[str, Any]:
    ensure_directories(paths)
    if not paths.state_path.exists():
        save_state(DEFAULT_STATE.copy(), paths=paths)
        return json.loads(json.dumps(DEFAULT_STATE))
    try:
        payload = json.loads(paths.state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        LOGGER.warning("State file corrupt; regenerating defaults")
        payload = json.loads(json.dumps(DEFAULT_STATE))
    return payload


def save_state(state: Mapping[str, Any], *, paths: SkillPaths = PATHS) -> None:
    ensure_directories(paths)
    with paths.state_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)


def append_jsonl(path: Path, record: Mapping[str, Any]) -> None:
    ensure_directories(PATHS)
    try:
        with path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")
    except OSError as exc:  # pragma: no cover - permission guard
        LOGGER.warning("Unable to write JSONL log at %s: %s", path, exc)


def transmit_puck(payload: Mapping[str, Any], *, recipients: Sequence[str], rhythm: str = "standard", tone: str | None = None) -> None:
    ensure_directories(PATHS)
    transmitter = TalkingDrumTransmitter("codex", comms_root=PATHS.comms_root)
    for recipient in recipients:
        try:
            transmitter.transmit(payload, recipient=recipient, rhythm=rhythm, tone=tone)
        except Exception as exc:  # pragma: no cover - filesystem/permission guard
            LOGGER.error("Failed to transmit puck to %s: %s", recipient, exc)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _today() -> date:
    return datetime.now(tz=timezone.utc).date()


def _day_index(state: MutableMapping[str, Any], *, reference: date | None = None) -> int:
    reference = reference or _today()
    timeline = state.setdefault("timeline", {})
    start = _parse_date(timeline.get("start_date")) or date(2025, 11, 10)
    days = max(0, (reference - start).days)
    timeline["days_elapsed"] = days
    timeline["last_report_date"] = reference.isoformat()
    return days


def _summarise_revenue(state: Mapping[str, Any], *, reference: date | None = None) -> dict[str, Any]:
    reference = reference or _today()
    history: Sequence[Mapping[str, Any]] = state.get("revenue", {}).get("history", [])  # type: ignore[assignment]
    today_total = 0.0
    week_total = 0.0
    month_total = 0.0
    streams = {"agent-as-a-service": 0.0, "intel-services": 0.0, "proposal-consultation": 0.0}
    week_start = reference - timedelta(days=6)
    for entry in history:
        event_date = _parse_date(str(entry.get("date")))
        if event_date is None:
            continue
        amount = float(entry.get("amount", 0.0))
        stream = str(entry.get("stream", "")).lower()
        if stream in streams:
            streams[stream] += amount
        if event_date == reference:
            today_total += amount
        if week_start <= event_date <= reference:
            week_total += amount
        if event_date.year == reference.year and event_date.month == reference.month:
            month_total += amount
    return {
        "today": round(today_total, 2),
        "week": round(week_total, 2),
        "month": round(month_total, 2),
        "streams": {key: round(value, 2) for key, value in streams.items()},
    }


def _total_spent(state: Mapping[str, Any]) -> float:
    return sum(float(cat.get("spent", 0.0)) for cat in state.get("cascade", {}).values())


def _update_runway(state: MutableMapping[str, Any]) -> None:
    total_spent = _total_spent(state)
    capital = state.setdefault("capital", {})
    revenue_summary = _summarise_revenue(state)
    capital_total = float(capital.get("total", 1500.0)) + float(capital.get("additional_inflows", 0.0))
    capital_remaining = capital_total - total_spent + revenue_summary["month"]
    capital["remaining"] = round(capital_remaining, 2)
    days_elapsed = max(1, int(state.get("timeline", {}).get("days_elapsed", 1)))
    burn_rate = total_spent / days_elapsed
    state.setdefault("metrics", {})["burn_rate"] = round(burn_rate, 2)
    runway = capital_remaining / burn_rate if burn_rate > 0 else 999.0
    state["metrics"]["runway_days"] = round(runway, 1)


def _budget_score(state: Mapping[str, Any]) -> tuple[float, list[str]]:
    penalties: list[str] = []
    score = 25.0
    for name, info in state.get("cascade", {}).items():
        allocation = float(info.get("allocation", 0.0))
        spent = float(info.get("spent", 0.0))
        if allocation <= 0:
            continue
        ratio = spent / allocation
        if ratio <= 1.0:
            continue
        overage = ratio - 1.0
        penalty = min(score, overage * 25.0)
        score -= penalty
        penalties.append(f"{name} over by {overage * 100:.1f}% (-{penalty:.1f})")
    return max(0.0, round(score, 1)), penalties


def _runway_score(runway: float) -> float:
    if runway >= 30:
        return 20.0
    if runway >= 14:
        return 15.0
    if runway >= 7:
        return 10.0
    if runway > 0:
        return 5.0
    return 0.0


def _revenue_score(state: Mapping[str, Any], *, reference: date) -> tuple[float, str]:
    summary = _summarise_revenue(state, reference=reference)
    month_total = summary["month"]
    day_ratio = min(1.0, max(0.0, _day_index(dict(state), reference=reference) / 30.0))
    expected_min = 855.0 * day_ratio
    expected_max = 1910.0 * day_ratio if day_ratio > 0 else 0.0
    if expected_min <= 0.0:
        score = 15.0 if month_total > 0 else 10.0
    elif month_total >= expected_min:
        score = 25.0
    else:
        ratio = month_total / expected_min if expected_min else 0.0
        score = max(5.0, 25.0 * ratio)
    descriptor = f"€{month_total:.2f} vs target ≥€{expected_min:.2f}"
    if expected_max and month_total > expected_max:
        descriptor += " (ahead of schedule)"
    return round(min(25.0, score), 1), descriptor


def _compliance_score(state: Mapping[str, Any]) -> tuple[float, list[str]]:
    score = 30.0
    notes: list[str] = []
    cascade = state.get("cascade", {})
    runway = float(state.get("metrics", {}).get("runway_days", 0.0))
    emergency_spent = float(cascade.get("emergency", {}).get("spent", 0.0))
    strategic_spent = float(cascade.get("strategic", {}).get("spent", 0.0))
    if strategic_spent > 0:
        score -= 15.0
        notes.append("Strategic reserve tapped (-15)")
    if emergency_spent > 0 and runway >= 14:
        score -= 10.0
        notes.append("Emergency reserve used outside crisis (-10)")
    if runway < 14 and emergency_spent == 0:
        notes.append("Emergency reserve available; consider activation")
    return max(0.0, round(score, 1)), notes


def compute_health(state: MutableMapping[str, Any], *, reference: date | None = None) -> dict[str, Any]:
    reference = reference or _today()
    days_elapsed = _day_index(state, reference=reference)
    _update_runway(state)
    budget_points, budget_notes = _budget_score(state)
    runway_points = _runway_score(state.get("metrics", {}).get("runway_days", 0.0))
    revenue_points, revenue_note = _revenue_score(state, reference=reference)
    compliance_points, compliance_notes = _compliance_score(state)

    total = round(budget_points + runway_points + revenue_points + compliance_points, 1)
    recommendations: list[str] = []
    burn_rate = float(state.get("metrics", {}).get("burn_rate", 0.0))
    if burn_rate > 45:
        recommendations.append("Burn rate exceeds €45/day; freeze non-essential spending.")
    if revenue_points < 20:
        recommendations.append("Accelerate revenue outreach to meet minimum trajectory.")
    if total < 70:
        recommendations.append("Plan corrective actions to restore health ≥70.")
    recommendations.extend(budget_notes)
    recommendations.extend(compliance_notes)
    recommendations.append(revenue_note)

    summary = {
        "score": total,
        "components": {
            "budget": budget_points,
            "runway": runway_points,
            "revenue": revenue_points,
            "compliance": compliance_points,
        },
        "recommendations": recommendations,
        "burn_rate": burn_rate,
        "runway_days": float(state.get("metrics", {}).get("runway_days", 0.0)),
        "days_elapsed": days_elapsed,
    }
    state.setdefault("health", {})["last_score"] = total
    state["health"]["last_breakdown"] = summary["components"]
    state["health"]["last_updated"] = datetime.now(tz=timezone.utc).isoformat()
    return summary


def register_spending(state: MutableMapping[str, Any], *, amount: float, category: str, description: str, requester: str, event_date: date | None = None) -> None:
    event_date = event_date or _today()
    category = category.lower()
    cascade = state.setdefault("cascade", {})
    if category not in cascade:
        raise ValueError(f"Unknown cascade category '{category}'")
    cascade[category]["spent"] = float(cascade[category].get("spent", 0.0)) + amount
    entry = {
        "date": event_date.isoformat(),
        "amount": round(amount, 2),
        "category": category,
        "description": description,
        "requester": requester,
    }
    state.setdefault("spending_log", []).append(entry)
    capital = state.setdefault("capital", {})
    capital["remaining"] = float(capital.get("remaining", 0.0)) - amount


def register_revenue(state: MutableMapping[str, Any], *, amount: float, stream: str, client: str, event_date: date | None = None) -> dict[str, Any]:
    event_date = event_date or _today()
    stream = stream.lower()
    streams = state.setdefault("revenue", {}).setdefault("streams", {})
    streams.setdefault(stream, 0.0)
    streams[stream] += amount
    history = state.setdefault("revenue", {}).setdefault("history", [])
    entry = {
        "date": event_date.isoformat(),
        "amount": round(amount, 2),
        "stream": stream,
        "client": client,
    }
    history.append(entry)
    capital = state.setdefault("capital", {})
    capital["remaining"] = float(capital.get("remaining", 0.0)) + amount
    return entry


def log_event(event: str, payload: Mapping[str, Any]) -> None:
    record = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "event": event,
        "payload": payload,
    }
    append_jsonl(PATHS.general_log, record)


def emoji_for_score(score: float) -> str:
    if score >= 90:
        return "🔥"
    if score >= 70:
        return "✅"
    if score >= 50:
        return "⚠️"
    if score >= 30:
        return "🚨"
    return "🆘"
