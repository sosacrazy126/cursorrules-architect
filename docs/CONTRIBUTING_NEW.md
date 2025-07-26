# Contributing to CursorRules Architect

Thank you for your interest in contributing to CursorRules Architect! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- A text editor or IDE

### Setting Up Your Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/cursorrules-architect.git
   cd cursorrules-architect
   ```

2. **Install Development Dependencies**
   ```bash
   make install-dev
   ```
   
   This will:
   - Install the package in development mode
   - Install all development dependencies
   - Set up pre-commit hooks

3. **Set Up API Keys**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Verify Installation**
   ```bash
   make test
   cursorrules-architect --help
   ```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking

Run all checks:
```bash
make check
```

Format code:
```bash
make format
```

### Testing

We use pytest for testing. Tests are organized into:

- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for full workflows
- `tests/fixtures/` - Test data and fixtures

Run tests:
```bash
# All tests
make test

# Specific test file
pytest tests/unit/test_config.py

# With coverage
pytest --cov=src/cursorrules_architect
```

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   make check
   make test
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test changes
   - `refactor:` for code refactoring

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Project Structure

```
cursorrules-architect/
├── src/cursorrules_architect/    # Main package
│   ├── cli/                      # Command-line interface
│   ├── config/                   # Configuration management
│   ├── core/                     # Core analysis engine
│   │   ├── analysis/             # Analysis pipeline
│   │   └── agents/               # AI agent implementations
│   └── utils/                    # Utility modules
├── tests/                        # Test suite
├── docs/                         # Documentation
├── scripts/                      # Development scripts
└── examples/                     # Usage examples
```

## Adding New Features

### Adding a New AI Provider

1. Create agent implementation in `src/cursorrules_architect/core/agents/`
2. Add provider to `AgentProvider` enum in `config/models.py`
3. Update factory in `core/agents/factory.py`
4. Add tests in `tests/unit/test_agents.py`
5. Update documentation

### Adding New Analysis Phases

1. Create phase implementation in `src/cursorrules_architect/core/analysis/phases/`
2. Update `ProjectAnalyzer` to include new phase
3. Add phase configuration options
4. Add comprehensive tests
5. Update documentation

### Adding New Output Formats

1. Extend `OutputGenerator` in `utils/output_generation/`
2. Add format-specific templates
3. Update configuration options
4. Add tests for new format
5. Update CLI help and documentation

## Testing Guidelines

### Unit Tests

- Test individual functions and classes in isolation
- Use mocks for external dependencies (API calls, file system)
- Aim for high coverage of core functionality

### Integration Tests

- Test complete workflows end-to-end
- Use real file systems but mock API calls
- Test error handling and edge cases

### Test Data

- Keep test data minimal and focused
- Use fixtures for reusable test data
- Don't commit large test files

## Documentation

### Code Documentation

- Use clear, descriptive docstrings
- Include type hints for all functions
- Document complex algorithms and business logic

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Keep documentation up-to-date with code changes

## Release Process

1. **Update Version**
   - Update version in `pyproject.toml`
   - Update `__version__` in `src/cursorrules_architect/__init__.py`

2. **Update Changelog**
   - Add new version section to `CHANGELOG.md`
   - List all significant changes

3. **Create Release**
   - Tag the release: `git tag v2.0.0`
   - Push tags: `git push --tags`
   - Create GitHub release with changelog

## Getting Help

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Discord**: Join our community Discord (link in README)

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## License

By contributing to CursorRules Architect, you agree that your contributions will be licensed under the MIT License.
