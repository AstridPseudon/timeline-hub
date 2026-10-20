from __future__ import annotations

import pytest

from astrid.packs.video_editing.shared import draft_voiceover as voiceover
from astrid.packs.video_editing.shared import draft_voiceover_proposal as proposal
from tests.packs.video_editing.test_draft_voiceover import (
    coordinator_client,
    fixture,
    synthesis,
)


def _normal_speech_output() -> dict:
    return {
        "association_id": "association-speech",
        "task_id": "speech-task",
        "attempt_id": "speech-attempt",
        "output_port": "generated_audio",
        "ordinal": 0,
        "role": "result",
        "filename": "speech.wav",
        "media_type": "audio/wav",
        "size": 1234,
        "digest": "sha256:" + "a" * 64,
        "durability": "durable",
    }


def test_normal_registered_speech_output_does_not_invent_selection_or_producer_pin():
    result = {
        "project_id": "p",
        "task_id": "speech-task",
        "attempt_id": "speech-attempt",
        "output": _normal_speech_output(),
    }

    assert proposal._completed_voiceover_output(result) is None


def test_native_voiceover_ready_requires_real_output_and_admitted_head():
    candidate = {
        "placements": [],
        "shots": {},
    }
    generated = [{
        "occurrence_id": "o1",
        "shot_id": "s1",
        "clip_id": "draft-vo-o1",
        "duration_seconds": 1,
        "output": _normal_speech_output(),
    }]

    assert not proposal._native_voiceover_ready(candidate, {}, generated, "pub-1")
    assert not proposal._native_voiceover_ready(candidate, {}, generated, None)


@pytest.mark.parametrize("timing_policy", ["preserve", "ripple"])
def test_unqualified_new_child_keeps_legacy_publish_route(monkeypatch, timing_policy):
    candidate, scripts = fixture(audio=False)
    scripts["occurrences"][0]["text"] = "New"
    client, bound = coordinator_client(candidate, scripts)
    monkeypatch.setattr(
        voiceover,
        "runtime_synthesizer",
        lambda *_args: lambda text, settings: {
            **synthesis(text, settings),
            "duration_seconds": 2,
        },
    )

    result = voiceover.sync_draft_voiceover(
        client, "p", "t", timing_policy=timing_policy,
    )

    assert result["status"] == "published"
    assert result["published"] and bound.published
    assert "proposal" not in result
