"""Captured bounds overlays use public9 rectangles and explicit occurrence joins."""
import copy

import pytest
from PIL import Image, ImageColor

from astrid.packs.rendering.actions.timeline_visualize import filmstrip_cards
from astrid.packs.rendering.actions.timeline_visualize.layers import builtin
from astrid.packs.rendering.actions.timeline_visualize.motion import model, sheet
from tests.packs.rendering.test_motion_cover_public import (
    clip as cover_clip,
)
from tests.packs.rendering.test_motion_cover_public import (
    public_query as _public_query,
)
from tests.packs.rendering.test_motion_cover_public import (
    timeline as cover_timeline,
)
from tests.packs.rendering.test_motion_diagnostics_public import (
    clip,
    elements,
    rect,
    timeline,
)
from tests.packs.rendering.test_motion_diagnostics_public import (
    no_private_boxes as _no_private_boxes,
)
from tests.packs.rendering.test_motion_diagnostics_public import (
    public_diagnostics as _public_diagnostics,
)
from tests.packs.rendering.test_scene_sampling_plan import MetadataProvider, composed_snapshot

public_query = _public_query
public_diagnostics = _public_diagnostics
no_private_boxes = _no_private_boxes


def rgb(colour):
    return ImageColor.getrgb(colour)


def snapshot(config, *, width=960, height=540):
    return {"config": config, "clips": config["clips"], "fps_rational": [30, 1], "duration_frames": 60,
            "timeline_id": "timeline", "render_run_id": "capture", "scripts": [],
            "project_slug": "demo", "video_digest": "sha256:" + "a" * 64,
            "theme": {"visual": {"canvas": {"width": width, "height": height}}}}


@pytest.mark.integration
def test_known_output_and_semantic_regions_scale_to_actual_png(public_diagnostics, no_private_boxes):
    config = timeline([clip("presenter", "am-presenter", bounds=rect(0, 0, 960, 540),
                            face=rect(200, 100, 200, 240), mouth=rect(250, 250, 60, 20)),
                       clip("card", "am-callout", bounds=rect(500, 100, 200, 180),
                            textRect=rect(520, 120, 160, 100), fontPx=32)])
    shared = public_diagnostics(config, [12], width=960, height=540)
    result = builtin.overlay_bounds(Image.new("RGB", (480, 270)), elements(config), .4, 30,
                                    labels=False, shared=shared)
    assert result.getpixel((100, 50)) == rgb(builtin.BOUND_COLOURS["face"])
    assert result.getpixel((125, 125)) == rgb("#ffffff")  # explicit mouth region
    assert result.getpixel((250, 50)) == rgb(builtin.BOUND_COLOURS["card"])
    assert result.getpixel((260, 60)) == rgb(builtin.BOUND_COLOURS["text"])
    assert result.getpixel((100, 13)) == rgb("#94a3b8")  # actual title-safe margin
    assert result.getpixel((50, 50)) == (0, 0, 0)  # no invented half-size geometry
    assert builtin._captured_bounds(elements(config), 12, shared)[2] == []


@pytest.mark.integration
def test_public_preroll_and_half_open_end_drive_motion_strip(tmp_path, public_query, no_private_boxes):
    config = cover_timeline([cover_clip("a", "back", x=100),
                             cover_clip("b", "back", "am-callout", at=1, x=600,
                                        transition={"type": "fade", "duration": .4})])
    shared = public_query(config, [24, 60])
    assert 'data-clip="b"' in shared["html"]["24"]
    source = elements(config)
    ctx = sheet.build_context(snapshot(config), {"index": 1, "start": .7, "end": .9}, {},
                              fps=30, frame_size=(960, 540), layer_names=("strip", "bounds"), **{
                                  key: value for key, value in shared.items() if key.startswith("scene_")})
    assert "b" not in [e.id for e in ctx.elements]  # complete identity universe is required
    path = tmp_path / "24.png"
    Image.new("RGB", (960, 540)).save(path)
    ctx.frames = {24: path}
    ctx.shared.update(tile_w=960, columns=1)
    result = builtin.render_strip(ctx)
    assert result.image.getpixel((10 + 300, 30 + 150)) == rgb(builtin.BOUND_COLOURS["card"])
    assert not builtin.render_bounds(ctx).findings
    boxes, canvas, notes = builtin._captured_bounds(source, 60, shared)
    assert boxes == [] and notes == [] and canvas == (1920, 1080)


@pytest.mark.integration
def test_repeated_sources_join_exact_occurrence_not_label_time_or_suffix(public_diagnostics, no_private_boxes):
    snap = composed_snapshot()
    clips = [copy.deepcopy(c) for c in snap["config"]["clips"]
             if c["app"]["astrid_shot_composition"]["source_clip_id"] == "lower"]
    for i, c in enumerate(clips):
        c.update(at=0, track=c["id"])
        c["params"]["rect"] = rect(200 + 600 * i, 300)
    config = timeline(clips)
    _, source = sheet.snapshot_elements(snap)
    source = [e for e in source if e.clip["app"]["astrid_shot_composition"]["source_clip_id"] == "lower"]
    shared = public_diagnostics(config, [12])
    boxes, _, notes = builtin._captured_bounds(source, 12, shared)
    assert notes == []
    assert [(b.element.occurrence_id, b.rect[0]) for b in boxes] == [("occ-1", 200), ("occ-2", 800)]
    second = copy.deepcopy(shared)
    second["scene_frames"]["12"]["layers"] = [second["scene_frames"]["12"]["layers"][1]]
    boxes, _, notes = builtin._captured_bounds(source, 12, second)
    assert notes == [] and len(boxes) == 1 and boxes[0].element.occurrence_id == "occ-2"


@pytest.mark.integration
@pytest.mark.parametrize("problem", ["missing", "stale", "cached", "unknown", "visibility", "bad-canvas",
                                    "bad-rect", "no-identity", "wrong-occurrence", "wrong-source", "duplicate-layer",
                                    "duplicate-mapping", "duplicate-element"])
def test_unavailable_facts_advise_without_private_or_guessed_rectangles(problem, public_diagnostics, no_private_boxes):
    config = timeline([clip("card", "am-callout", bounds=rect(600, 300, 200, 100), unknown=problem == "unknown")])
    source = elements(config)
    shared = public_diagnostics(config, [12])
    row = shared["scene_frames"]["12"]
    layer = row["layers"][0]
    if problem == "missing":
        shared["scene_frames"] = {}
    elif problem == "stale":
        row["frame"] = 11
    elif problem == "cached":
        shared["scene_unavailable"] = "cached pixels have no fresh Root facts"
    elif problem == "visibility":
        layer["visible"] = None
    elif problem == "bad-canvas":
        row["width"] = 0
    elif problem == "bad-rect":
        layer["bounds"]["rect"]["x"] = float("nan")
    elif problem == "no-identity":
        shared["scene_clip_identities"] = {}
    elif problem == "wrong-occurrence":
        shared["scene_clip_identities"]["card"]["occurrence_id"] = "other"
    elif problem == "wrong-source":
        shared["scene_clip_identities"]["card"]["clip_id"] = "other"
    elif problem == "duplicate-layer":
        row["layers"].append(copy.deepcopy(layer))
    elif problem == "duplicate-mapping":
        shared["scene_clip_identities"]["other"] = shared["scene_clip_identities"]["card"]
    elif problem == "duplicate-element":
        source.append(copy.deepcopy(source[0]))
    boxes, canvas, notes = builtin._captured_bounds(source, 12, shared)
    assert boxes == [] and notes
    result = builtin.overlay_bounds(Image.new("RGB", (960, 540)), source, .4, 30, labels=False, shared=shared)
    assert result.getpixel((300, 150)) == (0, 0, 0)
    assert result.crop((0, 0, 960, 20)).getbbox() is not None  # visible advisory
    if problem in ("missing", "stale", "cached", "bad-canvas"):
        assert canvas is None  # no fabricated safe area


@pytest.mark.integration
@pytest.mark.parametrize("view", ["motion", "contact"])
def test_filmstrip_caller_uses_pixel_facts_without_extra_queries(tmp_path, monkeypatch, public_diagnostics,
                                                             no_private_boxes, view):
    config = timeline([clip("card", "am-callout", bounds=rect(600, 300, 200, 100))])
    snap = snapshot(config, width=1920, height=1080)
    calls = []

    class Provider(MetadataProvider):
        def capture(self, cards, output, resolution):
            self.pixels = [card["frame"] for card in cards]
            calls.append(list(self.pixels))
            shared = public_diagnostics(config, self.pixels)
            self.scene_frames = shared["scene_frames"]
            self.scene_clip_identities = shared["scene_clip_identities"]
            for card in cards:
                path = output / card["image"]
                path.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (960, 540)).save(path)
            return {}

    provider = Provider()
    monkeypatch.setattr(filmstrip_cards, "_audio_envelope", lambda *args: None)
    if view == "contact":
        from astrid.packs.rendering.actions.timeline_visualize import contact_sheet

        def contact(cards, output, *, overlay, **kwargs):
            result = overlay(Image.new("RGB", (480, 270)), .4)
            assert result.getpixel((150, 75)) == rgb(builtin.BOUND_COLOURS["card"])
            return str(output / "contact-sheet.png")

        monkeypatch.setattr(contact_sheet, "static_contact_png", contact)
    else:
        original = sheet.compose_motion_sheet

        def compose(ctx, *args, **kwargs):
            assert len(builtin._captured_bounds(ctx.all_elements, 12, ctx.shared)[0]) == 1
            return original(ctx, *args, **kwargs)

        monkeypatch.setattr(sheet, "compose_motion_sheet", compose)
    result = filmstrip_cards.build_filmstrip_pack(
        out_root=tmp_path / "pack", snapshot=snap, frame_provider=provider,
        options={"view": view, "frame": 12, "layers": ["strip", "bounds"] if view == "motion" else ["bounds"],
                 "preset": "frame", "columns": 1})
    assert calls == [[12]] and provider.reserved is None
    assert not any("unavailable" in f for f in result["findings"])


def test_legacy_without_public_handoff_keeps_declared_boxes(monkeypatch):
    element = model.Element("card", "am-callout", "front", 0, 1, {}, {})
    calls = []

    def boxes(e, t, fps):
        calls.append((e, t, fps))
        return [model.Box(e, "card", (600, 300, 800, 400), "card")]

    monkeypatch.setattr(model, "boxes_at", boxes)
    assert builtin._bounds_handoff({"scene_frames": {}, "scene_clip_identities": {}}) is None
    result = builtin.overlay_bounds(Image.new("RGB", (960, 540)), [element], .4, 30, labels=False)
    assert result.getpixel((300, 150)) == rgb(builtin.BOUND_COLOURS["card"])
    assert calls == [(element, .4, 30)]


def test_motion_empty_public_handoff_keeps_advisory_and_never_uses_private(tmp_path, no_private_boxes):
    config = timeline([clip("card")])
    frame = tmp_path / "12.png"
    Image.new("RGB", (960, 540)).save(frame)
    ctx = sheet.build_context(snapshot(config), {"index": 1, "start": 0, "end": 1}, {12: frame},
                              fps=30, frame_size=(960, 540), layer_names=("strip", "bounds"), scene_frames={})
    result = builtin.render_strip(ctx)
    assert result.image is not None
    assert any("unavailable" in note for note in builtin.render_bounds(ctx).findings)


def test_contact_empty_public_handoff_never_falls_back(no_private_boxes):
    config = timeline([clip("card")])
    overlay = filmstrip_cards._contact_overlay_for_layers(snapshot(config), ["bounds"], 30, scene_shared={})
    result = overlay(Image.new("RGB", (480, 270)), .4)
    assert result.crop((0, 0, 480, 20)).getbbox() is not None
    assert result.getpixel((75, 75)) == (0, 0, 0)
