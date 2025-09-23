"""
UBOS Blueprint: AI Prime Orchestrator (Skeleton)

Philosophy: Blueprint Thinking + Strategic Starting Points
Strategic Purpose: Hold the Strategic Blueprint, the Agent Registry, and the
Communication Bus; provide a minimal surface to register adapters and stage
workflows while keeping agents independent.
System Design: Composition over coupling; inject registry and bus; load a
validated blueprint; expose small, clear methods that are easy to grow.
Feedback Loops: Ready hooks for Strategic Pause and Validation in later phases.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ai_prime_agent.blueprint.schema import StrategicBlueprint, load_blueprint
from ai_prime_agent.bus.inproc_bus import InProcBus, Handler
from ai_prime_agent.registry import AgentRegistry


@dataclass
class PrimeComponents:
    blueprint: StrategicBlueprint
    registry: AgentRegistry
    bus: InProcBus


class AIPrimeAgent:
    """
    UBOS Principle: Structure over control; smallest working orchestrator.
    Strategic Value: Central nervous system that coordinates without
    overreaching; each agent remains independent.
    System Role: Owns validated blueprint, registry, and bus.
    """

    def __init__(
        self,
        *,
        blueprint: StrategicBlueprint | None = None,
        blueprint_path: str | Path | None = None,
        registry: Optional[AgentRegistry] = None,
        bus: Optional[InProcBus] = None,
    ) -> None:
        if blueprint is None and blueprint_path is None:
            raise ValueError("Provide blueprint or blueprint_path")
        self._blueprint = blueprint or load_blueprint(Path(blueprint_path))  # type: ignore[arg-type]
        self._registry = registry or AgentRegistry()
        self._bus = bus or InProcBus(self._registry)

    # --------------------------------------------------------------
    @property
    def components(self) -> PrimeComponents:
        return PrimeComponents(self._blueprint, self._registry, self._bus)

    # --------------------------------------------------------------
    def register_adapter(self, *, agent_id: str, task: str, handler: Handler) -> None:
        """
        UBOS Principle: Strategic Starting Points (one handler at a time)
        Register a handler for a specific (agent_id, task) pair on the bus.
        """

        self._bus.register_handler(destination_agent_id=agent_id, task=task, handler=handler)

    # --------------------------------------------------------------
    def run_workflow(self, *, name: str, **kwargs) -> dict:
        """
        Placeholder for workflow coordination. For MVP, this simply confirms
        the blueprint is loaded and returns a stub plan reflecting inputs.

        This is intentionally small; Phase 2 introduces the Research & Synthesize
        workflow built on top of the bus.
        """

        _ = name  # unused in MVP
        return {
            "status": "READY",
            "blueprint_mission": self._blueprint.mission_statement,
            "registered_agents": [a.agent_id for a in self._registry.list_agents()],
        }


__all__ = ["AIPrimeAgent", "PrimeComponents"]

