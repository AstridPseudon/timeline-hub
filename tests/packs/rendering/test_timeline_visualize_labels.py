from __future__ import annotations

from pathlib import Path

from PIL import Image

from astrid.packs.rendering.actions.timeline_visualize import fast_lane
from astrid.packs.rendering.actions.timeline_visualize.fast_lane import Moment
from astrid.packs.rendering.actions.timeline_visualize.filmstrip_cards import (
    _contact_overlay_for_layers,
    attach_frame_addresses,
)
from astrid.packs.rendering.actions.timeline_visualize.layers import discover, resolve_layers
from astrid.packs.rendering.actions.timeline_visualize.layers.builtin import render_strip
from astrid.packs.rendering.actions.timeline_visualize.motion.sheet import build_context
from astrid.packs.rendering.actions.timeline_visualize.overlays.labels import (
    Visible,
    addresses_at,
    draw_labels,
    labels_for,
)
from tests.packs.rendering.test_host_scene import capture_label_inputs as capture_label_inputs
from tests.packs.rendering.test_host_scene import host_project as host_project
from tests.packs.rendering.test_host_scene import native_host as native_host

FPS = 10.0
CANVAS = {"width": 200, "height": 100}
CONTENT_RGB = (250, 204, 21)
PICTURE_RGB = (56, 189, 248)
BACKING_RGB = (11, 18, 32)
CONFIG = {
    "theme_overrides": {"visual": {"canvas": CANVAS}},
    "tracks": [{"id": "content", "kind": "visual"}, {"id": "plate", "kind": "visual"}],
    "clips": [
        {"id": "occ:c02.card", "track": "content", "clipType": "test-card", "at": 0, "from": 0, "to": 2,
         "app": {"cut": "c02", "layer": "card"}, "x": 20, "y": 40, "width": 60, "height": 40},
        {"id": "occ:c01.field", "track": "plate", "clipType": "test-field", "at": 0, "from": 0, "to": 2,
         "app": {"cut": "c01", "layer": "field"}},
        {"id": "occ:c03.late", "track": "content", "clipType": "test-card", "at": 1.5, "from": 0, "to": 1,
         "app": {"cut": "c03", "layer": "late"}, "x": 0, "y": 0, "width": 10, "height": 10},
    ],
}


def _blank() -> Image.Image:
    return Image.new("RGB", (200, 100), (0, 0, 0))


def test_labels_below_five_percent_opacity_are_skipped():
    faint = Visible(clip_id="occ:c09.ghost", address="c09.ghost", track="content", z=0, role="content",
                    opacity=0.01, bounds=(20.0, 10.0, 80.0, 50.0), bounds_source="declared", full_frame=False)
    out = draw_labels(_blank(), [faint], canvas=CANVAS, tile_size=(200, 100))
    assert out.tobytes() == _blank().tobytes()


def test_addresses_follow_visible_order_and_frame_time():
    assert addresses_at(CONFIG, 3, FPS) == ["c02.card", "c01.field"]
    assert [item.address for item in labels_for(CONFIG, 16, FPS)] == ["c03.late", "c02.card", "c01.field"]


def test_declared_boxes_and_full_frame_layers_are_drawn_differently(native_label_inputs):
    _snapshot, batches = native_label_inputs(CONFIG, [3], FPS, CANVAS)
    out = draw_labels(_blank(), batches[3], canvas=CANVAS, tile_size=(200, 100))
    assert out.getpixel((20, 60)) == CONTENT_RGB
    assert out.getpixel((3, 3)) == BACKING_RGB
    strip = [out.getpixel((x, y)) for x in range(4, 120) for y in range(4, 18)]
    assert PICTURE_RGB in strip
    assert out.getpixel((70, 70)) == (0, 0, 0)


def test_labels_layer_is_opt_in_for_motion_and_contact():
    layer = discover()["labels"]
    assert layer.default is False and layer.experimental is False
    assert "labels" not in {item.name for item in resolve_layers(None, view="motion")}
    assert "labels" in {item.name for item in resolve_layers(["labels"], view="motion")}
    assert "labels" not in {item.name for item in resolve_layers(None, view="contact")}
    assert "labels" in {item.name for item in resolve_layers(["labels"], view="contact")}


def test_motion_strip_adds_addresses_to_a_display_tile(tmp_path: Path, native_label_inputs):
    source = tmp_path / "frame.png"
    _blank().save(source)
    snapshot, batches = native_label_inputs(CONFIG, [3], FPS, CANVAS)
    cut = {"index": 1, "start": 0.0, "end": 2.0, "duration": 2.0, "clip_id": "c02", "shot": "demo"}
    ctx = build_context(snapshot, cut, {3: source}, fps=FPS, frame_size=(200, 100), layer_names=("labels",),
                        label_batches=batches, label_canvas=CANVAS)
    ctx.width = 220
    ctx.shared.update({"window": {"preset": "frame"}, "columns": 1, "tile_w": 200})

    result = render_strip(ctx)

    assert result.image.getpixel((30, 70)) == CONTENT_RGB


def test_contact_tiles_apply_labels_without_replacing_the_source_image(native_label_inputs):
    snapshot, batches = native_label_inputs(CONFIG, [3], FPS, CANVAS)
    overlay = _contact_overlay_for_layers(snapshot, ("labels",), FPS, frames=[3],
                                          label_batches=batches, label_canvas=CANVAS)
    assert overlay is not None
    original = _blank()
    labelled = overlay(original, 0.3)
    assert labelled.getpixel((20, 60)) == CONTENT_RGB
    assert original.getpixel((20, 60)) == (0, 0, 0)


def test_compact_frame_index_rows_include_visible_addresses():
    receipt = {"cards": [{"id": "frame-000000003"}, {"id": "frame-000000016"}]}
    cards = [{"frame": 3}, {"frame": 16}]

    attach_frame_addresses(receipt, {"config": CONFIG, "fps_rational": [10, 1]}, cards)

    assert receipt["cards"][0]["addresses"] == ["c02.card", "c01.field"]
    assert receipt["cards"][1]["addresses"] == ["c03.late", "c02.card", "c01.field"]


def test_verify_labels_use_display_copies_and_keep_decoded_frames_unchanged(tmp_path: Path, monkeypatch, native_label_inputs):
    snapshot, _batches = native_label_inputs(CONFIG, [3], FPS, CANVAS)
    pair = {
        "base_snapshot": snapshot,
        "working_snapshot": snapshot,
        "base_run": "base-run",
        "working_run": "working-run",
        "base_video": tmp_path / "base.mp4",
        "working_video": tmp_path / "working.mp4",
        "base_media": {"object_id": "base-object", "digest": "base-digest"},
        "working_media": {"object_id": "working-object", "digest": "working-digest"},
    }
    monkeypatch.setattr(fast_lane, "prepare_pair", lambda *args, **kwargs: pair)
    original_bytes = {}

    def decode(_video, frames, out_dir):
        out_dir.mkdir(parents=True, exist_ok=True)
        frame = frames[0]
        path = out_dir / f"frame-{frame}.png"
        _blank().save(path)
        original_bytes[path] = path.read_bytes()
        return {frame: path}

    monkeypatch.setattr(fast_lane, "decode_frames", decode)

    result = fast_lane.verify(
        object(), "demo", "timeline", [Moment(0.3, "moment")], draft=object(),
        root=tmp_path / "verify", labels=True,
    )

    row = result["rows"][0]
    assert result["notes"] == []
    assert result["base_media"] is pair["base_media"]
    assert result["working_media"] is pair["working_media"]
    assert set(row["labelled"]) == {"published", "working"}
    assert Path(row["published_display"]) != Path(row["published"])
    assert Path(row["working_display"]) != Path(row["working"])
    for path, contents in original_bytes.items():
        assert path.read_bytes() == contents
    with Image.open(row["working_display"]) as labelled:
        assert labelled.getpixel((20, 60)) == CONTENT_RGB


def test_verify_canvas_bounds_scale_raw_decoded_frame_coordinates():
    assert fast_lane._canvas_bounds((62, 7, 218, 75), (320, 180), (1920, 1080)) == (372, 42, 1308, 450)
    assert fast_lane._canvas_bounds((62, 7, 218, 75), (320, 180), (1920, 1080), offset=(10, 20)) == (72, 27, 228, 95)
