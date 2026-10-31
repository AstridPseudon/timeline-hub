"""Public SDK shot reuse against a scratch Runtime."""
from __future__ import annotations

import pytest

from tests.helpers.runtime import use_runtime


@pytest.fixture
def timeline_case(tmp_path, monkeypatch, real_runtime):
    from tests.helpers.runtime import runtime_checkout

    monkeypatch.setenv("ASTRID_RUNTIME_CHECKOUT", str(runtime_checkout()))
    use_runtime()
    daemon = real_runtime(authoring_profile="astrid")
    project = daemon.service.create_project({"slug": "sdk-shot-reuse", "name": "SDK shot reuse"})["id"]
    from tests.editing_conformance.test_commit_runtime_m1 import open_client

    client = open_client(daemon)
    created = client.timelines.create_empty(
        project=project,
        timeline_id="film",
        name="Shot reuse",
        idempotency_key="sdk-shot-reuse-create",
    )
    assert created.ok, created.as_dict()
    from astrid.sdk.timeline import Timeline

    timeline = Timeline.open(project, "film", client=client, outbox_path=tmp_path / "outbox.json")
    return client, project, timeline


def test_public_sdk_places_one_shot_in_two_occurrences(timeline_case):
    client, project, timeline = timeline_case
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    from astrid.sdk.timeline.native_occurrence_shared import capture_occurrence_place_shared

    bundle = bundle_from_document(timeline._runtime_document)
    birth = capture_occurrence_create(
        bundle,
        "occ-section",
        "shot-section",
        name="Section 1",
        track="V1",
        on=2,
        duration=3,
    )
    created = timeline.commit([birth], label="Turn section into shot", key="sdk-shot-reuse-birth")
    assert created["receipt"]["receipt_id"]

    bundle = bundle_from_document(timeline._runtime_document)
    shared = capture_occurrence_place_shared(bundle, "occurrence:occ-section", "occ-section-copy", on=9)
    placed = timeline.commit([shared], label="Place section again", key="sdk-shot-reuse-place")
    assert placed["receipt"]["receipt_id"]

    result = client.timelines.open_bundle(project, "film")
    assert result.ok, result.as_dict()
    occurrences = result.data["bundle"]["parent"]["occurrences"]
    by_id = {row["occurrence_id"]: row for row in occurrences}
    assert set(by_id) == {"occ-section", "occ-section-copy"}
    assert by_id["occ-section"]["shot_id"] == "shot-section"
    assert by_id["occ-section-copy"]["shot_id"] == "shot-section"
    assert by_id["occ-section"]["placement"]["start_ms"] == 2000
    assert by_id["occ-section-copy"]["placement"]["start_ms"] == 9000
