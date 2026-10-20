"""Pure lowering of the original draft voiceover outcome."""
from __future__ import annotations

import copy

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.native_voiceover import capture_draft_voiceover
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse
from tests.packs.video_editing.test_draft_voiceover import fixture, synthesis, vo

OLD = "sha256:" + "1" * 64
NEW = "sha256:" + "2" * 64


def _voiceover_bundle_and_outcome():
    candidate, scripts = fixture()
    candidate["placements"] = [candidate["placements"][0]]
    candidate["placements"][0].update(occurrence_id="occ-1", shot_id="shot-shared")
    candidate["shots"] = {"shot-shared": candidate["shots"].pop("s1")}
    scripts["occurrences"] = [scripts["occurrences"][0]]
    scripts["occurrences"][0]["occurrence_id"] = "occ-1"
    scripts["occurrences"][0]["text"] = "Long new narration"
    prepared = vo.prepare_draft_voiceover(
        candidate, scripts, synthesize=synthesis, timing_policy="ripple", padding_seconds=.15)

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
        "occurrence.swap-media", "shot.set"]
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
