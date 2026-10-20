from __future__ import annotations

import base64
import copy
import hashlib
from contextlib import contextmanager

import pytest

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.util import canonical_json, now


def _digest(value: str | bytes) -> str:
    raw = value.encode() if isinstance(value, str) else value
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _claim(service, capability, key):
    return service.claim_next(
        {"executor_id": "worker", "capability_ids": [capability], "runtime_epoch": service.health()["runtime_epoch"]},
        idempotency_key=key,
    )


def _settle(service, attempt, key, value):
    raw = value.encode()
    return service.settle_attempt(
        attempt["attempt_id"],
        {"lease_id": attempt["lease_id"], "fence": attempt["fence"], "runtime_epoch": attempt["runtime_epoch"],
         "outputs": [{"digest": _digest(raw), "data_base64": base64.b64encode(raw).decode(),
                      "media_type": "video/mp4", "name": "primary", "role": "primary", "is_primary": True}]},
        idempotency_key=key,
    )


def _ready_authoring_attempt(service, *, publication=None, legacy_parent=False):
    project = service.create_project({"slug": "publication", "name": "Publication"})
    child_cap, author_cap, render_cap = "test.child", "rendering.assemble_timeline", "rendering.render"
    digests = {cap: _digest(cap) for cap in (child_cap, author_cap, render_cap)}
    for cap, definition_digest in digests.items():
        service.register_capability({"capability_id": cap, "definition_digest": definition_digest})
    service.register_executor(
        {"executor_id": "worker", "capabilities": list(digests), "max_concurrency": 4},
        idempotency_key="register-worker",
    )
    service.create_timeline(project["id"], "main", idempotency_key="create-timeline")
    if legacy_parent:
        service.publish_parent_composition(project["id"], "main", {
            "project_id": project["id"], "timeline_id": "main", "expected_head": None,
            "parent_revision_id": "legacy-parent",
            "parent_composition": {"config": {}, "registry": {}, "clips": [], "occurrences": []},
        }, idempotency_key="legacy-parent")
    # publish_timeline_render still reads the timeline's config document; the retired
    # create_timeline_document route was the only writer, so seed that row directly.
    timestamp = now()
    service.store.conn.execute(
        "INSERT INTO project_documents VALUES (?, ?, ?, ?, 1, ?, ?)",
        ("timeline:main", project["id"], "timeline.composition",
         canonical_json({"slug": "main", "name": "Main", "config": {}, "registry": {}}), timestamp, timestamp),
    )
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
        "spec": {"runtime_dependencies": {
            "publication": {"timeline_id": "main", "expected_version": 1} if publication is None else publication,
            "edges": [
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


def _publication_body(attempt, render_digest):
    return {
        "lease_id": attempt["lease_id"], "fence": attempt["fence"], "runtime_epoch": attempt["runtime_epoch"],
        "timeline_id": "main", "expected_version": 1,
        "config": {"tracks": [{"id": "video", "clips": []}]}, "registry": {"assets": {}},
        "render": {"capability_id": "rendering.render", "capability_digest": render_digest,
                   "spec": {"capability_id": "rendering.render", "kind": "executor", "inputs": {"output_name": "final.mp4"}, "outputs": {}}},
    }


def _native_state(service):
    return (tuple(service.store.conn.iterdump()),
            {(root.name, str(path.relative_to(root))): path.read_bytes()
             for root in (service.store.cas_root, service.store.staging_root)
             for path in root.rglob("*") if path.is_file()})


def _native_pending_render(case):
    checkpoint = case.service.store.timeline_render_publication(case.task)
    pending = checkpoint["prepared"]["pending_render"]
    assert checkpoint["state"] == "prepared"
    assert pending is not None
    return copy.deepcopy(pending)


@contextmanager
def _native_case(tmp_path, astrid_importable):
    from test_timeline_render_publication_authority import native_target_isolation

    cases = native_target_isolation.__wrapped__(tmp_path, astrid_importable)
    case = next(cases)
    try:
        yield case
    finally:
        cases.close()


@pytest.mark.integration
def test_publication_is_fenced_atomic_and_exactly_replayable(tmp_path, astrid_importable):
    from test_timeline_producer_guards import _body as producer_body
    from test_timeline_render_publication_authority import _submit_native_producer

    with _native_case(tmp_path, astrid_importable) as case:
        stale = producer_body(case)
        stale["commands"][0]["args"]["pin"]["fence"] += 1
        before = _native_state(case.service)
        with pytest.raises(RuntimeErrorBase) as error:
            _submit_native_producer(case, body=stale, key="stale-native-publication")
        assert error.value.details["reason"] in {"producer_attempt_mismatch", "producer_dependency_unavailable"}
        assert _native_state(case.service) == before
        assert case.service.store.conn.execute(
            "SELECT COUNT(*) FROM timeline_render_publications",
        ).fetchone()[0] == 0

        accepted = _submit_native_producer(case, key="native-publication")
        head = case.service.get_project_timeline(case.project, "timelineB")
        assert head["version"] == 2
        assert head["head_revision_id"] == accepted["data"]["accepted_revision_id"]
        pending = _native_pending_render(case)
        admitted = case.service.create_task(pending["body"] | {"idempotency_key": pending["idempotency_key"]})
        task = admitted["task"]
        authority = task["spec"]["spec"]["inputs"]["timeline_authority"]
        selector = pending["body"]["spec"]["params"]["canonical_revision"]
        assert {key: authority[key] for key in (
            "project_id", "timeline_id", "parent_revision_id", "publication_id", "parent_content_digest",
        )} == {
            "project_id": selector["project_id"], "timeline_id": selector["timeline_id"],
            "parent_revision_id": selector["revision_id"], "publication_id": selector["publication_id"],
            "parent_content_digest": selector["content_digest"],
        }
        assert "timeline_snapshot" not in task["spec"]["spec"]["inputs"]
        snapshot_ref = task["spec"]["spec"]["timeline_snapshot_ref"]
        assert snapshot_ref["digest"] in task["spec"]["input_object_ids"]
        assert case.service.store.conn.execute(
            "SELECT COUNT(*) FROM timeline_render_publications",
        ).fetchone()[0] == 1
        assert case.service.store.conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'",
        ).fetchone()[0] == 1

        assert _submit_native_producer(case, key="native-publication") == accepted
        assert case.service.create_task(copy.deepcopy(pending["body"]) | {
            "idempotency_key": pending["idempotency_key"],
        }) == admitted

        changed = producer_body(case)
        changed["rationale"] += " changed"
        before = _native_state(case.service)
        with pytest.raises(RuntimeErrorBase):
            _submit_native_producer(case, body=changed, key="native-publication")
        assert _native_state(case.service) == before

        case.service.cancel_task_canonical(case.task, {}, idempotency_key="cancel-native-author")
        assert _submit_native_producer(case, key="native-publication") == accepted
        assert case.service.create_task(copy.deepcopy(pending["body"]) | {
            "idempotency_key": pending["idempotency_key"],
        }) == admitted


@pytest.mark.integration
def test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence(tmp_path, astrid_importable, monkeypatch):
    from test_timeline_producer_guards import _body as producer_body
    from test_timeline_render_publication_authority import _submit_native_producer

    from runtime_protocol.timeline_commit_port import RequestCommitPort

    with _native_case(tmp_path, astrid_importable) as case:
        stale = producer_body(case)
        stale["commands"][0]["args"]["pin"]["fence"] += 1
        before = _native_state(case.service)
        with pytest.raises(RuntimeErrorBase):
            _submit_native_producer(case, body=stale, key="stale-native-fence")
        assert _native_state(case.service) == before
        assert case.service.get_project_timeline(case.project, "timelineB")["version"] == 1

        observed = []
        original = RequestCommitPort.producer_attempt

        def capture_then_supersede(port, pin):
            value = original(port, pin)
            case.service.retry_task(case.task, {}, idempotency_key="supersede-native-proposal")
            observed.append(_native_state(case.service))
            return value

        monkeypatch.setattr(RequestCommitPort, "producer_attempt", capture_then_supersede)
        with pytest.raises(RuntimeErrorBase) as error:
            _submit_native_producer(case, key="superseded-native-proposal")
        assert error.value.details["reason"] in {"producer_attempt_mismatch", "producer_dependency_unavailable"}
        assert observed
        assert _native_state(case.service) == observed[0]
        assert case.service.get_project_timeline(case.project, "timelineB")["version"] == 1
        assert case.service.store.conn.execute(
            "SELECT COUNT(*) FROM timeline_render_publications",
        ).fetchone()[0] == 0
        assert case.service.store.conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'",
        ).fetchone()[0] == 0


@pytest.mark.integration
def test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart(tmp_path, astrid_importable):
    from test_timeline_render_publication_authority import _submit_native_producer

    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    with _native_case(tmp_path, astrid_importable) as case:
        accepted = _submit_native_producer(case, key="restart-native-publication")
        pending = _native_pending_render(case)
        root = case.service.store.root
        case.service.close()
        case.service = RuntimeService(root)
        case.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        try:
            assert _submit_native_producer(case, key="restart-native-publication") == accepted
            admitted = case.service.create_task(pending["body"] | {"idempotency_key": pending["idempotency_key"]})
            authority = admitted["task"]["spec"]["spec"]["inputs"]["timeline_authority"]
            selector = pending["body"]["spec"]["params"]["canonical_revision"]
            assert authority["parent_revision_id"] == selector["revision_id"] == accepted["data"]["accepted_revision_id"]
            assert authority["publication_id"] == selector["publication_id"] == accepted["receipt"]["receipt_id"]
            assert authority["parent_content_digest"] == selector["content_digest"]
            checkpoint = case.service.store.timeline_render_publication(case.task)
            assert checkpoint["state"] == "published"
            assert checkpoint["prepared"]["pending_render"] == pending
            assert checkpoint["render_task_id"] == admitted["task"]["id"]
            assert case.service.create_task(copy.deepcopy(pending["body"]) | {
                "idempotency_key": pending["idempotency_key"],
            }) == admitted
        finally:
            case.service.close()
