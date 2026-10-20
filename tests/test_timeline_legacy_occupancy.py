"""Legacy publication proves mutable destinations before writing any closure rows."""
from __future__ import annotations

import copy
import json

import pytest

from astrid_runtime_client import ApiError, WorkspaceClient
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.errors import ConflictError
from runtime_protocol.timeline_commit_store import TimelineCommitStore, digest
from test_shot_composition_runtime import _publication, _service, _validation_no_writes
from test_timeline_commit_acceptance import realm, validate_prepared  # noqa: F401 (API-built accepted history)
from test_timeline_projection_occupancy import (
    accept, image, media_item, new_timeline, proposal, with_media,
)


REFUSAL = {"code": "conflict", "message": "destination_occupied",
           "details": {"status": "refused", "reason": "destination_occupied"}}


def publish(service, project, body, key):
    return service.publish_parent_composition(project, "main", body, idempotency_key=key)


def collision(service, commits, project, *, foreign=False, archived=False):
    owner = service.create_project({"slug": "private", "name": "Private film"})["id"] if foreign else project
    new_timeline(service, commits, owner, "owner")
    item = media_item(service, owner, "keep-owner-item")
    shot, internal = image("shot-1", "owned-shot", items=[item], archived=archived)
    shot["payload"]["name"] = "KEEP OWNER NAME"
    shot["content_digest"] = digest(shot["payload"])
    accept(commits, with_media(proposal(service, commits, owner, "owner", "owned-parent",
                                      shots=[(shot, internal)]), item))
    service.create_timeline(project, "target", idempotency_key="target")
    body = _publication(project)
    body["timeline_id"] = "target"
    body["internal_timeline_revisions"][0]["timeline_id"] = "target"
    return body


@pytest.mark.parametrize("foreign", [False, True])
@pytest.mark.parametrize("archived", [False, True])
def test_legacy_publication_refuses_unrelated_destination_before_any_write(realm, foreign, archived):
    service, commits, project, _, _ = realm
    body = collision(service, commits, project, foreign=foreign, archived=archived)
    # A free child placed first must not be persisted before discovering the collision.
    free = copy.deepcopy(body["shot_revisions"][0])
    free.update(shot_id="free", revision_id="free-revision")
    occurrence = copy.deepcopy(body["parent_composition"]["occurrences"][0])
    occurrence.update(occurrence_id="free-occurrence", shot_id="free", shot_revision_id="free-revision")
    body["shot_revisions"].insert(0, free)
    body["parent_composition"]["occurrences"].insert(0, occurrence)
    owner_project = service.store.conn.execute("SELECT project_id FROM timelines WHERE id='owner'").fetchone()[0]
    owner_head = commits.head(owner_project, "owner")
    for _ in range(2):
        with _validation_no_writes(service), pytest.raises(ConflictError) as error:
            service.publish_parent_composition(project, "target", body, idempotency_key="intruder")
        assert error.value.status == 409
        assert error.value.as_dict() == REFUSAL  # no owner/project/revision disclosure
    conn = service.store.conn
    assert conn.execute("SELECT name FROM project_shots WHERE id='shot-1'").fetchone()[0] == "KEEP OWNER NAME"
    assert conn.execute("SELECT COUNT(*) FROM shot_items WHERE id='keep-owner-item'").fetchone()[0] == 1
    assert conn.execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id='shot-1'").fetchone()[0] == "owned-shot"
    assert commits.head(owner_project, "owner") == owner_head


def test_exact_f1_over_http(tmp_path):
    # Socket coverage is run only by the central test service.
    service, project = _service(tmp_path)
    root = service.store.root
    commits = TimelineCommitStore(service.store, validate_prepared=validate_prepared)
    body = collision(service, commits, project)
    service.close()
    daemon = RuntimeDaemon(root, support_root=tmp_path / "support").start()
    try:
        client = WorkspaceClient(daemon.endpoint, daemon.token)
        with _validation_no_writes(daemon.service), pytest.raises(ApiError) as error:
            client._request("POST", f"/v1/projects/{project}/timelines/target/composition-revisions",
                            body=json.dumps(body).encode(),
                            headers={"Content-Type": "application/json", "Idempotency-Key": "intruder"})
        assert error.value.status == 409
        assert (error.value.code, error.value.message, error.value.details) == (
            REFUSAL["code"], REFUSAL["message"], REFUSAL["details"])
    finally:
        daemon.stop()


@pytest.mark.parametrize("existing", [False, True])
def test_legacy_occupied_destination_without_shot_head_is_not_adopted(tmp_path, existing):
    service, project = _service(tmp_path)
    try:
        body = _publication(project)
        publish(service, project, body, "initial")
        service.store.conn.execute("DELETE FROM shot_revision_heads WHERE shot_id='shot-1'")
        body = _publication(project, expected_head="parent-1", parent_revision_id="second",
                            shot_revision_id="shot-rev-1" if existing else "new-shot")
        with _validation_no_writes(service), pytest.raises(ConflictError) as error:
            publish(service, project, body, "second")
        assert error.value.as_dict() == REFUSAL
    finally:
        service.close()


def test_legacy_current_closure_update_and_exact_retry_precede_live_checks(tmp_path):
    service, project = _service(tmp_path)
    try:
        initial = _publication(project)
        publish(service, project, initial, "initial")
        updated = _publication(project, expected_head="parent-1", parent_revision_id="second",
                               shot_revision_id="new-shot")
        updated["shot_revisions"][0]["payload"]["name"] = "Updated own shot"
        accepted = publish(service, project, updated, "second")
        assert accepted["data"]["old_head"] == "parent-1"
        assert service.get_project_shot_revision(project, "shot-1", "new-shot")["payload"]["name"] == "Updated own shot"
        assert service.store.conn.execute("SELECT name FROM project_shots WHERE id='shot-1'").fetchone()[0] == "Updated own shot"
        assert service.store.conn.execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id='shot-1'").fetchone()[0] == "new-shot"
        newer = _publication(project, expected_head="second", parent_revision_id="third", shot_revision_id="newest-shot")
        publish(service, project, newer, "third")
        # Current state no longer passes CAS or projection verification; exact receipts still replay.
        service.store.conn.execute("UPDATE project_shots SET name='changed after receipt' WHERE id='shot-1'")
        with _validation_no_writes(service):
            assert publish(service, project, updated, "second") == accepted
        with _validation_no_writes(service), pytest.raises(ConflictError) as error:
            publish(service, project, updated, "different-key")
        assert error.value.details["reason"] == "stale_head"
    finally:
        service.close()


@pytest.mark.parametrize("tamper", ["receipt", "occurrence", "digest", "projection", "removed"])
def test_legacy_current_destination_requires_verified_current_closure(tmp_path, tamper):
    service, project = _service(tmp_path)
    try:
        publish(service, project, _publication(project), "initial")
        expected = "parent-1"
        conn = service.store.conn
        if tamper == "receipt":
            conn.execute("DELETE FROM command_idempotency WHERE command_kind='parent_composition.publish'")
        elif tamper == "occurrence":
            conn.execute("DELETE FROM composition_revision_occurrences WHERE parent_revision_id='parent-1'")
        elif tamper == "digest":
            conn.execute("UPDATE parent_composition_revisions SET content_digest=? WHERE id='parent-1'", ("sha256:" + "0" * 64,))
        elif tamper == "projection":
            conn.execute("UPDATE project_shots SET name='unaccounted' WHERE id='shot-1'")
        else:
            empty = _publication(project, expected_head=expected, parent_revision_id="removed")
            empty["parent_composition"]["occurrences"] = []
            empty["shot_revisions"] = empty["internal_timeline_revisions"] = []
            publish(service, project, empty, "removed")
            expected = "removed"
        body = _publication(project, expected_head=expected, parent_revision_id="second", shot_revision_id="new-shot")
        with _validation_no_writes(service), pytest.raises(ConflictError) as error:
            publish(service, project, body, "second")
        assert error.value.as_dict() == REFUSAL
    finally:
        service.close()


@pytest.mark.parametrize("inline", [False, True])
def test_legacy_historical_reuse_keeps_newer_global_shot_head(tmp_path, inline):
    service, project = _service(tmp_path)
    try:
        initial = publish(service, project, _publication(project), "initial")
        commits = TimelineCommitStore(service.store, validate_prepared=validate_prepared)
        new_timeline(service, commits, project, "other")
        closure = commits.revision_closure(project, "main", "parent-1")
        source = (closure["shot_revisions"][0], closure["internal_timeline_revisions"][0])
        accept(commits, proposal(service, commits, project, "other", "linked", shots=[source]))
        accept(commits, proposal(service, commits, project, "other", "newer",
                                 shots=[image("shot-1", "newer-global-shot")]))
        replacement = _publication(project, expected_head="parent-1", parent_revision_id="replacement", shot_revision_id="replacement-shot")
        with _validation_no_writes(service), pytest.raises(ConflictError) as error:
            publish(service, project, replacement, "replacement")
        assert error.value.as_dict() == REFUSAL
        before = tuple(tuple(row) for row in service.store.conn.execute("SELECT * FROM project_shots"))
        reused = _publication(project, expected_head="parent-1", parent_revision_id="historical")
        if not inline:
            reused.pop("shot_revisions")
            reused.pop("internal_timeline_revisions")
        result = publish(service, project, reused, "historical")
        assert result["data"]["dependency_manifest"] == initial["data"]["dependency_manifest"]
        assert commits.revision_closure(project, "main", "historical")["shot_revisions"] == closure["shot_revisions"]
        assert service.store.conn.execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id='shot-1'").fetchone()[0] == "newer-global-shot"
        assert tuple(tuple(row) for row in service.store.conn.execute("SELECT * FROM project_shots")) == before
    finally:
        service.close()
