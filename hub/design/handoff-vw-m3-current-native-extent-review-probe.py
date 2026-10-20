"""Independent service-to-native-window regression; identical expectations before/after."""
import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from astrid.core.rendering.contracts import SCHEMA_VERSION, FrameWindow, RenderProfile, RenderRequest
from astrid.core.rendering.service import RenderService
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion

@pytest.mark.parametrize("hold", [10, 20])
@pytest.mark.parametrize("sparse", [False, True])
def test_original_layer_span_is_renderable(tmp_path, hold, sparse):
    raw = {"theme": "banodoco-default", "tracks": [
        {"id": t, "kind": "visual", "label": t} for t in ("plate", "top")],
        "clips": [{"id": "plate", "track": "plate", "at": 0, "hold": hold}]}
    if sparse:
        raw["clips"].append({"id": "early", "track": "top", "at": 0, "hold": 1})
    path = tmp_path / "timeline.json"
    path.write_text(json.dumps(raw))
    before = path.read_bytes()
    window = FrameWindow(150, 180, (30, 1))
    request = RenderRequest(SCHEMA_VERSION, str(path), "out.mp4", window=window)
    adapted, _ = RenderService._segment_request(object.__new__(RenderService), request,
        candidate=SimpleNamespace(id="probe", manifest=SimpleNamespace(capabilities={"supports_windows": True})),
        segment=SimpleNamespace(window=window, layer=SimpleNamespace(tracks=("top",), z=1)),
        index=0, workspace=tmp_path)
    selected = remotion._serialize_timeline(Path(adapted.timeline_path))
    kwargs = {}
    if "astrid_composition_duration_frames" in adapted.metadata:
        kwargs["composition_duration_frames"] = remotion._composition_duration_from_request(adapted)
    profile = RenderProfile(320, 180, (30, 1), (1, 90000), "h264", "yuv420p")
    assert remotion._native_window_argument(adapted.window, selected, profile, **kwargs) == "--frames=150-179"
    assert adapted.metadata["astrid_composition_duration_frames"] == str(hold * 30)
    assert selected["clips"] == [c for c in raw["clips"] if c["track"] == "top"]
    assert selected["metadata"]["astrid_layer"] == {"z": 1, "alpha": True}
    assert path.read_bytes() == before and adapted.window is window
