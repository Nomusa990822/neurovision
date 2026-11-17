from __future__ import annotations

from neurovision.datasets.manifest import create_manifest_template, validate_manifest, write_manifest


def test_template_is_candidate_and_unacquired() -> None:
    manifest = create_manifest_template("octdl_v4", "OCTDL")
    assert manifest["acquisition_status"] == "candidate"
    assert manifest["archive_sha256"] is None
    assert validate_manifest(manifest) == []


def test_manifest_requires_acquisition_evidence_after_acquisition() -> None:
    manifest = create_manifest_template("octdl_v4", "OCTDL")
    manifest["acquisition_status"] = "acquired"
    errors = validate_manifest(manifest)
    assert any("archive_sha256" in error for error in errors)
    assert any("acquired_at_utc" in error for error in errors)


def test_manifest_rejects_invalid_digest() -> None:
    manifest = create_manifest_template("octdl_v4", "OCTDL")
    manifest["archive_sha256"] = "not-a-hash"
    assert any("SHA-256" in error for error in validate_manifest(manifest))


def test_write_manifest_refuses_overwrite(tmp_path) -> None:
    manifest = create_manifest_template("octdl_v4", "OCTDL")
    target = tmp_path / "manifest.json"
    write_manifest(target, manifest)
    try:
        write_manifest(target, manifest)
    except FileExistsError:
        pass
    else:
        raise AssertionError("Existing manifest should not be overwritten")
