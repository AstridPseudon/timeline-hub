from __future__ import annotations

import hashlib
import json
import sys
import threading
import time
import types
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parents[1] / "packages" / "python"))
from banodoco_workspace_client import ApiError, WorkspaceClient
from http_helpers import Api
from runtime_protocol.auth import CredentialStore
from runtime_protocol.server import RuntimeHTTPServer, RuntimeHandler
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.util import canonical_json


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def runtime_api(tmp_path):
    realm = tmp_path / "realm"
    RealmStore.initialize(realm).close()
    service = RuntimeService(realm)
    project = service.create_project({"name": "Replay fixture", "slug": "replay-fixture"})["id"]
    other_project = service.create_project({"name": "Foreign fixture", "slug": "foreign-fixture"})["id"]
    credentials = CredentialStore(tmp_path / "credentials")
    token, _ = credentials.provision("writer", ["projects:read", "projects:write"])
    server = RuntimeHTTPServer(("127.0.0.1", 0), RuntimeHandler)
    server.runtime, server.credentials = service, credentials
    server.daemon_runtime = types.SimpleNamespace(instance_id="runtime-instance")
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    try:
        yield service, project, other_project, server, token
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        service.close()
        assert not thread.is_alive()


def api(server, token):
    return Api(f"http://127.0.0.1:{server.server_port}", token)


def state(service):
    return {
        table: [tuple(row) for row in service.store.conn.execute(f"SELECT * FROM {table}")]
        for table in ("project_documents", "command_idempotency", "events")
    }


def document_path(project, document_id=None, *, replay_only=False):
    path = f"/v1/projects/{project}/documents"
    if document_id is not None:
        path += f"/{document_id}"
    return path + ("?replay_only=true" if replay_only else "")


def test_replay_hits_return_original_create_and_update_after_independent_advancement(runtime_api):
    service, project, _, server, token = runtime_api
    caller = api(server, token)

    create_body = {"document_id": "created", "kind": "notes", "content": {"text": "original"}}
    create_key = "create-original"
    original_create = caller.request("POST", document_path(project), create_body,
                                     headers={"Idempotency-Key": create_key})
    caller.request("PATCH", document_path(project, "created"),
                   {"expected_version": 1, "content": {"text": "advanced"}},
                   headers={"Idempotency-Key": "advance-created"})
    before_create_replay = state(service)
    replayed_create = caller.request("POST", document_path(project, replay_only=True), create_body,
                                     headers={"Idempotency-Key": create_key})
    assert replayed_create == original_create
    assert replayed_create["data"]["version"] == 1
    assert state(service) == before_create_replay
    expected_create_hash = hashlib.sha256(canonical_json({
        "project_id": project, "document_id": "created", "kind": "notes", "content": {"text": "original"}
    }).encode()).hexdigest()
    assert replayed_create["receipt"]["request_hash"] == expected_create_hash

    update_doc_body = {"document_id": "update-path", "kind": "notes", "content": {"text": "update base"}}
    caller.request("POST", document_path(project), update_doc_body, headers={"Idempotency-Key": "update-seed"})
    update_body = {"expected_version": 1, "content": {"text": "first update"}}
    update_key = "update-original"
    original_update = caller.request("PATCH", document_path(project, "update-path"), update_body,
                                     headers={"Idempotency-Key": update_key})
    caller.request("PATCH", document_path(project, "update-path"),
                   {"expected_version": 2, "content": {"text": "advanced again"}},
                   headers={"Idempotency-Key": "advance-updated"})
    before_update_replay = state(service)
    replayed_update = caller.request("PATCH", document_path(project, "update-path", replay_only=True), update_body,
                                     headers={"Idempotency-Key": update_key})
    assert replayed_update == original_update
    assert replayed_update["data"]["version"] == 2
    assert state(service) == before_update_replay
    expected_update_hash = hashlib.sha256(canonical_json({
        "project_id": project, "document_id": "update-path", "body": update_body
    }).encode()).hexdigest()
    assert replayed_update["receipt"]["request_hash"] == expected_update_hash


@pytest.mark.parametrize("operation", ["create", "update"])
def test_replay_miss_is_typed_and_leaves_documents_ledger_and_events_unchanged(runtime_api, operation):
    service, project, _, server, token = runtime_api
    caller = api(server, token)
    if operation == "update":
        caller.request("POST", document_path(project),
                       {"document_id": "existing", "kind": "notes", "content": {"text": "before"}},
                       headers={"Idempotency-Key": "existing-create"})
        method = "PATCH"
        path = document_path(project, "existing", replay_only=True)
        body = {"expected_version": 1, "content": {"text": "after"}}
    else:
        method = "POST"
        path = document_path(project, replay_only=True)
        body = {"document_id": "missing", "kind": "notes", "content": {"text": "would create"}}
    before = state(service)
    if operation == "create":
        client = WorkspaceClient(f"http://127.0.0.1:{server.server_port}", token)
        with pytest.raises(ApiError) as caught:
            client.create_document(project, "missing", "notes", {"text": "would create"},
                                   idempotency_key="missing-create", replay_only=True)
        assert caught.value.status == 409
        assert caught.value.code == "no_committed_request"
    else:
        with pytest.raises(RuntimeError) as caught:
            caller.request(method, path, body, headers={"Idempotency-Key": f"missing-{operation}"})
        assert caught.value.status == 409
        assert caught.value.detail["code"] == "no_committed_request"
    assert state(service) == before


def test_replay_only_changed_body_keeps_existing_idempotency_conflict(runtime_api):
    service, project, _, server, token = runtime_api
    caller = api(server, token)
    original = {"document_id": "same-key", "kind": "notes", "content": {"text": "original"}}
    caller.request("POST", document_path(project), original, headers={"Idempotency-Key": "fixed-key"})
    before = state(service)
    changed = {**original, "content": {"text": "changed"}}
    with pytest.raises(RuntimeError) as caught:
        caller.request("POST", document_path(project, replay_only=True), changed,
                       headers={"Idempotency-Key": "fixed-key"})
    assert caught.value.status == 409
    assert caught.value.detail["code"] == "conflict"
    assert state(service) == before


def test_replay_only_keeps_wrong_project_revoked_and_read_only_denials(runtime_api, monkeypatch):
    service, project, other_project, server, token = runtime_api
    credentials = server.credentials
    caller = api(server, token)
    body = {"document_id": "denied", "kind": "notes", "content": {"text": "x"}}

    readonly, _ = credentials.provision("reader", ["projects:read"])
    before = state(service)
    with pytest.raises(RuntimeError) as read_error:
        api(server, readonly).request("POST", document_path(project, replay_only=True), body,
                                     headers={"Idempotency-Key": "readonly"})
    assert read_error.value.status == 401
    assert state(service) == before

    caller.request("POST", document_path(project), body, headers={"Idempotency-Key": "revoke-me"})
    before_revoke_retry = state(service)
    credentials.revoke("writer")
    with pytest.raises(RuntimeError) as revoked_error:
        caller.request("POST", document_path(project, replay_only=True), body,
                       headers={"Idempotency-Key": "revoke-me"})
    assert revoked_error.value.status == 401
    assert state(service) == before_revoke_retry

    # The production project-grant issuer lives in Astrid. This isolated
    # Runtime COW does not carry that package, so provide only the issuer type
    # needed to let Runtime's real paired-session and HTTP project-binding
    # path run. The path mismatch is denied by Runtime before the issuer's
    # decision method can be called.
    authority_module = types.ModuleType("astrid.core.execution.provider_route_grant")

    class ProjectGrantAuthority:
        def __init__(self, *, realm, browser_session, actor_id, selected_project, **_kwargs):
            self.realm = realm
            self.browser_session = browser_session
            self.actor_id = actor_id
            self.selected_project = selected_project

        def issue(self, grant):
            return {**grant, "selected_project": self.selected_project}

        def decide(self, *_args, **_kwargs):
            pytest.fail("wrong-project request must be denied before grant evaluation")

    authority_module.ProjectGrantAuthority = ProjectGrantAuthority
    authority_module.SELECTED_PROJECT_OPERATIONS = frozenset()
    for name in ("astrid", "astrid.core", "astrid.core.execution"):
        package = types.ModuleType(name)
        package.__path__ = []
        monkeypatch.setitem(sys.modules, name, package)
    monkeypatch.setitem(sys.modules, "astrid.core.execution.provider_route_grant", authority_module)

    service.select_project("connector", project, idempotency_key="connector-selection")
    connector_token, _ = credentials.provision_connector(
        "connector", ["handshake", "projects:read", "projects:write"],
        connector_id="fixture-connector", realm_id=service.realm["id"], expires_at=time.time() + 120,
    )
    context = {
        "pair_id": "replay-pair", "connector_id": "fixture-connector", "generation": 1,
        "realm_id": service.realm["id"], "expires_at": int((time.time() + 90) * 1000),
    }
    before_wrong_project = state(service)
    with pytest.raises(RuntimeError) as wrong_project_error:
        api(server, connector_token).request(
            "POST", document_path(other_project, replay_only=True), body,
            headers={"Idempotency-Key": "wrong-project", "X-Reigh-Paired-Session": json.dumps(context)},
        )
    assert wrong_project_error.value.status == 403
    assert wrong_project_error.value.detail["details"]["decision"]["code"] == "project_grant_project_denied"
    assert state(service) == before_wrong_project


def test_generated_python_clients_keep_query_outside_body_and_request_hash():
    calls = []
    receipt = {"receipt_id": "r", "command_kind": "document.create", "idempotency_key": "create-key",
               "request_hash": "a" * 64, "project_id": "p", "project_seq": [1, 1], "event_ids": [],
               "result": {}, "created_at": "2026-10-16T00:00:00Z"}

    def transport(method, path, headers, body):
        if method == "GET" and path == "/v1/health":
            calls.append((method, path, headers, None))
            return 200, {}, json.dumps({
                "status": "ok", "protocol": "workspace.v1", "schema_digest": "sha256:" + "a" * 64,
                "runtime_epoch": 1, "runtime_session_id": "runtime", "runtime_instance_id": "instance",
                "operation_versions": {"createDocument": [1, 2], "updateDocument": [1, 2]},
            }).encode()
        calls.append((method, path, headers, json.loads(body)))
        result = {"data": {"document_id": "doc", "kind": "notes", "content": {"text": "x"}, "version": 1},
                  "receipt": receipt}
        return 201 if method == "POST" else 200, {}, json.dumps(result).encode()

    client = WorkspaceClient("http://runtime", transport=transport)
    created = client.create_document("p", "doc", "notes", {"text": "x"}, idempotency_key="create-key", replay_only=True)
    updated = client.update_document("p", "doc", expected_version=1, idempotency_key="update-key",
                                     content={"text": "y"}, replay_only=True)
    client.create_document("p", "doc", "notes", {"text": "ordinary"}, idempotency_key="ordinary-key")
    mutation_calls = [call for call in calls if call[0] != "GET"]
    assert sum(path == "/v1/health" for _, path, _, _ in calls) == 2
    assert mutation_calls[0][1] == "/v1/projects/p/documents?replay_only=true"
    assert mutation_calls[0][3] == {"document_id": "doc", "kind": "notes", "content": {"text": "x"}}
    assert mutation_calls[1][1] == "/v1/projects/p/documents/doc?replay_only=true"
    assert mutation_calls[1][3] == {"expected_version": 1, "content": {"text": "y"}}
    assert mutation_calls[2][1] == "/v1/projects/p/documents"
    assert mutation_calls[2][3] == {"document_id": "doc", "kind": "notes", "content": {"text": "ordinary"}}
    assert all("replay_only" not in (request_body or {}) for _, _, _, request_body in calls)
    assert created.receipt == updated.receipt == receipt
    assert created["version"] == updated["version"] == 1


@pytest.mark.parametrize("operation", ["create", "update"])
def test_generated_python_clients_refuse_replay_query_without_matching_advertised_v2(operation):
    calls = []
    operation_id = "createDocument" if operation == "create" else "updateDocument"
    operation_versions = {"createDocument": [1, 2], "updateDocument": [1, 2]}
    operation_versions[operation_id] = [1]

    def transport(method, path, headers, body):
        calls.append((method, path, body))
        assert method == "GET" and path == "/v1/health"
        return 200, {}, json.dumps({
            "status": "ok", "protocol": "workspace.v1", "schema_digest": "sha256:" + "a" * 64,
            "runtime_epoch": 1, "runtime_session_id": "runtime", "runtime_instance_id": "instance",
            "operation_versions": operation_versions,
        }).encode()

    client = WorkspaceClient("http://old-runtime", transport=transport)
    with pytest.raises(ApiError) as caught:
        if operation == "create":
            client.create_document("p", "doc", "notes", {}, idempotency_key="key", replay_only=True)
        else:
            client.update_document("p", "doc", expected_version=1, idempotency_key="key", replay_only=True)
    assert caught.value.code == "unsupported_operation_version"
    assert calls == [("GET", "/v1/health", None)]


def test_openapi_declares_query_only_and_additive_operation_profiles():
    contract = yaml.safe_load((ROOT / "contract/openapi/workspace-v1.yaml").read_text())
    schemas = contract["components"]["schemas"]
    for path, method, operation_id, schema_name in [
        ("/v1/projects/{project_id}/documents", "post", "createDocument", "CreateDocument"),
        ("/v1/projects/{project_id}/documents/{document_id}", "patch", "updateDocument", "UpdateDocument"),
    ]:
        operation = contract["paths"][path][method]
        assert operation["operationId"] == operation_id
        assert operation["x-operation-versions"] == [1, 2]
        replay = next(param for param in operation["parameters"] if param.get("name") == "replay_only")
        assert replay["in"] == "query" and replay["schema"]["type"] == "boolean"
        assert "replay_only" not in schemas[schema_name]["properties"]
