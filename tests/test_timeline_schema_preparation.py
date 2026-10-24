from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from test_timeline_schema_resolution import _validators
from test_timeline_validation_cost import _packet

from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import ValidationError


def _errors(validator, value):
    def details(error):
        return (
            error.validator, list(error.path), list(error.schema_path), error.message,
            [details(child) for child in error.context],
        )

    return [details(error) for error in validator.iter_errors(value)]


@pytest.mark.parametrize("dialect", [
    "http://json-schema.org/draft-07/schema#",
    "https://json-schema.org/draft/2020-12/schema",
])
def test_reused_resolution_preserves_dialect_selection_and_nested_error_context(dialect):
    root = "https://example.invalid/root"
    resources = {root: {
        "$id": root,
        "$defs": {"integer": {"type": "integer"}},
        "properties": {"value": {
            "type": "array",
            "contains": {
                "$schema": dialect,
                "$ref": "#/$defs/integer",
                "minimum": 2,
            },
        }, "choices": {
            "type": "array",
            "items": {"oneOf": [
                {"type": "integer", "minimum": 2},
                {"type": "string", "minLength": 2},
            ]},
        }},
    }}
    original, reused = _validators(resources, root)
    for value in ({"value": [2], "choices": [2, "ok"]},
                  {"value": [1]}, {"choices": [False, "x", 1]},
                  {"value": [2], "choices": [2, "ok"]}):
        before = copy.deepcopy(value)
        assert _errors(reused, value) == _errors(original, value)
        assert value == before
    assert bool(_errors(reused, {"value": [1]})) == ("2020-12" in dialect)
    errors = list(reused.iter_errors({"choices": [False]}))
    assert list(errors[0].path) == ["choices", 0]
    assert list(errors[0].schema_path) == ["properties", "choices", "items", "oneOf"]
    assert len(errors[0].context) == 2


def test_reused_resolution_keeps_relative_json_pointer_base_and_escapes():
    root = "https://example.invalid/root"
    resources = {root: {
        "$id": root,
        "$defs": {name: {
            "$id": name + "/",
            "$defs": {"a/b~c": {"type": kind}},
            "$ref": "#/$defs/a~1b~0c",
        } for name, kind in (("integer", "integer"), ("string", "string"))},
        "properties": {
            "integer": {"$ref": "integer/"},
            "string": {"$ref": "string/"},
        },
    }}
    original, reused = _validators(resources, root)
    for value in ({"integer": 1, "string": "ok"},
                  {"integer": "ok", "string": 1},
                  {"integer": True, "string": None},
                  {"integer": 1, "string": "ok"}):
        assert _errors(reused, value) == _errors(original, value)
    assert len(_errors(reused, {"integer": "ok", "string": 1})) == 2


def test_warm_installed_validator_rechecks_independent_concurrent_mutations():
    document = _packet()["capture"]["original"]["commands"][0]["input"]
    before = copy.deepcopy(document)
    validation.validate_commit_value(document, "CanonicalDocument")
    barrier = Barrier(4)

    def check(worker):
        value = copy.deepcopy(document)
        barrier.wait(timeout=10)
        for _ in range(3):
            validation.validate_commit_value(value, "CanonicalDocument")
            if worker % 2:
                value["parent_revision"]["revision_id"] = None
                message = "invalid CanonicalDocument"
            else:
                value["parent_revision"]["payload"]["untyped"] = float("inf")
                message = "finite JSON"
            with pytest.raises(ValidationError, match=message):
                validation.validate_commit_value(value, "CanonicalDocument")
            value = copy.deepcopy(document)
        return value

    with ThreadPoolExecutor(max_workers=4) as pool:
        assert list(pool.map(check, range(4))) == [before] * 4
    assert document == before
