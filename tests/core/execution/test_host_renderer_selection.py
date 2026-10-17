"""Profile selection is closed over admitted bytes, never task/environment claims."""
import copy
import os
from pathlib import Path
import sys

import pytest

from tests.core.execution.test_remotion_closure_binding import roots, sha
from astrid.core.execution import remotion_closure as closure
from astrid.core.execution import host_renderer_selection as selected
from astrid.core.execution.declared_executables import ExecutableBinding, FilePin


@pytest.fixture
def selection(roots, monkeypatch):
    project, installed, receipt, args = roots
    patches = {}
    for relative in closure._RETAINED_TRANSPORT_PATCHES:
        path = installed/'node_modules/@remotion/renderer/dist'/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('disposable retained transport '+relative)
        patches[relative] = sha(path)
    monkeypatch.setattr(closure, '_RETAINED_TRANSPORT_PATCHES', patches)
    binding = closure.RemotionClosureBinding.admit(**args)
    node = ExecutableBinding('node', FilePin.measure(Path(sys.executable).resolve()), (), (), tuple(os.uname()))
    return selected.HostRendererSelection(binding, node)


def test_admitted_typed_selection_roundtrip_and_node_inspection(selection, monkeypatch):
    value = selection.payload()
    assert selected.validate_renderer_selection(value) == selection.closure
    from astrid.core.execution import declared_executables
    calls = []
    def inspect(name, path):
        calls.append((name, path))
        return selection.node
    monkeypatch.setattr(declared_executables, '_bind', inspect)
    assert selected.activate_renderer_selection(value) == selection.closure
    assert calls == [('node', selection.node.executable.path)]
    monkeypatch.setattr(declared_executables, '_bind', lambda *args: ExecutableBinding(
        'node', selection.node.executable, (), (Path('/changed/library'),), tuple(os.uname())))
    with pytest.raises(ValueError, match='Node admission'):
        selected.activate_renderer_selection(value)


@pytest.mark.parametrize('field', ['receipt_sha256', 'manifest_sha256', 'lock_sha256', 'closure_sha256', 'node_sha256'])
def test_selection_rejects_changed_pin(selection, field):
    value = selection.payload()
    value[field] = '0'*64
    with pytest.raises(ValueError):
        selected.validate_renderer_selection(value)


@pytest.mark.parametrize('change', ['receipt', 'manifest', 'lock', 'composition', 'worker', 'extra-source', 'dependency', 'project', 'node', 'extra-field'])
def test_selection_rejects_substitution_before_activation(selection, change, tmp_path):
    value = selection.payload()
    c = selection.closure
    paths = {'receipt': c.receipt, 'manifest': c.project/'package.json',
             'lock': c.project/'package-lock.json',
             'composition': c.project/'vendor/timeline-composition/evaluation.ts',
             'worker': c.project/'src/astrid-frame-worker.mjs',
             'extra-source': c.project/'src/unadmitted.mjs',
             'dependency': c.installed_project/'node_modules/@remotion/cli/remotion-cli.js'}
    if change in paths:
        paths[change].write_text('changed')
    elif change == 'project':
        value['project'] = str(tmp_path)
    elif change == 'node':
        value['node_executable'] = str(c.receipt)
    else:
        value['inspection'] = {'trusted': True}
    with pytest.raises((ValueError, OSError, KeyError)):
        selected.validate_renderer_selection(value)


def test_selection_rechecks_source_inventory_on_every_lease(selection):
    (selection.closure.project/'src/unadmitted.mjs').write_text('new')
    with pytest.raises(ValueError, match='inventory changed'):
        selection.closure.validate(selection.closure.project)


def test_raw_json_is_not_a_producer_admission(selection):
    with pytest.raises(ValueError, match='typed inputs'):
        selected.HostRendererSelection(selection.payload(), selection.node).payload()
