"""Prepare and run a whole-make test for a private tiny-package venue.

Preparation initializes only two disposable fixture Stores through the normal
Store API; it never writes Git, changes admission, mocks a command, or
substitutes a verifier. Missing venue inputs are a blocked result. The manager
commits fixture_sources() through its normal harness. Stores and orchestration
must live in this run's TMPDIR.
"""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys

from support import MAKER, PORTABLE_PARENT, block

PARENT_COMMIT = '9428f515fcd8dccaef26193438b3ac89f903f5aa'
PARENT_SHA256 = '0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39'
HELPER_SHA256 = '123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2'
MAKER_SHA256 = 'c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e'
PARENT_MAKER_SHA256 = '0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39'
RESERVE = 5905580032
STOP_LINE = 4000000000
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / 'e2e-fixtures/tiny'
FIXTURE_MANIFEST = FIXTURE_ROOT / 'manifest.json'
DEFAULT_RUNNER_PYTHON = Path('/home/user/work/venv-agent/bin/python')
DEFAULT_CHILD_PYTHON = Path('/usr/bin/python3.13')
DEFAULT_BOOTSTRAP_ARTIFACT = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz')
BOOTSTRAP_ARTIFACT_SHA256 = '443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548'
BOOTSTRAP_WHEELS = {
    'pip-26.2.1-py3-none-any.whl': '71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e',
    'setuptools-80.9.0-py3-none-any.whl': '062d34222ad13e0cc312a4c02d73f059e86a4acbfbdea8f8f76b28c99f306922',
    'wheel-0.46.3-py3-none-any.whl': '4b399d56c9d9338230118d705d9737a2a468ccca63d5e813e2a4fc7815d8bc4d',
}
REQUIRED_COMMANDS = ('bash', 'git', 'tar', 'mktemp', 'sha256sum', 'cut', 'grep',
                     'sed', 'find', 'chmod', 'mv', 'df', 'awk', 'timeout', 'readlink')


def fixture_sources():
    manifest = json.loads(FIXTURE_MANIFEST.read_text())
    require(manifest.get('schema') == 'timeline.ops-child-custody.tiny-source.v1',
            'tiny fixture source manifest schema mismatch')
    result = {}
    for role, entry in manifest['roles'].items():
        files = {}
        for name, expected in entry['files'].items():
            path = FIXTURE_ROOT / role / name
            require(path.is_file() and not path.is_symlink(), 'missing tiny fixture source: ' + role + '/' + name)
            data = path.read_bytes()
            require(hashlib.sha256(data).hexdigest() == expected,
                    'tiny fixture source hash mismatch: ' + role + '/' + name)
            files[name] = data.decode('utf-8')
        result[role] = files
    return result


def fixture_makers():
    manifest = json.loads(FIXTURE_MANIFEST.read_text())
    result = {}
    for role, entry in manifest['makers'].items():
        path = FIXTURE_ROOT / entry['path']
        require(path.is_file() and not path.is_symlink(), 'missing tiny maker: ' + role)
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == entry['sha256'],
                'tiny maker hash mismatch: ' + role)
        require(stat.S_IMODE(path.stat().st_mode) == int(entry['mode'], 8),
                'tiny maker mode mismatch: ' + role)
        result[role] = {'path': path, 'bytes': data, 'sha256': entry['sha256'],
                        'commit': entry['commit']}
    return result


def fixture_wheel_pins():
    manifest = json.loads(FIXTURE_MANIFEST.read_text())
    pins = dict(BOOTSTRAP_WHEELS)
    for role in ('dependency-dot', 'dependency-underscore'):
        wheel = manifest['roles'][role].get('wheel', {})
        require(re.fullmatch(r'[A-Za-z0-9_.-]+\.whl', wheel.get('filename', '')),
                'tiny dependency wheel filename pin missing')
        require(re.fullmatch(r'[0-9a-f]{64}', wheel.get('sha256', '')),
                'tiny dependency wheel hash pin missing')
        pins[wheel['filename']] = wheel['sha256']
    return pins


def command(argv, **kwargs):
    return subprocess.run(argv, capture_output=True, text=True, timeout=600, **kwargs)


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def parse_df_available(text):
    """Parse exactly one POSIX ``df -Pk`` data row without accepting headers."""
    rows = [line.split() for line in text.splitlines() if line.strip()]
    require(len(rows) == 2 and 'Available' in rows[0],
            'df output must contain one header and one data row')
    require(len(rows[1]) >= 4 and re.fullmatch(r'[0-9]+', rows[1][3]),
            'df Available field must be a non-negative integer')
    return int(rows[1][3]) * 1024


def df_free_bytes(path):
    result = command(['/usr/bin/df', '-Pk', str(path)])
    require(result.returncode == 0, 'df failed for fixture target')
    return parse_df_available(result.stdout)


def python_facts(path, need_build):
    code = (
        'import importlib, importlib.metadata, json, sys, venv, ensurepip, fcntl, unittest.mock\n'
        'facts = {"version": sys.version, "executable": sys.executable}\n'
        'for name in ("setuptools", "wheel"):\n'
        '    facts[name] = importlib.metadata.version(name)\n'
        'if NEED_BUILD:\n'
        '    facts["build"] = importlib.metadata.version("build")\n'
        'print(json.dumps(facts, sort_keys=True))\n'
    ).replace('NEED_BUILD', repr(need_build))
    try:
        result = command([str(path), '-I', '-c', code])
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode:
        return None
    try:
        return json.loads(result.stdout)
    except (TypeError, ValueError):
        return None


def check_only(args):
    """Enumerate every target prerequisite without Git/Store/maker mutation."""
    missing = []
    checked = []

    def check(label, condition):
        checked.append(label)
        if not condition:
            missing.append(label)

    scratch_value = os.environ.get('TMPDIR', '')
    scratch = Path(scratch_value)
    check('TMPDIR is an existing physical absolute directory',
          scratch.is_absolute() and scratch == scratch.resolve() and scratch.is_dir())
    check('fixture manifest is a regular non-symlink file',
          FIXTURE_MANIFEST.is_file() and not FIXTURE_MANIFEST.is_symlink())
    manifest = None
    try:
        manifest = json.loads(FIXTURE_MANIFEST.read_text())
    except (OSError, ValueError):
        pass
    check('fixture manifest is valid JSON with expected schema',
          isinstance(manifest, dict) and manifest.get('schema') == 'timeline.ops-child-custody.tiny-source.v1')

    if isinstance(manifest, dict):
        for role, entry in manifest.get('roles', {}).items():
            for name, expected in entry.get('files', {}).items():
                path = FIXTURE_ROOT / role / name
                try:
                    matches = (path.is_file() and not path.is_symlink()
                               and hashlib.sha256(path.read_bytes()).hexdigest() == expected
                               and stat.S_IMODE(path.stat().st_mode) == 0o644)
                except OSError:
                    matches = False
                check('fixture source ' + role + '/' + name, matches)
        for role, entry in manifest.get('makers', {}).items():
            path = FIXTURE_ROOT / entry.get('path', '')
            try:
                matches = (path.is_file() and not path.is_symlink()
                           and hashlib.sha256(path.read_bytes()).hexdigest() == entry.get('sha256')
                           and stat.S_IMODE(path.stat().st_mode) == int(entry.get('mode', '0'), 8))
            except (OSError, ValueError):
                matches = False
            check('packaged ' + role + ' maker bytes and mode', matches)
    else:
        check('all fixture source and maker manifest entries are readable', False)

    for label, path in (('protected Store helper', args.helper),
                        ('private wheelhouse', args.wheelhouse),
                        ('Agent source carrier checkout', args.agent),
                        ('Runtime source carrier checkout', args.runtime)):
        candidate = Path(path) if path else Path('')
        check(label + ' is supplied as an absolute physical path',
              bool(path) and candidate.is_absolute() and candidate == candidate.resolve()
              and candidate.exists() and not candidate.is_symlink())
    if args.helper:
        helper = Path(args.helper)
        try:
            helper_matches = helper.is_file() and hashlib.sha256(helper.read_bytes()).hexdigest() == HELPER_SHA256
        except OSError:
            helper_matches = False
        check('protected Store helper hash', helper_matches)
    if args.wheelhouse:
        wheelhouse = Path(args.wheelhouse)
        try:
            pins = fixture_wheel_pins()
        except (OSError, KeyError, TypeError, ValueError, RuntimeError):
            pins = {}
            check('all local wheel pins are valid', False)
        for name, expected in pins.items():
            wheel = wheelhouse / name
            try:
                matches = wheel.is_file() and not wheel.is_symlink() and hashlib.sha256(wheel.read_bytes()).hexdigest() == expected
            except OSError:
                matches = False
            check('local wheel ' + name, matches)
    artifact = Path(args.bootstrap_artifact) if args.bootstrap_artifact else Path('')
    try:
        artifact_matches = (artifact.is_file() and not artifact.is_symlink()
                            and hashlib.sha256(artifact.read_bytes()).hexdigest() == BOOTSTRAP_ARTIFACT_SHA256)
    except OSError:
        artifact_matches = False
    check('local bootstrap artifact hash', artifact_matches)

    for label, path, needs_build in (('runner Agent Python', args.runner_python, True),
                                     ('offline build Python', args.build_python, True),
                                     ('child Python', args.python, False)):
        candidate = Path(path) if path else Path('')
        check(label + ' exists and is executable', bool(path) and candidate.is_file()
              and not candidate.is_symlink() and os.access(candidate, os.X_OK))
        facts = python_facts(candidate, needs_build) if candidate.is_file() else None
        check(label + ' reports Python 3.13 with required imports',
              facts is not None and facts.get('version', '').startswith('3.13.'))
        if needs_build:
            check(label + ' provides build, setuptools, and wheel',
                  facts is not None and facts.get('build') == '1.4.0'
                  and facts.get('setuptools') == '80.9.0' and facts.get('wheel') == '0.46.3')

    for name in REQUIRED_COMMANDS:
        check('required command ' + name, shutil.which(name) is not None)
    try:
        available = df_free_bytes(scratch if scratch.is_dir() else Path.cwd())
        check('free space is above unchanged start reserve', available >= RESERVE)
        check('free space is above unchanged 4GB stop line', available >= STOP_LINE)
    except (OSError, RuntimeError, ValueError):
        check('df output has one numeric Available field', False)

    for label, path in (('orchestration root', args.orch_root),
                        ('parent work root', args.parent_work),
                        ('candidate work root', args.candidate_work)):
        candidate = Path(path) if path else Path('')
        check(label + ' is a fresh path inside TMPDIR', bool(path) and candidate.is_absolute()
              and candidate == candidate.resolve() and candidate.is_relative_to(scratch)
              and not candidate.exists())

    for label, path in (('Agent source carrier checkout', args.agent),
                        ('Runtime source carrier checkout', args.runtime)):
        candidate = Path(path) if path else Path('')
        if candidate.is_dir():
            expected = fixture_sources().get('agent' if label.startswith('Agent') else 'runtime', {})
            head = command(['git', '-C', str(candidate), 'rev-parse', '--verify', 'HEAD^{commit}'])
            status = command(['git', '-C', str(candidate), 'status', '--porcelain', '--untracked-files=all'])
            names = command(['git', '-C', str(candidate), 'ls-tree', '-r', '--name-only', 'HEAD'])
            modes = command(['git', '-C', str(candidate), 'ls-tree', '-r', 'HEAD'])
            mode_map = {line.split('\t', 1)[1]: line.split()[0]
                        for line in modes.stdout.splitlines() if '\t' in line}
            check(label + ' has a clean receiving-service Git commit', head.returncode == 0 and status.returncode == 0
                  and status.stdout == '' and names.returncode == 0 and modes.returncode == 0
                  and set(names.stdout.splitlines()) == set(expected)
                  and all(mode_map.get(name) == '100644' for name in expected))
        else:
            check(label + ' Git history and exact committed source are readable', False)

    try:
        helper_text = Path(args.helper).read_text() if args.helper and Path(args.helper).is_file() else ''
    except OSError:
        helper_text = ''
    for label, needle in (('Store API initialize', 'Store.initialize'),
                          ('Store API ensure', 'def ensure'),
                          ('Store API registration', 'register')):
        check(label + ' is present in the protected helper', needle in helper_text)
    check('candidate and parent maker verifier blocks are byte-identical',
          PORTABLE_PARENT.is_file() and MAKER.is_file()
          and block(PORTABLE_PARENT.read_text(), 'STORE_VERIFY') == block(MAKER.read_text(), 'STORE_VERIFY'))

    if args.result:
        output = Path(args.result)
        check('check-only result path is inside TMPDIR', output.is_absolute() and output == output.resolve()
              and output.parent.is_relative_to(scratch) and output.parent.is_dir()
              and not output.exists())
    result = {'schema': 'timeline.ops-child-custody.check-only.v1', 'mode': 'check-only',
              'ok': not missing, 'checked': checked, 'missing': missing,
              'mutating_setup_started': False, 'maker_started': False,
              'store_initialized': False, 'git_mutated': False}
    if args.result and Path(args.result).parent.is_relative_to(scratch) and Path(args.result).parent.is_dir():
        Path(args.result).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if missing:
        for item in missing:
            print('MISSING: ' + item, file=sys.stderr)
        return 2
    print('check-only PASS')
    return 0


def physical(value):
    path = Path(value)
    require(path.is_absolute() and path == path.resolve() and path.exists(), 'missing/nonphysical fixture input')
    return path


def executable(value, label):
    path = Path(value)
    require(path.is_absolute() and path.exists() and path.is_file() and os.access(path, os.X_OK),
            'missing/non-executable ' + label)
    return path


def private_path(value, scratch, label):
    path = Path(value)
    require(path.is_absolute() and path == path.resolve() and path.is_relative_to(scratch),
            label + ' must be an absolute path in this TMPDIR')
    return path


def committed_fixture(path, expected):
    require(command(['git', '-C', str(path), 'status', '--porcelain', '--untracked-files=all']).stdout == '',
            'fixture source must be clean')
    head = command(['git', '-C', str(path), 'rev-parse', '--verify', 'HEAD^{commit}'])
    require(head.returncode == 0 and re.fullmatch('[0-9a-f]{40}\n', head.stdout), 'missing fixture source commit')
    names = command(['git', '-C', str(path), 'ls-tree', '-r', '--name-only', head.stdout.strip()])
    require(names.returncode == 0 and set(names.stdout.splitlines()) == set(expected), 'fixture source file set mismatch')
    for name, content in expected.items():
        require((path / name).read_bytes() == content.encode(), 'fixture source bytes mismatch: ' + name)
    return head.stdout.strip()


def verify_wheelhouse(path):
    path = physical(path)
    pins = fixture_wheel_pins()
    for name, expected in pins.items():
        wheel = path / name
        require(wheel.is_file() and not wheel.is_symlink(), 'missing pinned local wheel: ' + name)
        require(hashlib.sha256(wheel.read_bytes()).hexdigest() == expected,
                'local wheel hash mismatch: ' + name)
    return pins


def store_module(helper):
    spec = importlib.util.spec_from_file_location('tiny_fixture_bench_store', helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_wheels(destination, build_python):
    scratch = physical(os.environ['TMPDIR'])
    destination = private_path(destination, scratch, 'wheel output')
    require(not destination.exists(), 'wheel output already exists; use a fresh TMPDIR path')
    destination.mkdir(parents=True)
    source_root = destination / 'sources'
    source_root.mkdir()
    for role, files in fixture_sources().items():
        for name, content in files.items():
            target = source_root / role / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    build_python = executable(build_python, 'wheel build Python')
    for role in ('dependency-dot', 'dependency-underscore'):
        result = command([str(build_python), '-m', 'build', '--wheel', '--no-isolation',
                          '--outdir', str(destination), str(source_root / role)],
                         env={**os.environ, 'PIP_NO_INDEX': '1',
                              'PIP_DISABLE_PIP_VERSION_CHECK': '1',
                              'PIP_CONFIG_FILE': os.devnull, 'SOURCE_DATE_EPOCH': '0'})
        require(result.returncode == 0, 'offline tiny dependency wheel build failed: ' + role)
    produced = {'custody_b-0.1.0-py3-none-any.whl', 'custody_a-0.1.0-py3-none-any.whl'}
    require(all((destination / name).is_file() for name in produced),
            'offline tiny dependency build did not produce the pinned wheel names')
    manifest = {'schema': 'timeline.ops-child-custody.tiny-wheelhouse.v1',
                'wheels': {name: {'sha256': hashlib.sha256((destination / name).read_bytes()).hexdigest(),
                                  'bytes': (destination / name).stat().st_size}
                           for name in sorted(produced)}}
    (destination / 'wheel-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


def prepare_venue(args):
    scratch = physical(os.environ['TMPDIR'])
    manifest_path = private_path(args.prepare_venue, scratch, 'venue manifest')
    require(not manifest_path.exists(), 'venue manifest already exists; use a fresh TMPDIR path')
    helper = physical(args.helper)
    require(hashlib.sha256(helper.read_bytes()).hexdigest() == HELPER_SHA256,
            'protected Store helper mismatch')
    orch = private_path(args.orch_root, scratch, 'fixture orchestration root')
    require(not orch.exists(), 'fixture orchestration root already exists; use a fresh TMPDIR path')
    agent = physical(args.agent)
    runtime = physical(args.runtime)
    sources = fixture_sources()
    agent_sha = committed_fixture(agent, sources['agent'])
    runtime_sha = committed_fixture(runtime, sources['runtime'])
    wheelhouse = physical(args.wheelhouse)
    wheel_hashes = verify_wheelhouse(wheelhouse)
    bootstrap_artifact = physical(args.bootstrap_artifact)
    require(hashlib.sha256(bootstrap_artifact.read_bytes()).hexdigest() == BOOTSTRAP_ARTIFACT_SHA256,
            'bootstrap artifact hash mismatch')
    python = physical(args.python)
    require(hashlib.sha256(PORTABLE_PARENT.read_bytes()).hexdigest() == PARENT_MAKER_SHA256,
            'packaged parent maker mismatch')
    require(hashlib.sha256(MAKER.read_bytes()).hexdigest() == MAKER_SHA256,
            'packaged candidate maker mismatch')
    parent_work = private_path(args.parent_work, scratch, 'parent fixture work root')
    candidate_work = private_path(args.candidate_work, scratch, 'candidate fixture work root')
    require(parent_work != candidate_work, 'parent and candidate fixture work roots must differ')
    require(not parent_work.exists() and not candidate_work.exists(),
            'fixture work roots already exist; use fresh TMPDIR paths')
    orch.mkdir(parents=True)
    (orch / 'bin').mkdir()
    (orch / 'tests').mkdir()
    (orch / 'artifacts').mkdir()
    # Store.ensure verifies the receiving projection before invoking any maker
    # body.  This empty baseline is part of the private fixture venue, not a
    # production suite or admission change.
    (orch / 'tests' / 'suites.conf').write_text('')
    shutil.copyfile(bootstrap_artifact, orch / 'artifacts' / bootstrap_artifact.name)
    shutil.copyfile(helper, orch / 'bin/bench_store.py')
    (orch / 'bin/bench_store.py').chmod(0o755)
    parent_work.mkdir()
    candidate_work.mkdir()
    store = store_module(orch / 'bin/bench_store.py')
    store.Store.initialize(parent_work / 'bench-store', orch / 'tests')
    store.Store.initialize(candidate_work / 'bench-store', orch / 'tests')
    venue = {
        'schema': 'timeline.ops-child-custody.tiny-venue.v1',
        'fixture_kind': 'private-tiny-source-carrier',
        'prepared_by': 'e2e_inventory.py --prepare-venue',
        'orch': str(orch),
        'python': str(python),
        'wheelhouse': str(wheelhouse),
        'agent': str(agent),
        'agent_sha': agent_sha,
        'runtime': str(runtime),
        'runtime_sha': runtime_sha,
        'parent_work': str(parent_work),
        'candidate_work': str(candidate_work),
        'helper_sha256': HELPER_SHA256,
        'parent_maker_sha256': PARENT_MAKER_SHA256,
        'maker_sha256': MAKER_SHA256,
        'wheel_hashes': wheel_hashes,
        'bootstrap_artifact_name': bootstrap_artifact.name,
        'bootstrap_artifact_sha256': BOOTSTRAP_ARTIFACT_SHA256,
        'stores_initialized_by_worker': True,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(venue, indent=2) + '\n')
    print('prepared private tiny fixture venue: ' + str(manifest_path))


def run_venue(manifest, output):
    scratch = physical(os.environ['TMPDIR'])
    venue = json.loads(manifest.read_text())
    require(venue['schema'] == 'timeline.ops-child-custody.tiny-venue.v1'
            and venue['fixture_kind'] == 'private-tiny-source-carrier',
            'missing private tiny fixture venue manifest')
    require(venue.get('stores_initialized_by_worker') is True,
            'private fixture Stores were not initialized by the normal Store API')
    output['store_initialized_by_worker'] = True
    orch = physical(venue['orch'])
    require(orch.is_relative_to(scratch), 'fixture orchestration must be in this TMPDIR')
    helper = orch / 'bin/bench_store.py'
    require(hashlib.sha256(helper.read_bytes()).hexdigest() == venue['helper_sha256'] == HELPER_SHA256,
            'protected Store helper mismatch')
    require(hashlib.sha256(MAKER.read_bytes()).hexdigest() == venue['maker_sha256'] == MAKER_SHA256,
            'candidate maker source mismatch')
    require(hashlib.sha256(PORTABLE_PARENT.read_bytes()).hexdigest() == venue['parent_maker_sha256'] == PARENT_MAKER_SHA256,
            'parent maker source mismatch')
    require((orch / 'tests' / 'suites.conf').is_file()
            and (orch / 'tests' / 'suites.conf').read_bytes() == b'',
            'fixture Store projection baseline missing')
    python = physical(venue['python'])
    wheelhouse = physical(venue['wheelhouse'])
    bootstrap_artifact = orch / 'artifacts' / Path(venue.get('bootstrap_artifact_name', DEFAULT_BOOTSTRAP_ARTIFACT.name))
    require(bootstrap_artifact.is_file()
            and hashlib.sha256(bootstrap_artifact.read_bytes()).hexdigest() == venue['bootstrap_artifact_sha256'] == BOOTSTRAP_ARTIFACT_SHA256,
            'bootstrap artifact mismatch')
    require(venue['wheel_hashes'] == verify_wheelhouse(wheelhouse),
            'venue wheel pins differ from the actual local wheelhouse')
    agent = physical(venue['agent'])
    runtime = physical(venue['runtime'])
    agent_sha = committed_fixture(agent, fixture_sources()['agent'])
    runtime_sha = committed_fixture(runtime, fixture_sources()['runtime'])
    require(agent_sha == venue['agent_sha'] and runtime_sha == venue['runtime_sha'],
            'venue source commit differs from its prepared manifest')
    client = 'packages/python/astrid_runtime_client/__init__.py=' + hashlib.sha256(
        fixture_sources()['runtime']['packages/python/astrid_runtime_client/__init__.py'].encode()).hexdigest()
    parent = PORTABLE_PARENT.read_bytes()
    require(hashlib.sha256(parent).hexdigest() == PARENT_SHA256,
            'exact installed0857 parent unavailable')
    parent_path = scratch / 'inventory-parent-0857'
    require(not parent_path.exists(), 'parent fixture script already exists; no overwrite')
    parent_path.write_bytes(parent)
    parent_path.chmod(0o755)
    require(block(parent.decode(), 'STORE_VERIFY') == block(MAKER.read_text(), 'STORE_VERIFY'), 'verifier changed')
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PIP_NO_INDEX': '1',
           'PIP_FIND_LINKS': str(wheelhouse), 'PIP_CONFIG_FILE': os.devnull,
           'CHILD_VENV_ORCH_ROOT': str(orch), 'CHILD_VENV_PYTHON': str(python),
           'CHILD_VENV_BUILD_TIMEOUT_SECONDS': '600'}
    # A caller environment must not redirect a fixture to production inputs.
    for key in ('PIP_INDEX_URL', 'PIP_EXTRA_INDEX_URL', 'PYTHONPATH', 'PYTHONHOME'):
        env.pop(key, None)
    final = None
    for label, maker in (('parent', parent_path), ('candidate', MAKER)):
        work = physical(venue[label + '_work'])
        require(work.is_relative_to(scratch), 'fixture work root must be in this TMPDIR')
        require((work / 'bench-store/owner.json').is_file(), 'preinitialized approved fixture Store missing')
        require(df_free_bytes(work) >= max(RESERVE, 5000000000), 'unchanged production reserve unavailable')
        # Only an empty, single-use fixture Store is suitable; no adoption/reuse.
        store = store_module(helper).Store(work / 'bench-store', orch / 'tests')
        index = store._load()
        require(not index['entries'] and not index['registrations'], 'fixture Store must be unused')
        argv = ['bash', str(maker), 'venv-agent-child-inventory-' + label, agent_sha,
                '--source-carrier', str(agent), str(runtime), runtime_sha]
        result = command(argv, env={**env, 'CHILD_VENV_WORK_ROOT': str(work)})
        output['commands'].append({'label': label, 'argv': argv, 'exit_code': result.returncode})
        # Persist stage names only, never stderr/private bodies or arbitrary URLs.
        output[label + '_stages'] = re.findall(r'child-venv stage=([a-z0-9-]+) (start|complete)', result.stdout)
        require(df_free_bytes(work) >= STOP_LINE, '4GB stop line reached')
        if label == 'parent':
            require(result.returncode != 0 and 'maker provision report differs from authenticated installed inventory' in result.stderr,
                    'parent did not reach the expected inventory refusal')
            output['parent_red'] = True
        else:
            require(result.returncode == 0, 'candidate whole make refused; retained fixture requires safe census')
            index = json.loads((work / 'bench-store/index.json').read_text())
            require(len(index['entries']) == 1 and len(index['registrations']) == 1, 'missing genuine fixture registration')
            final = Path(next(iter(index['entries'].values()))['path'])
            require(final.is_relative_to(work / 'bench-store/entries'), 'fixture publication escaped Store')
            report = (final / '.provision-report').read_bytes()
            require((orch / 'tests/provision/venv-agent-child-inventory-candidate.txt').read_bytes() == report,
                    'registered report projection mismatch')
            output['candidate_green'] = True
            output['report_sha256'] = hashlib.sha256(report).hexdigest()
    verifier = block(MAKER.read_text(), 'STORE_VERIFY')
    argv = [sys.executable, '-B', '-I', '-', str(final), client, str(agent), agent_sha,
            str(runtime), runtime_sha, str(venue['candidate_work']), str(python)]

    def verify(expected=None):
        result = command(argv, input=verifier)
        if expected is None:
            require(result.returncode == 0, 'unchanged sealed verifier refused genuine installed fixture')
            return json.loads(result.stdout)
        require(result.returncode != 0 and expected in result.stderr, 'adversarial mismatch did not refuse at expected check')
        output['adversarial_checks'] += 1

    inventory = verify()
    require({'.provision-report', '.astrid-distribution-metadata'}.issubset(inventory['__root__']),
            'authenticated maker inventory missing')
    for name, reason in (('.provision-report', 'maker provision report differs'),
                         ('.astrid-distribution-metadata', 'maker distribution metadata differs'),
                         ('.astrid-source-commit', 'retained source/client marker differs'),
                         ('.astrid-runtime-source-commit', 'retained source/client marker differs'),
                         ('.astrid-runtime-client-identity', 'retained source/client marker differs')):
        path = final / name
        original, mode = path.read_bytes(), path.stat().st_mode & 0o777
        changes = []
        lines = original.splitlines(keepends=True)
        for ordinal in range(len(lines)):
            changed = lines.copy()
            changed[ordinal] = changed[ordinal].rstrip(b'\n') + b'-foreign\n'
            changes.append(b''.join(changed))
        changes.extend((original.rstrip(b'\n'), original + b'\n', b''.join(reversed(lines))))
        try:
            for changed in changes:
                if changed == original:
                    continue
                path.chmod(mode | 0o200)
                path.write_bytes(changed)
                path.chmod(mode)
                verify(reason)
        finally:
            path.chmod(mode | 0o200)
            path.write_bytes(original)
            path.chmod(mode)
    verify()
    output['whole_make_e2e'] = 'PASS'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-inputs', type=Path)
    parser.add_argument('--build-wheels', type=Path)
    parser.add_argument('--build-python', type=Path, default=DEFAULT_RUNNER_PYTHON)
    parser.add_argument('--runner-python', type=Path, default=DEFAULT_RUNNER_PYTHON)
    parser.add_argument('--bootstrap-artifact', type=Path, default=DEFAULT_BOOTSTRAP_ARTIFACT)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--prepare-venue', type=Path)
    parser.add_argument('--helper', type=Path)
    parser.add_argument('--orch-root', type=Path)
    parser.add_argument('--python', type=Path, default=DEFAULT_CHILD_PYTHON)
    parser.add_argument('--wheelhouse', type=Path)
    parser.add_argument('--agent', type=Path)
    parser.add_argument('--runtime', type=Path)
    parser.add_argument('--parent-work', type=Path)
    parser.add_argument('--candidate-work', type=Path)
    parser.add_argument('--venue-manifest', type=Path)
    parser.add_argument('--result', type=Path)
    args = parser.parse_args()
    if args.check_only:
        return check_only(args)
    if args.write_inputs:
        require(args.write_inputs.resolve().is_relative_to(Path(os.environ['TMPDIR']).resolve()), 'fixture inputs must be in TMPDIR')
        args.write_inputs.mkdir(parents=True)
        for role, files in fixture_sources().items():
            for name, content in files.items():
                path = args.write_inputs / role / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
        return 0
    if args.build_wheels:
        require(args.build_python is not None, '--build-python is required with --build-wheels')
        build_wheels(args.build_wheels, args.build_python)
        return 0
    if args.prepare_venue:
        required = (args.helper, args.orch_root, args.python, args.wheelhouse, args.agent, args.runtime,
                    args.parent_work, args.candidate_work)
        require(all(required), '--prepare-venue requires all private venue paths and source checkouts')
        prepare_venue(args)
        return 0
    require(args.result is not None, '--result required')
    output = {'whole_make_e2e': 'NOTRUN', 'parent_red': False, 'candidate_green': False,
              'adversarial_checks': 0, 'commands': [], 'verifier_mocked': False,
              'store_initialized_by_worker': False, 'admission_changed': False}
    try:
        require(args.venue_manifest is not None and args.venue_manifest.is_file(),
                'EXACTMISSING: private tiny fixture venue manifest, initialized Stores, committed tiny sources and local wheels')
        run_venue(args.venue_manifest, output)
    except RuntimeError as error:
        output['blocker'] = str(error)
        args.result.write_text(json.dumps(output, indent=2) + '\n')
        print(output['blocker'])
        return 2
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        output['blocker'] = 'fixture input/command failure: ' + type(error).__name__
        args.result.write_text(json.dumps(output, indent=2) + '\n')
        print(output['blocker'])
        return 2
    args.result.write_text(json.dumps(output, indent=2) + '\n')
    print('whole-make tiny-package E2E PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
