"""Compact dormant WC5 requester, custody, and input-blob coverage."""
from __future__ import annotations

import copy
import hashlib
import json
from types import SimpleNamespace

import pytest

from astrid.packs.video_editing.shared import draft_voiceover as vo
from astrid.packs.video_editing.shared import settled_voiceover_input as settled
from astrid.packs.video_editing.shared import voiceover_requester as requester
from tests.packs.video_editing.test_draft_voiceover import fixture


def _speech_result(object_id: str):
    output = {"output_port": "speech", "object_id": object_id, "role": "result", "ordinal": 0}
    payload = {
        field: None for field in (
            "capability_id", "capability_type", "native_kind", "ok", "error",
            "manifest_path", "run_id", "run_root", "outputs", "raw_result",
            "executor_version", "kernel_run_id", "kernel_task_id", "kernel_attempt_id",
        )
    }
    payload.update(
        capability_id="generation.generate_speech", capability_type="executor",
        native_kind="executor", ok=True, run_id="inner-run", kernel_run_id="inner-run",
        kernel_task_id="inner-task", kernel_attempt_id="inner-attempt",
        outputs={"managed_outputs": [output]},
    )

    class Result:
        ok = True
        run_id = "inner-run"
        kernel_run_id = "inner-run"
        kernel_task_id = "inner-task"
        kernel_attempt_id = "inner-attempt"
        error = None

        def output_rows(self, name):
            return [output] if name == "speech" else []

        def to_dict(self):
            return copy.deepcopy(payload)

    return Result(), payload, output


def test_requester_emits_one_exact_execution_blob_and_reuses_its_identity(monkeypatch):
    candidate, scripts = fixture()
    scripts["occurrences"][0]["text"] = "New"
    object_id = "sha256:" + "a" * 64
    imported = []
    speech_calls = []

    class Media:
        def import_bytes(self, **kwargs):
            imported.append(kwargs)
            digest = "sha256:" + hashlib.sha256(kwargs["data"]).hexdigest()
            return SimpleNamespace(ok=True, data={"object_id": digest})

    client = SimpleNamespace(media=Media())
    monkeypatch.setattr(requester, "_read_authoritative_media_info",
                        lambda *args: ({"asset": "voice", "generation_id": "g",
                                        "variant_id": "original", "object_id": object_id,
                                        "catalog_digest": "sha256:" + "b" * 64},
                                       {"duration_seconds": 2}))

    def invoke(*args, **kwargs):
        speech_calls.append(kwargs)
        return _speech_result(object_id)[0]

    monkeypatch.setattr("astrid.sdk.invoke", invoke)
    first = requester._prepare_requester_speech_inputs(client, "p", candidate, scripts)
    second = requester._prepare_requester_speech_inputs(client, "p", candidate, scripts)

    assert first == second and len(first) == 1
    assert first[0] == {
        "name": "settled_speech_input", "object_id": first[0]["object_id"],
        "digest": first[0]["object_id"], "filename": first[0]["filename"],
        "required": True,
    }
    assert speech_calls[0]["idempotency_key"] == speech_calls[1]["idempotency_key"]
    assert imported[0]["data"] == imported[1]["data"]
    bundle = json.loads(imported[0]["data"])
    assert set(bundle) == {"entries"}
    assert set(bundle["entries"][0]) == {"occurrence_id", "text", "settings", "result"}
    assert set(bundle["entries"][0]["result"]) == {
        "schema_version", "input_digest", "result_digest", "result",
    }
    assert "duration_seconds" not in imported[0]["data"].decode()


def test_settled_input_rechecks_runtime_custody_before_consuming_blob(tmp_path, monkeypatch):
    object_id = "sha256:" + "c" * 64
    _result, payload, _output = _speech_result(object_id)
    envelope = {
        "schema_version": 1,
        "input_digest": "sha256:" + "d" * 64,
        "result_digest": settled._stable_digest(payload),
        "result": payload,
    }
    body = {"entries": [{
        "occurrence_id": "o1", "text": "New", "settings": dict(vo.DEFAULT_SETTINGS),
        "result": envelope,
    }]}
    root = tmp_path / "attempt"
    path = root / "inputs" / "settled-speech.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(body))
    task = {
        "id": "inner-task", "run_id": "inner-run", "attempt_id": "inner-attempt",
        "project_id": "p", "capability": "generation.generate_speech", "state": "succeeded",
        "spec": {"inputs": {"text": "New", **vo.DEFAULT_SETTINGS}},
        "result": {"outputs": [{"output_port": "speech", "object_id": object_id}]},
    }
    managed = [{"output_port": "speech", "role": "result", "task_id": "inner-task",
                "attempt_id": "inner-attempt", "project_id": "p", "object_id": object_id}]
    client = SimpleNamespace(tasks=SimpleNamespace(
        show=lambda task_id: task,
        list_managed_outputs=lambda task_id: managed,
    ))
    selection = {"asset": "voice", "generation_id": "g", "variant_id": "original",
                 "object_id": object_id, "catalog_digest": "sha256:" + "e" * 64}
    monkeypatch.setattr(settled, "_read_authoritative_media_info",
                        lambda *args: (selection, {"duration_seconds": 2}))
    plan = {"jobs": [{"occurrence_id": "o1", "text": "New",
                      "settings": dict(vo.DEFAULT_SETTINGS)}]}
    rows = []
    settled._consume_settled_voiceover_input(
        path, attempt_root=root, client=client, project="p", plan=plan, consume=rows.append,
    )
    assert rows[0]["audio_media_id"] == object_id
    assert rows[0]["duration_seconds"] == 2.0
    assert rows[0]["output"]["task_id"] == "inner-task"

    envelope["result_digest"] = "sha256:" + "f" * 64
    path.write_text(json.dumps(body))
    with pytest.raises(vo.VoiceoverSyncError, match="integrity"):
        settled._consume_settled_voiceover_input(
            path, attempt_root=root, client=client, project="p", plan=plan, consume=rows.append,
        )
