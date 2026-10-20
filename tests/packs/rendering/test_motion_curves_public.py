"""Curves consume exact captured intrinsic scalars without a private formula fallback."""
import copy
from fractions import Fraction

import pytest
from PIL import Image

from astrid.core.timeline import scene_answers
from astrid.core.timeline.cuts import occurrences_from_snapshot
from astrid.packs.rendering.actions.timeline_visualize import composed_frame
from astrid.packs.rendering.actions.timeline_visualize.layers import builtin
from astrid.packs.rendering.actions.timeline_visualize.layers.base import LayerContext
from astrid.packs.rendering.actions.timeline_visualize.motion import model, sheet
from tests.packs.rendering import test_scene_sampling_plan as sampling
from tests.packs.rendering.test_motion_diagnostics_public import (
    clip,
    timeline,
)
from tests.packs.rendering.test_motion_diagnostics_public import (
    public_diagnostics as _public_diagnostics,
)
from tests.packs.rendering.test_scene_sampling_plan import (
    MetadataProvider,
    composed_snapshot,
    run_pack,
)

public_diagnostics = _public_diagnostics
public_occlusion = sampling.public_occlusion


def context(elements, shared, frames=(12, 15)):
    return LayerContext(cut={"index": 1, "start": 0, "end": 1}, cuts=[], window=(0, 1), fps=30,
                        elements=elements, all_elements=elements, words=[], beats={}, sfx=[], events=[],
                        shared={"curve_frames": list(frames), "fps_rational": [30, 1], **shared})


def forbid_private(*args, **kwargs):
    pytest.fail("captured public curves must not evaluate a private model")


@pytest.fixture
def no_private(monkeypatch):
    monkeypatch.setattr(model, "props_at", forbid_private)
    monkeypatch.setattr(model, "mouth_state", forbid_private)
    monkeypatch.setattr(model, "own_motion", forbid_private)


@pytest.mark.integration
def test_public_intrinsic_scalars_use_the_prepared_component_content_clock(public_diagnostics, no_private):
    config = timeline([clip("card")])
    config["clips"][0]["hold"] = 2
    config["clips"][0]["speed"] = 2
    shared = public_diagnostics(config)
    elements = model.elements_from_occurrences(occurrences_from_snapshot(config))
    ctx = context(elements, shared)
    for frame in (12, 15):
        layer = shared["scene_frames"][str(frame)]["layers"][0]
        assert layer["diagnostics"]["motion"] == {"position": frame * 2}
        assert builtin._scene_motion(ctx, elements[0], frame) == (layer["diagnostics"]["motion"], None)
    result = builtin.render_curves(ctx)
    assert result.image is not None
    assert any("intrinsic position:" in f and "2 public samples; component units" in f for f in result.findings)
    assert not any("static over" in f or "mirror" in f or "unavailable" in f for f in result.findings)


@pytest.mark.integration
def test_repeated_source_clips_join_by_explicit_occurrence(public_diagnostics, no_private):
    snapshot = composed_snapshot()
    # Overlapping occurrences with different speed cannot be disambiguated by
    # authored time, source ID, label, or a suffix of the compiled ID.
    clips = [copy.deepcopy(c) for c in snapshot["config"]["clips"]
             if c["app"]["astrid_shot_composition"]["source_clip_id"] == "lower"]
    for c in clips:
        c["at"] = 0
        c["track"] = c["id"]
        if c["app"]["astrid_shot_composition"]["occurrence_id"] == "occ-2":
            c["speed"] = 2
    shared = public_diagnostics(timeline(clips))
    _, elements = sheet.snapshot_elements(snapshot)
    ctx = context(elements, shared)
    first, second = [e for e in elements if e.clip["app"]["astrid_shot_composition"]["source_clip_id"] == "lower"]
    assert first.occurrence_id != second.occurrence_id
    assert builtin._scene_motion(ctx, first, 12) == ({"position": 12}, None)
    assert builtin._scene_motion(ctx, second, 12) == ({"position": 24}, None)


def facts():
    element = model.Element("card", "am-type", "text", 0, 1, {}, {"id": "card"}, occurrence_id="o1")
    shared = {"scene_frames": {str(f): {"frame": f, "layers": [
        {"clipId": "compiled", "diagnostics": {"motion": {"x": f}}}]} for f in (12, 15)},
        "scene_clip_identities": {"compiled": {"clip_id": "card", "occurrence_id": "o1"}}}
    return element, shared


@pytest.mark.parametrize("problem", ["missing-row", "stale-row", "unavailable", "missing-motion", "unknown-motion",
                                    "invalid-number", "bool-number", "missing-identity", "wrong-occurrence",
                                    "wrong-source", "duplicate-layer", "duplicate-mapping", "duplicate-element"])
def test_missing_stale_unknown_and_duplicate_facts_stay_advisory(problem, no_private):
    element, shared = facts()
    row = shared["scene_frames"]["12"]
    layer = row["layers"][0]
    elements = [element]
    if problem == "missing-row":
        shared["scene_frames"].pop("12")
    elif problem == "stale-row":
        row["frame"] = 11
    elif problem == "unavailable":
        shared["scene_unavailable"] = "cached pixels have no current scene facts"
    elif problem == "missing-motion":
        layer.pop("diagnostics")
    elif problem == "unknown-motion":
        layer["diagnostics"]["motion"] = None
    elif problem == "invalid-number":
        layer["diagnostics"]["motion"]["x"] = float("nan")
    elif problem == "bool-number":
        layer["diagnostics"]["motion"]["x"] = True
    elif problem == "missing-identity":
        shared["scene_clip_identities"].clear()
    elif problem == "wrong-occurrence":
        shared["scene_clip_identities"]["compiled"]["occurrence_id"] = "o2"
    elif problem == "wrong-source":
        shared["scene_clip_identities"]["compiled"]["clip_id"] = "other"
    elif problem == "duplicate-layer":
        row["layers"].append(copy.deepcopy(layer))
    elif problem == "duplicate-mapping":
        shared["scene_clip_identities"]["other"] = dict(shared["scene_clip_identities"]["compiled"])
    else:
        elements.append(copy.deepcopy(element))
    ctx = context(elements, shared)
    values, reason = builtin._scene_motion(ctx, element, 12)
    assert values == {} and reason
    result = builtin.render_curves(ctx)
    assert any("unavailable at frame 12:" in f for f in result.findings)
    assert not any("static" in f or "mirror" in f for f in result.findings)


def test_unknown_sample_leaves_a_gap_in_the_plot(monkeypatch, no_private):
    element, shared = facts()
    shared["scene_frames"]["13"] = {"frame": 13, "layers": []}
    ctx = context([element], shared, frames=(12, 13, 15))
    lines = []
    original = builtin.ImageDraw.ImageDraw.line

    def record(draw, xy, *args, **kwargs):
        if kwargs.get("fill") in builtin.SERIES:
            lines.append(xy)
        return original(draw, xy, *args, **kwargs)

    monkeypatch.setattr(builtin.ImageDraw.ImageDraw, "line", record)
    builtin.render_curves(ctx)
    assert lines == []  # no bridge over unknown frame 13


def test_legacy_context_keeps_its_existing_model(monkeypatch):
    element, _ = facts()
    ctx = context([element], {})
    ctx.shared.pop("curve_frames")
    calls = []
    monkeypatch.setattr(model, "props_at", lambda e, t, fps: calls.append((t, fps)) or {"visible": 1.0})
    result = builtin.render_curves(ctx)
    assert len(calls) == 30 and result.image is not None
    assert any("static over the cut" in f for f in result.findings)


@pytest.mark.parametrize("fps", [Fraction(30), Fraction(30000, 1001), Fraction(24000, 1001)])
def test_curve_sampling_is_bounded_deterministic_and_half_open(fps):
    window = (Fraction(1001, 30000), Fraction(1001 * 137, 30000))
    planned = sheet.curve_sample_frames(window, fps)
    assert planned == sheet.curve_sample_frames(window, fps)
    assert len(planned) <= 60 and planned == sorted(set(planned))
    assert all(window[0] <= Fraction(f, 1) / fps < window[1] for f in planned)
    # An end exactly on a frame never includes that frame.
    assert sheet.curve_sample_frames((0, Fraction(2, 1) / fps), fps) == [0, 1]
    assert sheet.curve_sample_frames(tuple(float(t) for t in window), fps) == planned


@pytest.mark.parametrize("fps", [Fraction(30), Fraction(30000, 1001), Fraction(24000, 1001)])
def test_curve_metadata_shares_the_existing_extra_budget_and_preserves_lint_samples(fps):
    cut = {"index": 1, "start": 0, "end": 5}
    element = model.Element("keys", "am-type", "text", 0, 5, {"punchAt": list(range(1, 50))}, {})
    old = sheet.plan_scene_frames([cut], [element], float(fps))
    curves = sheet.curve_sample_frames((0, 5), fps)
    planned = sheet.plan_scene_frames([cut], [element], fps, curve_window=(0, 5))
    assert planned[:len(old)] == old and len(planned) == 60
    assert set(planned) <= set(old + curves)
    assert sheet.plan_scene_frames([cut], [], fps, pixel_frames=curves,
                                   curve_window=(0, 5), composition=False) == []


def test_selected_curve_layer_reserves_only_its_panel_samples_without_pixel_changes(tmp_path, monkeypatch):
    provider = MetadataProvider()
    ctx = run_pack(tmp_path, monkeypatch, provider, layers=("curves",))
    expected = sheet.curve_sample_frames(ctx.window, Fraction(30))
    assert provider.reserved == [f for f in expected if f not in provider.pixels]
    assert ctx.shared["curve_frames"] == expected
    assert all(f < 120 for f in provider.reserved)  # no queries for the second occurrence
    assert len(provider.reserved) <= 60


@pytest.mark.integration
def test_real_provider_queries_one_pixel_metadata_union_and_cached_facts_do_not_fall_back(
    tmp_path, monkeypatch, public_diagnostics, public_occlusion, no_private,
):
    snapshot = composed_snapshot()
    config = timeline([clip("card")])
    config["clips"][0]["hold"] = 10
    snapshot.update(config=config, clips=config["clips"], duration_frames=300)
    props = {"timeline": config, "assets": snapshot["registry"],
             "theme": {"visual": {"canvas": {"width": 1920, "height": 1080, "fps": 30}}}}
    queries, renders = [], []

    def query(actual, basis, frames):
        assert actual is props
        queries.append(list(frames))
        return list(public_diagnostics(actual["timeline"], frames)["scene_frames"].values())

    def render(frames, output, resolution):
        renders.append(list(frames))
        provider._scene_labels(props, frames)
        result = {}
        for frame in frames:
            path = output / f"{frame}.png"
            Image.new("RGB", (40, 24)).save(path)
            result[frame] = path
        return result

    monkeypatch.setattr(sampling, "composed_snapshot", lambda: snapshot)
    monkeypatch.setattr(scene_answers, "host_frames_at", query)
    monkeypatch.setattr(composed_frame, "renderer_environment_identity", lambda: "curve-test")
    provider = composed_frame.RemotionFrameProvider(
        snapshot, timeline_path=tmp_path / "timeline.json", assets_path=tmp_path / "assets.json",
        project_dir=tmp_path, cache=composed_frame.FrameCaptureCache(tmp_path / "cache"), renderer=render)
    reserve, capture = provider.reserve_scene_frames, provider.capture

    def record_reservation(frames):
        provider.reserved = list(frames)
        reserve(frames)

    def record_capture(cards, out_root, resolution):
        provider.pixels = [card["frame"] for card in cards]
        return capture(cards, out_root, resolution)

    monkeypatch.setattr(provider, "reserve_scene_frames", record_reservation)
    monkeypatch.setattr(provider, "capture", record_capture)
    try:
        ctx = run_pack(tmp_path, monkeypatch, provider, layers=("curves",), cut=None, range=(.4, 1.4))
        assert renders == [sorted(provider.pixels)]
        assert queries == [list(dict.fromkeys(sorted(provider.pixels) + provider.reserved))]
        assert set(ctx.shared["curve_frames"]) <= set(queries[0])
        result = builtin.render_curves(ctx)
        assert any("intrinsic position" in f for f in result.findings), result.findings
        cached = run_pack(tmp_path, monkeypatch, provider, layers=("curves",), cut=None, range=(.4, 1.4))
        assert len(queries) == len(renders) == 1
        assert provider.scene_frames == {} and provider._reserved_scene_frames == ()
        assert any("cached" in f and "unavailable" in f for f in builtin.render_curves(cached).findings)
    finally:
        provider.close()
