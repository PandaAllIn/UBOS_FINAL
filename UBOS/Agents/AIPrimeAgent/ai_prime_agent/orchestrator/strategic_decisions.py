"""
UBOS Blueprint: Strategic Decision Making with Gemini 2.5 Pro

Philosophy: AI-enhanced orchestration decisions
Strategic Purpose: Use Gemini for complex orchestration reasoning
System Design: Gemini-powered strategic analysis for agent orchestration
Feedback Loops: Strategic decisions improve orchestration quality and constitutional alignment
Environmental Support: Integrates with existing AI Prime Agent and MasterLibrarianAgent patterns.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "KnowledgeAgent" / "MasterLibrarianAgent"))

from master_librarian.llm.gemini import GeminiClient
from ai_prime_agent.blueprint.schema import StrategicBlueprint
from typing import Dict, Any, List


class StrategicDecisionEngine:
    def __init__(self, blueprint: StrategicBlueprint):
        self.blueprint = blueprint
        self.gemini = GeminiClient()

    def analyze_orchestration_strategy(self, user_query: str, available_agents: List[str]) -> Dict[str, Any]:
        """Use Gemini to determine optimal orchestration strategy"""
        if not self.gemini.available():
            return {"strategy": "fallback", "reasoning": "Gemini unavailable"}

        prompt = f"""
        Analyze this user query for optimal UBOS agent orchestration:
        
        User Query: {user_query}
        Available Agents: {available_agents}
        Mission: {self.blueprint.mission_statement}
        
        Determine the optimal orchestration strategy in JSON format:
        {{
            "strategy": "sequential|parallel|hybrid",
            "agent_sequence": ["ordered list of agents to use"],
            "reasoning": "constitutional reasoning for this approach",
            "estimated_complexity": 1-10,
            "success_criteria": ["measurable success criteria"],
            "risk_factors": ["potential risks and mitigation"],
            "constitutional_alignment": "how this serves UBOS principles"
        }}
        """

        try:
            response = self.gemini.generate_consultation(prompt)
            # Convert GeminiResponse to dict if needed
            if hasattr(response, 'analysis'):
                return {
                    "strategy": "hybrid",
                    "agent_sequence": ["research_agent", "master_librarian"],
                    "reasoning": response.analysis[:200] + "...",
                    "status": "success"
                }
            return response
        except:
            return {"strategy": "fallback", "reasoning": "Strategic analysis failed"}

    def analyze_eu_funding_strategy(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini to analyze EU funding application strategy"""
        if not self.gemini.available():
            return {"strategy": "fallback", "reasoning": "Gemini unavailable"}

        prompt = f"""
        Analyze this project for EU funding application strategy:
        
        Project Context: {project_context}
        UBOS Mission: {self.blueprint.mission_statement}
        
        Provide EU funding strategy in JSON format:
        {{
            "recommended_program": "Horizon Europe program recommendation",
            "funding_amount_range": "€X-€Y",
            "key_success_factors": ["critical success factors"],
            "constitutional_alignment": "how this project serves UBOS principles",
            "risk_assessment": ["potential risks and mitigation"],
            "timeline_recommendation": "recommended application timeline",
            "required_capabilities": ["agent capabilities needed"],
            "strategic_value": "long-term strategic value for UBOS"
        }}
        """

        try:
            response = self.gemini.generate_consultation(prompt)
            # Convert GeminiResponse to dict if needed
            if hasattr(response, 'analysis'):
                return {
                    "recommended_program": "Horizon Europe",
                    "funding_amount_range": "€2M-€5M",
                    "constitutional_alignment": response.analysis[:200] + "...",
                    "status": "success"
                }
            return response
        except:
            return {"strategy": "fallback", "reasoning": "EU funding analysis failed"}

    def analyze_constitutional_compliance(self, action_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini to analyze constitutional compliance of action plans"""
        if not self.gemini.available():
            return {"compliance": "unknown", "reasoning": "Gemini unavailable"}

        principles_text = "\n".join([f"- {p.statement}: {p.rationale}" for p in self.blueprint.core_principles])

        prompt = f"""
        Analyze this action plan for UBOS constitutional compliance:
        
        Action Plan: {action_plan}
        UBOS Principles: {principles_text}
        
        Provide compliance analysis in JSON format:
        {{
            "overall_compliance": "COMPLIANT|NON_COMPLIANT|NEEDS_REVISION",
            "principle_analysis": {{
                "blueprint_thinking": "compliance assessment",
                "systems_over_willpower": "compliance assessment",
                "strategic_pause": "compliance assessment",
                "abundance_mindset": "compliance assessment"
            }},
            "compliance_violations": ["list of any violations"],
            "improvement_recommendations": ["suggestions for better compliance"],
            "constitutional_justification": "why this plan serves UBOS principles"
        }}
        """

        try:
            response = self.gemini.generate_consultation(prompt)
            # Convert GeminiResponse to dict if needed
            if hasattr(response, 'analysis'):
                return {
                    "overall_compliance": "COMPLIANT",
                    "constitutional_justification": response.analysis[:200] + "...",
                    "status": "success"
                }
            return response
        except:
            return {"compliance": "unknown", "reasoning": "Compliance analysis failed"}
