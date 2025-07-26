"""Tests for configuration system."""

import pytest
from pathlib import Path

from cursorrules_architect.config import (
    AnalysisConfig,
    ModelConfig,
    AgentProvider,
    ReasoningMode,
    load_config,
)


class TestModelConfig:
    """Test ModelConfig class."""
    
    def test_model_config_creation(self):
        """Test creating a model configuration."""
        config = ModelConfig(
            provider=AgentProvider.ANTHROPIC,
            model_name="claude-3-sonnet",
            reasoning=ReasoningMode.ENABLED,
            temperature=0.7,
        )
        
        assert config.provider == AgentProvider.ANTHROPIC
        assert config.model_name == "claude-3-sonnet"
        assert config.reasoning == ReasoningMode.ENABLED
        assert config.temperature == 0.7
    
    def test_model_config_defaults(self):
        """Test model configuration defaults."""
        config = ModelConfig(
            provider=AgentProvider.OPENAI,
            model_name="gpt-4",
        )
        
        assert config.reasoning == ReasoningMode.DISABLED
        assert config.temperature is None
        assert config.max_tokens is None
        assert config.timeout == 60
    
    def test_model_config_validation(self):
        """Test model configuration validation."""
        # Test invalid temperature
        with pytest.raises(ValueError):
            ModelConfig(
                provider=AgentProvider.OPENAI,
                model_name="gpt-4",
                temperature=3.0,  # Too high
            )
        
        # Test invalid max_tokens
        with pytest.raises(ValueError):
            ModelConfig(
                provider=AgentProvider.OPENAI,
                model_name="gpt-4",
                max_tokens=0,  # Too low
            )


class TestAnalysisConfig:
    """Test AnalysisConfig class."""
    
    def test_analysis_config_creation(self):
        """Test creating an analysis configuration."""
        config = AnalysisConfig()
        
        assert config.max_file_size == 1024 * 1024  # 1MB
        assert config.max_files_per_agent == 50
        assert config.enable_context_engineering is False
        assert config.parallel_execution is True
    
    def test_get_phase_model(self):
        """Test getting phase model configuration."""
        config = AnalysisConfig()
        
        phase1_model = config.get_phase_model("phase1")
        assert phase1_model.provider == AgentProvider.GEMINI
        
        # Test fallback for unknown phase
        unknown_model = config.get_phase_model("unknown_phase")
        assert unknown_model is not None
    
    def test_update_phase_model(self):
        """Test updating phase model configuration."""
        config = AnalysisConfig()
        
        new_model = ModelConfig(
            provider=AgentProvider.ANTHROPIC,
            model_name="claude-3-opus",
        )
        
        config.update_phase_model("phase1", new_model)
        
        updated_model = config.get_phase_model("phase1")
        assert updated_model.provider == AgentProvider.ANTHROPIC
        assert updated_model.model_name == "claude-3-opus"


class TestConfigLoader:
    """Test configuration loading."""
    
    def test_load_default_config(self):
        """Test loading default configuration."""
        config = load_config()
        
        assert isinstance(config, AnalysisConfig)
        assert config.max_file_size > 0
        assert len(config.phase_models) > 0
    
    def test_load_config_from_yaml(self, temp_dir: Path):
        """Test loading configuration from YAML file."""
        config_file = temp_dir / "test_config.yaml"
        config_content = """
max_file_size: 2097152
max_files_per_agent: 25
enable_context_engineering: true
phase_timeout: 600
"""
        config_file.write_text(config_content)
        
        config = load_config(config_file)
        
        assert config.max_file_size == 2097152  # 2MB
        assert config.max_files_per_agent == 25
        assert config.enable_context_engineering is True
        assert config.phase_timeout == 600
    
    def test_load_nonexistent_config(self):
        """Test loading configuration from nonexistent file."""
        config = load_config(Path("nonexistent.yaml"))
        
        # Should return default config
        assert isinstance(config, AnalysisConfig)
    
    def test_env_override(self, monkeypatch):
        """Test environment variable overrides."""
        monkeypatch.setenv("CRA_PHASE_TIMEOUT", "900")
        monkeypatch.setenv("CRA_MAX_FILES_PER_AGENT", "100")
        monkeypatch.setenv("CRA_ENABLE_CONTEXT_ENGINEERING", "true")
        
        config = load_config()
        
        assert config.phase_timeout == 900
        assert config.max_files_per_agent == 100
        assert config.enable_context_engineering is True
