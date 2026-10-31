"""Focused regressions for keyed interrupted saves and function clashes."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline._pending import clash
from astrid.sdk.timeline.outbox import Outbox
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession

BASE = {"revision_id": "r0", "publication_id": "pub0"}
HEAD = {"revision_id": "r1", "publication_id": "pub1"}


def _failure(head=HEAD):
    return {
        "code": "commit_conflict",
        "message": "timeline changed",
        "details": {
            "status": "conflict",
            "reason": "value_conflict",
            "current": copy.deepcopy(head),
            "conflicts": [],
        },
    }


def _session(tmp_path, monkeypatch, state=None):
    identity = {"realm_id": "realm", "actor_id": "actor"}
    outbox = Outbox(tmp_path / "shared-outbox.json")
    outbox.write(state or {
        "scope": {**identity, "project_id": "project", "timeline_id": "film"},
        "base": copy.deepcopy(HEAD),
        "pending": [],
        "flight": None,
    })
    session = TimelineSession(object(), outbox, identity, "project", "film")
    monkeypatch.setattr("astrid.sdk.timeline.sync._connection", lambda _client: identity)
    monkeypatch.setattr("astrid.sdk.timeline.sync._pending_diff", lambda _session, _record: None)
    monkeypatch.setattr("astrid.sdk.timeline.sync._pending_clash", lambda _session, record: record)
    return session


def _save(session, commands, *, key="edit-key", evaluation=None, failure=None):
    return session.save_interrupted(
        commands,
        base=BASE,
        label="Arrange",
        steps=[],
        merge="atomic",
        reads=None,
        key=key,
        evaluation=evaluation or {"kind": "label"},
        failure=failure or _failure(),
    )


def test_repeated_keyed_save_interrupted_updates_one_pending_record(tmp_path, monkeypatch):
    session = _session(tmp_path, monkeypatch)

    first = _save(session, [{"op": "timeline.move", "args": {"on": 1}}])
    first_id = first.pending_id
    first_record = session.outbox.read()["pending_changes"][first_id]

    second = _save(session, [{"op": "timeline.move", "args": {"on": 1}}],
                   failure=_failure({"revision_id": "r2", "publication_id": "pub2"}))
    state = session.outbox.read()

    assert second.pending_id == first_id
    assert list(state["pending_changes"]) == [first_id]
    record = state["pending_changes"][first_id]
    assert record["attempts"] == 2
    assert record["rev"] == first_record["rev"] + 1
    assert record["parts"][0]["commands"] == [{"op": "timeline.move", "args": {"on": 1}}]
    assert record["head"] == {"revision_id": "r2", "publication_id": "pub2"}
    assert len(record["versions"]) == 1


def test_function_clash_guidance_keeps_the_function_retry_parameter():
    record = {
        "id": "pc_function",
        "state": "pending",
        "key": "function-key",
        "label": "Arrange",
        "origin": "function",
        "parts": [{"base": BASE}],
        "head": HEAD,
        "failure": _failure(),
    }

    packet = clash(record)
    error = CommitConflict(_failure(), label="Arrange", pending_id=record["id"], clash=packet)

    assert packet["next"] == 'tl.retry("pc_function", your_function)'
    assert 'tl.retry("pc_function", your_function)' in error.fix
    assert error.outcome == "not_applied"


def test_function_clash_is_retained_in_shared_outbox(tmp_path, monkeypatch):
    state = {
        "scope": {"realm_id": "realm", "actor_id": "actor", "project_id": "project", "timeline_id": "film"},
        "base": copy.deepcopy(BASE),
        "pending": [{"op": "timeline.move", "args": {"on": 4}}],
        "flight": {},
        "conflict": {"details": {"status": "conflict", "current": copy.deepcopy(HEAD)}},
        "evaluation": {"kind": "function"},
    }
    session = _session(tmp_path, monkeypatch, state)
    error = _save(session, [{"op": "timeline.move", "args": {"on": 1}}],
                  key="function-key", evaluation={"kind": "function", "count": 2})

    # A second session reading the same default outbox sees the durable retry record.
    reopened = Outbox(session.outbox.path).read()
    record = reopened["pending_changes"][error.pending_id]

    assert record["origin"] == "function"
    assert record["key"] == "function-key"
    assert record["parts"][0]["evaluation"] == {"kind": "function", "count": 2}
    assert record["flight"]["evaluation"] == {"kind": "function", "count": 2}
    assert reopened["pending_changes"][error.pending_id]["state"] == "pending"
    assert reopened["pending"] == []
    assert reopened["flight"] is None


def test_duplicate_pending_key_error_says_to_use_pending_id(tmp_path, monkeypatch):
    state = {
        "scope": {"realm_id": "realm", "actor_id": "actor", "project_id": "project", "timeline_id": "film"},
        "base": copy.deepcopy(HEAD),
        "pending": [],
        "flight": None,
        "pending_changes": {
            "pc_one": {"id": "pc_one", "key": "edit-key", "state": "pending"},
            "pc_two": {"id": "pc_two", "key": "edit-key", "state": "pending"},
        },
    }
    session = _session(tmp_path, monkeypatch, state)

    with pytest.raises(TimelineEditError, match="pending key 'edit-key' is ambiguous; use a pending id") as caught:
        _save(session, [{"op": "timeline.move", "args": {"on": 3}}])

    assert str(caught.value) == "pending key 'edit-key' is ambiguous; use a pending id"
