"""Real invocation HTTP/WAV binding; run centrally after manager scope approval.

These module integration tests do not mint source authority or qualify export.
Window/layer positives deliberately need the source owner's original-phase join.
"""

import copy
import hashlib
import io
import json
import os
import struct
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import wave
from contextlib import contextmanager
from pathlib import Path

import pytest

from astrid.core.rendering.assets import AssetMaterializer, InvocationAssetServer
from astrid.core.rendering.contracts import FrameWindow
from astrid.core.rendering.remotion_runtime import RemotionRuntimeTools
from astrid.core.rendering.service import RenderService

RATE = 30000
FRAMES = RATE * 2
STEREO = {"sound": (8192, -4096), "other": (-12288, 2048)}


def _validate_invocation_url(url, expected_port):
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == "http" and parsed.hostname == "127.0.0.1"
    assert parsed.port == expected_port
    return parsed


def _get(url, *, expected_port):
    _validate_invocation_url(url, expected_port)
    # Explicitly avoid ambient proxy settings. This remains real host HTTP.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url, timeout=3) as response:
        assert response.status == 200
        body = response.read()
        assert int(response.headers["Content-Length"]) == len(body)
        return body


def _float_wav(body):
    assert body[:4] == b"RIFF" and body[8:12] == b"WAVE"
    assert struct.unpack_from("<I", body, 4)[0] == len(body) - 8
    chunks = {}
    offset = 12
    while offset + 8 <= len(body):
        name, length = struct.unpack_from("<4sI", body, offset)
        chunks[name] = body[offset + 8:offset + 8 + length]
        offset += 8 + length + length % 2
    assert struct.unpack("<HHIIHH", chunks[b"fmt "][:16]) == (
        3, 2, RATE, RATE * 8, 8, 32,
    )
    assert len(chunks[b"data"]) == FRAMES * 8
    return list(struct.iter_unpack("<ff", chunks[b"data"]))


def _assert_pcm(body, asset, *, origin, speed, duration, fade):
    """Analytic authored linear ramp; independent of the JS preparation helper."""
    samples = _float_wav(body)
    left, right = (value / 32768 for value in STEREO[asset])
    for index, actual in enumerate(samples):
        time = (index / RATE - origin) / speed
        gain = max(0, min(1, time / fade)) * max(0, min(1, (duration - time) / fade))
        # One float32 epsilon: decoding and WAV output retain native float PCM.
        assert actual == pytest.approx((left * gain, right * gain), rel=0, abs=2 ** -24), index
    assert any(left != 0 and right != 0 for left, right in samples)


@contextmanager
def _stage(tmp_path, *, fps=30, exceptional=False):
    from astrid.packs.rendering.rendering.renderers.remotion.normal_audio import (
        prepare_normal_audio_sources,
    )

    project = Path(os.environ["PCM_SERVED_PROJECT"]).resolve(strict=True)
    node = Path(os.environ["PCM_SERVED_NODE"]).resolve(strict=True)
    tools = RemotionRuntimeTools(node, "20.19.4", project / "node_modules/.bin/remotion")
    registry = tmp_path / "assets.json"
    source_root = tmp_path / "managed"
    source_root.mkdir()
    sources, entries = {}, {}
    for key, stereo in STEREO.items():
        stream = io.BytesIO()
        with wave.open(stream, "wb") as writer:
            writer.setparams((2, 2, RATE, 0, "NONE", "not compressed"))
            writer.writeframes(struct.pack("<hh", *stereo) * FRAMES)
        sources[key] = source_root / f"{key}.wav"
        sources[key].write_bytes(stream.getvalue())
        entries[key] = {
            "object_id": f"object-{key}", "digest": hashlib.sha256(stream.getvalue()).hexdigest(),
            "type": "audio/wav", "opaque": {"keep": [0, None, {"future": True}]},
        }
    registry.write_text(json.dumps({"assets": entries}))
    originals = {path: path.read_bytes() for path in [registry, *sources.values()]}
    sentinel = tmp_path / "unrelated.txt"
    sentinel.write_bytes(b"keep outside attempt")
    materializer = AssetMaterializer(
        registry, materialized_objects={f"object-{k}": p for k, p in sources.items()},
        materialized_root=source_root, staging_parent=tmp_path,
    )
    server = InvocationAssetServer(materializer.serving_root)
    prepared_paths = []
    try:
        with server:
            staged = {key: asset.local_path for key, asset in materializer.assets.items()}
            sibling = materializer.serving_root / "unrelated-stage.txt"
            sibling.write_bytes(b"keep until materializer closes")
            props = {
                "timeline": {"tracks": [
                    {"id": "A1", "kind": "audio", "volume": 0.5},
                    {"id": "A2", "kind": "audio", "volume": 2},
                ], "clips": [{
                    "id": key, "track": f"A{index + 1}", "asset": key, "at": 0.25,
                    "from": 0.05, "to": 1.55, "speed": 1.5, "volume": 3,
                    "params": {"fadeIn": 0.1, "fadeOut": 0.1},
                    "audio": {"opaque": {"keep": None}},
                    "app": {"astrid_shot_composition": {"source_offset": 350, "speed": 2}},
                    "opaque": {"future": [False, "verbatim"]},
                } for index, key in enumerate(STEREO)]},
                "assets": materializer.resolved_registry(server),
                "compiledTransitions": {"fps": fps, "tracks": []},
            }
            for key, path in staged.items():
                assert path is not None
                assert path.read_bytes() == originals[sources[key]]
                assert hashlib.sha256(path.read_bytes()).hexdigest() == entries[key]["digest"]
                assert _get(
                    props["assets"]["assets"][key]["file"], expected_port=server.port,
                ) == originals[sources[key]]
            try:
                with tempfile.TemporaryDirectory(prefix="pcm-attempt-", dir=materializer.serving_root) as root:
                    attempt = Path(root)

                    def prepare(value):
                        return prepare_normal_audio_sources(
                            value, materializer=materializer, asset_server=server,
                            attempt_directory=attempt, project_dir=project, runtime_tools=tools,
                        )

                    yield props, prepare, attempt, server, materializer, prepared_paths
                    if exceptional:
                        raise RuntimeError("test interrupted consumption")
            finally:
                assert not attempt.exists()
                assert sibling.read_bytes() == b"keep until materializer closes"
                for key, path in staged.items():
                    assert path.read_bytes() == originals[sources[key]]
                for url in prepared_paths:
                    with pytest.raises(urllib.error.HTTPError) as error:
                        _get(url, expected_port=server.port)
                    assert error.value.code == 404
                    error.value.close()
    finally:
        server.close()
        assert server.port == 0
        assert server.thread is None or not server.thread.is_alive()
        materializer.close()
        assert not materializer.staging_dir.exists()
        assert sentinel.read_bytes() == b"keep outside attempt"
        assert all(path.read_bytes() == content for path, content in originals.items())


@pytest.mark.parametrize("fps,origin", [(30, 2 / 30), (30000 / 1001, 1001 / 30000)])
def test_actual_http_binds_two_assets_to_native_enveloped_wavs(tmp_path, fps, origin):
    with _stage(tmp_path, fps=fps) as (props, prepare, attempt, server, _, urls):
        before = copy.deepcopy(props)
        output = prepare(props)
        assert props == before
        assert output["assets"] == before["assets"]
        wavs = []
        keys = []
        for original, clip in zip(before["timeline"]["clips"], output["timeline"]["clips"]):
            prepared = clip["audio"].pop("render_source")
            envelope = clip["audio"].pop("envelope")
            assert clip == original  # asset key, constant gains, opaque fields, trim/rate
            assert prepared["source_from"] == origin
            assert prepared["playback_rate"] == 1.5
            keys.append(json.loads(prepared["envelope_key"]))
            assert envelope == keys[-1]
            assert keys[-1] == {"keyframes": [{"at": 0, "value": 1}], "multiply": [
                {"keyframes": [{"at": 0, "value": 0, "curve": "linear"},
                               {"at": 3 / fps, "value": 1}]},
                {"keyframes": [{"at": 30 / fps - 3 / fps, "value": 1, "curve": "linear"},
                               {"at": 30 / fps, "value": 0}]},
            ]}
            urls.append(prepared["file"])
            body = _get(prepared["file"], expected_port=server.port)
            # Bind the actual URL to exactly one produced file, independent of returned metadata.
            relative = urllib.parse.unquote(urllib.parse.urlsplit(prepared["file"]).path).lstrip("/")
            path = (server.staging_dir / relative).resolve(strict=True)
            path.relative_to(attempt)
            assert body == path.read_bytes()
            _assert_pcm(body, clip["asset"], origin=origin, speed=1.5, duration=30 / fps, fade=3 / fps)
            wavs.append(body)
        assert keys[0] == keys[1] and urls[0] != urls[1] and wavs[0] != wavs[1]
        # A same-envelope/clock URL swap must be caught by the independent byte oracle.
        for asset, wrong in zip(STEREO, reversed(wavs)):
            with pytest.raises(AssertionError):
                _assert_pcm(wrong, asset, origin=origin, speed=1.5, duration=30 / fps, fade=3 / fps)


def test_forged_binding_render_source_and_double_apply_leave_inputs_intact(tmp_path):
    with _stage(tmp_path) as (props, prepare, attempt, _, _, urls):
        before = copy.deepcopy(props)
        wrong = copy.deepcopy(props)
        wrong["assets"]["assets"]["sound"]["file"] = props["assets"]["assets"]["other"]["file"]
        with pytest.raises(ValueError, match="registry differs"):
            prepare(wrong)
        missing = copy.deepcopy(props)
        missing["timeline"]["clips"][0]["asset"] = "missing"
        with pytest.raises((KeyError, ValueError)):
            prepare(missing)
        assert list(attempt.iterdir()) == []
        forged = copy.deepcopy(props)
        forged["timeline"]["clips"][0]["audio"]["render_source"] = {
            "file": props["assets"]["assets"]["other"]["file"],
            "envelope_key": "{}", "source_from": 2 / 30, "playback_rate": 1.5,
        }
        with pytest.raises(ValueError, match="already prepared"):
            prepare(forged)
        output = prepare(props)
        urls.extend(clip["audio"]["render_source"]["file"] for clip in output["timeline"]["clips"])
        files = {path: path.read_bytes() for path in attempt.rglob("*") if path.is_file()}
        with pytest.raises(ValueError, match="already prepared"):
            prepare(output)
        assert files == {path: path.read_bytes() for path in attempt.rglob("*") if path.is_file()}
        assert props == before


def test_changed_staged_asset_is_rejected_without_deleting_siblings(tmp_path):
    with _stage(tmp_path) as (props, prepare, attempt, _, materializer, _):
        selected = materializer.assets["sound"].local_path
        other = materializer.assets["other"].local_path
        original = selected.read_bytes()
        try:
            selected.write_bytes(other.read_bytes())
            with pytest.raises(ValueError, match="integrity check"):
                prepare(props)
            assert list(attempt.iterdir()) == []
            assert selected.read_bytes() == other.read_bytes()
        finally:
            selected.write_bytes(original)


def test_partial_preparation_failure_removes_only_owned_batch(tmp_path):
    with _stage(tmp_path) as (props, prepare, attempt, _, _, _):
        sibling = attempt / "unrelated.txt"
        sibling.write_bytes(b"belongs to another attempt consumer")
        props["timeline"]["clips"][1]["params"]["fadeInCurve"] = "unknown-curve"
        before = copy.deepcopy(props)
        with pytest.raises(RuntimeError, match="invalid keyframe or unknown curve"):
            prepare(props)
        assert props == before
        assert list(attempt.iterdir()) == [sibling]
        assert sibling.read_bytes() == b"belongs to another attempt consumer"


def test_wrong_managed_bytes_fail_before_server_start(tmp_path):
    payload = b"different managed bytes"
    registry = tmp_path / "assets.json"
    registry.write_text(json.dumps({"assets": {"sound": {
        "object_id": "object-sound", "digest": hashlib.sha256(b"original").hexdigest(),
    }}}))
    with pytest.raises(ValueError, match="integrity check"):
        AssetMaterializer(registry, materialized_objects={"object-sound": payload}, staging_parent=tmp_path)
    assert list(tmp_path.glob("astrid-render-assets-*")) == []


def test_interrupted_consumption_closes_server_and_only_attempt_files(tmp_path):
    with pytest.raises(RuntimeError, match="test interrupted consumption"):
        with _stage(tmp_path, exceptional=True) as (props, prepare, _, server, _, urls):
            output = prepare(props)
            for clip in output["timeline"]["clips"]:
                url = clip["audio"]["render_source"]["file"]
                urls.append(url)
                _assert_pcm(
                    _get(url, expected_port=server.port),
                    clip["asset"], origin=2 / 30, speed=1.5, duration=1, fade=0.1,
                )


@pytest.mark.parametrize("tracks", [None, ("A1", "A2")], ids=["window", "layer"])
def test_slice_retains_original_phase_on_actual_http_until_source_owner_joins(tmp_path, tracks):
    # Ordinary RED until the real source owner retains original compiled clips.
    # Do not supply fabricated original_clips or trust app.astrid_slice_origin.
    with _stage(tmp_path) as (props, prepare, _, server, _, urls):
        for clip in props["timeline"]["clips"]:
            clip.update(at=0, **{"from": 0, "to": 2, "speed": 1})
            clip["params"] = {"fadeIn": 0.5, "fadeOut": 0.5}
        before = copy.deepcopy(props)
        props["timeline"] = RenderService._window_timeline(
            props["timeline"], FrameWindow(start_frame=15, end_frame=45, fps_rational=(30, 1)),
            tracks=tracks,
        )
        sliced_before = copy.deepcopy(props)
        output = prepare(props)
        assert props == sliced_before
        assert before["timeline"]["clips"][0]["from"] == 0
        for clip in output["timeline"]["clips"]:
            url = clip["audio"]["render_source"]["file"]
            urls.append(url)
            _assert_pcm(
                _get(url, expected_port=server.port),
                clip["asset"], origin=0, speed=1, duration=2, fade=0.5,
            )
