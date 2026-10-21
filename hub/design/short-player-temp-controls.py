#!/usr/bin/env python3
"""Custody and path-budget checks for one per-run Chromium temp root.

This helper deliberately uses lstat/os.scandir semantics.  A Chrome-created
leaf symlink is removed as a link; its target is never traversed or removed.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import stat
import tempfile


CLAIM = ".vw-player-temp-claim"
PREFIX = "vw-"
TMP_ROOT = Path("/tmp")
OLD_SOCKET = (
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/vw-m3-gate6-runner-child-contract-repair-0803/"
    "tmp-5aZG7i/com.google.Chrome.tFXWh4/SingletonSocket"
)


class Refused(RuntimeError):
    pass


def _lstat(path: Path) -> os.stat_result:
    try:
        return path.lstat()
    except FileNotFoundError as exc:
        raise Refused(f"missing path: {path}") from exc


def _identity(path_stat: os.stat_result) -> tuple[int, int]:
    return path_stat.st_dev, path_stat.st_ino


def _read_claim(path: Path, *, expected_uid: int, root_stat: os.stat_result) -> None:
    claim = path / CLAIM
    claim_stat = _lstat(claim)
    if not stat.S_ISREG(claim_stat.st_mode) or stat.S_ISLNK(claim_stat.st_mode):
        raise Refused(f"invalid claim: {claim}")
    if claim_stat.st_uid != expected_uid or stat.S_IMODE(claim_stat.st_mode) != 0o600:
        raise Refused(f"foreign claim: {claim}")
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
    try:
        fd = os.open(claim, flags)
    except OSError as exc:
        raise Refused(f"cannot open claim: {claim}") from exc
    with os.fdopen(fd, "r", encoding="ascii") as stream:
        opened_claim_stat = os.fstat(stream.fileno())
        if _identity(opened_claim_stat) != _identity(claim_stat):
            raise Refused(f"claim changed while opening: {claim}")
        fields = {}
        for line in stream:
            key, separator, value = line.rstrip("\n").partition("=")
            if not separator or key in fields:
                raise Refused(f"malformed claim: {claim}")
            fields[key] = value
    if set(fields) != {"pid", "dev", "ino"}:
        raise Refused(f"malformed claim: {claim}")
    try:
        int(fields["pid"])
        claimed_identity = (int(fields["dev"]), int(fields["ino"]))
    except ValueError as exc:
        raise Refused(f"malformed claim: {claim}") from exc
    if claimed_identity != _identity(root_stat):
        raise Refused(
            f"root identity changed: {path} "
            f"claimed={claimed_identity[0]}:{claimed_identity[1]} "
            f"current={root_stat.st_dev}:{root_stat.st_ino}"
        )


def validate_root(path: Path, *, expected_uid: int | None = None) -> os.stat_result:
    """Validate a claimed, direct child of physical /tmp without resolving it."""

    if not path.is_absolute() or path.parent != TMP_ROOT:
        raise Refused(f"foreign root: {path}")
    if not path.name.startswith(PREFIX):
        raise Refused(f"foreign root name: {path}")
    root_stat = _lstat(path)
    if not stat.S_ISDIR(root_stat.st_mode) or stat.S_ISLNK(root_stat.st_mode):
        raise Refused(f"symlink/non-directory root: {path}")
    if expected_uid is None:
        expected_uid = os.getuid()
    if root_stat.st_uid != expected_uid:
        raise Refused(f"foreign owner: {path}")
    if stat.S_IMODE(root_stat.st_mode) != 0o700:
        raise Refused(f"root mode is not 0700: {path}")
    _read_claim(path, expected_uid=expected_uid, root_stat=root_stat)
    return root_stat


def claim(path: Path) -> None:
    path = Path(path)
    if not path.is_absolute() or path.parent != TMP_ROOT or not path.name.startswith(PREFIX):
        raise Refused(f"foreign root: {path}")
    root_stat = _lstat(path)
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise Refused(f"symlink/non-directory root: {path}")
    if root_stat.st_uid != os.getuid() or stat.S_IMODE(root_stat.st_mode) != 0o700:
        raise Refused(f"unowned or incorrectly protected root: {path}")
    claim_path = path / CLAIM
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    try:
        fd = os.open(claim_path, flags, 0o600)
    except FileExistsError as exc:
        raise Refused(f"root already claimed: {path}") from exc
    with os.fdopen(fd, "w", encoding="ascii") as stream:
        stream.write(
            f"pid={os.getpid()}\n"
            f"dev={root_stat.st_dev}\n"
            f"ino={root_stat.st_ino}\n"
        )
    print(
        f"claim=PASS root={path} mode=0700 owner={os.getuid()} "
        f"device={root_stat.st_dev} inode={root_stat.st_ino}"
    )


def _audit_owned_tree(path: Path) -> None:
    """Audit entries with lstat; symlink targets are intentionally opaque."""

    for current, dirs, files in os.walk(path, topdown=False, followlinks=False):
        current_path = Path(current)
        for name in files + dirs:
            entry = current_path / name
            entry_stat = _lstat(entry)
            if entry_stat.st_uid != os.getuid():
                raise Refused(f"foreign-owned entry: {entry}")


def cleanup(path: Path) -> None:
    path = Path(path)
    claimed_root_stat = validate_root(path)
    _audit_owned_tree(path)
    current_root_stat = validate_root(path)
    if _identity(current_root_stat) != _identity(claimed_root_stat):
        raise Refused(f"root identity changed before cleanup: {path}")
    # rmtree(unlink) is intentionally implemented with lstat and unlink so a
    # Chrome internal symlink is removed as a leaf and never followed.
    for current, dirs, files in os.walk(path, topdown=False, followlinks=False):
        current_root_stat = validate_root(path)
        if _identity(current_root_stat) != _identity(claimed_root_stat):
            raise Refused(f"root identity changed during cleanup: {path}")
        current_path = Path(current)
        for name in files:
            if current_path == path and name == CLAIM:
                continue
            entry = current_path / name
            if entry.is_symlink() or entry.is_file():
                entry.unlink()
            else:
                raise Refused(f"unexpected file node: {entry}")
        for name in dirs:
            entry = current_path / name
            if entry.is_symlink():
                entry.unlink()
            else:
                entry.rmdir()
    current_root_stat = validate_root(path)
    if _identity(current_root_stat) != _identity(claimed_root_stat):
        raise Refused(f"root identity changed before root removal: {path}")
    (path / CLAIM).unlink()
    path.rmdir()
    print(f"cleanup=PASS root={path} symlinks=unlinked-without-following")


def path_budget() -> None:
    short_root = "/tmp/vw-XXXXXX"
    # Bound the Chrome profile component before a run.  The observed Chrome
    # form is much shorter; 58 bytes is a conservative cap that stays below
    # the 108-byte Unix socket limit with this root and leaf name.
    profile_component = "com.google.Chrome." + ("x" * 58)
    short_socket = f"{short_root}/{profile_component}/SingletonSocket"
    if len(OLD_SOCKET.encode()) != 188:
        raise Refused(f"recorded long witness changed length={len(OLD_SOCKET.encode())}")
    if len(short_socket.encode()) >= 108:
        raise Refused(f"short worst-case exceeds 107 bytes: {len(short_socket.encode())}")
    print(f"long-witness-bytes={len(OLD_SOCKET.encode())}")
    print(f"short-worst-case-bytes={len(short_socket.encode())} (<108)")
    print(f"short-worst-case={short_socket}")


def self_test() -> None:
    path_budget()
    root = Path(tempfile.mkdtemp(prefix=PREFIX, dir=TMP_ROOT))
    os.chmod(root, 0o700)
    claim(root)
    outside = Path(tempfile.mkstemp(prefix="vw-foreign-target-", dir=TMP_ROOT)[1])
    (root / "com.google.Chrome.example").mkdir()
    (root / "com.google.Chrome.example" / "SingletonSocket").symlink_to(outside)
    cleanup(root)
    if not outside.exists():
        raise Refused("symlink target was followed or removed")
    outside.unlink()

    claimed = Path(tempfile.mkdtemp(prefix=PREFIX, dir=TMP_ROOT))
    os.chmod(claimed, 0o700)
    claim(claimed)
    replacement = Path(tempfile.mkdtemp(prefix="vw-replacement-", dir=TMP_ROOT))
    os.chmod(replacement, 0o700)
    shutil.copyfile(claimed / CLAIM, replacement / CLAIM)
    os.chmod(replacement / CLAIM, 0o600)
    (claimed / CLAIM).unlink()
    claimed.rmdir()
    replacement.rename(claimed)
    try:
        try:
            cleanup(claimed)
        except Refused as exc:
            if not claimed.exists() or not (claimed / CLAIM).exists():
                raise Refused("replacement root was removed on refusal") from exc
            print(f"replacement-root-refusal=PASS reason={exc}")
        else:
            raise Refused("replacement root accepted")
    finally:
        shutil.rmtree(claimed)

    unclaimed = Path(tempfile.mkdtemp(prefix=PREFIX, dir=TMP_ROOT))
    os.chmod(unclaimed, 0o700)
    try:
        try:
            validate_root(unclaimed)
        except Refused as exc:
            print(f"unclaimed-root-refusal=PASS reason={exc}")
        else:
            raise Refused("unclaimed root accepted")
    finally:
        shutil.rmtree(unclaimed)

    foreign = Path(tempfile.mkdtemp(prefix="foreign-", dir=TMP_ROOT))
    os.chmod(foreign, 0o700)
    try:
        try:
            validate_root(foreign)
        except Refused as exc:
            print(f"foreign-root-refusal=PASS reason={exc}")
        else:
            raise Refused("foreign root accepted")
        owner_probe = TMP_ROOT / f"vw-owner-{foreign.name}"
        foreign.rename(owner_probe)
        try:
            validate_root(owner_probe, expected_uid=os.getuid() + 1)
        except Refused as exc:
            print(f"owner-refusal=PASS reason={exc}")
        else:
            raise Refused("foreign owner accepted")
        finally:
            shutil.rmtree(owner_probe)
    finally:
        if foreign.exists():
            shutil.rmtree(foreign)

    target = Path(tempfile.mkdtemp(prefix="vw-symlink-target-", dir=TMP_ROOT))
    link = TMP_ROOT / "vw-symlink-root-self-test"
    link.symlink_to(target, target_is_directory=True)
    try:
        try:
            validate_root(link)
        except Refused as exc:
            print(f"symlink-root-refusal=PASS reason={exc}")
        else:
            raise Refused("symlink root accepted")
    finally:
        link.unlink()
        target.rmdir()
    print("self-test=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--claim")
    group.add_argument("--cleanup")
    group.add_argument("--paths", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.claim:
        claim(Path(args.claim))
    elif args.cleanup:
        cleanup(Path(args.cleanup))
    elif args.paths:
        path_budget()
    else:
        self_test()


if __name__ == "__main__":
    try:
        main()
    except Refused as exc:
        raise SystemExit(f"REFUSED: {exc}")
