"""Unresolved recovery boundaries retained as failing security regressions."""
from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest

from runtime_protocol.errors import RuntimeErrorBase
from test_timeline_history_state import service, warm


def test_unobserved_file_round_trip_cannot_adopt_detached_history(service, monkeypatch, tmp_path):
    commits, publication, _, _ = warm(service, monkeypatch)
    original = service.store.conn
    original.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
    path = service.store.db_path
    saved = []
    for index, component in enumerate((path, Path(str(path) + "-wal"), Path(str(path) + "-shm"))):
        if component.exists():
            backup = tmp_path / f"original-{index}"
            component.replace(backup)
            saved.append((component, backup))
    shutil.copyfile(saved[0][1], path)
    stale = sqlite3.connect(path, isolation_level=None)
    assert stale.execute("SELECT event_ids_json FROM command_idempotency WHERE txn_id=?",
                         (publication,)).fetchone()[0] != "[]"
    for component, backup in saved:
        backup.replace(component)
    original.execute("UPDATE command_idempotency SET event_ids_json='[]' WHERE txn_id=?", (publication,))
    assert original.execute("SELECT event_ids_json FROM command_idempotency WHERE txn_id=?",
                            (publication,)).fetchone()[0] == "[]"
    assert stale.execute("SELECT event_ids_json FROM command_idempotency WHERE txn_id=?",
                         (publication,)).fetchone()[0] != "[]"
    service.store.conn = stale
    try:
        with pytest.raises(RuntimeErrorBase):
            commits.history_entry(service.test_project, "main", publication)
        assert not any(commits._history_state.values())
    finally:
        service.store.conn = original
        commits._connection = original
        stale.close()


def test_initial_physical_recovery_preserves_mounted_authorizer(service, monkeypatch, tmp_path):
    commits, publication, _, _ = warm(service, monkeypatch)
    service.store.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
    restricted = sqlite3.connect(service.store.db_path, isolation_level=None)

    def deny_history(operation, table, *_):
        if operation == sqlite3.SQLITE_READ and table == "timeline_commit_history":
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK

    restricted.set_authorizer(deny_history)
    with pytest.raises(sqlite3.DatabaseError, match="prohibited"):
        restricted.execute("SELECT * FROM timeline_commit_history").fetchall()
    replacement = tmp_path / "replacement.sqlite3"
    shutil.copyfile(service.store.db_path, replacement)
    replacement.replace(service.store.db_path)
    service.store.conn = restricted
    try:
        with pytest.raises((RuntimeErrorBase, sqlite3.DatabaseError)):
            commits.history_entry(service.test_project, "main", publication)
        assert not any(commits._history_state.values())
    finally:
        restricted.close()
