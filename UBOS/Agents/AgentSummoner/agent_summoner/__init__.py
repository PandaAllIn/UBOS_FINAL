"""
UBOS Blueprint: Agent Summoner - Constitutional Dynamic Agent Creation

Philosophy: Blueprint Thinking + Systems Over Willpower
Strategic Purpose: Create specialized agents that inherit UBOS constitutional principles from birth.
System Design: Template-based summoning with constitutional validation and lifecycle management.
Feedback Loops: All summoned agents report to registry; constitutional compliance monitored.
Environmental Support: Integrates with existing AgentRegistry, StrategicBlueprint, and StrategicPause.
"""

from .constitutional_summoner import ConstitutionalSummoner
from .agent_templates import AgentTemplateRegistry
from .lifecycle_manager import AgentLifecycleManager

__all__ = ["ConstitutionalSummoner", "AgentTemplateRegistry", "AgentLifecycleManager"]
