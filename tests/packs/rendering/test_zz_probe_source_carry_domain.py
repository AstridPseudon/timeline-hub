"""Temporary probe: raw vs compiled domain for the slicer. Deleted before report."""

from astrid.core.rendering.contracts import FrameWindow as Window
from astrid.core.rendering.service import RenderService
from astrid.core.timeline.banodoco_composer import Timeline


def _attempt(fn):
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001
        return f"ERR {type(exc).__name__}: {exc}"


def test_probe_domains():
    raw = {
        "tracks": [{"id": "A1", "kind": "audio", "label": "A1"}],
        "clips": [{"id": "sound", "track": "A1", "asset": "sound", "at": 0.1234,
                   "from": 0.125, "to": 2.125, "params": {"fadeIn": 0.5}}],
    }
    window = Window(start_frame=15, end_frame=45, fps_rational=(30, 1))
    compiled = _attempt(lambda: Timeline.from_json_data(raw).for_render().to_json_data())
    sliced_raw = _attempt(lambda: RenderService._window_timeline(raw, window))
    sliced_compiled = _attempt(lambda: RenderService._window_timeline(compiled, window))
    recompiled = _attempt(
        lambda: Timeline.from_json_data(sliced_raw).for_render().to_json_data()
    )
    idempotent = _attempt(
        lambda: Timeline.from_json_data(compiled).for_render().to_json_data() == compiled
    )
    assert False, "\n".join(
        repr(item)[:700]
        for item in (compiled, sliced_raw, sliced_compiled, recompiled, idempotent)
    )
