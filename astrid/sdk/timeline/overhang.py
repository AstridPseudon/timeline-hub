"""Caller-shaped overhang conversion on the ordinary command/history path."""
from __future__ import annotations

import copy
import json
import math
from dataclasses import replace

from astrid.core.timeline.cuts import clip_duration
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands, relations, shot_groups

APPEARANCE = ("opacity", "x", "y", "width", "height", "cropTop", "cropBottom", "cropLeft", "cropRight")
OP = "clip.overhang-to-hold"


def _positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def _inventory(tl, sid):
    authored = relations.affected(tl, [sid])
    affected = {sid} | {r["target"] for r in authored}
    groups = []
    for row in shot_groups.groups(tl):
        candidates = row.get("memberSelectors", row.get("clipIds", []))
        if any(sid in candidates or sid.split("/clip:", 1)[1] in candidates for sid in affected):
            if affected & set(shot_groups.selectors(tl, row)[0]):
                groups.append(copy.deepcopy(row))
    beds = {owner: copy.deepcopy(dict(row)) for owner, row in commands.music_carriers(tl).items()
            if owner in affected}
    return dict(authored=authored, groups=groups, beds=beds)


def guard(tl, call, source, states):
    sid = commands.scoped_clip(tl, source)
    if call.select != sid or (call.resolved and call.resolved != (sid,)):
        raise commands.CommandError("overhang conversion requires the exact source ScopedId and owner")
    child = call.args.get("child")
    scope = sid.split("/clip:", 1)[0]
    if (not isinstance(child, str) or not commands.is_scoped_id(child)
            or not child.startswith(scope + "/clip:") or child == sid):
        raise commands.CommandError("hold child must be an allocated clip ScopedId in the source owner")
    if call.created is not None and call.created != (child,):
        raise commands.CommandError("created must contain exactly the allocated hold child")
    expected = dict(call.expect or {})
    commands.track_owner(tl, scope + "/track:" + source.track)
    registry = "parent" if scope == "parent" else scope + "/registry"
    asset_path = ("registry.assets" if scope == "parent" else "assets") + "[" + json.dumps(source.asset) + "]"
    # The UI must bind the actual captured source/order/media, not ask the
    # producer to choose a new base after the gesture has already been planned.
    required = [(sid, ""), (sid, "clip_order"), (registry, asset_path), (scope + "/track:" + source.track, "")]
    if scope != "parent":
        required.extend((entity, "") for entity in (scope, scope + "/shot", scope + "/source"))
        if commands.state_at(states, scope + "/source", "")["state"] != "present":
            raise commands.CommandError("overhang conversion requires pinned occurrence source ownership")
    for entity, path in required:
        if entity + "::" + path not in expected:
            raise commands.CommandError("overhang conversion requires tagged source, clip_order, asset and owner expectations")
    def capture(entity, path=""):
        expected.setdefault(entity + "::" + path, commands.state_at(states, entity, path))
    capture(child)
    capture(scope + "/track:" + source.track)
    if scope != "parent":
        for entity in (scope, scope + "/shot", scope + "/source"):
            capture(entity)
    inventory = _inventory(tl, sid)
    if "relation_inventory" not in call.args:
        raise commands.CommandError("overhang conversion requires the captured relation_inventory")
    if call.args["relation_inventory"] != inventory:
        raise commands.SemanticConflict("dependent", sid, "relation_inventory",
                                        call.args["relation_inventory"], inventory, call.args)
    choices = call.args.get("relation_choices", [])
    if choices:
        relations.validate(choices)
    covered = {(r["target"], r["edge"]) for r in choices}
    if any((r["target"], r["edge"]) not in covered for r in inventory["authored"]):
        raise commands.CommandError("overhang conversion needs explicit choices for every affected authored relation")
    for row in inventory["authored"]:
        if row["target"] + "::" not in expected:
            raise commands.CommandError("overhang conversion requires tagged affected-source expectations")
    group_choices = call.args.get("group_choices", [])
    groups = [shot_groups.identity({k: row[k] for k in ("shotId", "trackId")}) for row in inventory["groups"]]
    if group_choices != [dict(group=group, choice="keep") for group in groups]:
        raise commands.CommandError("overhang conversion needs explicit keep choices for captured shot groups")
    for group in groups:
        capture(group)
    # A generated bed output is not an ordinary video source. Creating another
    # projection owner here would compete with the existing bed producer.
    if sid in inventory["beds"]:
        raise commands.CommandError("overhang conversion requires an ordinary video source, not a music-bed projection")
    args = {**call.args, "relation_inventory": inventory, "group_choices": group_choices}
    return replace(call, args=args, expect=expected, created=(child,))


def validate_result(source, child, args):
    """Explicit relation choices must still fulfill this composite's geometry."""
    playable = max(.05, max(0, args["source_duration"] - source.data.get("from", 0)) / source.data.get("speed", 1))
    if (source.data["to"] != args["out_s"]
            or not math.isclose(clip_duration(source.data), playable, abs_tol=1e-9)
            or not math.isclose(child.data["at"], source.data.get("at", 0) + playable, abs_tol=1e-9)
            or child.data["hold"] != args["hold_duration"]):
        raise commands.CommandError("relation choice contradicts the requested source clamp/hold geometry")


def convert(self, *, child: str, source_duration: float, out_s: float, hold_from: float,
            hold_to: float, hold_duration: float, kind: str, frame_rate=None,
            relation_inventory=None, group_choices=None):
    """Clamp one captured video and insert its explicitly allocated last-frame hold."""
    tl = self._tl
    tl._require_independent_clip(self)
    entry = tl._registry(self.shot_id).get(self.asset) or {}
    if self.element != "media" or not str(entry.get("type", "")).startswith("video"):
        raise commands.CommandError("overhang conversion requires a captured media video asset")
    if not _positive(source_duration) or source_duration != entry.get("duration"):
        raise commands.CommandError("source_duration must equal the captured positive asset duration")
    # Invalid/missing FPS follows the production caller's safe default. A valid
    # but different FPS is a stale/contradictory media selection, not an override.
    fps = frame_rate if _positive(frame_rate) else 30
    asset_fps = entry.get("fps") if _positive(entry.get("fps")) else 30
    if fps != asset_fps:
        raise commands.CommandError("frame_rate contradicts the captured asset FPS")
    source_in = self.data.get("from", 0)
    speed = self.data.get("speed", 1)
    if (not isinstance(source_in, (int, float)) or isinstance(source_in, bool)
            or not math.isfinite(source_in) or source_in < 0 or not _positive(speed)):
        raise commands.CommandError("source range and speed must be finite and consistent")
    total = max(.05, clip_duration(self.data))
    playable = max(.05, max(0, source_duration - source_in) / speed)
    overhang = total - playable
    expected = dict(out_s=max(source_in, source_in + playable * speed),
                    hold_from=max(0, source_duration - 1 / fps), hold_to=source_duration,
                    hold_duration=overhang)
    supplied = dict(out_s=out_s, hold_from=hold_from, hold_to=hold_to, hold_duration=hold_duration)
    if (kind != "hold" or overhang <= .0001 or any(
            isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)
            or not math.isclose(value, expected[key], rel_tol=1e-12, abs_tol=1e-12)
            for key, value in supplied.items())):
        raise commands.CommandError("hold kind, duration and last-frame source range must match the captured overhang")
    if intent.formulas(self.data) or intent.loop(self.data) or intent.orphan(self.data):
        raise commands.CommandError("overhang source has unresolved generated timing ownership")
    clips = tl._internal(self.shot_id)["clips"]
    index = next(i for i, row in enumerate(clips) if row is self.data)
    row = dict(id=child.split("/clip:", 1)[1], asset=self.asset, track=self.track,
               clipType="hold", at=self.data.get("at", 0) + playable, hold=float(hold_duration),
               **{"from": float(hold_from), "to": float(hold_to)}, speed=1, volume=0)
    row.update({key: copy.deepcopy(self.data[key]) for key in APPEARANCE if key in self.data})
    # OpCall canonicalization represents integral arguments as integers. Write
    # seconds consistently on first execution and replay, including JSON bytes
    # used by the existing durable saved-intent digest.
    self.data["to"] = float(out_s)
    # The SDK measures a media hold in source seconds. Preserve its presence;
    # without this update an existing hold would mask the newly clamped out.
    if "hold" in self.data:
        self.data["hold"] = playable * speed
    if intent.for_s(self.data) is not None:
        intent.set_for(self.data, playable)
    clips.insert(index + 1, row)
    tl._mcache = None
    from astrid.sdk.timeline.model import Clip
    return Clip(tl, self.shot_id, row)
