"""Production fork owner projection compatibility controls."""
from __future__ import annotations

import pytest

from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_auth import command_output

from .test_timeline_popup_fork_authority import _case


def _production_projection_case():
    boundary, record, following, accepted = _case()
    owner = boundary["parent"]["payload"]["occurrences"][0]
    projected_owner = {key: value for key, value in owner.items()
                       if key != "shot_revision_id"}
    projected_owner["shot_id"] = "authoring-owner"
    record["reads"] = [
        {"ref": "occurrence:occ-new", "path": [],
         "state": {"state": "present", "value": projected_owner}},
        {"ref": "occurrence:occ-new/shot", "path": ["shot_id"],
         "state": {"state": "present", "value": owner["shot_id"]}},
    ]
    record["writes"][1]["before"] = {"state": "present", "value": "authoring-owner"}
    return boundary, record, following, accepted


def test_fork_owner_uses_authenticated_agent_projection():
    boundary, record, following, accepted = _production_projection_case()

    result = command_output(boundary, record, following, accepted=accepted)

    assert result["parent"]["payload"]["occurrences"][0]["shot_id"] == "fork-shot"


@pytest.mark.parametrize("mutation", ["source", "projection", "missing"])
def test_fork_owner_projection_rejects_tampering(mutation):
    boundary, record, following, accepted = _production_projection_case()
    if mutation == "source":
        record["reads"][1]["state"]["value"] = "foreign-shot"
    elif mutation == "projection":
        record["reads"][0]["state"]["value"]["duration_ms"] = 999
    else:
        record["reads"].pop()

    with pytest.raises(CommitRejected):
        command_output(boundary, record, following, accepted=accepted)


def test_fork_owner_projection_rejects_forged_local_identity():
    boundary, record, following, accepted = _production_projection_case()
    record["reads"][0]["state"]["value"]["shot_id"] = "forged-owner"
    record["writes"][1]["before"]["value"] = "forged-owner"

    with pytest.raises(CommitRejected):
        command_output(boundary, record, following, accepted=accepted,
                       identity_scope=("project", "timeline"))

