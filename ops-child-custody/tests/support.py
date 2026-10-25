"""Small source-only fixtures; no package install, venv, Git mutation or body."""

import ast
import base64
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tarfile
import tempfile
from unittest.mock import patch

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
WORKER = ORCH / 'workers/rt-OPS-child-custody-resume-sol-1643'
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / 'e2e-fixtures/tiny'
MAKER = FIXTURE_ROOT / 'makers/candidate-c3226b/make-child-venv'
PARENT = WORKER / 'evidence/make-child-venv.preimage'
PORTABLE_PARENT = FIXTURE_ROOT / 'makers/parent-0857/make-child-venv'
AGENT = 'a4e016b6a9f91fbe372672bdcf382c630bf59186'
RUNTIME = '5e9ad1c6f74241d8771d3284fdd2ce7a214fd344'


def scratch():
    return Path(tempfile.mkdtemp(prefix='custody-', dir=os.environ['TMPDIR'])).resolve()


def block(text, name):
    return text.split('# ' + name + '_BEGIN\n', 1)[1].split('# ' + name + '_END', 1)[0]


def store_python(text):
    return text.split("<<'STORE_PY'\n", 1)[1].split('\nSTORE_PY\n', 1)[0]


def functions(text, names, namespace):
    tree = ast.parse(store_python(text))
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in selected} == set(names)
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<real STORE_PY functions>', 'exec'), namespace)


def store_module():
    spec = importlib.util.spec_from_file_location('custody_bench_store', ORCH / 'bin/bench_store.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def archive(files):
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode='w') as stream:
        for rel, data in files.items():
            entry = tarfile.TarInfo(rel)
            entry.size = len(data)
            entry.mode = 0o644
            stream.addfile(entry, io.BytesIO(data))
    return output.getvalue()


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def record_row(rel, data):
    return [rel, 'sha256=' + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip('='), str(len(data))]


def source_census(fixture, inventory):
    """One bounded read-only walk of a private fixture's entire source tree."""
    expected_files = {fixture.root / rel for rel in inventory['__root__']}
    expected_dirs = set().union(*(set(path.parents) for path in expected_files))
    paths = sorted(fixture.snapshot.rglob('*'))
    assert len(paths) < 1000
    refused = []
    for path in paths:
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            reason = 'unowned retained source directory' if path not in expected_dirs else None
        elif stat.S_ISREG(mode):
            reason = 'unowned retained source file' if path not in expected_files else None
        else:
            reason = 'unsafe or writable retained path'
        if reason:
            refused.append({'path': path.relative_to(fixture.root).as_posix(), 'reason': reason})
    return refused


class Layout:
    def __init__(self, kind='archive'):
        self.base = scratch()
        self.root = self.base / 'retained'
        self.root.mkdir()
        self.site = self.root / 'lib/python3.13/site-packages'
        self.site.mkdir(parents=True)
        self.snapshot = self.root / '.child-venv-source-venv-agent-child-custody'
        self.files = {}
        self.archives = {}
        self.dist_paths = {}
        self.kind = kind
        self.interpreter = self.base / 'maker-python'
        self.interpreter.write_bytes(b'private interpreter identity fixture\n')
        self.interpreter.chmod(0o755)
        put(self.root / 'bin/python', self.interpreter.read_bytes())
        self.client = 'packages/python/astrid_runtime_client/__init__.py=' + hashlib.sha256(b'CLIENT = 1\n').hexdigest()
        for name, role, packages in (
            ('astrid', 'agent', ('astrid', 'astrid_runtime_client')),
            ('astrid-runtime', 'runtime', ('astrid_runtime', 'runtime_protocol')),
        ):
            config = (f'[project]\nname = "{name}"\nversion = "0.1.0"\n'
                      '[tool.setuptools.packages.find]\ninclude = ' + json.dumps(list(packages)) + '\n')
            files = {'pyproject.toml': config.encode(), 'LICENSE': b'private license\n',
                     'requirements/proof.lock': b'fixture==1\n'}
            for package in packages:
                files[package + '/__init__.py'] = b'CLIENT = 1\n' if package == 'astrid_runtime_client' else b'VALUE = 1\n'
            # Several depths ensure every manifest-implied directory is exercised.
            files['docs/deep/nested/readme.txt'] = b'committed source data\n'
            self.files[role] = files
            self.archives[role] = archive(files)
            for rel, data in files.items():
                put(self.snapshot / role / rel, data)
            self.install(name, role, packages)
        for rel, data in (('.astrid-source-commit', AGENT), ('.astrid-runtime-source-commit', RUNTIME),
                          ('.astrid-runtime-client-identity', self.client)):
            put(self.root / rel, (data + '\n').encode())
        self.refresh_reports()

    def install(self, name, role, packages):
        dist = self.site / (name.replace('-', '_') + '-0.1.0.dist-info')
        self.dist_paths[role] = dist
        files = self.files[role]
        if self.kind == 'archive':
            carrier = self.root / '.source-inputs' / (role + '.tar')
            put(carrier, self.archives[role])
            direct = {'url': carrier.as_uri(), 'archive_info': {'hashes': {'sha256': hashlib.sha256(self.archives[role]).hexdigest()}}}
        else:
            direct = {'url': (self.snapshot / role).as_uri(), 'dir_info': {}}
        installed = {rel: data for rel, data in files.items() if rel.split('/')[0] in packages}
        installed.update({
            dist.name + '/METADATA': f'Metadata-Version: 2.4\nName: {name}\nVersion: 0.1.0\n'.encode(),
            dist.name + '/WHEEL': b'Wheel-Version: 1.0\n',
            dist.name + '/INSTALLER': b'pip\n',
            dist.name + '/REQUESTED': b'',
            dist.name + '/direct_url.json': json.dumps(direct).encode(),
            dist.name + '/licenses/LICENSE': files['LICENSE'],
        })
        for rel, data in installed.items():
            put(self.site / rel, data)
        rows = [record_row(rel, data) for rel, data in installed.items()]
        rows.append([dist.name + '/RECORD', '', ''])
        with (dist / 'RECORD').open('w') as output:
            csv.writer(output).writerows(rows)

    def refresh_record(self, role, extra=()):
        dist = self.dist_paths[role]
        rows = list(csv.reader(io.StringIO((dist / 'RECORD').read_text())))
        for row in rows:
            if row[1]:
                row[:] = record_row(row[0], (self.site / row[0]).read_bytes())
        rows.extend(extra)
        with (dist / 'RECORD').open('w') as output:
            csv.writer(output).writerows(rows)

    def refresh_reports(self):
        origins = ''.join(f'{p}={self.site / p / "__init__.py"}\n' for p in ('astrid', 'astrid_runtime', 'runtime_protocol', 'astrid_runtime_client'))
        metadata = ''
        freeze = []
        for name, role in (('astrid', 'agent'), ('astrid-runtime', 'runtime')):
            direct = json.loads((self.dist_paths[role] / 'direct_url.json').read_text())
            url = direct['url']
            metadata += f'{name}_name={name}\n{name}_version=0.1.0\n{name}_direct_url={url}\n{name}_provenance={self.kind}\n'
            suffix = '#sha256=' + direct['archive_info']['hashes']['sha256'] if self.kind == 'archive' else ''
            freeze.append(f'{name} @ {url}{suffix}\n')
        put(self.root / '.astrid-import-origins', origins.encode())
        put(self.root / '.astrid-distribution-metadata', metadata.encode())
        report = (f'status=passed\nagent_sha={AGENT}\nruntime_sha={RUNTIME}\n'
                  + 'runtime_client_identity_sha256=' + hashlib.sha256(self.client.encode()).hexdigest() + '\n'
                  + 'requirements_path=requirements/proof.lock\nrequirements_lock_sha256=' + hashlib.sha256(self.files['agent']['requirements/proof.lock']).hexdigest() + '\n'
                  + 'installed_import_origins:\n' + origins + 'installed_distribution_metadata:\n' + metadata
                  + 'pip_freeze:\n' + ''.join(sorted(freeze)))
        put(self.root / '.provision-report', report.encode())

    def verify(self, text=None, staging=True, argv_change=None):
        argv = ['verifier', str(self.root), self.client, '/fixture/agent', AGENT,
                '/fixture/runtime', RUNTIME, str(self.base), str(self.interpreter)]
        if staging:
            argv.append('--staging')
        if argv_change:
            argv_change(argv)

        def git_output(args, **kwargs):
            for role, sha in (('agent', AGENT), ('runtime', RUNTIME)):
                if args in (['git', '-C', '/fixture/' + role, 'archive', sha],
                            ['git', '-C', '/fixture/' + role, 'archive', '--format=tar', sha]):
                    return self.archives[role]
            raise AssertionError('Unexpected source identity: ' + repr(args))

        output = io.StringIO()
        with patch.object(sys, 'argv', argv), patch('subprocess.check_output', side_effect=git_output), \
                contextlib.redirect_stdout(output):
            exec(compile(block(text or MAKER.read_text(), 'STORE_VERIFY'), '<real STORE_VERIFY>', 'exec'), {})
        return json.loads(output.getvalue())

    def seal(self):
        for path in [*self.root.rglob('*'), self.root]:
            path.chmod(stat.S_IMODE(path.stat().st_mode) & ~0o222)


def caller_sources(text, fixture, seeded=False):
    """Run the real source/install branch with Git and installer fixture boundaries.

    The installer double models in-place packaging writes. It never invokes pip.
    Every stage command and input is captured; the independent verifier below
    validates the entire resulting retained source tree.
    """
    base = fixture.base
    fixture_archives = base / 'git-inputs'
    fixture_archives.mkdir()
    for role in ('agent', 'runtime'):
        put(fixture_archives / (role + '.tar'), fixture.archives[role])
    runner = base / 'installer.py'
    runner.write_text('''import pathlib, sys, tarfile
path = pathlib.Path(sys.argv[-1])
if path.is_dir():
    (path / 'build/lib').mkdir(parents=True)
    (path / 'build/lib/generated.py').write_text('generated build output')
    (path / 'fixture.egg-info').mkdir()
    (path / 'fixture.egg-info/PKG-INFO').write_text('generated metadata')
else:
    with tarfile.open(path) as source:
        assert source.getmember('pyproject.toml').isfile()
''')
    # Copy only the branch under change, byte-exact from STORE_BUILD. No stage
    # selection is substituted within the producer's source/install branch.
    body = block(text, 'STORE_BUILD')
    body = body[body.index('AGENT_SRC='):body.index("printf '%s\\n' \"$S\"")]
    # Existing retained source copies are created by the actual archive stages.
    target = base / 'caller'
    target.mkdir()
    env = {**os.environ, 'T': str(target), 'SRC': str(target / '.child-venv-source-caller'),
           'A': '/fixture/agent', 'R': '/fixture/runtime', 'S': AGENT, 'RUNTIME_SHA': RUNTIME,
           'DEPENDENCY_SEED': 'fixture' if seeded else '', 'FARM_REQUIRED': '0',
           'LOCAL_TIMEOUT_SECONDS': '30', 'PIP_TIMEOUT_SECONDS': '30',
           'P': sys.executable, 'INSTALLER': str(runner), 'FIXTURE_ARCHIVES': str(fixture_archives),
           'CALL_LOG': str(base / 'calls.txt')}
    prefix = '''set -euo pipefail
PIP_ARGS=()
git() {
  role=${2##*/}
  test "$3" = archive
  wanted=$S
  if [ "$role" = runtime ]; then wanted=$RUNTIME_SHA; fi
  test "${@: -1}" = "$wanted"
  if [ "$#" = 4 ]; then cat "$FIXTURE_ARCHIVES/$role.tar";
  else cp "$FIXTURE_ARCHIVES/$role.tar" "${5#--output=}"; fi
}
export -f git
run_stage() {
  stage=$1; shift 2
  printf '%s %s\\n' "$stage" "${@: -1}" >> "$CALL_LOG"
  case "$stage" in
    install-agent|install-runtime) "$P" "$INSTALLER" "$@" ;;
    *) "$@" ;;
  esac
}
'''
    subprocess.run(['bash', '-c', prefix + body], env=env, check=True, capture_output=True, text=True, timeout=30)
    return target, (base / 'calls.txt').read_text()
