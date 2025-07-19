"""
Memory Agent Implementation for CursorRules Architect

Implements knowledge persistence, semantic linking, and contextual retrieval
based on the memory.agent.md template from PROMPTS directory.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import sqlite3
from enum import Enum


class LinkType(Enum):
    """Types of semantic links between knowledge nodes."""
    REFERENCE = "reference"
    DEPENDENCY = "dependency"
    RELATED = "related"
    CONTRADICTS = "contradicts"
    EXPANDS = "expands"
    DEPRECATED = "deprecated"


class NodeType(Enum):
    """Types of knowledge nodes."""
    DOCUMENT = "doc"
    MEETING = "meeting"
    INSIGHT = "insight"
    SPECIFICATION = "spec"
    ANALYSIS = "analysis"
    PROJECT = "project"
    PATTERN = "pattern"


@dataclass
class KnowledgeNode:
    """Represents a single knowledge node in the memory system."""
    id: str
    title: str
    content: str
    type: NodeType
    created: datetime
    tags: List[str]
    links: List[str]  # List of linked node IDs
    source: str = ""
    contributor: str = ""
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary for storage."""
        data = asdict(self)
        data['created'] = self.created.isoformat()
        data['type'] = self.type.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeNode':
        """Create node from dictionary."""
        data['created'] = datetime.fromisoformat(data['created'])
        data['type'] = NodeType(data['type'])
        return cls(**data)


@dataclass
class SemanticLink:
    """Represents a semantic link between knowledge nodes."""
    source_id: str
    target_id: str
    link_type: LinkType
    reason: str
    created: datetime
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert link to dictionary for storage."""
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'link_type': self.link_type.value,
            'reason': self.reason,
            'created': self.created.isoformat(),
            'confidence': self.confidence
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SemanticLink':
        """Create link from dictionary."""
        data['created'] = datetime.fromisoformat(data['created'])
        data['link_type'] = LinkType(data['link_type'])
        return cls(**data)


class MemoryAgent:
    """
    Memory agent for knowledge persistence and contextual retrieval.
    
    Implements the memory.agent workflow:
    - ingest: Add new knowledge nodes
    - curate: Review and clean nodes
    - semantic_link: Create connections between nodes
    - contextual_retrieve: Find relevant nodes
    - recursive_refine: Improve categorization
    - audit_version: Track all changes
    """

    def __init__(self, db_path: str = "memory_agent.db"):
        """Initialize memory agent with database."""
        self.db_path = db_path
        self.audit_log = []
        self._init_database()
        
        # Make NodeType accessible as class attribute
        self.NodeType = NodeType

    def _init_database(self):
        """Initialize SQLite database for memory storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create nodes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                type TEXT NOT NULL,
                created TEXT NOT NULL,
                tags TEXT NOT NULL,
                links TEXT NOT NULL,
                source TEXT,
                contributor TEXT,
                metadata TEXT
            )
        ''')

        # Create links table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                link_type TEXT NOT NULL,
                reason TEXT NOT NULL,
                created TEXT NOT NULL,
                confidence REAL NOT NULL,
                FOREIGN KEY (source_id) REFERENCES nodes (id),
                FOREIGN KEY (target_id) REFERENCES nodes (id)
            )
        ''')

        # Create audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                node_id TEXT,
                contributor TEXT,
                timestamp TEXT NOT NULL,
                version TEXT,
                details TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def ingest_node(self, title: str, content: str, node_type: NodeType, 
                   tags: List[str], source: str = "", contributor: str = "") -> str:
        """
        Ingest new knowledge node into memory system.
        
        Args:
            title: Node title
            content: Node content
            node_type: Type of node
            tags: Associated tags
            source: Source of information
            contributor: Who contributed this
            
        Returns:
            Node ID
        """
        # Generate unique ID based on content hash
        content_hash = hashlib.md5(f"{title}{content}".encode()).hexdigest()
        node_id = f"N{content_hash[:8]}"

        # Check for duplicates
        if self._node_exists(node_id):
            self._log_audit("DUPLICATE_DETECTED", node_id, contributor, 
                          f"Duplicate node detected: {title}")
            return node_id

        # Create node
        node = KnowledgeNode(
            id=node_id,
            title=title,
            content=content,
            type=node_type,
            created=datetime.now(),
            tags=tags,
            links=[],
            source=source,
            contributor=contributor
        )

        # Store in database
        self._store_node(node)
        
        # Log audit
        self._log_audit("INGEST", node_id, contributor, f"Ingested: {title}")
        
        return node_id

    def curate_nodes(self, review_tags: List[str] = None) -> Dict[str, str]:
        """
        Review and curate knowledge nodes.
        
        Args:
            review_tags: Tags to focus curation on
            
        Returns:
            Curation results with actions taken
        """
        curation_results = {}
        nodes = self._get_nodes(tags_filter=review_tags)

        for node in nodes:
            action = self._determine_curation_action(node)
            curation_results[node.id] = action
            
            if action == "MERGE":
                similar_nodes = self._find_similar_nodes(node)
                if similar_nodes:
                    self._merge_nodes(node, similar_nodes[0])
                    
            elif action == "DELETE":
                self._delete_node(node.id)
                
            elif action == "UPDATE_TAGS":
                updated_tags = self._suggest_tag_improvements(node)
                self._update_node_tags(node.id, updated_tags)

        return curation_results

    def create_semantic_links(self, node_id: str) -> List[SemanticLink]:
        """
        Create semantic links for a knowledge node.
        
        Args:
            node_id: ID of node to create links for
            
        Returns:
            List of created semantic links
        """
        node = self._get_node(node_id)
        if not node:
            return []

        created_links = []
        potential_targets = self._find_link_candidates(node)

        for target, link_type, reason, confidence in potential_targets:
            link = SemanticLink(
                source_id=node_id,
                target_id=target.id,
                link_type=link_type,
                reason=reason,
                created=datetime.now(),
                confidence=confidence
            )
            
            self._store_link(link)
            created_links.append(link)
            
            # Update node links
            self._add_node_link(node_id, target.id)

        return created_links

    def contextual_retrieve(self, query: str, context: Dict[str, Any] = None) -> List[KnowledgeNode]:
        """
        Retrieve nodes relevant to query and context.
        
        Args:
            query: Search query
            context: Additional context for retrieval
            
        Returns:
            Ranked list of relevant nodes
        """
        # Parse query for tags and keywords
        query_tags = self._extract_tags_from_query(query)
        keywords = self._extract_keywords_from_query(query)

        # Find matching nodes
        candidate_nodes = self._search_nodes(keywords, query_tags)
        
        # Rank by relevance
        ranked_nodes = self._rank_nodes_by_relevance(candidate_nodes, query, context)
        
        # Log retrieval
        self._log_audit("RETRIEVE", None, "system", 
                       f"Retrieved {len(ranked_nodes)} nodes for query: {query[:50]}")
        
        return ranked_nodes

    def recursive_refine(self, max_depth: int = 3, depth: int = 0) -> Dict[str, Any]:
        """
        Recursively refine and recategorize knowledge base.
        
        Args:
            max_depth: Maximum recursion depth
            depth: Current recursion depth
            
        Returns:
            Refinement results and recommendations
        """
        if depth >= max_depth:
            return {"status": "max_depth_reached", "depth": depth}

        refinement_results = {
            "orphaned_nodes": self._find_orphaned_nodes(),
            "tag_suggestions": self._suggest_tag_consolidation(),
            "merge_candidates": self._find_merge_candidates(),
            "deprecated_content": self._find_deprecated_content()
        }

        # Apply automatic refinements
        changes_made = False
        
        # Link orphaned nodes
        for node in refinement_results["orphaned_nodes"][:5]:  # Limit to 5 per iteration
            links_created = self.create_semantic_links(node.id)
            if links_created:
                changes_made = True

        # If changes were made, recurse for further refinement
        if changes_made and depth < max_depth:
            nested_results = self.recursive_refine(max_depth, depth + 1)
            refinement_results["nested_refinement"] = nested_results

        return refinement_results

    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit log entries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT action, node_id, contributor, timestamp, version, details
            FROM audit_log
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        entries = []
        for row in cursor.fetchall():
            entries.append({
                'action': row[0],
                'node_id': row[1],
                'contributor': row[2],
                'timestamp': row[3],
                'version': row[4],
                'details': row[5]
            })
        
        conn.close()
        return entries

    # Private helper methods

    def _node_exists(self, node_id: str) -> bool:
        """Check if node exists in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM nodes WHERE id = ?', (node_id,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def _store_node(self, node: KnowledgeNode):
        """Store node in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO nodes 
            (id, title, content, type, created, tags, links, source, contributor, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            node.id, node.title, node.content, node.type.value,
            node.created.isoformat(), json.dumps(node.tags), 
            json.dumps(node.links), node.source, node.contributor,
            json.dumps(node.metadata)
        ))
        
        conn.commit()
        conn.close()

    def _get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get node by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM nodes WHERE id = ?', (node_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        return KnowledgeNode(
            id=row[0], title=row[1], content=row[2], 
            type=NodeType(row[3]), created=datetime.fromisoformat(row[4]),
            tags=json.loads(row[5]), links=json.loads(row[6]),
            source=row[7], contributor=row[8], 
            metadata=json.loads(row[9]) if row[9] else {}
        )

    def _get_nodes(self, tags_filter: List[str] = None) -> List[KnowledgeNode]:
        """Get all nodes, optionally filtered by tags."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if tags_filter:
            # This is a simplified filter - in production would use proper tag indexing
            cursor.execute('SELECT * FROM nodes')
            all_rows = cursor.fetchall()
            rows = []
            for row in all_rows:
                node_tags = json.loads(row[5])
                if any(tag in node_tags for tag in tags_filter):
                    rows.append(row)
        else:
            cursor.execute('SELECT * FROM nodes')
            rows = cursor.fetchall()
        
        conn.close()
        
        nodes = []
        for row in rows:
            nodes.append(KnowledgeNode(
                id=row[0], title=row[1], content=row[2], 
                type=NodeType(row[3]), created=datetime.fromisoformat(row[4]),
                tags=json.loads(row[5]), links=json.loads(row[6]),
                source=row[7], contributor=row[8],
                metadata=json.loads(row[9]) if row[9] else {}
            ))
        
        return nodes

    def _store_link(self, link: SemanticLink):
        """Store semantic link in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO links 
            (source_id, target_id, link_type, reason, created, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            link.source_id, link.target_id, link.link_type.value,
            link.reason, link.created.isoformat(), link.confidence
        ))
        
        conn.commit()
        conn.close()

    def _log_audit(self, action: str, node_id: str, contributor: str, details: str):
        """Log audit entry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (action, node_id, contributor, timestamp, version, details)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (action, node_id, contributor, datetime.now().isoformat(), "1.0", details))
        
        conn.commit()
        conn.close()

    # Simplified implementations for demonstration
    # In production, these would use more sophisticated algorithms

    def _determine_curation_action(self, node: KnowledgeNode) -> str:
        """Determine what curation action to take for a node."""
        # Simplified logic - in production would use ML/NLP
        if len(node.content) < 50:
            return "DELETE"  # Too short, likely noise
        elif "duplicate" in node.title.lower():
            return "MERGE"
        else:
            return "KEEP"

    def _find_similar_nodes(self, node: KnowledgeNode) -> List[KnowledgeNode]:
        """Find nodes similar to given node."""
        # Simplified - would use semantic similarity in production
        all_nodes = self._get_nodes()
        similar = []
        for other in all_nodes:
            if other.id != node.id and any(tag in other.tags for tag in node.tags):
                similar.append(other)
        return similar[:3]  # Return top 3

    def _find_link_candidates(self, node: KnowledgeNode) -> List[Tuple[KnowledgeNode, LinkType, str, float]]:
        """Find potential semantic link targets for a node."""
        candidates = []
        all_nodes = self._get_nodes()
        
        for other in all_nodes:
            if other.id == node.id:
                continue
                
            # Simple keyword matching - would use embeddings in production
            common_tags = set(node.tags) & set(other.tags)
            if common_tags:
                candidates.append((
                    other, 
                    LinkType.RELATED, 
                    f"Shares tags: {', '.join(common_tags)}", 
                    0.7
                ))
        
        return candidates[:5]  # Return top 5

    def _extract_tags_from_query(self, query: str) -> List[str]:
        """Extract tags from search query."""
        # Simplified - would use NLP in production
        words = query.lower().split()
        return [word for word in words if len(word) > 3]

    def _extract_keywords_from_query(self, query: str) -> List[str]:
        """Extract keywords from search query."""
        return query.lower().split()

    def _search_nodes(self, keywords: List[str], tags: List[str]) -> List[KnowledgeNode]:
        """Search nodes by keywords and tags."""
        all_nodes = self._get_nodes()
        matching = []
        
        for node in all_nodes:
            score = 0
            content_lower = node.content.lower()
            title_lower = node.title.lower()
            
            # Keyword matching
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1
                if keyword in title_lower:
                    score += 2
            
            # Tag matching
            for tag in tags:
                if tag in node.tags:
                    score += 3
            
            if score > 0:
                matching.append((node, score))
        
        # Sort by score and return nodes
        matching.sort(key=lambda x: x[1], reverse=True)
        return [node for node, score in matching]

    def _rank_nodes_by_relevance(self, nodes: List[KnowledgeNode], 
                                query: str, context: Dict[str, Any] = None) -> List[KnowledgeNode]:
        """Rank nodes by relevance to query and context."""
        # Simplified ranking - would use more sophisticated scoring in production
        return nodes[:10]  # Return top 10

    def _find_orphaned_nodes(self) -> List[KnowledgeNode]:
        """Find nodes with no semantic links."""
        all_nodes = self._get_nodes()
        return [node for node in all_nodes if not node.links]

    def _suggest_tag_consolidation(self) -> Dict[str, List[str]]:
        """Suggest tag consolidation opportunities."""
        # Simplified - would use clustering in production
        return {}

    def _find_merge_candidates(self) -> List[Tuple[str, str]]:
        """Find pairs of nodes that could be merged."""
        # Simplified - would use semantic similarity in production
        return []

    def _find_deprecated_content(self) -> List[KnowledgeNode]:
        """Find content that may be deprecated."""
        # Simplified - would check timestamps and references in production
        return []

    def _merge_nodes(self, node1: KnowledgeNode, node2: KnowledgeNode):
        """Merge two nodes into one."""
        # Simplified merge logic
        merged_content = f"{node1.content}\n\n--- MERGED FROM ---\n\n{node2.content}"
        merged_tags = list(set(node1.tags + node2.tags))
        
        # Update node1 with merged content
        node1.content = merged_content
        node1.tags = merged_tags
        self._store_node(node1)
        
        # Delete node2
        self._delete_node(node2.id)
        
        self._log_audit("MERGE", node1.id, "system", f"Merged {node2.id} into {node1.id}")

    def _delete_node(self, node_id: str):
        """Delete a node from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete the node
        cursor.execute('DELETE FROM nodes WHERE id = ?', (node_id,))
        
        # Delete associated links
        cursor.execute('DELETE FROM links WHERE source_id = ? OR target_id = ?', 
                      (node_id, node_id))
        
        conn.commit()
        conn.close()
        
        self._log_audit("DELETE", node_id, "system", f"Deleted node {node_id}")

    def _suggest_tag_improvements(self, node: KnowledgeNode) -> List[str]:
        """Suggest improved tags for a node."""
        # Simplified - would use NLP in production
        return node.tags  # Return unchanged for now

    def _update_node_tags(self, node_id: str, new_tags: List[str]):
        """Update tags for a node."""
        node = self._get_node(node_id)
        if node:
            node.tags = new_tags
            self._store_node(node)
            self._log_audit("UPDATE_TAGS", node_id, "system", f"Updated tags: {new_tags}")

    def _add_node_link(self, source_id: str, target_id: str):
        """Add a link reference to a node."""
        node = self._get_node(source_id)
        if node and target_id not in node.links:
            node.links.append(target_id)
            self._store_node(node)

    def _create_link(self, source_id: str, target_id: str, link_type: LinkType, reason: str) -> SemanticLink:
        """Create a semantic link between two nodes."""
        return SemanticLink(
            source_id=source_id,
            target_id=target_id,
            link_type=link_type,
            reason=reason,
            created=datetime.now(),
            confidence=1.0
        )

    def _get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)