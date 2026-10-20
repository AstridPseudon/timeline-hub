"""One-shot central controller for the default/partial mouth extension."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
OWN = ORCH / 'workers/vw-m3-mouth-default-partial-physical-prep'
ROOT = Path(os.environ['ASTRID_CHECKOUT']).resolve()
REVISION = os.environ['VIEWING_CROP_REVISION']
ARTIFACT = Path(os.environ['VIEWING_CROP_ARTIFACT']).resolve()
NODE = Path('/tmp/vw-m3-agent-gate-node20.19.4/bin/node')
PYTHON = Path('/home/user/work/venv-agent/bin/python')
BROWSER = Path('/opt/google/chrome/chrome')
PEERS = Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')
LOCK = Path('/tmp/timeline-viewing-browser.lock')

SIX_PEERS = {
    '@remotion/player/dist/cjs/PlayerUI.js': '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
    '@remotion/player/dist/cjs/use-player-methods.js': 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
    '@remotion/player/dist/cjs/use-playback.js': '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
    '@remotion/player/dist/esm/index.mjs': 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
    'remotion/dist/esm/index.mjs': '9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8',
    'remotion/dist/cjs/audio/shared-audio-tags.js': '471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c',
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_state(path: Path) -> dict[str, str]:
    result = {}

    def walk(directory: Path, ancestors: set[Path]) -> None:
        real = directory.resolve()
        assert real not in ancestors, f'recursive link: {directory}'
        for item in sorted(directory.iterdir()):
            key = str(item.relative_to(path))
            if item.is_symlink():
                result[key + ':link'] = str(item.resolve(strict=True))
            if item.is_dir():
                walk(item, ancestors | {real})
            elif item.is_file():
                result[key] = digest(item)

    walk(path, set())
    return result


def source_state() -> dict[str, str]:
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    assert head == REVISION and len(REVISION) == 40
    assert not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=ROOT)
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    return {name: digest(ROOT / name) for name in names if name}


def guard() -> None:
    assert (OWN / 'REVIEW.md').is_file()
    review = (OWN / 'REVIEW.md').read_text()
    assert f'APPROVED_SOURCE_SHA={REVISION}' in review.splitlines()
    assert (OWN / 'READY_GRANTED').read_text().strip() == REVISION
    assert ROOT.is_dir() and NODE.is_file() and PYTHON.is_file() and BROWSER.is_file()
    assert ARTIFACT.is_file() and digest(ARTIFACT) == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
    with tarfile.open(ARTIFACT) as archive:
        assert len([item for item in archive.getmembers() if item.isfile()]) == 77
    assert subprocess.check_output(['dpkg-query', '-W', '-f=${Version}', 'google-chrome-stable'], text=True).strip() == '155.0.8059.84-1'
    assert digest(NODE) == '43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490'
    assert {name: digest(PEERS / name) for name in SIX_PEERS} == SIX_PEERS
    assert os.environ.get('VIEWING_BROWSER_FLOCK_HELD') == '1'
    assert subprocess.run(['flock', '-n', str(LOCK), 'true']).returncode != 0


guard()
with (OWN / 'RUN_STARTED').open('x') as claim:
    claim.write(REVISION + '\n')
source_before = source_state()
peers_before = tree_state(PEERS)
browser_before = tree_state(BROWSER.parent)
scratch = Path(tempfile.mkdtemp(prefix='vw-mouth-default-partial-', dir='/tmp'))
env = {key: value for key, value in os.environ.items() if key not in {'NODE_OPTIONS', 'NODE_PATH', 'PYTHONPYCACHEPREFIX'}}
env.update(
    PYTHONPATH=str(ROOT),
    ASTRID_NODE_EXECUTABLE=str(NODE),
    ASTRID_COMPOSITION_TEST_ARTIFACT=str(ARTIFACT),
    ASTRID_COMPOSITION_TEST_NODE_MODULES=str(PEERS),
    ASTRID_CROP_BROWSER=str(BROWSER),
    TMPDIR=str(scratch),
)
command = [str(PYTHON), '-m', 'pytest', '-q', '-s', '-o', 'addopts=', '-p', 'no:cacheprovider',
           '--tb=short', 'tests/packs/rendering/test_presenter_crop_default_partial_physical.py',
           '--basetemp=' + str(scratch / 'pytest')]
try:
    result = subprocess.run(command, cwd=ROOT, env=env)
    raise SystemExit(result.returncode)
finally:
    assert source_state() == source_before
    assert tree_state(PEERS) == peers_before
    assert tree_state(BROWSER.parent) == browser_before
    shutil.rmtree(scratch)
