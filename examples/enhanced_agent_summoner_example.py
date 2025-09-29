#!/usr/bin/env python3
"""
🧠 Enhanced Constitutional Agent Summoner Example
Demonstrates the new hybrid thinking + template system
"""

import os
import sys
import asyncio
from pathlib import Path

# Add UBOS path
ubos_path = Path(__file__).parent.parent / "UBOS/Agents/AgentSummoner"
sys.path.insert(0, str(ubos_path))

async def enhanced_summoner_example():
    """Example of using Enhanced Constitutional Agent Summoner"""
    print("🧠 ENHANCED CONSTITUTIONAL AGENT SUMMONER EXAMPLE")
    print("=" * 60)

    # Check API keys
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️ GEMINI_API_KEY not set - thinking mode will be disabled")
        print("   System will fall back to template mode")

    try:
        from agent_summoner.enhanced_constitutional_summoner import EnhancedConstitutionalSummoner

        # Create enhanced summoner
        summoner = EnhancedConstitutionalSummoner()
        print(f"✅ Enhanced Constitutional Summoner created")
        print(f"🧠 Thinking enabled: {summoner.thinking_enabled}")
        print(f"🎯 Default mode: {summoner.default_mode}")

        # Test cases for different modes
        test_cases = [
            {
                "description": "Research constitutional AI governance frameworks for enterprise systems",
                "mode": "auto",
                "expected": "Should use research capabilities"
            },
            {
                "description": "Create an EU funding dashboard with AI-enhanced application assistance",
                "mode": "hybrid",
                "expected": "Should detect EU funding specialization"
            },
            {
                "description": "Generate constitutionally compliant Python code for data processing",
                "mode": "thinking",
                "expected": "Should create implementation-focused agent"
            },
            {
                "description": "Build a complex multi-agent orchestration system with constitutional oversight",
                "mode": "auto",
                "expected": "Should recognize architectural complexity"
            }
        ]

        print(f"\n📋 Running {len(test_cases)} test cases...")

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*50}")
            print(f"🧪 Test Case {i}: {test_case['mode'].upper()} mode")
            print(f"📝 Task: {test_case['description']}")
            print(f"🎯 Expected: {test_case['expected']}")
            print("-" * 50)

            try:
                # Test the summoning
                result = await summoner.summon_constitutional_agent(
                    task_description=test_case['description'],
                    mode=test_case['mode']
                )

                if result:
                    print(f"✅ Agent summoned successfully!")
                    print(f"🤖 Agent ID: {result.agent_id}")
                    print(f"🏛️ Constitutional Status: {result.status}")

                    # Show capabilities if available
                    if hasattr(result, 'capabilities') and result.capabilities:
                        print(f"⚡ Capabilities: {len(result.capabilities)}")
                        for cap in result.capabilities[:3]:  # Show first 3
                            print(f"   - {cap.name}: {cap.description}")
                        if len(result.capabilities) > 3:
                            print(f"   ... and {len(result.capabilities) - 3} more")
                else:
                    print("❌ No agent returned")

            except Exception as e:
                print(f"⚠️ Test failed: {e}")

        # Test quick convenience methods
        print(f"\n{'='*50}")
        print("🚀 Testing Convenience Methods")
        print("-" * 50)

        try:
            # Quick summon
            print("\n1️⃣ Quick summon test:")
            quick_result = await summoner.quick_summon("Analyze UBOS constitutional principles")
            if quick_result:
                print(f"   ✅ Quick summon successful: {quick_result.agent_id}")

            # Template summon
            print("\n2️⃣ Template summon test:")
            template_result = await summoner.template_summon("research_specialist", "Research AI trends")
            if template_result:
                print(f"   ✅ Template summon successful: {template_result.agent_id}")

            # Thinking summon (if available)
            if summoner.thinking_enabled:
                print("\n3️⃣ Thinking summon test:")
                thinking_result = await summoner.thinking_summon("Create a novel constitutional AI framework")
                if thinking_result:
                    print(f"   ✅ Thinking summon successful: {thinking_result.agent_id}")
            else:
                print("\n3️⃣ Thinking summon: Skipped (Gemini not available)")

        except Exception as e:
            print(f"⚠️ Convenience method test failed: {e}")

        # Show system capabilities
        print(f"\n{'='*50}")
        print("📊 SYSTEM CAPABILITIES SUMMARY")
        print("-" * 50)

        print(f"🏛️ Constitutional Modes Available:")
        print(f"   - Template Mode: ✅ (Backward compatible)")
        print(f"   - Thinking Mode: {'✅' if summoner.thinking_enabled else '❌'} (Gemini 2.5)")
        print(f"   - Hybrid Mode: ✅ (Intelligent selection)")
        print(f"   - Auto Mode: ✅ (Default smart mode)")

        print(f"\n🤖 Agent Knowledge Base:")
        for agent_type, info in summoner.agent_knowledge_base.items():
            capabilities = info.get('capabilities', [])
            cost = info.get('cost', 0)
            print(f"   - {agent_type}: {len(capabilities)} capabilities, ${cost:.3f}")

        print(f"\n🏆 Enhanced Features:")
        print(f"   - Constitutional task analysis")
        print(f"   - Intelligent agent recommendations")
        print(f"   - Dynamic agent creation capabilities")
        print(f"   - Hybrid template + thinking approach")
        print(f"   - EUFM integration ready")
        print(f"   - Cost-aware agent selection")

        print("\n🎊 Enhanced Constitutional Agent Summoner examples completed!")
        print("🏆 Hybrid intelligence + constitutional compliance = Next-level agent creation!")

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Make sure enhanced_constitutional_summoner.py is in the correct path")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(enhanced_summoner_example())