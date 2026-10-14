"""Duplicate a timeline's editable content with fresh shot and occurrence identities."""
from __future__ import annotations

import copy
import uuid
from collections.abc import Mapping

from astrid.sdk.timeline_checkout import Checkout, TimelineEditError
from astrid.sdk.timeline_editing import add_authoring_shot
from astrid.sdk.timeline_intent import migrate as migrate_intent


def _common_prefix(values):
    if not values:
        return ""
    prefix = values[0]
    for value in values[1:]:
        while prefix and not value.startswith(prefix):
            prefix = prefix[:-1]
    return prefix[: prefix.rfind("-") + 1] if "-" in prefix else ""


def id_map(old_ids, new_slug):
    values = [str(value) for value in old_ids]
    if len(values) != len(set(values)):
        raise TimelineEditError("cannot map duplicate source ids")
    prefix = _common_prefix(values) if len(values) > 1 else ""
    mapped = {old: f"{new_slug}-{old[len(prefix):] or old}" for old in values}
    if len(set(mapped.values())) != len(mapped):
        raise TimelineEditError("id mapping is not one-to-one; choose another slug")
    return mapped


def _remap_values(value, mapping):
    if isinstance(value, str):
        return mapping.get(value, value)
    if isinstance(value, list):
        return [_remap_values(item, mapping) for item in value]
    if isinstance(value, Mapping):
        return {key: _remap_values(item, mapping) for key, item in value.items()}
    return copy.deepcopy(value)


def copy_content(source, target, *, new_slug):
    """Copy source content onto target while retaining target identity/provenance."""
    rows = [copy.deepcopy(row) for row in source.get("placements") or []]
    shot_ids = [str(row["shot_id"]) for row in rows]
    occurrence_ids = [str(row["occurrence_id"]) for row in rows]
    shots = id_map(shot_ids, str(new_slug))
    occurrences = id_map(occurrence_ids, f"occ-{new_slug}")
    remap = {**shots, **occurrences}
    out = copy.deepcopy(dict(target))
    parent = source.get("parent") or {}
    out["parent"] = {**dict(out.get("parent") or {}),
                      "config": copy.deepcopy(parent.get("config") or {}),
                      "registry": _remap_values(parent.get("registry") or {}, remap),
                      "clips": _remap_values(parent.get("clips") or [], remap)}
    out["shots"], out["placements"] = {}, []
    source_mapping = copy.deepcopy(out.get("source_mapping") or {})
    source_mapping["shots"], source_mapping["placements"] = {}, {}
    out["source_mapping"] = source_mapping
    for row in rows:
        old_shot, old_occ = str(row["shot_id"]), str(row["occurrence_id"])
        original = (source.get("shots") or {}).get(old_shot)
        if not isinstance(original, Mapping):
            raise TimelineEditError(f"source shot {old_shot!r} has no content")
        new_shot, new_occ = shots[old_shot], occurrences[old_occ]
        added = add_authoring_shot(out, shot_id=new_shot, occurrence_id=new_occ,
                                   start_ms=(row.get("placement") or {}).get("start_ms", 0))
        payload = copy.deepcopy(dict(original.get("payload") or original.get("base_payload") or {}))
        payload.pop("internal_timeline_revision_id", None)
        payload["text_bindings"] = []
        added["payload"] = payload
        added["internal_timeline"] = _remap_values(original.get("internal_timeline") or {}, shots)
        new_row = _remap_values(row, remap)
        new_row.update(shot_id=new_shot, occurrence_id=new_occ)
        out["placements"][-1] = new_row
        source_mapping["placements"][new_occ] = copy.deepcopy(new_row)
    migrate_intent(out)
    return out, []


def _duplicate(client, project, source, *, slug):
    src = Checkout.open(project, source, client=client)
    report = src.check()
    if not report.valid:
        raise TimelineEditError(f"not duplicating {source}: its head is not valid; nothing was created")
    created = client.timelines.create_empty(project=project, timeline_id=slug or None,
        config=copy.deepcopy(dict((src.bundle.get("parent") or {}).get("config") or {})),
        idempotency_key=f"dup-{uuid.uuid4().hex}")
    if not created.ok:
        raise TimelineEditError(f"could not create the timeline: {getattr(created.error, 'message', created.error)}")
    data = created.data if isinstance(created.data, Mapping) else {}
    new_id = str(data.get("timeline_id") or slug or "")
    if not new_id:
        raise TimelineEditError("the runtime created a timeline but returned no id")
    try:
        dst = Checkout.open(project, new_id, client=client)
        dst.bundle, _ = copy_content(src.bundle, dst.bundle, new_slug=slug or new_id)
        receipt = dst.publish(f"duplicate of {source}", client=client, idempotency_key=f"dup-{uuid.uuid4().hex}")
    except Exception as exc:
        archived = client.timelines.archive(project, new_id)
        if getattr(archived, "ok", False):
            raise TimelineEditError(f"{exc} (nothing kept: the new timeline {new_id!r} was archived again)") from exc
        raise TimelineEditError(f"{exc} (the empty timeline {new_id!r} was created and could not be archived)") from exc
    return {"timeline_id": new_id, "slug": slug, "source": source,
            "shots": len(dst.bundle.get("shots") or {}),
            "old_head": receipt.get("old_head"), "new_head": receipt.get("new_head"), "notes": []}


def duplicate_timeline(project, source, *, slug=None, client=None):
    if client is not None:
        return _duplicate(client, project, source, slug=slug)
    from astrid.sdk import AstridClient
    with AstridClient.open_from_launcher(start_pack_host=False) as opened:
        return _duplicate(opened, project, source, slug=slug)
