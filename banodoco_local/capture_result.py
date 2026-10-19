"""Pure F246 capture serialization. Never runs commands or publishes raw bytes.

Original byte buffers stay immutable and private to the capture holder. Only
safe_record()/safe_json() are evidence projections. There is no text classifier,
exception formatter, request-id generator, retry, writer, or Runtime dependency.
The exact source pins and enumerations are in source-policy.json.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import re


PUBLIC_ERROR_CODES = frozenset({
    "conflict", "forbidden", "internal_error", "invalid_request", "lease_fenced",
    "no_committed_request", "not_found", "owner_busy", "protocol_error",
    "realm_admission_failed", "retired_route", "runtime_error", "unauthorized",
    "unavailable", "validation_error",
})
CLEANUP_ERROR_CODES = frozenset({"conflict", "enospc", "error", "os_error"})
ALLOWED_ERROR_CATEGORIES = PUBLIC_ERROR_CODES | CLEANUP_ERROR_CODES
# Deliberately narrower than arbitrary caller-supplied X-Request-ID. These are
# the two actual default producer forms; other strings are never echoed.
_REQUEST_ID = re.compile(r"(?:request-)?[0-9a-f]{32}", re.ASCII)
_MAX_JSON_BYTES = 1_048_576


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def _reject_constant(_):
    raise ValueError("nonfinite number")


def _bounded_fields(value):
    result = {}
    if type(value) is not dict:
        return result
    if type(value.get("ok")) is bool:
        result["ok"] = value["ok"]
    category = value.get("code")
    if type(category) is str and category in ALLOWED_ERROR_CATEGORIES:
        result["code"] = category
    status = value.get("status")
    if type(status) is int and 100 <= status <= 599:
        result["status"] = status
    request_id = value.get("request_id")
    if type(request_id) is str and _REQUEST_ID.fullmatch(request_id):
        result["request_id"] = request_id
    return result


def safe_fields(data: bytes) -> dict:
    """Retain finite source codes/typed identity fields; omit unsafe/absent data.

    Missing and null fields remain absent. A CLI free-text error is never
    reinterpreted as an HTTP code or a cleanup reason. Invalid JSON, duplicate
    keys, nonfinite data and oversized JSON yield no projected fields. The
    caller's original bytes are unaffected and still have an exact digest.
    """
    if type(data) is not bytes:
        raise TypeError("capture input must be immutable bytes")
    if len(data) > _MAX_JSON_BYTES:
        return {}
    try:
        value = json.loads(data, object_pairs_hook=_unique_pairs, parse_constant=_reject_constant)
    except (ValueError, UnicodeError, RecursionError):
        return {}
    result = _bounded_fields(value)
    if type(value) is dict:
        error = value.get("error")
        if type(error) is str and error in ALLOWED_ERROR_CATEGORIES:
            result["error"] = error
        elif type(error) is dict:
            projected = _bounded_fields(error)
            if projected:
                result["error"] = projected
    return result


def _summary(data: bytes, *, parse: bool) -> dict:
    result = {"byte_count": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    if parse:
        result["fields"] = safe_fields(data)
    return result


@dataclass(frozen=True, slots=True)
class CommandCapture:
    """Hold original primary/cleanup results without merging their failures.

    Raw buffers are excluded from repr. Do not serialize this object with a
    generic object/dataclass dumper: safe_json() is the publication boundary.
    This class performs no raw-buffer persistence, I/O, or command invocation.
    """

    returncode: int
    stdout: bytes = field(repr=False)
    stderr: bytes = field(default=b"", repr=False)
    result_bytes: bytes | None = field(default=None, repr=False)
    cleanup: CommandCapture | None = None

    def __post_init__(self):
        if type(self.returncode) is not int or not -(2**31) <= self.returncode < 2**31:
            raise TypeError("returncode must be a signed 32-bit integer")
        if (type(self.stdout) is not bytes or type(self.stderr) is not bytes
                or (self.result_bytes is not None and type(self.result_bytes) is not bytes)):
            raise TypeError("capture buffers must be immutable bytes")
        if self.cleanup is not None and (type(self.cleanup) is not CommandCapture or self.cleanup.cleanup is not None):
            raise TypeError("cleanup must be one separate command capture")

    def safe_record(self) -> dict:
        result = {
            "version": "f246.safe-command-capture/v1",
            "returncode": self.returncode,
            "stdout": _summary(self.stdout, parse=True),
            # stderr may be an arbitrary log. Never interpret or echo it.
            "stderr": _summary(self.stderr, parse=False),
        }
        if self.result_bytes is not None:
            result["result"] = _summary(self.result_bytes, parse=True)
        if self.cleanup is not None:
            result["cleanup"] = self.cleanup.safe_record()
        return result

    def safe_json(self) -> bytes:
        return (json.dumps(self.safe_record(), sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
