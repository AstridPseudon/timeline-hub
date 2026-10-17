"""Authenticated pending cleanup is deliberately separate from preparation authority.

Profile and peer observations are controlled at their existing boundary in these
unit tests. Native hosted descriptor/custody controls live in test_hosted_contract.
"""
import copy
import json
import os
import socket
import threading
from pathlib import Path
from types import SimpleNamespace
import pytest
from astrid.core.execution import generic_host as host
from astrid.core.execution import hosted_contract as contract
from astrid.core.execution import custody_broker as custody


@pytest.fixture
def pending(tmp_path, monkeypatch):
    owner = dict(pid=123, uid=os.getuid(), birth_id="owner", runtime_instance_id="epoch", coordinator_epoch="epoch")
    profile = dict(execution_mode="host_only_cpu", profile_digest="sha256:" + "1" * 64)
    request = dict(version=host._LOCAL_PREPARATION_VERSION, command="prepare_local_execution", operation_id="op", channel_id="ch",
        owner_epoch="epoch", runtime_owner=owner, profile=profile, custody_scope=str(tmp_path))
    preparation = host.LocalExecutionPreparation(operation_id="op", channel_id="ch")
    preparation._retained_relay_actor = SimpleNamespace(verify=lambda: owner)
    preparation._hosted_binding = dict(operation_id="op", channel_id="ch", owner_epoch="epoch", profile_digest=contract.digest(contract.canonical(profile)), scope=str(tmp_path), generation=1)
    reference = dict(generation=1, target=dict(pid=os.getpid(), birth_id=host.process_birth_identity()))
    class Authority:
        def __init__(self, *args): pass
        def reference(self): return reference
        def verify_reference(self, ref, **kw):
            assert ref == reference
            if kw != dict(expected_actor=owner, owner_epoch="epoch"): raise contract.HostedContractError("foreign actor")
    monkeypatch.setattr(custody, "RoleCustodyAuthority", Authority)
    abort = dict(version=request["version"], command="abort_local_execution", operation_id="op", channel_id="ch", owner_epoch="epoch",
        profile_digest=profile["profile_digest"], profile_binding_digest=host._handoff_digest(profile), custody_scope=str(tmp_path), custody_capabilities={"host": reference})
    return preparation, request, abort


def test_bound_semantic_refusal_retains_cleanup_only_and_abort_replays(pending):
    p, request, abort = pending
    with pytest.raises(host.HostError, match="shape"):
        p.dispatch(request)
    assert p._pending_host_request == request and p._request is None and p.result is None
    ack = p.dispatch(abort)
    assert ack["status"] == "cleaned" and ack["cleanup"] == {"host_children": "absent"}
    assert p.dispatch(abort) == ack
    with pytest.raises(host.HostError, match="replay"):
        p.dispatch(request)
    with pytest.raises(host.HostError, match="aborted"):
        p.construct_claim_host(lambda: pytest.fail("created after abort"))
    with pytest.raises(host.HostError, match="aborted"):
        p.retain_activation_grant(dict(version=host._ACTIVATION_VERSION, operation_id="op", channel_id="ch", executor_incarnation="inc", evidence_digest="sha256:" + "2" * 64))
    assert p.result is None


@pytest.mark.parametrize("mutation", ["extra", "version", "operation_id", "channel_id", "owner_epoch", "pid", "birth_id", "profile", "scope", "peer"])
def test_untrusted_request_cannot_install_pending_authority(pending, mutation):
    p, original, abort = pending
    request = copy.deepcopy(original)
    if mutation == "extra": request["extra"] = True
    elif mutation in {"version", "operation_id", "channel_id", "owner_epoch"}: request[mutation] = "foreign"
    elif mutation in {"pid", "birth_id"}: request["runtime_owner"][mutation] = 999 if mutation == "pid" else "foreign"
    elif mutation == "profile": request["profile"]["extra"] = True
    elif mutation == "scope": request["custody_scope"] += "foreign"
    else: p._retained_relay_actor = SimpleNamespace(verify=lambda: {**original["runtime_owner"], "birth_id": "foreign"})
    with pytest.raises((host.HostError, contract.HostedContractError)):
        p.dispatch(request)
    assert p._pending_host_request is None and p._request is None and p.result is None
    with pytest.raises(host.HostError): p.dispatch(abort)


@pytest.mark.parametrize("phase", ["parked", "claim_owned", "claim_constructing", "shutdown_failed"])
def test_cleanup_requires_controlled_phase_or_actual_owner_proof(pending, phase):
    p, request, abort = pending
    with pytest.raises(host.HostError): p.dispatch(request)
    calls = []
    p._host_only_phase = phase
    if phase in {"claim_owned", "shutdown_failed"}:
        def shutdown():
            calls.append("shutdown")
            if phase == "shutdown_failed": raise host.CleanupUncertainError("real child unresolved")
        p._claim_host = SimpleNamespace(shutdown=shutdown)
    result = p.dispatch(abort)
    assert result["status"] == ("cleaned" if phase in {"parked", "claim_owned"} else "unresolved")
    assert calls == (["shutdown"] if phase in {"claim_owned", "shutdown_failed"} else [])
    assert p._abort_started
    if result["status"] == "unresolved": assert not p._aborted and "cleanup" not in result


def test_failed_constructor_cannot_be_reported_as_no_child(pending):
    p, request, abort = pending
    with pytest.raises(host.HostError): p.dispatch(request)
    def fail(): raise ValueError("constructor failed after an unknown obligation")
    with pytest.raises(ValueError): p.construct_claim_host(fail)
    assert p._claim_host is None and p._host_only_phase == "claim_constructing"
    assert p.dispatch(abort)["status"] == "unresolved"


def test_abort_serializes_constructor_and_cleans_created_owner(pending):
    p, request, abort = pending
    with pytest.raises(host.HostError): p.dispatch(request)
    entered, release, finished = threading.Event(), threading.Event(), threading.Event()
    calls = []
    def factory():
        entered.set(); assert release.wait(2)
        return SimpleNamespace(shutdown=lambda: calls.append("shutdown"))
    constructor = threading.Thread(target=lambda: p.construct_claim_host(factory))
    constructor.start(); assert entered.wait(2)
    replies = []
    def stop(): replies.append(p.dispatch(abort)); finished.set()
    stopper = threading.Thread(target=stop); stopper.start()
    assert not finished.wait(0.02)
    release.set(); constructor.join(2); stopper.join(2)
    assert not constructor.is_alive() and not stopper.is_alive()
    assert calls == ["shutdown"] and replies[0]["status"] == "cleaned"


@pytest.mark.parametrize("transport", ["eof", "broken_pipe"])
def test_control_keeps_first_refusal_after_abort_and_transport_failure(pending, monkeypatch, caplog, transport):
    p, request, abort = pending
    monkeypatch.setattr(custody.AuthenticatedCleanupActor, "private_peer", lambda control: p._retained_relay_actor)
    parent, child = socket.socketpair(); parent.settimeout(2)
    if transport == "broken_pipe":
        monkeypatch.setattr(host, "_send_activation_frame", lambda *args: (_ for _ in ()).throw(BrokenPipeError("SECRET-TOKEN")))
    thread = p.serve_control(child.detach())
    host._send_activation_frame(parent, request) if transport == "eof" else parent.sendall(json.dumps(request).encode() + b"\n")
    if transport == "eof":
        refusal = host._read_activation_frame(parent, limit=65536)
        assert refusal["status"] == "unresolved" and p.result is None
        host._send_activation_frame(parent, abort)
        assert host._read_activation_frame(parent, limit=65536)["status"] == "cleaned"
    parent.close(); thread.join(2)
    assert not thread.is_alive()
    assert isinstance(p.control_error, host.HostError)
    assert p.control_diagnostics[0]["reason"] == "host-only selected profile shape is invalid"
    assert len(p.control_diagnostics) >= 2
    assert "SECRET-TOKEN" not in caplog.text


def test_arbitrary_exception_details_never_enter_diagnostics(pending, caplog):
    p, _, _ = pending
    first = ValueError("Bearer SECRET-TOKEN /private/credential")
    p._record_control_error(first)
    p._record_control_error(BrokenPipeError("SECOND-SECRET"))
    assert p.control_error is first
    assert "SECRET" not in json.dumps(p.control_diagnostics) and "SECRET" not in caplog.text


def test_abort_prepare_race_cannot_publish_late_success(pending, monkeypatch):
    p, request, abort = pending
    entered, release = threading.Event(), threading.Event()
    def prepare(_request):
        entered.set(); assert release.wait(2)
        p.result = {"status": "prepared"}
        p._host_only_phase = "prepared"
        return dict(p.result)
    monkeypatch.setattr(p, "_prepare_host_only", prepare)
    prepared, replies = [], []
    first = threading.Thread(target=lambda: prepared.append(p.dispatch(request)))
    first.start(); assert entered.wait(2)
    second = threading.Thread(target=lambda: replies.append(p.dispatch(abort)))
    second.start(); release.set(); first.join(2); second.join(2)
    assert not first.is_alive() and not second.is_alive()
    assert prepared == [{"status": "prepared"}] and replies[0]["status"] == "cleaned"
    with pytest.raises(host.HostError, match="replay"):
        p.dispatch(request)
