"""Immutable request and trusted result values for transcript publication.

This module owns only the value contract.  Publishing effects and caller
authority remain in the Host-owned adapter and transcript publisher.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from astrid.sdk.contracts import derive_stable_id
from astrid.sdk.managed_transcript import (
    TRANSCRIPT_DOCUMENT_KIND,
    TRANSCRIPT_SCHEMA_ID,
    TranscriptRecord,
    canonical_transcript_json,
    transcript_document_id,
    validate_transcript_record,
)

_PUBLISH_ACTION_ID = "media.transcript_publish"
_SHA256 = re.compile(r"^(?:sha256:)?([0-9a-f]{64})$")
_CANONICAL_SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


def _nonblank(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{field} must be a canonical non-empty string")
    return value


def _digest_hex(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a SHA-256 digest")
    match = _SHA256.fullmatch(value)
    if match is None:
        raise ValueError(f"{field} must be a lowercase SHA-256 digest")
    return match.group(1)


def _check_version(value: Any, *, field: str) -> None:
    if value is not None and (type(value) is not int or value < 0):
        raise ValueError(f"{field} must be a non-negative integer or null")


@dataclass(frozen=True, slots=True)
class TranscriptParentSelection:
    """Exact immutable parent pins used when validating a transcript correction."""

    expected_document_version: int
    lineage_id: str
    revision_id: str
    content_digest: str
    snapshot_object_id: str

    def __post_init__(self) -> None:
        _check_version(self.expected_document_version, field="parent_selection.expected_document_version")
        if self.expected_document_version is None:
            raise ValueError("parent_selection.expected_document_version is required")
        _nonblank(self.lineage_id, field="parent_selection.lineage_id")
        _nonblank(self.revision_id, field="parent_selection.revision_id")
        content_digest = _digest_hex(self.content_digest, field="parent_selection.content_digest")
        if not isinstance(self.snapshot_object_id, str) or not _CANONICAL_SHA256.fullmatch(
            self.snapshot_object_id
        ):
            raise ValueError("parent_selection.snapshot_object_id must be a sha256 object ID")
        if content_digest != self.snapshot_object_id.removeprefix("sha256:"):
            raise ValueError("parent selection content digest and snapshot object ID must match")


@dataclass(frozen=True, slots=True)
class PreparedTranscriptPublication:
    """Frozen, replayable data request; it carries no publication authority."""

    project_id: str
    document_id: str
    expected_document_version: int | None
    request_id: str
    admitted_action_id: str
    producer_digest: str
    canonical_record_json: str
    content_digest: str
    snapshot_object_id: str
    parent_selection: TranscriptParentSelection | None

    def __post_init__(self) -> None:
        _nonblank(self.project_id, field="project_id")
        _nonblank(self.document_id, field="document_id")
        _check_version(self.expected_document_version, field="expected_document_version")
        _nonblank(self.request_id, field="request_id")
        if self.admitted_action_id != _PUBLISH_ACTION_ID:
            raise ValueError("admitted_action_id must be media.transcript_publish")
        _digest_hex(self.producer_digest, field="producer_digest")
        if not isinstance(self.canonical_record_json, str) or not self.canonical_record_json:
            raise ValueError("canonical_record_json must be non-empty text")
        if not isinstance(self.content_digest, str) or not _CANONICAL_SHA256.fullmatch(
            self.content_digest
        ):
            raise ValueError("content_digest must be a sha256 digest")
        if not isinstance(self.snapshot_object_id, str) or not _CANONICAL_SHA256.fullmatch(
            self.snapshot_object_id
        ):
            raise ValueError("snapshot_object_id must be a sha256 object ID")
        if self.content_digest != self.snapshot_object_id:
            raise ValueError("content_digest and snapshot_object_id must identify the same bytes")
        if self.parent_selection is not None:
            if not isinstance(self.parent_selection, TranscriptParentSelection):
                raise TypeError("parent_selection must be a TranscriptParentSelection or None")
            if self.parent_selection.expected_document_version != self.expected_document_version:
                raise ValueError("parent selection version must match expected_document_version")


def _revision_id(
    *, project_id: str, document_id: str, admitted_action_id: str, request_id: str
) -> str:
    """Use the SDK's UUID5 stable-ID convention for one logical request."""
    scope = json.dumps(
        [project_id, document_id],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return derive_stable_id(
        command_kind=admitted_action_id,
        scope=scope,
        idempotency_key=request_id,
    )


def prepare_transcript_publication(
    record: Mapping[str, Any],
    *,
    project_id: str,
    expected_document_version: int | None,
    request_id: str,
    admitted_action_id: str,
    producer_digest: str,
    parent_selection: TranscriptParentSelection | None,
) -> PreparedTranscriptPublication:
    """Build a pure frozen request using the existing managed-transcript codec."""
    _nonblank(project_id, field="project_id")
    _check_version(expected_document_version, field="expected_document_version")
    _nonblank(request_id, field="request_id")
    if admitted_action_id != _PUBLISH_ACTION_ID:
        raise ValueError("admitted_action_id must be media.transcript_publish")
    supplied_producer_digest = _digest_hex(producer_digest, field="producer_digest")

    validated: TranscriptRecord = validate_transcript_record(record)
    record_producer_digest = _digest_hex(
        validated["source"]["producer_digest"], field="record.source.producer_digest"
    )
    if supplied_producer_digest != record_producer_digest:
        raise ValueError("producer_digest must match record.source.producer_digest")

    document_id = transcript_document_id(project_id, validated["subject"], validated["source"])
    revision_id = _revision_id(
        project_id=project_id,
        document_id=document_id,
        admitted_action_id=admitted_action_id,
        request_id=request_id,
    )
    publication_record = dict(validated)
    publication_record["source"] = {**validated["source"], "revision_id": revision_id}
    canonical_record_json = canonical_transcript_json(publication_record)

    # Encode once.  Both the document digest and CAS locator identify these
    # exact UTF-8 bytes, not a later JSON dump of the same value.
    canonical_bytes = canonical_record_json.encode("utf-8")
    snapshot_object_id = "sha256:" + hashlib.sha256(canonical_bytes).hexdigest()

    return PreparedTranscriptPublication(
        project_id=project_id,
        document_id=document_id,
        expected_document_version=expected_document_version,
        request_id=request_id,
        admitted_action_id=admitted_action_id,
        producer_digest=producer_digest,
        canonical_record_json=canonical_record_json,
        content_digest=snapshot_object_id,
        snapshot_object_id=snapshot_object_id,
        parent_selection=parent_selection,
    )


def _freeze_json(value: Any) -> Any:
    """Copy generated JSON values into recursively immutable containers."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_json(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_json(item) for item in value)
    return value


@dataclass(frozen=True, slots=True, init=False)
class ResolvedTranscriptPublication:
    """Internal immutable capture of bound WorkspaceClient data and CAS bytes."""

    data: Mapping[str, Any]
    receipt: Mapping[str, Any]
    prepared: PreparedTranscriptPublication
    snapshot_object_id: str
    snapshot_bytes: bytes

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        raise TypeError(
            "ResolvedTranscriptPublication is an internal capture; use the trusted SDK capture path"
        )


def _capture_resolved_transcript_publication(
    prepared: PreparedTranscriptPublication,
    mutation_response: Mapping[str, Any],
    *,
    snapshot_object_id: str,
    snapshot_response: Mapping[str, Any],
) -> ResolvedTranscriptPublication:
    """Capture normalized WorkspaceClient values after trusted verification.

    WorkspaceClient._call_generated converts generated mutation and byte
    responses to stable mappings. The trusted adapter passes these exact values
    here after the trusted publisher validates caller scope and result identity;
    it must not bypass the selected WorkspaceClient boundary.
    """
    if not isinstance(prepared, PreparedTranscriptPublication):
        raise TypeError("prepared must be a PreparedTranscriptPublication")
    if not isinstance(mutation_response, Mapping) or set(mutation_response) != {
        "data", "receipt"
    }:
        raise TypeError("mutation_response must be the normalized WorkspaceClient envelope")
    data_value = mutation_response["data"]
    receipt = mutation_response["receipt"]
    if not isinstance(data_value, Mapping) or not isinstance(receipt, Mapping):
        raise ValueError("WorkspaceClient mutation envelope must contain data and a committed receipt")
    if not isinstance(snapshot_response, Mapping) or set(snapshot_response) != {
        "data", "status", "headers"
    }:
        raise TypeError("snapshot_response must be the normalized WorkspaceClient byte response")
    snapshot_bytes = snapshot_response["data"]
    snapshot_status = snapshot_response["status"]
    if (
        type(snapshot_status) is not int
        or snapshot_status != 200
        or not isinstance(snapshot_bytes, bytes)
        or not isinstance(snapshot_response["headers"], Mapping)
    ):
        raise ValueError("snapshot response must contain a complete 200 byte response")
    if snapshot_object_id != prepared.snapshot_object_id:
        raise ValueError("snapshot locator does not match the prepared request")
    if "sha256:" + hashlib.sha256(snapshot_bytes).hexdigest() != snapshot_object_id:
        raise ValueError("snapshot bytes do not match their content-addressed locator")
    try:
        if snapshot_bytes.decode("utf-8") != prepared.canonical_record_json:
            raise ValueError("snapshot bytes do not match the prepared canonical record")
    except UnicodeDecodeError as exc:
        raise ValueError("snapshot bytes are not valid UTF-8") from exc

    data = dict(data_value)

    capture = object.__new__(ResolvedTranscriptPublication)
    object.__setattr__(capture, "data", _freeze_json(data))
    object.__setattr__(capture, "receipt", _freeze_json(receipt))
    object.__setattr__(capture, "prepared", prepared)
    object.__setattr__(capture, "snapshot_object_id", snapshot_object_id)
    object.__setattr__(capture, "snapshot_bytes", bytes(snapshot_bytes))
    return capture


__all__ = [
    "PreparedTranscriptPublication",
    "ResolvedTranscriptPublication",
    "TranscriptParentSelection",
    "TRANSCRIPT_DOCUMENT_KIND",
    "TRANSCRIPT_SCHEMA_ID",
    "prepare_transcript_publication",
]
