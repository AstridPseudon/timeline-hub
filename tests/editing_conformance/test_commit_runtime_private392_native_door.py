"""One bounded private392 project-data case through the authenticated Door."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

# The normal private pin is part of this qualification.  Keeping the selector
# here makes an explicit central socket run independent of ambient Runtime
# checkouts and lets the source-identity assertions below prove the import.
RUNTIME_PIN = Path("/home/user/work/wt/rt-pin-f8da4b6d").resolve()
REMOTION_PIN = Path("/home/user/work/runtimes/agent-remotion-0013").resolve()
os.environ["ASTRID_RUNTIME_CHECKOUT"] = str(RUNTIME_PIN)
os.environ["ASTRID_REMOTION_PROJECT_DIR"] = str(REMOTION_PIN)

import pytest  # noqa: E402  (environment must be selected before test imports)

from tests.editing_conformance.test_commit_runtime_m1 import film, open_client, renderer_off  # noqa: E402
from tests.helpers.runtime import use_runtime  # noqa: E402

pytestmark = pytest.mark.integration

TARGET = "com.example.private392"
SOURCE_KEY = "__dsl__:dsl://com.example.private392/main.json"
SOURCE_MAP_KEY = "__dsl_sm__:private392-source-map"
HEALTH_DIGEST = "sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042"


def _command(key, value):
    return {
        "schema_version": 1,
        "op": "project-data.write",
        "version": "1",
        "select": "parent",
        "args": {"target": TARGET, "key": key, "value": value, "mode": "replace"},
    }


def _head(client, fixture):
    result = client.timelines.history(fixture.project_id, fixture.timeline_id, limit=100)
    assert result.ok, result.as_dict()
    return result.data["head"]


def _body(fixture, head, commands):
    return {
        "api_version": 1,
        "project_id": fixture.project_id,
        "timeline_id": fixture.timeline_id,
        "base_revision_id": head["revision_id"],
        "base_publication_id": head["publication_id"],
        "commands": commands,
        "source": {"via": "python"},
        "rationale": "bounded private392 native Door qualification",
    }


def _commit(client, fixture, commands, key, *, head=None):
    return client.timelines.commit(
        fixture.project_id,
        fixture.timeline_id,
        _body(fixture, head or _head(client, fixture), commands),
        idempotency_key=key,
    )


def _project_data(document):
    return document["parent_revision"]["payload"]["config"].get("app", {}).get(TARGET, {})


def test_private392_project_data_door_roundtrip_stale_guard_and_opaque_rebase(
    tmp_path, film, renderer_off, real_runtime,
):
    """Use the real startup provider and authenticated /v1 Door for one case."""
    runtime = use_runtime()
    agent_root = Path(__file__).resolve().parents[2]
    agent_head = subprocess.check_output(
        ["git", "-C", str(agent_root), "rev-parse", "HEAD"], text=True,
    ).strip()
    if agent_head != "1303ce6be32e7bd96ed5c6b35afcb15819e81b50":
        # The central runner snapshots uncommitted worker edits in a synthetic
        # commit; the frozen pin must remain its direct parent.
        agent_head = subprocess.check_output(
            ["git", "-C", str(agent_root), "rev-parse", "HEAD^"], text=True,
        ).strip()
    assert agent_head == "1303ce6be32e7bd96ed5c6b35afcb15819e81b50"
    assert subprocess.check_output(["git", "-C", str(RUNTIME_PIN), "rev-parse", "HEAD"], text=True).strip() == (
        "f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414"
    )

    import astrid_runtime_client
    import runtime_protocol
    from astrid_runtime_client import contract_metadata

    imported = {
        "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()),
        "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()),
        "runtime_protocol_sha256": hashlib.sha256(
            Path(runtime_protocol.__file__).read_bytes()
        ).hexdigest(),
        "astrid_runtime_client_sha256": hashlib.sha256(
            Path(astrid_runtime_client.__file__).read_bytes()
        ).hexdigest(),
    }
    print(json.dumps(imported, sort_keys=True))
    assert Path(imported["runtime_protocol"]).is_relative_to(runtime)
    assert Path(imported["astrid_runtime_client"]).is_relative_to(agent_root)
    assert Path(runtime_protocol.__file__).read_bytes() == (RUNTIME_PIN / "runtime_protocol/__init__.py").read_bytes()
    assert contract_metadata.CONTRACT_VERSION == "0.2.13"
    assert contract_metadata.SCHEMA_DIGEST == HEALTH_DIGEST

    fixture, _, _ = film
    daemon = real_runtime(fixture.duplicate_root, support_root=tmp_path / "support",
                          authoring_profile="astrid")
    client = open_client(daemon)
    health = client._remote._transport.health()
    assert health["status"] == "ok"
    assert health["protocol"] == "workspace.v1"
    assert health["schema_digest"] == HEALTH_DIGEST

    opaque = {"version": 1, "opaque": {"__proto__": [None, False, {"keep": True}]}}
    initial_head = _head(client, fixture)
    first = _commit(client, fixture, [_command(SOURCE_KEY, opaque)], "private392-project-data")
    assert first.ok, first.as_dict()
    accepted = first.data["canonical_document"]
    assert _project_data(accepted)[SOURCE_KEY] == opaque
    stored = client._remote._transport.get_project_parent_composition_revision(
        fixture.project_id, fixture.timeline_id, first.data["accepted_revision_id"],
    )
    assert stored["payload"]["config"]["app"][TARGET][SOURCE_KEY] == opaque

    undone = _commit(client, fixture, [{
        "schema_version": 1,
        "op": "timeline.inverse",
        "version": "1",
        "select": None,
        "args": {"publications": [first.receipt.receipt_id]},
    }], "private392-project-data-undo")
    assert undone.ok, undone.as_dict()
    assert _project_data(undone.data["canonical_document"]) == {}

    redone = _commit(client, fixture, [{
        "schema_version": 1,
        "op": "timeline.inverse",
        "version": "1",
        "select": None,
        "args": {"publications": [undone.receipt.receipt_id]},
    }], "private392-project-data-redo")
    assert redone.ok, redone.as_dict()
    assert _project_data(redone.data["canonical_document"])[SOURCE_KEY] == opaque

    before_refusal = client.timelines.history(fixture.project_id, fixture.timeline_id, limit=100).data
    stale_same_leaf = _commit(
        client, fixture, [_command(SOURCE_KEY, {"changed": True})],
        "private392-project-data-stale-same", head=initial_head,
    )
    assert not stale_same_leaf.ok, stale_same_leaf.as_dict()
    assert client.timelines.history(fixture.project_id, fixture.timeline_id, limit=100).data == before_refusal

    disjoint = _commit(
        client, fixture, [_command(SOURCE_MAP_KEY, {"source": SOURCE_KEY})],
        "private392-project-data-disjoint", head=initial_head,
    )
    assert disjoint.ok, disjoint.as_dict()
    data = _project_data(disjoint.data["canonical_document"])
    assert data[SOURCE_KEY] == opaque
    assert data[SOURCE_MAP_KEY] == {"source": SOURCE_KEY}
