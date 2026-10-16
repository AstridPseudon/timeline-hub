"""Pin B's transcript identity cases to D's joined shared helper."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from astrid.sdk.managed_transcript import (
    TRANSCRIPT_DOCUMENT_KIND,
    transcript_document_id,
    validate_transcript_record,
)

FIXTURE = Path(__file__).parent / "fixtures/transcript_v1/document_identity_cases.json"


def _materialize_record(data: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    record = copy.deepcopy(data["records"][case["record_ref"]])
    for override in case.get("record_overrides", []):
        parts = override["path"].strip("/").split("/")
        target = record
        for part in parts[:-1]:
            target = target[part]
        target[parts[-1]] = override["value"]
    return record


def test_b_transcript_identity_cases_use_the_joined_d_helper() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    helper = data["packet"]["helper"]
    claims = data["packet"]["claims"]

    assert helper["import_path"] == "astrid.sdk.managed_transcript"
    assert helper["call"] == "transcript_document_id(project, subject, source)"
    assert helper["manual_hash_or_codec"] == "forbidden"
    assert helper["status"] == "joined_source_verified"
    assert claims["schema_validation"] == "actual_D_validator_executed_on_joined_source"
    assert claims["document_id_execution"] == "actual_D_helper_executed_on_joined_source"
    assert claims["test_pass"] == "asserted_by_test_transcript_identity_fixture"

    ids: dict[str, str] = {}
    for case in data["key_cases"]:
        record = _materialize_record(data, case)
        validate_transcript_record(record)
        actual = transcript_document_id(
            case["project_namespace"], record["subject"], record["source"]
        )
        assert actual == case["actual_document_id"], case["case_id"]

        logical_key = case["logical_key"]
        assert logical_key["kind"] == TRANSCRIPT_DOCUMENT_KIND
        assert logical_key["project_namespace"] == case["project_namespace"]
        assert logical_key["subject"] == record["subject"]
        assert logical_key["source"] == {
            "producer_id": record["source"]["producer_id"],
            "source_id": record["source"]["source_id"],
        }
        ids[case["case_id"]] = actual

    for case in data["key_cases"]:
        relation = case["expected_relation"]
        if relation == "baseline":
            assert case["case_id"] == "base_r1"
        elif relation.startswith("equal_to:"):
            expected_case_id = relation.removeprefix("equal_to:")
            assert ids[case["case_id"]] == ids[expected_case_id]
        elif relation.startswith("distinct_from:"):
            expected_case_id = relation.removeprefix("distinct_from:")
            assert ids[case["case_id"]] != ids[expected_case_id]
        else:
            raise AssertionError(f"unknown relation {relation!r}")

    assert helper["actual_document_id"] == ids["base_r1"]
