"""Faithful sprite cuts and explicit fallbacks for uncuttable visual crossers."""
from __future__ import annotations

import pytest

from astrid.sdk.timeline_restructure import describe, flatten, plan, split
from tests.sdk.test_timeline_restructure import flat_film, published


def test_sprite_pieces_shift_sparse_held_poses_and_preserve_animation_phase():
    flat = flat_film()
    flat["shots"]["film"]["internal_timeline"]["clips"].append({
        "id": "sprite-cross", "clipType": "am-sprite", "track": "sprite", "asset": "R",
        "at": 3.6333333333333333, "hold": 5.0,
        "params": {"x": 1, "y": 2, "flipX": False, "stepFrames": 2,
                    "keyframes": [{"frame": 2, "x": 4}, {"frame": 8, "y": 9},
                                  {"frame": 11, "flipX": True}, {"frame": 30, "x": 12}],
                    "frames": {"frameWidth": 16, "frameHeight": 16, "count": 4, "fps": 8},
                    "blinkAt": [10, 18, 40], "silhouette": {"until": 35},
                    "outline": {"px": 1, "pulse": 6}, "enter": "slideIn"},
    })

    planned = plan(flat)
    pieces = [c for chapter in planned.chapters for c in chapter.clips
              if c.get("app", {}).get("astrid", {}).get("timeline_restructure_piece", {}).get("id") == "sprite-cross"]

    assert len(pieces) == 3
    second = pieces[1]
    params = second["params"]
    assert params["frameOffset"] == 11
    assert second["app"]["astrid"]["timeline_restructure_piece"]["sprite_frame_offset"] == 11
    assert (params["x"], params["y"], params["flipX"]) == (4, 9, False)
    assert params["keyframes"] == [{"frame": 0, "flipX": True}, {"frame": 19, "x": 12}]
    assert params["blinkAt"] == [-1, 7, 29]
    assert params["silhouette"] == {"until": 24}
    assert params["frames"] == {"frameWidth": 16, "frameHeight": 16, "count": 4, "fps": 8}
    assert params["outline"] == {"px": 1, "pulse": 6}
    assert params["enter"] == "slideIn"


def test_uncuttable_keyframed_am_clips_use_noncolliding_over_row_and_round_trip_provenance():
    flat = flat_film()
    tracks = flat["parent"]["config"]["tracks"]
    tracks.append({"id": "picture-over", "kind": "visual", "opacity": 0.6})
    tracks[0]["opacity"] = 0.8  # the occurrence row supplies only the insertion position
    flat["shots"]["film"]["internal_timeline"]["tracks"][1]["opacity"] = 0.4
    clips = flat["shots"]["film"]["internal_timeline"]["clips"]
    clips.append({"id": "footage-cross", "name": "Footage", "clipType": "am-footage", "track": "sprite",
                  "asset": "R", "at": 3.5, "hold": 1.0, "params": {"in": 4, "zoom": 2, "keyframes": [{"frame": 0}]}})

    planned = plan(flat)
    fallback = next(c for c in planned.film_clips if c["id"] == "footage-cross")
    assert fallback["track"] == "picture-over-2"
    over_definition = next(track for track in planned.tracks if track["id"] == "picture-over-2")
    assert over_definition["opacity"] == 0.4
    assert fallback["app"]["astrid"]["timeline_restructure_over"] == {"track": "sprite", "row": "picture"}
    assert [t["id"] for t in planned.tracks][:3] == ["picture-over-2", "picture", "picture-over"]
    report = "\n".join(describe(flat))
    assert "footage-cross (Footage) [am-footage] -> picture-over-2" in report

    stored = published(split(flat))
    flattened = flatten(stored)
    restored = next(c for c in flattened["shots"][flattened["placements"][0]["shot_id"]]["internal_timeline"]["clips"]
                    if c["id"] == "footage-cross")
    assert restored["track"] == "sprite"
    assert "timeline_restructure_over" not in restored.get("app", {}).get("astrid", {})
    assert restored["params"] == {"in": 4, "zoom": 2, "keyframes": [{"frame": 0}]}


def test_sprite_phase_advances_at_clip_speed():
    flat = flat_film()
    flat["shots"]["film"]["internal_timeline"]["clips"].append({
        "id": "fast-sprite", "clipType": "am-sprite", "track": "sprite", "asset": "R",
        "at": 3.5, "hold": 2.0, "speed": 2.0, "params": {"x": 4, "y": 7},
    })
    planned = plan(flat)
    pieces = [c for chapter in planned.chapters for c in chapter.clips
              if c.get("app", {}).get("astrid", {}).get("timeline_restructure_piece", {}).get("id") == "fast-sprite"]
    assert pieces[1]["params"]["frameOffset"] == 30


@pytest.mark.parametrize(("speed", "phase"), [(0.5, 7), (1.5, 22), (2.0, 30)])
def test_sprite_cut_phase_uses_the_renderer_source_clock(speed, phase):
    flat = flat_film()
    flat["shots"]["film"]["internal_timeline"]["clips"].append({
        "id": "clocked-sprite", "clipType": "am-sprite", "track": "sprite", "asset": "R",
        "at": 3.5, "hold": 2.0, "speed": speed, "params": {"x": 4, "y": 8, "frameOffset": 3},
    })
    planned = plan(flat)
    piece = next(c for c in planned.chapters[1].clips
                 if c.get("app", {}).get("astrid", {}).get("timeline_restructure_piece", {}).get("id") == "clocked-sprite")
    assert piece["params"]["frameOffset"] == phase + 3


def test_am_snap_plate_animation_is_not_restarted_by_cutting():
    flat = flat_film()
    flat["shots"]["film"]["internal_timeline"]["clips"].append({
        "id": "plate-cross", "clipType": "am-snap-plate", "track": "plate", "asset": "P",
        "at": 3.5, "hold": 1.0, "params": {"punchAt": [2], "push": {"to": 3, "frames": 10}},
    })
    planned = plan(flat)
    clip = next(c for c in planned.film_clips if c["id"] == "plate-cross")
    assert clip["track"] == "picture-over"
    assert clip["params"] == {"punchAt": [2], "push": {"to": 3, "frames": 10}}

