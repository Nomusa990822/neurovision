from __future__ import annotations

import pytest

from neurovision.datasets.image_paths import build_image_index, resolve_image_path


def test_resolves_extensionless_manifest_stem(tmp_path) -> None:
    root = tmp_path / "images"
    nested = root / "AMD"
    nested.mkdir(parents=True)
    image = nested / "amd_sample_01.jpg"
    image.write_bytes(b"image")

    index = build_image_index(root)

    assert resolve_image_path("amd_sample_01", root, index) == image.resolve()


def test_prefers_exact_filename_when_stems_collide(tmp_path) -> None:
    root = tmp_path / "images"
    root.mkdir()
    jpg = root / "sample.jpg"
    png = root / "sample.png"
    jpg.write_bytes(b"jpg")
    png.write_bytes(b"png")

    index = build_image_index(root)

    assert resolve_image_path("sample.jpg", root, index) == jpg.resolve()


def test_rejects_ambiguous_extensionless_stem(tmp_path) -> None:
    root = tmp_path / "images"
    root.mkdir()
    (root / "sample.jpg").write_bytes(b"jpg")
    (root / "sample.png").write_bytes(b"png")

    index = build_image_index(root)

    with pytest.raises(FileNotFoundError, match="missing or ambiguous"):
        resolve_image_path("sample", root, index)


def test_rejects_parent_traversal(tmp_path) -> None:
    root = tmp_path / "images"
    root.mkdir()
    index = build_image_index(root)

    with pytest.raises(ValueError, match="Unsafe"):
        resolve_image_path("../outside.jpg", root, index)
