from __future__ import annotations

from neurovision.datasets.cli import main


def test_cli_hash(capsys, tmp_path) -> None:
    target = tmp_path / "payload.bin"
    target.write_bytes(b"abc")
    assert main(["hash", str(target)]) == 0
    assert "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" in capsys.readouterr().out


def test_cli_manifest_template(tmp_path) -> None:
    target = tmp_path / "octdl.json"
    assert main(["manifest-template", "--dataset-id", "octdl_v4", "--title", "OCTDL", "--output", str(target)]) == 0
    assert '"acquisition_status": "candidate"' in target.read_text()
