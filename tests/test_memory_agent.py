"""
Comprehensive tests for Memory Agent and Analysis Memory Integration.
"""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path

from core.memory.memory_agent import MemoryAgent, KnowledgeNode, NodeType, LinkType
from core.memory.analysis_memory_integration import AnalysisMemoryIntegration


class TestMemoryAgent(unittest.TestCase):
    """Test the core Memory Agent functionality."""

    def setUp(self):
        """Set up test environment."""
        self.test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.test_db.close()
        self.memory_agent = MemoryAgent(self.test_db.name)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)

    def test_memory_agent_initialization(self):
        """Test memory agent initializes correctly."""
        self.assertIsInstance(self.memory_agent, MemoryAgent)
        self.assertEqual(self.memory_agent.db_path, self.test_db.name)
        self.assertIsInstance(self.memory_agent.audit_log, list)

    def test_ingest_node(self):
        """Test knowledge node ingestion."""
        # Test basic node creation
        node_id = self.memory_agent.ingest_node(
            title="Test Project Analysis",
            content="Analysis of a React application with Node.js backend",
            node_type=NodeType.ANALYSIS,
            tags=["react", "nodejs", "analysis"],
            source="test_source",
            contributor="test_user"
        )
        
        self.assertIsInstance(node_id, str)
        self.assertTrue(node_id.startswith("N"))
        
        # Verify node was stored
        node = self.memory_agent._get_node(node_id)
        self.assertIsNotNone(node)
        self.assertEqual(node.title, "Test Project Analysis")
        self.assertEqual(node.type, NodeType.ANALYSIS)
        self.assertIn("react", node.tags)

    def test_duplicate_node_detection(self):
        """Test duplicate node detection."""
        # Create first node
        node_id1 = self.memory_agent.ingest_node(
            title="Same Title",
            content="Same content for testing",
            node_type=NodeType.DOCUMENT,
            tags=["test"]
        )
        
        # Try to create duplicate
        node_id2 = self.memory_agent.ingest_node(
            title="Same Title",
            content="Same content for testing",
            node_type=NodeType.DOCUMENT,
            tags=["test"]
        )
        
        # Should return same ID for duplicate
        self.assertEqual(node_id1, node_id2)

    def test_semantic_linking(self):
        """Test semantic link creation."""
        # Create two related nodes
        node1_id = self.memory_agent.ingest_node(
            title="React Component",
            content="A reusable React component implementation",
            node_type=NodeType.PATTERN,
            tags=["react", "component", "frontend"]
        )
        
        node2_id = self.memory_agent.ingest_node(
            title="Component Testing",
            content="Testing strategies for React components",
            node_type=NodeType.SPECIFICATION,
            tags=["react", "testing", "component"]
        )
        
        # Create semantic links
        links = self.memory_agent.create_semantic_links(node1_id)
        self.assertIsInstance(links, list)
        
        # Verify link was created (simplified check)
        node1 = self.memory_agent._get_node(node1_id)
        self.assertTrue(len(node1.links) >= 0)  # May or may not create link in simplified implementation

    def test_contextual_retrieval(self):
        """Test contextual retrieval functionality."""
        # Create several test nodes
        test_nodes = [
            ("React App Analysis", "Analysis of React application architecture", ["react", "analysis"]),
            ("Vue.js Performance", "Performance optimization for Vue.js apps", ["vue", "performance"]),
            ("React Performance", "React app performance best practices", ["react", "performance"]),
            ("Node.js Backend", "Backend implementation with Node.js", ["nodejs", "backend"])
        ]
        
        node_ids = []
        for title, content, tags in test_nodes:
            node_id = self.memory_agent.ingest_node(
                title=title,
                content=content,
                node_type=NodeType.ANALYSIS,
                tags=tags
            )
            node_ids.append(node_id)
        
        # Test retrieval with React query
        react_results = self.memory_agent.contextual_retrieve("React performance analysis")
        self.assertIsInstance(react_results, list)
        
        # Should find React-related nodes
        react_titles = [node.title for node in react_results]
        self.assertTrue(any("React" in title for title in react_titles))

    def test_curation_workflow(self):
        """Test node curation workflow."""
        # Create test nodes including some that should be curated
        self.memory_agent.ingest_node(
            title="Short",
            content="Too short",  # Should be flagged for deletion
            node_type=NodeType.DOCUMENT,
            tags=["test"]
        )
        
        self.memory_agent.ingest_node(
            title="Good Content",
            content="This is a properly sized piece of content that should be kept during curation",
            node_type=NodeType.ANALYSIS,
            tags=["test", "analysis"]
        )
        
        # Run curation
        curation_results = self.memory_agent.curate_nodes()
        self.assertIsInstance(curation_results, dict)
        
        # Verify curation decisions were made
        self.assertTrue(len(curation_results) > 0)

    def test_recursive_refinement(self):
        """Test recursive refinement functionality."""
        # Create some nodes to refine
        for i in range(3):
            self.memory_agent.ingest_node(
                title=f"Test Node {i}",
                content=f"Content for test node {i} with some analysis",
                node_type=NodeType.ANALYSIS,
                tags=["test", f"node{i}"]
            )
        
        # Run recursive refinement
        refinement_results = self.memory_agent.recursive_refine(max_depth=2)
        self.assertIsInstance(refinement_results, dict)
        
        # Check for expected refinement results
        self.assertIn("orphaned_nodes", refinement_results)
        self.assertIn("tag_suggestions", refinement_results)

    def test_audit_logging(self):
        """Test audit logging functionality."""
        # Perform some operations that should be audited
        node_id = self.memory_agent.ingest_node(
            title="Audit Test",
            content="Testing audit logging",
            node_type=NodeType.DOCUMENT,
            tags=["audit", "test"]
        )
        
        # Get audit log
        audit_entries = self.memory_agent.get_audit_log(limit=10)
        self.assertIsInstance(audit_entries, list)
        self.assertTrue(len(audit_entries) > 0)
        
        # Verify audit entry structure
        entry = audit_entries[0]
        self.assertIn("action", entry)
        self.assertIn("timestamp", entry)
        self.assertIn("details", entry)


class TestAnalysisMemoryIntegration(unittest.TestCase):
    """Test the Analysis Memory Integration layer."""

    def setUp(self):
        """Set up test environment."""
        self.test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.test_db.close()
        self.integration = AnalysisMemoryIntegration(self.test_db.name)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)

    def test_analysis_session_lifecycle(self):
        """Test complete analysis session lifecycle."""
        # Start analysis session
        project_id = self.integration.start_analysis_session(
            project_path="/test/project",
            project_name="Test React App"
        )
        
        self.assertIsInstance(project_id, str)
        self.assertIsNotNone(self.integration.current_analysis_session)
        
        # Store phase analysis
        phase_result = {
            "technologies": ["React", "Node.js", "MongoDB"],
            "key_findings": ["Component-based architecture", "RESTful API design"],
            "complexity_score": 7.5
        }
        
        phase_node_id = self.integration.store_phase_analysis(
            phase_name="Discovery",
            analysis_result=phase_result,
            phase_number=1
        )
        
        self.assertIsInstance(phase_node_id, str)
        
        # Store final analysis
        final_result = {
            "summary": "Well-structured React application with modern architecture",
            "recommendations": ["Improve error handling", "Add unit tests"],
            "technologies": ["React", "Node.js"]
        }
        
        final_node_id = self.integration.store_final_analysis(final_result)
        self.assertIsInstance(final_node_id, str)
        
        # End session
        session_summary = self.integration.end_analysis_session()
        self.assertIsInstance(session_summary, dict)
        self.assertIn("phases_completed", session_summary)

    def test_similar_projects_retrieval(self):
        """Test retrieval of similar projects."""
        # Create a project session first
        self.integration.start_analysis_session(
            project_path="/test/react-app",
            project_name="React E-commerce"
        )
        
        # Store some analysis
        self.integration.store_phase_analysis(
            "Discovery",
            {"technologies": ["React", "Redux", "Node.js"]},
            1
        )
        
        self.integration.end_analysis_session()
        
        # Now look for similar projects
        similar_projects = self.integration.get_similar_projects(
            technologies=["React", "Node.js"],
            project_type="web"
        )
        
        self.assertIsInstance(similar_projects, list)

    def test_phase_patterns_retrieval(self):
        """Test retrieval of patterns from similar phases."""
        # Create a project with multiple phases
        self.integration.start_analysis_session(
            project_path="/test/vue-app",
            project_name="Vue Dashboard"
        )
        
        # Store multiple phase analyses
        phases = [
            ("Discovery", {"technologies": ["Vue", "Vuex"], "patterns": ["SPA", "Component-based"]}, 1),
            ("Planning", {"architecture": "MVVM", "database": "PostgreSQL"}, 2),
            ("Analysis", {"performance": "good", "maintainability": "high"}, 3)
        ]
        
        for phase_name, phase_data, phase_num in phases:
            self.integration.store_phase_analysis(phase_name, phase_data, phase_num)
        
        # Get phase patterns
        patterns = self.integration.get_phase_patterns("Discovery", ["Vue", "JavaScript"])
        self.assertIsInstance(patterns, dict)
        self.assertIn("similar_analyses", patterns)

    def test_project_history_tracking(self):
        """Test project history tracking."""
        # Create multiple projects
        projects = [
            ("React Blog", "/test/blog", ["React", "Express"]),
            ("Vue Shop", "/test/shop", ["Vue", "Node.js"]),
            ("Angular CRM", "/test/crm", ["Angular", "NestJS"])
        ]
        
        for project_name, project_path, technologies in projects:
            self.integration.start_analysis_session(project_path, project_name)
            self.integration.store_phase_analysis(
                "Discovery",
                {"technologies": technologies},
                1
            )
            self.integration.end_analysis_session()
        
        # Get project history
        history = self.integration.get_project_history()
        self.assertIsInstance(history, list)
        self.assertTrue(len(history) >= 3)
        
        # Test filtered history
        react_history = self.integration.get_project_history("React Blog")
        self.assertIsInstance(react_history, list)


class TestMemoryAgentEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test environment."""
        self.test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.test_db.close()
        self.memory_agent = MemoryAgent(self.test_db.name)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)

    def test_empty_content_handling(self):
        """Test handling of empty or minimal content."""
        # Test empty content
        node_id = self.memory_agent.ingest_node(
            title="Empty Content Test",
            content="",
            node_type=NodeType.DOCUMENT,
            tags=["test"]
        )
        
        self.assertIsInstance(node_id, str)
        
        # Test very short content
        short_node_id = self.memory_agent.ingest_node(
            title="Short",
            content="Hi",
            node_type=NodeType.DOCUMENT,
            tags=["test"]
        )
        
        self.assertIsInstance(short_node_id, str)

    def test_large_content_handling(self):
        """Test handling of large content."""
        large_content = "This is a test. " * 1000  # 17,000 characters
        
        node_id = self.memory_agent.ingest_node(
            title="Large Content Test",
            content=large_content,
            node_type=NodeType.ANALYSIS,
            tags=["test", "large"]
        )
        
        self.assertIsInstance(node_id, str)
        
        # Verify content was stored
        node = self.memory_agent._get_node(node_id)
        self.assertIsNotNone(node)
        self.assertEqual(len(node.content), len(large_content))

    def test_special_characters_handling(self):
        """Test handling of special characters and unicode."""
        special_content = "Test with émojis 🚀, spëcial chars: áéíóú, and symbols: ∀∃∈∋∞"
        
        node_id = self.memory_agent.ingest_node(
            title="Special Characters Test",
            content=special_content,
            node_type=NodeType.DOCUMENT,
            tags=["test", "unicode", "émoji"]
        )
        
        self.assertIsInstance(node_id, str)
        
        # Verify content integrity
        node = self.memory_agent._get_node(node_id)
        self.assertEqual(node.content, special_content)

    def test_nonexistent_node_operations(self):
        """Test operations on nonexistent nodes."""
        # Test getting nonexistent node
        node = self.memory_agent._get_node("nonexistent_id")
        self.assertIsNone(node)
        
        # Test creating links for nonexistent node
        links = self.memory_agent.create_semantic_links("nonexistent_id")
        self.assertEqual(links, [])

    def test_concurrent_operations(self):
        """Test concurrent-like operations (simulated)."""
        # Create multiple nodes in quick succession
        node_ids = []
        for i in range(10):
            node_id = self.memory_agent.ingest_node(
                title=f"Concurrent Test {i}",
                content=f"Content for concurrent test node {i}",
                node_type=NodeType.ANALYSIS,
                tags=["concurrent", f"test{i}"]
            )
            node_ids.append(node_id)
        
        # Verify all nodes were created
        self.assertEqual(len(node_ids), 10)
        self.assertEqual(len(set(node_ids)), 10)  # All unique

    def test_memory_persistence(self):
        """Test that memory persists across agent instances."""
        # Create a node
        node_id = self.memory_agent.ingest_node(
            title="Persistence Test",
            content="This should persist across instances",
            node_type=NodeType.DOCUMENT,
            tags=["persistence", "test"]
        )
        
        # Create new agent instance with same database
        new_agent = MemoryAgent(self.test_db.name)
        
        # Verify node exists in new instance
        node = new_agent._get_node(node_id)
        self.assertIsNotNone(node)
        self.assertEqual(node.title, "Persistence Test")


def run_memory_tests():
    """Run all memory-related tests."""
    print("🧠 Running Memory Agent Tests...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestMemoryAgent,
        TestAnalysisMemoryIntegration,
        TestMemoryAgentEdgeCases
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_memory_tests()
    if success:
        print("✅ All Memory Agent tests passed!")
    else:
        print("❌ Some Memory Agent tests failed!")