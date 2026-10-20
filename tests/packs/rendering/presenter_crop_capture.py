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
    new = png_crop(public_box(case["rows"][0]), size)
    assert (area(old), area(new)) == (799, 387)
    images = []
    for path in paths:
        with Image.open(path) as captured:
            assert captured.format == "PNG" and captured.size == size
            images.append(captured.convert("RGB"))
    # Positive: the same unaltered captured PNG through each crop/comparator.
    # Every captured pose retains a nonempty footprint; no placeholder image.
    for image, row in zip(images, case["rows"]):
        assert png_crop(public_box(row), size) == new
        for crop in (old, new):
            region = image.crop(crop)
            assert _diff_fraction(region, region.copy())[0] == 0
    fractions = {"old": [], "public": []}
    for a, b in zip(images, images[1:]):
        for label, crop in (("old", old), ("public", new)):
            fractions[label].append(_diff_fraction(a.crop(crop), b.crop(crop))[0])
    assert any(f > .02 for f in fractions["old"]), fractions
    assert any(f > .02 for f in fractions["public"]), fractions
    assert [f > .02 for f in fractions["old"]] == [f > .02 for f in fractions["public"]]

    # Negative control uses a COPY of a real PNG. Exactly eight bright/dark
    # pixels in the overlap change above CHANGE_LEVEL: opposite 2% verdicts.
    planted = images[0].copy()
    for x in range(new[0] + 2, new[0] + 10):
        point = (x, new[1] + 2)
        original = planted.getpixel(point)
        planted.putpixel(point, (255, 255, 255) if sum(original) < 384 else (0, 0, 0))
    negative = {}
    for label, crop in (("old", old), ("public", new)):
        negative[label] = _diff_fraction(images[0].crop(crop), planted.crop(crop))[0]
        assert negative[label] == 8 / area(crop)
    assert negative["old"] <= .02 < negative["public"]
    # A larger planted defect is caught by BOTH unchanged comparators.
    for x in range(new[0] + 2, new[0] + 22):
        point = (x, new[1] + 2)
        original = images[0].getpixel(point)
        planted.putpixel(point, (255, 255, 255) if sum(original) < 384 else (0, 0, 0))
    for crop in (old, new):
        assert _diff_fraction(images[0].crop(crop), planted.crop(crop))[0] == 20 / area(crop)
        assert 20 / area(crop) > .02
    assert {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths} == before
    print(json.dumps({"png_sha256": before, "crop": {"old": old, "public": new},
                      "natural_pairs": fractions, "eight_pixel_negative": negative}, sort_keys=True))
