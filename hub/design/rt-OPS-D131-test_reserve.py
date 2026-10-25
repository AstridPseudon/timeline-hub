import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import bench_store


CHILD_RESERVE = 5905580032
RUNTIME_RESERVE = 8 * 1024 * 1024 * 1024
DECIMAL_6_1_GB = 6_100_000_000


class ReserveTests(unittest.TestCase):
    def make_store(self):
        parent = os.environ.get('TMPDIR')
        temp = tempfile.TemporaryDirectory(prefix='ops-d131-', dir=parent)
        folder = Path(temp.name)
        tests = folder / 'tests'
        tests.mkdir(mode=0o700)
        (tests / 'suites.conf').write_text('', encoding='utf-8')
        store = bench_store.Store.initialize(folder / 'store', tests)
        self.addCleanup(temp.cleanup)
        return store

    @staticmethod
    def identity(component, number):
        if component == 'child':
            return {'agent_sha': f'{number:040x}', 'backend_sha': 'b' * 40,
                    'client_tuple': {'sha256': 'c' * 64}}
        return {'remotion_tree': f'{number:040x}'}

    def attempt(self, component, free, number=1):
        store = self.make_store()
        calls = {'build': 0, 'verify': 0, 'registration': 0}

        def build(stage, final):
            calls['build'] += 1
            (Path(stage) / 'payload').write_text('tiny', encoding='utf-8')

        def verify(path):
            calls['verify'] += 1
            self.assertEqual((path / 'payload').read_text(encoding='utf-8'), 'tiny')

        def registration(path, final, reused):
            calls['registration'] += 1
            return {'name': f'{component}-{number}', 'env': '', 'suite': '', 'requires': []}

        usage = mock.Mock(free=free)
        with mock.patch.object(bench_store.shutil, 'disk_usage', return_value=usage):
            try:
                entry = store.ensure(component, self.identity(component, number),
                                     registration, build, verify)
            except bench_store.Refused:
                entry = None
        return store, calls, entry

    def test_child_below_equal_and_above_threshold(self):
        for free, admitted in ((CHILD_RESERVE - 1, False),
                               (CHILD_RESERVE, True),
                               (CHILD_RESERVE + 1, True)):
            store, calls, entry = self.attempt('child', free, free)
            self.assertEqual(entry is not None, admitted)
            if admitted:
                self.assertFalse(entry['reused'])
                self.assertEqual(calls, {'build': 1, 'verify': 1, 'registration': 1})
            else:
                self.assertEqual(calls, {'build': 0, 'verify': 0, 'registration': 0})
                index = json.loads((store.root / 'index.json').read_text(encoding='utf-8'))
                self.assertEqual(index['entries'], {})
                self.assertEqual(index['registrations'], {})

    def test_runtime_below_and_equal_threshold(self):
        for free, admitted in ((RUNTIME_RESERVE - 1, False), (RUNTIME_RESERVE, True)):
            store, calls, entry = self.attempt('runtime', free, free)
            self.assertEqual(entry is not None, admitted)
            if admitted:
                self.assertFalse(entry['reused'])
                self.assertEqual(calls, {'build': 1, 'verify': 1, 'registration': 1})
            else:
                self.assertEqual(calls, {'build': 0, 'verify': 0, 'registration': 0})

    def test_6_1_decimal_gb_admits_child_and_refuses_runtime(self):
        child_store, child_calls, child_entry = self.attempt('child', DECIMAL_6_1_GB, 61)
        self.assertIsNotNone(child_entry)
        self.assertEqual(child_calls, {'build': 1, 'verify': 1, 'registration': 1})

        runtime_store, runtime_calls, runtime_entry = self.attempt('runtime', DECIMAL_6_1_GB, 61)
        self.assertIsNone(runtime_entry)
        self.assertEqual(runtime_calls, {'build': 0, 'verify': 0, 'registration': 0})
        index = json.loads((runtime_store.root / 'index.json').read_text(encoding='utf-8'))
        self.assertEqual(index['entries'], {})
        self.assertEqual(index['registrations'], {})

    def test_reuse_behavior_remains_intact(self):
        store = self.make_store()
        calls = {'build': 0, 'verify': 0, 'registration': 0}

        def build(stage, final):
            calls['build'] += 1
            (Path(stage) / 'payload').write_text('tiny', encoding='utf-8')

        def verify(path):
            calls['verify'] += 1

        def registration(path, final, reused):
            calls['registration'] += 1
            return {'name': 'reuse-child', 'env': '', 'suite': '', 'requires': []}

        identity = self.identity('child', 9001)
        with mock.patch.object(bench_store.shutil, 'disk_usage', return_value=mock.Mock(free=CHILD_RESERVE)):
            first = store.ensure('child', identity, registration, build, verify)
            second = store.ensure('child', identity, registration, build, verify)
        self.assertFalse(first['reused'])
        self.assertTrue(second['reused'])
        self.assertEqual(calls, {'build': 1, 'verify': 2, 'registration': 2})

    def test_unknown_component_remains_fail_closed(self):
        store = self.make_store()
        calls = {'build': 0, 'registration': 0}

        def build(stage, final):
            calls['build'] += 1

        def registration(path, final, reused):
            calls['registration'] += 1
            return {'name': 'unknown', 'env': '', 'suite': '', 'requires': []}

        with self.assertRaises(bench_store.Refused):
            store.ensure('unknown', {}, registration, build, lambda path: None)
        self.assertEqual(calls, {'build': 0, 'registration': 0})


if __name__ == '__main__':
    unittest.main(verbosity=2)
