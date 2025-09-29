#!/usr/bin/env python3
"""
🏭 Agent Summoner Example
Demonstrates template-based agent creation with constitutional requirements
"""

import sys
from pathlib import Path

# Add UBOS path
ubos_path = Path(__file__).parent.parent / "UBOS/Agents/AgentSummoner"
sys.path.insert(0, str(ubos_path))

def agent_summoner_example():
    """Example of using Agent Summoner"""
    print("🏭 AGENT SUMMONER EXAMPLE")
    print("="*40)

    try:
        from agent_summoner.agent_templates import AgentTemplateRegistry

        # Create registry
        registry = AgentTemplateRegistry()
        print("✅ Agent Template Registry created")

        # List available templates
        templates = list(registry.templates.keys())
        print(f"\\n📋 Available Agent Templates ({len(templates)}):")
        for template_name in templates:
            template = registry.get_template(template_name)
            print(f"   🤖 {template_name}:")
            print(f"      Type: {template.agent_type}")
            print(f"      Description: {template.description[:80]}...")
            print(f"      Capabilities: {len(template.base_capabilities)}")
            print(f"      Constitutional requirements: {len(template.constitutional_requirements)}")
            print()

        # Show detailed example of specification agent
        print("📝 DETAILED EXAMPLE: Specification Agent Template")
        print("-" * 50)

        spec_template = registry.get_template("specification_agent")
        print(f"Name: {spec_template.name}")
        print(f"Type: {spec_template.agent_type}")
        print(f"Description: {spec_template.description}")
        print(f"\\nCapabilities:")
        for capability in spec_template.base_capabilities:
            print(f"   - {capability.name}: {capability.description}")

        print(f"\\nConstitutional Requirements:")
        for key, values in spec_template.constitutional_requirements.items():
            if isinstance(values, list):
                print(f"   {key}:")
                for value in values:
                    print(f"     • {value}")
            else:
                print(f"   {key}: {values}")

        print(f"\\nResource Limits:")
        for key, value in spec_template.resource_limits.items():
            print(f"   {key}: {value}")

        # Show EU Grant Specialist example
        print(f"\\n🇪🇺 DETAILED EXAMPLE: EU Grant Specialist Template")
        print("-" * 50)

        eu_template = registry.get_template("eu_grant_specialist")
        print(f"Name: {eu_template.name}")
        print(f"Type: {eu_template.agent_type}")
        print(f"Description: {eu_template.description}")
        print(f"\\nSpecialized Capabilities:")
        for capability in eu_template.base_capabilities:
            print(f"   - {capability.name}")
            print(f"     Description: {capability.description}")
            print(f"     Input: {list(capability.input_schema.keys())}")
            print(f"     Output: {list(capability.output_schema.keys())}")

        print(f"\\nConstitutional Alignment:")
        for key, values in eu_template.constitutional_requirements.items():
            print(f"   {key}: {values}")

        print("\\n🎊 Agent Summoner examples completed!")
        print("🏆 Template-based agent creation with constitutional requirements ready!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    agent_summoner_example()