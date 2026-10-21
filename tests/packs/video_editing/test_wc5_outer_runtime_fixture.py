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
import sys
from collections.abc import Mapping
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
        or "/home/user/work/wt/rt-pin-42a7203f"
    ).resolve()


def _data(value: Any) -> Any:
    return value.get("data", value) if isinstance(value, dict) else getattr(value, "data", value)


def _page_rows(value: Any) -> list[dict[str, Any]]:
    data = _data(value)
    if isinstance(data, Mapping):
        data = data.get("items", data.get("rows"))
    if isinstance(data, (list, tuple)) and len(data) == 2 and isinstance(data[0], list):
        data = data[0]
    if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
        raise AssertionError("Runtime read did not return a page of mappings")
    return data


def _managed_rows(client: Any, task_id: str) -> list[dict[str, Any]]:
    return _page_rows(client.tasks.list_managed_outputs(task_id))


def _assert_pinned_runtime_import(source: Path) -> None:
    """Import Runtime in a new interpreter, before pytest can import fixtures."""
    probe = subprocess.run(
        [
            sys.executable,
            "-B",
            "-c",
            (
                "import pathlib, runtime_protocol; "
                "module = pathlib.Path(runtime_protocol.__file__).resolve(); "
                "expected = pathlib.Path(__import__('sys').argv[1]).resolve(); "
                "assert module.is_relative_to(expected), (module, expected); "
                "print(module)"
            ),
            str(source),
        ],
        check=True,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONNOUSERSITE": "1",
            "PYTHONPATH": str(source),
        },
    )
    assert Path(probe.stdout.strip()).is_relative_to(source)


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
    assert source.joinpath("runtime_protocol").is_dir()
    commit = subprocess.run(
        ["git", "-C", str(source), "show", "-s", "--format=%H %T", RUNTIME_COMMIT],
        check=True, capture_output=True, text=True,
    ).stdout.strip().split()
    assert commit == [RUNTIME_COMMIT, RUNTIME_TREE]
    _assert_pinned_runtime_import(source)

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
        (requester_source, (
            "client.tasks.create", "observe_task_invocation", "TimelineSession.open",
            "queue_proposal", "session.flush", "authoring_proposal",
        )),
        (requester_module_source, ("generation.generate_speech", "_read_authoritative_media_info")),
        (shared_source, ("_read_authoritative_media_info", "settled_speech_input")),
    ):
        assert all(needle in source_text for needle in needles)
    assert all(Path(path).is_file() for path in ORIGINAL_POSITIVE_MAPPING)
    assert LATER_SELECTOR.endswith("test_wc5_real_runtime_outer_lifecycle")
    assert "real_runtime(commit=" not in inspect.getsource(test_wc5_real_runtime_outer_lifecycle)


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("ASTRID_RUN_WC5_OUTER") != "1",
    reason="source/preflight build; set ASTRID_RUN_WC5_OUTER=1 for the authorized real-runtime run",
)
def test_wc5_real_runtime_outer_lifecycle(tmp_path: Path, real_runtime) -> None:
    """Run the one real WC5 outer lifecycle when explicitly enabled."""
    import runtime_protocol
    from runtime_protocol.daemon import WORKER_ACTOR

    from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
    from astrid.packs.video_editing.shared import draft_voiceover
    from astrid.packs.video_editing.shared.draft_voiceover import _read_authoritative_media_info
    from astrid.sdk import AstridClient
    from astrid.sdk.invocation import invoke
    from astrid.sdk.timeline.sync import TimelineSession

    source = _runtime_source()
    assert Path(runtime_protocol.__file__).resolve().is_relative_to(source)
    assert subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip() == RUNTIME_COMMIT

    daemon = real_runtime()
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
            outbox_path = tmp_path / "outbox.json"
            commit_calls: list[tuple[dict[str, Any], str]] = []
            original_commit = client.timelines.commit

            def lost_ack(project: str, timeline: str, body: Mapping[str, Any], *, idempotency_key: str):
                captured = json.loads(json.dumps(body, sort_keys=True))
                commit_calls.append((captured, idempotency_key))
                accepted = original_commit(project, timeline, body, idempotency_key=idempotency_key)
                if len(commit_calls) == 1:
                    raise ConnectionError("lost acknowledgement after Runtime acceptance")
                return accepted

            client.timelines.commit = lost_ack
            try:
                with pytest.raises(ConnectionError, match="lost acknowledgement"):
                    draft_voiceover._sync_draft_voiceover(
                        client, project_id, "main", timing_policy="ripple", requester_entry=True,
                        outbox_path=outbox_path,
                    )
            finally:
                client.timelines.commit = original_commit
            speech_loop.result(timeout=30)
            outer_loop.result(timeout=30)

        assert len(commit_calls) == 1
        flight = json.loads(outbox_path.read_text(encoding="utf-8"))["flight"]
        assert flight["key"] == commit_calls[0][1]
        assert json.loads(flight["body"]) == commit_calls[0][0]

        task_rows = _page_rows(client.tasks.list(project_id))
        outer_rows = [row for row in task_rows if row.get("capability_id") == ACTION]
        assert len(outer_rows) == 1
        outer_id = str(outer_rows[0]["task_id"])
        outer_task = _data(client.tasks.show(outer_id))
        assert outer_task["task_id"] == outer_id
        assert outer_task["capability_id"] == ACTION
        assert outer_task["state"] in {"succeeded", "completed"}
        assert isinstance(outer_task["run_id"], str) and outer_task["run_id"]
        assert isinstance(outer_task["attempt_id"], str) and outer_task["attempt_id"]
        assert outer_task["result"]["outputs"]
        assert any(row.get("output_port") == "authoring_proposal"
                   for row in outer_task["result"]["outputs"])

        outer_outputs = _managed_rows(client, outer_id)
        proposal_outputs = [row for row in outer_outputs if row.get("output_port") == "authoring_proposal"]
        assert len(proposal_outputs) == 1
        proposal_output = proposal_outputs[0]
        assert proposal_output["task_id"] == outer_id
        assert proposal_output["attempt_id"] == outer_task["attempt_id"]
        assert proposal_output["run_id"] == outer_task["run_id"]
        assert proposal_output["provenance"]["task_id"] == outer_id
        assert proposal_output["provenance"]["attempt_id"] == outer_task["attempt_id"]
        proposal = json.loads(client.media.read_bytes(proposal_output["object_id"]))
        assert set(proposal) == {
            "schema_version", "producer", "admitted_target", "commands",
            "rationale", "proposal_digest",
        }
        assert proposal["producer"]["task_id"] == outer_id
        assert proposal["producer"]["attempt_id"] == outer_task["attempt_id"]
        assert proposal["producer"]["executor_id"] == "wc5-outer-worker"
        assert proposal["admitted_target"] == {
            "project_id": commit_calls[0][0]["project_id"],
            "timeline_id": commit_calls[0][0]["timeline_id"],
            "base_revision_id": commit_calls[0][0]["base_revision_id"],
            "base_publication_id": commit_calls[0][0]["base_publication_id"],
        }
        assert commit_calls[0][0]["commands"][0]["op"] == "producer.guard"
        assert commit_calls[0][0]["commands"][1:] == proposal["commands"]
        assert commit_calls[0][0]["commands"][0]["args"]["pin"]["task_id"] == outer_id

        speech_tasks = [row for row in task_rows if row.get("capability_id") == SPEECH]
        speech_task_ids = {str(row["task_id"]) for row in speech_tasks}
        speech_attempt_ids = {str(row["attempt_id"]) for row in speech_tasks if row.get("attempt_id")}
        assert old.kernel_task_id in speech_task_ids
        assert outer_id not in speech_task_ids
        assert proposal["producer"]["task_id"] not in speech_task_ids
        assert proposal["producer"]["attempt_id"] not in speech_attempt_ids
        speech_outputs = [row for row in _managed_rows(client, old.kernel_task_id)
                          if row.get("output_port") == "speech"]
        assert len(speech_outputs) == 1
        assert proposal_output["object_id"] not in {row["object_id"] for row in speech_outputs}

        session = TimelineSession.open(
            project_id, "main", client=client, outbox_path=outbox_path,
            base_revision_id=proposal["admitted_target"]["base_revision_id"],
            base_publication_id=proposal["admitted_target"]["base_publication_id"],
        )
        acceptance = session.flush()
        accepted = _data(acceptance)
        assert accepted["status"] in {"accepted", "rebased"}
        accepted_revision_id = accepted["accepted_revision_id"]
        accepted_publication_id = accepted["accepted_publication_id"]
        assert accepted_publication_id == acceptance["receipt"]["receipt_id"]
        history = _data(client.timelines.history(project_id, "main", limit=10))
        assert history["head"]["revision_id"] == accepted_revision_id
        assert history["head"]["publication_id"] == accepted_publication_id
        readback = _data(client.timelines.open_composition(project_id, "main"))
        assert readback["summary"]["head_revision_id"] == accepted_revision_id

        inverse = session.undo([accepted_publication_id], idempotency_key="wc5-outer-inverse")
        undone = _data(inverse)
        assert undone["status"] in {"accepted", "rebased"}
        assert undone["previous_publication_id"] == accepted_publication_id
        assert undone["accepted_revision_id"] == proposal["admitted_target"]["base_revision_id"]
        inverse_readback = _data(client.timelines.open_composition(project_id, "main"))
        assert inverse_readback["summary"]["head_revision_id"] == proposal["admitted_target"]["base_revision_id"]
    finally:
        speech_host.shutdown()
        outer_host.shutdown()
