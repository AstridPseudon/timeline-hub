"""Read-only MAIN6 capture preflight. No browser, renderer, or staging."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile

DESIGN = Path(__file__).resolve().parent
PREFIX = DESIGN / 'handoff-vw-m3-main-image-cap-render-proof-'
REPO = Path('/home/user/work/wt/vw-m3-main-image-cap-render-proof')
MAIN = 'a411628f8fd6129f9c58c332019b56769d997384'
COMPOSITION = Path('/home/user/peteromallet/timeline-composition')
OLD = '67b8aa3d0d6831d3e3504a340ff583c3da253707'
GRAPH = Path('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules')
BASELINE = DESIGN / 'handoff-vw-m3-root-smoke-central-ready-prepare-pre.json'
OLD_ARCHIVE = DESIGN.parent / 'workers/vw-m3-intended-dip-main-pixels/main-locked-0.0.6.tar.gz'
NODE = Path('/tmp/vw-m3-agent-gate-node20.19.4/bin/node')
BROWSER = Path('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell')
FORBIDDEN = (Path('/home/user/work/app/node_modules'),
             Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules'))
PEER_FILES = ('@remotion/player/dist/cjs/PlayerUI.js',
              '@remotion/player/dist/cjs/use-player-methods.js',
              '@remotion/player/dist/cjs/use-playback.js',
              '@remotion/player/dist/esm/index.mjs',
              'remotion/dist/esm/index.mjs',
              'remotion/dist/cjs/audio/shared-audio-tags.js')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def inventory(root):
    result = {}

    def walk(directory, ancestors):
        real = directory.resolve(strict=True)
        if real in ancestors:
            raise RuntimeError(f'dependency cycle: {directory}')
        for forbidden in FORBIDDEN:
            if real == forbidden or forbidden in real.parents:
                raise RuntimeError(f'polluted graph traversal: {directory}')
        for path in sorted(directory.iterdir()):
            relative = str(path.relative_to(root))
            if path.is_symlink():
                result[relative + '@link'] = os.readlink(path)
            if path.is_dir():
                walk(path, ancestors | {real})
            elif path.is_file():
                result[relative] = sha(path.read_bytes())
            else:
                raise RuntimeError(f'unsupported dependency entry: {path}')
    walk(root, set())
    return result


def main():
    before = inventory(GRAPH)
    baseline = json.loads(BASELINE.read_text())['graph']
    # MAIN6 is staged separately, never the public package in this peer graph.
    current = {k: v for k, v in before.items() if not k.startswith('@banodoco/')}
    expected = {k: v for k, v in baseline.items() if not k.startswith('@banodoco/')}
    added = sorted(current.keys() - expected.keys())
    missing = sorted(expected.keys() - current.keys())
    changed = sorted(k for k in current.keys() & expected.keys() if current[k] != expected[k])
    if added or changed or any(not k.startswith('.cache/webpack/') for k in missing):
        raise RuntimeError(f'graph differs from retained package bytes: {added=}, {changed=}, {missing=}')
    versions = {}
    for name, version in (('react', '18.3.1'), ('react-dom', '18.3.1'),
                          ('remotion', '4.0.509'), ('@remotion/bundler', '4.0.509'),
                          ('@remotion/renderer', '4.0.509'), ('@remotion/media', '4.0.509')):
        file = GRAPH / name / 'package.json'
        if json.loads(file.read_text())['version'] != version:
            raise RuntimeError(f'wrong peer version: {file}')
        versions[name] = {'version': version, 'package_json_sha256': sha(file.read_bytes())}
    peer_hashes = {name: sha((GRAPH / name).read_bytes()) for name in PEER_FILES}
    if any(peer_hashes[name] != baseline[name] for name in PEER_FILES):
        raise RuntimeError('six historical render peer hashes differ')
    if git(COMPOSITION, 'rev-parse', 'v0.0.6').decode().strip() != OLD:
        raise RuntimeError('Composition source tag changed')
    archive = subprocess.check_output(['gzip', '-n'], input=git(COMPOSITION,
        'archive', '--format=tar', '--prefix=timeline-composition-0.0.6/', 'v0.0.6'))
    lock_bytes = git(REPO, 'show', MAIN + ':remotion/package-lock.json')
    lock = json.loads(lock_bytes)['packages']['node_modules/@banodoco/timeline-composition']
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode()
    if lock['version'] != '0.0.6' or lock['integrity'] != integrity or archive != OLD_ARCHIVE.read_bytes():
        raise RuntimeError('MAIN6 git archive does not reproduce exact MAIN lock and retained archive')
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        members = {}
        for member in tar.getmembers():
            if member.isdir():
                continue
            if not member.isfile():
                raise RuntimeError(f'non-regular MAIN6 archive member: {member.name}')
            members[member.name] = sha(tar.extractfile(member).read())
    if len(members) != 29:
        raise RuntimeError(f'MAIN6 archive membership changed: {len(members)}')
    source = {}
    paths = ['remotion/src', 'remotion/webpack-alias.mjs', 'remotion/package.json',
             'remotion/package-lock.json', 'scripts/gen_effect_registry.py',
             'astrid/packs/local', 'astrid/packs/rendering']
    data = git(REPO, 'archive', MAIN, *paths)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for member in tar.getmembers():
            if member.isfile():
                source[member.name] = sha(tar.extractfile(member).read())
    after = inventory(GRAPH)
    if before != after:
        raise RuntimeError('peer graph changed during preflight')
    node_version = subprocess.check_output([str(NODE), '--version'], text=True).strip()
    if node_version != 'v20.19.4':
        raise RuntimeError('wrong Node version')
    preparation = json.loads((OLD_ARCHIVE.parent / 'preparation.json').read_text())
    tools = {'node': sha(NODE.read_bytes()), 'browser': sha(BROWSER.read_bytes())}
    if tools['node'] != preparation['node_sha256'] or tools['browser'] != preparation['browser_sha256']:
        raise RuntimeError('existing Node/browser differs from MAIN6 replay')
    free = shutil.disk_usage(DESIGN).free
    source_ready = sorted(str(p) for p in DESIGN.glob('handoff-vw-m3-main-image-cap-source-vector-*')
                          if 'READY' in p.name)
    blockers = []
    if free < 10 * 1024**3:
        blockers.append('free disk below required 10 GiB reserve; no staging/capture permitted')
    if not source_ready:
        blockers.append('source-vector completed flat READY/input/commands not published')
    quiet = DESIGN.parent / 'managers/viewing/QUIET.md'
    if quiet.exists():
        blockers.append('viewing QUIET is active')
    result = {'status': 'BLOCKED' if blockers else 'PREFLIGHT_ONLY_NOT_CAPTURE_GRANTED',
              'blockers': blockers, 'main': MAIN, 'composition6_source': OLD,
              'archive_sha256': sha(archive), 'archive_integrity': integrity,
              'archive_regular_members': len(members), 'archive_members': members,
              'main_source_sha256': source, 'six_peer_hashes_before': peer_hashes,
              'six_peer_hashes_after': {name: after[name] for name in PEER_FILES},
              'peer_versions': versions, 'graph': str(GRAPH), 'graph_entries': len(before),
              'graph_manifest_sha256': sha(json.dumps(before, sort_keys=True, separators=(',', ':')).encode()),
              'graph_unchanged': before == after, 'baseline_graph_added': added,
              'baseline_graph_changed': changed, 'baseline_graph_missing_cache_only': missing,
              'tools': tools, 'free_bytes': free, 'minimum_free_bytes': 10 * 1024**3,
              'source_ready_candidates': source_ready, 'capture_run': False}
    Path(str(PREFIX) + 'preflight.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'blockers', 'graph_entries',
          'archive_regular_members', 'archive_sha256', 'free_bytes')}, indent=2))
    return 1 if blockers else 0


if __name__ == '__main__':
    raise SystemExit(main())
