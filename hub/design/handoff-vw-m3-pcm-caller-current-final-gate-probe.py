import json
import struct

import pytest

from tests.packs.rendering.test_normal_audio_run import normal_profile, normal_scene, normal_run
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion


def test_retry_after_consumer_failure_gets_new_wav_and_attempt(normal_run):
    state = normal_run
    def fail():
        raise RuntimeError('reviewer consumer failure')
    state.consume = fail
    with pytest.raises(RuntimeError, match='reviewer consumer failure'):
        state.execute()
    first = list(state.paths)
    assert len(first) == 2 and all(not path.exists() for path in first)
    state.paths.clear()
    state.consume = lambda: None
    state.execute()
    assert len(state.paths) == 2
    assert set(first).isdisjoint(state.paths)
    assert all(not path.exists() for path in state.paths)
    assert state.events == ['server-enter', 'consume', 'server-exit'] * 2


def test_partial_preparation_failure_then_repaired_retry(normal_run):
    state = normal_run
    original = state.timeline_path.read_bytes()
    raw = json.loads(original)
    raw['clips'][1]['params']['fadeInCurve'] = 'reviewer-invalid'
    try:
        state.timeline_path.write_text(json.dumps(raw))
        with pytest.raises(RuntimeError, match='ENVELOPE_UNRENDERED'):
            state.execute()
    finally:
        state.timeline_path.write_bytes(original)
    assert state.events == ['server-enter', 'server-exit']
    assert not state.paths
    state.execute()
    assert len(state.paths) == 2 and all(not path.exists() for path in state.paths)
    assert state.events == ['server-enter', 'server-exit', 'server-enter', 'consume', 'server-exit']


def test_track_boost_and_clip_scalar_stay_out_of_pcm(normal_run, monkeypatch):
    state = normal_run
    serialize = remotion._serialize_timeline
    def boosted(*args, **kwargs):
        value = serialize(*args, **kwargs)
        value['tracks'][0]['volume'] = 2
        return value
    monkeypatch.setattr(remotion, '_serialize_timeline', boosted)
    def consume():
        props = state.props
        assert props['timeline']['tracks'][0]['volume'] == 2
        assert props['timeline']['clips'][0]['volume'] == 3
        assert struct.unpack_from('<ff', state.paths[0].read_bytes(), 44 + 30000 * 8) == (0.25, -0.125)
        assert props['timeline']['clips'][1]['volume'] == 0
        assert struct.unpack_from('<ff', state.paths[1].read_bytes(), 44 + 15000 * 8) == (0.25, -0.125)
    state.consume = consume
    state.execute()
