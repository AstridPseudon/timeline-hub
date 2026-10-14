"""Product timelines family CLI (m4 plan step 26, task T28).

This module is the product parser for the runtime-owned ``timelines``
family. Every verb is **argument parsing plus exactly one SDK
call** on the composed :class:`~astrid.sdk.client.AstridClient` (stamped
onto every subparser by
:func:`astrid.core.cli.registration.register_product_commands`), and every
handler renders through the shared product output layer
(:mod:`astrid.core.cli.domain_output`) so the exact five-key JSON envelope,
concise human output, and stable exit codes stay aligned with the frozen SDK
contract.

The parser also mounts the runtime-owned nested ``shots`` family beneath
``timelines``: ``astrid timelines shots <verb>`` embeds the shots
product parser (``astrid/packs/shots/cli.py``) so project-level reusable shot
``list/create/show/add/remove/reorder`` commands are executable only beneath timelines
(plan step 26, task T29). There is **no top-level shots family**.

Verbs (the product routes plus the nested ``shots`` mount; reads resolve the
Runtime-owned canonical current head. The detached working-copy verbs use the
existing timeline SDK checkout and publish semantics; they do not write a
parallel product store):

- ``create`` via ``client.timelines.create_empty`` creates the runtime identity
  shell and first empty parent-composition head.

- ``list`` — ``client.timelines.list`` (active timelines only), rendered as
  compact identity/count summaries; use ``show`` for the canonical current
  head inspection;
- ``show`` — the Runtime-owned bounded current-head inspection by UUID, ULID,
  or slug; ``--summary`` is retained as a presentation spelling and never
  exposes the legacy document;
- ``replace-parent-media`` — replace one selected clip in the canonical
  parent-composition closure through ``client.timelines.replace_parent_media``;
- ``archive`` — reversible event-backed ``client.timelines.archive``;
- ``recover`` — idempotent recovery through ``client.timelines.recover``;
- ``history`` — ordered lifecycle events (read);
- ``diff`` — exact canonical revision comparisons or explicit legacy version diffs (read).
- ``visualize`` — the single public native timeline visualization operation
  (the default captures composed frames from the saved revision with
  synchronized input lanes; ``--mode inputs`` is the render-free declared-input view).
- ``render`` — version-pinned kernel timeline render through the explicit
  ``rendering.render`` `timeline_ref` mode.

**Negative routes (sense check SC28):** the legacy timeline verbs
``migration``, ``push``, ``pull``, ``sync``, ``audit``, ``erase``, and
``repair`` are **absent** from this product parser, as are all obsolete
aliases (``ls``, ``tl``, ...), and ``copy`` is **absent** — the reserved
save-as-copy route is contractually deferred to m6 (plan step 2 / watch
item) and must never be registered here.

This module contains **no SQL** or **repository logic**: it parses argv,
delegates timeline editing semantics to the SDK, and renders the shared
product result envelope.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import shlex
import sys
import uuid
from functools import wraps
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

from astrid.core.cli.domain_output import DomainResult, envelope_dict, print_result, render_human
from astrid.core.cli.registration import CommandSpec, register_product_commands
from astrid.core.cli.task_progress import task_handoff

__all__ = ["COMMANDS", "build_parser"]

_FAMILY = "timelines"
_IN_VERB = False


def _parse_json_object(value: str) -> dict[str, Any]:
    """Parse a ``--config``/``--registry`` JSON object argument."""
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"invalid JSON object: {exc.msg}") from exc
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("must be a JSON object")
    return parsed


def _add_json_flag(subparser: argparse.ArgumentParser, *, default: bool = True) -> None:
    subparser.add_argument(
        "--json",
        action="store_true",
        default=default,
        help=(
            "Print the exact SDK envelope (ok/data/error/receipt/idempotency_key)."
            if not default
            else "Print the exact SDK envelope (ok/data/error/receipt/idempotency_key); default output."
        ),
    )


def _add_idempotency_key(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "--idempotency-key",
        dest="idempotency_key",
        default=None,
        help="Caller idempotency key (a fresh key is generated when absent).",
    )


def _add_project_arg(
    subparser: argparse.ArgumentParser, *, required: bool = True
) -> None:
    subparser.add_argument(
        "--project",
        required=required,
        default=None,
        help=(
            "Owning project id or immutable slug. When omitted, use the "
            "workspace runtime's current project."
            if not required
            else "Owning project id or immutable slug."
        ),
    )


# -- handlers (one SDK call each, no domain rules) -------------------------


def _parse_canvas(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*([1-9]\d*)[xX]([1-9]\d*)\s*", value)
    if match is None:
        raise argparse.ArgumentTypeError("canvas must be WIDTHxHEIGHT, e.g. 1920x1080")
    return int(match.group(1)), int(match.group(2))


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _cmd_create(parsed: argparse.Namespace) -> int:
    width, height = parsed.canvas
    config = {
        "tracks": [],
        "theme_overrides": {
            "visual": {"canvas": {"width": width, "height": height, "fps": parsed.fps}}
        },
    }
    result = parsed.client.timelines.create_empty(
        project=parsed.project,
        timeline_id=parsed.timeline_id,
        config=config,
        idempotency_key=parsed.idempotency_key,
    )
    return print_result(result, as_json=parsed.json)


def _cmd_list(parsed: argparse.Namespace) -> int:
    result = parsed.client.timelines.list(
        parsed.project, include_archived=parsed.include_archived
    )
    # Listing is a discovery route. Keep the identity/count view compact and
    # leave current-head content to the canonical ``show`` inspection route.
    if result.ok and isinstance(result.data, (list, tuple)):
        from astrid.sdk.contracts import DomainResult

        data: Any = list(result.data)
        # Runtime list reads are cursor pages: [rows, next_cursor]. Keep the
        # cursor in the envelope while compacting only the document rows.
        if (
            len(data) == 2
            and isinstance(data[0], list)
            and (data[1] is None or isinstance(data[1], str))
        ):
            data = [[_timeline_summary(item) for item in data[0]], data[1]]
        else:
            data = [_timeline_summary(item) for item in data]
        result = DomainResult.success(
            data,
            receipt=result.receipt,
            idempotency_key=result.idempotency_key,
        )
    return print_result(result, as_json=parsed.json)


def _timeline_summary(item: Any) -> Any:
    """Return a compact identity/count view for one listed timeline."""
    if not isinstance(item, Mapping):
        return item

    summary: dict[str, Any] = {}
    # These are the stable identity/lifecycle fields emitted by the runtime.
    for key in (
        "timeline_id", "id", "slug", "name", "version", "config_version",
        "archived", "archived_at", "is_default", "default",
    ):
        if key in item:
            summary[key] = item[key]
    # Some runtime projections keep the display metadata nested.
    display = item.get("display")
    if "is_default" not in summary and isinstance(display, Mapping):
        if "is_default" in display:
            summary["is_default"] = display["is_default"]

    config = item.get("config")
    registry = item.get("registry")
    counts: dict[str, int] = {}
    if isinstance(config, Mapping):
        counts["config_keys"] = len(config)
        for key in ("clips", "tracks", "shots", "scenes"):
            value = config.get(key)
            if isinstance(value, (list, tuple, Mapping)):
                counts[key] = len(value)
    if isinstance(registry, Mapping):
        assets = registry.get("assets")
        if isinstance(assets, (list, tuple, Mapping)):
            counts["assets"] = len(assets)
    if counts:
        summary["counts"] = counts
    return summary


def _human_time(value: Any) -> str:
    """Keep authored times readable without rounding away exact boundaries."""
    if value is None:
        return "?"
    if isinstance(value, (list, tuple)) and len(value) == 2:
        try:
            value = Fraction(int(value[0]), int(value[1]))
        except (TypeError, ValueError, ZeroDivisionError):
            pass
    if isinstance(value, Fraction):
        value = float(value)
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    text = str(value)
    if text.endswith(".0"):
        text = text[:-2]
    return text


def _human_clip_interval(clip: Mapping[str, Any]) -> tuple[str, str]:
    timing = clip.get("timing_projection")
    mounted = timing.get("mounted") if isinstance(timing, Mapping) else None
    if isinstance(mounted, Mapping) and mounted.get("start") is not None and mounted.get("end") is not None:
        return _human_time(mounted["start"]), _human_time(mounted["end"])
    bounds = clip.get("time_bounds") if isinstance(clip.get("time_bounds"), Mapping) else {}
    start = clip.get("at", clip.get("start", clip.get("start_time", clip.get("time", bounds.get("timeline_start")))))
    end = clip.get("end", clip.get("end_time", bounds.get("timeline_end")))
    if end is None:
        duration = clip.get("duration", clip.get("hold", clip.get("duration_seconds")))
        try:
            if isinstance(start, (list, tuple)) and len(start) == 2:
                start_value = Fraction(int(start[0]), int(start[1]))
            else:
                start_value = Fraction(str(start))
            if isinstance(duration, (list, tuple)) and len(duration) == 2:
                duration_value = Fraction(int(duration[0]), int(duration[1]))
            else:
                duration_value = Fraction(str(duration))
            end = start_value + duration_value
        except (TypeError, ValueError):
            end = None
    return _human_time(start), _human_time(end)


def _fractional(value: Any) -> Fraction | None:
    try:
        if isinstance(value, (list, tuple)) and len(value) == 2:
            return Fraction(int(value[0]), int(value[1]))
        return Fraction(str(value))
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def _clip_bounds(clip: Mapping[str, Any]) -> tuple[Fraction | None, Fraction | None]:
    timing = clip.get("timing_projection")
    mounted = timing.get("mounted") if isinstance(timing, Mapping) else None
    if isinstance(mounted, Mapping) and mounted.get("start") is not None and mounted.get("end") is not None:
        return _fractional(mounted["start"]), _fractional(mounted["end"])
    bounds = clip.get("time_bounds") if isinstance(clip.get("time_bounds"), Mapping) else {}
    start = _fractional(clip.get("start", clip.get("at", bounds.get("timeline_start"))))
    end = _fractional(clip.get("end", bounds.get("timeline_end")))
    if end is None and start is not None:
        duration = _fractional(clip.get("duration", clip.get("hold")))
        if duration is not None:
            end = start + duration
    return start, end


def _human_clip_name(clip: Mapping[str, Any]) -> str:
    source = clip.get("source")
    candidates = [
        clip.get("media_name"), clip.get("asset_name"), clip.get("name"),
        clip.get("asset"), clip.get("asset_id"),
        source.get("name") if isinstance(source, Mapping) else None,
        source.get("key") if isinstance(source, Mapping) else source if isinstance(source, str) else None,
    ]
    return next((str(value) for value in candidates if value not in (None, "")), "(unnamed media)")


def _human_clip_controls(clip: Mapping[str, Any]) -> list[str]:
    controls: list[str] = []
    dispatch = clip.get("compositor_dispatch")
    authored_prefix = "authored " if isinstance(dispatch, Mapping) and dispatch.get("status") == "resolved" else ""
    authored = clip.get("authored_fields") if isinstance(clip.get("authored_fields"), Mapping) else {}
    presentation = clip.get("presentation_fields") if isinstance(clip.get("presentation_fields"), Mapping) else {}
    opacity = clip.get("opacity", presentation.get("opacity", authored.get("opacity")))
    if isinstance(opacity, (int, float)) and opacity != 1 and opacity != 100:
        controls.append(authored_prefix + (f"opacity {opacity * 100:g}%" if 0 <= opacity <= 1 else f"opacity {opacity:g}%"))
    speed = clip.get("speed", clip.get("playback_rate"))
    if isinstance(speed, (list, tuple)) and len(speed) == 2:
        try:
            speed = float(Fraction(int(speed[0]), int(speed[1])))
        except (TypeError, ValueError, ZeroDivisionError):
            speed = None
    if isinstance(speed, (int, float)) and speed != 1:
        controls.append(f"{authored_prefix}speed {speed:g}×")
    blend = clip.get("blend", clip.get("blend_mode"))
    if blend not in (None, "", "normal"):
        controls.append(f"{authored_prefix}blend {blend}")
    if clip.get("muted") is True or clip.get("mute") is True:
        controls.append(f"{authored_prefix}muted")
    gain = clip.get("gain", clip.get("volume"))
    if isinstance(gain, (int, float)) and gain != 1:
        controls.append(f"{authored_prefix}gain {gain:g}")
    if clip.get("timing_unknown") is True:
        controls.append("motion timing unknown")
    return controls


def _human_track_controls(track: Mapping[str, Any]) -> list[str]:
    controls: list[str] = []
    opacity = track.get("opacity")
    if isinstance(opacity, (int, float)) and opacity not in (1, 100):
        controls.append(f"opacity {opacity * 100:g}%" if 0 <= opacity <= 1 else f"opacity {opacity:g}%")
    blend = track.get("blend", track.get("blend_mode", track.get("blendMode")))
    if blend not in (None, "", "normal"):
        controls.append(f"blend {blend}")
    if track.get("muted") is True or track.get("mute") is True:
        controls.append("muted")
    volume = track.get("volume", track.get("gain"))
    if isinstance(volume, (int, float)) and volume != 1:
        controls.append(f"gain {volume:g}")
    return controls


def _human_is_audio_clip(clip: Mapping[str, Any]) -> bool:
    """Prefer the resolved compositor target, falling back to authored facts."""
    dispatch = clip.get("compositor_dispatch")
    if isinstance(dispatch, Mapping) and dispatch.get("status") == "resolved":
        dispatched_track = dispatch.get("track")
        dispatched_kind = dispatched_track.get("kind") if isinstance(dispatched_track, Mapping) else None
        if dispatched_kind in {"audio", "visual"}:
            return dispatched_kind == "audio"
    track = clip.get("track")
    candidates = (
        clip.get("kind"), clip.get("media_type"), clip.get("clip_type"),
        track.get("kind") if isinstance(track, Mapping) else None,
        clip.get("track_kind"),
    )
    for value in candidates:
        if not isinstance(value, str) or not value.strip():
            continue
        kind = value.lower()
        if kind in {"audio", "sound", "music"} or kind.startswith("audio/"):
            return True
    return False


def _human_dispatch_lines(clip: Mapping[str, Any]) -> list[str]:
    """Describe effective compositor controls without replacing authored tracks."""
    dispatch = clip.get("compositor_dispatch")
    if not isinstance(dispatch, Mapping):
        return []
    if dispatch.get("status") != "resolved":
        reason = dispatch.get("reason") or "compositor dispatch could not be resolved"
        return [f"         [compositor dispatch unknown: {reason}]"]

    track = dispatch.get("track") if isinstance(dispatch.get("track"), Mapping) else {}
    controls = dispatch.get("controls") if isinstance(dispatch.get("controls"), Mapping) else {}
    kind = track.get("kind")
    track_id = track.get("id") or "unknown"
    effective: list[str] = []
    if kind == "audio":
        if track.get("muted") is True or track.get("mute") is True:
            effective.append("muted")
        parent_volume = track.get("volume", track.get("gain"))
        if isinstance(parent_volume, (int, float)) and parent_volume != 1:
            effective.append(f"parent volume {parent_volume:g}")
        base_gain = controls.get("base_gain")
        if isinstance(base_gain, (int, float)):
            effective.append(f"effective base gain {base_gain:g}")
    elif kind == "visual":
        track_opacity = controls.get("track_opacity_multiplier")
        if isinstance(track_opacity, (int, float)) and track_opacity != 1:
            effective.append(
                f"effective track opacity {track_opacity * 100:g}%"
                if 0 <= track_opacity <= 1 else f"effective track opacity {track_opacity:g}%"
            )
        clip_opacity = controls.get("clip_opacity_multiplier")
        if isinstance(clip_opacity, (int, float)) and clip_opacity != 1:
            effective.append(
                f"effective clip opacity {clip_opacity * 100:g}%"
                if 0 <= clip_opacity <= 1 else f"effective clip opacity {clip_opacity:g}%"
            )
        blend = track.get("blend", track.get("blend_mode", track.get("blendMode")))
        if blend not in (None, "", "normal"):
            effective.append(f"blend {blend}")
    if effective:
        return [f"         compositor dispatch: {kind or 'unknown'} track {track_id} [{', '.join(effective)}]"]
    return [f"         compositor dispatch: {kind or 'unknown'} track {track_id}"]


def _human_dispatch_group_presentation(
    clips: list[Mapping[str, Any]],
) -> tuple[str | None, dict[int, list[str]]]:
    """Hoist controls shared by one resolved dispatch track to its exact heading."""
    resolved: list[tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], str, str]] = []
    for clip in clips:
        dispatch = clip.get("compositor_dispatch")
        if not isinstance(dispatch, Mapping) or dispatch.get("status") != "resolved":
            return None, {}
        track = dispatch.get("track") if isinstance(dispatch.get("track"), Mapping) else {}
        controls = dispatch.get("controls") if isinstance(dispatch.get("controls"), Mapping) else {}
        kind = str(track.get("kind") or "unknown")
        track_id = str(track.get("id") or "unknown")
        resolved.append((clip, dispatch, track, kind, track_id))

    if not resolved:
        return None, {}

    _first_clip, first_dispatch, first_track, kind, track_id = resolved[0]
    first_controls = first_dispatch.get("controls", {})
    first_controls = first_controls if isinstance(first_controls, Mapping) else {}

    def shared_track_controls(
        track: Mapping[str, Any], controls: Mapping[str, Any], dispatch_kind: str
    ) -> list[str]:
        values: list[str] = []
        if dispatch_kind == "audio":
            if track.get("muted") is True or track.get("mute") is True:
                values.append("muted")
            parent_volume = track.get("volume", track.get("gain"))
            if isinstance(parent_volume, (int, float)) and parent_volume != 1:
                values.append(f"parent volume {parent_volume:g}")
        elif dispatch_kind == "visual":
            track_opacity = controls.get("track_opacity_multiplier")
            if isinstance(track_opacity, (int, float)) and track_opacity != 1:
                values.append(
                    f"effective track opacity {track_opacity * 100:g}%"
                    if 0 <= track_opacity <= 1 else f"effective track opacity {track_opacity:g}%"
                )
            blend = track.get("blend", track.get("blend_mode", track.get("blendMode")))
            if blend not in (None, "", "normal"):
                values.append(f"blend {blend}")
        return values

    shared = shared_track_controls(first_track, first_controls, kind)
    for _clip, dispatch, track, candidate_kind, candidate_id in resolved[1:]:
        controls = dispatch.get("controls", {})
        controls = controls if isinstance(controls, Mapping) else {}
        if (
            candidate_kind != kind
            or candidate_id != track_id
            or shared_track_controls(track, controls, candidate_kind) != shared
        ):
            return None, {}

    per_clip: dict[int, list[str]] = {}
    if kind == "audio":
        base_gains = []
        for _clip, dispatch, _track, _kind, _track_id in resolved:
            controls = dispatch.get("controls") if isinstance(dispatch.get("controls"), Mapping) else {}
            base_gains.append(controls.get("base_gain"))
        numeric_gains = [value for value in base_gains if isinstance(value, (int, float))]
        if (
            len(numeric_gains) == len(base_gains)
            and numeric_gains
            and all(value == numeric_gains[0] for value in numeric_gains)
        ):
            shared.append(f"effective base gain {numeric_gains[0]:g}")
        elif numeric_gains:
            for (clip, *_rest), base_gain in zip(resolved, base_gains):
                if isinstance(base_gain, (int, float)):
                    per_clip[id(clip)] = [f"         compositor dispatch clip controls: effective base gain {base_gain:g}"]
    elif kind == "visual":
        for clip, dispatch, _track, _kind, _track_id in resolved:
            controls = dispatch.get("controls") if isinstance(dispatch.get("controls"), Mapping) else {}
            clip_opacity = controls.get("clip_opacity_multiplier")
            if isinstance(clip_opacity, (int, float)) and clip_opacity != 1:
                label = (
                    f"effective clip opacity {clip_opacity * 100:g}%"
                    if 0 <= clip_opacity <= 1 else f"effective clip opacity {clip_opacity:g}%"
                )
                per_clip[id(clip)] = [f"         compositor dispatch clip controls: {label}"]

    dispatch_label = f"compositor dispatch: {kind} track {track_id}"
    if shared:
        dispatch_label += f" [{', '.join(shared)}]"
    return dispatch_label, per_clip


def _human_track_identity(clip: Mapping[str, Any]) -> tuple[str, str, str]:
    """Return the exact scoped track key, with a stable unassigned fallback."""
    reference = clip.get("track_ref") if isinstance(clip.get("track_ref"), Mapping) else {}
    track = clip.get("track")
    track_id = reference.get("track_id") or clip.get("track_id")
    if not track_id and isinstance(track, Mapping):
        track_id = track.get("id")
    if not track_id and isinstance(track, str):
        track_id = track
    return (
        str(reference.get("scope") or ""),
        str(reference.get("scope_id") or ""),
        str(track_id or "unassigned"),
    )


def _human_track_heading(identity: tuple[str, str, str]) -> str:
    scope, scope_id, track_id = identity
    heading = f"Track {track_id}"
    if scope or scope_id:
        heading += f" ({scope or 'scope unknown'}/{scope_id or 'owner unknown'})"
    return heading


def _human_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _human_clip_detail_lines(
    clip: Mapping[str, Any], *, summary: Mapping[str, Any], scope: Mapping[str, Any]
) -> list[str]:
    """Show bounded authored values plus the exact saved target in detail mode."""
    lines: list[str] = []
    authored = clip.get("authored_fields") if isinstance(clip.get("authored_fields"), Mapping) else {}
    label = clip.get("label", authored.get("label"))
    labels = clip.get("labels", authored.get("labels"))
    if label not in (None, ""):
        lines.append(f"       authored label: {_human_json(label)}")
    if labels not in (None, "", [], {}):
        lines.append(f"       authored labels: {_human_json(labels)}")
    params = clip.get("parameters")
    if params is None:
        params = next((authored.get(key) for key in ("parameters", "params", "props") if key in authored), None)
    if params not in (None, {}, []):
        source = clip.get("parameters_source") or next((key for key in ("parameters", "params", "props") if key in authored), "parameters")
        lines.append(f"       {source}: {_human_json(params)}")
    details = {
        key: value for key, value in (
            ("element_ref", clip.get("element_ref", authored.get("element_ref", authored.get("elementRef")))),
            ("extensions", clip.get("extensions", authored.get("extensions"))),
            ("presentation", clip.get("presentation", authored.get("presentation"))),
            ("presentation_fields", clip.get("presentation_fields", authored.get("presentation_fields"))),
            ("authored_timing", clip.get("authored_timing", authored.get("authored_timing"))),
        ) if value not in (None, {}, [])
    }
    if details:
        lines.append("       authored values: " + _human_json(details))
    # Keep future or opaque authored keys visible without repeating the fields
    # already presented above. Runtime has already bounded this mapping.
    if authored:
        known = {"label", "labels", "parameters", "params", "props", "element_ref", "elementRef",
                 "extensions", "presentation", "presentation_fields", "authored_timing",
                 "id", "clip_id", "clipType", "clip_type", "type", "track", "at", "at_ms",
                 "duration", "duration_ms", "hold", "from", "from_ms", "to", "to_ms",
                 "speed", "asset", "asset_id", "assetId", "source_object_id", "media_id",
                 "object_id", "content_sha256", "content_digest", "digest"}
        remaining = {key: value for key, value in authored.items() if key not in known}
        if remaining:
            lines.append("       authored fields: " + _human_json(remaining))
    elif any(item.get("path") == "authored_fields" for item in clip.get("omitted_fields", []) if isinstance(item, Mapping)):
        lines.append("       authored values: omitted by Runtime's authored-field byte limit")

    exact = {
        key: clip.get(key) for key in (
            "media_name", "asset_id", "source_object_id", "content_digest", "media_type", "element_ref"
        ) if clip.get(key) not in (None, "")
    }
    exact.update({key: clip.get(key) for key in ("shot_id", "occurrence_id", "clip_id") if clip.get(key) not in (None, "")})
    exact["timeline_id"] = scope.get("timeline") or scope.get("timeline_id")
    exact["revision_id"] = summary.get("revision_id")
    exact["is_current_head"] = summary.get("is_current_head")
    exact = {key: value for key, value in exact.items() if value not in (None, "")}
    lines.append("       identity: " + _human_json(exact))
    return lines


def _human_omission_lines(
    omissions: object, *, summary: Mapping[str, Any], scope: Mapping[str, Any],
    occurrence: Mapping[str, Any] | None = None, clip: Mapping[str, Any] | None = None,
    track_ref: Mapping[str, Any] | None = None,
) -> list[str]:
    if not isinstance(omissions, list):
        return []
    lines: list[str] = []
    seen: set[str] = set()
    for omission in omissions:
        if not isinstance(omission, Mapping):
            continue
        identity = _human_json(dict(omission))
        if identity in seen:
            continue
        seen.add(identity)
        path = omission.get("path") or "authored value"
        reason = omission.get("reason") or "omitted"
        size = omission.get("byte_length")
        limit = omission.get("limit_bytes")
        size_text = f" ({size} B; limit {limit} B)" if size is not None and limit is not None else ""
        target = {
            "timeline_id": scope.get("timeline") or scope.get("timeline_id"),
            "revision_id": summary.get("revision_id"),
        }
        if occurrence:
            target.update({key: occurrence.get(key) for key in ("occurrence_id", "shot_id") if occurrence.get(key) is not None})
        if clip:
            target.update({key: clip.get(key) for key in ("occurrence_id", "shot_id", "clip_id") if clip.get(key) is not None})
        if track_ref:
            target["track_ref"] = dict(track_ref)
        elif clip and isinstance(clip.get("track_ref"), Mapping):
            target["track_ref"] = dict(clip["track_ref"])
        elif occurrence and isinstance(occurrence.get("track_ref"), Mapping):
            target["track_ref"] = dict(occurrence["track_ref"])
        target = {key: value for key, value in target.items() if value not in (None, "")}
        digest = omission.get("sha256")
        digest_text = f"; sha256 {digest}" if digest else ""
        lines.append(
            f"       omitted {path}: {reason}{size_text}{digest_text}; pinned target {_human_json(target)}; "
            "full omitted values are unavailable through a bounded retrieval route"
        )
    return lines


def _human_occurrence_lookup(data: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    native = data.get("native_inspection") if isinstance(data.get("native_inspection"), Mapping) else {}
    selected = native.get("selected") if isinstance(native.get("selected"), list) else []
    result: dict[str, Mapping[str, Any]] = {}
    for row in selected:
        if not isinstance(row, Mapping):
            continue
        occurrence = row.get("occurrence")
        if isinstance(occurrence, Mapping) and occurrence.get("occurrence_id") is not None:
            result[str(occurrence["occurrence_id"])] = occurrence
    return result


def _human_motion_lines(clip: Mapping[str, Any], *, detail: bool = False) -> list[str]:
    """Present only producer-supported intervals; custom clocks stay declarations."""
    from astrid.packs.rendering.actions.timeline_visualize.readable_timing import project_readable_timing
    if "timed_changes" not in clip:
        clip = project_readable_timing([clip])[0]
    grouped = {}
    for change in clip.get("timed_changes", []):
        if change.get("hold") and not detail:
            continue
        key = (tuple(change["start"]), tuple(change["end"]), change["kind"], change.get("hold", False))
        grouped.setdefault(key, []).append(change)
    changes = []
    for (start, end, kind, hold), rows in sorted(
        grouped.items(), key=lambda item: (Fraction(*item[0][0]), Fraction(*item[0][1]), item[0][2], item[0][3])
    ):
        values = []
        for row in rows:
            before, after = row["before"], row["after"]
            if row["property"].endswith("multiplier"):
                before, after = f"{before*100:g}%", f"{after*100:g}%"
            else:
                before, after = f"{before:g}", f"{after:g}"
            values.append(f"{row['property']} holds {before}" if hold else f"{row['property']} {before} → {after}")
        label = "transform " if kind == "transform" else ""
        suffix = f" ({kind.replace('_', ' ')})" if kind != "transform" else ""
        if any(row.get("overlapping_fades") for row in rows):
            suffix += " [fade multipliers overlap]"
        changes.append(f"{_human_time(start)}–{_human_time(end)} {label}{'; '.join(values)}{suffix}")
    lines = changes if detail else changes[:3]
    if len(changes) > len(lines):
        lines.append(f"[{len(changes)-len(lines)} more change intervals; expand with --detail]")
    lines.extend(f"[motion timing unknown: {reason}]" for reason in clip.get("timing_unknowns", []))
    transition = clip.get("transition_projection")
    if isinstance(transition, Mapping):
        declaration = transition.get("transition")
        identifier = declaration.get("id", declaration.get("type", "transition")) if isinstance(declaration, Mapping) else declaration
        if transition.get("status") == "resolved":
            source = transition.get("from_target", {})
            destination = transition.get("to_target", {})
            target = lambda value: "/".join(str(value[key]) for key in ("occurrence_id", "clip_id") if value.get(key)) or str(value.get("render_clip_id"))
            lines.append(f"{_human_time(transition['start'])}–{_human_time(transition['end'])} transition {identifier}: {target(source)} → {target(destination)}")
        else:
            lines.append(f"[transition {identifier}; timing unresolved: {transition.get('reason', 'placement unavailable')}]")
    elif clip.get("transition"):
        declaration = clip["transition"]
        identifier = declaration.get("id", declaration.get("type", "transition")) if isinstance(declaration, Mapping) else declaration
        lines.append(f"[transition {identifier}; timing unresolved: producer unavailable]")
    if clip.get("source_clock"):
        lines.append(f"[{clip['source_clock']}]")
    return lines


def _append_navigation_footer(
    lines: list[str], navigation: Mapping[str, Any], *, include_visualize: bool = True,
) -> None:
    """Keep sibling views, editing, and control help visible but compact."""
    commands = navigation.get("commands") if isinstance(navigation.get("commands"), Mapping) else {}
    if include_visualize and commands.get("visualize"):
        lines.append(f"visualize: {commands['visualize']}")
    if commands.get("show"):
        lines.append(f"show: {commands['show']}")
    if commands.get("controls"):
        lines.append(f"controls: {commands['controls']}")
    editing = navigation.get("editing") if isinstance(navigation.get("editing"), Mapping) else {}
    if editing.get("guide"):
        lines.append(f"edit guide: {editing['guide']}")
    edit_commands = editing.get("commands") if isinstance(editing.get("commands"), Mapping) else {}
    if edit_commands.get("checkout"):
        lines.append(f"edit JSON (current head): {edit_commands['checkout']}")


def _render_timeline_human(result: object) -> str:
    """Render a compact, addressable authored timeline for human inspection."""
    envelope = envelope_dict(result)
    if not envelope["ok"]:
        return render_human(result)
    data = envelope.get("data")
    if not isinstance(data, Mapping):
        return render_human(result)
    summary = data.get("summary") if isinstance(data.get("summary"), Mapping) else {}
    query = data.get("query") if isinstance(data.get("query"), Mapping) else {}
    scope = data.get("scope") if isinstance(data.get("scope"), Mapping) else {}
    currentness = (
        "current head" if summary.get("is_current_head") is True
        else "saved revision (not current head)" if summary.get("is_current_head") is False
        else "currentness unknown"
    )
    lines = [
        f"Timeline {scope.get('timeline') or scope.get('timeline_id') or 'current'}",
        f"  revision: {summary.get('revision_id') or 'unknown'} · {currentness} · Authored timeline",
    ]
    filters = [f"{key}={query[key]}" for key in ("range", "occurrence", "shot", "clip", "track", "asset") if query.get(key) not in (None, "", [])]
    if filters:
        lines.append("  scope: " + ", ".join(filters))
    lines.append("Visual layers (order unavailable; grouped by exact scoped track)")
    clips = [item for item in data.get("clips", []) if isinstance(item, Mapping)]
    audio = [clip for clip in clips if _human_is_audio_clip(clip)]
    visual_clips = [clip for clip in clips if not _human_is_audio_clip(clip)]
    occurrence_lookup = _human_occurrence_lookup(data)
    detail = query.get("detail") is True

    def render_rows(rows: list[Mapping[str, Any]], *, section: str) -> None:
        groups: dict[tuple[str, str, str], list[Mapping[str, Any]]] = {}
        tracks: dict[tuple[str, str, str], Mapping[str, Any]] = {}
        for clip in rows:
            identity = _human_track_identity(clip)
            groups.setdefault(identity, []).append(clip)
            track = clip.get("track")
            if isinstance(track, Mapping):
                tracks.setdefault(identity, track)
        if not rows:
            lines.append(f"  (no {section} clip occurrences in this page)")
            return
        display_index = 0
        for identity, group in groups.items():
            track = tracks.get(identity, {})
            heading = _human_track_heading(identity)
            track_label = track.get("label") if isinstance(track, Mapping) else None
            if isinstance(track_label, str) and track_label.strip():
                heading += f" · {track_label}"
            controls = _human_track_controls(track) if isinstance(track, Mapping) else []
            suffix = f" [authored track controls: {', '.join(controls)}]" if controls else ""
            dispatch_heading, dispatch_clip_lines = _human_dispatch_group_presentation(group)
            dispatch_suffix = f" [{dispatch_heading}]" if dispatch_heading else ""
            lines.append(f"  {heading}{suffix}{dispatch_suffix}")
            if isinstance(track, Mapping):
                lines.extend(_human_omission_lines(
                    track.get("omitted_fields"), summary=summary, scope=scope,
                ))
            indexed = list(enumerate(group))
            indexed.sort(key=lambda pair: (
                _clip_bounds(pair[1])[0] is None,
                _clip_bounds(pair[1])[0] or Fraction(0),
                pair[0],
            ))
            for _source_index, clip in indexed:
                display_index += 1
                start, end = _human_clip_interval(clip)
                identity_parts = [clip.get("occurrence_id"), clip.get("clip_id")]
                row_identity = "/".join(str(value) for value in identity_parts if value not in (None, ""))
                label = f" · {row_identity}" if row_identity else ""
                controls = _human_clip_controls(clip)
                suffix = f" [{', '.join(controls)}]" if controls else ""
                lines.append(f"    {display_index}. {start}–{end}  {_human_clip_name(clip)}{label}{suffix}")
                if dispatch_heading:
                    lines.extend(dispatch_clip_lines.get(id(clip), []))
                else:
                    lines.extend(_human_dispatch_lines(clip))
                for change in _human_motion_lines(clip, detail=query.get("detail") is True):
                    lines.append(f"         {change}")
                occurrence = occurrence_lookup.get(str(clip.get("occurrence_id"))) if clip.get("occurrence_id") is not None else None
                if detail:
                    lines.extend(_human_clip_detail_lines(clip, summary=summary, scope=scope))
                # Authored value omissions remain visible in compact mode too.
                lines.extend(_human_omission_lines(
                    [
                        *(clip.get("omitted_fields", []) if isinstance(clip.get("omitted_fields"), list) else []),
                        *(clip.get("authored_omitted_fields", []) if isinstance(clip.get("authored_omitted_fields"), list) else []),
                        *(clip.get("asset_omitted_fields", []) if isinstance(clip.get("asset_omitted_fields"), list) else []),
                        *(clip.get("track_omitted_fields", []) if isinstance(clip.get("track_omitted_fields"), list) else []),
                    ], summary=summary, scope=scope,
                    occurrence=occurrence, clip=clip,
                ))

    # Parent-level occurrence tracks place child timelines on a layer. Keep
    # that owner separate from each child's internal track and associate it
    # with the exact occurrence IDs that appear in the clip rows below.
    placements: dict[tuple[str, str, str, tuple[str, ...]], list[tuple[Mapping[str, Any], Mapping[str, Any]]]] = {}
    for occurrence_id, occurrence in occurrence_lookup.items():
        reference = occurrence.get("track_ref") if isinstance(occurrence.get("track_ref"), Mapping) else {}
        track = occurrence.get("track") if isinstance(occurrence.get("track"), Mapping) else {}
        track_id = reference.get("track_id") or (track.get("id") if isinstance(track, Mapping) else None) or "unassigned"
        occurrence_controls: list[str] = _human_track_controls(track)
        if occurrence.get("mute") is True:
            occurrence_controls.append("muted")
        gain = occurrence.get("gain", occurrence.get("volume"))
        if isinstance(gain, (int, float)) and gain != 1:
            occurrence_controls.append(f"gain {gain:g}")
        key = (
            str(reference.get("scope") or ""), str(reference.get("scope_id") or ""),
            str(track_id), tuple(dict.fromkeys(occurrence_controls)),
        )
        placements.setdefault(key, []).append((occurrence, track))
    if placements:
        lines.append("  Occurrence placement tracks")
        for identity_with_controls, rows in placements.items():
            identity = identity_with_controls[:3]
            controls = list(identity_with_controls[3])
            track = rows[0][1]
            heading = _human_track_heading(identity)
            occurrence_ids = ", ".join(str(row[0].get("occurrence_id")) for row in rows)
            suffix = f" [{', '.join(controls)}]" if controls else ""
            lines.append(f"    {heading} · occurrences {occurrence_ids}{suffix}")
            for occurrence, _track in rows:
                lines.extend(_human_omission_lines(
                    [
                        *(occurrence.get("omitted_fields", []) if isinstance(occurrence.get("omitted_fields"), list) else []),
                        *(occurrence.get("track_omitted_fields", []) if isinstance(occurrence.get("track_omitted_fields"), list) else []),
                    ], summary=summary, scope=scope,
                    occurrence=occurrence,
                ))

    render_rows(visual_clips, section="visual")
    if audio:
        lines.append("Audio (separate tracks; order unavailable unless projected)")
        render_rows(audio, section="audio")
    native = data.get("native_inspection") if isinstance(data.get("native_inspection"), Mapping) else {}
    pagination = data.get("pagination") if isinstance(data.get("pagination"), Mapping) else {}
    if not pagination and isinstance(native.get("next_cursor"), str):
        pagination = {"next_cursor": native.get("next_cursor")}
    page = data.get("page") if isinstance(data.get("page"), Mapping) else native.get("page") if isinstance(native.get("page"), Mapping) else {}
    if page.get("returned_clips") is not None:
        page_line = f"page: returned {page['returned_clips']} of {page.get('total_selected_clips', page['returned_clips'])} selected clips"
        if page.get("remaining_clips") not in (None, 0):
            page_line += f"; {page['remaining_clips']} remain after this page"
        lines.append(page_line)
    if pagination.get("next_cursor"):
        lines.append(f"  page: more results available (cursor {pagination['next_cursor']})")
    omissions = data.get("omission_metadata") if isinstance(data.get("omission_metadata"), Mapping) else native.get("omission_metadata") if isinstance(native.get("omission_metadata"), Mapping) else {}
    omitted_count = omissions.get("authored_values_omitted")
    if isinstance(omitted_count, int) and omitted_count > 0:
        lines.append(f"page: {omitted_count} bounded values omitted; full values are unavailable through a bounded retrieval route")
    navigation = data.get("navigation") if isinstance(data.get("navigation"), Mapping) else {}
    if navigation:
        _append_navigation_footer(lines, navigation)
    return "\n".join(lines)


def _cmd_show(parsed: argparse.Namespace) -> int:
    """Print the Runtime-owned canonical current-head inspection.

    ``show`` deliberately has no whole-document fallback.  A legacy timeline
    document is a mutable storage projection and cannot be presented as the
    current editor state when the native Runtime inspection route is absent.
    """
    presentation = getattr(parsed, "presentation", None)
    if presentation:
        result = _show_presentation(parsed, presentation)
        return print_result(
            result,
            as_json=parsed.json,
            human_renderer=_render_presentation_human,
        )

    # The editor's default ``show`` is the authored cut table. Keep the
    # bounded Runtime inspection available behind --layers and its
    # clip/occurrence/track/asset/cursor selectors; those are the fields the
    # inspection projection can answer without opening the complete bundle.
    values = {
        name: getattr(parsed, name, None)
        for name in ("clip", "occurrence", "shot", "track", "asset", "range", "detail", "limit", "cursor", "revision_id")
    }
    inspection_view = bool(
        getattr(parsed, "layers", False)
        or getattr(parsed, "summary", False)
        or any(values.get(name) for name in ("clip", "occurrence", "asset", "track", "cursor"))
        or (values.get("detail") and not getattr(parsed, "at", None))
    )
    if not inspection_view:
        bundle_opener = getattr(parsed.client.timelines, "open_bundle", None)
        if callable(bundle_opener):
            return _print_cut_table(parsed, bundle_opener)

    from astrid.packs.rendering.actions.timeline_visualize.inspection_contract import inspection_options
    normalized = inspection_options(values)
    opener = getattr(parsed.client.timelines, "open_composition", None)
    if not callable(opener):
        from astrid.sdk.contracts import ErrorObject

        result = DomainResult.failure(
            ErrorObject(
                "unavailable",
                "canonical timeline inspection is unavailable",
                {"project": str(parsed.project), "timeline": str(parsed.ref)},
            )
        )
    else:
        # ``summary`` remains accepted as a presentation flag for CLI
        # compatibility, but both forms read the same bounded canonical
        # projection and never expose the legacy document.
        result = opener(
            parsed.project,
            parsed.ref,
            limit=values.get("limit") or 50,
            cursor=values.get("cursor"),
            clip=normalized["clip"],
            occurrence=normalized["occurrence"],
            shot=normalized["shot"],
            track=normalized["tracks"],
            asset=normalized["asset"],
            range_value=values.get("range"),
            detail=normalized["detail"],
            revision_id=values.get("revision_id"),
        )
    if result.ok and isinstance(result.data, Mapping):
        data = dict(result.data)
        data["navigation"] = _show_navigation_help(
            project=parsed.project,
            ref=parsed.ref,
            parsed=parsed,
            outputs=data,
        )
        result = DomainResult.success(
            data,
            receipt=result.receipt,
            idempotency_key=result.idempotency_key,
        )
    return print_result(result, as_json=parsed.json, human_renderer=_render_timeline_human)


def _render_presentation_human(result: object) -> str:
    """Render only the bounded presentation text from the stable envelope."""
    data = envelope_dict(result).get("data")
    if not isinstance(data, Mapping):
        return render_human(result)
    presentation = data.get("presentation")
    if isinstance(presentation, Mapping) and isinstance(presentation.get("text"), str):
        return presentation["text"]
    return render_human(result)


def _presentation_window(value: str | None) -> tuple[float, float] | None:
    if value in (None, ""):
        return None
    from astrid.sdk.timeline_cuts import _parse_range

    return _parse_range(value)


def _presentation_selection(
    bundle: Mapping[str, Any], parsed: argparse.Namespace,
) -> tuple[dict[str, Any], list[dict[str, Any]], set[str] | None, tuple[float, float] | None]:
    """Resolve presentation selectors against one already-open immutable bundle."""
    from astrid.sdk.timeline_cuts import build_cut_table, filter_rows

    table = build_cut_table(bundle)
    shot = getattr(parsed, "shot", None)
    range_value = getattr(parsed, "range", None)
    shot_rows = filter_rows(table, shot=shot) if shot else list(table.get("rows") or [])
    rows = filter_rows(table, range_value=range_value, shot=shot)
    shot_ids = {str(row["shot_id"]) for row in shot_rows if row.get("shot_id")}
    return table, rows, shot_ids if shot else None, _presentation_window(range_value)


def _print_cut_table(parsed: argparse.Namespace, opener) -> int:
    """Offline-compatible editor projection used by the existing show route."""
    from astrid.sdk.timeline_cuts import (
        build_cut_table, cut_table_payload, filter_rows, page_rows,
        paging_hint, render_cut_table,
    )
    from astrid.sdk.timeline_views import render_at, render_clips, render_code, render_script
    from astrid.sdk.timeline_checkout import Checkout

    result=opener(parsed.project,parsed.ref,revision_id=getattr(parsed,"revision_id",None))
    if not getattr(result,"ok",False):
        return print_result(result,as_json=parsed.json)
    opened=result.data if isinstance(result.data,Mapping) else {}
    bundle=opened.get("bundle",opened)
    checkout=Checkout(dict(bundle))
    working_copy=None; changed_ids=set()
    if not getattr(parsed,"published",False):
        import astrid.sdk.timeline_checkout as checkout_module
        from astrid.sdk.exceptions import ServiceUnavailableError
        try:
            draft=checkout_module.find_draft(parsed.project,parsed.ref)
        except ServiceUnavailableError:
            # A draft is an optional local overlay; an unavailable workspace
            # must not prevent the immutable revision from being inspected.
            draft=None
        if draft is not None:
            checkout=Checkout.load(draft); bundle=checkout.document()
            changes=checkout.edits().get("changes",[])
            changed_ids={str(change["clip_id"]) for change in changes
                         if isinstance(change,Mapping) and change.get("clip_id")}
            base_revision=(checkout.bundle.get("base_parent") or {}).get("revision_id","0")
            working_copy={"draft":str(draft),"edits":len(changed_ids),"base_revision":base_revision}
            table=build_cut_table(bundle)
    table=build_cut_table(bundle)
    try:
        rows=filter_rows(table,range_value=getattr(parsed,"range",None),shot=getattr(parsed,"shot",None))
    except ValueError as exc:
        print(f"error validation_error: {exc}")
        return 2
    view=getattr(parsed,"as_view","cuts") or "cuts"
    if getattr(parsed,"clips",False):
        text=render_clips(bundle,{str(r["shot_id"]) for r in table.get("rows",[]) if not parsed.shot or r.get("shot")==parsed.shot})
        data={"kind":"clips","text":text}
    elif getattr(parsed,"at",None) is not None:
        text=render_at(bundle,table,float(parsed.at),show_command="timelines show")
        data={"kind":"at","text":text}
    elif view in {"script","code"}:
        text=(render_script if view=="script" else render_code)(bundle)
        data={"kind":view,"text":text}
    else:
        shown,info=page_rows(rows,page=getattr(parsed,"page",None),page_size=getattr(parsed,"page_size",None))
        revision_id = opened.get("revision_id", "resolved")
        current = opened.get("is_current_head", opened.get("head_revision_id") in (None, revision_id))
        authority = "current head" if current else f"revision {revision_id}"
        title = f"Timeline {parsed.ref} · project {parsed.project} · {authority}"
        text=render_cut_table(table,shown,title=title,changed_clip_ids=changed_ids)
        if working_copy and changed_ids:
            text=f"WORKING COPY · {len(changed_ids)} clip changed vs published {working_copy['base_revision']} · --published\n"+text
        if info and shown:text += "\n"+paging_hint(table,rows,shown,info)
        if shown:
            command = shlex.join([
                "python3", "-m", "astrid", "timelines", "visualize", str(parsed.ref),
                "--project", str(parsed.project), "--view", "contact", "--range",
                f"{shown[0]['start']:.2f}..{shown[-1]['end']:.2f}",
            ])
            text += f"\nsee these cuts: {command}"
        text += "\nper-track layer rows: --layers · SDK envelope (complete): --json"
        payload=cut_table_payload(bundle,table)
        data={**payload,"timeline_id":opened.get("timeline_id"),"revision_id":revision_id,
              "rows":shown,"text":text,"working_copy":working_copy}
    from astrid.sdk.contracts import DomainResult
    result=DomainResult.success(data)
    if parsed.json:return print_result(result,as_json=True)
    print(data.get("text", ""))
    return 0


def _presentation_from_bundle(
    bundle: Mapping[str, Any], parsed: argparse.Namespace, mode: str,
    *, revision_id: str | None,
) -> dict[str, Any]:
    from astrid.sdk.timeline_cuts import render_cut_table
    from astrid.sdk.timeline_views import render_code, render_script

    table, rows, shot_ids, window = _presentation_selection(bundle, parsed)
    if mode == "cuts":
        limit = max(1, min(int(getattr(parsed, "limit", 50) or 50), 100))
        selected = rows[:limit]
        text = render_cut_table(table, selected, title=f"Cuts · revision {revision_id or 'resolved'}")
        return {
            "kind": "cuts",
            "revision_id": revision_id,
            "total_rows": len(rows),
            "rows": selected,
            "text": text,
        }
    renderer = render_script if mode == "script" else render_code
    text = renderer(bundle, window=window, shot_ids=shot_ids)
    return {
        "kind": mode,
        "revision_id": revision_id,
        "window": list(window) if window is not None else None,
        "shot_ids": sorted(shot_ids) if shot_ids is not None else None,
        "text": text,
    }


def _show_presentation(parsed: argparse.Namespace, mode: str) -> DomainResult:
    opener = getattr(parsed.client.timelines, "open_bundle", None)
    if not callable(opener):
        from astrid.sdk.contracts import ErrorObject

        return DomainResult.failure(
            ErrorObject(
                "unavailable",
                "immutable timeline bundle presentation is unavailable",
                {"project": str(parsed.project), "timeline": str(parsed.ref)},
            )
        )
    opened = opener(parsed.project, parsed.ref, revision_id=getattr(parsed, "revision_id", None))
    if not opened.ok or not isinstance(opened.data, Mapping):
        return opened
    bundle = opened.data.get("bundle")
    if not isinstance(bundle, Mapping):
        from astrid.sdk.contracts import ErrorObject

        return DomainResult.failure(
            ErrorObject("protocol_error", "immutable timeline bundle response omitted bundle", {})
        )
    try:
        data = {
            "kind": "timeline-presentation",
            "timeline_id": opened.data.get("timeline_id"),
            "revision_id": opened.data.get("revision_id") or getattr(parsed, "revision_id", None),
            "presentation": _presentation_from_bundle(
                bundle,
                parsed,
                mode,
                revision_id=opened.data.get("revision_id") or getattr(parsed, "revision_id", None),
            ),
        }
    except (TypeError, ValueError) as exc:
        from astrid.sdk.contracts import ErrorObject

        return DomainResult.failure(ErrorObject("validation_error", str(exc), {"presentation": mode}))
    return DomainResult.success(data, receipt=opened.receipt, idempotency_key=opened.idempotency_key)


def _revision_from_outputs(outputs: Mapping[str, Any]) -> str | None:
    """Read an already-admitted revision pin from bounded result metadata."""
    for container in (outputs, outputs.get("summary"), outputs.get("inspection"), outputs.get("provenance")):
        if isinstance(container, Mapping):
            for key in ("revision_id", "head_revision_id", "parent_revision_id"):
                value = container.get(key)
                if value not in (None, ""):
                    return str(value)
    return None


def _navigation_scope(
    *, project: str | None, timeline: str | None, outputs: Mapping[str, Any],
) -> tuple[str, str]:
    """Resolve copyable navigation scope without guessing a new default."""
    containers = [outputs]
    for key in ("summary", "scope", "native_inspection", "inspection", "provenance"):
        value = outputs.get(key)
        if isinstance(value, Mapping):
            containers.append(value)

    def first(keys: tuple[str, ...], fallback: str) -> str:
        if fallback not in (None, ""):
            return str(fallback)
        for container in containers:
            for key in keys:
                value = container.get(key)
                if value not in (None, ""):
                    return str(value)
        return fallback or "<unresolved>"

    return (
        first(("project_slug", "project_id", "project"), project),
        first(("timeline_slug", "timeline_id", "timeline", "ref"), timeline),
    )


def _timeline_editing_resources() -> dict[str, Any]:
    """Locate the installed checkout recipe without depending on cwd."""
    docs_root = Path(__file__).resolve().parents[1] / "rendering" / "docs"
    guide = docs_root / "references" / "document-checkout.md"
    script = docs_root / "scripts" / "timeline_document.py"
    return {
        "guide": str(guide),
        "script": str(script),
        "workflow": ["checkout", "edit", "check", "publish"],
        "scope": "complete parent/shot/internal-timeline composition",
        "checkout_revision": "current Runtime head at checkout; historical revisions remain read-only",
    }


def _editing_navigation(
    *, project: str | None, timeline: str | None,
) -> dict[str, Any]:
    """Return one small, copyable entry point for detached JSON editing."""
    resources = _timeline_editing_resources()
    file_path = "/tmp/timeline-edit.json"
    checkout = shlex.join([
        "python3", "-m", "astrid.packs.rendering.docs.scripts.timeline_document",
        "checkout", "--project", project or "<project>", "--timeline", timeline or "<timeline>",
        "--file", file_path,
    ])
    check = shlex.join([
        "python3", "-m", "astrid.packs.rendering.docs.scripts.timeline_document",
        "check", "--file", file_path,
    ])
    publish = shlex.join([
        "python3", "-m", "astrid.packs.rendering.docs.scripts.timeline_document",
        "publish", "--file", file_path, "--idempotency-key", "<edit-key>",
    ])
    resources["commands"] = {"checkout": checkout, "check": check, "publish": publish}
    return resources


def _show_navigation_help(
    *, project: str | None, ref: str | None, parsed: argparse.Namespace, outputs: Mapping[str, Any],
) -> dict[str, Any]:
    """Offer a revision-pinned visual continuation from structural show output."""
    resolved_project, resolved_timeline = _navigation_scope(
        project=project, timeline=ref, outputs=outputs,
    )
    argv = ["python3", "-m", "astrid", "timelines", "visualize", "--project", resolved_project]
    if resolved_timeline not in (None, ""):
        argv += ["--timeline-slug", resolved_timeline]
    revision = getattr(parsed, "revision_id", None) or _revision_from_outputs(outputs)
    if revision:
        argv += ["--revision-id", str(revision)]
    for name, flag in (("occurrence", "--occurrence"), ("shot", "--shot"), ("clip", "--clip"), ("asset", "--asset"), ("range", "--range")):
        value = getattr(parsed, name, None)
        if value not in (None, ""):
            argv += [flag, str(value)]
    for track in getattr(parsed, "track", None) or []:
        argv += ["--track", str(track)]
    edit = _editing_navigation(project=resolved_project, timeline=resolved_timeline)
    return {
        "commands": {
            "visualize": shlex.join(argv),
            "controls": "python3 -m astrid timelines visualize --help",
        },
        "editing": edit,
        "authority": revision or "resolved by Runtime current head",
        "note": "The visual continuation preserves the saved revision and structural filters; checkout starts a fresh current-head editable file.",
    }


def _cmd_replace_parent_media(parsed: argparse.Namespace) -> int:
    result = parsed.client.timelines.replace_parent_media(
        parsed.project,
        parsed.ref,
        occurrence_id=parsed.occurrence_id,
        clip_id=parsed.clip_id,
        source_object_id=parsed.source_object_id,
        expected_head=parsed.expected_head,
        idempotency_key=parsed.idempotency_key,
    )
    # The authoring route necessarily compiles the complete immutable
    # parent/shot/internal-timeline closure, but that closure is an internal
    # publication payload.  Never put it on the public CLI wire: a single
    # replacement can otherwise exceed the 4 MiB JSON pipe limit even though
    # the CAS publication succeeded.  Keep the SDK result lossless for
    # programmatic callers and project only a bounded public receipt here.
    if isinstance(result, DomainResult) and result.ok and isinstance(result.data, Mapping):
        source = result.data
        compact: dict[str, Any] = {}
        for key in (
            "representation",
            "project_id",
            "timeline_id",
            "occurrence_id",
            "clip_id",
            "expected_head",
            "candidate_digest",
        ):
            if key in source:
                compact[key] = source[key]
        validation = source.get("validation")
        if isinstance(validation, Mapping):
            compact["validation"] = {
                key: validation[key]
                for key in (
                    "valid",
                    "candidate_digest",
                    "publication_digest",
                    "changed_identities",
                    "reused_identities",
                )
                if key in validation
            }
        diff = source.get("diff")
        if isinstance(diff, Mapping):
            compact["diff"] = {
                key: diff[key]
                for key in ("changed", "changed_count", "summary")
                if key in diff and not isinstance(diff[key], (list, dict))
            }
            if not compact["diff"]:
                compact.pop("diff")
        publication = source.get("publication")
        if isinstance(publication, Mapping):
            published_data = publication.get("data")
            if not isinstance(published_data, Mapping):
                published_data = publication
            publication_summary = {
                key: published_data[key]
                for key in (
                    "new_head",
                    "old_head",
                    "revision_id",
                    "parent_revision_id",
                    "replayed",
                    "status",
                )
                if key in published_data and not isinstance(published_data[key], (dict, list))
            }
            dependency_manifest = published_data.get("dependency_manifest")
            if isinstance(dependency_manifest, Mapping):
                publication_summary["dependency_counts"] = {
                    key: len(value)
                    for key, value in dependency_manifest.items()
                    if key in {"shots", "internal_timelines", "media"}
                    and isinstance(value, list)
                }
            compact["publication"] = publication_summary
        result = DomainResult.success(
            compact,
            receipt=result.receipt,
            idempotency_key=result.idempotency_key,
        )
    return print_result(result, as_json=parsed.json)


def _cmd_archive(parsed: argparse.Namespace) -> int:
    result = parsed.client.timelines.archive(
        parsed.project,
        parsed.ref,
        idempotency_key=parsed.idempotency_key,
    )
    return print_result(result, as_json=parsed.json)


def _cmd_recover(parsed: argparse.Namespace) -> int:
    result = parsed.client.timelines.recover(
        parsed.project,
        parsed.ref,
        idempotency_key=parsed.idempotency_key,
    )
    return print_result(result, as_json=parsed.json)


def _cmd_history(parsed: argparse.Namespace) -> int:
    result = parsed.client.timelines.history(parsed.project, parsed.ref)
    return print_result(result, as_json=parsed.json)


def _cmd_diff(parsed: argparse.Namespace) -> int:
    from_revision = getattr(parsed, "from_revision", None)
    to_revision = getattr(parsed, "to_revision", None)
    from_version = getattr(parsed, "from_version", None)
    to_version = getattr(parsed, "to_version", None)
    output_format = getattr(parsed, "format", None)
    as_json = output_format == "json" or bool(getattr(parsed, "json", False))

    # Integer-version diffs remain the Runtime SDK route. Revision diffs use
    # the exact immutable bundles so the editor can show cuts, script, or code.
    if from_version is not None or to_version is not None:
        result = parsed.client.timelines.diff(
            parsed.project, parsed.ref,
            from_version=from_version, to_version=to_version,
        )
        if output_format in {"readable", "details"}:
            from astrid.core.timeline.authoring_diff_format import format_authoring_revision_diff
            return print_result(
                result,
                human_renderer=lambda envelope: format_authoring_revision_diff(
                    envelope_dict(envelope)["data"], mode=output_format,
                ),
            )
        return print_result(result, as_json=True)

    if not isinstance(from_revision, str) or not from_revision.strip():
        print(
            "error validation_error: say what to compare: --from <revision-id> "
            "[--to <revision-id>] compares two saved revisions (default --to: current head)."
        )
        return 2

    opener = getattr(parsed.client.timelines, "open_bundle", None)
    if not callable(opener):
        print("error unavailable: this client cannot open timeline revisions")
        return 2
    before = opener(parsed.project, parsed.ref, revision_id=from_revision)
    if not before.ok or not isinstance(before.data, Mapping):
        return print_result(before, as_json=as_json)
    after = opener(parsed.project, parsed.ref, revision_id=to_revision)
    if not after.ok or not isinstance(after.data, Mapping):
        return print_result(after, as_json=as_json)
    before_bundle = before.data.get("bundle")
    after_bundle = after.data.get("bundle")
    if not isinstance(before_bundle, Mapping) or not isinstance(after_bundle, Mapping):
        from astrid.sdk.contracts import ErrorObject
        return print_result(
            DomainResult.failure(ErrorObject("protocol_error", "revision response omitted bundle", {})),
            as_json=as_json,
        )

    old = str(before.data.get("revision_id") or from_revision)
    new = str(after.data.get("revision_id") or to_revision or "current head")
    view = getattr(parsed, "presentation", None) or "cuts"
    if view != "cuts":
        import difflib
        from astrid.sdk.timeline_views import render_code, render_script
        render = render_script if view == "script" else render_code
        lines = difflib.unified_diff(
            render(before_bundle).splitlines(), render(after_bundle).splitlines(),
            fromfile=old, tofile=new, lineterm="", n=2,
        )
        print("\n".join(lines) or f"No differences in the {view} view.")
        return 0

    from astrid.sdk.timeline_cuts import diff_bundles, render_diff
    diff = diff_bundles(before_bundle, after_bundle)
    diff.update({
        "from_revision": old,
        "to_revision": new,
        "timeline_id": after.data.get("timeline_id"),
    })
    commands: dict[str, str] = {}
    for low, high in diff.get("windows") or []:
        for label, revision in (("before", old), ("after", new)):
            commands[f"{label} {low:g}..{high:g}"] = shlex.join([
                "python3", "-m", "astrid", "timelines", "visualize", str(parsed.ref),
                "--project", str(parsed.project), "--revision-id", revision,
                "--range", f"{low:g}..{high:g}", "--every-frames", "5",
            ])
    diff["commands"] = commands
    if as_json:
        print(json.dumps({"ok": True, "data": diff, "error": None}, indent=2, sort_keys=True))
        return 0
    text = render_diff(diff, title=f"Timeline {after.data.get('timeline_id')}: {old} → {new}")
    if commands:
        text += "\nsee it: frames of only the changed moments, before and after (no full render):"
        text += "\n" + "\n".join(f"  {label}: {command}" for label, command in commands.items())
    print(text)
    return 0


def _diff_presentation(parsed: argparse.Namespace, mode: str) -> DomainResult:
    """Present two exact immutable revisions through the released V3 helpers."""
    from_revision = getattr(parsed, "from_revision", None)
    to_revision = getattr(parsed, "to_revision", None)
    opener = getattr(parsed.client.timelines, "open_bundle", None)
    if not callable(opener):
        from astrid.sdk.contracts import ErrorObject

        return DomainResult.failure(
            ErrorObject("unavailable", "immutable revision presentation is unavailable", {})
        )
    if not all(isinstance(value, str) and value.strip() for value in (from_revision, to_revision)):
        from astrid.sdk.contracts import ErrorObject

        return DomainResult.failure(
            ErrorObject(
                "validation_error",
                f"--as {mode} requires --from-revision and --to-revision",
                {"presentation": mode},
            )
        )
    before = opener(parsed.project, parsed.ref, revision_id=from_revision)
    if not before.ok or not isinstance(before.data, Mapping):
        return before
    after = opener(parsed.project, parsed.ref, revision_id=to_revision)
    if not after.ok or not isinstance(after.data, Mapping):
        return after
    before_bundle = before.data.get("bundle")
    after_bundle = after.data.get("bundle")
    if not isinstance(before_bundle, Mapping) or not isinstance(after_bundle, Mapping):
        from astrid.sdk.contracts import ErrorObject

        return DomainResult.failure(ErrorObject("protocol_error", "immutable revision response omitted bundle", {}))
    try:
        from astrid.sdk.timeline_cuts import (
            build_cut_table,
            diff_bundles,
            render_cut_table,
            render_diff,
        )
        from astrid.sdk.timeline_views import render_code, render_script

        delta = diff_bundles(before_bundle, after_bundle)
        if mode == "cuts":
            before_table = build_cut_table(before_bundle)
            after_table = build_cut_table(after_bundle)
            text = render_diff(delta, title=f"Cut diff · {from_revision} → {to_revision}")
            presentation = {
                "kind": "cuts",
                "from_revision": from_revision,
                "to_revision": to_revision,
                "diff": delta,
                "before_text": render_cut_table(before_table),
                "after_text": render_cut_table(after_table),
                "text": text,
            }
        else:
            renderer = render_script if mode == "script" else render_code
            presentation = {
                "kind": mode,
                "from_revision": from_revision,
                "to_revision": to_revision,
                "diff": delta,
                "before_text": renderer(before_bundle),
                "after_text": renderer(after_bundle),
                "text": render_diff(delta, title=f"{mode.title()} diff · {from_revision} → {to_revision}"),
            }
    except (TypeError, ValueError) as exc:
        from astrid.sdk.contracts import ErrorObject

        return DomainResult.failure(ErrorObject("validation_error", str(exc), {"presentation": mode}))
    return DomainResult.success(
        {
            "kind": "timeline-diff-presentation",
            "timeline_id": after.data.get("timeline_id"),
            "from_revision": from_revision,
            "to_revision": to_revision,
            "presentation": presentation,
        },
        receipt=after.receipt,
        idempotency_key=after.idempotency_key,
    )
def _visualize_format_argument(value: str) -> str:
    """Validate one bounded visualization format argument."""
    values = [part.strip().lower() for part in value.split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("format must name png or md")
    invalid = sorted(set(values) - {"png", "md"})
    if invalid:
        raise argparse.ArgumentTypeError(
            f"invalid visualization format(s): {', '.join(invalid)}; choose png or md"
        )
    return ",".join(values)


def _visualization_artifact_summary(outputs: Mapping[str, Any]) -> dict[str, Any] | None:
    """Summarize repeated visualization artifacts without dropping evidence."""
    raw_artifacts = outputs.get("artifacts")
    if not isinstance(raw_artifacts, list):
        return None

    groups: dict[tuple[str, str], dict[str, Any]] = {}
    media_ids: set[str] = set()
    hashes: set[str] = set()
    for artifact in raw_artifacts:
        if not isinstance(artifact, Mapping):
            continue
        media_id = artifact.get("media_id")
        content_hash = artifact.get("content_hash")
        if isinstance(media_id, str) and media_id:
            media_ids.add(media_id)
        if isinstance(content_hash, str) and content_hash:
            hashes.add(content_hash)
        if not (
            isinstance(media_id, str)
            and media_id
            and isinstance(content_hash, str)
            and content_hash
        ):
            continue
        key = (media_id, content_hash)
        group = groups.setdefault(
            key,
            {"media_id": media_id, "content_hash": content_hash, "count": 0, "labels": []},
        )
        group["count"] += 1
        label = artifact.get("label")
        if isinstance(label, str) and label:
            group["labels"].append(label)

    duplicate_groups = [group for group in groups.values() if group["count"] > 1]
    duplicate_groups.sort(key=lambda group: (-group["count"], group["media_id"]))
    return {
        "artifact_count": len(raw_artifacts),
        "unique_media_count": len(media_ids),
        "unique_content_hash_count": len(hashes),
        "duplicate_reference_count": sum(group["count"] - 1 for group in duplicate_groups),
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_groups": duplicate_groups,
    }


def _cmd_visualize(parsed: argparse.Namespace) -> int:
    """Run visualization through the public SDK and product output layer."""
    from astrid.sdk.contracts import DomainResult, ErrorObject
    from astrid.packs.rendering.actions.timeline_visualize.inspection_contract import inspection_options
    human_outputs: Mapping[str, Any] | None = None

    # Normalize repeatable and comma-separated spellings before the one
    # canonical SDK call. Inputs remain render-free; auto always composes
    # requested frames from the exact saved revision.
    formats = [
        item.strip().lower()
        for value in (parsed.formats or ["png", "md"])
        for item in str(value).split(",")
        if item.strip()
    ]
    inputs: dict[str, Any] = {"formats": formats}
    timeline_slug = parsed.timeline_slug or parsed.timeline_ref
    for name in (
        "shot", "sample", "every", "every_frames", "include_cuts",
        "render_run", "columns", "page_size", "resolution", "include_media",
        "range", "at", "frame", "clip", "asset", "context", "neighbors", "show", "hide",
        "track", "detail", "occurrence", "revision_id", "cut", "layers", "beats",
        "frame_budget", "preset", "window_s", "rules", "cuts", "preview",
        "before_revision_id", "after_revision_id",
    ):
        value = getattr(parsed, name, None)
        if value not in (None, "", []):
            inputs[name] = value
    # ``overview`` is a donor-facing semantic spelling; the admitted V3
    # action name is ``contact``.  Diff is a separate immutable-bundle
    # presentation and must carry both explicit revision selectors.
    inputs["view"] = "contact" if parsed.view == "overview" else parsed.view
    if "layers" in inputs:
        inputs["layers"] = [
            part.strip()
            for item in inputs["layers"]
            for part in str(item).split(",")
            if part.strip()
        ]
    from astrid.packs.timeline.cli_verify import with_labels_layer
    layers = with_labels_layer(inputs.get("layers"), parsed.labels)
    if layers is not None:
        inputs["layers"] = layers
    if timeline_slug not in (None, ""):
        inputs["timeline_slug"] = timeline_slug
    # The public text and visual routes use the same bounded selector
    # normalizer. Preserve all existing input spellings, but canonicalize the
    # occurrence identity before crossing the SDK boundary.
    inputs["occurrence"] = inspection_options({"occurrence": getattr(parsed, "occurrence", None)})["occurrence"]
    if inputs["occurrence"] is None:
        inputs.pop("occurrence")
    shown_components = inputs.get("show") or []
    hidden_components = inputs.get("hide") or []
    if "output" in hidden_components or (shown_components and "output" not in shown_components):
        mode = "inputs"
    else:
        mode = getattr(parsed, "mode", "auto")
    validation_error = None
    revision_selectors = ("before_revision_id", "after_revision_id")
    if inputs["view"] == "diff":
        missing = [name for name in revision_selectors if not str(inputs.get(name) or "").strip()]
        if not isinstance(parsed.project, str) or not parsed.project.strip():
            validation_error = ErrorObject(
                "validation_error",
                "view=diff requires an explicit --project",
                {"field": "project", "view": "diff"},
            )
        elif not isinstance(timeline_slug, str) or not timeline_slug.strip():
            validation_error = ErrorObject(
                "validation_error",
                "view=diff requires an explicit timeline slug or positional timeline",
                {"field": "timeline", "view": "diff"},
            )
        elif missing:
            validation_error = ErrorObject(
                "validation_error",
                "view=diff requires both --before-revision-id and --after-revision-id",
                {"fields": missing, "view": "diff"},
            )
        elif getattr(parsed, "revision_id", None) not in (None, ""):
            validation_error = ErrorObject(
                "validation_error",
                "view=diff uses only the explicit before/after revision selectors",
                {"field": "revision_id", "view": "diff"},
            )
        elif mode == "inputs":
            validation_error = ErrorObject(
                "validation_error",
                "render-free input mode supports only view=filmstrip; diff requires admitted immutable bundles",
                {"field": "mode", "view": "diff"},
            )
    elif any(str(inputs.get(name) or "").strip() for name in revision_selectors):
        validation_error = ErrorObject(
            "validation_error",
            "before/after revision selectors are valid only with view=diff",
            {"fields": list(revision_selectors), "view": inputs["view"]},
        )
    # --out is an export of the settled view (the managed cache stays the source), never the
    # capture's working directory.
    export_dir = getattr(parsed, "out", None)
    if validation_error is not None:
        result = DomainResult.failure(validation_error)
    else:
        result = parsed.client.timelines.visualize(
            parsed.project,
            timeline_slug,
            mode=mode,
            options=inputs,
            revision_id=getattr(parsed, "revision_id", None),
        )
    if isinstance(result, DomainResult):
        # Native Runtime views are already typed DomainResults and deliberately
        # have no task/run identity. Keep the CLI envelope compatible while
        # preserving Runtime-owned artifact/inspection data verbatim.
        if result.ok:
            outputs = dict(result.data) if isinstance(result.data, Mapping) else {"data": result.data}
            summary = _visualization_artifact_summary(outputs)
            if summary is not None:
                outputs["artifact_summary"] = summary
            outputs["navigation"] = _visualization_navigation_help(
                project=parsed.project,
                inputs=inputs,
                outputs=outputs,
            )
            if export_dir:
                outputs["exported"] = _export_visualization(outputs, export_dir)
            human_outputs = outputs
            envelope = DomainResult.success(
                {
                    "capability_id": "timelines.visualize",
                    "run_id": None,
                    "kernel_run_id": None,
                    "kernel_task_id": None,
                    "kernel_attempt_id": None,
                    "manifest_path": None,
                    "outputs": outputs,
                },
                receipt=result.receipt,
                idempotency_key=result.idempotency_key,
            )
        else:
            envelope = result
    elif result.ok:
        outputs = result.outputs
        if isinstance(outputs, Mapping):
            outputs = dict(outputs)
            summary = _visualization_artifact_summary(outputs)
            if summary is not None:
                outputs["artifact_summary"] = summary
            outputs["navigation"] = _visualization_navigation_help(
                project=parsed.project,
                inputs=inputs,
                outputs=outputs,
            )
            if export_dir:
                outputs["exported"] = _export_visualization(outputs, export_dir)
            human_outputs = outputs
        envelope = DomainResult.success(
            {
                "capability_id": result.capability_id,
                "run_id": result.run_id,
                "kernel_run_id": result.kernel_run_id,
                "kernel_task_id": result.kernel_task_id,
                "kernel_attempt_id": result.kernel_attempt_id,
                "manifest_path": result.manifest_path,
                "outputs": outputs,
            }
        )
    else:
        detail = dict(result.error or {})
        category = str(detail.get("sdk_category") or "invocation")
        envelope = DomainResult.failure(
            ErrorObject(
                code="validation_error" if category == "validation" else "invocation_error",
                message=str(detail.get("message") or "timeline visualization failed"),
                details={
                    "sdk_error": detail.get("sdk_error"),
                    "sdk_category": category,
                    "validation": detail.get("validation"),
                    "run_id": result.run_id,
                    "kernel_run_id": result.kernel_run_id,
                    "kernel_task_id": result.kernel_task_id,
                    "kernel_attempt_id": result.kernel_attempt_id,
                },
            )
        )
    exit_status = print_result(envelope, as_json=parsed.json)
    if result.ok and not parsed.json:
        if human_outputs is not None:
            _print_visualization_navigation(human_outputs)
            exported = human_outputs.get("exported")
            if exported:
                print(f"exported: {exported['dir']}  ({len(exported['pages'])} page(s), {len(exported['frames'])} frame(s))")
    return exit_status


def _export_visualization(outputs: Mapping[str, Any], out_dir: str) -> dict[str, Any]:
    """``--out DIR``: copy the view's page(s) and its raw frames (with frame-index.json) to DIR."""
    import shutil

    dest = Path(out_dir).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    pages = [str(page) for page in outputs.get("pages") or [] if page]
    primary = outputs.get("primary_page") or outputs.get("png")
    if primary and str(primary) not in pages:
        pages.insert(0, str(primary))
    copied_pages, copied_frames = [], []
    for page in pages:
        source = Path(page)
        if source.is_file():
            shutil.copy2(source, dest / source.name)
            copied_pages.append(str(dest / source.name))
    view_dir = Path(pages[0]).parent if pages else None
    if view_dir is not None and (view_dir / "frames").is_dir():
        (dest / "frames").mkdir(exist_ok=True)
        for frame in sorted((view_dir / "frames").iterdir()):
            if frame.is_file() and frame.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                shutil.copy2(frame, dest / "frames" / frame.name)
                copied_frames.append(str(dest / "frames" / frame.name))
        if (view_dir / "frame-index.json").is_file():
            shutil.copy2(view_dir / "frame-index.json", dest / "frame-index.json")
    return {"dir": str(dest), "pages": copied_pages, "frames": copied_frames}


def _visualization_navigation_help(
    *, project: str | None, inputs: Mapping[str, Any], outputs: Mapping[str, Any],
) -> dict[str, Any]:
    """Expose copyable zoom/sampling/navigation guidance in CLI results."""
    resolved_project, resolved_timeline = _navigation_scope(
        project=project, timeline=inputs.get("timeline_slug"), outputs=outputs,
    )
    identity = [
        "python3", "-m", "astrid", "timelines", "visualize",
        "--project", resolved_project,
    ]
    timeline = resolved_timeline
    if timeline not in (None, ""):
        identity += ["--timeline-slug", str(timeline)]
    render_run = inputs.get("render_run")
    if render_run not in (None, ""):
        identity += ["--render-run", str(render_run)]
    revision_id = inputs.get("revision_id") or _revision_from_outputs(outputs)
    if revision_id not in (None, ""):
        identity += ["--revision-id", str(revision_id)]
    if inputs.get("view") == "diff":
        for name, flag in (("before_revision_id", "--before-revision-id"), ("after_revision_id", "--after-revision-id")):
            if inputs.get(name) not in (None, ""):
                identity += [flag, str(inputs[name])]

    def tokens(value: Any) -> list[str]:
        if isinstance(value, (list, tuple)):
            return [str(item) for item in value if str(item)]
        return [str(value)] if value not in (None, "") else []

    def base(*, components: bool = True, sampling: bool = True, resolution: bool = True) -> list[str]:
        argv = identity + ["--view", str(inputs.get("view") or "filmstrip")]
        if components:
            shown = tokens(inputs.get("show"))
            hidden = tokens(inputs.get("hide"))
            if shown:
                argv += ["--show", ",".join(shown)]
            if hidden:
                argv += ["--hide", ",".join(hidden)]
            for track in tokens(inputs.get("track")):
                argv += ["--track", track]
            for key, flag in (("shot", "--shot"), ("clip", "--clip"), ("occurrence", "--occurrence"), ("asset", "--asset")):
                value = inputs.get(key)
                if value not in (None, ""):
                    argv += [flag, str(value)]
        if inputs.get("detail"):
            argv += ["--detail"]
        if inputs.get("sample") not in (None, "", "interval"):
            argv += ["--sample", str(inputs["sample"])]
        if inputs.get("include_cuts"):
            argv += ["--include-cuts"]
        if inputs.get("columns") not in (None, ""):
            argv += ["--columns", str(inputs["columns"])]
        if inputs.get("page_size") not in (None, ""):
            argv += ["--page-size", str(inputs["page_size"])]
        if sampling:
            range_value = inputs.get("range")
            if isinstance(range_value, (list, tuple)) and len(range_value) == 2:
                range_value = f"{range_value[0]}..{range_value[1]}"
            if range_value not in (None, ""):
                argv += ["--range", str(range_value)]
            if inputs.get("at") not in (None, ""):
                argv += ["--at", str(inputs["at"])]
            if inputs.get("frame") not in (None, ""):
                argv += ["--frame", str(inputs["frame"])]
            if inputs.get("every") not in (None, ""):
                argv += ["--every", str(inputs["every"])]
            if inputs.get("every_frames") not in (None, ""):
                argv += ["--every-frames", str(inputs["every_frames"])]
        if resolution and inputs.get("resolution") not in (None, ""):
            value = inputs["resolution"]
            if isinstance(value, (list, tuple)) and len(value) == 2:
                value = f"{value[0]}x{value[1]}"
            argv += ["--resolution", str(value)]
        return argv

    # Build replacement commands from a clean base so mutually-exclusive
    # selectors (show/hide, every/every-frames, range/at) never duplicate.
    input_only = base(components=False, sampling=True, resolution=False) + [
        "--show", "inputs", "--hide", "output"
    ]
    clean = base(sampling=False, resolution=False)
    zoom_detail = [] if inputs.get("detail") else ["--detail"]
    pages = outputs.get("pages")
    primary_page = pages[0] if isinstance(pages, list) and pages else outputs.get("png")
    manifest_ref = outputs.get("manifest_path") or "MANIFEST"
    inspect_base = ["python3", "-m", "astrid", "timelines", "inspect", "--manifest", str(manifest_ref)]
    output_components = outputs.get("components")
    if not isinstance(output_components, (list, tuple)):
        surface = outputs.get("static_surface")
        output_components = surface.get("components") if isinstance(surface, Mapping) else None
    effective_components = tokens(output_components)
    paired = (
        "output" in effective_components and "inputs" in effective_components
    ) or (
        not inputs.get("show") and not inputs.get("hide")
    )
    page_status = None
    if paired and isinstance(pages, list) and len(pages) > 1:
        page_status = f"Paired view generated {len(pages)} bite-sized pages; open them in numbered order."
    show_range = _visualization_show_range(inputs=inputs, outputs=outputs)
    show_selectors = [
        [flag, str(inputs[name])]
        for name, flag in (
            ("occurrence", "--occurrence"),
            ("shot", "--shot"),
            ("clip", "--clip"),
            ("asset", "--asset"),
        )
        if inputs.get(name) not in (None, "")
    ]
    if show_range is not None:
        show_selectors.append(["--range", show_range])
    show_command = shlex.join(
        [
            "python3", "-m", "astrid", "timelines", "show",
            "--project", resolved_project,
            *([str(timeline)] if timeline not in (None, "") else []),
            *(["--revision-id", str(revision_id)] if revision_id not in (None, "") else []),
            *sum(show_selectors, []),
            *sum((["--track", track] for track in tokens(inputs.get("track"))), []),
        ]
    )
    return {
        "primary_page": primary_page,
        "pages": pages,
        "markdown": outputs.get("markdown"),
        "inspection": shlex.join(inspect_base + ["--section", "summary"]),
        "editing": _editing_navigation(project=resolved_project, timeline=timeline),
        "status": page_status,
        "keyboard": [
            "Open the primary PNG page for visual inspection; use the bounded inspect command for exact card, placement, lane, or timing lookup.",
            "Use the rerun commands below to zoom, change sampling intervals, or narrow to input lanes.",
        ],
        "filters": [
            "Use Shot, Track, From/To, Samples, and Density by rerunning with the matching flags.",
            "Density only reduces captured frames; rerun for finer samples.",
        ],
        "commands": {
            "rerun": shlex.join(base()),
            "visualize": shlex.join(base()),
            "show": show_command,
            "controls": "python3 -m astrid timelines visualize --help",
            "zoom": shlex.join(clean + ["--range", "START..END", "--every", "0.25", *zoom_detail]),
            "interval_seconds": shlex.join(clean + ["--every", "1"]),
            "interval_frames": shlex.join(clean + ["--every-frames", "12"]),
            "exact_frame": shlex.join(clean + ["--frame", "FRAME"]),
            "resolution": shlex.join(base(resolution=False) + ["--resolution", "960x540"]),
            "inputs_only": shlex.join(input_only),
            "pages": shlex.join(clean + ["--columns", "5", "--page-size", "10"]),
            "inspect_summary": shlex.join(inspect_base + ["--section", "summary"]),
            "inspect_cards": shlex.join(inspect_base + ["--section", "cards"]),
            "inspect_placements": shlex.join(inspect_base + ["--section", "placements"]),
            "inspect_audio": shlex.join(inspect_base + ["--section", "audio"]),
            "inspect_boundaries": shlex.join(inspect_base + ["--section", "boundaries"]),
        },
        "notes": [
            "--range uses a half-open START..END seconds window.",
            "--every and --every-frames are mutually exclusive.",
            "--columns/--page-size change static layout; --track narrows input lanes.",
            "paired output+inputs pages show one row by default (five cards across); use --columns 6 for six across, or pass --page-size N explicitly for a denser two-row page.",
        ],
    }


def _fractional_seconds(value: Any) -> Fraction:
    """Parse the public seconds spelling without introducing float drift."""
    parts = str(value).split(":")
    if not 1 <= len(parts) <= 3:
        raise ValueError("invalid time")
    result = Fraction(0)
    for part in parts:
        result = result * 60 + Fraction(str(part))
    if result < 0:
        raise ValueError("invalid time")
    return result


def _visualization_fps(outputs: Mapping[str, Any]) -> Fraction:
    """Find the admitted frame clock, falling back to the public default."""
    containers: list[Mapping[str, Any]] = [outputs]
    for key in ("provenance", "inspection", "frame_index"):
        value = outputs.get(key)
        if isinstance(value, Mapping):
            containers.append(value)
            nested = value.get("provenance")
            if isinstance(nested, Mapping):
                containers.append(nested)
    for container in containers:
        raw = container.get("fps_rational")
        if isinstance(raw, (list, tuple)) and len(raw) == 2:
            try:
                fps = Fraction(int(raw[0]), int(raw[1]))
            except (TypeError, ValueError, ZeroDivisionError):
                continue
            if fps > 0:
                return fps
    frame_index = outputs.get("frame_index")
    frame_index_paths: list[Path] = []
    if isinstance(frame_index, str) and frame_index:
        frame_index_paths.append(Path(frame_index).expanduser())
        pack_root = outputs.get("pack_root")
        if isinstance(pack_root, str) and pack_root:
            candidate = Path(pack_root).expanduser() / frame_index
            if candidate not in frame_index_paths:
                frame_index_paths.append(candidate)
        manifest_path = outputs.get("manifest_path")
        if isinstance(manifest_path, str) and manifest_path:
            candidate = Path(manifest_path).expanduser().parent / frame_index
            if candidate not in frame_index_paths:
                frame_index_paths.append(candidate)
    for path in frame_index_paths:
        try:
            frame_index_data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, TypeError, ValueError):
            continue
        if isinstance(frame_index_data, Mapping):
            provenance = frame_index_data.get("provenance")
            if isinstance(provenance, Mapping):
                raw = provenance.get("fps_rational")
                if isinstance(raw, (list, tuple)) and len(raw) == 2:
                    try:
                        fps = Fraction(int(raw[0]), int(raw[1]))
                    except (TypeError, ValueError, ZeroDivisionError):
                        continue
                    if fps > 0:
                        return fps
    return Fraction(30, 1)


def _fraction_text(value: Fraction) -> str:
    """Serialize a time rational without moving a half-open boundary."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _visualization_show_range(
    inputs: Mapping[str, Any], *, outputs: Mapping[str, Any],
) -> str | None:
    """Project visualize's time selectors onto show's half-open range grammar."""
    range_value = inputs.get("range")
    if isinstance(range_value, (list, tuple)) and len(range_value) == 2:
        return f"{range_value[0]}..{range_value[1]}"
    if range_value not in (None, ""):
        return str(range_value)

    fps = _visualization_fps(outputs)
    frame = inputs.get("frame")
    if frame not in (None, ""):
        try:
            start = Fraction(int(frame), 1) / fps
        except (TypeError, ValueError, ZeroDivisionError):
            return None
        end = Fraction(int(frame) + 1, 1) / fps
    elif inputs.get("at") not in (None, ""):
        try:
            center = _fractional_seconds(inputs["at"])
            # A timestamp without explicit context is still an exact frame
            # request for visualization; an explicit context is preserved as
            # the broader structural show window.
            radius = (
                _fractional_seconds(inputs["context"])
                if inputs.get("context") not in (None, "")
                else Fraction(1, 1) / fps
            )
        except (TypeError, ValueError, ZeroDivisionError):
            return None
        start, end = max(Fraction(0), center - radius), center + radius
    else:
        return None

    return f"{_fraction_text(start)}..{_fraction_text(end)}"


def _print_visualization_navigation(outputs: Mapping[str, Any]) -> None:
    """Print short, copyable navigation hints in human CLI mode.

    ``--json`` already carries the structured ``outputs.navigation`` object;
    human mode should still be actionable without requiring the operator to
    rerun the command with another flag.
    """
    navigation = outputs.get("navigation")
    if not isinstance(navigation, Mapping):
        return
    print("navigation:")
    primary_page = navigation.get("primary_page")
    if primary_page:
        print(f"  open PNG: {primary_page}")
    inspection = navigation.get("inspection")
    if inspection:
        print(f"  inspect (bounded): {inspection}")
    status = navigation.get("status")
    if status:
        print(f"  status: {status}")
    footer: list[str] = []
    # The current command is already visible above. Keep the human footer to
    # the sibling view, controls, and editing entry points; JSON retains the
    # full rerun/exact-frame command catalog.
    _append_navigation_footer(footer, navigation, include_visualize=False)
    for line in footer:
        print(f"  {line}")


def _cmd_inspect(parsed: argparse.Namespace) -> int:
    from astrid.packs.rendering.actions.timeline_visualize.inspection_contract import inspect_filmstrip

    result = inspect_filmstrip(parsed.manifest, section=parsed.section, limit=parsed.limit, cursor=parsed.cursor,
                              frame=parsed.frame, card=parsed.card, shot=parsed.shot, occurrence=parsed.occurrence,
                              clip=parsed.clip, track=parsed.track, asset=parsed.asset, range_value=parsed.range_value)
    # This exact compact serialization is included in the inspector's byte cap.
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":")))
    return 0 if result["ok"] else 1


def _configure_inspect(subparser: argparse.ArgumentParser) -> None:
    from astrid.packs.rendering.actions.timeline_visualize.inspection_contract import INSPECTION_SECTIONS

    subparser.description = "Inspect a verified materialized filmstrip offline; no runtime or render admission. Responses are capped at 8 KiB."
    subparser.add_argument("--manifest", required=True, help="Materialized filmstrip manifest.json; bundle members are verified before reading.")
    subparser.add_argument("--section", default="summary", help="Named section: " + ", ".join(INSPECTION_SECTIONS))
    subparser.add_argument("--limit", type=int, default=10, help="Records per response: 1–50, default 10; byte cap may reduce the page.")
    subparser.add_argument("--cursor", default=None, help="Opaque cursor from this bundle and identical query.")
    subparser.add_argument("--frame", type=int, default=None, help="Exact decoded frame number.")
    for selector in ("card", "shot", "occurrence", "clip", "track", "asset"):
        subparser.add_argument("--" + selector, default=None, help="Exact " + selector + " identity (shot also accepts an exact name).")
    subparser.add_argument("--range", dest="range_value", default=None, help="Half-open START..END seconds window.")
    subparser.add_argument("--json", action="store_true", help="Compact JSON envelope is always used.")
    subparser.set_defaults(handler=_cmd_inspect)


def offline_inspect_main(args: list[str]) -> int:
    """Separate parser keeps argument errors bounded and skips runtime startup."""
    class OfflineParser(argparse.ArgumentParser):
        def error(self, message):
            raise ValueError("invalid_arguments")

    parser = OfflineParser(prog="astrid timelines inspect")
    _configure_inspect(parser)
    try:
        return _cmd_inspect(parser.parse_args(args))
    except ValueError:
        from astrid.packs.rendering.actions.timeline_visualize.inspection_contract import _inspection_error
        print(json.dumps(_inspection_error("invalid_arguments"), separators=(",", ":")))
        return 2


def _cmd_render(parsed: argparse.Namespace) -> int:
    """Render one kernel timeline through the shared runtime scope resolver."""
    from astrid.sdk.contracts import ErrorObject

    inputs: dict[str, Any] = {}
    if parsed.ref not in (None, ""):
        inputs["timeline_ref"] = parsed.ref
    for name in ("expected_version", "output_name", "profile", "review"):
        value = getattr(parsed, name, None)
        if value not in (None, ""):
            inputs[name] = value
    if parsed.backend not in (None, ""):
        # ``--backend`` is the product-language spelling.  The rendering
        # executor's stable input/CLI contract calls this value ``selector``;
        # forwarding it as ``backend`` made the public option silently inert
        # because the manifest has no such input port.
        inputs["selector"] = parsed.backend
    result = parsed.client.invoke_result(
        "rendering.render",
        kind="executor",
        project=parsed.project,
        inputs=inputs,
        wait=parsed.wait,
        timeout_seconds=parsed.timeout_seconds,
    )
    if result.ok:
        run_id = result.kernel_run_id or result.run_id
        task_id = result.kernel_task_id
        handoff = (
            task_handoff(project=parsed.project, task_id=task_id, run_id=run_id)
            if task_id
            else {}
        )
        envelope = DomainResult.success(
            {
                "capability_id": result.capability_id,
                "run_id": result.run_id,
                "kernel_run_id": result.kernel_run_id,
                "kernel_task_id": result.kernel_task_id,
                "kernel_attempt_id": result.kernel_attempt_id,
                "state": str((result.raw_result or {}).get("state") or ("completed" if parsed.wait else "admitted")),
                "handoff": handoff,
                "outputs": result.outputs,
                **_render_video_handle(result, parsed.project),
            }
        )
    else:
        detail = dict(result.error or {})
        category = str(detail.get("sdk_category") or "invocation")
        task_id = result.kernel_task_id
        run_id = result.kernel_run_id or result.run_id
        handoff = task_handoff(project=parsed.project, task_id=task_id, run_id=run_id) if task_id else {}
        envelope = DomainResult.failure(
            ErrorObject(
                code="validation_error" if category == "validation" else "invocation_error",
                message=str(detail.get("message") or "timeline render failed"),
                details={
                    "sdk_error": detail.get("sdk_error"),
                    "sdk_category": category,
                    "validation": detail.get("validation"),
                    "run_id": result.run_id,
                    "kernel_run_id": result.kernel_run_id,
                    "kernel_task_id": result.kernel_task_id,
                    "kernel_attempt_id": result.kernel_attempt_id,
                    "state": (result.raw_result or {}).get("state"),
                    "handoff": handoff,
                },
            )
        )
    if parsed.json or not envelope.ok:
        return print_result(envelope, as_json=parsed.json)
    data = envelope.data
    assert isinstance(data, Mapping)
    print(f"render {data['state']}")
    durable_run_id = data.get("kernel_run_id") or data.get("run_id")
    if durable_run_id:
        print(f"run: {durable_run_id}")
    if data.get("kernel_task_id"):
        print(f"task: {data['kernel_task_id']}")
    handoff = data.get("handoff")
    if isinstance(handoff, Mapping):
        if handoff.get("follow"):
            print(f"follow: {handoff['follow']}")
        if handoff.get("inspect"):
            print(f"inspect: {handoff['inspect']}")
        if handoff.get("events"):
            print(f"events: {handoff['events']}")
        if handoff.get("open"):
            print(f"open: {handoff['open']}")
        if handoff.get("recent"):
            print(f"recent: {handoff['recent']}")
    outputs = data.get("outputs")
    if data.get("state") == "completed" and isinstance(outputs, Mapping):
        artifacts = outputs.get("artifacts")
        if isinstance(artifacts, list):
            for artifact in artifacts:
                if isinstance(artifact, str):
                    print(f"output: {artifact}")
                elif isinstance(artifact, Mapping):
                    location = next(
                        (artifact.get(key) for key in ("url", "path", "locator", "object_id") if artifact.get(key)),
                        None,
                    )
                    if location:
                        print(f"output: {location}")
        if data.get("video"):
            print(f"video: {data['video']}   (export: {data['export']})")
    return 0


def _render_video_handle(result: Any, project: Any) -> dict[str, str]:
    """The film's handle and its export command (users guessed run:R/output#0; the port is video)."""
    run_id = getattr(result, "kernel_run_id", None) or getattr(result, "run_id", None)
    outputs = getattr(result, "outputs", None)
    for row in (outputs.get("managed_outputs") or []) if isinstance(outputs, Mapping) else []:
        if isinstance(row, Mapping) and str(row.get("output_port")) == "video" and run_id:
            handle = f"run:{run_id}/video#{row.get('ordinal') or 0}"
            return {"video": handle, "export": f"media open {handle} --project {project} --to FILE.mp4"}
    return {}


# -- parser ----------------------------------------------------------------


def _configure_create(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "timeline_id",
        nargs="?",
        default=None,
        help=(
            "New timeline id (ULID). Omit to generate one; the id is printed "
            "in the result and is what show/checkout/render accept."
        ),
    )
    _add_project_arg(subparser)
    subparser.add_argument(
        "--canvas",
        type=_parse_canvas,
        default=(1920, 1080),
        help="Canvas size WIDTHxHEIGHT (default 1920x1080).",
    )
    subparser.add_argument(
        "--fps",
        type=_positive_int,
        default=30,
        help="Canvas frame rate (default 30).",
    )
    _add_idempotency_key(subparser)
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_create)


def _configure_list(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser, required=False)
    subparser.add_argument(
        "--include-archived",
        dest="include_archived",
        action="store_true",
        help="Include archived timelines and their archived_at state.",
    )
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_list)


def _configure_show(subparser: argparse.ArgumentParser) -> None:
    subparser.epilog = (
        "Next: use `timelines visualize` for composed pixels. For edits, use the "
        "timeline_editing document-checkout recipe (checkout → edit → check → publish). "
        "Use `timelines visualize --help` for the visual controls."
    )
    _add_project_arg(subparser, required=False)
    subparser.add_argument(
        "ref", nargs="?", default=None,
        help="Optional timeline UUID, ULID, or slug; omit to use the project's default timeline.",
    )
    subparser.add_argument(
        "--summary",
        action="store_true",
        help="Presentation flag for the canonical bounded inspection (no legacy document).",
    )
    subparser.add_argument(
        "--as",
        dest="presentation",
        choices=("cuts", "script", "code"),
        default=None,
        help="Present the pinned immutable authoring bundle as cuts, script, or code.",
    )
    subparser.add_argument(
        "--occurrence",
        default=None,
        help="Restrict the bounded inspection projection to one exact authored occurrence id.",
    )
    subparser.add_argument("--clip", default=None, help="Restrict the inspection projection to one authored clip id.")
    subparser.add_argument("--shot", default=None, help="Restrict the inspection projection to one authored shot id.")
    subparser.add_argument("--track", action="append", default=None, help="Restrict the inspection projection to one or more tracks.")
    subparser.add_argument("--asset", default=None, help="Restrict the inspection projection to one canonical asset key.")
    subparser.add_argument("--range", dest="range", default=None, help="Half-open START..END seconds window.")
    subparser.add_argument("--limit", type=int, default=50, help="Maximum bounded inspection rows (1–100).")
    subparser.add_argument("--cursor", default=None, help="Continue a bounded inspection page from its cursor.")
    subparser.add_argument("--revision-id", default=None, help="Inspect an exact immutable timeline revision.")
    subparser.add_argument("--detail", action="store_true", default=False, help="Include full bounded text for selected clips.")
    subparser.add_argument("--layers", action="store_true", default=False,
                           help="Use the bounded per-track Runtime inspection projection.")
    # ``show`` is the human inspection route by default. Machine callers use
    # the explicit stable envelope switch and keep the SDK shape unchanged.
    _add_json_flag(subparser, default=False)
    subparser.set_defaults(handler=_cmd_show)


def _cmd_script(parsed: argparse.Namespace) -> int:
    return print_result(parsed.client.timelines.script(
        parsed.project, parsed.ref, revision_id=parsed.revision,
        occurrence=parsed.occurrence, kind=parsed.kind,
    ), as_json=parsed.json)


def _configure_script(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser, required=False)
    subparser.add_argument("ref", nargs="?", default=None)
    subparser.add_argument("--revision", default=None, help="Exact immutable parent revision; defaults to the current head.")
    subparser.add_argument("--occurrence", default=None, help="Read one exact placed occurrence.")
    subparser.add_argument("--kind", default="voiceover_script")
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_script)


def _configure_replace_parent_media(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline UUID, ULID, or slug.")
    subparser.add_argument("--occurrence-id", required=True, help="Exact parent-composition occurrence to edit.")
    subparser.add_argument("--clip-id", required=True, help="Exact internal-timeline clip id to replace.")
    subparser.add_argument("--source-object-id", required=True, help="Admitted project-owned media digest/object id.")
    subparser.add_argument(
        "--expected-head",
        required=True,
        help="Exact parent-composition revision id read from the target; stale heads fail closed.",
    )
    _add_idempotency_key(subparser)
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_replace_parent_media)


def _configure_archive(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline UUID, ULID, or slug.")
    _add_idempotency_key(subparser)
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_archive)


def _configure_recover(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument(
        "ref",
        help="Timeline UUID, ULID, or slug from list --include-archived.",
    )
    _add_idempotency_key(subparser)
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_recover)


def _configure_history(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline UUID, ULID, or slug.")
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_history)


def _configure_diff(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline UUID, ULID, or slug.")
    subparser.add_argument("--from", "--from-revision", dest="from_revision",
                           help="Exact immutable parent revision before the batch.")
    subparser.add_argument("--to", "--to-revision", dest="to_revision",
                           help="Exact immutable parent revision after the batch.")
    subparser.add_argument("--from-version", type=int, help="Explicit legacy integer version (not a canonical parent revision).")
    subparser.add_argument("--to-version", type=int, help="Explicit legacy integer version (not a canonical parent revision).")
    output = subparser.add_mutually_exclusive_group()
    output.add_argument("--format", choices=("readable", "details", "json"),
                        help="Group authored changes, show every raw detail, or print the exact SDK envelope (default: json).")
    output.add_argument("--json", dest="format", action="store_const", const="json",
                        help="Print the exact SDK envelope; equivalent to --format json (default).")
    subparser.add_argument(
        "--as",
        dest="presentation",
        choices=("cuts", "script", "code"),
        default=None,
        help="Present exact --from-revision/--to-revision bundles as cuts, script, or code.",
    )
    subparser.set_defaults(handler=_cmd_diff, format=None, json=False)


def _configure_visualize(subparser: argparse.ArgumentParser) -> None:
    subparser.epilog = (
        "Next: use `timelines show` for authored rows and timing. For edits, use the "
        "timeline_editing document-checkout recipe (checkout → edit → check → publish). "
        "Use this help page for component, sampling, frame, and resolution controls."
    )
    _add_project_arg(subparser, required=False)
    subparser.add_argument(
        "timeline_ref", nargs="?", default=None,
        help="Optional positional timeline slug, UUID, or ULID (prefer --timeline-slug).",
    )
    subparser.add_argument(
        "--timeline-slug",
        default=None,
        help="Timeline slug, UUID, or ULID; omit to use the project default.",
    )
    subparser.add_argument(
        "--shot", default=None,
        help=(
            "Focus an authored shot id or exact name; use 'first' or a positive "
            "one-based authored-order ordinal (for example 1) for friendly shot selection."
        ),
    )
    subparser.add_argument("--range", dest="range", default=None, help="Zoom to a closed-open START..END seconds window.")
    subparser.add_argument("--at", default=None, help="Focus a timestamp.")
    subparser.add_argument("--frame", type=int, default=None, help="Capture one exact rendered frame number.")
    subparser.add_argument("--revision-id", default=None, help="Capture/inspect an exact immutable timeline revision.")
    subparser.add_argument("--clip", default=None, help="Focus an authored clip id.")
    subparser.add_argument("--occurrence", default=None, help="Focus an exact authored shot occurrence id.")
    subparser.add_argument("--asset", default=None, help="Focus a canonical asset key.")
    subparser.add_argument(
        "--show", action="append", default=None, metavar="COMPONENT[,COMPONENT...]",
        help=(
            "Add synchronized components: inputs, output, text, or audio "
            "(default composed view: output with synchronized inputs, text, and audio; "
            "use --hide inputs for output-only)."
        ),
    )
    subparser.add_argument(
        "--hide", action="append", default=None, metavar="COMPONENT[,COMPONENT...]",
        help="Hide components from the resolved surface.",
    )
    subparser.add_argument(
        "--track", action="append", default=None, metavar="TRACK_ID",
        help="Restrict input lanes; repeat for multiple tracks.",
    )
    subparser.add_argument(
        "--detail", action="store_true", default=None,
        help="Use enlarged frame, waveform, and text panels; combine with --range/--shot for a focused inspection.",
    )
    subparser.add_argument("--context", type=float, default=None, help="Context seconds around a focus.")
    subparser.add_argument("--neighbors", type=int, default=None, help="Neighbor clips retained around a focus.")
    subparser.add_argument(
        "--format", dest="formats", action="append", default=None,
        metavar="FORMAT[,FORMAT...]",
        type=_visualize_format_argument,
        help="Repeatable/comma-separated png or md (default: png,md).",
    )
    subparser.add_argument(
        "--mode",
        choices=("auto", "inputs", "composed"),
        default="auto",
        help=(
            "auto always composes frames from the pinned saved revision; "
            "inputs is render-free; composed always requests composed frames."
        ),
    )
    subparser.add_argument(
        "--view",
        choices=("filmstrip", "contact", "overview", "motion", "diff"),
        default="filmstrip",
        help="filmstrip (default), contact/overview, motion, or immutable revision diff; diff requires explicit before/after revision ids.",
    )
    subparser.add_argument(
        "--before-revision-id", default=None,
        help="Required with --view diff: exact immutable before revision; no current-head fallback.",
    )
    subparser.add_argument(
        "--after-revision-id", default=None,
        help="Required with --view diff: exact immutable after revision; no current-head fallback.",
    )
    subparser.add_argument("--cut", default=None, help="Motion cut number, picture clip id, or @seconds.")
    subparser.add_argument(
        "--layer", dest="layers", action="append", default=None,
        help="Motion/contact layer name; repeat or comma-separate registered layers.",
    )
    from astrid.packs.timeline.cli_verify import add_visualize_labels_flag
    add_visualize_labels_flag(subparser)
    subparser.add_argument(
        "--beats", type=_parse_json_object, default=None,
        help="Caller-resolved beats JSON object with beats/downbeats/hits.",
    )
    subparser.add_argument("--frame-budget", dest="frame_budget", type=int, default=None,
                           help="Motion frame budget (1–120; default 60).")
    subparser.add_argument("--preset", default=None, help="Motion window preset: scan, motion, beat, frame, or cut.")
    subparser.add_argument("--window", dest="window_s", type=float, default=None,
                           help="Motion window width in seconds around --at.")
    subparser.add_argument(
        "--rules", type=_parse_json_object, default=None,
        help="Caller-resolved rules JSON object (params, severity, disable, path).",
    )
    subparser.add_argument("--cuts", default=None, help="Contact-only positive cut numbers, comma-separated (max 120).")
    subparser.add_argument("--preview", action="store_true", default=None,
                           help="Motion-only GIF from the already captured frames.")
    subparser.add_argument("--sample", choices=("interval", "clips", "cuts", "shots"), default=None,
                           help="Filmstrip sampling: interval (default), picture clips, cut boundaries, or authored story beats.")
    sampling = subparser.add_mutually_exclusive_group()
    sampling.add_argument("--every", type=float, default=None,
                          help="Filmstrip interval in seconds (default: 0.5); rerun with --range START..END to zoom.")
    sampling.add_argument("--every-frames", type=int, default=None,
                          help="Filmstrip interval in exact rendered frames; replaces --every (rerun for finer samples).")
    subparser.add_argument(
        "--include-cuts", action="store_true", default=None,
        help="With interval sampling, also capture visual cut-neighbor frames.",
    )
    subparser.add_argument(
        "--render-run", default=None,
        help=(
            "Explicit successful render run, or latest (filmstrip default). "
            "An explicit run may be historical/candidate; auto reuse checks the current timeline head."
        ),
    )
    subparser.add_argument("--columns", type=int, default=None,
                           help="Filmstrip contact sheet columns (default: 5; paired pages use one row by default).")
    subparser.add_argument("--page-size", type=int, default=None,
                           help="Filmstrip cards per static page (default: 50 standalone; paired pages use one row, or explicitly opt into up to two rows / 10 cards).")
    subparser.add_argument("--resolution", default=None, metavar="WIDTHxHEIGHT",
                           help="Filmstrip frame resolution, e.g. 960x540; recorded and applied exactly by the executor.")
    subparser.add_argument(
        "--include-media", action="store_true", default=None,
        help="Include a relative, digest-verified rendered video for offline filmstrip playback.",
    )
    subparser.add_argument(
        "--out", default=None, metavar="DIR",
        help=(
            "Also copy the view's page(s) and its raw frames (frames/, frame-index.json) to DIR once it "
            "settles; the managed copy stays where the summary says."
        ),
    )
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_visualize)


def _configure_render(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser, required=False)
    subparser.add_argument("--review", action="store_true", default=None, help="Burn in shot names/time plus pinned authored speech captions at the bottom (Remotion/Three.js).")
    subparser.add_argument(
        "ref",
        nargs="?",
        default=None,
        help=(
            "Canonical timeline UUID, ULID, or slug. "
            "When omitted, the project's default timeline is rendered."
        ),
    )
    subparser.add_argument(
        "--expected-version",
        dest="expected_version",
        type=int,
        default=None,
        help="Optional exact kernel config version; stale pins fail before admission.",
    )
    subparser.add_argument(
        "--backend",
        default=None,
        help="Qualified renderer id or supported compatibility selector.",
    )
    subparser.add_argument(
        "--profile",
        type=_parse_json_object,
        default=None,
        metavar="JSON",
        help=(
            "Flat RenderProfile v1 JSON object (no video/audio nesting). "
            "Complete Remotion MP4 example: "
            "{\"width\": 1920, \"height\": 1080, \"fps_rational\": [30, 1], "
            "\"time_base\": [1, 90000], \"container\": \"mp4\", "
            "\"video_codec\": \"h264\", \"video_profile\": null, "
            "\"video_level\": null, \"pixel_format\": \"yuv420p\", "
            "\"audio_codec\": \"aac\", \"audio_sample_rate\": 48000, "
            "\"audio_channel_layout\": \"stereo\", \"duration_tolerance\": 1}. "
            "The audio trio must be supplied together or all omitted. When omitted, the "
            "resolved theme canvas is used (default 1920x1080 at 30 fps), "
            "not legacy config.output resolution/fps hints. Explicit profiles must "
            "match the authoritative theme canvas; set theme_overrides.visual.canvas "
            "for a different size."
        ),
    )
    subparser.add_argument(
        "--output-name",
        default=None,
        help=(
            "Plain output filename (default hype.mp4). A canonical timeline stamped "
            "metadata.astrid_layer.alpha=true may request .mov for ProRes 4444/PCM output."
        ),
    )
    completion = subparser.add_mutually_exclusive_group()
    completion.add_argument(
        "--wait",
        dest="wait",
        action="store_true",
        default=True,
        help="Follow the render to completion and propagate terminal failure (default).",
    )
    completion.add_argument(
        "--detach",
        dest="wait",
        action="store_false",
        help="Return after admission with state=admitted; inspect the returned task/run later.",
    )
    subparser.add_argument(
        "--timeout-seconds",
        type=float,
        default=3600.0,
        help="Maximum wait for --wait before returning a non-success result (default: 3600).",
    )
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_cmd_render)


def _edit_checkout(parsed: argparse.Namespace):
    from astrid.sdk.timeline_checkout import Checkout
    return Checkout.draft(
        parsed.project,
        parsed.ref,
        name=getattr(parsed, "draft", None),
        client=parsed.client,
    )


def _checkout_change_units(checkout: Any) -> tuple[bool, list[list[str]]]:
    """Compare every SDK merge unit with the checkout's pinned base.

    ``Checkout.edits()`` is a clip/cut/placement diff. Fresh checkout safety
    and status also need parent config, shot payload, tracks, and registries,
    using the same whole-unit model as ``store.three_way(..., whole=True)``.
    An incomplete old draft base is unknown, so callers must not overwrite it.
    """
    from astrid.core.timeline.astrid_ns import normalized
    from astrid.sdk.timeline import store

    document = checkout.document()
    if not isinstance(document, Mapping):
        return False, []
    base_parent = document.get("base_parent_payload")
    if not isinstance(base_parent, Mapping):
        return False, []

    source_mapping = document.get("source_mapping")
    mapped_placements = (
        source_mapping.get("placements") if isinstance(source_mapping, Mapping) else None
    )
    if isinstance(mapped_placements, Mapping):
        base_placements = list(mapped_placements.values())
    elif isinstance(mapped_placements, list):
        base_placements = mapped_placements
    else:
        pinned_placements = document.get("base_placements")
        if not isinstance(pinned_placements, Mapping):
            return False, []
        base_placements = list(pinned_placements.values())
    if any(not isinstance(row, Mapping) or row.get("shot_id") is None for row in base_placements):
        return False, []

    current_shots = document.get("shots")
    if not isinstance(current_shots, Mapping):
        return False, []
    base_shots: dict[str, Any] = {}
    for row in base_placements:
        shot_id = str(row["shot_id"])
        shot = current_shots.get(shot_id)
        if not isinstance(shot, Mapping):
            return False, []
        base_payload = shot.get("base_payload")
        base_internal = shot.get("base_internal_timeline")
        if not isinstance(base_payload, Mapping) or not isinstance(base_internal, Mapping):
            return False, []
        base_shot = copy.deepcopy(dict(shot))
        base_shot["payload"] = copy.deepcopy(dict(base_payload))
        base_shot["internal_timeline"] = copy.deepcopy(dict(base_internal))
        base_shots[shot_id] = base_shot

    base_document = copy.deepcopy(dict(document))
    base_document["parent"] = copy.deepcopy(dict(base_parent))
    base_document["placements"] = copy.deepcopy(
        [dict(row) for row in base_placements]
    )
    base_document["shots"] = base_shots
    before_units = store._units(normalized(base_document), whole=True)
    current_units = store._units(normalized(document), whole=True)
    changed = []
    for key in set(before_units) | set(current_units):
        if key not in before_units or key not in current_units:
            changed.append(key)
            continue
        before = json.dumps(before_units[key], sort_keys=True, default=str)
        current = json.dumps(current_units[key], sort_keys=True, default=str)
        if before != current:
            changed.append(key)
    return True, [list(key) for key in sorted(changed)]


def _cmd_checkout(parsed: argparse.Namespace) -> int:
    from astrid.sdk.timeline import store
    from astrid.sdk.timeline_checkout import Checkout

    if parsed.fresh:
        project_id, timeline_id, _head = store.resolve_ids(
            parsed.project, parsed.ref, client=parsed.client
        )
        selected_name = parsed.draft or store.current_draft(project_id, timeline_id)
        selected_path = store.draft_path(project_id, timeline_id, selected_name)
        if selected_path.is_file():
            previous = Checkout.load(selected_path)
            base_known, changed_units = _checkout_change_units(previous)
            dirty = not base_known or bool(changed_units)
            if dirty:
                from astrid.sdk.contracts import ErrorObject

                return print_result(
                    DomainResult.failure(
                        ErrorObject(
                            "conflict",
                            "fresh checkout would replace a changed or unverifiable working copy; choose a distinct --draft name to preserve it",
                            {
                                "draft": selected_name,
                                "base_revision": previous.base_revision,
                                "change_state": "changed" if base_known else "unknown",
                                "changed_units": changed_units,
                            },
                        )
                    ),
                    as_json=parsed.json,
                )

    tl = Checkout.draft(
        parsed.project,
        parsed.ref,
        name=parsed.draft,
        client=parsed.client,
        fresh=parsed.fresh,
    )
    if getattr(parsed, "from_ref", None):
        if tl.changes():
            print("working copy has edits; choose a new --draft name before adopting another timeline", file=sys.stderr)
            return 2
        tl.adopt(parsed.from_ref, client=parsed.client)
        tl.save()
        print(f"adopted {parsed.from_ref}: narration, cuts, assets and intent")
    return 0 if tl else 1


def _cmd_status(parsed: argparse.Namespace) -> int:
    """Report the canonical head and an existing draft without creating one."""
    from astrid.sdk.timeline import store
    from astrid.sdk.timeline_checkout import Checkout

    project_id, timeline_id, current_head = store.resolve_ids(
        parsed.project, parsed.ref, client=parsed.client
    )
    draft_name = parsed.draft or store.current_draft(project_id, timeline_id)
    path = store.draft_path(project_id, timeline_id, draft_name)
    data: dict[str, Any] = {
        "timeline_id": timeline_id,
        "current_head": current_head,
        "draft": draft_name,
        "working_copy": "absent",
    }
    if path.is_file():
        checkout = Checkout.load(path)
        changes = checkout.changes()
        edit_diff = checkout.edits()
        base_known, changed_units = _checkout_change_units(checkout)
        cut_points = edit_diff.get("cut_points") or {}
        report = checkout.check()
        data.update(
            {
                "working_copy": "present",
                "base_revision": checkout.base_revision,
                "head_moved": checkout.base_revision != current_head,
                "changed": bool(changed_units) if base_known else None,
                "change_state": (
                    "unknown" if not base_known else "changed" if changed_units else "clean"
                ),
                "changed_units": changed_units,
                "changes": changes,
                "change_details": list(edit_diff.get("changes") or []),
                "placement_changes": list(edit_diff.get("placement_changes") or []),
                "cut_points": cut_points,
                "check": {
                    "valid": report.valid,
                    "problems": list(report.problems),
                    "changed_cuts": list(report.changed_cuts),
                },
            }
        )
    return print_result(DomainResult.success(data), as_json=parsed.json)


def _cmd_publish(parsed: argparse.Namespace) -> int:
    """Publish the named existing draft once through the SDK merge/CAS boundary."""
    from astrid.sdk.timeline_checkout import Checkout, find_draft

    path = find_draft(
        parsed.project, parsed.ref, parsed.draft, client=parsed.client
    )
    if path is None:
        from astrid.sdk.contracts import ErrorObject

        return print_result(
            DomainResult.failure(
                ErrorObject(
                    "not_found",
                    "no working copy exists to publish; run timelines checkout first",
                    {"timeline": parsed.ref, "draft": parsed.draft},
                ),
                idempotency_key=parsed.idempotency_key or "",
            ),
            as_json=parsed.json,
        )
    checkout = Checkout.load(path)
    key = parsed.idempotency_key or f"timeline-publish-{uuid.uuid4().hex}"
    receipt = checkout.publish(
        parsed.message,
        idempotency_key=key,
        client=parsed.client,
        force=parsed.force,
    )
    if receipt.get("narration_error"):
        from astrid.sdk.contracts import ErrorObject

        return print_result(
            DomainResult.failure(
                ErrorObject(
                    "partial_publication",
                    "timeline structure was published, but narration binding is pending",
                    {"receipt": receipt},
                ),
                idempotency_key=key,
            ),
            as_json=parsed.json,
        )
    return print_result(
        DomainResult.success(receipt, idempotency_key=key), as_json=parsed.json
    )


def _edit_duration(value: str) -> float:
    text=str(value).strip()
    if text.endswith("f"):
        return int(text[:-1]) / 30.0
    if text.endswith("s"):
        text=text[:-1]
    return float(text)


def _crossfade(tl: Any, parsed: argparse.Namespace) -> None:
    """--crossfade A B [curve=NAME] [--over S]: matching fades on two overlapping audio clips of one track."""
    from astrid.core.timeline.audio_curves import validate
    from astrid.sdk.timeline_editing import TimelineEditError

    args = list(parsed.crossfade)
    if len(args) not in (2, 3):
        raise TimelineEditError("--crossfade takes A B [curve=NAME]")
    curve_arg = args[2][6:] if len(args) == 3 and args[2].startswith("curve=") else None
    if len(args) == 3 and curve_arg is None:
        raise TimelineEditError("the optional --crossfade argument must be curve=NAME")
    a, b = tl.clip(args[0]), tl.clip(args[1])
    if not a.is_audio or not b.is_audio:
        raise TimelineEditError("--crossfade requires two audio clips")
    if a.track != b.track:
        raise TimelineEditError(f"--crossfade requires the same audio track ({a.track!r} vs {b.track!r})")
    if b.start < a.start:
        raise TimelineEditError("--crossfade requires A to start before B")
    try:
        curve = validate(curve_arg or "equal-power")
    except ValueError as exc:
        raise TimelineEditError(str(exc)) from None
    if parsed.overlap is not None:
        overlap = float(parsed.overlap)
        if overlap <= 0:
            raise TimelineEditError("--over must be a positive number of seconds")
        if overlap > min(a.duration, b.duration):
            raise TimelineEditError("--over cannot exceed either clip's duration")
        # Keep A fixed and move B so its start is exactly the requested overlap before A ends.
        b.enter_at(a.start + a.duration - overlap)
        print(f"crossfade overlap {overlap:g}s: moved {b.address} start; {a.address} stayed in place")
    else:
        if b.end < a.end:
            raise TimelineEditError("--crossfade requires B to continue through A's end; use --over to position B")
        overlap = min(a.start + a.duration, b.start + b.duration) - max(a.start, b.start)
        if overlap <= 0:
            raise TimelineEditError("clips do not overlap; supply --over SECONDS to move B's start")
    a.set_look(fade_out=overlap)
    b.set_look(fade_in=overlap)
    a.params["fadeOutCurve"] = curve
    b.params["fadeInCurve"] = curve
    print(f"crossfade {a.address} → {b.address}: {overlap:g}s, curve={curve}")


def _cmd_edit(parsed: argparse.Namespace) -> int:
    from astrid.sdk.timeline_editing import TimelineEditError
    tl = _edit_checkout(parsed)
    if getattr(parsed, "music", None) is not None:
        tl.music = parsed.music
    before = tl.document()
    line_operation = bool(parsed.replace_line or parsed.insert_line or parsed.from_script)
    line_only_args = bool(
        parsed.take or parsed.words or parsed.after or parsed.insert_gap_after is not None
        or parsed.line_text or parsed.takes or parsed.script_gaps
    )
    if parsed.replace_line:
        if not parsed.take or not parsed.words:
            raise TimelineEditError("--replace-line requires --take and --words")
        if parsed.insert_line or parsed.from_script or parsed.remove_line:
            raise TimelineEditError("--replace-line cannot be combined with another narration line operation")
        if parsed.after or parsed.insert_gap_after is not None or parsed.takes or parsed.script_gaps:
            raise TimelineEditError("insert and from-script options cannot be combined with --replace-line")
        tl.voice(parsed.replace_line).replace(
            parsed.take, words=parsed.words, text=parsed.line_text
        )
    elif parsed.insert_line:
        if not parsed.take or not parsed.words or not parsed.after:
            raise TimelineEditError("--insert-line requires --after, --take, and --words")
        if parsed.from_script or parsed.remove_line or parsed.takes or parsed.script_gaps:
            raise TimelineEditError("--insert-line cannot be combined with another narration line operation")
        tl.insert_line(
            parsed.insert_line,
            parsed.take,
            words=parsed.words,
            after=parsed.after,
            gap_after=parsed.insert_gap_after,
            text=parsed.line_text,
        )
    elif parsed.from_script:
        if parsed.take or parsed.words or parsed.after or parsed.insert_gap_after is not None or parsed.line_text:
            raise TimelineEditError("--from-script cannot be combined with single-line take options")
        if parsed.remove_line:
            raise TimelineEditError("--from-script owns line removal for this edit")
        tl.apply_script(parsed.from_script, takes=parsed.takes, gaps=parsed.script_gaps)
    elif line_only_args:
        raise TimelineEditError("--take, --words, --after, --insert-gap-after, --line-text, --takes and --gaps require a line operation")
    if getattr(parsed, "overlap", None) is not None and not parsed.crossfade:
        raise TimelineEditError("--over requires --crossfade A B")
    if parsed.crossfade:
        if parsed.clip or parsed.cut or parsed.close_gap_before or parsed.split or parsed.add_cut or line_operation:
            raise TimelineEditError("--crossfade is a timeline-level operation; run it separately")
        _crossfade(tl, parsed)
    if getattr(parsed, "add_media", None) is not None:
        if parsed.clip or parsed.cut or parsed.split or parsed.add_cut or line_operation or parsed.close_gap_before:
            raise TimelineEditError("--add-media is one edit; do not combine it with a clip selector or timeline-level edit")
        if not (parsed.track and parsed.on):
            raise TimelineEditError("--add-media needs --track TRACK and --on MOMENT")
        clip = tl.add("media", at=parsed.on, asset=parsed.add_media, track=parsed.track,
                      hold=parsed.for_seconds, clip_id=parsed.clip_id, cut=None)
        if not clip.is_audio:
            raise TimelineEditError(f"--track {parsed.track!r} is not an audio track")
        if parsed.until is not None:
            clip.until(parsed.until)
        source_in = parsed.trim_in if parsed.trim_in is not None else 0.0
        speed = float(clip.data.get("speed") or 1.0)
        if parsed.trim_out is not None:
            source_out = parsed.trim_out
        elif parsed.for_seconds is None and parsed.until is None:
            source_out = clip._source_duration()
        else:
            source_out = source_in + clip.duration * speed
        clip.trim(in_s=source_in, out_s=source_out)
        from astrid.packs.timeline.cli_look import apply_look, look_values
        values = look_values(parsed)
        if values:
            apply_look(tl, clip, values)
    elif parsed.clip:
        clip = tl.clip(parsed.clip)
        if parsed.set_values:
            values = {}
            for item in parsed.set_values:
                key, sep, raw = item.partition("=")
                if not sep:
                    raise TimelineEditError(f"--set expects key=value: {item}")
                try:
                    values[key] = json.loads(raw)
                except json.JSONDecodeError:
                    values[key] = raw
            clip.set(**values)
        if parsed.swap_asset:
            clip.swap_asset(parsed.swap_asset)  # a key, a file, a media handle, or KEY=HANDLE to name new media
        from astrid.packs.timeline.cli_look import apply_look, has_look, look_values
        if has_look(parsed):
            apply_look(tl, clip, look_values(parsed))
        if parsed.on is not None:
            clip.on(parsed.on)
        if parsed.until is not None:
            clip.until(parsed.until)
        if parsed.for_seconds is not None:
            clip.set_duration(parsed.for_seconds)
        if parsed.extend is not None:
            clip.extend(parsed.extend)
        if parsed.trim_in is not None or parsed.trim_out is not None:
            clip.trim(in_s=parsed.trim_in, out_s=parsed.trim_out)
        if parsed.slip is not None:
            clip.slip(parsed.slip)
        if parsed.nudge is not None or parsed.nudge_frames is not None:
            clip.nudge(parsed.nudge or 0, frames=parsed.nudge_frames or 0)
        if parsed.remove:
            clip.remove()
        if parsed.at is not None:
            clip.enter_at(parsed.at)
            if parsed.offset is not None: clip.nudge(parsed.offset)
    else:
        from astrid.packs.timeline.cli_look import has_look
        if has_look(parsed):
            raise TimelineEditError("look flags require --clip")
    if getattr(parsed, "replace_asset", None):
        key, sep, handle = parsed.replace_asset.partition("=")
        if not sep or not key or not handle:
            raise TimelineEditError("--replace-asset takes KEY=HANDLE (e.g. TOOL-BROOM=run:RUN/sprites#0)")
        replaced = tl.replace_asset(key, handle)
        print(f"replaced {key} in {len(replaced)} clip(s): {', '.join(replaced)}")
    if parsed.split:
        tl.cut(parsed.split).split(parsed.on)
    if parsed.add_cut:
        tl.add_cut(parsed.on)
    if parsed.cut and parsed.on:
        group=next((g for g in tl._cut_groups() if g["id"]==parsed.cut),None)
        if not group: raise TimelineEditError(f"cut {parsed.cut!r} does not exist")
        picture=tl.cut(parsed.cut).picture
        picture.on(parsed.on)
    if parsed.film_end:
        tl.film_end(parsed.film_end)
    for gap_spec in parsed.gap_after:
        segment, value = gap_spec.split("=", 1)
        tl.voice(segment).set_gap_after(float(value))
    if parsed.remove_line:
        tl.remove_line(parsed.remove_line)
    if parsed.close_gap_before:
        tl.close_gap(before=parsed.close_gap_before)
    changed = before != tl.document()
    if changed:
        tl.save(quiet=True)
        print("edited working copy")
        from astrid.packs.timeline.cli_sweep import auto_sweep_after_edit, touched_cuts

        sweep_status = auto_sweep_after_edit(
            parsed,
            tl,
            reflow=bool(
                parsed.film_end or parsed.gap_after or parsed.remove_line
                or parsed.close_gap_before or parsed.split or parsed.add_cut
                or line_operation
            ),
            touched_cuts=len(touched_cuts(before, tl)),
        )
        return sweep_status
    print("no change (the working copy already matches)")
    return 3


def _cmd_check(parsed: argparse.Namespace) -> int:
    from astrid.sdk.timeline_checkout import Checkout, find_draft

    path = find_draft(parsed.project, parsed.ref, parsed.draft, client=parsed.client)
    if path is None:
        print(f"no working copy · next: timelines checkout {parsed.ref} --project {parsed.project}")
        return 0

    tl = Checkout.load(path)
    report = tl.check()
    print(report.full_text() if parsed.all else str(report))
    if parsed.at is not None:
        verification = tl.verify(at=parsed.at, client=parsed.client, labels=parsed.labels)
        for line in verification.get("lines", []):
            print(line)
    sweep_status = 0
    if parsed.sweep:
        from astrid.packs.timeline.cli_sweep import print_sweep

        sweep_status = print_sweep(parsed, tl)
    if not report.valid:
        return 1
    if sweep_status == 2:
        return 2
    return sweep_status


def _cmd_apply(parsed: argparse.Namespace) -> int:
    from astrid.sdk.timeline_sheet import apply_sheet
    tl = _edit_checkout(parsed)
    before = tl.document()
    changes = apply_sheet(tl, Path(parsed.sheet_file).read_text(encoding="utf-8"))
    if changes or before != tl.document():
        tl.save(quiet=True)
        print("applied sheet")
        return 0
    print("no change (the sheet matches the working copy)")
    return 3


def _cmd_undo(parsed: argparse.Namespace) -> int:
    tl=_edit_checkout(parsed); labels=tl.undo(parsed.steps)
    print("undid "+"; ".join(labels)); return 0


def _cmd_redo(parsed: argparse.Namespace) -> int:
    tl=_edit_checkout(parsed); labels=tl.redo(parsed.steps)
    print("redid "+"; ".join(labels)); return 0


def _as_timeline_verb(handler):
    """Mark editor handlers while they run so journal records retain CLI provenance."""
    @wraps(handler)
    def run(parsed):
        global _IN_VERB
        previous = _IN_VERB
        _IN_VERB = True
        try:
            return handler(parsed)
        finally:
            _IN_VERB = previous
    return run


def _configure_checkout(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline id or slug to check out.")
    subparser.add_argument("--from", dest="from_ref", help="Adopt content from another timeline into this working copy.")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    subparser.add_argument("--fresh", action="store_true", help="Check out the current head instead of reusing the selected working copy.")
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_as_timeline_verb(_cmd_checkout))


def _configure_status(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline id or slug to inspect.")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_as_timeline_verb(_cmd_status))


def _configure_publish(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline id or slug with a saved working copy.")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    subparser.add_argument("-m", "--message", default="", help="Publication message.")
    _add_idempotency_key(subparser)
    subparser.add_argument("--force", action="store_true", help="Resolve overlapping edits in favor of this draft.")
    _add_json_flag(subparser)
    subparser.set_defaults(handler=_as_timeline_verb(_cmd_publish))


def _configure_edit(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline id or slug with a saved working copy.")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    subparser.add_argument("--clip")
    subparser.add_argument("--add-media", dest="add_media", default=None, metavar="FILE|HANDLE|KEY",
                           help="Add an audio media clip; audio tracks stay independent of picture cuts "
                                "(needs --track and --on; --for/--until/--trim-in/--trim-out/--gain-db/--id optional).")
    subparser.add_argument("--track", default=None, metavar="TRACK", help="Audio track for --add-media (music, vo, sfx ...).")
    subparser.add_argument("--id", dest="clip_id", default=None, metavar="ID", help="Clip id for --add-media.")
    subparser.add_argument("--trim-in", dest="trim_in", type=float, default=None, metavar="SECONDS",
                           help="Set a media clip's source in point; its film start stays and its length follows.")
    subparser.add_argument("--trim-out", dest="trim_out", type=float, default=None, metavar="SECONDS",
                           help="Set a media clip's source out point; its film start stays and its length follows.")
    subparser.add_argument("--slip", type=float, default=None, metavar="SECONDS",
                           help="Move a media clip's source window while its film position and length stay fixed.")
    subparser.add_argument("--set", dest="set_values", action="append", default=[])
    subparser.add_argument("--swap-asset", metavar="KEY|FILE|HANDLE|KEY=HANDLE",
                           help="Point the clip at an asset: a registry key, a local file, or project media "
                                "(run:RUN/PORT#n, task:TASK/PORT#n, ref:NAME, sha256:DIGEST). Name new media yourself "
                                "with KEY=HANDLE (BROOM=run:RUN/sprites#0).")
    subparser.add_argument("--replace-asset", dest="replace_asset", default=None, metavar="KEY=HANDLE",
                           help="Repoint every clip using KEY to new project media, keeping the key "
                                "(run:..., task:..., ref:..., sha256:...).")
    from astrid.packs.timeline.cli_look import add_look_flags
    add_look_flags(subparser)
    subparser.add_argument("--on")
    subparser.add_argument("--until")
    subparser.add_argument("--for", dest="for_seconds", type=float)
    subparser.add_argument("--extend", type=float)
    subparser.add_argument("--nudge", type=float)
    subparser.add_argument("--nudge-frames", type=int)
    subparser.add_argument("--close-gap-before")
    subparser.add_argument("--at", "--at-word", dest="at")
    subparser.add_argument("--offset", type=float)
    subparser.add_argument("--split")
    subparser.add_argument("--add-cut", action="store_true")
    subparser.add_argument("--cut")
    subparser.add_argument("--film-end")
    subparser.add_argument("--gap-after", action="append", default=[], metavar="LINE=SECONDS",
                           help="Set the declared silence after a line; repeat to set several lines.")
    subparser.add_argument("--remove-line")
    narration = subparser.add_mutually_exclusive_group()
    narration.add_argument("--replace-line", metavar="LINE", help="Replace one line's selected take and word timings.")
    narration.add_argument("--insert-line", metavar="LINE", help="Insert a line after --after.")
    narration.add_argument("--from-script", metavar="PATH", help="Apply a JSON narration script and its local takes.")
    subparser.add_argument("--take", help="Selected WAV or registered take for --replace-line/--insert-line.")
    subparser.add_argument("--words", help="Word-timing JSON for --replace-line/--insert-line.")
    subparser.add_argument("--after", help="Existing line after which --insert-line is placed.")
    subparser.add_argument("--insert-gap-after", type=float, help="Declared gap after a newly inserted line, in seconds.")
    subparser.add_argument("--text", "--line-text", dest="line_text",
                           help="Narration text to bind with a replacement or insertion.")
    subparser.add_argument("--takes", help="Take directory used by --from-script.")
    subparser.add_argument("--gaps", dest="script_gaps", action="store_true",
                           help="Use script-declared gaps when applying --from-script.")
    subparser.add_argument("--music", choices=("keep-end", "plays-on"),
                           help="Music policy used when a structural edit changes the film length.")
    from astrid.core.timeline.audio_curves import names as audio_curve_names

    subparser.add_argument("--crossfade", nargs="+", default=None, metavar="TOKEN",
                           help=f"Crossfade clips A and B on one audio track; optional third token curve=NAME "
                                f"(default: equal-power; curves: {', '.join(audio_curve_names())}). "
                                "With --over, moves B's start to create that overlap.")
    subparser.add_argument("--over", dest="overlap", type=float, default=None, metavar="SECONDS",
                           help="With --crossfade: requested overlap; keeps A fixed and moves B's start.")
    subparser.add_argument("--remove", action="store_true")
    from astrid.packs.timeline.cli_sweep import add_edit_sweep_flags
    add_edit_sweep_flags(subparser)
    subparser.set_defaults(handler=_as_timeline_verb(_cmd_edit))


def _configure_check(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline UUID, ULID, or slug with a saved working copy.")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    subparser.add_argument("--all", action="store_true", help="Print the full validation report.")
    subparser.add_argument("--at", action="append", default=None, metavar="MOMENT",
                           help="Compare the published timeline and working copy at this moment; repeat for multiple moments.")
    from astrid.packs.timeline.cli_verify import add_labels_flag
    add_labels_flag(subparser)
    from astrid.packs.timeline.cli_sweep import add_check_sweep_flag
    add_check_sweep_flag(subparser)
    subparser.set_defaults(handler=_as_timeline_verb(_cmd_check))


def _cmd_assets(parsed: argparse.Namespace) -> int:
    """List registry keys, media facts and the clips that use each key."""
    from astrid.sdk.timeline_checkout import Checkout, find_draft

    path = find_draft(parsed.project, parsed.ref, parsed.draft, client=parsed.client)
    tl = Checkout.load(path) if path else Checkout.open(parsed.project, parsed.ref, client=parsed.client)
    rows = tl.assets(parsed.key)
    if parsed.key and not rows:
        print(f"no asset key {parsed.key!r} in {parsed.ref}", file=sys.stderr)
        return 1
    if not rows:
        print("no registered assets")
        return 0
    for row in rows:
        media = row["media"]
        digest = str(media.get("content_sha256") or media.get("media_id") or "unknown")
        kind = str(media.get("type") or "unknown")
        size = media.get("size_bytes", media.get("size"))
        size_text = f"{size} bytes" if size is not None else str(media.get("resolution") or "size unknown")
        source = media.get("source") or "origin unknown"
        print(f"{row['key']}  {digest}  {kind}  {size_text}  {source}")
        print(f"  clips: {', '.join(row['clips']) if row['clips'] else 'none'}")
    return 0


def _configure_assets(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline id or slug.")
    subparser.add_argument("key", nargs="?", default=None, help="Show only this asset key.")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    subparser.set_defaults(handler=_cmd_assets)


def _configure_find(subparser: argparse.ArgumentParser) -> None:
    from astrid.packs.timeline.cli_find import configure_find, run_find

    configure_find(subparser, _add_project_arg)
    subparser.set_defaults(handler=run_find)


def _configure_working_verb(name: str):
    """Configure one of the working-copy verbs that live in cli_working (lint, lines, words, discard, duplicate)."""
    def configure(subparser: argparse.ArgumentParser) -> None:
        from astrid.packs.timeline import cli_working

        getattr(cli_working, f"_configure_{name}")(subparser)
    return configure


def _configure_log(subparser: argparse.ArgumentParser) -> None:
    from astrid.packs.timeline.cli_log import configure_log
    configure_log(subparser)


def _configure_apply(subparser: argparse.ArgumentParser) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref", help="Timeline id or slug with a saved working copy.")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    subparser.add_argument("sheet_file", help="Path to the edited cut sheet.")
    subparser.set_defaults(handler=_as_timeline_verb(_cmd_apply))


def _configure_history_edit(subparser: argparse.ArgumentParser, handler) -> None:
    _add_project_arg(subparser)
    subparser.add_argument("ref")
    subparser.add_argument("--draft", default=None, help="Working copy name (default: current working copy).")
    subparser.add_argument("--steps", type=_positive_int, default=1)
    subparser.set_defaults(handler=_as_timeline_verb(handler))


COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec("checkout", help="Create or open a detached editable working copy.", configure=_configure_checkout),
    CommandSpec("edit", help="Edit a detached timeline working copy.", configure=_configure_edit),
    CommandSpec("assets", help="List timeline asset keys, media details, and every clip using each key.", configure=_configure_assets),
    CommandSpec("find", help="Find what you hear or see: addresses and times.", configure=_configure_find),
    CommandSpec("apply", help="Apply a cut sheet to a detached working copy.", configure=_configure_apply),
    CommandSpec("undo", help="Undo edits to a detached working copy.", configure=lambda p: _configure_history_edit(p, _cmd_undo)),
    CommandSpec("redo", help="Redo edits to a detached working copy.", configure=lambda p: _configure_history_edit(p, _cmd_redo)),
    CommandSpec("check", help="Validate a working copy and optionally sweep every cut.", configure=_configure_check),
    CommandSpec("status", help="Show the canonical head and an existing working copy.", configure=_configure_status),
    CommandSpec("publish", help="Publish an existing working copy through the SDK merge/CAS boundary.", configure=_configure_publish),
    CommandSpec("discard", help="Drop a working copy (its unpublished edits).", configure=_configure_working_verb("discard")),
    CommandSpec("duplicate", help="Copy a timeline's published head into a new timeline, for a trial.", configure=_configure_working_verb("duplicate")),
    CommandSpec("lines", help="The narration line by line: id, when it is spoken, the gap after it, its text and take.", configure=_configure_working_verb("lines")),
    CommandSpec("words", help="List the spoken words with their times, or one word in full.", configure=_configure_working_verb("words")),
    CommandSpec(
        "create",
        help="Create an empty timeline with its first canonical head.",
        configure=_configure_create,
    ),
    CommandSpec(
        "list",
        help="List active timelines in a project (slug ascending).",
        configure=_configure_list,
    ),
    CommandSpec(
        "show",
        help="Show one timeline by UUID, ULID, or slug (use --summary for editor context).",
        configure=_configure_show,
    ),
    CommandSpec(
        "script",
        help="Read placed narration in timeline order from pinned shot text revisions.",
        configure=_configure_script,
    ),
    CommandSpec(
        "replace-parent-media",
        help="Atomically replace one clip in an exact canonical parent-composition closure.",
        configure=_configure_replace_parent_media,
    ),
    CommandSpec(
        "archive",
        help="Archive a timeline (reversible with recover).",
        configure=_configure_archive,
    ),
    CommandSpec(
        "recover",
        help="Restore archived work; safe to repeat (changed=false when active).",
        configure=_configure_recover,
    ),
    CommandSpec(
        "history",
        help="Ordered lifecycle event history for one timeline.",
        configure=_configure_history,
    ),
    CommandSpec(
        "log",
        help="Read and verify the hash-chained edit journal for one timeline.",
        configure=_configure_log,
    ),
    CommandSpec(
        "diff",
        help="Deterministic adjacent-version diffs for one timeline.",
        configure=_configure_diff,
    ),
    CommandSpec(
        "visualize",
        help="Build a timeline evidence pack synchronously through the public SDK.",
        configure=_configure_visualize,
        requires_pack_host=True,
    ),
    CommandSpec(
        "lint",
        help="Run every registered check over every picture cut, from timeline data (no capture).",
        configure=_configure_working_verb("lint"),
    ),
    CommandSpec(
        "inspect",
        help="Read bounded named sections of a verified filmstrip bundle offline.",
        configure=_configure_inspect,
    ),
    CommandSpec(
        "render",
        help="Render a canonical kernel timeline with optional version pinning.",
        configure=_configure_render,
        requires_pack_host=True,
    ),
)


def build_parser(client: Any) -> argparse.ArgumentParser:
    """Build the ``timelines`` product-family parser stamped with *client*.

    Exactly the supported verbs above are registered — no aliases, no legacy
    migration/push/pull/sync/audit/erase/repair verbs, and no ``copy``
    (reserved for m6) — plus the manifest-declared nested ``shots`` mount
    (``astrid timelines shots <verb>``) embedded from the shots product
    parser.
    """
    from astrid.packs.shots import cli as shots_cli

    def _configure_shots(subparser: argparse.ArgumentParser) -> None:
        nested = subparser.add_subparsers(dest="shot_command", required=True)
        register_product_commands(nested, shots_cli.COMMANDS, family="shots", client=client)

    parser = argparse.ArgumentParser(
        prog="astrid timelines",
        description=(
            "Timeline check/create/list/show/script/replace-parent-media/archive/recover/history/log/diff/visualize/lint/render/lines/words/discard/duplicate "
            "(product family); nested shots beneath 'timelines shots'."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    register_product_commands(
        subparsers,
        (
            *COMMANDS,
            CommandSpec(
                "shots",
                help="Nested project-level shot list/create/show/add/remove/reorder "
                "(manifest-owned mount).",
                configure=_configure_shots,
            ),
        ),
        family=_FAMILY,
        client=client,
    )
    return parser
