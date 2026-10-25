"""Private observer controls; never collects or changes the original P4 test."""
import importlib.util
import json
import os
import selectors
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import types
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).with_name('p4_sample_0233.py')


def observer():
    spec = importlib.util.spec_from_file_location('private_observer', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ObserverControls(unittest.TestCase):
    def test_bootstrap_fake_workload_checkpoints_are_durable(self):
        module = observer()
        ready = threading.Event()
        finished = threading.Event()
        clock = [0.0]
        ticks = iter((9.9, 10.0, 25.0, 40.0))

        class Stop:
            def wait(self, interval):
                if not ready.wait(2):
                    raise AssertionError('fake workload did not start')
                value = next(ticks, None)
                if value is None:
                    finished.set()
                    return True
                clock[0] = value
                return False

            def set(self):
                ready.set()

        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            def fake_main(args, plugins):
                plugins[0].pytest_runtest_logstart('fake-workload', None)
                child = subprocess.Popen([sys.executable, '-c', 'pass'])
                self.assertEqual(child.wait(), 0)
                with selectors.DefaultSelector() as selector:
                    self.assertEqual(selector.select(0), [])
                ready.set()
                self.assertTrue(finished.wait(3), 'sampler failed or stopped before callbacks')
                # Read while the observer still has the files open.
                rows = [json.loads(line) for line in (Path(folder) / 'events.jsonl').read_text().splitlines()]
                self.assertEqual([row['target'] for row in rows if row['kind'] == 'checkpoint'], [10, 25, 40])
                self.assertEqual(len([row for row in rows if row['kind'] == 'sample']), 4)
                self.assertTrue(any(row['kind'] == 'child_exit_observed' for row in rows))
                self.assertTrue(any(row['kind'] == 'poll' and row['timeout'] == 0 for row in rows))
                plugins[0].pytest_runtest_logreport(types.SimpleNamespace(when='call', outcome='passed', duration=40))
                return 0

            with patch.dict(os.environ, P4_SAMPLE_OUTPUT=folder), patch.dict(sys.modules, pytest=types.SimpleNamespace(main=fake_main)), patch.object(module, 'STOP', Stop()), patch.object(module.time, 'monotonic', lambda: clock[0]):
                self.assertEqual(module.main(), 0)
            rows = [json.loads(line) for line in (Path(folder) / 'events.jsonl').read_text().splitlines()]
            self.assertEqual(rows[-1]['sampler_errors'], [])
            self.assertEqual(rows[-1]['samples'], 4)
            self.assertEqual([row['test_elapsed'] for row in rows if row['kind'] == 'checkpoint'], [10, 25, 40])
            dumps = (Path(folder) / 'faulthandler.txt').read_text()
            for target in (10, 25, 40):
                self.assertIn(f'TARGET {target} ACTUAL', dumps)
            for name in ('events.jsonl', 'faulthandler.txt', 'loaded-origins.json'):
                self.assertEqual((Path(folder) / name).stat().st_mode & 0o777, 0o600)
            self.assertEqual(subprocess.Popen.__init__, module.ORIGINAL_INIT)

    def test_scheduler_fault_is_explicit_and_durable(self):
        module = observer()
        with tempfile.TemporaryFile(mode='w+', dir=os.environ.get('TMPDIR')) as stream:
            module.EVENTS = stream
            with patch.object(module, 'collect_samples', side_effect=TypeError('injected')):
                module.sample_loop()
            self.assertEqual(module.ERRORS, ['TypeError'])
            stream.seek(0)
            self.assertEqual(json.loads(stream.readline())['kind'], 'sampler_error')

    def test_sample_timestamp_survives_event_serialization(self):
        module = observer()
        with tempfile.TemporaryFile(mode='w+', dir=os.environ.get('TMPDIR')) as stream:
            module.EVENTS = stream
            module.event('sample', elapsed=10.0, test_elapsed=10.0)
            stream.seek(0)
            self.assertEqual(json.loads(stream.readline())['elapsed'], 10.0)

    def test_bootstrap_returns_nonzero_when_sampler_fails(self):
        module = observer()
        failed = threading.Event()

        def broken_collector():
            failed.set()
            raise TypeError('injected scheduler failure')

        def fake_main(args, plugins):
            self.assertTrue(failed.wait(2))
            return 0

        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            with patch.dict(os.environ, P4_SAMPLE_OUTPUT=folder), patch.dict(sys.modules, pytest=types.SimpleNamespace(main=fake_main)), patch.object(module, 'collect_samples', broken_collector):
                self.assertEqual(module.main(), 3)
            rows = [json.loads(line) for line in (Path(folder) / 'events.jsonl').read_text().splitlines()]
            self.assertEqual(rows[-1]['sampler_errors'], ['TypeError'])


if __name__ == '__main__':
    unittest.main()
