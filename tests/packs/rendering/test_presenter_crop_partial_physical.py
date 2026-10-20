"""Central-only pixel equivalence for the raw partial-mouth input.

The default and malformed cases are source-only registered tests. This test
captures only the two approved partial frames and does not fabricate a
positive for an absent mouth.
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
def test_actual_registered_partial_mouth_crop_pixels(presenter_query, tmp_path):
    assert os.environ.get("VIEWING_CROP_CENTRAL") == "1", "central READY grant required"
    assert subprocess.run(["flock", "-n", "/tmp/timeline-viewing-browser.lock", "true"]).returncode != 0
    stage_geometry(presenter_query)
    for name in ("presenter_crop_entry.mjs", "presenter_crop_partial_capture.mjs"):
        shutil.copyfile(Path(__file__).with_name(name), presenter_query.project / name)
    output = tmp_path / "capture"
    output.mkdir()
    process = subprocess.Popen(
        [str(presenter_query.node), "presenter_crop_partial_capture.mjs", str(output)],
        cwd=presenter_query.project,
        env={**presenter_query.env, "ASTRID_CROP_BROWSER": "/opt/google/chrome/chrome"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
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
    assert case["frames"] == [0, 3]
    assert len(list(output.glob("*.png"))) == 2
    size = tuple(case["size"])
    assert size == (640, 360)
    paths = [output / f"frame-{frame}.png" for frame in case["frames"]]
    before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    old = png_crop(model.mouth_box(legacy_element(case), 0), size)
    compat = png_crop(public_box(case["rows"][0]), size)
    erase = png_crop(public_box(case["rows"][0], "erase"), size)
    assert old == compat == (298, 202, 339, 219)
    assert erase == (300, 206, 343, 215)
    assert (area(old), area(compat), area(erase)) == (697, 697, 387)
    assert len(case["rows"]) == 1
    assert case["rows"][0]["componentFrame"] == 0
    assert case["rows"][0]["clipId"] == "presenter"
    crops = {"old": old, "compat": compat}
    images = []
    for path in paths:
        with Image.open(path) as captured:
            assert captured.format == "PNG" and captured.size == size
            images.append(captured.convert("RGB"))
    for image in images:
        assert image.crop(old).tobytes() == image.crop(compat).tobytes()
        assert _diff_fraction(image.crop(old), image.crop(compat))[0] == 0
    fractions = {
        label: [_diff_fraction(first.crop(crop), second.crop(crop))[0]
                for first, second in zip(images, images[1:])]
        for label, crop in crops.items()
    }
    assert fractions["old"] == fractions["compat"]

    planted = images[0].copy()
    points = [(old[0] + 2 + index, old[1] + 2) for index in range(20)]
    for point in points:
        original = images[0].getpixel(point)
        planted.putpixel(point, (255, 255, 255) if sum(original) < 384 else (0, 0, 0))
    negative = {
        label: _diff_fraction(images[0].crop(crop), planted.crop(crop))[0]
        for label, crop in crops.items()
    }
    assert negative == {"old": 20 / 697, "compat": 20 / 697}
    assert negative["old"] > 0.02
    assert {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths} == before
