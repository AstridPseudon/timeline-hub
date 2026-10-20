"""Shared preparation and strict assertions for the intended clip-look change."""
import hashlib
import json
import os
import shutil
import signal
import subprocess

from PIL import Image, ImageChops

from astrid.core.theme import builtin_theme
from tests.core.timeline.test_onscreen_more import _independent_fades_config
from .stage import FIXTURE, FILM_SHA256, digest, stage


def run_node(project, script, *args, timeout=90):
    env = {k: v for k, v in os.environ.items() if k not in ('NODE_OPTIONS', 'NODE_PATH')}
    process = subprocess.Popen([os.environ['ASTRID_NODE_EXECUTABLE'], script, *map(str, args)],
                               cwd=project, env=env, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
        raise
    assert process.returncode == 0, stdout + stderr


def prepare_pair(root, temporary, old_archive):
    film = _independent_fades_config()
    assert hashlib.sha256(json.dumps(film, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == FILM_SHA256
    props = {'timeline': film, 'assets': {'assets': {}}, 'theme': builtin_theme()}
    projects, identities, inspections = [], [], []
    for label in ('main', 'unified'):
        project, identity = stage(root, temporary / label,
            old_archive=old_archive if label == 'main' else None,
            public_archive=os.environ['ASTRID_COMPOSITION_TEST_ARTIFACT'],
            peers=os.environ['ASTRID_COMPOSITION_TEST_NODE_MODULES'])
        (project / 'props.json').write_text(json.dumps(props))
        # Deterministic image fixture bytes at the original two paths. The
        # authored film and the empty libraryAsset registry remain identical.
        for name in ('plate.png', 'footage.png'):
            Image.new('RGB', (1920, 1080), (240, 240, 240)).save(project / 'public' / name)
        identity['input_png_sha256'] = {name: digest(project / 'public' / name)
                                        for name in ('plate.png', 'footage.png')}
        shutil.copyfile(FIXTURE / 'inspect.mjs', project / 'inspect.mjs')
        run_node(project, 'inspect.mjs', label)
        inspection = json.loads((project / 'inspection.json').read_text())
        assert inspection['props'] == props
        identity['transitive_bundle_inputs_sha256'] = {
            name: digest(project / name.split('?', 1)[0]) for name in inspection['inputs']}
        projects.append(project)
        identities.append(identity)
        inspections.append(inspection)
    assert identities[0]['input_png_sha256'] == identities[1]['input_png_sha256']
    # Complete actual component markup for both clips, all 30 local frames.
    # This checks helper/field extraction semantically, without source-shape
    # substitutions or a replacement drawing component.
    assert inspections[0]['bodies'] == inspections[1]['bodies']
    for frame in range(45):
        markup = inspections[0]['html'][str(frame)]
        assert markup.count('<img ') == (2 if 15 <= frame < 30 else 1)
    answers = inspections[1]['answers']
    assert [row['coverage'] for row in answers[:45]] == ['COVERED'] * 16 + ['DIP'] * 14 + ['COVERED'] * 15
    for frame, row in enumerate(answers[:45]):
        expected_ids = ['out'] if frame < 15 else ['out', 'in'] if frame < 30 else ['in']
        assert [layer['clipId'] for layer in row['layers']] == expected_ids
        for layer in row['layers']:
            assert layer['fullFrame'] is True and layer['opaqueSupport'] == 'rect'
            assert layer['bounds']['rect'] == {'x': 0, 'y': 0, 'width': 1920, 'height': 1080}
            assert layer['findings'] == []
    assert [layer['opacity'] for layer in answers[15]['layers']] == [1, 0]
    assert answers[30]['layers'][0]['opacity'] == 1
    assert answers[45]['layers'] == [] and answers[45]['coverage'] == 'GAP'
    return projects, identities, inspections, props


def expected_rgb(background, layers):
    # Source-over on the two opaque 240-grey image fields, using the public
    # renderer's opacity facts and 8-bit alpha. This is an exact integer check;
    # no added pixel tolerance or relaxed difference-fraction threshold.
    color = background
    for layer in layers:
        alpha = int(layer['opacity'] * 255 + 0.5)
        color = tuple((240 * alpha + channel * (255 - alpha) + 127) // 255 for channel in color)
    return color


def compare_frames(main, unified, answers, background):
    samples = {}
    for frame in range(45):
        with Image.open(main / f'frame-{frame}.png') as old_image, Image.open(unified / f'frame-{frame}.png') as new_image:
            assert old_image.size == new_image.size == (1920, 1080)
            old, new = old_image.convert('RGB'), new_image.convert('RGB')
            assert old.getextrema() == ((240, 240),) * 3, f'MAIN must be opaque at {frame}'
            difference = ImageChops.difference(old, new)
            if frame not in range(16, 30):
                assert difference.getbbox() is None, f'unintended RGB difference at {frame}'
            else:
                color = expected_rgb(background, answers[frame]['layers'])
                assert new.getextrema() == tuple((channel, channel) for channel in color), (
                    frame, new.getextrema(), color)
                assert difference.getbbox() == (0, 0, 1920, 1080)
                assert all(min(bg, 240) < channel < max(bg, 240) for bg, channel in zip(background, color))
            samples[frame] = {'main_extrema': old.getextrema(), 'unified_extrema': new.getextrema(),
                              'difference_bounds': difference.getbbox()}
    return samples
