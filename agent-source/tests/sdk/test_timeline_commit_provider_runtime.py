"""Real Runtime custody of provider reservations; run in the integration lane."""
from __future__ import annotations

import copy

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


def test_structural_reservations_and_receipt_retry_survive_runtime_restart(tmp_path, monkeypatch):
    use_runtime()
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.timeline import commands, commit

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    project = service.create_project({"slug": "reservations", "name": "Reservations"})["id"]
    service.create_timeline(project, "film", idempotency_key="create-film")

    def head():
        resource = service.get_project_timeline(project, "film")
        return {"revision_id": resource["head_revision_id"],
                "publication_id": resource["head_publication_id"]}

    def request(calls, *, dry_run=False):
        current = head()
        return {"api_version": 1, "project_id": project, "timeline_id": "film",
                "base_revision_id": current["revision_id"],
                "base_publication_id": current["publication_id"], "commands": calls,
                "dry_run": dry_run}

    def submit(body, key):
        return service.commit_timeline(
            project, "film", body, idempotency_key=key, publisher="author",
            invocation_path=route_path(project, "film"), authorize=lambda: None,
        )

    def inverse(publication):
        return {"schema_version": 1, "op": "timeline.inverse", "version": "1",
                "select": None, "args": {"publications": [publication]}}

    create = {"schema_version": 1, "op": "track.create", "version": "1", "select": "parent",
              "args": {"row": {"id": "stable-track", "kind": "visual", "opaque": [None, False]}}}
    try:
        initial = head()
        preview = submit(request([create], dry_run=True), "preview")
        assert preview["receipt"] is None and head() == initial
        original_request = request([create])
        created = submit(original_request, "original-create")
        occupied = head()
        with pytest.raises(RuntimeErrorBase) as error:
            submit(request([create]), "occupied-create")
        assert error.value.code == "conflict" and error.value.status == 409
        assert error.value.details["reason"] == "identity_collision" and head() == occupied
        deleted = submit(request([inverse(created["receipt"]["receipt_id"])]), "undo-create")
        assert deleted["data"]["canonical_document"]["parent_revision"]["payload"][
            "config"]["tracks"] == []
        retired = head()
        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(commit.create_runtime_commit_service())
        assert head() == retired

        def forbidden(*args, **kwargs):
            raise AssertionError("receipt retry executed provider semantics or reservation checks")

        with monkeypatch.context() as retry:
            retry.setattr(commands, "execute", forbidden)
            retry.setattr(commit, "_check_reservations", forbidden)
            assert submit(original_request, "original-create") == created
        assert head() == retired
        with pytest.raises(RuntimeErrorBase) as error:
            submit(request([copy.deepcopy(create)]), "new-create-after-restart")
        assert error.value.code == "conflict" and error.value.status == 409
        assert error.value.details["reason"] == "identity_collision" and head() == retired
        restored = submit(request([inverse(deleted["receipt"]["receipt_id"])]), "redo-create")
        assert restored["data"]["canonical_document"] == created["data"]["canonical_document"]
        history = service.list_timeline_commits(project, "film", authorize=lambda: None)
        assert len(history["items"]) == 4  # Bootstrap, create, inverse-delete, inverse-restore.
    finally:
        service.close()


def test_restore_inverse_redo_and_exact_retry_survive_runtime_restart(tmp_path, monkeypatch):
    use_runtime()
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.timeline import commands, commit

    root = tmp_path / "restore-realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    project = service.create_project({"slug": "restore", "name": "Restore"})["id"]
    service.create_timeline(project, "film", idempotency_key="create-film")

    def head():
        resource = service.get_project_timeline(project, "film")
        return {"revision_id": resource["head_revision_id"],
                "publication_id": resource["head_publication_id"]}

    def request(calls, *, dry_run=False):
        current = head()
        return {"api_version": 1, "project_id": project, "timeline_id": "film",
                "base_revision_id": current["revision_id"],
                "base_publication_id": current["publication_id"], "commands": calls,
                "dry_run": dry_run}

    def submit(body, key):
        return service.commit_timeline(
            project, "film", body, idempotency_key=key, publisher="author",
            invocation_path=route_path(project, "film"), authorize=lambda: None,
        )

    def inverse(publication):
        return {"schema_version": 1, "op": "timeline.inverse", "version": "1",
                "select": None, "args": {"publications": [publication]}}

    try:
        initial = head()
        create = {"schema_version": 1, "op": "track.create", "version": "1", "select": "parent",
                  "args": {"row": {"id": "historical-track", "kind": "visual",
                                    "unknown": {"literal": "historical-track", "value": None}}}}
        created = submit(request([create]), "create-track")
        historical = created["data"]["canonical_document"]
        populated = head()
        original_body = {"expected_head": populated["revision_id"],
                         "expected_publication_id": populated["publication_id"]}
        path = route_path(project, "film", "composition-revisions/" + initial["revision_id"] + "/restore")
        restored = service.restore_project_parent_composition_revision(
            project, "film", initial["revision_id"], original_body,
            idempotency_key="restore-original", publisher="author", invocation_path=path,
            authorize=lambda: None,
        )
        empty = restored["data"]["canonical_document"]
        assert restored["data"]["accepted_revision_id"] == initial["revision_id"]
        assert restored["data"]["status"] == "accepted" and restored["data"]["rebased_onto"] is None
        assert empty["parent_revision"]["payload"]["config"]["tracks"] == []
        history = service.list_timeline_commits(project, "film", authorize=lambda: None)
        record = history["items"][-1]["records"]
        assert record["restored_from"] == {key: empty["parent_revision"][key]
                                            for key in ("revision_id", "content_digest")}
        assert record["commands"][0]["writes"][0]["ref"] == "timeline"
        assert record["commands"][0]["created"] == []
        assert restored["receipt"]["command_kind"] == "timeline.commit"
        assert restored["receipt"]["result"] == restored["data"]
        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(commit.create_runtime_commit_service())
        retired = head()

        def forbidden(*args, **kwargs):
            raise AssertionError("exact restore retry executed provider semantics")

        with monkeypatch.context() as retry:
            retry.setattr(commands, "execute", forbidden)
            assert service.restore_project_parent_composition_revision(
                project, "film", initial["revision_id"], original_body,
                idempotency_key="restore-original", publisher="author", invocation_path=path,
                authorize=lambda: None,
            ) == restored
        assert head() == retired
        with pytest.raises(RuntimeErrorBase) as error:
            submit(request([create]), "retired-id")
        assert error.value.details["reason"] == "identity_collision" and head() == retired
        undone = submit(request([inverse(restored["receipt"]["receipt_id"])]), "undo-restore")
        assert undone["data"]["canonical_document"] == historical
        redone = submit(request([inverse(undone["receipt"]["receipt_id"])]), "redo-restore")
        assert redone["data"]["canonical_document"] == empty
        stale_body = {"expected_head": initial["revision_id"],
                      "expected_publication_id": initial["publication_id"]}
        with pytest.raises(RuntimeErrorBase) as error:
            service.restore_project_parent_composition_revision(
                project, "film", initial["revision_id"], stale_body,
                idempotency_key="stale-publication", publisher="author", invocation_path=path,
                authorize=lambda: None,
            )
        assert error.value.details["reason"] == "stale_head"
        current = head()
        call = {"schema_version": 1, "op": "timeline.restore", "version": "1", "select": None,
                "args": {key: historical["parent_revision"][key]
                         for key in ("revision_id", "content_digest")}}
        preview = submit(request([call], dry_run=True), "restore-preview")
        assert preview["receipt"] is None and head() == current
        assert preview["data"]["canonical_document"] == historical
        reused = submit(request([call]), "restore-historical-ids")
        assert reused["data"]["canonical_document"] == historical
    finally:
        service.close()
