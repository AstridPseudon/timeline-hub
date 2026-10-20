"""Actual registered assembler, without a synthetic proposal or legacy SQL seed.

Child settlements are input fixtures, not registered generation qualification.
The assembler itself runs through GenericPackHost and the real Runtime door.
"""
from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import pytest

from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient


class UnsettledRegisteredAssembly(AssertionError):
    pass


@pytest.mark.integration
@pytest.mark.parametrize("duplicate_cas", [False, True])
@pytest.mark.xfail(
    strict=True,
    raises=UnsettledRegisteredAssembly,
    reason="D13: preserve registered assembly while migrating pre-settlement publication to a native proposal",
)
def test_registered_assembler_settles_on_normally_created_timeline(
    tmp_path, monkeypatch, real_runtime, duplicate_cas,
):
    daemon = real_runtime(authoring_profile="astrid")
    service = daemon.service
    client = RuntimeProtocolClient(daemon.endpoint, daemon.worker_token)
    client.executor_id = "astrid-pack-host"
    attempt_root = tmp_path / "assembly"
    host = GenericPackHost(
        pack_roots=[Path(__file__).resolve().parents[3] / "astrid/packs/rendering"],
        client=client, executor_id=client.executor_id, attempt_root=attempt_root,
    )
    try:
        host.discover()
        host.preflight("rendering.assemble_timeline")
        record = host.capabilities["rendering.assemble_timeline"]
        render_record = host.capabilities["rendering.render"]
        project = service.create_project({"slug": "registered", "name": "Registered"})["id"]
        service.create_timeline(project, "main", idempotency_key="timeline")
        service.list_timeline_commits(project, "main", authorize=lambda: daemon.credentials.require(
            daemon.token, "projects:read"))
        head = service.get_project_timeline(project, "main")
        original_target = {"project_id": project, "timeline_id": "main",
                           "base_revision_id": head["head_revision_id"],
                           "base_publication_id": head["head_publication_id"]}
        assert all(isinstance(value, str) and value for value in original_target.values())
        child_capability = "fixture.visual-input"
        child_digest = "sha256:" + hashlib.sha256(child_capability.encode()).hexdigest()
        for capability, digest in ((child_capability, child_digest), (record.id, record.capability_digest),
                                   (render_record.id, render_record.capability_digest)):
            service.register_capability({"capability_id": capability, "definition_digest": digest})
        service.register_executor({"executor_id": client.executor_id,
            "capabilities": [child_capability, record.id], "max_concurrency": 3},
            idempotency_key="executor")
        children = [service.create_task({"project": project, "capability_id": child_capability,
            "capability_digest": child_digest, "input_object_ids": [], "spec": {"index": index},
            "idempotency_key": f"child-{index}"})["task"]["id"] for index in range(2)]
        claims = [service.claim_next({"executor_id": client.executor_id,
            "capability_ids": [child_capability], "runtime_epoch": service.health()["runtime_epoch"]},
            idempotency_key=f"claim-child-{index}") for index in range(2)]
        by_task = {claim["task_id"]: claim for claim in claims}
        # Input fixtures deliberately finish in reverse. No producer artifact,
        # accepted command record, catalog selection or history is fabricated.
        for index in (1, 0):
            claim = by_task[children[index]]
            raw = b"shared visual input" if duplicate_cas else f"visual input {index}".encode()
            service.settle_attempt(claim["attempt_id"], {
                **{key: claim[key] for key in ("lease_id", "fence", "runtime_epoch")},
                "outputs": [{"name": "primary", "role": "primary", "is_primary": True,
                    "digest": "sha256:" + hashlib.sha256(raw).hexdigest(),
                    "data_base64": base64.b64encode(raw).decode(), "media_type": "video/mp4",
                    "duration_seconds": index + 1.0}]}, idempotency_key=f"settle-child-{index}")
        # Match the existing registered host requester. Do not enrich its spec
        # with a test-only admitted target, output declaration or native commands.
        author = service.create_task({"project": project, "capability_id": record.id,
            "capability_digest": record.capability_digest, "input_object_ids": [],
            "idempotency_key": "assembly", "spec": {"runtime_dependencies": {
                "edges": [{"from_task_id": child, "to": "self", "requires_event": "task.succeeded",
                           "fence": "runtime_task"} for child in children],
                "aggregation": {"kind": "ordered_cas_inputs"},
                "publication": {"timeline_id": "main", "expected_version": 1, "render": {
                    "capability_id": "rendering.render", "capability_digest": render_record.capability_digest,
                    "spec": {"capability_id": "rendering.render", "kind": "executor",
                             "inputs": {}, "outputs": {}}}}}}})["task"]["id"]
        claim = asdict(client.claim_next(executor_id=client.executor_id,
            capability_ids=[record.id], idempotency_key="claim-assembly"))
        assert claim["task_id"] == author
        task = {**service.task(author)["task"], "project_id": project,
                "run_id": claim["run_id"], "runtime_epoch": claim["runtime_epoch"]}
        calls = []

        def observe(name):
            operation = getattr(client, name)

            def delegated(*args, **kwargs):
                calls.append(name)
                return operation(*args, **kwargs)

            monkeypatch.setattr(client, name, delegated)

        for name in ("publish_timeline_render", "upload_object", "settle"):
            observe(name)
        failure = None
        try:
            host.run_task({"task": task}, lease_token=claim["lease_id"],
                          attempt_id=claim["attempt_id"], fence=claim["fence"], keep_attempt=True)
        except RuntimeError as exc:
            failure = exc
        proposal = json.loads((attempt_root / "outputs/authoring-proposal.json").read_text())
        materialized = json.loads((attempt_root / "inputs/resolved-children.json").read_text())
        assert [child["task_id"] for child in proposal["children"]] == children
        assert len({row["id"] for row in proposal["timeline"]["clips"]}) == 2
        assert len({row["asset"] for row in proposal["timeline"]["clips"]}) == 2
        assert proposal["timeline"]["clips"][1]["at"] == 1.0
        if failure is not None:
            # Only this observed live preservation defect is expected to fail;
            # fixture, preflight, transport and action failures remain failures.
            assert calls == ["publish_timeline_render"], (calls, repr(failure))
            assert "timeline document not found" in str(failure), repr(failure)
            raise UnsettledRegisteredAssembly(json.dumps({
                "failure": str(failure), "calls": calls,
                "immutable_spec": task["spec"], "materialized": materialized,
                "proposal_keys": sorted(proposal), "original_target": original_target,
                "task_state": service.task(author)["task"]["status"],
                "managed_outputs": service.managed_outputs(author),
            }, sort_keys=True))
        settled = service.task(author)["task"]
        assert settled["status"] == "completed"
        output = next(row for row in settled["result"]["outputs"] if row["name"] == "authoring_proposal")
        raw = service.object(output["digest"])[1]
        assert json.loads(raw) == proposal
    finally:
        host.shutdown()
        daemon.stop()
