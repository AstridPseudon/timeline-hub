"""Deferred real Runtime fixture for the WC5 outer voiceover lifecycle.

The executable selector is opt-in because this task is a source/preflight
build.  Its body deliberately uses the normal Runtime client, host admission,
claim/settle loop, and requester outbox; the default preflight never starts a
daemon, host, socket, native process, or renderer.
"""
from __future__ import annotations

import hashlib
import inspect
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pytest

RUNTIME_COMMIT = "42a7203f49bb89f299ec854cfbf2b1444e815a7c"
RUNTIME_TREE = "1f220b3d3a27e8eb061b15c944bad784c8fdb82e"
ACTION = "video_editing.sync_draft_voiceover"
SPEECH = "generation.generate_speech"
LATER_SELECTOR = (
    "tests/packs/video_editing/test_wc5_outer_runtime_fixture.py::"
    "test_wc5_real_runtime_outer_lifecycle"
)

# These are the original positive lanes.  They remain untouched: this fixture
# only supplies the missing real outer carrier around their established result.
ORIGINAL_POSITIVE_MAPPING = {
    "tests/packs/video_editing/test_draft_voiceover.py": "public/private preparation",
    "tests/editing_conformance/test_recipe_native_voiceover.py": "native lowering",
}


def _runtime_source() -> Path:
    return Path(
        os.environ.get("ASTRID_NORMAL_RUNTIME_SOURCE")
        or os.environ.get("ASTRID_RUNTIME_CHECKOUT")
        or "/home/user/work/runtime"
    ).resolve()


def _data(value: Any) -> Any:
    return value.get("data", value) if isinstance(value, dict) else getattr(value, "data", value)


def _fixture_pack(root: Path) -> Path:
    """Offline speech executor: deterministic WAV, no model or network call."""
    pack = root / "wc5_speech_fixture"
    executor = pack / "executors" / "generate_speech"
    executor.mkdir(parents=True)
    (pack / "pack.yaml").write_text(
        "schema_version: 2\n"
        "id: wc5_speech_fixture\n"
        "name: WC5 speech fixture\n"
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
                "id": SPEECH,
                "name": "WC5 speech fixture",
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


def _publish_initial_composition(client: Any, project_id: str, old_selection: dict[str, str]) -> None:
    """Seed one authoritative, text-bound audio clip through Runtime APIs."""
    transport = client._remote._transport
    shot_id = "wc5-shot"
    timeline_id = "main"
    transport.create_timeline(project_id, timeline_id, idempotency_key="wc5-timeline")
    created = transport.create_project_shot(
        project_id, {"shot_id": shot_id, "name": "WC5 opening", "metadata": {}},
        idempotency_key="wc5-shot",
    )
    assert _data(created)
    binding = transport.set_project_shot_text_binding(
        project_id,
        {"shot_id": shot_id, "kind": "voiceover_script", "text": "New narration", "expected_head": 0},
        idempotency_key="wc5-script",
    )
    binding = _data(binding)
    internal_revision_id = "wc5-internal-1"
    shot_revision_id = "wc5-shot-revision-1"
    parent_revision_id = "wc5-parent-1"
    internal = {
        "tracks": [{"id": "vo", "kind": "audio"}],
        "clips": [{
            "id": "voice-1", "track": "vo", "clipType": "media", "asset": "old-voice",
            "at": 0, "from": 0, "to": 1, "hold": 1,
        }],
        "effects": [], "audio": [], "layout": {},
        "registry": {"assets": {"old-voice": {**old_selection, "type": "audio"}}},
        "assets": [],
    }
    shot = {
        "name": "WC5 opening", "metadata": {"draft_voiceover": {
            "owner": ACTION, "status": "draft", "clip_id": "voice-1",
            "audio_media_id": old_selection["object_id"], "text": "Old narration",
            "text_digest": "sha256:" + hashlib.sha256(b"Old narration").hexdigest(),
            "settings": {"provider": "edge-tts", "voice": "en-US-ChristopherNeural",
                         "rate": "+0%", "volume": "+0%", "pitch": "+0Hz"},
        }},
        "items": [], "pools": [], "selected_variants": {}, "provenance": {},
        "generation_inputs": {}, "audio_bindings": [], "text_bindings": [binding],
        "internal_timeline_revision_id": internal_revision_id,
    }
    occurrence = {
        "occurrence_id": "occ-wc5", "shot_id": shot_id, "shot_revision_id": shot_revision_id,
        "placement": {"start_ms": 0, "track": "vo"}, "source_offset": {"start": 0, "end": 1000},
        "duration_ms": 1000, "speed": {"numerator": 1, "denominator": 1}, "track": "vo",
        "transform": {"scale": 1}, "gain": 1, "muted": False, "provenance": {},
    }
    parent = {"config": {"tracks": [{"id": "vo", "kind": "audio"}]},
              "registry": {}, "clips": [], "occurrences": [occurrence]}
    publication = {
        "project_id": project_id, "timeline_id": timeline_id, "expected_head": None,
        "parent_revision_id": parent_revision_id, "parent_composition": parent,
        "shot_revisions": [{"shot_id": shot_id, "revision_id": shot_revision_id,
                             "internal_timeline_revision_id": internal_revision_id,
                             "payload": shot, "content_digest": _digest(shot)}],
        "internal_timeline_revisions": [{"timeline_id": timeline_id,
                                          "revision_id": internal_revision_id,
                                          "payload": internal, "content_digest": _digest(internal)}],
    }
    result = transport.publish_parent_composition(
        project_id, timeline_id, publication, idempotency_key="wc5-parent",
    )
    assert _data(result).get("new_head") == parent_revision_id


def _digest(value: Any) -> str:
    from astrid.sdk.timeline.commit import _digest as digest

    return digest(value)


def test_wc5_outer_runtime_fixture_source_preflight() -> None:
    """Prove the later selector has every source prerequisite without running it."""
    source = _runtime_source()
    commit = subprocess.run(
        ["git", "-C", str(source), "show", "-s", "--format=%H %T", RUNTIME_COMMIT],
        check=True, capture_output=True, text=True,
    ).stdout.strip().split()
    assert commit == [RUNTIME_COMMIT, RUNTIME_TREE]

    from astrid.core.execution.generic_host import GenericPackHost

    host = GenericPackHost(pack_roots=[Path(__file__).resolve().parents[3] / "astrid/packs/video_editing"])
    discovered = {record.id: record for record in host.discover()}
    record = discovered[ACTION]
    assert record.definition.id == ACTION
    assert record.definition.isolation.network is False
    assert {output.name for output in record.definition.outputs} >= {"authoring_proposal", "report"}
    assert "settled_speech_input" in {item.name for item in record.definition.inputs}

    from astrid.packs.video_editing.actions.sync_draft_voiceover import run as action_run
    from astrid.packs.video_editing.shared import draft_voiceover, voiceover_requester

    action_source = inspect.getsource(action_run)
    requester_module_source = inspect.getsource(voiceover_requester)
    requester_source = inspect.getsource(voiceover_requester._requester_sync_draft_voiceover)
    shared_source = inspect.getsource(draft_voiceover._sync_draft_voiceover)
    for source_text, needles in (
        (action_source, ("_require_action_context", "_managed_read_client", "build_producer_batch")),
        (requester_source, ("client.tasks.create", "observe_task_invocation", "TimelineSession.open", "queue_proposal", "session.flush")),
        (requester_module_source, ("generation.generate_speech", "_read_authoritative_media_info")),
        (shared_source, ("_read_authoritative_media_info", "settled_speech_input")),
    ):
        assert all(needle in source_text for needle in needles)
    assert all(Path(path).is_file() for path in ORIGINAL_POSITIVE_MAPPING)
    assert LATER_SELECTOR.endswith("test_wc5_real_runtime_outer_lifecycle")


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("ASTRID_RUN_WC5_OUTER") != "1",
    reason="source/preflight build; set ASTRID_RUN_WC5_OUTER=1 for the authorized real-runtime run",
)
def test_wc5_real_runtime_outer_lifecycle(tmp_path: Path, real_runtime) -> None:
    """Run the one real WC5 outer lifecycle when explicitly enabled."""
    from runtime_protocol.daemon import WORKER_ACTOR

    from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
    from astrid.packs.video_editing.shared import draft_voiceover
    from astrid.packs.video_editing.shared.draft_voiceover import _read_authoritative_media_info
    from astrid.sdk import AstridClient
    from astrid.sdk.invocation import invoke

    daemon = real_runtime(commit=RUNTIME_COMMIT)
    client = AstridClient.open(
        endpoint=daemon.endpoint, credential=daemon.credential_path,
        realm_id=daemon.service.realm["id"], actor_id="owner",
        client_name="wc5-outer-fixture", client_version="test", protocol_version="workspace.v1",
    )
    transport = client._remote._transport
    project = _data(transport.create_project(
        "WC5 outer fixture", slug="wc5-outer-fixture", idempotency_key="wc5-project",
    ))
    project_id = str(project.get("project_id") or project["id"])
    speech_host = GenericPackHost(
        pack_roots=[_fixture_pack(tmp_path)], client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
        executor_id=WORKER_ACTOR, attempt_root=tmp_path / "speech-attempts",
    )
    outer_host = GenericPackHost(
        pack_roots=[Path(__file__).resolve().parents[3] / "astrid/packs/video_editing"],
        client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
        executor_id="wc5-outer-worker", attempt_root=tmp_path / "outer-attempts",
    )
    for host, capability in ((speech_host, SPEECH), (outer_host, ACTION)):
        host.discover()
        host.preflight(capability)
        host.register()
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            speech_loop = pool.submit(speech_host.run, once=False, poll_seconds=0.02, max_tasks=2)
            old = invoke(
                SPEECH, kind="executor", project=project_id,
                inputs={"text": "Old narration"}, client=client, wait=True,
                idempotency_key="wc5-old-speech",
            )
            assert old.ok, old.error
            old_output = old.output_rows("speech")
            assert len(old_output) == 1
            old_selection, _ = _read_authoritative_media_info(client, project_id, old_output[0])
            _publish_initial_composition(client, project_id, old_selection)

            outer_loop = pool.submit(outer_host.run, once=False, poll_seconds=0.02, max_tasks=1)
            result = draft_voiceover._sync_draft_voiceover(
                client, project_id, "main", timing_policy="ripple", requester_entry=True,
                outbox_path=tmp_path / "outbox.json",
            )
            speech_loop.result(timeout=30)
            outer_loop.result(timeout=30)

        assert result["status"] == "published" and result["published"] is True
        assert result["acceptance"]
        proposal = result["proposal"]
        assert set(proposal["admitted_target"]) == {"project_id", "timeline_id", "base_revision_id", "base_publication_id"}
        base_revision_id = proposal["admitted_target"]["base_revision_id"]
        admission = _data(result["admission"])
        task_id = admission.get("task_id") or admission.get("id")
        assert isinstance(task_id, str) and task_id
        managed, cursor = transport.list_managed_outputs(task_id)
        assert cursor is None
        assert [row for row in managed if row.get("output_port") == "authoring_proposal"]
        history = client.timelines.history(project_id, "main", limit=10)
        assert history.ok, history.as_dict()
        assert history.data["head"]["revision_id"] != base_revision_id
    finally:
        speech_host.shutdown()
        outer_host.shutdown()
