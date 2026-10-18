"""Completion diagnostics must retain failure evidence without receipt secrets."""
import json
import subprocess
from types import SimpleNamespace

import pytest

from astrid.core.rendering import remotion_runtime as runtime


SENTINEL = 'private-argv-environment-output-must-not-cross-diagnostic'


def _receipt():
    return {'original_wait_exit_code': 0, 'original_child_pid': 71,
            'retained_set_final_census_complete': True, 'custody_admitted': True,
            'argv': [SENTINEL], 'environment': {'TOKEN': SENTINEL}, 'cwd': SENTINEL,
            'stdout': SENTINEL, 'stderr': SENTINEL}


@pytest.mark.parametrize('field,value', [
    ('original_wait_exit_code', 1), ('original_wait_exit_code', None),
    ('retained_set_final_census_complete', False), ('custody_admitted', False),
])
def test_failed_probe_reports_exact_check_without_receipt_data(field, value):
    receipt = _receipt()
    if value is None:
        receipt.pop(field)
    else:
        receipt[field] = value
    with pytest.raises(runtime.RemotionValidationError) as caught:
        runtime._require_completed_probe(receipt, phase='registry_discovery')
    error = caught.value
    assert error.probe_check['phase'] == 'registry_discovery'
    assert error.probe_check['failed_checks'] == [field]
    assert error.probe_check['original_child_pid'] == 71
    assert error.probe_check['exit_code_missing'] is (value is None)
    assert SENTINEL not in str(error) + json.dumps(error.probe_check)
    assert not {'argv', 'environment', 'cwd', 'stdout', 'stderr'}.intersection(error.probe_check)
    assert error.__cause__ is None


@pytest.mark.parametrize('code', [0, False])
def test_completed_probe_keeps_original_acceptance_semantics(code):
    receipt = _receipt()
    receipt['original_wait_exit_code'] = code
    before = dict(receipt)
    assert runtime._require_completed_probe(receipt, phase='node_version') is None
    assert receipt == before


def test_probe_diagnostic_never_formats_untrusted_values_or_type_names():
    secret_type = type(SENTINEL, (), {'__repr__': lambda _: SENTINEL})
    receipt = _receipt()
    receipt.update(original_wait_exit_code=secret_type(), original_child_pid=True,
                   retained_set_final_census_complete='true', custody_admitted='true')
    with pytest.raises(runtime.RemotionValidationError) as caught:
        runtime._require_completed_probe(receipt, phase=SENTINEL)
    safe = caught.value.probe_check
    assert safe['phase'] == 'unknown' and safe['exit_code_type'] == 'other'
    assert safe['original_wait_exit_code'] is None and safe['original_child_pid'] is None
    assert safe['custody_admitted'] is False and safe['census_complete'] is False
    assert safe['custody_admitted_type'] == safe['census_complete_type'] == 'str'
    assert safe['failed_checks'] == ['original_wait_exit_code', 'retained_set_final_census_complete', 'custody_admitted']
    assert SENTINEL not in str(caught.value) + json.dumps(safe)


def test_registry_generator_nonzero_keeps_failure_and_safe_phase(monkeypatch, tmp_path):
    from astrid.packs.rendering.rendering.renderers.remotion import run, lock

    expected = {'content_hashes': {'fixed': 'registry-state'}}
    lock_path = tmp_path / 'held-lock'
    monkeypatch.setattr(lock, 'remotion_render_lock_held', lambda: True)
    monkeypatch.setattr(lock, '_resolved_lock_path', lambda: lock_path)
    monkeypatch.setattr(lock, 'remotion_render_lock_child_env', lambda: {'TOKEN': SENTINEL})
    monkeypatch.setattr(run, '_timeline_composition_src', lambda _: tmp_path / 'composition')
    monkeypatch.setattr(run, '_registry_output_paths', lambda _: ())
    monkeypatch.setattr(run, 'gen_effect_registry', object())
    monkeypatch.setattr(run, '_read_registry_state', lambda _: None)
    monkeypatch.setattr(run, '_registry_output_content_hashes', lambda _: {})
    monkeypatch.setattr(runtime, '_registry_context', lambda env, **_: dict(env))
    monkeypatch.setattr(runtime, '_registry_inputs', lambda _: {'bound': True})
    observation = {'state': expected, 'lock_path': str(lock_path)}
    monkeypatch.setattr(runtime, '_registry_probe', lambda *_a, **_k: (observation, _receipt()))
    calls = []

    def failed_generator(argv, **kwargs):
        calls.append((argv, kwargs))
        receipt = _receipt()
        receipt['original_wait_exit_code'] = 1
        return subprocess.CompletedProcess([SENTINEL], 1, SENTINEL, SENTINEL), receipt

    monkeypatch.setattr(runtime, '_owned_probe', failed_generator)
    with pytest.raises(runtime.RemotionValidationError) as caught:
        runtime._settle_registries(tmp_path, {'renderer': {'TOKEN': SENTINEL}}, 'fake-python')
    safe = caught.value.probe_check
    assert len(calls) == 1 and safe['phase'] == 'registry_generator'
    assert safe['failed_checks'] == ['original_wait_exit_code']
    assert safe['original_wait_exit_code'] == 1 and safe['original_child_pid'] == 71
    assert safe['custody_admitted'] is True and safe['census_complete'] is True
    assert SENTINEL not in str(caught.value) + json.dumps(safe)
    assert caught.value.__cause__ is None


def test_existing_failure_writer_retains_safe_check_and_original_error(monkeypatch, tmp_path):
    receipt = _receipt()
    receipt['original_wait_exit_code'] = -9
    try:
        runtime._require_completed_probe(receipt, phase='qualifying')
    except runtime.RemotionValidationError as error:
        original = error
    cause = RuntimeError('original fixed cause')
    original.__cause__ = cause
    process = SimpleNamespace(pid=71)
    original.process = process
    monkeypatch.setattr(runtime, '_UNRESOLVED_VALIDATION_PROBES', [])

    def fail(**kwargs):
        raise original

    monkeypatch.setattr(runtime, '_prepare_remotion_validation', fail)
    with pytest.raises(runtime.RemotionValidationError) as caught:
        runtime.prepare_remotion_validation(artifact_directory=tmp_path)
    assert caught.value is original and caught.value.__cause__ is cause
    assert caught.value.process is process
    evidence = json.loads(next(tmp_path.glob('failed-validation-*.json')).read_text())
    assert evidence['status'] == 'FAILED_NOT_READINESS'
    assert evidence['probe_check'] == original.probe_check
    assert evidence['probe_check']['original_wait_exit_code'] == -9
    assert evidence['retained_original_child_pid'] == 71
    assert evidence['original_probe_receipt'] is None
    assert SENTINEL not in json.dumps(evidence) + str(caught.value)


@pytest.mark.parametrize("phase", ["complete_inputs", "owned_probe_acquire", "owned_probe_execute"])
def test_validation_phase_begins_before_blocking_and_retains_first_failure(phase, capsys):
    error = runtime.RemotionValidationError(SENTINEL)
    @runtime._validation_timing(phase)
    def fail():
        rows = [json.loads(line) for line in capsys.readouterr().err.splitlines()]
        assert rows[-1]["outcome"] == "begun" and rows[-1]["phase"] == phase
        raise error
    with pytest.raises(runtime.RemotionValidationError) as caught:
        fail()
    assert caught.value is error and error.validation_phase == phase
    rows = [json.loads(line) for line in capsys.readouterr().err.splitlines()]
    assert rows[-1]["outcome"] == "failed" and rows[-1]["elapsed_ms"] >= 0
    assert SENTINEL not in json.dumps(rows)


def test_validation_artifact_write_failure_keeps_primary_and_phase(monkeypatch, tmp_path, capsys):
    error = runtime.RemotionValidationError(SENTINEL)
    error.validation_phase = "complete_inputs"
    monkeypatch.setattr(runtime, "_UNRESOLVED_VALIDATION_PROBES", [])
    monkeypatch.setattr(runtime, "_prepare_remotion_validation", lambda **_: (_ for _ in ()).throw(error))
    monkeypatch.setattr(runtime.Path, "mkdir", lambda *_a, **_k: (_ for _ in ()).throw(OSError(SENTINEL)))
    with pytest.raises(runtime.RemotionValidationError) as caught:
        runtime.prepare_remotion_validation(artifact_directory=tmp_path)
    assert caught.value is error and error.validation_evidence_error == "OSError"
    rows = [json.loads(line) for line in capsys.readouterr().err.splitlines()]
    assert rows[-1]["last_begun_phase"] == "complete_inputs"
    assert rows[-1]["persistence_error_class"] == "OSError"
    assert SENTINEL not in json.dumps(rows)


@pytest.mark.parametrize("seam", ["inputs", "acquisition", "execution"])
def test_actual_input_and_owned_probe_failure_phases_survive_cleanup(seam, monkeypatch, tmp_path, capsys):
    from astrid.core.execution import process_group
    primary = runtime.RemotionValidationError(SENTINEL)
    cleanup = TimeoutError(SENTINEL)
    process = SimpleNamespace(pid=71, returncode=None)
    def acquire(*args, **kwargs):
        if seam == "acquisition":
            raise primary
        return process
    process.communicate = lambda **_: (_ for _ in ()).throw(primary)
    monkeypatch.setattr(process_group, "popen_owned_group", acquire)
    monkeypatch.setattr(process_group, "terminate_group", lambda *_a, **_k: (_ for _ in ()).throw(cleanup))
    monkeypatch.setattr(process_group, "verify_tree_absent", lambda *_: None)
    monkeypatch.setattr(runtime, "_UNRESOLVED_VALIDATION_PROBES", [])
    def prepare(**kwargs):
        if seam == "inputs":
            return runtime._runtime_inputs(tmp_path, {}, "unused-python", {})
        return runtime._owned_probe([SENTINEL], cwd=tmp_path, env={"LANG": "C"}, timeout=1)
    monkeypatch.setattr(runtime, "_prepare_remotion_validation", prepare)
    with pytest.raises(runtime.RemotionValidationError) as caught:
        runtime.prepare_remotion_validation(artifact_directory=tmp_path)
    expected = {"inputs": "complete_inputs", "acquisition": "owned_probe_acquire", "execution": "owned_probe_execute"}[seam]
    assert caught.value.validation_phase == expected
    if seam != "inputs":
        assert caught.value is primary
    if seam == "execution":
        assert primary.cleanup_error is cleanup and primary.process is process
        assert runtime._UNRESOLVED_VALIDATION_PROBES == [primary]
    evidence = json.loads(next(tmp_path.glob("failed-validation-*.json")).read_text())
    assert evidence["last_begun_phase"] == expected
    rows = [json.loads(line) for line in capsys.readouterr().err.splitlines()]
    assert any(row.get("phase") == expected and row.get("outcome") == "begun" for row in rows)
    assert rows[-1]["last_begun_phase"] == expected
    assert SENTINEL not in json.dumps(rows) + json.dumps(evidence)
