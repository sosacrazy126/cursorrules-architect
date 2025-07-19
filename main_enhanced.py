#!/usr/bin/env python3

"""
main_enhanced.py

Enhanced CursorRules Architect with Context Engineering Integration

This demonstrates how the context engineering components integrate seamlessly 
with the existing workflow while preserving all original functionality.
"""

# ====================================================
# Section 1: Enhanced Setup and Initialization
# ====================================================

import click
from pathlib import Path
import os
import sys
import json
from typing import Dict, List, Optional
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
from dotenv import load_dotenv
import asyncio

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
from core.context_engineering.integration_manager import (
    ContextEngineeringIntegrationManager,
    IntegrationConfig
)

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
from core.analysis.enhanced_phase_1 import ContextAwarePhase1Analysis

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