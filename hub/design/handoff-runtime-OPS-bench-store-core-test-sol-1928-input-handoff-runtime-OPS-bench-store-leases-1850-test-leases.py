"""Private tiny fixtures. No real Git, service, bench, sockets or test body."""
import hashlib
import importlib.util
import os
from pathlib import Path
import signal
import shlex
import subprocess
import sys
import tempfile
import time
import unittest

sys.dont_write_bytecode = True
PREFIX = Path(__file__).with_name('handoff-runtime-OPS-bench-store-leases-1850-')
CORE = Path(__file__).with_name('handoff-runtime-OPS-bench-store-core-resume-1854-bench_store.py')
STAGED = Path(str(PREFIX) + 'test-run')
ORIGINAL = Path(str(PREFIX) + 'test-run.original')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def seam():
    source = STAGED.read_text().split("<<'BENCH_LEASE_PY'\n", 1)[1].split('\nBENCH_LEASE_PY\n', 1)[0]
    namespace = {'__name__': 'fixture_seam'}
    exec(compile(source, str(STAGED) + ':embedded', 'exec'), namespace)
    return namespace


def wait_for(path, process=None):
    until = time.monotonic() + 8
    while not path.exists():
        if process is not None and process.poll() is not None:
            raise AssertionError('holder exited early: ' + process.communicate()[0])
        if time.monotonic() >= until:
            raise AssertionError('timed out waiting for ' + str(path))
        time.sleep(.02)


def identity(number, component='runtime'):
    if component == 'runtime':
        return {'remotion_tree': f'{number:040x}'}
    return {'agent_sha': f'{number:040x}', 'backend_sha': 'b' * 40,
            'client_tuple': {'version': 'fixture', 'digest': 'tiny'}}


def create(store, number, name=None, component='runtime', requires=()):
    name = name or f'bench{number}'
    def build(stage, final):
        (Path(stage) / 'tiny').write_text('fixture')
    def verify(path):
        assert (Path(path) / 'tiny').read_text() == 'fixture'
    return store.ensure(component, identity(number, component),
                        {'name': name, 'env': 'FIXTURE={bench_path}\n',
                         'suite': f'agent {name} true\n', 'requires': list(requires)}, build, verify)


class LeaseTests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='lease-', dir=os.environ['TMPDIR']))
        self.tests = self.folder / 'tests'
        self.tests.mkdir()
        (self.tests / 'suites.conf').write_text('# unrelated exact bytes\nagent legacy true\n')
        (self.folder / 'bin').mkdir()
        (self.folder / 'bin/bench_store.py').symlink_to(CORE)
        self.core = load(CORE, 'fixture_core')
        self.store = self.core.Store.initialize(self.folder / 'store', self.tests)
        if self.store is None:
            self.store = self.core.Store(self.folder / 'store', self.tests)
        self.processes = []

    def tearDown(self):
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
            try:
                process.communicate(timeout=8)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=8)

    def holder(self, script, suite='bench1'):
        ready = self.folder / f'ready{len(self.processes)}'
        cancel = self.folder / f'cancel{len(self.processes)}'
        process = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--holder',
                                    str(self.folder / 'store'), str(self.tests), suite, str(cancel),
                                    'bash', '-c', script, 'fixture', str(ready)],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.processes.append(process)
        wait_for(ready, process)
        return process, cancel

    def retained_then_released(self, script, expected, cancel=False):
        first = create(self.store, 1)
        create(self.store, 2)
        with self.store.acquire(['bench1']) as entries:
            stat = os.fstat(entries[0]['lease_fd'])
            locks = [path for path in (self.folder / 'store').rglob('*')
                     if path.is_file() and (path.stat().st_dev, path.stat().st_ino) == (stat.st_dev, stat.st_ino)]
        self.assertEqual(len(locks), 1, 'stable lock inode not found')
        process, marker = self.holder(script)
        self.assertEqual(subprocess.run(['flock', '-n', '-x', str(locks[0]), 'true']).returncode, 1)
        third = create(self.store, 3)
        self.assertTrue(Path(first['path']).is_dir(), 'live bench evicted')
        self.assertTrue(Path(third['path']).is_dir())
        if cancel:
            marker.touch()
        output, _ = process.communicate(timeout=9)
        self.assertEqual(process.returncode, expected, output)
        self.assertEqual(subprocess.run(['flock', '-n', '-x', str(locks[0]), 'true']).returncode, 0)
        create(self.store, 4)
        self.assertFalse(Path(first['path']).exists(), 'released oldest bench retained')

    def test_normal_and_descendant_lifetime(self):
        self.retained_then_released('sleep .7 & echo ready > "$1"; exit 0', 0)

    def test_fake_snapshot_setup_is_leased(self):
        first = create(self.store, 1)
        create(self.store, 2)
        process, _ = self.holder('echo setup > "$1"; sleep .5; echo command; exit 0')
        create(self.store, 3)
        self.assertTrue(Path(first['path']).is_dir())
        output, _ = process.communicate(timeout=8)
        self.assertEqual(process.returncode, 0, output)
        self.assertIn('command', output)

    def test_exact_shell_suite_branch_uses_inherited_lease(self):
        first = create(self.store, 1)
        create(self.store, 2)
        source = STAGED.read_text()
        start = source.index('if [ -n "$BENCH_CONTROL_FD" ]; then')
        end = source.index('[ -n "$LEASED" ] && exit "$RC"', start)
        branch = source[start:end]
        command = f'echo ready > {self.folder}/ready0; sleep .5; exit 7'
        script = f'SNAP={self.folder}; D={self.folder}; CMD={shlex.quote(command)};\n' + branch + '\nexit "$RC"'
        process, _ = self.holder(script)
        create(self.store, 3)
        self.assertTrue(Path(first['path']).is_dir())
        output, _ = process.communicate(timeout=8)
        self.assertEqual(process.returncode, 7, output)

    def test_exact_shell_suite_branch_cancel_releases_timeout_group(self):
        first = create(self.store, 1)
        create(self.store, 2)
        source = STAGED.read_text()
        start = source.index('if [ -n "$BENCH_CONTROL_FD" ]; then')
        end = source.index('[ -n "$LEASED" ] && exit "$RC"', start)
        command = f'echo ready > {self.folder}/ready0; sleep 30'
        script = f'SNAP={self.folder}; D={self.folder}; CMD={shlex.quote(command)};\n' + source[start:end] + '\nexit "$RC"'
        process, marker = self.holder(script)
        create(self.store, 3)
        self.assertTrue(Path(first['path']).is_dir())
        marker.touch()
        output, _ = process.communicate(timeout=8)
        self.assertEqual(process.returncode, 130, output)
        create(self.store, 4)
        self.assertFalse(Path(first['path']).exists())

    def test_symlink_store_root_refuses_before_command(self):
        create(self.store, 1)
        alias = self.folder / 'alias'
        alias.symlink_to(self.folder / 'store', target_is_directory=True)
        ready = self.folder / 'must-not-run'
        result = subprocess.run([sys.executable, '-I', str(Path(str(PREFIX) + 'lease-seam.py')),
                                 str(self.folder), str(alias), 'agent', 'bench1', 'true',
                                 str(os.getpid()), str(self.folder / 'CANCELLED'),
                                 'bash', '-c', f'echo unsafe > {ready}'], capture_output=True, text=True, timeout=8)
        self.assertEqual(result.returncode, 125, result.stdout + result.stderr)
        self.assertFalse(ready.exists())

    def test_failure_release(self):
        self.retained_then_released('echo ready > "$1"; sleep .35; exit 7', 7)

    def test_suite_exit_125_is_preserved(self):
        self.retained_then_released('echo ready > "$1"; sleep .35; exit 125', 125)
        self.assertIn('BENCH-LEASE-RESULT', STAGED.read_text())

    def test_exact_python_entry_distinguishes_refusal_from_suite_125(self):
        create(self.store, 1)
        exported = Path(str(PREFIX) + 'lease-seam.py')
        args = [sys.executable, '-I', str(exported), str(self.folder), str(self.folder / 'store'),
                'agent', 'bench1', 'true', str(os.getpid()), str(self.folder / 'CANCELLED'),
                'bash', '-c', 'exit 125']
        result = subprocess.run(args, capture_output=True, text=True, timeout=8)
        self.assertEqual(result.returncode, 125, result.stdout + result.stderr)
        self.assertEqual((self.folder / 'BENCH-LEASE-RESULT').read_text(), 'complete\n')
        (self.tests / 'bench1.env').write_text('FORGED=1\n')
        result = subprocess.run(args, capture_output=True, text=True, timeout=8)
        self.assertEqual(result.returncode, 125, result.stdout + result.stderr)
        self.assertEqual((self.folder / 'BENCH-LEASE-RESULT').read_text(), 'error\n')

    def test_timeout_release(self):
        self.retained_then_released('echo ready > "$1"; timeout -k 1 .35 sleep 10', 124)

    def test_cancel_release(self):
        self.retained_then_released('echo ready > "$1"; sleep 30', 130, cancel=True)

    def test_term_release(self):
        first = create(self.store, 1)
        create(self.store, 2)
        process, _ = self.holder('echo ready > "$1"; sleep 30')
        process.terminate()
        output, _ = process.communicate(timeout=8)
        self.assertEqual(process.returncode, 130, output)
        create(self.store, 3)
        self.assertFalse(Path(first['path']).exists())

    def test_sigkill_inherited_fd_retains_until_command_finishes(self):
        first = create(self.store, 1)
        create(self.store, 2)
        process, _ = self.holder('echo ready > "$1"; sleep .8')
        process.kill()
        process.wait(timeout=3)
        create(self.store, 3)
        self.assertTrue(Path(first['path']).is_dir())
        time.sleep(1)
        create(self.store, 4)
        self.assertFalse(Path(first['path']).exists())

    def test_two_components_held(self):
        runtime = create(self.store, 1)
        child = create(self.store, 1, 'duo', 'child',
                       [{'component': 'runtime', 'key': runtime['key']}])
        create(self.store, 2)
        create(self.store, 2, 'child2', 'child')
        process, _ = self.holder('echo ready > "$1"; sleep .6', 'duo')
        create(self.store, 3)
        create(self.store, 3, 'child3', 'child')
        self.assertTrue(Path(runtime['path']).is_dir())
        self.assertTrue(Path(child['path']).is_dir())
        self.assertEqual(process.wait(timeout=8), 0)

    def test_forged_registration_and_path_refuse(self):
        first = create(self.store, 1)
        (self.tests / 'bench1.env').write_text('FORGED=1\n')
        with self.assertRaises(Exception):
            with seam()['suite_lease'](self.store, 'agent', 'bench1', 'true', self.tests):
                self.fail('forged registration acquired')
        self.assertTrue(Path(first['path']).is_dir())

    def test_path_name_refuses(self):
        create(self.store, 1)
        with self.assertRaises(Exception):
            with self.store.acquire(['../../outside']):
                self.fail('path acquired')

    def test_original_row_whitespace_is_bound_without_changing_command(self):
        def build(stage, final):
            (Path(stage) / 'tiny').write_text('fixture')
        self.store.ensure('runtime', identity(1),
                          {'name': 'spaced', 'env': '', 'suite': "agent spaced printf 'x  y'\n", 'requires': []},
                          build, lambda path: None)
        with seam()['suite_lease'](self.store, 'agent', 'spaced', "printf 'x y'", self.tests) as (entries, fds):
            self.assertEqual(len(entries), 1)
            self.assertEqual(len(fds), 1)

    def test_resolve_then_eviction_refuses_before_command(self):
        create(self.store, 1)
        create(self.store, 2)
        names = self.store.names_for_suite('agent', 'bench1', 'true')
        create(self.store, 3)
        with self.assertRaises(Exception):
            with self.store.acquire(names):
                self.fail('evicted resolved registration acquired')
        with self.assertRaises(Exception):
            with seam()['suite_lease'](self.store, 'agent', 'bench1', 'true', self.tests):
                self.fail('removed managed suite became legacy')

    def test_unregistered_existing_suite_has_no_lease(self):
        with seam()['suite_lease'](self.store, 'agent', 'legacy', 'true', self.tests) as (entries, fds):
            self.assertEqual((entries, fds), ([], []))

    def check_cached_branch_and_original_guards(self):
        source, original = STAGED.read_text(), ORIGINAL.read_text()
        start = original.index('  if [ $nocache = 0 ]')
        end = original.index('  [ -f $C/$KEY.running ]', start)
        branch = original[start:end]
        self.assertIn(branch, source)
        cache = self.folder / 'cache'
        cache.mkdir()
        src, dest = self.folder / 'cached', self.folder / 'new'
        src.mkdir()
        dest.mkdir()
        for filename, text in [('summary', 'tiny result'), ('exit', '0'), ('status', 'pass'), ('log.txt', '1 passed')]:
            (src / filename).write_text(text)
        (cache / 'key').write_text('cached')
        # The exact cache-hit block returns before the lease seam; no module can load.
        env = dict(os.environ, nocache='0', C=str(cache), KEY='key', O=str(self.folder),
                   D=str(dest), TREE='tree', ID='cached-fixture')
        branch = branch.replace('SRC=$O/tests/', 'SRC=$O/')
        result = subprocess.run(['bash', '-c', branch + '\nexit 93'], env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((dest / 'status').read_text(), 'pass')
        queue = original[original.index('if [ -z "$RUN" ]; then'):original.index('echo $$ > $D/running; SNAP=')]
        self.assertIn(queue, source)
        tail = original[original.index('git -C $W worktree remove --force $SNAP'):]
        self.assertTrue(source.endswith(tail))
        self.assertLess(source.index('  if [ $nocache = 0 ]'), source.index('# BENCH-LEASE-BEGIN'))
        self.assertIn('BASE_CMD=$CMD\nOK=', source)
        self.assertEqual(source.count('bash -c "$CMD"'), 2)

    def test_parent_death_releases_after_stopping_command(self):
        first = create(self.store, 1)
        create(self.store, 2)
        ready = self.folder / 'parent-ready'
        parent = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--parent',
                                   str(self.folder / 'store'), str(self.tests), str(ready)],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.processes.append(parent)
        wait_for(ready, parent)
        parent.kill()
        parent.communicate(timeout=8)
        create(self.store, 3)
        self.assertFalse(Path(first['path']).exists())

    def test_simultaneous_acquire_and_evict(self):
        first = create(self.store, 1)
        create(self.store, 2)
        ready = self.folder / 'race-ready'
        command = f'test -f {first["path"]}/tiny || exit 99; echo ready > "$1"; sleep .25; test -f {first["path"]}/tiny || exit 98'
        holder = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--holder',
                                   str(self.folder / 'store'), str(self.tests), 'bench1',
                                   str(self.folder / 'cancel-race'), 'bash', '-c', command, 'fixture', str(ready)],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.processes.append(holder)
        evictor = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--evict',
                                    str(self.folder / 'store'), str(self.tests)],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.processes.append(evictor)
        evict_output, _ = evictor.communicate(timeout=8)
        output, _ = holder.communicate(timeout=8)
        self.assertEqual(evictor.returncode, 0, evict_output)
        self.assertIn(holder.returncode, (0, 125), output)
        self.assertEqual(ready.exists(), holder.returncode == 0)


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='source-', dir=os.environ['TMPDIR']))

    test_cached_branch_and_original_guards = LeaseTests.check_cached_branch_and_original_guards


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--evict':
        core = load(CORE, 'evict_core')
        create(core.Store(sys.argv[2], sys.argv[3]), 3)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '--parent':
        root, tests, ready = sys.argv[2:]
        child = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--holder',
                                  root, tests, 'bench1', ready + '.cancel', 'bash', '-c',
                                  'echo ready > "$1"; sleep 30', 'fixture', ready])
        sys.exit(child.wait())
    if len(sys.argv) > 1 and sys.argv[1] == '--holder':
        root, tests, suite, cancelled, *argv = sys.argv[2:]
        try:
            sys.argv = ['production-embedded', str(Path(tests).parent), root, 'agent', suite,
                        'true', str(os.getppid()), cancelled, *argv]
            result = seam()['main']()
            sys.exit(result)
        except Exception as exc:
            print('BENCH-LEASE REFUSED:', exc)
            sys.exit(125)
    dependency_hash = hashlib.sha256(CORE.read_bytes()).hexdigest()
    result = unittest.main(verbosity=2, exit=False)
    if hashlib.sha256(CORE.read_bytes()).hexdigest() != dependency_hash:
        raise AssertionError('core source changed during fixture run; qualification invalid')
    print('core_sha256=' + dependency_hash)
    sys.exit(0 if result.result.wasSuccessful() else 1)
