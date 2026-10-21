"""Dormant D09 same-film replacement; requires the qualified public14 host."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path
from unittest.mock import patch

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node
from scripts import gen_effect_registry

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.integration


def _independent_fades_timeline():
    return {
        "tracks": [
            {"id": "fx", "kind": "visual"},
            {"id": "type", "kind": "visual"},
            {"id": "sprite", "kind": "visual"},
            {"id": "plate", "kind": "visual"},
        ],
        "clips": [
            {"id": "out", "track": "plate", "clipType": "am-snap-plate",
             "at": 0.0, "hold": 1.0, "params": {"src": "/plate.png"},
             "app": {"astrid": {"cut": "c01", "layer": "l"}},
             "effects": {"fade_out": 0.5}},
            {"id": "in", "track": "fx", "clipType": "am-footage",
             "at": 0.5, "hold": 1.0, "params": {"src": "/footage.png"},
             "app": {"astrid": {"cut": "c01", "layer": "l"}},
             "effects": {"fade_in": 0.5}},
        ],
    }


@pytest.fixture(scope="module")
def d09_public_query(tmp_path_factory):
    """Stage public14 and current Agent resources entirely in private tmp space."""
    artifact = Path(os.environ["ASTRID_COMPOSITION_TEST_ARTIFACT"])
    peers = Path(os.environ["ASTRID_COMPOSITION_TEST_NODE_MODULES"]).resolve()
    assert artifact.is_file()
    assert peers.is_dir()
    node = resolve_pinned_node(ROOT / "remotion", override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    assert node.ok and node.version == "v20.19.4"
    project_root = tmp_path_factory.mktemp("d09-same-film-public")
    project = project_root / "remotion"
    (project / "src").mkdir(parents=True)
    (project_root / "astrid").symlink_to(ROOT / "astrid", target_is_directory=True)
    modules = project / "node_modules"
    package = modules / "@banodoco/timeline-composition"
    package.parent.mkdir(parents=True)
    with tarfile.open(artifact) as archive:
        archive.extractall(project, filter="data")
    (project / "package").rename(package)
    assert json.loads((package / "package.json").read_text())["version"] == "0.0.14"
    for peer in peers.iterdir():
        if peer.name != "@banodoco":
            (modules / peer.name).symlink_to(peer, target_is_directory=peer.is_dir())
    for name in ("package.json", "webpack-alias.mjs", "native-scene.mjs", "scene-query.mjs"):
        shutil.copyfile(ROOT / "remotion" / name, project / name)
    for name in ("host-scene.ts", "host-registries.ts"):
        shutil.copyfile(ROOT / "remotion" / "src" / name, project / "src" / name)
    with patch.dict(os.environ, {"ASTRID_REMOTION_PROJECT_DIR": str(project)}):
        for kind in ("effects", "animations", "transitions"):
            (project / "src" / f"{kind}.generated.ts").write_text(
                gen_effect_registry.generate_element_registry(kind), encoding="utf-8")
    shutil.copyfile(Path(__file__).with_name("d09_same_film_public.mjs"), project / "query.mjs")
    env = {key: value for key, value in os.environ.items() if key not in ("NODE_OPTIONS", "NODE_PATH")}

    def query(name, *, timeline=None):
        args = [str(node.path), "query.mjs", name]
        result = subprocess.run(
            args,
            input=json.dumps(timeline) if timeline is not None else None,
            cwd=project,
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        return json.loads(result.stdout)

    try:
        yield query
    finally:
        shutil.rmtree(project_root)


def test_same_film_independent_fades_are_public_dip(d09_public_query):
    result = d09_public_query("legacy-crossfade", timeline=_independent_fades_timeline())
    assert result["props"]["timeline"] == _independent_fades_timeline()
    assert result["compiled"] is False
    assert [(row["coverage"], row["content"]) for row in result["answers"]] == (
        [("COVERED", "CONTENT")] * 16
        + [("DIP", None)] * 14
        + [("COVERED", "CONTENT")] * 15
    )
    assert [layer["opacity"] for layer in result["answers"][15]["layers"]] == [1, 0]
    for frame in range(16, 30):
        assert [layer["clipId"] for layer in result["answers"][frame]["layers"]] == ["out", "in"]
        assert all(0 < layer["opacity"] < 1 for layer in result["answers"][frame]["layers"])
    assert [layer["clipId"] for layer in result["answers"][30]["layers"]] == ["in"]
    assert result["answers"][30]["layers"][0]["opacity"] == 1
    assert result["after"]["layers"] == [] and result["after"]["coverage"] == "GAP"


def test_same_film_incoming_transition_remains_covered(d09_public_query):
    result = d09_public_query("incoming-crossfade")
    assert [(row["coverage"], row["content"]) for row in result["answers"]] == [
        ("COVERED", "CONTENT") for _ in range(60)
    ]
    assert result["compiled"] is True
    overlap = result["answers"][22]
    assert [layer["clipId"] for layer in overlap["layers"]] == ["out", "in"]
    assert overlap["layers"][0]["opacity"] == 1
    assert overlap["layers"][1]["opacity"] == pytest.approx(0.4666666666666667)
    assert result["after"]["layers"] == [] and result["after"]["coverage"] == "GAP"
