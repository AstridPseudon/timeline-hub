"""Direct production coverage for the unfrozen transcript source carrier."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.media_transcript import transcript_document_id
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.native_transcript_association import (
    REFERENCES_SCHEMA,
    TRANSCRIPT_SCHEMA_REF,
    _caption_id,
    _encode_component,
    _project_items,
    capture_transcript_association,
)
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse

PROJECT = "project-1"
MEDIA = "sha256:" + "a" * 64


def _document(source_id="source-1", segment_id="segment-a", *, version=1):
    content = {
        "schema": "media.transcript/v1", "media_id": MEDIA, "source_id": source_id,
        "segments": [{"id": segment_id, "start": 0, "end": 1, "text": "Hello",
                       "words": [{"id": "word-a", "start": 0, "end": 1, "text": "Hello"}]}],
    }
    pin = {"document_id": transcript_document_id(PROJECT, MEDIA, source_id),
           "version": version, "content_digest": _digest(content)}
    return pin, {"document_id": pin["document_id"], "project_id": PROJECT,
                 "kind": "media.transcript", "version": version, "content": content}


def _bundle(*, caption=False):
    pin, source = _document()
    payload = {
        "config": {"clips": [], "tracks": [], "output": {"fps": 30},
                   "bundle": {"schema_version": 1,
                              "transcriptReferences": {"schema": "media.transcript.references/v1", "associations": []},
                              "itemsBySchemaRef": {TRANSCRIPT_SCHEMA_REF: []}}},
        "clips": [], "occurrences": [],
        "registry": {"assets": {"asset-a": {"media_id": MEDIA, "type": "audio"}}},
        "opaque": {"keep": [None, False]},
    }
    if caption:
        payload["config"]["clips"] = [{"id": "caption-a", "track": "transcript-caption-foundry-track",
                                       "asset": "asset-a", "app": {"__generated__": {"provenance": {
                                           "sourceSchemaRef": TRANSCRIPT_SCHEMA_REF,
                                           "sourceItemId": "legacy-segment"}}}}]
    document = {"schema_version": 1, "project_id": PROJECT, "timeline_id": "film",
                "parent_revision": {"revision_id": "revision-1", "payload": payload,
                                    "content_digest": _digest(payload)},
                "shot_revisions": [], "internal_timeline_revisions": [],
                "dependency_manifest": _manifest([], [], [{"media_id": MEDIA, "content_digest": MEDIA}], [])}
    bundle = bundle_from_document(document)
    bundle["source_mapping"]["pinned_documents"] = [{"pin": pin, "document": source}]
    return bundle, pin


def _known_reconciliation_bundle():
    bundle, pin = _bundle()
    canonical = "transcript-source:asset-a:source:source-1:segment:segment-a"
    legacy = "transcript-source:source-1:segment:segment-a"
    source = bundle["source_mapping"]["pinned_documents"][0]["document"]
    source["content"]["segments"][0]["id"] = canonical
    source["content_digest"] = _digest(source["content"])
    pin = copy.deepcopy(pin)
    pin["content_digest"] = source["content_digest"]
    bundle["source_mapping"]["pinned_documents"] = [{"pin": pin, "document": source}]
    incoming = _project_items(source, source["content"], "asset-a")[0]
    old = copy.deepcopy(incoming)
    old["id"] = legacy
    old["payload"]["segmentId"] = legacy
    bundle["parent"]["config"]["bundle"]["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF] = [old]
    media = {"id": "media-a", "asset": "asset-a", "track": "A1", "clipType": "audio"}
    caption = {
        "id": _caption_id(legacy + "@media-a"),
        "track": "transcript-caption-foundry-track",
        "clipType": "text",
        "at": 0.1,
        "hold": 2.3,
        "x": 143,
        "y": 620,
        "text": {"content": "Human correction", "color": "#cc3377", "fontSize": 51},
        "app": {
            "retained": {"future": [None, False]},
            "__generated__": {
                "extensionId": "haus.astrid.transcript-lane",
                "contributionId": "transcript-caption-foundry",
                "provenance": {
                    "contractVersion": 1,
                    "sourceSchemaRef": TRANSCRIPT_SCHEMA_REF,
                    "sourceItemId": legacy,
                    "sourceFingerprint": "keep-source-fingerprint",
                    "generatorVersion": "1.3.0",
                    "outputFingerprint": "keep-output-fingerprint",
                    "conflictPolicy": "preserve-output",
                },
            },
        },
    }
    review_key = "transcript-source-review:" + _encode_component(legacy)
    review = {
        "schemaVersion": 1,
        "sourceSchemaRef": TRANSCRIPT_SCHEMA_REF,
        "sourceItemId": legacy,
        "status": "accepted-for-source-update",
        "proposedText": "Human correction",
        "opaque": {"keep": [None, False]},
    }
    config = bundle["parent"]["config"]
    config["clips"] = [media, caption]
    config["app"] = {
        "unrelated": {"keep": True},
        "haus.astrid.transcript-lane": {
            "preferences": {"color": "blue"},
            review_key: review,
        },
    }
    bundle["parent"]["clips"] = copy.deepcopy(config["clips"])
    payload = bundle["source_mapping"]["_runtime_document"]["parent_revision"]["payload"]
    payload["config"] = copy.deepcopy(config)
    payload["clips"] = copy.deepcopy(config["clips"])
    payload["config"]["bundle"] = copy.deepcopy(bundle["parent"]["config"]["bundle"])
    return bundle, pin, legacy, canonical, review_key


def test_association_records_source_planes_and_roundtrips_canonically():
    bundle, pin = _bundle()
    command = capture_transcript_association(bundle, "asset-a", document=pin)
    before = copy.deepcopy(bundle)
    plan = execute(bundle, [command])

    assert bundle == before
    assert plan.records[0]["dependencies"] == [{"key": "transcript.document", "kind": "transcript",
                                                  "pin": pin, "policy": "exact"}]
    assert plan.records[0]["selections"][0]["key"] == "transcript.source-items"
    payload = document_from_bundle(plan.bundle)["parent_revision"]["payload"]
    bundle = payload["config"]["bundle"]
    assert bundle["transcriptReferences"]["associations"] == [{"assetId": "asset-a", "documentId": pin["document_id"]}]
    assert bundle["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0]["payload"]["words"][0]["id"] == "word-a"
    assert payload["opaque"] == {"keep": [None, False]}
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))
    assert reloaded["parent"]["config"]["bundle"] == bundle


def test_association_uses_guarded_inverse_and_replay():
    bundle, pin = _bundle()
    command = capture_transcript_association(bundle, "asset-a", document=pin)
    plan = execute(bundle, [command])
    undone = inverse(plan.bundle, plan.records)
    assert document_from_bundle(undone.bundle) == document_from_bundle(bundle)
    assert replay(plan, bundle).bundle == plan.bundle
    changed = copy.deepcopy(plan.bundle)
    changed["parent"]["opaque"]["later"] = True
    assert inverse(changed, plan.records).bundle["parent"]["opaque"]["later"] is True


def test_replacement_requires_and_retains_exact_prior_pin():
    bundle, new_pin = _bundle()
    old_pin, _ = _document(source_id="source-old", segment_id="segment-old")
    old_source = _document(source_id="source-old", segment_id="segment-old")[1]
    bundle["source_mapping"]["pinned_documents"] = [{"pin": old_pin, "document": old_source}]
    old_command = capture_transcript_association(bundle, "asset-a", document=old_pin)
    old_plan = execute(bundle, [old_command])
    old_plan.bundle["source_mapping"]["pinned_documents"].append(
        {"pin": new_pin, "document": _document()[1]})
    replacement = capture_transcript_association(
        old_plan.bundle, "asset-a", document=new_pin, previous_document=old_pin)
    plan = execute(old_plan.bundle, [replacement])
    dependencies = plan.records[0]["dependencies"]
    assert {row["pin"]["document_id"] for row in dependencies} == {
        old_pin["document_id"], new_pin["document_id"]}
    assert plan.bundle["parent"]["config"]["bundle"]["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0]["payload"]["documentId"] == new_pin["document_id"]


def test_unqualified_caption_reference_does_not_block_source_association():
    bundle, pin = _bundle(caption=True)
    command = capture_transcript_association(bundle, "asset-a", document=pin)
    plan = execute(bundle, [command])
    assert plan.bundle["parent"]["config"]["bundle"]["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF]


def test_association_reconciles_real_caption_and_review_leaves_without_asset_on_caption():
    bundle, pin, legacy, canonical, review_key = _known_reconciliation_bundle()
    before = copy.deepcopy(bundle)
    command = capture_transcript_association(bundle, "asset-a", document=pin)
    plan = execute(bundle, [command])
    assert bundle == before
    write_paths = {(write["ref"], tuple(write["path"])) for write in plan.records[0]["writes"]}
    assert ("parent", ("config", "bundle", "transcriptReferences")) in write_paths
    assert ("parent", ("config", "bundle", "itemsBySchemaRef")) in write_paths
    assert ("parent", ("config", "app", "haus.astrid.transcript-lane")) in write_paths
    assert all(path != ("config",) for _, path in write_paths)

    payload = document_from_bundle(plan.bundle)["parent_revision"]["payload"]
    clips = payload["config"]["clips"]
    caption = clips[1]
    assert caption["id"] == _caption_id(canonical + "@media-a")
    assert "asset" not in caption
    assert caption["text"] == before["parent"]["config"]["clips"][1]["text"]
    assert caption["at"] == before["parent"]["config"]["clips"][1]["at"]
    assert caption["app"]["retained"] == {"future": [None, False]}
    assert caption["app"]["__generated__"]["provenance"]["sourceItemId"] == canonical
    extension = payload["config"]["app"]["haus.astrid.transcript-lane"]
    assert review_key not in extension
    canonical_review_key = "transcript-source-review:" + _encode_component(canonical)
    assert extension[canonical_review_key]["sourceItemId"] == canonical
    assert extension[canonical_review_key]["opaque"] == {"keep": [None, False]}
    assert payload["config"]["bundle"]["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0]["id"] == canonical

    reopened = bundle_from_document(document_from_bundle(plan.bundle))
    reopened["source_mapping"]["pinned_documents"] = copy.deepcopy(
        bundle["source_mapping"]["pinned_documents"]
    )
    undone = inverse(reopened, plan.records)
    assert document_from_bundle(undone.bundle) == document_from_bundle(bundle)
    redone = inverse(undone.bundle, undone.records)
    assert document_from_bundle(redone.bundle) == document_from_bundle(plan.bundle)


def test_association_refuses_caption_destination_collision_atomically():
    bundle, pin, _, canonical, _ = _known_reconciliation_bundle()
    target_id = _caption_id(canonical + "@media-a")
    bundle["parent"]["config"]["clips"].append({"id": target_id, "track": "other", "clipType": "text"})
    bundle["parent"]["clips"] = copy.deepcopy(bundle["parent"]["config"]["clips"])
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match="caption destination"):
        capture_transcript_association(bundle, "asset-a", document=pin)
    assert bundle == before


def test_association_refuses_shared_review_ownership_atomically():
    bundle, pin, _, _, _ = _known_reconciliation_bundle()
    old = copy.deepcopy(bundle["parent"]["config"]["bundle"]["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0])
    old["sourceArtifactRef"] = {"assetId": "asset-b"}
    bundle["parent"]["config"]["bundle"]["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF].append(old)
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match="review ownership"):
        capture_transcript_association(bundle, "asset-a", document=pin)
    assert bundle == before


def test_normal_serialization_reload_preserves_nested_carrier_through_inverse_and_redo():
    original, pin = _bundle()
    reloaded = bundle_from_document(document_from_bundle(original))
    # A normal App reload returns the persisted bundle; the normal command
    # boundary then hydrates the exact transcript pin through its source seam.
    reloaded["source_mapping"]["pinned_documents"] = copy.deepcopy(
        original["source_mapping"]["pinned_documents"])
    command = capture_transcript_association(reloaded, "asset-a", document=pin)
    plan = execute(reloaded, [command])

    persisted = document_from_bundle(plan.bundle)
    reopened = bundle_from_document(persisted)
    nested = reopened["parent"]["config"]["bundle"]
    assert nested["transcriptReferences"]["associations"]
    assert nested["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF]
    assert "transcriptReferences" not in reopened["parent"]
    assert "sourceItemsBySchemaRef" not in reopened["parent"]

    undone = inverse(reopened, plan.records)
    assert document_from_bundle(undone.bundle) == document_from_bundle(original)
    redone = inverse(undone.bundle, undone.records)
    redone_payload = document_from_bundle(redone.bundle)["parent_revision"]["payload"]
    assert redone_payload["config"]["bundle"] == nested


def test_rejected_parent_level_prototype_never_becomes_a_second_carrier():
    bundle, pin = _bundle()
    bundle["parent"]["transcriptReferences"] = {"schema": REFERENCES_SCHEMA, "associations": []}
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match="parent.config.bundle"):
        capture_transcript_association(bundle, "asset-a", document=pin)
    assert bundle == before


def test_missing_persisted_bundle_is_created_as_nested_recorded_container():
    bundle, pin = _bundle()
    del bundle["parent"]["config"]["bundle"]
    command = capture_transcript_association(bundle, "asset-a", document=pin)
    plan = execute(bundle, [command])
    nested = plan.bundle["parent"]["config"]["bundle"]
    assert nested["transcriptReferences"]["associations"]
    assert nested["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF]
    assert inverse(plan.bundle, plan.records).bundle["parent"]["config"].get("bundle") is None

