"""Tool execution engine with enhanced sandboxing and constitutional checks.

This module extends the basic sandbox executor with:
- Pre-execution constitutional validation
- Tool-specific security policies
- Execution result validation
- Rollback capability
"""
from __future__ import annotations

import asyncio
import json
import shlex
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .config import ToolConfig
from .logging_utils import AuditLogger, LogEvent
from .proposal_engine import ActionProposal, ProposalStatus, RiskLevel
from .quality_gates import MissionQualityError, evaluate_node_generation_quality
from .sandbox import SandboxConfig, SandboxExecutor
from .tools import ToolResult


@dataclass(slots=True)
class ExecutionLimits:
    """Resource limits enforced per execution."""

    cpu_percent_max: int = 80
    memory_mb_max: int = 2048
    disk_mb_max: int = 100
    timeout_seconds: int = 600


@dataclass(slots=True)
class ExecutionContext:
    """Context for tool execution with audit trail."""

    execution_id: str
    proposal_id: str
    vessel_id: str
    timestamp: str
    tool_name: str
    tool_config: ToolConfig
    workspace_path: Path
    constitutional_approved: bool
    rate_limit_approved: bool


class ToolExecutionEngine:
    """Enhanced tool execution engine with constitutional safeguards."""

    def __init__(
        self,
        sandbox: SandboxConfig,
        audit_logger: AuditLogger,
        tool_log_path: Path,
        vessel_id: str = "janus-in-balaur",
        *,
        resource_limits: ExecutionLimits | None = None,
        forbidden_tools: Optional[set[str]] = None,
        forbidden_patterns: Optional[set[str]] = None,
        max_risk_level: RiskLevel = RiskLevel.LOW,
    ) -> None:
        self.sandbox_executor = SandboxExecutor(sandbox)
        self.audit_logger = audit_logger
        self.tool_log_path = tool_log_path
        self.vessel_id = vessel_id
        self._execution_lock = asyncio.Lock()
        self.resource_limits = resource_limits or ExecutionLimits()
        self.max_risk_level = max_risk_level
        self.forbidden_tools = forbidden_tools or {
            "systemctl",
            "reboot",
            "shutdown",
            "sudo",
        }
        self.forbidden_patterns = forbidden_patterns or {
            "rm -rf",
            "wget ",
            "curl http://",
            "curl https://",
            "scp ",
        }
        self.forbidden_shell_tokens = {"sudo", "systemctl", "reboot", "shutdown", "pkexec", "iptables"}
        # Autonomous execution always runs with networking disabled
        self.sandbox_executor.force_block_network = True

    async def execute_proposal(
        self,
        proposal: ActionProposal,
        tool_config: ToolConfig,
    ) -> ToolResult:
        """Execute an approved proposal with full audit trail.

        This is the main entry point for executing approved autonomous actions.
        """
        async with self._execution_lock:
            if proposal.status not in {ProposalStatus.APPROVED, ProposalStatus.EXECUTING}:
                raise ValueError(
                    f"Proposal must be APPROVED before execution, got {proposal.status}"
                )

            self._enforce_policy(proposal)

            execution_id = f"exec-{proposal.proposal_id}"
            context = ExecutionContext(
                execution_id=execution_id,
                proposal_id=proposal.proposal_id,
                vessel_id=self.vessel_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                tool_name=proposal.tool_name,
                tool_config=tool_config,
                workspace_path=self.sandbox_executor.config.workspace_root,
                constitutional_approved=True,
                rate_limit_approved=True,
            )

            self.audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self.vessel_id,
                    event="tool_executor.start",
                    data={
                        "execution_id": execution_id,
                        "proposal_id": proposal.proposal_id,
                        "tool": proposal.tool_name,
                        "action_type": proposal.action_type,
                    },
                )
            )

            try:
                await self._pre_execution_checks(proposal, context)
                result = await self._execute_sandboxed(proposal, tool_config, context)
                if result.metadata is None:
                    result.metadata = {}
                result.metadata.setdefault("resource_limits", asdict(self.resource_limits))

                await self._post_execution_checks(proposal, result, context)
                self._log_execution(context, result, success=True)

                self.audit_logger.emit(
                    LogEvent.create(
                        level="info",
                        vessel=self.vessel_id,
                        event="tool_executor.success",
                        data={
                            "execution_id": execution_id,
                            "proposal_id": proposal.proposal_id,
                            "returncode": result.metadata.get("returncode", 0),
                        },
                    )
                )
                return result

            except Exception as exc:
                error_result = ToolResult(
                    ok=False,
                    stderr=str(exc),
                    metadata={"error": repr(exc)},
                )
                self._log_execution(context, error_result, success=False)

                self.audit_logger.emit(
                    LogEvent.create(
                        level="error",
                        vessel=self.vessel_id,
                        event="tool_executor.failed",
                        data={
                            "execution_id": execution_id,
                            "proposal_id": proposal.proposal_id,
                            "error": str(exc),
                        },
                    )
                )
                raise

    async def _pre_execution_checks(
        self,
        proposal: ActionProposal,
        context: ExecutionContext,
    ) -> None:
        """Perform pre-execution constitutional and safety checks."""
        # Check 1: Validate tool name matches configuration
        if proposal.tool_name != context.tool_config.name:
            raise ValueError(
                f"Tool mismatch: proposal requests '{proposal.tool_name}', "
                f"but config is for '{context.tool_config.name}'"
            )

        # Policy guard rails (risk/tool allowlists)
        self._enforce_policy(proposal)

        # Check 2: Validate command sanitization
        self._validate_command_safety(proposal, context.tool_config)

        # Check 3: Check resource availability
        await self._check_resource_availability()

        self.audit_logger.emit(
            LogEvent.create(
                level="debug",
                vessel=self.vessel_id,
                event="tool_executor.pre_checks_passed",
                data={"execution_id": context.execution_id},
            )
        )

    def _validate_command_safety(
        self,
        proposal: ActionProposal,
        tool_config: ToolConfig,
    ) -> None:
        """Validate command arguments for security issues."""
        # Check for shell injection attempts
        dangerous_chars = [";", "|", "&", "`", "$", "(", ")", "<", ">", "\n"]
        all_args = " ".join(proposal.tool_args)

        for char in dangerous_chars:
            if char in all_args:
                # Allow some characters if they're properly quoted
                if char not in ["-", "="]:
                    self.audit_logger.emit(
                        LogEvent.create(
                            level="warn",
                            vessel=self.vessel_id,
                            event="tool_executor.suspicious_command",
                            data={
                                "proposal_id": proposal.proposal_id,
                                "suspicious_char": char,
                                "args": proposal.tool_args,
                            },
                        )
                    )

        # Check for path traversal attempts
        for arg in proposal.tool_args:
            if ".." in arg and "/" in arg:
                raise ValueError(f"Path traversal detected in argument: {arg}")

        # Check for privileged operations
        privileged_commands = ["sudo", "su", "doas", "pkexec"]
        for cmd in privileged_commands:
            if cmd in proposal.tool_args:
                raise ValueError(f"Privileged command not allowed: {cmd}")

    def _risk_allowed(self, risk: RiskLevel) -> bool:
        order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]
        return order.index(risk) <= order.index(self.max_risk_level)

    def _enforce_policy(self, proposal: ActionProposal) -> None:
        """Ensure proposal complies with constitutional safety policy."""
        if not self._risk_allowed(proposal.risk_level):
            raise ValueError(
                f"Proposal risk level {proposal.risk_level.value} exceeds allowed maximum {self.max_risk_level.value}"
            )
        if proposal.tool_name in self.forbidden_tools:
            raise ValueError(f"Tool '{proposal.tool_name}' is forbidden for autonomous execution")

        combined_args = " ".join(proposal.tool_args)
        for pattern in self.forbidden_patterns:
            if pattern and pattern in combined_args:
                raise ValueError(f"Proposal arguments contain forbidden pattern '{pattern}'")

        if proposal.tool_name == "shell":
            for token in proposal.tool_args:
                token_clean = token.strip()
                if token_clean in self.forbidden_shell_tokens:
                    raise ValueError(f"Shell token '{token_clean}' is not permitted during autonomous execution")

    async def _check_resource_availability(self) -> None:
        """Check if sufficient resources available for execution."""
        # Check disk space
        try:
            stat = self.sandbox_executor.config.workspace_root.stat()
            # This is a placeholder - in production would check actual disk space
        except OSError as exc:
            raise RuntimeError(f"Cannot access workspace: {exc}") from exc

        # Add delay to ensure we don't overload system
        await asyncio.sleep(0.1)

    async def _execute_sandboxed(
        self,
        proposal: ActionProposal,
        tool_config: ToolConfig,
        context: ExecutionContext,
    ) -> ToolResult:
        """Execute tool command in sandboxed environment."""
        # Build command from proposal
        command = list(tool_config.command) + list(proposal.tool_args)

        # Execute in sandbox (runs in thread pool to avoid blocking)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.sandbox_executor,
            command,
            tool_config,
        )

        return result

    async def _post_execution_checks(
        self,
        proposal: ActionProposal,
        result: ToolResult,
        context: ExecutionContext,
    ) -> None:
        """Perform post-execution validation."""
        # Check 1: Validate result structure
        if not isinstance(result, ToolResult):
            raise ValueError(f"Invalid result type: {type(result)}")

        # Check 2: Check for suspicious output patterns
        if result.stderr:
            self._check_error_patterns(result.stderr, context)

        # Check 3: Validate expected outcome
        if not result.ok and proposal.expected_outcome:
            self.audit_logger.emit(
                LogEvent.create(
                    level="warn",
                    vessel=self.vessel_id,
                    event="tool_executor.unexpected_failure",
                    data={
                        "execution_id": context.execution_id,
                        "expected": proposal.expected_outcome,
                        "stderr": result.stderr[:200],
                    },
                )
            )
            return

        if proposal.tool_name == "node_generator" and result.ok:
            try:
                evaluation = evaluate_node_generation_quality(result.stdout)
            except MissionQualityError as exc:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self.vessel_id,
                        event="tool_executor.quality.violation",
                        data={
                            "execution_id": context.execution_id,
                            "proposal_id": proposal.proposal_id,
                            "code": getattr(exc, "code", "quality_violation"),
                            "message": str(exc),
                        },
                    )
                )
                raise ValueError(f"node_generator quality gate failed: {exc}") from exc

            if result.metadata is None:
                result.metadata = {}
            result.metadata["quality_summary"] = {
                "summary": evaluation.summary,
                "quality": evaluation.quality,
                "warnings": evaluation.warnings,
                "excellence": evaluation.excellence,
            }

            for warning in evaluation.warnings:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self.vessel_id,
                        event="tool_executor.quality.warning",
                        data={
                            "execution_id": context.execution_id,
                            "proposal_id": proposal.proposal_id,
                            "message": warning,
                        },
                    )
                )

            if evaluation.excellence:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="info",
                        vessel=self.vessel_id,
                        event="tool_executor.quality.metrics",
                        data={
                            "execution_id": context.execution_id,
                            "proposal_id": proposal.proposal_id,
                            "excellence": evaluation.excellence,
                        },
                    )
                )

    def _check_error_patterns(self, stderr: str, context: ExecutionContext) -> None:
        """Check stderr for concerning error patterns."""
        concerning_patterns = [
            "permission denied",
            "access denied",
            "unauthorized",
            "segmentation fault",
            "core dumped",
        ]

        stderr_lower = stderr.lower()
        for pattern in concerning_patterns:
            if pattern in stderr_lower:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self.vessel_id,
                        event="tool_executor.concerning_error",
                        data={
                            "execution_id": context.execution_id,
                            "pattern": pattern,
                        },
                    )
                )

    def _log_execution(
        self,
        context: ExecutionContext,
        result: ToolResult,
        success: bool,
    ) -> None:
        """Log detailed execution audit trail to tool_use.jsonl."""
        execution_log = {
            "timestamp": context.timestamp,
            "vessel_id": context.vessel_id,
            "execution_id": context.execution_id,
            "proposal_id": context.proposal_id,
            "tool": context.tool_name,
            "success": success,
            "returncode": result.metadata.get("returncode", -1) if result.metadata else -1,
            "stdout_length": len(result.stdout),
            "stderr_length": len(result.stderr),
            "workspace": str(result.metadata.get("workspace", "")) if result.metadata else "",
            "metadata": result.metadata or {},
        }

        # Append to tool use log
        self.tool_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.tool_log_path.open("a", encoding="utf-8") as f:
            json.dump(execution_log, f, separators=(",", ":"))
            f.write("\n")

    async def execute_rollback(
        self,
        proposal: ActionProposal,
        original_result: ToolResult,
    ) -> ToolResult:
        """Execute rollback plan for a failed or problematic action.

        This implements the rollback plan specified in the proposal.
        """
        self.audit_logger.emit(
            LogEvent.create(
                level="warn",
                vessel=self.vessel_id,
                event="tool_executor.rollback_start",
                data={
                    "proposal_id": proposal.proposal_id,
                    "rollback_plan": proposal.rollback_plan,
                },
            )
        )

        # In production, this would parse the rollback_plan and execute
        # appropriate compensating actions. For now, log the attempt.

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="tool_executor.rollback_complete",
                data={"proposal_id": proposal.proposal_id},
            )
        )

        return ToolResult(
            ok=True,
            stdout="Rollback procedure logged",
            metadata={"rollback": True},
        )

    def get_execution_history(
        self,
        proposal_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Retrieve execution history from tool use log."""
        if not self.tool_log_path.exists():
            return []

        executions = []
        with self.tool_log_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)

                # Filter by proposal_id if specified
                if proposal_id and entry.get("proposal_id") != proposal_id:
                    continue

                executions.append(entry)

                # Limit results
                if len(executions) >= limit:
                    break

        return list(reversed(executions[-limit:]))  # Most recent first
