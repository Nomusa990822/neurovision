# Dataset Acquisition Tooling

**Status:** WP10 complete and merged. GitHub Actions verification passed in [run #44053030829](https://github.com/Nomusa990822/neurovision/actions/runs/44053030829). The tooling is local-only; it does not download datasets, decode OCT images, establish licence permissions or approve dataset use.

The tooling uses the Python standard library so it can run without OCT data, cloud storage or Codespaces. Invoke it from the repository root with:

```bash
uv run python -m neurovision.datasets --help
```

## Commands

Create a candidate manifest (the command refuses to overwrite an existing file):

```bash
uv run python -m neurovision.datasets manifest-template \
  --dataset-id octdl_v4 --title "OCTDL Mendeley Version 4" \
  --output "$NEUROVISION_DATA_ROOT/manifests/octdl_v4.json"
```

Hash an acquired archive:

```bash
uv run python -m neurovision.datasets hash /path/to/original-archive.zip
```

Inspect archive members before extraction:

```bash
uv run python -m neurovision.datasets inspect-archive /path/to/original-archive.zip
```

Safely extract into a new or empty directory. Defaults limit extraction to 200,000 members and 100 GiB uncompressed size:

```bash
uv run python -m neurovision.datasets extract \
  /path/to/original-archive.zip "$NEUROVISION_DATA_ROOT/interim/octdl_v4"
```

Generate a deterministic per-file inventory with size and SHA-256:

```bash
uv run python -m neurovision.datasets inventory \
  "$NEUROVISION_DATA_ROOT/interim/octdl_v4" \
  --output "$NEUROVISION_DATA_ROOT/manifests/octdl_v4-files.json" --format json
```

Use `--format csv` for CSV output. Reports refuse to overwrite existing files; choose a new report path for a new run.

## Safety boundaries

- The original archive is never modified by these commands.
- Extraction rejects absolute paths, parent traversal, symbolic links and TAR special files.
- Extraction enforces configurable member-count and uncompressed-size limits, including a streaming byte limit during extraction.
- Destination must be empty to avoid accidental mixing of releases.
- Inventory skips symbolic links and records relative paths, file sizes, suffixes and SHA-256 hashes.
- The inventory does not decode image formats, inspect image dimensions, identify near-duplicates or reconcile labels/patient IDs. Those are subsequent audit work packages.
- Do not run acquisition/extraction inside the Git checkout. Keep raw and extracted data outside Git and public CI artifacts.
- Do not include patient identifiers in published inventory reports unless the data governance decision explicitly permits it.

## Verification

WP10 CI passed:
- 29 unit tests.
- Ruff lint and formatting.
- Strict mypy.
- Wheel and source distribution build.
- Docker image build and non-root runtime smoke test.

The overall statement coverage is 79% for the expanded package at this stage. Archive edge cases and CLI branches still have untested paths; this is a test-coverage observation, not a quality or clinical-performance metric. Synthetic tests do not access real OCT data and do not establish dataset suitability.
