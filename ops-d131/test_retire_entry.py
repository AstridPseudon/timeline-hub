import contextlib
import copy
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import bench_store

NOW = '2026-10-25T22:30:00Z'
REGISTERED = '2026-10-25T20:00:00Z'
CHILD_RESERVE = 5905580032


class RetirementTests(unittest.TestCase):
    def make_store(self):
        temp = tempfile.TemporaryDirectory(prefix='ops-d139-', dir=os.environ.get('TMPDIR'))
        folder = Path(temp.name)
        tests = folder / 'tests'
        tests.mkdir(mode=0o700)
        (tests / 'suites.conf').write_text('', encoding='utf-8')
        store = bench_store.Store.initialize(folder / 'store', tests)
        self.addCleanup(temp.cleanup)
        return store

    def make_entry(self, registration=True):
        store = self.make_store()
        identity = {'agent_sha': 'a' * 40, 'backend_sha': 'b' * 40,
                    'client_tuple': {'sha256': 'c' * 64}}

        def build(stage, final):
            (Path(stage) / 'payload').write_text('fixture', encoding='utf-8')

        value = {'name': 'retire-fixture', 'env': '', 'suite': '', 'requires': []}
        with mock.patch.object(bench_store.shutil, 'disk_usage', return_value=mock.Mock(free=CHILD_RESERVE)):
            store._fixture_clock = lambda: bench_store.timestamp(REGISTERED, 'fixture')
            entry = store.ensure('child', identity, value, build, lambda path: None)
        store._fixture_clock = lambda: bench_store.timestamp(NOW, 'fixture')
        eid = 'child-' + entry['key']
        return store, eid, entry

    @staticmethod
    def authorization(store, eid, entry):
        return {
            'owner': store.owner['id'], 'entry': eid, 'component': entry['component'],
            'key': entry['key'], 'identity': copy.deepcopy(entry['identity']),
            'path': entry['path'], 'node': entry['node'], 'lock': entry['lock'],
        }

    def test_eligible_entry_uses_single_retirement_journal_and_preserves_registration_receipt(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)

        receipt = store.retire_entry(eid, authorization)

        self.assertEqual(receipt['status'], 'retired')
        self.assertEqual(receipt['entry'], eid)
        self.assertEqual(receipt['registrations'], ['retire-fixture'])
        index = json.loads((store.root / 'index.json').read_text(encoding='utf-8'))
        self.assertNotIn(eid, index['entries'])
        self.assertEqual(index['registrations'], {})
        self.assertIn('retire-fixture', index['retired'])
        self.assertEqual(index['retired_entries'][0]['entry'], eid)
        self.assertEqual(index['retired_entries'][0]['registrations'], ['retire-fixture'])
        self.assertFalse(Path(entry['path']).exists())
        self.assertFalse(store.journal.exists())

    def test_interrupted_retirement_recovers_forward_consistently(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        original = store._checkpoint

        def interrupt(point):
            if point == 'retirement:journal':
                raise bench_store.Refused('fixture interruption')
            original(point)

        store._checkpoint = interrupt
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, authorization)
        self.assertTrue(store.journal.exists())
        self.assertIn(eid, json.loads((store.root / 'index.json').read_text(encoding='utf-8'))['entries'])
        store._checkpoint = original
        store.recover()
        self.assertFalse(store.journal.exists())
        self.assertNotIn(eid, json.loads((store.root / 'index.json').read_text(encoding='utf-8'))['entries'])
        self.assertFalse(Path(entry['path']).exists())

    def test_cli_wrapper_rejects_production_clock_override(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        auth_path = Path(store.root).parent / 'authorization.json'
        auth_path.write_text(json.dumps(authorization), encoding='utf-8')
        result = subprocess.run([
            sys.executable, str(Path(__file__).with_name('retire_entry.py')),
            '--root', str(store.root), '--tests-dir', str(store.tests), '--entry', eid,
            '--authorization', str(auth_path), '--now', NOW,
        ], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn('unrecognized arguments: --now', result.stderr)

    def assert_refused_unchanged(self, authorization):
        store, eid, entry = self.make_entry()
        authorization = copy.deepcopy(authorization(store, eid, entry)) if callable(authorization) else copy.deepcopy(authorization)
        before_index = (store.root / 'index.json').read_bytes()
        before_path = Path(entry['path'])
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, authorization)
        self.assertEqual((store.root / 'index.json').read_bytes(), before_index)
        self.assertTrue(before_path.exists())
        self.assertFalse(store.journal.exists())

    def test_caller_audit_fields_and_keep_marker_refuse_unchanged(self):
        for field, value in (
                ('worker_refs', ['worker-1']), ('queue_refs', ['queue-1']),
                ('processes', ['pid']), ('registration_refs', ['external']),
                ('keep', True), ('registered_at', '2099-01-01T00:00:00Z')):
            def mutate(store, eid, entry, field=field, value=value):
                auth = self.authorization(store, eid, entry)
                auth[field] = value
                return auth
            self.assert_refused_unchanged(mutate)

        store, eid, entry = self.make_entry()
        Path(entry['path'], 'KEEP').write_text('', encoding='utf-8')
        before = (store.root / 'index.json').read_bytes()
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, self.authorization(store, eid, entry))
        self.assertEqual((store.root / 'index.json').read_bytes(), before)

    def test_age_uses_persisted_state_and_rejects_clock_override(self):
        store, eid, entry = self.make_entry()
        store._fixture_clock = lambda: bench_store.timestamp('2026-10-25T20:30:00Z', 'fixture')
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, self.authorization(store, eid, entry))
        with self.assertRaises(TypeError):
            store.retire_entry(eid, self.authorization(store, eid, entry), now=NOW)

    def test_lease_process_identity_and_unknown_guards_refuse_unchanged(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        with store.acquire(['retire-fixture']):
            before = (store.root / 'index.json').read_bytes()
            with self.assertRaises(bench_store.Refused):
                store.retire_entry(eid, authorization)
            self.assertEqual((store.root / 'index.json').read_bytes(), before)

        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(5)'], cwd=entry['path'])
        try:
            time.sleep(0.1)
            with self.assertRaises(bench_store.Refused):
                store.retire_entry(eid, authorization)
        finally:
            process.terminate()
            process.wait(timeout=5)

        def identity(store, eid, entry):
            auth = self.authorization(store, eid, entry)
            auth['identity']['agent_sha'] = 'd' * 40
            return auth
        self.assert_refused_unchanged(identity)
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        with self.assertRaises(bench_store.Refused):
            store.retire_entry('child-' + 'f' * 64, authorization)
        self.assertIn(eid, json.loads((store.root / 'index.json').read_text(encoding='utf-8'))['entries'])

    def test_process_entering_after_initial_audit_refuses_unchanged(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        original = store._process_references
        process = None
        calls = 0

        def race(path, node=None):
            nonlocal calls, process
            result = original(path, node)
            calls += 1
            if calls == 1:
                process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(5)'],
                                           cwd=entry['path'])
            return result

        before = (store.root / 'index.json').read_bytes()
        store._process_references = race
        try:
            with self.assertRaises(bench_store.Refused):
                store.retire_entry(eid, authorization)
        finally:
            if process is not None:
                process.terminate()
                process.wait(timeout=5)
        self.assertEqual((store.root / 'index.json').read_bytes(), before)
        self.assertTrue(Path(entry['path']).exists())
        self.assertFalse(store.journal.exists())

    def test_corrupt_receipt_and_activity_refuse(self):
        store, eid, entry = self.make_entry()
        store.retire_entry(eid, self.authorization(store, eid, entry))
        index_path = store.root / 'index.json'
        index = json.loads(index_path.read_text(encoding='utf-8'))
        index['retired_entries'][0]['path'] = 7
        index_path.write_text(json.dumps(index), encoding='utf-8')
        with self.assertRaises(bench_store.Refused):
            store.registered('retire-fixture')

        store, eid, entry = self.make_entry()
        activity_path = store.root / 'activity.json'
        activity = json.loads(activity_path.read_text(encoding='utf-8'))
        activity['workers'] = [eid]
        activity_path.write_text(json.dumps(activity), encoding='utf-8')
        before = (store.root / 'index.json').read_bytes()
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, self.authorization(store, eid, entry))
        self.assertEqual((store.root / 'index.json').read_bytes(), before)

    def test_receipt_cross_associations_refuse_after_journal_is_finished(self):
        store, eid, entry = self.make_entry()
        identity = dict(entry['identity'], agent_sha='d' * 40)
        value = {'name': 'other-fixture', 'env': '',
                 'suite': 'agent other-fixture true\n', 'requires': []}
        with mock.patch.object(bench_store.shutil, 'disk_usage', return_value=mock.Mock(free=CHILD_RESERVE)):
            store._fixture_clock = lambda: bench_store.timestamp(REGISTERED, 'fixture')
            other = store.ensure('child', identity, value,
                                 lambda stage, final: None, lambda path: None)
        store._fixture_clock = lambda: bench_store.timestamp(NOW, 'fixture')
        store.retire_entry(eid, self.authorization(store, eid, entry))
        other_id = 'child-' + other['key']
        store.retire_entry(other_id, self.authorization(store, other_id, other))
        index_path = store.root / 'index.json'
        valid = index_path.read_bytes()
        original = json.loads(valid)
        store._load()
        for field, value in (
                ('node', other['node']), ('path', other['path']), ('seq', other['seq']),
                ('lock', other['lock']), ('owner', 'f' * 32),
                ('registrations', ['other-fixture']), ('suites', [['agent', 'other-fixture']])):
            with self.subTest(field=field):
                index = copy.deepcopy(original)
                index['retired_entries'][0][field] = value
                index_path.write_text(json.dumps(index), encoding='utf-8')
                with self.assertRaises(bench_store.Refused):
                    store._load()
                index_path.write_bytes(valid)
        index = copy.deepcopy(original)
        index['retired_entries'][0].pop('source', None)
        index_path.write_text(json.dumps(index), encoding='utf-8')
        with self.assertRaises(bench_store.Refused):
            store._load()

    def test_recovery_binds_receipt_source_to_exact_before_index(self):
        store, eid, entry = self.make_entry()

        def interrupt(point):
            if point == 'retirement:journal':
                raise bench_store.Refused('fixture interruption')

        store._checkpoint = interrupt
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, self.authorization(store, eid, entry))
        journal = json.loads(store.journal.read_bytes())
        receipt = journal['after']['retired_entries'][-1]
        receipt['node'] = [entry['node'][0], entry['node'][1] + 1]
        receipt['source']['entries'][eid]['node'] = receipt['node']
        store.journal.write_text(json.dumps(journal), encoding='utf-8')
        before = (store.root / 'index.json').read_bytes()
        with self.assertRaisesRegex(bench_store.Refused, 'retirement receipt authority'):
            store.recover()
        self.assertEqual((store.root / 'index.json').read_bytes(), before)
        self.assertTrue(Path(journal['quarantine']).exists())
        self.assertTrue(store.journal.exists())

    def test_retirement_deletes_nested_private_payload(self):
        store, eid, entry = self.make_entry()
        nested = Path(entry['path']) / 'nested' / 'deeper'
        nested.mkdir(parents=True)
        (nested / 'payload').write_text('fixture', encoding='utf-8')
        receipt = store.retire_entry(eid, self.authorization(store, eid, entry))
        self.assertEqual(receipt['status'], 'retired')
        self.assertFalse(Path(entry['path']).exists())
        self.assertFalse(store.journal.exists())

    def test_manager_wrapper_uses_guarded_retirement(self):
        from retire_entry import main

        store, eid, entry = self.make_entry()
        auth_path = store.root.parent / 'authorization.json'
        auth_path.write_text(json.dumps(self.authorization(store, eid, entry)), encoding='utf-8')
        argv = ['retire_entry.py', '--root', str(store.root), '--tests-dir', str(store.tests),
                '--entry', eid, '--authorization', str(auth_path)]
        before = (store.root / 'index.json').read_bytes()
        with mock.patch.object(sys, 'argv', argv), mock.patch.object(bench_store, 'Store', return_value=store):
            with store.acquire(['retire-fixture']), contextlib.redirect_stderr(io.StringIO()) as error:
                self.assertEqual(main(), 2)
                self.assertIn('entry lease held', error.getvalue())
            self.assertEqual((store.root / 'index.json').read_bytes(), before)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(main(), 0)
                self.assertEqual(json.loads(output.getvalue())['status'], 'retired')
        self.assertFalse(Path(entry['path']).exists())

    def test_symlink_and_hardlink_payloads_refuse_unchanged(self):
        store, eid, entry = self.make_entry()
        payload = Path(entry['path']) / 'payload'
        payload.unlink()
        payload.symlink_to('/etc/hosts')
        authorization = self.authorization(store, eid, entry)
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, authorization)
        self.assertTrue(Path(entry['path']).exists())

        store, eid, entry = self.make_entry()
        payload = Path(entry['path']) / 'payload'
        external = Path(store.root).parent / 'outside'
        external.write_text('outside', encoding='utf-8')
        payload.unlink()
        os.link(external, payload)
        authorization = self.authorization(store, eid, entry)
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, authorization)
        self.assertTrue(Path(entry['path']).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
