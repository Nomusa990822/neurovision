# Dataset Acquisition Tooling

**Status:** WP10 implementation candidate; local-only tooling. It does not download datasets, decode images, establish licence permissions or approve dataset use.

The tooling uses the Python standard library so it can run without OCT data, cloud storage or Codespaces. Invoke it from the repository root with:

```bash
uv run python -m neurovision.datasets.cli --help
```

## Commands

Create a candidate manifest (the command refuses to overwrite an existing file):

```bash
uv run python -m neurovision.datasets.cli manifest-template \\
  --dataset-id octdl_v4 --title "OCTDL Mendeley Version 4" \\
  --output "$NEUROVISION_DATA_ROOT/manifests/octdl_v4.json"
```

Hash an acquired archive:

```bash
uv run python -m neurovision.datasets.cli hash /path/to/original-archive.zip
```

Inspect archive members before extraction:

```bash
uv run python -m neurovision.datasets.cli inspect-archive /path/to/original-archive.zip
```

Safely extract into a new or empty directory. Defaults limit extraction to 200,000 members and 100 GiB uncompressed size:

```bash
uv run python -m neurovision.datasets.cli extract \\
  /path/to/original-archive.zip "$NEUROVISION_DATA_ROOT/interim/octdl_v4"
```

Generate a deterministic per-file inventory with size and SHA-256:

```bash
uv run python -m neurovision.datasets.cli inventory \\
  "$NEUROVISION_DATA_ROOT/interim/octdl_v4" \\
  --output "$NEUROVISION_DATA_ROOT/manifests/octdl_v4-files.json" --format json
```

Use `--format csv` for CSV output. Reports refuse to overwrite existing files; choose a new report path for a new run.

## Safety boundaries

- The original archive is never modified by these commands.
- Extraction rejects absolute paths, parent traversal, symbolic links and TAR special files.
- Extraction enforces configurable member-count and uncompressed-size limits.
- Destination must be empty to avoid accidental mixing of releases.
- Inventory skips symbolic links and records relative paths, file sizes, suffixes and SHA-256 hashes.
- The inventory does not decode image formats, inspect image dimensions, identify near-duplicates or reconcile labels/patient IDs. Those are subsequent audit work packages.
- Do not run acquisition/extraction inside the Git checkout. Keep raw and extracted data outside Git and public CI artifacts.
- Do not include patient identifiers in published inventory reports unless the data governance decision explicitly permits it.

## Verification

Synthetic tests exercise hashing, deterministic inventory, no-overwrite behavior, ZIP traversal rejection, TAR special-file rejection, extraction limits, manifest validation and CLI behavior. These tests do not access real OCT data and do not establish dataset suitability.
