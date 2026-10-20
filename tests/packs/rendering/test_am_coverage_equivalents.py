"""Real AM drawing and public scene answers; no media-alpha or pixel claim.

These exercise the supported incoming transition representation and the exact
legacy independent-fades film against the selected public artifact. MAIN's
locked 0.0.6 renderer has not qualified this candidate golden.
"""
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from astrid.core.rendering.remotion_runtime import RemotionRuntimeStatus
from astrid.core.timeline import scene_answers
from scripts import gen_effect_registry
from tests.core.timeline.test_onscreen_more import _independent_fades_config

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = {
    "0.0.9": "fa94f9c6438278764fad1285fa3d76063020ea7b20f4018de6bec4ffff0c9f61",
    "0.0.10": "cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7",
}
# Like the neighboring public-package tests, this lane needs the release
# artifact and locked peers; production consumer pins remain unchanged.
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def am_coverage_query(tmp_path_factory):
    artifact = Path(os.environ.get("ASTRID_COMPOSITION_TEST_ARTIFACT", str(
        ROOT / "remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz")))
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() in ARTIFACTS.values()
    peers = Path(os.environ.get("ASTRID_COMPOSITION_TEST_NODE_MODULES", str(
        ROOT / "remotion/node_modules"))).resolve()
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok, node.problem
    project_root = tmp_path_factory.mktemp("am-coverage")
    project = project_root / "remotion"
    source = project / "src"
    source.mkdir(parents=True)
    (project_root / "astrid").symlink_to(ROOT / "astrid", target_is_directory=True)
    modules = project / "node_modules"
    package = modules / "@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(artifact) as archive:
        archive.extractall(project, filter="data")
    (project / "package").rename(package)
    version = json.loads((package / "package.json").read_text())["version"]
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == ARTIFACTS[version]
    for peer in peers.iterdir():
        if peer.name != "@banodoco":
            (modules / peer.name).symlink_to(peer, target_is_directory=peer.is_dir())
    for name in ("package.json", "webpack-alias.mjs", "native-scene.mjs", "scene-query.mjs"):
        shutil.copyfile(ROOT / "remotion" / name, project / name)
    for name in ("host-scene.ts", "host-registries.ts"):
        shutil.copyfile(ROOT / "remotion/src" / name, source / name)
    # Normal discovered pack maps: no fixture components under AM names.
    for kind in ("effects", "animations", "transitions"):
        (source / f"{kind}.generated.ts").write_text(gen_effect_registry.generate_element_registry(kind))
    shutil.copyfile(Path(__file__).with_name("am_coverage_equivalents.mjs"), project / "query.mjs")

    def hashes():
        return {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in package.rglob("*") if p.is_file()}

    before = hashes()
    assert len(before) == 77
    peer_identity = {p.name: p.resolve() for p in modules.iterdir() if p.name != "@banodoco"}
    env = {k: v for k, v in os.environ.items() if k not in ("NODE_OPTIONS", "NODE_PATH")}

    def query(case, *, timeline=None):
        args = [str(node.path), "query.mjs", case]
        if timeline is not None:
            args.append("--timeline-stdin")
        result = subprocess.run(args, input=json.dumps(timeline) if timeline is not None else None,
                                cwd=project, env=env,
                                text=True, capture_output=True, timeout=60)
        assert result.returncode == 0, result.stdout + result.stderr
        return json.loads(result.stdout)

    def coverage(result):
        # As in native_host, replace availability only. The actual Python
        # adapter invokes the staged native host and real public package.
        with pytest.MonkeyPatch.context() as patch:
            for key in ("NODE_OPTIONS", "NODE_PATH", "PYTHONPYCACHEPREFIX"):
                patch.delenv(key, raising=False)
            patch.setattr(scene_answers, "remotion_runtime_status", lambda **kwargs:
                          RemotionRuntimeStatus(True, project, node_executable=node.path))
            return scene_answers.coverage(result["props"], result["basis"],
                                          start_frame=0, end_frame=len(result["answers"]))

    query.coverage = coverage
    try:
        yield query
        assert hashes() == before
        assert {p.name: p.resolve() for p in modules.iterdir() if p.name != "@banodoco"} == peer_identity
    finally:
        shutil.rmtree(project_root)


def test_actual_am_public_incoming_crossfade_stays_covered(am_coverage_query):
    result = am_coverage_query("incoming-crossfade")
    assert [(row["frame"], row["coverage"], row["content"]) for row in result["answers"]] == [
        (frame, "COVERED", "CONTENT") for frame in range(60)]
    assert result["after"]["layers"] == [] and result["after"]["coverage"] == "GAP"
    assert result["compiled"] is True
    overlap = result["answers"][22]
    assert [layer["clipId"] for layer in overlap["layers"]] == ["out", "in"]
    assert overlap["layers"][0]["opacity"] == 1
    assert 0 < overlap["layers"][1]["opacity"] < 1


def test_actual_am_legacy_independent_fades_have_a_public_artifact_dip(am_coverage_query):
    config = _independent_fades_config()
    result = am_coverage_query("legacy-crossfade", timeline=config)
    assert result["props"]["timeline"] == config
    assert result["compiled"] is False
    assert [(row["coverage"], row["content"]) for row in result["answers"]] == (
        [("COVERED", "CONTENT")] * 16 + [("DIP", None)] * 14 + [("COVERED", "CONTENT")] * 15)
    spans = am_coverage_query.coverage(result)
    assert [(s.start_frame, s.end_frame, s.cls, s.content) for s in spans] == [
        (0, 16, "COVERED", "CONTENT"),
        (16, 30, "DIP", None),
        (30, 45, "COVERED", "CONTENT"),
    ]
    assert [layer["opacity"] for layer in result["answers"][15]["layers"]] == [1, 0]
    for frame in range(16, 30):
        assert [layer["clipId"] for layer in result["answers"][frame]["layers"]] == ["out", "in"]
        assert all(0 < layer["opacity"] < 1 for layer in result["answers"][frame]["layers"])
    assert [layer["clipId"] for layer in result["answers"][30]["layers"]] == ["in"]
    assert result["answers"][30]["layers"][0]["opacity"] == 1
    assert result["after"]["layers"] == [] and result["after"]["coverage"] == "GAP"


def test_actual_am_one_sided_fade_has_dip_frames_then_coverage(am_coverage_query):
    result = am_coverage_query("one-sided-fade")
    assert [row["coverage"] for row in result["answers"]] == ["DIP"] * 15 + ["COVERED"] * 45
    assert [row["content"] for row in result["answers"]] == [None] * 15 + ["CONTENT"] * 45
    assert result["answers"][0]["layers"][0]["opacity"] == 0
    assert result["answers"][0]["layers"][0]["visible"] is False
    assert result["after"]["layers"] == [] and result["after"]["coverage"] == "GAP"
