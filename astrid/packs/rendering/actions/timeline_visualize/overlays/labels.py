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


def canvas_of(config: Mapping[str, Any], theme: Mapping[str, Any] | None = None) -> dict[str, int]:
    """Return the declared visual canvas, defaulting to 1920 by 1080."""
    canvas = (((config.get("theme_overrides") or {}).get("visual") or {}).get("canvas")
              or ((theme or {}).get("visual") or {}).get("canvas") or {})
    try:
        width, height = int(canvas.get("width") or DEFAULT_CANVAS[0]), int(canvas.get("height") or DEFAULT_CANVAS[1])
    except (TypeError, ValueError):
        width, height = DEFAULT_CANVAS
    return {"width": width, "height": height}


@dataclass(frozen=True)
class Visible:
    clip_id: str
    address: str
    track: str
    z: int
    role: str
    opacity: float | None
    bounds: tuple[float, float, float, float] | None
    bounds_source: str
    full_frame: bool
    status: str = "known"
    message: str = ""


def labels_batch(config: Mapping[str, Any], frames: Sequence[int], fps: float,
                 canvas: Mapping[str, int] | None = None, *, assets=None, theme=None) -> dict[int, list[Visible]]:
    """One native query for a set of frames; missing render inputs stay explicit."""
    from astrid.core.timeline import scene_answers

    requested = list(dict.fromkeys(frames))
    if not requested:
        return {}
    declared_canvas = (((config.get("theme_overrides") or {}).get("visual") or {}).get("canvas") or {})
    theme_canvas = ((theme or {}).get("visual") or {}).get("canvas") or {}
    basis = {**dict(canvas or declared_canvas or theme_canvas), "fps": fps}
    try:
        answers = scene_answers.host_frames_at({"timeline": config, "assets": assets, "theme": theme}, basis, requested)
    except scene_answers.SceneQueryUnavailable as exc:
        return unavailable_labels(config, requested, fps, str(exc))
    return labels_from_frames(config, answers)


def unavailable_labels(config: Mapping[str, Any], frames: Sequence[int], fps: float,
                       reason: str) -> dict[int, list[Visible]]:
    """Structural address diagnostics, never confirmed visibility or a new query."""
    if not frames:
        return {}

    from astrid.core.timeline.duration import clip_end_frame, clip_start_frame
    from astrid.core.timeline.scene_roles import _address, element_coverage, role_of

    clips = {c["id"]: c for c in config.get("clips") or []}
    declarations = element_coverage({c.get("clipType", "") for c in clips.values()})
    result = {}
    tracks = {t["id"]: (i, t) for i, t in enumerate(config.get("tracks") or [])}
    ordered = sorted(reversed(list(clips.values())), key=lambda c: tracks.get(c.get("track"), (len(tracks), {}))[0])
    ordered = [(i, c) for i, c in enumerate(ordered)
               if tracks.get(c.get("track"), (0, {}))[1].get("kind") != "audio"
               and role_of(c, c.get("track"), declarations) != "none"]
    for frame in frames:
        active = [(i, c) for i, c in ordered if clip_start_frame(c, fps) <= frame < clip_end_frame(c, fps)]
        result[frame] = [Visible(c["id"], _address(c), str(c.get("track", "")), i,
                                 role_of(c, c.get("track"), declarations), None, None, "unknown", False,
                                 "unavailable", reason) for i, c in active]
        if not active:
            result[frame] = [Visible("", "Scene unavailable", "", 0, "content", None, None,
                                     "unknown", False, "unavailable", reason)]
    return result


def labels_from_frames(config: Mapping[str, Any], answers: Sequence[Mapping[str, Any]]) -> dict[int, list[Visible]]:
    """Project labels from the same public rows retained by a fresh capture."""
    from astrid.core.timeline.scene_roles import _address

    clips = {c["id"]: c for c in config.get("clips") or []}
    result = {}
    for answer in answers:
        layers = []
        for layer in reversed(answer["layers"]):
            if layer["visible"] is False or layer["role"] == "none":
                continue
            rect = layer["bounds"].get("rect") if layer["bounds"]["status"] == "known" else None
            bounds = None if rect is None else (rect["x"], rect["y"], rect["x"] + rect["width"], rect["y"] + rect["height"])
            findings = tuple(finding.get("reason", "") for finding in layer.get("findings", ())
                             if finding.get("reason"))
            status = ("unknown" if layer["visible"] == "unknown" or layer.get("coverage") == "unknown"
                      or layer["bounds"]["status"] != "known" else "known")
            layers.append(Visible(layer["clipId"], _address(clips[layer["clipId"]]), layer["track"], layer["z"],
                                  layer["role"], layer["opacity"], bounds,
                                  "full" if layer["fullFrame"] else "declared" if bounds else "unknown",
                                  layer["fullFrame"], status, "; ".join(dict.fromkeys(findings))))
        result[answer["frame"]] = layers
    return result


def snapshot_labels(snapshot: Mapping[str, Any], frames: Sequence[int], *, captured=None) -> dict[int, list[Visible]]:
    """Keep the caller's frozen config, registry and resolved theme together.

    Older snapshots do not retain the runtime theme. Do not substitute their
    historical config slug, the current project theme, or an empty registry.
    """
    from fractions import Fraction

    captured = captured or {}
    missing = [frame for frame in frames if frame not in captured]
    result = labels_batch(snapshot.get("config") or {}, missing, float(Fraction(*snapshot["fps_rational"])),
                          assets=snapshot.get("registry"), theme=snapshot.get("theme"))
    result.update({frame: captured[frame] for frame in frames if frame in captured})
    return result


def labels_for(config: Mapping[str, Any], frame: int, fps: float,
               canvas: Mapping[str, int] | None = None, *, assets=None, theme=None) -> list[Visible]:
    """Layer addresses and honest known/unknown visibility at one exact frame."""
    return labels_batch(config, [frame], fps, canvas, assets=assets, theme=theme)[frame]


def addresses_at(config: Mapping[str, Any], frame: int, fps: float,
                 canvas: Mapping[str, int] | None = None, *, assets=None, theme=None) -> list[str]:
    """Candidate addresses, top first; unknown visibility remains advisory."""
    return [item.address for item in labels_for(config, frame, fps, canvas, assets=assets, theme=theme)
            if item.clip_id and (item.opacity is None or item.opacity >= MIN_OPACITY)]


def _caption(item: Visible) -> str:
    return (item.address + (" · scene unavailable" if item.status == "unavailable" else
                           " · visibility unknown" if item.status == "unknown" else "")
            + (" · opacity unknown" if item.opacity is None else ""))


def draw_labels(image, layers: Sequence[Any], *, canvas: Mapping[str, int],
                tile_size: Sequence[int], max_labels: int = 12):
    """Outline declared boxes and list full-frame/unknown-bound layers in a tile legend."""
    from PIL import ImageDraw

    from ..layers.base import draw_text, text_width

    out = image.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    sx = float(tile_size[0]) / float(canvas["width"])
    sy = float(tile_size[1]) / float(canvas["height"])
    shown = sorted((item for item in layers if item.opacity is None or item.opacity >= MIN_OPACITY), key=lambda item: item.z)
    boxed_all = [item for item in shown if item.bounds_source != "full" and item.bounds is not None]
    legend = [item for item in shown if item.bounds_source == "full" or item.bounds is None]
    boxed = boxed_all[:max_labels]
    size = 11
    for item in boxed:
        colour = ROLE_COLOURS.get(item.role, DEFAULT_COLOUR)
        x0, y0, x1, y1 = item.bounds
        rect = (x0 * sx, y0 * sy, x1 * sx, y1 * sy)
        draw.rectangle(rect, outline=colour, width=2)
        tx = max(0, min(rect[0], float(tile_size[0]) - 4))
        ty = rect[1] - size - 6 if rect[1] - size - 6 >= 0 else rect[1] + 2
        _backed_text(draw, (tx, ty), _caption(item), size, colour, text_width, draw_text)
    lines = [(_caption(item) + f" ({item.role})" + ("" if item.bounds is not None else " bounds unknown"),
              ROLE_COLOURS.get(item.role, DEFAULT_COLOUR)) for item in legend]
    hidden = len(boxed_all) - len(boxed)
    if hidden > 0:
        lines.append((f"+{hidden} more", DEFAULT_COLOUR))
    for index, (line, colour) in enumerate(lines[:max_labels]):
        _backed_text(draw, (4, 4 + index * (size + 6)), line, size, colour, text_width, draw_text)
    return out


def overlay_labels_frame(image, config: Mapping[str, Any], frame: int, fps: float, *, layers=None, canvas=None):
    """Draw the visible addresses for one exact decoded frame on a display copy."""
    canvas = canvas if canvas is not None else canvas_of(config)
    return draw_labels(image, layers if layers is not None else labels_for(config, frame, fps), canvas=canvas, tile_size=image.size)


def overlay_labels_at(image, config: Mapping[str, Any], seconds: float, fps: float, *, layers=None, canvas=None):
    """Draw the visible addresses for a contact tile using timeline frame rounding."""
    frame = int(math.floor(float(seconds) * float(fps) + 0.5))
    return overlay_labels_frame(image, config, frame, fps, layers=layers, canvas=canvas)


def _backed_text(draw, xy, text: str, size: int, colour: str, text_width, draw_text) -> None:
    """Draw address text over a dark backing so it reads over any picture."""
    width = text_width(draw, text, size)
    x, y = xy
    draw.rectangle((x - 1, y - 1, x + width + 3, y + size + 3), fill=BACKING)
    draw_text(draw, (x + 1, y), text, size, colour)
