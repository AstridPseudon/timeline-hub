"""Owned props preparation selects public9 only with the inherited source.

No real renderer, Runtime admission, browser, local socket or pixel claim.
Public compiler and scene/render SSR probes use the exact public9 artifact.
"""
import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest

from astrid.core.rendering.verified_source import SOURCE_ENV
from astrid.packs.rendering.rendering.renderers.remotion import canonical_transitions
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion
from tests.packs.rendering.test_canonical_root_compiler import compiler_host as _compiler_host
from tests.packs.rendering.test_canonical_root_compiler import host_project as _host_project
from tests.packs.rendering.test_canonical_root_compiler import observe, props
from tests.packs.rendering.test_verified_source import admitted

compiler_host = _compiler_host
host_project = _host_project


@pytest.mark.parametrize('start,duration,first', [(1, .4, False), (2, .4, True), (2, .4, False), (1, 2, False)])
@pytest.mark.parametrize('capture', [False, True])
def test_verified_prepared_file_compiler_and_scene_agree(
    tmp_path, monkeypatch, compiler_host, start, duration, first, capture,
):
    project, tools = compiler_host
    original = props(start=start, duration=duration, first=first)['timeline']
    original['tracks'][0]['label'] = 'Visual'
    original['clips'][0]['app'] = {'opaque': {'keep': [None, 4]}}
    host, spec, snapshot, ref = admitted(tmp_path, config=original, capture=capture)
    values = host._materialize_inputs(spec, tmp_path / 'attempt')
    monkeypatch.setenv(SOURCE_ENV, values.timeline_source._anchor)
    timeline, assets = Path(values['timeline']), Path(values['assets_registry'])
    source_bytes = timeline.read_bytes()
    # The real backend is launched as python run.py, with no package name.
    monkeypatch.setattr(remotion, '__package__', '')
    monkeypatch.setattr(remotion, '_available_remotion_port', lambda: 3001)
    monkeypatch.setattr(remotion, '_validate_project_dir', lambda _: tools)
    monkeypatch.setattr(remotion, '_regenerate_element_registries', lambda *_: None)
    monkeypatch.setattr(remotion, '_validate_renderer_effect_registry', lambda *_: None)
    monkeypatch.setattr(remotion, '_effective_registry_state', lambda *_: {})
    monkeypatch.setattr(remotion, '_stage_effect_assets_for_timeline', lambda *a, **kw: {})
    calls, delivered, observed = [], [], []
    real_compile = canonical_transitions.compile_canonical_root_props
    def compile_once(root_props, **kwargs):
        calls.append(deepcopy(root_props))
        return real_compile(root_props, **kwargs)
    monkeypatch.setattr(canonical_transitions, 'compile_canonical_root_props', compile_once)
    def consume(props_path):
        delivered.append(json.loads(Path(props_path).read_text()))
    class Session:
        def render(self, **kwargs):
            consume(kwargs['props_path'])
            (kwargs['output_dir'] / 'frame-0.png').write_bytes(b'frame placeholder')
        def retain_staged_public_root(self, _):
            pass
    real_run = subprocess.run
    def render_video(command, **kwargs):
        if len(command) > 2 and command[2] == 'render':
            consume(command[command.index('--props') + 1])
            Path(command[command.index('--output') + 1]).write_bytes(b'video placeholder')
            return subprocess.CompletedProcess(command, 0, '', '')
        return real_run(command, **kwargs)
    monkeypatch.setattr(remotion.subprocess, 'run', render_video)
    output = tmp_path / 'out.mp4'
    remotion._execute_remotion_locked(timeline, assets, output, provenance_out_path=output,
        project_dir=project, composition_id='TimelineComposition', theme_path=None, min_free_gb=None,
        **({'frame_numbers': [0], 'frame_output_dir': tmp_path / 'frames', 'frame_session': Session(),
            'on_scene_props': lambda prepared, frames: observed.append((deepcopy(prepared), list(frames)))} if capture else {}))
    assert len(calls) == len(delivered) == 1
    assert calls[0]['timeline'] == original
    assert timeline.read_bytes() == source_bytes
    assert values.timeline_source.read()['ref'] == ref
    compiled = delivered[0]['compiledTransitions']
    assert compiled['tracks'][0]['incomingTransitions'][0 if first else 1] == {'T': round(duration * 30)}
    if capture:
        assert observed == [(delivered[0], [0])]
    # Query real public preparation and SSR with exactly the props delivered
    # to Remotion, rather than a separately compiled test-only vector.
    rows = observe(compiler_host, delivered[0], [60 if first else max(0, round(start * 30 - duration * 30))])
    assert next(layer for layer in rows[0]['answer']['layers'] if layer['clipId'] == 'b')['opacity'] == 0
    assert not list(tmp_path.glob('.remotion-props.json'))
