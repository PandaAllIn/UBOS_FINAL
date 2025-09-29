#!/usr/bin/env python3
"""
🔬 Enhanced Research Agent Example
Demonstrates constitutional AI research capabilities
"""

import os
import sys
from pathlib import Path

# Add UBOS path
ubos_path = Path(__file__).parent.parent / "UBOS/Agents/ResearchAgent"
sys.path.insert(0, str(ubos_path))

def research_example():
    """Example of using Enhanced Research Agent"""
    print("🔬 ENHANCED RESEARCH AGENT EXAMPLE")
    print("="*50)

    # Check API keys
    if not os.getenv("PERPLEXITY_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        print("❌ Please set PERPLEXITY_API_KEY and GEMINI_API_KEY environment variables")
        return

    try:
        from enhanced_research_agent import EnhancedResearchAgent

        # Create agent
        agent = EnhancedResearchAgent()
        print("✅ Enhanced Research Agent created")

        # Example queries
        queries = [
            "Constitutional AI governance frameworks for enterprise systems",
            "Multi-agent coordination patterns with constitutional oversight",
            "UBOS principles applied to AI system architecture"
        ]

        for i, query in enumerate(queries, 1):
            print(f"\\n📋 Query {i}: {query}")
            print("⏳ Researching with constitutional analysis...")

            # Perform research
            result = agent.research_with_constitutional_analysis(query, "medium")

            # Show results
            content = result.get("content", "")
            analysis = result.get("constitutional_analysis")
            citations = result.get("citations", [])

            print(f"\\n📊 Results:")
            print(f"   Content: {len(content)} characters")
            print(f"   Citations: {len(citations)}")
            print(f"   Constitutional analysis: {bool(analysis)}")

            if content:
                print(f"\\n📄 Content preview:")
                print(f"   {content[:300]}{'...' if len(content) > 300 else ''}")

            if analysis and hasattr(analysis, 'analysis'):
                print(f"\\n🏛️ Constitutional analysis preview:")
                analysis_text = str(analysis.analysis)[:200] + "..."
                print(f"   {analysis_text}")

            print("-" * 50)

        print("\\n🎊 Research examples completed!")
        print("🏆 Enhanced Research Agent with constitutional AI is fully operational!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    research_example()