"""Default capture adapter checks files before rendering or using cached PNGs."""
import json
from copy import deepcopy

import pytest
from PIL import Image

from astrid.core.timeline import scene_answers
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

    def provider(value=None, *, scene_labels=False):
        return composed_frame.RemotionFrameProvider(
            snapshot if value is None else value, timeline_path=timeline, assets_path=assets,
            project_dir=tmp_path, cache=composed_frame.FrameCaptureCache(tmp_path / "cache"),
            scene_labels=scene_labels)

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


def test_mutating_caller_snapshot_cannot_cache_old_pixels_as_new_source(capture, tmp_path, monkeypatch):
    create, snapshot, timeline, _assets, calls = capture
    colors = {"historical": (255, 0, 0), "current": (0, 255, 0)}

    def acquire(**kwargs):
        def render(frames, output, _resolution):
            config = json.loads(kwargs["context"]["timeline_path"].read_text())
            source = config["app"]["opaque"]
            calls.append(source)
            result = {}
            for frame in frames:
                path = output / f"{frame}.png"
                Image.new("RGB", (8, 8), colors[source]).save(path)
                result[frame] = path
            return result

        return render

    monkeypatch.setattr(composed_frame, "_acquire_shared_remotion_handle", acquire)
    historical_snapshot = deepcopy(snapshot)
    historical = create()
    # The constructor already copied the historical closure for validation.
    # Changing the caller's dict must not relabel those historical pixels.
    snapshot["config"]["app"]["opaque"] = "current"
    snapshot["metadata"]["capture_authority"]["parent_revision_id"] = "new"
    snapshot["fps_rational"] = [60, 1]
    current_snapshot = deepcopy(snapshot)
    cards = [{"frame": 2, "image": "frames/2.png"}]
    try:
        assert historical.capture(cards, tmp_path / "historical")["fresh_frames"] == 1
        old_key = composed_frame.frame_cache_key(historical_snapshot, 2, None)
        new_key = composed_frame.frame_cache_key(current_snapshot, 2, None)
        assert old_key != new_key
        assert historical.cache.read(old_key) == (tmp_path / "historical/frames/2.png").read_bytes()
        assert historical.cache.read(new_key) is None
        timeline.write_text(json.dumps(current_snapshot["config"]))
        current = create(current_snapshot)
        try:
            assert current.capture(cards, tmp_path / "current")["fresh_frames"] == 1
            with Image.open(tmp_path / "current/frames/2.png") as image:
                assert image.getpixel((0, 0)) == colors["current"]
            assert current.capture(cards, tmp_path / "cached-current")["cached_frames"] == 1
            assert (tmp_path / "cached-current/frames/2.png").read_bytes() == current.cache.read(new_key)
            assert calls == ["historical", "current"]
        finally:
            current.close()
    finally:
        historical.close()


def test_caller_metadata_enrichment_keeps_original_cache_identity(capture, tmp_path):
    create, snapshot, _timeline, _assets, calls = capture
    original = deepcopy(snapshot)
    provider = create()
    cards = [{"frame": 2, "image": "frames/2.png"}]
    try:
        assert provider.capture(cards, tmp_path / "first")["fresh_frames"] == 1
        snapshot["metadata"]["capture_timing"] = {"prepare_s": 0.25}
        enriched = deepcopy(snapshot)
        cached = provider.capture(cards, tmp_path / "enriched")
        assert cached["cached_frames"] == 1 and cached["fresh_frames"] == 0
        assert calls == [(2,)] and snapshot == enriched
        old_key = composed_frame.frame_cache_key(original, 2, None)
        new_key = composed_frame.frame_cache_key(enriched, 2, None)
        assert old_key != new_key
        assert provider.cache.read(old_key) == (tmp_path / "enriched/frames/2.png").read_bytes()
        assert provider.cache.read(new_key) is None
        assert provider.scene_frames == {} and "cached" in provider.scene_unavailable
    finally:
        provider.close()


def test_caller_config_and_fps_mutation_keeps_prepared_scene_labels(capture, tmp_path, monkeypatch):
    create, snapshot, timeline, _assets, calls = capture
    canvas = {"width": 8, "height": 8, "fps": 30}
    props = {"timeline": json.loads(timeline.read_text()), "theme": {"visual": {"canvas": canvas}}}
    contexts, queries = [], []

    def query(actual, basis, frames):
        assert actual is props and basis == canvas
        queries.append(list(frames))
        return [{"frame": frame, "coverage": "GAP", "layers": []} for frame in frames]

    def acquire(**kwargs):
        contexts.append(kwargs["context"])

        def render(frames, output, _resolution):
            calls.append(tuple(frames))
            kwargs["context"]["on_scene_props"](props, frames)
            paths = {}
            for frame in frames:
                paths[frame] = output / f"{frame}.png"
                Image.new("RGB", (8, 8)).save(paths[frame])
            return paths

        return render

    monkeypatch.setattr(scene_answers, "host_frames_at", query)
    monkeypatch.setattr(composed_frame, "_acquire_shared_remotion_handle", acquire)
    provider = create(scene_labels=True)
    snapshot["fps_rational"][0] = 60
    snapshot["config"]["app"].update({"opaque": "current", "astrid_bounds": True})
    snapshot["metadata"]["capture_authority"]["parent_revision_id"] = "new"
    mutated = deepcopy(snapshot)
    try:
        provider.reserve_scene_frames([7])
        info = provider.capture([{"frame": 2, "image": "frames/2.png"}], tmp_path / "pack")
        assert info["fresh_frames"] == 1 and calls == [(2,)]
        assert queries == [[2, 7]] and provider.scene_unavailable is None
        assert provider.label_canvas == {"width": 8, "height": 8}
        assert provider.label_batches == {2: [], 7: []}
        assert provider.scene_frames == {str(frame): {"frame": frame, "coverage": "GAP", "layers": []}
                                         for frame in (2, 7)}
        assert provider._reserved_scene_frames == provider._active_reserved_scene_frames == ()
        assert provider.wants_bounds is False and snapshot == mutated
        assert "canonical_source" not in contexts[0] and "transition_policy" not in contexts[0]
    finally:
        provider.close()
