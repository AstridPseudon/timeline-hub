"""Frontend durability with generated transport fakes and the real command engine."""
from __future__ import annotations

import copy
import hashlib
import json
from types import SimpleNamespace

import pytest

from astrid.core.timeline.authoring_bundle import open_authoring_bundle
from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline import store
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.outbox import request_bytes
from astrid.sdk.timeline.rebase import replay
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid_runtime_client import ApiError


def initial_bundle():
    payload = {"config": {"output": {"fps": 30}, "tracks": [{"id": "picture", "kind": "visual"}]},
               "clips": [{"id": name, "track": "picture", "clipType": "am-type", "at": 0,
                          "hold": 1, "params": {"text": "café"}} for name in ("a", "b")],
               "occurrences": []}
    digest = "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return open_authoring_bundle({"project_id": "p", "timeline_id": "t", "revision_id": "r0",
                                  "content_digest": digest, "payload": payload},
                                 shot_revisions=[], internal_timeline_revisions=[])


class Generated:
    """Only the generated method boundary is fake; command meaning stays core-owned."""
    def __init__(self, path):
        self.path = path
        self.bundles = {"r0": initial_bundle()}
        self.head = {"revision_id": "r0", "publication_id": "pub0"}
        self.calls, self.accepted, self.records = [], {}, {}
        self.lose_ack = False
        self.refusal = None

    def list_timeline_commits(self, project, timeline, *, limit):
        assert (project, timeline, limit) == ("p", "t", 1)
        return {"head": copy.deepcopy(self.head), "items": [], "next_cursor": None}

    def commit_timeline(self, project, timeline, body, *, idempotency_key):
        raw = request_bytes(body)
        durable = json.loads(self.path.read_bytes())
        flight = durable["flight"]
        assert flight["body"].encode() == raw
        assert flight["key"] == idempotency_key
        assert flight["path"] == "/v1/projects/p/timelines/t/commit"
        self.calls.append((raw, idempotency_key))
        if self.refusal:
            raise self.refusal
        if idempotency_key in self.accepted:
            original, response = self.accepted[idempotency_key]
            if original != raw:
                raise ApiError(409, "conflict", "key payload changed", details={"status": "refused"})
            return copy.deepcopy(response)
        inverse_records = []
        if body["commands"][0]["op"] == "timeline.inverse":
            for publication in body["commands"][0]["args"]["publications"]:
                inverse_records.extend(self.records[publication])
        try:
            plan = execute(self.bundles[body["base_revision_id"]], body["commands"], inverse_records=inverse_records)
            if self.head["revision_id"] != body["base_revision_id"]:
                plan = replay(plan, self.bundles[self.head["revision_id"]])
        except TimelineEditError as exc:
            raise ApiError(409, "conflict", str(exc), details={"status": "conflict", "reason": "guard_changed"}) from exc
        if body["dry_run"]:
            return {"data": {"status": "preview", "evaluated_head": copy.deepcopy(self.head), "id_map": {}}, "receipt": None}
        ordinal = len(self.accepted) + 1
        revision, publication = f"r{ordinal}", f"pub{ordinal}"
        receipt = {"receipt_id": publication, "command_kind": "timeline.commit", "idempotency_key": idempotency_key,
                   "request_hash": hashlib.sha256(raw).hexdigest(), "project_id": project, "project_seq": [ordinal, ordinal],
                   "event_ids": [f"e{ordinal}"], "result": {}, "created_at": "2026-10-19T00:00:00Z"}
        response = {"data": {"status": "accepted", "accepted_revision_id": revision, "id_map": {}}, "receipt": receipt}
        self.bundles[revision] = plan.bundle
        self.records[publication] = plan.records
        self.head = {"revision_id": revision, "publication_id": publication}
        self.accepted[idempotency_key] = (raw, copy.deepcopy(response))
        if self.lose_ack:
            self.lose_ack = False
            raise ConnectionError("response lost after acceptance")
        return response


class Client:
    def __init__(self, generated):
        self._remote = SimpleNamespace(_transport=SimpleNamespace(
            _last_handshake={"realm_id": "realm", "actor_id": "actor"}, _generated=generated))
        self.timelines = SimpleNamespace(open_composition=self.open_composition, open_bundle=self.open_bundle)
        self.projects = SimpleNamespace(current=lambda: DomainResult.success({"project": {"id": "p"}}))
        self.generated = generated
        self.reads = []

    def open_composition(self, project, timeline):
        return DomainResult.success({"native_inspection": {"project_id": "p", "timeline_id": "t"},
                                     "summary": {"head_revision_id": self.generated.head["revision_id"]}})

    def open_bundle(self, project, timeline, *, revision_id):
        self.reads.append(revision_id)
        return DomainResult.success({"bundle": copy.deepcopy(self.generated.bundles[revision_id])})


@pytest.fixture
def connected(tmp_path, monkeypatch):
    path = tmp_path / "outbox.json"
    generated = Generated(path)
    client = Client(generated)
    for module, name in ((store, "publish_bundle"),):
        monkeypatch.setattr(module, name, lambda *a, **kw: pytest.fail("legacy writer called"))
    return client, generated, path


def open_session(connected):
    client, _, path = connected
    return TimelineSession.open("project-slug", "timeline-slug", client=client, outbox_path=path)


def test_capture_and_same_value_write_are_sent_even_without_a_diff(connected):
    session = open_session(connected)
    client, generated, path = connected
    command = session.queue_move("parent/clip:a", 0)
    assert command == capture_move(initial_bundle(), "parent/clip:a", 0)
    result = session.flush()
    assert generated.bundles["r1"]["parent"]["clips"][0]["at"] == 0
    assert any(write["path"] == ["at"] and write["before"] == write["after"]
               for write in generated.records["pub1"][0]["writes"])
    assert result["data"]["accepted_publication_id"] == "pub1"
    assert result["data"]["show_command"] == "astrid timelines show t --project p --published --revision-id r1"
    assert json.loads(path.read_bytes())["pending"] == []
    assert client.reads == ["r0"]


@pytest.mark.parametrize("target", ["parent/clip:a", "parent/clip:b"])
def test_lost_ack_reload_retries_exact_request_before_sending_suffix(connected, target):
    session = open_session(connected)
    client, generated, path = connected
    generated.lose_ack = True
    with pytest.raises(ConnectionError):
        session.move("parent/clip:a", 5, idempotency_key="original")
    before = json.loads(path.read_bytes())["flight"]
    session = open_session(connected)
    suffix = session.queue_move(target, 7)
    # An independent peer changes the head after the ambiguous request.
    generated.bundles["peer"] = copy.deepcopy(generated.bundles["r1"])
    generated.head = {"revision_id": "peer", "publication_id": "peer-publication"}
    session.flush()
    after = json.loads(path.read_bytes())
    assert generated.calls[0] == generated.calls[1]
    assert generated.calls[1] == (before["body"].encode(), "original")
    assert after["base"] == {"revision_id": "r1", "publication_id": "pub1"}
    assert after["pending"] == [suffix]
    assert after["flight"] is None
    # This sends B's ORIGINAL capture, only binding it to A's accepted base.
    session = open_session(connected)
    session.flush()
    body = json.loads(generated.calls[-1][0])
    assert body["commands"] == [suffix]
    assert body["base_revision_id"] == "r1" and body["base_publication_id"] == "pub1"
    assert generated.calls[-1][1] != "original"
    assert len(generated.accepted) == 2
    assert client.reads == ["r0", "r0"]


def test_failed_ack_write_recovers_the_original_flight(connected, monkeypatch):
    session = open_session(connected)
    _, generated, path = connected
    write = session.outbox.write

    def fail_ack(state):
        if state["base"]["revision_id"] == "r1":
            raise OSError("disk unavailable while acknowledging")
        write(state)

    monkeypatch.setattr(session.outbox, "write", fail_ack)
    with pytest.raises(OSError):
        session.move("parent/clip:a", 5)
    assert json.loads(path.read_bytes())["flight"]
    open_session(connected).flush()
    assert len(generated.accepted) == 1
    assert generated.calls[0] == generated.calls[1]
    assert json.loads(path.read_bytes())["pending"] == []


def test_failed_fsync_prevents_send_and_atomic_replace_preserves_unsent_intent(connected, monkeypatch):
    from astrid.sdk.timeline import outbox

    session = open_session(connected)
    _, generated, path = connected
    session.queue_move("parent/clip:a", 5)
    unsent = path.read_bytes()
    with monkeypatch.context() as patch:
        patch.setattr(outbox.os, "fsync", lambda fd: (_ for _ in ()).throw(OSError("fsync failed")))
        with pytest.raises(OSError):
            session.flush()
    assert generated.calls == []
    assert path.read_bytes() == unsent
    assert list(path.parent.glob(".outbox-*")) == []
    session.flush()
    assert generated.accepted


def test_changed_intent_key_and_dry_run_cannot_replace_an_ambiguous_request(connected):
    session = open_session(connected)
    _, generated, path = connected
    generated.lose_ack = True
    with pytest.raises(ConnectionError):
        session.move("parent/clip:a", 5, idempotency_key="original")
    persisted = path.read_bytes()
    for attempt in (lambda: session.move("parent/clip:a", 6),
                    lambda: session.flush(idempotency_key="different"),
                    lambda: session.flush(dry_run=True)):
        with pytest.raises(TimelineEditError):
            attempt()
        assert path.read_bytes() == persisted
    assert len(generated.calls) == 1


def test_semantic_conflict_is_retained_but_transport_failure_stays_ambiguous(connected):
    session = open_session(connected)
    _, generated, path = connected
    session.queue_move("parent/clip:a", 5)
    peer = execute(initial_bundle(), [capture_move(initial_bundle(), "parent/clip:a", 3)])
    generated.bundles["peer"] = peer.bundle
    generated.head = {"revision_id": "peer", "publication_id": "peer-publication"}
    with pytest.raises(CommitConflict):
        session.flush()
    state = json.loads(path.read_bytes())
    assert state["conflict"]["details"]["status"] == "conflict"
    assert state["pending"] and state["flight"]
    assert not generated.accepted
    generated.refusal = ConnectionError("connection unavailable")
    with pytest.raises(ConnectionError):
        open_session(connected).flush()
    assert json.loads(path.read_bytes()) == state


def test_preview_remains_unsent_and_acceptance_and_inverse_get_fresh_keys(connected):
    session = open_session(connected)
    _, generated, path = connected
    preview = session.move("parent/clip:a", 5, dry_run=True, idempotency_key="preview")
    assert preview["receipt"] is None and "show_command" not in preview["data"]
    assert not generated.accepted
    assert json.loads(path.read_bytes())["pending"]
    with pytest.raises(TimelineEditError, match="fresh key"):
        session.flush(idempotency_key="preview")
    accepted = session.flush()
    publication = accepted["receipt"]["receipt_id"]
    session.undo([publication])
    assert len({key for _, key in generated.calls}) == 3
    inverse = json.loads(generated.calls[-1][0])["commands"][0]
    assert inverse == {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
                       "args": {"publications": [publication]}}
    assert generated.bundles["r2"]["parent"] == initial_bundle()["parent"]


def test_identity_change_cannot_send_existing_outbox(connected):
    session = open_session(connected)
    client, generated, path = connected
    session.queue_move("parent/clip:a", 5)
    original = path.read_bytes()
    client._remote._transport._last_handshake["realm_id"] = "other-realm"
    with pytest.raises(TimelineEditError, match="identity changed"):
        session.flush()
    with pytest.raises(TimelineEditError, match="different realm"):
        open_session(connected)
    assert path.read_bytes() == original
    assert generated.calls == []


def test_new_clean_session_captures_current_published_state(connected):
    session = open_session(connected)
    _, generated, _ = connected
    session.move("parent/clip:a", 5)
    generated.bundles["peer"] = execute(generated.bundles["r1"], [
        capture_move(generated.bundles["r1"], "parent/clip:b", 3),
    ]).bundle
    generated.head = {"revision_id": "peer", "publication_id": "peer-publication"}
    command = open_session(connected).queue_move("parent/clip:b", 7)
    assert command == capture_move(generated.bundles["peer"], "parent/clip:b", 7)


def test_nonidentity_map_does_not_acknowledge_pending_work(connected, monkeypatch):
    session = open_session(connected)
    _, generated, path = connected
    send = generated.commit_timeline

    def remapping(*args, **kwargs):
        response = send(*args, **kwargs)
        response["data"]["id_map"] = {"a": "different"}
        return response

    monkeypatch.setattr(generated, "commit_timeline", remapping)
    with pytest.raises(TimelineEditError, match="nonidentity"):
        session.move("parent/clip:a", 5)
    state = json.loads(path.read_bytes())
    assert state["flight"] and state["pending"] and state["base"]["revision_id"] == "r0"
