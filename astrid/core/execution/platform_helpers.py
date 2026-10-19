"""Agent policy composed from Runtime's native platform primitives.

Candidates to upstream: ownership checks accepting both an open handle and
existing metadata, and recovery of an observed, birth-anchored POSIX group.
"""
from __future__ import annotations

import os
import stat
import sys

from runtime_protocol import platform


def owned_by_current_user(path_or_fd, metadata, *, mode: int | None = None,
                          forbidden: int = 0) -> bool:
    # Windows stat.st_uid has no SID. Keep ownership-only checks distinct
    # from private-state DACL checks, as on POSIX (media may be shared).
    if sys.platform == "win32":
        if path_or_fd is None:
            return False
        if mode is not None or forbidden:
            return platform.is_owner_only(path_or_fd)
        from runtime_protocol import windows_security
        try:
            with windows_security._handle(path_or_fd) as (handle, _info):
                windows_security._validate_handle(handle, owner_only=True)
            return True
        except OSError:
            return False
    return (platform.is_current_user(metadata)
            and (mode is None or stat.S_IMODE(metadata.st_mode) == mode)
            and not metadata.st_mode & forbidden)


def signal_observed_group(pgid: int, signum: int, *, leader_birth: str | None) -> None:
    """Recover a journalled group without granting signal authority to a PGID.

    Each member is revalidated by Runtime while binding its kernel signal
    handle. A reused leader invalidates the entire observation.
    """
    from .process_group import _process_snapshot

    if pgid <= 1 or pgid == platform.process_group(os.getpid()) or not leader_birth:
        raise ValueError("process group lacks a safe birth anchor")
    census = _process_snapshot()
    if not census:
        raise OSError("process census unavailable")
    leader = census.get(pgid)
    if leader is not None and leader.birth != leader_birth:
        raise ProcessLookupError("process group leader was replaced")
    expected = []
    for pid, info in census.items():
        if info.pgid != pgid:
            continue
        identity = platform.process_identity(pid)
        if identity is None:
            continue
        # Compare against a second agent census; its persisted birth format is
        # intentionally different from Runtime's Linux identity format.
        current = _process_snapshot().get(pid)
        if current is None or current.birth != info.birth or current.pgid != pgid:
            raise ProcessLookupError("process group member changed")
        expected.append(identity)
    for identity in reversed(expected):
        try:
            platform.signal_process(identity, signum)
        except ProcessLookupError:
            pass
