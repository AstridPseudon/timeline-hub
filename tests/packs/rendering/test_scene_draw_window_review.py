"""Registered checks join public preroll against the complete identity universe."""
import copy

import pytest

from astrid.packs.rendering.actions.timeline_visualize.motion import conditions, lint, model
from tests.packs.rendering.test_motion_cover_public import (
    clip,
    cover,
    elements,
    timeline,
)
from tests.packs.rendering.test_motion_cover_public import public_query as _public_query

public_query = _public_query
CUT = {"index": 1, "start": .7, "end": .9}


def preroll(kind="am-type"):
    return timeline([
        clip("a", "back", x=700),
        clip("b", "back", kind, at=1, x=1900,
             transition={"type": "fade", "duration": .4}),
        clip("upper", "front", "am-callout", hold=2, x=1890, width=120),
    ])


def registered(cut, source, shared=None):
    per_cut, whole = conditions.run_checks([cut], source, 30, only=["composition"], shared=shared)
    assert whole == []
    return per_cut[0][1]


@pytest.mark.integration
@pytest.mark.parametrize("kind", ["am-type", "am-callout"])
def test_registered_composition_check_keeps_public_incoming_preroll(public_query, kind):
    config = preroll(kind)
    if kind == "am-callout":
        config["clips"][-1]["params"]["rect"]["x"] = 300
    source = elements(config)
    inside = model.in_window(source, CUT["start"], CUT["end"])
    assert [e.id for e in inside] == ["a", "upper"]
    assert lint._sample_times(CUT, inside, 30) == [.8]
    shared = public_query(config, [24])
    assert [layer["clipId"] for layer in shared["scene_frames"]["24"]["layers"]] == ["a", "b", "upper"]
    assert 'data-clip="b"' in shared["html"]["24"]
    assert shared["scene_occlusions"]["0.98"]["24"]["b"]["occluderId"] == (
        "upper" if kind == "am-type" else None)

    found = registered(CUT, source, shared)
    if kind == "am-callout":
        assert any(f.code == "FRAME" and 'am-callout "b" is cut off: 80 px' in f.message for f in found), found
        assert not cover(found)
    else:
        assert cover(found) == ['am-callout "upper" fully covers am-type "b"']
    assert {f.t for f in found} == {.8}
    assert not any(f.code == "SCENE" for f in found)


@pytest.mark.integration
@pytest.mark.parametrize("change", ["stale", "unknown", "ambiguous"])
def test_preroll_unavailable_facts_are_advisory(public_query, change):
    config = preroll("am-callout")
    config["clips"][-1]["params"]["rect"]["x"] = 300
    source = elements(config)
    shared = public_query(config, [24])
    if change == "stale":
        shared["scene_frames"]["24"]["frame"] = 23
    elif change == "unknown":
        shared["scene_occlusions"]["0.98"]["24"]["b"] = {"status": "unknown", "reason": "unknown support"}
        layer = next(row for row in shared["scene_frames"]["24"]["layers"] if row["clipId"] == "b")
        layer["bounds"] = {"status": "unknown", "reason": "unknown layout"}
    else:
        # The duplicate lies outside the authored selection too; it must never
        # become a unique identity merely because the caller filtered it out.
        source.append(copy.deepcopy(next(e for e in source if e.id == "b")))
    found = registered(CUT, source, shared)
    assert not cover(found)
    assert not any(f.code == "FRAME" and '"b"' in f.message for f in found)
    for code in ("SCENE", "REGION"):
        assert any(f.code == code and f.severity == "info" and
                   (change == "stale" or '"b"' in f.message) for f in found), (code, found)


@pytest.mark.integration
def test_registered_half_open_end_does_not_infer_presence(public_query):
    config = preroll("am-callout")
    shared = public_query(config, [60])
    assert shared["scene_frames"]["60"]["layers"] == []
    assert registered({"index": 1, "start": 1.9, "end": 2.1}, elements(config), shared) == []


@pytest.mark.integration
def test_preroll_join_keeps_distinct_occurrences(public_query):
    config = preroll()
    source = elements(config)
    incoming = next(e for e in source if e.id == "b")
    incoming.occurrence_id = "incoming"
    other = copy.deepcopy(incoming)
    other.occurrence_id = "other"
    source.append(other)
    shared = public_query(config, [24])
    shared["scene_clip_identities"]["b"]["occurrence_id"] = "incoming"
    assert cover(registered(CUT, source, shared)) == ['am-callout "upper" fully covers am-type "b"']


def test_identity_universe_does_not_expand_selected_samples(monkeypatch):
    # This out-of-window element has a settled key sample inside the cut. It
    # belongs to the identity join, but must not spend a new sample reservation.
    source = [model.Element("ended", "am-type", "back", .65, .7, {"punchAt": [0]}, {})]
    cut = {"index": 1, "start": .7, "end": 1.3}
    assert lint._sample_times(cut, source, 30) == [1.0, 1.05]
    samples = []
    monkeypatch.setattr(lint, "_scene_boxes", lambda elements, t, fps, shared:
                        (samples.append(t) or [], {}, model.CANVAS, []))
    registered(cut, source, {"scene_frames": {}})
    assert samples == [1.0]


@pytest.mark.parametrize("shared", [None, {}, {"scene_unavailable": "no capture handoff"}])
def test_legacy_registered_path_keeps_authored_selection(monkeypatch, shared):
    source = elements(preroll("am-callout"))
    seen = []
    monkeypatch.setattr(model, "boxes_at", lambda element, *args: seen.append(element.id) or [])
    registered(CUT, source, shared)
    assert seen == ["a", "upper"]
