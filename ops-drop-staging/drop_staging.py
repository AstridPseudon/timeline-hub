#!/usr/bin/env python3
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
from pathlib import Path
import secrets
import shutil
import stat
import sys
import tarfile
from dataclasses import dataclass
from typing import Any, Callable, Iterable


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


@dataclass(frozen=True)
class TreeEntry:
    path: str
    kind: str
    size: int
    mode: int
    sha256: str | None

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "path": self.path,
            "kind": self.kind,
            "size": self.size,
            "mode": self.mode,
        }
        if self.sha256 is not None:
            result["sha256"] = self.sha256
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


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise DropError(f"could not hash {path}: {exc.strerror or exc}") from exc
    return digest.hexdigest()


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
    if not stat.S_ISREG(info.st_mode):
        return False
    return True


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
            reasons.append(f"cannot inspect path component {current}: {exc.strerror or exc}")
            return
        if stat.S_ISLNK(info.st_mode):
            reasons.append(f"symlink path component refused: {current.relative_to(stop)}")


def _marker_names(worker: Path) -> list[str]:
    try:
        names = {entry.name for entry in worker.iterdir()}
    except OSError:
        return []
    return sorted(names & MARKER_NAMES)


def _active_lease_reasons(workers_root: Path, worker_name: str) -> list[str]:
    """Read only the operational lease/ACTIVE records that can name a worker."""

    reasons: list[str] = []
    orch = workers_root.parent
    managers = orch / "managers"
    if not managers.is_dir() or managers.is_symlink():
        return reasons
    try:
        manager_dirs = sorted(managers.iterdir())
    except OSError as exc:
        return [f"cannot inspect manager leases: {exc.strerror or exc}"]
    for manager in manager_dirs:
        if not manager.is_dir() or manager.is_symlink():
            continue
        notes = manager / "notes"
        if not notes.is_dir() or notes.is_symlink():
            continue
        try:
            candidates = sorted(notes.iterdir())
        except OSError as exc:
            reasons.append(f"cannot inspect manager leases: {exc.strerror or exc}")
            continue
        for candidate in candidates:
            if not candidate.is_file() or candidate.is_symlink():
                continue
            if not (candidate.name.endswith(".lease") or "ACTIVE" in candidate.name):
                continue
            try:
                content = candidate.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                reasons.append(f"cannot inspect lease {candidate}: {exc.strerror or exc}")
                continue
            if worker_name in content or worker_name in candidate.name:
                reasons.append(f"active lease/marker names worker: {candidate}")
    return reasons


def _safe_walk(root: Path, reasons: list[str]) -> tuple[TreeEntry, ...]:
    entries: list[TreeEntry] = []

    def visit(path: Path, relative: str) -> None:
        try:
            info = path.lstat()
        except OSError as exc:
            reasons.append(f"cannot inspect staging entry {relative}: {exc.strerror or exc}")
            return
        mode = _mode(info.st_mode)
        if stat.S_ISLNK(info.st_mode):
            reasons.append(f"symlink inside staging refused: {relative}")
            return
        if stat.S_ISREG(info.st_mode):
            entries.append(TreeEntry(relative, "file", info.st_size, mode, _sha256_file(path)))
            return
        if stat.S_ISDIR(info.st_mode):
            entries.append(TreeEntry(relative, "directory", 0, mode, None))
            try:
                children = sorted(path.iterdir(), key=lambda child: child.name)
            except OSError as exc:
                reasons.append(f"cannot enumerate staging entry {relative}: {exc.strerror or exc}")
                return
            for child in children:
                child_relative = child.name if relative == "." else f"{relative}/{child.name}"
                visit(child, child_relative)
            return
        reasons.append(f"unsupported staging entry refused: {relative}")

    visit(root, ".")
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


def _verify_evidence(worker: Path, reasons: list[str]) -> EvidenceSnapshot | None:
    evidence = worker / "evidence"
    manifest_path = evidence / "manifest.json"
    try:
        evidence_info = evidence.lstat()
    except FileNotFoundError:
        reasons.append("evidence directory is missing")
        return None
    except OSError as exc:
        reasons.append(f"evidence directory cannot be inspected: {exc.strerror or exc}")
        return None
    if stat.S_ISLNK(evidence_info.st_mode) or not stat.S_ISDIR(evidence_info.st_mode):
        reasons.append("evidence directory is not a real directory")
        return None
    _check_no_symlink_components(evidence, worker, reasons)
    if not _regular_file(manifest_path, "evidence manifest"):
        reasons.append("evidence/manifest.json is missing, symlinked, or not a regular file")
        return None
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        reasons.append(f"evidence manifest is unreadable or invalid: {exc}")
        return None
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        reasons.append("evidence manifest must be an object with schema_version=1")
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
            reasons.append(f"evidence manifest row {index} has no relative path")
            continue
        parts, path_reasons = _relative_parts(relative_value, label=f"evidence path {relative_value!r}")
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
            reasons.append(f"evidence manifest has invalid sha256 for {normalized}")
            continue
        try:
            int(expected_hash, 16)
        except ValueError:
            reasons.append(f"evidence manifest has invalid sha256 for {normalized}")
            continue
        if expected_mode is None:
            reasons.append(f"evidence manifest has invalid mode for {normalized}")
            continue
        path = evidence.joinpath(*parts)
        _check_no_symlink_components(path, evidence, reasons)
        try:
            info = path.lstat()
        except FileNotFoundError:
            reasons.append(f"manifest evidence file is missing: {normalized}")
            continue
        except OSError as exc:
            reasons.append(f"cannot inspect manifest evidence file {normalized}: {exc.strerror or exc}")
            continue
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            reasons.append(f"manifest evidence file is not a regular file: {normalized}")
            continue
        actual_hash = _sha256_file(path)
        actual_mode = _mode(info.st_mode)
        if actual_hash != expected_hash:
            reasons.append(f"evidence hash mismatch: {normalized}")
        if actual_mode != expected_mode:
            reasons.append(f"evidence mode mismatch: {normalized}")
        verified.append({"path": normalized, "sha256": expected_hash, "mode": expected_mode})
    if reasons:
        return None
    manifest_digest = _sha256_file(manifest_path)
    return EvidenceSnapshot(manifest_path, tuple(verified), manifest_digest)


def preflight(workers_root: Path, worker_name: str, relative_target: str) -> tuple[Preflight | None, list[str]]:
    reasons: list[str] = []
    if not _worker_root_ok(workers_root, reasons):
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
    try:
        worker_info = worker.lstat()
    except FileNotFoundError:
        reasons.append(f"worker record does not exist: {worker_parts[0]}")
        return None, reasons
    if stat.S_ISLNK(worker_info.st_mode) or not stat.S_ISDIR(worker_info.st_mode):
        reasons.append("worker record is not a real directory")
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
    reasons.extend(_active_lease_reasons(workers_root, worker_parts[0]))
    manifest_snapshot = _verify_evidence(worker, reasons)
    if target_info is not None and stat.S_ISDIR(target_info.st_mode) and not stat.S_ISLNK(target_info.st_mode):
        _safe_walk(target, reasons)
    for parent in (target, *target.parents):
        if parent == worker or parent == workers_root:
            break
        if (parent / "KEEP").exists() or (parent / "KEEP").is_symlink():
            reasons.append(f"KEEP protection applies to target ancestor: {parent.relative_to(worker)}")
    if target_info is not None and stat.S_ISDIR(target_info.st_mode):
        for entry in target.rglob("*"):
            if entry.name in MARKER_NAMES:
                reasons.append(f"protected marker inside staging: {entry.relative_to(target)}")
    archive = worker / f"{target.name}.tgz"
    try:
        archive_info = archive.lstat()
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
        manifest_snapshot = EvidenceSnapshot(worker / MANIFEST_RELATIVE, (), "")
    if reasons:
        return None, reasons
    entries = _safe_walk(target, [])
    listing_sha256 = _listing_digest(entries)
    logical_bytes = sum(entry.size for entry in entries if entry.kind == "file")
    return (
        Preflight(worker, target, target_parts, manifest_snapshot, entries, listing_sha256, logical_bytes),
        [],
    )


def _open_dir(path: Path) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    try:
        return os.open(path, flags)
    except OSError as exc:
        raise DropError(f"could not securely open directory {path}: {exc.strerror or exc}") from exc


def _open_child_dir(parent_fd: int, name: str) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    try:
        return os.open(name, flags, dir_fd=parent_fd)
    except OSError as exc:
        raise DropError(f"could not securely open path component {name}: {exc.strerror or exc}") from exc


def _open_target_parent(worker_fd: int, parts: tuple[str, ...]) -> tuple[int, str, list[int]]:
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


def _same_inode(left: os.stat_result, right: os.stat_result) -> bool:
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino and left.st_mode == right.st_mode


def _fsync_fd(fd: int) -> None:
    try:
        os.fsync(fd)
    except OSError as exc:
        raise DropError(f"could not durably sync fd: {exc.strerror or exc}") from exc


def _write_log(worker: Path, record: dict[str, Any]) -> None:
    path = worker / DROP_LOG_NAME
    try:
        info = path.lstat()
    except FileNotFoundError:
        info = None
    if info is not None and (stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode)):
        raise DropError("durable action log path is not a regular file")
    line = _canonical_json(record) + b"\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags, 0o600)
    except OSError as exc:
        raise DropError(f"could not open durable action log: {exc.strerror or exc}") from exc
    try:
        written = 0
        while written < len(line):
            written += os.write(fd, line[written:])
        _fsync_fd(fd)
    finally:
        os.close(fd)
    try:
        directory_fd = _open_dir(worker)
        try:
            _fsync_fd(directory_fd)
        finally:
            os.close(directory_fd)
    except DropError:
        raise


def _listing_from_path(path: Path) -> tuple[tuple[TreeEntry, ...], list[str]]:
    reasons: list[str] = []
    result = _safe_walk(path, reasons)
    return result, reasons


def _archive_members_match(archive: Path, target_name: str, expected: tuple[TreeEntry, ...]) -> None:
    expected_by_name = {entry.path: entry for entry in expected}
    actual: dict[str, tuple[str, int, int, str | None]] = {}
    try:
        with tarfile.open(archive, "r:gz") as bundle:
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
                if member.issym() or member.islnk() or not (member.isdir() or member.isreg()):
                    raise DropError(f"archive contains an unsafe member: {name}")
                content_hash: str | None = None
                if member.isreg():
                    source = bundle.extractfile(member)
                    if source is None:
                        raise DropError(f"archive member cannot be read: {name}")
                    digest = hashlib.sha256()
                    for chunk in iter(lambda: source.read(1024 * 1024), b""):
                        digest.update(chunk)
                    content_hash = digest.hexdigest()
                kind = "directory" if member.isdir() else "file"
                actual[relative] = (kind, member.size, _mode(member.mode), content_hash)
    except (OSError, tarfile.TarError) as exc:
        raise DropError(f"archive verification failed: {exc}") from exc
    expected_map = {key: (value.kind, value.size, value.mode, value.sha256) for key, value in expected_by_name.items()}
    if actual != expected_map:
        raise DropError("archive verification differs from the source listing")


def _unlink_tree_at(parent_fd: int, name: str) -> None:
    """Remove one already-quarantined tree without following links."""

    child_fd = _open_child_dir(parent_fd, name)
    try:
        entries = list(os.scandir(child_fd))
        for entry in entries:
            entry_info = entry.stat(follow_symlinks=False)
            if stat.S_ISLNK(entry_info.st_mode):
                raise DropError(f"quarantined tree changed to contain a symlink: {entry.name}")
            if stat.S_ISDIR(entry_info.st_mode):
                _unlink_tree_at(child_fd, entry.name)
            elif stat.S_ISREG(entry_info.st_mode):
                os.unlink(entry.name, dir_fd=child_fd)
            else:
                raise DropError(f"quarantined tree contains unsupported entry: {entry.name}")
        os.rmdir(name, dir_fd=parent_fd)
    finally:
        os.close(child_fd)


def _archive_temp(worker: Path, target_name: str, source: Path, expected: tuple[TreeEntry, ...]) -> tuple[Path, str]:
    temp_name = f".{target_name}.tgz.partial-{secrets.token_hex(12)}"
    temp_path = worker / temp_name
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(temp_path, flags, 0o600)
        os.close(fd)
    except OSError as exc:
        raise DropError(f"could not reserve archive temporary path: {exc.strerror or exc}") from exc
    try:
        with tarfile.open(temp_path, "w:gz", dereference=False) as bundle:
            bundle.add(source, arcname=target_name, recursive=True)
        archive_digest = _sha256_file(temp_path)
        _archive_members_match(temp_path, target_name, expected)
        with temp_path.open("rb") as source_file:
            os.fsync(source_file.fileno())
        final_path = worker / f"{target_name}.tgz"
        try:
            os.link(temp_path, final_path, follow_symlinks=False)
        except OSError as exc:
            raise DropError(f"could not publish archive without overwrite: {exc.strerror or exc}") from exc
        return final_path, archive_digest
    except BaseException:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass
        raise
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def _disk_free(path: Path) -> int:
    try:
        return shutil.disk_usage(path).free
    except OSError as exc:
        raise DropError(f"could not determine free disk space: {exc.strerror or exc}") from exc


def execute(
    preflight_result: Preflight,
    *,
    pack_reserve_bytes: int = ARCHIVE_RESERVE_BYTES,
    disk_free: Callable[[Path], int] = _disk_free,
) -> dict[str, Any]:
    worker = preflight_result.worker
    worker_fd = _open_dir(worker)
    opened_parent_fds: list[int] = []
    quarantine_name: str | None = None
    parent_fd: int | None = None
    target_name: str | None = None
    try:
        try:
            fcntl.flock(worker_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise DropError(f"worker record is locked or active: {exc.strerror or exc}") from exc
        locked_reasons: list[str] = []
        for marker in _marker_names(worker):
            locked_reasons.append(f"worker has protected marker: {marker}")
        if (worker / "running").exists() or (worker / "running").is_symlink():
            locked_reasons.append("worker is running: running marker exists")
        if not _regular_file(worker / "ended", "ended marker"):
            locked_reasons.append("worker has not ended: ended marker is missing or unsafe")
        locked_reasons.extend(_active_lease_reasons(worker.parent, worker.name))
        if locked_reasons:
            raise DropError("worker guard changed before action: " + "; ".join(locked_reasons))
        parent_fd, target_name, opened_parent_fds = _open_target_parent(worker_fd, preflight_result.target_parts)
        target_fd = _open_child_dir(parent_fd, target_name)
        try:
            target_stat = os.fstat(target_fd)
            current_stat = os.stat(target_name, dir_fd=parent_fd, follow_symlinks=False)
            if not _same_inode(target_stat, current_stat):
                raise DropError("staging target changed before the guarded action")
            # The worker record and target are on the same filesystem because the
            # quarantine rename and archive hard-link both stay below worker.
            if target_stat.st_dev != os.fstat(worker_fd).st_dev:
                raise DropError("staging target is on a different filesystem")
            archive_path = worker / f"{target_name}.tgz"
            if archive_path.exists() or archive_path.is_symlink():
                raise DropError("archive collision appeared before the guarded action")
            quarantine_name = f".drop-staging-quarantine-{secrets.token_hex(12)}"
            os.rename(target_name, quarantine_name, src_dir_fd=parent_fd, dst_dir_fd=worker_fd)
        finally:
            os.close(target_fd)
        quarantine = worker / quarantine_name
        current_entries, current_reasons = _listing_from_path(quarantine)
        if current_reasons or current_entries != preflight_result.listing:
            raise DropError("staging changed while entering the guarded action")
        evidence_reasons: list[str] = []
        evidence_now = _verify_evidence(worker, evidence_reasons)
        if evidence_reasons or evidence_now is None or evidence_now != preflight_result.evidence:
            raise DropError("evidence manifest changed before the guarded action")
        archive_need = preflight_result.logical_bytes + max(0, pack_reserve_bytes)
        free_bytes = disk_free(worker)
        if free_bytes >= archive_need:
            archive_path, archive_digest = _archive_temp(worker, target_name, quarantine, preflight_result.listing)
            final_entries, final_reasons = _listing_from_path(quarantine)
            if final_reasons or final_entries != preflight_result.listing:
                raise DropError("staging changed while the archive was created")
            final_evidence_reasons: list[str] = []
            final_evidence = _verify_evidence(worker, final_evidence_reasons)
            if final_evidence_reasons or final_evidence is None or final_evidence != evidence_now:
                raise DropError("evidence manifest changed while the archive was created")
            log_record = {
                "action": "pack",
                "worker": worker.name,
                "target": "/".join(preflight_result.target_parts),
                "archive": archive_path.name,
                "archive_sha256": archive_digest,
                "evidence_verified": True,
                "evidence_manifest": str(MANIFEST_RELATIVE),
                "evidence_manifest_sha256": evidence_now.digest,
                "listing_sha256": preflight_result.listing_sha256,
                "original_bytes": preflight_result.logical_bytes,
            }
            _write_log(worker, log_record)
            _unlink_tree_at(worker_fd, quarantine_name)
            quarantine_name = None
            _fsync_fd(worker_fd)
            return {"status": "packed", **log_record}
        fallback_entries, fallback_reasons = _listing_from_path(quarantine)
        if fallback_reasons or fallback_entries != preflight_result.listing:
            raise DropError("staging changed before low-disk fallback")
        fallback_evidence_reasons: list[str] = []
        fallback_evidence = _verify_evidence(worker, fallback_evidence_reasons)
        if fallback_evidence_reasons or fallback_evidence is None or fallback_evidence != evidence_now:
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
        _write_log(worker, listing_record)
        _unlink_tree_at(worker_fd, quarantine_name)
        quarantine_name = None
        _fsync_fd(worker_fd)
        return {"status": "fallback", **listing_record}
    except BaseException:
        if quarantine_name is not None:
            quarantine = worker / quarantine_name
            if quarantine.exists() and not quarantine.is_symlink() and parent_fd is not None and target_name is not None:
                try:
                    os.rename(quarantine_name, target_name, src_dir_fd=worker_fd, dst_dir_fd=parent_fd)
                except OSError:
                    pass
        raise
    finally:
        for fd in reversed(opened_parent_fds):
            os.close(fd)
        os.close(worker_fd)


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
    parser.add_argument("relative_path", help="regenerable staging path below that worker")
    parser.add_argument("--workers-root", type=Path, default=None, help="worker records root (kit default: ../workers)")
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
        print(json.dumps({"status": "refused", "reasons": ["pack reserve cannot be negative"]}))
        return EXIT_REFUSED
    workers_root = (args.workers_root or _default_workers_root()).absolute()
    result, reasons = preflight(workers_root, args.worker, args.relative_path)
    if reasons:
        print(json.dumps({"status": "refused", "worker": args.worker, "target": args.relative_path, "reasons": reasons}, sort_keys=True))
        return EXIT_REFUSED
    try:
        assert result is not None
        outcome = execute(result, pack_reserve_bytes=args.pack_reserve_bytes)
    except DropError as exc:
        print(json.dumps({"status": "error", "worker": args.worker, "target": args.relative_path, "error": str(exc)}, sort_keys=True))
        return EXIT_ERROR
    print(json.dumps(outcome, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
