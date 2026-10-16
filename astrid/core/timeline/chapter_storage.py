"""Pure storage adaptation for exact parent/shot closures.

The working model stays flat. ``structure_base`` is an immutable physical
baseline, verified from the closure digests, never a caller's opt-in flag.
Resolved frames come from the SDK's existing story/timing compiler.
"""
from __future__ import annotations

import copy
import math
import re
from collections.abc import Mapping, Sequence
from typing import Any

from . import astrid_ns
from .authoring_bundle import AuthoringBundleError, _digest, _identity
from .cuts import bundle_fps, clip_duration


class ChapterStorageError(AuthoringBundleError):
    """A lossless chapter projection is unavailable; no effects are permitted."""


def _ranges(bundle):
    return astrid_ns.film_intent(bundle.get("parent", {}).get("config", {})).get("ranges", [])


def _chapters(bundle):
    rows = _ranges(bundle)
    if not isinstance(rows, list):
        raise ChapterStorageError("canonical story ranges must be a list")
    return [r for r in rows if isinstance(r, Mapping) and r.get("kind") == "chapter"]


def _start(row):
    placement = row.get("placement", {})
    return row.get("at_ms", placement.get("start_ms", 0))


def _number(value, path):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ChapterStorageError(f"{path} must be a finite number")
    return value


def _placement(row):
    # Keep opaque occurrence data only where it has an exact owner. Applying
    # transforms, trimming, gain or mute while moving film clips is lossy.
    allowed = {"occurrence_id", "shot_id", "at_ms", "placement", "duration_ms", "source_offset",
               "source_offset_ms", "speed", "track", "transform", "gain", "muted", "mute", "provenance"}
    if set(row) - allowed:
        raise ChapterStorageError("unsupported opaque placement fields for chapter conversion")
    if (row.get("source_offset", row.get("source_offset_ms", 0)) != 0 or row.get("speed", 1) != 1
            or row.get("transform", {}) != {} or row.get("gain", 1) != 1
            or row.get("muted", row.get("mute", False)) is not False or row.get("track") not in (None, "picture")):
        raise ChapterStorageError("chapter conversion requires identity placement transform, offset, speed, gain and track")
    placement = row.get("placement", {})
    if not isinstance(placement, Mapping) or set(placement) - {"start_ms", "track"} or placement.get("track") not in (None, "picture"):
        raise ChapterStorageError("unsupported nested placement for chapter conversion")
    if "at_ms" in row and "start_ms" in placement and row["at_ms"] != placement["start_ms"]:
        raise ChapterStorageError("conflicting placement clocks")
    _number(_start(row), "placement start")
    _number(row.get("duration_ms"), "placement duration")
    if row["duration_ms"] <= 0:
        raise ChapterStorageError("chapter placement duration must be positive")


def _set_start(row, ms):
    if "at_ms" in row:
        row["at_ms"] = ms
    else:
        row.setdefault("placement", {})["start_ms"] = ms
    if "start_ms" in row.get("placement", {}):
        row["placement"]["start_ms"] = ms


def _project_closure(parent_revision, *, shot_revisions, internal_timeline_revisions):
    from .shot_composition_projection import (
        ShotCompositionProjectionError,
        project_runtime_parent_composition,
    )
    try:
        return project_runtime_parent_composition(
            parent_revision, shot_revisions=shot_revisions,
            internal_timeline_revisions=internal_timeline_revisions)
    except ShotCompositionProjectionError as exc:
        raise ChapterStorageError(str(exc)) from exc


def _project(bundle):
    """Use B's existing projection, including its one track reconciliation path."""
    shots, internals, occurrences = [], [], []
    for index, row in enumerate(bundle["placements"]):
        sid = row["shot_id"]
        shot = bundle["shots"][sid]
        irid, srid = f"chapter-view-internal-{index}", f"chapter-view-shot-{index}"
        payload = {**copy.deepcopy(shot["payload"]), "internal_timeline_revision_id": irid}
        shots.append(dict(project_id=bundle["project_id"], shot_id=sid, revision_id=srid,
                          internal_timeline_revision_id=irid, payload=payload))
        internals.append(dict(project_id=bundle["project_id"], timeline_id=sid,
                              revision_id=irid, payload=copy.deepcopy(shot["internal_timeline"])))
        occurrences.append({**copy.deepcopy(row), "shot_revision_id": srid})
    projected = _project_closure(
        dict(project_id=bundle["project_id"], timeline_id=bundle["timeline_id"],
             revision_id=bundle["base_parent"]["revision_id"],
             payload={**copy.deepcopy(bundle["parent"]), "occurrences": occurrences}),
        shot_revisions=shots, internal_timeline_revisions=internals)
    _assert_track_projection_preserves_sources(bundle, projected.config.get("tracks", []))
    return projected


def _assert_track_projection_preserves_sources(bundle, projected):
    """Validate B's projection, never resolve/merge competing definitions here.

    This also fails closed on an older projection that silently discarded a
    child track field. B's existing projection remains the only merge owner.
    """
    from .authoring_bundle import _canonical_json
    by_id = {row.get("id"): row for row in projected}
    if len(by_id) != len(projected):
        raise ChapterStorageError("projected track identities are ambiguous")

    def contains(actual, source):
        if isinstance(actual, Mapping) and isinstance(source, Mapping):
            return all(key in actual and contains(actual[key], value) for key, value in source.items())
        return _canonical_json(actual) == _canonical_json(source)

    collections = [bundle["parent"].get("config", {}).get("tracks", [])]
    collections += [bundle["shots"][row["shot_id"]]["internal_timeline"].get("tracks", [])
                    for row in bundle["placements"]]
    for rows in collections:
        for source in rows:
            actual = by_id.get(source.get("id"))
            if (actual is None or _canonical_json({k: v for k, v in source.items() if k != "app"}) !=
                    _canonical_json({k: v for k, v in actual.items() if k != "app"}) or
                    ("app" in source and ("app" not in actual or not contains(actual["app"], source["app"])))):
                raise ChapterStorageError("shared track projection does not preserve every source definition")
    timelines = [bundle["parent"], *[bundle["shots"][r["shot_id"]]["internal_timeline"]
                                    for r in bundle["placements"]]]
    for timeline in timelines:
        for clip in timeline.get("clips", []):
            if clip.get("track") not in by_id:
                raise ChapterStorageError("shared track projection leaves an unresolved clip.track reference")


def _merge_assets(parent, internals):
    from .parent_registry import effective_parent_registry
    registry = copy.deepcopy(effective_parent_registry(parent))
    assets = registry.setdefault("assets", {})
    for internal in internals:
        child = internal.get("registry", {})
        if not isinstance(child, Mapping) or set(child) - {"assets"}:
            raise ChapterStorageError("chapter registry has unsupported non-asset state")
        for key, value in child.get("assets", {}).items():
            if key in assets and assets[key] != value:
                raise ChapterStorageError(f"conflicting chapter asset {key!r}")
            assets[key] = copy.deepcopy(value)
    return registry


def _clips(parent):
    primary = parent.get("clips", [])
    alternate = parent.get("config", {}).get("clips", [])
    if alternate and primary and alternate != primary:
        raise ChapterStorageError("parent has competing clip lists")
    return primary or alternate


def _internal_supported(internal):
    if any(value not in (None, {}, []) for key, value in internal.items()
           if key not in {"clips", "tracks", "registry"}):
        raise ChapterStorageError("unsupported chapter-level renderer state")


def _flat(bundle, *, projection=None):
    """Flatten a supported physical baseline, preserving all opaque child data."""
    rows = bundle["placements"]
    if len({r["shot_id"] for r in rows}) != len(rows):
        raise ChapterStorageError("shared chapter shots cannot be flattened losslessly")
    internals = [bundle["shots"][r["shot_id"]]["internal_timeline"] for r in rows]
    cursor = 0
    clips, ids = copy.deepcopy(_clips(bundle["parent"])), set()
    for clip in clips:
        if clip.get("id") in ids:
            raise ChapterStorageError("duplicate film clip identity")
        ids.add(clip.get("id"))
    prototype = {k: v for k, v in internals[0].items() if k not in {"clips", "tracks", "registry"}}
    for row, internal in zip(rows, internals):
        _placement(row)
        _internal_supported(internal)
        if _start(row) != cursor:
            raise ChapterStorageError("chapter placements must be contiguous from frame zero")
        # Effects/audio/layout/unknown renderer state is never discarded or
        # flattened across a wall where its meaning could change.
        other = {k: v for k, v in internal.items() if k not in {"clips", "tracks", "registry"}}
        if other != prototype or internal.get("effects") or internal.get("audio"):
            raise ChapterStorageError("unsupported chapter-level renderer state")
        for clip in internal.get("clips", []):
            value = copy.deepcopy(clip)
            if value.get("id") in ids:
                raise ChapterStorageError(f"duplicate flattened clip identity {value.get('id')!r}")
            ids.add(value.get("id"))
            at = _number(value.get("at", 0), "clip.at")
            duration = clip_duration(value)
            if at < 0 or duration < 0 or (at + duration) * 1000 > row["duration_ms"] + 1e-7:
                raise ChapterStorageError("chapter clip extends beyond its occurrence window")
            value["at"] = at + cursor / 1000
            clips.append(value)
        cursor += row["duration_ms"]
    out = copy.deepcopy(dict(bundle))
    first = rows[0]
    sid = first["shot_id"]
    parent = out["parent"]
    parent["clips"] = []
    parent.setdefault("config", {}).pop("clips", None)
    parent["config"]["tracks"] = copy.deepcopy((projection or _project(bundle)).config.get("tracks", []))
    _assert_track_projection_preserves_sources(bundle, parent["config"]["tracks"])
    # Assets may be shared across chapters. Keep the one complete authority on
    # the film; references and clip payloads remain byte-for-byte intact.
    parent["registry"] = _merge_assets(bundle["parent"], internals)
    if "registry" in parent["config"]:
        parent["config"]["registry"] = copy.deepcopy(parent["registry"])
    row = copy.deepcopy(first)
    row["duration_ms"] = cursor
    shot = copy.deepcopy(out["shots"][sid])
    # Legacy producer names are chapter display labels. The current producer
    # retains the complete original first-shot payload, including its name.
    if not _generated_storage(rows):
        shot["payload"].pop("name", None)
        shot["base_payload"].pop("name", None)
    internal = shot["internal_timeline"]
    internal.update(clips=clips, tracks=[], registry={})
    shot["base_internal_timeline"] = copy.deepcopy(internal)
    out["shots"] = {sid: shot}
    out["placements"] = [row]
    out["base_parent_payload"] = copy.deepcopy(parent)
    out["base_placements"] = {row["occurrence_id"]: copy.deepcopy(row)}
    out["source_mapping"]["placements"] = copy.deepcopy(out["base_placements"])
    out["source_mapping"]["shots"] = {sid: copy.deepcopy(bundle["source_mapping"]["shots"][sid])}
    return out


def _generated_storage(rows):
    # First opt-in retains the original flat shot, including its authored name.
    # The remaining identities are the canonical allocator's existing strings;
    # exact occurrence pins and closure digests still provide the authority.
    return len(rows) >= 2 and all(
        re.fullmatch(r"chapter-shot-[0-9a-f]{64}", row["shot_id"]) and
        row["occurrence_id"] == _identity("chapter-occurrence", row["shot_id"])
        for row in rows[1:])


def is_chapter_storage(bundle):
    rows = bundle.get("placements", [])
    if len(rows) < 2:
        return False
    if not isinstance(_ranges(bundle), list):
        return False
    chapters = _chapters(bundle)
    if len(rows) < 2 or len(rows) != len(chapters):
        return False
    names = [bundle["shots"][r["shot_id"]]["payload"].get("name", bundle["shots"][r["shot_id"]]["payload"].get("metadata", {}).get("name")) for r in rows]
    if names != [c["name"] for c in chapters] and not _generated_storage(rows):
        return False
    return True


def flatten_chapter_storage(bundle: Mapping[str, Any], *, projection=None) -> dict[str, Any]:
    """Flatten recognized physical chapter-shot storage into ordinary authoring."""
    if "structure_base" in bundle or "storage_policy" in bundle:
        raise ChapterStorageError("closure opener cannot accept injected storage metadata")
    if not is_chapter_storage(bundle):
        return copy.deepcopy(dict(bundle))
    out = _flat(bundle, projection=projection)
    out["structure_base"] = copy.deepcopy(dict(bundle))
    out["storage_policy"] = "chapters"
    return out


def _baseline(bundle):
    out = copy.deepcopy(dict(bundle))
    out["parent"] = copy.deepcopy(bundle["base_parent_payload"])
    out["placements"] = sorted(copy.deepcopy(bundle["base_placements"]).values(), key=_start)
    for shot in out["shots"].values():
        shot["payload"] = copy.deepcopy(shot["base_payload"])
        shot["internal_timeline"] = copy.deepcopy(shot["base_internal_timeline"])
    return out


def validate_structure_base(candidate: Mapping[str, Any]) -> dict[str, Any]:
    try:
        return _validate_structure_base(candidate)
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ChapterStorageError("malformed physical structure_base or working baseline") from exc


def _validate_structure_base(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Authenticate physical provenance, including all child bytes and pins."""
    base = candidate.get("structure_base")
    if not isinstance(base, Mapping) or "structure_base" in base or "storage_policy" in base:
        raise ChapterStorageError("invalid physical structure_base")
    if any(candidate.get(k) != base.get(k) for k in ("project_id", "timeline_id", "base_parent")):
        raise ChapterStorageError("physical structure_base identity differs from immutable base")
    if base != _baseline(base):
        raise ChapterStorageError("structure_base contains edits instead of an exact closure")
    pins = base["source_mapping"]["shots"]
    if base["source_mapping"]["placements"] != base["base_placements"]:
        raise ChapterStorageError("physical structure_base placement mapping mismatch")
    if set(pins) != set(base["shots"]) or set(base["shots"]) != {r["shot_id"] for r in base["placements"]}:
        raise ChapterStorageError("physical structure_base shot mapping mismatch")
    occurrences = []
    for row in base["placements"]:
        sid = row["shot_id"]
        source, shot = pins[sid], base["shots"][sid]
        if source.get("shot_id") != sid or any(k != v for k, v in source.get("item_id_map", {}).items()):
            raise ChapterStorageError("chapter storage requires independent physical identities")
        if (_digest(shot["payload"]) != source["content_digest"]
                or _digest(shot["internal_timeline"]) != source["internal_timeline_content_digest"]
                or shot["payload"].get("internal_timeline_revision_id") != source["internal_timeline_revision_id"]):
            raise ChapterStorageError("physical structure_base child digest/pin mismatch")
        occurrences.append({**copy.deepcopy(row), "shot_revision_id": source["revision_id"]})
    payload = {**copy.deepcopy(base["parent"]), "occurrences": occurrences}
    if _digest(payload) != base["base_parent"]["content_digest"]:
        raise ChapterStorageError("physical structure_base parent digest mismatch")
    expected = flatten_chapter_storage(base)
    if "structure_base" not in expected:
        raise ChapterStorageError("structure_base is not recognized chapter storage")
    actual = _baseline(candidate)
    for key in ("base_parent_payload", "base_placements", "shots", "placements", "parent"):
        # Compare known lossless namespace migrations without trusting edits to
        # the baseline. source_mapping itself can carry other admitted imports.
        if astrid_ns.normalized({key: actual[key]}) != astrid_ns.normalized({key: expected[key]}):
            raise ChapterStorageError(f"flattened {key} differs from exact structure_base")
    if candidate["source_mapping"]["placements"] != expected["source_mapping"]["placements"]:
        raise ChapterStorageError("flattened placement source mapping differs from structure_base")
    for sid, source in expected["source_mapping"]["shots"].items():
        actual_source = candidate["source_mapping"]["shots"].get(sid, {})
        if any(actual_source.get(k) != v for k, v in source.items() if k != "linked"):
            raise ChapterStorageError("flattened source mapping differs from structure_base")
    return copy.deepcopy(dict(base))


def _bounds(bundle, resolved):
    chapters = _chapters(bundle)
    if len(chapters) < 2:
        raise ChapterStorageError("restructure requires at least two resolved canonical chapter ranges")
    if not isinstance(resolved, Sequence) or len(resolved) != len(chapters):
        raise ChapterStorageError("resolved canonical chapters are required")
    fps = bundle_fps(dict(bundle)) or 30.0
    end = bundle["placements"][0]["duration_ms"]
    cursor, bounds = 0, []
    for chapter, row in zip(chapters, resolved):
        if row.get("range") != chapter:
            raise ChapterStorageError("resolved chapters differ from current canonical ranges")
        lo, hi = row.get("start_frame"), row.get("end_frame")
        if type(lo) is not int or type(hi) is not int or hi <= lo:
            raise ChapterStorageError("chapter edges must resolve to strictly ordered frames")
        a, b = lo * 1000 / fps, hi * 1000 / fps
        if abs(a - round(a)) > 1e-7 or abs(b - round(b)) > 1e-7:
            raise ChapterStorageError("chapter frame boundary is not representable by the occurrence millisecond clock")
        a, b = round(a), round(b)
        if a != cursor:
            raise ChapterStorageError("chapter ranges must cover the film contiguously from frame zero")
        bounds.append((a, b))
        cursor = b
    if cursor != end:
        raise ChapterStorageError("chapter ranges must end at the exact film end")
    return chapters, bounds


def split_chapter_storage(candidate: Mapping[str, Any], *, chapters=None) -> dict[str, Any]:
    """Prepare one physical candidate for the existing final compiler; no I/O."""
    old = validate_structure_base(candidate) if "structure_base" in candidate else None
    policy = candidate.get("storage_policy")
    if policy not in (None, "chapters"):
        raise ChapterStorageError("unsupported semantic storage policy")
    if policy == "chapters" and chapters is not None:
        _bounds(candidate, chapters)
    if old and policy == "chapters":
        baseline = _baseline(candidate)
        # An exact no-op must reuse the entire original physical closure,
        # including equal legacy track mirrors. Canonicalization needs an edit.
        if all(candidate[k] == baseline[k] for k in ("parent", "placements", "shots")):
            return old
    if not old and policy is None:
        return copy.deepcopy(dict(candidate))
    rows = candidate.get("placements", [])
    if len(rows) != 1 or _start(rows[0]) != 0:
        raise ChapterStorageError("chapter conversion requires one flat occurrence placed at zero")
    row = rows[0]
    _placement(row)
    sid = row["shot_id"]
    logical = candidate["shots"][sid]
    internal = logical["internal_timeline"]
    _internal_supported(internal)
    out = copy.deepcopy(old or dict(candidate))
    out.pop("structure_base", None)
    out.pop("storage_policy", None)
    # Keep exact physical baseline source mappings for deterministic materialization.
    out["parent"] = copy.deepcopy(candidate["parent"])
    if policy is None:  # the guarded inverse of an explicit storage opt-in
        previous = out["shots"][sid]
        previous["payload"] = copy.deepcopy(logical["payload"])
        previous["internal_timeline"] = copy.deepcopy(internal)
        out["shots"] = {sid: previous}
        out["placements"] = copy.deepcopy(rows)
        return out
    selected, bounds = _bounds(candidate, chapters)
    tracks = copy.deepcopy(_project(candidate).config.get("tracks", []))
    registry = _merge_assets(candidate["parent"], [internal])
    parent = out["parent"]
    parent.setdefault("config", {})["tracks"] = tracks
    parent["registry"] = registry
    if "registry" in parent["config"]:
        parent["config"]["registry"] = copy.deepcopy(registry)
    parent["config"].pop("clips", None)
    parent["clips"] = []
    if "tracks" in parent:
        raise ChapterStorageError("canonical chapter conversion requires parent.config.tracks as its sole track owner")
    collected = [copy.deepcopy(c) for c in _clips(candidate["parent"])] + copy.deepcopy(internal.get("clips", []))
    if len({c.get("id") for c in collected}) != len(collected):
        raise ChapterStorageError("duplicate film/shot clip identities")
    clips = [[] for _ in bounds]
    music = {t["id"] for t in tracks if t.get("kind") == "music" or t.get("id") == "music"}
    film_end = row["duration_ms"] / 1000
    for clip in collected:
        at = _number(clip.get("at", 0), "clip.at")
        duration = _number(clip_duration(clip), "clip duration")
        if at < 0 or duration <= 0 or at + duration > film_end + 1e-9:
            raise ChapterStorageError("clip is not fully representable within the flat film window")
        index = next((i for i, (a, b) in enumerate(bounds) if a / 1000 <= at < b / 1000), None)
        if index is None:
            raise ChapterStorageError("clip start is outside the chapter film")
        if clip.get("track") in music or at + duration > bounds[index][1] / 1000 + 1e-9:
            parent["clips"].append(clip)
        else:
            clip["at"] = at - bounds[index][0] / 1000
            clips[index].append(clip)
    old_rows = old["placements"] if old else []
    if old and len(old_rows) != len(bounds):
        raise ChapterStorageError("changing chapter topology requires a new explicit storage conversion")
    placements, shots = [], {}
    for index, ((a, b), chapter) in enumerate(zip(bounds, selected)):
        if old:
            physical_row = copy.deepcopy(old_rows[index])
            physical_sid = physical_row["shot_id"]
        elif index == 0:
            physical_row, physical_sid = copy.deepcopy(row), sid
        else:
            # Names and mutable parent heads are deliberately absent. Anchors
            # bind first opt-in allocation through retries, rebase and renames.
            physical_sid = _identity("chapter-shot", candidate["project_id"], candidate["timeline_id"],
                                     row["occurrence_id"], chapter["from"], chapter["to"])
            physical_row = copy.deepcopy(row)
            physical_row.update(shot_id=physical_sid, occurrence_id=_identity("chapter-occurrence", physical_sid))
        _set_start(physical_row, a)
        physical_row["duration_ms"] = b - a
        if physical_sid in out["shots"]:
            shot = copy.deepcopy(out["shots"][physical_sid])
        else:
            source = copy.deepcopy(candidate["source_mapping"]["shots"][sid])
            source["linked"] = False
            out["source_mapping"]["shots"][physical_sid] = source
            shot = copy.deepcopy(logical)
            shot["shot_id"] = physical_sid
            shot["payload"] = {}
        if index == 0:
            shot["payload"] = copy.deepcopy(logical["payload"])
        if index > 0 or (old and not _generated_storage(old_rows)):
            shot["payload"]["name"] = chapter["name"]
        shot["internal_timeline"] = copy.deepcopy(internal)
        shot["internal_timeline"].update(clips=clips[index], tracks=[], registry={})
        shots[physical_sid] = shot
        placements.append(physical_row)
    out["shots"], out["placements"] = shots, placements
    _assert_equivalent(candidate, out)
    return out


def _render_input(bundle):
    """Compare the shared renderer projection, retaining ordering within a track."""
    from .duration import timeline_render_duration_frames
    projected = _project(bundle)
    per_track = {}
    for raw in projected.config.get("clips", []):
        clip = copy.deepcopy(raw)
        for key in ("id", "shot_id", "shot_occurrence_id", "shot_name"):
            clip.pop(key, None)
        if isinstance(clip.get("app"), dict):
            clip["app"].pop("astrid_shot_composition", None)
            if not clip["app"]:
                clip.pop("app")
        for selector in ("asset", "asset_id"):
            if isinstance(clip.get(selector), str):
                clip[selector] = projected.registry.get("assets", {}).get(clip[selector], clip[selector])
        clip.setdefault("volume", 1)
        per_track.setdefault(clip.get("track"), []).append(clip)
    return (projected.config.get("tracks", []), per_track,
            timeline_render_duration_frames(projected.config, bundle_fps(dict(bundle)) or 30.0))


def _assert_equivalent(before, after):
    old_tracks, old_clips, old_frames = _render_input(before)
    tracks, clips, frames = _render_input(after)
    if old_tracks != tracks or old_frames != frames or set(old_clips) != set(clips):
        raise ChapterStorageError("restructure changes renderer tracks or frame duration")
    for track, previous in old_clips.items():
        current = clips[track]
        if len(previous) != len(current):
            raise ChapterStorageError(f"restructure changes renderer clip count on {track!r}")
        for old, new in zip(previous, current):
            old, new = copy.deepcopy(old), copy.deepcopy(new)
            a, b = old.pop("at", 0), new.pop("at", 0)
            if old != new or abs(a - b) > 1e-9:
                raise ChapterStorageError(f"restructure changes renderer clip payload/order on {track!r}")
