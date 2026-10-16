"""Admit visual transition changes at the existing atomic edit boundary."""
from __future__ import annotations

import json

from ._common import TimelineEditError


class TransitionAuthoringError(TimelineEditError):
    def __init__(self, code: str, message: str, next_step: str):
        self.code, self.next_step = code, next_step
        super().__init__(message if next_step in message else f"{message} Next step: {next_step}")


def admit_transition_changes(checkout, before_checkout, *, raw_transitions=None):
    # Reuse the transaction's existing previous snapshot; do not clone the film.
    previous = {(clip.shot_id, clip.id): clip for clip in before_checkout.clips()}
    current = list(checkout.clips())
    raw_transitions = raw_transitions or {}
    raw_patches = getattr(checkout._open_edit, "_transition_patches", {})

    def transition_of(clip):
        return raw_transitions.get((clip.shot_id, clip.id), clip.data.get("transition"))

    def pinned(value):
        # The existing composite command owns revisioned destination declarations.
        # Its registry/elementRef guard must not be reinterpreted as an outgoing builtin.
        return isinstance(value, dict) and "revision" in value
    def restored(clip, transition):
        # Only this exact captured payload is legacy restoration. An inverse in
        # the same batch must never exempt a later fresh look authoring call.
        key = (clip.shot_id, clip.id)
        if key in raw_patches:
            return False
        for call in checkout._open_edit.calls:
            if call.op != "timeline.inverse":
                continue
            for write in call.args.get("writes", ()):
                state = write["after"]
                if state["state"] != "present":
                    continue
                if write["path"] == "transition":
                    value = state["value"]
                elif write["path"] == "" and isinstance(state["value"], dict):
                    value = state["value"].get("transition")
                else:
                    continue
                scope, _, member = write["id"].rpartition("/")
                if member != "clip:" + clip.id or value != transition:
                    continue
                if scope == "parent" and clip.shot_id is None:
                    return True
                if any(scope == "occurrence:" + row.get("occurrence_id", "")
                       and row.get("shot_id") == clip.shot_id for row in checkout.bundle.get("placements", ())):
                    return True
        return False
    tracks, authored = set(), set()
    def stable(value):
        return json.dumps(value, sort_keys=True)

    def timing(clip):
        return [clip.start_frame, clip.end_frame, clip.track]
    for clip in current:
        if clip.is_audio:
            continue
        key = (clip.shot_id, clip.id)
        old = previous.get(key)
        transition = transition_of(clip)
        if transition and stable(old.data.get("transition") if old else None) != stable(transition) and not restored(clip, transition):
            tracks.add((clip.shot_id, clip.track))
            if not pinned(transition):
                authored.add(key)
        if old is None or timing(old) != timing(clip):
            for track in [old.track if old else None, clip.track]:
                if track and any(c.shot_id == clip.shot_id and c.track == track and transition_of(c) for c in current):
                    tracks.add((clip.shot_id, track))
    remaining = {(clip.shot_id, clip.id) for clip in current}
    for key, clip in previous.items():
        if key not in remaining and not clip.is_audio and any(
            c.shot_id == clip.shot_id and c.track == clip.track and transition_of(c) for c in current
        ):
            tracks.add((clip.shot_id, clip.track))
    if not tracks:
        return
    try:
        from astrid.packs.rendering.actions.timeline_visualize.motion.element_motion import admit_transitions, Unavailable
    except ImportError as exc:
        raise TransitionAuthoringError("transition/unsupported-host", "The renderer admission boundary is unavailable.",
            "Use the configured renderer with the admitted evaluation export and its existing toolchain.") from exc
    requests = []
    for shot, track in sorted(tracks, key=lambda pair: (pair[0] or "", pair[1] or "")):
        clips = sorted((c for c in current if c.shot_id == shot and c.track == track and not c.is_audio),
                       key=lambda c: (c.start_frame, c.id))
        edits = []
        for clip in clips:
            if (shot, clip.id) not in authored:
                continue
            ref = transition_of(clip)
            patch = raw_patches.get((shot, clip.id))
            if isinstance(patch, dict):
                # The public look codec may drop parameters or round duration.
                # Admit the raw authoring values without changing its stored shape.
                ref = {**ref, **patch}
                if "type" in patch and "id" not in patch:
                    ref.pop("id", None)
                if "duration" in patch and "durationFrames" not in patch:
                    ref.pop("durationFrames", None)
            # Existing coercion owns interpretation. No guessed duration default.
            if not isinstance(ref, dict) or "durationFrames" not in ref and "duration" not in ref:
                raise TransitionAuthoringError("transition/invalid-duration", "New transitions require an explicit duration.",
                                               "Supply a duration in frames or seconds, then retry.")
            edits.append({"trackId": track, "clipId": clip.id, "transition": {
                "type": ref.get("id", ref.get("type")),
                "duration": ref["durationFrames"] / checkout.fps if "durationFrames" in ref else ref["duration"],
                "params": ref.get("params", {}),
            }})
        requests.append({"trackIds": [track], "clips": [
            {"id": c.id, "track": track, "start": c.start_frame, "duration": c.end_frame - c.start_frame}
            for c in clips], "authored": edits, "fps": checkout.fps, "host": "timeline-composition"})
    try:
        result = admit_transitions(requests)
    except Unavailable as exc:
        raise TransitionAuthoringError("transition/unsupported-host", str(exc),
            "Use the configured renderer with the admitted evaluation export and its existing toolchain.") from exc
    if not result["ok"]:
        error = result["error"]
        raise TransitionAuthoringError(error["code"], error["message"], error["nextStep"])
