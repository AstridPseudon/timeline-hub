#!/usr/bin/env python3
"""Read-only owner-film differences scanner.

The scanner accepts one exact Runtime canonical-document JSON closure and an
extracted Agent checkout.  It uses the Agent's existing projector, clip-field
codec, element registry, rational-FPS helper, and half-open duration helpers.
It does not search for projects, open a database, fetch media, render, use a
credential, or modify the input.

This is a delivery utility, not an Astrid product command.  Its output is
deliberately bounded to IDs, pins, property names, source paths, frame ranges,
compile availability, and known/unknown classifications.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections.abc import Mapping, Sequence
from itertools import combinations
from pathlib import Path
from typing import Any

VERSION = "1.0.7"
SEMANTIC_CATEGORIES = (
    "curve_honoured",
    "element_clip_look_overlap",
    "continuous_audio_fade",
)
_BUILTIN_CLIP_TYPES = frozenset(
    {"media", "video", "image", "audio", "text", "effect-layer", "hold"}
)
_AUDIO_ROLES = frozenset(
    {"audio", "dialogue", "music", "sfx", "sound", "voiceover", "vo"}
)
_AUDIO_ASSET_TYPES = frozenset(
    {"audio", "audio/mpeg", "audio/mp4", "audio/wav", "audio/x-wav"}
)
_AUDIO_FADE_PATHS = {"fade_in": "params.fadeIn", "fade_out": "params.fadeOut"}
_AUDIO_CURVE_PATHS = {
    "fade_in": "params.fadeInCurve",
    "fade_out": "params.fadeOutCurve",
}
_LOOK_NAMES = (
    "opacity",
    "entrance",
    "exit",
    "fade_in",
    "fade_out",
    "crop_top",
    "crop_right",
    "crop_bottom",
    "crop_left",
    "speed",
)
_MEDIA_LOOK_NAMES = ("entrance", "exit")
_NOT_COVERED = (
    "transition_conversion",
    "media_clip_look_overlap",
    "renderer_presence_alpha_pixel_coverage",
)
_REFERENCE_FIELDS = (
    "project_id",
    "timeline_id",
    "revision_id",
    "occurrence_id",
    "shot_id",
    "shot_revision_id",
    "internal_timeline_revision_id",
    "clip_id",
    "authored_clip_id",
    "source_kind",
    "source_path",
)
_REFERENCE_LIST_FIELDS = ("clip_ids", "occurrence_ids", "source_kinds")


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _dotted(value: Any, path: str) -> Any:
    current = value
    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def _dedupe(values: Sequence[str | None]) -> list[str]:
    return list(dict.fromkeys(value for value in values if isinstance(value, str) and value))


def _add_error(errors: list[str], message: str) -> None:
    if message not in errors:
        errors.append(message)


def _reference_error(field: str) -> str:
    return f"{field} reference must be a string"


def _rows(value: Any) -> Sequence[Any]:
    return value if isinstance(value, list) else ()


def _sanitize_ref_value(
    field: str, value: Any, errors: list[str], *, allow_none: bool = True
) -> str | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str):
        _add_error(errors, _reference_error(field))
        return None
    return value


def _sanitize_refs(refs: Mapping[str, Any], errors: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in _REFERENCE_FIELDS:
        if field not in refs or refs[field] is None:
            continue
        value = _sanitize_ref_value(field, refs[field], errors)
        if value is not None:
            result[field] = value
    for field in _REFERENCE_LIST_FIELDS:
        if field not in refs or refs[field] is None:
            continue
        value = refs[field]
        if not isinstance(value, (list, tuple)):
            _add_error(errors, f"{field} references must be strings")
            continue
        valid = [item for item in value if isinstance(item, str)]
        if len(valid) != len(value):
            _add_error(errors, f"{field} references must be strings")
        result[field] = valid
    return result


def _agent_api(agent_root: str | os.PathLike[str]) -> dict[str, Any]:
    """Load only public Agent helpers from the explicitly supplied checkout."""
    root = Path(agent_root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("--agent-root must name an extracted Agent directory")
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from astrid.core.element.registry import load_default_registry
    from astrid.core.timeline import audio_curves, clip_fields
    from astrid.core.timeline.duration import clip_end_frame, clip_start_frame
    from astrid.core.timeline.shot_composition_projection import (
        project_runtime_parent_composition,
    )
    from astrid.sdk.timeline.capture import rate

    return {
        "root": root,
        "audio_curves": audio_curves,
        "clip_fields": clip_fields,
        "clip_end_frame": clip_end_frame,
        "clip_start_frame": clip_start_frame,
        "load_default_registry": load_default_registry,
        "project_runtime_parent_composition": project_runtime_parent_composition,
        "rate": rate,
    }


def _fps_rational(config: Mapping[str, Any], api: Mapping[str, Any]) -> tuple[int, int]:
    output = config.get("output")
    if isinstance(output, Mapping) and output.get("fps") is not None:
        fps = api["rate"](output["fps"])
        return fps.numerator, fps.denominator
    from astrid.core.rendering.profile import resolve_render_profile

    profile = resolve_render_profile(config)
    return tuple(profile.fps_rational)


def _raw_clip_sources(document: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Return source paths and immutable identity pins, never raw clip data."""
    parent = _mapping(document["parent_revision"], "parent_revision")
    payload = _mapping(parent["payload"], "parent_revision.payload")
    paths: dict[str, dict[str, Any]] = {}
    parent_clips = payload.get("clips")
    if isinstance(parent_clips, list):
        parent_prefix = "parent_revision.payload.clips"
    else:
        config = _mapping(payload.get("config"), "parent_revision.payload.config")
        parent_clips = config.get("clips", [])
        parent_prefix = "parent_revision.payload.config.clips"
    if isinstance(parent_clips, list):
        for index, raw in enumerate(parent_clips):
            if isinstance(raw, Mapping) and isinstance(raw.get("id"), str):
                paths[raw["id"]] = {
                    "source_kind": "parent_clip",
                    "source_path": f"{parent_prefix}[{index}]",
                    "authored_clip_id": raw["id"],
                }

    shots = {
        (row.get("shot_id"), row.get("revision_id")): row
        for row in _rows(document.get("shot_revisions"))
        if isinstance(row, Mapping)
        and isinstance(row.get("shot_id"), str)
        and isinstance(row.get("revision_id"), str)
    }
    internal_rows = _rows(document.get("internal_timeline_revisions"))
    internals: dict[str, Mapping[str, Any]] = {}
    internal_indexes: dict[str, int] = {}
    # Source indexes must be unambiguous even when this helper is used directly.
    # The Agent projector remains the canonical closure validator in scan().
    for index, row in enumerate(internal_rows):
        if not isinstance(row, Mapping) or not isinstance(row.get("revision_id"), str):
            continue
        revision_id = row["revision_id"]
        if revision_id in internal_indexes:
            raise ValueError(
                f"internal_timeline_revisions[{index}].revision_id has an ambiguous source index"
            )
        internals[revision_id] = row
        internal_indexes[revision_id] = index
    for occurrence in _rows(payload.get("occurrences")):
        if not isinstance(occurrence, Mapping):
            continue
        occurrence_id = occurrence.get("occurrence_id")
        shot_key = (
            occurrence.get("shot_id"),
            occurrence.get("shot_revision_id", occurrence.get("revision_id")),
        )
        shot = shots.get(shot_key)
        if not isinstance(occurrence_id, str) or not isinstance(shot, Mapping):
            continue
        internal_id = shot.get("internal_timeline_revision_id")
        if not isinstance(internal_id, str):
            shot_payload = shot.get("payload")
            if isinstance(shot_payload, Mapping):
                internal_id = shot_payload.get("internal_timeline_revision_id")
        internal = internals.get(internal_id)
        internal_payload = internal.get("payload") if isinstance(internal, Mapping) else None
        clips = internal_payload.get("clips", []) if isinstance(internal_payload, Mapping) else []
        for index, raw in enumerate(clips):
            if not isinstance(raw, Mapping) or not isinstance(raw.get("id"), str):
                continue
            paths[f"{occurrence_id}:{raw['id']}"] = {
                "source_kind": "occurrence_child_clip",
                "source_path": (
                    f"internal_timeline_revisions[{internal_indexes[internal_id]}].payload.clips[{index}]"
                    if internal_id in internal_indexes
                    else None
                ),
                "occurrence_id": occurrence_id,
                "shot_id": shot_key[0],
                "shot_revision_id": shot_key[1],
                "internal_timeline_revision_id": internal_id,
                "authored_clip_id": raw["id"],
            }
    return paths


def _look_source_paths(clip: Mapping[str, Any], base: str | None, clip_fields: Any) -> dict[str, str]:
    if not base:
        return {}
    paths: dict[str, str] = {}
    for name in (*_LOOK_NAMES, "transition"):
        spec = clip_fields.FIELDS.get(name)
        if spec is None:
            continue
        stored_path = spec.stored_at
        if _dotted(clip, stored_path) is not None:
            paths[name] = f"{base}.{stored_path}"
    if isinstance(clip.get("entrance"), Mapping) and clip["entrance"].get("type") == "fade":
        paths.setdefault("fade_in", f"{base}.entrance")
    if isinstance(clip.get("exit"), Mapping) and clip["exit"].get("type") == "fade":
        paths.setdefault("fade_out", f"{base}.exit")
    return paths


def _unreadable_look_names(
    clip: Mapping[str, Any], *, fps: float, clip_fields: Any, names: Sequence[str]
) -> list[str]:
    """Identify look names whose isolated Agent description still fails.

    This probes the existing Agent codec with one authored field at a time. It
    does not validate the document or copy a value into the report; the caller
    emits only the bounded field source path for fields the codec cannot
    describe.
    """
    unreadable: list[str] = []
    for name in names:
        spec = clip_fields.FIELDS.get(name)
        if spec is None:
            continue
        stored_path = spec.stored_at
        value = _dotted(clip, stored_path)
        if value is None:
            continue
        probe: dict[str, Any] = {}
        node = probe
        parts = stored_path.split(".")
        for part in parts[:-1]:
            child: dict[str, Any] = {}
            node[part] = child
            node = child
        node[parts[-1]] = value
        try:
            clip_fields.describe(probe, fps=fps)
        except Exception:  # noqa: BLE001 - the codec is the source of truth
            unreadable.append(name)
    return unreadable


def _element_info(clip: Mapping[str, Any], registry: Any, agent_root: Path) -> dict[str, str]:
    ref = clip.get("elementRef")
    clip_type = clip.get("clipType", clip.get("clip_type", "media"))
    requested_id = ref.get("id") if isinstance(ref, Mapping) else clip_type
    requested_kind = ref.get("kind") if isinstance(ref, Mapping) else None
    if not isinstance(requested_id, str) or requested_id in _BUILTIN_CLIP_TYPES:
        return {"classification": "not_element", "compile_availability": "not_applicable"}
    if not requested_id or (
        isinstance(ref, Mapping) and requested_kind not in (None, "effect", "effects")
    ):
        return {"classification": "unknown_candidate", "compile_availability": "unknown"}
    if registry is None:
        return {"classification": "unknown_candidate", "compile_availability": "unknown"}
    pack_id = ref.get("packId") if isinstance(ref, Mapping) else None
    try:
        definition = registry.get("effects", requested_id, pack_id=pack_id)
    except (KeyError, TypeError, ValueError):
        return {"classification": "unknown_candidate", "compile_availability": "unknown"}
    source = getattr(definition, "component", None) or getattr(definition, "root", None)
    source_path = str(source) if source is not None else None
    if source_path:
        source_file = Path(source_path)
        if not source_file.is_absolute():
            source_file = agent_root / source_file
    available = bool(source_path and source_file.exists()) if source_path else False
    return {
        "classification": "registered_element",
        "compile_availability": "available" if available else "unavailable",
    }


def _public_refs(candidate: Mapping[str, Any], errors: list[str]) -> dict[str, Any]:
    allowed = (
        "project_id",
        "timeline_id",
        "revision_id",
        "occurrence_id",
        "shot_id",
        "shot_revision_id",
        "internal_timeline_revision_id",
        "clip_id",
        "authored_clip_id",
        "source_kind",
        "source_path",
        "interval_frames",
    )
    return _sanitize_refs(
        {key: candidate[key] for key in allowed if key in candidate and candidate[key] is not None},
        errors,
    )


def _finding(
    *,
    category: str,
    known: bool,
    properties: Sequence[str],
    source_paths: Sequence[str],
    refs: Mapping[str, Any],
    errors: list[str],
    interval_frames: Sequence[int] | None = None,
    compile_availability: str | None = None,
) -> dict[str, Any]:
    safe_refs = _sanitize_refs(refs, errors)
    result: dict[str, Any] = {
        **safe_refs,
        "semantic_category": category,
        "knowledge": "known" if known and safe_refs == dict(refs) else "unknown",
        "properties": _dedupe(properties),
        "source_paths": _dedupe(source_paths),
    }
    if interval_frames is not None:
        result["interval_frames"] = list(interval_frames)
    if compile_availability is not None:
        result["compile_availability"] = compile_availability
    return result


def _track_and_asset_context(
    clip: Mapping[str, Any], config: Mapping[str, Any], registry: Mapping[str, Any]
) -> tuple[bool, list[str]]:
    track_id = clip.get("track")
    tracks = config.get("tracks")
    assets = registry.get("assets")
    if not isinstance(track_id, str) or not isinstance(tracks, list) or not isinstance(assets, Mapping):
        return False, []
    track_index = next(
        (index for index, row in enumerate(tracks) if isinstance(row, Mapping) and row.get("id") == track_id),
        None,
    )
    if track_index is None:
        return False, []
    track = tracks[track_index]
    role = track.get("role")
    asset_id = next(
        (clip.get(key) for key in ("asset", "asset_id", "media_id", "object_id") if clip.get(key) is not None),
        None,
    )
    asset = assets.get(asset_id) if isinstance(asset_id, str) else None
    asset_type = asset.get("type") if isinstance(asset, Mapping) else None
    media_type = asset.get("media_type") if isinstance(asset, Mapping) else None
    raw_type = asset_type if isinstance(asset_type, str) else media_type
    normalized_type = raw_type.strip().lower() if isinstance(raw_type, str) else ""
    known = isinstance(role, str) and role.lower() in _AUDIO_ROLES and (
        normalized_type in _AUDIO_ASSET_TYPES or normalized_type.startswith("audio/")
    )
    source_paths = [f"projected.config.tracks[{track_index}].role"]
    if isinstance(asset_id, str):
        source_paths.append(f"projected.registry.assets[{asset_id!r}].type")
    return known, source_paths


def _audio_fade_observations(
    clip: Mapping[str, Any], *, source_path: str | None, fps: float, config: Mapping[str, Any], registry: Mapping[str, Any], api: Mapping[str, Any]
) -> list[tuple[str, bool, bool, list[str], list[str], bool]]:
    audio_curves = api["audio_curves"]
    observations: list[tuple[str, bool, bool, list[str], list[str], bool]] = []
    audio_known, audio_paths = _track_and_asset_context(clip, config, registry)
    for name, fade_path in _AUDIO_FADE_PATHS.items():
        duration = _dotted(clip, fade_path)
        curve_path = _AUDIO_CURVE_PATHS[name]
        raw_curve = _dotted(clip, curve_path)
        if duration is None and raw_curve is None:
            continue
        properties = [name, fade_path]
        source_paths = [f"{source_path}.{fade_path}"] if source_path else []
        curve_present = raw_curve is not None and raw_curve != "linear"
        curve_known = True
        if raw_curve is not None:
            properties.append(curve_path)
            if source_path:
                source_paths.append(f"{source_path}.{curve_path}")
            try:
                audio_curves.validate(raw_curve)
            except (TypeError, ValueError):
                curve_known = False
        observations.append((name, curve_present, curve_known, properties, [*source_paths, *audio_paths], audio_known))
    return observations


def _look_inventory(
    record: Mapping[str, Any],
    properties: Sequence[str],
    source_paths: Sequence[str],
    errors: list[str],
    *,
    knowledge: str = "known",
) -> dict[str, Any]:
    result = _public_refs(record, errors)
    result.update(
        {
            "knowledge": knowledge,
            "properties": _dedupe(properties),
            "source_paths": _dedupe(source_paths),
            "interval_frames": list(record["interval_frames"]),
        }
    )
    return result


def _transition_inventory(
    clip: Mapping[str, Any], record: Mapping[str, Any], *, fps: float, api: Mapping[str, Any], errors: list[str]
) -> dict[str, Any] | None:
    source_path = record.get("source_path")
    error = f"{source_path}.transition is unreadable" if isinstance(source_path, str) else "transition is unreadable"
    try:
        transition = api["clip_fields"].read(clip, "transition", fps=fps)
    except Exception:  # noqa: BLE001 - unreadable declarations make the scan incomplete
        _add_error(errors, error)
        return None
    if transition is None:
        return None
    if not isinstance(transition, Mapping) or any(
        transition.get(key) is not None and not isinstance(transition[key], str)
        for key in ("id", "type")
    ):
        _add_error(errors, error)
        return None
    transition_id = transition.get("id")
    transition_type = transition.get("type")
    if not isinstance(transition_id, str) or not transition_id:
        transition_id = transition_type
    if not isinstance(transition_id, str) or not transition_id:
        _add_error(errors, error)
        return None
    if not isinstance(transition_type, str) or not transition_type:
        transition_type = transition_id
    result = _public_refs(record, errors)
    result.update(
        {
            "transition_id": transition_id,
            "transition_type": transition_type,
            "semantics": "incoming",
            "interval_frames": list(record["interval_frames"]),
            "source_paths": _dedupe(
                [
                    f"{record['source_path']}.transition"
                    if isinstance(record.get("source_path"), str)
                    else ""
                ]
            ),
        }
    )
    return result


def _closure_error(
    document: Mapping[str, Any], errors: Sequence[str], refs: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    result = {
        "version": VERSION,
        "status": "incomplete",
        "closure_errors": list(errors),
        "fps_rational": None,
        "input_authority": "runtime_canonical_document",
        "evidence_kind": "synthetic_or_unverified_canonical_input",
        "semantic_categories": list(SEMANTIC_CATEGORIES),
        "not_covered": list(_NOT_COVERED),
        "transition_boundaries": [],
        "media_look_inventory": [],
        "finding_count": 0,
        "findings": [],
        "clean_claim": False,
    }
    if refs:
        result.update(refs)
    return result


def scan(document: Mapping[str, Any], *, agent_root: str | os.PathLike[str]) -> dict[str, Any]:
    """Scan one supplied closure; never claim that an owner film is clean."""
    errors: list[str] = []
    if not isinstance(document, Mapping):
        return _closure_error({}, ["input JSON must be an object"])
    scope_refs: dict[str, Any] = {}
    for field in ("project_id", "timeline_id"):
        if field not in document:
            continue
        value = _sanitize_ref_value(field, document[field], errors, allow_none=False)
        if value is not None:
            scope_refs[field] = value
    parent = document.get("parent_revision")
    if isinstance(parent, Mapping) and "revision_id" in parent:
        revision_id = _sanitize_ref_value("revision_id", parent["revision_id"], errors, allow_none=False)
        if revision_id is not None:
            scope_refs["revision_id"] = revision_id
    required = (
        "project_id",
        "timeline_id",
        "parent_revision",
        "shot_revisions",
        "internal_timeline_revisions",
    )
    missing = [key for key in required if key not in document]
    if missing:
        _add_error(errors, f"missing top-level keys: {', '.join(missing)}")
        return _closure_error(document, errors, scope_refs)
    try:
        parent = _mapping(document["parent_revision"], "parent_revision")
    except ValueError as exc:
        return _closure_error(document, [str(exc)], scope_refs)
    if not isinstance(parent.get("payload"), Mapping):
        _add_error(errors, "parent_revision.payload is absent")
        return _closure_error(document, errors, scope_refs)
    if document.get("schema_version") != 1:
        _add_error(errors, "schema_version is not 1")
    if "dependency_manifest" not in document:
        _add_error(errors, "dependency_manifest is absent")
    try:
        api = _agent_api(agent_root)
        projected = api["project_runtime_parent_composition"](
            parent,
            shot_revisions=document["shot_revisions"],
            internal_timeline_revisions=document["internal_timeline_revisions"],
        )
    except Exception as exc:  # noqa: BLE001 - projection is the exact closure boundary
        _add_error(errors, f"canonical projection unavailable: {type(exc).__name__}")
        return _closure_error(document, errors, scope_refs)
    config = _mapping(projected.config, "projected.config")
    try:
        fps_rational = _fps_rational(config, api)
    except Exception as exc:  # noqa: BLE001 - timing setup fails closed
        _add_error(errors, f"rational FPS unavailable: {type(exc).__name__}")
        return _closure_error(document, errors, scope_refs)
    fps = fps_rational[0] / fps_rational[1]
    try:
        registry = api["load_default_registry"](project_root=api["root"])
    except Exception as exc:  # noqa: BLE001 - registry failure remains unknown
        registry = None
        _add_error(errors, f"Agent element registry unavailable: {type(exc).__name__}")
    try:
        source_paths = _raw_clip_sources(document)
    except Exception as exc:  # noqa: BLE001 - malformed source paths remain bounded
        source_paths = {}
        _add_error(errors, f"source paths unavailable: {type(exc).__name__}")
    records: list[tuple[Mapping[str, Any], dict[str, Any]]] = []
    element_candidates: list[dict[str, Any]] = []
    transition_boundaries: list[dict[str, Any]] = []
    media_look_inventory: list[dict[str, Any]] = []
    for clip in config.get("clips", []):
        if not isinstance(clip, Mapping):
            continue
        clip_id = clip.get("id")
        source = dict(source_paths.get(clip_id, {})) if isinstance(clip_id, str) else {}
        source.update(scope_refs)
        try:
            interval = [
                api["clip_start_frame"](clip, fps),
                api["clip_end_frame"](clip, fps),
            ]
        except Exception as exc:  # noqa: BLE001 - one malformed clip remains incomplete
            _add_error(errors, f"clip timing unavailable: {type(exc).__name__}")
            continue
        record = {
            **source,
            "interval_frames": interval,
        }
        if isinstance(clip_id, str):
            record["clip_id"] = clip_id
        records.append((clip, record))
        source_path = source.get("source_path")
        look_paths = _look_source_paths(clip, source_path, api["clip_fields"])
        look_names = [name for name in _LOOK_NAMES if name in look_paths]
        look_decode_failed = False
        try:
            described = api["clip_fields"].describe(clip, fps=fps)
        except Exception:  # noqa: BLE001 - unreadable looks make the scan incomplete
            unreadable = _unreadable_look_names(
                clip,
                fps=fps,
                clip_fields=api["clip_fields"],
                names=look_names,
            )
            for name in unreadable:
                _add_error(errors, f"{look_paths[name]} is unreadable")
            look_decode_failed = bool(unreadable)
            described = {}
        if clip.get("clipType", clip.get("clip_type", "media")) in {"media", "video", "image"}:
            media_properties = (
                [name for name in _MEDIA_LOOK_NAMES if name in look_names]
                if look_decode_failed
                else [name for name in _MEDIA_LOOK_NAMES if name in described]
            )
            if media_properties:
                media_look_inventory.append(
                    _look_inventory(
                        record,
                        media_properties,
                        [look_paths[name] for name in media_properties if name in look_paths],
                        errors,
                        knowledge="unknown" if look_decode_failed else "known",
                    )
                )
        transition = _transition_inventory(clip, record, fps=fps, api=api, errors=errors)
        if transition is not None:
            transition_boundaries.append(transition)
        info = _element_info(clip, registry, api["root"])
        if info["classification"] != "not_element":
            look_properties = (
                look_names if look_decode_failed else [name for name in _LOOK_NAMES if name in described]
            )
            element_candidates.append(
                {
                    **record,
                    "track_id": clip.get("track"),
                    "classification": (
                        "unknown_candidate" if look_decode_failed else info["classification"]
                    ),
                    "compile_availability": (
                        "unknown" if look_decode_failed else info["compile_availability"]
                    ),
                    "properties": look_properties,
                    "source_paths": [look_paths[name] for name in look_properties if name in look_paths],
                }
            )

    findings: list[dict[str, Any]] = []
    projected_registry = projected.registry if isinstance(projected.registry, Mapping) else {}
    for clip, record in records:
        refs = _public_refs(record, errors)
        for name, curve_present, curve_known, properties, paths, audio_known in _audio_fade_observations(
            clip, source_path=record.get("source_path"), fps=fps, config=config, registry=projected_registry, api=api
        ):
            findings.append(
                _finding(
                    category="continuous_audio_fade",
                    known=audio_known,
                    properties=properties,
                    source_paths=paths,
                    refs=refs,
                    errors=errors,
                    interval_frames=record["interval_frames"],
                )
            )
            if curve_present:
                findings.append(
                    _finding(
                        category="curve_honoured",
                        known=audio_known and curve_known,
                        properties=properties,
                        source_paths=paths,
                        refs=refs,
                        errors=errors,
                        interval_frames=record["interval_frames"],
                    )
                )
    for candidate in element_candidates:
        if not candidate["properties"]:
            continue
        known = candidate["classification"] == "registered_element"
        findings.append(
            _finding(
                category="element_clip_look_overlap",
                known=known,
                properties=candidate["properties"],
                source_paths=candidate["source_paths"],
                refs={**scope_refs, "clip_ids": [candidate.get("clip_id")]},
                errors=errors,
                interval_frames=candidate["interval_frames"],
                compile_availability=(
                    "available" if known and candidate["compile_availability"] == "available" else "unknown"
                ),
            )
        )
    for left, right in combinations(element_candidates, 2):
        if not left["properties"] and not right["properties"]:
            continue
        start = max(left["interval_frames"][0], right["interval_frames"][0])
        end = min(left["interval_frames"][1], right["interval_frames"][1])
        if start >= end:
            continue
        known = left["classification"] == right["classification"] == "registered_element"
        findings.append(
            _finding(
                category="element_clip_look_overlap",
                known=known,
                properties=[*left["properties"], *right["properties"]],
                source_paths=[*left["source_paths"], *right["source_paths"]],
                refs={
                    **scope_refs,
                    "clip_ids": [left.get("clip_id"), right.get("clip_id")],
                    "occurrence_ids": _dedupe([left.get("occurrence_id"), right.get("occurrence_id")]),
                    "source_kinds": _dedupe([left.get("source_kind"), right.get("source_kind")]),
                },
                errors=errors,
                interval_frames=[start, end],
                compile_availability=(
                    "available"
                    if known and left["compile_availability"] == right["compile_availability"] == "available"
                    else "unknown"
                ),
            )
        )
    result = {
        "version": VERSION,
        "status": "incomplete" if errors else "complete",
        "closure_errors": errors,
        "fps_rational": list(fps_rational),
        "input_authority": "runtime_canonical_document",
        "evidence_kind": "synthetic_or_unverified_canonical_input",
        "semantic_categories": list(SEMANTIC_CATEGORIES),
        "not_covered": list(_NOT_COVERED),
        "transition_boundaries": transition_boundaries,
        "media_look_inventory": media_look_inventory,
        "finding_count": len(findings),
        "findings": findings,
        "clean_claim": False,
    }
    result.update(scope_refs)
    return result


def _load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, Mapping) and isinstance(value.get("data"), Mapping):
        value = value["data"]
    if isinstance(value, Mapping) and isinstance(value.get("canonical_document"), Mapping):
        value = value["canonical_document"]
    return _mapping(value, "input JSON")


def _reject_output_alias(input_path: Path, output_path: Path) -> None:
    """Reject same-file, symlink, and hardlink outputs before any write."""
    input_stat = input_path.stat()
    input_resolved = input_path.resolve(strict=True)
    if output_path.is_symlink():
        raise ValueError("--json-out must not be a symlink")
    if output_path.exists():
        output_stat = output_path.stat()
        if output_path.resolve(strict=True) == input_resolved or (
            output_stat.st_dev == input_stat.st_dev and output_stat.st_ino == input_stat.st_ino
        ):
            raise ValueError("--json-out must not alias --input")


def _write_json_safely(input_path: Path, output_path: Path, text: str) -> None:
    _reject_output_alias(input_path, output_path)
    output_path.parent.mkdir(parents=False, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=output_path.parent, prefix=f".{output_path.name}.", suffix=".tmp", delete=False
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        _reject_output_alias(input_path, output_path)
        os.replace(temp_path, output_path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="immutable Runtime canonical-document JSON closure")
    parser.add_argument("--agent-root", type=Path, required=True, help="extracted Agent repository root")
    parser.add_argument("--json-out", type=Path, help="write bounded JSON report; stdout is always emitted")
    args = parser.parse_args(argv)
    input_path = args.input.expanduser()
    if input_path.is_symlink() or not input_path.is_file():
        parser.error("--input must name a regular canonical-document JSON file, not a symlink")
    input_path = input_path.resolve(strict=True)
    if args.json_out is not None:
        try:
            _reject_output_alias(input_path, args.json_out.expanduser())
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
    try:
        result = scan(_load_json(input_path), agent_root=args.agent_root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    output = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.json_out is not None:
        try:
            _write_json_safely(input_path, args.json_out.expanduser(), output)
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


