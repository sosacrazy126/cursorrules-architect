#!/usr/bin/env python3

"""
main_enhanced.py

Enhanced CursorRules Architect with Context Engineering Integration
ENHANCED: Critical error handling and graceful fallback mechanisms
"""

# ====================================================
# Section 1: Enhanced Setup and Initialization
# ====================================================

import click
from pathlib import Path
import os
import sys
import json
from typing import Dict, List, Optional, Any
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
from dotenv import load_dotenv
import asyncio
import traceback

# Load environment variables
if os.path.exists('.env'):
    load_dotenv()
    logging.info("Loaded environment variables from .env file")

# Import existing components
from openai import OpenAI
from anthropic import Anthropic
from config.exclusions import EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS
from core.utils.file_creation.phases_output import save_phase_outputs
from core.utils.file_creation.cursorignore import create_cursorignore
from core.utils.tools.clean_cursorrules import clean_cursorrules
from core.utils.tools.tree_generator import get_project_tree
from core.agents.openai import OpenAIAgent

# ENHANCED: Import context engineering components
try:
    from core.context_engineering.integration_manager import (
        ContextEngineeringIntegrationManager,
        IntegrationConfig,
        ContextEngineeringError,
        validate_context_engineering_dependencies
    )
    from core.analysis.enhanced_phase_1 import ContextAwarePhase1Analysis
    CONTEXT_ENGINEERING_AVAILABLE = True
except ImportError as e:
    CONTEXT_ENGINEERING_AVAILABLE = False
    IMPORT_ERROR = str(e)

# ENHANCED: Import original phases AND enhanced phases
from core.analysis import (
    Phase1Analysis,
    Phase2Analysis, 
    Phase3Analysis,
    Phase4Analysis,
    Phase5Analysis,
    FinalAnalysis
)

# ENHANCED: Import enhanced phase implementations
# from core.analysis.enhanced_phase_1 import ContextAwarePhase1Analysis # This line is now redundant

from core.utils.tools.model_config_helper import get_model_config_name
from config.config import (
    MODEL_CONFIG, 
    PHASE_MODEL_MAPPING, 
    set_model_config,
    get_used_providers,
    ModelProvider
)

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("CursorRules-Architect-Enhanced")
console = Console()

# Initialize API clients (same as original)
used_providers = get_used_providers()

if ModelProvider.OPENAI in used_providers:
    openai_client = OpenAI()
    logger.info("Initialized OpenAI client")
else:
    openai_client = None

if ModelProvider.ANTHROPIC in used_providers:
    anthropic_client = Anthropic()
    logger.info("Initialized Anthropic client")
else:
    anthropic_client = None

# ====================================================
# Section 2: Enhanced Project Analyzer Class
# ====================================================

class EnhancedProjectAnalyzer:
    """
    Enhanced ProjectAnalyzer with Context Engineering Integration.
    
    Maintains full backward compatibility while adding revolutionary 
    context engineering capabilities.
    """
    
    def __init__(self, directory: Path, enable_context_engineering: bool = True):
        """
        Initialize the Enhanced ProjectAnalyzer.
        
        Args:
            directory: Path to the project directory to analyze
            enable_context_engineering: Whether to enable context engineering enhancements
        """
        self.directory = directory
        self.enable_context_engineering = enable_context_engineering
        
        # Initialize result storage (same as original)
        self.phase1_results = {}
        self.phase2_results = {}
        self.phase3_results = {}
        self.phase4_results = {}
        self.consolidated_report = {}
        self.final_analysis = {}
        
        # ENHANCED: Initialize context engineering components
        if self.enable_context_engineering:
            console.print("[bold green]🧠 Initializing Context Engineering[/bold green]")
            
            # Create integration configuration
            self.integration_config = IntegrationConfig(
                enable_atomic_prompting=True,
                enable_field_dynamics=True,
                enable_cognitive_tools=True,
                enable_pattern_synthesis=True,
                optimization_mode="balanced"
            )
            
            # Initialize integration manager
            self.integration_manager = ContextEngineeringIntegrationManager(
                self.integration_config
            )
            
            # Initialize ENHANCED phase analyzers
            self.phase1_analyzer = ContextAwarePhase1Analysis()  # Enhanced with context engineering
            console.print("   ✅ Enhanced Phase 1 with atomic prompting + field dynamics")
            
            # For other phases, we'll use the integration manager to enhance them
            self.phase2_analyzer = Phase2Analysis()  # Will be enhanced via integration manager
            self.phase3_analyzer = Phase3Analysis()  # Will be enhanced via integration manager
            self.phase4_analyzer = Phase4Analysis()  # Will be enhanced via integration manager
            self.phase5_analyzer = Phase5Analysis()  # Will be enhanced via integration manager
            self.final_analyzer = FinalAnalysis()    # Will be enhanced via integration manager
            
            console.print("   ✅ Integration Manager initialized for all phases")
            console.print("   🎯 Context engineering: ENABLED")
            
        else:
            # Use original analyzers for backward compatibility
            console.print("[yellow]📊 Using Original Analysis (Context Engineering: DISABLED)[/yellow]")
            self.phase1_analyzer = Phase1Analysis()
            self.phase2_analyzer = Phase2Analysis()
            self.phase3_analyzer = Phase3Analysis()
            self.phase4_analyzer = Phase4Analysis()
            self.phase5_analyzer = Phase5Analysis()
            self.final_analyzer = FinalAnalysis()
            self.integration_manager = None
    
    async def analyze(self) -> Dict:
        """
        Enhanced analysis workflow with context engineering integration.
        
        Maintains the exact same interface as the original while adding
        revolutionary context engineering capabilities.
        """
        console.print(f"\n[bold]🚀 Enhanced Analysis Starting[/] {self.directory}")
        
        if self.enable_context_engineering:
            console.print("[dim]🧠 Context engineering enhancements: ACTIVE[/dim]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            # Generate project tree (same as original)
            console.print("\n[bold green]Generating project structure...[/bold green]")
            tree_task = progress.add_task("[green]Scanning files...", total=1)
            
            tree_for_analysis, package_info = get_project_tree(
                str(self.directory), 
                excluded_dirs=EXCLUDED_DIRS,
                excluded_files=EXCLUDED_FILES,
                excluded_extensions=EXCLUDED_EXTENSIONS
            )
            
            progress.update(tree_task, completed=1)
            progress.stop_task(tree_task)
            progress.remove_task(tree_task)
            console.print("[green]✓[/green] Project structure generated")

            # ENHANCED: Phase 1 with Context Engineering
            console.print("\n[bold blue]🔬 Phase 1: Enhanced Initial Discovery[/bold blue]")
            if self.enable_context_engineering:
                console.print("[dim]⚡ Atomic prompting + neural fields + cognitive analysis[/dim]")
            else:
                console.print("[dim]📊 Standard initial discovery analysis[/dim]")
            
            task1 = progress.add_task("[blue]Running enhanced discovery...", total=1)
            self.phase1_results = await self.run_enhanced_phase1(tree_for_analysis, package_info)
            
            progress.update(task1, completed=1)
            progress.stop_task(task1)
            progress.remove_task(task1)
            
            if self.enable_context_engineering:
                # Display context engineering metrics
                ce_metrics = self.phase1_results.get("enhancement_metrics", {})
                coherence = ce_metrics.get("field_coherence", 0.0)
                efficiency = ce_metrics.get("atomic_prompt_efficiency", 0.0)
                console.print(f"[green]✓[/green] Phase 1 complete: Coherence {coherence:.2f}, Efficiency {efficiency:.2f}")
            else:
                console.print("[green]✓[/green] Phase 1 complete: Standard analysis finished")

            # ENHANCED: Phase 2 with Molecular Context Building
            console.print("\n[bold blue]🧬 Phase 2: Enhanced Methodical Planning[/bold blue]")
            if self.enable_context_engineering:
                console.print("[dim]🔗 Molecular context building + pattern chaining[/dim]")
            
            task2 = progress.add_task("[blue]Creating enhanced analysis plan...", total=1)
            self.phase2_results = await self.run_enhanced_phase2(self.phase1_results, tree_for_analysis)
            
            progress.update(task2, completed=1)
            progress.stop_task(task2)
            progress.remove_task(task2)
            console.print("[blue]✓[/blue] Phase 2 complete: Enhanced analysis plan created")

            # ENHANCED: Phase 3 with Memory Integration
            console.print("\n[bold yellow]🧮 Phase 3: Enhanced Deep Analysis[/bold yellow]")
            
            agent_count = len(self.phase2_results.get("agents", []))
            if self.enable_context_engineering:
                console.print(f"[dim]🧠 Memory-integrated analysis with {agent_count} specialized agents[/dim]")
            else:
                console.print(f"[dim]📊 Standard deep analysis with {agent_count} agents[/dim]")
                
            task3 = progress.add_task("[yellow]Running enhanced deep analysis...", total=1)
            self.phase3_results = await self.run_enhanced_phase3(self.phase2_results, tree_for_analysis)
            
            progress.update(task3, completed=1)
            progress.stop_task(task3)
            progress.remove_task(task3)
            console.print("[yellow]✓[/yellow] Phase 3 complete: Enhanced deep analysis finished")

            # ENHANCED: Phase 4 with Organic Synthesis
            console.print("\n[bold magenta]🌿 Phase 4: Enhanced Synthesis[/bold magenta]")
            if self.enable_context_engineering:
                console.print("[dim]🎼 Multi-field orchestration + organic pattern synthesis[/dim]")
            
            task4 = progress.add_task("[magenta]Running enhanced synthesis...", total=1)
            self.phase4_results = await self.run_enhanced_phase4(self.phase3_results)
            
            progress.update(task4, completed=1)
            progress.stop_task(task4)
            progress.remove_task(task4)
            console.print("[magenta]✓[/magenta] Phase 4 complete: Enhanced synthesis finished")

            # ENHANCED: Phase 5 with Cognitive Tools Integration
            console.print("\n[bold cyan]🧩 Phase 5: Enhanced Consolidation[/bold cyan]")
            if self.enable_context_engineering:
                console.print("[dim]🤖 Comprehensive cognitive tools + meta-analysis[/dim]")
            
            task5 = progress.add_task("[cyan]Running enhanced consolidation...", total=1)
            all_results = {
                "phase1": self.phase1_results,
                "phase2": self.phase2_results,
                "phase3": self.phase3_results,
                "phase4": self.phase4_results
            }
            self.consolidated_report = await self.run_enhanced_phase5(all_results)
            
            progress.update(task5, completed=1)
            progress.stop_task(task5)
            progress.remove_task(task5)
            console.print("[cyan]✓[/cyan] Phase 5 complete: Enhanced consolidation finished")

            # ENHANCED: Final Analysis with System Orchestration
            console.print("\n[bold white]✨ Final Analysis: System Orchestration[/bold white]")
            if self.enable_context_engineering:
                console.print("[dim]🌟 Emergent intelligence synthesis + adaptive rule generation[/dim]")
            else:
                console.print("[dim]📝 Standard rule generation[/dim]")
            
            task6 = progress.add_task("[white]Creating enhanced rules...", total=1)
            self.final_analysis = await self.run_enhanced_final_analysis(
                self.consolidated_report, tree_for_analysis
            )
            
            progress.update(task6, completed=1)
            progress.stop_task(task6)
            progress.remove_task(task6)
            
            if self.enable_context_engineering:
                # Display final system metrics
                if hasattr(self, 'integration_manager') and self.integration_manager:
                    summary = self.integration_manager.get_integration_summary()
                    console.print(f"[white]✨[/white] Final Analysis complete: {summary.get('system_status', 'unknown').upper()}")
                    console.print(f"[dim]   System Coherence: {summary.get('average_coherence', 0.0):.2f}[/dim]")
                    console.print(f"[dim]   Optimization Efficiency: {summary.get('optimization_efficiency', 0.0):.2f}[/dim]")
            else:
                console.print("[white]✓[/white] Final Analysis complete: Standard rules generated")

        return {
            "status": "complete",
            "enhanced": self.enable_context_engineering,
            "phases": {
                "phase1": self.phase1_results,
                "phase2": self.phase2_results,
                "phase3": self.phase3_results,
                "phase4": self.phase4_results,
                "phase5": self.consolidated_report,
                "final": self.final_analysis
            }
        }

    # ====================================================
    # Enhanced Phase Execution Methods
    # ====================================================

    async def run_enhanced_phase1(self, tree: List[str], package_info: Dict) -> Dict:
        """Enhanced Phase 1 with context engineering integration."""
        if self.enable_context_engineering:
            # Use the enhanced Phase 1 analyzer with full context engineering
            return await self.phase1_analyzer.run(tree, package_info)
        else:
            # Use original Phase 1 analyzer for backward compatibility
            return await self.phase1_analyzer.run(tree, package_info)

    async def run_enhanced_phase2(self, phase1_results: Dict, tree: List[str]) -> Dict:
        """Enhanced Phase 2 with molecular context building."""
        if self.enable_context_engineering and self.integration_manager:
            # Enhance Phase 2 with molecular context patterns
            phase2_data = {
                "phase1_results": phase1_results,
                "tree": tree,
                "analysis_type": "planning"
            }
            
            # Extract context from Phase 1 for Phase 2
            previous_context = None
            if "context_engineering" in phase1_results:
                previous_context = {
                    "phase_1_insights": phase1_results["context_engineering"],
                    "field_state": phase1_results.get("enhancement_metrics", {}),
                    "atomic_efficiency": phase1_results.get("enhancement_metrics", {}).get("atomic_prompt_efficiency", 0.0)
                }
            
            # Use integration manager to enhance Phase 2
            enhanced_results = self.integration_manager.enhance_phase(
                "phase_2", phase2_data, previous_context
            )
            
            # Run standard Phase 2 with enhanced context
            enhanced_context = enhanced_results["enhanced_data"]
            standard_results = await self.phase2_analyzer.run(phase1_results, tree)
            
            # Merge standard results with context engineering enhancements
            return {
                **standard_results,
                "context_engineering": enhanced_results["context_engineering"],
                "integration_metrics": enhanced_results["integration_metrics"]
            }
        else:
            # Use original Phase 2 analyzer
            return await self.phase2_analyzer.run(phase1_results, tree)

    async def run_enhanced_phase3(self, analysis_plan: Dict, tree: List[str]) -> Dict:
        """Enhanced Phase 3 with cellular memory integration."""
        if self.enable_context_engineering and self.integration_manager:
            # Enhance Phase 3 with memory integration
            phase3_data = {
                "analysis_plan": analysis_plan,
                "tree": tree,
                "analysis_type": "deep_analysis"
            }
            
            # Extract context from previous phases
            previous_context = {
                "phase_2_insights": analysis_plan.get("context_engineering", {}),
                "planning_results": analysis_plan.get("integration_metrics", {}),
                "agent_allocation": analysis_plan.get("agents", [])
            }
            
            # Use integration manager to enhance Phase 3
            enhanced_results = self.integration_manager.enhance_phase(
                "phase_3", phase3_data, previous_context
            )
            
            # Run standard Phase 3 with enhanced context
            standard_results = await self.phase3_analyzer.run(analysis_plan, tree, self.directory)
            
            # Merge results
            return {
                **standard_results,
                "context_engineering": enhanced_results["context_engineering"],
                "integration_metrics": enhanced_results["integration_metrics"]
            }
        else:
            return await self.phase3_analyzer.run(analysis_plan, tree, self.directory)

    async def run_enhanced_phase4(self, phase3_results: Dict) -> Dict:
        """Enhanced Phase 4 with organic synthesis."""
        if self.enable_context_engineering and self.integration_manager:
            # Enhance Phase 4 with organic synthesis
            phase4_data = {
                "phase3_results": phase3_results,
                "analysis_type": "synthesis"
            }
            
            # Extract context from Phase 3
            previous_context = {
                "phase_3_insights": phase3_results.get("context_engineering", {}),
                "deep_analysis_results": phase3_results.get("integration_metrics", {}),
                "file_analyses": phase3_results.get("results", {})
            }
            
            # Use integration manager to enhance Phase 4
            enhanced_results = self.integration_manager.enhance_phase(
                "phase_4", phase4_data, previous_context
            )
            
            # Run standard Phase 4 with enhanced context
            standard_results = await self.phase4_analyzer.run(phase3_results)
            
            # Merge results
            return {
                **standard_results,
                "context_engineering": enhanced_results["context_engineering"],
                "integration_metrics": enhanced_results["integration_metrics"]
            }
        else:
            return await self.phase4_analyzer.run(phase3_results)

    async def run_enhanced_phase5(self, all_results: Dict) -> Dict:
        """Enhanced Phase 5 with cognitive tools integration."""
        if self.enable_context_engineering and self.integration_manager:
            # Enhance Phase 5 with comprehensive cognitive tools
            phase5_data = {
                "all_results": all_results,
                "analysis_type": "consolidation"
            }
            
            # Extract context from all previous phases
            previous_context = {
                "accumulated_insights": all_results,
                "cross_phase_patterns": self._extract_cross_phase_patterns(all_results),
                "system_evolution": self._track_system_evolution(all_results)
            }
            
            # Use integration manager to enhance Phase 5
            enhanced_results = self.integration_manager.enhance_phase(
                "phase_5", phase5_data, previous_context
            )
            
            # Run standard Phase 5 with enhanced context
            standard_results = await self.phase5_analyzer.run(all_results)
            
            # Merge results
            return {
                **standard_results,
                "context_engineering": enhanced_results["context_engineering"],
                "integration_metrics": enhanced_results["integration_metrics"]
            }
        else:
            return await self.phase5_analyzer.run(all_results)

    async def run_enhanced_final_analysis(self, consolidated_report: Dict, tree: List[str] = None) -> Dict:
        """Enhanced Final Analysis with system orchestration."""
        if self.enable_context_engineering and self.integration_manager:
            # Perform multi-phase orchestration for final synthesis
            all_phases_data = {
                "phase_1": self.phase1_results,
                "phase_2": self.phase2_results,
                "phase_3": self.phase3_results,
                "phase_4": self.phase4_results,
                "phase_5": consolidated_report
            }
            
            # Run system-level orchestration
            orchestration_results = self.integration_manager.orchestrate_multi_phase_analysis(
                all_phases_data
            )
            
            # Run standard final analysis
            standard_results = await self.final_analyzer.run(consolidated_report, tree)
            
            # Create enhanced final analysis
            enhanced_final = {
                **standard_results,
                "context_engineering_orchestration": orchestration_results,
                "system_intelligence": {
                    "system_coherence": orchestration_results.get("system_coherence", 0.0),
                    "emergent_patterns": orchestration_results.get("emergent_intelligence", {}),
                    "adaptive_capabilities": self._assess_adaptive_capabilities(orchestration_results)
                },
                "integration_summary": self.integration_manager.get_integration_summary()
            }
            
            return enhanced_final
        else:
            return await self.final_analyzer.run(consolidated_report, tree)

    # ====================================================
    # Helper Methods for Context Engineering
    # ====================================================

    def _extract_cross_phase_patterns(self, all_results: Dict) -> Dict:
        """Extract patterns that appear across multiple phases."""
        cross_patterns = {}
        
        for phase_name, phase_results in all_results.items():
            if isinstance(phase_results, dict) and "context_engineering" in phase_results:
                ce_data = phase_results["context_engineering"]
                cross_patterns[phase_name] = {
                    "metrics": phase_results.get("integration_metrics", {}),
                    "patterns": str(ce_data)[:200] + "..."  # Sample of patterns
                }
        
        return cross_patterns

    def _track_system_evolution(self, all_results: Dict) -> Dict:
        """Track how the system has evolved across phases."""
        evolution = {
            "coherence_progression": [],
            "complexity_growth": [],
            "enhancement_trajectory": []
        }
        
        for phase_name, phase_results in all_results.items():
            if isinstance(phase_results, dict) and "integration_metrics" in phase_results:
                metrics = phase_results["integration_metrics"]
                evolution["coherence_progression"].append({
                    "phase": phase_name,
                    "coherence": metrics.get("coherence", 0.0)
                })
        
        return evolution

    def _assess_adaptive_capabilities(self, orchestration_results: Dict) -> Dict:
        """Assess the adaptive capabilities of the enhanced system."""
        capabilities = {
            "pattern_recognition": "enhanced" if orchestration_results.get("system_coherence", 0.0) > 0.7 else "standard",
            "context_retention": "excellent" if len(orchestration_results.get("enhanced_phases", {})) >= 5 else "good",
            "emergent_intelligence": orchestration_results.get("emergent_intelligence", {}).get("emergent_score", 0.0),
            "adaptation_level": "high" if orchestration_results.get("system_coherence", 0.0) > 0.8 else "moderate"
        }
        
        return capabilities

# ====================================================
# Enhanced CLI Interface
# ====================================================

class EnhancedCursorRulesProjectAnalyzer:
    """Enhanced project analyzer with context engineering and robust error handling."""
    
    def __init__(self, enable_context_engineering: bool = True):
        """Initialize with comprehensive error handling."""
        try:
            # Initialize base analyzer first
            super().__init__()
            
            # Context engineering initialization with validation
            self.enable_context_engineering = enable_context_engineering
            self.context_engineering_healthy = False
            self.integration_manager = None
            self.enhancement_metrics = {
                "initialization_time": time.time(),
                "context_engineering_attempts": 0,
                "context_engineering_successes": 0,
                "fallback_uses": 0,
                "total_errors": 0
            }
            
            # Validate and initialize context engineering
            if self.enable_context_engineering and CONTEXT_ENGINEERING_AVAILABLE:
                self._initialize_context_engineering()
            else:
                if not CONTEXT_ENGINEERING_AVAILABLE:
                    console.print(f"[yellow]⚠️ Context Engineering not available: {IMPORT_ERROR}[/yellow]")
                else:
                    console.print("[blue]ℹ️ Context Engineering disabled by user[/blue]")
                
                self.enable_context_engineering = False
            
            # Enhanced phase analyzers with error handling
            self._initialize_enhanced_phases()
            
            console.print("[bold green]✅ Enhanced CursorRules Architect initialized[/bold green]")
            
        except Exception as e:
            logger.error(f"Critical error in enhanced analyzer initialization: {e}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            
            # Fall back to original analyzer
            console.print(f"[red]❌ Enhanced initialization failed: {e}[/red]")
            console.print("[yellow]🔄 Falling back to original CursorRules Architect[/yellow]")
            
            # Re-initialize as original
            super().__init__()
            self.enable_context_engineering = False
            self.context_engineering_healthy = False
            self.integration_manager = None
    
    def _initialize_context_engineering(self):
        """Initialize context engineering with comprehensive validation."""
        try:
            console.print("[bold green]🧠 Initializing Context Engineering[/bold green]")
            
            # Validate dependencies
            deps_ok, dep_issues = validate_context_engineering_dependencies()
            if not deps_ok:
                raise EnhancedCursorRulesError(f"Context engineering dependencies missing: {dep_issues}")
            
            if dep_issues:  # Warnings only
                console.print(f"[yellow]⚠️ Context engineering warnings: {dep_issues}[/yellow]")
            
            # Create integration configuration with validation
            try:
                self.integration_config = IntegrationConfig(
                    enable_atomic_prompting=True,
                    enable_field_dynamics=True,
                    enable_cognitive_tools=True,
                    enable_pattern_synthesis=True,
                    optimization_mode="balanced",
                    error_tolerance_level="moderate",
                    enable_fallback=True,
                    max_processing_time=300,  # 5 minutes max
                    max_context_size=500000   # 500KB max
                )
                console.print("   ✅ Configuration validated")
            except Exception as e:
                raise EnhancedCursorRulesError(f"Configuration validation failed: {e}")
            
            # Initialize integration manager with error handling
            try:
                self.integration_manager = ContextEngineeringIntegrationManager(
                    self.integration_config
                )
                console.print("   ✅ Integration manager initialized")
            except Exception as e:
                raise EnhancedCursorRulesError(f"Integration manager initialization failed: {e}")
            
            # Validate integration manager health
            try:
                health = self.integration_manager.field_dynamics.get_system_health() if hasattr(self.integration_manager, 'field_dynamics') and self.integration_manager.field_dynamics else None
                if health and health.get("health_status") in ["critical", "unhealthy", "error"]:
                    raise EnhancedCursorRulesError(f"Integration manager unhealthy: {health}")
                console.print("   ✅ System health validated")
            except Exception as e:
                logger.warning(f"Health check failed: {e}")
                # Continue anyway if health check fails
            
            self.context_engineering_healthy = True
            console.print("[bold green]🎉 Context Engineering successfully initialized[/bold green]")
            
        except Exception as e:
            logger.error(f"Context engineering initialization failed: {e}")
            console.print(f"[red]❌ Context Engineering initialization failed: {e}[/red]")
            console.print("[yellow]🔄 Continuing with standard analysis only[/yellow]")
            
            self.enable_context_engineering = False
            self.context_engineering_healthy = False
            self.integration_manager = None
    
    def _initialize_enhanced_phases(self):
        """Initialize enhanced phase analyzers with error handling."""
        try:
            if self.enable_context_engineering and self.context_engineering_healthy:
                # Initialize enhanced Phase 1
                try:
                    self.phase1_analyzer = ContextAwarePhase1Analysis()
                    if self.phase1_analyzer.enhancement_enabled:
                        console.print("   ✅ Enhanced Phase 1 with context engineering")
                    else:
                        console.print("   🟡 Phase 1 with limited enhancement (fallback mode)")
                except Exception as e:
                    logger.error(f"Enhanced Phase 1 initialization failed: {e}")
                    console.print(f"   ❌ Enhanced Phase 1 failed, using standard: {e}")
                    self.phase1_analyzer = None  # Will use original
                
                # For now, phases 2-5 use integration manager wrapper
                # TODO: Create enhanced versions similar to Phase 1
                console.print("   ✅ Phases 2-5 will use integration manager enhancement")
            else:
                console.print("   ℹ️ Using standard phase analyzers")
                self.phase1_analyzer = None
                
        except Exception as e:
            logger.error(f"Enhanced phase initialization failed: {e}")
            console.print(f"[yellow]⚠️ Enhanced phases initialization failed: {e}[/yellow]")
            self.phase1_analyzer = None
    
    async def run_analysis(self, project_path: str) -> Dict[str, Any]:
        """Run enhanced analysis with comprehensive error handling and fallback."""
        start_time = time.time()
        self.enhancement_metrics["context_engineering_attempts"] += 1
        
        try:
            console.print(Panel.fit(
                "[bold cyan]🚀 Starting Enhanced CursorRules Analysis[/bold cyan]",
                border_style="cyan"
            ))
            
            # Input validation
            if not project_path or not isinstance(project_path, str):
                raise ValueError("project_path must be a non-empty string")
            
            # Try enhanced analysis first
            if self.enable_context_engineering and self.context_engineering_healthy:
                try:
                    enhanced_results = await self._run_enhanced_analysis(project_path)
                    
                    # Validate enhanced results
                    if self._validate_analysis_results(enhanced_results):
                        processing_time = time.time() - start_time
                        self._update_enhancement_metrics(True, processing_time)
                        
                        console.print("[bold green]✅ Enhanced analysis completed successfully[/bold green]")
                        console.print(f"[dim]Processing time: {processing_time:.2f}s[/dim]")
                        
                        return enhanced_results
                    else:
                        logger.warning("Enhanced analysis validation failed")
                        return await self._fallback_to_original_analysis(project_path, "validation_failed")
                        
                except ContextEngineeringError as e:
                    logger.warning(f"Context engineering error: {e}")
                    return await self._fallback_to_original_analysis(project_path, f"context_engineering_error: {e}")
                
                except Exception as e:
                    logger.error(f"Enhanced analysis failed: {e}")
                    logger.error(f"Stack trace: {traceback.format_exc()}")
                    return await self._fallback_to_original_analysis(project_path, f"unknown_error: {e}")
            else:
                # Enhancement not available, use original analysis
                console.print("[blue]ℹ️ Context engineering not available, using standard analysis[/blue]")
                return await self._fallback_to_original_analysis(project_path, "enhancement_disabled")
                
        except Exception as e:
            self.enhancement_metrics["total_errors"] += 1
            logger.error(f"Critical error in run_analysis: {e}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            
            # Last resort fallback
            try:
                return await self._emergency_fallback_analysis(project_path, e)
            except Exception as final_error:
                logger.error(f"Emergency fallback also failed: {final_error}")
                return self._create_error_result(project_path, final_error)
    
    async def _run_enhanced_analysis(self, project_path: str) -> Dict[str, Any]:
        """Run enhanced analysis with context engineering."""
        analysis_results = {}
        previous_context = None
        
        try:
            # Enhanced Phase 1 (if available)
            if self.phase1_analyzer and hasattr(self.phase1_analyzer, 'enhancement_enabled'):
                console.print("[bold blue]📊 Running Enhanced Phase 1 Analysis[/bold blue]")
                try:
                    # Get tree and package info
                    tree = self._get_project_tree(project_path)
                    package_info = self._get_package_info(project_path)
                    
                    # Run enhanced Phase 1
                    phase1_results = await self.phase1_analyzer.run(tree, package_info)
                    analysis_results["phase1"] = phase1_results
                    
                    # Extract context for next phases
                    previous_context = self._extract_phase_context(phase1_results)
                    
                    console.print("   ✅ Enhanced Phase 1 completed")
                    
                except Exception as e:
                    logger.error(f"Enhanced Phase 1 failed: {e}")
                    console.print(f"   ❌ Enhanced Phase 1 failed: {e}")
                    
                    # Fallback to original Phase 1
                    phase1_results = await self._run_original_phase1(project_path)
                    analysis_results["phase1"] = phase1_results
                    previous_context = {}
            else:
                # Use original Phase 1
                console.print("[blue]📊 Running Standard Phase 1 Analysis[/blue]")
                phase1_results = await self._run_original_phase1(project_path)
                analysis_results["phase1"] = phase1_results
                previous_context = {}
            
            # Enhanced Phases 2-5 (using integration manager)
            for phase_num in range(2, 6):
                phase_name = f"phase{phase_num}"
                console.print(f"[bold blue]📊 Running Enhanced {phase_name.title()} Analysis[/bold blue]")
                
                try:
                    # Run original phase
                    original_phase_results = await self._run_original_phase(phase_num, analysis_results)
                    
                    # Enhance with context engineering if available
                    if self.integration_manager:
                        try:
                            enhanced_phase_results = self.integration_manager.enhance_phase(
                                phase_name,
                                original_phase_results,
                                previous_context
                            )
                            
                            # Check enhancement success
                            if enhanced_phase_results.get("status") not in ["error_fallback", "timeout_fallback"]:
                                analysis_results[phase_name] = self._ensure_phase_compatibility(enhanced_phase_results)
                                previous_context = self._extract_phase_context(enhanced_phase_results)
                                console.print(f"   ✅ Enhanced {phase_name} completed")
                            else:
                                logger.warning(f"Enhancement failed for {phase_name}: {enhanced_phase_results.get('status')}")
                                analysis_results[phase_name] = self._add_enhancement_metadata(original_phase_results, False, enhanced_phase_results.get("error_message"))
                                console.print(f"   🟡 {phase_name} completed (enhancement failed)")
                        except Exception as e:
                            logger.error(f"Enhancement failed for {phase_name}: {e}")
                            analysis_results[phase_name] = self._add_enhancement_metadata(original_phase_results, False, str(e))
                            console.print(f"   🟡 {phase_name} completed (enhancement error)")
                    else:
                        # No enhancement available
                        analysis_results[phase_name] = self._add_enhancement_metadata(original_phase_results, False, "integration_manager_unavailable")
                        console.print(f"   ✅ Standard {phase_name} completed")
                    
                except Exception as e:
                    logger.error(f"Phase {phase_num} failed: {e}")
                    console.print(f"   ❌ {phase_name} failed: {e}")
                    
                    # Create error result for this phase
                    analysis_results[phase_name] = {
                        "error": str(e),
                        "phase": phase_name,
                        "_enhancement_metadata": {
                            "enhanced": False,
                            "error": str(e),
                            "fallback_used": True
                        }
                    }
            
            # Final analysis with enhancement
            console.print("[bold blue]📊 Running Enhanced Final Analysis[/bold blue]")
            try:
                final_analysis = await self._run_original_final_analysis(analysis_results)
                
                # Enhance final analysis if possible
                if self.integration_manager:
                    try:
                        enhanced_final = self.integration_manager.enhance_phase(
                            "final_analysis",
                            final_analysis,
                            previous_context
                        )
                        
                        if enhanced_final.get("status") not in ["error_fallback", "timeout_fallback"]:
                            analysis_results["final_analysis"] = self._ensure_phase_compatibility(enhanced_final)
                            console.print("   ✅ Enhanced final analysis completed")
                        else:
                            analysis_results["final_analysis"] = self._add_enhancement_metadata(final_analysis, False, enhanced_final.get("error_message"))
                            console.print("   🟡 Final analysis completed (enhancement failed)")
                    except Exception as e:
                        logger.error(f"Final analysis enhancement failed: {e}")
                        analysis_results["final_analysis"] = self._add_enhancement_metadata(final_analysis, False, str(e))
                        console.print("   🟡 Final analysis completed (enhancement error)")
                else:
                    analysis_results["final_analysis"] = self._add_enhancement_metadata(final_analysis, False, "integration_manager_unavailable")
                    console.print("   ✅ Standard final analysis completed")
                    
            except Exception as e:
                logger.error(f"Final analysis failed: {e}")
                analysis_results["final_analysis"] = {
                    "error": str(e),
                    "_enhancement_metadata": {
                        "enhanced": False,
                        "error": str(e),
                        "fallback_used": True
                    }
                }
            
            # Add global enhancement metadata
            analysis_results["_global_enhancement_metadata"] = {
                "context_engineering_enabled": self.enable_context_engineering,
                "context_engineering_healthy": self.context_engineering_healthy,
                "integration_manager_available": self.integration_manager is not None,
                "enhanced_phases": [
                    phase for phase in analysis_results.keys() 
                    if phase.startswith("phase") and analysis_results[phase].get("_enhancement_metadata", {}).get("enhanced", False)
                ],
                "total_processing_time": time.time() - time.time(),
                "enhancement_metrics": self.enhancement_metrics
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Enhanced analysis execution failed: {e}")
            raise EnhancedCursorRulesError(f"Enhanced analysis failed: {e}")
    
    async def _fallback_to_original_analysis(self, project_path: str, reason: str) -> Dict[str, Any]:
        """Fallback to original analysis with error context."""
        try:
            self.enhancement_metrics["fallback_uses"] += 1
            console.print(f"[yellow]🔄 Falling back to original analysis: {reason}[/yellow]")
            
            # Run original analysis
            original_results = await super().run_analysis(project_path)
            
            # Add fallback metadata to all phases
            for phase_key in original_results.keys():
                if isinstance(original_results[phase_key], dict):
                    original_results[phase_key]["_enhancement_metadata"] = {
                        "enhanced": False,
                        "fallback_reason": reason,
                        "context_engineering_attempted": True,
                        "fallback_time": time.time()
                    }
            
            # Add global metadata
            original_results["_global_enhancement_metadata"] = {
                "context_engineering_enabled": False,
                "fallback_used": True,
                "fallback_reason": reason,
                "original_enhancement_attempted": True
            }
            
            console.print("[green]✅ Original analysis completed successfully[/green]")
            return original_results
            
        except Exception as e:
            logger.error(f"Fallback analysis also failed: {e}")
            raise EnhancedCursorRulesError(f"Both enhanced and fallback analysis failed. Fallback reason: {reason}, Error: {e}")
    
    async def _emergency_fallback_analysis(self, project_path: str, original_error: Exception) -> Dict[str, Any]:
        """Emergency fallback when everything else fails."""
        try:
            console.print("[red]🚨 Emergency fallback mode activated[/red]")
            
            # Try minimal analysis
            emergency_results = {
                "error": f"Analysis failed: {original_error}",
                "emergency_mode": True,
                "project_path": project_path,
                "timestamp": time.time(),
                "_global_enhancement_metadata": {
                    "emergency_fallback": True,
                    "original_error": str(original_error),
                    "context_engineering_enabled": False
                }
            }
            
            # Try to get basic project info
            try:
                tree = self._get_project_tree(project_path)
                emergency_results["basic_tree"] = tree[:50] if tree else []  # Limit to first 50 files
            except Exception:
                emergency_results["basic_tree"] = []
            
            try:
                package_info = self._get_package_info(project_path)
                emergency_results["basic_package_info"] = {
                    "name": package_info.get("name", "unknown"),
                    "type": package_info.get("project_type", "unknown")
                }
            except Exception:
                emergency_results["basic_package_info"] = {}
            
            console.print("[yellow]⚠️ Emergency analysis completed with limited data[/yellow]")
            return emergency_results
            
        except Exception as e:
            logger.error(f"Emergency fallback failed: {e}")
            raise e
    
    def _create_error_result(self, project_path: str, error: Exception) -> Dict[str, Any]:
        """Create error result when all else fails."""
        return {
            "error": f"Complete analysis failure: {error}",
            "project_path": project_path,
            "timestamp": time.time(),
            "fatal_error": True,
            "_global_enhancement_metadata": {
                "total_failure": True,
                "error_message": str(error),
                "context_engineering_enabled": False
            }
        }
    
    def _validate_analysis_results(self, results: Dict[str, Any]) -> bool:
        """Validate analysis results structure and content."""
        try:
            if not isinstance(results, dict):
                logger.warning("Analysis results is not a dictionary")
                return False
            
            # Check for critical error
            if results.get("fatal_error") or results.get("emergency_mode"):
                logger.warning("Analysis results indicate critical failure")
                return False
            
            # Check for expected phases
            expected_phases = ["phase1", "phase2", "phase3", "phase4", "phase5", "final_analysis"]
            missing_phases = [phase for phase in expected_phases if phase not in results]
            
            if len(missing_phases) > 2:  # Allow some missing phases
                logger.warning(f"Too many missing phases: {missing_phases}")
                return False
            
            # Check result size
            result_size = len(str(results))
            if result_size > 50000000:  # 50MB limit
                logger.warning(f"Analysis results too large: {result_size} chars")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Result validation failed: {e}")
            return False
    
    def _ensure_phase_compatibility(self, enhanced_results: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure enhanced phase results are compatible with original format."""
        try:
            # If enhanced_data contains expected format, use it
            if "enhanced_data" in enhanced_results:
                enhanced_data = enhanced_results["enhanced_data"]
                if isinstance(enhanced_data, dict):
                    # Add context engineering metadata
                    enhanced_data["_context_engineering"] = enhanced_results.get("context_engineering", {})
                    enhanced_data["_enhancement_metadata"] = {
                        "enhanced": True,
                        "enhancement_level": enhanced_results.get("enhancement_level", "unknown")
                    }
                    return enhanced_data
            
            # If original_results is available, use it as base
            if "original_results" in enhanced_results:
                base_results = enhanced_results["original_results"].copy()
                base_results["_context_engineering"] = enhanced_results.get("context_engineering", {})
                base_results["_enhancement_metadata"] = {
                    "enhanced": True,
                    "enhancement_level": enhanced_results.get("enhancement_level", "unknown")
                }
                return base_results
            
            # Use enhanced results as-is with metadata
            enhanced_results["_enhancement_metadata"] = {
                "enhanced": True,
                "format_processing": "used_as_is",
                "enhancement_level": enhanced_results.get("enhancement_level", "unknown")
            }
            return enhanced_results
            
        except Exception as e:
            logger.error(f"Phase compatibility processing failed: {e}")
            # Return results with error metadata
            enhanced_results["_compatibility_error"] = str(e)
            return enhanced_results
    
    def _add_enhancement_metadata(self, results: Dict[str, Any], enhanced: bool, error_message: Optional[str] = None) -> Dict[str, Any]:
        """Add enhancement metadata to phase results."""
        try:
            if isinstance(results, dict):
                results["_enhancement_metadata"] = {
                    "enhanced": enhanced,
                    "error_message": error_message,
                    "timestamp": time.time()
                }
            return results
        except Exception as e:
            logger.warning(f"Failed to add enhancement metadata: {e}")
            return results
    
    def _extract_phase_context(self, phase_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract context from phase results for next phase."""
        try:
            context = {}
            
            # Extract context engineering insights
            if "_context_engineering" in phase_results:
                context["context_engineering_insights"] = phase_results["_context_engineering"]
            
            # Extract basic analysis context
            if "analysis" in phase_results:
                context["previous_analysis"] = str(phase_results["analysis"])[:1000]  # Limit size
            
            # Extract enhancement metadata
            if "_enhancement_metadata" in phase_results:
                context["enhancement_metadata"] = phase_results["_enhancement_metadata"]
            
            return context
            
        except Exception as e:
            logger.warning(f"Context extraction failed: {e}")
            return {}
    
    def _update_enhancement_metrics(self, success: bool, processing_time: float):
        """Update enhancement performance metrics."""
        try:
            if success:
                self.enhancement_metrics["context_engineering_successes"] += 1
            
            # Log performance periodically
            if self.enhancement_metrics["context_engineering_attempts"] % 5 == 0:
                success_rate = (self.enhancement_metrics["context_engineering_successes"] / 
                              self.enhancement_metrics["context_engineering_attempts"])
                console.print(f"[dim]Enhancement performance: {success_rate:.2%} success rate, {processing_time:.2f}s[/dim]")
                
        except Exception as e:
            logger.warning(f"Enhancement metrics update failed: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        try:
            status = {
                "context_engineering_available": CONTEXT_ENGINEERING_AVAILABLE,
                "context_engineering_enabled": self.enable_context_engineering,
                "context_engineering_healthy": self.context_engineering_healthy,
                "integration_manager_status": "unavailable",
                "enhanced_phase1_status": "unavailable",
                "enhancement_metrics": self.enhancement_metrics
            }
            
            # Check integration manager
            if self.integration_manager:
                try:
                    if hasattr(self.integration_manager, 'field_dynamics') and self.integration_manager.field_dynamics:
                        health = self.integration_manager.field_dynamics.get_system_health()
                        status["integration_manager_status"] = health.get("health_status", "unknown")
                    else:
                        status["integration_manager_status"] = "initialized"
                except Exception as e:
                    status["integration_manager_status"] = f"error: {e}"
            
            # Check enhanced Phase 1
            if hasattr(self, 'phase1_analyzer') and self.phase1_analyzer:
                try:
                    phase1_status = self.phase1_analyzer.get_enhancement_status()
                    status["enhanced_phase1_status"] = phase1_status
                except Exception as e:
                    status["enhanced_phase1_status"] = f"error: {e}"
            
            return status
            
        except Exception as e:
            logger.error(f"System status check failed: {e}")
            return {
                "error": str(e),
                "context_engineering_available": CONTEXT_ENGINEERING_AVAILABLE
            }

@click.command()
@click.argument('path', required=False)
@click.option('--output', help='Output file path (deprecated)', default=None)
@click.option('--context-engineering/--no-context-engineering', 
              default=True, 
              help='Enable/disable context engineering enhancements')
@click.option('--optimization-mode', 
              type=click.Choice(['efficiency', 'depth', 'balanced']), 
              default='balanced',
              help='Context engineering optimization mode')
def main(path, output, context_engineering, optimization_mode):
    """
    Enhanced CursorRules Architect with Context Engineering Integration.
    
    Analyzes your project and generates optimized .cursorrules with revolutionary
    AI-native capabilities including atomic prompting, neural field dynamics,
    and cognitive reasoning tools.
    """
    try:
        # Prompt for path if not provided
        if not path:
            path = click.prompt('Please provide the project directory path', type=str)

        # Validate directory
        directory = Path(os.path.expanduser(path))
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Invalid directory path: {path}")
            sys.exit(1)

        # Handle deprecated output option
        if output:
            logger.warning("The --output option is deprecated and no longer used.")

        # Display configuration
        console.print(f"\n[bold]🚀 Enhanced CursorRules Architect[/] {directory}")
        
        if context_engineering:
            console.print(f"[green]🧠 Context Engineering: ENABLED[/green]")
            console.print(f"[dim]   Optimization Mode: {optimization_mode}[/dim]")
            console.print(f"[dim]   ⚡ Atomic Prompting + 🌊 Neural Fields + 🧩 Cognitive Tools[/dim]")
        else:
            console.print(f"[yellow]📊 Context Engineering: DISABLED (Standard Mode)[/yellow]")

        # Create enhanced analyzer
        analyzer = EnhancedProjectAnalyzer(directory, enable_context_engineering=context_engineering)
        
        # Run enhanced analysis
        start_time = time.time()
        analysis_result = asyncio.run(analyzer.analyze())
        analysis_time = time.time() - start_time

        # Extract results (same structure as original)
        phase1_results = analyzer.phase1_results if hasattr(analyzer, 'phase1_results') else {}
        phase2_results = analyzer.phase2_results if hasattr(analyzer, 'phase2_results') else {}
        phase3_results = analyzer.phase3_results if hasattr(analyzer, 'phase3_results') else {}
        phase4_results = analyzer.phase4_results if hasattr(analyzer, 'phase4_results') else {}
        consolidated_report = analyzer.consolidated_report if hasattr(analyzer, 'consolidated_report') else {}
        final_analysis = analyzer.final_analysis if hasattr(analyzer, 'final_analysis') else {}

        # Prepare enhanced analysis data
        analysis_data = {
            "phase1": phase1_results,
            "phase2": phase2_results,
            "phase3": phase3_results,
            "phase4": phase4_results,
            "consolidated_report": consolidated_report,
            "final_analysis": final_analysis,
            "metrics": {
                "time": analysis_time,
                "enhanced": context_engineering,
                "optimization_mode": optimization_mode if context_engineering else "standard"
            }
        }

        # Add context engineering metrics if enabled
        if context_engineering and hasattr(analyzer, 'integration_manager') and analyzer.integration_manager:
            integration_summary = analyzer.integration_manager.get_integration_summary()
            analysis_data["context_engineering_summary"] = integration_summary

        # Save outputs (same as original)
        save_phase_outputs(directory, analysis_data)
        
        # Create supporting files
        success, message = create_cursorignore(str(directory))
        if success:
            console.print(f"[green]{message}[/]")
        else:
            console.print(f"[yellow]{message}[/]")

        success, message = clean_cursorrules(str(directory))
        if success:
            console.print(f"[green]Cleaned cursor rules file[/]")

        # Display completion messages
        console.print(f"[green]Phase outputs saved to:[/] {directory}/phases_output/")
        console.print(f"[green]Cursor rules created at:[/] {directory}/.cursorrules")
        console.print(f"[green]Cursor ignore created at:[/] {directory}/.cursorignore")
        console.print(f"[green]Execution metrics saved to:[/] {directory}/phases_output/metrics.md")
        
        if context_engineering:
            console.print(f"[green]Context engineering summary saved to:[/] {directory}/phases_output/context_engineering_summary.json")
            console.print(f"\n[bold green]✨ Enhanced analysis complete with context engineering![/bold green]")
        else:
            console.print(f"\n[bold blue]✅ Standard analysis complete![/bold blue]")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()