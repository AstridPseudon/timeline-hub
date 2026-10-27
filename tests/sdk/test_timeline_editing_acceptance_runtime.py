"""E14 acceptance against the current editing-integration Runtime."""
from __future__ import annotations

import copy
import io
import json
import subprocess
import time
import wave
from pathlib import Path

import pytest

RUNTIME_CHECKOUT = "/home/user/work/wt-int/runtime-tl-editing-integration"
RUNTIME_COMMIT = "d3ba02669bdffa84f9c43979c87dae0d3648b287"


@pytest.fixture
def editing_case(tmp_path, monkeypatch, real_runtime):
    """A fresh Runtime realm with a real HTTP client and an empty timeline."""
    from tests.helpers.runtime import use_runtime

    monkeypatch.setenv("ASTRID_RUNTIME_CHECKOUT", RUNTIME_CHECKOUT)
    runtime = use_runtime()
    actual = subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD"], text=True).strip()
    assert actual == RUNTIME_COMMIT
    from runtime_protocol import timeline_commit_store

    assert Path(timeline_commit_store.__file__).resolve() == runtime / "runtime_protocol/timeline_commit_store.py"

    daemon = real_runtime(authoring_profile="astrid")
    project = daemon.service.create_project({"slug": "e14-acceptance", "name": "E14 acceptance"})["id"]
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    client = open_client(daemon)
    created = client.timelines.create_empty(
        project=project,
        timeline_id="film",
        name="E14 film",
        idempotency_key="e14-create-film",
    )
    assert created.ok, created.as_dict()
    from astrid.sdk.timeline import Timeline

    timeline = Timeline.open(project, "film", client=client, outbox_path=tmp_path / "outbox.json")
    return daemon, client, project, timeline


def _history(client, project):
    result = client.timelines.history(project, "film", limit=100)
    assert result.ok, result.as_dict()
    return result.data["items"]


def _snapshot(timeline):
    return copy.deepcopy(timeline._runtime_document)


def _media_file(path):
    """Create a tiny deterministic PNG without an external fixture or install."""
    subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=16x16:r=1",
         "-frames:v", "1", "-threads", "1", "-c:v", "png", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return path


def _voice_file(path):
    audio = io.BytesIO()
    with wave.open(audio, "wb") as output:
        output.setparams((1, 2, 8000, 0, "NONE", "not compressed"))
        output.writeframes(b"\x00\x00" * 16000)
    path.write_bytes(audio.getvalue())
    return path


def test_e14_twenty_real_occurrences_arrange_once_and_exact_undo(editing_case):
    _daemon, client, project, timeline = editing_case
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create

    bundle = bundle_from_document(_snapshot(timeline))
    births = [capture_occurrence_create(
        bundle, f"occ-{index:02d}", f"shot-{index:02d}", name=f"Shot {index:02d}",
        track="V1", on=index * 3, duration=2,
    ) for index in range(20)]
    setup = timeline.commit(births, label="Create twenty shot occurrences", key="e14-create-shots")
    assert setup["receipt"]["receipt_id"]
    assert len(_history(client, project)) == 2  # Bootstrap plus occurrence setup.

    before = _snapshot(timeline)
    history_before = _history(client, project)
    order = [f"occ-{index:02d}" for index in reversed(range(20))]
    arranged = timeline.commit(lambda t: t.arrange(order, at=100, gap=0),
                               label="Arrange twenty shots", key="e14-arrange-shots")
    assert arranged["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(history_before) + 1
    rows = arranged["data"]["canonical_document"]["parent_revision"]["payload"]["occurrences"]
    assert [row["occurrence_id"] for row in rows] == order
    assert [row["placement"]["start_ms"] for row in rows] == [100000 + i * 2000 for i in range(20)]
    undone = timeline.undo(publications=[arranged["receipt"]["receipt_id"]])
    assert undone["data"]["canonical_document"] == before
    assert len(_history(client, project)) == len(history_before) + 2


def test_e14_picture_and_voice_on_new_tracks_one_receipt_exact_undo(editing_case, tmp_path):
    _daemon, client, project, timeline = editing_case
    picture = _media_file(tmp_path / "picture.png")
    voice = _voice_file(tmp_path / "voice.wav")
    before = _snapshot(timeline)
    history_before = _history(client, project)

    result = timeline.commit(
        lambda t: (
            t.track("V2", above="V1"),
            t.add(picture, at=0, hold=2, track="V2", id="new-picture"),
            t.add(voice, at=0, track="A2", id="new-voice"),
        ),
        label="Picture and voice on new tracks",
        key="e14-picture-voice",
    )
    after = result["data"]["canonical_document"]
    payload = after["parent_revision"]["payload"]
    clips = {row["id"]: row for row in payload["clips"]}
    assert result["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(history_before) + 1
    assert clips["new-picture"]["track"] == "V2"
    assert clips["new-voice"]["track"] == "A2"
    assert {row["id"] for row in payload["config"]["tracks"]} >= {"V1", "V2", "A2"}
    undone = timeline.undo(publications=[result["receipt"]["receipt_id"]])
    assert undone["data"]["canonical_document"] == before
    assert len(_history(client, project)) == len(history_before) + 2


def test_e14_twenty_ordered_media_one_receipt_exact_undo_and_timings(editing_case, tmp_path):
    _daemon, client, project, timeline = editing_case
    timeline_type = type(timeline)
    source = _media_file(tmp_path / "frame.png")
    before = _snapshot(timeline)
    history_before = _history(client, project)

    result = timeline.commit(
        lambda t: [t.add(source, at=index * 2, hold=1, track="V1", id=f"shot-{index + 1:02d}")
                   for index in range(20)],
        label="Place twenty files",
        key="e14-place-twenty",
    )

    assert result["data"]["status"] in {"accepted", "merged", "rebased"}
    assert result["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(history_before) + 1
    assert len(result["imports"]) == 1  # Same content under one identity is reused.
    after = copy.deepcopy(result["data"]["canonical_document"])
    clips = after["parent_revision"]["payload"]["clips"]
    assert [row["id"] for row in clips] == [f"shot-{index + 1:02d}" for index in range(20)]
    assert [row["at"] for row in clips] == [index * 2 for index in range(20)]

    undo = timeline.undo(publications=[result["receipt"]["receipt_id"]])
    assert undo["data"]["canonical_document"] == before
    assert len(_history(client, project)) == len(history_before) + 2

    # Timing is observational evidence only; it is deliberately not a performance gate.
    timings = {}
    local = timeline_type.open(project, "film", client=client,
                               outbox_path=tmp_path / "timing-20.json")
    prior = _snapshot(local)
    timing_history = _history(client, project)
    start = time.perf_counter()
    measured = local.commit(
        lambda t: [t.add(source, at=1000 + index * 2, hold=1,
                         track="V1", id=f"timing-20-{index:03d}")
                   for index in range(20)],
        label="Timing 20 items",
        key="e14-timing-20",
    )
    timings["20"] = round(time.perf_counter() - start, 6)
    assert measured["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(timing_history) + 1
    timed_after = copy.deepcopy(measured["data"]["canonical_document"])
    undone = local.undo(publications=[measured["receipt"]["receipt_id"]])
    assert undone["data"]["canonical_document"] == prior
    assert timed_after != prior
    assert len(_history(client, project)) == len(timing_history) + 2

    # Keep each setup request bounded. The measured edit below changes one clip
    # on a timeline that already contains 200 real items; it is not a 200-item
    # batch mislabeled as a timeline-size observation.
    timing_setup_commits = 0
    local = timeline_type.open(project, "film", client=client,
                               outbox_path=tmp_path / "timing-200.json")
    for batch in range(10):
        start_index = batch * 20
        seeded = local.commit(
            lambda t, start_index=start_index: [
                t.add(source, at=2000 + index * 2, hold=1, track="V1",
                      id=f"timing-200-{index:03d}")
                for index in range(start_index, start_index + 20)
            ],
            label=f"Seed 200-item timing fixture {batch + 1}",
            key=f"e14-timing-200-seed-{batch + 1}",
        )
        assert seeded["receipt"]["receipt_id"]
        timing_setup_commits += 1

    prior = _snapshot(local)
    assert len(prior["parent_revision"]["payload"]["clips"]) == 200
    timing_history = _history(client, project)
    start = time.perf_counter()
    measured = local.commit(
        lambda t: t.clip("timing-200-000").hold_for(2),
        label="Timing edit on 200 items",
        key="e14-timing-200-edit",
    )
    timings["200_item_timeline_edit"] = round(time.perf_counter() - start, 6)
    assert measured["receipt"]["receipt_id"]
    assert len(_history(client, project)) == len(timing_history) + 1
    timed_after = copy.deepcopy(measured["data"]["canonical_document"])
    assert timed_after != prior
    undone = local.undo(publications=[measured["receipt"]["receipt_id"]])
    assert undone["data"]["canonical_document"] == prior
    assert len(_history(client, project)) == len(timing_history) + 2

    evidence = Path(
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
        "/scratchpad/orch/workers/D-E14-reserved-identity-r1/evidence"
    )
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "e14-timings.json").write_text(
        json.dumps({"runtime": RUNTIME_COMMIT,
                    "commit_seconds": timings,
                    "200_item_setup_commits": timing_setup_commits,
                    "200_item_setup_count": 200}, indent=2) + "\n",
        encoding="utf-8",
    )

