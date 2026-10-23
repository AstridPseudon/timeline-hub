import ctypes
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def supervise(store, repo, suite, command, argv, cancelled, parent):
    # Subreaping keeps the lease until orphaned grandchildren finish as well.
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
        raise OSError(ctypes.get_errno(), "cannot enable child subreaper")
    stopping = False

    def stop(signum, frame):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        raise OSError(ctypes.get_errno(), "cannot watch runner death")
    if os.getppid() != parent:
        return 130

    with store.acquire_suite(repo, suite, command) as (entries, fds):
        if stopping:
            return 130
        read_fd, write_fd = os.pipe2(os.O_CLOEXEC | os.O_NONBLOCK)
        env = dict(os.environ, BENCH_CONTROL_FD=str(write_fd))
        child = subprocess.Popen(argv, env=env, pass_fds=tuple(fds) + (write_fd,), process_group=0)
        os.close(write_fd)
        groups = {child.pid}
        pending = b""
        result = None
        sent = None
        killed = False
        deadline = None
        timed_out = False
        try:
            while True:
                try:
                    pending += os.read(read_fd, 4096)
                except BlockingIOError:
                    pass
                while b"\n" in pending:
                    item, pending = pending.split(b"\n", 1)
                    pid = int(item)
                    if pid <= 1:
                        raise ValueError("bad suite process group")
                    groups.add(pid)
                    deadline = time.monotonic() + 90 * 60
                no_children = False
                while True:
                    try:
                        pid, status = os.waitpid(-1, os.WNOHANG)
                    except ChildProcessError:
                        no_children = True
                        break
                    if not pid:
                        break
                    if pid == child.pid:
                        result = os.waitstatus_to_exitcode(status)
                        child.returncode = result
                if no_children:
                    break
                now = time.monotonic()
                stopping = stopping or cancelled.exists() or os.getppid() != parent
                if deadline is not None and now >= deadline:
                    timed_out = True
                if (stopping or timed_out) and sent is None:
                    sent = now
                    for pgid in groups:
                        try:
                            os.killpg(pgid, signal.SIGTERM)
                        except ProcessLookupError:
                            pass
                if sent is not None and now - sent >= (5 if stopping else 60) and not killed:
                    killed = True
                    for pgid in groups:
                        try:
                            os.killpg(pgid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                time.sleep(0.02)
        finally:
            os.close(read_fd)
        if stopping:
            return 130
        if timed_out:
            return 124
        return result if result >= 0 else 128 - result


def main():
    orch, root, repo, suite, command, parent, cancelled, *argv = sys.argv[1:]
    spec = importlib.util.spec_from_file_location("bench_store", Path(orch) / "bin/bench_store.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    store = module.Store(root, Path(orch) / "tests")
    return supervise(store, repo, suite, command, argv, Path(cancelled), int(parent))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"BENCH-LEASE REFUSED: {exc}", file=sys.stderr)
        sys.exit(125)
