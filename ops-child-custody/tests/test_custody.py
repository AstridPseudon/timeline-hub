import ast
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import unittest
from unittest.mock import Mock, patch

from support import (
    AGENT,
    MAKER,
    ORCH,
    PARENT,
    RUNTIME,
    Layout,
    block,
    caller_sources,
    functions,
    put,
    record_row,
    scratch,
    source_census,
    store_module,
    store_python,
)


class SourceCallerTests(unittest.TestCase):
    def test_failing_stage_retains_exact_private_stderr_and_exit_status(self):
        fixture = scratch()
        (fixture / 'tests').mkdir()
        text = MAKER.read_text()
        functions = (text[text.index('progress() {'):text.index('\nN=${1:-}')]
                     + text[text.index('failure() {'):text.index('\nmissing=()')])
        env = {**os.environ, 'T': str(fixture), 'N': 'venv-agent-child-stderr',
               'O': str(fixture), 'PYTHON': sys.executable,
               'S': AGENT, 'RUNTIME_SHA': RUNTIME, 'REQUIREMENTS_PATH': 'requirements/proof.lock',
               'LOCK_SHA': 'a' * 64, 'TIMEOUT_BIN': 'timeout', 'KILL_AFTER_SECONDS': '1'}
        result = subprocess.run(
            ['bash', '-u', '-o', 'pipefail', '-c', functions + '''\nrun_stage install-agent 20 bash -c 'printf "%s\\n" "private first error" >&2; exit 17'\n'''],
            env=env, capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 17)
        log = fixture / '.provision-stderr/install-agent.stderr'
        self.assertEqual(log.read_bytes(), b'private first error\n')
        self.assertEqual(log.stat().st_mode & 0o777, 0o600)
        marker = (fixture / '.provision-failure').read_text()
        self.assertIn('stage=install-agent\n', marker)
        self.assertIn('rc=17\n', marker)
        self.assertIn('private first error', log.read_text())
        self.assertNotIn('private first error', result.stderr)
        evidence = fixture / 'tests/provision-stderr/venv-agent-child-stderr.install-agent.stderr'
        self.assertEqual(evidence.read_bytes(), b'private first error\n')
        self.assertEqual(evidence.stat().st_mode & 0o777, 0o600)
        self.assertEqual(json.loads(evidence.with_suffix('.json').read_text())['truncated'], False)

    def test_timed_out_stage_keeps_first_stderr_and_timeout_status(self):
        fixture = scratch()
        (fixture / 'tests').mkdir()
        text = MAKER.read_text()
        functions = (text[text.index('progress() {'):text.index('\nN=${1:-}')]
                     + text[text.index('failure() {'):text.index('\nmissing=()')])
        env = {**os.environ, 'T': str(fixture), 'N': 'venv-agent-child-timeout',
               'O': str(fixture), 'PYTHON': sys.executable,
               'S': AGENT, 'RUNTIME_SHA': RUNTIME, 'REQUIREMENTS_PATH': 'requirements/proof.lock',
               'LOCK_SHA': 'b' * 64, 'TIMEOUT_BIN': 'timeout', 'KILL_AFTER_SECONDS': '1'}
        result = subprocess.run(
            ['bash', '-u', '-o', 'pipefail', '-c', functions + '''\nrun_stage pinned-requirements 1 bash -c 'printf "%s\\n" "timeout first error" >&2; sleep 5'\n'''],
            env=env, capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 124)
        log = fixture / '.provision-stderr/pinned-requirements.stderr'
        self.assertEqual(log.read_bytes(), b'timeout first error\n')
        self.assertEqual(log.stat().st_mode & 0o777, 0o600)
        self.assertIn('stage=pinned-requirements\n', (fixture / '.provision-failure').read_text())
        evidence = fixture / 'tests/provision-stderr/venv-agent-child-timeout.pinned-requirements.stderr'
        self.assertEqual(evidence.read_bytes(), b'timeout first error\n')
        self.assertEqual(evidence.stat().st_mode & 0o777, 0o600)

    def test_store_cleanup_boundary_keeps_nonzero_and_timeout_evidence(self):
        for stage, command, expected in (
            ('install-agent', "printf '%s\\n' 'store private first error' >&2; exit 17", 17),
            ('pinned-requirements', "printf '%s\\n' 'store timeout first error' >&2; sleep 5", 124),
        ):
            with self.subTest(stage=stage):
                fixture = scratch()
                tests = fixture / 'tests'
                tests.mkdir()
                (tests / 'suites.conf').write_text('')
                store_root = fixture / 'store'
                module = store_module()
                store = module.Store.initialize(store_root, tests)
                name = 'venv-agent-child-cleanup-' + stage
                identity = {'agent_sha': AGENT, 'backend_sha': RUNTIME,
                            'client_tuple': {'client.py': 'f' * 64}}
                text = MAKER.read_text()
                shell_functions = (text[text.index('progress() {'):text.index('\nN=${1:-}')]
                                    + text[text.index('failure() {'):text.index('\nmissing=()')])

                def build(stage_path, _final):
                    env = {**os.environ, 'T': str(stage_path), 'O': str(fixture),
                           'N': name, 'PYTHON': sys.executable, 'S': AGENT,
                           'RUNTIME_SHA': RUNTIME, 'REQUIREMENTS_PATH': 'requirements/proof.lock',
                           'LOCK_SHA': 'c' * 64, 'TIMEOUT_BIN': 'timeout',
                           'KILL_AFTER_SECONDS': '1'}
                    budget = '1' if expected == 124 else '20'
                    result = subprocess.run(
                        ['bash', '-u', '-o', 'pipefail', '-c',
                         shell_functions + f"\nrun_stage {stage} {budget} bash -c {shlex.quote(command)}\n"],
                        env=env, capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, expected, result.stderr)
                    lock_sha = 'c' * 64
                    build.failure_evidence = (
                        f'status=failed\nstage={stage}\nrc={expected}\n'
                        f'elapsed_seconds=0\nagent_sha={AGENT}\nruntime_sha={RUNTIME}\n'
                        f'requirements_path=requirements/proof.lock\nlock_sha256={lock_sha}\n'
                        'diagnostic=stage-command-failed\n')
                    raise subprocess.CalledProcessError(result.returncode, result.args)

                build.failure_evidence = None
                with patch.object(module.shutil, 'disk_usage',
                                  return_value=Mock(free=module.Store.RESERVE_BYTES)):
                    with self.assertRaises(subprocess.CalledProcessError):
                        store.ensure('child', identity, {'name': name, 'env': '', 'suite': ''},
                                     build, Mock(), failure_name=name)
                private = tests / 'provision-stderr' / (name + '.' + stage + '.stderr')
                self.assertEqual(private.read_text(),
                                 'store private first error\n' if expected == 17
                                 else 'store timeout first error\n')
                self.assertEqual(private.stat().st_mode & 0o777, 0o600)
                self.assertEqual(list((store_root / 'staging').iterdir()), [])
                self.assertNotIn('store ', (tests / 'provision-failures' / (name + '.txt')).read_text())

    def test_stderr_handoff_rejects_forged_paths_and_never_clobbers(self):
        fixture = scratch()
        (fixture / 'tests').mkdir()
        text = MAKER.read_text()
        shell_functions = (text[text.index('progress() {'):text.index('\nN=${1:-}')]
                           + text[text.index('failure() {'):text.index('\nmissing=()')])
        source = fixture / 'stage.stderr'
        source.write_bytes(b'first private payload\n')
        source.chmod(0o600)
        env = {**os.environ, 'O': str(fixture), 'N': 'venv-agent-child-guards',
               'PYTHON': sys.executable, 'T': str(fixture), 'S': AGENT,
               'RUNTIME_SHA': RUNTIME, 'REQUIREMENTS_PATH': 'requirements/proof.lock',
               'LOCK_SHA': 'd' * 64}
        command = shell_functions + '\nretain_stage_stderr "$SOURCE" install-agent\n'
        result = subprocess.run(['bash', '-u', '-o', 'pipefail', '-c', command],
                                env={**env, 'SOURCE': str(source)}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = fixture / 'tests/provision-stderr/venv-agent-child-guards.install-agent.stderr'
        source.write_bytes(b'foreign replacement\n')
        result = subprocess.run(['bash', '-u', '-o', 'pipefail', '-c', command],
                                env={**env, 'SOURCE': str(source)}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(evidence.read_bytes(), b'first private payload\n')

        source.write_bytes(b'x' * (1024 * 1024 + 17))
        result = subprocess.run(['bash', '-u', '-o', 'pipefail', '-c',
                                 command.replace('install-agent', 'large-stage')],
                                env={**env, 'SOURCE': str(source)}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        large = evidence.with_name('venv-agent-child-guards.large-stage.stderr')
        metadata = json.loads(large.with_suffix('.json').read_text())
        self.assertEqual(large.stat().st_size, 1024 * 1024)
        self.assertEqual(metadata['original_bytes'], 1024 * 1024 + 17)
        self.assertEqual(metadata['retained_bytes'], 1024 * 1024)
        self.assertTrue(metadata['truncated'])
        self.assertEqual(metadata['sha256'], hashlib.sha256(source.read_bytes()).hexdigest())

        forged = fixture / 'forged'
        forged.write_bytes(b'outside\n')
        target = evidence.with_name('venv-agent-child-guards.forged.stderr')
        target.symlink_to(forged)
        result = subprocess.run(['bash', '-u', '-o', 'pipefail', '-c', command.replace('install-agent', 'forged')],
                                env={**env, 'SOURCE': str(source)}, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(forged.read_bytes(), b'outside\n')

        hardlink_target = evidence.with_name('venv-agent-child-guards.hardlink.stderr')
        hardlink_target.hardlink_to(forged)
        result = subprocess.run(['bash', '-u', '-o', 'pipefail', '-c',
                                 command.replace('install-agent', 'hardlink')],
                                env={**env, 'SOURCE': str(source)}, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(forged.read_bytes(), b'outside\n')
        result = subprocess.run(['bash', '-u', '-o', 'pipefail', '-c',
                                 command.replace('install-agent', 'bad_stage')],
                                env={**env, 'SOURCE': str(source)}, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_real_source_state_requires_exact_clean_checkout(self):
        text = MAKER.read_text()
        function = text[text.index('source_state() {'):text.index('\nsource_state "$A" "$S"')]
        for head, status, accepted in ((AGENT, '', True), ('0' * 40, '', False),
                                       (AGENT, '?? foreign-file', False)):
            env = {**os.environ, 'FIXTURE_HEAD': head, 'FIXTURE_STATUS': status,
                   'FIXTURE_WANTED': AGENT}
            prefix = '''git() {
  test "$1" = -C && test "$2" = /fixture/agent || return 2
  case "$3" in
    rev-parse) printf '%s\\n' "$FIXTURE_HEAD" ;;
    status) printf '%s' "$FIXTURE_STATUS" ;;
    *) return 2 ;;
  esac
}
'''
            result = subprocess.run(['bash', '-c', prefix + function +
                                     '\nsource_state /fixture/agent "$FIXTURE_WANTED"'],
                                    env=env, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode == 0, accepted)

    def test_parent_census_lists_all_generated_paths_in_one_read_only_walk(self):
        fixture = Layout(kind='directory')
        inventory = fixture.verify()
        target, _ = caller_sources(PARENT.read_text(), fixture)
        for role in ('agent', 'runtime'):
            shutil.copytree(target / '.child-venv-source-caller' / role,
                            fixture.snapshot / role, dirs_exist_ok=True)
        before = {p.relative_to(fixture.root).as_posix(): (p.lstat(), p.read_bytes() if p.is_file() else None)
                  for p in fixture.root.rglob('*')}
        refused = source_census(fixture, inventory)
        self.assertEqual({row['path'] for row in refused}, {
            f'{fixture.snapshot.name}/{role}/{rel}' for role in ('agent', 'runtime')
            for rel in ('build', 'build/lib', 'build/lib/generated.py',
                        'fixture.egg-info', 'fixture.egg-info/PKG-INFO')})
        self.assertEqual(len(refused), 10)
        for p in fixture.root.rglob('*'):
            info, data = before[p.relative_to(fixture.root).as_posix()]
            after = p.lstat()
            self.assertEqual((info.st_ino, info.st_mode, info.st_uid, info.st_nlink, info.st_mtime_ns),
                             (after.st_ino, after.st_mode, after.st_uid, after.st_nlink, after.st_mtime_ns))
            if data is not None:
                self.assertEqual(p.read_bytes(), data)

    def test_exact_parent_red_candidate_green_through_real_build_and_verifier(self):
        for maker, accepted in ((PARENT, False), (MAKER, True)):
            with self.subTest(maker=maker.name):
                fixture = Layout(kind='archive' if accepted else 'directory')
                target, calls = caller_sources(maker.read_text(), fixture)
                for role in ('agent', 'runtime'):
                    shutil.copytree(target / '.child-venv-source-caller' / role,
                                    fixture.snapshot / role, dirs_exist_ok=True)
                if accepted:
                    inventory = fixture.verify(maker.read_text())
                    for role in ('agent', 'runtime'):
                        self.assertIn(f'.source-inputs/{role}.tar', inventory['__root__'])
                        self.assertEqual((target / '.source-inputs' / (role + '.tar')).read_bytes(),
                                         fixture.archives[role])
                        self.assertIn(f'install-{role} {target}/.source-inputs/{role}.tar\n', calls)
                else:
                    with self.assertRaisesRegex(SystemExit, 'unowned retained source directory'):
                        fixture.verify(maker.read_text())

    def test_seeded_caller_keeps_supported_archive_route(self):
        for maker in (PARENT, MAKER):
            with self.subTest(maker=maker.name):
                fixture = Layout()
                target, calls = caller_sources(maker.read_text(), fixture, seeded=True)
                for role in ('agent', 'runtime'):
                    self.assertIn(f'install-{role} {target}/.source-inputs/{role}.tar\n', calls)
                    self.assertEqual((target / '.source-inputs' / (role + '.tar')).read_bytes(),
                                     fixture.archives[role])
                    self.assertFalse((target / '.child-venv-source-caller' / role / 'build').exists())

    def test_verifier_and_outer_production_caller_are_byte_exact(self):
        before, after = PARENT.read_text(), MAKER.read_text()
        self.assertEqual(block(before, 'STORE_VERIFY'), block(after, 'STORE_VERIFY'))
        self.assertEqual(store_python(before), store_python(after))
        self.assertIn("store.ensure('child', identity, registration, build, verify, seal=seal,", after)
        self.assertIn("source_state \"$A\" \"$S\"", after)

    def test_every_embedded_python_compiles_in_memory(self):
        text = MAKER.read_text()
        blocks = {'STORE_PY': store_python(text), 'STORE_VERIFY': block(text, 'STORE_VERIFY')}
        for name in ('STAGING_INVENTORY', 'RELOCATE'):
            blocks[name] = text.split("<<'" + name + "'\n", 1)[1].split('\n' + name + '\n', 1)[0]
        for name, code in re.findall(r"(?m)^(\w+_SCRIPT)='(.*?)'\nrun_stage", text, re.S):
            blocks[name] = code
        self.assertEqual(set(blocks), {'STORE_PY', 'STORE_VERIFY', 'STAGING_INVENTORY', 'RELOCATE',
                                      'PROVENANCE_SCRIPT', 'DIST_METADATA_SCRIPT', 'IDENTITY_SCRIPT'})
        for name, code in blocks.items():
            compile(code, name, 'exec')


class VerifierTests(unittest.TestCase):
    def test_missing_committed_source_file_is_refused(self):
        for role in ('agent', 'runtime'):
            fixture = Layout()
            path = fixture.snapshot / role / 'docs/deep/nested/readme.txt'
            path.rename(fixture.base / 'withheld-committed-file')
            with self.assertRaisesRegex(SystemExit, 'retained source differs from requested commit'):
                fixture.verify()

    def test_symlink_replacement_of_each_complete_source_ancestor_refuses(self):
        for role in ('agent', 'runtime'):
            for rel in ('', role, role + '/docs', role + '/docs/deep', role + '/docs/deep/nested'):
                with self.subTest(role=role, rel=rel):
                    fixture = Layout()
                    path = fixture.snapshot / rel
                    outside = fixture.base / 'displaced'
                    path.rename(outside)
                    path.symlink_to(outside, target_is_directory=True)
                    with self.assertRaisesRegex(SystemExit, 'unsafe or writable retained path'):
                        fixture.verify()

    def test_symlink_replacement_of_carrier_and_metadata_refuses(self):
        for rel in ('.source-inputs', '.source-inputs/agent.tar',
                    'lib/python3.13/site-packages/astrid-0.1.0.dist-info',
                    'lib/python3.13/site-packages/astrid-0.1.0.dist-info/RECORD'):
            fixture = Layout()
            path = fixture.root / rel
            directory = path.is_dir()
            outside = fixture.base / 'displaced'
            path.rename(outside)
            path.symlink_to(outside, target_is_directory=directory)
            with self.assertRaisesRegex(SystemExit, 'unsafe or writable retained path'):
                fixture.verify()

    def test_extra_snapshot_and_editable_provenance_refuse(self):
        fixture = Layout()
        (fixture.root / '.child-venv-source-foreign').mkdir()
        with self.assertRaisesRegex(SystemExit, 'ambiguous retained source snapshot'):
            fixture.verify()
        fixture = Layout(kind='directory')
        path = fixture.dist_paths['agent'] / 'direct_url.json'
        direct = json.loads(path.read_text())
        direct['dir_info']['editable'] = True
        path.write_text(json.dumps(direct))
        fixture.refresh_record('agent')
        with self.assertRaisesRegex(SystemExit, 'source is not a noneditable directory install'):
            fixture.verify()

    def test_archive_ownership_and_complete_ancestry(self):
        fixture = Layout()
        inventory = fixture.verify()
        for role, files in fixture.files.items():
            for rel in files:
                self.assertIn(f'{fixture.snapshot.name}/{role}/{rel}', inventory['__root__'])
        fixture.seal()
        self.assertEqual(fixture.verify(staging=False), inventory)

    def test_supported_clean_directory_provenance_remains_accepted(self):
        self.assertIn('astrid', Layout(kind='directory').verify())

    def test_every_empty_generated_and_foreign_source_path_is_refused(self):
        for role in ('agent', 'runtime'):
            for relative, data in (('empty', None), ('build/lib', None),
                                   ('fixture.egg-info/PKG-INFO', b'generated'),
                                   ('docs/deep/nested/foreign.txt', b'foreign'),
                                   ('foreign/deep/empty', None)):
                with self.subTest(role=role, relative=relative):
                    fixture = Layout()
                    path = fixture.snapshot / role / relative
                    if data is None:
                        path.mkdir(parents=True)
                    else:
                        put(path, data)
                    with self.assertRaisesRegex(SystemExit, 'unowned retained source (directory|file)'):
                        fixture.verify()

    def test_source_bytes_missing_and_mismatched_are_refused(self):
        for role in ('agent', 'runtime'):
            fixture = Layout()
            (fixture.snapshot / role / 'docs/deep/nested/readme.txt').write_bytes(b'mismatched')
            with self.assertRaisesRegex(SystemExit, 'retained source differs from requested commit'):
                fixture.verify()

    def test_identity_marker_mismatch_is_refused(self):
        for marker in ('.astrid-source-commit', '.astrid-runtime-source-commit', '.astrid-runtime-client-identity'):
            fixture = Layout()
            (fixture.root / marker).write_text('foreign identity\n')
            with self.assertRaisesRegex(SystemExit, 'retained source/client marker differs'):
                fixture.verify()

    def test_commit_argument_mismatch_never_reads_near_match(self):
        fixture = Layout()
        with self.assertRaisesRegex(AssertionError, 'Unexpected source identity'):
            fixture.verify(argv_change=lambda argv: argv.__setitem__(4, '0' * 40))

    def test_unsupported_committed_symlink_is_refused(self):
        fixture = Layout()
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode='w') as stream:
            entry = tarfile.TarInfo('malicious-link')
            entry.type = tarfile.SYMTYPE
            entry.linkname = '/outside'
            stream.addfile(entry)
        fixture.archives['agent'] = output.getvalue()
        with self.assertRaisesRegex(SystemExit, 'unsupported committed source file'):
            fixture.verify()

    def test_archive_bytes_hash_and_location_are_authenticated(self):
        for change in ('bytes', 'hash', 'url'):
            fixture = Layout()
            direct_path = fixture.dist_paths['agent'] / 'direct_url.json'
            direct = json.loads(direct_path.read_text())
            if change == 'bytes':
                (fixture.root / '.source-inputs/agent.tar').write_bytes(b'foreign archive')
            elif change == 'hash':
                direct['archive_info']['hashes']['sha256'] = '0' * 64
            else:
                direct['url'] = (fixture.root / '.source-inputs/foreign.tar').as_uri()
            direct_path.write_text(json.dumps(direct))
            fixture.refresh_record('agent')
            with self.assertRaisesRegex(SystemExit, 'source archive differs from requested commit'):
                fixture.verify()

    def test_symlinks_at_every_source_ancestry_depth_and_archive_refuse(self):
        for rel in ('.child-venv-source-link', '.source-inputs/link.tar',
                    'agent/link', 'agent/docs/link', 'agent/docs/deep/nested/link'):
            fixture = Layout()
            outside = fixture.base / 'outside'
            outside.mkdir()
            path = fixture.root / rel if rel.startswith('.') else fixture.snapshot / rel
            path.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(SystemExit, 'unsafe or writable retained path'):
                fixture.verify()

    def test_source_hardlinks_and_foreign_owner_refuse(self):
        fixture = Layout()
        source = fixture.snapshot / 'agent/LICENSE'
        os.link(source, fixture.base / 'hardlink')
        with self.assertRaisesRegex(SystemExit, 'foreign or hardlinked retained path'):
            fixture.verify()
        fixture = Layout()
        actual = Path.lstat
        foreign = fixture.snapshot / 'runtime/LICENSE'

        def lstat(path, *args, **kwargs):
            info = actual(path, *args, **kwargs)
            if path == foreign:
                values = list(info)
                values[4] = os.getuid() + 1
                return os.stat_result(values)
            return info

        with patch.object(Path, 'lstat', lstat):
            with self.assertRaisesRegex(SystemExit, 'foreign or hardlinked retained path'):
                fixture.verify()

    def test_writable_final_refuses_and_exact_lib64_exception_remains(self):
        fixture = Layout()
        (fixture.root / 'lib64').symlink_to('lib', target_is_directory=True)
        fixture.verify()
        with self.assertRaisesRegex(SystemExit, 'unsafe or writable retained path'):
            fixture.verify(staging=False)

    def test_record_digest_and_unowned_record_additions_refuse(self):
        fixture = Layout()
        (fixture.site / 'astrid/__init__.py').write_bytes(b'changed')
        with self.assertRaisesRegex(SystemExit, 'RECORD bytes mismatch'):
            fixture.verify()
        for rel, message in (('foreign.txt', 'unowned local distribution RECORD addition'),
                             ('astrid-0.1.0.dist-info/foreign.txt', 'unowned local distribution metadata')):
            fixture = Layout()
            put(fixture.site / rel, b'foreign')
            fixture.refresh_record('agent', [record_row(rel, b'foreign')])
            with self.assertRaisesRegex(SystemExit, message):
                fixture.verify()

    def test_generated_metadata_license_ownership_stays_exact(self):
        fixture = Layout()
        license_path = fixture.dist_paths['agent'] / 'licenses/LICENSE'
        license_path.write_bytes(b'foreign license')
        fixture.refresh_record('agent')
        with self.assertRaisesRegex(SystemExit, 'unowned local distribution metadata'):
            fixture.verify()

    def test_distribution_name_and_import_provenance_refuse_mismatch(self):
        fixture = Layout()
        metadata = fixture.dist_paths['agent'] / 'METADATA'
        metadata.write_text(metadata.read_text().replace('0.1.0', '0.2.0'))
        with self.assertRaisesRegex(SystemExit, 'distribution name/version mismatch'):
            fixture.verify()
        fixture = Layout()
        (fixture.root / '.astrid-import-origins').write_text('astrid=/outside/__init__.py\n')
        with self.assertRaisesRegex(SystemExit, 'import origin mismatch'):
            fixture.verify()


class RetentionLifecycleTests(unittest.TestCase):
    def fixture(self):
        module = store_module()
        base = scratch()
        tests = base / 'tests'
        tests.mkdir()
        store = module.Store.initialize(base / 'store', tests)
        namespace = dict(
            hashlib=hashlib, json=json, os=os, pathlib=__import__('pathlib'),
            re=re, stat=stat, subprocess=subprocess, module=module, store=store,
            root=str(store.root), tests=str(tests), name='venv-agent-child-custody',
            identity={'agent_sha': AGENT, 'backend_sha': RUNTIME, 'client_tuple': {'client': '0' * 64}},
            checkout='/fixture/agent', agent=AGENT, runtime_checkout='/fixture/runtime', backend=RUNTIME,
            requirements='requirements/proof.lock', lock='0' * 64, client='client=' + '0' * 64,
            source=MAKER.read_text(), verifier=block(MAKER.read_text(), 'STORE_VERIFY'),
            helper=str(ORCH / 'bin/bench_store.py'), verify_invocation=[],
        )
        functions(MAKER.read_text(), ['diagnostic_retention'], namespace)
        return module, store, namespace

    def test_success_failure_cancellation_and_seal_failure_keep_stage_only(self):
        for outcome in ('success', 'failure', 'cancel', 'seal-failure'):
            with self.subTest(outcome=outcome):
                module, store, ns = self.fixture()
                before = (store.root / 'index.json').read_bytes()
                calls = []

                def build(stage, final):
                    calls.append('build')
                    (stage / 'fixture').write_text('fixture')
                    if outcome == 'cancel':
                        raise KeyboardInterrupt()

                def verify(stage):
                    calls.append('verify')
                    if outcome == 'failure':
                        raise RuntimeError('unowned retained source directory')

                def seal(stage):
                    calls.append('seal')
                    if outcome == 'seal-failure':
                        raise RuntimeError('fixture seal refusal')
                    for path in [*stage.rglob('*'), stage]:
                        path.chmod(path.stat().st_mode & ~0o222)

                ns.update(build=build, verify=verify, seal=seal)
                disk = Mock(free=module.Store.RESERVE_BYTES)
                with patch.object(module.shutil, 'disk_usage', return_value=disk):
                    if outcome == 'success':
                        ns['diagnostic_retention']()
                    else:
                        with self.assertRaisesRegex(RuntimeError, 'diagnostic retention'):
                            ns['diagnostic_retention']()
                receipts = list((store.root / 'staging').glob('*.diagnostic-retention.json'))
                self.assertEqual(len(receipts), 1)
                receipt = json.loads(receipts[0].read_text())
                expected = {'success': 'verified-staging', 'failure': 'failed-staging',
                            'cancel': 'cancelled-staging', 'seal-failure': 'refused'}[outcome]
                self.assertEqual(receipt['status'], expected)
                self.assertTrue(receipt['authority']['index_unchanged'])
                self.assertTrue(all(value is False for value in receipt['barriers'].values()))
                self.assertEqual((store.root / 'index.json').read_bytes(), before)
                self.assertEqual(list((store.root / 'entries').iterdir()), [])
                self.assertFalse(store.journal.exists())
                self.assertEqual(calls[-1], 'seal')
                self.assertEqual(calls[:2], ['build', 'seal'] if outcome == 'cancel' else ['build', 'verify'])

    def test_diagnostic_reserve_refuses_before_build(self):
        module, store, ns = self.fixture()
        ns.update(build=Mock(), verify=Mock(), seal=Mock())
        with patch.object(module.shutil, 'disk_usage', return_value=Mock(free=module.Store.RESERVE_BYTES - 1)):
            with self.assertRaisesRegex(module.Refused, 'free-space reserve unavailable'):
                ns['diagnostic_retention']()
        ns['build'].assert_not_called()
        self.assertEqual(list((store.root / 'staging').iterdir()), [])

    def test_real_verify_function_uses_exact_embedded_verifier_staging_argv(self):
        fixture = Layout()
        interpreter = fixture.root / 'bin/python'
        interpreter.chmod(0o755)
        ns = dict(pathlib=__import__('pathlib'), os=os, hashlib=hashlib, json=json,
                  subprocess=subprocess, identity={}, client=fixture.client,
                  checkout='/fixture/agent', agent=AGENT, runtime_checkout='/fixture/runtime',
                  backend=RUNTIME, work=str(fixture.base), python=str(fixture.interpreter),
                  requirements='requirements/proof.lock',
                  lock=hashlib.sha256(fixture.files['agent']['requirements/proof.lock']).hexdigest(),
                  dependency_seed='', source=MAKER.read_text(),
                  verifier=block(MAKER.read_text(), 'STORE_VERIFY'), verified_reports={})
        functions(MAKER.read_text(), ['verify', 'report_bytes'], ns)
        expected = ['python3', '-I', '-', str(fixture.root), fixture.client, '/fixture/agent', AGENT,
                    '/fixture/runtime', RUNTIME, str(fixture.base), str(fixture.interpreter), '--staging']

        def run_verifier(argv, input, text):
            self.assertEqual(argv, expected)
            self.assertEqual(input, block(MAKER.read_text(), 'STORE_VERIFY'))
            return json.dumps(fixture.verify())

        with patch('subprocess.check_output', side_effect=run_verifier), patch('subprocess.run') as child:
            # Nested verifier's Git boundary is independently bound by Layout.verify.
            ns['verify'](fixture.root)
        self.assertEqual(ns['verify_invocation'], expected)
        self.assertEqual(child.call_args.args[0][0], str(interpreter))
        self.assertIn(str(fixture.root), ns['verified_reports'])

    def test_normal_dispatch_keeps_store_ensure_and_diagnostic_has_no_registration(self):
        tree = ast.parse(store_python(MAKER.read_text()))
        dispatch = next(node for node in tree.body if isinstance(node, ast.Try))
        for diagnostic in (False, True):
            store = Mock()
            entry = {'path': '/fixture/final'}
            store.ensure.return_value = entry
            ns = dict(store=store, diagnostic_mode=diagnostic, identity={}, registration=Mock(),
                      build=Mock(), verify=Mock(), seal=Mock(), name='venv-agent-child-custody',
                      verified_reports={'/fixture/final': b'report'}, success_receipt=Mock(return_value='ok'),
                      diagnostic_retention=Mock(return_value='retained'))
            exec(compile(ast.Module(body=[dispatch], type_ignores=[]), '<real dispatch>', 'exec'), ns)
            if diagnostic:
                store.ensure.assert_not_called()
                ns['registration'].assert_not_called()
                ns['diagnostic_retention'].assert_called_once_with()
            else:
                store.ensure.assert_called_once_with('child', ns['identity'], ns['registration'],
                                                     ns['build'], ns['verify'], seal=ns['seal'],
                                                     failure_name=ns['name'])

    def test_bad_unknown_duplicate_and_missing_option_arguments_refuse(self):
        for options in (['--unknown'], ['--retain-staging-no-register', '--retain-staging-no-register'],
                        ['--source-carrier'], ['--dependency-wheelhouse']):
            result = subprocess.run(['bash', str(MAKER), 'venv-agent-child-custody', AGENT, *options],
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 2)
            self.assertIn('REFUSED:', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
