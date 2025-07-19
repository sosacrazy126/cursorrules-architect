"""
core/analysis_enhancement/__init__.py

REALISTIC Analysis Enhancement Module
Replaces the pseudoscientific "context engineering" with actual analysis improvements.
"""

from .prompt_optimizer import RealPromptOptimizer, PromptStrategy, PromptMetrics, PromptCache
from .analysis_enhancer import (
    RealAnalysisEnhancer, 
    AnalysisMetrics,
    CodePatternAnalyzer,
    DependencyAnalyzer, 
    ArchitectureAnalyzer
)

__all__ = [
    # Prompt optimization (real LLM improvements)
    "RealPromptOptimizer",
    "PromptStrategy", 
    "PromptMetrics",
    "PromptCache",
    
    # Analysis enhancement (real code analysis)
    "RealAnalysisEnhancer",
    "AnalysisMetrics", 
    "CodePatternAnalyzer",
    "DependencyAnalyzer",
    "ArchitectureAnalyzer"
]