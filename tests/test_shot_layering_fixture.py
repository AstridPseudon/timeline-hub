from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "conformance/fixtures/shot-layering-v1.json"
REQUIRED_CASES = {
    "film-picture-over-type",
    "loose-above-shot",
    "loose-below-shot",
    "loose-same-row",
    "shot-only-suffix-tracks",
    "two-shots-one-row",
    "shot-row-missing",
}


def load_shot_layering_fixture() -> dict[str, Any]:
    """Read the shared fixture through Runtime's checked-in conformance path."""
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _values(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _values(child)
    else:
        yield value


def test_shared_shot_layering_fixture_is_valid_and_complete():
    fixture = load_shot_layering_fixture()

    assert fixture["$schema"] == "timeline.shot-layering/v1"
    assert fixture["schema_version"] == 1
    assert "UNKNOWN" not in set(_values(fixture))

    cases = fixture["cases"]
    assert {case["id"] for case in cases} == REQUIRED_CASES
    assert fixture["representation"]["group_tag"]["path"] == "track.app.group"
    assert fixture["representation"]["empty_area"] == {
        "mode": "transparent",
        "parent_content_visible": True,
        "opaque_background": False,
    }

    for case in cases:
        expected = case["expected"]
        assert expected["track_order"]
        group_ids = [group["id"] for group in expected["group_tracks"]]
        assert group_ids == [track_id for track_id in expected["track_order"] if "~" in track_id]
        for group in expected["group_tracks"]:
            tag = group["app"]["group"]
            assert group["id"] == f"{tag['id']}~{tag['sourceTrack']}"


def test_shared_shot_layering_fixture_read_path_covers_parent_and_child_timing():
    fixture = load_shot_layering_fixture()
    film = next(case for case in fixture["cases"] if case["id"] == "film-picture-over-type")
    shot = film["input"]["shots"][0]
    occurrence = shot["occurrence"]
    assert occurrence["track"] == "picture"
    assert occurrence["at_ms"] == 9100
    assert occurrence["duration_ms"] == 19600
    assert all("at_ms" in clip and "duration_ms" in clip for clip in shot["timeline"]["clips"])
    assert film["expected"]["clip_tracks"]["clip-0"] == "type"
    assert film["expected"]["clip_tracks"]["vision-audio"] == "audio"

