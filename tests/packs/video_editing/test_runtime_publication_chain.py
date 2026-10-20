from __future__ import annotations

import base64
import hashlib
import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import GenericPackHost, HostError, RuntimeProtocolClient
from astrid.core.contracts.runtime_orchestration import OrchestrationContractError
from astrid.packs.rendering.actions.assemble_timeline.run import build_authoring_proposal
from astrid.packs.rendering.shared.runtime_stitch import publish_authoring_proposal
from astrid.sdk.client import AstridClient
from astrid.sdk.timeline.assembly import read_assembly_proposal
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.helpers.runtime import use_runtime


def _digest(value: str | bytes) -> str:
    raw = value.encode() if isinstance(value, str) else value
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _claim_child(service, capability: str, *, key: str) -> dict:
    epoch = service.health()["runtime_epoch"]
    claim = service.claim_next(
        {"executor_id": "chain-worker", "capability_ids": [capability], "runtime_epoch": epoch},
        idempotency_key=key,
    )
    row = service.store.conn.execute("SELECT * FROM attempts WHERE task_id=?", (claim["task_id"],)).fetchone()
    return {"task_id": claim["task_id"], "attempt_id": row["id"], "lease_id": row["lease_id"], "fence": row["fence"], "runtime_epoch": row["runtime_epoch"]}


def _settle_child(service, attempt: dict, *, index: int, value: bytes, digest: str) -> dict:
    service.settle_attempt(
        attempt["attempt_id"],
        {
            "attempt_id": attempt["attempt_id"],
            "lease_id": attempt["lease_id"],
            "fence": attempt["fence"],
            "runtime_epoch": attempt["runtime_epoch"],
            "outputs": [{
                "digest": digest,
                "data_base64": base64.b64encode(value).decode(),
                "media_type": "video/mp4",
                "name": f"child-{index}",
                "role": "primary",
                "is_primary": True,
                "duration_seconds": 1.0,
            }],
        },
        idempotency_key=f"chain-settle-{index}",
    )
    return {"task_id": attempt["task_id"], "digest": digest}


def _media_effect(project_id: str) -> dict:
    return {
        "effect_type": "generation.publish_v1",
        "target_id": project_id,
        "payload": {
            "version": 1,
            "modality": "video",
            "generation_type": "multi_output_render",
            "metadata": {"params": {"duration_seconds": 1.0, "width": 64, "height": 36}},
            "partial_success_policy": "reject",
            "groups": [{"group_key": "main", "selectors": [{
                "selector": "primary", "ordinal": 0, "variant_key": "primary", "output_port": "video",
            }]}],
        },
    }


@pytest.mark.integration
def test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task(tmp_path, real_runtime):
    """Exercise child settlement -> authoring -> fenced publication -> render admission."""
    daemon = real_runtime(authoring_profile="astrid")
    service = daemon.service
    try:
        project = service.create_project({"slug": "chain", "name": "Chain"})
        child_cap, author_cap, render_cap = "video.child", "rendering.assemble_timeline", "rendering.render"
        digests = {cap: _digest(cap) for cap in (child_cap, author_cap, render_cap)}
        for capability, digest in digests.items():
            service.register_capability({"capability_id": capability, "definition_digest": digest, "status": "ready"})
        service.register_executor(
            {"executor_id": "chain-worker", "capabilities": [child_cap, author_cap, render_cap], "max_concurrency": 4},
            idempotency_key="chain-register",
        )
        service.create_timeline(project["id"], "main", name="Main", idempotency_key="chain-timeline")
        client = AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=service.realm["id"], actor_id="owner", client_name="astrid-chain-test",
            client_version="stage1", protocol_version="workspace.v1",
        )
        child_ids = []
        for index in range(2):
            task = service.create_task({
                "project": project["id"], "capability_id": child_cap, "capability_digest": digests[child_cap],
                "input_object_ids": [], "spec": {"index": index}, "idempotency_key": f"chain-child-{index}",
            })
            child_ids.append(task["task"]["id"])
        service.create_task({
            "project": project["id"], "capability_id": author_cap, "capability_digest": digests[author_cap],
            "input_object_ids": [], "idempotency_key": "chain-author",
            "spec": {"runtime_dependencies": {"edges": [
                {"from_task_id": task_id, "to": "self", "requires_event": "task.succeeded", "fence": "runtime_task"}
                for task_id in child_ids
            ], "aggregation": {"kind": "ordered_cas_inputs", "order": []}}},
        })
        outputs = [_digest(b"child-zero"), _digest(b"child-one")]
        claims = [_claim_child(service, child_cap, key=f"chain-claim-child-{index}") for index in range(2)]
        assert {claim["task_id"] for claim in claims} == set(child_ids)
        by_task = {claim["task_id"]: claim for claim in claims}
        # Deliberately settle ordinal 1 before ordinal 0; claim order is
        # runtime-owned and may differ from admission order.
        _settle_child(service, by_task[child_ids[1]], index=1, value=b"child-one", digest=outputs[1])
        _settle_child(service, by_task[child_ids[0]], index=0, value=b"child-zero", digest=outputs[0])

        author_claim = service.claim_next(
            {"executor_id": "chain-worker", "capability_ids": [author_cap], "runtime_epoch": service.health()["runtime_epoch"]},
            idempotency_key="chain-claim-author",
        )
        author_row = service.store.conn.execute("SELECT * FROM attempts WHERE task_id=?", (author_claim["task_id"],)).fetchone()
        runtime_attempt = {"attempt_id": author_row["id"], "lease_id": author_row["lease_id"], "fence": author_row["fence"], "runtime_epoch": author_row["runtime_epoch"]}
        author_task = service.task(author_claim["task_id"])["task"]
        # Feed the exact Runtime claim envelope into the authoring executor;
        # no enriched test-only descriptors are inserted here.
        proposal = build_authoring_proposal({
            "task_id": author_task["id"],
            "capability_id": author_task["capability"],
            "input_object_ids": author_task["spec"]["input_object_ids"],
            "spec": author_task["spec"],
        })
        with pytest.raises(OrchestrationContractError, match="authoring task publication target is unavailable"):
            publish_authoring_proposal(
                client, proposal=proposal, timeline_id="main", expected_version=1,
                runtime_attempt=runtime_attempt, render_capability_digest=digests[render_cap],
                output_name="chain.mp4", idempotency_key="chain-publish",
            )
        assert service.store.conn.execute("SELECT COUNT(*) FROM tasks WHERE capability=?", (render_cap,)).fetchone()[0] == 0
    finally:
        daemon.stop()


def test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts(tmp_path):
    """Unsafe legacy admission is visible, terminal, and leaves its artifact untouched."""
    proposal_path = tmp_path / "attempt" / "outputs" / "authoring-proposal.json"
    proposal_path.parent.mkdir(parents=True)
    original = json.dumps({
        "timeline": {"tracks": [], "clips": []}, "registry": {"assets": {}},
        "publication": {"authority": "workspace_runtime", "render_capability": "rendering.render"},
    }).encode()
    proposal_path.write_bytes(original)

    class Runtime:
        def __init__(self): self.calls = []
        def fail(self, *args, **kwargs): self.calls.append((args, kwargs))
        def heartbeat(self, *args, **kwargs): self.calls.append((args, kwargs))
        def task(self, *args, **kwargs): self.calls.append((args, kwargs))
        def settle(self, *args, **kwargs): self.calls.append((args, kwargs))
        def upload_object(self, *args, **kwargs): self.calls.append((args, kwargs))

    runtime = Runtime()
    host = GenericPackHost(pack_roots=[], client=runtime, attempt_root=tmp_path / "host-attempt")
    host.capabilities = {
        "rendering.assemble_timeline": SimpleNamespace(
            ready=True,
            definition=SimpleNamespace(metadata={}),
            matrix={},
        )
    }
    host.preflight = lambda _capability: None
    host._registration_admission_reason = lambda: None
    task = {
        "id": "author-1",
        "capability": "rendering.assemble_timeline",
        "spec": {"runtime_dependencies": {"publication": {"timeline_id": "main"}}},
        "input_object_ids": [],
        "project_id": "project-1",
        "attempt_id": "attempt-1",
        "fence": 1,
        "runtime_epoch": 1,
    }
    try:
        with pytest.raises(HostError, match="immutable original target"):
            host.run_task(task, lease_token="lease-1", attempt_id="attempt-1", fence=1)
    finally:
        host.shutdown()
    assert proposal_path.read_bytes() == original
    assert len(runtime.calls) == 1
    args, kwargs = runtime.calls[0]
    assert args[:2] == ("author-1", "lease-1")
    assert kwargs["runtime_epoch"] == 1
    assert not any(name in repr(runtime.calls) for name in ("publish_timeline_render", "save", "invoke"))


@pytest.mark.integration
def test_daemon_backed_host_executes_authoring_and_final_render(tmp_path, monkeypatch, real_runtime):
    """Run registered native assembly through requester, host, Runtime, and render."""
    use_runtime()
    astrid_root = Path(__file__).resolve().parents[3]
    # The named integration suite supplies the pinned current Remotion/runtime
    # pair. Keep this bootstrap read-only and do not redirect it to a mutable
    # checkout-local renderer.
    assert os.environ.get("ASTRID_REMOTION_PROJECT_DIR")
    assert os.environ.get("ASTRID_NODE_EXECUTABLE")
    assert os.environ.get("ASTRID_TIMELINE_SCHEMA_PYTHONPATH")
    from astrid.core.rendering.remotion_runtime import prepare_remotion_validation

    # The central runner's loopback proxy presents a self-signed certificate
    # to Remotion's usage beacon. Inject its CA only through this private
    # wrapper around the pinned Node executable, so host admission still sees
    # the same registered runtime and no shared environment is changed.
    pinned_node = Path(os.environ["ASTRID_NODE_EXECUTABLE"]).resolve()
    ca_bundle = Path("/root/.ccr/ca-bundle.crt")
    assert ca_bundle.is_file()
    trusted_node = tmp_path / "node-current-with-runner-ca"
    trusted_node.write_text(
        "#!/bin/sh\n"
        f"export NODE_EXTRA_CA_CERTS={shlex.quote(str(ca_bundle))}\n"
        f"exec {shlex.quote(str(pinned_node))} \"$@\"\n",
        encoding="utf-8",
    )
    trusted_node.chmod(0o755)
    monkeypatch.setenv("ASTRID_NODE_EXECUTABLE", str(trusted_node))
    pinned_remotion = Path(os.environ["ASTRID_REMOTION_PROJECT_DIR"]).resolve()
    private_remotion = tmp_path / "remotion-current"
    shutil.copytree(
        pinned_remotion, private_remotion, symlinks=True,
        ignore=shutil.ignore_patterns(".git"),
    )
    (tmp_path / "astrid").symlink_to(astrid_root / "astrid", target_is_directory=True)
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(private_remotion))
    validation = prepare_remotion_validation(
        artifact_directory=tmp_path / "remotion-validation",
        host_environment=dict(os.environ),
        python_executable=os.sys.executable,
        launch_id=hashlib.sha256(str(tmp_path).encode()).hexdigest()[:32],
        contexts={"host": dict(os.environ), "worker": [dict(os.environ)]},
    )
    for name, value in validation.items():
        monkeypatch.setenv(name, value)
    daemon = real_runtime(authoring_profile="astrid")
    service = daemon.service
    client = None
    host = GenericPackHost(
        pack_roots=[astrid_root / "astrid/packs/rendering"],
        client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
        executor_id="astrid-pack-host",
        attempt_root=tmp_path / "attempt",
    )
    try:
        host.discover()
        host.preflight("rendering.assemble_timeline")
        host.preflight("rendering.render")
        assemble_digest = host.capabilities["rendering.assemble_timeline"].capability_digest
        render_digest = host.capabilities["rendering.render"].capability_digest
        child_capability = "video.child"
        child_digest = _digest(child_capability)
        project = service.create_project({"slug": "host-chain", "name": "Host chain"})
        for capability, digest in (
            (child_capability, child_digest),
            ("rendering.assemble_timeline", assemble_digest),
            ("rendering.render", render_digest),
        ):
            service.register_capability(
                {"capability_id": capability, "definition_digest": digest, "status": "ready"}
            )
        service.register_executor(
            {
                "executor_id": "astrid-pack-host",
                "capabilities": [child_capability, "rendering.assemble_timeline", "rendering.render"],
                "max_concurrency": 3,
            },
            idempotency_key="host-chain-register",
        )
        client = AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=service.realm["id"], actor_id="owner", client_name="astrid-chain-test",
            client_version="stage1", protocol_version="workspace.v1",
        )
        service.create_timeline(project["id"], "main", name="Main", idempotency_key="host-chain-timeline")
        blobs = []
        for index, colour in enumerate(("blue", "red")):
            path = tmp_path / f"child-{index}.mp4"
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", f"color=c={colour}:s=64x36:r=30:d=1", "-an", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", str(path),
                ],
                check=True,
                capture_output=True,
            )
            blobs.append(path.read_bytes())
        child_ids = []
        for index in range(2):
            child_ids.append(
                service.create_task(
                    {
                        "project": project["id"],
                        "capability_id": child_capability,
                        "capability_digest": child_digest,
                        "input_object_ids": [],
                        "spec": {"index": index},
                        "settlement_effect": _media_effect(project["id"]),
                        "idempotency_key": f"host-chain-child-{index}",
                    }
                )["task"]["id"]
            )
        claims = []
        for index in range(2):
            claim = service.claim_next(
                {
                    "executor_id": "astrid-pack-host",
                    "capability_ids": [child_capability],
                    "runtime_epoch": service.health()["runtime_epoch"],
                },
                idempotency_key=f"host-chain-claim-child-{index}",
            )
            claims.append(claim)
        by_task = {claim["task_id"]: claim for claim in claims}
        assert set(by_task) == set(child_ids)
        # Finish ordinal 1 first; Runtime still resolves the declared order.
        for index in (1, 0):
            claim = by_task[child_ids[index]]
            service.settle_attempt(
                claim["attempt_id"],
                {
                    "attempt_id": claim["attempt_id"],
                    "lease_id": claim["lease_id"],
                    "fence": claim["fence"],
                    "runtime_epoch": claim["runtime_epoch"],
                    "outputs": [{
                        "digest": _digest(blobs[index]),
                        "data_base64": base64.b64encode(blobs[index]).decode(),
                        "media_type": "video/mp4",
                        "name": f"child-{index}",
                        "output_port": "video",
                        "group_key": "main",
                        "variant_key": "primary",
                        "ordinal": 0,
                        "role": "primary",
                        "is_primary": True,
                        "duration_seconds": 1.0,
                    }],
                    "effect": _media_effect(project["id"]),
                },
                idempotency_key=f"host-chain-settle-child-{index}",
            )
        selectors = []
        for child_id in child_ids:
            associations = service.managed_outputs(child_id)
            association = next(row for row in associations if row["output_port"] == "video")
            selectors.append({
                "association_id": association["association_id"],
                "object_id": association["object_id"],
                "version": association["lifecycle"]["version"],
            })
        session = TimelineSession.open(
            project["id"], "main", client=client, outbox_path=tmp_path / "host-chain-outbox.json",
        )
        admission = session.admit_assembly(
            selectors, replace_clips=[], assembler_digest=assemble_digest,
            idempotency_key="host-chain-author",
        )
        author = admission["data"]["task_id"]
        author_claim = host.client.claim_next(
            executor_id="astrid-pack-host",
            capability_ids=["rendering.assemble_timeline"],
            idempotency_key="host-chain-claim-author",
        )
        host.run_task(
            {
                "task": {
                    "id": author_claim["task_id"],
                    "capability": "rendering.assemble_timeline",
                    "spec": author_claim["spec"],
                    "input_object_ids": author_claim["input_object_ids"],
                    "project_id": author_claim["project_id"],
                    "run_id": author_claim["run_id"],
                    "attempt_id": author_claim["attempt_id"],
                    "fence": author_claim["fence"],
                    "runtime_epoch": author_claim["runtime_epoch"],
                }
            },
            lease_token=author_claim["lease_id"],
            attempt_id=author_claim["attempt_id"],
            fence=author_claim["fence"],
            keep_attempt=True,
        )
        author_result = service.task(author)["task"]["result"]
        assert {item["name"] for item in author_result["outputs"]} >= {"authoring_proposal", "timeline", "assets"}
        settled = read_assembly_proposal(session, author, attempt_id=author_claim["attempt_id"])
        assert [command["op"] for command in settled["commands"][:3]] == [
            "timeline.assembled-target", "track.create", "clip.add-media",
        ]
        assert [command["args"]["media"]["object_id"] for command in settled["commands"] if command["op"] == "clip.add-media"] == [
            selector["object_id"] for selector in selectors
        ]
        session.queue_assembly(author, attempt_id=author_claim["attempt_id"])
        pending = json.loads((tmp_path / "host-chain-outbox.json").read_text())
        assert pending["pending"][0]["op"] == "producer.guard"
        original_commit = client.timelines.commit

        def lose_ack(*args, **kwargs):
            original_commit(*args, **kwargs)
            raise WorkspaceClientError(0, "transport_error", "lost commit acknowledgement")

        client.timelines.commit = lose_ack
        with pytest.raises(WorkspaceClientError, match="lost commit acknowledgement"):
            session.flush(idempotency_key="host-chain-commit")
        saved_flight = json.loads((tmp_path / "host-chain-outbox.json").read_text())["flight"]
        assert saved_flight["key"] == "host-chain-commit"
        client.timelines.commit = original_commit
        restarted = TimelineSession.open(
            project["id"], "main", client=client, outbox_path=tmp_path / "host-chain-outbox.json",
        )
        committed = restarted.flush(idempotency_key="host-chain-commit")
        accepted_revision = committed["data"]["accepted_revision_id"]
        accepted_publication = committed["data"]["accepted_publication_id"]
        assert accepted_revision and accepted_publication
        assert json.loads((tmp_path / "host-chain-outbox.json").read_text())["flight"] is None

        scope = client.timelines.resolve_scope(project["id"], "main")
        assert scope.ok and isinstance(scope.data.get("version"), int)
        render_admission = client.invoke_result(
            "rendering.render", kind="executor", project=project["id"],
            inputs={"timeline_ref": "main", "expected_version": scope.data["version"], "output_name": "host-chain.mp4"},
            wait=False,
        )
        assert render_admission.ok
        render_task_id = render_admission.kernel_task_id
        assert isinstance(render_task_id, str) and render_task_id
        render_claim = host.client.claim_next(
            executor_id="astrid-pack-host",
            capability_ids=["rendering.render"],
            idempotency_key="host-chain-claim-render",
        )
        host.run_task(
            {
                "task": {
                    "id": render_claim["task_id"],
                    "capability": "rendering.render",
                    "spec": render_claim["spec"],
                    "input_object_ids": render_claim["input_object_ids"],
                    "project_id": render_claim["project_id"],
                    "run_id": render_claim["run_id"],
                    "attempt_id": render_claim["attempt_id"],
                    "fence": render_claim["fence"],
                    "runtime_epoch": render_claim["runtime_epoch"],
                }
            },
            lease_token=render_claim["lease_id"],
            attempt_id=render_claim["attempt_id"],
            fence=render_claim["fence"],
            keep_attempt=True,
        )
        render_result = service.task(render_task_id)["task"]["result"]
        assert {item["name"] for item in render_result["outputs"]} >= {"video", "provenance"}
        video = next(item for item in render_result["outputs"] if item["name"] == "video")
        _, video_bytes = service.object(video["digest"])
        assert len(video_bytes) > 100
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", "-"],
            input=video_bytes,
            capture_output=True,
        )
        assert probe.returncode == 0
        assert float(probe.stdout.strip()) > 0
        render_task = service.task(render_task_id)["task"]
        assert render_task["spec"]["spec"]["inputs"]["timeline_authority"]["parent_revision_id"] == accepted_revision
        undone = restarted.undo([accepted_publication], idempotency_key="host-chain-undo")
        assert undone["data"]["accepted_revision_id"]
    finally:
        host.shutdown()
        daemon.stop()
