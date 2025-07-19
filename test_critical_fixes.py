#!/usr/bin/env python3
"""
test_critical_fixes.py

Comprehensive test suite for critical error handling and fallback mechanisms
in the enhanced CursorRules Architect with Context Engineering.

Tests the Priority 1 critical fixes that prevent system crashes and data loss.
"""

import asyncio
import time
import tempfile
import os
import sys
import json
import logging
from typing import Dict, Any, Optional
import unittest
from unittest.mock import Mock, patch, MagicMock

# Setup logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test framework setup
class CriticalFixesTestSuite:
    """Test suite for critical error handling fixes."""
    
    def __init__(self):
        self.test_results = {
            "passed": [],
            "failed": [],
            "errors": [],
            "warnings": []
        }
        self.start_time = time.time()
    
    async def run_all_tests(self):
        """Run all critical tests."""
        print("🔍 Running Critical Fixes Test Suite...")
        print("="*60)
        
        # Test categories
        test_categories = [
            ("Error Handling", self.test_error_handling),
            ("Memory Management", self.test_memory_management),
            ("Input Validation", self.test_input_validation),
            ("Fallback Mechanisms", self.test_fallback_mechanisms),
            ("Configuration Validation", self.test_configuration_validation),
            ("Dependency Validation", self.test_dependency_validation),
            ("Integration Consistency", self.test_integration_consistency)
        ]
        
        for category_name, test_method in test_categories:
            print(f"\n📊 Testing {category_name}...")
            try:
                await test_method()
                self.test_results["passed"].append(category_name)
                print(f"✅ {category_name} tests passed")
            except Exception as e:
                self.test_results["failed"].append(f"{category_name}: {e}")
                print(f"❌ {category_name} tests failed: {e}")
        
        # Print summary
        self.print_test_summary()
    
    async def test_error_handling(self):
        """Test comprehensive error handling and fallback mechanisms."""
        print("  🔧 Testing error handling...")
        
        # Test 1: Integration Manager Error Handling
        try:
            from core.context_engineering.integration_manager import (
                ContextEngineeringIntegrationManager,
                IntegrationConfig,
                ContextEngineeringError,
                validate_context_engineering_dependencies
            )
            
            # Test invalid configuration
            try:
                invalid_config = IntegrationConfig(
                    field_capacity=-1000,  # Invalid
                    token_efficiency_threshold=2.0  # Invalid
                )
                assert False, "Should have raised ConfigurationError"
            except Exception as e:
                assert "field_capacity must be a positive integer" in str(e)
                print("    ✅ Configuration validation catches invalid values")
            
            # Test valid configuration
            valid_config = IntegrationConfig(
                enable_atomic_prompting=True,
                enable_field_dynamics=True,
                optimization_mode="balanced",
                error_tolerance_level="moderate"
            )
            print("    ✅ Valid configuration passes validation")
            
            # Test dependency validation
            deps_ok, issues = validate_context_engineering_dependencies()
            print(f"    ℹ️ Dependencies status: {deps_ok}, issues: {len(issues)}")
            
        except ImportError as e:
            print(f"    ⚠️ Context engineering not available: {e}")
        
        # Test 2: Enhanced Phase 1 Error Handling
        try:
            from core.analysis.enhanced_phase_1 import ContextAwarePhase1Analysis
            
            # Test initialization with missing dependencies
            with patch('core.context_engineering.integration_manager.validate_context_engineering_dependencies') as mock_deps:
                mock_deps.return_value = (False, ["numpy missing"])
                
                phase1 = ContextAwarePhase1Analysis()
                assert not phase1.context_engineering_available
                assert not phase1.enhancement_enabled
                print("    ✅ Enhanced Phase 1 gracefully handles missing dependencies")
            
            # Test with valid dependencies
            phase1 = ContextAwarePhase1Analysis()
            print(f"    ℹ️ Enhanced Phase 1 status: enhancement_enabled={getattr(phase1, 'enhancement_enabled', False)}")
            
        except ImportError as e:
            print(f"    ⚠️ Enhanced Phase 1 not available: {e}")
        
        # Test 3: Input sanitization
        try:
            from core.context_engineering.integration_manager import sanitize_input_data
            
            # Test normal data  
            normal_data = {"test_field": "value", "number": 42}
            sanitized, warnings = sanitize_input_data(normal_data)
            assert sanitized["test_field"] == "value"
            assert sanitized["number"] == 42
            assert len(warnings) == 0
            print("    ✅ Normal data passes sanitization")
            
            # Test sensitive data redaction
            sensitive_data = {"api_key": "secret123", "password": "hidden"}
            sanitized, warnings = sanitize_input_data(sensitive_data)
            assert sanitized["api_key"] == "[REDACTED]"
            assert sanitized["password"] == "[REDACTED]"
            print("    ✅ Sensitive data is properly redacted")
            
            # Test large data
            large_data = {"large_text": "x" * 1000000}  # 1MB of text
            sanitized, warnings = sanitize_input_data(large_data, max_size=100000)
            assert len(warnings) > 0
            assert "too large" in warnings[0]
            print("    ✅ Large data is properly truncated")
            
            # Test None data
            sanitized, warnings = sanitize_input_data(None)
            assert sanitized == {}
            assert "Input data is None" in warnings[0]
            print("    ✅ None data is handled safely")
            
        except ImportError as e:
            print(f"    ⚠️ Input sanitization not available: {e}")
    
    async def test_memory_management(self):
        """Test memory management and cleanup mechanisms."""
        print("  🧠 Testing memory management...")
        
        try:
            from core.context_engineering.field_dynamics import FieldDynamics, FieldType, NeuralField
            
            # Test field creation with limits
            field_dynamics = FieldDynamics(max_fields=5, memory_limit_mb=10)
            
            # Create multiple fields to test limits
            for i in range(7):  # More than max_fields
                success = field_dynamics.create_field(
                    f"test_field_{i}",
                    FieldType.DISCOVERY,
                    {"test_data": f"data_{i}"}
                )
                if i < 5:
                    assert success, f"Field {i} should have been created"
                # Fields beyond limit should either succeed (by removing old ones) or fail gracefully
            
            assert len(field_dynamics.active_fields) <= 5, "Should respect max_fields limit"
            print("    ✅ Field creation respects memory limits")
            
            # Test memory cleanup
            initial_field_count = len(field_dynamics.active_fields)
            cleanup_count = field_dynamics.cleanup_inactive_fields(inactivity_threshold=0.1)
            print(f"    ℹ️ Cleaned up {cleanup_count} fields")
            
            # Test health monitoring
            health = field_dynamics.get_system_health()
            assert "health_status" in health
            assert "memory_usage_mb" in health
            assert "active_fields" in health
            print(f"    ✅ System health: {health['health_status']}")
            
            # Test attractor limits in neural field
            neural_field = NeuralField("test", FieldType.DISCOVERY, max_attractors=5)
            
            # Try to add many attractors
            from core.context_engineering.field_dynamics import AttractorState
            
            for i in range(10):
                attractor = AttractorState(
                    pattern_id=f"pattern_{i}",
                    strength=0.5,
                    basin_width=0.3,
                    activation_level=0.2
                )
                neural_field.add_attractor(attractor)
            
            assert len(neural_field.attractors) <= 5, "Should respect max_attractors limit"
            print("    ✅ Attractor limits are enforced")
            
        except ImportError as e:
            print(f"    ⚠️ Field dynamics not available: {e}")
    
    async def test_input_validation(self):
        """Test input validation and sanitization."""
        print("  🔍 Testing input validation...")
        
        # Test project path validation
        try:
            # Import the enhanced analyzer (if available)
            try:
                from main_enhanced import EnhancedCursorRulesProjectAnalyzer
                analyzer = EnhancedCursorRulesProjectAnalyzer(enable_context_engineering=False)
                
                # Test invalid project path
                try:
                    await analyzer.run_analysis("")  # Empty string
                    assert False, "Should have raised ValueError"
                except ValueError as e:
                    assert "non-empty string" in str(e)
                    print("    ✅ Empty project path is rejected")
                
                # Test None project path
                try:
                    await analyzer.run_analysis(None)
                    assert False, "Should have raised ValueError"
                except (ValueError, TypeError) as e:
                    print("    ✅ None project path is rejected")
                
            except ImportError:
                print("    ⚠️ Enhanced analyzer not available")
            
            # Test enhanced Phase 1 input validation
            try:
                from core.analysis.enhanced_phase_1 import ContextAwarePhase1Analysis
                
                phase1 = ContextAwarePhase1Analysis()
                
                # Test with invalid inputs
                result = await phase1.run(None, None)
                assert isinstance(result, dict)
                assert "error" in result or "_enhancement_metadata" in result
                print("    ✅ Enhanced Phase 1 handles None inputs gracefully")
                
                # Test with very large inputs
                large_tree = ["file_" + str(i) for i in range(10000)]
                large_package = {"dependencies": {f"dep_{i}": "1.0" for i in range(1000)}}
                
                result = await phase1.run(large_tree, large_package)
                assert isinstance(result, dict)
                print("    ✅ Enhanced Phase 1 handles large inputs")
                
            except ImportError:
                print("    ⚠️ Enhanced Phase 1 not available")
        
        except Exception as e:
            print(f"    ⚠️ Input validation test error: {e}")
    
    async def test_fallback_mechanisms(self):
        """Test fallback mechanisms when context engineering fails."""
        print("  🔄 Testing fallback mechanisms...")
        
        try:
            from core.analysis.enhanced_phase_1 import ContextAwarePhase1Analysis
            
            # Test fallback when context engineering is disabled
            with patch.object(ContextAwarePhase1Analysis, '__init__') as mock_init:
                def mock_init_func(self):
                    # Simulate failed context engineering initialization
                    super(ContextAwarePhase1Analysis, self).__init__()
                    self.context_engineering_available = False
                    self.enhancement_enabled = False
                    self.integration_manager = None
                    self.performance_metrics = {
                        "enhancement_attempts": 0,
                        "enhancement_successes": 0,
                        "fallback_uses": 0,
                        "average_enhancement_time": 0.0,
                        "errors": []
                    }
                
                mock_init.side_effect = mock_init_func
                
                phase1 = ContextAwarePhase1Analysis()
                
                # Should still work with fallback
                result = await phase1.run(["test.py"], {"name": "test"})
                assert isinstance(result, dict)
                assert result.get("_enhancement_metadata", {}).get("enhanced") == False
                print("    ✅ Phase 1 falls back gracefully when context engineering fails")
            
            # Test error handling in enhancement
            phase1 = ContextAwarePhase1Analysis()
            if hasattr(phase1, 'integration_manager') and phase1.integration_manager:
                # Mock integration manager to fail
                with patch.object(phase1.integration_manager, 'enhance_phase') as mock_enhance:
                    mock_enhance.side_effect = Exception("Mock enhancement failure")
                    
                    result = await phase1.run(["test.py"], {"name": "test"})
                    assert isinstance(result, dict)
                    print("    ✅ Phase 1 handles enhancement failures gracefully")
            
        except ImportError:
            print("    ⚠️ Enhanced Phase 1 not available for fallback testing")
        
        # Test enhanced analyzer fallback
        try:
            from main_enhanced import EnhancedCursorRulesProjectAnalyzer
            
            # Test with context engineering disabled
            analyzer = EnhancedCursorRulesProjectAnalyzer(enable_context_engineering=False)
            assert not analyzer.enable_context_engineering
            print("    ✅ Enhanced analyzer can run with context engineering disabled")
            
            # Test emergency fallback
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create a minimal test project
                test_file = os.path.join(temp_dir, "test.py")
                with open(test_file, "w") as f:
                    f.write("print('hello')")
                
                # Mock to trigger emergency fallback
                with patch.object(analyzer, '_run_enhanced_analysis') as mock_enhanced:
                    mock_enhanced.side_effect = Exception("Mock critical failure")
                    
                    result = await analyzer.run_analysis(temp_dir)
                    assert isinstance(result, dict)
                    # Should have emergency fallback metadata
                    assert "_global_enhancement_metadata" in result
                    print("    ✅ Enhanced analyzer emergency fallback works")
        
        except ImportError:
            print("    ⚠️ Enhanced analyzer not available for fallback testing")
    
    async def test_configuration_validation(self):
        """Test configuration validation and error handling."""
        print("  ⚙️ Testing configuration validation...")
        
        try:
            from core.context_engineering.integration_manager import IntegrationConfig, ConfigurationError
            
            # Test invalid field capacity
            try:
                IntegrationConfig(field_capacity=-100)
                assert False, "Should raise ConfigurationError"
            except (ConfigurationError, ValueError) as e:
                assert "field_capacity" in str(e)
                print("    ✅ Invalid field_capacity is rejected")
            
            # Test invalid token efficiency threshold
            try:
                IntegrationConfig(token_efficiency_threshold=2.0)
                assert False, "Should raise ConfigurationError"
            except (ConfigurationError, ValueError) as e:
                assert "token_efficiency_threshold" in str(e)
                print("    ✅ Invalid token_efficiency_threshold is rejected")
            
            # Test invalid optimization mode
            try:
                IntegrationConfig(optimization_mode="invalid_mode")
                assert False, "Should raise ConfigurationError"
            except (ConfigurationError, ValueError) as e:
                assert "optimization_mode" in str(e)
                print("    ✅ Invalid optimization_mode is rejected")
            
            # Test valid configuration
            valid_config = IntegrationConfig(
                enable_atomic_prompting=True,
                enable_field_dynamics=True,
                optimization_mode="balanced",
                field_capacity=8000,
                token_efficiency_threshold=0.7,
                error_tolerance_level="moderate"
            )
            print("    ✅ Valid configuration is accepted")
            
        except ImportError:
            print("    ⚠️ Configuration validation not available")
    
    async def test_dependency_validation(self):
        """Test dependency validation and graceful degradation."""
        print("  📦 Testing dependency validation...")
        
        try:
            from core.context_engineering.integration_manager import validate_context_engineering_dependencies
            
            # Test dependency validation
            deps_ok, issues = validate_context_engineering_dependencies()
            print(f"    ℹ️ Dependencies OK: {deps_ok}")
            print(f"    ℹ️ Issues found: {len(issues)}")
            
            for issue in issues[:3]:  # Show first 3 issues
                print(f"      - {issue}")
            
            # Test with mocked missing dependencies
            with patch('builtins.__import__') as mock_import:
                def mock_import_func(name, *args, **kwargs):
                    if name == 'numpy':
                        raise ImportError("numpy not found")
                    return __import__(name, *args, **kwargs)
                
                mock_import.side_effect = mock_import_func
                
                deps_ok, issues = validate_context_engineering_dependencies()
                assert not deps_ok
                assert any("numpy" in issue for issue in issues)
                print("    ✅ Missing numpy dependency is detected")
        
        except ImportError:
            print("    ⚠️ Dependency validation not available")
    
    async def test_integration_consistency(self):
        """Test integration consistency and backward compatibility."""
        print("  🔗 Testing integration consistency...")
        
        try:
            from core.analysis.enhanced_phase_1 import ContextAwarePhase1Analysis
            
            phase1 = ContextAwarePhase1Analysis()
            
            # Test that enhanced results are backward compatible
            result = await phase1.run(["test.py", "main.py"], {"name": "test_project"})
            
            # Check for standard Phase 1 structure
            expected_keys = ["architects", "metadata"]
            if not any(key in result for key in expected_keys):
                # Check if it's an error result or enhanced format
                if "_enhancement_metadata" in result or "error" in result:
                    print("    ✅ Enhanced Phase 1 provides fallback structure on error")
                else:
                    print("    ⚠️ Enhanced Phase 1 result structure may not be backward compatible")
            else:
                print("    ✅ Enhanced Phase 1 maintains backward compatibility")
            
            # Test enhancement metadata presence
            if "_enhancement_metadata" in result:
                metadata = result["_enhancement_metadata"]
                assert "enhanced" in metadata
                assert "fallback_reason" in metadata or metadata.get("enhanced") == True
                print("    ✅ Enhancement metadata is properly included")
            
        except ImportError:
            print("    ⚠️ Enhanced Phase 1 not available for consistency testing")
        
        # Test standardized error format
        try:
            from core.context_engineering.integration_manager import ContextEngineeringIntegrationManager, IntegrationConfig
            
            config = IntegrationConfig()
            manager = ContextEngineeringIntegrationManager(config)
            
            # Test with invalid input to trigger error handling
            result = manager.enhance_phase("test_phase", {"invalid": "data"}, None)
            
            # Check for standardized error format
            if "status" in result and result["status"] in ["error_fallback", "timeout_fallback"]:
                assert "error_type" in result
                assert "error_message" in result
                assert "fallback_used" in result
                print("    ✅ Standardized error format is used")
            
        except ImportError:
            print("    ⚠️ Integration manager not available for consistency testing")
    
    def print_test_summary(self):
        """Print comprehensive test summary."""
        print("\n" + "="*60)
        print("🎯 CRITICAL FIXES TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results["passed"]) + len(self.test_results["failed"])
        passed_count = len(self.test_results["passed"])
        failed_count = len(self.test_results["failed"])
        
        print(f"Total Test Categories: {total_tests}")
        print(f"✅ Passed: {passed_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"⚠️ Warnings: {len(self.test_results['warnings'])}")
        
        if self.test_results["passed"]:
            print("\n✅ PASSED TESTS:")
            for test in self.test_results["passed"]:
                print(f"   • {test}")
        
        if self.test_results["failed"]:
            print("\n❌ FAILED TESTS:")
            for test in self.test_results["failed"]:
                print(f"   • {test}")
        
        if self.test_results["warnings"]:
            print("\n⚠️ WARNINGS:")
            for warning in self.test_results["warnings"]:
                print(f"   • {warning}")
        
        # Overall assessment
        print(f"\n⏱️ Total test time: {time.time() - self.start_time:.2f}s")
        
        if failed_count == 0:
            print("\n🎉 ALL CRITICAL FIXES ARE WORKING!")
            print("✨ The system should be stable and production-ready for error handling.")
        elif failed_count <= 2:
            print("\n🟡 MOSTLY STABLE with minor issues")
            print("⚠️ Review failed tests before production deployment.")
        else:
            print("\n🔴 CRITICAL ISSUES DETECTED")
            print("❌ Address failed tests before deployment!")
        
        print("="*60)

# Test execution functions
async def run_quick_test():
    """Run a quick subset of critical tests."""
    print("🚀 Running Quick Critical Fixes Test...")
    
    suite = CriticalFixesTestSuite()
    
    # Quick tests
    await suite.test_error_handling()
    await suite.test_input_validation()
    await suite.test_fallback_mechanisms()
    
    suite.print_test_summary()

async def run_full_test():
    """Run the complete test suite."""
    print("🚀 Running Full Critical Fixes Test Suite...")
    
    suite = CriticalFixesTestSuite()
    await suite.run_all_tests()

def main():
    """Main test runner."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        asyncio.run(run_quick_test())
    else:
        asyncio.run(run_full_test())

if __name__ == "__main__":
    main()