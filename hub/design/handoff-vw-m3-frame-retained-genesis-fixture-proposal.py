"""UNAPPLIED Runtime-owner review code. Do not invoke before explicit approval.

This initializes only a NEW caller-owned inactive test realm. It does not make
the retained source the head, forge an edit record, or certify any capture.
"""
from __future__ import annotations

import base64
from pathlib import Path


def prepare_inactive_realm(root: Path, build_fixture):
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_store import TimelineCommitStore
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    if root.exists():
        raise ValueError("retained fixture requires a new ephemeral realm path")
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        project = service.create_project({"slug": "image-cap", "name": "Image cap fixture"},
                                         idempotency_key="image-cap-project")["id"]
        timeline = "image-cap"
        # Normal create_timeline owns the genuine empty genesis and receipt.
        service.create_timeline(project, timeline, name="Image cap fixture", idempotency_key="image-cap-timeline")
        fixture = build_fixture(project, timeline)
        for media in fixture["media"]:
            service.ingest(project, base64.b64decode(media["bytes_base64"]),
                media_type=media["media_type"], original_name=media["original_name"],
                expected_digest=media["digest"], idempotency_key="image-cap-png")
        commits = TimelineCommitStore(service.store,
            validate_prepared=lambda value: validate_commit_value(value, "PreparedCommit"))
        before = commits.head(project, timeline)
        document = fixture["canonical_document"]
        # PRIVATE, TEST-ONLY approval boundary. No direct SQL or head/history writes.
        # _persist_closure also creates the shot projection and shot head.
        with service.store._mutex, service.store._transaction():
            validate_commit_value(document, "CanonicalDocument")
            commits._validate_closure(document)
            commits._persist_closure(document)
            assert commits.revision_closure(project, timeline, document["parent_revision"]["revision_id"]) == document
            assert commits.head(project, timeline) == before
        return {"realm_id": service.realm["id"], "fixture": fixture, "head": before}
    finally:
        service.close()


def test_owner_retained_genesis_restore(tmp_path):
    """UNEXECUTED native service witness for the Runtime owner after approval.

    Authorization here uses Runtime's native test seam, not an HTTP credential.
    The viewing worker's pure check runner never imports this module.
    """
    import importlib.util
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_store import TimelineCommitStore
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    path = Path(__file__).with_name("handoff-vw-m3-frame-retained-genesis-fixture-fixture.py")
    spec = importlib.util.spec_from_file_location("retained_fixture", path)
    fixture_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture_module)
    root = tmp_path / "realm"
    prepared = prepare_inactive_realm(root, fixture_module.build_fixture)
    document = prepared["fixture"]["canonical_document"]
    service = RuntimeService(root)
    try:
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        request = fixture_module.restore_request(document, prepared["head"])
        project, timeline = document["project_id"], document["timeline_id"]
        def restore():
            return service.commit_timeline(project, timeline, request,
                idempotency_key="image-cap-restore", publisher="fixture-owner-test",
                invocation_path=f"/v1/projects/{project}/timelines/{timeline}/commit",
                authorize=service._assert_mutation_admitted)
        result = restore()
        assert result["data"]["canonical_document"] == document
        assert result["receipt"]["command_kind"] == "timeline.commit"
        assert restore() == result
        commits = TimelineCommitStore(service.store,
            validate_prepared=lambda value: validate_commit_value(value, "PreparedCommit"))
        assert commits.head(project, timeline) == {
            "revision_id": result["data"]["accepted_revision_id"],
            "publication_id": result["receipt"]["receipt_id"]}
        assert commits.revision_closure(project, timeline, document["parent_revision"]["revision_id"]) == document
        assert service.store.integrity_report()["ok"]
    finally:
        service.close()


if __name__ == "__main__":
    raise SystemExit("UNAPPLIED: Runtime-owner approval required; no realm created")
