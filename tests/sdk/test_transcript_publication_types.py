from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import FrozenInstanceError, asdict
from importlib.resources import files
from typing import Any

import jsonschema
import pytest

from astrid.sdk.contracts import derive_stable_id
from astrid.sdk.managed_transcript import (
    TRANSCRIPT_DOCUMENT_KIND,
    canonical_transcript_json,
    transcript_document_id,
    validate_transcript_record,
)
from astrid.sdk.transcript_publication_types import (
    PreparedTranscriptPublication,
    ResolvedTranscriptPublication,
    TranscriptParentSelection,
    _capture_resolved_transcript_publication,
    prepare_transcript_publication,
)
from banodoco_workspace_client.generated import ByteResponse, MutationResult

ACTION_ID = "media.transcript_publish"
PROJECT_ID = "project-synthetic"
PRODUCER_DIGEST = "sha256:" + "a" * 64


def _record() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "subject": {
            "media_object_id": "sha256:" + "b" * 64,
            "media_sha256": "b" * 64,
        },
        "source": {
            "producer_id": "fixture-producer",
            "source_id": "fixture-source",
            "lineage_id": "lineage-synthetic",
            "revision_id": "caller-supplied-revision-is-replaced",
            "producer_digest": PRODUCER_DIGEST,
        },
        "clock": {"kind": "media", "unit": "seconds", "origin_seconds": 0},
        "words": [{"id": "w1", "text": "café", "start_s": 0.0, "end_s": 0.25}],
        "segments": [{"id": "s1", "word_ids": ["w1"]}],
        "metadata": {"opaque": {"tags": ["kept", "as-is"]}},
        "provenance": {"generator": "synthetic fixture", "opaque_flag": True},
    }


def _prepare(
    *,
    request_id: str = "request-synthetic-1",
    expected_document_version: int | None = None,
    parent_selection: TranscriptParentSelection | None = None,
    record: dict[str, Any] | None = None,
    **overrides: Any,
) -> PreparedTranscriptPublication:
    values: dict[str, Any] = {
        "project_id": PROJECT_ID,
        "expected_document_version": expected_document_version,
        "request_id": request_id,
        "admitted_action_id": ACTION_ID,
        "producer_digest": PRODUCER_DIGEST,
        "parent_selection": parent_selection,
    }
    values.update(overrides)
    return prepare_transcript_publication(record or _record(), **values)


def _schema() -> dict[str, Any]:
    return json.loads(
        files("astrid")
        .joinpath("packs", "media", "schemas", "transcript-publication-request-v1.json")
        .read_text(encoding="utf-8")
    )


def _envelope(prepared: PreparedTranscriptPublication) -> dict[str, Any]:
    return {
        **{
            key: getattr(prepared, key)
            for key in (
                "project_id",
                "document_id",
                "expected_document_version",
                "request_id",
                "admitted_action_id",
                "producer_digest",
                "canonical_record_json",
                "content_digest",
                "snapshot_object_id",
            )
        },
        "parent_selection": (
            asdict(prepared.parent_selection) if prepared.parent_selection is not None else None
        ),
    }


def test_prepared_envelope_schema_is_strict_and_accepts_canonical_shape():
    prepared = _prepare()
    envelope = _envelope(prepared)
    schema = _schema()
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)

    validator.validate(envelope)
    validate_transcript_record(json.loads(prepared.canonical_record_json))
    assert _schema()["$id"] == "media.transcript-publication-request/v1"

    with pytest.raises(jsonschema.ValidationError):
        validator.validate({**envelope, "unrecognized": "field"})
    missing = dict(envelope)
    del missing["request_id"]
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(missing)
    wrong_action = {**envelope, "admitted_action_id": "media.transcript_read"}
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(wrong_action)

    parent_digest = "sha256:" + "c" * 64
    parent = TranscriptParentSelection(
        expected_document_version=3,
        lineage_id="lineage-parent",
        revision_id="revision-parent",
        content_digest=parent_digest,
        snapshot_object_id=parent_digest,
    )
    correction = _prepare(expected_document_version=3, parent_selection=parent)
    validator.validate(_envelope(correction))
    bad_parent = _envelope(correction)
    bad_parent["parent_selection"] = {
        **bad_parent["parent_selection"],
        "unrecognized": "field",
    }
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad_parent)


def test_builder_reuses_exact_helper_text_and_hashes_one_canonical_byte_sequence():
    original = _record()
    request = _prepare(record=original)
    decoded = validate_transcript_record(json.loads(request.canonical_record_json))
    expected_id = transcript_document_id(PROJECT_ID, original["subject"], original["source"])
    expected_revision = derive_stable_id(
        command_kind=ACTION_ID,
        scope=json.dumps([PROJECT_ID, expected_id], ensure_ascii=False, separators=(",", ":")),
        idempotency_key=request.request_id,
    )
    expected_record = copy.deepcopy(original)
    expected_record["source"]["revision_id"] = expected_revision
    expected_text = canonical_transcript_json(expected_record)
    expected_bytes = expected_text.encode("utf-8")
    expected_digest = "sha256:" + hashlib.sha256(expected_bytes).hexdigest()

    assert request.document_id == expected_id
    assert request.canonical_record_json == expected_text
    assert request.content_digest == expected_digest
    assert request.snapshot_object_id == expected_digest
    assert decoded["source"]["revision_id"] == expected_revision
    assert decoded["metadata"] == original["metadata"]
    assert decoded["provenance"] == original["provenance"]
    assert original["source"]["revision_id"] == "caller-supplied-revision-is-replaced"


def test_same_request_reuses_identity_and_new_request_gets_new_logical_revision():
    first = _prepare()
    retry = _prepare()
    next_request = _prepare(request_id="request-synthetic-2")
    first_record = json.loads(first.canonical_record_json)
    retry_record = json.loads(retry.canonical_record_json)
    next_record = json.loads(next_request.canonical_record_json)

    assert first.request_id == retry.request_id
    assert first.document_id == retry.document_id == next_request.document_id
    assert first.canonical_record_json == retry.canonical_record_json
    assert first.snapshot_object_id == retry.snapshot_object_id
    assert first_record["source"]["revision_id"] == retry_record["source"]["revision_id"]
    assert next_request.request_id != first.request_id
    assert next_record["source"]["revision_id"] != first_record["source"]["revision_id"]
    assert next_request.content_digest != first.content_digest


def test_prepared_request_and_parent_selection_are_frozen():
    digest = "sha256:" + "c" * 64
    parent = TranscriptParentSelection(
        expected_document_version=3,
        lineage_id="lineage-parent",
        revision_id="revision-parent",
        content_digest=digest,
        snapshot_object_id=digest,
    )
    request = _prepare(expected_document_version=3, parent_selection=parent)

    with pytest.raises(FrozenInstanceError):
        request.request_id = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        parent.revision_id = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"expected_document_version": True}, "expected_document_version"),
        ({"expected_document_version": -1}, "expected_document_version"),
        ({"admitted_action_id": "media.transcript_read"}, "admitted_action_id"),
        ({"producer_digest": "sha256:" + "d" * 64}, "producer_digest"),
    ],
)
def test_invalid_publication_preconditions_fail_closed(overrides, message):
    with pytest.raises(ValueError, match=message):
        _prepare(**overrides)


def test_parent_version_must_match_prepared_expected_version():
    digest = "sha256:" + "c" * 64
    parent = TranscriptParentSelection(
        expected_document_version=2,
        lineage_id="lineage-parent",
        revision_id="revision-parent",
        content_digest=digest,
        snapshot_object_id=digest,
    )
    with pytest.raises(ValueError, match="must match"):
        _prepare(expected_document_version=3, parent_selection=parent)
    with pytest.raises(ValueError, match="must match"):
        _prepare(parent_selection=parent)


def test_capture_requires_generated_mutation_and_byte_response_and_freezes_them():
    prepared = _prepare()
    expected_content = json.loads(prepared.canonical_record_json)
    mutation = MutationResult(
        {
            "project_id": prepared.project_id,
            "document_id": prepared.document_id,
            "kind": TRANSCRIPT_DOCUMENT_KIND,
            "content": expected_content,
            "version": 1,
        },
        {"receipt_id": "receipt-synthetic", "project_id": prepared.project_id},
    )
    snapshot = ByteResponse(prepared.canonical_record_json.encode("utf-8"), 200, {})
    captured = _capture_resolved_transcript_publication(
        prepared,
        mutation,
        snapshot_object_id=prepared.snapshot_object_id,
        snapshot_response=snapshot,
    )

    assert captured.prepared is prepared
    assert captured.data["content"]["source"]["revision_id"] == expected_content["source"]["revision_id"]
    assert captured.data["content"]["metadata"]["opaque"]["tags"] == ("kept", "as-is")
    assert captured.receipt["receipt_id"] == "receipt-synthetic"
    assert captured.snapshot_object_id == prepared.snapshot_object_id
    assert captured.snapshot_bytes == snapshot.data
    with pytest.raises(TypeError):
        captured.receipt["receipt_id"] = "forged"  # type: ignore[index]
    with pytest.raises(FrozenInstanceError):
        captured.snapshot_bytes = b"changed"  # type: ignore[misc]
    with pytest.raises(TypeError, match="generated MutationResult"):
        _capture_resolved_transcript_publication(
            prepared,
            {"data": dict(mutation), "receipt": mutation.receipt},  # type: ignore[arg-type]
            snapshot_object_id=prepared.snapshot_object_id,
            snapshot_response=snapshot,
        )


def test_external_json_receipt_cannot_construct_resolved_capture():
    prepared = _prepare()
    external_envelope = {
        "prepared": _envelope(prepared),
        "data": {"document_id": prepared.document_id},
        "receipt": {"receipt_id": "external-json"},
        "snapshot_object_id": prepared.snapshot_object_id,
        "snapshot_bytes": prepared.canonical_record_json.encode("utf-8"),
    }

    with pytest.raises(TypeError, match="internal capture"):
        ResolvedTranscriptPublication(**external_envelope)  # type: ignore[arg-type]


def test_capture_refuses_wrong_locator_bytes_or_mutation_content():
    prepared = _prepare()
    content = json.loads(prepared.canonical_record_json)
    mutation = MutationResult(
        {
            "project_id": prepared.project_id,
            "document_id": prepared.document_id,
            "kind": TRANSCRIPT_DOCUMENT_KIND,
            "content": content,
            "version": 1,
        },
        {"receipt_id": "receipt-synthetic", "project_id": prepared.project_id},
    )
    snapshot = ByteResponse(prepared.canonical_record_json.encode("utf-8"), 200, {})

    with pytest.raises(ValueError, match="locator"):
        _capture_resolved_transcript_publication(
            prepared,
            mutation,
            snapshot_object_id="sha256:" + "f" * 64,
            snapshot_response=snapshot,
        )
    with pytest.raises(ValueError, match="content-addressed locator"):
        _capture_resolved_transcript_publication(
            prepared,
            mutation,
            snapshot_object_id=prepared.snapshot_object_id,
            snapshot_response=ByteResponse(b"{}", 200, {}),
        )
    mismatch = MutationResult(
        {**dict(mutation), "content": {}},
        mutation.receipt,
    )
    with pytest.raises(ValueError, match="prepared transcript request"):
        _capture_resolved_transcript_publication(
            prepared,
            mismatch,
            snapshot_object_id=prepared.snapshot_object_id,
            snapshot_response=snapshot,
        )
