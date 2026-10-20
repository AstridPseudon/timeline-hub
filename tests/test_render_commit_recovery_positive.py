"""One missing assertion for the real native render recovery mapping.

The unchanged publication tests retain the old cancellation/stale-fence
assertions.  The existing D13 Agent integration covers settled proposal ->
requester ``producer.guard`` commit, lost acknowledgement, restart, exact
retry, and revision-pinned render admission.  This small Runtime case adds
the equivalent actual-film refusal/no-write assertion without rebuilding that
integration fixture or inventing a proposal carrier.
"""
from __future__ import annotations

import copy

import pytest

from runtime_protocol.errors import ConflictError, RuntimeErrorBase

from test_render_commit_publication_positive import actual_agent_source, _submit, native_publication_case
from test_render_native_historical_retry import native_render_case, _move


pytestmark = pytest.mark.integration

def _store_state(service):
    return tuple(service.store.conn.iterdump())


def test_actual_native_producer_refuses_cancelled_superseded_attempt_without_film_writes(native_publication_case):
    """A requester cannot consume a proposal after its live attempt is cancelled."""
    case = native_publication_case
    before_history = case.service.list_timeline_commits(case.project, "film", authorize=lambda: None)
    before_head = case.service.get_project_timeline(case.project, "film")

    original_request = case.request
    case.request = copy.deepcopy(original_request)
    case.request["commands"][0]["args"]["pin"]["fence"] += 1
    with pytest.raises(RuntimeErrorBase) as error:
        _submit(case, "native-stale-producer-fence")
    assert error.value.details["reason"] in {"producer_attempt_mismatch", "producer_dependency_unavailable"}
    assert case.service.list_timeline_commits(case.project, "film", authorize=lambda: None) == before_history
    assert case.service.get_project_timeline(case.project, "film") == before_head
    case.request = original_request

    case.service.retry_task(case.task, {}, idempotency_key="retry-before-settle")
    claimed = case.service.claim_next(
        {"executor_id": "worker", "capability_ids": ["fixture.propose-track"],
         "runtime_epoch": case.service.health()["runtime_epoch"]},
        idempotency_key="claim-before-settle",
    )
    assert claimed["task_id"] == case.task
    cancelled = case.service.cancel_task_canonical(case.task, {}, idempotency_key="cancel-before-settle")
    assert cancelled["data"]["state"] == "cancelled"

    with pytest.raises(RuntimeErrorBase) as error:
        _submit(case, "native-before-settle")
    assert error.value.details["reason"] in {"producer_attempt_mismatch", "producer_dependency_unavailable"}
    assert case.service.list_timeline_commits(case.project, "film", authorize=lambda: None) == before_history
    assert case.service.get_project_timeline(case.project, "film") == before_head
    assert case.service.store.timeline_render_publication(case.task) is None
    assert case.service.store.conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'"
    ).fetchone()[0] == 0


def test_actual_native_acceptance_replays_after_crash_before_render_admission(native_publication_case):
    """The accepted receipt and pending pinned render survive a Runtime restart."""
    case = native_publication_case
    accepted = _submit(case, "native-crash-before-render")
    checkpoint = case.service.store.timeline_render_publication(case.task)
    pending = copy.deepcopy(checkpoint["prepared"]["pending_render"])
    assert checkpoint["state"] == "prepared"
    assert case.service.store.conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'"
    ).fetchone()[0] == 0

    case.service.close()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    try:
        cancelled = case.service.cancel_task_canonical(case.task, {}, idempotency_key="cancel-completed-noop")
        assert cancelled["data"]["state"] == "succeeded"
        replay = _submit(case, "native-crash-before-render")
        assert replay == accepted
        assert case.service.store.timeline_render_publication(case.task)["state"] == "prepared"
        assert case.service.store.conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'"
        ).fetchone()[0] == 0

        admitted = case.service.create_task({**pending["body"], "idempotency_key": pending["idempotency_key"]})
        authority = admitted["task"]["spec"]["spec"]["inputs"]["timeline_authority"]
        selector = pending["body"]["spec"]["params"]["canonical_revision"]
        assert {key: authority[key] for key in (
            "project_id", "timeline_id", "parent_revision_id", "publication_id", "parent_content_digest"
        )} == {
            "project_id": selector["project_id"], "timeline_id": selector["timeline_id"],
            "parent_revision_id": selector["revision_id"], "publication_id": selector["publication_id"],
            "parent_content_digest": selector["content_digest"],
        }
        assert case.service.store.conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'"
        ).fetchone()[0] == 1
    finally:
        case.service.close()


def test_actual_native_render_refuses_stale_revision_selector_without_writes(native_render_case):
    """A real Agent commit cannot hand a stale publication identity to render."""
    case = native_render_case
    accepted = _move(case, "music-bed", 1, "native-recovery-A")
    from astrid.core.dev.journey import build_app_render_admission

    capability = next(
        item for item in case.service.list_capabilities()["items"]
        if item["capability_id"] == "rendering.render"
    )
    built = build_app_render_admission(
        project=case.film.project_id, timeline_id=case.film.timeline_id,
        output_name="native-recovery.mp4", capability=capability, token="test-token",
    )
    request = copy.deepcopy(built["body"])
    request["idempotency_key"] = "native-recovery-stale-selector"
    parent = accepted["data"]["canonical_document"]["parent_revision"]
    request["spec"]["params"]["canonical_revision"] = {
        "project_id": case.film.project_id,
        "timeline_id": case.film.timeline_id,
        "revision_id": accepted["data"]["accepted_revision_id"],
        "publication_id": "stale-publication",
        "content_digest": parent["content_digest"],
    }
    before = _store_state(case.service)
    with pytest.raises(ConflictError, match="render revision does not match"):
        case.service.create_task(request)
    assert _store_state(case.service) == before
    assert case.service.store.conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'"
    ).fetchone()[0] == 0
