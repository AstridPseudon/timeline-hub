"""Real Runtime coverage for chapter shots and shared shot occurrences."""
from __future__ import annotations

import subprocess

import pytest

pytestmark = pytest.mark.integration


def test_real_chapter_shots_can_be_shared_and_arranged_with_typed_fps(
    tmp_path, monkeypatch, real_runtime,
):
    from tests.helpers.runtime import runtime_checkout, use_runtime

    runtime = runtime_checkout()
    monkeypatch.setenv("ASTRID_RUNTIME_CHECKOUT", str(runtime))
    use_runtime()

    daemon = real_runtime(authoring_profile="astrid")
    project = daemon.service.create_project({"slug": "chapter-shots", "name": "Chapter shots"})["id"]
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    client = open_client(daemon)
    created = client.timelines.create_empty(
        project=project,
        timeline_id="film",
        name="Chapter shots film",
        config={"output": {
            "resolution": "1280x720",
            "fps": {"numerator": 30000, "denominator": 1001},
            "file": "output.mp4",
            "background": None,
            "background_scale": None,
        }},
        idempotency_key="chapter-shots-create-film",
    )
    assert created.ok, created.as_dict()

    from astrid.sdk.timeline import Timeline
    from astrid.sdk.timeline import timeline_intent as intent

    timeline = Timeline.open(project, "film", client=client, outbox_path=tmp_path / "outbox.json")
    picture = tmp_path / "chapter.png"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=16x16:r=1",
         "-frames:v", "1", "-threads", "1", "-c:v", "png", str(picture)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    def seed_chapters(t):
        t.add(picture, at=0, hold=4, track="V1", id="opening", cut="c1")
        t.add(picture, at=4, hold=4, track="V1", id="next", cut="c2")
        intent.set_chapters(t.bundle, [
            {"name": "01 OPEN", "from": "c1"},
            {"name": "02 NEXT", "from": "c2"},
        ])

    seeded = timeline.commit(seed_chapters, label="Seed chapter film", key="chapter-shots-seed")
    assert seeded["receipt"]["receipt_id"]
    assert timeline.bundle["parent"]["config"]["output"]["fps"] == {
        "numerator": 30000, "denominator": 1001,
    }

    from astrid.sdk.timeline.checkout import Checkout

    checkout = Checkout.open(project, "film", client=client)
    restructured = checkout.publish(
        "Store chapters as shots", restructure=True, client=client,
        idempotency_key="chapter-shots-restructure",
    )
    assert restructured["receipt"]["receipt_id"]

    timeline = Timeline.open(project, "film", client=client, outbox_path=tmp_path / "shots-outbox.json")
    placements = timeline.bundle["placements"]
    assert len(placements) == 2
    canonical = placements[0]
    source_ref = "occurrence:" + canonical["occurrence_id"]
    from astrid.sdk.timeline.native_occurrence_shared import capture_occurrence_place_shared

    shared = capture_occurrence_place_shared(
        timeline.bundle, source_ref, "occ-shared", on=8,
    )
    placed = timeline.commit([shared], label="Place shared chapter shot", key="chapter-shots-share")
    assert placed["receipt"]["receipt_id"]

    arranged_ids = [canonical["occurrence_id"], placements[1]["occurrence_id"], "occ-shared"]
    arranged = timeline.commit(
        lambda t: t.arrange(arranged_ids, at=0, gap=0),
        label="Arrange chapter shots", key="chapter-shots-arrange",
    )
    assert arranged["receipt"]["receipt_id"]

    from astrid.sdk.timeline.commit import bundle_from_document

    persisted = bundle_from_document(arranged["data"]["canonical_document"])
    rows = {row["occurrence_id"]: row for row in persisted["placements"]}
    assert set(rows) == set(arranged_ids)
    assert rows["occ-shared"]["shot_id"] == canonical["shot_id"]
    assert [rows[identity]["placement"]["start_ms"] for identity in arranged_ids] == [0, 4004, 8008]
    assert persisted["shots"][canonical["shot_id"]]["payload"]["name"] == "01 OPEN"
    assert persisted["parent"]["config"]["output"]["fps"] == {
        "numerator": 30000, "denominator": 1001,
    }
