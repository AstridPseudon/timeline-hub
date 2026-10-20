"""Legacy publication cannot overwrite tracked history or choose its own target."""
from __future__ import annotations

import pytest

from runtime_protocol.errors import ConflictError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
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


def test_legacy_head_without_canonical_publication_remains_publishable(service):
    _, _, attempt, render_digest = _ready_authoring_attempt(service, legacy_parent=True)
    head = service.store.conn.execute(
        "SELECT revision_id, publication_id FROM parent_composition_heads WHERE timeline_id='main'",
    ).fetchone()
    assert head["revision_id"] == "legacy-parent" and head["publication_id"] is None
    result = service.publish_timeline_render(attempt["attempt_id"], _publication_body(attempt, render_digest),
                                            idempotency_key="publish")
    assert result["timeline_version"] == 2
