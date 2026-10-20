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

import fcntl
import json
import os
import signal
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
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


# Crash-orphan journal: one owner-only file in the host's support root listing
# each live scope as {pid, start, pgid, task}.  An entry is removed when the
# scope settles; the next host start kills whatever a dead host left behind.
_journal: Path | None = None
_journal_lock = threading.Lock()


def set_orphan_journal(path: Path | str | None) -> None:
    global _journal
    _journal = Path(path) if path is not None else None


def _journal_edit(path: Path, edit) -> None:
    """Read-modify-write the journal under a lock; never raises."""
    try:
        with _journal_lock:
            fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, "r+") as stream:
                fcntl.flock(stream, fcntl.LOCK_EX)
                try:
                    entries = json.loads(stream.read() or "[]")
                    entries = entries if isinstance(entries, list) else []
                except ValueError:
                    entries = []
                entries = edit(entries)
                stream.seek(0)
                stream.truncate()
                stream.write(json.dumps(entries))
                os.fchmod(stream.fileno(), 0o600)
    except OSError:
        pass


def _birth(pid: int) -> str | None:
    from astrid.core.execution import process_group as pg
    try:
        info = pg._process_snapshot().get(pid)
    except Exception:
        return None
    return info.birth if info is not None else None


def reap_orphans(path: Path | str) -> list[str]:
    """Kill groups a crashed host left running, then clear the journal.

    A group is signalled only when its recorded leader still exists with the
    recorded start time, or the leader is gone and the group still has members
    (a live group keeps its pgid from being reused).  A pid now owned by an
    unrelated process is never signalled.  Returns notes for what was killed
    or could not be.
    """
    path = Path(path)
    try:
        entries = json.loads(path.read_text())
    except (OSError, ValueError):
        return []
    notes: list[str] = []
    from astrid.core.execution import process_group as pg
    for entry in entries if isinstance(entries, list) else []:
        try:
            pid, pgid, start = int(entry["pid"]), int(entry["pgid"]), entry.get("start")
            census = pg._process_snapshot()
            if not census:
                notes.append(f"orphan scope {pgid} unchecked: census unavailable")
                continue
            leader = census.get(pid)
            if leader is not None and leader.status != _DARWIN_ZOMBIE and leader.birth != start:
                continue  # the pid belongs to an unrelated process now
            members = [p for p, i in census.items() if i.pgid == pgid and i.status != _DARWIN_ZOMBIE]
            if not members:
                continue
            for sig, wait in ((signal.SIGTERM, 2.0), (signal.SIGKILL, 3.0)):
                _killpg(pgid, sig)
                deadline = time.monotonic() + wait
                while time.monotonic() < deadline:
                    members = [p for p, i in pg._process_snapshot().items()
                               if i.pgid == pgid and i.status != _DARWIN_ZOMBIE]
                    if not members:
                        break
                    time.sleep(0.05)
                if not members:
                    break
            notes.append(f"killed orphan task scope {pgid} ({entry.get('task')}) left by a crashed host"
                         if not members else
                         f"orphan task scope {pgid} ({entry.get('task')}) still running after KILL: {members}")
        except Exception as exc:
            notes.append(f"orphan scope entry {entry!r} unchecked: {exc}")
    try:
        path.write_text("[]")
    except OSError:
        pass
    return notes


def spawn(argv: Sequence[str], **popen_kwargs: Any) -> subprocess.Popen:
    """Start ``argv`` as the leader of a new session and group."""
    process = subprocess.Popen(list(argv), **{**popen_kwargs, "start_new_session": True})
    process._astrid_task_scope = True  # type: ignore[attr-defined]
    if _journal is not None:
        entry = {"pid": process.pid, "pgid": process.pid, "start": _birth(process.pid),
                 "task": str(popen_kwargs.get("cwd") or "")}
        _journal_edit(_journal, lambda entries: [*entries, entry])
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
    report = _stop(process, grace, kill_wait)
    if _journal is not None and report.status == "settled":
        _journal_edit(_journal, lambda entries: [e for e in entries if e.get("pgid") != report.pgid])
    return report


def _stop(process: subprocess.Popen, grace: float, kill_wait: float) -> ScopeReport:
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
