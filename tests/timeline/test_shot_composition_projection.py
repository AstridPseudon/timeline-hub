from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame, clip_timeline_duration
from astrid.core.timeline.shot_composition import MissingDependencyError
from astrid.core.timeline.shot_composition_projection import (
    ShotCompositionProjectionError,
    project_runtime_parent_composition,
    project_shot_composition,
    resolve_parent_tracks,
)
from astrid.sdk.timeline_editing import _clip_duration

FIXTURE = Path(__file__).parents[1] / "fixtures" / "timeline" / "shot_composition.json"


def graph() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_resolve_parent_tracks_keeps_parent_first_definitions_detached_and_lossless() -> None:
    parent = {"config": {"tracks": [
        {"id": "voice", "kind": "audio", "label": "Voice",
         "app": {"scaleAppliesToPositionedClips": False, "opaque": {"keep": [1, None]}}},
    ]}}
    children = [
        {"tracks": [
            {"id": "voice", "kind": "audio", "label": "Voice",
             "app": {"legacy": {"future": True}}},
            {"id": "voice", "kind": "audio", "label": "Voice",
             "app": {"same-child": "merged"}},
        ], "clips": [{"id": "a", "track": "voice"}]},
        {"tracks": [{"id": "voice", "kind": "audio", "label": "Voice",
                     "app": {"other": None}}], "clips": [{"id": "b", "track": "voice"}]},
        {"tracks": [{"id": "child", "kind": "visual", "label": "Child"}], "clips": []},
    ]
    before = copy.deepcopy((parent, children))

    resolved = resolve_parent_tracks(parent, children)

    assert [row["id"] for row in resolved] == ["voice", "child"]
    assert resolved[0]["app"] == {
        "scaleAppliesToPositionedClips": False,
        "opaque": {"keep": [1, None]},
        "legacy": {"future": True},
        "same-child": "merged",
        "other": None,
    }
    assert (parent, children) == before
    resolved[0]["app"]["opaque"]["keep"].append("detached")
    assert parent["config"]["tracks"][0]["app"]["opaque"]["keep"] == [1, None]


def test_resolve_parent_tracks_coalesces_exact_legacy_rows_parent_first() -> None:
    parent_row = {"id": "parent", "kind": "visual", "label": "Parent"}
    legacy_row = {"id": "legacy", "kind": "audio", "label": "Legacy"}
    resolved = resolve_parent_tracks(
        {"config": {"tracks": [parent_row]}},
        [{"tracks": [legacy_row], "clips": []}, {"tracks": [copy.deepcopy(legacy_row)], "clips": []}],
    )
    assert resolved == [parent_row, legacy_row]
    assert [row["id"] for row in resolved] == ["parent", "legacy"]


@pytest.mark.parametrize("film_label,child_label", [(True, False), (False, True), (False, False), (True, True)])
def test_legacy_optional_track_label_is_lossless_and_detached(film_label, child_label):
    film = {"id": "video", "kind": "visual"}
    child = copy.deepcopy(film)
    for row, supplied in ((film, film_label), (child, child_label)):
        if supplied:
            row["label"] = " Video · exact "
    before = copy.deepcopy((film, child))
    resolved = resolve_parent_tracks({"config": {"tracks": [film]}}, [
        {"tracks": [child], "clips": [{"id": "clip", "track": "video"}]},
    ])
    expected = {"id": "video", "kind": "visual"}
    if film_label or child_label:
        expected["label"] = " Video · exact "
    assert resolved == [expected]
    assert (film, child) == before


@pytest.mark.parametrize("field,value", [
    ("label", "Other"), ("label", None), ("label", ""), ("label", 1),
    ("kind", "audio"), ("gain", 0.5), ("volume", 0), ("muted", False),
    ("mute", False), ("timing", {"offset": 0}), ("routing", []),
    ("future", {"keep": None}),
])
def test_optional_label_does_not_hide_supplied_or_semantic_conflicts(field, value):
    film = {"id": "video", "kind": "visual", "label": "Video"}
    child = {"id": "video", "kind": "visual", field: value}
    before = copy.deepcopy((film, child))
    with pytest.raises(ShotCompositionProjectionError):
        resolve_parent_tracks({"config": {"tracks": [film]}}, [{"tracks": [child]}])
    assert (film, child) == before


@pytest.mark.parametrize(
    ("parent_tracks", "children", "message"),
    [
        ([{"id": "x", "kind": "audio"}, {"id": "x", "kind": "audio"}], [], "duplicate id"),
        ([{"id": "x", "kind": "audio"}],
         [{"tracks": [{"id": "x", "kind": "visual"}], "clips": []}], "conflicts"),
        ([{"id": "x", "kind": "audio", "muted": False}],
         [{"tracks": [{"id": "x", "kind": "audio", "muted": 0}], "clips": []}], "conflicts"),
        ([{"id": "x", "kind": "audio", "app": {"mode": "a"}}],
         [{"tracks": [{"id": "x", "kind": "audio", "app": {"mode": "b"}}], "clips": []}], "conflicts"),
        ([], [{"tracks": [], "clips": [{"id": "c", "track": "missing"}]}], "missing track"),
        ([], [{"tracks": [], "clips": [{"id": "c", "track": None}]}], "non-empty string"),
        ([], [{"tracks": [{"id": "x", "app": None}], "clips": []}], "app must be an object"),
    ],
)
def test_resolve_parent_tracks_rejects_conflicts_and_invalid_references(parent_tracks, children, message):
    with pytest.raises(ShotCompositionProjectionError, match=message):
        resolve_parent_tracks({"config": {"tracks": parent_tracks}}, children)


def test_runtime_projection_resolves_parent_owned_tracks_without_child_mirrors() -> None:
    parent = {
        "project_id": "p", "timeline_id": "t", "revision_id": "parent-r1",
        "payload": {
            "config": {"fps": 24, "tracks": [{"id": "voice", "kind": "audio", "label": "Voice",
                                                  "app": {"scaleAppliesToPositionedClips": True}}],
                       "clips": []},
            "clips": [],
            "registry": {"assets": {}},
            "occurrences": [{"occurrence_id": "o1", "shot_id": "s1", "shot_revision_id": "sr1",
                              "at_ms": 0, "duration_ms": 1000}],
        },
    }
    shots = [{"shot_id": "s1", "revision_id": "sr1", "internal_timeline_revision_id": "ir1"}]
    internals = [{"revision_id": "ir1", "payload": {
        "tracks": [],
        "clips": [{"id": "voiceover", "clipType": "media", "track": "voice",
                   "at": 0, "hold": 1}],
        "registry": {"assets": {}},
    }}]
    before = copy.deepcopy((parent, shots, internals))

    projected = project_runtime_parent_composition(
        parent, shot_revisions=shots, internal_timeline_revisions=internals
    )

    assert projected.config["tracks"] == [{"id": "voice", "kind": "audio", "label": "Voice",
                                            "app": {"scaleAppliesToPositionedClips": True}}]
    assert projected.config["clips"][0]["track"] == "voice"
    assert (parent, shots, internals) == before
    assert internals[0]["payload"]["tracks"] == []

    internals[0]["payload"]["clips"][0]["track"] = "missing"
    with pytest.raises(ShotCompositionProjectionError, match="missing track"):
        project_runtime_parent_composition(
            parent, shot_revisions=shots, internal_timeline_revisions=internals
        )


def test_projection_preserves_frames_trim_audio_and_occurrence_placement() -> None:
    source = graph()
    revision = next(item for item in source["shot_revisions"] if item["shot_id"] == "shot-alpha" and item["revision_id"] == "rev-a")
    revision["internal_timeline_revision"]["timeline"]["clips"][0].pop("duration_ms")
    revision["internal_timeline_revision"]["timeline"]["clips"][0].update({"from": 2, "to": 10, "speed": 2})
    occurrence = source["occurrences"][0]
    occurrence.update({"duration_ms": 1000, "source_offset": 7, "speed": 1.5, "gain": 0.5, "muted": True})

    projected = project_shot_composition(source)
    video = next(item for item in projected.config["clips"] if item["shot_occurrence_id"] == "occ-1" and item["app"]["astrid_shot_composition"]["source_clip_id"] == "alpha-video")
    assert video["at"] == 0
    assert video["from"] == 2
    assert video["to"] == 4  # one second of the two-times-speed source remains
    assert video["volume"] == 0
    assert video["app"]["astrid_shot_composition"]["source_offset"] == 7
    assert video["app"]["astrid_shot_composition"]["speed"] == 1.5
    assert video["app"]["astrid_shot_composition"]["muted"] is True
    assert clip_start_frame(video, 30) == 0
    assert clip_end_frame(video, 30) == 30

    audio = next(item for item in projected.config["clips"] if item["shot_occurrence_id"] == "occ-1" and item["app"]["astrid_shot_composition"]["source_clip_id"] == "alpha-audio")
    assert audio["track"] == "audio"
    assert audio["hold"] == 1


def test_linked_occurrences_remain_distinct_and_export_metadata_is_qualified() -> None:
    projected = project_shot_composition(graph())
    linked = [item for item in projected.config["clips"] if item.get("shot_id") == "shot-alpha"]
    assert {item["shot_occurrence_id"] for item in linked} >= {"occ-1", "occ-2", "occ-3"}
    assert len({item["id"] for item in linked}) == len(linked)
    assert projected.outputs[0]["output_identity"].endswith("occurrence/occ-1/output/final-video")
    assert projected.outputs[0]["output_identity"] != projected.outputs[1]["output_identity"]
    assert projected.config["app"]["astrid_shot_composition"]["outputs"][0]["occurrence_id"] == "occ-1"


def test_projection_reports_missing_dependency_before_downstream_reads() -> None:
    source = graph()
    source["shot_revisions"][1]["dependencies"] = [{"shot_id": "missing", "revision_id": "rev-x", "required": True}]
    with pytest.raises(MissingDependencyError):
        project_shot_composition(source)


def test_deeper_nesting_and_unsupported_compositing_fail_closed() -> None:
    nested = graph()
    nested["shot_revisions"][0]["internal_timeline_revision"]["timeline"]["clips"][0]["clip_type"] = "shot"
    with pytest.raises(ShotCompositionProjectionError, match="deeper shot nesting"):
        project_shot_composition(nested)

    compositing = graph()
    compositing["shot_revisions"][0]["internal_timeline_revision"]["timeline"]["compositing"] = "screen"
    with pytest.raises(ShotCompositionProjectionError, match="unsupported compositing"):
        project_shot_composition(compositing)


def test_blank_child_keeps_bounded_occurrence_and_blank_output_metadata() -> None:
    source = graph()
    revision = next(item for item in source["shot_revisions"] if item["shot_id"] == "shot-beta")
    revision["internal_timeline_revision"]["timeline"]["clips"] = []
    projected = project_shot_composition(source)
    output = next(item for item in projected.outputs if item["occurrence_id"] == "occ-4")
    assert output["blank"] is True
    assert output["duration_ms"] == 1200
    assert not any(item.get("shot_occurrence_id") == "occ-4" for item in projected.config["clips"])
    occurrence = next(item for item in projected.config["app"]["astrid_shot_composition"]["occurrences"] if item["occurrence_id"] == "occ-4")
    assert occurrence["blank"] is True
    assert occurrence["duration_seconds"] == 1.2


def test_projects_all_child_audio_clips_and_preserves_legacy_audio_as_read_only_metadata() -> None:
    source = graph()
    revision = next(item for item in source["shot_revisions"] if item["shot_id"] == "shot-alpha" and item["revision_id"] == "rev-a")
    timeline = revision["internal_timeline_revision"]["timeline"]
    timeline["clips"].append({
        "id": "alpha-audio-second",
        "clip_type": "media",
        "track": "audio",
        "at_ms": 500,
        "duration_ms": 700,
        "asset_id": "alpha-image",
    })
    legacy_audio = copy.deepcopy(revision["audio"])

    projected = project_shot_composition(source)
    child_audio = [clip for clip in projected.config["clips"] if clip["track"] == "audio"]

    assert {clip["id"] for clip in child_audio} >= {"occ-1:alpha-audio", "occ-1:alpha-audio-second"}
    assert projected.graph["shot_revisions"][1]["audio"] == legacy_audio
    assert "audio" not in projected.config


def test_managed_media_type_is_authoritative_and_unknown_media_stays_unknown() -> None:
    source = graph()
    revision = next(item for item in source["shot_revisions"] if item["shot_id"] == "shot-alpha" and item["revision_id"] == "rev-a")
    revision["assets"][0]["media_type"] = "image/png"
    revision["assets"][0]["type"] = "video"
    revision["assets"].append({
        "asset_id": "future-media",
        "object_id": "object-future-media",
        "digest": "sha256:" + "a" * 64,
        "scope": {"project_id": "project-001"},
        "role": "image",
        "media_type": "application/x-future",
    })
    revision["assets"].append({
        "asset_id": "missing-kind",
        "object_id": "object-missing-kind",
        "digest": "sha256:" + "b" * 64,
        "scope": {"project_id": "project-001"},
        "role": "image",
    })

    projected = project_shot_composition(source)

    assert projected.registry["assets"]["alpha-image"]["type"] == "image"
    assert projected.registry["assets"]["future-media"]["type"] == "unknown"
    assert projected.registry["assets"]["missing-kind"]["type"] == "unknown"


def test_invalid_present_managed_media_type_is_rejected() -> None:
    source = graph()
    revision = next(item for item in source["shot_revisions"] if item["shot_id"] == "shot-alpha" and item["revision_id"] == "rev-a")
    revision["assets"][0]["media_type"] = {"type": "image/png"}

    with pytest.raises(ShotCompositionProjectionError, match="media_type must be a non-empty string"):
        project_shot_composition(source)


@pytest.mark.parametrize(
    ("vector_id", "clip", "expected_duration", "expected_frames"),
    [
        ("hold-plain", {"id": "hold-plain", "at": 0.125, "hold": 0.5, "speed": 1}, 0.5, (4, 19)),
        ("duration-ms-fast", {"id": "duration-ms-fast", "at": 0.001, "hold": 0.017, "speed": 2}, 0.0085, (0, 1)),
        ("trim-slow", {"id": "trim-slow", "at": 0.1, "from": 2, "to": 3, "speed": 0.5}, 2, (3, 63)),
        ("trim-fast", {"id": "trim-fast", "at": 0.1, "from": 2, "to": 6, "speed": 2}, 2, (3, 63)),
        ("hold-fast-clipped", {"id": "hold-fast-clipped", "at": 0.25, "hold": 1.5, "speed": 2}, 0.75, (8, 31)),
        ("hold-slow-clipped", {"id": "hold-slow-clipped", "at": 0, "hold": 0.625, "speed": 0.5}, 1.25, (0, 38)),
    ],
)
def test_shared_visible_time_vectors_match_sdk_and_renderer_rounding(
    vector_id: str,
    clip: dict,
    expected_duration: float,
    expected_frames: tuple[int, int],
) -> None:
    assert _clip_duration(clip) == pytest.approx(expected_duration), vector_id
    assert clip_timeline_duration(clip) == pytest.approx(expected_duration), vector_id
    assert (clip_start_frame(clip, 30), clip_end_frame(clip, 30)) == expected_frames


@pytest.mark.parametrize(
    ("speed", "source_hold", "occurrence_duration", "expected_source_hold"),
    [
        (2, 4, 0.75, 1.5),
        (0.5, 1, 1.25, 0.625),
    ],
)
def test_projection_caps_visible_time_without_applying_speed_twice_or_mutating_source(
    speed: float,
    source_hold: float,
    occurrence_duration: float,
    expected_source_hold: float,
) -> None:
    source = graph()
    first_occurrence = source["occurrences"][0]
    source["occurrences"] = [first_occurrence]
    first_occurrence["duration_ms"] = round(occurrence_duration * 1000)
    revision = next(
        item for item in source["shot_revisions"]
        if item["shot_id"] == first_occurrence["shot_id"] and item["revision_id"] == first_occurrence["revision_id"]
    )
    timeline = revision["internal_timeline_revision"]["timeline"]
    original_clip = copy.deepcopy(timeline["clips"][0])
    timeline["clips"] = [{
        **original_clip,
        "id": "speed-vector",
        "at_ms": 0,
        "hold": source_hold,
        "speed": speed,
    }]
    timeline["clips"][0].pop("duration_ms", None)

    projected = project_shot_composition(source)
    clip = projected.config["clips"][0]

    assert clip["hold"] == pytest.approx(expected_source_hold)
    assert clip_timeline_duration(clip) == pytest.approx(occurrence_duration)
    assert timeline["clips"][0]["hold"] == source_hold
    assert timeline["clips"][0]["speed"] == speed
