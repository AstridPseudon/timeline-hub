"""Uninstall also accounts for a bootstrap outside a custom program folder."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from astrid.installer.backend import Backend
from astrid.installer.core import write_json
from astrid.installer.service import LABEL, default_program_root


def installation(tmp_path, monkeypatch):
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg-data"))
    root, data = tmp_path / "custom program", tmp_path / "workspace"
    data.mkdir()
    (data / "sentinel").write_text("keep")
    write_json(root / "install.json", {"owner": LABEL, "data_root": str(data)})
    if os.name == "nt":
        monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local-app-data"))
    bootstrap = default_program_root(home, sys.platform) / "bootstrap"
    bootstrap.mkdir(parents=True)
    uv = bootstrap / ("uv.exe" if os.name == "nt" else "uv")
    uv.write_text("installer-owned bootstrap")
    return Backend(root, tmp_path / "log", uv), root, data, bootstrap


def test_custom_root_uninstall_removes_default_bootstrap_and_keeps_data(tmp_path, monkeypatch):
    backend, root, data, bootstrap = installation(tmp_path, monkeypatch)

    assert backend.remove(root, data, delete_data=False) == []

    assert not root.exists()
    assert not bootstrap.exists()
    assert (data / "sentinel").read_text() == "keep"


def test_custom_root_reports_locked_default_bootstrap(tmp_path, monkeypatch):
    backend, root, data, bootstrap = installation(tmp_path, monkeypatch)
    remove_tree = shutil.rmtree

    def remove(path, *args, **kwargs):
        if Path(path) == bootstrap:
            raise PermissionError("running bootstrap is locked")
        return remove_tree(path, *args, **kwargs)

    monkeypatch.setattr(shutil, "rmtree", remove)

    assert backend.remove(root, data, delete_data=False) == [bootstrap]
    assert not root.exists()
    assert bootstrap.is_dir()
    assert (data / "sentinel").read_text() == "keep"


def test_custom_root_does_not_remove_a_linked_bootstrap(tmp_path, monkeypatch):
    backend, root, data, bootstrap = installation(tmp_path, monkeypatch)
    external = tmp_path / "external"
    external.mkdir()
    (external / "sentinel").write_text("keep")
    shutil.rmtree(bootstrap)
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", str(bootstrap), str(external)],
                       check=True, capture_output=True, text=True)
    else:
        bootstrap.symlink_to(external, target_is_directory=True)

    assert backend.remove(root, data, delete_data=False) == [bootstrap]
    assert (external / "sentinel").read_text() == "keep"
    assert (data / "sentinel").read_text() == "keep"


def test_custom_uv_does_not_authorize_removing_default_bootstrap(tmp_path, monkeypatch):
    backend, root, data, bootstrap = installation(tmp_path, monkeypatch)
    backend.uv = tmp_path / "other-tools" / "uv"

    assert backend.remove(root, data, delete_data=False) == []
    assert bootstrap.is_dir()
    assert (data / "sentinel").read_text() == "keep"
