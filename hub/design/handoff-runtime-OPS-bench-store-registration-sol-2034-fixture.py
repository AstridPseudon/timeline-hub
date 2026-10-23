"""Finite private OPS-bench-store registration proof; stdlib, no live operations."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
EVIDENCE = ORCH / 'design'
PREFIX = 'handoff-ap2-OPS-retired-registrations-1841-'
PACKET = 'handoff-runtime-OPS-bench-store-registration-sol-2034-'
CORE = HERE / 'bench_store.py'
CALLER = HERE / 'test-run'
if Path(__file__).name.startswith(PACKET):
    CORE = HERE / (PACKET + 'core.py')
    CALLER = HERE / (PACKET + 'test-run')
SPEC = importlib.util.spec_from_file_location('registration_core', CORE)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
ORIGINAL = (EVIDENCE / (PREFIX + 'evidence-suites.conf.original')).read_bytes()
assert hashlib.sha256(ORIGINAL).hexdigest() == '07dfac86a0a63b3449a5d3393327ea95cc5688c342413fe1d9e323f3cfd9a330'
ENVS = {name: (EVIDENCE / (PREFIX + 'evidence-' + name + '.env.original')).read_bytes()
        for name in core.Store.UNREGISTER}
for name, value in ENVS.items():
    assert hashlib.sha256(value).hexdigest() == core.Store.UNREGISTER[name]['env_sha256']
NAMES = sorted(ENVS)
POINTS = ['unregistration:journal', 'projection:suites.conf',
          *('projection:' + name + '.env' for name in NAMES), 'index']


def sha(value):
    return hashlib.sha256(value).hexdigest()


class Crash(BaseException):
    pass


class Fixture:
    def __init__(self, unknown=False):
        self.home = Path(tempfile.mkdtemp(prefix='registration-', dir=os.environ['TMPDIR']))
        self.tests = self.home / 'tests'
        if unknown:
            self.tests.mkdir()
            (self.tests / 'suites.conf').write_bytes(ORIGINAL)
        self.store = core.Store.initialize(self.home / 'store', self.tests)
        with self.store.mutex():
            (self.tests / 'suites.conf').write_bytes(ORIGINAL)
            for name, value in ENVS.items():
                (self.tests / (name + '.env')).write_bytes(value)
            for name in ('agent-remotion-ap2-current-079-2a9-1743', 'P1', 'P2', 'P3', 'F',
                         'agent-remotion', 'agent-remotion-current', 'generaltemplate'):
                (self.tests / (name + '.env')).write_text('PROTECTED=' + name + '\n')
        self.legacy = self.home / 'legacy'
        self.legacy.mkdir()
        for name in NAMES:
            folder = self.legacy / name
            folder.mkdir()
            # All seven deliberately share one Remotion content identity.
            (folder / 'remotion-key').write_text('a' * 40 + '\n')
            (folder / 'payload').write_bytes(b'legacy must stay exact\x00' + name.encode())
        self.legacy_before = self.tree(self.legacy)
        self.outside = {p.name: p.read_bytes() for p in self.tests.iterdir()
                        if p.name != 'suites.conf' and p.stem not in ENVS}
        self.request = {'names': dict(core.Store.UNREGISTER), 'suites_sha256': sha(ORIGINAL)}
        self.request_path = self.home / 'request.json'
        self.request_path.write_text(json.dumps(self.request))

    @staticmethod
    def tree(root):
        return {str(p.relative_to(root)): (p.stat().st_mode, p.stat().st_ino,
                                          p.read_bytes() if p.is_file() else None)
                for p in [root, *root.rglob('*')]}

    def same_legacy_outside(self):
        assert self.tree(self.legacy) == self.legacy_before
        assert {name: (self.tests / name).read_bytes() for name in self.outside} == self.outside

    def unchanged(self):
        assert (self.tests / 'suites.conf').read_bytes() == ORIGINAL
        assert {name: (self.tests / (name + '.env')).read_bytes() for name in NAMES} == ENVS
        self.same_legacy_outside()

    def success(self):
        rows = ORIGINAL.decode().splitlines(keepends=True)
        expected = ''.join(row for row in rows
                           if row.split(None, 2)[:2] not in [['agent', n + '-nodes'] for n in NAMES])
        assert (self.tests / 'suites.conf').read_text() == expected
        assert all(not (self.tests / (name + '.env')).exists() for name in NAMES)
        index = json.loads((self.store.root / 'index.json').read_text())
        assert index['entries'] == {} and index['registrations'] == {}
        assert index['retired'] == NAMES
        assert not self.store.journal.exists()
        self.same_legacy_outside()

    def cli(self, empty_env=False):
        env = {'PATH': '/usr/bin:/bin', 'TMPDIR': os.environ['TMPDIR'],
               'PYTHONDONTWRITEBYTECODE': '1'} if empty_env else dict(os.environ)
        return subprocess.run([sys.executable, '-I', str(CORE),
                               '--root', str(self.store.root), '--tests-dir', str(self.tests),
                               'unregister', '--request', str(self.request_path)],
                              env=env, capture_output=True, text=True, check=False)


def caller_module():
    source = CALLER.read_text().split("<<'BENCH_LEASE_PY'\n", 1)[1].split('\nBENCH_LEASE_PY', 1)[0]
    namespace = {'__name__': 'private_test_run'}
    exec(compile(source, 'private-test-run-heredoc', 'exec'), namespace)
    return namespace


def caller_shape():
    fixture = Fixture()
    caller = caller_module()
    row = next(row for row in ORIGINAL.decode().splitlines()
               if row.split(None, 2)[:2] == ['agent', NAMES[0] + '-nodes'])
    command = ' '.join(row.split(None, 2)[2].split())
    with caller['suite_lease'](fixture.store, 'agent', NAMES[0] + '-nodes', command,
                               fixture.tests) as (entries, fds):
        assert not entries and len(fds) == 1
        # Actual production supervisor, safe private argv (never the evidence shell).
    result = caller['supervise'](fixture.store, 'agent', NAMES[0] + '-nodes', command,
                                 [sys.executable, '-c', 'raise SystemExit(0)'],
                                 fixture.home / 'CANCELLED', os.getppid(), fixture.tests)
    assert result == 0
    result = fixture.cli()
    assert result.returncode == 0, result.stderr
    fixture.success()
    print('PASS real test-run prelease/supervisor -> CLI exact-seven transaction')


class RegistrationTests(unittest.TestCase):
    def test_exact_seven_shared_key_success_and_no_retry(self):
        f = Fixture()
        f.store.unregister(f.request)
        f.success()
        with self.assertRaises(core.Refused):
            f.store.unregister(f.request)
        f.success()

    def test_existing_managed_shared_key_and_all_metadata_preserved(self):
        f = Fixture()
        def build(stage, final):
            (stage / 'payload').write_text('existing managed runtime')
        def verify(path):
            assert (path / 'payload').read_text() == 'existing managed runtime'
        f.store.ensure('runtime', {'remotion_tree': 'a' * 40},
                       {'name': 'current-managed', 'env': 'BENCH={bench_path}\n',
                        'suite': 'agent current-managed true\n'}, build, verify)
        before = json.loads((f.store.root / 'index.json').read_text())
        entries = Fixture.tree(f.store.root / 'entries')
        env = (f.tests / 'current-managed.env').read_bytes()
        f.request['suites_sha256'] = sha((f.tests / 'suites.conf').read_bytes())
        f.store.unregister(f.request)
        after = json.loads((f.store.root / 'index.json').read_text())
        self.assertEqual(after['entries'], before['entries'])
        self.assertEqual(after['registrations'], before['registrations'])
        self.assertEqual(after['seq'], before['seq'])
        self.assertEqual(Fixture.tree(f.store.root / 'entries'), entries)
        self.assertEqual((f.tests / 'current-managed.env').read_bytes(), env)
        self.assertTrue((f.tests / 'suites.conf').read_bytes().endswith(b'agent current-managed true\n'))
        f.same_legacy_outside()

    def test_crash_after_journal_removal_is_complete(self):
        f = Fixture()
        finish = f.store._finish_journal
        def crash_finished():
            finish()
            raise Crash('after-journal-removal')
        f.store._finish_journal = crash_finished
        with self.assertRaises(Crash):
            f.store.unregister(f.request)
        f.success()
        f.store.recover()
        f.success()

    def test_unknown_legacy_cutover_cli_normal_and_empty_env(self):
        f = Fixture(unknown=True)
        for empty in (False, True):
            result = f.cli(empty)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn('legacy cutover unknown', result.stderr)
            f.unchanged()

    def test_existing_empty_directory_cannot_fabricate_custody(self):
        home = Path(tempfile.mkdtemp(prefix='unknown-', dir=os.environ['TMPDIR']))
        tests = home / 'tests'
        tests.mkdir()
        (tests / 'suites.conf').write_text('')
        store = core.Store.initialize(home / 'store', tests)
        with self.assertRaisesRegex(core.Refused, 'legacy cutover unknown'):
            with store.prelease_suite('agent', NAMES[0] + '-nodes'):
                self.fail('unknown legacy custody was accepted')

    def test_held_lease_refuses_without_mutation(self):
        f = Fixture()
        with f.store.prelease_suite('agent', NAMES[0] + '-nodes'):
            result = f.cli()
            self.assertEqual(result.returncode, 2)
            f.unchanged()
        f.store.unregister(f.request)
        f.success()

    def test_inherited_child_keeps_prelease_after_parent_context_exits(self):
        f = Fixture()
        with f.store.prelease_suite('agent', NAMES[0] + '-nodes') as fds:
            child = subprocess.Popen([sys.executable, '-c', 'import sys; sys.stdin.buffer.read(1)'],
                                     stdin=subprocess.PIPE, pass_fds=tuple(fds))
        try:
            self.assertEqual(f.cli().returncode, 2)
            f.unchanged()
        finally:
            child.communicate(b'x', timeout=10)
        self.assertEqual(child.returncode, 0)
        f.store.unregister(f.request)
        f.success()

    def test_stale_baseline_and_exact_names(self):
        f = Fixture()
        bad = dict(f.request, suites_sha256='0' * 64)
        with self.assertRaisesRegex(core.Refused, 'stale'):
            f.store.unregister(bad)
        for names in ({}, {**f.request['names'], 'foreign': {}},
                      {**f.request['names'], NAMES[0]: {'env_sha256': '0' * 64}}):
            with self.assertRaisesRegex(core.Refused, 'exact original seven'):
                f.store.unregister(dict(f.request, names=names))
        f.unchanged()

    def test_changed_env_and_ambiguous_suite(self):
        for changed in ('env', 'suite'):
            f = Fixture()
            if changed == 'env':
                (f.tests / (NAMES[0] + '.env')).write_text('CHANGED=yes\n')
            else:
                row = next(r for r in ORIGINAL.decode().splitlines(keepends=True)
                           if r.split(None, 2)[:2] == ['agent', NAMES[0] + '-nodes'])
                (f.tests / 'suites.conf').write_bytes(ORIGINAL + row.encode())
                f.request['suites_sha256'] = sha((f.tests / 'suites.conf').read_bytes())
            before = Fixture.tree(f.tests)
            with self.assertRaises(core.Refused):
                f.store.unregister(f.request)
            self.assertEqual(Fixture.tree(f.tests), before)
            f.same_legacy_outside()

    def test_outside_references_are_refused_kept_not_erased(self):
        for target in ('suite', 'env'):
            f = Fixture()
            if target == 'suite':
                (f.tests / 'suites.conf').write_bytes(ORIGINAL + ('agent foreign source ' + NAMES[0] + '.env\n').encode())
                f.request['suites_sha256'] = sha((f.tests / 'suites.conf').read_bytes())
            else:
                (f.tests / 'reference.env').write_text('source ' + NAMES[0] + '.env\n')
            before = Fixture.tree(f.tests)
            with self.assertRaisesRegex(core.Refused, 'reference protected'):
                f.store.unregister(f.request)
            self.assertEqual(Fixture.tree(f.tests), before)
            f.same_legacy_outside()

    def test_symlink_hardlink_foreign_and_unsafe_directory(self):
        for kind in ('symlink', 'hardlink', 'foreign', 'unsafe-directory'):
            f = Fixture()
            path = f.tests / (NAMES[0] + '.env')
            if kind in ('symlink', 'hardlink'):
                saved = f.home / 'saved.env'
                path.rename(saved)
                if kind == 'symlink':
                    path.symlink_to(saved)
                else:
                    os.link(saved, path)
            elif kind == 'foreign':
                original_fstat = os.fstat
                def foreign_fstat(fd):
                    info = original_fstat(fd)
                    if (info.st_dev, info.st_ino) == (path.stat().st_dev, path.stat().st_ino):
                        values = list(info)
                        values[4] = info.st_uid + 1
                        return os.stat_result(values)
                    return info
                with patch.object(core.os, 'fstat', foreign_fstat):
                    with self.assertRaisesRegex(core.Refused, 'unsafe metadata'):
                        f.store.unregister(f.request)
                f.unchanged()
                continue
            else:
                f.tests.chmod(0o777)
            before = path.read_bytes()
            with self.assertRaises((core.Refused, OSError)):
                f.store.unregister(f.request)
            self.assertEqual(path.read_bytes(), before)
            f.same_legacy_outside()

    def test_races_refuse_and_preserve_changed_file(self):
        for point in ('unregistration:validated', 'unregistration:journal',
                      'unregistration:publish:suites.conf'):
            f = Fixture()
            path = f.tests / (NAMES[0] + '.env')
            def race(where):
                if where == point:
                    path.write_text('RACED=preserve\n')
            f.store._checkpoint = race
            with self.assertRaisesRegex(core.Refused, 'raced'):
                f.store.unregister(f.request)
            self.assertEqual(path.read_text(), 'RACED=preserve\n')
            self.assertEqual((f.tests / 'suites.conf').read_bytes(), ORIGINAL)
            f.same_legacy_outside()
            if f.store.journal.exists():
                f.store._checkpoint = lambda _: None
                with self.assertRaises(core.Refused):
                    f.store.recover()
                self.assertEqual(path.read_text(), 'RACED=preserve\n')

    def test_symlink_race_after_validation_and_recovery(self):
        f = Fixture()
        path = f.tests / (NAMES[0] + '.env')
        saved = f.home / 'saved.env'
        def race(where):
            if where == 'unregistration:journal':
                path.rename(saved)
                path.symlink_to(saved)
        f.store._checkpoint = race
        with self.assertRaises((core.Refused, OSError)):
            f.store.unregister(f.request)
        with self.assertRaises((core.Refused, OSError)):
            f.store.recover()
        self.assertEqual(saved.read_bytes(), ENVS[NAMES[0]])
        self.assertTrue(path.is_symlink())
        f.same_legacy_outside()

    def test_crash_each_publication_then_forward_recover(self):
        for point in POINTS:
            with self.subTest(point=point):
                f = Fixture()
                def crash(where):
                    if where == point:
                        raise Crash(where)
                f.store._checkpoint = crash
                with self.assertRaises(Crash):
                    f.store.unregister(f.request)
                f.same_legacy_outside()
                f.store._checkpoint = lambda _: None
                f.store.recover()
                f.success()
                f.store.recover()
                f.success()

    def test_crash_during_each_recovery_publication(self):
        for point in POINTS[1:]:
            with self.subTest(point=point):
                f = Fixture()
                def crash_journal(where):
                    if where == 'unregistration:journal':
                        raise Crash(where)
                f.store._checkpoint = crash_journal
                with self.assertRaises(Crash):
                    f.store.unregister(f.request)
                def crash_recovery(where):
                    if where == point:
                        raise Crash(where)
                f.store._checkpoint = crash_recovery
                with self.assertRaises(Crash):
                    f.store.recover()
                f.same_legacy_outside()
                f.store._checkpoint = lambda _: None
                f.store.recover()
                f.success()

    def test_pending_recovery_refuses_held_lease(self):
        f = Fixture()
        def crash(where):
            if where == 'unregistration:journal':
                raise Crash(where)
        f.store._checkpoint = crash
        with self.assertRaises(Crash):
            f.store.unregister(f.request)
        index = json.loads((f.store.root / 'index.json').read_text())
        fd = f.store._registration_lock(index)
        try:
            with self.assertRaises(BlockingIOError):
                f.store.recover()
            f.unchanged()
        finally:
            os.close(fd)
        f.store._checkpoint = lambda _: None
        f.store.recover()
        f.success()

    def test_recovery_rejects_journal_scope_and_identity_changes(self):
        for tamper in ('foreign-projection', 'changed-identity', 'payload-victim', 'outside-index'):
            f = Fixture()
            def crash(where):
                if where == 'unregistration:journal':
                    raise Crash(where)
            f.store._checkpoint = crash
            with self.assertRaises(Crash):
                f.store.unregister(f.request)
            journal = json.loads(f.store.journal.read_text())
            if tamper == 'foreign-projection':
                journal['projections']['P1.env'] = ['PROTECTED=P1\n', None]
            elif tamper == 'changed-identity':
                journal['projections'][NAMES[0] + '.env'][0] = 'UNREVIEWED=1\n'
            elif tamper == 'payload-victim':
                journal['victims'] = [str(f.legacy / NAMES[0])]
            else:
                journal['after']['seq'] += 1
            core.atomic(f.store.journal, core.canonical(journal))
            f.store._checkpoint = lambda _: None
            with self.assertRaises(core.Refused):
                f.store.recover()
            f.unchanged()

    def test_race_after_index_leaves_pending_and_preserves_external_bytes(self):
        f = Fixture()
        path = f.tests / (NAMES[0] + '.env')
        def race(where):
            if where == 'index':
                path.write_text('EXTERNAL=preserve\n')
        f.store._checkpoint = race
        with self.assertRaisesRegex(core.Refused, 'raced before completion'):
            f.store.unregister(f.request)
        self.assertTrue(f.store.journal.exists())
        f.store._checkpoint = lambda _: None
        with self.assertRaisesRegex(core.Refused, 'projection changed'):
            f.store.recover()
        self.assertEqual(path.read_text(), 'EXTERNAL=preserve\n')
        f.same_legacy_outside()

    def test_replaced_or_symlink_lease_refuses(self):
        for symlink in (False, True):
            f = Fixture()
            lock = f.store.root / 'locks' / 'registration-cutover'
            saved = f.home / 'old-lock'
            lock.rename(saved)
            if symlink:
                lock.symlink_to(saved)
            else:
                lock.write_bytes(b'')
            with self.assertRaises(core.Refused):
                f.store.unregister(f.request)
            f.unchanged()

    def test_concurrent_real_cli_calls_serialize_one_success_one_refusal(self):
        f = Fixture()
        argv = [sys.executable, '-I', str(CORE), '--root', str(f.store.root),
                '--tests-dir', str(f.tests), 'unregister', '--request', str(f.request_path)]
        calls = [subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for call in calls:
            call.communicate(timeout=10)
        self.assertEqual(sorted(call.returncode for call in calls), [0, 2])
        f.success()

    def test_real_caller_shape_normal_and_env_i(self):
        for empty in (False, True):
            env = {'PATH': '/usr/bin:/bin', 'TMPDIR': os.environ['TMPDIR'],
                   'PYTHONDONTWRITEBYTECODE': '1'} if empty else dict(os.environ)
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--caller-shape'],
                                    env=env, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('PASS real test-run', result.stdout)


if __name__ == '__main__':
    if sys.argv[1:] == ['--caller-shape']:
        caller_shape()
    else:
        unittest.main(verbosity=2)
