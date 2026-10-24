"""D42: a warm replay must observe changed validation dependencies."""
from __future__ import annotations

import pytest
import test_timeline_history_replay_memo as memo_tests

from runtime_protocol import timeline_commit_auth as auth
from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import ProtocolError

service = memo_tests.service
setup_read = memo_tests.setup_read


def refuse(*args, **kwargs):
    raise ValueError("changed validation dependency refuses this publication")


def test_validate_claims_replacement_refuses_warm_and_cold_history(service, monkeypatch):
    commits, _, calls, read = setup_read(service, monkeypatch)
    expected = read()
    assert read() == expected
    assert len(calls) == 1
    monkeypatch.setattr(auth, "validate_claims", refuse)
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()
    commits._replay_memo.clear()
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()
    assert len(calls) == 3


@pytest.mark.parametrize("helper", [
    "require", "images", "validate_step", "validate_bindings", "step_output",
    "value_equal", "_capture_projection_equal", "location", "normalized", "site", "stored_path",
    "validate_sequential_capture", "_capture_document_images", "_capture_records",
])
def test_related_replay_helper_replacement_refuses(service, monkeypatch, helper):
    _, _, _, read = setup_read(service, monkeypatch, sequential=True)
    read()
    monkeypatch.setattr(auth, helper, refuse)
    for _ in range(2):
        with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
            read()


def test_helper_in_place_code_change_refuses(service, monkeypatch):
    _, _, _, read = setup_read(service, monkeypatch)
    read()
    monkeypatch.setattr(auth.validate_claims, "__code__", refuse.__code__)
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()


@pytest.mark.parametrize("helper", ["finite_json", "validate_commit_value", "_validator"])
def test_schema_helper_replacement_refuses(service, monkeypatch, helper):
    _, _, _, read = setup_read(service, monkeypatch, sequential=True)
    read()
    monkeypatch.setattr(validation, helper, refuse)
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()


def test_cached_schema_validator_method_replacement_refuses(service, monkeypatch):
    _, _, _, read = setup_read(service, monkeypatch, sequential=True)
    read()
    monkeypatch.setattr(type(validation._validator("CommitContext")), "validate", refuse)
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()


def test_schema_keyword_in_place_code_change_refuses(service, monkeypatch):
    _, _, _, read = setup_read(service, monkeypatch, sequential=True)
    read()
    checker = type(validation._validator("CommitContext")).VALIDATORS["type"]
    monkeypatch.setattr(checker, "__code__", refuse.__code__)
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()


def test_recursive_equality_global_replacement_refuses(service, monkeypatch):
    from runtime_protocol import timeline_commit_producer as producer

    _, _, _, read = setup_read(service, monkeypatch)
    read()
    monkeypatch.setattr(producer, "value_equal", refuse)
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()


def test_helper_defaults_change_reverifies(service, monkeypatch):
    _, _, calls, read = setup_read(service, monkeypatch)
    expected = read()
    monkeypatch.setattr(auth.site, "__defaults__", ({},))
    assert read() == expected
    assert len(calls) == 2
    assert read() == expected
    assert len(calls) == 2


def test_referenced_schema_in_place_mutation_refuses(service, monkeypatch):
    _, _, _, read = setup_read(service, monkeypatch, sequential=True)
    read()
    _, registry = validation._schema_resources()
    for resource in registry.values():
        definition = resource.contents.get("$defs", {}).get("CanonicalDocument")
        if definition is not None:
            monkeypatch.setitem(definition, "not", {})
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()


def test_stateful_callable_dependency_is_reverified(service, monkeypatch):
    _, _, calls, read = setup_read(service, monkeypatch)
    original = auth.validate_claims

    class Claims:
        allowed = True

        def __call__(self, *args, **kwargs):
            if not self.allowed:
                refuse()
            return original(*args, **kwargs)

    claims = Claims()
    monkeypatch.setattr(auth, "validate_claims", claims)
    read()
    read()
    assert len(calls) == 2
    claims.allowed = False
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        read()
