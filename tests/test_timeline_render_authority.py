"""The retired publication route cannot save a timeline or admit render work."""
from __future__ import annotations

import hashlib

import pytest

from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import RetiredRouteError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.util import canonical_json
from tests.http_helpers import Api
from test_timeline_commit_port import PreparedProvider
from test_timeline_render_publication import _claim, _digest, _publication_body, _settle


def _ready_authoring_attempt(service):
    project = service.create_project({"slug": "publication", "name": "Publication"})
    child_cap, author_cap, render_cap = "test.child", "rendering.assemble_timeline", "rendering.render"
    digests = {cap: _digest(cap) for cap in (child_cap, author_cap, render_cap)}
    for cap in digests:
        service.register_capability({"capability_id": cap, "definition_digest": digests[cap]})
    service.register_executor(
        {"executor_id": "worker", "capabilities": list(digests), "max_concurrency": 4},
        idempotency_key="register-worker",
    )
    service.register_timeline_commit_provider(PreparedProvider())
    service.create_timeline(project["id"], "main", name="Main", idempotency_key="create-timeline")
    children = []
    for index in range(2):
        children.append(service.create_task({
            "project": project["id"], "capability_id": child_cap, "capability_digest": digests[child_cap],
            "input_object_ids": [], "spec": {"index": index}, "idempotency_key": f"child-{index}",
        }))
    child_ids = [value["task"]["id"] for value in children]
    author = service.create_task({
        "project": project["id"], "capability_id": author_cap, "capability_digest": digests[author_cap],
        "input_object_ids": [], "idempotency_key": "author",
        "spec": {"runtime_dependencies": {"edges": [
            {"from_task_id": task_id, "to": "self", "requires_event": "task.succeeded", "fence": "runtime_task"}
            for task_id in child_ids
        ], "aggregation": {"kind": "ordered_cas_inputs"}}},
    })
    attempts = {_claim(service, child_cap, f"claim-child-{index}")["task_id"]: None for index in range(2)}
    # Claims may arrive in either order; settle deliberately in reverse.
    for index, task_id in enumerate(list(attempts)):
        attempts[task_id] = service.store.conn.execute("SELECT attempt_id FROM tasks WHERE id=?", (task_id,)).fetchone()[0]
    claims = {}
    for task_id in child_ids:
        row = service.store.conn.execute("SELECT * FROM attempts WHERE task_id=?", (task_id,)).fetchone()
        claims[task_id] = {"attempt_id": row["id"], "lease_id": row["lease_id"], "fence": row["fence"], "runtime_epoch": row["runtime_epoch"]}
    _settle(service, claims[child_ids[1]], "settle-second", "second")
    _settle(service, claims[child_ids[0]], "settle-first", "first")
    return project, author, _claim(service, author_cap, "claim-author"), digests[render_cap]


@pytest.fixture(params=["service", "http"])
def publication(request, tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    daemon = None
    if request.param == "http":
        daemon = RuntimeDaemon(root, support_root=tmp_path / "support").start()
        service = daemon.service
        token, _ = daemon.credentials.provision("publication-worker", ["worker:execute"])
        api = Api(daemon.endpoint, token)
    else:
        service = RuntimeService(root)
        api = None
    try:
        project, author, attempt, render_digest = _ready_authoring_attempt(service)
        service.create_timeline(project["id"], "empty", idempotency_key="empty-bootstrap")
        yield service, api, author, attempt, _publication_body(attempt, render_digest)
    finally:
        if daemon:
            daemon.stop()
        else:
            service.close()


def _state(service):
    # Include all tables: canonical projections/revisions/head/history, receipts,
    # events/sequences, tasks/admissions/leases/checkpoints and object custody.
    conn = service.store.conn
    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    rows = {table: [tuple(row) for row in conn.execute('SELECT * FROM "' + table.replace('"', '""') + '"')]
            for table in tables}
    files = {str(path.relative_to(service.store.root)): hashlib.sha256(path.read_bytes()).hexdigest()
             for directory in (service.store.cas_root, service.store.staging_root)
             for path in directory.rglob("*") if path.is_file()}
    return rows, files, conn.total_changes


def _refuse(publication, body, key, *, attempt_id=None):
    service, api, _, attempt, _ = publication
    attempt_id = attempt_id or attempt["attempt_id"]
    before = _state(service)
    if api:
        with pytest.raises(RuntimeError) as caught:
            api.request("POST", f"/v1/attempts/{attempt_id}/publish-timeline-render", body,
                        headers={"Idempotency-Key": key})
        assert caught.value.status == 410
        error = caught.value.detail
    else:
        with pytest.raises(RetiredRouteError) as caught:
            service.publish_timeline_render(attempt_id, body, idempotency_key=key)
        assert caught.value.status == 410
        error = caught.value.as_dict()
    assert error["code"] == "retired_route"
    assert error["details"] == {
        "reason": "command_required",
        "replacement": "POST /v1/projects/{project_id}/timelines/{timeline_id}/commit",
    }
    assert _state(service) == before


@pytest.mark.parametrize("timeline_id", ["main", "empty", "unused"])
def test_publication_refuses_existing_bootstrapped_and_fresh_ids_without_effects(publication, timeline_id):
    body = {**publication[-1], "timeline_id": timeline_id}
    _refuse(publication, body, "publish")
    _refuse(publication, body, "publish")
    _refuse(publication, {**body, "config": {"opaque": "changed"}}, "publish")


def test_refusal_precedes_payload_lease_and_attempt_lookup(publication):
    _refuse(publication, {}, "missing-fields", attempt_id="unused-attempt")
    _refuse(publication, {**publication[-1], "fence": 0}, "stale-fence")
    # Direct/internal callers also have no missing-key exemption.
    service = publication[0]
    before = _state(service)
    with pytest.raises(RetiredRouteError):
        service.publish_timeline_render("unused-attempt", None)
    assert _state(service) == before


@pytest.mark.parametrize("state", ["prepared", "published"])
def test_old_checkpoint_identity_cannot_resume_or_replay(publication, state):
    service, _, author, attempt, body = publication
    task_id = author["task"]["id"]
    frozen = {key: body.get(key) for key in (
        "timeline_id", "expected_version", "config", "registry", "render", "slug", "name",
    )}
    request_hash = hashlib.sha256(canonical_json(frozen).encode()).hexdigest()
    service.store.prepare_timeline_render_publication(
        task_id, attempt["attempt_id"], attempt["fence"], attempt["runtime_epoch"], request_hash, frozen,
    )
    if state == "published":
        # Seed only the legacy task checkpoint, not accepted timeline history.
        # Its render link is a real ordinary admission; the retired method must
        # never trust this cached result, even for the exact old request hash.
        render = service.create_task({
            "project": attempt["project_id"], "capability_id": "rendering.render",
            "capability_digest": body["render"]["capability_digest"], "idempotency_key": "old-render",
            "spec": {"params": {"timeline_ref": "main", "expected_version": 1}},
        })
        result = {"checkpoint_state": "published", "render_task_id": render["task"]["id"]}
        with service.store._transaction():
            service.store.complete_timeline_render_publication(
                task_id, attempt_id=attempt["attempt_id"], fence=attempt["fence"],
                runtime_epoch=attempt["runtime_epoch"], timeline_id="main", timeline_version=1,
                render_task_id=render["task"]["id"], render_run_id=render["run"]["id"], result=result,
            )
    checkpoint = service.store.timeline_render_publication(task_id)
    assert checkpoint["request_hash"] == request_hash and checkpoint["state"] == state
    _refuse(publication, body, "publish")
    _refuse(publication, body, "another-key")
    _refuse(publication, {**body, "registry": {"assets": {}, "opaque": True}}, "publish")
