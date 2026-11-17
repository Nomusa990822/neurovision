"""Command-line interface for local dataset provenance and archive tooling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections.abc import Sequence

from neurovision.datasets.archive import inspect_archive, safe_extract_archive
from neurovision.datasets.audit import (
    inventory_files,
    sha256_file,
    write_inventory_csv,
    write_inventory_json,
)
from neurovision.datasets.manifest import create_manifest_template, write_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="neurovision-datasets")
    commands = parser.add_subparsers(dest="command", required=True)

    manifest = commands.add_parser(
        "manifest-template", help="Create an unapproved dataset manifest template"
    )
    manifest.add_argument("--dataset-id", required=True)
    manifest.add_argument("--title", required=True)
    manifest.add_argument("--output", type=Path, required=True)

    digest = commands.add_parser("hash", help="Calculate SHA-256 for a local file")
    digest.add_argument("file", type=Path)

    inspect = commands.add_parser("inspect-archive", help="Inspect archive paths and sizes")
    inspect.add_argument("archive", type=Path)

    extract = commands.add_parser("extract", help="Safely extract a ZIP/TAR archive")
    extract.add_argument("archive", type=Path)
    extract.add_argument("destination", type=Path)
    extract.add_argument("--max-members", type=int, default=200_000)
    extract.add_argument("--max-total-bytes", type=int, default=100 * 1024**3)

    inventory = commands.add_parser("inventory", help="Hash files beneath a directory")
    inventory.add_argument("root", type=Path)
    inventory.add_argument("--output", type=Path, required=True)
    inventory.add_argument("--format", choices=("json", "csv"), default="json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "manifest-template":
        manifest = create_manifest_template(args.dataset_id, args.title)
        write_manifest(args.output, manifest)
        print(f"Created candidate manifest: {args.output}")
    elif args.command == "hash":
        print(f"{sha256_file(args.file)}  {args.file}")
    elif args.command == "inspect-archive":
        members = inspect_archive(args.archive)
        payload = [
            {"name": item.name, "size_bytes": item.size_bytes, "is_directory": item.is_directory}
            for item in members
        ]
        print(json.dumps(payload, indent=2))
    elif args.command == "extract":
        count = safe_extract_archive(
            args.archive,
            args.destination,
            max_members=args.max_members,
            max_total_bytes=args.max_total_bytes,
        )
        print(f"Extracted {count} files to {args.destination}")
    elif args.command == "inventory":
        records = inventory_files(args.root)
        if args.format == "json":
            write_inventory_json(args.output, records)
        else:
            write_inventory_csv(args.output, records)
        print(f"Inventoried {len(records)} files: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
