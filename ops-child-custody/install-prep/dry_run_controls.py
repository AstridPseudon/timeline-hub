"""Private offline controls for the reviewed maker installation route.

Every target, backup, helper, source, lock, and temporary path is created below
a fresh TMPDIR replica. This module never reads or writes a live ORCH tree and
never invokes the maker, Store, package manager, network, or source mutation.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from install_atomic import copy_reserved, rename_if_same  # noqa: E402


SOURCE_COMMIT = "D137_DECISION_SOURCE_COMMIT"
PARENT_COMMIT = "cf80cfcb918ee9e311a294fb7291ad5e11c48d0b"
SOURCE_REL = "ops-child-custody/make-child-venv"
CANDIDATE_SHA256 = "5b6bfa01a74e7760e2cefe6713c0557cca695abb61074b3f01c9391949cfb064"
CANDIDATE_BYTES = 93300
PREIMAGE_SHA256 = "f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f"
PREIMAGE_BYTES = 75541
UID = os.getuid()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_owned(path: Path, mode: int = 0o755) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not stat.S_ISLNK(info.st_mode), f"symlink: {path}"
    assert info.st_nlink == 1, f"hardlink: {path}"
    assert info.st_uid == UID, f"owner mismatch: {path}"
    assert stat.S_IMODE(info.st_mode) == mode, f"mode mismatch: {path}"


def git_bytes(commit: str) -> bytes:
    import subprocess

    if commit == SOURCE_COMMIT:
        return (ROOT / SOURCE_REL).read_bytes()
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{commit}:{SOURCE_REL}"],
    )


def write_extracted(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    path.chmod(0o755)


def cas_install(target: Path, candidate: Path, backup: Path) -> None:
    """Offline equivalent of the lock/CAS/backup/atomic replacement route."""

    regular_owned(target)
    assert digest(target) == PREIMAGE_SHA256
    assert target.stat().st_size == PREIMAGE_BYTES
    regular_owned(candidate)
    assert digest(candidate) == CANDIDATE_SHA256
    assert candidate.stat().st_size == CANDIDATE_BYTES
    assert not backup.exists() and not backup.is_symlink(), "backup clobber"
    lock = target.parent / ".make-child-venv.install.lock"
    lock.mkdir()
    try:
        target_info = target.stat()
        copy_reserved(target, backup, UID, 0o755)
        regular_owned(backup)
        assert digest(backup) == PREIMAGE_SHA256
        replacement = target.with_name(f".{target.name}.replacement")
        copy_reserved(candidate, replacement, UID, 0o755)
        regular_owned(replacement)
        assert digest(replacement) == CANDIDATE_SHA256
        rename_if_same(
            target.parent,
            target.name,
            replacement.name,
            target_info.st_dev,
            target_info.st_ino,
            UID,
            0o755,
        )
    finally:
        lock.rmdir()
    regular_owned(target)
    assert digest(target) == CANDIDATE_SHA256
    assert target.stat().st_size == CANDIDATE_BYTES


def fresh_replica() -> tuple[Path, Path, Path, Path, Path]:
    temp_root = private_tmp_parent()
    root = Path(tempfile.mkdtemp(prefix="ops-install-prep-", dir=temp_root)).resolve()
    assert root.is_relative_to(temp_root)
    target = root / "orch/bin/make-child-venv"
    backup = root / "orch/backups/make-child-venv.20261025T000000Z.bak"
    helper = root / "orch/bin/bench_store.py"
    dependency = root / "orch/bin/verify_dependency_seed.py"
    candidate = root / "private-source/ops-child-custody/make-child-venv"
    target.parent.mkdir(parents=True)
    backup.parent.mkdir()
    helper.write_bytes(b"protected Store helper replica\n")
    dependency.write_bytes(b"protected dependency helper replica\n")
    helper.chmod(0o755)
    dependency.chmod(0o755)
    write_extracted(target, git_bytes(PARENT_COMMIT))
    write_extracted(candidate, git_bytes(SOURCE_COMMIT))
    assert digest(target) == PREIMAGE_SHA256
    assert digest(candidate) == CANDIDATE_SHA256
    regular_owned(helper)
    regular_owned(dependency)
    return root, target, backup, helper, dependency


def positive_candidate_match() -> None:
    root, target, backup, helper, dependency = fresh_replica()
    before_helpers = digest(helper), digest(dependency)
    cas_install(target, root / "private-source/ops-child-custody/make-child-venv", backup)
    assert digest(helper) == before_helpers[0]
    assert digest(dependency) == before_helpers[1]
    assert digest(target) == CANDIDATE_SHA256
    assert digest(backup) == PREIMAGE_SHA256


def wrong_preimage_refusal() -> None:
    root, target, backup, helper, dependency = fresh_replica()
    target.write_bytes(target.read_bytes() + b"wrong-preimage")
    target.chmod(0o755)
    before_target = target.read_bytes()
    before_helpers = digest(helper), digest(dependency)
    try:
        cas_install(target, root / "private-source/ops-child-custody/make-child-venv", backup)
    except AssertionError:
        pass
    else:
        raise AssertionError("wrong preimage was accepted")
    assert target.read_bytes() == before_target
    assert not backup.exists()
    assert (digest(helper), digest(dependency)) == before_helpers


def no_clobber_backup_refusal() -> None:
    root, target, backup, helper, dependency = fresh_replica()
    backup.write_bytes(b"existing backup sentinel\n")
    backup.chmod(0o755)
    before_target = target.read_bytes()
    before_backup = backup.read_bytes()
    before_helpers = digest(helper), digest(dependency)
    try:
        cas_install(target, root / "private-source/ops-child-custody/make-child-venv", backup)
    except AssertionError:
        pass
    else:
        raise AssertionError("existing backup was clobbered")
    assert target.read_bytes() == before_target
    assert backup.read_bytes() == before_backup
    assert (digest(helper), digest(dependency)) == before_helpers


def descriptor_reservation_guards() -> None:
    root, target, backup, helper, dependency = fresh_replica()
    outside = root / "outside-sentinel"
    outside.write_bytes(b"must remain unchanged\n")
    outside.chmod(0o755)
    for destination in (
        root / "orch/backups/backup-reservation",
        root / "orch/bin/replacement-reservation",
    ):
        destination.symlink_to(outside)
        try:
            copy_reserved(target, destination, UID, 0o755)
        except FileExistsError:
            pass
        else:
            raise AssertionError("symlink reservation was accepted")
        assert outside.read_bytes() == b"must remain unchanged\n"


def identity_cas_refusal() -> None:
    root, target, backup, helper, dependency = fresh_replica()
    replacement = target.with_name(".replacement")
    copy_reserved(root / "private-source/ops-child-custody/make-child-venv", replacement, UID, 0o755)
    original = target.stat()
    changed = target.with_name(".changed-target")
    write_extracted(changed, b"changed target")
    os.replace(changed, target)
    try:
        rename_if_same(
            target.parent,
            target.name,
            replacement.name,
            original.st_dev,
            original.st_ino,
            UID,
            0o755,
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError("changed target identity was accepted")
    assert replacement.exists()
    assert target.read_bytes() == b"changed target"


def private_tmp_parent() -> Path:
    temp_root = Path(os.environ.get("TMPDIR", tempfile.gettempdir())).resolve()
    info = temp_root.lstat()
    assert stat.S_ISDIR(info.st_mode), "TMPDIR is not a directory"
    assert not stat.S_ISLNK(info.st_mode), "TMPDIR is a symlink"
    assert info.st_uid == UID, "TMPDIR owner mismatch"
    assert stat.S_IMODE(info.st_mode) & 0o022 == 0, "TMPDIR is broadly writable"
    return temp_root


def protected_shape_refusals() -> None:
    root, target, backup, helper, dependency = fresh_replica()
    candidate = root / "private-source/ops-child-custody/make-child-venv"
    target_link = root / "target-link"
    target_link.symlink_to(target)
    try:
        regular_owned(target_link)
    except AssertionError:
        pass
    else:
        raise AssertionError("symlink target accepted")
    target_link.unlink()
    target_hardlink = root / "target-hardlink"
    os.link(target, target_hardlink)
    try:
        regular_owned(target)
    except AssertionError:
        pass
    else:
        raise AssertionError("hardlinked target accepted")
    assert digest(candidate) == CANDIDATE_SHA256


def main() -> None:
    private_tmp_parent()
    positive_candidate_match()
    wrong_preimage_refusal()
    no_clobber_backup_refusal()
    descriptor_reservation_guards()
    identity_cas_refusal()
    protected_shape_refusals()
    print("PASS: private candidate, preimage, no-clobber, descriptor race, identity CAS, helper, symlink, and hardlink controls")


if __name__ == "__main__":
    main()

