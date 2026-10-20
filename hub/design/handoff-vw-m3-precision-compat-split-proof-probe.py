"""Private diagnostics only: actual normal runner + actual old render serializer."""
import copy
import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from astrid.core.rendering.service import RenderService
from astrid.core.rendering.contracts import FrameWindow
from astrid.core.timeline.banodoco_composer import TimelineRenderView
from astrid.core.timeline.duration import clip_start_frame, clip_end_frame
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion
from tests.packs.rendering import test_normal_audio_run as normal

BASE = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
TASK = BASE / 'workers/vw-m3-precision-compat-split-proof'
DATA = json.loads((BASE / 'design/handoff-vw-m3-precision-compat-split-proof-compiled.json').read_text())
spec = importlib.util.spec_from_file_location('astrid.core.timeline._prior_composer', TASK / 'current/astrid/core/timeline/banodoco_composer.py')
prior = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = prior
spec.loader.exec_module(prior)
normal_run = normal.normal_run
ROWS = []


@pytest.fixture(scope='session', autouse=True)
def save_rows():
    yield
    (BASE / 'design/handoff-vw-m3-precision-compat-split-proof-vectors.json').write_text(json.dumps(ROWS, indent=2) + '\n')


@pytest.fixture(params=['candidate-precise', 'compat-serialized'], autouse=True)
def policy(request, monkeypatch):
    monkeypatch.setattr(normal, '_timeline', lambda: copy.deepcopy(DATA['config']))
    if request.param == 'compat-serialized':
        # Exact current M2 source method, no replacement timing arithmetic.
        monkeypatch.setattr(TimelineRenderView, 'to_json_data', prior.TimelineRenderView.to_json_data)
    return request.param


def test_actual_normal_full_window_layer_retains_final_serialized_original(normal_run, policy, request):
    state = normal_run
    registry = json.loads(state.registry.read_text())
    registry['assets']['occ-1:voice'] = copy.deepcopy(registry['assets']['sound'])
    state.registry.write_text(json.dumps(registry))
    serialized = remotion._serialize_timeline(state.timeline_path)
    expected = next(c for c in serialized['clips'] if c['id'] == 'occ-1:voice-1')
    serialized_before = copy.deepcopy(serialized)

    def consume():
        actual = next(c for c in state.props['timeline']['clips'] if c['id'] == expected['id'])
        without_audio = copy.deepcopy(actual)
        without_audio.pop('audio')
        assert without_audio == expected
        assert actual['volume'] == 1.5  # occurrence gain applied by M2, not raw child 3
        assert actual['speed'] == 1.5
        assert actual['at'] == (0.017 if policy == 'compat-serialized' else 0.016682)
        prepared = actual['audio']['render_source']
        wav_path = state.server.root / prepared['file'].removeprefix('http://attempt.invalid/')
        sliced = next(c for c in RenderService._window_timeline(serialized, FrameWindow(15, 45, (30000, 1001)), tracks=('A1',))['clips']
                      if c['id'] == expected['id'] + '_15_45')
        source = state.server.root / state.props['assets']['assets'][expected['asset']]['file'].removeprefix('http://attempt.invalid/')
        with tempfile.TemporaryDirectory(prefix='slice-probe-', dir=TASK) as slice_directory:
          result = subprocess.run(
            [os.environ['ASTRID_NODE_EXECUTABLE'], str(TASK / 'audio-project/compare.mjs')],
            input=json.dumps({'clip': expected, 'rawChild': DATA['raw_child'], 'prepared': prepared,
                              'fps': 30000 / 1001, 'path': str(wav_path), 'source': str(source),
                              'sliced': sliced, 'sliceDirectory': slice_directory}),
            text=True, capture_output=True, check=False,
        )
        assert result.returncode == 0, result.stderr
        row = json.loads(result.stdout)
        row['start'] = clip_start_frame(expected, 30000 / 1001)
        row['duration'] = clip_end_frame(expected, 30000 / 1001) - row['start']
        assert row['start'] == (1 if policy == 'compat-serialized' else 0)
        assert row['clock'] == {'source_from': 2 / (30000 / 1001), 'playback_rate': 1.5}
        assert row['duration'] == 35
        row.update(route=request.node.callspec.params['normal_run'], policy=policy)
        ROWS.append(row)
        assert serialized == serialized_before

    state.consume = consume
    state.execute()
    assert state.events == ['server-enter', 'consume', 'server-exit']
    assert all(not p.exists() for p in state.paths)
