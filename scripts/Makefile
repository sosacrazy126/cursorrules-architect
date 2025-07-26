# CursorRules Architect - Development Makefile
# Note: Run this from the project root directory

.PHONY: help install install-dev test lint format clean build docs

# Get the project root directory (parent of scripts directory)
PROJECT_ROOT := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

help:  ## Show this help message
	@echo "CursorRules Architect - Development Commands"
	@echo "==========================================="
	@echo "Note: Run 'make -f scripts/Makefile <target>' from project root"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	cd $(PROJECT_ROOT) && pip install -e .

install-dev:  ## Install package with development dependencies
	cd $(PROJECT_ROOT) && pip install -e .[dev]
	cd $(PROJECT_ROOT) && pre-commit install

test:  ## Run tests
	cd $(PROJECT_ROOT) && pytest tests/ -v --cov=src/cursorrules_architect --cov-report=term-missing

test-fast:  ## Run tests without coverage
	cd $(PROJECT_ROOT) && pytest tests/ -v

lint:  ## Run linting checks
	cd $(PROJECT_ROOT) && flake8 src/ tests/
	cd $(PROJECT_ROOT) && mypy src/cursorrules_architect/
	cd $(PROJECT_ROOT) && black --check src/ tests/
	cd $(PROJECT_ROOT) && isort --check-only src/ tests/

format:  ## Format code
	cd $(PROJECT_ROOT) && black src/ tests/
	cd $(PROJECT_ROOT) && isort src/ tests/

clean:  ## Clean build artifacts
	cd $(PROJECT_ROOT) && rm -rf build/
	cd $(PROJECT_ROOT) && rm -rf dist/
	cd $(PROJECT_ROOT) && rm -rf *.egg-info/
	cd $(PROJECT_ROOT) && rm -rf .pytest_cache/
	cd $(PROJECT_ROOT) && rm -rf .coverage
	cd $(PROJECT_ROOT) && rm -rf htmlcov/
	cd $(PROJECT_ROOT) && rm -rf analysis_memory.db
	cd $(PROJECT_ROOT) && rm -rf analysis_memory.json
	cd $(PROJECT_ROOT) && find . -type d -name __pycache__ -exec rm -rf {} +
	cd $(PROJECT_ROOT) && find . -type f -name "*.pyc" -delete

build:  ## Build package
	cd $(PROJECT_ROOT) && python -m build

docs:  ## Generate documentation
	@echo "Documentation generation not yet implemented"

migrate:  ## Migrate from old structure
	cd $(PROJECT_ROOT) && python scripts/migrate_to_new_structure.py

demo:  ## Run demo analysis on current project
	cd $(PROJECT_ROOT) && cursorrules-architect generate . --tool cursor

validate-config:  ## Validate current configuration
	cd $(PROJECT_ROOT) && cursorrules-architect validate .cursorrules

# Development shortcuts
dev-setup: install-dev  ## Complete development setup
	@echo "✅ Development environment ready!"
	@echo "Run 'make demo' to test the installation"

check: lint test  ## Run all checks (lint + test)

release-check: clean lint test build  ## Pre-release checks
	@echo "✅ Ready for release!"
