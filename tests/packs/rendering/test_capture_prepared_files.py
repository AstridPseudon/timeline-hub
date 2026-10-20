"""Default capture adapter checks files before rendering or using cached PNGs."""
import json
from copy import deepcopy

import pytest
from PIL import Image

from astrid.packs.rendering.actions.timeline_visualize import composed_frame


@pytest.fixture
def capture(tmp_path, monkeypatch):
    config = {"tracks": [], "clips": [], "app": {"opaque": "historical"}}
    registry = {"assets": {}}
    snapshot = {"config": config, "registry": registry, "fps_rational": [30, 1],
                "metadata": {"capture_authority": {"parent_revision_id": "old"}},
                "video_digest": "sha256:" + "a" * 64}
    timeline = tmp_path / "timeline.json"
    assets = tmp_path / "assets.json"
    timeline.write_text(json.dumps(config))
    assets.write_text(json.dumps(registry))
    calls = []

    def render(frames, output, _resolution):
        calls.append(tuple(frames))
        paths = {}
        for frame in frames:
            paths[frame] = output / f"{frame}.png"
            Image.new("RGB", (8, 8)).save(paths[frame])
        return paths

    monkeypatch.setattr(composed_frame, "_acquire_shared_remotion_handle", lambda **_kwargs: render)
    monkeypatch.setattr(composed_frame, "renderer_environment_identity", lambda: "fixture-renderer")

    def provider(value=None):
        return composed_frame.RemotionFrameProvider(
            snapshot if value is None else value, timeline_path=timeline, assets_path=assets,
            project_dir=tmp_path, cache=composed_frame.FrameCaptureCache(tmp_path / "cache"))

    return provider, snapshot, timeline, assets, calls


def test_matching_files_capture_and_cache_without_mutating_source(capture, tmp_path):
    create, snapshot, _timeline, _assets, calls = capture
    before = deepcopy(snapshot)
    provider = create()
    cards = [{"frame": 2, "image": "frames/2.png"}]
    assert provider.capture(cards, tmp_path / "first")["fresh_frames"] == 1
    assert provider.capture(cards, tmp_path / "second")["cached_frames"] == 1
    assert calls == [(2,)] and snapshot == before


@pytest.mark.parametrize("which", ["timeline", "registry"])
@pytest.mark.parametrize("problem", ["changed", "missing", "invalid"])
def test_files_must_match_before_acquiring_renderer(capture, which, problem):
    create, _snapshot, timeline, assets, calls = capture
    path = timeline if which == "timeline" else assets
    if problem == "missing":
        path.unlink()
    else:
        path.write_text('{"different":true}' if problem == "changed" else "invalid JSON")
    with pytest.raises(ValueError, match="Composed frame capture"):
        create()
    assert calls == []


def test_changed_files_cannot_reuse_a_cached_historical_frame(capture, tmp_path):
    create, _snapshot, timeline, _assets, calls = capture
    provider = create()
    cards = [{"frame": 2, "image": "frames/2.png"}]
    provider.capture(cards, tmp_path / "first")
    timeline.write_text('{"clips":[],"app":{"opaque":"current"}}')
    with pytest.raises(ValueError, match="prepared config differs"):
        provider.capture(cards, tmp_path / "cached")
    assert calls == [(2,)]
    assert not (tmp_path / "cached/frames/2.png").exists()


def test_capture_labels_cannot_override_file_mismatch(capture):
    create, snapshot, timeline, _assets, calls = capture
    snapshot["metadata"].update({"capture_authority": {"canonical": True},
                                "snapshot_label": "canonical"})
    timeline.write_text('{"canonical_source":true}')
    with pytest.raises(ValueError, match="prepared config differs"):
        create()
    assert calls == []


@pytest.mark.parametrize("key,value", [("config", None), ("registry", None)])
def test_incomplete_prepared_closure_is_refused(capture, key, value):
    create, snapshot, _timeline, _assets, calls = capture
    snapshot[key] = value
    with pytest.raises(ValueError, match=f"snapshot has no {key}"):
        create()
    assert calls == []


def test_native_adapter_omits_source_selection(capture, monkeypatch):
    create, _snapshot, timeline, assets, calls = capture
    contexts = []
    monkeypatch.setattr(composed_frame, "_acquire_shared_remotion_handle",
                        lambda **kwargs: contexts.append(kwargs["context"]) or (lambda *_args: {}))
    timeline.unlink()
    assets.unlink()
    create({"fps_rational": [30, 1], "metadata": {
        "capture_authority": {"canonical": True}, "snapshot_label": "canonical"},
        "canonical_source": {"source_kind": "revision"}, "transition_policy": "incoming"})
    assert len(contexts) == 1
    assert "canonical_source" not in contexts[0]
    assert "transition_policy" not in contexts[0]
    assert calls == []


def test_prepared_file_mismatch_clears_prior_scene_facts_and_reservation(capture, tmp_path):
    create, _snapshot, timeline, _assets, calls = capture
    provider = create()
    cards = [{"frame": 2, "image": "frames/2.png"}]
    provider.capture(cards, tmp_path / "first")
    provider.label_batches = {2: ["prior label"]}
    provider.label_canvas = {"width": 200, "height": 100}
    provider.scene_frames = {"2": {"frame": 2}}
    provider.scene_occlusions = {"0.98": {"2": {}}}
    provider.scene_clip_identities = {"old": {"clip_id": "old"}}
    provider.reserve_scene_frames([12, 30])
    timeline.write_text('{"clips":[],"app":{"opaque":"current"}}')
    with pytest.raises(ValueError, match="prepared config differs"):
        provider.capture(cards, tmp_path / "mismatch")
    assert calls == [(2,)]
    assert provider._reserved_scene_frames == provider._active_reserved_scene_frames == ()
    assert provider.label_batches == provider.scene_frames == provider.scene_occlusions == provider.scene_clip_identities == {}
    assert provider.label_canvas is None
    assert "prepared config differs" in provider.scene_unavailable
    assert not (tmp_path / "mismatch").exists()
