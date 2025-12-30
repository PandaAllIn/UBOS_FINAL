"""Proposal generation engine for autonomous actions.

This module implements the proposal workflow for Janus-in-Balaur autonomous actions.
Every proposal includes rationale, expected outcome, risk assessment, and rollback plan.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass
import re
from collections import deque
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Optional


class RiskLevel(Enum):
    """Risk classification for proposed actions."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProposalStatus(Enum):
    """Lifecycle states for action proposals."""

    DRAFT = "draft"
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SUSPENDED = "suspended"


@dataclass(slots=True)
class ActionProposal:
    """Structured proposal for an autonomous action."""

    proposal_id: str
    timestamp: str
    vessel_id: str
    mission_context: str
    action_type: str
    rationale: str
    expected_outcome: str
    risk_level: RiskLevel
    risk_mitigation: str
    rollback_plan: str
    tool_name: str
    tool_args: list[str]
    tool_kwargs: dict[str, Any]
    status: ProposalStatus
    metadata: dict[str, Any]
    approval_timestamp: Optional[str] = None
    approval_source: Optional[str] = None
    rejection_reason: Optional[str] = None
    execution_result: Optional[dict[str, Any]] = None

    @property
    def requires_approval(self) -> bool:
        """Check if this proposal requires explicit approval based on risk level."""
        return self.risk_level in (RiskLevel.MEDIUM, RiskLevel.HIGH)

    @property
    def proposal_hash(self) -> str:
        """Generate deterministic hash for proposal content."""
        content = {
            "action_type": self.action_type,
            "tool_name": self.tool_name,
            "tool_args": self.tool_args,
            "tool_kwargs": self.tool_kwargs,
        }
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        """Serialize proposal to dictionary for logging."""
        data = asdict(self)
        data["risk_level"] = self.risk_level.value
        data["status"] = self.status.value
        return data


class ProposalEngine:
    """Engine for generating and tracking action proposals."""

    def __init__(
        self,
        vessel_id: str,
        proposals_log: Path,
        constitutional_memory: Optional[Path] = None,
        auto_approval_policy: Optional[dict[str, Any]] = None,
        known_tools: Optional[Iterable[str]] = None,
    ) -> None:
        self.vessel_id = vessel_id
        self.proposals_log = proposals_log
        self.constitutional_memory = constitutional_memory
        self._proposals: dict[str, ActionProposal] = {}
        # keep a small rolling window of recent rationales for novelty checks
        self._recent_rationales: deque[tuple[str, str]] = deque(maxlen=500)
        self.auto_approval_policy = self._build_auto_policy(auto_approval_policy)
        self._known_tools: set[str] = set()
        if known_tools:
            self.register_known_tools(known_tools)
        self._stats: dict[str, int] = {"completed": 0, "failed": 0}
        self._failure_alert_threshold: float = 0.3
        self._failure_alert_active: bool = False
        self._failure_alert_pending: bool = False
        self._load_proposals()
        self._recompute_stats_from_history()

    @staticmethod
    def _build_auto_policy(config: Optional[dict[str, Any]]) -> dict[str, set[Any]]:
        """Construct the auto-approval policy from config or defaults."""
        default_policy = {
            "risk_levels": {RiskLevel.LOW},
            "action_types": {"analysis", "optimization_experiment", "generate_new_nodes", "reconnaissance"},
            "tool_names": {"llama-cli", "shell", "node_generator"},
        }
        if not config:
            return {
                "risk_levels": set(default_policy["risk_levels"]),
                "action_types": set(default_policy["action_types"]),
                "tool_names": set(default_policy["tool_names"]),
            }

        policy = {
            "risk_levels": set(default_policy["risk_levels"]),
            "action_types": set(default_policy["action_types"]),
            "tool_names": set(default_policy["tool_names"]),
        }
        if "risk_levels" in config:
            policy["risk_levels"] = {RiskLevel(level) if not isinstance(level, RiskLevel) else level for level in config["risk_levels"]}
        if "action_types" in config:
            policy["action_types"] = {ProposalEngine._normalize_action_type(v) for v in config["action_types"]}
        if "tool_names" in config:
            policy["tool_names"] = {v.strip() for v in config["tool_names"] if v}
        return policy

    def _load_proposals(self) -> None:
        """Load existing proposals from log file."""
        if not self.proposals_log.exists():
            self.proposals_log.parent.mkdir(parents=True, exist_ok=True)
            return

        with self.proposals_log.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                proposal = self._deserialize_proposal(data)
                self._proposals[proposal.proposal_id] = proposal

    def _recompute_stats_from_history(self) -> None:
        completed = sum(1 for proposal in self._proposals.values() if proposal.status == ProposalStatus.COMPLETED)
        failed = sum(1 for proposal in self._proposals.values() if proposal.status == ProposalStatus.FAILED)
        self._stats["completed"] = completed
        self._stats["failed"] = failed
        total = completed + failed
        if total == 0:
            self._failure_alert_active = False
            self._failure_alert_pending = False
            return
        failure_rate = self.get_failure_rate()
        self._failure_alert_active = failure_rate >= self._failure_alert_threshold
        self._failure_alert_pending = False

    def _deserialize_proposal(self, data: dict[str, Any]) -> ActionProposal:
        """Reconstruct proposal from logged data."""
        return ActionProposal(
            proposal_id=data["proposal_id"],
            timestamp=data["timestamp"],
            vessel_id=data["vessel_id"],
            mission_context=data["mission_context"],
            action_type=data["action_type"],
            rationale=data["rationale"],
            expected_outcome=data["expected_outcome"],
            risk_level=RiskLevel(data["risk_level"]),
            risk_mitigation=data["risk_mitigation"],
            rollback_plan=data["rollback_plan"],
            tool_name=data["tool_name"],
            tool_args=data["tool_args"],
            tool_kwargs=data["tool_kwargs"],
            status=ProposalStatus(data["status"]),
            metadata=data["metadata"],
            approval_timestamp=data.get("approval_timestamp"),
            approval_source=data.get("approval_source"),
            rejection_reason=data.get("rejection_reason"),
            execution_result=data.get("execution_result"),
        )

    # ---- Normalization & Novelty -------------------------------------------------

    @staticmethod
    def _normalize_action_type(value: str) -> str:
        """Normalize action type to canonical snake_case.

        - Trim whitespace
        - Insert underscores between camelCase/PascalCase boundaries
        - Replace non-alphanumeric groups with single underscore
        - Lowercase and strip leading/trailing underscores
        """
        if not value:
            return "unknown"
        s = value.strip()
        # insert underscore between lower-to-upper boundaries (fooBar -> foo_Bar)
        s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
        # replace non-alphanum with underscores
        s = re.sub(r"[^A-Za-z0-9]+", "_", s)
        s = s.strip("_").lower()
        return s

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        """Simple tokenization for novelty checking.

        - Lowercase
        - Alphanumeric word tokens of length >= 3
        """
        if not text:
            return set()
        tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
        return {t for t in tokens if len(t) >= 3}

    @classmethod
    def _jaccard(cls, a: str, b: str) -> float:
        ta = cls._tokenize(a)
        tb = cls._tokenize(b)
        if not ta or not tb:
            return 0.0
        inter = len(ta & tb)
        if inter == 0:
            return 0.0
        union = len(ta | tb)
        return inter / union if union else 0.0

    def is_novel(
        self,
        action_type: str,
        rationale: str,
        threshold: float = 0.75,
        search_window: int = 200,
    ) -> tuple[bool, float, Optional[str]]:
        """Assess whether a proposal is novel compared to recent history.

        Returns (is_novel, max_similarity, duplicate_of_id)
        """
        norm_type = self._normalize_action_type(action_type)

        # Search most recent proposals (limited window) for same action type
        candidates: list[ActionProposal] = []
        # Fast path via rolling window (proposal_id, rationale_norm_type)
        checked = 0
        for pid, atype in reversed(self._recent_rationales):
            if atype == norm_type:
                p = self._proposals.get(pid)
                if p is not None:
                    candidates.append(p)
            checked += 1
            if checked >= search_window:
                break

        # Fallback if recent window didn't find enough
        if not candidates:
            for p in reversed(list(self._proposals.values())):
                if self._normalize_action_type(p.action_type) == norm_type:
                    candidates.append(p)
                if len(candidates) >= search_window:
                    break

        max_sim = 0.0
        dup_id: Optional[str] = None
        for p in candidates:
            sim = self._jaccard(p.rationale, rationale)
            if sim > max_sim:
                max_sim = sim
                dup_id = p.proposal_id

        return (max_sim < threshold, max_sim, dup_id)

    def create_proposal(
        self,
        mission_context: str,
        action_type: str,
        rationale: str,
        expected_outcome: str,
        risk_level: RiskLevel,
        risk_mitigation: str,
        rollback_plan: str,
        tool_name: str,
        tool_args: list[str],
        tool_kwargs: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
        *,
        enforce_novelty: bool = True,
        novelty_threshold: float = 0.75,
        novelty_window: int = 200,
    ) -> ActionProposal:
        """Create a new action proposal with constitutional alignment check."""
        proposal_id = f"janus-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        norm_action = self._normalize_action_type(action_type)

        # Novelty guard: suppress near-duplicate proposals of same action type
        if enforce_novelty:
            is_new, sim, dup = self.is_novel(norm_action, rationale, threshold=novelty_threshold, search_window=novelty_window)
            if not is_new:
                # Record a lightweight suppression event in the proposals log for observability
                suppressed = ActionProposal(
                    proposal_id=proposal_id,
                    timestamp=timestamp,
                    vessel_id=self.vessel_id,
                    mission_context=mission_context,
                    action_type=norm_action,
                    rationale=rationale,
                    expected_outcome=expected_outcome,
                    risk_level=risk_level,
                    risk_mitigation=risk_mitigation,
                    rollback_plan=rollback_plan,
                    tool_name=tool_name,
                    tool_args=tool_args,
                    tool_kwargs=tool_kwargs or {},
                    status=ProposalStatus.DRAFT,
                    metadata={
                        **(metadata or {}),
                        "suppressed": True,
                        "novelty_score": round(float(sim), 3),
                        "duplicate_of": dup,
                        "action_type_normalized": norm_action,
                    },
                )
                self._persist_proposal(suppressed)
                # do not add to in-memory proposals to avoid inflating state
                return suppressed

        proposal = ActionProposal(
            proposal_id=proposal_id,
            timestamp=timestamp,
            vessel_id=self.vessel_id,
            mission_context=mission_context,
            action_type=norm_action,
            rationale=rationale,
            expected_outcome=expected_outcome,
            risk_level=risk_level,
            risk_mitigation=risk_mitigation,
            rollback_plan=rollback_plan,
            tool_name=tool_name,
            tool_args=tool_args,
            tool_kwargs=tool_kwargs or {},
            status=ProposalStatus.PROPOSED,
            metadata={
                **(metadata or {}),
                "action_type_normalized": norm_action,
                "original_action_type": action_type,
            },
        )

        # Store in memory and persist to log
        self._proposals[proposal_id] = proposal
        self._persist_proposal(proposal)
        # Update rolling window index
        self._recent_rationales.append((proposal_id, norm_action))

        return proposal

    def _persist_proposal(self, proposal: ActionProposal) -> None:
        """Append proposal to JSONL log."""
        with self.proposals_log.open("a", encoding="utf-8") as f:
            json.dump(proposal.to_dict(), f, separators=(",", ":"))
            f.write("\n")

    def approve_proposal(
        self,
        proposal_id: str,
        approval_source: str = "first_citizen",
    ) -> ActionProposal:
        """Mark proposal as approved for execution."""
        if proposal_id not in self._proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")

        proposal = self._proposals[proposal_id]
        proposal.status = ProposalStatus.APPROVED
        proposal.approval_timestamp = datetime.now(timezone.utc).isoformat()
        proposal.approval_source = approval_source

        self._persist_proposal(proposal)
        return proposal

    def reject_proposal(
        self,
        proposal_id: str,
        reason: str,
    ) -> ActionProposal:
        """Mark proposal as rejected with reason."""
        if proposal_id not in self._proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")

        proposal = self._proposals[proposal_id]
        proposal.status = ProposalStatus.REJECTED
        proposal.rejection_reason = reason

        self._persist_proposal(proposal)
        return proposal

    def mark_executing(self, proposal_id: str) -> ActionProposal:
        """Mark proposal as currently executing."""
        if proposal_id not in self._proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")

        proposal = self._proposals[proposal_id]
        proposal.status = ProposalStatus.EXECUTING
        self._persist_proposal(proposal)
        return proposal

    def mark_completed(
        self,
        proposal_id: str,
        result: dict[str, Any],
    ) -> ActionProposal:
        """Mark proposal as successfully completed."""
        if proposal_id not in self._proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")

        proposal = self._proposals[proposal_id]
        quality_summary = result.get("quality_summary")
        if quality_summary:
            mission_quality = proposal.metadata.setdefault("mission_quality", {})
            mission_quality["summary"] = quality_summary.get("summary")
            mission_quality["quality"] = quality_summary.get("quality")
            if quality_summary.get("warnings"):
                mission_quality["warnings"] = quality_summary["warnings"]
            if quality_summary.get("excellence"):
                mission_quality["excellence"] = quality_summary["excellence"]
        self._record_outcome(success=True)
        proposal.status = ProposalStatus.COMPLETED
        proposal.execution_result = result
        self._persist_proposal(proposal)
        return proposal

    # ---- Tool Registry -------------------------------------------------------
    def register_known_tools(self, tools: Iterable[str]) -> None:
        for tool in tools:
            if not tool:
                continue
            cleaned = str(tool).strip()
            if cleaned:
                self._known_tools.add(cleaned)

    def is_known_tool(self, tool_name: str) -> bool:
        return str(tool_name).strip() in self._known_tools

    def list_known_tools(self) -> list[str]:
        return sorted(self._known_tools)

    # ---- Failure Rate Tracking -----------------------------------------------
    def _record_outcome(self, *, success: bool) -> None:
        if success:
            self._stats["completed"] += 1
        else:
            self._stats["failed"] += 1

        total = self._stats["completed"] + self._stats["failed"]
        if total == 0:
            return

        failure_rate = self.get_failure_rate()
        threshold = self._failure_alert_threshold
        if total >= 5 and failure_rate >= threshold and not self._failure_alert_active:
            self._failure_alert_active = True
            self._failure_alert_pending = True
        elif self._failure_alert_active and failure_rate < threshold * 0.5:
            self._failure_alert_active = False

    def get_failure_rate(self) -> float:
        total = self._stats["completed"] + self._stats["failed"]
        if total == 0:
            return 0.0
        return self._stats["failed"] / total

    def pop_failure_alert(self) -> bool:
        if self._failure_alert_pending:
            self._failure_alert_pending = False
            return True
        return False

    def mark_failed(
        self,
        proposal_id: str,
        error: dict[str, Any],
    ) -> ActionProposal:
        """Mark proposal as failed during execution."""
        if proposal_id not in self._proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")

        proposal = self._proposals[proposal_id]
        self._record_outcome(success=False)
        proposal.status = ProposalStatus.FAILED
        proposal.execution_result = error
        self._persist_proposal(proposal)
        return proposal

    def suspend(self, proposal_id: str) -> ActionProposal:
        """Suspend an approved or executing proposal (emergency stop)."""
        if proposal_id not in self._proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")
        proposal = self._proposals[proposal_id]
        proposal.status = ProposalStatus.SUSPENDED
        self._persist_proposal(proposal)
        return proposal

    def get_proposal(self, proposal_id: str) -> Optional[ActionProposal]:
        """Retrieve proposal by ID."""
        return self._proposals.get(proposal_id)

    def list_pending_approvals(self) -> list[ActionProposal]:
        """Get all proposals awaiting approval."""
        return [
            p
            for p in self._proposals.values()
            if p.status == ProposalStatus.PROPOSED
        ]

    def list_approved_pending_execution(self) -> list[ActionProposal]:
        """Get all approved proposals not yet executed."""
        return [
            p
            for p in self._proposals.values()
            if p.status == ProposalStatus.APPROVED
        ]

    def list_all(self) -> list[ActionProposal]:
        """Return all proposals ordered by timestamp ascending."""
        return sorted(self._proposals.values(), key=lambda p: p.timestamp)

    def list_auto_approvable(self) -> list[ActionProposal]:
        """List proposals that meet auto-approval policy."""
        return [
            p
            for p in self._proposals.values()
            if self.is_auto_approvable(p)
        ]

    def is_auto_approvable(self, proposal: ActionProposal) -> bool:
        """Check whether a proposal can be auto-approved."""
        if proposal.status != ProposalStatus.PROPOSED:
            return False
        policy = self.auto_approval_policy
        if proposal.risk_level not in policy["risk_levels"]:
            return False
        if self._normalize_action_type(proposal.action_type) not in policy["action_types"]:
            return False
        if proposal.tool_name not in policy["tool_names"]:
            return False
        return True

    def get_approval_rate(self, days: int = 30) -> float:
        """Calculate approval rate over recent history."""
        # Simple implementation - can be enhanced with time filtering
        total = len([p for p in self._proposals.values() if p.status in (ProposalStatus.APPROVED, ProposalStatus.REJECTED)])
        if total == 0:
            return 1.0
        approved = len([p for p in self._proposals.values() if p.status == ProposalStatus.APPROVED])
        return approved / total

    def validate_constitutional_alignment(self, proposal: ActionProposal) -> tuple[bool, str]:
        """Validate proposal aligns with constitutional principles.

        Returns (is_valid, reason) tuple.
        """
        # Basic validation rules based on Autonomous Vessel Protocol

        # 1. Check risk level matches action type
        high_risk_actions = {"system_config", "network_config", "security_change"}
        if proposal.action_type in high_risk_actions and proposal.risk_level != RiskLevel.HIGH:
            return False, f"Action type '{proposal.action_type}' must be classified as HIGH risk"

        # 2. Ensure rationale is substantive
        if len(proposal.rationale) < 20:
            return False, "Rationale must be substantive (minimum 20 characters)"

        # 3. Ensure rollback plan exists for medium/high risk actions
        if proposal.risk_level in (RiskLevel.MEDIUM, RiskLevel.HIGH):
            if len(proposal.rollback_plan) < 10:
                return False, "Medium/High risk actions require detailed rollback plan"

        # 4. Check mission context is provided
        if not proposal.mission_context or proposal.mission_context == "unknown":
            return False, "Actions must have clear mission context"

        return True, "Proposal aligns with constitutional principles"
