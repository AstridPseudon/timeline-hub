"""Run the real service/serialization/duration boundary, without rendering."""
import copy
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

from astrid.core.rendering.contracts import FrameWindow, RenderProfile, RenderRequest, SCHEMA_VERSION
from astrid.core.rendering.service import RenderService
from astrid.core.timeline.duration import timeline_duration_frames, timeline_render_duration_frames
from astrid.packs.rendering.shared.rendering_backend import _serialize_timeline
from astrid.packs.rendering.rendering.renderers.remotion.run import _native_window_argument


def result(call):
    try:
        return {"value": call()}
    except ValueError as error:
        return {"error": str(error)}


clock = {"authored_duration_frames": 300, "render_duration_frames": 330,
         "tail": {"policy": "unmapped_excess_rendered_region", "source_asset": "tail",
                  "start_frame": 300, "end_frame": 330,
                  "source_start_frame": 300, "source_end_frame": 330}}
profile = RenderProfile(320, 180, (30, 1), (1, 90000), "h264", "yuv420p")
rows = []
with tempfile.TemporaryDirectory(prefix="tail-legacy-probe-") as directory:
    root = Path(directory)
    for shape, source_role in [(shape, source_role) for source_role in (False, True)
                               for shape in ("empty", "sparse-early", "sparse-middle", "sparse-end")]:
        payload = {
            "theme": "banodoco-default",
            "theme_overrides": {"visual": {"canvas": {"width": 320, "height": 180, "fps": 30}}},
            "tracks": [{"id": key, "kind": "visual", "label": key} for key in ("bottom", "top")],
            "clips": [{"id": "base", "track": "bottom", "asset": "base", "at": 0, "from": 0, "to": 10}],
            "app": {"astrid_render_clock": copy.deepcopy(clock)},
            "metadata": {"custom": {"keep": True}},
        }
        if source_role:
            payload["tracks"].append({"id": "reference", "kind": "visual", "label": "Reference", "role": "source"})
            payload["clips"].append({"id": "reference", "track": "reference", "asset": "tail", "at": 0, "from": 0, "to": 20})
        if shape != "empty":
            at, hold = {"sparse-early": (0, 1), "sparse-middle": (5, 0.5), "sparse-end": (9, 1)}[shape]
            payload["clips"].append({"id": "top", "track": "top", "asset": "base", "at": at, "from": 0, "to": hold})
        source = root / "timeline.json"
        source.write_text(json.dumps(payload))
        before = source.read_bytes()
        original = _serialize_timeline(source)
        assert timeline_duration_frames(payload, 30) == (600 if source_role else 300)
        raw_duration = result(lambda: timeline_render_duration_frames(payload, 30))
        assert ("error" in raw_duration) is source_role
        assert timeline_duration_frames(original, 30) == 300
        assert timeline_render_duration_frames(original, 30) == 330
        assert all(t["id"] != "reference" for t in original["tracks"])
        assert original["app"]["astrid_render_clock"] == clock
        cases = [("ordinary-full", None, None, True)]
        for start, end in ((0, 330), (150, 180), (285, 315), (300, 330)):
            window = FrameWindow(start, end, (30, 1))
            cases.append((f"ordinary-window-{start}-{end}", None, window, True))
            for track, z in (("bottom", 0), ("top", 1), ("reference", 2)):
                if track == "reference" and not source_role:
                    continue
                for native in (True, False):
                    cases.append((f"{track}-{start}-{end}-supports-{native}",
                                  SimpleNamespace(tracks=(track,), z=z), window, native))
        for name, layer, window, native in cases:
            request = RenderRequest(SCHEMA_VERSION, str(source), "out.mp4", window=window,
                                    metadata={"review": "{}"})
            adapted, _ = RenderService._segment_request(
                object.__new__(RenderService), request,
                candidate=SimpleNamespace(id="fixture", manifest=SimpleNamespace(capabilities={"supports_windows": native})),
                segment=SimpleNamespace(window=window, layer=layer), index=len(rows), workspace=root)
            materialized = json.loads(Path(adapted.timeline_path).read_text())
            selected = _serialize_timeline(Path(adapted.timeline_path))
            assert selected["app"]["astrid_render_clock"] == clock
            assert adapted.metadata == request.metadata
            assert source.read_bytes() == before
            if layer:
                assert selected["metadata"]["astrid_layer"] == {"z": layer.z, "alpha": layer.z > 0}
            duration = result(lambda: timeline_render_duration_frames(selected, 30))
            native_argument = result(lambda: _native_window_argument(adapted.window, selected, profile))
            if layer is None:
                assert duration == {"value": 330}
                assert native_argument == {"value": None if window is None else f"--frames={window.start_frame}-{window.end_frame - 1}"}
            rows.append({"shape": shape, "source_role": source_role, "case": name,
                         "original_raw_duration": raw_duration,
                         "window": None if adapted.window is None else [adapted.window.start_frame, adapted.window.end_frame],
                         "selected_absolute_window": None if window is None else [window.start_frame, window.end_frame],
                         "raw_clip_extent": timeline_duration_frames(materialized, 30),
                         "render_clip_extent": timeline_duration_frames(selected, 30),
                         "render_duration": duration, "native_argument": native_argument,
                         "props": {"timeline": selected, "assets": {"assets": {
                             "base": {"file": "plate.mp4"}, "tail": {"file": "tail.mp4"}}}}})
print(json.dumps({"revision": sys.argv[1], "service_source": str(Path(sys.modules[RenderService.__module__].__file__).resolve()),
                  "rows": rows}, indent=2))
