#!/usr/bin/env python3
"""CursorRules Architect - AI-powered project analysis and rules generation."""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import click
from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

from config.agents import MODEL_CONFIG, ModelProvider
from config.exclusions import EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS
from core.analysis import (
    Phase1Analysis,
    Phase2Analysis,
    Phase3Analysis,
    Phase4Analysis,
    Phase5Analysis,
    FinalAnalysis
)
from core.agents.openai import OpenAIAgent
from core.utils.file_creation.cursorignore import create_cursorignore
from core.utils.file_creation.phases_output import save_phase_outputs
from core.utils.tools.clean_cursorrules import clean_cursorrules
from core.utils.tools.model_config_helper import get_model_config_name
from core.utils.tools.tree_generator import get_project_tree

console = Console()

class HTTPRequestFilter(logging.Filter):
    """Filter HTTP request logs to show only essential information."""
    
    API_PROVIDERS = {
        "api.openai.com": "Using OpenAI model",
        "api.anthropic.com": "Using Anthropic model", 
        "generativelanguage.googleapis.com": "Using Google Gemini model",
        "api.deepseek.com": "Using DeepSeek model"
    }
    
    def filter(self, record):
        if "HTTP Request:" in record.getMessage():
            msg = record.getMessage()
            for api_url, provider_msg in self.API_PROVIDERS.items():
                if api_url in msg:
                    record.msg = provider_msg
                    return True
            return False
        return True

def setup_logging():
    """Configure logging with HTTP request filtering."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_time=False, markup=True)]
    )
    
    logger = logging.getLogger("project_extractor")
    logger.addFilter(HTTPRequestFilter())
    
    # Suppress verbose logs from HTTP libraries
    for logger_name in ["openai", "httpx", "httpcore", "anthropic", "google", "genai"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    
    return logger

def load_environment():
    """Load environment variables from .env file if it exists."""
    if os.path.exists('.env'):
        load_dotenv()
        logging.info("Loaded environment variables from .env file")
    else:
        logging.warning("No .env file found. Make sure API keys are set in environment variables.")


def initialize_clients(logger):
    """Initialize AI clients only for providers that are actually used."""
    used_providers = {config.provider for config in MODEL_CONFIG.values()}
    clients = {}
    
    if ModelProvider.OPENAI in used_providers:
        clients['openai'] = OpenAI()
        logger.info("Initialized OpenAI client")
    else:
        logger.info("OpenAI client not initialized (not used in any phase)")
    
    if ModelProvider.ANTHROPIC in used_providers:
        clients['anthropic'] = Anthropic()
        logger.info("Initialized Anthropic client")
    else:
        logger.info("Anthropic client not initialized (not used in any phase)")
    
    return clients


class ProjectAnalyzer:
    """Orchestrates the complete project analysis workflow."""
    
    def __init__(self, directory: Path):
        """Initialize the ProjectAnalyzer with the specified directory.
        
        Args:
            directory: Path to the project directory to analyze
        """
        self.directory = directory
        self._results = {
            'phase1': {},
            'phase2': {},
            'phase3': {},
            'phase4': {},
            'consolidated_report': {},
            'final_analysis': {}
        }
        self._analyzers = {
            'phase1': Phase1Analysis(),
            'phase2': Phase2Analysis(),
            'phase3': Phase3Analysis(),
            'phase4': Phase4Analysis(),
            'phase5': Phase5Analysis(),
            'final': FinalAnalysis()
        }
    
    @property
    def phase1_results(self):
        return self._results['phase1']
    
    @phase1_results.setter
    def phase1_results(self, value):
        self._results['phase1'] = value
    
    @property
    def phase2_results(self):
        return self._results['phase2']
    
    @phase2_results.setter
    def phase2_results(self, value):
        self._results['phase2'] = value
    
    @property
    def phase3_results(self):
        return self._results['phase3']
    
    @phase3_results.setter
    def phase3_results(self, value):
        self._results['phase3'] = value
    
    @property
    def phase4_results(self):
        return self._results['phase4']
    
    @phase4_results.setter
    def phase4_results(self, value):
        self._results['phase4'] = value
        
    @property
    def consolidated_report(self):
        return self._results['consolidated_report']
    
    @consolidated_report.setter
    def consolidated_report(self, value):
        self._results['consolidated_report'] = value
        
    @property
    def final_analysis(self):
        return self._results['final_analysis']
    
    @final_analysis.setter
    def final_analysis(self, value):
        self._results['final_analysis'] = value

    async def run_phase1(self, tree: List[str], package_info: Dict) -> Dict:
        """Run Initial Discovery Phase."""
        return await self._analyzers['phase1'].run(tree, package_info)

    async def run_phase2(self, phase1_results: Dict, tree: List[str]) -> Dict:
        """Run Methodical Planning Phase."""
        return await self._analyzers['phase2'].run(phase1_results, tree)

    async def run_phase3(self, analysis_plan: Dict, tree: List[str]) -> Dict:
        """Run Deep Analysis Phase."""
        return await self._analyzers['phase3'].run(analysis_plan, tree, self.directory)

    async def run_phase4(self, phase3_results: Dict) -> Dict:
        """Run Synthesis Phase."""
        return await self._analyzers['phase4'].run(phase3_results)

    async def run_phase5(self, all_results: Dict) -> Dict:
        """Run Consolidation Phase."""
        return await self._analyzers['phase5'].run(all_results)

    async def run_final_analysis(self, consolidated_report: Dict, tree: List[str] = None) -> Dict:
        """Run Final Analysis Phase."""
        return await self._analyzers['final'].run(consolidated_report, tree)

    async def analyze(self) -> str:
        """Run complete analysis workflow"""
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),  # Show a spinner animation
            TextColumn("[progress.description]{task.description}"),  # Show a description of the current task
            console=console  # Use the `rich` console for output
        ) as progress:

            # --- Phase 1: Initial Discovery ---
            console.print("\n[bold green]Phase 1: Initial Discovery[/bold green]")
            console.print("[dim]Running three concurrent agents: Structure Agent, Dependency Agent, and Tech Stack Agent...[/dim]")
            
            task1 = progress.add_task("[green]Running analysis agents...", total=1)  # Add a task for Phase 1 with a total
            tree_with_delimiters = get_project_tree(self.directory)  # Generate the directory tree using the enhanced tree generator
            
            # Remove delimiters for analysis
            tree_for_analysis = tree_with_delimiters
            if len(tree_with_delimiters) >= 2 and tree_with_delimiters[0] == "<@tree_generator.py project_structure>" and tree_with_delimiters[-1] == "</project_structure>":
                tree_for_analysis = tree_with_delimiters[1:-1]
            
            package_info = {}  # Placeholder for package information (you would parse package.json here)
            self.phase1_results = await self.run_phase1(tree_for_analysis, package_info)  # Run Phase 1
            
            # Complete and remove the task
            progress.update(task1, completed=1)
            progress.stop_task(task1)
            progress.remove_task(task1)
            console.print("[green]✓[/green] Phase 1 complete: All three agents have finished their analysis")

            # --- Phase 2: Methodical Planning ---
            console.print("\n[bold blue]Phase 2: Methodical Planning[/bold blue]")
            console.print("[dim]Creating a detailed plan for deeper analysis...[/dim]")
            
            task2 = progress.add_task("[blue]Creating analysis plan...", total=1)
            self.phase2_results = await self.run_phase2(self.phase1_results, tree_for_analysis)
            
            # Complete and remove the task
            progress.update(task2, completed=1)
            progress.stop_task(task2)
            progress.remove_task(task2)
            console.print("[blue]✓[/blue] Phase 2 complete: Analysis plan created")

            # --- Phase 3: Deep Analysis ---
            console.print("\n[bold yellow]Phase 3: Deep Analysis[/bold yellow]")
            
            # Check if we have defined agents
            agent_count = len(self.phase2_results.get("agents", []))
            if agent_count > 0:
                console.print(f"[dim]Running {agent_count} specialized analysis agents on their assigned files...[/dim]")
            else:
                console.print("[dim]Running specialized analysis on project files...[/dim]")
                
            task3 = progress.add_task("[yellow]Analyzing files in depth...", total=1)
            self.phase3_results = await self.run_phase3(self.phase2_results, tree_for_analysis)
            
            # Complete and remove the task
            progress.update(task3, completed=1)
            progress.stop_task(task3)
            progress.remove_task(task3)
            console.print("[yellow]✓[/yellow] Phase 3 complete: In-depth analysis finished")

            # --- Phase 4: Synthesis ---
            console.print("\n[bold magenta]Phase 4: Synthesis[/bold magenta]")
            console.print("[dim]Synthesizing findings from all previous analyses...[/dim]")
            
            task4 = progress.add_task("[magenta]Synthesizing findings...", total=1)
            self.phase4_results = await self.run_phase4(self.phase3_results)
            
            # Complete and remove the task
            progress.update(task4, completed=1)
            progress.stop_task(task4)
            progress.remove_task(task4)
            console.print("[magenta]✓[/magenta] Phase 4 complete: Findings synthesized")

            # --- Phase 5: Consolidation ---
            console.print("\n[bold cyan]Phase 5: Consolidation[/bold cyan]")
            console.print("[dim]Consolidating all results into a comprehensive report...[/dim]")
            
            task5 = progress.add_task("[cyan]Consolidating results...", total=1)
            all_results = {  # Combine the results from all previous phases
                "phase1": self.phase1_results,
                "phase2": self.phase2_results,
                "phase3": self.phase3_results,
                "phase4": self.phase4_results
            }
            self.consolidated_report = await self.run_phase5(all_results)  # Run Phase 5
            
            # Complete and remove the task
            progress.update(task5, completed=1)
            progress.stop_task(task5)
            progress.remove_task(task5)
            console.print("[cyan]✓[/cyan] Phase 5 complete: Results consolidated")

            # --- Final Analysis ---
            console.print("\n[bold white]Final Analysis[/bold white]")
            console.print("[dim]Creating final analysis for Cursor IDE...[/dim]")
            
            task6 = progress.add_task("[white]Creating rules...", total=1)
            self.final_analysis = await self.run_final_analysis(self.consolidated_report, tree_for_analysis)  # Run the final analysis with project structure
            
            # Complete and remove the task
            progress.update(task6, completed=1)
            progress.stop_task(task6)
            progress.remove_task(task6)
            console.print("[white]✓[/white] Final Analysis complete: Cursor rules created")

        return self._format_analysis_report(tree_with_delimiters, time.time() - start_time)
    
    def _format_analysis_report(self, tree_with_delimiters: List[str], execution_time: float) -> str:
        """Format the complete analysis report."""
        analysis = [
            f"Project Analysis Report for: {self.directory}",
            "=" * 50 + "\n",
            "## Project Structure\n"
        ]
        
        analysis.extend(tree_with_delimiters)
        analysis.append("\n")
        
        # Get model configuration names
        model_configs = {phase: get_model_config_name(MODEL_CONFIG[phase]) 
                        for phase in ['phase1', 'phase2', 'phase3', 'phase4', 'phase5', 'final']}
        
        analysis.extend([
            f"Phase 1: Initial Discovery (Config: {model_configs['phase1']})",
            "-" * 30,
            json.dumps(self.phase1_results, indent=2),
            "\n",
            f"Phase 2: Methodical Planning (Config: {model_configs['phase2']})",
            "-" * 30,
            self.phase2_results.get("plan", "Error in planning phase"),
            "\n",
            f"Phase 3: Deep Analysis (Config: {model_configs['phase3']})",
            "-" * 30,
            json.dumps(self.phase3_results, indent=2),
            "\n",
            f"Phase 4: Synthesis (Config: {model_configs['phase4']})",
            "-" * 30,
            self.phase4_results.get("analysis", "Error in synthesis phase"),
            "\n",
            f"Phase 5: Consolidation (Config: {model_configs['phase5']})",
            "-" * 30,
            self.consolidated_report.get("report", "Error in consolidation phase"),
            "\n",
            f"Final Analysis (Config: {model_configs['final']})",
            "-" * 30,
            self.final_analysis.get("analysis", "Error in final analysis phase"),
            "\n",
            "Analysis Metrics",
            "-" * 30,
            f"Time taken: {execution_time:.2f} seconds"
        ])
        
        return "\n".join(analysis)


@click.command()
@click.option('--path', '-p', type=str, help='Path to the project directory')
@click.option('--output', '-o', type=str, help='Output file path (deprecated, no longer used)')
def main(path: str, output: str):
    """Run the complete project analysis workflow.
    
    Args:
        path: Path to the project directory to analyze
        output: Path to the output file (deprecated, no longer used)
    """
    logger = setup_logging()
    load_environment()
    clients = initialize_clients(logger)
    
    try:
        if not path:
            path = click.prompt('Please provide the project directory path', type=str)

        directory = Path(os.path.expanduser(path))
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Invalid directory path: {path}")
            sys.exit(1)

        if output:
            logger.warning("The --output option is deprecated and no longer used.")

        console.print(f"\n[bold]Analyzing project:[/] {directory}")
        analyzer = ProjectAnalyzer(directory)
        start_time = time.time()
        analysis_result = asyncio.run(analyzer.analyze())

        analysis_data = {
            "phase1": analyzer.phase1_results,
            "phase2": analyzer.phase2_results,
            "phase3": analyzer.phase3_results,
            "phase4": analyzer.phase4_results,
            "consolidated_report": analyzer.consolidated_report,
            "final_analysis": analyzer.final_analysis,
            "metrics": {
                "time": time.time() - start_time
            }
        }

        _save_outputs_and_files(directory, analysis_data)
        _display_completion_messages(directory)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

def _save_outputs_and_files(directory: Path, analysis_data: Dict):
    """Save phase outputs and create necessary files."""
    save_phase_outputs(directory, analysis_data)
    
    success, message = create_cursorignore(str(directory))
    if success:
        console.print(f"[green]{message}[/]")
    else:
        console.print(f"[yellow]{message}[/]")

    success, message = clean_cursorrules(str(directory))
    if success:
        console.print(f"[green]Cleaned cursor rules file: removed text before 'You are...'[/]")
    else:
        if "not found" in message:
            console.print(f"[yellow]No cursor rules file found to clean[/]")
        elif "Pattern 'You are' not found" in message:
            console.print(f"[yellow]Pattern 'You are' not found in cursor rules file[/]")
        else:
            console.print(f"[yellow]{message}[/]")


def _display_completion_messages(directory: Path):
    """Display completion messages to the user."""
    console.print(f"[green]Individual phase outputs saved to:[/] {directory}/phases_output/")
    console.print(f"[green]Cursor rules created at:[/] {directory}/.cursorrules")
    console.print(f"[green]Cursor ignore created at:[/] {directory}/.cursorignore")
    console.print(f"[green]Execution metrics saved to:[/] {directory}/phases_output/metrics.md")


if __name__ == '__main__':
    main()