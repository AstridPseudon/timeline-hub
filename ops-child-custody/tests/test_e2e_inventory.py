"""Read-only portability census controls for the tiny receiving venue."""

import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import e2e_inventory


HEAD = 'a' * 40


def write(path, data, mode=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    if mode is not None:
        path.chmod(mode)


class PortableCensusTests(unittest.TestCase):
    def make_fixture(self, root, missing_sources=False):
        fixture_root = root / 'tiny'
        sources = {
            'agent': {'agent.py': b'AGENT SOURCE\n'},
            'runtime': {'runtime.py': b'RUNTIME SOURCE\n'},
        }
        roles = {
            role: {'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
            for role, files in sources.items()
        }
        if not missing_sources:
            for role, files in sources.items():
                for name, data in files.items():
                    write(fixture_root / role / name, data)
        else:
            write(fixture_root / 'runtime' / 'runtime.py', b'MALFORMED SOURCE\n')
        maker = b'# STORE_VERIFY_BEGIN\nVERIFY\n# STORE_VERIFY_END\n'
        makers = {}
        for role, name in (('parent', 'parent-maker'), ('candidate', 'candidate-maker')):
            path = fixture_root / 'makers' / name
            write(path, maker, 0o755)
            makers[role] = {'path': str(path.relative_to(fixture_root)),
                            'commit': HEAD, 'sha256': hashlib.sha256(maker).hexdigest(),
                            'mode': '755'}
        manifest = {'schema': 'timeline.ops-child-custody.tiny-source.v1',
                    'source_commit': HEAD, 'makers': makers, 'roles': roles}
        manifest_path = fixture_root / 'manifest.json'
        write(manifest_path, (json.dumps(manifest) + '\n').encode())
        return fixture_root, manifest_path, sources, maker

    def args(self, root, helper, wheelhouse, agent, runtime, runner, build, child, artifact):
        return SimpleNamespace(
            helper=helper, wheelhouse=wheelhouse, agent=agent, runtime=runtime,
            runner_python=runner, build_python=build, python=child,
            bootstrap_artifact=artifact, orch_root=root / 'orch',
            parent_work=root / 'parent', candidate_work=root / 'candidate',
            result=root / 'check-only.json',
        )

    def run_census(self, missing_sources=False, altered_committed=False):
        root_path = Path(tempfile.mkdtemp(prefix='portable-census-', dir=os.environ['TMPDIR']))
        fixture_root, manifest_path, sources, maker = self.make_fixture(root_path, missing_sources)
        helper = root_path / 'bench_store.py'
        artifact = root_path / 'bootstrap.tgz'
        wheelhouse = root_path / 'wheelhouse'
        wheelhouse.mkdir()
        write(helper, b'Store.initialize\ndef ensure\nregister\n')
        write(artifact, b'bootstrap fixture\n')
        python_paths = []
        for name in ('runner', 'build', 'child'):
            path = root_path / name
            write(path, b'python fixture\n', 0o755)
            python_paths.append(path)
        agent = root_path / 'agent-checkout'
        runtime = root_path / 'runtime-checkout'
        agent.mkdir()
        runtime.mkdir()
        if missing_sources:
            args = self.args(root_path, root_path / 'missing-bench-store.py',
                             root_path / 'missing-wheelhouse', root_path / 'missing-agent-checkout',
                             root_path / 'missing-runtime-checkout', root_path / 'missing-runner',
                             root_path / 'missing-build', root_path / 'missing-child',
                             root_path / 'missing-bootstrap.tgz')
        else:
            args = self.args(root_path, helper, wheelhouse, agent, runtime,
                             python_paths[0], python_paths[1], python_paths[2], artifact)
        source_data = {str(agent): sources['agent']['agent.py'],
                       str(runtime): sources['runtime']['runtime.py']}
        if altered_committed:
            source_data[str(agent)] = b'ALTERED COMMITTED BYTES\n'

        def fake_command(argv, **kwargs):
            if argv[0:2] != ['git', '-C']:
                return subprocess.CompletedProcess(argv, 0, '', '')
            checkout = argv[2]
            operation = argv[3]
            if operation == 'rev-parse':
                return subprocess.CompletedProcess(argv, 0, HEAD + '\n', '')
            if operation == 'status':
                return subprocess.CompletedProcess(argv, 0, '', '')
            if operation == 'ls-tree' and '--name-only' in argv:
                role = 'agent' if checkout == str(agent) else 'runtime'
                return subprocess.CompletedProcess(argv, 0, '\n'.join(sources[role]) + '\n', '')
            if operation == 'ls-tree':
                role = 'agent' if checkout == str(agent) else 'runtime'
                rows = [f'100644 blob {"b" * 40}\t{name}' for name in sources[role]]
                return subprocess.CompletedProcess(argv, 0, '\n'.join(rows) + '\n', '')
            raise AssertionError('unexpected census command: ' + repr(argv))

        def fake_blob(path, revision, name):
            return source_data[str(path)]

        facts = {'version': '3.13.0 fixture', 'build': '1.4.0',
                 'setuptools': '80.9.0', 'wheel': '0.46.3'}
        patches = [
            patch.object(e2e_inventory, 'FIXTURE_ROOT', fixture_root),
            patch.object(e2e_inventory, 'FIXTURE_MANIFEST', manifest_path),
            patch.object(e2e_inventory, 'PORTABLE_PARENT', fixture_root / 'makers/parent-maker'),
            patch.object(e2e_inventory, 'MAKER', fixture_root / 'makers/candidate-maker'),
            patch.object(e2e_inventory, 'HELPER_SHA256', hashlib.sha256(helper.read_bytes()).hexdigest()),
            patch.object(e2e_inventory, 'BOOTSTRAP_ARTIFACT_SHA256', hashlib.sha256(artifact.read_bytes()).hexdigest()),
            patch.object(e2e_inventory, 'BOOTSTRAP_WHEELS', {}),
            patch.object(e2e_inventory, 'fixture_wheel_pins', return_value={}),
            patch.object(e2e_inventory, 'RESERVE', 0),
            patch.object(e2e_inventory, 'STOP_LINE', 0),
            patch.object(e2e_inventory, 'command', side_effect=fake_command),
            patch.object(e2e_inventory, 'committed_source_bytes', side_effect=fake_blob),
            patch.object(e2e_inventory, 'python_facts', return_value=facts),
            patch.object(e2e_inventory, 'df_free_bytes', return_value=1),
            patch.object(e2e_inventory.shutil, 'which', return_value='/usr/bin/fixture'),
            patch.object(e2e_inventory, 'fixture_sources', side_effect=AssertionError('check-only loaded source fixture eagerly')),
            patch.dict(os.environ, {'TMPDIR': str(root_path)}),
        ]
        for active in patches:
            active.start()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                result = e2e_inventory.check_only(args)
            census = json.loads(args.result.read_text())
        finally:
            for active in reversed(patches):
                active.stop()
        return result, census

    def test_check_only_refuses_altered_clean_committed_source_bytes(self):
        result, census = self.run_census(altered_committed=True)
        self.assertEqual(result, 2)
        self.assertFalse(census['ok'])
        self.assertIn('Agent source carrier checkout committed source bytes agent.py', census['missing'])
        self.assertNotIn('fixture source agent/agent.py', census['missing'])
        self.assertNotIn('Agent source carrier checkout has a clean receiving-service Git commit', census['missing'])

    def test_check_only_accumulates_missing_and_malformed_sources_with_other_prerequisites(self):
        result, census = self.run_census(missing_sources=True)
        self.assertEqual(result, 2)
        self.assertFalse(census['ok'])
        self.assertIn('fixture source agent/agent.py', census['missing'])
        self.assertIn('fixture source runtime/runtime.py', census['missing'])
        self.assertIn('protected Store helper is supplied as an absolute physical path', census['missing'])
        self.assertIn('local bootstrap artifact hash', census['missing'])
        self.assertIn('Agent source carrier checkout Git history and exact committed source are readable', census['missing'])
        self.assertGreater(len(census['missing']), 5)


if __name__ == '__main__':
    unittest.main()
