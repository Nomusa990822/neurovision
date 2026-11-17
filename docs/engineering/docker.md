# NeuroVision Docker Baseline

## Purpose and scope

The Docker image packages the current Python research scaffold in a reproducible, minimal runtime. It is an engineering baseline, not a deployed inference service. The image does not contain OCT datasets, model checkpoints, training code, an API server or a database.

## Build

From the repository root, with Docker Engine available:

```bash
docker build --pull -t neurovision:0.1.0 .
```

The build uses Python 3.12 slim and the committed `uv.lock`. Runtime dependencies are installed with `uv sync --locked --no-dev`; development tools and tests are excluded from the image.

## Run the container smoke command

```bash
docker run --rm neurovision:0.1.0
```

Expected output:

```text
NeuroVision 0.1.0 container ready
```

The default command is deliberately a short package-import smoke check. It exits after verifying that the package is available; it is not a long-running service.

## Runtime identity and writable data directory

The image runs as the unprivileged `neurovision` user (UID 10001), not root. Its configured data directory is `/app/data`, owned by that user.

Verify the runtime identity and write permission:

```bash
docker run --rm --entrypoint python neurovision:0.1.0 -c "import os; from pathlib import Path; assert os.getuid() == 10001; p = Path('/app/data/.write-check'); p.write_text('ok'); p.unlink(); print('non-root identity and data write check passed')"
```

## Data handling

Do not copy OCT datasets, patient metadata, model weights, credentials or local environment files into the image. The root `.dockerignore` excludes the local data, model, experiment and environment paths from the build context. When a future workflow needs data, mount an approved external path or use an explicitly governed data-access mechanism; do not bake datasets into an image.

## CI verification

The GitHub Actions workflow builds the image and runs it as a container smoke test after Python quality checks pass. The CI check also verifies the configured production environment, non-root UID and writable data directory.

## Limitations

This baseline does not claim production readiness, vulnerability-free dependencies, clinical suitability or inference performance. Image scanning, SBOM generation, runtime hardening and service orchestration can be added when the application runtime and deployment threat model are defined.
