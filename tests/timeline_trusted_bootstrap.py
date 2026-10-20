"""Trusted setup only; import from ``<runtime checkout>/tests`` on sys.path.

This does not install an Agent provider or qualify migration semantics. The
returned receipt/history are genuinely produced by Runtime storage acceptance,
labelled with a test-only operation. Never submit that operation to a product
endpoint. The caller owns real managed media and live Documents beforehand.
"""
from __future__ import annotations

from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_commit_baseline import empty_bootstrap_document
from runtime_protocol.timeline_commit_inputs import (
    DocumentInputLink,
    capture_document_input,
    persist_document_input_links,
    validate_captured_document_inputs,
)
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_store import detached, digest, request_identity
from runtime_protocol.timeline_commit_validation import validate_commit_value


def seed_trusted_legacy_parent(service, document, *, idempotency_key):
    """Seed an exact raw CanonicalDocument over a fresh empty timeline.

    Project/timeline, managed media and pinned Documents must already exist via
    ordinary APIs. No identity, time, fps, pin or payload is rewritten here.
    Only a legacy parent with no shots/occurrences is supported. Inputs must be
    current on first use; retry returns storage's original receipt. The helper
    records the actual root replacement, not a migration command or Agent
    semantic acceptance. Later migration/reload/inverse belong to the Agent.
    """
    document = detached(document)
    validate_commit_value(document, "CanonicalDocument")
    project, timeline = document["project_id"], document["timeline_id"]
    parent, manifest = document["parent_revision"], document["dependency_manifest"]
    if (document["shot_revisions"] or document["internal_timeline_revisions"]
            or parent["payload"]["occurrences"]
            or not parent["payload"]["config"].get("pinnedShotGroups")):
        raise ValidationError("trusted setup requires a legacy parent without canonical shots")
    if not isinstance(idempotency_key, str) or not idempotency_key:
        raise ValidationError("trusted setup requires an idempotency key")
    commits, _ = service._timeline_commits()
    authorize = service._timeline_authorize(project, timeline, lambda: None)
    # This is Runtime's genuine empty bootstrap, including its provenance.
    head = commits.bootstrap(project, timeline, authorize=authorize)
    page = commits.history(project, timeline, head)
    base = page["items"][0]
    if base["intent"] != "bootstrap":
        raise ValidationError("trusted setup requires an empty bootstrap ancestry")
    original_head = {"revision_id": base["revision_id"], "publication_id": base["publication_id"]}
    command = {"schema_version": 1, "op": "test.trusted-legacy-bootstrap", "version": "1",
               "select": "parent", "args": {"document_digest": digest(document)}, "created": []}
    request = {"api_version": 1, "project_id": project, "timeline_id": timeline,
               "base_revision_id": original_head["revision_id"],
               "base_publication_id": original_head["publication_id"], "commands": [command],
               "rationale": "Trusted test setup only; no Agent migration acceptance"}
    context = {"request": request, "invocation": {"operation": "commitTimeline",
               "path": route_path(project, timeline), "body": detached(request)},
               "idempotency_key": idempotency_key, "realm_id": service.realm["id"],
               "publisher": "test-only-trusted-bootstrap"}
    context["request_hash"] = request_identity(context)
    replay = commits.lookup(context, authorize=authorize)
    if replay is not None:
        return replay
    before = commits.revision_closure(project, timeline, head["revision_id"])
    if (head != original_head or page["next_cursor"] is not None or len(page["items"]) != 1
            or before != empty_bootstrap_document(project, timeline, head["revision_id"])):
        raise ValidationError("trusted setup cannot overwrite an edited timeline")
    captures = []
    for pin in manifest["documents"]:
        resource = service.get_document(project, pin["document_id"])
        captures.append(capture_document_input(
            service.store.conn, project, pin, expected_kind=resource["kind"],
            expected_schema=resource["content"].get("schema"),
        ))
    links = [DocumentInputLink(capture, "transcript" if capture.document["kind"] == "media.transcript"
                              else "source", ordinal) for ordinal, capture in enumerate(captures)]

    class Inputs:
        def validate(self, prepared):
            validate_captured_document_inputs(service.store.conn, captures)

        def persist(self, prepared, publication_id, revision_id):
            persist_document_input_links(service.store.conn, project_id=project, timeline_id=timeline,
                                         publication_id=publication_id, revision_id=revision_id, links=links)

    record = {"ordinal": 0, "command": command,
              "writes": [{"ref": "parent", "path": [],
                          "before": {"state": "present", "value": before["parent_revision"]["payload"]},
                          "after": {"state": "present", "value": parent["payload"]}}],
              "reads": [], "selections": [], "bindings": [], "created": [], "derived_writes": [],
              "dependencies": [{"key": f"setup-input-{link.ordinal}", "kind": link.dependency_kind,
                                "pin": link.capture.pin, "policy": "exact"} for link in links]}
    prepared = {"expected_head": head, "canonical_document": document, "document_digest": digest(document),
                "records": {"schema_version": 1, "commands": [record], "undo_of": [], "restored_from": None},
                "id_map": {}, "semantic_events": [], "provider_version": "test-only-trusted-bootstrap",
                "compiler_version": "test-only-no-compilation"}
    return commits.accept(context, prepared, authorize=authorize, inputs=Inputs())
