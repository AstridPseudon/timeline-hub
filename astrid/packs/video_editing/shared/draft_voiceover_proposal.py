"""Private native proposal seam for the known draft voiceover insertion."""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import uuid
from collections.abc import Mapping
from typing import Any

_MEDIA_SELECTION_FIELDS = ("asset", "generation_id", "variant_id", "object_id", "catalog_digest")
_PRODUCER_FIELDS = ("task_id", "attempt_id", "executor_id", "fence", "runtime_epoch")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def _completed_voiceover_output(result: Mapping[str, Any]) -> tuple[dict, dict, dict] | None:
    """Return the exact settled WAV selection, producer pin, and raw row.

    A digest alone is not an accepted media selection.  The requester needs the
    completed variant's complete five-field selection and the immutable
    provenance that settled it; anything less stays an open proposal.
    """
    output = result.get("output")
    if not isinstance(output, Mapping):
        return None
    selection = output.get("selection")
    if (not isinstance(selection, Mapping)
            or set(selection) != set(_MEDIA_SELECTION_FIELDS)
            or any(not isinstance(selection.get(key), str) or not selection[key]
                   for key in _MEDIA_SELECTION_FIELDS)
            or _DIGEST.fullmatch(selection["object_id"]) is None
            or _DIGEST.fullmatch(selection["catalog_digest"]) is None):
        return None
    provenance = output.get("provenance")
    if not isinstance(provenance, Mapping):
        provenance = output.get("producer")
    if not isinstance(provenance, Mapping):
        provenance = result.get("producer")
    if (not isinstance(provenance, Mapping)
            or set(provenance) != set(_PRODUCER_FIELDS)
            or any(not isinstance(provenance.get(key), str) or not provenance[key]
                   for key in ("task_id", "attempt_id", "executor_id"))
            or any(type(provenance.get(key)) is not int or provenance[key] <= 0
                   for key in ("fence", "runtime_epoch"))):
        return None
    if (not isinstance(output.get("association_id"), str)
            or not isinstance(output.get("task_id"), str)
            or not isinstance(output.get("attempt_id"), str)
            or output["task_id"] != provenance["task_id"]
            or output["attempt_id"] != provenance["attempt_id"]):
        return None
    if output.get("object_id") is not None and output.get("object_id") != selection["object_id"]:
        return None
    if output.get("media_type") != "audio/wav" or output.get("project_id") not in (None, result.get("project_id")):
        return None
    return dict(selection), {key: provenance[key] for key in _PRODUCER_FIELDS}, dict(output)


def _native_voiceover_ready(candidate: Mapping, scripts: Mapping, generated: list[Mapping],
                            base_publication_id: Any) -> bool:
    """Preflight the known-child branch without capturing any commands.

    Normal speech results do not satisfy this predicate: native activation is
    reserved for an existing Runtime-admitted, task/attempt-bound managed
    output with an explicit completed selection and the ordinary captured
    child/text shape.
    """
    if not isinstance(base_publication_id, str) or not base_publication_id or not generated:
        return False
    producer = None
    for item in generated:
        completed = _completed_voiceover_output(item)
        if completed is None:
            return False
        _selection, pin, output = completed
        if producer is None:
            producer = pin
        elif producer != pin:
            return False
        oid, shot_id = item.get("occurrence_id"), item.get("shot_id")
        placement = next((row for row in candidate.get("placements", [])
                          if row.get("occurrence_id") == oid and row.get("shot_id") == shot_id), None)
        shot = candidate.get("shots", {}).get(shot_id, {})
        internal = shot.get("internal_timeline", {})
        tracks = internal.get("tracks")
        registry = internal.get("registry", {}).get("assets") if isinstance(internal.get("registry"), Mapping) else None
        clips = internal.get("clips")
        if (not isinstance(placement, Mapping) or not isinstance(tracks, list)
                or not isinstance(registry, dict) or not isinstance(clips, list)):
            return False
        clip_id = item.get("clip_id")
        if not isinstance(clip_id, str) or any(clip.get("id") == clip_id for clip in clips):
            return False
        if sum(track.get("kind") == "audio" for track in tracks) > 1:
            return False
        size = output.get("size", output.get("bytes"))
        duration = item.get("duration_seconds")
        if (type(size) is not int or size <= 0 or not isinstance(duration, (int, float))
                or isinstance(duration, bool) or not math.isfinite(duration) or duration <= 0):
            return False
        if _script_binding_pin(candidate, scripts, oid, shot_id) is None:
            return False
    return producer is not None


def _script_binding_pin(candidate: Mapping, scripts: Mapping, occurrence_id: str,
                        shot_id: str) -> tuple[dict, dict] | None:
    """Find only a registered, frozen UTF-8 script binding that captures cleanly."""
    from .draft_voiceover import digest
    row = next((item for item in scripts.get("occurrences", [])
                if isinstance(item, Mapping) and item.get("occurrence_id") == occurrence_id), None)
    if not isinstance(row, Mapping) or row.get("status") != "present" or not isinstance(row.get("text"), str):
        return None
    bindings = row.get("bindings")
    if not isinstance(bindings, list) or len(bindings) != 1:
        return None
    source = bindings[0]
    if (not isinstance(source, Mapping) or source.get("provenance") != "registered_pin"
            or source.get("media_id") != source.get("content_hash")
            or type(source.get("byte_size")) is not int or source["byte_size"] < 0):
        return None
    raw = row["text"].encode("utf-8")
    if (len(raw) != source["byte_size"]
            or digest(row["text"]) != source["content_hash"]):
        return None
    shot = candidate["shots"].get(shot_id, {})
    authored = shot.get("payload", {}).get("text_bindings", [])
    if not isinstance(authored, list):
        return None
    authored_row = next((item for item in authored
                         if isinstance(item, Mapping)
                         and item.get("kind") == "voiceover_script"
                         and item.get("slot") is None), None)
    if not isinstance(authored_row, Mapping):
        return None
    media_type = authored_row.get("mime_type")
    if (media_type != "text/plain; charset=utf-8"
            or authored_row.get("media_id") != source["media_id"]
            or authored_row.get("content_hash") != source["content_hash"]
            or authored_row.get("byte_size") != source["byte_size"]):
        return None
    pin = {"object_id": source["media_id"], "digest": source["content_hash"],
           "size": source["byte_size"], "media_type": media_type}
    return {"kind": "voiceover_script", "slot": None}, pin


def _capture_voiceover_commands(candidate: Mapping, scripts: Mapping, generated: list[Mapping]):
    """Capture one known insertion branch using the existing native commands."""
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_add_media
    from astrid.sdk.timeline.native_text_binding import capture_text_binding_set

    commands, gaps, producer, working = [], [], None, copy.deepcopy(candidate)
    for item in generated:
        completed = _completed_voiceover_output(item)
        if completed is None:
            gaps.append({"occurrence_id": item.get("occurrence_id"), "capability": "settled voiceover variant",
                         "reason": "completed WAV lacks the exact media five-tuple or producer provenance"})
            continue
        selection, pin, output = completed
        if producer is None:
            producer = pin
        elif producer != pin:
            gaps.append({"occurrence_id": item.get("occurrence_id"), "capability": "producer.guard",
                         "reason": "one proposal cannot combine outputs from different settled attempts"})
            continue
        oid, shot_id = item.get("occurrence_id"), item.get("shot_id")
        placement = next((row for row in working.get("placements", [])
                          if row.get("occurrence_id") == oid and row.get("shot_id") == shot_id), None)
        shot = working.get("shots", {}).get(shot_id, {})
        internal = shot.get("internal_timeline", {})
        tracks = internal.get("tracks")
        registry = internal.get("registry", {}).get("assets") if isinstance(internal.get("registry"), Mapping) else None
        if not isinstance(placement, Mapping) or not isinstance(tracks, list) or not isinstance(registry, dict):
            gaps.append({"occurrence_id": oid, "capability": "occurrence.add-media",
                         "reason": "voiceover insertion needs a normal captured child scope and asset registry"})
            continue
        clip_id = item.get("clip_id")
        if not isinstance(clip_id, str) or any(clip.get("id") == clip_id for clip in internal.get("clips", [])):
            gaps.append({"occurrence_id": oid, "capability": "occurrence.add-media",
                         "reason": "known branch only inserts a newly reserved voiceover clip"})
            continue
        audio_tracks = [track for track in tracks if track.get("kind") == "audio"]
        if len(audio_tracks) > 1:
            gaps.append({"occurrence_id": oid, "capability": "track.create",
                         "reason": "voiceover lane is ambiguous"})
            continue
        track_id = audio_tracks[0]["id"] if audio_tracks else "draft-voiceover-" + oid
        verified = [{"selection": selection, "media_type": output["media_type"],
                     "size": output.get("size", output.get("bytes")),
                     "duration_seconds": item["duration_seconds"]}]
        if type(verified[0]["size"]) is not int or verified[0]["size"] <= 0:
            gaps.append({"occurrence_id": oid, "capability": "occurrence.add-media",
                         "reason": "settled WAV has no positive raw byte size"})
            continue
        if not audio_tracks:
            command = capture_track_create(working, "occurrence:" + oid,
                                           {"id": track_id, "kind": "audio", "role": "output"})
            commands.append(command)
            working = execute(working, [command]).bundle
        duration = item.get("duration_seconds")
        if not isinstance(duration, (int, float)) or isinstance(duration, bool) or not math.isfinite(duration) or duration <= 0:
            gaps.append({"occurrence_id": oid, "capability": "occurrence.add-media",
                         "reason": "settled WAV has no finite positive duration"})
            continue
        row = {"id": clip_id, "clipType": "media", "asset": selection["asset"], "track": track_id,
               "at": 0, "from": 0, "to": duration, "hold": duration}
        command = capture_occurrence_add_media(working, "occurrence:" + oid, row, selection,
                                               verified_media=verified)
        commands.append(command)
        working = execute(working, [command], verified_media=verified).bundle
        binding = _script_binding_pin(candidate, scripts, oid, shot_id)
        if binding is None:
            gaps.append({"occurrence_id": oid, "capability": "text-binding.set",
                         "reason": "frozen registered UTF-8 script binding did not pass normal capture"})
            continue
        binding_row, text_pin = binding
        command = capture_text_binding_set(working, "occurrence:" + oid, binding_row,
                                           text=text_pin, verified_text=[{**text_pin, "utf8": True}])
        commands.append(command)
        working = execute(working, [command], verified_media=[{**text_pin, "utf8": True}]).bundle
    return commands if not gaps else [], gaps, producer


def _voiceover_proposal(producer: Mapping, candidate: Mapping, base_publication_id: str,
                        commands: list[Mapping]) -> dict:
    from astrid.sdk.timeline.commit import _digest

    proposal = {"schema_version": 1,
                "producer": dict(producer),
                "admitted_target": {"project_id": candidate["project_id"],
                                    "timeline_id": candidate["timeline_id"],
                                    "base_revision_id": candidate["base_parent"]["revision_id"],
                                    "base_publication_id": base_publication_id},
                "commands": copy.deepcopy(commands),
                "rationale": "Insert settled managed voiceover WAV and preserve its frozen script binding"}
    proposal["proposal_digest"] = _digest(proposal)
    return proposal


def _commit_voiceover_proposal(client, proposal: Mapping):
    from astrid.sdk.timeline.sync import TimelineSession

    target = proposal["admitted_target"]
    session = TimelineSession.open(proposal["admitted_target"]["project_id"],
                                   proposal["admitted_target"]["timeline_id"], client=client,
                                   base_revision_id=target["base_revision_id"],
                                   base_publication_id=target["base_publication_id"])
    session.queue_proposal(proposal)
    return session.flush(idempotency_key="voiceover-" + proposal["proposal_digest"].removeprefix("sha256:"),
                         via="voiceover-proposal:" + proposal["proposal_digest"])


def _known_voiceover_insertions(candidate: Mapping, generated: list[Mapping]) -> bool:
    """Limit this migration to the branch that reserves new child clip IDs."""
    for item in generated:
        shot = candidate.get("shots", {}).get(item.get("shot_id"), {})
        clips = shot.get("internal_timeline", {}).get("clips", [])
        clip_id = item.get("clip_id")
        if (not isinstance(clip_id, str)
                or any(isinstance(clip, Mapping) and clip.get("id") == clip_id for clip in clips)):
            return False
    return bool(generated)

def _artifact_identity(row):
    from .draft_voiceover import VoiceoverSyncError
    for key in ("object_id", "media_id", "content_hash", "digest", "sha256"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value if value.startswith("sha256:") else "sha256:" + value
    raise VoiceoverSyncError("Managed artifact has no digest")


def runtime_synthesizer(client, project):
    """Invoke speech through SDK; verify provenance bytes from managed outputs."""
    from .draft_voiceover import VoiceoverSyncError, digest
    # A deliberate regeneration must not replay a failed or missing old output.
    # Share one identity within this batch; a later explicit sync gets a new one.
    request_context = {"draft_voiceover_sync": uuid.uuid4().hex}
    def synthesize(text, settings):
        import astrid.sdk as sdk
        result = sdk.invoke("generation.generate_speech", kind="executor", project=project,
            inputs={"text": text, **settings}, client=client, wait=True,
            idempotency_context=request_context)
        if not result.ok:
            raise VoiceoverSyncError(str(result.error))
        artifacts = result.outputs.get("managed_outputs") or result.outputs.get("artifacts") or []
        manifest_row = next((r for r in artifacts if r.get("name") in {"speech_manifest", "manifest", "manifest.json"}
                             or str(r.get("path", "")).endswith("manifest.json")), None)
        audio_row = next((r for r in artifacts if r.get("name") in {"speech", "generated_audio"}
                          or str(r.get("path", "")).endswith("speech.wav")), None)
        if manifest_row is None or audio_row is None:
            raise VoiceoverSyncError("Completed speech run has no managed WAV/provenance outputs")
        manifest = json.loads(client.media.read_bytes(_artifact_identity(manifest_row)))
        audio_id = _artifact_identity(audio_row)
        audio_bytes = client.media.read_bytes(audio_id)
        if ("sha256:" + hashlib.sha256(audio_bytes).hexdigest() != audio_id
                or manifest.get("audio_sha256") != audio_id.removeprefix("sha256:")
                or manifest.get("text_sha256") != digest(text).removeprefix("sha256:")):
            raise VoiceoverSyncError("Managed speech provenance failed hash verification")
        return {"text": manifest["text"], "settings": manifest["settings"],
                "audio_media_id": audio_id, "duration_seconds": manifest["duration_seconds"],
                "run_id": result.run_id, "task_id": result.kernel_task_id,
                "project_id": project, "output": dict(audio_row)}
    return synthesize


