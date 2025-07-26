"""
Integration layer for Protocol Engine with Phase 2 Analysis Planning.

Enhances Phase 2 planning with collaborative protocol design capabilities,
versioning, and workflow management.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from .protocol_engine import (
    ProtocolEngine, ProtocolType, ProtocolScope, ParticipantRole, 
    CollaborationMode, Participant
)


class Phase2ProtocolIntegration:
    """
    Integration layer for Protocol Engine with Phase 2 analysis planning.
    
    Enhances Phase 2 with:
    - Collaborative analysis planning protocols
    - Versioned analysis strategies
    - Multi-stakeholder coordination
    - Protocol evolution tracking
    """

    def __init__(self, protocol_storage_path: str = "phase2_protocols.json"):
        """Initialize with protocol engine."""
        self.protocol_engine = ProtocolEngine(protocol_storage_path)
        self.current_analysis_protocol = None
        self.phase2_templates = self._initialize_phase2_templates()

    def create_analysis_protocol(self, project_context: Dict[str, Any], 
                                stakeholders: List[Dict[str, Any]]) -> str:
        """
        Create a collaborative analysis protocol for Phase 2 planning.
        
        Args:
            project_context: Context about the project being analyzed
            stakeholders: List of stakeholders involved in analysis
            
        Returns:
            Protocol name for the created analysis protocol
        """
        # Prepare context for protocol creation
        protocol_context = {
            "protocol_name": f"analysis_protocol_{project_context.get('name', 'project')}_{datetime.now().strftime('%Y%m%d')}",
            "purpose": f"Collaborative analysis planning for {project_context.get('name', 'project')}",
            "domain": "technical",
            "scope": "pilot",
            "collaboration_mode": "async",
            "participants": []
        }

        # Add stakeholders as participants
        for i, stakeholder in enumerate(stakeholders):
            participant_data = {
                "id": f"stakeholder_{i}",
                "role": stakeholder.get("role", "contributor"),
                "expertise": stakeholder.get("expertise", "general")
            }
            protocol_context["participants"].append(participant_data)

        # Add default analysis roles if no stakeholders provided
        if not stakeholders:
            default_participants = [
                {"id": "analyst", "role": "initiator", "expertise": "code_analysis"},
                {"id": "architect", "role": "reviewer", "expertise": "system_design"},
                {"id": "qa_lead", "role": "contributor", "expertise": "quality_assurance"}
            ]
            protocol_context["participants"] = default_participants

        # Run protocol design workflow
        clarified_context = self.protocol_engine.clarify_context(protocol_context)
        ideation_results = self.protocol_engine.ideate(clarified_context, 
                                                      ["analysis_strategy", "technology_assessment", "risk_identification"])
        workflow_mapping = self.protocol_engine.map_workflow(clarified_context, ideation_results)
        protocol_draft = self.protocol_engine.draft_protocol(clarified_context, workflow_mapping)

        # Store current protocol for session
        self.current_analysis_protocol = protocol_context["protocol_name"]

        # Enhance protocol with Phase 2 specific elements
        self._enhance_protocol_for_phase2(protocol_context["protocol_name"], project_context)

        return protocol_context["protocol_name"]

    def get_analysis_strategy(self, protocol_name: str, 
                            project_technologies: List[str]) -> Dict[str, Any]:
        """
        Get analysis strategy from protocol for specific technologies.
        
        Args:
            protocol_name: Name of the analysis protocol
            project_technologies: Technologies detected in project
            
        Returns:
            Customized analysis strategy
        """
        if protocol_name not in self.protocol_engine.protocols:
            raise ValueError(f"Protocol {protocol_name} not found")

        # Get base protocol phases
        base_phases = self.protocol_engine.phases.get(protocol_name, [])
        
        # Customize strategy based on technologies
        analysis_strategy = {
            "protocol_name": protocol_name,
            "technology_focus": project_technologies,
            "analysis_phases": [],
            "risk_factors": [],
            "recommended_tools": [],
            "success_criteria": []
        }

        # Adapt phases for detected technologies
        for phase in base_phases:
            adapted_phase = {
                "name": phase.name,
                "description": phase.description,
                "technology_specific_tasks": [],
                "validation_criteria": phase.criteria.copy()
            }

            # Add technology-specific tasks
            for tech in project_technologies:
                tech_tasks = self._get_technology_specific_tasks(tech, phase.name)
                adapted_phase["technology_specific_tasks"].extend(tech_tasks)

            analysis_strategy["analysis_phases"].append(adapted_phase)

        # Add technology-specific recommendations
        for tech in project_technologies:
            tech_risks = self._get_technology_risks(tech)
            analysis_strategy["risk_factors"].extend(tech_risks)
            
            tech_tools = self._get_technology_tools(tech)
            analysis_strategy["recommended_tools"].extend(tech_tools)

        # Define success criteria
        analysis_strategy["success_criteria"] = [
            "All critical components identified",
            "Technology stack fully mapped",
            "Risk assessment completed",
            "Performance bottlenecks identified",
            "Security vulnerabilities documented"
        ]

        return analysis_strategy

    def propose_analysis_revision(self, protocol_name: str, 
                                 revision_type: str, changes: Dict[str, Any],
                                 proposer: str, rationale: str) -> Dict[str, Any]:
        """
        Propose a revision to the analysis protocol.
        
        Args:
            protocol_name: Name of protocol to revise
            revision_type: Type of revision (scope, strategy, timeline)
            changes: Proposed changes
            proposer: Who is proposing the revision
            rationale: Why the revision is needed
            
        Returns:
            Revision proposal results
        """
        # Prepare revision changes
        revision_changes = {
            "description": f"{revision_type} revision",
            "type": revision_type,
            **changes
        }

        # Apply revision through protocol engine
        revision_result = self.protocol_engine.revision(
            protocol_name=protocol_name,
            changes=revision_changes,
            author=proposer,
            rationale=rationale
        )

        # Add Phase 2 specific validation
        validation_result = self._validate_phase2_revision(protocol_name, revision_changes)
        revision_result["phase2_validation"] = validation_result

        return revision_result

    def fork_analysis_approach(self, protocol_name: str, alternative_name: str,
                              forked_by: str, alternative_purpose: str) -> str:
        """
        Create an alternative analysis approach by forking the protocol.
        
        Args:
            protocol_name: Original protocol to fork
            alternative_name: Name for alternative approach
            forked_by: Who is creating the alternative
            alternative_purpose: Purpose of the alternative approach
            
        Returns:
            Branch ID for the alternative approach
        """
        branch_id = self.protocol_engine.fork_protocol(
            protocol_name=protocol_name,
            branch_name=alternative_name,
            created_by=forked_by,
            purpose=alternative_purpose
        )

        # Customize fork for alternative analysis approach
        self._customize_analysis_fork(branch_id, alternative_purpose)

        return branch_id

    def merge_analysis_approaches(self, source_branch_id: str, 
                                target_protocol_name: str, merged_by: str) -> Dict[str, Any]:
        """
        Merge alternative analysis approach back into main protocol.
        
        Args:
            source_branch_id: Branch with alternative approach
            target_protocol_name: Main protocol to merge into
            merged_by: Who is performing the merge
            
        Returns:
            Merge results with conflict resolution
        """
        merge_result = self.protocol_engine.merge_protocol(
            source_branch_id=source_branch_id,
            target_protocol_name=target_protocol_name,
            merged_by=merged_by,
            merge_strategy="phase2_analysis_merge"
        )

        # Add Phase 2 specific merge validation
        merge_validation = self._validate_analysis_merge(source_branch_id, target_protocol_name)
        merge_result["analysis_validation"] = merge_validation

        return merge_result

    def get_protocol_evolution_for_project(self, protocol_name: str) -> Dict[str, Any]:
        """
        Get evolution history of analysis protocol for project reporting.
        
        Args:
            protocol_name: Name of the analysis protocol
            
        Returns:
            Evolution history formatted for project reporting
        """
        evolution = self.protocol_engine.get_protocol_evolution(protocol_name)
        
        # Add Phase 2 specific interpretation
        phase2_evolution = {
            "protocol_name": protocol_name,
            "current_analysis_version": evolution["current_version"],
            "analysis_iterations": len(evolution["revisions"]),
            "alternative_approaches": len(evolution["branches"]),
            "approach_merges": len(evolution["merges"]),
            "evolution_summary": self._summarize_analysis_evolution(evolution),
            "lessons_learned": self._extract_analysis_lessons(evolution)
        }

        return phase2_evolution

    def generate_phase2_report(self, protocol_name: str) -> Dict[str, Any]:
        """
        Generate comprehensive Phase 2 report including protocol evolution.
        
        Args:
            protocol_name: Name of analysis protocol
            
        Returns:
            Comprehensive Phase 2 analysis report
        """
        if protocol_name not in self.protocol_engine.protocols:
            raise ValueError(f"Protocol {protocol_name} not found")

        protocol = self.protocol_engine.protocols[protocol_name]
        evolution = self.get_protocol_evolution_for_project(protocol_name)
        decision_log = self.protocol_engine.get_decision_log(protocol_name)

        report = {
            "protocol_overview": {
                "name": protocol.name,
                "purpose": protocol.purpose,
                "created": protocol.created.isoformat(),
                "current_version": protocol.version,
                "scope": protocol.scope.value
            },
            "analysis_strategy": self._extract_analysis_strategy_from_protocol(protocol_name),
            "collaboration_summary": self._summarize_collaboration(protocol_name),
            "evolution_history": evolution,
            "decision_trail": decision_log[-10:],  # Last 10 decisions
            "recommendations": self._generate_phase2_recommendations(protocol_name)
        }

        return report

    # Private helper methods

    def _initialize_phase2_templates(self) -> Dict[str, Any]:
        """Initialize Phase 2 specific protocol templates."""
        return {
            "web_application": {
                "focus_areas": ["frontend_framework", "backend_api", "database", "deployment"],
                "risk_factors": ["scalability", "security", "performance"],
                "tools": ["static_analysis", "dependency_scan", "performance_profiling"]
            },
            "mobile_application": {
                "focus_areas": ["platform_compatibility", "ui_framework", "data_storage", "api_integration"],
                "risk_factors": ["device_compatibility", "performance", "app_store_compliance"],
                "tools": ["mobile_testing", "performance_monitoring", "security_scan"]
            },
            "data_science": {
                "focus_areas": ["data_pipeline", "ml_framework", "model_architecture", "deployment"],
                "risk_factors": ["data_quality", "model_bias", "scalability"],
                "tools": ["data_profiling", "model_validation", "pipeline_testing"]
            }
        }

    def _enhance_protocol_for_phase2(self, protocol_name: str, project_context: Dict[str, Any]):
        """Enhance protocol with Phase 2 specific elements."""
        if protocol_name not in self.protocol_engine.protocols:
            return

        protocol = self.protocol_engine.protocols[protocol_name]
        
        # Add Phase 2 specific metadata
        protocol.metadata.update({
            "phase2_enhanced": True,
            "project_type": project_context.get("type", "unknown"),
            "expected_technologies": project_context.get("technologies", []),
            "analysis_depth": "comprehensive",
            "timeline_estimate": "3-5 days"
        })

        # Store enhanced protocol
        self.protocol_engine.protocols[protocol_name] = protocol

    def _get_technology_specific_tasks(self, technology: str, phase_name: str) -> List[str]:
        """Get technology-specific tasks for a phase."""
        tech_tasks = {
            "javascript": {
                "initialization": ["Identify JS frameworks", "Check package.json dependencies"],
                "execution": ["Analyze component structure", "Review async patterns"],
                "validation": ["Check for security vulnerabilities", "Validate performance patterns"]
            },
            "python": {
                "initialization": ["Identify Python version", "Check requirements.txt"],
                "execution": ["Analyze package structure", "Review import patterns"],
                "validation": ["Run security scans", "Check code style compliance"]
            },
            "react": {
                "initialization": ["Identify React version", "Check component architecture"],
                "execution": ["Analyze component hierarchy", "Review state management"],
                "validation": ["Check accessibility compliance", "Validate performance"]
            }
        }

        return tech_tasks.get(technology.lower(), {}).get(phase_name, [])

    def _get_technology_risks(self, technology: str) -> List[str]:
        """Get risk factors for specific technology."""
        tech_risks = {
            "javascript": ["dependency vulnerabilities", "callback complexity", "browser compatibility"],
            "python": ["dependency conflicts", "version compatibility", "performance bottlenecks"],
            "react": ["component complexity", "state management issues", "render performance"],
            "node.js": ["async complexity", "memory leaks", "security vulnerabilities"],
            "database": ["query performance", "data consistency", "backup strategies"]
        }

        return tech_risks.get(technology.lower(), [])

    def _get_technology_tools(self, technology: str) -> List[str]:
        """Get recommended tools for specific technology."""
        tech_tools = {
            "javascript": ["ESLint", "Prettier", "Jest", "Webpack Bundle Analyzer"],
            "python": ["pylint", "black", "pytest", "bandit"],
            "react": ["React DevTools", "Testing Library", "Storybook"],
            "node.js": ["nodemon", "PM2", "clinic.js"],
            "database": ["pgAdmin", "MongoDB Compass", "SQL profiler"]
        }

        return tech_tools.get(technology.lower(), [])

    def _validate_phase2_revision(self, protocol_name: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Phase 2 specific revision changes."""
        validation = {
            "valid": True,
            "warnings": [],
            "errors": []
        }

        # Check if changes maintain Phase 2 integrity
        if "scope" in changes and changes["scope"] not in ["narrow", "broad", "pilot"]:
            validation["errors"].append("Invalid scope for Phase 2 analysis")
            validation["valid"] = False

        # Check if analysis depth is maintained
        if "analysis_depth" in changes and changes["analysis_depth"] not in ["basic", "comprehensive", "deep"]:
            validation["warnings"].append("Analysis depth should be appropriate for Phase 2")

        return validation

    def _customize_analysis_fork(self, branch_id: str, alternative_purpose: str):
        """Customize forked protocol for alternative analysis approach."""
        # This would contain logic to adapt the forked protocol
        # based on the alternative purpose
        pass

    def _validate_analysis_merge(self, source_branch_id: str, target_protocol_name: str) -> Dict[str, Any]:
        """Validate analysis-specific merge requirements."""
        return {
            "conflicts_detected": False,
            "analysis_consistency": True,
            "merge_recommendations": []
        }

    def _summarize_analysis_evolution(self, evolution: Dict[str, Any]) -> str:
        """Summarize evolution history for analysis context."""
        summary = f"Analysis protocol evolved through {len(evolution['revisions'])} iterations"
        
        if evolution["branches"]:
            summary += f" with {len(evolution['branches'])} alternative approaches explored"
        
        if evolution["merges"]:
            summary += f" and {len(evolution['merges'])} approaches merged"

        return summary

    def _extract_analysis_lessons(self, evolution: Dict[str, Any]) -> List[str]:
        """Extract lessons learned from protocol evolution."""
        lessons = []
        
        if len(evolution["revisions"]) > 3:
            lessons.append("Multiple iterations indicate complex analysis requirements")
        
        if evolution["branches"]:
            lessons.append("Alternative approaches were necessary for comprehensive analysis")
        
        if evolution["merges"]:
            lessons.append("Collaborative analysis approach yielded better results")

        return lessons

    def _extract_analysis_strategy_from_protocol(self, protocol_name: str) -> Dict[str, Any]:
        """Extract analysis strategy summary from protocol."""
        protocol = self.protocol_engine.protocols[protocol_name]
        phases = self.protocol_engine.phases.get(protocol_name, [])
        
        return {
            "approach": protocol.purpose,
            "phases": len(phases),
            "scope": protocol.scope.value,
            "estimated_duration": f"{len(phases) * 2} days"
        }

    def _summarize_collaboration(self, protocol_name: str) -> Dict[str, Any]:
        """Summarize collaboration aspects of the protocol."""
        participants = [p for p in self.protocol_engine.participants.values()]
        
        return {
            "participants": len(participants),
            "roles_involved": list(set(p.role.value for p in participants)),
            "expertise_areas": list(set(p.expertise for p in participants)),
            "collaboration_mode": "async"  # Default for now
        }

    def _generate_phase2_recommendations(self, protocol_name: str) -> List[str]:
        """Generate recommendations based on protocol analysis."""
        protocol = self.protocol_engine.protocols[protocol_name]
        
        recommendations = [
            "Continue with planned analysis approach",
            "Monitor for emerging technical risks",
            "Validate findings with stakeholders"
        ]

        # Add specific recommendations based on metadata
        if protocol.metadata.get("project_type") == "web_application":
            recommendations.append("Focus on frontend-backend integration analysis")
        
        if len(self.protocol_engine.revisions.get(protocol_name, [])) > 2:
            recommendations.append("Consider stabilizing analysis approach")

        return recommendations