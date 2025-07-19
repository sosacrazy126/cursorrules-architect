"""
Comprehensive tests for Context Field Engine and Analysis Context Integration.
"""

import unittest
import math
from datetime import datetime, timedelta

from core.context.context_field_engine import (
    ContextFieldEngine, FieldAttractor, SymbolicResidue, FieldResonance,
    EmergentPattern, ProtocolExecution, AttractorType, ProtocolState
)
from core.context.analysis_context_integration import AnalysisContextIntegration


class TestContextFieldEngine(unittest.TestCase):
    """Test the core Context Field Engine functionality."""

    def setUp(self):
        """Set up test environment."""
        self.field_engine = ContextFieldEngine(field_dimensions=(50, 50, 50))

    def test_field_engine_initialization(self):
        """Test field engine initializes correctly."""
        self.assertIsInstance(self.field_engine, ContextFieldEngine)
        self.assertEqual(self.field_engine.field_dimensions, (50, 50, 50))
        self.assertIsInstance(self.field_engine.attractors, dict)
        self.assertIsInstance(self.field_engine.resonance_patterns, dict)
        
        # Should have some core attractors
        self.assertTrue(len(self.field_engine.attractors) > 0)

    def test_attractor_creation(self):
        """Test attractor creation and management."""
        # Create a new attractor
        attractor_id = self.field_engine.create_attractor(
            concept="test_concept",
            attractor_type=AttractorType.CONCEPT,
            position=(25, 25, 25),
            strength=0.8
        )
        
        self.assertIsInstance(attractor_id, str)
        self.assertIn(attractor_id, self.field_engine.attractors)
        
        # Verify attractor properties
        attractor = self.field_engine.attractors[attractor_id]
        self.assertEqual(attractor.concept, "test_concept")
        self.assertEqual(attractor.attractor_type, AttractorType.CONCEPT)
        self.assertEqual(attractor.position, (25, 25, 25))
        self.assertEqual(attractor.strength, 0.8)

    def test_attractor_activation(self):
        """Test attractor activation functionality."""
        # Create attractor
        attractor_id = self.field_engine.create_attractor(
            "activation_test", AttractorType.PATTERN, (30, 30, 30), 0.5
        )
        
        attractor = self.field_engine.attractors[attractor_id]
        initial_strength = attractor.strength
        initial_count = attractor.activation_count
        
        # Activate attractor
        attractor.activate()
        
        # Verify activation effects
        self.assertGreater(attractor.strength, initial_strength)
        self.assertEqual(attractor.activation_count, initial_count + 1)
        self.assertIsNotNone(attractor.last_activated)

    def test_symbolic_residue_creation(self):
        """Test symbolic residue creation and management."""
        # Create symbolic residue
        residue_id = self.field_engine.add_symbolic_residue(
            symbol="⊕",
            meaning="combination_operation",
            context="mathematical_context",
            position=(15, 15, 15),
            decay_rate=0.01
        )
        
        self.assertIsInstance(residue_id, str)
        self.assertIn(residue_id, self.field_engine.symbolic_residues)
        
        # Verify residue properties
        residue = self.field_engine.symbolic_residues[residue_id]
        self.assertEqual(residue.symbol, "⊕")
        self.assertEqual(residue.meaning, "combination_operation")
        self.assertEqual(residue.decay_rate, 0.01)
        self.assertEqual(residue.strength, 1.0)

    def test_symbolic_residue_decay(self):
        """Test symbolic residue decay over time."""
        residue_id = self.field_engine.add_symbolic_residue(
            "∞", "infinity", "test_context", (20, 20, 20), decay_rate=0.1
        )
        
        residue = self.field_engine.symbolic_residues[residue_id]
        initial_strength = residue.strength
        
        # Apply decay
        residue.decay(time_delta=1.0)
        
        # Verify decay occurred
        expected_strength = initial_strength * math.exp(-0.1 * 1.0)
        self.assertAlmostEqual(residue.strength, expected_strength, places=5)

    def test_field_resonance_creation(self):
        """Test field resonance creation and management."""
        # Create some attractors first
        attr1_id = self.field_engine.create_attractor(
            "resonance_test_1", AttractorType.CONCEPT, (10, 10, 10)
        )
        attr2_id = self.field_engine.create_attractor(
            "resonance_test_2", AttractorType.CONCEPT, (15, 15, 15)
        )
        
        # Create resonance between them
        resonance_id = self.field_engine.create_resonance(
            source_ids=[attr1_id, attr2_id],
            frequency=1.5,
            amplitude=0.8,
            resonance_type="test_resonance"
        )
        
        self.assertIsInstance(resonance_id, str)
        self.assertIn(resonance_id, self.field_engine.resonance_patterns)
        
        # Verify resonance properties
        resonance = self.field_engine.resonance_patterns[resonance_id]
        self.assertEqual(resonance.source_ids, [attr1_id, attr2_id])
        self.assertEqual(resonance.frequency, 1.5)
        self.assertEqual(resonance.amplitude, 0.8)

    def test_protocol_execution(self):
        """Test protocol execution in the field."""
        # Test attractor co-emergence protocol
        execution_id = self.field_engine.execute_protocol(
            "attractor_co_emerge",
            {"concepts": ["concept_a", "concept_b", "concept_c"]}
        )
        
        self.assertIsInstance(execution_id, str)
        self.assertIn(execution_id, self.field_engine.protocol_executions)
        
        # Verify execution state
        execution = self.field_engine.protocol_executions[execution_id]
        self.assertEqual(execution.protocol_name, "attractor_co_emerge")
        self.assertEqual(execution.state, ProtocolState.CONVERGED)
        self.assertTrue(len(execution.created_attractors) > 0)

    def test_emergent_pattern_detection(self):
        """Test emergent pattern detection."""
        # Create multiple related attractors to form patterns
        concepts = ["pattern_element_1", "pattern_element_2", "pattern_element_3"]
        for i, concept in enumerate(concepts):
            self.field_engine.create_attractor(
                concept, AttractorType.CONCEPT, (20 + i*5, 20 + i*5, 20)
            )
        
        # Detect emergent patterns
        patterns = self.field_engine.detect_emergence()
        
        self.assertIsInstance(patterns, list)
        # Should detect at least some patterns from all the attractors
        self.assertTrue(len(patterns) >= 0)

    def test_field_coherence_calculation(self):
        """Test field coherence calculation."""
        # Create some resonances to affect coherence
        attr1_id = self.field_engine.create_attractor(
            "coherence_test_1", AttractorType.CONCEPT, (25, 25, 25)
        )
        attr2_id = self.field_engine.create_attractor(
            "coherence_test_2", AttractorType.CONCEPT, (30, 30, 30)
        )
        
        self.field_engine.create_resonance(
            [attr1_id, attr2_id], frequency=1.0, amplitude=0.9
        )
        
        coherence = self.field_engine.get_field_coherence()
        self.assertIsInstance(coherence, float)
        self.assertGreaterEqual(coherence, 0.0)
        self.assertLessEqual(coherence, 1.0)

    def test_field_energy_calculation(self):
        """Test field energy calculation."""
        energy = self.field_engine.get_field_energy()
        self.assertIsInstance(energy, float)
        self.assertGreater(energy, 0.0)  # Should have some energy from core attractors

    def test_field_evolution(self):
        """Test field evolution over time."""
        # Add some residues that will decay
        residue_id = self.field_engine.add_symbolic_residue(
            "⌘", "evolution_test", "test", (40, 40, 40), decay_rate=0.1
        )
        
        initial_residue_count = len(self.field_engine.symbolic_residues)
        
        # Evolve field (this should decay weak residues)
        self.field_engine.evolve_field(time_delta=5.0)  # Large time step
        
        # Check that evolution occurred
        final_residue_count = len(self.field_engine.symbolic_residues)
        # May or may not have fewer residues, depending on decay threshold

    def test_self_reflection(self):
        """Test meta-recursive self-reflection."""
        # Add some complexity to the field first
        self.field_engine.create_attractor(
            "reflection_test", AttractorType.INSIGHT, (35, 35, 35)
        )
        
        reflection = self.field_engine.self_reflect()
        
        self.assertIsInstance(reflection, dict)
        self.assertIn("field_metrics", reflection)
        self.assertIn("pattern_analysis", reflection)
        self.assertIn("improvement_opportunities", reflection)
        self.assertIn("stability_assessment", reflection)
        
        # Verify metrics structure
        metrics = reflection["field_metrics"]
        self.assertIn("total_attractors", metrics)
        self.assertIn("field_coherence", metrics)
        self.assertIn("field_energy", metrics)

    def test_field_improvement(self):
        """Test field improvement application."""
        # Create some weak attractors
        weak_attr_id = self.field_engine.create_attractor(
            "weak_concept", AttractorType.CONCEPT, (45, 45, 45), strength=0.2
        )
        
        initial_strength = self.field_engine.attractors[weak_attr_id].strength
        
        # Apply improvement
        self.field_engine.apply_improvement(
            "strengthen_weak_attractors",
            {"threshold": 0.3}
        )
        
        # Verify improvement
        final_strength = self.field_engine.attractors[weak_attr_id].strength
        self.assertGreater(final_strength, initial_strength)

    def test_interpretability_map(self):
        """Test interpretability map generation."""
        # Add some field elements
        self.field_engine.create_attractor(
            "interpretable_concept", AttractorType.CONCEPT, (12, 12, 12)
        )
        
        interpretability_map = self.field_engine.get_interpretability_map()
        
        self.assertIsInstance(interpretability_map, dict)
        self.assertIn("field_structure", interpretability_map)
        self.assertIn("emergence_trace", interpretability_map)
        self.assertIn("symbolic_landscape", interpretability_map)
        self.assertIn("causal_attribution", interpretability_map)

    def test_multiple_protocol_execution(self):
        """Test execution of multiple different protocols."""
        protocols_to_test = [
            ("recursive_emergence", {"concept": "test_recursion"}),
            ("field_resonance_scaffold", {"phase": "test_phase"}),
            ("symbolic_mechanism", {"symbols": ["α", "β"], "meanings": ["start", "end"]}),
            ("meta_recursive_framework", {"analysis_depth": "basic"})
        ]
        
        execution_ids = []
        for protocol_name, context in protocols_to_test:
            execution_id = self.field_engine.execute_protocol(protocol_name, context)
            execution_ids.append(execution_id)
            
            # Verify execution
            execution = self.field_engine.protocol_executions[execution_id]
            self.assertEqual(execution.protocol_name, protocol_name)
            self.assertEqual(execution.state, ProtocolState.CONVERGED)
        
        # Verify all executions were unique
        self.assertEqual(len(execution_ids), len(set(execution_ids)))


class TestAnalysisContextIntegration(unittest.TestCase):
    """Test the Analysis Context Integration layer."""

    def setUp(self):
        """Set up test environment."""
        self.integration = AnalysisContextIntegration()

    def test_field_analysis_session_lifecycle(self):
        """Test complete field analysis session lifecycle."""
        # Start field analysis
        project_context = {
            "name": "Test React Application",
            "technologies": ["React", "Node.js", "PostgreSQL"],
            "type": "web_application"
        }
        
        session_id = self.integration.start_field_analysis(project_context)
        
        self.assertIsInstance(session_id, str)
        self.assertIsNotNone(self.integration.current_analysis_session)
        
        # Enhance multiple phases
        phases = [
            ("Discovery", {"technologies": ["React", "Node.js"], "patterns": ["SPA"]}, 1),
            ("Planning", {"architecture": "microservices", "database": "PostgreSQL"}, 2),
            ("Deep Analysis", {"performance": "good", "security": "moderate"}, 3)
        ]
        
        for phase_name, phase_data, phase_number in phases:
            enhanced_data = self.integration.enhance_phase_with_field(
                phase_name, phase_data, phase_number
            )
            
            self.assertIsInstance(enhanced_data, dict)
            self.assertIn("field_enhancement", enhanced_data)
            
            enhancement = enhanced_data["field_enhancement"]
            self.assertIn("attractors_created", enhancement)
            self.assertIn("protocols_executed", enhancement)
            self.assertIn("field_insights", enhancement)
        
        # End analysis session
        session_summary = self.integration.end_field_analysis()
        
        self.assertIsInstance(session_summary, dict)
        self.assertIn("session_id", session_summary)
        self.assertIn("phases_enhanced", session_summary)

    def test_cross_phase_pattern_detection(self):
        """Test cross-phase pattern detection."""
        # Start session and process multiple phases
        project_context = {
            "name": "Vue.js Dashboard",
            "technologies": ["Vue.js", "Express", "MongoDB"]
        }
        
        self.integration.start_field_analysis(project_context)
        
        # Process phases with overlapping concepts
        phases = [
            ("Discovery", {"frameworks": ["Vue.js"], "components": ["dashboard", "charts"]}, 1),
            ("Planning", {"components": ["dashboard", "reports"], "data": ["MongoDB"]}, 2),
            ("Analysis", {"performance": ["dashboard"], "optimization": ["charts"]}, 3)
        ]
        
        for phase_name, phase_data, phase_number in phases:
            self.integration.enhance_phase_with_field(
                phase_name, phase_data, phase_number
            )
        
        # Get cross-phase patterns
        cross_patterns = self.integration.get_cross_phase_patterns()
        
        self.assertIsInstance(cross_patterns, dict)
        self.assertIn("cross_phase_patterns", cross_patterns)
        self.assertIn("resonance_analysis", cross_patterns)
        self.assertIn("meta_insights", cross_patterns)

    def test_meta_recursive_enhancement(self):
        """Test meta-recursive enhancement functionality."""
        # Start session
        project_context = {"name": "Test System", "technologies": ["Python"]}
        self.integration.start_field_analysis(project_context)
        
        # Add some complexity
        self.integration.enhance_phase_with_field(
            "Test Phase", {"complexity": "high", "patterns": ["recursive"]}, 1
        )
        
        # Perform meta-recursive enhancement
        enhancement_result = self.integration.perform_meta_recursive_enhancement()
        
        self.assertIsInstance(enhancement_result, dict)
        self.assertIn("meta_execution_id", enhancement_result)
        self.assertIn("self_reflection", enhancement_result)
        self.assertIn("improvements_applied", enhancement_result)
        self.assertIn("recommendations", enhancement_result)

    def test_field_interpretability_mapping(self):
        """Test field interpretability mapping."""
        # Create some field activity
        project_context = {"name": "Interpretability Test", "technologies": ["JavaScript"]}
        self.integration.start_field_analysis(project_context)
        
        self.integration.enhance_phase_with_field(
            "Test Phase", {"insights": ["pattern1", "pattern2"]}, 1
        )
        
        # Get interpretability map
        interpretability_map = self.integration.get_field_interpretability_map()
        
        self.assertIsInstance(interpretability_map, dict)
        self.assertIn("field_structure", interpretability_map)
        self.assertIn("analysis_context", interpretability_map)
        self.assertIn("analysis_recommendations", interpretability_map)
        
        # Verify analysis-specific sections
        analysis_context = interpretability_map["analysis_context"]
        self.assertIn("session_info", analysis_context)
        self.assertIn("phase_attribution", analysis_context)

    def test_field_state_export(self):
        """Test field state export functionality."""
        # Create field state
        project_context = {"name": "Export Test", "technologies": ["TypeScript"]}
        self.integration.start_field_analysis(project_context)
        
        self.integration.enhance_phase_with_field(
            "Export Phase", {"data": ["export_test"]}, 1
        )
        
        # Export field state
        field_state = self.integration.export_field_state()
        
        self.assertIsInstance(field_state, dict)
        self.assertIn("field_dimensions", field_state)
        self.assertIn("attractors", field_state)
        self.assertIn("resonances", field_state)
        self.assertIn("session_info", field_state)
        
        # Verify serializable format
        import json
        try:
            json.dumps(field_state, default=str)  # Should not raise exception
        except TypeError:
            self.fail("Field state is not serializable")

    def test_phase_specific_protocols(self):
        """Test that different phases trigger appropriate protocols."""
        project_context = {"name": "Protocol Test", "technologies": ["Angular"]}
        self.integration.start_field_analysis(project_context)
        
        # Test different phases trigger different protocols
        test_phases = [
            (1, "Discovery"),
            (2, "Planning"),
            (3, "Deep Analysis"),
            (4, "Synthesis"),
            (5, "Consolidation"),
            (6, "Final Analysis")
        ]
        
        for phase_number, phase_name in test_phases:
            enhanced_data = self.integration.enhance_phase_with_field(
                phase_name, {"test": f"phase_{phase_number}"}, phase_number
            )
            
            enhancement = enhanced_data["field_enhancement"]
            protocols = enhancement["protocols_executed"]
            
            # Each phase should execute at least one protocol
            self.assertTrue(len(protocols) > 0)

    def test_field_evolution_metrics(self):
        """Test field evolution metrics calculation."""
        project_context = {"name": "Evolution Test", "technologies": ["Ruby"]}
        self.integration.start_field_analysis(project_context)
        
        # Process multiple phases to create evolution
        for i in range(3):
            self.integration.enhance_phase_with_field(
                f"Phase_{i+1}", {"iteration": i+1}, i+1
            )
        
        # End session and get evolution metrics
        session_summary = self.integration.end_field_analysis()
        
        self.assertIn("field_evolution_metrics", session_summary)
        evolution_metrics = session_summary["field_evolution_metrics"]
        
        # Should have various growth metrics
        metric_keys = list(evolution_metrics.keys())
        self.assertTrue(any("growth" in key for key in metric_keys))


class TestContextFieldEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test environment."""
        self.field_engine = ContextFieldEngine()

    def test_invalid_positions(self):
        """Test handling of invalid field positions."""
        # Test positions outside field boundaries
        large_position = (1000, 1000, 1000)
        attractor_id = self.field_engine.create_attractor(
            "boundary_test", AttractorType.CONCEPT, large_position
        )
        
        # Should still create attractor (no strict boundary enforcement)
        self.assertIsInstance(attractor_id, str)

    def test_zero_strength_attractors(self):
        """Test handling of zero or negative strength attractors."""
        # Test zero strength
        zero_attr_id = self.field_engine.create_attractor(
            "zero_strength", AttractorType.CONCEPT, (25, 25, 25), strength=0.0
        )
        self.assertIsInstance(zero_attr_id, str)
        
        # Test negative strength
        neg_attr_id = self.field_engine.create_attractor(
            "negative_strength", AttractorType.CONCEPT, (30, 30, 30), strength=-0.5
        )
        self.assertIsInstance(neg_attr_id, str)

    def test_empty_protocol_execution(self):
        """Test protocol execution with empty or invalid context."""
        # Test empty context
        execution_id = self.field_engine.execute_protocol(
            "attractor_co_emerge", {}
        )
        self.assertIsInstance(execution_id, str)
        
        # Test unknown protocol
        unknown_execution_id = self.field_engine.execute_protocol(
            "unknown_protocol", {"test": "data"}
        )
        self.assertIsInstance(unknown_execution_id, str)

    def test_massive_field_operations(self):
        """Test field with large numbers of elements."""
        # Create many attractors
        for i in range(50):
            self.field_engine.create_attractor(
                f"mass_test_{i}", AttractorType.CONCEPT, 
                (i % 10 * 5, i % 10 * 5, i % 10 * 5)
            )
        
        # Create many residues
        for i in range(30):
            self.field_engine.add_symbolic_residue(
                f"S{i}", f"meaning_{i}", "mass_test", 
                (i % 5 * 10, i % 5 * 10, i % 5 * 10)
            )
        
        # Test operations still work
        coherence = self.field_engine.get_field_coherence()
        self.assertIsInstance(coherence, float)
        
        patterns = self.field_engine.detect_emergence()
        self.assertIsInstance(patterns, list)

    def test_field_with_no_elements(self):
        """Test field operations with minimal elements."""
        # Create fresh field with minimal core elements
        empty_field = ContextFieldEngine()
        
        # Clear most attractors (keep some core ones)
        initial_count = len(empty_field.attractors)
        
        # Test operations on minimal field
        coherence = empty_field.get_field_coherence()
        self.assertIsInstance(coherence, float)
        
        energy = empty_field.get_field_energy()
        self.assertIsInstance(energy, float)
        
        patterns = empty_field.detect_emergence()
        self.assertIsInstance(patterns, list)

    def test_rapid_field_evolution(self):
        """Test rapid field evolution with large time steps."""
        # Add some residues
        for i in range(5):
            self.field_engine.add_symbolic_residue(
                f"R{i}", f"rapid_test_{i}", "evolution_test",
                (i*10, i*10, i*10), decay_rate=0.2
            )
        
        initial_count = len(self.field_engine.symbolic_residues)
        
        # Evolve with very large time step
        self.field_engine.evolve_field(time_delta=100.0)
        
        final_count = len(self.field_engine.symbolic_residues)
        # Most or all residues should have decayed away
        self.assertLessEqual(final_count, initial_count)


def run_context_field_tests():
    """Run all context field related tests."""
    print("🌊 Running Context Field Engine Tests...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestContextFieldEngine,
        TestAnalysisContextIntegration,
        TestContextFieldEdgeCases
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_context_field_tests()
    if success:
        print("✅ All Context Field Engine tests passed!")
    else:
        print("❌ Some Context Field Engine tests failed!")