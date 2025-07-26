"""Tests for AI agents."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from cursorrules_architect.config.models import ModelConfig, AgentProvider, ReasoningMode
from cursorrules_architect.core.agents import create_agent
from cursorrules_architect.core.agents.base import AgentContext, AgentResponse
from cursorrules_architect.core.agents.anthropic import AnthropicAgent


class TestAgentFactory:
    """Test agent factory functions."""
    
    def test_create_anthropic_agent(self, mock_api_key):
        """Test creating Anthropic agent."""
        config = ModelConfig(
            provider=AgentProvider.ANTHROPIC,
            model_name="claude-3-sonnet",
        )
        
        agent = create_agent(config, "test_agent")
        
        assert isinstance(agent, AnthropicAgent)
        assert agent.name == "test_agent"
        assert agent.config == config
    
    def test_create_agent_unsupported_provider(self):
        """Test creating agent with unsupported provider."""
        config = ModelConfig(
            provider="unsupported",  # type: ignore
            model_name="test-model",
        )
        
        with pytest.raises(ValueError, match="Unsupported agent provider"):
            create_agent(config)


class TestAgentContext:
    """Test AgentContext data structure."""
    
    def test_agent_context_creation(self):
        """Test creating agent context."""
        context = AgentContext(
            project_path="/test/project",
            project_tree=["file1.py", "file2.py"],
            assigned_files=["file1.py"],
            previous_results={"phase1": "results"},
        )
        
        assert context.project_path == "/test/project"
        assert len(context.project_tree) == 2
        assert len(context.assigned_files) == 1
        assert "phase1" in context.previous_results
    
    def test_agent_context_defaults(self):
        """Test agent context with defaults."""
        context = AgentContext(
            project_path="/test/project",
            project_tree=["file1.py"],
        )
        
        assert context.assigned_files == []
        assert context.previous_results == {}


class TestAgentResponse:
    """Test AgentResponse data structure."""
    
    def test_agent_response_creation(self):
        """Test creating agent response."""
        response = AgentResponse(
            agent_name="test_agent",
            status="success",
            content="Analysis complete",
            metadata={"model": "claude-3-sonnet"},
            token_usage={"input": 100, "output": 200},
        )
        
        assert response.agent_name == "test_agent"
        assert response.status == "success"
        assert response.content == "Analysis complete"
        assert response.metadata["model"] == "claude-3-sonnet"
        assert response.token_usage["input"] == 100
    
    def test_agent_response_defaults(self):
        """Test agent response with defaults."""
        response = AgentResponse(
            agent_name="test_agent",
            status="success",
            content="Test content",
        )
        
        assert response.metadata == {}
        assert response.error_message is None
        assert response.token_usage is None


class TestAnthropicAgent:
    """Test AnthropicAgent implementation."""
    
    @pytest.fixture
    def anthropic_config(self):
        """Create Anthropic configuration."""
        return ModelConfig(
            provider=AgentProvider.ANTHROPIC,
            model_name="claude-3-sonnet",
            reasoning=ReasoningMode.ENABLED,
        )
    
    @pytest.fixture
    def sample_context(self):
        """Create sample agent context."""
        return AgentContext(
            project_path="/test/project",
            project_tree=["main.py", "utils.py"],
            assigned_files=["main.py"],
        )
    
    def test_anthropic_agent_creation(self, anthropic_config, mock_api_key):
        """Test creating Anthropic agent."""
        agent = AnthropicAgent(anthropic_config, "test_anthropic")
        
        assert agent.name == "test_anthropic"
        assert agent.config == anthropic_config
        assert agent.provider == AgentProvider.ANTHROPIC
    
    def test_anthropic_agent_missing_api_key(self, anthropic_config, monkeypatch):
        """Test Anthropic agent without API key."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY environment variable is required"):
            AnthropicAgent(anthropic_config)
    
    @patch('cursorrules_architect.core.agents.anthropic.Anthropic')
    async def test_anthropic_agent_analyze(self, mock_anthropic_class, anthropic_config, sample_context, mock_api_key):
        """Test Anthropic agent analysis."""
        # Mock the Anthropic client
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        
        # Mock the API response
        mock_response = Mock()
        mock_response.content = [Mock(text="Analysis result")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=200)
        mock_client.messages.create.return_value = mock_response
        
        # Create agent and run analysis
        agent = AnthropicAgent(anthropic_config, "test_agent")
        response = await agent.analyze(sample_context)
        
        # Verify response
        assert response.status == "success"
        assert response.content == "Analysis result"
        assert response.agent_name == "test_agent"
        assert response.token_usage["input_tokens"] == 100
        assert response.token_usage["output_tokens"] == 200
    
    @patch('cursorrules_architect.core.agents.anthropic.Anthropic')
    async def test_anthropic_agent_error_handling(self, mock_anthropic_class, anthropic_config, sample_context, mock_api_key):
        """Test Anthropic agent error handling."""
        # Mock the Anthropic client to raise an exception
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")
        
        # Create agent and run analysis
        agent = AnthropicAgent(anthropic_config, "test_agent")
        response = await agent.analyze(sample_context)
        
        # Verify error response
        assert response.status == "error"
        assert response.error_message == "API Error"
        assert response.content == ""
