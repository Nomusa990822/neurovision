# NeuroVision Development Setup

The Python 3.12 development environment is locked and verified by the GitHub Actions workflow at `.github/workflows/python-quality.yml`.

## Requirements

- Python 3.12.
- uv.
- Git.

## Create or synchronise the environment

From the repository root:

```bash
uv sync --locked --all-groups
```

The committed `uv.lock` records the resolved development dependency graph. Use `--locked` so uv fails rather than silently changing the lockfile during environment setup.

## Quality and reproducibility commands

```bash
uv lock --check --python 3.12
uv sync --locked --all-groups
uv run pytest --cov=neurovision --cov-report=term-missing
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv build
```

These checks run on GitHub-hosted Ubuntu runners for pull requests and pushes to `main`. The workflow uses Python 3.12, verifies the committed lockfile, installs the locked environment, runs the test and quality gates, and builds both wheel and source distributions.

## Configuration

Copy `.env.example` to `.env` for local overrides. The current standard-library settings layer recognises:

| Variable | Default | Accepted values |
|---|---|---|
| `NEUROVISION_ENVIRONMENT` | `development` | development, testing, production |
| `NEUROVISION_LOG_LEVEL` | `INFO` | CRITICAL, ERROR, WARNING, INFO, DEBUG |
| `NEUROVISION_DATA_DIR` | `data` | Non-empty filesystem path |

Do not place secrets, patient identifiers or private dataset paths in `.env.example`, source control, test output or logs. Raw datasets and generated artefacts must remain outside Git.

## Current scaffold boundaries

The initial package contains package metadata, immutable settings implemented with standard-library dataclasses, path resolution and a Python random-seed helper. It does not yet implement dataset ingestion, image processing, models, training, calibration, explainability, uncertainty estimation, API routes or database access.

The Docker baseline is still pending and will be delivered under WP08.
