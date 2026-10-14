"""Adopt a stopped canonical realm into this installation without changing its source."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
import time
import uuid
from typing import Any

from .bootstrap import BootstrapConfig, BootstrapError, RuntimeBoundary, _bootstrap_mutex, _read_catalog, _validate_support_paths, bootstrap
from .io import atomic_write_json
from .paths import RuntimePaths
from .workspace import _opaque_realm_id, _root, configure_workspace
from .operator_upgrade import _verify_running
from runtime_protocol.errors import OwnerBusyError
from runtime_protocol.fsclone import clone_file, clone_or_copy_file
from runtime_protocol.store import SCHEMA_VERSION  # the current canonical schema, never a pinned number
from runtime_protocol.upgrade import _file_digest, _owner_fence, inspect_canonical_schema, migrate_canonical_to_current


class WorkspaceAdoptError(BootstrapError):
    """Adoption stopped before changing source or selecting an unsafe realm."""


def _source_root(source: str | Path, realm_id: str) -> Path:
    source = _root(source, must_exist=True)
    if (source / "realm.sqlite3").is_file():
        return source
    catalog_path = source / "runtime" / "catalog.json"
    if catalog_path.exists():
        catalog = _read_catalog(RuntimePaths.current_mac(data_root=source))
        selected = catalog.get("selected_realm_id")
        realms = catalog.get("realms", [])
        if selected != realm_id or len(realms) != 1:
            raise WorkspaceAdoptError("source data root does not select the requested realm")
        candidate = _root(realms[0]["data_root"], must_exist=True)
        if not candidate.is_relative_to(source):
            raise WorkspaceAdoptError("source realm must be inside the supplied data root")
        return candidate
    return _root(source / "runtime" / "realms" / realm_id, must_exist=True)


def _source_files(root: Path) -> list[tuple[Path, Path, int]]:
    """Freeze a symlink-free file inventory; reject device nodes and other surprises."""
    files: list[tuple[Path, Path, int]] = []
    def visit(directory: Path) -> None:
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                visit(path)
            elif stat.S_ISREG(mode):
                files.append((path, path.relative_to(root), entry.stat(follow_symlinks=False).st_size))
            else:
                raise WorkspaceAdoptError(f"source contains an unsafe filesystem entry: {path}")
    visit(root)
    if not any(relative == Path("realm.sqlite3") for _, relative, _ in files):
        raise WorkspaceAdoptError("source realm database is missing")
    if not any(relative == Path("owner.lock") for _, relative, _ in files):
        raise WorkspaceAdoptError("source owner.lock is missing; refusing to create a file in the source")
    return files


def _journal(path: Path, **fields: Any) -> None:
    previous: dict[str, Any] = {}
    if path.is_file() and not path.is_symlink():
        previous = json.loads(path.read_text(encoding="utf-8"))
    history = list(previous.get("history", []))
    history.append({"state": fields["state"], "at": time.time()})
    payload = {**previous, **fields, "history": history, "version": 1}
    if fields["state"] != "failed":
        payload.pop("error", None)
    atomic_write_json(path, payload)


def _mirror_directories(root: Path, temporary: Path) -> None:
    """Recreate the realm's directory tree with its modes, empty ones included.

    Admission requires storage roots such as cas/sha256 and staging/ to exist
    (and the Runtime keeps them 0700); copying only regular files would drop
    empty directories and widen modes.
    """
    for directory in sorted(path for path in root.rglob("*") if path.is_dir() and not path.is_symlink()):
        target = temporary / directory.relative_to(root)
        target.mkdir(parents=True, exist_ok=True)
        target.chmod(directory.stat().st_mode & 0o777)


def _materialize(root: Path, temporary: Path, files: list[tuple[Path, Path, int]]) -> dict[str, int]:
    counts = {"bytes_cloned": 0, "bytes_copied": 0}
    _mirror_directories(root, temporary)
    for source, relative, size in files:
        target = temporary / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        method = clone_or_copy_file(source, target)
        # A clone is identical by construction (the source is fenced, so it
        # can't change underneath); only a byte copy needs a content check.
        if method == "cloned":
            if target.stat().st_size != size:
                raise WorkspaceAdoptError(f"clone size mismatch: {relative}")
        elif _file_digest(source) != _file_digest(target):
            raise WorkspaceAdoptError(f"copy integrity mismatch: {relative}")
        counts["bytes_cloned" if method == "cloned" else "bytes_copied"] += size
    return counts


def _inspect_source_snapshot(root: Path, realm_id: str) -> dict[str, object]:
    """Inspect SQLite sidecars on a private copy; ordinary read-only SQLite may checkpoint the source WAL."""
    with tempfile.TemporaryDirectory(prefix="banodoco-adopt-inspect-") as scratch:
        snapshot = Path(scratch)
        for name in ("realm.sqlite3", "realm.sqlite3-wal", "realm.sqlite3-shm", "realm.sqlite3-journal"):
            candidate = root / name
            if candidate.exists() or candidate.is_symlink():
                if not stat.S_ISREG(candidate.lstat().st_mode):
                    raise WorkspaceAdoptError(f"source SQLite component is unsafe: {name}")
                clone_or_copy_file(candidate, snapshot / name)
        return inspect_canonical_schema(snapshot, expected_realm_id=realm_id)


def adopt_workspace(
    paths: RuntimePaths,
    boundary: RuntimeBoundary,
    config: BootstrapConfig,
    *,
    source: str | Path,
    realm_id: str,
) -> dict[str, Any]:
    """Clone, migrate, select, and start one stopped realm; reruns resume published work."""
    started = time.monotonic()
    realm_id = _opaque_realm_id(realm_id, generate=False)
    if realm_id in {".", ".."}:
        raise WorkspaceAdoptError("realm id cannot be a filesystem dot component")
    _validate_support_paths(paths)
    root = _source_root(source, realm_id)
    destination = paths.realms_dir / realm_id
    if root == destination or destination.is_relative_to(root) or root.is_relative_to(destination):
        raise WorkspaceAdoptError("source and destination realms must be separate")
    catalog = _read_catalog(paths)
    journal_path = paths.runtime_support / "adopt-journal.json"
    if journal_path.is_symlink():
        raise WorkspaceAdoptError("adoption journal must not be a symlink")
    prior = json.loads(journal_path.read_text(encoding="utf-8")) if journal_path.is_file() and not journal_path.is_symlink() else {}
    selected = catalog.get("realms", [])
    already_attached = bool(selected and len(selected) == 1 and catalog.get("selected_realm_id") == realm_id and selected[0].get("data_root") == str(destination))
    if (selected or catalog.get("selected_realm_id")) and not (already_attached and prior.get("source") == str(root) and prior.get("destination") == str(destination)):
        raise WorkspaceAdoptError("destination already has a workspace selection")
    resume = destination.exists()
    if resume and (prior.get("source") != str(root) or prior.get("destination") != str(destination) or prior.get("realm_id") != realm_id or prior.get("state") not in {"published", "attached", "started", "complete", "failed"}):
        raise WorkspaceAdoptError("destination realm already exists and is not a resumable adoption")
    if destination.is_symlink():
        raise WorkspaceAdoptError("destination realm must not be a symlink")
    try:
        with _owner_fence(root):
            _source_files(root)
            identity = _inspect_source_snapshot(root, realm_id)
    except OwnerBusyError as exc:
        raise WorkspaceAdoptError("source realm is live; stop the old runtime first: banodoco-local down --profile astrid") from exc
    paths.ensure_support_dirs()
    with _bootstrap_mutex(paths):
        if _read_catalog(paths).get("realms") and not already_attached:
            raise WorkspaceAdoptError("destination acquired a workspace selection during adoption")
        try:
            with _owner_fence(root):
                # Classification and inventory are repeated after the lock, so
                # a stopped source cannot be swapped between preflight and copy.
                files = _source_files(root)
                if not resume:
                    # Reclaim an unpublished tree before checking fallback space.
                    if prior.get("source") == str(root) and prior.get("destination") == str(destination) and prior.get("temporary"):
                        stale = Path(prior["temporary"])
                        if stale.parent == paths.realms_dir and stale.name.startswith(f".{realm_id}.adopt-") and stale.is_dir() and not stale.is_symlink():
                            shutil.rmtree(stale)
                    operation_id = uuid.uuid4().hex
                    probe = paths.realms_dir / f".adopt-probe-{operation_id}"
                    try:
                        clone_supported = clone_file(root / "realm.sqlite3", probe)
                    finally:
                        probe.unlink(missing_ok=True)
                    source_device = (root / "realm.sqlite3").stat().st_dev
                    if not clone_supported or any(source_file.stat().st_dev != source_device for source_file, _, _ in files):
                        required = sum(size for _, _, size in files) + 2 * (root / "realm.sqlite3").stat().st_size + 64 * 1024 * 1024
                        free = shutil.disk_usage(paths.realms_dir).free
                        if free < required:
                            raise WorkspaceAdoptError(f"byte-copy fallback needs {required} free bytes; only {free} available")
                identity = _inspect_source_snapshot(root, realm_id)
                if resume:
                    inspect_canonical_schema(destination, expected_realm_id=realm_id)
                    counts = dict(prior.get("counts") or {})
                    migration = prior.get("migration")
                else:
                    temporary = paths.realms_dir / f".{realm_id}.adopt-{operation_id}"
                    if destination.exists():
                        raise WorkspaceAdoptError("destination realm already exists")
                    _journal(journal_path, operation_id=operation_id, state="planned", source=str(root), destination=str(destination), realm_id=realm_id, source_version=identity["version"], temporary=str(temporary))
                    try:
                        temporary.mkdir(mode=0o700)
                        _journal(journal_path, state="copying")
                        counts = _materialize(root, temporary, files)
                        _journal(journal_path, state="copied", counts=counts)
                        migration = migrate_canonical_to_current(temporary, confirmation=f"MIGRATE CANONICAL {realm_id}", expected_realm_id=realm_id)
                        final = inspect_canonical_schema(temporary, expected_realm_id=realm_id)
                        if int(final["version"]) != SCHEMA_VERSION:
                            raise WorkspaceAdoptError(f"adopted realm did not reach canonical v{SCHEMA_VERSION} (got v{final['version']})")
                        _journal(journal_path, state="migrated", migration=migration)
                        os.rename(temporary, destination)
                        _journal(journal_path, state="published")
                    except Exception:
                        if temporary.is_dir() and not temporary.is_symlink():
                            shutil.rmtree(temporary)
                        if not destination.exists():
                            _journal(journal_path, state="failed")
                        raise
        except OwnerBusyError as exc:
            raise WorkspaceAdoptError("source realm is live; stop the old runtime first: banodoco-local down --profile astrid") from exc

    # Attach owns catalog writes; bootstrap owns runtime launch and verification.
    try:
        configure_workspace(paths, boundary, config, mode="attach", realm_root=destination, realm_id=realm_id)
        _journal(journal_path, state="attached")
        launch = bootstrap(paths, boundary, config)
        verification = _verify_running(paths, boundary, launch)
        _journal(journal_path, state="complete", verification=verification)
    except Exception as exc:
        _journal(journal_path, state="failed", error=str(exc))
        raise WorkspaceAdoptError(f"realm materialized at {destination}; finish with banodoco-local up after resolving: {exc}") from exc
    return {"ok": True, "source": str(root), "destination": str(destination), "realm_id": realm_id,
            "source_version": int(identity["version"]), "target_version": SCHEMA_VERSION, **counts,
            "elapsed_seconds": round(time.monotonic() - started, 3), "migration": migration, "verification": verification}


__all__ = ["WorkspaceAdoptError", "adopt_workspace"]
