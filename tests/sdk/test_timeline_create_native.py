"""Direct adapter checks for the native empty-timeline caller."""
from __future__ import annotations

from copy import deepcopy

from astrid.sdk.remote import RemoteTimelines
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession


def _receipt(data, key="caller-head"):
    return {
        "receipt_id": "init-publication",
        "command_kind": "timeline.commit",
        "idempotency_key": key,
        "request_hash": "a" * 64,
        "project_id": "P-1",
        "project_seq": [2, 2],
        "event_ids": ["init-event"],
        "result": data,
        "created_at": "2026-10-21T00:00:00+00:00",
    }


class _Client:
    def __init__(self):
        self.calls = []
        self.history = []

    def create_timeline(self, project, timeline, *, name=None, idempotency_key):
        self.calls.append(("create_timeline", project, timeline, name, idempotency_key))
        return {"data": {"project_id": "P-1", "timeline_id": timeline, "head_revision_id": "bootstrap"}, "receipt": None}

    def list_timeline_commits(self, project, timeline, *, cursor=None, limit=50):
        self.calls.append(("list_timeline_commits", project, timeline, cursor, limit))
        return {"items": deepcopy(self.history), "next_cursor": None}


class _Session:
    def __init__(self, result=None, error=None):
        self.result, self.error = result, error
        self.calls = []

    def commit(self, command, *, idempotency_key):
        self.calls.append((deepcopy(command), idempotency_key))
        if self.error is not None:
            raise self.error
        return self.result


def _accepted(command, key="caller-head"):
    data = {
        "status": "accepted",
        "accepted_revision_id": "initialized",
        "commands": [deepcopy(command)],
    }
    receipt = _receipt(data, key)
    return {"data": data, "receipt": receipt}


def test_create_empty_uses_create_shell_then_native_capture_without_legacy_post(monkeypatch):
    client = _Client()
    session = _Session()

    def commit(command, *, idempotency_key):
        session.calls.append((deepcopy(command), idempotency_key))
        return _accepted(command, idempotency_key)

    session.commit = commit
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: session)

    result = RemoteTimelines(client).create_empty(
        project="render-smoke", timeline_id="Main", name="Main", config={"tracks": []},
        idempotency_key="caller",
    )

    assert result.ok, result.error
    assert result.data == {
        "project_id": "P-1", "timeline_id": "Main", "name": "Main",
        "head_revision_id": "initialized", "created": True,
    }
    assert client.calls[:2] == [
        ("create_timeline", "render-smoke", "Main", "Main", "caller-shell"),
        ("list_timeline_commits", "P-1", "Main", None, 50),
    ]
    command, key = session.calls[0]
    assert key == "caller-head"
    assert command["op"] == "timeline.init"
    assert command["args"] == {
        "name": "Main",
        "slug": "main",
        "output": {
            "resolution": "1280x720", "fps": 30, "file": "output.mp4",
            "background": None, "background_scale": None,
        },
    }
    assert not any(call[0] == "publish_parent_composition" for call in client.calls)


def test_create_empty_keeps_the_native_flight_for_an_ambiguous_retry(monkeypatch):
    client = _Client()
    first = _Session(error=ConnectionError("response lost after acceptance"))
    second = _Session()
    sessions = iter((first, second))
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: next(sessions))

    failed = RemoteTimelines(client).create_empty(
        project="render-smoke", timeline_id="film", config={"tracks": []}, idempotency_key="caller",
    )
    retried_session = second
    retried_session.result = None

    # The adapter retries the exact persisted operation/key; the real session
    # supplies the persisted flight and prevents recapture over a changed head.
    def retry(command, *, idempotency_key):
        retried_session.calls.append((deepcopy(command), idempotency_key))
        return _accepted(command, idempotency_key)

    retried_session.commit = retry
    retried = RemoteTimelines(client).create_empty(
        project="render-smoke", timeline_id="film", config={"tracks": []}, idempotency_key="caller",
    )

    assert not failed.ok and failed.error.code == "unavailable"
    assert retried.ok, retried.error
    assert first.calls == second.calls
    assert first.calls[0][1] == second.calls[0][1] == "caller-head"
    assert first.calls[0][0] == second.calls[0][0]


def test_create_empty_replays_history_instead_of_reapplying_after_later_edit_or_undo(monkeypatch):
    client = _Client()
    first = _Session()
    first.commit = lambda command, *, idempotency_key: _accepted(command, idempotency_key)
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: first)
    initial = RemoteTimelines(client).create_empty(
        project="render-smoke", timeline_id="film", config={"tracks": []}, idempotency_key="caller",
    )
    assert initial.ok
    client.history.append({"receipt": _receipt(initial.receipt.result, "caller-head")})

    def must_not_reapply(*args, **kwargs):
        raise AssertionError("accepted init was recaptured over a later edit or inverse")

    monkeypatch.setattr(TimelineSession, "open", must_not_reapply)
    replay = RemoteTimelines(client).create_empty(
        project="render-smoke", timeline_id="film", config={"tracks": []}, idempotency_key="caller",
    )

    assert replay.ok, replay.error
    assert replay.data == initial.data
    assert replay.receipt == initial.receipt


def test_create_empty_exposes_runtime_refusal_and_keeps_draft(monkeypatch):
    client = _Client()
    session = _Session(error=CommitConflict({
        "code": "conflict", "message": "timeline changed", "details": {"status": "refused", "reason": "not_pristine"},
    }))
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: session)

    result = RemoteTimelines(client).create_empty(
        project="render-smoke", timeline_id="film", config={"tracks": []}, idempotency_key="caller",
    )

    assert not result.ok
    assert result.error.code == "conflict"
    assert result.error.details == {"status": "refused", "reason": "not_pristine"}
    assert session.calls
    assert not any(call[0] == "publish_parent_composition" for call in client.calls)


def test_create_empty_refuses_unsupported_legacy_canvas_before_creating_a_shell():
    client = _Client()
    result = RemoteTimelines(client).create_empty(
        project="render-smoke", timeline_id="film",
        config={"tracks": [], "theme_overrides": {"visual": {"canvas": {"width": 640, "height": 360, "fps": 24}}}},
        idempotency_key="caller",
    )

    assert not result.ok and result.error.code == "validation_error"
    assert client.calls == []
