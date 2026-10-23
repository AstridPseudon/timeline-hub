"""Private tiny lifecycle fixtures; no installed benches or services."""
import importlib.util
import hashlib
import stat
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CORE = Path(__file__).with_name('handoff-runtime-OPS-bench-store-readonly-sol-1941-bench_store.py')
if not CORE.exists():
    CORE = Path(__file__).with_name('bench_store.py')
spec = importlib.util.spec_from_file_location('core', CORE)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


def identity(n):
    return {'remotion_tree': f'{n:040x}'}


def registration(n):
    return {'name': f'bench{n}', 'env': 'BENCH={bench_path}\n', 'suite': f'agent bench{n}-nodes true\n', 'requires': []}


def build(stage, final):
    with (stage / 'payload').open('wb') as stream:
        stream.write(b'x' * 65536)
        stream.flush()
        os.fsync(stream.fileno())


def verify(path):
    assert (path / 'payload').stat().st_size == 65536


def create(store, n, builder=build, reg=None):
    return store.ensure('runtime', identity(n), reg or registration(n), builder, verify)


def assert_payload_reclaimed(root, payload):
    # Match the unique old fixture bytes, allowing inode reuse for new metadata.
    expected = hashlib.sha256(payload).digest()
    for path in root.rglob('*'):
        info = path.lstat()
        if stat.S_ISREG(info.st_mode) and info.st_size == len(payload):
            if hashlib.sha256(path.read_bytes()).digest() == expected:
                raise AssertionError('old payload retained: ' + str(path))


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='core-', dir=os.environ['TMPDIR']))
        self.tests = self.folder / 'tests'
        self.tests.mkdir()
        self.unrelated = '# approved bytes\nagent legacy true\n'
        (self.tests / 'suites.conf').write_text(self.unrelated)
        (self.tests / 'legacy.env').write_text('LEGACY=exact\n')
        self.store = core.Store.initialize(self.folder / 'store', self.tests)

    def test_reclamation_is_real_before_callback_and_failure_preserves_eviction(self):
        # Distinct old bytes let the oracle detect retained or quarantined payloads
        # without imposing a global inode allocation policy on the filesystem.
        old_payload = b'evicted-only1928' * 4096
        def old_build(stage, final):
            with (stage / 'payload').open('wb') as stream:
                stream.write(old_payload)
                stream.flush()
                os.fsync(stream.fileno())
        first = create(self.store, 1, old_build)
        second = create(self.store, 2)
        old_free = os.statvfs(self.folder).f_bavail * os.statvfs(self.folder).f_frsize
        called = []
        def fail(stage, final):
            self.assertFalse(Path(first['path']).exists())
            self.assertFalse((self.tests / 'bench1.env').exists())
            self.assertNotIn('bench1-nodes', (self.tests / 'suites.conf').read_text())
            assert_payload_reclaimed(self.store.root, old_payload)
            self.assertNotIn('runtime-' + core.runtime_key(identity(1)['remotion_tree']), self.store._load()['entries'])
            self.assertNotIn('bench1', self.store._load()['registrations'])
            free = os.statvfs(self.folder).f_bavail * os.statvfs(self.folder).f_frsize
            self.assertGreaterEqual(free, old_free + 32768)
            self.assertFalse(self.store.journal.read_text().find('"kind":"eviction"') >= 0)
            called.append(True)
            raise RuntimeError('new build failed')
        with self.assertRaisesRegex(RuntimeError, 'new build failed'):
            create(self.store, 3, fail)
        self.assertEqual(called, [True])
        self.assertFalse(Path(first['path']).exists())
        self.assertTrue(Path(second['path']).exists())
        self.assertFalse(self.store.journal.exists())
        self.assertEqual((self.tests / 'legacy.env').read_text(), 'LEGACY=exact\n')
        self.assertTrue((self.tests / 'suites.conf').read_text().startswith(self.unrelated))
        with self.assertRaises(core.Refused):
            self.store.names_for_suite('agent', 'bench1-nodes', 'true')

    def test_latest_two_plus_all_leases_and_release_reap(self):
        first = create(self.store, 1)
        second = create(self.store, 2)
        with self.store.acquire(['bench1']), self.store.acquire(['bench2']):
            third = create(self.store, 3)
            fourth = create(self.store, 4)
            self.assertTrue(all(Path(e['path']).is_dir() for e in (first, second, third, fourth)))
        create(self.store, 4)  # Reuse also runs the policy transaction.
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse(Path(second['path']).exists())
        self.assertTrue(Path(third['path']).exists())
        self.assertTrue(Path(fourth['path']).exists())

    def test_tampered_projection_refuses_before_delete_or_build(self):
        first = create(self.store, 1)
        create(self.store, 2)
        (self.tests / 'bench1.env').write_text('FORGED\n')
        with self.assertRaises(core.Refused):
            create(self.store, 3, lambda *_: self.fail('installer ran'))
        self.assertTrue(Path(first['path']).is_dir())
        self.assertFalse(self.store.journal.exists())

    def test_all_owned_registration_rows_removed_only(self):
        first = create(self.store, 1)
        alias = dict(registration(1), name='alias', suite='agent alias-suite true\n')
        create(self.store, 1, lambda *_: self.fail('duplicate build'), alias)
        create(self.store, 2)
        create(self.store, 3)
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse((self.tests / 'alias.env').exists())
        self.assertNotIn('alias-suite', (self.tests / 'suites.conf').read_text())
        with self.assertRaises(core.Refused):
            self.store.names_for_suite('agent', 'alias-suite', 'true')

    def test_exact_keys_and_immutable_registration(self):
        a, b = 'a' * 40, 'b' * 40
        old = core.child_key(a, b, {'digest': 'c'})
        self.assertNotEqual(old, core.child_key(b, b, {'digest': 'c'}))
        self.assertNotEqual(old, core.child_key(a, a, {'digest': 'c'}))
        self.assertNotEqual(old, core.child_key(a, b, {'digest': 'd'}))
        self.assertEqual(core.runtime_key(a), core.key_for('runtime', {'remotion_tree': a}))
        create(self.store, 1)
        with self.assertRaises(core.Refused):
            create(self.store, 1, reg=dict(registration(1), env='CHANGED=1\n'))
        self.assertTrue(self.store.registered('bench1'))

    def test_unknown_paths_symlinks_crosskey_and_lock_replacement(self):
        first = create(self.store, 1)
        outside = self.folder / 'outside'
        outside.mkdir()
        (outside / 'protected').write_text('safe')
        (Path(first['path']) / 'link').symlink_to(outside, target_is_directory=True)
        create(self.store, 2)
        create(self.store, 3)
        self.assertEqual((outside / 'protected').read_text(), 'safe')
        with self.assertRaises(core.Refused):
            core.Store.initialize(outside, self.tests)
        with self.assertRaises(core.Refused):
            with self.store.acquire(['../../outside']):
                self.fail('forged name accepted')
        index_path = self.store.root / 'index.json'
        index = json.loads(index_path.read_text())
        eid = next(iter(index['entries']))
        original = index_path.read_text()
        index['entries'][eid]['path'] = str(outside)
        index_path.write_text(json.dumps(index))
        with self.assertRaises(core.Refused):
            create(self.store, 4)
        index_path.write_text(original)
        lock = self.store.root / 'locks' / eid
        lock.rename(lock.with_name(lock.name + '.old'))
        lock.write_text('')
        with self.assertRaises(core.Refused):
            create(self.store, 4)
        self.assertEqual((outside / 'protected').read_text(), 'safe')

    def test_failed_verify_rolls_back_new_publication(self):
        first = create(self.store, 1)
        before = (self.tests / 'suites.conf').read_text()
        def bad_verify(path):
            raise RuntimeError('custody failed')
        with self.assertRaisesRegex(RuntimeError, 'custody failed'):
            self.store.ensure('runtime', identity(2), registration(2), build, bad_verify)
        self.assertEqual((self.tests / 'suites.conf').read_text(), before)
        self.assertTrue(Path(first['path']).exists())
        self.assertFalse((self.store.root / 'entries' / ('runtime-' + core.runtime_key(identity(2)['remotion_tree']))).exists())
        self.assertFalse(self.store.journal.exists())

    def crash_run(self, point):
        result = subprocess.run([sys.executable, '-I', str(Path(__file__).resolve()), '--crash', str(self.store.root), str(self.tests), point], capture_output=True, text=True)
        self.assertEqual(result.returncode, 73, result.stdout + result.stderr)
        self.assertTrue(self.store.journal.exists())
        with self.assertRaises(core.Refused):
            create(self.store, 4, lambda *_: self.fail('installer ran while pending'))
        self.store.recover()
        self.assertFalse(self.store.journal.exists())
        self.store._verify_projection(self.store._load())

    def test_real_crash_eviction_journal(self):
        first = create(self.store, 1)
        create(self.store, 2)
        self.crash_run('eviction:journal')
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse(self.store.registered('bench3'))

    def test_real_crash_eviction_projection(self):
        first = create(self.store, 1)
        create(self.store, 2)
        self.crash_run('projection:suites.conf')
        self.assertFalse(Path(first['path']).exists())

    def test_real_crash_eviction_index(self):
        first = create(self.store, 1)
        create(self.store, 2)
        self.crash_run('index')
        self.assertFalse(Path(first['path']).exists())

    def test_real_crash_partial_deletion(self):
        first = create(self.store, 1)
        create(self.store, 2)
        self.crash_run('eviction:file')
        self.assertFalse(Path(first['path']).exists())

    def test_real_crash_creation_publish(self):
        first = create(self.store, 1)
        create(self.store, 2)
        self.crash_run('creation:publish')
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse(self.store.registered('bench3'))
        self.assertEqual(len(self.store._load()['entries']), 1)

    def test_real_crash_creation_index_rolls_back_projection(self):
        create(self.store, 1)
        create(self.store, 2)
        self.crash_run('creation:index')
        self.assertFalse((self.tests / 'bench3.env').exists())
        self.assertFalse(self.store.registered('bench3'))

    def test_projection_write_failure_rolls_back_new_only(self):
        first = create(self.store, 1)
        create(self.store, 2)
        before = (self.tests / 'suites.conf').read_text().replace('agent bench1-nodes true\n', '')
        failed = []
        def fault(point):
            if point == 'projection:bench3.env' and not failed:
                failed.append(True)
                raise OSError('projection write failure')
        self.store._checkpoint = fault
        with self.assertRaisesRegex(OSError, 'projection write failure'):
            create(self.store, 3)
        self.assertFalse(Path(first['path']).exists())
        self.assertEqual((self.tests / 'suites.conf').read_text(), before)
        self.assertFalse((self.tests / 'bench3.env').exists())
        self.assertFalse(self.store.journal.exists())

    def test_reserve_refuses_before_callback(self):
        from unittest.mock import patch
        from collections import namedtuple
        usage = namedtuple('usage', 'total used free')
        with patch.object(core.shutil, 'disk_usage', return_value=usage(10, 10, 0)):
            with self.assertRaisesRegex(core.Refused, 'reserve'):
                create(self.store, 1, lambda *_: self.fail('installer ran'))
        self.assertFalse(self.store.journal.exists())

    def test_concurrent_same_key_builds_once(self):
        args = [sys.executable, '-I', str(Path(__file__).resolve()), '--duplicate', str(self.store.root), str(self.tests)]
        processes = [subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) for _ in range(2)]
        for process in processes:
            output, _ = process.communicate(timeout=8)
            self.assertEqual(process.returncode, 0, output)
        self.assertEqual((self.folder / 'build-count').read_text(), 'build\n')
        self.assertEqual(len(self.store._load()['entries']), 1)

    def test_forged_marker_and_suite_duplicate_refuse(self):
        first = create(self.store, 1)
        create(self.store, 2)
        marker = Path(first['path']) / '.bench-owner.json'
        original = marker.read_text()
        value = json.loads(original)
        value['key'] = 'f' * 64
        marker.write_text(json.dumps(value))
        with self.assertRaises(core.Refused):
            create(self.store, 3)
        marker.write_text(original)
        suites = self.tests / 'suites.conf'
        suites.write_text(suites.read_text() + 'agent bench1-nodes forged\n')
        with self.assertRaises(core.Refused):
            create(self.store, 3)
        self.assertTrue(Path(first['path']).exists())

    def test_before_build_crash_has_completed_reclamation(self):
        first = create(self.store, 1)
        create(self.store, 2)
        result = subprocess.run([sys.executable, '-I', str(Path(__file__).resolve()), '--crash', str(self.store.root), str(self.tests), 'before-build'])
        self.assertEqual(result.returncode, 73)
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse(self.store.journal.exists())
        self.store.recover()
        self.assertFalse(self.store.registered('bench3'))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--duplicate':
        store = core.Store(sys.argv[2], sys.argv[3])
        def counted(stage, final):
            with (store.root.parent / 'build-count').open('a') as stream:
                stream.write('build\n')
            build(stage, final)
        create(store, 1, counted)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '--crash':
        store = core.Store(sys.argv[2], sys.argv[3])
        def crash(point):
            if point == sys.argv[4]:
                os._exit(73)
        store._checkpoint = crash
        create(store, 3)
        sys.exit(99)
    unittest.main(verbosity=2)
