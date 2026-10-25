"""Report contract controls; these are not whole-make E2E evidence."""

import hashlib
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

from support import AGENT, MAKER, RUNTIME, Layout, archive, block, put


def report_script(text):
    return text.split("\nDIST_METADATA_SCRIPT='", 1)[1].split("'\nrun_stage", 1)[0]


def produce(fixture, text=None):
    result = subprocess.run(
        [sys.executable, '-B', '-I', '-c', report_script(text or MAKER.read_text()),
         str(fixture.snapshot / 'agent'), str(fixture.snapshot / 'runtime'),
         AGENT, RUNTIME, fixture.client, 'requirements/proof.lock',
         hashlib.sha256(fixture.files['agent']['requirements/proof.lock']).hexdigest()],
        text=True, capture_output=True, timeout=20,
    )
    if result.returncode:
        raise AssertionError('report producer failed: ' + result.stderr)
    put(fixture.root / '.provision-report', result.stdout.encode())
    return result.stdout


def dependency(fixture, directory, name, version='1.0', direct=False):
    path = fixture.site / (directory + '.dist-info')
    put(path / 'METADATA', f'Metadata-Version: 2.4\nName: {name}\nVersion: {version}\n'.encode())
    if direct:
        put(path / 'direct_url.json', json.dumps({
            'url': (fixture.base / 'private-input.whl').as_uri(),
            'archive_info': {'hashes': {'sha256': 'a' * 64}},
        }).encode())


class InventoryTests(unittest.TestCase):
    def test_exact_shell_freeze_stage_uses_one_inventory_and_writes_private_reports(self):
        fixture = Layout()
        dependency(fixture, 'direct-1.0', 'direct', direct=True)
        text = MAKER.read_text()
        functions = (text[text.index('progress() {'):text.index('\nN=${1:-}')]
                     + text[text.index('failure() {'):text.index('\nmissing=()')])
        stage = text[text.index('run_stage freeze "$FREEZE_TIMEOUT_SECONDS"'):
                     text.index('\nIDENTITY_SCRIPT=')]
        env = {**os.environ, 'P': sys.executable, 'DIST_METADATA_SCRIPT': report_script(text),
               'AGENT_SRC': str(fixture.snapshot / 'agent'),
               'RUNTIME_SRC': str(fixture.snapshot / 'runtime'),
               'S': AGENT, 'RUNTIME_SHA': RUNTIME, 'CLIENT_IDENTITY': fixture.client,
               'REQUIREMENTS_PATH': 'requirements/proof.lock',
               'LOCK_SHA': hashlib.sha256(fixture.files['agent']['requirements/proof.lock']).hexdigest(),
               'REPORT_TMP': str(fixture.root / '.provision-report'), 'T': str(fixture.root),
               'FREEZE_TIMEOUT_SECONDS': '20', 'KILL_AFTER_SECONDS': '1',
               'TIMEOUT_BIN': 'timeout',
               'N': 'venv-agent-child-inventory'}
        result = subprocess.run(['bash', '-u', '-o', 'pipefail', '-c', functions + '\n' + stage],
                                env=env, capture_output=True, text=True, timeout=25)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ('.provision-report', '.astrid-distribution-metadata'):
            self.assertEqual((fixture.root / name).stat().st_mode & 0o777, 0o600)
        fixture.verify()

    def test_optional_farm_schema_metadata_and_inventory_order(self):
        fixture = Layout()
        fixture.files['schema'] = {
            'pyproject.toml': b'[project]\nname = "banodoco-timeline-schema"\nversion = "0.1.0"\n'
                             b'[tool.setuptools.packages.find]\ninclude = ["banodoco_timeline_schema"]\n',
            'banodoco_timeline_schema/__init__.py': b'VALUE = "schema"\n',
            'LICENSE': b'private license\n',
        }
        fixture.archives['schema'] = archive(fixture.files['schema'])
        for name, data in fixture.files['schema'].items():
            put(fixture.snapshot / 'schema' / name, data)
        fixture.install('banodoco-timeline-schema', 'schema', ('banodoco_timeline_schema',))
        path = fixture.root / '.astrid-import-origins'
        path.write_text(path.read_text() + f'banodoco_timeline_schema={fixture.site}/banodoco_timeline_schema/__init__.py\n')
        report = produce(fixture)
        self.assertIn('banodoco-timeline-schema_provenance=archive\n', report)
        schema_commit = '242f9c4306bf3b501222cb041a9eb246ef47bc85:packages/timeline-schema/python'
        expected = {'/fixture/agent': (AGENT, 'agent'), '/fixture/runtime': (RUNTIME, 'runtime'),
                    '/fixture/schema': (schema_commit, 'schema')}

        def git(args, **kwargs):
            commit, role = expected[args[2]]
            self.assertIn(args, (['git', '-C', args[2], 'archive', commit],
                                 ['git', '-C', args[2], 'archive', '--format=tar', commit]))
            return fixture.archives[role]

        argv = ['verifier', str(fixture.root), fixture.client, '/fixture/agent', AGENT,
                '/fixture/runtime', RUNTIME, str(fixture.base), str(fixture.interpreter),
                '--farm-source', '/fixture/schema', '--staging']
        output = io.StringIO()
        with patch.object(sys, 'argv', argv), patch('subprocess.check_output', side_effect=git), \
                contextlib.redirect_stdout(output):
            exec(compile(block(MAKER.read_text(), 'STORE_VERIFY'), '<unchanged verifier>', 'exec'), {})
        self.assertIn('banodoco-timeline-schema', json.loads(output.getvalue()))

    def test_real_pip_freeze_contract_is_red_installed_inventory_producer_green(self):
        fixture = Layout()
        dependency(fixture, 'a_a-1.0', 'a_a', direct=True)
        dependency(fixture, 'a.b-1.0', 'a.b')
        dependency(fixture, 'Mixed_Case-1.0', 'Mixed_Case')
        report = produce(fixture)
        self.assertIn('a_a==1.0\n', report)
        self.assertIn('Mixed_Case==1.0\n', report)
        fixture.verify()
        pip = subprocess.run(
            [sys.executable, '-B', '-I', '-m', 'pip', 'freeze', '--all', '--path', str(fixture.site)],
            capture_output=True, text=True, timeout=20,
            env={**os.environ, 'PIP_NO_INDEX': '1', 'PIP_DISABLE_PIP_VERSION_CHECK': '1'},
        )
        self.assertEqual(pip.returncode, 0, pip.stderr)
        prefix, inventory = report.split('pip_freeze:\n')
        self.assertNotEqual(pip.stdout, inventory)
        put(fixture.root / '.provision-report', (prefix + 'pip_freeze:\n' + pip.stdout).encode())
        with self.assertRaisesRegex(SystemExit, 'maker provision report differs'):
            fixture.verify()
        produce(fixture)
        fixture.verify()

    def test_installed_inventory_preserves_duplicate_dependency_rows_and_canonical_order(self):
        fixture = Layout()
        for directory, name in (('first-1.0', 'a_a'), ('second-1.0', 'a-a'), ('third-1.0', 'a.b')):
            dependency(fixture, directory, name)
        freeze = produce(fixture).split('pip_freeze:\n')[1].splitlines()
        self.assertEqual(freeze[:3], ['a-a==1.0', 'a_a==1.0', 'a.b==1.0'])
        fixture.verify()

    def test_both_supported_source_provenance_kinds_use_installed_distribution_metadata(self):
        for kind in ('archive', 'directory'):
            fixture = Layout(kind=kind)
            produce(fixture)
            inventory = fixture.verify()
            self.assertIn('.provision-report', inventory['__root__'])
            self.assertEqual((fixture.root / '.astrid-distribution-metadata').stat().st_mode & 0o777, 0o600)

    def test_every_report_header_section_path_hash_order_and_content_mismatch_refuses(self):
        fixture = Layout()
        report = produce(fixture)
        lines = report.splitlines(keepends=True)
        # Every header, section delimiter, provenance field and freeze row.
        for ordinal, line in enumerate(lines):
            with self.subTest(ordinal=ordinal):
                changed = lines.copy()
                changed[ordinal] = line.rstrip('\n') + '-foreign\n'
                put(fixture.root / '.provision-report', ''.join(changed).encode())
                with self.assertRaisesRegex(SystemExit, 'maker provision report differs'):
                    fixture.verify()
        for changed in (report.rstrip('\n'), report + '\n', ''.join(reversed(lines))):
            put(fixture.root / '.provision-report', changed.encode())
            with self.assertRaisesRegex(SystemExit, 'maker provision report differs'):
                fixture.verify()

    def test_every_distribution_metadata_field_order_and_trailing_newline_refuses(self):
        fixture = Layout()
        produce(fixture)
        path = fixture.root / '.astrid-distribution-metadata'
        original = path.read_text()
        lines = original.splitlines(keepends=True)
        changes = []
        for ordinal in range(len(lines)):
            changed = lines.copy()
            changed[ordinal] = changed[ordinal].rstrip('\n') + '-foreign\n'
            changes.append(''.join(changed))
        changes.extend((''.join(reversed(lines)), original.rstrip('\n'), original + '\n'))
        for changed in changes:
            path.write_text(changed)
            with self.assertRaisesRegex(SystemExit, 'maker distribution metadata differs'):
                fixture.verify()

    def test_each_executable_metadata_file_refuses_after_exact_content_checks(self):
        for name in ('.astrid-distribution-metadata', '.provision-report'):
            fixture = Layout()
            produce(fixture)
            path = fixture.root / name
            path.chmod(0o700)
            with self.assertRaisesRegex(SystemExit, 'unsafe maker metadata'):
                fixture.verify()

    def test_producer_bounds_whole_report_before_granting_metadata(self):
        fixture = Layout()
        dependency(fixture, 'large-1.0', 'large', '1' * (1024 * 1024))
        with self.assertRaisesRegex(AssertionError, 'maker metadata exceeds limit'):
            produce(fixture)

    def test_source_name_identity_is_not_normalized_to_accept_mismatch(self):
        fixture = Layout()
        path = fixture.dist_paths['runtime'] / 'METADATA'
        path.write_text(path.read_text().replace('Name: astrid-runtime', 'Name: astrid_runtime'))
        with self.assertRaisesRegex(AssertionError, 'report producer failed'):
            produce(fixture)
        with self.assertRaisesRegex(SystemExit, 'distribution name/version mismatch'):
            fixture.verify()

    def test_producer_inventory_is_same_scope_as_verifier(self):
        script = report_script(MAKER.read_text())
        self.assertIn('metadata.distributions(path=[str(sites[0])])', script)
        self.assertNotIn('pip freeze', script)
        self.assertIn('sorted(freeze)', script)
        self.assertTrue(re.search(r'len\(sites\) == 1', script))


if __name__ == '__main__':
    unittest.main()
