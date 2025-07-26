#!/usr/bin/env python3
"""
demo_blueprint.py

Demonstration script showing the Blueprint Generator in action for Plan Mode workflow.
"""

import asyncio
import json
from pathlib import Path
from .core.blueprint import BlueprintGenerator, BlueprintIntegration

def main():
    """Demonstrate blueprint generation and integration."""
    print("🔧 Blueprint Generator Demonstration")
    print("=" * 50)
    
    # Initialize the blueprint generator
    generator = BlueprintGenerator("phases_output")
    
    # Sample project context
    project_context = {
        "project_info": {
            "name": "cursorrules-architect",
            "type": "python_project",
            "framework": "asyncio"
        },
        "environment": {
            "python_version": "3.8+",
            "requirements": ["anthropic", "openai", "rich", "pydantic"]
        },
        "dependencies": {
            "runtime": ["asyncio", "json", "pathlib"],
            "dev": ["pytest", "black", "mypy"]
        },
        "existing_analysis": {}
    }
    
    # Generate blueprints for all phases
    phases = ["phase1", "phase2", "phase3", "phase4", "phase5"]
    
    for phase in phases:
        print(f"\n📋 Generating blueprint for {phase.upper()}")
        
        blueprint = generator.generate_blueprint(
            phase,
            project_context,
            custom_requirements={
                "priority_focus": "accuracy" if phase in ["phase1", "phase3"] else "efficiency"
            }
        )
        
        print(f"✅ Blueprint saved with {len(blueprint['tasks'])} tasks and {len(blueprint['agents'])} agents")
        
        # Show a sample of the blueprint content
        print(f"   Tasks: {', '.join([t['name'] for t in blueprint['tasks']])}")
        if blueprint['agents']:
            print(f"   Agents: {', '.join([a['name'] for a in blueprint['agents']])}")
    
    # Demonstrate prompt injection
    print(f"\n🔄 Demonstrating prompt injection for Phase 1")
    
    base_prompt = """You are an AI architect analyzing a project.
    
Analyze this project context and provide insights:
{context}

Please provide your analysis in a structured format."""
    
    phase1_blueprint = generator.generate_blueprint("phase1", project_context)
    enhanced_prompt = generator.inject_into_prompt(base_prompt, phase1_blueprint)
    
    print(f"Enhanced prompt length: {len(enhanced_prompt)} characters")
    print(f"Blueprint context added: {'BLUEPRINT CONTEXT' in enhanced_prompt}")
    
    # Save enhanced prompt for inspection
    with open("phases_output/enhanced_prompt_example.md", "w") as f:
        f.write("# Enhanced Prompt Example\n\n")
        f.write("This shows how the blueprint is injected into agent prompts.\n\n")
        f.write("```\n")
        f.write(enhanced_prompt)
        f.write("\n```")
    
    print(f"✅ Enhanced prompt saved to phases_output/enhanced_prompt_example.md")
    
    # Show file structure created
    print(f"\n📁 Generated files:")
    output_dir = Path("phases_output")
    for file in sorted(output_dir.glob("*.md")):
        print(f"   - {file.name}")
    for file in sorted(output_dir.glob("*.json")):
        print(f"   - {file.name}")
    for file in sorted(output_dir.glob("*.yaml")):
        print(f"   - {file.name}")
    
    print(f"\n✨ Blueprint generation complete! Check the phases_output/ directory for all generated files.")

if __name__ == "__main__":
    main()
