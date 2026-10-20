#!/usr/bin/env python3
"""Central-only bounded integration launcher, after manager final source/scope grant.

No host admission is invented here. The source SHA, installed test project and
scope are explicit command arguments approved by the manager in the named suite.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-pcm-peer-topology-guard'
ARCHIVE = ORCH / 'workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz'
ARCHIVE_SHA = '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
PYTHON = '/home/user/work/venv-agent/bin/python'
HELPERS = ('normal-audio-sources.mjs', 'attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs')
GRAPH = Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')
APPROVED_GRAPH_MANIFEST = Path(
    '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/'
    'scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-prepare-pre.json'
)
APPROVED_GRAPH_MANIFEST_SHA256 = '2387ebb5e0beaf9b5c0eea064edf0d9e1425059f05f39e9cb31fea064a5414ed'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def output(*args, cwd=None):
    return subprocess.check_output(args, text=True, cwd=cwd).strip()


def assert_clean_source(source):
    """Reject tracked and untracked source changes in the central snapshot."""
    assert output(
        'git', 'status', '--porcelain=v1', '--untracked-files=all', cwd=source,
    ) == '', 'source has tracked or untracked edits'


def graph_inventory(root):
    """Inventory the borrowed graph without allowing recursive symlink walks."""
    root = Path(root).resolve(strict=True)
    result = {}

    def walk(current, ancestors):
        resolved = current.resolve(strict=True)
        require(resolved not in ancestors, 'symlink cycle: ' + str(current))
        require(resolved == root or root in resolved.parents,
                'graph directory symlink escapes approved root: ' + str(current))
        for path in sorted(current.iterdir()):
            name = str(path.relative_to(root))
            if path.is_symlink():
                result[name + '@link'] = os.readlink(path)
                target = path.resolve(strict=True)
                require(target == root or root in target.parents,
                        'graph symlink escapes approved root: ' + str(path))
            if path.is_dir():
                walk(path, ancestors | {resolved})
            else:
                require(path.is_file(), 'non-file graph member: ' + str(path))
                result[name] = hashlib.sha256(path.read_bytes()).hexdigest()

    walk(root, set())
    return result


def approved_graph():
    require(APPROVED_GRAPH_MANIFEST.is_file(), 'retained approved graph manifest missing')
    require(digest(APPROVED_GRAPH_MANIFEST) == APPROVED_GRAPH_MANIFEST_SHA256,
            'retained approved graph manifest changed')
    manifest = json.loads(APPROVED_GRAPH_MANIFEST.read_text())
    graph = manifest.get('graph')
    require(isinstance(graph, dict) and graph, 'retained approved graph manifest has no graph')
    return graph


def assert_approved_graph(root=GRAPH, *, expected=None):
    """Reject cycles and every entry/target/byte drift from the retained graph."""
    expected = approved_graph() if expected is None else expected
    actual = graph_inventory(root)
    if actual == expected:
        return actual
    added = sorted(set(actual) - set(expected))
    missing = sorted(set(expected) - set(actual))
    changed = sorted(key for key in set(actual) & set(expected) if actual[key] != expected[key])
    detail = []
    if added:
        detail.append('added=' + repr(added[:3]))
    if missing:
        detail.append('missing=' + repr(missing[:3]))
    if changed:
        detail.append('changed=' + repr(changed[:3]))
    raise RuntimeError('borrowed graph differs from retained approved topology: ' + ', '.join(detail))


def preflight(source, source_sha, project, node):
    assert source_sha and len(source_sha) == 40, 'final producer commit SHA required'
    assert output('git', 'rev-parse', 'HEAD^{tree}', cwd=source) == output(
        'git', 'rev-parse', source_sha + '^{tree}', cwd=source,
    ), 'central snapshot must contain exactly the approved producer source tree'
    assert output('git', 'diff', '--name-only', 'HEAD', cwd=source) == '', 'source has tracked edits'
    assert_clean_source(source)
    assert_approved_graph()
    module = source / 'astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py'
    assert module.is_file(), 'normal_audio producer missing'
    for helper in HELPERS:
        assert (source / 'remotion' / helper).read_bytes() == (project / helper).read_bytes(), helper
    assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() == ARCHIVE_SHA
    package = project / 'node_modules/@banodoco/timeline-composition'
    with tarfile.open(ARCHIVE, 'r:gz') as archive:
        members = archive.getmembers()
        assert len(members) == 77
        names = set()
        for member in members:
            name = PurePosixPath(member.name)
            assert member.isfile() and name.parts[0] == 'package' and '..' not in name.parts
            relative = Path(*name.parts[1:])
            assert relative not in names
            names.add(relative)
            assert (package / relative).read_bytes() == archive.extractfile(member).read(), str(relative)
        assert {p.relative_to(package) for p in package.rglob('*') if p.is_file()} == names
    environment = {key: os.environ[key] for key in
                   ('HOME', 'LANG', 'LC_ALL', 'LC_CTYPE', 'PATH', 'TMPDIR') if key in os.environ}
    environment['PATH'] = str(node.parent) + os.pathsep + environment.get('PATH', '')
    # Resolve peers from the same actual project as the helper, not global imports.
    probe = """
const {createRequire} = require('node:module');
const req = createRequire(process.argv[1] + '/normal-audio-sources.mjs');
for (const [name, version] of Object.entries({react:'18.3.1', 'react-dom':'18.3.1',
  remotion:'4.0.509', '@remotion/media':'4.0.509', '@remotion/layout-utils':'4.0.509'})) {
  if (req(name + '/package.json').version !== version) throw Error(name + ' version');
}
if (process.version !== 'v20.19.4') throw Error('Node version');
"""
    subprocess.run([str(node), '-e', probe, str(project)], env=environment, check=True, timeout=15)
    environment.update(PYTHONPATH=str(source), PYTHONDONTWRITEBYTECODE='1',
                       PCM_SERVED_PROJECT=str(project), PCM_SERVED_NODE=str(node))
    return environment


def run_test(command, environment, source, source_sha, project, node):
    """Run pytest and always repeat the complete source/project/environment preflight."""
    result = 1
    postflight_error = None
    try:
        result = subprocess.run(command, env=environment, timeout=180).returncode
    finally:
        try:
            # This repeats the source status/tree, helper bytes, archive/package graph,
            # dependency versions, and Node/environment preflight after pytest even
            # when pytest fails.
            preflight(source, source_sha, project, node)
        except Exception as exc:  # noqa: BLE001 - preserve pytest's result below
            postflight_error = exc
            print(f'POSTFLIGHT FAILED: {exc}', file=sys.stderr)
    if postflight_error is not None:
        if result:
            print(f'preserving pytest return code: {result}', file=sys.stderr)
            return result
        return 1
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--node', required=True, type=Path)
    parser.add_argument('--scope', required=True, choices=('whole', 'with-phase'))
    parser.add_argument('--check', action='store_true', help='offline checks only; no listener or pytest')
    args = parser.parse_args()
    if (ORCH / 'QUIET.md').exists() or (ORCH / 'managers/viewing/QUIET.md').exists():
        raise SystemExit('QUIET active; no work started')
    source = Path.cwd().resolve(strict=True)
    environment = preflight(source, args.source_sha, args.project.resolve(strict=True), args.node.resolve(strict=True))
    print('public12 archive/77 members/peers/Node/source/helper bytes PASS', flush=True)
    if args.check:
        return
    # Service snapshots have .test-* names; direct worker execution stays closed.
    assert source.name.startswith('.test-'), 'run only from central test-service snapshot'
    test = Path(str(PREFIX) + '-test_normal_audio_served_sources.py')
    own = ORCH / 'workers/vw-m3-pcm-peer-topology-guard'
    with tempfile.TemporaryDirectory(prefix='central-pcm-', dir=own) as temporary:
        command = [PYTHON, '-B', '-m', 'pytest', '-c', str(source / 'pyproject.toml'),
                   '-p', 'no:cacheprovider', '--basetemp', temporary, '-q', str(test)]
        if args.scope == 'whole':
            command += ['-k', 'not slice_retains_original_phase']
        return run_test(command, environment, source, args.source_sha,
                        args.project.resolve(strict=True), args.node.resolve(strict=True))


if __name__ == '__main__':
    raise SystemExit(main())
