from pathlib import Path

from astrid.packs.rendering.rendering.renderers.remotion.run import PersistentRemotionFrameSession


def test_bench_uses_a_private_owner_and_enables_diagnostics(monkeypatch, tmp_path):
    seen = {}
    session = PersistentRemotionFrameSession()
    monkeypatch.setenv("ASTRID_FRAME_BENCH_ID", "probe-1")
    monkeypatch.setenv("ASTRID_FRAME_DIAGNOSTICS", "1")
    monkeypatch.setattr("astrid.core.execution.remotion_host_session.host_remotion_client", lambda: None)
    monkeypatch.setattr(session, "_owner_paths",
                        lambda identity: (seen.update(identity=identity), (tmp_path / "owner-deadbeef.sock", tmp_path / "lock"))[1])
    monkeypatch.setattr(session, "_ensure_owner", lambda **kwargs: False)
    monkeypatch.setattr(session, "_request", lambda request: (seen.update(request=request), {"ok": True, "diagnostics": {"browser": []}})[1])
    session.render(
        project_dir=tmp_path, composition_id="TimelineComposition", node_executable=Path("/node"),
        remotion_cli=Path("/cli"), props_path=tmp_path / "props.json", output_dir=tmp_path,
        frames=[30], resolution=None, port=1, environment={}, identity="real-identity",
    )
    assert seen["identity"] == "real-identity|bench:probe-1"
    assert seen["request"]["diagnostics"] is True
    assert session.diagnostics == {"browser": []}


def test_no_bench_leaves_identity_and_request_unchanged(monkeypatch, tmp_path):
    seen = {}
    session = PersistentRemotionFrameSession()
    monkeypatch.delenv("ASTRID_FRAME_BENCH_ID", raising=False)
    monkeypatch.delenv("ASTRID_FRAME_DIAGNOSTICS", raising=False)
    monkeypatch.setattr("astrid.core.execution.remotion_host_session.host_remotion_client", lambda: None)
    monkeypatch.setattr(session, "_owner_paths",
                        lambda identity: (seen.update(identity=identity), (tmp_path / "owner-aa.sock", tmp_path / "lock"))[1])
    monkeypatch.setattr(session, "_ensure_owner", lambda **kwargs: False)
    monkeypatch.setattr(session, "_request", lambda request: (seen.update(request=request), {"ok": True})[1])
    session.render(
        project_dir=tmp_path, composition_id="TimelineComposition", node_executable=Path("/node"),
        remotion_cli=Path("/cli"), props_path=tmp_path / "props.json", output_dir=tmp_path,
        frames=[1], resolution=None, port=1, environment={}, identity="real-identity",
    )
    assert seen["identity"] == "real-identity"
    assert "diagnostics" not in seen["request"]
