"""Frame-level regressions for cuts checked against the pinned compositor."""
from __future__ import annotations

import math

import pytest

from astrid.sdk import timeline_restructure
from astrid.sdk.timeline_restructure import differences, plan, split
from tests.sdk.test_timeline_restructure import flat_film

FPS = 30


def _pinned_rendered_interval(start: float, hold: float, fps: int = FPS) -> tuple[int, int]:
    """Return compositor frames using composition/typescript/src/lib/duration.ts.

    The pinned compositor uses secondsToFrames = Math.round(seconds * fps),
    then max(1, round(hold / speed * fps)); its Sequence starts at the rounded
    start frame. Keep this tiny adapter local so the test checks the renderer's
    independent rounding, not Astrid's timeline interval helper.
    """
    start_frame = math.floor(start * fps + 0.5)  # JavaScript Math.round for nonnegative time.
    duration_frames = max(1, math.floor(hold * fps + 0.5))
    return start_frame, start_frame + duration_frames


def _pieces(stored, source_id):
    result = []
    starts = {row["shot_id"]: row["placement"]["start_ms"] / 1000 for row in stored["placements"]}
    for shot in stored["shots"].values():
        if shot["shot_id"] not in starts:
            continue
        start = starts[shot["shot_id"]]
        for clip in shot["internal_timeline"]["clips"]:
            marker = clip.get("app", {}).get("astrid", {}).get("timeline_restructure_piece", {})
            if marker.get("id") == source_id:
                result.append((start + clip["at"], clip["hold"]))
    return sorted(result)


@pytest.mark.parametrize("clip_type", ["media", "image", "video", "still", "text", "am-sprite"])
def test_fractional_cut_that_rounds_to_an_extra_compositor_frame_is_rejected(monkeypatch, clip_type):
    flat = flat_film()
    source_id = f"duration-phase-{clip_type}"
    clip = {"id": source_id, "clipType": clip_type, "track": "sprite", "asset": "R",
            "at": 3.51, "hold": 0.51, "params": {}}
    flat["shots"]["film"]["internal_timeline"]["clips"].append(clip)

    # Construct the exact legacy cut that the old path would have made. The
    # production safety check must be restored before differences() inspects it.
    with monkeypatch.context() as bypass:
        bypass.setattr(timeline_restructure, "_cut_safety_reason", lambda *_args, **_kwargs: None)
        legacy = split(flat)

    original_interval = _pinned_rendered_interval(clip["at"], clip["hold"])
    rendered_pieces = [_pinned_rendered_interval(start, hold) for start, hold in _pieces(legacy, source_id)]
    assert original_interval == (105, 120)
    assert rendered_pieces == [(105, 120), (120, 121)]
    problems = differences(flat, legacy)
    assert problems, "the renderer's extra frame must make this unsafe legacy cut differ"

    planned = plan(flat)
    fallback = next(clip for clip in planned.film_clips if clip["id"] == source_id)
    assert fallback["track"].endswith("-over")
    assert not _pieces(split(flat), source_id)


@pytest.mark.parametrize("clip_type", ["image", "text", "am-sprite"])
def test_fractional_start_whose_cut_frame_intervals_match_remains_cuttable(clip_type):
    flat = flat_film()
    source_id = f"duration-phase-safe-{clip_type}"
    clip = {"id": source_id, "clipType": clip_type, "track": "sprite", "asset": "R",
            "at": 3.51, "hold": 1.0, "params": {}}
    flat["shots"]["film"]["internal_timeline"]["clips"].append(clip)

    stored = split(flat)
    original_interval = _pinned_rendered_interval(clip["at"], clip["hold"])
    piece_intervals = [_pinned_rendered_interval(start, hold) for start, hold in _pieces(stored, source_id)]

    assert original_interval == (105, 135)
    assert piece_intervals == [(105, 120), (120, 135)]
    assert differences(flat, stored) == []
