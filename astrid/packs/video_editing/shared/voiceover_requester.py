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
import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable

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
_CAPABILITY = "generation.generate_speech"
_ENVELOPE_FIELDS = {"schema_version", "input_digest", "result_digest", "result"}
_RESULT_FIELDS = {
    "capability_id", "capability_type", "native_kind", "ok", "error",
    "manifest_path", "run_id", "run_root", "outputs", "raw_result",
    "executor_version", "kernel_run_id", "kernel_task_id", "kernel_attempt_id",
}
_REQUEST_FIELDS = {"requester_key", "target", "script_pin", "settings", "occurrence_ids"}
_ENTRY_FIELDS = {"occurrence_id", "root_idempotency_key", "text", "settings", "result"}


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
            "text": job["text"],
            "settings": dict(normalized_settings),
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


def _data(value: Any, label: str) -> Any:
    if hasattr(value, "ok") and hasattr(value, "data"):
        if not bool(value.ok):
            raise VoiceoverSyncError(f"NO-CARRIER: Runtime {label} read failed")
        value = value.data
    return value


def _text(value: Any, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise VoiceoverSyncError(f"settled voiceover {label} is invalid")
    return value


def _read_json(path: Path, *, attempt_root: Path) -> Mapping[str, Any]:
    """Read only the caller's already-materialized input file."""
    try:
        root = attempt_root.resolve(strict=True)
        if path.is_symlink():
            raise VoiceoverSyncError("settled voiceover input must not be a symlink")
        source = path.resolve(strict=True)
    except OSError as exc:
        raise VoiceoverSyncError("settled voiceover input is unavailable") from exc
    if source.is_symlink() or root == source or root not in source.parents:
        raise VoiceoverSyncError("settled voiceover input is outside its materialized attempt")
    try:
        if not source.is_file():
            raise VoiceoverSyncError("settled voiceover input is not a file")
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VoiceoverSyncError("settled voiceover input is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise VoiceoverSyncError("settled voiceover input must be an object")
    return value


def _jobs(plan: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    jobs = plan.get("jobs")
    if not isinstance(jobs, list) or not jobs or not all(isinstance(job, Mapping) for job in jobs):
        raise VoiceoverSyncError("settled voiceover plan has no ordered jobs")
    ids = [job.get("occurrence_id") for job in jobs]
    if any(type(value) is not str or not value for value in ids) or len(set(ids)) != len(ids):
        raise VoiceoverSyncError("settled voiceover plan has duplicate occurrences")
    return jobs


def _sha256(value: Any, label: str) -> str:
    digest = value
    if (type(digest) is not str or len(digest) != 71 or not digest.startswith("sha256:")
            or any(char not in "0123456789abcdef" for char in digest[7:])):
        raise VoiceoverSyncError(f"settled voiceover {label} is invalid")
    return digest


def _envelope(value: Any) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != _ENVELOPE_FIELDS:
        raise VoiceoverSyncError("settled speech result has an invalid H3 envelope")
    if value.get("schema_version") != _CARRIER_SCHEMA_VERSION:
        raise VoiceoverSyncError("settled speech result envelope version is unsupported")
    _sha256(value.get("input_digest"), "input digest")
    _sha256(value.get("result_digest"), "result digest")
    result = value["result"]
    if not isinstance(result, Mapping) or set(result) != _RESULT_FIELDS:
        raise VoiceoverSyncError("settled speech invocation result is incomplete")
    if value["result_digest"] != _stable_digest(result):
        raise VoiceoverSyncError("settled speech result failed its integrity check")
    return result


def _claimed_output(result: Mapping[str, Any]) -> Mapping[str, Any]:
    outputs = result.get("outputs")
    rows = outputs.get("managed_outputs") if isinstance(outputs, Mapping) else None
    if not isinstance(rows, list):
        raise VoiceoverSyncError("settled speech result has no managed output list")
    speech = [row for row in rows if isinstance(row, Mapping)
              and row.get("output_port") == "speech" and row.get("role") != "thumbnail"]
    if len(speech) != 1:
        raise VoiceoverSyncError("settled speech result must claim exactly one speech output")
    row = speech[0]
    if row.get("ordinal", 0) != 0:
        raise VoiceoverSyncError("settled speech output has an invalid ordinal")
    _text(row.get("object_id"), "output object_id")
    _text(row.get("task_id"), "output task_id")
    _text(row.get("attempt_id"), "output attempt_id")
    return row


def _request_identity(
    document: Mapping[str, Any], *, project: str, jobs: list[Mapping[str, Any]],
    target: Mapping[str, Any], script_pin: Mapping[str, Any], requester_key: str,
) -> Mapping[str, Any]:
    request = document.get("request")
    if not isinstance(request, Mapping) or set(request) != _REQUEST_FIELDS:
        raise VoiceoverSyncError("settled voiceover input has an invalid request identity")
    request_target = _json_copy(request.get("target"), label="settled voiceover target")
    if set(request_target) != _TARGET_FIELDS:
        raise VoiceoverSyncError("settled voiceover target must preserve the original four-field pin")
    if any(type(request_target[field]) is not str or not request_target[field].strip()
           for field in _TARGET_FIELDS):
        raise VoiceoverSyncError("settled voiceover target fields must be nonempty strings")
    if request_target["project_id"] != project:
        raise VoiceoverSyncError("settled voiceover target project differs from the requester project")
    request_script = _json_copy(request.get("script_pin"), label="settled voiceover script pin")
    if type(request.get("requester_key")) is not str or not request["requester_key"].strip():
        raise VoiceoverSyncError("settled voiceover requester key is invalid")
    settings = request.get("settings")
    if (not isinstance(settings, Mapping)
            or any(not isinstance(job.get("settings"), Mapping)
                   or dict(settings) != dict(job["settings"])
                   for job in jobs)):
        raise VoiceoverSyncError("settled voiceover request settings differ from the ordered plan")
    occurrence_ids = request.get("occurrence_ids")
    expected_ids = [job["occurrence_id"] for job in jobs]
    if occurrence_ids != expected_ids:
        raise VoiceoverSyncError("settled voiceover request occurrence order differs from the plan")
    expected_target = _json_copy(target, label="expected voiceover target")
    if set(expected_target) != _TARGET_FIELDS:
        raise VoiceoverSyncError("expected voiceover target must preserve the original four-field pin")
    if any(type(expected_target[field]) is not str or not expected_target[field].strip()
           for field in _TARGET_FIELDS):
        raise VoiceoverSyncError("expected voiceover target fields must be nonempty strings")
    if expected_target["project_id"] != project:
        raise VoiceoverSyncError("expected voiceover target project differs from the requester project")
    if request_target != expected_target:
        raise VoiceoverSyncError("settled voiceover target differs from the expected source")
    expected_script = _json_copy(script_pin, label="expected voiceover script pin")
    if request_script != expected_script:
        raise VoiceoverSyncError("settled voiceover script pin differs from the expected source")
    if type(requester_key) is not str or not requester_key.strip():
        raise VoiceoverSyncError("expected voiceover requester key is invalid")
    if request["requester_key"] != requester_key:
        raise VoiceoverSyncError("settled voiceover requester key differs from the expected source")
    return request


def _task_inputs(task: Mapping[str, Any], *, text: str, settings: Mapping[str, Any]) -> None:
    spec = task.get("spec")
    if isinstance(spec, Mapping) and isinstance(spec.get("spec"), Mapping):
        spec = spec["spec"]
    values = spec.get("inputs") if isinstance(spec, Mapping) else None
    if not isinstance(values, Mapping):
        raise VoiceoverSyncError("NO-CARRIER: settled speech task has no authoritative inputs")
    actual = {}
    for key, value in values.items():
        if isinstance(value, Mapping) and set(value) == {"value"}:
            value = value["value"]
        actual[key] = value
    expected = {"text": text, **dict(settings)}
    if actual != expected:
        raise VoiceoverSyncError("settled speech task inputs differ from the plan")


def _runtime_output(client: Any, project: str, result: Mapping[str, Any],
                    claimed: Mapping[str, Any], task: Mapping[str, Any]) -> Mapping[str, Any]:
    task_id = _text(result.get("kernel_task_id"), "task_id")
    run_id = _text(result.get("kernel_run_id"), "run_id")
    attempt_id = _text(result.get("kernel_attempt_id"), "attempt_id")
    actual_task_id = task.get("task_id", task.get("id"))
    capability = task.get("capability_id", task.get("capability"))
    if (actual_task_id != task_id or task.get("run_id") != run_id
            or task.get("attempt_id") != attempt_id):
        raise VoiceoverSyncError("settled speech task identity differs from Runtime")
    if task.get("project_id") != project or capability != _CAPABILITY:
        raise VoiceoverSyncError("settled speech task project or capability differs from Runtime")
    state = str(task.get("state") or task.get("status") or "").lower()
    if state not in {"succeeded", "completed"}:
        raise VoiceoverSyncError("settled speech task is not completed")
    task_result = task.get("result")
    if not isinstance(task_result, Mapping):
        raise VoiceoverSyncError("NO-CARRIER: settled speech task has no completed result")
    for field, expected in (("task_id", task_id), ("run_id", run_id),
                            ("attempt_id", attempt_id), ("project_id", project)):
        if field in task_result and task_result[field] != expected:
            raise VoiceoverSyncError("settled speech task result identity differs from Runtime")
    task_outputs = task_result.get("outputs")
    if not isinstance(task_outputs, list):
        raise VoiceoverSyncError("NO-CARRIER: settled speech result has no output list")
    matching_task_rows = [
        row for row in task_outputs
        if isinstance(row, Mapping)
        and (row.get("output_port") or row.get("name")) == "speech"
        and (row.get("object_id") or row.get("digest")) == claimed.get("object_id")
        and row.get("role") != "thumbnail"
    ]
    if len(matching_task_rows) != 1:
        raise VoiceoverSyncError("settled speech task result does not contain the claimed output")
    task_row = matching_task_rows[0]
    for field, expected in (("task_id", task_id), ("run_id", run_id),
                            ("attempt_id", attempt_id), ("project_id", project)):
        if field in task_row and task_row[field] != expected:
            raise VoiceoverSyncError("settled speech task output identity differs from Runtime")
    try:
        managed = _data(client.tasks.list_managed_outputs(task_id), "managed output")
    except Exception as exc:  # noqa: BLE001 - unavailable authority is fail-closed
        raise VoiceoverSyncError("NO-CARRIER: Runtime managed output read is unavailable") from exc
    if isinstance(managed, tuple) and len(managed) == 2:
        managed = managed[0]
    if not isinstance(managed, list):
        raise VoiceoverSyncError("NO-CARRIER: Runtime managed output read is unavailable")
    matches = [row for row in managed if isinstance(row, Mapping)
               and row.get("output_port") == "speech" and row.get("role") != "thumbnail"]
    if len(matches) != 1:
        raise VoiceoverSyncError("Runtime must expose exactly one settled speech output")
    row = matches[0]
    for field, expected in (("task_id", task_id), ("run_id", run_id),
                            ("attempt_id", attempt_id), ("project_id", project)):
        if row.get(field) != expected:
            raise VoiceoverSyncError("settled speech output is not bound to its task attempt")
    if row.get("object_id") != claimed.get("object_id"):
        raise VoiceoverSyncError("settled speech output differs from the claimed object")
    return row


def _consume_settled_voiceover_input(
    path: str | Path,
    *,
    attempt_root: str | Path,
    client: Any,
    project: str,
    plan: Mapping[str, Any],
    consume: Callable[[Mapping[str, Any]], Any],
    target: Mapping[str, Any],
    script_pin: Mapping[str, Any],
    requester_key: str,
) -> list[Any]:
    """Consume one requester's file after re-reading every Runtime claim.

    The file is claimant data.  H3 envelope digests detect malformed transport
    data, but Runtime task/spec/result, managed-output, media-selection, WAV
    bytes, and intrinsic duration reads remain the authority.  Trusted outer
    identity is validated here but is intentionally not copied into the
    consumed rows; the caller supplies it separately to the existing
    capture/proposal path.
    """
    if not _text(project, "project") or not callable(consume):
        raise VoiceoverSyncError("settled voiceover consumer arguments are invalid")
    jobs = _jobs(plan)
    document = _read_json(Path(path), attempt_root=Path(attempt_root))
    if set(document) != {"schema_version", "request", "results"} or document.get("schema_version") != _CARRIER_SCHEMA_VERSION:
        raise VoiceoverSyncError("settled voiceover input has an unsupported shape")
    request = _request_identity(document, project=project, jobs=jobs, target=target,
                                script_pin=script_pin, requester_key=requester_key)
    entries = document.get("results")
    if not isinstance(entries, list) or len(entries) != len(jobs):
        raise VoiceoverSyncError("settled voiceover input is missing an ordered entry for every job")
    prepared: list[tuple[str, str, Mapping[str, Any], str, Mapping[str, Any], Mapping[str, Any]]] = []
    for job, entry in zip(jobs, entries):
        if not isinstance(entry, Mapping) or set(entry) != _ENTRY_FIELDS:
            raise VoiceoverSyncError("settled voiceover entry has unsupported fields")
        occurrence_id = entry.get("occurrence_id")
        if occurrence_id != job.get("occurrence_id"):
            raise VoiceoverSyncError("settled voiceover entries differ from the ordered plan")
        text = entry.get("text")
        settings = entry.get("settings")
        if text != job.get("text") or settings != job.get("settings"):
            raise VoiceoverSyncError("settled voiceover entry differs from the ordered plan")
        if not isinstance(text, str) or not isinstance(settings, Mapping):
            raise VoiceoverSyncError("settled voiceover entry values are invalid")
        root_key = entry.get("root_idempotency_key")
        expected_key = _root_idempotency_key(
            requester_key=request["requester_key"], target=request["target"],
            script_pin=request["script_pin"], settings=settings,
            occurrence_id=occurrence_id, text=text,
        )
        if root_key != expected_key:
            raise VoiceoverSyncError("settled voiceover root idempotency key differs from the request")
        envelope = entry["result"]
        result = _envelope(envelope)
        expected_input_digest = _stable_digest({
            "capability_id": _CAPABILITY, "kind": "executor", "project": project,
            "inputs": {"text": text, **dict(settings)},
        })
        if envelope["input_digest"] != expected_input_digest:
            raise VoiceoverSyncError("settled speech input digest differs from the request")
        if (result.get("capability_id") != _CAPABILITY
                or result.get("capability_type") != "executor"
                or result.get("native_kind") != "executor" or result.get("ok") is not True):
            raise VoiceoverSyncError("settled speech result has the wrong capability or status")
        claimed = _claimed_output(result)
        prepared.append((occurrence_id, text, settings, root_key, result, claimed))

    verified_rows: list[dict[str, Any]] = []
    for occurrence_id, text, settings, root_key, result, claimed in prepared:
        try:
            task = _data(client.tasks.show(_text(result.get("kernel_task_id"), "task_id")), "task")
        except Exception as exc:  # noqa: BLE001 - unavailable authority is fail-closed
            raise VoiceoverSyncError("NO-CARRIER: Runtime task read is unavailable") from exc
        if not isinstance(task, Mapping):
            raise VoiceoverSyncError("NO-CARRIER: Runtime task read returned no task")
        _task_inputs(task, text=text, settings=settings)
        output = _runtime_output(client, project, result, claimed, task)
        try:
            selection, verified = _read_authoritative_media_info(client, project, output)
        except VoiceoverSyncError:
            raise
        except Exception as exc:  # noqa: BLE001 - unavailable authority is fail-closed
            raise VoiceoverSyncError("NO-CARRIER: Runtime media read is unavailable") from exc
        duration = verified.get("duration_seconds")
        if (isinstance(duration, bool) or not isinstance(duration, (int, float))
                or not math.isfinite(float(duration)) or duration <= 0):
            raise VoiceoverSyncError("Runtime settled speech duration is invalid")
        verified_rows.append({
            "occurrence_id": occurrence_id,
            "text": text,
            "settings": dict(settings),
            "root_idempotency_key": root_key,
            "audio_media_id": selection["object_id"],
            "media_selection": selection,
            "duration_seconds": float(duration),
            "output": dict(output),
        })
    return [consume(row) for row in verified_rows]
