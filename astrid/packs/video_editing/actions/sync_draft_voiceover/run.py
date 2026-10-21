"""Settle a draft narration proposal under the managed outer claim."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from astrid.core.pack.entrypoint import guard_canonical_entrypoint

guard_canonical_entrypoint("video_editing.sync_draft_voiceover")

def _decode(value: Any, default: Any) -> Any:
    if value is None:
        return default
    if isinstance(value, str):
        return json.loads(value)
    return value


def _as_bool(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def run(
    *,
    project: str,
    timeline_ref: str,
    timing_policy: str,
    settings: Any = None,
    occurrence_ids: Any = None,
    adopt_clip_ids: Any = None,
    padding_seconds: float = 0.15,
    plan_only: bool = False,
) -> dict[str, Any]:
    """Settle a managed proposal or the helper's advisory report; never publish."""
    from astrid.core._shared.result_manifest import build_manifest, write_manifest
    from astrid.core.execution.executor._action_context import (
        _PreparationClient,
        _require_action_context,
    )
    from astrid.core.foundation.atomic_io import write_json_atomic
    from astrid.packs.video_editing.shared.draft_voiceover import _sync_draft_voiceover_proposal
    from astrid.sdk.timeline.producer import build_producer_batch

    context = _require_action_context()
    if not project:
        raise ValueError("project is required")
    if not timeline_ref:
        raise ValueError("timeline_ref is required")
    settings_value = _decode(settings, {})
    occurrence_value = _decode(occurrence_ids, None)
    adopt_value = _decode(adopt_clip_ids, [])
    if settings_value is None:
        settings_value = {}
    if adopt_value is None:
        adopt_value = []

    from astrid.sdk import AstridClient

    with AstridClient.open_from_launcher() as client:
        result = _sync_draft_voiceover_proposal(
            _PreparationClient(client, context),
            project,
            timeline_ref,
            settings=settings_value,
            occurrence_ids=occurrence_value,
            adopt_clip_ids=adopt_value,
            timing_policy=timing_policy,
            padding_seconds=float(padding_seconds),
            plan_only=_as_bool(plan_only),
        )
    if not isinstance(result, dict):
        raise TypeError("draft voiceover synchronization must return a mapping")
    proposal = result.get("authoring_proposal")
    if isinstance(proposal, dict):
        if (proposal.get("producer") != context.producer
                or proposal.get("admitted_target") != context.admitted_target):
            raise ValueError("authoring proposal does not match the trusted outer claim")
        build_producer_batch(proposal)
        proposal_path = context.out / "authoring-proposal.json"
        write_json_atomic(proposal_path, proposal)
        manifest_outputs = [{"name": "authoring_proposal", "path": proposal_path.name, "type": "file",
                             "artifact_type": "timeline/authoring-proposal", "role": "result", "is_primary": True}]
        action_result = {"authoring_proposal": proposal}
    elif result.get("status") in {"planned", "unchanged"}:
        report_path = context.out / "report.json"
        write_json_atomic(report_path, result)
        manifest_outputs = [{"name": "report", "path": report_path.name, "type": "file",
                             "artifact_type": "application/json", "role": "result", "is_primary": True}]
        action_result = {"report": result}
    else:
        raise ValueError("synchronization produced neither an authoring proposal nor an advisory report")
    manifest = build_manifest(
        kind="video_editing.sync_draft_voiceover",
        inputs={},
        outputs=manifest_outputs,
        created=datetime.now(timezone.utc).isoformat(),
    )
    write_manifest(context.out / "manifest.json", manifest)
    return action_result
