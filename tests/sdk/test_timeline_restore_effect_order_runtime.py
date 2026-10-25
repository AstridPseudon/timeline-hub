"""Real Runtime proof for ordinary restore inverse effect order."""
from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


def test_id5_public_undo_of_restore_preserves_authenticated_effect_order(tmp_path):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    from astrid.sdk import timeline
    from astrid.sdk.contracts import DomainResult
    from astrid.sdk.remote import RemoteTimelines
    from astrid.sdk.timeline._command_state import ABSENT, present
    from astrid.sdk.timeline._doc_patch import inverse_changes
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.workspace_client import WorkspaceClient
    from tests.editing_conformance.test_doc_patch_v2 import change, patch

    root = tmp_path / "restore-effect-order"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    project = service.create_project({"slug": "restore-order", "name": "Restore order"})["id"]
    service.create_timeline(project, "film", idempotency_key="create-film")

    generated = SimpleNamespace()
    transport = WorkspaceClient.__new__(WorkspaceClient)
    transport._generated = generated
    transport._last_handshake = {"realm_id": service.realm["id"], "actor_id": "restore-order-test"}
    client = SimpleNamespace(_remote=SimpleNamespace(_transport=transport),
                             timelines=RemoteTimelines(transport))
    client.timelines._resolve_timeline = lambda p, t: DomainResult.success({
        "project_id": p, "timeline_id": t})
    client.timelines.open_composition = lambda p, t: DomainResult.success({
        "native_inspection": {"project_id": p, "timeline_id": t},
        "summary": {"head_revision_id": service.get_project_timeline(p, t)["head_revision_id"]}})
    client.timelines.open_bundle = lambda p, t, revision_id=None, **kw: DomainResult.success({
        "bundle": bundle_from_document(service._timeline_commits()[0].revision_closure(p, t, revision_id))})
    wires = []

    def send(p, t, body, *, idempotency_key):
        result = service.commit_timeline(
            p, t, body, idempotency_key=idempotency_key, publisher="restore-order-test",
            invocation_path=f"/v1/projects/{p}/timelines/{t}/commit", authorize=lambda: None)
        wires.append({"body": copy.deepcopy(body), "key": idempotency_key,
                      "response": copy.deepcopy(result)})
        return result

    generated.commit_timeline = send
    outbox = tmp_path / "restore-effect-order-outbox.json"

    def opened():
        return timeline.open(project, "film", client=client, outbox_path=outbox)

    try:
        initial = opened()
        initial.command(capture_track_create(
            initial.bundle, "parent", {"id": "opaque-track", "kind": "visual",
                                         "seed": {"opaque": [None, False]}}),
            label="Create opaque track")
        created = initial.commit("Create opaque track", idempotency_key="create-track")
        target_document = copy.deepcopy(created["data"]["canonical_document"])
        target_parent = created["data"]["canonical_document"]["parent_revision"]

        changed = opened()
        track = next(row for row in changed.bundle["parent"]["config"]["tracks"]
                     if row["id"] == "opaque-track")
        seed = copy.deepcopy(track["seed"])
        changed.command(patch(
            change(["config", "tracks", "id:opaque-track", "seed"], present(seed),
                   {"opaque": [None, False, "changed-seed"]}),
            change(["config", "tracks", "id:opaque-track", "opaque"], ABSENT,
                   {"literal": "new-opaque-sibling"})),
            label="Change opaque siblings")
        changed_result = changed.commit("Change opaque siblings", idempotency_key="change-siblings")
        changed_document = copy.deepcopy(changed_result["data"]["canonical_document"])
        changed_head = {
            "revision_id": changed_result["data"]["accepted_revision_id"],
            "publication_id": changed_result["receipt"]["receipt_id"],
        }

        restored = opened().restore(
            target_parent["revision_id"], target_parent["content_digest"],
            idempotency_key="restore-a")
        assert restored["data"]["status"] == "accepted"
        assert restored["data"]["canonical_document"] == target_document
        restore_publication = restored["receipt"]["receipt_id"]
        restore_wire = next(wire for wire in wires if wire["key"] == "restore-a")
        assert ((restore_wire["body"]["base_revision_id"],
                 restore_wire["body"]["base_publication_id"])
                == (changed_head["revision_id"], changed_head["publication_id"]))
        assert restore_wire["body"]["commands"] == [{
            "schema_version": 1, "op": "timeline.restore", "version": "1", "select": None,
            "args": {"revision_id": target_parent["revision_id"],
                     "content_digest": target_parent["content_digest"]},
        }]

        before_undo = service.list_timeline_commits(project, "film", authorize=lambda: None)["items"]
        source_entry = copy.deepcopy(before_undo[-1])
        assert source_entry["records"]["commands"][0]["command"]["op"] == "timeline.restore"
        source_step = source_entry["records"]["steps"][0]
        source_patch = source_step["patch"]
        sibling_paths = [
            (change["ref"], tuple(change["path"][:-1]))
            for change in source_patch
            if change["path"]
        ]
        assert len(sibling_paths) >= 2
        assert len(set(sibling_paths)) == 1
        assert len({tuple(change["path"]) for change in source_patch if change["path"]}) >= 2

        restore_head = service.get_project_timeline(project, "film")
        preview = opened().undo([restore_publication], dry_run=True, idempotency_key="preview-undo-restore")
        assert preview["receipt"] is None
        assert preview["data"]["would_status"] == "accepted"
        assert service.get_project_timeline(project, "film") == restore_head
        assert service.list_timeline_commits(project, "film", authorize=lambda: None)["items"] == before_undo

        undone = opened().undo([restore_publication], idempotency_key="undo-restore")
        history = service.list_timeline_commits(project, "film", authorize=lambda: None)["items"]
        inverse_entry = history[-1]
        inverse_step = inverse_entry["records"]["steps"][0]

        assert undone["data"]["canonical_document"] == changed_document
        assert inverse_step["patch"] == inverse_changes(source_patch)
        assert [tuple(change["path"]) for change in inverse_step["patch"]] == [
            tuple(change["path"]) for change in reversed(source_patch)]
        assert history[-2] == source_entry
        assert len(history) == len(before_undo) + 1
        assert inverse_entry["records"]["undo_of"] == [restore_publication]
        assert (service.get_project_timeline(project, "film")["head_revision_id"],
                service.get_project_timeline(project, "film")["head_publication_id"]) == (
                    undone["data"]["accepted_revision_id"], undone["receipt"]["receipt_id"])

        undo_wire = next(wire for wire in wires if wire["key"] == "undo-restore")
        retry = generated.commit_timeline(
            project, "film", copy.deepcopy(undo_wire["body"]), idempotency_key="undo-restore")
        assert retry == undo_wire["response"] == undone
        assert service.list_timeline_commits(project, "film", authorize=lambda: None)["items"] == history
    finally:
        service.close()
