"""D94 keeps only process-owned proofs behind a fresh storage boundary."""
from __future__ import annotations

import copy
import shutil
import sqlite3
from collections import Counter
from contextlib import closing

import pytest
import test_timeline_commit_integration as real
import test_timeline_commit_port as port_tests
import test_timeline_request_verification as verification_cases
from test_timeline_commit_authentication import body, provider
from test_timeline_commit_port import commit, rows

from runtime_protocol.errors import AuthorizationError, ProtocolError, RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_store import TimelineCommitStore

film = real.film
service = port_tests.service


def warm(service, monkeypatch):
    provider(service)
    accepted = commit(service, body(service))
    commits, _ = service._timeline_commits()
    publication = accepted["receipt"]["receipt_id"]
    commits.clear_replay_memo()
    calls = Counter()
    original = commits._verify_accepted_record

    def counted(row, edge, **kwargs):
        calls[edge["publication_id"]] += 1
        return original(row, edge, **kwargs)

    monkeypatch.setattr(commits, "_verify_accepted_record", counted)
    entry = commits.history_entry(service.test_project, "main", publication)
    assert calls == {publication: 1}
    return commits, publication, entry, calls


def test_warm_entries_and_closures_are_detached_and_only_new_entry_is_verified(service, monkeypatch):
    commits, publication, expected, calls = warm(service, monkeypatch)
    for _ in range(3):
        value = commits.history_entry(service.test_project, "main", publication)
        assert value == expected
        value["records"]["steps"].clear()
        document = commits.revision_closure(service.test_project, "main", expected["revision_id"])
        document["parent_revision"]["payload"].clear()
    next_body = body(service)
    change = next_body["commands"][0]["args"]["changes"][0]
    change["before"] = {"state": "present", "value": copy.deepcopy(change["value"])}
    change["value"] = {"org.example.timeline": {"note": "next"}}
    next_body["steps"][0]["patch"] = [copy.deepcopy(change)]
    accepted = commit(service, next_body, key="next")
    assert calls == {publication: 1, accepted["receipt"]["receipt_id"]: 1}
    assert commits.history_entry(service.test_project, "main", publication) == expected
    assert calls == {publication: 1, accepted["receipt"]["receipt_id"]: 1}


@pytest.mark.parametrize("writer", ["same-connection", "external", "wal-checkpoint", "file-size"])
def test_nonaccept_change_forces_full_verification(service, monkeypatch, writer):
    commits, publication, expected, calls = warm(service, monkeypatch)
    version = commits._store_version()
    if writer == "same-connection":
        service.store.conn.execute("UPDATE timelines SET name=COALESCE(name, '') || ' changed'")
    elif writer == "external":
        assert service.store.conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        with closing(sqlite3.connect(service.store.db_path, isolation_level=None)) as connection:
            connection.execute("UPDATE timelines SET name=COALESCE(name, '') || ' changed'")
    elif writer == "wal-checkpoint":
        service.store.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
    else:
        with service.store.db_path.open("ab") as stream:
            stream.write(b"\0" * 4096)
    assert commits._store_version() != version
    assert commits.history_entry(service.test_project, "main", publication) == expected
    assert calls == {publication: 2}


@pytest.mark.parametrize("component", ["database", "wal"])
def test_replaced_sqlite_file_requires_reopen_instead_of_trusting_disconnected_inode(service, monkeypatch, tmp_path,
                                                                                   component):
    commits, publication, _, _ = warm(service, monkeypatch)
    target = service.store.db_path if component == "database" else service.store.db_path.with_name("realm.sqlite3-wal")
    replacement = tmp_path / "replacement.sqlite3"
    shutil.copyfile(target, replacement)
    replacement.replace(target)
    with pytest.raises(ProtocolError, match="reopen required"):
        commits.history_entry(service.test_project, "main", publication)
    assert not any(commits._history_state.values())


@pytest.mark.parametrize("writer", ["same-connection", "external"])
def test_change_after_warm_hit_is_refused_before_return(service, monkeypatch, writer):
    commits, publication, _, _ = warm(service, monkeypatch)
    original = commits._verify_accepted

    def changed(*args, **kwargs):
        result = original(*args, **kwargs)
        if writer == "external":
            with closing(sqlite3.connect(service.store.db_path, isolation_level=None)) as connection:
                connection.execute("UPDATE timelines SET name=COALESCE(name, '') || ' changed'")
        else:
            service.store.conn.execute("UPDATE timelines SET name=COALESCE(name, '') || ' changed'")
        return result

    monkeypatch.setattr(commits, "_verify_accepted", changed)
    with pytest.raises(ProtocolError, match="changed during verification"):
        commits.history_entry(service.test_project, "main", publication)
    assert not any(commits._history_state.values())


def test_retained_warm_forgery_is_also_rejected_after_an_external_write(service, monkeypatch):
    connection = service.store.conn
    original = verification_cases.accepted
    with closing(sqlite3.connect(service.store.db_path, isolation_level=None)) as writer:
        class ExternalMutations:
            def __getattr__(self, name):
                return getattr(connection, name)

            def execute(self, query, parameters=()):
                # Route only the unchanged retained witness's mutations through
                # the second real connection. Reads still use Runtime's handle.
                return (writer if query.startswith("UPDATE") else connection).execute(query, parameters)

        def accepted(*args, **kwargs):
            result = original(*args, **kwargs)
            service.store.conn = ExternalMutations()
            return result

        monkeypatch.setattr(verification_cases, "accepted", accepted)
        try:
            verification_cases.test_retained_rehashed_step_forgery_refuses_with_warm_memo(service, monkeypatch)
        finally:
            service.store.conn = connection


def test_refusal_discards_state_and_a_new_store_always_verifies_cold(service, monkeypatch):
    commits, publication, expected, calls = warm(service, monkeypatch)

    def refuse():
        raise AuthorizationError("refused")

    with pytest.raises(AuthorizationError):
        service.list_timeline_commits(service.test_project, "main", authorize=refuse)
    assert not any(commits._history_state.values())
    assert commits.history_entry(service.test_project, "main", publication) == expected
    assert calls == {publication: 2}
    reopened = TimelineCommitStore(service.store, validate_prepared=commits.validate_prepared,
                                   validate_event=commits.validate_event)
    verified = []
    original = reopened._verify_accepted_record

    def counted(*args, **kwargs):
        verified.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(reopened, "_verify_accepted_record", counted)
    assert reopened.history_entry(service.test_project, "main", publication) == expected
    assert verified == [True]


def test_rolled_back_accept_publishes_no_history_state(service, monkeypatch):
    commits, _, _, _ = warm(service, monkeypatch)
    next_body = body(service)
    change = next_body["commands"][0]["args"]["changes"][0]
    change["before"] = {"state": "present", "value": copy.deepcopy(change["value"])}
    next_body["steps"][0]["patch"] = [copy.deepcopy(change)]
    before = rows(service)
    original = commits._publish
    attempted = []

    def fail(*args, **kwargs):
        original(*args, **kwargs)
        attempted.append(True)
        raise ValueError("rollback after publish")

    monkeypatch.setattr(commits, "_publish", fail)
    with pytest.raises(RuntimeErrorBase):
        commit(service, next_body, key="rollback")
    assert rows(service) == before
    assert attempted == [True]
    assert not any(commits._history_state.values())


def test_integrity_diagnostics_keep_reporting_corrupt_rows(service, monkeypatch):
    commits, publication, _, _ = warm(service, monkeypatch)
    service.store.conn.execute("UPDATE command_idempotency SET event_ids_json='[]' WHERE txn_id=?", (publication,))
    before = rows(service)
    errors = commits.integrity_errors()
    assert any(error["id"] == publication for error in errors)
    assert rows(service) == before


@pytest.mark.parametrize("operation", ["lookup", "accept"])
def test_authorization_refusal_precedes_cached_object_reads(service, monkeypatch, operation):
    commits, _, _, _ = warm(service, monkeypatch)

    def refuse():
        raise AuthorizationError("refused")

    def unreadable():
        pytest.fail("cached CAS read before authorization")

    monkeypatch.setattr(commits, "_check_history_objects", unreadable)
    with pytest.raises(AuthorizationError):
        if operation == "lookup":
            commits.lookup({}, authorize=refuse)
        else:
            commits.accept({}, {}, authorize=refuse)


def test_cached_legacy_closure_still_checks_physical_cas_bytes(film):
    runtime = RuntimeService(film.fixture.duplicate_root)
    try:
        project, timeline = film.fixture.project_id, film.fixture.timeline_id
        commits, _ = runtime._timeline_commits()
        commits.install_verified_baseline(project, timeline, authorize=lambda: None)
        runtime.list_timeline_commits(project, timeline, authorize=lambda: None)
        pin = commits.head(project, timeline)
        document = commits.revision_closure(project, timeline, pin["revision_id"])
        media = document["dependency_manifest"]["media"][0]["media_id"].removeprefix("sha256:")
        assert media in commits._history_state["objects"]
        path = runtime.cas.path_for(media)
        original = path.read_bytes()
        path.write_bytes(bytes([original[0] ^ 1]) + original[1:])
        before = rows(runtime)
        with pytest.raises(RuntimeErrorBase):
            commits.revision_closure(project, timeline, pin["revision_id"])
        assert rows(runtime) == before
        assert not any(commits._history_state.values())
    finally:
        runtime.close()
