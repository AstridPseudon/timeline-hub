"""Offline requester-side carrier tests; no speech root or Runtime is run."""
from __future__ import annotations

import copy
import hashlib
import json
from types import SimpleNamespace

import pytest

from astrid.packs.video_editing.shared import draft_voiceover as vo
from astrid.packs.video_editing.shared import voiceover_requester as requester
from astrid.sdk.results import InvocationResult
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commit import _digest
from tests.packs.video_editing.test_draft_voiceover import fixture
from tests.sdk.test_timeline_sync import initial_bundle


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
    candidate["project_id"] = "project"
    candidate["timeline_id"] = "timeline"
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
        "project_id": "project",
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
    imported = []

    class Media:
        def import_bytes(self, **kwargs):
            imported.append(kwargs)
            body_digest = "sha256:" + hashlib.sha256(kwargs["data"]).hexdigest()
            return SimpleNamespace(ok=True, data={"object_id": body_digest, "digest": body_digest})

    client = SimpleNamespace(media=Media())
    monkeypatch.setattr(requester, "_read_authoritative_media_info",
                        lambda *args: (copy.deepcopy(selection), copy.deepcopy(verified)))
    speech_calls = []

    def invoke(*args, **kwargs):
        speech_calls.append((args, copy.deepcopy(kwargs)))
        return _speech_result(output)

    monkeypatch.setattr("astrid.sdk.invoke", invoke)
    return SimpleNamespace(candidate=candidate, scripts=scripts, client=client,
                           imported=imported, speech_calls=speech_calls)


def _prepare(case):
    return requester._prepare_requester_speech_inputs(
        case.client, "project", case.candidate, case.scripts, occurrence_ids=["o1"])


def test_requester_uses_normal_speech_inputs_without_duration_or_intent(requester_case):
    descriptors = _prepare(requester_case)
    assert len(descriptors) == 1
    _, kwargs = requester_case.speech_calls[0]
    assert kwargs["wait"] is True
    assert kwargs["inputs"] == {"text": "New first line", **vo.DEFAULT_SETTINGS}
    assert "duration" not in kwargs["inputs"]
    assert "generation_intent" not in kwargs["inputs"]


def test_requester_imports_exact_h3_entries_and_ordinary_descriptor(requester_case):
    descriptor = _prepare(requester_case)[0]
    imported = requester_case.imported[0]
    assert descriptor == {
        "name": "settled_speech_input",
        "object_id": descriptor["object_id"],
        "digest": descriptor["object_id"],
        "filename": descriptor["filename"],
        "required": True,
    }
    assert imported["filename"] == descriptor["filename"]
    bundle = json.loads(imported["data"])
    assert set(bundle) == {"entries"}
    entry = bundle["entries"][0]
    assert set(entry) == {"occurrence_id", "text", "settings", "result"}
    assert entry["occurrence_id"] == "o1"
    assert set(entry["result"]) == {"schema_version", "input_digest", "result_digest", "result"}
    assert entry["result"]["result"]["kernel_task_id"] == "speech-task"
    assert "duration_seconds" not in entry["result"]["result"]["outputs"]["managed_outputs"][0]


def test_requester_reuses_root_and_bundle_identity_on_retry(requester_case):
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


def test_dormant_requester_joins_outer_admission_and_existing_producer_outbox(
        requester_case, monkeypatch, tmp_path):
    target = {
        "project_id": "project", "timeline_id": "timeline",
        "base_revision_id": "r0", "base_publication_id": "pub0",
    }
    descriptor = {
        "name": "settled_speech_input", "object_id": "sha256:" + "b" * 64,
        "digest": "sha256:" + "b" * 64, "filename": "settled.json", "required": True,
    }
    command = capture_move(initial_bundle(), "parent/clip:a", 3)
    proposal = {
        "schema_version": 1,
        "producer": {"task_id": "outer-task", "attempt_id": "outer-attempt",
                      "executor_id": "worker", "fence": 1, "runtime_epoch": 2},
        "admitted_target": target,
        "commands": [command],
        "rationale": "Reviewed voiceover",
    }
    proposal["proposal_digest"] = _digest(proposal)
    proposal_bytes = json.dumps(proposal, sort_keys=True).encode()
    proposal_id = "sha256:" + hashlib.sha256(proposal_bytes).hexdigest()
    admissions = []
    class Tasks:
        def create(self, **kwargs):
            admissions.append(kwargs)
            return SimpleNamespace(ok=True, data={"task_id": "outer-task", "run_id": "outer-run"})

    class Media:
        def read_bytes(self, object_id):
            assert object_id == proposal_id
            return proposal_bytes

    requester_case.client.tasks = Tasks()
    requester_case.client.media = Media()
    monkeypatch.setattr(requester, "_prepare_requester_speech_inputs",
                        lambda *args, **kwargs: [copy.deepcopy(descriptor)])
    monkeypatch.setattr("astrid.sdk.observe_task_invocation", lambda *args, **kwargs: InvocationResult(
        capability_id="video_editing.sync_draft_voiceover", capability_type="executor",
        native_kind="executor", ok=True, kernel_run_id="outer-run", kernel_task_id="outer-task",
        kernel_attempt_id="outer-attempt", outputs={"managed_outputs": [{
            "output_port": "authoring_proposal", "object_id": proposal_id,
            "role": "result", "ordinal": 0,
        }]},
    ))
    queued = []
    class Session:
        def queue_proposal(self, value):
            queued.append(copy.deepcopy(value))
        def flush(self, **kwargs):
            return {"accepted": True, **kwargs}

    monkeypatch.setattr("astrid.sdk.timeline.sync.TimelineSession.open",
                        lambda *args, **kwargs: Session())
    result = requester._requester_sync_draft_voiceover(
        requester_case.client, "project", "timeline", candidate=requester_case.candidate,
        scripts=requester_case.scripts, admitted_target=target, timing_policy="ripple",
        outbox_path=tmp_path / "outbox.json",
    )
    assert result["status"] == "published" and queued == [proposal]
    admission = admissions[0]
    assert admission["capability"] == "video_editing.sync_draft_voiceover"
    assert admission["input_manifest"] == [descriptor["object_id"]]
    assert admission["execution_request"]["inputs"] == [descriptor]
    assert admission["spec"]["inputs"]["settled_speech_input"] == descriptor
    assert admission["spec"]["runtime_dependencies"]["publication"]["admitted_target"] == target
    assert "path" not in descriptor and "producer" not in descriptor
