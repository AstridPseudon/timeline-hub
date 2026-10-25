"""Ancestry traversal borrows authenticated entries until the port detaches them."""
from __future__ import annotations

import copy
from collections import Counter

import pytest
import test_timeline_commit_authentication as auth
from test_timeline_commit_port import commit, rows

from runtime_protocol import timeline_commit_store as store_module
from runtime_protocol.errors import AuthorizationError, RuntimeErrorBase

service = auth.service


def test_repeated_ancestry_does_not_detach_internal_entries(service, monkeypatch):
    auth.provider(service)
    accepted = commit(service, auth.body(service))
    commits, _ = service._timeline_commits()
    publication = accepted["receipt"]["receipt_id"]
    expected = commits.history_entry(service.test_project, "main", publication)
    before = rows(service)
    copies = Counter()
    original = store_module.detached

    def counted(value):
        if isinstance(value, dict) and value.get("publication_id") == publication and "receipt" in value:
            copies[publication] += 1
        return original(value)

    monkeypatch.setattr(store_module, "detached", counted)
    ports = []

    def execute(context, port):
        ports.append(port)
        for _ in range(3):
            entry = port.history_entry(publication)
            assert entry == expected
            entry["receipt"]["result"]["canonical_document"]["parent_revision"]["payload"].clear()
            entry["records"]["steps"].clear()
            page = port.history(port.head())
            assert page["items"][-1] == expected
            page["items"][-1]["records"]["commands"].clear()
        raise AuthorizationError("end read-only provider")

    service.test_provider.action = execute
    for number in range(2):
        with pytest.raises(AuthorizationError, match="end read-only provider"):
            commit(service, auth.body(service), key=f"read-only-{number}")
        assert copies == {}, "internal ancestry reads copied the same authenticated entry again"
        with pytest.raises(AuthorizationError, match="closed"):
            ports[-1].history_entry(publication)
        assert rows(service) == before
        # Public store readers still receive their own independently mutable value.
        actual = commits.history_entry(service.test_project, "main", publication)
        assert actual == expected
        actual["records"]["steps"].clear()
        copies.clear()


def test_ancestry_view_rechecks_authorization_and_live_history(service):
    auth.provider(service)
    accepted = commit(service, auth.body(service))
    publication = accepted["receipt"]["receipt_id"]
    checks = []
    revoked = []

    def authorize():
        checks.append(True)
        if revoked:
            raise AuthorizationError("revoked")

    def execute(context, port):
        expected = copy.deepcopy(port.history_entry(publication))
        prior = len(checks)
        revoked.append(True)
        with pytest.raises(AuthorizationError, match="revoked"):
            port.history_entry(publication)
        assert len(checks) > prior
        revoked.clear()
        assert port.history_entry(publication) == expected
        service.store.conn.execute(
            "UPDATE timeline_commit_history SET records_json='{}' WHERE publication_id=?", (publication,))
        with pytest.raises(RuntimeErrorBase):
            port.history_entry(publication)
        raise AuthorizationError("end tamper control")

    service.test_provider.action = execute
    with pytest.raises(AuthorizationError, match="end tamper control"):
        commit(service, auth.body(service), key="live-history", authorize=authorize)
