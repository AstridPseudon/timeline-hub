"""One missing assertion for the real native render recovery mapping.

The unchanged publication tests retain the old cancellation/stale-fence
assertions.  The existing D13 Agent integration covers settled proposal ->
requester ``producer.guard`` commit, lost acknowledgement, restart, exact
retry, and revision-pinned render admission.  This small Runtime case adds
the equivalent actual-film refusal/no-write assertion without rebuilding that
integration fixture or inventing a proposal carrier.
"""
from __future__ import annotations

import copy
import os
from pathlib import Path

import pytest

from runtime_protocol.errors import ConflictError

from test_render_native_historical_retry import native_render_case, _move


pytestmark = pytest.mark.integration

_PRIVATE_AGENT = Path("/home/user/work/wt/agt-pin-3c4f6de4")
if _PRIVATE_AGENT.is_dir():
    os.environ["ASTRID_CHECKOUT"] = str(_PRIVATE_AGENT)


def _store_state(service):
    return tuple(service.store.conn.iterdump())


def test_actual_native_render_refuses_stale_revision_selector_without_writes(native_render_case):
    """A real Agent commit cannot hand a stale publication identity to render."""
    case = native_render_case
    accepted = _move(case, "music-bed", 1, "native-recovery-A")
    from astrid.core.dev.journey import build_app_render_admission

    capability = next(
        item for item in case.service.list_capabilities()["items"]
        if item["capability_id"] == "rendering.render"
    )
    built = build_app_render_admission(
        project=case.film.project_id, timeline_id=case.film.timeline_id,
        output_name="native-recovery.mp4", capability=capability, token="test-token",
    )
    request = copy.deepcopy(built["body"])
    request["idempotency_key"] = "native-recovery-stale-selector"
    parent = accepted["data"]["canonical_document"]["parent_revision"]
    request["spec"]["params"]["canonical_revision"] = {
        "project_id": case.film.project_id,
        "timeline_id": case.film.timeline_id,
        "revision_id": accepted["data"]["accepted_revision_id"],
        "publication_id": "stale-publication",
        "content_digest": parent["content_digest"],
    }
    before = _store_state(case.service)
    with pytest.raises(ConflictError, match="render revision does not match"):
        case.service.create_task(request)
    assert _store_state(case.service) == before
    assert case.service.store.conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'"
    ).fetchone()[0] == 0
