"""Actual Agent producer acceptance with a revision-pinned render handoff."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import subprocess
import sys
from types import SimpleNamespace

import pytest

from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider


AGENT_SOURCE = "3c4f6de4fa777323b3386c01c7266b619b86af6d"
pytestmark = pytest.mark.integration


def _digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _settle_output(service, attempt, raw, name, media_type, key):
    service.settle_attempt(
        attempt["attempt_id"],
        {**{field: attempt[field] for field in ("lease_id", "fence", "runtime_epoch")},
         "outputs": [{"name": name, "output_port": name, "kind": "object",
                      "filename": name + ".json", "digest": _digest(raw), "size": len(raw),
                      "media_type": media_type, "durability": "durable",
                      "data_base64": base64.b64encode(raw).decode("ascii")}]},
        idempotency_key=key,
    )


def _settle_proposal(service, attempt, raw, key):
    _settle_output(service, attempt, raw, "authoring_proposal", "application/json", key)


@pytest.fixture
def actual_agent_source(astrid_importable, monkeypatch):
    """Expose the exact private 014 Agent checkout, not the ambient source."""
    root = astrid_importable
    actual_head = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if actual_head != AGENT_SOURCE:
        raise AssertionError(
            f"Agent checkout is not the exact publication source: {root} (HEAD {actual_head}, "
            f"expected {AGENT_SOURCE})"
        )
    for name in [name for name in sys.modules if name == "astrid" or name.startswith("astrid.")]:
        if not str(getattr(sys.modules[name], "__file__", "") or "").startswith(str(root)):
            monkeypatch.delitem(sys.modules, name)
    return root


@pytest.fixture
def native_publication_case(tmp_path, actual_agent_source):
    from astrid.sdk.timeline import build_producer_batch, commit
    from astrid.sdk.timeline.capture import capture_track_create

    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    project = service.create_project({"slug": "native-publication", "name": "Native publication"})["id"]
    service.create_timeline(project, "film", idempotency_key="timeline")
    timeline = service.get_project_timeline(project, "film")
    target = {key: timeline[key] for key in (
        "project_id", "timeline_id", "head_revision_id", "head_publication_id")}
    target = {"project_id": target["project_id"], "timeline_id": target["timeline_id"],
              "base_revision_id": target["head_revision_id"],
              "base_publication_id": target["head_publication_id"]}

    producer_capability = "fixture.propose-track"
    producer_digest = commit._digest(producer_capability)
    child_capability = "fixture.producer-input"
    child_digest = commit._digest(child_capability)
    render_digest = commit._digest("rendering.render")
    service.register_capability({"capability_id": producer_capability, "definition_digest": producer_digest})
    service.register_capability({"capability_id": child_capability, "definition_digest": child_digest})
    service.register_capability({"capability_id": "rendering.render", "definition_digest": render_digest})
    service.register_executor(
        {"executor_id": "worker", "capabilities": [producer_capability, child_capability, "rendering.render"]},
        idempotency_key="executor",
    )

    render = {"capability_id": "rendering.render", "capability_digest": render_digest,
              "spec": {"family": "render", "params": {"timeline_ref": "film", "selector": "rendering.remotion",
                                                         "expected_version": 1,
                                                         "canonical_head_revision_id": target["base_revision_id"]},
                        "inputs": {"output_name": "accepted.mp4", "expected_version": 1}}}
    children = []
    for index in range(2):
        child = service.create_task({"project": project, "capability_id": child_capability,
                                     "capability_digest": child_digest, "input_object_ids": [],
                                     "spec": {"index": index}, "idempotency_key": f"input-{index}"})
        child_attempt = service.claim_next({"executor_id": "worker", "capability_ids": [child_capability],
                                            "runtime_epoch": service.health()["runtime_epoch"]},
                                           idempotency_key=f"claim-input-{index}")
        _settle_output(service, child_attempt, commit._json({"index": index}).encode("utf-8"),
                       "data", "application/json", f"settle-input-{index}")
        children.append(child["task"]["id"])

    task = service.create_task({
        "project": project, "capability_id": producer_capability, "capability_digest": producer_digest,
        "input_object_ids": [], "idempotency_key": "producer",
        "spec": {"runtime_dependencies": {"publication": {"admitted_target": target, "render": render},
                                            "edges": [{"from_task_id": child, "to": "self",
                                                       "requires_event": "task.succeeded", "fence": "runtime_task"}
                                                      for child in children],
                                            "aggregation": {"kind": "ordered_cas_inputs"}},
                 "outputs": {"authoring_proposal": {"type": "file", "artifact_type": "timeline/authoring-proposal"}}},
    })
    attempt = service.claim_next({"executor_id": "worker", "capability_ids": [producer_capability],
                                  "runtime_epoch": service.health()["runtime_epoch"]}, idempotency_key="claim")
    document = service._timeline_commits()[0].revision_closure(project, "film", target["base_revision_id"])
    command = capture_track_create(commit.bundle_from_document(document), "parent",
                                   {"id": "proposed", "kind": "visual", "opaque": [1.0, -0.0, False]})
    proposal = {"schema_version": 1,
                "producer": {"task_id": attempt["task_id"], "attempt_id": attempt["attempt_id"],
                             "executor_id": "worker", "fence": attempt["fence"],
                             "runtime_epoch": attempt["runtime_epoch"]},
                "admitted_target": target, "rationale": "Reviewed native publication", "commands": [command]}
    proposal["proposal_digest"] = commit._digest(proposal)
    proposal_raw = commit._json(proposal).encode("utf-8")
    _settle_proposal(service, attempt, proposal_raw, "settle-proposal")
    request = {"api_version": 1, **build_producer_batch(proposal)}
    case = SimpleNamespace(service=service, root=root, project=project, task=task["task"]["id"],
                           target=target, request=request, render=render, proposal=proposal,
                           capture_track_create=capture_track_create, commit=commit)
    try:
        yield case
    finally:
        case.service.close()


def _submit(case, key):
    return case.service.commit_timeline(
        case.project, "film", case.request, idempotency_key=key, publisher="requester",
        invocation_path=route_path(case.project, "film"), authorize=lambda: None,
    )


def test_actual_agent_publication_is_atomic_pinned_and_exactly_replayable(native_publication_case):
    case = native_publication_case
    assert {key: case.request[key] for key in case.target} == case.target
    accepted = _submit(case, "native-publication")
    checkpoint = case.service.store.timeline_render_publication(case.task)
    assert accepted["data"]["status"] == "accepted"
    assert checkpoint["state"] == "prepared"
    assert checkpoint["result"]["accepted"]["receipt"] == accepted["receipt"]
    assert case.service.store.conn.execute("SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'").fetchone()[0] == 0

    accepted_revision = accepted["data"]["accepted_revision_id"]
    accepted_parent = accepted["data"]["canonical_document"]["parent_revision"]
    pending = copy.deepcopy(checkpoint["prepared"]["pending_render"])
    selector = pending["body"]["spec"]["params"]["canonical_revision"]
    assert selector == {"project_id": case.project, "timeline_id": "film",
                        "revision_id": accepted_revision, "publication_id": accepted["receipt"]["receipt_id"],
                        "content_digest": accepted_parent["content_digest"]}

    later_document = case.service._timeline_commits()[0].revision_closure(case.project, "film", accepted_revision)
    later_command = case.capture_track_create(case.commit.bundle_from_document(later_document), "parent",
                                               {"id": "later", "kind": "visual", "opaque": [2, 0.0, False]})
    later = case.service.commit_timeline(
        case.project, "film", {"api_version": 1, "project_id": case.project, "timeline_id": "film",
                                "base_revision_id": accepted_revision, "base_publication_id": accepted["receipt"]["receipt_id"],
                                "commands": [later_command], "source": {"via": "python"}},
        idempotency_key="later-edit", publisher="requester", invocation_path=route_path(case.project, "film"),
        authorize=lambda: None,
    )
    assert later["data"]["accepted_revision_id"] != accepted_revision

    admitted = case.service.create_task({**pending["body"], "idempotency_key": pending["idempotency_key"]})
    authority = admitted["task"]["spec"]["spec"]["inputs"]["timeline_authority"]
    assert authority["parent_revision_id"] == accepted_revision
    assert authority["publication_id"] == accepted["receipt"]["receipt_id"]
    assert authority["parent_content_digest"] == selector["content_digest"]
    assert case.service.get_project_timeline(case.project, "film")["head_revision_id"] == later["data"]["accepted_revision_id"]
    assert case.service.store.conn.execute("SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'").fetchone()[0] == 1
    render_spec = admitted["task"]["spec"]["spec"]
    assert "timeline_snapshot" not in render_spec["inputs"]
    snapshot_ref = render_spec["timeline_snapshot_ref"]
    assert snapshot_ref["digest"] in admitted["task"]["spec"]["input_object_ids"]
    snapshot = json.loads(case.service.object(snapshot_ref["digest"])[1])
    assert snapshot["config"] == accepted_parent["payload"]["config"]
    assert snapshot["registry"] == accepted_parent["payload"]["registry"]

    case.service.cancel_task_canonical(case.task, {}, idempotency_key="cancel-producer")
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    try:
        assert _submit(case, "native-publication") == accepted
        assert case.service.create_task({**pending["body"], "idempotency_key": pending["idempotency_key"]}) == admitted
        assert case.service.store.conn.execute("SELECT COUNT(*) FROM tasks WHERE capability='rendering.render'").fetchone()[0] == 1
    finally:
        case.service.close()
