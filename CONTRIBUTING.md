
# Contributing to CursorRules Architect

Thank you for considering contributing to CursorRules Architect! Your help is greatly appreciated. This guide explains how you can contribute to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Changes](#submitting-changes)
    - [Git Workflow](#git-workflow)
    - [Code Standards](#code-standards)
    - [Commit Messages](#commit-messages)
    - [Pull Request Guidelines](#pull-request-guidelines)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Installing Dependencies](#installing-dependencies)
  - [Setting Up API Keys](#setting-up-api-keys)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Important Notes](#important-notes)
  - [Fixed Models](#fixed-models)
  - [Model Usage Restrictions](#model-usage-restrictions)

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful and considerate in all interactions.

## Getting Started

To get started with development, you'll need to set up your local environment.

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key with access to `o1`
- An Anthropic API key with access to `claude-3-7-sonnet-20250219`
- Git

### Installing Dependencies

Clone the repository:

```bash
git clone https://github.com/SlyyCooper/cursorrules-architect.git
cd cursorrules-architect
```

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Setting Up API Keys

Set your API keys as environment variables:

```bash
# Linux/macOS
export OPENAI_API_KEY='your-openai-api-key'
export ANTHROPIC_API_KEY='your-anthropic-api-key'

# Windows Command Prompt
set OPENAI_API_KEY=your-openai-api-key
set ANTHROPIC_API_KEY=your-anthropic-api-key

# Windows PowerShell
$env:OPENAI_API_KEY='your-openai-api-key'
$env:ANTHROPIC_API_KEY='your-anthropic-api-key'
```

**Important:** Ensure that your API keys have access to the required models (`o1` for OpenAI and `claude-3-7-sonnet-20250219` for Anthropic).

## How to Contribute

Contributions can be in the form of bug reports, feature suggestions, or code changes.

### Reporting Bugs

If you encounter any bugs, please open an issue on GitHub with detailed information:

- Steps to reproduce the issue
- Expected and actual results
- Any relevant error messages or logs
- Your environment details (OS, Python version, package versions)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:

- A clear and descriptive title
- A detailed description of the feature
- Any proposed implementation details

### Submitting Changes

#### Git Workflow

1. **Fork the Repository** on GitHub.
2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/SlyyCooper/cursorrules-architect.git
   cd cursorrules-architect
   ```

3. **Create a Feature Branch**:

   ```bash
   git checkout -b feature/YourFeature
   ```

4. **Make Your Changes** and commit them.

5. **Push to Your Branch**:

   ```bash
   git push origin feature/YourFeature
   ```

6. **Open a Pull Request** on the original repository.

#### Code Standards

- **Python Style**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.
- **Typing**: Use type hints where appropriate.
- **Imports**: Organize imports according to [PEP 8](https://www.python.org/dev/peps/pep-0008/#imports).
- **Documentation**: Include docstrings for functions, classes, and modules.

#### Commit Messages

- Use descriptive commit messages.
- Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification when possible.

#### Pull Request Guidelines

- Ensure your code passes all tests.
- Address any merge conflicts.
- Provide a clear description of your changes in the pull request.

## Development Setup

### Running the Project

You can run the main script using:

```bash
python main.py -p /path/to/your/project
```

Replace `/path/to/your/project` with the path to the project you want to analyze.

### Testing

At this time, unit tests are not implemented. If you contribute tests, please include instructions on how to run them.

## Questions?

If you have any questions or need assistance, feel free to open an issue or reach out to the maintainers.

We look forward to your contributions!


