"""P4's original ten-note case through Runtime's normal v2 HTTP boundary.

The test is source preparation for the compatible G3/R2 client and Runtime
join.  It deliberately uses the existing daemon fixture and generated
transport; no transport or provider is substituted here.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, cast

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.emitter import emit_document_commands
from tests.editing_conformance import test_native_batch_ingress
from tests.helpers.trusted_seed import seed_trusted_parent
from tests.sdk.test_timeline_commit_provider_document import document_fixture

pytestmark = pytest.mark.integration
runtime = test_native_batch_ingress.runtime

ROOT = Path(__file__).parents[1]
CASES = ROOT / "sdk" / "fixtures" / "p4_commit_cases" / "cases.json"
NOTE_PATH_PREFIX = ["clips", "id:clip-a", "app", "org.example", "p4_note"]


def _case() -> dict[str, Any]:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    return next(case for case in data["cases"] if case["id"] == "ten-notes-one-commit")


def _notes() -> list[dict[str, Any]]:
    return _case()["notes"]


def _seed_original(runtime: Any) -> dict[str, Any]:
    """Install the original shared fixture before acceptance observation.

    The note namespace is an isolated empty-container genesis setup: the
    original fixture has no note keys, while doc.patch requires the parent
    object to exist before setting each independently addressed child.
    """
    source = document_fixture(shared=True)
    source["project_id"] = runtime.project
    source["timeline_id"] = "film"
    source["parent_revision"]["revision_id"] = "p4-ten-note-baseline"
    payload = source["parent_revision"]["payload"]
    for clips in (payload["clips"], payload["config"]["clips"]):
        clip = next(row for row in clips if row["id"] == "clip-a")
        clip["app"]["org.example"]["p4_note"] = {}
    source["parent_revision"]["content_digest"] = _digest(payload)
    publication = {
        "project_id": runtime.project,
        "timeline_id": "film",
        "expected_head": None,
        "parent_revision_id": source["parent_revision"]["revision_id"],
        "parent_composition": payload,
        "shot_revisions": source["shot_revisions"],
        "internal_timeline_revisions": source["internal_timeline_revisions"],
    }
    seeded = seed_trusted_parent(
        runtime.service(), publication, idempotency_key="p4-ten-note-baseline"
    )
    runtime.restart()
    return seeded


def _note_values(bundle: dict[str, Any]) -> dict[str, Any]:
    values = []
    for clips in (bundle["parent"]["clips"], bundle["parent"]["config"]["clips"]):
        clip = next(row for row in clips if row["id"] == "clip-a")
        values.append(copy.deepcopy(clip["app"]["org.example"].get("p4_note", {})))
    assert values[0] == values[1]
    return values[0]


def _without_notes(bundle: dict[str, Any]) -> dict[str, Any]:
    """Keep every authored field and closure image except the tested namespace."""
    value = {
        key: copy.deepcopy(bundle[key])
        for key in ("parent", "base_parent_payload", "placements", "shots")
    }
    for parent_key in ("parent", "base_parent_payload"):
        parent = value[parent_key]
        for clips in (parent["clips"], parent["config"]["clips"]):
            clip = next(row for row in clips if row["id"] == "clip-a")
            clip["app"]["org.example"].pop("p4_note", None)
    return value


def _assert_step_patch(step: dict[str, Any], note: dict[str, Any]) -> None:
    assert step["id"] == f"step-{note['ordinal'] + 1}"
    assert step["label"] == note["id"]
    assert step["intent"] == note["text"]
    assert step["tags"] == ["review"]
    assert step["command_ordinals"] == [note["ordinal"]]
    assert len(step["patch"]) == 1
    change = step["patch"][0]
    assert change == {
        "op": "set",
        "ref": "parent",
        "path": [*NOTE_PATH_PREFIX, note["id"]],
        "before": {"state": "absent"},
        "value": note["text"],
    }
    assert step.get("dependencies")


def _run_cli(runtime: Any, capsys: Any, *args: str) -> tuple[int, dict[str, Any]]:
    from astrid.packs.timeline.cli import build_parser

    parsed = build_parser(runtime.client()).parse_args([
        *args, "--project", runtime.project, "--json",
    ])
    code = parsed.handler(parsed)
    return code, json.loads(capsys.readouterr().out)


def test_http_ten_note_commit_per_step_inverse_and_redo(runtime, tmp_path, capsys):
    seeded = _seed_original(runtime)
    opened = timeline.open(
        runtime.project, "film", client=runtime.client(),
        outbox_path=tmp_path / "ten-note-open.json",
    )
    original = copy.deepcopy(opened.bundle)
    assert _note_values(original) == {}
    assert len(original["placements"]) == 2
    assert original["placements"][0]["shot_id"] == original["placements"][1]["shot_id"]
    assert next(row for row in original["parent"]["clips"] if row["id"] == "clip-b")["at"] == 5

    for note in _notes():
        before = copy.deepcopy(opened.bundle)
        after = copy.deepcopy(before)
        for clips in (after["parent"]["clips"], after["parent"]["config"]["clips"]):
            clip = next(row for row in clips if row["id"] == "clip-a")
            clip["app"]["org.example"]["p4_note"][note["id"]] = note["text"]
        commands = emit_document_commands(before, after)
        assert len(commands) == 1
        assert commands[0]["args"]["changes"] == [{
            "op": "set", "ref": "parent", "path": [*NOTE_PATH_PREFIX, note["id"]],
            "before": {"state": "absent"}, "value": note["text"],
        }]
        opened.command(
            commands[0], label=note["id"], intent=note["text"], tags=["review"], reads=[]
        )

    result = opened.commit("Add ten review notes", merge="fields", reads=[],
                           idempotency_key="p4-ten-note-commit")
    data = result["data"]
    receipt = result["receipt"]
    assert data["status"] == "accepted"
    assert len(runtime.calls) == 1
    request = json.loads(runtime.calls[0][0])
    assert runtime.calls[0][1] == "p4-ten-note-commit"
    assert request["api_version"] == 1
    assert {key: request[key] for key in (
        "project_id", "timeline_id", "base_revision_id", "base_publication_id",
    )} == {
        "project_id": runtime.project,
        "timeline_id": "film",
        "base_revision_id": original["base_parent"]["revision_id"],
        "base_publication_id": seeded["receipt"]["receipt_id"],
    }
    assert len(request["commands"]) == len(request["steps"]) == 10
    assert request["label"] == "Add ten review notes"
    assert request["merge"] == "fields"
    assert request["reads"] == []
    assert request["dry_run"] is False
    assert request["source"] == {"via": "python"}
    for command, step, note in zip(request["commands"], request["steps"], _notes()):
        assert command["op"] == "doc.patch"
        assert step == {
            "id": f"step-{note['ordinal'] + 1}", "label": note["id"], "intent": note["text"],
            "tags": ["review"], "command_ordinals": [note["ordinal"]],
            "patch": command["args"]["changes"], "reads": [],
        }

    assert data["merge_mode"] == "fields"
    for key in (
        "canonical_document", "document_digest", "accepted_revision_id", "commands",
        "id_map", "steps", "merge_mode", "previous_revision_id",
        "previous_publication_id", "rebased_onto", "publisher",
        "provider_version", "compiler_version",
    ):
        assert key in data
    assert data["id_map"] == {}
    assert data["rebased_onto"] is None
    assert data["publisher"]
    assert data["commands"] == request["commands"]
    assert len(data["steps"]) == 10
    for step, note in zip(data["steps"], _notes()):
        _assert_step_patch(step, note)
    assert receipt["receipt_id"]
    assert receipt["command_kind"] == "timeline.commit"
    landed = bundle_from_document(data["canonical_document"])
    assert _note_values(landed) == {note["id"]: note["text"] for note in _notes()}
    assert _without_notes(landed) == _without_notes(original)

    show_code, shown = _run_cli(
        runtime, capsys, "show", "film", "--published",
        "--revision-id", data["accepted_revision_id"],
    )
    assert show_code == 0 and shown["ok"] is True
    assert any(row["clip_id"] == "clip-a" and row["start"] == 1 for row in shown["data"]["rows"])
    history_code, history = _run_cli(runtime, capsys, "history", "film", "--limit", "50")
    assert history_code == 0 and history["ok"] is True
    revision = next(
        item for item in history["data"]["revisions"]
        if item["id"] == data["accepted_revision_id"]
    )
    assert revision["message"] == "Add ten review notes"
    raw_history = runtime.client().timelines.history(runtime.project, "film", limit=50)
    assert raw_history.ok
    stored = next(item for item in raw_history.data["items"] if item["publication_id"] == receipt["receipt_id"])
    assert stored["label"] == "Add ten review notes"
    assert stored["publisher"]
    assert stored["merge_mode"] == "fields"
    assert len(stored["steps"]) == 10
    for step, note in zip(stored["steps"], _notes()):
        _assert_step_patch(step, note)

    runtime.restart()
    reloaded = timeline.open(
        runtime.project, "film", client=runtime.client(),
        outbox_path=tmp_path / "ten-note-reloaded.json",
    )
    for note in _notes():
        step_id = f"step-{note['ordinal'] + 1}"
        session = cast(Any, reloaded.session)
        undo = session.undo(
            [receipt["receipt_id"]],
            steps={receipt["receipt_id"]: [step_id]},
            idempotency_key=f"p4-ten-note-undo-{note['id']}",
        )
        undo_data = undo["data"]
        assert undo_data["status"] == "accepted"
        inverse_request = json.loads(runtime.calls[-1][0])
        assert inverse_request["commands"][0]["op"] == "timeline.inverse"
        assert inverse_request["commands"][0]["args"]["steps"] == {
            receipt["receipt_id"]: [step_id]
        }
        undone = bundle_from_document(undo_data["canonical_document"])
        expected = {item["id"]: item["text"] for item in _notes() if item != note}
        assert _note_values(undone) == expected
        assert _without_notes(undone) == _without_notes(original)

        redo = session.undo(
            [undo["receipt"]["receipt_id"]],
            idempotency_key=f"p4-ten-note-redo-{note['id']}",
        )
        assert redo["data"]["status"] == "accepted"
        redone = bundle_from_document(redo["data"]["canonical_document"])
        assert _note_values(redone) == {item["id"]: item["text"] for item in _notes()}
        assert _without_notes(redone) == _without_notes(original)

