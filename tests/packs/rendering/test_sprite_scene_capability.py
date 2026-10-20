"""Registered AMsprite geometry on compiled inputs; SSR is not pixel proof."""
import copy
import json
import os
import subprocess
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.timeline import scene_answers
from astrid.core.timeline.shot_composition_projection import project_shot_composition
from astrid.packs.rendering.shared.rendering_backend import _serialize_timeline
from astrid.sdk.timeline.units import from_canvas
from tests.packs.rendering.test_scene_host import BASIS, ROOT, props

pytest_plugins = ['tests.packs.rendering.test_scene_host']


def prepared_props(tmp_path, clips, assets=None):
    graph = json.loads((ROOT / 'tests/fixtures/timeline/shot_composition.json').read_text())
    graph['occurrences'] = graph['occurrences'][:1]
    revision = graph['shot_revisions'][1]
    revision['internal_timeline_revision']['timeline'] = {
        'tracks': [{'id': 'sprite', 'kind': 'visual', 'label': 'Sprites'}], 'clips': clips,
    }
    revision['assets'] = []
    projection = project_shot_composition(graph, base_registry={'assets': assets or {}})
    timeline = tmp_path / 'timeline.json'
    timeline.write_text(json.dumps(projection.config))
    return props(assets=projection.registry) | {'timeline': _serialize_timeline(timeline)}


def sprite(params=None, **extra):
    return {'id': 'a-rocket', 'track': 'sprite', 'clipType': 'am-sprite', 'at': 0, 'hold': 2,
            'asset': 'R', 'params': params or {},
            'elementRef': {'kind': 'effect', 'id': 'am-sprite', 'packId': 'astrid_motion'}, **extra}


def asset(**extra):
    return {'file': '/sprite.png', 'resolution': '16x16', 'type': 'image/png', **extra}


def test_compiled_sprite_bounds_keep_logical_units_and_source(native_host, tmp_path):
    p = prepared_props(tmp_path, [sprite({'x': 4212, 'y': 20, 'scale': 8})], {'R': asset()})
    original = copy.deepcopy(p)
    row = scene_answers.host_frames_at(p, BASIS, [0])[0]
    layer = row['layers'][0]
    assert layer['clipId'] == p['timeline']['clips'][0]['id']
    assert layer['bounds'] == {'status': 'known', 'rect': {
        'x': 25272, 'y': 120, 'width': 128, 'height': 128}}
    assert layer['bounds']['rect']['x'] >= BASIS['width']
    assert layer['visible'] == 'unknown'  # Bounds do not certify decoded PNG alpha.
    assert p == original


def test_compiled_sprite_editor_units_snap_once(native_host, tmp_path):
    params = {key: from_canvas('am-sprite', key, value) for key, value in {'x': 4212, 'y': 20}.items()}
    params['scale'] = 8
    assert params == {'x': 702, 'y': 3, 'scale': 8}
    p = prepared_props(tmp_path, [sprite(params)], {'R': asset()})
    layer = scene_answers.host_frames_at(p, BASIS, [0])[0]['layers'][0]
    assert layer['bounds'] == {'status': 'known', 'rect': {
        'x': 4212, 'y': 18, 'width': 128, 'height': 128}}


@pytest.fixture
def sprite_ssr(native_host):
    node = resolve_pinned_node(ROOT / 'remotion', override=os.environ.get('ASTRID_NODE_EXECUTABLE'))
    assert node.ok, node.problem
    script = native_host / 'sprite-ssr.mjs'
    script.write_text(r"""
import {readFileSync} from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {build} from 'esbuild';
import {createElement as h} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';
import {TimelineComposition} from '@banodoco/timeline-composition';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';
const project = process.cwd();
const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
const bundle = await build({stdin: {contents: `
export {resolveHostRegistries} from './src/host-registries';
export {elementSource} from '../astrid/packs/astrid_motion/rendering/elements/_shared/am';`, resolveDir: project},
  bundle: true, write: false, platform: 'node', format: 'esm', jsx: 'automatic',
  nodePaths: [path.join(project, 'node_modules')], logLevel: 'silent',
  plugins: [{name: 'renderer-aliases', setup(builder) {
    builder.onResolve({filter: /^[^./]/}, async args => {
      if (args.pluginData?.resolvingPackage) return;
      const alias = Object.keys(aliases).find(key => args.path === key || args.path.startsWith(`${key}/`));
      if (alias) return builder.resolve(path.join(aliases[alias], args.path.slice(alias.length).split('?')[0]),
        {kind: args.kind, resolveDir: project});
      const resolved = await builder.resolve(args.path, {kind: args.kind, resolveDir: args.resolveDir,
        pluginData: {resolvingPackage: true}});
      if (resolved.errors.length) return {errors: resolved.errors};
      return {path: path.isAbsolute(resolved.path) ? pathToFileURL(resolved.path).href : resolved.path, external: true};
    });
  }}]});
const {resolveHostRegistries, elementSource} = await import(`data:text/javascript;base64,${Buffer.from(bundle.outputFiles[0].text).toString('base64')}`);
const {props, frames, basis} = JSON.parse(readFileSync(0, 'utf8'));
const metadata = {id: 'sprite', component: TimelineComposition, defaultProps: {}, ...basis,
  durationInFrames: 300, folderName: null, parentFolderName: null, nonce: [], schema: null,
  calculateMetadata: null, stack: null};
const html = frames.map(frame => renderToStaticMarkup(h(Internals.CompositionManager.Provider, {value: {
  compositions: [metadata], currentCompositionMetadata: null, folders: [],
  canvasContent: {type: 'composition', compositionId: 'sprite'},
}}, h(Internals.TimelineContext.Provider, {value: {frame: {sprite: frame}, playing: false,
  imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
h(Internals.CanUseRemotionHooksProvider, null,
  h(TimelineComposition, {...props, registries: resolveHostRegistries(props.theme)}))))));
console.log(JSON.stringify({html, sources: props.timeline.clips.map(c => elementSource(props.assets.assets[c.asset], c.params?.src))}));
""")

    def render(p, frames, *, sources=False):
        result = subprocess.run([str(node.path), str(script)],
                                input=json.dumps({'props': p, 'frames': frames, 'basis': BASIS}),
                                cwd=native_host, text=True, capture_output=True, timeout=30)
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)['sources' if sources else 'html']
    return render


def test_sprite_registered_ssr_preserves_drawing(sprite_ssr, tmp_path):
    import hashlib
    cases = [
        {}, {'x': 4212, 'y': 20, 'scale': 8},
        {'x': 10, 'y': 20, 'scale': 6, 'enter': 'stamp', 'blinkAt': 8},
        {'x': 10, 'y': 20, 'scale': 8, 'enter': 'slideIn', 'slideFrom': 'right',
         'keyframes': [{'frame': 5, 'x': 40, 'y': 22, 'flipX': True}]},
        {'x': 10, 'y': 20, 'frames': {'frameWidth': 8, 'frameHeight': 16, 'count': 4, 'fps': 12},
         'blinkAt': 8, 'blinkIndex': 3, 'outline': {'px': 2, 'pulse': 3},
         'shadow': {'groundY': 45}, 'silhouette': {'until': 6}},
    ]
    hashes = []
    for params in cases:
        p = prepared_props(tmp_path, [sprite(params)], {'R': asset()})
        hashes.append([hashlib.sha256(html.encode()).hexdigest() for html in sprite_ssr(p, [0, 1, 2, 5, 6, 8, 12])])
    assert hashlib.sha256(json.dumps(hashes).encode()).hexdigest() == "963140ecb235706a8f4c0ab57f5ba8f17984bad9ed58fa4f3647a128d888ca2b"


def test_public_sprite_offcanvas_run_in_mixedscale_and_integrity_addresses(native_host, sprite_ssr, tmp_path):
    clips = [
        sprite({'x': 4212, 'scale': 8, 'keyframes': [{'frame': 12, 'x': 4300, 'y': 20}]}, at=1, hold=1),
        sprite({'x': 20, 'scale': 6}, id='a-hourglass', asset='H', at=1.25, hold=.5),
        sprite({'x': -900, 'scale': 6, 'keyframes': [{'frame': 8, 'x': 300, 'y': 20}]},
               id='a-runner', asset='H', at=1.25, hold=.5),
    ]
    assets = {'R': asset(pixel_provenance={'executor': 'pixel.sprites', 'run_id': 'sprite-run',
              'lattice': {'detected': True, 'block': 4.0}, 'outline_integrity': {'fraction': .70}}),
              'H': asset(pixel_provenance={'outline_integrity': {'fraction': .56}})}
    p = prepared_props(tmp_path, clips, assets)
    # Use the compiler's explicit source join, never split a generated clip ID.
    compiled = {c['id']: c for c in p['timeline']['clips']}
    rows = scene_answers.host_frames_at(p, BASIS, [30, 38, 42, 46, 52])
    by_source = [{compiled[layer['clipId']]['app']['astrid_shot_composition']['source_clip_id']: layer
                  for layer in row['layers']} for row in rows]
    assert all(row['a-rocket']['bounds']['rect']['x'] >= BASIS['width'] for row in by_source)
    assert by_source[1]['a-runner']['bounds']['rect']['x'] == -5400
    assert by_source[3]['a-runner']['bounds']['rect'] == {'x': 1800, 'y': 120, 'width': 96, 'height': 96}
    assert by_source[1]['a-rocket']['bounds']['rect']['width'] == 128
    assert by_source[1]['a-hourglass']['bounds']['rect']['width'] == 96
    for source, fraction in [('a-rocket', .70), ('a-hourglass', .56)]:
        layer = by_source[1][source]
        c = compiled[layer['clipId']]
        assert c['shot_occurrence_id'] == 'occ-1'
        assert p['assets']['assets'][c['asset']]['pixel_provenance']['outline_integrity']['fraction'] == fraction
    html = sprite_ssr(p, [38, 46])
    assert 'left:-5400px' in html[0] and 'left:1800px;top:120px;transform:scale(6)' in html[1]
    assert 'left:25272px' in html[0] and 'left:25800px' in html[1]
    assert 'transform:scale(8)' in html[0] and 'transform:scale(6)' in html[0]


@pytest.mark.parametrize('extra', [{}, {'alpha': False, 'opaque': True}])
def test_known_sprite_bounds_do_not_invent_media_alpha(native_host, tmp_path, extra):
    p = prepared_props(tmp_path, [sprite({'x': 10, 'y': 20})], {'R': asset(**extra)})
    row = scene_answers.host_frames_at(p, BASIS, [0])[0]
    layer = row['layers'][0]
    assert layer['bounds']['rect'] == {'x': 60, 'y': 120, 'width': 96, 'height': 96}
    assert layer['visible'] == 'unknown' and layer['opacity'] is None
    assert layer['opaqueSupport'] == 'unknown'
    assert row['coverage'] == 'UNKNOWN'


@pytest.mark.parametrize('params,entry', [
    ({}, None), ({'width': 16, 'height': 16}, {'file': '/unknown.png'}),
    ({'src': '/static.png'}, {'resolution': '16x16'}),
    ({'outline': {'px': 2}}, asset()), ({'shadow': {'groundY': 45}}, asset()),
])
def test_sprite_missing_dimensions_and_decorations_stay_unknown(native_host, sprite_ssr, tmp_path, params, entry):
    p = prepared_props(tmp_path, [sprite(params)], {'R': entry} if entry else {})
    layer = scene_answers.host_frames_at(p, BASIS, [0])[0]['layers'][0]
    assert layer['bounds']['status'] == 'unknown'
    html = sprite_ssr(p, [0])[0]
    assert ('<img' in html) is (entry is not None)


def test_sprite_stepped_strip_and_hidden_frames_use_the_draw_clock(native_host, sprite_ssr, tmp_path):
    p = prepared_props(tmp_path, [sprite({'x': 10, 'y': 20, 'scale': 8, 'enter': 'stamp', 'blinkAt': 8,
        'keyframes': [{'frame': 5, 'x': 40, 'y': 22, 'flipX': True}]})], {'R': asset()})
    rows = scene_answers.host_frames_at(p, BASIS, [0, 1, 2, 5, 6, 8, 10])
    assert [row['layers'][0]['bounds']['rect']['y'] for row in rows] == [114, 114, 120, 120, 132, 132, 132]
    html = sprite_ssr(p, [1, 6, 8, 10])
    assert 'display:none' in html[0] and 'display:none' in html[2]
    assert 'left:240px;top:132px;transform:scale(8)' in html[1]
    assert 'scaleX(-1)' in html[1]
    for index in [1, 5]:
        assert rows[index]['layers'][0]['visible'] is False
    strip = prepared_props(tmp_path, [sprite({'src': '/strip.png', 'scale': 8, 'blinkAt': 8, 'blinkIndex': 3,
        'frames': {'frameWidth': 8, 'frameHeight': 16, 'count': 4, 'fps': 12}}, asset='missing')])
    layer = scene_answers.host_frames_at(strip, BASIS, [8])[0]['layers'][0]
    assert layer['bounds']['rect'] == {'x': 0, 'y': 0, 'width': 64, 'height': 128}
    assert 'left:-24px' in sprite_ssr(strip, [8])[0]


def test_sprite_renderer_selected_source_wins_over_static_fallback(native_host, sprite_ssr, tmp_path):
    p = prepared_props(tmp_path, [sprite({'src': '/wrong.png'})], {'R': asset(file='/selected.png')})
    layer = scene_answers.host_frames_at(p, BASIS, [0])[0]['layers'][0]
    assert layer['bounds']['rect']['width'] == 96
    html = sprite_ssr(p, [0])[0]
    assert '<img' in html
    assert sprite_ssr(p, [0], sources=True) == ['/selected.png']
    c = p['timeline']['clips'][0]
    c['elementRef']['packId'] = 'missing'
    with pytest.raises(scene_answers.SceneQueryUnavailable, match='Unknown effect owner'):
        scene_answers.host_frames_at(p, BASIS, [0])


@pytest.mark.parametrize('outer', [{'cropLeft': .1}, {'entrance': {'type': 'fade-up', 'duration': .2}}, {'exit': {'type': 'fade-up', 'duration': .2}}])
def test_sprite_unsupported_outer_geometry_stays_unknown(native_host, tmp_path, outer):
    p = prepared_props(tmp_path, [sprite(**outer)], {'R': asset()})
    layer = scene_answers.host_frames_at(p, BASIS, [2])[0]['layers'][0]
    assert layer['bounds']['status'] == 'unknown'


def test_sprite_public12_declarations_and_installed_bytes(native_host, tmp_path):
    import hashlib
    import shutil
    import tarfile

    package = native_host / 'node_modules/@banodoco/timeline-composition'
    archive = ROOT / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
    with tarfile.open(archive) as tar:
        expected = {m.name.removeprefix('package/'): hashlib.sha256(tar.extractfile(m).read()).hexdigest()
                    for m in tar.getmembers() if m.isfile()}

    def hashes():
        return {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in package.rglob('*') if p.is_file()}

    assert len(expected) == 77 and hashes() == expected
    assert json.loads((package / 'package.json').read_text())['version'] == '0.0.12'
    modules = native_host / 'node_modules'
    # Scopes belong to this stage; only dependency leaves point into read-only peers.
    assert not (modules / '@banodoco').is_symlink()
    assert not (modules / '@remotion').is_symlink()
    peers = Path(os.environ.get('ASTRID_TEST_NODE_MODULES', ROOT / 'remotion/node_modules'))
    for name in ['typescript', '@types/react', '@types/react-dom', '@types/node', 'csstype']:
        target = modules / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to((peers / name).resolve(), target_is_directory=True)
    project = tmp_path / 'typecheck'
    project.mkdir()
    (project / 'node_modules').symlink_to(modules, target_is_directory=True)
    for relative in [
        'astrid/packs/astrid_motion/rendering/elements/effects/am-sprite/component.tsx',
        'astrid/packs/astrid_motion/rendering/elements/_shared/am.tsx',
        'astrid/packs/rendering/shared/element_contracts.ts',
    ]:
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    (project / 'tsconfig.json').write_text(json.dumps({'compilerOptions': {
        'target': 'ES2022', 'module': 'ESNext', 'moduleResolution': 'Bundler', 'jsx': 'react-jsx',
        'strict': True, 'skipLibCheck': True, 'noEmit': True}, 'include': ['astrid']}))
    node = resolve_pinned_node(ROOT / 'remotion', override=os.environ.get('ASTRID_NODE_EXECUTABLE'))
    assert node.ok, node.problem
    result = subprocess.run([str(node.path), str(modules / 'typescript/bin/tsc'),
                             '--project', str(project / 'tsconfig.json')],
                            cwd=project, text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert hashes() == expected
