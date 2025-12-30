from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable, List, MutableMapping, Sequence

# Ensure repository root is importable when scripts are executed directly.
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from trinity.pucklib.comms import TalkingDrumTransmitter  # noqa: E402

LOGGER = logging.getLogger(__name__)


def utc_now() -> datetime:
    """Return the current UTC timestamp with timezone information."""
    return datetime.now(tz=timezone.utc)


@dataclass(frozen=True)
class SkillPaths:
    """Canonical paths used by the EU Grant Hunter skill."""

    repo_root: Path
    skill_root: Path
    pipeline_dir: Path
    pipeline_state: Path
    grant_opportunities_dir: Path
    deadline_calendar: Path
    log_file: Path
    comms_root: Path
    assets_dir: Path


@dataclass
class Opportunity:
    """In-memory representation of an EU funding opportunity."""

    opportunity_id: str
    title: str
    program: str
    budget_min: int | None
    budget_max: int | None
    deadline: datetime | None
    description: str
    url: str
    criteria: list[str]
    discovered_date: date
    last_seen: date
    fit_score: float | None = None
    fit_explanation: list[str] = field(default_factory=list)
    ubos_project_match: str | None = None
    matched_keywords: list[str] = field(default_factory=list)
    status: str = "new"
    reminders_sent: list[int] = field(default_factory=list)
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the opportunity to a JSON-safe dictionary."""
        return {
            "opportunity_id": self.opportunity_id,
            "title": self.title,
            "program": self.program,
            "budget_min": self.budget_min,
            "budget_max": self.budget_max,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "description": self.description,
            "url": self.url,
            "criteria": list(self.criteria),
            "discovered_date": self.discovered_date.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "fit_score": self.fit_score,
            "fit_explanation": list(self.fit_explanation),
            "ubos_project_match": self.ubos_project_match,
            "matched_keywords": list(self.matched_keywords),
            "status": self.status,
            "reminders_sent": list(self.reminders_sent),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: MutableMapping[str, Any]) -> "Opportunity":
        """Rehydrate an Opportunity from JSON."""
        deadline_raw = payload.get("deadline")
        deadline: datetime | None = None
        if deadline_raw:
            try:
                deadline = datetime.fromisoformat(deadline_raw)
            except ValueError:
                LOGGER.warning("Invalid deadline ISO format: %s", deadline_raw)
                deadline = None

        discovered_raw = payload.get("discovered_date")
        last_seen_raw = payload.get("last_seen")
        discovered_date = _parse_date(discovered_raw) if discovered_raw else date.today()
        last_seen = _parse_date(last_seen_raw) if last_seen_raw else date.today()

        return cls(
            opportunity_id=str(payload.get("opportunity_id")),
            title=str(payload.get("title")),
            program=str(payload.get("program")),
            budget_min=_coerce_int(payload.get("budget_min")),
            budget_max=_coerce_int(payload.get("budget_max")),
            deadline=deadline,
            description=str(payload.get("description") or ""),
            url=str(payload.get("url") or ""),
            criteria=list(payload.get("criteria") or []),
            discovered_date=discovered_date,
            last_seen=last_seen,
            fit_score=_coerce_float(payload.get("fit_score")),
            fit_explanation=list(payload.get("fit_explanation") or []),
            ubos_project_match=payload.get("ubos_project_match"),
            matched_keywords=list(payload.get("matched_keywords") or []),
            status=str(payload.get("status") or "new"),
            reminders_sent=[int(value) for value in payload.get("reminders_sent", [])],
            notes=payload.get("notes"),
        )

    def update_from(self, other: "Opportunity") -> None:
        """Merge data from a fresh scan into the existing record."""
        self.title = other.title or self.title
        self.program = other.program or self.program
        self.budget_min = other.budget_min or self.budget_min
        self.budget_max = other.budget_max or self.budget_max
        self.deadline = other.deadline or self.deadline
        self.description = other.description or self.description
        self.url = other.url or self.url
        if other.criteria:
            self.criteria = list(sorted(set(self.criteria) | set(other.criteria)))
        self.last_seen = other.last_seen
        if other.discovered_date < self.discovered_date:
            self.discovered_date = other.discovered_date
        if other.fit_score is not None:
            self.fit_score = other.fit_score
            self.fit_explanation = other.fit_explanation
            self.ubos_project_match = other.ubos_project_match
            self.matched_keywords = other.matched_keywords
        if other.notes:
            self.notes = other.notes
        # Preserve reminders already sent.
        if other.reminders_sent:
            merged = set(self.reminders_sent)
            merged.update(other.reminders_sent)
            self.reminders_sent = sorted(merged)
        if other.status and other.status != "new":
            self.status = other.status

    def days_until_deadline(self, reference: datetime | None = None) -> int | None:
        if not self.deadline:
            return None
        reference = reference or utc_now()
        delta = self.deadline - reference
        return delta.days


def resolve_paths() -> SkillPaths:
    skill_root = Path(__file__).resolve().parents[1]
    repo_root = Path(__file__).resolve().parents[4]
    pipeline_dir = repo_root / "01_STRATEGY" / "grant_pipeline"
    return SkillPaths(
        repo_root=repo_root,
        skill_root=skill_root,
        pipeline_dir=pipeline_dir,
        pipeline_state=pipeline_dir / "pipeline_state.json",
        grant_opportunities_dir=repo_root / "01_STRATEGY" / "grant_opportunities",
        deadline_calendar=pipeline_dir / "deadline_calendar.md",
        log_file=repo_root / "logs" / "grant_hunter.jsonl",
        comms_root=repo_root / "03_OPERATIONS" / "COMMS_HUB",
        assets_dir=skill_root / "assets",
    )


PATHS = resolve_paths()


def ensure_directories(paths: SkillPaths = PATHS) -> None:
    paths.pipeline_dir.mkdir(parents=True, exist_ok=True)
    paths.grant_opportunities_dir.mkdir(parents=True, exist_ok=True)
    paths.log_file.parent.mkdir(parents=True, exist_ok=True)
    (paths.comms_root / "logs").mkdir(parents=True, exist_ok=True)


def load_pipeline_state(paths: SkillPaths = PATHS) -> dict[str, Any]:
    if not paths.pipeline_state.exists():
        return {
            "metadata": {"generated_at": None, "source": "bootstrap"},
            "opportunities": [],
        }

    with paths.pipeline_state.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    opportunities = [Opportunity.from_dict(raw) for raw in payload.get("opportunities", [])]
    payload["opportunities"] = opportunities
    return payload


def save_pipeline_state(
    opportunities: Iterable[Opportunity],
    *,
    metadata: dict[str, Any] | None = None,
    paths: SkillPaths = PATHS,
) -> dict[str, Any]:
    ensure_directories(paths)
    metadata = metadata or {}
    metadata.setdefault("generated_at", utc_now().isoformat())
    metadata.setdefault("source", "scan")

    serialized = [opportunity.to_dict() for opportunity in opportunities]
    payload = {"metadata": metadata, "opportunities": serialized}

    with paths.pipeline_state.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)

    return payload


def merge_opportunity_sets(
    existing: Iterable[Opportunity],
    fresh: Iterable[Opportunity],
) -> list[Opportunity]:
    merged: dict[str, Opportunity] = {op.opportunity_id: op for op in existing}

    for item in fresh:
        current = merged.get(item.opportunity_id)
        if current is None:
            merged[item.opportunity_id] = item
        else:
            current.update_from(item)

    return sorted(
        merged.values(),
        key=lambda op: (
            op.deadline or datetime.max.replace(tzinfo=timezone.utc),
            op.title.lower(),
        ),
    )


def append_log(event: str, payload: dict[str, Any], *, paths: SkillPaths = PATHS) -> None:
    ensure_directories(paths)
    record = {
        "timestamp": utc_now().isoformat(),
        "event": event,
        "payload": payload,
    }
    try:
        with paths.log_file.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")
    except OSError as exc:  # pragma: no cover - filesystem permissions
        LOGGER.warning("Unable to write grant hunter log: %s", exc)


def transmit_puck(
    puck: dict[str, Any],
    *,
    recipients: Sequence[str],
    rhythm: str = "standard",
    tone: str | None = None,
    agent_name: str = "codex",
    paths: SkillPaths = PATHS,
) -> list[Path]:
    ensure_directories(paths)
    transmitter = TalkingDrumTransmitter(agent_name, comms_root=paths.comms_root)
    written: list[Path] = []
    for recipient in recipients:
        try:
            written.extend(
                transmitter.transmit(
                    puck,
                    recipient=recipient,
                    rhythm=rhythm,
                    tone=tone,
                )
            )
        except Exception as exc:  # pragma: no cover - guard for filesystem errors
            LOGGER.error("Failed to transmit puck to %s: %s", recipient, exc)
    return written


def slugify(value: str) -> str:
    normalized = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    return "-".join(filter(None, normalized.split("-")))


def format_euro(amount: int | None) -> str:
    if amount is None:
        return "unknown"
    return f"{amount:,.0f}".replace(",", "\u202f")


def _coerce_int(value: Any) -> int | None:
    if value in (None, "", "null"):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        LOGGER.debug("Unable to coerce %r to int", value)
        return None


def _coerce_float(value: Any) -> float | None:
    if value in (None, "", "null"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        LOGGER.debug("Unable to coerce %r to float", value)
        return None


def _parse_date(raw: str) -> date:
    try:
        return date.fromisoformat(raw)
    except ValueError:
        LOGGER.warning("Invalid date format: %s", raw)
        return utc_now().date()


def resolve_template(name: str, *, paths: SkillPaths = PATHS) -> Path:
    template_path = paths.assets_dir / name
    if not template_path.exists():
        raise FileNotFoundError(f"Template '{name}' not found at {template_path}")
    return template_path


def render_template(template_path: Path, replacements: MutableMapping[str, str]) -> str:
    content = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def normalise_criteria(values: Sequence[str] | None) -> list[str]:
    if not values:
        return []
    unique: List[str] = []
    for entry in values:
        entry = entry.strip()
        if entry and entry.lower() not in {item.lower() for item in unique}:
            unique.append(entry)
    return unique
