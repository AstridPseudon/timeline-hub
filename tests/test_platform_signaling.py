from __future__ import annotations

import ctypes
import errno
import os
import signal
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from runtime_protocol import platform
from tests.lanes import requires_linux_tree_custody


def _syscall_environment(monkeypatch, *, machine="x86_64", widths=(8, 8), multiarch="", result=0):
    syscall = Mock(return_value=result)
    library = Mock(return_value=SimpleNamespace(syscall=syscall))
    monkeypatch.setattr(platform, "sys", SimpleNamespace(
        platform="linux", implementation=SimpleNamespace(_multiarch=multiarch),
    ))
    monkeypatch.setattr(platform.os, "uname", lambda: SimpleNamespace(machine=machine), raising=False)
    monkeypatch.setattr(platform, "ctypes", SimpleNamespace(
        c_int=ctypes.c_int, c_long=ctypes.c_long, c_void_p=ctypes.c_void_p,
        sizeof=lambda kind: widths[0] if kind is ctypes.c_void_p else widths[1],
        CDLL=library, get_errno=lambda: errno.EPERM,
    ))
    return syscall, library


@pytest.mark.parametrize("machine,width,multiarch", [
    ("x86_64", 8, ""),
    ("i386", 4, ""), ("i486", 4, ""), ("i586", 4, ""), ("i686", 4, ""),
    ("aarch64", 8, ""),
    ("armv6l", 4, "arm-linux-gnueabi"),
    ("armv7l", 4, "arm-linux-gnueabihf"),
    ("armv7l", 4, "arm-linux-musleabi"),
    ("armv7l", 4, "arm-linux-musleabihf"),
    ("ppc64", 8, ""), ("ppc64le", 8, ""), ("s390x", 8, ""),
    ("riscv64", 8, ""), ("loongarch64", 8, ""),
])
@pytest.mark.parametrize("operation,arguments,number", [
    ("pidfd_open", (123, 0), 434),
    ("pidfd_send_signal", (18, 0, None, 0), 424),
])
def test_linux_pidfd_syscall_uses_verified_abi_and_typed_arguments(
    monkeypatch, machine, width, multiarch, operation, arguments, number,
):
    syscall, library = _syscall_environment(
        monkeypatch, machine=machine, widths=(width, width), multiarch=multiarch, result=18,
    )
    assert platform._linux_pidfd_syscall(operation, *arguments) == 18
    library.assert_called_once_with(None, use_errno=True)
    assert syscall.argtypes == [ctypes.c_long]
    assert syscall.restype is ctypes.c_long
    actual_number, *actual_arguments = syscall.call_args.args
    assert actual_number == number
    assert tuple(value.value for value in actual_arguments) == arguments
    for value, expected in zip(actual_arguments, arguments):
        assert isinstance(value, ctypes.c_void_p if expected is None else ctypes.c_int)


@pytest.mark.parametrize("machine,widths,multiarch", [
    ("unknown", (8, 8), ""),
    ("mips", (4, 4), "mips-linux-gnu"),
    ("mips64", (8, 8), "mips64-linux-gnuabi64"),
    ("mips64", (4, 4), "mips64-linux-gnuabin32"),
    ("x86_64", (4, 4), "x86_64-linux-gnux32"),
    ("i686", (4, 4), "x86_64-linux-gnux32"),
    ("i686", (4, 4), "x86_64-linux-muslx32"),
    ("x86_64", (8, 4), ""),
    ("i686", (8, 8), ""),
    ("aarch64", (4, 4), ""),
    ("ppc64", (4, 4), ""),
    ("armv7l", (4, 4), "arm-linux-gnu"),
    ("armv6l", (4, 4), ""),
])
def test_linux_pidfd_syscall_refuses_unverified_abi_before_loading_libc(
    monkeypatch, machine, widths, multiarch,
):
    syscall, library = _syscall_environment(
        monkeypatch, machine=machine, widths=widths, multiarch=multiarch,
    )
    with pytest.raises(NotImplementedError, match=f"does not support ABI {machine}"):
        platform._linux_pidfd_syscall("pidfd_open", 123, 0)
    library.assert_not_called()
    syscall.assert_not_called()


def test_pidfd_syscall_fallback_is_linux_only(monkeypatch):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="freebsd"))
    with pytest.raises(NotImplementedError, match="Linux pidfd support"):
        platform._linux_pidfd_syscall("pidfd_open", 123, 0)


def test_linux_pidfd_syscall_refuses_missing_libc_entry_point(monkeypatch):
    _syscall, library = _syscall_environment(monkeypatch)
    library.return_value = SimpleNamespace()
    with pytest.raises(NotImplementedError, match="libc syscall support"):
        platform._linux_pidfd_syscall("pidfd_open", 123, 0)


@pytest.mark.parametrize("operation,arguments", [
    ("pidfd_open", (123, 0)),
    ("pidfd_send_signal", (18, 0, None, 0)),
])
@pytest.mark.parametrize("error", [errno.ENOSYS, errno.ESRCH, errno.EPERM, errno.EINVAL])
def test_linux_pidfd_syscall_preserves_errno(monkeypatch, operation, arguments, error):
    _syscall_environment(monkeypatch, result=-1)
    monkeypatch.setattr(platform.ctypes, "get_errno", lambda: error)
    with pytest.raises(OSError, match=operation) as caught:
        platform._linux_pidfd_syscall(operation, *arguments)
    assert caught.value.errno == error
    assert os.strerror(error) in str(caught.value)


@pytest.mark.parametrize("operation,arguments", [
    ("pidfd_open", (2**32 + 123, 0)),
    ("pidfd_open", (-2**31 - 1, 0)),
    ("pidfd_send_signal", (18, 2**32 + platform.TERM, None, 0)),
])
def test_linux_pidfd_syscall_refuses_integer_wraparound(monkeypatch, operation, arguments):
    syscall, library = _syscall_environment(monkeypatch)
    with pytest.raises(OverflowError, match="does not fit a C int"):
        platform._linux_pidfd_syscall(operation, *arguments)
    library.assert_not_called()
    syscall.assert_not_called()


@pytest.mark.parametrize("missing", [None, "pidfd_open", "pidfd_send_signal", "both"])
def test_linux_signaling_uses_each_available_stdlib_wrapper(monkeypatch, missing):
    expected = {"pid": 123, "uid": 501, "birth_id": "proc-start-ticks:42"}
    calls = []
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    monkeypatch.setattr(platform.os, "pidfd_open", lambda pid: calls.append(("open", pid)) or 18, raising=False)
    monkeypatch.setattr(platform.signal, "pidfd_send_signal", lambda fd, sig: calls.append(("send", fd, sig)), raising=False)
    for module, name in ((platform.os, "pidfd_open"), (platform.signal, "pidfd_send_signal")):
        if missing in (name, "both"):
            monkeypatch.delattr(module, name, raising=False)
    monkeypatch.setattr(platform, "process_identity", lambda pid: calls.append(("observe", pid)) or expected)
    monkeypatch.setattr(platform.os, "close", lambda fd: calls.append(("close", fd)))
    monkeypatch.setattr(platform.os, "kill", lambda *_: pytest.fail("signaling must use a pidfd"))

    def syscall(operation, *arguments):
        calls.append((operation, *arguments))
        return 18 if operation == "pidfd_open" else 0

    monkeypatch.setattr(platform, "_linux_pidfd_syscall", syscall)
    platform.signal_process(expected, platform.TERM)
    assert calls == [
        ("pidfd_open", 123, 0) if missing in ("pidfd_open", "both") else ("open", 123),
        ("observe", 123),
        ("pidfd_send_signal", 18, platform.TERM, None, 0) if missing in ("pidfd_send_signal", "both")
        else ("send", 18, platform.TERM),
        ("close", 18),
    ]


@pytest.mark.parametrize("opener_available", [False, True])
def test_linux_signaling_refuses_unknown_abi_and_closes_any_open_pidfd(monkeypatch, opener_available):
    _syscall, library = _syscall_environment(monkeypatch, machine="mips64")
    expected = {"pid": 123, "uid": 501, "birth_id": "proc-start-ticks:42"}
    observe = Mock(return_value=expected)
    close = Mock()
    monkeypatch.setattr(platform, "process_identity", observe)
    monkeypatch.setattr(platform.os, "close", close)
    monkeypatch.setattr(platform.os, "pidfd_open", lambda _pid: 18, raising=False)
    if not opener_available:
        monkeypatch.delattr(platform.os, "pidfd_open", raising=False)
    monkeypatch.delattr(platform.signal, "pidfd_send_signal", raising=False)
    with pytest.raises(NotImplementedError, match="does not support ABI mips64"):
        platform.signal_process(expected, platform.TERM)
    if opener_available:
        observe.assert_called_once_with(123)
        close.assert_called_once_with(18)
    else:
        observe.assert_not_called()
        close.assert_not_called()
    library.assert_not_called()


def test_linux_signaling_does_not_observe_identity_when_pidfd_open_fails(monkeypatch):
    _syscall_environment(monkeypatch, result=-1)
    monkeypatch.delattr(platform.os, "pidfd_open", raising=False)
    monkeypatch.delattr(platform.signal, "pidfd_send_signal", raising=False)
    observe, close = Mock(), Mock()
    monkeypatch.setattr(platform, "process_identity", observe)
    monkeypatch.setattr(platform.os, "close", close)
    with pytest.raises(PermissionError, match="pidfd_open"):
        platform.signal_process({"pid": 123}, platform.TERM)
    observe.assert_not_called()
    close.assert_not_called()


def test_linux_signaling_closes_pidfd_when_send_syscall_fails(monkeypatch):
    syscall, _library = _syscall_environment(monkeypatch)
    syscall.side_effect = [18, -1]
    expected = {"pid": 123, "uid": 501, "birth_id": "proc-start-ticks:42"}
    monkeypatch.delattr(platform.os, "pidfd_open", raising=False)
    monkeypatch.delattr(platform.signal, "pidfd_send_signal", raising=False)
    monkeypatch.setattr(platform, "process_identity", lambda _pid: expected)
    close = Mock()
    monkeypatch.setattr(platform.os, "close", close)
    with pytest.raises(PermissionError, match="pidfd_send_signal") as caught:
        platform.signal_process(expected, platform.TERM)
    assert caught.value.errno == errno.EPERM
    close.assert_called_once_with(18)


@pytest.fixture
def waiting_child():
    process = subprocess.Popen([sys.executable, "-c", "import sys; sys.stdin.buffer.read()"], stdin=subprocess.PIPE)
    try:
        yield process
    finally:
        process.stdin.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def _record_real_fallback(monkeypatch):
    monkeypatch.delattr(platform.os, "pidfd_open", raising=False)
    monkeypatch.delattr(platform.signal, "pidfd_send_signal", raising=False)
    monkeypatch.setattr(platform.os, "kill", lambda *_: pytest.fail("signaling must use a pidfd"))
    invoke = platform._linux_pidfd_syscall
    opened = []
    operations = []

    def syscall(operation, *arguments):
        operations.append(operation)
        result = invoke(operation, *arguments)
        if operation == "pidfd_open":
            opened.append(result)
        return result

    monkeypatch.setattr(platform, "_linux_pidfd_syscall", syscall)
    return opened, operations


def _assert_closed(fd):
    with pytest.raises(OSError) as caught:
        os.fstat(fd)
    assert caught.value.errno == errno.EBADF


@requires_linux_tree_custody
def test_linux_pidfd_fallback_checks_and_terminates_real_child(monkeypatch, waiting_child):
    expected = platform.process_identity(waiting_child.pid)
    observe = platform.process_identity
    with monkeypatch.context() as patch:
        opened, operations = _record_real_fallback(patch)

        def identity(pid):
            assert opened, "pidfd must open before process identity is observed"
            os.fstat(opened[-1])
            return observe(pid)

        patch.setattr(platform, "process_identity", identity)
        platform.signal_process(expected, 0)
        assert waiting_child.poll() is None
        assert len(opened) == 1
        _assert_closed(opened[-1])
        platform.signal_process(expected, platform.TERM)
        assert waiting_child.wait(timeout=5) == -platform.TERM
        assert len(opened) == 2
        _assert_closed(opened[-1])
        assert operations == ["pidfd_open", "pidfd_send_signal"] * 2


@requires_linux_tree_custody
@pytest.mark.parametrize("mismatch", ["pid", "uid", "birth_id", "absent", "error"])
def test_linux_pidfd_fallback_refuses_changed_or_unknown_identity(monkeypatch, waiting_child, mismatch):
    expected = platform.process_identity(waiting_child.pid)
    observed = dict(expected)
    if mismatch in ("pid", "uid"):
        observed[mismatch] += 1
    elif mismatch == "birth_id":
        observed[mismatch] += ":changed"
    with monkeypatch.context() as patch:
        opened, operations = _record_real_fallback(patch)

        def identity(_pid):
            assert opened, "pidfd must open before process identity is observed"
            os.fstat(opened[-1])
            if mismatch == "error":
                raise PermissionError(errno.EACCES, "identity observation denied")
            return None if mismatch == "absent" else observed

        patch.setattr(platform, "process_identity", identity)
        with pytest.raises(OSError, match="identity observation denied" if mismatch == "error" else "incarnation changed"):
            platform.signal_process(expected, platform.TERM)
        assert len(opened) == 1
        assert operations == ["pidfd_open"]
        _assert_closed(opened[0])
        assert waiting_child.poll() is None


@requires_linux_tree_custody
@pytest.mark.parametrize("signum", [-1, 2**32 + platform.TERM])
def test_linux_pidfd_fallback_rejects_invalid_signal_without_terminating_child(monkeypatch, waiting_child, signum):
    expected = platform.process_identity(waiting_child.pid)
    with monkeypatch.context() as patch:
        opened, _operations = _record_real_fallback(patch)
        with pytest.raises(OSError if signum < 0 else OverflowError) as caught:
            platform.signal_process(expected, signum)
        if signum < 0:
            assert caught.value.errno == errno.EINVAL
        assert len(opened) == 1
        _assert_closed(opened[0])
        assert waiting_child.poll() is None
