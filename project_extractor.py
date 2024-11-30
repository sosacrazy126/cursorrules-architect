#!/usr/bin/env python3

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
from openai import OpenAI
from anthropic import Anthropic
import asyncio

# Initialize clients
openai_client = OpenAI()
anthropic_client = Anthropic()

# Setup logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)]
)
logger = logging.getLogger("project_extractor")

def generate_tree(path: Path, prefix: str = "", max_depth: int = 4, current_depth: int = 0) -> List[str]:
    """Generate a tree structure of the directory up to max_depth"""
    EXCLUDED_DIRS = {
        'node_modules', '.next', '.git', 'venv', '__pycache__', 
        'dist', 'build', '.vscode', '.idea', 'coverage',
        '.pytest_cache', '.mypy_cache', 'env', '.env', '.venv',
        'site-packages'
    }
    
    EXCLUDED_FILES = {
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        '.DS_Store', '.env', '.env.local', '.gitignore',
        'README.md', 'LICENSE', '.eslintrc', '.prettierrc',
        'tsconfig.json', 'requirements.txt', 'poetry.lock',
        'Pipfile.lock'
    }
    
    EXCLUDED_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.ico',
        '.svg', '.mp4', '.mp3', '.pdf', '.zip',
        '.woff', '.woff2', '.ttf', '.eot',
        '.pyc', '.pyo', '.pyd', '.so', '.pkl', '.pickle',
        '.db', '.sqlite', '.log', '.cache'
    }
    
    if current_depth >= max_depth:
        return ["    " + prefix + "..."]
    
    try:
        items = sorted(path.glob('*'))
        filtered_items = []
        
        for item in items:
            if item.is_dir():
                if item.name not in EXCLUDED_DIRS and not item.name.startswith('.'):
                    filtered_items.append(item)
            elif item.is_file():
                if (item.name not in EXCLUDED_FILES and 
                    item.suffix.lower() not in EXCLUDED_EXTENSIONS and
                    not item.name.startswith('.')):
                    filtered_items.append(item)
        
        tree = []
        for i, item in enumerate(filtered_items):
            is_last = i == len(filtered_items) - 1
            current_prefix = "└── " if is_last else "├── "
            item_name = f"{item.name}/" if item.is_dir() else item.name
            tree.append(f"{prefix}{current_prefix}{item_name}")
            
            if item.is_dir():
                extension = "    " if is_last else "│   "
                tree.extend(generate_tree(
                    item,
                    prefix + extension,
                    max_depth,
                    current_depth + 1
                ))
        
        return tree
    except Exception as e:
        logger.error(f"Error processing {path}: {str(e)}")
        return [f"{prefix}└── <e>"]

class ClaudeAgent:
    def __init__(self, name: str, role: str, responsibilities: List[str]):
        self.name = name
        self.role = role
        self.responsibilities = responsibilities
        
    async def analyze(self, context: Dict) -> Dict:
        """Run agent analysis using Claude-3-5-sonnet-20241022"""
        try:
            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": f"""You are the {self.name}, responsible for {self.role}.
                    
                    Your specific responsibilities are:
                    {chr(10).join(f'- {r}' for r in self.responsibilities)}
                    
                    Analyze this project context and provide a detailed report focused on your domain:
                    
                    {json.dumps(context, indent=2)}
                    
                    Format your response as a structured report with clear sections and findings."""
                }]
            )
            
            return {
                "agent": self.name,
                "findings": response.content[0].text
            }
        except Exception as e:
            logger.error(f"Error in {self.name} analysis: {str(e)}")
            return {
                "agent": self.name,
                "error": str(e)
            }

class ProjectAnalyzer:
    def __init__(self, directory: Path):
        self.directory = directory
        
        # Phase 1: Initial Discovery Agents
        self.phase1_agents = [
            ClaudeAgent("Structure Agent", "analyzing directory and file organization", [
                "Analyze directory and file organization",
                "Map project layout and file relationships",
                "Identify key architectural components"
            ]),
            ClaudeAgent("Dependency Agent", "investigating packages and libraries", [
                "Investigate all packages and libraries",
                "Determine version requirements",
                "Research compatibility issues"
            ]),
            ClaudeAgent("Tech Stack Agent", "identifying frameworks and technologies", [
                "Identify all frameworks and technologies",
                "Gather latest documentation for each",
                "Note current best practices and updates"
            ])
        ]
        
        # Phase 3: Deep Analysis Agents
        self.phase3_agents = [
            ClaudeAgent("Code Analysis Agent", "examining core logic and patterns", [
                "Examine core logic and patterns",
                "Review implementation details",
                "Identify optimization opportunities"
            ]),
            ClaudeAgent("Dependency Mapping Agent", "mapping file relationships", [
                "Map all file relationships",
                "Document import/export patterns",
                "Chart data flow paths"
            ]),
            ClaudeAgent("Architecture Agent", "studying design patterns", [
                "Study design patterns",
                "Review architectural decisions",
                "Evaluate system structure"
            ]),
            ClaudeAgent("Documentation Agent", "creating comprehensive documentation", [
                "Create comprehensive docs",
                "Maintain analysis records",
                "Format findings clearly"
            ])
        ]
        
    async def run_phase1(self, tree: List[str], package_info: Dict) -> Dict:
        """Initial Discovery Phase using Claude-3.5-Sonnet agents"""
        context = {
            "tree_structure": tree,
            "package_info": package_info
        }
        
        agent_tasks = [agent.analyze(context) for agent in self.phase1_agents]
        results = await asyncio.gather(*agent_tasks)
        
        return {
            "phase": "Initial Discovery",
            "findings": results
        }
        
    async def run_phase2(self, phase1_results: Dict) -> Dict:
        """Methodical Planning Phase using o1-preview"""
        try:
            response = openai_client.chat.completions.create(
                model="o1-preview",
                messages=[{
                    "role": "user",
                    "content": f"""Process these agent findings and create a detailed, step-by-step analysis plan:

                    Agent Findings:
                    {json.dumps(phase1_results, indent=2)}

                    Create a comprehensive plan including:
                    1. File-by-file examination approach
                    2. Critical areas needing investigation
                    3. Documentation requirements
                    4. Inter-dependency mapping method
                    """
                }],
                max_completion_tokens=25000
            )
            
            reasoning_tokens = 0
            if hasattr(response.usage, 'completion_tokens_details'):
                reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
            
            return {
                "phase": "Methodical Planning",
                "plan": response.choices[0].message.content,
                "reasoning_tokens": reasoning_tokens
            }
        except Exception as e:
            logger.error(f"Error in Phase 2: {str(e)}")
            return {
                "phase": "Methodical Planning",
                "error": str(e)
            }
            
    async def run_phase3(self, analysis_plan: Dict, tree: List[str]) -> Dict:
        """Deep Analysis Phase using Claude-3.5-Sonnet agents"""
        context = {
            "analysis_plan": analysis_plan,
            "tree_structure": tree
        }
        
        agent_tasks = [agent.analyze(context) for agent in self.phase3_agents]
        results = await asyncio.gather(*agent_tasks)
        
        return {
            "phase": "Deep Analysis",
            "findings": results
        }
        
    async def run_phase4(self, phase3_results: Dict) -> Dict:
        """Synthesis Phase using o1-preview"""
        try:
            response = openai_client.chat.completions.create(
                model="o1-preview",
                messages=[{
                    "role": "user",
                    "content": f"""Review and synthesize these agent findings:

                    Analysis Results:
                    {json.dumps(phase3_results, indent=2)}

                    Provide:
                    1. Deep analysis of all findings
                    2. Methodical processing of new information
                    3. Updated analysis directions
                    4. Refined instructions for agents
                    5. Areas needing deeper investigation
                    """
                }],
                max_completion_tokens=25000
            )
            
            reasoning_tokens = 0
            if hasattr(response.usage, 'completion_tokens_details'):
                reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
            
            return {
                "phase": "Synthesis",
                "analysis": response.choices[0].message.content,
                "reasoning_tokens": reasoning_tokens
            }
        except Exception as e:
            logger.error(f"Error in Phase 4: {str(e)}")
            return {
                "phase": "Synthesis",
                "error": str(e)
            }
            
    async def run_phase5(self, all_results: Dict) -> Dict:
        """Consolidation Phase using Claude-3-5-sonnet-20241022"""
        try:
            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": f"""As the Report Agent, create a comprehensive final report from all analysis phases:
                    
                    Analysis Results:
                    {json.dumps(all_results, indent=2)}
                    
                    Your tasks:
                    1. Combine all agent findings
                    2. Organize by component/module
                    3. Create comprehensive documentation
                    4. Highlight key discoveries
                    5. Prepare final report for O1"""
                }]
            )
            
            return {
                "phase": "Consolidation",
                "report": response.content[0].text
            }
        except Exception as e:
            logger.error(f"Error in Phase 5: {str(e)}")
            return {
                "phase": "Consolidation",
                "error": str(e)
            }
            
    async def run_final_analysis(self, consolidated_report: Dict) -> Dict:
        """Final Analysis Phase using o1-preview"""
        try:
            response = openai_client.chat.completions.create(
                model="o1-preview",
                messages=[{
                    "role": "user",
                    "content": f"""Process this consolidated report and provide a final analysis:

                    Consolidated Report:
                    {json.dumps(consolidated_report, indent=2)}

                    Provide:
                    1. Identified architectural patterns
                    2. Complete system structure mapping
                    3. Comprehensive relationship documentation
                    4. Improvement recommendations
                    5. Next analysis phase planning
                    """
                }],
                max_completion_tokens=25000
            )
            
            reasoning_tokens = 0
            if hasattr(response.usage, 'completion_tokens_details'):
                reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
            
            return {
                "phase": "Final Analysis",
                "analysis": response.choices[0].message.content,
                "reasoning_tokens": reasoning_tokens
            }
        except Exception as e:
            logger.error(f"Error in Final Analysis: {str(e)}")
            return {
                "phase": "Final Analysis",
                "error": str(e)
            }
            
    async def analyze(self) -> str:
        """Run complete analysis workflow"""
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Phase 1: Initial Discovery (Claude-3.5-Sonnet)
            task1 = progress.add_task("[green]Phase 1: Initial Discovery...", total=None)
            tree = generate_tree(self.directory)
            package_info = {}  # You can implement package.json parsing here
            phase1_results = await self.run_phase1(tree, package_info)
            progress.update(task1, completed=True)
            
            # Phase 2: Methodical Planning (o1-preview)
            task2 = progress.add_task("[blue]Phase 2: Methodical Planning...", total=None)
            phase2_results = await self.run_phase2(phase1_results)
            progress.update(task2, completed=True)
            
            # Phase 3: Deep Analysis (Claude-3.5-Sonnet)
            task3 = progress.add_task("[yellow]Phase 3: Deep Analysis...", total=None)
            phase3_results = await self.run_phase3(phase2_results, tree)
            progress.update(task3, completed=True)
            
            # Phase 4: Synthesis (o1-preview)
            task4 = progress.add_task("[magenta]Phase 4: Synthesis...", total=None)
            phase4_results = await self.run_phase4(phase3_results)
            progress.update(task4, completed=True)
            
            # Phase 5: Consolidation (Claude-3.5-Sonnet)
            task5 = progress.add_task("[cyan]Phase 5: Consolidation...", total=None)
            all_results = {
                "phase1": phase1_results,
                "phase2": phase2_results,
                "phase3": phase3_results,
                "phase4": phase4_results
            }
            consolidated_report = await self.run_phase5(all_results)
            progress.update(task5, completed=True)
            
            # Final Analysis (o1-preview)
            task6 = progress.add_task("[white]Final Analysis...", total=None)
            final_analysis = await self.run_final_analysis(consolidated_report)
            progress.update(task6, completed=True)
        
        # Format final output
        analysis = [
            f"Project Analysis Report for: {self.directory}",
            "=" * 50 + "\n",
            "Phase 1: Initial Discovery (Claude-3.5-Sonnet)",
            "-" * 30,
            json.dumps(phase1_results, indent=2),
            "\n",
            "Phase 2: Methodical Planning (o1-preview)",
            "-" * 30,
            phase2_results.get("plan", "Error in planning phase"),
            "\n",
            "Phase 3: Deep Analysis (Claude-3.5-Sonnet)",
            "-" * 30,
            json.dumps(phase3_results, indent=2),
            "\n",
            "Phase 4: Synthesis (o1-preview)",
            "-" * 30,
            phase4_results.get("analysis", "Error in synthesis phase"),
            "\n",
            "Phase 5: Consolidation (Claude-3.5-Sonnet)",
            "-" * 30,
            consolidated_report.get("report", "Error in consolidation phase"),
            "\n",
            "Final Analysis (o1-preview)",
            "-" * 30,
            final_analysis.get("analysis", "Error in final analysis phase"),
            "\n",
            "Analysis Metrics",
            "-" * 30,
            f"Time taken: {time.time() - start_time:.2f} seconds",
            f"Phase 2 reasoning tokens: {phase2_results.get('reasoning_tokens', 0)}",
            f"Phase 4 reasoning tokens: {phase4_results.get('reasoning_tokens', 0)}",
            f"Final Analysis reasoning tokens: {final_analysis.get('reasoning_tokens', 0)}"
        ]
        
        return "\n".join(analysis)

@click.command()
@click.option('--path', '-p', type=str, help='Path to the project directory')
@click.option('--output', '-o', type=str, help='Output file path')
def main(path: str, output: str):
    """Run multi-phase project analysis"""
    try:
        if not path:
            path = click.prompt('Please provide the project directory path', type=str)
        
        directory = Path(os.path.expanduser(path))
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Invalid directory path: {path}")
            sys.exit(1)
        
        output_file = output or f"{directory.name}_analysis.txt"
        
        console.print(f"\n[bold]Analyzing project:[/] {directory}")
        analyzer = ProjectAnalyzer(directory)
        analysis = asyncio.run(analyzer.analyze())
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis)
        
        console.print(f"\n[green]Analysis saved to:[/] {output_file}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 