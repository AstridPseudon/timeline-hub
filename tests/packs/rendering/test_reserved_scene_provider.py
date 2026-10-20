from __future__ import annotations

import copy
import math
from pathlib import Path

import pytest
from PIL import Image

from astrid.core.timeline import scene_answers
from astrid.packs.rendering.actions.timeline_visualize import composed_frame


CANVAS = {"width": 200, "height": 100, "fps": 30}


def _props() -> dict:
    clips = [
        {"id": "compiled-first", "clipType": "test-card", "track": "plate", "at": 0, "hold": 1,
         "app": {"astrid_shot_composition": {"source_clip_id": "source-card", "occurrence_id": "one"}}},
        {"id": "compiled-second", "clipType": "test-card", "track": "plate", "at": 2, "hold": 1,
         "app": {"astrid_shot_composition": {"source_clip_id": "source-card", "occurrence_id": "two"}}},
    ]
    return {
        "timeline": {"tracks": [{"id": "plate", "kind": "visual"}], "clips": clips},
        "assets": {"assets": {}},
        "theme": {"id": "actual-theme", "visual": {"canvas": dict(CANVAS)}},
    }


def _answer(frame: int, clip_id: str) -> dict:
    return {
        "frame": frame,
        "coverage": "COVERED",
        "content": clip_id,
        "layers": [{
            "clipId": clip_id,
            "track": "plate",
            "z": 0,
            "role": "picture",
            "visible": True,
            "opacity": 1,
            "fullFrame": False,
            "coverage": "covered",
            "bounds": {"status": "known", "rect": {"x": 20, "y": 10, "width": 60, "height": 40}},
            "findings": [],
        }],
        "findings": [],
    }


def _provider(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, rows: dict[int, dict], calls: list,
              render_calls: list, *, fail: bool = False) -> composed_frame.RemotionFrameProvider:
    props = _props()

    def query(actual, basis, frames):
        assert actual is props
        assert basis == CANVAS
        calls.append(list(frames))
        return [copy.deepcopy(rows[frame]) for frame in frames]

    monkeypatch.setattr(scene_answers, "host_frames_at", query)
    monkeypatch.setattr(scene_answers, "occlusions_from_frames", lambda answers, targets: [
        {"status": "known", "fraction": target["min_fraction"]} for target in targets
    ], raising=False)
    provider = None

    def render(frames, output, _resolution):
        render_calls.append(list(frames))
        if fail:
            raise RuntimeError("capture failed")
        provider._scene_labels(props, frames)
        result = {}
        for frame in frames:
            path = Path(output) / f"frame-{frame:06d}.png"
            Image.new("RGB", (32, 18), (frame, 0, 0)).save(path)
            result[frame] = path
        return result

    provider = composed_frame.RemotionFrameProvider(
        {"fps_rational": [30, 1]},
        timeline_path=tmp_path / "timeline.json",
        assets_path=tmp_path / "assets.json",
        project_dir=tmp_path,
        cache=composed_frame.FrameCaptureCache(tmp_path / "cache"),
        renderer=render,
    )
    return provider


def test_reservation_validates_deduplicates_and_preserves_order(tmp_path):
    provider = composed_frame.RemotionFrameProvider(
        {"fps_rational": [30, 1]},
        timeline_path=tmp_path / "timeline.json", assets_path=tmp_path / "assets.json",
        project_dir=tmp_path, renderer=lambda *_args: {},
    )
    provider.reserve_scene_frames([7, 2, 7, 4])
    assert provider._reserved_scene_frames == (7, 2, 4)
    provider.reserve_scene_frames(range(60))
    assert len(provider._reserved_scene_frames) == 60

    for invalid in (True, False, -1, 2**53, 1.0, 1.5, math.nan, math.inf, "4"):
        with pytest.raises(ValueError):
            provider.reserve_scene_frames([invalid])
    with pytest.raises(ValueError, match="at most 60"):
        provider.reserve_scene_frames(range(61))


def test_capture_queries_pixel_union_once_and_reuses_answers_for_all_scene_facts(tmp_path, monkeypatch):
    rows = {frame: _answer(frame, "compiled-first" if frame < 2 else "compiled-second")
            for frame in (0, 2, 4, 7)}
    calls, render_calls = [], []
    provider = _provider(tmp_path, monkeypatch, rows, calls, render_calls)
    provider.reserve_scene_frames([7, 4, 7, 2])

    info = provider.capture([
        {"frame": 2, "image": "frames/2.png"}, {"frame": 0, "image": "frames/0.png"},
    ], tmp_path / "pack")

    assert info["requested_frames"] == [2, 0]
    assert render_calls == [[0, 2]]
    assert calls == [[0, 2, 7, 4]]
    assert set(provider.scene_frames) == {"0", "2", "4", "7"}
    assert set(provider.label_batches) == {0, 2, 4, 7}
    assert set(provider.scene_clip_identities) == {"compiled-first", "compiled-second"}
    assert provider.scene_occlusions["0.9"]["7"]["compiled-second"]["status"] == "known"
    assert provider._reserved_scene_frames == () and provider._active_reserved_scene_frames == ()


def test_default_capture_queries_only_selected_pixels_and_cached_capture_does_not_requery(
    tmp_path, monkeypatch,
):
    rows = {frame: _answer(frame, "compiled-first") for frame in (0, 1, 9)}
    calls, render_calls = [], []
    provider = _provider(tmp_path, monkeypatch, rows, calls, render_calls)
    cards = [{"frame": 0, "image": "frames/0.png"}]

    provider.capture(cards, tmp_path / "first")
    provider.reserve_scene_frames([9])
    cached = provider.capture(cards, tmp_path / "second")

    assert calls == [[0]]
    assert render_calls == [[0]]
    assert cached["evidence_source"] == "cache"
    assert provider.scene_frames == {}
    assert provider.scene_unavailable == "exact scene facts unavailable for cached pixels"
    assert provider._reserved_scene_frames == () and provider._active_reserved_scene_frames == ()


def test_capture_error_and_close_clear_reservations(tmp_path, monkeypatch):
    rows = {1: _answer(1, "compiled-first"), 8: _answer(8, "compiled-first")}
    calls, render_calls = [], []
    provider = _provider(tmp_path, monkeypatch, rows, calls, render_calls, fail=True)
    provider.reserve_scene_frames([8])
    with pytest.raises(RuntimeError, match="capture failed"):
        provider.capture([{"frame": 1, "image": "frames/1.png"}], tmp_path / "failed")
    assert provider._reserved_scene_frames == () and provider._active_reserved_scene_frames == ()

    provider.reserve_scene_frames([8])
    provider.close()
    assert provider._reserved_scene_frames == () and provider._active_reserved_scene_frames == ()
