"""D42: stable implementation identities do not freeze validator state."""
from __future__ import annotations

from types import FunctionType

import pytest
import test_timeline_history_replay_memo as memo_tests
from test_timeline_commit_port import rows

from runtime_protocol import timeline_commit_auth as auth
from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import ProtocolError

service = memo_tests.service

# Supplied by each FunctionType's private globals, rather than closure cells.
gate = delegate = check_gate = None


def test_active_resolver_replacement_refuses_warm_history(service, monkeypatch):
    from referencing import Registry

    commits, _, calls, read = memo_tests.setup_read(service, monkeypatch, sequential=True)
    expected = read()
    assert read() == expected
    assert len(calls) == 2
    validator = validation._validator("CommitContext")
    monkeypatch.setattr(validator, "_resolver", Registry().resolver())
    assert_warm_and_cold_refuse(commits, read, service)


@pytest.mark.parametrize("dependency", ["class", "callable"])
def test_direct_global_dependency_refuses_warm_history(service, monkeypatch, dependency):
    commits, _, calls, read = memo_tests.setup_read(service, monkeypatch)
    original = auth.validate_claims

    class Gate:
        allowed = True

    state = {"allowed": True}

    def check():
        if not state["allowed"]:
            raise ValueError("changed global callable refuses this publication")

    if dependency == "class":
        def template(*args, **kwargs):
            if not gate.allowed:
                raise ValueError("changed global class refuses this publication")
            return delegate(*args, **kwargs)

        claims = FunctionType(template.__code__, {"gate": Gate, "delegate": original})
    else:
        def template(*args, **kwargs):
            check_gate()
            return delegate(*args, **kwargs)

        claims = FunctionType(template.__code__, {"check_gate": check, "delegate": original})
    monkeypatch.setattr(auth, "validate_claims", claims)
    expected = read()
    assert read() == expected
    assert len(calls) == 1
    if dependency == "class":
        Gate.allowed = False
    else:
        state["allowed"] = False
    assert_warm_and_cold_refuse(commits, read, service)


def assert_warm_and_cold_refuse(commits, read, service):
    before = rows(service)
    try:
        with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
            read()
    finally:
        assert rows(service) == before
        commits._replay_memo.clear()
        with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
            read()
        assert rows(service) == before


def test_same_function_closure_mutation_refuses_warm_history(service, monkeypatch):
    commits, _, calls, read = memo_tests.setup_read(service, monkeypatch)
    original = auth.validate_claims
    state = {"allowed": True}

    def claims(*args, **kwargs):
        if not state["allowed"]:
            raise ValueError("changed closure refuses this publication")
        return original(*args, **kwargs)

    monkeypatch.setattr(auth, "validate_claims", claims)
    expected = read()
    code, defaults = claims.__code__, claims.__defaults__
    assert read() == expected
    assert len(calls) == 1
    state["allowed"] = False
    assert auth.validate_claims is claims
    assert claims.__code__ is code and claims.__defaults__ is defaults
    assert_warm_and_cold_refuse(commits, read, service)


@pytest.mark.parametrize("dependency", ["default", "closure", "nested_callable", "class", "global"])
def test_same_function_mutable_dependency_refuses_warm_history(service, monkeypatch, dependency):
    commits, _, _, read = memo_tests.setup_read(service, monkeypatch)
    original = auth.validate_claims

    class Gate:
        allowed = True

        def __call__(self):
            if not self.allowed:
                raise ValueError("changed dependency refuses this publication")

    gate = Gate()
    if dependency == "default":
        def claims(*args, gate=gate, **kwargs):
            gate()
            return original(*args, **kwargs)
    elif dependency == "closure":
        def claims(*args, **kwargs):
            if not gate.allowed:
                raise ValueError("changed dependency refuses this publication")
            return original(*args, **kwargs)
    elif dependency == "nested_callable":
        def claims(*args, **kwargs):
            gate()
            return original(*args, **kwargs)
    elif dependency == "class":
        def claims(*args, **kwargs):
            if not Gate.allowed:
                raise ValueError("changed dependency refuses this publication")
            return original(*args, **kwargs)
    else:
        def template(*args, **kwargs):
            if not globals()["state"].allowed:
                raise ValueError("changed dependency refuses this publication")
            return globals()["delegate"](*args, **kwargs)

        claims = FunctionType(template.__code__, {"state": gate, "delegate": original})
    monkeypatch.setattr(auth, "validate_claims", claims)
    read()
    if dependency == "class":
        Gate.allowed = False
    else:
        gate.allowed = False
    assert_warm_and_cold_refuse(commits, read, service)
