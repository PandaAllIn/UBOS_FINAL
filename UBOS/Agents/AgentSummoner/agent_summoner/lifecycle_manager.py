"""
UBOS Blueprint: Agent Lifecycle Manager

Philosophy: Systems Over Willpower + Strategic Pause
Strategic Purpose: Manage summoned agent lifecycles with constitutional oversight.
System Design: Lifecycle tracking with constitutional metadata and automated cleanup.
Feedback Loops: Agent status monitoring enables early detection of constitutional drift.
Environmental Support: Integrates with existing AgentRegistry and AgentStatus patterns.
"""

from typing import Dict, List, Set
from datetime import datetime, timezone
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from ai_prime_agent.registry import AgentRegistry, AgentStatus


class AgentLifecycleManager:
    """Constitutional lifecycle management for summoned agents."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.tracked_agents: Set[str] = set()
        self.agent_birth_times: Dict[str, str] = {}

    def track_agent(self, agent_id: str):
        """Begin constitutional tracking of summoned agent."""
        self.tracked_agents.add(agent_id)
        self.agent_birth_times[agent_id] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def retire_agent(self, agent_id: str, reason: str = "task_completed"):
        """Constitutionally retire a summoned agent."""
        if agent_id in self.tracked_agents:
            # Update constitutional metadata
            agent = self.registry.get(agent_id)
            agent.metadata["retired_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            agent.metadata["retirement_reason"] = reason
            agent.status = AgentStatus.INACTIVE

            # Remove from tracking
            self.tracked_agents.remove(agent_id)

            # Preserve knowledge for constitutional learning
            self._preserve_agent_knowledge(agent_id)

    def _preserve_agent_knowledge(self, agent_id: str):
        """Preserve summoned agent's knowledge for constitutional evolution."""
        # This would integrate with Master Librarian for knowledge preservation
        pass

    def cleanup_stale_agents(self, max_age_hours: int = 24):
        """Constitutional cleanup of stale summoned agents."""
        now = datetime.now(timezone.utc)
        stale_agents = []

        for agent_id in list(self.tracked_agents):
            birth_time = datetime.strptime(self.agent_birth_times[agent_id], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            age_hours = (now - birth_time).total_seconds() / 3600

            if age_hours > max_age_hours:
                stale_agents.append(agent_id)

        for agent_id in stale_agents:
            self.retire_agent(agent_id, "stale_timeout")
