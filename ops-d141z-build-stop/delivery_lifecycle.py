"""Bounded delivery-build admission, tracing, process-group stop, and reap."""

from __future__ import annotations

import ctypes
import fcntl
import json
import os
import select
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DISPATCH_FLOOR_BYTES = 4_860_000_000
STOP_FLOOR_BYTES = 4_000_000_000
DEFAULT_TIMEOUT_SECONDS = 30 * 60
SAMPLER_READY_SECONDS = 10.0
SAMPLER_STALE_SECONDS = 15.0
STOP_GRACE_SECONDS = 5.0
TRACE_SCRIPT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
    "/scratchpad/orch/bin/d141-disk-trace.py"
)
TRACE_VALIDATOR = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
    "/scratchpad/orch/bin/d141-validate-trace.py"
)
HEAVY_LOCK = Path("/tmp/timeline-final-delivery-heavy.lock")


class LifecycleError(RuntimeError):
    """A sampler or lifecycle invariant failed closed."""


def available_bytes(probe: str) -> int:
    result = subprocess.run(
        ["df", "-B1", "--output=avail", probe],
        check=True,
        capture_output=True,
        text=True,
        timeout=2,
    )
    rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 2 or rows[0] != "Avail" or not rows[1].isdigit():
        raise LifecycleError(f"invalid disk availability: {result.stdout!r}")
    return int(rows[1])


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


def _reap(reaped: list[int]) -> None:
    while True:
        try:
            pid, _status = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            return
        if pid <= 0:
            return
        reaped.append(pid)


def _signal_groups(groups: set[int], signum: signal.Signals) -> None:
    for pgid in sorted(groups):
        if pgid <= 1:
            continue
        try:
            os.killpg(pgid, signum)
        except ProcessLookupError:
            pass


def _latest_sample(trace: Path) -> tuple[int, float] | None:
    try:
        rows = trace.read_text().splitlines()
    except (OSError, UnicodeDecodeError):
        return None
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
    return value, trace.stat().st_mtime


def _validate_trace(trace: Path, job_id: str, body_pid: int) -> None:
    if not TRACE_VALIDATOR.is_file() or TRACE_VALIDATOR.is_symlink():
        raise LifecycleError("disk trace validator is unavailable")
    result = subprocess.run(
        [sys.executable, "-I", str(TRACE_VALIDATOR), str(trace), job_id, str(body_pid), str(os.getuid())],
        capture_output=True,
        text=True,
        timeout=10,
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
        "dispatch_floor_bytes": DISPATCH_FLOOR_BYTES,
        "stop_floor_bytes": STOP_FLOOR_BYTES,
        "reaped_pids": [], "process_groups": [],
    }
    signal_reason: dict[str, str] = {}
    previous_signals: dict[signal.Signals, Any] = {}

    def request_stop(signum: int, _frame: Any) -> None:
        signal_reason["reason"] = "sigterm" if signum == signal.SIGTERM else "sigint"

    previous_signals = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT)}
    for sig in previous_signals:
        signal.signal(sig, request_stop)
    lock_fd = os.open(HEAVY_LOCK, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            record.update(status="refused", reason="heavy_slot_busy", exit=75)
            _write_lifecycle(lifecycle_path, record)
            return 75, "delivery admission refused: heavy slot busy\n", record
        try:
            try:
                admitted = available_bytes(probe)
            except (OSError, subprocess.SubprocessError, LifecycleError) as exc:
                record.update(status="refused", reason="disk_unreadable", detail=str(exc), exit=75)
                _write_lifecycle(lifecycle_path, record)
                return 75, f"delivery admission refused: {exc}\n", record
            record["admitted_bytes"] = admitted
            if admitted < DISPATCH_FLOOR_BYTES:
                record.update(status="refused", reason="low_disk_at_dispatch", exit=75)
                _write_lifecycle(lifecycle_path, record)
                return 75, f"delivery admission refused: available={admitted} floor={DISPATCH_FLOOR_BYTES}\n", record

            _prctl(36, 1)
            if trace.exists() or trace.is_symlink():
                raise LifecycleError("delivery trace already exists")
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
            if sampler.stdout is not None:
                sampler.stdout.close()
            if sampler.stderr is not None:
                sampler.stderr.close()

            process = subprocess.Popen(
                command, env=env or os.environ.copy(), text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True,
            )
            supervisor_pid = os.getpid()
            known = {supervisor_pid, process.pid}
            groups = {process.pid}
            reaped: list[int] = []
            stop_reason: str | None = None
            stop_code = 0
            sent_at: float | None = None
            missing_started: float | None = None
            started = time.monotonic()
            try:
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
                    _reap(reaped)
                    now = time.monotonic()
                    try:
                        latest = _latest_sample(trace)
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
                    if sampler.poll() is not None and stop_reason is None:
                        stop_reason, stop_code = "sampler_failed", 125
                    if cancel_path is not None and cancel_path.exists() and stop_reason is None:
                        stop_reason, stop_code = "cancelled", 130
                    if signal_reason and stop_reason is None:
                        stop_reason = signal_reason["reason"]
                        stop_code = 143 if stop_reason == "sigterm" else 130
                    if now - started >= timeout_seconds and stop_reason is None:
                        stop_reason, stop_code = "timeout", 124
                    if stop_reason is not None and sent_at is None:
                        sent_at = now
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
            finally:
                for sig, handler in previous_signals.items():
                    signal.signal(sig, handler)
            output, _ = process.communicate()
            process_code = int(process.returncode if process.returncode is not None else 125)
            sampler_code = _stop_sampler(sampler, time.monotonic() + 8)
            _reap(reaped)
            record.update(
                process_groups=sorted(groups), reaped_pids=sorted(set(reaped)),
                process_exit=process_code, sampler_exit=sampler_code,
                stop_reason=stop_reason, terminal="stopped" if stop_reason else "normal",
            )
            try:
                _validate_trace(trace, job_id, body_pid)
                record["trace_status"] = "PASS"
            except (OSError, subprocess.SubprocessError, LifecycleError, ValueError) as exc:
                record.update(trace_status="FAIL", trace_error=str(exc))
                if stop_reason is None:
                    stop_reason, stop_code = "trace_invalid", 125
            final_sample = _latest_sample(trace)
            if stop_reason is None and final_sample is not None and final_sample[0] <= STOP_FLOOR_BYTES:
                stop_reason, stop_code = "low_disk_after", 75
            if stop_reason is not None:
                record.update(status="stopped", exit=stop_code)
                _write_lifecycle(lifecycle_path, record)
                return stop_code, output, record
            record.update(status="complete" if process_code == 0 else "failed", exit=process_code)
            _write_lifecycle(lifecycle_path, record)
            return process_code, output, record
        except (OSError, LifecycleError, ValueError) as exc:
            record.update(status="unknown", reason="lifecycle_error", detail=str(exc), exit=125)
            _write_lifecycle(lifecycle_path, record)
            return 125, f"delivery lifecycle failed closed: {exc}\n", record
        finally:
            for sig, handler in previous_signals.items():
                signal.signal(sig, handler)
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            except OSError:
                pass
    finally:
        os.close(lock_fd)
