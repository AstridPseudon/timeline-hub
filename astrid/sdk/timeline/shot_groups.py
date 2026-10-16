"""Closed shot-group producers on the ordinary recorder/transaction path.

The encoded semantic entity is a view of the existing (shotId, trackId) key,
not a persisted identity or an alternative group store.
"""
from __future__ import annotations

import base64
import copy
import json
import math
from collections.abc import Mapping
from dataclasses import replace

from astrid.sdk.timeline import commands

PREFIX = "parent/shot-group:"


def key(value):
    if (not isinstance(value, Mapping) or set(value) != {"shotId", "trackId"}
            or any(not isinstance(v, str) or not v for v in value.values())):
        raise commands.CommandError("group requires exact nonempty shotId and trackId")
    return dict(value)


def identity(value):
    value = key(value)
    return PREFIX + base64.urlsafe_b64encode(json.dumps([value["shotId"], value["trackId"]], separators=(",", ":"), ensure_ascii=False).encode()).decode().rstrip("=")


def groups(tl):
    config = tl.bundle["parent"].get("config", {})
    if not isinstance(config, dict):
        raise commands.CommandError("parent config must be an object")
    rows = config.get("pinnedShotGroups", [])
    if not isinstance(rows, list):
        raise commands.CommandError("pinnedShotGroups must be an array")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise commands.CommandError("shot group must be an object")
        sid = identity({k: row.get(k) for k in ("shotId", "trackId")})
        if sid in seen:
            raise commands.CommandError("duplicate shot group key")
        seen.add(sid)
    return rows


def semantic_states(tl, states):
    """Represent group rows once, preserving per-key rather than array guards."""
    for row in groups(tl):
        states[identity({k: row[k] for k in ("shotId", "trackId")})] = copy.deepcopy(row)
    config = states["parent"].get("config", {})
    config.pop("pinnedShotGroups", None)
    for row in tl.bundle.get("placements", []):
        internal = tl.bundle["shots"][row["shot_id"]]["internal_timeline"]
        source = tl.bundle["source_mapping"]["shots"][row["shot_id"]]
        states[f"occurrence:{row['occurrence_id']}/source"] = {k: copy.deepcopy(source[k]) for k in ("shot_id", "revision_id", "internal_timeline_revision_id")}
        states[f"occurrence:{row['occurrence_id']}/registry"] = copy.deepcopy(internal.get("registry", {}))


def order_path(values):
    encoded = base64.urlsafe_b64encode(json.dumps(values, separators=(",", ":")).encode()).decode().rstrip("=")
    return "clip_order[" + json.dumps(encoded) + "]"


def order_state(entities, sid, path):
    try:
        encoded = json.loads(path[len("clip_order["):-1])
        values = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
            raise ValueError("invalid order selectors")
        prefix = sid.split("/clip:", 1)[0] + "/clip:"
        if any(not value.startswith(prefix) for value in values):
            raise ValueError("order crosses owner scope")
        return dict(state="present", value=[key for key in entities if key in values])
    except (ValueError, TypeError) as exc:
        raise commands.CommandError("invalid captured group order path") from exc


def internal(tl, scope):
    if scope == "parent":
        return tl.bundle["parent"]
    rows = [r for r in tl.bundle["placements"] if "occurrence:" + r["occurrence_id"] == scope]
    if len(rows) != 1:
        raise commands.CommandError("missing or ambiguous group member owner")
    return tl.bundle["shots"][rows[0]["shot_id"]]["internal_timeline"]


def member(tl, selector):
    if (not isinstance(selector, str) or not commands.is_scoped_id(selector)
            or "/clip:" not in selector or selector.startswith("shot:")):
        raise commands.CommandError("group members require exact parent/occurrence clip selectors; projected IDs are not authority")
    owner = commands.authored_owner(tl, selector, selected=True)
    if commands.scoped_clip(tl, owner) != selector:
        raise commands.CommandError("ambiguous group member owner")
    return owner


def selectors(tl, row):
    if "memberSelectors" in row:
        values = row["memberSelectors"]
    else:
        values = []
        states = commands.entity_states(tl)
        for local in row.get("clipIds", []):
            if isinstance(local, str) and commands.is_scoped_id(local):
                values.append(local)
                continue
            found = []
            for sid in states:
                if not sid.endswith("/clip:" + str(local)):
                    continue
                if sid.startswith("parent/"):
                    found.append(sid)
                else:
                    oid = sid.split("/", 1)[0].removeprefix("occurrence:")
                    placements = [p for p in tl.bundle["placements"] if p["occurrence_id"] == oid]
                    if len(placements) == 1:
                        source = tl.bundle["source_mapping"]["shots"][placements[0]["shot_id"]]
                        if row["shotId"] in {source["shot_id"], placements[0]["shot_id"], oid}:
                            found.append(sid)
            if len(found) != 1:
                raise commands.CommandError("missing or ambiguous group clip owner")
            values.append(found[0])
    if (not isinstance(values, list) or not values or any(not isinstance(v, str) for v in values)
            or len(values) != len(set(values))):
        raise commands.CommandError("group requires nonempty distinct ordered member selectors")
    owners = [member(tl, value) for value in values]
    if "memberSelectors" in row and row.get("clipIds") != [c.id for c in owners]:
        raise commands.CommandError("group ordered clip membership disagrees with scoped provenance")
    scopes = {value.split("/clip:", 1)[0] for value in values}
    tracks = {c.data.get("track") for c in owners}
    if len(scopes) != 1 or len(tracks) != 1 or None in tracks:
        raise commands.CommandError("group membership does not prove one owner and destination track")
    scope, track = next(iter(scopes)), next(iter(tracks))
    if scope != "parent":
        oid = scope.removeprefix("occurrence:")
        placement = next(p for p in tl.bundle["placements"] if p["occurrence_id"] == oid)
        source = tl.bundle["source_mapping"]["shots"][placement["shot_id"]]
        if row.get("ownerOccurrenceId") != oid and row["shotId"] not in {source["shot_id"], placement["shot_id"], oid}:
            raise commands.CommandError("group shot does not own the selected members")
    track_sid = scope + "/track:" + track
    commands.track_owner(tl, track_sid)
    return values, scope, track


def snapshot_rows(row):
    values = row.get("imageClipSnapshot")
    if not isinstance(values, list) or not values:
        raise commands.CommandError("video group requires retained authoritative image snapshot")
    if any(not isinstance(v, dict) or not isinstance(v.get("authoring"), dict)
           or set(v["authoring"]) != {"selector", "clip", "order"} for v in values):
        raise commands.CommandError("snapshot lacks lossless authored provenance")
    ids = [v["authoring"]["selector"] for v in values]
    if len(ids) != len(set(ids)):
        raise commands.CommandError("duplicate dormant snapshot identity")
    return values


def snapshot_track(tl, row, scope):
    tracks = {snap["authoring"]["clip"].get("track") for snap in snapshot_rows(row)}
    if len(tracks) != 1 or any(not isinstance(track, str) or not track for track in tracks):
        raise commands.CommandError("retained images do not prove one destination track")
    track = next(iter(tracks))
    commands.track_owner(tl, scope + "/track:" + track)
    return track


def reservations(tl):
    values = []
    for row in groups(tl):
        for snap in row.get("imageClipSnapshot", []):
            if isinstance(snap, dict) and isinstance(snap.get("authoring"), dict):
                values.append(snap["authoring"].get("selector"))
    return values


def guard(tl, call):
    """Capture exact selected reads before mutation; replay checks originals."""
    args = call.args
    if any(value is None for value in args.values()):
        raise commands.CommandError("omit unspecified shot-group arguments; explicit null is not an intent")
    group = key(args.get("group"))
    sid = identity(group)
    rows = groups(tl)
    found = [row for row in rows if identity({k: row[k] for k in group}) == sid]
    row = found[0] if found else None
    intent = args.get("intent")
    if call.op == "shot-group.set" and intent == "pin":
        values = args.get("members")
        probe = dict(group, memberSelectors=values, clipIds=[member(tl, s).id for s in values] if isinstance(values, list) else [])
        values, scope, track = selectors(tl, probe)
    else:
        if row is None:
            raise commands.CommandError("selected shot group is absent")
        values, scope, track = selectors(tl, row)
    destination = snapshot_track(tl, row, scope) if intent == "images" else track
    target = dict(group, trackId=destination)
    if target != group and any(identity({k: r[k] for k in group}) == identity(target) for r in rows):
        raise commands.CommandError("corrected shot group identity collides")
    states = commands.entity_states(tl)
    expected = dict(call.expect or {})
    def capture(entity, path=""):
        expected.setdefault(entity + "::" + path, commands.state_at(states, entity, path))
    capture(sid)
    capture(identity(target))
    capture(scope + "/track:" + track)
    capture(scope + "/track:" + destination)
    if group["trackId"] != track:
        capture(scope + "/track:" + group["trackId"])
    if scope != "parent":
        capture(scope)
        capture(scope + "/shot")
        capture(scope + "/source")
    for value in values:
        capture(value)
    capture(values[0], order_path(values))
    asset_keys = {member(tl, value).data.get("asset") for value in values}
    if row:
        asset_keys.add(row.get("videoAssetKey"))
        for snap in row.get("imageClipSnapshot", []):
            if isinstance(snap, dict):
                asset_keys.add(snap.get("assetKey"))
                authored = snap.get("authoring", {})
                if isinstance(authored, dict) and isinstance(authored.get("selector"), str):
                    capture(authored["selector"])
    if isinstance(args.get("media"), Mapping):
        asset_keys.add(args["media"].get("asset"))
    registry_sid = "parent" if scope == "parent" else scope + "/registry"
    for asset in asset_keys - {None}:
        if scope != "parent":
            capture("parent", "registry.assets[" + json.dumps(asset) + "]")
        capture(registry_sid, ("registry.assets" if scope == "parent" else "assets") + "[" + json.dumps(asset) + "]")
    if intent == "video":
        identities = args.get("identities")
        if not isinstance(identities, Mapping) or set(identities) != {"clip_id"}:
            raise commands.CommandError("video requires reserved identities {clip_id}")
        reserved = identities["clip_id"]
        if not isinstance(reserved, str) or not reserved or "/" in reserved:
            raise commands.CommandError("invalid reserved video clip ID")
        selected = scope + "/clip:" + reserved
        capture(selected)
        if selected in states or selected in reservations(tl):
            raise commands.CommandError("reserved video identity collides with authored or dormant content")
    return replace(call, expect=expected)


def _store(tl, old, new):
    rows = tl.bundle["parent"].setdefault("config", {}).setdefault("pinnedShotGroups", [])
    position = next((i for i, row in enumerate(rows) if identity({k: row[k] for k in old}) == identity(old)), len(rows))
    rows[:] = [r for r in rows if identity({k: r[k] for k in old}) != identity(old)]
    if new is not None:
        rows.insert(position, new)


def _media_entry(media, record):
    if not isinstance(record, Mapping) or any(record.get(k) != v for k, v in media.items()):
        raise commands.CommandError("exact captured media record is required")
    entry = record["entry"]
    duration = entry.get("duration_seconds")
    if (not str(entry.get("media_type", "")).startswith("video/") or
            not isinstance(duration, (float, int)) or isinstance(duration, bool)
            or not math.isfinite(duration) or duration <= 0):
        raise commands.CommandError("video requires finite positive captured intrinsic duration")
    return dict(media_id=record["object_id"], content_sha256=record["object_id"].removeprefix("sha256:"),
                type=entry["media_type"], duration=duration, format=copy.deepcopy(entry),
                generationId=record["generation_id"], variantId=record["variant_id"],
                authoring_metadata={k: copy.deepcopy(record[k]) for k in ("generation", "variant")})


def set_group(self, *, group, intent, members=None, name=None, media=None, identities=None, media_record=None):
    group = key(group)
    allowed = {"pin": {"members", "name"}, "video": {"media", "identities", "media_record"},
               "replace-video": {"media", "media_record"}, "images": set()}
    supplied = {k for k, v in dict(members=members, name=name, media=media, identities=identities, media_record=media_record).items() if v is not None}
    if not isinstance(intent, str) or intent not in allowed or supplied - allowed[intent]:
        raise commands.CommandError("shot-group.set has closed intent-specific arguments")
    rows = groups(self)
    previous = next((r for r in rows if identity({k: r[k] for k in group}) == identity(group)), None)
    row = copy.deepcopy(previous or group)
    if intent == "pin":
        if previous and previous.get("mode") == "video":
            raise commands.CommandError("pin cannot discard a retained video snapshot")
        row.update(memberSelectors=members, clipIds=[member(self, s).id for s in members], mode="images")
        if name is not None:
            if not isinstance(name, str) or not name:
                raise commands.CommandError("group name must be nonempty text")
            row["name"] = name
    values, scope, track = selectors(self, row)
    if scope != "parent":
        row["ownerOccurrenceId"] = scope.removeprefix("occurrence:")
    if intent == "images":
        track = snapshot_track(self, row, scope)
    row["trackId"] = track  # active or retained authored membership proves the destination
    container = internal(self, scope)
    clips = container.setdefault("clips", [])
    if intent in {"video", "replace-video"}:
        entry = _media_entry(media, media_record)
        assets = container.setdefault("registry", {}).setdefault("assets", {})
        asset = media["asset"]
        if asset in assets and any(not commands._same_value(assets[asset].get(k), v) for k, v in entry.items()):
            raise commands.CommandError("selected media asset key collides")
        assets.setdefault(asset, entry)
        if intent == "video":
            if row.get("mode") != "images":
                raise commands.CommandError("video intent requires image group")
            rows_by_id = {c["id"]: c for c in clips}
            selected = [member(self, value).data for value in values]
            from astrid.core.timeline.parent_registry import effective_parent_registry
            parent_assets = effective_parent_registry(self.bundle["parent"]).get("assets", {})
            for clip in selected:
                metadata = assets.get(clip.get("asset"), parent_assets.get(clip.get("asset"), {}))
                kind = metadata.get("type", metadata.get("media_type", ""))
                if not isinstance(kind, str) or not kind.startswith("image/"):
                    raise commands.CommandError("video intent requires captured image media members")
            # Existing intervals must establish one contiguous window. Do not repair it.
            chronological = sorted(selected, key=lambda c: c.get("at", 0))
            for a, b in zip(chronological, chronological[1:]):
                if not math.isclose(a.get("at", 0) + a.get("hold", 0), b.get("at", 0), abs_tol=1e-9):
                    raise commands.CommandError("group video requires explicit contiguous member timing")
            row["imageClipSnapshot"] = [dict(copy.deepcopy(clip), assetKey=clip.get("asset"), authoring=dict(selector=value, clip=copy.deepcopy(clip), order=list(rows_by_id))) for value, clip in zip(values, selected)]
            local = identities["clip_id"]
            start = chronological[0].get("at", 0)
            span = chronological[-1].get("at", 0) + chronological[-1].get("hold", 0) - start
            if not math.isfinite(span) or span <= 0:
                raise commands.CommandError("group members require a positive captured interval")
            duration = min(span, entry["duration"])
            video = dict(id=local, clipType="media", asset=asset, track=track, at=start,
                         hold=duration, **{"from": 0, "to": duration}, params={})
            selected_ids = {clip["id"] for clip in selected}
            index = min(i for i, clip in enumerate(clips) if clip["id"] in selected_ids)
            clips[:] = [clip for clip in clips if clip["id"] not in selected_ids]
            clips.insert(index, video)
            row.update(clipIds=[local], memberSelectors=[scope + "/clip:" + local], mode="video")
        else:
            if row.get("mode") != "video" or len(values) != 1:
                raise commands.CommandError("replacement requires exactly one video member")
            video = member(self, values[0]).data
            video["asset"] = asset
            left, speed, hold = video.get("from", 0), video.get("speed", 1), video.get("hold")
            if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) for v in (left, speed, hold)) or left < 0 or speed <= 0 or hold <= 0:
                raise commands.CommandError("replacement requires finite captured source trim/duration")
            right = min(video.get("to", left + hold * speed), entry["duration"])
            if left >= right:
                raise commands.CommandError("replacement intrinsic duration cannot preserve source trim")
            video.update(hold=min(hold, (right - left) / speed), **{"to": right})
        row["videoAssetKey"] = asset
    elif intent == "images":
        if row.get("mode") != "video" or len(values) != 1:
            raise commands.CommandError("images intent requires exactly one video member")
        snapshot = snapshot_rows(row)
        occupied = {scope + "/clip:" + c["id"] for c in clips}
        restored = []
        for snap in snapshot:
            authored = snap["authoring"]
            selector, clip = authored["selector"], copy.deepcopy(authored["clip"])
            if selector != scope + "/clip:" + str(clip.get("id")) or selector in occupied or clip.get("track") != track:
                raise commands.CommandError("retained image identity collision or wrong snapshot owner")
            restored.append((selector, clip, authored["order"]))
        removed = {member(self, v).id for v in values}
        clips[:] = [c for c in clips if c["id"] not in removed]
        for selector, clip, order in restored:
            index = next((i for i, c in enumerate(clips) if c["id"] in order and order.index(c["id"]) > order.index(clip["id"])), len(clips))
            clips.insert(index, clip)
        row.update(mode="images", clipIds=[c[1]["id"] for c in restored], memberSelectors=[c[0] for c in restored])
        # IDs are active again; keep the retained snapshot and selected video reference.
    _store(self, group, row)
    self._refresh()
    return self


def remove_group(self, *, group, remove_clip_ids):
    group = key(group)
    row = next(r for r in groups(self) if identity({k: r[k] for k in group}) == identity(group))
    values, scope, _ = selectors(self, row)
    if (not isinstance(remove_clip_ids, list) or any(not isinstance(v, str) for v in remove_clip_ids) or len(remove_clip_ids) != len(set(remove_clip_ids))
            or not set(remove_clip_ids) <= set(values)):
        raise commands.CommandError("remove_clip_ids must explicitly select distinct verified scoped group members")
    clips = internal(self, scope)["clips"]
    removed = {member(self, value).id for value in remove_clip_ids}
    clips[:] = [c for c in clips if c["id"] not in removed]
    _store(self, group, None)
    self._refresh()
    return self


def direct_paths(entry, args, before, after):
    changes = set(commands.changed_paths(before, after))
    # Exact aggregate row, explicit member roots, and registry entries own inverse.
    result = {(sid, "") for sid in set(before) | set(after) if sid.startswith(PREFIX) and before.get(sid) != after.get(sid)}
    for sid, path in changes:
        if "/clip:" in sid:
            result.add((sid, ""))
        elif sid.endswith("/registry") or sid == "parent" and path.startswith("registry"):
            result.add((sid, path))
    # A semantic no-op still guards the selected key.
    if not result:
        result.add((identity(args["group"]), ""))
    return result


def restore_entity(tl, write):
    sid, state = write["id"], write["after"]
    if sid.endswith("/registry"):
        container = internal(tl, sid.removesuffix("/registry"))
        if write["path"]:
            from astrid.sdk.timeline.inverse import _write
            _write(container.setdefault("registry", {}), write["path"], state)
        elif state["state"] == "present":
            container["registry"] = copy.deepcopy(state["value"])
        else:
            container.pop("registry", None)
        return True
    if not sid.startswith(PREFIX):
        return False
    if write["path"]:
        raise commands.CommandError("group inverse requires a whole selected row")
    rows = tl.bundle["parent"].setdefault("config", {}).setdefault("pinnedShotGroups", [])
    rows[:] = [r for r in rows if identity({k: r[k] for k in ("shotId", "trackId")}) != sid]
    if state["state"] == "present":
        row = copy.deepcopy(state["value"])
        if identity({k: row[k] for k in ("shotId", "trackId")}) != sid:
            raise commands.CommandError("group inverse identity mismatch")
        order = write.get("order", [])
        position = order.index(sid) if sid in order else len(order)
        index = next((i for i, r in enumerate(rows) if identity({k: r[k] for k in ("shotId", "trackId")}) in order[position + 1:]), len(rows))
        rows.insert(index, row)
    elif not rows:
        shape = write.get("group_containers", {})
        if not shape.get("groups", True):
            tl.bundle["parent"]["config"].pop("pinnedShotGroups", None)
        if not shape.get("config", True) and not tl.bundle["parent"]["config"]:
            tl.bundle["parent"].pop("config", None)
    return True


def register():
    for op, function in (("shot-group.set", set_group), ("shot-group.remove", remove_group)):
        commands.REGISTRY[op] = commands.Operation(op, "timeline", op.rsplit(".", 1)[1], function)
