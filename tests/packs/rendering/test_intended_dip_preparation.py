"""Offline preparation checks. No browser, socket, renderStill or installs."""
import os
from pathlib import Path

import pytest
from PIL import Image

from tests.core.timeline.test_onscreen_more import _independent_fades_config
from tests.packs.rendering.intended_dip_fixture.proof import compare_frames, prepare_pair, run_node
from tests.packs.rendering.intended_dip_fixture.stage import FIXTURE, digest, locked_archive, stage

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.integration


@pytest.mark.parametrize('host', ['main', 'unified'])
def test_bundle_root_contains_the_original_declared_image_routes(tmp_path, host):
    project = tmp_path / host
    public = project / 'public'
    public.mkdir(parents=True)
    routes = {clip['params']['src'] for clip in _independent_fades_config()['clips']}
    assert routes == {'/plate.png', '/footage.png'}
    for route in routes:
        image = public / route.removeprefix('/')
        Image.new('RGB', (1920, 1080), (240, 240, 240)).save(image)
        assert digest(image) == '38e1647dbb753fa4956ed5f0d056c6c123019d93793455d4ee09db7d4dd31bf5'
    bundle = project / 'frame-bundle'
    bundle.mkdir()
    (bundle / 'index.html').write_text('original bundle entry')
    # Execute Remotion's real public-copy step, without webpack or a server.
    run_node(project, '--input-type=module', '-e', """
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [adapter, publicDir, bundle] = process.argv.slice(1);
const require = createRequire(import.meta.url);
const {copyDir} = require(path.join(process.env.ASTRID_COMPOSITION_TEST_NODE_MODULES,
  '@remotion/bundler/dist/copy-dir.js'));
await copyDir({src: publicDir, dest: path.join(bundle, 'public')});
assert.equal(existsSync(path.join(bundle, 'plate.png')), false);
assert.equal(existsSync(path.join(bundle, 'footage.png')), false);
const {exposeDeclaredImages} = await import(pathToFileURL(adapter).href);
exposeDeclaredImages(bundle);
""", FIXTURE / 'bundle-assets.mjs', public, bundle)
    assert {p.name for p in bundle.iterdir()} == {'index.html', 'public', 'plate.png', 'footage.png'}
    assert (bundle / 'index.html').read_text() == 'original bundle entry'
    for route in routes:
        name = route.removeprefix('/')
        assert (bundle / name).read_bytes() == (bundle / 'public' / name).read_bytes() == (public / name).read_bytes()


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
