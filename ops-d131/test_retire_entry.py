import copy
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
NOT_BEFORE = '2026-10-25T21:00:00Z'
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
            entry = store.ensure('child', identity, value, build, lambda path: None)
        eid = 'child-' + entry['key']
        return store, eid, entry

    @staticmethod
    def authorization(store, eid, entry):
        return {
            'owner': store.owner['id'], 'entry': eid, 'component': entry['component'],
            'key': entry['key'], 'identity': copy.deepcopy(entry['identity']),
            'path': entry['path'], 'node': entry['node'], 'lock': entry['lock'],
            'registered_at': REGISTERED, 'not_before': NOT_BEFORE,
            'keep': False, 'active': False, 'processes': [], 'cwd_refs': [],
            'fd_refs': [], 'cmdline_refs': [], 'registration_refs': [],
            'suite_refs': [], 'worker_refs': [], 'queue_refs': [],
        }

    def test_eligible_entry_uses_single_retirement_journal_and_preserves_registration_receipt(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)

        receipt = store.retire_entry(eid, authorization, now=NOW)

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
            store.retire_entry(eid, authorization, now=NOW)
        self.assertTrue(store.journal.exists())
        self.assertIn(eid, json.loads((store.root / 'index.json').read_text(encoding='utf-8'))['entries'])
        store._checkpoint = original
        store.recover()
        self.assertFalse(store.journal.exists())
        self.assertNotIn(eid, json.loads((store.root / 'index.json').read_text(encoding='utf-8'))['entries'])
        self.assertFalse(Path(entry['path']).exists())

    def test_cli_wrapper_returns_receipt(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        auth_path = Path(store.root).parent / 'authorization.json'
        auth_path.write_text(json.dumps(authorization), encoding='utf-8')
        result = subprocess.run([
            sys.executable, str(Path(__file__).with_name('retire_entry.py')),
            '--root', str(store.root), '--tests-dir', str(store.tests), '--entry', eid,
            '--authorization', str(auth_path), '--now', NOW,
        ], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['entry'], eid)

    def assert_refused_unchanged(self, authorization, *, now=NOW):
        store, eid, entry = self.make_entry()
        authorization = copy.deepcopy(authorization(store, eid, entry)) if callable(authorization) else copy.deepcopy(authorization)
        before_index = (store.root / 'index.json').read_bytes()
        before_path = Path(entry['path'])
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, authorization, now=now)
        self.assertEqual((store.root / 'index.json').read_bytes(), before_index)
        self.assertTrue(before_path.exists())
        self.assertFalse(store.journal.exists())

    def test_reference_keep_and_timestamp_guards_refuse_unchanged(self):
        for field, value in (
                ('worker_refs', ['worker-1']), ('queue_refs', ['queue-1']),
                ('processes', ['pid']), ('cwd_refs', ['pid:cwd']),
                ('fd_refs', ['pid:fd']), ('cmdline_refs', ['pid:cmdline']),
                ('registration_refs', ['external']), ('suite_refs', ['suite'])):
            def mutate(store, eid, entry, field=field, value=value):
                auth = self.authorization(store, eid, entry)
                auth[field] = value
                return auth
            self.assert_refused_unchanged(mutate)
        def keep(store, eid, entry):
            auth = self.authorization(store, eid, entry)
            auth['keep'] = True
            return auth
        self.assert_refused_unchanged(keep)
        def too_young(store, eid, entry):
            auth = self.authorization(store, eid, entry)
            auth['not_before'] = '2026-10-25T22:31:00Z'
            return auth
        self.assert_refused_unchanged(too_young)
        def no_minimum(store, eid, entry):
            auth = self.authorization(store, eid, entry)
            auth['not_before'] = '2026-10-25T20:30:00Z'
            return auth
        self.assert_refused_unchanged(no_minimum)

    def test_lease_process_identity_and_unknown_guards_refuse_unchanged(self):
        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        with store.acquire(['retire-fixture']):
            before = (store.root / 'index.json').read_bytes()
            with self.assertRaises(bench_store.Refused):
                store.retire_entry(eid, authorization, now=NOW)
            self.assertEqual((store.root / 'index.json').read_bytes(), before)

        store, eid, entry = self.make_entry()
        authorization = self.authorization(store, eid, entry)
        process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(5)'], cwd=entry['path'])
        try:
            time.sleep(0.1)
            with self.assertRaises(bench_store.Refused):
                store.retire_entry(eid, authorization, now=NOW)
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
            store.retire_entry('child-' + 'f' * 64, authorization, now=NOW)
        self.assertIn(eid, json.loads((store.root / 'index.json').read_text(encoding='utf-8'))['entries'])

    def test_symlink_and_hardlink_payloads_refuse_unchanged(self):
        store, eid, entry = self.make_entry()
        payload = Path(entry['path']) / 'payload'
        payload.unlink()
        payload.symlink_to('/etc/hosts')
        authorization = self.authorization(store, eid, entry)
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, authorization, now=NOW)
        self.assertTrue(Path(entry['path']).exists())

        store, eid, entry = self.make_entry()
        payload = Path(entry['path']) / 'payload'
        external = Path(store.root).parent / 'outside'
        external.write_text('outside', encoding='utf-8')
        payload.unlink()
        os.link(external, payload)
        authorization = self.authorization(store, eid, entry)
        with self.assertRaises(bench_store.Refused):
            store.retire_entry(eid, authorization, now=NOW)
        self.assertTrue(Path(entry['path']).exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
