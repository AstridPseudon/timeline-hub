"""Ancestry walks retain private views of already-authenticated history values."""
from __future__ import annotations

import copy
import sqlite3
import sys
from contextlib import closing

import pytest
import test_timeline_commit_port as port_tests
from test_timeline_commit_port import commit, request
from test_timeline_request_source_snapshot import port_for

from runtime_protocol import timeline_commit_store as store_module
from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import AuthorizationError, RuntimeErrorBase
from runtime_protocol.util import canonical_json

service = port_tests.service


def test_repeated_history_value_detaches_once_and_remains_private(service, monkeypatch, record_property):
    accepted = commit(service, request(service))
    publication = accepted["receipt"]["receipt_id"]
    store, _ = service._timeline_commits()
    expected = store.history_entry(service.test_project, "main", publication)
    expected_bytes = canonical_json(expected)
    port = port_for(service, [])
    original_copy = copy.deepcopy
    original_finite = validation.finite_json
    copies, validations = [], []

    def is_entry(value):
        return isinstance(value, dict) and value.get("publication_id") == publication and "receipt" in value

    def counted_copy(value, memo=None):
        if is_entry(value) and sys._getframe(1).f_code.co_filename in {
            store_module.__file__, validation.__file__,
        }:
            copies.append(len(canonical_json(value).encode()))
        return original_copy(value) if memo is None else original_copy(value, memo)

    def counted_finite(value):
        if is_entry(value):
            validations.append(len(canonical_json(value).encode()))
        return original_finite(value)

    monkeypatch.setattr(copy, "deepcopy", counted_copy)
    monkeypatch.setattr(validation, "finite_json", counted_finite)
    try:
        first = port.history_entry(publication)
        assert canonical_json(first) == expected_bytes
        first["receipt"]["result"]["canonical_document"]["parent_revision"]["payload"].clear()
        first["records"]["commands"].clear()
        second = port.history_entry(publication)
        assert canonical_json(second) == expected_bytes
        assert len(copies) == 1
        assert validations == []
    finally:
        port.close()
    with pytest.raises(AuthorizationError, match="closed"):
        port.history_entry(publication)
    next_port = port_for(service, [])
    try:
        assert canonical_json(next_port.history_entry(publication)) == expected_bytes
        assert len(copies) == 2
        assert validations == []
    finally:
        next_port.close()
    assert canonical_json(store.history_entry(service.test_project, "main", publication)) == expected_bytes
    record_property("history_snapshot_copies", len(copies))
    record_property("history_snapshot_bytes", sum(copies))


@pytest.mark.parametrize("writer", ["same-connection", "external"])
def test_history_snapshot_does_not_hide_changed_authority(service, writer):
    accepted = commit(service, request(service))
    publication = accepted["receipt"]["receipt_id"]
    port = port_for(service, [])
    try:
        port.history_entry(publication)
        query = "UPDATE timeline_commit_history SET publisher='forged' WHERE publication_id=?"
        if writer == "external":
            with closing(sqlite3.connect(service.store.db_path, isolation_level=None)) as connection:
                connection.execute(query, (publication,))
        else:
            service.store.conn.execute(query, (publication,))
        with pytest.raises(RuntimeErrorBase):
            port.history_entry(publication)
    finally:
        port.close()


def test_history_snapshot_rechecks_authorization(service):
    accepted = commit(service, request(service))
    publication = accepted["receipt"]["receipt_id"]
    allowed = True

    def authorize():
        if not allowed:
            raise AuthorizationError("revoked")

    port = port_for(service, [], authorize)
    try:
        expected = port.history_entry(publication)
        allowed = False
        with pytest.raises(AuthorizationError, match="revoked"):
            port.history_entry(publication)
        allowed = True
        assert port.history_entry(publication) == expected
    finally:
        port.close()


def test_history_snapshot_replacement_still_fully_verifies(service, monkeypatch):
    accepted = commit(service, request(service))
    publication = accepted["receipt"]["receipt_id"]
    store, _ = service._timeline_commits()
    port = port_for(service, [])
    previous_connection = service.store.conn
    verify = store._verify_accepted_record
    verified = []

    def counted(row, edge, **kwargs):
        verified.append(edge["publication_id"])
        return verify(row, edge, **kwargs)

    monkeypatch.setattr(store, "_verify_accepted_record", counted)
    try:
        expected = port.history_entry(publication)
        assert verified == []
        service.store.conn = sqlite3.connect(service.store.db_path, isolation_level=None)
        assert port.history_entry(publication) == expected
        assert verified == [publication]
        service.store.conn.execute("UPDATE timeline_commit_history SET publisher='forged' WHERE publication_id=?",
                                   (publication,))
        with pytest.raises(RuntimeErrorBase):
            port.history_entry(publication)
    finally:
        port.close()
        previous_connection.close()
