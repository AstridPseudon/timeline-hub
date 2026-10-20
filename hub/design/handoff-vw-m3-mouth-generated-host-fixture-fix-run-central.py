"""READY only. Manager selects the committed source and grants this exact SHA."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

own = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-mouth-generated-host-fixture-fix')
orch = own.parents[1]
quiet = orch / 'managers/viewing/QUIET.md'
root = Path(os.environ['ASTRID_CHECKOUT']).resolve()
revision = os.environ['VIEWING_CROP_REVISION']
peers = Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')
node = Path('/tmp/vw-m3-agent-gate-node20.19.4/bin/node')
python = '/home/user/work/venv-agent/bin/python'
browser = Path('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux')
artifact = own.parent / 'vw-m3-opacity-package-ten/artifacts/banodoco-timeline-composition-0.0.10.tgz'


def guard():
    review = own / 'REVIEW.md'
    if review.is_file():
        print(review.read_text(), flush=True)
    if quiet.exists():
        (own / 'PAUSED_ACK').write_text(datetime.now(timezone.utc).isoformat() + ' CPU paused\n')
        sys.exit(75)
    assert review.is_file(), 'manager REVIEW.md approval required'
    assert f'APPROVED_SOURCE_SHA={revision}' in review.read_text().splitlines(), 'manager must approve exact source SHA'
    assert (own / 'READY_GRANTED').read_text().strip() == revision
    assert root == Path('/home/user/work/wt/vw-m3-mouth-generated-host-fixture-fix')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_state(path):
    # Include symlink targets and their contents, and refuse recursive links.
    result = {}

    def walk(directory, ancestors):
        real = directory.resolve()
        assert real not in ancestors, f'recursive dependency link: {directory}'
        for p in sorted(directory.iterdir()):
            key = str(p.relative_to(path))
            if p.is_symlink():
                result[key + ':link'] = str(p.resolve(strict=True))
            if p.is_dir():
                walk(p, ancestors | {real})
            elif p.is_file():
                result[key] = digest(p)
    walk(path, set())
    return result


def source_state():
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    assert head == revision and len(revision) == 40
    assert not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=root)
    assert len(subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], cwd=root).strip()) == 40
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    return {name: digest(root / name) for name in paths if name}


guard()
assert len(revision) == 40 and all(c in '0123456789abcdef' for c in revision)
# Only the central outer process owns the browser flock.
assert os.environ.get('VIEWING_BROWSER_FLOCK_HELD') == '1'
assert subprocess.run(['flock', '-n', '/tmp/timeline-viewing-browser.lock', 'true']).returncode != 0
assert digest(artifact) == 'cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7'
assert json.loads((peers / '@remotion/bundler/package.json').read_text())['version'] == '4.0.509'
six_peers = {
    '@remotion/player/dist/cjs/PlayerUI.js': '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
    '@remotion/player/dist/cjs/use-player-methods.js': 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
    '@remotion/player/dist/cjs/use-playback.js': '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
    '@remotion/player/dist/esm/index.mjs': 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
    'remotion/dist/esm/index.mjs': '9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8',
    'remotion/dist/cjs/audio/shared-audio-tags.js': '471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c',
}
assert {name: digest(peers / name) for name in six_peers} == six_peers
source_before = source_state()
graph_before = tree_state(peers)
tools_before = {str(p): digest(p) for p in (node, artifact,
    browser / 'headless_shell', Path(__file__), own / 'READY.sh', own / 'REVIEW.md', own / 'READY_GRANTED')}
browser_before = tree_state(browser)
scratch = Path(tempfile.mkdtemp(prefix='viewing-mouth-crop-central-'))
env = {k: v for k, v in os.environ.items() if k not in ('NODE_OPTIONS', 'NODE_PATH', 'PYTHONPYCACHEPREFIX')}
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(root),
    ASTRID_NODE_EXECUTABLE=str(node), ASTRID_COMPOSITION_TEST_ARTIFACT=str(artifact),
    ASTRID_COMPOSITION_TEST_NODE_MODULES=str(peers), VIEWING_CROP_CENTRAL='1',
    TMPDIR=str(scratch))
try:
    guard()
    # Exclusive one-shot claim: an old grant can never silently run twice.
    with (own / 'RUN_STARTED').open('x') as claim:
        claim.write(revision + '\n')
    command = [python, '-m', 'pytest', '-q', '-s', '-o', 'addopts=', '-p', 'no:cacheprovider',
               '--tb=short', 'tests/packs/rendering/presenter_crop_capture.py',
               '--basetemp=' + str(scratch / 'pytest')]
    print('SOURCE_SHA:', revision, flush=True)
    print('SOURCE_FILES:', len(source_before), 'DEPENDENCY_FILES:', len(graph_before), 'BROWSER_FILES:', len(browser_before), flush=True)
    print('COMMAND:', ' '.join(command), flush=True)
    result = subprocess.run(command, cwd=root, env=env)
    if result.returncode == 0:
        # Retain only the original four PNGs and inspection, outside the source.
        captures = sorted({p.resolve() for p in scratch.glob('pytest/**/capture/inspection.json')})
        assert len(captures) == 1
        capture = captures[0].parent
        evidence = own / 'evidence'
        evidence.mkdir(exist_ok=False)
        for name in ('inspection.json', 'frame-0.png', 'frame-3.png', 'frame-4.png', 'frame-5.png'):
            shutil.copyfile(capture / name, evidence / name)
            assert digest(evidence / name) == digest(capture / name)
        (evidence / 'sha256.json').write_text(json.dumps(
            {p.name: digest(p) for p in sorted(evidence.iterdir())}, indent=2) + '\n')
        print('EVIDENCE:', evidence, flush=True)
    sys.exit(result.returncode)
finally:
    try:
        assert source_state() == source_before
        assert tree_state(peers) == graph_before
        assert {name: digest(Path(name)) for name in tools_before} == tools_before
        assert tree_state(browser) == browser_before
        assert {name: digest(peers / name) for name in six_peers} == six_peers
        print('PASS: pre/post source, six peers, full dependency graph, browser and tool bytes unchanged', flush=True)
        guard()
    finally:
        shutil.rmtree(scratch)
