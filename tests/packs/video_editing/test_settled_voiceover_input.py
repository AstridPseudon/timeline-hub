"""Private settled-input consumer checks; the outer action stays dormant."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.packs.video_editing.shared import settled_voiceover_input as consumer
from astrid.packs.video_editing.shared.draft_voiceover import VoiceoverSyncError

SETTINGS = {"provider": "edge-tts", "voice": "en-US-ChristopherNeural",
            "rate": "+0%", "volume": "+0%", "pitch": "+0Hz"}
SELECTION = {"asset": "draft-voiceover", "generation_id": "generation-1",
             "variant_id": "variant-1", "object_id": "sha256:" + "a" * 64,
             "catalog_digest": "sha256:" + "b" * 64}


def _envelope(*, task_id="speech-task", run_id="speech-run", attempt_id="speech-attempt",
              object_id=None, ok=True):
    object_id = object_id or SELECTION["object_id"]
    output = {"output_port": "speech", "ordinal": 0, "role": "result",
              "object_id": object_id, "task_id": task_id, "attempt_id": attempt_id,
              "project_id": "project"}
    result = {
        "capability_id": "generation.generate_speech", "capability_type": "executor",
        "native_kind": "executor", "ok": ok, "error": None, "manifest_path": None,
        "run_id": run_id, "run_root": None, "outputs": {"managed_outputs": [output]},
        "raw_result": {}, "executor_version": None, "kernel_run_id": run_id,
        "kernel_task_id": task_id, "kernel_attempt_id": attempt_id,
    }
    return {"schema_version": 1, "input_digest": "sha256:" + "1" * 64,
            "result_digest": consumer._stable_digest(result), "result": result}


def _client(*, state="succeeded", task_id="speech-task", run_id="speech-run",
            attempt_id="speech-attempt", capability="generation.generate_speech",
            project="project"):
    task = {"id": task_id, "run_id": run_id, "attempt_id": attempt_id,
            "project_id": project, "capability": capability, "state": state,
            "spec": {"inputs": {"text": "hello", **SETTINGS}},
            "result": {"outputs": [{"output_port": "speech",
                                      "object_id": SELECTION["object_id"]}]}}
    managed = [{"output_port": "speech", "ordinal": 0, "role": "result",
                "object_id": SELECTION["object_id"], "task_id": task_id,
                "attempt_id": attempt_id, "project_id": project}]
    return SimpleNamespace(tasks=SimpleNamespace(
        show=lambda value: task if value == task_id else None,
        list_managed_outputs=lambda value: managed if value == task_id else None,
    ))


def _entry():
    return {"occurrence_id": "occ-1", "text": "hello", "settings": dict(SETTINGS),
            "result": _envelope()}


def _write_input(tmp_path: Path, entries):
    path = tmp_path / "inputs.json"
    path.write_text(json.dumps({"entries": entries}), encoding="utf-8")
    return path


def _plan():
    return {"jobs": [{"occurrence_id": "occ-1", "text": "hello",
                      "settings": dict(SETTINGS)}]}


def test_consumer_rechecks_runtime_claim_and_returns_intrinsic_duration(monkeypatch, tmp_path):
    reads = []

    def authoritative(client, project, output):
        reads.append((client, project, dict(output)))
        return dict(SELECTION), {"selection": dict(SELECTION), "media_type": "audio/wav",
                                "size": 8, "duration_seconds": 2.75}

    monkeypatch.setattr(consumer, "_read_authoritative_media_info", authoritative)
    seen = []
    output = consumer._consume_settled_voiceover_input(
        _write_input(tmp_path, [_entry()]), attempt_root=tmp_path, client=_client(),
        project="project", plan=_plan(), consume=seen.append)

    assert output == [None]
    assert len(reads) == 1 and reads[0][1] == "project"
    assert seen[0]["media_selection"] == SELECTION
    assert seen[0]["audio_media_id"] == SELECTION["object_id"]
    assert seen[0]["duration_seconds"] == 2.75
    assert "duration_seconds" not in _entry()["result"]["result"]["outputs"]["managed_outputs"][0]


@pytest.mark.parametrize("change", [
    lambda entry: entry.update(occurrence_id="occ-2"),
    lambda entry: entry.update(text="different"),
    lambda entry: entry.update(settings={**SETTINGS, "rate": "+5%"}),
])
def test_consumer_rejects_plan_mismatch_before_runtime_read(monkeypatch, tmp_path, change):
    entry = _entry()
    change(entry)
    monkeypatch.setattr(consumer, "_read_authoritative_media_info",
                        lambda *args: pytest.fail("media must not be read"))
    with pytest.raises(VoiceoverSyncError, match="differs from the ordered plan"):
        consumer._consume_settled_voiceover_input(
            _write_input(tmp_path, [entry]), attempt_root=tmp_path, client=_client(),
            project="project", plan=_plan(), consume=lambda value: value)


@pytest.mark.parametrize("field,value,pattern", [
    ("state", "running", "not completed"),
    ("project", "foreign", "project or capability"),
    ("capability", "rendering.render", "project or capability"),
    ("attempt_id", "foreign-attempt", "identity differs"),
])
def test_consumer_rejects_foreign_or_unsettled_runtime_task(tmp_path, field, value, pattern):
    kwargs = {field: value}
    if field == "project":
        kwargs["project"] = value
    with pytest.raises(VoiceoverSyncError, match=pattern):
        consumer._consume_settled_voiceover_input(
            _write_input(tmp_path, [_entry()]), attempt_root=tmp_path,
            client=_client(**kwargs), project="project", plan=_plan(),
            consume=lambda value: value)


def test_consumer_rejects_claimed_duration_and_missing_runtime_authority(monkeypatch, tmp_path):
    entry = _entry()
    entry["result"]["result"]["outputs"]["managed_outputs"][0]["duration_seconds"] = 99
    entry["result"]["result_digest"] = consumer._stable_digest(entry["result"]["result"])
    monkeypatch.setattr(consumer, "_read_authoritative_media_info",
                        lambda *args: (_ for _ in ()).throw(VoiceoverSyncError("NO-CARRIER")))
    with pytest.raises(VoiceoverSyncError, match="NO-CARRIER"):
        consumer._consume_settled_voiceover_input(
            _write_input(tmp_path, [entry]), attempt_root=tmp_path, client=_client(),
            project="project", plan=_plan(), consume=lambda value: value)


def test_consumer_does_not_mutate_claimant(tmp_path, monkeypatch):
    entry = _entry()
    before = copy.deepcopy(entry)
    monkeypatch.setattr(consumer, "_read_authoritative_media_info",
                        lambda *args: (dict(SELECTION), {"selection": dict(SELECTION),
                                                         "media_type": "audio/wav", "size": 8,
                                                         "duration_seconds": 1.0}))
    consumer._consume_settled_voiceover_input(
        _write_input(tmp_path, [entry]), attempt_root=tmp_path, client=_client(),
        project="project", plan=_plan(), consume=lambda value: value)
    assert entry == before
