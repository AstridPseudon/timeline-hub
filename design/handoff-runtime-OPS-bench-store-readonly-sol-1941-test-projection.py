"""Tiny writable fixtures only; no readonly child publication or services."""
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).parent

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

CORE = HERE / 'handoff-runtime-OPS-bench-store-readonly-sol-1941-bench_store.py'
if not CORE.exists():
    CORE = HERE / 'bench_store.py'
core = load(CORE, 'projection_core')
SEAM = HERE / 'handoff-runtime-OPS-bench-store-readonly-sol-1941-lease-seam.py'
if SEAM.exists():
    seam = load(SEAM, 'projection_lease')
REPORT = 'status=passed\r\nactual café {bench_path}\n'

class Crash(BaseException):
    pass

class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='projection-', dir=os.environ['TMPDIR']))
        self.tests = self.folder / 'tests'
        self.tests.mkdir()
        (self.tests / 'suites.conf').write_bytes(b'# untouched\r\nagent legacy true\n')
        (self.tests / 'legacy.env').write_bytes(b'KEEP=exact\r\n')
        self.store = core.Store.initialize(self.folder / 'store', self.tests)

    def create(self, n, report=REPORT, **fields):
        def build(stage, final):
            (stage / 'payload').write_bytes(b'x')
            (stage / '.provision-report').write_bytes(REPORT.encode())
        def verify(path):
            self.assertEqual((path / '.provision-report').read_bytes(), REPORT.encode())
        reg = dict(name=f'bench{n}', env='PATH={bench_path}\n', suite=f'agent bench{n} true\n')
        if report is not Ellipsis:
            reg['report'] = report
        reg.update(fields)
        return self.store.ensure('runtime', {'remotion_tree': f'{n:040x}'}, reg, build, verify)

    def report_path(self, n):
        return self.tests / 'provision' / f'bench{n}.txt'

    def crash_at(self, target):
        def checkpoint(point):
            if point == target:
                raise Crash()
        self.store._checkpoint = checkpoint

    def test_exact_report_callback_reuse_and_controls(self):
        entry = self.create(1)
        self.assertEqual(self.report_path(1).read_bytes(), REPORT.encode())
        self.assertTrue(self.create(1)['reused'])
        reg = self.store._load()['registrations']['bench1']
        self.assertEqual(reg['report_sha256'], core.digest(REPORT))
        self.assertEqual((self.tests / 'bench1.env').read_text(), f"PATH={entry['path']}\n")
        self.assertEqual((self.tests / 'legacy.env').read_bytes(), b'KEEP=exact\r\n')
        self.assertTrue((self.tests / 'suites.conf').read_bytes().startswith(b'# untouched\r\nagent legacy true\n'))

    def test_empty_absent_report_preserves_old_metadata(self):
        self.create(1, '')
        self.create(2, Ellipsis)
        self.assertFalse((self.tests / 'provision').exists())
        for reg in self.store._load()['registrations'].values():
            self.assertEqual(set(reg), {'env', 'suite', 'requires', 'hash'})

    def test_absent_report_leaves_foreign_same_name_bytes_untouched(self):
        (self.tests / 'provision').mkdir()
        self.report_path(1).write_bytes(b'preexisting unrelated\r\n')
        self.create(1, Ellipsis)
        self.create(2, '')
        self.create(3, '')
        self.assertEqual(self.report_path(1).read_bytes(), b'preexisting unrelated\r\n')

    def test_type_size_source_claim_and_path_refused(self):
        for value in (None, b'bytes', 3, 'x' * (core.Store.REPORT_LIMIT + 1), 'forged'):
            with self.subTest(value=type(value).__name__):
                with self.assertRaises(core.Refused):
                    self.create(1, value)
                self.assertFalse(self.report_path(1).exists())
        with self.assertRaises(core.Refused):
            self.create(1, name='../outside')
        self.assertFalse(self.store.journal.exists())

    def test_foreign_fixed_path_and_directory_symlink(self):
        folder = self.tests / 'provision'
        folder.mkdir()
        self.report_path(1).write_bytes(b'foreign')
        with self.assertRaises(core.Refused):
            self.create(1)
        self.assertEqual(self.report_path(1).read_bytes(), b'foreign')
        self.assertFalse(self.store.journal.exists())
        folder.rename(self.tests / 'saved-provision')
        folder.symlink_to(self.tests / 'saved-provision', target_is_directory=True)
        with self.assertRaises(core.Refused):
            self.create(1)
        self.assertEqual((self.tests / 'saved-provision' / 'bench1.txt').read_bytes(), b'foreign')

    def test_report_symlink_hardlink_directory_and_oversize_refuse(self):
        self.create(1)
        report = self.report_path(1)
        report.rename(report.with_suffix('.saved'))
        report.symlink_to(report.with_suffix('.saved'))
        with self.assertRaises((core.Refused, OSError)):
            self.create(2)
        report.unlink()
        os.link(report.with_suffix('.saved'), report)
        with self.assertRaises(core.Refused):
            self.create(2)
        report.unlink()
        report.mkdir()
        with self.assertRaises(core.Refused):
            self.create(2)
        report.rmdir()
        report.write_bytes(b'x' * (core.Store.REPORT_LIMIT + 1))
        with self.assertRaises(core.Refused):
            self.create(2)

    def test_tamper_refuses_before_any_changes(self):
        first = self.create(1)
        self.create(2)
        baseline = {p: p.read_bytes() for p in (self.store.root / 'index.json', self.tests / 'suites.conf', self.tests / 'bench1.env')}
        self.report_path(1).write_bytes(b'tampered')
        with self.assertRaises(core.Refused):
            self.create(3)
        self.assertTrue(Path(first['path']).exists())
        self.assertEqual(baseline, {p: p.read_bytes() for p in baseline})
        with self.assertRaises(core.Refused):
            with self.store.acquire(['bench1']):
                self.fail('tampered report leased')

    def test_eviction_removes_all_only_owned_report_and_held_survives(self):
        first = self.create(1)
        self.create(1, name='alias', suite='agent alias true\n')
        unrelated = self.tests / 'provision' / 'foreign.txt'
        unrelated.write_bytes(b'foreign\r\n')
        self.create(2)
        with self.store.acquire(['bench1']):
            self.create(3)
            self.assertTrue(self.report_path(1).exists())
        self.create(3)
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse(self.report_path(1).exists())
        self.assertFalse((self.tests / 'provision' / 'alias.txt').exists())
        self.assertEqual(unrelated.read_bytes(), b'foreign\r\n')
        self.assertEqual(self.report_path(2).read_bytes(), REPORT.encode())
        self.assertEqual(self.report_path(3).read_bytes(), REPORT.encode())

    def test_creation_report_crash_rolls_back_exact_bytes(self):
        self.create(1)
        baseline = {p: p.read_bytes() for p in (self.report_path(1), self.tests / 'suites.conf', self.tests / 'bench1.env')}
        self.crash_at('projection:provision/bench2.txt')
        with self.assertRaises(Crash):
            self.create(2)
        self.assertEqual(self.report_path(2).read_bytes(), REPORT.encode())
        self.store._checkpoint = lambda _: None
        self.store.recover()
        self.assertFalse(self.report_path(2).exists())
        self.assertFalse((self.tests / 'bench2.env').exists())
        self.assertEqual(baseline, {p: p.read_bytes() for p in baseline})

    def test_eviction_report_crash_recovers_forward(self):
        first = self.create(1)
        self.create(2)
        self.crash_at('projection:provision/bench1.txt')
        with self.assertRaises(Crash):
            self.create(3)
        self.store._checkpoint = lambda _: None
        self.store.recover()
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse(self.report_path(1).exists())
        self.assertEqual(self.report_path(2).read_bytes(), REPORT.encode())
        self.assertFalse(self.report_path(3).exists())

    def test_pending_report_hash_mutation_refuses_without_writes(self):
        self.create(1)
        self.crash_at('creation:index')
        with self.assertRaises(Crash):
            self.create(2)
        self.store._checkpoint = lambda _: None
        pending = self.store.journal.read_bytes()
        index = (self.store.root / 'index.json').read_bytes()
        self.report_path(2).write_bytes(b'changed while pending')
        with self.assertRaises(core.Refused):
            self.store.recover()
        self.assertEqual(self.store.journal.read_bytes(), pending)
        self.assertEqual((self.store.root / 'index.json').read_bytes(), index)
        self.report_path(2).write_bytes(REPORT.encode())
        journal = json.loads(pending)
        journal['after']['registrations']['bench2']['report'] = 'forged'
        self.store.journal.write_text(json.dumps(journal))
        with self.assertRaisesRegex(core.Refused, 'report hash'):
            self.store.recover()

    def test_custom_existing_row_leases_all_managed_dependencies_real_flock(self):
        first = self.create(1, suite='')
        self.create(2, suite='')
        command = f"env BENCH_PATH={first['path']} true"
        with (self.tests / 'suites.conf').open('a') as stream:
            stream.write('agent custom ' + command + '\n')
        names = self.store.names_for_suite('agent', 'custom', command)
        self.assertEqual(names, ['bench1', 'bench2'])
        with seam.suite_lease(self.store, 'agent', 'custom', command, self.tests) as (entries, fds):
            self.assertEqual(len(entries), 2)
            process = subprocess.Popen([sys.executable, '-c', 'import sys; print("ready", flush=True); sys.stdin.buffer.read(1)'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, pass_fds=tuple(e['lease_fd'] for e in entries))
            self.assertEqual(process.stdout.readline(), b'ready\n')
        try:
            self.create(3, suite='')
            self.assertTrue(Path(first['path']).exists())
            self.assertTrue(self.report_path(1).exists())
        finally:
            process.communicate(b'x', timeout=5)
        self.assertEqual(process.returncode, 0)
        self.create(3, suite='')
        self.assertFalse(Path(first['path']).exists())
        with self.assertRaises(core.Refused):
            self.store.names_for_suite('agent', 'missing', 'true')

    def test_real_process_crash_report_rollback(self):
        self.create(1)
        result = subprocess.run([sys.executable, '-I', '-B', str(Path(__file__).resolve()), '--crash-report',
                                 str(self.store.root), str(self.tests), 'projection:provision/crash-child.txt'], capture_output=True)
        self.assertEqual(result.returncode, 73, result.stderr)
        child_report = self.tests / 'provision' / 'crash-child.txt'
        self.assertEqual(child_report.read_bytes(), REPORT.encode())
        self.store.recover()
        self.assertFalse(child_report.exists())
        self.assertEqual(self.report_path(1).read_bytes(), REPORT.encode())

    def test_frozen_baseline_custom_row_old_red(self):
        original = load(HERE / 'handoff-runtime-OPS-bench-store-core-precondition-1858-bench_store.py', 'frozen_core')
        self.store = original.Store(self.store.root, self.tests)
        first = self.create(1, Ellipsis, suite='')
        self.create(2, Ellipsis, suite='')
        command = f"env BENCH_PATH={first['path']} true"
        with (self.tests / 'suites.conf').open('a') as stream:
            stream.write('agent custom ' + command + '\n')
        self.assertEqual(self.store.names_for_suite('agent', 'custom', command), [])
        with seam.suite_lease(self.store, 'agent', 'custom', command, self.tests) as (entries, fds):
            self.assertEqual(entries, [])
            process = subprocess.Popen([sys.executable, '-c', 'import sys; print("ready", flush=True); sys.stdin.buffer.read(1)'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, pass_fds=tuple(fds))
            self.assertEqual(process.stdout.readline(), b'ready\n')
        try:
            self.create(3, Ellipsis, suite='')
            self.assertFalse(Path(first['path']).exists())  # Baseline RED reproduction.
        finally:
            process.communicate(b'x', timeout=5)
        self.assertEqual(process.returncode, 0)

    def test_missing_tampered_managed_row_never_falls_through(self):
        self.create(1)
        suites = self.tests / 'suites.conf'
        original = suites.read_text()
        for replacement in ('', 'agent bench1 forged\n'):
            suites.write_text(original.replace('agent bench1 true\n', replacement))
            with self.assertRaises(core.Refused):
                self.store.names_for_suite('agent', 'bench1', 'true')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--crash-report':
        store = core.Store(sys.argv[2], sys.argv[3])
        def crash(point):
            if point == sys.argv[4]:
                os._exit(73)
        store._checkpoint = crash
        def build(stage, final):
            (stage / '.provision-report').write_bytes(REPORT.encode())
        def verify(path):
            assert (path / '.provision-report').read_bytes() == REPORT.encode()
        store.ensure('child', {'agent_sha': 'a' * 40, 'backend_sha': 'b' * 40, 'client_tuple': {'sha256': 'c' * 64}},
                     {'name': 'crash-child', 'env': '', 'suite': '', 'report': REPORT}, build, verify)
        sys.exit(99)
    unittest.main(verbosity=2)
