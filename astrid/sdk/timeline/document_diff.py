"""Bounded editable-view adapter for detached timeline document files.

The document script is a view over one pinned authoring bundle. This module
only translates raw rows and fields with an existing EditCommand recipe. It
does not replace a parent or a whole candidate.
"""
from __future__ import annotations

import copy
import math
from collections.abc import Mapping

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import CommandError, equal
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params, capture_track_set
from astrid.sdk.timeline._trim_commands import capture_clip_trim
from astrid.sdk.timeline.capture import capture_move, occurrence_start
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_swap_media
from astrid.sdk.timeline_address import element_schema


class DocumentDiffError(ValueError):
    """The detached document contains an edit outside the native view slice."""


def _rows(value, key, path):
    if isinstance(value, Mapping):
        value = list(value.values())
    if not isinstance(value, list):
        raise DocumentDiffError(f"{path} must remain an ordered row list or identity map")
    result = {}
    for index, row in enumerate(value):
        if not isinstance(row, Mapping) or not isinstance(row.get(key), str) or not row[key]:
            raise DocumentDiffError(f"{path}[{index}] needs a stable {key} identity")
        if row[key] in result:
            raise DocumentDiffError(f"{path} has duplicate {key} identity {row[key]!r}")
        result[row[key]] = row
    return result


def _require_same(before, after, message):
    if not equal(before, after):
        raise DocumentDiffError(message)


def _require_explicit_rows(candidate_rows, result_rows, message):
    """Compare the view's explicit fields, retaining command-derived fields."""
    candidate_map = _rows(candidate_rows, "id", message + ".candidate")
    result_map = _rows(result_rows, "id", message + ".result")
    if list(candidate_map) != list(result_map):
        raise DocumentDiffError(message + " changed row membership/order")
    for identity, row in candidate_map.items():
        if any(not equal(result_map[identity].get(field), value) for field, value in row.items()):
            raise DocumentDiffError(f"{message} differs at row {identity!r}")


def _params(row):
    value = row.get("params")
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise DocumentDiffError("clip.params must remain an object or null")
    return dict(value)


def _clip_ref(owner, clip_id):
    return f"{owner}/clip:{clip_id}"


def _capture(factory, ref, *args, **kwargs):
    try:
        return factory(*args, **kwargs)
    except CommandError as exc:
        raise DocumentDiffError(f"{ref} native command is held: {exc}") from exc


def _changed_keys(before, after):
    return {key for key in set(before) | set(after) if not equal(before.get(key), after.get(key))}


def _asset_rows(timeline):
    registry = timeline.get("registry", {}) if isinstance(timeline, Mapping) else {}
    assets = registry.get("assets", {}) if isinstance(registry, Mapping) else {}
    return assets if isinstance(assets, Mapping) else {}


def _same_alias_changes(before_timeline, after_timeline, *, owner):
    before, after = _asset_rows(before_timeline), _asset_rows(after_timeline)
    if set(before) != set(after):
        raise DocumentDiffError(f"{owner} registry alias membership/order is held by the document view")
    changes = {}
    managed = {"media_id", "type", "generationId", "variantId"}
    for alias in before:
        old, new = before[alias], after[alias]
        if not isinstance(old, Mapping) or not isinstance(new, Mapping):
            raise DocumentDiffError(f"{owner}/asset:{alias} registry binding is malformed")
        changed = _changed_keys(old, new)
        if not changed:
            continue
        if not changed <= managed or old.get("media_id") == new.get("media_id"):
            raise DocumentDiffError(f"{owner}/asset:{alias} registry edits are held by the document view")
        changes[alias] = (old, new)
    return changes


def _replace_known_payload_media(payload, replacements):
    """Normalize only payload mirrors rewritten by the media planner."""
    value = copy.deepcopy(payload)
    for row in value.get("items", []) if isinstance(value.get("items"), list) else ():
        if isinstance(row, dict) and isinstance(row.get("media_id"), str):
            for old, new in replacements.items():
                if row["media_id"].removeprefix("sha256:") == new.removeprefix("sha256:"):
                    row["media_id"] = old
    for row in value.get("assets", []) if isinstance(value.get("assets"), list) else ():
        if not isinstance(row, dict):
            continue
        for container in (row, row.get("source")):
            if not isinstance(container, dict):
                continue
            for key in ("object_id", "media_id", "digest", "content_digest", "content_sha256"):
                selected = container.get(key)
                if not isinstance(selected, str):
                    continue
                for old, new in replacements.items():
                    if selected.removeprefix("sha256:") == new.removeprefix("sha256:"):
                        container[key] = old.removeprefix("sha256:") if key == "content_sha256" else old
    for row in value.get("audio_bindings", []) if isinstance(value.get("audio_bindings"), list) else ():
        if not isinstance(row, dict):
            continue
        for key in ("object_id", "media_id"):
            selected = row.get(key)
            if not isinstance(selected, str):
                continue
            for old, new in replacements.items():
                if selected.removeprefix("sha256:") == new.removeprefix("sha256:"):
                    row[key] = old
    return value


def _replace_registry_media(registry, replacements):
    value = copy.deepcopy(registry)
    assets = value.get("assets", {}) if isinstance(value, Mapping) else {}
    for alias, (old, new) in replacements.items():
        entry = assets.get(alias) if isinstance(assets, Mapping) else None
        if not isinstance(entry, dict):
            continue
        for key in ("media_id", "type", "generationId", "variantId"):
            if key in new and entry.get(key) == new.get(key):
                entry[key] = old.get(key)
    return value


def _check_clip_shape(before, after, *, owner, clip_id):
    changed = _changed_keys(before, after)
    allowed = {"at", "hold", "from", "to", "params"}
    if "asset" in changed or any(key in changed for key in ("asset_id", "media_id", "object_id")):
        raise DocumentDiffError(
            f"{_clip_ref(owner, clip_id)} media selection is held: the document view has no "
            "lossless native recipe for same-alias replacement"
        )
    unsupported = sorted(changed - allowed)
    if unsupported:
        raise DocumentDiffError(f"{_clip_ref(owner, clip_id)} changed unsupported raw fields: {unsupported}")


def _check_clip_baseline(canonical, pinned, *, owner, clip_id):
    ref = _clip_ref(owner, clip_id)
    if not equal(canonical, pinned):
        raise DocumentDiffError(f"{ref} does not match the pinned original base")


def _emit_clip_commands(working, owner, before, after):
    clip_id = before["id"]
    ref = _clip_ref(owner, clip_id)
    commands = []

    def emit(command):
        nonlocal working
        try:
            result = execute(working, [command])
        except CommandError as exc:
            raise DocumentDiffError(f"{ref} native command is held: {exc}") from exc
        commands.append(command)
        working = result.bundle

    if not equal(before.get("at"), after.get("at")):
        if (not isinstance(after.get("at"), (int, float))
                or isinstance(after.get("at"), bool)
                or not math.isfinite(after["at"])):
            raise DocumentDiffError(f"{ref}.at must be a finite literal number")
        on = after["at"]
        if owner != "parent":
            occurrence = next(row for row in working["placements"]
                              if "occurrence:" + row["occurrence_id"] == owner)
            on += occurrence_start(occurrence)
        emit(_capture(capture_move, ref, working, ref, on))

    if any(not equal(before.get(key), after.get(key)) for key in ("from", "to")):
        if owner != "parent":
            raise DocumentDiffError(f"{ref} child source trim is held by the document view")
        emit(_capture(capture_clip_trim, ref, working, ref,
                      in_s=after.get("from"), out_s=after.get("to")))

    if not equal(before.get("hold"), after.get("hold")):
        if "hold" in after:
            emit(_capture(capture_clip_set, ref, working, ref,
                          values={"hold": after["hold"]}, clear=[]))
        else:
            emit(_capture(capture_clip_set, ref, working, ref, values={}, clear=["hold"]))

    old_params, new_params = _params(before), _params(after)
    values = {key: new_params[key] for key in new_params
              if key not in old_params or not equal(old_params[key], new_params[key])}
    clear = sorted(set(old_params) - set(new_params))
    if values or clear:
        element = after.get("clipType") or after.get("clip_type") or "media"
        selected = after.get("elementRef") or after.get("element_ref")
        if isinstance(selected, Mapping) and selected.get("packId"):
            raise DocumentDiffError(f"{ref} selected-pack parameters require an exact captured schema input")
        try:
            properties = element_schema(element).get("properties", {})
        except (KeyError, TypeError, ValueError) as exc:
            raise DocumentDiffError(f"{ref} has no captured schema for params") from exc
        unsupported = sorted((set(values) | set(clear)) - set(properties))
        if unsupported:
            raise DocumentDiffError(f"{ref} changed opaque or undeclared params: {unsupported}")
        emit(_capture(capture_clip_set_params, ref, working, ref, values=values, clear=clear))
    return working, commands


def _parent_tracks(bundle):
    config = bundle.get("parent", {}).get("config", {})
    return _rows(config.get("tracks", []), "id", "parent.config.tracks")


def _native_track_commands(working, before_bundle, candidate_bundle):
    before = _parent_tracks(before_bundle)
    after = _parent_tracks(candidate_bundle)
    if list(before) != list(after):
        raise DocumentDiffError("parent track membership/order is held by the document view")
    commands = []
    for track_id, old in before.items():
        new = after[track_id]
        changed = _changed_keys(old, new)
        if changed - {"label"}:
            raise DocumentDiffError(
                f"parent/track:{track_id} changed unsupported raw fields: {sorted(changed - {'label'})}"
            )
        if "label" not in changed:
            continue
        ref = f"parent/track:{track_id}"
        command = _capture(
            capture_track_set, ref, working, ref,
            values={} if "label" not in new else {"label": new["label"]},
            clear=[] if "label" in new else ["label"],
        )
        commands.append(command)
        working = execute(working, [command]).bundle
    return working, commands


def _validate_pinned_bundle(candidate, base):
    if candidate.get("project_id") != base.get("project_id") or candidate.get("timeline_id") != base.get("timeline_id"):
        raise DocumentDiffError("document and Runtime bundle have different project/timeline scope")
    _require_same(candidate.get("base_parent_payload"), base.get("parent"),
                  "document does not contain the exact pinned parent base")
    base_placements = _rows(base.get("placements", []), "occurrence_id", "Runtime placements")
    pinned_placements = _rows(candidate.get("base_placements", []), "occurrence_id", "candidate.base_placements")
    _require_same(base_placements, pinned_placements,
                  "document does not contain the exact pinned placement base")
    source_placements = _rows(candidate.get("placements", []), "occurrence_id", "candidate.placements")
    if list(source_placements) != list(base_placements):
        raise DocumentDiffError("placement membership/order changes are held by the document view")
    _require_same(source_placements, base_placements, "placement edits are held by the document view")

    candidate_shots = candidate.get("shots")
    base_shots = base.get("shots")
    if not isinstance(candidate_shots, Mapping) or not isinstance(base_shots, Mapping):
        raise DocumentDiffError("document and Runtime bundle must contain shot maps")
    if set(candidate_shots) != set(base_shots):
        raise DocumentDiffError("shot creation/deletion is held by the document view")
    for shot_id, shot in candidate_shots.items():
        if not isinstance(shot, Mapping) or not isinstance(base_shots[shot_id], Mapping):
            raise DocumentDiffError(f"candidate.shots[{shot_id!r}] is malformed")
        runtime_shot = base_shots[shot_id]
        _require_same(shot.get("base_payload"), runtime_shot.get("payload"),
                      f"candidate.shots[{shot_id!r}].base_payload is not the pinned source")
        _require_same(shot.get("base_internal_timeline"), runtime_shot.get("internal_timeline"),
                      f"candidate.shots[{shot_id!r}].base_internal_timeline is not the pinned source")


def document_diff_to_commands(candidate, base, *, media_selections=None, verified_media=(),
                              defer_media=False):
    """Translate supported raw document fields to captured commands."""
    _validate_pinned_bundle(candidate, base)
    working = copy.deepcopy(base)
    commands = []
    working, emitted = _native_track_commands(working, base, candidate)
    commands.extend(emitted)
    canonical_shots = base["shots"]
    for shot_id, shot in candidate["shots"].items():
        owner = next(("occurrence:" + row["occurrence_id"] for row in base["placements"]
                      if row["shot_id"] == shot_id), None)
        if owner is None:
            raise DocumentDiffError(f"candidate shot {shot_id!r} has no stable occurrence owner")
        before_rows = _rows(canonical_shots[shot_id]["internal_timeline"].get("clips", []), "id",
                            f"Runtime shots[{shot_id!r}].internal_timeline.clips")
        pinned_rows = _rows(shot["base_internal_timeline"].get("clips", []), "id",
                            f"candidate.shots[{shot_id!r}].base_internal_timeline.clips")
        after_rows = _rows(shot["internal_timeline"].get("clips", []), "id",
                           f"candidate.shots[{shot_id!r}].internal_timeline.clips")
        if list(before_rows) != list(pinned_rows) or list(before_rows) != list(after_rows):
            raise DocumentDiffError(f"{owner} clip membership/order is held by the document view")
        media_changes = _same_alias_changes(
            canonical_shots[shot_id]["internal_timeline"], shot["internal_timeline"], owner=owner
        )
        deferred = set()
        for alias, (old_entry, new_entry) in media_changes.items():
            if sum(row["shot_id"] == shot_id for row in base["placements"]) != 1:
                raise DocumentDiffError(f"{owner}/asset:{alias} shared placement scope is ambiguous")
            affected = [clip_id for clip_id, row in before_rows.items() if row.get("asset") == alias]
            if not affected or any(after_rows[clip_id].get("asset") != alias for clip_id in affected):
                raise DocumentDiffError(f"{owner}/asset:{alias} media consumers changed identity")
            pair = (media_selections or {}).get((owner, alias))
            if pair is None:
                if not defer_media:
                    raise DocumentDiffError(f"{owner}/asset:{alias} requires an exact Runtime media selection")
                deferred.add(alias)
                continue
            try:
                old_media, new_media = pair["old"], pair["new"]
                command = capture_occurrence_swap_media(
                    working, _clip_ref(owner, affected[0]), old_media, new_media,
                    verified_media=verified_media,
                )
            except (CommandError, KeyError, TypeError) as exc:
                raise DocumentDiffError(
                    f"{owner}/asset:{alias} native same-alias media rebind is held: {exc}"
                ) from exc
            try:
                result = execute(working, [command], verified_media=verified_media)
            except CommandError as exc:
                raise DocumentDiffError(
                    f"{owner}/asset:{alias} native same-alias media rebind is held: {exc}"
                ) from exc
            commands.append(command)
            working = result.bundle
        for clip_id, before in before_rows.items():
            _check_clip_baseline(before, pinned_rows[clip_id], owner=owner, clip_id=clip_id)
            after = after_rows[clip_id]
            _check_clip_shape(before, after, owner=owner, clip_id=clip_id)
            working, emitted = _emit_clip_commands(working, owner, before, after)
            commands.extend(emitted)
        _require_explicit_rows(
            shot["internal_timeline"].get("clips", []),
            working["shots"][shot_id]["internal_timeline"].get("clips", []),
            f"{owner} clips differ from the native command result",
        )
        _require_same(shot["internal_timeline"].get("tracks"),
                      shot["base_internal_timeline"].get("tracks"),
                      f"{owner} track edits are held by the document view")
        if not media_changes:
            _require_same(shot["internal_timeline"].get("registry"),
                          shot["base_internal_timeline"].get("registry"),
                          f"{owner} registry/media edits are held by the document view")
            _require_same(shot.get("payload"), shot.get("base_payload"),
                          f"{owner} shot payload/narration edits are held by the document view")
        else:
            if deferred:
                _require_same(
                    _replace_registry_media(shot["internal_timeline"].get("registry"),
                                            {alias: media_changes[alias] for alias in deferred}),
                    shot["base_internal_timeline"].get("registry"),
                    f"{owner} registry contains unsupported media fields",
                )
            else:
                _require_same(shot["internal_timeline"].get("registry"),
                              working["shots"][shot_id]["internal_timeline"].get("registry"),
                              f"{owner} registry/media differs from the native command result")
            if deferred:
                replacements = {
                    old.get("media_id"): new.get("media_id")
                    for alias, (old, new) in media_changes.items() if alias in deferred
                }
                _require_same(_replace_known_payload_media(shot.get("payload"), replacements),
                              shot.get("base_payload"),
                              f"{owner} payload contains unsupported media or narration edits")
            else:
                _require_same(shot.get("payload"), working["shots"][shot_id]["payload"],
                              f"{owner} payload differs from the native command result")
        for key in set(shot["internal_timeline"]) - {"clips", "tracks", "registry"}:
            _require_same(shot["internal_timeline"].get(key), shot["base_internal_timeline"].get(key),
                          f"{owner} internal field {key!r} is held by the document view")

    parent = candidate.get("parent")
    base_parent = candidate.get("base_parent_payload")
    if not isinstance(parent, Mapping) or not isinstance(base_parent, Mapping):
        raise DocumentDiffError("candidate parent is malformed")
    for key in set(parent) | set(base_parent):
        if key in {"clips", "config"}:
            continue
        _require_same(parent.get(key), base_parent.get(key), f"parent field {key!r} is held by the document view")
    parent_clips = _rows(parent.get("clips", []), "id", "candidate.parent.clips")
    base_clips = _rows(base_parent.get("clips", []), "id", "candidate.base_parent_payload.clips")
    if list(parent_clips) != list(base_clips):
        raise DocumentDiffError("parent clip membership/order is held by the document view")
    runtime_clips = _rows(base.get("parent", {}).get("clips", []), "id", "Runtime parent.clips")
    for clip_id, before in base_clips.items():
        _check_clip_baseline(runtime_clips[clip_id], before, owner="parent", clip_id=clip_id)
        _check_clip_shape(before, parent_clips[clip_id], owner="parent", clip_id=clip_id)
        working, emitted = _emit_clip_commands(working, "parent", before, parent_clips[clip_id])
        commands.extend(emitted)
    for key in set(parent.get("config", {})) | set(base_parent.get("config", {})):
        if key != "clips":
            _require_same(parent.get("config", {}).get(key), base_parent.get("config", {}).get(key),
                          f"parent.config field {key!r} is held by the document view")
    _require_explicit_rows(parent.get("config", {}).get("clips", []),
                           working.get("parent", {}).get("config", {}).get("clips", []),
                           "parent.config.clips differs from the native command result")
    _require_explicit_rows(parent.get("clips", []), working.get("parent", {}).get("clips", []),
                           "parent.clips differs from the native command result")
    return {"commands": commands, "bundle": working}


__all__ = ["DocumentDiffError", "document_diff_to_commands"]
