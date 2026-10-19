from __future__ import annotations

import copy

import pytest

from http_helpers import Api
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import RetiredRouteError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_store import TimelineCommitStore
from test_timeline_commit_acceptance import validate_prepared


@pytest.fixture(scope="module", params=["service", "http"])
def documents(request, tmp_path_factory):
    root = tmp_path_factory.mktemp(request.param) / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({"slug": "authority", "name": "Authority"})["id"]
    for index, timeline in enumerate(("main", "spoofed", "alias", "shot:shot-1")):
        service.create_timeline_document(
            project, {"timeline_id": timeline, "config": {}, "registry": {}},
            idempotency_key=f"seed-{index}",
        )
    TimelineCommitStore(service.store, validate_prepared=validate_prepared).bootstrap(project, "main", authorize=lambda: None)
    # Persisted legacy/corrupt identities are fixture setup, before admission
    # and measurement. Neither the HTTP nor service guard is disabled.
    service.store.conn.execute(
        "UPDATE project_documents SET kind='example.notes' WHERE id='timeline:spoofed'"
    )
    service.store.conn.execute(
        "UPDATE project_documents SET id='legacy-projection' WHERE id='timeline:alias'"
    )
    service.create_document(
        project, {"document_id": "ordinary", "kind": "example.notes", "content": {"kept": True}},
        idempotency_key="seed-ordinary",
    )
    daemon = None
    api = None
    if request.param == "http":
        service.close()
        daemon = RuntimeDaemon(root, support_root=root.parent / "support").start()
        service = daemon.service
        token, _ = daemon.credentials.provision("document-editor", ["projects:read", "projects:write"])
        api = Api(daemon.endpoint, token)

    def call(method, document_id, body, key):
        if api is not None:
            path = f"/v1/projects/{project}/documents"
            if method == "PATCH":
                path += f"/{document_id}"
            return api.request(method, path, body, headers={"Idempotency-Key": key})
        if method == "POST":
            return service.create_document(project, body, idempotency_key=key)
        return service.update_document(project, document_id, body, idempotency_key=key)

    yield service, project, call
    if daemon is not None:
        daemon.stop()
    else:
        service.close()


def _snapshot(service):
    with service.store._mutex:
        return (
            service.store.conn.total_changes,
            tuple(service.store.conn.iterdump()),
            {str(path.relative_to(service.cas.root)): path.read_bytes()
             for path in service.cas.root.rglob("*") if path.is_file()},
        )


def _assert_denied(documents, monkeypatch, method, document_id, body):
    service, _, call = documents

    def replay_must_not_run(*args, **kwargs):
        pytest.fail("canonical Document authority must be checked before receipt replay")

    monkeypatch.setattr(service, "_command_replay", replay_must_not_run)
    before = _snapshot(service)
    with pytest.raises((RetiredRouteError, RuntimeError)) as error:
        call(method, document_id, body, "forbidden-document")
    assert error.value.status == 410
    if isinstance(error.value, RetiredRouteError):
        assert error.value.code == "retired_route"
    else:
        assert error.value.detail["code"] == "retired_route"
    # Includes every row, head/history, receipt/event/project sequence and CAS
    # byte, plus total_changes to detect writes even if rolled back.
    assert _snapshot(service) == before


@pytest.mark.parametrize("document_id, kind", [
    ("timeline:main", "timeline.composition"),
    ("timeline:main", "example.notes"),
    ("timeline:fresh", "timeline.composition"),
    ("timeline:fresh", "example.notes"),
    ("timeline:", "example.notes"),
    ("timeline:shot:shot-1", "example.notes"),
    ("timeline:shot:fresh", "example.notes"),
    ("timeline:spoofed", "example.notes"),
    ("fresh", "timeline.composition"),
    ("ordinary", "timeline.composition"),
    ("legacy-projection", "example.notes"),
    ("legacy-projection", "timeline.composition"),
])
def test_create_rejects_canonical_existing_and_proposed_identity(documents, monkeypatch, document_id, kind):
    _assert_denied(documents, monkeypatch, "POST", document_id, {
        "document_id": document_id, "kind": kind, "content": {"config": {"changed": True}},
    })


@pytest.mark.parametrize("document_id, patch", [
    ("timeline:main", {}),
    ("timeline:main", {"kind": "example.notes", "document_id": "ordinary"}),
    ("timeline:main", {"content": None}),
    ("timeline:fresh", {"kind": "example.notes"}),
    ("timeline:fresh", {"kind": "timeline.composition"}),
    ("timeline:shot:shot-1", {"kind": "example.notes"}),
    ("timeline:shot:fresh", {"kind": "example.notes"}),
    ("timeline:spoofed", {}),
    ("legacy-projection", {}),
    ("legacy-projection", {"kind": "example.notes", "document_id": "ordinary"}),
    ("ordinary", {"kind": "timeline.composition"}),
    ("ordinary", {"document_id": "timeline:main"}),
    ("ordinary", {"document_id": "timeline:fresh", "kind": "example.notes"}),
    ("fresh", {"kind": "timeline.composition"}),
    ("fresh", {"document_id": "timeline:fresh"}),
])
def test_update_rejects_canonical_existing_and_proposed_identity(documents, monkeypatch, document_id, patch):
    _assert_denied(documents, monkeypatch, "PATCH", document_id, {
        "expected_version": 1, "content": {"config": {"changed": True}}, **patch,
    })


@pytest.mark.parametrize("document_id", ["timeline:main", "legacy-projection"])
def test_exact_duplicate_create_is_also_denied(documents, monkeypatch, document_id):
    service, project, _ = documents
    old = service.get_document(project, document_id)
    _assert_denied(documents, monkeypatch, "POST", document_id, {
        "document_id": document_id, "kind": old["kind"], "content": old["content"],
    })


@pytest.mark.parametrize("kind", ["pack.config", "media.transcript"])
def test_ordinary_source_create_update_and_retry_still_work(documents, kind):
    service, project, call = documents
    if kind == "media.transcript":
        media = service.ingest(project, b"transcript source", idempotency_key="source-media")["data"]["object_id"]
        document_id = service._transcript_document_id(project, media, "default")
        content = {"schema": "media.transcript/v1", "media_id": media, "source_id": "default",
                   "segments": [{"id": "segment", "text": "original", "start": 0, "end": 1, "words": []}]}
        replacement = copy.deepcopy(content)
        replacement["segments"][0]["text"] = "corrected"
    else:
        document_id = "pack-config"
        content = {"schema": "pack.config/v1", "opaque": {"clear": None}, "enabled": True}
        replacement = {**content, "enabled": False}
    body = {"document_id": document_id, "kind": kind, "content": content}
    created = call("POST", document_id, body, f"create-{kind}")
    assert created["data"]["content"] == content
    assert call("POST", document_id, body, f"create-{kind}") == created
    patch = {"expected_version": 1, "content": replacement}
    updated = call("PATCH", document_id, patch, f"update-{kind}")
    assert updated["data"]["version"] == 2
    assert updated["data"]["content"] == replacement
    assert call("PATCH", document_id, patch, f"update-{kind}") == updated
    assert service.get_document(project, document_id) == updated["data"]
