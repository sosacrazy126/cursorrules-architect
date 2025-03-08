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
from openai import OpenAI  # For interacting with the OpenAI API
from anthropic import Anthropic  # For interacting with the Anthropic API
import asyncio  # For asynchronous programming (running multiple tasks concurrently)
from config.exclusions import EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS  # Import exclusion lists from config
from core.utils.file_creation.phases_output import save_phase_outputs  # Import the save_phase_outputs function
from core.utils.file_creation.cursorignore import create_cursorignore  # Import the create_cursorignore function
from core.utils.tools.tree_generator import get_project_tree  # Import the tree generator function
from core.agents.anthropic import ClaudeAgent  # Import the ClaudeAgent class
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

# Initialize clients for OpenAI and Anthropic APIs.  These are used to access
# external AI models.
openai_client = OpenAI()
anthropic_client = Anthropic()

# Setup logging.  This configures how log messages are displayed.
console = Console()
logging.basicConfig(
    level=logging.INFO,  # Set the minimum log level to INFO (show informational messages and above)
    format="%(message)s",  # Set the format of log messages to just show the message itself
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)]  # Use RichHandler for colorful and informative logs
)
logger = logging.getLogger("project_extractor")  # Create a logger instance named "project_extractor"


# ====================================================
# Section 2: Project Analyzer Class
# This class orchestrates the entire analysis process.
# It defines methods for each phase of the analysis
# and a main `analyze` method to run them sequentially.
# ====================================================

class ProjectAnalyzer:
    def __init__(self, directory: Path, use_new_architecture: bool = False):
        """
        Initialize the ProjectAnalyzer with the specified directory.
        
        Args:
            directory: Path to the project directory to analyze
            use_new_architecture: Whether to use the new Architect architecture (default: False)
        """
        self.directory = directory
        self.use_new_architecture = use_new_architecture
        
        # Initialize result storage
        self.phase1_results = {}
        self.phase2_results = {}
        self.phase3_results = {}
        self.phase4_results = {}
        self.consolidated_report = {}
        self.final_analysis = {}
        
        # Initialize all phase analyzers
        self.phase1_analyzer = Phase1Analysis(use_new_architecture=use_new_architecture)
        self.phase2_analyzer = Phase2Analysis(model="o1")
        self.phase3_analyzer = Phase3Analysis()
        self.phase4_analyzer = Phase4Analysis(model="o1")
        self.phase5_analyzer = Phase5Analysis(model="claude-3-7-sonnet-20250219")
        self.final_analyzer = FinalAnalysis(model="o1")

    async def run_phase1(self, tree: List[str], package_info: Dict) -> Dict:
        """Initial Discovery Phase using Claude-3.7-Sonnet agents"""
        # Use the Phase1Analysis class to run the analysis
        return await self.phase1_analyzer.run(tree, package_info)

    async def run_phase2(self, phase1_results: Dict, tree: List[str]) -> Dict:
        """Methodical Planning Phase using o1"""
        # Use the Phase2Analysis class to run the analysis
        return await self.phase2_analyzer.run(phase1_results, tree)

    async def run_phase3(self, analysis_plan: Dict, tree: List[str]) -> Dict:
        """Deep Analysis Phase using Claude-3.7-Sonnet agents"""
        # Use the Phase3Analysis class to run the analysis
        return await self.phase3_analyzer.run(analysis_plan, tree, self.directory)

    async def run_phase4(self, phase3_results: Dict) -> Dict:
        """Synthesis Phase using o1"""
        # Use the Phase4Analysis class to run the analysis
        return await self.phase4_analyzer.run(phase3_results)

    async def run_phase5(self, all_results: Dict) -> Dict:
        """Consolidation Phase using Claude-3-7-sonnet"""
        # Use the Phase5Analysis class to run the analysis
        return await self.phase5_analyzer.run(all_results)

    async def run_final_analysis(self, consolidated_report: Dict, tree: List[str] = None) -> Dict:
        """Final Analysis Phase using o1"""
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
            task1 = progress.add_task("[green]Phase 1: Initial Discovery...", total=None)  # Add a task for Phase 1
            tree_with_delimiters = get_project_tree(self.directory)  # Generate the directory tree using the enhanced tree generator
            
            # Remove delimiters for analysis
            tree_for_analysis = tree_with_delimiters
            if len(tree_with_delimiters) >= 2 and tree_with_delimiters[0] == "<@tree_generator.py project_structure>" and tree_with_delimiters[-1] == "</project_structure>":
                tree_for_analysis = tree_with_delimiters[1:-1]
            
            package_info = {}  # Placeholder for package information (you would parse package.json here)
            self.phase1_results = await self.run_phase1(tree_for_analysis, package_info)  # Run Phase 1
            progress.update(task1, completed=True)  # Mark Phase 1 as complete

            # --- Phase 2: Methodical Planning ---
            task2 = progress.add_task("[blue]Phase 2: Methodical Planning...", total=None)
            self.phase2_results = await self.run_phase2(self.phase1_results, tree_for_analysis)
            progress.update(task2, completed=True)

            # --- Phase 3: Deep Analysis ---
            task3 = progress.add_task("[yellow]Phase 3: Deep Analysis...", total=None)
            self.phase3_results = await self.run_phase3(self.phase2_results, tree_for_analysis)
            progress.update(task3, completed=True)

            # --- Phase 4: Synthesis ---
            task4 = progress.add_task("[magenta]Phase 4: Synthesis...", total=None)
            self.phase4_results = await self.run_phase4(self.phase3_results)
            progress.update(task4, completed=True)

            # --- Phase 5: Consolidation ---
            task5 = progress.add_task("[cyan]Phase 5: Consolidation...", total=None)
            all_results = {  # Combine the results from all previous phases
                "phase1": self.phase1_results,
                "phase2": self.phase2_results,
                "phase3": self.phase3_results,
                "phase4": self.phase4_results
            }
            self.consolidated_report = await self.run_phase5(all_results)  # Run Phase 5
            progress.update(task5, completed=True)

            # --- Final Analysis ---
            task6 = progress.add_task("[white]Final Analysis...", total=None)
            self.final_analysis = await self.run_final_analysis(self.consolidated_report, tree_for_analysis)  # Run the final analysis with project structure
            progress.update(task6, completed=True)

        # Format the final output
        analysis = [
            f"Project Analysis Report for: {self.directory}",
            "=" * 50 + "\n",
            "## Project Structure\n"
        ]
        
        # Add the tree with delimiters
        analysis.extend(tree_with_delimiters)
        analysis.append("\n")

        analysis.extend([
            "Phase 1: Initial Discovery (Claude-3.7-Sonnet)",
            "-" * 30,
            json.dumps(self.phase1_results, indent=2),  # Include Phase 1 results (formatted as JSON)
            "\n",
            "Phase 2: Methodical Planning (o1)",
            "-" * 30,
            self.phase2_results.get("plan", "Error in planning phase"),  # Include Phase 2 plan (or an error message)
            "\n",
            "Phase 3: Deep Analysis (Claude-3.7-Sonnet)",
            "-" * 30,
            json.dumps(self.phase3_results, indent=2),  # Include Phase 3 results
            "\n",
            "Phase 4: Synthesis (o1)",
            "-" * 30,
            self.phase4_results.get("analysis", "Error in synthesis phase"),  # Include Phase 4 analysis
            "\n",
            "Phase 5: Consolidation (Claude-3.7-Sonnet)",
            "-" * 30,
            self.consolidated_report.get("report", "Error in consolidation phase"),  # Include Phase 5 report
            "\n",
            "Final Analysis",
            "-" * 30,
            self.final_analysis.get("analysis", "Error in final analysis phase"),  # Include the final analysis
            "\n",
            "Analysis Metrics",
            "-" * 30,
            f"Time taken: {time.time() - start_time:.2f} seconds",  # Include the total time taken
            f"Phase 2 reasoning tokens: {self.phase2_results.get('reasoning_tokens', 0)}",  # Include token usage
            f"Phase 4 reasoning tokens: {self.phase4_results.get('reasoning_tokens', 0)}",
            f"Final Analysis reasoning tokens: {self.final_analysis.get('reasoning_tokens', 0)}"
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
@click.option('--use-new-architecture', '-n', is_flag=True, help='Use the new Architect architecture')  # Define a flag for using the new architecture
def main(path: str, output: str, use_new_architecture: bool):
    """
    Run the complete project analysis workflow.
    
    Args:
        path: Path to the project directory to analyze
        output: Path to the output file (deprecated, no longer used)
        use_new_architecture: Whether to use the new Architect architecture
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
        analyzer = ProjectAnalyzer(directory, use_new_architecture)  # Create a `ProjectAnalyzer` instance
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
                "time": time.time() - start_time,  # Calculate the total time taken
                "phase2_tokens": phase2_results.get("reasoning_tokens", 0),  # Get token usage for each phase
                "phase4_tokens": phase4_results.get("reasoning_tokens", 0),
                "final_tokens": final_analysis.get("reasoning_tokens", 0)
            }
        }

        # Save individual phase outputs to separate files.
        save_phase_outputs(directory, analysis_data)
        
        # Create .cursorignore file with default patterns
        success, message = create_cursorignore()
        if success:
            console.print(f"[green]{message}[/]")
        else:
            console.print(f"[yellow]{message}[/]")

        console.print(f"[green]Individual phase outputs saved to:[/] {directory}/phases_output/")
        console.print(f"[green]Cursor rules created at:[/] {directory}/.cursorrules")  # Inform about .cursorrules file
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