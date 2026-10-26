#!/usr/bin/env python3
"""Record real free-space observations for one dispatched heavy body."""

from __future__ import annotations

import os
import signal
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

INTERVAL_SECONDS = 5.0
STOP_BYTES = 4_000_000_000


def proc_start_ticks(pid: int) -> str:
    fields = Path(f"/proc/{pid}/stat").read_text().split()
    return fields[21]


def available_bytes(probe: str) -> int:
    result = subprocess.run(
        ["df", "-B1", "--output=avail", probe],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 2 or rows[0] != "Avail" or not rows[1].isdigit():
        raise RuntimeError(f"unexpected df output: {result.stdout!r}")
    return int(rows[1])


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parent_binding(path: Path, owner_uid: int) -> tuple[int, str]:
    """Open every physical parent without following links and bind its identity."""
    if not path.is_absolute() or path.name != "disk-trace.tsv":
        raise RuntimeError("trace path is not the fixed absolute file")
    if any(component in {".", ".."} for component in path.parts[1:]):
        raise RuntimeError("trace path contains traversal components")
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
                raise RuntimeError("trace parent is not an owned directory")
            if mode & (stat.S_IWGRP | stat.S_IWOTH) and not (item.st_uid == 0 and mode & stat.S_ISVTX):
                raise RuntimeError("trace parent is writable by an untrusted class")
            records.append(f"{component}:{item.st_dev}:{item.st_ino}:{item.st_uid}:{mode:o}")
        return descriptor, sha256("|".join(records).encode()).hexdigest()
    except BaseException:
        os.close(descriptor)
        raise


def write_all(descriptor: int, raw: bytes) -> None:
    while raw:
        written = os.write(descriptor, raw)
        if written <= 0:
            raise OSError("trace write made no progress")
        raw = raw[written:]


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print("usage: disk-trace.py TRACE JOB_ID BODY_PID PROBE PARENT_START_TICKS", file=sys.stderr)
        return 2
    trace_path = Path(argv[0])
    job_id = argv[1]
    body_pid = int(argv[2])
    probe = argv[3]
    parent_start_ticks = argv[4]
    stopping = False

    def stop(_signum: int, _frame: object) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    owner_uid = os.getuid()
    parent_descriptor, parent_hash = parent_binding(trace_path, owner_uid)
    trace_descriptor = -1
    try:
        create_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        trace_descriptor = os.open(trace_path.name, create_flags, 0o600, dir_fd=parent_descriptor)
        item = os.fstat(trace_descriptor)
        if not stat.S_ISREG(item.st_mode) or item.st_uid != owner_uid or stat.S_IMODE(item.st_mode) != 0o600 or item.st_nlink != 1:
            raise RuntimeError("sampler trace is not a single-link owned regular file")
        write_all(trace_descriptor, b"timestamp_utc\tmonotonic_ns\tavailable_bytes\tjob_id\tbody_pid\tkind\n")
        os.fsync(trace_descriptor)
        print(
            f"ready\t{item.st_dev}\t{item.st_ino}\t{item.st_uid}\t{stat.S_IMODE(item.st_mode):o}\t{item.st_nlink}\t{parent_hash}",
            flush=True,
        )
        next_sample = time.monotonic()
        first = True
        while True:
            try:
                parent_alive = os.getppid() == body_pid and proc_start_ticks(body_pid) == parent_start_ticks
            except OSError:
                parent_alive = False
            if not parent_alive:
                stopping = True
            kind = "first" if first else ("final" if stopping else "periodic")
            value = available_bytes(probe)
            write_all(trace_descriptor, f"{timestamp()}\t{time.monotonic_ns()}\t{value}\t{job_id}\t{body_pid}\t{kind}\n".encode())
            os.fsync(trace_descriptor)
            if value <= STOP_BYTES and not stopping:
                # Keep the paired admission's measured stop semantics: the
                # durable below-stop observation asks the body to stop.
                stop_path = trace_path.with_name(trace_path.name + ".stop")
                stop_descriptor = os.open(
                    stop_path.name,
                    os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                    0o600,
                    dir_fd=parent_descriptor,
                )
                try:
                    write_all(stop_descriptor, b"4gb-stop\n")
                    os.fsync(stop_descriptor)
                finally:
                    os.close(stop_descriptor)
                os.kill(body_pid, signal.SIGUSR1)
                stopping = True
            first = False
            if stopping:
                return 0
            next_sample += INTERVAL_SECONDS
            delay = max(0.0, next_sample - time.monotonic())
            try:
                time.sleep(delay)
            except InterruptedError:
                # The signal handler records the terminal request; loop once
                # so the required final sample is durable before exit.
                stopping = True
    finally:
        if trace_descriptor >= 0:
            os.close(trace_descriptor)
        os.close(parent_descriptor)


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"disk trace failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
