"""Delivery tracing and stop propagation inside the existing dispatcher lease."""

from __future__ import annotations

import ctypes
import errno
import fcntl
import hashlib
import json
import os
import select
import signal
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

EXTERNAL_DISPATCH_FLOOR_BYTES = 4_860_000_000
STOP_FLOOR_BYTES = 4_000_000_000
DEFAULT_TIMEOUT_SECONDS = 30 * 60
SAMPLER_READY_SECONDS = 10.0
SAMPLER_STALE_SECONDS = 15.0
# The enclosing test-run lease supervisor escalates after five seconds. Reap the
# private D68 groups before that supervisor can kill this caller's suite group.
STOP_GRACE_SECONDS = 1.0
TRACE_SCRIPT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
    "/scratchpad/orch/bin/d141-disk-trace.py"
)
TRACE_APPEND_FINAL = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
    "/scratchpad/orch/bin/d141-append-final.py"
)


class LifecycleError(RuntimeError):
    """A sampler or lifecycle invariant failed closed."""


def _proc_rows() -> dict[int, tuple[int, int, str]]:
    rows: dict[int, tuple[int, int, str]] = {}
    for item in Path("/proc").iterdir():
        if not item.name.isdigit():
            continue
        try:
            raw = (item / "stat").read_text()
            _, tail = raw.rsplit(")", 1)
            fields = tail.split()
            rows[int(item.name)] = (int(fields[1]), int(fields[2]), fields[0])
        except (OSError, ValueError, IndexError):
            continue
    return rows


def _descendants(known: set[int], rows: dict[int, tuple[int, int, str]]) -> set[int]:
    result = {pid for pid in known if pid in rows}
    changed = True
    while changed:
        changed = False
        for pid, (ppid, _pgid, _state) in rows.items():
            if ppid in result and pid not in result:
                result.add(pid)
                changed = True
    return result


def _prctl(option: int, argument: int) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(option, argument, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), f"prctl({option}) failed")


def _reap(reaped: list[int], *processes: subprocess.Popen[str]) -> None:
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            return
        if pid <= 0:
            return
        reaped.append(pid)
        for process in processes:
            if pid == process.pid:
                process.returncode = os.waitstatus_to_exitcode(status)


def _control_descriptor(env: dict[str, str]) -> int | None:
    raw = env.pop("BENCH_CONTROL_FD", None)
    if raw is None:
        return None
    descriptor = int(raw)
    if descriptor < 0:
        raise LifecycleError("invalid BENCH_CONTROL_FD")
    try:
        item = os.fstat(descriptor)
    except OSError as exc:
        # test-run publishes the suite group and closes its writer before exec.
        # Its environment still names that now-closed descriptor.
        if exc.errno == errno.EBADF:
            return None
        raise
    if not stat.S_ISFIFO(item.st_mode) or fcntl.fcntl(descriptor, fcntl.F_GETFL) & os.O_ACCMODE == os.O_RDONLY:
        raise LifecycleError("BENCH_CONTROL_FD is not a writable pipe")
    return descriptor


def _signal_groups(groups: set[int], signum: signal.Signals) -> None:
    for pgid in sorted(groups):
        if pgid <= 1:
            continue
        try:
            os.killpg(pgid, signum)
        except ProcessLookupError:
            pass


def _parse_binding(raw: str) -> tuple[int, int, int, int, int, str]:
    fields = raw.split("\t")
    if len(fields) != 7 or fields[0] != "ready":
        raise LifecycleError("disk sampler binding is malformed")
    try:
        values = [int(value, 8 if index == 3 else 10) for index, value in enumerate(fields[1:6])]
    except ValueError as exc:
        raise LifecycleError("disk sampler binding has non-numeric identity") from exc
    device, inode, owner, mode, links = values
    parent_hash = fields[6]
    if device < 0 or inode < 0 or owner < 0 or mode != 0o600 or links != 1:
        raise LifecycleError("disk sampler binding has invalid identity")
    if len(parent_hash) != 64 or any(char not in "0123456789abcdef" for char in parent_hash):
        raise LifecycleError("disk sampler binding has invalid parent identity")
    return device, inode, owner, mode, links, parent_hash


def _open_parent(path: Path, owner_uid: int) -> tuple[int, str]:
    if not path.is_absolute() or path.name != "disk-trace.tsv":
        raise LifecycleError("trace path is not the fixed absolute file")
    if any(component in {".", ".."} for component in path.parts[1:]):
        raise LifecycleError("trace path contains traversal components")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path.anchor, flags)
    records: list[str] = []
    try:
        for component in path.parts[1:-1]:
            child = os.open(component, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
            item = os.fstat(descriptor)
            mode = stat.S_IMODE(item.st_mode)
            if not stat.S_ISDIR(item.st_mode) or item.st_uid not in {0, owner_uid}:
                raise LifecycleError("trace parent is not an owned directory")
            if mode & (stat.S_IWGRP | stat.S_IWOTH) and not (
                item.st_uid == 0 and mode & stat.S_ISVTX
            ):
                raise LifecycleError("trace parent is writable by an untrusted class")
            records.append(f"{component}:{item.st_dev}:{item.st_ino}:{item.st_uid}:{mode:o}")
        return descriptor, hashlib.sha256("|".join(records).encode()).hexdigest()
    except BaseException:
        os.close(descriptor)
        raise


def _open_bound_trace(trace: Path, binding_text: str) -> tuple[int, tuple[int, int, int, int, int, str]]:
    binding = _parse_binding(binding_text)
    parent, parent_hash = _open_parent(trace, os.getuid())
    descriptor = -1
    success = False
    try:
        if parent_hash != binding[5]:
            raise LifecycleError("trace parent identity changed before monitoring")
        flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(trace.name, flags, dir_fd=parent)
        item = os.fstat(descriptor)
        identity = (item.st_dev, item.st_ino, item.st_uid, stat.S_IMODE(item.st_mode), item.st_nlink)
        if not stat.S_ISREG(item.st_mode) or identity != binding[:5] or item.st_uid != os.getuid():
            raise LifecycleError("trace identity, ownership, mode, or link count changed")
        success = True
        return descriptor, binding
    finally:
        os.close(parent)
        if descriptor >= 0 and not success:
            os.close(descriptor)


def _read_bound_trace(descriptor: int, binding: tuple[int, int, int, int, int, str]) -> str:
    item = os.fstat(descriptor)
    identity = (item.st_dev, item.st_ino, item.st_uid, stat.S_IMODE(item.st_mode), item.st_nlink)
    if not stat.S_ISREG(item.st_mode) or identity != binding[:5] or item.st_uid != os.getuid():
        raise LifecycleError("trace identity, ownership, mode, or link count changed")
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    size = 0
    while True:
        chunk = os.read(descriptor, 65536)
        if not chunk:
            break
        chunks.append(chunk)
        size += len(chunk)
        if size > 16 * 1024 * 1024:
            raise LifecycleError("trace is too large")
    return b"".join(chunks).decode("utf-8")


def _latest_sample(
    trace_fd: int, binding: tuple[int, int, int, int, int, str]
) -> tuple[int, float] | None:
    try:
        raw = _read_bound_trace(trace_fd, binding)
    except (OSError, UnicodeDecodeError):
        return None
    rows = raw.splitlines()
    if len(rows) < 2:
        return None
    fields = rows[-1].split("\t")
    if len(fields) != 6:
        raise LifecycleError("disk trace row is malformed")
    try:
        value = int(fields[2])
    except ValueError as exc:
        raise LifecycleError("disk trace availability is invalid") from exc
    if value < 0 or fields[5] not in {"first", "periodic", "final"}:
        raise LifecycleError("disk trace sample is invalid")
    return value, os.fstat(trace_fd).st_mtime


def _validate_trace(trace: Path, job_id: str, body_pid: int, probe: str, binding: str) -> None:
    if not TRACE_APPEND_FINAL.is_file() or TRACE_APPEND_FINAL.is_symlink():
        raise LifecycleError("disk trace append-final helper is unavailable")
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            str(TRACE_APPEND_FINAL),
            str(trace),
            job_id,
            str(body_pid),
            probe,
            binding,
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        raise LifecycleError(f"disk trace rejected: {result.stderr.strip()}")


def _write_lifecycle(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _stop_sampler(sampler: subprocess.Popen[str], deadline: float) -> int:
    if sampler.poll() is None:
        try:
            sampler.send_signal(signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            sampler.wait(timeout=max(0.0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            sampler.kill()
            sampler.wait()
    return int(sampler.returncode if sampler.returncode is not None else 125)


def _read_ready(sampler: subprocess.Popen[str]) -> str:
    if sampler.stdout is None:
        raise LifecycleError("disk sampler has no readiness channel")
    ready, _, _ = select.select([sampler.stdout], [], [], SAMPLER_READY_SECONDS)
    if not ready:
        raise LifecycleError("disk sampler readiness timed out")
    line = sampler.stdout.readline().strip()
    if not line.startswith("ready\t"):
        raise LifecycleError("disk sampler readiness is invalid")
    return line


def run_delivery(
    command: list[str],
    service_tmp: Path,
    *,
    env: dict[str, str] | None = None,
    probe: str = "/home/user",
    cancel_path: Path | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> tuple[int, str, dict[str, Any]]:
    """Run the existing D68 caller under the final-build lifecycle contract."""

    service_tmp = service_tmp.absolute()
    keep_dir = service_tmp / "timeline-delivery-KEEP"
    keep_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    keep_marker = keep_dir / "KEEP"
    keep_marker.write_text("retain delivery lifecycle evidence\n")
    lifecycle_path = keep_dir / "lifecycle.json"
    trace = keep_dir / "disk-trace.tsv"
    job_id = "delivery-build"
    record: dict[str, Any] = {
        "status": "not_started", "job_id": job_id,
        "keep": str(keep_marker), "trace": str(trace),
        "external_dispatch_floor_bytes": EXTERNAL_DISPATCH_FLOOR_BYTES,
        "admission_owner": "normal dispatcher test-run; no private lifecycle admission",
        "stop_floor_bytes": STOP_FLOOR_BYTES,
        "reaped_pids": [], "process_groups": [],
    }
    signal_reason: dict[str, str] = {}
    previous_signals: dict[signal.Signals, Any] = {}
    trace_fd = -1
    parent_pid = os.getppid()
    death_signal = ctypes.c_int()
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(2, ctypes.byref(death_signal), 0, 0, 0) != 0:  # PR_GET_PDEATHSIG
        raise OSError(ctypes.get_errno(), "cannot read parent-death signal")
    child_env = dict(os.environ if env is None else env)
    sampler: subprocess.Popen[str] | None = None
    process: subprocess.Popen[str] | None = None
    groups: set[int] = set()
    reaped: list[int] = []

    def request_stop(signum: int, _frame: Any) -> None:
        signal_reason["reason"] = "sigterm" if signum == signal.SIGTERM else "sigint"

    previous_signals = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT)}
    for sig in previous_signals:
        signal.signal(sig, request_stop)
    try:
        try:
            _prctl(36, 1)
            _prctl(1, signal.SIGTERM)  # PR_SET_PDEATHSIG; recheck the installation race.
            control_fd = _control_descriptor(child_env)
            record.update(parent_pid=parent_pid, control_pipe=control_fd is not None)
            if os.getppid() != parent_pid or signal_reason or (cancel_path is not None and cancel_path.exists()):
                record.update(status="stopped", stop_reason="cancelled_before_start", exit=130)
                _write_lifecycle(lifecycle_path, record)
                return 130, "", record
            if trace.exists() or trace.is_symlink():
                raise LifecycleError(f"delivery trace already exists: {trace}")
            body_pid = os.getpid()
            start_ticks = Path(f"/proc/{body_pid}/stat").read_text().split()[21]
            sampler = subprocess.Popen(
                [sys.executable, "-I", str(TRACE_SCRIPT), str(trace), job_id, str(body_pid), probe, start_ticks],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True,
            )
            try:
                binding = _read_ready(sampler)
            except (OSError, LifecycleError, ValueError) as exc:
                _stop_sampler(sampler, time.monotonic() + 2)
                record.update(status="unknown", reason="sampler_not_ready", detail=str(exc), exit=125)
                _write_lifecycle(lifecycle_path, record)
                return 125, f"delivery lifecycle refused: {exc}\n", record
            record["sampler_binding"] = binding
            try:
                trace_fd, parsed_binding = _open_bound_trace(trace, binding)
            except (OSError, LifecycleError, ValueError) as exc:
                _stop_sampler(sampler, time.monotonic() + 2)
                record.update(status="unknown", reason="trace_binding_invalid", detail=str(exc), exit=125)
                _write_lifecycle(lifecycle_path, record)
                return 125, f"delivery lifecycle refused: {exc}\n", record
            if sampler.stdout is not None:
                sampler.stdout.close()
            if sampler.stderr is not None:
                sampler.stderr.close()

            deadline = time.monotonic() + SAMPLER_READY_SECONDS
            first = _latest_sample(trace_fd, parsed_binding)
            while first is None and time.monotonic() < deadline and sampler.poll() is None:
                time.sleep(0.02)
                first = _latest_sample(trace_fd, parsed_binding)
            if first is None:
                raise LifecycleError("sampler has no initial sample")
            before_reason = None
            before_code = 130
            if first[0] <= STOP_FLOOR_BYTES:
                before_reason, before_code = "low_disk_before", 75
            elif time.time() - first[1] > SAMPLER_STALE_SECONDS:
                before_reason, before_code = "sampler_stale_before", 125
            elif os.getppid() != parent_pid or signal_reason or (cancel_path is not None and cancel_path.exists()):
                before_reason = "cancelled_before_start"
            if before_reason is not None:
                _stop_sampler(sampler, time.monotonic() + 2)
                _validate_trace(trace, job_id, body_pid, probe, binding)
                record.update(status="stopped", stop_reason=before_reason, trace_status="PASS", exit=before_code)
                _write_lifecycle(lifecycle_path, record)
                return before_code, "", record

            process = subprocess.Popen(
                command, env=child_env, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True,
            )
            supervisor_pid = os.getpid()
            known = {supervisor_pid, process.pid}
            groups = {process.pid}
            stop_reason: str | None = None
            stop_code = 0
            if control_fd is not None:
                try:
                    os.write(control_fd, f"{process.pid}\n".encode())
                except BrokenPipeError:
                    stop_reason, stop_code = "control_pipe_closed", 130
            sent_at: float | None = None
            missing_started: float | None = None
            started = time.monotonic()
            while True:
                rows = _proc_rows()
                descendants = _descendants(known, rows)
                descendants.update(
                    pid for pid, (ppid, _pgid, _state) in rows.items()
                    if ppid == supervisor_pid and pid != sampler.pid
                )
                known.update(descendants)
                for pid in descendants:
                    row = rows.get(pid)
                    if row is not None and pid != supervisor_pid:
                        groups.add(row[1])
                _reap(reaped, process, sampler)
                now = time.monotonic()
                try:
                    latest = _latest_sample(trace_fd, parsed_binding)
                except (OSError, LifecycleError):
                    latest = None
                    stop_reason = stop_reason or "sampler_invalid"
                    stop_code = 125
                if latest is None:
                    missing_started = missing_started or now
                    if now - missing_started > SAMPLER_READY_SECONDS:
                        stop_reason = stop_reason or "sampler_missing"
                        stop_code = 125
                else:
                    missing_started = None
                    if latest[0] <= STOP_FLOOR_BYTES:
                        stop_reason = stop_reason or "low_disk"
                        stop_code = 75
                    elif time.time() - latest[1] > SAMPLER_STALE_SECONDS:
                        stop_reason = stop_reason or "sampler_frozen"
                        stop_code = 125
                if sampler.poll() not in (None, 0) and stop_reason is None:
                    stop_reason, stop_code = "sampler_failed", 125
                if os.getppid() != parent_pid and stop_reason is None:
                    stop_reason, stop_code = "parent_died", 130
                if cancel_path is not None and cancel_path.exists() and stop_reason is None:
                    stop_reason, stop_code = "cancelled", 130
                if signal_reason and stop_reason is None:
                    stop_reason = signal_reason["reason"]
                    stop_code = 143 if stop_reason == "sigterm" else 130
                if now - started >= timeout_seconds and stop_reason is None:
                    stop_reason, stop_code = "timeout", 124
                if stop_reason is not None and sent_at is None:
                    sent_at = now
                if sent_at is not None:
                    # Include groups discovered after the first stop request.
                    _signal_groups(groups, signal.SIGTERM)
                if sent_at is not None and now - sent_at >= STOP_GRACE_SECONDS:
                    _signal_groups(groups, signal.SIGKILL)
                process_done = process.poll() is not None
                current_rows = _proc_rows()
                live_descendants = _descendants(known, current_rows)
                live_descendants.update(
                    pid for pid, (ppid, _pgid, _state) in current_rows.items()
                    if ppid == supervisor_pid and pid != sampler.pid
                )
                live_descendants -= {process.pid, supervisor_pid, sampler.pid}
                if process_done and not live_descendants:
                    break
                time.sleep(0.02)
            output, _ = process.communicate()
            process_code = int(process.returncode if process.returncode is not None else 125)
            sampler_code = _stop_sampler(sampler, time.monotonic() + 8)
            if sampler_code != 0 and stop_reason is None:
                stop_reason, stop_code = "sampler_failed", 125
            _reap(reaped, process, sampler)
            record.update(
                process_groups=sorted(groups), reaped_pids=sorted(set(reaped)),
                process_exit=process_code, sampler_exit=sampler_code,
                stop_reason=stop_reason, terminal="stopped" if stop_reason else "normal",
            )
            try:
                _validate_trace(trace, job_id, body_pid, probe, binding)
                record["trace_status"] = "PASS"
            except (OSError, subprocess.SubprocessError, LifecycleError, ValueError) as exc:
                record.update(trace_status="FAIL", trace_error=str(exc))
                if stop_reason is None:
                    stop_reason, stop_code = "trace_invalid", 125
            final_sample = _latest_sample(trace_fd, parsed_binding)
            if stop_reason is None and final_sample is not None and final_sample[0] <= STOP_FLOOR_BYTES:
                stop_reason, stop_code = "low_disk_after", 75
            if stop_reason is not None:
                record.update(status="stopped", exit=stop_code, stop_reason=stop_reason)
                _write_lifecycle(lifecycle_path, record)
                return stop_code, output, record
            record.update(status="complete" if process_code == 0 else "failed", exit=process_code)
            _write_lifecycle(lifecycle_path, record)
            return process_code, output, record
        except (OSError, LifecycleError, ValueError) as exc:
            if process is not None:
                # A monitoring/control error must not abandon a started builder.
                rows = _proc_rows()
                descendants = _descendants({os.getpid(), process.pid}, rows)
                stopped_pids = descendants - {os.getpid(), sampler.pid if sampler else -1}
                groups.update(rows[pid][1] for pid in stopped_pids)
                _signal_groups(groups, signal.SIGKILL)
                process.wait()
                deadline = time.monotonic() + 2
                while time.monotonic() < deadline:
                    _reap(reaped, process, *([sampler] if sampler else []))
                    if not _descendants(stopped_pids, _proc_rows()):
                        break
                    time.sleep(0.02)
                record.update(process_groups=sorted(groups), reaped_pids=sorted(set(reaped)))
            record.update(status="unknown", reason="lifecycle_error", detail=str(exc), exit=125)
            _write_lifecycle(lifecycle_path, record)
            return 125, f"delivery lifecycle failed closed: {exc}\n", record
        finally:
            if sampler is not None and sampler.poll() is None:
                _stop_sampler(sampler, time.monotonic() + 2)
            _prctl(1, death_signal.value)
            for sig, handler in previous_signals.items():
                signal.signal(sig, handler)
            if trace_fd >= 0:
                os.close(trace_fd)
                trace_fd = -1
    finally:
        pass
