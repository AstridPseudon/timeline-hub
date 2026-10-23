"""P4's note-04 conflict and bounded callback rerun through real Runtime HTTP."""
from __future__ import annotations

import copy
import json
from typing import Any

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.emitter import emit_document_commands
from tests.editing_conformance import test_native_batch_ingress
from tests.editing_conformance.test_p4_ten_note_v2_runtime import (
    NOTE_PATH_PREFIX,
    _note_values,
    _notes,
    _seed_original,
    _without_notes,
)

pytestmark = pytest.mark.integration
runtime = test_native_batch_ingress.runtime

NOTE_PATH = [*NOTE_PATH_PREFIX, "note-04"]
PEER_VALUE = "Peer reviewer owns this note"
SUFFIX = " — reviewed"


def _set_note(bundle: dict[str, Any], note_id: str, value: str) -> None:
    for clips in (bundle["parent"]["clips"], bundle["parent"]["config"]["clips"]):
        clip = next(row for row in clips if row["id"] == "clip-a")
        clip["app"]["org.example"].setdefault("p4_note", {})[note_id] = value


def _note(bundle: dict[str, Any], note_id: str = "note-04") -> str | None:
    values = []
    for clips in (bundle["parent"]["clips"], bundle["parent"]["config"]["clips"]):
        clip = next(row for row in clips if row["id"] == "clip-a")
        values.append(clip["app"]["org.example"].get("p4_note", {}).get(note_id))
    assert values[0] == values[1]
    return values[0]


def _seed_other_notes(runtime: Any, tmp_path: Any) -> dict[str, Any]:
    """Publish the nine original notes while retaining note-04's absence."""
    opened = timeline.open(
        runtime.project,
        "film",
        client=runtime.client(),
        outbox_path=tmp_path / "nine-note-seed.json",
    )
    for note in _notes():
        if note["id"] == "note-04":
            continue
        before = copy.deepcopy(opened.bundle)
        after = copy.deepcopy(before)
        _set_note(after, note["id"], note["text"])
        commands = emit_document_commands(before, after)
        assert len(commands) == 1
        opened.command(commands[0], label=note["id"], intent=note["text"], tags=["review"], reads=[])
    result = opened.commit("Seed nine review notes", merge="fields", reads=[],
                           idempotency_key="p4-note-nine-seed")
    assert result["data"]["status"] == "accepted"
    return result


def _assert_request(
    body: dict[str, Any], *, runtime: Any, base: dict[str, str], change: dict[str, Any],
) -> None:
    assert body["api_version"] == 1
    assert {key: body[key] for key in (
        "project_id", "timeline_id", "base_revision_id", "base_publication_id",
    )} == {
        "project_id": runtime.project,
        "timeline_id": "film",
        **base,
    }
    assert body["commands"] == [{
        "schema_version": 1,
        "op": "doc.patch",
        "version": "1",
        "select": None,
        "args": {"changes": [change]},
    }]
    assert body["label"] == "append_review_suffix"
    assert body["steps"] == [{
        "id": "step-1",
        "label": "Edit document",
        "intent": "",
        "tags": [],
        "command_ordinals": [0],
        "patch": [change],
        "reads": [{"kind": "scope", "ref": "timeline", "path": []}],
    }]
    assert body["merge"] == "atomic"
    assert "reads" not in body  # omitted reads conservatively become atomic
    assert body["dry_run"] is False
    assert body["source"] == {"via": "python"}


def _assert_success(result: dict[str, Any], body: dict[str, Any]) -> None:
    data = result["data"]
    receipt = result["receipt"]
    assert data["status"] in {"accepted", "merged"}
    assert data["canonical_document"]["schema_version"] == 1
    canonical = data["canonical_document"]
    assert {canonical["project_id"], canonical["timeline_id"]} == {
        body["project_id"], body["timeline_id"],
    }
    assert data["document_digest"] == _digest(canonical)
    assert canonical["parent_revision"]["content_digest"] == _digest(
        canonical["parent_revision"]["payload"]
    )
    assert data["accepted_revision_id"] == canonical["parent_revision"]["revision_id"]
    assert data["accepted_publication_id"] == receipt["receipt_id"]
    assert data["commands"] == body["commands"]
    assert data["steps"] == body["steps"] or (
        len(data["steps"]) == 1
        and data["steps"][0]["id"] == "step-1"
        and data["steps"][0]["command_ordinals"] == [0]
    )
    assert data["merge_mode"] == "atomic"
    assert data["publisher"]
    assert data["provider_version"]
    assert data["compiler_version"]
    assert receipt["command_kind"] == "timeline.commit"
    assert receipt["project_id"] == body["project_id"]
    receipt_data = copy.deepcopy(data)
    receipt_data.pop("accepted_publication_id", None)
    receipt_data.pop("show_command", None)
    assert receipt["result"] == receipt_data
    assert data["status"] == "accepted"
    assert data["rebased_onto"] is None
    assert {
        "canonical_document", "document_digest", "accepted_revision_id", "commands",
        "steps", "merge_mode", "previous_revision_id", "previous_publication_id",
        "rebased_onto", "publisher", "provider_version", "compiler_version",
    } <= data.keys()


def _assert_full_closure(bundle: dict[str, Any], original: dict[str, Any]) -> None:
    assert len(bundle["placements"]) == 2
    canonical = bundle["source_mapping"]["_runtime_document"]
    assert len(canonical["shot_revisions"]) == 1
    assert len(canonical["internal_timeline_revisions"]) == 1
    assert [(row["shot_id"], row["shot_revision_id"])
            for row in canonical["parent_revision"]["payload"]["occurrences"]] == [
        ("chapter-shot", "shot-1"), ("chapter-shot", "shot-1"),
    ]
    physical_shot = canonical["shot_revisions"][0]
    physical_internal = canonical["internal_timeline_revisions"][0]
    assert physical_shot["internal_timeline_revision_id"] == "internal-1"
    assert physical_internal["timeline_id"] == "chapter-1"
    assert physical_shot["payload"]["unknown"] == {"keep": None}
    assert physical_internal["payload"]["unknown"] == [1, 2]
    assert physical_internal["payload"]["source_window"] == {"start": 4, "end": 9}
    parent = canonical["parent_revision"]["payload"]
    clip = next(row for row in parent["clips"] if row["id"] == "clip-a")
    assert clip["app"]["org.example"]["literal"] == "clip-a"
    assert clip["app"]["org.example"]["clear"] is None
    assert parent["config"]["opaque"] == {"timestamp": "authored timestamp", "v": [None, False, 0]}
    assert _without_notes(bundle) == _without_notes(original)


def test_http_note_conflict_reruns_public_function_from_verified_peer_document(runtime, tmp_path):
    seeded = _seed_original(runtime)
    _seed_other_notes(runtime, tmp_path)
    opened = timeline.open(
        runtime.project,
        "film",
        client=runtime.client(),
        outbox_path=tmp_path / "note-rerun-open.json",
    )
    original = copy.deepcopy(opened.bundle)
    expected_notes = {note["id"]: note["text"] for note in _notes() if note["id"] != "note-04"}
    assert _note_values(original) == expected_notes
    assert _note(original) is None
    assert len(original["placements"]) == 2
    original_base = opened.head
    peer = timeline.open(
        runtime.project,
        "film",
        client=runtime.client(),
        outbox_path=tmp_path / "note-rerun-peer.json",
    )
    calls_before = len(runtime.calls)
    evaluations: list[tuple[dict[str, str], str | None]] = []
    peer_result: dict[str, Any] | None = None
    history_after_peer: dict[str, Any] | None = None
    original_note = next(note["text"] for note in _notes() if note["id"] == "note-04")

    def append_review_suffix(working: Any) -> None:
        nonlocal history_after_peer, peer_result
        current = _note(working.bundle)
        evaluations.append((working.head, current))
        if len(evaluations) == 1:
            _set_note(peer.bundle, "note-04", PEER_VALUE)
            peer_result = peer.commit("Peer review note", idempotency_key="p4-note-peer")
            history_after_peer = runtime.history()
        source = current if current is not None else original_note
        _set_note(working.bundle, "note-04", source + SUFFIX)

    result = opened.commit(append_review_suffix, idempotency_key="p4-note-original")
    assert peer_result is not None
    peer_pin = {
        "revision_id": peer_result["data"]["accepted_revision_id"],
        "publication_id": peer_result["receipt"]["receipt_id"],
    }
    assert len(evaluations) == 2
    assert [head for head, _ in evaluations] == [original_base, peer_pin]
    assert [value for _, value in evaluations] == [None, PEER_VALUE]

    outer_calls = runtime.calls[calls_before:]
    assert len(outer_calls) == 3
    assert [call[2] for call in outer_calls] == [200, 409, 200]
    peer_body = json.loads(outer_calls[0][0])
    assert peer_body["base_revision_id"] == original_base["revision_id"]
    assert peer_body["base_publication_id"] == original_base["publication_id"]
    assert peer_body["commands"][0]["args"]["changes"] == [{
        "op": "set", "ref": "parent", "path": NOTE_PATH,
        "before": {"state": "absent"}, "value": PEER_VALUE,
    }]
    first_body = json.loads(outer_calls[1][0])
    retry_body = json.loads(outer_calls[2][0])
    first_change = {
        "op": "set", "ref": "parent", "path": NOTE_PATH,
        "before": {"state": "absent"},
        "value": _notes()[3]["text"] + SUFFIX,
    }
    retry_change = {
        "op": "set", "ref": "parent", "path": NOTE_PATH,
        "before": {"state": "present", "value": PEER_VALUE},
        "value": PEER_VALUE + SUFFIX,
    }
    _assert_request(first_body, runtime=runtime, base=original_base, change=first_change)
    _assert_request(retry_body, runtime=runtime, base=peer_pin, change=retry_change)
    assert outer_calls[1][1] == "p4-note-original"
    assert outer_calls[2][1] != outer_calls[1][1]

    conflict = outer_calls[1][3]
    assert conflict["code"] == "conflict"
    details = conflict["details"]
    assert {
        "status", "reason", "code", "path", "hint", "suggested_command", "base", "current",
        "conflicts",
    } <= details.keys()
    assert details["status"] == "conflict"
    assert details["reason"] == "atomic_scope_changed"
    assert details["code"] == "atomic_scope_changed"
    assert details["path"] == NOTE_PATH
    assert details["current"] == peer_pin
    assert details["base"] == original_base
    assert not conflict.get("receipt")

    _assert_success(result, retry_body)
    data = result["data"]
    assert opened.head == {
        "revision_id": data["accepted_revision_id"],
        "publication_id": result["receipt"]["receipt_id"],
    }
    landed = bundle_from_document(data["canonical_document"])
    assert _note_values(landed) == {**expected_notes, "note-04": PEER_VALUE + SUFFIX}
    _assert_full_closure(landed, original)
    assert len(landed["shots"]) == len(original["shots"]) == 2
    assert landed["parent"]["config"]["opaque"] == original["parent"]["config"]["opaque"]

    assert history_after_peer is not None
    final_history = runtime.history()
    assert len(final_history["items"]) == len(history_after_peer["items"]) + 1
    stored = next(item for item in final_history["items"]
                  if item["publication_id"] == result["receipt"]["receipt_id"])
    assert stored["label"] == "append_review_suffix"
    assert stored["publisher"] == data["publisher"]
    assert stored["merge_mode"] == "atomic"
    assert stored["steps"] == data["steps"]
    assert stored["records"]["steps"] == data["steps"]
    record = stored["records"]["commands"][0]
    assert {"writes", "reads", "selections", "bindings", "created", "dependencies", "derived_writes"} <= record.keys()
    assert record["writes"] and record["bindings"] and record["dependencies"]
    assert data["steps"][0]["patch"] == [retry_change]
    assert data["steps"][0]["dependencies"]
    assert {"kind": "scope", "ref": "timeline", "path": []} in data["steps"][0]["dependencies"]

    runtime.restart()
    reloaded = timeline.open(
        runtime.project,
        "film",
        client=runtime.client(),
        outbox_path=tmp_path / "note-rerun-reloaded.json",
    )
    assert _note_values(reloaded.bundle) == {**expected_notes, "note-04": PEER_VALUE + SUFFIX}
    _assert_full_closure(reloaded.bundle, original)
    state = json.loads(reloaded.session.outbox.path.read_text(encoding="utf-8"))
    assert state["pending"] == [] and state["flight"] is None
    assert seeded["receipt"]["receipt_id"]
