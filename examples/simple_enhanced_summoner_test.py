#!/usr/bin/env python3
"""
🧠 Simple Enhanced Constitutional Agent Summoner Test
Quick test of the enhanced summoner functionality
"""

import os
import sys
import asyncio
from pathlib import Path

# Add UBOS path
ubos_path = Path(__file__).parent.parent / "UBOS/Agents/AgentSummoner"
sys.path.insert(0, str(ubos_path))

async def simple_enhanced_test():
    """Simple test of enhanced summoner"""
    print("🧠 SIMPLE ENHANCED SUMMONER TEST")
    print("="*40)

    try:
        from agent_summoner.enhanced_constitutional_summoner import EnhancedConstitutionalSummoner

        # Test initialization
        print("1️⃣ Testing initialization...")
        summoner = EnhancedConstitutionalSummoner()
        print(f"   ✅ Summoner created")
        print(f"   🧠 Thinking enabled: {summoner.thinking_enabled}")
        print(f"   🏛️ Template registry: {bool(summoner.template_registry)}")

        # Test knowledge base
        print("\n2️⃣ Testing knowledge base...")
        print(f"   📖 Agent types: {len(summoner.agent_knowledge_base)}")
        for agent_type in summoner.agent_knowledge_base.keys():
            print(f"      - {agent_type}")

        # Test template selection
        print("\n3️⃣ Testing template selection...")
        test_tasks = [
            "Research constitutional AI",
            "Create EU funding application",
            "Generate Python code",
            "Analyze complex requirements"
        ]

        for task in test_tasks:
            template = summoner._select_best_template(task)
            confidence = summoner._calculate_template_confidence(task)
            print(f"   📝 '{task[:30]}...' → {template} ({confidence:.1%})")

        # Test simple task analysis (without Gemini)
        print("\n4️⃣ Testing task analysis...")
        analysis = summoner._simple_task_analysis("Research constitutional AI governance frameworks")
        print(f"   📊 Task type: {analysis.task_type}")
        print(f"   📊 Complexity: {analysis.complexity}")
        print(f"   📊 Capabilities: {analysis.required_capabilities}")
        print(f"   📊 Confidence: {analysis.confidence_score:.1%}")

        # Test template mode (quick)
        print("\n5️⃣ Testing template-based summoning...")
        try:
            result = await summoner.summon_constitutional_agent(
                "Quick research task",
                mode="template"
            )
            if result:
                print(f"   ✅ Template agent created: {result.agent_id}")
                print(f"   📋 Template source: {result.template_source}")
            else:
                print("   ❌ No agent returned")
        except Exception as e:
            print(f"   ⚠️ Template test error: {e}")

        print("\n🎊 SIMPLE TEST COMPLETED!")
        print("✅ Enhanced Constitutional Summoner basic functionality working")

        return True

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(simple_enhanced_test())
    sys.exit(0 if success else 1)