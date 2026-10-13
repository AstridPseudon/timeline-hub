"""Process-group ownership helpers for tests that launch real workers."""
from __future__ import annotations

import os
import signal
import subprocess
import time


class ProcessGroups:
    def __init__(self) -> None:
        self.groups: dict[int, list[subprocess.Popen]] = {}
        self.cleanups = []

    def add_cleanup(self, callback) -> None:
        self.cleanups.append(callback)

    def popen(self, *args, **kwargs) -> subprocess.Popen:
        process = subprocess.Popen(*args, **kwargs)
        if kwargs.get("start_new_session"):
            self.record(process)
        return process

    def record(self, process: subprocess.Popen) -> None:
        if process.poll() is not None:
            return
        try:
            pgid = os.getpgid(process.pid)
        except ProcessLookupError:
            return
        if pgid != os.getpgrp():
            self.groups.setdefault(pgid, []).append(process)

    def add_group(self, pgid: int) -> None:
        if pgid > 1 and pgid != os.getpgrp():
            self.groups.setdefault(pgid, [])

    def terminate_all(self, timeout: float = 3.0) -> None:
        for callback in reversed(self.cleanups):
            try:
                callback()
            except Exception:
                pass
        self.cleanups.clear()
        for pgid, members in reversed(tuple(self.groups.items())):
            try:
                os.killpg(pgid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                continue
            for process in members:
                try:
                    process.wait(timeout=timeout)
                except (subprocess.TimeoutExpired, ChildProcessError):
                    pass
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline and _group_alive(pgid):
                time.sleep(0.02)
            if _group_alive(pgid):
                try:
                    os.killpg(pgid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass


def _group_alive(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True
