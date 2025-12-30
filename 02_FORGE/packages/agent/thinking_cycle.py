"""Periodic thinking cycle for autonomous reasoning.

This module implements the autonomous thinking cycle where Janus-in-Balaur:
1. Reviews current state and mission objectives
2. Analyzes available information and recent actions
3. Proposes new actions to advance strategic goals
4. Respects operational mode constraints (Alpha/Beta/Omega)
"""
from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from .llm_client import LLMClient, OracleBridge
from .logging_utils import AuditLogger, LogEvent
from .proposal_engine import ActionProposal, ProposalEngine, RiskLevel


class OperationalMode:
    """Operational mode definitions per Autonomous Vessel Protocol."""

    ALPHA = "alpha"  # Propose-only, requires approval
    BETA = "beta"  # Supervised autonomy with playbooks
    OMEGA = "omega"  # Full autonomy


@dataclass(slots=True)
class ThinkingCycleConfig:
    """Configuration for autonomous thinking cycles."""

    cycle_interval: timedelta = timedelta(hours=1)
    constitutional_memory_path: Optional[Path] = None
    mission_objectives_path: Optional[Path] = None
    mission_file_path: Optional[Path] = None
    operational_mode: str = OperationalMode.ALPHA
    playbook_registry_path: Optional[Path] = None
    enable_autonomous_proposals: bool = True
    max_proposals_per_cycle: int = 3
    study_materials_max_chars: int = 6000


@dataclass(slots=True)
class Playbook:
    """Pre-approved action playbook for Mode Beta autonomous execution."""

    playbook_id: str
    name: str
    description: str
    trigger_conditions: dict[str, Any]
    action_sequence: list[dict[str, Any]]
    approved_by: str
    approved_at: str


class PlaybookRegistry:
    """Registry of approved playbooks for Mode Beta operation."""

    def __init__(self, registry_path: Optional[Path] = None) -> None:
        self.registry_path = registry_path
        self._playbooks: dict[str, Playbook] = {}
        if registry_path and registry_path.exists():
            self._load_playbooks()

    def _load_playbooks(self) -> None:
        """Load approved playbooks from registry file."""
        if not self.registry_path or not self.registry_path.exists():
            return

        with self.registry_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data.get("playbooks", []):
                playbook = Playbook(
                    playbook_id=item["playbook_id"],
                    name=item["name"],
                    description=item["description"],
                    trigger_conditions=item["trigger_conditions"],
                    action_sequence=item["action_sequence"],
                    approved_by=item["approved_by"],
                    approved_at=item["approved_at"],
                )
                self._playbooks[playbook.playbook_id] = playbook

    def get_playbook(self, playbook_id: str) -> Optional[Playbook]:
        """Retrieve playbook by ID."""
        return self._playbooks.get(playbook_id)

    def match_playbook(self, context: dict[str, Any]) -> Optional[Playbook]:
        """Find playbook matching current context conditions."""
        for playbook in self._playbooks.values():
            if self._matches_conditions(playbook.trigger_conditions, context):
                return playbook
        return None

    def _matches_conditions(
        self,
        conditions: dict[str, Any],
        context: dict[str, Any],
    ) -> bool:
        """Check if context matches playbook trigger conditions."""
        # Simple key-value matching - can be enhanced with more sophisticated rules
        for key, expected_value in conditions.items():
            if key not in context:
                return False
            if context[key] != expected_value:
                return False
        return True

    def list_playbooks(self) -> list[Playbook]:
        """Get all registered playbooks."""
        return list(self._playbooks.values())


class ThinkingCycle:
    """Autonomous reasoning and proposal generation cycle."""

    def __init__(
        self,
        config: ThinkingCycleConfig,
        proposal_engine: ProposalEngine,
        llm_client: LLMClient,
        audit_logger: AuditLogger,
        vessel_id: str = "janus-in-balaur",
        oracle_bridge: Optional[OracleBridge] = None,
    ) -> None:
        self.config = config
        self.proposal_engine = proposal_engine
        self.llm_client = llm_client
        self.audit_logger = audit_logger
        self.vessel_id = vessel_id
        self.oracle_bridge = oracle_bridge
        self.playbook_registry = PlaybookRegistry(config.playbook_registry_path)
        self._task: Optional[asyncio.Task[None]] = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        """Start the thinking cycle background task."""
        if self._task and not self._task.done():
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._thinking_loop(), name="janus-thinking-cycle")
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.started",
                data={"mode": self.config.operational_mode, "interval": self.config.cycle_interval.total_seconds()},
            )
        )

    async def stop(self) -> None:
        """Stop the thinking cycle."""
        if not self._task or self._task.done():
            return
        self._stop_event.set()
        if self._task:
            await self._task

    async def _thinking_loop(self) -> None:
        """Main thinking cycle loop."""
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.loop_started",
                data={},
            )
        )
        while not self._stop_event.is_set():
            try:
                await self._execute_thinking_cycle()
            except Exception as exc:
                self.audit_logger.emit(
                    LogEvent.create(
                        level="error",
                        vessel=self.vessel_id,
                        event="thinking_cycle.error",
                        data={"error": str(exc)},
                    )
                )

            # Wait for next cycle
            self.audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self.vessel_id,
                    event="thinking_cycle.waiting_for_next_cycle",
                    data={"interval": self.config.cycle_interval.total_seconds()},
                )
            )
            await asyncio.sleep(self.config.cycle_interval.total_seconds())
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.loop_stopped",
                data={},
            )
        )

    async def _execute_thinking_cycle(self) -> None:
        """Execute one thinking cycle iteration."""
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.begin",
                data={"timestamp": datetime.now(timezone.utc).isoformat()},
            )
        )

        # 1. Gather current state and context
        context = await self._gather_context()

        # 2. Check operational mode and decide action
        if self.config.operational_mode == OperationalMode.ALPHA:
            self.audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self.vessel_id,
                    event="thinking_cycle.alpha_mode",
                    data={},
                )
            )
            # Mode Alpha: Generate proposals only
            await self._generate_proposals(context)

        elif self.config.operational_mode == OperationalMode.BETA:
            self.audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self.vessel_id,
                    event="thinking_cycle.beta_mode",
                    data={},
                )
            )
            # Mode Beta: Try to match playbooks, else generate proposal
            playbook = self.playbook_registry.match_playbook(context)
            if playbook:
                await self._execute_playbook(playbook, context)
            else:
                await self._generate_proposals(context)

        elif self.config.operational_mode == OperationalMode.OMEGA:
            # Mode Omega: Full autonomy (future implementation)
            self.audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self.vessel_id,
                    event="thinking_cycle.omega_mode",
                    data={"message": "Mode Omega not yet implemented"},
                )
            )

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.complete",
                data={"timestamp": datetime.now(timezone.utc).isoformat()},
            )
        )

    async def _gather_context(self) -> dict[str, Any]:
        """Gather current state and mission context.

        This method should be extended to integrate with:
        - Mission objectives file
        - Recent action results
        - System state
        - External intelligence (Oracle Trinity, etc.)
        """
        context: dict[str, Any] = {
            "vessel_id": self.vessel_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operational_mode": self.config.operational_mode,
        }

        # Load mission objectives if available
        if self.config.mission_objectives_path and self.config.mission_objectives_path.exists():
            try:
                with self.config.mission_objectives_path.open("r", encoding="utf-8") as f:
                    objectives = json.load(f)
                    context["mission_objectives"] = objectives
            except (json.JSONDecodeError, IOError):
                pass

        # Load full mission (YAML or JSON) + study materials if available
        if self.config.mission_file_path and self.config.mission_file_path.exists():
            try:
                from .mission_loader import load_mission

                mission = load_mission(self.config.mission_file_path, max_chars=self.config.study_materials_max_chars)
                context["mission"] = mission
                # Provide a concise study brief for the LLM
                brief_lines: list[str] = []
                if mission.get("mission_name"):
                    brief_lines.append(f"Mission: {mission['mission_name']}")
                if mission.get("objectives"):
                    brief_lines.append("Objectives: " + "; ".join(mission["objectives"]))
                if mission.get("materials"):
                    brief_lines.append(f"Study materials: {len(mission['materials'])} sources loaded")
                context["mission_brief"] = " | ".join(brief_lines)
            except Exception:
                # Non-fatal: continue with lighter context
                pass

        # Check recent proposal history
        recent_proposals = self.proposal_engine.list_pending_approvals()
        context["pending_approvals"] = len(recent_proposals)
        context["approval_rate"] = self.proposal_engine.get_approval_rate()

        return context

    async def _generate_proposals(self, context: dict[str, Any]) -> None:
        """Generate autonomous action proposals based on context."""
        if not self.config.enable_autonomous_proposals:
            return

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.proposal_generation.start",
                data={},
            )
        )

        try:
            # Convert context to a string for the LLM
            context_str = json.dumps(context, indent=2)
            
            # Use the LLM to generate a structured proposal
            proposal_data = await self.llm_client.generate_proposal_json(context_str)
            requested_tool = str(proposal_data.get("tool_name", "") or "").strip()
            if requested_tool and not self.proposal_engine.is_known_tool(requested_tool):
                available = self.proposal_engine.list_known_tools()
                self.audit_logger.emit(
                    LogEvent.create(
                        level="warn",
                        vessel=self.vessel_id,
                        event="thinking_cycle.unknown_tool",
                        data={
                            "requested_tool": requested_tool,
                            "available_tools": available,
                        },
                    )
                )
                return
            if not requested_tool:
                requested_tool = "shell"

            # Create a formal proposal from the LLM's output
            tool_args = proposal_data.get("tool_args", [])
            tool_kwargs = proposal_data.get("tool_kwargs", {}) or {}
            enforce_novelty = True

            if requested_tool == "node_generator":
                tool_args = self._build_node_generator_args(context, proposal_data)
                enforce_novelty = False

            proposal = self.proposal_engine.create_proposal(
                mission_context=(
                    context.get("mission_objectives", {}).get("current")
                    or (context.get("mission", {}) or {}).get("mission_id")
                    or "Default Mission"
                ),
                action_type=proposal_data.get("action_type", "unknown"),
                rationale=proposal_data.get("rationale", "No rationale provided."),
                expected_outcome=proposal_data.get("expected_outcome", "No outcome provided."),
                risk_level=RiskLevel(proposal_data.get("risk_level", "medium")),
                risk_mitigation="Standard operational checks.",
                rollback_plan="Manual rollback by operator.",
                tool_name=requested_tool,
                tool_args=tool_args,
                tool_kwargs=tool_kwargs if isinstance(tool_kwargs, dict) else {},
                enforce_novelty=enforce_novelty,
            )

            self.audit_logger.emit(
                LogEvent.create(
                    level="info",
                    vessel=self.vessel_id,
                    event="thinking_cycle.proposal_generation.success",
                    data={"proposal_id": proposal.proposal_id, "action": proposal.action_type},
                )
            )

        except Exception as e:
            self.audit_logger.emit(
                LogEvent.create(
                    level="error",
                    vessel=self.vessel_id,
                    event="thinking_cycle.proposal_generation.failed",
                    data={"error": str(e)},
                )
            )

    async def _execute_playbook(self, playbook: Playbook, context: dict[str, Any]) -> None:
        """Execute a pre-approved playbook autonomously (Mode Beta only)."""
        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.playbook_matched",
                data={
                    "playbook_id": playbook.playbook_id,
                    "playbook_name": playbook.name,
                },
            )
        )

        # Create proposal for playbook execution
        proposal = self.proposal_engine.create_proposal(
            mission_context=f"Playbook execution: {playbook.name}",
            action_type="playbook_execution",
            rationale=f"Automated playbook: {playbook.description}",
            expected_outcome=f"Execute pre-approved playbook {playbook.playbook_id}",
            risk_level=RiskLevel.LOW,  # Playbooks are pre-approved as low-risk
            risk_mitigation="Playbook approved and validated",
            rollback_plan="Standard playbook rollback procedure",
            tool_name="shell",  # Placeholder - would use actual playbook tools
            tool_args=[],
            tool_kwargs={},
            metadata={
                "playbook_id": playbook.playbook_id,
                "playbook_name": playbook.name,
                "trigger_context": context,
            },
        )

        # Auto-approve playbook proposals in Mode Beta
        self.proposal_engine.approve_proposal(
            proposal.proposal_id,
            approval_source="playbook_registry",
        )

        self.audit_logger.emit(
            LogEvent.create(
                level="info",
                vessel=self.vessel_id,
                event="thinking_cycle.playbook_approved",
                data={"proposal_id": proposal.proposal_id},
            )
        )

    def set_operational_mode(self, mode: str) -> None:
        """Change operational mode (requires proper authorization in production)."""
        if mode not in (OperationalMode.ALPHA, OperationalMode.BETA, OperationalMode.OMEGA):
            raise ValueError(f"Invalid operational mode: {mode}")

        old_mode = self.config.operational_mode
        self.config.operational_mode = mode

        self.audit_logger.emit(
            LogEvent.create(
                level="warn",
                vessel=self.vessel_id,
                event="thinking_cycle.mode_change",
                data={"old_mode": old_mode, "new_mode": mode},
            )
        )

    def trigger_immediate_cycle(self) -> None:
        """Trigger an immediate thinking cycle (for testing/debugging)."""
        if not self._task or self._task.done():
            raise RuntimeError("Thinking cycle not running")

        # Create a new task that executes immediately
        asyncio.create_task(self._execute_thinking_cycle(), name="janus-immediate-cycle")

    def _build_node_generator_args(self, context: dict[str, Any], proposal_data: dict[str, Any]) -> list[str]:
        """Canonicalise node generator arguments for the autonomous mission."""
        mission_info = context.get("mission_objectives", {}).get("current") or context.get("mission", {})
        deliverable = mission_info.get("deliverable") if isinstance(mission_info, dict) else {}

        mission_id = ""
        mission_name = ""
        if isinstance(mission_info, dict):
            mission_id = str(mission_info.get("mission_id") or mission_info.get("mission") or "").strip()
            mission_name = str(mission_info.get("mission_name") or "").strip()
        mission_id = mission_id or str(proposal_data.get("mission_id") or "STUDY-UNKNOWN")
        mission_name = mission_name or str(proposal_data.get("mission_name") or "Steampunk Constitutional Synthesis")

        output_dir = ""
        if isinstance(deliverable, dict):
            output_dir = str(deliverable.get("location") or "").strip()
        output_dir = output_dir or "/srv/janus/03_OPERATIONS/vessels/balaur/workspace/philosophy_generated/beta/"

        target_min, target_max = self._extract_target_range(
            deliverable.get("required_count") if isinstance(deliverable, dict) else None
        )

        raw_keywords = proposal_data.get("keywords")
        if isinstance(raw_keywords, str):
            keyword_list = [part.strip() for part in raw_keywords.split(",") if part.strip()]
        elif isinstance(raw_keywords, (list, tuple)):
            keyword_list = [str(part).strip() for part in raw_keywords if str(part).strip()]
        else:
            keyword_list = []
        if not keyword_list:
            keyword_list = ["steampunk", "governor", "relief", "autonomy"]

        args = [
            "--mission",
            mission_id,
            "--theme",
            mission_name,
            "--books-root",
            "/srv/janus/00_CONSTITUTION/principles/philosophy_books",
            "--output-dir",
            output_dir,
            "--target-min",
            str(target_min),
            "--target-max",
            str(target_max),
            "--keywords",
            ",".join(keyword_list),
            "--json",
        ]
        return args

    @staticmethod
    def _extract_target_range(required: Any) -> tuple[int, int]:
        if isinstance(required, (list, tuple)) and len(required) >= 2:
            try:
                min_val = int(required[0])
                max_val = int(required[1])
                return (min_val, max(min_val, max_val))
            except (TypeError, ValueError):
                pass

        numbers = []
        if required is not None:
            numbers = [int(match) for match in re.findall(r"\d+", str(required))]
        if len(numbers) >= 2:
            return (numbers[0], numbers[1])
        if len(numbers) == 1:
            return (numbers[0], numbers[0])
        return (30, 50)
