"""Real migration through Runtime; trusted legacy bootstrap is test setup only."""
from __future__ import annotations

import base64
import copy

import pytest

from tests.helpers.runtime import runtime_checkout, use_runtime

RUNTIME_COMMIT = "c3d26567ff6fe4e20a959476d40aff90ad23a0ca"
TRUSTED_BOOTSTRAP_HELPER = "54db299d6ebb9ec98649895760a4cd37cee6c147"

pytestmark = pytest.mark.integration


def test_public_seed_refuses_exact_rational_fps_legacy_input_atomically(tmp_path):
    use_runtime(commit=RUNTIME_COMMIT)
    from runtime_protocol.errors import NotFoundError, ValidationError
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore

    from tests.editing_conformance.test_recipe_m2_group_migration import legacy_document

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "migration", "name": "Migration"})["id"]
        service.create_timeline(project, "film", idempotency_key="timeline")
        media = service.ingest(
            project, b"migration-image", media_type="image/png", original_name="image.png",
            idempotency_key="image",
        )["data"]["object_id"]
        document = legacy_document(project_id=project, media_id=media)
        parent = document["parent_revision"]
        before = service.get_project_timeline(project, "film")
        publication = {
            "project_id": project,
            "timeline_id": "film",
            "expected_head": None,
            "parent_revision_id": parent["revision_id"],
            "parent_composition": parent["payload"],
            "shot_revisions": [],
            "internal_timeline_revisions": [],
            "dependency_manifest": document["dependency_manifest"],
        }
        # Neutral legacy publication has no DocumentPin field. Removing it
        # for the second probe exposes the independent rational-fps refusal.
        with pytest.raises(
            ValidationError, match="dependency_manifest contains unsupported fields"
        ) as error:
            service.publish_parent_composition(
                project, "film", publication, idempotency_key="legacy-pins"
            )
        assert error.value.details == {"field": "documents"}
        del publication["dependency_manifest"]["documents"]
        with pytest.raises(ValidationError, match="visual timing fps must be finite and positive"):
            service.publish_parent_composition(
                project, "film", publication, idempotency_key="legacy-seed"
            )
        assert service.get_project_timeline(project, "film") == before
        with pytest.raises(NotFoundError):
            service.get_project_parent_composition_revision(project, "film", parent["revision_id"])
    finally:
        service.close()


@pytest.fixture(params=[False, True], ids=["golden-parent", "opaque-parent"])
def legacy_runtime(tmp_path, monkeypatch, request):
    use_runtime(commit=RUNTIME_COMMIT)
    # Runtime owns this helper: it uses normal storage acceptance and retained
    # inputs, without claiming an Agent migration or repairing the old writer.
    helper = runtime_checkout(TRUSTED_BOOTSTRAP_HELPER)
    monkeypatch.syspath_prepend(str(helper / "tests"))
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from timeline_trusted_bootstrap import seed_trusted_legacy_parent

    from astrid.sdk.media_transcript import transcript_document_id
    from astrid.sdk.timeline.commit import _digest, create_runtime_commit_service
    from tests.editing_conformance.test_recipe_m2_group_migration import legacy_document

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        service.register_timeline_commit_provider(create_runtime_commit_service())
        project = service.create_project({"slug": "migration", "name": "Migration"})["id"]
        service.create_timeline(project, "film", idempotency_key="timeline")
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j1ioAAAAASUVORK5CYII="
        )
        media = service.ingest(
            project, png, media_type="image/png", original_name="source.png", idempotency_key="image"
        )["data"]["object_id"]
        content = {
            "schema": "media.transcript/v1",
            "media_id": media,
            "source_id": "whisper",
            "segments": [
                {
                    "id": "line-1",
                    "start": 4,
                    "end": 5,
                    "text": "original",
                    "words": [{"id": "word-1", "start": 4, "end": 5, "text": "original"}],
                }
            ],
        }
        source = service.create_document(
            project,
            {
                "document_id": transcript_document_id(project, media, "whisper"),
                "kind": "media.transcript",
                "content": content,
            },
            idempotency_key="transcript",
        )["data"]
        pin = {
            "document_id": source["document_id"],
            "version": source["version"],
            "content_digest": _digest(content),
        }
        document = legacy_document(
            opaque_variant=request.param, project_id=project, media_id=media, transcript_pin=pin
        )
        original = copy.deepcopy(document)

        def unavailable(*args, **kwargs):
            raise AssertionError("legacy setup or migration evaluated a scene")

        monkeypatch.setattr("runtime_protocol.service.evaluate_closure", unavailable)
        monkeypatch.setattr("runtime_protocol.visual_seam.evaluate_closure", unavailable)
        setup = seed_trusted_legacy_parent(service, document, idempotency_key="legacy-setup")
        assert document == original
        assert setup["data"]["canonical_document"] == original
        yield service, root, document, source
    finally:
        service.close()


def assert_retained_readback(service, document, source):
    from runtime_protocol.timeline_commit_inputs import (
        capture_document_input,
        reachable_document_input_pins,
    )

    from astrid.sdk.timeline.commit import _digest

    project, timeline = document["project_id"], document["timeline_id"]
    parent = document["parent_revision"]
    head = service.get_project_timeline(project, timeline)
    assert head["head_revision_id"] == parent["revision_id"]
    revision = service.get_project_parent_composition_revision(project, timeline, parent["revision_id"])
    assert revision["payload"] == parent["payload"]
    assert revision["content_digest"] == parent["content_digest"] == _digest(parent["payload"])
    assert revision["dependency_manifest"] == document["dependency_manifest"]
    commits, _ = service._timeline_commits()
    assert commits.revision_closure(project, timeline, parent["revision_id"]) == document
    pin = document["dependency_manifest"]["documents"][0]
    assert pin == {
        "document_id": source["document_id"],
        "version": 1,
        "content_digest": _digest(source["content"]),
    }
    reachable = reachable_document_input_pins(
        service.store.conn, project, timeline, revision_ids=[parent["revision_id"]]
    )
    assert reachable == [pin]
    captured = capture_document_input(
        service.store.conn,
        project,
        pin,
        reachable_pins=reachable,
        expected_kind="media.transcript",
        expected_schema="media.transcript/v1",
    )
    assert captured.document == source
    inspected = service.inspect_timeline(project, timeline, {"detail": True})
    assert inspected["revision_id"] == parent["revision_id"]
    assert inspected["parent_content_digest"] == parent["content_digest"]
    assert inspected["render_requested"] is False
    assert inspected["render_timing_context"]["fps"] == {"numerator": 30000, "denominator": 1001}
    return inspected


def replace_source(service, source):
    updated = service.update_document(
        source["project_id"],
        source["document_id"],
        {"expected_version": 1, "content": {**source["content"], "segments": []}},
        idempotency_key="source-v2",
    )["data"]
    assert updated["version"] == 2 and updated["content"]["segments"] == []


def test_exact_legacy_setup_get_inspect_and_v1_source_survive_v2_and_reopen(legacy_runtime):
    from runtime_protocol.service import RuntimeService

    service, root, document, source = legacy_runtime
    inspected = assert_retained_readback(service, document, source)
    assert [(row["clip_id"], row["start"], row["duration"]) for row in inspected["selected_parent_clips"]] == [
        ("before", [10, 1], [1, 1]),
        ("c1", [0, 1], [2, 1]),
        ("c2", [2, 1], [2, 1]),
        ("after", [12, 1], [1, 1]),
    ]
    replace_source(service, source)
    service.close()
    reopened = RuntimeService(root)
    try:
        assert reopened.get_document(source["project_id"], source["document_id"])["version"] == 2
        assert assert_retained_readback(reopened, document, source) == inspected
        assert reopened.store.integrity_report()["ok"]
    finally:
        reopened.close()


def test_real_migration_accepted_reload_inverse_exact_legacy_redo_same_ids(legacy_runtime):
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.timeline.commit import (
        bundle_from_document,
        create_runtime_commit_service,
        document_from_bundle,
    )
    from astrid.sdk.timeline.new_group_commands import capture_migrate_groups
    from tests.editing_conformance.test_recipe_m2_group_migration import GROUPS
    from tests.sdk.test_timeline_commit_provider import inverse

    service, root, original, source = legacy_runtime
    project, timeline = original["project_id"], original["timeline_id"]
    assert_retained_readback(service, original, source)

    def submit(runtime, command, key):
        head = runtime.get_project_timeline(project, timeline)
        body = {
            "api_version": 1,
            "project_id": project,
            "timeline_id": timeline,
            "base_revision_id": head["head_revision_id"],
            "base_publication_id": head["head_publication_id"],
            "commands": [command],
        }
        return runtime.commit_timeline(
            project,
            timeline,
            body,
            idempotency_key=key,
            publisher="author",
            invocation_path=route_path(project, timeline),
            authorize=lambda: None,
        )

    migrated = submit(service, capture_migrate_groups(original, GROUPS), "migrate")
    canonical = migrated["data"]["canonical_document"]
    assert migrated["data"]["status"] == "accepted"
    assert migrated["receipt"] is not None
    assert document_from_bundle(bundle_from_document(canonical)) == canonical
    assert canonical["dependency_manifest"]["documents"] == original["dependency_manifest"]["documents"]
    assert canonical["dependency_manifest"]["media"] == original["dependency_manifest"]["media"]
    assert [row["shot_id"] for row in canonical["shot_revisions"]] == ["new-shot"]
    assert [
        row["occurrence_id"] for row in canonical["parent_revision"]["payload"]["occurrences"]
    ] == ["new-occ"]
    assert_retained_readback(service, canonical, source)
    replace_source(service, source)
    service.close()
    reopened = RuntimeService(root)
    try:
        reopened.register_timeline_commit_provider(create_runtime_commit_service())
        assert reopened.get_document(project, source["document_id"])["version"] == 2
        assert_retained_readback(reopened, canonical, source)
        undone = submit(reopened, inverse([migrated["receipt"]["receipt_id"]]), "undo")
        assert undone["data"]["canonical_document"] == original
        assert_retained_readback(reopened, original, source)
        redone = submit(reopened, inverse([undone["receipt"]["receipt_id"]]), "redo")
        assert redone["data"]["canonical_document"] == canonical
        assert redone["data"]["commands"][0]["created"] == [
            "shot:new-shot", "occurrence:new-occ"
        ]
        assert_retained_readback(reopened, canonical, source)
        assert reopened.store.integrity_report()["ok"]
    finally:
        reopened.close()


def test_literal_detached_lines_transcript_is_refused(legacy_runtime):
    from runtime_protocol.errors import ValidationError

    from tests.sdk.test_timeline_commit_provider import source_fixture

    service, _, document, _ = legacy_runtime
    literal = source_fixture("transcript")["document"]
    assert "lines" in literal["content"] and "segments" not in literal["content"]
    before = service.get_project_timeline(document["project_id"], "film")
    with pytest.raises(
        ValidationError, match="transcript content must have the canonical media.transcript/v1 fields"
    ):
        service.create_document(
            document["project_id"],
            {"document_id": literal["document_id"], "kind": literal["kind"], "content": literal["content"]},
            idempotency_key="unsupported-lines",
        )
    assert service.get_project_timeline(document["project_id"], "film") == before


def test_official_runtime_schema_admits_compiled_canonical_candidate():
    use_runtime(commit=RUNTIME_COMMIT)
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from astrid.sdk.timeline.commit import document_from_bundle
    from tests.editing_conformance.test_recipe_m2_group_migration import plan_for

    _, plan = plan_for()
    validate_commit_value(document_from_bundle(plan.bundle), "CanonicalDocument")


def test_official_runtime_schema_admits_recorded_migration_command():
    use_runtime(commit=RUNTIME_COMMIT)
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from tests.editing_conformance.test_recipe_m2_group_migration import plan_for

    _, plan = plan_for()
    validate_commit_value(plan.commands[0], "EditCommand")
