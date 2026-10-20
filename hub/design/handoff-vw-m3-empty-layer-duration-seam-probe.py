"""Read-only source probes; no proposed duration seam is implemented here."""
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

from astrid.core.rendering.contracts import FrameWindow, RenderProfile, RenderRequest, SCHEMA_VERSION
from astrid.core.rendering.service import RenderService
from astrid.core.timeline.banodoco_composer import Timeline
from astrid.core.timeline.duration import clip_start_frame, timeline_render_duration_frames
from astrid.packs.rendering.rendering.renderers.remotion.run import _native_window_argument
from astrid.packs.rendering.shared.rendering_backend import _serialize_timeline


def outcome(window, payload, profile):
    try:
        return _native_window_argument(window, payload, profile)
    except ValueError as error:
        return str(error)


results = {}
with tempfile.TemporaryDirectory(prefix="empty-layer-design-") as directory:
    root = Path(directory)
    for fps_pair in ((30, 1), (30000, 1001)):
        fps = fps_pair[0] / fps_pair[1]
        profile = RenderProfile(320, 180, fps_pair, (1, 90000), "h264", "yuv420p")
        window = FrameWindow(150, 180, fps_pair)
        for shape in ("empty", "sparse", "source-only-longer"):
            payload = {
                "tracks": [{"id": key, "kind": "visual", "label": key}
                           for key in ("bottom", "top")],
                "clips": [{"id": "plate", "track": "bottom", "asset": "plate", "at": 0, "hold": 10}],
                "metadata": {"duration_seconds": 999, "unrelated": {"keep": True}},
            }
            if shape == "sparse":
                payload["clips"].append({"id": "early", "track": "top", "asset": "early", "at": 0.016682, "hold": 1, "from": 0, "to": 1})
            if shape == "source-only-longer":
                payload["tracks"].append({"id": "reference", "kind": "visual", "label": "Reference", "role": "source"})
                payload["clips"].append({"id": "reference", "track": "reference", "asset": "reference", "at": 0, "hold": 20})
            path = root / "source.json"
            path.write_text(json.dumps(payload))
            before = path.read_bytes()
            original = _serialize_timeline(path)
            total = timeline_render_duration_frames(original, fps)
            assert total == 300
            assert outcome(window, original, profile) == "--frames=150-179"
            row = {"original_frames": total, "selected_output_frames": window.duration_frames}
            for native in (True, False):
                request = RenderRequest(SCHEMA_VERSION, str(path), "out.mp4", window=window,
                                        metadata={"review": "{}"})
                candidate = SimpleNamespace(id="fixture", manifest=SimpleNamespace(capabilities={"supports_windows": native}))
                segment = SimpleNamespace(window=window, layer=SimpleNamespace(tracks=("top",), z=1))
                adapted, _ = RenderService._segment_request(
                    object.__new__(RenderService), request, candidate=candidate,
                    segment=segment, index=int(native), workspace=root,
                )
                selected = _serialize_timeline(Path(adapted.timeline_path))
                result = outcome(adapted.window, selected, profile)
                assert selected["metadata"]["astrid_layer"] == {"z": 1, "alpha": True}
                assert adapted.metadata == {"review": "{}"}
                if native:
                    assert result == "Remotion window extends beyond the full composition"
                    assert selected["clips"] == [c for c in original["clips"] if c["track"] == "top"]
                    assert selected["metadata"]["duration_seconds"] == 999
                else:
                    assert result is None and selected["clips"] == []
                    assert abs(selected["metadata"]["duration_seconds"] * fps - 30) < 1e-10
                row[str(native)] = {"selected_clip_extent": timeline_render_duration_frames(selected, fps),
                                    "native_argument_or_error": result, "metadata": selected["metadata"]}
            assert path.read_bytes() == before
            assert outcome(FrameWindow(150, 301, fps_pair), original, profile).endswith("beyond the full composition")
            results[f"{fps_pair}:{shape}"] = row

    raw = {"theme": "banodoco-default", "tracks": [{"id": "a", "kind": "audio", "label": "Audio"}],
           "clips": [{"id": "sound", "track": "a", "asset": "sound", "at": 0.016682,
                      "from": 2, "to": 3, "params": {"opaque": [None, False]}}]}
    authored = Timeline.from_json_data(raw)
    rendered = authored.for_render().to_json_data()
    stored = authored.to_json_data()
    path = root / "stored.json"
    authored.dump(path)
    reopened = _serialize_timeline(path)
    assert raw == rendered and stored == reopened
    for pair in ((30, 1), (30000, 1001)):
        fps = pair[0] / pair[1]
        starts = [clip_start_frame(p["clips"][0], fps) for p in (rendered, stored, reopened)]
        # At 30 fps the exact value is above the tie; at 30000/1001 it is below.
        assert starts == ([1, 1, 1] if pair == (30, 1) else [0, 1, 1])
        results[f"precision:{pair}"] = {"render_at": rendered["clips"][0]["at"],
                                        "stored_at": stored["clips"][0]["at"], "start_frames": starts}
    rendered["clips"][0]["params"]["opaque"].append("copy-only")
    assert authored.for_render().to_json_data() == raw

    filtered = []
    totals = []
    window = FrameWindow(150, 180, (30, 1))
    for hold in (10, 20):
        payload = {"tracks": [{"id": key, "kind": "visual", "label": key} for key in ("bottom", "top")],
                   "clips": [{"id": "plate", "track": "bottom", "asset": "plate", "at": 0, "hold": hold}]}
        path.write_text(json.dumps(payload))
        totals.append(timeline_render_duration_frames(_serialize_timeline(path), 30))
        adapted, _ = RenderService._segment_request(
            object.__new__(RenderService), RenderRequest(SCHEMA_VERSION, str(path), "out.mp4", window=window),
            candidate=SimpleNamespace(id="fixture", manifest=SimpleNamespace(capabilities={"supports_windows": True})),
            segment=SimpleNamespace(window=window, layer=SimpleNamespace(tracks=("top",), z=1)),
            index=0, workspace=root,
        )
        filtered.append(_serialize_timeline(Path(adapted.timeline_path)))
    assert filtered[0] == filtered[1] and totals == [300, 600]
    results["information_loss"] = {"identical_filtered_props": True, "original_frame_counts": totals}

    clock = {"authored_duration_frames": 600, "render_duration_frames": 660,
             "tail": {"policy": "unmapped_excess_rendered_region", "source_asset": "plate",
                      "start_frame": 600, "end_frame": 660, "source_start_frame": 600, "source_end_frame": 660}}
    payload["app"] = {"astrid_render_clock": clock}
    assert timeline_render_duration_frames(payload, 30) == 660
    selected = {**filtered[0], "app": payload["app"]}
    try:
        timeline_render_duration_frames(selected, 30)
    except ValueError as error:
        assert str(error) == "render clock authored_duration_frames must match the authored clip extent"
        results["existing_render_clock_after_filtering"] = str(error)
    else:
        raise AssertionError("An existing media-tail clock must not become a generic duration override")

print(json.dumps(results, indent=2, sort_keys=True))
