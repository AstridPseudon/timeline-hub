from __future__ import annotations

import fcntl
import hashlib
from pathlib import Path
import sqlite3

import pytest

from banodoco_local.bootstrap import BootstrapConfig, SourceProfile
from banodoco_local.paths import RuntimePaths
from banodoco_local.workspace_adopt import WorkspaceAdoptError, adopt_workspace
from runtime_protocol.store import RealmStore
from runtime_protocol.upgrade import inspect_canonical_schema
from runtime_protocol.store import SCHEMA_VERSION


class _Boundary:
    def inspect(self, *, realm_root):
        return RealmStore.inspect_realm(realm_root)


def _setup(tmp_path):
    root = tmp_path / "old" / "runtime" / "realms" / "film"
    RealmStore.initialize(root, realm_id="film").close()
    connection = sqlite3.connect(root / "realm.sqlite3")
    try:
        # A fresh realm is the current schema; walk it back to a genuine v26 layout:
        # v28 -> v27 (inline specs, no task_specs) then v27 -> v26 (no user_preferences).
        connection.execute("PRAGMA foreign_keys=OFF")
        connection.execute("DROP INDEX IF EXISTS idx_tasks_retention")
        for table in ("runs", "tasks"):
            connection.execute(f"ALTER TABLE {table} ADD COLUMN spec_json TEXT")
            connection.execute(f"ALTER TABLE {table} DROP COLUMN spec_digest")
        connection.execute("DROP TABLE task_specs")
        connection.execute("DROP TABLE user_preferences")
        connection.execute("UPDATE runtime_schema SET version=26 WHERE id=1")
        connection.commit()
    finally:
        connection.close()
    (root / "cas" / "sha256" / "aa").mkdir(parents=True)
    (root / "cas" / "sha256" / "aa" / "sample").write_bytes(b"sample-media")
    paths = RuntimePaths.current_mac(data_root=tmp_path / "new")
    profile = SourceProfile("astrid", str(tmp_path), str(tmp_path))
    config = BootstrapConfig(source_profile=profile)
    return root, paths, config


def _fingerprints(root):
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


def _adopt(root, paths, config, monkeypatch):
    monkeypatch.setattr("banodoco_local.workspace_adopt.bootstrap", lambda *_: object())
    monkeypatch.setattr("banodoco_local.workspace_adopt._verify_running", lambda *_: {"health": True})
    return adopt_workspace(paths, _Boundary(), config, source=root.parent.parent.parent, realm_id="film")


def test_adopts_v26_without_modifying_source(tmp_path, monkeypatch):
    root, paths, config = _setup(tmp_path)
    before = _fingerprints(root)
    result = _adopt(root, paths, config, monkeypatch)
    assert result["source_version"] == 26
    assert result["target_version"] == SCHEMA_VERSION
    assert inspect_canonical_schema(paths.realms_dir / "film")["version"] == SCHEMA_VERSION
    assert _fingerprints(root) == before
    assert result["bytes_cloned"] + result["bytes_copied"] >= (root / "realm.sqlite3").stat().st_size


def test_refuses_live_source_with_stop_instruction(tmp_path, monkeypatch):
    root, paths, config = _setup(tmp_path)
    with (root / "owner.lock").open("r+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(WorkspaceAdoptError, match="stop the old runtime first"):
            _adopt(root, paths, config, monkeypatch)
    assert not (paths.realms_dir / "film").exists()


def test_copy_fallback_and_interrupted_retry(tmp_path, monkeypatch):
    root, paths, config = _setup(tmp_path)
    monkeypatch.setattr("runtime_protocol.fsclone.clone_file", lambda *_: False)
    monkeypatch.setattr("banodoco_local.workspace_adopt.clone_file", lambda *_: False)
    from banodoco_local import workspace_adopt
    original = workspace_adopt._materialize
    calls = 0
    def fail_once(*args):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("interrupted")
        return original(*args)
    monkeypatch.setattr(workspace_adopt, "_materialize", fail_once)
    with pytest.raises(RuntimeError, match="interrupted"):
        _adopt(root, paths, config, monkeypatch)
    assert not (paths.realms_dir / "film").exists()
    result = _adopt(root, paths, config, monkeypatch)
    assert result["bytes_cloned"] == 0
    assert result["bytes_copied"] > 0
    assert inspect_canonical_schema(paths.realms_dir / "film")["version"] == SCHEMA_VERSION


def test_retries_launch_after_published_attach(tmp_path, monkeypatch):
    root, paths, config = _setup(tmp_path)
    monkeypatch.setattr("banodoco_local.workspace_adopt.bootstrap", lambda *_: (_ for _ in ()).throw(RuntimeError("launch failed")))
    with pytest.raises(WorkspaceAdoptError, match="finish with banodoco-local up"):
        adopt_workspace(paths, _Boundary(), config, source=root, realm_id="film")
    assert (paths.realms_dir / "film").is_dir()
    monkeypatch.setattr("banodoco_local.workspace_adopt.bootstrap", lambda *_: object())
    monkeypatch.setattr("banodoco_local.workspace_adopt._verify_running", lambda *_: {"health": True})
    result = adopt_workspace(paths, _Boundary(), config, source=root, realm_id="film")
    assert result["ok"]
    assert result["target_version"] == SCHEMA_VERSION


def test_mirror_directories_keeps_empty_storage_roots_and_modes(tmp_path):
    # Real realms have an empty staging/ and 0700 storage roots; admission
    # refuses a realm without them ("realm storage roots are incomplete").
    from banodoco_local.workspace_adopt import _mirror_directories

    source = tmp_path / "source"
    for relative in ("cas/sha256/ab", "staging", "presentations"):
        (source / relative).mkdir(parents=True)
    for relative in ("cas", "cas/sha256", "staging"):
        (source / relative).chmod(0o700)
    target = tmp_path / "target"
    target.mkdir()
    _mirror_directories(source, target)
    for relative in ("cas", "cas/sha256", "cas/sha256/ab", "staging", "presentations"):
        assert (target / relative).is_dir()
    assert (target / "staging").stat().st_mode & 0o777 == 0o700
    assert (target / "cas/sha256").stat().st_mode & 0o777 == 0o700


def test_completed_adoption_rerun_reuses_destination_without_clone_or_migration(tmp_path, monkeypatch):
    root, paths, config = _setup(tmp_path)
    before = _fingerprints(root)
    first = _adopt(root, paths, config, monkeypatch)
    destination = paths.realms_dir / "film"
    database = (destination / "realm.sqlite3").read_bytes()
    journal = paths.runtime_support / "adopt-journal.json"
    import json
    assert json.loads(journal.read_text())["state"] == "complete"
    def unexpected(*args, **kwargs):
        pytest.fail("completed adoption must not reclone or remigrate the destination")
    monkeypatch.setattr("banodoco_local.workspace_adopt._materialize", unexpected)
    monkeypatch.setattr("banodoco_local.workspace_adopt.migrate_canonical_to_current", unexpected)
    second = _adopt(root, paths, config, monkeypatch)
    assert second["destination"] == first["destination"]
    assert second["migration"] == first["migration"]
    assert (destination / "realm.sqlite3").read_bytes() == database
    assert _fingerprints(root) == before
    assert json.loads(journal.read_text())["state"] == "complete"
