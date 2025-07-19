"""
Comprehensive tests for Protocol Engine and Phase 2 Protocol Integration.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime

from core.protocol.protocol_engine import (
    ProtocolEngine, ProtocolType, ProtocolScope, ParticipantRole, 
    CollaborationMode, Participant, ProtocolDefinition
)
from core.protocol.phase2_protocol_integration import Phase2ProtocolIntegration


class TestProtocolEngine(unittest.TestCase):
    """Test the core Protocol Engine functionality."""

    def setUp(self):
        """Set up test environment."""
        self.test_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.test_file.close()
        self.protocol_engine = ProtocolEngine(self.test_file.name)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)

    def test_protocol_engine_initialization(self):
        """Test protocol engine initializes correctly."""
        self.assertIsInstance(self.protocol_engine, ProtocolEngine)
        self.assertEqual(self.protocol_engine.storage_path, self.test_file.name)
        self.assertIsInstance(self.protocol_engine.protocols, dict)
        self.assertIsInstance(self.protocol_engine.audit_log, list)

    def test_context_clarification(self):
        """Test protocol context clarification."""
        context = {
            "protocol_name": "Test Data Analysis Protocol",
            "purpose": "Analyze project data systematically",
            "domain": "technical",
            "scope": "pilot",
            "participants": [
                {"id": "analyst1", "role": "initiator", "expertise": "data_analysis"},
                {"id": "reviewer1", "role": "reviewer", "expertise": "quality_assurance"}
            ]
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        
        self.assertIsInstance(clarified, dict)
        self.assertEqual(clarified["protocol_name"], "Test Data Analysis Protocol")
        self.assertEqual(clarified["purpose"], "Analyze project data systematically")
        self.assertEqual(len(clarified["participants"]), 2)
        self.assertIsInstance(clarified["open_questions"], list)

    def test_ideation_phase(self):
        """Test protocol ideation functionality."""
        context = {
            "protocol_name": "Code Review Protocol",
            "purpose": "Systematic code review process",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified, ["requirements", "strategies", "tools"])
        
        self.assertIsInstance(ideation, dict)
        self.assertIn("idea_pool", ideation)
        self.assertIn("thematic_clusters", ideation)
        self.assertTrue(len(ideation["idea_pool"]) > 0)

    def test_workflow_mapping(self):
        """Test workflow mapping functionality."""
        context = {
            "protocol_name": "Testing Protocol",
            "purpose": "Comprehensive testing strategy",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        
        self.assertIsInstance(workflow, dict)
        self.assertIn("phases", workflow)
        self.assertIn("dependencies", workflow)
        self.assertIn("critical_path", workflow)
        self.assertTrue(len(workflow["phases"]) > 0)

    def test_protocol_drafting(self):
        """Test protocol draft creation."""
        context = {
            "protocol_name": "API Design Protocol",
            "purpose": "Design RESTful APIs",
            "domain": "technical",
            "scope": "standard"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        draft = self.protocol_engine.draft_protocol(clarified, workflow)
        
        self.assertIsInstance(draft, dict)
        self.assertIn("protocol_definition", draft)
        self.assertIn("protocol_steps", draft)
        self.assertIn("outstanding_issues", draft)
        
        # Verify protocol was stored
        protocol_name = context["protocol_name"]
        self.assertIn(protocol_name, self.protocol_engine.protocols)

    def test_protocol_revision(self):
        """Test protocol revision functionality."""
        # First create a protocol
        context = {
            "protocol_name": "Deployment Protocol",
            "purpose": "Deploy applications safely",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        self.protocol_engine.draft_protocol(clarified, workflow)
        
        # Now revise it
        changes = {
            "purpose": "Deploy applications safely with zero downtime",
            "metadata": {"deployment_type": "blue_green"}
        }
        
        revision_result = self.protocol_engine.revision(
            protocol_name="Deployment Protocol",
            changes=changes,
            author="devops_engineer",
            rationale="Added zero downtime requirement"
        )
        
        self.assertIsInstance(revision_result, dict)
        self.assertIn("new_version", revision_result)
        self.assertIn("changes_applied", revision_result)
        
        # Verify revision was stored
        self.assertIn("Deployment Protocol", self.protocol_engine.revisions)

    def test_protocol_forking(self):
        """Test protocol forking functionality."""
        # Create a base protocol
        context = {
            "protocol_name": "Security Audit Protocol",
            "purpose": "Audit application security",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        self.protocol_engine.draft_protocol(clarified, workflow)
        
        # Fork the protocol
        branch_id = self.protocol_engine.fork_protocol(
            protocol_name="Security Audit Protocol",
            branch_name="mobile_security",
            created_by="mobile_security_expert",
            purpose="Mobile-specific security audit"
        )
        
        self.assertIsInstance(branch_id, str)
        self.assertIn(branch_id, self.protocol_engine.branches)
        
        # Verify branch protocol was created
        branch_protocol_name = "Security Audit Protocol_mobile_security"
        self.assertIn(branch_protocol_name, self.protocol_engine.protocols)

    def test_protocol_merging(self):
        """Test protocol merging functionality."""
        # Create base protocol and fork
        context = {
            "protocol_name": "Performance Testing Protocol",
            "purpose": "Test application performance",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        self.protocol_engine.draft_protocol(clarified, workflow)
        
        # Fork it
        branch_id = self.protocol_engine.fork_protocol(
            protocol_name="Performance Testing Protocol",
            branch_name="load_testing",
            created_by="performance_engineer",
            purpose="Load testing specific approach"
        )
        
        # Merge it back
        merge_result = self.protocol_engine.merge_protocol(
            source_branch_id=branch_id,
            target_protocol_name="Performance Testing Protocol",
            merged_by="tech_lead"
        )
        
        self.assertIsInstance(merge_result, dict)
        self.assertIn("merge_id", merge_result)
        self.assertIn("new_version", merge_result)
        
        # Verify merge was recorded
        merge_id = merge_result["merge_id"]
        self.assertIn(merge_id, self.protocol_engine.merges)

    def test_protocol_evolution_tracking(self):
        """Test protocol evolution tracking."""
        # Create and evolve a protocol
        protocol_name = "Code Quality Protocol"
        context = {
            "protocol_name": protocol_name,
            "purpose": "Maintain code quality standards",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        self.protocol_engine.draft_protocol(clarified, workflow)
        
        # Make some revisions
        self.protocol_engine.revision(
            protocol_name,
            {"purpose": "Maintain high code quality standards"},
            "developer1",
            "Improved clarity"
        )
        
        # Fork and merge
        branch_id = self.protocol_engine.fork_protocol(
            protocol_name, "strict_quality", "qa_lead", "Stricter quality standards"
        )
        
        self.protocol_engine.merge_protocol(
            branch_id, protocol_name, "tech_lead"
        )
        
        # Get evolution
        evolution = self.protocol_engine.get_protocol_evolution(protocol_name)
        
        self.assertIsInstance(evolution, dict)
        self.assertIn("revisions", evolution)
        self.assertIn("branches", evolution)
        self.assertIn("merges", evolution)
        self.assertIn("evolution_diagram", evolution)

    def test_decision_logging(self):
        """Test decision and audit logging."""
        # Perform various protocol operations
        context = {
            "protocol_name": "Documentation Protocol",
            "purpose": "Document system architecture",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        self.protocol_engine.draft_protocol(clarified, workflow)
        
        # Get decision log
        decision_log = self.protocol_engine.get_decision_log()
        self.assertIsInstance(decision_log, list)
        self.assertTrue(len(decision_log) > 0)
        
        # Test filtered log
        filtered_log = self.protocol_engine.get_decision_log("Documentation Protocol")
        self.assertIsInstance(filtered_log, list)

    def test_persistence(self):
        """Test protocol engine state persistence."""
        # Create a protocol
        context = {
            "protocol_name": "Persistence Test Protocol",
            "purpose": "Test persistence functionality",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        self.protocol_engine.draft_protocol(clarified, workflow)
        
        # Save state
        self.protocol_engine.save_state()
        
        # Create new engine instance and load state
        new_engine = ProtocolEngine(self.test_file.name)
        
        # Verify protocol exists in new instance
        self.assertIn("Persistence Test Protocol", new_engine.protocols)


class TestPhase2ProtocolIntegration(unittest.TestCase):
    """Test the Phase 2 Protocol Integration layer."""

    def setUp(self):
        """Set up test environment."""
        self.test_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.test_file.close()
        self.integration = Phase2ProtocolIntegration(self.test_file.name)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)

    def test_analysis_protocol_creation(self):
        """Test creation of analysis protocols."""
        project_context = {
            "name": "E-commerce Platform",
            "type": "web_application",
            "technologies": ["React", "Node.js", "PostgreSQL"]
        }
        
        stakeholders = [
            {"role": "initiator", "expertise": "frontend_development"},
            {"role": "reviewer", "expertise": "backend_architecture"},
            {"role": "contributor", "expertise": "database_design"}
        ]
        
        protocol_name = self.integration.create_analysis_protocol(
            project_context, stakeholders
        )
        
        self.assertIsInstance(protocol_name, str)
        self.assertIn("analysis_protocol", protocol_name)
        self.assertIsNotNone(self.integration.current_analysis_protocol)

    def test_analysis_strategy_retrieval(self):
        """Test analysis strategy retrieval."""
        # Create an analysis protocol first
        project_context = {
            "name": "Mobile App",
            "type": "mobile_application",
            "technologies": ["React Native", "Firebase"]
        }
        
        protocol_name = self.integration.create_analysis_protocol(
            project_context, []
        )
        
        # Get analysis strategy
        strategy = self.integration.get_analysis_strategy(
            protocol_name, ["React Native", "Firebase", "JavaScript"]
        )
        
        self.assertIsInstance(strategy, dict)
        self.assertIn("protocol_name", strategy)
        self.assertIn("technology_focus", strategy)
        self.assertIn("analysis_phases", strategy)
        self.assertIn("risk_factors", strategy)

    def test_protocol_revision_workflow(self):
        """Test protocol revision workflow."""
        # Create protocol
        project_context = {
            "name": "Data Pipeline",
            "type": "data_science",
            "technologies": ["Python", "Apache Airflow", "PostgreSQL"]
        }
        
        protocol_name = self.integration.create_analysis_protocol(
            project_context, []
        )
        
        # Propose revision
        revision_result = self.integration.propose_analysis_revision(
            protocol_name=protocol_name,
            revision_type="scope",
            changes={"scope": "broad", "timeline": "extended"},
            proposer="data_engineer",
            rationale="Need more comprehensive analysis for complex pipeline"
        )
        
        self.assertIsInstance(revision_result, dict)
        self.assertIn("new_version", revision_result)
        self.assertIn("phase2_validation", revision_result)

    def test_analysis_approach_forking(self):
        """Test forking of analysis approaches."""
        # Create base protocol
        project_context = {
            "name": "Microservices System",
            "type": "distributed_system",
            "technologies": ["Docker", "Kubernetes", "Go"]
        }
        
        protocol_name = self.integration.create_analysis_protocol(
            project_context, []
        )
        
        # Fork for alternative approach
        branch_id = self.integration.fork_analysis_approach(
            protocol_name=protocol_name,
            alternative_name="security_focused",
            forked_by="security_architect",
            alternative_purpose="Security-first analysis approach"
        )
        
        self.assertIsInstance(branch_id, str)

    def test_analysis_approach_merging(self):
        """Test merging of analysis approaches."""
        # Create and fork protocol
        project_context = {
            "name": "API Gateway",
            "type": "infrastructure",
            "technologies": ["Kong", "Redis", "MongoDB"]
        }
        
        protocol_name = self.integration.create_analysis_protocol(
            project_context, []
        )
        
        branch_id = self.integration.fork_analysis_approach(
            protocol_name, "performance_focused", "performance_engineer",
            "Performance-optimized analysis"
        )
        
        # Merge approaches
        merge_result = self.integration.merge_analysis_approaches(
            source_branch_id=branch_id,
            target_protocol_name=protocol_name,
            merged_by="technical_lead"
        )
        
        self.assertIsInstance(merge_result, dict)
        self.assertIn("merge_id", merge_result)
        self.assertIn("analysis_validation", merge_result)

    def test_protocol_evolution_reporting(self):
        """Test protocol evolution reporting."""
        # Create and evolve a protocol
        project_context = {
            "name": "Machine Learning Pipeline",
            "type": "ml_system",
            "technologies": ["TensorFlow", "Kubeflow", "GCS"]
        }
        
        protocol_name = self.integration.create_analysis_protocol(
            project_context, []
        )
        
        # Make some changes
        self.integration.propose_analysis_revision(
            protocol_name, "strategy", {"focus": "model_performance"},
            "ml_engineer", "Focus on model performance"
        )
        
        # Get evolution
        evolution = self.integration.get_protocol_evolution_for_project(protocol_name)
        
        self.assertIsInstance(evolution, dict)
        self.assertIn("current_analysis_version", evolution)
        self.assertIn("analysis_iterations", evolution)
        self.assertIn("evolution_summary", evolution)

    def test_phase2_report_generation(self):
        """Test Phase 2 report generation."""
        # Create comprehensive protocol
        project_context = {
            "name": "E-learning Platform",
            "type": "web_application",
            "technologies": ["Vue.js", "Laravel", "MySQL"]
        }
        
        stakeholders = [
            {"role": "initiator", "expertise": "education_technology"},
            {"role": "contributor", "expertise": "web_development"}
        ]
        
        protocol_name = self.integration.create_analysis_protocol(
            project_context, stakeholders
        )
        
        # Generate report
        report = self.integration.generate_phase2_report(protocol_name)
        
        self.assertIsInstance(report, dict)
        self.assertIn("protocol_overview", report)
        self.assertIn("analysis_strategy", report)
        self.assertIn("collaboration_summary", report)
        self.assertIn("recommendations", report)


class TestProtocolEngineEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test environment."""
        self.test_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.test_file.close()
        self.protocol_engine = ProtocolEngine(self.test_file.name)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)

    def test_empty_context_handling(self):
        """Test handling of empty or minimal context."""
        empty_context = {}
        clarified = self.protocol_engine.clarify_context(empty_context)
        
        self.assertIsInstance(clarified, dict)
        self.assertIn("open_questions", clarified)
        self.assertTrue(len(clarified["open_questions"]) > 0)

    def test_invalid_protocol_operations(self):
        """Test operations on invalid or nonexistent protocols."""
        # Test revision of nonexistent protocol
        with self.assertRaises(ValueError):
            self.protocol_engine.revision(
                "nonexistent_protocol", {}, "user", "test"
            )
        
        # Test forking nonexistent protocol
        with self.assertRaises(ValueError):
            self.protocol_engine.fork_protocol(
                "nonexistent_protocol", "branch", "user", "test"
            )
        
        # Test merging with nonexistent protocol
        with self.assertRaises(ValueError):
            self.protocol_engine.merge_protocol(
                "nonexistent_branch", "nonexistent_protocol", "user"
            )

    def test_large_protocol_handling(self):
        """Test handling of protocols with large amounts of data."""
        # Create context with many participants
        large_context = {
            "protocol_name": "Large Team Protocol",
            "purpose": "Coordinate large development team",
            "participants": [
                {"id": f"participant_{i}", "role": "contributor", "expertise": f"skill_{i}"}
                for i in range(50)  # 50 participants
            ]
        }
        
        clarified = self.protocol_engine.clarify_context(large_context)
        self.assertEqual(len(clarified["participants"]), 50)
        
        # Create large ideation
        ideation = self.protocol_engine.ideate(
            clarified, [f"focus_area_{i}" for i in range(20)]
        )
        self.assertIsInstance(ideation, dict)

    def test_concurrent_protocol_operations(self):
        """Test concurrent-like protocol operations."""
        # Create multiple protocols quickly
        protocols = []
        for i in range(5):
            context = {
                "protocol_name": f"Concurrent Protocol {i}",
                "purpose": f"Purpose for protocol {i}",
                "domain": "technical"
            }
            
            clarified = self.protocol_engine.clarify_context(context)
            ideation = self.protocol_engine.ideate(clarified)
            workflow = self.protocol_engine.map_workflow(clarified, ideation)
            self.protocol_engine.draft_protocol(clarified, workflow)
            protocols.append(context["protocol_name"])
        
        # Verify all protocols were created
        for protocol_name in protocols:
            self.assertIn(protocol_name, self.protocol_engine.protocols)

    def test_protocol_state_corruption_recovery(self):
        """Test recovery from corrupted protocol state."""
        # Create a protocol
        context = {
            "protocol_name": "Test Protocol",
            "purpose": "Test recovery",
            "domain": "technical"
        }
        
        clarified = self.protocol_engine.clarify_context(context)
        ideation = self.protocol_engine.ideate(clarified)
        workflow = self.protocol_engine.map_workflow(clarified, ideation)
        self.protocol_engine.draft_protocol(clarified, workflow)
        
        # Simulate corruption by writing invalid JSON
        with open(self.test_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Create new engine instance - should handle corruption gracefully
        new_engine = ProtocolEngine(self.test_file.name)
        self.assertIsInstance(new_engine, ProtocolEngine)
        self.assertEqual(len(new_engine.protocols), 0)  # Should start fresh


def run_protocol_tests():
    """Run all protocol-related tests."""
    print("🔄 Running Protocol Engine Tests...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestProtocolEngine,
        TestPhase2ProtocolIntegration,
        TestProtocolEngineEdgeCases
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_protocol_tests()
    if success:
        print("✅ All Protocol Engine tests passed!")
    else:
        print("❌ Some Protocol Engine tests failed!")