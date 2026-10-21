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


@pytest.mark.timeout(240)
def test_actual_registered_presenter_crop_pixels(presenter_query, tmp_path):
    assert os.environ.get("VIEWING_CROP_CENTRAL") == "1", "central READY grant required"
    assert subprocess.run(["flock", "-n", "/tmp/timeline-viewing-browser.lock", "true"]).returncode != 0
    stage_geometry(presenter_query)
    for name in ("presenter_crop_entry.mjs", "presenter_crop_capture.mjs"):
        shutil.copyfile(Path(__file__).with_name(name), presenter_query.project / name)
    output = tmp_path / "capture"
    output.mkdir()
    process = subprocess.Popen([str(presenter_query.node), "presenter_crop_capture.mjs", str(output)],
                               cwd=presenter_query.project, env=presenter_query.env,
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
    case = json.loads((output / "inspection.json").read_text())
    assert case["frames"] == [0, 3, 4, 5]
    assert len(list(output.glob("*.png"))) == 4
    size = tuple(case["size"])
    assert size == (640, 360)
    paths = [output / f"frame-{f}.png" for f in case["frames"]]
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    old = png_crop(model.mouth_box(legacy_element(case), 0), size)
    compat = png_crop(public_box(case["rows"][0]), size)
    erase = png_crop(public_box(case["rows"][0], "erase"), size)
    assert old == compat == (298, 202, 345, 219)
    assert erase == (300, 206, 343, 215)
    assert (area(old), area(compat), area(erase)) == (799, 799, 387)
    assert len(case["rows"]) == 1  # one component-zero query for the series
    assert case["rows"][0]["componentFrame"] == 0
    assert case["rows"][0]["clipId"] == "presenter"
    crops = {"old": old, "compat": compat, "erase": erase}
    images = []
    for path in paths:
        with Image.open(path) as captured:
            assert captured.format == "PNG" and captured.size == size
            images.append(captured.convert("RGB"))
    # Same unaltered actual PNGs and the unchanged strict >2% comparator.
    for image in images:
        assert image.crop(old).tobytes() == image.crop(compat).tobytes()
        for crop in crops.values():
            region = image.crop(crop)
            assert _diff_fraction(region, region.copy())[0] == 0
    fractions = {label: [_diff_fraction(a.crop(crop), b.crop(crop))[0]
                         for a, b in zip(images, images[1:])]
                 for label, crop in crops.items()}
    assert fractions["old"] == fractions["compat"]
    for values in fractions.values():
        assert any(f > .02 for f in values), fractions
    assert [f > .02 for f in fractions["old"]] == [f > .02 for f in fractions["compat"]]
    assert [f > .02 for f in fractions["old"]] == [f > .02 for f in fractions["erase"]]

    def planted_fractions(points):
        # Plant above CHANGE_LEVEL in a fresh copy; never edit a captured PNG.
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
    # Sixteen points wholly in padding: old/compat detect, erase misses.
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
def test_actual_registered_presenter_default_crop_pixels(presenter_query, tmp_path):
    """One default-constructor case; fail at the real private/public seam."""
    assert os.environ.get("VIEWING_CROP_CENTRAL") == "1", "central READY grant required"
    assert subprocess.run(["flock", "-n", "/tmp/timeline-viewing-browser.lock", "true"]).returncode != 0
    stage_geometry(presenter_query)
    for name in ("presenter_crop_entry.mjs", "presenter_crop_capture.mjs"):
        shutil.copyfile(Path(__file__).with_name(name), presenter_query.project / name)
    output = tmp_path / "default-capture"
    output.mkdir()
    process = subprocess.Popen([str(presenter_query.node), "presenter_crop_capture.mjs", str(output), "default"],
                               cwd=presenter_query.project, env=presenter_query.env,
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
    case = json.loads((output / "inspection.json").read_text())
    assert case["frames"] == [0, 3, 4, 5]
    assert len(list(output.glob("*.png"))) == 4
    params = case["props"]["timeline"]["clips"][0]["params"]
    assert "mouth" not in params
    size = tuple(case["size"])
    assert size == (640, 360)
    paths = [output / f"frame-{f}.png" for f in case["frames"]]
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    public = png_crop(public_box(case["rows"][0]), size)
    private_box = model.mouth_box(legacy_element(case), 0)
    assert private_box is not None, (
        "default-mouth source mismatch: registered default publishes a known frame-0 ROI, "
        "but the existing private default crop is absent; the smallest next correction "
        "is component-owned compatibility for the normal default constructor"
    )
    private = png_crop(private_box, size)
    assert private == public
    images = []
    for path in paths:
        with Image.open(path) as captured:
            assert captured.format == "PNG" and captured.size == size
            images.append(captured.convert("RGB"))
    assert all(image.crop(private).tobytes() == image.crop(public).tobytes() for image in images)
    private_fractions = [_diff_fraction(a.crop(private), b.crop(private))[0]
                         for a, b in zip(images, images[1:])]
    public_fractions = [_diff_fraction(a.crop(public), b.crop(public))[0]
                        for a, b in zip(images, images[1:])]
    assert private_fractions == public_fractions
    assert [fraction > .02 for fraction in private_fractions] == [fraction > .02 for fraction in public_fractions]
    assert any(fraction > .02 for fraction in private_fractions)
    assert {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths} == before
    print(json.dumps({"png_sha256": before, "crop": {"private": private, "public": public},
                      "natural_pairs": private_fractions}, sort_keys=True))
