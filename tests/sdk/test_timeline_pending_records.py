"""Durable SDK records for refused timeline edits."""
from __future__ import annotations

import copy
from pathlib import Path
from types import SimpleNamespace

from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline.outbox import Outbox, request_bytes
from astrid.sdk.timeline.sync import TimelineSession


def _session(path):
    transport = SimpleNamespace(_last_handshake={"realm_id": "realm", "actor_id": "actor"})
    timelines = SimpleNamespace(
        open_composition=lambda *a, **kw: DomainResult.success({
            "native_inspection": {"project_id": "project", "timeline_id": "timeline"},
            "summary": {"head_revision_id": "r2"}}),
        history=lambda *a, **kw: DomainResult.success({
            "head": {"revision_id": "r2", "publication_id": "p2"}}))
    client = SimpleNamespace(_remote=SimpleNamespace(_transport=transport), timelines=timelines)
    identity = {"realm_id": "realm", "actor_id": "actor"}
    return TimelineSession(client, Outbox(Path(path)), identity, "project", "timeline")


def _scope():
    return {"realm_id": "realm", "actor_id": "actor", "project_id": "project",
            "timeline_id": "timeline"}


def test_pending_drop_keeps_raw_record_and_tombstone(tmp_path):
    session = _session(tmp_path / "outbox.json")
    record = {"id": "pc_0123456789ab", "state": "pending", "rev": 2,
              "key": "recut", "key_generated": False, "label": "Recut", "origin": "list",
              "parts": [{"base": {"revision_id": "r1", "publication_id": "p1"},
                         "commands": [{"op": "clip.move", "select": "clip:a", "args": {"on": 3}}],
                         "commit_options": {"merge": "fields"}, "rationale": None,
                         "media_input": None, "imports": [], "evaluation": None}],
              "part": 0, "failure": {"details": {"status": "conflict"}},
              "head": {"revision_id": "r2", "publication_id": "p2"}, "choices": {},
              "candidate": None, "flight_fence": None, "receipts": [], "versions": [],
              "created_at": "2026-10-29T00:00:00Z", "updated_at": "2026-10-29T00:00:00Z",
              "dropped_reason": None}
    session.outbox.write({"scope": _scope(), "base": record["parts"][0]["base"],
                          "pending": [], "flight": None, "pending_changes": {record["id"]: record}})

    assert session.pending_list() == [record]
    assert session.pending_show("recut") == record
    dropped = session.pending_drop(record["id"], reason="keep for later")

    assert dropped["state"] == "dropped"
    assert dropped["rev"] == 3
    assert dropped["dropped_reason"] == "keep for later"
    assert dropped["parts"] == record["parts"]
    assert session.pending_list() == []
    assert session.pending_list(all=True) == [dropped]
    assert session.pending_show(record["id"]) == dropped


def test_open_migrates_legacy_rejected_conflict(tmp_path):
    path = tmp_path / "outbox.json"
    session = _session(path)
    body = {"api_version": 1, "project_id": "project", "timeline_id": "timeline",
            "base_revision_id": "r1", "base_publication_id": "p1",
            "commands": [{"op": "clip.move", "select": "clip:a", "args": {"on": 3}}],
            "label": "Recut", "steps": [{"id": "step-1"}], "merge": "fields"}
    flight = {"body": request_bytes(body).decode(), "key": "wire-key", "logical_key": "recut",
              "explicit_key": True, "count": 1, "fence": "fence"}
    failure = {"code": "conflict", "message": "head moved", "details": {
        "status": "conflict", "reason": "head_moved",
        "current": {"revision_id": "r2", "publication_id": "p2"}, "conflicts": []}}
    state = {"scope": _scope(), "base": {"revision_id": "r1", "publication_id": "p1"},
             "pending": [], "flight": None,
             "rejected": {"base": {"revision_id": "r1", "publication_id": "p1"},
                          "commands": copy.deepcopy(body["commands"]), "flight": flight,
                          "failure": failure, "commit_options": {"label": "Recut", "merge": "fields"},
                          "evaluation": None}}
    session.outbox.write(state)

    # Opening an already scoped outbox migrates it before returning.
    session = TimelineSession.open("project", "timeline", client=session.client, outbox_path=path)
    saved = session.pending_list()[0]
    persisted = session.outbox.read()

    assert saved["key"] == "recut"
    assert saved["key_generated"] is False
    assert saved["label"] == "Recut"
    assert saved["parts"][0]["commands"] == body["commands"]
    assert saved["failure"] == failure
    assert persisted["pending"] == [] and persisted["flight"] is None
    assert "rejected" not in persisted
