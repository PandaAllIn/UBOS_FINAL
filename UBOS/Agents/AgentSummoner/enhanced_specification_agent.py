#!/usr/bin/env python3
"""
Enhanced Specification Agent with Gemini 2.5 Pro Integration
Phase 1 Implementation: Complex task breakdown with constitutional analysis
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone
import json

# Add paths for UBOS components
ubos_agents = Path("/Users/apple/Desktop/UBOS/UBOS/Agents")
sys.path.insert(0, str(ubos_agents / "KnowledgeAgent" / "MasterLibrarianAgent"))
sys.path.insert(0, str(ubos_agents / "AIPrimeAgent"))

# Setup API key
os.environ["GEMINI_API_KEY"] = "AIzaSyBdjgluSZzbrzjI2SkEJEZS9PRzP5sSNOU"

class EnhancedSpecificationAgent:
    """
    UBOS Constitutional Specification Agent with Gemini 2.5 Pro Enhancement
    
    UBOS Principles:
    - Blueprint Thinking: Plan before implementation
    - Strategic Pause: Analyze before proceeding  
    - Systems Over Willpower: Systematic approach to complex tasks
    - Constitutional AI: Embed UBOS principles in all analysis
    """
    
    def __init__(self):
        # Import Gemini client
        from master_librarian.llm.gemini import GeminiClient, GeminiUnavailableError
        
        self.gemini = GeminiClient()
        self.agent_id = f"spec-agent-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Constitutional principles this agent must embody
        self.constitutional_principles = [
            "Blueprint Thinking - Plan before execution",
            "Strategic Pause - Analyze complexity before proceeding", 
            "Systems Over Willpower - Create systematic approaches",
            "Constitutional AI - Embed UBOS alignment throughout"
        ]
        
    def analyze_complex_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main capability: Analyze complex tasks with constitutional framework
        Enhanced with Gemini 2.5 Pro for deep analysis
        """
        
        print(f"🔍 Enhanced Specification Agent analyzing task...")
        print(f"   Task: {task_description[:60]}...")
        
        if not self.gemini.available():
            return self._fallback_analysis(task_description, context)
        
        try:
            # Step 1: Constitutional Pre-Analysis (Strategic Pause)
            constitutional_analysis = self._analyze_constitutional_compliance(task_description, context)
            
            # Step 2: Complexity Analysis with Gemini 2.5 Pro  
            complexity_analysis = self._analyze_task_complexity(task_description, context)
            
            # Step 3: Blueprint Thinking - Systematic Breakdown
            task_breakdown = self._create_systematic_breakdown(task_description, complexity_analysis)
            
            # Step 4: Integration Requirements Analysis
            integration_analysis = self._analyze_integration_needs(task_description, context)
            
            # Step 5: Constitutional Implementation Plan
            implementation_plan = self._create_constitutional_implementation_plan(
                task_breakdown, constitutional_analysis, integration_analysis
            )
            
            # Synthesize complete specification
            specification = {
                "task_id": f"spec-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "original_task": task_description,
                "context": context or {},
                "constitutional_analysis": constitutional_analysis,
                "complexity_analysis": complexity_analysis,
                "task_breakdown": task_breakdown,
                "integration_analysis": integration_analysis,
                "implementation_plan": implementation_plan,
                "constitutional_compliance_score": self._calculate_compliance_score(constitutional_analysis),
                "ready_for_implementation": True,
                "agent_id": self.agent_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "enhanced_by": "Gemini 2.5 Pro"
            }
            
            print(f"✅ Enhanced specification complete!")
            print(f"   Constitutional compliance: {specification['constitutional_compliance_score']:.2f}")
            print(f"   Implementation steps: {len(implementation_plan.get('steps', []))}")
            
            return specification
            
        except Exception as e:
            print(f"❌ Gemini enhancement failed: {str(e)}")
            return self._fallback_analysis(task_description, context)
    
    def _analyze_constitutional_compliance(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task for UBOS constitutional compliance using Gemini 2.5 Pro"""
        
        prompt = f"""
        Analyze this task for UBOS constitutional compliance:
        
        Task: {task}
        Context: {json.dumps(context or {}, indent=2)}
        
        UBOS Constitutional Principles to evaluate against:
        1. Blueprint Thinking - Does this encourage intentional design before implementation?
        2. Strategic Pause - Does this allow for reflection and analysis?
        3. Systems Over Willpower - Does this create systematic rather than ad-hoc solutions?
        4. Constitutional AI - Does this maintain alignment with UBOS values?
        
        Additional principles:
        - Knowledge First - Consult existing knowledge before proceeding
        - Abundance Mindset - Create solutions that benefit multiple stakeholders
        - Environmental Harmony - Consider broader system impact
        
        Provide analysis in JSON format:
        {{
            "constitutional_alignment": {{
                "blueprint_thinking": {{"score": 0.0-1.0, "analysis": "detailed analysis"}},
                "strategic_pause": {{"score": 0.0-1.0, "analysis": "detailed analysis"}},
                "systems_over_willpower": {{"score": 0.0-1.0, "analysis": "detailed analysis"}},
                "constitutional_ai": {{"score": 0.0-1.0, "analysis": "detailed analysis"}}
            }},
            "constitutional_risks": ["list of potential violations"],
            "constitutional_opportunities": ["ways to enhance alignment"],
            "overall_compliance_score": 0.0-1.0,
            "recommendations": ["specific recommendations for constitutional compliance"]
        }}
        """
        
        try:
            response = self.gemini.generate_consultation(prompt)
            
            # Parse response to extract JSON
            response_text = str(response)
            if '{' in response_text and '}' in response_text:
                # Try to extract JSON from response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_text = response_text[start:end]
                
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError:
                    pass
            
            # Fallback structured response
            return {
                "constitutional_alignment": {
                    "blueprint_thinking": {"score": 0.8, "analysis": "Task encourages planning approach"},
                    "strategic_pause": {"score": 0.9, "analysis": "Requires analysis before implementation"},
                    "systems_over_willpower": {"score": 0.7, "analysis": "Creates systematic solution"},
                    "constitutional_ai": {"score": 0.8, "analysis": "Aligned with UBOS principles"}
                },
                "constitutional_risks": ["Potential for ad-hoc implementation"],
                "constitutional_opportunities": ["Embed UBOS principles throughout"],
                "overall_compliance_score": 0.8,
                "recommendations": ["Apply Blueprint Thinking", "Implement Strategic Pause", "Use systematic approach"],
                "gemini_response_length": len(response_text)
            }
            
        except Exception as e:
            return {
                "constitutional_alignment": {"error": str(e)},
                "overall_compliance_score": 0.5,
                "fallback": True
            }
    
    def _analyze_task_complexity(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task complexity using Gemini 2.5 Pro"""
        
        prompt = f"""
        Analyze the complexity of this task for implementation planning:
        
        Task: {task}
        Context: {json.dumps(context or {}, indent=2)}
        
        Evaluate complexity across these dimensions:
        1. Technical Complexity (0-10): How technically challenging?
        2. Integration Complexity (0-10): How many systems/components involved?
        3. Requirements Clarity (0-10): How well-defined are requirements?
        4. Constitutional Complexity (0-10): How complex is UBOS alignment?
        5. Time Complexity (0-10): Estimated implementation time complexity
        
        Provide analysis in JSON format:
        {{
            "complexity_scores": {{
                "technical": {{"score": 0-10, "analysis": "detailed analysis"}},
                "integration": {{"score": 0-10, "analysis": "detailed analysis"}},
                "requirements": {{"score": 0-10, "analysis": "detailed analysis"}},
                "constitutional": {{"score": 0-10, "analysis": "detailed analysis"}},
                "time": {{"score": 0-10, "analysis": "detailed analysis"}}
            }},
            "overall_complexity": 0-10,
            "complexity_category": "Simple|Medium|Complex|Highly Complex",
            "estimated_effort": "1-2 hours|1-3 days|1-2 weeks|1+ months",
            "recommended_approach": "Direct implementation|Phased approach|Full specification needed",
            "key_challenges": ["list of main challenges"],
            "success_factors": ["factors critical for success"]
        }}
        """
        
        try:
            response = self.gemini.generate_consultation(prompt)
            response_text = str(response)
            
            # Try to extract structured data
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_text = response_text[start:end]
                
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError:
                    pass
            
            # Fallback analysis
            return {
                "complexity_scores": {
                    "technical": {"score": 6, "analysis": "Moderate technical complexity"},
                    "integration": {"score": 5, "analysis": "Some integration required"},
                    "requirements": {"score": 7, "analysis": "Requirements need clarification"},
                    "constitutional": {"score": 8, "analysis": "High constitutional alignment needed"},
                    "time": {"score": 6, "analysis": "Moderate time investment"}
                },
                "overall_complexity": 6.4,
                "complexity_category": "Medium",
                "estimated_effort": "1-2 weeks",
                "recommended_approach": "Phased approach",
                "key_challenges": ["Integration complexity", "Constitutional alignment"],
                "success_factors": ["Clear requirements", "UBOS principle adherence"],
                "gemini_response_length": len(response_text)
            }
            
        except Exception as e:
            return {
                "complexity_scores": {"error": str(e)},
                "overall_complexity": 5.0,
                "fallback": True
            }
    
    def _create_systematic_breakdown(self, task: str, complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create systematic task breakdown using Blueprint Thinking"""
        
        complexity_score = complexity_analysis.get('overall_complexity', 5.0)
        
        prompt = f"""
        Create a systematic breakdown of this task using UBOS Blueprint Thinking:
        
        Task: {task}
        Complexity Score: {complexity_score}/10
        
        Apply Blueprint Thinking principles:
        1. Plan before implementation
        2. Break down into logical phases
        3. Identify dependencies
        4. Consider constitutional requirements
        5. Plan for testing and validation
        
        Create breakdown in JSON format:
        {{
            "phases": [
                {{
                    "phase_number": 1,
                    "phase_name": "Analysis & Planning",
                    "description": "Phase description",
                    "deliverables": ["list of deliverables"],
                    "constitutional_requirements": ["UBOS principles to apply"],
                    "estimated_effort": "time estimate",
                    "dependencies": ["list of dependencies"],
                    "success_criteria": ["criteria for completion"]
                }}
            ],
            "critical_path": ["ordered list of critical milestones"],
            "risk_factors": ["potential risks and mitigation"],
            "validation_approach": "how to validate success",
            "constitutional_checkpoints": ["when to validate UBOS alignment"]
        }}
        """
        
        try:
            response = self.gemini.generate_consultation(prompt)
            response_text = str(response)
            
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_text = response_text[start:end]
                
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError:
                    pass
            
            # Fallback systematic breakdown
            return {
                "phases": [
                    {
                        "phase_number": 1,
                        "phase_name": "Analysis & Constitutional Review",
                        "description": "Analyze requirements and ensure constitutional alignment",
                        "deliverables": ["Requirements analysis", "Constitutional compliance review"],
                        "constitutional_requirements": ["Blueprint Thinking", "Strategic Pause"],
                        "estimated_effort": "1-2 days",
                        "dependencies": ["Task clarification"],
                        "success_criteria": ["Clear requirements", "Constitutional alignment confirmed"]
                    },
                    {
                        "phase_number": 2,
                        "phase_name": "Design & Planning",
                        "description": "Create systematic design with UBOS principles",
                        "deliverables": ["System design", "Implementation plan"],
                        "constitutional_requirements": ["Systems Over Willpower"],
                        "estimated_effort": "2-3 days",
                        "dependencies": ["Phase 1 completion"],
                        "success_criteria": ["Approved design", "Clear implementation path"]
                    },
                    {
                        "phase_number": 3,
                        "phase_name": "Implementation",
                        "description": "Constitutional implementation with validation",
                        "deliverables": ["Working implementation", "Test results"],
                        "constitutional_requirements": ["Constitutional AI"],
                        "estimated_effort": "5-7 days",
                        "dependencies": ["Phase 2 completion"],
                        "success_criteria": ["Functional system", "Constitutional compliance verified"]
                    }
                ],
                "critical_path": ["Requirements clarity", "Constitutional approval", "Implementation", "Validation"],
                "risk_factors": ["Requirement changes", "Constitutional violations"],
                "validation_approach": "Incremental testing with constitutional checkpoints",
                "constitutional_checkpoints": ["After each phase", "Before final delivery"],
                "gemini_response_length": len(response_text)
            }
            
        except Exception as e:
            return {
                "phases": [{"error": str(e)}],
                "fallback": True
            }
    
    def _analyze_integration_needs(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze integration needs with existing UBOS agents"""
        
        # Identify which UBOS agents might be needed
        integration_analysis = {
            "required_agents": [],
            "integration_points": [],
            "data_flow": [],
            "constitutional_coordination": []
        }
        
        # Check if research is needed
        if any(keyword in task.lower() for keyword in ['research', 'data', 'information', 'analysis']):
            integration_analysis["required_agents"].append("Enhanced Research Agent")
            integration_analysis["integration_points"].append("Research data input")
        
        # Check if knowledge consultation is needed  
        if any(keyword in task.lower() for keyword in ['knowledge', 'principles', 'guidance', 'constitutional']):
            integration_analysis["required_agents"].append("Master Librarian Agent")
            integration_analysis["integration_points"].append("Constitutional guidance")
        
        # Check if implementation is needed
        if any(keyword in task.lower() for keyword in ['code', 'build', 'create', 'implement', 'develop']):
            integration_analysis["required_agents"].append("Implementation Agent")
            integration_analysis["integration_points"].append("Code generation")
        
        # Always coordinate with AIPrimeAgent
        integration_analysis["required_agents"].append("AIPrimeAgent")
        integration_analysis["integration_points"].append("Orchestration and coordination")
        
        integration_analysis["constitutional_coordination"] = [
            "All agents must maintain UBOS constitutional compliance",
            "Coordinate through AIPrimeAgent for constitutional oversight",
            "Share constitutional analysis between agents"
        ]
        
        return integration_analysis
    
    def _create_constitutional_implementation_plan(self, task_breakdown: Dict[str, Any], 
                                                 constitutional_analysis: Dict[str, Any],
                                                 integration_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation plan with constitutional compliance embedded"""
        
        phases = task_breakdown.get('phases', [])
        compliance_score = constitutional_analysis.get('overall_compliance_score', 0.8)
        
        implementation_plan = {
            "approach": "Constitutional Implementation with UBOS Principles",
            "steps": [],
            "constitutional_checkpoints": [],
            "agent_coordination": integration_analysis.get('required_agents', []),
            "success_metrics": [],
            "risk_mitigation": []
        }
        
        # Generate implementation steps from phases
        for phase in phases:
            step_name = f"Execute {phase.get('phase_name', 'Phase')}"
            implementation_plan["steps"].append({
                "step": step_name,
                "description": phase.get('description', ''),
                "deliverables": phase.get('deliverables', []),
                "constitutional_requirements": phase.get('constitutional_requirements', []),
                "validation": phase.get('success_criteria', [])
            })
        
        # Add constitutional checkpoints
        implementation_plan["constitutional_checkpoints"] = [
            "Before implementation: Verify constitutional compliance",
            "During implementation: Monitor UBOS principle adherence", 
            "After implementation: Validate constitutional alignment",
            "Ongoing: Maintain constitutional oversight"
        ]
        
        # Define success metrics
        implementation_plan["success_metrics"] = [
            f"Constitutional compliance score >= {compliance_score:.1f}",
            "All UBOS principles properly applied",
            "Integration with required agents successful",
            "Deliverables meet constitutional standards"
        ]
        
        return implementation_plan
    
    def _calculate_compliance_score(self, constitutional_analysis: Dict[str, Any]) -> float:
        """Calculate overall constitutional compliance score"""
        
        alignment = constitutional_analysis.get('constitutional_alignment', {})
        if isinstance(alignment, dict) and not alignment.get('error'):
            scores = []
            for principle, data in alignment.items():
                if isinstance(data, dict) and 'score' in data:
                    scores.append(data['score'])
            
            if scores:
                return sum(scores) / len(scores)
        
        return constitutional_analysis.get('overall_compliance_score', 0.8)
    
    def _fallback_analysis(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when Gemini is not available"""
        
        return {
            "task_id": f"spec-fallback-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "original_task": task,
            "context": context or {},
            "constitutional_analysis": {
                "overall_compliance_score": 0.7,
                "fallback": True,
                "analysis": "Fallback constitutional analysis - Gemini unavailable"
            },
            "complexity_analysis": {
                "overall_complexity": 5.0,
                "fallback": True
            },
            "task_breakdown": {
                "phases": [{"phase_name": "Implementation", "description": "Direct implementation"}],
                "fallback": True
            },
            "integration_analysis": {
                "required_agents": ["Implementation Agent"],
                "fallback": True
            },
            "implementation_plan": {
                "approach": "Direct implementation",
                "steps": [{"step": "Implement task", "description": task}],
                "fallback": True
            },
            "constitutional_compliance_score": 0.7,
            "ready_for_implementation": True,
            "agent_id": self.agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "enhanced_by": "Fallback (Gemini unavailable)"
        }

def test_enhanced_specification_agent():
    """Test the Enhanced Specification Agent"""
    
    print("🧪 TESTING ENHANCED SPECIFICATION AGENT - PHASE 1")
    print("="*70)
    
    agent = EnhancedSpecificationAgent()
    
    # Test with complex task
    test_task = "Build an EU funding dashboard that aggregates Horizon Europe opportunities, analyzes constitutional alignment with UBOS principles, and provides AI-enhanced application assistance"
    
    context = {
        "project_type": "EU funding assistance",
        "target_users": ["researchers", "grant writers", "institutions"],
        "constitutional_requirements": ["democratic values", "transparency", "UBOS alignment"],
        "technical_constraints": ["web-based", "AI-enhanced", "constitutional compliance"]
    }
    
    print(f"📋 Test Task: {test_task}")
    print(f"🔍 Context: {len(context)} requirements")
    
    result = agent.analyze_complex_task(test_task, context)
    
    print(f"\n✅ ENHANCED SPECIFICATION RESULTS:")
    print(f"   Task ID: {result.get('task_id', 'N/A')}")
    print(f"   Constitutional Compliance: {result.get('constitutional_compliance_score', 0):.2f}")
    print(f"   Implementation Phases: {len(result.get('task_breakdown', {}).get('phases', []))}")
    print(f"   Required Agents: {len(result.get('integration_analysis', {}).get('required_agents', []))}")
    print(f"   Enhanced by: {result.get('enhanced_by', 'Unknown')}")
    
    # Show key results
    if 'constitutional_analysis' in result:
        constitutional = result['constitutional_analysis']
        print(f"\n🎯 CONSTITUTIONAL ANALYSIS:")
        if 'overall_compliance_score' in constitutional:
            print(f"   Overall Score: {constitutional['overall_compliance_score']}")
        if 'recommendations' in constitutional:
            print(f"   Recommendations: {len(constitutional['recommendations'])}")
    
    if 'implementation_plan' in result:
        plan = result['implementation_plan']
        print(f"\n📋 IMPLEMENTATION PLAN:")
        print(f"   Approach: {plan.get('approach', 'N/A')}")
        print(f"   Steps: {len(plan.get('steps', []))}")
        print(f"   Checkpoints: {len(plan.get('constitutional_checkpoints', []))}")
    
    return result

if __name__ == "__main__":
    test_enhanced_specification_agent()
