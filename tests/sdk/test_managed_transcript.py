from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.managed_transcript import (
    TRANSCRIPT_DOCUMENT_KIND,
    TranscriptValidationError,
    canonical_transcript_json,
    transcript_document_id,
    validate_transcript_record,
)


def _record() -> dict:
    return {
        "schema_version": 1,
        "subject": {
            "media_object_id": "media-object-01",
            "media_sha256": "a" * 64,
        },
        "source": {
            "producer_id": "fixture.transcriber",
            "source_id": "transcript.main",
            "lineage_id": "lineage-1",
            "revision_id": "revision-1",
            "producer_digest": "b" * 64,
        },
        "clock": {"kind": "media", "unit": "seconds", "origin_seconds": 0},
        "words": [
            {"id": "word-a", "text": "Hello", "start_s": 0.1, "end_s": 0.4},
            {"id": "word-b", "text": "world", "start_s": 0.5, "end_s": 0.9},
        ],
        "segments": [{"id": "segment-a", "word_ids": ["word-a", "word-b"]}],
        "metadata": {"engine": "fixture", "opaque": {"confidence": [0.8, None]}},
        "provenance": {"import": {"unit": "milliseconds", "original": [100, 400]}},
    }


def test_valid_record_has_canonical_serialization_and_preserves_opaque_fields() -> None:
    record = _record()
    validated = validate_transcript_record(record, media_duration_s=1.0)

    assert validated == record
    assert validated is not record
    assert validated["metadata"] == record["metadata"]
    assert validated["metadata"] is not record["metadata"]
    assert validated["provenance"] == record["provenance"]

    reordered = dict(reversed(list(record.items())))
    assert canonical_transcript_json(reordered) == canonical_transcript_json(record)
    assert json.loads(canonical_transcript_json(record)) == record


def test_empty_transcript_is_valid_without_segments() -> None:
    record = _record()
    record["words"] = []
    record["segments"] = []

    assert validate_transcript_record(record)["words"] == []


@pytest.mark.parametrize(
    "mutate",
    [
        lambda row: row.pop("subject"),
        lambda row: row["subject"].pop("media_sha256"),
        lambda row: row.update(schema_version=True),
        lambda row: row["source"].pop("producer_digest"),
        lambda row: row["clock"].update(unit="frames"),
        lambda row: row["words"][0].update(start_s=0.6),
        lambda row: row["words"][1].update(id="word-a"),
        lambda row: row["segments"][0].update(word_ids=["word-b"]),
        lambda row: row["segments"][0].update(word_ids=["word-a", "missing"]),
        lambda row: row["metadata"].update(opaque=object()),
        lambda row: row["words"][0].update(start_s=float("nan")),
    ],
)
def test_malformed_v1_records_are_refused(mutate) -> None:
    record = _record()
    mutate(record)

    with pytest.raises(TranscriptValidationError):
        validate_transcript_record(record)


def test_media_interval_is_checked_against_admitted_extent() -> None:
    with pytest.raises(TranscriptValidationError, match="media duration"):
        validate_transcript_record(_record(), media_duration_s=0.8)

    with pytest.raises(TranscriptValidationError, match="finite and non-negative"):
        validate_transcript_record(_record(), media_duration_s=-1)


def test_transcript_document_id_golden_key_and_stable_revision_behavior() -> None:
    record = _record()
    expected_id = "document:f0433b93-7d84-5eed-a7d7-f26ebc7a39fb"
    actual_id = transcript_document_id("project-demo", record["subject"], record["source"])
    assert actual_id == expected_id

    revised = copy.deepcopy(record)
    revised["source"].update(
        revision_id="revision-2",
        parent_revision_id="revision-1",
        producer_digest="c" * 64,
    )
    revised["words"][0].update(text="Hi", end_s=0.3)
    revised["segments"] = [
        {"id": "segment-a", "word_ids": ["word-a"]},
        {"id": "segment-b", "word_ids": ["word-b"]},
    ]
    assert validate_transcript_record(revised)["source"]["parent_revision_id"] == "revision-1"
    assert transcript_document_id("project-demo", revised["subject"], revised["source"]) == expected_id
    occurrence_source = {**revised["source"], "occurrence_id": "clip-occurrence-2"}
    assert transcript_document_id("project-demo", revised["subject"], occurrence_source) == expected_id

    prefixed_subject = {**record["subject"], "media_sha256": "sha256:" + "a" * 64}
    assert transcript_document_id("project-demo", prefixed_subject, record["source"]) == expected_id
    assert TRANSCRIPT_DOCUMENT_KIND == "media.transcript/v1"


@pytest.mark.parametrize(
    ("project", "subject_change", "source_change"),
    [
        ("project-other", {}, {}),
        ("project-demo", {"media_object_id": "media-object-02"}, {}),
        ("project-demo", {"media_sha256": "d" * 64}, {}),
        ("project-demo", {}, {"producer_id": "fixture.other"}),
        ("project-demo", {}, {"source_id": "transcript.alt"}),
    ],
)
def test_document_id_changes_for_each_logical_identity_component(
    project: str,
    subject_change: dict,
    source_change: dict,
) -> None:
    record = _record()
    subject = {**record["subject"], **subject_change}
    source = {**record["source"], **source_change}

    assert transcript_document_id(project, subject, source) != transcript_document_id(
        "project-demo", record["subject"], record["source"]
    )
