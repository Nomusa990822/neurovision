from __future__ import annotations

import hashlib

from neurovision.datasets.audit import inventory_files, sha256_file, write_inventory_csv, write_inventory_json


def test_sha256_file_matches_known_digest(tmp_path) -> None:
    target = tmp_path / "sample.bin"
    target.write_bytes(b"neurovision")
    assert sha256_file(target) == hashlib.sha256(b"neurovision").hexdigest()


def test_inventory_is_sorted_and_excludes_symlinks(tmp_path) -> None:
    root = tmp_path / "data"
    root.mkdir()
    (root / "b.bin").write_bytes(b"b")
    (root / "a.bin").write_bytes(b"a")
    (root / "ignored.tmp").write_bytes(b"x")
    (root / "link.bin").symlink_to(root / "a.bin")
    records = inventory_files(root, exclude_names={"ignored.tmp"})
    assert [record.relative_path for record in records] == ["a.bin", "b.bin"]


def test_inventory_reports_hash_size_and_suffix(tmp_path) -> None:
    (tmp_path / "scan.TIF").write_bytes(b"oct")
    record = inventory_files(tmp_path)[0]
    assert record.size_bytes == 3
    assert record.suffix == ".tif"
    assert record.sha256 == hashlib.sha256(b"oct").hexdigest()


def test_inventory_writers_do_not_overwrite(tmp_path) -> None:
    records = inventory_files(tmp_path)
    json_path = tmp_path / "inventory.json"
    csv_path = tmp_path / "inventory.csv"
    write_inventory_json(json_path, records)
    write_inventory_csv(csv_path, records)
    assert json_path.exists() and csv_path.exists()
    for writer, path in ((write_inventory_json, json_path), (write_inventory_csv, csv_path)):
        try:
            writer(path, records)
        except FileExistsError:
            pass
        else:
            raise AssertionError("Existing inventory must not be overwritten")
