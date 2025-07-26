"""
Analysis result classes for tracking analysis pipeline execution.

This module provides classes for tracking the results of analysis phases
and the overall analysis pipeline execution.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass
class PhaseResult:
    """Result of a single analysis phase."""
    
    phase_name: str
    phase_number: int
    status: str  # "success", "error", "warning", "skipped"
    data: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    token_usage: Dict[str, int] = field(default_factory=dict)
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Set timestamps if not provided."""
        if self.started_at is None:
            self.started_at = datetime.now()
        if self.completed_at is None and self.status in ["success", "error"]:
            self.completed_at = datetime.now()


@dataclass 
class AnalysisResult:
    """Complete analysis pipeline result."""
    
    project_path: str
    project_name: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    phase_results: List[PhaseResult] = field(default_factory=list)
    total_execution_time: float = 0.0
    status: str = "running"  # "running", "completed", "failed", "cancelled"
    
    # Generated outputs
    cursorrules_content: Optional[str] = None
    cursorignore_content: Optional[str] = None
    
    # Metadata
    config_used: Optional[Dict[str, Any]] = None
    context_engineering_enabled: bool = False
    
    def add_phase_result(self, phase_result: PhaseResult) -> None:
        """Add a phase result to the analysis."""
        self.phase_results.append(phase_result)
        self.total_execution_time += phase_result.execution_time
        
        # Update overall status based on phase results
        if phase_result.status == "error":
            self.status = "failed"
        elif self.status == "running" and phase_result.status == "success":
            # Keep running status until all phases complete
            pass
    
    def complete_analysis(self) -> None:
        """Mark the analysis as completed."""
        self.completed_at = datetime.now()
        if self.status == "running":
            self.status = "completed"
    
    def is_successful(self) -> bool:
        """Check if the analysis completed successfully."""
        return (
            self.status == "completed" and
            all(phase.status == "success" for phase in self.phase_results)
        )
    
    @property
    def total_tokens_used(self) -> int:
        """Calculate total tokens used across all phases."""
        total = 0
        for phase in self.phase_results:
            if phase.token_usage:
                total += phase.token_usage.get("input", 0)
                total += phase.token_usage.get("output", 0)
        return total
    
    def get_phase_result(self, phase_name: str) -> Optional[PhaseResult]:
        """Get result for a specific phase."""
        for phase in self.phase_results:
            if phase.phase_name == phase_name:
                return phase
        return None
    
    def get_errors(self) -> List[str]:
        """Get all error messages from failed phases."""
        errors = []
        for phase in self.phase_results:
            if phase.error_message:
                errors.append(f"{phase.phase_name}: {phase.error_message}")
        return errors
    
    def get_warnings(self) -> List[str]:
        """Get all warnings from all phases."""
        warnings = []
        for phase in self.phase_results:
            for warning in phase.warnings:
                warnings.append(f"{phase.phase_name}: {warning}")
        return warnings
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "project_path": self.project_path,
            "project_name": self.project_name,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_execution_time": self.total_execution_time,
            "status": self.status,
            "phase_results": [
                {
                    "phase_name": phase.phase_name,
                    "phase_number": phase.phase_number,
                    "status": phase.status,
                    "execution_time": phase.execution_time,
                    "token_usage": phase.token_usage,
                    "error_message": phase.error_message,
                    "warnings": phase.warnings,
                }
                for phase in self.phase_results
            ],
            "total_tokens_used": self.total_tokens_used,
            "cursorrules_content": self.cursorrules_content,
            "cursorignore_content": self.cursorignore_content,
            "context_engineering_enabled": self.context_engineering_enabled,
        }


__all__ = ["PhaseResult", "AnalysisResult"]
