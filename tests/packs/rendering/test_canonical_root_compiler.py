"""Direct prepared-props compilation; no host launch, browser or media decode.

During the coordinated package adoption ASTRID_COMPOSITION_TEST_ARTIFACT may
name the private public-export tarball. Peers always come from the locked host
graph; no dependencies are installed or copied.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.rendering.remotion_runtime import RemotionRuntimeTools, RemotionValidationError
from astrid.core.theme import builtin_theme
from astrid.packs.rendering.rendering.renderers.remotion.canonical_transitions import (
    compile_canonical_root_props,
)
from tests.packs.rendering.test_host_scene import host_project as _host_project
from tests.packs.rendering.test_scene_query_occlusion import admitted_public_artifact

host_project = _host_project
ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def compiler_host(host_project, tmp_path, monkeypatch):
    project, pack = host_project
    # Restore the fixture's native peer graph before creating a private overlay.
    modules = project / "node_modules"
    modules.unlink()
    modules.symlink_to(ROOT / "remotion/node_modules", target_is_directory=True)
    artifact, _version = admitted_public_artifact("ASTRID_COMPOSITION_TEST_ARTIFACT")
    overlay = tmp_path / "node_modules"
    overlay.mkdir()
    for entry in modules.iterdir():
        if entry.name != "@banodoco":
            (overlay / entry.name).symlink_to(entry.resolve(), target_is_directory=entry.is_dir())
    scope = overlay / "@banodoco"
    scope.mkdir()
    with tarfile.open(artifact) as archive:
        archive.extractall(tmp_path / "artifact", filter="data")
    (scope / "timeline-composition").symlink_to(tmp_path / "artifact/package", target_is_directory=True)
    modules.unlink()
    modules.symlink_to(overlay, target_is_directory=True)
    shutil.copyfile(ROOT / "remotion/canonical-transitions.mjs", project / "canonical-transitions.mjs")
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok and node.version == "v20.19.4"
    for name in ("NODE_OPTIONS", "NODE_PATH", "PYTHONPYCACHEPREFIX"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("ASTRID_PACKS_PATH", str(pack))
    tools = RemotionRuntimeTools(node.path, node.version, modules / "@remotion/cli/remotion-cli.js")
    package = modules / "@banodoco/timeline-composition"
    before = {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in package.rglob("*") if p.is_file()}
    assert len(before) == 77
    yield project, tools
    assert {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in package.rglob("*") if p.is_file()} == before


def props(*, start=1, duration=.4, first=False):
    clips = [] if first else [{"id": "a", "track": "v", "clipType": "custom", "at": 0, "hold": 1}]
    clips += [{"id": "b", "track": "v", "clipType": "custom", "at": start, "hold": 1,
               "transition": {"type": "fade", "duration": duration}},
              {"id": "c", "track": "v", "clipType": "custom", "at": start + 1, "hold": 1}]
    return {"timeline": {"theme": "historical-slug", "tracks": [{"id": "v", "kind": "visual"}],
                         "clips": clips}, "assets": {"assets": {}}, "theme": builtin_theme(),
            "review": {"shots": [], "preserve": [None, 3]}}


PROBE = r"""
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {build} from 'esbuild';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';
const project = process.cwd();
const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
const result = await build({stdin: {contents: `
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';
import {TimelineComposition, prepareCompositionScene, querySceneFrame, toRuntimeTheme}
  from '@banodoco/timeline-composition';
import {resolveHostRegistries} from './src/host-registries';
export const probe = ({props, frames}) => {
  const theme = toRuntimeTheme(props.theme);
  const registries = resolveHostRegistries(theme);
  const tracks = props.timeline.tracks.map(track => ({track,
    clips: props.timeline.clips.filter(clip => clip.track === track.id)}));
  const scene = prepareCompositionScene(tracks, props.assets, 30, theme, 1920, 1080,
    undefined, {}, {}, '', {}, registries, props.compiledTransitions);
  const composition = {id: 'probe', width: 1920, height: 1080, fps: 30,
    durationInFrames: 300, defaultProps: {}, folderName: null, parentFolderName: null,
    component: () => null, nonce: [], schema: null, calculateMetadata: null, stack: null};
  return frames.map(frame => ({answer: querySceneFrame(scene, frame),
    html: renderToStaticMarkup(createElement(Internals.CompositionManager.Provider,
      {value: {compositions: [composition], currentCompositionMetadata: null, folders: [],
        canvasContent: {type: 'composition', compositionId: 'probe'}}},
      createElement(Internals.TimelineContext.Provider,
        {value: {frame: {probe: frame}, playing: false, imperativePlaying: {current: false},
          audioAndVideoTags: {current: []}}},
        createElement(Internals.CanUseRemotionHooksProvider, null,
          createElement(TimelineComposition, {...props, registries})))))}));
};`, resolveDir: project, loader: 'tsx'}, absWorkingDir: project,
  nodePaths: [path.join(project, 'node_modules')], bundle: true, write: false,
  platform: 'node', format: 'esm', logLevel: 'silent',
  plugins: [{name: 'aliases', setup(builder) {
    builder.onResolve({filter: /^[^./]/}, async args => {
      if (args.pluginData?.resolvingPackage) return;
      const alias = Object.keys(aliases).find(key => args.path === key || args.path.startsWith(`${key}/`));
      if (alias) return builder.resolve(path.join(aliases[alias], args.path.slice(alias.length)),
        {kind: args.kind, resolveDir: project});
      const resolved = await builder.resolve(args.path, {kind: args.kind, resolveDir: args.resolveDir,
        pluginData: {resolvingPackage: true}});
      if (resolved.errors.length) return {errors: resolved.errors};
      return {path: path.isAbsolute(resolved.path) ? pathToFileURL(resolved.path).href : resolved.path,
        external: true};
    });
  }}]});
const {probe} = await import(`data:text/javascript;base64,${Buffer.from(result.outputFiles[0].text).toString('base64')}`);
console.log(JSON.stringify(probe(JSON.parse(fs.readFileSync(0, 'utf8')))));
"""


def observe(host, prepared, frames):
    project, tools = host
    from astrid.core.rendering.remotion_runtime import probe_context

    env = probe_context(environment=os.environ, python_executable=os.sys.executable)["node_env"]
    env["ASTRID_PACKS_PATH"] = os.environ["ASTRID_PACKS_PATH"]
    result = subprocess.run([str(tools.node_executable), "--input-type=module", "-e", PROBE],
                            input=json.dumps({"props": prepared, "frames": frames}), cwd=project,
                            env=env, check=False, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize("start,duration,first,origin,end,midpoint", [
    (1, .4, False, 18, 60, 24), (2, .4, True, 60, 90, 66),
    (2, .4, False, 48, 90, 54), (.5, .4, False, 3, 45, 9),
    (1, 2, False, 0, 90, 30),
])
def test_prepared_root_compiles_once_for_public_render_and_scene(
    compiler_host, start, duration, first, origin, end, midpoint,
):
    project, tools = compiler_host
    original = props(start=start, duration=duration, first=first)
    before = copy.deepcopy(original)
    prepared = compile_canonical_root_props(original, project_dir=project, runtime_tools=tools)
    assert original == before
    assert {k: v for k, v in prepared.items() if k != "compiledTransitions"} == original
    compiled = prepared["compiledTransitions"]
    assert compiled["fps"] == 30
    index = 0 if first else 1
    assert compiled["tracks"][0]["incomingTransitions"][index] == {"T": round(duration * 30)}
    with pytest.raises(ValueError, match="already been compiled"):
        compile_canonical_root_props(prepared, project_dir=project, runtime_tools=tools)
    rows = observe(compiler_host, json.loads(json.dumps(prepared)), [origin, midpoint, end - 1, end])
    def layer(row):
        return next((item for item in row["answer"]["layers"] if item["clipId"] == "b"), None)
    assert layer(rows[0])["opacity"] == 0
    assert layer(rows[1])["opacity"] == .5
    assert layer(rows[1])["contentFrame"] == midpoint - origin
    assert layer(rows[2]) is not None and layer(rows[3]) is None
    assert 'opacity:0.5' in rows[1]["html"]
    assert layer(rows[1])["clipId"] == "b"


def test_native_omission_retains_outgoing_public_semantics(compiler_host):
    native = props()
    rows = observe(compiler_host, native, [24, 57])
    assert "compiledTransitions" not in native
    assert [item["clipId"] for item in rows[0]["answer"]["layers"]] == ["a"]
    assert next(item for item in rows[1]["answer"]["layers"] if item["clipId"] == "c")["opacity"] == .5


@pytest.mark.parametrize("transition,message", [
    ({"type": "unknown", "duration": .4}, "Unknown transition id"),
    ({"type": "fade", "duration": .4, "params": {"easing": "ease-in"}}, "transition/unsupported-params"),
])
def test_unsupported_transition_refuses_without_native_fallback(compiler_host, transition, message):
    project, tools = compiler_host
    original = props()
    original["timeline"]["clips"][1]["transition"] = transition
    before = copy.deepcopy(original)
    with pytest.raises(RuntimeError, match=message):
        compile_canonical_root_props(original, project_dir=project, runtime_tools=tools)
    assert original == before


def test_compiler_refuses_unqualified_environment_before_node(compiler_host, monkeypatch):
    project, tools = compiler_host
    monkeypatch.setenv("NODE_OPTIONS", "--no-warnings")
    with pytest.raises(RemotionValidationError, match="loader/interpreter"):
        compile_canonical_root_props(props(), project_dir=project, runtime_tools=tools)


@pytest.mark.parametrize("alias", ["fade", "crossfade", "cross-fade"])
def test_canonical_aliases_use_public_resolution(compiler_host, alias):
    project, tools = compiler_host
    original = props()
    original["timeline"]["clips"][1]["transition"]["type"] = alias
    compiled = compile_canonical_root_props(original, project_dir=project, runtime_tools=tools)
    assert compiled["compiledTransitions"]["tracks"][0]["incomingTransitions"] == [None, {"T": 12}, None]


def test_old_public_api_refuses_instead_of_cutting(compiler_host, tmp_path):
    _, tools = compiler_host
    old = tmp_path / "old-host"
    old.mkdir()
    (old / "node_modules").symlink_to(ROOT / "remotion/node_modules", target_is_directory=True)
    for name in ("package.json", "canonical-transitions.mjs", "webpack-alias.mjs"):
        shutil.copyfile(ROOT / "remotion" / name, old / name)
    with pytest.raises(RuntimeError, match="no canonical transition compiler"):
        compile_canonical_root_props(props(), project_dir=old, runtime_tools=tools)


def test_custom_host_implementation_is_not_replaced_by_builtin(compiler_host):
    project, tools = compiler_host
    registry = project / "src/transitions.generated.ts"
    before = registry.read_text()
    try:
        registry.write_text(before + "\nTRANSITION_REGISTRY.fade = () => ({presentation: null, timing: null});\n")
        with pytest.raises(RuntimeError, match="transition/unsupported-implementation"):
            compile_canonical_root_props(props(), project_dir=project, runtime_tools=tools)
    finally:
        registry.write_text(before)
