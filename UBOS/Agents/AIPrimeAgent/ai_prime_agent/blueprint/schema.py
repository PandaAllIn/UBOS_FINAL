"""
UBOS Blueprint: Strategic Blueprint Schema Utilities

Philosophy: Blueprint Thinking + Systems over Willpower
Strategic Purpose: Provide a validated, machine-readable source of truth that keeps the AI Prime Agent aligned with UBOS intent.
System Design: Dataclasses encode the blueprint structure; lightweight validators enforce required fields, ID patterns, and guardrail presence.
Feedback Loops: Validation surfaces schema drift early; loading helpers enable periodic Strategic Pauses to refresh blueprint data.
Environmental Support: Relies on YAML/JSON documents, Gemini 2.5 Pro consultations, and agent registries produced elsewhere in the system.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - yaml is optional but provided in repo
    yaml = None


class BlueprintValidationError(ValueError):
    """Raised when a Strategic Blueprint payload fails UBOS-aligned validation."""


def _require_dict(name: str, value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise BlueprintValidationError(f"{name} must be an object")
    return value


def _require_list(name: str, value: Any) -> List[Any]:
    if not isinstance(value, list):
        raise BlueprintValidationError(f"{name} must be a list")
    return value


def _require_str(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BlueprintValidationError(f"{name} must be a non-empty string")
    return value.strip()


def _require_int(name: str, value: Any) -> int:
    if not isinstance(value, int):
        raise BlueprintValidationError(f"{name} must be an integer")
    return value


def _require_float(name: str, value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    raise BlueprintValidationError(f"{name} must be numeric")


def _validate_iso_utc(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:  # pragma: no cover - defensive error path
        raise BlueprintValidationError(
            "last_updated_utc must be ISO-8601 format YYYY-MM-DDTHH:MM:SSZ"
        ) from exc
    return value


@dataclass
class BlueprintMetadata:
    schema_version: str
    document_version: str
    last_updated_utc: str
    review_cadence_days: int
    ubos_alignment: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlueprintMetadata":
        payload = _require_dict("blueprint_metadata", data)
        schema_version = _require_str("schema_version", payload.get("schema_version"))
        document_version = _require_str("document_version", payload.get("document_version"))
        last_updated = _validate_iso_utc(_require_str("last_updated_utc", payload.get("last_updated_utc")))
        cadence = _require_int("review_cadence_days", payload.get("review_cadence_days"))
        alignment_raw = payload.get("ubos_alignment", [])
        if isinstance(alignment_raw, str):
            alignment = [alignment_raw]
        else:
            alignment = [_require_str("ubos_alignment entry", item) for item in _require_list("ubos_alignment", alignment_raw)] if alignment_raw else []
        return cls(
            schema_version=schema_version,
            document_version=document_version,
            last_updated_utc=last_updated,
            review_cadence_days=cadence,
            ubos_alignment=alignment,
        )


@dataclass
class CorePrinciple:
    principle_id: str
    statement: str
    rationale: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CorePrinciple":
        payload = _require_dict("corePrinciple", data)
        return cls(
            principle_id=_require_str("principleId", payload.get("principleId")),
            statement=_require_str("statement", payload.get("statement")),
            rationale=(
                _require_str("rationale", payload["rationale"]) if payload.get("rationale") else None
            ),
        )


@dataclass
class ActiveGoal:
    goal_id: str
    objective: str
    key_results: List[str]
    status: str
    assigned_agent_ids: List[str] = field(default_factory=list)
    process_documentation_uri: Optional[str] = None

    GOAL_ID_PATTERN = re.compile(r"^G-[0-9]{4}$")
    STATUS_OPTIONS = {"pending", "active", "paused", "completed", "failed"}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActiveGoal":
        payload = _require_dict("activeGoal", data)
        goal_id = _require_str("goalId", payload.get("goalId"))
        if not cls.GOAL_ID_PATTERN.match(goal_id):
            raise BlueprintValidationError("goalId must match pattern G-0000")
        status = _require_str("status", payload.get("status"))
        if status not in cls.STATUS_OPTIONS:
            raise BlueprintValidationError(f"status must be one of {sorted(cls.STATUS_OPTIONS)}")
        key_results = [
            _require_str("keyResults entry", item)
            for item in _require_list("keyResults", payload.get("keyResults"))
        ]
        assigned = []
        if payload.get("assignedAgentIds") is not None:
            assigned = [
                _require_str("assignedAgentIds entry", item)
                for item in _require_list("assignedAgentIds", payload.get("assignedAgentIds"))
            ]
        documentation = None
        if payload.get("processDocumentationURI"):
            documentation = _require_str("processDocumentationURI", payload["processDocumentationURI"])
        return cls(
            goal_id=goal_id,
            objective=_require_str("objective", payload.get("objective")),
            key_results=key_results,
            status=status,
            assigned_agent_ids=assigned,
            process_documentation_uri=documentation,
        )


@dataclass
class AgentProfile:
    agent_id: str
    name: str
    capabilities: List[str]
    status: str

    AGENT_ID_PATTERN = re.compile(r"^A-[0-9]{4}$")
    STATUS_OPTIONS = {"active", "inactive", "maintenance"}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentProfile":
        payload = _require_dict("agentRegistry entry", data)
        agent_id = _require_str("agentId", payload.get("agentId"))
        if not cls.AGENT_ID_PATTERN.match(agent_id):
            raise BlueprintValidationError("agentId must match pattern A-0000")
        status = _require_str("status", payload.get("status"))
        if status not in cls.STATUS_OPTIONS:
            raise BlueprintValidationError(f"agent status must be one of {sorted(cls.STATUS_OPTIONS)}")
        capabilities = [
            _require_str("capabilities entry", item)
            for item in _require_list("capabilities", payload.get("capabilities"))
        ]
        return cls(
            agent_id=agent_id,
            name=_require_str("name", payload.get("name")),
            capabilities=capabilities,
            status=status,
        )


@dataclass
class Guardrails:
    operational: Dict[str, Any] = field(default_factory=dict)
    ethical: Dict[str, Any] = field(default_factory=dict)
    adaptive: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Guardrails":
        payload = _require_dict("guardrails", data)
        adaptive = payload.get("adaptive") or {}
        if "reviewCadenceDays" in adaptive:
            _require_int("adaptive.reviewCadenceDays", adaptive["reviewCadenceDays"])
        if "performanceDegradationThreshold" in adaptive:
            _require_float("adaptive.performanceDegradationThreshold", adaptive["performanceDegradationThreshold"])
        return cls(
            operational=_require_dict("guardrails.operational", payload.get("operational", {})),
            ethical=_require_dict("guardrails.ethical", payload.get("ethical", {})),
            adaptive=_require_dict("guardrails.adaptive", adaptive),
        )


@dataclass
class StrategicBlueprint:
    metadata: BlueprintMetadata
    mission_statement: str
    core_principles: List[CorePrinciple]
    active_goals: List[ActiveGoal]
    agent_registry: List[AgentProfile]
    guardrails: Guardrails

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StrategicBlueprint":
        payload = _require_dict("blueprint", data)
        metadata = BlueprintMetadata.from_dict(payload.get("blueprint_metadata", {}))
        mission = _require_str("missionStatement", payload.get("missionStatement"))
        core_principles = [
            CorePrinciple.from_dict(item)
            for item in _require_list("corePrinciples", payload.get("corePrinciples", []))
        ]
        if not core_principles:
            raise BlueprintValidationError("corePrinciples must contain at least one entry")
        active_goals = [
            ActiveGoal.from_dict(item)
            for item in _require_list("activeGoals", payload.get("activeGoals", []))
        ]
        agent_registry = [
            AgentProfile.from_dict(item)
            for item in _require_list("agentRegistry", payload.get("agentRegistry", []))
        ]
        guardrails = Guardrails.from_dict(payload.get("guardrails", {}))
        return cls(
            metadata=metadata,
            mission_statement=mission,
            core_principles=core_principles,
            active_goals=active_goals,
            agent_registry=agent_registry,
            guardrails=guardrails,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "blueprint_metadata": {
                "schema_version": self.metadata.schema_version,
                "document_version": self.metadata.document_version,
                "last_updated_utc": self.metadata.last_updated_utc,
                "review_cadence_days": self.metadata.review_cadence_days,
                "ubos_alignment": self.metadata.ubos_alignment,
            },
            "missionStatement": self.mission_statement,
            "corePrinciples": [
                {
                    "principleId": principle.principle_id,
                    "statement": principle.statement,
                    **({"rationale": principle.rationale} if principle.rationale else {}),
                }
                for principle in self.core_principles
            ],
            "activeGoals": [
                {
                    "goalId": goal.goal_id,
                    "objective": goal.objective,
                    "keyResults": goal.key_results,
                    "status": goal.status,
                    "assignedAgentIds": goal.assigned_agent_ids,
                    **(
                        {"processDocumentationURI": goal.process_documentation_uri}
                        if goal.process_documentation_uri
                        else {}
                    ),
                }
                for goal in self.active_goals
            ],
            "agentRegistry": [
                {
                    "agentId": agent.agent_id,
                    "name": agent.name,
                    "capabilities": agent.capabilities,
                    "status": agent.status,
                }
                for agent in self.agent_registry
            ],
            "guardrails": {
                "operational": self.guardrails.operational,
                "ethical": self.guardrails.ethical,
                "adaptive": self.guardrails.adaptive,
            },
        }


def validate_blueprint_dict(data: Dict[str, Any]) -> StrategicBlueprint:
    """Validate and normalise a Strategic Blueprint payload."""

    return StrategicBlueprint.from_dict(data)


def load_blueprint(path: Path | str) -> StrategicBlueprint:
    """Load and validate a blueprint file stored as JSON or YAML."""

    blueprint_path = Path(path)
    if not blueprint_path.exists():
        raise FileNotFoundError(f"Blueprint file not found: {blueprint_path}")

    if blueprint_path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise BlueprintValidationError("PyYAML is required to load YAML blueprints")
        data = yaml.safe_load(blueprint_path.read_text(encoding="utf-8"))
    else:
        data = json.loads(blueprint_path.read_text(encoding="utf-8"))

    return validate_blueprint_dict(data)
