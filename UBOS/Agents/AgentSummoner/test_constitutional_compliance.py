#!/usr/bin/env python3
"""
Constitutional Compliance Test

Test the Agent Summoner for constitutional compliance with UBOS principles.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "AIPrimeAgent"))

from ai_prime_agent.blueprint.schema import StrategicBlueprint, validate_blueprint_dict
from ai_prime_agent.registry import AgentRegistry
from agent_summoner.constitutional_summoner import ConstitutionalSummoner
from agent_summoner.agent_templates import AgentTemplateRegistry


def test_constitutional_summoning():
    """Test that summoned agents inherit constitutional principles."""
    print("🧪 Testing Constitutional Summoning...")
    
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
            {"principleId": "UBOS-P-01", "statement": "Blueprint Thinking"},
            {"principleId": "UBOS-P-02", "statement": "Systems Over Willpower"}
        ],
        "activeGoals": [],
        "agentRegistry": [],
        "guardrails": {}
    }

    try:
        blueprint = validate_blueprint_dict(blueprint_data)
        print("✅ Blueprint validation successful")
    except Exception as e:
        print(f"❌ Blueprint validation failed: {e}")
        return False

    try:
        registry = AgentRegistry()
        print("✅ Agent Registry created")
    except Exception as e:
        print(f"❌ Agent Registry creation failed: {e}")
        return False

    try:
        template_registry = AgentTemplateRegistry()
        print("✅ Template Registry created")
    except Exception as e:
        print(f"❌ Template Registry creation failed: {e}")
        return False

    try:
        summoner = ConstitutionalSummoner(blueprint, registry, template_registry)
        print("✅ Constitutional Summoner created")
    except Exception as e:
        print(f"❌ Constitutional Summoner creation failed: {e}")
        return False

    try:
        # Summon a constitutional agent
        agent = summoner.summon_agent("eu_grant_specialist")
        print("✅ Agent summoned successfully")
        
        # Verify constitutional inheritance
        assert "constitutional" in agent.agent_type
        print("✅ Agent type includes 'constitutional'")
        
        assert "constitutional_framework" in agent.metadata
        print("✅ Agent metadata includes constitutional framework")
        
        assert agent.metadata["constitutional_framework"] == "UBOS_v1.0"
        print("✅ Constitutional framework version correct")
        
        assert "Blueprint Thinking" in agent.metadata["constitutional_principles"]
        print("✅ Agent inherits Blueprint Thinking principle")
        
        # Verify capabilities have constitutional extensions
        for cap in agent.capabilities:
            assert "constitutional_alignment" in cap.output_schema
            assert "ubos_principles" in cap.output_schema
        print("✅ Agent capabilities have constitutional extensions")
        
        print(f"🎉 Constitutional compliance test PASSED!")
        print(f"   Agent ID: {agent.agent_id}")
        print(f"   Agent Type: {agent.agent_type}")
        print(f"   Capabilities: {len(agent.capabilities)}")
        print(f"   Constitutional Principles: {len(agent.metadata['constitutional_principles'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent summoning or validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template_validation():
    """Test template constitutional validation."""
    print("\n🧪 Testing Template Constitutional Validation...")
    
    try:
        template_registry = AgentTemplateRegistry()
        
        # Test EU Grant Specialist template
        eu_template = template_registry.get_template("eu_grant_specialist")
        print("✅ EU Grant Specialist template retrieved")
        
        # Test Specification Agent template
        spec_template = template_registry.get_template("specification_agent")
        print("✅ Specification Agent template retrieved")
        
        # Test Research Specialist template
        research_template = template_registry.get_template("research_specialist")
        print("✅ Research Specialist template retrieved")
        
        print("🎉 Template validation test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Template validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting Constitutional Compliance Tests...")
    
    success = True
    
    # Test 1: Constitutional Summoning
    if not test_constitutional_summoning():
        success = False
    
    # Test 2: Template Validation
    if not test_template_validation():
        success = False
    
    if success:
        print("\n🎉 ALL CONSTITUTIONAL COMPLIANCE TESTS PASSED!")
        print("✅ Agent Summoner is constitutionally compliant")
        print("✅ Ready for integration with AI Prime Agent")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("❌ Agent Summoner needs fixes before integration")
        sys.exit(1)
