"""Repeated exact source reads reuse validation without sharing provider data."""
from __future__ import annotations

import copy
import sqlite3
from contextlib import closing

import pytest
import test_timeline_commit_port as port_tests
from test_timeline_commit_inputs import _media, _pin, _transcript
from test_timeline_commit_port import (
    PreparedProvider,
    commit,
    prepared,
    request,
    use_provider,
)

from runtime_protocol import timeline_commit_inputs as inputs
from runtime_protocol.errors import AuthorizationError, RuntimeErrorBase
from runtime_protocol.timeline_commit_port import RequestCommitPort
from runtime_protocol.util import canonical_json

service = port_tests.service


def source(service, name="source"):
    return service.create_document(
        service.test_project,
        {"document_id": name, "kind": "producer.config",
         "content": {"schema": "producer.config/v1", "nested": [{"values": [1, 2, 3]}]}},
        idempotency_key=name,
    )["data"]


def body(service, pins):
    return request(service, commands=[{
        "schema_version": 1, "op": "fixture.capture-source", "version": "1", "select": None,
        "args": {"pins": pins}, "created": [],
    }])


def port_for(service, pins, authorize=lambda: None):
    store, _ = service._timeline_commits()
    return RequestCommitPort(service, store, {
        "invocation": {"operation": "commitTimeline"}, "request": body(service, pins),
    }, authorize)


def retain(service, pin):
    def action(context, port):
        port.config_source(pin)
        candidate = prepared(context, port)
        candidate["canonical_document"]["dependency_manifest"]["documents"] = [pin]
        from runtime_protocol.timeline_commit_validation import digest
        candidate["document_digest"] = digest(candidate["canonical_document"])
        candidate["records"]["commands"][0]["dependencies"] = [
            {"key": "config:source", "kind": "source", "pin": pin, "policy": "exact"},
        ]
        return port.accept(candidate)

    use_provider(service, PreparedProvider(action))
    return commit(service, body(service, [pin]), key="retain")


@pytest.mark.parametrize("retained", [False, True])
def test_repeated_source_validates_once_per_exact_pin(service, monkeypatch, retained, record_property):
    resource = source(service)
    pin = _pin(resource)
    if retained:
        retain(service, pin)
    other = source(service, "other")
    other_pin = _pin(other)
    assert pin["content_digest"] == other_pin["content_digest"]
    port = port_for(service, [pin, other_pin])
    if retained:
        port.revision_closure(body(service, [pin])["base_revision_id"])
    finite = inputs.finite_json
    validated_bytes = []

    def counted(value):
        validated_bytes.append(len(canonical_json(value).encode()))
        return finite(value)

    monkeypatch.setattr(inputs, "finite_json", counted)
    try:
        first = port.config_source(pin)
        expected_bytes = canonical_json(first)
        first["document"]["content"]["nested"][0]["values"].append(999)
        first["pin"]["version"] = 999
        second = port.config_source(pin)
        assert canonical_json(second) == expected_bytes
        assert len(validated_bytes) == 1
        assert port.config_source(other_pin)["document"] == other
        assert len(validated_bytes) == 2  # Equal bytes under a new pin are a new capture.
        second["document"]["content"]["nested"].clear()
        assert canonical_json(port.config_source(pin)) == expected_bytes
        assert len(validated_bytes) == 2
        assert service.get_document(service.test_project, resource["document_id"])["content"] == resource["content"]
    finally:
        port.close()
    with pytest.raises(AuthorizationError, match="closed"):
        port.config_source(pin)
    next_port = port_for(service, [pin])
    try:
        if retained:
            next_port.revision_closure(body(service, [pin])["base_revision_id"])
        assert canonical_json(next_port.config_source(pin)) == expected_bytes
        assert len(validated_bytes) == 3
    finally:
        next_port.close()
    record_property("source_validations", len(validated_bytes))
    record_property("validated_bytes", sum(validated_bytes))
    record_property("canonical_bytes", len(expected_bytes.encode()))


@pytest.mark.parametrize("writer", ["same-connection", "external"])
@pytest.mark.parametrize("retained", [False, True])
def test_source_snapshot_rejects_changed_stored_bytes(service, writer, retained):
    resource = source(service)
    pin = _pin(resource)
    if retained:
        retain(service, pin)
    port = port_for(service, [pin])
    try:
        if retained:
            port.revision_closure(body(service, [pin])["base_revision_id"])
        port.config_source(pin)
        query = ("UPDATE timeline_document_input_contents SET content_json='{}' WHERE content_digest=?"
                 if retained else "UPDATE project_documents SET content_json='{}' WHERE id=?")
        parameters = (pin["content_digest"] if retained else pin["document_id"],)
        if writer == "external":
            with closing(sqlite3.connect(service.store.db_path, isolation_level=None)) as connection:
                connection.execute(query, parameters)
        else:
            service.store.conn.execute(query, parameters)
        with pytest.raises(RuntimeErrorBase):
            port.config_source(pin)
    finally:
        port.close()


def test_source_snapshot_reauthorizes_and_discards_on_error(service, monkeypatch):
    resource = source(service)
    pin = _pin(resource)
    allowed = True
    authorizations = 0

    def authorize():
        nonlocal authorizations
        authorizations += 1
        if not allowed:
            raise AuthorizationError("revoked")

    port = port_for(service, [pin], authorize)
    finite = inputs.finite_json
    validations = 0

    def counted(value):
        nonlocal validations
        validations += 1
        return finite(value)

    monkeypatch.setattr(inputs, "finite_json", counted)
    try:
        assert port.config_source(pin)["document"] == resource
        allowed = False
        with pytest.raises(AuthorizationError, match="revoked"):
            port.config_source(pin)
        allowed = True
        assert port.config_source(pin)["document"] == resource
        assert authorizations == 3
        assert validations == 2
    finally:
        port.close()


def test_transcript_snapshot_keeps_schema_and_current_custody_checks(service):
    media = _media(service, service.test_project)
    resource, _ = _transcript(service, service.test_project, media)
    pin = _pin(resource)
    port = port_for(service, [pin])
    try:
        first = port.transcript_source(pin)
        expected = copy.deepcopy(first)
        first["document"]["content"]["segments"][0]["words"].clear()
        assert port.transcript_source(pin) == expected
        with pytest.raises(RuntimeErrorBase):
            port.transcript_source({**pin, "version": True})
        service.store.conn.execute("DELETE FROM project_objects WHERE project_id=? AND digest=?",
                                   (service.test_project, media.removeprefix("sha256:")))
        with pytest.raises(RuntimeErrorBase):
            port.transcript_source(pin)
    finally:
        port.close()


def test_config_snapshot_does_not_grant_transcript_schema_authority(service):
    resource = source(service)
    pin = _pin(resource)
    port = port_for(service, [pin])
    try:
        port.config_source(pin)
        with pytest.raises(RuntimeErrorBase):
            port.transcript_source(pin)
        assert port.config_source(pin)["document"] == resource
    finally:
        port.close()


@pytest.mark.parametrize("writer", ["rollback", "external"])
def test_source_snapshot_revalidates_after_storage_change(service, monkeypatch, writer):
    resource = source(service)
    pin = _pin(resource)
    port = port_for(service, [pin])
    finite = inputs.finite_json
    validations = []

    def counted(value):
        validations.append(canonical_json(value))
        return finite(value)

    monkeypatch.setattr(inputs, "finite_json", counted)
    try:
        expected = port.config_source(pin)
        query = "UPDATE timelines SET name='changed' WHERE id='main'"
        if writer == "rollback":
            service.store.conn.execute("BEGIN")
            service.store.conn.execute(query)
            service.store.conn.rollback()
        else:
            with closing(sqlite3.connect(service.store.db_path, isolation_level=None)) as connection:
                connection.execute(query)
        assert port.config_source(pin) == expected
        assert validations == [canonical_json(resource["content"])] * 2
    finally:
        port.close()
