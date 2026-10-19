from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from tests.lanes import requires_posix_file_modes_native_custody

from astrid_runtime import custody_broker as custody
from runtime_protocol import platform


def _identities(monkeypatch):
    owner = {"pid": os.getpid(), "uid": platform.current_user(), "birth_id": "controller-birth"}
    target = {"pid": 44121, "uid": platform.current_user(), "birth_id": "target-birth"}
    monkeypatch.setattr(custody, "default_process_identity", lambda _pid: dict(owner))
    # Exercise the native pidfd/OpenProcess branch without entering Darwin's
    # audit-token lane. The signal itself remains a mocked platform call.
    monkeypatch.setattr(custody, "sys", SimpleNamespace(platform="linux"))
    return owner, target


def test_native_custody_publish_release_and_adopted_signal_use_guard(tmp_path, monkeypatch):
    owner_identity, target = _identities(monkeypatch)
    delivered = []
    monkeypatch.setattr(platform, "signal_process", lambda identity, signum: delivered.append((dict(identity), signum)))
    original = custody.NativeProcessCustody(tmp_path, target)
    original.publish()
    stored = json.loads(original.path.read_text())
    assert stored["state"] == "owned"
    assert stored["controller"] == owner_identity
    assert stored["target"] == target

    guarded = []
    def validate_inside_lock():
        with pytest.raises(BlockingIOError):
            with platform.file_lock(original.lock, blocking=False):
                pytest.fail("native custody guard was not held during validation")
        guarded.append(True)
    original.signal(platform.TERM, validate=validate_inside_lock)
    assert guarded == [True]
    assert delivered == [(target, platform.TERM)]

    assert original.release() == {"state": "released"}
    assert json.loads(original.path.read_text())["state"] == "released"
    # A fresh operator object adopts the released record and delivers through
    # the identity-pinning platform boundary.
    adopted = custody.NativeProcessCustody(tmp_path, target)
    adopted.signal(platform.KILL)
    assert delivered == [(target, platform.TERM), (target, platform.KILL)]


@pytest.mark.parametrize("mutation,match", [
    ("target", "differs from the selected owner"),
    ("version", "differs from the selected owner"),
])
def test_native_custody_rejects_wrong_target_or_version(tmp_path, monkeypatch, mutation, match):
    _owner, target = _identities(monkeypatch)
    instance = custody.NativeProcessCustody(tmp_path, target)
    instance.publish()
    value = json.loads(instance.path.read_text())
    if mutation == "target":
        value["target"] = {**target, "birth_id": "replacement-birth"}
    else:
        value["version"] = "other"
    custody._atomic_owner_json(instance.path, value)
    with pytest.raises(custody.CustodyError, match=match):
        instance._read()


def test_native_custody_rejects_another_live_controller_while_owned(tmp_path, monkeypatch):
    old = {"pid": 41001, "uid": platform.current_user(), "birth_id": "old-controller"}
    other = {"pid": 41002, "uid": platform.current_user(), "birth_id": "other-controller"}
    target = {"pid": 44121, "uid": platform.current_user(), "birth_id": "target-birth"}
    identities = {old["pid"]: old, other["pid"]: other}
    monkeypatch.setattr(custody, "sys", SimpleNamespace(platform="linux"))
    monkeypatch.setattr(custody, "default_process_identity", lambda pid: identities.get(pid))
    class OsProxy:
        current_pid = old["pid"]
        def __getattr__(self, name): return getattr(os, name)
        def getpid(self): return self.current_pid
    os_proxy = OsProxy()
    monkeypatch.setattr(custody, "os", os_proxy)
    instance = custody.NativeProcessCustody(tmp_path, target)
    instance.publish()
    os_proxy.current_pid = other["pid"]
    with pytest.raises(custody.CustodyError, match="another controller"):
        instance.release()
    with pytest.raises(custody.CustodyError, match="another live controller"):
        instance.signal(platform.TERM)


def test_native_custody_recovers_when_prior_controller_is_proven_absent(tmp_path, monkeypatch):
    old = {"pid": 41011, "uid": platform.current_user(), "birth_id": "dead-controller"}
    current = {"pid": 41012, "uid": platform.current_user(), "birth_id": "current-controller"}
    target = {"pid": 44122, "uid": platform.current_user(), "birth_id": "target-birth"}
    identities = {old["pid"]: old, current["pid"]: current}
    monkeypatch.setattr(custody, "sys", SimpleNamespace(platform="linux"))
    monkeypatch.setattr(custody, "default_process_identity", lambda pid: identities.get(pid))
    class OsProxy:
        current_pid = old["pid"]
        def __getattr__(self, name): return getattr(os, name)
        def getpid(self): return self.current_pid
    os_proxy = OsProxy()
    monkeypatch.setattr(custody, "os", os_proxy)
    instance = custody.NativeProcessCustody(tmp_path, target)
    instance.publish()
    os_proxy.current_pid = current["pid"]
    # The old controller PID is absent; the signal operation durably adopts
    # the active record before delivering through the platform boundary.
    identities.pop(old["pid"])
    delivered = []
    monkeypatch.setattr(platform, "signal_process", lambda identity, signum: delivered.append((dict(identity), signum)))
    instance.signal(platform.TERM)
    record = json.loads(instance.path.read_text())
    assert record["state"] == "owned"
    assert record["controller"] == current
    assert delivered == [(target, platform.TERM)]


@requires_posix_file_modes_native_custody
def test_native_custody_rejects_unsafe_owner_file(tmp_path, monkeypatch):
    _owner, target = _identities(monkeypatch)
    instance = custody.NativeProcessCustody(tmp_path, target)
    instance.publish()
    instance.path.chmod(0o644)
    with pytest.raises(custody.CustodyError, match="owner-only"):
        instance._read()


def test_native_custody_wraps_platform_identity_drift_without_signaling(tmp_path, monkeypatch):
    _owner, target = _identities(monkeypatch)
    instance = custody.NativeProcessCustody(tmp_path, target)
    instance.publish()
    failures = []
    def reject_drift(identity, signum):
        failures.append((identity, signum))
        raise OSError("process incarnation changed")
    monkeypatch.setattr(platform, "signal_process", reject_drift)
    with pytest.raises(custody.CustodyError, match="process incarnation changed"):
        instance.signal(platform.TERM)
    assert failures == [(target, platform.TERM)]
