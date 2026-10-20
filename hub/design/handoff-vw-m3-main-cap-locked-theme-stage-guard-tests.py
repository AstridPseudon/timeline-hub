"""Offline guard calibrations; synthetic grants never authorize a real capture."""
from contextlib import ExitStack, contextmanager, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-main-cap-locked-theme-stage-'
TARGET = Path(str(PREFIX) + 'controller.py')
RENDER = Path(str(PREFIX) + 'render.mjs')
spec = importlib.util.spec_from_file_location('repaired_controller', TARGET)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


@contextmanager
def synthetic_attempt(private, **overrides):
    """Exercise real allocation/finally; never execute source or child processes."""
    result = {'status': 'SYNTHETIC_ONLY', 'blockers': [], 'free_bytes': 100 * m.FLOOR,
              'required_before_extraction_bytes': 0, 'source': {'unpacked_bytes': 0}, 'theme': {'unpacked_bytes': 0}}
    defaults = {'OWN': private, 'PREFIX': private / 'synthetic-', 'central_grant': lambda: 'SYNTHETIC-NO-SERVICE',
                'script_grant': lambda: None, 'preflight': lambda: result,
                'graph_check': lambda: ({}, {}), 'theme_check': lambda: result['theme'], 'source_check': lambda: result['source'],
                'verify_stage': lambda *a, **k: None, 'inventory': lambda *a: {},
                'evidence': lambda *a: None, 'disk': lambda *a: None}
    defaults.update(overrides)
    with ExitStack() as stack:
        for name, value in defaults.items():
            stack.enter_context(patch.object(m, name, value))
        stack.enter_context(patch.object(m.subprocess, 'Popen', side_effect=AssertionError('child execution forbidden')))
        stack.enter_context(patch.object(sys, 'argv', [str(TARGET), 'capture']))
        stack.enter_context(redirect_stdout(io.StringIO()))
        yield


class Guards(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='handoff-vw-m3-main-cap-locked-theme-stage-guard-only-', dir=m.DESIGN)
        self.addCleanup(self.temporary.cleanup)
        self.private = Path(self.temporary.name)

    def test_durable_pinned_main_reads(self):
        self.assertEqual(m.REPO, Path('/home/user/work/agent'))
        self.assertEqual(m.MAIN, 'a411628f8fd6129f9c58c332019b56769d997384')
        self.assertEqual(subprocess.check_output(['git', '-C', str(m.REPO), 'cat-file', '-t', m.MAIN], text=True), 'commit\n')
        calls = []
        original = m.subprocess.check_output

        def read_only(command, **kwargs):
            calls.append(command)
            self.assertEqual(command[:3], ['git', '-C', '/home/user/work/agent'])
            self.assertIn(command[3], ('archive', 'show'))
            self.assertTrue(command[4].startswith(m.MAIN))
            return original(command, **kwargs)

        with patch.object(m.subprocess, 'check_output', side_effect=read_only):
            source = m.source_check()
        self.assertEqual(len(calls), 2)
        self.assertEqual(source['original_main_files'], 2414)
        self.assertEqual(len(source['locked_archive_members']), 29)
        self.assertEqual(len(source['seven_expected_output_hashes']), 7)

    def test_historical_theme_source_and_main_version(self):
        proof = m.theme_check()
        self.assertEqual(proof['version'], '0.1.1')
        self.assertEqual(proof['member_count'], 20)
        self.assertFalse(proof['github_archive_integrity_verified'])
        self.assertEqual(proof['v0.1.0_to_v0.1.1_changed_members'], ['package.json'])
        root = self.private / 'main'
        root.mkdir()
        m.stage_theme(root, proof)
        theme = root / 'remotion/node_modules/@banodoco/timeline-theme-2rp'
        self.assertFalse(theme.is_symlink())
        self.assertEqual(m.inventory(theme), proof['member_sha256'])
        with self.assertRaisesRegex(RuntimeError, 'overwrite existing package'):
            m.stage_theme(root, proof)
        (theme / 'src/effects/art-card/component.tsx').write_text('changed')
        with self.assertRaisesRegex(RuntimeError, 'historical theme changed'):
            m.verify_stage(self.private, {'source_files': {}})

    def test_disk_boundaries_and_quiet(self):
        for remaining in (0, m.HEADROOM + m.PNG_RAW, 2283658796):
            with self.subTest(remaining=remaining), patch.object(m, 'quiet', return_value=False):
                with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=m.FLOOR + remaining - 1)):
                    with self.assertRaisesRegex(RuntimeError, 'disk BLOCKED'):
                        m.disk(remaining)
                with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=m.FLOOR + remaining)):
                    self.assertEqual(m.disk(remaining), m.FLOOR + remaining)
        with patch.object(m.shutil, 'disk_usage', return_value=SimpleNamespace(free=100 * m.FLOOR)), patch.object(m, 'quiet', return_value=True):
            with self.assertRaisesRegex(RuntimeError, 'QUIET'):
                m.disk(0)
        self.assertEqual(m.FLOOR, 10 * 1024**3)
        self.assertEqual(m.HEADROOM, 2 * 1024**3)

    def test_missing_grant_precedes_preflight_or_allocation(self):
        with patch.object(m, 'GRANT', self.private / 'ABSENT'), patch.object(m, 'preflight', side_effect=AssertionError('preflight ran')), patch.object(sys, 'argv', [str(TARGET), 'capture']):
            with self.assertRaisesRegex(RuntimeError, 'exact grant missing'):
                m.main()
        self.assertEqual(list(self.private.iterdir()), [])

    def test_both_hashes_and_path_only_refusal_before_allocation_or_execution(self):
        prefix = self.private / 'synthetic-'
        controller = Path(str(prefix) + 'controller.py')
        render = Path(str(prefix) + 'render.mjs')
        grant = self.private / 'SYNTHETIC-GRANT'
        controller.write_bytes(TARGET.read_bytes())
        render.write_bytes(RENDER.read_bytes())
        with patch.object(m, '__file__', str(controller)), patch.object(m, 'PREFIX', prefix), patch.object(m, 'GRANT', grant):
            approved = '\n'.join([m.suite_line(), f'controller_sha256={m.file_sha(controller)}', f'render_sha256={m.file_sha(render)}']) + '\n'
            grant.write_text(approved)
            m.script_grant()  # Positive synthetic calibration.
            cases = [('path-only', None), ('controller', controller), ('render', render)]
            for label, changed in cases:
                with self.subTest(label=label):
                    grant.write_text(m.suite_line() + '\n' if changed is None else approved)
                    if changed:
                        original = changed.read_bytes()
                        changed.write_bytes(original + b'\n// changed bytes\n')
                    with patch.object(m, 'preflight', side_effect=AssertionError('preflight ran')), patch.object(sys, 'argv', [str(controller), 'capture']):
                        with self.assertRaisesRegex(RuntimeError, 'controller/render SHA256'):
                            m.main()
                    with patch.object(m.subprocess, 'Popen', side_effect=AssertionError('child started')):
                        with self.assertRaisesRegex(RuntimeError, 'controller/render SHA256'):
                            m.run_process(['FORBIDDEN'], self.private, {}, self.private / 'UNCREATED.log')
                    self.assertFalse((self.private / 'UNCREATED.log').exists())
                    if changed:
                        changed.write_bytes(original)

    def test_refusal_preserves_existing_directory_file_and_symlink(self):
        for kind in ('directory', 'file', 'symlink'):
            with self.subTest(kind=kind):
                private = self.private / kind
                private.mkdir()
                stage = private / 'synthetic-capture-stage'
                sentinel = private / 'sentinel'
                sentinel.write_text('must survive refusal\n')
                if kind == 'directory':
                    stage.mkdir()
                    sentinel.rename(stage / 'sentinel')
                    sentinel = stage / 'sentinel'
                elif kind == 'file':
                    stage.write_text('existing stage file\n')
                else:
                    stage.symlink_to(sentinel)
                with synthetic_attempt(private):
                    with self.assertRaisesRegex(RuntimeError, 'stage already exists'):
                        m.main()
                self.assertEqual(sentinel.read_text(), 'must survive refusal\n')
                self.assertTrue(stage.exists())
                self.assertEqual(stage.is_symlink(), kind == 'symlink')

    def test_partial_staging_and_postflight_failure_cleanup(self):
        for postflight_failure in (False, True):
            with self.subTest(postflight_failure=postflight_failure):
                private = self.private / str(postflight_failure)
                private.mkdir()
                stage = private / 'synthetic-capture-stage'

                def partial_failure(*args, **kwargs):
                    self.assertTrue((stage / 'main').is_dir())
                    (stage / 'main/partial').write_text('tiny partial allocation\n')
                    raise RuntimeError('synthetic partial staging failure')

                def evidence(name, value):
                    if postflight_failure and name == 'postflight.json':
                        raise RuntimeError('synthetic postflight write failure')

                with synthetic_attempt(private, evidence=evidence), patch.object(m.tarfile, 'open', side_effect=partial_failure):
                    with self.assertRaisesRegex(RuntimeError, 'synthetic .* failure'):
                        m.main()
                self.assertFalse(stage.exists())
                self.assertTrue((private / 'synthetic-CAPTURE-STARTED').is_file())

    def test_disk_failure_allocates_nothing(self):
        def blocked(*args):
            raise RuntimeError('disk BLOCKED: synthetic guard')

        with synthetic_attempt(self.private, disk=blocked):
            with self.assertRaisesRegex(RuntimeError, 'disk BLOCKED'):
                m.main()
        self.assertFalse((self.private / 'synthetic-capture-stage').exists())

    def test_success_cleanup_and_no_automatic_retry(self):
        def staged(stage, source):
            root = stage / 'main'
            (root / 'remotion').mkdir(parents=True)
            return root

        with synthetic_attempt(self.private, source_stage=staged, run_process=lambda *a: None, measure=lambda: {}):
            self.assertEqual(m.main(), 0)
            self.assertFalse((self.private / 'synthetic-capture-stage').exists())
            with self.assertRaises(FileExistsError):
                m.main()

    def test_renderer_hash_guards_without_renderer_execution(self):
        # Execute only the built-in-import admission header, ending before stage
        # inspection or any peer import. Redirect its ORCH to a disposable fake.
        worker = m.WORKER
        own = self.private / 'workers' / worker
        own.mkdir(parents=True)
        design = self.private / 'design'
        design.mkdir()
        result = self.private / 'tests/synthetic-result'
        result.mkdir(parents=True)
        (result / 'status').write_text('running\n')
        (result / 'request').write_text(f'target={worker}\nsuite={m.SUITE}\n')
        controller = design / f'handoff-{worker}-controller.py'
        render = design / f'handoff-{worker}-render.mjs'
        controller.write_bytes(TARGET.read_bytes())
        render.write_bytes(RENDER.read_bytes())
        suite = f'agent {m.SUITE} {m.PYTHON} {controller} capture'
        (result.parent / 'suites.conf').write_text(suite + '\n')
        approved = f'{suite}\ncontroller_sha256={m.file_sha(controller)}\nrender_sha256={m.file_sha(render)}\n'
        grant = design / f'handoff-{worker}-CAPTURE-GRANT.txt'
        header = RENDER.read_text().split('check(stage ===', 1)[0]
        header = header.replace(f"const orch = '{ORCH}';", f'const orch = {json.dumps(str(self.private))};')
        header = header.replace('const service = process.env.MAIN_CAP_SERVICE_RESULT;', f'const service = {json.dumps(str(result))};')
        header = header.replace('fileURLToPath(import.meta.url)', f'fileURLToPath({json.dumps(render.as_uri())})')
        for changed in (None, 'path-only', controller, render):
            with self.subTest(changed=str(changed)):
                grant.write_text(suite + '\n' if changed == 'path-only' else approved)
                if isinstance(changed, Path):
                    original = changed.read_bytes()
                    changed.write_bytes(original + b'\n// changed bytes\n')
                run = subprocess.run([str(m.NODE), '--input-type=module', '-'], input=header, text=True, capture_output=True)
                if changed is None:
                    self.assertEqual(run.returncode, 0, run.stderr)
                else:
                    self.assertNotEqual(run.returncode, 0)
                    self.assertIn('controller/render SHA256', run.stderr)
                if isinstance(changed, Path):
                    changed.write_bytes(original)


if __name__ == '__main__':
    unittest.main(verbosity=2)
