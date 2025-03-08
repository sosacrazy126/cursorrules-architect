#!/usr/bin/env python3
"""
tests/phase_2/parser.py

This module provides testing functionality for the Phase 2 output parser.
It verifies that the agent_parser correctly handles the XML format where
<reasoning> and <analysis_plan> tags are separate.

This test module helps ensure that the Phase 3 analysis can properly access
the agent assignments created in Phase 2.
"""

import os
import sys
import unittest
from pathlib import Path

# Add the project root to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.tools.agent_parser import (
    parse_agents_from_phase2,
    get_agent_file_mapping,
    get_all_file_assignments,
    create_xml_from_phase2_output
)

class TestPhase2Parser(unittest.TestCase):
    """Test case for the Phase 2 output parser functionality."""
    
    def setUp(self):
        """Set up test case by loading the test document."""
        # Get the path to the test document relative to this file
        self.test_doc_path = Path(__file__).parent / "test_doc.md"
        # Load the test document
        with open(self.test_doc_path, 'r', encoding='utf-8') as f:
            self.test_content = f.read()
    
    def test_create_xml_from_phase2_output(self):
        """Test that create_xml_from_phase2_output correctly handles the output format."""
        # Call the function
        result = create_xml_from_phase2_output(self.test_content)
        
        # Check that it returns a string
        self.assertIsInstance(result, str)
        
        # Check that the result includes an analysis_plan tag
        self.assertIn("<analysis_plan>", result)
        self.assertIn("</analysis_plan>", result)
        
        # Check that it contains agent tags
        self.assertIn("<agent_1", result)
        self.assertIn("<agent_2", result)
        self.assertIn("<agent_3", result)
    
    def test_parse_agents_from_phase2(self):
        """Test that parse_agents_from_phase2 correctly parses the agent definitions."""
        # Call the function
        agents = parse_agents_from_phase2(self.test_content)
        
        # Check that it returns a list
        self.assertIsInstance(agents, list)
        
        # Check that there are 3 agents
        self.assertEqual(len(agents), 3)
        
        # Check the first agent
        agent1 = agents[0]
        self.assertEqual(agent1["id"], "agent_1")
        self.assertEqual(agent1["name"], "Project Structure and Utilities")
        self.assertIn("core structural elements", agent1["description"])
        
        # Check that the agent has file assignments
        self.assertTrue(len(agent1["file_assignments"]) > 0)
        self.assertIn("main.py", agent1["file_assignments"])
        
        # Check the second agent
        agent2 = agents[1]
        self.assertEqual(agent2["id"], "agent_2")
        self.assertEqual(agent2["name"], "LLM Integration")
        
        # Check the third agent
        agent3 = agents[2]
        self.assertEqual(agent3["id"], "agent_3")
        self.assertEqual(agent3["name"], "Configuration and Documentation")
    
    def test_get_agent_file_mapping(self):
        """Test that get_agent_file_mapping correctly maps agents to files."""
        # Call the function
        mapping = get_agent_file_mapping(self.test_content)
        
        # Check that it returns a dictionary
        self.assertIsInstance(mapping, dict)
        
        # Check that there are 3 agents
        self.assertEqual(len(mapping), 3)
        
        # Check that each agent has files
        self.assertTrue(len(mapping["agent_1"]) > 0)
        self.assertTrue(len(mapping["agent_2"]) > 0)
        self.assertTrue(len(mapping["agent_3"]) > 0)
        
        # Check specific file assignments
        self.assertIn("main.py", mapping["agent_1"])
        self.assertIn("core/agents/anthropic.py", mapping["agent_2"])
        self.assertIn("config/prompts/phase_1_prompts.py", mapping["agent_3"])
    
    def test_get_all_file_assignments(self):
        """Test that get_all_file_assignments correctly gets all file paths."""
        # Call the function
        file_paths = get_all_file_assignments(self.test_content)
        
        # Check that it returns a list
        self.assertIsInstance(file_paths, list)
        
        # Check that there are files
        self.assertTrue(len(file_paths) > 0)
        
        # Check specific files from all agents
        self.assertIn("main.py", file_paths)
        self.assertIn("core/agents/anthropic.py", file_paths)
        self.assertIn("config/prompts/phase_1_prompts.py", file_paths)
        
        # Check that all files from all agents are included
        # Count total files in test document
        test_file_count = self.test_content.count("<file_path>")
        self.assertEqual(len(file_paths), test_file_count)


def run_tests():
    """Run the tests defined in this module."""
    unittest.main()


if __name__ == "__main__":
    run_tests()