"""Exact E216 authored flat HOLD5, kept separate from bounded shot placements."""

import copy
import json
from pathlib import Path

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.core.timeline.authoring_bundle import open_authoring_bundle
from astrid.core.timeline.cuts import (
    occurrences_from_bundle,
    occurrences_from_snapshot,
    picture_cuts,
)
from astrid.core.timeline.duration import timeline_duration_seconds
from astrid.sdk.timeline.chapter_storage import compile_candidate
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")

FIXTURE = Path(__file__).parents[1] / "fixtures/timeline_editing/e216_flat_hold5_parent.json"


def flat():
    return open_authoring_bundle(
        json.loads(FIXTURE.read_text()), shot_revisions=[], internal_timeline_revisions=[]
    )


def call(op, **args):
    return {
        "op": op,
        "select": "parent/clip:clip-0",
        "args": args,
        "expect": {
            "hold" if op == "clip.set-duration" else "at": {
                "state": "present",
                "value": 5 if op == "clip.set-duration" else 0,
            }
        },
    }


def test_exact_serialized_parent_move_resize_reload_inverse(tmp_path):
    before = Checkout(flat()).document()
    for command, extent in [
        (call("clip.nudge", frames=30), 6),
        (call("clip.set-duration", seconds=6), 6),
    ]:
        after, plan, _ = RuntimeCommitService._apply(before, [command])
        tl = Checkout(after)
        assert tl.duration == extent
        pictures = [cut.picture for cut in tl.cuts if cut.picture is not None]
        assert len(pictures) == 1 and pictures[0].shot_id is None
        assert pictures[0].end == extent
        assert tl._length_problems() == []
        parent = tl.document()["parent"]
        assert timeline_duration_seconds(parent, tl.fps) == extent
        assert max(c["end"] for c in picture_cuts(occurrences_from_bundle(after))) == extent
        assert max(c["end"] for c in picture_cuts(occurrences_from_snapshot(parent))) == extent
        assert [
            c["clip_id"] for c in picture_cuts(occurrences_from_bundle(after)) if c["clip"]
        ] == ["clip-0"]
        published = compile_candidate(after).publication["parent_composition"]
        assert timeline_duration_seconds(published, tl.fps) == extent
        assert after["shots"] == {} and after["placements"] == []
        assert parent["registry"] == before["parent"]["registry"]
        assert parent["config"]["tracks"] == before["parent"]["config"]["tracks"]
        assert parent["clips"][0].get("app") == before["parent"]["clips"][0].get("app")
        path = tmp_path / "flat.json"
        path.write_text(json.dumps(after))
        assert Checkout.load(path).document() == tl.document()
        undo = inverse_command(
            plan.calls, before, after, "synthetic-publication", consequences=plan.consequences
        )
        restored = RuntimeCommitService._apply(after, [undo])[0]
        assert restored == before
    # Moving the first image leaves an actual black interval; it is not filled.
    moved = RuntimeCommitService._apply(before, [call("clip.nudge", frames=30)])[0]
    assert [
        (c["start"], c["end"])
        for c in picture_cuts(occurrences_from_bundle(moved))
        if c["clip"] is None
    ] == [(0, 1)]


def test_audio_extent_is_not_picture_coverage():
    data = flat()
    data["parent"]["clips"] = [
        {"id": "sound", "track": "A1", "clipType": "media", "at": 0, "from": 2, "to": 10}
    ]
    assert Checkout(data).duration == 8
    from astrid.sdk.timeline_cuts import build_cut_table

    assert build_cut_table(data)["duration"] == 8
    assert picture_cuts(occurrences_from_bundle(data)) == []
    from types import SimpleNamespace

    gaps = Checkout(data).picture_gaps([SimpleNamespace(cls="GAP", start_frame=0, end_frame=240)])
    assert any("0.000–8.000" in line for line in gaps)
    data["parent"]["clips"].append(
        {"id": "picture", "track": "V1", "clipType": "hold", "at": 2, "hold": 2}
    )
    cuts = picture_cuts(occurrences_from_bundle(data))
    assert [(c["start"], c["end"]) for c in cuts if c["clip"] is None] == [(0, 2), (4, 8)]
    assert all(c["clip_id"] != "sound" for c in cuts)


@pytest.mark.parametrize("patch", [{"speed": 0}, {"speed": -1}, {"at": float("nan")}, {"hold": -1}])
def test_malformed_flat_timing_refused(patch):
    data = flat()
    data["parent"]["clips"][0].update(patch)
    with pytest.raises(ValueError):
        _ = Checkout(data).duration


def test_stale_duration_refused_without_mutating_input():
    data = flat()
    frozen = copy.deepcopy(data)
    command = call("clip.set-duration", seconds=6)
    command["expect"]["hold"]["value"] = 4
    with pytest.raises(ValueError):
        RuntimeCommitService._apply(data, [command])
    assert data == frozen


def test_frame_arithmetic_and_source_clocks_preserved():
    data = flat()
    clip = data["parent"]["clips"][0]
    clip.update(at=0.5 / 30, hold=5, speed=2, **{"from": 100, "to": 101})
    tl = Checkout(data)
    assert tl.duration == pytest.approx(76 / 30, abs=1e-6)
    assert tl.document()["parent"]["clips"][0] == clip
    assert tl._length_problems() == []


def test_bounded_child_and_parent_overlay_do_not_expand_placement():
    tiny = json.loads((FIXTURE.parent / "tiny.json").read_text())
    tiny["shots"]["A"]["internal_timeline"]["clips"].append(
        {"id": "overrun", "track": "plate", "at": 0, "hold": 6}
    )
    tl = Checkout(tiny)
    assert any("overrun" in line for line in tl._length_problems())
    assert tl.duration == 8
    tiny["parent"]["clips"] = [{"id": "overlay-overrun", "track": "V1", "at": 0, "hold": 12}]
    tl = Checkout(tiny)
    assert any("overlay-overrun" in line for line in tl._length_problems())


def test_empty_flat_first_visual_add_is_one_track_and_media_transaction_with_inverse(tmp_path):
    from types import SimpleNamespace

    from astrid.core.timeline.authoring_bundle import _digest

    parent = copy.deepcopy(json.loads(FIXTURE.read_text())["payload"])
    parent["clips"] = []
    parent["config"]["clips"] = []
    parent["config"]["tracks"] = []
    parent["registry"] = {"assets": {}}
    revision = dict(
        project_id="p",
        timeline_id="t",
        revision_id="empty-r1",
        content_digest=_digest(parent),
        payload=parent,
    )
    before = Checkout(
        open_authoring_bundle(revision, shot_revisions=[], internal_timeline_revisions=[])
    ).document()
    record = dict(
        realm_id="realm",
        project_id="p",
        asset="selected",
        generation_id="g",
        variant_id="v",
        object_id="sha256:" + "a" * 64,
        generation={"type": "image", "source_task_id": None, "metadata": {"opaque": None}},
        variant={"variant_type": "original", "metadata": {"op": "clear"}},
        entry={
            "object_id": "sha256:" + "a" * 64,
            "media_type": "image/png",
            "size": 4,
            "filename": "selected.png",
            "duration_seconds": None,
        },
    )
    selection = {key: record[key] for key in ["asset", "generation_id", "variant_id", "object_id"]}
    selection["catalog_digest"] = _digest(record)
    track = {
        "op": "timeline.add",
        "select": "parent/track:V1",
        "args": {"track": {"id": "V1", "kind": "visual", "label": "Picture"}},
        "created": ["parent/track:V1"],
        "expect": {"parent/track:V1::": {"state": "absent"}},
    }
    add = {
        "op": "timeline.add",
        "select": "parent/track:V1",
        "args": {"media": selection, "clip_id": "first", "at": 0, "duration": 5},
        "created": ["parent/clip:first"],
        "expect": {
            "parent/clip:first::": {"state": "absent"},
            "parent::registry.assets.selected": {"state": "absent"},
        },
    }
    port = SimpleNamespace(
        selected_media=lambda selected: {**record, "catalog_digest": _digest(record)}
    )
    captured = RuntimeCommitService._capture_media(port, {"project_id": "p"}, [track, add])
    after, plan, _ = RuntimeCommitService._apply(before, captured)
    assert Checkout(after).duration == 5 and Checkout(after)._length_problems() == []
    assert after["shots"] == {} and after["placements"] == []
    assert after["parent"]["registry"]["assets"]["selected"]["authoring_metadata"]["variant"][
        "metadata"
    ] == {"op": "clear"}
    published = compile_candidate(after).publication["parent_composition"]
    assert timeline_duration_seconds(published, 30) == 5
    path = tmp_path / "added.json"
    path.write_text(json.dumps(after))
    assert Checkout.load(path).document() == after
    inverse = inverse_command(
        plan.calls, before, after, "synthetic-add-publication", consequences=plan.consequences
    )
    restored = RuntimeCommitService._apply(after, [inverse])[0]
    assert restored == before
    bad = copy.deepcopy(add)
    bad["args"]["media"]["object_id"] = "sha256:" + "c" * 64
    with pytest.raises(ValueError, match="identity"):
        RuntimeCommitService._capture_media(port, {"project_id": "p"}, [track, bad])


@pytest.mark.parametrize("at,hold", [(0.49 / 30, 1.49 / 30), (0.5 / 30, 1.5 / 30)])
def test_flat_containment_uses_actual_sequence_frame_edges(at, hold):
    data = flat()
    data["parent"]["clips"][0].update(at=at, hold=hold)
    tl = Checkout(data)
    assert tl.duration == pytest.approx(timeline_duration_seconds(data["parent"], tl.fps), abs=1e-6)
    assert tl._length_problems() == []
    assert max(row["end"] for row in picture_cuts(occurrences_from_bundle(data))) == pytest.approx(
        tl.duration, abs=1e-6
    )
