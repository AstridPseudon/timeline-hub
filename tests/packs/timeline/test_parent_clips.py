"""Clips that sit directly on the parent composition (media dropped on an empty App timeline, no shots) are
found and edited by the same lookup, with the same matching and ambiguity rules, as clips inside shots."""
from __future__ import annotations

import copy

import pytest

from astrid.packs.timeline import cli
from astrid.sdk.timeline._common import PARENT_SHOT, TimelineEditError
from astrid.sdk.timeline_checkout import Checkout
from tests.packs.timeline.test_cli_edit_flags import FPS
from tests.packs.timeline.test_cli_edit_flags import bundle as shot_bundle

CANVAS = {"theme_overrides": {"visual": {"canvas": {"fps": FPS, "width": 1920, "height": 1080}}}}


def _clips():
    return [
        {"id": "clip-1", "clipType": "media", "track": "V1", "asset": "photo", "at": 0.0, "hold": 3.0, "params": {"opacity": 1}},
        {"id": "clip-2", "clipType": "media", "track": "A1", "asset": "song", "at": 0.0, "from": 0.0, "to": 6.0},
        {"id": "clip-3", "clipType": "text", "track": "V2", "at": 1.0, "hold": 2.0, "params": {"text": "Hello world"}},
    ]


def media_only():
    """What the App writes for media dropped on an empty timeline: clips on the parent, no shots."""
    return {
        "project_id": "p", "timeline_id": "t", "schema_version": 1,
        "base_parent": {"revision_id": "rev-0", "content_digest": "sha256:" + "0" * 64},
        "parent": {
            "config": {**copy.deepcopy(CANVAS), "tracks": [{"id": "V1", "kind": "visual"}, {"id": "V2", "kind": "visual"},
                                                           {"id": "A1", "kind": "audio"}]},
            "registry": {"assets": {"photo": {"media_id": "sha256:" + "4" * 64}, "song": {"media_id": "sha256:" + "5" * 64}}},
            "clips": _clips(),
        },
        "placements": [], "shots": {},
    }


def mixed():
    """The two-shot bundle with a parent clip added next to the shot clips."""
    value = shot_bundle()
    value["parent"]["clips"] = [{"id": "p-title", "clipType": "text", "track": "type", "at": 0.5, "hold": 1.0,
                                 "params": {"text": "Parent title"}}]
    return value


def _run(*argv) -> int:
    parsed = cli.build_parser(None).parse_args(list(argv))
    return parsed.handler(parsed)


def _file(tmp_path, value):
    path = tmp_path / "t.checkout.json"
    Checkout(value).save(path)
    return path


def _reload(path):
    return Checkout.load(path)


# ---- lookup -----------------------------------------------------------------------------

@pytest.mark.parametrize("query,expected", [("clip-1", "clip-1"), ("photo", "clip-1"), ("song", "clip-2"), ("Hello", "clip-3")])
def test_a_media_only_parent_is_found_by_id_asset_and_text(query, expected):
    clip = Checkout(media_only()).clip(query)
    assert clip.id == expected and clip.shot_id == PARENT_SHOT


def test_parent_clips_are_listed_with_timeline_absolute_clocks():
    tl = Checkout(media_only())
    assert [c.id for c in tl.clips()] == ["clip-1", "clip-2", "clip-3"]
    assert (tl.clip("clip-3").start, tl.clip("clip-3").end) == (1.0, 3.0)
    assert tl.clip("song").is_audio and not tl.clip("photo").is_audio


def test_a_missing_ref_still_says_so():
    with pytest.raises(TimelineEditError, match="no clip in the timeline matches 'nope'"):
        Checkout(media_only()).clip("nope")


def test_a_mixed_timeline_finds_both_kinds():
    tl = Checkout(mixed())
    assert tl.clip("p-title").shot_id == PARENT_SHOT
    assert tl.clip("a-rocket").shot_id == "A"
    assert {"p-title", "a-rocket", "b-type"} <= {c.id for c in tl.clips()}


def test_one_ref_on_a_parent_clip_and_a_shot_clip_is_ambiguous():
    value = mixed()
    value["parent"]["clips"].append({"id": "extra", "clipType": "am-type", "track": "type", "at": 5.0, "hold": 1.0, "params": {}})
    with pytest.raises(TimelineEditError, match="matches 2 clips") as raised:
        Checkout(value).clip("am-type")
    assert "extra" in str(raised.value) and "b-type" in str(raised.value)


def test_a_parent_mirror_in_config_clips_is_one_list():
    value = media_only()
    value["parent"]["config"]["clips"] = value["parent"].pop("clips")
    tl = Checkout(value)
    assert tl.clip("clip-1").id == "clip-1"
    tl.clip("clip-1").set(opacity=0.5)
    assert tl.bundle["parent"]["config"]["clips"][0]["opacity"] == 0.5


# ---- timelines edit --clip ------------------------------------------------------------------

@pytest.mark.parametrize("ref", ["clip-1", "photo"])
def test_edit_set_by_id_and_asset_on_a_media_only_parent(tmp_path, ref):
    path = _file(tmp_path, media_only())
    assert _run("edit", "--file", str(path), "--clip", ref, "--set", "opacity=0.5") == 0
    assert _reload(path).bundle["parent"]["clips"][0]["opacity"] == 0.5


def test_edit_set_by_text_on_a_media_only_parent(tmp_path):
    path = _file(tmp_path, media_only())
    assert _run("edit", "--file", str(path), "--clip", "Hello", "--set", 'text="Bye"') == 0
    assert _reload(path).bundle["parent"]["clips"][2]["params"]["text"] == "Bye"


def test_edit_timing_on_a_parent_clip_is_timeline_absolute(tmp_path):
    path = _file(tmp_path, media_only())
    assert _run("edit", "--file", str(path), "--clip", "clip-3", "--at", "2") == 0
    assert _reload(path).bundle["parent"]["clips"][2]["at"] == 2.0


def test_edit_remove_takes_the_parent_clip_off_the_parent(tmp_path):
    path = _file(tmp_path, media_only())
    assert _run("edit", "--file", str(path), "--clip", "clip-3", "--remove") == 0
    assert [c["id"] for c in _reload(path).bundle["parent"]["clips"]] == ["clip-1", "clip-2"]


def test_edit_on_a_mixed_timeline_edits_whichever_matched(tmp_path):
    path = _file(tmp_path, mixed())
    assert _run("edit", "--file", str(path), "--clip", "p-title", "--set", 'text="New"') == 0
    assert _run("edit", "--file", str(path), "--clip", "a-rocket", "--set", "x=4") == 0
    after = _reload(path).bundle
    assert after["parent"]["clips"][0]["params"]["text"] == "New"
    assert after["shots"]["A"]["internal_timeline"]["clips"][1]["params"]["x"] != 10


def test_edit_with_an_ambiguous_ref_across_parent_and_shot_exits_with_the_listing(tmp_path, capsys):
    value = mixed()
    value["parent"]["clips"].append({"id": "extra", "clipType": "am-type", "track": "type", "at": 5.0, "hold": 1.0, "params": {}})
    path = _file(tmp_path, value)
    assert _run("edit", "--file", str(path), "--clip", "am-type", "--set", "x=1") == 2
    err = capsys.readouterr().err
    assert "'am-type' matches 2 clips" in err and "extra" in err and "b-type" in err


# ---- the other commands that resolve a clip ref ----------------------------------------------

def test_crossfade_resolves_two_parent_audio_clips(tmp_path):
    value = media_only()
    value["parent"]["clips"].append({"id": "clip-4", "clipType": "media", "track": "A1", "asset": "song", "at": 5.0, "from": 0.0, "to": 4.0})
    path = _file(tmp_path, value)
    assert _run("edit", "--file", str(path), "--crossfade", "clip-2", "clip-4") == 0
    clips = {c["id"]: c for c in _reload(path).bundle["parent"]["clips"]}
    assert "fade" in str(clips["clip-2"]).lower() and "fade" in str(clips["clip-4"]).lower()


def test_crossfade_refuses_a_parent_picture_clip(tmp_path, capsys):
    path = _file(tmp_path, media_only())
    assert _run("edit", "--file", str(path), "--crossfade", "clip-1", "clip-2") == 2
    assert "requires two audio clips" in capsys.readouterr().err


def test_sequence_reaches_a_parent_clip_by_ref():
    with pytest.raises(TimelineEditError, match="clip-1 is not a step of a sequence"):
        Checkout(media_only()).sequence("clip-1")
