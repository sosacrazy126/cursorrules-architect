#!/usr/bin/env python3
"""
Quick Phase 3 Diagnostic Runner

This script provides a quick way to diagnose Phase 3 issues by analyzing
a real example of problematic agent assignments and file paths.

Usage: python tests/run_phase3_diagnostic.py
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analysis.phase_3 import Phase3Analysis
from config.exclusions import EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def analyze_file_path_issues(file_assignments, base_dir):
    """Analyze file path issues in assignments."""
    issues = []
    
    for file_path in file_assignments:
        path = Path(file_path)
        full_path = base_dir / file_path if not path.is_absolute() else path
        
        issue = {
            "file_path": file_path,
            "exists": full_path.exists(),
            "is_build_artifact": is_build_artifact(path),
            "should_be_excluded": should_exclude_path(path),
            "issue_type": categorize_issue(file_path, full_path.exists())
        }
        issues.append(issue)
    
    return issues

def is_build_artifact(path: Path) -> bool:
    """Check if path is a build artifact."""
    build_indicators = [
        "out/_next", "out/static", "dist/", "build/", 
        ".next/", "node_modules/", "__pycache__/", 
        "venv/", "coverage/"
    ]
    
    path_str = str(path)
    return any(indicator in path_str for indicator in build_indicators)

def should_exclude_path(path: Path) -> bool:
    """Check if path should be excluded based on exclusion rules."""
    # Check directories
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return True
    
    # Check files
    if path.name in EXCLUDED_FILES:
        return True
    
    # Check extensions
    if path.suffix in EXCLUDED_EXTENSIONS:
        return True
    
    return False

def categorize_issue(file_path: str, exists: bool) -> str:
    """Categorize the type of issue."""
    if is_build_artifact(Path(file_path)):
        return "build_artifact"
    elif not exists:
        return "missing_file"
    elif file_path.startswith('/'):
        return "absolute_path"
    else:
        return "none"

async def test_realistic_scenario():
    """Test with a realistic problematic scenario."""
    logger.info("🧪 Testing realistic Phase 3 scenario...")
    
    # Simulate the problematic scenario from the logs
    problematic_plan = {
        "agents": [
            {
                "id": "agent_1",
                "name": "Desktop Application Engineer",
                "description": "Analyzes desktop application frameworks and GUI components",
                "file_assignments": [
                    "pickleglass_web/out/_next",        # Build artifact directory
                    "pickleglass_web/out/static",       # Build artifact directory
                    "src/main.py",                      # Likely valid file
                    "src/components/Button.tsx",        # Likely valid file
                    "package.json",                     # Likely valid file
                    "nonexistent_file.js"               # Non-existent file
                ]
            },
            {
                "id": "agent_2",
                "name": "API Integration Specialist",
                "description": "Analyzes API connections and data flow",
                "file_assignments": [
                    "api/routes/user.js",               # Likely valid file
                    "config/database.json",             # Likely valid file
                    "dist/bundle.js"                    # Build artifact
                ]
            }
        ]
    }
    
    # Use current directory as base
    base_dir = Path.cwd()
    
    print("\n" + "="*60)
    print("🔍 PHASE 3 DIAGNOSTIC ANALYSIS")
    print("="*60)
    
    # Analyze each agent's file assignments
    total_issues = 0
    
    for agent in problematic_plan["agents"]:
        agent_name = agent["name"]
        file_assignments = agent["file_assignments"]
        
        print(f"\n🤖 Agent: {agent_name}")
        print(f"   Files assigned: {len(file_assignments)}")
        
        # Analyze file path issues
        file_issues = analyze_file_path_issues(file_assignments, base_dir)
        
        # Categorize issues
        build_artifacts = [i for i in file_issues if i["issue_type"] == "build_artifact"]
        missing_files = [i for i in file_issues if i["issue_type"] == "missing_file"]
        valid_files = [i for i in file_issues if i["issue_type"] == "none" and i["exists"]]
        
        print(f"   📊 Analysis:")
        print(f"     • Build artifacts: {len(build_artifacts)}")
        print(f"     • Missing files: {len(missing_files)}")
        print(f"     • Valid files: {len(valid_files)}")
        
        if build_artifacts:
            print(f"     🏗️  Build artifacts found:")
            for artifact in build_artifacts:
                print(f"       - {artifact['file_path']}")
        
        if missing_files:
            print(f"     ❌ Missing files:")
            for missing in missing_files:
                print(f"       - {missing['file_path']}")
        
        total_issues += len(build_artifacts) + len(missing_files)
    
    # Test the actual Phase 3 file content retrieval
    print(f"\n🔧 Testing Phase 3 file content retrieval...")
    
    phase3 = Phase3Analysis()
    
    # Test with problematic file assignments
    test_assignments = [
        "pickleglass_web/out/_next",
        "pickleglass_web/out/static",
        "nonexistent_file.js"
    ]
    
    file_contents = await phase3._get_file_contents(base_dir, test_assignments)
    
    print(f"   📄 File retrieval results:")
    print(f"     • Files requested: {len(test_assignments)}")
    print(f"     • Files retrieved: {len(file_contents)}")
    print(f"     • Success rate: {len(file_contents)/len(test_assignments)*100:.1f}%")
    
    for assignment in test_assignments:
        found = assignment in file_contents
        print(f"     • {assignment}: {'✅ Found' if found else '❌ Not found'}")
    
    # Summary
    print(f"\n📋 DIAGNOSTIC SUMMARY:")
    print(f"   • Total agents analyzed: {len(problematic_plan['agents'])}")
    print(f"   • Total file assignments: {sum(len(agent['file_assignments']) for agent in problematic_plan['agents'])}")
    print(f"   • Total issues found: {total_issues}")
    
    # Root cause analysis
    print(f"\n🔍 ROOT CAUSE ANALYSIS:")
    
    if total_issues > 0:
        print("   ❌ Issues detected:")
        print("     1. Build artifacts are being assigned to agents")
        print("        → Phase 2 planning is not filtering build directories")
        print("     2. Non-existent files are being assigned")
        print("        → File validation is needed before assignment")
        print("     3. Directory paths are treated as files")
        print("        → Need to distinguish between files and directories")
        
        print(f"\n💡 RECOMMENDED FIXES:")
        print("   1. Enhance Phase 2 planning to filter build artifacts")
        print("   2. Add file existence validation in Phase 3")
        print("   3. Improve exclusion patterns for build directories")
        print("   4. Add directory vs file detection")
    else:
        print("   ✅ No major issues detected in current configuration")
    
    print("="*60)
    
    return {
        "total_agents": len(problematic_plan["agents"]),
        "total_assignments": sum(len(agent["file_assignments"]) for agent in problematic_plan["agents"]),
        "total_issues": total_issues,
        "file_retrieval_success_rate": len(file_contents)/len(test_assignments)*100
    }

async def main():
    """Run the diagnostic test."""
    try:
        results = await test_realistic_scenario()
        
        # Save results
        output_file = Path("tests/phase3_diagnostic_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Diagnostic test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())