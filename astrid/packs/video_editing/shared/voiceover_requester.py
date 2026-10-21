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


def _requester_sync_draft_voiceover(
    client: Any,
    project: str,
    timeline: str,
    *,
    candidate: Mapping[str, Any],
    scripts: Mapping[str, Any],
    admitted_target: Mapping[str, Any],
    timing_policy: str,
    settings: Mapping[str, Any] | None = None,
    occurrence_ids=None,
    adopt_clip_ids=None,
    padding_seconds: float = 0.15,
    plan_only: bool = False,
    outbox_path=None,
):
    """Keep the reviewed requester/action/outbox chain dormant.

    This is a private source seam for a containing operation that already has
    the exact candidate, script read, and admitted target.  It deliberately
    does not become the public/default voiceover caller: the surrounding
    operation must decide when this native admission is available.
    """
    if plan_only:
        raise VoiceoverSyncError("dormant requester path does not settle plan-only work")
    if not isinstance(admitted_target, Mapping):
        raise VoiceoverSyncError("requester voiceover target must be an object")
    target = dict(admitted_target)
    if set(target) != {"project_id", "timeline_id", "base_revision_id", "base_publication_id"}:
        raise VoiceoverSyncError("requester voiceover target is not the existing four-field pin")
    if target.get("project_id") != project or target.get("timeline_id") != timeline:
        raise VoiceoverSyncError("requester voiceover target differs from its project or timeline")

    descriptors = _prepare_requester_speech_inputs(
        client,
        project,
        candidate,
        scripts,
        settings=settings,
        occurrence_ids=occurrence_ids,
        adopt_clip_ids=adopt_clip_ids,
    )
    if not descriptors:
        return {"status": "unchanged", "published": False}
    if len(descriptors) != 1 or not isinstance(descriptors[0], Mapping):
        raise VoiceoverSyncError("requester voiceover must use one ordered bundle descriptor")
    input_object_ids = [descriptor["object_id"] for descriptor in descriptors]
    if any(not isinstance(value, str) or not value for value in input_object_ids):
        raise VoiceoverSyncError("requester voiceover input descriptors lack object IDs")

    action = "video_editing.sync_draft_voiceover"
    action_inputs = {
        "project": project,
        "timeline_ref": timeline,
        "timing_policy": timing_policy,
        "settings": dict(settings or {}),
        "occurrence_ids": occurrence_ids,
        "adopt_clip_ids": adopt_clip_ids or [],
        "padding_seconds": padding_seconds,
        "plan_only": False,
        "settled_speech_input": descriptors[0],
    }
    execution_request = {
        "schema_version": 1,
        "target": {"kind": "default"},
        "inputs": descriptors,
    }
    spec = {
        "capability_id": action,
        "kind": "executor",
        "inputs": action_inputs,
        "outputs": {"authoring_proposal": {
            "type": "file", "artifact_type": "timeline/authoring-proposal",
        }},
        "runtime_dependencies": {"publication": {"admitted_target": target}},
    }
    admission_key = "video-editing-sync-draft-voiceover-" + _stable_digest({
        "action": action,
        "target": target,
        "inputs": input_object_ids,
        "timing_policy": timing_policy,
    })[7:]
    admitted = client.tasks.create(
        project_id=project,
        capability=action,
        spec=spec,
        input_manifest=input_object_ids,
        execution_request=execution_request,
        idempotency_key=admission_key,
    )
    if getattr(admitted, "ok", True) is False:
        raise VoiceoverSyncError(f"Runtime rejected the outer voiceover admission: {admitted}")
    admitted_data = getattr(admitted, "data", admitted)
    if not isinstance(admitted_data, Mapping):
        raise VoiceoverSyncError("Runtime outer voiceover admission returned no task")
    task = admitted_data.get("task") if isinstance(admitted_data.get("task"), Mapping) else admitted_data
    task_id = task.get("task_id") or task.get("id")
    run_id = task.get("run_id")
    if not isinstance(task_id, str) or not task_id or not isinstance(run_id, str) or not run_id:
        raise VoiceoverSyncError("Runtime outer voiceover admission lacks task/run identity")

    from astrid.sdk import observe_task_invocation

    result = observe_task_invocation(
        client,
        capability_id=action,
        capability_type="executor",
        native_kind="executor",
        task_id=task_id,
        run_id=run_id,
        wait=True,
        read_managed_outputs=True,
    )
    if not result.ok:
        raise VoiceoverSyncError(f"Outer voiceover action did not settle: {result}")
    rows = result.output_rows("authoring_proposal")
    if len(rows) != 1:
        raise VoiceoverSyncError("Outer voiceover action must settle one authoring proposal")
    object_id = rows[0].get("object_id") or rows[0].get("digest")
    if not isinstance(object_id, str) or not object_id:
        raise VoiceoverSyncError("Outer authoring proposal has no managed object identity")
    raw = client.media.read_bytes(object_id)
    try:
        proposal = json.loads(raw)
    except (TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VoiceoverSyncError("Outer authoring proposal is not valid JSON") from exc
    proposal_target = proposal.get("admitted_target") if isinstance(proposal, Mapping) else None
    if not isinstance(proposal_target, Mapping) or dict(proposal_target) != target:
        raise VoiceoverSyncError("Outer authoring proposal changed the admitted target")

    from astrid.sdk.timeline.producer import build_producer_batch
    from astrid.sdk.timeline.sync import TimelineSession

    build_producer_batch(proposal)
    session = TimelineSession.open(
        project,
        timeline,
        client=client,
        outbox_path=outbox_path,
        base_revision_id=target["base_revision_id"],
        base_publication_id=target["base_publication_id"],
    )
    session.queue_proposal(proposal)
    acceptance = session.flush(idempotency_key="timeline-producer-" + proposal["proposal_digest"][7:])
    return {"status": "published", "published": True, "proposal": dict(proposal),
            "admission": admitted_data, "acceptance": acceptance}
