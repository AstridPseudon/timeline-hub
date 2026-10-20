"""Read-only capture certification using the startup semantic provider."""
from __future__ import annotations

import copy
import json

from .errors import ConflictError, RuntimeErrorBase, ValidationError
from .snapshot_refs import working_copy_binding
from .timeline_commit import CommitRejected
from .timeline_commit_port import detached, digest
from .util import canonical_json


RESEND_HINT = 'send it as source_kind "cas" (explicit UNCERTIFIED) or forward the real authoring_preview.candidate'


def _equal(left, right, message):
    if canonical_json(left) != canonical_json(right):
        raise ConflictError(message)


def _candidate_document(commits, base, preview, ref):
    candidate = preview["candidate"]
    publication = preview["publication"]
    binding = ref["working_copy"]
    _equal(preview["kind"], "authoring-candidate-preview", "invalid authoring preview kind")
    _equal(preview["candidate_digest"], digest(candidate), "candidate digest changed")
    _equal(preview["publication_digest"], digest(publication), "candidate publication digest changed")
    _equal(preview["head"], candidate["base_parent"], "candidate base bindings differ")
    _equal(candidate["base_parent"], {
        "revision_id": binding["base_revision_id"], "content_digest": binding["base_revision_digest"],
    }, "candidate base differs from capture binding")
    for value in (candidate, publication):
        _equal([value["project_id"], value["timeline_id"]],
               [base["project_id"], base["timeline_id"]], "candidate scope differs from saved base")
    _equal([preview["candidate_digest"], preview["publication_digest"],
            publication["parent_revision_id"], publication["expected_head"]],
           [binding["candidate_digest"], binding["publication_digest"],
            ref["revision_id"], binding["base_revision_id"]], "candidate differs from capture binding")
    document = copy.deepcopy(base)
    document["parent_revision"] = {
        "revision_id": publication["parent_revision_id"], "content_digest": publication["content_digest"],
        "payload": publication["parent_composition"],
    }
    manifest = copy.deepcopy(publication["dependency_manifest"])
    # A draft may reuse the exact document inputs retained by its saved base.
    pins = base["dependency_manifest"]["documents"]
    _equal(manifest.get("documents", pins), pins, "candidate document inputs are not retained by its base")
    manifest["documents"] = copy.deepcopy(pins)
    document["dependency_manifest"] = manifest
    for family, key in (("shot_revisions", "shots"), ("internal_timeline_revisions", "internal_timelines")):
        rows = {row["revision_id"]: row for row in base[family]}
        rows.update((row["revision_id"], row) for row in publication[family])
        document[family] = [rows[pin["revision_id"]] for pin in manifest[key]]
    commits._validate_closure(document)


def validate_capture(service, snapshot, ref, inputs):
    source_kind = ref.get("source_kind") or ("revision" if ref.get("revision_id") else "cas")
    if source_kind == "cas":
        return
    method = getattr(service._timeline_commit_provider, "project_capture", None)
    if not callable(method):
        raise ValidationError("canonical capture projection provider is unavailable")
    try:
        commits, _ = service._timeline_commits()
        preview = None
        revision = ref["revision_id"]
        if source_kind == "working_copy":
            preview = detached(inputs.get("authoring_preview"))
            if not isinstance(preview, dict):
                raise ValidationError("working-copy capture requires its actual authoring_preview; " + RESEND_HINT)
            revision = ref["working_copy"]["base_revision_id"]
        document = commits.revision_closure(ref["project_id"], ref["timeline_id"], revision)
        if preview is not None:
            _candidate_document(commits, document, preview, ref)
        projection = detached(method(detached(document), authoring_preview=preview))
        for key in ("config", "registry"):
            _equal(snapshot[key], projection[key], "capture differs from authoritative " + key)
        expansion = projection["expansion"]
        _equal(expansion["parent_revision_id"], ref["revision_id"], "projector returned a different revision")
        if preview is None:
            _equal(expansion["parent_content_digest"], ref["revision_digest"], "capture parent digest changed")
        metadata = snapshot["metadata"]
        authority = metadata["capture_authority"]
        for value in (authority, metadata.get("canonical_timeline", authority)):
            _equal(value["parent_content_digest"], expansion["parent_content_digest"], "capture parent digest changed")
            _equal(value["expansion"], expansion, "capture expansion differs from authoritative projection")
        if preview is not None:
            _equal(metadata["working_copy"], expansion["working_copy"], "capture candidate marker changed")
            _equal(working_copy_binding(snapshot, ref["revision_id"]), ref["working_copy"],
                   "capture candidate binding changed")
    except CommitRejected as exc:
        raise ConflictError(exc.failure["message"], details=exc.failure["details"]) from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise ValidationError("capture source or authoring_preview is invalid; " + RESEND_HINT) from exc


def claim_capture_view(service, spec):
    """Present a stored capture as canonical only while it still verifies.

    Specs admitted before capture content was checked stay readable and are
    never rewritten; a claim of one that cannot be verified exactly now is
    labelled CAS-only (uncertified legacy preview) instead.
    """
    inner = spec.get("spec") if isinstance(spec.get("spec"), dict) else {}
    context = inner.get("authority_context") if isinstance(inner.get("authority_context"), dict) else {}
    ref = context.get("capture_snapshot_ref")
    if not isinstance(ref, dict) or ref.get("source_kind") not in {"revision", "working_copy"}:
        return spec
    try:
        snapshot = json.loads(service.object(ref["digest"])[1])
        validate_capture(service, snapshot, ref, inner.get("inputs") if isinstance(inner.get("inputs"), dict) else {})
        return spec
    except (RuntimeErrorBase, OSError, KeyError, TypeError, ValueError):
        pass
    uncertified = {"digest": ref["digest"], "project_id": ref.get("project_id"),
                   "timeline_id": ref.get("timeline_id"), "source_kind": "cas"}

    def relabel(value):
        if isinstance(value, dict):
            return {key: uncertified if key == "capture_snapshot_ref" and item == ref else relabel(item)
                    for key, item in value.items()}
        if isinstance(value, str):
            try:
                decoded = json.loads(value)
            except ValueError:
                return value
            if isinstance(decoded, dict) and "capture_snapshot_ref" in decoded:
                return canonical_json(relabel(decoded))
        return value

    return relabel(spec)
