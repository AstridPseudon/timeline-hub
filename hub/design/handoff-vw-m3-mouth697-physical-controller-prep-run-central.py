"""One-shot central controller for the corrected partial-mouth extension."""
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
OWN = ORCH / 'workers/vw-m3-mouth697-physical-controller-prep'
ROOT = Path(os.environ['ASTRID_CHECKOUT']).resolve()
REVISION = os.environ['VIEWING_CROP_REVISION']
ARTIFACT = Path(os.environ['VIEWING_CROP_ARTIFACT']).resolve()
NODE = Path('/tmp/vw-m3-agent-gate-node20.19.4/bin/node')
PYTHON = Path('/home/user/work/venv-agent/bin/python')
BROWSER = Path('/opt/google/chrome/chrome')
PEERS = Path('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules')
LOCK = Path('/tmp/timeline-viewing-browser.lock')
FLOOR = 10 * 1024**3
TEMP_BUDGET = 512 * 1024**2
EXPECTED_ARTIFACT = '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
EXPECTED_NODE = '43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490'
EXPECTED_CHROME_TREE = '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e'
EXPECTED_GRAPH_COUNT = 21488
EXPECTED_GRAPH_TREE = '9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425'
EXPECTED_GRAPH_REVISION = 'f8164bef73215272562c4d6974acadbd82c2898a'
EXPECTED_SOURCE_REVISION = 'ee71010a0947edcbbacbf8178e5fee11ab6bab3d'

SOURCE_HASHES = {
    'astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/component.tsx': 'b1dea928a4c709e1148525ceb88c704952b93fdf6f2b89c49e6e668afb7e84cc',
    'astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/motion.ts': '00b60482093b5f5ead7179bd81689afcc671502f40f38059432d5087634c7701',
    'astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/scene.ts': '4cde365dd358ac02eafca9a59f565a96fe8e204f68b955b51c6b260441e46e50',
    'astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/element.yaml': '7bbcb59775818bda4d0cdc58e364256139d904901ce87bcc7263c8ee80afe156',
    'tests/packs/rendering/presenter_scene_capability.mjs': 'c8c6d64e258bb7069ea8e4daaf6aa13aae951dc6d79640e0f97ff57a36a379b0',
    'tests/packs/rendering/test_presenter_scene_capability.py': 'bbe8feb39d0580295af82582b94e2778063f207dc4ba106559dffef5789b5a43',
    'astrid/packs/astrid_motion/pack.yaml': '064d7450d0ce3f2c6eac73c3d0ac2517a0ea6bdca4993134dd672f8ad5c556e1',
    'remotion/src/host-registries.ts': '16cb1c2068e6643edca57e89dc155f757418676adab6658192539ed7036b83df',
}

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
    result: dict[str, str] = {}

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


def graph_state(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}

    def walk(directory: Path, ancestors: set[Path]) -> None:
        real = directory.resolve()
        assert real not in ancestors, f'recursive link: {directory}'
        for item in sorted(directory.iterdir()):
            key = str(item.relative_to(path))
            if item.is_symlink():
                result[key + '@link'] = os.readlink(item)
            if item.is_dir():
                walk(item, ancestors | {real})
            else:
                assert item.is_file(), f'nonregular dependency: {item}'
                result[key] = digest(item)

    walk(path, set())
    return result


def chrome_tree(path: Path) -> tuple[str, int]:
    entries = []
    for item in sorted(path.rglob('*')):
        name = str(item.relative_to(path))
        if item.is_symlink():
            entries.append([name, 'symlink', hashlib.sha256(os.readlink(item).encode()).hexdigest()])
        elif item.is_file():
            entries.append([name, 'executable' if item.stat().st_mode & 0o111 else 'file', digest(item)])
        else:
            assert item.is_dir(), f'unsupported Chrome tree member: {item}'
    payload = json.dumps(entries, separators=(',', ':'), ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest(), len(entries)


def source_state() -> dict[str, str]:
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    assert head == REVISION and len(REVISION) == 40
    assert subprocess.run(['git', 'merge-base', '--is-ancestor', EXPECTED_SOURCE_REVISION, REVISION], cwd=ROOT).returncode == 0
    assert {name: digest(ROOT / name) for name in SOURCE_HASHES} == SOURCE_HASHES
    assert not subprocess.check_output(
        ['git', 'status', '--porcelain', '--untracked-files=all'], cwd=ROOT
    )
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    return {name: digest(ROOT / name) for name in names if name}


def check_space() -> None:
    free = shutil.disk_usage('/tmp').free
    assert free >= FLOOR + TEMP_BUDGET, f'10GiB floor + temp budget: {free}'


def guard() -> None:
    assert not (ORCH / 'managers/viewing/QUIET.md').exists()
    assert (OWN / 'REVIEW.md').is_file()
    assert f'APPROVED_SOURCE_SHA={REVISION}' in (OWN / 'REVIEW.md').read_text().splitlines()
    assert (OWN / 'READY_GRANTED').read_text().strip() == REVISION
    assert ROOT.is_dir() and NODE.is_file() and PYTHON.is_file() and BROWSER.is_file()
    assert ARTIFACT.is_file() and digest(ARTIFACT) == EXPECTED_ARTIFACT
    with tarfile.open(ARTIFACT) as archive:
        assert len([item for item in archive.getmembers() if item.isfile()]) == 77
    assert subprocess.check_output(
        ['dpkg-query', '-W', '-f=${Version}', 'google-chrome-stable'], text=True
    ).strip() == '155.0.8059.84-1'
    assert digest(NODE) == EXPECTED_NODE
    assert {name: digest(PEERS / name) for name in SIX_PEERS} == SIX_PEERS
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=PEERS.parent, text=True).strip() == EXPECTED_GRAPH_REVISION
    graph = graph_state(PEERS)
    assert len(graph) == EXPECTED_GRAPH_COUNT
    payload = json.dumps(graph, sort_keys=True, separators=(',', ':')).encode()
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_GRAPH_TREE
    chrome_hash, chrome_count = chrome_tree(BROWSER.parent)
    assert (chrome_hash, chrome_count) == (EXPECTED_CHROME_TREE, 255)
    assert os.environ.get('VIEWING_BROWSER_FLOCK_HELD') == '1'
    assert subprocess.run(['flock', '-n', str(LOCK), 'true']).returncode != 0
    check_space()


guard()
with (OWN / 'RUN_STARTED').open('x') as claim:
    claim.write(REVISION + '\n')
source_before = source_state()
peers_before = tree_state(PEERS)
browser_before = tree_state(BROWSER.parent)
tools_before = {str(path): digest(path) for path in (NODE, ARTIFACT, Path(__file__))}
scratch = Path(tempfile.mkdtemp(prefix='vw-mouth697-', dir='/tmp'))
assert scratch.stat().st_mode & 0o777 == 0o700
env = {key: value for key, value in os.environ.items()
       if key not in {'NODE_OPTIONS', 'NODE_PATH', 'PYTHONPYCACHEPREFIX'}}
env.update(
    PYTHONPATH=str(ROOT),
    ASTRID_NODE_EXECUTABLE=str(NODE),
    ASTRID_COMPOSITION_TEST_ARTIFACT=str(ARTIFACT),
    ASTRID_COMPOSITION_TEST_NODE_MODULES=str(PEERS),
    ASTRID_CROP_BROWSER=str(BROWSER),
    TMPDIR=str(scratch),
    XDG_CACHE_HOME=str(scratch / 'cache'),
)
command = [str(PYTHON), '-m', 'pytest', '-q', '-s', '-o', 'addopts=', '-p', 'no:cacheprovider',
           '--tb=short', 'tests/packs/rendering/test_presenter_crop_partial_physical.py',
           '--basetemp=' + str(scratch / 'pytest')]
try:
    result = subprocess.run(command, cwd=ROOT, env=env)
    raise SystemExit(result.returncode)
finally:
    assert source_state() == source_before
    assert tree_state(PEERS) == peers_before
    assert tree_state(BROWSER.parent) == browser_before
    assert {name: digest(Path(name)) for name in tools_before} == tools_before
    shutil.rmtree(scratch)
