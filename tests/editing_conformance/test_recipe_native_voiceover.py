"""Pure lowering of the original draft voiceover outcome."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.compiler import TimingInputs, compile_timing
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.native_voiceover import capture_draft_voiceover
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse
from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm
from tests.packs.video_editing.test_draft_voiceover import fixture, synthesis, vo
from tests.sdk.test_timeline_commit_provider import inverse as inverse_call
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi,  # noqa: F401 -- detached provider ABI fixture
)
from tests.timeline.test_authoring_bundle import AUDIO, _closure
from tests.timeline.test_authoring_bundle import OLD as PICTURE

OLD = "sha256:" + "1" * 64
NEW = "sha256:" + "2" * 64


def _voiceover_bundle_and_outcome():
    authored = bundle(shared=False)
    authored_shot = next(iter(authored["shots"].values()))
    next(row for row in authored_shot["internal_timeline"]["tracks"]
         if row["id"] == "voice")["id"] = "vo"
    audio = next(row for row in authored_shot["internal_timeline"]["clips"]
                 if row["id"] == "voice-1")
    audio["id"] = "vo"
    audio["track"] = "vo"
    audio.update({"from": 0, "to": 4, "hold": 4})
    authored_shot["internal_timeline"]["registry"]["assets"]["voice"]["media_id"] = OLD
    authored_shot["payload"]["metadata"][vo.KEY] = copy.deepcopy(
        fixture()[0]["shots"]["s1"]["payload"]["metadata"][vo.KEY])
    scripts = {"revision_id": authored["base_parent"]["revision_id"], "occurrences": [
        {"occurrence_id": "occ-1", "status": "present", "text": "Long new narration"}]}
    prepared = vo.prepare_draft_voiceover(
        authored, scripts, synthesize=synthesis, timing_policy="ripple", padding_seconds=.15)
    return authored, prepared


def _parent_duration_mirror_bundle_and_outcome(duration=6, *, duration_present=True):
    authored = bundle(shared=False)
    parent_clip = authored["parent"]["clips"][0]
    parent_clip.update({"at": 0, "hold": 6})
    authored["parent"]["config"]["clips"] = copy.deepcopy(authored["parent"]["clips"])
    if duration_present:
        authored["parent"]["config"]["duration"] = duration
    placement = authored["placements"][0]
    placement["placement"]["start_ms"] = 0
    placement["duration_ms"] = 3000
    shot = authored["shots"][placement["shot_id"]]
    shot["payload"]["metadata"][vo.KEY] = copy.deepcopy(
        fixture()[0]["shots"]["s1"]["payload"]["metadata"][vo.KEY]
    )
    shot["payload"]["metadata"][vo.KEY]["clip_id"] = "voice-1"
    audio = next(row for row in shot["internal_timeline"]["clips"] if row["id"] == "voice-1")
    audio.update({"from": 0, "to": 4, "hold": 4})
    shot["internal_timeline"]["registry"]["assets"]["voice"]["media_id"] = OLD
    scripts = {"revision_id": authored["base_parent"]["revision_id"], "occurrences": [
        {"occurrence_id": placement["occurrence_id"], "status": "present",
         "text": "Long new narration"}]}
    prepared = vo.prepare_draft_voiceover(
        authored, scripts, synthesize=synthesis, timing_policy="ripple", padding_seconds=.15,
        occurrence_ids=[placement["occurrence_id"]]
    )
    return authored, prepared


def test_original_voiceover_outcome_lowers_to_audio_and_metadata_commands_with_inverse():
    authored, prepared = _voiceover_bundle_and_outcome()
    old = {"asset": "voice", "generation_id": "generation-old", "variant_id": "variant-old",
           "object_id": OLD, "catalog_digest": "sha256:" + "a" * 64}
    new = {"asset": "draft-voiceover-vo", "generation_id": "generation-new", "variant_id": "variant-new",
           "object_id": NEW, "catalog_digest": "sha256:" + "b" * 64}
    verified = [
        {"selection": copy.deepcopy(old), "media_type": "audio/wav", "size": 4,
         "duration_seconds": 4},
        {"selection": copy.deepcopy(new), "media_type": "audio/wav", "size": 4,
         "duration_seconds": 4},
    ]
    lowered = capture_draft_voiceover(
        authored, prepared, media_by_occurrence={"occ-1": new},
        old_media_by_occurrence={"occ-1": old}, verified_media=verified)

    assert [command["op"] for command in lowered["commands"]] == [
        "occurrence.resize", "clip.set", "occurrence.swap-media", "shot.set"]
    assert lowered["capture"]["timing_policy"] == "ripple"
    assert lowered["capture"]["jobs"][0]["source"] == {"from": 0, "to": 4, "hold": 4}

    before = copy.deepcopy(authored)
    plan = execute(authored, lowered["commands"], verified_media=verified)
    assert authored == before
    assert State(plan.bundle).entity("occurrence:occ-1/clip:vo")["asset"] == new["asset"]
    assert State(plan.bundle).entity("occurrence:occ-1/clip:vo")["hold"] == 4
    assert State(plan.bundle).entity("shot:shot-shared")["payload"]["metadata"][vo.KEY] == \
        prepared["candidate"]["shots"]["shot-shared"]["payload"]["metadata"][vo.KEY]
    assert replay(plan, authored, verified_media=verified).records == plan.records
    assert inverse(plan.bundle, plan.records).bundle == before


def test_voiceover_same_alias_swap_updates_duration_mirrors_and_inverse():
    authored, prepared = _voiceover_bundle_and_outcome()
    shot = authored["shots"]["shot-shared"]
    shot["internal_timeline"]["registry"]["assets"]["voice"]["duration"] = 2
    shot["payload"]["assets"] = [{
        "asset_id": "voice", "object_id": OLD, "digest": OLD,
        "source": {"media_id": OLD, "content_sha256": OLD[7:], "duration": 2},
    }]
    shot["payload"]["items"] = [{"item_id": "voice-item", "media_id": OLD,
                                  "metadata": {"keep": True}}]
    old = {"asset": "voice", "generation_id": "generation-old", "variant_id": "variant-old",
           "object_id": OLD, "catalog_digest": "sha256:" + "a" * 64}
    new = {"asset": "voice", "generation_id": "generation-new", "variant_id": "variant-new",
           "object_id": NEW, "catalog_digest": "sha256:" + "b" * 64}
    verified = [{"selection": copy.deepcopy(media), "media_type": "audio/wav", "size": 4,
                 "duration_seconds": 4} for media in (old, new)]

    lowered = capture_draft_voiceover(
        authored, prepared, media_by_occurrence={"occ-1": new},
        old_media_by_occurrence={"occ-1": old}, verified_media=verified)
    before = copy.deepcopy(authored)
    plan = execute(authored, lowered["commands"], verified_media=verified)
    updated = plan.bundle["shots"]["shot-shared"]
    assert updated["internal_timeline"]["registry"]["assets"]["voice"]["duration"] == 4
    assert updated["payload"]["assets"] == [{
        "asset_id": "voice", "object_id": NEW, "digest": NEW,
        "source": {"media_id": NEW, "content_sha256": NEW[7:], "duration": 2},
    }]
    assert updated["payload"]["items"] == [{"item_id": "voice-item", "media_id": NEW,
                                               "metadata": {"keep": True}}]
    assert replay(plan, authored, verified_media=verified).records == plan.records
    assert inverse(plan.bundle, plan.records).bundle == before


def test_parent_duration_mirror_follows_parent_hold_through_compile_and_inverse():
    authored, prepared = _parent_duration_mirror_bundle_and_outcome()
    occurrence_id = authored["placements"][0]["occurrence_id"]
    old = {"asset": "voice", "generation_id": "generation-old", "variant_id": "variant-old",
           "object_id": OLD, "catalog_digest": "sha256:" + "a" * 64}
    new = {"asset": "draft-voiceover-vo", "generation_id": "generation-new",
           "variant_id": "variant-new", "object_id": NEW,
           "catalog_digest": "sha256:" + "b" * 64}
    verified = [{"selection": copy.deepcopy(media), "media_type": "audio/wav", "size": 4,
                 "duration_seconds": 4} for media in (old, new)]
    before = copy.deepcopy(authored)
    before_timing = compile_timing(TimingInputs(authored)).timings[('parent', '', 'direct')]

    lowered = capture_draft_voiceover(
        authored, prepared, media_by_occurrence={occurrence_id: new},
        old_media_by_occurrence={occurrence_id: old}, verified_media=verified)
    plan = execute(authored, lowered["commands"], verified_media=verified)
    after_timing = compile_timing(TimingInputs(plan.bundle)).timings[('parent', '', 'direct')]

    assert plan.bundle["parent"]["clips"][0]["hold"] == 7.15
    assert plan.bundle["parent"]["config"]["duration"] == 7.15
    duration_record = next(record for record in plan.records
                           if record["command"]["op"] == "clip.set"
                           and record["command"]["select"] == "parent/clip:direct")
    assert [write["path"] for write in duration_record["derived_writes"]] == [
        ["config", "clips"], ["config", "duration"]]
    assert before_timing["end"] == 6
    assert float(after_timing["end"]) == pytest.approx(7.15)
    config_only = copy.deepcopy(plan.bundle)
    config_only["parent"]["config"]["duration"] = 999
    assert compile_timing(TimingInputs(config_only)).timings[('parent', '', 'direct')] == after_timing
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    assert compile_timing(TimingInputs(undone.bundle)).timings[('parent', '', 'direct')] == before_timing
    assert replay(plan, before, verified_media=verified).records == plan.records


@pytest.mark.parametrize("shape", ["absent", "null", "opaque"])
def test_parent_duration_absent_null_or_opaque_value_remains_untouched(shape):
    value = None if shape == "null" else {"future": True}
    authored, prepared = _parent_duration_mirror_bundle_and_outcome(
        duration=value, duration_present=shape != "absent")
    occurrence_id = authored["placements"][0]["occurrence_id"]
    old = {"asset": "voice", "generation_id": "generation-old", "variant_id": "variant-old",
           "object_id": OLD, "catalog_digest": "sha256:" + "a" * 64}
    new = {"asset": "draft-voiceover-vo", "generation_id": "generation-new",
           "variant_id": "variant-new", "object_id": NEW,
           "catalog_digest": "sha256:" + "b" * 64}
    verified = [{"selection": copy.deepcopy(media), "media_type": "audio/wav", "size": 4,
                 "duration_seconds": 4} for media in (old, new)]
    lowered = capture_draft_voiceover(
        authored, prepared, media_by_occurrence={occurrence_id: new},
        old_media_by_occurrence={occurrence_id: old}, verified_media=verified)
    plan = execute(authored, lowered["commands"], verified_media=verified)

    assert plan.bundle["parent"]["clips"][0]["hold"] == 7.15
    if shape == "absent":
        assert "duration" not in plan.bundle["parent"]["config"]
    else:
        assert plan.bundle["parent"]["config"]["duration"] == value
    assert all(write["path"] != ["config", "duration"]
               for record in plan.records for write in record["derived_writes"])
    assert inverse(plan.bundle, plan.records).bundle == authored


@pytest.mark.parametrize("source_bound", [False, True])
@pytest.mark.usefixtures("runtime_abi")
def test_prepared_ripple_timing_and_padding_survive_lowering_inverse_and_redo(source_bound):
    # Main stores padding only through these concrete timing consequences.
    authored = bundle()
    shot = authored["shots"][authored["placements"][0]["shot_id"]]
    shot["payload"]["metadata"][vo.KEY] = copy.deepcopy(
        fixture()[0]["shots"]["s1"]["payload"]["metadata"][vo.KEY]
    )
    shot["payload"]["metadata"][vo.KEY]["clip_id"] = "voice-1"
    State(authored).entity("occurrence:occ-1/clip:voice-1").update(
        {"from": 0, "to": 4, "hold": 4})
    shot["internal_timeline"]["registry"]["assets"]["voice"]["media_id"] = OLD
    if source_bound:
        parent, shots, internals = _closure()
        parent["payload"]["config"]["output"] = {"fps": {"numerator": 30000, "denominator": 1001}}
        internals[0]["payload"]["output"] = copy.deepcopy(parent["payload"]["config"]["output"])
        for index, row in enumerate(parent["payload"]["occurrences"]):
            row.update(duration_ms=10000, source_offset=0, speed=1)
            row["placement"]["start_ms"] = 10000 + 10000 * index
        shots[0]["payload"]["metadata"] = copy.deepcopy(shot["payload"]["metadata"])
        internals[0]["payload"]["clips"][1].update({"from": 0, "to": 4, "hold": 4})
        internals[0]["payload"]["registry"]["assets"]["voice"]["media_id"] = OLD
        for image in [parent, *shots, *internals]:
            image.pop("project_id")
            image["content_digest"] = _digest(image["payload"])
        parent.pop("timeline_id")
        document = {"schema_version": 1, "project_id": "project-1", "timeline_id": "film",
                    "parent_revision": parent, "shot_revisions": shots,
                    "internal_timeline_revisions": internals,
                    "dependency_manifest": _manifest(shots, internals, [
                        {"media_id": identity, "content_digest": identity} for identity in (PICTURE, AUDIO)], [])}
        authored = bundle_from_document(document)
    scripts = {"revision_id": authored["base_parent"]["revision_id"], "occurrences": [
        {"occurrence_id": "occ-1", "status": "present", "text": "Long new narration"}]}
    before = copy.deepcopy(authored)
    prepared = vo.prepare_draft_voiceover(
        authored, scripts, synthesize=synthesis, timing_policy="ripple",
        padding_seconds=.15, occurrence_ids=["occ-1"])
    assert prepared["candidate"]["placements"][0]["duration_ms"] == 4150
    assert prepared["candidate"]["placements"][1]["placement"]["start_ms"] == 14150

    old = {"asset": "voice", "generation_id": "generation-old", "variant_id": "variant-old",
           "object_id": OLD, "catalog_digest": "sha256:" + "a" * 64}
    new = {"asset": "draft-voiceover-vo", "generation_id": "generation-new", "variant_id": "variant-new",
           "object_id": NEW, "catalog_digest": "sha256:" + "b" * 64}
    verified = [{"selection": copy.deepcopy(media), "media_type": "audio/wav", "size": 4,
                 "duration_seconds": 4} for media in (old, new)]
    lowered = capture_draft_voiceover(
        authored, prepared, media_by_occurrence={"occ-1": new},
        old_media_by_occurrence={"occ-1": old}, verified_media=verified)
    plan = execute(authored, lowered["commands"], verified_media=verified)
    assert authored == before
    if source_bound:
        assert [command["version"] for command in lowered["commands"]] == ["1", "1", "2", "2", "2"]
        accepted = bundle_from_document(document_from_bundle(plan.bundle))
        assert State(accepted).occurrence("occurrence:occ-2")["placement"]["start_ms"] == 14150
        assert State(accepted).entity("occurrence:occ-1/clip:picture-1")["hold"] == .415
        realm = MediaRealm(document, verified)
        committed = realm.call(lowered["commands"])
        assert committed["data"]["canonical_document"] == document_from_bundle(plan.bundle)
        undo = realm.call([inverse_call([committed["receipt"]["receipt_id"]])])
        assert undo["data"]["canonical_document"] == document
        redo = realm.call([inverse_call([undo["receipt"]["receipt_id"]])])
        assert redo["data"]["canonical_document"] == committed["data"]["canonical_document"]
    assert replay(plan, authored, verified_media=verified).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle

    def timing(candidate):
        state = State(candidate)
        return {
            "occurrence:occ-1::duration_ms": state.occurrence("occurrence:occ-1")["duration_ms"],
            "occurrence:occ-2::placement.start_ms": state.occurrence("occurrence:occ-2")["placement"]["start_ms"],
            "occurrence:occ-1/clip:picture-1::hold": state.entity("occurrence:occ-1/clip:picture-1")["hold"],
        }

    assert timing(plan.bundle) == timing(prepared["candidate"]) == {
        "occurrence:occ-1::duration_ms": 4150,
        "occurrence:occ-2::placement.start_ms": 14150,
        "occurrence:occ-1/clip:picture-1::hold": .415,
    }
    assert "padding_seconds" not in lowered["capture"]
    assert plan.bundle["placements"] == prepared["candidate"]["placements"]
    assert plan.bundle["parent"] == prepared["candidate"]["parent"]
    assert all("padding_seconds" not in write["path"] and (
        write["path"] or "/asset:" in write["ref"])
               for record in plan.records for write in record["writes"])
    sibling = before["placements"][1]["shot_id"]
    assert plan.bundle["shots"][sibling] == before["shots"][sibling]
    for owner in ("occurrence:occ-1", "occurrence:occ-2"):
        metadata = State(plan.bundle).entity(owner + "/shot")
        shot_id = State(plan.bundle).occurrence(owner)["shot_id"]
        authored_metadata = plan.bundle["shots"][shot_id]["payload"]["metadata"]
        assert authored_metadata == prepared["candidate"]["shots"][shot_id]["payload"]["metadata"]
        assert "padding_seconds" not in authored_metadata
        assert {key: value for key, value in authored_metadata.items() if key != vo.KEY} == {
            key: value for key, value in before["shots"][shot_id]["payload"]["metadata"].items()
            if key != vo.KEY}
        assert metadata["shot_id"] == before["source_mapping"]["shots"][shot_id]["shot_id"]


@pytest.mark.parametrize("mutate", [
    lambda candidate: candidate["placements"][0].update(shot_revision_id="revision-foreign"),
    lambda candidate: candidate["placements"][0].update(source_id="source-foreign"),
    lambda candidate: candidate["source_mapping"]["shots"]["shot-shared"].update(
        revision_id="revision-foreign"),
])
def test_prepared_source_identity_refuses_stale_values_before_capture(mutate):
    authored, prepared = _voiceover_bundle_and_outcome()
    mutate(prepared["candidate"])
    before_authored = copy.deepcopy(authored)
    before_prepared = copy.deepcopy(prepared)
    old = {"asset": "voice", "generation_id": "generation-old", "variant_id": "variant-old",
           "object_id": OLD, "catalog_digest": "sha256:" + "a" * 64}
    new = {"asset": "draft-voiceover-vo", "generation_id": "generation-new", "variant_id": "variant-new",
           "object_id": NEW, "catalog_digest": "sha256:" + "b" * 64}
    verified = [{"selection": copy.deepcopy(media), "media_type": "audio/wav", "size": 4,
                 "duration_seconds": 4} for media in (old, new)]

    with pytest.raises(CommandError, match="prepared .*source"):
        capture_draft_voiceover(
            authored, prepared, media_by_occurrence={"occ-1": new},
            old_media_by_occurrence={"occ-1": old}, verified_media=verified)
    assert authored == before_authored
    assert prepared == before_prepared


@pytest.mark.parametrize("change", ["parent-duration", "visual-start", "source-window"])
def test_unrepresented_prepared_timing_refuses_without_a_partial_result(change):
    authored, _ = _voiceover_bundle_and_outcome()
    if change == "parent-duration":
        authored["parent"]["config"]["duration"] = 30
    elif change == "visual-start":
        State(authored).entity("occurrence:occ-1/clip:picture-1")["at"] = .25
    else:
        State(authored).entity("occurrence:occ-1/clip:vo").update({"from": 1, "to": 5})
    scripts = {"revision_id": authored["base_parent"]["revision_id"], "occurrences": [
        {"occurrence_id": "occ-1", "status": "present", "text": "Long new narration"}]}
    prepared = vo.prepare_draft_voiceover(
        authored, scripts, synthesize=synthesis, timing_policy="ripple", padding_seconds=.15)
    before = copy.deepcopy(authored)
    old = {"asset": "voice", "generation_id": "generation-old", "variant_id": "variant-old",
           "object_id": OLD, "catalog_digest": "sha256:" + "a" * 64}
    new = {**old, "asset": "draft-voiceover-vo", "object_id": NEW}
    verified = [{"selection": copy.deepcopy(media), "media_type": "audio/wav", "size": 4,
                 "duration_seconds": 4} for media in (old, new)]
    from astrid.sdk.timeline._command_state import CommandError

    with pytest.raises(CommandError, match="literal command carrier"):
        capture_draft_voiceover(authored, prepared, media_by_occurrence={"occ-1": new},
                               old_media_by_occurrence={"occ-1": old}, verified_media=verified)
    assert authored == before
