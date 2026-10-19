"""Frontend durability with generated transport fakes and the real command engine."""
from __future__ import annotations

import copy
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from types import SimpleNamespace

import pytest

from astrid.core.receipts.canonical import canonical_json
from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
from astrid.sdk.contracts import DomainResult
from astrid.sdk.remote import RemoteTimelines
from astrid.sdk.timeline import store
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.outbox import request_bytes
from astrid.sdk.timeline.rebase import replay
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid.sdk.workspace_client import WorkspaceClient, WorkspaceClientError
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

    def list_timeline_commits(self, project, timeline, *, cursor=None, limit):
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
        ordinal = len(self.accepted) + 1
        revision, publication = f"r{ordinal}", f"pub{ordinal}"
        compiled = compile_authoring_candidate(plan.bundle).publication
        document = {"schema_version": 1, "project_id": project, "timeline_id": timeline,
                    "parent_revision": {"revision_id": revision, "content_digest": compiled["content_digest"],
                                        "payload": compiled["parent_composition"]},
                    "shot_revisions": compiled["shot_revisions"],
                    "internal_timeline_revisions": compiled["internal_timeline_revisions"],
                    "dependency_manifest": {**compiled["dependency_manifest"], "documents": []}}
        candidate = {"canonical_document": document, "document_digest": "sha256:" + hashlib.sha256(
            json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest(),
            "commands": plan.commands, "id_map": {}, "provider_version": "astrid-v1", "compiler_version": "m1"}
        base = {key: body[key] for key in ("base_revision_id", "base_publication_id")}
        if body.get("dry_run", False):
            return {"data": {"status": "preview", **base, "evaluated_head": copy.deepcopy(self.head), **candidate}, "receipt": None}
        rebased = self.head != {"revision_id": body["base_revision_id"], "publication_id": body["base_publication_id"]}
        data = {"status": "rebased" if rebased else "accepted", **base,
                "previous_revision_id": self.head["revision_id"], "previous_publication_id": self.head["publication_id"],
                "accepted_revision_id": revision, "rebased_onto": copy.deepcopy(self.head) if rebased else None,
                **candidate, "publisher": "actor"}
        for key in ("source", "label", "rationale", "group_id"):
            if key in body:
                data[key] = copy.deepcopy(body[key])
        receipt = {"receipt_id": publication, "command_kind": "timeline.commit", "idempotency_key": idempotency_key,
                   "request_hash": hashlib.sha256(canonical_json({"operation": "commitTimeline", "path": flight["path"],
                       "publisher": "actor", "request": body}).encode()).hexdigest(), "project_id": project, "project_seq": [ordinal, ordinal],
                   "event_ids": [f"e{ordinal}"], "result": copy.deepcopy(data), "created_at": "2026-10-19T00:00:00Z"}
        response = {"data": data, "receipt": receipt}
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
        transport = WorkspaceClient.__new__(WorkspaceClient)
        transport._generated = generated
        transport._last_handshake = {"realm_id": "realm", "actor_id": "actor"}
        self._remote = SimpleNamespace(_transport=transport)
        self.timelines = RemoteTimelines(transport)
        self.timelines.open_composition = self.open_composition
        self.timelines.open_bundle = self.open_bundle
        self.timelines._resolve_timeline = lambda *a, **kw: DomainResult.success({"project_id": "p", "timeline_id": "t"})
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
    assert result["receipt"] == next(iter(generated.accepted.values()))[1]["receipt"]
    assert "show_command" not in result["receipt"]["result"]
    assert json.loads(path.read_bytes())["pending"] == []
    assert client.reads == ["r0"]


@pytest.mark.parametrize("target", ["parent/clip:a", "parent/clip:b"])
def test_lost_ack_reload_retries_exact_request_before_sending_suffix(connected, target):
    session = open_session(connected)
    client, generated, path = connected
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
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
    with pytest.raises(WorkspaceClientError):
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
    with pytest.raises(WorkspaceClientError):
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


def test_blocked_send_allows_queue_and_acknowledges_only_frozen_prefix(connected, monkeypatch):
    session = open_session(connected)
    _, generated, path = connected
    entered, release = Event(), Event()
    send = generated.commit_timeline

    def blocked(*args, **kwargs):
        response = send(*args, **kwargs)
        entered.set()
        assert release.wait(10)
        return response

    monkeypatch.setattr(generated, "commit_timeline", blocked)
    session.queue_move("parent/clip:a", 5)
    with ThreadPoolExecutor(max_workers=2) as pool:
        sending = pool.submit(session.flush, idempotency_key="original")
        try:
            assert entered.wait(10)
            frozen = json.loads(path.read_bytes())["flight"]
            suffix = pool.submit(open_session(connected).queue_move, "parent/clip:a", 7).result(timeout=10)
            during = json.loads(path.read_bytes())
            assert during["flight"] == frozen and during["pending"][1:] == [suffix]
            assert suffix["reads"] and suffix["selections"] and suffix["bindings"]
        finally:
            release.set()
        sending.result(timeout=10)
    state = json.loads(path.read_bytes())
    assert state["base"] == {"revision_id": "r1", "publication_id": "pub1"}
    assert state["flight"] is None and state["pending"] == [suffix]
    open_session(connected).flush()
    assert json.loads(generated.calls[-1][0])["commands"] == [suffix]
    assert len(generated.accepted) == 2


@pytest.mark.parametrize("late", ["ack", "timeout", "conflict"])
def test_duplicate_flush_and_late_completion_cannot_overwrite_new_flight(connected, monkeypatch, late):
    session = open_session(connected)
    _, generated, path = connected
    entered_a, entered_b, release_a, release_b = Event(), Event(), Event(), Event()
    send = generated.commit_timeline

    def blocked(*args, **kwargs):
        response = send(*args, **kwargs)
        if kwargs["idempotency_key"] == "a" and not entered_a.is_set():
            entered_a.set()
            assert release_a.wait(10)
            if late == "timeout":
                raise ConnectionError("late timeout")
            if late == "conflict":
                raise ApiError(409, "conflict", "late conflict", details={"status": "conflict"})
        elif kwargs["idempotency_key"] == "b":
            entered_b.set()
            assert release_b.wait(10)
        return response

    monkeypatch.setattr(generated, "commit_timeline", blocked)
    session.queue_move("parent/clip:a", 5)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(session.flush, idempotency_key="a")
        try:
            assert entered_a.wait(10)
            open_session(connected).flush(idempotency_key="a")
            assert generated.calls[0] == generated.calls[1]
            session.queue_move("parent/clip:a", 7)
            second = pool.submit(session.flush, idempotency_key="b")
            assert entered_b.wait(10)
            newer = path.read_bytes()
            release_a.set()
            if late == "ack":
                first.result(timeout=10)
            else:
                with pytest.raises(CommitConflict if late == "conflict" else WorkspaceClientError):
                    first.result(timeout=10)
            assert path.read_bytes() == newer
            assert json.loads(newer)["flight"]["key"] == "b"
        finally:
            release_a.set()
            release_b.set()
        second.result(timeout=10)
    assert len(generated.accepted) == 2
    assert json.loads(path.read_bytes())["pending"] == []


@pytest.mark.parametrize(("field", "value"), [
    (("data", "status"), "preview"),
    (("receipt",), None),
    (("receipt", "receipt_id"), ""),
    (("receipt", "receipt_id"), "pub0"),
    (("receipt", "command_kind"), "timeline.restore"),
    (("receipt", "project_id"), "other"),
    (("receipt", "idempotency_key"), "other"),
    (("receipt", "request_hash"), "wrong"),
    (("receipt", "result"), {}),
    (("receipt", "project_seq"), [True, 1]),
    (("data", "base_revision_id"), "other"),
    (("data", "base_publication_id"), "other"),
    (("data", "publisher"), "other"),
    (("data", "accepted_revision_id"), "other"),
    (("data", "previous_publication_id"), "other"),
    (("data", "rebased_onto"), {"revision_id": "peer", "publication_id": "peer"}),
    (("data", "canonical_document", "project_id"), "other"),
    (("data", "canonical_document", "timeline_id"), "other"),
    (("data", "canonical_document", "schema_version"), True),
    (("data", "canonical_document", "parent_revision", "revision_id"), "other"),
    (("data", "canonical_document", "parent_revision", "payload"), []),
    (("data", "canonical_document", "shot_revisions"), None),
    (("data", "canonical_document", "dependency_manifest"), {}),
    (("data", "commands"), []),
    (("data", "commands"), [{}]),
    (("data", "id_map"), None),
    (("data", "id_map"), {"": ""}),
    (("data", "provider_version"), 1),
    (("data", "compiler_version"), ""),
    (("data", "document_digest"), "bad"),
])
def test_invalid_ack_retains_exact_flight_and_suffix(connected, monkeypatch, field, value):
    session = open_session(connected)
    _, generated, path = connected
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        session.move("parent/clip:a", 5, idempotency_key="original")
    session.queue_move("parent/clip:a", 7)
    before = path.read_bytes()
    send = generated.commit_timeline

    def invalid(*args, **kwargs):
        result = send(*args, **kwargs)
        target = result
        for key in field[:-1]:
            target = target[key]
        target[field[-1]] = value
        # Isolate semantic validation from the independent result equality check.
        if field[0] == "data":
            result["receipt"]["result"] = copy.deepcopy(result["data"])
        return result

    with monkeypatch.context() as patch:
        patch.setattr(generated, "commit_timeline", invalid)
        with pytest.raises((TimelineEditError, ValueError)):
            open_session(connected).flush()
    assert path.read_bytes() == before
    open_session(connected).flush()
    assert generated.calls[-1] == generated.calls[0]
    assert len(json.loads(path.read_bytes())["pending"]) == 1


@pytest.mark.parametrize(("field", "value"), [
    (("data", "status"), "accepted"),
    (("receipt",), {}),
    (("data", "evaluated_head"), {"revision_id": "r0"}),
    (("data", "accepted_revision_id"), "r1"),
    (("data", "base_publication_id"), "wrong"),
    (("data", "canonical_document", "timeline_id"), "wrong"),
])
def test_invalid_preview_never_releases_original_request(connected, monkeypatch, field, value):
    session = open_session(connected)
    _, generated, path = connected
    send = generated.commit_timeline
    before = []

    def invalid(*args, **kwargs):
        before.append(path.read_bytes())
        result = send(*args, **kwargs)
        target = result
        for key in field[:-1]:
            target = target[key]
        target[field[-1]] = value
        return result

    monkeypatch.setattr(generated, "commit_timeline", invalid)
    with pytest.raises((TimelineEditError, ValueError)):
        session.move("parent/clip:a", 5, dry_run=True, idempotency_key="preview")
    assert path.read_bytes() == before[0]
    assert not generated.accepted


@pytest.mark.parametrize("optional", [{}, {"dry_run": False, "source": {"via": "cli", "detail": "café"},
                                          "label": "", "rationale": "keep this", "group_id": "gesture"}])
def test_restart_preserves_parsed_body_source_and_optional_presence(connected, optional):
    session = open_session(connected)
    client, generated, path = connected
    command = session.queue_move("parent/clip:a", 5)
    with session.outbox.locked():
        state = session._state()
        body = {"api_version": 1, "project_id": "p", "timeline_id": "t", "base_revision_id": "r0",
                "base_publication_id": "pub0", "commands": [command], **optional}
        state["flight"] = {"path": session.path, "key": "original", "count": 1,
                           "body": request_bytes(body).decode()}
        session.outbox.write(state)
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        session.flush(via="app")
    frozen = json.loads(path.read_bytes())["flight"]
    # Explicit reconnect may change discovery/credential, never authenticated scope.
    client._remote._transport.endpoint = "http://new-runtime-door"
    client._remote._transport.token = "rotated"
    open_session(connected).flush(via="python")
    assert generated.calls == [(frozen["body"].encode(), "original")] * 2
    assert json.loads(generated.calls[-1][0]) == body


@pytest.mark.parametrize("change", ["read", "identity"])
def test_dependent_suffix_conflict_preserves_original_guards_and_identity(connected, change):
    session = open_session(connected)
    _, generated, path = connected
    generated.lose_ack = True
    with pytest.raises(WorkspaceClientError):
        session.move("parent/clip:a", 5)
    suffix = session.queue_move("parent/clip:a", 7)
    original = copy.deepcopy(suffix)
    session.flush()
    peer = copy.deepcopy(generated.bundles["r1"])
    peer["parent"]["clips"][0]["hold" if change == "read" else "id"] = 2 if change == "read" else "replacement"
    generated.bundles["peer"] = peer
    generated.head = {"revision_id": "peer", "publication_id": "peer-publication"}
    with pytest.raises(CommitConflict):
        open_session(connected).flush(idempotency_key="b")
    state = json.loads(path.read_bytes())
    assert state["pending"] == [original]
    assert state["conflict"] and state["flight"]["key"] == "b"
    body = json.loads(state["flight"]["body"])
    assert body["commands"] == [original] and body["base_revision_id"] == "r1"
    before = path.read_bytes()
    with pytest.raises(TimelineEditError, match="immutable"):
        session.flush(idempotency_key="replacement")
    assert path.read_bytes() == before


@pytest.mark.parametrize("field", ["realm_id", "actor_id"])
def test_scope_change_while_response_is_outstanding_keeps_original_flight(connected, monkeypatch, field):
    session = open_session(connected)
    client, generated, path = connected
    entered, release = Event(), Event()
    send = generated.commit_timeline

    def blocked(*args, **kwargs):
        result = send(*args, **kwargs)
        entered.set()
        assert release.wait(10)
        return result

    monkeypatch.setattr(generated, "commit_timeline", blocked)
    session.queue_move("parent/clip:a", 5)
    with ThreadPoolExecutor(max_workers=1) as pool:
        sending = pool.submit(session.flush)
        try:
            assert entered.wait(10)
            before = path.read_bytes()
            handshake = client._remote._transport._last_handshake
            original = handshake[field]
            handshake[field] = "other"
        finally:
            release.set()
        with pytest.raises(TimelineEditError, match="identity changed"):
            sending.result(timeout=10)
    assert path.read_bytes() == before
    handshake[field] = original
    open_session(connected).flush()
    assert generated.calls[0] == generated.calls[1]
    assert len(generated.accepted) == 1


@pytest.mark.parametrize("field", ["realm_id", "actor_id"])
def test_missing_authenticated_scope_never_defaults_identity(connected, field):
    client, generated, path = connected
    del client._remote._transport._last_handshake[field]
    with pytest.raises(TimelineEditError, match="authenticated"):
        open_session(connected)
    assert not path.exists() and not generated.calls


@pytest.mark.parametrize("reading", ["history", "bundle"])
def test_blocked_read_does_not_hold_outbox_lock_or_overwrite_concurrent_work(connected, monkeypatch, reading):
    session = open_session(connected)
    client, generated, path = connected
    entered, release = Event(), Event()
    if reading == "bundle":
        session.queue_move("parent/clip:a", 5)
    read = client.timelines.history if reading == "history" else client.timelines.open_bundle

    def blocked(*args, **kwargs):
        result = read(*args, **kwargs)
        entered.set()
        assert release.wait(10)
        return result

    monkeypatch.setattr(client.timelines, "history" if reading == "history" else "open_bundle", blocked)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(open_session, connected) if reading == "history" else pool.submit(session.queue_move, "parent/clip:b", 7)
        try:
            assert entered.wait(10)
            if reading == "history":
                # Capture can read through a separate session while history is blocked.
                queued = pool.submit(session.queue_move, "parent/clip:a", 5).result(timeout=10)
                before = path.read_bytes()
            else:
                pool.submit(session.flush).result(timeout=10)
                assert json.loads(path.read_bytes())["base"]["revision_id"] == "r1"
        finally:
            release.set()
        result = first.result(timeout=10)
    state = json.loads(path.read_bytes())
    if reading == "history":
        assert path.read_bytes() == before and state["pending"] == [queued]
        assert result.project_id == "p"
    else:
        assert state["base"]["revision_id"] == "r1" and state["pending"] == [result]
        assert client.reads == ["r0", "r0", "r1"]
