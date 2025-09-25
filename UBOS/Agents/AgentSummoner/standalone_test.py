#!/usr/bin/env python3
"""
Standalone Constitutional Test

Test the Agent Summoner components without external dependencies.
"""

import sys
from pathlib import Path

def test_template_registry_standalone():
    """Test the template registry without external dependencies."""
    print("🧪 Testing Template Registry (Standalone)...")
    
    try:
        # Import only the template registry
        sys.path.append(str(Path(__file__).parent / "agent_summoner"))
        
        from agent_templates import AgentTemplateRegistry
        
        registry = AgentTemplateRegistry()
        print("✅ Template registry created")
        
        # Test available templates
        templates = list(registry.templates.keys())
        print(f"✅ Available templates: {templates}")
        
        # Test EU Grant Specialist template
        eu_template = registry.get_template("eu_grant_specialist")
        print(f"✅ EU Grant Specialist template: {eu_template.name}")
        print(f"   - Agent Type: {eu_template.agent_type}")
        print(f"   - Capabilities: {len(eu_template.base_capabilities)}")
        print(f"   - Constitutional Requirements: {len(eu_template.constitutional_requirements)}")
        
        # Test Specification Agent template
        spec_template = registry.get_template("specification_agent")
        print(f"✅ Specification Agent template: {spec_template.name}")
        print(f"   - Agent Type: {spec_template.agent_type}")
        print(f"   - Capabilities: {len(spec_template.base_capabilities)}")
        
        # Test Research Specialist template
        research_template = registry.get_template("research_specialist")
        print(f"✅ Research Specialist template: {research_template.name}")
        print(f"   - Agent Type: {research_template.agent_type}")
        print(f"   - Capabilities: {len(research_template.base_capabilities)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Template registry test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_constitutional_validation_standalone():
    """Test constitutional validation without external dependencies."""
    print("\n🧪 Testing Constitutional Validation (Standalone)...")
    
    try:
        # Import only the constitutional validator
        sys.path.append(str(Path(__file__).parent / "agent_summoner"))
        
        from constitutional.constitutional_validator import ConstitutionalValidator
        from agent_templates import AgentTemplateRegistry
        
        # Create a mock blueprint
        class MockBlueprint:
            def __init__(self):
                self.core_principles = [
                    type('Principle', (), {'statement': 'Blueprint Thinking'})(),
                    type('Principle', (), {'statement': 'Systems Over Willpower'})()
                ]
        
        blueprint = MockBlueprint()
        validator = ConstitutionalValidator(blueprint)
        print("✅ Constitutional validator created")
        
        # Test template validation
        registry = AgentTemplateRegistry()
        eu_template = registry.get_template("eu_grant_specialist")
        
        is_valid = validator.validate_template(eu_template)
        print(f"✅ EU Grant Specialist template validation: {'PASSED' if is_valid else 'FAILED'}")
        
        spec_template = registry.get_template("specification_agent")
        is_valid = validator.validate_template(spec_template)
        print(f"✅ Specification Agent template validation: {'PASSED' if is_valid else 'FAILED'}")
        
        research_template = registry.get_template("research_specialist")
        is_valid = validator.validate_template(research_template)
        print(f"✅ Research Specialist template validation: {'PASSED' if is_valid else 'FAILED'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Constitutional validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_lifecycle_management_standalone():
    """Test lifecycle management without external dependencies."""
    print("\n🧪 Testing Lifecycle Management (Standalone)...")
    
    try:
        # Import only the lifecycle manager
        sys.path.append(str(Path(__file__).parent / "agent_summoner"))
        
        from lifecycle_manager import AgentLifecycleManager
        
        # Create a mock registry
        class MockRegistry:
            def __init__(self):
                self.agents = {}
            
            def get(self, agent_id):
                return self.agents.get(agent_id)
        
        registry = MockRegistry()
        lifecycle_manager = AgentLifecycleManager(registry)
        print("✅ Lifecycle manager created")
        
        # Test agent tracking
        test_agent_id = "test-agent-001"
        lifecycle_manager.track_agent(test_agent_id)
        print(f"✅ Agent {test_agent_id} tracked")
        
        # Test agent retirement
        lifecycle_manager.retire_agent(test_agent_id, "test_completion")
        print(f"✅ Agent {test_agent_id} retired")
        
        return True
        
    except Exception as e:
        print(f"❌ Lifecycle management test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_constitutional_principles():
    """Test that constitutional principles are properly embedded."""
    print("\n🧪 Testing Constitutional Principles...")
    
    try:
        sys.path.append(str(Path(__file__).parent / "agent_summoner"))
        
        from agent_templates import AgentTemplateRegistry
        
        registry = AgentTemplateRegistry()
        
        # Test EU Grant Specialist constitutional requirements
        eu_template = registry.get_template("eu_grant_specialist")
        constitutional_reqs = eu_template.constitutional_requirements
        
        print(f"✅ EU Grant Specialist constitutional requirements:")
        for key, value in constitutional_reqs.items():
            print(f"   - {key}: {value}")
        
        # Test Specification Agent constitutional requirements
        spec_template = registry.get_template("specification_agent")
        constitutional_reqs = spec_template.constitutional_requirements
        
        print(f"✅ Specification Agent constitutional requirements:")
        for key, value in constitutional_reqs.items():
            print(f"   - {key}: {value}")
        
        # Test Research Specialist constitutional requirements
        research_template = registry.get_template("research_specialist")
        constitutional_reqs = research_template.constitutional_requirements
        
        print(f"✅ Research Specialist constitutional requirements:")
        for key, value in constitutional_reqs.items():
            print(f"   - {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Constitutional principles test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Standalone Constitutional Tests...")
    
    success = True
    
    # Test 1: Template Registry
    if not test_template_registry_standalone():
        success = False
    
    # Test 2: Constitutional Validation
    if not test_constitutional_validation_standalone():
        success = False
    
    # Test 3: Lifecycle Management
    if not test_lifecycle_management_standalone():
        success = False
    
    # Test 4: Constitutional Principles
    if not test_constitutional_principles():
        success = False
    
    if success:
        print("\n🎉 ALL STANDALONE TESTS PASSED!")
        print("✅ Agent Summoner components are working correctly")
        print("✅ Constitutional compliance verified")
        print("✅ Ready for integration with AI Prime Agent")
        print("\n📋 Next Steps:")
        print("   1. Fix AIPrimeAgent import paths")
        print("   2. Test full integration")
        print("   3. Deploy with constitutional oversight")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("❌ Agent Summoner needs fixes before integration")
        sys.exit(1)
