"""Offline preparation checks. No browser, socket, renderStill or installs."""
import os
from pathlib import Path

import pytest
from PIL import Image

from tests.packs.rendering.intended_dip_fixture.proof import compare_frames, prepare_pair
from tests.packs.rendering.intended_dip_fixture.stage import locked_archive, stage

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.integration


def test_locked_main_and_unified_real_component_bodies_match(tmp_path):
    archive = locked_archive('/home/user/work/composition')
    projects, identities, inspections, props = prepare_pair(ROOT, tmp_path, archive)
    assert identities[0]['main_lock_verified'] is True
    assert identities[1]['main_lock_verified'] is False
    assert len(identities[1]['package_before']) == 77
    assert inspections[0]['props'] == inspections[1]['props'] == props
    assert all((project / 'src/Root.tsx').is_file() for project in projects)


def test_main_rejects_the_native8_archive(tmp_path):
    with pytest.raises(AssertionError):
        stage(ROOT, tmp_path, old_archive=(ROOT / 'remotion/artifacts/banodoco-timeline-composition-0.0.8.tgz').read_bytes(),
              public_archive=os.environ['ASTRID_COMPOSITION_TEST_ARTIFACT'],
              peers=os.environ['ASTRID_COMPOSITION_TEST_NODE_MODULES'])


def test_comparator_rejects_a_planted_change_outside_the_intended_window(tmp_path):
    old, new = tmp_path / 'main', tmp_path / 'unified'
    old.mkdir()
    new.mkdir()
    image = Image.new('RGB', (1920, 1080), (240, 240, 240))
    image.save(old / 'frame-0.png')
    image.putpixel((100, 100), (239, 240, 240))
    image.save(new / 'frame-0.png')
    with pytest.raises(AssertionError, match='unintended RGB difference at 0'):
        compare_frames(old, new, [], (21, 19, 17))
