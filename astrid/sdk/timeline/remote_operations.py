"""Remote Timeline route implementations kept outside the family facade."""

from __future__ import annotations

import uuid
from typing import Any, Mapping

from astrid.sdk.contracts import DomainResult, ErrorObject


def commit_timeline(timelines: Any, project, ref, body: Mapping[str, Any], *, idempotency_key=None):
    """Commit a scoped command batch without changing its request body."""
    key = idempotency_key or uuid.uuid4().hex
    resolved = timelines._resolve_timeline(project, ref)
    if not resolved.ok:
        return DomainResult.failure(resolved.error, idempotency_key=key)
    scope = resolved.data
    project_id = scope.get("project_id") if isinstance(scope, Mapping) else None
    timeline_id = scope.get("timeline_id") if isinstance(scope, Mapping) else None
    if not isinstance(project_id, str) or not project_id or not isinstance(timeline_id, str) or not timeline_id:
        return DomainResult.failure(
            ErrorObject("protocol_error", "timeline scope has no canonical project/timeline identity", {}),
            idempotency_key=key,
        )
    if not isinstance(body, Mapping) or body.get("project_id") != project_id or body.get("timeline_id") != timeline_id:
        return DomainResult.failure(
            ErrorObject(
                "validation_error",
                "commit body does not match the resolved timeline scope",
                {"project_id": project_id, "timeline_id": timeline_id},
            ),
            idempotency_key=key,
        )
    return timelines._typed(
        "commit_timeline", project_id, timeline_id, body,
        key=key, idempotency_key=key,
    )


def history_timeline(timelines: Any, project, ref, *, cursor=None, limit=50):
    """Read scoped immutable commit history, including its exact head pair."""
    resolved = timelines._resolve_timeline(project, ref)
    if not resolved.ok:
        return resolved
    scope = resolved.data
    project_id = scope.get("project_id") if isinstance(scope, Mapping) else None
    timeline_id = scope.get("timeline_id") if isinstance(scope, Mapping) else None
    if not isinstance(project_id, str) or not project_id or not isinstance(timeline_id, str) or not timeline_id:
        return DomainResult.failure(
            ErrorObject("protocol_error", "timeline scope has no canonical project/timeline identity", {})
        )
    return timelines._typed(
        "list_timeline_commits", project_id, timeline_id,
        cursor=cursor, limit=limit,
    )


def recover_timeline(timelines: Any, project, ref, *, expected_version=None, version=None, idempotency_key=None):
    key = idempotency_key or uuid.uuid4().hex
    resolved = timelines._resolve_timeline(project, ref)
    if not resolved.ok or not isinstance(resolved.data, Mapping):
        return DomainResult.failure(resolved.error, idempotency_key=key)
    timeline_id = resolved.data.get("timeline_id")
    if not isinstance(timeline_id, str) or not timeline_id:
        return DomainResult.failure(
            ErrorObject("protocol_error", "timeline listing has no canonical identity", {}),
            idempotency_key=key,
        )
    try:
        value = resolved.data.get("version", resolved.data.get("config_version", 1))
        current_version = int(value)
        expected = int(expected_version) if expected_version is not None else current_version
        target = current_version if version is None else int(version)
    except (TypeError, ValueError):
        return DomainResult.failure(
            ErrorObject("protocol_error", "Runtime timeline listing has no valid version", {}),
            idempotency_key=key,
        )
    return timelines._typed(
        "recover_timeline",
        timeline_id,
        key=key,
        expected_version=expected,
        version=target,
        idempotency_key=key,
    )
