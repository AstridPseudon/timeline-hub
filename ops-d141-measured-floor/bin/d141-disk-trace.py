#!/usr/bin/env python3
"""Record real free-space observations for one dispatched heavy body."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
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
    trace_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if trace_path.is_symlink():
        raise RuntimeError("trace path is symlinked")
    with trace_path.open("x", encoding="utf-8") as stream:
        stream.write("timestamp_utc\tmonotonic_ns\tavailable_bytes\tjob_id\tbody_pid\tkind\n")
        stream.flush()
        os.fsync(stream.fileno())
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
            stream.write(f"{timestamp()}\t{time.monotonic_ns()}\t{value}\t{job_id}\t{body_pid}\t{kind}\n")
            stream.flush()
            os.fsync(stream.fileno())
            if value <= STOP_BYTES and not stopping:
                # The sampler is outside the body. Ask the runner to stop its
                # active command and finalize the whole admission unit after
                # this below-stop observation is durable.
                Path(f"{trace_path}.stop").write_text("4gb-stop\n", encoding="utf-8")
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


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"disk trace failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
