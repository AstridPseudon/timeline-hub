"""Adversarial reads through the real settled-producer request port."""
from __future__ import annotations

import base64
import copy

import pytest
from test_timeline_producer_guards import (
    _assert_refused,
    _body,
    _candidate,
    _context,
    _digest,
    _execute,
    _settle,
    _state,
)
from test_timeline_producer_guards import (
    producer as producer,  # noqa: PLC0414 - expose the shared pytest fixture
)

from runtime_protocol.errors import ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_port import RequestCommitPort


@pytest.mark.parametrize("field,value", [
    ("task_id", ""), ("attempt_id", None), ("executor_id", " "),
    ("fence", True), ("fence", 1.0), ("fence", 0),
    ("runtime_epoch", False), ("runtime_epoch", -1), ("runtime_epoch", 1.5),
    ("proposal_digest", "sha256:" + "A" * 64), ("proposal_digest", "0" * 64),
    ("lease_id", "secret"), ("task_id", "\ud800"),
])
def test_malformed_pin_refuses_422_without_reads_or_writes(producer, field, value):
    pin = copy.deepcopy(producer.pin)
    pin[field] = value
    commits, _ = producer.service._timeline_commits()
    port = RequestCommitPort(producer.service, commits, _context(producer), lambda: None)
    try:
        before = _state(producer.service)
        with pytest.raises(ValidationError) as error:
            port.producer_attempt(pin)
        assert error.value.status == 422
        assert _state(producer.service) == before
    finally:
        port.close()


@pytest.mark.parametrize("raw", [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}',
    b'{"a":1e999}', b'{"a":"\\ud800"}', b'{"\\udfff":1}', b'\xff', b'{} trailing'])
def test_strict_settled_json_rejects_invalid_original_bytes(producer, raw):
    attempt = producer.attempt
    producer.service.settle_attempt(attempt["attempt_id"], {
        **{key: attempt[key] for key in ("lease_id", "fence", "runtime_epoch")},
        "outputs": [{"name": "authoring_proposal", "output_port": "authoring_proposal", "kind": "object",
            "filename": "proposal.json", "digest": _digest(raw), "size": len(raw), "media_type": "application/json",
            "durability": "durable", "data_base64": base64.b64encode(raw).decode()}],
    }, idempotency_key="settle-invalid-proposal")
    _assert_refused(producer.service, lambda: _execute(producer), {"producer_dependency_unavailable"})


@pytest.mark.parametrize("damage", ["copy", "nested", "second", "inverse", "restore"])
def test_guard_requires_first_pin_only_and_no_other_authority_commands(producer, damage):
    _settle(producer)
    body = _body(producer)
    if damage == "copy":
        body["commands"][0]["args"]["proposal"] = copy.deepcopy(producer.proposal)
    elif damage == "nested":
        body["commands"] = [{"op": "timeline.batch", "args": {"commands": body["commands"]}}]
    elif damage == "second":
        body["commands"].append(copy.deepcopy(body["commands"][0]))
    else:
        body["commands"][1]["op"] = "timeline." + damage
    service = producer.service
    commits, _ = service._timeline_commits()
    port = RequestCommitPort(service, commits, _context(producer, body), lambda: None)
    try:
        _assert_refused(service, lambda: port.producer_attempt(producer.pin),
                        {"producer_dependency_unavailable", "producer_attempt_mismatch"})
    finally:
        port.close()


def test_unconsumed_completed_proposal_survives_runtime_restart(producer):
    _settle(producer)
    producer.service.close()
    producer.service = RuntimeService(producer.root)
    assert producer.service.health()["runtime_epoch"] > producer.pin["runtime_epoch"]
    assert _execute(producer)["data"]["status"] == "accepted"


def test_private_accessor_is_detached_and_record_boolean_cannot_forge_fence(producer):
    _settle(producer)
    service = producer.service
    commits, _ = service._timeline_commits()
    context = _context(producer)
    port = RequestCommitPort(service, commits, context, lambda: None)
    try:
        port.producer_attempt(producer.pin)
        candidate = _candidate(context, port, producer.pin)
        before = _state(service)
        captures = port._producer_captures(candidate)
        capture, = captures
        assert capture["proposal"] == producer.proposal
        assert capture["identity"]["request_hash"] == context["request_hash"]
        capture["pin"]["fence"] += 10
        assert port._producer_captures(candidate)[0]["pin"] == producer.pin
        assert _state(service) == before
        candidate["records"]["commands"][0]["dependencies"][0]["pin"]["fence"] = True
        _assert_refused(service, lambda: port._producer_captures(candidate), {"producer_dependency_unavailable"})
    finally:
        port.close()


def test_selected_child_lifecycle_change_after_capture_refuses(producer):
    _settle(producer)
    service = producer.service
    commits, _ = service._timeline_commits()
    context = _context(producer)
    port = RequestCommitPort(service, commits, context, lambda: None)
    try:
        port.producer_attempt(producer.pin)
        candidate = _candidate(context, port, producer.pin)
        child = producer.spec["runtime_dependencies"]["resolved_children"][0]["task_id"]
        association, = service.managed_outputs(child)
        service.update_managed_output_lifecycle(association["association_id"],
            {"operation": "promote", "expected_version": association["lifecycle"]["version"]},
            idempotency_key="promote-child")
        _assert_refused(service, lambda: port._producer_captures(candidate), {"producer_attempt_mismatch"})
    finally:
        port.close()
