"""Private requester-side carrier for already-settled speech results.

The requester owns speech-root creation and imports one immutable JSON file.
The managed outer action only receives the resulting ordinary CAS file input;
it rechecks every task, output, media-selection, and duration fact before use.
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
from .settled_voiceover_input import _stable_digest

_CAPABILITY = "generation.generate_speech"
_INPUT_NAME = "settled_speech_input"


def _invocation_payload(result: Any) -> dict[str, Any]:
    to_dict = getattr(result, "to_dict", None)
    payload = to_dict() if callable(to_dict) else {
        field: getattr(result, field, None)
        for field in (
            "capability_id", "capability_type", "native_kind", "ok", "error",
            "manifest_path", "run_id", "run_root", "outputs", "raw_result",
            "executor_version", "kernel_run_id", "kernel_task_id", "kernel_attempt_id",
        )
    }
    if not isinstance(payload, Mapping):
        raise VoiceoverSyncError("Completed speech result did not serialize to an object")
    return dict(payload)


def _speech_output(result: Any) -> dict[str, Any]:
    if getattr(result, "ok", False) is not True:
        raise VoiceoverSyncError(f"Speech root did not complete: {getattr(result, 'error', result)}")
    if any(not isinstance(getattr(result, field, None), str)
           or not getattr(result, field, "")
           for field in ("run_id", "kernel_run_id", "kernel_task_id", "kernel_attempt_id")):
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


def _invocation_envelope(result: Any, *, input_digest: str) -> dict[str, Any]:
    payload = _invocation_payload(result)
    return {
        "schema_version": 1,
        "input_digest": input_digest,
        "result_digest": _stable_digest(payload),
        "result": payload,
    }


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
    settings: Mapping[str, Any] | None = None,
    occurrence_ids=None,
    adopt_clip_ids=None,
) -> list[dict[str, Any]]:
    """Create one ordinary execution-input descriptor for settled speech.

    Speech roots are requester-owned. The carrier contains only the H3 result
    envelopes and ordered script values; intrinsic duration is read from
    Runtime's verified media response and is never serialized as claimant data.
    """
    normalized_settings = settings_with_defaults(settings)
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
        root_inputs = {"text": job["text"], **normalized_settings}
        root_key = "video-editing-voiceover-speech-" + _stable_digest({
            "project": project,
            "candidate_base": candidate.get("base_parent", {}).get("revision_id"),
            "occurrence_id": job["occurrence_id"],
            "inputs": root_inputs,
        })[7:]
        result = sdk.invoke(
            _CAPABILITY,
            kind="executor",
            project=project,
            inputs=root_inputs,
            client=client,
            wait=True,
            idempotency_key=root_key,
        )
        output = _speech_output(result)
        _read_authoritative_media_info(client, project, output)
        entries.append({
            "occurrence_id": job["occurrence_id"],
            "text": job["text"],
            "settings": dict(job["settings"]),
            "result": _invocation_envelope(
                result,
                input_digest=_stable_digest({
                    "capability_id": _CAPABILITY,
                    "project": project,
                    "inputs": root_inputs,
                }),
            ),
        })

    body = (json.dumps({"entries": entries}, indent=2, sort_keys=True) + "\n").encode()
    filename = "settled-speech-" + hashlib.sha256(body).hexdigest()[:32] + ".json"
    return [_import_bundle(client, project=project, body=body, filename=filename)]
