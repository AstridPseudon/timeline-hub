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

    def open_pidfd(pid, flags=0):
        assert flags == 0
        calls.append(("open", pid))
        return 18

    def send_signal(fd, sig, siginfo=None, flags=0):
        assert siginfo is None
        assert flags == 0
        calls.append(("send", fd, sig))

    monkeypatch.setattr(platform.os, "pidfd_open", open_pidfd, raising=False)
    monkeypatch.setattr(platform.signal, "pidfd_send_signal", send_signal, raising=False)
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
    opener = Mock(return_value=18)
    monkeypatch.setattr(platform.os, "pidfd_open", opener, raising=False)
    if not opener_available:
        monkeypatch.delattr(platform.os, "pidfd_open", raising=False)
    monkeypatch.delattr(platform.signal, "pidfd_send_signal", raising=False)
    with pytest.raises(NotImplementedError, match="does not support ABI mips64"):
        platform.signal_process(expected, platform.TERM)
    if opener_available:
        opener.assert_called_once_with(123, 0)
        observe.assert_called_once_with(123)
        close.assert_called_once_with(18)
    else:
        opener.assert_not_called()
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


@pytest.mark.parametrize("wrapper_available", [False, True])
@pytest.mark.parametrize("operation,arguments,stdlib_arguments,syscall_arguments,result", [
    ("pidfd_open", (123,), (123, 0), (123, 0), 18),
    ("pidfd_open", (123, 0x800), (123, 0x800), (123, 0x800), 18),
    ("pidfd_send_signal", (18, platform.TERM), (18, platform.TERM, None, 0), (18, platform.TERM, None, 0), None),
    ("pidfd_send_signal", (18, platform.TERM, None, 1), (18, platform.TERM, None, 1), (18, platform.TERM, None, 1), None),
])
def test_public_pidfd_helpers_select_wrappers_independently_and_preserve_arguments(
    monkeypatch, wrapper_available, operation, arguments, stdlib_arguments, syscall_arguments, result,
):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    monkeypatch.delattr(platform.os, "pidfd_open", raising=False)
    monkeypatch.delattr(platform.signal, "pidfd_send_signal", raising=False)
    wrapper = Mock(return_value=result)
    if wrapper_available:
        module = platform.os if operation == "pidfd_open" else platform.signal
        monkeypatch.setattr(module, operation, wrapper, raising=False)
    syscall = Mock(return_value=18 if operation == "pidfd_open" else 0)
    monkeypatch.setattr(platform, "_linux_pidfd_syscall", syscall)
    monkeypatch.setattr(platform, "process_identity", lambda *_: pytest.fail("caller owns identity checks"))
    monkeypatch.setattr(platform.os, "close", lambda *_: pytest.fail("caller owns fd closure"))
    actual = getattr(platform, operation)(*arguments)
    if result is None:
        assert actual is None
    else:
        assert actual == result
    if wrapper_available:
        wrapper.assert_called_once_with(*stdlib_arguments)
        syscall.assert_not_called()
    else:
        wrapper.assert_not_called()
        syscall.assert_called_once_with(operation, *syscall_arguments)


def test_public_pidfd_send_signal_preserves_siginfo_for_stdlib(monkeypatch):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    siginfo = object()
    sender = Mock(return_value=None)
    monkeypatch.setattr(platform.signal, "pidfd_send_signal", sender, raising=False)
    monkeypatch.setattr(platform, "_linux_pidfd_syscall", lambda *_: pytest.fail("stdlib wrapper is available"))
    assert platform.pidfd_send_signal(18, platform.TERM, siginfo=siginfo, flags=1) is None
    sender.assert_called_once_with(18, platform.TERM, siginfo, 1)


@pytest.mark.parametrize("siginfo", [object(), 0, False])
def test_public_pidfd_send_signal_fallback_refuses_non_null_siginfo(monkeypatch, siginfo):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    monkeypatch.delattr(platform.signal, "pidfd_send_signal", raising=False)
    syscall = Mock()
    monkeypatch.setattr(platform, "_linux_pidfd_syscall", syscall)
    monkeypatch.setattr(platform.os, "close", lambda *_: pytest.fail("caller owns fd closure"))
    with pytest.raises(NotImplementedError, match="does not support siginfo"):
        platform.pidfd_send_signal(18, platform.TERM, siginfo)
    syscall.assert_not_called()


@pytest.mark.parametrize("os_name", ["freebsd", "darwin", "win32"])
@pytest.mark.parametrize("operation,arguments", [
    ("pidfd_open", (123,)),
    ("pidfd_send_signal", (18, platform.TERM)),
])
def test_public_pidfd_helpers_require_linux_even_with_stdlib_wrapper(monkeypatch, os_name, operation, arguments):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform=os_name))
    wrapper = Mock()
    module = platform.os if operation == "pidfd_open" else platform.signal
    monkeypatch.setattr(module, operation, wrapper, raising=False)
    syscall = Mock()
    monkeypatch.setattr(platform, "_linux_pidfd_syscall", syscall)
    with pytest.raises(NotImplementedError, match="Linux pidfd support"):
        getattr(platform, operation)(*arguments)
    wrapper.assert_not_called()
    syscall.assert_not_called()


@pytest.mark.parametrize("wrapper_available", [False, True])
@pytest.mark.parametrize("operation,arguments", [
    ("pidfd_open", (123,)),
    ("pidfd_send_signal", (18, platform.TERM)),
])
@pytest.mark.parametrize("error_number", [errno.EPERM, errno.ENOSYS])
def test_public_pidfd_helpers_propagate_errors_without_closing_fd(
    monkeypatch, wrapper_available, operation, arguments, error_number,
):
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    error = OSError(error_number, "pidfd operation failed")
    module = platform.os if operation == "pidfd_open" else platform.signal
    if wrapper_available:
        monkeypatch.setattr(module, operation, Mock(side_effect=error), raising=False)
        monkeypatch.setattr(platform, "_linux_pidfd_syscall", lambda *_: pytest.fail("stdlib error must propagate"))
    else:
        monkeypatch.delattr(module, operation, raising=False)
        monkeypatch.setattr(platform, "_linux_pidfd_syscall", Mock(side_effect=error))
    monkeypatch.setattr(platform.os, "close", lambda *_: pytest.fail("caller owns fd closure"))
    with pytest.raises(OSError) as caught:
        getattr(platform, operation)(*arguments)
    assert caught.value is error
    assert caught.value.errno == error_number


def test_signal_process_uses_public_pidfd_helpers(monkeypatch):
    expected = {"pid": 123, "uid": 501, "birth_id": "proc-start-ticks:42"}
    calls = []
    monkeypatch.setattr(platform, "sys", SimpleNamespace(platform="linux"))
    monkeypatch.setattr(platform, "pidfd_open", lambda pid: calls.append(("open", pid)) or 18)
    monkeypatch.setattr(platform, "process_identity", lambda pid: calls.append(("observe", pid)) or expected)
    monkeypatch.setattr(platform, "pidfd_send_signal", lambda fd, sig: calls.append(("send", fd, sig)))
    monkeypatch.setattr(platform.os, "close", lambda fd: calls.append(("close", fd)))
    monkeypatch.setattr(platform.os, "pidfd_open", lambda *_: pytest.fail("use the public helper"), raising=False)
    monkeypatch.setattr(platform.signal, "pidfd_send_signal", lambda *_: pytest.fail("use the public helper"), raising=False)
    platform.signal_process(expected, platform.TERM)
    assert calls == [("open", 123), ("observe", 123), ("send", 18, platform.TERM), ("close", 18)]


@requires_linux_tree_custody
def test_public_pidfd_helpers_fallback_signals_real_child_and_retains_fd(monkeypatch, waiting_child):
    expected = platform.process_identity(waiting_child.pid)
    with monkeypatch.context() as patch:
        opened, operations = _record_real_fallback(patch)
        fd = platform.pidfd_open(waiting_child.pid, 0)
        try:
            assert fd == opened[0]
            assert not os.get_inheritable(fd)
            observed = platform.process_identity(waiting_child.pid)
            assert all(observed.get(key) == expected.get(key) for key in ("pid", "uid", "birth_id"))
            assert platform.pidfd_send_signal(fd, 0, None, 0) is None
            assert waiting_child.poll() is None
            os.fstat(fd)
            assert platform.pidfd_send_signal(fd, platform.TERM) is None
            assert waiting_child.wait(timeout=5) == -platform.TERM
            os.fstat(fd)
        finally:
            os.close(fd)
        _assert_closed(fd)
        assert operations == ["pidfd_open", "pidfd_send_signal", "pidfd_send_signal"]


@requires_linux_tree_custody
@pytest.mark.parametrize("signum,siginfo,error_type,error_number", [
    (-1, None, OSError, errno.EINVAL),
    (2**32 + platform.TERM, None, OverflowError, None),
    (platform.TERM, object(), NotImplementedError, None),
])
def test_public_pidfd_send_signal_fallback_errors_retain_real_fd(
    monkeypatch, waiting_child, signum, siginfo, error_type, error_number,
):
    with monkeypatch.context() as patch:
        _record_real_fallback(patch)
        fd = platform.pidfd_open(waiting_child.pid)
        try:
            with pytest.raises(error_type) as caught:
                platform.pidfd_send_signal(fd, signum, siginfo)
            if error_number is not None:
                assert caught.value.errno == error_number
            assert waiting_child.poll() is None
            os.fstat(fd)
        finally:
            os.close(fd)
        _assert_closed(fd)
