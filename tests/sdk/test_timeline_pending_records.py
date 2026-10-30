"""Durable SDK records for refused timeline edits."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline.commit_session import Timeline
from astrid.sdk.timeline.outbox import Outbox
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


def _timeline(session):
    timeline = Timeline.__new__(Timeline)
    timeline.session = session
    return timeline


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
    timeline = _timeline(session)

    assert timeline.pending_list() == [record]
    assert timeline.pending_show("recut") == record
    dropped = timeline.pending_drop(record["id"], reason="keep for later")

    assert dropped["state"] == "dropped"
    assert dropped["rev"] == 3
    assert dropped["dropped_reason"] == "keep for later"
    assert dropped["parts"] == record["parts"]
    assert timeline.pending_list() == []
    assert timeline.pending_list(all=True) == [dropped]
    assert timeline.pending_show(record["id"]) == dropped
