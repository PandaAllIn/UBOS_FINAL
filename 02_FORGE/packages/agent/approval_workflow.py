"""Human approval workflow for Mode Alpha autonomous proposals.

This module implements the approval workflow where proposals await human
review and explicit approval/rejection from the First Citizen.
"""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from .logging_utils import AuditLogger, LogEvent
from .proposal_engine import ActionProposal, ProposalEngine, ProposalStatus


@dataclass(slots=True)
class ApprovalWorkflowConfig:
    """Configuration for approval workflow."""

    approval_queue_path: Path
    approval_timeout: timedelta = timedelta(hours=24)
    auto_reject_on_timeout: bool = False
    notification_enabled: bool = True
    notification_script: Optional[Path] = None


class ApprovalQueue:
    """Queue for managing proposals awaiting approval."""

    def __init__(self, queue_path: Path) -> None:
        self.queue_path = queue_path
        self.queue_path.parent.mkdir(parents=True, exist_ok=True)

    def add_to_queue(self, proposal: ActionProposal) -> None:
        """Add proposal to approval queue."""
        queue_entry = {
            "proposal_id": proposal.proposal_id,
            "timestamp": proposal.timestamp,
            "action_type": proposal.action_type,
            "risk_level": proposal.risk_level.value,
            "summary": {
                "rationale": proposal.rationale,
                "expected_outcome": proposal.expected_outcome,
                "tool": proposal.tool_name,
            },
        }

        # Append to queue file
        with self.queue_path.open("a", encoding="utf-8") as f:
            json.dump(queue_entry, f, separators=(",", ":"))
            f.write("\n")

    def load_pending(self) -> list[dict[str, Any]]:
        """Load all pending proposals from queue."""
        if not self.queue_path.exists():
            return []

        pending = []
        with self.queue_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                pending.append(json.loads(line))
        return pending

    def clear(self) -> None:
        """Clear approval queue (after processing)."""
        if self.queue_path.exists():
            self.queue_path.unlink()


class ApprovalWorkflow:
    """Workflow manager for human approval of autonomous proposals."""

    def __init__(
        self,
        config: ApprovalWorkflowConfig,
        proposal_engine: ProposalEngine,
        audit_logger: AuditLogger,
        vessel_id: str = "janus-in-balaur",
    ) -> None:
        self.config = config
        self.proposal_engine = proposal_engine
        self.audit_logger = audit_logger
        self.vessel_id = vessel_id
        self.approval_queue = ApprovalQueue(config.approval_queue_path)
        self._monitor_task: Optional[asyncio.Task[None]] = None
        self._stop_event = asyncio.Event()
        self._approval_callbacks: list[Callable[[ActionProposal], None]] = []

    async def start(self) -> None:
        """Start approval workflow monitoring."""
        if self._monitor_task and not self._monitor_task.done():
            return
        self._stop_event.clear()
        self._monitor_task = asyncio.create_task(
            self._monitor_loop(),
            name="janus-approval-monitor",
        )
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="approval_workflow.started",
                data={},
            )
        )

    async def stop(self) -> None:
        """Stop approval workflow monitoring."""
        if not self._monitor_task or self._monitor_task.done():
            return
        self._stop_event.set()
        if self._monitor_task:
            await self._monitor_task

    def register_approval_callback(
        self,
        callback: Callable[[ActionProposal], None],
    ) -> None:
        """Register callback to be invoked when proposal receives approval."""
        self._approval_callbacks.append(callback)

    async def submit_for_approval(self, proposal: ActionProposal) -> None:
        """Submit proposal for human approval."""
        # Validate proposal is in correct state
        if proposal.status != ProposalStatus.PROPOSED:
            raise ValueError(f"Proposal must be in PROPOSED state, got {proposal.status}")

        # Add to approval queue
        self.approval_queue.add_to_queue(proposal)

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="approval_workflow.submitted",
                data={
                    "proposal_id": proposal.proposal_id,
                    "action_type": proposal.action_type,
                    "risk_level": proposal.risk_level.value,
                },
            )
        )

        # Send notification if enabled
        if self.config.notification_enabled:
            await self._send_notification(proposal)

    async def _send_notification(self, proposal: ActionProposal) -> None:
        """Send notification to First Citizen about pending approval.

        In production, this would integrate with:
        - COMMS_HUB notification system
        - Email alerts
        - Telegram/Signal notifications
        - Dashboard UI updates
        """
        notification_data = {
            "proposal_id": proposal.proposal_id,
            "vessel_id": self.vessel_id,
            "timestamp": proposal.timestamp,
            "action_type": proposal.action_type,
            "risk_level": proposal.risk_level.value,
            "summary": proposal.rationale[:200],
            "review_command": f"ubos review {proposal.proposal_id}",
            "approve_command": f"ubos approve {proposal.proposal_id}",
            "reject_command": f"ubos reject {proposal.proposal_id}",
        }

        # If notification script provided, execute it
        if self.config.notification_script and self.config.notification_script.exists():
            try:
                import subprocess

                subprocess.run(
                    [str(self.config.notification_script), json.dumps(notification_data)],
                    check=False,
                    timeout=10,
                    capture_output=True,
                )
            except (subprocess.TimeoutExpired, OSError) as exc:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self.vessel_id,
                        event="approval_workflow.notification_failed",
                        data={"error": str(exc)},
                    )
                )

        # Log notification for monitoring systems to pick up
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="approval_workflow.notification",
                data=notification_data,
            )
        )

    async def _monitor_loop(self) -> None:
        """Monitor pending approvals and handle timeouts."""
        while not self._stop_event.is_set():
            await asyncio.sleep(60)  # Check every minute

            # Get all pending proposals
            pending = self.proposal_engine.list_pending_approvals()

            for proposal in pending:
                # Check if proposal has timed out
                proposal_time = datetime.fromisoformat(proposal.timestamp)
                age = datetime.now(timezone.utc) - proposal_time

                if age > self.config.approval_timeout:
                    await self._handle_timeout(proposal)

    async def _handle_timeout(self, proposal: ActionProposal) -> None:
        """Handle proposal that has timed out waiting for approval."""
        self.audit_logger.emit(
            LogEvent.create(
                level="warn",
                vessel=self.vessel_id,
                event="approval_workflow.timeout",
                data={
                    "proposal_id": proposal.proposal_id,
                    "action_type": proposal.action_type,
                    "age_hours": (
                        datetime.now(timezone.utc)
                        - datetime.fromisoformat(proposal.timestamp)
                    ).total_seconds()
                    / 3600,
                },
            )
        )

        if self.config.auto_reject_on_timeout:
            self.proposal_engine.reject_proposal(
                proposal.proposal_id,
                reason=f"Timeout: No approval received within {self.config.approval_timeout}",
            )

    def approve(
        self,
        proposal_id: str,
        approval_source: str = "first_citizen",
    ) -> ActionProposal:
        """Approve a proposal for execution.

        This method is called by the CLI/API when First Citizen approves.
        """
        proposal = self.proposal_engine.approve_proposal(proposal_id, approval_source)

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="approval_workflow.approved",
                data={
                    "proposal_id": proposal_id,
                    "approval_source": approval_source,
                },
            )
        )

        # Invoke registered callbacks
        for callback in self._approval_callbacks:
            try:
                callback(proposal)
            except Exception as exc:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="error",
                        vessel=self.vessel_id,
                        event="approval_workflow.callback_error",
                        data={"error": str(exc)},
                    )
                )

        return proposal

    def reject(
        self,
        proposal_id: str,
        reason: str,
    ) -> ActionProposal:
        """Reject a proposal with reason.

        This method is called by the CLI/API when First Citizen rejects.
        """
        proposal = self.proposal_engine.reject_proposal(proposal_id, reason)

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="approval_workflow.rejected",
                data={
                    "proposal_id": proposal_id,
                    "reason": reason,
                },
            )
        )

        return proposal

    def get_pending_proposals(self) -> list[ActionProposal]:
        """Get all proposals awaiting approval."""
        return self.proposal_engine.list_pending_approvals()

    def get_proposal_details(self, proposal_id: str) -> Optional[ActionProposal]:
        """Get detailed information about a specific proposal."""
        return self.proposal_engine.get_proposal(proposal_id)

    def format_proposal_for_review(self, proposal: ActionProposal) -> str:
        """Format proposal for human-readable review."""
        lines = [
            f"PROPOSAL: {proposal.proposal_id}",
            f"Timestamp: {proposal.timestamp}",
            f"Vessel: {proposal.vessel_id}",
            f"",
            f"ACTION TYPE: {proposal.action_type}",
            f"RISK LEVEL: {proposal.risk_level.value.upper()}",
            f"",
            f"MISSION CONTEXT:",
            f"  {proposal.mission_context}",
            f"",
            f"RATIONALE:",
            f"  {proposal.rationale}",
            f"",
            f"EXPECTED OUTCOME:",
            f"  {proposal.expected_outcome}",
            f"",
            f"RISK MITIGATION:",
            f"  {proposal.risk_mitigation}",
            f"",
            f"ROLLBACK PLAN:",
            f"  {proposal.rollback_plan}",
            f"",
            f"TOOL INVOCATION:",
            f"  Tool: {proposal.tool_name}",
            f"  Args: {' '.join(proposal.tool_args)}",
            f"  Kwargs: {json.dumps(proposal.tool_kwargs, indent=2)}",
            f"",
            f"COMMANDS:",
            f"  Review:  ubos review {proposal.proposal_id}",
            f"  Approve: ubos approve {proposal.proposal_id}",
            f"  Reject:  ubos reject {proposal.proposal_id} --reason 'Your reason here'",
        ]
        return "\n".join(lines)
