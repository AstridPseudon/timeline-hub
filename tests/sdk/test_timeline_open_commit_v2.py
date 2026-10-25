"""Public G2 sessions: real native execution, durable transport and conflict reruns.

The generated-client boundary is fake; provider-v2 and G3 emitter integration
remain separately owned. No test supplies a second patch executor.
"""
from __future__ import annotations

import copy
import json
import sys

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline import api, commit_session
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.sync import CommitConflict
from astrid.sdk.workspace_client import WorkspaceClientError
from astrid_runtime_client import ApiError
from tests.sdk.test_timeline_commit_provider_document import document_fixture
from tests.sdk.test_timeline_sync import connected  # noqa: F401


def opened(connected):
    client, _, path = connected
    return timeline.open("p", "t", client=client, outbox_path=path)


def at(tl, clip="a"):
    return next(row["at"] for row in tl.bundle["parent"]["clips"] if row["id"] == clip)


def advance(generated, ordinal, *, clip="a"):
    base = generated.bundles[generated.head["revision_id"]]
    command = {"schema_version": 1, "op": "clip.move", "version": "1",
               "select": "parent/clip:" + clip, "args": {"on": ordinal}}
    revision = "other-" + str(ordinal)
    generated.bundles[revision] = execute(base, [command]).bundle
    generated.head = {"revision_id": revision, "publication_id": "pub-" + revision}
    # The peer head is produced by the real command engine above; keep the
    # public reader's authenticated revision/publication pair in sync with it.
    generated.publications[revision] = generated.head["publication_id"]


def conflict(generated, *, status="conflict", current=True):
    return ApiError(409 if status != "invalid" else 422, "conflict", "changed", details={
        "status": status, "reason": "value_conflict", "code": "value_conflict",
        "path": ["clips", "id:a", "at"], "hint": "read the head", "suggested_command": "timeline show",
        "current": copy.deepcopy(generated.head) if current else None,
    })


def test_open_exports_and_default_connection(connected, monkeypatch):
    from astrid.sdk import AstridClient

    client, _, path = connected
    monkeypatch.setattr(AstridClient, "open_from_launcher", lambda **kwargs: client)
    tl = timeline.open(outbox_path=path)
    assert isinstance(tl, timeline.Timeline)
    assert api.open is timeline.open
    assert api.Timeline is timeline.Timeline
    assert api.CommitConflict is timeline.CommitConflict
    assert tl.bundle == client.generated.bundles["r0"]
    assert tl.head == {"revision_id": "r0", "publication_id": "pub0"}
    assert client.reads == ["r0"]


def test_native_edits_commit_once_with_label_and_steps(connected):
    tl = opened(connected)
    _, generated, path = connected
    tl.move("parent/clip:a", 3).move("parent/clip:b", 6)
    assert generated.calls == []
    result = tl.commit("Move both", reads=[])
    assert len(generated.calls) == 1
    body = json.loads(generated.calls[0][0])
    assert body["label"] == "Move both"
    assert body["merge"] == "fields" and body["reads"] == []
    assert [step["command_ordinals"] for step in body["steps"]] == [[0], [1]]
    assert all(step["patch"] == [] for step in body["steps"])
    assert (at(tl), at(tl, "b")) == (3, 6)
    assert tl.head == {"revision_id": result["data"]["accepted_revision_id"],
                       "publication_id": result["receipt"]["receipt_id"]}
    assert json.loads(path.read_text())["pending"] == []
    assert tl._journal == []


@pytest.mark.parametrize("selected", [None, ["step-2"]])
def test_public_session_undo_preserves_whole_shape_and_forwards_steps(connected, selected):  # noqa: F811
    tl = opened(connected)
    _, generated, _ = connected
    tl.move("parent/clip:a", 3).move("parent/clip:b", 6)
    accepted = tl.commit("Move both")
    publication = accepted["receipt"]["receipt_id"]

    selector = None if selected is None else {publication: selected}
    tl.undo(publications=[publication], steps=selector)

    inverse = json.loads(generated.calls[-1][0])["commands"][0]
    assert inverse["args"]["publications"] == [publication]
    if selector is None:
        assert "steps" not in inverse["args"]
    else:
        assert inverse["args"]["steps"] == selector


@pytest.mark.parametrize("status", ["merged", "rebased"])
def test_adopts_complete_merged_head_including_other_writer(connected, monkeypatch, status):
    tl = opened(connected)
    _, generated, _ = connected
    tl.move("parent/clip:a", 4)
    advance(generated, 9, clip="b")
    original = generated.commit_timeline

    def reply(*args, **kwargs):
        result = original(*args, **kwargs)
        if result["data"]["status"] == "rebased":
            result["data"]["status"] = status
            result["receipt"]["result"]["status"] = status
        return result

    monkeypatch.setattr(generated, "commit_timeline", reply)
    result = tl.commit("Move a")
    assert result["data"]["status"] == status
    assert (at(tl), at(tl, "b")) == (4, 9)
    tl.move("parent/clip:a", 5)
    tl.commit("Continue from merged head")
    assert json.loads(generated.calls[-1][0])["base_revision_id"] == result["data"]["accepted_revision_id"]
    assert at(tl, "b") == 9


def test_declared_request_and_step_reads_and_atomic_are_preserved(connected):
    tl = opened(connected)
    _, generated, _ = connected
    step_reads = [{"kind": "collection", "ref": "parent", "path": ["clips"],
                   "members": ["a", "b"], "order": ["a", "b"]}]
    request_reads = [{"kind": "scope", "ref": "internal-revision:physical-id", "path": []}]
    tl.command({"schema_version": 1, "op": "clip.move", "version": "1", "select": "parent/clip:a",
                "args": {"on": 2}}, label="Step", intent="place title", tags=["title"], reads=step_reads)
    step_reads.clear()
    tl.commit("Atomic batch", merge="atomic", reads=request_reads)
    body = json.loads(generated.calls[0][0])
    assert body["reads"] == request_reads and body["merge"] == "atomic"
    assert body["steps"][0]["reads"][0]["kind"] == "collection"
    assert body["steps"][0]["intent"] == "place title"
    assert body["steps"][0]["tags"] == ["title"]


def test_function_reads_each_returned_head_and_recomputes_with_new_keys(connected, monkeypatch):
    tl = opened(connected)
    client, generated, _ = connected
    original = generated.commit_timeline
    sent, evaluations = [], []

    def reply(*args, **kwargs):
        sent.append((copy.deepcopy(args[2]), kwargs["idempotency_key"]))
        if len(sent) < 3:
            advance(generated, len(sent) * 10)
            raise conflict(generated)
        return original(*args, **kwargs)

    monkeypatch.setattr(generated, "commit_timeline", reply)

    def increment(working):
        evaluations.append((working.head, at(working)))
        working.move("parent/clip:a", at(working) + 1)

    tl.commit(increment, idempotency_key="first-evaluation")
    assert [value for _, value in evaluations] == [0, 10, 20]
    assert [head["revision_id"] for head, _ in evaluations] == ["r0", "other-10", "other-20"]
    assert client.reads == ["r0", "r0", "other-10", "other-20"]
    assert len({key for _, key in sent}) == 3
    assert sent[0][1] == "first-evaluation"
    assert [body["base_revision_id"] for body, _ in sent] == ["r0", "other-10", "other-20"]
    assert all(body["merge"] == "atomic" and "reads" not in body for body, _ in sent)
    assert all(body["steps"][0]["reads"] == [{"kind": "scope", "ref": "timeline", "path": []}]
               for body, _ in sent)
    assert at(tl) == 21


def test_declared_function_reads_allow_fields(connected):
    tl = opened(connected)
    _, generated, _ = connected
    tl.commit(lambda working: working.move("parent/clip:a", 5), reads=[])
    body = json.loads(generated.calls[0][0])
    assert body["merge"] == "fields" and body["reads"] == []
    assert "reads" not in body["steps"][0]


def test_three_evaluation_bound_survives_reopening(connected, monkeypatch):
    tl = opened(connected)
    _, generated, path = connected
    evaluations, sent = [], []

    def refuse(*args, **kwargs):
        sent.append(kwargs["idempotency_key"])
        advance(generated, len(sent))
        raise conflict(generated)

    monkeypatch.setattr(generated, "commit_timeline", refuse)

    def edit(working):
        evaluations.append(at(working))
        working.move("parent/clip:a", at(working) + 1)

    with pytest.raises(CommitConflict):
        tl.commit(edit)
    assert evaluations == [0, 1, 2] and len(set(sent)) == 3
    assert json.loads(path.read_text())["evaluation"]["count"] == 3
    with pytest.raises(CommitConflict):
        opened(connected).commit(edit)
    assert len(evaluations) == len(sent) == 3


@pytest.mark.parametrize("status", ["refused", "invalid"])
def test_definitive_nonconflicts_never_rerun(connected, monkeypatch, status):
    tl = opened(connected)
    _, generated, _ = connected
    evaluations = []
    monkeypatch.setattr(generated, "commit_timeline", lambda *args, **kwargs: (_ for _ in ()).throw(conflict(generated, status=status)))

    def edit(working):
        evaluations.append(1)
        working.move("parent/clip:a", 3)

    with pytest.raises(CommitConflict) as caught:
        tl.commit(edit)
    assert caught.value.failure["details"]["status"] == status
    assert len(evaluations) == 1


@pytest.mark.parametrize("lost_ack", [False, True])
def test_unknown_outcome_retries_exact_request_without_reevaluation(connected, monkeypatch, lost_ack):
    tl = opened(connected)
    _, generated, path = connected
    original = generated.commit_timeline
    evaluations, sent = [], []
    generated.lose_ack = lost_ack

    def send(*args, **kwargs):
        sent.append((copy.deepcopy(args[2]), kwargs["idempotency_key"]))
        if not lost_ack and len(sent) == 1:
            raise ApiError(503, "not_ready", "unknown outcome")
        return original(*args, **kwargs)

    monkeypatch.setattr(generated, "commit_timeline", send)

    def edit(working):
        evaluations.append(1)
        working.move("parent/clip:a", 7)

    with pytest.raises(WorkspaceClientError):
        tl.commit(edit, idempotency_key="stable")
    frozen = json.loads(path.read_text())["flight"]
    reopened = opened(connected)
    reopened.commit(edit)
    assert evaluations == [1]
    assert len(sent) == 2 and sent[0] == sent[1]
    assert sent[1][1] == frozen["key"] == "stable"
    assert len(generated.accepted) == 1 and at(reopened) == 7


def test_failed_ack_persistence_reconciles_without_running_function(connected, monkeypatch):
    tl = opened(connected)
    _, generated, _ = connected
    write = tl.session.outbox.write

    def fail_ack(state):
        if state["flight"] is None and not state["pending"]:
            raise OSError("ack storage unavailable")
        write(state)

    monkeypatch.setattr(tl.session.outbox, "write", fail_ack)
    with pytest.raises(OSError):
        tl.commit(lambda working: working.move("parent/clip:a", 7))
    restarted = opened(connected)
    restarted.commit(lambda working: pytest.fail("accepted function evaluated again"))
    assert generated.calls[0] == generated.calls[1]
    assert len(generated.accepted) == 1 and at(restarted) == 7


def test_dry_run_has_no_history_or_adopted_preview_base_and_next_key_is_fresh(connected):
    tl = opened(connected)
    _, generated, path = connected
    before = copy.deepcopy(tl.bundle)
    initial_head = tl.head
    preview = tl.commit(lambda working: working.move("parent/clip:a", 6), dry_run=True)
    assert preview["receipt"] is None and preview["data"]["status"] == "preview"
    assert tl.bundle == before and tl.head == initial_head
    assert tl._journal == [] and generated.accepted == {} and generated.records == {}
    state = json.loads(path.read_text())
    assert state["base"] == initial_head and state["pending"] == [] and state["flight"] is None
    tl.move("parent/clip:a", 6)
    with pytest.raises(TimelineEditError, match="fresh key"):
        tl.commit("Accept", idempotency_key=generated.calls[0][1])
    tl.commit("Accept")
    assert generated.calls[0][1] != generated.calls[1][1]
    assert len(generated.accepted) == 1 and at(tl) == 6


def test_callback_exception_and_nested_commit_publish_nothing(connected):
    tl = opened(connected)
    _, generated, _ = connected
    before = copy.deepcopy(tl.bundle)

    def edit(working):
        working.move("parent/clip:a", 5)
        raise ValueError("failed computation")

    with pytest.raises(ValueError):
        tl.commit(edit)
    with pytest.raises(TimelineEditError, match="own evaluation"):
        tl.commit(lambda working: working.commit("nested"))
    assert tl.bundle == before and generated.calls == [] and tl._journal == []


def test_missing_g3_emitter_refuses_free_edits_without_publication(connected, monkeypatch):
    tl = opened(connected)
    _, generated, _ = connected
    # Keep the original unavailable-dependency control now that the real
    # emitter is mounted in this branch.  The ordinary G2 bundle intentionally
    # has no verified Runtime document, so allowing the import would exercise a
    # different dependency failure instead of the original refusal boundary.
    monkeypatch.setitem(sys.modules, "astrid.sdk.timeline.emitter", None)
    tl.bundle["parent"]["clips"][0]["at"] = 4
    with pytest.raises(TimelineEditError, match="G3 document emitter"):
        tl.commit("Free edit")
    assert generated.calls == [] and at(tl) == 4


def test_g3_emitter_uses_existing_provider_with_verified_runtime_document(connected):
    client, generated, path = connected
    document = document_fixture(shared=False)
    document.update(project_id="p", timeline_id="t")
    document["parent_revision"]["revision_id"] = "r0"
    generated.bundles = {"r0": bundle_from_document(document)}
    assert "_runtime_document" in generated.bundles["r0"]["source_mapping"]

    tl = timeline.open("p", "t", client=client, outbox_path=path)
    tl.bundle["parent"]["name"] = "Joined film"
    # The existing generated provider compiles only changed child images; keep
    # the fixture's complete closure valid through its real acceptance path.
    tl.bundle["shots"]["chapter-shot"]["payload"]["name"] = "Joined chapter"
    result = tl.commit("Rename film")

    assert result["data"]["status"] == "accepted"
    assert len(generated.calls) == 1
    body = json.loads(generated.calls[0][0])
    assert body["label"] == "Rename film"
    assert body["merge"] == "atomic"
    assert body["commands"][0]["op"] == "doc.patch"
    assert {
        "op": "set", "ref": "parent", "path": ["name"],
        "before": {"state": "present", "value": "Renamed Film"},
        "value": "Joined film",
    } in body["commands"][0]["args"]["changes"]
    assert {
        "op": "set", "ref": "shot-revision:shot-1", "path": ["name"],
        "before": {"state": "present", "value": "Chapter One"},
        "value": "Joined chapter",
    } in body["commands"][0]["args"]["changes"]
    assert body["steps"][0]["label"] == "Edit document"
    assert body["steps"][0]["patch"] == body["commands"][0]["args"]["changes"]
    assert generated.bundles[result["data"]["accepted_revision_id"]]["parent"]["name"] == "Joined film"


def test_g3_emitter_seam_captures_helpers_once(connected, monkeypatch):
    tl = opened(connected)
    _, generated, _ = connected
    calls = []

    def emit(before, after):
        calls.append((before, after))
        return [{"schema_version": 1, "op": "clip.move", "version": "1", "select": "parent/clip:a",
                 "args": {"on": after["parent"]["clips"][0]["at"]}}]

    monkeypatch.setattr(commit_session, "emit_document_commands", emit)
    tl.bundle["parent"]["clips"][0]["at"] = 4
    tl.commit("Free edit")
    assert len(calls) == len(generated.calls) == 1 and at(tl) == 4
    assert calls[0][0]["parent"]["clips"][0]["at"] == 0
    body = json.loads(generated.calls[0][0])
    assert body["merge"] == "atomic" and "reads" not in body


def test_stale_local_handle_cannot_submit_at_another_sessions_base(connected):
    first = opened(connected)
    stale = opened(connected)
    _, generated, _ = connected
    stale.move("parent/clip:a", 6)
    first.move("parent/clip:b", 9).commit("Other handle")
    with pytest.raises(TimelineEditError, match="base changed"):
        stale.commit("Stale")
    assert len(generated.calls) == 1


def test_unknown_retry_then_conflict_continues_with_persisted_evaluation_count(connected, monkeypatch):
    tl = opened(connected)
    _, generated, path = connected
    original = generated.commit_timeline
    sent, evaluations = [], []

    def send(*args, **kwargs):
        sent.append((copy.deepcopy(args[2]), kwargs["idempotency_key"]))
        if len(sent) == 1:
            advance(generated, 10)
            raise conflict(generated)
        if len(sent) == 2:
            raise ApiError(503, "not_ready", "unknown")
        if len(sent) == 3:
            advance(generated, 20)
            raise conflict(generated)
        return original(*args, **kwargs)

    monkeypatch.setattr(generated, "commit_timeline", send)

    def edit(working):
        evaluations.append(at(working))
        working.move("parent/clip:a", at(working) + 1)

    with pytest.raises(WorkspaceClientError):
        tl.commit(edit)
    assert json.loads(path.read_text())["evaluation"]["count"] == 2
    reopened = opened(connected)
    reopened.commit(edit)
    assert evaluations == [0, 10, 20] and at(reopened) == 21
    assert sent[1] == sent[2]
    assert len({key for _, key in sent}) == 3


def test_unknown_payload_cannot_change_key_or_preview_mode(connected):
    tl = opened(connected)
    _, generated, path = connected
    generated.lose_ack = True
    tl.move("parent/clip:a", 4)
    with pytest.raises(WorkspaceClientError):
        tl.commit("Original", idempotency_key="original")
    frozen = path.read_bytes()
    with pytest.raises(TimelineEditError, match="immutable"):
        tl.commit("Original", idempotency_key="replacement")
    with pytest.raises(TimelineEditError, match="immutable"):
        tl.commit("Original", dry_run=True)
    assert path.read_bytes() == frozen and len(generated.accepted) == 1
    tl.commit("Original")
    assert len(generated.accepted) == 1


def test_conflict_without_verified_current_pair_does_not_rerun(connected, monkeypatch):
    tl = opened(connected)
    _, generated, _ = connected
    evaluations = []

    def refuse(*args, **kwargs):
        raise conflict(generated, current=False)

    monkeypatch.setattr(generated, "commit_timeline", refuse)

    def edit(working):
        evaluations.append(1)
        working.move("parent/clip:a", 4)

    with pytest.raises(TimelineEditError, match="verified publication"):
        tl.commit(edit)
    assert len(evaluations) == 1


def test_label_commit_does_not_reauthor_after_conflict(connected, monkeypatch):
    tl = opened(connected)
    _, generated, path = connected
    sent = []

    def refuse(*args, **kwargs):
        sent.append(kwargs["idempotency_key"])
        advance(generated, 10)
        raise conflict(generated)

    monkeypatch.setattr(generated, "commit_timeline", refuse)
    tl.move("parent/clip:a", 4)
    with pytest.raises(CommitConflict):
        tl.commit("Literal")
    frozen = path.read_bytes()
    with pytest.raises(CommitConflict):
        tl.commit("Literal")
    assert path.read_bytes() == frozen and len(sent) == 1


def test_conflict_replacement_preserves_later_pending_dependents(connected, monkeypatch):
    tl = opened(connected)
    _, generated, path = connected

    def refuse(*args, **kwargs):
        advance(generated, 10)
        raise conflict(generated)

    monkeypatch.setattr(generated, "commit_timeline", refuse)
    tl.move("parent/clip:a", 4)
    with pytest.raises(CommitConflict):
        tl.commit("Literal")
    with tl.session.outbox.locked():
        state = tl.session._state()
        state["pending"].append(copy.deepcopy(state["pending"][0]))
        tl.session.outbox.write(state)
    before = path.read_bytes()
    with pytest.raises(TimelineEditError, match="dependent"):
        tl.session.submit(state["pending"][:1], label="Replacement", steps=[], expected_state=state,
                          base=generated.head)
    assert path.read_bytes() == before
