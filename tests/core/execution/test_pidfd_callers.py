"""Agent retained-handle callers work when Linux Python omits pidfd wrappers."""

from __future__ import annotations

import errno
import os
import signal
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from runtime_protocol import platform

from astrid.core.execution import custody_broker as custody
from astrid.core.execution import process_group as groups


@pytest.fixture
def without_stdlib_pidfds(monkeypatch):
    monkeypatch.delattr(os, "pidfd_open", raising=False)
    monkeypatch.delattr(signal, "pidfd_send_signal", raising=False)
    assert not hasattr(os, "pidfd_open")
    assert not hasattr(signal, "pidfd_send_signal")


@pytest.fixture
def runtime_pidfd_provider(without_stdlib_pidfds, monkeypatch):
    monkeypatch.setattr(custody.sys, "platform", "linux")
    provider = SimpleNamespace(pidfd_open=Mock(return_value=73), pidfd_send_signal=Mock())
    monkeypatch.setattr(platform, "pidfd_open", provider.pidfd_open)
    monkeypatch.setattr(platform, "pidfd_send_signal", provider.pidfd_send_signal)
    monkeypatch.setattr(os, "kill", lambda *_: pytest.fail("numeric PID fallback"))
    monkeypatch.setattr(os, "killpg", lambda *_: pytest.fail("numeric process-group fallback"))
    return provider


@pytest.mark.parametrize("missing", ["pidfd_open", "pidfd_send_signal"])
@pytest.mark.parametrize("availability", ["absent", "not-callable"])
def test_custody_launch_refuses_unavailable_runtime_pidfds(
    tmp_path, monkeypatch, runtime_pidfd_provider, missing, availability,
):
    if availability == "absent":
        monkeypatch.delattr(platform, missing)
    else:
        monkeypatch.setattr(platform, missing, None)
    owner = custody.ProcessCustody(scope_root=tmp_path)
    with pytest.raises(custody.CustodyError, match="kernel custody is unavailable"):
        owner.prepare_launch([sys.executable, "-c", "pass"], start_new_session=True)
    runtime_pidfd_provider.pidfd_open.assert_not_called()
    runtime_pidfd_provider.pidfd_send_signal.assert_not_called()


def test_custody_retains_runtime_pidfd_and_preserves_signal_fences(tmp_path, monkeypatch, runtime_pidfd_provider):
    provider = runtime_pidfd_provider
    owner = custody.ProcessCustody(scope_root=tmp_path)
    argv = [sys.executable, "-c", "pass"]
    assert owner.prepare_launch(argv, start_new_session=True) == (argv, {})
    provider.pidfd_open.assert_not_called()  # Preflight acquires no incidental handle.
    monkeypatch.setattr(groups, "process_birth_identity", lambda pid=None: "actor" if pid is None else "child")
    monkeypatch.setattr(groups, "held_child_birth_identity", lambda _pid: "child")
    inheritable, closed = Mock(), Mock()
    monkeypatch.setattr(custody.os, "set_inheritable", inheritable)
    monkeypatch.setattr(custody.os, "close", closed)
    owner.bind_launch(SimpleNamespace(pid=123))
    assert owner._handles[123] == ("child", 73)
    provider.pidfd_open.assert_called_once_with(123)
    inheritable.assert_called_once_with(73, False)
    with pytest.raises(custody.CustodyError, match="retained exact process"):
        owner.signal(123, "replacement", platform.TERM)
    monkeypatch.setattr(groups, "process_birth_identity", lambda *_: "replacement-actor")
    with pytest.raises(custody.CustodyError, match="actor incarnation changed"):
        owner.signal(123, "child", platform.TERM)
    provider.pidfd_send_signal.assert_not_called()
    monkeypatch.setattr(groups, "process_birth_identity", lambda *_: "actor")
    owner.signal(123, "child", platform.TERM)
    provider.pidfd_send_signal.assert_called_once_with(73, platform.TERM)
    owner.release_pidfds()
    closed.assert_called_once_with(73)


@pytest.mark.parametrize("failure", [errno.ENOSYS, errno.EPERM, errno.ESRCH])
def test_custody_open_failure_cannot_acquire_signal_authority(tmp_path, monkeypatch, runtime_pidfd_provider, failure):
    provider = runtime_pidfd_provider
    provider.pidfd_open.side_effect = OSError(failure, "native pidfd failure")
    owner = custody.ProcessCustody(scope_root=tmp_path)
    monkeypatch.setattr(groups, "process_birth_identity", lambda *_: "child")
    monkeypatch.setattr(groups, "held_child_birth_identity", lambda _pid: "child")
    with pytest.raises(OSError) as error:
        owner.bind_launch(SimpleNamespace(pid=123))
    assert error.value.errno == failure
    assert not owner._handles and owner._uncertain is error.value
    provider.pidfd_send_signal.assert_not_called()


def test_custody_birth_drift_after_open_closes_unadmitted_handle(tmp_path, monkeypatch, runtime_pidfd_provider):
    owner = custody.ProcessCustody(scope_root=tmp_path)
    births = iter(("child", "replacement"))
    monkeypatch.setattr(groups, "process_birth_identity", lambda *_: next(births))
    closed = Mock()
    monkeypatch.setattr(custody.os, "close", closed)
    owner.register(123, "child")
    assert not owner._handles
    closed.assert_called_once_with(73)
    runtime_pidfd_provider.pidfd_send_signal.assert_not_called()


@pytest.mark.parametrize("entry", ["register", "bind-launch"])
@pytest.mark.parametrize("stage", ["identity", "inheritability"])
def test_custody_post_open_failure_closes_untransferred_handle(
    tmp_path, monkeypatch, runtime_pidfd_provider, entry, stage,
):
    provider = runtime_pidfd_provider
    owner = custody.ProcessCustody(scope_root=tmp_path)
    process = SimpleNamespace(pid=123)
    failure = OSError(errno.EIO, f"post-open {stage} failure")

    def identify(pid):
        if stage == "identity" and provider.pidfd_open.called:
            raise failure
        return "child"

    monkeypatch.setattr(groups, "process_birth_identity", lambda pid=None: "actor" if pid is None else identify(pid))
    monkeypatch.setattr(groups, "held_child_birth_identity", identify)
    monkeypatch.setattr(custody.os, "set_inheritable", Mock(side_effect=failure if stage == "inheritability" else None))
    closed = Mock()
    monkeypatch.setattr(custody.os, "close", closed)
    with pytest.raises(OSError) as error:
        if entry == "register":
            owner.register(process.pid, "child")
        else:
            owner.bind_launch(process)
    assert error.value is failure
    provider.pidfd_open.assert_called_once_with(123)
    provider.pidfd_send_signal.assert_not_called()
    assert not owner._handles
    closed.assert_called_once_with(73)
    owner.release_pidfds()
    closed.assert_called_once_with(73)
    if entry == "bind-launch":
        assert owner._uncertain is failure
        assert process._astrid_tree_uncertain == str(failure)
    else:
        assert owner._uncertain is None


@pytest.mark.integration
@pytest.mark.skipif(sys.platform != "linux", reason="Linux retained pidfd custody")
def test_pack_host_and_retained_custody_without_stdlib_pidfds(tmp_path, without_stdlib_pidfds):
    from astrid.core.execution.generic_host import GenericPackHost

    host = GenericPackHost(pack_roots=[], attempt_root=tmp_path / "attempts")
    owner = custody.ProcessCustody(scope_root=tmp_path / "custody")
    argv = [sys.executable, "-c", "import time; time.sleep(60)"]
    wrapped, environment = owner.prepare_launch(argv, start_new_session=True)
    assert wrapped == argv and environment == {}
    child = subprocess.Popen(wrapped, start_new_session=True)
    try:
        owner.bind_launch(child)
        birth, descriptor = owner._handles[child.pid]
        assert not os.get_inheritable(descriptor)
        owner.signal(child.pid, birth, 0)
        assert child.poll() is None
        with pytest.raises(custody.CustodyError, match="retained exact process"):
            owner.signal(child.pid, "replacement", platform.TERM)
        assert child.poll() is None
        owner.signal(child.pid, birth, platform.TERM)
        assert child.wait(timeout=5) == -platform.TERM
        owner.release_pidfds(only_exited=True)
        with pytest.raises(OSError) as closed:
            os.fstat(descriptor)
        assert closed.value.errno == errno.EBADF
    finally:
        if child.poll() is None:
            child.kill()
        child.wait(timeout=5)
        owner.release_pidfds()
        host.shutdown()
