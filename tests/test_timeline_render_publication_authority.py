"""Legacy publication cannot overwrite tracked history or choose its own target."""
from __future__ import annotations

import base64
import copy
import hashlib

import pytest

from precut_realm_fixture import load_precut_realm_fixture
from runtime_protocol.errors import ConflictError, RetiredRouteError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_baseline import verify_baseline
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.util import canonical_json
from test_timeline_render_publication import _publication_body, _ready_authoring_attempt


@pytest.fixture
def service(tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    value = RuntimeService(root)
    try:
        yield value
    finally:
        value.close()


def _state(service):
    return (tuple(service.store.conn.iterdump()),
            {(root.name, str(path.relative_to(root))): path.read_bytes()
             for root in (service.store.cas_root, service.store.staging_root)
             for path in root.rglob("*") if path.is_file()})


def _refused(service, attempt, body, reason):
    before, changes = _state(service), service.store.conn.total_changes
    with pytest.raises(ConflictError) as error:
        service.publish_timeline_render(attempt["attempt_id"], body, idempotency_key="refused")
    assert error.value.details["reason"] == reason
    assert _state(service) == before
    assert service.store.conn.total_changes == changes


def _track(service, project):
    commits = service._timeline_commits()[0]
    return commits.bootstrap(project, "main", authorize=lambda: None)


def _publication_checkpoint(service, author, attempt, body, *, state, result=None):
    frozen = {
        "timeline_id": body["timeline_id"],
        "expected_version": body["expected_version"],
        "config": body["config"],
        "registry": body["registry"],
        "render": body["render"],
        "slug": body.get("slug"),
        "name": body.get("name"),
    }
    request_hash = hashlib.sha256(canonical_json(frozen).encode()).hexdigest()
    service.store.prepare_timeline_render_publication(
        author["task"]["id"], attempt["attempt_id"], body["fence"], body["runtime_epoch"], request_hash, frozen,
    )
    if state == "published":
        service.store.conn.execute(
            "UPDATE timeline_render_publications SET state='published', timeline_id=?, timeline_version=?, result_json=? "
            "WHERE authoring_task_id=?",
            (body["timeline_id"], body["expected_version"] + 1, canonical_json(result), author["task"]["id"]),
        )


def _digest(value):
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def _ready_legacy_authoring_attempt(service, project_id, timeline_id):
    child_cap = "test.child"
    author_cap = "rendering.assemble_timeline"
    render_cap = "rendering.render"
    digests = {cap: _digest(cap) for cap in (child_cap, author_cap, render_cap)}
    for capability_id, definition_digest in digests.items():
        service.register_capability({"capability_id": capability_id, "definition_digest": definition_digest})
    service.register_executor(
        {"executor_id": "legacy-worker", "capabilities": list(digests), "max_concurrency": 4},
        idempotency_key="register-legacy-worker",
    )
    child_ids = []
    for index in range(2):
        child = service.create_task({
            "project": project_id, "capability_id": child_cap, "capability_digest": digests[child_cap],
            "input_object_ids": [], "spec": {"index": index}, "idempotency_key": f"legacy-child-{index}",
        })
        child_ids.append(child["task"]["id"])
    author = service.create_task({
        "project": project_id, "capability_id": author_cap, "capability_digest": digests[author_cap],
        "input_object_ids": [], "idempotency_key": "legacy-author",
        "spec": {"runtime_dependencies": {
            "publication": {"timeline_id": timeline_id, "expected_version": 1},
            "edges": [
                {"from_task_id": child_id, "to": "self", "requires_event": "task.succeeded", "fence": "runtime_task"}
                for child_id in child_ids
            ],
            "aggregation": {"kind": "ordered_cas_inputs"},
        }},
    })
    child_attempts = {}
    for index, child_id in enumerate(child_ids):
        claimed = service.claim_next(
            {"executor_id": "legacy-worker", "capability_ids": [child_cap],
             "runtime_epoch": service.health()["runtime_epoch"]},
            idempotency_key=f"claim-legacy-child-{index}",
        )
        child_attempts[child_id] = claimed
    for index, child_id in enumerate(reversed(child_ids)):
        claimed = child_attempts[child_id]
        raw = f"legacy-child-{index}".encode()
        service.settle_attempt(
            claimed["attempt_id"],
            {"lease_id": claimed["lease_id"], "fence": claimed["fence"],
             "runtime_epoch": claimed["runtime_epoch"], "outputs": [{
                 "digest": "sha256:" + hashlib.sha256(raw).hexdigest(),
                 "data_base64": base64.b64encode(raw).decode(),
                 "media_type": "text/plain", "name": "primary", "role": "primary", "is_primary": True,
             }]},
            idempotency_key=f"settle-legacy-child-{index}",
        )
    attempt = service.claim_next(
        {"executor_id": "legacy-worker", "capability_ids": [author_cap],
         "runtime_epoch": service.health()["runtime_epoch"]},
        idempotency_key="claim-legacy-author",
    )
    return attempt, digests[render_cap]


def _legacy_publication_body(service, project_id, timeline_id, attempt, render_digest):
    parent = service.get_project_parent_composition_revision(
        project_id, timeline_id, service.get_project_timeline(project_id, timeline_id)["head_revision_id"],
    )
    return {
        "lease_id": attempt["lease_id"], "fence": attempt["fence"], "runtime_epoch": attempt["runtime_epoch"],
        "timeline_id": timeline_id, "expected_version": 1,
        "config": copy.deepcopy(parent["payload"]["config"]),
        "registry": copy.deepcopy(parent["payload"]["registry"]),
        "render": {"capability_id": "rendering.render", "capability_digest": render_digest,
                   "spec": {"capability_id": "rendering.render", "kind": "executor",
                             "inputs": {"output_name": "final.mp4"}, "outputs": {}}},
    }


def _commit_body(project_id, timeline_id, head, command):
    return {
        "api_version": 1, "project_id": project_id, "timeline_id": timeline_id,
        "base_revision_id": head["revision_id"], "base_publication_id": head["publication_id"],
        "commands": [command], "source": {"via": "python"},
    }


def test_retired_writer_refuses_before_lookup_without_writes(service):
    before = _state(service)
    with pytest.raises(RetiredRouteError) as error:
        service.publish_timeline_render("missing-attempt", None)
    assert error.value.status == 410
    assert error.value.details == {
        "reason": "command_required",
        "replacement": "POST /v1/projects/{project_id}/timelines/{timeline_id}/commit",
    }
    assert _state(service) == before


def test_tracked_target_refuses_without_invalidating_canonical_history(service):
    project, author, attempt, render_digest = _ready_authoring_attempt(service)
    head = _track(service, project["id"])
    _refused(service, attempt, _publication_body(attempt, render_digest), "timeline_commit_required")
    assert service._timeline_commits()[0].head(project["id"], "main") == head
    assert service.store.timeline_render_publication(author["task"]["id"]) is None


def test_existing_same_project_unadmitted_target_refuses_before_checkpoint(service):
    project, author, attempt, render_digest = _ready_authoring_attempt(service)
    service.create_timeline(project["id"], "other", idempotency_key="other")
    # Historical/adversarial neighbor only; this is not a normal-create positive.
    service.store.conn.execute(
        "INSERT INTO project_documents SELECT 'timeline:other', project_id, kind, content_json, version, "
        "created_at, updated_at FROM project_documents WHERE id='timeline:main'",
    )
    body = {**_publication_body(attempt, render_digest), "timeline_id": "other"}
    _refused(service, attempt, body, "publication_target_mismatch")
    assert service.store.timeline_render_publication(author["task"]["id"]) is None


@pytest.mark.parametrize("publication", [
    {}, False, [], "main", {"timeline_id": None}, {"timeline_id": []}, {"timeline_id": " "},
    {"timeline_id": "main", "admitted_target": None},
    {"timeline_id": "main", "admitted_target": {"timeline_id": "main"}},
])
def test_missing_or_malformed_admitted_target_fails_closed(service, publication):
    _, _, attempt, render_digest = _ready_authoring_attempt(service, publication=publication)
    _refused(service, attempt, _publication_body(attempt, render_digest), "publication_target_unavailable")


def test_inconsistent_native_target_cannot_override_legacy_admission(service):
    # Build the declaration at admission, not from the publication worker body.
    target = {"project_id": "foreign", "timeline_id": "other", "base_revision_id": "base",
              "base_publication_id": "receipt"}
    publication = {"timeline_id": "main", "admitted_target": target}
    _, _, attempt, render_digest = _ready_authoring_attempt(service, publication=publication)
    _refused(service, attempt, _publication_body(attempt, render_digest), "publication_target_unavailable")


def test_corrupt_immutable_spec_cannot_supply_target_authority(service):
    _, author, attempt, render_digest = _ready_authoring_attempt(service)
    service.store.conn.execute(
        "UPDATE task_specs SET body_json='{}' WHERE digest=(SELECT spec_digest FROM tasks WHERE id=?)",
        (author["task"]["id"],),
    )
    _refused(service, attempt, _publication_body(attempt, render_digest), "publication_target_unavailable")


@pytest.mark.xfail(
    strict=True,
    reason="RT07 removes the legacy prepare/write path; preserve this seam assertion until its native replacement is integrated",
)
def test_canonical_tracking_after_prepare_refuses_before_publication_writes(service, monkeypatch):
    project, author, attempt, render_digest = _ready_authoring_attempt(service)
    original = service.store.prepare_timeline_render_publication
    after_tracking = None

    def prepare_then_track(*args, **kwargs):
        nonlocal after_tracking
        value = original(*args, **kwargs)
        _track(service, project["id"])
        after_tracking = _state(service), service.store.conn.total_changes
        return value

    monkeypatch.setattr(service.store, "prepare_timeline_render_publication", prepare_then_track)
    with pytest.raises(ConflictError) as error:
        service.publish_timeline_render(attempt["attempt_id"], _publication_body(attempt, render_digest),
                                        idempotency_key="track-at-seam")
    assert error.value.details["reason"] == "timeline_commit_required"
    assert (_state(service), service.store.conn.total_changes) == after_tracking
    assert service.store.timeline_render_publication(author["task"]["id"])["state"] == "prepared"
    service._timeline_commits()[0].head(project["id"], "main")


def test_retired_writer_refuses_without_prepare_or_publication_writes(service):
    _, author, attempt, render_digest = _ready_authoring_attempt(service)
    body = _publication_body(attempt, render_digest)
    before, changes = _state(service), service.store.conn.total_changes
    with pytest.raises(RetiredRouteError) as error:
        service.publish_timeline_render(attempt["attempt_id"], body, idempotency_key="retired")
    assert error.value.status == 410
    assert (_state(service), service.store.conn.total_changes) == (before, changes)
    assert service.store.timeline_render_publication(author["task"]["id"]) is None


def test_published_checkpoint_replays_read_only_after_live_authority_changes(service):
    _, author, attempt, render_digest = _ready_authoring_attempt(service)
    body = _publication_body(attempt, render_digest)
    result = {
        "checkpoint_state": "published", "authoring_task_id": author["task"]["id"],
        "timeline_id": "main", "timeline_version": 2,
        "render_task_id": "legacy-render", "render_run_id": "legacy-run",
    }
    _publication_checkpoint(service, author, attempt, body, state="published", result=result)
    service.cancel_task_canonical(author["task"]["id"], {}, idempotency_key="cancel")
    service.store.conn.execute("UPDATE tasks SET spec_digest=NULL WHERE id=?", (author["task"]["id"],))
    service.store.conn.execute("UPDATE timelines SET archived_at=created_at WHERE id='main'")
    before, changes = _state(service), service.store.conn.total_changes

    assert service.publish_timeline_render(attempt["attempt_id"], body, idempotency_key="replay") == result
    with pytest.raises(ConflictError, match="payload changed"):
        service.publish_timeline_render(attempt["attempt_id"], {**body, "config": {}}, idempotency_key="changed")
    assert (_state(service), service.store.conn.total_changes) == (before, changes)


def test_prepared_checkpoint_remains_retired_without_recovery_write(service):
    _, author, attempt, render_digest = _ready_authoring_attempt(service)
    body = _publication_body(attempt, render_digest)
    _publication_checkpoint(service, author, attempt, body, state="prepared")
    before, changes = _state(service), service.store.conn.total_changes

    with pytest.raises(RetiredRouteError) as error:
        service.publish_timeline_render(attempt["attempt_id"], body, idempotency_key="prepared-retry")
    assert error.value.status == 410
    assert (_state(service), service.store.conn.total_changes) == (before, changes)


def test_exact_published_checkpoint_replays_before_live_target_changes(service):
    project, author, attempt, render_digest = _ready_authoring_attempt(service)
    body = {**_publication_body(attempt, render_digest), "config": {"clips": [], "tracks": []}, "registry": {}}
    result = service.publish_timeline_render(attempt["attempt_id"], body, idempotency_key="publish")
    _track(service, project["id"])
    service.cancel_task_canonical(author["task"]["id"], {}, idempotency_key="cancel")
    # Fault injection: replay must not depend on even the spec/target remaining live.
    service.store.conn.execute("UPDATE tasks SET spec_digest=NULL WHERE id=?", (author["task"]["id"],))
    service.store.conn.execute("UPDATE timelines SET archived_at=created_at WHERE id='main'")
    before, changes = _state(service), service.store.conn.total_changes
    assert service.publish_timeline_render(attempt["attempt_id"], body, idempotency_key="replay") == result
    with pytest.raises(ConflictError, match="payload changed"):
        service.publish_timeline_render(attempt["attempt_id"], {**body, "config": {}}, idempotency_key="changed")
    assert _state(service) == before
    assert service.store.conn.total_changes == changes


def test_tracking_is_scoped_to_the_publication_target(service):
    project, _, attempt, render_digest = _ready_authoring_attempt(service)
    service.create_timeline(project["id"], "other", idempotency_key="other")
    service._timeline_commits()[0].bootstrap(project["id"], "other", authorize=lambda: None)
    result = service.publish_timeline_render(attempt["attempt_id"], _publication_body(attempt, render_digest),
                                            idempotency_key="publish")
    assert result["timeline_id"] == "main"
    assert result["timeline_version"] == 2


def test_legacy_head_without_canonical_publication_refuses_without_writes(tmp_path):
    captured = load_precut_realm_fixture(tmp_path, variant="music-documents")
    project_id, timeline_id = captured.pins["project_id"], captured.pins["timeline_id"]
    service = RuntimeService(captured.copy_roots[1])
    try:
        assert service.get_project_timeline(project_id, timeline_id)["head_publication_id"] is None
        before_document = verify_baseline(
            service.store.conn, project_id, timeline_id, read_object=service.cas.read,
        )["canonical_document"]
        attempt, render_digest = _ready_legacy_authoring_attempt(service, project_id, timeline_id)
        before = _state(service)
        with pytest.raises(RetiredRouteError) as error:
            service.publish_timeline_render(
                attempt["attempt_id"], _legacy_publication_body(
                    service, project_id, timeline_id, attempt, render_digest,
                ), idempotency_key="retired-legacy-film",
            )
        assert error.value.status == 410
        assert error.value.details["reason"] == "command_required"
        assert _state(service) == before
        assert verify_baseline(
            service.store.conn, project_id, timeline_id, read_object=service.cas.read,
        )["canonical_document"] == before_document
    finally:
        service.close()


@pytest.mark.integration
def test_canonical_equivalent_film_commit_remains_publishable(tmp_path, astrid_importable):
    """The safe replacement for the retired legacy-head publication succeeds.

    The legitimate behavior change is narrow: an untracked legacy render write
    is refused, while the captured film is first admitted as canonical history,
    then committed through the current provider before historical render
    admission.
    """
    from astrid.core.dev.journey import build_app_render_admission
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    assert (astrid_importable / "astrid/sdk/timeline/commit.py").is_file()
    captured = load_precut_realm_fixture(tmp_path, variant="music-documents")
    project_id, timeline_id = captured.pins["project_id"], captured.pins["timeline_id"]
    service = RuntimeService(captured.copy_roots[1])
    try:
        baseline = verify_baseline(
            service.store.conn, project_id, timeline_id, read_object=service.cas.read,
        )["canonical_document"]
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        head = service.get_project_timeline(project_id, timeline_id)
        canonical = service._timeline_commits()[0].revision_closure(
            project_id, timeline_id, head["head_revision_id"],
        )
        assert canonical == baseline
        assert canonical["parent_revision"]["payload"]["clips"][1]["extension"] == {
            "opaque": [None, {"keep": True}],
        }
        assert canonical["dependency_manifest"]["media"]

        command = {
            "schema_version": 1, "op": "timeline.restore", "version": "1", "select": None,
            "args": {"revision_id": head["head_revision_id"],
                     "content_digest": canonical["parent_revision"]["content_digest"]},
            "created": [],
        }
        accepted = service.commit_timeline(
            project_id, timeline_id, _commit_body(project_id, timeline_id, {
                "revision_id": head["head_revision_id"], "publication_id": head["head_publication_id"]}, command),
            idempotency_key="canonical-equivalent-film", publisher="legacy-film-editor",
            invocation_path=route_path(project_id, timeline_id), authorize=lambda: None,
        )
        assert accepted["data"]["canonical_document"] == canonical
        assert accepted["data"]["provider_version"] == "astrid-v1"
        assert accepted["data"]["canonical_document"]["dependency_manifest"]["media"] == \
            canonical["dependency_manifest"]["media"]

        render_digest = _digest("rendering.render")
        service.register_capability({
            "capability_id": "rendering.render", "definition_digest": render_digest,
        })
        service.register_executor(
            {"executor_id": "historical-render-worker", "capabilities": ["rendering.render"]},
            idempotency_key="register-historical-render-worker",
        )
        capability = next(
            item for item in service.list_capabilities()["items"]
            if item["capability_id"] == "rendering.render"
        )
        request = build_app_render_admission(
            project=project_id, timeline_id=timeline_id, output_name="canonical-equivalent-review.mp4",
            capability=capability, token="test-token",
        )
        request = copy.deepcopy(request["body"])
        request["idempotency_key"] = "canonical-equivalent-historical-render"
        parent = accepted["data"]["canonical_document"]["parent_revision"]
        request["spec"]["params"]["canonical_revision"] = {
            "project_id": project_id, "timeline_id": timeline_id,
            "revision_id": accepted["data"]["accepted_revision_id"],
            "publication_id": accepted["receipt"]["receipt_id"],
            "content_digest": parent["content_digest"],
        }
        admitted = service.create_task(request)
        authority = admitted["task"]["spec"]["spec"]["inputs"]["timeline_authority"]
        assert authority["project_id"] == project_id
        assert authority["timeline_id"] == timeline_id
        assert authority["parent_revision_id"] == accepted["data"]["accepted_revision_id"]
        assert authority["publication_id"] == accepted["receipt"]["receipt_id"]
        assert authority["parent_content_digest"] == parent["content_digest"]
    finally:
        service.close()
