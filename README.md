# Project Chimera: The Agentic OS

[![Chimera CI - Build and Test](https://github.com/dagiteferi/chimera-os/actions/workflows/main.yml/badge.svg)](https://github.com/dagiteferi/chimera-os/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)

**Project Chimera** is the foundational infrastructure for an autonomous AI influencer network. This repository contains the "Agentic Operating System" designed to manage a fleet of AI agents that can research trends, generate content, and manage engagement without direct human intervention for every action.

This project is built with a **Spec-Driven Development (SDD)** philosophy. The `specs/` directory is the source of truth, and all development is guided by these formal requirements.

---

## Repository Structure

Understanding the directory structure is key to understanding the project.

-   `specs/`: **(Start Here)** The specification directory. It contains the functional and technical blueprints for the entire system. All development work is derived from these documents.
-   `research/`: Contains the high-level domain research, architectural strategy, and tooling decisions. Read this directory to understand the "why" behind the technical choices made in the `specs/` directory.
-   `skills/`: Defines the agent's capabilities (e.g., `trend_fetcher`, `content_generator`). Each skill has a defined input/output schema that acts as its API.
-   `tests/`: Contains the automated test suite. This project uses a Test-Driven Development (TDD) approach, meaning tests are written *before* the implementation.
-   `scripts/`: Includes utility scripts, such as the `spec_check.py` script for validating the project's structure against the specifications.
-   `.github/workflows/`: Contains the CI/CD pipeline, which automatically runs tests on every push and pull request.
-   `Dockerfile` & `Makefile`: The core of the project's containerization and automation, used for creating a consistent development and testing environment.

## Getting Started

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started)
-   [Make](https://www.gnu.org/software/make/)
-   Python 3.11+ (for local setup)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dagiteferi/chimera-os.git
    cd chimera-os
    ```

2.  **Set up the local environment:**
    This command creates a Python virtual environment and installs the dependencies listed in `pyproject.toml`. It prefers `uv` for speed but will fall back to `pip` if `uv` is not installed.
    ```bash
    make setup
    ```

## How to Run & Test with Docker

This project uses Docker to ensure a clean, consistent, and reliable testing environment. The primary way to run the project's test suite is via the `Makefile`.

**To run the tests:**

```bash
make test
```

**What this command does:**

1.  It builds a Docker image from the `Dockerfile`, installing all necessary dependencies in a clean environment.
2.  It runs the project's test suite (using `pytest`) inside a new container created from that image.

### Important: Expect Test Failures

This project follows a **Test-Driven Development (TDD)** methodology. The tests in the `tests/` directory have been written *before* the full implementation of the skills.

Therefore, when you run `make test`, you should expect to see **failing tests**. This is the correct and desired outcome at this stage. These failures define the "empty slots" that need to be filled by implementing the agent skills according to the project's specifications.

## CI/CD Pipeline

This repository is equipped with a GitHub Actions workflow defined in `.github/workflows/main.yml`. This pipeline automatically runs the `make test` command on every push and pull request to the `main` branch, ensuring that all changes are continuously validated against the test suite.
## for more short video 
```bash
(https://www.youtube.com/watch?v=7_elo03jjq4)
```


## for more short video

```bash
https://www.youtube.com/watch?v=7_elo03jjq4)
```
---
