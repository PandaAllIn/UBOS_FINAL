"""
UBOS Blueprint: Constitutional Agent Templates

Philosophy: Blueprint Thinking + Smallest Working Version
Strategic Purpose: Provide constitutional templates for dynamic agent creation.
System Design: Template registry with constitutional requirements and resource limits.
Feedback Loops: Template validation ensures constitutional compliance before agent creation.
Environmental Support: Integrates with existing AgentCapability and AgentRecord patterns.
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from ai_prime_agent.registry import AgentCapability


@dataclass
class AgentTemplate:
    name: str
    agent_type: str
    description: str
    base_capabilities: List[AgentCapability]
    constitutional_requirements: Dict[str, Any]
    resource_limits: Dict[str, Any]


class AgentTemplateRegistry:
    """Registry of constitutional agent templates."""

    def __init__(self):
        self.templates: Dict[str, AgentTemplate] = {}
        self._register_default_templates()

    def _register_default_templates(self):
        """Register UBOS constitutional agent templates."""

        # EU Grant Specialist Template
        eu_grant_template = AgentTemplate(
            name="eu_grant_specialist",
            agent_type="eu_funding_specialist",
            description="Constitutional agent specialized in EU Horizon Europe applications",
            base_capabilities=[
                AgentCapability(
                    name="eu_grant.research",
                    version="1.0",
                    description="Research EU funding opportunities with constitutional alignment",
                    input_schema={"query": {"type": "string"}, "program": {"type": "string"}},
                    output_schema={"opportunities": {"type": "array"}, "alignment_score": {"type": "number"}}
                ),
                AgentCapability(
                    name="eu_grant.generate_application",
                    version="1.0",
                    description="Generate constitutionally compliant EU grant applications",
                    input_schema={"opportunity": {"type": "object"}, "project_details": {"type": "object"}},
                    output_schema={"application": {"type": "object"}, "compliance_report": {"type": "object"}}
                )
            ],
            constitutional_requirements={
                "must_align_with": ["European democratic values", "UBOS constitutional principles"],
                "forbidden_activities": ["surveillance", "military applications", "privacy violations"]
            },
            resource_limits={
                "max_runtime_minutes": 60,
                "max_memory_mb": 512,
                "max_api_calls_per_hour": 100
            }
        )
        self.templates["eu_grant_specialist"] = eu_grant_template

        # Specification Agent Template  
        spec_template = AgentTemplate(
            name="specification_agent",
            agent_type="specification_specialist",
            description="Constitutional agent for complex task specification and breakdown",
            base_capabilities=[
                AgentCapability(
                    name="specification.analyze_task",
                    version="1.0",
                    description="Analyze complex tasks with constitutional framework",
                    input_schema={"task": {"type": "string"}, "context": {"type": "object"}},
                    output_schema={"specification": {"type": "object"}, "constitutional_analysis": {"type": "object"}}
                )
            ],
            constitutional_requirements={
                "must_embody": ["Blueprint Thinking", "Strategic Pause", "Systems Over Willpower"]
            },
            resource_limits={
                "max_runtime_minutes": 30,
                "max_memory_mb": 256
            }
        )
        self.templates["specification_agent"] = spec_template

        # Research Specialist Template
        research_template = AgentTemplate(
            name="research_specialist",
            agent_type="research_specialist",
            description="Constitutional agent for specialized research with constitutional alignment",
            base_capabilities=[
                AgentCapability(
                    name="research.specialized_query",
                    version="1.0",
                    description="Perform specialized research with constitutional compliance",
                    input_schema={"query": {"type": "string"}, "specialization": {"type": "string"}},
                    output_schema={"findings": {"type": "object"}, "constitutional_alignment": {"type": "object"}}
                )
            ],
            constitutional_requirements={
                "must_embody": ["Strategic Pause", "Blueprint Thinking", "Systems Over Willpower"]
            },
            resource_limits={
                "max_runtime_minutes": 45,
                "max_memory_mb": 384
            }
        )
        self.templates["research_specialist"] = research_template

        # Implementation Agent Template
        implementation_template = AgentTemplate(
            name="implementation_agent",
            agent_type="implementation_specialist",
            description="Constitutional agent for code implementation and generation",
            base_capabilities=[
                AgentCapability(
                    name="code.implementation",
                    version="1.0",
                    description="Generate constitutionally compliant code from specifications",
                    input_schema={"specification": {"type": "object"}, "language": {"type": "string"}},
                    output_schema={"code": {"type": "string"}, "constitutional_validation": {"type": "object"}}
                ),
                AgentCapability(
                    name="code.review",
                    version="1.0",
                    description="Review code for constitutional compliance",
                    input_schema={"code": {"type": "string"}, "language": {"type": "string"}},
                    output_schema={"review_result": {"type": "object"}, "improvements": {"type": "array"}}
                ),
                AgentCapability(
                    name="code.enhancement",
                    version="1.0",
                    description="Enhance existing code with constitutional improvements",
                    input_schema={"code": {"type": "string"}, "enhancement_requirements": {"type": "array"}},
                    output_schema={"enhanced_code": {"type": "string"}, "enhancement_metadata": {"type": "object"}}
                )
            ],
            constitutional_requirements={
                "must_embody": ["Blueprint Thinking", "Systems Over Willpower", "Strategic Pause"],
                "must_use": ["Codex CLI", "Context7 MCP", "Constitutional validation"]
            },
            resource_limits={
                "max_runtime_minutes": 60,
                "max_memory_mb": 512,
                "max_codex_calls_per_hour": 50
            }
        )
        self.templates["implementation_agent"] = implementation_template

    def get_template(self, name: str) -> AgentTemplate:
        if name not in self.templates:
            raise ValueError(f"Template {name} not found")
        return self.templates[name]

    def register_template(self, template: AgentTemplate):
        self.templates[template.name] = template
