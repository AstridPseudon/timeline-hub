"""Installer admission and lock placement through the Windows permission seam."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from astrid.installer import cli
from runtime_protocol import platform, windows_security


@pytest.mark.parametrize("custom_root", [False, True])
def test_windows_installer_lock_stays_inside_private_logs(tmp_path, monkeypatch, custom_root):
    local = tmp_path / "local"
    log_dir = local / "Astrid Runtime" / "logs"
    root = tmp_path / "custom" if custom_root else local / "Astrid"
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setattr(cli, "sys", SimpleNamespace(platform="win32"))
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="win32"))
    monkeypatch.setattr(platform, "log_dir", lambda: log_dir)
    admitted = []

    def private_directory(path):
        path = Path(path)
        assert path != local, "the installer must never change LOCALAPPDATA's ACL"
        admitted.append(path)
        path.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(windows_security, "private_directory", private_directory)
    backend = Mock()
    backend.service.recorded.return_value = {}
    monkeypatch.setattr(cli, "Backend", Mock(return_value=backend))
    monkeypatch.setattr(cli, "find_data_root", lambda *_: (tmp_path / "workspace", False))
    monkeypatch.setattr(cli, "current", lambda _: SimpleNamespace(python=Path(__file__)))
    installer = Mock()
    monkeypatch.setattr(cli, "Installer", Mock(return_value=installer))
    locks = []
    monkeypatch.setattr(platform, "lock_file", lambda fd, **_: locks.append(fd))
    unlock = Mock()
    monkeypatch.setattr(platform, "unlock_file", unlock)

    args = ["--repair", "--root", str(root)] if custom_root else ["--repair"]
    assert cli.main(args) == 0
    lock = log_dir / "installer" / "astrid-install.lock"
    assert admitted == [log_dir, lock.parent, root]
    assert lock.is_file()
    assert root not in lock.parents
    assert not (local / "astrid-install.lock").exists()
    assert len(locks) == 1
    unlock.assert_called_once_with(locks[0])
    installer.run.assert_called_once()


def test_windows_installer_does_not_bypass_existing_root_validation(tmp_path, monkeypatch):
    log_dir = tmp_path / "logs"
    root = tmp_path / "program"
    root.mkdir()
    monkeypatch.setattr(cli, "sys", SimpleNamespace(platform="win32"))
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="win32"))
    monkeypatch.setattr(platform, "log_dir", lambda: log_dir)

    def private_directory(path):
        if Path(path) == root:
            raise PermissionError("unprotected existing DACL")
        Path(path).mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(windows_security, "private_directory", private_directory)
    backend = Mock()
    backend.service.recorded.return_value = {}
    monkeypatch.setattr(cli, "Backend", Mock(return_value=backend))
    monkeypatch.setattr(cli, "find_data_root", lambda *_: (tmp_path / "workspace", False))
    monkeypatch.setattr(platform, "lock_file", Mock())
    monkeypatch.setattr(platform, "unlock_file", Mock())
    installer = Mock()
    monkeypatch.setattr(cli, "Installer", installer)

    assert cli.main(["--repair", "--root", str(root)]) == 1
    installer.assert_not_called()
    assert not (root / "install.json").exists()
