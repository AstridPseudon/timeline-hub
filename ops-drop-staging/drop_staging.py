"""Guarded removal of one finished worker's regenerable staging directory.

This module is intentionally standalone.  The normal kit installs the
``drop-staging`` launcher beside ``bin/`` and derives ``workers/`` from that
installation; tests pass a private workers root explicitly.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import secrets
import shutil
import stat
import sys
import tarfile
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXIT_REFUSED = 2
EXIT_ERROR = 1
MANIFEST_RELATIVE = Path("evidence") / "manifest.json"
DROP_LOG_NAME = "staging-drop.log"
MARKER_NAMES = frozenset({"ACTIVE", "active", "KEEP", "keep", "LEASE", "lease"})
ARCHIVE_RESERVE_BYTES = 1 << 20


class DropError(RuntimeError):
    """An operational failure after preflight, not a guard refusal."""


@dataclass(frozen=True)
class EvidenceSnapshot:
    manifest_path: Path
    files: tuple[dict[str, Any], ...]
    digest: str
    manifest_identity: tuple[int, ...]


@dataclass(frozen=True)
class TreeEntry:
    path: str
    kind: str
    size: int
    mode: int
    sha256: str | None
    device: int
    inode: int

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "path": self.path,
            "kind": self.kind,
            "size": self.size,
            "mode": self.mode,
        }
        if self.sha256 is not None:
            result["sha256"] = self.sha256
        result["identity"] = {"device": self.device, "inode": self.inode}
        return result


@dataclass(frozen=True)
class Preflight:
    worker: Path
    target: Path
    target_parts: tuple[str, ...]
    evidence: EvidenceSnapshot
    listing: tuple[TreeEntry, ...]
    listing_sha256: str
    logical_bytes: int
    workers_root_identity: tuple[int, ...]
    orchestration_identity: tuple[int, ...]
    worker_identity: tuple[int, ...]
    target_identity: tuple[int, ...]


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _identity(info: os.stat_result, *, content: bool = True) -> tuple[int, ...]:
    values = (info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid)
    if content:
        return values + (info.st_size, info.st_mtime_ns, info.st_ctime_ns)
    return values


def _listing_identity(info: os.stat_result) -> tuple[int, int]:
    return info.st_dev, info.st_ino


def _same_identity(
    left: os.stat_result, right: os.stat_result, *, content: bool = True
) -> bool:
    return _identity(left, content=content) == _identity(right, content=content)


def _sha256_fd(fd: int, description: str) -> tuple[str, os.stat_result]:
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise DropError(f"{description} is not a regular file")
        os.lseek(fd, 0, os.SEEK_SET)
        digest = hashlib.sha256()
        for chunk in iter(lambda: os.read(fd, 1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(fd)
    except OSError as exc:
        raise DropError(f"could not hash {description}: {exc.strerror or exc}") from exc
    if not _same_identity(before, after):
        raise DropError(f"{description} changed while it was being read")
    return digest.hexdigest(), after


def _read_fd(fd: int, description: str) -> tuple[bytes, os.stat_result]:
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise DropError(f"{description} is not a regular file")
        os.lseek(fd, 0, os.SEEK_SET)
        data = bytearray()
        for chunk in iter(lambda: os.read(fd, 1024 * 1024), b""):
            data.extend(chunk)
        after = os.fstat(fd)
    except OSError as exc:
        raise DropError(f"could not read {description}: {exc.strerror or exc}") from exc
    if not _same_identity(before, after):
        raise DropError(f"{description} changed while it was being read")
    return bytes(data), after


def _mode(mode: int) -> int:
    return stat.S_IMODE(mode)


def _lstat(path: Path) -> os.stat_result:
    try:
        return path.lstat()
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise DropError(f"could not inspect {path}: {exc.strerror or exc}") from exc


def _regular_file(path: Path, description: str) -> bool:
    try:
        info = _lstat(path)
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(info.st_mode):
        return False
    return stat.S_ISREG(info.st_mode)


def _relative_parts(value: str, *, label: str) -> tuple[tuple[str, ...], list[str]]:
    reasons: list[str] = []
    raw = Path(value)
    if not value or raw.is_absolute():
        reasons.append(f"{label} must be a non-empty relative path")
        return (), reasons
    parts = tuple(raw.parts)
    if not parts or any(part in {"", ".", ".."} for part in parts):
        reasons.append(f"{label} contains traversal or dot path components")
    if os.sep == "/" and any("\\" in part for part in parts):
        reasons.append(f"{label} contains a platform path separator")
    return parts, reasons


def _worker_root_ok(root: Path, reasons: list[str]) -> bool:
    try:
        info = root.lstat()
    except FileNotFoundError:
        reasons.append(f"workers root does not exist: {root}")
        return False
    except OSError as exc:
        reasons.append(f"workers root cannot be inspected: {exc.strerror or exc}")
        return False
    if stat.S_ISLNK(info.st_mode):
        reasons.append("workers root is a symlink")
        return False
    if not stat.S_ISDIR(info.st_mode):
        reasons.append("workers root is not a directory")
        return False
    return True


def _check_no_symlink_components(path: Path, stop: Path, reasons: list[str]) -> None:
    current = stop
    try:
        relative = path.relative_to(stop)
    except ValueError:
        reasons.append("target is outside the worker record")
        return
    for part in relative.parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            return
        except OSError as exc:
            reasons.append(
                f"cannot inspect path component {current}: {exc.strerror or exc}"
            )
            return
        if stat.S_ISLNK(info.st_mode):
            reasons.append(
                f"symlink path component refused: {current.relative_to(stop)}"
            )


def _marker_names(worker: Path) -> list[str]:
    try:
        names = {entry.name for entry in worker.iterdir()}
    except OSError:
        return []
    return sorted(names & MARKER_NAMES)


def _open_dir_at(parent_fd: int, name: str) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    try:
        return os.open(name, flags, dir_fd=parent_fd)
    except OSError as exc:
        raise DropError(
            f"could not securely open directory {name}: {exc.strerror or exc}"
        ) from exc


def _open_regular_at(
    parent_fd: int, parts: tuple[str, ...], description: str
) -> tuple[int, os.stat_result]:
    if not parts:
        raise DropError(f"empty path for {description}")
    opened: list[int] = []
    current = parent_fd
    try:
        for part in parts[:-1]:
            child = _open_dir_at(current, part)
            opened.append(child)
            current = child
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(parts[-1], flags, dir_fd=current)
        except OSError as exc:
            raise DropError(
                f"could not securely open {description}: {exc.strerror or exc}"
            ) from exc
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):
                os.close(fd)
                raise DropError(f"{description} is not a regular file")
            return fd, info
        except BaseException:
            if "fd" in locals():
                try:
                    os.close(fd)
                except OSError:
                    pass
            raise
    finally:
        for fd in reversed(opened):
            os.close(fd)


def _active_lease_reasons_fd(
    orch_fd: int, manager_root_name: str, worker_name: str
) -> list[str]:
    """Inspect leases below a stable orchestration-root descriptor.

    Any symlink or unreadable reference in the manager lease tree is ambiguous
    and therefore a refusal.  Missing optional manager/notes roots are fine.
    """
    reasons: list[str] = []
    try:
        managers_fd = _open_dir_at(orch_fd, "managers")
    except DropError as exc:
        if "No such file or directory" in str(exc):
            return reasons
        return [f"cannot inspect manager lease root: {exc}"]
    try:
        manager_dirs = sorted(os.scandir(managers_fd), key=lambda entry: entry.name)
    except OSError as exc:
        os.close(managers_fd)
        return [f"cannot inspect manager leases: {exc.strerror or exc}"]
    try:
        for manager_entry in manager_dirs:
            manager_name = manager_entry.name
            try:
                manager_info = manager_entry.stat(follow_symlinks=False)
            except OSError as exc:
                reasons.append(
                    f"cannot inspect manager lease root {manager_name}: {exc.strerror or exc}"
                )
                continue
            if stat.S_ISLNK(manager_info.st_mode):
                reasons.append(f"manager lease root is a symlink: {manager_name}")
                continue
            if not stat.S_ISDIR(manager_info.st_mode):
                continue
            try:
                manager_fd = _open_dir_at(managers_fd, manager_name)
            except DropError as exc:
                reasons.append(
                    f"cannot inspect manager lease root {manager_name}: {exc}"
                )
                continue
            try:
                try:
                    notes_info = os.stat(
                        "notes", dir_fd=manager_fd, follow_symlinks=False
                    )
                except FileNotFoundError:
                    continue
                except OSError as exc:
                    reasons.append(
                        f"cannot inspect manager notes {manager_name}: {exc.strerror or exc}"
                    )
                    continue
                if stat.S_ISLNK(notes_info.st_mode) or not stat.S_ISDIR(
                    notes_info.st_mode
                ):
                    reasons.append(
                        f"manager notes root is unsafe: {manager_name}/notes"
                    )
                    continue
                try:
                    notes_fd = _open_dir_at(manager_fd, "notes")
                except DropError as exc:
                    reasons.append(
                        f"cannot inspect manager notes {manager_name}: {exc}"
                    )
                    continue
                try:
                    try:
                        candidates = sorted(
                            os.scandir(notes_fd), key=lambda entry: entry.name
                        )
                    except OSError as exc:
                        reasons.append(
                            f"cannot inspect manager leases: {exc.strerror or exc}"
                        )
                        continue
                    for candidate in candidates:
                        if not (
                            candidate.name.endswith(".lease")
                            or "ACTIVE" in candidate.name
                        ):
                            continue
                        try:
                            info = candidate.stat(follow_symlinks=False)
                        except OSError as exc:
                            reasons.append(
                                f"cannot inspect lease {manager_name}/notes/{candidate.name}: {exc.strerror or exc}"
                            )
                            continue
                        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                            reasons.append(
                                f"lease reference is unsafe: {manager_name}/notes/{candidate.name}"
                            )
                            continue
                        try:
                            fd, _ = _open_regular_at(
                                notes_fd, (candidate.name,), f"lease {candidate.name}"
                            )
                            try:
                                data, after = _read_fd(fd, f"lease {candidate.name}")
                            finally:
                                os.close(fd)
                        except DropError as exc:
                            reasons.append(str(exc))
                            continue
                        if not _same_identity(info, after):
                            reasons.append(
                                f"lease changed while it was read: {candidate.name}"
                            )
                            continue
                        content = data.decode("utf-8", errors="replace")
                        if worker_name in content or worker_name in candidate.name:
                            reasons.append(
                                f"active lease/marker names worker: {manager_name}/notes/{candidate.name}"
                            )
                finally:
                    os.close(notes_fd)
            finally:
                os.close(manager_fd)
    finally:
        os.close(managers_fd)
    return reasons


def _active_lease_reasons(workers_root: Path, worker_name: str) -> list[str]:
    try:
        orch_fd = _open_dir(workers_root.parent)
    except DropError as exc:
        return [f"cannot inspect orchestration root: {exc}"]
    try:
        return _active_lease_reasons_fd(orch_fd, workers_root.name, worker_name)
    finally:
        os.close(orch_fd)


def _marker_names_fd(directory_fd: int) -> list[str]:
    try:
        with os.scandir(directory_fd) as entries:
            return sorted(entry.name for entry in entries if entry.name in MARKER_NAMES)
    except OSError as exc:
        raise DropError(
            f"cannot inspect protected markers: {exc.strerror or exc}"
        ) from exc


def _protected_ancestor_reasons_fd(worker_fd: int, parts: tuple[str, ...]) -> list[str]:
    reasons: list[str] = []
    opened: list[int] = []
    current = worker_fd
    try:
        for index, part in enumerate(parts):
            for marker in _marker_names_fd(current):
                prefix = "/".join(parts[:index]) or "."
                reasons.append(
                    f"protected marker applies to target ancestor: {prefix}/{marker}"
                )
            if part in MARKER_NAMES:
                reasons.append(
                    f"protected marker applies to target ancestor: {'/'.join(parts[: index + 1])}"
                )
            child = _open_dir_at(current, part)
            opened.append(child)
            current = child
    except DropError as exc:
        reasons.append(str(exc))
    finally:
        for fd in reversed(opened):
            os.close(fd)
    return reasons


def _safe_walk_fd(root_fd: int, reasons: list[str]) -> tuple[TreeEntry, ...]:
    entries: list[TreeEntry] = []

    try:
        root_info = os.fstat(root_fd)
    except OSError as exc:
        reasons.append(f"cannot inspect staging root: {exc.strerror or exc}")
        return ()
    if not stat.S_ISDIR(root_info.st_mode):
        reasons.append("staging root is not a directory")
        return ()
    entries.append(
        TreeEntry(
            ".",
            "directory",
            0,
            _mode(root_info.st_mode),
            None,
            *_listing_identity(root_info),
        )
    )

    def visit(directory_fd: int, relative: str) -> None:
        try:
            candidates = sorted(os.scandir(directory_fd), key=lambda entry: entry.name)
        except OSError as exc:
            reasons.append(f"cannot inspect manager leases: {exc.strerror or exc}")
            return
        try:
            for entry in candidates:
                child_relative = (
                    entry.name if relative == "." else f"{relative}/{entry.name}"
                )
                if entry.name in MARKER_NAMES:
                    reasons.append(f"protected marker inside staging: {child_relative}")
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    reasons.append(
                        f"cannot inspect staging entry {child_relative}: {exc.strerror or exc}"
                    )
                    continue
                if stat.S_ISLNK(info.st_mode):
                    reasons.append(f"symlink inside staging refused: {child_relative}")
                    continue
                if stat.S_ISREG(info.st_mode):
                    try:
                        fd, opened_info = _open_regular_at(
                            directory_fd,
                            (entry.name,),
                            f"staging entry {child_relative}",
                        )
                        try:
                            if not _same_identity(info, opened_info):
                                raise DropError(
                                    f"staging entry changed before it was opened: {child_relative}"
                                )
                            digest, final_info = _sha256_fd(
                                fd, f"staging entry {child_relative}"
                            )
                        finally:
                            os.close(fd)
                    except DropError as exc:
                        reasons.append(str(exc))
                        continue
                    entries.append(
                        TreeEntry(
                            child_relative,
                            "file",
                            final_info.st_size,
                            _mode(final_info.st_mode),
                            digest,
                            *_listing_identity(final_info),
                        )
                    )
                    continue
                if stat.S_ISDIR(info.st_mode):
                    child_fd: int | None = None
                    try:
                        child_fd = _open_dir_at(directory_fd, entry.name)
                        child_info = os.fstat(child_fd)
                        if not _same_identity(info, child_info, content=False):
                            raise DropError(
                                f"staging directory changed before it was opened: {child_relative}"
                            )
                    except (DropError, OSError) as exc:
                        reasons.append(str(exc))
                        if child_fd is not None:
                            try:
                                os.close(child_fd)
                            except OSError:
                                pass
                        continue
                    entries.append(
                        TreeEntry(
                            child_relative,
                            "directory",
                            0,
                            _mode(child_info.st_mode),
                            None,
                            *_listing_identity(child_info),
                        )
                    )
                    try:
                        assert child_fd is not None
                        visit(child_fd, child_relative)
                    finally:
                        os.close(child_fd)
                    continue
                reasons.append(f"unsupported staging entry refused: {child_relative}")
        finally:
            pass

    visit(root_fd, ".")
    return tuple(entries)


def _listing_digest(entries: Iterable[TreeEntry]) -> str:
    return _sha256_bytes(_canonical_json([entry.as_dict() for entry in entries]))


def _manifest_mode(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = int(value, 8) if value.startswith("0") else int(value)
        except ValueError:
            return None
    else:
        return None
    return parsed if 0 <= parsed <= 0o7777 else None


def _verify_evidence(
    worker: Path, reasons: list[str], worker_fd: int | None = None
) -> EvidenceSnapshot | None:
    owned_worker_fd = worker_fd is None
    if worker_fd is None:
        try:
            worker_fd = _open_dir(worker)
        except DropError as exc:
            reasons.append(str(exc))
            return None
    assert worker_fd is not None
    try:
        try:
            evidence_fd = _open_dir_at(worker_fd, "evidence")
        except DropError as exc:
            reasons.append(f"evidence directory is not a real directory: {exc}")
            return None
        try:
            try:
                manifest_fd, manifest_info = _open_regular_at(
                    evidence_fd, ("manifest.json",), "evidence manifest"
                )
                try:
                    manifest_data, manifest_after = _read_fd(
                        manifest_fd, "evidence manifest"
                    )
                finally:
                    os.close(manifest_fd)
            except DropError as exc:
                reasons.append(
                    f"evidence/manifest.json is missing, symlinked, or not a regular file: {exc}"
                )
                return None
            if not _same_identity(manifest_info, manifest_after):
                reasons.append("evidence manifest changed while it was read")
                return None
            try:
                payload = json.loads(manifest_data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                reasons.append(f"evidence manifest is unreadable or invalid: {exc}")
                return None
            if not isinstance(payload, dict) or payload.get("schema_version") != 1:
                reasons.append(
                    "evidence manifest must be an object with schema_version=1"
                )
                return None
            rows = payload.get("files")
            if not isinstance(rows, list) or not rows:
                reasons.append("evidence manifest files must be a non-empty list")
                return None
            verified: list[dict[str, Any]] = []
            seen: set[str] = set()
            for index, row in enumerate(rows):
                if not isinstance(row, dict):
                    reasons.append(f"evidence manifest row {index} is not an object")
                    continue
                relative_value = row.get("path")
                if not isinstance(relative_value, str):
                    reasons.append(
                        f"evidence manifest row {index} has no relative path"
                    )
                    continue
                parts, path_reasons = _relative_parts(
                    relative_value, label=f"evidence path {relative_value!r}"
                )
                reasons.extend(path_reasons)
                if not parts:
                    continue
                normalized = "/".join(parts)
                if normalized in seen:
                    reasons.append(f"evidence manifest repeats path: {normalized}")
                    continue
                seen.add(normalized)
                if normalized == "manifest.json":
                    reasons.append("evidence manifest cannot list itself")
                    continue
                expected_hash = row.get("sha256")
                expected_mode = _manifest_mode(row.get("mode"))
                if not isinstance(expected_hash, str) or len(expected_hash) != 64:
                    reasons.append(
                        f"evidence manifest has invalid sha256 for {normalized}"
                    )
                    continue
                try:
                    int(expected_hash, 16)
                except ValueError:
                    reasons.append(
                        f"evidence manifest has invalid sha256 for {normalized}"
                    )
                    continue
                if expected_mode is None:
                    reasons.append(
                        f"evidence manifest has invalid mode for {normalized}"
                    )
                    continue
                try:
                    file_fd, _ = _open_regular_at(
                        evidence_fd, parts, f"manifest evidence file {normalized}"
                    )
                    try:
                        actual_hash, after = _sha256_fd(
                            file_fd, f"manifest evidence file {normalized}"
                        )
                    finally:
                        os.close(file_fd)
                except DropError as exc:
                    reasons.append(
                        f"manifest evidence file is missing, symlinked, or unsafe: {normalized}: {exc}"
                    )
                    continue
                actual_mode = _mode(after.st_mode)
                if actual_hash != expected_hash:
                    reasons.append(f"evidence hash mismatch: {normalized}")
                if actual_mode != expected_mode:
                    reasons.append(f"evidence mode mismatch: {normalized}")
                verified.append(
                    {
                        "path": normalized,
                        "sha256": expected_hash,
                        "mode": expected_mode,
                        "identity": {
                            "device": after.st_dev,
                            "inode": after.st_ino,
                            "uid": after.st_uid,
                            "gid": after.st_gid,
                        },
                    }
                )
            if reasons:
                return None
            manifest_digest = _sha256_bytes(manifest_data)
            return EvidenceSnapshot(
                worker / MANIFEST_RELATIVE,
                tuple(verified),
                manifest_digest,
                _identity(manifest_after),
            )
        finally:
            os.close(evidence_fd)
    finally:
        if owned_worker_fd:
            os.close(worker_fd)


def preflight(
    workers_root: Path, worker_name: str, relative_target: str
) -> tuple[Preflight | None, list[str]]:
    reasons: list[str] = []
    if not _worker_root_ok(workers_root, reasons):
        return None, reasons
    try:
        orchestration_info = workers_root.parent.lstat()
    except OSError as exc:
        reasons.append(f"orchestration root cannot be inspected: {exc.strerror or exc}")
        return None, reasons
    if stat.S_ISLNK(orchestration_info.st_mode) or not stat.S_ISDIR(
        orchestration_info.st_mode
    ):
        reasons.append("orchestration root is not a real directory")
        return None, reasons
    worker_parts, worker_reasons = _relative_parts(worker_name, label="worker")
    target_parts, target_reasons = _relative_parts(relative_target, label="target")
    reasons.extend(worker_reasons)
    reasons.extend(target_reasons)
    if len(worker_parts) != 1:
        reasons.append("worker must name exactly one worker record, not a path")
    if reasons:
        return None, reasons
    worker = workers_root / worker_parts[0]
    target = worker.joinpath(*target_parts)
    root_fd: int | None = None
    worker_fd: int | None = None
    try:
        root_fd = _open_dir(workers_root)
        worker_fd = _open_dir_at(root_fd, worker_parts[0])
        root_open_info = os.fstat(root_fd)
        worker_info = os.fstat(worker_fd)
    except (DropError, OSError) as exc:
        if worker_fd is not None:
            os.close(worker_fd)
        if root_fd is not None:
            os.close(root_fd)
        reasons.append(f"worker record does not exist or is unsafe: {exc}")
        return None, reasons
    assert root_fd is not None and worker_fd is not None
    if not stat.S_ISDIR(worker_info.st_mode):
        reasons.append("worker record is not a real directory")
        os.close(worker_fd)
        os.close(root_fd)
        return None, reasons
    _check_no_symlink_components(worker, workers_root, reasons)
    _check_no_symlink_components(target, worker, reasons)
    if target == worker:
        reasons.append("target cannot be the worker root")
    evidence = worker / "evidence"
    try:
        target.relative_to(worker)
    except ValueError:
        reasons.append("target is outside the worker record")
    try:
        target.relative_to(evidence)
        reasons.append("target overlaps the protected evidence directory")
    except ValueError:
        pass
    if target == evidence:
        reasons.append("target cannot be the evidence directory")
    try:
        target_info = target.lstat()
    except FileNotFoundError:
        reasons.append(f"staging target does not exist: {relative_target}")
        target_info = None
    except OSError as exc:
        reasons.append(f"staging target cannot be inspected: {exc.strerror or exc}")
        target_info = None
    if target_info is not None:
        if stat.S_ISLNK(target_info.st_mode):
            reasons.append("staging target is a symlink")
        elif not stat.S_ISDIR(target_info.st_mode):
            reasons.append("staging target is not a directory")
        else:
            expected_real = os.path.normpath(str(target.absolute()))
            if os.path.realpath(target) != expected_real:
                reasons.append("staging target realpath changed or contains a symlink")
    for marker in _marker_names(worker):
        reasons.append(f"worker has protected marker: {marker}")
    if (worker / "running").exists() or (worker / "running").is_symlink():
        reasons.append("worker is running: running marker exists")
    ended = worker / "ended"
    if not _regular_file(ended, "ended marker"):
        reasons.append("worker has not ended: ended marker is missing or unsafe")
    reasons.extend(_protected_ancestor_reasons_fd(worker_fd, target_parts))
    reasons.extend(_active_lease_reasons(workers_root, worker_parts[0]))
    manifest_snapshot = _verify_evidence(worker, reasons, worker_fd)
    entries: tuple[TreeEntry, ...] = ()
    target_identity: tuple[int, ...] = ()
    if (
        target_info is not None
        and stat.S_ISDIR(target_info.st_mode)
        and not stat.S_ISLNK(target_info.st_mode)
    ):
        try:
            parent_fd, target_name, opened = _open_target_parent(
                worker_fd, target_parts
            )
            try:
                target_fd = _open_child_dir(parent_fd, target_name)
                try:
                    target_open_info = os.fstat(target_fd)
                    if not _same_identity(target_info, target_open_info, content=False):
                        reasons.append("staging target changed while it was opened")
                    target_identity = _identity(target_open_info, content=False)
                    entries = _safe_walk_fd(target_fd, reasons)
                finally:
                    os.close(target_fd)
            finally:
                for fd in reversed(opened):
                    os.close(fd)
        except (DropError, OSError) as exc:
            reasons.append(f"staging target cannot be securely opened: {exc}")
    archive = worker / f"{target.name}.tgz"
    try:
        archive_info = os.stat(archive.name, dir_fd=worker_fd, follow_symlinks=False)
    except FileNotFoundError:
        archive_info = None
    except OSError as exc:
        reasons.append(f"archive collision cannot be inspected: {exc.strerror or exc}")
        archive_info = None
    if archive_info is not None:
        reasons.append(f"archive collision exists: {archive.name}")
    if target.name == DROP_LOG_NAME:
        reasons.append("target name is reserved for the durable action log")
    if manifest_snapshot is None:
        manifest_snapshot = EvidenceSnapshot(worker / MANIFEST_RELATIVE, (), "", ())
    if reasons:
        os.close(worker_fd)
        os.close(root_fd)
        return None, reasons
    listing_sha256 = _listing_digest(entries)
    logical_bytes = sum(entry.size for entry in entries if entry.kind == "file")
    os.close(worker_fd)
    os.close(root_fd)
    return (
        Preflight(
            worker,
            target,
            target_parts,
            manifest_snapshot,
            entries,
            listing_sha256,
            logical_bytes,
            _identity(root_open_info, content=False),
            _identity(orchestration_info, content=False),
            _identity(worker_info, content=False),
            target_identity,
        ),
        [],
    )


def _open_dir(path: Path) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    try:
        return os.open(path, flags)
    except OSError as exc:
        raise DropError(
            f"could not securely open directory {path}: {exc.strerror or exc}"
        ) from exc


def _open_child_dir(parent_fd: int, name: str) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    try:
        return os.open(name, flags, dir_fd=parent_fd)
    except OSError as exc:
        raise DropError(
            f"could not securely open path component {name}: {exc.strerror or exc}"
        ) from exc


def _open_target_parent(
    worker_fd: int, parts: tuple[str, ...]
) -> tuple[int, str, list[int]]:
    if not parts:
        raise DropError("empty target path")
    current = worker_fd
    opened: list[int] = []
    try:
        for part in parts[:-1]:
            child = _open_child_dir(current, part)
            opened.append(child)
            current = child
        return current, parts[-1], opened
    except BaseException:
        for fd in reversed(opened):
            os.close(fd)
        raise


def _fsync_fd(fd: int) -> None:
    try:
        os.fsync(fd)
    except OSError as exc:
        raise DropError(f"could not durably sync fd: {exc.strerror or exc}") from exc


def _write_log(worker_fd: int, record: dict[str, Any]) -> None:
    line = _canonical_json(record) + b"\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(DROP_LOG_NAME, flags, 0o600, dir_fd=worker_fd)
    except OSError as exc:
        raise DropError(
            f"could not open durable action log: {exc.strerror or exc}"
        ) from exc
    try:
        written = 0
        while written < len(line):
            written += os.write(fd, line[written:])
        _fsync_fd(fd)
    finally:
        os.close(fd)
    _fsync_fd(worker_fd)


def _listing_from_fd(fd: int) -> tuple[tuple[TreeEntry, ...], list[str]]:
    reasons: list[str] = []
    return _safe_walk_fd(fd, reasons), reasons


def _unlink_tree_at(parent_fd: int, name: str) -> None:
    """Remove one already-quarantined tree without following links."""

    child_fd = _open_child_dir(parent_fd, name)
    try:
        entries = list(os.scandir(child_fd))
        for entry in entries:
            entry_info = entry.stat(follow_symlinks=False)
            if entry.name in MARKER_NAMES:
                raise DropError(
                    f"protected marker appeared in quarantined tree: {entry.name}"
                )
            if stat.S_ISLNK(entry_info.st_mode):
                raise DropError(
                    f"quarantined tree changed to contain a symlink: {entry.name}"
                )
            if stat.S_ISDIR(entry_info.st_mode):
                _unlink_tree_at(child_fd, entry.name)
            elif stat.S_ISREG(entry_info.st_mode):
                os.unlink(entry.name, dir_fd=child_fd)
            else:
                raise DropError(
                    f"quarantined tree contains unsupported entry: {entry.name}"
                )
        os.rmdir(name, dir_fd=parent_fd)
    finally:
        os.close(child_fd)


def _archive_tree(
    bundle: tarfile.TarFile,
    source_fd: int,
    target_name: str,
    expected: tuple[TreeEntry, ...],
) -> None:
    for entry in expected:
        archive_name = (
            target_name if entry.path == "." else f"{target_name}/{entry.path}"
        )
        info = tarfile.TarInfo(archive_name)
        info.mode = entry.mode
        info.mtime = 0
        if entry.kind == "directory":
            info.type = tarfile.DIRTYPE
            bundle.addfile(info)
            continue
        info.size = entry.size
        info.type = tarfile.REGTYPE
        parts = tuple(entry.path.split("/"))
        fd, current = _open_regular_at(source_fd, parts, f"archive source {entry.path}")
        try:
            if _listing_identity(current) != (entry.device, entry.inode):
                raise DropError(f"archive source identity changed: {entry.path}")
            with os.fdopen(os.dup(fd), "rb") as source:
                bundle.addfile(info, source)
        finally:
            os.close(fd)


def _archive_members_match_fd(
    archive_fd: int, target_name: str, expected: tuple[TreeEntry, ...]
) -> None:
    expected_by_name = {entry.path: entry for entry in expected}
    actual: dict[str, tuple[str, int, int, str | None]] = {}
    try:
        os.lseek(archive_fd, 0, os.SEEK_SET)
        with tarfile.open(
            fileobj=os.fdopen(os.dup(archive_fd), "rb"), mode="r:gz"
        ) as bundle:
            for member in bundle.getmembers():
                name = member.name
                if name == target_name:
                    relative = "."
                elif name.startswith(target_name + "/"):
                    relative = name[len(target_name) + 1 :]
                else:
                    raise DropError(f"archive contains an outside member: {name}")
                if relative in actual:
                    raise DropError(f"archive repeats member: {name}")
                if (
                    member.issym()
                    or member.islnk()
                    or not (member.isdir() or member.isreg())
                ):
                    raise DropError(f"archive contains an unsafe member: {name}")
                content_hash: str | None = None
                if member.isreg():
                    source = bundle.extractfile(member)
                    if source is None:
                        raise DropError(f"archive member cannot be read: {name}")
                    digest = hashlib.sha256()
                    while chunk := source.read(1024 * 1024):
                        digest.update(chunk)
                    content_hash = digest.hexdigest()
                kind = "directory" if member.isdir() else "file"
                actual[relative] = (kind, member.size, _mode(member.mode), content_hash)
    except (OSError, tarfile.TarError) as exc:
        raise DropError(f"archive verification failed: {exc}") from exc
    expected_map = {
        key: (value.kind, value.size, value.mode, value.sha256)
        for key, value in expected_by_name.items()
    }
    if actual != expected_map:
        raise DropError("archive verification differs from the source listing")


def _write_archive_fd(
    archive_fd: int, source_fd: int, target_name: str, expected: tuple[TreeEntry, ...]
) -> None:
    archive_stream = os.fdopen(os.dup(archive_fd), "w+b")
    try:
        with tarfile.open(fileobj=archive_stream, mode="w:gz") as bundle:
            _archive_tree(bundle, source_fd, target_name, expected)
    finally:
        archive_stream.close()


def _archive_temp(
    worker_fd: int, target_name: str, source_fd: int, expected: tuple[TreeEntry, ...]
) -> tuple[str, str]:
    temp_name = f".{target_name}.tgz.partial-{secrets.token_hex(12)}"
    flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(temp_name, flags, 0o600, dir_fd=worker_fd)
    except OSError as exc:
        raise DropError(
            f"could not reserve archive temporary path: {exc.strerror or exc}"
        ) from exc
    try:
        with os.fdopen(fd, "w+b") as archive_file:
            _write_archive_fd(archive_file.fileno(), source_fd, target_name, expected)
            archive_file.flush()
            os.fsync(archive_file.fileno())
            archive_digest, _ = _sha256_fd(
                archive_file.fileno(), f"temporary archive {temp_name}"
            )
            _archive_members_match_fd(archive_file.fileno(), target_name, expected)
        try:
            os.link(
                temp_name,
                f"{target_name}.tgz",
                src_dir_fd=worker_fd,
                dst_dir_fd=worker_fd,
                follow_symlinks=False,
            )
        except OSError as exc:
            raise DropError(
                f"could not publish archive without overwrite: {exc.strerror or exc}"
            ) from exc
        return f"{target_name}.tgz", archive_digest
    except BaseException:
        try:
            os.unlink(temp_name, dir_fd=worker_fd)
        except FileNotFoundError:
            pass
        raise
    finally:
        try:
            os.unlink(temp_name, dir_fd=worker_fd)
        except FileNotFoundError:
            pass


def _disk_free(path: Path) -> int:
    try:
        return shutil.disk_usage(path).free
    except OSError as exc:
        raise DropError(
            f"could not determine free disk space: {exc.strerror or exc}"
        ) from exc


def execute(
    preflight_result: Preflight,
    *,
    pack_reserve_bytes: int = ARCHIVE_RESERVE_BYTES,
    disk_free: Callable[[Path], int] = _disk_free,
) -> dict[str, Any]:
    worker = preflight_result.worker
    orchestration_fd = _open_dir(worker.parent.parent)
    try:
        workers_root_fd = _open_child_dir(orchestration_fd, worker.parent.name)
    except BaseException:
        os.close(orchestration_fd)
        raise
    try:
        worker_fd = _open_child_dir(workers_root_fd, worker.name)
    except BaseException:
        os.close(workers_root_fd)
        os.close(orchestration_fd)
        raise
    opened_parent_fds: list[int] = []
    quarantine_name: str | None = None
    quarantine_fd: int | None = None
    parent_fd: int | None = None
    target_name: str | None = None
    try:
        if (
            _identity(os.fstat(orchestration_fd), content=False)
            != preflight_result.orchestration_identity
        ):
            raise DropError("orchestration root changed after preflight")
        if (
            _identity(os.fstat(workers_root_fd), content=False)
            != preflight_result.workers_root_identity
        ):
            raise DropError("workers root changed after preflight")
        if (
            _identity(os.fstat(worker_fd), content=False)
            != preflight_result.worker_identity
        ):
            raise DropError("worker record changed after preflight")
        try:
            fcntl.flock(worker_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise DropError(
                f"worker record is locked or active: {exc.strerror or exc}"
            ) from exc
        locked_reasons: list[str] = []
        try:
            for entry in os.scandir(worker_fd):
                if entry.name in MARKER_NAMES:
                    locked_reasons.append(f"worker has protected marker: {entry.name}")
        except OSError as exc:
            locked_reasons.append(
                f"cannot inspect worker markers: {exc.strerror or exc}"
            )
        try:
            running_info = os.stat("running", dir_fd=worker_fd, follow_symlinks=False)
            if running_info:
                locked_reasons.append("worker is running: running marker exists")
        except FileNotFoundError:
            pass
        except OSError as exc:
            locked_reasons.append(
                f"cannot inspect running marker: {exc.strerror or exc}"
            )
        try:
            ended_fd, _ = _open_regular_at(worker_fd, ("ended",), "ended marker")
            os.close(ended_fd)
        except DropError:
            locked_reasons.append(
                "worker has not ended: ended marker is missing or unsafe"
            )
        locked_reasons.extend(
            _protected_ancestor_reasons_fd(worker_fd, preflight_result.target_parts)
        )
        locked_reasons.extend(
            _active_lease_reasons_fd(orchestration_fd, worker.parent.name, worker.name)
        )
        if locked_reasons:
            raise DropError(
                "worker guard changed before action: " + "; ".join(locked_reasons)
            )
        parent_fd, target_name, opened_parent_fds = _open_target_parent(
            worker_fd, preflight_result.target_parts
        )
        target_fd = _open_child_dir(parent_fd, target_name)
        try:
            target_stat = os.fstat(target_fd)
            if (
                _identity(target_stat, content=False)
                != preflight_result.target_identity
            ):
                raise DropError("staging target changed before the guarded action")
            # The worker record and target are on the same filesystem because the
            # quarantine rename and archive hard-link both stay below worker.
            if target_stat.st_dev != os.fstat(worker_fd).st_dev:
                raise DropError("staging target is on a different filesystem")
            boundary_reasons = _protected_ancestor_reasons_fd(
                worker_fd, preflight_result.target_parts
            )
            if boundary_reasons:
                raise DropError(
                    "worker guard changed before quarantine: "
                    + "; ".join(boundary_reasons)
                )
            try:
                os.stat(f"{target_name}.tgz", dir_fd=worker_fd, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise DropError("archive collision appeared before the guarded action")
            quarantine_name = f".drop-staging-quarantine-{secrets.token_hex(12)}"
            os.rename(
                target_name, quarantine_name, src_dir_fd=parent_fd, dst_dir_fd=worker_fd
            )
        finally:
            os.close(target_fd)
        quarantine_fd = _open_child_dir(worker_fd, quarantine_name)
        current_entries, current_reasons = _listing_from_fd(quarantine_fd)
        if current_reasons or current_entries != preflight_result.listing:
            raise DropError("staging changed while entering the guarded action")
        evidence_reasons: list[str] = []
        evidence_now = _verify_evidence(worker, evidence_reasons, worker_fd)
        if (
            evidence_reasons
            or evidence_now is None
            or evidence_now != preflight_result.evidence
        ):
            raise DropError("evidence manifest changed before the guarded action")
        archive_need = preflight_result.logical_bytes + max(0, pack_reserve_bytes)
        free_bytes = disk_free(worker)
        if free_bytes >= archive_need:
            archive_name, archive_digest = _archive_temp(
                worker_fd, target_name, quarantine_fd, preflight_result.listing
            )
            final_entries, final_reasons = _listing_from_fd(quarantine_fd)
            if final_reasons or final_entries != preflight_result.listing:
                raise DropError("staging changed while the archive was created")
            final_evidence_reasons: list[str] = []
            final_evidence = _verify_evidence(worker, final_evidence_reasons, worker_fd)
            if (
                final_evidence_reasons
                or final_evidence is None
                or final_evidence != evidence_now
            ):
                raise DropError(
                    "evidence manifest changed while the archive was created"
                )
            log_record = {
                "action": "pack",
                "worker": worker.name,
                "target": "/".join(preflight_result.target_parts),
                "archive": archive_name,
                "archive_sha256": archive_digest,
                "evidence_verified": True,
                "evidence_manifest": str(MANIFEST_RELATIVE),
                "evidence_manifest_sha256": evidence_now.digest,
                "listing_sha256": preflight_result.listing_sha256,
                "original_bytes": preflight_result.logical_bytes,
            }
            _write_log(worker_fd, log_record)
            _unlink_tree_at(worker_fd, quarantine_name)
            quarantine_name = None
            _fsync_fd(worker_fd)
            return {"status": "packed", **log_record}
        fallback_entries, fallback_reasons = _listing_from_fd(quarantine_fd)
        if fallback_reasons or fallback_entries != preflight_result.listing:
            raise DropError("staging changed before low-disk fallback")
        fallback_evidence_reasons: list[str] = []
        fallback_evidence = _verify_evidence(
            worker, fallback_evidence_reasons, worker_fd
        )
        if (
            fallback_evidence_reasons
            or fallback_evidence is None
            or fallback_evidence != evidence_now
        ):
            raise DropError("evidence manifest changed before low-disk fallback")
        listing_record = {
            "action": "fallback",
            "worker": worker.name,
            "target": "/".join(preflight_result.target_parts),
            "reason": "insufficient free disk for archive",
            "free_bytes": free_bytes,
            "archive_required_bytes": archive_need,
            "evidence_manifest": str(MANIFEST_RELATIVE),
            "evidence_manifest_sha256": fallback_evidence.digest,
            "evidence_verified": True,
            "listing_sha256": preflight_result.listing_sha256,
            "original_bytes": preflight_result.logical_bytes,
        }
        _write_log(worker_fd, listing_record)
        _unlink_tree_at(worker_fd, quarantine_name)
        quarantine_name = None
        _fsync_fd(worker_fd)
        return {"status": "fallback", **listing_record}
    except BaseException:
        if quarantine_name is not None:
            try:
                quarantine_exists = os.stat(
                    quarantine_name, dir_fd=worker_fd, follow_symlinks=False
                )
            except FileNotFoundError:
                quarantine_exists = None
            if (
                quarantine_exists is not None
                and stat.S_ISDIR(quarantine_exists.st_mode)
                and parent_fd is not None
                and target_name is not None
            ):
                try:
                    os.rename(
                        quarantine_name,
                        target_name,
                        src_dir_fd=worker_fd,
                        dst_dir_fd=parent_fd,
                    )
                except OSError:
                    pass
        raise
    finally:
        if quarantine_fd is not None:
            os.close(quarantine_fd)
        for fd in reversed(opened_parent_fds):
            os.close(fd)
        os.close(worker_fd)
        os.close(workers_root_fd)
        os.close(orchestration_fd)


def _default_workers_root() -> Path:
    configured = os.environ.get("ORCH_WORKERS_ROOT")
    if configured:
        return Path(configured)
    # Installed form is ORCH/bin/drop-staging.  The private source form is
    # deliberately explicit in tests and does not guess at the live ORCH tree.
    return Path(__file__).resolve().parent.parent / "workers"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worker", help="one worker record name, not a path")
    parser.add_argument(
        "relative_path", help="regenerable staging path below that worker"
    )
    parser.add_argument(
        "--workers-root",
        type=Path,
        default=None,
        help="worker records root (kit default: ../workers)",
    )
    parser.add_argument(
        "--pack-reserve-bytes",
        type=int,
        default=ARCHIVE_RESERVE_BYTES,
        help="additional free bytes required for archive admission (default: 1048576)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.pack_reserve_bytes < 0:
        print(
            json.dumps(
                {"status": "refused", "reasons": ["pack reserve cannot be negative"]}
            )
        )
        return EXIT_REFUSED
    workers_root = (args.workers_root or _default_workers_root()).absolute()
    result, reasons = preflight(workers_root, args.worker, args.relative_path)
    if reasons:
        print(
            json.dumps(
                {
                    "status": "refused",
                    "worker": args.worker,
                    "target": args.relative_path,
                    "reasons": reasons,
                },
                sort_keys=True,
            )
        )
        return EXIT_REFUSED
    try:
        assert result is not None
        outcome = execute(result, pack_reserve_bytes=args.pack_reserve_bytes)
    except DropError as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "worker": args.worker,
                    "target": args.relative_path,
                    "error": str(exc),
                },
                sort_keys=True,
            )
        )
        return EXIT_ERROR
    print(json.dumps(outcome, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
