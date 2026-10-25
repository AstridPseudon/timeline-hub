"""Accept-time recorder verification and authenticated historical digest links."""
from __future__ import annotations

import json
from collections import Counter

import pytest
import test_timeline_commit_integration as real

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_validation import digest
from runtime_protocol.util import canonical_json

film = real.film
agent = real.agent
editing = real.editing
pytestmark = pytest.mark.integration


def note(editing, index):
    change = {"op": "set", "ref": "parent", "path": ["meta"],
              "before": {"state": "absent"}, "value": {"org.example.note": {"text": str(index)}}}
    if index:
        change.update(path=["meta", "org.example.note", "text"],
                      before={"state": "present", "value": str(index - 1)}, value=str(index))
    command = {"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
               "args": {"changes": [change]}}
    body = editing.body([command])
    body["steps"][0]["patch"] = [change]
    return body


def event(editing, result):
    return editing.service.store.conn.execute("SELECT * FROM timeline_events WHERE id=?",
                                              (result["receipt"]["event_ids"][-1],)).fetchone()


def test_accept_replays_once_and_read_retry_history_inverse_use_recorded_result(editing, monkeypatch):
    commits, _ = editing.service._timeline_commits()
    calls = Counter()
    replay = commits._verify_accepted_replay

    def counted(row, edge, *args):
        calls[edge["publication_id"]] += 1
        return replay(row, edge, *args)

    monkeypatch.setattr(commits, "_verify_accepted_replay", counted)
    body = note(editing, 0)
    first = editing.commit(body, "attested-first")
    publication = first["receipt"]["receipt_id"]
    assert calls == {publication: 1}
    payload = json.loads(event(editing, first)["payload_json"])
    verified = payload["verification"]
    assert verified["version"] == 1
    assert verified["facts"] == {"recorder_abi": 2, "step_records": True, "sequential_capture": False}
    assert set(verified) == {"version", "entry_digest", "previous_digest", "source_digest", "realm_id", "facts"}
    for _ in range(2):
        assert editing.commit(body, "attested-first") == first
        editing.assert_readback(first)
    assert calls == {publication: 1}
    undone = editing.commit(editing.body([real.inverse(publication)]), "attested-undo")
    assert calls == {publication: 1, undone["receipt"]["receipt_id"]: 1}
    assert commits.verify_history() == []
    assert calls[publication] > 1 and calls[undone["receipt"]["receipt_id"]] > 1


def test_genuine_legacy_mix_falls_back_to_full_replay(editing, monkeypatch):
    commits, _ = editing.service._timeline_commits()
    seal = commits._attest_acceptance
    # A genuine commit on the old writer path, before recording verification.
    monkeypatch.setattr(commits, "_attest_acceptance", lambda result: None)
    old = editing.commit(note(editing, 0), "legacy-entry")
    assert "verification" not in json.loads(event(editing, old)["payload_json"])
    monkeypatch.setattr(commits, "_attest_acceptance", seal)
    fresh = editing.commit(note(editing, 1), "attested-entry")
    calls = []
    replay = commits._verify_accepted_replay

    def counted(row, edge, *args):
        calls.append(edge["publication_id"])
        return replay(row, edge, *args)

    monkeypatch.setattr(commits, "_verify_accepted_replay", counted)
    for _ in range(2):
        commits.history_entry(editing.project, editing.timeline, fresh["receipt"]["receipt_id"])
    assert calls == [old["receipt"]["receipt_id"]] * 2


@pytest.mark.parametrize("damage", ["result-byte", "metadata-byte", "records-byte", "receipt", "chain", "reorder",
                                   "rewind", "fork", "aba", "partial", "verified-flag", "verification", "facts"])
def test_attested_chain_tampering_refuses_without_writing(editing, damage):
    accepted = [editing.commit(note(editing, i), f"chain-{i}") for i in range(3)]
    conn = editing.service.store.conn
    first, middle, last = accepted
    publication = middle["receipt"]["receipt_id"]
    if damage in {"metadata-byte", "records-byte"}:
        column = "metadata_json" if damage == "metadata-byte" else "records_json"
        conn.execute(f"UPDATE timeline_commit_history SET {column}={column} || ' ' WHERE publication_id=?", (publication,))
    elif damage == "result-byte":
        conn.execute("UPDATE command_idempotency SET result_json=result_json || ' ' WHERE txn_id=?", (publication,))
    elif damage == "receipt":
        conn.execute("UPDATE command_idempotency SET idempotency_key='forged' WHERE txn_id=?", (publication,))
    elif damage in {"chain", "fork"}:
        conn.execute("UPDATE timeline_commit_history SET previous_publication_id=?, previous_revision_id=? WHERE publication_id=?",
                     (first["receipt"]["receipt_id"], first["data"]["accepted_revision_id"], last["receipt"]["receipt_id"]))
    elif damage == "reorder":
        conn.execute("UPDATE timeline_commit_history SET project_seq=project_seq+100 WHERE publication_id=?", (publication,))
    elif damage in {"rewind", "aba"}:
        conn.execute("UPDATE parent_composition_heads SET revision_id=?, publication_id=? WHERE project_id=? AND timeline_id=?",
                     (first["data"]["accepted_revision_id"], first["receipt"]["receipt_id"], editing.project, editing.timeline))
        if damage == "aba":
            conn.execute("UPDATE parent_composition_heads SET revision_id=?, publication_id=? WHERE project_id=? AND timeline_id=?",
                         (last["data"]["accepted_revision_id"], last["receipt"]["receipt_id"], editing.project, editing.timeline))
            conn.execute("UPDATE timeline_commit_history SET metadata_json='{}' WHERE publication_id=?", (publication,))
    elif damage == "partial":
        conn.execute("DELETE FROM timeline_events WHERE id=?", (middle["receipt"]["event_ids"][-1],))
    else:
        row = event(editing, middle)
        payload = json.loads(row["payload_json"])
        if damage == "verified-flag":
            payload["verification"] = True
        elif damage == "verification":
            payload["verification"]["entry_digest"] = "sha256:" + "0" * 64
        else:
            payload["verification"]["facts"]["recorder_abi"] = True
        conn.execute("UPDATE timeline_events SET payload_json=? WHERE id=?", (canonical_json(payload), row["id"]))
    before = real.rows(editing.service)
    with pytest.raises(RuntimeErrorBase):
        editing.service._timeline_commits()[0].head(editing.project, editing.timeline)
    assert real.rows(editing.service) == before


def test_forged_verified_flag_is_refused_even_with_consistent_event_hash(editing):
    result = editing.commit(note(editing, 0), "forged-flag")
    row = event(editing, result)
    payload = json.loads(row["payload_json"])
    payload["verification"] = {"verified": True}
    hashed = {"timeline_id": editing.timeline, "kind": row["kind"], "payload": payload,
              "previous_hash": row["previous_hash"], "created_at": row["created_at"]}
    editing.service.store.conn.execute("UPDATE timeline_events SET payload_json=?, event_hash=? WHERE id=?",
                                       (canonical_json(payload), digest(hashed)[7:], row["id"]))
    with pytest.raises(RuntimeErrorBase):
        editing.history()


def test_attestation_survives_restart_and_offline_command_replays(editing, monkeypatch, capsys):
    from runtime_protocol.cli import main
    from runtime_protocol.timeline_commit_store import TimelineCommitStore

    result = editing.commit(note(editing, 0), "restart-attested")
    root = editing.service.store.root
    editing.service.close()
    replay = TimelineCommitStore._verify_accepted_replay
    calls = []

    def counted(self, row, edge, *args):
        calls.append(edge["publication_id"])
        return replay(self, row, edge, *args)

    monkeypatch.setattr(TimelineCommitStore, "_verify_accepted_replay", counted)
    reopened = RuntimeService(root)
    try:
        commits, _ = reopened._timeline_commits()
        assert commits.history_entry(editing.project, editing.timeline, result["receipt"]["receipt_id"])["receipt"] == result["receipt"]
        assert not calls
    finally:
        reopened.close()
    assert main(["verify-timeline-history", "--root", str(root)]) == 0
    assert json.loads(capsys.readouterr().out) == {"ok": True, "errors": []}
    assert result["receipt"]["receipt_id"] in calls
