from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import shlex
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.timeline.authoring_bundle import (
    compile_authoring_candidate,
    open_authoring_bundle,
    publish_authoring_candidate,
)
from astrid.core.timeline.authoring_feedback import authoring_change_summary, publication_feedback
from astrid.packs.timeline.cli import _configure_diff, _configure_show, _configure_visualize
from astrid.sdk.authoring_remote import AuthoringRemoteError, TargetBoundAuthoringBundle
from astrid.sdk.timeline.document_diff import DocumentDiffError, document_diff_to_commands
from astrid.sdk.timeline_editing import duplicate_authoring_shot, remove_authoring_shot
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.timeline.test_authoring_bundle import AUDIO, NEW, OLD, _closure, _digest


def bundle(*, images=1, shared=False):
    parent, shots, internals = _closure(shared=shared)
    internal = internals[0]["payload"]
    payload = shots[0]["payload"]
    for index in range(2, images + 1):
        clip = copy.deepcopy(internal["clips"][0])
        clip.update(id=f"picture-{index}", at=index - 1)
        internal["clips"].append(clip)
    internals[0]["content_digest"] = _digest(internal)
    shots[0]["content_digest"] = _digest(payload)
    return open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)


def replace_images(work):
    shot = next(iter(work["shots"].values()))
    shot["internal_timeline"]["registry"]["assets"]["old-picture"]["media_id"] = NEW
    shot["payload"]["items"][0]["media_id"] = NEW
    return shot


class Writer:
    def __init__(self):
        self.calls = []

    def publish_parent_composition(self, project, timeline, publication, **kwargs):
        self.calls.append(publication)
        return {"data": {"new_head": "saved-revision", "old_head": "parent-1"}}


def publish(work, *, imports=()):
    writer = Writer()
    result = publish_authoring_candidate(work, writer, idempotency_key="feedback-test", media_imports=imports)
    assert len(writer.calls) == 1
    assert result["publication"]["data"]["new_head"] == "saved-revision"
    return result


def test_three_changed_image_selections_with_no_catalog_imports():
    work = bundle(images=3)
    replace_images(work)
    result = publish(work)
    assert result["update"].startswith("Updated 3 image selections.")
    assert result["summary"]["media_selections"]["image"] == {
        "updated": 3, "replaced": 3, "added": 0, "removed": 0,
    }
    assert result["summary"]["catalog_media"] == {"imported": 0, "reused": 0}
    assert result["summary"]["new_head"] == "saved-revision"


def test_saved_pair_action_quotes_receipt_ids_and_parses_exact_supported_flags():
    feedback = publication_feedback(
        authoring_change_summary(bundle()),
        {"old_head": "old head; $(no)", "new_head": "new 'head'"},
        project_id="project 'one'", timeline_id="timeline; two",
    )
    action = next(row for row in feedback["next_actions"]
                  if row["scope"] == "saved_revision_pair")
    parser = argparse.ArgumentParser()
    _configure_diff(parser)
    parsed = parser.parse_args(shlex.split(action["command"])[5:])
    assert parsed.project == "project 'one'"
    assert parsed.ref == "timeline; two"
    assert parsed.from_revision == "old head; $(no)"
    assert parsed.to_revision == "new 'head'"
    assert parsed.format == "readable"


def test_receipt_without_old_head_does_not_fabricate_saved_diff_pair():
    feedback = publication_feedback(authoring_change_summary(bundle()),
                                    {"new_head": "saved"}, project_id="project-1", timeline_id="main")
    assert all(row["scope"] != "saved_revision_pair" for row in feedback["next_actions"])
    assert "--from-revision" not in feedback["update"]


def test_registry_payload_and_selector_mirrors_count_one_selection():
    work = bundle()
    shot = replace_images(work)
    timeline = shot["internal_timeline"]
    timeline["registry"]["assets"]["new-picture"] = timeline["registry"]["assets"].pop("old-picture")
    timeline["clips"][0]["asset"] = "new-picture"
    result = publish(work)
    assert result["summary"]["media_selections"]["image"]["updated"] == 1
    assert result["update"].startswith("Updated 1 image selection.")


def test_new_ids_are_additions_and_array_shifts_do_not_replace_surviving_clips():
    work = bundle()
    shot = next(iter(work["shots"].values()))
    timeline = shot["internal_timeline"]
    previous = timeline["clips"].pop(0)
    timeline["registry"]["assets"]["new-picture"] = {"media_id": NEW, "type": "image"}
    for index in range(3):
        clip = dict(previous, id=f"new-{index}", asset="new-picture", at=index, hold=1)
        timeline["clips"].insert(index, clip)
    shot["payload"]["items"][0]["media_id"] = NEW
    result = publish(work)
    assert result["update"].startswith("Updated 3 image selections. Removed 1 image selection.")
    assert result["summary"]["media_selections"]["image"] == {
        "updated": 3, "replaced": 0, "added": 3, "removed": 1,
    }
    assert result["summary"]["media_selections"]["audio"]["updated"] == 0


def test_alias_equivalence_and_clip_reorder_do_not_claim_new_images():
    work = bundle()
    timeline = next(iter(work["shots"].values()))["internal_timeline"]
    timeline["registry"]["assets"]["alias"] = {"media_id": OLD.removeprefix("sha256:"), "type": "image"}
    timeline["clips"][0]["asset"] = "alias"
    timeline["clips"].reverse()
    result = publish(work)
    assert result["summary"]["media_selections"]["image"]["updated"] == 0
    assert result["update"].startswith("Other properties changed.")


def test_timing_fields_on_one_clip_count_one_adjustment_and_no_images():
    work = bundle()
    clip = next(iter(work["shots"].values()))["internal_timeline"]["clips"][0]
    clip.update(at=0.01, hold=0.99)
    result = publish(work)
    assert result["update"].startswith("Adjusted timing on 1 clip.")
    assert result["summary"]["timing_changes"] == {"clips": 1, "occurrences": 0}
    assert result["summary"]["media_selections"]["image"]["updated"] == 0


def test_document_view_adapter_emits_native_command_for_explicit_parent_timing():
    work = bundle()
    base = copy.deepcopy(work)
    work["parent"]["clips"][0]["at"] = 4
    work["parent"]["config"]["clips"][0]["at"] = 4

    native = document_diff_to_commands(work, base)

    assert [command["op"] for command in native["commands"]] == ["clip.move"]
    assert native["commands"][0]["select"] == "parent/clip:direct"


@pytest.mark.parametrize("field", ["params", "at", "from", "to"])
def test_document_view_adapter_refuses_null_to_absent_clip_fields_without_dropping_draft(field):
    work = bundle(shared=False)
    base = copy.deepcopy(work)
    shot = next(iter(work["shots"].values()))
    base_shot = next(iter(base["shots"].values()))
    for timeline in (base_shot["internal_timeline"], shot["base_internal_timeline"],
                     shot["internal_timeline"]):
        timeline["clips"][0][field] = None
    shot["internal_timeline"]["clips"][0].pop(field)

    before = copy.deepcopy(work)
    with pytest.raises(DocumentDiffError, match="null/absence"):
        document_diff_to_commands(work, base)
    assert work == before


@pytest.mark.parametrize("field", ["layout", "effects", "audio", "opaque_timeline"])
def test_document_view_adapter_refuses_deleting_held_internal_fields_without_dropping_draft(field):
    work = bundle(shared=False)
    base = copy.deepcopy(work)
    shot = next(iter(work["shots"].values()))
    shot["internal_timeline"].pop(field)

    before = copy.deepcopy(work)
    with pytest.raises(DocumentDiffError, match=f"internal field {field!r}"):
        document_diff_to_commands(work, base)
    assert work == before


def test_document_view_adapter_refuses_an_undeclared_null_param_without_dropping_draft():
    work = bundle()
    base = copy.deepcopy(work)
    shot = next(iter(work["shots"].values()))
    base_shot = next(iter(base["shots"].values()))
    for timeline in (base_shot["internal_timeline"], shot["base_internal_timeline"],
                     shot["internal_timeline"]):
        timeline["clips"][0]["clipType"] = "am-type"
    shot["internal_timeline"]["clips"][0]["params"] = {"null": None}

    before = copy.deepcopy(work)
    with pytest.raises(DocumentDiffError, match="undeclared params"):
        document_diff_to_commands(work, base)
    assert work == before


def test_document_view_adapter_refuses_setting_an_absent_field_to_null_without_dropping_draft():
    work = bundle()
    base = copy.deepcopy(work)
    for parent in (base["parent"], work["base_parent_payload"], work["parent"]):
        for rows in (parent["clips"], parent["config"]["clips"]):
            rows[0].pop("hold", None)
    work["parent"]["clips"][0]["hold"] = None
    work["parent"]["config"]["clips"][0]["hold"] = None

    before = copy.deepcopy(work)
    with pytest.raises(DocumentDiffError, match="native command is held"):
        document_diff_to_commands(work, base)
    assert work == before


@pytest.mark.parametrize("scope", ["parent", "child"])
def test_document_view_adapter_clears_present_null_hold_without_zero_command(scope):
    work = bundle()
    base = copy.deepcopy(work)
    if scope == "parent":
        for parent in (base["parent"], work["base_parent_payload"], work["parent"]):
            for rows in (parent["clips"], parent["config"]["clips"]):
                rows[0].update({"from": 0, "to": 1, "hold": None})
        for rows in (work["parent"]["clips"], work["parent"]["config"]["clips"]):
            rows[0].pop("hold")
    else:
        shot_id = next(iter(work["shots"]))
        base_shot = base["shots"][shot_id]
        shot = work["shots"][shot_id]
        for timeline in (base_shot["internal_timeline"], shot["base_internal_timeline"],
                         shot["internal_timeline"]):
            timeline["clips"][0].update({"from": 0, "to": 1, "hold": None})
        shot["internal_timeline"]["clips"][0].pop("hold")
        # The native child-hold command is intentionally limited to a simple
        # translation-only occurrence; keep this fixture inside that contract.
        for bundle_value in (base, work):
            bundle_value["placements"][0].update(source_offset=0, speed=1)
            bundle_value["base_placements"]["occ-1"].update(source_offset=0, speed=1)

    native = document_diff_to_commands(work, base)

    assert [command["op"] for command in native["commands"]] == ["clip.set"]
    assert native["commands"][0]["args"] == {"values": {}, "clear": ["hold"]}
    if scope == "parent":
        assert "hold" not in native["bundle"]["parent"]["clips"][0]
        assert "hold" not in native["bundle"]["parent"]["config"]["clips"][0]
    else:
        assert "hold" not in native["bundle"]["shots"][shot_id]["internal_timeline"]["clips"][0]


def test_document_view_adapter_clears_a_present_nonnull_param():
    work = bundle()
    base = copy.deepcopy(work)
    shot = next(iter(work["shots"].values()))
    base_shot = next(iter(base["shots"].values()))
    for timeline in (base_shot["internal_timeline"], shot["base_internal_timeline"],
                     shot["internal_timeline"]):
        timeline["clips"][0]["clipType"] = "am-type"
        timeline["clips"][0]["params"] = {"text": "hello"}
    shot["internal_timeline"]["clips"][0]["params"] = {}

    native = document_diff_to_commands(work, base)

    assert [command["op"] for command in native["commands"]] == ["clip.set-params"]
    assert native["commands"][0]["args"] == {"values": {}, "clear": ["text"]}
    assert native["bundle"]["shots"][shot["shot_id"]]["internal_timeline"]["clips"][0][
        "params"] == {}


def test_document_view_adapter_validates_parent_track_rename_against_captured_result():
    work = bundle()
    base = copy.deepcopy(work)
    work["parent"]["config"]["tracks"][0]["label"] = "Renamed"

    native = document_diff_to_commands(work, base)

    assert [command["op"] for command in native["commands"]] == ["track.set"]
    assert native["commands"][0]["args"] == {"values": {"label": "Renamed"}, "clear": []}
    assert native["bundle"]["parent"]["config"]["tracks"][0]["label"] == "Renamed"


def test_document_view_adapter_holds_narration_and_same_alias_media_changes():
    work = bundle()
    base = copy.deepcopy(work)
    shot = next(iter(work["shots"].values()))
    shot["payload"]["text_bindings"][0]["text"] = "changed"
    with pytest.raises(DocumentDiffError, match="payload/narration"):
        document_diff_to_commands(work, base)

    work = bundle()
    shot = next(iter(work["shots"].values()))
    shot["internal_timeline"]["registry"]["assets"]["old-picture"]["media_id"] = NEW
    with pytest.raises(DocumentDiffError, match="exact Runtime media selection"):
        document_diff_to_commands(work, bundle())


def test_document_view_adapter_requires_the_exact_pinned_base():
    work = bundle()
    base = bundle()
    base["parent"]["clips"][0]["at"] = 9

    with pytest.raises(DocumentDiffError, match="exact pinned parent base"):
        document_diff_to_commands(work, base)


@pytest.mark.parametrize("scope,remove,move", [
    ("parent", False, False), ("config", False, False),
    ("parent", True, False), ("config", True, False), ("parent", False, True),
])
def test_document_view_adapter_holds_opaque_presence_atomically(scope, remove, move):
    parent, shots, internals = _closure(shared=False)
    payload = parent["payload"]
    if remove:
        (payload["config"] if scope == "config" else payload)["presence_probe"] = None
    parent["content_digest"] = _digest(payload)
    work = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    base = copy.deepcopy(work)
    target = work["parent"]["config"] if scope == "config" else work["parent"]
    if remove:
        target.pop("presence_probe")
    else:
        target["presence_probe"] = None
    if move:
        for rows in (work["parent"]["clips"], work["parent"]["config"]["clips"]):
            rows[0]["at"] = 4
    compile_authoring_candidate(work)
    before, pinned = copy.deepcopy(work), copy.deepcopy(base)
    for defer_media in (True, False):
        with pytest.raises(DocumentDiffError, match="held by the document view"):
            document_diff_to_commands(work, base, defer_media=defer_media)
        assert work == before and base == pinned


@pytest.mark.parametrize("container", ["parent-clips", "config-clips", "tracks", "config", "child-clips"])
@pytest.mark.parametrize("remove", [True, False])
def test_document_view_adapter_holds_empty_container_presence(container, remove):
    parent, shots, internals = _closure(shared=False)
    payload, internal = parent["payload"], internals[0]["payload"]
    payload["clips"] = []
    payload["config"]["clips"] = []
    if container == "tracks":
        payload["config"]["tracks"] = []
    if container == "config":
        payload["config"] = {}
    if container == "child-clips":
        internal["clips"] = []
    source, key = {
        "parent-clips": (payload, "clips"), "config-clips": (payload["config"], "clips"),
        "tracks": (payload["config"], "tracks"), "config": (payload, "config"),
        "child-clips": (internal, "clips"),
    }[container]
    empty = copy.deepcopy(source[key])
    if not remove:
        source.pop(key)
    parent["content_digest"] = _digest(payload)
    internals[0]["content_digest"] = _digest(internal)
    work = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    base = copy.deepcopy(work)
    target = (next(iter(work["shots"].values()))["internal_timeline"] if container == "child-clips"
              else work["parent"]["config"] if container in {"config-clips", "tracks"} else work["parent"])
    if remove:
        target.pop(key)
    else:
        target[key] = empty
    compile_authoring_candidate(work)
    before, pinned = copy.deepcopy(work), copy.deepcopy(base)
    with pytest.raises(DocumentDiffError, match="container presence"):
        document_diff_to_commands(work, base)
    assert work == before and base == pinned


def test_document_view_adapter_holds_missing_registry_to_null_with_parent_authority():
    parent, shots, internals = _closure(shared=False)
    parent["payload"]["registry"]["assets"].update({
        "old-picture": {"media_id": OLD, "type": "image"},
        "voice": {"media_id": AUDIO, "type": "audio"},
    })
    internals[0]["payload"].pop("registry")
    parent["content_digest"] = _digest(parent["payload"])
    internals[0]["content_digest"] = _digest(internals[0]["payload"])
    work = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    base = copy.deepcopy(work)
    assert document_diff_to_commands(work, base)["commands"] == []
    next(iter(work["shots"].values()))["internal_timeline"]["registry"] = None
    compile_authoring_candidate(work)
    before, pinned = copy.deepcopy(work), copy.deepcopy(base)
    for defer_media in (True, False):
        with pytest.raises(DocumentDiffError, match="registry/media edits are held"):
            document_diff_to_commands(work, base, defer_media=defer_media)
    assert work == before and base == pinned


@pytest.mark.parametrize("field,value", [("asset", "direct"), ("params", None), ("hold", 1),
                                         ("at", 3), ("opaque", None), ("app", {})])
def test_document_view_adapter_holds_mirror_only_field_deletions(field, value):
    parent, shots, internals = _closure(shared=False)
    for rows in (parent["payload"]["clips"], parent["payload"]["config"]["clips"]):
        rows[0][field] = value
    parent["content_digest"] = _digest(parent["payload"])
    work = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    base = copy.deepcopy(work)
    work["parent"]["config"]["clips"][0].pop(field)
    before, pinned = copy.deepcopy(work), copy.deepcopy(base)
    with pytest.raises(DocumentDiffError, match="native command result"):
        document_diff_to_commands(work, base)
    assert work == before and base == pinned


def test_document_view_adapter_refuses_candidate_only_mirror_field_matching_move_result():
    work = bundle()
    base = copy.deepcopy(work)
    work["parent"]["clips"][0]["at"] = 4
    mirror = work["parent"]["config"]["clips"][0]
    mirror["at"] = 4
    mirror["app"] = {"astrid": {"fixed_start": True, "for": 1.0}}

    before, pinned = copy.deepcopy(work), copy.deepcopy(base)
    with pytest.raises(DocumentDiffError, match="candidate-only"):
        document_diff_to_commands(work, base)
    assert work == before and base == pinned


def test_document_view_adapter_accepts_identity_map_spelling_and_new_native_move_fields():
    work = bundle()
    base = copy.deepcopy(work)
    for timeline in (work["parent"], work["parent"]["config"],
                     next(iter(work["shots"].values()))["internal_timeline"]):
        timeline["clips"] = {row["id"]: row for row in timeline["clips"]}
    config = work["parent"]["config"]
    config["tracks"] = {row["id"]: row for row in config["tracks"]}
    work["parent"]["clips"]["direct"]["at"] = 4
    config["clips"]["direct"]["at"] = 4
    native = document_diff_to_commands(work, base)
    assert [command["op"] for command in native["commands"]] == ["clip.move"]
    result = native["bundle"]["parent"]
    assert result["clips"][0]["at"] == result["config"]["clips"][0]["at"] == 4
    assert "app" in result["clips"][0] and "app" not in base["parent"]["clips"][0]


def test_document_view_adapter_checks_native_media_rebind_and_unrelated_held_edits():
    from astrid.sdk.timeline.commit import _digest, bundle_from_document
    from tests.editing_conformance.test_recipe_occurrence_media import inputs

    document, old, new, verified = inputs()
    parent = document["parent_revision"]
    parent["payload"]["occurrences"] = parent["payload"]["occurrences"][:1]
    parent["content_digest"] = _digest(parent["payload"])
    base = bundle_from_document(document)
    work = copy.deepcopy(base)
    owner = "occurrence:occ-a"
    shot = next(iter(work["shots"].values()))
    alias = old["asset"]
    new = {**new, "asset": alias}
    verified = [{**row, "selection": {**row["selection"], "asset": alias}} for row in verified]
    shot["internal_timeline"]["registry"]["assets"][alias].update(
        media_id=new["object_id"], generationId=new["generation_id"], variantId=new["variant_id"])
    shot["payload"]["items"][0]["media_id"] = new["object_id"]
    assert document_diff_to_commands(work, base, defer_media=True)["commands"] == []
    selections = {(owner, alias): {"old": old, "new": new}}
    result = document_diff_to_commands(work, base, media_selections=selections, verified_media=verified)
    assert [command["op"] for command in result["commands"]] == ["occurrence.swap-media"]
    replayed = result["bundle"]["shots"][shot["shot_id"]]
    assert replayed["internal_timeline"]["registry"] == shot["internal_timeline"]["registry"]
    assert replayed["payload"] == shot["payload"]
    # Both pre-import validation and final replay must retain unrelated presence.
    shot["internal_timeline"]["registry"]["opaque"] = None
    before, pinned = copy.deepcopy(work), copy.deepcopy(base)
    for kwargs in ({"defer_media": True}, {"media_selections": selections, "verified_media": verified}):
        with pytest.raises(DocumentDiffError, match="registry"):
            document_diff_to_commands(work, base, **kwargs)
    assert work == before and base == pinned


@pytest.mark.parametrize("operation", ["trim", "params", "label-clear"])
def test_document_view_adapter_preserves_native_writes_and_literal_script_slots(operation):
    parent, shots, internals = _closure(shared=False)
    parent["payload"]["registry"]["assets"]["direct"].update(type="video", duration=2)
    for rows in (parent["payload"]["clips"], parent["payload"]["config"]["clips"]):
        rows[0].update({"from": 0, "to": 1})
    parent["payload"]["config"]["tracks"][0]["label"] = "Picture"
    internals[0]["payload"]["clips"][0].update(clipType="am-type", params={"text": "hello"})
    shots[0]["payload"].update(script=None, slot="hello")
    for image in (parent, shots[0], internals[0]):
        image["content_digest"] = _digest(image["payload"])
    work = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=internals)
    base = copy.deepcopy(work)
    shot = next(iter(work["shots"].values()))
    if operation == "trim":
        for rows in (work["parent"]["clips"], work["parent"]["config"]["clips"]):
            rows[0].update({"from": .25, "to": 1.25})
        expected_op = "clip.trim"
    elif operation == "params":
        shot["internal_timeline"]["clips"][0]["params"]["text"] = "ordinary value"
        expected_op = "clip.set-params"
    else:
        work["parent"]["config"]["tracks"][0].pop("label")
        expected_op = "track.set"
    result = document_diff_to_commands(work, base)
    assert [command["op"] for command in result["commands"]] == [expected_op]
    replayed = result["bundle"]
    if operation == "trim":
        for rows in (replayed["parent"]["clips"], replayed["parent"]["config"]["clips"]):
            assert (rows[0]["from"], rows[0]["to"]) == (.25, 1.25)
    elif operation == "params":
        assert replayed["shots"][shot["shot_id"]]["internal_timeline"]["clips"][0]["params"] == {
            "text": "ordinary value"}
    else:
        assert "label" not in replayed["parent"]["config"]["tracks"][0]
    assert replayed["shots"][shot["shot_id"]]["payload"] == shot["payload"]
    assert shot["payload"]["script"] is None and shot["payload"]["slot"] == "hello"


def test_unchanged_checkout_reports_no_authored_changes_and_unknown_imports_by_default():
    result = publish_authoring_candidate(bundle(), Writer(), idempotency_key="noop")
    assert result["update"].startswith("No authored changes. Saved revision saved-revision.")
    assert result["summary"]["authored_change_count"] == 0
    assert result["summary"]["catalog_media"] is None


def test_catalog_imports_and_reuse_are_separate_from_selection_counts():
    work = bundle()
    replace_images(work)
    result = publish(work, imports=[{"asset_id": NEW}, {"asset_id": OLD, "reused": True}])
    assert result["summary"]["catalog_media"] == {"imported": 1, "reused": 1}
    assert result["summary"]["media_selections"]["image"]["updated"] == 1
    assert "Imported 1 catalog media item. Reused 1 catalog media item." in result["update"]


def test_removed_shot_without_its_baseline_does_not_claim_noop_or_invent_media_counts():
    work = bundle()
    remove_authoring_shot(work, work["placements"][0]["shot_id"])
    result = publish(work)
    assert result["summary"]["occurrence_changes"]["removed"] == 1
    assert result["summary"]["unavailable_selection_baselines"] == ["occ-1"]
    assert "Removed 1 shot occurrence." in result["update"]
    assert "No authored changes" not in result["update"]
    assert "Selection counts are partial" in result["update"]


def test_repeated_occurrences_count_independent_selections_and_skip_unplaced_shots():
    work = bundle(shared=True)
    for shot in work["shots"].values():
        shot["internal_timeline"]["registry"]["assets"]["old-picture"]["media_id"] = NEW
        shot["payload"]["items"][0]["media_id"] = NEW
    result = publish(work)
    assert result["summary"]["media_selections"]["image"]["updated"] == 2
    work = bundle()
    source_id = work["placements"][0]["shot_id"]
    duplicate_authoring_shot(work, source_id, new_shot_id="unplaced", occurrence_id="unplaced-occ")
    work["placements"].pop()
    orphan = work["shots"]["unplaced"]
    orphan["internal_timeline"]["registry"]["assets"]["old-picture"]["media_id"] = NEW
    assert publish(work)["summary"]["media_selections"]["image"]["updated"] == 0


def test_next_actions_quote_authoritative_scope_and_parse_supported_options():
    work = bundle()
    work["project_id"] = "project '$(touch example)' `quoted`"
    work["timeline_id"] = 'timeline "special"; echo example'
    result = publish(work)
    current_actions = [action for action in result["next_actions"] if action["scope"] == "current_head"]
    for action, configure in zip(current_actions, (_configure_show, _configure_visualize)):
        argv = shlex.split(action["command"])
        assert argv[:4] == ["python3", "-m", "astrid", "timelines"]
        parser = argparse.ArgumentParser()
        configure(parser)
        parsed = parser.parse_args(argv[5:])
        assert parsed.project == work["project_id"]
        assert getattr(parsed, "ref", getattr(parsed, "timeline_ref", None)) == work["timeline_id"]
        assert action["scope"] == "current_head"
    assert "Use timelines show to view the timeline" in result["update"]
    assert "Use timelines visualize to visualize" in result["update"]
    assert "--mode inputs" in result["update"]


def test_document_publish_holds_move_with_presence_edit_before_import_and_keeps_file(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[2] / "astrid/packs/rendering/docs/scripts/timeline_document.py"
    spec = importlib.util.spec_from_file_location("timeline_document_presence_test", script)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    base = bundle()
    base["base_parent"]["publication_id"] = "publication-1"
    work = copy.deepcopy(base)
    work["parent"]["presence_probe"] = None
    for rows in (work["parent"]["clips"], work["parent"]["config"]["clips"]):
        rows[0]["at"] = 4
    path = tmp_path / "draft.json"
    source = json.dumps(work)
    path.write_text(source)
    session = SimpleNamespace(
        _state=lambda: {"base": {"revision_id": "parent-1", "publication_id": "publication-1"}},
        _bundle=lambda state: base,
        commit_many=lambda *args, **kwargs: pytest.fail("held draft reached commit"),
    )
    monkeypatch.setattr(helper.AstridClient, "open_from_launcher", lambda **kwargs: nullcontext(object()))
    monkeypatch.setattr(helper, "workspace", lambda: object())
    monkeypatch.setattr(helper.TimelineSession, "open", lambda *args, **kwargs: session)
    monkeypatch.setattr(helper, "import_authoring_media",
                        lambda *args: pytest.fail("held draft reached import"))
    monkeypatch.setattr("sys.argv", [str(script), "publish", "--file", str(path), "--idempotency-key", "held-move"])
    with pytest.raises(RuntimeError, match="document publish is held: parent field 'presence_probe'"):
        helper.main()
    assert path.read_text() == source
    assert not path.with_suffix(".publication.json").exists()
    assert not path.with_suffix(".prepared.json").exists()


def test_document_publish_stdout_and_durable_receipt_contain_shared_feedback(tmp_path, monkeypatch, capsys):
    script = Path(__file__).resolve().parents[2] / "astrid/packs/rendering/docs/scripts/timeline_document.py"
    spec = importlib.util.spec_from_file_location("timeline_document_feedback_test", script)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    work = bundle()
    work["base_parent"]["publication_id"] = "publication-1"
    work["parent"]["clips"][0]["at"] = 4
    work["parent"]["config"]["clips"][0]["at"] = 4
    path = tmp_path / "batch 'one' edit.json"
    source = json.dumps(work)
    path.write_text(source)
    commits = []

    class Session:
        def _state(self):
            return {"base": {"revision_id": "parent-1", "publication_id": "publication-1"}}

        def _bundle(self, _state):
            original = bundle()
            original["base_parent"]["publication_id"] = "publication-1"
            return original

        def commit_many(self, commands, **kwargs):
            commits.append(commands)
            assert [command["op"] for command in commands] == ["clip.move"]
            assert kwargs["idempotency_key"] == "batch-feedback"
            return {"data": {
                "status": "accepted", "accepted_revision_id": "saved-revision",
                "previous_revision_id": "parent-1",
            }}

    client = SimpleNamespace(timelines=SimpleNamespace(history=lambda *args, **kwargs: None))
    monkeypatch.setattr(helper.AstridClient, "open_from_launcher", lambda **kwargs: nullcontext(client))
    monkeypatch.setattr(helper, "workspace", lambda: SimpleNamespace())
    monkeypatch.setattr(helper.TimelineSession, "open", lambda *args, **kwargs: Session())
    monkeypatch.setattr("sys.argv", [str(script), "publish", "--file", str(path), "--idempotency-key", "batch-feedback"])
    helper.main()
    output = json.loads(capsys.readouterr().out)
    saved = json.loads(path.with_suffix(".publication.json").read_text())
    assert output["update"].startswith("Adjusted timing on 1 clip.")
    for field in ("update", "summary", "next_actions"):
        assert output[field] == saved[field]
    assert output["publication"]["data"]["accepted_revision_id"] == "saved-revision"
    assert saved["media_imports"] == []
    assert output["artifacts"] == saved["artifacts"]
    for key, suffix in (("check", ".check.json"), ("prepared", ".prepared.json"), ("publication", ".publication.json")):
        assert output["artifacts"][key] == str(path.with_suffix(suffix))
        assert Path(output["artifacts"][key]).is_file()
    check_action = next(action for action in output["next_actions"] if action["scope"] == "candidate_preflight")
    assert shlex.split(check_action["command"]) == ["python3", "-m", "json.tool", str(path.with_suffix(".check.json"))]
    diff_actions = [action for action in output["next_actions"] if action["scope"] == "saved_revision_pair"]
    assert [action["format"] for action in diff_actions] == ["readable", "details"]
    for diff_action in diff_actions:
        assert diff_action["from_revision"] == "parent-1"
        assert diff_action["to_revision"] == "saved-revision"
        parser = argparse.ArgumentParser()
        _configure_diff(parser)
        parsed = parser.parse_args(shlex.split(diff_action["command"])[5:])
        assert parsed.format == diff_action["format"]
    assert "--from-revision parent-1 --to-revision saved-revision" in output["update"]
    assert path.read_text() == source


def test_target_bound_sdk_forwards_shared_publication_feedback():
    work = bundle()
    replace_images(work)
    writer = Writer()
    client = SimpleNamespace(
        endpoint="http://127.0.0.1:63331",
        list_timelines=lambda *args, **kwargs: ([{"timeline_id": "main"}], None),
        inspect_timeline=lambda *args, **kwargs: {"data": {"is_current_head": True, "revision_id": "parent-1"}},
        get_project_object_location=lambda project, object_id: {"data": {"verified": True, "object_id": object_id}},
        publish_parent_composition=writer.publish_parent_composition,
    )
    target = {"endpoint": client.endpoint, "project_id": "project-1", "timeline_id": "main",
              "head_revision_id": "parent-1", "capabilities": {"edit": {
                  "status": "available", "route": "authoring-bundle validate/commit",
              }}}
    result = TargetBoundAuthoringBundle(client, target).publish(work, idempotency_key="sdk-feedback")
    assert result["update"].startswith("Updated 1 image selection.")
    assert result["summary"]["new_head"] == "saved-revision"
    assert len(result["next_actions"]) == 4


def test_target_bound_sdk_defers_replay_and_stale_decisions_to_runtime():
    class ReplayRuntime:
        endpoint = "http://127.0.0.1:63331"

        def __init__(self):
            self.current_head = "parent-1"
            self.requests = {}
            self.publication_calls = 0

        def list_timelines(self, project_id, **kwargs):
            return ([{"timeline_id": "main"}], None)

        def inspect_timeline(self, project_id, timeline_id, options=None):
            return {"data": {"is_current_head": True, "revision_id": self.current_head}}

        def get_project_object_location(self, project_id, object_id):
            return {"data": {"verified": True, "object_id": object_id}}

        def publish_parent_composition(self, project_id, timeline_id, publication, *, idempotency_key):
            self.publication_calls += 1
            body = json.dumps(publication, sort_keys=True)
            prior = self.requests.get(idempotency_key)
            if prior is not None:
                if prior[0] != body:
                    raise WorkspaceClientError(
                        409, "idempotency_conflict", "idempotency key was reused with a different request"
                    )
                return {"data": prior[1]}
            if publication["expected_head"] != self.current_head:
                raise WorkspaceClientError(409, "conflict", "parent composition head is stale")
            result = {"new_head": "advanced-head", "old_head": self.current_head}
            self.requests[idempotency_key] = (body, result)
            self.current_head = "advanced-head"
            return {"data": result}

    runtime = ReplayRuntime()
    target = {
        "endpoint": runtime.endpoint,
        "project_id": "project-1",
        "timeline_id": "main",
        "head_revision_id": "parent-1",
        "capabilities": {"edit": {
            "status": "available", "route": "authoring-bundle validate/commit",
        }},
    }
    remote = TargetBoundAuthoringBundle(runtime, target)
    first = remote.publish(bundle(), idempotency_key="replay-key")
    replay = remote.publish(bundle(), idempotency_key="replay-key")
    assert replay["publication"] == first["publication"]

    changed = bundle()
    changed["placements"][0]["duration_ms"] += 1
    with pytest.raises(AuthoringRemoteError, match="idempotency key was reused"):
        remote.publish(changed, idempotency_key="replay-key")
    with pytest.raises(AuthoringRemoteError, match="parent composition head is stale"):
        remote.publish(bundle(), idempotency_key="new-stale-key")
    assert runtime.publication_calls == 4
