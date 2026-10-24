"""D42: accepted row bytes do not contain every authenticated read input."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest
import test_timeline_commit_port as port_tests
from test_timeline_commit_authentication import body, provider
from test_timeline_commit_port import commit, rows

from runtime_protocol.errors import ProtocolError
from runtime_protocol.timeline_commit_execution import CommitOutcomeUnknown
from runtime_protocol.timeline_commit_validation import digest
from runtime_protocol.util import canonical_json

service = port_tests.service


def accepted_bytes(service, publication):
    conn = service.store.conn
    return canonical_json([
        dict(conn.execute("SELECT * FROM command_idempotency WHERE txn_id=?", (publication,)).fetchone()),
        dict(conn.execute("SELECT * FROM timeline_commit_history WHERE publication_id=?", (publication,)).fetchone()),
    ]).encode()


@pytest.mark.parametrize("read", ["history", "retry"])
@pytest.mark.parametrize("external", ["event_prefix", "project_sequence", "source"])
def test_warm_accepted_bytes_do_not_authorize_changed_external_inputs(service, read, external):
    provider(service)
    first = commit(service, body(service))
    submitted = body(service)
    change = submitted["commands"][0]["args"]["changes"][0]
    change["before"] = {"state": "present", "value": copy.deepcopy(change["value"])}
    change["value"] = {"org.example.timeline": {"note": "closing"}}
    submitted["steps"][0]["patch"] = [copy.deepcopy(change)]
    accepted = commit(service, submitted, key="second")
    publication = accepted["receipt"]["receipt_id"]
    commits, _ = service._timeline_commits()

    def reread():
        if read == "history":
            return commits.history_entry(service.test_project, "main", publication)
        return commit(service, submitted, key="second")

    reread()
    original = accepted_bytes(service, publication)
    original_hash = hashlib.sha256(original).digest()
    conn = service.store.conn
    if external == "event_prefix":
        # An earlier accepted event is outside both rows of the later publication.
        conn.execute("UPDATE timeline_events SET event_hash='tampered' WHERE id=?",
                     (first["receipt"]["event_ids"][-1],))
    elif external == "project_sequence":
        conn.execute("UPDATE project_sequences SET next_seq=? WHERE project_id=?",
                     (accepted["receipt"]["project_seq"][0], service.test_project))
    else:
        source = copy.deepcopy(first["data"]["canonical_document"])
        parent = source["parent_revision"]
        parent["payload"]["meta"]["org.example.timeline"]["note"] = "forgery"
        parent["content_digest"] = digest(parent["payload"])
        conn.execute("UPDATE parent_composition_revisions SET payload_json=?, content_digest=? WHERE id=?",
                     (canonical_json(parent["payload"]), parent["content_digest"], parent["revision_id"]))
        # A self-consistent closure is insufficient: replay must still bind it
        # to the accepted command's original input, including its observations.
        assert commits.revision_closure(service.test_project, "main", parent["revision_id"]) == source

    assert accepted_bytes(service, publication) == original
    assert hashlib.sha256(accepted_bytes(service, publication)).digest() == original_hash
    before = rows(service)
    for _ in range(2):
        error_type = ProtocolError if read == "history" else CommitOutcomeUnknown
        with pytest.raises(error_type) as error:
            reread()
        corruption = error.value if read == "history" else error.value.__cause__
        assert isinstance(corruption, ProtocolError)
        assert str(corruption) == "accepted commit record is corrupt"
        assert rows(service) == before


def test_single_byte_accepted_record_change_is_refused_after_warm_read(service, monkeypatch):
    provider(service)
    accepted = commit(service, body(service))
    publication = accepted["receipt"]["receipt_id"]
    commits, _ = service._timeline_commits()
    commits.history_entry(service.test_project, "main", publication)
    conn = service.store.conn
    original = conn.execute("SELECT records_json FROM timeline_commit_history WHERE publication_id=?",
                            (publication,)).fetchone()[0]
    records = json.loads(original)
    records["label"] = "Annotate Film"
    changed = canonical_json(records)
    assert len(changed.encode()) == len(original.encode())
    assert sum(a != b for a, b in zip(changed.encode(), original.encode())) == 1
    conn.execute("UPDATE timeline_commit_history SET records_json=? WHERE publication_id=?", (changed, publication))
    calls = []
    verify = commits._verify_accepted

    def counted(*args, **kwargs):
        calls.append(None)
        return verify(*args, **kwargs)

    monkeypatch.setattr(commits, "_verify_accepted", counted)
    before = rows(service)
    for _ in range(2):
        with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
            commits.history_entry(service.test_project, "main", publication)
        assert rows(service) == before
    assert len(calls) == 2
