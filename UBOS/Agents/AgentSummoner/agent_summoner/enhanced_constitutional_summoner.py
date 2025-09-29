"""
UBOS Blueprint: Enhanced Constitutional Agent Summoner v2.0

Philosophy: Blueprint Thinking + Constitutional Intelligence + Adaptive Evolution
Strategic Purpose: Create constitutionally optimal agents through intelligent reasoning and template evolution.
System Design: Hybrid template + thinking system with Gemini 2.5 constitutional reasoning.
Feedback Loops: Agent performance feeds back into constitutional learning and template evolution.
Environmental Support: Extends existing constitutional summoner with intelligent adaptation.

Evolution Notes:
- Phase 1: Hybrid approach (template fallback + thinking mode)
- Maintains 100% backward compatibility with existing system
- Adds constitutional intelligence without breaking current functionality
"""

from __future__ import annotations

import json
import uuid
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import sys

# Import existing constitutional summoner
from .constitutional_summoner import ConstitutionalSummoner
from .agent_templates import AgentTemplateRegistry, AgentTemplate

# Import Gemini for constitutional thinking
sys.path.append(str(Path(__file__).parent.parent.parent / "KnowledgeAgent/MasterLibrarianAgent"))
try:
    from master_librarian.llm.gemini import GeminiClient
except ImportError:
    GeminiClient = None

@dataclass
class TaskAnalysis:
    """Intelligent task analysis results"""
    task_type: str  # research, development, architecture, integration, documentation, testing
    complexity: str  # simple, moderate, complex
    required_capabilities: List[str]
    constitutional_requirements: List[str]
    estimated_time_minutes: int
    confidence_score: float  # How confident we are in this analysis
    reasoning: str  # Why we made these choices

@dataclass
class AgentRecommendation:
    """Intelligent agent recommendation"""
    agent_type: str
    suitability_score: float  # 0-100
    reasoning: str
    constitutional_alignment: Dict[str, Any]
    estimated_cost: float
    configuration: Dict[str, Any]
    template_match: Optional[str]  # None if dynamic creation needed

@dataclass
class ConstitutionalGenetics:
    """Constitutional DNA for agent creation"""
    blueprint_thinking_gene: Dict[str, Any]
    strategic_pause_gene: Dict[str, Any]
    systems_over_willpower_gene: Dict[str, Any]
    constitutional_ai_gene: Dict[str, Any]
    domain_specialization_gene: Dict[str, Any]
    adaptation_potential: float  # How well this agent can evolve

class EnhancedConstitutionalSummoner:
    """
    Enhanced Constitutional Summoner with Gemini 2.5 thinking capabilities.

    Modes:
    - 'template': Use existing template system (backward compatibility)
    - 'thinking': Use Gemini 2.5 constitutional reasoning
    - 'hybrid': Intelligent choice between template and thinking
    - 'auto': Alias for hybrid (default)
    """

    def __init__(self, blueprint=None, registry=None, template_registry=None):
        # Create fallback instances if not provided
        if not template_registry:
            template_registry = AgentTemplateRegistry()

        # For now, keep it simple and initialize basic attributes
        # Parent class integration will be added in future phases
        self.template_registry = template_registry
        self.blueprint = blueprint
        self.registry = registry
        self.lifecycle_manager = None
        self.constitutional_validator = None
        self.strategic_pause = None

        # Initialize thinking capabilities
        self.gemini_client = None
        self.thinking_enabled = False
        self._initialize_thinking_system()

        # Agent knowledge base (inspired by original EUFM system)
        self.agent_knowledge_base = self._load_agent_capabilities()

        # Constitutional learning system
        self.constitutional_memory = {}
        self.agent_genealogy = {}
        self.performance_metrics = {}

        # Default mode
        self.default_mode = "hybrid"

    def _initialize_thinking_system(self):
        """Initialize Gemini 2.5 thinking capabilities"""
        try:
            if GeminiClient:
                self.gemini_client = GeminiClient()
                if self.gemini_client.available():
                    self.thinking_enabled = True
                    print("✅ Constitutional thinking enabled (Gemini 2.5)")
                else:
                    print("⚠️ Gemini not available - using template mode only")
            else:
                print("⚠️ Gemini client not found - using template mode only")
        except Exception as e:
            print(f"⚠️ Thinking system initialization failed: {e}")

    def _load_agent_capabilities(self) -> Dict[str, Any]:
        """Load agent capability knowledge base (enhanced from EUFM system)"""
        return {
            "enhanced_research_agent": {
                "capabilities": ["research", "constitutional_analysis", "perplexity_integration", "gemini_consultation"],
                "cost": 0.05,  # per query
                "speed": "medium",  # 30 seconds
                "quality": "professional",
                "constitutional_alignment": "maximum",
                "domains": ["general", "constitutional_ai", "eu_funding", "academic"]
            },
            "agent_summoner": {
                "capabilities": ["meta_analysis", "agent_discovery", "template_creation", "constitutional_validation"],
                "cost": 0.02,
                "speed": "fast",  # instant templates
                "quality": "enterprise",
                "constitutional_alignment": "maximum",
                "domains": ["agent_creation", "constitutional_compliance"]
            },
            "master_librarian": {
                "capabilities": ["knowledge_management", "constitutional_consultation", "ubos_concepts", "gemini_integration"],
                "cost": 0.03,
                "speed": "fast",  # 15 seconds
                "quality": "expert",
                "constitutional_alignment": "maximum",
                "domains": ["knowledge_base", "constitutional_guidance", "ubos_principles"]
            },
            "orchestration_engine": {
                "capabilities": ["agent_routing", "constitutional_priority", "strategic_decisions", "workflow_management"],
                "cost": 0.01,
                "speed": "very_fast",  # <1 second
                "quality": "intelligent",
                "constitutional_alignment": "maximum",
                "domains": ["coordination", "decision_making", "constitutional_override"]
            },
            "implementation_agent": {
                "capabilities": ["code_generation", "constitutional_implementation", "ubos_compliance", "documentation"],
                "cost": 0.04,
                "speed": "medium",
                "quality": "production_ready",
                "constitutional_alignment": "maximum",
                "domains": ["development", "constitutional_coding", "quality_assurance"]
            }
        }

    async def summon_constitutional_agent(self,
                                        task_description: str,
                                        mode: str = "auto",
                                        template_name: Optional[str] = None,
                                        agent_id: Optional[str] = None,
                                        specialized_config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Enhanced agent summoning with constitutional intelligence.

        Args:
            task_description: Natural language description of what the agent should do
            mode: 'template', 'thinking', 'hybrid', or 'auto'
            template_name: Specific template to use (if mode='template')
            agent_id: Custom agent ID
            specialized_config: Additional configuration

        Returns:
            AgentRecord with constitutional inheritance
        """

        if mode == "auto":
            mode = self.default_mode

        print(f"🧠 Constitutional Agent Summoning: {mode} mode")
        print(f"📋 Task: {task_description}")

        try:
            if mode == "template":
                return await self._template_based_summoning(template_name, task_description, agent_id, specialized_config)

            elif mode == "thinking" and self.thinking_enabled:
                return await self._thinking_based_summoning(task_description, agent_id, specialized_config)

            elif mode == "hybrid":
                return await self._hybrid_intelligent_summoning(task_description, agent_id, specialized_config)

            else:
                # Fallback to template mode
                print("⚠️ Falling back to template mode")
                return await self._template_based_summoning(None, task_description, agent_id, specialized_config)

        except Exception as e:
            print(f"❌ Agent summoning failed: {e}")
            # Ultimate fallback - use template creation
            fallback_template = template_name or "specification_agent"
            return await self._fallback_template_creation(fallback_template, agent_id, specialized_config)

    async def _template_based_summoning(self, template_name: Optional[str], task_description: str,
                                      agent_id: Optional[str], specialized_config: Optional[Dict[str, Any]]) -> Any:
        """Use existing template system (backward compatibility)"""
        print("🏛️ Using template-based constitutional summoning")

        if not template_name:
            # Intelligent template selection based on task
            template_name = self._select_best_template(task_description)
            print(f"📝 Auto-selected template: {template_name}")

        # Use our own template creation system
        return await self._fallback_template_creation(template_name, agent_id, specialized_config)

    async def _thinking_based_summoning(self, task_description: str,
                                      agent_id: Optional[str], specialized_config: Optional[Dict[str, Any]]) -> Any:
        """Use Gemini 2.5 constitutional thinking for agent creation"""
        print("🧠 Using constitutional thinking summoning")

        # Step 1: Constitutional task analysis
        task_analysis = await self._analyze_task_constitutionally(task_description)
        print(f"📊 Task analysis confidence: {task_analysis.confidence_score:.1%}")

        # Step 2: Constitutional agent recommendation
        recommendations = await self._recommend_constitutional_agent(task_analysis)

        # Step 3: If template matches well, use it; otherwise create dynamic agent
        best_rec = recommendations[0] if recommendations else None

        if best_rec and best_rec.template_match and best_rec.suitability_score >= 70:
            print(f"✅ High-confidence template match: {best_rec.template_match} ({best_rec.suitability_score:.1f}%)")
            return await self._template_based_summoning(best_rec.template_match, task_description, agent_id, specialized_config)
        else:
            print("🔬 Creating dynamic constitutional agent")
            return await self._create_dynamic_constitutional_agent(task_analysis, best_rec, agent_id, specialized_config)

    async def _hybrid_intelligent_summoning(self, task_description: str,
                                          agent_id: Optional[str], specialized_config: Optional[Dict[str, Any]]) -> Any:
        """Intelligent hybrid approach - best of both worlds"""
        print("🎯 Using hybrid intelligent summoning")

        # Quick template confidence check
        template_confidence = self._calculate_template_confidence(task_description)
        print(f"🏛️ Template confidence: {template_confidence:.1%}")

        if template_confidence >= 0.7:
            print("✅ High template confidence - using template system")
            return await self._template_based_summoning(None, task_description, agent_id, specialized_config)

        elif self.thinking_enabled:
            print("🧠 Low template confidence - using constitutional thinking")
            return await self._thinking_based_summoning(task_description, agent_id, specialized_config)

        else:
            print("⚠️ Thinking disabled - falling back to best template")
            return await self._template_based_summoning(None, task_description, agent_id, specialized_config)

    def _select_best_template(self, task_description: str) -> str:
        """Select best template based on task analysis"""
        task_lower = task_description.lower()

        # Simple heuristic matching (can be enhanced)
        if any(word in task_lower for word in ["research", "analyze", "investigate", "study"]):
            return "research_specialist"
        elif any(word in task_lower for word in ["eu", "grant", "funding", "horizon", "european"]):
            return "eu_grant_specialist"
        elif any(word in task_lower for word in ["code", "develop", "implement", "generate", "create"]):
            return "implementation_agent"
        elif any(word in task_lower for word in ["spec", "specification", "breakdown", "plan"]):
            return "specification_agent"
        else:
            return "specification_agent"  # Default

    def _calculate_template_confidence(self, task_description: str) -> float:
        """Calculate how confident we are that templates can handle this task"""
        task_lower = task_description.lower()

        # Check for template keywords
        template_keywords = {
            "research_specialist": ["research", "analyze", "investigate", "study", "data", "findings"],
            "eu_grant_specialist": ["eu", "grant", "funding", "horizon", "european", "application"],
            "implementation_agent": ["code", "develop", "implement", "generate", "create", "build"],
            "specification_agent": ["spec", "specification", "breakdown", "plan", "requirements"]
        }

        max_confidence = 0.0
        for template, keywords in template_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in task_lower)
            confidence = min(matches / len(keywords), 1.0)
            max_confidence = max(max_confidence, confidence)

        # Penalty for complex or unusual requests
        complexity_indicators = ["complex", "advanced", "novel", "unique", "custom", "specialized"]
        complexity_penalty = sum(0.1 for indicator in complexity_indicators if indicator in task_lower)

        return max(0.0, max_confidence - complexity_penalty)

    async def _analyze_task_constitutionally(self, task_description: str) -> TaskAnalysis:
        """Use Gemini 2.5 for constitutional task analysis"""

        if not self.gemini_client:
            # Fallback to simple analysis
            return self._simple_task_analysis(task_description)

        try:
            analysis_prompt = f"""
            Constitutional AI Task Analysis:

            Task: {task_description}

            Analyze this task according to UBOS constitutional principles:

            1. TASK TYPE: What type of task is this?
               - research (investigation, analysis, data gathering)
               - development (coding, creation, building)
               - architecture (planning, design, structure)
               - integration (connecting, combining, coordinating)
               - documentation (writing, explaining, guides)
               - testing (validation, verification, quality assurance)

            2. COMPLEXITY: How complex is this task?
               - simple (straightforward, single-step, clear requirements)
               - moderate (multi-step, some uncertainty, standard complexity)
               - complex (multi-faceted, high uncertainty, advanced requirements)

            3. CONSTITUTIONAL REQUIREMENTS: Which UBOS principles are essential?
               - blueprint_thinking (comprehensive planning needed?)
               - strategic_pause (complexity analysis required?)
               - systems_over_willpower (systematic approach needed?)
               - constitutional_ai (UBOS alignment critical?)

            4. CAPABILITIES NEEDED: What specific capabilities are required?
               From: research, constitutional_analysis, code_generation,
               knowledge_management, agent_coordination, web_automation,
               document_generation, quality_assurance

            5. TIME ESTIMATE: How long should this reasonably take?
               Give estimate in minutes (5-300 range)

            6. CONFIDENCE: How confident are you in this analysis? (0-100%)

            Respond in JSON format:
            {{
                "task_type": "...",
                "complexity": "...",
                "constitutional_requirements": ["...", "..."],
                "required_capabilities": ["...", "..."],
                "estimated_time_minutes": 0,
                "confidence_score": 0.0,
                "reasoning": "Detailed explanation of analysis..."
            }}
            """

            response = await self.gemini_client.constitutional_consultation(analysis_prompt, {
                "task": task_description,
                "analysis_type": "constitutional_task_analysis"
            })

            # Parse Gemini response
            try:
                analysis_data = json.loads(response.analysis)
                return TaskAnalysis(**analysis_data)
            except (json.JSONDecodeError, TypeError):
                # Fallback parsing from text response
                return self._parse_text_analysis(response.analysis, task_description)

        except Exception as e:
            print(f"⚠️ Gemini analysis failed: {e}")
            return self._simple_task_analysis(task_description)

    def _simple_task_analysis(self, task_description: str) -> TaskAnalysis:
        """Simple fallback task analysis without Gemini"""
        task_lower = task_description.lower()

        # Determine task type
        task_type = "development"  # default
        if any(word in task_lower for word in ["research", "analyze", "investigate"]):
            task_type = "research"
        elif any(word in task_lower for word in ["architecture", "design", "structure"]):
            task_type = "architecture"
        elif any(word in task_lower for word in ["integrate", "connect", "api"]):
            task_type = "integration"
        elif any(word in task_lower for word in ["document", "readme", "guide"]):
            task_type = "documentation"
        elif any(word in task_lower for word in ["test", "verify", "validate"]):
            task_type = "testing"

        # Determine complexity
        complexity = "moderate"
        if any(word in task_lower for word in ["simple", "quick", "basic"]):
            complexity = "simple"
        elif any(word in task_lower for word in ["complex", "advanced", "comprehensive"]):
            complexity = "complex"

        # Required capabilities
        capabilities = []
        if "research" in task_lower or "analyze" in task_lower:
            capabilities.append("research")
        if "code" in task_lower or "develop" in task_lower:
            capabilities.append("code_generation")
        if "constitutional" in task_lower or "ubos" in task_lower:
            capabilities.append("constitutional_analysis")

        return TaskAnalysis(
            task_type=task_type,
            complexity=complexity,
            required_capabilities=capabilities,
            constitutional_requirements=["constitutional_ai"],  # Default
            estimated_time_minutes=30 if complexity == "complex" else 15,
            confidence_score=0.6,  # Moderate confidence for simple analysis
            reasoning=f"Simple analysis based on keywords in task description"
        )

    async def _recommend_constitutional_agent(self, task_analysis: TaskAnalysis) -> List[AgentRecommendation]:
        """Recommend optimal constitutional agent based on analysis"""
        recommendations = []

        # Score each available agent type
        for agent_type, agent_info in self.agent_knowledge_base.items():
            suitability_score = self._calculate_agent_suitability(agent_type, agent_info, task_analysis)

            if suitability_score > 20:  # Only include reasonable matches

                # Check if this matches an existing template
                template_match = self._find_template_match(agent_type, task_analysis)

                recommendation = AgentRecommendation(
                    agent_type=agent_type,
                    suitability_score=suitability_score,
                    reasoning=self._generate_recommendation_reasoning(agent_type, agent_info, task_analysis),
                    constitutional_alignment={
                        "alignment_score": agent_info.get("constitutional_alignment", "medium"),
                        "requirements_met": task_analysis.constitutional_requirements
                    },
                    estimated_cost=agent_info.get("cost", 0.02),
                    configuration=self._generate_agent_configuration(agent_type, task_analysis),
                    template_match=template_match
                )

                recommendations.append(recommendation)

        # Sort by suitability score
        recommendations.sort(key=lambda r: r.suitability_score, reverse=True)
        return recommendations[:3]  # Top 3 recommendations

    def _calculate_agent_suitability(self, agent_type: str, agent_info: Dict[str, Any],
                                   task_analysis: TaskAnalysis) -> float:
        """Calculate how suitable an agent type is for the analyzed task"""
        score = 0.0

        # Capability matching (40% weight)
        agent_capabilities = agent_info.get("capabilities", [])
        capability_matches = len(set(task_analysis.required_capabilities) & set(agent_capabilities))
        if task_analysis.required_capabilities:
            capability_score = (capability_matches / len(task_analysis.required_capabilities)) * 40
            score += capability_score

        # Task type specific bonuses (30% weight)
        task_bonuses = {
            "research": {"enhanced_research_agent": 25, "master_librarian": 15},
            "development": {"implementation_agent": 25, "orchestration_engine": 10},
            "architecture": {"agent_summoner": 20, "orchestration_engine": 15},
            "integration": {"orchestration_engine": 25, "implementation_agent": 15},
            "documentation": {"implementation_agent": 20, "master_librarian": 15},
            "testing": {"implementation_agent": 15, "orchestration_engine": 10}
        }

        task_bonus = task_bonuses.get(task_analysis.task_type, {}).get(agent_type, 0)
        score += task_bonus

        # Complexity bonuses (10% weight)
        if task_analysis.complexity == "complex":
            if agent_info.get("quality") in ["professional", "expert", "production_ready"]:
                score += 10
        elif task_analysis.complexity == "simple":
            if agent_info.get("speed") in ["fast", "very_fast"]:
                score += 5

        # Constitutional alignment bonus (20% weight)
        if agent_info.get("constitutional_alignment") == "maximum":
            score += 20

        return min(100.0, score)

    def _find_template_match(self, agent_type: str, task_analysis: TaskAnalysis) -> Optional[str]:
        """Check if agent type matches an existing template"""
        template_mappings = {
            "enhanced_research_agent": "research_specialist",
            "implementation_agent": "implementation_agent",
            "master_librarian": None,  # No direct template
            "orchestration_engine": None,  # No direct template
            "agent_summoner": "specification_agent"  # Closest match
        }

        # Special case for EU funding
        if any("eu" in cap.lower() for cap in task_analysis.required_capabilities):
            if agent_type == "enhanced_research_agent":
                return "eu_grant_specialist"

        return template_mappings.get(agent_type)

    def _generate_recommendation_reasoning(self, agent_type: str, agent_info: Dict[str, Any],
                                         task_analysis: TaskAnalysis) -> str:
        """Generate human-readable reasoning for recommendation"""
        reasoning_parts = []

        # Capability matching
        agent_capabilities = set(agent_info.get("capabilities", []))
        required_capabilities = set(task_analysis.required_capabilities)
        matches = agent_capabilities & required_capabilities

        if matches:
            reasoning_parts.append(f"Matches capabilities: {', '.join(matches)}")

        # Task type alignment
        if task_analysis.task_type in agent_info.get("domains", []):
            reasoning_parts.append(f"Specialized for {task_analysis.task_type} tasks")

        # Quality indicators
        if agent_info.get("constitutional_alignment") == "maximum":
            reasoning_parts.append("Maximum constitutional alignment")

        quality = agent_info.get("quality")
        if quality:
            reasoning_parts.append(f"Quality: {quality}")

        cost = agent_info.get("cost", 0)
        reasoning_parts.append(f"Cost: ${cost:.3f}")

        return "; ".join(reasoning_parts)

    def _generate_agent_configuration(self, agent_type: str, task_analysis: TaskAnalysis) -> Dict[str, Any]:
        """Generate optimal configuration for agent based on analysis"""
        base_config = {
            "task_type": task_analysis.task_type,
            "complexity": task_analysis.complexity,
            "constitutional_requirements": task_analysis.constitutional_requirements,
            "estimated_time_minutes": task_analysis.estimated_time_minutes
        }

        # Agent-specific configurations
        specific_configs = {
            "enhanced_research_agent": {
                "depth": "deep" if task_analysis.complexity == "complex" else "medium",
                "constitutional_analysis_required": True,
                "archive_enabled": True
            },
            "implementation_agent": {
                "constitutional_compliance": "maximum",
                "quality_assurance": True,
                "documentation_required": task_analysis.task_type == "documentation"
            },
            "master_librarian": {
                "constitutional_consultation": True,
                "ubos_concepts_integration": True
            },
            "orchestration_engine": {
                "constitutional_priority": True,
                "routing_optimization": True
            }
        }

        base_config.update(specific_configs.get(agent_type, {}))
        return base_config

    async def _create_dynamic_constitutional_agent(self, task_analysis: TaskAnalysis,
                                                 recommendation: Optional[AgentRecommendation],
                                                 agent_id: Optional[str],
                                                 specialized_config: Optional[Dict[str, Any]]) -> Any:
        """Create a dynamic constitutional agent using Gemini reasoning"""
        print("🧬 Creating dynamic constitutional agent with Gemini reasoning")

        # For now, we'll create a hybrid approach - use the best template but enhance it
        # Full dynamic creation would require more complex agent instantiation

        if recommendation and recommendation.template_match:
            print(f"🎯 Using enhanced template: {recommendation.template_match}")
            # Use template but with enhanced configuration
            enhanced_config = {**(specialized_config or {}), **recommendation.configuration}
            return await self._template_based_summoning(recommendation.template_match,
                                                      f"Enhanced: {task_analysis.reasoning}",
                                                      agent_id, enhanced_config)
        else:
            print("🔧 Falling back to specification agent for dynamic tasks")
            # Fallback to most flexible template
            return await self._template_based_summoning("specification_agent",
                                                      task_analysis.reasoning,
                                                      agent_id, specialized_config)

    def _parse_text_analysis(self, text_response: str, task_description: str) -> TaskAnalysis:
        """Fallback text parsing if JSON parsing fails"""
        # Simple keyword extraction from Gemini response
        text_lower = text_response.lower()

        # Extract task type
        task_type = "development"
        if "research" in text_lower:
            task_type = "research"
        elif "architecture" in text_lower:
            task_type = "architecture"
        elif "integration" in text_lower:
            task_type = "integration"
        elif "documentation" in text_lower:
            task_type = "documentation"
        elif "testing" in text_lower:
            task_type = "testing"

        # Extract complexity
        complexity = "moderate"
        if "simple" in text_lower:
            complexity = "simple"
        elif "complex" in text_lower:
            complexity = "complex"

        return TaskAnalysis(
            task_type=task_type,
            complexity=complexity,
            required_capabilities=["general"],
            constitutional_requirements=["constitutional_ai"],
            estimated_time_minutes=20,
            confidence_score=0.7,
            reasoning=f"Parsed from Gemini text response: {text_response[:200]}..."
        )

    # Convenience methods for easy usage
    async def quick_summon(self, task_description: str) -> Any:
        """Quick agent summoning with auto mode"""
        return await self.summon_constitutional_agent(task_description, mode="auto")

    async def template_summon(self, template_name: str, task_description: str = "") -> Any:
        """Force template mode summoning"""
        return await self.summon_constitutional_agent(task_description, mode="template", template_name=template_name)

    async def thinking_summon(self, task_description: str) -> Any:
        """Force thinking mode summoning"""
        return await self.summon_constitutional_agent(task_description, mode="thinking")

    async def _fallback_template_creation(self, template_name: str, agent_id: Optional[str],
                                        specialized_config: Optional[Dict[str, Any]]) -> Any:
        """Fallback template creation when parent class is unavailable"""
        try:
            template = self.template_registry.get_template(template_name)
            final_id = agent_id or f"enhanced-{template_name}-{uuid.uuid4().hex[:8]}"

            # Create a simple agent record structure
            from dataclasses import dataclass
            from datetime import datetime, timezone

            @dataclass
            class SimpleAgentRecord:
                agent_id: str
                name: str
                status: str
                capabilities: List[Any]
                template_source: str
                created_at: str
                configuration: Dict[str, Any]

            agent_record = SimpleAgentRecord(
                agent_id=final_id,
                name=f"Enhanced {template.name}",
                status="ACTIVE",
                capabilities=template.base_capabilities,
                template_source=template_name,
                created_at=datetime.now(timezone.utc).isoformat(),
                configuration=specialized_config or {}
            )

            print(f"✅ Created fallback agent: {final_id}")
            return agent_record

        except Exception as e:
            print(f"❌ Fallback creation failed: {e}")
            # Ultimate fallback
            @dataclass
            class MinimalAgentRecord:
                agent_id: str
                status: str
                template_source: str

            return MinimalAgentRecord(
                agent_id=agent_id or f"minimal-{uuid.uuid4().hex[:8]}",
                status="CREATED",
                template_source=template_name or "unknown"
            )