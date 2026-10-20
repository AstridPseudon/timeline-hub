"""The retired timeline family cannot publish, including before retry lookup.

publish_parent_composition is not in that family: it stays live for headless timelines
until the App migration lands, and refuses only a tracked timeline (below).

Run the whole file through the central restore-integration lane with the actual
Agent checkout. Only the HTTP cases need sockets; service cases run directly.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from astrid_runtime_client import ApiError, WorkspaceClient
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import RetiredRouteError, RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import route_path
from test_shot_composition_runtime import restore_provider as actual_provider  # noqa: F401 (fixture)


FAMILIES = (
    "update_timeline", "replace_timeline_clip", "create_timeline_document",
    "replace_parent_composition_media", "archive_timeline", "recover_timeline",
)
STATES = ("tracked", "fresh", "unused")


def seed(root, provider):
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({"slug": "authority", "name": "Authority"})["id"]
    service.create_timeline(project, "fresh", idempotency_key="fresh-create")
    service.ingest(project, b"ordinary artifact", idempotency_key="artifact")
    service.register_timeline_commit_provider(provider)
    service.create_timeline(project, "tracked", idempotency_key="tracked-create")
    return service, project


@pytest.fixture
def service_case(tmp_path, actual_provider):
    service, project = seed(tmp_path / "realm", actual_provider)
    try:
        yield SimpleNamespace(service=service, project=project)
    finally:
        service.close()


@pytest.fixture
def http_case(tmp_path, actual_provider):
    root = tmp_path / "realm"
    service, project = seed(root, actual_provider)
    service.close()
    daemon = RuntimeDaemon(root, support_root=tmp_path / "support", authoring_profile="astrid").start()
    try:
        yield SimpleNamespace(service=daemon.service, project=project,
                              client=WorkspaceClient(daemon.endpoint, daemon.token), daemon=daemon)
    finally:
        daemon.stop()


def snapshot(service):
    with service.store._mutex:
        database = tuple(service.store.conn.iterdump())
        objects = {str(path.relative_to(service.store.cas_root)): path.read_bytes()
                   for path in service.store.cas_root.rglob("*") if path.is_file()}
    return database, objects


def legacy_request(case, family, timeline):
    project = case.project
    resource = None if timeline == "unused" else case.service.get_project_timeline(project, timeline)
    head = resource["head_revision_id"] if resource else None
    version = resource["version"] if resource else 1
    object_id = "sha256:" + "0" * 64
    requests = {
        "update_timeline": ("PATCH", f"/v1/timelines/{timeline}",
                            {"expected_version": version, "shots": [], "references": []}),
        "replace_timeline_clip": ("POST", f"/v1/timelines/{timeline}/replace-clip",
                                  {"expected_version": version, "clip_id": "clip", "source_object_id": object_id}),
        "create_timeline_document": ("POST", f"/v1/projects/{project}/timeline-documents",
                                     {"timeline_id": timeline, "config": {}, "registry": {}}),
        "publish_parent_composition": ("POST", f"/v1/projects/{project}/timelines/{timeline}/composition-revisions",
                                       {"project_id": project, "timeline_id": timeline, "expected_head": head,
                                        "parent_revision_id": "legacy-parent", "parent_composition": {
                                            "config": {}, "registry": {}, "clips": [], "occurrences": []}}),
        "replace_parent_composition_media": ("POST", f"/v1/projects/{project}/timelines/{timeline}/replace-parent-media",
                                             {"expected_head": head or "old-parent", "occurrence_id": "occurrence",
                                              "clip_id": "clip", "source_object_id": object_id}),
        "archive_timeline": ("POST", f"/v1/timelines/{timeline}/archive", {"expected_version": version}),
        "recover_timeline": ("POST", f"/v1/timelines/{timeline}/recover", {"expected_version": version, "version": 1}),
    }
    return requests[family]


def call_service(case, family, timeline, body, key):
    args = (case.project, body) if family == "create_timeline_document" else (
        (case.project, timeline, body) if family in ("publish_parent_composition", "replace_parent_composition_media")
        else (timeline, body)
    )
    return getattr(case.service, family)(*args, idempotency_key=key)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("timeline", STATES)
def test_service_legacy_family_refuses_without_writes(service_case, family, timeline):
    case = service_case
    _, _, body = legacy_request(case, family, timeline)
    before, changes = snapshot(case.service), case.service.store.conn.total_changes
    for key in ("legacy-key", None):
        with pytest.raises(RetiredRouteError) as error:
            call_service(case, family, timeline, body, key)
        assert error.value.status == 410
        assert error.value.details["reason"] == "timeline_commit_required"
        assert snapshot(case.service) == before
        assert case.service.store.conn.total_changes == changes


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("timeline", STATES)
def test_service_refusal_precedes_accepted_retry_lookup(service_case, monkeypatch, family, timeline):
    case = service_case
    _, _, body = legacy_request(case, family, timeline)
    before = snapshot(case.service)

    def replay(*args, **kwargs):
        pytest.fail("retired writer consulted accepted legacy retries")

    monkeypatch.setattr(case.service, "_command_replay", replay)
    with pytest.raises(RetiredRouteError):
        call_service(case, family, timeline, body, "exact-old-legacy-retry")
    assert snapshot(case.service) == before


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("timeline", STATES)
def test_http_authenticated_legacy_family_refuses_without_writes(http_case, monkeypatch, family, timeline):
    case = http_case
    method, path, body = legacy_request(case, family, timeline)
    before, changes = snapshot(case.service), case.service.store.conn.total_changes
    reader_token, _ = case.daemon.credentials.provision("reader", ["projects:read"])
    for client, status in ((WorkspaceClient(case.daemon.endpoint, None), 401),
                           (WorkspaceClient(case.daemon.endpoint, reader_token), 401)):
        with pytest.raises(ApiError) as error:
            client._request(method, path, body=json.dumps(body).encode(),
                            headers={"Content-Type": "application/json", "Idempotency-Key": "legacy-key"})
        assert error.value.status == status
        assert snapshot(case.service) == before
        assert case.service.store.conn.total_changes == changes

    def replay(*args, **kwargs):
        pytest.fail("retired HTTP writer consulted accepted legacy retries")

    monkeypatch.setattr(case.service, "_command_replay", replay)
    for key in ("legacy-key", "exact-old-legacy-retry"):
        with pytest.raises(ApiError) as error:
            case.client._request(method, path, body=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Idempotency-Key": key})
        assert error.value.status == 410
        assert error.value.code == "retired_route"
        # createTimelineDocument already retires in the handler, before service.
        if family != "create_timeline_document":
            assert error.value.details["reason"] == "timeline_commit_required"
        assert snapshot(case.service) == before
        assert case.service.store.conn.total_changes == changes


def test_service_publish_parent_composition_refuses_tracked_timeline_without_writes(service_case):
    case = service_case
    _, _, body = legacy_request(case, "publish_parent_composition", "tracked")
    before, changes = snapshot(case.service), case.service.store.conn.total_changes
    for key in ("legacy-key", "legacy-key"):
        with pytest.raises(RuntimeErrorBase) as error:
            call_service(case, "publish_parent_composition", "tracked", body, key)
        assert error.value.status == 409
        assert error.value.details["reason"] == "timeline_commit_required"
        assert snapshot(case.service) == before
        assert case.service.store.conn.total_changes == changes


def test_http_publish_parent_composition_refuses_tracked_timeline_without_writes(http_case):
    case = http_case
    method, path, body = legacy_request(case, "publish_parent_composition", "tracked")
    before, changes = snapshot(case.service), case.service.store.conn.total_changes
    with pytest.raises(ApiError) as error:
        case.client._request(method, path, body=json.dumps(body).encode(),
                             headers={"Content-Type": "application/json", "Idempotency-Key": "legacy-key"})
    assert error.value.status == 409
    assert error.value.details["reason"] == "timeline_commit_required"
    assert snapshot(case.service) == before
    assert case.service.store.conn.total_changes == changes


def command_body(case, commands):
    timeline = case.service.get_project_timeline(case.project, "tracked")
    return {"api_version": 1, "project_id": case.project, "timeline_id": "tracked",
            "base_revision_id": timeline["head_revision_id"],
            "base_publication_id": timeline["head_publication_id"], "commands": commands}


def test_service_actual_bootstrap_command_restore_and_exact_retries(service_case, monkeypatch):
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document

    case = service_case
    service = case.service
    before = snapshot(service)
    created = service.create_timeline(case.project, "tracked", idempotency_key="tracked-create")
    assert snapshot(service) == before
    initial = service.get_project_timeline(case.project, "tracked")
    assert initial["head_revision_id"] == created["data"]["head_revision_id"]
    assert initial["head_publication_id"] == created["data"]["head_publication_id"]
    history = service.list_timeline_commits(case.project, "tracked", authorize=lambda: None)["items"]
    assert len(history) == 1
    bootstrap = history[0]
    assert bootstrap["intent"] == "bootstrap" and bootstrap["previous"] is None
    assert bootstrap["receipt"]["command_kind"] == "parent_composition.publish"
    assert bootstrap["publication_id"] == initial["head_publication_id"]
    document = service._timeline_commits()[0].revision_closure(case.project, "tracked", initial["head_revision_id"])
    assert document["parent_revision"]["payload"]["clips"] == []
    assert document["shot_revisions"] == document["internal_timeline_revisions"] == []

    def forbidden(*args, **kwargs):
        pytest.fail("bootstrap, commit or restore called the retired public publisher or renderer")

    monkeypatch.setattr(service, "publish_parent_composition", forbidden)
    monkeypatch.setattr("runtime_protocol.service.evaluate_closure", forbidden)
    # Exercise a second creation while the public publisher is unavailable.
    service.create_timeline(case.project, "second", idempotency_key="second-create")
    command = capture_track_create(bundle_from_document(document), "parent", {"id": "video", "kind": "visual"})
    body = command_body(case, [command])
    accepted = service.commit_timeline(case.project, "tracked", body, idempotency_key="real-command",
        publisher="editor", invocation_path=route_path(case.project, "tracked"), authorize=lambda: None)
    assert accepted["receipt"]["command_kind"] == "timeline.commit"
    assert accepted["data"]["canonical_document"]["parent_revision"]["payload"]["config"]["tracks"] == [
        {"id": "video", "kind": "visual"}]
    guards = {"expected_head": accepted["data"]["accepted_revision_id"],
              "expected_publication_id": accepted["receipt"]["receipt_id"]}
    path = route_path(case.project, "tracked", f"composition-revisions/{initial['head_revision_id']}/restore")
    def restore():
        return service.restore_project_parent_composition_revision(
            case.project, "tracked", initial["head_revision_id"], guards, idempotency_key="real-restore",
            publisher="editor", invocation_path=path, authorize=lambda: None)
    restored = restore()
    assert restored["data"]["canonical_document"] == document
    assert restored["receipt"]["command_kind"] == "timeline.commit"
    entry = service.list_timeline_commits(case.project, "tracked", authorize=lambda: None)["items"][-1]
    assert entry["records"]["restored_from"]["revision_id"] == initial["head_revision_id"]
    before = snapshot(service)
    assert restore() == restored
    assert service.commit_timeline(case.project, "tracked", body, idempotency_key="real-command",
        publisher="editor", invocation_path=route_path(case.project, "tracked"), authorize=lambda: None) == accepted
    assert snapshot(service) == before
    with pytest.raises(RuntimeErrorBase) as error:
        service.restore_project_parent_composition_revision(
            case.project, "tracked", initial["head_revision_id"], guards, idempotency_key="stale-restore",
            publisher="editor", invocation_path=path, authorize=lambda: None)
    assert error.value.status == 409 and error.value.details["reason"] == "stale_head"
    assert snapshot(service) == before


def test_http_actual_create_command_restore_rename_and_ordinary_artifact_metadata(http_case):
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document

    case = http_case
    before = case.service._timeline_commits()[0].head(case.project, "tracked")
    renamed = case.client.rename_timeline(case.project, "tracked", "Display name", idempotency_key="rename")
    assert renamed["name"] == "Display name"
    assert case.service._timeline_commits()[0].head(case.project, "tracked") == before
    created = case.client.create_timeline(case.project, "http-empty", idempotency_key="http-create")
    assert created["head_revision_id"] and created["head_publication_id"]
    document = case.service._timeline_commits()[0].revision_closure(
        case.project, "http-empty", created["head_revision_id"])
    command = capture_track_create(bundle_from_document(document), "parent", {"id": "audio", "kind": "audio"})
    body = {"api_version": 1, "project_id": case.project, "timeline_id": "http-empty",
            "base_revision_id": created["head_revision_id"],
            "base_publication_id": created["head_publication_id"], "commands": [command]}
    accepted = case.client.commit_timeline(case.project, "http-empty", body, idempotency_key="http-command")
    assert accepted["receipt"]["command_kind"] == "timeline.commit"
    assert accepted["data"]["canonical_document"]["parent_revision"]["payload"]["config"]["tracks"] == [
        {"id": "audio", "kind": "audio"}]
    restored = case.client.restore_project_parent_composition_revision(
        case.project, "http-empty", created["head_revision_id"],
        expected_head=accepted["data"]["accepted_revision_id"],
        expected_publication_id=accepted["receipt"]["receipt_id"], idempotency_key="http-restore")
    assert restored["receipt"]["command_kind"] == "timeline.commit"
    assert restored["data"]["canonical_document"] == document
    document = case.client.create_document(case.project, "notes", "artifact.notes", {"title": "draft"},
                                           idempotency_key="notes-create")
    updated = case.client.update_document(case.project, "notes", expected_version=document["version"],
                                           content={"title": "final"}, idempotency_key="notes-update")
    assert updated["content"] == {"title": "final"}
    assert case.service._timeline_commits()[0].head(case.project, "tracked") == before
