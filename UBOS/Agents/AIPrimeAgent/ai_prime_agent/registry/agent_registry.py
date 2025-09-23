"""
UBOS Blueprint: Agent Registry System

Philosophy: Smallest Working Version + Systems Produce Current Results
Strategic Purpose: Maintain a living catalog of UBOS agents so delegation is automated and capability-aware.
System Design: In-memory registry with deterministic CRUD operations, capability queries, and heartbeat telemetry.
Feedback Loops: Heartbeats and status updates expose alignment issues early; registry snapshots support strategic pauses.
Environmental Support: Designed for lightweight bootstrapping, ready to back onto persistent storage in later iterations.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Iterable, List, Optional


class RegistryError(RuntimeError):
    """Raised when registry operations fail (duplicate IDs, missing agents, etc.)."""


class AgentStatus(str, Enum):
    """Operational state for a registered agent."""

    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    BUSY = "BUSY"
    ERROR = "ERROR"
    INACTIVE = "INACTIVE"


@dataclass
class AgentCapability:
    """Specification of an agent capability advertised to the Prime Agent."""

    name: str
    version: str
    description: str
    input_schema: Dict[str, object]
    output_schema: Dict[str, object]


@dataclass
class AgentTelemetry:
    """Rolling telemetry snapshot for an agent."""

    last_heartbeat_utc: str
    current_load_percentage: float = 0.0
    avg_response_time_ms: int = 0
    error_count: int = 0

    @classmethod
    def initial(cls) -> "AgentTelemetry":
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return cls(last_heartbeat_utc=now)

    def record_heartbeat(
        self,
        *,
        load_percentage: Optional[float] = None,
        response_time_ms: Optional[int] = None,
        error_count: Optional[int] = None,
    ) -> None:
        self.last_heartbeat_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if load_percentage is not None:
            self.current_load_percentage = max(0.0, min(100.0, float(load_percentage)))
        if response_time_ms is not None:
            self.avg_response_time_ms = max(0, int(response_time_ms))
        if error_count is not None:
            self.error_count = max(0, int(error_count))


@dataclass
class AgentRecord:
    """Single agent entry in the registry."""

    agent_id: str
    agent_type: str
    status: AgentStatus
    capabilities: List[AgentCapability]
    telemetry: AgentTelemetry
    metadata: Dict[str, object] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        agent_id: Optional[str],
        agent_type: str,
        capabilities: Iterable[AgentCapability],
        status: AgentStatus = AgentStatus.IDLE,
        metadata: Optional[Dict[str, object]] = None,
    ) -> "AgentRecord":
        record_id = agent_id or f"A-{uuid.uuid4().hex[:8]}"
        meta = metadata.copy() if metadata else {}
        if "registered_at_utc" not in meta:
            meta["registered_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return cls(
            agent_id=record_id,
            agent_type=agent_type,
            status=status,
            capabilities=list(capabilities),
            telemetry=AgentTelemetry.initial(),
            metadata=meta,
        )


class AgentRegistry:
    """In-memory registry that tracks agent capabilities and health."""

    def __init__(self) -> None:
        self._agents: Dict[str, AgentRecord] = {}

    # ------------------------------------------------------------------
    def register(self, record: AgentRecord) -> AgentRecord:
        if record.agent_id in self._agents:
            raise RegistryError(f"Agent {record.agent_id} already registered")
        self._agents[record.agent_id] = record
        return record

    # ------------------------------------------------------------------
    def update_capabilities(
        self,
        agent_id: str,
        capabilities: Iterable[AgentCapability],
    ) -> AgentRecord:
        agent = self._get(agent_id)
        agent.capabilities = list(capabilities)
        return agent

    # ------------------------------------------------------------------
    def set_status(self, agent_id: str, status: AgentStatus) -> AgentRecord:
        agent = self._get(agent_id)
        agent.status = status
        return agent

    # ------------------------------------------------------------------
    def record_heartbeat(
        self,
        agent_id: str,
        *,
        status: Optional[AgentStatus] = None,
        load_percentage: Optional[float] = None,
        response_time_ms: Optional[int] = None,
        error_count: Optional[int] = None,
    ) -> AgentRecord:
        agent = self._get(agent_id)
        if status is not None:
            agent.status = status
        agent.telemetry.record_heartbeat(
            load_percentage=load_percentage,
            response_time_ms=response_time_ms,
            error_count=error_count,
        )
        return agent

    # ------------------------------------------------------------------
    def deregister(self, agent_id: str) -> AgentRecord:
        agent = self._get(agent_id)
        del self._agents[agent_id]
        return agent

    # ------------------------------------------------------------------
    def get(self, agent_id: str) -> AgentRecord:
        return self._get(agent_id)

    # ------------------------------------------------------------------
    def list_agents(self) -> List[AgentRecord]:
        return list(self._agents.values())

    # ------------------------------------------------------------------
    def query_by_capability(
        self,
        capability_name: str,
        *,
        include_statuses: Optional[Iterable[AgentStatus]] = None,
    ) -> List[AgentRecord]:
        statuses = set(include_statuses) if include_statuses else None
        results: List[AgentRecord] = []
        for agent in self._agents.values():
            if statuses and agent.status not in statuses:
                continue
            if any(cap.name == capability_name for cap in agent.capabilities):
                results.append(agent)
        return results

    # ------------------------------------------------------------------
    def prune_stale(self, *, timeout_seconds: int) -> List[AgentRecord]:
        """Mark agents as ERROR if their heartbeat is older than timeout."""

        stale: List[AgentRecord] = []
        now = datetime.now(timezone.utc)
        for agent in self._agents.values():
            heartbeat = datetime.strptime(
                agent.telemetry.last_heartbeat_utc, "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=timezone.utc)
            delta = (now - heartbeat).total_seconds()
            if delta > timeout_seconds and agent.status not in {AgentStatus.INACTIVE, AgentStatus.ERROR}:
                agent.status = AgentStatus.ERROR
                stale.append(agent)
        return stale

    # ------------------------------------------------------------------
    def _get(self, agent_id: str) -> AgentRecord:
        try:
            return self._agents[agent_id]
        except KeyError as exc:  # pragma: no cover - defensive path
            raise RegistryError(f"Agent {agent_id} not found") from exc
