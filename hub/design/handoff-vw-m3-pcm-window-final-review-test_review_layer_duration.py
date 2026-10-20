import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.rendering.contracts import FrameWindow, RenderProfile, RenderRequest, SCHEMA_VERSION
from astrid.core.rendering.service import RenderService
from astrid.core.timeline.banodoco_composer import Timeline
from astrid.packs.rendering.rendering.renderers.remotion.run import _native_window_argument


@pytest.mark.parametrize('early_clip', [False, True], ids=['empty-layer', 'layer-ended-before-window'])
def test_valid_original_window_remains_renderable_after_layer_filter(tmp_path, early_clip):
    raw = {
        'tracks': [{'id': 'bottom', 'kind': 'visual', 'label': 'Bottom'},
                   {'id': 'top', 'kind': 'visual', 'label': 'Top'}],
        'clips': [{'id': 'plate', 'track': 'bottom', 'asset': 'plate', 'at': 0, 'from': 0, 'to': 10}],
    }
    if early_clip:
        raw['clips'].append({'id': 'early', 'track': 'top', 'asset': 'overlay', 'at': 0, 'from': 0, 'to': 2})
    source = tmp_path / 'timeline.json'
    source.write_text(json.dumps(raw))
    window = FrameWindow(150, 180, (30, 1))
    request = RenderRequest(SCHEMA_VERSION, str(source), 'out.mp4', window=window)
    segment = SimpleNamespace(window=window, layer=SimpleNamespace(tracks=('top',), z=1))
    profile = RenderProfile(320, 180, (30, 1), (1, 90000), 'h264', 'yuv420p')
    original = Timeline.load(source).for_render().to_json_data()
    assert _native_window_argument(window, original, profile) == '--frames=150-179'
    # The existing non-window backend retains an explicit one-second fill span.
    legacy, _ = RenderService._segment_request(
        object.__new__(RenderService), request,
        candidate=SimpleNamespace(id='legacy', manifest=SimpleNamespace(capabilities={'supports_windows': False})),
        segment=segment, index=0, workspace=tmp_path,
    )
    assert legacy.window is None
    assert json.loads(Path(legacy.timeline_path).read_text())['metadata']['duration_seconds'] == 1
    native, _ = RenderService._segment_request(
        object.__new__(RenderService), request,
        candidate=SimpleNamespace(id='native', manifest=SimpleNamespace(capabilities={'supports_windows': True})),
        segment=segment, index=1, workspace=tmp_path,
    )
    filtered = Timeline.load(Path(native.timeline_path)).for_render().to_json_data()
    assert native.window is window
    # Keep the intended behavior as a failing executable counterexample.
    assert _native_window_argument(native.window, filtered, profile) == '--frames=150-179'
