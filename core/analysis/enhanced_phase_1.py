"""
core/analysis/enhanced_phase_1.py

Enhanced Phase 1 Analysis with Context Engineering Integration
ENHANCED: Critical error handling and fallback mechanisms added
"""

import asyncio
import logging
import time
import traceback
from typing import Dict, List, Any, Optional
from core.analysis.phase_1 import Phase1Analysis
from core.context_engineering.integration_manager import (
    ContextEngineeringIntegrationManager, 
    IntegrationConfig,
    ContextEngineeringError,
    validate_context_engineering_dependencies,
    sanitize_input_data
)

logger = logging.getLogger(__name__)

class EnhancedPhase1Error(Exception):
    """Error specific to Enhanced Phase 1 operations."""
    pass

class ContextAwarePhase1Analysis(Phase1Analysis):
    """Enhanced Phase 1 with context engineering capabilities and robust error handling."""
    
    def __init__(self):
        """Initialize with error handling for context engineering components."""
        try:
            # Initialize base Phase 1
            super().__init__()
            
            # Validate context engineering dependencies
            deps_ok, dep_issues = validate_context_engineering_dependencies()
            if not deps_ok:
                logger.warning(f"Context engineering dependencies missing: {dep_issues}")
                self.context_engineering_available = False
                self.integration_manager = None
                self.enhancement_enabled = False
            else:
                if dep_issues:  # Warnings only
                    logger.warning(f"Context engineering warnings: {dep_issues}")
                
                try:
                    # Create integration configuration with error handling
                    self.integration_config = IntegrationConfig(
                        enable_atomic_prompting=True,
                        enable_field_dynamics=True,
                        enable_cognitive_tools=True,
                        enable_pattern_synthesis=True,
                        optimization_mode="balanced",
                        error_tolerance_level="moderate",
                        enable_fallback=True
                    )
                    
                    # Initialize integration manager with error handling
                    self.integration_manager = ContextEngineeringIntegrationManager(
                        self.integration_config
                    )
                    
                    self.context_engineering_available = True
                    self.enhancement_enabled = True
                    logger.info("✅ Enhanced Phase 1 initialized with context engineering")
                    
                except Exception as e:
                    logger.error(f"Failed to initialize context engineering: {e}")
                    self.context_engineering_available = False
                    self.integration_manager = None
                    self.enhancement_enabled = False
                    # Continue with standard Phase 1 only
            
            # Performance tracking
            self.performance_metrics = {
                "enhancement_attempts": 0,
                "enhancement_successes": 0,
                "fallback_uses": 0,
                "average_enhancement_time": 0.0,
                "errors": []
            }
            
        except Exception as e:
            logger.error(f"Critical error in Enhanced Phase 1 initialization: {e}")
            # Fall back to basic Phase 1
            super().__init__()
            self.context_engineering_available = False
            self.integration_manager = None
            self.enhancement_enabled = False
    
    async def run(self, tree: List[str], package_info: Dict) -> Dict[str, Any]:
        """
        Enhanced Phase 1 analysis with comprehensive error handling and fallback.
        
        Args:
            tree: File tree structure
            package_info: Package information
            
        Returns:
            Enhanced analysis results or fallback to original Phase 1
        """
        start_time = time.time()
        self.performance_metrics["enhancement_attempts"] += 1
        
        # Input validation and sanitization
        try:
            tree_sanitized, tree_warnings = sanitize_input_data(tree, max_size=100000)
            package_sanitized, package_warnings = sanitize_input_data(package_info, max_size=50000)
            
            if tree_warnings or package_warnings:
                logger.warning(f"Input sanitization warnings: {tree_warnings + package_warnings}")
                
        except Exception as e:
            logger.error(f"Input sanitization failed: {e}")
            # Use original inputs if sanitization fails
            tree_sanitized, package_sanitized = tree, package_info
        
        # Try enhanced analysis first if available
        if self.enhancement_enabled and self.context_engineering_available:
            try:
                enhanced_results = await self._run_enhanced_analysis(tree_sanitized, package_sanitized)
                
                # Validate enhanced results
                if self._validate_enhanced_results(enhanced_results):
                    processing_time = time.time() - start_time
                    self._update_performance_metrics(True, processing_time)
                    
                    # Ensure backward compatibility
                    return self._ensure_backward_compatibility(enhanced_results)
                else:
                    logger.warning("Enhanced results validation failed, falling back to standard analysis")
                    return await self._fallback_to_standard_analysis(tree_sanitized, package_sanitized, "validation_failed")
                    
            except ContextEngineeringError as e:
                logger.warning(f"Context engineering error: {e}, falling back to standard analysis")
                return await self._fallback_to_standard_analysis(tree_sanitized, package_sanitized, f"context_engineering_error: {e}")
                
            except Exception as e:
                logger.error(f"Enhanced analysis failed: {e}")
                logger.error(f"Stack trace: {traceback.format_exc()}")
                return await self._fallback_to_standard_analysis(tree_sanitized, package_sanitized, f"unknown_error: {e}")
        else:
            # Enhancement not available, use standard analysis
            logger.info("Context engineering not available, using standard Phase 1 analysis")
            return await self._fallback_to_standard_analysis(tree_sanitized, package_sanitized, "enhancement_disabled")
    
    async def _run_enhanced_analysis(self, tree: List[str], package_info: Dict) -> Dict[str, Any]:
        """Run enhanced analysis with context engineering."""
        
        # Check if integration manager is healthy
        if self.integration_manager:
            health = self.integration_manager.field_dynamics.get_system_health() if hasattr(self.integration_manager, 'field_dynamics') and self.integration_manager.field_dynamics else {"health_status": "unknown"}
            if health.get("health_status") in ["critical", "unhealthy", "error"]:
                raise ContextEngineeringError(f"Integration manager unhealthy: {health.get('health_status')}")
        
        # Step 1: Run standard Phase 1 analysis
        try:
            standard_results = await super().run(tree, package_info)
            if "error" in standard_results:
                raise EnhancedPhase1Error(f"Standard Phase 1 failed: {standard_results['error']}")
        except Exception as e:
            raise EnhancedPhase1Error(f"Standard Phase 1 analysis failed: {e}")
        
        # Step 2: Prepare context for enhancement
        try:
            discovery_context = self._prepare_discovery_context(tree, package_info, standard_results)
        except Exception as e:
            logger.warning(f"Context preparation failed: {e}, using minimal context")
            discovery_context = {"tree": tree, "package_info": package_info}
        
        # Step 3: Apply context engineering enhancements
        try:
            enhanced_results = self.integration_manager.enhance_phase(
                "phase_1",
                standard_results,
                {"discovery_context": discovery_context}
            )
            
            # Check if enhancement actually succeeded
            if enhanced_results.get("status") in ["error_fallback", "timeout_fallback"]:
                logger.warning(f"Enhancement failed with status: {enhanced_results.get('status')}")
                # Return standard results with enhancement failure note
                return self._create_fallback_enhanced_result(standard_results, enhanced_results.get("error_message", "Enhancement failed"))
            
        except Exception as e:
            logger.error(f"Context engineering enhancement failed: {e}")
            # Return standard results with error note
            return self._create_fallback_enhanced_result(standard_results, f"Enhancement error: {e}")
        
        # Step 4: Merge results ensuring backward compatibility
        try:
            final_results = self._merge_standard_and_enhanced_results(standard_results, enhanced_results)
        except Exception as e:
            logger.error(f"Result merging failed: {e}")
            # Return standard results if merging fails
            return self._create_fallback_enhanced_result(standard_results, f"Merging error: {e}")
        
        return final_results
    
    def _prepare_discovery_context(self, tree: List[str], package_info: Dict, standard_results: Dict) -> Dict[str, Any]:
        """Prepare context for discovery phase enhancement."""
        try:
            context = {
                "codebase_tree": tree[:1000] if isinstance(tree, list) else str(tree)[:5000],  # Limit size
                "package_metadata": {
                    "name": package_info.get("name", "unknown"),
                    "dependencies": list(package_info.get("dependencies", {}).keys())[:50],  # Limit deps
                    "structure_type": package_info.get("project_type", "unknown")
                },
                "initial_analysis": {
                    "architect_count": len(standard_results.get("architects", {})),
                    "analysis_depth": len(str(standard_results)[:1000]),  # Rough measure
                    "patterns_identified": self._extract_pattern_hints(standard_results)
                }
            }
            
            return context
        except Exception as e:
            logger.warning(f"Context preparation failed: {e}")
            return {"minimal_context": True, "tree_size": len(tree) if tree else 0}
    
    def _extract_pattern_hints(self, standard_results: Dict) -> List[str]:
        """Extract pattern hints from standard analysis for context engineering."""
        try:
            patterns = []
            
            # Look for architectural patterns in architect results
            architects = standard_results.get("architects", {})
            for architect_name, architect_result in architects.items():
                if isinstance(architect_result, dict):
                    analysis_text = str(architect_result.get("analysis", ""))
                    
                    # Simple pattern detection
                    if "mvc" in analysis_text.lower():
                        patterns.append("mvc_architecture")
                    if "microservice" in analysis_text.lower():
                        patterns.append("microservices")
                    if "component" in analysis_text.lower():
                        patterns.append("component_based")
                    if "api" in analysis_text.lower():
                        patterns.append("api_oriented")
            
            # Limit patterns to prevent context explosion
            return patterns[:10]
            
        except Exception as e:
            logger.warning(f"Pattern extraction failed: {e}")
            return ["pattern_extraction_failed"]
    
    def _merge_standard_and_enhanced_results(self, standard_results: Dict, enhanced_results: Dict) -> Dict[str, Any]:
        """Merge standard and enhanced results ensuring backward compatibility."""
        try:
            # Start with standard results as base
            merged_results = standard_results.copy()
            
            # Add context engineering insights as additional data
            if "context_engineering" in enhanced_results:
                merged_results["_context_engineering"] = enhanced_results["context_engineering"]
            
            # Add enhancement metadata
            merged_results["_enhancement_metadata"] = {
                "enhanced": True,
                "enhancement_level": enhanced_results.get("enhancement_level", "unknown"),
                "context_engineering_status": enhanced_results.get("status", "unknown"),
                "features_active": enhanced_results.get("context_engineering", {}).get("features_active", [])
            }
            
            # Enhance standard results if enhanced data is available
            if "enhanced_data" in enhanced_results:
                enhanced_data = enhanced_results["enhanced_data"]
                
                # Carefully merge enhanced data without breaking original structure
                if isinstance(enhanced_data, dict):
                    for key, value in enhanced_data.items():
                        if key not in merged_results:  # Only add new keys
                            merged_results[key] = value
                        elif key == "architects" and isinstance(value, dict):
                            # Enhance architect results
                            merged_results[key] = self._merge_architect_results(
                                merged_results.get(key, {}), value
                            )
            
            return merged_results
            
        except Exception as e:
            logger.error(f"Result merging failed: {e}")
            # Return standard results with error info
            standard_results["_enhancement_error"] = f"Merging failed: {e}"
            return standard_results
    
    def _merge_architect_results(self, original_architects: Dict, enhanced_architects: Dict) -> Dict:
        """Merge original and enhanced architect results."""
        try:
            merged_architects = original_architects.copy()
            
            for architect_name, enhanced_result in enhanced_architects.items():
                if architect_name in merged_architects:
                    # Add enhanced insights to existing architect
                    if isinstance(enhanced_result, dict) and isinstance(merged_architects[architect_name], dict):
                        merged_architects[architect_name]["_enhanced_insights"] = enhanced_result.get("enhanced_analysis", {})
                else:
                    # Add new enhanced architect
                    merged_architects[architect_name] = enhanced_result
            
            return merged_architects
            
        except Exception as e:
            logger.warning(f"Architect result merging failed: {e}")
            return original_architects
    
    async def _fallback_to_standard_analysis(self, tree: List[str], package_info: Dict, reason: str) -> Dict[str, Any]:
        """Fallback to standard Phase 1 analysis with error context."""
        try:
            self.performance_metrics["fallback_uses"] += 1
            logger.info(f"Falling back to standard Phase 1 analysis: {reason}")
            
            # Run standard analysis
            standard_results = await super().run(tree, package_info)
            
            # Add fallback metadata
            standard_results["_enhancement_metadata"] = {
                "enhanced": False,
                "fallback_reason": reason,
                "context_engineering_attempted": True,
                "fallback_time": time.time()
            }
            
            return standard_results
            
        except Exception as e:
            logger.error(f"Fallback analysis also failed: {e}")
            # Return minimal error response
            return {
                "error": f"Both enhanced and standard analysis failed. Enhanced reason: {reason}, Standard error: {e}",
                "_enhancement_metadata": {
                    "enhanced": False,
                    "total_failure": True,
                    "fallback_reason": reason,
                    "final_error": str(e)
                }
            }
    
    def _create_fallback_enhanced_result(self, standard_results: Dict, error_message: str) -> Dict[str, Any]:
        """Create a fallback enhanced result when enhancement fails."""
        fallback_result = standard_results.copy()
        fallback_result["_enhancement_metadata"] = {
            "enhanced": False,
            "enhancement_attempted": True,
            "enhancement_error": error_message,
            "fallback_used": True
        }
        return fallback_result
    
    def _validate_enhanced_results(self, enhanced_results: Dict) -> bool:
        """Validate that enhanced results have expected structure."""
        try:
            # Check basic structure
            if not isinstance(enhanced_results, dict):
                logger.warning("Enhanced results is not a dictionary")
                return False
            
            # Check for critical errors
            if enhanced_results.get("status") == "error_fallback":
                logger.warning("Enhanced results indicate error fallback")
                return False
            
            # Check if results have meaningful content
            if "enhanced_data" not in enhanced_results and "original_results" not in enhanced_results:
                logger.warning("Enhanced results missing expected data keys")
                return False
            
            # Validate data size (prevent massive results)
            result_size = len(str(enhanced_results))
            if result_size > 10000000:  # 10MB limit
                logger.warning(f"Enhanced results too large: {result_size} chars")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Result validation failed: {e}")
            return False
    
    def _ensure_backward_compatibility(self, enhanced_results: Dict) -> Dict[str, Any]:
        """Ensure enhanced results are backward compatible with original Phase 1 format."""
        try:
            # If enhanced_data contains original format, use it
            if "enhanced_data" in enhanced_results:
                enhanced_data = enhanced_results["enhanced_data"]
                if isinstance(enhanced_data, dict) and "architects" in enhanced_data:
                    # This looks like original Phase 1 format, enhance it
                    enhanced_data["_context_engineering"] = enhanced_results.get("context_engineering", {})
                    enhanced_data["_enhancement_metadata"] = {
                        "enhanced": True,
                        "enhancement_level": enhanced_results.get("enhancement_level", "unknown")
                    }
                    return enhanced_data
            
            # If original_results is available, use it as base
            if "original_results" in enhanced_results:
                base_results = enhanced_results["original_results"].copy()
                base_results["_context_engineering"] = enhanced_results.get("context_engineering", {})
                base_results["_enhancement_metadata"] = {
                    "enhanced": True,
                    "enhancement_level": enhanced_results.get("enhancement_level", "unknown")
                }
                return base_results
            
            # Otherwise, try to extract compatible format
            logger.warning("Enhanced results do not match expected format, attempting extraction")
            return self._extract_compatible_format(enhanced_results)
            
        except Exception as e:
            logger.error(f"Backward compatibility processing failed: {e}")
            # Return enhanced results as-is with warning
            enhanced_results["_compatibility_warning"] = f"Backward compatibility processing failed: {e}"
            return enhanced_results
    
    def _extract_compatible_format(self, enhanced_results: Dict) -> Dict[str, Any]:
        """Extract compatible format from non-standard enhanced results."""
        try:
            # Create minimal compatible structure
            compatible_results = {
                "architects": {},
                "metadata": enhanced_results.get("metadata", {}),
                "_context_engineering": enhanced_results.get("context_engineering", {}),
                "_enhancement_metadata": {
                    "enhanced": True,
                    "format_extraction": True,
                    "original_format": "non_standard"
                },
                "_original_enhanced_results": enhanced_results  # Preserve original
            }
            
            # Try to extract architect-like data
            if "enhanced_data" in enhanced_results:
                enhanced_data = enhanced_results["enhanced_data"]
                if isinstance(enhanced_data, dict):
                    compatible_results["architects"]["enhanced_architect"] = {
                        "analysis": enhanced_data,
                        "source": "context_engineering_extraction"
                    }
            
            return compatible_results
            
        except Exception as e:
            logger.error(f"Compatible format extraction failed: {e}")
            # Return minimal error structure
            return {
                "error": f"Failed to extract compatible format: {e}",
                "_original_enhanced_results": enhanced_results,
                "_enhancement_metadata": {
                    "enhanced": False,
                    "extraction_failed": True
                }
            }
    
    def _update_performance_metrics(self, success: bool, processing_time: float):
        """Update performance tracking metrics."""
        try:
            if success:
                self.performance_metrics["enhancement_successes"] += 1
                
                # Update average processing time
                current_avg = self.performance_metrics["average_enhancement_time"]
                success_count = self.performance_metrics["enhancement_successes"]
                self.performance_metrics["average_enhancement_time"] = (
                    (current_avg * (success_count - 1) + processing_time) / success_count
                )
            
            # Log performance periodically
            if self.performance_metrics["enhancement_attempts"] % 10 == 0:
                success_rate = (self.performance_metrics["enhancement_successes"] / 
                              self.performance_metrics["enhancement_attempts"])
                logger.info(f"Enhanced Phase 1 performance: {success_rate:.2%} success rate, "
                          f"{self.performance_metrics['average_enhancement_time']:.2f}s avg time")
                
        except Exception as e:
            logger.warning(f"Performance metrics update failed: {e}")
    
    def get_enhancement_status(self) -> Dict[str, Any]:
        """Get current enhancement status and performance metrics."""
        return {
            "context_engineering_available": self.context_engineering_available,
            "enhancement_enabled": self.enhancement_enabled,
            "integration_manager_healthy": (
                self.integration_manager.get_system_health() 
                if hasattr(self.integration_manager, 'get_system_health') and self.integration_manager 
                else {"status": "unavailable"}
            ),
            "performance_metrics": self.performance_metrics,
            "configuration": (
                {
                    "optimization_mode": self.integration_config.optimization_mode,
                    "error_tolerance": self.integration_config.error_tolerance_level,
                    "max_processing_time": self.integration_config.max_processing_time
                }
                if hasattr(self, 'integration_config') 
                else {"status": "not_configured"}
            )
        }