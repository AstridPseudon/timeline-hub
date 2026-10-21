"""Central-only real pixel test: explicitly select this non-default filename.

Run through the worker's READY script under the central browser flock. This is
not automatically collected by main's cheap pytest lane and never fabricates a
positive PNG. The source fixture owns and removes the temporary host project.
"""

import hashlib
import json
import os
import shutil
import signal
import subprocess
from pathlib import Path

import pytest
from PIL import Image

from astrid.packs.rendering.actions.timeline_visualize.layers.builtin import _diff_fraction
from astrid.packs.rendering.actions.timeline_visualize.motion import model
from tests.packs.rendering.test_presenter_crop_equivalence import (
    area,
    legacy_element,
    png_crop,
    public_box,
    stage_geometry,
)
from tests.packs.rendering.test_presenter_scene_capability import (
    presenter_query as _presenter_query,
)

presenter_query = _presenter_query


def _capture(presenter_query, output, mode="explicit"):
    stage_geometry(presenter_query)
    for name in ("presenter_crop_entry.mjs", "presenter_crop_capture.mjs"):
        shutil.copyfile(Path(__file__).with_name(name), presenter_query.project / name)
    output.mkdir()
    command = [str(presenter_query.node), "presenter_crop_capture.mjs", str(output)]
    if mode != "explicit":
        command.append(mode)
    process = subprocess.Popen(command, cwd=presenter_query.project, env=presenter_query.env,
                               text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=180)
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=10)
    assert process.returncode == 0, stdout + stderr
    return json.loads((output / "inspection.json").read_text())


@pytest.mark.timeout(240)
def test_actual_registered_presenter_crop_pixels(presenter_query, tmp_path):
    assert os.environ.get("VIEWING_CROP_CENTRAL") == "1", "central READY grant required"
    assert subprocess.run(["flock", "-n", "/tmp/timeline-viewing-browser.lock", "true"]).returncode != 0
    case = _capture(presenter_query, tmp_path / "capture")
    assert case["frames"] == [0, 3, 4, 5]
    assert len(list((tmp_path / "capture").glob("*.png"))) == 4
    size = tuple(case["size"])
    assert size == (640, 360)
    paths = [tmp_path / "capture" / f"frame-{f}.png" for f in case["frames"]]
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    old = png_crop(model.mouth_box(legacy_element(case), 0), size)
    compat = png_crop(public_box(case["rows"][0]), size)
    erase = png_crop(public_box(case["rows"][0], "erase"), size)
    assert old == compat == (298, 202, 345, 219)
    assert erase == (300, 206, 343, 215)
    assert (area(old), area(compat), area(erase)) == (799, 799, 387)
    assert len(case["rows"]) == 1
    assert case["rows"][0]["componentFrame"] == 0
    assert case["rows"][0]["clipId"] == "presenter"
    crops = {"old": old, "compat": compat, "erase": erase}
    images = []
    for path in paths:
        with Image.open(path) as captured:
            assert captured.format == "PNG" and captured.size == size
            images.append(captured.convert("RGB"))
    for image in images:
        assert image.crop(old).tobytes() == image.crop(compat).tobytes()
        for crop in crops.values():
            assert _diff_fraction(image.crop(crop), image.crop(crop))[0] == 0
    fractions = {label: [_diff_fraction(a.crop(crop), b.crop(crop))[0]
                         for a, b in zip(images, images[1:])]
                 for label, crop in crops.items()}
    assert fractions["old"] == fractions["compat"]
    for values in fractions.values():
        assert any(f > .02 for f in values), fractions
    assert [f > .02 for f in fractions["old"]] == [f > .02 for f in fractions["compat"]]
    assert [f > .02 for f in fractions["old"]] == [f > .02 for f in fractions["erase"]]

    def planted_fractions(points):
        planted = images[0].copy()
        for point in points:
            original = images[0].getpixel(point)
            planted.putpixel(point, (255, 255, 255) if sum(original) < 384 else (0, 0, 0))
        return {label: _diff_fraction(images[0].crop(crop), planted.crop(crop))[0]
                for label, crop in crops.items()}

    controls = {}
    for count in (8, 15, 16, 20):
        points = [(erase[0] + 2 + i, erase[1] + 2) for i in range(count)]
        values = planted_fractions(points)
        for label, crop in crops.items():
            assert values[label] == count / area(crop)
        assert (values["old"] > .02) == (count >= 16)
        assert (values["compat"] > .02) == (count >= 16)
        assert values["erase"] > .02
        controls[str(count)] = values
    assert controls["8"]["old"] <= .02 < controls["8"]["erase"]
    assert controls["15"]["old"] <= .02 < controls["16"]["old"]
    points = [(compat[0] + i, compat[1]) for i in range(16)]
    assert all(not (erase[0] <= x < erase[2] and erase[1] <= y < erase[3]) for x, y in points)
    padding = planted_fractions(points)
    assert padding == {"old": 16 / 799, "compat": 16 / 799, "erase": 0}
    assert padding["old"] > .02 and padding["compat"] > .02
    controls["padding16"] = padding
    assert {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths} == before
    print(json.dumps({"png_sha256": before, "crop": crops,
                      "natural_pairs": fractions, "planted_controls": controls}, sort_keys=True))


@pytest.mark.timeout(240)
def test_actual_registered_presenter_partial_crop_pixels(presenter_query, tmp_path):
    """Future physical case: retain the partial-input 697 px private crop."""
    assert os.environ.get("VIEWING_CROP_CENTRAL") == "1", "central READY grant required"
    assert subprocess.run(["flock", "-n", "/tmp/timeline-viewing-browser.lock", "true"]).returncode != 0
    output = tmp_path / "partial-capture"
    case = _capture(presenter_query, output, "partial")
    assert case["frames"] == [0, 3, 4, 5]
    assert len(list(output.glob("*.png"))) == 4
    assert case["props"]["timeline"]["clips"][0]["params"]["mouth"] == {"x": 151, "y": 104}
    size = tuple(case["size"])
    assert size == (640, 360)
    paths = [output / f"frame-{f}.png" for f in case["frames"]]
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    private = png_crop(model.mouth_box(legacy_element(case), 0), size)
    compat = png_crop(public_box(case["rows"][0]), size)
    erase = png_crop(public_box(case["rows"][0], "erase"), size)
    assert private == (298, 202, 339, 219)
    assert compat == (298, 202, 345, 219)
    assert erase == (300, 206, 343, 215)
    assert (area(private), area(compat), area(erase)) == (697, 799, 387)
    assert len(case["rows"]) == 1
    assert case["rows"][0]["componentFrame"] == 0
    assert case["rows"][0]["clipId"] == "presenter"
    images = []
    for path in paths:
        with Image.open(path) as captured:
            assert captured.format == "PNG" and captured.size == size
            images.append(captured.convert("RGB"))
    public_private = (compat[0], compat[1], private[2], private[3])
    for image in images:
        assert image.crop(private).tobytes() == image.crop(public_private).tobytes()
    crops = {"private": private, "compat": compat, "erase": erase}
    fractions = {label: [_diff_fraction(a.crop(crop), b.crop(crop))[0]
                         for a, b in zip(images, images[1:])]
                 for label, crop in crops.items()}
    for values in fractions.values():
        assert any(f > .02 for f in values), fractions

    def planted_fractions(points):
        planted = images[0].copy()
        for point in points:
            original = images[0].getpixel(point)
            planted.putpixel(point, (255, 255, 255) if sum(original) < 384 else (0, 0, 0))
        return {label: _diff_fraction(images[0].crop(crop), planted.crop(crop))[0]
                for label, crop in crops.items()}

    controls = {}
    for count in (8, 15, 16, 20):
        points = [(erase[0] + 2 + i, erase[1] + 2) for i in range(count)]
        values = planted_fractions(points)
        for label, crop in crops.items():
            assert values[label] == count / area(crop)
        assert (values["private"] > .02) == (count >= 15)
        assert (values["compat"] > .02) == (count >= 16)
        assert values["erase"] > .02
        controls[str(count)] = values
    assert controls["8"]["private"] <= .02 < controls["8"]["erase"]
    assert controls["15"]["private"] > .02 >= controls["15"]["compat"]
    points = [(compat[0] + i, compat[1]) for i in range(16)]
    assert all(not (erase[0] <= x < erase[2] and erase[1] <= y < erase[3]) for x, y in points)
    padding = planted_fractions(points)
    assert padding == {"private": 16 / 697, "compat": 16 / 799, "erase": 0}
    assert padding["private"] > .02 and padding["compat"] > .02
    assert {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths} == before
    print(json.dumps({"png_sha256": before, "crop": crops,
                      "natural_pairs": fractions, "planted_controls": controls},
                     sort_keys=True, separators=(",", ":")))
