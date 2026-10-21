#!/usr/bin/env python3
"""Pure custody and socket-budget controls for the Player-only temp root."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import tempfile
from pathlib import Path


SOCKET_SUFFIX = Path("com.google.Chrome.12345678901234567890") / "SingletonSocket"
SHORT_NAME = re.compile(r"vw-[A-Za-z0-9_-]+\Z")
MAX_SOCKET_BYTES = 108


def socket_bytes(root: Path, suffix: Path = SOCKET_SUFFIX) -> int:
    return len(os.fsencode(root / suffix))


def assert_short_root(root: Path, *, expected_uid: int | None = None) -> None:
    if not root.is_absolute() or root.parent != Path("/tmp") or not SHORT_NAME.fullmatch(root.name):
        raise AssertionError(f"short Player root must be a direct /tmp/vw-<id> directory: {root}")
    info = root.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise AssertionError("short Player root must be a real directory")
    if expected_uid is not None and info.st_uid != expected_uid:
        raise AssertionError("short Player root is not owned by this run")
    if stat.S_IMODE(info.st_mode) != 0o700:
        raise AssertionError("short Player root must be mode 0700")
    if socket_bytes(root) >= MAX_SOCKET_BYTES:
        raise AssertionError("Chrome SingletonSocket path exceeds AF_UNIX capacity")


def cleanup_owned_root(root: Path, *, expected_uid: int) -> None:
    """Delete only a still-real, still-owned root after evidence is written."""
    assert_short_root(root, expected_uid=expected_uid)
    for entry in root.rglob("*"):
        info = entry.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != expected_uid:
            raise AssertionError("refusing cleanup of foreign or symlinked Player temp content")
    shutil.rmtree(root)
    if root.exists() or root.is_symlink():
        raise AssertionError("owned Player temp cleanup did not remove the root")


def run_controls() -> None:
    uid = os.getuid()
    root = Path(tempfile.mkdtemp(prefix="vw-", dir="/tmp"))
    root.chmod(0o700)
    foreign_link = Path(tempfile.mkdtemp(prefix="vw-", dir="/tmp"))
    foreign_link.chmod(0o700)
    try:
        assert_short_root(root, expected_uid=uid)
        assert socket_bytes(root) < MAX_SOCKET_BYTES

        too_long = Path("/tmp") / ("x" * 100)
        assert socket_bytes(too_long) >= MAX_SOCKET_BYTES

        try:
            assert_short_root(root, expected_uid=uid + 1)
        except AssertionError:
            pass
        else:
            raise AssertionError("foreign-owner control was accepted")

        alias = foreign_link / "alias"
        alias.symlink_to(root, target_is_directory=True)
        try:
            assert_short_root(alias, expected_uid=uid)
        except (AssertionError, FileNotFoundError):
            pass
        else:
            raise AssertionError("symlinked-root control was accepted")

        child_alias = root / "child-alias"
        child_alias.symlink_to(foreign_link, target_is_directory=True)
        try:
            cleanup_owned_root(root, expected_uid=uid)
        except AssertionError:
            pass
        else:
            raise AssertionError("cleanup followed a planted symlink")
        child_alias.unlink()
        cleanup_owned_root(root, expected_uid=uid)
        print("short-player-temp-controls=PASS")
    finally:
        shutil.rmtree(root, ignore_errors=True)
        shutil.rmtree(foreign_link, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-path", type=Path)
    parser.add_argument("--witness", type=Path)
    parser.add_argument("suffix", nargs="?", default=str(SOCKET_SUFFIX))
    parser.add_argument("--cleanup", type=Path)
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    if args.witness is not None:
        measured = socket_bytes(args.witness, Path(args.suffix))
        if measured < MAX_SOCKET_BYTES:
            raise AssertionError("recorded long Player temp shape is not a negative socket-path witness")
        print(f"recorded-long-player-socket-bytes={measured}")
    elif args.check_path is not None:
        assert_short_root(args.check_path, expected_uid=os.getuid())
        print(f"short-player-socket-bytes={socket_bytes(args.check_path)}")
    elif args.cleanup is not None:
        cleanup_owned_root(args.cleanup, expected_uid=os.getuid())
        print("short-player-temp-cleanup=PASS")
    else:
        run_controls()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
