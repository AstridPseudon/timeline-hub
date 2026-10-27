"""E14 acceptance against the current editing-integration Runtime."""
from __future__ import annotations

import copy
import json
import subprocess
import time
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
    for count in (20, 200):
        local = timeline_type.open(project, "film", client=client,
                                   outbox_path=tmp_path / f"timing-{count}.json")
        prior = _snapshot(local)
        timing_history = _history(client, project)
        start = time.perf_counter()
        measured = local.commit(
            lambda t, n=count: [t.add(source, at=1000 + index * 2, hold=1,
                                      track="V1", id=f"timing-{n}-{index:03d}")
                                for index in range(n)],
            label=f"Timing {count} items",
            key=f"e14-timing-{count}",
        )
        timings[str(count)] = round(time.perf_counter() - start, 6)
        assert measured["receipt"]["receipt_id"]
        assert len(_history(client, project)) == len(timing_history) + 1
        timed_after = copy.deepcopy(measured["data"]["canonical_document"])
        undone = local.undo(publications=[measured["receipt"]["receipt_id"]])
        assert undone["data"]["canonical_document"] == prior
        assert timed_after != prior
        assert len(_history(client, project)) == len(timing_history) + 2

    evidence = Path(
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a"
        "/scratchpad/orch/workers/D-E14-reserved-identity-r1/evidence"
    )
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "e14-timings.json").write_text(
        json.dumps({"runtime": RUNTIME_COMMIT,
                    "commit_seconds": timings}, indent=2) + "\n",
        encoding="utf-8",
    )

