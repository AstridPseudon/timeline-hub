"""Public command recovery after a partial program removal."""

import os
import subprocess
from unittest.mock import Mock

import pytest

from astrid.installer import cli
from astrid.installer.core import Version, current, write_json
from astrid.installer.service import LABEL


def test_partial_uninstall_can_finish_after_version_metadata_was_removed(tmp_path, monkeypatch):
    from runtime_protocol import platform

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local-app-data"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg-data"))
    monkeypatch.setattr(platform, "log_dir", lambda: tmp_path / "logs")
    root, data = tmp_path / "program", tmp_path / "workspace"
    write_json(root / "install.json", {"owner": LABEL, "data_root": str(data)})
    (root / "current").write_text("removed-version\n")
    backend = Mock()
    backend.service.recorded.return_value = {
        "owner": LABEL, "program_root": str(root),
        "data_root": str(data), "uninstalled": True,
    }
    backend.existing.return_value = None
    backend.remove.return_value = []
    monkeypatch.setattr(cli, "Backend", Mock(return_value=backend))

    assert cli.main(["--root", str(root), "--uninstall"]) == 0
    backend.stop.assert_called_once_with(None, data)
    backend.unregister.assert_called_once_with()
    backend.remove.assert_called_once_with(root, data, delete_data=False)


@pytest.mark.parametrize("entry", ["versions", "version"])
def test_absent_version_record_does_not_allow_linked_parents(tmp_path, entry):
    root, external = tmp_path / "program", tmp_path / "external"
    root.mkdir()
    external.mkdir()
    sentinel = external / "keep.txt"
    sentinel.write_text("keep")
    (root / "current").write_text("removed-version\n")
    if entry == "versions":
        link = root / "versions"
    else:
        (root / "versions").mkdir()
        link = root / "versions/removed-version"
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(external)],
                       check=True, capture_output=True, text=True)
    else:
        link.symlink_to(external, target_is_directory=True)

    with pytest.raises(ValueError, match="cannot contain links"):
        current(root)

    assert list(external.iterdir()) == [sentinel]
    assert sentinel.read_text() == "keep"


def test_present_malformed_version_record_is_not_treated_as_removed(tmp_path):
    write_json(tmp_path / "install.json", {"owner": LABEL})
    (tmp_path / "current").write_text("v1\n")
    record = tmp_path / "versions/v1/version.json"
    record.parent.mkdir(parents=True)
    record.write_text("[]")

    with pytest.raises(ValueError, match="Expected an object"):
        current(tmp_path)


def test_current_version_identifier_cannot_escape_program_root(tmp_path):
    (tmp_path / "current").write_text("../external\n")

    with pytest.raises(ValueError, match="Invalid installation version identifier"):
        current(tmp_path)


def test_current_record_cannot_point_outside_managed_versions(tmp_path):
    root, external = tmp_path / "program", tmp_path / "external"
    record = root / "versions/v1/version.json"
    version = Version(external, external / "bin/python", external / "profile.json", {})
    write_json(record, version.document())
    (root / "current").write_text("v1\n")

    with pytest.raises(ValueError, match="points outside the managed directory"):
        current(root)
