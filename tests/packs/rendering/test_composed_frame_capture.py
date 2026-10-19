from pathlib import Path

import pytest

from PIL import Image

from astrid.packs.rendering.actions.timeline_visualize.composed_frame import (
    FrameCaptureCache,
    FrameCaptureWorker,
    RemotionFrameProvider,
    frame_cache_key,
)
from astrid.packs.rendering.rendering.renderers.remotion.run import _resize_frame_outputs
from astrid.packs.rendering.actions.timeline_visualize.filmstrip_cards import (
    build_filmstrip_pack,
    plan_filmstrip,
)
from astrid.packs.rendering.actions.timeline_visualize.filmstrip_options import filmstrip_options


def _snapshot():
    return {
        "project_slug": "demo",
        "timeline_id": "timeline-1",
        "render_run_id": "capture-1",
        "video_digest": "sha256:" + "a" * 64,
        "fps_rational": [24, 1],
        "duration_frames": 48,
        "clips": [],
        "scripts": [],
        "metadata": {"capture_identity": "sha256:revision-a"},
    }


def test_exact_frame_planning_reports_one_frame_and_rejects_out_of_range():
    options = filmstrip_options({"frame": 7, "resolution": "320x180"})
    index = plan_filmstrip(_snapshot(), options)
    assert [card["frame"] for card in index["cards"]] == [7]
    assert index["cards"][0]["image"].endswith(".jpg")
    assert index["sampling"]["requested_frame"] == 7
    assert options["request"]["frame"] == 7

    try:
        plan_filmstrip(_snapshot(), {"frame": 48})
    except ValueError as exc:
        assert "outside" in str(exc)
    else:
        raise AssertionError("out-of-range frame was accepted")


def test_worker_is_serialized_and_expires(tmp_path):
    calls = []

    def render(frames, output_dir, resolution):
        calls.append((tuple(frames), tuple(resolution or ())))
        output = Path(output_dir)
        result = {}
        for frame in frames:
            path = output / f"frame-{frame:06d}.png"
            Image.new("RGB", (32, 18), (frame, 0, 0)).save(path)
            result[frame] = path
        return result

    worker = FrameCaptureWorker(render, idle_seconds=0)
    output = tmp_path / "frames"
    assert worker.capture([2, 1], output, [32, 18])
    assert calls == [((1, 2), (32, 18))]
    assert worker.started is False
    worker.close()


def test_worker_closes_after_renderer_failure(tmp_path):
    def render(_frames, _output_dir, _resolution):
        raise RuntimeError("renderer failed")

    worker = FrameCaptureWorker(render, idle_seconds=45)
    try:
        worker.capture([1], tmp_path / "frames", [32, 18])
    except RuntimeError as exc:
        assert str(exc) == "renderer failed"
    else:
        raise AssertionError("renderer failure was swallowed")
    assert worker.started is False
    assert worker._closed is True


def test_frame_outputs_are_resized_after_native_render(tmp_path):
    output = tmp_path / "frame-000000.png"
    Image.new("RGB", (1920, 1080), (12, 34, 56)).save(output)

    _resize_frame_outputs(tmp_path, (320, 180))

    with Image.open(output) as image:
        assert image.size == (320, 180)


def test_provider_uses_cache_on_second_request(tmp_path):
    calls = []

    def render(frames, output_dir, resolution):
        calls.append(tuple(frames))
        result = {}
        for frame in frames:
            path = Path(output_dir) / f"frame-{frame:06d}.png"
            Image.new("RGB", (32, 18), (frame, 0, 0)).save(path)
            result[frame] = path
        return result

    snapshot = _snapshot()
    cache = FrameCaptureCache(tmp_path / "cache")
    provider = RemotionFrameProvider(
        snapshot,
        timeline_path=tmp_path / "timeline.json",
        assets_path=tmp_path / "assets.json",
        project_dir=tmp_path,
        cache=cache,
        renderer=render,
        idle_seconds=0,
    )
    cards = [{"frame": 1, "image": "frames/frame-000000001.png"}]
    first = provider.capture(cards, tmp_path / "first", [32, 18])
    assert first["evidence_source"] == "fresh_capture"
    second_provider = RemotionFrameProvider(
        snapshot,
        timeline_path=tmp_path / "timeline.json",
        assets_path=tmp_path / "assets.json",
        project_dir=tmp_path,
        cache=cache,
        renderer=render,
        idle_seconds=0,
    )
    second = second_provider.capture(cards, tmp_path / "second", [32, 18])
    assert second["evidence_source"] == "cache"
    assert calls == [(1,)]
    assert (tmp_path / "second" / cards[0]["image"]).is_file()
    assert frame_cache_key(snapshot, 1, [32, 18]) != frame_cache_key(snapshot, 2, [32, 18])
    assert provider.worker.started is False
    provider.close()
    assert provider.worker.started is False


def test_cache_identity_changes_when_renderer_source_changes(tmp_path, monkeypatch):
    source_root = tmp_path / "renderer-source"
    source_root.mkdir()
    source_file = source_root / "effect.tsx"
    source_file.write_text("export const value = 1;", encoding="utf-8")
    monkeypatch.setenv("ASTRID_RENDERER_SOURCE_ROOT", str(source_root))
    first = frame_cache_key(_snapshot(), 1, [32, 18])
    source_file.write_text("export const value = 2;", encoding="utf-8")
    second = frame_cache_key(_snapshot(), 1, [32, 18])
    assert first != second


def test_cache_identity_ignores_ephemeral_attempt_directory_paths():
    first = _snapshot()
    second = _snapshot()
    first["metadata"]["asset_integrity"] = {
        "clip": {
            "observed_sha256": "abc",
            "path": "/tmp/astrid-attempt-first/managed-objects/0000-content",
        }
    }
    second["metadata"]["asset_integrity"] = {
        "clip": {
            "observed_sha256": "abc",
            "path": "/tmp/astrid-attempt-second/managed-objects/0000-content",
        }
    }
    assert frame_cache_key(first, 1, [32, 18]) == frame_cache_key(second, 1, [32, 18])


def test_cache_identity_changes_when_remotion_source_changes(tmp_path, monkeypatch):
    project = tmp_path / "remotion"
    source = project / "src"
    source.mkdir(parents=True)
    worker = source / "astrid-frame-worker.mjs"
    worker.write_text("const version = 1;", encoding="utf-8")
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(project))
    first = frame_cache_key(_snapshot(), 1, [32, 18])
    worker.write_text("const version = 2;", encoding="utf-8")
    second = frame_cache_key(_snapshot(), 1, [32, 18])
    assert first != second


def test_cache_identity_changes_when_remotion_config_changes(tmp_path, monkeypatch):
    project = tmp_path / "remotion"
    (project / "src").mkdir(parents=True)
    config = project / "remotion.config.ts"
    config.write_text("export default {};\n", encoding="utf-8")
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(project))
    first = frame_cache_key(_snapshot(), 1, [32, 18])
    config.write_text("export default { enableTailwind: true };\n", encoding="utf-8")
    second = frame_cache_key(_snapshot(), 1, [32, 18])
    assert first != second


def test_shared_owner_force_release_forwards_force_to_session(monkeypatch):
    from astrid.packs.rendering.actions.timeline_visualize import composed_frame

    class Session:
        def __init__(self):
            self.calls = []

        def close(self, *, force=False):
            self.calls.append(force)

    session = Session()
    owner = object.__new__(composed_frame._SharedRemotionOwner)
    owner.session = session
    owner.lock = __import__("threading").RLock()
    owner.references = 1
    owner.timer = None
    owner.timer_generation = 0
    owner.closed = False
    owner.idle_seconds = 45.0
    owner.release(force=True)
    assert session.calls == [True]


def _pretend_launchctl_present(monkeypatch):
    """Make the /bin/launchctl existence gate in _remove_owner_job pass on any host."""
    real_is_file = Path.is_file
    monkeypatch.setattr(
        Path, "is_file", lambda self: True if str(self) == "/bin/launchctl" else real_is_file(self)
    )


def test_force_close_removes_submitted_launchd_owner(monkeypatch, tmp_path):
    from astrid.packs.rendering.rendering.renderers.remotion import run as remotion_run

    calls = []

    class Connection:
        def sendall(self, value):
            calls.append(("send", value))

        def close(self):
            calls.append(("close",))

    def fake_connect(_path, *, timeout_seconds=None):
        calls.append(("connect", timeout_seconds))
        return Connection()

    def fake_read_response(_connection):
        calls.append(("read",))
        return {"ok": True, "released": True, "exit": True}

    def fake_run(command, **kwargs):
        calls.append(("run", command))
        return __import__("types").SimpleNamespace(returncode=0)

    _pretend_launchctl_present(monkeypatch)
    monkeypatch.setattr(remotion_run.sys, "platform", "darwin")
    monkeypatch.setattr(remotion_run.subprocess, "run", fake_run)
    session = remotion_run.PersistentRemotionFrameSession()
    monkeypatch.setattr(session, "_connect", fake_connect)
    monkeypatch.setattr(session, "_read_response", fake_read_response)
    socket_path = tmp_path / ("owner-" + "a" * 32 + ".sock")
    session._socket_path = socket_path
    session.close(force=True)

    # The owner must acknowledge a forced release before its launchd job is removed.
    assert calls == [
        ("connect", 5.0),
        ("send", b'{"type":"release","force":true}\n'),
        ("read",),
        ("close",),
        ("run", ["/bin/launchctl", "remove", "astrid-rfo-" + "a" * 32]),
    ]
    assert session._socket_path is None


def test_filmstrip_pack_accepts_capture_provider_without_video(tmp_path):
    snapshot = _snapshot()
    snapshot["duration_frames"] = 3
    options = filmstrip_options({"frame": 1, "resolution": "32x18"})
    options["frame_extension"] = "png"

    class Provider:
        def capture(self, cards, out_root, resolution):
            for card in cards:
                path = Path(out_root) / card["image"]
                path.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (32, 18), "#204050").save(path)
            return {"evidence_source": "fresh_capture", "fresh_frames": len(cards), "cached_frames": 0}

    result = build_filmstrip_pack(
        out_root=tmp_path / "filmstrip-view",
        snapshot=snapshot,
        options=options,
        frame_provider=Provider(),
    )
    assert result["frame_index"]["frame_capture"]["evidence_source"] == "fresh_capture"
    assert result["cards"][0]["image"].endswith(".png")
    assert Path(result["paths"]["png"][0]).is_file()


def _actual_session_boundary_fixture(monkeypatch, tmp_path):
    from astrid.packs.rendering.rendering.renderers.remotion import run as remotion_run
    session = remotion_run.PersistentRemotionFrameSession()
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "astrid-frame-worker.mjs").write_text("// controlled selected helper fixture")
    socket_path = tmp_path / ("owner-" + "c" * 32 + ".sock")
    events = []
    monkeypatch.setattr(session, "_owner_paths", lambda _: (socket_path, socket_path.with_suffix(".lock")))
    class Connection:
        def sendall(self, value):
            assert value == b'{"type":"release","force":true}\n'
        def close(self): pass
    def connect(*_args, **kwargs):
        if kwargs.get("timeout_seconds") == 5.0: return Connection()
        raise FileNotFoundError()
    monkeypatch.setattr(session, "_connect", connect)
    monkeypatch.setattr(session, "_read_response", lambda _: {"ok": True, "released": True, "exit": True})
    def launch(**kwargs):
        events.append(("launch", kwargs["socket_path"]))
    monkeypatch.setattr(session, "_launch_owner", launch)
    monkeypatch.setattr(session, "_remove_owner_job", lambda selected: events.append(("remove", selected)) or
                        {"removal_attempted": True, "returncode": 0, "native_cleanup": "UNPROVED"})
    def request(payload):
        events.append(("request", payload["type"]))
        return {"ok": True}
    monkeypatch.setattr(session, "_request", request)
    arguments = dict(project_dir=tmp_path, composition_id="fixture", node_executable=tmp_path / "node",
                     remotion_cli=tmp_path / "cli", props_path=tmp_path / "props.json", output_dir=tmp_path / "frames",
                     frames=[0], resolution=(160, 90), port=8000, environment={}, identity="fixture-owner")
    return remotion_run, session, socket_path, events, arguments


def test_successful_submission_readiness_failure_retains_owner_for_cleanup(monkeypatch, tmp_path):
    import pytest
    _, session, selected, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    timeout = TimeoutError("controlled owner readiness timeout")
    def wait(socket):
        assert socket == selected and session._socket_path == selected
        raise timeout
    monkeypatch.setattr(session, "_wait_for_owner", wait)
    with pytest.raises(TimeoutError) as caught:
        session.render(**arguments)
    assert caught.value is timeout
    assert events == [("launch", selected), ("remove", selected)]
    assert session._socket_path is None
    assert [r["stage"] for r in session._owner_boundary_diagnostics] == [
        "submission_requested", "submitted", "readiness_failed", "removal_observed"]
    assert session._owner_boundary_diagnostics[-1]["native_cleanup"] == "UNPROVED"
    session.close(force=True)
    assert len(events) == 2


def test_discovered_owner_readiness_failure_does_not_acquire_cleanup(monkeypatch, tmp_path):
    import pytest
    _, session, _, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(session, "_connect", lambda *_, **__: __import__("types").SimpleNamespace(close=lambda: None))
    monkeypatch.setattr(session, "_wait_for_owner", lambda *_: (_ for _ in ()).throw(TimeoutError("not ready")))
    with pytest.raises(TimeoutError): session.render(**arguments)
    session.close(force=True)
    assert events == [] and session._socket_path is None
    assert [r["stage"] for r in session._owner_boundary_diagnostics] == ["existing_owner_discovered", "readiness_failed"]


def test_prelaunch_missing_helper_does_not_acquire_cleanup(monkeypatch, tmp_path):
    import pytest
    module, session, _, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    (tmp_path / "src" / "astrid-frame-worker.mjs").unlink()
    fallback = tmp_path / "unselected-checkout" / "remotion" / "src"
    fallback.mkdir(parents=True)
    (fallback / "astrid-frame-worker.mjs").write_text("// must not be selected")
    monkeypatch.setattr(module, "REPO_ROOT", fallback.parents[1])
    with pytest.raises(FileNotFoundError): session.render(**arguments)
    session.close(force=True)
    assert events == [] and session._socket_path is None


def test_refused_or_ambiguous_submission_does_not_acquire_cleanup(monkeypatch, tmp_path):
    import pytest
    import subprocess
    module, session, _, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    for error in (module._FrameOwnerSubmissionRefused("controlled refusal", 7),
                  subprocess.TimeoutExpired("controlled submit", 1)):
        def launch(**_): raise error
        monkeypatch.setattr(session, "_launch_owner", launch)
        with pytest.raises(type(error)) as caught: session.render(**arguments)
        assert caught.value is error
        session.close(force=True)
        assert events == [] and session._socket_path is None
    assert "submission_refused" in [r["stage"] for r in session._owner_boundary_diagnostics]
    assert "submission_unresolved" in [r["stage"] for r in session._owner_boundary_diagnostics]
    assert "submitted" not in [r["stage"] for r in session._owner_boundary_diagnostics]


def test_previously_bound_owner_refusal_keeps_established_cleanup_responsibility(monkeypatch, tmp_path):
    import pytest
    module, session, selected, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    session._socket_path = selected
    # The fixture's 1.0 s liveness probe of the bound endpoint fails (only the 5.0 s
    # release connection succeeds), so replacement of the retained owner is refused.
    with pytest.raises(RuntimeError, match="replacement refused") as caught: session.render(**arguments)
    assert isinstance(caught.value.__cause__, FileNotFoundError)
    # The established cleanup responsibility is discharged by an acknowledged forced release.
    assert events == [("remove", selected)]
    assert session._owner_cleanup_error is caught.value.__cause__
    stages = [r["stage"] for r in session._owner_boundary_diagnostics]
    assert "submission_requested" not in stages and "submitted" not in stages


def test_different_previous_binding_is_not_replaced_by_refusal(monkeypatch, tmp_path):
    import pytest
    module, session, _, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    original = tmp_path / "owner-previous.sock"
    session._socket_path = original
    def launch(**_): raise module._FrameOwnerSubmissionRefused("controlled refusal", 7)
    monkeypatch.setattr(session, "_launch_owner", launch)
    with pytest.raises(module._FrameOwnerSubmissionRefused): session.render(**arguments)
    assert events == [] and session._socket_path == original


def test_readiness_failure_stays_primary_if_cleanup_raises(monkeypatch, tmp_path):
    import pytest
    _, session, _, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    timeout = TimeoutError("controlled readiness failure")
    cleanup = OSError("controlled removal failure")
    monkeypatch.setattr(session, "_wait_for_owner", lambda *_: (_ for _ in ()).throw(timeout))
    monkeypatch.setattr(session, "_remove_owner_job", lambda *_: (_ for _ in ()).throw(cleanup))
    with pytest.raises(TimeoutError) as caught: session.render(**arguments)
    assert caught.value is timeout and caught.value.__cause__ is cleanup
    assert not any(stage == "request" for stage, _ in events)
    assert session._owner_boundary_diagnostics[-1] == {"stage": "cleanup_failed", "error_type": "OSError"}


def test_successful_readiness_request_and_existing_close_behavior(monkeypatch, tmp_path):
    _, session, selected, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(session, "_wait_for_owner", lambda *_: None)
    session.render(**arguments)
    assert events == [("launch", selected), ("request", "render")]
    assert session._socket_path == selected and session._identity == "fixture-owner"
    session.close(force=True)
    assert events[-1] == ("remove", selected)


def test_request_failure_preserves_existing_force_close(monkeypatch, tmp_path):
    import pytest
    _, session, selected, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(session, "_wait_for_owner", lambda *_: None)
    error = RuntimeError("controlled request failure")
    monkeypatch.setattr(session, "_request", lambda *_: (_ for _ in ()).throw(error))
    with pytest.raises(RuntimeError) as caught: session.render(**arguments)
    assert caught.value is error and events == [("launch", selected), ("remove", selected)]


def test_launchd_removal_records_return_code_without_native_cleanup_claim(monkeypatch, tmp_path):
    module, session, selected, _, _ = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    _pretend_launchctl_present(monkeypatch)
    monkeypatch.setattr(module.sys, "platform", "darwin")
    monkeypatch.setattr(module.subprocess, "run", lambda *_, **__: __import__("types").SimpleNamespace(returncode=9))
    result = module.PersistentRemotionFrameSession._remove_owner_job(selected)
    assert result == {"removal_attempted": True, "returncode": 9, "native_cleanup": "UNPROVED"}


def test_warm_owner_retention_requires_explicit_allocation(monkeypatch):
    from astrid.packs.rendering.actions.timeline_visualize.composed_frame import FrameCaptureWorker
    monkeypatch.delenv("ASTRID_WARM_IDLE_SECONDS", raising=False)
    monkeypatch.delenv("ASTRID_REMOTION_WARM_MEMORY_BUDGET_BYTES", raising=False)
    assert FrameCaptureWorker(lambda *args: {}).idle_seconds == 45
    monkeypatch.setenv("ASTRID_REMOTION_WARM_MEMORY_BUDGET_BYTES", str(512 * 1024**2))
    assert FrameCaptureWorker(lambda *args: {}).idle_seconds == 300
    # The one knob for every warm holder overrides the owner's own default.
    monkeypatch.setenv("ASTRID_WARM_IDLE_SECONDS", "900")
    assert FrameCaptureWorker(lambda *args: {}).idle_seconds == 900
    monkeypatch.setenv("ASTRID_WARM_IDLE_SECONDS", "nan")
    assert FrameCaptureWorker(lambda *args: {}).idle_seconds == 300


def test_frame_session_launches_helper_from_selected_project_with_empty_checkout(monkeypatch, tmp_path):
    module, session, selected, events, arguments = _actual_session_boundary_fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(module, 'REPO_ROOT', tmp_path / 'installed-site-without-remotion')
    launched = []
    def launch(**kwargs):
        launched.append(kwargs)
        events.append(('launch', kwargs['socket_path']))
    monkeypatch.setattr(session, '_launch_owner', launch)
    monkeypatch.setattr(session, '_wait_for_owner', lambda *_: None)
    session.render(**arguments)
    assert len(launched) == 1
    assert launched[0]['helper'] == arguments['project_dir'] / 'src/astrid-frame-worker.mjs'
    assert launched[0]['project_dir'] == arguments['project_dir']
    assert launched[0]['node_executable'] == arguments['node_executable']
    assert session._socket_path == selected and session._identity == 'fixture-owner'
    session.close(force=True)
    assert events[-1] == ('remove', selected)
    assert session._socket_path is None and session._identity is None
    assert session._owner_boundary_diagnostics[-1]['native_cleanup'] == 'UNPROVED'


@pytest.mark.parametrize("boundary", ["worker", "provider"])
def test_native_render_primary_survives_secondary_cleanup_failure(tmp_path, boundary):
    primary = ValueError("original native render connection failed")
    cleanup = RuntimeError("original owner release remains uncertain")
    class Renderer:
        calls = 0
        def __call__(self, *_args):
            self.calls += 1
            raise primary
        def close(self, *, force=False):
            assert force is True
            raise cleanup
    renderer = Renderer()
    if boundary == "worker":
        worker = FrameCaptureWorker(renderer, idle_seconds=45)
        invoke = lambda: worker.capture([1], tmp_path / "frames", [32, 18])
    else:
        provider = RemotionFrameProvider(
            _snapshot(), timeline_path=tmp_path / "timeline.json",
            assets_path=tmp_path / "assets.json", project_dir=tmp_path,
            cache=FrameCaptureCache(tmp_path / "cache"), renderer=renderer,
            idle_seconds=45,
        )
        worker = provider.worker
        invoke = lambda: provider.capture(
            [{"frame": 1, "image": "frames/frame-000000001.png"}],
            tmp_path / "out", [32, 18],
        )
    with pytest.raises(ValueError) as caught:
        invoke()
    assert caught.value is primary and caught.value.__cause__ is cleanup
    assert renderer.calls == 1 and worker._closed and not worker.started
    assert not list(tmp_path.glob("astrid-frame-capture-*"))
