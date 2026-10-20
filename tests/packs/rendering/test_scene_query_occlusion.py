"""D1 occlusion queries consume serialized public SceneFrame answers only."""

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering import remotion_runtime
from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.timeline import scene_answers

ROOT = Path(__file__).resolve().parents[3]
PUBLIC_ARTIFACT_ENV = "ASTRID_TEST_PUBLIC_ARTIFACT"
PUBLIC_ARTIFACT = ROOT / "remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz"
PUBLIC_SHA256 = "cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7"
_ADMITTED_RELEASES = {
    "0.0.9": "fa94f9c6438278764fad1285fa3d76063020ea7b20f4018de6bec4ffff0c9f61",
    "0.0.10": PUBLIC_SHA256,
}


def admitted_public_artifact(env_name: str = PUBLIC_ARTIFACT_ENV) -> tuple[Path, str]:
    """Return the default public10 artifact or an explicitly admitted public9 override."""
    artifact = Path(os.environ.get(env_name, PUBLIC_ARTIFACT))
    assert artifact.is_file(), f"required public artifact is missing: {artifact}"
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    version = next((version for version, expected in _ADMITTED_RELEASES.items()
                    if expected == digest), None)
    assert version is not None, f"public artifact is not admitted: {artifact} ({digest})"
    with tarfile.open(artifact) as archive:
        manifest_file = archive.extractfile("package/package.json")
        assert manifest_file is not None, f"public artifact has no package manifest: {artifact}"
        manifest = json.load(manifest_file)
    assert manifest.get("version") == version
    return artifact, version


def admitted_public_evaluation(env_name: str = "ASTRID_TEST_SCENE_EVALUATION") -> Path:
    """Validate an installed public evaluation against the selected release tarball."""
    artifact, version = admitted_public_artifact("ASTRID_COMPOSITION_TEST_ARTIFACT")
    evaluation = Path(os.environ.get(env_name, str(
        ROOT / "remotion/node_modules/@banodoco/timeline-composition/dist/evaluation.js")))
    package = evaluation.parent.parent
    assert json.loads((package / "package.json").read_text())["version"] == version
    with tarfile.open(artifact) as archive:
        expected = {
            name.removeprefix("package/"): hashlib.sha256(archive.extractfile(name).read()).hexdigest()
            for name in archive.getnames()
            if name.startswith("package/") and not name.endswith("/")
        }
    actual = {str(path.relative_to(package)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in package.rglob("*") if path.is_file()}
    assert len(expected) == len(actual) == 77
    assert actual == expected
    return evaluation


def _stage_artifact(root: Path, artifact: Path) -> Path:
    package = root / "node_modules/@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(artifact) as archive:
        archive.extractall(root, filter="data")
    (root / "package").rename(package)
    (root / "package.json").write_text('{"type":"module"}')
    shutil.copyfile(ROOT / "remotion/scene-query.mjs", root / "scene-query.mjs")
    return package


@pytest.fixture
def installed(tmp_path, monkeypatch):
    for key in ("PYTHONPYCACHEPREFIX", "NODE_OPTIONS", "NODE_PATH"):
        monkeypatch.delenv(key, raising=False)
    artifact, _version = admitted_public_artifact()
    toolchain = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert toolchain.ok, toolchain.problem
    assert toolchain.version == "v20.19.4"
    package = _stage_artifact(tmp_path, artifact)
    before = {str(path.relative_to(package)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in package.rglob("*") if path.is_file()}
    assert len(before) == 77
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        remotion_runtime.RemotionRuntimeStatus(
                            True, tmp_path, node_executable=Path(toolchain.path), node_version="v20.19.4"))
    yield tmp_path, Path(toolchain.path)
    after = {str(path.relative_to(package)): hashlib.sha256(path.read_bytes()).hexdigest()
             for path in package.rglob("*") if path.is_file()}
    assert len(after) == 77
    assert after == before
    _artifact, _version = admitted_public_artifact()


def _public_scene_frames(project: Path, node: Path) -> list[dict]:
    script = r'''
import {prepareScene, querySceneFrame} from '@banodoco/timeline-composition/evaluation';

const frames = [
  {frame: 0, layers: [['target', 'target'], ['front', 'front95']]},
  {frame: 1, layers: [['target-order', 'target'], ['back', 'full'], ['front-order', 'front95']]},
  {frame: 2, layers: [['target-transparent', 'target'], ['transparent', 'transparent']]},
  {frame: 3, layers: [['target-unknown', 'target'], ['unknown', 'unknown']]},
  {frame: 4, layers: [['offscreen', 'offscreen'], ['front-offscreen', 'full']]},
  {frame: 5, layers: [['absent', 'absent']]},
];
const support = (kind) => {
  const rects = {
    target: {x: 0, y: 0, width: 100, height: 100},
    front95: {x: 0, y: 0, width: 95, height: 100},
    full: {x: 0, y: 0, width: 100, height: 100},
    offscreen: {x: 100, y: 0, width: 10, height: 100},
  };
  if (kind === 'unknown') return {presence: 'present', opaqueSupport: 'unknown',
    bounds: {status: 'unknown', reason: 'registered unknown geometry'}};
  if (kind === 'transparent') return {presence: 'present', opaqueSupport: 'none',
    bounds: {status: 'known', rect: rects.full}};
  if (kind === 'absent') return {presence: 'absent', opaqueSupport: 'none',
    bounds: {status: 'known', rect: rects.full}};
  return {presence: 'present', opaqueSupport: 'rect', bounds: {status: 'known', rect: rects[kind]}};
};
const result = frames.map(({frame, layers}) => {
  const clips = layers.map(([id, kind]) => ({id, at: frame / 30, hold: 1, track: 'v1', clipType: 'registered',
    params: {kind}}));
  const capabilities = {components: Object.fromEntries(clips.map(clip => [clip.id, {
    identity: `${clip.id}:${clip.params.kind}`, frame: () => support(clip.params.kind),
  }]))};
  const prepared = prepareScene([{track: {id: 'v1', kind: 'visual', label: 'Video'}, clips,
    transitions: Array(Math.max(0, clips.length - 1)).fill(null)}], {assets: {}}, 30, 100, 100,
    {elements: new Set(['registered']), capabilities, roles: Object.fromEntries(clips.map(clip => [clip.id, 'content']))});
  return querySceneFrame(prepared, frame);
});
console.log(JSON.stringify(result));
'''
    result = subprocess.run([str(node), "--input-type=module", "-e", script], cwd=project,
                            check=True, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)


def test_occlusions_use_actual_public_frames_and_preserve_target_order(installed, monkeypatch):
    project, node = installed
    answers = _public_scene_frames(project, node)
    targets = [
        {"frame": 0, "clip_id": "target", "min_fraction": .90},
        {"frame": 0, "clip_id": "target", "min_fraction": .98},
        {"frame": 1, "clip_id": "target-order", "min_fraction": .90},
        {"frame": 2, "clip_id": "target-transparent", "min_fraction": .90},
        {"frame": 3, "clip_id": "target-unknown", "min_fraction": .90},
        {"frame": 4, "clip_id": "offscreen", "min_fraction": .90},
        {"frame": 5, "clip_id": "absent", "min_fraction": .90},
        {"frame": 0, "clip_id": "front", "min_fraction": .90},
        {"frame": 999, "clip_id": "missing", "min_fraction": .90},
    ]
    calls = []
    real_run = scene_answers.subprocess.run

    def capture(*args, **kwargs):
        calls.append(json.loads(kwargs["input"]))
        return real_run(*args, **kwargs)

    monkeypatch.setattr(scene_answers.subprocess, "run", capture)
    assert scene_answers.occlusions_from_frames(answers, targets) == [
        {"status": "known", "occluderId": "front", "fraction": .95},
        {"status": "known", "occluderId": None, "fraction": 0},
        {"status": "known", "occluderId": "front-order", "fraction": .95},
        {"status": "unknown", "reason": "Upper layer support or alpha is undeclared"},
        {"status": "unknown", "reason": "Upper layer support or alpha is undeclared"},
        {"status": "known", "occluderId": None, "fraction": 0},
        {"status": "known", "occluderId": None, "fraction": 0},
        {"status": "known", "occluderId": None, "fraction": 0},
        {"status": "unavailable", "reason": "SceneFrame for frame 999 is unavailable"},
    ]
    assert calls == [{"query": "occlusion", "answers": answers, "targets": targets}]


@pytest.mark.parametrize(
    ("answers", "targets", "message"),
    [
        ([{"frame": 0}, {"frame": 0}], [{"frame": 0, "clip_id": "x", "min_fraction": .9}],
         "duplicate occlusion answer frame"),
        ([{"frame": 0}], [{"frame": True, "clip_id": "x", "min_fraction": .9}],
         "target frame"),
        ([{"frame": 0}], [{"frame": 0, "clip_id": "", "min_fraction": .9}], "clip_id"),
        ([{"frame": 0}], [{"frame": 0, "clip_id": "x", "min_fraction": float("nan")}],
         "min_fraction"),
        ([{"frame": 0}], [
            {"frame": 0, "clip_id": "x", "min_fraction": .9},
            {"frame": 0, "clip_id": "x", "min_fraction": .9},
        ], "duplicate occlusion target"),
    ],
)
def test_occlusion_protocol_validation_is_explicit(installed, answers, targets, message):
    with pytest.raises(scene_answers.SceneQueryUnavailable, match=message):
        scene_answers.occlusions_from_frames(answers, targets)


def test_occlusion_response_cardinality_is_not_unique_frame_count(installed, monkeypatch):
    answers = [{"frame": 0, "layers": [], "width": 1, "height": 1}]
    targets = [
        {"frame": 0, "clip_id": "a", "min_fraction": .90},
        {"frame": 0, "clip_id": "b", "min_fraction": .98},
    ]
    calls = []
    real_run = scene_answers.subprocess.run

    def capture(*args, **kwargs):
        calls.append(json.loads(kwargs["input"]))
        return SimpleNamespace(returncode=0, stdout=json.dumps([{
            "status": "known", "occluderId": None, "fraction": 0}, {
            "status": "unknown", "reason": "fixture",
        }]), stderr="")

    monkeypatch.setattr(scene_answers.subprocess, "run", capture)
    result = scene_answers.occlusions_from_frames(answers, targets)
    monkeypatch.setattr(scene_answers.subprocess, "run", real_run)
    assert len(result) == 2
    assert calls == [{"query": "occlusion", "answers": answers, "targets": targets}]


@pytest.mark.parametrize("response", [[], [None]])
def test_malformed_occlusion_response_is_unavailable(installed, monkeypatch, response):
    monkeypatch.setattr(scene_answers.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(returncode=0, stdout=json.dumps(response), stderr=""))
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="invalid scene query response"):
        scene_answers.occlusions_from_frames(
            [{"frame": 0, "layers": [], "width": 1, "height": 1}],
            [{"frame": 0, "clip_id": "target", "min_fraction": .90}],
        )


def test_old_public_export_is_unavailable_for_occlusion(installed, tmp_path, monkeypatch):
    _, node = installed
    old_project = tmp_path / "old"
    old_project.mkdir()
    old_package = ROOT / "remotion/artifacts/banodoco-timeline-composition-0.0.8.tgz"
    _stage_artifact(old_project, old_package)
    monkeypatch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                        remotion_runtime.RemotionRuntimeStatus(
                            True, old_project, node_executable=node, node_version="v20.19.4"))
    with pytest.raises(scene_answers.SceneQueryUnavailable, match="scene evaluation unavailable"):
        scene_answers.occlusions_from_frames(
            [{"frame": 0, "layers": [], "width": 1, "height": 1}],
            [{"frame": 0, "clip_id": "missing", "min_fraction": .90}],
        )
