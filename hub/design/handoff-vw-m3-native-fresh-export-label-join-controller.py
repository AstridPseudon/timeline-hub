"""Offline fingerprinting and manager-reviewed, central-only one-frame command.

No packages are installed. Every render-writable input is copied privately.
The native host must carry its existing explicit browser selector; no alias or
replacement launcher is supplied here.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
WORKER = 'vw-m3-native-fresh-export-label-join'
WORK = ORCH / 'workers' / WORKER
PREFIX = ORCH / 'design' / ('handoff-' + WORKER)
BASE = 'd93b4ff6a'
RUNTIME = '2c4ac180c2220bdad966bc01e95ad230e99ce26a'
RUNTIME_ARCHIVE = 'eed22a1b0d1af2045f823ec9f71dbd7cd862ba7935edfd5199171656e3ff1669'
PEERS = Path('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules')
PUBLIC = '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
NODE = '43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490'
CHROME = Path('/opt/google/chrome/chrome')
PYTHON = Path('/home/user/work/venv-agent/bin/python')
TEST = 'tests/packs/rendering/test_native_fresh_export_label.py::test_one_fresh_saved_frame_exports_retained_revision'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def manifest(root):
    return {str(p.relative_to(root)): ('link:' + os.readlink(p)) if p.is_symlink() else sha(p.read_bytes())
            for p in sorted(root.rglob('*')) if (p.is_file() or p.is_symlink()) and '__pycache__' not in p.parts}


def browser_tree():
    entries = []
    for p in sorted(CHROME.parent.rglob('*')):
        name = str(p.relative_to(CHROME.parent))
        if p.is_symlink():
            entries.append([name, 'symlink', sha(os.readlink(p).encode())])
        elif p.is_file():
            entries.append([name, 'executable' if p.stat().st_mode & 0o111 else 'file', sha(p.read_bytes())])
    return {'sha256': sha(json.dumps(entries, separators=(',', ':')).encode()), 'fileCount': len(entries)}


def inventory(root):
    baseline = json.loads((ORCH / 'design/handoff-vw-m3-live-source-label-native-join-qualified-pre.json').read_text())
    assert subprocess.check_output(['git', '-C', str(PEERS.parent.parent), 'rev-parse', 'HEAD']).decode().strip() == 'f8164bef73215272562c4d6974acadbd82c2898a'
    peers = manifest(PEERS)
    assert peers == baseline['peer_graph'], 'clean f816 graph changed'
    artifact = root / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
    assert sha(artifact.read_bytes()) == PUBLIC
    with tarfile.open(artifact) as archive:
        public = {m.name.removeprefix('package/'): sha(archive.extractfile(m).read()) for m in archive if m.isfile()}
    assert len(public) == 77 and public == baseline['public12']
    with tarfile.open('/tmp/node-v20.19.4-linux-x64.tar.xz') as archive:
        node = archive.extractfile('node-v20.19.4-linux-x64/bin/node').read()
    assert sha(node) == NODE
    browser = browser_tree()
    assert browser == {'sha256': '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e', 'fileCount': 255}
    assert sha(CHROME.read_bytes()) == 'cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76'
    runtime = subprocess.check_output(['git', '-C', '/home/user/work/runtime', 'archive', RUNTIME])
    assert sha(runtime) == RUNTIME_ARCHIVE
    files = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard']).decode().split('\0')
    source = {name: ('link:' + os.readlink(root / name)) if (root / name).is_symlink() else sha((root / name).read_bytes())
              for name in sorted(set(files)) if name and (root / name).is_file()}
    return {'declared_base': subprocess.check_output(['git', '-C', str(root), 'rev-parse', BASE]).decode().strip(),
            'source': source, 'runtime_commit': RUNTIME, 'runtime_archive': sha(runtime),
            'peer_graph': peers, 'public12': public, 'node': NODE, 'chrome': browser,
            'python': manifest(PYTHON.parent.parent), 'controller': sha(Path(__file__).read_bytes())}, runtime, node


def capture(root, fingerprint, runtime, node):
    # This known native-host seam is outside the rendering-leaf task. Refuse
    # fallback browser discovery rather than silently testing another browser.
    host = (root / 'astrid/core/execution/remotion_host_session.py').read_text()
    start = host.split('    def _start(', 1)[1].split('    def _exchange(', 1)[0]
    if 'ASTRID_REMOTION_BROWSER_EXECUTABLE' not in start:
        raise RuntimeError('normal HostRemotionSession._start drops the explicit Chrome155 selector; core execution owner must repair the native carry before capture')
    if shutil.disk_usage(WORK).free < 5 * 1024**3:
        raise RuntimeError('less than 5 GiB free')
    with tempfile.TemporaryDirectory(prefix='frame-', dir=WORK) as temporary:
        stage = Path(temporary)
        project = stage / 'runtime/remotion'
        shutil.copytree(root / 'remotion', project, ignore=shutil.ignore_patterns('node_modules', '__pycache__', '.vite', '.cache'))
        (project.parent / 'astrid').symlink_to(root / 'astrid', target_is_directory=True)
        shutil.copytree(PEERS, project / 'node_modules', symlinks=True)
        package = project / 'node_modules/@banodoco/timeline-composition'
        shutil.rmtree(package)
        with tarfile.open(project / 'artifacts/banodoco-timeline-composition-0.0.12.tgz') as archive:
            archive.extractall(stage / 'public', filter='data')
        (stage / 'public/package').rename(package)
        assert manifest(package) == fingerprint['public12']
        for p in (project / 'node_modules').rglob('*'):
            if p.is_symlink():
                assert p.resolve().is_relative_to(project / 'node_modules'), p
        shutil.copytree(PYTHON.parent.parent, stage / 'python', symlinks=True)
        with tarfile.open(fileobj=io.BytesIO(runtime)) as archive:
            archive.extractall(stage / 'runtime-source', filter='data')
        (stage / 'node').write_bytes(node)
        (stage / 'node').chmod(0o755)
        scratch = stage / 'tmp'
        scratch.mkdir(mode=0o700)
        environment = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'ASTRID_REMOTION_VALIDATION_'))
                       and k not in {'NODE_OPTIONS', 'NODE_PATH', 'PYTHONPYCACHEPREFIX', 'ASTRID_VERIFIED_TIMELINE_SOURCE'}}
        environment.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(root),
            ASTRID_RUNTIME_CHECKOUT=str(stage / 'runtime-source'), ASTRID_NODE_EXECUTABLE=str(stage / 'node'),
            ASTRID_REMOTION_PROJECT_DIR=str(project), ASTRID_REMOTION_BROWSER_EXECUTABLE=str(CHROME),
            ASTRID_TIMELINE_SCHEMA_PYTHONPATH=str(stage / 'python/lib/python3.11/site-packages'),
            TMPDIR=str(scratch), TMP=str(scratch), TEMP=str(scratch))
        try:
            return subprocess.call([str(stage / 'python/bin/python'), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                '-o', 'addopts=', '--basetemp=' + str(stage / 'pytest'), TEST], cwd=root, env=environment)
        finally:
            after, _, _ = inventory(root)
            assert after == fingerprint, 'source/shared input changed during capture'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['preflight', 'capture'])
    parser.add_argument('--source', type=Path, default=Path.cwd())
    parser.add_argument('--reviewed-sha256')
    args = parser.parse_args()
    root = args.source.resolve()
    before, runtime, node = inventory(root)
    digest = sha(encoded(before))
    if args.mode == 'preflight':
        Path(str(PREFIX) + '-fingerprints.json').write_bytes(encoded(before))
        print(json.dumps({'fingerprint_sha256': digest, 'agent_files': len(before['source']),
            'peer_entries': len(before['peer_graph']), 'public12_files': len(before['public12']),
            'browser': before['chrome'], 'test': TEST}, indent=2))
        return 0
    assert args.reviewed_sha256 == digest, 'manager-reviewed source/environment fingerprint required'
    return capture(root, before, runtime, node)


if __name__ == '__main__':
    raise SystemExit(main())
