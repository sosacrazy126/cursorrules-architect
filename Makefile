# CursorRules Architect - Root Makefile
# This is a convenience wrapper that delegates to scripts/Makefile

.PHONY: help install install-dev test lint format clean build docs demo validate-config dev-setup

# Default target
help:
	@make -f scripts/Makefile help

# Delegate all targets to scripts/Makefile
install install-dev test test-fast lint format clean build docs migrate demo validate-config dev-setup:
	@make -f scripts/Makefile $@

# Additional convenience targets
setup: install-dev  ## Alias for install-dev
	@echo "✅ Development setup complete!"

check: lint test  ## Run both linting and tests
	@echo "✅ All checks passed!"
