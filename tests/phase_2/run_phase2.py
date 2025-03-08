#!/usr/bin/env python3
"""
tests/phase_2/run_phase2.py

This script runs Phase 2 (Methodical Planning) of the project analysis
and saves its output to the tests/phase_2/output directory. This helps
visualize what's being passed to Phase 3 and verify that the parser can
handle the structure with separate <reasoning> and <analysis_plan> tags.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Add the project root to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.analysis.phase_2 import Phase2Analysis
from core.utils.tools.agent_parser import parse_agents_from_phase2

# Sample Phase 1 results to pass to Phase 2
SAMPLE_PHASE1_RESULTS = {
    "phase": "Initial Discovery",
    "findings": [
        {
            "agent": "Structure Agent",
            "findings": "# Structure Analysis Report\n\nThis is a well-structured project with clear separation of concerns."
        },
        {
            "agent": "Dependency Agent",
            "findings": "# Dependency Analysis Report\n\nThe project uses Anthropic and OpenAI SDKs for AI capabilities."
        },
        {
            "agent": "Tech Stack Agent",
            "findings": "# Tech Stack Analysis Report\n\nPrimary tech: Python, Anthropic API, OpenAI API."
        }
    ]
}

# Sample directory tree to pass to Phase 2
SAMPLE_TREE = [
    "cursorrules-architect",
    "├── config",
    "│   ├── prompts",
    "│   │   ├── __init__.py",
    "│   │   ├── final_analysis_prompt.py",
    "│   │   ├── phase_1_prompts.py",
    "│   │   ├── phase_2_prompts.py",
    "│   │   ├── phase_4_prompts.py",
    "│   │   └── phase_5_prompts.py",
    "│   ├── __init__.py",
    "│   └── exclusions.py",
    "├── core",
    "│   ├── agents",
    "│   │   ├── __init__.py",
    "│   │   ├── anthropic.py",
    "│   │   └── openai.py",
    "│   ├── analysis",
    "│   │   ├── __init__.py",
    "│   │   ├── final_analysis.py",
    "│   │   ├── phase_1.py",
    "│   │   ├── phase_2.py",
    "│   │   ├── phase_3.py",
    "│   │   ├── phase_4.py",
    "│   │   └── phase_5.py",
    "│   └── __init__.py",
    "├── utils",
    "│   ├── file_creation",
    "│   │   ├── cursorignore.py",
    "│   │   ├── cursorrules.py",
    "│   │   └── phases_output.py",
    "│   └── tools",
    "│       ├── agent_parser.py",
    "│       ├── file_retriever.py",
    "│       └── tree_generator.py",
    "├── CONTRIBUTING.md",
    "├── main.py",
    "└── requirements.txt"
]


async def run_phase2():
    """Run Phase 2 analysis and save its output."""
    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Get timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Initialize Phase 2 analyzer
        analyzer = Phase2Analysis(model="o1")
        
        # Run Phase 2 analysis
        print("Running Phase 2 analysis...")
        results = await analyzer.run(SAMPLE_PHASE1_RESULTS, SAMPLE_TREE)
        
        # Save raw output
        raw_output_path = output_dir / f"phase2_raw_output_{timestamp}.txt"
        with open(raw_output_path, "w", encoding="utf-8") as f:
            f.write(results.get("plan", "Error: No plan generated"))
        
        print(f"Raw Phase 2 output saved to: {raw_output_path}")
        
        # Save structured output (for debugging)
        json_output_path = output_dir / f"phase2_structured_{timestamp}.json"
        with open(json_output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
            
        print(f"Structured Phase 2 output saved to: {json_output_path}")
        
        # Parse agents and save the parsed results
        plan = results.get("plan", "")
        if plan:
            agents = parse_agents_from_phase2(plan)
            
            # Save parsed agents
            parsed_output_path = output_dir / f"phase2_parsed_{timestamp}.json"
            with open(parsed_output_path, "w", encoding="utf-8") as f:
                json.dump(agents, f, indent=2)
                
            print(f"Parsed agents saved to: {parsed_output_path}")
            print(f"Found {len(agents)} agents:")
            for i, agent in enumerate(agents, 1):
                print(f"  {i}. {agent['name']} - {len(agent['file_assignments'])} files")
        else:
            print("No plan was generated, cannot parse agents")
    
    except Exception as e:
        print(f"Error running Phase 2: {e}")
        # Save error to file
        error_path = output_dir / f"phase2_error_{timestamp}.txt"
        with open(error_path, "w", encoding="utf-8") as f:
            f.write(f"Error running Phase 2: {e}")
        print(f"Error details saved to: {error_path}")


def run_with_existing_test_doc():
    """Parse the existing test document and save the parsed results."""
    # Get the path to the test document
    test_doc_path = Path(__file__).parent / "test_doc.md"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Load the test document
        with open(test_doc_path, "r", encoding="utf-8") as f:
            test_content = f.read()
        
        # Parse agents from the test document
        agents = parse_agents_from_phase2(test_content)
        
        # Save parsed agents
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        parsed_output_path = output_dir / f"test_doc_parsed_{timestamp}.json"
        with open(parsed_output_path, "w", encoding="utf-8") as f:
            json.dump(agents, f, indent=2)
            
        print(f"Parsed test document saved to: {parsed_output_path}")
        print(f"Found {len(agents)} agents in test document:")
        for i, agent in enumerate(agents, 1):
            print(f"  {i}. {agent['name']} - {len(agent['file_assignments'])} files")
    
    except Exception as e:
        print(f"Error parsing test document: {e}")


if __name__ == "__main__":
    # Process command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--test-doc":
        # Parse the existing test document
        run_with_existing_test_doc()
    else:
        # Run Phase 2 analysis
        asyncio.run(run_phase2())