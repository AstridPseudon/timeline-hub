from __future__ import annotations

import copy
import hashlib
import json
from types import SimpleNamespace

import pytest

from astrid.packs.video_editing.shared import draft_voiceover as vo
from astrid.packs.video_editing.shared import voiceover_requester as requester
from astrid.packs.video_editing.shared.voiceover_requester import (
    _consume_settled_voiceover_input,
    _prepare_requester_speech_inputs,
)
from astrid.sdk.remote import RemoteAstridClient
from astrid.sdk.results import InvocationResult
from astrid.sdk.workspace_client import WorkspaceClient
from tests.packs.video_editing.test_draft_voiceover import fixture


def _target() -> dict[str, str]:
    return {
        "project_id": "p",
        "timeline_id": "t",
        "base_revision_id": "h",
        "base_publication_id": "publication",
    }


def _speech_result(output: dict[str, object]) -> InvocationResult:
    return InvocationResult(
        capability_id="generation.generate_speech",
        capability_type="executor",
        native_kind="executor",
        ok=True,
        raw_result={"task": {"state": "succeeded", "id": "speech-task"}},
        run_id="speech-run",
        kernel_run_id="speech-run",
        kernel_task_id="speech-task",
        kernel_attempt_id="speech-attempt",
        outputs={"managed_outputs": [output]},
    )


@pytest.fixture
def requester_case(monkeypatch):
    candidate, scripts = fixture(audio=False)
    scripts["occurrences"][0]["text"] = "New first line"
    candidate["project_id"] = "p"
    candidate["timeline_id"] = "t"
    audio = b"settled-wav"
    object_id = "sha256:" + hashlib.sha256(audio).hexdigest()
    selection = {
        "asset": "draft-voiceover-o1",
        "generation_id": "generation-1",
        "variant_id": "original",
        "object_id": object_id,
        "catalog_digest": "sha256:" + "a" * 64,
    }
    output = {
        "association_id": "association-1",
        "project_id": "p",
        "task_id": "speech-task",
        "attempt_id": "speech-attempt",
        "output_port": "speech",
        "object_id": object_id,
        "digest": object_id,
        "media_type": "audio/wav",
        "version": 2,
        "lifecycle": {"version": 2},
        "asset": selection["asset"],
        "generation_id": selection["generation_id"],
        "variant_id": selection["variant_id"],
        "catalog_digest": selection["catalog_digest"],
    }
    verified = {"selection": selection, "media_type": "audio/wav",
                "size": len(audio), "duration_seconds": 1.0}
    calls: list[dict[str, object]] = []
    imported: list[dict[str, object]] = []

    class Media:
        def import_bytes(self, **kwargs):
            imported.append(kwargs)
            body_digest = "sha256:" + hashlib.sha256(kwargs["data"]).hexdigest()
            return SimpleNamespace(ok=True, data={"object_id": body_digest, "digest": body_digest})

    workspace = WorkspaceClient("http://127.0.0.1:8765", "requester-token")

    def get_selection(self, project, selector):
        calls.append({"method": "selection", "project": project, "selector": selector})
        return selection

    def get_verified(self, project, selected):
        calls.append({"method": "verified", "project": project, "selection": selected})
        return verified

    def get_object(self, selected):
        calls.append({"method": "object", "object_id": selected})
        return {"data": audio}

    monkeypatch.setattr(WorkspaceClient, "get_project_media_selection", get_selection)
    monkeypatch.setattr(WorkspaceClient, "get_project_verified_media", get_verified)
    monkeypatch.setattr(WorkspaceClient, "get_object", get_object)
    from astrid.sdk.client import AstridClient

    client = AstridClient(remote=RemoteAstridClient(workspace))
    client.media.import_bytes = Media().import_bytes

    results = [_speech_result(output)]
    speech_calls = []

    def invoke(*args, **kwargs):
        speech_calls.append((args, copy.deepcopy(kwargs)))
        return results[0]

    monkeypatch.setattr("astrid.sdk.invoke", invoke)
    return SimpleNamespace(
        candidate=candidate, scripts=scripts, client=client, output=output,
        selection=selection, verified=verified, calls=calls, imported=imported,
        speech_calls=speech_calls,
    )


def _prepare(case):
    return _prepare_requester_speech_inputs(
        case.client,
        "p",
        case.candidate,
        case.scripts,
        requester_key="requester-original-key",
        target=_target(),
        script_pin={"revision_id": "h", "script_digest": "sha256:" + "b" * 64},
        occurrence_ids=["o1"],
    )


def test_requester_uses_normal_speech_body_without_duration_or_explicit_intent(requester_case):
    descriptors = _prepare(requester_case)
    assert len(descriptors) == 1
    _, kwargs = requester_case.speech_calls[0]
    assert kwargs["idempotency_key"].startswith("video-editing-voiceover-speech-")
    assert kwargs["wait"] is True
    assert kwargs["inputs"] == {"text": "New first line", **vo.DEFAULT_SETTINGS}
    assert "duration" not in kwargs["inputs"]
    assert "generation_intent" not in kwargs["inputs"]
    assert requester_case.calls[:3] == [
        {"method": "selection", "project": "p", "selector": {
            "association_id": "association-1", "object_id": requester_case.output["object_id"],
            "version": 2}},
        {"method": "verified", "project": "p", "selection": requester_case.selection},
        {"method": "object", "object_id": requester_case.output["object_id"]},
    ]


def test_requester_bundle_is_h3_enveloped_and_descriptor_is_exact(requester_case):
    descriptor = _prepare(requester_case)[0]
    imported = requester_case.imported[0]
    assert descriptor == {
        "name": "voiceover_speech_results",
        "object_id": descriptor["object_id"],
        "digest": descriptor["object_id"],
        "filename": descriptor["filename"],
        "required": True,
    }
    assert imported["filename"] == descriptor["filename"]
    body = imported["data"].decode()
    bundle = json.loads(body)
    assert bundle["schema_version"] == 1
    entry = bundle["results"][0]
    assert entry["occurrence_id"] == "o1"
    assert entry["result"]["schema_version"] == 1
    assert set(entry["result"]) == {"schema_version", "input_digest", "result_digest", "result"}
    assert entry["result"]["result"]["kernel_task_id"] == "speech-task"
    assert entry["result"]["result"]["outputs"]["managed_outputs"][0]["association_id"] == "association-1"


def test_requester_retry_reuses_root_key_and_original_file(requester_case):
    first = _prepare(requester_case)
    first_call = requester_case.speech_calls[0][1]
    first_import = requester_case.imported[0]
    second = _prepare(requester_case)
    second_call = requester_case.speech_calls[1][1]
    second_import = requester_case.imported[1]
    assert first == second
    assert first_call["idempotency_key"] == second_call["idempotency_key"]
    assert first_import["data"] == second_import["data"]
    assert first_import["idempotency_key"] == second_import["idempotency_key"]
    assert first_import["filename"] == second_import["filename"]


def test_requester_keys_are_per_occurrence_and_bundle_ordered(requester_case):
    requester_case.scripts["occurrences"][1]["text"] = "New second line"
    descriptors = _prepare_requester_speech_inputs(
        requester_case.client,
        "p",
        requester_case.candidate,
        requester_case.scripts,
        requester_key="requester-original-key",
        target=_target(),
        script_pin={"revision_id": "h", "script_digest": "sha256:" + "b" * 64},
    )
    assert len(descriptors) == 1
    keys = [call[1]["idempotency_key"] for call in requester_case.speech_calls]
    assert len(keys) == 2 and keys[0] != keys[1]
    entries = json.loads(requester_case.imported[0]["data"])["results"]
    assert [entry["occurrence_id"] for entry in entries] == ["o1", "o2"]


def test_requester_reuses_planner_refusal_for_normal_unowned_audio(monkeypatch):
    candidate, scripts = fixture(owned=False)
    client = SimpleNamespace(media=SimpleNamespace(import_bytes=lambda **kwargs: pytest.fail("must not import")))
    monkeypatch.setattr("astrid.sdk.invoke", lambda **kwargs: pytest.fail("must not synthesize"))
    assert _prepare_requester_speech_inputs(
        client, "p", candidate, scripts, requester_key="key", target=_target(),
        script_pin={"revision_id": "h"},
    ) == []


def _consumer_task(case, *, text="New first line", attempt_id="speech-attempt",
                   object_id=None):
    object_id = object_id or case.output["object_id"]
    output = {**case.output, "run_id": "speech-run", "task_id": "speech-task",
              "attempt_id": attempt_id, "object_id": object_id}
    return {
        "task_id": "speech-task", "run_id": "speech-run", "attempt_id": attempt_id,
        "project_id": "p", "capability_id": "generation.generate_speech",
        "state": "completed",
        "spec": {"spec": {"inputs": {"text": text, **vo.DEFAULT_SETTINGS}}},
        "result": {"outputs": [{"output_port": "speech", "object_id": object_id,
                                  "task_id": "speech-task", "attempt_id": attempt_id,
                                  "project_id": "p"}]},
    }, output


def _consume_requester_bundle(case, tmp_path, *, task=None, managed=None,
                              plan=None, **kwargs):
    descriptor = _prepare(case)[0]
    body = case.imported[-1]["data"]
    source = tmp_path / "voiceover-input.json"
    source.write_bytes(body)
    task, output = task or _consumer_task(case)
    case.client._remote.tasks = SimpleNamespace(
        show=lambda task_id: task if task_id == "speech-task" else None,
        list_managed_outputs=lambda task_id: managed if managed is not None else [output],
    )
    return source, descriptor, plan or {"jobs": [{
        "occurrence_id": "o1", "text": "New first line", "settings": dict(vo.DEFAULT_SETTINGS),
    }]}


def test_requester_consumer_roundtrips_one_claimant_file(requester_case, tmp_path):
    case = requester_case
    source, descriptor, plan = _consume_requester_bundle(case, tmp_path)
    seen = []
    consumed = _consume_settled_voiceover_input(
        source, attempt_root=tmp_path, client=case.client, project="p", plan=plan,
        target=_target(), script_pin={"revision_id": "h", "script_digest": "sha256:" + "b" * 64},
        requester_key="requester-original-key", consume=seen.append,
    )
    assert descriptor["object_id"] == "sha256:" + hashlib.sha256(
        case.imported[-1]["data"]
    ).hexdigest()
    assert consumed == [None]
    assert seen[0]["occurrence_id"] == "o1"
    assert seen[0]["root_idempotency_key"].startswith("video-editing-voiceover-speech-")
    assert seen[0]["media_selection"] == case.selection
    assert seen[0]["duration_seconds"] == case.verified["duration_seconds"]


@pytest.mark.parametrize("change", [
    lambda task: task["spec"]["spec"]["inputs"].update(text="changed"),
    lambda task: task.update(attempt_id="foreign-attempt"),
])
def test_requester_consumer_rejects_changed_runtime_claim(requester_case, tmp_path, change):
    case = requester_case
    source, _, plan = _consume_requester_bundle(case, tmp_path)
    task, _ = _consumer_task(case)
    change(task)
    case.client._remote.tasks = SimpleNamespace(
        show=lambda task_id: task,
        list_managed_outputs=lambda task_id: [],
    )
    with pytest.raises(vo.VoiceoverSyncError):
        _consume_settled_voiceover_input(
            source, attempt_root=tmp_path, client=case.client, project="p", plan=plan,
            consume=lambda value: value,
        )


def test_requester_consumer_rejects_duplicate_or_reordered_entries(requester_case, tmp_path):
    case = requester_case
    first = _prepare(case)[0]
    body = json.loads(case.imported[-1]["data"])
    second = copy.deepcopy(body["results"][0])
    second["occurrence_id"] = "o2"
    second["text"] = "New first line"
    second["root_idempotency_key"] = requester._root_idempotency_key(
        requester_key=body["request"]["requester_key"], target=body["request"]["target"],
        script_pin=body["request"]["script_pin"], settings=second["settings"],
        occurrence_id="o2", text="New first line",
    )
    body["request"]["occurrence_ids"] = ["o1", "o2"]
    body["results"].append(second)
    source = tmp_path / "voiceover-input.json"
    source.write_text(json.dumps(body), encoding="utf-8")
    task, output = _consumer_task(case)
    case.client._remote.tasks = SimpleNamespace(show=lambda task_id: task,
                                        list_managed_outputs=lambda task_id: [output])
    plan = {"jobs": [
        {"occurrence_id": "o1", "text": "New first line", "settings": dict(vo.DEFAULT_SETTINGS)},
        {"occurrence_id": "o2", "text": "New first line", "settings": dict(vo.DEFAULT_SETTINGS)},
    ]}
    assert len(_consume_settled_voiceover_input(
        source, attempt_root=tmp_path, client=case.client, project="p", plan=plan,
        consume=lambda value: value,
    )) == 2
    body["results"] = [second, first]
    body["request"]["occurrence_ids"] = ["o2", "o1"]
    source.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(vo.VoiceoverSyncError, match="occurrence order"):
        _consume_settled_voiceover_input(
            source, attempt_root=tmp_path, client=case.client, project="p", plan=plan,
            consume=lambda value: value,
        )
    body["results"] = [first, second]
    body["results"][1]["occurrence_id"] = "o1"
    body["request"]["occurrence_ids"] = ["o1", "o1"]
    source.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(vo.VoiceoverSyncError, match="occurrence order"):
        _consume_settled_voiceover_input(
            source, attempt_root=tmp_path, client=case.client, project="p", plan=plan,
            consume=lambda value: value,
        )
    assert first["object_id"] == "sha256:" + hashlib.sha256(
        case.imported[-1]["data"]
    ).hexdigest()


def test_requester_consumer_refuses_media_authority_failure(requester_case, tmp_path, monkeypatch):
    case = requester_case
    source, _, plan = _consume_requester_bundle(case, tmp_path)
    monkeypatch.setattr(requester, "_read_authoritative_media_info",
                        lambda *args: (_ for _ in ()).throw(vo.VoiceoverSyncError("NO-CARRIER")))
    with pytest.raises(vo.VoiceoverSyncError, match="NO-CARRIER"):
        _consume_settled_voiceover_input(
            source, attempt_root=tmp_path, client=case.client, project="p", plan=plan,
            consume=lambda value: value,
        )
