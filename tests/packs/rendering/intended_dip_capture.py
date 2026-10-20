"""ONE central-only actual-pixel comparison, collected explicitly after grant.

MAIN 0.0.6 mounts custom clips opaque; unified 0.0.10 applies the owner's
v0.0.7 clip look. Independent clip fades intentionally DIP at frames 16–29.
This is a named behavior change, not an equivalence claim about old MAIN.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

from tests.packs.rendering.intended_dip_fixture.proof import compare_frames, prepare_pair, run_node
from tests.packs.rendering.intended_dip_fixture.stage import FIXTURE, digest, hashes, locked_archive
from tests.packs.rendering import test_am_coverage_equivalents as am_controls

am_coverage_query = am_controls.am_coverage_query
pytestmark = [pytest.mark.integration, pytest.mark.timeout(900)]


def test_main_opaque_vs_unified_intended_clip_look_dip_pixels(tmp_path, am_coverage_query):
    assert os.environ.get('VIEWING_INTENDED_DIP_CENTRAL') == '1', 'central grant required'
    assert os.environ.get('VIEWING_BROWSER_FLOCK_HELD') == '1'
    assert subprocess.run(['flock', '-n', '/tmp/timeline-viewing-browser.lock', 'true']).returncode != 0
    output = Path(os.environ['VIEWING_INTENDED_DIP_OUTPUT'])
    output.mkdir(exist_ok=False)
    archive = locked_archive('/home/user/work/composition')
    (output / 'main-locked-0.0.6.tar.gz').write_bytes(archive)
    projects, identities, inspections, props = prepare_pair(Path(os.environ['VIEWING_INTENDED_DIP_SOURCE']), tmp_path, archive)
    # Named positive and adjacent controls use the normal discovered registry
    # and real public query. No old strict-xfail waiver is involved.
    controls = {}

    def query_control(name):
        controls[name] = am_coverage_query(name)
        return controls[name]

    am_controls.test_actual_am_public_incoming_crossfade_stays_covered(query_control)
    am_controls.test_actual_am_one_sided_fade_has_dip_frames_then_coverage(query_control)
    (output / 'public-controls.json').write_text(json.dumps(controls, indent=2) + '\n')

    def staged_state(project):
        return {name: hashes(project.parent / name)
                for name in ('astrid', 'scripts', 'remotion/src', 'remotion/public',
                             'remotion/node_modules/@banodoco/timeline-composition')}

    before = [staged_state(project) for project in projects]
    for project in projects:
        shutil.copyfile(FIXTURE / 'frames.mjs', project / 'frames.mjs')
    project_list = tmp_path / 'projects.json'
    project_list.write_text(json.dumps([str(project) for project in projects]))
    observations = output / 'render-observations.json'
    try:
        run_node(projects[0], 'frames.mjs', project_list, observations, timeout=750)
    finally:
        # Retain original PNG bytes and hashes before pixel assertions, including
        # on failure. Never draw an oracle into or rewrite a captured PNG.
        for label, project, identity, inspection, staged_before in zip(
                ('main', 'unified'), projects, identities, inspections, before):
            target = output / label
            target.mkdir()
            pngs = sorted(project.glob('frame-*.png'))
            identity['captured_png_sha256'] = {p.name: digest(p) for p in pngs}
            for png in pngs:
                shutil.copyfile(png, target / png.name)
                assert digest(target / png.name) == digest(png)
            for name, sha in identity['input_png_sha256'].items():
                shutil.copyfile(project / 'public' / name, target / ('input-' + name))
                assert digest(target / ('input-' + name)) == sha
            (target / 'identity.json').write_text(json.dumps(identity, indent=2) + '\n')
            (target / 'inspection.json').write_text(json.dumps(inspection, indent=2) + '\n')
            staged_after = staged_state(project)
            (target / 'prepost.json').write_text(json.dumps({
                'before': staged_before, 'after': staged_after,
                'unchanged': staged_before == staged_after}, indent=2) + '\n')
            assert staged_before == staged_after
    observed = json.loads(observations.read_text())
    assert len(observed) == 2
    for row in observed:
        assert row['inputProps'] == props and row['compositionId'] == 'TimelineComposition'
        assert row['frames'] == list(range(45)) and row['errors'] == []
    background = tuple(bytes.fromhex(props['theme']['visual']['color']['bg'].removeprefix('#')))
    samples = compare_frames(output / 'main', output / 'unified', inspections[1]['answers'], background)
    (output / 'pixels.json').write_text(json.dumps(samples, indent=2) + '\n')
    assert len(list(output.glob('*/frame-*.png'))) == 90
