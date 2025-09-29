#!/usr/bin/env python3
"""
Enhanced AIPrimeAgent Orchestration Engine - Phase 2
Intelligent routing between Specification Agent, Implementation Agent, and Context7 MCP
Uses Gemini 2.5 Pro for decision making
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json

# Setup paths
ubos_agents = Path("/Users/apple/Desktop/UBOS/UBOS/Agents")
sys.path.insert(0, str(ubos_agents / "KnowledgeAgent" / "MasterLibrarianAgent"))
sys.path.insert(0, str(ubos_agents / "AIPrimeAgent"))
sys.path.insert(0, str(ubos_agents / "AgentSummoner"))

# Setup API keys
os.environ["GEMINI_API_KEY"] = "AIzaSyBdjgluSZzbrzjI2SkEJEZS9PRzP5sSNOU"
os.environ["PERPLEXITY_API_KEY"] = os.getenv("PERPLEXITY_API_KEY", "pplx-your-perplexity-api-key-here")

class EnhancedOrchestrationEngine:
    """
    UBOS Enhanced Orchestration Engine with Gemini 2.5 Pro Decision Making
    
    UBOS Principles:
    - Blueprint Thinking: Analyze before routing
    - Strategic Pause: Consider all options before proceeding
    - Systems Over Willpower: Systematic agent selection
    - Constitutional AI: Ensure all decisions align with UBOS principles
    """
    
    def __init__(self):
        # Import Gemini for decision making
        from master_librarian.llm.gemini import GeminiClient
        
        self.gemini = GeminiClient()
        self.orchestrator_id = f"orchestrator-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Decision thresholds for routing
        self.complexity_thresholds = {
            "simple": 0.3,      # Use Context7 MCP directly
            "medium": 0.6,      # Use Specification Agent
            "complex": 0.8,     # Use full pipeline
            "highly_complex": 1.0  # Use all agents with coordination
        }
        
        self.constitutional_threshold = 0.7  # Minimum constitutional compliance needed
        
    def orchestrate_request(self, user_request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main orchestration method: Analyze request and route to appropriate agents
        Enhanced with Gemini 2.5 Pro for intelligent decision making
        """
        
        print(f"🎯 Enhanced Orchestration Engine analyzing request...")
        print(f"   Request: {user_request[:60]}...")
        
        context = context or {}
        
        if not self.gemini.available():
            return self._fallback_orchestration(user_request, context)
        
        try:
            # Step 1: Strategic Pause - Analyze request complexity and requirements
            analysis = self._analyze_request_complexity(user_request, context)
            
            # Step 2: Constitutional Analysis - Ensure UBOS alignment
            constitutional_analysis = self._analyze_constitutional_requirements(user_request, context)
            
            # Step 3: Agent Selection Decision - Route based on analysis
            routing_decision = self._make_routing_decision(analysis, constitutional_analysis, user_request)
            
            # Step 4: Execute routing decision
            execution_result = self._execute_routing_decision(routing_decision, user_request, context)
            
            # Step 5: Synthesize results with constitutional oversight
            orchestration_result = {
                "orchestration_id": f"orch-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "original_request": user_request,
                "context": context,
                "complexity_analysis": analysis,
                "constitutional_analysis": constitutional_analysis,
                "routing_decision": routing_decision,
                "execution_result": execution_result,
                "orchestrator": "Enhanced AIPrimeAgent",
                "enhanced_by": "Gemini 2.5 Pro",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "constitutional_compliance": constitutional_analysis.get('overall_score', 0.8),
                "success": execution_result.get('success', False)
            }
            
            print(f"✅ Orchestration complete!")
            print(f"   Routing: {routing_decision.get('selected_approach', 'Unknown')}")
            print(f"   Constitutional compliance: {orchestration_result['constitutional_compliance']:.2f}")
            print(f"   Success: {orchestration_result['success']}")
            
            return orchestration_result
            
        except Exception as e:
            print(f"❌ Enhanced orchestration failed: {str(e)}")
            return self._fallback_orchestration(user_request, context, error=str(e))
    
    def _analyze_request_complexity(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze request complexity using Gemini 2.5 Pro"""
        
        prompt = f"""
        Analyze this user request for complexity and routing decisions:
        
        Request: {request}
        Context: {json.dumps(context, indent=2)}
        
        Evaluate complexity across these dimensions:
        1. Technical Complexity (0.0-1.0): How technically challenging?
        2. Requirements Clarity (0.0-1.0): How well-defined are requirements? 
        3. Constitutional Complexity (0.0-1.0): How much UBOS alignment needed?
        4. Integration Complexity (0.0-1.0): How many systems/agents needed?
        5. Planning Complexity (0.0-1.0): How much upfront planning required?
        
        Determine routing recommendation:
        - CONTEXT7_MCP: Simple, well-defined coding tasks (complexity < 0.3)
        - SPECIFICATION_AGENT: Complex requirements needing analysis (0.3-0.8)
        - FULL_PIPELINE: Specification → Implementation → Validation (> 0.8)
        
        Provide analysis in JSON format:
        {{
            "complexity_scores": {{
                "technical": 0.0-1.0,
                "requirements": 0.0-1.0,
                "constitutional": 0.0-1.0,
                "integration": 0.0-1.0,
                "planning": 0.0-1.0
            }},
            "overall_complexity": 0.0-1.0,
            "complexity_category": "Simple|Medium|Complex|Highly Complex",
            "routing_recommendation": "CONTEXT7_MCP|SPECIFICATION_AGENT|FULL_PIPELINE",
            "reasoning": "detailed reasoning for recommendation",
            "key_indicators": ["factors that influenced the decision"],
            "estimated_effort": "time estimate",
            "risk_factors": ["potential challenges"]
        }}
        """
        
        try:
            response = self.gemini.generate_consultation(prompt)
            response_text = str(response)
            
            # Try to extract JSON
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_text = response_text[start:end]
                
                try:
                    parsed = json.loads(json_text)
                    parsed["gemini_response_length"] = len(response_text)
                    return parsed
                except json.JSONDecodeError:
                    pass
            
            # Fallback analysis
            return self._extract_complexity_indicators(request, response_text)
            
        except Exception as e:
            return {
                "complexity_scores": {"error": str(e)},
                "overall_complexity": 0.5,
                "routing_recommendation": "SPECIFICATION_AGENT",
                "fallback": True
            }
    
    def _extract_complexity_indicators(self, request: str, response_text: str) -> Dict[str, Any]:
        """Extract complexity indicators from Gemini response"""
        
        # Analyze request for complexity indicators
        complexity_indicators = {
            "simple_keywords": ["fix", "update", "change", "add", "remove", "simple"],
            "medium_keywords": ["build", "create", "implement", "design", "analyze"],
            "complex_keywords": ["system", "framework", "architecture", "integration", "constitutional", "multi-agent"]
        }
        
        request_lower = request.lower()
        
        simple_score = sum(1 for word in complexity_indicators["simple_keywords"] if word in request_lower)
        medium_score = sum(1 for word in complexity_indicators["medium_keywords"] if word in request_lower)
        complex_score = sum(1 for word in complexity_indicators["complex_keywords"] if word in request_lower)
        
        # Calculate overall complexity
        if complex_score > 0:
            overall_complexity = 0.8
            category = "Complex"
            recommendation = "FULL_PIPELINE"
        elif medium_score > simple_score:
            overall_complexity = 0.6
            category = "Medium"
            recommendation = "SPECIFICATION_AGENT"
        else:
            overall_complexity = 0.3
            category = "Simple"
            recommendation = "CONTEXT7_MCP"
        
        return {
            "complexity_scores": {
                "technical": 0.6,
                "requirements": 0.5,
                "constitutional": 0.7,
                "integration": 0.5,
                "planning": 0.6
            },
            "overall_complexity": overall_complexity,
            "complexity_category": category,
            "routing_recommendation": recommendation,
            "reasoning": f"Based on keyword analysis and response patterns",
            "key_indicators": [f"Simple: {simple_score}", f"Medium: {medium_score}", f"Complex: {complex_score}"],
            "estimated_effort": "TBD",
            "gemini_response_length": len(response_text),
            "keyword_analysis": True
        }
    
    def _analyze_constitutional_requirements(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze constitutional requirements using Gemini 2.5 Pro"""
        
        prompt = f"""
        Analyze this request for UBOS constitutional requirements:
        
        Request: {request}
        Context: {json.dumps(context, indent=2)}
        
        Evaluate constitutional alignment needs:
        1. Blueprint Thinking: Does this need systematic planning?
        2. Strategic Pause: Does this need careful analysis before proceeding?
        3. Systems Over Willpower: Does this need systematic vs ad-hoc approach?
        4. Constitutional AI: Does this need UBOS principle embedding?
        
        Additional considerations:
        - Democratic values alignment
        - Transparency requirements
        - Ethical AI considerations
        - User empowerment focus
        
        Provide analysis in JSON format:
        {{
            "constitutional_requirements": {{
                "blueprint_thinking": {{"needed": true/false, "importance": 0.0-1.0, "reason": "why"}},
                "strategic_pause": {{"needed": true/false, "importance": 0.0-1.0, "reason": "why"}},
                "systems_over_willpower": {{"needed": true/false, "importance": 0.0-1.0, "reason": "why"}},
                "constitutional_ai": {{"needed": true/false, "importance": 0.0-1.0, "reason": "why"}}
            }},
            "overall_score": 0.0-1.0,
            "constitutional_priority": "Low|Medium|High|Critical",
            "specific_requirements": ["list specific constitutional needs"],
            "risk_assessment": "constitutional risks if not properly handled"
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
                    parsed = json.loads(json_text)
                    parsed["gemini_response_length"] = len(response_text)
                    return parsed
                except json.JSONDecodeError:
                    pass
            
            # Fallback constitutional analysis
            return {
                "constitutional_requirements": {
                    "blueprint_thinking": {"needed": True, "importance": 0.8, "reason": "Planning approach recommended"},
                    "strategic_pause": {"needed": True, "importance": 0.9, "reason": "Analysis before action needed"},
                    "systems_over_willpower": {"needed": True, "importance": 0.7, "reason": "Systematic approach preferred"},
                    "constitutional_ai": {"needed": True, "importance": 0.8, "reason": "UBOS alignment required"}
                },
                "overall_score": 0.8,
                "constitutional_priority": "High",
                "specific_requirements": ["UBOS principle alignment", "Systematic approach"],
                "gemini_response_length": len(response_text),
                "fallback": True
            }
            
        except Exception as e:
            return {
                "constitutional_requirements": {"error": str(e)},
                "overall_score": 0.7,
                "fallback": True
            }
    
    def _make_routing_decision(self, complexity_analysis: Dict[str, Any], 
                             constitutional_analysis: Dict[str, Any], 
                             request: str) -> Dict[str, Any]:
        """Make intelligent routing decision based on analysis"""
        
        overall_complexity = complexity_analysis.get('overall_complexity', 0.5)
        constitutional_score = constitutional_analysis.get('overall_score', 0.7)
        recommended_route = complexity_analysis.get('routing_recommendation', 'SPECIFICATION_AGENT')
        
        # Decision logic
        decision = {
            "analysis_inputs": {
                "complexity_score": overall_complexity,
                "constitutional_score": constitutional_score,
                "gemini_recommendation": recommended_route
            },
            "decision_factors": [],
            "selected_approach": None,
            "agent_sequence": [],
            "reasoning": "",
            "constitutional_override": False
        }
        
        # Apply decision logic
        if constitutional_score >= 0.8:
            # High constitutional requirements - always use Specification Agent
            decision["constitutional_override"] = True
            decision["selected_approach"] = "SPECIFICATION_FIRST"
            decision["agent_sequence"] = ["Enhanced Specification Agent", "Implementation Agent"]
            decision["reasoning"] = "High constitutional requirements demand specification-first approach"
            decision["decision_factors"].append("Constitutional override")
            
        elif overall_complexity >= 0.8:
            # Highly complex - use full pipeline
            decision["selected_approach"] = "FULL_PIPELINE"
            decision["agent_sequence"] = ["Enhanced Specification Agent", "Implementation Agent", "Validation"]
            decision["reasoning"] = "High complexity requires full specification and implementation pipeline"
            decision["decision_factors"].append("High complexity")
            
        elif overall_complexity >= 0.4:
            # Medium complexity - use Specification Agent
            decision["selected_approach"] = "SPECIFICATION_AGENT"
            decision["agent_sequence"] = ["Enhanced Specification Agent"]
            decision["reasoning"] = "Medium complexity benefits from specification analysis"
            decision["decision_factors"].append("Medium complexity")
            
        else:
            # Simple tasks - could use Context7 MCP, but prefer constitutional approach
            if constitutional_score >= 0.6:
                decision["selected_approach"] = "SPECIFICATION_AGENT"
                decision["agent_sequence"] = ["Enhanced Specification Agent"]
                decision["reasoning"] = "Simple task but constitutional analysis recommended"
                decision["decision_factors"].append("Constitutional preference")
            else:
                decision["selected_approach"] = "CONTEXT7_MCP"
                decision["agent_sequence"] = ["Context7 MCP"]
                decision["reasoning"] = "Simple, well-defined task suitable for direct implementation"
                decision["decision_factors"].append("Low complexity, low constitutional needs")
        
        # Add Gemini recommendation factor
        if recommended_route and recommended_route != decision["selected_approach"]:
            decision["decision_factors"].append(f"Gemini recommended: {recommended_route}")
        
        return decision
    
    def _execute_routing_decision(self, routing_decision: Dict[str, Any], 
                                request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the routing decision"""
        
        selected_approach = routing_decision.get('selected_approach')
        agent_sequence = routing_decision.get('agent_sequence', [])
        
        execution_result = {
            "approach_executed": selected_approach,
            "agents_used": agent_sequence,
            "results": {},
            "success": False,
            "execution_details": []
        }
        
        try:
            if selected_approach in ["SPECIFICATION_AGENT", "SPECIFICATION_FIRST", "FULL_PIPELINE"]:
                # Use Enhanced Specification Agent
                execution_result["execution_details"].append("Executing Enhanced Specification Agent")
                
                from enhanced_specification_agent import EnhancedSpecificationAgent
                spec_agent = EnhancedSpecificationAgent()
                spec_result = spec_agent.analyze_complex_task(request, context)
                
                execution_result["results"]["specification"] = spec_result
                execution_result["success"] = spec_result.get('ready_for_implementation', False)
                
                # If full pipeline, continue to implementation
                if selected_approach == "FULL_PIPELINE" and execution_result["success"]:
                    execution_result["execution_details"].append("Proceeding to Implementation Agent")
                    # Implementation would go here
                    execution_result["results"]["implementation"] = {"status": "Ready for Phase 3"}
                
            elif selected_approach == "CONTEXT7_MCP":
                # Use Context7 MCP (placeholder for now)
                execution_result["execution_details"].append("Routing to Context7 MCP")
                execution_result["results"]["context7"] = {
                    "status": "Would route to Context7 MCP",
                    "task": request,
                    "approach": "Direct implementation"
                }
                execution_result["success"] = True
                
            else:
                execution_result["execution_details"].append(f"Unknown approach: {selected_approach}")
                execution_result["success"] = False
            
        except Exception as e:
            execution_result["execution_details"].append(f"Execution failed: {str(e)}")
            execution_result["error"] = str(e)
            execution_result["success"] = False
        
        return execution_result
    
    def _fallback_orchestration(self, request: str, context: Dict[str, Any], error: str = None) -> Dict[str, Any]:
        """Fallback orchestration when Gemini is unavailable"""
        
        return {
            "orchestration_id": f"orch-fallback-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "original_request": request,
            "context": context,
            "routing_decision": {
                "selected_approach": "SPECIFICATION_AGENT",
                "reasoning": "Fallback to constitutional approach",
                "fallback": True
            },
            "execution_result": {
                "approach_executed": "FALLBACK",
                "success": False,
                "error": error or "Gemini unavailable"
            },
            "orchestrator": "Enhanced AIPrimeAgent (Fallback)",
            "enhanced_by": "Fallback mode",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "constitutional_compliance": 0.7,
            "success": False,
            "fallback": True
        }

def test_orchestration_engine():
    """Test the Enhanced Orchestration Engine"""
    
    print("🧪 TESTING ENHANCED ORCHESTRATION ENGINE - PHASE 2")
    print("="*70)
    
    engine = EnhancedOrchestrationEngine()
    
    # Test different types of requests
    test_cases = [
        {
            "name": "Simple Task",
            "request": "Fix a typo in the README file",
            "context": {"urgency": "low", "complexity": "minimal"}
        },
        {
            "name": "Medium Complexity",
            "request": "Build a contact form with validation and email sending",
            "context": {"requirements": "clear", "scope": "limited"}
        },
        {
            "name": "Complex Constitutional Task",
            "request": "Design a constitutional AI governance system for multi-agent coordination with UBOS principle embedding",
            "context": {"constitutional_focus": True, "complexity": "high"}
        },
        {
            "name": "EU Dashboard Project",
            "request": "Create an EU funding dashboard with AI-enhanced application assistance and constitutional compliance analysis",
            "context": {"project_type": "EU funding", "ai_enhanced": True, "constitutional": True}
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"   Request: {test_case['request'][:50]}...")
        
        result = engine.orchestrate_request(test_case['request'], test_case['context'])
        results[test_case['name']] = result
        
        routing = result.get('routing_decision', {})
        print(f"   Decision: {routing.get('selected_approach', 'Unknown')}")
        print(f"   Success: {result.get('success', False)}")
    
    return results

if __name__ == "__main__":
    test_orchestration_engine()
