"""Finite subprocess controls. Free-space values are simulated; no disk filling."""

import ast
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

import d77_phase_guard as guard


STUB = r'''
import os, signal, subprocess, sys, time
from pathlib import Path
root, mode = Path(sys.argv[1]), sys.argv[2]
def cancelled(sig, frame):
    (root / ('signal-' + str(os.getpid()))).write_text(str(sig))
    raise SystemExit(0)
signal.signal(signal.SIGINT, cancelled)
signal.signal(signal.SIGTERM, cancelled)
if mode == 'family':
    child = subprocess.Popen([sys.executable, __file__, str(root), 'child'])
    (root / 'child-pid').write_text(str(child.pid))
    def parent_cancelled(sig, frame):
        (root / ('signal-' + str(os.getpid()))).write_text(str(sig))
        child.wait(timeout=1)
        raise SystemExit(0)
    signal.signal(signal.SIGINT, parent_cancelled)
    signal.signal(signal.SIGTERM, parent_cancelled)
if mode == 'orphan':
    child = subprocess.Popen([sys.executable, __file__, str(root), 'child'])
    (root / 'child-pid').write_text(str(child.pid))
    while not (root / 'child-ready').exists():
        time.sleep(.005)
if mode == 'child':
    (root / 'child-ready').write_text('ready')
else:
    (root / 'ready').write_text(str(time.monotonic()))
if mode in ('quick', 'orphan'):
    raise SystemExit(0)
if mode == 'fail':
    raise SystemExit(7)
if mode == 'stubborn':
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
for _ in range(120):
    time.sleep(.01)
'''


class GuardControls(unittest.TestCase):
    observations = {}

    def setUp(self):
        # Harness cleans this scratch directory; keep every control artifact.
        self.root = Path(tempfile.mkdtemp(prefix='guard-control-', dir=os.environ['TMPDIR']))
        self.stub = self.root / 'stub.py'
        self.stub.write_text(STUB)
        self.bounds = guard.Bounds(400_000_000, 0, True)

    def step(self, mode='quick', label='download', bounds=True):
        return guard.Step(label, (sys.executable, str(self.stub), str(self.root), mode),
                          str(self.root), self.bounds if bounds else None)

    def run_guard(self, steps, **kwargs):
        return guard.Monitor(self.root, free=lambda: 5_400_000_000,
                             **kwargs).run(steps)

    def assert_stopped(self, result, commands):
        self.assertFalse(result['phase_complete'])
        self.assertNotEqual(result['status'], 'complete')
        self.assertEqual(len(result['commands']), commands)

    def test_fast_download_growth_cancels_above_floor_despite_exit_zero(self):
        def free():
            ready = self.root / 'ready'
            if not ready.exists():
                return 5_400_000_000
            elapsed = time.monotonic() - float(ready.read_text())
            return int(4_900_000_000 - elapsed * 400_000_000)
        result = guard.Monitor(self.root, free=free).run(
            [self.step('grow'), self.step(label='must-not-start')])
        self.observations['fast_download'] = result
        self.assert_stopped(result, 1)
        row = result['commands'][0]
        self.assertTrue(row['cancelled'])
        self.assertEqual(row['exit'], 0)
        self.assertTrue(row['cleanup_complete'])
        self.assertEqual(row['cancel_signals'], ['SIGINT'])
        self.assertGreater(min(s['free_bytes'] for s in result['samples']),
                           guard.PHASE_FLOOR_BYTES)

    def test_exact_1237_native_start_is_rejected_before_jump(self):
        calls = 0
        def free():
            nonlocal calls
            calls += 1
            return 5_400_000_000 if calls < 3 else 4_710_780_928
        result = guard.Monitor(self.root, free=free).run(
            [self.step(), self.step(label='native-fetch')])
        self.assert_stopped(result, 1)
        self.assertEqual(result['reason'], 'phase-reserve')

    def test_preexisting_low_space_never_spawns(self):
        for value in (5_200_000_000, 4_499_999_999, 3_999_999_999):
            with self.subTest(free=value), patch.object(guard.subprocess, 'Popen') as popen:
                result = guard.Monitor(self.root, free=lambda: value).run([self.step()])
                self.assert_stopped(result, 0)
                popen.assert_not_called()

    def test_slow_du_is_outside_poll_and_admission_is_rechecked(self):
        free_value = 5_400_000_000
        def allocation():
            nonlocal free_value
            time.sleep(.15)
            free_value = 5_199_999_999
            return 100
        with patch.object(guard.subprocess, 'Popen') as popen:
            result = guard.Monitor(self.root, free=lambda: free_value,
                                   allocation=allocation).run([self.step()])
            self.assert_stopped(result, 0)
            popen.assert_not_called()

    def test_slow_du_does_not_delay_active_growth_sampling(self):
        calls = []
        def allocation():
            calls.append(time.monotonic())
            time.sleep(.2)
            return 100
        def free():
            ready = self.root / 'ready'
            return (5_400_000_000 if not ready.exists() else
                    int(4_900_000_000 - (time.monotonic()-float(ready.read_text())) * 400_000_000))
        result = guard.Monitor(self.root, free=free, allocation=allocation).run([self.step('grow')])
        self.observations['slow_du'] = result
        self.assert_stopped(result, 1)
        self.assertEqual(len(calls), 1)
        polls = [s['monotonic'] for s in result['samples'] if s['label'].endswith(':poll')]
        self.assertGreater(len(polls), 3)
        self.assertLess(max(b-a for a, b in zip(polls, polls[1:])), .15)

    def test_exit_before_first_poll_still_checks_free_and_stops(self):
        real_popen = subprocess.Popen
        def exited(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            process.wait(timeout=2)
            return process
        def free():
            return 4_400_000_000 if (self.root / 'ready').exists() else 5_400_000_000
        with patch.object(guard.subprocess, 'Popen', side_effect=exited):
            result = guard.Monitor(self.root, free=free).run([self.step(), self.step(label='later')])
        self.assert_stopped(result, 1)
        self.assertEqual(result['commands'][0]['exit'], 0)
        self.assertTrue(result['cancelled'])

    def test_owned_child_cleanup_and_caller_cancel_propagation(self):
        event = threading.Event()
        def free():
            if (self.root / 'child-ready').exists() and (self.root / 'ready').exists():
                event.set()
            return 5_400_000_000
        result = guard.Monitor(self.root, free=free, cancel=event).run(
            [self.step('family'), self.step(label='later')])
        self.observations['owned_child_cancel'] = result
        self.assert_stopped(result, 1)
        self.assertEqual(result['reason'], 'caller-cancelled')
        self.assertTrue(result['commands'][0]['cleanup_complete'])
        child = int((self.root / 'child-pid').read_text())
        self.assertTrue((self.root / ('signal-' + str(child))).exists())
        self.assertEqual(len(list(self.root.glob('signal-*'))), 2)

    def test_leader_exit_does_not_hide_live_child(self):
        result = self.run_guard([self.step('orphan'), self.step(label='later')])
        self.assert_stopped(result, 1)
        self.assertEqual(result['reason'], 'descendants-after-command-exit')
        self.assertTrue(result['commands'][0]['cleanup_complete'])
        child = int((self.root / 'child-pid').read_text())
        self.assertTrue((self.root / ('signal-' + str(child))).exists())

    def test_uncooperative_normal_cancel_reports_unsupported_without_force(self):
        monitor = guard.Monitor(self.root, free=lambda: 5_400_000_000, timeout=.15)
        result = monitor.run([self.step('stubborn'), self.step(label='later')])
        self.assert_stopped(result, 1)
        self.assertEqual(result['status'], 'unsupported-normal-cancellation-seam')
        self.assertFalse(result['commands'][0]['cleanup_complete'])
        self.assertEqual(result['commands'][0]['cancel_signals'], ['SIGINT', 'SIGTERM'])
        # This finite stub exits naturally, without any additional signal.
        self.assertEqual(len(monitor.unfinished), 1)
        monitor.unfinished[0].wait(timeout=2)
        pid_files = list(self.root.glob('signal-*'))
        self.assertEqual(pid_files, [])

    def test_sigterm_to_wrapper_uses_normal_owned_group_cancellation(self):
        driver = self.root / 'driver.py'
        driver.write_text(
            'import json, sys\n'
            f'sys.path.insert(0, {str(Path(guard.__file__).parent)!r})\n'
            'from d77_phase_guard import Monitor, Step, Bounds\n'
            f'step = Step("download", {(sys.executable, str(self.stub), str(self.root), "grow")!r}, '
            f'{str(self.root)!r}, Bounds(400000000, 0, True))\n'
            f'result = Monitor({str(self.root)!r}, free=lambda: 5400000000).run([step, step])\n'
            'print(json.dumps(result))\n')
        process = subprocess.Popen([sys.executable, str(driver)], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
        deadline = time.monotonic() + 2
        while not (self.root / 'ready').exists() and process.poll() is None:
            if time.monotonic() >= deadline:
                self.fail('finite driver did not become ready')
            time.sleep(.01)
        process.terminate()
        stdout, stderr = process.communicate(timeout=3)
        self.assertEqual(process.returncode, 0, stderr)
        result = json.loads(stdout)
        self.assert_stopped(result, 1)
        self.assertEqual(result['reason'], 'caller-cancelled')
        self.assertTrue(result['commands'][0]['cleanup_complete'])

    def test_post_setup_admission_cannot_use_lower_phase_threshold(self):
        calls = 0
        def free():
            nonlocal calls
            calls += 1
            return 5_400_000_000 if calls < 5 else 5_199_999_999
        step = self.step(label='post-setup-install')
        admitted = guard.Step(step.label, step.argv, step.cwd, step.bounds, admission=True)
        result = guard.Monitor(self.root, free=free).run([self.step(), admitted])
        self.assert_stopped(result, 1)
        self.assertEqual(result['reason'], 'admission')

    def test_command_failure_blocks_later_commands(self):
        result = self.run_guard([self.step('fail'), self.step(label='later')])
        self.assert_stopped(result, 1)
        self.assertEqual(result['commands'][0]['exit'], 7)

    def test_all_steps_complete_and_single_use(self):
        monitor = guard.Monitor(self.root, free=lambda: 5_400_000_000)
        result = monitor.run([self.step(label=label) for label in guard.OMP_LABELS])
        self.assertTrue(result['phase_complete'])
        self.assertFalse(result['cancelled'])
        self.assertEqual(result['status'], 'complete')
        self.assertEqual([r['label'] for r in result['commands']], list(guard.OMP_LABELS))
        with self.assertRaises(RuntimeError):
            monitor.run([self.step()])

    def test_missing_unsafe_bounds_refuse_entire_path_before_launch(self):
        for bounds in (None, guard.Bounds(0, 0, True), guard.Bounds(1, -1, True),
                       guard.Bounds(1, 0, False)):
            with self.subTest(bounds=bounds), patch.object(guard.subprocess, 'Popen') as popen:
                steps = [self.step(), guard.Step('unsafe-fetch', ('unused',), str(self.root), bounds)]
                result = self.run_guard(steps)
                self.assert_stopped(result, 0)
                self.assertEqual(result['status'], 'unsupported-normal-cancellation-seam')
                popen.assert_not_called()

    def test_free_stat_failure_refuses_launch(self):
        def broken():
            raise OSError('stub stat failure')
        result = guard.Monitor(self.root, free=broken).run([self.step()])
        self.assert_stopped(result, 0)
        self.assertIn('free-space-unavailable', result['reason'])

    def test_original_pins_commands_and_source_are_preserved(self):
        path = Path(guard.__file__).parent
        source = (path / 'retained-1237-wrapper.txt').read_bytes()
        info = json.loads((path / 'retained-1237-source.json').read_text())
        self.assertEqual(hashlib.sha256(source).hexdigest(), info['wrapper_sha256'])
        constants = {}
        for node in ast.parse(source).body:
            if isinstance(node, ast.Assign):
                try:
                    value = ast.literal_eval(node.value)
                except ValueError:
                    continue
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        constants[target.id] = value
        for key in ('ARCHIVE_SHA', 'SOURCE_SHA', 'LOCK_SHA', 'BUN_SHA', 'NATIVE_SHA',
                    'BUN_URL', 'NATIVE_URL'):
            self.assertEqual(getattr(guard, key), constants[key])
        empty = self.root / 'empty'
        empty.mkdir()
        steps = guard.omp_steps(empty, self.root / 'never-fetched.tar',
                                {label: self.bounds for label in guard.OMP_LABELS})
        self.assertEqual([s.label for s in steps], list(guard.OMP_LABELS))
        by_label = {s.label: s for s in steps}
        self.assertEqual(by_label['bun-install'].argv[1:],
                         ('install', '--frozen-lockfile', '--ignore-scripts', '--omit', 'optional'))
        self.assertTrue(by_label['bun-install'].admission)
        self.assertEqual(by_label['gen-tool-views'].argv[1:], ('run', 'gen:tool-views'))
        self.assertEqual(by_label['bun-link'].argv[1:],
                         ('link', '--frozen-lockfile', '--ignore-scripts', '--no-save'))
        self.assertIn(guard.ABI_PROBE.encode(), source)
        self.assertEqual(list(empty.iterdir()), [])

    def omp_fixture(self, grow):
        """Tiny fake fetch/extract implementation; never import real installer tools."""
        tools = self.root / 'modules/astrid/installer'
        tools.mkdir(parents=True)
        (tools / 'tools.py').write_text(
            'from pathlib import Path\nimport time\n'
            f'ROOT = Path({str(self.root)!r})\n'
            'def source_tree_sha256(source): return "stub-source"\n'
            'def extract(archive, destination, *, reject_links=False):\n'
            '    assert reject_links\n'
            '    destination.mkdir()\n'
            '    (destination / "bun.lock").write_text("stub-lock")\n'
            '    (destination / "packages/coding-agent").mkdir(parents=True)\n'
            '    (destination / "packages/natives/native").mkdir(parents=True)\n'
            '    (destination / "packages/natives/native/index.js").write_text("stub")\n'
            'def fetch_archive(url, destination, *, sha256, reject_links=False):\n'
            '    if destination.name == "bun":\n'
            f'        assert url == {guard.BUN_URL!r} and sha256 == {guard.BUN_SHA!r}\n'
            '        assert reject_links\n'
            '        bun = destination / "bun-linux-x64/bun"\n'
            '        bun.parent.mkdir(parents=True)\n'
            f'        bun.write_text({("#!" + sys.executable + "\nimport sys\nprint(\"1.3.14\")\n")!r})\n'
            '    else:\n'
            f'        assert url == {guard.NATIVE_URL!r} and sha256 == {guard.NATIVE_SHA!r}\n'
            '        (ROOT / "native-ready").write_text(str(time.monotonic()))\n'
            f'        if {grow!r}:\n'
            '            for _ in range(120): time.sleep(.01)\n'
            '        package = destination / "package"\n'
            '        package.mkdir(parents=True)\n'
            '        for name in ("pi_natives.linux-x64-baseline.node", "pi_natives.linux-x64-modern.node"):\n'
            '            (package / name).write_bytes(b"finite-stub")\n')
        archive = self.root / 'retained-stub.tar'
        archive.write_bytes(b'finite-source-stub')
        # Private interpreter shim changes only fixture digests, in its own child.
        interpreter = self.root / 'python-stub'
        interpreter.write_text(
            '#!' + sys.executable + '\nimport sys\n'
            f'sys.path.insert(0, {str(Path(guard.__file__).parent)!r})\n'
            'import d77_phase_guard as g\n'
            f'g.ARCHIVE_SHA = {hashlib.sha256(archive.read_bytes()).hexdigest()!r}\n'
            f'g.LOCK_SHA = {hashlib.sha256(b"stub-lock").hexdigest()!r}\n'
            'g.SOURCE_SHA = "stub-source"\n'
            'assert sys.argv[2] == "--omp-step"\n'
            'g.omp_worker(*sys.argv[3:])\n')
        interpreter.chmod(0o755)
        phase = self.root / 'private-phase'
        phase.mkdir()
        env = dict(os.environ, PYTHONPATH=str(self.root / 'modules'))
        return guard.omp_steps(phase, archive,
                               {label: self.bounds for label in guard.OMP_LABELS},
                               python=str(interpreter), env=env), phase

    def test_exact_omp_worker_path_all_steps_with_finite_tools(self):
        steps, phase = self.omp_fixture(grow=False)
        result = self.run_guard(steps)
        self.observations['exact_omp_stub_success'] = result
        self.assertEqual(result['status'], 'complete')
        self.assertTrue(result['phase_complete'])
        self.assertEqual([r['label'] for r in result['commands']], list(guard.OMP_LABELS))
        native = json.loads((phase / 'native-fetch.json').read_text())
        self.assertEqual(len(native['native_files_sha256']), 2)
        self.assertTrue((phase / 'lock-after-views.json').exists())

    def test_exact_omp_native_fetch_is_monitored_and_blocks_abi_link(self):
        steps, phase = self.omp_fixture(grow=True)
        def free():
            ready = self.root / 'native-ready'
            return (5_400_000_000 if not ready.exists() else
                    int(4_900_000_000 - (time.monotonic()-float(ready.read_text())) * 400_000_000))
        result = guard.Monitor(self.root, free=free).run(steps)
        self.observations['exact_omp_stub_native_cancel'] = result
        self.assert_stopped(result, 7)
        row = result['commands'][-1]
        self.assertEqual(row['label'], 'native-fetch')
        self.assertTrue(row['cancelled'])
        self.assertTrue(row['cleanup_complete'])
        self.assertFalse((phase / 'native-fetch.json').exists())
        self.assertGreater(min(s['free_bytes'] for s in result['samples']),
                           guard.PHASE_FLOOR_BYTES)


if __name__ == '__main__':
    if sys.argv[1:] == ['--record']:
        import io
        directory = Path(__file__).parent
        evidence = directory / 'evidence'
        evidence.mkdir(exist_ok=True)
        stream = io.StringIO()
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(GuardControls)
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        (evidence / 'tests.log').write_text(stream.getvalue())
        print(stream.getvalue(), end='')
        (evidence / 'controls.json').write_text(json.dumps({
            'command': 'PYTHONDONTWRITEBYTECODE=1 python3 diagnostics/test_d77_phase_guard.py --record',
            'tests_run': result.testsRun, 'failures': len(result.failures),
            'errors': len(result.errors), 'successful': result.wasSuccessful(),
            'observations': GuardControls.observations,
        }, indent=2) + '\n')
        files = ('d77_phase_guard.py', 'test_d77_phase_guard.py', 'README.md',
                 'retained-1237-wrapper.txt', 'retained-1237-source.json')
        (evidence / 'frozen-source.json').write_text(json.dumps({
            'algorithm': 'sha256',
            'files': {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
                      for name in files},
        }, indent=2) + '\n')
        raise SystemExit(not result.wasSuccessful())
    else:
        unittest.main()
