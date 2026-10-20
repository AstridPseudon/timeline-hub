"""Real normal props and native PCM preparation, with socket-free consumption."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import struct
import subprocess
import wave
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering.contracts import (
    SCHEMA_VERSION,
    FrameWindow,
    RenderProfile,
    RenderRequest,
)
from astrid.core.rendering.service import RenderService
from astrid.core.timeline.banodoco_composer import Timeline
from astrid.core.timeline.duration import clip_start_frame
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion


def _profile():
    return RenderProfile(width=320, height=180, fps_rational=(30000, 1001),
                         time_base=(1, 90000), video_codec="h264", pixel_format="yuv420p")


def _timeline():
    return {
        "theme": "banodoco-default",
        "tracks": [{"id": "A1", "kind": "audio", "label": "Audio", "volume": 0.5},
                   {"id": "V1", "kind": "visual", "label": "Visual"}, {"id": "other", "kind": "audio", "label": "Other"}],
        "clips": [{
            "id": "sound", "track": "A1", "asset": "sound", "at": 0.016682,
            "from": 0.051, "to": 3.051, "speed": 1.5, "volume": 3,
            "params": {"fadeIn": 0.2, "fadeOut": 0.2, "fadeInCurve": "equal-power"},
            "app": {"astrid_slice_origin": {"at": 99}, "opaque": [1, {"keep": True}]},
        }, {
            "id": "overlap", "track": "A1", "asset": "sound", "at": 0.2,
            "from": 0, "to": 3, "volume": 0,
            "params": {"fadeIn": 0.1},
        }, {
            "id": "sprite", "track": "V1", "clipType": "am-sprite", "at": 0,
            "hold": 4, "opacity": 0.4, "params": {"keyframes": [{"frame": 0, "x": 1, "y": 0}]},
        }, {"id": "excluded", "track": "other", "asset": "sound", "at": 0, "from": 0, "to": 9}],
        "metadata": {"opaque": {"original": [1, 2]}},
    }


def _layer_request(tmp_path, native=True):
    timeline_path = tmp_path / "timeline.json"
    timeline_path.write_text(json.dumps(_timeline()))
    window = FrameWindow(15, 45, (30000, 1001))
    request = RenderRequest(SCHEMA_VERSION, str(timeline_path), "out.mp4", window=window)
    segment = SimpleNamespace(window=window, layer=SimpleNamespace(tracks=("A1", "V1"), z=0))
    candidate = SimpleNamespace(id="fixture", manifest=SimpleNamespace(capabilities={"supports_windows": native}))
    adapted, sidecar = RenderService._segment_request(
        object.__new__(RenderService), request, candidate=candidate, segment=segment,
        index=0, workspace=tmp_path,
    )
    return request, adapted, sidecar


def test_native_layer_retains_exact_clips_window_and_materialized_hash(tmp_path):
    request, adapted, sidecar = _layer_request(tmp_path)
    original = json.loads(Path(request.timeline_path).read_text())
    materialized = json.loads(Path(adapted.timeline_path).read_text())
    assert adapted.window is request.window
    assert materialized["clips"] == original["clips"][:3]
    assert materialized["tracks"] == original["tracks"][:2]
    assert materialized["metadata"] == {**original["metadata"], "astrid_layer": {"z": 0, "alpha": False}}
    assert sidecar == {"materialized_timeline": hashlib.sha256(Path(adapted.timeline_path).read_bytes()).hexdigest()}
    assert RenderService._input_hashes(request)["timeline"] == hashlib.sha256(Path(request.timeline_path).read_bytes()).hexdigest()
    assert remotion._native_window_argument(adapted.window, materialized, _profile()) == "--frames=15-44"
    assert original == _timeline()


def test_legacy_layer_still_rebases_its_window(tmp_path):
    request, adapted, _ = _layer_request(tmp_path, native=False)
    actual = json.loads(Path(adapted.timeline_path).read_text())
    expected = RenderService._window_timeline(_timeline(), request.window, tracks=("A1", "V1"))
    expected["metadata"]["astrid_layer"] = {"z": 0, "alpha": False}
    assert adapted.window is None
    assert actual == expected
    assert actual["clips"][0]["id"] == "sound_15_45"


def test_render_serialization_preserves_submillisecond_source_placement():
    raw = _timeline()
    before = copy.deepcopy(raw)
    timeline = Timeline.from_json_data(raw)
    actual = timeline.for_render().to_json_data()
    assert actual == raw
    assert raw == before
    # Persistence keeps its existing formatting convention.
    persisted = timeline.to_json_data()
    assert persisted["clips"][0]["at"] == 0.017
    assert clip_start_frame(actual["clips"][0], 30000 / 1001) == 0
    assert clip_start_frame(persisted["clips"][0], 30000 / 1001) == 1
    actual["clips"][0]["params"]["fadeIn"] = 99
    assert timeline.for_render().to_json_data() == raw


@pytest.fixture(params=["full", "window", "layer"])
def normal_run(tmp_path, monkeypatch, request):
    monkeypatch.delenv("PYTHONPYCACHEPREFIX", raising=False)
    monkeypatch.delenv("ASTRID_PROGRESS_PATH", raising=False)
    monkeypatch.setenv("ASTRID_REMOTION_STREAM_MEMORY_BUDGET_BYTES", "0")
    original_request, layer_request, _ = _layer_request(tmp_path)
    render_request = layer_request if request.param == "layer" else original_request
    if request.param == "full":
        render_request = replace(render_request, window=None)
    timeline_path = Path(render_request.timeline_path)
    original = timeline_path.read_bytes()
    audio = io.BytesIO()
    with wave.open(audio, "wb") as writer:
        writer.setparams((2, 2, 30000, 0, "NONE", "not compressed"))
        writer.writeframes(struct.pack("<hh", 8192, -4096) * 90000)
    payload = audio.getvalue()
    registry = tmp_path / "assets.json"
    registry.write_text(json.dumps({"assets": {"sound": {
        "object_id": "object-sound", "digest": hashlib.sha256(payload).hexdigest(), "type": "audio/wav",
    }}}))
    project = Path(os.environ["ASTRID_REMOTION_PROJECT_DIR"])
    runtime = SimpleNamespace(node_executable=Path(os.environ["ASTRID_NODE_EXECUTABLE"]),
                              remotion_cli=project / "unused-render-cli", node_version="v20.19.4")
    for name in ("_regenerate_element_registries", "_validate_renderer_effect_registry"):
        monkeypatch.setattr(remotion, name, lambda *a: None)
    monkeypatch.setattr(remotion, "_validate_project_dir", lambda *a: runtime)
    monkeypatch.setattr(remotion, "_effective_registry_state", lambda *a: {"hash": "fixture"})
    monkeypatch.setattr(remotion, "_canonical_profile", lambda *a: _profile())
    monkeypatch.setattr(remotion, "_resolved_theme_for_render", lambda *a: {"id": "banodoco-default"})
    monkeypatch.setattr(remotion, "_stage_effect_assets_for_timeline", lambda *a, **k: {"effects": []})
    monkeypatch.setattr(remotion, "_available_remotion_port", lambda: 32101)
    state = SimpleNamespace(paths=[], events=[], props=None, consume=lambda: None,
                            materialized_objects={"object-sound": payload})

    class ContainedServer:
        def __init__(self, root, **kwargs):
            self.root = root
            self.alive = False
            state.server = self

        def __enter__(self):
            self.alive = True
            state.events.append("server-enter")
            return self

        def local_url(self, path):
            assert self.alive
            return "http://attempt.invalid/" + Path(path).resolve(strict=True).relative_to(self.root).as_posix()

        def __exit__(self, *args):
            state.events.append("server-exit")
            # WAV lifetime belongs to the attempt and ends before the server.
            assert all(not path.exists() for path in state.paths)
            self.alive = False

    monkeypatch.setattr(remotion, "InvocationAssetServer", ContainedServer)
    real_subprocess = subprocess.run

    def command(argv, **kwargs):
        if str(runtime.remotion_cli) not in argv:
            return real_subprocess(argv, **kwargs)
        state.events.append("consume")
        assert state.server.alive
        assert ("--frames=15-44" in argv) == (render_request.window is not None)
        props_path = Path(argv[argv.index("--props") + 1])
        state.props_path = props_path
        state.props = json.loads(props_path.read_text())
        for clip in state.props["timeline"]["clips"]:
            source = clip.get("audio", {}).get("render_source")
            if source:
                path = state.server.root / source["file"].removeprefix("http://attempt.invalid/")
                assert path.is_file()
                state.paths.append(path)
        assert len(state.paths) == 2
        assert timeline_path.read_bytes() == original
        state.consume()
        Path(argv[argv.index("--output") + 1]).write_bytes(b"test consumer output, not a render")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(remotion.subprocess, "run", command)

    def execute():
        return remotion._execute_remotion_locked(
            timeline_path, registry, tmp_path / "out.mp4", provenance_out_path=tmp_path / "out.mp4",
            project_dir=project, composition_id="TimelineComposition", theme_path=None,
            min_free_gb=None, materialized_objects=state.materialized_objects, staging_parent=tmp_path,
            window=render_request.window,
        )

    state.execute = execute
    state.timeline_path = timeline_path
    state.registry = registry
    yield state
    assert timeline_path.read_bytes() == original
    assert not list(tmp_path.glob("astrid-render-assets-*"))
    assert not list(tmp_path.glob(".remotion-runtime-*"))
    assert not (tmp_path / ".remotion-props.json").exists()


def test_actual_normal_props_prepare_native_source_without_baking_scalar_gain(normal_run):
    state = normal_run

    def consume():
        props = state.props
        assert "compiledTransitions" not in props
        raw = json.loads(state.timeline_path.read_text())
        assert props["timeline"]["tracks"] == raw["tracks"]
        for expected, actual in zip(raw["clips"], props["timeline"]["clips"], strict=True):
            actual = copy.deepcopy(actual)
            if "render_source" in actual.get("audio", {}):
                actual.pop("audio")
                expected = {key: value for key, value in expected.items() if key != "audio"}
            assert actual == expected
        source = props["timeline"]["clips"][0]["audio"]["render_source"]
        assert source["source_from"] == 2 / (30000 / 1001)
        assert source["playback_rate"] == 1.5
        wav = state.paths[0].read_bytes()
        assert struct.unpack_from("<HHI", wav, 20) == (3, 2, 30000)
        assert len(wav) == 44 + 90000 * 8
        # Full native source, gain envelope only: scalar clip/track gains are
        # still 3 and 0.5 in props and are applied by the consumer once.
        assert struct.unpack_from("<ff", wav, 44 + 30000 * 8) == (0.25, -0.125)
        assert struct.unpack_from("<ff", state.paths[1].read_bytes(), 44 + 30000 * 8) == (0.25, -0.125)
        assert props["timeline"]["clips"][1]["volume"] == 0
        assert props["timeline"]["clips"][0]["volume"] == 3
        assert struct.unpack_from("<ff", wav, 44) == (0, 0)

    state.consume = consume
    state.execute()
    assert state.events == ["server-enter", "consume", "server-exit"]
    assert all(not path.exists() for path in state.paths)
    assert not state.props_path.exists()


@pytest.mark.parametrize("error", [RuntimeError("consumer failed"), KeyboardInterrupt(), subprocess.TimeoutExpired("consumer", 1)])
def test_normal_consumer_failure_cancel_and_timeout_release_attempt(normal_run, error):
    def fail():
        raise error

    normal_run.consume = fail
    with pytest.raises(type(error)):
        normal_run.execute()
    assert normal_run.events == ["server-enter", "consume", "server-exit"]
    assert all(not path.exists() for path in normal_run.paths)


def test_normal_pcm_error_never_launches_consumer(normal_run):
    raw = json.loads(normal_run.timeline_path.read_text())
    raw["clips"][1]["params"]["fadeInCurve"] = "unknown"
    original = normal_run.timeline_path.read_bytes()
    try:
        normal_run.timeline_path.write_text(json.dumps(raw))
        with pytest.raises(RuntimeError, match="ENVELOPE_UNRENDERED"):
            normal_run.execute()
    finally:
        normal_run.timeline_path.write_bytes(original)
    assert normal_run.events == ["server-enter", "server-exit"]


def test_normal_source_digest_error_never_prepares_or_launches(normal_run):
    original = normal_run.registry.read_bytes()
    raw = json.loads(original)
    raw["assets"]["sound"]["digest"] = "0" * 64
    try:
        normal_run.registry.write_text(json.dumps(raw))
        with pytest.raises(ValueError, match="integrity check"):
            normal_run.execute()
    finally:
        normal_run.registry.write_bytes(original)
    assert normal_run.events == []


def test_normal_native_decode_error_releases_attempt_before_consumer(normal_run):
    original = normal_run.registry.read_bytes()
    raw = json.loads(original)
    corrupt = b"managed bytes with no audio stream"
    raw["assets"]["sound"]["digest"] = hashlib.sha256(corrupt).hexdigest()
    normal_run.materialized_objects["object-sound"] = corrupt
    try:
        normal_run.registry.write_text(json.dumps(raw))
        with pytest.raises(RuntimeError, match="ffprobe"):
            normal_run.execute()
    finally:
        normal_run.registry.write_bytes(original)
    assert normal_run.events == ["server-enter", "server-exit"]
