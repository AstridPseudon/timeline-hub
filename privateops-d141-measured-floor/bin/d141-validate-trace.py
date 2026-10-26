#!/usr/bin/env python3
"""Fail closed on missing, stale, malformed, or non-continuous body traces."""

from __future__ import annotations

import os
import stat
import sys
from datetime import datetime
from itertools import pairwise
from pathlib import Path


class TraceError(ValueError):
    pass


def fail(message: str) -> None:
    raise TraceError(message)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: validate-trace.py TRACE JOB_ID BODY_PID EXPECTED_OWNER_UID", file=sys.stderr)
        return 2
    path = Path(argv[0])
    job_id = argv[1]
    body_pid = int(argv[2])
    owner_uid = int(argv[3])
    item = os.lstat(path)
    if stat.S_ISLNK(item.st_mode) or not stat.S_ISREG(item.st_mode):
        fail("trace is not a regular non-symlink file")
    if item.st_uid != owner_uid:
        fail("trace owner mismatch")
    rows = path.read_text(encoding="utf-8").splitlines()
    expected = "timestamp_utc\tmonotonic_ns\tavailable_bytes\tjob_id\tbody_pid\tkind"
    if not rows or rows[0] != expected:
        fail("trace header mismatch")
    samples: list[tuple[datetime, int, int, str]] = []
    for raw in rows[1:]:
        fields = raw.split("\t")
        if len(fields) != 6:
            fail("trace row has wrong field count")
        stamp = datetime.fromisoformat(fields[0].replace("Z", "+00:00"))
        monotonic_ns = int(fields[1])
        available = int(fields[2])
        recorded_pid = int(fields[4])
        if monotonic_ns < 0 or available < 0 or fields[3] != job_id or recorded_pid != body_pid:
            fail("trace sample identity or value mismatch")
        if fields[5] not in {"first", "periodic", "final"}:
            fail("trace sample kind is invalid")
        samples.append((stamp, monotonic_ns, available, fields[5]))
    if len(samples) < 2:
        fail("trace needs first and final samples")
    if samples[0][3] != "first" or samples[-1][3] != "final":
        fail("trace does not have first/final samples")
    if any(left[1] >= right[1] or left[0] >= right[0] for left, right in pairwise(samples)):
        fail("trace timestamps are not strictly increasing")
    periodic = [sample for sample in samples if sample[3] == "periodic"]
    for left, right in pairwise(periodic):
        seconds = (right[1] - left[1]) / 1_000_000_000
        if not 4.0 <= seconds <= 7.0:
            fail(f"trace periodic interval is {seconds:.3f}s, outside 4-7s")
    print(f"trace PASS: {len(samples)} actual samples; first={samples[0][0].isoformat()} last={samples[-1][0].isoformat()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, ValueError, TraceError) as exc:
        print(f"trace rejected: {exc}", file=sys.stderr)
        raise SystemExit(1)
