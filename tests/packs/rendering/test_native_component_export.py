"""Native exporter source proof; these checks do not render/capture frames."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from astrid.core.pack.components import bind_component, resolve_component
from astrid.packs.rendering.rendering.renderers.remotion.components import stage_render_components
from astrid.sdk.timeline.commands import CommandError

REPO = Path(__file__).resolve().parents[3]
J029_ID = 'timeline.component/fresh_vignette_029.vignette'
J029_DIGEST = '1ac864cc8cf36842bc9fecddc80761f601eb88b7447eab8df6daf72a9ab98d0b'
NODE_RUN = subprocess.run
J029_SOURCE = 'fcded70fe529fb02aa59d79d1b0845f865950a3060786d073898212e429d0c39'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def timeline(identity):
    return {'clips': [{'id': 'owner', 'modifiers': [
        {'id': 'look', 'element': identity, 'params': {'strength': 0.6}}]}]}


@pytest.fixture(autouse=True)
def isolated_source_inventory(tmp_path, monkeypatch):
    # Never inspect the operator's installed pack inventory in source fixtures.
    monkeypatch.setenv('ASTRID_SOURCE_STATE', str(tmp_path / 'empty-source-state.json'))


@pytest.fixture(params=['synthetic', 'j029'])
def admitted(request, tmp_path, monkeypatch):
    monkeypatch.delenv('ASTRID_PACKS_PATH', raising=False)
    if request.param == 'j029':
        source = os.environ.get('ASTRID_TEST_COMPONENT_PACK_ROOT')
        if not source:
            pytest.skip('exact run-owned J029 input requires ASTRID_TEST_COMPONENT_PACK_ROOT')
        root = Path(source)
        identity = J029_ID
        assert sha(root / 'pack.yaml') == '8029e6e5ec2450f3bf5cdc948cd12d58130a39fe8ab86959c93d6243e154fc28'
        assert sha(root / 'extensions/timeline.component/vignette.yaml') == '19c32dd2f6222d2d90204e1bbfc0afa39be677dc04e9600b0f318d5ccf8bf010'
        assert sha(root / 'extensions/timeline.component/vignette.tsx') == J029_SOURCE
    else:
        root = tmp_path / 'synthetic'
        shutil.copytree(REPO / 'examples/packs/clip_looks', root)
        manifest = root / 'pack.yaml'
        value = yaml.safe_load(manifest.read_text())
        value['id'] = 'synthetic'
        manifest.write_text(yaml.safe_dump(value))
        descriptor = root / 'extensions/timeline.component/vignette.yaml'
        value = yaml.safe_load(descriptor.read_text())
        value['id'] = 'synthetic.arbitrary'
        value['implementation']['export'] = 'bindSynthetic'
        descriptor.write_text(yaml.safe_dump(value))
        (root / value['implementation']['path']).write_text('''
export const bindSynthetic = (host, descriptor) => host.declareModifier({
  kind: 'modifier', element: `${descriptor.point}/${descriptor.id}`,
  hosts: descriptor.hosts, bounds: 'preserve', alpha: 'preserve', support: 'preserve',
  component: ({children}) => children, resolveParams: (params) => params,
});
''')
        identity = 'timeline.component/synthetic.arbitrary'
    component = resolve_component(identity, extra_pack_roots=(str(root),))
    binding = bind_component(component, host='composition')
    if request.param == 'j029':
        assert binding['implementation_digest'] == J029_DIGEST
    env = {'ASTRID_COMPONENTS': json.dumps([{
        'identity': identity, 'implementation_digest': binding['implementation_digest']}]),
        'ASTRID_COMPONENT_PACK_ROOTS': json.dumps([str(root)])}
    return root, identity, binding, env


def stage(admitted, tmp_path):
    _, identity, _, env = admitted
    return stage_render_components(timeline(identity), output=tmp_path / 'stage', environment=env)


def probe(projection, identity, tmp_path, phase=""):
    dependencies = os.environ.get('ASTRID_TEST_REMOTION_DEPENDENCY_ROOT')
    if not dependencies:
        pytest.skip('source execution requires existing Remotion TypeScript/React dependencies')
    manifest = tmp_path / 'projection.json'
    manifest.write_text(json.dumps(projection))
    return NODE_RUN(['node', str(Path(__file__).with_name('fixtures') / 'native-component-probe.mjs'),
                           str(REPO), dependencies, str(manifest), identity, phase],
                          text=True, capture_output=True, check=False)


def test_native_root_consumes_exact_staged_declared_source(admitted, tmp_path):
    _, identity, binding, _ = admitted
    projection = stage(admitted, tmp_path)
    result = probe(projection, identity, tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    consumed = json.loads(result.stdout)
    assert consumed['identity'] == consumed['declaration'] == identity
    assert consumed['key'] == identity + '@' + binding['implementation_digest']
    declared = binding['descriptor']['implementation']['path']
    sources = [Path(f) for f in consumed['importedSources'] if f.endswith(declared)]
    assert len(sources) == 1
    assert sources[0].is_relative_to(Path(projection['root']))
    assert sha(sources[0]) == binding['sources'][declared]['sha256']
    if identity == J029_ID:
        assert sha(sources[0]) == J029_SOURCE


@pytest.mark.parametrize('damage', ['changed', 'missing', 'escape', 'module'])
def test_staged_source_refuses_before_root_execution(admitted, tmp_path, damage):
    _, identity, binding, _ = admitted
    projection = stage(admitted, tmp_path)
    filename = next(Path(f) for f in projection['files']
                    if f.endswith(binding['descriptor']['implementation']['path']))
    if damage == 'changed':
        filename.write_text('// tampered source')
    elif damage == 'missing':
        filename.unlink()
    elif damage == 'module':
        Path(projection['module']).write_text('export const componentBindings = [];')
    else:
        outside = tmp_path / 'outside.tsx'
        outside.write_bytes(filename.read_bytes())
        filename.unlink()
        filename.symlink_to(outside)
    result = probe(projection, identity, tmp_path)
    assert result.returncode != 0
    assert not result.stdout


def test_loader_rechecks_source_after_alias_setup(admitted, tmp_path):
    _, identity, _, _ = admitted
    projection = stage(admitted, tmp_path)
    result = probe(projection, identity, tmp_path, 'late-change')
    assert result.returncode != 0
    assert 'Changed or escaped staged component' in result.stderr
    assert not result.stdout


@pytest.mark.parametrize('damage', ['digest', 'identity', 'wrong-full-identity', 'unselected', 'no-roots', 'wrong-root', 'env-only'])
def test_untrusted_or_mismatched_selection_refuses(admitted, tmp_path, monkeypatch, damage):
    root, identity, _, original = admitted
    env = dict(original)
    requests = json.loads(env['ASTRID_COMPONENTS'])
    if damage == 'digest':
        requests[0]['implementation_digest'] = '0' * 64
    elif damage == 'identity':
        requests[0]['identity'] = 'vignette'
    elif damage == 'wrong-full-identity':
        requests[0]['identity'] = 'timeline.component/wrong.identity'
    elif damage == 'unselected':
        env.pop('ASTRID_COMPONENTS')
    elif damage == 'no-roots':
        env.pop('ASTRID_COMPONENT_PACK_ROOTS')
    else:
        env['ASTRID_COMPONENT_PACK_ROOTS'] = json.dumps([str(tmp_path)])
        # The synthetic root is under tmp_path, so use a disjoint explicit root.
        other = tmp_path / 'unrelated'
        other.mkdir()
        env['ASTRID_COMPONENT_PACK_ROOTS'] = json.dumps([str(other)])
        if damage == 'env-only':
            monkeypatch.setenv('ASTRID_PACKS_PATH', str(root))
    if damage != 'unselected':
        env['ASTRID_COMPONENTS'] = json.dumps(requests)
    with pytest.raises((CommandError, ValueError)):
        stage_render_components(timeline(identity), output=tmp_path / 'refused', environment=env)
    assert not (tmp_path / 'refused').exists()


@pytest.mark.parametrize('damage', ['changed-source', 'missing-source', 'changed-descriptor'])
def test_original_closure_rechecked_before_staging(admitted, tmp_path, damage):
    root, identity, binding, env = admitted
    copied = tmp_path / 'copy'
    shutil.copytree(root, copied)
    env = dict(env, ASTRID_COMPONENT_PACK_ROOTS=json.dumps([str(copied)]))
    source = copied / binding['descriptor']['implementation']['path']
    if damage == 'changed-source':
        source.write_text(source.read_text() + '\n// changed\n')
    elif damage == 'missing-source':
        source.unlink()
    else:
        descriptor = copied / 'extensions/timeline.component/vignette.yaml'
        descriptor.write_text(descriptor.read_text() + '\n# changed descriptor bytes\n')
    with pytest.raises((CommandError, ValueError)):
        stage_render_components(timeline(identity), output=tmp_path / 'refused', environment=env)


def test_component_free_build_keeps_default_path(tmp_path):
    assert stage_render_components({'clips': []}, output=tmp_path / 'none', environment={}) is None
    assert not (tmp_path / 'none').exists()


@pytest.mark.parametrize('admission', ['selected', 'no-roots', 'component-free'])
def test_exporter_passes_private_stage_to_native_bundle(admitted, tmp_path, monkeypatch, admission):
    from astrid.packs.rendering.rendering.renderers.remotion import run

    _, identity, _, env = admitted
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    if admission == 'no-roots':
        monkeypatch.delenv('ASTRID_COMPONENT_PACK_ROOTS')
    elif admission == 'component-free':
        monkeypatch.delenv('ASTRID_COMPONENTS')
        monkeypatch.setenv('ASTRID_REMOTION_COMPONENT_STAGE', 'unchecked-prior-stage')
    document_data = {'clips': []} if admission == 'component-free' else timeline(identity)
    document = tmp_path / 'timeline.json'
    document.write_text(json.dumps(document_data))
    assets = tmp_path / 'assets.json'
    assets.write_text('{"assets": {}}')
    project = tmp_path / 'remotion'
    project.mkdir()
    for name, function in {
        '_validate_project_dir': lambda _: SimpleNamespace(node_executable=Path('/node'), remotion_cli=Path('/cli')),
        '_regenerate_element_registries': lambda *a: None,
        '_validate_renderer_effect_registry': lambda *a: None,
        '_effective_registry_state': lambda *a: {},
        '_serialize_timeline': lambda *a, **k: document_data,
        '_resolved_theme_for_render': lambda *a: {},
        '_stage_effect_assets_for_timeline': lambda *a, **k: {},
    }.items():
        monkeypatch.setattr(run, name, function)
    captured = []

    class BeforeRender(Exception):
        pass

    def intercept(argv, **kwargs):
        if admission == 'component-free':
            assert kwargs['env']['ASTRID_REMOTION_COMPONENT_STAGE'] == ''
            captured.append(None)
            raise BeforeRender
        projection = json.loads(kwargs['env']['ASTRID_REMOTION_COMPONENT_STAGE'])
        props = json.loads(Path(argv[argv.index('--props') + 1]).read_text())
        assert 'modifierRegistry' not in props  # functions travel through imports
        result = probe(projection, identity, tmp_path)
        assert result.returncode == 0, result.stderr
        captured.append(projection)
        raise BeforeRender

    monkeypatch.setattr(run.subprocess, 'run', intercept)
    with pytest.raises(CommandError if admission == 'no-roots' else BeforeRender):
        run._execute_remotion_locked(document, assets, tmp_path / 'output.mp4',
            provenance_out_path=tmp_path / 'output.mp4', project_dir=project,
            composition_id='TimelineComposition', theme_path=None, min_free_gb=None,
            frame_numbers=[0], frame_output_dir=tmp_path / 'frames')
    if admission == 'selected':
        assert captured and not Path(captured[0]['root']).exists()
    elif admission == 'no-roots':
        assert not captured
    else:
        assert captured == [None]
    assert not (tmp_path / '.remotion-props.json').exists()
