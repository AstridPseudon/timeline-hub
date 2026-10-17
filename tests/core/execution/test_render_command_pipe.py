"""Refusal boundaries of the finite render relay; no renderer substitutes."""

import sys
from pathlib import Path

import pytest

from astrid.core.execution import render_command_pipe as relay


@pytest.mark.parametrize(
    "mutation", ["command", "backend", "verb", "cwd", "source", "role", "fields"]
)
def test_backend_refuses_drift_before_process_launch(tmp_path, mutation):
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.role = "executor"
    owner.backend_root = tmp_path
    owner.source_digest = "pinned"
    owner._source_digest = lambda: "pinned"
    owner.binding = {"admission": {}}
    request = dict(
        verb="support",
        command=[sys.executable, "run.py"],
        backend="rendering.remotion",
        request_path=str(tmp_path / "request.json"),
        result_path=str(tmp_path / "result.json"),
        cwd=str(tmp_path),
        timeout=5,
        required_binaries=[],
    )
    if mutation == "command":
        request["command"] = [sys.executable, "-c", "raise AssertionError()"]
    elif mutation == "backend":
        request["backend"] = "rendering.ffmpeg"
    elif mutation == "verb":
        request["verb"] = "finalize"
    elif mutation == "cwd":
        request["cwd"] = str(tmp_path.parent)
    elif mutation == "source":
        owner.source_digest = "different"
    elif mutation == "role":
        owner.role = "backend"
    elif mutation == "fields":
        request["env"] = {"PATH": "/untrusted"}
    with pytest.raises(ValueError, match="admitted Remotion backend"):
        owner._backend(request)


def test_executor_cannot_request_cli_or_supply_an_executable():
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.role = "executor"
    with pytest.raises(ValueError, match="admitted backend pipe"):
        owner._cli(
            {
                "argv": [sys.executable, "-c", "raise AssertionError()"],
                "cwd": "/",
                "render_environment": {},
            }
        )


@pytest.mark.parametrize("escape", ["outside", "symlink", "traversal"])
def test_protocol_artifact_must_stay_inside_retained_private_root(tmp_path, escape):
    from types import SimpleNamespace

    private = tmp_path / "private"
    private.mkdir()
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.policy = SimpleNamespace(private_write_root=private)
    if escape == "outside":
        path = tmp_path / "result.json"
    elif escape == "symlink":
        path = private / "alias"
        path.symlink_to(tmp_path)
    else:
        path = private / ".." / "result.json"
    with pytest.raises(ValueError, match="retained scratch"):
        owner._artifact(str(path), exists=False)


def test_cli_refuses_absent_host_closure_before_any_spawn(tmp_path):
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.role, owner.closure = "backend", None
    with pytest.raises(ValueError, match="host admitted installed closure"):
        owner._cli(
            {
                "argv": [
                    str(Path(sys.executable)),
                    str(tmp_path / "cli"),
                    "render",
                    "TimelineComposition",
                    "--props",
                    "/props",
                    "--output",
                    "/output",
                    "--concurrency=1",
                ],
                "cwd": str(tmp_path),
                "render_environment": {},
            }
        )


def test_component_free_video_producer_matches_closed_relay_environment(tmp_path, monkeypatch):
    """Controlled collaborators, real producer/consumer; stops before any launch."""
    from types import SimpleNamespace

    from astrid.packs.rendering.rendering.renderers.remotion import run

    project = tmp_path / 'project'
    project.mkdir()
    cli = project / 'cli.js'
    cli.write_text('// unit boundary; never executed')
    workspace = tmp_path / 'private'
    workspace.mkdir()
    document = workspace / 'timeline.json'
    document.write_text('{"clips": []}')
    assets = workspace / 'assets.json'
    assets.write_text('{"assets": {}}')
    monkeypatch.delenv('ASTRID_COMPONENTS', raising=False)
    monkeypatch.delenv('ASTRID_REMOTION_COMPONENT_STAGE', raising=False)
    monkeypatch.delenv('ASTRID_TIMELINE_SCHEMA_PYTHONPATH', raising=False)
    monkeypatch.setenv('ASTRID_REMOTION_STREAM_MEMORY_BUDGET_BYTES', '0')
    for name, function in {
        '_validate_project_dir': lambda _: SimpleNamespace(node_executable=Path(sys.executable), remotion_cli=cli),
        '_regenerate_element_registries': lambda *a: None,
        '_validate_renderer_effect_registry': lambda *a: None,
        '_effective_registry_state': lambda *a: {},
        '_serialize_timeline': lambda *a, **kw: {'clips': []},
        '_resolved_theme_for_render': lambda *a: {},
        '_stage_effect_assets_for_timeline': lambda *a, **kw: {},
        '_canonical_profile': lambda *a: SimpleNamespace(width=16, height=16, fps_rational=(30, 1)),
        '_timeline_composition_src': lambda *a: None,
    }.items():
        monkeypatch.setattr(run, name, function)

    class BeforeLaunch(Exception):
        pass

    def before_launch():
        raise BeforeLaunch('finite validation completed; no renderer launched')

    endpoint = {'port': 7011}
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.role = 'backend'
    owner.closure = SimpleNamespace(project=project, validate=lambda _: cli,
                                    require_retained_transport=lambda: None)
    owner.policy = SimpleNamespace(private_write_root=workspace, executable_bindings=[
        SimpleNamespace(name='node', executable=SimpleNamespace(resolved=Path(sys.executable).resolve()))])
    owner.environment = {}
    owner.renderer_transport = SimpleNamespace(metadata=lambda: endpoint, select_browser=before_launch)
    requests = []

    class Consumer:
        def request(self, operation, request):
            if operation == 'renderer_endpoint':
                return endpoint
            assert operation == 'remotion_cli'
            requests.append(request)
            return owner._cli(request)

    monkeypatch.setattr(relay, 'command_client', lambda: Consumer())
    with pytest.raises(BeforeLaunch):
        run._execute_remotion_locked(document, assets, workspace / 'video.mp4',
            provenance_out_path=workspace / 'video.mp4', project_dir=project,
            composition_id='TimelineComposition', theme_path=None, min_free_gb=None,
            staging_parent=workspace)
    assert len(requests) == 1
    assert 'ASTRID_REMOTION_COMPONENT_STAGE' not in requests[0]['render_environment']
    assert '--enforce-audio-track' in requests[0]['argv']
    for key, value in [('ASTRID_REMOTION_COMPONENT_STAGE', ''),
                       ('ASTRID_REMOTION_COMPONENT_STAGE', '{"root":"/outside"}'),
                       ('NODE_OPTIONS', '--require=/outside/code.js')]:
        altered = {**requests[0], 'render_environment': {
            **requests[0]['render_environment'], key: value}}
        # The producer correction does not widen the real consumer's allowlist.
        # It must still refuse both stage overrides and arbitrary Node code.
        # Recreate the now-cleaned private temp for the preceding path checks.
        temporary = Path(requests[0]['render_environment']['TMPDIR'])
        temporary.mkdir(parents=True, exist_ok=True)
        props = Path(requests[0]['argv'][5])
        props.write_text('{}')
        try:
            with pytest.raises(ValueError, match='unsupported Remotion invocation environment'):
                owner._cli(altered)
        finally:
            props.unlink()
            temporary.rmdir()
    assert not list(workspace.glob('.remotion-runtime-*'))
    assert not (workspace / '.remotion-props.json').exists()
