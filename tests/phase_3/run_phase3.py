#!/usr/bin/env python3
"""
tests/phase_3/run_phase3.py

This script runs Phase 3 (Deep Analysis) of the project analysis
using the output from Phase 2 as input. It demonstrates how the
dynamically created agents from Phase 2 are used to analyze the
codebase in Phase 3.
"""

import os
import sys
import json
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

# Add the project root to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.analysis.phase_3 import Phase3Analysis
from utils.tools.tree_generator import get_project_tree

# Directory paths
INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class MockClaudeAgent:
    """Mock agent for testing without making API calls."""
    
    def __init__(self, name, role, responsibilities, prompt_template=None):
        self.name = name
        self.role = role
        self.responsibilities = responsibilities
        self.prompt_template = prompt_template
    
    async def analyze(self, context):
        """Mock analyze method that returns sample findings."""
        # Check if there's a pre-formatted prompt
        if "formatted_prompt" in context:
            # We would use this in a real agent, but here we'll just acknowledge it
            prompt_preview = context["formatted_prompt"][:50] + "..."
        else:
            prompt_preview = "No formatted prompt provided"
            
        # Extract agent's file assignments for a more realistic mock response
        files = context.get("assigned_files", [])
        file_list = "\n".join([f"- {f}" for f in files[:5]])  # Show only first 5 files
        
        return {
            "agent": self.name,
            "findings": f"""# {self.name} Analysis Report

## Overview
This is a mock analysis of {len(files)} files assigned to this agent.

## Files Analyzed
{file_list}
{"..." if len(files) > 5 else ""}

## Key Findings
- This is a mock finding for testing
- The agent would normally analyze code patterns and structure
- In a real run, this would contain detailed analysis

## Recommendations
- This is a mock recommendation for testing
"""
        }


async def run_phase3(use_mock=False):
    """Run Phase 3 analysis using the output from Phase 2 as input."""
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Get timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Load the parsed agents from Phase 2
        phase2_output_path = INPUT_DIR / "phase2_parsed_20250307_143503.json"
        with open(phase2_output_path, "r", encoding="utf-8") as f:
            phase2_agents = json.load(f)
        
        print(f"Loaded {len(phase2_agents)} agents from Phase 2 output")
        
        # Create analysis plan dictionary with agents
        analysis_plan = {
            "agents": phase2_agents
        }
        
        # Generate project tree for context
        tree = get_project_tree(PROJECT_ROOT)
        
        # Initialize Phase 3 analyzer
        analyzer = Phase3Analysis()
        
        # If in mock mode, replace the agent creation method
        if use_mock:
            print("MOCK MODE: Using mock agents instead of actual Claude API calls")
            original_create_method = analyzer._create_agents_from_phase2
            
            # Override the agent creation method to use mock agents
            def mock_create_agents(agent_definitions):
                agents = []
                for agent_def in agent_definitions:
                    name = agent_def.get("name", f"Agent {agent_def.get('id', 'Unknown')}")
                    description = agent_def.get("description", "analyzing the assigned codebase files")
                    agents.append(MockClaudeAgent(
                        name=name,
                        role=description,
                        responsibilities=agent_def.get("responsibilities", [])
                    ))
                return agents
            
            # Replace the method
            analyzer._create_agents_from_phase2 = mock_create_agents
        
        # Run Phase 3 analysis
        print("Running Phase 3 analysis with the following agents:")
        for i, agent in enumerate(phase2_agents, 1):
            print(f"  {i}. {agent['name']} - {len(agent['file_assignments'])} files")
        
        results = await analyzer.run(analysis_plan, tree, PROJECT_ROOT)
        
        # Save the results to file
        output_path = OUTPUT_DIR / f"phase3_output_{timestamp}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        print(f"Phase 3 output saved to: {output_path}")
        
        # Print a summary of the results
        if "findings" in results:
            print(f"\nPhase 3 Analysis Summary:")
            print(f"Found {len(results['findings'])} agent results:")
            for i, finding in enumerate(results['findings'], 1):
                agent_name = finding.get('agent', f"Agent {i}")
                
                # Check if there was an error
                if "error" in finding:
                    print(f"  {i}. {agent_name}: ERROR - {finding['error']}")
                else:
                    findings_excerpt = str(finding.get('findings', ""))[:150]
                    findings_excerpt = findings_excerpt.replace("\n", " ") + "..." if findings_excerpt else "No findings"
                    print(f"  {i}. {agent_name}: {findings_excerpt}")
        
    except Exception as e:
        print(f"Error running Phase 3: {e}")
        import traceback
        traceback.print_exc()
        
        # Save error to file
        error_path = OUTPUT_DIR / f"phase3_error_{timestamp}.txt"
        with open(error_path, "w", encoding="utf-8") as f:
            f.write(f"Error running Phase 3: {e}\n\n")
            f.write(traceback.format_exc())
        print(f"Error details saved to: {error_path}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Phase 3 analysis test")
    parser.add_argument("--mock", action="store_true", help="Use mock agents instead of real API calls")
    args = parser.parse_args()
    
    # Make sure input directory exists
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Created input directory: {INPUT_DIR}")
        print("Please place phase2_parsed_20250307_143503.json in this directory")
        sys.exit(1)
    
    # Make sure the Phase 2 output file exists
    phase2_file = INPUT_DIR / "phase2_parsed_20250307_143503.json"
    if not phase2_file.exists():
        print(f"Error: Could not find Phase 2 output at {phase2_file}")
        print("Please ensure the file exists at this location")
        sys.exit(1)
    
    # Run Phase 3 analysis
    asyncio.run(run_phase3(use_mock=args.mock))
