#!/usr/bin/env python3
"""Append the body-owned terminal free-space sample after sampler reaping."""

from __future__ import annotations

import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def available_bytes(probe: str) -> int:
    result = subprocess.run(["df", "-B1", "--output=avail", probe], check=True, capture_output=True, text=True)
    rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 2 or rows[0] != "Avail" or not rows[1].isdigit():
        raise RuntimeError(f"unexpected df output: {result.stdout!r}")
    return int(rows[1])


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        return 2
    trace, job_id, body_pid, probe = Path(argv[0]), argv[1], int(argv[2]), argv[3]
    now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    with trace.open("a", encoding="utf-8") as stream:
        stream.write(f"{now}\t{time.monotonic_ns()}\t{available_bytes(probe)}\t{job_id}\t{body_pid}\tfinal\n")
        stream.flush()
        os.fsync(stream.fileno())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"final trace sample failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
