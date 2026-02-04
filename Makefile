# Makefile for the Chimera Project

# --- Variables ---
# Determines the Python interpreter.
PYTHON_INTERPRETER := $(shell command -v python3 || command -v python)
# Directory for the virtual environment.
VENV_DIR := venv
# Docker image name and tag.
IMAGE_NAME := chimera-agent-factory
IMAGE_TAG := latest

# --- Phony Targets ---
# Declares targets that are not actual files, preventing conflicts.
.PHONY: all help setup test test-local spec-check docker-build docker-test clean

# --- Main Targets ---

# Default target: Display the help message.
all: help

# help: Shows a list of available commands and their descriptions.
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo "  setup         Initializes the local development environment."
	@echo "  test          Builds the Docker image and runs tests inside the container."
	@echo "  test-local    Runs tests using the local Python environment."
	@echo "  spec-check    Validates the project's specification files and structure."
	@echo "  docker-build  Builds the Docker image."
	@echo "  docker-test   Runs tests inside a pre-built Docker container."
	@echo "  clean         Removes temporary files and the virtual environment."
	@echo "  help          Displays this help message."

# setup: Creates a virtual environment and installs dependencies.
# Prefers 'uv' for speed, but falls back to 'pip' if 'uv' is not available.
setup:
	@echo "--> Setting up local development environment..."
	@if command -v uv >/dev/null; then \
		echo "--> 'uv' found. Using uv for setup."; \
		uv venv $(VENV_DIR) && uv pip install -r pyproject.toml; \
	else \
		echo "--> 'uv' not found. Falling back to standard venv and pip."; \
		$(PYTHON_INTERPRETER) -m venv $(VENV_DIR) && \
		. $(VENV_DIR)/bin/activate && \
		pip install -r pyproject.toml; \
	fi
	@echo "--> Setup complete. Activate the environment with: source $(VENV_DIR)/bin/activate"

# test-local: Runs the pytest suite in the local environment.
test-local:
	@echo "--> Running tests locally..."
	@$(PYTHON_INTERPRETER) -m pytest

# spec-check: Executes the script to validate project specifications.
spec-check:
	@echo "--> Validating project specifications..."
	@$(PYTHON_INTERPRETER) scripts/spec_check.py

# --- Docker Targets ---

# docker-build: Builds the main Docker image for the project.
docker-build:
	@echo "--> Building Docker image: $(IMAGE_NAME):$(IMAGE_TAG)..."
	@docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

# docker-test: Runs the test suite within a new Docker container.
docker-test:
	@echo "--> Running tests inside Docker container..."
	@docker run --rm $(IMAGE_NAME):$(IMAGE_TAG)

# test: The primary test command for CI. It builds the image and runs tests inside it.
test: docker-build docker-test

# --- Utility Targets ---

# clean: Removes the virtual environment and Python cache files.
clean:
	@echo "--> Cleaning up project artifacts..."
	@rm -rf $(VENV_DIR) .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "--> Cleanup complete."
