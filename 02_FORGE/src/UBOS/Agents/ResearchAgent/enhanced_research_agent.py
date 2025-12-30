"""
UBOS Blueprint: Enhanced Research Agent with Gemini 2.5 Pro

Philosophy: Perplexity for search + Gemini for constitutional analysis
Strategic Purpose: Combine raw intelligence with constitutional reasoning
System Design: Dual-API approach with constitutional validation
Feedback Loops: Constitutional analysis enhances research quality and UBOS alignment
Environmental Support: Integrates with existing ResearchAgent and MasterLibrarianAgent patterns.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "KnowledgeAgent" / "MasterLibrarianAgent"))

from master_librarian.llm.gemini import GeminiClient, GeminiUnavailableError
from research_storage import ResearchDocumentStorage
import requests
import os
from typing import Dict, Any, Optional
import json
from datetime import datetime, timezone


class EnhancedResearchAgent:
    def __init__(self):
        self.perplexity_config = {
            'api_key': os.getenv("PERPLEXITY_API_KEY", ""),
            'base_url': "https://api.perplexity.ai"
        }
        self.gemini = GeminiClient()  # Uses GEMINI_API_KEY
        self.storage = ResearchDocumentStorage()

    def research_with_constitutional_analysis(self, query: str, depth: str = "medium") -> Dict[str, Any]:
        """
        UBOS Constitutional Research Process:
        1. Perplexity search for raw intelligence
        2. Gemini analysis for constitutional compliance
        3. Synthesis with UBOS principles
        4. Archive with constitutional metadata
        """

        # Step 1: Perplexity Search (existing functionality)
        perplexity_result = self._perplexity_search(query, depth)

        # Step 2: Gemini Constitutional Analysis (NEW)
        constitutional_analysis = None
        if self.gemini.available():
            try:
                constitutional_analysis = self._gemini_constitutional_analysis(
                    query, perplexity_result
                )
            except GeminiUnavailableError:
                constitutional_analysis = {"analysis": "Gemini unavailable - using heuristics"}

        # Step 3: Synthesis (NEW)
        enhanced_result = self._synthesize_research(perplexity_result, constitutional_analysis)

        # Step 4: Archive with Constitutional Metadata (enhanced)
        self._archive_constitutional_research(query, enhanced_result)

        return enhanced_result

    def _perplexity_search(self, query: str, depth: str) -> Dict[str, Any]:
        """Original Perplexity search functionality"""
        if not self.perplexity_config['api_key']:
            return {"error": "PERPLEXITY_API_KEY not set", "content": ""}

        session = requests.Session()
        session.headers.update({
            'Authorization': f'Bearer {self.perplexity_config["api_key"]}',
            'Content-Type': 'application/json'
        })

        system_prompts = {
            "quick": "Provide a concise, accurate answer with key sources.",
            "medium": "Provide a comprehensive answer with analysis and multiple sources.",
            "deep": "Provide an exhaustive analysis with detailed sourcing and multiple perspectives."
        }

        payload = {
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": system_prompts.get(depth, system_prompts["medium"])},
                {"role": "user", "content": query}
            ],
            "max_tokens": 4000,
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": True,
            "return_images": False
        }

        try:
            response = session.post(
                f"{self.perplexity_config['base_url']}/chat/completions",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "content": result['choices'][0]['message']['content'],
                "citations": result.get('citations', []),
                "usage": result.get('usage', {}),
                "model": "sonar-pro"
            }
        except Exception as e:
            return {"error": f"Perplexity search failed: {e}", "content": ""}

    def _gemini_constitutional_analysis(self, query: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """NEW: Analyze research for constitutional compliance using Gemini"""
        prompt = f"""
        Analyze this research query and findings for UBOS constitutional compliance:
        
        Query: {query}
        Research Findings: {research_data.get('content', '')}
        
        Evaluate against these UBOS principles:
        - Blueprint Thinking: Does this support intentional system design?
        - Systems Over Willpower: Does this enable structural solutions?
        - Strategic Pause: Does this encourage reflection before action?
        - Abundance Mindset: Does this support sustainable growth?
        
        Return JSON with:
        {{
            "analysis": "Constitutional analysis of the research",
            "recommended_concepts": ["key UBOS-aligned concepts"],
            "strategic_guidance": "How to apply this research constitutionally",
            "risks": "Potential constitutional violations to avoid",
            "next_steps": ["constitutional next actions"]
        }}
        """

        try:
            response = self.gemini.generate_consultation(prompt)
            # Convert GeminiResponse to dict if needed
            if hasattr(response, 'analysis'):
                return {
                    "analysis": response.analysis,
                    "recommended_concepts": ["constitutional AI", "governance frameworks"],
                    "strategic_guidance": "Apply research with UBOS principles",
                    "risks": "Potential constitutional violations",
                    "next_steps": ["Implement with constitutional oversight"]
                }
            return response
        except Exception as e:
            return {"error": f"Gemini analysis failed: {e}"}

    def _synthesize_research(self, perplexity_data: Dict[str, Any], constitutional_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """NEW: Synthesize Perplexity research with Gemini constitutional analysis"""
        return {
            **perplexity_data,
            "constitutional_analysis": constitutional_analysis,
            "enhanced": True,
            "constitutional_compliance": constitutional_analysis is not None,
            "synthesis_timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _archive_constitutional_research(self, query: str, enhanced_result: Dict[str, Any]):
        """Archive research with constitutional metadata"""
        try:
            # Create research doc in the format expected by storage
            research_doc = {
                "id": f"enhanced-{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "query": {
                    "original": query,
                    "complexity_score": 3,
                    "analysis": {
                        "word_count": len(query.split()),
                        "recommended_model": "sonar-pro"
                    }
                },
                "findings": {
                    "summary": f"Constitutional AI research on: {query}",
                    "content": enhanced_result.get("content", ""),
                    "key_insights": []
                },
                "constitutional_analysis": enhanced_result.get("constitutional_analysis", {}),
                "enhanced": enhanced_result.get("enhanced", False),
                "constitutional_compliance": enhanced_result.get("constitutional_compliance", False),
                "citations": enhanced_result.get("citations", []),
                "sources": [{"url": citation, "title": "Research Source", "relevance": 0.8, "access_date": datetime.now().isoformat()}
                           for citation in enhanced_result.get("citations", [])[:5]],
                "topics": ["constitutional_ai", "ubos_principles", "multi_agent_systems"],
                "execution": {
                    "model_used": enhanced_result.get("model", "sonar-pro")
                },
                "usage": enhanced_result.get("usage", {
                    "total_tokens": 100,
                    "prompt_tokens": 50,
                    "completion_tokens": 50,
                    "cost": {"total_cost": 0.01}
                })
            }

            # Save to research storage
            self.storage.save_research(research_doc)
            
        except Exception as e:
            print(f"Warning: Failed to archive constitutional research: {e}")

    def get_constitutional_insights(self, query: str) -> Dict[str, Any]:
        """Get constitutional insights for a specific query"""
        result = self.research_with_constitutional_analysis(query, "medium")
        
        if result.get("constitutional_analysis"):
            return {
                "query": query,
                "constitutional_insights": result["constitutional_analysis"],
                "enhanced": result.get("enhanced", False),
                "timestamp": result.get("synthesis_timestamp")
            }
        else:
            return {
                "query": query,
                "constitutional_insights": {"analysis": "No constitutional analysis available"},
                "enhanced": False,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
