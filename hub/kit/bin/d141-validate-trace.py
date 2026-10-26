#!/usr/bin/env python3
"""Fail closed on missing, stale, malformed, or non-continuous body traces."""

from __future__ import annotations

import hashlib
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


def parent_binding(path: Path, owner_uid: int) -> tuple[int, str]:
    if not path.is_absolute() or path.name != "disk-trace.tsv":
        fail("trace path is not the fixed absolute file")
    if any(component in {".", ".."} for component in path.parts[1:]):
        fail("trace path contains traversal components")
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
                fail("trace parent is not an owned directory")
            if mode & (stat.S_IWGRP | stat.S_IWOTH) and not (item.st_uid == 0 and mode & stat.S_ISVTX):
                fail("trace parent is writable by an untrusted class")
            records.append(f"{component}:{item.st_dev}:{item.st_ino}:{item.st_uid}:{mode:o}")
        return descriptor, hashlib.sha256("|".join(records).encode()).hexdigest()
    except BaseException:
        os.close(descriptor)
        raise


def parse_binding(raw: str) -> tuple[int, int, int, int, int, str]:
    fields = raw.split("\t")
    if len(fields) != 7 or fields[0] != "ready":
        fail("sampler binding is malformed")
    try:
        values = [int(value, 8 if index == 3 else 10) for index, value in enumerate(fields[1:6])]
    except ValueError as exc:
        raise TraceError("sampler binding has non-numeric identity") from exc
    device, inode, owner, mode, links = values
    parent_hash = fields[6]
    if device < 0 or inode < 0 or owner < 0 or mode != 0o600 or links != 1 or len(parent_hash) != 64:
        fail("sampler binding has invalid identity")
    return device, inode, owner, mode, links, parent_hash


def check_trace(descriptor: int, binding: tuple[int, int, int, int, int, str] | None, owner_uid: int) -> None:
    item = os.fstat(descriptor)
    if not stat.S_ISREG(item.st_mode) or item.st_uid != owner_uid or stat.S_IMODE(item.st_mode) != 0o600 or item.st_nlink != 1:
        fail("trace is not a single-link owned regular file with mode 600")
    if binding is not None:
        device, inode, owner, mode, links, _ = binding
        if (item.st_dev, item.st_ino, item.st_uid, stat.S_IMODE(item.st_mode), item.st_nlink) != (device, inode, owner, mode, links):
            fail("trace identity, ownership, mode, or link count changed")


def read_descriptor(descriptor: int) -> bytes:
    chunks: list[bytes] = []
    size = 0
    while True:
        chunk = os.read(descriptor, 65536)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)
        size += len(chunk)
        if size > 16 * 1024 * 1024:
            fail("trace is too large")


def validate_rows(raw: bytes, job_id: str, body_pid: int) -> int:
    try:
        rows = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        fail(f"trace is not UTF-8: {exc}")
    expected = "timestamp_utc\tmonotonic_ns\tavailable_bytes\tjob_id\tbody_pid\tkind"
    if not rows or rows[0] != expected:
        fail("trace header mismatch")
    samples: list[tuple[datetime, int, int, str]] = []
    for raw_row in rows[1:]:
        fields = raw_row.split("\t")
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
    return len(samples)


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--fd":
        if len(argv) != 6:
            return 2
        descriptor, job_id, body_pid_text, owner_text, binding_text = int(argv[1]), argv[2], argv[3], argv[4], argv[5]
        owner_uid = int(owner_text)
        binding = parse_binding(binding_text)
        check_trace(descriptor, binding, owner_uid)
        os.lseek(descriptor, 0, os.SEEK_SET)
        count = validate_rows(read_descriptor(descriptor), job_id, int(body_pid_text))
    else:
        if len(argv) != 4:
            print("usage: validate-trace.py TRACE JOB_ID BODY_PID EXPECTED_OWNER_UID", file=sys.stderr)
            return 2
        path, job_id, body_pid, owner_uid = Path(argv[0]), argv[1], int(argv[2]), int(argv[3])
        parent_descriptor, _ = parent_binding(path, owner_uid)
        descriptor = -1
        try:
            flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
            check_trace(descriptor, None, owner_uid)
            count = validate_rows(read_descriptor(descriptor), job_id, body_pid)
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            os.close(parent_descriptor)
    print(f"trace PASS: {count} actual samples")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, ValueError, TraceError) as exc:
        print(f"trace rejected: {exc}", file=sys.stderr)
        raise SystemExit(1)
