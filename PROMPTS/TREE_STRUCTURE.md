# PROMPTS Directory - Organized Tree Structure

## Proposed Reorganization

```
PROMPTS/
├── README.md                           # Keep - Entry point documentation
├── TREE_STRUCTURE.md                   # This file - Organization guide
│
├── agents/                             # Core prompt agents (17 files)
│   ├── research/
│   │   ├── research.agent.md
│   │   ├── lit.agent.md
│   │   └── experiment.agent.md
│   │
│   ├── analysis/
│   │   ├── alignment.agent.md
│   │   ├── incident.agent.md
│   │   ├── triage.agent.md
│   │   └── diligence.agent.md
│   │
│   ├── communication/
│   │   ├── comms.agent.md
│   │   ├── grant.agent.md
│   │   └── portfolio.agent.md
│   │
│   ├── development/
│   │   ├── pipeline.agent.md
│   │   ├── memory.agent.md
│   │   └── protocol.agent.md
│   │
│   ├── planning/
│   │   ├── ideation.agent.md
│   │   ├── learningroadmap.agent.md
│   │   └── policyimpact.agent.md
│   │
│   └── governance/
│       └── ethics.agent.md
│
├── templates/                          # Reusable templates
│   ├── minimal_context.yaml
│   ├── schema_template.json
│   └── schema_template.yaml
│
├── schemas/                           # Keep existing schema directory
│   ├── README.md
│   ├── protocolShell.v1.json
│   └── symbolicResidue.v1.json
│
├── context-schemas/                    # Keep existing context-schemas
│   ├── README.md
│   ├── context.json
│   ├── context_v2.0.json
│   ├── context_v3.0.json
│   ├── context_v3.5.json
│   ├── context_v4.0.json
│   ├── context_v5.0.json
│   └── context_v6.0.json
│
└── archive/                           # Move documentation/theory here
    ├── documentation/
    │   ├── patterns.md
    │   ├── expert_guides.md
    │   └── minimal_context.md
    │
    └── architectures/
        ├── research-architecture.md
        ├── solver-architecture.md
        ├── tutor-architecture.md
        ├── interpretability-architecture.md
        └── unified_architecture.md
```

## File Classification

### ✅ Core Prompts (Keep & Organize)
**Agent Prompts (17 files):**
- Practical, actionable prompt templates
- Clear parameters and workflows
- Ready for immediate use

**Templates:**
- `minimal_context.yaml` - Base context template
- `schema_template.json/yaml` - Schema templates

### 📁 Keep in Place
**Schema Directories:**
- `context-schemas/` - Version-controlled context schemas
- `schemas/` - Protocol and residue schemas

### 📦 Archive (Documentation/Theory)
**Documentation:**
- `patterns.md` - Design pattern theory
- `expert_guides.md` - General guidance
- `minimal_context.md` - Duplicate of YAML

**Architecture Theory:**
- `*-architecture.md` (4 files) - Theoretical frameworks
- `unified_architecture.md` - Meta-architecture theory

**Cognitive Theory:**
- `attractor_design.md` - Field theory
- `chain_of_thought.md` - Reasoning theory
- `few_shot_learning.md` - Learning theory  
- `self_organization.md` - Emergence theory
- `verification_loop.md` - Validation theory

## Benefits of Reorganization

1. **Clear Separation**: Prompts vs documentation vs schemas
2. **Logical Grouping**: Related agents grouped by function
3. **Reduced Noise**: Theory moved to archive
4. **Better Discovery**: Hierarchical structure aids navigation
5. **Maintained History**: Nothing deleted, just reorganized

## Implementation Priority

1. **High**: Create agent category directories
2. **High**: Move agent files to appropriate categories  
3. **Medium**: Create templates directory
4. **Medium**: Move documentation to archive
5. **Low**: Update README with new structure

## Usage Impact

- **Agents**: More organized, easier to find specific functionality
- **Templates**: Dedicated location for reusable components
- **Schemas**: Unchanged location, maintained compatibility
- **Documentation**: Preserved but not cluttering prompt space