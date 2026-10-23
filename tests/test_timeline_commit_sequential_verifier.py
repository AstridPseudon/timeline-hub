"""Request-private original/landing execution carrier checks."""
from __future__ import annotations

import copy

import pytest
import test_timeline_commit_authentication as auth

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.timeline_commit_validation import digest

service = auth.service


def _capture(context, port, prepared):
    request = context["request"]
    base = port.revision_closure(request["base_revision_id"])
    head = prepared["expected_head"]
    current = port.revision_closure(head["revision_id"])
    output = prepared["canonical_document"]
    boundary = {
        "base_revision_id": request["base_revision_id"],
        "base_publication_id": request["base_publication_id"],
        "evaluated_head": head,
        "step_id": prepared["records"]["steps"][0]["id"],
        "command_ordinal": 0,
        "phase": "input",
    }
    execution = {
        "evaluated_head": head,
        "commands": [{"boundary": boundary, "input": current, "output": output}],
        "records": copy.deepcopy(prepared["records"]),
    }
    original = copy.deepcopy(execution)
    original["evaluated_head"] = {
        "revision_id": request["base_revision_id"],
        "publication_id": request["base_publication_id"],
    }
    original["commands"][0]["boundary"]["evaluated_head"] = original["evaluated_head"]
    original["commands"][0]["input"] = base
    return {
        "schema_version": 1,
        "context": copy.deepcopy(context),
        "original": original,
        "landing": execution,
        "replay_bindings": [],
        "prepared_digest": digest(prepared),
    }


def _provider_with_capture(service, mutate=None):
    def execute(context, port):
        prepared = auth.candidate(context, port)
        capture = _capture(context, port, prepared)
        if mutate is not None:
            mutate(capture, prepared)
        port.capture_sequential_execution(capture)
        return port.accept(prepared)

    service.test_provider.action = execute


def test_private_sequential_carrier_accepts_authenticated_candidate(service):
    _provider_with_capture(service)
    result = auth.commit(service, auth.body(service), key="sequential-private-positive")
    assert result["data"]["status"] == "accepted"


def test_private_sequential_carrier_rejects_context_tampering_without_write(service):
    def mutate(capture, _prepared):
        capture["context"]["idempotency_key"] = "other-request"

    _provider_with_capture(service, mutate)
    before = auth.rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        auth.commit(service, auth.body(service), key="sequential-private-context")
    assert error.value.details is not None
    assert error.value.details["reason"] == "invocation_mismatch"
    assert auth.rows(service) == before


def test_private_sequential_carrier_rejects_prepared_digest_and_boundary_tampering(service):
    def mutate(capture, prepared):
        if prepared["records"]["label"] == "digest":
            capture["prepared_digest"] = digest({"forged": True})
        else:
            capture["landing"]["commands"][0]["input"] = copy.deepcopy(capture["original"]["commands"][0]["input"])
            capture["landing"]["commands"][0]["input"]["parent_revision"]["content_digest"] = "sha256:" + "0" * 64

    for damage in ("digest", "input"):
        request = auth.body(service)
        request["label"] = damage
        _provider_with_capture(service, mutate)
        before = auth.rows(service)
        with pytest.raises(RuntimeErrorBase) as error:
            auth.commit(service, request, key="sequential-private-" + damage)
        assert error.value.details is not None
        assert error.value.details["reason"] == "invalid_records"
        assert auth.rows(service) == before


def test_private_sequential_carrier_rejects_boolean_command_ordinal(service):
    def mutate(capture, _prepared):
        capture["landing"]["commands"][0]["boundary"]["command_ordinal"] = True

    _provider_with_capture(service, mutate)
    before = auth.rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        auth.commit(service, auth.body(service), key="sequential-private-bool-ordinal")
    assert error.value.details is not None
    assert error.value.details["reason"] == "invalid_records"
    assert auth.rows(service) == before


def test_private_sequential_carrier_is_one_attempt_and_does_not_extend_history(service):
    def execute(context, port):
        prepared = auth.candidate(context, port)
        capture = _capture(context, port, prepared)
        port.capture_sequential_execution(capture)
        prepared["records"]["label"] = "forged-after-capture"
        return port.accept(prepared)

    service.test_provider.action = execute
    before = auth.rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        auth.commit(service, auth.body(service), key="sequential-private-attempt")
    assert error.value.details is not None
    assert error.value.details["reason"] == "invalid_records"
    assert auth.rows(service) == before


def test_moved_head_staged_alias_without_private_proof_fails_closed(service):
    def execute(context, port):
        prepared = auth.candidate(context, port)
        binding = prepared["records"]["commands"][0]["bindings"][0]
        binding["ref"] = "internal-revision:staged-unlanded"
        binding["physical_ref"] = "internal-revision:staged-unlanded"
        return port.accept(prepared)

    service.test_provider.action = execute
    before = auth.rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        auth.commit(service, auth.body(service), key="sequential-private-missing")
    assert error.value.details is not None
    assert error.value.details["reason"] == "sequential_proof_unavailable"
    assert auth.rows(service) == before
