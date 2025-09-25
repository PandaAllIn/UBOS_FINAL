"""
UBOS Blueprint: Constitutional Agent Summoner

Philosophy: Blueprint Thinking + Systems Over Willpower
Strategic Purpose: Create specialized agents that inherit UBOS constitutional principles from birth.
System Design: Template-based summoning with constitutional validation and lifecycle management.
Feedback Loops: All summoned agents report to registry; constitutional compliance monitored.
Environmental Support: Integrates with existing AgentRegistry, StrategicBlueprint, and StrategicPause.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from ai_prime_agent.blueprint.schema import StrategicBlueprint
from ai_prime_agent.registry import AgentRegistry, AgentRecord, AgentCapability, AgentStatus
from ai_prime_agent.pause import StrategicPause, PauseDecision
from ai_prime_agent.validation import BlueprintValidator

from .agent_templates import AgentTemplateRegistry, AgentTemplate
from .lifecycle_manager import AgentLifecycleManager
from .constitutional import ConstitutionalValidator


class ConstitutionalSummoner:
    """
    UBOS Principle: Create agents that embody constitutional principles from birth.
    Strategic Value: Dynamic capability expansion while maintaining constitutional alignment.
    """

    def __init__(self, 
                 blueprint: StrategicBlueprint,
                 registry: AgentRegistry,
                 template_registry: AgentTemplateRegistry):
        self.blueprint = blueprint
        self.registry = registry
        self.template_registry = template_registry
        self.lifecycle_manager = AgentLifecycleManager(registry)
        self.constitutional_validator = ConstitutionalValidator(blueprint)
        self.strategic_pause = StrategicPause(blueprint)

    def summon_agent(self, 
                     template_name: str,
                     agent_id: Optional[str] = None,
                     specialized_config: Optional[Dict[str, Any]] = None) -> AgentRecord:
        """
        UBOS Constitutional Process:
        1. Pre-summoning pause (constitutional analysis)
        2. Template retrieval and constitutional validation
        3. Agent creation with constitutional compliance
        4. Registry integration
        5. Post-summoning validation
        """

        # Step 1: Constitutional Pre-Summoning Pause
        pause_decision = self.strategic_pause.pre_delegation(
            query=f"Summon {template_name} agent",
            objectives=[f"Create constitutionally compliant {template_name}"]
        )

        if pause_decision.status == "escalate":
            raise ValueError(f"Constitutional escalation: {pause_decision.reasons}")

        # Step 2: Retrieve and Validate Template
        template = self.template_registry.get_template(template_name)
        if not self.constitutional_validator.validate_template(template):
            raise ValueError(f"Template {template_name} fails constitutional validation")

        # Step 3: Create Agent with Constitutional Inheritance
        agent_record = self._create_constitutional_agent(
            template=template,
            agent_id=agent_id,
            config=specialized_config or {}
        )

        # Step 4: Register with Constitutional Metadata
        self.registry.register(agent_record)

        # Step 5: Initialize Lifecycle Management
        self.lifecycle_manager.track_agent(agent_record.agent_id)

        return agent_record

    def _create_constitutional_agent(self, 
                                     template: AgentTemplate,
                                     agent_id: Optional[str],
                                     config: Dict[str, Any]) -> AgentRecord:
        """Create agent with constitutional DNA embedded."""

        final_id = agent_id or f"A-sum-{uuid.uuid4().hex[:8]}"

        # Constitutional capabilities inherit UBOS principles
        constitutional_capabilities = []
        for cap in template.base_capabilities:
            constitutional_cap = AgentCapability(
                name=cap.name,
                version=cap.version,
                description=f"Constitutional: {cap.description}",
                input_schema=cap.input_schema,
                output_schema={
                    **cap.output_schema,
                    "constitutional_alignment": {"type": "object"},
                    "ubos_principles": {"type": "array"}
                }
            )
            constitutional_capabilities.append(constitutional_cap)

        # Constitutional metadata
        constitutional_metadata = {
            "constitutional_framework": "UBOS_v1.0",
            "summoned_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "template_used": template.name,
            "constitutional_principles": [p.statement for p in self.blueprint.core_principles],
            "summoner_id": "constitutional_summoner",
            "lifecycle_managed": True,
            "specialized_config": config
        }

        return AgentRecord.create(
            agent_id=final_id,
            agent_type=f"constitutional_{template.agent_type}",
            capabilities=constitutional_capabilities,
            status=AgentStatus.IDLE,
            metadata=constitutional_metadata
        )
