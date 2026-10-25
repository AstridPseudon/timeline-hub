import importlib.util
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parents[1]
STORE_SOURCE = ROOT / 'bench_store.py'
RETIRE_SOURCE = ROOT / 'retire-child-venv'


def load_store():
    spec = importlib.util.spec_from_file_location('d139_bench_store', STORE_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STORE = load_store()


def fixture_root():
    base = Path(tempfile.mkdtemp(prefix='d139-retirement-', dir=os.environ.get('TMPDIR')))
    work = base / 'work'
    work.mkdir()
    tests = base / 'orch' / 'tests'
    (tests / 'provision').parent.mkdir(parents=True)
    (tests / 'suites.conf').write_text('', encoding='utf-8')
    (base / 'orch' / 'queue' / 'pending').mkdir(parents=True)
    (base / 'orch' / 'queue' / 'done').mkdir()
    (base / 'orch' / 'workers').mkdir()
    store = STORE.Store.initialize(work / 'bench-store', tests)
    return base, work, tests, store


def identity(suffix):
    return {
        'agent_sha': (suffix * 40)[:40],
        'backend_sha': (chr(ord(suffix) + 1) * 40)[:40],
        'client_tuple': {'client.py': (chr(ord(suffix) + 2) * 64)[:64]},
    }


def add_child(store, name, suffix, suite='', report=None):
    value = report or f'status=passed\nname={name}\n'

    def build(stage, _final):
        (stage / 'payload.txt').write_text(name, encoding='utf-8')
        (stage / '.provision-report').write_text(value, encoding='utf-8')

    with patch.object(STORE.shutil, 'disk_usage', return_value=type('Usage', (), {'free': 10_000_000_000})()):
        entry = store.ensure(
            'child',
            identity(suffix),
            {'name': name, 'env': '', 'suite': suite, 'report': value},
            build,
            lambda path: None,
        )
    return entry, value


def retire_env(base, work, tests, store, name, **extra):
    env = os.environ.copy()
    env.update({
        'RETIRE_VENV_ORCH_ROOT': str(base / 'orch'),
        'RETIRE_VENV_WORK_ROOT': str(work),
        'RETIRE_VENV_PROC_ROOT': str(base / 'proc'),
        'RETIRE_VENV_BENCH_STORE_SCRIPT': str(STORE_SOURCE),
        'RETIRE_VENV_BENCH_STORE_ROOT': str(store.root),
        'RETIRE_VENV_BENCH_STORE_TESTS': str(tests),
    })
    (base / 'proc').mkdir(exist_ok=True)
    env.update(extra)
    return subprocess.run(
        ['bash', str(RETIRE_SOURCE), name], env=env, capture_output=True, text=True, check=False
    )


def make_old(path):
    old = time.time() - 7201
    os.utime(path, (old, old))


def read_index(store):
    return json.loads((store.root / 'index.json').read_text(encoding='utf-8'))


def test_parent_workroot_route_cannot_reach_store_entry():
    base, work, tests, store = fixture_root()
    entry, _ = add_child(store, 'venv-agent-child-d137-a4e016', 'a')
    make_old(Path(entry['path']))
    result = retire_env(
        base,
        work,
        tests,
        store,
        'venv-agent-child-d137-a4e016',
        RETIRE_VENV_BENCH_STORE_SCRIPT=str(base / 'missing-bench-store.py'),
    )
    assert result.returncode == 2
    assert Path(entry['path']).is_dir()
    assert 'registrations' in read_index(store)


def test_store_route_retires_exact_child_and_preserves_receipt_and_unrelated_entry():
    base, work, tests, store = fixture_root()
    target, target_report = add_child(store, 'venv-agent-child-d137-a4e016', 'a')
    other, other_report = add_child(store, 'venv-agent-child-d40-ba8f-f320', 'b')
    make_old(Path(target['path']))
    result = retire_env(base, work, tests, store, 'venv-agent-child-d137-a4e016')
    assert result.returncode == 0, result.stdout + result.stderr
    assert not Path(target['path']).exists()
    assert Path(other['path']).is_dir()
    index = read_index(store)
    assert 'venv-agent-child-d137-a4e016' not in index['registrations']
    assert 'venv-agent-child-d137-a4e016' in index['retired']
    assert index['registrations']['venv-agent-child-d40-ba8f-f320']['requires'] == [
        'child-' + other['key']
    ]
    assert (tests / 'provision/venv-agent-child-d137-a4e016.txt').read_text(encoding='utf-8') == target_report
    assert (tests / 'provision/venv-agent-child-d40-ba8f-f320.txt').read_text(encoding='utf-8') == other_report


@pytest.mark.parametrize('case', ['young', 'referenced', 'keep', 'unknown'])
def test_store_route_refuses_safety_guards(case):
    base, work, tests, store = fixture_root()
    name = 'venv-agent-child-d137-a4e016'
    entry, _ = add_child(
        store,
        name,
        'a',
        suite=f'agent {name} full env -i true\n' if case == 'referenced' else '',
    )
    if case != 'young':
        make_old(Path(entry['path']))
    if case == 'keep':
        (Path(entry['path']) / 'KEEP').touch()
    requested = name if case != 'unknown' else 'venv-agent-child-unknown'
    result = retire_env(base, work, tests, store, requested)
    assert result.returncode == 2
    assert Path(entry['path']).is_dir()
    assert name in read_index(store)['registrations']


def test_store_route_refuses_held_lease():
    base, work, tests, store = fixture_root()
    name = 'venv-agent-child-d137-a4e016'
    entry, _ = add_child(store, name, 'a')
    make_old(Path(entry['path']))
    with store.acquire([name]):
        result = retire_env(base, work, tests, store, name)
    assert result.returncode == 2
    assert Path(entry['path']).is_dir()
    assert name in read_index(store)['registrations']


def test_store_route_refuses_process_using_entry():
    base, work, tests, store = fixture_root()
    name = 'venv-agent-child-d137-a4e016'
    entry, _ = add_child(store, name, 'a')
    target = Path(entry['path'])
    make_old(target)
    process = subprocess.Popen(['sleep', '5'], cwd=target)
    try:
        result = retire_env(base, work, tests, store, name, RETIRE_VENV_PROC_ROOT='/proc')
    finally:
        process.terminate()
        process.wait(timeout=5)
    assert result.returncode == 2
    assert target.is_dir()
    assert name in read_index(store)['registrations']


def test_store_route_refuses_wrong_identity_and_unknown_dependency():
    base, work, tests, store = fixture_root()
    name = 'venv-agent-child-d137-a4e016'
    entry, _ = add_child(store, name, 'a')
    make_old(Path(entry['path']))
    index = read_index(store)
    eid = 'child-' + entry['key']
    index['entries'][eid]['identity']['agent_sha'] = 'b' * 40
    (store.root / 'index.json').write_text(json.dumps(index), encoding='utf-8')
    result = retire_env(base, work, tests, store, name)
    assert result.returncode == 2
    assert Path(entry['path']).is_dir()


def test_retirement_recovery_reuses_journal_and_owned_delete():
    _base, _work, _tests, store = fixture_root()
    name = 'venv-agent-child-d137-a4e016'
    entry, report = add_child(store, name, 'a')
    make_old(Path(entry['path']))
    original = store._checkpoint

    def fail(point):
        if point == 'retirement:journal':
            raise RuntimeError('fixture crash')
        original(point)

    store._checkpoint = fail
    with pytest.raises(RuntimeError, match='fixture crash'):
        store.retire(name)
    assert (store.root / 'pending.json').exists()
    store._checkpoint = original
    store.recover()
    assert not Path(entry['path']).exists()
    assert (store.tests / 'provision' / f'{name}.txt').read_text(encoding='utf-8') == report
    assert name in read_index(store)['retired']


def test_legacy_workroot_route_remains_unchanged():
    base, work, tests, store = fixture_root()
    name = 'venv-agent-child-legacy'
    target = work / name
    target.mkdir()
    (target / 'payload.txt').write_text('legacy', encoding='utf-8')
    make_old(target)
    result = retire_env(base, work, tests, store, name)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not target.exists()

