"""
UBOS Blueprint: Constitutional Summoner Tests

Philosophy: Test-First + Constitutional Validation
Strategic Purpose: Validate constitutional agent summoning functionality.
System Design: Test framework following existing test patterns.
Feedback Loops: Test results validate constitutional compliance.
Environmental Support: Integrates with existing test infrastructure.
"""

import pytest
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from ai_prime_agent.blueprint.schema import StrategicBlueprint, validate_blueprint_dict
from ai_prime_agent.registry import AgentRegistry
from agent_summoner.constitutional_summoner import ConstitutionalSummoner
from agent_summoner.agent_templates import AgentTemplateRegistry


def test_constitutional_summoning():
    """Test that summoned agents inherit constitutional principles."""

    # Create minimal constitutional blueprint
    blueprint_data = {
        "blueprint_metadata": {
            "schema_version": "1.0",
            "document_version": "1.0.0",
            "last_updated_utc": "2025-09-25T10:00:00Z",
            "review_cadence_days": 7
        },
        "missionStatement": "Constitutional AI governance",
        "corePrinciples": [
            {"principleId": "UBOS-P-01", "statement": "Blueprint Thinking"}
        ],
        "activeGoals": [],
        "agentRegistry": [],
        "guardrails": {}
    }

    blueprint = validate_blueprint_dict(blueprint_data)
    registry = AgentRegistry()
    template_registry = AgentTemplateRegistry()

    summoner = ConstitutionalSummoner(blueprint, registry, template_registry)

    # Summon a constitutional agent
    agent = summoner.summon_agent("eu_grant_specialist")

    # Verify constitutional inheritance
    assert "constitutional" in agent.agent_type
    assert "constitutional_framework" in agent.metadata
    assert agent.metadata["constitutional_framework"] == "UBOS_v1.0"
    assert "Blueprint Thinking" in agent.metadata["constitutional_principles"]

    # Verify capabilities have constitutional extensions
    for cap in agent.capabilities:
        assert "constitutional_alignment" in cap.output_schema
        assert "ubos_principles" in cap.output_schema
