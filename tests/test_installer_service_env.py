"""The login owner reads its settings without depending on a shell profile."""

import json
import sys
from types import ModuleType
from unittest.mock import Mock

import pytest

from astrid.installer.backend import Backend
from astrid.installer.core import Version, read_json, write_json
from astrid.installer.service import LABEL, Service, command, default_program_root


def test_service_wrapper_loads_settings_before_runtime(tmp_path, monkeypatch):
    settings = tmp_path / "service-env.json"
    write_json(settings, {"ASTRID_WARM_IDLE_SECONDS": "17", "ASTRID_ALLOW_UNQUALIFIED_GPU": "1"})
    monkeypatch.setenv("ASTRID_WARM_IDLE_SECONDS", "900")
    monkeypatch.setenv("ASTRID_ALLOW_UNQUALIFIED_GPU", "0")
    version = Version(tmp_path / "version", tmp_path / "python", tmp_path / "profile", {})
    observed = []
    module = ModuleType("astrid_runtime.cli")

    def main(argv):
        import os

        observed.append((argv, os.environ["ASTRID_WARM_IDLE_SECONDS"], os.environ["ASTRID_ALLOW_UNQUALIFIED_GPU"]))
        return 0

    module.main = main
    monkeypatch.setitem(sys.modules, "astrid_runtime.cli", module)
    argv = command(version, tmp_path / "data", env_file=settings)
    with pytest.raises(SystemExit) as result:
        exec(argv[3], {})
    assert result.value.code == 0
    assert observed == [(["run", "--profile", "astrid", "--data-root", str(tmp_path / "data"),
                         "--source-manifest", str(version.profile)], "17", "1")]


@pytest.mark.parametrize("settings", [{"PATH": "/unmanaged"}, {"ASTRID_WARM_IDLE_SECONDS": 3}, []])
def test_service_wrapper_rejects_unknown_or_nonstring_settings(tmp_path, settings):
    path = tmp_path / "service-env.json"
    path.write_text(json.dumps(settings))
    version = Version(tmp_path / "version", tmp_path / "python", tmp_path / "profile", {})
    with pytest.raises(ValueError, match="Invalid Astrid service-env.json"):
        exec(command(version, tmp_path / "data", env_file=path)[3], {})


def test_registration_preserves_settings_and_records_selection(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg-data"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg-config"))
    root = tmp_path / "program"
    manager = Service(root, tmp_path / "log", Mock(side_effect=FileNotFoundError()), home=tmp_path, system="linux", say=lambda _: None)
    write_json(manager.env_file, {"ASTRID_WARM_IDLE_SECONDS": "17"})
    before = manager.env_file.read_bytes()
    version = Version(root / "versions/one", tmp_path / "python", tmp_path / "profile", {})
    manager.register(version, tmp_path / "data")
    manager.register(version, tmp_path / "data")
    assert manager.env_file.read_bytes() == before
    assert str(manager.env_file) in manager.path.read_text()
    assert read_json(manager.selection)["program_root"] == str(root)
    assert default_program_root(tmp_path, "linux") == tmp_path / "xdg-data/astrid"


def test_removed_install_can_delete_kept_data_repeatedly(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg-data"))
    root, data = tmp_path / "removed-program", tmp_path / "kept-data"
    data.mkdir()
    (data / "sentinel").write_text("kept")
    backend = Backend(root, tmp_path / "log", tmp_path / "uv")
    write_json(backend.service.selection, {"owner": LABEL, "program_root": str(root),
                                         "data_root": str(data), "uninstalled": True})
    assert backend.remove(root, data, delete_data=False) == []
    assert (data / "sentinel").read_text() == "kept"
    assert backend.remove(root, data, delete_data=True) == []
    assert not data.exists()
    assert backend.remove(root, data, delete_data=True) == []
    assert not root.exists()


def test_doctor_does_not_report_a_stale_bundle_after_failure(tmp_path, monkeypatch):
    import subprocess

    backend = Backend(tmp_path / "program", tmp_path / "log", tmp_path / "uv")
    version = Version(tmp_path / "version", tmp_path / "python", tmp_path / "profile", {})
    bundle = tmp_path / "doctor.zip"
    bundle.write_bytes(b"previous report")
    monkeypatch.setattr(backend, "run", Mock(side_effect=subprocess.CalledProcessError(1, "doctor")))
    with pytest.raises(subprocess.CalledProcessError):
        backend.doctor(version, tmp_path / "data", bundle)
    assert bundle.read_bytes() == b"previous report"


def test_doctor_returns_a_new_bundle_for_an_unhealthy_runtime(tmp_path, monkeypatch):
    import subprocess

    backend = Backend(tmp_path / "program", tmp_path / "log", tmp_path / "uv")
    version = Version(tmp_path / "version", tmp_path / "python", tmp_path / "profile", {})
    bundle = tmp_path / "doctor.zip"
    calls = []

    def unhealthy(argv, *, extra_env):
        calls.append((argv, extra_env))
        bundle.write_bytes(b"new unhealthy report")
        raise subprocess.CalledProcessError(1, "doctor")

    monkeypatch.setattr(backend, "run", unhealthy)
    assert backend.doctor(version, tmp_path / "data", bundle) == bundle
    assert calls[0][1]["ASTRID_RUNTIME_DATA_ROOT"] == str(tmp_path / "data")
