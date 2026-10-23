#!/usr/bin/env python3
"""Private source replay and normal-dispatch first-use proof; no real builds."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
TMP = Path(os.environ['TMPDIR']).resolve(strict=True)
assert TMP.is_dir() and TMP.stat().st_uid == os.getuid()
ROOT = Path(tempfile.mkdtemp(prefix='store-initialize-', dir=TMP))
assert ROOT.is_relative_to(TMP) and not ROOT.is_symlink()
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
MANIFEST = json.loads((HERE / 'bench-store-initialize-manifest.json').read_text())


def private(path):
    path = Path(path)
    assert path.is_absolute() and path.resolve().is_relative_to(ROOT)
    if path.exists():
        assert path.stat().st_uid == os.getuid()
    return path


def run(argv, *, env=None, cwd=None, input=None):
    result = subprocess.run(argv, env=env, cwd=cwd, input=input, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=25, check=False)
    return result


def write(path, value, executable=False):
    path = private(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value)
    if executable:
        path.chmod(0o700)
    return path


def snapshot(root):
    return {str(p.relative_to(root)): (p.lstat().st_mode, p.lstat().st_ino,
            p.readlink().as_posix() if p.is_symlink() else
            p.read_bytes() if p.is_file() else None)
            for p in [root, *root.rglob('*')]}


def module(path):
    spec = importlib.util.spec_from_file_location('private_store', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def replay():
    replay_root = private(ROOT / 'replay')
    (replay_root / 'bin').mkdir(parents=True)
    for record in MANIFEST['files']:
        for kind in ('source', 'target'):
            data = (HERE / record[kind]['snapshot']).read_bytes()
            assert len(data) == record[kind]['bytes']
            assert hashlib.sha256(data).hexdigest() == record[kind]['sha256']
        shutil.copyfile(HERE / record['source']['snapshot'], replay_root / record['path'])
    result = run(['patch', '--batch', '--fuzz=0', '-p1'], cwd=replay_root,
                 input=(HERE / 'bench-store-initialize.patch').read_text())
    assert result.returncode == 0, result.stdout
    assert 'offset' not in result.stdout and 'fuzz' not in result.stdout
    for record in MANIFEST['files']:
        actual = (replay_root / record['path']).read_bytes()
        assert actual == (HERE / record['target']['snapshot']).read_bytes()
        assert hashlib.sha256(actual).hexdigest() == record['target']['sha256']
        if record['path'].endswith('.py'):
            compile(actual, record['path'], 'exec')
        else:
            assert run(['bash', '-n', str(replay_root / record['path'])]).returncode == 0
            baseline = (HERE / record['source']['snapshot']).read_text()
            assert actual.decode() == baseline.replace(
                'store = module.Store(root, tests)',
                'store = module.Store.open_or_initialize(root, tests)', 1)
    for name, record in MANIFEST['unchanged'].items():
        data = (HERE / 'baseline' / name).read_bytes()
        assert len(data) == record['bytes']
        assert hashlib.sha256(data).hexdigest() == record['sha256']
    print('PASS literal patch --batch --fuzz=0; byte/SHA replay; compile; bash -n; carrier invariants')
    return replay_root


def core_cases(source):
    core = module(source)
    case = private(ROOT / 'core')
    case.mkdir()
    tests = case / 'tests'
    tests.mkdir()
    (tests / 'suites.conf').write_text('')
    root = case / 'bench-store'
    store = core.Store.open_or_initialize(root, tests)
    owner = (root / 'owner.json').read_bytes()
    before = snapshot(case)
    assert core.Store.open_or_initialize(root, tests).owner == store.owner
    assert snapshot(case) == before

    def refused(label, callback):
        before = snapshot(case)
        try:
            callback()
        except (core.Refused, OSError, ValueError, TypeError, KeyError):
            pass
        else:
            raise AssertionError('accepted ' + label)
        assert snapshot(case) == before, label + ': wrote on refusal'
        print('PASS refusal/no-write ' + label)

    unknown = case / 'unknown'
    unknown.mkdir()
    (unknown / 'sentinel').write_text('untouched')
    refused('unknown existing root', lambda: core.Store.open_or_initialize(unknown, tests))
    partial = case / 'partial'
    partial.mkdir()
    (partial / 'owner.json').write_text('{}')
    refused('partial owner', lambda: core.Store.open_or_initialize(partial, tests))
    link = case / 'link'
    link.symlink_to(root, target_is_directory=True)
    refused('root symlink', lambda: core.Store.open_or_initialize(link, tests))
    dangling = case / 'dangling'
    dangling.symlink_to(case / 'absent')
    refused('dangling symlink', lambda: core.Store.open_or_initialize(dangling, tests))
    wrong_tests = case / 'wrong-tests'
    wrong_tests.mkdir()
    refused('wrong tests', lambda: core.Store.open_or_initialize(root, wrong_tests))
    refused('missing tests', lambda: core.Store.open_or_initialize(case / 'fresh', case / 'missing-tests'))
    for field, value in (('uid', os.getuid() + 1), ('root', str(case / 'foreign')),
                         ('version', 999)):
        damaged = json.loads(owner)
        damaged[field] = value
        (root / 'owner.json').write_text(json.dumps(damaged))
        refused('foreign owner ' + field, lambda: core.Store.open_or_initialize(root, tests))
        (root / 'owner.json').write_bytes(owner)
    with patch.object(core.os, 'getuid', return_value=os.getuid() + 1):
        refused('foreign filesystem UID', lambda: core.Store.open_or_initialize(root, tests))
    (root / 'entries').rename(root / 'entries-old')
    (root / 'entries').mkdir()
    refused('replaced directory inode', lambda: core.Store.open_or_initialize(root, tests))
    (root / 'entries').rename(root / 'entries-new')
    (root / 'entries-old').rename(root / 'entries')
    root.rename(case / 'old-root')
    root.mkdir()
    for p in (case / 'old-root').iterdir():
        p.rename(root / p.name)
    refused('replaced root inode', lambda: core.Store.open_or_initialize(root, tests))

    # Failed initialization is never repaired or adopted by the next request.
    failed = case / 'failed'
    real_atomic = core.atomic

    def crash(path, value):
        if path.name == 'index.json':
            raise OSError('private simulated initialization interruption')
        return real_atomic(path, value)

    with patch.object(core, 'atomic', side_effect=crash):
        try:
            core.Store.open_or_initialize(failed, tests)
        except OSError:
            pass
        else:
            raise AssertionError('missing crash')
    refused('interrupted initialization', lambda: core.Store.open_or_initialize(failed, tests))
    print('PASS valid reopen unchanged; existing ownership/mutex/index checks retained')


# This private read-only Git fixture answers only source-inspection commands.
# It never invokes Git, writes .git, archives sources, installs or builds.
GIT_TOOL = '''#!/usr/bin/env python3
import hashlib, json, os, pathlib, sys
args = sys.argv[1:]
assert args[:1] == ['-C'], args
repo = pathlib.Path(args[1]); args = args[2:]
root = pathlib.Path(os.environ['FIXTURE_ROOT']).resolve()
assert repo.resolve().is_relative_to(root)
facts = json.loads((repo / 'facts.json').read_text())
op = args[0]
if op == 'rev-parse':
    if '--is-inside-work-tree' in args: print('true')
    elif args[-1].endswith(':remotion'): print('c' * 40)
    else: print(facts['sha'])
elif op == 'status': pass
elif op == 'show':
    commit, name = args[1].split(':', 1)
    assert commit in (facts['sha'], 'HEAD'), args
    sys.stdout.write((repo / name).read_text())
elif op == 'cat-file':
    value = args[-1]
    if ':' in value:
        assert (repo / value.split(':', 1)[1]).is_file(), args
    else: assert value in (facts['sha'] + '^{commit}', 'HEAD^{commit}'), args
elif op == 'ls-tree':
    print('packages/python/astrid_runtime_client/__init__.py')
else: raise AssertionError(args)
'''


def caller_cases(replay_root):
    parent = private(ROOT / 'caller')
    orch, work, tools = parent / 'orch', parent / 'work', parent / 'tools'
    for folder in ('bin', 'tests', 'queue/pending', 'queue/done', 'queue/refused'):
        (orch / folder).mkdir(parents=True, exist_ok=True)
    (work / 'runtimes').mkdir(parents=True)
    tools.mkdir()
    agent, runtime = parent / 'agent', parent / 'runtime'
    package = {'name': 'private', 'engines': {'node': '=20.19.4', 'npm': '=10.8.2'}}
    lock = {'packages': {'node_modules/remotion': {'version': '3'},
                        'node_modules/@banodoco/timeline-composition': {'version': '1'}}}
    for repo, sha in ((agent, 'a' * 40), (runtime, 'b' * 40)):
        write(repo / 'facts.json', json.dumps({'sha': sha}))
        write(repo / 'pyproject.toml', '[project]\nname="private"\nversion="0"\n')
    write(agent / 'requirements/proof.lock', '# private preflight only\n')
    write(agent / 'remotion/package.json', json.dumps(package))
    write(agent / 'remotion/package-lock.json', json.dumps(lock))
    write(runtime / 'packages/python/astrid_runtime_client/__init__.py', 'CLIENT=True\n')
    write(tools / 'git', GIT_TOOL, True)
    write(tools / 'python3', '#!/bin/sh\nexec ' + sys.executable + ' "$@"\n', True)
    write(tools / 'fixture-python', '#!/bin/sh\ncase "$*" in\n'
          '"--version") echo "Python 3.13.0";;\n'
          '"-m venv --help"|"-c "*) exit 0;;\n'
          '*) echo "REFUSED private interpreter build" >&2; exit 97;;\nesac\n', True)
    node = parent / 'node'
    write(node / 'node', '#!/bin/sh\n[ "$*" = --version ] || exit 97\necho v20.19.4\n', True)
    write(node / 'npm', '#!/bin/sh\n[ "$*" = --version ] || exit 97\necho 10.8.2\n', True)
    for name in ('curl', 'tar', 'xz', 'pip', 'npm'):
        write(tools / name, '#!/bin/sh\necho "REFUSED private build/network tool" >&2\nexit 97\n', True)
    for name in ('make-child-venv', 'make-runtime', 'bench_store.py'):
        shutil.copyfile(replay_root / 'bin' / name, private(orch / 'bin' / name))
        (orch / 'bin' / name).chmod(0o700)
    for name in ('request-child-venv', 'request-runtime'):
        shutil.copyfile(HERE / 'baseline' / name, private(orch / 'bin' / name))
        (orch / 'bin' / name).chmod(0o700)
    # Existing fixed templates are copied as inert bytes, never executed.
    for name in ('suites.conf', 'agent-remotion-0013.env', 'agent-remotion.env'):
        shutil.copyfile(ORCH / 'tests' / name, private(orch / 'tests' / name))
    helper = orch / 'bin/bench_store.py'
    helper.write_text(helper.read_text() + '''
def _private_stop(self, point):
    if point == 'before-build':
        raise Refused('PRIVATE_BEFORE_BUILD owner=' + self.owner['id'])
Store._checkpoint = _private_stop
''')
    env = {'PATH': str(tools) + ':/usr/bin:/bin', 'HOME': str(parent), 'TMPDIR': str(TMP),
           'FIXTURE_ROOT': str(parent), 'PYTHONDONTWRITEBYTECODE': '1',
           'CHILD_VENV_ORCH_ROOT': str(orch), 'CHILD_VENV_WORK_ROOT': str(work),
           'CHILD_VENV_AGENT_CHECKOUT': str(agent), 'CHILD_VENV_RUNTIME_CHECKOUT': str(runtime),
           'CHILD_VENV_PYTHON': str(tools / 'fixture-python'),
           'RUNTIME_ORCH_ROOT': str(orch), 'RUNTIME_WORK_ROOT': str(work)}
    for path in (orch, work, tools, agent, runtime, node, helper):
        private(path)
    assert not (work / 'bench-store').exists()
    daemon = (HERE / 'baseline/dispatcher-daemon').read_text()
    commands = {}
    for kind, name in (('CHILDVENV', 'make-child-venv'), ('RUNTIME', 'make-runtime')):
        match = re.search(r'out=\$\((\$O/bin/' + name + r' .*?) 2>&1\); rc=', daemon)
        assert match, kind
        commands[kind] = match[1]
    lock_sha = hashlib.sha256((agent / 'remotion/package-lock.json').read_bytes()).hexdigest()

    def chain(kind, clean, suffix):
        if kind == 'CHILDVENV':
            name = 'venv-agent-child-' + suffix
            requester = orch / 'bin/request-child-venv'
            args = [name, 'a' * 40, 'remotion-env-nodes', 'private-graph',
                    '--source-carrier', str(agent), str(runtime), 'b' * 40]
            pending = orch / 'queue/pending' / ('childvenv-' + name)
        else:
            name = 'agent-remotion-' + suffix
            requester = orch / 'bin/request-runtime'
            args = [name, 'a' * 40, lock_sha, str(agent), str(runtime), 'b' * 40,
                    'remotion-env-nodes', str(node)]
            pending = orch / 'queue/pending' / ('runtime-' + name)
        command = [str(requester), *args]
        if clean:
            command = ['/usr/bin/env', '-i', *(k + '=' + v for k, v in env.items()), *command]
        result = run(command, env=env)
        assert result.returncode == 0, result.stdout
        assert pending.read_text() == kind + ' ' + ' '.join(args) + '\n'
        # Execute precisely the live daemon's maker invocation, no eval, daemon
        # mutation, queue cleanup loop, fake receipt, or real daemon process.
        command = ['bash', '-c', 'O=$1; f=$2; ' + commands[kind],
                   'private-dispatch', str(orch), str(pending)]
        if clean:
            command = ['/usr/bin/env', '-i', *(k + '=' + v for k, v in env.items()), *command]
        result = run(command, env=env)
        assert result.returncode != 0 and 'PRIVATE_BEFORE_BUILD owner=' in result.stdout, result.stdout
        assert not (work / name).exists()
        assert not list((work / 'bench-store/staging').iterdir())
        return re.search(r'PRIVATE_BEFORE_BUILD owner=([a-f0-9]{32})', result.stdout)[1]

    # Different components contend on the same parent inode before metadata exists.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(chain, kind, False, 'concurrent-' + kind.lower())
                   for kind in ('CHILDVENV', 'RUNTIME')]
        owners = [future.result() for future in futures]
    root = work / 'bench-store'
    assert owners[0] == owners[1] == json.loads((root / 'owner.json').read_text())['id']
    core = module(replay_root / 'bin/bench_store.py')
    store = core.Store(root, orch / 'tests')
    with store.mutex():
        assert store._load() == {'version': 1, 'seq': 0, 'entries': {},
                                 'registrations': {}, 'retired': [], 'retired_suites': []}
    before = snapshot(root)
    for kind in ('CHILDVENV', 'RUNTIME'):
        assert chain(kind, True, 'envi-' + kind.lower()) == owners[0]
        assert snapshot(root) == before
    # Each component also gets its own genuinely absent first use under env -i.
    for kind in ('CHILDVENV', 'RUNTIME'):
        root.rename(work / ('retained-' + kind.lower()))
        chain(kind, True, 'fresh-envi-' + kind.lower())
        assert (root / 'owner.json').is_file() and (root / 'index.json').is_file()
    assert not list((root / 'staging').iterdir())
    assert not (root / 'pending.json').exists()
    print('PASS real requester -> unchanged daemon invocation -> normal maker: '
          'child/runtime concurrent first-use; env -i first-use/reopen; one owner; valid index; build=0')


if __name__ == '__main__':
    replay_root = replay()
    core_cases(replay_root / 'bin/bench_store.py')
    caller_cases(replay_root)
    print('PASS source-only private acceptance; no real store/build/network/download or Git writes')
