"""Run the retained, unapplied pixel proposal on this worktree without capture."""
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path('/home/user/work/wt/vw-m3-mouth-series-current-port')
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
DESIGN = ORCH / 'design'
PREFIX = 'handoff-vw-m3-mouth-series-current-port-'
ARCHIVE = ORCH / 'artifacts/viewing-mouth-legacy-public-four-stills-v1.tgz'
assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() == 'e7f32e40aa1aa25d81f30d05fd5ccb83a8a19cd8ce4a5a560e9fd93dc73d7c39'
version = sys.argv[1]
assert version in ('10', '12')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT),
           ASTRID_NODE_EXECUTABLE='/tmp/vw-m3-agent-gate-node20.19.4/bin/node',
           ASTRID_COMPOSITION_TEST_NODE_MODULES='/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')
for key in ('NODE_OPTIONS', 'NODE_PATH', 'ASTRID_COMPOSITION_TEST_ARTIFACT'):
    env.pop(key, None)
if version == '12':
    env['ASTRID_COMPOSITION_TEST_ARTIFACT'] = str(ORCH / 'artifacts/banodoco-timeline-composition-0.0.12.tgz')
with tempfile.TemporaryDirectory(prefix='.mouth-series-check-', dir=ROOT) as temporary:
    stage = Path(temporary)
    tests = stage / 'tests/packs/rendering'
    tests.mkdir(parents=True)
    fixture = stage / 'tests/fixtures/presenter_selected_cut'
    fixture.mkdir(parents=True)
    with tarfile.open(ARCHIVE) as archive:
        archive.extractall(fixture, filter='data')
    shutil.copyfile(DESIGN / 'handoff-vw-m3-mouth-selected-cut-aggregate-fixture-test_presenter_selected_cut_aggregate.py',
                    tests / 'test_presenter_selected_cut_aggregate.py')
    query = (DESIGN / (PREFIX + 'fixture-presenter_selected_cut_query.mjs') if version == '12' else
             DESIGN / 'handoff-vw-m3-mouth-selected-cut-aggregate-fixture-presenter_selected_cut_query.mjs')
    shutil.copyfile(query, tests / 'presenter_selected_cut_query.mjs')
    result = subprocess.run(['/home/user/work/venv-agent/bin/python', '-m', 'pytest', '-q', '-s',
                             '-c', str(ROOT / 'pyproject.toml'), '-o', 'addopts=', '-p', 'no:cacheprovider',
                             '--tb=short', str(tests / 'test_presenter_selected_cut_aggregate.py')],
                            cwd=ROOT, env=env, check=False)
raise SystemExit(result.returncode)
