from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from referencing.exceptions import Unresolvable

from runtime_protocol import timeline_commit_auth as auth
from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import ValidationError

FIXTURE = Path(__file__).parent / "fixtures/timeline_sequential_capture.json"


def _packet():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_retained_capture_boundaries_call_the_shared_validator_once_each(monkeypatch):
    packet = _packet()
    boundaries = [
        document
        for side in ("original", "landing")
        for command in packet["capture"][side]["commands"]
        for document in (command["input"], command["output"])
    ]
    original_validator = validation._validator("CanonicalDocument")
    calls = []

    class CountingValidator:
        def validate(self, value):
            calls.append(value)
            return original_validator.validate(value)

    monkeypatch.setattr(validation, "_validator", lambda _definition: CountingValidator())
    for document in boundaries:
        auth._capture_document_images(copy.deepcopy(document))

    assert len(calls) == len(boundaries)
    assert len(boundaries) == 8


def test_validation_does_not_reuse_a_previous_result_after_mutation(monkeypatch):
    packet = _packet()
    value = copy.deepcopy(packet["capture"]["original"]["commands"][0]["input"])
    original_validator = validation._validator("CanonicalDocument")
    calls = 0

    class CountingValidator:
        def validate(self, candidate):
            nonlocal calls
            calls += 1
            return original_validator.validate(candidate)

    monkeypatch.setattr(validation, "_validator", lambda _definition: CountingValidator())
    validation.validate_commit_value(value, "CanonicalDocument")
    value["unexpected"] = True
    with pytest.raises(ValidationError, match="invalid CanonicalDocument"):
        validation.validate_commit_value(value, "CanonicalDocument")

    assert calls == 2


def test_validation_preserves_finite_nested_and_reference_refusals():
    packet = _packet()
    value = copy.deepcopy(packet["capture"]["original"]["commands"][0]["input"])
    value["parent_revision"]["revision_id"] = None
    with pytest.raises(ValidationError, match="invalid CanonicalDocument"):
        validation.validate_commit_value(value, "CanonicalDocument")

    value = copy.deepcopy(packet["capture"]["original"]["commands"][0]["input"])
    value["parent_revision"]["payload"]["nested"] = float("nan")
    with pytest.raises(ValidationError, match="finite JSON"):
        validation.validate_commit_value(value, "CanonicalDocument")

    _, registry = validation._schema_resources()
    with pytest.raises(Unresolvable):
        registry.resolver().lookup("https://example.invalid/schema.json")
    with pytest.raises(ValidationError, match="unknown commit schema"):
        validation.validate_commit_value({}, "https://example.invalid/schema.json")
