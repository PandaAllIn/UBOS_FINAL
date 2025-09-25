"""
UBOS Blueprint: Codex CLI Wrapper

Philosophy: Systems Over Willpower + Constitutional Code
Strategic Purpose: Integrate Codex CLI with constitutional validation
System Design: Wrapper around Codex CLI with constitutional enhancements
Feedback Loops: Code generation feedback improves constitutional compliance
Environmental Support: Integrates with Codex CLI and constitutional validation
"""

import subprocess
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path


class CodexWrapper:
    """
    Codex CLI Wrapper with Constitutional Enhancements
    
    UBOS Principle: Systems Over Willpower - Automated code generation
    Strategic Value: Generate code using Codex CLI with constitutional oversight
    """
    
    def __init__(self):
        self.codex_path = self._find_codex_path()
        self.constitutional_prompts = self._load_constitutional_prompts()
    
    def _find_codex_path(self) -> str:
        """Find Codex CLI installation path"""
        # Check if codex is in PATH
        try:
            result = subprocess.run(['which', 'codex'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Check environment variable
        codex_path = os.getenv('CODEX_PATH')
        if codex_path and Path(codex_path).exists():
            return codex_path
        
        # Default fallback
        return 'codex'
    
    def _load_constitutional_prompts(self) -> Dict[str, str]:
        """Load constitutional prompts for code generation"""
        return {
            "constitutional_header": """
# UBOS Constitutional Code
# Philosophy: Blueprint Thinking + Systems Over Willpower
# Strategic Purpose: {purpose}
# Constitutional Compliance: {compliance_requirements}
# Generated: {timestamp}
""",
            "constitutional_docstring": '''
"""
Constitutional Implementation

Philosophy: {philosophy}
Strategic Purpose: {purpose}
Constitutional Requirements: {constitutional_requirements}
System Design: {system_design}
Feedback Loops: {feedback_loops}
Environmental Support: {environmental_support}
"""''',
            "constitutional_validation": """
# Constitutional Validation
def validate_constitutional_compliance():
    \"\"\"Validate that this code follows UBOS constitutional principles\"\"\"
    # Add constitutional compliance checks here
    pass
"""
        }
    
    def generate_code(self, 
                     specification: Dict[str, Any],
                     language: str = "Python",
                     constitutional_requirements: List[str] = None,
                     constitutional_analysis: Dict[str, Any] = None) -> str:
        """Generate code using Codex CLI with constitutional enhancements"""
        
        if constitutional_requirements is None:
            constitutional_requirements = ["Blueprint Thinking", "Systems Over Willpower"]
        
        # Build constitutional prompt
        constitutional_prompt = self._build_constitutional_prompt(
            specification, language, constitutional_requirements, constitutional_analysis
        )
        
        try:
            # Execute Codex CLI
            result = subprocess.run(
                [self.codex_path, constitutional_prompt],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                raise Exception(f"Codex CLI failed: {result.stderr}")
            
            generated_code = result.stdout.strip()
            
            # Add constitutional enhancements
            enhanced_code = self._add_constitutional_enhancements(
                generated_code, specification, constitutional_requirements
            )
            
            return enhanced_code
            
        except subprocess.TimeoutExpired:
            raise Exception("Codex CLI timeout - code generation took too long")
        except Exception as e:
            raise Exception(f"Code generation failed: {e}")
    
    def _build_constitutional_prompt(self, 
                                   specification: Dict[str, Any],
                                   language: str,
                                   constitutional_requirements: List[str],
                                   constitutional_analysis: Dict[str, Any] = None) -> str:
        """Build constitutional prompt for Codex CLI"""
        
        base_prompt = f"""
Generate {language} code for the following specification with constitutional compliance:

SPECIFICATION:
{json.dumps(specification, indent=2)}

CONSTITUTIONAL REQUIREMENTS:
{', '.join(constitutional_requirements)}

CONSTITUTIONAL GUIDANCE:
- Follow Blueprint Thinking: Design intentionally before implementing
- Apply Systems Over Willpower: Use structural solutions over manual approaches
- Include Strategic Pause: Add reflection points and validation
- Embrace Abundance Mindset: Build for growth and scalability

CODE REQUIREMENTS:
- Include comprehensive documentation
- Add constitutional compliance comments
- Implement error handling
- Follow {language} best practices
- Include type hints (if applicable)
- Add logging for debugging
"""
        
        if constitutional_analysis:
            base_prompt += f"\nCONSTITUTIONAL ANALYSIS:\n{json.dumps(constitutional_analysis, indent=2)}"
        
        return base_prompt
    
    def _add_constitutional_enhancements(self, 
                                       code: str,
                                       specification: Dict[str, Any],
                                       constitutional_requirements: List[str]) -> str:
        """Add constitutional enhancements to generated code"""
        
        # Add constitutional header
        header = self.constitutional_prompts["constitutional_header"].format(
            purpose=specification.get("description", "Constitutional implementation"),
            compliance_requirements=", ".join(constitutional_requirements),
            timestamp=os.popen('date').read().strip()
        )
        
        # Add constitutional docstring to main functions/classes
        enhanced_code = self._add_constitutional_docstrings(code, specification)
        
        # Add constitutional validation
        validation_code = self.constitutional_prompts["constitutional_validation"]
        
        # Combine all enhancements
        final_code = f"{header}\n\n{enhanced_code}\n\n{validation_code}"
        
        return final_code
    
    def _add_constitutional_docstrings(self, 
                                     code: str,
                                     specification: Dict[str, Any]) -> str:
        """Add constitutional docstrings to code"""
        # This is a simplified version - in practice, you'd parse the code
        # and add docstrings to functions and classes
        
        docstring_template = self.constitutional_prompts["constitutional_docstring"]
        
        # For now, just prepend a constitutional docstring
        constitutional_docstring = docstring_template.format(
            philosophy="Blueprint Thinking + Systems Over Willpower",
            purpose=specification.get("description", "Constitutional implementation"),
            constitutional_requirements="UBOS principles compliance",
            system_design="Constitutional code generation",
            feedback_loops="Constitutional validation and testing",
            environmental_support="Codex CLI integration"
        )
        
        return f"{constitutional_docstring}\n\n{code}"
    
    def enhance_code(self, 
                    code: str,
                    enhancement_requirements: List[str],
                    language: str = "Python") -> str:
        """Enhance existing code using Codex CLI"""
        
        enhancement_prompt = f"""
Enhance the following {language} code with these requirements:

CODE:
{code}

ENHANCEMENT REQUIREMENTS:
{', '.join(enhancement_requirements)}

CONSTITUTIONAL GUIDANCE:
- Maintain UBOS constitutional compliance
- Follow Blueprint Thinking principles
- Apply Systems Over Willpower approach
- Include proper documentation and error handling
"""
        
        try:
            result = subprocess.run(
                [self.codex_path, enhancement_prompt],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f"Codex CLI enhancement failed: {result.stderr}")
            
            return result.stdout.strip()
            
        except Exception as e:
            raise Exception(f"Code enhancement failed: {e}")
    
    def review_code(self, 
                   code: str,
                   language: str = "Python",
                   focus_areas: List[str] = None) -> Dict[str, Any]:
        """Review code using Codex CLI"""
        
        if focus_areas is None:
            focus_areas = ["constitutional_compliance", "code_quality", "security"]
        
        review_prompt = f"""
Review the following {language} code focusing on these areas:

CODE:
{code}

FOCUS AREAS:
{', '.join(focus_areas)}

CONSTITUTIONAL REQUIREMENTS:
- Blueprint Thinking compliance
- Systems Over Willpower application
- Strategic Pause implementation
- Abundance Mindset approach

Provide detailed feedback in JSON format:
{{
    "overall_quality": "assessment",
    "constitutional_compliance": "assessment",
    "security_issues": ["list of issues"],
    "improvement_suggestions": ["list of suggestions"],
    "code_quality_score": 0-10
}}
"""
        
        try:
            result = subprocess.run(
                [self.codex_path, review_prompt],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f"Codex CLI review failed: {result.stderr}")
            
            # Parse JSON response
            try:
                review_result = json.loads(result.stdout.strip())
                return review_result
            except json.JSONDecodeError:
                return {
                    "overall_quality": "Unable to parse review",
                    "constitutional_compliance": "Unknown",
                    "security_issues": [],
                    "improvement_suggestions": ["Review parsing failed"],
                    "code_quality_score": 5
                }
            
        except Exception as e:
            return {
                "overall_quality": f"Review failed: {e}",
                "constitutional_compliance": "Unknown",
                "security_issues": [],
                "improvement_suggestions": ["Review system unavailable"],
                "code_quality_score": 0
            }
