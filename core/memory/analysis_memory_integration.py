"""
Integration layer between Memory Agent and CursorRules Architect analysis system.

Provides seamless integration of memory capabilities into the existing
6-phase analysis pipeline.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from .memory_agent import MemoryAgent, KnowledgeNode, NodeType, LinkType


class AnalysisMemoryIntegration:
    """
    Integration layer for Memory Agent with CursorRules Architect.
    
    Handles:
    - Storing analysis results as knowledge nodes
    - Retrieving similar project analysis for context
    - Linking related analysis phases
    - Learning from previous analysis patterns
    """

    def __init__(self, memory_db_path: str = "analysis_memory.db"):
        """Initialize with memory agent."""
        self.memory_agent = MemoryAgent(memory_db_path)
        self.current_project_id = None
        self.current_analysis_session = None

    def start_analysis_session(self, project_path: str, project_name: str) -> str:
        """
        Start a new analysis session and create project node.
        
        Args:
            project_path: Path to project being analyzed
            project_name: Name of the project
            
        Returns:
            Project node ID
        """
        # Create project metadata
        project_metadata = {
            "project_path": project_path,
            "analysis_started": datetime.now().isoformat(),
            "framework_version": "1.0.0"
        }

        # Create project node
        self.current_project_id = self.memory_agent.ingest_node(
            title=f"Project Analysis: {project_name}",
            content=f"Analysis of project at {project_path}",
            node_type=NodeType.PROJECT,
            tags=["project", "analysis", project_name.lower()],
            source="cursorrules_architect",
            contributor="analysis_system"
        )

        # Update project node with metadata
        project_node = self.memory_agent._get_node(self.current_project_id)
        if project_node:
            project_node.metadata = project_metadata
            self.memory_agent._store_node(project_node)

        # Initialize analysis session
        self.current_analysis_session = {
            "project_id": self.current_project_id,
            "phase_nodes": {},
            "start_time": datetime.now(),
            "project_path": project_path,
            "project_name": project_name
        }

        return self.current_project_id

    def store_phase_analysis(self, phase_name: str, analysis_result: Dict[str, Any], 
                           phase_number: int) -> str:
        """
        Store analysis result from a specific phase.
        
        Args:
            phase_name: Name of the analysis phase
            analysis_result: Result data from the phase
            phase_number: Phase number (1-6)
            
        Returns:
            Node ID for the phase analysis
        """
        if not self.current_analysis_session:
            raise ValueError("No active analysis session. Call start_analysis_session first.")

        # Create phase node
        phase_title = f"Phase {phase_number}: {phase_name}"
        phase_content = self._format_analysis_content(analysis_result)
        
        phase_tags = [
            "analysis_phase", 
            f"phase_{phase_number}", 
            phase_name.lower().replace(" ", "_"),
            self.current_analysis_session["project_name"].lower()
        ]

        # Add framework/technology tags from analysis
        if "technologies" in analysis_result:
            phase_tags.extend([tech.lower() for tech in analysis_result["technologies"]])

        phase_node_id = self.memory_agent.ingest_node(
            title=phase_title,
            content=phase_content,
            node_type=NodeType.ANALYSIS,
            tags=phase_tags,
            source="cursorrules_architect",
            contributor=f"phase_{phase_number}_analyzer"
        )

        # Store in session
        self.current_analysis_session["phase_nodes"][phase_name] = phase_node_id

        # Link to project node
        if self.current_project_id:
            self.memory_agent._store_link(self.memory_agent._create_link(
                source_id=self.current_project_id,
                target_id=phase_node_id,
                link_type=LinkType.REFERENCE,
                reason=f"Contains analysis from {phase_name}"
            ))

        # Link to previous phase if exists
        if phase_number > 1:
            previous_phases = [
                node_id for phase, node_id in self.current_analysis_session["phase_nodes"].items()
                if node_id != phase_node_id
            ]
            if previous_phases:
                self.memory_agent._store_link(self.memory_agent._create_link(
                    source_id=previous_phases[-1],  # Most recent previous phase
                    target_id=phase_node_id,
                    link_type=LinkType.DEPENDENCY,
                    reason=f"Sequential analysis phase dependency"
                ))

        return phase_node_id

    def get_similar_projects(self, technologies: List[str], 
                           project_type: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve similar projects from memory for context.
        
        Args:
            technologies: List of technologies used in current project
            project_type: Type of project (web, mobile, etc.)
            
        Returns:
            List of similar project analyses with similarity scores
        """
        # Create search query
        tech_query = " ".join(technologies)
        if project_type:
            tech_query += f" {project_type}"

        # Retrieve similar nodes
        similar_nodes = self.memory_agent.contextual_retrieve(
            query=tech_query,
            context={"node_types": [NodeType.PROJECT.value, NodeType.ANALYSIS.value]}
        )

        # Format results
        similar_projects = []
        for node in similar_nodes[:5]:  # Top 5 most similar
            if node.type == NodeType.PROJECT:
                project_info = {
                    "project_id": node.id,
                    "project_name": node.title,
                    "technologies": [tag for tag in node.tags if tag not in ["project", "analysis"]],
                    "analysis_date": node.created.isoformat(),
                    "metadata": node.metadata
                }
                
                # Get related phase analyses
                related_phases = self._get_project_phases(node.id)
                project_info["phases"] = related_phases
                
                similar_projects.append(project_info)

        return similar_projects

    def get_phase_patterns(self, phase_name: str, technologies: List[str]) -> Dict[str, Any]:
        """
        Get patterns and insights from previous analyses of similar phases.
        
        Args:
            phase_name: Name of the current phase
            technologies: Technologies in current project
            
        Returns:
            Patterns and recommendations from similar analyses
        """
        # Search for similar phase analyses
        query = f"phase {phase_name} " + " ".join(technologies)
        similar_phases = self.memory_agent.contextual_retrieve(
            query=query,
            context={"node_type": NodeType.ANALYSIS.value, "phase": phase_name}
        )

        patterns = {
            "common_issues": [],
            "best_practices": [],
            "recommendations": [],
            "similar_analyses": len(similar_phases)
        }

        # Extract patterns from similar analyses
        for phase_node in similar_phases[:10]:  # Analyze top 10
            try:
                # Parse phase content (simplified - would use NLP in production)
                content = phase_node.content.lower()
                
                # Extract common issues
                if "issue" in content or "problem" in content:
                    patterns["common_issues"].append(self._extract_issues(content))
                
                # Extract best practices
                if "recommend" in content or "best practice" in content:
                    patterns["best_practices"].append(self._extract_practices(content))
                    
            except Exception as e:
                # Log error but continue processing
                continue

        # Deduplicate and rank patterns
        patterns["common_issues"] = list(set(filter(None, patterns["common_issues"])))
        patterns["best_practices"] = list(set(filter(None, patterns["best_practices"])))

        return patterns

    def store_final_analysis(self, final_result: Dict[str, Any]) -> str:
        """
        Store the final consolidated analysis result.
        
        Args:
            final_result: Complete analysis result
            
        Returns:
            Node ID for final analysis
        """
        if not self.current_analysis_session:
            raise ValueError("No active analysis session.")

        # Create final analysis node
        final_content = self._format_final_analysis(final_result)
        
        final_node_id = self.memory_agent.ingest_node(
            title=f"Final Analysis: {self.current_analysis_session['project_name']}",
            content=final_content,
            node_type=NodeType.SPECIFICATION,
            tags=[
                "final_analysis", 
                "complete",
                self.current_analysis_session["project_name"].lower()
            ],
            source="cursorrules_architect",
            contributor="final_analyzer"
        )

        # Link to all phase nodes
        for phase_node_id in self.current_analysis_session["phase_nodes"].values():
            self.memory_agent._store_link(self.memory_agent._create_link(
                source_id=final_node_id,
                target_id=phase_node_id,
                link_type=LinkType.REFERENCE,
                reason="Synthesizes analysis from this phase"
            ))

        # Update project node with final analysis link
        if self.current_project_id:
            self.memory_agent._store_link(self.memory_agent._create_link(
                source_id=self.current_project_id,
                target_id=final_node_id,
                link_type=LinkType.REFERENCE,
                reason="Final analysis result"
            ))

        return final_node_id

    def end_analysis_session(self) -> Dict[str, Any]:
        """
        End the current analysis session and perform cleanup.
        
        Returns:
            Session summary
        """
        if not self.current_analysis_session:
            return {"status": "no_active_session"}

        session_summary = {
            "project_id": self.current_project_id,
            "phases_completed": len(self.current_analysis_session["phase_nodes"]),
            "phase_nodes": list(self.current_analysis_session["phase_nodes"].values()),
            "duration": (datetime.now() - self.current_analysis_session["start_time"]).total_seconds(),
            "project_name": self.current_analysis_session["project_name"]
        }

        # Create semantic links between related phases
        self._create_phase_links()

        # Reset session
        self.current_analysis_session = None
        self.current_project_id = None

        return session_summary

    def get_project_history(self, project_name: str = None) -> List[Dict[str, Any]]:
        """
        Get analysis history for projects.
        
        Args:
            project_name: Specific project name to filter by
            
        Returns:
            List of project analysis histories
        """
        if project_name:
            query = f"project {project_name}"
        else:
            query = "project analysis"

        project_nodes = self.memory_agent.contextual_retrieve(query)
        
        histories = []
        for node in project_nodes:
            if node.type == NodeType.PROJECT:
                history = {
                    "project_id": node.id,
                    "project_name": node.title,
                    "analysis_date": node.created.isoformat(),
                    "metadata": node.metadata,
                    "phases": self._get_project_phases(node.id)
                }
                histories.append(history)

        return histories

    # Private helper methods

    def _format_analysis_content(self, analysis_result: Dict[str, Any]) -> str:
        """Format analysis result for storage."""
        formatted_lines = []
        
        for key, value in analysis_result.items():
            if isinstance(value, list):
                formatted_lines.append(f"## {key.replace('_', ' ').title()}")
                for item in value:
                    formatted_lines.append(f"- {item}")
                formatted_lines.append("")
            elif isinstance(value, dict):
                formatted_lines.append(f"## {key.replace('_', ' ').title()}")
                formatted_lines.append(json.dumps(value, indent=2))
                formatted_lines.append("")
            else:
                formatted_lines.append(f"**{key.replace('_', ' ').title()}**: {value}")
                formatted_lines.append("")

        return "\n".join(formatted_lines)

    def _format_final_analysis(self, final_result: Dict[str, Any]) -> str:
        """Format final analysis result for storage."""
        content = "# Final Analysis Summary\n\n"
        
        if "summary" in final_result:
            content += f"## Executive Summary\n{final_result['summary']}\n\n"
        
        if "recommendations" in final_result:
            content += "## Key Recommendations\n"
            for rec in final_result["recommendations"]:
                content += f"- {rec}\n"
            content += "\n"
        
        if "technologies" in final_result:
            content += f"## Technologies Identified\n"
            content += f"{', '.join(final_result['technologies'])}\n\n"
        
        # Add complete result as JSON
        content += "## Complete Analysis Data\n"
        content += f"```json\n{json.dumps(final_result, indent=2)}\n```"
        
        return content

    def _get_project_phases(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all phase analyses for a project."""
        # Get all links from the project node
        conn = self.memory_agent._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT target_id FROM links 
            WHERE source_id = ? AND link_type = ?
        ''', (project_id, LinkType.REFERENCE.value))
        
        linked_nodes = cursor.fetchall()
        conn.close()
        
        phases = []
        for (target_id,) in linked_nodes:
            node = self.memory_agent._get_node(target_id)
            if node and node.type == NodeType.ANALYSIS:
                phases.append({
                    "phase_id": node.id,
                    "phase_name": node.title,
                    "created": node.created.isoformat(),
                    "tags": node.tags
                })
        
        return phases

    def _create_phase_links(self):
        """Create semantic links between related phases in current session."""
        if not self.current_analysis_session:
            return

        phase_ids = list(self.current_analysis_session["phase_nodes"].values())
        
        # Create links between consecutive phases
        for i in range(len(phase_ids) - 1):
            current_phase = phase_ids[i]
            next_phase = phase_ids[i + 1]
            
            # Only create if link doesn't already exist
            existing_links = self._get_node_links(current_phase)
            if next_phase not in [link.target_id for link in existing_links]:
                self.memory_agent._store_link(self.memory_agent._create_link(
                    source_id=current_phase,
                    target_id=next_phase,
                    link_type=LinkType.DEPENDENCY,
                    reason="Sequential phase in analysis pipeline"
                ))

    def _get_node_links(self, node_id: str) -> List[Any]:
        """Get all links for a node."""
        # Simplified implementation
        return []

    def _extract_issues(self, content: str) -> Optional[str]:
        """Extract issues from phase content."""
        # Simplified extraction - would use NLP in production
        sentences = content.split('.')
        for sentence in sentences:
            if "issue" in sentence or "problem" in sentence:
                return sentence.strip()[:100]  # First 100 chars
        return None

    def _extract_practices(self, content: str) -> Optional[str]:
        """Extract best practices from phase content."""
        # Simplified extraction - would use NLP in production
        sentences = content.split('.')
        for sentence in sentences:
            if "recommend" in sentence or "best practice" in sentence:
                return sentence.strip()[:100]  # First 100 chars
        return None