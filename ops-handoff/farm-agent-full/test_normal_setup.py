"""Private checks of the installed API; never call the held wrapper."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
from test_farm_agent_full import BENCH_SOURCE, PACKET, _snapshot

INPUTS = json.loads((PACKET / 'selected-inputs.json').read_bytes())


@pytest.fixture
def api():
    assert hashlib.sha256(BENCH_SOURCE.read_bytes()).hexdigest() == INPUTS['bench_source_sha256']
    spec = importlib.util.spec_from_file_location('normal_setup_store', BENCH_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fresh_api_and_public_read_only_reuse(api, tmp_path: Path) -> None:
    tests = tmp_path / 'tests'
    tests.mkdir()
    baseline = INPUTS['full_row'].encode()
    (tests / 'suites.conf').write_bytes(baseline)
    root = tmp_path / 'store'
    store = api.Store.initialize(root, tests)
    assert root.stat().st_mode & 0o777 == 0o700
    index = json.loads((root / 'index.json').read_bytes())
    assert index == {
        'version': 1, 'seq': 0, 'entries': {}, 'registrations': {},
        'retired': [], 'retired_suites': [],
    }
    before = _snapshot(tmp_path)
    reopened = api.Store(root, tests)
    assert reopened.owner == store.owner
    assert not reopened.registered('farm-agent-full')
    assert reopened.names_for_suite('agent', 'full', baseline.decode().split(None, 2)[2].rstrip('\n')) == []
    assert _snapshot(tmp_path) == before


@pytest.mark.parametrize('kind', ['unknown', 'partial', 'symlink'])
def test_initialize_never_adopts_and_writes_nothing(api, tmp_path: Path, kind: str) -> None:
    tests = tmp_path / 'tests'
    tests.mkdir()
    (tests / 'suites.conf').write_text(INPUTS['full_row'])
    root = tmp_path / 'store'
    if kind == 'symlink':
        root.symlink_to(tests, target_is_directory=True)
    else:
        root.mkdir()
        (root / ('owner.json' if kind == 'partial' else 'unowned')).write_text('{}')
    before = _snapshot(tmp_path)
    with pytest.raises(api.Refused):
        api.Store.initialize(root, tests)
    assert _snapshot(tmp_path) == before


def test_fresh_index_requires_first_managed_build(api, tmp_path: Path) -> None:
    tests = tmp_path / 'tests'
    tests.mkdir()
    (tests / 'suites.conf').write_text(INPUTS['full_row'])
    store = api.Store.initialize(tmp_path / 'store', tests)
    called = []

    def build(stage, final):
        called.append((stage, final))
        raise RuntimeError('first managed build required')

    def verify(path):
        pytest.fail('fresh entry must be built before verification')

    with pytest.raises(RuntimeError, match='first managed build required'):
        store.ensure('runtime', {'remotion_tree': INPUTS['remotion_tree']}, {}, build, verify)
    assert len(called) == 1
    assert not store.registered('farm-agent-full')
    assert (tests / 'suites.conf').read_text() == INPUTS['full_row']


def test_selected_lock_and_exact_full_row() -> None:
    raw = (PACKET / 'runtime.lock.selected.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == INPUTS['runtime_lock_sha256']
    assert json.loads(raw)['source_commit'] == INPUTS['runtime_commit']
    baseline = INPUTS['full_row'].encode()
    assert len(baseline) == 86
    assert hashlib.sha256(baseline).hexdigest() == INPUTS['full_row_sha256']
    row = (PACKET / 'registration-row.txt').read_bytes()
    runtime = INPUTS['runtime_checkout'].encode()
    assert row == (
        b'agent full-farm env ASTRID_RUNTIME_CHECKOUT=' + runtime
        + b' PYTHONPATH="$PWD:' + runtime + b'" '
        + baseline.split(None, 2)[2]
    )
