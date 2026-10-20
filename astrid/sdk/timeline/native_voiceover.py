"""Pure lowering of a prepared draft voiceover into native commands."""
from __future__ import annotations

import copy
import math
from collections.abc import Mapping

from ._command_state import CommandError, State, equal
from ._shot_commands import capture_shot_set
from .capture import capture_track_create, number
from .commands import execute
from .native_occurrence_media_commands import (
    capture_occurrence_add_media,
    capture_occurrence_swap_media,
)

_MEDIA_FIELDS = {"asset", "generation_id", "variant_id", "object_id", "catalog_digest"}


def _selection(value, label):
    if not isinstance(value, Mapping) or set(value) != _MEDIA_FIELDS:
        raise CommandError(f"{label} must be the exact five-field media selection",
                           kind="unsupported_media")
    return copy.deepcopy(dict(value))


def _source_row(clip, duration, label):
    if not isinstance(clip, Mapping) or (
            clip.get("clipType") is not None and clip.get("clipType") not in ("media", "audio")):
        raise CommandError(f"{label} requires a media audio clip", kind="unsupported_media")
    if not isinstance(clip.get("track"), str) or not clip["track"]:
        raise CommandError(f"{label} requires an explicit audio child track",
                           kind="unsupported_timing")
    left, right = clip.get("from"), clip.get("to")
    if left is None or right is None:
        raise CommandError(f"{label} requires source-unit from/to extents",
                           kind="unsupported_timing")
    left, right = number(left, f"{label}.from"), number(right, f"{label}.to")
    speed = number(clip.get("speed", 1), f"{label}.speed", positive=True)
    hold = number(clip.get("hold", right - left), f"{label}.hold", positive=True)
    duration = number(duration, f"{label}.duration", positive=True)
    if speed != 1 or not math.isclose(right - left, duration, abs_tol=1e-9) \
            or not math.isclose(hold, duration, abs_tol=1e-9):
        raise CommandError(f"{label} source-unit hold/extents differ from settled audio",
                           kind="unsupported_timing")
    return left, right, hold


def capture_draft_voiceover(bundle, prepared, *, media_by_occurrence,
                            verified_media, old_media_by_occurrence=None,
                            timing_policy=None):
    """Lower one prepared voiceover outcome to existing captured commands.

    ``prepared`` is the unmodified result of ``prepare_draft_voiceover`` and
    ``media_by_occurrence`` contains the Runtime-settled five-field selection
    for each generated occurrence. Existing clips additionally require their
    exact prior five-field selection. All IDs and rows come from the prepared
    outcome; this helper allocates no IDs and never writes the candidate. The
    timing policy is retained as a local capture fact; the emitted commands
    are literal and do not re-run ripple resolution on replay.
    """
    if not isinstance(prepared, Mapping) or not isinstance(prepared.get("candidate"), Mapping):
        raise CommandError("voiceover lowering requires a prepared draft outcome")
    policy = timing_policy if timing_policy is not None else prepared.get("timing_policy")
    if policy not in {"preserve", "ripple"}:
        raise CommandError("voiceover lowering requires preserve or ripple intent",
                           kind="unsupported_timing")
    if not isinstance(media_by_occurrence, Mapping):
        raise CommandError("settled voiceover media must be keyed by occurrence")
    old_media_by_occurrence = old_media_by_occurrence or {}
    plan = prepared.get("plan")
    generated = prepared.get("generated")
    if not isinstance(plan, Mapping) or not isinstance(plan.get("jobs"), list) \
            or not isinstance(generated, list):
        raise CommandError("voiceover lowering requires the original synthesis outcome")
    jobs = {job.get("occurrence_id"): job for job in plan["jobs"]}
    if len(jobs) != len(plan["jobs"]):
        raise CommandError("voiceover synthesis outcome has duplicate occurrences")
    if {row.get("occurrence_id") for row in generated} != set(jobs):
        raise CommandError("voiceover synthesis outcome and plan disagree")

    work = copy.deepcopy(bundle)
    commands = []
    captures = []
    candidate = prepared["candidate"]
    for result in generated:
        occurrence_id = result.get("occurrence_id")
        job = jobs[occurrence_id]
        owner = "occurrence:" + occurrence_id
        shot_id = job.get("shot_id")
        shot = candidate.get("shots", {}).get(shot_id)
        if not isinstance(shot, Mapping):
            raise CommandError("voiceover prepared shot disappeared", kind="identity_conflict")
        clip_id = job.get("clip_id")
        clip = next((row for row in shot.get("internal_timeline", {}).get("clips", [])
                     if row.get("id") == clip_id), None)
        duration = number(result.get("duration_seconds"), "audio duration", positive=True)
        source = _source_row(clip, duration, "voiceover")
        media = _selection(media_by_occurrence.get(occurrence_id), "settled media")
        if media["object_id"] != result.get("audio_media_id"):
            raise CommandError("settled media differs from synthesized audio",
                               kind="dependency_changed")
        matching = [row for row in verified_media
                    if isinstance(row, Mapping) and equal(row.get("selection"), media)]
        if len(matching) != 1 or not math.isclose(
                number(matching[0].get("duration_seconds"), "intrinsic duration", positive=True),
                duration, abs_tol=1e-9):
            raise CommandError("settled media lacks exact intrinsic duration",
                               kind="dependency_changed")

        state = State(work)
        target = owner + "/clip:" + clip_id
        existing = state.entity(target, optional=True)
        track = owner + "/track:" + clip["track"]
        track_value = state.entity(track, optional=True)
        if track_value is None:
            track_row = {"id": clip["track"], "kind": "audio"}
            track_command = capture_track_create(work, owner, track_row)
            commands.append(track_command)
            work = execute(work, [track_command]).bundle
            track_value = State(work).entity(track, optional=True)
        if not isinstance(track_value, Mapping) or track_value.get("kind") != "audio":
            raise CommandError("voiceover requires an active audio child track",
                               kind="unsupported_media")

        if existing is None:
            row = copy.deepcopy(dict(clip))
            row["asset"] = media["asset"]
            row["clipType"] = "media"
            row["from"], row["to"], row["hold"] = source
            row.pop("media_id", None)
            command = capture_occurrence_add_media(work, owner, row, media,
                                                   verified_media=verified_media)
        else:
            # Swap changes only the selected asset. Do not claim a prepared
            # duration while retaining a different authored source window.
            _source_row(existing, duration, "authored voiceover")
            old = _selection(old_media_by_occurrence.get(occurrence_id), "old media")
            command = capture_occurrence_swap_media(work, target, old, media,
                                                    verified_media=verified_media)
        commands.append(command)
        work = execute(work, [command], verified_media=verified_media).bundle

        metadata = shot.get("payload", {}).get("metadata", {})
        draft = metadata.get("draft_voiceover")
        if "draft_voiceover" not in metadata:
            raise CommandError("prepared voiceover is missing its provenance leaf",
                               kind="identity_conflict")
        metadata_command = capture_shot_set(
            work, owner + "/shot", values={"metadata": {"draft_voiceover": copy.deepcopy(draft)}})
        commands.append(metadata_command)
        work = execute(work, [metadata_command]).bundle
        captures.append({"occurrence_id": occurrence_id, "clip_id": clip_id,
                         "source": {"from": source[0], "to": source[1], "hold": source[2]},
                         "timing_policy": policy})

    return {"commands": commands, "capture": {"timing_policy": policy, "jobs": captures}}
