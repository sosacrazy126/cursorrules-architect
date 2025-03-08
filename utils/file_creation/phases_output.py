"""
utils/file_creation/phases_output.py

This module provides functionality for saving the outputs of analysis phases
to separate files. It handles the creation of output directories and formatting
of the output files.

This module is used by the main analysis process to save results in a structured way.
"""

# ====================================================
# Importing Necessary Libraries
# This section imports external libraries that are used in the code.
# These libraries add extra functionalities that Python doesn't have by default.
# ====================================================

import json  # Used for working with JSON data
from pathlib import Path  # Used for interacting with file paths in a more object-oriented way
from typing import Dict, Any  # Used for type hinting, which makes the code easier to understand


# ====================================================
# Function to Save Phase Outputs
# This is the main function that takes the analysis results and saves them into separate files.
# ====================================================

def save_phase_outputs(directory: Path, analysis_data: dict) -> None:
    """Save each phase's output to separate markdown files.
    
    Args:
        directory: The project directory path
        analysis_data: Dictionary containing the results of all analysis phases
    """
    # ====================================================
    # Create Output Directory
    # This part creates a new folder named "phases_output" inside the project directory.
    # This folder will store all the generated output files.
    # ====================================================
    output_dir = directory / "phases_output"
    output_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    # ====================================================
    # Helper Function: Ensure String
    # This function converts any data (like dictionaries or lists) into a string format.
    # This is important because we can only write strings to files.
    # ====================================================
    def ensure_string(value: Any) -> str:
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value, indent=2)  # Convert dictionaries/lists to nicely formatted JSON strings
        return str(value)

    # ====================================================
    # Save Results to Individual Markdown Files
    # This section writes the results of each analysis phase to a separate file.
    # Each file is named based on the phase it represents (e.g., phase1_discovery.md).
    # ====================================================

    # Phase 1: Initial Discovery
    with open(output_dir / "phase1_discovery.md", "w", encoding="utf-8") as f:
        f.write("# Phase 1: Initial Discovery (Claude-3.7-Sonnet)\n\n")
        f.write("## Agent Findings\n\n")
        f.write("```json\n")
        f.write(json.dumps(analysis_data["phase1"], indent=2))  # Write the Phase 1 results as JSON
        f.write("\n```\n")

    # Phase 2: Methodical Planning
    with open(output_dir / "phase2_planning.md", "w", encoding="utf-8") as f:
        f.write("# Phase 2: Methodical Planning (o1)\n\n")
        plan_data = analysis_data["phase2"].get("plan", "Error in planning phase")
        f.write(ensure_string(plan_data))  # Ensure we're writing a string

    # Phase 3: Deep Analysis
    with open(output_dir / "phase3_analysis.md", "w", encoding="utf-8") as f:
        f.write("# Phase 3: Deep Analysis (Claude-3.7-Sonnet)\n\n")
        f.write("```json\n")
        f.write(json.dumps(analysis_data["phase3"], indent=2))  # Write the Phase 3 results as JSON
        f.write("\n```\n")

    # Phase 4: Synthesis
    with open(output_dir / "phase4_synthesis.md", "w", encoding="utf-8") as f:
        f.write("# Phase 4: Synthesis (o1)\n\n")
        analysis_data_phase4 = analysis_data["phase4"].get("analysis", "Error in synthesis phase")
        f.write(ensure_string(analysis_data_phase4))  # Ensure we're writing a string

    # Phase 5: Consolidation
    with open(output_dir / "phase5_consolidation.md", "w", encoding="utf-8") as f:
        f.write("# Phase 5: Consolidation (Claude-3.7-Sonnet)\n\n")
        report_data = analysis_data["consolidated_report"].get("report", "Error in consolidation phase")
        f.write(ensure_string(report_data))  # Ensure we're writing a string

    # Final Analysis - Save to both markdown file and .cursorrules file
    final_analysis_data = analysis_data["final_analysis"].get("analysis", "Error in final analysis phase")
    
    # Save to markdown file in phases_output directory
    with open(output_dir / "final_analysis.md", "w", encoding="utf-8") as f:
        f.write("# Final Analysis\n\n")
        f.write(ensure_string(final_analysis_data))  # Ensure we're writing a string
    
    # Save to .cursorrules file in project root directory with project tree
    # Define directories to exclude from the tree
    exclude_dirs = ["phases_output", "__pycache__", ".git", ".vscode", ".cursor"]
    
    # Get the project tree without the excluded directories
    from utils.tools.tree_generator import generate_tree, DEFAULT_EXCLUDE_DIRS, DEFAULT_EXCLUDE_PATTERNS
    
    # Create a custom set of exclude directories by combining defaults with our additions
    custom_exclude_dirs = DEFAULT_EXCLUDE_DIRS.union(set(exclude_dirs))
    
    # Generate a tree with our custom exclusions
    tree = generate_tree(
        directory,
        exclude_dirs=custom_exclude_dirs,
        exclude_patterns=DEFAULT_EXCLUDE_PATTERNS
    )
    
    # Add delimiters and format for inclusion in the .cursorrules file
    tree_section = [
        "\n<project_structure>",
    ]
    tree_section.extend(tree)
    tree_section.append("</project_structure>")
    
    # Write final analysis and tree to .cursorrules file
    with open(directory / ".cursorrules", "w", encoding="utf-8") as f:
        f.write(ensure_string(final_analysis_data))  # Save the final analysis
        f.write("\n\n")  # Add spacing
        f.write("# Project Directory Structure\n")  # Section header
        f.write("---\n\n")  # Section divider
        f.write('\n'.join(tree_section))  # Append the tree structure

    # ====================================================
    # Create metrics file
    # This section creates a metrics file that summarizes key information
    # from the entire analysis, including metrics like total time and token usage.
    # ====================================================
    with open(output_dir / "metrics.md", "w", encoding="utf-8") as f:
        f.write("# CursorRules Architect Metrics\n\n")
        f.write(f"Project: {directory}\n")
        f.write("=" * 50 + "\n\n")
        f.write("## Analysis Metrics\n\n")
        f.write(f"- Time taken: {analysis_data['metrics']['time']:.2f} seconds\n")  # Write the total time
        f.write(f"- Phase 2 reasoning tokens: {analysis_data['metrics']['phase2_tokens']}\n")  # Write token usage
        f.write(f"- Phase 4 reasoning tokens: {analysis_data['metrics']['phase4_tokens']}\n")
        f.write(f"- Final Analysis reasoning tokens: {analysis_data['metrics']['final_tokens']}\n\n")
        f.write("## Generated Files\n\n")
        f.write("- `.cursorrules` - Contains the final analysis for Cursor IDE\n")
        f.write("- `.cursorignore` - Contains patterns of files to ignore in Cursor IDE\n")
        f.write("- `phase1_discovery.md` - Results from Initial Discovery (Claude)\n")
        f.write("- `phase2_planning.md` - Results from Methodical Planning (O1)\n")
        f.write("- `phase3_analysis.md` - Results from Deep Analysis (Claude)\n")
        f.write("- `phase4_synthesis.md` - Results from Synthesis (O1)\n")
        f.write("- `phase5_consolidation.md` - Results from Consolidation (Claude)\n")
        f.write("- `final_analysis.md` - Copy of the final analysis\n\n")
        f.write("See individual phase files for detailed outputs.")
