"""Private consumer for requester-settled speech inputs.

The JSON file is an execution-request materialized input, not a settlement
record.  Its H3-shaped invocation results only locate the inner tasks and
their claimed outputs.  Every identity, terminal state, output association,
media selection, byte hash, and duration is read again from Runtime before a
caller-owned preparation/capture callback sees an audio row.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable, Mapping

from .draft_voiceover import VoiceoverSyncError, _read_authoritative_media_info

_CAPABILITY = "generation.generate_speech"
_ENVELOPE_FIELDS = {"schema_version", "input_digest", "result_digest", "result"}
_RESULT_FIELDS = {
    "capability_id", "capability_type", "native_kind", "ok", "error",
    "manifest_path", "run_id", "run_root", "outputs", "raw_result",
    "executor_version", "kernel_run_id", "kernel_task_id", "kernel_attempt_id",
}
_ENTRY_FIELDS = {"occurrence_id", "text", "settings", "result"}


def _stable_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


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


def _envelope(value: Any) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != _ENVELOPE_FIELDS:
        raise VoiceoverSyncError("settled speech result has an invalid H3 envelope")
    if value.get("schema_version") != 1:
        raise VoiceoverSyncError("settled speech result envelope version is unsupported")
    for field in ("input_digest", "result_digest"):
        digest = value.get(field)
        if (type(digest) is not str or len(digest) != 71 or not digest.startswith("sha256:")
                or any(char not in "0123456789abcdef" for char in digest[7:])):
            raise VoiceoverSyncError(f"settled speech result {field} is invalid")
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
    return row


def _task_inputs(task: Mapping[str, Any], *, text: str, settings: Mapping[str, Any]) -> None:
    spec = task.get("spec")
    values = spec.get("inputs") if isinstance(spec, Mapping) else None
    if not isinstance(values, Mapping):
        raise VoiceoverSyncError("NO-CARRIER: settled speech task has no authoritative inputs")
    expected = {"text": text, **dict(settings)}
    for key, wanted in expected.items():
        actual = values.get(key)
        if isinstance(actual, Mapping) and set(actual) == {"value"}:
            actual = actual["value"]
        if actual != wanted:
            raise VoiceoverSyncError(f"settled speech task input {key!r} differs from the plan")


def _runtime_output(client: Any, project: str, result: Mapping[str, Any], claimed: Mapping[str, Any],
                    task: Mapping[str, Any]) -> Mapping[str, Any]:
    task_id = _text(result.get("kernel_task_id"), "task_id")
    run_id = _text(result.get("kernel_run_id"), "run_id")
    attempt_id = _text(result.get("kernel_attempt_id"), "attempt_id")
    if result.get("run_id") != run_id:
        raise VoiceoverSyncError("settled speech result run identity differs from Runtime")
    actual_task_id = task.get("task_id", task.get("id"))
    if actual_task_id != task_id or task.get("run_id") != run_id or task.get("attempt_id") != attempt_id:
        raise VoiceoverSyncError("settled speech task identity differs from Runtime")
    if task.get("project_id") != project or task.get("capability", task.get("capability_id")) != _CAPABILITY:
        raise VoiceoverSyncError("settled speech task project or capability differs from Runtime")
    state = str(task.get("state") or task.get("status") or "").lower()
    if state not in {"succeeded", "completed"}:
        raise VoiceoverSyncError("settled speech task is not completed")
    if not isinstance(task.get("result"), Mapping):
        raise VoiceoverSyncError("NO-CARRIER: settled speech task has no completed result")
    task_outputs = task["result"].get("outputs")
    if not isinstance(task_outputs, list):
        raise VoiceoverSyncError("NO-CARRIER: settled speech result has no output list")
    if not any(
            isinstance(row, Mapping)
            and (row.get("output_port") or row.get("name")) == "speech"
            and (row.get("object_id") or row.get("digest")) == claimed.get("object_id")
            for row in task_outputs):
        raise VoiceoverSyncError("settled speech task result does not contain the claimed output")
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
    if (row.get("task_id") != task_id
            or row.get("attempt_id") != attempt_id
            or row.get("project_id") != project
            or row.get("object_id") != claimed.get("object_id")):
        raise VoiceoverSyncError("settled speech output is not bound to its task attempt")
    return row


def _consume_settled_voiceover_input(
    path: str | Path,
    *,
    attempt_root: str | Path,
    client: Any,
    project: str,
    plan: Mapping[str, Any],
    consume: Callable[[Mapping[str, Any]], Any],
) -> list[Any]:
    """Consume requester-settled speech rows through existing preparation code.

    ``consume`` receives one immutable mapping per ordered plan job with the
    Runtime-selected five-field ``media_selection``, verified WAV identity,
    and Runtime's intrinsic ``duration_seconds``.  It is deliberately private
    and dormant: the outer action caller must explicitly join it later.
    """
    if not _text(project, "project") or not callable(consume):
        raise VoiceoverSyncError("settled voiceover consumer arguments are invalid")
    jobs = _jobs(plan)
    document = _read_json(Path(path), attempt_root=Path(attempt_root))
    entries = document.get("entries")
    if not isinstance(entries, list) or len(entries) != len(jobs):
        raise VoiceoverSyncError("settled voiceover input is missing an ordered entry for every job")
    seen: set[str] = set()
    prepared: list[tuple[str, str, Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]] = []
    for job, entry in zip(jobs, entries):
        if not isinstance(entry, Mapping) or set(entry) != _ENTRY_FIELDS:
            raise VoiceoverSyncError("settled voiceover entry has unsupported fields")
        occurrence_id = entry.get("occurrence_id")
        if type(occurrence_id) is not str or occurrence_id in seen:
            raise VoiceoverSyncError("settled voiceover entries contain duplicate occurrences")
        seen.add(occurrence_id)
        if occurrence_id != job.get("occurrence_id") or entry.get("text") != job.get("text") \
                or entry.get("settings") != job.get("settings"):
            raise VoiceoverSyncError("settled voiceover entry differs from the ordered plan")
        result = _envelope(entry["result"])
        if result.get("capability_id") != _CAPABILITY or result.get("capability_type") != "executor" \
                or result.get("native_kind") != "executor" or result.get("ok") is not True:
            raise VoiceoverSyncError("settled speech result has the wrong capability or status")
        claimed = _claimed_output(result)
        if not isinstance(entry["settings"], Mapping):
            raise VoiceoverSyncError("settled voiceover settings are invalid")
        prepared.append((occurrence_id, entry["text"], entry["settings"], result, claimed))

    verified_rows: list[dict[str, Any]] = []
    for occurrence_id, text, settings, result, claimed in prepared:
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
            "audio_media_id": selection["object_id"],
            "media_selection": selection,
            "duration_seconds": float(duration),
            "output": dict(output),
        })
    return [consume(row) for row in verified_rows]
