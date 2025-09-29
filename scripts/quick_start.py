#!/usr/bin/env python3
"""
🚀 UBOS Quick Start Script
Quickly test all enhanced agents with a single command
"""

import os
import sys
from pathlib import Path

# Add UBOS paths
ubos_path = Path(__file__).parent.parent / "UBOS"
sys.path.insert(0, str(ubos_path / "Agents/ResearchAgent"))
sys.path.insert(0, str(ubos_path / "Agents/AgentSummoner"))
sys.path.insert(0, str(ubos_path / "Agents/KnowledgeAgent/MasterLibrarianAgent"))
sys.path.insert(0, str(ubos_path / "Agents/AIPrimeAgent"))

def check_api_keys():
    """Check if API keys are configured"""
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not perplexity_key or not gemini_key:
        print("⚠️ API KEYS NOT CONFIGURED")
        print("Please set your API keys:")
        print("export PERPLEXITY_API_KEY='your_key'")
        print("export GEMINI_API_KEY='your_key'")
        return False

    print("✅ API keys configured")
    return True

def quick_test_all_agents():
    """Quick test of all enhanced agents"""
    print("🚀 UBOS ENHANCED AGENTS QUICK START")
    print("="*50)

    if not check_api_keys():
        return False

    results = {}

    # Test Enhanced Research Agent
    print("\\n🔬 Testing Enhanced Research Agent...")
    try:
        from enhanced_research_agent import EnhancedResearchAgent

        agent = EnhancedResearchAgent()
        result = agent.research_with_constitutional_analysis(
            "Constitutional AI principles for multi-agent systems", "quick"
        )

        content_length = len(result.get("content", ""))
        has_analysis = bool(result.get("constitutional_analysis"))

        print(f"   ✅ Content: {content_length} chars")
        print(f"   ✅ Constitutional analysis: {has_analysis}")
        results["research_agent"] = True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        results["research_agent"] = False

    # Test Agent Summoner
    print("\\n🏭 Testing Agent Summoner...")
    try:
        from agent_summoner.agent_templates import AgentTemplateRegistry

        registry = AgentTemplateRegistry()
        templates = list(registry.templates.keys())

        print(f"   ✅ Available templates: {len(templates)}")
        print(f"   ✅ Templates: {', '.join(templates)}")
        results["agent_summoner"] = True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        results["agent_summoner"] = False

    # Test Master Librarian
    print("\\n📚 Testing Master Librarian...")
    try:
        from master_librarian.llm.gemini import GeminiClient
        from load_ubos_knowledge import SimpleKnowledgeGraph

        # Test Gemini
        gemini = GeminiClient()
        gemini_available = gemini.available()

        # Test knowledge
        kg = SimpleKnowledgeGraph()
        concepts = len(kg.concepts)

        print(f"   ✅ Gemini available: {gemini_available}")
        print(f"   ✅ UBOS concepts: {concepts}")
        results["master_librarian"] = gemini_available and concepts > 0

    except Exception as e:
        print(f"   ❌ Error: {e}")
        results["master_librarian"] = False

    # Summary
    working = sum(results.values())
    total = len(results)

    print(f"\\n📊 QUICK START RESULTS:")
    print(f"   Working agents: {working}/{total}")
    print(f"   Success rate: {working/total:.1%}")

    if working == total:
        print("\\n🎉 ALL AGENTS WORKING! Your UBOS system is ready!")
        print("🏆 System Status: 100% OPERATIONAL")
    elif working >= total * 0.8:
        print("\\n🟢 Most agents working! System mostly operational")
    else:
        print("\\n🟡 Some agents need configuration")

    return working == total

if __name__ == "__main__":
    success = quick_test_all_agents()
    sys.exit(0 if success else 1)