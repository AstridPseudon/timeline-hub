#!/usr/bin/env python3
"""Append and validate a terminal trace through one custody-checked descriptor."""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def fail(message: str) -> None:
    raise RuntimeError(message)


def parent_binding(path: Path, owner_uid: int) -> tuple[int, str]:
    """Open every physical parent without following links and bind its identity."""
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
        raise RuntimeError("sampler binding has non-numeric identity") from exc
    device, inode, owner, mode, links = values
    parent_hash = fields[6]
    if device < 0 or inode < 0 or owner < 0 or mode != 0o600 or links != 1 or len(parent_hash) != 64:
        fail("sampler binding has invalid identity")
    return device, inode, owner, mode, links, parent_hash


def check_trace(descriptor: int, binding: tuple[int, int, int, int, int, str], owner_uid: int) -> None:
    item = os.fstat(descriptor)
    device, inode, owner, mode, links, _ = binding
    if (
        not stat.S_ISREG(item.st_mode)
        or item.st_dev != device
        or item.st_ino != inode
        or item.st_uid != owner
        or stat.S_IMODE(item.st_mode) != mode
        or item.st_nlink != links
        or item.st_uid != owner_uid
    ):
        fail("trace identity, ownership, mode, or link count changed")


def write_all(descriptor: int, raw: bytes) -> None:
    while raw:
        written = os.write(descriptor, raw)
        if written <= 0:
            fail("trace write made no progress")
        raw = raw[written:]


def available_bytes(probe: str) -> int:
    result = subprocess.run(["df", "-B1", "--output=avail", probe], check=True, capture_output=True, text=True)
    rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 2 or rows[0] != "Avail" or not rows[1].isdigit():
        raise RuntimeError(f"unexpected df output: {result.stdout!r}")
    return int(rows[1])


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        return 2
    trace, job_id, body_pid, probe, binding_text = Path(argv[0]), argv[1], int(argv[2]), argv[3], argv[4]
    owner_uid = os.getuid()
    binding = parse_binding(binding_text)
    parent_descriptor, parent_hash = parent_binding(trace, owner_uid)
    descriptor = -1
    try:
        if parent_hash != binding[5]:
            fail("trace parent identity changed")
        flags = os.O_RDWR | os.O_APPEND | os.O_CLOEXEC | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(trace.name, flags, dir_fd=parent_descriptor)
        check_trace(descriptor, binding, owner_uid)
        now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        write_all(descriptor, f"{now}\t{time.monotonic_ns()}\t{available_bytes(probe)}\t{job_id}\t{body_pid}\tfinal\n".encode())
        os.fsync(descriptor)
        validator = Path(__file__).with_name("d141-validate-trace.py")
        result = subprocess.run(
            [sys.executable, "-I", str(validator), "--fd", str(descriptor), job_id, str(body_pid), str(owner_uid), binding_text],
            check=False,
            pass_fds=(descriptor,),
            text=True,
            capture_output=True,
        )
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(parent_descriptor)


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"final trace sample failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
