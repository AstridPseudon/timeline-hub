"""Read-only portability census controls for the tiny receiving venue."""

import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
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
            'dependency-dot': {'dot.py': b'DOT SOURCE\n'},
            'dependency-underscore': {'underscore.py': b'UNDERSCORE SOURCE\n'},
        }
        roles = {
            role: {'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
            for role, files in sources.items()
        }
        for role in ('dependency-dot', 'dependency-underscore'):
            roles[role]['wheel'] = {'filename': role + '.whl',
                                    'sha256': hashlib.sha256(role.encode()).hexdigest()}
        if not missing_sources:
            for role, files in sources.items():
                for name, data in files.items():
                    write(fixture_root / role / name, data, 0o644)
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

    def run_census(self, missing_sources=False, altered_committed=False, change=None, git_error=False, bad_facts=False):
        root_path = Path(tempfile.mkdtemp(prefix='portable-census-', dir=os.environ['TMPDIR']))
        fixture_root, manifest_path, sources, maker = self.make_fixture(root_path, missing_sources)
        helper = root_path / 'bench_store.py'
        artifact = root_path / e2e_inventory.DEFAULT_BOOTSTRAP_ARTIFACT.name
        wheelhouse = root_path / 'wheelhouse'
        wheelhouse.mkdir()
        for role in ('dependency-dot', 'dependency-underscore'):
            write(wheelhouse / (role + '.whl'), role.encode())
        write(wheelhouse / 'bootstrap.whl', b'bootstrap wheel')
        write(helper, b'def initialize(\ndef ensure\nregister\n')
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
        for role, checkout in (('agent', agent), ('runtime', runtime)):
            for name, data in sources[role].items():
                write(checkout / name, data, 0o644)
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

        if change is not None:
            change(fixture_root, manifest_path, args)

        def fake_command(argv, **kwargs):
            if git_error:
                raise subprocess.TimeoutExpired(argv, 1)
            self.assertEqual(kwargs.get('env', {}).get('GIT_OPTIONAL_LOCKS'), '0')
            if argv[0:2] != ['git', '-C']:
                return subprocess.CompletedProcess(argv, 0, '', '')
            checkout = argv[2]
            operation = argv[3]
            variant = getattr(args, 'git_variant', None) if checkout == str(args.agent) else None
            if operation == 'rev-parse':
                return subprocess.CompletedProcess(argv, 0, 'invalid-head\n' if variant == 'head' else HEAD + '\n', '')
            if operation == 'status':
                return subprocess.CompletedProcess(argv, 0, ' M agent.py\n' if variant == 'dirty' else '', '')
            if operation == 'ls-tree' and '--name-only' in argv:
                role = 'agent' if checkout == str(args.agent) else 'runtime'
                return subprocess.CompletedProcess(argv, 0, '\n'.join(sources[role]) + '\n', '')
            if operation == 'ls-tree':
                role = 'agent' if checkout == str(args.agent) else 'runtime'
                rows = [f'{"100755" if variant == "mode" else "100644"} blob {"b" * 40}\t{name}' for name in sources[role]]
                return subprocess.CompletedProcess(argv, 0, '\n'.join(rows) + '\n', '')
            raise AssertionError('unexpected census command: ' + repr(argv))

        def fake_blob(path, revision, name):
            return source_data[str(agent if str(path) == str(args.agent) else runtime)]

        facts = {'version': '3.13.0 fixture', 'build': '1.4.0',
                 'setuptools': '80.9.0', 'wheel': '0.46.3'}
        access = os.access
        patches = [
            patch.object(e2e_inventory, 'FIXTURE_ROOT', fixture_root),
            patch.object(e2e_inventory, 'FIXTURE_MANIFEST', manifest_path),
            patch.object(e2e_inventory, 'PORTABLE_PARENT', fixture_root / 'makers/parent-maker'),
            patch.object(e2e_inventory, 'MAKER', fixture_root / 'makers/candidate-maker'),
            patch.object(e2e_inventory, 'HELPER_SHA256', hashlib.sha256(b'def initialize(\ndef ensure\nregister\n').hexdigest()),
            patch.object(e2e_inventory, 'REQUIRED_SOURCE_FILES', {role: tuple(files) for role, files in sources.items()}),
            patch.object(e2e_inventory, 'BOOTSTRAP_ARTIFACT_SHA256', hashlib.sha256(b'bootstrap fixture\n').hexdigest()),
            patch.object(e2e_inventory, 'BOOTSTRAP_WHEELS', {'bootstrap.whl': hashlib.sha256(b'bootstrap wheel').hexdigest()}),
            patch.object(e2e_inventory, 'PARENT_MAKER_SHA256', hashlib.sha256(maker).hexdigest()),
            patch.object(e2e_inventory, 'MAKER_SHA256', hashlib.sha256(maker).hexdigest()),
            patch.object(e2e_inventory, 'store_module', side_effect=AssertionError('census imported Store')),
            patch.object(e2e_inventory, 'prepare_venue', side_effect=AssertionError('census started setup')),
            patch.object(e2e_inventory, 'run_venue', side_effect=AssertionError('census started maker')),
            patch.object(e2e_inventory, 'RESERVE', 0),
            patch.object(e2e_inventory, 'STOP_LINE', 0),
            patch.object(e2e_inventory, 'command', side_effect=fake_command),
            patch.object(e2e_inventory, 'committed_source_bytes', side_effect=fake_blob),
            patch.object(e2e_inventory, 'python_facts', return_value=[] if bad_facts else facts),
            patch.object(e2e_inventory, 'df_free_bytes', return_value=1),
            patch.object(e2e_inventory.shutil, 'which', side_effect=lambda name: None if name == getattr(args, 'missing_command', None) else '/usr/bin/fixture'),
            patch.object(e2e_inventory.os, 'access', side_effect=lambda path, mode: False if getattr(args, 'unwritable', False) and mode & os.W_OK else access(path, mode)),
            patch.object(e2e_inventory, 'fixture_sources', side_effect=AssertionError('check-only loaded source fixture eagerly')),
            patch.dict(os.environ, {'TMPDIR': str(getattr(args, 'scratch', root_path))}),
        ]
        for active in patches:
            active.start()
        def snapshot():
            return {str(path): (path.lstat().st_mode, path.read_bytes() if path.is_file() else None)
                    for path in root_path.rglob('*') if path != args.result}

        before = snapshot()
        prior_result = args.result.read_bytes() if isinstance(args.result, Path) and args.result.is_file() else None
        try:
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
                result = e2e_inventory.check_only(args)
            census, _ = json.JSONDecoder().raw_decode(stdout.getvalue())
            self.assertEqual(snapshot(), before)
            if prior_result is not None:
                self.assertEqual(args.result.read_bytes(), prior_result)
            for flag in ('mutating_setup_started', 'maker_started', 'store_initialized', 'git_mutated'):
                self.assertIs(census[flag], False)
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

    def assert_refused(self, census, label):
        self.assertFalse(census['ok'])
        self.assertIn(label, census['missing'])
        self.assertIn('required command timeout', census['checked'])
        self.assertIn('candidate and parent maker verifier blocks are byte-identical', census['checked'])

    def test_valid_census_authenticates_sources_wheels_makers_and_all_prerequisites(self):
        result, census = self.run_census()
        self.assertEqual(result, 0, census['missing'])
        self.assertTrue(census['ok'])
        self.assertEqual(census['missing'], [])
        for label in ('Agent source carrier checkout committed source bytes agent.py',
                      'Runtime source carrier checkout committed source bytes runtime.py',
                      'local wheel dependency-dot.whl', 'local wheel dependency-underscore.whl',
                      'local wheel bootstrap.whl', 'packaged parent maker bytes and mode'):
            self.assertIn(label, census['checked'])

    def test_malformed_role_variants_accumulate_with_simultaneous_missing_prerequisites(self):
        for role in ('agent', 'runtime', 'dependency-dot', 'dependency-underscore'):
            for value in (None, [], ['not-a-role'], '', 1, True):
                with self.subTest(role=role, value=value):
                    def change(_root, manifest_path, args, role=role, value=value):
                        manifest = json.loads(manifest_path.read_text())
                        manifest['roles'][role] = value
                        manifest_path.write_text(json.dumps(manifest))
                        args.helper = args.helper.parent / 'missing-helper'
                        args.runner_python = args.helper.parent / 'missing-runner'
                    result, census = self.run_census(change=change)
                    self.assertEqual(result, 2)
                    self.assert_refused(census, 'fixture source manifest role is valid: ' + role)
                    self.assertIn('protected Store helper hash', census['missing'])
                    self.assertIn('runner Agent Python exists and is executable', census['missing'])
                    self.assertIn('local wheel bootstrap.whl', census['checked'])

    def test_missing_roles_and_malformed_role_maps_are_not_an_empty_success(self):
        for value in (None, [], '', 2, True, {}, {'agent': {}}):
            with self.subTest(value=value):
                def change(_root, manifest_path, _args, value=value):
                    manifest = json.loads(manifest_path.read_text())
                    manifest['roles'] = value
                    manifest_path.write_text(json.dumps(manifest))
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'fixture source manifest has exactly the four required roles')
                self.assertIn('fixture source manifest role is valid: runtime', census['missing'])

    def test_missing_malformed_or_wrong_schema_manifest_still_checks_other_inputs(self):
        for data in (None, b'{', b'[]', b'null', b'1', b'true', b'"manifest"', b'{}', b'\xff'):
            with self.subTest(data=data):
                def change(_root, manifest_path, args, data=data):
                    if data is None:
                        manifest_path.rename(manifest_path.with_suffix('.absent'))
                    else:
                        manifest_path.write_bytes(data)
                    args.wheelhouse = args.wheelhouse.parent / 'missing-wheels'
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'fixture manifest is valid JSON with expected schema')
                self.assertIn('local wheel bootstrap.whl', census['missing'])
                self.assertIn('Agent source carrier checkout has a clean receiving-service Git commit', census['missing'])

    def test_source_file_maps_names_and_hash_types_are_explicitly_validated(self):
        variants = [None, [], '', True, {}, {'agent.py': None}, {'agent.py': []},
                    {'agent.py': 3}, {'agent.py': 'a' * 63}, {'agent.py': 'G' * 64},
                    {'../escape.py': 'a' * 64}, {'/absolute': 'a' * 64},
                    {'nested/../escape': 'a' * 64}, {'bad\x00name': 'a' * 64}, {'a//b': 'a' * 64}]
        for files in variants:
            with self.subTest(files=files):
                def change(_root, manifest_path, _args, files=files):
                    manifest = json.loads(manifest_path.read_text())
                    manifest['roles']['agent']['files'] = files
                    manifest_path.write_text(json.dumps(manifest))
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assertFalse(census['ok'])
                self.assertTrue(any(label.startswith('fixture source manifest') for label in census['missing']))
                self.assertIn('Runtime source carrier checkout committed source bytes runtime.py', census['checked'])

    def test_maker_map_entry_and_field_shapes_are_censused(self):
        cases = [('makers', None), ('makers', []), ('makers', {}), ('parent', []),
                 ('path', None), ('path', []), ('path', '../escape'), ('path', 'makers/candidate-maker'), ('sha256', {}),
                 ('sha256', 'g' * 64), ('sha256', 'a' * 64), ('mode', 755), ('mode', []), ('mode', '644'),
                 ('mode', 'invalid'), ('commit', None), ('commit', 'not-a-commit')]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                def change(_root, manifest_path, _args, field=field, value=value):
                    manifest = json.loads(manifest_path.read_text())
                    if field == 'makers':
                        manifest[field] = value
                    elif field == 'parent':
                        manifest['makers'][field] = value
                    else:
                        manifest['makers']['parent'][field] = value
                    manifest_path.write_text(json.dumps(manifest))
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assertFalse(census['ok'])
                self.assertTrue(any(label.startswith('fixture maker') for label in census['missing']))
                self.assertIn('local wheel bootstrap.whl', census['checked'])

    def test_wheel_shapes_and_pins_are_checked_even_without_wheelhouse(self):
        for wheel in (None, [], True, {}, {'filename': []},
                      {'filename': '../escape.whl', 'sha256': 'a' * 64},
                      {'filename': 'a.whl', 'sha256': 1},
                      {'filename': 'a.whl', 'sha256': 'g' * 64},
                      {'filename': 'bootstrap.whl', 'sha256': 'a' * 64}):
            with self.subTest(wheel=wheel):
                def change(_root, manifest_path, args, wheel=wheel):
                    manifest = json.loads(manifest_path.read_text())
                    manifest['roles']['dependency-dot']['wheel'] = wheel
                    manifest_path.write_text(json.dumps(manifest))
                    args.wheelhouse = None
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assertIn('local wheel bootstrap.whl', census['missing'])
                self.assertTrue(any(label.startswith('tiny dependency wheel') for label in census['missing']))

    def test_missing_changed_wrong_mode_or_symlink_fixture_files_refuse(self):
        for kind in ('missing', 'changed', 'mode', 'symlink', 'directory', 'non-utf8'):
            with self.subTest(kind=kind):
                def change(root, manifest_path, _args, kind=kind):
                    source = root / 'agent/agent.py'
                    if kind == 'mode':
                        source.chmod(0o755)
                    elif kind == 'changed':
                        source.write_bytes(b'changed')
                    elif kind == 'non-utf8':
                        source.write_bytes(b'\xff')
                        manifest = json.loads(manifest_path.read_text())
                        manifest['roles']['agent']['files']['agent.py'] = hashlib.sha256(b'\xff').hexdigest()
                        manifest_path.write_text(json.dumps(manifest))
                    else:
                        source.rename(source.with_suffix('.saved'))
                        if kind == 'symlink':
                            source.symlink_to(source.with_suffix('.saved'))
                        elif kind == 'directory':
                            source.mkdir()
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'fixture source agent/agent.py')

    def test_missing_wrong_hash_mode_or_symlink_makers_refuse_without_verifier_crash(self):
        for kind in ('missing', 'changed', 'mode', 'symlink', 'directory'):
            with self.subTest(kind=kind):
                def change(root, _manifest_path, _args, kind=kind):
                    maker = root / 'makers/parent-maker'
                    if kind == 'mode':
                        maker.chmod(0o644)
                    elif kind == 'changed':
                        maker.write_bytes(b'no verifier')
                    else:
                        maker.rename(maker.with_suffix('.saved'))
                        if kind == 'symlink':
                            maker.symlink_to(maker.with_suffix('.saved'))
                        elif kind == 'directory':
                            maker.mkdir()
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'packaged parent maker bytes and mode')
                self.assertIn('candidate and parent maker verifier blocks are byte-identical', census['missing'])

    def test_wrong_wheel_hash_and_missing_helper_and_artifact_accumulate(self):
        def change(_root, _manifest_path, args):
            (args.wheelhouse / 'dependency-dot.whl').write_bytes(b'foreign')
            args.helper = args.helper.parent / 'absent-helper'
            args.bootstrap_artifact = args.bootstrap_artifact.parent / 'absent-bootstrap'
        result, census = self.run_census(change=change)
        self.assertEqual(result, 2)
        for label in ('local wheel dependency-dot.whl', 'protected Store helper hash', 'local bootstrap artifact hash'):
            self.assert_refused(census, label)

    def test_nonphysical_relative_or_wrong_type_paths_are_structured_missing(self):
        for field in ('helper', 'wheelhouse', 'agent', 'runtime', 'bootstrap_artifact',
                      'runner_python', 'build_python', 'python', 'orch_root', 'parent_work', 'candidate_work'):
            for value in (None, [], 7, 'relative/path', '/bad\x00path'):
                with self.subTest(field=field, value=value):
                    def change(_root, _manifest_path, args, field=field, value=value):
                        setattr(args, field, value)
                    result, census = self.run_census(change=change)
                    self.assertEqual(result, 2)
                    self.assertFalse(census['ok'])
                    self.assertIn('required command timeout', census['checked'])

    def test_supported_venv_python_symlinks_remain_valid(self):
        def change(root, _manifest_path, args):
            for field in ('runner_python', 'build_python'):
                original = getattr(args, field)
                link = root / (field + '-link')
                link.symlink_to(original)
                setattr(args, field, link)
        result, census = self.run_census(change=change)
        self.assertEqual(result, 0, census['missing'])

    def test_git_timeout_and_malformed_python_facts_accumulate(self):
        result, census = self.run_census(git_error=True, bad_facts=True)
        self.assertEqual(result, 2)
        for label in ('Agent source carrier checkout Git history and exact committed source are readable',
                      'Runtime source carrier checkout Git history and exact committed source are readable',
                      'runner Agent Python reports Python 3.13 with required imports',
                      'child Python reports Python 3.13 with required imports'):
            self.assert_refused(census, label)

    def test_overlapping_private_roots_and_unsafe_source_path_are_refused(self):
        for kind in ('same', 'nested', 'existing', 'scratch', 'unsafe-agent', 'venue-collision'):
            with self.subTest(kind=kind):
                def change(root, _manifest_path, args, kind=kind):
                    if kind == 'same':
                        args.parent_work = args.candidate_work
                    elif kind == 'nested':
                        args.parent_work = args.orch_root / 'nested'
                    elif kind == 'existing':
                        args.parent_work.mkdir()
                    elif kind == 'scratch':
                        args.parent_work = root.parent
                    elif kind == 'venue-collision':
                        args.prepare_venue = args.result
                    else:
                        unsafe = args.agent.with_name('unsafe agent')
                        args.agent.rename(unsafe)
                        args.agent = unsafe
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assertFalse(census['ok'])

    def test_existing_result_and_symlink_result_are_never_overwritten(self):
        for symlink in (False, True):
            with self.subTest(symlink=symlink):
                def change(root, _manifest_path, args, symlink=symlink):
                    protected = root.parent / 'protected-result'
                    protected.write_bytes(b'keep this result')
                    if symlink:
                        args.result.symlink_to(protected)
                    else:
                        args.result.write_bytes(b'existing result')
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'check-only result path is inside TMPDIR')

    def test_fixture_helpers_refuse_malformed_manifest_with_runtime_error(self):
        root = Path(tempfile.mkdtemp(prefix='bad-metadata-', dir=os.environ['TMPDIR']))
        fixture_root, manifest_path, _, _ = self.make_fixture(root)
        manifest = json.loads(manifest_path.read_text())
        manifest['roles']['dependency-dot'] = []
        manifest_path.write_text(json.dumps(manifest))
        with patch.object(e2e_inventory, 'FIXTURE_ROOT', fixture_root), \
                patch.object(e2e_inventory, 'FIXTURE_MANIFEST', manifest_path):
            for helper in (e2e_inventory.fixture_sources, e2e_inventory.fixture_makers, e2e_inventory.fixture_wheel_pins):
                with self.subTest(helper=helper.__name__), self.assertRaisesRegex(RuntimeError, 'fixture source manifest'):
                    helper()

    def test_required_commands_and_tmpdir_write_capability_join_the_census(self):
        for name in ('python3', 'timeout', 'mkdir', 'git'):
            with self.subTest(name=name):
                def change(_root, _manifest_path, args, name=name):
                    args.missing_command = name
                    args.unwritable = True
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'required command ' + name)
                self.assertIn('TMPDIR is writable and searchable', census['missing'])
                self.assertIn('Runtime source carrier checkout committed source bytes runtime.py', census['checked'])

    def test_wrong_git_head_dirty_checkout_and_committed_modes_are_refused(self):
        for variant in ('head', 'dirty', 'mode'):
            with self.subTest(variant=variant):
                def change(_root, _manifest_path, args, variant=variant):
                    args.git_variant = variant
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'Agent source carrier checkout has a clean receiving-service Git commit')

    def test_nonregular_manifest_still_emits_all_independent_missing_inputs(self):
        for kind in ('symlink', 'directory', 'fifo'):
            with self.subTest(kind=kind):
                def change(_root, manifest_path, args, kind=kind):
                    original = manifest_path.with_suffix('.saved')
                    manifest_path.rename(original)
                    if kind == 'symlink':
                        manifest_path.symlink_to(original)
                    elif kind == 'directory':
                        manifest_path.mkdir()
                    else:
                        os.mkfifo(manifest_path)
                    args.helper = None
                # The FIFO is never opened: regular-file validation comes first.
                result, census = self.run_census(change=change)
                self.assertEqual(result, 2)
                self.assert_refused(census, 'fixture manifest is a regular non-symlink file')
                self.assertIn('protected Store helper hash', census['missing'])

    def test_prepare_cli_requires_successful_complete_census_before_setup(self):
        root = Path(tempfile.mkdtemp(prefix='prepare-refusal-', dir=os.environ['TMPDIR']))
        venue = root / 'venue.json'
        stdout = io.StringIO()
        with patch.object(sys, 'argv', ['e2e_inventory.py', '--prepare-venue', str(venue)]), \
                patch.object(e2e_inventory, 'prepare_venue') as prepare, \
                patch.dict(os.environ, {'TMPDIR': str(root)}), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            result = e2e_inventory.main()
        self.assertEqual(result, 2)
        census, _ = json.JSONDecoder().raw_decode(stdout.getvalue())
        self.assert_refused(census, 'protected Store helper is supplied as an absolute physical path')
        prepare.assert_not_called()
        self.assertFalse(venue.exists())

    def test_invalid_optional_result_path_and_tmpdir_are_refused(self):
        for field, values in (('result', ([], 7, 'relative', '/bad\x00path')),
                              ('scratch', ('', 'relative', '/missing-portable-tmpdir'))):
            for value in values:
                with self.subTest(field=field, value=value):
                    def change(_root, _manifest_path, args, field=field, value=value):
                        setattr(args, field, value)
                    result, census = self.run_census(change=change)
                    self.assertEqual(result, 2)
                    label = ('check-only result path is inside TMPDIR' if field == 'result'
                             else 'TMPDIR is an existing physical absolute directory')
                    self.assert_refused(census, label)

    def test_actual_manifest_helper_and_frozen_makers_pass_readonly_component_checks(self):
        root = Path(tempfile.mkdtemp(prefix='actual-components-', dir=os.environ['TMPDIR']))
        helper = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py')
        args = self.args(root, helper, None, None, None,
                         e2e_inventory.DEFAULT_RUNNER_PYTHON, e2e_inventory.DEFAULT_RUNNER_PYTHON,
                         e2e_inventory.DEFAULT_CHILD_PYTHON, e2e_inventory.DEFAULT_BOOTSTRAP_ARTIFACT)
        stdout = io.StringIO()
        with patch.dict(os.environ, {'TMPDIR': str(root)}), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            result = e2e_inventory.check_only(args)
        self.assertEqual(result, 2)  # Receiving Git carriers/wheels are intentionally absent.
        census, _ = json.JSONDecoder().raw_decode(stdout.getvalue())
        for label in ('protected Store helper hash', 'Store API initialize is present in the protected helper',
                      'Store API ensure is present in the protected helper', 'Store API registration is present in the protected helper',
                      'packaged parent maker bytes and mode', 'packaged candidate maker bytes and mode',
                      'parent maker has exactly one verifier block', 'candidate maker has exactly one verifier block',
                      'candidate and parent maker verifier blocks are byte-identical'):
            self.assertIn(label, census['checked'])
            self.assertNotIn(label, census['missing'])
        for label in census['missing']:
            self.assertFalse(label.startswith('fixture '), label)


if __name__ == '__main__':
    unittest.main()
