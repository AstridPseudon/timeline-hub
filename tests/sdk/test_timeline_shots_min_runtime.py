"""Minimum public Runtime proof for reusing one shot in two occurrences."""
from __future__ import annotations

import copy

import pytest


@pytest.fixture
def shots_case(tmp_path, monkeypatch, real_runtime):
    from tests.helpers.runtime import runtime_checkout, use_runtime

    runtime = runtime_checkout()
    monkeypatch.setenv("ASTRID_RUNTIME_CHECKOUT", str(runtime))
    use_runtime()

    daemon = real_runtime(authoring_profile="astrid")
    project = daemon.service.create_project({"slug": "shots-min", "name": "Shots minimum"})["id"]
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    client = open_client(daemon)
    created = client.timelines.create_empty(
        project=project,
        timeline_id="film",
        name="Shots minimum",
        idempotency_key="shots-min-create-film",
    )
    assert created.ok, created.as_dict()

    from astrid.sdk.timeline import Timeline

    timeline = Timeline.open(project, "film", client=client, outbox_path=tmp_path / "outbox.json")
    return client, project, timeline


def test_one_named_shot_can_be_placed_twice_arranged_and_listed_on_runtime(shots_case):
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    from astrid.sdk.timeline.native_occurrence_shared import capture_occurrence_place_shared

    client, project, timeline = shots_case
    timeline.commit(lambda t: t.track("picture", kind="visual"), label="Add picture track")
    first_bundle = bundle_from_document(copy.deepcopy(timeline._runtime_document))
    first = capture_occurrence_create(
        first_bundle,
        "occ-section-a",
        "shot-section",
        name="Section",
        track="picture",
        on=0,
        duration=2,
    )
    timeline.commit([first], label="Make section a shot")

    current_bundle = bundle_from_document(copy.deepcopy(timeline._runtime_document))
    second = capture_occurrence_place_shared(
        current_bundle, "occurrence:occ-section-a", "occ-section-b", on=0,
    )
    timeline.commit([second], label="Use section shot twice")

    timeline.commit(
        lambda t: t.arrange(["occ-section-b", "occ-section-a"], at=5, gap=1),
        label="Arrange section occurrences",
    )

    listed = client.timelines.show(project, "film")
    assert listed.ok, listed.as_dict()
    rows = listed.data["canonical_document"]["parent_revision"]["payload"]["occurrences"]
    by_id = {row["occurrence_id"]: row for row in rows}
    assert set(by_id) == {"occ-section-a", "occ-section-b"}
    assert [by_id[key]["shot_id"] for key in ("occ-section-b", "occ-section-a")] == [
        "shot-section", "shot-section",
    ]
    assert [by_id[key]["placement"]["start_ms"] for key in ("occ-section-b", "occ-section-a")] == [
        5000, 8000,
    ]
