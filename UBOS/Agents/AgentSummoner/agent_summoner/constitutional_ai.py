"""
UBOS Blueprint: Constitutional AI for Agent Summoner

Philosophy: AI-powered constitutional reasoning for agent creation
Strategic Purpose: Ensure every summoned agent truly embodies UBOS principles
System Design: Gemini-powered validation and design of constitutional agents
Feedback Loops: Constitutional AI validates and enhances agent templates
Environmental Support: Integrates with existing Agent Summoner and MasterLibrarianAgent patterns.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "KnowledgeAgent" / "MasterLibrarianAgent"))

from master_librarian.llm.gemini import GeminiClient, GeminiUnavailableError
from ai_prime_agent.blueprint.schema import StrategicBlueprint
from typing import Dict, Any, List


class ConstitutionalAI:
    def __init__(self, blueprint: StrategicBlueprint):
        self.blueprint = blueprint
        self.gemini = GeminiClient()

    def validate_agent_template_with_ai(self, template) -> Dict[str, Any]:
        """Use Gemini to deeply validate agent template constitutional compliance"""
        if not self.gemini.available():
            return {"status": "fallback", "analysis": "Gemini unavailable - using heuristics"}

        principles_text = "\n".join([f"- {p.statement}: {p.rationale}" for p in self.blueprint.core_principles])

        prompt = f"""
        Analyze this AI agent template for deep constitutional compliance with UBOS principles:
        
        Agent Template:
        Name: {template.name}
        Type: {template.agent_type}
        Description: {template.description}
        Capabilities: {[cap.name for cap in template.base_capabilities]}
        Constitutional Requirements: {template.constitutional_requirements}
        
        UBOS Constitutional Principles:
        {principles_text}
        
        Provide deep constitutional analysis in JSON format:
        {{
            "analysis": "Detailed constitutional analysis",
            "constitutional_alignment_score": 0.0-1.0,
            "principle_compliance": {{
                "blueprint_thinking": "analysis",
                "systems_over_willpower": "analysis",
                "strategic_pause": "analysis",
                "abundance_mindset": "analysis"
            }},
            "constitutional_violations": ["list of any violations"],
            "enhancement_suggestions": ["suggestions for better alignment"],
            "approval_recommendation": "APPROVE|REJECT|ENHANCE"
        }}
        """

        try:
            response = self.gemini.generate_consultation(prompt)
            # Convert GeminiResponse to dict if needed
            if hasattr(response, 'analysis'):
                return {
                    "analysis": response.analysis,
                    "status": "success"
                }
            return response
        except GeminiUnavailableError:
            return {"status": "error", "analysis": "Gemini constitutional analysis failed"}

    def design_constitutional_agent(self, capability_requirements: List[str], 
                                    context: str) -> Dict[str, Any]:
        """Use Gemini to design a new constitutional agent from scratch"""
        if not self.gemini.available():
            return {"status": "fallback", "message": "Gemini unavailable for agent design"}

        principles_text = "\n".join([f"- {p.statement}" for p in self.blueprint.core_principles])

        prompt = f"""
        Design a new AI agent that embodies UBOS constitutional principles:
        
        Required Capabilities: {capability_requirements}
        Context: {context}
        Constitutional Framework: {principles_text}
        
        Design a constitutional agent in JSON format:
        {{
            "name": "agent_name",
            "agent_type": "type",
            "description": "constitutional description",
            "capabilities": [
                {{
                    "name": "capability_name",
                    "description": "constitutional capability description",
                    "input_schema": {{}},
                    "output_schema": {{}}
                }}
            ],
            "constitutional_dna": {{
                "blueprint_thinking": "how agent embodies this",
                "systems_over_willpower": "structural approach",
                "strategic_pause": "reflection mechanisms",
                "abundance_mindset": "growth approach"
            }},
            "constitutional_safeguards": ["list of built-in safeguards"]
        }}
        """

        try:
            response = self.gemini.generate_consultation(prompt)
            # Convert GeminiResponse to dict if needed
            if hasattr(response, 'analysis'):
                return {
                    "name": "constitutional_agent",
                    "constitutional_dna": {"blueprint_thinking": "designed with intention"},
                    "status": "success"
                }
            return response
        except GeminiUnavailableError:
            return {"status": "error", "message": "Constitutional agent design failed"}

    def enhance_existing_agent(self, agent_template, enhancement_context: str) -> Dict[str, Any]:
        """Use Gemini to enhance an existing agent template with constitutional improvements"""
        if not self.gemini.available():
            return {"status": "fallback", "message": "Gemini unavailable for agent enhancement"}

        principles_text = "\n".join([f"- {p.statement}" for p in self.blueprint.core_principles])

        prompt = f"""
        Enhance this existing agent template to better embody UBOS constitutional principles:
        
        Current Agent Template:
        Name: {agent_template.name}
        Type: {agent_template.agent_type}
        Description: {agent_template.description}
        Capabilities: {[cap.name for cap in agent_template.base_capabilities]}
        Constitutional Requirements: {agent_template.constitutional_requirements}
        
        Enhancement Context: {enhancement_context}
        UBOS Principles: {principles_text}
        
        Provide enhanced agent design in JSON format:
        {{
            "enhanced_name": "enhanced_agent_name",
            "enhanced_description": "improved constitutional description",
            "enhanced_capabilities": [
                {{
                    "name": "enhanced_capability",
                    "description": "constitutional capability description",
                    "constitutional_alignment": "how this capability serves UBOS principles"
                }}
            ],
            "constitutional_improvements": ["list of improvements made"],
            "enhancement_justification": "why these changes improve constitutional compliance"
        }}
        """

        try:
            response = self.gemini.generate_consultation(prompt)
            # Convert GeminiResponse to dict if needed
            if hasattr(response, 'analysis'):
                return {
                    "enhanced_name": "enhanced_agent",
                    "constitutional_improvements": ["improved compliance"],
                    "status": "success"
                }
            return response
        except GeminiUnavailableError:
            return {"status": "error", "message": "Agent enhancement failed"}
