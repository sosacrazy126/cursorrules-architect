# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Main Analysis Pipeline
```bash
# Run complete 6-phase analysis (primary functionality)
python main.py -p /path/to/your/project

# Test environment setup
python tests/test_env.py
```

### Universal AI Tool Generation
```bash
# Generate configuration for specific AI tool
python -m cli.commands.generate /path/to/project --tool cursor
python -m cli.commands.generate /path/to/project --tool windsurf  
python -m cli.commands.generate /path/to/project --tool claude

# Generate for all supported tools
python -m cli.commands.generate /path/to/project --tool all

# Preview before saving
python -m cli.commands.generate /path/to/project --tool cursor --preview

# Interactive tool selection
python -m cli.commands.generate /path/to/project
```

### Testing
```bash
# Run diagnostic tests for Phase 3 (critical component)
python tests/phase_3_diagnostic_test.py
python tests/run_phase3_diagnostic.py

# Individual phase tests
python tests/phase_1_test/run_phase1_test.py
python tests/phase_2_test/run_phase2_test.py
python tests/phase_3_test/run_phase3_test.py
python tests/phase_4_test/run_phase4_test.py
python tests/phase_5_test/run_phase5_test.py

# Real project integration test
python tests/test_real_project_phase3.py

# Final analysis test
python tests/final_analysis_test/run_final_analysis_test.py
```

### Dependencies
```bash
# Install dependencies (currently using requirements.txt)
pip install -r requirements.txt

# Key dependencies verification
python -c "import anthropic, openai, google.generativeai, rich, typer; print('All dependencies imported successfully')"
```

## Architecture

### Multi-Provider AI System
This is a sophisticated AI-powered project analysis platform that supports multiple AI providers:
- **Anthropic**: Claude 3.7 Sonnet with reasoning capabilities
- **OpenAI**: o1, o3-mini, GPT-4o with different reasoning modes  
- **DeepSeek**: DeepSeek Reasoner
- **Google**: Gemini 2.0 Flash, 2.5 Pro with thinking capabilities

### Six-Phase Analysis Pipeline
The core analysis follows a structured approach:

1. **Phase 1 (Initial Discovery)**: Three parallel agents analyze structure, dependencies, and tech stack
2. **Phase 2 (Methodical Planning)**: Creates detailed analysis plan with specialized agent assignments
3. **Phase 3 (Deep Analysis)**: Dynamic specialized agents perform in-depth file analysis
4. **Phase 4 (Synthesis)**: Integrates findings into cohesive insights
5. **Phase 5 (Consolidation)**: Creates comprehensive project documentation
6. **Final Analysis**: Generates optimized configurations for AI tools

### Universal AI Tool Support
Beyond the original .cursorrules generation, the system generates configurations for:
- **Cursor IDE** (.cursorrules)
- **Windsurf** (.windsurfrules) 
- **Cline VS Code extension** (.clinerules)
- **Roo Code** (.roorules)
- **Claude Code CLI** (CLAUDE.md)

### Context Engineering Framework
The system implements revolutionary Context Engineering concepts:
- **Neural Field Dynamics**: Continuous semantic field processing
- **Protocol Shell Engine**: Structured interaction patterns using Pareto-lang format
- **Memory Integration**: Cross-session learning and pattern recognition
- **Symbolic Residue Tracking**: Persistent project knowledge

## Key Components

### Core Analysis (`core/analysis/`)
- `phase_1.py`: Initial project discovery with parallel agents
- `phase_2.py`: Dynamic planning and agent creation
- `phase_3.py`: **CRITICAL COMPONENT** - Deep analysis execution
- `phase_4.py`: Synthesis of findings 
- `phase_5.py`: Consolidation and reporting
- `final_analysis.py`: AI tool configuration generation

### AI Provider Interfaces (`core/agents/`)
- `base.py`: BaseArchitect abstract class for model agnosticism
- `anthropic.py`: Anthropic Claude integration
- `openai.py`: OpenAI model integration
- `deepseek.py`: DeepSeek Reasoner integration
- `gemini.py`: Google Gemini integration

### Configuration Management (`config/`)
- `agents.py`: Model configurations and phase assignments
- `exclusions.py`: File/directory filtering patterns
- `prompts/`: Phase-specific prompt templates

### Universal CLI Generator (`cli/`)
- `commands/generate.py`: Multi-tool configuration generator
- `formatters/`: Tool-specific output formatters
- `ui/`: Interactive user interface components

### Context Engineering (`Context-Engineering/`)
- `00_foundations/`: Theoretical underpinnings and concepts
- `60_protocols/`: Protocol shells and schemas
- `cognitive-tools/`: Cognitive architectures and templates

## Critical Issues

### Phase 3 File Retrieval Problem
**URGENT**: Currently experiencing `ClientError` and 0.0% file retrieval success rate in `core/analysis/phase_3.py` for critical agents. This affects:
- AI Concept Architect agent
- Prompt and Agent Developer agent

**Root cause location**: `core/utils/tools/file_retriever.py`

**Debugging approach**:
1. Run `python tests/phase_3_diagnostic_test.py` 
2. Check `tests/phase3_diagnostic_results.json` for detailed error information
3. Examine file access patterns and API rate limiting

## Development Workflow

### Model Configuration
Customize AI models for each phase in `config/agents.py`:

```python
MODEL_CONFIG = {
    "phase1": GEMINI_BASIC,
    "phase2": GEMINI_WITH_REASONING, 
    "phase3": CLAUDE_WITH_REASONING,
    "phase4": O1_HIGH,
    "phase5": DEEPSEEK_REASONER,
    "final": CLAUDE_WITH_REASONING,
}
```

### Adding New AI Providers
1. Create new agent class inheriting from `BaseArchitect` in `core/agents/`
2. Implement required methods: `analyze()`, `create_analysis_plan()`, `synthesize_findings()`, etc.
3. Add configuration in `config/agents.py`
4. Update `core/types/agent_config.py` for type definitions

### Output Structure
Analysis generates comprehensive documentation:
```
your-project/
├── .cursorrules                 # Generated rules for Cursor IDE
├── .cursorignore               # Generated ignore patterns 
├── phases_output/              # Detailed phase outputs
│   ├── phase1_discovery.md     # Initial findings
│   ├── phase2_planning.md      # Agent assignments (XML format)
│   ├── phase3_analysis.md      # Deep analysis results
│   ├── phase4_synthesis.md     # Synthesized insights
│   ├── phase5_consolidation.md # Consolidated report
│   ├── final_analysis.md       # Final recommendations
│   ├── complete_report.md      # Phase overview
│   └── metrics.md              # Performance metrics
```

### API Keys Required
Set up environment variables or `.env` file:
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key'
export OPENAI_API_KEY='your-openai-api-key' 
export DEEPSEEK_API_KEY='your-deepseek-api-key'
export GEMINI_API_KEY='your-gemini-api-key'
```

## Context Engineering Integration

This project implements advanced Context Engineering concepts that treat AI context as dynamic semantic fields rather than static token sequences. Key concepts:

- **Neural Field Dynamics**: Semantic attractors, boundaries, and resonance patterns
- **Quantum Semantics**: Superposition and collapse of meaning interpretations
- **Protocol Shells**: Structured interaction patterns in Pareto-lang format
- **Emergent Intelligence**: Self-monitoring and recursive improvement capabilities

When working with this codebase, understanding these theoretical foundations in `Context-Engineering/00_foundations/` will provide crucial context for the implementation approach.

## Testing Strategy

The project uses comprehensive testing across multiple levels:
- **Unit tests**: Individual phase functionality
- **Integration tests**: Real project analysis
- **Diagnostic tests**: Specific component debugging
- **CI/CD**: GitHub Actions for automated testing

Focus testing efforts on Phase 3 (`core/analysis/phase_3.py`) as it's the most complex component with dynamic agent creation and file processing.