"""More on-screen model cases (TRUTH.md §2.2): cross-fades, fades at the film start, layout, audio, element data, speed."""
from __future__ import annotations

import pytest

from tests.core.timeline.scene_support import coverage, visible_at

FPS = 30
CANVAS = {"width": 1920, "height": 1080}
ELEMENTS = {
    "am-snap-plate": {"coverage": "picture", "background_unless": ["asset", "params.src"]},
    "am-footage": {"coverage": "picture"},
    "am-type": {"coverage": "content"},
    "am-sprite": {"coverage": "content"},
    "am-guide": {"coverage": "none"},
}
TRACKS = [{"id": t, "kind": "visual"} for t in ("fx", "type", "sprite", "plate")]


def _clip(cid, clip_type, track, *, at=0.0, hold=1.0, cut="c01", layer="l", **fields):
    clip = {"id": cid, "clipType": clip_type, "track": track, "at": at, "hold": hold, "params": {},
            "app": {"cut": cut, "layer": layer}}
    clip.update(fields)
    return clip


def _plate(cid="plate", *, asset="P", at=0.0, hold=1.0, **fields):
    return _clip(cid, "am-snap-plate", "plate", asset=asset, at=at, hold=hold, **fields)


def _config(clips, tracks=TRACKS):
    return {"tracks": [dict(t) for t in tracks], "clips": clips}


def _independent_fades_config():
    return _config([
        _plate("out", asset=None, params={"src": "/plate.png"}, at=0.0, hold=1.0, effects={"fade_out": 0.5}),
        _clip("in", "am-footage", "fx", at=0.5, hold=1.0, params={"src": "/footage.png"}, effects={"fade_in": 0.5}),
    ])


# Main's drawing and the registered native renderer agree: independent clip
# fades expose the canvas. The named public incoming-crossfade test stays covered.
def test_independent_full_plate_fades_have_a_render_backed_dip():
    config = _independent_fades_config()
    spans = coverage(config, FPS, CANVAS, ELEMENTS, end_frame=45)
    assert [(s.start_frame, s.end_frame, s.cls, s.content) for s in spans] == [
        (0, 16, "COVERED", "CONTENT"),
        (16, 30, "DIP", None),
        (30, 45, "COVERED", "CONTENT"),
    ]


# Keep the continuous DIP expectation across the fully transparent first frame.
@pytest.mark.xfail(strict=True, reason='M3 requires continuous coverage-class runs; native span encoding currently splits DIP when visible clip membership changes.')
def test_a_one_sided_fade_is_a_dip_during_the_ramp_then_covered():
    config = _config([_plate("only", asset=None, params={"src": "/plate.png"}, at=0.0, hold=2.0, effects={"fade_in": 0.5})])
    spans = coverage(config, FPS, CANVAS, ELEMENTS)
    assert [(s.start_frame, s.end_frame, s.cls) for s in spans] == [(0, 15, "DIP"), (15, 60, "COVERED")]
    assert spans[0].content is None
    assert spans[1].content == "CONTENT"


def test_a_none_element_is_not_listed():
    config = _config([_plate("plate"), _clip("guide", "am-guide", "fx", asset="G")])
    assert [v.clip_id for v in visible_at(config, 0, FPS, CANVAS, ELEMENTS)] == ["plate"]


def test_an_inset_with_layout_is_declared_and_not_full_frame():
    config = _config([_clip("fx", "am-footage", "fx", params={"src": "/footage.png", "background": "transparent",
        "inset": {"x": 1200, "y": 600, "w": 576, "h": 324, "shadow": False}})])
    (inset,) = visible_at(config, 0, FPS, CANVAS, ELEMENTS)
    assert inset.bounds_source == "declared"
    assert inset.bounds == (1200.0, 600.0, 1200.0 + 1920 * 0.3, 600.0 + 1080 * 0.3)
    assert inset.full_frame is False


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 requires canonical declared scale-in animation geometry/alpha.')
def test_a_scale_in_entrance_is_not_full_frame_during_its_duration_but_keeps_its_opacity():
    config = _config([_plate("plate", hold=1.0, entrance={"type": "scale-in", "duration": 0.5})])
    early, late = visible_at(config, 0, FPS, CANVAS, ELEMENTS)[0], visible_at(config, 20, FPS, CANVAS, ELEMENTS)[0]
    assert early.full_frame is False and early.opacity == 1.0
    assert late.full_frame is True


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 requires canonical declared fade-up animation geometry/alpha.')
def test_a_fade_up_entrance_ramps_opacity_and_keeps_full_frame():
    config = _config([_plate("plate", hold=1.0, entrance={"type": "fade-up", "duration": 0.5})])
    first = visible_at(config, 0, FPS, CANVAS, ELEMENTS)[0]
    assert first.opacity == 0.0 and first.full_frame is True


def test_audio_clips_and_audio_tracks_are_ignored():
    tracks = TRACKS + [{"id": "music", "kind": "audio"}]
    config = _config([_clip("score", "am-footage", "music", asset="M")], tracks=tracks)
    assert visible_at(config, 0, FPS, CANVAS, ELEMENTS) == []
    assert [(s.cls, s.end_frame) for s in coverage(config, FPS, CANVAS, ELEMENTS)] == [("GAP", 30)]


def test_element_coverage_reads_metadata_coverage_from_element_yaml(tmp_path, monkeypatch):
    from astrid.core.timeline import scene_roles as onscreen

    packs = tmp_path / "packs"
    declared = packs / "tmp" / "elements" / "effects" / "am-tmp-plate"
    declared.mkdir(parents=True)
    (declared / "element.yaml").write_text(
        "id: am-tmp-plate\nkind: effect\nmetadata:\n  coverage: picture\n  background_unless: [asset]\n",
        encoding="utf-8",
    )
    bare = packs / "tmp" / "elements" / "effects" / "am-tmp-bare"
    bare.mkdir(parents=True)
    (bare / "element.yaml").write_text("id: am-tmp-bare\nkind: effect\n", encoding="utf-8")
    monkeypatch.setattr(onscreen, "_PACKS_ROOT", packs)
    monkeypatch.setattr(onscreen, "_COVERAGE_CACHE", {})

    assert onscreen.element_coverage(["am-tmp-plate", "am-tmp-bare", "am-missing"]) == {
        "am-tmp-plate": {"coverage": "picture", "background_unless": ["asset"]},
        "am-tmp-bare": {},
        "am-missing": {},
    }


def test_the_real_elements_declare_the_picture_roles_coverage_needs():
    from astrid.core.timeline.scene_roles import element_coverage

    found = element_coverage(["am-snap-plate", "am-footage", "am-presenter"])
    assert found["am-snap-plate"] == {"coverage": "picture", "background_unless": ["asset", "params.src"]}
    assert found["am-footage"]["coverage"] == found["am-presenter"]["coverage"] == "picture"


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 requires declared opaque component capabilities and native batched coverage for these 300 custom clips.')
def test_large_coverage_processes_each_clip_boundary_once(monkeypatch):
    from tests.core.timeline import scene_support as onscreen

    clips = []
    for i in range(300):
        track = "plate" if i % 2 == 0 else "fx"
        clips.append(_clip(
            f"c{i}", "am-snap-plate" if track == "plate" else "am-footage", track,
            at=i * 0.5, hold=1.0, asset="P", cut=f"c{i:02d}", layer="l",
            effects={"fade_in": 0.2, "fade_out": 0.2},
        ))
    config = _config(clips)
    boundary_calls = {"start": {}, "end": {}}
    original_start = onscreen.clip_start_frame
    original_end = onscreen.clip_end_frame

    def count_boundary(kind, original):
        def counted(clip, fps):
            clip_id = clip["id"]
            boundary_calls[kind][clip_id] = boundary_calls[kind].get(clip_id, 0) + 1
            return original(clip, fps)
        return counted

    monkeypatch.setattr(onscreen, "clip_start_frame", count_boundary("start", original_start))
    monkeypatch.setattr(onscreen, "clip_end_frame", count_boundary("end", original_end))
    spans = onscreen.coverage(config, FPS, CANVAS, ELEMENTS, end_frame=4500)

    assert [(span.start_frame, span.end_frame, span.cls, span.content) for span in spans] == [
        (0, 6, "DIP", None),
        (6, 4500, "COVERED", "CONTENT"),
    ]
    expected_ids = {clip["id"] for clip in clips}
    assert boundary_calls == {
        "start": {clip_id: 1 for clip_id in expected_ids},
        "end": {clip_id: 1 for clip_id in expected_ids},
    }


# Retain the behavior until the named M3 input/capability requirement is met.
@pytest.mark.xfail(strict=True, reason='M3 requires canonical declared scale-in animation geometry/alpha.')
def test_a_declared_non_fade_entrance_on_the_picture_is_a_dip_not_a_gap():
    from tests.core.timeline.scene_support import coverage

    config = {"tracks": [{"id": "plate", "kind": "visual"}],
              "clips": [{"id": "p", "clipType": "am-snap-plate", "track": "plate", "asset": "P", "at": 0.0, "hold": 1.0,
                         "params": {}, "entrance": {"type": "scale-in", "duration": 0.2}}]}
    spans = coverage(config, 30, {"width": 1920, "height": 1080},
                     {"am-snap-plate": {"coverage": "picture", "background_unless": ["asset", "params.src"]}})
    assert [(s.start_frame, s.end_frame, s.cls) for s in spans] == [(0, 6, "DIP"), (6, 30, "COVERED")]


from tests.packs.rendering.test_host_scene import host_project, native_host  # noqa: E402, F401

pytestmark = pytest.mark.usefixtures("native_host")


def test_real_am_components_share_draw_helpers_and_public_scene_capabilities(request):
    import subprocess

    from astrid.core.timeline import scene_answers
    from tests.packs.rendering import test_host_scene as native_fixtures

    project = request.getfixturevalue("native_host")
    node = scene_answers.remotion_runtime_status().node_executable
    assert node is not None
    script = (native_fixtures.ROOT / "astrid/packs/astrid_motion/rendering/elements/effects"
              / "am-snap-plate/scene.test.mjs")
    result = subprocess.run([str(node), str(script), str(project), str(native_fixtures.ROOT)],
                            text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
