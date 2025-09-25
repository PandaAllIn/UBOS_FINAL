#!/usr/bin/env python3
"""
Real Codex CLI Wrapper for UBOS Implementation Agent

This module provides a real implementation that interfaces with the actual Codex CLI
for generating constitutionally compliant code.
"""

import os
import subprocess
import json
import tempfile
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timezone

class RealCodexWrapper:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
        self.setup_environment()

    def setup_environment(self):
        """Configure environment for Codex CLI usage"""
        os.environ['OPENAI_API_KEY'] = self.api_key

    def generate_code(self, 
                     prompt: str, 
                     context: Dict[str, Any] = None,
                     constitutional_principles: List[str] = None) -> Dict[str, Any]:
        """
        Generate code using the real Codex CLI with constitutional compliance
        
        Args:
            prompt: The code generation prompt
            context: Additional context for the generation
            constitutional_principles: List of UBOS constitutional principles to follow
            
        Returns:
            Dictionary containing generated code and metadata
        """
        try:
            # Prepare constitutional context
            constitutional_context = self._prepare_constitutional_context(
                prompt, context, constitutional_principles
            )
            
            # Create temporary file for the prompt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(constitutional_context)
                temp_file = f.name
            
            try:
                # Call Codex CLI
                result = subprocess.run([
                    'codex', 'generate', 
                    '--file', temp_file,
                    '--format', 'json',
                    '--max-tokens', '4000'
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    response_data = json.loads(result.stdout)
                    return self._format_response(response_data, constitutional_principles)
                else:
                    return {
                        'success': False,
                        'error': result.stderr,
                        'code': '',
                        'metadata': {
                            'timestamp': datetime.now(timezone.utc).isoformat(),
                            'constitutional_principles': constitutional_principles or []
                        }
                    }
                    
            finally:
                # Clean up temporary file
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Codex CLI request timed out',
                'code': '',
                'metadata': {
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'constitutional_principles': constitutional_principles or []
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'code': '',
                'metadata': {
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'constitutional_principles': constitutional_principles or []
                }
            }

    def _prepare_constitutional_context(self, 
                                      prompt: str, 
                                      context: Dict[str, Any] = None,
                                      constitutional_principles: List[str] = None) -> str:
        """Prepare the prompt with constitutional compliance context"""
        
        constitutional_principles = constitutional_principles or [
            "Blueprint Thinking",
            "Systems Over Willpower", 
            "Strategic Pause",
            "Abundance Mindset"
        ]
        
        context_str = ""
        if context:
            context_str = f"\n\nContext:\n{json.dumps(context, indent=2)}"
        
        constitutional_context = f"""
UBOS Constitutional Code Generation

Constitutional Principles to Follow:
{chr(10).join(f"- {principle}" for principle in constitutional_principles)}

Code Generation Requirements:
1. Follow clean code principles
2. Include comprehensive error handling
3. Add detailed documentation
4. Implement proper logging
5. Ensure scalability and maintainability
6. Follow UBOS constitutional principles

Original Prompt:
{prompt}{context_str}

Please generate constitutionally compliant code that follows all the above principles.
"""
        return constitutional_context

    def _format_response(self, response_data: Dict[str, Any], 
                        constitutional_principles: List[str] = None) -> Dict[str, Any]:
        """Format the Codex response with constitutional compliance metadata"""
        
        return {
            'success': True,
            'code': response_data.get('code', ''),
            'metadata': {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'constitutional_principles': constitutional_principles or [],
                'codex_metadata': {
                    'model': response_data.get('model', 'unknown'),
                    'tokens_used': response_data.get('usage', {}).get('total_tokens', 0),
                    'finish_reason': response_data.get('finish_reason', 'unknown')
                }
            },
            'constitutional_compliance': {
                'principles_applied': constitutional_principles or [],
                'compliance_score': self._calculate_compliance_score(response_data.get('code', '')),
                'recommendations': self._generate_recommendations(response_data.get('code', ''))
            }
        }

    def _calculate_compliance_score(self, code: str) -> float:
        """Calculate a compliance score based on code quality indicators"""
        if not code:
            return 0.0
            
        score = 0.0
        total_checks = 6
        
        # Check for documentation
        if '"""' in code or "'''" in code or '#' in code:
            score += 1.0
            
        # Check for error handling
        if any(keyword in code for keyword in ['try:', 'except:', 'raise', 'error']):
            score += 1.0
            
        # Check for logging
        if any(keyword in code.lower() for keyword in ['log', 'print', 'debug']):
            score += 1.0
            
        # Check for type hints
        if '->' in code or ': ' in code:
            score += 1.0
            
        # Check for class structure
        if 'class ' in code or 'def ' in code:
            score += 1.0
            
        # Check for imports
        if 'import ' in code:
            score += 1.0
            
        return score / total_checks

    def _generate_recommendations(self, code: str) -> List[str]:
        """Generate recommendations for improving constitutional compliance"""
        recommendations = []
        
        if not code:
            return ["No code generated - check prompt and try again"]
            
        if '"""' not in code and "'''" not in code:
            recommendations.append("Add comprehensive docstrings to all functions and classes")
            
        if 'try:' not in code:
            recommendations.append("Add proper error handling with try-except blocks")
            
        if 'log' not in code.lower():
            recommendations.append("Add logging for better debugging and monitoring")
            
        if '->' not in code:
            recommendations.append("Add type hints for better code clarity")
            
        return recommendations

    def validate_constitutional_compliance(self, code: str, 
                                         principles: List[str] = None) -> Dict[str, Any]:
        """Validate that generated code follows constitutional principles"""
        
        principles = principles or [
            "Blueprint Thinking",
            "Systems Over Willpower", 
            "Strategic Pause",
            "Abundance Mindset"
        ]
        
        compliance_results = {}
        
        for principle in principles:
            if principle == "Blueprint Thinking":
                compliance_results[principle] = {
                    'compliant': 'class ' in code or 'def ' in code,
                    'reason': 'Code should be well-structured with clear classes and functions'
                }
            elif principle == "Systems Over Willpower":
                compliance_results[principle] = {
                    'compliant': 'import ' in code and 'def ' in code,
                    'reason': 'Code should leverage existing systems and libraries'
                }
            elif principle == "Strategic Pause":
                compliance_results[principle] = {
                    'compliant': 'try:' in code or 'if ' in code,
                    'reason': 'Code should include strategic decision points and error handling'
                }
            elif principle == "Abundance Mindset":
                compliance_results[principle] = {
                    'compliant': 'def ' in code and 'return ' in code,
                    'reason': 'Code should be designed for scalability and reusability'
                }
        
        overall_compliance = all(result['compliant'] for result in compliance_results.values())
        
        return {
            'overall_compliance': overall_compliance,
            'principle_results': compliance_results,
            'compliance_score': sum(1 for result in compliance_results.values() if result['compliant']) / len(principles),
            'recommendations': self._generate_recommendations(code)
        }
