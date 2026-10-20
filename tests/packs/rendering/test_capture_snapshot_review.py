"""Prepared-file agreement and cache identity must use the same frozen input."""

import json
from copy import deepcopy

from PIL import Image

from astrid.packs.rendering.actions.timeline_visualize import composed_frame
from tests.packs.rendering.test_capture_prepared_files import capture as _capture

capture = _capture


def test_mutating_caller_snapshot_cannot_cache_old_pixels_as_new_source(capture, tmp_path, monkeypatch):
    create, snapshot, timeline, _assets, calls = capture
    colors = {"historical": (255, 0, 0), "current": (0, 255, 0)}

    def acquire(**kwargs):
        def render(frames, output, _resolution):
            config = json.loads(kwargs["context"]["timeline_path"].read_text())
            source = config["app"]["opaque"]
            calls.append(source)
            result = {}
            for frame in frames:
                path = output / f"{frame}.png"
                Image.new("RGB", (8, 8), colors[source]).save(path)
                result[frame] = path
            return result

        return render

    monkeypatch.setattr(composed_frame, "_acquire_shared_remotion_handle", acquire)
    historical = create()
    # The constructor already copied the historical closure for validation.
    # Changing the caller's dict must not relabel those historical pixels.
    snapshot["config"]["app"]["opaque"] = "current"
    snapshot["metadata"]["capture_authority"]["parent_revision_id"] = "new"
    snapshot["fps_rational"] = [60, 1]
    current_snapshot = deepcopy(snapshot)
    cards = [{"frame": 2, "image": "frames/2.png"}]
    try:
        historical.capture(cards, tmp_path / "historical")
        timeline.write_text(json.dumps(current_snapshot["config"]))
        current = create(current_snapshot)
        try:
            current.capture(cards, tmp_path / "current")
            with Image.open(tmp_path / "current/frames/2.png") as image:
                assert image.getpixel((0, 0)) == colors["current"]
            assert calls == ["historical", "current"]
        finally:
            current.close()
    finally:
        historical.close()
