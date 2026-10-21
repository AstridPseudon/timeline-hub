"""Private requester-side speech preparation for managed voiceover.

The requesting session owns the speech roots and imports one immutable JSON
bundle for the later outer action.  The bundle is caller data: Runtime's
completed task/output and media reads remain the authority at the outer
boundary.  This module intentionally has no public entrypoint, outbox, or
task-launch wrapper.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

from .draft_voiceover import (
    VoiceoverSyncError,
    _read_authoritative_media_info,
    plan_draft_voiceover,
    settings_with_defaults,
)

_CARRIER_SCHEMA_VERSION = 1
_INPUT_NAME = "voiceover_speech_results"
_TARGET_FIELDS = frozenset(
    {"project_id", "timeline_id", "base_revision_id", "base_publication_id"}
)


def _stable_digest(value: Any) -> str:
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise VoiceoverSyncError("Voiceover requester identity must contain JSON values") from exc
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _json_copy(value: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    try:
        copied = json.loads(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                       allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise VoiceoverSyncError(f"{label} must contain JSON values") from exc
    if not isinstance(copied, dict):
        raise VoiceoverSyncError(f"{label} must be an object")
    return copied


def _validate_request_identity(
    *, project: str, candidate: Mapping[str, Any], scripts: Mapping[str, Any],
    requester_key: str, target: Mapping[str, Any], script_pin: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(requester_key, str) or not requester_key.strip():
        raise VoiceoverSyncError("Voiceover requester key must be nonempty")
    target_copy = _json_copy(target, label="Voiceover target")
    if set(target_copy) != _TARGET_FIELDS:
        raise VoiceoverSyncError("Voiceover target must preserve the original four-field pin")
    if any(not isinstance(target_copy[field], str) or not target_copy[field].strip()
           for field in _TARGET_FIELDS):
        raise VoiceoverSyncError("Voiceover target fields must be nonempty strings")
    if target_copy["project_id"] != project:
        raise VoiceoverSyncError("Voiceover target project differs from the requester project")
    if target_copy["project_id"] != candidate.get("project_id"):
        raise VoiceoverSyncError("Voiceover target differs from the candidate project")
    if target_copy["timeline_id"] != candidate.get("timeline_id"):
        raise VoiceoverSyncError("Voiceover target differs from the candidate timeline")
    if target_copy["base_revision_id"] != candidate.get("base_parent", {}).get("revision_id"):
        raise VoiceoverSyncError("Voiceover target differs from the candidate base revision")
    if target_copy["base_revision_id"] != scripts.get("revision_id"):
        raise VoiceoverSyncError("Voiceover target differs from the pinned script revision")

    script_copy = _json_copy(script_pin, label="Voiceover script pin")
    if script_copy.get("revision_id") != scripts.get("revision_id"):
        raise VoiceoverSyncError("Voiceover script pin differs from the loaded script revision")
    return target_copy, script_copy


def _root_idempotency_key(
    *, requester_key: str, target: Mapping[str, Any], script_pin: Mapping[str, Any],
    settings: Mapping[str, str], occurrence_id: str, text: str,
) -> str:
    identity = {
        "requester_key": requester_key,
        "target": target,
        "script_pin": script_pin,
        "settings": settings,
        "occurrence_id": occurrence_id,
        "text": text,
    }
    return "video-editing-voiceover-speech-" + _stable_digest(identity)[7:]


def _invocation_payload(result: Any) -> dict[str, Any]:
    """Use the existing H3 InvocationResult JSON payload shape."""
    to_dict = getattr(result, "to_dict", None)
    payload = to_dict() if callable(to_dict) else {
        field: getattr(result, field, None)
        for field in (
            "capability_id", "capability_type", "native_kind", "ok", "error",
            "manifest_path", "raw_result", "run_id", "run_root", "outputs",
            "executor_version", "kernel_run_id", "kernel_task_id",
            "kernel_attempt_id",
        )
    }
    if not isinstance(payload, Mapping):
        raise VoiceoverSyncError("Completed speech result did not serialize to an object")
    return dict(payload)


def _invocation_envelope(result: Any, *, input_digest: str) -> dict[str, Any]:
    payload = _invocation_payload(result)
    return {
        "schema_version": _CARRIER_SCHEMA_VERSION,
        "input_digest": input_digest,
        "result_digest": _stable_digest(payload),
        "result": payload,
    }


def _speech_output(result: Any) -> dict[str, Any]:
    if getattr(result, "ok", False) is not True:
        raise VoiceoverSyncError(f"Speech root did not complete: {getattr(result, 'error', result)}")
    if not all(isinstance(getattr(result, field, None), str)
               and getattr(result, field, "")
               for field in ("run_id", "kernel_task_id", "kernel_attempt_id")):
        raise VoiceoverSyncError("Completed speech result lacks Runtime task identity")
    output_rows = getattr(result, "output_rows", None)
    rows = output_rows("speech") if callable(output_rows) else []
    if len(rows) != 1 or not isinstance(rows[0], Mapping):
        raise VoiceoverSyncError("Completed speech result must contain one managed speech output")
    output = dict(rows[0])
    if output.get("task_id") not in (None, result.kernel_task_id):
        raise VoiceoverSyncError("Completed speech output task differs from its result")
    if output.get("attempt_id") not in (None, result.kernel_attempt_id):
        raise VoiceoverSyncError("Completed speech output attempt differs from its result")
    return output


def _import_bundle(client: Any, *, project: str, body: bytes, filename: str) -> dict[str, Any]:
    importer = getattr(getattr(client, "media", None), "import_bytes", None)
    if not callable(importer):
        raise VoiceoverSyncError("Requester client cannot import the speech result bundle")
    object_id = "sha256:" + hashlib.sha256(body).hexdigest()
    stored = importer(
        project=project,
        data=body,
        filename=filename,
        media_type="application/json",
        idempotency_key="video-editing-voiceover-input-" + object_id[7:],
    )
    if getattr(stored, "ok", True) is False:
        raise VoiceoverSyncError(f"Runtime rejected the speech result bundle: {stored}")
    data = getattr(stored, "data", stored)
    if not isinstance(data, Mapping):
        raise VoiceoverSyncError("Runtime speech result import returned no object descriptor")
    stored_id = data.get("object_id") or data.get("digest")
    if stored_id != object_id:
        raise VoiceoverSyncError("Imported speech result bundle differs from its digest")
    return {
        "name": _INPUT_NAME,
        "object_id": object_id,
        "digest": object_id,
        "filename": filename,
        "required": True,
    }


def _prepare_requester_speech_inputs(
    client: Any,
    project: str,
    candidate: Mapping[str, Any],
    scripts: Mapping[str, Any],
    *,
    requester_key: str,
    target: Mapping[str, Any],
    script_pin: Mapping[str, Any],
    settings: Mapping[str, Any] | None = None,
    occurrence_ids=None,
    adopt_clip_ids=None,
) -> list[dict[str, Any]]:
    """Prepare one immutable execution input for the existing outer action.

    Every changed occurrence gets one stable speech-root idempotency key.  The
    imported file is derived only from the original request and completed
    results, so an exact retry reuses the same key and bytes.  No duration is
    supplied to speech; intrinsic duration is read from Runtime's verified
    media response only as a pre-freeze check.
    """
    normalized_settings = settings_with_defaults(settings)
    target_copy, script_copy = _validate_request_identity(
        project=project, candidate=candidate, scripts=scripts,
        requester_key=requester_key, target=target, script_pin=script_pin,
    )
    plan = plan_draft_voiceover(
        candidate,
        scripts,
        settings=normalized_settings,
        occurrence_ids=occurrence_ids,
        adopt_clip_ids=adopt_clip_ids,
    )
    if not plan["jobs"]:
        return []

    import astrid.sdk as sdk

    entries: list[dict[str, Any]] = []
    for job in plan["jobs"]:
        occurrence_id = job["occurrence_id"]
        root_key = _root_idempotency_key(
            requester_key=requester_key, target=target_copy, script_pin=script_copy,
            settings=normalized_settings, occurrence_id=occurrence_id, text=job["text"],
        )
        root_inputs = {"text": job["text"], **normalized_settings}
        result = sdk.invoke(
            "generation.generate_speech",
            kind="executor",
            project=project,
            inputs=root_inputs,
            client=client,
            wait=True,
            idempotency_key=root_key,
        )
        output = _speech_output(result)
        # This read is deliberately not serialized as authority.  It proves
        # the completed result names an exact Runtime selection with verified
        # WAV bytes before the requester freezes caller data for the outer task.
        _read_authoritative_media_info(client, project, output)
        input_digest = _stable_digest({
            "capability_id": "generation.generate_speech",
            "kind": "executor",
            "project": project,
            "inputs": root_inputs,
        })
        entries.append({
            "occurrence_id": occurrence_id,
            "root_idempotency_key": root_key,
            "result": _invocation_envelope(result, input_digest=input_digest),
        })

    request_identity = {
        "requester_key": requester_key,
        "target": target_copy,
        "script_pin": script_copy,
        "settings": normalized_settings,
        "occurrence_ids": [entry["occurrence_id"] for entry in entries],
    }
    bundle = {
        "schema_version": _CARRIER_SCHEMA_VERSION,
        "request": request_identity,
        "results": entries,
    }
    body = (json.dumps(bundle, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    request_digest = _stable_digest(request_identity)
    filename = "voiceover-speech-results-" + request_digest[7:39] + ".json"
    return [_import_bundle(client, project=project, body=body, filename=filename)]
