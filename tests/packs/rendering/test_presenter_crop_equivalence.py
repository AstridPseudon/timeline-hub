"""Counterexamples to replacing the legacy inspection crop with an erase region.

Only geometry is exercised here. Decoded pixel checks require the separately
selected presenter_crop_capture.py central test; generated PNGs are not evidence.
"""

import json
import math
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.packs.rendering.actions.timeline_visualize.motion import model
from tests.packs.rendering.test_presenter_scene_capability import (
    presenter_query as _presenter_query,
)

presenter_query = _presenter_query
pytestmark = pytest.mark.integration


def stage_geometry(query):
    shutil.copyfile(Path(__file__).with_name("presenter_crop_geometry.mjs"),
                    query.project / "presenter_crop_geometry.mjs")


@pytest.fixture(scope="module")
def crop_cases(presenter_query):
    stage_geometry(presenter_query)
    result = subprocess.run([str(presenter_query.node), "presenter_crop_geometry.mjs", "geometry"],
                            cwd=presenter_query.project, env=presenter_query.env,
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def legacy_element(case, *, own_view=True):
    clip = case["props"]["timeline"]["clips"][0]
    # Feed the same registered view to the existing old box function. This
    # isolates padding/default differences from the optional private view mirror.
    by_frame = {row["frame"]: row["motion"] for row in case["rows"]}
    return model.Element(clip["id"], clip["clipType"], clip["track"], 0, 2,
                         clip["params"], clip,
                         maths=SimpleNamespace(at=lambda _e, f, _fps: by_frame[f]) if own_view else None)


def png_crop(box, size):
    """Literal legacy builtin.lipsync conversion, including +1 and lower clamp."""
    sx, sy = size[0] / model.CANVAS[0], size[1] / model.CANVAS[1]
    return (max(0, int(box[0] * sx)), max(0, int(box[1] * sy)),
            int(box[2] * sx) + 1, int(box[3] * sy) + 1)


def public_box(row):
    assert row["mouth"]["status"] == "known"
    r = row["mouth"]["rect"]
    return r["x"], r["y"], r["x"] + r["width"], r["y"] + r["height"]


def area(crop):
    return (crop[2] - crop[0]) * (crop[3] - crop[1])


def test_registered_default_and_clamped_anchors_are_not_legacy_defaults(crop_cases):
    for case in crop_cases:
        old = model.mouth_box(legacy_element(case), 0)
        row = case["rows"][0]
        if case["name"] == "default":
            assert old is None
            assert public_box(row) == (900, 618, 1026, 642)
        elif case["name"] == "clamps":
            assert old == (-132, 5976, -108, 6024)
            assert public_box(row) == (-6, 1068, 12, 1092)
        elif case["name"] == "fractional":
            assert old == (903, 604.2, 1050.6, 652.2)
            assert public_box(row) == (912, 618, 1050, 642)


@pytest.mark.parametrize("size", [(1920, 1080), (640, 360), (641, 361), (720, 405)])
def test_same_frame_scaled_crop_denominators_differ(crop_cases, size):
    seen = set()
    for case in crop_cases:
        if case["name"] not in ("custom", "fractional", "zoom", "focusClamp", "push", "punch", "bob"):
            continue
        element = legacy_element(case)
        for row in case["rows"]:
            frame = row["frame"]
            seen.add(row["motion"]["mouth"])
            old = png_crop(model.mouth_box(element, frame), size)
            new = png_crop(public_box(row), size)
            assert all(math.isfinite(v) for v in old + new)
            if area(new) > 0 and area(old) > 0:
                assert area(old) != area(new), (case["name"], frame, size)
            # Using the private fallback view cannot fix the padding mismatch.
            fallback = png_crop(model.mouth_box(legacy_element(case, own_view=False), frame), size)
            assert fallback != new
    assert seen == {0, .5, 1}


def test_minimal_two_percent_counterexample_without_invented_pixels(crop_cases):
    case = next(c for c in crop_cases if c["name"] == "custom" and c["basis"]["fps"] == 30)
    old = png_crop(model.mouth_box(legacy_element(case), 0), (640, 360))
    new = png_crop(public_box(case["rows"][0]), (640, 360))
    assert old == (298, 202, 345, 219)
    assert new == (300, 206, 343, 215)
    assert (area(old), area(new)) == (799, 387)
    # Eight pixels above CHANGE_LEVEL inside both crops produce opposite verdicts
    # under the unchanged strict >2% rule. Actual comparator proof is central-only.
    assert 8 / area(old) <= .02 < 8 / area(new)


def test_frame_zero_series_crop_cannot_follow_a_moving_region(crop_cases):
    for name in ("push", "punch", "bob"):
        case = next(c for c in crop_cases if c["name"] == name and c["basis"]["fps"] == 30)
        element = legacy_element(case)
        fixed = model.mouth_box(element, 0)  # builtin.lipsync uses this for every pair
        assert any(model.mouth_box(element, row["frame"]) != fixed for row in case["rows"])
        assert any(public_box(row) != public_box(case["rows"][0]) for row in case["rows"])


def test_source_bound_unknown_is_not_a_replacement_crop(crop_cases):
    for case in crop_cases:
        if case["name"] in ("mosaic", "outer"):
            row = case["rows"][0]
            assert row["mouth"]["status"] == "unknown"
            assert "reason" in row["mouth"]
            assert model.mouth_box(legacy_element(case), 0) is not None
            with pytest.raises(AssertionError):
                public_box(row)
