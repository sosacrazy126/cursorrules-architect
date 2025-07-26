"""
Master test runner for all CursorRules Architect context engineering features.

Runs comprehensive tests for:
- Protocol Engine and Phase 2 Protocol Integration
- Context Field Engine and Analysis Context Integration
"""

import sys
import os
import unittest
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import test modules
from tests.test_protocol_engine import run_protocol_tests
from tests.test_context_field_engine import run_context_field_tests


def print_test_header():
    """Print test header with timestamp."""
    print("=" * 80)
    print("🚀 CursorRules Architect Context Engineering Test Suite")
    print("=" * 80)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Testing: Memory Agent, Protocol Engine, Context Field Engine")
    print("-" * 80)


def print_test_summary(results):
    """Print test summary."""
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    for component, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{component:<30} {status}")
    
    print("-" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED! Context engineering features are ready.")
    else:
        print(f"\n⚠️  {failed_tests} test suite(s) failed. Please review the output above.")
    
    print("=" * 80)


def run_integration_tests():
    """Run integration tests across all components."""
    print("\n🔗 Running Integration Tests...")
    
    try:
        # Import all components to test basic integration
        from core.protocol.protocol_engine import ProtocolEngine
        from core.protocol.phase2_protocol_integration import Phase2ProtocolIntegration
        from core.context.context_field_engine import ContextFieldEngine
        from core.context.analysis_context_integration import AnalysisContextIntegration
        
        print("✅ All modules imported successfully")
        
        # Test basic instantiation
        import tempfile
        temp_json = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        temp_json.close()

        protocol_engine = ProtocolEngine(temp_json.name)
        field_engine = ContextFieldEngine()

        print("✅ All engines instantiated successfully")

        # Test basic operations
        protocol_engine.clarify_context({"protocol_name": "Integration Test Protocol"})

        field_engine.create_attractor("integration_test", field_engine.AttractorType.CONCEPT,
                                    (25, 25, 25))

        print("✅ Basic operations completed successfully")

        # Test integration layers
        protocol_integration = Phase2ProtocolIntegration(temp_json.name)
        context_integration = AnalysisContextIntegration()

        print("✅ Integration layers instantiated successfully")
        
        # Cleanup temp files
        import os
        try:
            os.unlink(temp_json.name)
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False


def run_comprehensive_scenario_test():
    """Run a comprehensive scenario test using all components together."""
    print("\n🎭 Running Comprehensive Scenario Test...")
    
    try:
        # Simulate a complete analysis workflow
        from core.protocol.phase2_protocol_integration import Phase2ProtocolIntegration
        from core.context.analysis_context_integration import AnalysisContextIntegration
        
        # Initialize all systems with temp files
        import tempfile
        temp_protocol_json = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        temp_protocol_json.close()

        protocol_system = Phase2ProtocolIntegration(temp_protocol_json.name)
        context_system = AnalysisContextIntegration()
        
        print("✅ All systems initialized")
        
        # Simulate project analysis workflow
        project_context = {
            "name": "Comprehensive Test Project",
            "type": "web_application",
            "technologies": ["React", "Node.js", "PostgreSQL"],
            "complexity": "high"
        }
        
        # 1. Start analysis session in memory system
        memory_project_id = memory_system.start_analysis_session(
            "/test/comprehensive", "Comprehensive Test Project"
        )
        print("✅ Memory system: Analysis session started")
        
        # 2. Create analysis protocol
        stakeholders = [
            {"role": "initiator", "expertise": "full_stack_development"},
            {"role": "reviewer", "expertise": "system_architecture"}
        ]
        protocol_name = protocol_system.create_analysis_protocol(
            project_context, stakeholders
        )
        print("✅ Protocol system: Analysis protocol created")
        
        # 3. Start field analysis
        field_session_id = context_system.start_field_analysis(project_context)
        print("✅ Context system: Field analysis started")
        
        # 4. Simulate phase analysis with all systems
        phase_data = {
            "technologies": ["React", "Node.js"],
            "patterns": ["Component-based", "API-driven"],
            "key_findings": ["Modern architecture", "Good separation of concerns"],
            "complexity_score": 7.5
        }
        
        # Store in memory system
        memory_phase_id = memory_system.store_phase_analysis(
            "Discovery", phase_data, 1
        )
        print("✅ Memory system: Phase analysis stored")
        
        # Get analysis strategy from protocol system
        strategy = protocol_system.get_analysis_strategy(
            protocol_name, ["React", "Node.js", "PostgreSQL"]
        )
        print("✅ Protocol system: Analysis strategy retrieved")
        
        # Enhance phase with field dynamics
        enhanced_phase = context_system.enhance_phase_with_field(
            "Discovery", phase_data, 1
        )
        print("✅ Context system: Phase enhanced with field dynamics")
        
        # 5. Cross-system insights
        similar_projects = memory_system.get_similar_projects(
            ["React", "Node.js"], "web_application"
        )
        
        cross_patterns = context_system.get_cross_phase_patterns()
        
        protocol_evolution = protocol_system.get_protocol_evolution_for_project(
            protocol_name
        )
        
        print("✅ Cross-system insights generated")
        
        # 6. Cleanup
        memory_system.end_analysis_session()
        context_system.end_field_analysis()
        
        # Cleanup temp files
        import os
        try:
            os.unlink(temp_memory_db.name)
            os.unlink(temp_protocol_json.name)
        except:
            pass
        
        print("✅ All sessions ended successfully")
        print("🎉 Comprehensive scenario test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive scenario test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test runner."""
    print_test_header()
    
    # Track test results
    test_results = {}
    
    # Run individual component tests
    print("\n🔄 Testing Protocol Engine Components...")
    test_results["Protocol Engine"] = run_protocol_tests()
    
    print("\n🌊 Testing Context Field Engine Components...")
    test_results["Context Field Engine"] = run_context_field_tests()
    
    # Run integration tests
    print("\n🔗 Testing Component Integration...")
    test_results["Integration Tests"] = run_integration_tests()
    
    # Run comprehensive scenario test
    print("\n🎭 Testing Complete Workflow...")
    test_results["Comprehensive Scenario"] = run_comprehensive_scenario_test()
    
    # Print summary
    print_test_summary(test_results)
    
    # Return overall success
    return all(test_results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)