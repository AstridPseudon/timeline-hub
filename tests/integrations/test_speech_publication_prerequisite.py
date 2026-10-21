"""Root speech publication proof against the pinned Runtime source."""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest


RUNTIME_COMMIT = "c3d26567ff6fe4e20a959476d40aff90ad23a0ca"
RUNTIME_TREE = Path(
    os.environ.get("ASTRID_NORMAL_RUNTIME_SOURCE")
    or os.environ.get("ASTRID_RUNTIME_CHECKOUT")
    or "/home/user/work/wt/rt-pin-c3d26567"
).resolve()
os.environ["ASTRID_RUNTIME_CHECKOUT"] = str(RUNTIME_TREE)
sys.path.insert(0, str(RUNTIME_TREE))

from astrid.core.execution.generic_host import (  # noqa: E402
    GenericPackHost,
    RuntimeProtocolClient,
)
from astrid.sdk.invocation import invoke  # noqa: E402
from astrid.sdk.remote import RemoteAstridClient  # noqa: E402
from astrid.sdk.workspace_client import WorkspaceClient  # noqa: E402
from runtime_protocol.daemon import WORKER_ACTOR  # noqa: E402


pytestmark = pytest.mark.integration


def _wav_bytes() -> bytes:
    stream = io.BytesIO()
    with wave.open(stream, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(8000)
        output.writeframes(b"\0\0" * 8000)
    return stream.getvalue()


def _fixture_pack(root: Path) -> Path:
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
import wave
from pathlib import Path
import sys

out = Path(sys.argv[1])
out.joinpath("audio").mkdir(parents=True, exist_ok=True)
wav_path = out / "audio" / "speech.wav"
with wave.open(str(wav_path), "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(8000)
    wav.writeframes(b"\\0\\0" * 8000)
audio_hash = hashlib.sha256(wav_path.read_bytes()).hexdigest()
manifest_path = out / "speech-provenance.json"
manifest_path.write_text(json.dumps({
    "text": sys.argv[2],
    "audio_sha256": audio_hash,
    "duration_seconds": 1.0,
}, sort_keys=True), encoding="utf-8")
(out / "manifest.json").write_text(json.dumps({
    "schema_version": 1,
    "outputs": [
        {"name": "speech", "path": "audio/speech.wav", "type": "file",
         "artifact_type": "audio", "ordinal": 0, "role": "result",
         "is_primary": True, "content_hash": "sha256:" + audio_hash,
         "bytes": wav_path.stat().st_size, "media_type": "audio/wav"},
        {"name": "speech_manifest", "path": "speech-provenance.json", "type": "file",
         "ordinal": 1, "role": "auxiliary", "is_primary": False,
         "content_hash": "sha256:" + hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
         "bytes": manifest_path.stat().st_size, "media_type": "application/json"},
    ],
}, sort_keys=True), encoding="utf-8")
"""
    (executor / "executor.yaml").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "id": "generation.generate_speech",
                "name": "Speech fixture",
                "kind": "external",
                "version": "1.0",
                "inputs": [
                    {"name": "task_spec_json", "type": "string", "required": True},
                    {"name": "text", "type": "string", "required": True},
                ],
                "command": {"argv": ["{python_exec}", "-c", script, "{out}", "{text}"]},
                "outputs": [
                    {"name": "speech", "type": "file", "path_template": "{out}/audio/speech.wav", "artifact_type": "audio"},
                    {"name": "speech_manifest", "type": "file", "path_template": "{out}/speech-provenance.json", "artifact_type": "application/json"},
                ],
                "isolation": {"mode": "subprocess", "network": False},
                "metadata": {
                    "resource_keys": [],
                    "estimated_scratch_bytes": 1024,
                    "estimated_output_bytes": 65536,
                    "generation_publication": {
                        "version": 1,
                        "modality": "audio",
                        "output_port": "speech",
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    return pack


def test_sdk_speech_admission_settles_fixture_wav_and_reads_exact_selection(
    tmp_path: Path, real_runtime
) -> None:
    """Normal SDK admission reaches an authorized host and exact media reads."""
    assert RUNTIME_TREE.joinpath("runtime_protocol").is_dir()
    runtime_head = subprocess.run(
        ["git", "-C", str(RUNTIME_TREE), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert runtime_head == RUNTIME_COMMIT

    daemon = real_runtime(commit=RUNTIME_COMMIT)
    transport = WorkspaceClient(daemon.endpoint, daemon.token)
    transport.handshake(
        "speech-prerequisite-writer",
        "1",
        ["projects:read", "projects:write", "tasks:read", "tasks:write", "objects:read", "objects:write"],
    )
    remote = RemoteAstridClient(transport)
    project_result = remote.projects.create(
        slug="speech-prerequisite", name="Speech prerequisite", idempotency_key="speech-project"
    )
    assert project_result.ok, project_result.error
    project_id = project_result.data.get("project_id") or project_result.data["id"]

    worker = RuntimeProtocolClient(daemon.endpoint, daemon.worker_token)
    host = GenericPackHost(
        pack_roots=[_fixture_pack(tmp_path)],
        client=worker,
        executor_id=WORKER_ACTOR,
        attempt_root=tmp_path / "attempts",
    )
    host.discover()
    host.preflight("generation.generate_speech")
    host.register()
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(host.run, once=False, poll_seconds=0.02, max_tasks=1)
            result = invoke(
                "generation.generate_speech",
                kind="executor",
                project=project_id,
                inputs={
                    "text": "A genuine fixture speech task.",
                    "generation_intent": {
                        "version": 1,
                        "modality": "audio",
                        "partial_success_policy": "reject",
                        "groups": [{
                            "group_key": "main",
                            "selectors": [{
                                "selector": "main-0",
                                "ordinal": 0,
                                "variant_key": "original",
                                "required": True,
                            }],
                        }],
                        "metadata": {
                            "params": {
                                "media_type": "audio/wav",
                                "duration_seconds": 1.0,
                            },
                        },
                    },
                },
                client=remote,
                wait=True,
            )
            future.result(timeout=30)

        assert result.ok, result.error
        assert result.kernel_task_id and result.kernel_attempt_id
        task = transport.get_task(result.kernel_task_id)
        assert task["generation_intent"] == {
            "version": 1,
            "modality": "audio",
            "partial_success_policy": "reject",
            "groups": [{
                "group_key": "main",
                "selectors": [{
                    "selector": "main-0",
                    "ordinal": 0,
                    "variant_key": "original",
                    "required": True,
                }],
            }],
            "metadata": {
                "params": {
                    "media_type": "audio/wav",
                    "duration_seconds": 1.0,
                },
            },
        }
        assert task["expected_effect"]["effect_type"] == "generation.publish_v1"
        assert task["expected_effect"]["target_id"] == project_id
        assert task["expected_effect"]["payload"]["groups"][0]["selectors"][0]["output_port"] == "speech"

        managed, next_cursor = transport.list_managed_outputs(result.kernel_task_id)
        assert next_cursor is None
        speech_outputs = [item for item in managed if item["output_port"] == "speech"]
        assert len(speech_outputs) == 1
        association = speech_outputs[0]
        wav = _wav_bytes()
        assert association["object_id"] == "sha256:" + hashlib.sha256(wav).hexdigest()

        reader_token, _ = daemon.credentials.provision(
            "speech-prerequisite-reader", ["handshake", "projects:read"]
        )
        reader = WorkspaceClient(daemon.endpoint, reader_token)
        reader.handshake("speech-prerequisite-reader", "1", ["projects:read"])
        selection = reader.get_project_media_selection(project_id, {
            "association_id": association["association_id"],
            "object_id": association["object_id"],
            "version": association["lifecycle"]["version"],
        })
        assert set(selection) == {"asset", "generation_id", "variant_id", "object_id", "catalog_digest"}
        assert selection["object_id"] == association["object_id"]
        verified = reader.get_project_verified_media(project_id, selection)
        assert verified == {
            "selection": selection,
            "media_type": "audio/wav",
            "size": len(wav),
            "duration_seconds": 1.0,
        }
    finally:
        host.shutdown()
