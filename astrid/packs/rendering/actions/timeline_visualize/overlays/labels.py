"""Canonical on-screen layer addresses on captured timeline tiles (``c08.loras``)."""
from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

MIN_OPACITY = 0.05
ROLE_COLOURS = {"picture": "#38bdf8", "background": "#a3a3a3", "content": "#facc15"}
DEFAULT_COLOUR = "#e5e7eb"
BACKING = "#0b1220"
DEFAULT_CANVAS = (1920, 1080)


@dataclass(frozen=True)
class SceneLabel:
    address: str
    z: int
    role: str
    opacity: float | None
    bounds: tuple[float, float, float, float] | None
    bounds_source: str
    visible: bool | str


def labels_for_scene(answer: Mapping[str, Any], addresses: Mapping[str, str]) -> list[SceneLabel]:
    """Format public rows and owner-provided addresses without evaluating visibility."""
    labels = []
    for z, layer in enumerate(reversed(answer["layers"])):
        if layer["visible"] is False:
            continue
        bounds = layer["bounds"]
        rect = bounds.get("rect") if bounds["status"] == "known" else None
        box = None if rect is None else (rect["x"], rect["y"],
                                         rect["x"] + rect["width"], rect["y"] + rect["height"])
        labels.append(SceneLabel(addresses[layer["clipId"]], z, layer["role"], layer["opacity"],
                                 box, "unknown" if box is None else "full" if layer["fullFrame"] else "declared",
                                 layer["visible"]))
    return labels


def _labels_for_scene_facts(
    facts: Mapping[str, Any], frame: int, fps: float,
    canvas: Mapping[str, int] | None = None, *, source_identity: str = "",
) -> tuple[list[SceneLabel], dict[str, int]]:
    """Format one already-admitted Scene row without re-evaluating visibility."""
    from astrid.core.rendering.scene_answers import SceneQueryUnavailable

    answer = facts.get("answer")
    basis = facts.get("basis")
    addresses = facts.get("addresses")
    if not source_identity or facts.get("source_identity") != source_identity:
        raise SceneQueryUnavailable("scene label source mismatch")
    if (not isinstance(answer, Mapping) or type(answer.get("frame")) is not int
            or answer["frame"] != frame or not isinstance(answer.get("layers"), list)):
        raise SceneQueryUnavailable("scene label frame mismatch")
    if (not isinstance(basis, Mapping) or type(basis.get("width")) is not int
            or type(basis.get("height")) is not int or basis["width"] <= 0
            or basis["height"] <= 0 or not isinstance(basis.get("fps"), (int, float))
            or isinstance(basis["fps"], bool) or not math.isclose(float(basis["fps"]), fps,
                                                                     rel_tol=0.0, abs_tol=1e-9)):
        raise SceneQueryUnavailable("scene label basis mismatch")
    if (answer.get("width") != basis["width"] or answer.get("height") != basis["height"]
            or not isinstance(addresses, Mapping)
            or any(not isinstance(clip_id, str) or not isinstance(address, str) or not address
                   for clip_id, address in addresses.items())):
        raise SceneQueryUnavailable("scene label source mapping mismatch")
    if any(not isinstance(layer, Mapping) or layer.get("clipId") not in addresses
           for layer in answer["layers"]):
        raise SceneQueryUnavailable("scene label clip mapping mismatch")
    scene_canvas = {"width": basis["width"], "height": basis["height"]}
    requested_canvas = dict(canvas or scene_canvas)
    if requested_canvas != scene_canvas:
        raise SceneQueryUnavailable("scene label canvas mismatch")
    try:
        labels = labels_for_scene(answer, addresses)
    except (KeyError, TypeError, ValueError) as exc:
        raise SceneQueryUnavailable("scene label row is malformed") from exc
    return labels, scene_canvas


def canvas_of(config: Mapping[str, Any]) -> dict[str, int]:
    """Return the declared visual canvas, defaulting to 1920 by 1080."""
    canvas = ((config.get("theme_overrides") or {}).get("visual") or {}).get("canvas") or {}
    try:
        width, height = int(canvas.get("width") or DEFAULT_CANVAS[0]), int(canvas.get("height") or DEFAULT_CANVAS[1])
    except (TypeError, ValueError):
        width, height = DEFAULT_CANVAS
    return {"width": width, "height": height}


def labels_for(config: Mapping[str, Any], frame: int, fps: float,
               canvas: Mapping[str, int] | None = None, *, scene: Mapping[str, Any] | None = None,
               source_identity: str = "") -> list:
    """Visible timeline clips at a frame, top first, using the canonical on-screen model."""
    if scene is not None:
        labels, _scene_canvas = _labels_for_scene_facts(
            scene, frame, fps, canvas, source_identity=source_identity,
        )
        return labels
    from astrid.core.timeline.onscreen import element_coverage, visible_at

    types = {str(clip.get("clipType")) for clip in config.get("clips") or ()
             if isinstance(clip, Mapping) and clip.get("clipType")}
    return visible_at(config, frame, fps, dict(canvas or canvas_of(config)), element_coverage(types))


def addresses_at(config: Mapping[str, Any], frame: int, fps: float,
                 canvas: Mapping[str, int] | None = None, *, scene: Mapping[str, Any] | None = None,
                 source_identity: str = "") -> list[str]:
    """Visible addresses at or above the canonical 5 percent opacity threshold, top first."""
    return [item.address for item in labels_for(
        config, frame, fps, canvas, scene=scene, source_identity=source_identity,
    ) if item.opacity is None or item.opacity >= MIN_OPACITY]


def draw_labels(image, layers: Sequence[Any], *, canvas: Mapping[str, int],
                tile_size: Sequence[int], max_labels: int = 12):
    """Outline declared boxes and list full-frame/unknown-bound layers in a tile legend."""
    from PIL import ImageDraw

    from ..layers.base import draw_text, text_width

    out = image.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    sx = float(tile_size[0]) / float(canvas["width"])
    sy = float(tile_size[1]) / float(canvas["height"])
    shown = sorted((item for item in layers if item.opacity is None or item.opacity >= MIN_OPACITY),
                   key=lambda item: item.z)
    boxed_all = [item for item in shown if item.bounds_source != "full" and item.bounds is not None
                 and item.opacity is not None and getattr(item, "visible", True) is True]
    legend = [item for item in shown if item not in boxed_all]
    boxed = boxed_all[:max_labels]
    size = 11
    for item in boxed:
        colour = ROLE_COLOURS.get(item.role, DEFAULT_COLOUR)
        x0, y0, x1, y1 = item.bounds
        rect = (x0 * sx, y0 * sy, x1 * sx, y1 * sy)
        draw.rectangle(rect, outline=colour, width=2)
        tx = max(0, min(rect[0], float(tile_size[0]) - 4))
        ty = rect[1] - size - 6 if rect[1] - size - 6 >= 0 else rect[1] + 2
        _backed_text(draw, (tx, ty), item.address, size, colour, text_width, draw_text)
    lines = [(item.address + f" ({item.role})" + ("" if item.bounds is not None else " bounds unknown")
              + (" opacity unknown" if item.opacity is None else "")
              + (" visibility unknown" if getattr(item, "visible", True) == "unknown" else ""),
              ROLE_COLOURS.get(item.role, DEFAULT_COLOUR)) for item in legend]
    hidden = len(boxed_all) - len(boxed)
    if hidden > 0:
        lines.append((f"+{hidden} more", DEFAULT_COLOUR))
    for index, (line, colour) in enumerate(lines[:max_labels]):
        _backed_text(draw, (4, 4 + index * (size + 6)), line, size, colour, text_width, draw_text)
    return out


def overlay_labels_frame(image, config: Mapping[str, Any], frame: int, fps: float, *,
                         capture=None, source_identity: str = "", scene: Mapping[str, Any] | None = None):
    """Draw the visible addresses for one exact decoded frame on a display copy."""
    if capture is not None:
        layers, canvas = capture.labels(frame, source_identity=source_identity)
        return draw_labels(image, layers, canvas=canvas, tile_size=image.size)
    if scene is not None:
        layers, canvas = _labels_for_scene_facts(
            scene, frame, fps, source_identity=source_identity,
        )
        return draw_labels(image, layers, canvas=canvas, tile_size=image.size)
    canvas = canvas_of(config)
    return draw_labels(image, labels_for(config, frame, fps, canvas), canvas=canvas, tile_size=image.size)


def overlay_labels_at(image, config: Mapping[str, Any], seconds: float, fps: float):
    """Draw the visible addresses for a contact tile using timeline frame rounding."""
    frame = int(math.floor(float(seconds) * float(fps) + 0.5))
    return overlay_labels_frame(image, config, frame, fps)


def _backed_text(draw, xy, text: str, size: int, colour: str, text_width, draw_text) -> None:
    """Draw address text over a dark backing so it reads over any picture."""
    width = text_width(draw, text, size)
    x, y = xy
    draw.rectangle((x - 1, y - 1, x + width + 3, y + size + 3), fill=BACKING)
    draw_text(draw, (x + 1, y), text, size, colour)
