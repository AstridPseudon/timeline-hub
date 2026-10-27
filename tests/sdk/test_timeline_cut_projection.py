"""Cut readers share the renderer's projected clocks and identities."""
from astrid.core.timeline.cuts import find_cut, occurrences_from_bundle, occurrences_from_snapshot, picture_cuts
from astrid.core.timeline.shot_composition_projection import _project_clip
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline_cuts import build_cut_table
from astrid.sdk.timeline_views import render_at


def _clip(id, track, at, hold, cut=None):
    return {"id": id, "clipType": "media", "track": track, "at": at, "hold": hold,
            "app": {"cut": cut} if cut else {}}


def test_flat_non_plate_cut_is_visible_and_addressable():
    bed = _clip("bed", "picture", 0, 4, "c1")
    overlay = _clip("title", "title", 1, 1)
    bundle = {"parent": {"clips": [bed, overlay], "tracks": [
        {"id": "title", "kind": "visual"}, {"id": "picture", "kind": "visual"}]},
        "placements": [], "shots": {}}
    tl = Checkout(bundle)
    table = build_cut_table(bundle)
    assert tl.cut("c1").picture.id == "bed"
    assert tl._cut_on_screen(1.5) == "c1"
    assert {clip.id for clip in tl.at(1.5)["showing"]} == {"bed", "title"}
    assert "title" in render_at(bundle, table, 1.5)
    assert find_cut(picture_cuts(occurrences_from_snapshot(bundle["parent"])), "c1")["clip_id"] == "bed"


def test_repeated_occurrences_match_projected_snapshot_with_parent_overlay():
    bed = _clip("bed", "picture", 0, 4, "c1")
    overlay = _clip("overlay", "overlay", 1, 6)
    internal = {"tracks": [{"id": "picture", "kind": "visual"}], "clips": [bed]}
    placements = [{"shot_id": "s", "occurrence_id": "o1", "at_ms": 0, "duration_ms": 2000,
                   "source_offset": 1000, "speed": 2},
                  {"shot_id": "s", "occurrence_id": "o2", "at_ms": 4000, "duration_ms": 2000,
                   "source_offset": 2000, "speed": 2}]
    bundle = {"parent": {"clips": [overlay], "tracks": [{"id": "overlay", "kind": "visual"}]},
              "placements": placements, "shots": {"s": {"internal_timeline": internal}}}
    occurrences = occurrences_from_bundle(bundle)
    projected = []
    for placement in placements:
        start = placement["at_ms"] / 1000
        row = _project_clip(bed, occurrence=placement, revision={"shot_id": "s", "revision_id": "r",
                            "internal_timeline_revision": {"timeline": internal}}, occurrence_start=start,
                            occurrence_end=start + 2, occurrence_speed=2, track_definitions=internal["tracks"], path="clip")
        row["track"] = placement["occurrence_id"] + "~picture"
        projected.append(row)
    snapshot = {"clips": [overlay, *projected], "tracks": [{"id": "overlay", "kind": "visual"},
                *[{"id": p["occurrence_id"] + "~picture", "kind": "visual"} for p in placements]],
                "occurrences": [{"occurrence_id": p["occurrence_id"], "shot_id": "s",
                                 "start": p["at_ms"] / 1000, "end": p["at_ms"] / 1000 + 2} for p in placements]}
    cuts = picture_cuts(occurrences)
    visual = picture_cuts(occurrences_from_snapshot(snapshot))
    assert [(c["start"], c["end"], c["cut_id"]) for c in cuts] == [(0, 2, "c1"), (4, 6, "c1")]
    assert [(c["start"], c["end"], c["cut_id"]) for c in visual] == [(0, 2, "c1"), (4, 6, "c1")]
    assert projected[0]["from"] == 1 and projected[1]["from"] == 2
    assert all([s["id"] for s in c["layers"]] == ["overlay"] for c in cuts)
    tl = Checkout(bundle)
    assert {c.id for c in tl.at(4.5)["showing"]} == {"bed", "overlay"}
    assert "overlay" in render_at(bundle, build_cut_table(bundle), 4.5)
