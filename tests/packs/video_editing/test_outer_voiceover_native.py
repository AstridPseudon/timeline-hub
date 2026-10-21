"""One native private15 voiceover proposal through the requester outbox."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest
from runtime_protocol.timeline_commit_port import route_path

from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.client import AstridClient
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.native_text_binding import capture_text_binding_set
from astrid.sdk.timeline.sync import TimelineSession
from astrid_runtime_client import WorkspaceClient
from tests.editing_conformance.test_recipe_m1_commands import bundle as authored_bundle
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration

OLD_TEXT = "Long old narration with extra words"
NEW_TEXT = "Long new narration"
TIMELINE = "film"
SETTINGS = {
    "provider": "edge-tts",
    "voice": "en-US-ChristopherNeural",
    "rate": "+0%",
    "volume": "+0%",
    "pitch": "+0Hz",
}


def _fixture_generation_pack(root: Path) -> Path:
    """Build a network-disabled speech executor with text-distinct WAV output."""
    pack = root / "generation"
    executor = pack / "executors" / "generate_speech"
    executor.mkdir(parents=True)
    (pack / "pack.yaml").write_text(
        "schema_version: 2\n"
        "id: generation\n"
        "name: Private15 speech fixture\n"
        "version: 1.0.0\n"
        "capabilities: [generate_speech]\n"
        "content:\n  executors: executors\n",
        encoding="utf-8",
    )
    (executor / "STAGE.md").write_text(
        "# Private15 speech fixture\n\n"
        "This executor is a deterministic, network-disabled test fixture.\n",
        encoding="utf-8",
    )
    script = r'''
import hashlib
import json
import io
import wave
from pathlib import Path
import sys

out = Path(sys.argv[1])
text = sys.argv[2]
out.joinpath("audio").mkdir(parents=True, exist_ok=True)
wav_path = out / "audio" / "speech.wav"
seed = hashlib.sha256(text.encode("utf-8")).digest()
with wave.open(str(wav_path), "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(8000)
    wav.writeframes((seed * (8000 * 4 // len(seed) + 1))[:8000 * 4])
audio_hash = hashlib.sha256(wav_path.read_bytes()).hexdigest()
manifest_path = out / "speech-provenance.json"
manifest_path.write_text(json.dumps({
    "text": text,
    "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    "settings": {
        "provider": "edge-tts",
        "voice": "en-US-ChristopherNeural",
        "rate": "+0%",
        "volume": "+0%",
        "pitch": "+0Hz",
    },
    "audio_sha256": audio_hash,
    "duration_seconds": 4.0,
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
'''
    (executor / "executor.yaml").write_text(json.dumps({
        "schema_version": 1,
        "id": "generation.generate_speech",
        "name": "Private15 speech fixture",
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
    }), encoding="utf-8")
    return pack


def _selection(row):
    value = row.get("selection", row)
    return {key: value[key] for key in (
        "asset", "generation_id", "variant_id", "object_id", "catalog_digest")}


def _preflight_fixture(pack: Path) -> None:
    """Validate the complete fixture closure before starting a real worker flow."""
    from astrid.core._shared.result_manifest import harvest_staged_outputs
    from astrid.core.execution.executor.folder import (
        discover_folder_executor_roots,
        load_folder_executor,
    )
    from astrid.core.execution.generic_host import component_load_failures
    from astrid.core.pack.canonical import validate_canonical_pack
    from astrid.core.pack.loader import discover_packs
    from astrid.core.pack.validate import validate_pack
    from astrid.sdk.invocation import _generation_publish_effect

    errors, warnings = validate_pack(pack)
    assert errors == [], errors
    assert warnings == [], warnings
    canonical = validate_canonical_pack(pack)
    assert canonical.definition.id == pack.name == "generation"
    discovered_packs = discover_packs(pack.parent)
    assert [(item.id, item.root.name) for item in discovered_packs] == [("generation", "generation")]
    assert component_load_failures([pack]) == []

    executor_roots = discover_folder_executor_roots(pack)
    assert executor_roots == (pack / "executors" / "generate_speech",)
    definition = load_folder_executor(executor_roots[0])
    assert definition.id == "generation.generate_speech"
    assert definition.metadata["generation_publication"] == {
        "version": 1,
        "modality": "audio",
        "output_port": "speech",
    }
    assert definition.isolation.network is False
    assert {output.name for output in definition.outputs} == {"speech", "speech_manifest"}
    assert {
        output.path_template for output in definition.outputs
    } == {"{out}/audio/speech.wav", "{out}/speech-provenance.json"}
    assert json.loads((executor_roots[0] / "executor.yaml").read_text())["isolation"] == {
        "mode": "subprocess",
        "network": False,
    }

    host = GenericPackHost(pack_roots=[pack], client=None, attempt_root=pack.parent / "preflight-attempts")
    try:
        records = host.discover()
        assert [record.id for record in records] == ["generation.generate_speech"]
        host.preflight("generation.generate_speech")
        record = host.capabilities["generation.generate_speech"]
        assert record.ready
        assert record.preflight["network"] == {"ok": True}
        assert record.definition.metadata["source_pack"] == "generation"
        effect = _generation_publish_effect(
            SimpleNamespace(
                id=record.id,
                outputs=record.definition.outputs,
                definition=record.definition.to_dict(),
            ),
            project="preflight-project",
            generation_intent={
                "version": 1,
                "modality": "audio",
                "partial_success_policy": "reject",
                "groups": [{
                    "group_key": "main",
                    "selectors": [{
                        "selector": "main-0",
                        "ordinal": 0,
                        "variant_key": "original",
                    }],
                }],
            },
        )
        assert effect["effect_type"] == "generation.publish_v1"
        assert effect["payload"]["generation_type"] == record.id
        assert effect["payload"]["groups"][0]["selectors"][0]["output_port"] == "speech"

        with tempfile.TemporaryDirectory(prefix="private15-fixture-output-") as output_dir:
            output_root = Path(output_dir)
            command = [
                sys.executable if argument == "{python_exec}" else argument
                for argument in record.definition.command.argv
            ]
            command = [
                str(output_root) if argument == "{out}" else argument
                for argument in command
            ] + ["Preflight narration"]
            completed = subprocess.run(command, check=False, capture_output=True, text=True)
            assert completed.returncode == 0, completed.stderr
            harvested = harvest_staged_outputs(
                output_root, definition=record.definition, require=True
            )
            assert {item["name"] for item in harvested} == {"speech", "speech_manifest"}
            assert {Path(item["path"]).name for item in harvested} == {
                "speech.wav", "speech-provenance.json"
            }
    finally:
        host.shutdown()


def _speech_result(client, project: str, text: str, key: str):
    result = client.invoke_result(
        "generation.generate_speech",
        kind="executor",
        project=project,
        inputs={"text": text, **SETTINGS},
        wait=True,
        idempotency_context={"private15_native": key},
    )
    assert result.ok, result.error
    outputs = result.outputs.get("managed_outputs") or result.outputs.get("artifacts") or []
    audio = next(
        row for row in outputs
        if row.get("name") in {"speech", "generated_audio"}
        or row.get("output_port") in {"speech", "generated_audio"}
        or str(row.get("path", "")).endswith("speech.wav")
    )
    from astrid.packs.video_editing.shared.draft_voiceover import _read_authoritative_media_info

    selection, verified = _read_authoritative_media_info(client, project, audio)
    return result, selection, verified


def _replace_source_media(value, *, old_object: str, old_selection: dict,
                          old_media: str, old_audio_media: str,
                          old_audio_object: str) -> None:
    if isinstance(value, dict):
        for key, child in list(value.items()):
            if isinstance(child, str) and child == old_media:
                value[key] = old_object
            else:
                if isinstance(child, str) and child == old_audio_media:
                    value[key] = old_audio_object
                else:
                    _replace_source_media(child, old_object=old_object,
                                          old_selection=old_selection, old_media=old_media,
                                          old_audio_media=old_audio_media,
                                          old_audio_object=old_audio_object)
        if value.get("selection") == old_selection:
            value["selection"] = copy.deepcopy(old_selection)
        if value.get("object_id") == old_media:
            value["object_id"] = old_object
    elif isinstance(value, list):
        for child in value:
            _replace_source_media(child, old_object=old_object,
                                  old_selection=old_selection, old_media=old_media,
                                  old_audio_media=old_audio_media,
                                  old_audio_object=old_audio_object)


def _source_document(project: str, old_selection: dict, old_duration: float,
                     new_duration: float, picture_object: str) -> dict:
    """Build the authored source using native fixture structure and live media pins."""
    source = authored_bundle(shared=False)
    source["project_id"] = project
    source["timeline_id"] = TIMELINE
    old_media = "sha256:" + "1" * 64
    old_audio_media = "sha256:" + "3" * 64
    for shot in source["shots"].values():
        internal = shot["internal_timeline"]
        next(row for row in internal["tracks"] if row["id"] == "voice")["id"] = "vo"
        audio = next(row for row in internal["clips"] if row["id"] == "voice-1")
        audio["id"] = "vo"
        audio["track"] = "vo"
        audio.update({"from": 0, "to": new_duration, "hold": new_duration})
        registry = internal["registry"]["assets"]["voice"]
        registry["media_id"] = old_selection["object_id"]
        registry["selection"] = copy.deepcopy(old_selection)
        registry["duration"] = old_duration
        shot["payload"]["metadata"]["draft_voiceover"] = {
            "schema_version": 1,
            "owner": "video_editing.sync_draft_voiceover",
            "status": "draft",
            "clip_id": "vo",
            "audio_media_id": old_selection["object_id"],
            "text": OLD_TEXT,
            "text_digest": _digest(OLD_TEXT),
            "settings": copy.deepcopy(SETTINGS),
            "duration_seconds": old_duration,
        }
    _replace_source_media(source, old_object=picture_object, old_selection=old_selection,
                          old_media=old_media, old_audio_media=old_audio_media,
                          old_audio_object=old_selection["object_id"])
    publication = compile_authoring_candidate(source).publication
    publication["project_id"] = project
    publication["timeline_id"] = TIMELINE
    return {
        "project_id": project,
        "timeline_id": TIMELINE,
        "expected_head": None,
        "parent_revision_id": publication["parent_revision_id"],
        "content_digest": publication["content_digest"],
        "parent_composition": publication["parent_composition"],
        "internal_timeline_revisions": publication["internal_timeline_revisions"],
        "shot_revisions": publication["shot_revisions"],
    }


def _commit_body(service, project: str, commands: list[dict]) -> dict:
    head = service.get_project_timeline(project, TIMELINE)
    return {
        "api_version": 1,
        "project_id": project,
        "timeline_id": TIMELINE,
        "base_revision_id": head["head_revision_id"],
        "base_publication_id": head["head_publication_id"],
        "commands": commands,
        "dry_run": False,
    }


def _outer_admission(owner, record, project: str, target: dict, script_object: str):
    return owner.admit_task(
        capability_id=record.id,
        capability_digest=record.capability_digest,
        input_object_ids=[script_object],
        project_id=project,
        idempotency_key="private15-outer-task",
        spec={
            "capability_id": record.id,
            "kind": "executor",
            "inputs": {
                "project": project,
                "timeline_ref": TIMELINE,
                "timing_policy": "ripple",
                "occurrence_ids": ["occ-1"],
                "padding_seconds": 0.15,
            },
            "runtime_dependencies": {"publication": {"admitted_target": target}},
            "outputs": {
                "authoring_proposal": {
                    "type": "file",
                    "artifact_type": "timeline/authoring-proposal",
                }
            },
        },
        execution_request={
            "target": {"kind": "default"},
            "inputs": [{
                "name": "script",
                "object_id": script_object,
                "filename": "script.txt",
                "required": True,
            }],
        },
    )


def test_outer_native_voiceover_proposal_outbox_retry_undo(tmp_path: Path, real_runtime, monkeypatch):
    """Managed outer action -> real speech -> settled proposal -> durable requester."""
    use_runtime()
    generation_root = _fixture_generation_pack(tmp_path)
    _preflight_fixture(generation_root)
    daemon = real_runtime()
    inner = outer = sdk = None
    inner_thread = None
    try:
        owner = WorkspaceClient(daemon.endpoint, daemon.token)
        owner.handshake(
            "private15-native-owner", "1.0", [
                "projects:read", "projects:write", "objects:read", "objects:write",
                "tasks:read", "tasks:write", "worker:execute",
            ],
        )
        sdk = AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=daemon.service.realm["id"],
            actor_id="owner",
            client_name="private15-native-owner",
            client_version="1.0",
            protocol_version="workspace.v1",
        )
        project = owner.create_project(
            "Private15 native", slug="private15-native", idempotency_key="private15-project"
        ).project_id
        from runtime_protocol.daemon import WORKER_SCOPES

        inner_token, inner_credential = daemon.credentials.provision(
            "private15-inner-speech", list(WORKER_SCOPES)
        )
        outer_token, outer_credential = daemon.credentials.provision(
            "private15-outer-producer", list(WORKER_SCOPES)
        )
        dependency_root = tmp_path / "site-packages"
        dependency_root.mkdir()
        (dependency_root / "runtime_protocol").symlink_to(
            use_runtime() / "runtime_protocol", target_is_directory=True
        )
        monkeypatch.setenv(
            "PYTHONPATH",
            os.pathsep.join((str(dependency_root), os.environ.get("PYTHONPATH", ""))),
        )
        inner = GenericPackHost(
            pack_roots=[generation_root],
            client=RuntimeProtocolClient(
                daemon.endpoint, inner_token, credential_file=inner_credential
            ),
            executor_id="private15-inner-speech",
            attempt_root=tmp_path / "inner-attempts",
        )
        inner.discover()
        inner.preflight("generation.generate_speech")
        assert inner.capabilities["generation.generate_speech"].ready
        inner.register()

        def serve_inner():
            inner.run(once=False, poll_seconds=0.05, max_tasks=3)

        inner_thread = threading.Thread(target=serve_inner, daemon=True)
        inner_thread.start()
        old_result, old_selection, old_verified = _speech_result(sdk, project, OLD_TEXT, "old")
        new_result, new_selection, new_verified = _speech_result(sdk, project, NEW_TEXT, "new-setup")
        assert old_result.kernel_task_id != new_result.kernel_task_id
        assert old_selection["object_id"] != new_selection["object_id"]
        assert old_verified["media_type"] == new_verified["media_type"] == "audio/wav"

        picture = owner.ingest_project_object(
            project, b"private15-picture-source", media_type="video/mp4", filename="picture.mp4",
            idempotency_key="private15-picture",
        )
        source = _source_document(
            project, old_selection, old_verified["duration_seconds"],
            new_verified["duration_seconds"], picture["object_id"],
        )
        source_result = daemon.service.publish_parent_composition(
            project, TIMELINE, source, idempotency_key="private15-source-publish"
        )
        assert source_result["data"]["project_id"] == project
        commits, _ = daemon.service._timeline_commits()
        commits.install_verified_baseline(project, TIMELINE, authorize=lambda: None)

        script_old = owner.ingest_project_object(
            project, OLD_TEXT.encode(), media_type="text/plain; charset=utf-8", filename="old.txt",
            idempotency_key="private15-script-old",
        )
        old_pin = {
            "object_id": script_old["object_id"], "digest": script_old["object_id"],
            "size": script_old["size"], "media_type": "text/plain; charset=utf-8", "utf8": True,
        }
        closure = commits.revision_closure(
            project, TIMELINE, daemon.service.get_project_timeline(project, TIMELINE)["head_revision_id"]
        )
        text_command = capture_text_binding_set(
            bundle_from_document(closure), "occurrence:occ-1",
            {"kind": "voiceover_script", "slot": None}, text=old_pin, verified_text=[old_pin],
        )
        first_text = daemon.service.commit_timeline(
            project, TIMELINE, _commit_body(daemon.service, project, [text_command]),
            idempotency_key="private15-text-old", publisher="private15-setup",
            invocation_path=route_path(project, TIMELINE),
            authorize=lambda: None,
        )
        assert first_text["data"]["status"] == "accepted"

        script_new = owner.ingest_project_object(
            project, NEW_TEXT.encode(), media_type="text/plain; charset=utf-8", filename="new.txt",
            idempotency_key="private15-script-new",
        )
        new_pin = {
            "object_id": script_new["object_id"], "digest": script_new["object_id"],
            "size": script_new["size"], "media_type": "text/plain; charset=utf-8", "utf8": True,
        }
        closure = commits.revision_closure(
            project, TIMELINE, daemon.service.get_project_timeline(project, TIMELINE)["head_revision_id"]
        )
        text_command = capture_text_binding_set(
            bundle_from_document(closure), "occurrence:occ-1",
            {"kind": "voiceover_script", "slot": None}, text=new_pin, verified_text=[new_pin],
        )
        changed_text = daemon.service.commit_timeline(
            project, TIMELINE, _commit_body(daemon.service, project, [text_command]),
            idempotency_key="private15-text-new", publisher="private15-setup",
            invocation_path=route_path(project, TIMELINE),
            authorize=lambda: None,
        )
        assert changed_text["data"]["status"] == "accepted"
        baseline = commits.revision_closure(
            project, TIMELINE, daemon.service.get_project_timeline(project, TIMELINE)["head_revision_id"]
        )
        target = {
            "project_id": project, "timeline_id": TIMELINE,
            "base_revision_id": daemon.service.get_project_timeline(project, TIMELINE)["head_revision_id"],
            "base_publication_id": daemon.service.get_project_timeline(project, TIMELINE)["head_publication_id"],
        }

        video_root = Path(__file__).resolve().parents[3] / "astrid/packs/video_editing"
        outer = GenericPackHost(
            pack_roots=[video_root],
            client=RuntimeProtocolClient(
                daemon.endpoint, outer_token, credential_file=outer_credential
            ),
            executor_id="private15-outer-producer",
            attempt_root=tmp_path / "outer-attempts",
        )
        records = outer.discover()
        record = next(row for row in records if row.id == "video_editing.sync_draft_voiceover")
        outer.preflight("video_editing.sync_draft_voiceover")
        assert outer.capabilities[record.id].ready
        outer.register()
        task = _outer_admission(owner, record, project, target, script_new["object_id"])
        outer_results = outer.run(once=True)
        assert len(outer_results) == 1 and outer_results[0].state == "succeeded"
        completed = owner.get_task(task.task_id)
        proposal_output = next(
            row for row in completed.result["outputs"] if row["name"] == "authoring_proposal"
        )
        proposal = json.loads(owner.get_object(proposal_output["digest"]).data)
        assert set(proposal) == {"schema_version", "producer", "admitted_target", "commands", "rationale", "proposal_digest"}
        assert proposal["producer"]["task_id"] == task.task_id
        assert proposal["producer"]["task_id"] not in {old_result.kernel_task_id, new_result.kernel_task_id}
        assert proposal["admitted_target"] == target
        assert [command["op"] for command in proposal["commands"]] == [
            "occurrence.resize", "occurrence.start", "clip.set", "occurrence.swap-media", "shot.set"
        ]
        assert proposal["commands"][0]["args"]["duration_ms"] == pytest.approx(
            new_verified["duration_seconds"] * 1000 + 150, abs=1
        )
        assert proposal["commands"][1]["args"]["start_ms"] == pytest.approx(
            proposal["commands"][0]["args"]["duration_ms"] + 10000, abs=1
        )
        assert proposal["commands"][3]["args"]["media"]["object_id"] == new_selection["object_id"]
        assert proposal["commands"][3]["args"]["old_media"]["object_id"] == old_selection["object_id"]

        outbox = tmp_path / "private15-requester-outbox.json"
        session = TimelineSession.open(project, TIMELINE, client=sdk, outbox_path=outbox)
        session.queue_proposal(proposal)
        transport = sdk._remote._transport
        real_commit = transport.commit_timeline
        calls = []

        def lost_ack(*args, **kwargs):
            calls.append((copy.deepcopy(args), copy.deepcopy(kwargs)))
            real_commit(*args, **kwargs)
            raise ConnectionError("lost TimelineSession acknowledgement")

        monkeypatch.setattr(transport, "commit_timeline", lost_ack)
        with pytest.raises(ConnectionError, match="lost TimelineSession acknowledgement"):
            session.flush(idempotency_key="private15-request")
        state = json.loads(outbox.read_text())
        assert state["flight"]["key"] == "private15-request"
        assert state["pending"]

        monkeypatch.setattr(transport, "commit_timeline", real_commit)
        retry_calls = []

        def record_retry(*args, **kwargs):
            retry_calls.append((copy.deepcopy(args), copy.deepcopy(kwargs)))
            return real_commit(*args, **kwargs)

        monkeypatch.setattr(transport, "commit_timeline", record_retry)
        restarted = TimelineSession.open(project, TIMELINE, client=sdk, outbox_path=outbox)
        accepted = restarted.flush()
        assert len(calls) == len(retry_calls) == 1
        assert calls[0] == retry_calls[0]
        assert accepted["data"]["status"] == "accepted"
        accepted_receipt = accepted["receipt"]["receipt_id"]
        undone = restarted.undo([accepted_receipt], idempotency_key="private15-undo")
        assert undone["data"]["status"] == "accepted"
        assert undone["data"]["canonical_document"] == baseline
        history = daemon.service.list_timeline_commits(project, TIMELINE, authorize=lambda: None)["items"]
        assert sum(row["publication_id"] == accepted_receipt for row in history) == 1
        assert len(history) >= 5
    finally:
        if outer is not None:
            outer.shutdown()
        if inner is not None:
            inner.shutdown()
        if inner_thread is not None:
            inner_thread.join(timeout=5)
        if sdk is not None:
            sdk.__exit__(None, None, None)
        daemon.stop()

