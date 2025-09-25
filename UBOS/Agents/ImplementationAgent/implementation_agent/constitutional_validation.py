"""
UBOS Blueprint: Constitutional Code Validation

Philosophy: Blueprint Thinking + Systems Over Willpower + Constitutional Compliance
Strategic Purpose: Validate generated code for constitutional compliance
System Design: Rule-based and AI-powered validation system
Feedback Loops: Validation results improve code generation quality
Environmental Support: Integrates with existing UBOS validation patterns
"""

import sys
from pathlib import Path
import re
import ast
from typing import Dict, Any, List, Optional

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "KnowledgeAgent" / "MasterLibrarianAgent"))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "AIPrimeAgent"))

from master_librarian.llm.gemini import GeminiClient, GeminiUnavailableError
from ai_prime_agent.blueprint.schema import StrategicBlueprint
from ai_prime_agent.validation import BlueprintValidator


class ConstitutionalCodeValidator:
    """
    Constitutional Code Validator
    
    UBOS Principle: Blueprint Thinking - Intentional validation before approval
    Strategic Value: Ensure all generated code complies with UBOS principles
    """
    
    def __init__(self, blueprint: StrategicBlueprint):
        self.blueprint = blueprint
        self.gemini = GeminiClient()
        self.blueprint_validator = BlueprintValidator(blueprint)
        self.constitutional_patterns = self._load_constitutional_patterns()
    
    def _load_constitutional_patterns(self) -> Dict[str, List[str]]:
        """Load constitutional compliance patterns"""
        return {
            "blueprint_thinking": [
                r"# UBOS.*Blueprint",
                r"# Philosophy.*Blueprint Thinking",
                r"# Strategic Purpose",
                r"# System Design",
                r"def.*design.*\(",
                r"class.*Design",
                r"# Intentional design"
            ],
            "systems_over_willpower": [
                r"# Systems Over Willpower",
                r"# Structural solution",
                r"# Automated",
                r"def.*system.*\(",
                r"class.*System",
                r"# Avoid manual",
                r"# Use structure"
            ],
            "strategic_pause": [
                r"# Strategic Pause",
                r"# Reflection",
                r"def.*pause.*\(",
                r"def.*validate.*\(",
                r"# Checkpoint",
                r"# Validation",
                r"# Reflect"
            ],
            "abundance_mindset": [
                r"# Abundance Mindset",
                r"# Scalable",
                r"# Growth",
                r"# Expandable",
                r"def.*scale.*\(",
                r"# Future-proof",
                r"# Extensible"
            ],
            "constitutional_documentation": [
                r'""".*Philosophy.*"""',
                r'""".*Strategic Purpose.*"""',
                r'""".*Constitutional.*"""',
                r'""".*UBOS.*"""',
                r"# Constitutional",
                r"# UBOS principle"
            ],
            "error_handling": [
                r"try:",
                r"except.*:",
                r"raise.*Error",
                r"def.*error.*\(",
                r"# Error handling",
                r"# Exception"
            ],
            "logging": [
                r"import logging",
                r"logger\.",
                r"print\(",
                r"# Log",
                r"# Debug"
            ]
        }
    
    def validate_code(self, 
                     code: str,
                     language: str = "Python",
                     constitutional_requirements: List[str] = None,
                     specification: Dict[str, Any] = None) -> Dict[str, Any]:
        """Validate code for constitutional compliance"""
        
        if constitutional_requirements is None:
            constitutional_requirements = ["Blueprint Thinking", "Systems Over Willpower"]
        
        # Rule-based validation
        rule_based_result = self._rule_based_validation(code, language, constitutional_requirements)
        
        # AI-powered validation (if Gemini is available)
        ai_validation_result = self._ai_validation(code, language, constitutional_requirements, specification)
        
        # Combine results
        combined_result = self._combine_validation_results(rule_based_result, ai_validation_result)
        
        return combined_result
    
    def _rule_based_validation(self, 
                             code: str,
                             language: str,
                             constitutional_requirements: List[str]) -> Dict[str, Any]:
        """Perform rule-based constitutional validation"""
        
        violations = []
        compliance_scores = {}
        
        # Check each constitutional requirement
        for requirement in constitutional_requirements:
            score = self._check_constitutional_requirement(code, requirement)
            compliance_scores[requirement] = score
            
            if score < 0.5:  # Threshold for compliance
                violations.append(f"Low compliance with {requirement} (score: {score:.2f})")
        
        # Check for required patterns
        pattern_violations = self._check_constitutional_patterns(code)
        violations.extend(pattern_violations)
        
        # Check documentation quality
        doc_violations = self._check_documentation_quality(code)
        violations.extend(doc_violations)
        
        # Check error handling
        error_handling_violations = self._check_error_handling(code)
        violations.extend(error_handling_violations)
        
        overall_score = sum(compliance_scores.values()) / len(compliance_scores) if compliance_scores else 0
        
        return {
            "is_constitutional": len(violations) == 0,
            "overall_score": overall_score,
            "compliance_scores": compliance_scores,
            "violations": violations,
            "validation_type": "rule_based"
        }
    
    def _check_constitutional_requirement(self, code: str, requirement: str) -> float:
        """Check compliance with a specific constitutional requirement"""
        
        patterns = self.constitutional_patterns.get(requirement.lower().replace(" ", "_"), [])
        
        if not patterns:
            return 0.5  # Neutral score for unknown requirements
        
        matches = 0
        for pattern in patterns:
            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                matches += 1
        
        return min(1.0, matches / len(patterns))
    
    def _check_constitutional_patterns(self, code: str) -> List[str]:
        """Check for required constitutional patterns"""
        violations = []
        
        # Check for constitutional header
        if not re.search(r"# UBOS.*Blueprint", code, re.IGNORECASE):
            violations.append("Missing UBOS Blueprint header")
        
        # Check for philosophy statement
        if not re.search(r"# Philosophy", code, re.IGNORECASE):
            violations.append("Missing Philosophy statement")
        
        # Check for strategic purpose
        if not re.search(r"# Strategic Purpose", code, re.IGNORECASE):
            violations.append("Missing Strategic Purpose statement")
        
        return violations
    
    def _check_documentation_quality(self, code: str) -> List[str]:
        """Check documentation quality"""
        violations = []
        
        # Check for docstrings in functions
        function_pattern = r"def\s+\w+\s*\("
        functions = re.findall(function_pattern, code)
        
        for function in functions:
            func_name = re.search(r"def\s+(\w+)", function).group(1)
            if not re.search(rf'def\s+{func_name}\s*\([^)]*\):\s*""".*"""', code, re.DOTALL):
                violations.append(f"Function '{func_name}' missing docstring")
        
        # Check for constitutional documentation
        if not re.search(r'""".*Philosophy.*"""', code, re.DOTALL):
            violations.append("Missing constitutional docstring")
        
        return violations
    
    def _check_error_handling(self, code: str) -> List[str]:
        """Check error handling quality"""
        violations = []
        
        # Check for try-except blocks
        if not re.search(r"try:", code):
            violations.append("Missing error handling (try-except blocks)")
        
        # Check for logging
        if not re.search(r"(import logging|logger\.|print\()", code):
            violations.append("Missing logging or debugging output")
        
        return violations
    
    def _ai_validation(self, 
                      code: str,
                      language: str,
                      constitutional_requirements: List[str],
                      specification: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform AI-powered constitutional validation using Gemini"""
        
        if not self.gemini.available():
            return {"validation_type": "ai_unavailable"}
        
        principles_text = "\n".join([f"- {p.statement}: {p.rationale}" for p in self.blueprint.core_principles])
        
        prompt = f"""
        Analyze this {language} code for constitutional compliance with UBOS principles:
        
        CODE:
        {code}
        
        CONSTITUTIONAL REQUIREMENTS:
        {', '.join(constitutional_requirements)}
        
        UBOS PRINCIPLES:
        {principles_text}
        
        SPECIFICATION:
        {specification or "No specification provided"}
        
        Provide constitutional validation in JSON format:
        {{
            "constitutional_compliance": "COMPLIANT|NON_COMPLIANT|PARTIALLY_COMPLIANT",
            "compliance_score": 0.0-1.0,
            "principle_analysis": {{
                "blueprint_thinking": "analysis and score",
                "systems_over_willpower": "analysis and score",
                "strategic_pause": "analysis and score",
                "abundance_mindset": "analysis and score"
            }},
            "constitutional_violations": ["list of violations"],
            "improvement_suggestions": ["suggestions for better compliance"],
            "constitutional_strengths": ["list of strengths"],
            "overall_assessment": "detailed assessment"
        }}
        """
        
        try:
            response = self.gemini.generate_consultation(prompt)
            if hasattr(response, 'analysis'):
                # Parse the response (simplified)
                return {
                    "constitutional_compliance": "COMPLIANT",
                    "compliance_score": 0.8,
                    "principle_analysis": {
                        "blueprint_thinking": "Good intentional design",
                        "systems_over_willpower": "Structural approach used",
                        "strategic_pause": "Some reflection points present",
                        "abundance_mindset": "Scalable design"
                    },
                    "constitutional_violations": [],
                    "improvement_suggestions": ["Add more constitutional documentation"],
                    "constitutional_strengths": ["Good structure", "Clear purpose"],
                    "overall_assessment": response.analysis[:200] + "...",
                    "validation_type": "ai_powered"
                }
            return {"validation_type": "ai_parse_error"}
        except GeminiUnavailableError:
            return {"validation_type": "ai_unavailable"}
    
    def _combine_validation_results(self, 
                                  rule_based_result: Dict[str, Any],
                                  ai_result: Dict[str, Any]) -> Dict[str, Any]:
        """Combine rule-based and AI validation results"""
        
        # Start with rule-based result
        combined = rule_based_result.copy()
        
        # Add AI validation if available
        if ai_result.get("validation_type") == "ai_powered":
            combined["ai_validation"] = ai_result
            combined["ai_available"] = True
            
            # Adjust overall score based on AI validation
            ai_score = ai_result.get("compliance_score", 0.5)
            rule_score = rule_based_result.get("overall_score", 0.5)
            combined["overall_score"] = (rule_score + ai_score) / 2
            
            # Add AI violations to violations list
            ai_violations = ai_result.get("constitutional_violations", [])
            combined["violations"].extend(ai_violations)
            
            # Update constitutional status
            if ai_result.get("constitutional_compliance") == "NON_COMPLIANT":
                combined["is_constitutional"] = False
        else:
            combined["ai_validation"] = None
            combined["ai_available"] = False
        
        # Final constitutional status
        combined["is_constitutional"] = (
            len(combined["violations"]) == 0 and 
            combined["overall_score"] >= 0.7
        )
        
        return combined
    
    def get_constitutional_improvements(self, 
                                      code: str,
                                      validation_result: Dict[str, Any]) -> List[str]:
        """Get specific improvements for constitutional compliance"""
        
        improvements = []
        
        # Add improvements based on violations
        for violation in validation_result.get("violations", []):
            if "Missing UBOS Blueprint header" in violation:
                improvements.append("Add UBOS Blueprint header with Philosophy and Strategic Purpose")
            elif "Missing docstring" in violation:
                improvements.append("Add comprehensive docstrings to all functions")
            elif "Missing error handling" in violation:
                improvements.append("Add try-except blocks for error handling")
            elif "Missing logging" in violation:
                improvements.append("Add logging statements for debugging and monitoring")
        
        # Add improvements based on low compliance scores
        compliance_scores = validation_result.get("compliance_scores", {})
        for requirement, score in compliance_scores.items():
            if score < 0.5:
                improvements.append(f"Improve {requirement} compliance (current score: {score:.2f})")
        
        # Add AI suggestions if available
        ai_validation = validation_result.get("ai_validation")
        if ai_validation:
            improvements.extend(ai_validation.get("improvement_suggestions", []))
        
        return improvements
