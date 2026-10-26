"""Shot-layer grouping in both renderer-facing projection entry points."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
from pathlib import Path

import pytest

from astrid.core.timeline.duration import clip_timeline_duration
from astrid.core.timeline.shot_composition_projection import (
    ShotCompositionProjectionError,
    project_runtime_parent_composition,
    project_shot_composition,
)
from tests.helpers.runtime import locate_runtime

FIXTURE = Path(__file__).parents[1] / "fixtures" / "timeline" / "shot-layering-v1.json"
# Exact Runtime conformance/fixtures/shot-layering-v1.json, shared with the App.
FIXTURE_SHA256 = "3c75d3ede4f868bedc46bfebe1c6988e159a58d4edf444986509e9a87f8fba1e"
CASES = json.loads(FIXTURE.read_bytes())["cases"]


def test_fixture_matches_canonical_runtime_bytes():
    data = FIXTURE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == FIXTURE_SHA256
    runtime = locate_runtime()
    if runtime is not None:
        canonical = runtime / "conformance" / "fixtures" / FIXTURE.name
        if canonical.is_file():
            assert data == canonical.read_bytes()


def runtime_projection(graph):
    """Translate the canonical fixture's pins to the Runtime closure boundary."""
    parent = graph["parent_composition"]
    return project_runtime_parent_composition(
        {
            "project_id": graph["project"]["project_id"],
            "timeline_id": graph["primary_timeline"]["document_id"],
            "revision_id": graph["primary_timeline"]["head"]["revision_id"],
            "payload": {
                **parent,
                "occurrences": copy.deepcopy(graph["occurrences"]),
            },
        },
        shot_revisions=[
            {**revision, "internal_timeline_revision_id": revision["internal_timeline_revision"]["revision_id"]}
            for revision in graph["shot_revisions"]
        ],
        internal_timeline_revisions=[
            {"revision_id": revision["internal_timeline_revision"]["revision_id"],
             "payload": revision["internal_timeline_revision"]["timeline"]}
            for revision in graph["shot_revisions"]
        ],
    )


@pytest.fixture(params=[project_shot_composition, runtime_projection], ids=["graph", "runtime"])
def project(request):
    return request.param


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_shared_fixture_projection(project, case, caplog):
    graph = copy.deepcopy(case["input"])
    before = copy.deepcopy(graph)
    with caplog.at_level(logging.WARNING, logger="astrid.core.timeline.shot_composition_projection"):
        projection = project(graph)
    expected = case["expected"]
    tracks = projection.config["tracks"]
    assert [track["id"] for track in tracks] == expected["track_order"]
    assert [{"id": track["id"], "app": {"group": track["app"]["group"]}}
            for track in tracks if "group" in track.get("app", {})] == expected["group_tracks"]
    assert {
        clip.get("app", {}).get("astrid_shot_composition", {}).get("source_clip_id", clip["id"]): clip["track"]
        for clip in projection.config["clips"]
    } == expected["clip_tracks"]
    assert [{"severity": record.levelname.lower(), "code": record.code, "message": record.getMessage()}
            for record in caplog.records] == expected["warnings"]
    assert graph == before
    assert projection.config["clips"][:len(graph["parent_composition"]["config"]["clips"])] == graph["parent_composition"]["config"]["clips"]
    for start_ms, end_ms in expected.get("transparent_windows_ms", []):
        visual_tracks = {track["id"] for track in tracks if "group" in track.get("app", {})}
        assert not any(
            clip["track"] in visual_tracks
            and clip["at"] < end_ms / 1000
            and clip["at"] + clip_timeline_duration(clip) > start_ms / 1000
            for clip in projection.config["clips"]
        )


def source_graph():
    path = Path(__file__).parents[1] / "fixtures" / "timeline" / "shot_composition.json"
    graph = json.loads(path.read_text(encoding="utf-8"))
    graph["occurrences"] = graph["occurrences"][:1]
    graph["occurrences"][0]["track"] = "picture"
    graph["parent_composition"] = {
        "config": {"tracks": [{"id": "picture", "kind": "visual"}], "clips": []},
        "registry": {"assets": {}},
    }
    return graph


@pytest.mark.parametrize("placement", [
    {"transform": {"opacity": 0}}, {"transform": {"scale": 1}},
    {"transform": {"opaque": True}}, {"opacity": 0}, {"opacity": 1},
])
@pytest.mark.parametrize("blank", [False, True])
def test_nonempty_placement_compositing_is_refused_even_for_empty_shots(project, placement, blank):
    graph = source_graph()
    graph["occurrences"][0].update(placement)
    if blank:
        for revision in graph["shot_revisions"]:
            revision["internal_timeline_revision"]["timeline"]["clips"] = []
    with pytest.raises(ShotCompositionProjectionError) as exc:
        project(graph)
    assert str(exc.value) == (
        "Shot opacity and transforms are not supported yet. "
        "Remove them from the shot placement to render this timeline."
    )


@pytest.mark.parametrize("placement", [{}, {"transform": {}}, {"transform": None, "opacity": None}])
def test_empty_placement_keeps_child_geometry_and_audio(project, placement):
    graph = source_graph()
    graph["occurrences"][0].update(placement, gain=0.5, muted=True)
    revision = next(r for r in graph["shot_revisions"] if r["shot_id"] == "shot-alpha" and r["revision_id"] == "rev-a")
    timeline = revision["internal_timeline_revision"]["timeline"]
    timeline["tracks"][0]["app"] = {"keep": [1, 2]}
    timeline["clips"][0].update(x=10, width=200, opacity=0.4)
    before = copy.deepcopy(graph)
    projection = project(graph)
    assert graph == before
    visual, audio = projection.config["clips"]
    assert visual["track"] == "occ-1~video"
    assert {key: visual[key] for key in ("x", "width", "opacity")} == {"x": 10, "width": 200, "opacity": 0.4}
    assert visual["volume"] == 0
    assert audio["track"] == "audio"
    assert audio["hold"] == 2
    assert audio["volume"] == 0
    assert projection.config["tracks"][0]["app"] == {
        "keep": [1, 2], "group": {"id": "occ-1", "sourceTrack": "video"},
    }
