"""Actual Three.js component source props, compared with the retained legacy route."""
import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering.service import RenderService
from astrid.packs.rendering.rendering.renderers.threejs import run as threejs
from tests.packs.rendering.test_live_scene_boundary import _package
from tests.packs.rendering.test_live_scene_composition import _composition, _request

PROBE = Path(__file__).with_suffix('.cjs')
SOURCE = Path(os.environ['REVIEW_SOURCE_ROOT']) / 'remotion/src/ThreeTimelineComposition.tsx'
PREFIX = Path(__file__).with_name('handoff-vw-m3-current-extent-fixture-final-gate')
PHASE = Path(os.environ['REVIEW_SOURCE_ROOT']).name

@pytest.mark.parametrize('z', [0, 1])
def test_final_three_source_props_match_legacy(tmp_path, monkeypatch, z):
    package = _package()
    raw = _composition(package)
    raw['clips'][0]['hold'] = 20
    raw['clips'][0]['app']['opaque'] = {'keep': [None, False, {'raw': 'unchanged'}]}
    path = tmp_path / 'source.json'
    path.write_text(json.dumps(raw))
    original = path.read_bytes()
    request = _request(path)
    monkeypatch.setattr(threejs, '_default_settings', lambda: threejs._ThreeSettings(tmp_path, None, None))
    monkeypatch.setattr(threejs, '_threejs_project_reasons', lambda *args: [])
    monkeypatch.setattr(threejs, '_binaries_reasons', lambda: [])
    captured = []
    class Observed(Exception):
        pass
    def capture(timeline_path, assets_path, output_path, **kwargs):
        payload = json.loads(timeline_path.read_text())
        scene = payload['clips'][0]
        assert (scene['at'], scene['from'], scene['to'], scene['speed'], scene['hold']) == (0, 63, 65, 2, 2)
        assert scene['app'] == raw['clips'][0]['app']
        assert output_path.suffix == ('.mov' if z else '.mp4')
        result = subprocess.run(['/tmp/vw-m3-agent-gate-node20.19.4/bin/node', str(PROBE), str(SOURCE), str(timeline_path)], capture_output=True, text=True, check=True)
        observations = json.loads(result.stdout)
        for observed in observations[:30]:
            assert len(observed['sources']) == 1
            assert observed['sources'][0]['source'] == package
            assert observed['backgrounds'] == ['transparent' if z else '#050814']
        assert observations[0]['sources'][0]['sourceTime'] == 63
        assert observations[29]['sources'][0]['sourceTime'] < 65
        assert observations[30]['sources'] == []
        captured.append((payload, observations))
        raise Observed()
    monkeypatch.setattr(threejs, '_execute_remotion', capture)
    for index, native in enumerate((True, False)):
        adapted, _ = RenderService._segment_request(object.__new__(RenderService), request,
            candidate=SimpleNamespace(manifest=SimpleNamespace(capabilities={'supports_windows': native})),
            segment=SimpleNamespace(window=request.window, layer=SimpleNamespace(tracks=('scene',), z=z)),
            index=index, workspace=tmp_path)
        with pytest.raises(Observed):
            threejs._protocol_render(adapted, workspace=tmp_path)
    assert captured[0] == captured[1]
    assert path.read_bytes() == original
    evidence = Path(str(PREFIX) + '-' + PHASE + '-three-payload-' + str(z) + '.json')
    evidence.write_text(json.dumps(captured[0], indent=2) + '\n')
    if PHASE == 'candidate':
        baseline = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-extent-landable-review-baseline-three-payload-' + str(z) + '.json')
        assert captured[0] == tuple(json.loads(baseline.read_text()))
