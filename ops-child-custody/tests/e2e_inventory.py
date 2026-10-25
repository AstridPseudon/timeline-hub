"""Whole-make test for an admitted, preinitialized, private tiny-package venue.

This program never initializes a Store, writes Git, changes admission, mocks a
command, or substitutes a verifier. Missing venue inputs are a blocked result.
The manager supplies two disposable fixture Stores and commits fixture_sources()
through its normal harness. They must live in this run's TMPDIR.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from support import MAKER, block

PARENT_COMMIT = '9428f515fcd8dccaef26193438b3ac89f903f5aa'
PARENT_SHA256 = '0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39'
HELPER_SHA256 = '123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2'
RESERVE = 5905580032


def fixture_sources():
    build = ('[build-system]\nrequires = ["setuptools==80.9.0", "wheel==0.46.3"]\n'
             'build-backend = "setuptools.build_meta"\n')

    def project(name, packages, scripts=''):
        return (build + f'[project]\nname = "{name}"\nversion = "0.1.0"\n' + scripts
                + '[tool.setuptools.packages.find]\ninclude = ' + json.dumps(packages) + '\n')

    client = 'CLIENT = "tiny-custody-contract"\n'
    return {
        'agent': {
            'pyproject.toml': project('astrid', ['astrid', 'astrid_runtime_client']),
            'LICENSE': 'Tiny private fixture license\n',
            'requirements/proof.lock': 'custody.B==0.1.0\ncustody_A==0.1.0\n',
            'astrid/__init__.py': 'VALUE = "tiny-agent"\n',
            'astrid_runtime_client/__init__.py': client,
        },
        'runtime': {
            'pyproject.toml': project('astrid-runtime', ['astrid_runtime', 'runtime_protocol'],
                                      '[project.scripts]\nastrid-runtime = "astrid_runtime:main"\n'
                                      'astrid-runtime-protocol = "runtime_protocol:main"\n'),
            'LICENSE': 'Tiny private fixture license\n',
            'astrid_runtime/__init__.py': 'def main():\n    return 0\n',
            'astrid_runtime/__main__.py': 'from . import main\nraise SystemExit(main())\n',
            'runtime_protocol/__init__.py': 'def main():\n    return 0\n',
            'packages/python/astrid_runtime_client/__init__.py': client,
        },
        'dependency-dot': {
            'pyproject.toml': project('custody.B', ['custody_b']),
            'custody_b/__init__.py': 'VALUE = "dot"\n',
        },
        'dependency-underscore': {
            'pyproject.toml': project('custody_A', ['custody_a']),
            'custody_a/__init__.py': 'VALUE = "underscore"\n',
        },
    }


def command(argv, **kwargs):
    return subprocess.run(argv, capture_output=True, text=True, timeout=600, **kwargs)


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def physical(value):
    path = Path(value)
    require(path.is_absolute() and path == path.resolve() and path.exists(), 'missing/nonphysical fixture input')
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


def run_venue(manifest, output):
    scratch = physical(os.environ['TMPDIR'])
    venue = json.loads(manifest.read_text())
    require(venue['approved_private_fixture'] is True, 'missing manager fixture admission')
    orch = physical(venue['orch'])
    require(orch.is_relative_to(scratch), 'fixture orchestration must be in this TMPDIR')
    helper = orch / 'bin/bench_store.py'
    require(hashlib.sha256(helper.read_bytes()).hexdigest() == HELPER_SHA256, 'protected Store helper mismatch')
    python = physical(venue['python'])
    wheelhouse = physical(venue['wheelhouse'])
    require(wheelhouse.is_dir(), 'missing already available local wheels')
    require(any(wheelhouse.glob('pip-26.2.1-*.whl'))
            and any(wheelhouse.glob('setuptools-80.9.0-*.whl'))
            and any(wheelhouse.glob('wheel-0.46.3-*.whl'))
            and any(wheelhouse.glob('custody_b-0.1.0-*.whl'))
            and any(wheelhouse.glob('custody_a-0.1.0-*.whl')),
            'missing supported bootstrap/private dependency wheels; no acquisition allowed')
    agent = physical(venue['agent'])
    runtime = physical(venue['runtime'])
    agent_sha = committed_fixture(agent, fixture_sources()['agent'])
    runtime_sha = committed_fixture(runtime, fixture_sources()['runtime'])
    client = 'packages/python/astrid_runtime_client/__init__.py=' + hashlib.sha256(
        fixture_sources()['runtime']['packages/python/astrid_runtime_client/__init__.py'].encode()).hexdigest()
    parent = command(['git', 'show', PARENT_COMMIT + ':ops-child-custody/make-child-venv'], cwd=MAKER.parents[1])
    require(parent.returncode == 0 and hashlib.sha256(parent.stdout.encode()).hexdigest() == PARENT_SHA256,
            'exact installed0857 parent unavailable')
    parent_path = scratch / 'inventory-parent-0857'
    require(not parent_path.exists(), 'parent fixture script already exists; no overwrite')
    parent_path.write_text(parent.stdout)
    require(block(parent.stdout, 'STORE_VERIFY') == block(MAKER.read_text(), 'STORE_VERIFY'), 'verifier changed')
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
        require(shutil.disk_usage(work).free >= max(RESERVE, 5000000000), 'unchanged production reserve unavailable')
        # Only an empty, single-use fixture Store is suitable; no adoption/reuse.
        index = json.loads((work / 'bench-store/index.json').read_text())
        require(not index['entries'] and not index['registrations'], 'fixture Store must be unused')
        argv = ['bash', str(maker), 'venv-agent-child-inventory-' + label, agent_sha,
                '--source-carrier', str(agent), str(runtime), runtime_sha]
        result = command(argv, env={**env, 'CHILD_VENV_WORK_ROOT': str(work)})
        output['commands'].append({'label': label, 'argv': argv, 'exit_code': result.returncode})
        # Persist stage names only, never stderr/private bodies or arbitrary URLs.
        output[label + '_stages'] = re.findall(r'child-venv stage=([a-z0-9-]+) (start|complete)', result.stdout)
        require(shutil.disk_usage(work).free >= 4000000000, '4GB stop line reached')
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
    parser.add_argument('--venue-manifest', type=Path)
    parser.add_argument('--result', type=Path)
    args = parser.parse_args()
    if args.write_inputs:
        require(args.write_inputs.resolve().is_relative_to(Path(os.environ['TMPDIR']).resolve()), 'fixture inputs must be in TMPDIR')
        args.write_inputs.mkdir()
        for role, files in fixture_sources().items():
            for name, content in files.items():
                path = args.write_inputs / role / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
        return 0
    require(args.result is not None, '--result required')
    output = {'whole_make_e2e': 'NOTRUN', 'parent_red': False, 'candidate_green': False,
              'adversarial_checks': 0, 'commands': [], 'verifier_mocked': False,
              'store_initialized_by_worker': False, 'admission_changed': False}
    try:
        require(args.venue_manifest is not None and args.venue_manifest.is_file(),
                'EXACTMISSING: approved private fixture venue manifest, Store custody, committed tiny sources and local wheels')
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
