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
    TRANSCRIPT_SCHEMA_REF,
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
        "config": {"clips": [], "tracks": [], "output": {"fps": 30}},
        "clips": [], "occurrences": [],
        "registry": {"assets": {"asset-a": {"media_id": MEDIA, "type": "audio"}}},
        "transcriptReferences": {"schema": "media.transcript.references/v1", "associations": []},
        "sourceItemsBySchemaRef": {TRANSCRIPT_SCHEMA_REF: []},
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
    assert payload["transcriptReferences"]["associations"] == [{"assetId": "asset-a", "documentId": pin["document_id"]}]
    assert payload["sourceItemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0]["payload"]["words"][0]["id"] == "word-a"
    assert payload["opaque"] == {"keep": [None, False]}
    assert bundle_from_document(document_from_bundle(plan.bundle))["parent"]["sourceItemsBySchemaRef"] == payload["sourceItemsBySchemaRef"]


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
    assert plan.bundle["parent"]["sourceItemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0]["payload"]["documentId"] == new_pin["document_id"]


def test_association_refuses_caption_reconciliation_before_any_write():
    bundle, pin = _bundle(caption=True)
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match="caption/review reconciliation"):
        capture_transcript_association(bundle, "asset-a", document=pin)
    assert bundle == before

