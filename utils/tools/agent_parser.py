#!/usr/bin/env python3
"""
utils/tools/agent_parser.py

This module provides functionality for parsing agent assignments from Phase 2's
XML-like output format. It extracts agent definitions, responsibilities, and file
assignments to enable dynamic agent creation in Phase 3.

This module is used by Phase 3 to create agents based on Phase 2's allocation plan.
"""

# ====================================================
# Importing Necessary Libraries
# This section imports all the external libraries needed for this script to work.
# These libraries add extra functionalities like handling XML, regular expressions, and logging.
# ====================================================

import re
import logging
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET
from io import StringIO

# ====================================================
# Initialize Logger
# Set up a logger to record important events and errors during the script's execution.
# ====================================================

logger = logging.getLogger("project_extractor")

# ====================================================
# Define XML Tag Constants
# These constants store the names of XML tags used in the Phase 2 output.
# Using constants makes it easier to update tag names if they change in the future.
# ====================================================

DESCRIPTION_TAG = "description"
FILE_ASSIGNMENTS_TAG = "file_assignments"
FILE_PATH_TAG = "file_path"
NAME_TAG = "name"
EXPERTISE_TAG = "expertise"
RESPONSIBILITIES_TAG = "responsibilities"
RESPONSIBILITY_TAG = "responsibility"
REASONING_TAG = "reasoning"
ANALYSIS_PLAN_TAG = "analysis_plan"


# ====================================================
# Function: create_xml_from_phase2_output
# This function takes the raw output from Phase 2 and converts it into a well-formed XML string.
# It handles cases where the output might be missing tags or have formatting issues.
# ====================================================

def create_xml_from_phase2_output(phase2_output: str) -> str:
    """
    Create proper XML from the Phase 2 output by wrapping it in a root element
    and fixing any XML issues.
    
    Args:
        phase2_output: Raw output from Phase 2
        
    Returns:
        str: Properly formatted XML string
    """
    # Extract the XML-like content from between <analysis_plan> tags
    plan_match = re.search(r'<analysis_plan>(.*?)</analysis_plan>', 
                          phase2_output, re.DOTALL)
    
    # If not found, check if there's a reasoning tag followed by an analysis_plan tag
    if not plan_match:
        reasoning_and_plan_match = re.search(r'<reasoning>(.*?)</reasoning>.*?<analysis_plan>(.*?)</analysis_plan>',
                                        phase2_output, re.DOTALL)
        if reasoning_and_plan_match:
            # Just extract the analysis_plan part
            xml_content = reasoning_and_plan_match.group(2).strip()
            logger.info("Found analysis_plan after reasoning tag")
        else:
            logger.error("Could not find <analysis_plan> tags in Phase 2 output")
            # Try to extract without tags as a fallback
            # Look for agent tag sequences
            agent_matches = re.findall(r'<agent_\d+.*?>.*?</agent_\d+>', phase2_output, re.DOTALL)
            if agent_matches:
                xml_content = "\n".join(agent_matches)
                logger.info("Extracted agent definitions without analysis_plan tag")
            else:
                logger.error("Could not find agent definitions in Phase 2 output")
                return "<analysis_plan></analysis_plan>"
    else:
        xml_content = plan_match.group(1).strip()
    
    # Fix non-standard attribute format in agent tags
    # Replace <agent_1="Name"> with <agent_1 name="Name">
    xml_content = re.sub(r'<(agent_\d+)="([^"]*)">', r'<\1 name="\2">', xml_content)
    
    # Escape any potentially problematic characters in content between tags
    # This is a quick and dirty fix - ideally we would parse and rebuild the XML properly
    xml_content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_content)
    
    # Wrap in a root element
    return f"<analysis_plan>\n{xml_content}\n</analysis_plan>"


# ====================================================
# Function: parse_agent_definition
# This function takes an XML element representing an agent and extracts its information.
# It pulls out details like ID, name, description, expertise, responsibilities, and file assignments.
# ====================================================

def parse_agent_definition(agent_element: ET.Element) -> Dict:
    """
    Parse an agent element into a structured dictionary.
    
    Args:
        agent_element: XML Element representing an agent
        
    Returns:
        Dict: Structured agent definition
    """
    agent_id = agent_element.tag
    agent_info = {
        "id": agent_id,
        "name": "",
        "description": "",
        "expertise": [],
        "responsibilities": [],
        "file_assignments": []
    }
    
    # Get agent name from attribute first
    if "name" in agent_element.attrib:
        agent_info["name"] = agent_element.attrib["name"]
    else:
        # Try to get name from child element
        name_elem = agent_element.find(NAME_TAG)
        if name_elem is not None and name_elem.text:
            agent_info["name"] = name_elem.text.strip()
        else:
            # Use agent_id as fallback name
            agent_info["name"] = agent_id.replace("_", " ").title()
    
    # Get description
    description_elem = agent_element.find(DESCRIPTION_TAG)
    if description_elem is not None and description_elem.text:
        agent_info["description"] = description_elem.text.strip()
    
    # Get expertise
    expertise_elem = agent_element.find(EXPERTISE_TAG)
    if expertise_elem is not None and expertise_elem.text:
        agent_info["expertise"] = [exp.strip() for exp in expertise_elem.text.split(',')]
    
    # Get responsibilities
    responsibilities_elem = agent_element.find(RESPONSIBILITIES_TAG)
    if responsibilities_elem is not None:
        for resp_elem in responsibilities_elem.findall(RESPONSIBILITY_TAG):
            if resp_elem.text:
                agent_info["responsibilities"].append(resp_elem.text.strip())
    
    # Get file assignments
    file_assignments_elem = agent_element.find(FILE_ASSIGNMENTS_TAG)
    if file_assignments_elem is not None:
        for file_path_elem in file_assignments_elem.findall(FILE_PATH_TAG):
            if file_path_elem.text and file_path_elem.text.strip():
                agent_info["file_assignments"].append(file_path_elem.text.strip())
    
    return agent_info


# ====================================================
# Function: extract_agent_fallback
# This function is a backup plan for extracting agent information.
# If the XML parsing fails, this function uses regular expressions to find and extract agent details.
# ====================================================

def extract_agent_fallback(phase2_output: str) -> List[Dict]:
    """
    Extract agent definitions using regex as a fallback when XML parsing fails.
    
    Args:
        phase2_output: Raw output from Phase 2
        
    Returns:
        List[Dict]: List of agent definitions
    """
    # First try to directly extract full agent blocks with regex
    agents = []
    
    # Find all file assignment blocks to make sure we get all files
    assignment_blocks = re.findall(r'<file_assignments>(.*?)</file_assignments>', phase2_output, re.DOTALL)
    
    # Try to extract agent IDs and names
    # First, try to get agents with name attributes
    agent_matches = re.findall(r'<(agent_\d+)\s+name="([^"]*)"', phase2_output, re.DOTALL)
    
    # If no matches with name attribute, try simpler extraction
    if not agent_matches:
        # Look for agent tags without attributes, then try to find name tags inside
        agent_ids = re.findall(r'<(agent_\d+)[^>]*>', phase2_output, re.DOTALL)
        agent_matches = []
        
        for agent_id in agent_ids:
            # Try to find a name tag inside this agent element
            name_pattern = f'<{agent_id}[^>]*>.*?<name>(.*?)</name>'
            name_match = re.search(name_pattern, phase2_output, re.DOTALL)
            name = name_match.group(1).strip() if name_match else f"Agent {agent_id.split('_')[1]}"
            agent_matches.append((agent_id, name))
    
    # If we still have no matches, create generic agents based on assignment blocks
    if not agent_matches:
        agent_matches = [(f"agent_{i+1}", f"Agent {i+1}") for i in range(len(assignment_blocks))]
    
    # Extract file assignments for each agent
    for i, (agent_id, agent_name) in enumerate(agent_matches):
        if i < len(assignment_blocks):
            block = assignment_blocks[i]
            file_paths = re.findall(r'<file_path>(.*?)</file_path>', block, re.DOTALL)
            file_paths = [path.strip() for path in file_paths if path.strip()]
            
            # Try to get description
            desc_pattern = f'<{agent_id}[^>]*>.*?<description>(.*?)</description>'
            desc_match = re.search(desc_pattern, phase2_output, re.DOTALL)
            description = desc_match.group(1).strip() if desc_match else f"Agent {i+1}"
            
            # Create agent dict without XML entity decoding issues
            agent_info = {
                "id": agent_id,
                "name": agent_name.replace("&amp;", "and"),  # Replace XML entity with "and"
                "description": description.replace("&amp;", "and"),  # Replace XML entity with "and"
                "expertise": [],
                "responsibilities": [],
                "file_assignments": file_paths
            }
            
            agents.append(agent_info)
    
    # If we still failed to extract agents, create a simple one with all files
    if not agents:
        all_files = []
        for block in assignment_blocks:
            file_paths = re.findall(r'<file_path>(.*?)</file_path>', block, re.DOTALL)
            all_files.extend([path.strip() for path in file_paths if path.strip()])
        
        if all_files:
            agents.append({
                "id": "agent_1",
                "name": "Fallback Agent",
                "description": "Automatically created fallback agent",
                "expertise": [],
                "responsibilities": [],
                "file_assignments": all_files
            })
    
    return agents


# ====================================================
# Function: parse_agents_from_phase2
# This is the main function for parsing agent definitions from the Phase 2 output.
# It first tries to parse the output as XML, and if that fails, it uses the fallback function.
# ====================================================

def parse_agents_from_phase2(phase2_output: str) -> List[Dict]:
    """
    Parse agent definitions from Phase 2 output.
    
    Args:
        phase2_output: Raw output from Phase 2
        
    Returns:
        List[Dict]: List of agent definitions
    """
    try:
        # First attempt: Try to parse as proper XML
        xml_content = create_xml_from_phase2_output(phase2_output)
        root = ET.fromstring(xml_content)
        
        agents = []
        # Look for any tags that start with "agent_"
        for element in root:
            if element.tag.startswith("agent_"):
                agent_info = parse_agent_definition(element)
                agents.append(agent_info)
        
        if agents:
            return agents
            
    except ET.ParseError as e:
        logger.warning(f"XML parsing failed: {e}. Falling back to regex method.")
    
    # Fallback: Try the regex-based extraction
    logger.info("Using regex-based extraction method")
    return extract_agent_fallback(phase2_output)


# ====================================================
# Function: get_agent_file_mapping
# This function creates a dictionary that maps agent IDs to the list of files they are assigned to.
# ====================================================

def get_agent_file_mapping(phase2_output: str) -> Dict[str, List[str]]:
    """
    Get a mapping of agent IDs to their assigned files.
    
    Args:
        phase2_output: Raw output from Phase 2
        
    Returns:
        Dict[str, List[str]]: Dictionary mapping agent IDs to file paths
    """
    agents = parse_agents_from_phase2(phase2_output)
    mapping = {}
    
    for agent in agents:
        mapping[agent["id"]] = agent["file_assignments"]
    
    return mapping

# ====================================================
# Function: get_all_file_assignments
# This function gathers all the unique file paths that are assigned to any agent.
# ====================================================

def get_all_file_assignments(phase2_output: str) -> List[str]:
    """
    Get a list of all unique file paths assigned to any agent.
    
    Args:
        phase2_output: Raw output from Phase 2
        
    Returns:
        List[str]: List of all unique file paths
    """
    agents = parse_agents_from_phase2(phase2_output)
    all_files = set()
    
    for agent in agents:
        for file_path in agent["file_assignments"]:
            all_files.add(file_path)
    
    return list(all_files)