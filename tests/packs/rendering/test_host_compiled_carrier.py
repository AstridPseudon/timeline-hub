"""The native host must pass the serialized canonical carrier to public Composition."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from tests.packs.rendering.test_host_scene import host_project

ROOT = Path(__file__).resolve().parents[3]
REMOTION = ROOT / "remotion"
NODE = Path("/tmp/vw-m3-agent-gate-node20.19.4/bin/node")
ARTIFACT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/vw-m3-incoming-public-api/artifacts/"
    "banodoco-timeline-composition-0.0.9.tgz"
)


@pytest.fixture
def exact_node(monkeypatch):
    monkeypatch.setenv("ASTRID_NODE_EXECUTABLE", str(NODE))
    return NODE


@pytest.fixture
def private_host(host_project, exact_node, tmp_path, monkeypatch):
    """Overlay only the package in a temporary copy of the locked host graph."""
    assert ARTIFACT.is_file()
    assert NODE.is_file()
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
    subprocess.run(["tar", "-xzf", str(ARTIFACT), "-C", str(artifact)], check=True)
    package = artifact / "package"
    shutil.copytree(package, package_scope / "timeline-composition")
    project_node_modules = project / "node_modules"
    project_node_modules.unlink()
    project_node_modules.symlink_to(private_modules, target_is_directory=True)
    assert json.loads((package / "package.json").read_text())["version"] == "0.0.9"
    return project


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
const props = {timeline: {theme: 'historical-slug', tracks, clips}, assets: {assets: {}},
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
  renderedFrame: html.includes('data-frame="6"'),
  renderedOpacity: html.includes('opacity:0.5'),
  renderedHasClip: html.includes('data-clip-id="b"'),
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


def test_host_forwards_serialized_compiled_carrier_to_scene_and_render(private_host):
    result = _probe(NODE, private_host)
    assert result["compiled"] == {
        "fps": 30,
        "tracks": [{"trackId": "visual", "clipIds": ["a", "b", "c"],
                     "incomingTransitions": [None, {"T": 12}, None]}],
    }
    layer = next(layer for layer in result["compiledAnswer"]["layers"] if layer["clipId"] == "b")
    assert (layer["contentFrame"], layer["transitionOpacity"]) == (6, 0.5)
    assert result["renderedFrame"] and result["renderedOpacity"] and result["renderedHasClip"]
    assert result["propsUnchanged"]


def test_host_refuses_mismatched_carriers_and_keeps_native_default(private_host):
    result = _probe(NODE, private_host)
    assert "frame rate" in result["wrongFps"]
    assert "clip identities" in result["wrongClip"]
    assert [layer["clipId"] for layer in result["nativeAnswer"]["layers"]] == ["a"]


def test_host_reports_old_public_api_as_unavailable_for_supplied_carrier(old_host):
    assert _old_api_probe(NODE, old_host) == (
        "scene compiled transition carrier unavailable in installed Composition API"
    )
