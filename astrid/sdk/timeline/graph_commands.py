"""Occurrence graph producers over the existing recorder and authoring compiler.

Source records are exact immutable closure pins, never client payload authority.
"""
from __future__ import annotations

import copy
import math
import re
from collections.abc import Mapping

from astrid.sdk.timeline import commands

PIN_FIELDS = {"shot_id", "shot_revision_id", "internal_revision_id"}
SOURCE_FIELDS = PIN_FIELDS | {"parent_revision_id", "occurrence_id"}
SHOT_PATHS = {"name": "provenance.name", "settings": "metadata.settings"}
PLACEMENT_PATHS = {"start_ms": "placement.start_ms", "duration_ms": "duration_ms", "track": "track", "gain": "gain", "muted": "muted"}


def source_ref(value):
    if (not isinstance(value, Mapping) or set(value) not in (PIN_FIELDS, SOURCE_FIELDS) or
            any(not isinstance(v, str) or not v or '/' in v for v in value.values())):
        raise commands.CommandError("source requires exact shot/shot-revision/internal-revision pins, optionally parent and occurrence pins")
    return dict(value)


def request_sources(values):
    """Collect only declared immutable reads, including guarded inverse restores."""
    if not isinstance(values, (list, tuple)):
        raise commands.CommandError("commands must be an array")
    result = []
    for value in values:
        call = commands.EditCommand.coerce(value)
        if call.op == "timeline.batch":
            result.extend(request_sources(call.args.get("commands", [])))
        if call.op in {"shot.set", "occurrence.set", "occurrence.add"}:
            result.append(source_ref(call.args.get("source")))
            if call.args.get("replacement") is not None:
                result.append(source_ref(call.args["replacement"]))
        if call.op == "timeline.inverse":
            writes = call.args.get("writes", [])
            if not isinstance(writes, list) or any(not isinstance(w, Mapping) for w in writes):
                raise commands.CommandError("inverse writes must be an object array")
            result.extend(source_ref(w["source"]) for w in writes if "source" in w)
    return result


class Owner:
    def __init__(self, tl, sid, *, new=False):
        if not isinstance(sid, str) or not re.fullmatch(r"occurrence:[^/]+(?:/shot)?", sid):
            raise commands.CommandError("graph command requires an exact occurrence or shot selector")
        self._tl, self.id, self.scoped_id = tl, sid, sid
        self.oid = sid.split(":", 1)[1].split("/", 1)[0]
        rows = [r for r in tl.bundle.get("placements", []) if r.get("occurrence_id") == self.oid]
        if len(rows) != (0 if new else 1):
            raise commands.CommandError("missing, ambiguous or colliding occurrence identity")
        self.row = None if new else rows[0]


def _source(tl, ref):
    ref = source_ref(ref)
    if "parent_revision_id" not in ref:
        from astrid.sdk.timeline.commit import _digest
        record = tl.bundle.get("source_mapping", {}).get("pinned_shots", {}).get(_digest(ref))
        if not isinstance(record, Mapping) or (record.get("project_id"), record.get("timeline_id")) != (tl.bundle["project_id"], tl.bundle["timeline_id"]):
            raise commands.CommandError("shot source is outside the request-bound immutable read")
        return record["shot"], record["source"], copy.deepcopy(record["placement"])
    if ref["parent_revision_id"] == tl.bundle["base_parent"]["revision_id"]:
        bundle = tl.bundle
    else:
        bundle = tl.bundle.get("source_mapping", {}).get("imports", {}).get(ref["parent_revision_id"])
    if not isinstance(bundle, Mapping):
        raise commands.CommandError("source is outside the request-bound immutable closure")
    rows = [r for r in bundle["source_mapping"]["placements"].values() if r["occurrence_id"] == ref["occurrence_id"]]
    if len(rows) != 1:
        raise commands.CommandError("source occurrence is unavailable")
    sid = rows[0]["shot_id"]
    source = bundle["source_mapping"]["shots"][sid]
    if any(source[k] != ref[f] for k, f in (("shot_id", "shot_id"), ("revision_id", "shot_revision_id"), ("internal_timeline_revision_id", "internal_revision_id"))):
        raise commands.CommandError("stale source shot/internal pins")
    return bundle["shots"][sid], source, rows[0]


def guard_source(owner, source):
    _source(owner._tl, source)
    actual = owner._tl.bundle["source_mapping"]["shots"][owner.row["shot_id"]]
    existing = owner.oid in owner._tl.bundle.get("base_placements", {})
    if (existing and "occurrence_id" in source and source["occurrence_id"] != owner.oid) or any(actual[k] != source[f] for k, f in (("shot_id", "shot_id"), ("revision_id", "shot_revision_id"), ("internal_timeline_revision_id", "internal_revision_id"))):
        raise commands.CommandError("selected occurrence does not match captured source pins")


def _write(data, path, value, *, clear=False):
    parts = path.split(".")
    for key in parts[:-1]:
        if key not in data:
            if clear:
                return
            data[key] = {}
        if not isinstance(data[key], dict):
            raise commands.CommandError(f"{key} is not an object; explicit parent replacement is required")
        data = data[key]
    if clear:
        data.pop(parts[-1], None)
    else:
        data[parts[-1]] = copy.deepcopy(value)


def set_shot(self, *, source, values=None, clear=None):
    if not self.id.endswith("/shot"):
        raise commands.CommandError("shot.set selects occurrence:<id>/shot")
    guard_source(self, source)
    values = {} if values is None else values
    clear = [] if clear is None else clear
    if (not isinstance(values, Mapping) or not isinstance(clear, list) or
            any(not isinstance(k, str) for k in clear) or len(clear) != len(set(clear)) or
            (set(values) | set(clear)) - set(SHOT_PATHS) or set(values) & set(clear)):
        raise commands.CommandError("shot.set has closed name/settings values and disjoint explicit clear")
    if "name" in values and (not isinstance(values["name"], str) or not values["name"]):
        raise commands.CommandError("shot name must be nonempty text")
    if "settings" in values and values["settings"] is not None and not isinstance(values["settings"], Mapping):
        raise commands.CommandError("settings must be an object or JSON null")
    payload = self._tl.bundle["shots"][self.row["shot_id"]]["payload"]
    for key, value in values.items():
        _write(payload, SHOT_PATHS[key], value)
    for key in clear:
        _write(payload, SHOT_PATHS[key], None, clear=True)
    return self


def _placement(tl, row, values):
    if not isinstance(values, Mapping) or set(values) - set(PLACEMENT_PATHS):
        raise commands.CommandError("placement accepts start_ms, duration_ms, track, gain, muted only")
    for key, value in values.items():
        if key == "track":
            if value != row.get("track"):
                raise commands.CommandError("occurrence placement must stay on the same lane")
        elif key == "muted":
            if not isinstance(value, bool):
                raise commands.CommandError("muted must be boolean")
        elif not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0 or (key == "duration_ms" and (value <= 0 or int(value) != value)):
            raise commands.CommandError(f"invalid placement {key}")
        _write(row, PLACEMENT_PATHS[key], value)
    # The parent window cannot pretend to trim its authored children. Child
    # commands earlier in this transaction must explicitly establish the fit.
    internal = tl.bundle["shots"][row["shot_id"]]["internal_timeline"]
    end = max((float(c.get("at", 0)) + float(c.get("hold", 0)) for c in internal.get("clips", [])), default=0) * 1000
    if end > row["duration_ms"] + 1e-6:
        raise commands.CommandError("placement trim requires explicit child edits within the same transaction")
    start = row.get("placement", {}).get("start_ms", 0)
    for sibling in tl.bundle["placements"]:
        if sibling["occurrence_id"] == row["occurrence_id"] or sibling.get("track") != row.get("track"):
            continue
        other = sibling.get("placement", {}).get("start_ms", 0)
        if start < other + sibling["duration_ms"] and other < start + row["duration_ms"]:
            raise commands.CommandError("occurrence placement overlaps same-lane content")


def install_source(tl, ref, oid, *, shot_id=None, independent=False, identities=None):
    from astrid.core.timeline.authoring_bundle import (
        _copy_shot_for_placement,
        _identity,
        _remap_known_item_references,
    )
    original, source, _ = _source(tl, ref)
    sid = shot_id or _identity("shot-placement", tl.bundle["project_id"], tl.bundle["timeline_id"], oid, ref["shot_revision_id"])
    if sid in tl.bundle["shots"]:
        raise commands.CommandError("reserved shot identity collides")
    # Duplicate the exact pinned source, never a mutable partially-edited sibling.
    payload, item_map = _copy_shot_for_placement(original["base_payload"], project_id=tl.bundle["project_id"], timeline_id=tl.bundle["timeline_id"], occurrence_id=oid, authoring_shot_id=sid, source_shot_id=source["shot_id"])
    if sid == original["shot_id"]:
        payload, item_map = copy.deepcopy(original["base_payload"]), {}
    internal = _remap_known_item_references(original["base_internal_timeline"], item_map)
    tl.bundle["shots"][sid] = dict(shot_id=sid, payload=copy.deepcopy(payload), base_payload=copy.deepcopy(payload), internal_timeline=copy.deepcopy(internal), base_internal_timeline=copy.deepcopy(internal))
    mapped = copy.deepcopy(source)
    original_map = source.get("item_id_map", {})
    mapped["item_id_map"] = {key: item_map.get(value, value) for key, value in original_map.items()} if original_map else item_map
    mapped["linked"] = not independent
    if identities:
        mapped["reserved_revisions"] = {k: identities[k] for k in ("shot_revision_id", "internal_revision_id")}
    tl.bundle["source_mapping"]["shots"][sid] = mapped
    return sid


def set_occurrence(self, *, source, placement=None, replacement=None):
    if "/" in self.id:
        raise commands.CommandError("occurrence.set selects occurrence:<id>")
    guard_source(self, source)
    if replacement is not None:
        self.row["shot_id"] = install_source(self._tl, replacement, self.oid)
    _placement(self._tl, self.row, {} if placement is None else placement)
    self._tl._refresh()
    return self


def add_occurrence(self, *, source, mode, placement, identities):
    if "/" in self.id or mode not in {"linked", "independent"}:
        raise commands.CommandError("occurrence.add requires a placement selector and linked/independent mode")
    fields = {"occurrence_id"} | ({"shot_id", "shot_revision_id", "internal_revision_id"} if mode == "independent" else set())
    if not isinstance(identities, Mapping) or set(identities) != fields or identities.get("occurrence_id") != self.oid or any(not isinstance(v, str) or not v or '/' in v for v in identities.values()) or len(set(identities.values())) != len(identities):
        raise commands.CommandError("exact distinct reserved output identities are required")
    if mode == "independent":
        resources = self._tl.bundle["source_mapping"]["shots"].values()
        occupied = {row[key] for row in resources for key in ("shot_id", "revision_id", "internal_timeline_revision_id")}
        for row in self._tl.bundle["source_mapping"]["shots"].values():
            occupied.update(row.get("reserved_revisions", {}).values())
        if any(identities[k] in occupied for k in fields - {"occurrence_id"}):
            raise commands.CommandError("reserved output resource identity collides with pinned source")
    _, _, original = _source(self._tl, source)
    sid = install_source(self._tl, source, self.oid, shot_id=identities.get("shot_id"), independent=mode == "independent", identities=identities if mode == "independent" else None)
    row = copy.deepcopy(original)
    if "parent_revision_id" not in source:
        row["track"] = placement.get("track") if isinstance(placement, Mapping) else None
    row.update(occurrence_id=self.oid, shot_id=sid)
    if not isinstance(placement, Mapping) or not {"start_ms", "duration_ms", "track"} <= set(placement):
        raise commands.CommandError("add requires explicit destination start_ms, duration_ms and track")
    _placement(self._tl, row, placement)
    self._tl.bundle["placements"].append(row)
    self._tl._refresh()
    return self


def register():
    for op, handler in (("shot.set", set_shot), ("occurrence.set", set_occurrence), ("occurrence.add", add_occurrence)):
        commands.REGISTRY[op] = commands.Operation(op, "shot" if op == "shot.set" else "occurrence", "set" if op.endswith(".set") else "add", handler)
