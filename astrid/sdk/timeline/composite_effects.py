"""Closed fade/transition producers over the shared clip-field codec.

No renderer or implementation lookup is inferred from a transition name.
The existing admitted element-resource binding supplies declaration ownership.
"""

from __future__ import annotations

import copy
import math
from collections.abc import Mapping

import jsonschema

from astrid.core.timeline import clip_fields as cf
from astrid.sdk.timeline._common import TimelineEditError


def _project(clip, values):
    try:
        return cf.transition_composite(clip.data, values, fps=clip._tl.fps)
    except cf.ClipFieldError as exc:
        raise TimelineEditError(str(exc)) from None


def _predecessor(clip, values, trial):
    from astrid.sdk.timeline import commands

    if trial.get("transition") is None:
        return None
    tl = clip._tl
    if clip.is_audio or not clip.track:
        raise TimelineEditError("transition requires a visual track")
    tracks = [r for r in tl._internal(clip.shot_id).get("tracks", []) if r.get("id") == clip.track]
    if len(tracks) != 1 or tracks[0].get("kind") != "visual":
        raise TimelineEditError("transition requires an exact declared visual track")
    sid = commands.scoped_clip(tl, clip)
    from astrid.sdk.timeline.model import Clip

    peers = []
    for row in tl._internal(clip.shot_id)["clips"]:
        if row.get("track") != clip.track:
            continue
        peer = Clip(tl, clip.shot_id, row)
        if getattr(clip, "_occurrence_id", None) is not None:
            peer._occurrence_id = clip._occurrence_id
        peers.append(peer)
    peers.sort(key=lambda c: (c.at, c.id))
    index = next((i for i, c in enumerate(peers) if commands.scoped_clip(tl, c) == sid), -1)
    if index <= 0:
        raise TimelineEditError("transition destination requires an adjacent predecessor")
    previous = peers[index - 1]
    exact = commands.scoped_clip(tl, previous)
    if "from_clip" in values:
        if values["from_clip"] != exact:
            raise TimelineEditError(
                "from_clip must be the exact adjacent same-track predecessor ScopedId"
            )
    elif (
        not isinstance(clip.data.get("transition"), Mapping)
        or not isinstance(clip.data.get("elementRef"), Mapping)
        or ("elementRef" in values and values["elementRef"] != clip.data["elementRef"])
    ):
        raise TimelineEditError("between-clip assignment requires explicit from_clip")
    from astrid.core.timeline.duration import clip_timeline_duration

    try:
        previous_duration = clip_timeline_duration(previous.data)
        destination_duration = clip_timeline_duration(clip.data)
    except ValueError as exc:
        raise TimelineEditError(f"invalid transition clip timing: {exc}") from None
    if not previous.is_audio and previous.at + previous_duration > clip.at and not math.isclose(
        previous.at + previous_duration, clip.at, abs_tol=1e-9, rel_tol=0
    ):
        from astrid.sdk.timeline.transitions import TransitionAuthoringError

        raise TransitionAuthoringError(
            "transition/same-track-overlap", "Transition clips overlap on the same visual track.",
            "Move or trim the clips into non-overlapping track order, then retry; gaps are allowed.",
        )
    if previous.is_audio or not math.isclose(
        previous.at + previous_duration, clip.at, abs_tol=1e-9, rel_tol=0
    ):
        raise TimelineEditError(
            "transition clips must be adjacent on the same visual track without a gap or overlap"
        )
    duration = trial["transition"]["duration"]
    if duration > min(previous_duration, destination_duration):
        raise TimelineEditError("transition duration must fit both adjacent clips")
    return previous


def _declaration(clip, trial):
    from astrid.core.element import catalog
    from astrid.sdk.invocation import (
        CapabilityValidationError,
        _admitted_timeline_element_resources,
    )

    ref, transition = trial["elementRef"], trial["transition"]
    if ref.get("kind", "transition") not in {"transition", "transitions"}:
        raise TimelineEditError("elementRef must name a transition declaration")
    if ref["revision"].startswith("draft-") or transition["revision"] != ref["revision"]:
        raise TimelineEditError("transition revision and pinned elementRef revision must agree")
    try:
        registry = catalog._registry()
        element = registry.get("transitions", ref["id"], pack_id=ref.get("packId"))
        descriptor = catalog._element_descriptor(element)
        if descriptor["revision"] != ref["revision"]:
            raise ValueError("stale transition resource revision")
        if descriptor["kind"] != "transition" or descriptor["id"] != transition["type"]:
            raise ValueError("transition type differs from the admitted declaration")
        # Normalizing the lookup kind does not rewrite the captured reference.
        binding_ref = {**ref, "kind": "transitions"}
        binding = _admitted_timeline_element_resources(
            {"clips": [{"id": clip.id, "elementRef": binding_ref}]}, registry=registry
        )[clip.id]
        declaration = binding["declaration"]
        from pathlib import Path

        root = Path(declaration["pack_root"])
        implementations = {
            (root / r["path"]).resolve()
            for r in declaration["resources"]
            if r["kind"] in {"implementation", "support"}
        }
        if element.component.resolve() not in implementations:
            raise ValueError("transition implementation is not bound by the admitted declaration")
        params = {**descriptor.get("defaults", {}), **(transition.get("params") or {})}
        jsonschema.Draft202012Validator.check_schema(descriptor["schema"])
        validator = jsonschema.Draft202012Validator(descriptor["schema"])
        validator.validate(params)
        validator.validate({**params, "durationFrames": transition["duration"] * clip._tl.fps})
    except (
        KeyError,
        ValueError,
        CapabilityValidationError,
        jsonschema.ValidationError,
        jsonschema.SchemaError,
    ) as exc:
        raise TimelineEditError(f"invalid transition declaration/resource: {exc}") from None


def guard_call(tl, call, clip, states, selected):
    """Capture read dependencies as ordinary tagged expectations for rebase."""
    from dataclasses import replace

    from astrid.sdk.timeline import commands

    trial = _project(clip, call.args)
    previous = _predecessor(clip, call.args, trial)
    if previous is not None:
        # Shared-source adapters may materialize an occurrence before calling
        # the setter. Refuse invalid resources before that provisional write.
        _declaration(clip, trial)
    expectations = dict(call.expect or {})
    if previous is not None:
        for owner in (clip, previous):
            sid = commands.scoped_clip(tl, owner)
            for path in (
                "track",
                "at",
                "hold",
                "from",
                "to",
                "speed",
                "clipType",
                "app.astrid.on",
                "app.astrid.until",
                "app.astrid.for",
            ):
                key = commands.write_key(sid, path, selected)
                expectations.setdefault(key, commands.state_at(states, sid, path))
        # A retained reference is a captured value, never a request for latest.
        expectations.setdefault("elementRef", commands.state_at(states, selected[0], "elementRef"))
        track = selected[0].rsplit("/clip:", 1)[0] + "/track:" + clip.track
        expectations.setdefault(track + "::kind", commands.state_at(states, track, "kind"))
        fps_path = "config.theme_overrides.visual.canvas.fps"
        expectations.setdefault(
            "parent::" + fps_path, commands.state_at(states, "parent", fps_path)
        )
    return replace(call, expect=expectations)


def set_fade(self, **values):
    try:
        trial = cf.fade_composite(self.data, values)
    except cf.ClipFieldError as exc:
        raise TimelineEditError(str(exc)) from None
    self.data.clear()
    self.data.update(trial)
    self._tl._mcache = None
    return self


def set_transition(self, **values):
    trial = _project(self, values)
    _predecessor(self, values, trial)
    if trial.get("transition") is not None:
        _declaration(self, trial)
    self.data.clear()
    self.data.update(copy.deepcopy(trial))
    self._tl._mcache = None
    return self


def direct_paths(sid, args, before):
    """Parent presence belongs to inverse too; leaf paths allow disjoint fades."""
    paths = set()
    sides = (set(args) | set(args.get("clear", ()))) & {"fade_in", "fade_out"}
    for side in sides:
        phase = "entrance" if side == "fade_in" else "exit"
        paths.add(phase)
        # Absent/null containers must be restored exactly. An existing object
        # permits independent edits to another side or an opaque sibling.
        paths.add("effects." + side if isinstance(before.get("effects"), Mapping) else "effects")
    return {(sid, path) for path in paths}
