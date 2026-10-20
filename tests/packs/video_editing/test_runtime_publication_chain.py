from __future__ import annotations

import base64
import hashlib
import io
import json
import shutil
import subprocess
import sys
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.packs.rendering.actions.assemble_timeline.run import build_authoring_proposal
from astrid.packs.rendering.shared.runtime_stitch import publish_authoring_proposal
from astrid.sdk.client import AstridClient
from astrid.sdk.remote import RemoteAstridClient
from astrid.sdk.workspace_client import WorkspaceClient


SPEECH_RUNTIME_COMMIT = "ad97e16effc53fa13f91c43f076f6edb3c38985f"


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


@pytest.mark.integration
def test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task(tmp_path, real_runtime):
    """Exercise child settlement -> authoring -> fenced publication -> render admission."""
    daemon = real_runtime()
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
        service.create_timeline_document(
            project["id"], {"timeline_id": "main", "slug": "main", "name": "Main", "config": {}, "registry": {}},
            idempotency_key="chain-timeline",
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
        client = AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=service.realm["id"], actor_id="owner", client_name="astrid-chain-test",
            client_version="stage1", protocol_version="workspace.v1",
        )
        result = publish_authoring_proposal(
            client, proposal=proposal, timeline_id="main", expected_version=1,
            runtime_attempt=runtime_attempt, render_capability_digest=digests[render_cap],
            output_name="chain.mp4", idempotency_key="chain-publish",
        )
        assert result["timeline_version"] == 2
        assert service.store.conn.execute("SELECT COUNT(*) FROM tasks WHERE capability=?", (render_cap,)).fetchone()[0] == 1
        render = service.task(result["render_task_id"])["task"]
        assert render["spec"]["spec"]["inputs"]["timeline_snapshot"]["config"] == proposal["timeline"]
        assert render["spec"]["spec"]["inputs"]["expected_version"] == 2
        # The checkpoint admits the ordinary public renderer; the next worker
        # claim therefore sees rendering.render without a stitch-specific task.
        render_claim = service.claim_next(
            {"executor_id": "chain-worker", "capability_ids": [render_cap], "runtime_epoch": service.health()["runtime_epoch"]},
            idempotency_key="chain-claim-render",
        )
        assert render_claim["task_id"] == result["render_task_id"]
    finally:
        daemon.stop()


def test_generic_host_hook_materializes_and_publishes_without_local_save_or_invoke(tmp_path):
    """The registered authoring host hook has one Runtime publication route."""
    proposal_path = tmp_path / "attempt" / "outputs" / "authoring-proposal.json"
    proposal_path.parent.mkdir(parents=True)
    proposal_path.write_text(json.dumps({
        "timeline": {"tracks": [], "clips": []}, "registry": {"assets": {}},
        "publication": {"authority": "workspace_runtime", "render_capability": "rendering.render"},
    }))

    class Runtime:
        def __init__(self): self.calls = []
        def publish_timeline_render(self, *args, **kwargs):
            self.calls.append((args, kwargs))
            return {"timeline_version": 2, "render_task_id": "render-1"}

    runtime = Runtime()
    host = GenericPackHost.__new__(GenericPackHost)
    host.client = runtime
    host.capabilities = {}
    result = host._publish_assembled_timeline(
        task_data={"id": "author-1", "spec": {"family": "stitch_finalization", "runtime_dependencies": {
            "publication": {"timeline_id": "main", "expected_version": 1, "render": {
                "capability_id": "rendering.render", "capability_digest": _digest("rendering.render"),
                "spec": {"inputs": {"selector": "rendering.ffmpeg"}},
            }},
        }}},
        attempt_id="attempt-1", fence=1, lease_token="lease-1",
        outputs=[{"path": str(proposal_path), "artifact_type": "timeline/authoring-proposal"}],
        attempt_root=proposal_path.parents[1],
    )
    assert result["render_task_id"] == "render-1"
    assert len(runtime.calls) == 1
    args, kwargs = runtime.calls[0]
    assert args[:2] == ("attempt-1", "lease-1")
    assert kwargs["timeline_id"] == "main"
    assert kwargs["expected_version"] == 1
    assert "save" not in repr(runtime.calls) and "invoke" not in repr(runtime.calls)


@pytest.mark.integration
def test_daemon_backed_host_executes_authoring_and_final_render(tmp_path, monkeypatch, real_runtime):
    """Run the complete two-child continuation through the real pack host."""
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None or shutil.which("node") is None:
        pytest.skip("ffmpeg, ffprobe, and node are required for the daemon render chain")
    astrid_root = Path(__file__).resolve().parents[3]
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(astrid_root / "remotion"))
    monkeypatch.setenv("ASTRID_NODE_EXECUTABLE", shutil.which("node") or "node")
    monkeypatch.setenv(
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH",
        str(astrid_root / "remotion/node_modules/@banodoco/timeline-schema/python"),
    )
    daemon = real_runtime(production_worker_credentials=True)
    service = daemon.service
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
        service.create_timeline_document(
            project["id"],
            {"timeline_id": "main", "slug": "main", "name": "Main", "config": {}, "registry": {}},
            idempotency_key="host-chain-timeline",
        )
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
                    "outputs": [
                        {
                            "digest": _digest(blobs[index]),
                            "data_base64": base64.b64encode(blobs[index]).decode(),
                            "media_type": "video/mp4",
                            "name": f"child-{index}",
                            "role": "primary",
                            "is_primary": True,
                            "duration_seconds": 1.0,
                        }
                    ],
                },
                idempotency_key=f"host-chain-settle-child-{index}",
            )
        render_spec = {
            "capability_id": "rendering.render",
            "schema_version": "1",
            "spec": {
                "capability_id": "rendering.render",
                "kind": "executor",
                "inputs": {"selector": "rendering.ffmpeg", "output_name": "host-chain.mp4"},
                "outputs": {},
            },
        }
        author = service.create_task(
            {
                "project": project["id"],
                "capability_id": "rendering.assemble_timeline",
                "capability_digest": assemble_digest,
                "input_object_ids": [],
                "spec": {
                    "runtime_dependencies": {
                        "edges": [
                            {"from_task_id": task_id, "to": "self", "requires_event": "task.succeeded", "fence": "runtime_task"}
                            for task_id in child_ids
                        ],
                        "aggregation": {"kind": "ordered_cas_inputs", "order": []},
                        "publication": {"timeline_id": "main", "expected_version": 1, "render": render_spec},
                    }
                },
                "idempotency_key": "host-chain-author",
            }
        )["task"]["id"]
        author_claim = service.claim_next(
            {
                "executor_id": "astrid-pack-host",
                "capability_ids": ["rendering.assemble_timeline"],
                "runtime_epoch": service.health()["runtime_epoch"],
            },
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
                    "attempt_id": author_claim["attempt_id"],
                    "fence": author_claim["fence"],
                }
            },
            lease_token=author_claim["lease_id"],
            attempt_id=author_claim["attempt_id"],
            fence=author_claim["fence"],
            keep_attempt=True,
        )
        author_result = service.task(author)["task"]["result"]
        publication = author_result["timeline_render_publication"]
        render_task_id = publication["render_task_id"]
        render_claim = service.claim_next(
            {
                "executor_id": "astrid-pack-host",
                "capability_ids": ["rendering.render"],
                "runtime_epoch": service.health()["runtime_epoch"],
            },
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
                    "attempt_id": render_claim["attempt_id"],
                    "fence": render_claim["fence"],
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
    finally:
        host.shutdown()
        daemon.stop()


def _speech_fixture_pack(root: Path, *, malformed: bool) -> Path:
    """Make a deterministic speech producer that still settles through the host."""
    pack = root / "speech_fixture"
    executor = pack / "executors" / "generate_speech"
    executor.mkdir(parents=True)
    (pack / "pack.yaml").write_text(
        "schema_version: 2\n"
        "id: speech_fixture\n"
        "name: Speech fixture\n"
        "version: 1.0.0\n"
        "capabilities: [generate_speech]\n"
        "content:\n  executors: executors\n",
        encoding="utf-8",
    )
    script = """
import hashlib
import json
import sys
import wave
from pathlib import Path

out = Path(sys.argv[1])
text = sys.argv[2]
settings = {"provider": sys.argv[3], "voice": sys.argv[4], "rate": sys.argv[5],
            "volume": sys.argv[6], "pitch": sys.argv[7]}
malformed = sys.argv[8] == "1"
wav_path = out / "speech.wav"
with wave.open(str(wav_path), "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(8000)
    wav.writeframes(b"\\x00\\x00" * 8000)
audio_digest = hashlib.sha256(wav_path.read_bytes()).hexdigest()
provenance = {
    "text": text,
    "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    "settings": settings,
    "audio_sha256": None if malformed else audio_digest,
    "duration_seconds": 1.0,
}
(out / "speech-provenance.json").write_text(json.dumps(provenance, sort_keys=True), encoding="utf-8")
"""
    (executor / "executor.yaml").write_text(
        json.dumps({
            "schema_version": 1,
            "id": "generation.generate_speech",
            "name": "Speech fixture",
            "kind": "external",
            "version": "1.0",
            "inputs": [
                {"name": "task_spec_json", "type": "string", "required": True},
                {"name": "text", "type": "string", "required": True},
                {"name": "provider", "type": "string", "required": False, "default": "edge-tts"},
                {"name": "voice", "type": "string", "required": False, "default": "en-US-ChristopherNeural"},
                {"name": "rate", "type": "string", "required": False, "default": "+0%"},
                {"name": "volume", "type": "string", "required": False, "default": "+0%"},
                {"name": "pitch", "type": "string", "required": False, "default": "+0Hz"},
                {"name": "malformed", "type": "string", "required": False, "default": "1" if malformed else "0"},
            ],
            "command": {"argv": [
                "{python_exec}", "-c", script, "{out}", "{text}", "{provider}",
                "{voice}", "{rate}", "{volume}", "{pitch}", "{malformed}",
            ]},
            "outputs": [
                {"name": "speech", "type": "file", "path_template": "{out}/speech.wav", "artifact_type": "audio/wav"},
                {"name": "speech_manifest", "type": "file", "path_template": "{out}/speech-provenance.json", "artifact_type": "application/json"},
            ],
            "isolation": {"mode": "subprocess", "network": False},
            "metadata": {"resource_keys": [], "estimated_scratch_bytes": 1024, "estimated_output_bytes": 65536},
        }),
        encoding="utf-8",
    )
    return pack


def _speech_outer_fixture(project_id: str):
    candidate = {
        "project_id": project_id,
        "timeline_id": "timeline",
        "base_parent": {"revision_id": "speech-head"},
        "parent": {"clips": [{"id": "background", "at": 0, "hold": 2, "track": "picture"}], "config": {"duration": 2}},
        "placements": [{"shot_id": "shot-1", "occurrence_id": "occ-1", "placement": {"start_ms": 0}, "duration_ms": 2000}],
        "shots": {"shot-1": {"payload": {"metadata": {}}, "internal_timeline": {
            "tracks": [{"id": "picture", "kind": "visual"}],
            "clips": [{"id": "image", "asset": "image", "at": 0, "hold": 2, "track": "picture"}],
            "registry": {"assets": {}},
        }}},
    }
    scripts = {"revision_id": "speech-head", "occurrences": [
        {"occurrence_id": "occ-1", "status": "present", "text": "Hello"},
    ]}

    class Bound:
        def __init__(self):
            self.published = None

        def open(self):
            return json.loads(json.dumps(candidate))

        def validate(self, work):
            assert work["shots"]["shot-1"]["payload"]["metadata"]["draft_voiceover"]["status"] == "draft"
            return {}

        def diff(self, work):
            return {"changes": ["audio"]}

        def preview(self, work):
            return {"candidate_digest": _digest(json.dumps(work, sort_keys=True))}

        def publish(self, work, **kwargs):
            self.published = {"candidate": json.loads(json.dumps(work)), "kwargs": kwargs}
            return {"publication": {"head": "speech-published"}}

    bound = Bound()
    timelines = SimpleNamespace(
        open_composition=lambda *args, **kwargs: {"summary": {"head_revision_id": "speech-head"}},
        resolve_scope=lambda *args, **kwargs: {"project_id": project_id, "timeline_id": "timeline"},
        script=lambda *args, **kwargs: scripts,
    )
    return candidate, scripts, bound, timelines


def _run_real_speech_sync(tmp_path: Path, real_runtime, *, malformed: bool):
    from astrid.packs.video_editing.shared import draft_voiceover

    daemon = real_runtime(commit=SPEECH_RUNTIME_COMMIT)
    worker = RuntimeProtocolClient(daemon.endpoint, daemon.worker_token)
    host = GenericPackHost(
        pack_roots=[_speech_fixture_pack(tmp_path, malformed=malformed)],
        client=worker,
        executor_id="speech-fixture-host",
        attempt_root=tmp_path / "attempts",
    )
    transport = WorkspaceClient(daemon.endpoint, daemon.token)
    transport.handshake(
        "speech-publication-test",
        "1",
        ["projects:read", "projects:write", "objects:read", "objects:write", "tasks:read", "tasks:write"],
    )
    remote = RemoteAstridClient(transport)
    project_result = remote.projects.create(slug="speech-wc5", name="Speech WC5", idempotency_key="speech-wc5-project")
    assert project_result.ok, project_result.error
    project_id = project_result.data.get("project_id") or project_result.data["id"]
    _candidate, _scripts, bound, timelines = _speech_outer_fixture(project_id)
    remote.timelines = timelines
    remote.open_authoring_target = lambda target: bound
    host.discover()
    host.preflight("generation.generate_speech")
    host.register()
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(host.run, once=False, poll_seconds=0.02, max_tasks=1)
            if malformed:
                with pytest.raises(draft_voiceover.VoiceoverSyncError, match="hash verification"):
                    draft_voiceover.sync_draft_voiceover(
                        remote, project_id, "timeline", timing_policy="preserve", occurrence_ids=["occ-1"]
                    )
                assert bound.published is None
            else:
                result = draft_voiceover.sync_draft_voiceover(
                    remote, project_id, "timeline", timing_policy="preserve", occurrence_ids=["occ-1"]
                )
                assert result["published"] and bound.published is not None
                generated = result["generated"][0]
                context = generated["runtime_context"]
                assert {"task", "task_id", "attempt_id", "association_id", "managed_output", "generation_publish_v1"} <= set(context)
                assert context["task"]["task_id"] == context["task_id"]
                assert context["task"]["attempt_id"] == context["attempt_id"]
                assert context["managed_output"]["association_id"] == context["association_id"]
                assert context["generation_publish_v1"]["effect_type"] == "generation.publish_v1"
                output = context["managed_output"]
                selection = transport._generated.get_project_media_selection(project_id, {
                    "association_id": output["association_id"],
                    "object_id": output["object_id"],
                    "version": output["lifecycle"]["version"],
                })
                assert set(selection) == {"asset", "generation_id", "variant_id", "object_id", "catalog_digest"}
                assert selection["object_id"] == output["object_id"]
                verified = transport._generated.get_project_verified_media(project_id, selection)
                assert verified["selection"] == selection
                assert verified["media_type"] == "audio/wav"
                assert verified["duration_seconds"] == 1.0
                wav_bytes = remote.media.read_bytes(output["object_id"])
                with wave.open(io.BytesIO(wav_bytes), "rb") as wav:
                    assert wav.getframerate() == 8000 and wav.getnframes() == 8000
            future.result(timeout=60)
    finally:
        host.shutdown()
        daemon.stop()


@pytest.mark.integration
def test_real_speech_publication_seam_settles_wav_and_selection(tmp_path, real_runtime):
    """Outer sync -> normal SDK speech admission -> managed WAV -> five-field selection."""
    _run_real_speech_sync(tmp_path, real_runtime, malformed=False)


@pytest.mark.integration
def test_real_speech_publication_rejects_malformed_provenance(tmp_path, real_runtime):
    """A settled WAV with null provenance metadata cannot reach outer publication."""
    _run_real_speech_sync(tmp_path, real_runtime, malformed=True)
