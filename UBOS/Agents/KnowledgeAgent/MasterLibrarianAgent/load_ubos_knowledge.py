#!/usr/bin/env python3
"""
Load UBOS Knowledge Data into Master Librarian
"""

import sys
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

# Add path
sys.path.insert(0, str(Path(__file__).parent))

@dataclass
class SimpleConcept:
    """Simple concept for UBOS knowledge"""
    id: str
    name: str
    description: str
    category: str

def create_ubos_concepts() -> Dict[str, SimpleConcept]:
    """Create core UBOS concepts"""
    concepts = {}

    # Core UBOS principles
    concepts["blueprint_thinking"] = SimpleConcept(
        id="blueprint_thinking",
        name="Blueprint Thinking",
        description="Plan before execution - create intentional system designs",
        category="core_principle"
    )

    concepts["strategic_pause"] = SimpleConcept(
        id="strategic_pause",
        name="Strategic Pause",
        description="Analyze complexity before proceeding - reflection precedes action",
        category="core_principle"
    )

    concepts["systems_over_willpower"] = SimpleConcept(
        id="systems_over_willpower",
        name="Systems Over Willpower",
        description="Create systematic approaches rather than relying on individual effort",
        category="core_principle"
    )

    concepts["constitutional_ai"] = SimpleConcept(
        id="constitutional_ai",
        name="Constitutional AI",
        description="Embed UBOS alignment and principles throughout AI systems",
        category="core_principle"
    )

    # Implementation concepts
    concepts["agent_summoning"] = SimpleConcept(
        id="agent_summoning",
        name="Agent Summoning",
        description="Dynamic creation of specialized agents with constitutional templates",
        category="implementation"
    )

    concepts["multi_agent_coordination"] = SimpleConcept(
        id="multi_agent_coordination",
        name="Multi-Agent Coordination",
        description="Orchestrated collaboration between constitutional AI agents",
        category="implementation"
    )

    concepts["specification_driven_development"] = SimpleConcept(
        id="specification_driven_development",
        name="Specification-Driven Development",
        description="Information gathering → Specification → Implementation workflow",
        category="implementation"
    )

    concepts["gemini_enhancement"] = SimpleConcept(
        id="gemini_enhancement",
        name="Gemini 2.5 Pro Enhancement",
        description="AI-enhanced analysis and constitutional validation using Gemini",
        category="technology"
    )

    concepts["perplexity_research"] = SimpleConcept(
        id="perplexity_research",
        name="Perplexity Research Integration",
        description="Real-time research capabilities with constitutional analysis",
        category="technology"
    )

    concepts["constitutional_compliance"] = SimpleConcept(
        id="constitutional_compliance",
        name="Constitutional Compliance",
        description="Validation that all actions align with UBOS principles",
        category="validation"
    )

    return concepts

class SimpleKnowledgeGraph:
    """Simple knowledge graph for UBOS concepts"""

    def __init__(self):
        self.concepts = create_ubos_concepts()
        self._loaded = True

    def get_concept(self, concept_id: str) -> SimpleConcept:
        """Get concept by ID"""
        return self.concepts.get(concept_id)

    def search_concepts(self, query: str) -> List[SimpleConcept]:
        """Search concepts by query"""
        query_lower = query.lower()
        results = []

        for concept in self.concepts.values():
            if (query_lower in concept.name.lower() or
                query_lower in concept.description.lower()):
                results.append(concept)

        return results

    def get_concepts_by_category(self, category: str) -> List[SimpleConcept]:
        """Get concepts by category"""
        return [c for c in self.concepts.values() if c.category == category]

def test_knowledge_loading():
    """Test UBOS knowledge loading"""
    print("📚 TESTING UBOS KNOWLEDGE LOADING")
    print("="*50)

    try:
        # Create knowledge graph
        kg = SimpleKnowledgeGraph()

        print(f"   ✅ Knowledge graph created")
        print(f"   📊 Concepts loaded: {len(kg.concepts)}")

        # Test concept retrieval
        blueprint = kg.get_concept("blueprint_thinking")
        if blueprint:
            print(f"   🔍 Blueprint Thinking: {blueprint.description[:50]}...")

        # Test search
        ai_concepts = kg.search_concepts("AI")
        print(f"   🔎 AI-related concepts: {len(ai_concepts)}")

        # Test categories
        principles = kg.get_concepts_by_category("core_principle")
        print(f"   🏛️ Core principles: {len(principles)}")

        for principle in principles:
            print(f"      - {principle.name}")

        return {
            "knowledge_loaded": True,
            "concept_count": len(kg.concepts),
            "categories": len(set(c.category for c in kg.concepts.values())),
            "knowledge_graph": kg
        }

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"knowledge_loaded": False, "error": str(e)}

if __name__ == "__main__":
    result = test_knowledge_loading()

    if result["knowledge_loaded"]:
        print(f"\n✅ UBOS Knowledge Successfully Loaded!")
        print(f"   Concepts: {result['concept_count']}")
        print(f"   Categories: {result['categories']}")
    else:
        print(f"\n❌ Knowledge loading failed: {result.get('error')}")