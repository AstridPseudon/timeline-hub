#!/usr/bin/env python3
"""Validate one dispatcher-attached D89d measured-floor receipt.

The receipt is data only.  This validator has no execution, import, or
source-selection fields; its output is the one computed floor in bytes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any


class ReceiptError(ValueError):
    """A receipt is not admissible for this dispatch."""


def fail(message: str) -> None:
    raise ReceiptError(message)


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> Any:
    fail(f"non-finite JSON number: {value}")


def exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict:
        fail(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        fail(f"{label} keys differ (missing={missing}, extra={extra})")
    return value


def integer(value: Any, label: str) -> int:
    if type(value) is not int:
        fail(f"{label} must be an integer")
    return value


def nonnegative(value: Any, label: str) -> int:
    result = integer(value, label)
    if result < 0:
        fail(f"{label} must be nonnegative")
    return result


def text(value: Any, label: str) -> str:
    if type(value) is not str or not value:
        fail(f"{label} must be a non-empty string")
    return value


def no_symlink_components(path: Path) -> None:
    if not path.is_absolute():
        fail(f"path is not absolute: {path}")
    current = Path(path.anchor)
    for component in path.parts[1:]:
        current /= component
        try:
            item = os.lstat(current)
        except OSError as exc:
            fail(f"path is unreadable: {path}: {exc}")
        if stat.S_ISLNK(item.st_mode):
            fail(f"path contains symlink: {path}")


def read_regular_nofollow(path: Path, owner_uid: int | None = None) -> tuple[bytes, os.stat_result]:
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow | os.O_CLOEXEC)
    except OSError as exc:
        fail(f"path cannot be opened without following links: {path}: {exc}")
    try:
        item = os.fstat(descriptor)
        if not stat.S_ISREG(item.st_mode):
            fail(f"path is not a regular file: {path}")
        if owner_uid is not None and item.st_uid != owner_uid:
            fail(f"path owner differs: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            chunks.append(chunk)
            if sum(map(len, chunks)) > 1_048_576:
                fail(f"path is too large: {path}")
    except OSError as exc:
        fail(f"path cannot be read: {path}: {exc}")
    finally:
        os.close(descriptor)
    return b"".join(chunks), item


def witness_path(root: Path, relative: Any) -> Path:
    relative_text = text(relative, "witness.path")
    if "\\" in relative_text or relative_text.startswith("/"):
        fail(f"witness path must be a relative POSIX path: {relative_text}")
    components = relative_text.split("/")
    if any(component in {"", ".", ".."} for component in components):
        fail(f"witness path contains an unsafe component: {relative_text}")
    path = root.joinpath(*components)
    no_symlink_components(path)
    try:
        if path.relative_to(root) != path:
            fail(f"witness escapes trusted manager root: {relative_text}")
    except ValueError:
        fail(f"witness escapes trusted manager root: {relative_text}")
    return path


def witness_value(raw: bytes, path: Path) -> int:
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        fail(f"witness is not UTF-8: {path}")
    lines = decoded.splitlines()
    if len(lines) != 2 or lines[0].strip() != "Avail" or not decoded.endswith("\n"):
        fail(f"witness has unexpected df format: {path}")
    value = lines[1].strip()
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)", value):
        fail(f"witness value is not a strict decimal integer: {path}")
    return int(value)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def validate(
    receipt_path: Path,
    manager_root: Path,
    job_id: str,
    repo: str,
    suite: str,
    worktree: Path,
    head: str,
    tree: str,
    command: str,
) -> int:
    no_symlink_components(manager_root)
    root_stat = os.lstat(manager_root)
    if not stat.S_ISDIR(root_stat.st_mode):
        fail("trusted manager root is not a directory")
    if root_stat.st_uid != 0:
        fail("trusted manager root is not manager-owned")
    if root_stat.st_mode & 0o022:
        fail("trusted manager root is writable by group or other")

    expected_receipt = manager_root / "tests" / job_id / "recorded-measured-floor.json"
    if receipt_path != expected_receipt:
        fail("receipt is not attached at the fixed per-job path")
    no_symlink_components(receipt_path)
    raw_receipt, receipt_stat = read_regular_nofollow(receipt_path, root_stat.st_uid)
    try:
        decoded = raw_receipt.decode("utf-8")
        value = json.loads(
            decoded,
            object_pairs_hook=unique_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"receipt is not strict JSON: {exc}")
    root = exact_keys(
        value,
        {"schema", "trusted_manager_root", "manager_owner_uid", "scope", "measurement", "witnesses"},
        "receipt",
    )
    if root["schema"] != "timeline.d89d.measured-floor.v1":
        fail("unsupported receipt schema")
    if root["trusted_manager_root"] != str(manager_root):
        fail("receipt trusted manager root mismatch")
    if integer(root["manager_owner_uid"], "manager_owner_uid") != root_stat.st_uid:
        fail("receipt manager owner mismatch")
    if receipt_stat.st_uid != root_stat.st_uid:
        fail("receipt owner mismatch")

    scope = exact_keys(root["scope"], {"job_id", "repo", "suite", "source"}, "scope")
    if scope["job_id"] != job_id or scope["repo"] != repo or scope["suite"] != suite:
        fail("receipt job/repo/suite scope mismatch")
    source = exact_keys(scope["source"], {"head", "tree", "command_sha256"}, "scope.source")
    if source["head"] != head or source["tree"] != tree:
        fail("receipt source revision/tree mismatch")
    if source["command_sha256"] != sha256(command.encode()):
        fail("receipt suite command mismatch")

    measurement = exact_keys(
        root["measurement"],
        {"growth_bytes", "floor_bytes", "minimum_bytes", "stop_bytes", "margin_bytes", "semantics"},
        "measurement",
    )
    growth_claim = nonnegative(measurement["growth_bytes"], "measurement.growth_bytes")
    floor_claim = nonnegative(measurement["floor_bytes"], "measurement.floor_bytes")
    if measurement["minimum_bytes"] != 4_600_000_000:
        fail("measurement minimum is not the D89d minimum")
    if measurement["stop_bytes"] != 4_000_000_000:
        fail("measurement stop line changed")
    if measurement["margin_bytes"] != 200_000_000:
        fail("measurement margin changed")
    if measurement["semantics"] != "start_end_bracket_delta_only_not_continuous_peak":
        fail("measurement semantics must disclose bracket-only growth")

    witnesses = root["witnesses"]
    if type(witnesses) is not list or len(witnesses) != 2:
        fail("receipt must contain exactly two witnesses")
    roles: set[str] = set()
    values: dict[str, int] = {}
    for raw_witness in witnesses:
        witness = exact_keys(
            raw_witness,
            {"role", "path", "sha256", "owner_uid", "owner_gid"},
            "witness",
        )
        role = text(witness["role"], "witness.role")
        if role not in {"start", "stop"} or role in roles:
            fail("witness roles must be unique start and stop")
        roles.add(role)
        owner_uid = integer(witness["owner_uid"], "witness.owner_uid")
        owner_gid = integer(witness["owner_gid"], "witness.owner_gid")
        if owner_uid != root_stat.st_uid or owner_gid != root_stat.st_gid:
            fail("witness owner is not the trusted manager")
        digest = text(witness["sha256"], "witness.sha256")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            fail("witness sha256 is not lowercase hexadecimal")
        path = witness_path(manager_root, witness["path"])
        raw, item = read_regular_nofollow(path, owner_uid)
        if item.st_gid != owner_gid:
            fail(f"witness group owner differs: {path}")
        if sha256(raw) != digest:
            fail(f"witness hash mismatch: {path}")
        values[role] = witness_value(raw, path)
    if roles != {"start", "stop"}:
        fail("receipt must contain start and stop witnesses")
    growth = values["start"] - values["stop"]
    if growth < 0 or growth != growth_claim:
        fail("receipt growth does not match the witness values")
    expected_floor = max(4_600_000_000, 4_000_000_000 + growth + 200_000_000)
    if floor_claim != expected_floor:
        fail("receipt floor arithmetic mismatch")
    return floor_claim


def main(argv: list[str]) -> int:
    if len(argv) != 10:
        print("measured-floor validator requires exactly nine arguments", file=sys.stderr)
        return 2
    try:
        floor = validate(
            Path(argv[1]),
            Path(argv[2]),
            argv[3],
            argv[4],
            argv[5],
            Path(argv[6]),
            argv[7],
            argv[8],
            argv[9],
        )
    except ReceiptError as exc:
        print(f"receipt rejected: {exc}", file=sys.stderr)
        return 1
    print(floor)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
