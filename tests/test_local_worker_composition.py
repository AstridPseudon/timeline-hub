from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import socket
import subprocess
import sys
from types import SimpleNamespace

import pytest

from test_storage_preparation_relay import source_composition

from runtime_protocol.errors import ConflictError
from runtime_protocol.local_worker import LocalWorkerProfile, ProcessIdentity
from runtime_protocol.local_worker_composition import (
    CrossProcessWorkerPreparer,
    OSProcessInspector,
    _PreparedWorker,
    _listening_socket_owner,
    load_local_worker_composition,
)


def _start_source(w):
    return w.d.start_local_worker(w.profile.profile_id, w.s.realm["id"])


def test_source_daemon_unavailable_storage_selects_authoring_and_is_idempotent(source_composition):
    w = source_composition
    w.availability("action_child_unavailable:fixture")
    assert _start_source(w) == {"state": "active"}
    selection = w.s._authoring_scene_selection
    assert selection.handle is w.handle and w.s._preparation_relay is None
    assert _start_source(w) == {"state": "active"}
    assert w.s._authoring_scene_selection is selection
    assert w.s._preparation_relay is None


@pytest.mark.parametrize("authoring", [None, "astrid"])
def test_source_daemon_ready_same_generation_preserves_preparation(source_composition, monkeypatch, authoring):
    from runtime_protocol.local_preparation_relay import LocalPreparationRelay
    w = source_composition
    w.d.authoring_profile = authoring
    monkeypatch.setattr(LocalPreparationRelay, "_paths", lambda self: None)
    _start_source(w)
    previous = w.s._preparation_relay
    _start_source(w)
    assert w.s._preparation_relay is previous
    previous._selected_host_check()


def test_source_daemon_replacement_clears_stale_storage_and_fences_old_work(source_composition, monkeypatch):
    from runtime_protocol.local_preparation_relay import LocalPreparationRelay
    w = source_composition
    monkeypatch.setattr(LocalPreparationRelay, "_paths", lambda self: None)
    _start_source(w)
    previous, selection = w.s._preparation_relay, w.s._authoring_scene_selection
    closed = []
    w.s._authoring_scene_relay = SimpleNamespace(close=lambda: closed.append(True))
    w.selected[0] = SimpleNamespace(**vars(w.handle))
    w.availability("action_child_unavailable:fixture")
    _start_source(w)
    assert w.s._preparation_relay is None and w.s._authoring_scene_relay is None
    assert w.s._authoring_scene_selection is not selection and closed == [True]
    with pytest.raises(Exception): previous._selected_host_check()
    with pytest.raises(Exception): selection.check()


@pytest.mark.parametrize("failure", ["staging", "selection", "recheck", "revoke", "credential_generation", "readiness", "publication"])
def test_source_daemon_fatal_composition_invalidates_references_retains_activation(source_composition, monkeypatch, failure):
    from runtime_protocol import local_preparation_relay as storage, authoring_scene as authoring
    from runtime_protocol.daemon import WORKER_ACTOR
    from runtime_protocol.errors import RuntimeErrorBase
    w = source_composition
    if failure in {"readiness", "publication"}:
        monkeypatch.setattr(storage.LocalPreparationRelay, "_paths", lambda self: None)
    else:
        w.availability("action_child_unavailable:fixture")
    _start_source(w)
    def close(): raise RuntimeError("secondary close failure")
    w.s._authoring_scene_relay = SimpleNamespace(close=close)
    primary = ConflictError("primary composition failure")
    if failure == "staging":
        def failed(*args): raise primary
        monkeypatch.setattr(storage, "bind_selected_host", failed)
    elif failure == "selection":
        def failed(*args, **kwargs): raise primary
        monkeypatch.setattr(authoring, "SelectedHostScene", failed)
    elif failure == "recheck":
        original = storage.bind_selected_host
        def replace(*args):
            staged = original(*args)
            w.selected[0] = SimpleNamespace(**vars(w.handle))
            return staged
        monkeypatch.setattr(storage, "bind_selected_host", replace)
    elif failure == "revoke": w.d.credentials.disable_actor(WORKER_ACTOR)
    elif failure == "readiness":
        def failed(*args): raise primary
        monkeypatch.setattr(storage.LocalPreparationRelay, "check_readiness", failed)
    elif failure == "publication":
        w.selected[0] = SimpleNamespace(**vars(w.handle))
        class FailPublication(type(w.s)):
            def __setattr__(self, name, value):
                if name == "_authoring_scene_selection" and value is not None:
                    assert self._preparation_relay is not None  # First write was staged under the mutex.
                    raise primary
                super().__setattr__(name, value)
        monkeypatch.setattr(w.s, "__class__", FailPublication)
    else: w.provision()
    with pytest.raises(RuntimeErrorBase) as caught:
        _start_source(w)
    if failure in {"staging", "selection", "readiness", "publication"}: assert caught.value is primary
    assert caught.value.details["local_worker_state"] == "activated_composition_failed"
    assert w.s._preparation_relay is None and w.s._authoring_scene_selection is None and w.s._authoring_scene_relay is None
    assert w.handle.activated and not w.handle.closed
    assert w.d.local_worker_launcher is not None
    assert w.d.credentials.actor_metadata(WORKER_ACTOR)["local_launch_receipt"] == w.receipt


def _digest(char: str) -> str:
    return "sha256:" + char * 64


def _content_digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _profile_document(tmp_path: Path) -> tuple[dict[str, object], Path, Path, Path]:
    source = tmp_path / "astrid"
    packs = source / "astrid" / "packs"
    packs.mkdir(parents=True)
    support = tmp_path / "support"
    support.mkdir()
    boot = support / "boot.json"
    boot.write_text("{}", encoding="utf-8")
    session_root = tmp_path / "vibecomfy" / "out" / "sessions" / "fixture"
    document = {
        "profile_id": "astrid",
        "machine_id": platform.node(),
        "engine_endpoint": "http://127.0.0.1:8188",
        "worker_environment": sys.prefix,
        "worker_executable": str(Path(sys.executable).resolve()),
        "host_executable": str(Path(sys.executable).resolve()),
        "engine_executable": str(Path(sys.executable).resolve()),
        "engine_listener_executable": str(Path(sys.executable).resolve()),
        "worker_artifact_digest": _digest("1"),
        "host_artifact_digest": _digest("2"),
        "engine_artifact_digest": _digest("3"),
        "engine_listener_artifact_digest": _digest("4"),
        "session_config_digest": _digest("5"),
        "profile_revision": "fixture-r1",
        "profile_digest": _digest("6"),
        "release_digest": _digest("7"),
        "source_checkout": str(source),
        "pack_root": str(packs),
        "boot_manifest_path": str(boot),
        "boot_manifest_hash": _digest("8"),
        "environment": {
            "ASTRID_VIBECOMFY_SESSION_DIR": str(session_root),
            "ASTRID_VIBECOMFY_PORT": "8188",
        },
    }
    return document, source, support, packs


def test_factory_derives_runtime_identity_and_roots(tmp_path: Path) -> None:
    document, source, support, _packs = _profile_document(tmp_path)
    path = tmp_path / "worker-profile.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    composition = load_local_worker_composition(
        path,
        workspace_uuid="realm-from-runtime",
        realm_root=tmp_path / "runtime-realm",
        support_root=support,
        runtime_instance_id="instance-1",
    )
    profile = composition.profiles["astrid"]
    assert profile.workspace_uuid == "realm-from-runtime"
    assert profile.realm_root == (tmp_path / "runtime-realm").resolve()
    assert profile.support_root == support.resolve()
    assert profile.realm_root != source.resolve()
    composition.bind_runtime(endpoint="http://127.0.0.1:1234", runtime_instance_id="instance-2", credential_file=support / "worker.token")
    assert composition.preparer.config["runtime_endpoint"] == "http://127.0.0.1:1234"
    assert composition.preparer.config["runtime_instance_id"] == "instance-2"


def test_factory_rejects_unknown_authority_fields(tmp_path: Path) -> None:
    document, _source, support, _packs = _profile_document(tmp_path)
    document["realm_root"] = "/attacker/realm"
    path = tmp_path / "worker-profile.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(Exception, match="unsupported fields"):
        load_local_worker_composition(
            path,
            workspace_uuid="realm",
            realm_root=tmp_path / "realm",
            support_root=support,
            runtime_instance_id="instance",
        )


def test_factory_rejects_endpoint_that_disagrees_with_worker_launch_port(tmp_path: Path) -> None:
    document, _source, support, _packs = _profile_document(tmp_path)
    document["engine_endpoint"] = "http://127.0.0.1:8189"
    path = tmp_path / "worker-profile.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(Exception, match="engine_endpoint"):
        load_local_worker_composition(
            path,
            workspace_uuid="realm",
            realm_root=tmp_path / "realm",
            support_root=support,
            runtime_instance_id="instance",
        )


def test_independent_inspector_rejects_worker_birth_claim(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    document, _source, support, _packs = _profile_document(tmp_path)
    path = tmp_path / "worker-profile.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    composition = load_local_worker_composition(
        path,
        workspace_uuid="realm",
        realm_root=tmp_path / "realm",
        support_root=support,
        runtime_instance_id="instance",
    )
    profile = composition.profiles["astrid"]
    inspector = OSProcessInspector(profile)
    pid = os.getpid()
    report = {
        "processes": {
            "worker": {"pid": pid, "birth_id": "worker-claim"},
            "host": {"pid": pid, "birth_id": "host-claim"},
            "engine": {"pid": pid, "birth_id": "engine-claim"},
            "engine_listener": {"pid": pid, "birth_id": "listener-claim"},
        },
        "engine_binding": {"socket_owner_pid": pid},
        "session_config_digest": profile.session_config_digest,
    }
    monkeypatch.setattr(
        "runtime_protocol.local_worker_composition.process_birth_identity",
        lambda observed_pid: "independently-observed-birth",
    )
    monkeypatch.setattr(
        "runtime_protocol.local_worker_composition._ps",
        lambda observed_pid, field: str(os.getpid()) if field == "ppid" else str(Path(sys.executable)),
    )
    handle = SimpleNamespace(report_value=report)
    with pytest.raises(ConflictError, match="birth identity"):
        inspector.observe(handle)


@pytest.mark.parametrize(
    ("socket_name", "accepted"),
    [
        ("127.0.0.1:8188", True),
        ("127.0.0.1:8189", False),
        ("127.0.0.2:8188", False),
        ("*:8188", False),
    ],
)
def test_listener_proof_requires_exact_configured_endpoint(monkeypatch, socket_name, accepted):
    monkeypatch.setattr(
        "runtime_protocol.local_worker_composition.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=f"p4321\nn{socket_name}\n"),
    )
    if accepted:
        assert _listening_socket_owner(4321, "http://127.0.0.1:8188") == (
            4321,
            "http://127.0.0.1:8188",
        )
    else:
        with pytest.raises(ConflictError, match="configured engine endpoint"):
            _listening_socket_owner(4321, "http://127.0.0.1:8188")


def _inspector_fixture(tmp_path: Path, *, machine_id="owner-machine", session_digest=None):
    config = b'{"port":8188,"warm_policy":"auto"}'
    config_path = tmp_path / "session" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_bytes(config)
    session_digest = session_digest or _content_digest(config)
    profile = LocalWorkerProfile(
        profile_id="astrid",
        workspace_uuid="realm",
        realm_root=tmp_path / "realm",
        support_root=tmp_path / "support",
        machine_id=machine_id,
        worker_executable=Path("/worker"),
        host_executable=Path("/host"),
        engine_executable=Path("/engine"),
        engine_listener_executable=Path("/listener"),
        engine_endpoint="http://127.0.0.1:8188",
        worker_artifact_digest=_digest("1"),
        host_artifact_digest=_digest("2"),
        engine_artifact_digest=_digest("3"),
        engine_listener_artifact_digest=_digest("4"),
        session_config_digest=session_digest,
        profile_revision="r1",
        profile_digest=_digest("6"),
        release_digest=_digest("7"),
    )
    report = {
        "processes": {
            "worker": {"pid": 100, "birth_id": "b100"},
            "host": {"pid": 101, "birth_id": "b101"},
            "engine": {"pid": 102, "birth_id": "b102"},
            "engine_listener": {"pid": 103, "birth_id": "b103"},
        },
        "engine_binding": {"socket_owner_pid": 103},
        "session_config_digest": session_digest,
    }
    return profile, SimpleNamespace(
        report_value=report,
        owner_session_config_path=config_path,
    )


def test_private_worker_v2_profile_shape_excludes_runtime_only_endpoint(tmp_path):
    profile, _handle = _inspector_fixture(tmp_path)
    payload = CrossProcessWorkerPreparer._profile_payload(profile)
    assert "engine_endpoint" not in payload
    assert set(payload) == {
        "profile_id", "workspace_uuid", "realm_root", "support_root", "machine_id",
        "worker_executable", "host_executable", "engine_executable",
        "engine_listener_executable", "worker_artifact_digest", "host_artifact_digest",
        "engine_artifact_digest", "engine_listener_artifact_digest",
        "session_config_digest", "profile_revision", "profile_digest", "release_digest",
    }


def _patch_inspector_os(monkeypatch, inspector):
    def identity(pid, birth, executable, digest, **kwargs):
        parents = {100: os.getpid(), 101: 100, 102: 100, 103: 102}
        groups = {100: 100, 101: 101, 102: 102, 103: 102}
        return ProcessIdentity(pid, birth, os.getuid(), parents[pid], groups[pid], groups[pid], executable, digest)

    monkeypatch.setattr(inspector, "_identity", identity)
    monkeypatch.setattr(
        "runtime_protocol.local_worker_composition._listening_socket_owner",
        lambda pid, endpoint: (pid, endpoint),
    )
    monkeypatch.setattr(
        "runtime_protocol.local_worker_composition._owner_machine_id",
        lambda: "owner-machine",
    )


def test_inspector_derives_machine_and_session_from_owner_facts(tmp_path, monkeypatch):
    profile, handle = _inspector_fixture(tmp_path)
    inspector = OSProcessInspector(profile)
    _patch_inspector_os(monkeypatch, inspector)

    observed = inspector.observe(handle)

    assert observed.machine_id == "owner-machine"
    assert observed.session_config_digest == _content_digest(handle.owner_session_config_path.read_bytes())
    assert observed.engine_endpoint == profile.engine_endpoint


def test_forged_profile_machine_cannot_create_observed_fact(tmp_path, monkeypatch):
    profile, handle = _inspector_fixture(tmp_path, machine_id="forged-machine")
    inspector = OSProcessInspector(profile)
    _patch_inspector_os(monkeypatch, inspector)
    with pytest.raises(ConflictError, match="machine identity"):
        inspector.observe(handle)


@pytest.mark.parametrize("forgery", ["profile", "report", "observed_file"])
def test_forged_session_digest_cannot_create_observed_fact(tmp_path, monkeypatch, forgery):
    profile, handle = _inspector_fixture(tmp_path)
    if forgery == "profile":
        from dataclasses import replace
        profile = replace(profile, session_config_digest=_digest("9"))
    else:
        if forgery == "report":
            handle.report_value = dict(handle.report_value)
            handle.report_value["session_config_digest"] = _digest("9")
        else:
            handle.owner_session_config_path.write_bytes(b'{"port":8189}')
    inspector = OSProcessInspector(profile)
    _patch_inspector_os(monkeypatch, inspector)
    with pytest.raises(ConflictError, match="session configuration"):
        inspector.observe(handle)


def test_cross_process_abort_is_bounded_and_reaps_after_kill(tmp_path, monkeypatch):
    profile, _handle = _inspector_fixture(tmp_path)

    class Worker:
        pid = 4321
        returncode = None

        def poll(self):
            return self.returncode

        def wait(self, timeout=None):
            if self.returncode is None:
                raise subprocess.TimeoutExpired("worker", timeout)
            return self.returncode

    parent, peer = socket.socketpair()
    worker = Worker()
    handle = _PreparedWorker(worker, "birth", parent, {}, tmp_path / "config.json")
    preparer = CrossProcessWorkerPreparer(
        profile=profile,
        config={},
        environment={},
        timeout_seconds=900,
        cleanup_timeout_seconds=0.05,
    )
    preparer._active = handle
    monkeypatch.setattr(preparer, "_birth", lambda _pid: "birth")
    signals = []

    def killpg(_pid, sent_signal):
        signals.append(sent_signal)
        if sent_signal == signal.SIGKILL:
            worker.returncode = -signal.SIGKILL

    monkeypatch.setattr("runtime_protocol.local_worker_composition.os.killpg", killpg)
    started = __import__("time").monotonic()
    try:
        with pytest.raises((TimeoutError, OSError)):
            preparer.abort(handle)
    finally:
        peer.close()
    elapsed = __import__("time").monotonic() - started

    assert elapsed < 0.5
    assert signals == [signal.SIGTERM, signal.SIGKILL]
    assert worker.poll() == -signal.SIGKILL
    assert handle.closed is True
    assert preparer._active is None


def test_cancel_current_does_not_wait_unbounded_for_spawn_handoff(tmp_path):
    profile, _handle = _inspector_fixture(tmp_path)
    preparer = CrossProcessWorkerPreparer(
        profile=profile,
        config={},
        environment={},
        cleanup_timeout_seconds=0.05,
    )
    preparer._handoff_lock.acquire()
    started = __import__("time").monotonic()
    try:
        preparer.cancel_current()
    finally:
        preparer._handoff_lock.release()
    assert __import__("time").monotonic() - started < 0.5


def test_control_probe_rejects_buffered_data_from_closed_peer(tmp_path, monkeypatch):
    profile, _unused = _inspector_fixture(tmp_path)

    class Worker:
        pid = 4321

        @staticmethod
        def poll():
            return None

    parent, peer = socket.socketpair()
    handle = _PreparedWorker(Worker(), "birth", parent, {}, tmp_path / "config.json")
    preparer = CrossProcessWorkerPreparer(profile=profile, config={}, environment={})
    monkeypatch.setattr(preparer, "_birth", lambda _pid: "birth")
    peer.sendall(b"unexpected")
    peer.close()
    try:
        assert preparer.control_alive(handle) is False
    finally:
        parent.close()


def test_explicit_relay_profile_translates_exact_engine_launch_without_worker_environment(tmp_path):
    from test_local_execution_supervisor import _prepare_case
    document, _source, support, _packs = _profile_document(tmp_path)
    selected, _ = _prepare_case()
    document.pop("worker_environment")
    document["engine_launch"] = selected["profile"]["engine_launch"]
    document["session_config_digest"] = selected["profile"]["session_config_digest"]
    path = tmp_path / "relay-profile.json"
    path.write_text(json.dumps(document))
    composition = load_local_worker_composition(path, workspace_uuid="realm", realm_root=tmp_path / "realm", support_root=support, runtime_instance_id="runtime-epoch")
    assert composition.profiles["astrid"].engine_launch == document["engine_launch"]
    assert "ASTRID_WORKER_ENVIRONMENT" not in composition.preparer.environment
    assert composition.preparer.config["runtime_instance_id"] == "runtime-epoch"


def test_relay_receipt_v4_binds_epoch_scope_roles_and_selected_profile(tmp_path):
    from dataclasses import replace
    from test_local_execution_supervisor import _prepare_case
    from runtime_protocol.local_execution_supervisor import preparation_report, digest
    from runtime_protocol.local_worker import LocalWorkerLauncher, LocalWorkerObservation, _selected_profile_payload, _receipt_identity_digest_valid
    selected, host_report = _prepare_case()
    profile = LocalWorkerProfile(**{k: Path(v) if k in {"realm_root", "support_root", "worker_executable", "host_executable", "engine_executable", "engine_listener_executable"} else v for k, v in selected["profile"].items()})
    refs = dict(host_report["custody_capabilities"])
    for role, pid, birth in (("relay", 20, "relay-birth"), ("host", 21, "host-birth")):
        refs[role] = {**refs["engine"], "role": role, "target": {**refs["engine"]["target"], "pid": pid, "birth_id": birth}}
    for ref in refs.values():
        ref["target"] = {**ref["target"], "uid": os.getuid()}
    host_report = {**host_report, "custody_capabilities": {role: refs[role] for role in ("engine", "engine_listener")}}
    report = preparation_report(selected, host_report, relay_process={"pid": 20, "birth_id": "relay-birth"}, relay_reference=refs["relay"], host_reference=refs["host"])
    processes = {}
    for role, pid, parent, birth in (("worker", 20, 19, "relay-birth"), ("host", 21, 20, "host-birth"), ("engine", 22, 21, "engine-birth"), ("engine_listener", 23, 22, "listener-birth")):
        exe_name = "worker" if role == "worker" else role
        processes[role] = ProcessIdentity(pid, birth, os.getuid(), parent, 22 if role == "engine_listener" else pid, 22 if role == "engine_listener" else pid, getattr(profile, exe_name + "_executable"), getattr(profile, exe_name + "_artifact_digest"))
    observed = LocalWorkerObservation(profile.machine_id, os.getuid(), profile.workspace_uuid, profile.realm_root, profile.support_root, **processes, engine_listener_socket_owner_pid=23, engine_endpoint=profile.engine_endpoint, session_config_digest=profile.session_config_digest, owner_epoch="runtime-epoch", custody_scope=selected["custody_scope"], custody_capabilities=refs)
    launcher = object.__new__(LocalWorkerLauncher)
    launcher.runtime_pid = 19
    launcher.workspace_uuid = profile.workspace_uuid
    launcher.realm_root = profile.realm_root
    launcher.support_root = profile.support_root
    identity = launcher._validate_observation(profile, observed, report=report, operation_id="operation", channel_id="channel")
    receipt = {"version": "runtime.local-worker-receipt/v4", **identity, "executor_incarnation": "incarnation"}
    assert identity["profile_binding_digest"] == digest(_selected_profile_payload(profile))
    args = dict(workspace_uuid=profile.workspace_uuid, realm_root=profile.realm_root, support_root=profile.support_root)
    assert _receipt_identity_digest_valid(profile, receipt, **args)
    changed = {**receipt, "owner_epoch": "replacement-runtime"}
    assert not _receipt_identity_digest_valid(profile, changed, **args)
    changed_report = {**report, "owner_epoch": "replacement-runtime"}
    with pytest.raises(ConflictError, match="independently verified custody"):
        launcher._validate_observation(profile, observed, report=changed_report, operation_id="operation", channel_id="channel")


def test_relay_stop_without_retained_control_never_uses_numeric_signal(tmp_path, monkeypatch):
    from dataclasses import replace
    document, _, support, _ = _profile_document(tmp_path)
    profile = LocalWorkerProfile(**{k: Path(v) if k in {"realm_root", "support_root", "worker_executable", "host_executable", "engine_executable", "engine_listener_executable"} else v for k, v in __import__("test_local_execution_supervisor")._prepare_case()[0]["profile"].items()})
    preparer = CrossProcessWorkerPreparer(profile=profile, config={}, environment={})
    monkeypatch.setattr(os, "kill", lambda *_: pytest.fail("numeric fallback"))
    monkeypatch.setattr(os, "killpg", lambda *_: pytest.fail("numeric fallback"))
    with pytest.raises(ConflictError, match="retained control"):
        preparer.stop_owned({})


def test_relay_restart_cannot_treat_missing_control_as_absent_generation():
    from test_local_execution_supervisor import _prepare_case
    selected = _prepare_case()[0]["profile"]
    profile = LocalWorkerProfile(**{k: Path(v) if k in {"realm_root", "support_root", "worker_executable", "host_executable", "engine_executable", "engine_listener_executable"} else v for k, v in selected.items()})
    preparer = CrossProcessWorkerPreparer(profile=profile, config={}, environment={})
    with pytest.raises(ConflictError, match="capability recovery remains unresolved"):
        preparer.reconnect({"version": "runtime.local-worker-receipt/v4"})


def test_relay_retained_reconnect_requires_exact_receipt_and_incarnation(tmp_path, monkeypatch):
    import copy
    from test_local_execution_supervisor import _handoff_case, _prepare_case
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.local_worker import _credential_commit_generation
    from runtime_protocol.local_execution_handoff import write_protected
    request, _ = _handoff_case(tmp_path)
    caps = request["binding"]["current_roles"]
    selected = _prepare_case()[0]["profile"]
    selected.update(support_root=str(tmp_path))
    profile = LocalWorkerProfile(**{k: Path(v) if k in {"realm_root", "support_root", "worker_executable", "host_executable", "engine_executable", "engine_listener_executable"} else v for k, v in selected.items()})
    preparer = CrossProcessWorkerPreparer(profile=profile, config={}, environment={})
    scope = tmp_path / "custody"
    receipt = {"version": "runtime.local-worker-receipt/v4", "owner_epoch": "A", "custody_scope": str(scope), "profile_binding_digest": "sha256:" + "1" * 64, "executor_incarnation": "incarnation", "evidence_digest": "sha256:" + "2" * 64, "custody_capabilities": caps,
               **{alias: {k: caps[role]["target"][k] for k in ("pid", "birth_id")} for alias, role in (("worker", "relay"), ("host", "host"), ("engine", "engine"), ("engine_listener", "engine_listener"))}}
    credentials = CredentialStore(tmp_path / "credentials")
    credentials.provision("actor", [], metadata={"local_launch_receipt": receipt})
    generation = _credential_commit_generation(credentials, "actor")
    write_protected(scope / "activation-record.json", {"evidence_digest": receipt["evidence_digest"], "executor_incarnation": "incarnation", "custody_capabilities": caps, "original_owner_epoch": "A", "credential_generation": generation})
    live = copy.deepcopy(caps)
    current = request["binding"]["source_owner"]
    monkeypatch.setattr("banodoco_local.custody_broker.AuthenticatedCleanupActor.current", lambda: SimpleNamespace(verify=lambda: current))
    class Authority:
        def __init__(self, scope, role):
            self.role = role
        def verify_reference(self, ref, **kwargs):
            if ref != live[self.role]:
                raise ConflictError("kernel incarnation changed")
            return ref
    monkeypatch.setattr("banodoco_local.custody_broker.RoleCustodyAuthority", Authority)
    handle = SimpleNamespace(relay=True, activated=True, closed=False, owner_epoch="A", custody_scope=str(scope), retained=SimpleNamespace(verify=lambda: caps["relay"]["target"]))
    preparer._active = handle
    preparer._generation_verifier = (handle, lambda: _credential_commit_generation(credentials, "actor"))
    report = {"owner_epoch": "A", "profile_binding_digest": receipt["profile_binding_digest"], "custody_scope": str(scope), "custody_capabilities": caps, "processes": {role: receipt[role] for role in ("worker", "host", "engine", "engine_listener")}}
    monkeypatch.setattr(preparer, "report", lambda h: copy.deepcopy(report))
    before = (scope / "activation-record.json").read_bytes()
    assert preparer.reconnect(receipt) is handle
    assert (scope / "activation-record.json").read_bytes() == before
    changed = {**receipt, "evidence_digest": "sha256:" + "9" * 64}
    with pytest.raises(ConflictError, match="activation evidence"):
        preparer.reconnect(changed)
    live["engine"]["target"]["birth_id"] = "replacement"
    with pytest.raises(ConflictError, match="incarnation changed"):
        preparer.reconnect(receipt)


def test_relay_adoption_failure_retains_nonchild_cleanup_obligation(tmp_path, monkeypatch):
    from test_local_execution_supervisor import _prepare_case
    selected = _prepare_case()[0]["profile"]
    profile = LocalWorkerProfile(**{k: Path(v) if k in {"realm_root", "support_root", "worker_executable", "host_executable", "engine_executable", "engine_listener_executable"} else v for k, v in selected.items()})
    preparer = CrossProcessWorkerPreparer(profile=profile, config={}, environment={})
    a, b = socket.socketpair()
    obligation = SimpleNamespace(control=a, inherited_from="A", cleanup_unresolved=True)
    monkeypatch.setattr(os, "kill", lambda *_: pytest.fail("numeric fallback"))
    monkeypatch.setattr(os, "waitpid", lambda *_: pytest.fail("nonchild wait"))
    try:
        with pytest.raises(ConflictError, match="fresh authenticated B"):
            preparer.adopt_control_descriptor(obligation, {}, {})
        assert obligation.control.fileno() >= 0 and obligation.cleanup_unresolved
        assert preparer._active is None
        a.sendall(b"retained"); assert b.recv(8) == b"retained"
    finally:
        a.close(); b.close()


def test_g1b_both_profile_projections_preserve_optional_protocol():
    from dataclasses import replace
    from runtime_protocol.local_worker import _selected_profile_payload
    from test_local_worker import profile_case, declaration
    profile=profile_case()
    assert 'host_protocol' not in CrossProcessWorkerPreparer._profile_payload(profile)
    selected=replace(profile,host_protocol=declaration())
    projected=CrossProcessWorkerPreparer._profile_payload(selected)
    canonical=_selected_profile_payload(selected)
    assert projected['host_protocol']==canonical['host_protocol']==declaration()
    from runtime_protocol.local_execution_supervisor import digest
    assert digest(projected)!=digest(CrossProcessWorkerPreparer._profile_payload(profile))


@pytest.mark.parametrize('protocol',[None, {}, {'version':'unknown'}, {'version':'runtime.local-execution-current-roles/v1','module':'astrid.core.execution.generic_host','source_closure_digest':'sha256:'+'a'*64}])
def test_g1b_profile_loader_rejects_malformed_optional_field(tmp_path,protocol):
    document,source,support,packs=_profile_document(tmp_path);document['host_protocol']=protocol
    path=tmp_path/'worker-profile.json';path.write_text(json.dumps(document))
    with pytest.raises(Exception,match='host_protocol'):
        load_local_worker_composition(path,workspace_uuid='w',realm_root=tmp_path/'realm',support_root=support,runtime_instance_id='epoch')


def test_g1b_profile_loader_rejects_legacy_protocol_path(tmp_path):
    from test_local_worker import declaration
    document,source,support,packs=_profile_document(tmp_path);document['host_protocol']=declaration()
    path=tmp_path/'worker-profile.json';path.write_text(json.dumps(document))
    with pytest.raises(Exception,match='requires.*engine_launch'):
        load_local_worker_composition(path,workspace_uuid='w',realm_root=tmp_path/'realm',support_root=support,runtime_instance_id='epoch')


def test_g1b_selected_loader_carries_protocol_without_claiming_verification(tmp_path):
    from test_local_execution_supervisor import _prepare_case
    from test_local_worker import declaration
    document,source,support,packs=_profile_document(tmp_path);selected=_prepare_case()[0]['profile']
    document.update(engine_launch=selected['engine_launch'],session_config_digest=selected['session_config_digest'],host_protocol=declaration())
    path=tmp_path/'worker-profile.json';path.write_text(json.dumps(document))
    composition=load_local_worker_composition(path,workspace_uuid='w',realm_root=tmp_path/'realm',support_root=support,runtime_instance_id='epoch')
    assert composition.profiles['astrid'].host_protocol==declaration()
    assert CrossProcessWorkerPreparer._profile_payload(composition.profiles['astrid'])['host_protocol']==declaration()


def test_host_only_loader_preserves_lexical_interpreter_and_rejects_engine(tmp_path):
    from runtime_protocol.local_worker import _digest
    from runtime_protocol.local_execution_supervisor import CURRENT_ROLES_VERSION
    document, source, support, packs = _profile_document(tmp_path)
    for key in ['worker_environment','worker_executable','worker_artifact_digest','engine_executable','engine_listener_executable','engine_artifact_digest','engine_listener_artifact_digest','engine_endpoint']:
        document.pop(key)
    document.update(execution_mode='host_only_cpu', host_executable=os.path.abspath(sys.executable),
        host_os_executable=str(Path(sys.executable).resolve()), host_os_artifact_digest=_digest('1'),
        host_protocol={'version':CURRENT_ROLES_VERSION,'module':'astrid.core.execution.generic_host','source_closure_digest':'a'*64},environment={},max_concurrency=4)
    launch = {k:document[k] for k in ('source_checkout','pack_root','boot_manifest_path','boot_manifest_hash','environment')}
    launch['capability_matrix']=None
    launch['max_concurrency']=4
    document['session_config_digest']=_digest(launch)
    path=tmp_path/'host-only.json';path.write_text(json.dumps(document))
    result=load_local_worker_composition(path, workspace_uuid='realm', realm_root=tmp_path/'realm',support_root=support,runtime_instance_id='epoch')
    profile=result.profiles['astrid']
    assert str(profile.host_executable)==os.path.abspath(sys.executable)
    assert profile.worker_executable is None and profile.engine_launch is None
    document['engine_launch']={};path.write_text(json.dumps(document))
    with pytest.raises(Exception,match='cannot declare'):
        load_local_worker_composition(path, workspace_uuid='realm',realm_root=tmp_path/'realm',support_root=support,runtime_instance_id='epoch')


def test_host_only_nonchild_stop_and_reconnect_never_signal(tmp_path, monkeypatch):
    from test_local_worker import host_only_profile_case
    profile=host_only_profile_case()
    preparer=CrossProcessWorkerPreparer(profile=profile,config={},environment={})
    monkeypatch.setattr(os,'kill',lambda *args:pytest.fail('numeric PID cleanup'))
    monkeypatch.setattr(os,'killpg',lambda *args:pytest.fail('numeric group cleanup'))
    with pytest.raises(ConflictError,match='original retained'):
        preparer.stop_owned({'host':{'pid':123,'birth_id':'old'}})
    with pytest.raises(ConflictError,match='unsupported'):
        preparer.reconnect({'host':{'pid':123,'birth_id':'old'}})


@pytest.mark.parametrize("selection,fault", [(s, None) for s in ("none", "unselected_matrix", "isolation", "matrix", "additional", "unavailable", "renderer")]
    + [("isolation", f) for f in ("seal", "release", "reply", "inspection_cleanup")])
def test_host_only_preparer_projects_admitted_slots_and_canonical_binding_without_engine(tmp_path,monkeypatch,selection,fault,request):
    """Offline transport contract only; fake handles grant no native custody proof."""
    import threading
    from dataclasses import replace
    from test_local_worker import host_only_profile_case
    from runtime_protocol import local_worker_composition as module
    from runtime_protocol import verified_host_launch, local_execution_supervisor
    import banodoco_local.custody_broker as custody
    import astrid.core.execution.custody_broker as inspection_custody
    from astrid.core.execution import declared_executables as de
    renderer = selection == "renderer"
    needs_inspection = selection not in {"none", "unselected_matrix"}
    original=SimpleNamespace(pid=4242)
    identity={'pid':4242,'birth_id':'original','uid':os.getuid()}
    selected=host_only_profile_case()
    packs = tmp_path / 'packs'; packs.mkdir()
    extra = tmp_path / 'extra'; extra.mkdir()
    executable = tmp_path / 'helper'; executable.write_bytes(b'offline executable pin'); executable.chmod(0o700)
    if selection == 'unavailable': executable.unlink()
    tool = tmp_path / 'reader'; tool.write_bytes(b'offline reader pin')
    tool_pin = de.FilePin.measure(tool)
    monkeypatch.setattr(de, '_InspectionTool', lambda: SimpleNamespace(executable=tool_pin, verify=tool_pin.verify))
    manifest = {'schema_version': 1, 'id': 'test.cpu', 'name': 'CPU', 'kind': 'external', 'version': '1.0',
        'command': {'argv': ['{python_exec}', '-c', 'pass']}, 'outputs': [],
        'isolation': {'mode': 'subprocess', 'network': False, 'binaries': ['helper'] if selection in {'isolation', 'additional', 'unavailable'} else []}}
    (extra if selection == 'additional' else packs).joinpath('executor.yaml').write_text(json.dumps(manifest))
    matrix = tmp_path / 'matrix.json'
    matrix.write_text(json.dumps({'schema_version': 1, 'capabilities': [{'id': 'not.selected' if selection == 'unselected_matrix' else 'test.cpu', 'disposition': 'required',
        'evidence_reason': 'offline contract', 'required_binaries': ['helper'] if selection in {'matrix', 'unselected_matrix'} else []}]}))
    from runtime_protocol.local_worker import _digest
    launch = {**selected.host_launch, 'source_checkout': str(tmp_path), 'pack_root': str(packs),
        'capability_matrix': str(matrix), 'environment': {'PATH': str(tmp_path)}}
    if selection == 'additional':
        launch['additional_pack_roots'] = [{'path': str(extra), 'files': module._pack_inventory(str(extra))}]
    profile=replace(selected,support_root=tmp_path,host_launch=launch,session_config_digest=_digest(launch))
    if renderer:
        from runtime_protocol.local_worker import _digest
        from astrid.core.execution import host_renderer_selection
        launch={**profile.host_launch, "renderer_selection":{"node_executable":str(Path(sys.executable).resolve())}}
        profile=replace(profile,host_launch=launch,session_config_digest=_digest(launch))
        monkeypatch.setattr(host_renderer_selection,"renderer_selection_payload",lambda value:None)
    config={**profile.host_launch,'runtime_endpoint':'http://127.0.0.1:1','runtime_instance_id':'epoch',
        'credential_file':str(tmp_path/'credential'),'ready_file':str(tmp_path/'ready')}
    captures={};read_done=threading.Event()
    for key in ('PYTHONPATH','PYTHONHOME','PYTHONDONTWRITEBYTECODE','BANODOCO_LOCAL_DATA_ROOT','BANODOCO_RUNTIME_OWNER_TOKEN','ASTRID_OUTPUT_ROOT','ASTRID_EXECUTION_TARGET_JSON','ASTRID_COMMAND_CUSTODY_ENABLED','ASTRID_COMMAND_CONTROL_FD'):
        monkeypatch.setenv(key,'unadmitted-ambient')
    class Verifier:
        def __init__(self,**kwargs):pass
        def verify(self,**kwargs):captures['argv']=kwargs['host_argv'];captures['environment']=kwargs['environment'];return object()
        def claim(self,proof,**kwargs):
            captures['binding_fd']=kwargs['binding_fd']
            captures['claimed']=True
            return [kwargs['host_argv'][0],'-I','-S',str(verified_host_launch.__file__),'--binding-fd',str(kwargs['binding_fd'])],b'{"canonical":true}'
        def bind_child(self,proof,**kwargs):assert kwargs['child'] is original
        def verify_child(self,proof,**kwargs):assert kwargs['child'] is original
    class Retained:
        def __init__(self,process):assert process is original
        def bind_actor(self):
            if needs_inspection: assert captures.get("released") is True
        def verify(self):return identity
        def poll(self):return captures.get('original_wait')
        def wait(self,timeout):
            assert captures['signalled'] == original.pid
            captures['original_wait'] = 0
            return 0
    class Broker:
        def __init__(self,**kwargs):
            assert kwargs['role']=='host'
            assert kwargs.get('defer_accept',False) is needs_inspection
            assert kwargs.get('retain_channel',False) is needs_inspection
            descriptor=custody._open_authority_scope_lock(kwargs['authority_scope_root'])
            os.close(descriptor)
            self.role_authority=SimpleNamespace(reference=lambda:{'role':'host'})
            self.role='host';self.owner_epoch=kwargs['owner_epoch'];self.run_id='fake-run'
            self.custody_generation=1;self.authority_scope_root=kwargs['authority_scope_root']
            self.operation_channel=None
            self.child_pipe_binding=[]
            self.pipe_fds=[]
            if needs_inspection:
                # Match the SDK broker's actual anonymous directional endpoints.
                request_read, request_write = os.pipe()
                reply_read, reply_write = os.pipe()
                self.pipe_fds = [request_read, request_write, reply_read, reply_write]
                self.child_pipe_binding = [inspection_custody._pipe_identity(reply_read, os.O_RDONLY),
                                           inspection_custody._pipe_identity(request_write, os.O_WRONLY)]
        def create_hosted_launch(self,preparation):
            from astrid.core.execution.hosted_contract import HostedLaunch
            captures['hosted'] = HostedLaunch(self,preparation)
            return captures['hosted']
        def child_environment(self,argv,**kwargs):return {}
        def start_accept(self):
            assert captures.get('claimed') and captures.get('inspection_prepared')
            captures['accept_started']=True
        def wait_until_sealed(self):
            if fault == 'seal': raise ConflictError('offline seal refusal')
            captures["sealed"]=True
        def close_child_pipes(self):
            for fd in self.pipe_fds: os.close(fd)
            self.pipe_fds=[]
        def abort_before_spawn(self):self.close_child_pipes()
        def set_cleanup_deadline(self,deadline):pass
        def signal(self,sig,*,expected_pid):
            assert sig == signal.SIGTERM and expected_pid == original.pid
            captures['signalled'] = expected_pid
        def release_suspended_launch(self,**kwargs):
            assert needs_inspection and captures.get("sealed") is True
            assert kwargs==dict(expected_pid=original.pid,process=original)
            if fault == 'release': raise ConflictError('offline release refusal')
            captures["released"]=True
    class InspectionBroker(Broker):
        def __init__(self, **kwargs):
            assert needs_inspection
            super().__init__(**kwargs)
    class PlainBroker(Broker):
        def __init__(self, **kwargs):
            assert not needs_inspection
            super().__init__(**kwargs)
    class InspectionOwner(inspection_custody._CommandInventoryOwner):
        def __init__(self,context,policy):
            super().__init__(context,policy)
            captures['inspection_prepared']=True
            assert context._launch_broker.owner_epoch == context.owner_epoch == 'epoch'
            assert context.process is None and context.root == tmp_path/'local-execution-custody'/'op'
            assert set(policy['inspection'].selections) == ({'node'} if renderer else set() if selection == 'unavailable' else {'helper'})
        def start(self):
            assert self.custody.process is original
            # Only the native transport thread is replaced. Abort and finish
            # still run the exact SDK owner lifecycle against retained state.
            self.done.set()
            if fault == 'inspection_cleanup': self.error = inspection_custody.CustodyError('offline uncertain helper')
    monkeypatch.setattr(inspection_custody,"_CommandInventoryOwner",InspectionOwner)
    monkeypatch.setattr(inspection_custody,"RoleBoundCustodyBroker",InspectionBroker)
    monkeypatch.setattr(inspection_custody,"default_process_identity",lambda pid:{"pid":os.getpid(),"uid":os.getuid(),"parent_pid":1,"birth_id":"owner"})
    def popen(argv,**kwargs):
        from astrid.core.execution import hosted_contract
        assert type(captures['hosted']) is hosted_contract.HostedLaunch
        binding = captures['hosted'].value
        if needs_inspection:
            assert captures.get('accept_started')
            assert binding['inspection_pipes'] == captures['hosted'].broker.child_pipe_binding
            assert {p['fd'] for p in binding['inspection_pipes']} <= set(kwargs['pass_fds'])
            hosted_contract.validate(binding, role='host')  # Real open pipe identities, before spawn.
        else:
            assert 'inspection_pipes' not in binding
        # The fake child must retain the real anonymous endpoint just as a
        # spawned child would. Preparation sends its preflight bytes directly;
        # intercepting _frame_send covers only the later ordinary controls.
        captures['control_peer'] = captures['hosted'].children['control'].dup()
        request.addfinalizer(captures['control_peer'].close)
        descriptor=os.dup(captures['binding_fd'])
        def read_binding():
            data=b''
            while True:
                chunk=os.read(descriptor,4096)
                if not chunk:break
                data+=chunk
            os.close(descriptor);captures['binding']=data;read_done.set()
        threading.Thread(target=read_binding,daemon=True).start()
        return original
    monkeypatch.setattr(verified_host_launch,'TrustedLocalHostLaunchVerifier',Verifier)
    monkeypatch.setattr(local_execution_supervisor,'RetainedProcess',Retained)
    monkeypatch.setattr(custody,'RoleBoundCustodyBroker',PlainBroker)
    monkeypatch.setattr(custody,'default_process_identity',lambda pid:{'pid':os.getpid(),'uid':os.getuid(),'parent_pid':1,'birth_id':'owner'})
    monkeypatch.setattr(module,'_installed_host_release',lambda *args:{})
    monkeypatch.setattr(module.subprocess,'Popen',popen)
    monkeypatch.setattr(module,'_frame_send',lambda channel,value:captures.update(request=value))
    encode = module._prepare_frame_encode
    def capture_preparation(value):
        captures['request'] = value
        return encode(value)
    monkeypatch.setattr(module, '_prepare_frame_encode', capture_preparation)
    receive_frame = module._frame_receive
    def receive(channel, **kwargs):
        request = captures['request']
        if request.get('command') == 'abort_local_execution':
            return {**{k:v for k,v in request.items() if k != 'command'}, 'status':'cleaned', 'cleanup':{'host_children':'absent'}}
        captures['control_peer'].settimeout(1)
        assert receive_frame(captures['control_peer']) == request
        if fault == 'reply': raise ConflictError('offline reply refusal')
        return {'version':request['version'],'status':'prepared', 'operation_id':'op','channel_id':'channel',
            'owner_epoch':'epoch','execution_mode':'host_only_cpu', 'processes':{'host':{'pid':4242,'birth_id':'original'}},
            'session_config_digest':profile.session_config_digest}
    monkeypatch.setattr(module,'_frame_receive',receive)
    preparer=CrossProcessWorkerPreparer(profile=profile,config=config,environment={})
    if fault in {'seal', 'release', 'reply'}:
        with pytest.raises(ConflictError, match=f'offline {fault} refusal'):
            preparer.prepare(profile,operation_id='op',channel_id='channel')
        assert captures['original_wait'] == 0 and captures['request']['channel_id'] == 'channel'
        assert read_done.wait(1)
        if fault == 'reply':
            assert preparer._active is None  # Released owner settles normally.
        else:
            handle = preparer._active
            assert handle.worker is original and handle.inspection_owner.cancelled.is_set()
            assert handle.inspection_owner.released.is_set() and handle.inspection_owner.error is not None
            assert not handle.closed and preparer.cleanup_uncertain == 'host-only startup cleanup unresolved'
        return
    handle=preparer.prepare(profile,operation_id='op',channel_id='channel')
    try:
        assert preparer._active is handle and handle.worker is original and handle.host_only
        if needs_inspection:
            assert captures["released"] is True and handle.inspection_owner.released.is_set()
            assert captures['environment']['ASTRID_COMMAND_CUSTODY_ENABLED'] == '1'
        else:
            assert handle.inspection_owner is None and 'inspection_prepared' not in captures
            assert 'ASTRID_COMMAND_CUSTODY_ENABLED' not in captures['environment']

        assert read_done.wait(1) and captures['binding']==b'{"canonical":true}'
        argv=captures['argv'];assert argv[argv.index('--max-concurrency')+1]=='4'
        target=json.loads(argv[argv.index('--execution-target-json')+1]);assert target=={'kind':'default'}
        assert set(handle.report_value['processes'])=={'host'}
        env=captures['environment']
        assert env['ASTRID_OUTPUT_ROOT']==str(profile.support_root/'host-output')
        assert env['BANODOCO_LOCAL_DATA_ROOT']==str(profile.realm_root)
        assert not set(env)&{'PYTHONPATH','PYTHONHOME','PYTHONDONTWRITEBYTECODE','BANODOCO_RUNTIME_OWNER_TOKEN','ASTRID_EXECUTION_TARGET_JSON'}
        if fault == 'inspection_cleanup':
            with pytest.raises(ConflictError, match='original inspection owner unresolved'):
                preparer.abort(handle)
            assert preparer._active is handle and not handle.closed
        else:
            preparer.abort(handle)
            assert handle.closed and preparer._active is None
        assert handle.original_host_wait == 0 and handle.cleanup_acknowledged
        if needs_inspection:
            assert handle.inspection_owner.cancelled.is_set() and not handle.inspection_owner.accepting
    finally:
        handle.control.close();handle.activation.close()


@pytest.fixture
def cpu_inspection_owner(tmp_path, monkeypatch):
    """Exact SDK producer and predicates, with only native/tool surfaces mocked."""
    from astrid.core.execution import custody_broker as cb, declared_executables as de
    source = tmp_path / 'source'; source.mkdir()
    (source / '.git').write_text('offline source marker')
    pack = source / 'pack'; pack.mkdir()
    (pack / 'executor.yaml').write_text(json.dumps({'schema_version': 1, 'id': 'test.cpu', 'name': 'CPU',
        'kind': 'external', 'version': '1.0', 'command': {'argv': ['{python_exec}', '-c', 'pass']},
        'outputs': [], 'isolation': {'mode': 'subprocess', 'network': False, 'binaries': ['helper']}}))
    installed = tmp_path / 'installed'; installed.mkdir()
    executable = installed / 'helper'; executable.write_bytes(b'offline helper'); executable.chmod(0o700)
    tool = installed / 'reader'; tool.write_bytes(b'offline reader')
    tool_pin = de.FilePin.measure(tool)
    monkeypatch.setattr(de, '_InspectionTool', lambda: SimpleNamespace(executable=tool_pin, verify=tool_pin.verify))
    launch = cb._HostInspectionLaunch((pack,), source, {'PATH': str(installed)}, node_executable=None)
    identity = {'pid': os.getpid(), 'uid': os.getuid(), 'birth_id': 'offline-root',
        'audit_token_sha256': 'offline-token', 'audit_token_pidversion': 1}
    bound_identity = dict(identity)
    binding = {'run_id': 'offline-run', 'owner_epoch': 'epoch', 'generation': 1, 'target': dict(bound_identity)}
    actor = SimpleNamespace(verify=lambda: dict(identity))
    broker = SimpleNamespace(run_id='offline-run', operation_channel=object(),
        registration={'identity': dict(identity)}, retained_pipe_actor=lambda: actor,
        role_authority=SimpleNamespace(reference=lambda: {'generation': 1, 'target': dict(bound_identity)}),
        bind_ready_token=lambda **kw: None)
    owner = cb._CommandInventoryOwner(SimpleNamespace(_launch_broker=broker, owner_epoch='epoch',
        process=SimpleNamespace(pid=os.getpid()), root=tmp_path), launch.policy(launch.environment, str(tmp_path)))
    frame = {'version': cb._COMMAND_INVENTORY_VERSION, 'command': 'inventory_load_commands',
        'binding': binding, 'operation_id': 1, 'selection': 'helper', 'image': str(executable)}
    return SimpleNamespace(cb=cb, launch=launch, owner=owner, broker=broker, frame=frame,
        source=source, executable=executable, tool=tool, identity=identity)


@pytest.mark.parametrize('fault', ['missing', 'foreign_channel', 'foreign_peer', 'stale_peer',
    'epoch', 'generation', 'target', 'operation', 'replay', 'command'])
def test_cpu_command_inspection_refuses_missing_foreign_and_stale_channels(cpu_inspection_owner, monkeypatch, fault):
    from astrid.core.execution import process_group as pg
    case = cpu_inspection_owner; cb = case.cb
    monkeypatch.setattr(pg, 'popen_owned_process', lambda *a, **kw: pytest.fail('refusal spawned a helper'))
    monkeypatch.setattr(subprocess, 'run', lambda *a, **kw: pytest.fail('inspection used a local fallback'))
    if fault == 'missing':
        monkeypatch.delenv(cb._COMMAND_INVENTORY_FD, raising=False)
        with pytest.raises(cb.CustodyError, match='requires its original owner'):
            cb._inventory_load_commands('helper', case.executable)
    elif fault == 'foreign_channel':
        with pytest.raises(cb.CustodyError, match='original host channel'):
            case.owner._execute(case.frame, object())
    elif fault in {'foreign_peer', 'stale_peer'}:
        if fault == 'stale_peer':
            case.owner._authenticate(case.broker.operation_channel)
        case.identity['birth_id'] = 'changed'
        with pytest.raises(cb.CustodyError, match='original root|custody changed'):
            case.owner._execute(case.frame, case.broker.operation_channel)
    else:
        if fault in {'epoch', 'generation', 'target'}:
            case.frame['binding'][{'epoch': 'owner_epoch'}.get(fault, fault)] = 'changed'
        elif fault == 'command':
            case.frame['command'] = 'execute_arbitrary_command'
        elif fault == 'operation':
            case.frame['operation_id'] = 2
        else:
            case.owner.last_operation = 1
        with pytest.raises(cb.CustodyError, match='invalid binding'):
            case.owner._execute(case.frame, case.broker.operation_channel)
    assert not case.owner.helpers and case.owner.pending is None


@pytest.mark.parametrize('fault', ['source', 'source_marker', 'binary', 'binary_alias', 'tool', 'selection', 'image'])
def test_cpu_command_inspection_refuses_source_and_binary_drift(cpu_inspection_owner, monkeypatch, fault):
    from astrid.core.execution import declared_executables as de, process_group as pg
    case = cpu_inspection_owner
    monkeypatch.setattr(pg, 'popen_owned_process', lambda *a, **kw: pytest.fail('drift spawned a helper'))
    if fault == 'source':
        case.source.rename(case.source.with_name('retained-source')); case.source.mkdir()
        with pytest.raises(case.cb.CustodyError, match='source checkout changed'):
            case.launch.policy(case.launch.environment, str(case.source.parent))
    elif fault == 'source_marker':
        (case.source / '.git').write_text('changed marker')
        with pytest.raises(de.ExecutableAdmissionError, match='artifact replaced'):
            case.owner._validate_policy(str(case.source), case.owner.policy['cwd'], case.launch.environment, 'revision')
    else:
        if fault == 'binary': case.executable.write_bytes(b'changed executable')
        elif fault == 'tool': case.tool.write_bytes(b'changed reader')
        elif fault == 'binary_alias':
            case.executable.rename(case.executable.with_name('retained-helper'))
            case.executable.symlink_to(case.executable.with_name('retained-helper'))
        elif fault == 'selection': case.frame['selection'] = 'undeclared'
        else: case.frame['image'] = str(case.tool)
        with pytest.raises(de.ExecutableAdmissionError):
            case.owner._execute(case.frame, case.broker.operation_channel)
    assert not case.owner.helpers and case.owner.pending is None


def test_cpu_command_inspection_typed_channel_retains_fixed_helpers_and_original_wait(cpu_inspection_owner, monkeypatch):
    from astrid.core.execution import process_group as pg
    case = cpu_inspection_owner; cb = case.cb
    request_read, request_write = os.pipe(); reply_read, reply_write = os.pipe()
    server = cb._PipeChannel(request_read, reply_write)
    descriptor = cb._canonical([cb._pipe_identity(reply_read, os.O_RDONLY),
        cb._pipe_identity(request_write, os.O_WRONLY)]).decode()
    case.broker.operation_channel = server
    events = []
    class Helper:
        _astrid_custody = SimpleNamespace(_observer=None)
        def __init__(self):
            self.pid = 4000 + len(events)
            for name in ('stdout', 'stderr'):
                read, write = os.pipe(); os.close(write)
                setattr(self, name, os.fdopen(read, 'rb', buffering=0))
        def poll(self):return 0
        def wait(self, timeout):events.append(('wait', self)); return 0
    def spawn(argv, **kwargs):
        assert argv == [str(case.tool), '-l', str(case.executable)]
        assert kwargs['env'] == {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}
        assert kwargs['cwd'] == case.owner.policy['cwd'] and kwargs['_delegate_inventory'] is False
        helper = Helper(); events.append(('spawn', helper)); return helper
    monkeypatch.setattr(pg, 'popen_owned_process', spawn)
    monkeypatch.setattr(pg, 'verify_tree_absent', lambda helper: events.append(('closure', helper)))
    monkeypatch.setenv(cb._COMMAND_INVENTORY_FD, descriptor)
    case.owner.released.set(); case.owner.start()
    key = (os.getpid(), descriptor)
    try:
        for operation in (1, 2):
            result = cb._inventory_load_commands('helper', case.executable)
            assert result.returncode == 0 and result.stdout == result.stderr == ''
            assert case.owner.last_operation == operation and case.owner.pending is None
        assert list(case.owner.helpers) == [1, 2]
        for helper in case.owner.helpers.values():
            assert [('spawn', helper), ('wait', helper), ('closure', helper)] == [e for e in events if e[1] is helper]
    finally:
        client = cb._COMMAND_CLIENTS.pop(key, None)
        if client is not None: client.channel.close()
        else:
            os.close(reply_read); os.close(request_write)
        case.owner.finish(cancel=True, timeout=2)
    assert case.owner.done.is_set() and case.owner.error is None and case.owner.channel_closed


def test_host_only_observation_rejects_missing_original_handle():
    from test_local_worker import host_only_profile_case
    with pytest.raises(ConflictError, match="original retained handle"):
        OSProcessInspector(host_only_profile_case()).observe(None)


def test_host_only_custody_scope_is_private_before_real_authority_open(tmp_path):
    from runtime_protocol.local_worker_composition import _create_host_custody_scope
    from banodoco_local.custody_broker import _open_authority_scope_lock
    scope=tmp_path/'new-parent'/'operation'
    _create_host_custody_scope(scope)
    assert scope.stat().st_mode & 0o777 == 0o700
    descriptor=_open_authority_scope_lock(scope)
    os.close(descriptor)


@pytest.mark.parametrize('mode',[0o700,0o755])
def test_host_only_custody_scope_collision_retains_existing_bytes(tmp_path,mode):
    from runtime_protocol.local_worker_composition import _create_host_custody_scope
    scope=tmp_path/'operation';scope.mkdir(mode=mode);scope.chmod(mode)
    evidence=scope/'retained';evidence.write_bytes(b'original obligation')
    before=scope.stat()
    with pytest.raises(ConflictError,match='already exists'):
        _create_host_custody_scope(scope)
    after=scope.stat()
    assert (after.st_ino,after.st_mode)==(before.st_ino,before.st_mode)
    assert evidence.read_bytes()==b'original obligation'


def test_host_only_custody_scope_alias_never_mutates_target(tmp_path):
    from runtime_protocol.local_worker_composition import _create_host_custody_scope
    target=tmp_path/'target';target.mkdir()
    alias=tmp_path/'alias';alias.symlink_to(target,target_is_directory=True)
    with pytest.raises(ConflictError,match='not canonical'):
        _create_host_custody_scope(alias/'operation')
    assert not list(target.iterdir())


def test_host_only_custody_scope_wrong_owner_never_grants_authority(tmp_path,monkeypatch):
    from runtime_protocol.local_worker_composition import _create_host_custody_scope
    scope=tmp_path/'operation'
    original_uid=os.getuid()
    monkeypatch.setattr(os,'getuid',lambda:original_uid+1)
    with pytest.raises(ConflictError,match='not owner-only'):
        _create_host_custody_scope(scope)
    assert scope.stat().st_uid==original_uid
    assert not list(scope.iterdir())


def _host_only_cleanup_case(tmp_path, monkeypatch, case):
    from test_local_worker import host_only_profile_case
    from runtime_protocol import local_worker_composition as module
    profile = host_only_profile_case()
    preparer = CrossProcessWorkerPreparer(profile=profile, config={}, environment={})
    calls, sent = [], []
    state = {"exit": 120 if case == "terminal120" else 7 if case == "exited" else None}
    class Retained:
        def poll(self):
            calls.append("poll")
            if case == "missing_wait": raise ChildProcessError("missing original wait")
            return state["exit"]
        def verify(self):
            calls.append("verify")
            return {"pid": 42, "birth_id": "birth"}
        def wait(self, timeout):
            calls.append(("wait", timeout))
            if case in {"wait_timeout", "kill"} and signal.SIGKILL not in calls:
                raise TimeoutError()
            if case == "wait_timeout": raise TimeoutError()
            state["exit"] = -9 if signal.SIGKILL in calls else 0
            return state["exit"]
    def send(channel, request):
        sent.append(request)
        if case == "broken_pipe": raise BrokenPipeError("secret is not logged")
    def receive(channel):
        if case == "eof": raise EOFError()
        if case in {"unresolved", "wait_timeout", "missing_wait"}: return {"status": "unresolved"}
        return {**{k: v for k, v in sent[-1].items() if k != "command"}, "status": "cleaned", "cleanup": {"host_children": "absent"}}
    broker = SimpleNamespace(set_cleanup_deadline=lambda d: calls.append("deadline"),
        role_authority=SimpleNamespace(reference=lambda: {"role": "host"}),
        signal=lambda sig, **kw: calls.append(sig))
    channel = SimpleNamespace(settimeout=lambda t: None, close=lambda: calls.append("close"))
    handle = _PreparedWorker(SimpleNamespace(pid=42), "birth", channel, {}, tmp_path / "config",
        retained=Retained(), broker=broker, host_only=True, activation=channel,
        preparation={"version": "runtime.local-execution-preparation/v1", "operation_id": "op", "channel_id": "ch", "owner_epoch": "epoch"},
        custody_scope=str(tmp_path))
    preparer._active = handle
    monkeypatch.setattr(module, "_frame_send", send)
    monkeypatch.setattr(module, "_frame_receive", receive)
    monkeypatch.setattr(preparer, "_host_only_report", lambda h: pytest.fail("cleanup required a live report"))
    return preparer, handle, calls, sent, state


@pytest.mark.parametrize("case", ["ack", "unresolved", "broken_pipe", "eof", "exited", "wait_timeout", "missing_wait", "kill"])
def test_host_only_cleanup_always_reaches_original_wait_and_keeps_graph_failure(tmp_path, monkeypatch, case):
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, case)
    if case in {"ack", "kill"}:
        preparer.abort(handle)
        assert handle.closed and preparer._active is None and handle.cleanup_acknowledged
        preparer.abort(handle)
    else:
        with pytest.raises(ConflictError, match="unresolved"):
            preparer.abort(handle)
        assert preparer._active is handle and not handle.closed and preparer.cleanup_uncertain
        if case not in {"wait_timeout", "missing_wait"}:
            assert handle.original_host_wait is not None
        assert not handle.cleanup_acknowledged
    if case == "exited": assert not sent and signal.SIGTERM not in calls and handle.original_host_wait == 7
    elif case == "ack": assert signal.SIGTERM not in calls and handle.original_host_wait == 0
    elif case != "missing_wait": assert signal.SIGTERM in calls
    if case in {"kill", "wait_timeout"}: assert signal.SIGKILL in calls
    assert preparer.shutdown_timeout_seconds >= 3 * max(1, preparer.cleanup_timeout_seconds) + 1


def test_host_only_original_child_exit_is_retained_wait_not_absence(tmp_path):
    from runtime_protocol.local_execution_supervisor import RetainedProcess
    child = subprocess.Popen([sys.executable, "-I", "-c", "raise SystemExit(17)"])
    retained = RetainedProcess(child)
    assert retained.wait(3) == 17
    assert retained.poll() == 17 and child.returncode == 17


def test_preparation_diagnostic_keeps_actual_refusal_and_hashes_arbitrary_values():
    from runtime_protocol.local_worker_composition import _preparation_diagnostic
    frame = {"version": "runtime.local-execution-preparation/v1", "status": "unresolved", "error_code": "preparation_unresolved", "operation_id": "SECRET", "unknown": "TOKEN"}
    report = _preparation_diagnostic(frame, {"status": "prepared", "processes": {}, "operation_id": "expected"})
    assert report["status"] == "unresolved" and report["error_code"] == "preparation_unresolved"
    assert report["missing_fields"] == ["processes"] and report["differing_fields"] == ["operation_id", "status"]
    assert "unknown" in report["extra_fields"]
    assert "SECRET" not in json.dumps(report) and "TOKEN" not in json.dumps(report)
class _MemoryFrameChannel:
    def __init__(self, incoming=b'', *, fragment=4096, dispatch=None):
        self.incoming = bytearray(incoming)
        self.fragment = fragment
        self.dispatch = dispatch
        self.sent = []
        self.closed = False

    def recv(self, size):
        count = min(size, self.fragment, len(self.incoming))
        data = bytes(self.incoming[:count])
        del self.incoming[:count]
        return data

    def sendall(self, data):
        self.sent.append(data)
        if self.dispatch is not None:
            self.incoming.extend(self.dispatch(data))

    def settimeout(self, timeout):
        pass

    def close(self):
        self.closed = True

    def fileno(self):
        return 42


@pytest.fixture
def qualified_preparation_frame():
    from dataclasses import replace
    from test_local_worker import host_only_profile_case
    from runtime_protocol.local_worker import _selected_profile_payload
    from runtime_protocol.local_execution_supervisor import host_prepare_request
    root = os.environ.get('J_FRAME_EVIDENCE_ROOT')
    if not root:
        pytest.skip('select retained qualified J profile and public source evidence')
    root = Path(root)
    qualification = json.loads((root/'profile-qualification.json').read_text())
    path = Path(qualification['profile_path'])
    content = path.read_bytes()
    assert hashlib.sha256(content).hexdigest() == qualification['profile_sha256'] == '4b56987a482aec3a104b50ac3a21a25ff7b3e28cecd98782a2b9ad98c1ad87af'
    document = json.loads(content)
    allocation = json.loads((root/'allocation.json').read_text())
    runtime_path = root/'runtime-catalogue-readiness-continuation.json'
    assert hashlib.sha256(runtime_path.read_bytes()).hexdigest() == '2cfa1d8a431987a412193875f60c68b0935f6596a762642a976cef90c8a72687'
    runtime = json.loads(runtime_path.read_text())['runtime']
    launch = {name: document[name] for name in ('source_checkout', 'pack_root', 'boot_manifest_path',
        'boot_manifest_hash', 'capability_matrix', 'environment', 'max_concurrency', 'selected_actions')}
    fields = {name: document[name] for name in ('profile_id', 'machine_id', 'host_artifact_digest',
        'session_config_digest', 'profile_revision', 'profile_digest', 'release_digest', 'host_protocol', 'host_os_artifact_digest')}
    profile = replace(host_only_profile_case(), **fields, workspace_uuid=qualification['realm_id'],
        realm_root=Path(allocation['paths']['realm_root']), support_root=Path(allocation['paths']['support_root']),
        host_executable=Path(document['host_executable']), host_os_executable=Path(document['host_os_executable']), host_launch=launch)
    epoch = runtime['runtime_instance_id']
    owner = dict(pid=runtime['pid'], uid=os.getuid(), birth_id=runtime['process_birth_id'],
        runtime_instance_id=epoch, coordinator_epoch=epoch)
    request = host_prepare_request(operation_id='a'*32, channel_id='b'*32, owner_epoch=epoch,
        runtime_owner=owner, profile=_selected_profile_payload(profile),
        custody_scope=str(profile.support_root/'local-execution-custody'/('a'*32)))
    selection = request['profile']['host_launch']['selected_actions']['chiptune.compose']
    assert selection == document['selected_actions']['chiptune.compose']
    assert len(selection['distributions']['numpy']['files']) == 1040
    assert len(json.dumps(selection, sort_keys=True, separators=(',', ':')).encode()) == 111367
    return SimpleNamespace(profile=profile, request=request, owner=owner, document=document)


@pytest.fixture
def sdk_preparation_receiver(qualified_preparation_frame, monkeypatch):
    import copy
    from astrid.core.execution import generic_host as host, custody_broker, hosted_contract
    from runtime_protocol.verified_host_launch import raw_digest
    fixture = qualified_preparation_frame
    request = fixture.request
    preparation = host.LocalExecutionPreparation(operation_id=request['operation_id'], channel_id=request['channel_id'])
    actor = SimpleNamespace(verify=lambda: dict(fixture.owner))
    preparation._retained_relay_actor = actor
    preparation._hosted_binding = {**{name: request[name] for name in ('operation_id', 'channel_id', 'owner_epoch')},
        'profile_digest': hosted_contract.digest(hosted_contract.canonical(request['profile'])),
        'scope': request['custody_scope'], 'generation': 1}
    class Authority:
        def __init__(self, *args):
            pass
        def reference(self):
            return {'generation': 1, 'target': {'pid': os.getpid()}}
        def verify_reference(self, reference, *, expected_actor, owner_epoch):
            assert expected_actor == fixture.owner
            assert owner_epoch == request['owner_epoch']
    monkeypatch.setattr(custody_broker, 'RoleCustodyAuthority', Authority)
    monkeypatch.setattr(host, 'process_birth_identity', lambda *args: 'offline-host-birth')
    monkeypatch.setattr(host, '_RETAINED_ACTION_LAUNCH', {
        'profile_digest': raw_digest(request['profile']),
        'actions': copy.deepcopy(request['profile']['host_launch']['selected_actions'])}, raising=False)
    journals = []
    monkeypatch.setattr(preparation, '_acquire_handoff_journal', lambda scope: journals.append(scope) or True)
    return SimpleNamespace(host=host, preparation=preparation, fixture=fixture, journals=journals)


def test_preparation_frame_full_numpy_inventory_reaches_real_sdk_dispatch(sdk_preparation_receiver):
    from runtime_protocol import local_worker_composition as module
    from runtime_protocol.local_execution_supervisor import FRAME_LIMIT
    receiver = sdk_preparation_receiver
    wire = module._prepare_frame_encode(receiver.fixture.request)
    assert module.CONTROL_FRAME_LIMIT < len(wire) < FRAME_LIMIT
    frame = receiver.host._read_activation_frame(_MemoryFrameChannel(wire, fragment=31), limit=FRAME_LIMIT)
    assert frame == receiver.fixture.request
    assert module._frame_encode(frame) == wire
    reply = receiver.preparation.dispatch(frame)
    assert reply['status'] == 'prepared'
    assert reply['operation_id'] == frame['operation_id']
    assert reply['channel_id'] == frame['channel_id']
    assert receiver.preparation._request == frame
    assert len(receiver.journals) == 1
    print('QUALIFIED_NUMPY_FRAME', json.dumps({'wire_bytes': len(wire), 'sha256': hashlib.sha256(wire).hexdigest(),
        'numpy_files': 1040, 'selection_bytes': 111367, 'private_ids': 'same-length offline placeholders'}))


def test_preparation_frame_actual_sdk_control_reader_uses_large_bound(sdk_preparation_receiver, monkeypatch):
    from runtime_protocol import local_worker_composition as module
    from astrid.core.execution import custody_broker
    receiver = sdk_preparation_receiver
    channel = _MemoryFrameChannel(module._prepare_frame_encode(receiver.fixture.request), fragment=43)
    actor = receiver.preparation._retained_relay_actor
    monkeypatch.setattr(receiver.host.socket, 'socket', lambda **kwargs: channel)
    monkeypatch.setattr(custody_broker.AuthenticatedCleanupActor, 'private_peer', staticmethod(lambda control: actor))
    thread = receiver.preparation.serve_control(42)
    thread.join(5)
    assert not thread.is_alive() and channel.closed
    assert len(channel.sent) == 1
    reply = module._frame_receive(_MemoryFrameChannel(channel.sent[0], fragment=11))
    assert reply['status'] == 'prepared'
    assert receiver.preparation._request == receiver.fixture.request


@pytest.mark.parametrize("failure", [None, "transport", "cleanup", "reporter"])
def test_preparation_frame_sender_sends_same_preflight_bytes(sdk_preparation_receiver, monkeypatch, capsys, failure):
    import io
    from runtime_protocol import local_worker_composition as module, local_execution_supervisor, verified_host_launch
    import banodoco_local.custody_broker as custody
    import banodoco_local.hosted_contract as hosted
    receiver = sdk_preparation_receiver
    fixture = receiver.fixture
    events = []
    encoded = []
    original_encode = module._prepare_frame_encode
    def encode(value):
        frame = original_encode(value)
        encoded.append(frame)
        events.append('preflight')
        return frame
    def dispatch(wire):
        events.append('send')
        request = receiver.host._read_activation_frame(_MemoryFrameChannel(wire, fragment=37), limit=1048576)
        return module._frame_encode(receiver.preparation.dispatch(request))
    control = _MemoryFrameChannel(dispatch=dispatch)
    activation = _MemoryFrameChannel()
    child = SimpleNamespace(pid=os.getpid())
    identity = {'pid': child.pid, 'uid': os.getuid(), 'birth_id': 'offline-host-birth'}
    class Payload(io.BytesIO):
        def fileno(self):
            return 84
    class Verifier:
        def __init__(self, **kwargs):
            pass
        def verify(self, **kwargs):
            assert kwargs['preparation'] == fixture.request
            return object()
        def claim(self, proof, **kwargs):
            return kwargs['host_argv'], b'{}'
        def bind_child(self, proof, **kwargs):
            assert kwargs['child'] is child
        def verify_child(self, proof, **kwargs):
            assert kwargs['child'] is child
    class Retained:
        def __init__(self, process):
            assert process is child
        def bind_actor(self):
            assert 'sealed' in events
        def verify(self):
            return dict(identity)
    class Broker:
        def __init__(self, **kwargs):
            events.append('broker')
            assert events.index('preflight') < events.index('custody')
            assert kwargs['owner_epoch'] == fixture.request['owner_epoch']
            self.role_authority = SimpleNamespace(reference=lambda: {'role': 'host'})
        def create_hosted_launch(self, request):
            assert request == fixture.request
            return SimpleNamespace(parents={'control': control, 'activation': activation},
                children={'control': control, 'activation': activation}, pass_fds=(),
                environment=lambda *args, **kwargs: {}, close_children=lambda: None)
        def child_environment(self, *args, **kwargs):
            return {}
        def wait_until_sealed(self):
            events.append('sealed')
    def mkdir(path, *args, **kwargs):
        assert path == fixture.profile.support_root/'host-output'
        events.append('output-directory')
    def spawn(*args, **kwargs):
        events.append('spawn')
        return child
    monkeypatch.setattr(module, '_prepare_frame_encode', encode)
    monkeypatch.setattr(module, '_create_host_custody_scope', lambda scope: events.append('custody'))
    monkeypatch.setattr(module, '_installed_host_release', lambda *args: {})
    monkeypatch.setattr(receiver.host, '_launch_needs_command_inspection', lambda *args: False)
    monkeypatch.setattr(custody, 'RoleBoundCustodyBroker', Broker)
    monkeypatch.setattr(custody, 'default_process_identity', lambda pid: dict(fixture.owner))
    monkeypatch.setattr(custody, 'custody_wrapper_argv', lambda path: [path])
    monkeypatch.setattr(custody, '_atomic_owner_json', lambda *args: None)
    monkeypatch.setattr(hosted, 'readonly_payload', Payload)
    monkeypatch.setattr(verified_host_launch, 'TrustedLocalHostLaunchVerifier', Verifier)
    monkeypatch.setattr(local_execution_supervisor, 'RetainedProcess', Retained)
    monkeypatch.setattr(module.os, 'dup2', lambda *args, **kwargs: None)
    monkeypatch.setattr(module.Path, 'mkdir', mkdir)
    monkeypatch.setattr(module.subprocess, 'Popen', spawn)
    config = {**fixture.profile.host_launch, 'runtime_instance_id': fixture.request['owner_epoch'],
        'runtime_endpoint': 'http://127.0.0.1:1', 'credential_file': '/offline-unread-credential', 'ready_file': '/offline-ready'}
    preparer = CrossProcessWorkerPreparer(profile=fixture.profile, config=config, environment={})
    if failure is not None:
        primary = RuntimeError("private-primary-transport-value")
        before_cleanup = []
        monkeypatch.setattr(module, "_frame_receive", lambda *_a, **_k: (_ for _ in ()).throw(primary))
        def abort(handle):
            events.append("abort")
            before_cleanup.append(capsys.readouterr().err)
            if failure == "cleanup":
                raise TimeoutError("private-cleanup-value")
        monkeypatch.setattr(preparer, "abort", abort)
        if failure == "reporter":
            monkeypatch.setattr(module, "_report_start_failure", lambda *_a, **_k: (_ for _ in ()).throw(OSError("private-reporter-value")), raising=False)
        with pytest.raises(RuntimeError) as caught:
            preparer.prepare(fixture.profile, operation_id=fixture.request['operation_id'], channel_id=fixture.request['channel_id'])
        assert caught.value is primary
        assert events.count("spawn") == events.count("abort") == 1
        if failure != "reporter":
            assert '"event":"local_worker_start_failed"' in before_cleanup[0]
            assert '"phase":"host_only_prepare"' in before_cleanup[0]
            assert "private-primary-transport-value" not in before_cleanup[0]
        if failure == "cleanup":
            assert preparer.cleanup_uncertain
        assert "private-cleanup-value" not in capsys.readouterr().err
        return
    handle = preparer.prepare(fixture.profile, operation_id=fixture.request['operation_id'], channel_id=fixture.request['channel_id'])
    assert control.sent[0] is encoded[0]
    assert len(encoded) == 1
    assert handle.preparation == fixture.request == receiver.preparation._request
    assert events.index('preflight') < events.index('custody') < events.index('broker') < events.index('spawn') < events.index('send')
    assert handle.report_value['profile_binding_digest'] == local_execution_supervisor.digest(fixture.request['profile'])


@pytest.mark.parametrize('field', ['operation', 'channel', 'owner', 'epoch', 'profile', 'closure'])
def test_preparation_frame_binding_refusals_still_precede_journal(sdk_preparation_receiver, field):
    import copy
    from runtime_protocol import local_worker_composition as module
    from runtime_protocol.local_execution_supervisor import FRAME_LIMIT
    receiver = sdk_preparation_receiver
    request = copy.deepcopy(receiver.fixture.request)
    if field == 'operation': request['operation_id'] = 'foreign'
    elif field == 'channel': request['channel_id'] = 'foreign'
    elif field == 'owner': request['runtime_owner']['birth_id'] = 'foreign'
    elif field == 'epoch':
        request['owner_epoch'] = 'foreign'
        request['runtime_owner'].update(runtime_instance_id='foreign', coordinator_epoch='foreign')
    elif field == 'profile': request['profile']['profile_digest'] = _digest('0')
    else:
        files = request['profile']['host_launch']['selected_actions']['chiptune.compose']['distributions']['numpy']['files']
        files[next(iter(files))] = '0'*64
    frame = receiver.host._read_activation_frame(_MemoryFrameChannel(module._prepare_frame_encode(request)), limit=FRAME_LIMIT)
    with pytest.raises((receiver.host.HostError, RuntimeError)):
        receiver.preparation.dispatch(frame)
    assert receiver.preparation.result is None and not receiver.journals


@pytest.mark.parametrize('wire_size', [114291, 1048576])
def test_preparation_frame_exact_wire_limits_include_newline(wire_size):
    from astrid.core.execution import generic_host as host
    from runtime_protocol import local_worker_composition as module
    from runtime_protocol.local_execution_supervisor import FRAME_LIMIT
    value = {'value': ''}
    value['value'] = 'x'*(wire_size - len(module._frame_encode(value)))
    wire = module._prepare_frame_encode(value)
    assert len(wire) == wire_size and wire.endswith(b'\n')
    assert host._read_activation_frame(_MemoryFrameChannel(wire, fragment=257), limit=FRAME_LIMIT) == value
    if wire_size == FRAME_LIMIT:
        value['value'] += 'x'
        with pytest.raises(ConflictError, match='preparation frame is too large'):
            module._prepare_frame_encode(value)
        with pytest.raises(host.HostError, match='too large'):
            host._read_activation_frame(_MemoryFrameChannel(module._frame_encode(value)), limit=FRAME_LIMIT)


def test_preparation_frame_ordinary_controls_remain_64k(monkeypatch):
    from astrid.core.execution import generic_host as host
    from runtime_protocol import local_worker_composition as module
    value = {'command': 'prepare_local_execution', 'limit': 1048576, 'value': ''}
    value['value'] = 'x'*(module.CONTROL_FRAME_LIMIT - len(module._frame_encode(value)))
    channel = _MemoryFrameChannel()
    module._frame_send(channel, value)
    assert len(channel.sent[0]) == 65536
    assert module._frame_receive(_MemoryFrameChannel(channel.sent[0], fragment=19)) == value
    assert host._read_activation_frame(_MemoryFrameChannel(channel.sent[0], fragment=17)) == value
    monkeypatch.setenv('CONTROL_FRAME_LIMIT', '1048576')
    value['value'] += 'x'
    with pytest.raises(ConflictError, match='control frame is too large'):
        module._frame_send(channel, value)
    assert len(channel.sent) == 1
    with pytest.raises(ConflictError, match='too large'):
        module._frame_receive(_MemoryFrameChannel(module._frame_encode(value)))
    with pytest.raises(host.HostError, match='too large'):
        host._read_activation_frame(_MemoryFrameChannel(module._frame_encode(value)))


@pytest.mark.parametrize('wire', [b'', b'{"missing":"newline"}', b'{"invalid":"\xff"}\n',
    b'{broken}\n', b'{"key":1,"key":2}\n', b'{"nested":{"key":1,"key":2}}\n',
    b'{"value":1e10000}\n', b'{"value":NaN}\n', b'{"value":Infinity}\n',
    b'{"value":-Infinity}\n', b'{}\n{}\n', b'{}\ntrailing', b'[]\n'])
def test_preparation_frame_malformed_and_unsolicited_input_is_refused(wire):
    from astrid.core.execution import generic_host as host
    from runtime_protocol import local_worker_composition as module
    from runtime_protocol.local_execution_supervisor import FRAME_LIMIT
    with pytest.raises((host.HostError, ValueError)):
        host._read_activation_frame(_MemoryFrameChannel(wire), limit=FRAME_LIMIT)
    with pytest.raises(ConflictError):
        module._frame_receive(_MemoryFrameChannel(wire))


def test_preparation_frame_oversize_fails_before_any_start_obligation(qualified_preparation_frame, monkeypatch, tmp_path):
    import copy
    from dataclasses import replace
    from runtime_protocol import local_worker_composition as module, local_execution_supervisor
    import banodoco_local.custody_broker as custody
    from astrid.core.execution import custody_broker as inspection_custody
    from astrid.core.execution import generic_host as host
    fixture = qualified_preparation_frame
    launch = copy.deepcopy(fixture.profile.host_launch)
    launch['environment']['PATH'] = 'x'*local_execution_supervisor.FRAME_LIMIT
    profile = replace(fixture.profile, host_launch=launch, support_root=tmp_path/'unused-support',
        session_config_digest=local_execution_supervisor.digest(launch))
    preparer = CrossProcessWorkerPreparer(profile=profile, config={'runtime_instance_id': fixture.request['owner_epoch']}, environment={})
    def forbidden(*args, **kwargs):
        pytest.fail('oversize preparation created a start obligation')
    monkeypatch.setattr(custody, 'default_process_identity', lambda pid: dict(fixture.owner))
    monkeypatch.setattr(inspection_custody, 'default_process_identity', lambda pid: dict(fixture.owner))
    monkeypatch.setattr(module, '_create_host_custody_scope', forbidden)
    monkeypatch.setattr(host, '_launch_needs_command_inspection', forbidden)
    monkeypatch.setattr(custody, 'RoleBoundCustodyBroker', forbidden)
    monkeypatch.setattr(inspection_custody, 'RoleBoundCustodyBroker', forbidden)
    monkeypatch.setattr(module.subprocess, 'Popen', forbidden)
    with pytest.raises(ConflictError, match='preparation frame is too large'):
        preparer.prepare(profile, operation_id=fixture.request['operation_id'], channel_id=fixture.request['channel_id'])
    assert preparer._active is None
    assert not profile.support_root.exists()


def test_preparation_frame_inspection_owner_change_refused_before_custody(qualified_preparation_frame, monkeypatch):
    from runtime_protocol import local_worker_composition as module
    import banodoco_local.custody_broker as custody
    from astrid.core.execution import custody_broker as inspection_custody, generic_host as host
    fixture = qualified_preparation_frame
    def forbidden(*args, **kwargs):
        pytest.fail('changed owner created a start obligation')
    monkeypatch.setattr(custody, 'default_process_identity', lambda pid: dict(fixture.owner))
    monkeypatch.setattr(inspection_custody, 'default_process_identity', lambda pid: {**fixture.owner, 'birth_id': 'foreign'})
    monkeypatch.setattr(host, '_launch_needs_command_inspection', lambda *args: True)
    monkeypatch.setattr(module, '_create_host_custody_scope', forbidden)
    monkeypatch.setattr(inspection_custody, 'RoleBoundCustodyBroker', forbidden)
    monkeypatch.setattr(module.subprocess, 'Popen', forbidden)
    preparer = CrossProcessWorkerPreparer(profile=fixture.profile,
        config={'runtime_instance_id': fixture.request['owner_epoch']}, environment={})
    with pytest.raises(ConflictError, match='original Runtime owner changed'):
        preparer.prepare(fixture.profile, operation_id=fixture.request['operation_id'], channel_id=fixture.request['channel_id'])
    assert preparer._active is None


def test_selected_action_installed_release_projects_real_verified_host_binding(tmp_path,monkeypatch):
    """Offline installed-record/verifier join; no profile or Host is started."""
    import copy,importlib.metadata,json,os,sys
    from pathlib import Path
    from types import SimpleNamespace
    from runtime_protocol import verified_host_launch as gate
    from runtime_protocol.local_worker import _selected_profile_payload
    from runtime_protocol.local_worker_composition import _installed_host_release
    from test_local_worker import host_only_profile_case
    # Reuse the same immutable exact-artifact fixture producer used by the
    # child tests without enabling a real installed profile/setup path.
    from test_verified_host_launch import selected_action_installation
    class Factory:
        def mktemp(self,name):
            directory=tmp_path/name;directory.mkdir();return directory
    f=selected_action_installation.__wrapped__(Factory())
    selected=_selected_profile_payload(host_only_profile_case())
    launch={**selected['host_launch'],'source_checkout':str(f.root),'pack_root':str(f.root/'astrid/packs'),
        'capability_matrix':str(f.matrix),'selected_actions':copy.deepcopy(f.actions)}
    selected.update(host_launch=launch,host_executable=os.path.abspath(sys.executable),
        host_artifact_digest='sha256:'+f.actions['generation.generate_speech']['interpreter']['sha256'],
        host_os_executable=str(Path(sys.executable).resolve()),
        host_os_artifact_digest='sha256:'+f.actions['generation.generate_speech']['interpreter']['sha256'],
        session_config_digest='sha256:'+gate.raw_digest(launch),release_digest='sha256:'+gate.raw_digest(f.closure['distributions']),
        host_protocol={'version':gate.CURRENT_ROLES_VERSION,'module':gate.HOST_MODULE,
            'source_closure_digest':gate.source_checkout_closure(f.root)['digest']})
    profile=SimpleNamespace(**selected)
    distributions={name:importlib.metadata.PathDistribution(f.root/(name.replace('-','_')+'-1.0.dist-info'))
                   for name in ('astrid','banodoco-workspace-runtime')}
    original=importlib.metadata.distribution
    monkeypatch.setattr(importlib.metadata,'distribution',lambda name:distributions[name] if name in distributions else original(name))
    monkeypatch.setattr(sys,'prefix',str(f.root.parent))
    config={**launch,'support_root':selected['support_root']}
    record=_installed_host_release(profile,config)
    verifier=gate.TrustedLocalHostLaunchVerifier(installed_release=record)
    arguments=dict(preparation={'profile':_selected_profile_payload(profile)},config=config,
        host_argv=[sys.executable,'-m',gate.HOST_MODULE],environment={
            'ASTRID_OUTPUT_ROOT':str(Path(selected['support_root'])/'host-output'),'BANODOCO_LOCAL_DATA_ROOT':selected['realm_root']})
    proof=verifier.verify(**arguments)
    argv,data=verifier.claim(proof,**arguments,binding_fd=3)
    payload=json.loads(data)
    assert argv[1:3]==['-I','-S']
    assert payload['action_launch']['actions']==f.actions
    assert payload['action_launch']['profile_digest']==gate.raw_digest(arguments['preparation']['profile'])
    assert 'edge_tts' not in payload['mapping']
    assert set(f.closure['distributions'])==set(gate.HOST_DISTRIBUTIONS)
    (tmp_path/'verified-host-action-projection.json').write_bytes(gate.canonical(payload['action_launch']))


@pytest.mark.parametrize("case", ["terminal120", "ack"])
@pytest.mark.parametrize("logger_fails", [False, True])
def test_host_only_cleanup_retains_outcome_before_logger(tmp_path, monkeypatch, case, logger_fails):
    from runtime_protocol import local_worker_composition as module
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, case)
    handle.inspection_owner = SimpleNamespace(finish=lambda **kw: calls.append("inspection"))
    def log(*args):
        assert handle.cleanup_outcome["original_host_wait"] == (120 if case == "terminal120" else 0)
        assert handle.cleanup_outcome["inspection_owner_settled"] is True
        assert bool(preparer.cleanup_uncertain) == (case == "terminal120")
        if logger_fails:
            raise OSError("private-logger-value")
    monkeypatch.setattr(module._LOGGER, "warning", log)
    if case == "terminal120":
        with pytest.raises(ConflictError, match="acknowledgement unresolved") as caught:
            preparer.abort(handle)
        assert caught.value.details["reason"] == "child_cleanup_acknowledgement_unresolved"
        assert not handle.closed and preparer._active is handle and not sent
    else:
        preparer.abort(handle)
        assert handle.closed and preparer._active is None
    outcome = handle.cleanup_outcome
    assert outcome["child_cleanup_acknowledged"] == (case == "ack")
    assert outcome["complete_graph"] == (case == "ack")
    assert outcome["logging_status"] == ("failed" if logger_fails else "written")
    assert "private-logger-value" not in json.dumps(outcome)


def test_host_only_cleanup_channel_failure_keeps_refusal_after_good_ack(tmp_path, monkeypatch):
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, "ack")
    def close():
        calls.append("close")
        raise OSError("private-close-value")
    handle.control.close = close
    with pytest.raises(ConflictError, match="channel close unresolved") as caught:
        preparer.abort(handle)
    assert caught.value.details["reason"] == "cleanup_failed"
    assert handle.cleanup_outcome["child_cleanup_acknowledged"] is True
    assert handle.cleanup_outcome["original_host_wait"] == 0
    assert handle.cleanup_outcome["complete_graph"] is True
    assert handle.cleanup_outcome["secondary_error_codes"] == ["os_error", "os_error"]
    assert not handle.closed and preparer._active is handle and preparer.cleanup_uncertain
    assert calls.count("close") == 2
    assert "private-" not in json.dumps(handle.cleanup_outcome)


@pytest.mark.parametrize("case", ["ack", "kill", "unresolved", "wait_timeout"])
@pytest.mark.parametrize("logger_fails", [False, True])
def test_startup_primary_survives_actual_owner_cleanup_outcome(tmp_path, monkeypatch, case, logger_fails):
    from runtime_protocol.daemon import RuntimeDaemon
    from runtime_protocol import local_worker_composition as module
    from runtime_protocol.local_preparation_relay import unavailable
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, case)
    handle.inspection_owner = SimpleNamespace(finish=lambda **kw: calls.append("inspection"))
    if logger_fails:
        monkeypatch.setattr(module._LOGGER, "warning", lambda *args: (_ for _ in ()).throw(OSError("SECRET")))
    daemon = RuntimeDaemon.__new__(RuntimeDaemon)
    daemon.httpd = None
    daemon.service = None
    daemon.instance_id = "fixture"
    daemon.discovery = SimpleNamespace(clear=lambda instance: None)
    daemon._shutdown_http = lambda: None
    daemon.local_worker_launcher = SimpleNamespace(begin_shutdown=lambda: [handle],
        finish_shutdown=lambda handles: preparer.abort(handles[0]))
    # Serialized actual H004 boundary, with no credentials/handles/private paths.
    data = json.loads((Path(__file__).parent / "fixtures/h004-startup-boundary.json").read_text())
    primary = unavailable(data["primary"]["reason"])
    with pytest.raises(type(primary)) as caught:
        try:
            raise primary
        finally:
            daemon.__exit__(type(primary), primary, primary.__traceback__)
    assert caught.value is primary and primary.details["reason"] == data["primary"]["reason"]
    result = primary.local_worker_cleanup
    outcome = result["outcomes"][0]
    assert outcome["terminal"] == (case != "wait_timeout")
    assert outcome["graceful"] == (case == "ack")
    assert outcome["complete_graph"] == (case in {"ack", "kill"})
    assert outcome["child_cleanup_acknowledged"] == (case in {"ack", "kill"})
    assert outcome["inspection_owner_settled"] is True
    assert outcome["owner_settled"] == (case in {"ack", "kill"})
    assert outcome["logging_status"] == ("failed" if logger_fails else "written")
    if case == "kill":
        assert outcome["original_host_wait"] == -9 and not outcome["graceful"]
    if logger_fails: assert "logging" in outcome["secondary_error_stages"]
    if case in {"unresolved", "wait_timeout"}:
        assert result["status"] == "failed" and result["secondary_error_stage"] == "worker_cleanup"
        assert daemon.local_worker_launcher is not None
        assert daemon._local_worker_shutdown_handles == [handle] and preparer._active is handle
    else:
        assert result["status"] == "complete" and daemon.local_worker_launcher is None
    assert "SECRET" not in json.dumps(result)


def test_cleanup_without_primary_still_refuses_and_retains_outcome(tmp_path, monkeypatch):
    from runtime_protocol.daemon import RuntimeDaemon
    daemon = RuntimeDaemon.__new__(RuntimeDaemon)
    def fail(handles, set_stage):
        set_stage("worker_cleanup")
        raise ConflictError("private error")
    daemon._stop_owned = fail
    with pytest.raises(ConflictError): daemon.stop()
    assert daemon.local_worker_cleanup["status"] == "failed"
    assert daemon.local_worker_cleanup["secondary_error_stage"] == "worker_cleanup"


def test_retained_wait_deadline_is_distinct_from_lost_wait_ownership(monkeypatch):
    from runtime_protocol.local_execution_supervisor import RetainedProcess, RetainedWaitTimeout, RelayError
    retained = RetainedProcess(None)
    monkeypatch.setattr(retained, "poll", lambda: None)
    with pytest.raises(RetainedWaitTimeout, match="exit remains unresolved"):
        retained.wait(.001)
    assert issubclass(RetainedWaitTimeout, RelayError)
    missing = RelayError("retained child wait ownership is unknown")
    monkeypatch.setattr(retained, "poll", lambda: (_ for _ in ()).throw(missing))
    with pytest.raises(RelayError) as caught: retained.wait(0)
    assert caught.value is missing and not isinstance(missing, TimeoutError)


def test_ack_natural_exit_and_escalation_share_existing_total_deadline(tmp_path, monkeypatch):
    from runtime_protocol import local_worker_composition as module
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, "kill")
    clock = SimpleNamespace(now=0.0)
    monkeypatch.setattr(module, "time", SimpleNamespace(monotonic=lambda: clock.now))
    budgets = []
    def wait(timeout):
        assert timeout >= 0
        budgets.append(timeout)
        clock.now += timeout
        if signal.SIGKILL not in calls: raise TimeoutError()
        state["exit"] = -9
        return -9
    handle.retained.wait = wait
    handle.inspection_owner = SimpleNamespace(finish=lambda **kw: budgets.append(kw["timeout"]))
    preparer.abort(handle)
    total = 3 * max(1, preparer.cleanup_timeout_seconds)
    assert clock.now <= total and sum(budgets) <= total
    assert budgets[0] == max(1, preparer.cleanup_timeout_seconds) / 2
    assert handle.cleanup_outcome["original_host_wait"] == -9
    assert handle.cleanup_outcome["complete_graph"] and handle.cleanup_outcome["owner_settled"]
    assert not handle.cleanup_outcome["graceful"]
