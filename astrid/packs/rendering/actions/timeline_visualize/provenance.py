"""Truthful labels for the immutable snapshot a visualize result consumed."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _first_string(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str) and value:
            return value
    return None


def _is_candidate(metadata: Mapping[str, Any], authority: Mapping[str, Any]) -> bool:
    selection = str(metadata.get("selection") or "").strip().lower()
    if selection in {"explicit_candidate_preview", "candidate_preview", "unpublished_candidate_preview"}:
        return True
    if isinstance(metadata.get("working_copy"), Mapping):
        return True
    if isinstance(authority.get("working_copy"), Mapping):
        return True
    if isinstance(authority.get("authoring_preview"), Mapping):
        return True
    mode = str(authority.get("render_mode") or authority.get("mode") or "").strip().lower()
    return mode in {"authoring_candidate_preview", "candidate", "preview", "unpublished"}


def snapshot_label(snapshot: Mapping[str, Any] | None) -> dict[str, Any]:
    """Describe the revision represented by an admitted visualize snapshot.

    The snapshot's canonical authority is the only source of revision identity.
    In particular, ``requested_revision_id`` and current-head fields are not
    used: they can describe a request or a later mutable state rather than the
    bytes that were actually rendered.
    """
    if not isinstance(snapshot, Mapping):
        return {
            "status": "unavailable",
            "label": "revision unavailable",
            "actual_revision_id": None,
            "base_revision_id": None,
        }

    metadata = snapshot.get("metadata")
    metadata = metadata if isinstance(metadata, Mapping) else {}
    canonical = metadata.get("canonical_timeline")
    canonical = canonical if isinstance(canonical, Mapping) else {}
    capture = metadata.get("capture_authority")
    capture = capture if isinstance(capture, Mapping) else {}
    # A composed capture has its own authority block; ordinary managed renders
    # use canonical_timeline. Prefer the capture block only when it carries the
    # immutable parent, never a requested/current-head hint.
    authority = capture if _first_string(
        capture.get("parent_revision_id"), capture.get("head_revision_id"), capture.get("revision_id")
    ) else canonical
    actual = _first_string(
        authority.get("parent_revision_id"), authority.get("head_revision_id"), authority.get("revision_id")
    )
    candidate = _is_candidate(metadata, authority)
    if actual is None and candidate and isinstance(authority.get("authoring_preview"), Mapping):
        preview = authority["authoring_preview"]
        actual = _first_string(
            preview.get("candidate_parent_revision_id"), preview.get("base_revision_id")
        )
    if candidate:
        if actual is None:
            return {
                "status": "unavailable",
                "label": "candidate revision unavailable",
                "actual_revision_id": None,
                "base_revision_id": None,
            }
        return {
            "status": "candidate",
            "label": f"unsaved candidate based on committed revision {actual}",
            "actual_revision_id": None,
            "base_revision_id": actual,
        }
    if actual is None:
        return {
            "status": "unavailable",
            "label": "revision unavailable",
            "actual_revision_id": None,
            "base_revision_id": None,
        }
    return {
        "status": "committed",
        "label": f"committed revision {actual}",
        "actual_revision_id": actual,
        "base_revision_id": None,
    }
