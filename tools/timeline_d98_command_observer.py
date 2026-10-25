"""Passive D98 command-pair observer for the existing Runtime route.

Install this file as ``sitecustomize.py`` in a private evidence directory and
put that directory first on the existing route's ``PYTHONPATH``.  Python then
loads the observer in the caller and Runtime processes without changing the
caller, provider, request, or refusal path.

The observer is deliberately narrow: it watches only the existing
``timeline_commit_auth.validate_claims`` frame and writes a record only when
that frame raises while its submitted and recorded command pairs differ.  It
never serializes a command value, request body, exception text, traceback, or
credential.  If the target frame or trace slot is unavailable it stays quiet.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from types import FrameType
from typing import Any, Callable

_TARGET_NAME = "validate_claims"
_TARGET_FILE = "timeline_commit_auth.py"
_SCHEMA = "d98-command-pair-v1"
_KNOWN_FIELDS = frozenset(
    {
        "api_version",
        "args",
        "asset",
        "at",
        "authorship",
        "bindings",
        "command",
        "commands",
        "clipType",
        "created",
        "expect",
        "hold",
        "id",
        "intent",
        "media",
        "media_id",
        "old_media",
        "op",
        "ordinal",
        "reads",
        "record",
        "records",
        "resolved",
        "row",
        "schema_version",
        "select",
        "selections",
        "shot_id",
        "track",
        "version",
    }
)
_ABSENT = object()


def _evidence_dir() -> Path | None:
    raw = os.environ.get("D98_EVIDENCE_DIR")
    if not raw:
        return None
    try:
        path = Path(raw).resolve()
    except (OSError, RuntimeError, ValueError):
        return None
    return path if path.is_absolute() else None


def _canonical(value: Any) -> bytes:
    """Encode JSON-like values without invoking repr or user code."""

    if value is _ABSENT:
        value = {"state": "absent"}
    if value is None or isinstance(value, (bool, int, float, str)):
        return json.dumps(value, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode()
    if isinstance(value, list):
        return b"[" + b",".join(_canonical(item) for item in value) + b"]"
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        pairs = sorted((key, _canonical(item)) for key, item in value.items())
        return b"{" + b",".join(
            json.dumps(key, ensure_ascii=True, separators=(",", ":")).encode() + b":" + item
            for key, item in pairs
        ) + b"}"
    # Unsupported values are not expected in an authenticated JSON record.
    # A type marker keeps the diagnostic safe if an introspection boundary is
    # reached during a partial failure.
    return json.dumps({"type": type(value).__name__}, separators=(",", ":")).encode()


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _shape(value: Any) -> dict[str, Any]:
    if value is _ABSENT:
        return {"state": "absent"}
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, str):
        return {"type": "string", "length": len(value)}
    if isinstance(value, list):
        return {"type": "array", "length": len(value)}
    if isinstance(value, dict):
        return {"type": "object", "fields": len(value)}
    return {"type": type(value).__name__}


def _token(key: Any) -> str:
    if isinstance(key, str) and key in _KNOWN_FIELDS:
        return key
    return "key#" + _sha256(key)[:16]


def _path(prefix: str, child: Any) -> str:
    if isinstance(child, int):
        return f"{prefix}[{child}]"
    return f"{prefix}.{_token(child)}" if prefix else _token(child)


def _differences(left: Any, right: Any, prefix: str = "command") -> list[tuple[str, Any, Any]]:
    if left is _ABSENT or right is _ABSENT:
        return [(prefix, left, right)] if left is not right else []
    if type(left) is not type(right):
        return [(prefix, left, right)]
    if isinstance(left, dict):
        keys = sorted(set(left) | set(right), key=_canonical)
        result: list[tuple[str, Any, Any]] = []
        for key in keys:
            result.extend(
                _differences(left.get(key, _ABSENT), right.get(key, _ABSENT), _path(prefix, key))
            )
        return result
    if isinstance(left, list):
        result = []
        for index in range(max(len(left), len(right))):
            result.extend(
                _differences(
                    left[index] if index < len(left) else _ABSENT,
                    right[index] if index < len(right) else _ABSENT,
                    _path(prefix, index),
                )
            )
        return result
    return [(prefix, left, right)] if left != right else []


def _safe_side(value: Any) -> dict[str, Any]:
    return {"shape": _shape(value), "sha256": _sha256(value)}


def _input_tuple_digest(request: dict[str, Any], ordinal: int) -> str:
    tuple_identity = {
        "project_id": request.get("project_id", _ABSENT),
        "timeline_id": request.get("timeline_id", _ABSENT),
        "base_revision_id": request.get("base_revision_id", _ABSENT),
        "base_publication_id": request.get("base_publication_id", _ABSENT),
        "command_ordinal": ordinal,
    }
    return _sha256(tuple_identity)


def _comparison(
    request: dict[str, Any], command_ordinal: int, record_ordinal: int, label: str,
    submitted: Any, recorded: Any,
) -> dict[str, Any] | None:
    differences = _differences(submitted, recorded)
    if not differences:
        return None
    paths = []
    submitted_sides: dict[str, Any] = {}
    recorded_sides: dict[str, Any] = {}
    for field_path, left, right in differences:
        paths.append(field_path)
        submitted_sides[field_path] = _safe_side(left)
        recorded_sides[field_path] = _safe_side(right)
    return {
        "comparison": label,
        "record_ordinal": record_ordinal,
        "input_tuple_sha256": _input_tuple_digest(request, command_ordinal),
        "differing_field_paths": paths,
        "submitted": submitted_sides,
        "recorded": recorded_sides,
    }


def _record_differences(request: Any, records: Any) -> list[dict[str, Any]]:
    if not isinstance(request, dict) or not isinstance(records, dict):
        return []
    submitted_commands = request.get("commands")
    recorded_commands = records.get("commands")
    if not isinstance(submitted_commands, list) or not isinstance(recorded_commands, list):
        return []
    result: list[dict[str, Any]] = []
    for ordinal, submitted in enumerate(submitted_commands):
        if ordinal >= len(recorded_commands) or not isinstance(submitted, dict):
            continue
        record = recorded_commands[ordinal]
        if not isinstance(record, dict):
            continue
        record_ordinal = record.get("ordinal")
        if type(record_ordinal) is not int:
            record_ordinal = ordinal
        recorded_command = record.get("command", _ABSENT)
        comparisons = [
            _comparison(
                request, ordinal, record_ordinal, "submitted_command_vs_records.command",
                submitted, recorded_command,
            ),
            _comparison(
                request,
                ordinal,
                record_ordinal,
                "submitted_created_vs_records.command.created",
                submitted.get("created", []),
                recorded_command.get("created", _ABSENT)
                if isinstance(recorded_command, dict)
                else _ABSENT,
            ),
            _comparison(
                request,
                ordinal,
                record_ordinal,
                "submitted_created_vs_records.created",
                submitted.get("created", []),
                record.get("created", _ABSENT),
            ),
        ]
        result.extend(item for item in comparisons if item is not None)
    return result


def _write(value: dict[str, Any]) -> None:
    evidence = _evidence_dir()
    if evidence is None:
        return
    try:
        evidence.mkdir(parents=True, exist_ok=True)
        path = evidence / f"d98-command-observer-{os.getpid()}.jsonl"
        line = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
        flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
        fd = os.open(path, flags, 0o600)
        try:
            os.write(fd, line)
            os.fsync(fd)
        finally:
            os.close(fd)
    except (OSError, TypeError, ValueError):
        # Diagnostics must never affect the route or replace its refusal.
        return


def _observer_hash() -> str:
    try:
        return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        return "unavailable"


def _trace_frame(frame: FrameType, event: str, arg: Any) -> Callable[..., Any] | None:
    if event != "exception":
        return _trace_frame
    try:
        exception = arg[1] if isinstance(arg, tuple) and len(arg) == 3 else None
        if type(exception).__name__ != "CommitRejected":
            return _trace_frame
        failure = getattr(exception, "failure", None)
        details = failure.get("details") if isinstance(failure, dict) else None
        if not isinstance(details, dict) or details.get("reason") != "provider executed a different command":
            return _trace_frame
        request = frame.f_locals.get("request")
        records = frame.f_locals.get("records")
        for comparison in _record_differences(request, records):
            _write(
                {
                    "schema": _SCHEMA,
                    "event": "existing_refusal_command_mismatch",
                    "observer_sha256": _observer_hash(),
                    **comparison,
                }
            )
    except (AttributeError, KeyError, TypeError, ValueError):
        return _trace_frame
    return _trace_frame


def _trace(frame: FrameType, event: str, arg: Any) -> Callable[..., Any] | None:
    if event == "call" and frame.f_code.co_name == _TARGET_NAME:
        if Path(frame.f_code.co_filename).name == _TARGET_FILE:
            return _trace_frame
    return None


def activate() -> bool:
    """Install one passive trace, or return false without touching the route."""

    if _evidence_dir() is None or sys.gettrace() is not None:
        return False
    try:
        sys.settrace(_trace)
    except (RuntimeError, TypeError):
        return False
    _write(
        {
            "schema": _SCHEMA,
            "event": "observer_active",
            "observer_sha256": _observer_hash(),
            "target": f"{_TARGET_FILE}:{_TARGET_NAME}",
        }
    )
    return True


activate()
