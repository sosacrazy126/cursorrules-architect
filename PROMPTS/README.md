# Context Engineering Prompt Templates

> "The diversity of languages is not a diversity of signs and sounds but a diversity of views of the world." — **Wilhelm von Humboldt**

## Overview

The `PROMPTS` directory contains specialized, ready-to-use prompt templates organized for immediate practical use. This reorganized structure separates actionable prompts from documentation, making it easier to find and use the right prompt for your needs.

## Directory Structure

```
PROMPTS/
├── agents/                    # Core prompt agents (organized by function)
│   ├── research/             # Research and literature analysis
│   ├── analysis/             # Analysis and evaluation tasks
│   ├── communication/        # Communication and content creation
│   ├── development/          # Technical development tasks
│   ├── planning/             # Planning and ideation
│   └── governance/           # Ethics and governance
├── templates/                # Reusable base templates
├── context-schemas/          # Context schema definitions
├── schemas/                  # Protocol and data schemas
└── archive/                  # Documentation and theory (moved from main)
    ├── documentation/        # General documentation and guides
    └── architectures/        # Architecture theory and frameworks
```

## Prompt Template Structure

```
┌──────────────────────────────────────────────────────────┐
│                      META SECTION                        │
│ Version, author, purpose, context requirements           │
├──────────────────────────────────────────────────────────┤
│                  STRUCTURE SECTION                       │
│ Template structure, parameters, expected inputs/outputs  │
├──────────────────────────────────────────────────────────┤
│                   CONTEXT SECTION                        │
│ Field setup, attractors, residue tracking, coherence     │
├──────────────────────────────────────────────────────────┤
│                    PROMPT SECTION                        │
│ Actual prompt template with parameter placeholders       │
├──────────────────────────────────────────────────────────┤
│                  WORKFLOW SECTION                        │
│ Multi-stage process flow, feedback loops                 │
├──────────────────────────────────────────────────────────┤
│                   EXAMPLES SECTION                       │
│ Sample use cases, inputs/outputs, variations             │
└──────────────────────────────────────────────────────────┘
```

## Agent Categories

All prompt agents are organized into functional categories for easy discovery:

### 🔬 Research (`agents/research/`)
- **research.agent.md** - Literature review and synthesis
- **lit.agent.md** - Literary analysis and interpretation
- **experiment.agent.md** - Experimental design and analysis

### 🔍 Analysis (`agents/analysis/`)
- **alignment.agent.md** - AI safety and alignment evaluation
- **incident.agent.md** - Post-incident analysis and investigation
- **triage.agent.md** - Priority assessment and resource allocation
- **diligence.agent.md** - Thorough investigation and verification

### 💬 Communication (`agents/communication/`)
- **comms.agent.md** - Communication strategy and messaging
- **grant.agent.md** - Grant writing and funding proposals
- **portfolio.agent.md** - Portfolio creation and presentation

### 🛠️ Development (`agents/development/`)
- **pipeline.agent.md** - Development pipeline and workflow management
- **memory.agent.md** - Memory systems and knowledge management
- **protocol.agent.md** - Protocol implementation and orchestration

### 📋 Planning (`agents/planning/`)
- **ideation.agent.md** - Creative ideation and brainstorming
- **learningroadmap.agent.md** - Learning path design and progression
- **policyimpact.agent.md** - Policy analysis and impact assessment

### ⚖️ Governance (`agents/governance/`)
- **ethics.agent.md** - Ethical decision making and frameworks

## Templates & Schemas

### 📄 Base Templates (`templates/`)
- **minimal_context.yaml** - Basic context structure template
- **schema_template.json** - JSON schema template
- **schema_template.yaml** - YAML schema template

### 📊 Context Schemas (`context-schemas/`)
- Version-controlled context schema definitions (v2.0 through v6.0)
- Progressive context engineering implementations

### 🔧 Protocol Schemas (`schemas/`)
- **protocolShell.v1.json** - Protocol shell definitions
- **symbolicResidue.v1.json** - Symbolic residue tracking schemas

## Archived Materials

Documentation and theory files have been moved to `archive/` to reduce noise:

### 📚 Documentation (`archive/documentation/`)
- Design patterns and cognitive theory
- Expert guides and learning materials
- Context engineering principles

### 🏗️ Architectures (`archive/architectures/`)
- Research assistant architecture
- Solver and tutor architectures
- Interpretability frameworks
- Unified architecture theory

## Usage Patterns

### Basic Template Application

To use a prompt template in its simplest form:

```python
import re

# Load template
with open('PROMPTS/agents/research/research.agent.md', 'r') as f:
    template = f.read()

# Replace parameters
filled_template = template.replace('{{RESEARCH_TOPIC}}', 'climate change mitigation')
                         .replace('{{FOCUS_AREA}}', 'carbon capture technologies')
                         .replace('{{TIME_FRAME}}', 'last 5 years')

# Use with LLM
response = llm.generate(filled_template)
```

### Advanced Integration

For more sophisticated applications, integrate with other context engineering components:

```python
from templates.prompt_program_template import PromptProgram
from templates.field_protocol_shells import ProtocolShell

# Load prompt template
with open('PROMPTS/agents/development/protocol.agent.md', 'r') as f:
    template = f.read()
    
# Extract context section
context_section = re.search(r'## Context\s+```yaml\s+(.*?)\s+```', 
                          template, re.DOTALL).group(1)
                          
# Parse context configuration
context_config = yaml.safe_load(context_section)

# Create field protocol
protocol = ProtocolShell.from_dict(context_config.get('protocol', {}))

# Create prompt program with the template
program = PromptProgram(
    description=context_config.get('description', ''),
    template=template
)

# Execute integrated system
result = program.execute_with_protocol(protocol, {'input': user_query})
```

### Template Customization

Templates can be customized for specific use cases:

1. **Parameter Adjustment**: Modify placeholder values for your specific needs
2. **Section Enhancement**: Add specialized sections for your domain
3. **Context Integration**: Connect with your knowledge base or retrieval system
4. **Workflow Modification**: Adapt the process flow for your specific task
5. **Field Tuning**: Adjust attractor strengths and field parameters

## Implementation Principles

All prompt templates in this directory follow these core principles:

1. **Layered Structure**: Building from fundamental prompts to complex systems
2. **Parameterization**: Clear parameter interfaces for customization
3. **Context Awareness**: Explicit context management and field dynamics
4. **Workflow Integration**: Defined process flows and interaction patterns
5. **Example Provision**: Concrete examples demonstrating effective use
6. **Documentation**: Comprehensive explanations of design and application
7. **Modularity**: Ability to compose with other templates and components

## Development Guidelines

When creating new prompt templates, follow these guidelines:

1. Use the standardized section structure
2. Document all parameters with clear descriptions
3. Include at least three example use cases
4. Specify context requirements and field dynamics
5. Implement appropriate workflow processes
6. Test across different models and scenarios
7. Follow naming convention: `[domain].[purpose].md`

## Learning Path

For those new to context engineering prompts, we recommend this progression:

1. Start with basic task-specific templates
2. Move to cognitive tool templates to learn reasoning patterns
3. Explore field operation templates for advanced context dynamics
4. Experiment with agent protocol templates for autonomous systems

## Related Resources

- See [`templates/minimal_context.yaml`](templates/minimal_context.yaml) for foundational context structure
- See [`context-schemas/`](context-schemas/) for context schema definitions
- See [`schemas/`](schemas/) for protocol and data schemas
- See [`archive/documentation/`](archive/documentation/) for theory and guides

---

*This directory is continuously expanded with new templates as context engineering techniques evolve. Contributions are welcome via pull requests.*
