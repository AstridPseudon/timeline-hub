"""E241: exact receiptless authority retirement, with historical process UNKNOWN."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest

from http_helpers import Api
from runtime_protocol.daemon import RuntimeDaemon, WORKER_ACTOR, WORKER_SCOPES
from runtime_protocol.errors import AuthorizationError, ConflictError, RuntimeErrorBase
from runtime_protocol.local_execution_handoff import FENCE_VERSION, write_protected
from runtime_protocol.store import RealmStore
from tests.test_remote_credential_generation import _task


@pytest.fixture
def daemon(tmp_path):
    RealmStore.initialize(tmp_path / "realm").close()
    d = RuntimeDaemon(tmp_path / "realm", support_root=tmp_path / "support",
                      production_worker_credentials=True).start()
    try:
        yield d
    finally:
        d.stop()


def _identity(d, token):
    # Same authenticated identity captured by RuntimeHandler._identity, without
    # carrying token bytes across the service admission boundary.
    with d.credentials._lock:
        value = d.credentials.require(token, "handshake")
        return {**value, "_credential_binding": d.credentials._sha256(token.encode()),
                "_credential_generation_digest": d.credentials._sha256(
                    d.credentials._paths(value["actor"])[2].read_bytes())}


def _owner(d):
    return _identity(d, d.token)


def _proof(d):
    return d.receiptless_worker_generation(identity=_owner(d))["binding"]


def _retire(d, proof):
    return d.retire_receiptless_worker_credential(proof, identity=_owner(d))


def _files(d):
    return {p.name: p.read_bytes() for p in d.credentials._paths(WORKER_ACTOR)
            if p.exists() and not p.is_symlink()}


def test_owner_http_retirement_once_preserves_unknown_and_no_process_receipt(daemon):
    d = daemon
    token = d.worker_token
    from banodoco_workspace_client import WorkspaceClient
    owner, worker = Api(d.endpoint, d.token), Api(d.endpoint, token)
    supported_owner = WorkspaceClient(d.endpoint, d.token)
    observation = supported_owner.get_receiptless_worker_credential_generation()
    proof = observation["binding"]
    assert observation["state"] == "committed"
    assert observation["historical_process_state"] == "UNKNOWN"
    assert token not in json.dumps(observation)
    for method, route, body in [
        ("GET", "credential-generation", None), ("POST", "retire-credential", proof),
    ]:
        with pytest.raises(RuntimeError) as denied:
            worker.request(method, "/v1/control/local-worker/" + route, body)
        assert denied.value.status == 401
    result = supported_owner.retire_receiptless_worker_credential(proof)
    assert result == {"state": "credential_authority_retired", "binding": proof,
                      "historical_process_state": "UNKNOWN"}
    assert supported_owner.retire_receiptless_worker_credential(proof) == result
    assert _files(d) == {}
    checkpoint = d._local_relinquish_state()
    assert checkpoint["state"] == "complete" and "receipt" not in checkpoint
    assert token not in d._local_relinquish_path().read_text()
    assert owner.request("GET", "/v1/control/local-worker/credential-generation")["state"] == "complete"
    with pytest.raises(AuthorizationError):
        d.credentials.load(token)
    with pytest.raises(RuntimeError) as unavailable:
        owner.request("GET", "/v1/control/local-worker/generation")
    assert unavailable.value.status == 404
    assert d.service.store.conn.execute("SELECT count(*) FROM events").fetchone()[0] == 0


@pytest.mark.parametrize("field", ["actor", "workspace_uuid", "realm_root", "support_root", "credential_generation_digest", "file_digests", "extra"])
def test_exact_request_mismatch_refuses_unchanged(daemon, field):
    d = daemon
    proof = copy.deepcopy(_proof(d))
    if field == "file_digests":
        proof[field]["astrid-pack-host.token"] = "sha256:" + "a" * 64
    else:
        proof[field] = "sha256:" + "b" * 64 if field.endswith("digest") else "foreign"
    before = _files(d)
    with pytest.raises(RuntimeErrorBase):
        _retire(d, proof)
    assert _files(d) == before and not d._local_relinquish_path().exists()


@pytest.mark.parametrize("mutation", ["rotation", "token", "metadata", "commit", "duplicate_metadata", "duplicate_commit", "bad_generation", "bad_actor", "scopes", "execution_binding", "qualified_activation", "local_launch_receipt"])
def test_changed_malformed_or_bound_generation_refuses(daemon, mutation):
    d = daemon
    proof = _proof(d)
    paths = d.credentials._paths(WORKER_ACTOR)
    if mutation == "rotation":
        d.credentials.provision(WORKER_ACTOR, list(WORKER_SCOPES), rotate=True)
    elif mutation in {"bad_actor", "scopes", "execution_binding", "qualified_activation", "local_launch_receipt"}:
        metadata = d.credentials.actor_metadata(WORKER_ACTOR)
        if mutation == "bad_actor":
            metadata["actor"] = "other"
        elif mutation == "scopes":
            metadata["scopes"] = ["admin"]
        else:
            metadata[mutation] = {}  # Presence, even malformed/empty, is a different lifecycle.
        d.credentials._publish(WORKER_ACTOR, d.worker_token, metadata)
    elif mutation == "bad_generation":
        value = json.loads(paths[2].read_bytes())
        value["generation"] = None
        paths[2].write_text(json.dumps(value))
    elif mutation.startswith("duplicate"):
        index = 1 if mutation == "duplicate_metadata" else 2
        original = paths[index].read_bytes()
        paths[index].write_bytes(b'{"actor":"forged",' + original[1:] if index == 1
                                 else b'{"generation":"forged",' + original[1:])
        if index == 1:
            value = json.loads(paths[2].read_bytes())
            value["metadata_sha256"] = d.credentials._sha256(paths[1].read_bytes())
            paths[2].write_text(json.dumps(value))
    else:
        paths[{"token": 0, "metadata": 1, "commit": 2}[mutation]].write_bytes(b"malformed")
    before = _files(d)
    with pytest.raises(RuntimeErrorBase):
        _retire(d, proof)
    assert _files(d) == before and not d._local_relinquish_path().exists()


@pytest.mark.parametrize("index", [0, 1, 2])
@pytest.mark.parametrize("fault", ["missing", "symlink", "hardlink", "permissions", "directory"])
def test_each_unsafe_file_refuses_without_cleanup(daemon, tmp_path, index, fault):
    d = daemon
    proof = _proof(d)
    path = d.credentials._paths(WORKER_ACTOR)[index]
    if fault == "missing":
        path.unlink()
    elif fault == "permissions":
        path.chmod(0o644)
    elif fault == "hardlink":
        os.link(path, tmp_path / "alias")
    else:
        data = path.read_bytes()
        path.unlink()
        if fault == "directory":
            path.mkdir()
        else:
            target = tmp_path / "alias"
            target.write_bytes(data)
            target.chmod(0o600)
            path.symlink_to(target)
    before = {p: (p.lstat(), p.read_bytes() if p.is_file() else None)
              for p in d.credentials._paths(WORKER_ACTOR) if p.exists() or p.is_symlink()}
    with pytest.raises(RuntimeErrorBase):
        _retire(d, proof)
    for p, (info, data) in before.items():
        assert p.lstat().st_ino == info.st_ino
        if data is not None:
            assert p.read_bytes() == data
    assert not d._local_relinquish_path().exists()


@pytest.mark.parametrize("kind,payload", [
    ("task.remote_activation_qualified", '{"activation_id":"active"}'),
    ("task.remote_activation_accepted", '{"activation_id":"active"}'),
    ("task.remote_activation_qualified", "malformed"),
    ("task.remote_activation_accepted", "[]"),
    ("task.remote_activation_revoked", '{"activation_id":null}'),
    ("task.remote_activation_revoked", '{"activation_id":""}'),
    ("task.remote_activation_revoked", '{"activation_id":"a","activation_id":"b"}'),
])
def test_activation_and_corrupt_history_refuse(daemon, kind, payload):
    d = daemon
    proof = _proof(d)
    task, _, _ = _task(d, "history")
    row = d.service.store.get_task(task)
    d.service.store._append_event(row["run"]["id"], task, kind, {})
    d.service.store.conn.execute("UPDATE events SET payload_json=? WHERE id=(SELECT max(id) FROM events)", (payload,))
    before = _files(d)
    with pytest.raises(ConflictError):
        _retire(d, proof)
    assert _files(d) == before and not d._local_relinquish_path().exists()


@pytest.mark.parametrize("obligation", ["running", "cancel_requested", "attempt", "reservation", "binding"])
def test_each_actor_work_obligation_refuses(daemon, obligation):
    d, s = daemon, daemon.service
    proof = _proof(d)
    task, _, _ = _task(d, "obligation")
    if obligation == "binding":
        s.store.conn.execute("UPDATE execution_bindings SET status='claimed', executor_id=? WHERE task_id=?", (WORKER_ACTOR, task))
    elif obligation in {"running", "cancel_requested"}:
        s.store.conn.execute("UPDATE tasks SET status=?, executor_id=? WHERE id=?", (obligation, WORKER_ACTOR, task))
    elif obligation == "reservation":
        s.store.conn.execute("INSERT INTO reservations(task_id,resource_key,lease_token,created_at,executor_id) VALUES (?,'gpu','lease','now',?)", (task, WORKER_ACTOR))
    else:
        s.store.conn.execute("INSERT INTO attempts(id,task_id,executor_id,lease_id,fence,runtime_epoch,lease_expires_at,settled) VALUES ('attempt',?,?,'lease',1,1,'later',0)", (task, WORKER_ACTOR))
    before = _files(d)
    with pytest.raises(ConflictError, match="outstanding"):
        _retire(d, proof)
    assert _files(d) == before and not d._local_relinquish_path().exists()


@pytest.mark.parametrize("fence", ["claim_held", "claim_corrupt", "relinquish", "relinquish_corrupt", "launcher", "launch_in_progress", "preparer"])
def test_unresolved_fences_and_launch_owners_refuse(daemon, fence):
    d = daemon
    proof = _proof(d)
    if fence == "claim_held":
        write_protected(d.service._local_claim_fence_path(), {
            "version": FENCE_VERSION, "state": "held", "workspace_uuid": d.service.realm["id"],
            "executor_incarnation": "inc", "credential_generation_digest": proof["credential_generation_digest"],
            "operation_id": "op", "handoff_id": "handoff", "intent_digest": "sha256:" + "a" * 64,
            "source_owner_epoch": "source", "target_owner_epoch": "target", "fence_generation": 1,
            "release_ack_digest": None,
        })
    elif fence == "claim_corrupt":
        write_protected(d.service._local_claim_fence_path(), {"broken": True})
    elif fence.startswith("relinquish"):
        write_protected(d._local_relinquish_path(), {"version": 1, "state": "fenced", "receipt": {}}
                        if fence == "relinquish" else {"broken": True})
    elif fence in {"launcher", "launch_in_progress"}:
        d.local_worker_launcher = SimpleNamespace(is_idle=lambda: False, close=lambda: None)
    else:
        d.local_worker_preparer = SimpleNamespace(current_handle=lambda: object())
    before = _files(d)
    checkpoint = d._local_relinquish_path().read_bytes() if d._local_relinquish_path().exists() else None
    with pytest.raises(RuntimeErrorBase):
        _retire(d, proof)
    assert _files(d) == before
    assert (d._local_relinquish_path().read_bytes() if d._local_relinquish_path().exists() else None) == checkpoint
    d.local_worker_launcher = None
    d.local_worker_preparer = None


@pytest.mark.parametrize("operation", ["register", "capability", "claim", "write"])
def test_authenticated_request_waiting_for_mutex_cannot_mutate_after_retirement(daemon, operation):
    d, s = daemon, daemon.service
    proof, identity = _proof(d), _identity(d, d.worker_token)
    waiting = threading.Event()
    def mutate():
        waiting.set()
        if operation == "register":
            return s.register_executor({"executor_id": WORKER_ACTOR, "capabilities": []}, idempotency_key="late", identity=identity)
        if operation == "capability":
            return s.register_capability({"capability_id": "late", "definition_digest": "sha256:" + "a" * 64}, identity=identity)
        if operation == "claim":
            return s.claim_next({"executor_id": WORKER_ACTOR, "capability_ids": [], "runtime_epoch": s.store._current_runtime_epoch()}, idempotency_key="late", identity=identity)
        return s.ingest_object(b"late write", idempotency_key="late", identity=identity)
    with ThreadPoolExecutor(max_workers=1) as pool:
        with s.store._mutex:
            future = pool.submit(mutate)
            assert waiting.wait(2)
            _retire(d, proof)
        with pytest.raises(RuntimeErrorBase):
            future.result(timeout=5)
    for table in ("executors", "capabilities", "objects", "attempts", "reservations"):
        assert s.store.conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == 0
    assert list(s.cas.root.rglob("*")) == []


@pytest.mark.parametrize("point", ["before_intent", "after_intent", "before_revoke", "after_commit", "after_token", "after_revoke", "before_completion", "after_completion"])
def test_crash_replay_remains_fenced_and_exact_across_restart(daemon, monkeypatch, point):
    d = daemon
    proof, identity = _proof(d), _identity(d, d.worker_token)
    original_write, original_revoke, original_unlink = d._write_local_relinquish, d.credentials.revoke, Path.unlink
    def write(value):
        if (point == "before_intent" and value["state"] == "fencing") or (point == "before_completion" and value["state"] == "complete"):
            raise OSError("injected crash")
        original_write(value)
        if (point == "after_intent" and value["state"] == "fencing") or (point == "after_completion" and value["state"] == "complete"):
            raise OSError("injected crash")
    def revoke(actor):
        if point == "before_revoke":
            raise OSError("injected crash")
        original_revoke(actor)
        if point == "after_revoke":
            raise OSError("injected crash")
    def unlink(path, *args, **kwargs):
        result = original_unlink(path, *args, **kwargs)
        if (point == "after_commit" and path == d.credentials._paths(WORKER_ACTOR)[2]) or (point == "after_token" and path == d.credentials._paths(WORKER_ACTOR)[0]):
            raise OSError("injected crash")
        return result
    with monkeypatch.context() as patch:
        patch.setattr(d, "_write_local_relinquish", write)
        patch.setattr(d.credentials, "revoke", revoke)
        patch.setattr(Path, "unlink", unlink)
        with pytest.raises(OSError, match="injected"):
            _retire(d, proof)
    if point == "before_intent":
        assert not d._local_relinquish_path().exists()
        s = d.service
        with s.store._mutex:
            s._assert_worker_credential_admitted(identity)
        assert _retire(d, proof)["state"] == "credential_authority_retired"
        return
    with d.service.store._mutex, pytest.raises(RuntimeErrorBase):
        d.service._assert_worker_credential_admitted(identity)
    remaining = _files(d)
    root, support = d.root, d.support_root
    d.stop()
    replacement = RuntimeDaemon(root, support_root=support, production_worker_credentials=True).start()
    try:
        # Pending retirement cannot rotate/reconstruct missing files at boot.
        assert _files(replacement) == remaining
        assert replacement.worker_token is None
        foreign = copy.deepcopy(proof)
        foreign["file_digests"]["astrid-pack-host.token"] = "sha256:" + "f" * 64
        with pytest.raises(ConflictError):
            _retire(replacement, foreign)
        assert _files(replacement) == remaining
        assert _retire(replacement, proof)["state"] == "credential_authority_retired"
        assert _retire(replacement, proof)["state"] == "credential_authority_retired"
    finally:
        replacement.stop()


def test_pending_retirement_cannot_retire_replaced_generation(daemon, monkeypatch):
    d = daemon
    proof = _proof(d)
    def fail(actor):
        raise OSError("crash before revoke")
    with monkeypatch.context() as patch:
        patch.setattr(d.credentials, "revoke", fail)
        with pytest.raises(OSError):
            _retire(d, proof)
    successor, _ = d.credentials.provision(WORKER_ACTOR, list(WORKER_SCOPES), rotate=True)
    successor_identity = _identity(d, successor)
    before = _files(d)
    with pytest.raises(ConflictError):
        _retire(d, proof)
    assert _files(d) == before and d._local_relinquish_pending()
    with d.service.store._mutex, pytest.raises(ConflictError):
        d.service._assert_worker_credential_admitted(successor_identity)


def test_owner_must_authenticate_current_owner_bearer(daemon):
    d = daemon
    proof = _proof(d)
    before = _files(d)
    for identity in (None, {"actor": "owner", "scopes": ["admin"]},
                     _identity(d, d.worker_token)):
        with pytest.raises(RuntimeErrorBase):
            d.retire_receiptless_worker_credential(proof, identity=identity)
    assert _files(d) == before and not d._local_relinquish_path().exists()


def test_actual_authenticated_binary_transfer_finishing_after_retirement_is_denied(daemon, monkeypatch):
    from runtime_protocol.server import RuntimeHandler
    d, s = daemon, daemon.service
    proof = _proof(d)
    authenticated, resume = threading.Event(), threading.Event()
    original = RuntimeHandler._binary_chunks
    def paused_chunks(handler):
        authenticated.set()  # Route has already authenticated before staging.
        assert resume.wait(5)
        yield from original(handler)
    monkeypatch.setattr(RuntimeHandler, "_binary_chunks", paused_chunks)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(Api(d.endpoint, d.worker_token).request, "POST", "/v1/objects",
                             raw=b"in flight", headers={"Idempotency-Key": "in-flight"})
        try:
            assert authenticated.wait(5)
            Api(d.endpoint, d.token).request("POST", "/v1/control/local-worker/retire-credential", proof)
        finally:
            resume.set()
        with pytest.raises(RuntimeError) as denied:
            future.result(timeout=5)
        assert denied.value.status == 401
    assert s.store.conn.execute("SELECT count(*) FROM objects").fetchone()[0] == 0
    assert list(s.cas.root.rglob("*")) == []


def test_retirement_preserves_start_refusal_then_allows_genuine_local_producer(tmp_path):
    # Native processes are doubled by the existing launcher fixture. Credential
    # issue, launch receipt validation and owner readback use production code.
    from tests.test_local_worker_handover import _daemon
    d, preparer, _, workspace = _daemon(tmp_path)
    try:
        token, _ = d.credentials.provision(WORKER_ACTOR, list(WORKER_SCOPES), rotate=True)
        proof, stale = _proof(d), _identity(d, token)
        before = _files(d)
        with pytest.raises(ConflictError, match="custody"):
            d.start_local_worker("astrid", workspace)
        assert _files(d) == before
        assert preparer.events == []
        _retire(d, proof)
        assert "stop_owned" not in preparer.events
        assert not d._remote_worker_custody_unresolved() and not d._local_relinquish_pending()
        # Use the real two-phase producer; the unrelated daemon composition
        # fixture is not part of this focused source proof.
        result = d.local_worker_launcher.start("astrid", workspace)
        assert result["state"] == "active"
        metadata = d.credentials.actor_metadata(WORKER_ACTOR)
        assert metadata["local_launch_receipt"]["executor_incarnation"] == result["executor_incarnation"]
        assert d.local_worker_generation(identity=_owner(d))["executor_incarnation"] == result["executor_incarnation"]
        fresh = _identity(d, d.credentials.path_for(WORKER_ACTOR).read_text())
        with d.service.store._mutex:
            d.service._assert_worker_credential_admitted(fresh)
            with pytest.raises(AuthorizationError):
                d.service._assert_worker_credential_admitted(stale)
        successor = _files(d)
        with pytest.raises(ConflictError):
            _retire(d, proof)
        assert _files(d) == successor
        relinquished = d.relinquish_local_worker(result["executor_incarnation"], result["evidence_digest"], identity=_owner(d))
        assert relinquished["state"] == "relinquished"
        assert preparer.events.count("stop_owned") == 1
        assert d.credentials.actor_metadata(WORKER_ACTOR) is None
    finally:
        d.stop()


@pytest.mark.parametrize("corruption", ["hash", "link", "qualification_shape", "acceptance_shape", "revocation_shape"])
def test_revoked_history_is_not_cleanup_authority_when_corrupt(daemon, corruption):
    d, s = daemon, daemon.service
    proof = _proof(d)
    task, qualification, _ = _task(d, "revoked-history")
    run = s.store.get_task(task)["run"]["id"]
    qualified = {"activation_id": "old"} if corruption == "qualification_shape" else qualification
    s.store._append_event(run, task, "task.remote_activation_qualified", qualified)
    accepted = {"activation_id": qualification["activation_id"]}
    if corruption == "acceptance_shape":
        accepted["extra"] = True
    s.store._append_event(run, task, "task.remote_activation_accepted", accepted)
    revoked = {"activation_id": qualification["activation_id"], "revoked_at": "2026-10-19T00:00:00+00:00"}
    if corruption == "revocation_shape":
        revoked.pop("revoked_at")
    s.store._append_event(run, task, "task.remote_activation_revoked", revoked)
    if corruption in {"hash", "link"}:
        column = "event_hash" if corruption == "hash" else "previous_hash"
        s.store.conn.execute(f"UPDATE events SET {column}='corrupt' WHERE id=(SELECT max(id) FROM events)")
    before = _files(d)
    with pytest.raises(ConflictError):
        _retire(d, proof)
    assert _files(d) == before and not d._local_relinquish_path().exists()


def test_valid_revoked_remote_history_is_preserved_and_not_reported_stopped(daemon):
    d, s = daemon, daemon.service
    proof = _proof(d)
    task, qualification, _ = _task(d, "revoked")
    run = s.store.get_task(task)["run"]["id"]
    s.store._append_event(run, task, "task.remote_activation_qualified", qualification)
    s.store._append_event(run, task, "task.remote_activation_accepted", {"activation_id": qualification["activation_id"]})
    s.store._append_event(run, task, "task.remote_activation_revoked", {"activation_id": qualification["activation_id"], "revoked_at": "2026-10-19T00:00:00+00:00"})
    before = [tuple(row) for row in s.store.conn.execute("SELECT * FROM events ORDER BY id")]
    result = _retire(d, proof)
    assert result["historical_process_state"] == "UNKNOWN"
    assert [tuple(row) for row in s.store.conn.execute("SELECT * FROM events ORDER BY id")] == before


@pytest.mark.parametrize("index", [0, 1, 2])
def test_foreign_file_owner_refuses_before_intent(daemon, monkeypatch, index):
    d = daemon
    proof, before = _proof(d), _files(d)
    target = d.credentials._paths(WORKER_ACTOR)[index]
    original = Path.lstat
    def lstat(path, *args, **kwargs):
        value = original(path, *args, **kwargs)
        if path == target:
            fields = list(value)
            fields[4] = os.getuid() + 1
            return os.stat_result(fields)
        return value
    with monkeypatch.context() as patch:
        patch.setattr(Path, "lstat", lstat)
        with pytest.raises(RuntimeErrorBase):
            _retire(d, proof)
    assert _files(d) == before and not d._local_relinquish_path().exists()


def test_generation_changed_during_snapshot_refuses_before_intent(daemon, monkeypatch):
    d = daemon
    proof = _proof(d)
    original = d.credentials._generation_file_snapshot
    count = 0
    def snapshot(path):
        nonlocal count
        result = original(path)
        count += 1
        if count == 3:
            d.credentials.provision(WORKER_ACTOR, list(WORKER_SCOPES), rotate=True)
        return result
    with monkeypatch.context() as patch:
        patch.setattr(d.credentials, "_generation_file_snapshot", snapshot)
        with pytest.raises(RuntimeErrorBase):
            _retire(d, proof)
    assert not d._local_relinquish_path().exists()
    assert d.credentials.actor_metadata(WORKER_ACTOR) is not None
