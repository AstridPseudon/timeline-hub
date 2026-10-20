"""Socket-free counterexample: native track filtering can shorten a layer clock."""
import hashlib
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

from astrid.core.rendering.contracts import FrameWindow, RenderProfile, RenderRequest, SCHEMA_VERSION
from astrid.core.rendering.service import RenderService
from astrid.core.timeline.banodoco_composer import Timeline
from astrid.packs.rendering.rendering.renderers.remotion.run import _native_window_argument

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    source = root / 'timeline.json'
    source.write_text(json.dumps({
        'tracks': [{'id': 'bottom', 'kind': 'visual', 'label': 'Bottom'},
                   {'id': 'top', 'kind': 'visual', 'label': 'Top'}],
        'clips': [{'id': 'plate', 'track': 'bottom', 'asset': 'plate', 'at': 0, 'hold': 10}],
    }))
    # Existing schema and file digest, with no producer label or source grant.
    validated = Timeline.load(source).for_render().to_json_data()
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    window = FrameWindow(150, 180, (30, 1))
    request = RenderRequest(SCHEMA_VERSION, str(source), 'out.mp4', window=window)
    segment = SimpleNamespace(window=window, layer=SimpleNamespace(tracks=('top',), z=1))
    profile = RenderProfile(320, 180, (30, 1), (1, 90000), 'h264', 'yuv420p')
    results = {'source_digest': digest, 'original_frames': _native_window_argument(window, validated, profile)}
    for native in (True, False):
        candidate = SimpleNamespace(id='fixture', manifest=SimpleNamespace(capabilities={'supports_windows': native}))
        adapted, hashes = RenderService._segment_request(
            object.__new__(RenderService), request, candidate=candidate,
            segment=segment, index=int(native), workspace=root,
        )
        materialized = Timeline.load(Path(adapted.timeline_path)).for_render().to_json_data()
        try:
            frames = _native_window_argument(adapted.window, materialized, profile)
        except ValueError as error:
            frames = str(error)
        results[str(native)] = {'window_retained': adapted.window is not None,
                                'clips': materialized['clips'], 'metadata': materialized['metadata'],
                                'frames_or_error': frames, 'hashes': hashes}
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
    assert results['True']['frames_or_error'] == 'Remotion window extends beyond the full composition'
    assert results['False']['window_retained'] is False
    assert results['False']['metadata']['duration_seconds'] == 1
    print(json.dumps(results, indent=2))
