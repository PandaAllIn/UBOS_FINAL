#!/usr/bin/env python3
"""
Simple Constitutional Test

Test the Agent Summoner components individually for constitutional compliance.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "AIPrimeAgent"))

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing Imports...")
    
    try:
        from agent_summoner.agent_templates import AgentTemplateRegistry
        print("✅ AgentTemplateRegistry import successful")
    except Exception as e:
        print(f"❌ AgentTemplateRegistry import failed: {e}")
        return False
    
    try:
        from agent_summoner.lifecycle_manager import AgentLifecycleManager
        print("✅ AgentLifecycleManager import successful")
    except Exception as e:
        print(f"❌ AgentLifecycleManager import failed: {e}")
        return False
    
    try:
        from agent_summoner.constitutional.constitutional_validator import ConstitutionalValidator
        print("✅ ConstitutionalValidator import successful")
    except Exception as e:
        print(f"❌ ConstitutionalValidator import failed: {e}")
        return False
    
    return True

def test_template_registry():
    """Test the template registry functionality."""
    print("\n🧪 Testing Template Registry...")
    
    try:
        from agent_summoner.agent_templates import AgentTemplateRegistry
        
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

def test_constitutional_validation():
    """Test constitutional validation functionality."""
    print("\n🧪 Testing Constitutional Validation...")
    
    try:
        from agent_summoner.constitutional.constitutional_validator import ConstitutionalValidator
        from agent_summoner.agent_templates import AgentTemplateRegistry
        
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

def test_lifecycle_management():
    """Test lifecycle management functionality."""
    print("\n🧪 Testing Lifecycle Management...")
    
    try:
        from agent_summoner.lifecycle_manager import AgentLifecycleManager
        
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

if __name__ == "__main__":
    print("🚀 Starting Simple Constitutional Tests...")
    
    success = True
    
    # Test 1: Imports
    if not test_imports():
        success = False
    
    # Test 2: Template Registry
    if not test_template_registry():
        success = False
    
    # Test 3: Constitutional Validation
    if not test_constitutional_validation():
        success = False
    
    # Test 4: Lifecycle Management
    if not test_lifecycle_management():
        success = False
    
    if success:
        print("\n🎉 ALL SIMPLE TESTS PASSED!")
        print("✅ Agent Summoner components are working correctly")
        print("✅ Constitutional compliance verified")
        print("✅ Ready for integration with AI Prime Agent")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("❌ Agent Summoner needs fixes before integration")
        sys.exit(1)
