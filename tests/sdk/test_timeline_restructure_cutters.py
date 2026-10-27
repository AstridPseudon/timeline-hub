"""Core media cutters used when a flat timeline is split into chapter shots."""
from __future__ import annotations

from astrid.sdk.timeline_restructure import differences, flatten, plan, split

from tests.sdk.test_timeline_restructure import flat_film


def _clips_by_source(chapters, source_id):
    return [clip for chapter in chapters for clip in chapter.clips
            if clip.get("app", {}).get("astrid", {}).get("timeline_restructure_piece", {}).get("id") == source_id]


def test_speeded_media_crossing_multiple_walls_advances_source_and_keeps_window():
    flat = flat_film()
    clips = flat["shots"]["film"]["internal_timeline"]["clips"]
    clips.append({"id": "media-cross", "clipType": "media", "track": "plate", "asset": "P",
                  "at": 3.5, "from": 5.0, "to": 17.0, "hold": 12.0, "speed": 2.0})

    planned = plan(flat)
    pieces = _clips_by_source(planned.chapters, "media-cross")

    assert len(pieces) == 3
    assert [(clip["at"], clip["hold"], clip["from"], clip["to"]) for clip in pieces] == [
        (3.5, 1.0, 5.0, 6.0), (0.0, 8.0, 6.0, 14.0), (0.0, 3.0, 14.0, 17.0)]
    assert [clip["app"]["astrid"]["timeline_restructure_piece"]["index"] for clip in pieces] == [0, 1, 2]
    assert len({clip["id"] for clip in pieces}) == 3
    assert pieces == _clips_by_source(plan(flat).chapters, "media-cross")


def test_still_and_text_crossers_are_cut_while_am_types_use_over_row_fallback():
    flat = flat_film()
    clips = flat["shots"]["film"]["internal_timeline"]["clips"]
    clips.extend([
        {"id": "still-cross", "clipType": "image", "track": "type", "asset": "R",
         "at": 3.0, "hold": 2.0, "params": {"fit": "cover"}},
        {"id": "text-cross", "clipType": "text", "track": "type", "at": 7.5, "hold": 1.0,
         "params": {"text": "Hello", "style": {"font": "serif"}}},
        {"id": "element-cross", "clipType": "am-type", "track": "type", "at": 3.5, "hold": 1.0,
         "params": {"text": "legacy"}},
    ])

    planned = plan(flat)

    stills = _clips_by_source(planned.chapters, "still-cross")
    texts = _clips_by_source(planned.chapters, "text-cross")
    assert [(clip["at"], clip["hold"], clip["params"]) for clip in stills] == [
        (3.0, 1.0, {"fit": "cover"}), (0.0, 1.0, {"fit": "cover"})]
    assert [(clip["at"], clip["hold"], clip["params"]) for clip in texts] == [
        (3.5, 0.5, {"text": "Hello", "style": {"font": "serif"}}),
        (0.0, 0.5, {"text": "Hello", "style": {"font": "serif"}})]
    element = next(clip for clip in planned.film_clips if clip["id"] == "element-cross")
    assert element["track"] == "picture-over"
    assert element["app"]["astrid"]["timeline_restructure_over"] == {"track": "type", "row": "picture"}


def test_clip_type_projection_alias_is_cut_like_cliptype():
    flat = flat_film()
    flat["shots"]["film"]["internal_timeline"]["clips"].append({
        "id": "alias-cross", "clip_type": "image", "track": "type", "asset": "R",
        "at": 3.5, "hold": 1.0,
    })
    planned = plan(flat)
    pieces = _clips_by_source(planned.chapters, "alias-cross")
    assert len(pieces) == 2
    assert {piece["clip_type"] for piece in pieces} == {"image"}


def test_media_crosser_clips_at_film_end():
    flat = flat_film()
    clips = flat["shots"]["film"]["internal_timeline"]["clips"]
    clips.append({"id": "tail", "clipType": "video", "track": "plate", "asset": "P",
                  "at": 11.0, "from": 4.0, "to": 8.0, "speed": 1.0})

    planned = plan(flat)
    pieces = [clip for chapter in planned.chapters for clip in chapter.clips if clip.get("id") == "tail"]

    assert len(pieces) == 1
    assert pieces[0]["from"] == 4.0 and pieces[0]["to"] == 5.0
    assert planned.film_clips == [clip for clip in planned.film_clips if clip["id"] != "tail"]


def test_media_without_from_advances_from_implicit_zero_and_rejoins_timed_words():
    flat = flat_film()
    source = {"id": "worded-media", "clipType": "media", "track": "type", "asset": "P",
              "at": 3.5, "hold": 2.0,
              "app": {"astrid": {"words": [[0.2, 0.4, "before"], [0.55, 0.75, "after"]]}}}
    flat["shots"]["film"]["internal_timeline"]["clips"].append(source)

    stored = split(flat)
    pieces = _clips_by_source(plan(flat).chapters, "worded-media")
    assert [(piece["from"], piece["at"]) for piece in pieces] == [(0.0, 3.5), (0.5, 0.0)]
    assert pieces[1]["app"]["astrid"]["words"] == [[0.05, 0.25, "after"]]
    restored = next(clip for shot in flatten(stored)["shots"].values()
                    for clip in shot["internal_timeline"]["clips"] if clip["id"] == "worded-media")
    assert "from" not in restored
    assert restored["app"]["astrid"]["words"] == source["app"]["astrid"]["words"]
    assert differences(flat, stored) == []

    changed = split(flat)
    second = next(clip for shot in changed["shots"].values() for clip in shot["internal_timeline"]["clips"]
                  if clip.get("app", {}).get("astrid", {}).get("timeline_restructure_piece", {}).get("id") == "worded-media"
                  and clip["app"]["astrid"]["timeline_restructure_piece"]["index"] == 1)
    second["app"]["astrid"]["words"][0][2] = "edited"
    assert differences(flat, changed)
