from __future__ import annotations

import os
from pathlib import Path

import pytest

from runtime_protocol.dirfd import filesystem


def test_platform_filesystem_exports_shared_os_api():
    """The facade forwards ordinary os calls on every supported platform."""
    assert filesystem.path is os.path
    assert filesystem.fspath(Path("sample")) == os.fspath(Path("sample"))


@pytest.mark.skipif(os.name != "nt", reason="exercises the native Windows dir-fd adapter")
def test_windows_directory_descriptor_operations(tmp_path):
    directory_flag = filesystem.O_DIRECTORY
    nofollow_flag = filesystem.O_NOFOLLOW
    root_fd = filesystem.open(tmp_path, os.O_RDONLY | directory_flag | nofollow_flag)
    try:
        filesystem.mkdir("nested", dir_fd=root_fd)
        nested_fd = filesystem.open("nested", os.O_RDONLY | directory_flag | nofollow_flag, dir_fd=root_fd)
        try:
            filesystem.mkdir("inner", dir_fd=nested_fd)
            filesystem.mkdir("inner/deeper", dir_fd=nested_fd)
            fd = filesystem.open(
                "first.bin", os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow_flag,
                0o600, dir_fd=nested_fd,
            )
            try:
                filesystem.write(fd, b"payload")
                filesystem.fsync(fd)
            finally:
                filesystem.close(fd)

            assert filesystem.stat("first.bin", dir_fd=nested_fd).st_size == 7
            filesystem.rename("first.bin", "second.bin", src_dir_fd=nested_fd, dst_dir_fd=nested_fd)
            filesystem.link("second.bin", "copy.bin", src_dir_fd=nested_fd, dst_dir_fd=nested_fd)
            assert set(filesystem.listdir(nested_fd)) == {"inner", "second.bin", "copy.bin"}
            assert filesystem.stat("inner/deeper", dir_fd=nested_fd).st_mode
            with filesystem.scandir(nested_fd) as entries:
                assert {entry.name for entry in entries} == {"inner", "second.bin", "copy.bin"}
            filesystem.unlink("second.bin", dir_fd=nested_fd)
            filesystem.unlink("copy.bin", dir_fd=nested_fd)
            filesystem.rmdir("inner/deeper", dir_fd=nested_fd)
            filesystem.rmdir("inner", dir_fd=nested_fd)
        finally:
            filesystem.close(nested_fd)
        filesystem.rmdir("nested", dir_fd=root_fd)
    finally:
        filesystem.close(root_fd)


@pytest.mark.skipif(os.name != "nt", reason="exercises Windows reparse-point rejection")
def test_windows_directory_descriptor_rejects_symlink_component(tmp_path):
    target = tmp_path / "real"
    target.mkdir()
    alias = tmp_path / "alias"
    try:
        alias.symlink_to(target, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is unavailable for this Windows account")
    with pytest.raises(OSError):
        filesystem.open(alias, os.O_RDONLY | filesystem.O_DIRECTORY | filesystem.O_NOFOLLOW)


@pytest.mark.skipif(os.name != "nt", reason="exercises Windows SQLite backup snapshots")
def test_windows_backup_restore_verify_uses_pinned_filesystem_paths(tmp_path):
    from runtime_protocol.backup import create_backup, restore_backup, verify_backup, verify_restore_candidate
    from runtime_protocol.store import RealmStore

    root = tmp_path / "realm"
    store = RealmStore.initialize(root, realm_id="windows-backup-test")
    backup = tmp_path / "backup"
    restored = tmp_path / "restored"
    try:
        create_backup(store, backup)
    finally:
        store.close()

    assert verify_backup(backup)["doctor"]["ok"]
    restore_backup(backup, restored)
    assert verify_restore_candidate(restored)["doctor"]["ok"]
