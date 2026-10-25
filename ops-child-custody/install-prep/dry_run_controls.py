"""Private offline controls for the reviewed maker installation route.

Every target, backup, helper, and source path is created below a fresh TMPDIR
replica. This module never reads or writes ORCH/bin and never invokes the maker,
Store, package manager, network, or a source checkout mutation.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import stat
import tempfile


ROOT = Path(__file__).resolve().parents[2]
SOURCE_COMMIT = "09ed4999741b822fba7e8b3033ca28db6bcf8fa1"
PARENT_COMMIT = "9428f515fcd8dccaef26193438b3ac89f903f5aa"
SOURCE_REL = "ops-child-custody/make-child-venv"
CANDIDATE_SHA256 = "c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e"
CANDIDATE_BYTES = 69516
PREIMAGE_SHA256 = "0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39"
PREIMAGE_BYTES = 68351


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_owned(path: Path, mode: int = 0o755) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not stat.S_ISLNK(info.st_mode), f"symlink: {path}"
    assert info.st_nlink == 1, f"hardlink: {path}"
    assert info.st_uid == os.getuid(), f"owner mismatch: {path}"
    assert stat.S_IMODE(info.st_mode) == mode, f"mode mismatch: {path}"


def git_bytes(commit: str) -> bytes:
    import subprocess

    return subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{commit}:{SOURCE_REL}"],
    )


def write_extracted(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    path.chmod(0o755)


def cas_install(target: Path, candidate: Path, backup: Path) -> None:
    """Offline equivalent of the reviewed CAS/backup/atomic replacement."""

    regular_owned(target)
    assert digest(target) == PREIMAGE_SHA256
    assert target.stat().st_size == PREIMAGE_BYTES
    regular_owned(candidate)
    assert digest(candidate) == CANDIDATE_SHA256
    assert candidate.stat().st_size == CANDIDATE_BYTES
    assert not backup.exists() and not backup.is_symlink(), "backup clobber"

    # O_EXCL makes the no-clobber backup reservation atomic. It is a private
    # replica, so the only permission operation here is on the replica copy.
    fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o755)
    with os.fdopen(fd, "wb") as stream:
        stream.write(target.read_bytes())
    backup.chmod(0o755)
    regular_owned(backup)
    assert digest(backup) == PREIMAGE_SHA256

    replacement = target.with_name(f".{target.name}.replacement")
    assert not replacement.exists() and not replacement.is_symlink()
    shutil.copyfile(candidate, replacement)
    replacement.chmod(0o755)
    regular_owned(replacement)
    assert digest(replacement) == CANDIDATE_SHA256
    os.replace(replacement, target)

    regular_owned(target)
    assert digest(target) == CANDIDATE_SHA256
    assert target.stat().st_size == CANDIDATE_BYTES


def fresh_replica() -> tuple[Path, Path, Path, Path, Path]:
    temp_root = Path(os.environ.get("TMPDIR", tempfile.gettempdir())).resolve()
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
    positive_candidate_match()
    wrong_preimage_refusal()
    no_clobber_backup_refusal()
    protected_shape_refusals()
    print("PASS: private candidate match, wrong-preimage refusal, no-clobber backup, helper invariance, and shape guards")


if __name__ == "__main__":
    main()
