"""The Runtime's native OS boundary (stdlib only).

Windows permissions use owner/SYSTEM protected DACLs and handle-based checks.
Process identities are observations, never signal authority;
``signal_process`` pins a kernel handle before comparing an expected identity.
"""
from __future__ import annotations

from contextlib import contextmanager, nullcontext
import ctypes
import errno
import hashlib
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import threading
import time

from . import cancellation

TERM = int(signal.SIGTERM)
KILL = int(getattr(signal, "SIGKILL", 9))
USER1 = int(signal.SIGUSR1) if hasattr(signal, "SIGUSR1") else None
_directory_mutex_guard = threading.Lock()
_directory_mutexes: dict[int, tuple[int, threading.Lock, int]] = {}
_directory_mutex_gates: dict[str, threading.Lock] = {}


def current_user() -> int:
    """UID on POSIX; an opaque, stable integer derived from the token SID on Windows."""
    if sys.platform != "win32":
        return os.getuid()
    return _windows_user(_kernel().GetCurrentProcess())


def data_root(home: Path | str | None = None) -> Path:
    home = Path(home).expanduser() if home is not None else Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "Astrid Runtime"
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA") or home / "AppData" / "Local") / "Astrid Runtime"
    return Path(os.environ.get("XDG_DATA_HOME") or home / ".local" / "share") / "astrid-runtime"


def log_dir(home: Path | str | None = None) -> Path:
    home = Path(home).expanduser() if home is not None else Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Logs" / "Astrid Runtime"
    if sys.platform == "win32":
        return data_root(home) / "logs"
    return Path(os.environ.get("XDG_STATE_HOME") or home / ".local" / "state") / "astrid-runtime" / "logs"


def owner_only(path_or_fd, *, directory: bool | None = None) -> None:
    """Apply 0600/0700 or a protected owner/SYSTEM DACL."""
    if sys.platform == "win32":
        from .windows_security import restrict
        restrict(path_or_fd)
        return
    value = os.fstat(path_or_fd) if isinstance(path_or_fd, int) else os.stat(path_or_fd, follow_symlinks=False)
    if stat.S_ISLNK(value.st_mode):
        raise OSError(errno.ELOOP, "owner-only permissions cannot be applied through a symlink")
    directory = stat.S_ISDIR(value.st_mode) if directory is None else directory
    if isinstance(path_or_fd, int):
        os.fchmod(path_or_fd, 0o700 if directory else 0o600)
    else:
        os.chmod(path_or_fd, 0o700 if directory else 0o600)


def is_owner_only(path_or_fd_or_stat, *, directory: bool | None = None) -> bool:
    """Check native owner and access permissions; stat alone cannot check a DACL."""
    if sys.platform == "win32":
        if isinstance(path_or_fd_or_stat, os.stat_result):
            return False
        from .windows_security import validate
        try:
            validate(path_or_fd_or_stat)
            return True
        except OSError:
            return False
    try:
        value = path_or_fd_or_stat
        if not isinstance(value, os.stat_result):
            value = os.fstat(value) if isinstance(value, int) else os.stat(value, follow_symlinks=False)
        if stat.S_ISLNK(value.st_mode):
            return False
        directory = stat.S_ISDIR(value.st_mode) if directory is None else directory
        return value.st_uid == current_user() and stat.S_IMODE(value.st_mode) == (0o700 if directory else 0o600)
    except OSError:
        return False


def is_current_user(metadata) -> bool:
    """Ownership-only check for artifacts whose existing mode is not restricted."""
    return sys.platform == "win32" or metadata.st_uid == current_user()


def private_directory(path) -> None:
    if sys.platform == "win32":
        from .windows_security import private_directory as create
        create(path)
    else:
        Path(path).mkdir(parents=True, exist_ok=True)
        owner_only(path, directory=True)


def private_temporary(directory, prefix):
    if sys.platform == "win32":
        from .windows_security import private_temporary as create
        return create(directory, prefix)
    import tempfile
    return tempfile.mkstemp(dir=directory, prefix=prefix)


def read_private_file(path):
    if sys.platform == "win32":
        from .windows_security import read_private
        return read_private(path)
    return Path(path).read_bytes()


def lock_file(fd: int, *, exclusive: bool = True, blocking: bool = True) -> None:
    if blocking and cancellation.active():
        while True:
            cancellation.check()
            try:
                return _lock_file(fd, exclusive=exclusive, blocking=False)
            except BlockingIOError:
                cancellation.pause(0.05)
    return _lock_file(fd, exclusive=exclusive, blocking=blocking)


def _lock_file(fd: int, *, exclusive: bool = True, blocking: bool = True) -> None:
    if sys.platform != "win32":
        import fcntl
        fcntl.flock(fd, (fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH) | (0 if blocking else fcntl.LOCK_NB))
        return
    info = os.fstat(fd)
    if stat.S_ISDIR(info.st_mode):
        if not exclusive:
            raise NotImplementedError("shared Windows directory locks are not supported")
        with _directory_mutex_guard:
            held = _directory_mutexes.get(fd)
            if held is not None and held[2] == threading.get_ident():
                return
        handle, gate, owner_thread = _lock_windows_directory(fd, info, blocking=blocking)
        with _directory_mutex_guard:
            _directory_mutexes[fd] = (handle, gate, owner_thread)
        return
    import msvcrt
    from ctypes import wintypes
    overlap = _windows_overlapped()
    kernel = _kernel()
    kernel.LockFileEx.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p]
    kernel.LockFileEx.restype = wintypes.BOOL
    if not kernel.LockFileEx(wintypes.HANDLE(msvcrt.get_osfhandle(fd)),
                             (2 if exclusive else 0) | (0 if blocking else 1),
                             0, 1, 0, ctypes.byref(overlap)):
        error = ctypes.get_last_error()
        if error in (33, 158):
            raise BlockingIOError(errno.EAGAIN, "file is locked")
        raise ctypes.WinError(error)


def unlock_file(fd: int) -> None:
    if sys.platform != "win32":
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN)
        return
    import msvcrt
    from ctypes import wintypes
    with _directory_mutex_guard:
        held = _directory_mutexes.get(fd)
        if held is not None and held[2] != threading.get_ident():
            raise RuntimeError("Windows directory locks must be released by their acquiring thread")
        if held is not None:
            del _directory_mutexes[fd]
    if held is not None:
        mutex, gate, _owner_thread = held
        kernel = _kernel()
        kernel.ReleaseMutex.argtypes = [wintypes.HANDLE]
        kernel.ReleaseMutex.restype = wintypes.BOOL
        if not kernel.ReleaseMutex(wintypes.HANDLE(mutex)):
            error = ctypes.get_last_error()
            kernel.CloseHandle(wintypes.HANDLE(mutex))
            gate.release()
            raise ctypes.WinError(error)
        kernel.CloseHandle(wintypes.HANDLE(mutex))
        gate.release()
        return
    overlap = _windows_overlapped()
    kernel = _kernel()
    kernel.UnlockFileEx.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p]
    kernel.UnlockFileEx.restype = wintypes.BOOL
    if not kernel.UnlockFileEx(wintypes.HANDLE(msvcrt.get_osfhandle(fd)), 0, 1, 0, ctypes.byref(overlap)):
        error = ctypes.get_last_error()
        if error != 158:  # unlock after an unsuccessful nonblocking acquisition
            raise ctypes.WinError(error)


def _windows_overlapped():
    """Return a correctly aligned OVERLAPPED for both Windows pointer sizes."""
    from ctypes import wintypes

    class Overlapped(ctypes.Structure):
        _fields_ = [
            ("Internal", ctypes.c_size_t),
            ("InternalHigh", ctypes.c_size_t),
            ("Offset", wintypes.DWORD),
            ("OffsetHigh", wintypes.DWORD),
            ("hEvent", wintypes.HANDLE),
        ]
    return Overlapped()


def _lock_windows_directory(fd: int, info, *, blocking: bool) -> tuple[int, threading.Lock, int]:
    """Lock a directory identity with an abandoned-aware named mutex.

    LockFileEx does not accept directory handles. Windows file IDs and volume
    serials identify the retained directory independently of its path. The
    non-reentrant in-process gate prevents Win32 mutex same-thread recursion;
    acquisition and release must occur on the same thread.
    """
    from ctypes import wintypes
    identity = f"{current_user()}:{int(info.st_dev)}:{int(info.st_ino)}".encode()
    name = "Local\\AstridRuntime.directory." + hashlib.sha256(identity).hexdigest()
    kernel = _kernel()
    with _directory_mutex_guard:
        gate = _directory_mutex_gates.setdefault(name, threading.Lock())
    if not gate.acquire(blocking=blocking):
        raise BlockingIOError(errno.EAGAIN, "directory is locked")
    kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    kernel.CreateMutexW.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.WaitForSingleObject.restype = wintypes.DWORD
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    mutex = kernel.CreateMutexW(None, False, name)
    if not mutex:
        gate.release()
        raise ctypes.WinError(ctypes.get_last_error())
    result = int(kernel.WaitForSingleObject(mutex, 0xFFFFFFFF if blocking else 0))
    if result in (0, 0x80):  # WAIT_OBJECT_0 or WAIT_ABANDONED
        return int(mutex), gate, threading.get_ident()
    error = ctypes.get_last_error()
    kernel.CloseHandle(mutex)
    gate.release()
    if result == 0x102:  # WAIT_TIMEOUT
        raise BlockingIOError(errno.EAGAIN, "directory is locked")
    if result == 0xFFFFFFFF:  # WAIT_FAILED
        raise ctypes.WinError(error)
    raise OSError(f"unexpected Windows directory lock wait status: {result}")


@contextmanager
def file_lock(path_or_fd, *, exclusive: bool = True, blocking: bool = True):
    own = not isinstance(path_or_fd, int)
    if own:
        from .dirfd import filesystem
        fd = filesystem.open(
            path_or_fd,
            os.O_RDWR | os.O_CREAT | getattr(filesystem, "O_NOFOLLOW", 0),
            0o600,
        )
    else:
        fd = path_or_fd
    locked = False
    try:
        if own:
            owner_only(fd)
        lock_file(fd, exclusive=exclusive, blocking=blocking)
        locked = True
        yield fd
    finally:
        if locked:
            unlock_file(fd)
        if own:
            os.close(fd)


class _DarwinBSDInfo(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint32) for name in (
        "flags", "status", "xstatus", "pid", "ppid", "uid", "gid", "ruid", "rgid", "svuid", "svgid", "reserved",
    )] + [("comm", ctypes.c_char * 16), ("name", ctypes.c_char * 32)] + [
        (name, ctypes.c_uint32) for name in ("nfiles", "pgid", "pjobc", "tdev", "tpgid")
    ] + [("nice", ctypes.c_int32), ("start_sec", ctypes.c_uint64), ("start_usec", ctypes.c_uint64)]


def _read_darwin_process_info(pid: int, *, include_exit: bool = False):
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    reader = library.proc_pidinfo
    reader.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
    reader.restype = ctypes.c_int
    value = _DarwinBSDInfo()
    ctypes.set_errno(0)
    count = reader(pid, 3, 0, ctypes.byref(value), ctypes.sizeof(value))
    error = ctypes.get_errno()
    if count == 0 and error == errno.ESRCH:
        return None
    if count != ctypes.sizeof(value) or error:
        raise OSError(error, "native process identity observation failed or was partial")
    if value.pid != pid or value.start_sec == 0 or value.start_usec >= 1_000_000:
        raise OSError("native process identity observation was malformed")
    return {"pid": int(value.pid), "uid": int(value.uid), "parent_pid": int(value.ppid),
            "start_sec": int(value.start_sec), "start_usec": int(value.start_usec),
            **({"status": int(value.status)} if include_exit else {})}


def _kernel():
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    return kernel


def _windows_user(handle) -> int:
    from ctypes import wintypes
    advapi = ctypes.WinDLL("advapi32", use_last_error=True)
    advapi.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    advapi.OpenProcessToken.restype = wintypes.BOOL
    advapi.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    advapi.GetTokenInformation.restype = wintypes.BOOL
    advapi.GetLengthSid.argtypes = [ctypes.c_void_p]
    advapi.GetLengthSid.restype = wintypes.DWORD
    token = wintypes.HANDLE()
    if not advapi.OpenProcessToken(handle, 8, ctypes.byref(token)):
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        size = wintypes.DWORD()
        advapi.GetTokenInformation(token, 1, None, 0, ctypes.byref(size))
        buffer = ctypes.create_string_buffer(size.value)
        if not advapi.GetTokenInformation(token, 1, buffer, size, ctypes.byref(size)):
            raise ctypes.WinError(ctypes.get_last_error())
        sid = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_void_p))[0]
        sid_size = int(advapi.GetLengthSid(sid))
        if sid_size <= 0:
            raise OSError("current process token contains an invalid SID")
        # Runtime's persisted UID field is a signed SQLite INTEGER. Keep the
        # SID-derived identifier stable and within its non-negative range.
        return int.from_bytes(hashlib.sha256(ctypes.string_at(sid, sid_size)).digest()[:8], "big") & 0x7FFF_FFFF_FFFF_FFFF
    finally:
        _kernel().CloseHandle(token)


def _windows_identity(pid: int, handle):
    from ctypes import wintypes
    kernel = _kernel()
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    times = [wintypes.FILETIME() for _ in range(4)]
    if not kernel.GetProcessTimes(handle, *[ctypes.byref(value) for value in times]):
        raise ctypes.WinError(ctypes.get_last_error())
    created = (times[0].dwHighDateTime << 32) | times[0].dwLowDateTime
    try:
        parent_pid = _windows_parent(pid)
    except (OSError, ProcessLookupError):
        # Parent enumeration is an optional observation and may race process
        # exit; it must not invalidate the kernel-backed identity fields.
        parent_pid = None
    return {"pid": pid, "uid": _windows_user(handle), "parent_pid": parent_pid,
            "birth_id": f"windows-creation:{created}", "process_group": pid, "session_id": pid}


def _windows_process_active(handle) -> bool:
    from ctypes import wintypes
    kernel = _kernel()
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.WaitForSingleObject.restype = wintypes.DWORD
    result = int(kernel.WaitForSingleObject(handle, 0))
    if result == 0x102:  # WAIT_TIMEOUT means the process object is unsignaled.
        return True
    if result == 0:  # WAIT_OBJECT_0 proves the process has exited.
        return False
    if result == 0xFFFFFFFF:  # WAIT_FAILED
        raise ctypes.WinError(ctypes.get_last_error())
    raise OSError(f"unexpected Windows process wait status: {result}")


def _windows_parent(pid):
    from ctypes import wintypes
    class Entry(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD), ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.c_size_t), ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", ctypes.c_long),
                    ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260)]
    kernel = _kernel()
    kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(Entry)]
    kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(Entry)]
    kernel.Process32FirstW.restype = wintypes.BOOL
    kernel.Process32NextW.restype = wintypes.BOOL
    snapshot = kernel.CreateToolhelp32Snapshot(2, 0)
    if snapshot == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        entry = Entry(); entry.dwSize = ctypes.sizeof(entry)
        found = kernel.Process32FirstW(snapshot, ctypes.byref(entry))
        while found:
            if entry.th32ProcessID == pid:
                return int(entry.th32ParentProcessID)
            found = kernel.Process32NextW(snapshot, ctypes.byref(entry))
        raise ProcessLookupError(pid)
    finally:
        kernel.CloseHandle(snapshot)


def process_identity(pid: int, *, timeout: float = 1.0):
    """Return identity, None only for proven absence; raise on unknown observation."""
    if timeout <= 0:
        raise OSError("process identity observation deadline expired")
    if pid <= 0:
        return None
    if sys.platform == "darwin":
        deadline = time.monotonic() + timeout
        first = _read_darwin_process_info(pid)
        if first is None:
            return None
        second = _read_darwin_process_info(pid)
        if time.monotonic() >= deadline:
            raise OSError("process identity observation deadline expired")
        if first != second:
            raise OSError("native process identity changed during observation")
        local = time.localtime(first["start_sec"])
        birth = ("ps-lstart:" + time.strftime("%a %b ", local) + f"{local.tm_mday:2d}"
                 + time.strftime(" %H:%M:%S %Y", local))
        return {"pid": first["pid"], "uid": first["uid"], "parent_pid": first["parent_pid"], "birth_id": birth}
    if sys.platform == "win32":
        kernel = _kernel()
        handle = kernel.OpenProcess(0x1000 | 0x00100000, False, pid)  # QUERY_LIMITED_INFORMATION | SYNCHRONIZE
        if not handle:
            if ctypes.get_last_error() == 87:
                return None
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            if not _windows_process_active(handle):
                return None
            try:
                identity = _windows_identity(pid, handle)
            except OSError:
                if not _windows_process_active(handle):
                    return None
                raise
            if not _windows_process_active(handle):
                return None
            return identity
        finally:
            kernel.CloseHandle(handle)
    root = Path("/proc") / str(pid)
    try:
        raw = (root / "stat").read_text()
        fields = raw.rsplit(")", 1)[1].split()
        value = {"pid": pid, "uid": root.stat().st_uid, "parent_pid": int(fields[1]),
                 "birth_id": f"proc-start-ticks:{fields[19]}", "process_group": int(fields[2]), "session_id": int(fields[3])}
        second = (root / "stat").read_text().rsplit(")", 1)[1].split()
        if fields[19] != second[19]:
            raise OSError("process identity changed during observation")
        if second[0] in {"Z", "X", "x"}:
            return None  # /proc still retains an exited process awaiting reap.
        return value
    except FileNotFoundError:
        return None
    except (ValueError, IndexError) as exc:
        raise OSError("process identity observation was malformed") from exc


def process_executable(pid: int) -> str:
    if sys.platform == "darwin":
        library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
        library.proc_pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
        library.proc_pidpath.restype = ctypes.c_int
        buffer = ctypes.create_string_buffer(4096)
        if library.proc_pidpath(int(pid), buffer, len(buffer)) <= 0:
            raise OSError(ctypes.get_errno(), "process executable observation failed")
        return os.fsdecode(buffer.value)
    if sys.platform != "win32":
        return str((Path("/proc") / str(pid) / "exe").resolve(strict=True))
    from ctypes import wintypes
    kernel = _kernel(); handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        kernel.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        buffer = ctypes.create_unicode_buffer(32768); size = wintypes.DWORD(len(buffer))
        if not kernel.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            raise ctypes.WinError(ctypes.get_last_error())
        return buffer.value
    finally:
        kernel.CloseHandle(handle)


def process_group(pid):
    return pid if sys.platform == "win32" else os.getpgid(pid)


def session_id(pid):
    return pid if sys.platform == "win32" else os.getsid(pid)


def start_session() -> None:
    """Create a POSIX session before exec; Windows spawn_tree creates a group."""
    if sys.platform != "win32":
        os.setsid()


def validate_child_reaper(child):
    """Return the Popen wait guard after rejecting unsafe POSIX auto-reaping."""
    if sys.platform != "win32" and signal.getsignal(signal.SIGCHLD) != signal.SIG_DFL:
        raise RuntimeError("retained child cannot bind with automatic reaping")
    wait_guard = getattr(child, "_waitpid_lock", None)
    if wait_guard is None:
        if sys.platform == "win32":
            return nullcontext()
        raise RuntimeError("retained child has no serialized wait ownership")
    return wait_guard


class _Job:
    """A non-inheritable kill-on-close Job Object owning a complete process tree."""
    def __init__(self):
        from ctypes import wintypes
        class Basic(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD)]
        class IO(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint64) for name in ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount", "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]
        class Extended(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", Basic), ("IoInfo", IO), ("ProcessMemoryLimit", ctypes.c_size_t),
                        ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]
        kernel = _kernel()
        kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        kernel.CreateJobObjectW.restype = wintypes.HANDLE
        kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        kernel.SetInformationJobObject.restype = wintypes.BOOL
        self.handle = kernel.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = Extended(); limits.BasicLimitInformation.LimitFlags = 0x2000
        if not kernel.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            self.close(); raise ctypes.WinError(ctypes.get_last_error())

    def assign(self, process):
        from ctypes import wintypes
        kernel = _kernel()
        kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        kernel.AssignProcessToJobObject.restype = wintypes.BOOL
        if not kernel.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if getattr(self, "handle", None):
            _kernel().CloseHandle(self.handle); self.handle = None

    def __del__(self):
        self.close()


def _resume_process(pid):
    from ctypes import wintypes
    class ThreadEntry(ctypes.Structure):
        _fields_ = [(name, wintypes.DWORD) for name in ("dwSize", "cntUsage", "th32ThreadID", "th32OwnerProcessID")] + [("tpBasePri", ctypes.c_long), ("tpDeltaPri", ctypes.c_long), ("dwFlags", wintypes.DWORD)]
    kernel = _kernel()
    kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(ThreadEntry)]
    kernel.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(ThreadEntry)]
    kernel.Thread32First.restype = wintypes.BOOL
    kernel.Thread32Next.restype = wintypes.BOOL
    kernel.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenThread.restype = wintypes.HANDLE
    kernel.ResumeThread.argtypes = [wintypes.HANDLE]
    kernel.ResumeThread.restype = wintypes.DWORD
    snapshot = kernel.CreateToolhelp32Snapshot(4, 0)
    if snapshot == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        entry = ThreadEntry(); entry.dwSize = ctypes.sizeof(entry)
        found = kernel.Thread32First(snapshot, ctypes.byref(entry))
        while found:
            if entry.th32OwnerProcessID == pid:
                handle = kernel.OpenThread(2, False, entry.th32ThreadID)
                if not handle:
                    raise ctypes.WinError(ctypes.get_last_error())
                try:
                    if kernel.ResumeThread(handle) == 0xFFFFFFFF:
                        raise ctypes.WinError(ctypes.get_last_error())
                    return
                finally:
                    kernel.CloseHandle(handle)
            found = kernel.Thread32Next(snapshot, ctypes.byref(entry))
        raise ProcessLookupError(pid)
    finally:
        kernel.CloseHandle(snapshot)


def spawn_tree(argv, *, detached=False, hidden=False, **kwargs):
    """Spawn a session/Job, assigning Windows children before their first instruction.

    Detached Windows daemons inherit the sole extra Job handle, so launcher
    exit preserves the daemon, and daemon exit still kills its descendants.
    """
    if sys.platform != "win32":
        kwargs.setdefault("start_new_session", True)
        return subprocess.Popen(argv, **kwargs)
    kwargs.pop("start_new_session", None)
    if kwargs.pop("pass_fds", ()):
        raise NotImplementedError("Windows worker descriptor handoff is unavailable")
    job = _Job()
    if detached:
        os.set_handle_inheritable(job.handle, True)
        startup = kwargs.setdefault("startupinfo", subprocess.STARTUPINFO())
        attributes = dict(startup.lpAttributeList or {})
        attributes["handle_list"] = [*attributes.get("handle_list", []), job.handle]
        startup.lpAttributeList = attributes
        kwargs["env"] = dict(kwargs.get("env") or os.environ)
        kwargs["env"]["ASTRID_RUNTIME_JOB_HANDLE"] = str(job.handle)
        kwargs["close_fds"] = True
    process = None
    try:
        kwargs["creationflags"] = kwargs.get("creationflags", 0) | 0x200 | 0x4 | (0x08000000 if hidden else 0)
        process = subprocess.Popen(argv, **kwargs)
        job.assign(process)
        process._runtime_job = job
        _resume_process(process.pid)
        return process
    except BaseException:
        if process is not None:
            process.kill(); process.wait()
        job.close()
        raise
    finally:
        if detached and job.handle:
            os.set_handle_inheritable(job.handle, False)


def signal_tree(process_or_pid, signum):
    pid = process_or_pid if isinstance(process_or_pid, int) else process_or_pid.pid
    if sys.platform == "linux":
        if isinstance(process_or_pid, int):
            raise ProcessLookupError("process-group custody requires an unreaped child")
        with getattr(process_or_pid, "_waitpid_lock", nullcontext()):
            _signal_linux_group(process_or_pid, signum)
    elif sys.platform != "win32":
        os.killpg(pid, signum)
    elif signum == KILL:
        job = getattr(process_or_pid, "_runtime_job", None)
        if job:
            from ctypes import wintypes
            kernel = _kernel(); kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
            if not kernel.TerminateJobObject(job.handle, 1):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            signal_process(process_identity(pid), KILL)
    else:
        os.kill(pid, signal.CTRL_BREAK_EVENT)


def tree_exited(process):
    """Observe exit without reaping a POSIX tree's process-group anchor.

    The caller must remain the sole waiter until stop_tree has killed any
    surviving descendants. Windows retains that authority in the Job handle.
    """
    if sys.platform == "linux":
        with getattr(process, "_waitpid_lock", nullcontext()):
            if process.returncode is not None:
                return True
            return os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT) is not None
    if sys.platform == "darwin":
        with getattr(process, "_waitpid_lock", nullcontext()):
            return _darwin_tree_exited(process)
    return process.poll() is not None


def _darwin_tree_exited(process):
    if process.returncode is not None:
        return True
    info = _read_darwin_process_info(process.pid, include_exit=True)
    return info is None or info["status"] == 5  # SZOMB


def stop_tree(process, grace=5.0):
    if sys.platform == "linux":
        return _stop_linux_tree(process, grace)
    if sys.platform == "darwin":
        # Keep the unreaped leader until the last group signal, as on Linux.
        with getattr(process, "_waitpid_lock", nullcontext()):
            if process.returncode is not None:
                return
            if not _darwin_tree_exited(process):
                try:
                    signal_tree(process, TERM)
                except ProcessLookupError:
                    pass
                deadline = time.monotonic() + grace
                while time.monotonic() < deadline and not _darwin_tree_exited(process):
                    time.sleep(min(0.05, max(0, deadline - time.monotonic())))
            try:
                signal_tree(process, KILL)
            except ProcessLookupError:
                pass
        process.wait(timeout=max(2.0, grace))
        return
    try:
        if process.poll() is None:
            try:
                signal_tree(process, TERM)
            except (OSError, ValueError):
                if sys.platform != "win32":
                    raise
            try:
                process.wait(timeout=grace)
            except subprocess.TimeoutExpired:
                signal_tree(process, KILL)
                process.wait(timeout=max(2.0, grace))
        # Kill any descendants which outlived their session leader.
        if sys.platform != "win32":
            try:
                signal_tree(process, KILL)
            except ProcessLookupError:
                pass
    finally:
        job = getattr(process, "_runtime_job", None)
        if job:
            job.close()


def _stop_linux_tree(process, grace):
    # poll()/wait() reap the leader and release its numeric PID/PGID. Hold
    # Popen's wait lock and use WNOWAIT until the final descendant signal.
    with getattr(process, "_waitpid_lock", nullcontext()):
        if process.returncode is not None:
            return
        try:
            exited = os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
        except ChildProcessError:
            return  # externally reaped: no authority to signal a bare PGID
        if exited is None:
            try:
                _signal_linux_group(process, TERM)
            except ProcessLookupError:
                pass
            deadline = time.monotonic() + grace
            while time.monotonic() < deadline:
                try:
                    exited = os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
                except ChildProcessError:
                    return
                if exited is not None:
                    break
                time.sleep(min(0.05, max(0, deadline - time.monotonic())))
        try:
            _signal_linux_group(process, KILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=max(2.0, grace))


def _signal_linux_group(process, signum):
    """Caller holds Popen's wait lock until killpg has consumed the PGID."""
    if process.returncode is not None:
        raise ProcessLookupError("process-group custody lost: child was reaped")
    try:
        os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
    except ChildProcessError as exc:
        raise ProcessLookupError("process-group custody lost: child is no longer waitable") from exc
    os.killpg(process.pid, signum)


def signal_process(expected, signum):
    """Signal one incarnation via pidfd / retained Windows handle, never a bare PID."""
    if not expected:
        raise ProcessLookupError("missing process identity")
    pid = int(expected["pid"])
    if sys.platform == "darwin":
        # Import lazily: custody_broker itself imports this platform module.
        from astrid_runtime.custody_broker import (
            audit_token_details,
            current_process_audit_token,
            signal_audit_token,
        )
        before = process_identity(pid)
        if before is None or any(before.get(key) != expected.get(key) for key in ("pid", "uid", "birth_id")):
            raise OSError("process incarnation changed")
        token = current_process_audit_token(pid)
        details = audit_token_details(token["words"])
        if details.get("pid") != pid or details.get("uid") != expected.get("uid"):
            raise OSError("audit token does not match expected process identity")
        after = process_identity(pid)
        if after is None or any(after.get(key) != expected.get(key) for key in ("pid", "uid", "birth_id")):
            raise OSError("process incarnation changed while binding its audit token")
        signal_audit_token(token["words"], signum)
        return
    if sys.platform == "win32":
        from ctypes import wintypes
        kernel = _kernel(); handle = kernel.OpenProcess(0x1000 | 1 | 0x100000, False, pid)
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            observed = _windows_identity(pid, handle)
            if any(observed.get(k) != expected.get(k) for k in ("pid", "uid", "birth_id")):
                raise OSError("process incarnation changed")
            # CTRL_BREAK is cooperative and addressed to the isolated group;
            # force termination always uses the identity-checked kernel handle.
            if signum != KILL:
                try:
                    os.kill(pid, signal.CTRL_BREAK_EVENT)
                    return
                except OSError:
                    # Services and console-less processes have no console
                    # control channel. In that case fail closed to the
                    # identity-checked process handle below.
                    pass
            kernel.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
            if not kernel.TerminateProcess(handle, 1):
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            kernel.CloseHandle(handle)
        return
    if not hasattr(os, "pidfd_open") or not hasattr(signal, "pidfd_send_signal"):
        raise NotImplementedError("identity-safe process signaling requires Linux pidfd support")
    fd = os.pidfd_open(pid)
    try:
        observed = process_identity(pid)
        if observed is None or any(observed.get(k) != expected.get(k) for k in ("pid", "uid", "birth_id")):
            raise OSError("process incarnation changed")
        signal.pidfd_send_signal(fd, signum)
    finally:
        os.close(fd)


def install_stop_handlers(callback):
    """Install native console/service-manager stop handlers; return a restore callable."""
    signals = [signal.SIGINT, signal.SIGTERM]
    if hasattr(signal, "SIGBREAK"):
        signals.append(signal.SIGBREAK)
    previous = {value: signal.signal(value, callback) for value in signals}
    def restore():
        for value, handler in previous.items():
            signal.signal(value, handler)
    return restore


def _adopt_inherited_job():
    # A detached owner keeps this handle until process exit. Clear inheritance
    # before it can launch children, so its death closes the final Job handle.
    if sys.platform == "win32":
        value = os.environ.pop("ASTRID_RUNTIME_JOB_HANDLE", None)
        if value:
            handle = int(value)
            os.set_handle_inheritable(handle, False)
            return handle
    return None


_inherited_job_handle = _adopt_inherited_job()
