"""The native host must pass the serialized canonical carrier to public Composition."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tarfile
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from tests.packs.rendering.test_host_scene import host_project as _host_project
from tests.packs.rendering.test_scene_query_occlusion import admitted_public_artifact

host_project = _host_project

ROOT = Path(__file__).resolve().parents[3]
REMOTION = ROOT / "remotion"


@pytest.fixture
def exact_node(monkeypatch):
    node = resolve_pinned_node(REMOTION, override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok, node.problem
    assert node.version == "v20.19.4"
    monkeypatch.setenv("ASTRID_NODE_EXECUTABLE", str(node.path))
    return node.path


@pytest.fixture
def private_host(host_project, exact_node, tmp_path, monkeypatch):
    """Overlay only the package in a temporary copy of the locked host graph."""
    artifact_path, version = admitted_public_artifact("ASTRID_COMPOSITION_TEST_ARTIFACT")
    project, pack = host_project
    _bind_host(project, pack, exact_node, monkeypatch)
    private_modules = tmp_path / "node_modules"
    private_modules.mkdir()
    base_modules = REMOTION / "node_modules"
    for entry in base_modules.iterdir():
        if entry.name != "@banodoco":
            (private_modules / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
    package_scope = private_modules / "@banodoco"
    package_scope.mkdir()
    artifact = tmp_path / "artifact"
    artifact.mkdir()
    with tarfile.open(artifact_path) as archive:
        archive.extractall(artifact, filter="data")
    package = artifact / "package"
    (package_scope / "timeline-composition").symlink_to(package, target_is_directory=True)
    project_node_modules = project / "node_modules"
    project_node_modules.unlink()
    project_node_modules.symlink_to(private_modules, target_is_directory=True)
    assert json.loads((package / "package.json").read_text())["version"] == version
    before = {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in package.rglob("*") if p.is_file()}
    assert len(before) == 77
    yield project
    assert {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in package.rglob("*") if p.is_file()} == before
    _artifact, _version = admitted_public_artifact("ASTRID_COMPOSITION_TEST_ARTIFACT")


@pytest.fixture
def old_host(host_project, exact_node, monkeypatch):
    project, pack = host_project
    _bind_host(project, pack, exact_node, monkeypatch)
    return project


def _bind_host(project: Path, pack: Path, exact_node: Path, monkeypatch) -> None:
    project_node_modules = project / "node_modules"
    if project_node_modules.is_symlink() or project_node_modules.exists():
        project_node_modules.unlink()
    project_node_modules.symlink_to(REMOTION / "node_modules", target_is_directory=True)
    toolchain = resolve_pinned_node(REMOTION, override=str(exact_node))
    assert toolchain.ok and toolchain.version == "v20.19.4"
    for key in ("NODE_OPTIONS", "NODE_PATH", "PYTHONPYCACHEPREFIX"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("ASTRID_PACKS_PATH", str(pack))


def _probe(node: Path, project: Path) -> dict:
    script = r"""
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {build} from 'esbuild';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';
import {loadHostScene} from './native-scene.mjs';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';
import {TimelineComposition, compileCanonicalTransitions, DEFAULT_THEME,
  prepareCompositionScene, querySceneFrame, toRuntimeTheme} from '@banodoco/timeline-composition';

const project = process.cwd();
const output = path.join(project, 'host-registries.mjs');
const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
await build({entryPoints: [path.join(project, 'src/host-registries.ts')], outfile: output,
  bundle: true, platform: 'node', format: 'esm', nodePaths: [path.join(project, 'node_modules')],
  plugins: [{name: 'renderer-aliases', setup(builder) {
    builder.onResolve({filter: /^[^./]/}, async (args) => {
      if (args.pluginData?.resolvingPackage) return;
      const alias = Object.keys(aliases).find(key => args.path === key || args.path.startsWith(`${key}/`));
      if (!alias) {
        const resolved = await builder.resolve(args.path, {kind: args.kind,
          resolveDir: args.resolveDir, pluginData: {resolvingPackage: true}});
        if (resolved.errors.length) return {errors: resolved.errors};
        return {path: path.isAbsolute(resolved.path) ? pathToFileURL(resolved.path).href : resolved.path,
          external: true};
      }
      const target = path.join(aliases[alias], args.path.slice(alias.length).split('?')[0]);
      return builder.resolve(target, {kind: args.kind, resolveDir: project});
    });
  }}]});
const {resolveHostRegistries} = await import(pathToFileURL(output));
const prepareHostScene = await loadHostScene(project);
const theme = DEFAULT_THEME;
const runtimeTheme = toRuntimeTheme(theme);
const track = {id: 'visual', kind: 'visual', label: 'Visual'};
const clips = [
  {id: 'a', track: 'visual', clipType: 'custom', at: 0, hold: 1},
  {id: 'b', track: 'visual', clipType: 'custom', at: 1, hold: 1,
    transition: {type: 'fade', duration: .4}},
  {id: 'c', track: 'visual', clipType: 'custom', at: 2, hold: 1},
];
const tracks = [{track, clips}];
const registries = resolveHostRegistries(runtimeTheme);
const compiled = JSON.parse(JSON.stringify(
  compileCanonicalTransitions(tracks, 30, runtimeTheme, registries)));
const props = {timeline: {theme: 'historical-slug', tracks: [track], clips}, assets: {assets: {}},
  theme, registries, compiledTransitions: compiled};
const before = JSON.stringify(props);
const basis = {fps: 30, width: 1920, height: 1080};
const roles = {a: 'picture', b: 'picture', c: 'picture'};
const prepared = prepareHostScene(props, basis, roles);
const compiledAnswer = querySceneFrame(prepared, 24);

const composition = {id: 'test', width: 1920, height: 1080, fps: 30,
  durationInFrames: 90, defaultProps: {}, folderName: null, parentFolderName: null,
  component: () => null, nonce: [], schema: null, calculateMetadata: null, stack: null};
const render = (renderProps) => renderToStaticMarkup(createElement(
  Internals.CompositionManager.Provider, {value: {compositions: [composition],
    currentCompositionMetadata: null, folders: [], canvasContent: {type: 'composition', compositionId: 'test'}}},
  createElement(Internals.TimelineContext.Provider, {value: {frame: {test: 24}, playing: false,
    imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
    createElement(Internals.CanUseRemotionHooksProvider, null,
      createElement(TimelineComposition, renderProps)))));
const html = render(props);
const nativeProps = {...props};
delete nativeProps.compiledTransitions;
const nativeAnswer = querySceneFrame(prepareHostScene(nativeProps, basis, roles), 24);
const mismatch = (carrier) => {
  try {
    prepareHostScene({...props, compiledTransitions: carrier}, basis, roles);
    return null;
  } catch (error) {
    return String(error?.message ?? error);
  }
};
const wrongFps = JSON.parse(JSON.stringify(compiled));
wrongFps.fps = 24;
const wrongClip = JSON.parse(JSON.stringify(compiled));
wrongClip.tracks[0].clipIds[1] = 'wrong';
console.log(JSON.stringify({
  compiled,
  compiledAnswer,
  nativeAnswer,
  propsUnchanged: before === JSON.stringify(props),
  renderedTransition: html.includes('data-clip-id="b"') && html.includes('opacity:0.5'),
  wrongFps: mismatch(wrongFps),
  wrongClip: mismatch(wrongClip),
}));
"""
    result = subprocess.run(
        [str(node), "--input-type=module", "-e", script],
        cwd=project,
        env=os.environ.copy(),
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def _old_api_probe(node: Path, project: Path) -> str:
    script = r"""
import {loadHostScene} from './native-scene.mjs';
import {DEFAULT_THEME} from '@banodoco/timeline-composition';
const prepareHostScene = await loadHostScene(process.cwd());
try {
  prepareHostScene({timeline: {theme: 'old', tracks: [], clips: []}, assets: {assets: {}},
    theme: DEFAULT_THEME, compiledTransitions: {fps: 30, tracks: []}},
    {fps: 30, width: 1920, height: 1080}, {});
  console.log('accepted');
} catch (error) {
  console.log(String(error?.message ?? error));
}
"""
    result = subprocess.run(
        [str(node), "--input-type=module", "-e", script],
        cwd=project,
        env=os.environ.copy(),
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_host_forwards_serialized_compiled_carrier_to_scene_and_render(private_host, exact_node):
    result = _probe(exact_node, private_host)
    assert result["compiled"] == {
        "fps": 30,
        "tracks": [{"trackId": "visual", "clipIds": ["a", "b", "c"],
                     "incomingTransitions": [None, {"T": 12}, None]}],
    }
    layer = next(layer for layer in result["compiledAnswer"]["layers"] if layer["clipId"] == "b")
    assert (layer["contentFrame"], layer["transitionOpacity"]) == (6, 0.5)
    assert result["renderedTransition"]
    assert result["propsUnchanged"]


def test_host_refuses_mismatched_carriers_and_keeps_native_default(private_host, exact_node):
    result = _probe(exact_node, private_host)
    assert "frame rate" in result["wrongFps"]
    assert "clip identities" in result["wrongClip"]
    assert [layer["clipId"] for layer in result["nativeAnswer"]["layers"]] == ["a"]


def test_host_reports_old_public_api_as_unavailable_for_supplied_carrier(old_host, exact_node):
    assert _old_api_probe(exact_node, old_host) == (
        "scene compiled transition carrier unavailable in installed Composition API"
    )


def test_real_am_capabilities_on_final_public_context(private_host, exact_node):
    script = ROOT / "astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/scene.test.mjs"
    result = subprocess.run([str(exact_node), str(script), str(private_host), str(ROOT)],
                            text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
