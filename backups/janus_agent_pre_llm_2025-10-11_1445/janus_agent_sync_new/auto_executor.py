"""Automatic proposal execution for Mode Beta autonomous operation."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional

from .config import ToolConfig
from .logging_utils import AuditLogger, LogEvent
from .proposal_engine import ActionProposal, ProposalStatus, RiskLevel

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    from .proposal_engine import ProposalEngine
    from .tool_executor import ToolExecutionEngine


def _normalize_action_type(value: str) -> str:
    """Normalize action type strings to canonical snake_case."""
    if not value:
        return "unknown"
    s = value.strip()
    # insert underscore between lower/upper boundaries
    normalized = []
    for idx, char in enumerate(s):
        if idx > 0 and char.isupper() and (s[idx - 1].islower() or (idx + 1 < len(s) and s[idx + 1].islower())):
            normalized.append("_")
        normalized.append(char)
    s = "".join(normalized)
    # replace non-alphanumeric runs with underscore
    cleaned = []
    last_was_sep = False
    for char in s:
        if char.isalnum():
            cleaned.append(char.lower())
            last_was_sep = False
        else:
            if not last_was_sep:
                cleaned.append("_")
                last_was_sep = True
    result = "".join(cleaned).strip("_")
    return result or "unknown"


@dataclass(slots=True)
class ResourceLimits:
    """Execution resource limits."""

    cpu_percent_max: int = 80
    memory_mb_max: int = 2048
    disk_mb_max: int = 100
    timeout_seconds: int = 600


@dataclass(slots=True)
class AutoExecutorConfig:
    """Configuration for autonomous execution."""

    enabled: bool = True
    poll_interval_seconds: float = 60.0
    auto_approval_source: str = "auto-approval-system"
    allowed_tools: tuple[str, ...] = ("llama-cli", "shell", "node_generator")
    allowed_action_types: tuple[str, ...] = ("analysis", "optimization_experiment", "generate_new_nodes", "reconnaissance")
    max_risk_level: RiskLevel = RiskLevel.LOW
    resource_limits: ResourceLimits = field(default_factory=ResourceLimits)

    def __post_init__(self) -> None:
        self.allowed_tools = tuple(tool.strip() for tool in self.allowed_tools)
        self.allowed_action_types = tuple(_normalize_action_type(action) for action in self.allowed_action_types)

    def allows(self, proposal: ActionProposal) -> bool:
        """Check whether a proposal is allowed under this config."""
        allowed_levels = {RiskLevel.LOW}
        if self.max_risk_level == RiskLevel.MEDIUM:
            allowed_levels.add(RiskLevel.MEDIUM)
        elif self.max_risk_level == RiskLevel.HIGH:
            allowed_levels.update({RiskLevel.MEDIUM, RiskLevel.HIGH})
        if proposal.risk_level not in allowed_levels:
            return False
        if proposal.tool_name not in self.allowed_tools:
            return False
        if _normalize_action_type(proposal.action_type) not in self.allowed_action_types:
            return False
        return True


class AutoExecutor:
    """Background worker that auto-approves and executes low-risk proposals."""

    def __init__(
        self,
        proposal_engine: "ProposalEngine",
        tool_executor: "ToolExecutionEngine",
        tool_configs: Dict[str, ToolConfig],
        audit_logger: AuditLogger,
        config: AutoExecutorConfig,
    ) -> None:
        self._proposal_engine = proposal_engine
        self._tool_executor = tool_executor
        self._tool_configs = tool_configs
        self._audit_logger = audit_logger
        self._config = config
        self._task: Optional[asyncio.Task[None]] = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        """Start the auto executor background loop."""
        if not self._config.enabled or (self._task and not self._task.done()):
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run_loop(), name="janus-auto-executor")
        self._audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self._proposal_engine.vessel_id,
                event="auto_executor.started",
                data={"poll_interval_seconds": self._config.poll_interval_seconds},
            )
        )

    async def stop(self) -> None:
        """Stop the auto executor loop."""
        if not self._task:
            return
        self._stop_event.set()
        await self._task
        self._audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self._proposal_engine.vessel_id,
                event="auto_executor.stopped",
                data={},
            )
        )

    async def _run_loop(self) -> None:
        """Continuously poll for proposals to execute."""
        interval = max(5.0, float(self._config.poll_interval_seconds))
        self._audit_logger.emit(
            LogEvent.create(
                level="debug",
                vessel=self._proposal_engine.vessel_id,
                event="auto_executor.loop_entered",
                data={"interval": interval},
            )
        )
        while not self._stop_event.is_set():
            self._audit_logger.emit(
                LogEvent.create(
                    level="debug",
                    vessel=self._proposal_engine.vessel_id,
                    event="auto_executor.loop_iteration",
                    data={"stop_event_set": self._stop_event.is_set()},
                )
            )
            try:
                await self._tick()
            except Exception as exc:  # pragma: no cover - defensive logging
                self._audit_logger.emit(
                    LogEvent.create(
                        level="error",
                        vessel=self._proposal_engine.vessel_id,
                        event="auto_executor.error",
                        data={"error": str(exc)},
                    )
                )
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=interval)
                # If we reach here WITHOUT TimeoutError, stop_event was set
                self._audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self._proposal_engine.vessel_id,
                        event="auto_executor.stop_event_triggered",
                        data={"stop_event_set": self._stop_event.is_set()},
                    )
                )
            except asyncio.TimeoutError:
                continue
        self._audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self._proposal_engine.vessel_id,
                event="auto_executor.loop_exited",
                data={"stop_event_set": self._stop_event.is_set()},
            )
        )

    async def _tick(self) -> None:
        """Process a single proposal if available."""
        proposal = self._select_next_proposal()
        if proposal is None:
            return

        if proposal.status == ProposalStatus.PROPOSED:
            if not self._proposal_engine.is_auto_approvable(proposal) or not self._config.allows(proposal):
                return
            proposal = self._proposal_engine.approve_proposal(
                proposal.proposal_id,
                approval_source=self._config.auto_approval_source,
            )
            self._audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self._proposal_engine.vessel_id,
                    event="auto_executor.auto_approved",
                    data={
                        "proposal_id": proposal.proposal_id,
                        "action_type": proposal.action_type,
                        "tool": proposal.tool_name,
                    },
                )
            )

        await self._execute(proposal)

    def _select_next_proposal(self) -> Optional[ActionProposal]:
        """Find the next proposal ready for execution."""
        approved = self._proposal_engine.list_approved_pending_execution()
        if approved:
            # Execute the oldest approved proposal first
            return sorted(approved, key=lambda p: p.timestamp)[0]

        auto_candidates = self._proposal_engine.list_auto_approvable()
        if auto_candidates:
            return sorted(auto_candidates, key=lambda p: p.timestamp)[0]
        return None

    async def _execute(self, proposal: ActionProposal) -> None:
        """Execute proposal and update lifecycle state."""
        tool_config = self._tool_configs.get(proposal.tool_name)
        if tool_config is None:
            self._audit_logger.emit(
                LogEvent.create(
                    level="error",
                    vessel=self._proposal_engine.vessel_id,
                    event="auto_executor.missing_tool_config",
                    data={
                        "proposal_id": proposal.proposal_id,
                        "tool": proposal.tool_name,
                    },
                )
            )
            self._proposal_engine.mark_failed(
                proposal.proposal_id,
                {
                    "error": "tool_configuration_missing",
                    "message": f"No tool configuration for '{proposal.tool_name}'",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
            if self._proposal_engine.pop_failure_alert():
                self._audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self._proposal_engine.vessel_id,
                        event="auto_executor.failure_rate_alert",
                        data={
                            "failure_rate": self._proposal_engine.get_failure_rate(),
                            "proposal_id": proposal.proposal_id,
                        },
                    )
                )
            return

        self._proposal_engine.mark_executing(proposal.proposal_id)
        try:
            result = await self._tool_executor.execute_proposal(proposal, tool_config)
        except Exception as exc:
            self._proposal_engine.mark_failed(
                proposal.proposal_id,
                {
                    "error": "execution_failed",
                    "message": str(exc),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )
            self._audit_logger.emit(
                LogEvent.create(
                    level="error",
                    vessel=self._proposal_engine.vessel_id,
                    event="auto_executor.execution_failed",
                    data={
                        "proposal_id": proposal.proposal_id,
                        "error": str(exc),
                    },
                )
            )
            if self._proposal_engine.pop_failure_alert():
                self._audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self._proposal_engine.vessel_id,
                        event="auto_executor.failure_rate_alert",
                        data={
                            "failure_rate": self._proposal_engine.get_failure_rate(),
                            "proposal_id": proposal.proposal_id,
                        },
                    )
                )
            return

        payload = self._build_execution_payload(result)
        self._proposal_engine.mark_completed(proposal.proposal_id, payload)
        self._audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self._proposal_engine.vessel_id,
                event="auto_executor.execution_completed",
                data={
                    "proposal_id": proposal.proposal_id,
                    "returncode": payload.get("returncode"),
                },
            )
        )

    @staticmethod
    def _build_execution_payload(result: Any) -> dict[str, object]:
        """Convert execution result into proposal payload."""
        metadata = getattr(result, "metadata", None) or {}
        return {
            "returncode": metadata.get("returncode", 0),
            "stdout": getattr(result, "stdout", ""),
            "stderr": getattr(result, "stderr", ""),
            "workspace": metadata.get("workspace"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "quality_summary": metadata.get("quality_summary"),
        }
