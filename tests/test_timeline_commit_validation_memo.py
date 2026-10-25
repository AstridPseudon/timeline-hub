from __future__ import annotations

import copy
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from test_timeline_validation_cost import _packet

from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import ValidationError


class _AcceptingValidator:
    def __init__(self, calls):
        self.calls = calls

    def validate(self, value):
        self.calls.append(copy.deepcopy(value))


@pytest.fixture(autouse=True)
def _fresh_memo():
    validation.clear_validation_memo()
    yield
    validation.clear_validation_memo()


def test_exact_success_is_reused_without_retaining_the_value(monkeypatch):
    value = _packet()["capture"]["original"]["commands"][0]["input"]
    calls = []
    monkeypatch.setattr(validation, "_validator", lambda _definition: _AcceptingValidator(calls))

    validation.validate_commit_value(value, "CanonicalDocument")
    validation.validate_commit_value(copy.deepcopy(value), "CanonicalDocument")

    assert len(calls) == 1
    assert all(
        isinstance(key, tuple)
        and len(key) == 3
        and all(isinstance(part, str) for part in key)
        for key in validation._validation_memo
    )


def test_mutation_changes_key_and_invalid_value_is_not_admitted(monkeypatch):
    value = _packet()["capture"]["original"]["commands"][0]["input"]
    calls = []
    original = validation._validator("CanonicalDocument")

    class CountingValidator:
        def validate(self, candidate):
            calls.append(copy.deepcopy(candidate))
            return original.validate(candidate)

    monkeypatch.setattr(validation, "_validator", lambda _definition: CountingValidator())
    validation.validate_commit_value(value, "CanonicalDocument")
    value["unexpected"] = True
    with pytest.raises(ValidationError, match="invalid CanonicalDocument"):
        validation.validate_commit_value(value, "CanonicalDocument")

    assert len(calls) == 2
    assert len(validation._validation_memo) == 1


def test_failures_are_never_cached(monkeypatch):
    value = _packet()["capture"]["original"]["commands"][0]["input"]
    value["unexpected"] = True
    calls = []
    original = validation._validator("CanonicalDocument")

    class CountingValidator:
        def validate(self, candidate):
            calls.append(copy.deepcopy(candidate))
            return original.validate(candidate)

    monkeypatch.setattr(validation, "_validator", lambda _definition: CountingValidator())
    for _ in range(2):
        with pytest.raises(ValidationError, match="invalid CanonicalDocument"):
            validation.validate_commit_value(value, "CanonicalDocument")

    assert len(calls) == 2
    assert not validation._validation_memo


def test_definition_schema_and_python_type_domains_are_separate(monkeypatch):
    calls = []
    monkeypatch.setattr(validation, "_validator", lambda _definition: _AcceptingValidator(calls))

    validation.validate_commit_value({"value": 1}, "definition-a")
    validation.validate_commit_value({"value": 1}, "definition-b")
    validation.validate_commit_value(1, "definition-a")
    validation.validate_commit_value(True, "definition-a")

    assert len(calls) == 4


def test_changed_schema_bundle_digest_does_not_hit_old_success(monkeypatch):
    calls = []
    schema_digest = "schema-a"
    monkeypatch.setattr(validation, "_active_schema_bundle", lambda: ({}, {}, schema_digest))
    monkeypatch.setattr(validation, "_validator", lambda _definition: _AcceptingValidator(calls))

    validation.validate_commit_value({"value": 1}, "definition")
    schema_digest = "schema-b"
    validation.validate_commit_value({"value": 1}, "definition")

    assert len(calls) == 2
    assert len(validation._validation_memo) == 2


def test_memo_is_bounded_and_old_entries_evict(monkeypatch):
    calls = []
    monkeypatch.setattr(validation, "_validator", lambda _definition: _AcceptingValidator(calls))

    for number in range(validation._VALIDATION_MEMO_MAXSIZE + 1):
        validation.validate_commit_value({"number": number}, "definition")
    validation.validate_commit_value({"number": 0}, "definition")

    assert len(validation._validation_memo) == validation._VALIDATION_MEMO_MAXSIZE
    assert len(calls) == validation._VALIDATION_MEMO_MAXSIZE + 2


def test_concurrent_exact_successes_validate_once(monkeypatch):
    calls = 0
    calls_lock = threading.Lock()

    class CountingValidator:
        def validate(self, _candidate):
            nonlocal calls
            with calls_lock:
                calls += 1
            time.sleep(0.001)

    monkeypatch.setattr(validation, "_validator", lambda _definition: CountingValidator())
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: validation.validate_commit_value({"value": 1}, "definition"), range(8)))

    assert calls == 1


def test_mutation_during_validation_is_refused_and_not_cached(monkeypatch):
    class MutatingValidator:
        def validate(self, candidate):
            candidate["value"] = 2

    monkeypatch.setattr(validation, "_validator", lambda _definition: MutatingValidator())

    with pytest.raises(ValidationError, match="changed during validation"):
        validation.validate_commit_value({"value": 1}, "definition")

    assert not validation._validation_memo


def test_clear_memo_restores_restart_lifecycle(monkeypatch):
    calls = []
    monkeypatch.setattr(validation, "_validator", lambda _definition: _AcceptingValidator(calls))

    validation.validate_commit_value({"value": 1}, "definition")
    validation.clear_validation_memo()
    validation.validate_commit_value({"value": 1}, "definition")

    assert len(calls) == 2
    assert len(validation._validation_memo) == 1
