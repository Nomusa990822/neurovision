# NeuroVision Development Setup

> This guide describes the initial package scaffold. A committed dependency lock and CI verification are still pending; do not treat this as a fully reproducible release environment until those gates pass.

## Requirements

- Python 3.12.
- uv (use the version selected by the project maintainers).
- Git.

## Create the environment

From the repository root:

```bash
uv sync --all-groups
```

Until `uv.lock` is committed, this command resolves the declared dependency ranges and is not yet guaranteed to reproduce an identical environment. Once the lockfile is added, use:

```bash
uv sync --locked --all-groups
```

## Quality commands

```bash
uv run pytest
uv run pytest --cov=neurovision --cov-report=term-missing
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

## Package build

```bash
uv build
```

## Configuration

Copy `.env.example` to `.env` for local overrides. The current standard-library settings layer recognises:

| Variable | Default | Accepted values |
|---|---|---|
| `NEUROVISION_ENVIRONMENT` | `development` | development, testing, production |
| `NEUROVISION_LOG_LEVEL` | `INFO` | CRITICAL, ERROR, WARNING, INFO, DEBUG |
| `NEUROVISION_DATA_DIR` | `data` | Non-empty filesystem path |

Do not place secrets, patient identifiers or private dataset paths in `.env.example`, source control, test output or logs. Raw datasets and generated artefacts must remain outside Git.

## Current scaffold boundaries

The initial package contains package metadata, immutable settings, path resolution and a Python random-seed helper. It does not yet implement dataset ingestion, image processing, models, training, calibration, explainability, uncertainty estimation, API routes or database access.
