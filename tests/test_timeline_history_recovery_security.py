"""Physical replacement boundaries must not authorize a disconnected history."""
from __future__ import annotations

import shutil
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from runtime_protocol.errors import ProtocolError, RuntimeErrorBase
from test_timeline_history_state import service, warm


@pytest.mark.parametrize("tamper", [False, True])
def test_wal_swap_after_canonical_reopen_fails_closed(service, monkeypatch, tmp_path, tamper):
    commits, publication, _, _ = warm(service, monkeypatch)
    stale = sqlite3.connect(service.store.db_path, isolation_level=None)
    database = tmp_path / "replacement.sqlite3"
    shutil.copyfile(service.store.db_path, database)
    database.replace(service.store.db_path)
    wal = Path(str(service.store.db_path) + "-wal")
    replacement = tmp_path / "replacement-wal"
    shutil.copyfile(wal, replacement)
    if tamper:
        with replacement.open("r+b") as stream:
            stream.seek(-1, 2)
            byte = stream.read(1)
            stream.seek(-1, 2)
            stream.write(bytes([byte[0] ^ 1]))
    service.store.conn = stale
    original_open = service.store._open

    def racing_open(*, fresh=False):
        original_open(fresh=fresh)
        replacement.replace(wal)

    monkeypatch.setattr(service.store, "_open", racing_open)
    try:
        with pytest.raises(ProtocolError, match="identity changed during reopen"):
            commits.history_entry(service.test_project, "main", publication)
        assert not any(commits._history_state.values())
    finally:
        stale.close()


@pytest.mark.parametrize("component", ["database", "wal"])
def test_replacement_during_handle_adoption_fails_closed(service, monkeypatch, tmp_path, component):
    commits, publication, _, _ = warm(service, monkeypatch)
    tracked = commits._connection
    current = sqlite3.connect(service.store.db_path, isolation_level=None)
    target = service.store.db_path if component == "database" else Path(str(service.store.db_path) + "-wal")
    replacement = tmp_path / "replacement"
    shutil.copyfile(target, replacement)
    original_check = commits._replacement_connection_is_current

    def racing_check(connection):
        original_check(connection)
        replacement.replace(target)

    service.store.conn = current
    monkeypatch.setattr(commits, "_replacement_connection_is_current", racing_check)
    try:
        with pytest.raises(ProtocolError, match="identity changed during"):
            commits.history_entry(service.test_project, "main", publication)
        assert not any(commits._history_state.values())
    finally:
        service.store.conn = tracked
        current.close()


def test_delayed_stale_handle_after_recovery_cannot_authorize_tampered_database(service, monkeypatch, tmp_path):
    commits, publication, expected, calls = warm(service, monkeypatch)
    service.store.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
    stale = sqlite3.connect(service.store.db_path, isolation_level=None)
    # Open the WAL too, so the delayed handle really retains the old files.
    stale.execute("SELECT COUNT(*) FROM command_idempotency").fetchone()
    replacement = tmp_path / "replacement.sqlite3"
    shutil.copyfile(service.store.db_path, replacement)
    replacement.replace(service.store.db_path)
    assert commits.history_entry(service.test_project, "main", publication) == expected
    assert calls == {publication: 2}
    with closing(sqlite3.connect(service.store.db_path, isolation_level=None)) as writer:
        writer.execute("UPDATE command_idempotency SET event_ids_json='[]' WHERE txn_id=?", (publication,))
    service.store.conn = stale
    try:
        with pytest.raises(RuntimeErrorBase):
            commits.history_entry(service.test_project, "main", publication)
        assert not any(commits._history_state.values())
        assert commits._connection is not stale
    finally:
        service.store.conn = commits._connection
        stale.close()


def test_canonical_recovery_allows_own_wal_creation(service, monkeypatch, tmp_path):
    commits, publication, expected, calls = warm(service, monkeypatch)
    # A valid checkpointed replacement need not bring a WAL with it.
    service.store.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
    replacement = tmp_path / "replacement.sqlite3"
    shutil.copyfile(service.store.db_path, replacement)
    service.store.conn.close()
    service.store.conn = None
    replacement.replace(service.store.db_path)
    service.store.conn = sqlite3.connect(service.store.db_path, isolation_level=None)
    assert not Path(str(service.store.db_path) + "-wal").exists()
    assert commits.history_entry(service.test_project, "main", publication) == expected
    assert calls == {publication: 2}
    assert commits.history_entry(service.test_project, "main", publication) == expected
    assert calls == {publication: 2}
