"""Offline renderer liveness refusal capture; no lifecycle or process access."""
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from runtime_protocol import local_worker
from runtime_protocol import verified_host_launch as gate
from test_verified_host_launch import fixture_authority


@pytest.mark.parametrize('edge', ['shape', 'missing-path'])
def test_real_renderer_refusal_keeps_cause_frames_and_fences_child(tmp_path, monkeypatch, capsys, edge):
    source = os.environ.get('HOST_LAUNCH_TEST_ASTRID_SOURCE')
    if not source:
        pytest.skip('select admitted SDK source for exact renderer validation')
    from astrid.core.execution import host_renderer_selection as renderer
    assert Path(renderer.__file__).is_relative_to(Path(source))
    selection = {}
    if edge == 'missing-path':
        selection = dict(version='astrid.host-renderer-selection/v1',
                         **{name: str(tmp_path/'private-unrecorded-path') for name in (
                             'project', 'installed_project', 'verification_receipt', 'node_executable')},
                         **{name: '0'*64 for name in (
                             'receipt_sha256', 'manifest_sha256', 'lock_sha256', 'closure_sha256',
                             'node_admission_sha256', 'node_sha256')})
    observation = gate._LocalInstallationObservation(
        dict(host_executable='/private-unrecorded-executable', host_artifact_digest='sha256:'+'0'*64,
             host_launch={'renderer_selection': selection}),
        dict(path='/private-unrecorded-launcher', sha256='0'*64))
    f = fixture_authority(tmp_path/'authority')
    proof = f.verifier.verify(**f.args)
    f.verifier.claim(proof, **f.args, binding_fd=3)
    child, identity = SimpleNamespace(pid=41), dict(pid=41, uid=0, birth_id='offline')
    f.verifier.bind_child(proof, child=child, identity=identity)
    monkeypatch.setattr(f.lease, 'verify', observation.verify)
    with pytest.raises(gate.HostLaunchError, match='selected renderer closure changed') as caught:
        f.verifier.verify_child(proof, child=child, identity=identity)
    cause = caught.value.__cause__
    assert isinstance(cause, ValueError if edge == 'shape' else FileNotFoundError)
    local_worker._report_start_failure(caught.value, phase='liveness')
    output = capsys.readouterr().err
    row = json.loads(output)
    assert row['phase'] == 'liveness' and row['exception_type'] == 'HostLaunchError'
    assert row['causes'][0]['exception_type'] == type(cause).__name__
    assert any(frame['file'] == 'host_renderer_selection.py' for frame in row['causes'][0]['frames'])
    assert all(set(frame) == {'file', 'function', 'line'} for item in [row, *row['causes']] for frame in item['frames'])
    assert 'private-unrecorded' not in output and str(tmp_path) not in output
    assert str(cause) not in output
    with pytest.raises(gate.HostLaunchError, match='child/session binding changed'):
        f.verifier.verify_child(proof, child=child, identity=identity)


def test_cause_capture_bounds_chain_and_cycles_without_values(capsys):
    errors = [ValueError('private-value-'+str(i)) for i in range(8)]
    for current, cause in zip(errors, errors[1:]):
        current.__cause__ = cause
    local_worker._report_start_failure(errors[0])
    row = json.loads(capsys.readouterr().err)
    assert len(row['causes']) == 4
    assert 'private-value' not in json.dumps(row)
    errors[1].__cause__ = errors[0]
    local_worker._report_start_failure(errors[0])
    assert len(json.loads(capsys.readouterr().err)['causes']) == 1


def test_implicit_context_and_exception_values_remain_private(capsys):
    try:
        raise ValueError('private-context')
    except ValueError:
        error = RuntimeError('private-primary')
        local_worker._report_start_failure(error, phase='liveness')
    row = json.loads(capsys.readouterr().err)
    assert 'causes' not in row and row['exception_type'] == 'RuntimeError'
    assert 'private-' not in json.dumps(row)


def test_cause_capture_sink_failure_is_secondary(monkeypatch):
    import builtins
    error = RuntimeError('private-primary')
    error.__cause__ = ValueError('private-cause')
    def broken(*args, **kwargs):
        raise OSError('private-sink')
    monkeypatch.setattr(builtins, 'print', broken)
    assert local_worker._report_start_failure(error, phase='liveness') is None
    assert isinstance(error.__cause__, ValueError)
