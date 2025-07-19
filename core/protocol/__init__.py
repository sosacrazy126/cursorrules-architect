"""
Protocol system for CursorRules Architect.

Provides collaborative protocol design, versioning, and workflow management
capabilities for enhanced project analysis planning.
"""

from .protocol_engine import (
    ProtocolEngine, ProtocolDefinition, ProtocolPhase, ProtocolRevision,
    ProtocolBranch, ProtocolMerge, Participant, ProtocolType, ProtocolScope,
    ParticipantRole, CollaborationMode
)

__all__ = [
    'ProtocolEngine', 'ProtocolDefinition', 'ProtocolPhase', 'ProtocolRevision',
    'ProtocolBranch', 'ProtocolMerge', 'Participant', 'ProtocolType', 'ProtocolScope',
    'ParticipantRole', 'CollaborationMode'
]