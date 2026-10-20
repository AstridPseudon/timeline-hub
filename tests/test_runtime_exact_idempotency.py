from __future__ import annotations

import copy
import json

import pytest

from astrid_runtime_client import ApiError, WorkspaceClient
from http_helpers import Api, legacy_call
from runtime_protocol.errors import InvalidRequestError, RuntimeErrorBase
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore


def test_executor_registration_requires_key_and_fences_stale_replay_after_restart(tmp_path):
    root = tmp_path / "realm"
    support = tmp_path / "support"
    RealmStore.initialize(root).close()
    daemon = RuntimeDaemon(root, support_root=support).start()
    try:
        api = Api(daemon.endpoint, daemon.token)
        executor = {
            "executor_id": "exact-executor",
            "max_concurrency": 2,
            "resource_keys": ["gpu"],
            "capabilities": ["render.basic"],
            "protocol": "workspace.v1",
        }
        with pytest.raises(RuntimeError) as missing:
            api.request("POST", "/v1/executors", executor)
        assert missing.value.status == 400
        first = api.request("POST", "/v1/executors", executor, headers={"Idempotency-Key": "executor-exact"})
        assert first["executor_id"] == "exact-executor"
    finally:
        daemon.stop()

    restarted = RuntimeDaemon(root, support_root=support).start()
    try:
        api = Api(restarted.endpoint, restarted.token)
        with pytest.raises(RuntimeError) as stale:
            api.request("POST", "/v1/executors", executor, headers={"Idempotency-Key": "executor-exact"})
        assert stale.value.status == 409
        with pytest.raises(RuntimeError) as changed:
            api.request("POST", "/v1/executors", {**executor, "max_concurrency": 3}, headers={"Idempotency-Key": "executor-exact"})
        assert changed.value.status == 409
        assert restarted.service.store.conn.execute("SELECT COUNT(*) FROM executors WHERE id=?", ("exact-executor",)).fetchone()[0] == 1
    finally:
        restarted.stop()


def test_project_reference_creation_is_keyed_durable_and_non_overwriting(tmp_path):
    root = tmp_path / "realm"
    support = tmp_path / "support"
    RealmStore.initialize(root).close()
    daemon = RuntimeDaemon(root, support_root=support).start()
    try:
        client = WorkspaceClient(daemon.endpoint, daemon.token)
        project = client.create_project("Exact Reference", idempotency_key="exact-project")
        media = client.ingest_project_object(project.project_id, b"exact-reference", media_type="application/octet-stream", idempotency_key="exact-media")
        reference = {"reference_id": "exact-reference", "kind": "character", "name": "Exact", "media_id": media.object_id}
        with pytest.raises(ApiError) as missing_reference:
            client._request("POST", f"/v1/projects/{project.project_id}/references", body=json.dumps(reference).encode(), headers={"Content-Type": "application/json"})
        assert missing_reference.value.status == 400
        first_reference = client.create_project_reference(project.project_id, reference, idempotency_key="exact-reference-key")
    finally:
        daemon.stop()

    restarted = RuntimeDaemon(root, support_root=support).start()
    try:
        client = WorkspaceClient(restarted.endpoint, restarted.token)
        assert client.create_project_reference(project.project_id, reference, idempotency_key="exact-reference-key") == first_reference
        with pytest.raises(ApiError) as changed_reference:
            client.create_project_reference(project.project_id, {**reference, "name": "Changed"}, idempotency_key="exact-reference-key")
        assert changed_reference.value.status == 409
        with pytest.raises(ApiError) as overwrite_reference:
            client.create_project_reference(project.project_id, {**reference, "name": "Overwrite"}, idempotency_key="different-reference-key")
        assert overwrite_reference.value.status == 409
        assert restarted.service.store.conn.execute("SELECT name FROM project_references WHERE id='exact-reference'").fetchone()[0] == "Exact"
    finally:
        restarted.stop()


@pytest.mark.integration
def test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting(tmp_path):
    # The public 0.2.13 schema does not contain occurrence.create.  The native
    # helpers select the unchanged ordinary014 staging candidate, whose exact
    # contract identity is qualified separately; published013 remains intact.
    from test_timeline_clip_replacement import (
        _native_bootstrap_commands,
        _native_body,
        _native_commit,
        _native_empty_document,
        _native_import_media,
        _native_imports,
    )

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    native = _native_imports()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "exact-timeline", "name": "Exact Timeline"})
        project_id = project["id"]
        service.register_timeline_commit_provider(native.load_timeline_commit_provider("astrid"))
        service.create_timeline(project_id, "film", idempotency_key="exact-timeline")
        media, verified_media = _native_import_media(service, project_id, alias="exact")
        body = _native_body(
            service,
            project_id,
            _native_bootstrap_commands(
                native,
                _native_empty_document(service, project_id),
                media,
                verified_media,
            ),
        )
        before_missing = (
            service.get_project_timeline(project_id, "film"),
            service.list_project_shots(project_id),
            service.list_project_objects(project_id),
        )
        with pytest.raises(InvalidRequestError) as missing_key:
            _native_commit(service, project_id, body, None)
        assert missing_key.value.status == 400
        assert (
            service.get_project_timeline(project_id, "film"),
            service.list_project_shots(project_id),
            service.list_project_objects(project_id),
        ) == before_missing

        first = _native_commit(service, project_id, body, "exact-creation-key")
        assert first["data"]["status"] == "accepted"
        document = first["data"]["canonical_document"]
        assert document["shot_revisions"][0]["shot_id"] == "native-shot"
        assert document["parent_revision"]["payload"]["occurrences"] == [{
            "duration_ms": 5000.0,
            "gain": 1,
            "occurrence_id": "native-occurrence",
            "placement": {"start_ms": 0.0, "track": "picture"},
            "shot_id": "native-shot",
            "shot_revision_id": document["shot_revisions"][0]["revision_id"],
            "source_offset": 0,
            "speed": 1,
            "track": "picture",
        }]
        shots = service.list_project_shots(project_id)["items"]
        assert len(shots) == 1
        assert shots[0]["project_id"] == project_id
        assert shots[0]["shot_id"] == "native-shot"
        assert shots[0]["name"] == "Native chapter"
        catalog = service.list_project_objects(project_id)["items"]
        assert len(catalog) == 1
        assert catalog[0]["object_id"] == media["object_id"]
        assert catalog[0]["digest"] == media["object_id"]
        assert document["parent_revision"]["payload"]["registry"]["assets"][media["asset"]]["media_id"] == media["object_id"]
        before_restart = (
            service.get_project_timeline(project_id, "film"),
            service.list_project_shots(project_id),
            service.list_project_objects(project_id),
        )
    finally:
        service.close()

    restarted = RuntimeService(root)
    try:
        restarted.register_timeline_commit_provider(native.load_timeline_commit_provider("astrid"))
        assert _native_commit(restarted, project_id, body, "exact-creation-key") == first
        assert (
            restarted.get_project_timeline(project_id, "film"),
            restarted.list_project_shots(project_id),
            restarted.list_project_objects(project_id),
        ) == before_restart

        changed = copy.deepcopy(body)
        occurrence = next(command for command in changed["commands"] if command["op"] == "occurrence.create")
        occurrence["args"]["name"] = "Changed"
        before_refusal = (
            restarted.get_project_timeline(project_id, "film"),
            restarted.list_project_shots(project_id),
            restarted.list_project_objects(project_id),
        )
        with pytest.raises(RuntimeErrorBase) as changed_request:
            _native_commit(restarted, project_id, changed, "exact-creation-key")
        assert changed_request.value.status == 409
        assert changed_request.value.details["reason"] == "idempotency_mismatch"
        with pytest.raises(RuntimeErrorBase) as overwrite:
            _native_commit(restarted, project_id, changed, "different-creation-key")
        assert overwrite.value.status == 409
        assert (
            restarted.get_project_timeline(project_id, "film"),
            restarted.list_project_shots(project_id),
            restarted.list_project_objects(project_id),
        ) == before_refusal
    finally:
        restarted.close()
