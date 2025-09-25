"""
UBOS Blueprint: Constitutional Implementation Agent

Philosophy: Blueprint Thinking + Systems Over Willpower + Constitutional Code
Strategic Purpose: Generate constitutionally compliant code from specifications
System Design: Codex CLI wrapper with constitutional validation and Context7 guidance
Feedback Loops: Constitutional code review, testing, and iterative refinement
Environmental Support: Integrates with Codex CLI, Context7 MCP, and existing UBOS agents
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "KnowledgeAgent" / "MasterLibrarianAgent"))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "AIPrimeAgent"))

from master_librarian.llm.gemini import GeminiClient, GeminiUnavailableError
from ai_prime_agent.blueprint.schema import StrategicBlueprint
from ai_prime_agent.pause import StrategicPause, PauseDecision
from ai_prime_agent.validation import BlueprintValidator

from .real_codex_wrapper import RealCodexWrapper
from .context7_integration import Context7Integration
from .constitutional_validation import ConstitutionalCodeValidator


class ConstitutionalImplementationAgent:
    """
    Constitutional Implementation Agent
    
    UBOS Principle: Blueprint Thinking - Intentional code design before generation
    Strategic Value: Generate constitutionally compliant code from specifications
    """
    
    def __init__(self, blueprint: StrategicBlueprint):
        self.blueprint = blueprint
        self.gemini = GeminiClient()
        self.strategic_pause = StrategicPause(blueprint)
        self.blueprint_validator = BlueprintValidator(blueprint)
        self.codex_wrapper = RealCodexWrapper()
        self.context7_integration = Context7Integration()
        self.constitutional_validator = ConstitutionalCodeValidator(blueprint)
        
    def implement_from_specification(self, 
                                   specification: Dict[str, Any], 
                                   constitutional_requirements: List[str],
                                   language: str = "Python") -> Dict[str, Any]:
        """
        UBOS Constitutional Implementation Process:
        1. Strategic pause before implementation
        2. Constitutional analysis of specification
        3. Codex CLI code generation
        4. Constitutional code validation
        5. Context7 guidance integration
        6. Testing and refinement
        """
        
        # Step 1: Strategic Pause (Constitutional Checkpoint)
        pause_decision = self.strategic_pause.pre_delegation(
            query=f"Implement {specification.get('name', 'specification')}",
            objectives=[f"Generate constitutionally compliant {language} code"]
        )
        
        if pause_decision.status == "escalate":
            return {
                "status": "escalated",
                "error": f"Constitutional escalation: {pause_decision.reasons}",
                "code": None
            }
        
        # Step 2: Constitutional Analysis of Specification
        constitutional_analysis = self._analyze_specification_constitutionally(
            specification, constitutional_requirements
        )
        
        # Step 3: Generate Code with Codex CLI
        try:
            generated_code = self.codex_wrapper.generate_code(
                specification=specification,
                language=language,
                constitutional_requirements=constitutional_requirements,
                constitutional_analysis=constitutional_analysis
            )
        except Exception as e:
            return {
                "status": "error",
                "error": f"Code generation failed: {e}",
                "code": None
            }
        
        # Step 4: Constitutional Code Validation
        validation_result = self.constitutional_validator.validate_code(
            code=generated_code,
            language=language,
            constitutional_requirements=constitutional_requirements,
            specification=specification
        )
        
        if not validation_result["is_constitutional"]:
            # Attempt to fix constitutional violations
            fixed_code = self._fix_constitutional_violations(
                generated_code, validation_result, language
            )
            if fixed_code:
                generated_code = fixed_code
                validation_result = self.constitutional_validator.validate_code(
                    code=generated_code,
                    language=language,
                    constitutional_requirements=constitutional_requirements,
                    specification=specification
                )
        
        # Step 5: Context7 Guidance Integration
        guidance = self.context7_integration.get_implementation_guidance(
            specification=specification,
            generated_code=generated_code,
            language=language
        )
        
        # Step 6: Generate Constitutional Documentation
        constitutional_docs = self._generate_constitutional_documentation(
            specification, generated_code, constitutional_analysis, validation_result
        )
        
        return {
            "status": "success",
            "code": generated_code,
            "language": language,
            "constitutional_analysis": constitutional_analysis,
            "validation_result": validation_result,
            "guidance": guidance,
            "constitutional_documentation": constitutional_docs,
            "implementation_metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "constitutional_framework": "UBOS_v1.0",
                "specification_id": specification.get("id", "unknown"),
                "constitutional_compliance": validation_result["is_constitutional"]
            }
        }
    
    def _analyze_specification_constitutionally(self, 
                                              specification: Dict[str, Any], 
                                              constitutional_requirements: List[str]) -> Dict[str, Any]:
        """Analyze specification for constitutional compliance using Gemini"""
        if not self.gemini.available():
            return {"analysis": "Gemini unavailable - using heuristics"}
        
        principles_text = "\n".join([f"- {p.statement}: {p.rationale}" for p in self.blueprint.core_principles])
        
        prompt = f"""
        Analyze this specification for constitutional compliance with UBOS principles:
        
        Specification: {json.dumps(specification, indent=2)}
        Constitutional Requirements: {constitutional_requirements}
        
        UBOS Principles:
        {principles_text}
        
        Provide constitutional analysis in JSON format:
        {{
            "constitutional_alignment": "how this specification aligns with UBOS principles",
            "implementation_guidance": "constitutional guidance for implementation",
            "potential_violations": ["list of potential constitutional violations"],
            "constitutional_enhancements": ["suggestions for better constitutional compliance"],
            "blueprint_thinking_applied": "how Blueprint Thinking applies to this implementation",
            "systems_over_willpower_applied": "how Systems Over Willpower applies to this implementation"
        }}
        """
        
        try:
            response = self.gemini.generate_consultation(prompt)
            if hasattr(response, 'analysis'):
                return {
                    "constitutional_alignment": response.analysis,
                    "implementation_guidance": "Follow UBOS principles in implementation",
                    "potential_violations": [],
                    "constitutional_enhancements": ["Add constitutional documentation"],
                    "blueprint_thinking_applied": "Intentional design before coding",
                    "systems_over_willpower_applied": "Structural solutions over manual coding"
                }
            return response
        except GeminiUnavailableError:
            return {"analysis": "Gemini constitutional analysis failed"}
    
    def _fix_constitutional_violations(self, 
                                     code: str, 
                                     validation_result: Dict[str, Any], 
                                     language: str) -> Optional[str]:
        """Attempt to fix constitutional violations in generated code"""
        if not self.gemini.available():
            return None
        
        violations = validation_result.get("violations", [])
        if not violations:
            return code
        
        prompt = f"""
        Fix these constitutional violations in the generated code:
        
        Code:
        {code}
        
        Language: {language}
        Violations: {violations}
        
        Provide the corrected code that addresses all constitutional violations:
        """
        
        try:
            response = self.gemini.generate_consultation(prompt)
            if hasattr(response, 'analysis'):
                return response.analysis
            return None
        except GeminiUnavailableError:
            return None
    
    def _generate_constitutional_documentation(self, 
                                             specification: Dict[str, Any],
                                             code: str,
                                             constitutional_analysis: Dict[str, Any],
                                             validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate constitutional documentation for the implemented code"""
        return {
            "constitutional_principles": [p.statement for p in self.blueprint.core_principles],
            "implementation_purpose": specification.get("description", "Constitutional implementation"),
            "constitutional_alignment": constitutional_analysis.get("constitutional_alignment", ""),
            "validation_status": "CONSTITUTIONAL" if validation_result["is_constitutional"] else "NON_CONSTITUTIONAL",
            "constitutional_safeguards": [
                "Built-in constitutional compliance checks",
                "UBOS principle documentation",
                "Constitutional error handling"
            ],
            "usage_guidelines": [
                "Use this code in accordance with UBOS principles",
                "Maintain constitutional compliance during modifications",
                "Document any changes with constitutional justification"
            ]
        }
    
    def review_implementation(self, 
                            code: str, 
                            language: str = "Python",
                            focus_areas: List[str] = None) -> Dict[str, Any]:
        """Review implementation for constitutional compliance and quality"""
        if focus_areas is None:
            focus_areas = ["constitutional_compliance", "code_quality", "security"]
        
        return self.constitutional_validator.validate_code(
            code=code,
            language=language,
            constitutional_requirements=["Blueprint Thinking", "Systems Over Willpower"],
            specification={"name": "code_review", "description": "Implementation review"}
        )
    
    def enhance_implementation(self, 
                             code: str, 
                             enhancement_requirements: List[str],
                             language: str = "Python") -> Dict[str, Any]:
        """Enhance existing implementation with constitutional improvements"""
        # This would use Codex CLI to enhance the code
        try:
            enhanced_code = self.codex_wrapper.enhance_code(
                code=code,
                enhancement_requirements=enhancement_requirements,
                language=language
            )
            
            # Validate enhanced code
            validation_result = self.constitutional_validator.validate_code(
                code=enhanced_code,
                language=language,
                constitutional_requirements=["Blueprint Thinking", "Systems Over Willpower"],
                specification={"name": "enhancement", "description": "Code enhancement"}
            )
            
            return {
                "status": "success",
                "enhanced_code": enhanced_code,
                "validation_result": validation_result,
                "enhancement_metadata": {
                    "enhanced_at": datetime.now(timezone.utc).isoformat(),
                    "constitutional_framework": "UBOS_v1.0"
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Enhancement failed: {e}",
                "enhanced_code": None
            }
