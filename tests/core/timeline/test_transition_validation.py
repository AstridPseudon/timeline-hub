"""Canonical incoming declarations and native compiled outgoing validation."""

from copy import deepcopy

import jsonschema
import pytest

from astrid.core.timeline import banodoco_schema
from astrid.core.timeline.validators.timeline import validate_timeline


@pytest.fixture(autouse=True)
def transition_catalog(monkeypatch):
    monkeypatch.setattr(banodoco_schema, "_transition_ids", lambda: {"fade", "cross-fade"})


def clip(clip_id, at, duration, *, track="v1", transition=None):
    result = {"id": clip_id, "at": at, "hold": duration, "track": track}
    if transition is not None:
        result["transition"] = transition
    return result


def config(clips, *, fps=30):
    return {
        "tracks": [],
        "clips": clips,
        "theme_overrides": {"visual": {"canvas": {"fps": fps}}},
    }


@pytest.mark.parametrize("duration", [{"duration": 0.4}, {"durationFrames": 12}])
def test_incoming_owner_is_not_constrained_by_short_successor(duration):
    timeline = config([
        clip("a", 0, 2),
        clip("b", 2, 1, transition={"id": "fade", **duration}),
        clip("c", 3, 0.1),
    ])
    before = deepcopy(timeline)
    validate_timeline(timeline, document_kind="canonical")
    assert timeline == before
    # Native b owns the transition into c; canonical b owns the one from a.
    with pytest.raises(ValueError, match=r"clips\[1\].transition.*fit both adjacent"):
        validate_timeline(timeline, document_kind="compiled")
    with pytest.raises(ValueError, match="fit both adjacent"):
        validate_timeline(timeline)


def test_incoming_window_can_exceed_predecessor_as_well_as_owner():
    timeline = config([
        clip("a", 0, 0.1),
        clip("b", 0.1, 0.2, transition={"id": "fade", "duration": 2}),
        clip("c", 0.3, 3),
    ])
    validate_timeline(timeline, document_kind="canonical")
    with pytest.raises(ValueError, match="fit both adjacent"):
        validate_timeline(timeline, document_kind="compiled")


@pytest.mark.parametrize("at,frames", [(1, 12), (2, 12), (0.5, 12), (1, 60)])
@pytest.mark.parametrize("transition_id", ["fade", "crossfade", "cross-fade"])
def test_canonical_adjacent_gap_overlap_and_oversized_windows(at, frames, transition_id):
    timeline = config([
        clip("a", 0, 1),
        clip("b", at, 1, transition={"type": transition_id, "durationFrames": frames}),
    ])
    before = deepcopy(timeline)
    validate_timeline(timeline, document_kind="canonical")
    # Validation does not move ownership, clamp windows, or add an endpoint.
    assert timeline == before


@pytest.mark.parametrize("at", [0, 2])
@pytest.mark.parametrize("transition", ["fade", {"id": "crossfade", "duration": 2}])
def test_first_clip_accepts_incoming_transition_without_predecessor(at, transition):
    validate_timeline(
        config([clip("first", at, 1, transition=transition)]),
        document_kind="canonical",
    )


def test_track_order_and_original_indices_are_preserved():
    timeline = config([
        clip("c", 3, 0.1),
        clip("overlay", 1.9, 0.01, track="v2"),
        clip("b", 2, 1, transition={"id": "fade", "duration": 0.4}),
        clip("a", 0, 2),
    ])
    before = deepcopy(timeline)
    validate_timeline(timeline, document_kind="canonical")
    with pytest.raises(ValueError, match=r"clips\[2\].transition.*fit both adjacent"):
        validate_timeline(timeline, document_kind="compiled")
    assert timeline == before


def test_native_successor_is_chosen_by_time_on_same_track():
    timeline = config([
        clip("b", 2, 1, transition={"id": "fade", "duration": 0.4}),
        clip("other-track", 2.1, 0.01, track="v2"),
        clip("c", 3, 2),
        clip("a", 0, 0.1),
    ])
    # Neither the short predecessor nor the interleaved track owns native b's pair.
    validate_timeline(timeline, document_kind="compiled")
    validate_timeline(timeline, document_kind="canonical")


@pytest.mark.parametrize("document_kind", ["canonical", "compiled"])
@pytest.mark.parametrize("fps", [24, 30, 60, 30000 / 1001])
def test_frames_and_seconds_at_exact_half_open_cut(document_kind, fps):
    seconds = 12 / fps
    for duration in ({"duration": seconds}, {"durationFrames": 12}):
        timeline = config([
            clip("a", 0, seconds, transition={"id": "fade", **duration}),
            clip("b", seconds, seconds),
        ], fps=fps)
        before = deepcopy(timeline)
        validate_timeline(timeline, document_kind=document_kind)
        assert timeline == before


def test_native_frame_duration_has_precedence_over_seconds():
    timeline = config([
        clip("a", 0, 1, transition={"id": "fade", "durationFrames": 12, "duration": 2}),
        clip("b", 1, 1),
    ])
    validate_timeline(timeline, document_kind="compiled")
    del timeline["clips"][0]["transition"]["durationFrames"]
    with pytest.raises(ValueError, match="fit both adjacent"):
        validate_timeline(timeline, document_kind="compiled")


@pytest.mark.parametrize("document_kind", ["canonical", "compiled"])
def test_from_alias_remains_valid_without_mutating_source(document_kind):
    timeline = config([
        {"id": "a", "at": 0, "track": "v1", "from_": 2, "to": 3,
         "transition": {"id": "fade", "durationFrames": 12}},
        clip("b", 1, 1),
    ])
    before = deepcopy(timeline)
    validate_timeline(timeline, document_kind=document_kind)
    assert timeline == before


@pytest.mark.parametrize("document_kind", ["canonical", "compiled"])
@pytest.mark.parametrize("field", ["duration", "durationFrames"])
@pytest.mark.parametrize("value", [0, -1, True, False, None, "1", float("nan"), float("inf"), -float("inf")])
def test_rejects_malformed_or_nonfinite_duration(document_kind, field, value):
    # Include a valid preferred duration so malformed secondary fields cannot hide.
    transition = {"id": "fade", "durationFrames": 12, field: value}
    with pytest.raises((ValueError, jsonschema.ValidationError)):
        validate_timeline(
            config([clip("a", 0, 1, transition=transition)]),
            document_kind=document_kind,
        )


@pytest.mark.parametrize("document_kind", ["canonical", "compiled"])
@pytest.mark.parametrize("transition", ["", {"id": ""}, {"id": "fade", "params": []}, {"id": "fade", "extra": 1}, 42])
def test_rejects_malformed_reference(document_kind, transition):
    with pytest.raises((ValueError, jsonschema.ValidationError)):
        validate_timeline(
            config([clip("a", 0, 1, transition=transition)]),
            document_kind=document_kind,
        )


@pytest.mark.parametrize("document_kind", ["canonical", "compiled"])
def test_unknown_id_retains_original_index_in_error(document_kind):
    with pytest.raises(ValueError, match=r"clips\[0\].transition.*transitions catalog"):
        validate_timeline(
            config([clip("b", 1, 1, transition="unknown"), clip("a", 0, 1)]),
            document_kind=document_kind,
        )


def test_canonical_alias_does_not_widen_native_catalog():
    timeline = config([clip("a", 0, 1, transition="crossfade")])
    validate_timeline(timeline, document_kind="canonical")
    with pytest.raises(ValueError, match="transitions catalog"):
        validate_timeline(timeline, document_kind="compiled")


def test_unknown_document_kind_is_refused():
    with pytest.raises(ValueError, match="document_kind"):
        validate_timeline(config([]), document_kind="guess")
