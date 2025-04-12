#!/usr/bin/env python3

# ====================================================
# Section 1: Setup and Initialization
# This section imports necessary libraries, sets up logging,
# and initializes API clients. It's the foundation for the rest of the script.
# ====================================================

import click  # For creating command-line interfaces
from pathlib import Path  # For working with file paths in a more object-oriented way
import os  # For interacting with the operating system (e.g., file paths)
import sys  # For accessing system-specific parameters and functions (e.g., exiting the script)
import json  # For working with JSON data
from typing import Dict, List, Optional  # For type hinting (helps with code readability and error checking)
import logging  # For logging messages
from rich.console import Console  # For rich text output in the console
from rich.logging import RichHandler  # For enhanced logging with rich formatting
from rich.progress import Progress, SpinnerColumn, TextColumn  # For displaying progress bars
import time  # For measuring time taken for analysis
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file if it exists
if os.path.exists('.env'):
    load_dotenv()
    logging.info("Loaded environment variables from .env file")
else:
    logging.warning("No .env file found. Make sure API keys are set in environment variables.")

from openai import OpenAI  # For interacting with the OpenAI API
from anthropic import Anthropic  # For interacting with the Anthropic API
import asyncio  # For asynchronous programming (running multiple tasks concurrently)
from config.exclusions import EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS  # Import exclusion lists from config
from core.utils.file_creation.phases_output import save_phase_outputs  # Import the save_phase_outputs function
from core.utils.file_creation.cursorignore import create_cursorignore  # Import the create_cursorignore function
from core.utils.tools.clean_cursorrules import clean_cursorrules  # Import the clean_cursorrules function
from core.utils.tools.tree_generator import get_project_tree  # Import the tree generator function
from core.agents.openai import OpenAIAgent  # Import the OpenAIAgent class
# Import all phase analysis classes from the core.analysis package
from core.analysis import (
    Phase1Analysis,
    Phase2Analysis,
    Phase3Analysis,
    Phase4Analysis,
    Phase5Analysis,
    FinalAnalysis
)
# Import the helper to get model configuration names
from core.utils.tools.model_config_helper import get_model_config_name

# Setup logging.  This configures how log messages are displayed.
console = Console()

# Filter HTTP request logs
class HTTPRequestFilter(logging.Filter):
    def filter(self, record):
        # Filter out detailed HTTP request logs from OpenAI, Anthropic, etc.
        if "HTTP Request:" in record.getMessage():
            # Extract and modify the message to show only important parts
            msg = record.getMessage()
            if "api.openai.com" in msg:
                record.msg = "Using OpenAI model"
                return True
            elif "api.anthropic.com" in msg:
                record.msg = "Using Anthropic model"
                return True
            elif "generativelanguage.googleapis.com" in msg:
                record.msg = "Using Google Gemini model"
                return True
            elif "api.deepseek.com" in msg:
                record.msg = "Using DeepSeek model"
                return True
            return False
        return True

# Setup root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False, markup=True)]
)

# Get the logger and add our filter
logger = logging.getLogger("project_extractor")
http_filter = HTTPRequestFilter()
logger.addFilter(http_filter)

# Also filter the OpenAI and httpx loggers
for logger_name in ["openai", "httpx", "httpcore", "anthropic", "google", "genai"]:
    mod_logger = logging.getLogger(logger_name)
    mod_logger.setLevel(logging.WARNING)  # Only show warnings and errors

# Initialize clients only for the providers that are actually used
from config.agents import MODEL_CONFIG, ModelProvider

# Check which providers are used in the configuration
used_providers = {config.provider for config in MODEL_CONFIG.values()}

# Only initialize clients for providers that are actually used
if ModelProvider.OPENAI in used_providers:
    openai_client = OpenAI()
    logger.info("Initialized OpenAI client")
else:
    openai_client = None
    logger.info("OpenAI client not initialized (not used in any phase)")

if ModelProvider.ANTHROPIC in used_providers:
    anthropic_client = Anthropic()
    logger.info("Initialized Anthropic client")
else:
    anthropic_client = None
    logger.info("Anthropic client not initialized (not used in any phase)")

# ====================================================
# Section 2: Project Analyzer Class
# This class orchestrates the entire analysis process.
# It defines methods for each phase of the analysis
# and a main `analyze` method to run them sequentially.
# ====================================================

class ProjectAnalyzer:
    def __init__(self, directory: Path):
        """
        Initialize the ProjectAnalyzer with the specified directory.
        
        Args:
            directory: Path to the project directory to analyze
        """
        self.directory = directory
        
        # Initialize result storage
        self.phase1_results = {}
        self.phase2_results = {}
        self.phase3_results = {}
        self.phase4_results = {}
        self.consolidated_report = {}
        self.final_analysis = {}
        
        # Initialize all phase analyzers with dynamic model configurations
        self.phase1_analyzer = Phase1Analysis()
        self.phase2_analyzer = Phase2Analysis()
        self.phase3_analyzer = Phase3Analysis()
        self.phase4_analyzer = Phase4Analysis()
        self.phase5_analyzer = Phase5Analysis()
        self.final_analyzer = FinalAnalysis()

    async def run_phase1(self, tree: List[str], package_info: Dict) -> Dict:
        """Initial Discovery Phase using configured model"""
        # Use the Phase1Analysis class to run the analysis
        return await self.phase1_analyzer.run(tree, package_info)

    async def run_phase2(self, phase1_results: Dict, tree: List[str]) -> Dict:
        """Methodical Planning Phase using configured model"""
        # Use the Phase2Analysis class to run the analysis
        return await self.phase2_analyzer.run(phase1_results, tree)

    async def run_phase3(self, analysis_plan: Dict, tree: List[str]) -> Dict:
        """Deep Analysis Phase using configured model"""
        # Use the Phase3Analysis class to run the analysis
        return await self.phase3_analyzer.run(analysis_plan, tree, self.directory)

    async def run_phase4(self, phase3_results: Dict) -> Dict:
        """Synthesis Phase using configured model"""
        # Use the Phase4Analysis class to run the analysis
        return await self.phase4_analyzer.run(phase3_results)

    async def run_phase5(self, all_results: Dict) -> Dict:
        """Consolidation Phase using configured model"""
        # Use the Phase5Analysis class to run the analysis
        return await self.phase5_analyzer.run(all_results)

    async def run_final_analysis(self, consolidated_report: Dict, tree: List[str] = None) -> Dict:
        """Final Analysis Phase using configured model"""
        # Use the FinalAnalysis class to run the analysis
        return await self.final_analyzer.run(consolidated_report, tree)

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

        # Get model information from the configuration
        from config.agents import MODEL_CONFIG
        
        # Format the final output
        analysis = [
            f"Project Analysis Report for: {self.directory}",
            "=" * 50 + "\n",
            "## Project Structure\n"
        ]
        
        # Add the tree with delimiters
        analysis.extend(tree_with_delimiters)
        analysis.append("\n")

        # Get model configuration names
        phase1_model = get_model_config_name(MODEL_CONFIG['phase1'])
        phase2_model = get_model_config_name(MODEL_CONFIG['phase2'])
        phase3_model = get_model_config_name(MODEL_CONFIG['phase3'])
        phase4_model = get_model_config_name(MODEL_CONFIG['phase4'])
        phase5_model = get_model_config_name(MODEL_CONFIG['phase5'])
        final_model = get_model_config_name(MODEL_CONFIG['final'])

        analysis.extend([
            f"Phase 1: Initial Discovery (Config: {phase1_model})",
            "-" * 30,
            json.dumps(self.phase1_results, indent=2),  # Include Phase 1 results (formatted as JSON)
            "\n",
            f"Phase 2: Methodical Planning (Config: {phase2_model})",
            "-" * 30,
            self.phase2_results.get("plan", "Error in planning phase"),  # Include Phase 2 plan (or an error message)
            "\n",
            f"Phase 3: Deep Analysis (Config: {phase3_model})",
            "-" * 30,
            json.dumps(self.phase3_results, indent=2),  # Include Phase 3 results
            "\n",
            f"Phase 4: Synthesis (Config: {phase4_model})",
            "-" * 30,
            self.phase4_results.get("analysis", "Error in synthesis phase"),  # Include Phase 4 analysis
            "\n",
            f"Phase 5: Consolidation (Config: {phase5_model})",
            "-" * 30,
            self.consolidated_report.get("report", "Error in consolidation phase"),  # Include Phase 5 report
            "\n",
            f"Final Analysis (Config: {final_model})",
            "-" * 30,
            self.final_analysis.get("analysis", "Error in final analysis phase"),  # Include the final analysis
            "\n",
            "Analysis Metrics",
            "-" * 30,
            f"Time taken: {time.time() - start_time:.2f} seconds"  # Include the total time taken
        ])

        return "\n".join(analysis)  # Join the lines with newline characters

# ====================================================
# Section 3: Main Function and Command-Line Interface
# This section defines the main function, which is the entry point of the
# script. It uses the `click` library to handle command-line arguments
# and options, making the script user-friendly.
# ====================================================

@click.command()  # Decorate the `main` function as a click command
@click.option('--path', '-p', type=str, help='Path to the project directory')  # Define a command-line option for the project path
@click.option('--output', '-o', type=str, help='Output file path (deprecated, no longer used)')  # Mark as deprecated
def main(path: str, output: str):
    """
    Run the complete project analysis workflow.
    
    Args:
        path: Path to the project directory to analyze
        output: Path to the output file (deprecated, no longer used)
    """
    try:
        # If the user doesn't provide a project path, prompt them to enter it.
        if not path:
            path = click.prompt('Please provide the project directory path', type=str)

        # Convert the path to a `Path` object and check if it's a valid directory.
        directory = Path(os.path.expanduser(path))  # Expand user (~)
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Invalid directory path: {path}")
            sys.exit(1)  # Exit the script with an error code

        # Remove output file functionality
        if output:
            logger.warning("The --output option is deprecated and no longer used.")

        console.print(f"\n[bold]Analyzing project:[/] {directory}")  # Print a message indicating which project is being analyzed
        analyzer = ProjectAnalyzer(directory)  # Create a `ProjectAnalyzer` instance
        start_time = time.time()  # Start timing here
        analysis_result = asyncio.run(analyzer.analyze())  # Run the analysis (this is an asynchronous operation)

        # Extract results from the analyzer.  These are stored as attributes
        # of the `ProjectAnalyzer` instance.  If an attribute doesn't exist
        # (e.g., due to an error in a phase), use an empty dictionary as a default.
        phase1_results = analyzer.phase1_results if hasattr(analyzer, 'phase1_results') else {}
        phase2_results = analyzer.phase2_results if hasattr(analyzer, 'phase2_results') else {}
        phase3_results = analyzer.phase3_results if hasattr(analyzer, 'phase3_results') else {}
        phase4_results = analyzer.phase4_results if hasattr(analyzer, 'phase4_results') else {}
        consolidated_report = analyzer.consolidated_report if hasattr(analyzer, 'consolidated_report') else {}
        final_analysis = analyzer.final_analysis if hasattr(analyzer, 'final_analysis') else {}

        # Prepare data for individual phase outputs.  This creates a dictionary
        # containing all the results, which will be passed to the
        # `save_phase_outputs` function.
        analysis_data = {
            "phase1": phase1_results,
            "phase2": phase2_results,
            "phase3": phase3_results,
            "phase4": phase4_results,
            "consolidated_report": consolidated_report,
            "final_analysis": final_analysis,
            "metrics": {  # Include analysis metrics
                "time": time.time() - start_time  # Calculate the total time taken
            }
        }

        # Save individual phase outputs to separate files.
        save_phase_outputs(directory, analysis_data)
        
        # Create .cursorignore file with default patterns
        success, message = create_cursorignore(str(directory))
        if success:
            console.print(f"[green]{message}[/]")
        else:
            console.print(f"[yellow]{message}[/]")

        # Clean cursor rules file by removing text before "You are..." if needed
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

        console.print(f"[green]Individual phase outputs saved to:[/] {directory}/phases_output/")
        console.print(f"[green]Cursor rules created at:[/] {directory}/.cursorrules")  # Inform about .cursorrules file
        console.print(f"[green]Cursor ignore created at:[/] {directory}/.cursorignore")  # Inform about .cursorignore file
        console.print(f"[green]Execution metrics saved to:[/] {directory}/phases_output/metrics.md")  # Inform about metrics file

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)  # Exit the script with an error code if any exception occurs

# ====================================================
# Section 4: Script Execution
# This block ensures that the `main` function is called only when the script
# is run directly (not when it's imported as a module).
# ====================================================
if __name__ == '__main__':
    main()