"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path
from typing import Generator

import pytest

from cursorrules_architect.config import AnalysisConfig
from cursorrules_architect.core.analysis.result import AnalysisResult


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_project_dir(temp_dir: Path) -> Path:
    """Create a sample project directory structure."""
    project_dir = temp_dir / "sample_project"
    project_dir.mkdir()
    
    # Create sample files
    (project_dir / "main.py").write_text("""
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""")
    
    (project_dir / "requirements.txt").write_text("""
requests>=2.25.0
click>=8.0.0
""")
    
    (project_dir / "README.md").write_text("""
# Sample Project

This is a sample project for testing.
""")
    
    # Create subdirectory
    src_dir = project_dir / "src"
    src_dir.mkdir()
    (src_dir / "__init__.py").write_text("")
    (src_dir / "utils.py").write_text("""
def helper_function():
    return "helper"
""")
    
    return project_dir


@pytest.fixture
def default_config() -> AnalysisConfig:
    """Create a default analysis configuration."""
    return AnalysisConfig()


@pytest.fixture
def sample_analysis_result(sample_project_dir: Path) -> AnalysisResult:
    """Create a sample analysis result."""
    from datetime import datetime
    
    result = AnalysisResult(
        project_path=str(sample_project_dir),
        project_name=sample_project_dir.name,
        started_at=datetime.now(),
    )
    
    return result


@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock API keys for testing."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")


# Pytest markers
pytest_plugins = []
