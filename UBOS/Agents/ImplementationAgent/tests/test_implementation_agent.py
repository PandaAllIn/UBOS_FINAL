"""
UBOS Blueprint: Implementation Agent Tests

Philosophy: Blueprint Thinking + Systems Over Willpower
Strategic Purpose: Validate Implementation Agent functionality and constitutional compliance
System Design: Comprehensive test suite with constitutional validation
Feedback Loops: Test results improve implementation quality
Environmental Support: Integrates with existing UBOS test patterns
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "AIPrimeAgent"))

# Mock the AIPrimeAgent imports for testing
class MockBlueprintMetadata:
    def __init__(self):
        self.schema_version = "1.0"
        self.document_version = "1.0.0"
        self.last_updated_utc = "2025-09-25T10:00:00Z"
        self.review_cadence_days = 7

class MockCorePrinciple:
    def __init__(self, principleId: str, statement: str, rationale: str = ""):
        self.principleId = principleId
        self.statement = statement
        self.rationale = rationale

class MockStrategicBlueprint:
    def __init__(self):
        self.blueprint_metadata = MockBlueprintMetadata()
        self.mission_statement = "Constitutional implementation testing"
        self.core_principles = [
            MockCorePrinciple("UBOS-P-01", "Blueprint Thinking", "Intentional design"),
            MockCorePrinciple("UBOS-P-02", "Systems Over Willpower", "Structural solutions")
        ]
        self.active_goals = []
        self.agent_registry = []
        self.guardrails = {}

class MockStrategicPause:
    def __init__(self, blueprint):
        self.blueprint = blueprint
    
    def pre_delegation(self, query: str, objectives: list):
        class MockPauseDecision:
            def __init__(self, status: str, reasons: str = ""):
                self.status = status
                self.reasons = reasons
        return MockPauseDecision("proceed")

class MockBlueprintValidator:
    def __init__(self, blueprint):
        self.blueprint = blueprint

class MockGeminiClient:
    def __init__(self):
        self.available_flag = True
    
    def available(self):
        return self.available_flag
    
    def generate_consultation(self, prompt: str):
        class MockResponse:
            def __init__(self):
                self.analysis = "Constitutional analysis response"
        return MockResponse()

# Mock the imports
sys.modules['ai_prime_agent.blueprint.schema'] = Mock()
sys.modules['ai_prime_agent.blueprint.schema'].validate_blueprint_dict = lambda x: MockStrategicBlueprint()
sys.modules['ai_prime_agent.pause'] = Mock()
sys.modules['ai_prime_agent.pause'].StrategicPause = MockStrategicPause
sys.modules['ai_prime_agent.validation'] = Mock()
sys.modules['ai_prime_agent.validation'].BlueprintValidator = MockBlueprintValidator
sys.modules['master_librarian.llm.gemini'] = Mock()
sys.modules['master_librarian.llm.gemini'].GeminiClient = MockGeminiClient
sys.modules['master_librarian.llm.gemini'].GeminiUnavailableError = Exception

# Now import the Implementation Agent components
from implementation_agent.constitutional_coder import ConstitutionalImplementationAgent
from implementation_agent.codex_wrapper import CodexWrapper
from implementation_agent.context7_integration import Context7Integration
from implementation_agent.constitutional_validation import ConstitutionalCodeValidator


class TestConstitutionalImplementationAgent:
    """Test Constitutional Implementation Agent functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.blueprint = MockStrategicBlueprint()
        self.agent = ConstitutionalImplementationAgent(self.blueprint)
    
    def test_initialization(self):
        """Test agent initialization."""
        assert self.agent.blueprint is not None
        assert self.agent.gemini is not None
        assert self.agent.strategic_pause is not None
        assert self.agent.blueprint_validator is not None
        assert self.agent.codex_wrapper is not None
        assert self.agent.context7_integration is not None
        assert self.agent.constitutional_validator is not None
    
    def test_implement_from_specification_success(self):
        """Test successful implementation from specification."""
        # Mock CodexWrapper
        with patch.object(self.agent.codex_wrapper, 'generate_code') as mock_generate:
            mock_generate.return_value = '''
# UBOS Blueprint: TestClass
# Philosophy: Blueprint Thinking + Systems Over Willpower

class TestClass:
    """Constitutional test class."""
    pass
'''
            
            # Mock ConstitutionalCodeValidator
            with patch.object(self.agent.constitutional_validator, 'validate_code') as mock_validate:
                mock_validate.return_value = {
                    "is_constitutional": True,
                    "overall_score": 0.9,
                    "violations": []
                }
                
                # Test implementation
                specification = {
                    "name": "TestClass",
                    "description": "Test specification"
                }
                
                result = self.agent.implement_from_specification(
                    specification=specification,
                    constitutional_requirements=["Blueprint Thinking"],
                    language="Python"
                )
                
                assert result["status"] == "success"
                assert result["code"] is not None
                assert result["constitutional_analysis"] is not None
                assert result["validation_result"]["is_constitutional"] is True
    
    def test_implement_from_specification_escalation(self):
        """Test implementation escalation."""
        # Mock strategic pause to return escalation
        with patch.object(self.agent.strategic_pause, 'pre_delegation') as mock_pause:
            mock_pause.return_value.status = "escalate"
            mock_pause.return_value.reasons = "Constitutional violation"
            
            specification = {"name": "TestClass"}
            
            result = self.agent.implement_from_specification(
                specification=specification,
                constitutional_requirements=["Blueprint Thinking"]
            )
            
            assert result["status"] == "escalated"
            assert "Constitutional escalation" in result["error"]
    
    def test_review_implementation(self):
        """Test implementation review."""
        test_code = '''
# UBOS Blueprint: TestClass
# Philosophy: Blueprint Thinking

class TestClass:
    """Test class."""
    pass
'''
        
        with patch.object(self.agent.constitutional_validator, 'validate_code') as mock_validate:
            mock_validate.return_value = {
                "is_constitutional": True,
                "overall_score": 0.8,
                "violations": []
            }
            
            result = self.agent.review_implementation(
                code=test_code,
                language="Python"
            )
            
            assert result["is_constitutional"] is True
            assert result["overall_score"] == 0.8


class TestCodexWrapper:
    """Test Codex CLI Wrapper functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.wrapper = CodexWrapper()
    
    def test_initialization(self):
        """Test wrapper initialization."""
        assert self.wrapper.codex_path is not None
        assert self.wrapper.constitutional_prompts is not None
    
    @patch('subprocess.run')
    def test_generate_code_success(self, mock_run):
        """Test successful code generation."""
        # Mock subprocess result
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "generated code"
        mock_run.return_value = mock_result
        
        specification = {"name": "TestClass", "description": "Test class"}
        
        result = self.wrapper.generate_code(
            specification=specification,
            language="Python",
            constitutional_requirements=["Blueprint Thinking"]
        )
        
        assert "generated code" in result
        assert "# UBOS" in result  # Should have constitutional header
    
    @patch('subprocess.run')
    def test_generate_code_failure(self, mock_run):
        """Test code generation failure."""
        # Mock subprocess failure
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Codex CLI error"
        mock_run.return_value = mock_result
        
        specification = {"name": "TestClass"}
        
        with pytest.raises(Exception) as exc_info:
            self.wrapper.generate_code(
                specification=specification,
                language="Python"
            )
        
        assert "Codex CLI failed" in str(exc_info.value)


class TestContext7Integration:
    """Test Context7 MCP Integration functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.integration = Context7Integration()
    
    def test_initialization(self):
        """Test integration initialization."""
        assert self.integration.available is not None
    
    def test_get_implementation_guidance(self):
        """Test implementation guidance retrieval."""
        specification = {"name": "TestClass", "description": "Test class"}
        generated_code = "class TestClass: pass"
        
        result = self.integration.get_implementation_guidance(
            specification=specification,
            generated_code=generated_code,
            language="Python"
        )
        
        assert "constitutional_guidance" in result
        assert "implementation_best_practices" in result
        assert "constitutional_safeguards" in result


class TestConstitutionalCodeValidator:
    """Test Constitutional Code Validator functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.blueprint = MockStrategicBlueprint()
        self.validator = ConstitutionalCodeValidator(self.blueprint)
    
    def test_initialization(self):
        """Test validator initialization."""
        assert self.validator.blueprint is not None
        assert self.validator.gemini is not None
        assert self.validator.constitutional_patterns is not None
    
    def test_validate_code_constitutional(self):
        """Test validation of constitutional code."""
        constitutional_code = '''
# UBOS Blueprint: TestClass
# Philosophy: Blueprint Thinking + Systems Over Willpower
# Strategic Purpose: Test implementation

class TestClass:
    """Constitutional test class."""
    pass
'''
        
        result = self.validator.validate_code(
            code=constitutional_code,
            language="Python",
            constitutional_requirements=["Blueprint Thinking"]
        )
        
        assert result["is_constitutional"] is True
        assert result["overall_score"] > 0.5
    
    def test_validate_code_non_constitutional(self):
        """Test validation of non-constitutional code."""
        non_constitutional_code = '''
class TestClass:
    pass
'''
        
        result = self.validator.validate_code(
            code=non_constitutional_code,
            language="Python",
            constitutional_requirements=["Blueprint Thinking"]
        )
        
        assert result["is_constitutional"] is False
        assert len(result["violations"]) > 0


def test_constitutional_implementation_workflow():
    """Test complete constitutional implementation workflow."""
    # Test that all components can be initialized
    blueprint = MockStrategicBlueprint()
    
    # Test all components
    agent = ConstitutionalImplementationAgent(blueprint)
    wrapper = CodexWrapper()
    integration = Context7Integration()
    validator = ConstitutionalCodeValidator(blueprint)
    
    assert agent is not None
    assert wrapper is not None
    assert integration is not None
    assert validator is not None
    
    print("✅ Constitutional Implementation Workflow components initialized successfully")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])