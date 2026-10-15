"""Task scopes: containment of an ordinary command by its process group.

The command leader starts a new session, so its process group is its own.
Nothing observes the tree while the command runs.  Cleanup signals the group
only (``killpg(TERM)``, grace, ``killpg(KILL)``) and then confirms with
censuses that nothing remains, reporting ``settled`` or ``unresolved`` with the
survivors named.  A census is evidence, never signal authority: a process found
only by census (e.g. one that left the group with ``setsid``) is reported, not
signalled.

Accepted limitation: on normal completion ``Popen.poll()`` has already reaped
the leader before the group kill, so there is a tiny window in which the pgid
could in principle be recycled.  When the leader is still alive (cancel,
timeout, shutdown) the group is signalled before it is reaped.
"""

from __future__ import annotations

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Sequence

_DARWIN_ZOMBIE = 5


class TaskScopeUnresolved(RuntimeError):
    """Processes remained after KILL; fails the task, never the host."""

    def __init__(self, report: "ScopeReport"):
        self.report = report
        super().__init__(report.describe())


@dataclass(frozen=True)
class Survivor:
    pid: int
    command: str


@dataclass(frozen=True)
class ScopeReport:
    status: str  # "settled" | "unresolved"
    pgid: int
    survivors: tuple[Survivor, ...] = ()
    detail: str = ""

    def describe(self) -> str:
        names = ", ".join(f"{s.pid} ({s.command})" for s in self.survivors)
        return (f"cleanup unresolved for process group {self.pgid}"
                + (f": still running after KILL: {names}" if names else "")
                + (f" [{self.detail}]" if self.detail else ""))


def spawn(argv: Sequence[str], **popen_kwargs: Any) -> subprocess.Popen:
    """Start ``argv`` as the leader of a new session and group."""
    process = subprocess.Popen(list(argv), **{**popen_kwargs, "start_new_session": True})
    process._astrid_task_scope = True  # type: ignore[attr-defined]
    return process


def _command_of(pid: int) -> str:
    try:
        out = subprocess.run(["ps", "-o", "command=", "-p", str(pid)], capture_output=True,
                             text=True, timeout=2, check=False).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return out[:200] or "unknown"


def _scope_census(pgid: int, leader: int) -> dict[int, str]:
    """``pid -> birth`` of live processes in the group or descending from it."""
    from astrid.core.execution import process_group as pg
    census = pg._process_snapshot()
    if not census:
        raise RuntimeError(pg._census_message("process census unavailable", census))
    live = {pid: info for pid, info in census.items()
            if pid != leader and info.status != _DARWIN_ZOMBIE}
    found = {pid for pid, info in live.items() if info.pgid == pgid}
    grew = True
    while grew:
        grew = False
        for pid, info in live.items():
            if pid not in found and info.ppid in (found | {leader}):
                found.add(pid)
                grew = True
    return {pid: live[pid].birth for pid in found}


def _alive(pgid: int, known: dict[int, str]) -> dict[int, str]:
    """Group members and descendants now, plus earlier-seen ones still alive."""
    now = _scope_census(pgid, pgid)
    from astrid.core.execution import process_group as pg
    census = pg._process_snapshot()
    kept = {pid: birth for pid, birth in known.items()
            if (info := census.get(pid)) is not None and info.birth == birth
            and info.status != _DARWIN_ZOMBIE}
    return {**kept, **now}


def _killpg(pgid: int, sig: int) -> str:
    try:
        os.killpg(pgid, sig)
    except ProcessLookupError:
        return ""
    except PermissionError as exc:  # a zombie-only group can answer EPERM on macOS
        return f"killpg({int(sig)}): {exc}"
    return ""


def stop(process: subprocess.Popen, grace: float = 2.0, kill_wait: float = 3.0) -> ScopeReport:
    """TERM the group, wait ``grace``, KILL it, reap the leader, confirm absence."""
    pgid = process.pid
    notes: list[str] = []
    try:
        members = _scope_census(pgid, pgid)  # evidence for naming survivors
    except Exception as exc:
        members, _ = {}, notes.append(f"pre-census failed: {exc}")
    # A group member is signalled only through the anchored group.
    notes.append(_killpg(pgid, signal.SIGTERM))
    escalated = False
    deadline = time.monotonic() + max(grace, 0.0)
    alive: dict[int, str] = dict(members)
    problem = ""
    while True:
        leader_gone = process.poll() is not None  # a live leader may still fork in a TERM handler
        try:
            alive, problem = _alive(pgid, members), ""
        except Exception as exc:
            problem = f"census failed: {exc}"
        if (leader_gone and not alive and not problem) or time.monotonic() >= deadline:
            if (alive or problem or not leader_gone) and not escalated:
                notes.append(_killpg(pgid, signal.SIGKILL))
                escalated = True
                deadline = time.monotonic() + kill_wait
            else:
                break
        time.sleep(0.02)
    # Reap the leader last (it may already have been reaped by poll()).
    try:
        process.wait(timeout=kill_wait)
    except subprocess.TimeoutExpired:
        try:
            os.kill(process.pid, signal.SIGKILL)  # we hold the unreaped leader
            process.wait(timeout=kill_wait)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            pass
    detail = "; ".join(n for n in (*notes, problem) if n)
    if alive or problem:
        return ScopeReport("unresolved", pgid,
                           tuple(Survivor(pid, _command_of(pid)) for pid in alive), detail)
    return ScopeReport("settled", pgid)
