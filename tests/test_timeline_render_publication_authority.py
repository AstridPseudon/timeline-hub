"""Legacy publication cannot overwrite tracked history or choose its own target."""
from __future__ import annotations

import base64
import hashlib
from types import SimpleNamespace

import pytest

from runtime_protocol.errors import ConflictError, RetiredRouteError, RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.util import canonical_json
from test_timeline_render_publication import _publication_body, _ready_authoring_attempt
from test_timeline_producer_guards import _body as _producer_body
from test_timeline_producer_guards import _bytes as _producer_bytes
from test_timeline_producer_guards import _digest as _producer_digest
from test_timeline_producer_guards import _settle as _settle_proposal


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


def _settle_json_child(service, attempt, key, value):
    raw = value.encode()
    return service.settle_attempt(
        attempt["attempt_id"],
        {**{field: attempt[field] for field in ("lease_id", "fence", "runtime_epoch")},
         "outputs": [{"name": "primary", "output_port": "primary", "kind": "object",
                      "filename": "primary.json", "digest": _producer_digest(raw),
                      "size": len(raw), "media_type": "application/json", "durability": "durable",
                      "data_base64": base64.b64encode(raw).decode()}]},
        idempotency_key=key,
    )


@pytest.fixture
def native_target_isolation(tmp_path, astrid_importable):
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    try:
        project = service.create_project({"slug": "target-isolation", "name": "Target isolation"})["id"]
        service.create_timeline(project, "timelineA", idempotency_key="timeline-a")
        service.create_timeline(project, "timelineB", idempotency_key="timeline-b")

        # Establish the tracked canonical A state through the native provider.
        a_head = service.get_project_timeline(project, "timelineA")
        a_document = service._timeline_commits()[0].revision_closure(
            project, "timelineA", a_head["head_revision_id"],
        )
        a_command = capture_track_create(
            bundle_from_document(a_document), "parent", {"id": "tracked-a", "kind": "visual"},
        )
        service.commit_timeline(
            project, "timelineA",
            {"api_version": 1, "project_id": project, "timeline_id": "timelineA",
             "base_revision_id": a_head["head_revision_id"],
             "base_publication_id": a_head["head_publication_id"], "commands": [a_command]},
            idempotency_key="track-a", publisher="editor",
            invocation_path=route_path(project, "timelineA"), authorize=lambda: None,
        )
        a_head = service.get_project_timeline(project, "timelineA")
        a_history = service.list_timeline_commits(project, "timelineA", authorize=lambda: None)
        a_closure = service._timeline_commits()[0].revision_closure(
            project, "timelineA", a_head["head_revision_id"],
        )

        b_head = service.get_project_timeline(project, "timelineB")
        target = {"project_id": project, "timeline_id": "timelineB",
                  "base_revision_id": b_head["head_revision_id"],
                  "base_publication_id": b_head["head_publication_id"]}
        proposal_capability = "fixture.target-isolation-producer"
        child_capability = "fixture.target-isolation-input"
        proposal_digest = _producer_digest(proposal_capability.encode())
        child_digest = _producer_digest(child_capability.encode())
        for capability, digest in ((proposal_capability, proposal_digest),
                                    (child_capability, child_digest)):
            service.register_capability({"capability_id": capability, "definition_digest": digest})
        render_capability = "rendering.render"
        render_digest = _producer_digest(render_capability.encode())
        service.register_capability({"capability_id": render_capability,
                                      "definition_digest": render_digest})
        service.register_executor(
            {"executor_id": "target-isolation-worker",
             "capabilities": [proposal_capability, child_capability, render_capability]},
            idempotency_key="target-isolation-worker",
        )

        children = []
        for index in range(2):
            child = service.create_task({
                "project": project, "capability_id": child_capability,
                "capability_digest": child_digest, "input_object_ids": [],
                "spec": {"index": index}, "idempotency_key": f"target-input-{index}",
            })
            claim = service.claim_next({
                "executor_id": "target-isolation-worker", "capability_ids": [child_capability],
                "runtime_epoch": service.health()["runtime_epoch"],
            }, idempotency_key=f"claim-target-input-{index}")
            _settle_json_child(service, claim, f"settle-target-input-{index}", f"input-{index}")
            children.append(child["task"]["id"])

        producer_spec = {
            "runtime_dependencies": {
                "publication": {"admitted_target": target},
                "edges": [{"from_task_id": child, "to": "self", "requires_event": "task.succeeded",
                            "fence": "runtime_task"} for child in children],
                "aggregation": {"kind": "ordered_cas_inputs"},
            },
            "outputs": {"authoring_proposal": {
                "type": "file", "artifact_type": "timeline/authoring-proposal",
            }},
        }
        producer_task = service.create_task({
            "project": project, "capability_id": proposal_capability,
            "capability_digest": proposal_digest, "input_object_ids": [],
            "spec": producer_spec, "idempotency_key": "target-isolation-producer",
        })
        attempt = service.claim_next({
            "executor_id": "target-isolation-worker", "capability_ids": [proposal_capability],
            "runtime_epoch": service.health()["runtime_epoch"],
        }, idempotency_key="claim-target-isolation-producer")

        b_document = service._timeline_commits()[0].revision_closure(
            project, "timelineB", target["base_revision_id"],
        )
        proposal_command = capture_track_create(
            bundle_from_document(b_document), "parent",
            {"id": "proposed-b", "kind": "visual", "opaque": [1.0, -0.0, False]},
        )
        proposal = {
            "schema_version": 1,
            "producer": {"task_id": attempt["task_id"], "attempt_id": attempt["attempt_id"],
                         "executor_id": "target-isolation-worker", "fence": attempt["fence"],
                         "runtime_epoch": attempt["runtime_epoch"]},
            "admitted_target": target,
            "rationale": "Reviewed target-isolated proposal",
            "commands": [proposal_command],
        }
        proposal["proposal_digest"] = _producer_digest(_producer_bytes(proposal))
        case = SimpleNamespace(
            service=service, project=project, target=target, proposal=proposal,
            task=producer_task["task"]["id"], attempt=attempt,
            pin={**proposal["producer"], "admitted_target": target,
                 "proposal_digest": proposal["proposal_digest"]},
            a_head=a_head, a_history=a_history, a_closure=a_closure,
        )
        _settle_proposal(case)
        yield case
    finally:
        service.close()


def _submit_native_producer(case, *, body=None, timeline_id="timelineB", key="target-isolation-commit"):
    body = _producer_body(case) if body is None else body
    return case.service.commit_timeline(
        case.project, timeline_id, body, idempotency_key=key, publisher="requester",
        invocation_path=route_path(case.project, timeline_id), authorize=lambda: None,
    )


def _historical_render_request(case, accepted, *, timeline_id="timelineB", key="target-isolation-render"):
    parent = accepted["data"]["canonical_document"]["parent_revision"]
    return {
        "project": case.project, "capability_id": "rendering.render",
        "capability_digest": _producer_digest(b"rendering.render"), "input_object_ids": [],
        "idempotency_key": key,
        "spec": {"family": "render", "params": {
            "timeline_ref": timeline_id, "selector": "rendering.remotion",
            "canonical_revision": {
                "project_id": case.project, "timeline_id": timeline_id,
                "revision_id": accepted["data"]["accepted_revision_id"],
                "publication_id": accepted["receipt"]["receipt_id"],
                "content_digest": parent["content_digest"],
            },
        }},
    }


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


@pytest.mark.integration
def test_tracking_is_scoped_to_the_publication_target(native_target_isolation):
    case = native_target_isolation
    accepted = _submit_native_producer(case)
    admitted = case.service.create_task(_historical_render_request(case, accepted))
    authority = admitted["task"]["spec"]["spec"]["inputs"]["timeline_authority"]

    # The original target-scope assertions map to the native receipt and the
    # historical admission: B succeeds while A remains fully intact.
    assert accepted["data"]["canonical_document"]["parent_revision"]["payload"]["config"]["tracks"] == [
        {"id": "proposed-b", "kind": "visual", "opaque": [1.0, -0.0, False]},
    ]
    assert authority["project_id"] == case.project
    assert authority["timeline_id"] == "timelineB"
    assert authority["parent_revision_id"] == accepted["data"]["accepted_revision_id"]
    assert authority["publication_id"] == accepted["receipt"]["receipt_id"]
    assert case.service.get_project_timeline(case.project, "timelineA") == case.a_head
    assert case.service.list_timeline_commits(case.project, "timelineA", authorize=lambda: None) == case.a_history
    assert case.service._timeline_commits()[0].revision_closure(
        case.project, "timelineA", case.a_head["head_revision_id"],
    ) == case.a_closure


@pytest.mark.integration
def test_native_target_substitution_refuses_without_writes(native_target_isolation):
    case = native_target_isolation
    body = _producer_body(case)
    body["timeline_id"] = "timelineA"
    before = _state(case.service)
    with pytest.raises(RuntimeErrorBase) as error:
        _submit_native_producer(case, body=body, timeline_id="timelineA", key="wrong-target")
    assert error.value.details["reason"] in {
        "producer_attempt_mismatch", "producer_dependency_unavailable",
    }
    assert _state(case.service) == before


def test_legacy_head_without_canonical_publication_remains_publishable(service):
    _, _, attempt, render_digest = _ready_authoring_attempt(service, legacy_parent=True)
    head = service.store.conn.execute(
        "SELECT revision_id, publication_id FROM parent_composition_heads WHERE timeline_id='main'",
    ).fetchone()
    assert head["revision_id"] == "legacy-parent" and head["publication_id"] is None
    result = service.publish_timeline_render(attempt["attempt_id"], _publication_body(attempt, render_digest),
                                            idempotency_key="publish")
    assert result["timeline_version"] == 2
