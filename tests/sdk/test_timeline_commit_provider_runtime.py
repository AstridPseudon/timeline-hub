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
