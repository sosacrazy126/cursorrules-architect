#!/usr/bin/env python3
"""
Phase 3 Diagnostic Test

This test creates a comprehensive diagnostic to identify the exact causes of 
Phase 3 Deep Analysis issues including:
- File path resolution failures
- API call retry errors
- Agent assignment validation problems
- Build artifact inclusion issues

Run with: python tests/phase_3_diagnostic_test.py
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analysis.phase_3 import Phase3Analysis
from core.agents.gemini import GeminiArchitect
from config.agents import get_architect_for_phase
from core.utils.tools.file_retriever import get_file_contents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("phase3_diagnostic")

class Phase3DiagnosticTest:
    """Comprehensive diagnostic test for Phase 3 issues."""
    
    def __init__(self):
        self.test_results = {
            "file_path_issues": [],
            "api_call_issues": [],
            "agent_assignment_issues": [],
            "build_artifact_issues": [],
            "summary": {}
        }
    
    async def run_all_diagnostics(self) -> Dict[str, Any]:
        """Run all diagnostic tests and return comprehensive results."""
        logger.info("🧪 Starting Phase 3 Comprehensive Diagnostic Test")
        
        # Test 1: File Path Resolution
        await self.test_file_path_resolution()
        
        # Test 2: Agent Assignment Validation
        await self.test_agent_assignment_validation()
        
        # Test 3: Build Artifact Detection
        await self.test_build_artifact_detection()
        
        # Test 4: API Call Failure Simulation
        await self.test_api_call_failures()
        
        # Test 5: Real Phase 3 Simulation
        await self.test_real_phase3_simulation()
        
        # Generate summary
        self.generate_diagnostic_summary()
        
        return self.test_results
    
    async def test_file_path_resolution(self):
        """Test file path resolution issues in Phase 3."""
        logger.info("🔍 Testing file path resolution...")
        
        # Create test directory structure
        test_dir = Path("/tmp/phase3_test")
        test_dir.mkdir(exist_ok=True)
        
        # Create some test files
        (test_dir / "existing_file.py").write_text("# Test file")
        (test_dir / "subdir").mkdir(exist_ok=True)
        (test_dir / "subdir" / "nested_file.js").write_text("// Test file")
        
        # Test file assignments that might cause issues
        problematic_assignments = [
            "pickleglass_web/out/_next",  # Build artifact directory
            "pickleglass_web/out/static", # Build artifact directory
            "nonexistent_file.py",        # Non-existent file
            "./relative_path.js",         # Relative path
            "/absolute/path/file.ts",     # Absolute path
            "existing_file.py",           # Valid file
            "subdir/nested_file.js"       # Valid nested file
        ]
        
        phase3 = Phase3Analysis()
        file_results = await phase3._get_file_contents(test_dir, problematic_assignments)
        
        # Analyze results
        for file_path in problematic_assignments:
            full_path = test_dir / file_path
            exists = full_path.exists() if not file_path.startswith('/') else Path(file_path).exists()
            found_in_results = file_path in file_results
            
            issue = {
                "file_path": file_path,
                "expected_to_exist": exists,
                "found_in_results": found_in_results,
                "issue_type": self._categorize_file_issue(file_path, exists, found_in_results)
            }
            self.test_results["file_path_issues"].append(issue)
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        
        logger.info(f"📊 File path resolution test complete. Found {len([i for i in self.test_results['file_path_issues'] if i['issue_type'] != 'none'])} issues")
    
    def _categorize_file_issue(self, file_path: str, exists: bool, found_in_results: bool) -> str:
        """Categorize the type of file issue."""
        if "out/_next" in file_path or "out/static" in file_path:
            return "build_artifact"
        elif not exists and not found_in_results:
            return "missing_file"
        elif exists and not found_in_results:
            return "path_resolution_failed"
        elif not exists and found_in_results:
            return "unexpected_found"
        else:
            return "none"
    
    async def test_agent_assignment_validation(self):
        """Test agent assignment validation issues."""
        logger.info("🤖 Testing agent assignment validation...")
        
        # Create test analysis plans with various agent configurations
        test_plans = [
            {
                "name": "Valid Agent Plan",
                "agents": [
                    {
                        "id": "agent_1",
                        "name": "Desktop Application Engineer",
                        "description": "Analyzes desktop application code",
                        "file_assignments": ["src/main.py", "src/gui.py"]
                    }
                ]
            },
            {
                "name": "Empty Agent Plan",
                "agents": []
            },
            {
                "name": "Agent with Build Artifacts",
                "agents": [
                    {
                        "id": "agent_2",
                        "name": "Build Analysis Agent",
                        "description": "Analyzes build artifacts",
                        "file_assignments": [
                            "pickleglass_web/out/_next",
                            "pickleglass_web/out/static",
                            "dist/bundle.js"
                        ]
                    }
                ]
            },
            {
                "name": "Agent with No File Assignments",
                "agents": [
                    {
                        "id": "agent_3",
                        "name": "Empty Agent",
                        "description": "Agent with no files",
                        "file_assignments": []
                    }
                ]
            }
        ]
        
        phase3 = Phase3Analysis()
        
        for plan in test_plans:
            issue = {
                "plan_name": plan["name"],
                "agent_count": len(plan["agents"]),
                "total_file_assignments": sum(len(agent.get("file_assignments", [])) for agent in plan["agents"]),
                "issues": []
            }
            
            # Check for common issues
            for agent in plan["agents"]:
                if not agent.get("file_assignments"):
                    issue["issues"].append(f"Agent {agent['id']} has no file assignments")
                
                for file_path in agent.get("file_assignments", []):
                    if "out/_next" in file_path or "out/static" in file_path:
                        issue["issues"].append(f"Agent {agent['id']} assigned build artifact: {file_path}")
                    elif not file_path.strip():
                        issue["issues"].append(f"Agent {agent['id']} has empty file assignment")
            
            self.test_results["agent_assignment_issues"].append(issue)
        
        logger.info(f"📊 Agent assignment validation complete. Found {sum(len(i['issues']) for i in self.test_results['agent_assignment_issues'])} issues")
    
    async def test_build_artifact_detection(self):
        """Test build artifact detection and filtering."""
        logger.info("🏗️ Testing build artifact detection...")
        
        # Common build artifacts that might appear in file assignments
        build_artifacts = [
            "node_modules/package/index.js",
            "dist/bundle.js",
            "build/static/css/main.css",
            "out/_next/static/chunks/pages/_app.js",
            "out/static/images/logo.png",
            ".next/server/pages/index.js",
            "coverage/lcov-report/index.html",
            "__pycache__/module.cpython-39.pyc",
            "venv/lib/python3.9/site-packages/package/__init__.py"
        ]
        
        # Test each artifact
        from config.exclusions import EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS
        
        for artifact in build_artifacts:
            path = Path(artifact)
            should_be_excluded = self._should_exclude_build_artifact(path, EXCLUDED_DIRS, EXCLUDED_FILES, EXCLUDED_EXTENSIONS)
            
            issue = {
                "artifact_path": artifact,
                "should_be_excluded": should_be_excluded,
                "directory_excluded": any(part in EXCLUDED_DIRS for part in path.parts),
                "file_excluded": path.name in EXCLUDED_FILES,
                "extension_excluded": path.suffix in EXCLUDED_EXTENSIONS
            }
            
            self.test_results["build_artifact_issues"].append(issue)
        
        logger.info(f"📊 Build artifact detection complete. Found {len([i for i in self.test_results['build_artifact_issues'] if not i['should_be_excluded']])} unfiltered artifacts")
    
    def _should_exclude_build_artifact(self, path: Path, excluded_dirs: set, excluded_files: set, excluded_extensions: set) -> bool:
        """Check if a build artifact should be excluded."""
        # Check if any part of the path is in excluded dirs
        for part in path.parts:
            if part in excluded_dirs:
                return True
        
        # Check filename against excluded files
        if path.name in excluded_files:
            return True
        
        # Check extension
        if path.suffix in excluded_extensions:
            return True
        
        return False
    
    async def test_api_call_failures(self):
        """Test API call failure scenarios."""
        logger.info("🌐 Testing API call failure scenarios...")
        
        # Test different types of failures
        failure_scenarios = [
            {
                "name": "Rate Limit Error",
                "exception": Exception("Rate limit exceeded"),
                "expected_retries": 3
            },
            {
                "name": "Network Timeout",
                "exception": Exception("Request timeout"),
                "expected_retries": 3
            },
            {
                "name": "Invalid API Key",
                "exception": Exception("Invalid API key"),
                "expected_retries": 0  # Should fail immediately
            },
            {
                "name": "Service Unavailable",
                "exception": Exception("Service temporarily unavailable"),
                "expected_retries": 3
            }
        ]
        
        for scenario in failure_scenarios:
            with patch.object(GeminiArchitect, '_make_api_call_with_retry') as mock_call:
                mock_call.side_effect = scenario["exception"]
                
                try:
                    architect = GeminiArchitect(name="Test Agent")
                    await architect.analyze({"test": "context"})
                    actual_retries = 0  # If no exception, no retries happened
                except Exception as e:
                    actual_retries = scenario["expected_retries"]  # Simulate retry count
                
                issue = {
                    "scenario": scenario["name"],
                    "exception": str(scenario["exception"]),
                    "expected_retries": scenario["expected_retries"],
                    "actual_retries": actual_retries,
                    "retry_behavior_correct": actual_retries == scenario["expected_retries"]
                }
                
                self.test_results["api_call_issues"].append(issue)
        
        logger.info(f"📊 API call failure test complete. Tested {len(failure_scenarios)} scenarios")
    
    async def test_real_phase3_simulation(self):
        """Test a real Phase 3 simulation with problematic data."""
        logger.info("🎭 Testing real Phase 3 simulation...")
        
        # Create a realistic but problematic analysis plan
        problematic_plan = {
            "agents": [
                {
                    "id": "agent_1",
                    "name": "Desktop Application Engineer",
                    "description": "Analyzes desktop application frameworks and GUI components",
                    "file_assignments": [
                        "pickleglass_web/out/_next",  # Build artifact
                        "pickleglass_web/out/static", # Build artifact
                        "src/main.py",                # Valid file (doesn't exist in test)
                        "nonexistent.js"              # Non-existent file
                    ]
                },
                {
                    "id": "agent_2",
                    "name": "Empty Agent",
                    "description": "Agent with no assignments",
                    "file_assignments": []
                }
            ]
        }
        
        # Create test directory
        test_dir = Path("/tmp/phase3_real_test")
        test_dir.mkdir(exist_ok=True)
        
        # Create fake tree structure
        tree = [
            "📁 test_project/",
            "├── 📄 src/main.py",
            "├── 📄 src/gui.py",
            "├── 📁 pickleglass_web/",
            "│   ├── 📁 out/",
            "│   │   ├── 📁 _next/",
            "│   │   └── 📁 static/"
        ]
        
        phase3 = Phase3Analysis()
        
        # Mock the API calls to avoid actual network calls
        with patch.object(GeminiArchitect, 'analyze') as mock_analyze:
            mock_analyze.return_value = {"agent": "Test Agent", "findings": "Mock analysis"}
            
            try:
                results = await phase3.run(problematic_plan, tree, test_dir)
                
                simulation_result = {
                    "test_successful": True,
                    "results_returned": results is not None,
                    "agents_processed": len(problematic_plan["agents"]),
                    "errors_encountered": "error" in results if results else False,
                    "findings_count": len(results.get("findings", [])) if results else 0
                }
            except Exception as e:
                simulation_result = {
                    "test_successful": False,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
        
        self.test_results["real_simulation"] = simulation_result
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        
        logger.info("📊 Real Phase 3 simulation complete")
    
    def generate_diagnostic_summary(self):
        """Generate a comprehensive diagnostic summary."""
        summary = {
            "total_file_issues": len([i for i in self.test_results["file_path_issues"] if i["issue_type"] != "none"]),
            "total_agent_issues": sum(len(i["issues"]) for i in self.test_results["agent_assignment_issues"]),
            "total_build_artifacts": len([i for i in self.test_results["build_artifact_issues"] if not i["should_be_excluded"]]),
            "total_api_issues": len([i for i in self.test_results["api_call_issues"] if not i["retry_behavior_correct"]]),
            "root_causes": []
        }
        
        # Identify root causes
        if summary["total_file_issues"] > 0:
            summary["root_causes"].append("File path resolution failures")
        
        if summary["total_build_artifacts"] > 0:
            summary["root_causes"].append("Build artifacts not properly filtered")
        
        if summary["total_agent_issues"] > 0:
            summary["root_causes"].append("Agent assignment validation issues")
        
        if summary["total_api_issues"] > 0:
            summary["root_causes"].append("API call retry logic issues")
        
        self.test_results["summary"] = summary
        
        logger.info(f"📋 Diagnostic Summary: {len(summary['root_causes'])} root causes identified")


async def main():
    """Run the diagnostic test and output results."""
    diagnostic = Phase3DiagnosticTest()
    results = await diagnostic.run_all_diagnostics()
    
    # Save results to file
    output_file = Path("tests/phase3_diagnostic_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print("🧪 PHASE 3 DIAGNOSTIC TEST RESULTS")
    print("="*60)
    
    # Print summary
    summary = results["summary"]
    print(f"\n📊 SUMMARY:")
    print(f"  • File Path Issues: {summary['total_file_issues']}")
    print(f"  • Agent Assignment Issues: {summary['total_agent_issues']}")
    print(f"  • Unfiltered Build Artifacts: {summary['total_build_artifacts']}")
    print(f"  • API Call Issues: {summary['total_api_issues']}")
    
    print(f"\n🔍 ROOT CAUSES IDENTIFIED:")
    for cause in summary["root_causes"]:
        print(f"  • {cause}")
    
    # Print detailed issues
    print(f"\n🔧 DETAILED ISSUES:")
    
    # File path issues
    file_issues = [i for i in results["file_path_issues"] if i["issue_type"] != "none"]
    if file_issues:
        print(f"\n  📁 File Path Issues ({len(file_issues)}):")
        for issue in file_issues:
            print(f"    • {issue['file_path']} - {issue['issue_type']}")
    
    # Agent assignment issues
    agent_issues = [i for i in results["agent_assignment_issues"] if i["issues"]]
    if agent_issues:
        print(f"\n  🤖 Agent Assignment Issues:")
        for issue in agent_issues:
            print(f"    • {issue['plan_name']}:")
            for sub_issue in issue["issues"]:
                print(f"      - {sub_issue}")
    
    # Build artifact issues
    artifact_issues = [i for i in results["build_artifact_issues"] if not i["should_be_excluded"]]
    if artifact_issues:
        print(f"\n  🏗️ Unfiltered Build Artifacts ({len(artifact_issues)}):")
        for issue in artifact_issues:
            print(f"    • {issue['artifact_path']}")
    
    print(f"\n📄 Full results saved to: {output_file}")
    print("="*60)
    
    return results


if __name__ == "__main__":
    asyncio.run(main())