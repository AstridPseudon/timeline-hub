"""Transcript association through the normal authenticated Runtime door.

The saved parent is the existing trusted-test setup boundary.  The edit itself
uses the startup-loaded Agent provider through the public ``/v1`` client; no
provider or schema is installed by this test.
"""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.media_transcript import transcript_document_id
from astrid.sdk.timeline.commit import _digest
from astrid.sdk.timeline.native_transcript_association import (
    REFERENCES_SCHEMA,
    TRANSCRIPT_SCHEMA_REF,
    _caption_id,
    capture_transcript_association,
)
from tests.editing_conformance.test_commit_runtime_m1 import open_client
from tests.helpers.trusted_seed import seed_trusted_parent

pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def _approved_runtime(monkeypatch):
    """Use the independently approved Runtime source for this proof node."""
    monkeypatch.setenv("ASTRID_RUNTIME_CHECKOUT", "/home/user/work/wt/rt-pin-3dcae183")


def _content(media_id: str, segment_id: str) -> dict:
    return {
        "schema": "media.transcript/v1",
        "media_id": media_id,
        "source_id": "source-1",
        "segments": [{
            "id": segment_id,
            "start": 0,
            "end": 1,
            "text": "Hello",
            "words": [{"id": "word-a", "start": 0, "end": 1, "text": "Hello"}],
        }],
    }


def _pin(project: str, media_id: str, content: dict, version: int) -> dict:
    return {
        "document_id": transcript_document_id(project, media_id, content["source_id"]),
        "version": version,
        "content_digest": _digest(content),
    }


def _inverse(publication_id: str) -> dict:
    return {
        "schema_version": 1,
        "op": "timeline.inverse",
        "version": "1",
        "select": None,
        "args": {"publications": [publication_id]},
    }


def _source_item(item_id: str, *, asset_id: str, source_id: str, document_id: str,
                 version: int, text: str = "Hello") -> dict:
    return {
        "id": item_id,
        "shape": "interval",
        "domain": "source_seconds",
        "extent": {"start": 0, "end": 1},
        "schemaRef": TRANSCRIPT_SCHEMA_REF,
        "sourceArtifactRef": {"assetId": asset_id},
        "provenance": {"adapterId": "astrid.projectTranscript", "adapterVersion": "1"},
        "payload": {
            "sourceId": source_id,
            "segmentId": item_id,
            "text": text,
            "words": [{"id": f"{item_id}:word:word-a", "start": 0, "end": 1, "text": text}],
            "documentId": document_id,
            "documentVersion": version,
        },
        "opaque": {"source-item": [None, False, 7]},
    }


def _app_parent(media_id: str, old_pin: dict, old_item: dict, unrelated: list[dict]) -> dict:
    old_id = old_item["id"]
    bundle = {
        "schema_version": 1,
        "futureMetadata": {"keep": [None, False]},
        "transcriptReferences": {
            "schema": REFERENCES_SCHEMA,
            "associations": [{"assetId": "asset-a", "documentId": old_pin["document_id"]}],
        },
        "itemsBySchemaRef": {
            TRANSCRIPT_SCHEMA_REF: [old_item, *unrelated],
            "astrid.other_source/v1": [{"id": "other-1", "opaque": {"keep": True}}],
        },
    }
    media = {
        "id": "media-a",
        "asset": "asset-a",
        "track": "A1",
        "clipType": "audio",
        "at": 0,
        "from": 0,
        "to": 8,
    }
    caption = {
        "id": _caption_id(old_id + "@media-a"),
        "track": "transcript-caption-foundry-track",
        "clipType": "text",
        "at": 0.1,
        "hold": 2.3,
        "x": 143,
        "y": 620,
        "text": {"content": "Human correction", "color": "#cc3377", "fontSize": 51},
        # This is the assetless generated-caption shape from App's
        # importTranscriptIdentity fixture; media-a proves ownership.
        "app": {
            "retained": {"future": [None, False]},
            "__generated__": {
                "extensionId": "haus.astrid.transcript-lane",
                "contributionId": "transcript-caption-foundry",
                "provenance": {
                    "contractVersion": 1,
                    "sourceSchemaRef": TRANSCRIPT_SCHEMA_REF,
                    "sourceItemId": old_id,
                    "sourceFingerprint": "original-source-fingerprint",
                    "generatorVersion": "1.3.0",
                    "outputFingerprint": "original-output-fingerprint",
                    "conflictPolicy": "preserve-output",
                },
            },
        },
    }
    review_key = "transcript-source-review:transcript-source%3Asource-1%3Asegment%3Asegment-a"
    config = {
        "output": {"resolution": "1920x1080", "fps": 30, "file": "out.mp4"},
        "tracks": [
            {"id": "A1", "kind": "audio", "label": "Audio", "muted": False},
            {"id": "transcript-caption-foundry-track", "kind": "visual", "label": "Captions", "muted": False},
        ],
        "clips": [media, caption],
        "app": {
            "unrelated": {"keep": True},
            "haus.astrid.transcript-lane": {
                "preferences": {"color": "blue"},
                review_key: {
                    "schemaVersion": 1,
                    "sourceSchemaRef": TRANSCRIPT_SCHEMA_REF,
                    "sourceItemId": old_id,
                    "status": "accepted-for-source-update",
                    "proposedText": "Human correction",
                    "proposedTimelineStart": 0.1,
                    "proposedTimelineEnd": 2.4,
                    "sourceFingerprintAtGeneration": "original-source-fingerprint",
                    "currentSourceFingerprint": "reviewed-source-fingerprint",
                    "generatedOutputFingerprint": "original-output-fingerprint",
                    "editedOutputFingerprint": "human-output-fingerprint",
                    "generatorVersion": "1.3.0",
                    "handoffFingerprint": "accepted-handoff-fingerprint",
                    "decisionRevision": 12,
                    "opaque": {"keep": [None, False]},
                },
            },
        },
        "bundle": bundle,
    }
    return {
        "config": config,
        "clips": copy.deepcopy(config["clips"]),
        "occurrences": [],
        "registry": {"assets": {"asset-a": {"media_id": media_id, "type": "audio"}}},
    }


def _wire_bundle(client, project: str, timeline: str, revision_id: str | None = None) -> dict:
    result = client.timelines.open_bundle(project, timeline, revision_id=revision_id)
    assert result.ok, result.as_dict()
    return result.data["bundle"]


def test_transcript_association_normal_door_reload_restart_inverse_redo(tmp_path, real_runtime):
    root = tmp_path / "transcript-normal-door"
    support = tmp_path / "support"
    daemon = real_runtime(root, support_root=support, authoring_profile="astrid")
    assert daemon.service._timeline_commit_provider.provider_id == "astrid-v1"
    service = daemon.service
    project = service.create_project({"slug": "transcript-door", "name": "Transcript door"})["id"]
    service.create_timeline(project, "film", idempotency_key="transcript-door-film")
    media = service.ingest(
        project, b"transcript-door-audio", media_type="audio/wav",
        original_name="door.wav", idempotency_key="transcript-door-media",
    )["data"]["object_id"]
    client = open_client(daemon)

    old_id = "transcript-source:source-1:segment:segment-a"
    old_content = _content(media, old_id)
    document_id = transcript_document_id(project, media, "source-1")
    created = client.documents.create(
        kind="media.transcript", content=old_content, project=project,
        document_id=document_id, idempotency_key="transcript-door-v1",
    )
    assert created.ok, created.as_dict()
    old_document = created.data
    old_pin = _pin(project, media, old_content, 1)
    unrelated = [
        _source_item("transcript-source:other:segment:one", asset_id="asset-b",
                     source_id="other-source", document_id="other-document", version=4,
                     text="Other one"),
        _source_item("transcript-source:other:segment:two", asset_id="asset-b",
                     source_id="other-source", document_id="other-document", version=4,
                     text="Other two"),
    ]
    parent = _app_parent(media, old_pin, _source_item(
        old_id, asset_id="asset-a", source_id="source-1", document_id=document_id, version=1,
    ), unrelated)
    seed_trusted_parent(
        service, {
            "project_id": project,
            "timeline_id": "film",
            "expected_head": None,
            "parent_revision_id": "transcript-door-genesis",
            "parent_composition": parent,
            "shot_revisions": [],
            "internal_timeline_revisions": [],
        }, idempotency_key="transcript-door-genesis",
    )

    # The client reload is the authenticated public source of the command's
    # carrier. Hydration supplies only the exact document read from Runtime.
    reloaded = _wire_bundle(client, project, "film")
    assert reloaded["parent"]["config"]["bundle"] == parent["config"]["bundle"]
    reloaded["source_mapping"]["pinned_documents"] = [{"pin": old_pin, "document": old_document}]

    def submit(command: dict, key: str) -> dict:
        history = client.timelines.history(project, "film", limit=100)
        assert history.ok, history.as_dict()
        head = history.data["head"]
        result = client.timelines.commit(
            project, "film", {
                "api_version": 1,
                "project_id": project,
                "timeline_id": "film",
                "base_revision_id": head["revision_id"],
                "base_publication_id": head["publication_id"],
                "commands": [command],
            }, idempotency_key=key,
        )
        assert result.ok, result.as_dict()
        return result.as_dict()

    # V1 is only in the trusted seed's authored carrier at this point; its
    # empty manifest does not authorize retention. Accept it through the
    # normal command path before replacing the live catalog row with V2.
    initial = submit(
        capture_transcript_association(
            reloaded, "asset-a", document=old_pin, previous_document=old_pin,
        ),
        "transcript-door-associate-v1",
    )
    assert initial["data"]["canonical_document"]["dependency_manifest"]["documents"] == [old_pin]
    reloaded = _wire_bundle(client, project, "film", initial["data"]["accepted_revision_id"])
    reloaded["source_mapping"]["pinned_documents"] = [{"pin": old_pin, "document": old_document}]

    canonical_id = "transcript-source:asset-a:source:source-1:segment:segment-a"
    new_content = _content(media, canonical_id)
    updated = client.documents.update(
        document_id, content=new_content, expected_version=1, project=project,
        idempotency_key="transcript-door-v2",
    )
    assert updated.ok, updated.as_dict()
    new_document = updated.data
    new_pin = _pin(project, media, new_content, 2)
    reloaded["source_mapping"]["pinned_documents"].append({"pin": new_pin, "document": new_document})
    replacement = capture_transcript_association(
        reloaded, "asset-a", document=new_pin, previous_document=old_pin,
    )

    accepted = submit(replacement, "transcript-door-associate-v2")
    accepted_data = accepted["data"]
    accepted_document = accepted_data["canonical_document"]
    accepted_bundle = accepted_document["parent_revision"]["payload"]["config"]["bundle"]
    assert accepted_document["dependency_manifest"]["documents"] == [old_pin, new_pin]
    assert accepted_bundle["transcriptReferences"]["associations"] == [
        {"assetId": "asset-a", "documentId": new_pin["document_id"]},
    ]
    assert [row["id"] for row in accepted_bundle["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF]] == [
        unrelated[0]["id"], unrelated[1]["id"], canonical_id,
    ]
    assert accepted_bundle["itemsBySchemaRef"]["astrid.other_source/v1"] == [
        {"id": "other-1", "opaque": {"keep": True}},
    ]
    assert accepted_bundle["futureMetadata"] == {"keep": [None, False]}
    accepted_config = accepted_document["parent_revision"]["payload"]["config"]
    accepted_caption = accepted_config["clips"][1]
    assert "asset" not in accepted_caption
    assert accepted_caption["id"] == _caption_id(canonical_id + "@media-a")
    assert accepted_caption["text"] == {"content": "Human correction", "color": "#cc3377", "fontSize": 51}
    assert accepted_caption["app"]["retained"] == {"future": [None, False]}
    assert accepted_caption["app"]["__generated__"]["provenance"]["sourceItemId"] == canonical_id
    extension = accepted_config["app"]["haus.astrid.transcript-lane"]
    assert "transcript-source-review:transcript-source%3Asource-1%3Asegment%3Asegment-a" not in extension
    canonical_review_key = "transcript-source-review:transcript-source%3Aasset-a%3Asource%3Asource-1%3Asegment%3Asegment-a"
    assert extension[canonical_review_key]["sourceItemId"] == canonical_id
    assert extension[canonical_review_key]["opaque"] == {"keep": [None, False]}
    history_entry = next(
        row for row in client.timelines.history(project, "film", limit=100).data["items"]
        if row["publication_id"] == accepted["receipt"]["receipt_id"]
    )
    dependencies = history_entry["records"]["commands"][0]["dependencies"]
    assert dependencies[:2] == [
        {"key": "transcript.document", "kind": "transcript", "pin": new_pin, "policy": "exact"},
        {"key": "transcript.previous", "kind": "transcript", "pin": old_pin, "policy": "exact"},
    ]

    public_reload = _wire_bundle(client, project, "film", accepted_data["accepted_revision_id"])
    assert public_reload["parent"]["config"]["bundle"] == accepted_bundle
    port = daemon.httpd.server_port
    daemon.stop()
    daemon = real_runtime(root, support_root=support, port=port, authoring_profile="astrid")
    client = open_client(daemon)
    restarted = _wire_bundle(client, project, "film")
    assert restarted["parent"]["config"]["bundle"] == accepted_bundle

    undone = submit(_inverse(accepted["receipt"]["receipt_id"]), "transcript-door-undo-v2")
    undone_bundle = undone["data"]["canonical_document"]["parent_revision"]["payload"]["config"]["bundle"]
    assert undone_bundle["transcriptReferences"]["associations"] == [
        {"assetId": "asset-a", "documentId": old_pin["document_id"]},
    ]
    assert [row["id"] for row in undone_bundle["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF]] == [
        old_id, unrelated[0]["id"], unrelated[1]["id"],
    ]
    undone_config = undone["data"]["canonical_document"]["parent_revision"]["payload"]["config"]
    assert undone_config["clips"][1]["id"] == _caption_id(old_id + "@media-a")
    assert undone_config["clips"][1]["app"]["__generated__"]["provenance"]["sourceItemId"] == old_id
    assert "transcript-source-review:transcript-source%3Aasset-a%3Asource%3Asource-1%3Asegment%3Asegment-a" not in undone_config["app"]["haus.astrid.transcript-lane"]
    assert "transcript-source-review:transcript-source%3Asource-1%3Asegment%3Asegment-a" in undone_config["app"]["haus.astrid.transcript-lane"]
    assert _wire_bundle(client, project, "film", undone["data"]["accepted_revision_id"])["parent"]["config"]["bundle"] == undone_bundle

    redone = submit(_inverse(undone["receipt"]["receipt_id"]), "transcript-door-redo-v2")
    assert redone["data"]["canonical_document"] == accepted_document
    assert _wire_bundle(client, project, "film", redone["data"]["accepted_revision_id"])["parent"]["config"]["bundle"] == accepted_bundle
