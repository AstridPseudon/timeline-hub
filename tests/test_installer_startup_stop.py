"""A published candidate can fail before its owner publishes discovery."""

import os
import subprocess
import sys
from unittest.mock import Mock

import pytest
from runtime_protocol import platform

from astrid.installer.backend import Backend
from astrid.installer.core import write_json
from astrid.installer.service import LABEL


def backend(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local-app-data"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg-data"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg-config"))
    value = Backend(tmp_path / "program", tmp_path / "log", tmp_path / "uv")
    value.service.system = "linux"
    value.service.systemd = lambda: False
    return value


def record(manager, pid=123, birth="original"):
    write_json(manager.registry, {"owner": LABEL, "foreground": {"pid": pid, "birth_id": birth}})


@pytest.mark.parametrize("stale_discovery", [False, True])
def test_stop_before_discovery_terminates_the_actual_recorded_owner(tmp_path, monkeypatch, stale_discovery):
    value = backend(tmp_path, monkeypatch)
    discovery = tmp_path / "data/runtime/discovery.json"
    if stale_discovery:
        write_json(discovery, {"pid": 2**31 - 1, "process_birth_id": "already absent"})
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        identity = platform.process_identity(child.pid)
        assert identity and identity["uid"] == platform.current_user()
        record(value.service, child.pid, identity["birth_id"])
        runtime = Mock(side_effect=AssertionError("unpublished owner has no Runtime down endpoint"))
        monkeypatch.setattr(value, "runtime", runtime)

        value.stop(None, tmp_path / "data")

        assert child.wait(timeout=5) != 0
        runtime.assert_not_called()
        assert discovery.exists() is stale_discovery
    finally:
        if child.poll() is None:
            child.kill()
        child.wait(timeout=5)


def test_unpublished_stop_uses_the_observed_identity_with_the_native_helper(tmp_path, monkeypatch):
    value = backend(tmp_path, monkeypatch)
    record(value.service)
    identity = {"pid": 123, "birth_id": "original", "uid": os.getuid() if hasattr(os, "getuid") else 7}
    monkeypatch.setattr(platform, "current_user", lambda: identity["uid"])
    monkeypatch.setattr(platform, "process_identity", lambda pid: identity)
    signal = Mock()
    monkeypatch.setattr(platform, "signal_process", signal)

    value.service.stop_foreground()

    signal.assert_called_once_with(identity, platform.TERM)


@pytest.mark.parametrize("identity", [None, {"pid": 123, "birth_id": "reused", "uid": 7}])
def test_absent_or_reused_foreground_is_never_signaled(tmp_path, monkeypatch, identity):
    value = backend(tmp_path, monkeypatch)
    record(value.service)
    monkeypatch.setattr(platform, "process_identity", lambda pid: identity)
    signal = Mock()
    monkeypatch.setattr(platform, "signal_process", signal)

    value.service.stop_foreground()

    signal.assert_not_called()


@pytest.mark.parametrize("identity", [
    {"pid": 124, "birth_id": "original", "uid": 7},
    {"pid": 123, "birth_id": "original", "uid": 8},
])
def test_other_owner_or_invalid_pid_is_refused(tmp_path, monkeypatch, identity):
    value = backend(tmp_path, monkeypatch)
    record(value.service)
    monkeypatch.setattr(platform, "current_user", lambda: 7)
    monkeypatch.setattr(platform, "process_identity", lambda pid: identity)
    signal = Mock()
    monkeypatch.setattr(platform, "signal_process", signal)

    with pytest.raises(RuntimeError, match="identity changed"):
        value.service.stop_foreground()
    signal.assert_not_called()


def test_unknown_identity_observation_does_not_signal(tmp_path, monkeypatch):
    value = backend(tmp_path, monkeypatch)
    record(value.service)
    monkeypatch.setattr(platform, "process_identity", Mock(side_effect=PermissionError("cannot observe")))
    signal = Mock()
    monkeypatch.setattr(platform, "signal_process", signal)

    with pytest.raises(PermissionError, match="cannot observe"):
        value.service.stop_foreground()
    signal.assert_not_called()


def test_native_identity_drift_failure_is_not_retried_with_a_pid(tmp_path, monkeypatch):
    value = backend(tmp_path, monkeypatch)
    record(value.service)
    identity = {"pid": 123, "birth_id": "original", "uid": 7}
    monkeypatch.setattr(platform, "current_user", lambda: 7)
    monkeypatch.setattr(platform, "process_identity", lambda pid: identity)
    signal = Mock(side_effect=OSError("incarnation changed while binding"))
    monkeypatch.setattr(platform, "signal_process", signal)

    with pytest.raises(OSError, match="incarnation changed"):
        value.service.stop_foreground()
    signal.assert_called_once_with(identity, platform.TERM)


@pytest.mark.parametrize("foreground", [{}, {"pid": True, "birth_id": "original"},
                                         {"pid": 123, "birth_id": ""}, {"pid": -1, "birth_id": "old"}])
def test_incomplete_foreground_identity_fails_before_signaling(tmp_path, monkeypatch, foreground):
    value = backend(tmp_path, monkeypatch)
    write_json(value.service.registry, {"owner": LABEL, "foreground": foreground})
    signal = Mock()
    monkeypatch.setattr(platform, "signal_process", signal)

    with pytest.raises(ValueError, match="identity is incomplete"):
        value.service.stop_foreground()
    signal.assert_not_called()


def test_native_exit_race_never_retries_the_numeric_pid(tmp_path, monkeypatch):
    value = backend(tmp_path, monkeypatch)
    record(value.service)
    identity = {"pid": 123, "birth_id": "original", "uid": 7}
    monkeypatch.setattr(platform, "current_user", lambda: 7)
    monkeypatch.setattr(platform, "process_identity", lambda pid: identity)
    signal = Mock(side_effect=ProcessLookupError("already exited"))
    monkeypatch.setattr(platform, "signal_process", signal)

    value.service.stop_foreground()

    signal.assert_called_once_with(identity, platform.TERM)


def test_live_runtime_drains_through_down_without_signaling_foreground(tmp_path, monkeypatch):
    value = backend(tmp_path, monkeypatch)
    data = tmp_path / "data"
    discovery = data / "runtime/discovery.json"
    write_json(discovery, {"pid": 123, "process_birth_id": "original"})
    monkeypatch.setattr(platform, "process_identity", lambda pid: {"pid": 123, "birth_id": "original"})
    calls = []

    def runtime(version, root, operation, **kwargs):
        assert operation == "down" and root == data and kwargs == {"profile": True}
        calls.append("runtime-down")
        discovery.unlink()

    monkeypatch.setattr(value, "runtime", runtime)
    signal = Mock(side_effect=AssertionError("live Runtime must own its drain"))
    monkeypatch.setattr(value.service, "stop_foreground", signal)
    monkeypatch.setattr(value.service, "stop", lambda: calls.append("wait-manager"))

    value.stop(None, data)

    assert calls == ["runtime-down", "wait-manager"]
    signal.assert_not_called()
