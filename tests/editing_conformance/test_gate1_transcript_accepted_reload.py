"""Persisted transcript association proof against the compatible Runtime.

This is a bounded carrier/history witness, not native App qualification.  The
normal App-generated caption/review cohort is not available in this checkout;
the pure Agent tests cover those leaves separately.
"""
from __future__ import annotations

import pytest

from astrid.sdk.media_transcript import transcript_document_id
from astrid.sdk.timeline import commit as agent
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.native_transcript_association import (
    TRANSCRIPT_SCHEMA_REF,
    capture_transcript_association,
)
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


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


def test_transcript_association_survives_accepted_reload_inverse_and_restart(tmp_path):
    use_runtime()
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    root = tmp_path / "transcript-reload"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "transcript-proof", "name": "Transcript proof"})["id"]
        service.create_timeline(project, "film", idempotency_key="create-film")
        media = service.ingest(
            project, b"transcript-proof-audio", media_type="audio/wav",
            original_name="proof.wav", idempotency_key="proof-media",
        )["data"]["object_id"]
        document_id = transcript_document_id(project, media, "source-1")
        old_content = _content(media, "transcript-source:source-1:segment:segment-a")
        old_document = service.create_document(
            project, {"document_id": document_id, "kind": "media.transcript", "content": old_content},
            idempotency_key="proof-transcript-v1",
        )["data"]
        old_pin = _pin(project, media, old_content, 1)

        registry = {"assets": {"asset-a": {"media_id": media, "type": "audio"}}}
        parent = {
            "config": {
                "output": {"fps": 30},
                "registry": registry,
                "bundle": {
                    "schema_version": 1,
                    "transcriptReferences": {
                        "schema": "media.transcript.references/v1", "associations": [],
                    },
                    "itemsBySchemaRef": {TRANSCRIPT_SCHEMA_REF: []},
                },
                "clips": [],
                "tracks": [],
            },
            "clips": [],
            "occurrences": [],
            "registry": registry,
        }
        service.publish_parent_composition(
            project, "film", {
                "project_id": project,
                "timeline_id": "film",
                "expected_head": None,
                "parent_revision_id": "proof-seed",
                "parent_composition": parent,
            }, idempotency_key="proof-seed",
        )
        service.register_timeline_commit_provider(agent.create_runtime_commit_service())

        def head():
            timeline = service.get_project_timeline(project, "film")
            return {
                "revision_id": timeline["head_revision_id"],
                "publication_id": timeline["head_publication_id"],
            }

        def persisted(revision_id):
            # This reads the Runtime's immutable accepted closure after it has
            # been committed, rather than reusing the detached command input.
            return service._timeline_commits()[0].revision_closure(project, "film", revision_id)

        def submit(command, key):
            current = head()
            body = {
                "api_version": 1,
                "project_id": project,
                "timeline_id": "film",
                "base_revision_id": current["revision_id"],
                "base_publication_id": current["publication_id"],
                "commands": [command],
            }
            return service.commit_timeline(
                project, "film", body, idempotency_key=key, publisher="agent-proof",
                invocation_path=route_path(project, "film"), authorize=lambda: None,
            )

        initial = bundle_from_document(persisted("proof-seed"))
        initial["source_mapping"]["pinned_documents"] = [{"pin": old_pin, "document": old_document}]
        first = submit(
            capture_transcript_association(initial, "asset-a", document=old_pin),
            "proof-associate-v1",
        )

        canonical_id = "transcript-source:asset-a:source:source-1:segment:segment-a"
        new_content = _content(media, canonical_id)
        new_document = service.update_document(
            project, document_id,
            {"expected_version": 1, "content": new_content},
            idempotency_key="proof-transcript-v2",
        )["data"]
        new_pin = _pin(project, media, new_content, 2)

        # Reopen before the replacement so its command starts from accepted
        # history and the persisted nested carrier, not the detached first plan.
        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(agent.create_runtime_commit_service())
        replacement_bundle = bundle_from_document(persisted(first["data"]["accepted_revision_id"]))
        replacement_bundle["source_mapping"]["pinned_documents"] = [
            {"pin": old_pin, "document": old_document},
            {"pin": new_pin, "document": new_document},
        ]
        replacement = capture_transcript_association(
            replacement_bundle, "asset-a", document=new_pin, previous_document=old_pin,
        )
        second = submit(replacement, "proof-associate-v2")
        accepted = second["data"]["canonical_document"]
        nested = accepted["parent_revision"]["payload"]["config"]["bundle"]
        assert nested["transcriptReferences"]["associations"] == [
            {"assetId": "asset-a", "documentId": new_pin["document_id"]},
        ]
        assert nested["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0]["id"] == canonical_id
        assert accepted["dependency_manifest"]["documents"] == [old_pin, new_pin]

        history = service.list_timeline_commits(project, "film", authorize=lambda: None)["items"]
        replacement_entry = next(
            entry for entry in history if entry["receipt"]["receipt_id"] == second["receipt"]["receipt_id"]
        )
        dependencies = replacement_entry["records"]["commands"][0]["dependencies"]
        assert dependencies[:2] == [
            {"key": "transcript.document", "kind": "transcript", "pin": new_pin, "policy": "exact"},
            {"key": "transcript.previous", "kind": "transcript", "pin": old_pin, "policy": "exact"},
        ]
        assert {tuple(sorted(dependency["pin"].items())) for dependency in dependencies} == {
            tuple(sorted(old_pin.items())), tuple(sorted(new_pin.items())),
        }

        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(agent.create_runtime_commit_service())
        assert persisted(accepted["parent_revision"]["revision_id"]) == accepted
        undone = submit(_inverse(second["receipt"]["receipt_id"]), "proof-undo-v2")
        undone_document = undone["data"]["canonical_document"]
        undone_bundle = undone_document["parent_revision"]["payload"]["config"]["bundle"]
        assert undone_bundle["transcriptReferences"]["associations"] == [
            {"assetId": "asset-a", "documentId": old_pin["document_id"]},
        ]
        assert undone_bundle["itemsBySchemaRef"][TRANSCRIPT_SCHEMA_REF][0]["id"] == old_content["segments"][0]["id"]

        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(agent.create_runtime_commit_service())
        redone = submit(_inverse(undone["receipt"]["receipt_id"]), "proof-redo-v2")
        assert redone["data"]["canonical_document"] == accepted
        assert persisted(accepted["parent_revision"]["revision_id"])["parent_revision"]["payload"]["config"]["bundle"] == nested
    finally:
        service.close()
