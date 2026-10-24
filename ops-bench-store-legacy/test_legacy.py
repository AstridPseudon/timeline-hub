"""Finite, private recovery proof. Legacy custody is deliberately not invented."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('bench_store', HERE / 'bench_store.py')
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
FINITE = {
    'venv-agent-child-s2': {},
    'venv-agent-child-s2-c13': {
        '.astrid-source-commit': '0b2f662e32e1a6818d58f9cf12130f0a89fb5a3b\n',
    },
    'runtimes/agent-remotion': {},
    'runtimes/agent-remotion-0013': {},
    'runtimes/agent-remotion-current': {
        '.source-commit': '7970544bb17dfcf234bd1cc1bb55ab5d713decd8\n',
    },
    'runtimes/agent-remotion-independent-review.partial.HIa4dVUW': {},
    'runtimes/agent-remotion-independent-review.partial.6U6z45XJ': {},
}


class Crash(BaseException):
    pass


def tree(root):
    result = {}
    for path in [root, *sorted(root.rglob('*'))]:
        info = path.lstat()
        value = (os.readlink(path) if path.is_symlink() else
                 hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None)
        result[str(path.relative_to(root))] = (
            info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_mtime_ns, value)
    return result


class Fixture:
    def __init__(self, store=True):
        self.home = Path(tempfile.mkdtemp(prefix='legacy-proof-', dir=os.environ['TMPDIR']))
        self.work = self.home / 'work'
        self.work.mkdir()
        self.orch = self.home / 'orch'
        self.tests = self.orch / 'tests'
        self.tests.mkdir(parents=True)
        (self.tests / 'suites.conf').write_text('')
        for folder in ('bin', 'queue/pending', 'queue/done', 'queue/refused'):
            (self.orch / folder).mkdir(parents=True)
        for name in ('bench_store.py', 'request-runtime', 'dispatcher-daemon'):
            shutil.copy2(HERE / name, self.orch / 'bin' / name)
        for name, markers in FINITE.items():
            path = self.work / name
            path.mkdir(parents=True)
            (path / 'payload').write_text('unowned legacy: ' + name)
            for marker, value in markers.items():
                (path / marker).write_text(value)
        self.legacy_before = self.legacy()
        self.root = self.work / 'bench-store'
        self.store = core.Store.initialize(self.root, self.tests) if store else None
        self.queue = self.orch / 'queue/pending/bench-store-recovery'

    def legacy(self):
        return {name: tree(self.work / name) for name in FINITE}

    def env(self, empty=False):
        env = {} if empty else dict(os.environ)
        env.update(PATH='/usr/bin:/bin', TMPDIR=os.environ['TMPDIR'],
                   PYTHONDONTWRITEBYTECODE='1', RUNTIME_ORCH_ROOT=str(self.orch))
        return env

    def request(self, *args, empty=False):
        argv = ['bash', str(self.orch / 'bin/request-runtime'), *args]
        if empty:
            argv = ['/usr/bin/env', '-i',
                    *(key + '=' + value for key, value in self.env(True).items()), *argv]
        return subprocess.run(argv, env=self.env(empty), capture_output=True,
                              text=True, check=False)

    def dispatch(self, empty=False, fds=()):
        # Source the production function. Its daemon loop calls this exact function;
        # no daemon, process probe, test-run, maker, install or live queue is started.
        code = '''source "$1"
O=$2
W=$3
dispatch_request "$4"
printf '%s\\n' "$out"
exit "$rc"
'''
        argv = ['bash', '-c', code, 'private-dispatch',
                str(self.orch / 'bin/dispatcher-daemon'), str(self.orch),
                str(self.work), str(self.queue)]
        if empty:
            argv = ['/usr/bin/env', '-i',
                    *(key + '=' + value for key, value in self.env(True).items()), *argv]
        return subprocess.run(argv, env=self.env(empty),
                              pass_fds=fds, capture_output=True, text=True, check=False)

    def entry(self, number):
        # Synthetic identities describe only new private Store births, never a
        # reconstructed tuple for any of the seven legacy directories above.
        identity = {'remotion_tree': f'{number:040x}'}
        return self.store.ensure(
            'runtime', identity,
            {'name': f'fixture-{number}', 'env': 'ROOT={bench_path}\n',
             'suite': f'agent fixture-{number} printf fixture-{number}\n'},
            lambda stage, final: (stage / 'payload').write_text(f'owned-{number}'),
            lambda path: None)

    def pending_eviction(self, point='eviction:journal', empty=False):
        self.old = self.entry(1)
        self.current = self.entry(2)
        self.current_before = tree(Path(self.current['path']))

        def checkpoint(name):
            if name == point:
                raise Crash(name)

        self.store._checkpoint = checkpoint
        try:
            self.entry(3)
        except Crash:
            pass
        else:
            raise AssertionError('expected authentic interrupted eviction')
        self.store._checkpoint = lambda point: None
        assert self.store.journal.exists()
        assert self.request('--recover-store', empty=empty).returncode == 0

    def protected(self):
        assert self.legacy() == self.legacy_before
        assert tree(Path(self.current['path'])) == self.current_before


class LegacyRecoveryTests(unittest.TestCase):
    def test_request_dispatch_recovery_normal_and_env_i(self):
        for empty in (False, True):
            with self.subTest(env_i=empty):
                f = Fixture()
                f.pending_eviction(empty=empty)
                self.assertEqual(f.queue.read_bytes(), b'BENCHRECOVER\n')
                result = f.dispatch(empty=empty)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(Path(f.old['path']).exists())
                self.assertFalse(f.store.journal.exists())
                with self.assertRaisesRegex(core.Refused, 'registration was evicted'):
                    f.store.registered('fixture-1')
                self.assertTrue(f.store.registered('fixture-2'))
                f.protected()

    def test_interrupted_eviction_recovers_each_existing_checkpoint(self):
        for point in ('eviction:journal', 'projection:suites.conf',
                      'projection:fixture-1.env', 'index',
                      'eviction:file', 'eviction:directory'):
            with self.subTest(point=point):
                f = Fixture()
                f.pending_eviction(point)
                result = f.dispatch()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(Path(f.old['path']).exists())
                self.assertFalse(f.store.journal.exists())
                f.protected()

    def test_inherited_lease_refuses_without_writes(self):
        for empty in (False, True):
            with self.subTest(env_i=empty):
                f = Fixture()
                f.pending_eviction()
                eid = 'runtime-' + f.old['key']
                fd = f.store._lock(eid, f.old)
                try:
                    before = tree(f.root), tree(f.tests)
                    result = f.dispatch(empty=empty, fds=(fd,))
                    self.assertEqual(result.returncode, 2, result.stdout)
                    self.assertIn('REFUSED:', result.stdout)
                    self.assertEqual((tree(f.root), tree(f.tests)), before)
                    f.protected()
                finally:
                    os.close(fd)
                self.assertEqual(f.dispatch().returncode, 0)

    def test_finite_legacy_unknown_no_store_even_with_forged_markers(self):
        for variant in ('absent', 'partial', 'forged-marker', 'forged-receipt'):
            with self.subTest(variant=variant):
                f = Fixture(store=False)
                for name in FINITE:
                    path = f.work / name
                    if variant == 'partial':
                        (path / '.astrid-runtime-source-commit').write_text('a' * 40 + '\n')
                    elif variant == 'forged-marker':
                        (path / '.bench-owner.json').write_text('{"owner":"invented"}')
                    elif variant == 'forged-receipt':
                        (path / '.provision-failure').write_text('status=failed\nstage=finished\n')
                before = tree(f.work), tree(f.tests)
                self.assertEqual(f.request('--recover-store').returncode, 0)
                result = f.dispatch()
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('REFUSED:', result.stdout)
                self.assertEqual((tree(f.work), tree(f.tests)), before)
                self.assertFalse(f.root.exists())

    def test_inherited_lease_remains_after_parent_closes(self):
        f = Fixture()
        f.pending_eviction(empty=True)
        fd = f.store._lock('runtime-' + f.old['key'], f.old)
        code = '''source "$1"
O=$2
W=$3
: <&"$5" || exit 90
IFS= read -r ready || exit 91
dispatch_request "$4"
printf '%s\\n' "$out"
exit "$rc"
'''
        before = tree(f.root), tree(f.tests)
        child = subprocess.Popen(
            ['/usr/bin/env', '-i', *(key + '=' + value for key, value in f.env(True).items()),
             'bash', '-c', code, 'inherited-private-dispatch',
             str(f.orch / 'bin/dispatcher-daemon'), str(f.orch), str(f.work),
             str(f.queue), str(fd)], env=f.env(True), pass_fds=(fd,),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.close(fd)
        output, error = child.communicate('go\n', timeout=10)
        self.assertEqual(child.returncode, 2, output + error)
        self.assertIn('REFUSED:', output)
        self.assertEqual((tree(f.root), tree(f.tests)), before)
        f.protected()
        self.assertEqual(f.dispatch(empty=True).returncode, 0)

    def test_existing_store_does_not_adopt_legacy(self):
        f = Fixture()
        before = tree(f.root), tree(f.tests), f.legacy()
        self.assertEqual(f.request('--recover-store').returncode, 0)
        self.assertEqual(f.dispatch().returncode, 0)
        self.assertEqual((tree(f.root), tree(f.tests), f.legacy()), before)

    def test_no_target_force_or_cutover_input(self):
        for arg in (*FINITE, '--force', '--stamp-idle', '--adopt'):
            with self.subTest(arg=arg):
                f = Fixture()
                before = tree(f.home)
                self.assertEqual(f.request('--recover-store', arg).returncode, 2)
                self.assertEqual(tree(f.home), before)

    def test_queue_duplicate_symlink_hardlink_protected(self):
        for kind in ('regular', 'symlink', 'hardlink'):
            with self.subTest(kind=kind):
                f = Fixture()
                other = f.home / 'protected-queue-content'
                other.write_text('preserved')
                if kind == 'symlink':
                    f.queue.symlink_to(other)
                elif kind == 'hardlink':
                    os.link(other, f.queue)
                else:
                    f.queue.write_text('existing')
                before = tree(f.home)
                self.assertEqual(f.request('--recover-store').returncode, 2)
                self.assertEqual(tree(f.home), before)

    def test_metadata_substitution_refuses_without_writes(self):
        for kind in ('index-hardlink', 'mutex-substitution', 'lock-symlink',
                     'directory-substitution', 'journal-path', 'journal-owner',
                     'journal-projection', 'suite-reference-race', 'env-reference-race'):
            with self.subTest(kind=kind):
                f = Fixture()
                f.pending_eviction()
                if kind == 'index-hardlink':
                    os.link(f.root / 'index.json', f.home / 'index-alias')
                elif kind == 'mutex-substitution':
                    (f.root / 'mutex').rename(f.root / 'mutex-original')
                    (f.root / 'mutex').write_text('')
                elif kind == 'lock-symlink':
                    lock = f.root / 'locks' / ('runtime-' + f.old['key'])
                    lock.rename(f.home / 'original-lock')
                    lock.symlink_to(f.home / 'original-lock')
                elif kind == 'directory-substitution':
                    (f.root / 'entries').rename(f.home / 'entries-original')
                    (f.root / 'entries').mkdir()
                elif kind.startswith('journal-'):
                    value = json.loads(f.store.journal.read_text())
                    if kind == 'journal-path':
                        eid = value['victims'][0]
                        value['before']['entries'][eid]['path'] = str(f.work / 'venv-agent-child-s2')
                    elif kind == 'journal-owner':
                        value['owner'] = 'unknown'
                    else:
                        value['projections']['suites.conf'][1] += 'agent forged ignored\n'
                    f.store.journal.write_text(core.canonical(value))
                elif kind == 'suite-reference-race':
                    with (f.tests / 'suites.conf').open('a') as stream:
                        stream.write('agent changed printf changed\n')
                else:
                    (f.tests / 'fixture-1.env').write_text('ROOT=changed\n')
                before = tree(f.root), tree(f.tests)
                result = f.dispatch()
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('REFUSED:', result.stdout)
                self.assertEqual((tree(f.root), tree(f.tests)), before)
                self.assertEqual(f.legacy(), f.legacy_before)

    def test_payload_custody_refuses_before_projection_writes(self):
        for kind in ('missing-marker', 'partial-marker', 'forged-marker',
                     'marker-hardlink', 'marker-symlink', 'path-substitution',
                     'root-symlink', 'nonfile-marker'):
            with self.subTest(kind=kind):
                f = Fixture()
                f.pending_eviction()
                path = Path(f.old['path'])
                marker = path / '.bench-owner.json'
                if kind == 'missing-marker':
                    marker.rename(f.home / 'original-marker')
                elif kind == 'partial-marker':
                    marker.write_text('{')
                elif kind == 'forged-marker':
                    marker.write_text('{}')
                elif kind == 'marker-hardlink':
                    os.link(marker, f.home / 'marker-alias')
                elif kind == 'marker-symlink':
                    marker.rename(f.home / 'original-marker')
                    marker.symlink_to(f.home / 'original-marker')
                elif kind == 'path-substitution':
                    path.rename(f.home / 'original-payload')
                    path.mkdir()
                    (path / 'payload').write_text('substituted')
                elif kind == 'root-symlink':
                    path.rename(f.home / 'original-payload')
                    path.symlink_to(f.home / 'original-payload', target_is_directory=True)
                else:
                    marker.rename(f.home / 'original-marker')
                    marker.mkdir()
                before = tree(f.root), tree(f.tests)
                result = f.dispatch()
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn('REFUSED:', result.stdout)
                self.assertEqual((tree(f.root), tree(f.tests)), before)
                f.protected()

    def test_interrupted_creation_rollback_uses_dispatcher(self):
        for point in ('creation:stage', 'creation:publish', 'creation:seal', 'creation:index'):
            with self.subTest(point=point):
                f = Fixture()

                def checkpoint(name):
                    if name == point:
                        raise Crash(name)

                f.store._checkpoint = checkpoint
                with self.assertRaises(Crash):
                    f.entry(1)
                f.store._checkpoint = lambda point: None
                self.assertEqual(f.request('--recover-store').returncode, 0)
                result = f.dispatch()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(f.store.journal.exists())
                self.assertEqual(list((f.root / 'entries').iterdir()), [])
                self.assertEqual(list((f.root / 'staging').iterdir()), [])
                self.assertEqual((f.tests / 'suites.conf').read_text(), '')
                self.assertEqual(f.legacy(), f.legacy_before)

    def test_runtime_request_existing_call_shape_unchanged(self):
        f = Fixture()
        args = ['agent-remotion-fixture', 'a' * 40, 'b' * 64,
                '/private/agent', '/private/runtime', 'c' * 40,
                'agent-remotion-0013-nodes', '/private/node/bin']
        self.assertEqual(f.request(*args, empty=True).returncode, 0)
        self.assertEqual((f.orch / 'queue/pending/runtime-agent-remotion-fixture').read_text(),
                         'RUNTIME ' + ' '.join(args) + '\n')

    def test_dispatch_rejects_recovery_payload_extension(self):
        f = Fixture()
        f.queue.write_text('BENCHRECOVER --force\n')
        before = tree(f.home)
        result = f.dispatch()
        self.assertEqual(result.returncode, 2)
        self.assertIn('REFUSED: invalid store recovery request', result.stdout)
        self.assertEqual(tree(f.home), before)

    def test_fixture_budget(self):
        # Every fixture is tiny and resides exclusively in the harness TMPDIR.
        roots = Path(os.environ['TMPDIR']).glob('legacy-proof-*')
        total = sum(path.lstat().st_size for root in roots for path in root.rglob('*')
                    if path.is_file() and not path.is_symlink())
        self.assertLessEqual(total, 20 * 1024 * 1024)


if __name__ == '__main__':
    unittest.main(verbosity=2)
