#!/usr/bin/env python3
"""Prepare offline; run once only in a centrally created, manager-granted snapshot."""
import difflib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
NAME = 'vw-m3-root-smoke-central-ready'
OWN = ORCH / 'workers' / NAME
PREFIX = ORCH / 'design' / ('handoff-' + NAME)
SOURCE = Path('/home/user/work/wt') / NAME
SHA = '5acd7233df676bf42b2086d86cb0a6358398bf5f'
TREE = '66898dd11df74e205af95903651782a29e9886b4'
GRAPH = Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')
NODE = Path('/tmp/vw-m3-agent-gate-node20.19.4/bin/node')
PYTHON = '/home/user/work/venv-agent/bin/python'
SCHEMA = '/home/user/work/venv-agent/lib/python3.11/site-packages'
BROWSER = Path('/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
ARCHIVE = 'remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz'
ARCHIVE_SHA = 'cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7'
HISTORICAL = {
    '@remotion/player/dist/cjs/PlayerUI.js': '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
    '@remotion/player/dist/cjs/use-player-methods.js': 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
    '@remotion/player/dist/cjs/use-playback.js': '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
    '@remotion/player/dist/esm/index.mjs': 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
    'remotion/dist/esm/index.mjs': '9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8',
    'remotion/dist/cjs/audio/shared-audio-tags.js': '471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c',
}


def artifact(suffix):
    return Path(str(PREFIX) + '-' + suffix)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def quiet():
    if any(p.exists() for p in (ORCH / 'QUIET.md', ORCH / 'managers/viewing/QUIET.md')):
        (OWN / 'PAUSED_ACK').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + '\n')
        raise SystemExit(75)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def command(args, cwd=None, env=None):
    return subprocess.check_output(args, cwd=cwd, env=env, text=True).strip()


def git(root, *args):
    return command(['git', '-C', str(root), *args])


def tracked(root):
    files = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).decode().split('\0')
    result = {}
    for name in sorted(filter(None, files)):
        path = root / name
        result[name] = {'sha256': digest(path), 'mode': path.stat().st_mode & 0o777,
                        'link': os.readlink(path) if path.is_symlink() else None}
    return result


def inventory(root):
    result = {}

    def walk(current, parents):
        resolved = current.resolve(strict=True)
        require(resolved not in parents, 'symlink cycle: ' + str(current))
        for path in sorted(current.iterdir()):
            name = str(path.relative_to(root))
            if path.is_symlink():
                result[name + '@link'] = os.readlink(path)
            if path.is_dir():
                walk(path, parents | {resolved})
            else:
                require(path.is_file(), 'non-file graph member: ' + str(path))
                result[name] = digest(path)
    walk(root, set())
    return result


def pins(root):
    require(digest(root / ARCHIVE) == ARCHIVE_SHA, 'public10 archive changed')
    pkg = json.loads((root / 'remotion/package.json').read_text())
    lock = json.loads((root / 'remotion/package-lock.json').read_text())
    import base64
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512((root / ARCHIVE).read_bytes()).digest()).decode()
    require(pkg['engines'] == {'node': '=20.19.4', 'npm': '=10.8.2'}, 'engine pins changed')
    require(lock['packages']['node_modules/@banodoco/timeline-composition']['integrity'] == integrity,
            'public10 lock integrity mismatch')
    require(pkg['dependencies']['@banodoco/timeline-composition'] == 'file:artifacts/banodoco-timeline-composition-0.0.10.tgz',
            'public10 package pin mismatch')
    for name, version in {'react': '18.3.1', 'react-dom': '18.3.1', 'remotion': '4.0.509',
                          '@remotion/media': '4.0.509', '@remotion/layout-utils': '4.0.509',
                          '@remotion/renderer': '4.0.509', '@remotion/bundler': '4.0.509',
                          '@remotion/cli': '4.0.509'}.items():
        require(json.loads((GRAPH / name / 'package.json').read_text())['version'] == version, name + ' installed version mismatch')
        require(lock['packages']['node_modules/' + name]['version'] == version, name + ' lock mismatch')
    for name, expected in HISTORICAL.items():
        require(digest(GRAPH / name) == expected, 'historical graph hash changed: ' + name)
    require(command([str(NODE), '--version']) == 'v20.19.4', 'Node version mismatch')
    require(command([str(NODE), str(NODE.parent.parent / 'lib/node_modules/npm/bin/npm-cli.js'), '--version']) == '10.8.2',
            'npm version mismatch')
    renderer = (GRAPH / '@remotion/renderer/dist/select-composition.js').read_text()
    require('browserExecutable: browserExecutable' in renderer and 'onBrowserDownload' in renderer,
            'renderer explicit browser API unavailable')


def smoke_invocation(original):
    # Invocation only: the committed snapshots, fixtures and metadata assertions remain verbatim.
    marker = "import {remotionPrimitiveAliasesFor} from '../webpack-alias.mjs';"
    require(original.count(marker) == 1 and original.count('      inputProps,\n') == 1, 'smoke invocation shape changed')
    changed = original.replace(marker, marker + "\nimport {sharedBrowserExecutable} from '../shared-browser.mjs';")
    changed = changed.replace('const main = async () => {', '''const main = async () => {
  const browserExecutable = sharedBrowserExecutable({projectRoot: projectDir});
  if (!browserExecutable) fail('An explicit existing browser is required');
  const browserOptions = {
    browserExecutable,
    chromeMode: 'chrome-for-testing',
    onBrowserDownload: () => fail('Browser download is prohibited'),
  };''')
    changed = changed.replace('      inputProps,\n', '      inputProps,\n      ...browserOptions,\n')
    # The bundler defaults to a persistent node_modules/.cache directory.
    changed = changed.replace('    entryPoint,\n', '    entryPoint,\n    enableCaching: false,\n')
    marker = '  console.log(`Smoke bundle OK'
    require(original.count(marker) == 1, 'smoke completion marker changed')
    empty = '''  const empty = await selectComposition({
    serveUrl: bundleLocation,
    id: compositionId,
    ...browserOptions,
  });
  assertPositiveMetadata('empty', empty);
  if (empty.durationInFrames !== 1) fail('Empty timeline must select exactly one frame');
  console.log('Empty timeline metadata OK: ' + JSON.stringify(empty));

'''
    return changed.replace(marker, empty + marker)


def stage(root, destination):
    project = destination / 'remotion'
    project.mkdir(parents=True)
    files = tracked(root)
    for name in sorted({name.split('/')[0] for name in files} - {'remotion'}):
        (destination / name).symlink_to(root / name, target_is_directory=(root / name).is_dir())
    for name in files:
        if name.startswith('remotion/'):
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / name, target, follow_symlinks=False)
            require(digest(target) == files[name]['sha256'], 'staged tracked file differs: ' + name)
    nm = project / 'node_modules'
    nm.mkdir()
    for entry in sorted(GRAPH.iterdir()):
        if entry.name in {'.cache', '.remotion'}:
            continue
        if entry.name in {'@banodoco', '@remotion'}:
            (nm / entry.name).mkdir()
            for child in sorted(entry.iterdir()):
                target = nm / entry.name / child.name
                if entry.name == '@banodoco' and child.name == 'timeline-composition':
                    continue
                if entry.name == '@remotion' and child.name == 'cli':
                    shutil.copytree(child, target, symlinks=True)
                    require(inventory(child) == inventory(target), 'local CLI copy differs')
                else:
                    target.symlink_to(child, target_is_directory=child.is_dir())
        else:
            (nm / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
    package = nm / '@banodoco/timeline-composition'
    package.mkdir(parents=True)
    with tarfile.open(root / ARCHIVE, 'r:gz') as archive:
        members = archive.getmembers()
        require(len(members) == 77 and len({m.name for m in members}) == 77, 'public10 must have exactly 77 distinct members')
        expected = {}
        for member in members:
            parts = PurePosixPath(member.name).parts
            require(member.isfile() and parts[0] == 'package' and '..' not in parts and not member.name.startswith('/'),
                    'unsafe public10 member: ' + member.name)
            name = '/'.join(parts[1:])
            require(bool(name), 'empty member name')
            data = archive.extractfile(member).read()
            target = package / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            expected[name] = hashlib.sha256(data).hexdigest()
        require(inventory(package) == expected, 'public10 extraction differs')
    smoke = project / '__smoke__/bundle.mjs'
    original = smoke.read_text()
    changed = smoke_invocation(original)
    smoke.write_text(changed)
    artifact('invocation.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True), changed.splitlines(True),
                                                                      fromfile='committed/remotion/__smoke__/bundle.mjs',
                                                                      tofile='ORCH-stage/remotion/__smoke__/bundle.mjs')))
    return project


def environment(root, project, temp):
    return {
        'HOME': str(temp), 'TMPDIR': str(temp), 'LANG': 'C.UTF-8',
        'PATH': str(NODE.parent) + ':/home/user/work/venv-agent/bin:/usr/bin:/bin',
        'PYTHONPATH': str(root), 'PYTHONDONTWRITEBYTECODE': '1',
        'ASTRID_NODE_EXECUTABLE': str(NODE), 'ASTRID_REMOTION_PROJECT_DIR': str(project),
        'ASTRID_TIMELINE_SCHEMA_PYTHONPATH': SCHEMA,
        'ASTRID_REMOTION_BROWSER_EXECUTABLE': str(BROWSER),
        'PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD': '1', 'CI': '1',
    }


def readiness(root, project, temp, label):
    probe = '''import json, os, sys
from pathlib import Path
from astrid.core.rendering import remotion_runtime as r
p = Path(os.environ['ASTRID_REMOTION_PROJECT_DIR'])
problem = r.remotion_install_problem(p)
if problem is not None: raise RuntimeError(problem)
bound = r._runtime_inputs(p, os.environ, sys.executable, {})
print(json.dumps({'install_problem': problem, 'bound': bound}, sort_keys=True))
'''
    result = command([PYTHON, '-c', probe], cwd=root, env=environment(root, project, temp))
    artifact(label + '-readiness.json').write_text(result + '\n')
    return json.loads(result)


def snapshot(root):
    return {'head': git(root, 'rev-parse', 'HEAD'), 'tree': git(root, 'rev-parse', 'HEAD^{tree}'),
            'source': tracked(root), 'graph': inventory(GRAPH),
            'browser': inventory(BROWSER.parent), 'node': digest(NODE)}


def controller_hashes():
    return {p.name: digest(p) for p in (Path(__file__), artifact('READY.sh'))}


def prepare():
    quiet()
    require(git(SOURCE, 'rev-parse', 'HEAD') == SHA and git(SOURCE, 'rev-parse', 'HEAD^{tree}') == TREE, 'source identity changed')
    require(not git(SOURCE, 'status', '--porcelain', '--untracked-files=all'), 'source is dirty')
    before = snapshot(SOURCE)
    write(artifact('prepare-pre.json'), before)
    destination = Path(tempfile.mkdtemp(prefix=NAME + '-prepare-', dir=OWN))
    staged = None
    project = None
    try:
        pins(SOURCE)
        project = stage(SOURCE, destination)
        temp = destination / 'temp'
        temp.mkdir()
        quiet()
        bound = readiness(SOURCE, project, temp, 'prepare')
        command([str(NODE), '--check', str(project / '__smoke__/bundle.mjs')])
        package = inventory(project / 'node_modules/@banodoco/timeline-composition')
        staged = inventory(project)
        ready = {'status': 'READY, NOT RUN; manager grant required', 'source_sha': SHA, 'source_tree': TREE,
                 'source_file_count': len(before['source']), 'graph_file_count': len(before['graph']),
                 'graph_path': str(GRAPH), 'archive_sha256': ARCHIVE_SHA, 'archive_members': len(package),
                 'controller_hashes': controller_hashes(), 'browser': str(BROWSER), 'node': str(NODE),
                 'pre_manifest_sha256': digest(artifact('prepare-pre.json')),
                 'staged_smoke_sha256': digest(project / '__smoke__/bundle.mjs'),
                 'package': package, 'staged_graph_manifest_sha256': hashlib.sha256(canonical(staged).encode()).hexdigest(),
                 'binding_file_count': bound['bound']['file_count']}
    finally:
        try:
            if staged is not None:
                staged_final = inventory(project)
                require(staged == staged_final, 'staged graph changed during preparation')
        finally:
            try:
                after = snapshot(SOURCE)
                write(artifact('prepare-finally.json'), after)
                require(before == after, 'source/graph/browser/Node changed during preparation')
                require(not git(SOURCE, 'status', '--porcelain', '--untracked-files=all'), 'source dirty after preparation')
            finally:
                shutil.rmtree(destination)
    write(artifact('READY.json'), ready)
    print(canonical({k: v for k, v in ready.items() if k != 'package'}))


def run():
    quiet()
    root = Path.cwd()
    require(root.name.startswith('.test-' + NAME + '-e2e-viewing-public10-root-smoke-'), 'central snapshot required')
    ready = json.loads(artifact('READY.json').read_text())
    require(ready['controller_hashes'] == controller_hashes(), 'controller changed since READY')
    grant = json.loads((OWN / 'READY_GRANTED').read_text())
    require(grant == {'source_sha': SHA, 'controller_hashes': controller_hashes(),
                      'ready_sha256': digest(artifact('READY.json'))}, 'manager exact-SHA/controller grant does not match')
    require(git(root, 'rev-parse', 'HEAD^') == SHA and git(root, 'rev-parse', 'HEAD^{tree}') == TREE,
            'central source parent/tree differs from grant')
    baseline = json.loads(artifact('prepare-pre.json').read_text())
    require(digest(artifact('prepare-pre.json')) == ready['pre_manifest_sha256'], 'READY baseline changed')
    before = snapshot(root)
    # Central adds a synthetic snapshot commit; its parent was checked above.
    require({**before, 'head': SHA} == baseline, 'full tracked source or borrowed graph/browser/Node differs from READY')
    require(not git(root, 'status', '--porcelain', '--untracked-files=all'), 'central snapshot is dirty')
    write(artifact('run-pre.json'), before)
    # O_EXCL consumes the single permitted attempt only after grant and preflight.
    fd = os.open(OWN / 'ATTEMPT_STARTED', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    with os.fdopen(fd, 'w') as handle:
        handle.write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + '\n')
    destination = Path(tempfile.mkdtemp(prefix=NAME + '-run-', dir=OWN))
    rc = 1
    staged_pre = None
    project = None
    try:
        pins(root)
        project = stage(root, destination)
        temp = destination / 'temp'
        temp.mkdir()
        require(digest(project / '__smoke__/bundle.mjs') == ready['staged_smoke_sha256'], 'staged invocation differs from READY')
        staged_pre = inventory(project)
        require(hashlib.sha256(canonical(staged_pre).encode()).hexdigest() == ready['staged_graph_manifest_sha256'],
                'complete staged source/CLI/public10/peer graph differs from READY')
        write(artifact('stage-pre.json'), staged_pre)
        quiet()
        readiness(root, project, temp, 'run')
        quiet()
        env = environment(root, project, temp)
        with artifact('smoke.log').open('x') as log:
            process = subprocess.Popen([str(NODE), str(project / '__smoke__/bundle.mjs')], cwd=project,
                                       env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                deadline = time.monotonic() + 300
                while process.poll() is None:
                    quiet()
                    require(time.monotonic() < deadline, 'smoke exceeded five minutes')
                    time.sleep(0.25)
                rc = process.returncode
            finally:
                # Remotion's internal cleanup is asynchronous; reap its whole process group too.
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait(timeout=10)
                except ProcessLookupError:
                    pass
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                # A finished Node parent can leave browser children in this group.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
        output = artifact('smoke.log').read_text()
        require(rc == 0, 'existing Root smoke failed; see retained smoke.log')
        require('Smoke bundle OK for golden, full fixtures' in output and 'Empty timeline metadata OK:' in output,
                'smoke completion/empty assertion missing')
        print(output)
        staged_post = inventory(project)
        write(artifact('stage-post.json'), staged_post)
        require(staged_pre == staged_post, 'staged source/package/peer graph changed')
    finally:
        try:
            if staged_pre is not None:
                staged_final = inventory(project)
                write(artifact('stage-finally.json'), staged_final)
                require(staged_pre == staged_final, 'staged source/package/peer graph changed in finally')
        finally:
            try:
                after = snapshot(root)
                write(artifact('run-finally.json'), after)
                require(before == after, 'source/borrowed graph/browser/Node changed during smoke')
                require(not git(root, 'status', '--porcelain', '--untracked-files=all'), 'central source dirty after smoke')
            finally:
                shutil.rmtree(destination)
                (OWN / 'ATTEMPT_FINISHED').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + '\n')
    write(artifact('result.json'), {'status': 'PASS', 'source_sha': SHA, 'source_tree': TREE,
                                  'scope': 'package-consumer Root smoke; golden/full/empty metadata only'})


if __name__ == '__main__':
    require(len(sys.argv) == 2 and sys.argv[1] in {'prepare', 'run'}, 'use prepare or run')
    # READY.sh holds the browser lock for runs; offline preparation takes it too.
    if sys.argv[1] == 'prepare':
        with open('/tmp/timeline-viewing-browser.lock', 'a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            prepare()
    else:
        # The wrapper passes its locked open-file description through exec.
        require(os.readlink('/proc/self/fd/9') == '/tmp/timeline-viewing-browser.lock', 'READY.sh lock FD required')
        fcntl.flock(9, fcntl.LOCK_EX | fcntl.LOCK_NB)
        def interrupted(signum, frame):
            raise SystemExit(128 + signum)
        signal.signal(signal.SIGTERM, interrupted)
        run()
