"""D27 ordering/removal controls in tiny fresh run-owned TMPDIR fixtures."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest

CORE = Path(__file__).with_name('handoff-runtime-OPS-bench-store-readonly-sol-1941-bench_store.py')
spec = importlib.util.spec_from_file_location('d27_core', CORE)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

class Crash(BaseException):
    pass

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix='d27-', dir=os.environ['TMPDIR']))
        self.tests = self.root / 'tests'
        self.tests.mkdir()
        (self.tests / 'suites.conf').write_text('# keep exact\n')
        self.store = core.Store.initialize(self.root / 'store', self.tests)
        self.calls = []

    def create(self, n=1):
        def build(stage, final):
            self.assertTrue(stage.stat().st_mode & stat.S_IWUSR)
            self.assertFalse(final.exists())
            (stage / 'nested').mkdir()
            (stage / 'nested/payload').write_bytes(b'd27')
            (stage / '.provision-report').write_bytes(b'status=passed\n')
            self.calls.append('build')
        def seal(final):
            self.assertEqual(final.parent, self.store.root / 'entries')
            self.assertTrue(final.is_dir())
            self.assertFalse((self.store.root / 'staging' / core.runtime_key(f'{n:040x}')).exists())
            self.assertNotIn(f'bench{n}', self.store._load(False)['registrations'])
            self.assertFalse((self.tests / 'provision' / f'bench{n}.txt').exists())
            for path in [*final.rglob('*'), final]:
                self.assertFalse(path.is_symlink())
                path.chmod(path.stat().st_mode & ~0o222)
            self.calls.append('seal')
        def verify(final):
            self.assertTrue(all(not p.lstat().st_mode & 0o222 for p in [final, *final.rglob('*')]))
            self.assertEqual((final / 'nested/payload').read_bytes(), b'd27')
            self.calls.append('verify')
        return self.store.ensure('runtime', {'remotion_tree': f'{n:040x}'},
            {'name': f'bench{n}', 'env': 'D={bench_path}\n', 'suite': f'agent bench{n} true\n',
             'report': 'status=passed\n'}, build, verify, seal=seal)

    def fault(self, point, error):
        def checkpoint(actual):
            if actual == point:
                self.store._checkpoint = lambda actual: None
                raise error()
        self.store._checkpoint = checkpoint

    def assert_rolled_back(self):
        self.assertEqual((self.tests / 'suites.conf').read_bytes(), b'# keep exact\n')
        self.assertEqual(list((self.store.root / 'entries').iterdir()), [])
        self.assertEqual(list((self.store.root / 'staging').iterdir()), [])
        self.assertFalse((self.tests / 'bench1.env').exists())
        self.assertFalse((self.tests / 'provision/bench1.txt').exists())
        self.assertFalse(self.store.journal.exists())
        self.assertEqual(self.store._load()['registrations'], {})

    def test_final_seal_precedes_verify_projection_and_reuse_never_reseals(self):
        first = self.create()
        self.assertEqual(self.calls, ['build', 'seal', 'verify'])
        self.assertEqual((self.tests / 'provision/bench1.txt').read_bytes(), b'status=passed\n')
        self.assertTrue(self.create()['reused'])
        self.assertEqual(self.calls, ['build', 'seal', 'verify', 'verify'])
        self.assertEqual(first['node'], core.inode(Path(first['path'])))
        with self.store.acquire(['bench1']) as entries:
            self.assertEqual(entries[0]['node'], first['node'])

    def test_failure_at_every_creation_boundary_rolls_back_owned_readonly(self):
        for point in ('creation:stage', 'creation:build', 'creation:publish', 'creation:seal',
                      'projection:suites.conf', 'projection:provision/bench1.txt', 'creation:index'):
            with self.subTest(point=point):
                self.fault(point, RuntimeError)
                with self.assertRaises(RuntimeError):
                    self.create()
                self.assert_rolled_back()

    def test_crash_recovery_at_every_creation_boundary(self):
        for point in ('creation:stage', 'creation:build', 'creation:publish', 'creation:seal',
                      'projection:suites.conf', 'projection:provision/bench1.txt', 'creation:index'):
            with self.subTest(point=point):
                self.fault(point, Crash)
                with self.assertRaises(Crash):
                    self.create()
                self.assertTrue(self.store.journal.exists())
                self.store.recover()
                self.assert_rolled_back()

    def test_final_verifier_refuses_incomplete_seal(self):
        original = self.store.ensure
        def unsealed(*args, **kwargs):
            kwargs['seal'] = lambda final: None
            return original(*args, **kwargs)
        self.store.ensure = unsealed
        with self.assertRaises(AssertionError):
            self.create()
        self.assert_rolled_back()

    def test_readonly_eviction_keeps_latest_two_and_lease(self):
        first = self.create(1)
        self.create(2)
        with self.store.acquire(['bench1']):
            self.create(3)
            self.assertTrue(Path(first['path']).exists())
        self.create(3)
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse((self.tests / 'provision/bench1.txt').exists())
        self.assertFalse((self.tests / 'bench1.env').exists())
        self.assertNotIn('bench1 true', (self.tests / 'suites.conf').read_text())
        self.assertEqual(len(self.store._load()['entries']), 2)

    def test_recovery_requires_stable_exclusive_creation_lock(self):
        self.fault('creation:seal', Crash)
        with self.assertRaises(Crash):
            self.create()
        entry = json.loads(self.store.journal.read_text())['new']
        fd = self.store._lock(self.store._entry_id(entry['component'], entry['key']), entry)
        try:
            with self.assertRaises(BlockingIOError):
                self.store.recover()
            self.assertFalse(Path(entry['path']).stat().st_mode & 0o222)
        finally:
            os.close(fd)
        self.store.recover()
        self.assert_rolled_back()

    def test_foreign_marker_and_symlink_refused_without_chmod(self):
        entry = self.create()
        entry.pop('reused')
        path = Path(entry['path'])
        marker = path / '.bench-owner.json'
        old = marker.read_bytes()
        marker.chmod(0o600)
        marker.write_text('{}')
        marker.chmod(0o400)
        mode = path.stat().st_mode
        with self.assertRaises(core.Refused):
            self.store._delete_owned(path, entry)
        self.assertEqual(path.stat().st_mode, mode)
        marker.chmod(0o600)
        marker.write_bytes(old)
        marker.chmod(0o400)
        moved = self.root / 'held-owned'
        # D27 allows u+w only on this run's own fixture before a fixture rename.
        path.chmod(mode | stat.S_IWUSR)
        path.rename(moved)
        moved.chmod(mode)
        foreign = self.root / 'foreign'
        foreign.mkdir(mode=0o500)
        path.symlink_to(foreign, target_is_directory=True)
        with self.assertRaises(core.Refused):
            self.store._delete_owned(path, entry)
        self.assertEqual(foreign.stat().st_mode & 0o777, 0o500)
        self.assertEqual(moved.stat().st_mode, mode)

    def test_replaced_lock_and_path_refused_before_restoring_write(self):
        entry = self.create()
        entry.pop('reused')
        path = Path(entry['path'])
        mode = path.stat().st_mode
        forged = dict(entry, path=str(self.root / 'foreign'))
        with self.assertRaises(core.Refused):
            self.store._delete_owned(path, forged)
        lock = self.store.root / 'locks' / self.store._entry_id(entry['component'], entry['key'])
        lock.rename(self.root / 'held-lock')
        lock.write_text('replacement')
        with self.assertRaises(core.Refused):
            self.store._delete_owned(path, entry)
        self.assertEqual(path.stat().st_mode, mode)

    def test_child_symlink_race_refuses_without_chmod(self):
        entry = self.create()
        entry.pop('reused')
        path = Path(entry['path'])
        nested = path / 'nested'
        mode = nested.stat().st_mode
        foreign = self.root / 'foreign'
        foreign.mkdir(mode=0o500)
        def race(point):
            if point == 'deletion:child':
                self.store._checkpoint = lambda actual: None
                nested.chmod(mode | stat.S_IWUSR)
                nested.rename(self.root / 'held-child')
                (self.root / 'held-child').chmod(mode)
                nested.symlink_to(foreign, target_is_directory=True)
        self.store._checkpoint = race
        with self.assertRaises(core.Refused):
            self.store._delete_owned(path, entry)
        self.assertEqual(foreign.stat().st_mode & 0o777, 0o500)
        self.assertEqual((self.root / 'held-child').stat().st_mode, mode)

    def test_seal_callback_failure_rolls_back_partially_sealed_tree(self):
        original = self.store.ensure
        def fail_seal(*args, **kwargs):
            seal = kwargs['seal']
            def fail(final):
                seal(final)
                raise RuntimeError('seal callback failed')
            kwargs['seal'] = fail
            return original(*args, **kwargs)
        self.store.ensure = fail_seal
        with self.assertRaisesRegex(RuntimeError, 'seal callback failed'):
            self.create()
        self.assert_rolled_back()

    def test_root_race_after_validation_refuses_without_chmod(self):
        entry = self.create()
        entry.pop('reused')
        path = Path(entry['path'])
        mode = path.stat().st_mode
        def race(point):
            if point == 'deletion:validated':
                self.store._checkpoint = lambda actual: None
                path.chmod(mode | stat.S_IWUSR)
                path.rename(self.root / 'held-owned')
                (self.root / 'held-owned').chmod(mode)
                path.mkdir(mode=0o500)
        self.store._checkpoint = race
        with self.assertRaises(core.Refused):
            self.store._delete_owned(path, entry)
        self.assertEqual(path.stat().st_mode & 0o777, 0o500)
        self.assertEqual((self.root / 'held-owned').stat().st_mode, mode)

if __name__ == '__main__':
    unittest.main(verbosity=2)
