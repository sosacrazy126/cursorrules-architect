"""
Protocol Engine Implementation for CursorRules Architect

Implements collaborative protocol design and analysis workflow management
based on the protocol.agent.md template from PROMPTS directory.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib


class ProtocolType(Enum):
    """Types of protocols that can be managed."""
    TECHNICAL = "technical"
    SOCIAL = "social"
    SCIENTIFIC = "scientific"
    HYBRID = "hybrid"


class ProtocolScope(Enum):
    """Scope of protocol application."""
    NARROW = "narrow"
    BROAD = "broad" 
    PILOT = "pilot"
    STANDARD = "standard"


class ParticipantRole(Enum):
    """Roles participants can have in protocol design."""
    INITIATOR = "initiator"
    CONTRIBUTOR = "contributor"
    REVIEWER = "reviewer"
    APPROVER = "approver"


class CollaborationMode(Enum):
    """Modes of collaboration for protocol design."""
    SYNC = "sync"
    ASYNC = "async"
    ROUNDTABLE = "roundtable"
    OPEN_CALL = "open_call"


@dataclass
class Participant:
    """Represents a participant in protocol design."""
    id: str
    role: ParticipantRole
    expertise: str
    contributions: List[str] = None

    def __post_init__(self):
        if self.contributions is None:
            self.contributions = []


@dataclass
class ProtocolDefinition:
    """Represents a protocol being designed."""
    name: str
    protocol_type: ProtocolType
    purpose: str
    scope: ProtocolScope
    created: datetime
    version: str = "1.0.0"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ProtocolPhase:
    """Represents a phase in protocol design workflow."""
    name: str
    description: str
    inputs: List[str]
    outputs: List[str]
    criteria: List[str]
    completed: bool = False
    results: Dict[str, Any] = None

    def __post_init__(self):
        if self.results is None:
            self.results = {}


@dataclass
class ProtocolRevision:
    """Represents a revision to a protocol."""
    protocol_id: str
    change_description: str
    author: str
    rationale: str
    timestamp: datetime
    version: str
    diff: Dict[str, Any] = None

    def __post_init__(self):
        if self.diff is None:
            self.diff = {}


@dataclass
class ProtocolBranch:
    """Represents a protocol branch (fork)."""
    branch_id: str
    parent_protocol_id: str
    branch_name: str
    created_by: str
    created_at: datetime
    purpose: str
    active: bool = True


@dataclass
class ProtocolMerge:
    """Represents a protocol merge operation."""
    merge_id: str
    source_branch_id: str
    target_protocol_id: str
    merged_by: str
    merged_at: datetime
    merge_strategy: str
    conflicts_resolved: List[str] = None

    def __post_init__(self):
        if self.conflicts_resolved is None:
            self.conflicts_resolved = []


class ProtocolEngine:
    """
    Protocol Engine for collaborative protocol design and management.
    
    Implements the protocol.agent workflow:
    - clarify_context: Understand requirements and participants
    - ideate: Generate protocol concepts and strategies
    - map_workflow: Design protocol phases and dependencies
    - draft_protocol: Create actionable protocol draft
    - revision: Incorporate feedback and track changes
    - merge_fork_version: Handle branching and merging
    - decision_logging: Track all decisions and outcomes
    """

    def __init__(self, storage_path: str = "protocols.json"):
        """Initialize protocol engine."""
        self.storage_path = storage_path
        self.protocols: Dict[str, ProtocolDefinition] = {}
        self.participants: Dict[str, Participant] = {}
        self.phases: Dict[str, List[ProtocolPhase]] = {}
        self.revisions: Dict[str, List[ProtocolRevision]] = {}
        self.branches: Dict[str, ProtocolBranch] = {}
        self.merges: Dict[str, ProtocolMerge] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.load_state()

    def clarify_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clarify protocol requirements and context.
        
        Args:
            context: Context information including participants, goals, etc.
            
        Returns:
            Clarified context with identified gaps and questions
        """
        clarified = {
            "protocol_name": context.get("protocol_name", ""),
            "purpose": context.get("purpose", ""),
            "domain": context.get("domain", ""),
            "scope": context.get("scope", "broad"),
            "participants": [],
            "collaboration_mode": context.get("collaboration_mode", "async"),
            "open_questions": [],
            "clarified_goals": []
        }

        # Process participants
        for participant_data in context.get("participants", []):
            participant = Participant(
                id=participant_data.get("id", f"participant_{len(self.participants)}"),
                role=ParticipantRole(participant_data.get("role", "contributor")),
                expertise=participant_data.get("expertise", "general")
            )
            self.participants[participant.id] = participant
            clarified["participants"].append({
                "id": participant.id,
                "role": participant.role.value,
                "expertise": participant.expertise
            })

        # Identify missing information
        if not clarified["protocol_name"]:
            clarified["open_questions"].append("What should this protocol be named?")
        
        if not clarified["purpose"]:
            clarified["open_questions"].append("What is the primary purpose of this protocol?")

        if len(clarified["participants"]) == 0:
            clarified["open_questions"].append("Who are the key participants in this protocol design?")

        # Generate clarified goals
        if clarified["purpose"]:
            clarified["clarified_goals"].append(f"Create {clarified['scope']} protocol for {clarified['purpose']}")
        
        if clarified["participants"]:
            clarified["clarified_goals"].append(f"Coordinate input from {len(clarified['participants'])} participants")

        self._log_audit("CLARIFY_CONTEXT", None, "system", 
                       f"Clarified context for {clarified['protocol_name']}")

        return clarified

    def ideate(self, context: Dict[str, Any], focus_areas: List[str] = None) -> Dict[str, Any]:
        """
        Facilitate ideation for protocol concepts.
        
        Args:
            context: Clarified context from previous phase
            focus_areas: Specific areas to focus ideation on
            
        Returns:
            Ideation results with concepts and themes
        """
        if focus_areas is None:
            focus_areas = ["requirements", "strategies", "features", "constraints"]

        ideation_results = {
            "idea_pool": [],
            "thematic_clusters": {},
            "focus_areas": focus_areas,
            "participant_contributions": {}
        }

        # Generate initial ideas based on context
        protocol_type = context.get("domain", "technical")
        purpose = context.get("purpose", "")

        # Seed ideas based on protocol type and purpose
        base_ideas = self._generate_base_ideas(protocol_type, purpose)
        ideation_results["idea_pool"].extend(base_ideas)

        # Cluster ideas by themes
        for area in focus_areas:
            area_ideas = [idea for idea in base_ideas if area.lower() in idea.lower()]
            if area_ideas:
                ideation_results["thematic_clusters"][area] = area_ideas

        # Track participant contributions (placeholder for actual collaboration)
        for participant_id in context.get("participants", []):
            if isinstance(participant_id, dict):
                participant_id = participant_id["id"]
            ideation_results["participant_contributions"][participant_id] = []

        self._log_audit("IDEATE", None, "system", 
                       f"Generated {len(ideation_results['idea_pool'])} ideas")

        return ideation_results

    def map_workflow(self, context: Dict[str, Any], 
                    ideation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map workflow phases and dependencies for protocol.
        
        Args:
            context: Protocol context
            ideation_results: Results from ideation phase
            
        Returns:
            Workflow mapping with phases and dependencies
        """
        # Define standard protocol workflow phases
        standard_phases = [
            ProtocolPhase(
                name="initialization",
                description="Set up protocol parameters and initial state",
                inputs=["requirements", "participants"],
                outputs=["initialized_protocol", "parameter_set"],
                criteria=["all_parameters_defined", "participants_registered"]
            ),
            ProtocolPhase(
                name="execution",
                description="Execute main protocol logic and processes",
                inputs=["initialized_protocol", "input_data"],
                outputs=["processed_results", "execution_log"],
                criteria=["logic_completed", "no_errors", "outputs_validated"]
            ),
            ProtocolPhase(
                name="validation",
                description="Validate protocol results and outcomes",
                inputs=["processed_results", "validation_criteria"],
                outputs=["validation_report", "approved_results"],
                criteria=["results_verified", "criteria_met", "stakeholder_approval"]
            ),
            ProtocolPhase(
                name="finalization",
                description="Finalize protocol execution and cleanup",
                inputs=["approved_results", "cleanup_requirements"],
                outputs=["final_results", "execution_summary"],
                criteria=["cleanup_completed", "results_documented", "protocol_closed"]
            )
        ]

        # Customize phases based on ideation results
        if "thematic_clusters" in ideation_results:
            for theme, ideas in ideation_results["thematic_clusters"].items():
                if theme == "requirements":
                    # Enhance initialization phase
                    standard_phases[0].inputs.extend(ideas[:3])  # Add top 3 requirement ideas
                elif theme == "strategies":
                    # Enhance execution phase
                    standard_phases[1].criteria.extend([f"strategy_applied: {idea[:50]}" for idea in ideas[:2]])

        workflow_mapping = {
            "phases": [asdict(phase) for phase in standard_phases],
            "dependencies": self._calculate_phase_dependencies(standard_phases),
            "critical_path": [phase.name for phase in standard_phases],
            "estimated_duration": self._estimate_workflow_duration(standard_phases),
            "risk_factors": self._identify_workflow_risks(standard_phases)
        }

        # Store phases for this protocol
        protocol_name = context.get("protocol_name", "default")
        self.phases[protocol_name] = standard_phases

        self._log_audit("MAP_WORKFLOW", protocol_name, "system", 
                       f"Mapped workflow with {len(standard_phases)} phases")

        return workflow_mapping

    def draft_protocol(self, context: Dict[str, Any], workflow_mapping: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create draft protocol from previous phases.
        
        Args:
            context: Protocol context
            workflow_mapping: Workflow from mapping phase
            
        Returns:
            Protocol draft with steps and outstanding issues
        """
        protocol_name = context.get("protocol_name", f"protocol_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Create protocol definition
        protocol = ProtocolDefinition(
            name=protocol_name,
            protocol_type=ProtocolType(context.get("domain", "technical")),
            purpose=context.get("purpose", ""),
            scope=ProtocolScope(context.get("scope", "broad")),
            created=datetime.now()
        )

        # Generate protocol steps from workflow phases
        protocol_steps = []
        for phase_data in workflow_mapping.get("phases", []):
            phase_step = {
                "step": len(protocol_steps) + 1,
                "name": phase_data["name"],
                "description": phase_data["description"],
                "inputs": phase_data["inputs"],
                "outputs": phase_data["outputs"],
                "success_criteria": phase_data["criteria"]
            }
            protocol_steps.append(phase_step)

        # Identify outstanding issues
        outstanding_issues = []
        if not context.get("protocol_name"):
            outstanding_issues.append("Protocol name needs to be finalized")
        
        if not context.get("participants"):
            outstanding_issues.append("Participant roles and responsibilities need definition")

        if workflow_mapping.get("risk_factors"):
            outstanding_issues.extend([f"Risk mitigation needed: {risk}" for risk in workflow_mapping["risk_factors"][:3]])

        protocol_draft = {
            "protocol_definition": asdict(protocol),
            "protocol_steps": protocol_steps,
            "outstanding_issues": outstanding_issues,
            "estimated_complexity": self._assess_protocol_complexity(protocol_steps),
            "implementation_notes": self._generate_implementation_notes(protocol_steps)
        }

        # Store protocol
        self.protocols[protocol.name] = protocol

        self._log_audit("DRAFT_PROTOCOL", protocol.name, "system", 
                       f"Created draft with {len(protocol_steps)} steps")

        return protocol_draft

    def revision(self, protocol_name: str, changes: Dict[str, Any], 
                author: str, rationale: str) -> Dict[str, Any]:
        """
        Apply revisions to protocol and track changes.
        
        Args:
            protocol_name: Name of protocol to revise
            changes: Changes to apply
            author: Who is making the changes
            rationale: Why changes are being made
            
        Returns:
            Revision results with change log
        """
        if protocol_name not in self.protocols:
            raise ValueError(f"Protocol {protocol_name} not found")

        protocol = self.protocols[protocol_name]
        
        # Generate new version
        current_version = protocol.version
        new_version = self._increment_version(current_version)
        
        # Create revision record
        revision = ProtocolRevision(
            protocol_id=protocol_name,
            change_description=changes.get("description", "Protocol revision"),
            author=author,
            rationale=rationale,
            timestamp=datetime.now(),
            version=new_version,
            diff=changes
        )

        # Apply changes to protocol
        if "purpose" in changes:
            protocol.purpose = changes["purpose"]
        
        if "scope" in changes:
            protocol.scope = ProtocolScope(changes["scope"])
        
        if "metadata" in changes:
            protocol.metadata.update(changes["metadata"])

        # Update version
        protocol.version = new_version

        # Store revision
        if protocol_name not in self.revisions:
            self.revisions[protocol_name] = []
        self.revisions[protocol_name].append(revision)

        revision_results = {
            "revision_id": f"{protocol_name}_{new_version}",
            "previous_version": current_version,
            "new_version": new_version,
            "changes_applied": len(changes),
            "author": author,
            "timestamp": revision.timestamp.isoformat()
        }

        self._log_audit("REVISION", protocol_name, author, 
                       f"Applied revision: {rationale}")

        return revision_results

    def fork_protocol(self, protocol_name: str, branch_name: str, 
                     created_by: str, purpose: str) -> str:
        """
        Create a fork (branch) of an existing protocol.
        
        Args:
            protocol_name: Name of protocol to fork
            branch_name: Name for the new branch
            created_by: Who is creating the fork
            purpose: Purpose of the fork
            
        Returns:
            Branch ID
        """
        if protocol_name not in self.protocols:
            raise ValueError(f"Protocol {protocol_name} not found")

        # Generate branch ID
        branch_id = f"{protocol_name}_branch_{hashlib.md5(f'{branch_name}{datetime.now().isoformat()}'.encode()).hexdigest()[:8]}"

        # Create branch
        branch = ProtocolBranch(
            branch_id=branch_id,
            parent_protocol_id=protocol_name,
            branch_name=branch_name,
            created_by=created_by,
            created_at=datetime.now(),
            purpose=purpose
        )

        # Create copy of protocol for branch
        original_protocol = self.protocols[protocol_name]
        branch_protocol = ProtocolDefinition(
            name=f"{protocol_name}_{branch_name}",
            protocol_type=original_protocol.protocol_type,
            purpose=f"{original_protocol.purpose} (Branch: {purpose})",
            scope=original_protocol.scope,
            created=datetime.now(),
            version=f"{original_protocol.version}_branch",
            metadata=original_protocol.metadata.copy()
        )

        # Store branch and protocol
        self.branches[branch_id] = branch
        self.protocols[branch_protocol.name] = branch_protocol

        self._log_audit("FORK", protocol_name, created_by, 
                       f"Created branch {branch_name}: {purpose}")

        return branch_id

    def merge_protocol(self, source_branch_id: str, target_protocol_name: str, 
                      merged_by: str, merge_strategy: str = "recursive") -> Dict[str, Any]:
        """
        Merge a protocol branch back into main protocol.
        
        Args:
            source_branch_id: ID of branch to merge
            target_protocol_name: Name of target protocol
            merged_by: Who is performing the merge
            merge_strategy: Strategy for handling conflicts
            
        Returns:
            Merge results
        """
        if source_branch_id not in self.branches:
            raise ValueError(f"Branch {source_branch_id} not found")
        
        if target_protocol_name not in self.protocols:
            raise ValueError(f"Target protocol {target_protocol_name} not found")

        branch = self.branches[source_branch_id]
        branch_protocol_name = f"{branch.parent_protocol_id}_{branch.branch_name}"
        
        if branch_protocol_name not in self.protocols:
            raise ValueError(f"Branch protocol {branch_protocol_name} not found")

        # Perform merge
        target_protocol = self.protocols[target_protocol_name]
        branch_protocol = self.protocols[branch_protocol_name]

        # Detect conflicts (simplified)
        conflicts_resolved = []
        if target_protocol.purpose != branch_protocol.purpose:
            # Merge purposes
            merged_purpose = f"{target_protocol.purpose} | {branch_protocol.purpose}"
            target_protocol.purpose = merged_purpose
            conflicts_resolved.append("purpose_conflict_resolved")

        # Update version
        target_protocol.version = self._increment_version(target_protocol.version)

        # Create merge record
        merge_id = f"merge_{hashlib.md5(f'{source_branch_id}{target_protocol_name}{datetime.now().isoformat()}'.encode()).hexdigest()[:8]}"
        merge = ProtocolMerge(
            merge_id=merge_id,
            source_branch_id=source_branch_id,
            target_protocol_id=target_protocol_name,
            merged_by=merged_by,
            merged_at=datetime.now(),
            merge_strategy=merge_strategy,
            conflicts_resolved=conflicts_resolved
        )

        self.merges[merge_id] = merge

        # Deactivate branch
        branch.active = False

        merge_results = {
            "merge_id": merge_id,
            "conflicts_resolved": len(conflicts_resolved),
            "merge_strategy": merge_strategy,
            "new_version": target_protocol.version,
            "merged_at": merge.merged_at.isoformat()
        }

        self._log_audit("MERGE", target_protocol_name, merged_by, 
                       f"Merged branch {branch.branch_name}")

        return merge_results

    def get_protocol_evolution(self, protocol_name: str) -> Dict[str, Any]:
        """
        Get evolution history of a protocol including branches and merges.
        
        Args:
            protocol_name: Name of protocol
            
        Returns:
            Evolution diagram and history
        """
        if protocol_name not in self.protocols:
            raise ValueError(f"Protocol {protocol_name} not found")

        evolution = {
            "protocol_name": protocol_name,
            "current_version": self.protocols[protocol_name].version,
            "revisions": [],
            "branches": [],
            "merges": [],
            "evolution_diagram": ""
        }

        # Get revisions
        if protocol_name in self.revisions:
            evolution["revisions"] = [
                {
                    "version": rev.version,
                    "author": rev.author,
                    "timestamp": rev.timestamp.isoformat(),
                    "rationale": rev.rationale
                }
                for rev in self.revisions[protocol_name]
            ]

        # Get branches
        for branch_id, branch in self.branches.items():
            if branch.parent_protocol_id == protocol_name:
                evolution["branches"].append({
                    "branch_id": branch_id,
                    "branch_name": branch.branch_name,
                    "created_by": branch.created_by,
                    "created_at": branch.created_at.isoformat(),
                    "purpose": branch.purpose,
                    "active": branch.active
                })

        # Get merges
        for merge_id, merge in self.merges.items():
            if merge.target_protocol_id == protocol_name:
                evolution["merges"].append({
                    "merge_id": merge_id,
                    "source_branch": merge.source_branch_id,
                    "merged_by": merge.merged_by,
                    "merged_at": merge.merged_at.isoformat(),
                    "conflicts_resolved": len(merge.conflicts_resolved)
                })

        # Generate evolution diagram
        evolution["evolution_diagram"] = self._generate_evolution_diagram(evolution)

        return evolution

    def get_decision_log(self, protocol_name: str = None) -> List[Dict[str, Any]]:
        """
        Get decision and audit log.
        
        Args:
            protocol_name: Filter by specific protocol
            
        Returns:
            List of decisions and audit entries
        """
        if protocol_name:
            return [
                entry for entry in self.audit_log 
                if entry.get("protocol_name") == protocol_name
            ]
        else:
            return self.audit_log.copy()

    def save_state(self):
        """Save protocol engine state to storage."""
        # Custom function to handle enum serialization
        def serialize_protocol(protocol):
            data = asdict(protocol)
            # Convert enums to their values
            data["protocol_type"] = protocol.protocol_type.value
            data["scope"] = protocol.scope.value
            return data

        def serialize_participant(participant):
            data = asdict(participant)
            # Convert enum to its value
            data["role"] = participant.role.value
            return data

        state = {
            "protocols": {name: serialize_protocol(protocol) for name, protocol in self.protocols.items()},
            "participants": {pid: serialize_participant(participant) for pid, participant in self.participants.items()},
            "revisions": {
                name: [asdict(rev) for rev in revisions] 
                for name, revisions in self.revisions.items()
            },
            "branches": {bid: asdict(branch) for bid, branch in self.branches.items()},
            "merges": {mid: asdict(merge) for mid, merge in self.merges.items()},
            "audit_log": self.audit_log
        }

        # Convert datetime objects to ISO strings
        state_json = json.dumps(state, default=str, indent=2)
        
        with open(self.storage_path, 'w') as f:
            f.write(state_json)

    def load_state(self):
        """Load protocol engine state from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    return  # Empty file, skip loading
                state = json.loads(content)

            # Restore protocols
            for name, protocol_data in state.get("protocols", {}).items():
                try:
                    protocol_data["created"] = datetime.fromisoformat(protocol_data["created"])
                    # Handle both string and enum values for protocol_type
                    if isinstance(protocol_data["protocol_type"], str):
                        protocol_data["protocol_type"] = ProtocolType(protocol_data["protocol_type"])
                    # Handle both string and enum values for scope
                    if isinstance(protocol_data["scope"], str):
                        protocol_data["scope"] = ProtocolScope(protocol_data["scope"])
                    self.protocols[name] = ProtocolDefinition(**protocol_data)
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid protocol {name}: {e}")
                    continue

            # Restore participants
            for pid, participant_data in state.get("participants", {}).items():
                try:
                    # Handle both string and enum values for role
                    if isinstance(participant_data["role"], str):
                        participant_data["role"] = ParticipantRole(participant_data["role"])
                    self.participants[pid] = Participant(**participant_data)
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid participant {pid}: {e}")
                    continue

            # Restore other components (simplified for now)
            self.audit_log = state.get("audit_log", [])

        except FileNotFoundError:
            # Initialize empty state
            pass
        except (json.JSONDecodeError, ValueError) as e:
            # Initialize empty state on JSON errors
            pass
        except Exception as e:
            print(f"Unexpected error loading protocol engine state: {e}")
            # Initialize empty state on any error
            pass

    # Private helper methods

    def _log_audit(self, action: str, protocol_name: str, author: str, details: str):
        """Log audit entry."""
        entry = {
            "action": action,
            "protocol_name": protocol_name,
            "author": author,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.audit_log.append(entry)

    def _generate_base_ideas(self, protocol_type: str, purpose: str) -> List[str]:
        """Generate base ideas for ideation."""
        ideas = [
            f"Define clear {protocol_type} requirements",
            f"Establish {protocol_type} validation criteria",
            f"Create {protocol_type} implementation guidelines",
            f"Design {protocol_type} testing procedures",
            f"Plan {protocol_type} rollout strategy"
        ]
        
        if purpose:
            ideas.append(f"Optimize for {purpose} use case")
            ideas.append(f"Address {purpose} specific constraints")
        
        return ideas

    def _calculate_phase_dependencies(self, phases: List[ProtocolPhase]) -> List[Dict[str, Any]]:
        """Calculate dependencies between phases."""
        dependencies = []
        for i, phase in enumerate(phases):
            if i > 0:
                dependencies.append({
                    "source": phases[i-1].name,
                    "target": phase.name,
                    "type": "sequential",
                    "required": True
                })
        return dependencies

    def _estimate_workflow_duration(self, phases: List[ProtocolPhase]) -> Dict[str, int]:
        """Estimate workflow duration."""
        base_duration_per_phase = 5  # days
        return {
            "total_days": len(phases) * base_duration_per_phase,
            "total_phases": len(phases),
            "parallel_possible": False
        }

    def _identify_workflow_risks(self, phases: List[ProtocolPhase]) -> List[str]:
        """Identify potential risks in workflow."""
        risks = []
        if len(phases) > 5:
            risks.append("High complexity may lead to delays")
        
        for phase in phases:
            if len(phase.criteria) > 5:
                risks.append(f"Phase {phase.name} has many success criteria")
        
        return risks

    def _assess_protocol_complexity(self, protocol_steps: List[Dict[str, Any]]) -> str:
        """Assess protocol complexity."""
        total_criteria = sum(len(step.get("success_criteria", [])) for step in protocol_steps)
        
        if total_criteria < 10:
            return "low"
        elif total_criteria < 20:
            return "medium"
        else:
            return "high"

    def _generate_implementation_notes(self, protocol_steps: List[Dict[str, Any]]) -> List[str]:
        """Generate implementation notes."""
        notes = []
        if len(protocol_steps) > 3:
            notes.append("Consider breaking complex phases into sub-phases")
        
        notes.append("Ensure all participants understand their roles")
        notes.append("Plan regular checkpoint reviews")
        
        return notes

    def _increment_version(self, current_version: str) -> str:
        """Increment protocol version."""
        try:
            parts = current_version.split(".")
            if len(parts) >= 3:
                parts[2] = str(int(parts[2]) + 1)
            else:
                parts.append("1")
            return ".".join(parts)
        except:
            return "1.0.1"

    def _generate_evolution_diagram(self, evolution: Dict[str, Any]) -> str:
        """Generate ASCII evolution diagram."""
        diagram = f"[v1.0] {evolution['protocol_name']}\n"
        
        current_version = evolution["current_version"]
        revisions = evolution["revisions"]
        branches = evolution["branches"]
        merges = evolution["merges"]
        
        if revisions:
            diagram += " |\n"
            for rev in revisions[-3:]:  # Show last 3 revisions
                diagram += f" +--[{rev['version']}] {rev['rationale'][:30]}...\n"
        
        if branches:
            diagram += " |\n"
            for branch in branches[-2:]:  # Show last 2 branches
                status = "active" if branch["active"] else "merged"
                diagram += f" +--[branch: {branch['branch_name']}] ({status})\n"
        
        if current_version != "1.0.0":
            diagram += f" |\n +--[{current_version}] current\n"
        
        return diagram