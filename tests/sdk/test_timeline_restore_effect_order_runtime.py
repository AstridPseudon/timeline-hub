"""Real Runtime proof for ordinary restore inverse effect order."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline.capture import capture_track_create
from tests.editing_conformance import test_native_batch_ingress

pytestmark = pytest.mark.integration
runtime = test_native_batch_ingress.runtime


def test_id5_public_undo_of_restore_preserves_authenticated_effect_order(runtime, tmp_path):
    project = runtime.project
    outbox = tmp_path / "restore-effect-order-outbox.json"

    def opened():
        return timeline.open(project, "film", client=runtime.client(), outbox_path=outbox)

    def history():
        result = runtime.client().timelines.history(project, "film", limit=200)
        assert result.ok, result.error
        assert result.data["next_cursor"] is None
        return result.data

    def current():
        result = runtime.client().timelines.show(project, "film")
        assert result.ok, result.error
        return result.data

    initial = opened()
    initial.command(capture_track_create(
        initial.bundle, "parent", {"id": "opaque-track", "kind": "visual", "label": "Opaque track",
                                   "app": {"seed": {"opaque": [None, False]}}}),
        label="Create opaque track")
    created = initial.commit("Create opaque track", idempotency_key="create-track")
    assert created["data"]["status"] == "accepted"
    target_document = copy.deepcopy(created["data"]["canonical_document"])
    target_parent = created["data"]["canonical_document"]["parent_revision"]

    changed = opened()
    track = next(row for row in changed.bundle["parent"]["config"]["tracks"]
                 if row["id"] == "opaque-track")
    assert track["app"]["seed"] == {"opaque": [None, False]}
    changed.command({
        "schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
        "args": {"changes": [
            {"op": "set", "ref": "parent",
             "path": ["config", "tracks", "id:opaque-track", "app", "seed", "opaque"],
             "before": {"state": "present", "value": [None, False]},
             "value": [None, False, "changed-seed"]},
            {"op": "set", "ref": "parent",
             "path": ["config", "tracks", "id:opaque-track", "app", "seed", "sibling"],
             "before": {"state": "absent"},
             "value": {"literal": "new-opaque-sibling"}},
        ]}},
        label="Change opaque siblings")
    changed_result = changed.commit("Change opaque siblings", idempotency_key="change-siblings")
    changed_document = copy.deepcopy(changed_result["data"]["canonical_document"])
    assert changed_result["data"]["status"] == "accepted"
    # Only these two opaque leaves change anywhere in the complete closure.
    expected_changed = copy.deepcopy(target_document)
    expected_changed["parent_revision"].update({
        key: changed_document["parent_revision"][key]
        for key in ("revision_id", "content_digest")
    })
    expected_track = next(row for row in expected_changed["parent_revision"]["payload"]["config"]["tracks"]
                          if row["id"] == "opaque-track")
    expected_track["app"]["seed"] = {
        "opaque": [None, False, "changed-seed"],
        "sibling": {"literal": "new-opaque-sibling"},
    }
    assert changed_document == expected_changed
    changed_head = {
        "revision_id": changed_result["data"]["accepted_revision_id"],
        "publication_id": changed_result["receipt"]["receipt_id"],
    }

    restored = opened().session.restore(
        target_parent["revision_id"], target_parent["content_digest"],
        idempotency_key="restore-a")
    assert restored["data"]["status"] == "accepted"
    assert restored["data"]["canonical_document"] == target_document
    restore_publication = restored["receipt"]["receipt_id"]
    restore_wire = next(wire for wire in runtime.calls if wire[1] == "restore-a")
    restore_body = json.loads(restore_wire[0])
    assert restore_wire[2] == 200
    assert (restore_body["api_version"], restore_body["project_id"], restore_body["timeline_id"]) == (
        1, project, "film")
    assert restore_body["dry_run"] is False
    assert ((restore_body["base_revision_id"], restore_body["base_publication_id"])
            == (changed_head["revision_id"], changed_head["publication_id"]))
    assert restore_body["commands"] == [{
        "schema_version": 1, "op": "timeline.restore", "version": "1", "select": None,
        "args": {"revision_id": target_parent["revision_id"],
                 "content_digest": target_parent["content_digest"]},
    }]

    before_undo_page = history()
    before_undo = before_undo_page["items"]
    source_entry = copy.deepcopy(before_undo[-1])
    assert source_entry["publication_id"] == restore_publication
    assert source_entry["previous"] == changed_head
    assert before_undo_page["head"] == {
        "revision_id": target_parent["revision_id"], "publication_id": restore_publication,
    }
    assert source_entry["receipt"]["result"]["canonical_document"] == target_document
    assert source_entry["publisher"] == restored["data"]["publisher"] == "owner"
    assert before_undo[-2]["receipt"]["result"]["canonical_document"] == changed_document
    assert len(source_entry["records"]["commands"]) == len(source_entry["records"]["steps"]) == 1
    assert source_entry["records"]["commands"][0]["command"]["op"] == "timeline.restore"
    source_step = source_entry["records"]["steps"][0]
    source_patch = source_step["patch"]
    # This scene has exactly two leaf effects. C0 §5 reverses their
    # sequence, exchanges tagged before/value, and turns removal into set.
    expected_source = [
        {"op": "set", "ref": "parent",
         "path": ["config", "tracks", "id:opaque-track", "app", "seed", "opaque"],
         "before": {"state": "present", "value": [None, False, "changed-seed"]},
         "value": [None, False]},
        {"op": "remove", "ref": "parent",
         "path": ["config", "tracks", "id:opaque-track", "app", "seed", "sibling"],
         "before": {"state": "present", "value": {"literal": "new-opaque-sibling"}}},
    ]
    expected_inverse = [
        {"op": "set", "ref": "parent",
         "path": ["config", "tracks", "id:opaque-track", "app", "seed", "sibling"],
         "before": {"state": "absent"}, "value": {"literal": "new-opaque-sibling"}},
        {"op": "set", "ref": "parent",
         "path": ["config", "tracks", "id:opaque-track", "app", "seed", "opaque"],
         "before": {"state": "present", "value": [None, False]},
         "value": [None, False, "changed-seed"]},
    ]
    assert source_patch == expected_source
    assert restored["data"]["steps"] == source_entry["records"]["steps"] == source_entry["steps"]
    sibling_paths = [
        (change["ref"], tuple(change["path"][:-1]))
        for change in source_patch
        if change["path"]
    ]
    assert len(sibling_paths) >= 2
    assert len(set(sibling_paths)) == 1
    assert len({tuple(change["path"]) for change in source_patch if change["path"]}) >= 2

    runtime.restart()
    assert history() == before_undo_page
    reloaded = opened()
    assert reloaded.head == before_undo_page["head"]
    restore_head = current()
    preview = reloaded.undo(publications=[restore_publication], dry_run=True,
                            idempotency_key="preview-undo-restore")
    assert preview["receipt"] is None
    assert preview["data"]["would_status"] == "accepted"
    assert preview["data"]["canonical_document"] == changed_document
    assert preview["data"]["steps"][0]["patch"] == expected_inverse
    assert current() == restore_head
    assert history() == before_undo_page

    undone = opened().undo(publications=[restore_publication], idempotency_key="undo-restore")
    after_undo_page = history()
    after_undo = after_undo_page["items"]
    inverse_entry = after_undo[-1]
    inverse_step = inverse_entry["records"]["steps"][0]

    assert undone["data"]["canonical_document"] == changed_document
    assert inverse_step["patch"] == expected_inverse
    assert undone["data"]["steps"] == inverse_entry["records"]["steps"] == inverse_entry["steps"]
    assert [tuple(change["path"]) for change in inverse_step["patch"]] == [
        tuple(change["path"]) for change in reversed(source_patch)]
    assert after_undo[-2] == source_entry
    assert after_undo[:-1] == before_undo
    assert len(after_undo) == len(before_undo) + 1
    assert inverse_entry["records"]["undo_of"] == [restore_publication]
    assert inverse_entry["records"]["undo_steps"] is None
    assert inverse_entry["publisher"] == undone["data"]["publisher"] == source_entry["publisher"]
    assert (after_undo_page["head"]["revision_id"],
            after_undo_page["head"]["publication_id"]) == (
                undone["data"]["accepted_revision_id"], undone["receipt"]["receipt_id"])

    undo_wire = next(wire for wire in runtime.calls if wire[1] == "undo-restore")
    undo_body = json.loads(undo_wire[0])
    assert undo_wire[2] == 200
    assert undo_body["commands"] == [{
        "schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
        "args": {"publications": [restore_publication]},
    }]
    assert (undo_body["base_revision_id"], undo_body["base_publication_id"]) == (
        before_undo_page["head"]["revision_id"], before_undo_page["head"]["publication_id"])
    assert undone["data"]["status"] == "accepted"
    assert undone["data"]["rebased_onto"] is None
    assert (undone["data"]["previous_revision_id"], undone["data"]["previous_publication_id"]) == (
        undo_body["base_revision_id"], undo_body["base_publication_id"])
    runtime.restart()
    retry = runtime.client().timelines.commit(
        project, "film", copy.deepcopy(undo_body), idempotency_key="undo-restore")
    assert retry.ok, retry.error
    retry_envelope = retry.as_dict()
    assert {key: retry_envelope[key] for key in ("data", "receipt")} == undo_wire[3]
    accepted_data = copy.deepcopy(undone["data"])
    assert accepted_data.pop("accepted_publication_id") == retry_envelope["receipt"]["receipt_id"]
    assert accepted_data.pop("show_command") == (
        f"astrid timelines show film --project {project} --published "
        f"--revision-id {undone['data']['accepted_revision_id']}")
    assert retry.data == accepted_data
    assert retry_envelope["receipt"] == undone["receipt"]
    assert runtime.calls[-1][:2] == undo_wire[:2]
    assert history() == after_undo_page
    assert opened().head == after_undo_page["head"]
