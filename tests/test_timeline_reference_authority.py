"""Reference writers retire before lookup/replay, even in an empty project.

Existing reference rows and accepted legacy retries require the genuine pre-cut
realm from rt-m2-precut-fixture. These cases create only projects, empty timeline
bootstraps and ordinary media; they do not fabricate reference/history rows.
Run the whole file through the central restore-integration lane for real HTTP.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from astrid_runtime_client import ApiError, WorkspaceClient
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import RetiredRouteError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from test_shot_composition_runtime import restore_provider as actual_provider  # noqa: F401 (fixture)


FAMILIES = (
    "create_project_reference", "update_project_reference", "archive_project_reference",
    "recover_project_reference", "associate_reference", "set_primary_reference",
    "link_references", "create_reference", "update_reference", "archive_reference",
    "recover_reference",
)
STATES = ("fresh", "unused")


def seed(root, provider):
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    if provider is not None:
        service.register_timeline_commit_provider(provider)
    cases = {}
    for state in STATES:
        project = service.create_project({"slug": state, "name": state.title()})["id"]
        media = service.ingest(project, b"ordinary media", idempotency_key=f"media-{state}")
        cases[state] = SimpleNamespace(project=project, timeline=state, media=media["data"]["object_id"])
    service.create_timeline(cases["fresh"].project, "fresh", idempotency_key="bootstrap")
    return service, cases


@pytest.fixture(params=("neutral", "astrid"))
def service_case(tmp_path, actual_provider, request):
    service, cases = seed(tmp_path / "realm", actual_provider if request.param == "astrid" else None)
    try:
        yield SimpleNamespace(service=service, cases=cases)
    finally:
        service.close()


@pytest.fixture
def http_case(tmp_path, actual_provider):
    root = tmp_path / "realm"
    service, cases = seed(root, actual_provider)
    service.close()
    daemon = RuntimeDaemon(root, support_root=tmp_path / "support", authoring_profile="astrid").start()
    try:
        yield SimpleNamespace(service=daemon.service, cases=cases, daemon=daemon,
                              client=WorkspaceClient(daemon.endpoint, daemon.token))
    finally:
        daemon.stop()


def snapshot(service):
    # Whole DB covers canonical/reference rows, heads, history, receipts, events
    # and sequence counters; total_changes also catches rolled-back SQL writes.
    with service.store._mutex:
        database = tuple(service.store.conn.iterdump())
        objects = {str(path.relative_to(service.store.cas_root)): path.read_bytes()
                   for path in service.store.cas_root.rglob("*") if path.is_file()}
        return database, objects, service.store.conn.total_changes


def reference_request(case, family):
    project, reference = case.project, "uncreated-reference"
    prefix = f"/v1/projects/{project}/references"
    resource = f"{prefix}/{reference}"
    version = {"expected_version": 1}
    requests = {
        "create_project_reference": ("POST", prefix, {
            "reference_id": reference, "kind": "character", "name": "Character", "media_id": case.media}),
        "update_project_reference": ("PATCH", resource, {**version, "name": "Renamed"}),
        "archive_project_reference": ("POST", f"{resource}/archive", version),
        "recover_project_reference": ("POST", f"{resource}/recover", {**version, "version": 1}),
        "associate_reference": ("POST", f"{resource}/associations", {
            "association_id": "association", "media_id": case.media, "role": "canonical"}),
        "set_primary_reference": ("POST", f"{resource}/primary", {**version, "association_id": "association"}),
        "link_references": ("POST", f"/v1/projects/{project}/reference-links", {
            "from_reference_id": reference, "to_reference_id": "uncreated-target", "kind": "related_to"}),
        "create_reference": ("POST", f"/v1/timelines/{case.timeline}/references", {
            "reference_id": reference, "object_id": case.media, "role": "source"}),
        "update_reference": ("PATCH", f"/v1/references/{reference}", {**version, "object_id": case.media}),
        "archive_reference": ("POST", f"/v1/references/{reference}/archive", version),
        "recover_reference": ("POST", f"/v1/references/{reference}/recover", {**version, "version": 1}),
    }
    return requests[family]


def call_service(service, case, family, body, key):
    reference = "uncreated-reference"
    kwargs = {"idempotency_key": key}
    if family in ("archive_project_reference", "recover_project_reference"):
        kwargs["archived"] = family == "archive_project_reference"
        family = "update_project_reference"
    if family in ("create_project_reference", "link_references"):
        args = (case.project, body)
    elif family == "set_primary_reference":
        args = (case.project, reference, "association", body)
    elif family in ("update_project_reference", "associate_reference"):
        args = (case.project, reference, body)
    elif family == "create_reference":
        args = (case.timeline, body)
    else:
        args = (reference, body)
    return getattr(service, family)(*args, **kwargs)


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("state", STATES)
def test_service_reference_writers_refuse_before_lookup_or_replay(service_case, monkeypatch, family, state):
    service, case = service_case.service, service_case.cases[state]
    _, _, body = reference_request(case, family)
    before = snapshot(service)

    def replay(*args, **kwargs):
        pytest.fail("retired reference writer consulted legacy retries")

    monkeypatch.setattr(service, "_command_replay", replay)
    for key in ("reference-request", "old-reference-retry", None):
        with pytest.raises(RetiredRouteError) as error:
            call_service(service, case, family, body, key)
        assert error.value.status == 410
        assert error.value.details["reason"] == "timeline_commit_required"
        assert snapshot(service) == before


@pytest.mark.parametrize("archived", (None, True, False))
def test_service_private_reference_state_writer_is_also_retired(service_case, archived):
    service = service_case.service
    before = snapshot(service)
    with pytest.raises(RetiredRouteError):
        service._update_reference_state("uncreated-reference", {"expected_version": 1}, archived=archived)
    assert snapshot(service) == before


@pytest.mark.parametrize("family", FAMILIES)
@pytest.mark.parametrize("state", STATES)
def test_http_reference_writers_preserve_auth_and_refuse_without_writes(http_case, monkeypatch, family, state):
    case = http_case
    method, path, body = reference_request(case.cases[state], family)
    reader_token, _ = case.daemon.credentials.provision("reader", ["projects:read"])
    before = snapshot(case.service)
    for client in (WorkspaceClient(case.daemon.endpoint, None),
                   WorkspaceClient(case.daemon.endpoint, reader_token)):
        with pytest.raises(ApiError) as error:
            client._request(method, path, body=json.dumps(body).encode(),
                            headers={"Content-Type": "application/json", "Idempotency-Key": "reference-request"})
        assert error.value.status == 401
        assert snapshot(case.service) == before

    def replay(*args, **kwargs):
        pytest.fail("retired HTTP reference writer consulted legacy retries")

    monkeypatch.setattr(case.service, "_command_replay", replay)
    for key in ("reference-request", "old-reference-retry"):
        with pytest.raises(ApiError) as error:
            case.client._request(method, path, body=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Idempotency-Key": key})
        assert error.value.status == 410
        assert error.value.code == "retired_route"
        assert error.value.details["reason"] == "timeline_commit_required"
        assert snapshot(case.service) == before


def test_http_ordinary_media_artifacts_and_project_metadata_remain_writable(http_case):
    case = http_case
    project = case.cases["fresh"].project
    before = case.service.get_project_timeline(project, "fresh")
    media = case.client.ingest_project_object(project, b"new ordinary artifact", media_type="application/octet-stream",
                                               idempotency_key="ordinary-media")
    objects, _ = case.client.list_project_objects(project)
    assert media["object_id"] in {item.object_id for item in objects}
    document = case.client.create_document(project, "notes", "artifact.notes", {"title": "draft"},
                                           idempotency_key="notes-create")
    updated = case.client.update_document(project, "notes", expected_version=document["version"],
                                           content={"title": "final"}, idempotency_key="notes-update")
    assert updated["content"] == {"title": "final"}
    renamed = case.client.update_project(project, name="Renamed", metadata={"note": "ordinary metadata"},
                                          idempotency_key="project-update")
    assert renamed.name == "Renamed"
    assert case.client.list_project_references(project)[0] == []
    after = case.service.get_project_timeline(project, "fresh")
    for field in ("head_revision_id", "head_publication_id", "version"):
        assert after[field] == before[field]
