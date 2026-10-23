"""Request-private original/landing execution carrier checks."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import test_timeline_commit_authentication as auth

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.timeline_commit import CommitRejected, StaleHead
from runtime_protocol.timeline_commit_auth import validate, validate_sequential_capture
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


@pytest.fixture
def captured_sequence():
    # Actual Agent 1403 capture-1-0 from retained packet SHA-256 59e329b65a9b83c3.
    # Transport evidence only: this fixture does not qualify a production join.
    return json.loads((Path(__file__).parent / "fixtures/timeline_sequential_capture.json").read_text())


def _verify_packet(packet):
    continuations = {}
    entries = {entry["publication_id"]: entry for entry in packet["history"]["items"]}
    cursor = packet["history"]["head"]
    while cursor["publication_id"] != packet["request"]["base_publication_id"]:
        entry = entries[cursor["publication_id"]]
        for record in (entry["records"] or {}).get("commands", []):
            for binding in record["bindings"]:
                if binding.get("key") == "commit.materialization":
                    continuations.setdefault(binding["physical_ref"], set()).add(binding["successor"])
        cursor = entry["previous"]
    proof = validate_sequential_capture(packet["request"], packet["prepared"], packet["capture"],
                                        packet["head_document"], packet["source"], continuations)
    validate(packet["request"], packet["prepared"], packet["head_document"], packet["source"],
             continuations, sequential=proof)


def test_retained_real_capture_runs_both_verification_stages(captured_sequence):
    before = copy.deepcopy(captured_sequence)
    _verify_packet(captured_sequence)
    assert captured_sequence == before


@pytest.mark.parametrize("damage", ["omitted", "duplicate", "future", "owner", "terminal",
                                   "bool", "negative", "past_end", "malformed"])
def test_retained_real_capture_rejects_replay_forgery(captured_sequence, damage):
    replay = captured_sequence["capture"]["replay_bindings"]
    entry = replay[-1]
    if damage == "omitted":
        replay.pop()
    elif damage == "duplicate":
        replay.append(copy.deepcopy(entry))
    elif damage == "future":
        entry["source"]["step_id"] = "second"
    elif damage == "owner":
        entry["source"].update(owner="occurrence:foreign/shot", owners=["occurrence:foreign/shot"])
    elif damage == "terminal":
        entry["source"]["source"] = "internal-revision:foreign"
    elif damage == "malformed":
        entry["source"]["owners"] = {"owner": True}
    else:
        entry["command_ordinal"] = {"bool": True, "negative": -1, "past_end": 2}[damage]
    with pytest.raises(CommitRejected):
        _verify_packet(captured_sequence)


@pytest.mark.parametrize("side", ["original", "landing"])
@pytest.mark.parametrize("damage", ["record", "snapshot", "source"])
def test_coordinated_capture_record_map_and_digest_forgery(captured_sequence, side, damage):
    capture = captured_sequence["capture"]
    execution = capture[side]
    if damage == "record":
        # Keep both public recorder copies and the envelope digest in agreement.
        for record in execution["records"]["commands"]:
            for binding in record["bindings"]:
                if binding.get("key") == "commit.materialization":
                    binding["edge_before"] = "shot-revision:foreign"
        if side == "landing":
            captured_sequence["prepared"]["records"] = copy.deepcopy(execution["records"])
    elif damage == "snapshot":
        # Matching adjacent snapshots with freshly computed hashes cannot invent
        # an earlier command result. The actual submitted nudge is still 4.0.
        for document in (execution["commands"][0]["output"], execution["commands"][1]["input"]):
            image = document["internal_timeline_revisions"][0]
            next(row for row in image["payload"]["clips"] if row["id"] == "cross")["at"] = 9.0
            image["content_digest"] = digest(image["payload"])
        for binding in execution["records"]["commands"][1]["bindings"]:
            if binding.get("physical_ref", "").startswith("internal-revision:"):
                binding["content_digest"] = execution["commands"][1]["input"]["internal_timeline_revisions"][0]["content_digest"]
        if side == "landing":
            captured_sequence["prepared"]["records"] = copy.deepcopy(execution["records"])
    else:
        # A coordinated source/map rewrite must still originate at the captured
        # authenticated BASE or HEAD, even when every carrier agrees with it.
        image = execution["commands"][0]["input"]["internal_timeline_revisions"][0]
        old = image["revision_id"]
        encoded = json.dumps(execution).replace(old, "forged-internal")
        execution.update(json.loads(encoded))
        for entry in capture["replay_bindings"]:
            entry["source"] = json.loads(json.dumps(entry["source"]).replace(old, "forged-internal"))
        if side == "landing":
            captured_sequence["prepared"]["records"] = copy.deepcopy(execution["records"])
    capture["prepared_digest"] = digest(captured_sequence["prepared"])
    with pytest.raises(CommitRejected):
        _verify_packet(captured_sequence)


@pytest.mark.parametrize("damage", ["schema_bool", "binding_bool", "effect_bool", "effect_float", "missing_record_field",
                                   "bad_image", "bad_binding"])
def test_private_capture_malformed_json_has_a_structured_refusal(service, damage):
    def mutate(capture, prepared):
        if damage == "schema_bool":
            capture["schema_version"] = True
        elif damage == "binding_bool":
            capture["original"]["records"]["commands"][0]["bindings"][0]["boundary"]["command_ordinal"] = False
        elif damage in {"effect_bool", "effect_float"}:
            capture["original"]["records"]["commands"][0]["bindings"][0]["effect_ordinal"] = True if damage == "effect_bool" else 0.0
        elif damage == "missing_record_field":
            capture["original"]["records"]["commands"][0].pop("writes")
        elif damage == "bad_image":
            capture["original"]["commands"][0]["input"]["shot_revisions"] = [None]
        else:
            capture["original"]["records"]["commands"][0]["bindings"] = [None]

    _provider_with_capture(service, mutate)
    before = auth.rows(service)
    with pytest.raises(RuntimeErrorBase) as error:
        auth.commit(service, auth.body(service), key="malformed-sequential-" + damage)
    assert error.value.status < 500
    assert auth.rows(service) == before


@pytest.mark.parametrize("kind", ["read", "patch", "change"])
@pytest.mark.parametrize("ordinal", [-1, 2, True])
def test_real_capture_rejects_all_replay_ordinal_ranges(captured_sequence, kind, ordinal):
    entry = next(entry for entry in captured_sequence["capture"]["replay_bindings"]
                 if entry["kind"] == ("patch" if kind == "change" else kind))
    entry["change_ordinal" if kind == "change" else "command_ordinal"] = ordinal
    with pytest.raises(CommitRejected):
        _verify_packet(captured_sequence)


@pytest.mark.parametrize("damage", ["nested_self", "unconsumed_original", "missing_landing"])
def test_real_capture_requires_complete_ordered_correspondence(captured_sequence, damage):
    capture = captured_sequence["capture"]
    if damage == "nested_self":
        node = capture["replay_bindings"][-1]["source"]
        node["source"] = copy.deepcopy(node)
    elif damage == "unconsumed_original":
        bindings = capture["original"]["records"]["commands"][1]["bindings"]
        bindings.append(copy.deepcopy(bindings[0]))
    else:
        capture["landing"]["records"]["commands"][1]["bindings"].pop(0)
        captured_sequence["prepared"]["records"] = copy.deepcopy(capture["landing"]["records"])
        capture["prepared_digest"] = digest(captured_sequence["prepared"])
    with pytest.raises(CommitRejected):
        _verify_packet(captured_sequence)


def test_private_capture_detaches_and_consumes_on_validation_failure(service):
    def execute(context, port):
        prepared = auth.candidate(context, port)
        capture = _capture(context, port, prepared)
        port.capture_sequential_execution(capture)
        capture["prepared_digest"] = "sha256:" + "0" * 64
        source = port.revision_closure(prepared["expected_head"]["revision_id"])
        proof = port._validate_sequential_execution(prepared, source, source, {}, None)
        assert proof is not None
        assert port._validate_sequential_execution(prepared, source, source, {}, None) is None
        port.capture_sequential_execution(capture)
        with pytest.raises(CommitRejected):
            port._validate_sequential_execution(prepared, source, source, {}, None)
        assert port._validate_sequential_execution(prepared, source, source, {}, None) is None
        return port.accept(prepared)

    service.test_provider.action = execute
    result = auth.commit(service, auth.body(service), key="sequential-detached-consumed")
    assert result["data"]["status"] == "accepted"


@pytest.mark.parametrize("failure", ["invalid", "cas"])
def test_private_capture_is_discarded_before_a_later_accept_attempt(service, monkeypatch, failure):
    def execute(context, port):
        prepared = auth.candidate(context, port)
        port.capture_sequential_execution(_capture(context, port, prepared))
        source = port.revision_closure(prepared["expected_head"]["revision_id"])
        if failure == "invalid":
            with pytest.raises(CommitRejected):
                port.accept({**prepared, "document_digest": "sha256:" + "0" * 64})
        else:
            store = port._RequestCommitPort__store
            accept = store.accept

            def stale(*_args, **_kwargs):
                raise StaleHead(prepared["expected_head"])

            with monkeypatch.context() as patch:
                patch.setattr(store, "accept", stale)
                with pytest.raises(StaleHead):
                    port.accept(prepared)
            assert store.accept == accept
        assert port._validate_sequential_execution(prepared, source, source, {}, None) is None
        return port.accept(prepared)

    service.test_provider.action = execute
    result = auth.commit(service, auth.body(service), key="sequential-attempt-" + failure)
    assert result["data"]["status"] == "accepted"
