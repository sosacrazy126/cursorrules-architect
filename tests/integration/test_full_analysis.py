"""Integration tests for full analysis pipeline."""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

from cursorrules_architect.config import AnalysisConfig
from cursorrules_architect.core.analysis import ProjectAnalyzer


class TestFullAnalysisPipeline:
    """Test the complete analysis pipeline."""
    
    @pytest.fixture
    def analysis_config(self):
        """Create analysis configuration for testing."""
        config = AnalysisConfig()
        # Disable context engineering for simpler testing
        config.enable_context_engineering = False
        # Reduce timeouts for faster tests
        config.phase_timeout = 30
        config.total_timeout = 120
        return config
    
    @pytest.mark.asyncio
    async def test_project_analyzer_initialization(self, sample_project_dir, analysis_config):
        """Test project analyzer initialization."""
        analyzer = ProjectAnalyzer(sample_project_dir, analysis_config)
        
        assert analyzer.project_path == sample_project_dir
        assert analyzer.config == analysis_config
        assert len(analyzer.phases) == 6  # 5 phases + final
        assert analyzer.result.project_name == sample_project_dir.name
    
    @pytest.mark.asyncio
    @patch('cursorrules_architect.core.agents.factory.create_agent')
    async def test_analysis_pipeline_mock(self, mock_create_agent, sample_project_dir, analysis_config, mock_api_key):
        """Test analysis pipeline with mocked agents."""
        # Mock agent responses
        mock_agent = AsyncMock()
        mock_agent.analyze.return_value = Mock(
            status="success",
            content="Mock analysis result",
            metadata={"model": "test-model"},
            token_usage={"input": 100, "output": 200},
        )
        mock_agent.create_plan.return_value = Mock(
            status="success",
            content="Mock plan result",
            metadata={"model": "test-model"},
        )
        mock_agent.synthesize.return_value = Mock(
            status="success",
            content="Mock synthesis result",
            metadata={"model": "test-model"},
        )
        
        mock_create_agent.return_value = mock_agent
        
        # Run analysis
        analyzer = ProjectAnalyzer(sample_project_dir, analysis_config)
        result = await analyzer.analyze()
        
        # Verify result structure
        assert result.project_path == str(sample_project_dir)
        assert result.completed_at is not None
        assert result.total_execution_time > 0
        assert len(result.phase_results) > 0
        
        # Verify phases were called
        assert mock_agent.analyze.called
    
    @pytest.mark.asyncio
    async def test_analysis_with_errors(self, sample_project_dir, analysis_config):
        """Test analysis pipeline with simulated errors."""
        # This test would require more sophisticated mocking
        # to simulate specific error conditions
        analyzer = ProjectAnalyzer(sample_project_dir, analysis_config)
        
        # For now, just verify the analyzer can be created
        assert analyzer is not None
    
    @pytest.mark.asyncio
    async def test_tree_generation(self, sample_project_dir, analysis_config):
        """Test project tree generation."""
        analyzer = ProjectAnalyzer(sample_project_dir, analysis_config)
        
        # Generate tree
        tree = await analyzer._generate_project_tree()
        
        assert isinstance(tree, list)
        assert len(tree) > 0
        
        # Check that main files are included
        tree_str = "\n".join(tree)
        assert "main.py" in tree_str
        assert "requirements.txt" in tree_str
        assert "README.md" in tree_str


class TestAnalysisResult:
    """Test analysis result handling."""
    
    def test_analysis_result_creation(self, sample_project_dir):
        """Test creating analysis result."""
        from cursorrules_architect.core.analysis.result import AnalysisResult
        from datetime import datetime
        
        result = AnalysisResult(
            project_path=str(sample_project_dir),
            project_name=sample_project_dir.name,
            started_at=datetime.now(),
        )
        
        assert result.project_path == str(sample_project_dir)
        assert result.project_name == sample_project_dir.name
        assert result.phase_results == []
        assert result.total_execution_time == 0.0
    
    def test_add_phase_result(self, sample_analysis_result):
        """Test adding phase results."""
        from cursorrules_architect.core.analysis.result import PhaseResult
        
        phase_result = PhaseResult(
            phase_name="test_phase",
            phase_number=1,
            status="success",
            data={"test": "data"},
            execution_time=1.5,
            token_usage={"input": 100, "output": 200},
        )
        
        sample_analysis_result.add_phase_result(phase_result)
        
        assert len(sample_analysis_result.phase_results) == 1
        assert sample_analysis_result.total_execution_time == 1.5
        assert sample_analysis_result.total_tokens_used == 300
    
    def test_get_phase_result(self, sample_analysis_result):
        """Test getting specific phase result."""
        from cursorrules_architect.core.analysis.result import PhaseResult
        
        phase_result = PhaseResult(
            phase_name="phase1",
            phase_number=1,
            status="success",
            data={"test": "data"},
        )
        
        sample_analysis_result.add_phase_result(phase_result)
        
        retrieved = sample_analysis_result.get_phase_result("phase1")
        assert retrieved is not None
        assert retrieved.phase_name == "phase1"
        
        missing = sample_analysis_result.get_phase_result("nonexistent")
        assert missing is None
    
    def test_is_successful(self, sample_analysis_result):
        """Test success detection."""
        from cursorrules_architect.core.analysis.result import PhaseResult
        
        # Add successful phase
        success_phase = PhaseResult(
            phase_name="phase1",
            phase_number=1,
            status="success",
            data={},
        )
        sample_analysis_result.add_phase_result(success_phase)
        
        assert sample_analysis_result.is_successful() is True
        
        # Add error phase
        error_phase = PhaseResult(
            phase_name="phase2",
            phase_number=2,
            status="error",
            data={},
            error_message="Test error",
        )
        sample_analysis_result.add_phase_result(error_phase)
        
        assert sample_analysis_result.is_successful() is False
    
    def test_get_errors(self, sample_analysis_result):
        """Test error collection."""
        from cursorrules_architect.core.analysis.result import PhaseResult
        
        # Add phase with error
        error_phase = PhaseResult(
            phase_name="phase1",
            phase_number=1,
            status="error",
            data={},
            error_message="Test error message",
        )
        sample_analysis_result.add_phase_result(error_phase)
        
        errors = sample_analysis_result.get_errors()
        assert len(errors) == 1
        assert "phase1: Test error message" in errors
