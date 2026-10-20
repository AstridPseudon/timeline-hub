from __future__ import annotations

import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from types import SimpleNamespace

import pytest

from tests.lanes import (
    requires_posix_private_modes,
    requires_posix_process_groups,
    requires_windows_job_object,
    requires_windows_token_process_times,
)

from runtime_protocol import platform


@pytest.mark.parametrize("os_name", ["darwin", "linux", "win32"])
def test_native_data_and_log_roots_use_os_default_and_injected_home(monkeypatch, tmp_path, os_name):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform=os_name))
    home = tmp_path / "home"
    local_app_data = tmp_path / "user-local"
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg-data"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg-state"))
    if os_name == "darwin":
        assert platform.data_root(home) == home / "Library/Application Support/Astrid Runtime"
        assert platform.log_dir(home) == home / "Library/Logs/Astrid Runtime"
    elif os_name == "linux":
        assert platform.data_root(home) == tmp_path / "xdg-data/astrid-runtime"
        assert platform.log_dir(home) == tmp_path / "xdg-state/astrid-runtime/logs"
    else:
        assert platform.data_root(home) == local_app_data / "Astrid Runtime"
        assert platform.log_dir(home) == local_app_data / "Astrid Runtime/logs"


def test_linux_data_and_log_roots_fall_back_to_injected_home(monkeypatch, tmp_path):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    home = tmp_path / "home"
    assert platform.data_root(home) == home / ".local/share/astrid-runtime"
    assert platform.log_dir(home) == home / ".local/state/astrid-runtime/logs"


def test_windows_roots_fall_back_to_injected_home(monkeypatch, tmp_path):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="win32"))
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    home = tmp_path / "home"
    assert platform.data_root(home) == home / "AppData/Local/Astrid Runtime"
    assert platform.log_dir(home) == home / "AppData/Local/Astrid Runtime/logs"


@requires_posix_private_modes
def test_owner_only_applies_and_checks_private_file_and_directory_modes(tmp_path):
    file_path = tmp_path / "secret"
    file_path.write_text("secret")
    directory = tmp_path / "private"
    directory.mkdir()
    platform.owner_only(file_path)
    platform.owner_only(directory, directory=True)
    assert platform.is_owner_only(file_path)
    assert platform.is_owner_only(file_path.stat())
    assert platform.is_owner_only(directory, directory=True)
    if sys.platform != "win32":
        assert file_path.stat().st_mode & 0o777 == 0o600
        assert directory.stat().st_mode & 0o777 == 0o700
    file_path.chmod(0o640)
    assert not platform.is_owner_only(file_path)


def test_file_lock_excludes_contender_and_releases(tmp_path):
    lock_path = tmp_path / "owner.lock"
    with platform.file_lock(lock_path, blocking=True):
        with pytest.raises(BlockingIOError):
            with platform.file_lock(lock_path, blocking=False):
                pytest.fail("contender acquired a held lock")
    with platform.file_lock(lock_path, blocking=False):
        pass


def test_current_process_identity_is_stable_and_has_native_fields():
    identity = platform.process_identity(os.getpid())
    assert identity is not None
    assert identity["pid"] == os.getpid()
    assert identity["uid"] == platform.current_user()
    assert identity["birth_id"]


def test_linux_proc_identity_parser_uses_stat_and_brackets_start_tick(monkeypatch):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    reads = []
    start_ticks = ["4242", "4242"]

    class FakePath:
        def __init__(self, value):
            self.value = str(value)
        def __truediv__(self, part):
            return FakePath(self.value.rstrip("/") + "/" + str(part))
        def read_text(self):
            reads.append(self.value)
            if self.value == "/proc/sys/kernel/random/boot_id":
                return "b38142f7-84c5-487d-95a4-8180cbff3972\n"
            tick = start_ticks[min(len(reads) - 1, 1)]
            fields = ["S", "23", "24", "25"] + ["0"] * 15 + [tick, "0"]
            return "77 (worker ) with parens) " + " ".join(fields)
        def stat(self):
            return SimpleNamespace(st_uid=501)

    monkeypatch.setattr(platform, "Path", FakePath)
    value = platform.process_identity(77)
    assert value["pid"] == 77
    assert value["uid"] == 501
    assert value["parent_pid"] == 23
    assert value["process_group"] == 24
    assert value["session_id"] == 25
    assert value["birth_id"] == "b38142f7-84c5-487d-95a4-8180cbff3972:4242"
    assert reads == ["/proc/sys/kernel/random/boot_id", "/proc/77/stat", "/proc/77/stat"]


def test_linux_proc_identity_rejects_pid_reuse_during_observation(monkeypatch):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    ticks = iter(("4242", "4243"))

    class FakePath:
        def __init__(self, value): self.value = str(value)
        def __truediv__(self, part): return FakePath(self.value.rstrip("/") + "/" + str(part))
        def read_text(self):
            if self.value == "/proc/sys/kernel/random/boot_id":
                return "b38142f7-84c5-487d-95a4-8180cbff3972\n"
            fields = ["S", "23", "24", "25"] + ["0"] * 15 + [next(ticks), "0"]
            return "77 (worker) " + " ".join(fields)
        def stat(self): return SimpleNamespace(st_uid=501)

    monkeypatch.setattr(platform, "Path", FakePath)
    with pytest.raises(OSError, match="changed"):
        platform.process_identity(77)


@pytest.mark.parametrize("boot_id,tick", [
    (None, "4242"), ("", "4242"), ("corrupt", "4242"),
    ("b38142f7-84c5-487d-95a4-8180cbff3972", "corrupt"),
])
def test_linux_proc_identity_refuses_unknown_boot_or_start_tick(tmp_path, monkeypatch, boot_id, tick):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    proc = tmp_path / "proc"
    (proc / "77").mkdir(parents=True)
    fields = ["S", "23", "24", "25"] + ["0"] * 15 + [tick, "0"]
    (proc / "77" / "stat").write_text("77 (worker) " + " ".join(fields))
    boot = tmp_path / "boot_id"
    if boot_id is not None:
        boot.write_text(boot_id)
    monkeypatch.setattr(platform, "Path", lambda path: boot if str(path).endswith("boot_id") else proc)
    with pytest.raises(OSError):
        platform.process_identity(77)


@pytest.mark.parametrize("birth_id", [
    "e1a239c5-fbdb-4c06-b924-6f0479e69568:4242",  # Same PID/tick, prior boot.
    "b38142f7-84c5-487d-95a4-8180cbff3972:4243",  # Reused PID.
    "proc-start-ticks:4242", "corrupt",
])
def test_linux_signal_refuses_mismatched_birth_before_kernel_signal(monkeypatch, birth_id):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    observed = {"pid": 77, "uid": 501, "birth_id": "b38142f7-84c5-487d-95a4-8180cbff3972:4242"}
    opened, closed = [], []
    monkeypatch.setattr(platform.os, "pidfd_open", lambda pid: opened.append(pid) or 99, raising=False)
    monkeypatch.setattr(platform.os, "close", closed.append)
    monkeypatch.setattr(platform.signal, "pidfd_send_signal", lambda *_: pytest.fail("mismatched birth signaled"), raising=False)
    monkeypatch.setattr(platform, "process_identity", lambda pid: observed)
    with pytest.raises(OSError, match="incarnation changed"):
        platform.signal_process({**observed, "birth_id": birth_id}, platform.TERM)
    assert opened == [77]
    assert closed == [99]


def test_darwin_identity_keeps_legacy_birth_marker_and_brackets_native_observation(monkeypatch):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="darwin"))
    seconds = int(time.mktime((2026, 10, 9, 18, 21, 21, 0, 0, -1)))
    observation = {"pid": 123, "uid": 501, "parent_pid": 41, "start_sec": seconds, "start_usec": 123456}
    rows = iter((observation, dict(observation)))
    monkeypatch.setattr(platform, "_read_darwin_process_info", lambda _pid: next(rows))
    value = platform.process_identity(123)
    assert value == {
        "pid": 123, "uid": 501, "parent_pid": 41,
        "birth_id": "ps-lstart:Fri Oct  9 18:21:21 2026",
    }


def test_darwin_identity_only_proves_absence_from_native_esrch(monkeypatch):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="darwin"))
    monkeypatch.setattr(platform, "_read_darwin_process_info", lambda _pid: None)
    assert platform.process_identity(123) is None
    monkeypatch.setattr(platform, "_read_darwin_process_info", lambda _pid: (_ for _ in ()).throw(PermissionError("denied")))
    with pytest.raises(PermissionError):
        platform.process_identity(123)


@requires_windows_token_process_times
def test_windows_current_user_and_get_process_times_identity():
    assert platform.current_user() > 0
    identity = platform.process_identity(os.getpid())
    assert identity["uid"] == platform.current_user()
    assert identity["birth_id"].startswith("windows-creation:")


@pytest.mark.integration
@requires_posix_process_groups
def test_stop_tree_cleans_up_grandchild(tmp_path):
    from runtime_protocol.platform import spawn_tree, stop_tree
    pid_file = tmp_path / "grandchild.pid"
    child_code = "import time; time.sleep(60)"
    parent_code = (
        "import subprocess,sys,time,pathlib; "
        f"p=subprocess.Popen([sys.executable,'-c',{child_code!r}]); "
        f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid)); time.sleep(60)"
    )
    process = spawn_tree([sys.executable, "-c", parent_code], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 5
        while not pid_file.exists() and time.monotonic() < deadline:
            time.sleep(.02)
        assert pid_file.exists()
        grandchild = int(pid_file.read_text())
    finally:
        stop_tree(process, grace=.1)
    _wait_absent(grandchild)


@pytest.mark.integration
@requires_windows_job_object
def test_windows_job_close_kills_grandchild(tmp_path):
    from runtime_protocol.platform import spawn_tree
    pid_file = tmp_path / "grandchild.pid"
    child_code = "import time; time.sleep(60)"
    parent_code = (
        "import subprocess,sys,time,pathlib; "
        f"p=subprocess.Popen([sys.executable,'-c',{child_code!r}]); "
        f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid)); time.sleep(60)"
    )
    process = spawn_tree([sys.executable, "-c", parent_code], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 5
        while not pid_file.exists() and time.monotonic() < deadline:
            time.sleep(.02)
        assert pid_file.exists()
        grandchild = int(pid_file.read_text())
    finally:
        process._runtime_job.close()
        process.wait(timeout=5)
    _wait_absent(grandchild)


def _wait_absent(pid):
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if platform.process_identity(pid) is None:
            return
        time.sleep(.02)
    pytest.fail(f"process {pid} outlived its owned tree")
