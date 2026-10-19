"""Native preparation needs the render's asset and theme inputs, beyond its config.

These probes exercise the installed public API; they do not qualify the current
check/label consumers, which do not yet pass these inputs through.
"""

import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

from astrid.core.rendering.node_pin import resolve_pinned_node

ROOT = Path(__file__).resolve().parents[3]
REMOTION = ROOT / "remotion"
PACKAGE = REMOTION / "node_modules/@banodoco/timeline-composition"
SHA256 = "93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa"


@pytest.fixture
def native_scene():
    if not PACKAGE.is_dir():
        pytest.skip("requires the host's locked npm install")
    toolchain = resolve_pinned_node(
        REMOTION, override=os.environ.get("ASTRID_NODE_EXECUTABLE"))
    if not toolchain.ok:
        pytest.skip(toolchain.problem)
    assert toolchain.version == "v20.19.4"
    assert hashlib.sha256((REMOTION / "artifacts/banodoco-timeline-composition-0.0.8.tgz")
                          .read_bytes()).hexdigest() == SHA256
    assert json.loads((PACKAGE / "package.json").read_text())["version"] == "0.0.8"
    before = {str(path.relative_to(PACKAGE)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in PACKAGE.rglob("*") if path.is_file()}

    def run(script):
        result = subprocess.run(
            [str(toolchain.path), "--input-type=module", "-e", script], cwd=REMOTION,
            check=True, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout)

    yield run
    assert before == {str(path.relative_to(PACKAGE)): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in PACKAGE.rglob("*") if path.is_file()}


@pytest.mark.integration
def test_identical_config_requires_exact_asset_closure_for_scene_bounds(native_scene):
    answers = native_scene("""
import {prepareCompositionScene, querySceneFrame, toRuntimeTheme, DEFAULT_THEME}
  from '@banodoco/timeline-composition';
const track = {id: 'plate', kind: 'visual', fit: 'contain'};
const clip = {id: 'exact:picture', clipType: 'image', track: 'plate', asset: 'picture',
  at: 0, hold: 1};
const tracks = [{track, clips: [clip]}];
const query = assets => querySceneFrame(prepareCompositionScene(tracks, assets,
  30000 / 1001, toRuntimeTheme(DEFAULT_THEME), 200, 100), 0);
const answers = ['100x200', '200x100'].map(resolution => query({assets: {
  picture: {file: 'picture.png', type: 'image', resolution},
}}));
answers.push(query({assets: {}}));
console.log(JSON.stringify(answers));
""")
    portrait, landscape, unresolved = [answer["layers"][0] for answer in answers]
    assert portrait["bounds"] == {"status": "known", "rect": {
        "x": 75, "y": 0, "width": 50, "height": 100}}
    assert landscape["bounds"] == {"status": "known", "rect": {
        "x": 0, "y": 0, "width": 200, "height": 100}}
    assert unresolved["bounds"]["status"] == "unknown"
    # Asset metadata alone proves neither alpha nor visibility.
    assert all(answer["coverage"] == "UNKNOWN" for answer in answers)
    assert all(answer["layers"][0]["opacity"] is None for answer in answers)


@pytest.mark.integration
def test_runtime_theme_selects_public_registry_independently_of_config_slug(native_scene):
    selections = native_scene("""
import {prepareCompositionScene, toRuntimeTheme, DEFAULT_THEME}
  from '@banodoco/timeline-composition';
const clip = {id: 'exact:card', clipType: 'art-card', at: 0, hold: 1, track: 'plate'};
const tracks = [{track: {id: 'plate', kind: 'visual'}, clips: [clip]}];
console.log(JSON.stringify(['banodoco-default', '2rp'].map(id => {
  const scene = prepareCompositionScene(tracks, {assets: {}}, 30,
    toRuntimeTheme({...DEFAULT_THEME, id}), 1920, 1080);
  return {id, admitted: scene.elements.has('art-card')};
})));
""")
    assert selections == [{"id": "banodoco-default", "admitted": False},
                          {"id": "2rp", "admitted": True}]
