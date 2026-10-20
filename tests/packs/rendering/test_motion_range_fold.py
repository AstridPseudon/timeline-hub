"""Inactive exact folds use the host's public preparation and component clock."""

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from tests.packs.rendering.test_scene_query_occlusion import admitted_public_artifact

ROOT = Path(__file__).resolve().parents[3]
COMPONENT = """
import {createElement} from 'react';
import {useCurrentFrame} from 'remotion';

const support = (clip, frame) => {
  const p = clip.params;
  let motion = {phase: frame === 181 ? 1 : 0, clock: frame, energy: -.125,
    k1: 1, k2: 2, k3: 3, k4: 4, k5: 5};
  if (p.distinct) motion = Object.fromEntries(Array.from({length: 8}, (_, i) => [String(i), frame]));
  if (p.vary && frame === 2) motion = {energy: -.125};
  if (p.vary && frame === 3) motion = {phase: NaN};
  if (p.invalid) motion = {phase: ({nan: NaN, infinity: Infinity,
    bool: true, string: '0', null: null})[p.invalid]};
  return {presence: p.presence ?? 'present', opaqueSupport: 'rect',
    bounds: {status: 'known', rect: {x: 0, y: 0, width: 200, height: 100}},
    ...(p.vary && frame === 1 ? {} : {diagnostics: {motion}})};
};
const Probe = ({clip}) => {
  const facts = support(clip, useCurrentFrame());
  if (facts.presence === 'absent') return null;
  const {x, y, width, height} = facts.bounds.rect;
  return createElement('div', {'data-phase': facts.diagnostics?.motion?.phase,
    style: {position: 'absolute', left: x, top: y, width, height, background: '#123456'}});
};
export default Object.assign(Probe, {
  prepareSceneCapability: ({clip}) => {
    globalThis.rangeProbe.preparations++;
    return {identity: clip.id, frame: frame => {
      globalThis.rangeProbe.frames++;
      return support(clip, frame);
    }};
  },
});
"""


@pytest.fixture(scope="module")
def public_fold(tmp_path_factory):
    artifact, version = admitted_public_artifact("ASTRID_COMPOSITION_TEST_ARTIFACT")
    assert version == "0.0.10"
    peers = Path(os.environ.get("ASTRID_COMPOSITION_TEST_NODE_MODULES",
                                str(ROOT / "remotion/node_modules"))).resolve()
    assert peers.is_dir()
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok and node.version == "v20.19.4", node.problem
    project = tmp_path_factory.mktemp("motion-range-fold")
    modules = project / "node_modules"
    (modules / "@banodoco").mkdir(parents=True)
    package = modules / "@banodoco/timeline-composition"
    with tarfile.open(artifact) as archive:
        expected = {m.name.removeprefix("package/"):
                    hashlib.sha256(archive.extractfile(m).read()).hexdigest()
                    for m in archive.getmembers() if m.isfile()}
        archive.extractall(project, filter="data")
    (project / "package").rename(package)
    for peer in peers.iterdir():
        if peer.name != "@banodoco":
            (modules / peer.name).symlink_to(peer, target_is_directory=peer.is_dir())
    for name in ("native-scene.mjs", "webpack-alias.mjs"):
        shutil.copyfile(ROOT / "remotion" / name, project / name)
    src = project / "src"
    src.mkdir()
    for name in ("host-scene.ts", "host-registries.ts"):
        shutil.copyfile(ROOT / "remotion/src" / name, src / name)
    (src / "probe.tsx").write_text(COMPONENT)
    (src / "effects.generated.ts").write_text(
        "import Probe from './probe';\n"
        "export const EFFECT_REGISTRY = {'range-probe': Probe};\n"
        "export const CLIP_TYPE_ALIASES = {};\n")
    for kind in ("animations", "transitions"):
        prefix = kind[:-1].upper()
        (src / f"{kind}.generated.ts").write_text(
            "\n".join(f"export const {prefix}_{suffix} = {{}};"
                      for suffix in ("REGISTRY", "DEFAULTS", "META")))
    shutil.copyfile(Path(__file__).with_name("motion_range_fold.mjs"), project / "query.mjs")
    env = {k: v for k, v in os.environ.items() if k not in ("NODE_OPTIONS", "NODE_PATH")}
    # Resolve peers from both the host and the immutable package's own location.
    preflight = """
import {createRequire} from 'node:module';
import {realpathSync} from 'node:fs';
const host = createRequire(`${process.cwd()}/package.json`);
const library = createRequire(host.resolve('@banodoco/timeline-composition'));
const peers = ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils'];
console.log(JSON.stringify([host, library].map(require => Object.fromEntries(peers.map(name =>
  [name, {path: realpathSync(require.resolve(`${name}/package.json`)),
    version: require(`${name}/package.json`).version}])))));
"""
    resolved = json.loads(subprocess.check_output(
        [str(node.path), "--input-type=module", "-e", preflight], cwd=project,
        env=env, text=True, timeout=30))
    for graph in resolved:
        for name, peer in graph.items():
            assert Path(peer["path"]).is_relative_to(peers)
            assert peer["version"] == ("18.3.1" if name in ("react", "react-dom") else "4.0.509")

    def hashes():
        return {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in package.rglob("*") if p.is_file()}

    before = hashes()
    assert len(before) == 77 and before == expected

    def run(mode, **kwargs):
        return json.loads(subprocess.check_output(
            [str(node.path), "query.mjs"], cwd=project, env=env, text=True,
            input=json.dumps({"mode": mode, **kwargs}), timeout=30))

    try:
        yield run
        assert hashes() == before
    finally:
        shutil.rmtree(project)


@pytest.mark.integration
@pytest.mark.parametrize("mode", ["exact", "unknown", "invisible", "clock", "ranges",
                                 "preroll", "invalid-request"])
def test_exact_public_motion_fold(public_fold, mode):
    public_fold(mode)


@pytest.mark.integration
@pytest.mark.parametrize("invalid", ["nan", "infinity", "bool", "string", "null"])
def test_invalid_public_motion_is_unknown(public_fold, invalid):
    public_fold("invalid-fact", invalid=invalid)


@pytest.mark.integration
def test_bounded_fold_cost(public_fold):
    cost = public_fold("cost")
    assert cost["totalFrames"] == 3600
    assert cost["factPairs"] == 64
    print(f"motion fold cost: {json.dumps(cost, sort_keys=True)}")
