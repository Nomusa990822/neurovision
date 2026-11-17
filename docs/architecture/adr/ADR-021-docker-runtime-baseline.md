# ADR-021: Minimal non-root Docker runtime baseline

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owners:** NeuroVision project owner and engineering team

## Context

WP08 requires a repeatable container build without prematurely introducing an API server, database, model runtime or dataset. The Python package and locked dependency graph are already verified on Python 3.12 through GitHub Actions.

## Decision

- Use the official Python 3.12 slim Bookworm runtime image.
- Copy the pinned uv CLI from the uv 0.10.0 image and install the project using the committed lockfile with `uv sync --locked --no-dev`.
- Run as a dedicated unprivileged user with UID 10001.
- Provide an application-owned `/app/data` directory for future mounted data workflows.
- Exclude datasets, model artefacts, local environments, credentials and development-only files from the Docker build context.
- Use a package-import smoke command as the default container command until a real service entrypoint exists.
- Build and execute the image in GitHub Actions after the Python quality job.

## Consequences

The image is intentionally small in scope and does not expose a network service. It provides a reproducible packaging and non-root execution baseline. A future API or worker service must define its own lifecycle, health endpoint, secrets handling, persistent storage and deployment-specific security controls before changing the container entrypoint.

## Alternatives considered

- **Full API container now:** rejected because no API exists and introducing one here would expand scope without a validated inference contract.
- **Root runtime:** rejected because it is unnecessary for the current package and weakens the default security posture.
- **Copy datasets into the image:** rejected because datasets require separate provenance, licence, privacy and versioning controls.
