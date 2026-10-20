#!/usr/bin/env python3
"""Offline preparation for the unchanged four-case gate; no launch authority."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tarfile

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-current-frame-cohort-ready'
APP = Path('/home/user/work/wt/vw-m3-current-frame-cohort-ready')
PRIVATE = ORCH / 'workers/vw-m3-app-private12-clean-install/clean-project'
NODE = Path('/tmp/vw-m3-agent-gate-node20.19.4/bin/node')
AGENT = Path('/home/user/work/wt/app-m3-agent013-current-pair-source')
RUNTIME = Path('/home/user/work/wt/rt-m2-pin-2c4ac180')
REMOTION = Path('/home/user/work/runtimes/agent-remotion-current')
ARTIFACT = '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
PEERS = [
    'remotion/dist/cjs/audio/shared-audio-tags.js', 'remotion/dist/esm/index.mjs',
    '@remotion/player/dist/cjs/use-player-methods.js', '@remotion/player/dist/esm/index.mjs',
    '@remotion/player/dist/cjs/use-playback.js', '@remotion/player/dist/cjs/PlayerUI.js',
]


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stdin=subprocess.DEVNULL).decode().strip()


def inventory(root):
    rows = []
    for directory, folders, files in os.walk(root, followlinks=False):
        for name in sorted(folders + files):
            path = Path(directory) / name
            info = path.lstat()
            row = {'path': path.relative_to(root).as_posix(), 'mode': stat.S_IMODE(info.st_mode)}
            if path.is_symlink():
                row.update(kind='symlink', target=os.readlink(path), sha256=digest(os.readlink(path).encode()))
            elif stat.S_ISDIR(info.st_mode):
                row['kind'] = 'directory'
            else:
                assert stat.S_ISREG(info.st_mode), path
                row.update(kind='executable' if info.st_mode & 0o111 else 'file', bytes=info.st_size,
                           sha256=file_hash(path), device=info.st_dev, inode=info.st_ino, links=info.st_nlink)
            rows.append(row)
    return sorted(rows, key=lambda row: row['path'])


def source(root):
    if not root.exists():
        return {'root': str(root), 'available': False}
    names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others',
                                     '--exclude-standard'], stdin=subprocess.DEVNULL).decode().split('\0')
    rows = []
    for name in sorted(set(filter(None, names))):
        path = root / name
        rows.append([name, 'symlink' if path.is_symlink() else 'executable' if path.stat().st_mode & 0o111 else 'file',
                     digest(os.readlink(path).encode()) if path.is_symlink() else file_hash(path)])
    return {'root': str(root), 'available': True, 'head': git(root, 'rev-parse', 'HEAD'),
            'tree': git(root, 'rev-parse', 'HEAD^{tree}'), 'status': git(root, 'status', '--porcelain'),
            'files': rows, 'sha256': digest(compact(rows))}


def write(suffix, data):
    Path(str(PREFIX) + suffix).write_text(json.dumps(data, indent=2) + '\n')


def prepare(boundary):
    assert not (ORCH / 'managers/viewing/QUIET.md').exists(), 'QUIET: preparation held'
    assert os.statvfs(APP).f_bavail * os.statvfs(APP).f_frsize >= 10 * 1024**3, '10 GiB floor'
    assert (APP / 'node_modules').resolve() == PRIVATE / 'node_modules'
    expected = json.loads((ORCH / 'design/handoff-vw-m3-app-private12-clean-install-manifest.json').read_text())
    graph = inventory(PRIVATE / 'node_modules')
    expected_graph = sorted([
        {**row, 'path': row['path'][len('node_modules/'):]} for row in expected['entries']
        if row['path'].startswith('node_modules/')
    ], key=lambda row: row['path'])
    assert graph == expected_graph, 'whole private graph differs from fresh installer manifest'
    archive = APP / 'vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz'
    assert file_hash(archive) == ARTIFACT
    with tarfile.open(archive) as tar:
        members = [member for member in tar.getmembers() if member.isfile()]
        assert len(members) == 77 and len({member.name for member in members}) == 77
        composition = []
        for member in members:
            assert member.name.startswith('package/') and '..' not in Path(member.name).parts
            name = member.name[len('package/'):]
            expected_hash = digest(tar.extractfile(member).read())
            assert file_hash(PRIVATE / 'node_modules/@banodoco/timeline-composition' / name) == expected_hash
            composition.append([name, expected_hash])
    installed = inventory(PRIVATE / 'node_modules/@banodoco/timeline-composition')
    assert sorted(row['path'] for row in installed if row['kind'] != 'directory') == sorted(row[0] for row in composition)
    for name in ['package.json', 'package-lock.json']:
        assert (APP / name).read_bytes() == (PRIVATE / name).read_bytes(), name
    peers = {name: file_hash(PRIVATE / 'node_modules' / name) for name in PEERS}
    chrome = inventory(Path('/opt/google/chrome'))
    export_browser = inventory(Path('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux'))
    assert file_hash(Path('/opt/google/chrome/chrome')) == 'cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76'
    assert file_hash(Path('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell')) == '63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4'
    sources = {name: source(root) for name, root in {
        'app': APP, 'publishedAgent': AGENT, 'publishedRuntime': RUNTIME,
        'observedAgentMirrorOnly': Path('/home/user/work/agent'),
        'observedRuntimeMirrorOnly': Path('/home/user/work/runtime'),
        'composition': Path('/home/user/work/composition'),
    }.items()}
    environment = {
        'controllerSha256': file_hash(Path(__file__)),
        'offlineRunnerSha256': file_hash(ORCH / 'workers/vw-m3-current-frame-cohort-ready/run-offline.py'),
        'app': str(APP), 'privateGraph': str(PRIVATE / 'node_modules'),
        'node': {'path': str(NODE), 'sha256': file_hash(NODE)},
        'config': str(APP / 'playwright.viewing-parity.normal-profile-native1920.config.ts'),
        'sourceTuple': None, 'publishedAgent': str(AGENT), 'publishedRuntime': str(RUNTIME),
        'remotionProject': {'path': str(REMOTION), 'available': REMOTION.exists()},
        'agentPython': '/home/user/work/venv-agent/bin/python',
        'runtimePython': '/home/user/work/venv-runtime/bin/python',
        'composition77': sorted(composition), 'appSixPeers': peers,
        'agentSixPeers': None, 'wholePrivateGraphHash': digest(compact(graph)),
        'chromeGraphHash': digest(compact(chrome)), 'exportBrowserGraphHash': digest(compact(export_browser)),
        'appSourceHash': sources['app']['sha256'],
        'publishedAgentCommit': 'd8749a9ce12a699672faf3ad96b4e4cbea9245c2',
        'runtimeProducerCommit': '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
        'sourceObservations': {name: {key: value for key, value in data.items() if key != 'files'}
                               for name, data in sources.items()},
        'actualRun': False, 'managerFreeze': False,
    }
    write(f'-{boundary}-graph.json', graph)
    write(f'-{boundary}-browser.json', {'chrome': chrome, 'export': export_browser})
    write(f'-{boundary}-sources.json', sources)
    write(f'-{boundary}-environment.json', environment)
    write(f'-{boundary}-resources.json', {
        'quietAbsent': True, 'diskFloorBytes': 10 * 1024**3,
        'diskFreeBytes': os.statvfs(APP).f_bavail * os.statvfs(APP).f_frsize,
        'actualRun': False, 'flockRequiredForActualRun': '/tmp/timeline-viewing-browser.lock',
    })
    print(json.dumps({'boundary': boundary, 'EnvHash': digest(compact(environment)), 'graphEntries': len(graph),
                      'compositionFiles': len(composition), 'appPeerFiles': len(peers), 'actualRun': False}))


if __name__ == '__main__':
    if sys.argv[1:] == ['--run']:
        print('BLOCKED: no manager freeze; fixture seeds through the legacy compatibility publication writer '
              'before authoring startup, which this task forbids. No live refusal was observed. '
              'Retained fixture, approved current Agent launcher and current private Remotion graph are pending. '
              'No launch attempted.', file=sys.stderr)
        sys.exit(78)
    assert sys.argv[1:] in [['--prepare', 'pre'], ['--prepare', 'post']]
    prepare(sys.argv[2])
