"""Update backups reserve disk space and preserve the logs of a failed update."""

import shutil
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from astrid.installer.backend import Backend
from astrid.installer.core import BackupSpaceError, Version, write_json


def workspace(tmp_path, system):
    program, data = tmp_path / "program", tmp_path / "support"
    realm = data / "runtime/realms/selected"
    realm.mkdir(parents=True)
    (realm / "realm.sqlite3").write_bytes(b"selected database")
    (realm / "media").write_bytes(b"selected media")
    write_json(data / "runtime/catalog.json", {"selected": "selected"})
    write_json(data / "runtime/discovery.json", {"transient": True})
    (data / "runtime/instance.lock").write_bytes(b"live lock")
    (data / "runtime/bootstrap.lock").write_bytes(b"bootstrap lock")
    other = data / "runtime/realms/other"
    other.mkdir()
    (other / "excluded").write_bytes(b"unselected media" * 100)
    logs = data / "logs"
    logs.mkdir()
    (logs / "install.log").write_text("before the update\n")
    (logs / "runtime-service.log").write_text("service output\n")
    backend = Backend(program, logs / "install.log", tmp_path / "uv")
    backend.service.system = system
    version = Version(program / "versions/old", tmp_path / "python", tmp_path / "profile", {})

    def runtime(_version, _data, *args, **_kwargs):
        if args[0] == "backup":
            shutil.copytree(realm, Path(args[2]))
        return {}

    backend.runtime = Mock(side_effect=runtime)
    backend.stop = Mock()
    return backend, data, realm, version


@pytest.mark.parametrize("system", ["linux", "win32"])
def test_full_backup_checks_realm_support_and_margin_before_starting(tmp_path, monkeypatch, system):
    backend, data, realm, version = workspace(tmp_path, system)
    selected_size = sum(path.stat().st_size for path in realm.iterdir())
    support_size = (data / "runtime/catalog.json").stat().st_size
    assert backend._backup_size(data, support=True) == support_size
    required = selected_size + support_size + 256 * 1024 * 1024
    usage = Mock(return_value=SimpleNamespace(free=required - 1))
    monkeypatch.setattr(shutil, "disk_usage", usage)

    with pytest.raises(BackupSpaceError) as failure:
        backend.backup(version, data, {"realm_root": str(realm)})

    assert str(failure.value) == "There is not enough free disk space to back up your workspace."
    usage.assert_called_once_with(backend.root)
    backend.runtime.assert_not_called()
    backend.stop.assert_not_called()
    assert list((backend.root / "backups").iterdir()) == []
    assert (data / "logs/install.log").read_text() == "before the update\n"

    usage.return_value.free = required
    backup = backend.backup(version, data, {"realm_root": str(realm)})
    snapshot = Path(backup["root"]) / "support"
    assert backend._backup_size(snapshot) == support_size
    assert not (snapshot / "logs").exists()
    assert not (snapshot / "runtime/realms").exists()
    assert not (snapshot / "runtime/discovery.json").exists()


def test_large_backup_reserves_ten_percent_when_larger_than_minimum_margin(tmp_path, monkeypatch):
    backend, data, realm, version = workspace(tmp_path, "linux")
    size = 4 * 1024 * 1024 * 1024
    monkeypatch.setattr(backend, "_backup_size", lambda path, **_kwargs: size if path == realm else 0)
    monkeypatch.setattr(shutil, "disk_usage", lambda _path: SimpleNamespace(free=size + size // 10 - 1))

    with pytest.raises(BackupSpaceError):
        backend.backup(version, data, {"realm_root": str(realm)})

    backend.runtime.assert_not_called()


@pytest.mark.parametrize("step", ["up", "backup", "stop", "support", "metadata", "cancel"])
def test_failed_full_backup_removes_its_partial_snapshot(tmp_path, monkeypatch, step):
    import astrid.installer.backend as module

    backend, data, realm, version = workspace(tmp_path, "linux")
    original_runtime, original_copy = backend.runtime, backend._copy
    failure = KeyboardInterrupt() if step == "cancel" else OSError("backup failed")

    def runtime(*args, **kwargs):
        operation = args[2]
        if operation == step or (operation == "backup" and step == "cancel"):
            (next((backend.root / "backups").iterdir()) / "partial").write_bytes(b"partial data")
            raise failure
        return original_runtime(*args, **kwargs)

    backend.runtime = runtime
    if step == "stop":
        backend.stop = Mock(side_effect=failure)

    def copy(source, destination, **kwargs):
        original_copy(source, destination, **kwargs)
        if step == "support":
            raise failure

    monkeypatch.setattr(backend, "_copy", copy)
    if step == "metadata":
        monkeypatch.setattr(module, "write_json", Mock(side_effect=failure))

    with pytest.raises(type(failure)):
        backend.backup(version, data, {"realm_root": str(realm)})

    assert list((backend.root / "backups").iterdir()) == []
    assert (data / "logs/install.log").read_text() == "before the update\n"


def test_failed_clone_backup_removes_its_partial_snapshot(tmp_path, monkeypatch):
    backend, data, realm, version = workspace(tmp_path, "darwin")

    def clone(source, destination):
        shutil.copy2(source, destination)
        raise OSError("clone failed")

    monkeypatch.setattr("runtime_protocol.fsclone.clone_or_copy_file", clone)

    with pytest.raises(OSError, match="clone failed"):
        backend.backup(version, data, {"realm_root": str(realm)})

    assert list((backend.root / "backups").iterdir()) == []
    backend.runtime.assert_not_called()


def test_rollback_preserves_live_logs_even_in_an_older_snapshot(tmp_path, monkeypatch):
    backend, data, realm, version = workspace(tmp_path, "darwin")
    monkeypatch.setattr("runtime_protocol.fsclone.clone_or_copy_file", shutil.copy2)
    identity = {"realm_root": str(realm)}
    backup = backend.backup(version, data, identity)
    snapshot = Path(backup["root"]) / "support"
    assert not (snapshot / "logs").exists()
    shutil.copytree(data / "logs", snapshot / "logs")  # Previous installer snapshots included logs.
    (realm / "realm.sqlite3").write_bytes(b"failed migration")
    (data / "logs/install.log").write_text("the update failed here\n")
    (data / "logs/runtime-service.log").write_text("live shutdown output\n")
    remove = shutil.rmtree

    def remove_except_logs(path, *args, **kwargs):
        assert Path(path) != data / "logs", "the rollback must leave open Windows log handles alone"
        return remove(path, *args, **kwargs)

    monkeypatch.setattr(shutil, "rmtree", remove_except_logs)
    backend.restore(version, data, identity, backup)

    assert (realm / "realm.sqlite3").read_bytes() == b"selected database"
    assert (data / "logs/install.log").read_text() == "the update failed here\n"
    assert (data / "logs/runtime-service.log").read_text() == "live shutdown output\n"
    assert (data / "runtime/realms/other/excluded").is_file()


def test_backup_size_propagates_unreadable_directory_errors(tmp_path, monkeypatch):
    backend, data, _realm, _version = workspace(tmp_path, "linux")

    def unreadable(_source, *, onerror):
        onerror(PermissionError("cannot read workspace"))
        return iter(())

    monkeypatch.setattr("astrid.installer.backend.os.walk", unreadable)

    with pytest.raises(PermissionError, match="cannot read workspace"):
        backend._backup_size(data, support=True)
