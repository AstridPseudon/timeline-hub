"""Explicit draft narration reconciliation over the canonical authoring bundle.

The coordinator uses its caller's existing project authoring authority. Pack
workers can prepare the same candidate, but never acquire publish credentials.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import uuid
from typing import Any, Callable, Mapping

KEY = "draft_voiceover"
DEFAULT_SETTINGS = {"provider": "edge-tts", "voice": "en-US-ChristopherNeural",
                    "rate": "+0%", "volume": "+0%", "pitch": "+0Hz"}


class VoiceoverSyncError(ValueError):
    pass


def digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def settings_with_defaults(settings: Mapping[str, Any] | None) -> dict[str, str]:
    result = dict(DEFAULT_SETTINGS)
    supplied = dict(settings or {})
    if set(supplied) - set(result):
        raise VoiceoverSyncError("Unknown speech settings")
    result.update(supplied)
    if any(not isinstance(value, str) or not value for value in result.values()):
        raise VoiceoverSyncError("Speech settings must be nonempty strings")
    if result["provider"] != "edge-tts":
        raise VoiceoverSyncError("Supported speech provider: edge-tts")
    return result


def selected_media(clip: Mapping, internal: Mapping) -> str | None:
    assets = internal.get("registry", {}).get("assets", {})
    for field in ("media_id", "object_id", "asset", "asset_id"):
        value = clip.get(field)
        if isinstance(value, str) and value.startswith("sha256:"):
            return value
        asset = assets.get(value, {}) if isinstance(value, str) else {}
        for key in ("media_id", "object_id", "digest", "content_sha256"):
            identity = asset.get(key)
            if isinstance(identity, str) and identity:
                return identity if identity.startswith("sha256:") else "sha256:" + identity
    return None


def _audio_clips(shot: Mapping) -> list[dict]:
    internal = shot["internal_timeline"]
    tracks = {t["id"]: t.get("kind") for t in internal.get("tracks", [])}
    assets = internal.get("registry", {}).get("assets", {})
    return [clip for clip in internal.get("clips", [])
            if tracks.get(clip.get("track")) in {"audio", "voice", "vo"}
            or str(assets.get(clip.get("asset"), {}).get("type", "")).startswith("audio")]


def plan_draft_voiceover(candidate: Mapping, scripts: Mapping, *, settings=None,
                         occurrence_ids=None, adopt_clip_ids=None,
                         available_media_ids=None) -> dict:
    """Compare verified pinned script rows with the exact selected audio identity.

    An adoption is explicit permission to replace a particular legacy draft
    clip; it is never evidence that its old audio matches the current words.
    """
    voice = settings_with_defaults(settings)
    if scripts.get("revision_id") != candidate["base_parent"]["revision_id"]:
        raise VoiceoverSyncError("Script and candidate must pin the same parent revision")
    rows = {row["occurrence_id"]: row for row in scripts["occurrences"]}
    selected = set(occurrence_ids) if occurrence_ids is not None else None
    known = {p["occurrence_id"] for p in candidate["placements"]}
    if selected is not None and selected - known:
        raise VoiceoverSyncError("Unknown selected occurrence")
    adopted = set(adopt_clip_ids or ())
    clip_occurrences: dict[str, int] = {}
    adoption_placements = [p for p in candidate["placements"]
                          if selected is None or p["occurrence_id"] in selected]
    for placement in adoption_placements:
        shot = candidate["shots"][placement["shot_id"]]
        for clip in _audio_clips(shot):
            clip_occurrences[clip["id"]] = clip_occurrences.get(clip["id"], 0) + 1
    known_clips = set(clip_occurrences)
    if adopted - known_clips:
        raise VoiceoverSyncError("Unknown adoption clip id")
    if any(clip_occurrences[clip_id] > 1 for clip_id in adopted):
        raise VoiceoverSyncError("Adoption clip id is ambiguous across shot occurrences")
    jobs, statuses = [], []
    for placement in candidate["placements"]:
        oid = placement["occurrence_id"]
        if selected is not None and oid not in selected:
            continue
        shot = candidate["shots"][placement["shot_id"]]
        row = rows.get(oid, {})
        status = {"occurrence_id": oid, "shot_id": placement["shot_id"]}
        if row.get("status") not in {"present", "empty"} or not isinstance(row.get("text"), str):
            statuses.append({**status, "status": "blocked_script", "reason": row.get("status", "missing")})
            continue
        text = row["text"]
        if not text.strip():
            statuses.append({**status, "status": "empty_script"})
            continue
        metadata = shot["payload"].get("metadata", {})
        record = metadata.get(KEY, {})
        audio = _audio_clips(shot)
        target = [c for c in audio if c.get("id") == record.get("clip_id")]
        if not target:
            target = [c for c in audio if c["id"] in adopted]
        if record.get("status") in {"final", "recorded", "locked"}:
            statuses.append({**status, "status": "protected_audio"})
            continue
        if len(target) > 1 or (audio and not target):
            statuses.append({**status, "status": "protected_audio", "clip_ids": [c["id"] for c in audio]})
            continue
        clip = target[0] if target else None
        if clip is not None and (clip.get("app", {}).get(KEY, {}).get("status") in {"final", "recorded", "locked"}):
            statuses.append({**status, "status": "protected_audio"})
            continue
        media = selected_media(clip, shot["internal_timeline"]) if clip else None
        owned = record.get("owner") == "video_editing.sync_draft_voiceover" and record.get("status") == "draft"
        fresh = (owned and media and record.get("audio_media_id") == media
                 and record.get("text") == text and record.get("text_digest") == digest(text)
                 and record.get("settings") == voice
                 and (available_media_ids is None or media in available_media_ids))
        if fresh:
            statuses.append({**status, "status": "reused", "clip_id": clip["id"]})
            continue
        if clip is not None and not owned and clip["id"] not in adopted:
            statuses.append({**status, "status": "protected_audio"})
            continue
        jobs.append({**status, "text": text, "settings": voice,
                     "clip_id": clip["id"] if clip else "draft-vo-" + oid,
                     "previous_media_id": media})
        statuses.append({**status, "status": "regenerate"})
    return {"schema_version": 1, "base_head": candidate["base_parent"]["revision_id"],
            "settings": voice, "jobs": jobs, "statuses": statuses}


def _duration(clip: Mapping) -> float:
    if "hold" in clip:
        return float(clip["hold"])
    return (float(clip.get("to", 0)) - float(clip.get("from", 0))) / float(clip.get("speed", 1))


def _canonical_media_id(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return value if value.startswith("sha256:") else "sha256:" + value


def _bind_generated_audio(shot: dict, clip: dict, result: Mapping) -> None:
    """Keep generated draft audio addressable through the authored asset registry.

    Astrid's occurrence projection resolves audio through ``clip.asset`` and the
    shot revision's asset rows. A bare clip ``media_id`` passes timeline
    validation but leaves the preview without a source.
    """
    internal = shot["internal_timeline"]
    registry = internal.setdefault("registry", {}).setdefault("assets", {})
    old_media = selected_media(clip, internal)
    selector = clip.get("asset") or clip.get("asset_id")
    if not isinstance(selector, str) or selector not in registry:
        selector = next((key for key, entry in registry.items()
                         if old_media and _canonical_media_id(
                             entry.get("media_id") or entry.get("object_id") or entry.get("digest")
                         ) == old_media), None)
    if selector is None:
        selector = "draft-voiceover-" + str(clip["id"])
    entry = registry.setdefault(selector, {"type": "audio"})
    entry.update(media_id=result["audio_media_id"], duration=result["duration_seconds"])
    entry.setdefault("type", "audio")

    # Keep one canonical selector in the internal clip, so the player can
    # project the matching asset entry and its playable source URL.
    for key in ("asset_id", "object_id", "media_id", "hold", "speed"):
        clip.pop(key, None)
    clip["asset"] = selector

    payload = shot["payload"]
    asset_rows = payload.setdefault("assets", [])
    asset = next((row for row in asset_rows if row.get("asset_id") == selector), None)
    if asset is None:
        asset = {"asset_id": selector, "role": "audio", "media_type": "audio/wav",
                 "scope": {"project_id": payload.get("project_id")}}
        asset_rows.append(asset)
    asset.update(digest=result["audio_media_id"], object_id=result["audio_media_id"])
    asset_source = asset.setdefault("source", {})
    asset_source.update(content_sha256=result["audio_media_id"],
                        media_id=result["audio_media_id"],
                        duration=result["duration_seconds"])
    asset_source.setdefault("type", asset.get("media_type", "audio/wav"))

    # Existing shot items mirror a selected audio object for gallery/playback
    # surfaces. Update only rows that point at this clip/asset or old bytes.
    for item in payload.get("items", []):
        asset_key = item.get("metadata", {}).get("asset_key")
        item_media = _canonical_media_id(item.get("media_id"))
        if asset_key in {selector, str(clip["id"])} or (old_media and item_media == old_media):
            if item_media == old_media or asset_key in {selector, str(clip["id"])}:
                prior = item.get("media_id")
                item["media_id"] = (result["audio_media_id"].removeprefix("sha256:")
                                    if isinstance(prior, str) and not prior.startswith("sha256:")
                                    else result["audio_media_id"])


def _default_source_offset(value: Any) -> bool:
    """Match the canonical authoring compiler's untrimmed placement forms."""
    return value in (None, 0, 0.0, {}) or (
        isinstance(value, Mapping)
        and value.get("start", 0) == 0
        and value.get("end", 0) == 0
    )


def _default_speed(value: Any) -> bool:
    """Match the compiler's numeric and rational representations of 1x."""
    return value in (None, 1, 1.0) or (
        isinstance(value, Mapping)
        and value.get("numerator") == 1
        and value.get("denominator") == 1
    )


def _interval(clip: dict, start: float, end: float) -> None:
    old_duration = _duration(clip)
    if end <= start:
        raise VoiceoverSyncError("Retime would collapse a clip")
    clip["at"] = round(start, 9)
    if "hold" in clip:
        clip["hold"] = round(end - start, 9)
    else:
        clip["speed"] = float(clip.get("speed", 1)) * old_duration / (end - start)


def retime_candidate(candidate: dict, durations: Mapping[str, float], *, policy: str,
                     padding_seconds: float = 0.15) -> None:
    """Preserve placement lengths or ripple a nonoverlapping shot sequence.

    Ripple scales visual intervals and moves parent layers with the same
    piecewise time map. Audio other than the owned draft is never stretched.
    Parameterized clips need an explicit app.draft_voiceover_timing='stretch'
    declaration before their interval may be scaled; parameter internals remain
    the component owner's responsibility. Source offsets/speeds are rejected.
    """
    if policy not in {"preserve", "ripple"}:
        raise VoiceoverSyncError("timing_policy must be preserve or ripple")
    if not math.isfinite(padding_seconds) or padding_seconds < 0:
        raise VoiceoverSyncError("padding_seconds must be finite and nonnegative")
    placements = sorted(candidate["placements"], key=lambda p: p["placement"]["start_ms"])
    spans, delta = [], 0.0
    previous_end = -1.0
    for p in placements:
        start = p["placement"]["start_ms"] / 1000
        length = p["duration_ms"] / 1000
        if p["occurrence_id"] in durations:
            if (not _default_source_offset(p.get("source_offset"))
                    or not _default_speed(p.get("speed"))):
                raise VoiceoverSyncError("Draft narration retiming requires untrimmed speed-1 occurrences")
            audio_duration = durations[p["occurrence_id"]]
            if policy == "preserve" and audio_duration > length + 1e-9:
                raise VoiceoverSyncError("New narration exceeds preserved shot duration; choose ripple")
            new_length = math.ceil((audio_duration + padding_seconds) * 1000) / 1000 if policy == "ripple" else length
        else:
            new_length = length
        if policy == "ripple" and start < previous_end - 1e-9:
            raise VoiceoverSyncError("Ripple requires nonoverlapping shot placements")
        spans.append((start, start + length, start + delta, start + delta + new_length))
        previous_end = start + length
        if new_length != length:
            shot = candidate["shots"][p["shot_id"]]
            owned_id = shot["payload"].get("metadata", {}).get(KEY, {}).get("clip_id")
            for clip in shot["internal_timeline"].get("clips", []):
                if clip.get("id") == owned_id:
                    continue
                if clip in _audio_clips(shot):
                    raise VoiceoverSyncError("Ripple cannot stretch another audio clip")
                if clip.get("params") and clip.get("app", {}).get("draft_voiceover_timing") != "stretch":
                    raise VoiceoverSyncError("Parameterized internal clip needs explicit stretch permission")
                a = float(clip.get("at", 0))
                b = a + _duration(clip)
                _interval(clip, a * new_length / length, b * new_length / length)
            # config may carry an admitted duration mirror.
            if "duration" in shot["internal_timeline"]:
                shot["internal_timeline"]["duration"] = new_length
        p["placement"]["start_ms"] = round((start + delta) * 1000)
        p["duration_ms"] = round(new_length * 1000)
        delta += new_length - length
    if policy == "preserve" or not delta and all(a == c and b == d for a,b,c,d in spans):
        return
    def warp(t):
        shift = 0.0
        for a, b, c, d in spans:
            if t < a:
                return t + shift
            if t <= b:
                return c + (t - a) * (d - c) / (b - a)
            shift = d - b
        return t + shift
    for clip in candidate["parent"].get("clips", []):
        a = float(clip.get("at", 0))
        b = a + _duration(clip)
        c, d = warp(a), warp(b)
        if abs((d-c)-(b-a)) > 1e-8:
            if clip.get("params") and clip.get("app", {}).get("draft_voiceover_timing") != "stretch":
                raise VoiceoverSyncError("Parameterized parent layer needs explicit stretch permission")
            tracks = candidate["parent"].get("config", {}).get("tracks", [])
            if any(t.get("id") == clip.get("track") and t.get("kind") == "audio" for t in tracks):
                raise VoiceoverSyncError("Ripple cannot stretch parent audio")
        _interval(clip, c, d)
    config = candidate["parent"].get("config", {})
    if "clips" in config:
        config["clips"] = copy.deepcopy(candidate["parent"].get("clips", []))
    if "duration" in config:
        config["duration"] = warp(float(config["duration"]))


def prepare_draft_voiceover(candidate: Mapping, scripts: Mapping, *, synthesize: Callable,
                            settings=None, occurrence_ids=None, adopt_clip_ids=None,
                            timing_policy: str, padding_seconds=0.15,
                            available_media_ids=None) -> dict:
    plan = plan_draft_voiceover(candidate, scripts, settings=settings,
        occurrence_ids=occurrence_ids, adopt_clip_ids=adopt_clip_ids,
        available_media_ids=available_media_ids)
    work = copy.deepcopy(candidate)
    generated, durations = [], {}
    # Complete every synthesis before changing even the detached candidate.
    for job in plan["jobs"]:
        result = dict(synthesize(job["text"], job["settings"]))
        duration = float(result["duration_seconds"])
        media = result["audio_media_id"]
        if not math.isfinite(duration) or duration <= 0 or not isinstance(media, str) or not media.startswith("sha256:"):
            raise VoiceoverSyncError("Speech result lacks verified managed audio and duration")
        if result.get("text") != job["text"] or result.get("settings") != job["settings"]:
            raise VoiceoverSyncError("Speech provenance differs from requested words/settings")
        generated.append((job, result))
    for job, result in generated:
        shot = work["shots"][job["shot_id"]]
        internal = shot["internal_timeline"]
        clips = internal.setdefault("clips", [])
        clip = next((c for c in clips if c["id"] == job["clip_id"]), None)
        if clip is None:
            track = "draft-vo"
            tracks = internal.setdefault("tracks", [])
            if not any(t["id"] == track for t in tracks):
                tracks.append({"id": track, "kind": "audio"})
            clip = {"id": job["clip_id"], "track": track, "clipType": "media", "volume": 1}
            clips.append(clip)
        _bind_generated_audio(shot, clip, result)
        clip.update(at=0, **{"from": 0, "to": result["duration_seconds"]})
        shot["payload"].setdefault("metadata", {})[KEY] = {
            "schema_version": 1, "owner": "video_editing.sync_draft_voiceover", "status": "draft",
            "clip_id": clip["id"], "audio_media_id": result["audio_media_id"],
            "text": job["text"], "text_digest": digest(job["text"]), "settings": job["settings"],
            "duration_seconds": result["duration_seconds"], "generation_run_id": result.get("run_id"),
            "generation_task_id": result.get("task_id"), "source_parent_head": plan["base_head"],
        }
        durations[job["occurrence_id"]] = result["duration_seconds"]
    retime_candidate(work, durations, policy=timing_policy, padding_seconds=padding_seconds)
    return {"candidate": work, "plan": plan, "changed": bool(generated),
            "timing_policy": timing_policy, "padding_seconds": padding_seconds,
            "generated": [{"occurrence_id": job["occurrence_id"], **result} for job,result in generated]}


def _settled_speech_synthesizer(rows: list[Mapping[str, Any]]) -> Callable:
    """Adapt verified requester rows to the existing preparation callback."""
    cursor = iter(rows)

    def synthesize(text: str, settings: Mapping[str, Any]) -> dict[str, Any]:
        try:
            row = next(cursor)
        except StopIteration as exc:
            raise VoiceoverSyncError("Settled speech input has too few ordered rows") from exc
        if row.get("text") != text or row.get("settings") != settings:
            raise VoiceoverSyncError("Settled speech provenance differs from requested words/settings")
        output = row.get("output")
        if not isinstance(output, Mapping):
            raise VoiceoverSyncError("Settled speech input has no Runtime output binding")
        return {
            "text": text,
            "settings": dict(settings),
            "audio_media_id": row["audio_media_id"],
            "duration_seconds": row["duration_seconds"],
            "task_id": output.get("task_id"),
            "run_id": output.get("run_id"),
            "media_selection": dict(row["media_selection"]),
            "runtime_context": {"managed_output": dict(output)},
        }

    return synthesize


def _data(result):
    if hasattr(result, "ok"):
        if not result.ok:
            raise VoiceoverSyncError(str(result.error))
        return result.data
    return result.get("data", result)


def _artifact_identity(row):
    for key in ("object_id", "media_id", "content_hash", "digest", "sha256"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value if value.startswith("sha256:") else "sha256:" + value
    raise VoiceoverSyncError("Managed artifact has no digest")


def _speech_generation_intent(text: str, settings: Mapping[str, str]) -> dict[str, Any]:
    """Declare the existing single-output speech publication shape.

    The executor still receives the exact text/settings as ordinary inputs.
    This envelope only supplies Runtime's existing generation publication
    admission metadata; it does not claim a catalog selection or duration.
    """
    return {
        "version": 1,
        "modality": "audio",
        "partial_success_policy": "reject",
        "groups": [{
            "group_key": "main",
            "selectors": [{
                "selector": "speech",
                "ordinal": 0,
                "variant_key": "original",
                "required": True,
            }],
        }],
        "metadata": {
            "content_type": "audio",
            "voice": settings["voice"],
            "text_sha256": digest(text),
        },
    }


def _speech_runtime_context(result: Any, audio_row: Mapping[str, Any]) -> dict[str, Any]:
    """Keep terminal Runtime identity available to a future exact media read."""
    raw_result = getattr(result, "raw_result", {})
    raw_result = raw_result if isinstance(raw_result, Mapping) else {}
    settled = raw_result.get("result")
    settled = settled if isinstance(settled, Mapping) else {}
    task = raw_result.get("task")
    task = dict(task) if isinstance(task, Mapping) else None
    publication = settled.get("generation_publish_v1")
    publication = dict(publication) if isinstance(publication, Mapping) else None
    return {
        "task": task,
        "task_id": getattr(result, "kernel_task_id", None),
        "attempt_id": getattr(result, "kernel_attempt_id", None),
        "association_id": audio_row.get("association_id"),
        "managed_output": dict(audio_row),
        "generation_publish_v1": publication,
    }


def _workspace_media_client(client):
    """Use the fixed normal client chain, never a caller-installed reader."""
    from astrid.core.execution.executor._action_context import _PreparationClient
    from astrid.sdk.client import AstridClient
    from astrid.sdk.remote import RemoteAstridClient
    from astrid.sdk.workspace_client import WorkspaceClient

    if type(client) is _PreparationClient:
        client._context._check()
        client = client._client
    if (type(client) is not AstridClient
            or type(client._remote) is not RemoteAstridClient
            or type(client._remote._transport) is not WorkspaceClient):
        raise VoiceoverSyncError("Authoritative media reads require the normal Runtime client")
    return client._remote._transport


def _media_identity_claims(output: Mapping[str, Any]) -> dict[str, Any]:
    """Reject conflicting repeated identities before choosing a selector."""
    aliases = {"digest": "object_id", "media_id": "object_id", "content_hash": "object_id",
               "sha256": "object_id", "content_sha256": "object_id", "asset_id": "asset"}
    fields = {*_MEDIA_SELECTION_FIELDS, "project_id", "association_id", "version"}
    claims = {}
    pending = [output]
    while pending:
        row = pending.pop()
        for field, value in row.items():
            key = aliases.get(field, field)
            if key in fields:
                if key == "version":
                    valid = type(value) is int and value >= 1
                else:
                    valid = isinstance(value, str) and bool(value.strip())
                    if key in {"object_id", "catalog_digest"}:
                        valid = (valid and len(value) == 71 and value.startswith("sha256:")
                                 and all(c in "0123456789abcdef" for c in value[7:]))
                if not valid or (key in claims and claims[key] != value):
                    raise VoiceoverSyncError(f"Conflicting or invalid media {key}")
                claims[key] = value
            elif field in {"selection", "source", "scope", "selector", "lifecycle"}:
                if isinstance(value, Mapping):
                    pending.append(value)
    return claims


def _media_selector(output: Mapping[str, Any]) -> dict[str, Any]:
    """Send exactly one existing selector; retain all other claims for comparison."""
    claims = _media_identity_claims(output)
    if "association_id" in claims or "version" in claims:
        fields = ("association_id", "object_id", "version")
    else:
        fields = ("asset", "generation_id", "variant_id")
    if not all(key in claims for key in fields):
        raise VoiceoverSyncError("Settled managed output lacks an exact Runtime media selector")
    return {key: claims[key] for key in fields}


def _match_media_identity(output, project, selection):
    expected = {"project_id": project, **selection}
    for key, value in _media_identity_claims(output).items():
        if key in expected and value != expected[key]:
            raise VoiceoverSyncError(f"Runtime media {key} differs from the bound output")


def _read_authoritative_media_info(client: Any, project: str,
                                   output: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Read Runtime's exact pin and intrinsic metadata, then hash its bytes."""
    from astrid.sdk.workspace_client import WorkspaceClient

    workspace = _workspace_media_client(client)
    selector = _media_selector(output)
    claims = _media_identity_claims(output)
    if "project_id" in claims and claims["project_id"] != project:
        raise VoiceoverSyncError("Runtime media project_id differs from the bound output")
    selected = _data(WorkspaceClient.get_project_media_selection(workspace, project, selector))
    selection = _exact_media_selection(selected, label="Runtime media selection")
    if selection is None or selected != selection:
        raise VoiceoverSyncError("Runtime media selection is not the exact five-field selection")
    _match_media_identity(selection, project, selection)
    _match_media_identity(output, project, selection)
    verified = _data(WorkspaceClient.get_project_verified_media(workspace, project, selection))
    if not isinstance(verified, Mapping) or verified.get("selection") != selection:
        raise VoiceoverSyncError("Runtime verified media selection changed")
    _match_media_identity(verified, project, {**claims, **selection})
    media_type = verified.get("media_type")
    size = verified.get("size")
    duration = verified.get("duration_seconds")
    if media_type != "audio/wav":
        raise VoiceoverSyncError("Runtime settled voiceover media is not audio/wav")
    if type(size) is not int or size <= 0:
        raise VoiceoverSyncError("Runtime settled media lacks a verified byte size")
    if (isinstance(duration, bool) or not isinstance(duration, (int, float))
            or not math.isfinite(float(duration)) or duration <= 0):
        raise VoiceoverSyncError("Runtime settled media lacks a positive intrinsic duration")
    # Use the same WorkspaceClient for the ordinary managed object download.
    payload = WorkspaceClient.get_object(workspace, selection["object_id"]).get("data")
    if (not isinstance(payload, bytes) or len(payload) != size
            or "sha256:" + hashlib.sha256(payload).hexdigest() != selection["object_id"]):
        raise VoiceoverSyncError("Runtime settled media failed byte hash or size verification")
    return selection, {"selection": selection, "media_type": media_type,
                       "size": size, "duration_seconds": float(duration)}


def runtime_synthesizer(client, project, *, generation_intent: Mapping[str, Any] | None = None,
                        authoritative_media: bool = False):
    """Invoke speech through SDK; verify provenance bytes from managed outputs."""
    # A deliberate regeneration must not replay a failed or missing old output.
    # Share one identity within this batch; a later explicit sync gets a new one.
    request_context = {"draft_voiceover_sync": uuid.uuid4().hex}
    def synthesize(text, settings):
        import astrid.sdk as sdk
        intent = (generation_intent if generation_intent is not None
                  else _speech_generation_intent(text, settings))
        result = sdk.invoke("generation.generate_speech", kind="executor", project=project,
            inputs={"text": text, **settings, "generation_intent": intent}, client=client, wait=True,
            idempotency_context=request_context)
        if not result.ok:
            raise VoiceoverSyncError(str(result.error))
        artifacts = result.outputs.get("managed_outputs") or result.outputs.get("artifacts") or []
        manifest_row = next((r for r in artifacts if r.get("name") in {"speech_manifest", "manifest", "manifest.json"}
                             or r.get("output_port") in {"speech_manifest", "manifest"}
                             or str(r.get("path", "")).endswith("manifest.json")), None)
        audio_row = next((r for r in artifacts if r.get("name") in {"speech", "generated_audio"}
                          or r.get("output_port") in {"speech", "generated_audio"}
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
        settled = None
        duration = manifest["duration_seconds"]
        if authoritative_media:
            settled, info = _read_authoritative_media_info(client, project, audio_row)
            if settled["object_id"] != audio_id:
                raise VoiceoverSyncError("Runtime settled media differs from generated object")
            duration = info["duration_seconds"]
        return {"text": manifest["text"], "settings": manifest["settings"],
                "audio_media_id": audio_id, "duration_seconds": duration,
                "run_id": result.run_id, "task_id": result.kernel_task_id,
                "runtime_context": _speech_runtime_context(result, audio_row),
                **({"media_selection": settled} if settled is not None else {})}
    return synthesize


_MEDIA_SELECTION_FIELDS = ("asset", "generation_id", "variant_id", "object_id", "catalog_digest")
_PRODUCER_FIELDS = ("task_id", "attempt_id", "executor_id", "fence", "runtime_epoch")


def _exact_media_selection(value: Any, *, label: str) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    nested = value.get("selection")
    if isinstance(nested, Mapping):
        value = nested
    if not all(key in value for key in _MEDIA_SELECTION_FIELDS):
        return None
    selection = {key: value[key] for key in _MEDIA_SELECTION_FIELDS}
    if any(not isinstance(selection[key], str) or not selection[key]
           for key in _MEDIA_SELECTION_FIELDS):
        raise VoiceoverSyncError(f"{label} has an invalid five-field media selection")
    return selection


def _settled_media(result: Mapping[str, Any]) -> tuple[dict[str, Any], float, int]:
    """Read only a settled selection and intrinsic duration from the output row."""
    context = result.get("runtime_context")
    managed = context.get("managed_output") if isinstance(context, Mapping) else None
    candidates = [result.get("output"), result.get("media_selection"), managed]
    selected_row, selection = None, None
    for row in candidates:
        selection = _exact_media_selection(row, label="settled media")
        if selection is not None:
            selected_row = row
            break
    if selection is None:
        raise VoiceoverSyncError("Speech result lacks a settled five-field media selection")
    if selection["object_id"] != result.get("audio_media_id"):
        raise VoiceoverSyncError("Settled media differs from synthesized audio")
    duration = selected_row.get("intrinsic_duration_seconds", selected_row.get("duration_seconds"))
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) \
            or not math.isfinite(float(duration)) or float(duration) <= 0:
        raise VoiceoverSyncError("Settled media lacks a positive intrinsic duration")
    size = selected_row.get("size")
    if type(size) is not int or size <= 0:
        raise VoiceoverSyncError("Settled media lacks verified byte size")
    return selection, float(duration), size


def _candidate_media_selection(candidate: Mapping, job: Mapping[str, Any]) -> dict[str, Any] | None:
    shot = candidate.get("shots", {}).get(job.get("shot_id"), {})
    internal = shot.get("internal_timeline", {})
    clip = next((row for row in internal.get("clips", []) if row.get("id") == job.get("clip_id")), None)
    if not isinstance(clip, Mapping):
        return None
    values = [clip]
    assets = internal.get("registry", {}).get("assets", {})
    selector = clip.get("asset") or clip.get("asset_id")
    if isinstance(selector, str):
        values.append(assets.get(selector))
    for row in shot.get("payload", {}).get("assets", []):
        if isinstance(row, Mapping) and row.get("asset_id") == selector:
            values.append(row)
    selections = [_exact_media_selection(value, label="old media") for value in values]
    selection = next((value for value in selections if value is not None), None)
    if selection is not None:
        for value in values:
            if isinstance(value, Mapping):
                _match_media_identity(value, candidate["project_id"], selection)
    return selection


_TARGET_FIELDS = ("project_id", "timeline_id", "base_revision_id", "base_publication_id")


def _trusted_outer_context() -> tuple[dict[str, Any], dict[str, Any]]:
    """Read the host-owned context; caller and speech identity are not carriers."""
    try:
        from astrid.core.execution.executor._action_context import _require_action_context
    except (ImportError, AttributeError) as exc:
        raise VoiceoverSyncError(
            "Outer authoring proposal requires the private trusted host context"
        ) from exc
    try:
        context = _require_action_context()
        producer = dict(context.producer)
        admitted_target = dict(context.admitted_target)
    except (AttributeError, TypeError, ValueError) as exc:
        raise VoiceoverSyncError(
            "Outer authoring proposal requires the private trusted host context"
        ) from exc
    if set(producer) != set(_PRODUCER_FIELDS):
        raise VoiceoverSyncError("Trusted outer execution context is incomplete")
    if any(not isinstance(producer[key], str) or not producer[key].strip()
           for key in ("task_id", "attempt_id", "executor_id")):
        raise VoiceoverSyncError("Trusted outer producer identity is invalid")
    if any(type(producer[key]) is not int or producer[key] < 1
           for key in ("fence", "runtime_epoch")):
        raise VoiceoverSyncError("Trusted outer producer fence is invalid")
    if set(admitted_target) != set(_TARGET_FIELDS) or any(
            not isinstance(admitted_target[key], str) or not admitted_target[key].strip()
            for key in _TARGET_FIELDS):
        raise VoiceoverSyncError("Trusted outer admitted target is invalid")
    return producer, admitted_target


def _build_voiceover_proposal(*, producer: Mapping[str, Any], candidate: Mapping[str, Any],
                              base_publication_id: str, commands: list[dict[str, Any]],
                              admitted_target: Mapping[str, Any]) -> dict[str, Any]:
    from astrid.sdk.timeline.commit import _digest

    target = {
        "project_id": candidate["project_id"],
        "timeline_id": candidate["timeline_id"],
        "base_revision_id": candidate["base_parent"]["revision_id"],
        "base_publication_id": base_publication_id,
    }
    if dict(admitted_target) != target:
        raise VoiceoverSyncError("Prepared proposal does not match the admitted target")
    proposal = {
        "schema_version": 1,
        "producer": dict(producer),
        "admitted_target": target,
        "commands": copy.deepcopy(commands),
        "rationale": "Insert settled managed voiceover WAV and preserve its frozen script binding",
    }
    proposal["proposal_digest"] = _digest(proposal)
    return proposal


def _sync_draft_voiceover(client, project: str, timeline: str, *, timing_policy: str,
                         settings=None, occurrence_ids=None, adopt_clip_ids=None,
                         padding_seconds=0.15, plan_only=False,
                         managed_proposal=False, settled_speech_input=None,
                         attempt_root=None, requester_entry=False,
                         outbox_path=None) -> dict:
    """Run the shared preparation, with publication mode selected privately.

    No render is requested. Protected/empty/missing-script rows are reported.
    The source script is read from pinned runtime text; callers cannot inject it.
    """
    if timing_policy not in {"preserve", "ripple"}:
        raise VoiceoverSyncError("timing_policy must be preserve or ripple")
    if not math.isfinite(padding_seconds) or padding_seconds < 0:
        raise VoiceoverSyncError("padding_seconds must be finite and nonnegative")
    outer = _trusted_outer_context() if managed_proposal else None
    shown = _data(client.timelines.open_composition(project, timeline))
    head = shown["summary"]["head_revision_id"]
    base_publication_id = shown["summary"].get("head_publication_id") if managed_proposal else None
    scope = _data(client.timelines.resolve_scope(project, timeline))
    project_row = _data(client.projects.show(project))
    project_id = project_row.get("project_id") or project_row["id"]
    timeline_id = scope["timeline_id"]
    endpoint = getattr(client, "endpoint", None)
    endpoint = getattr(endpoint, "url", endpoint)
    bound = client.open_authoring_target({"endpoint": endpoint, "project_id": project_id,
        "timeline_id": timeline_id, "head_revision_id": head,
        "capabilities": {"edit": {"status": "available", "route": "authoring-bundle validate/commit"}}})
    candidate = bound.open()
    if managed_proposal:
        target = {"project_id": project_id, "timeline_id": timeline_id,
                  "base_revision_id": head, "base_publication_id": base_publication_id}
        if (target != outer[1] or candidate.get("project_id") != project_id
                or candidate.get("timeline_id") != timeline_id
                or candidate.get("base_parent", {}).get("revision_id") != head):
            raise VoiceoverSyncError("Prepared source does not match the admitted target")
    scripts = _data(client.timelines.script(project_id, timeline_id, revision_id=head))
    options = dict(settings=settings, occurrence_ids=occurrence_ids, adopt_clip_ids=adopt_clip_ids)
    plan = plan_draft_voiceover(candidate, scripts, **options)
    if requester_entry and not plan_only and plan["jobs"]:
        base_publication_id = shown["summary"].get("head_publication_id")
        if not isinstance(base_publication_id, str) or not base_publication_id:
            raise VoiceoverSyncError("Timeline head lacks its settled publication identity")
        from .voiceover_requester import _requester_sync_draft_voiceover

        return _requester_sync_draft_voiceover(
            client,
            project,
            timeline,
            candidate=candidate,
            scripts=scripts,
            admitted_target={
                "project_id": project_id,
                "timeline_id": timeline_id,
                "base_revision_id": head,
                "base_publication_id": base_publication_id,
            },
            timing_policy=timing_policy,
            settings=settings,
            occurrence_ids=occurrence_ids,
            adopt_clip_ids=adopt_clip_ids,
            padding_seconds=padding_seconds,
            outbox_path=outbox_path,
        )
    # Fresh provenance is reusable only while its managed audio bytes remain
    # readable and match the selected immutable identity. A missing object is
    # regenerated; authorization, integrity, and protocol errors stay visible.
    available_media_ids = set()
    for row in plan["statuses"]:
        if row.get("status") != "reused":
            continue
        shot = candidate["shots"][row["shot_id"]]
        clip = next(c for c in _audio_clips(shot) if c["id"] == row["clip_id"])
        media = selected_media(clip, shot["internal_timeline"])
        try:
            payload = client.media.read_bytes(media)
        except Exception as exc:
            if getattr(exc, "code", None) == "not_found":
                continue
            raise
        if not isinstance(payload, bytes) or "sha256:" + hashlib.sha256(payload).hexdigest() != media:
            raise VoiceoverSyncError("Selected draft audio failed managed-byte hash verification")
        available_media_ids.add(media)
    plan = plan_draft_voiceover(candidate, scripts,
        **options, available_media_ids=available_media_ids)
    if plan_only or not plan["jobs"]:
        return {"status": "planned" if plan_only else "unchanged", "plan": plan, "published": False}
    if managed_proposal and (not isinstance(base_publication_id, str) or not base_publication_id):
        raise VoiceoverSyncError("Timeline head lacks its settled publication identity")
    if settled_speech_input is not None:
        if attempt_root is None:
            raise VoiceoverSyncError("Settled speech input requires the managed attempt root")
        from .settled_voiceover_input import _consume_settled_voiceover_input

        settled_rows: list[Mapping[str, Any]] = []
        _consume_settled_voiceover_input(
            settled_speech_input,
            attempt_root=attempt_root,
            client=client,
            project=project_id,
            plan=plan,
            consume=settled_rows.append,
        )
        synthesizer = _settled_speech_synthesizer(settled_rows)
    else:
        synthesizer = (runtime_synthesizer(client, project_id, authoritative_media=True)
                       if managed_proposal else runtime_synthesizer(client, project_id))
    prepared = prepare_draft_voiceover(candidate, scripts,
        synthesize=synthesizer,
        timing_policy=timing_policy,
        padding_seconds=padding_seconds, available_media_ids=available_media_ids, **options)
    # Detect edits made while generation was in flight. Publication repeats the
    # check and Runtime CAS closes the final race. Never rebase stale speech.
    current = _data(client.timelines.open_composition(project_id, timeline_id))
    if (current["summary"]["head_revision_id"] != head
            or (managed_proposal
                and current["summary"].get("head_publication_id") != base_publication_id)):
        raise VoiceoverSyncError("Timeline changed during synthesis; rerun sync from its new head")
    bound.validate(prepared["candidate"])
    diff = bound.diff(prepared["candidate"])
    if not managed_proposal:
        frozen = bound.preview(prepared["candidate"])
        receipt = bound.publish(prepared["candidate"], idempotency_key=frozen["candidate_digest"])
        return {"status": "published", "published": True, "plan": plan, "diff": diff,
                "generated": prepared["generated"], "receipt": receipt}

    bound.preview(prepared["candidate"])

    from astrid.sdk.timeline.native_voiceover import capture_draft_voiceover
    from astrid.sdk.timeline.producer import build_producer_batch

    media_by_occurrence, verified_media, old_media_by_occurrence = {}, [], {}
    for result in prepared["generated"]:
        context = result.get("runtime_context")
        output = context.get("managed_output") if isinstance(context, Mapping) else None
        if not isinstance(output, Mapping):
            raise VoiceoverSyncError(
                "Managed voiceover proposal lacks the settled Runtime output binding"
            )
        selection, info = _read_authoritative_media_info(client, project_id, output)
        if (selection != result.get("media_selection")
                or selection["object_id"] != result["audio_media_id"]
                or info["duration_seconds"] != result["duration_seconds"]):
            raise VoiceoverSyncError("Runtime settled media changed during preparation")
        occurrence_id = result["occurrence_id"]
        media_by_occurrence[occurrence_id] = selection
        if not any(row["selection"] == selection for row in verified_media):
            verified_media.append(info)
        job = next(job for job in prepared["plan"]["jobs"]
                   if job["occurrence_id"] == occurrence_id)
        old = _candidate_media_selection(candidate, job)
        if old is not None:
            old_media_by_occurrence[occurrence_id] = old
            old_info_output = old
            old_selection, old_info = _read_authoritative_media_info(
                client, project_id, old_info_output)
            if old_selection != old:
                raise VoiceoverSyncError("Runtime old media selection differs from the authored source")
            if not any(row["selection"] == old_selection for row in verified_media):
                verified_media.append(old_info)
    captured = capture_draft_voiceover(
        candidate, prepared, media_by_occurrence=media_by_occurrence,
        verified_media=verified_media, old_media_by_occurrence=old_media_by_occurrence,
        timing_policy=timing_policy)
    proposal = _build_voiceover_proposal(
        producer=outer[0], candidate=candidate, base_publication_id=base_publication_id,
        commands=captured["commands"], admitted_target=outer[1])
    # Validate the exact existing six-key proposal and its single guard. The
    # requester later queues this original proposal through its outbox.
    build_producer_batch(proposal)
    return {"status": "proposal_ready", "published": False, "plan": plan, "diff": diff,
            "generated": prepared["generated"], "authoring_proposal": proposal}


def sync_draft_voiceover(client, project: str, timeline: str, *, timing_policy: str,
                         settings=None, occurrence_ids=None, adopt_clip_ids=None,
                         padding_seconds=0.15, plan_only=False) -> dict:
    """Preserve the existing public preparation, validation, and publication path."""
    return _sync_draft_voiceover(
        client, project, timeline, timing_policy=timing_policy, settings=settings,
        occurrence_ids=occurrence_ids, adopt_clip_ids=adopt_clip_ids,
        padding_seconds=padding_seconds, plan_only=plan_only,
    )


def _sync_draft_voiceover_proposal(client, project: str, timeline: str, *, timing_policy: str,
                                   settings=None, occurrence_ids=None, adopt_clip_ids=None,
                                   padding_seconds=0.15, plan_only=False,
                                   settled_speech_input=None, attempt_root=None) -> dict:
    """Private managed-producer entry; the requester owns proposal submission."""
    return _sync_draft_voiceover(
        client, project, timeline, timing_policy=timing_policy, settings=settings,
        occurrence_ids=occurrence_ids, adopt_clip_ids=adopt_clip_ids,
        padding_seconds=padding_seconds, plan_only=plan_only, managed_proposal=True,
        settled_speech_input=settled_speech_input, attempt_root=attempt_root,
    )
