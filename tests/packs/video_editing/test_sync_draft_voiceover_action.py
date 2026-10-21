"""Managed Python invocation and real manifest harvest, without live services."""
from __future__ import annotations

import copy
import json
import sys
from contextlib import nullcontext
from dataclasses import replace

import pytest

from astrid.core.env_vars import ASTRID_INTERNAL_INVOCATION
from astrid.core.execution.executor import _action_context as action_context
from astrid.core.execution.executor._action_context import _require_action_context
from astrid.core.execution.executor.registry import ExecutorRegistry
from astrid.core.execution.executor.runner import ExecutorRunnerError, run_executor
from astrid.core.execution.generic_host import HostError
from astrid.packs.video_editing.shared import draft_voiceover
from astrid.sdk import AstridClient
from astrid.sdk.timeline.commit import _digest
from tests.core.execution.test_python_action_context import managed_invocation as managed_invocation
from tests.editing_conformance.test_settled_proposal_contract import settled_proposal


def proposal(f):
    result = settled_proposal()
    result['producer'] = {key: f.bound[key] for key in result['producer']}
    result['admitted_target'] = copy.deepcopy(f.target)
    result.pop('proposal_digest')
    result['proposal_digest'] = _digest(result)
    return result


@pytest.fixture
def action(request, monkeypatch):
    f = request.getfixturevalue('managed_invocation')
    monkeypatch.setenv(ASTRID_INTERNAL_INVOCATION, '1')
    f.proposal = proposal(f)
    # A hostile client/environment must never supply outer authority.
    f.client = type('CallerClient', (), {'trusted_execution_context': {
        'task_id': 'inner-speech', 'attempt_id': 'inner-attempt', 'executor_id': 'caller-worker',
        'fence': 999, 'runtime_epoch': 999}})()
    monkeypatch.setenv('ASTRID_NETWORK_ADMISSION', json.dumps(f.client.trusted_execution_context))
    monkeypatch.setattr(action_context, '_managed_read_client',
                        lambda context: nullcontext(f.client))
    f.calls = []

    def sync(client, project, timeline, **kwargs):
        f.calls.append((client, project, timeline, kwargs))
        assert _require_action_context().producer['task_id'] == 'outer-task'
        assert client.trusted_execution_context == _require_action_context().producer
        assert client.trusted_execution_context != f.client.trusted_execution_context
        return {'authoring_proposal': copy.deepcopy(f.proposal)}

    monkeypatch.setattr(draft_voiceover, '_sync_draft_voiceover_proposal', sync)
    return f


def invoke(f, *, request=None, admission=None):
    return run_executor(request or f.request, ExecutorRegistry([f.definition]),
                        _admission=f.bound if admission is None else admission)


def assert_closed():
    with pytest.raises(ValueError, match='managed host invocation'):
        _require_action_context()
    assert not any(name.startswith('_astrid_pack_') for name in sys.modules)


def test_existing_action_settles_only_claim_bound_proposal_and_manifest(action):
    f = action
    result = invoke(f)
    assert result.ok and result.payload == {'action_result': {'authoring_proposal': f.proposal}}
    assert len(f.calls) == 1 and f.calls[0][1:3] == ('project', 'timeline')
    assert len(result.outputs) == 1
    output = result.outputs[0]
    assert output['name'] == 'authoring_proposal'
    assert output['path'] == str(f.request.out / 'authoring-proposal.json')
    assert output['role'] == 'result' and output['is_primary']
    assert json.loads((f.request.out / 'authoring-proposal.json').read_text()) == f.proposal
    manifest = json.loads((f.request.out / 'manifest.json').read_text())
    assert len(manifest['outputs']) == 1
    assert manifest['outputs'][0]['artifact_type'] == 'timeline/authoring-proposal'
    assert output['content_hash'] == manifest['outputs'][0]['content_hash']
    assert 'receipt' not in result.payload['action_result']
    assert 'report' not in result.payload['action_result']
    assert_closed()


def test_action_uses_private_managed_entry_not_public_sync(action, monkeypatch):
    monkeypatch.setattr(draft_voiceover, 'sync_draft_voiceover',
                        lambda *a, **k: pytest.fail('public sync path must not run'))
    result = invoke(action)
    assert result.ok and result.payload['action_result']['authoring_proposal'] == action.proposal
    assert_closed()


def test_declaration_keeps_existing_eight_inputs_and_network_false(action):
    f = action
    assert [port.name for port in f.definition.inputs] == [
        'project', 'timeline_ref', 'timing_policy', 'settings', 'occurrence_ids',
        'adopt_clip_ids', 'padding_seconds', 'plan_only']
    assert f.definition.isolation.network is False
    assert f.definition.metadata['output_result_manifest'] is True
    assert [port.artifact_type for port in f.definition.outputs] == [
        'timeline/authoring-proposal', 'application/json']


def test_missing_trusted_context_refuses_before_shared_work(action):
    f = action
    with pytest.raises(ValueError, match='managed host invocation'):
        invoke(f, admission=f.admission)
    assert not f.calls and not list(f.request.out.iterdir())
    assert_closed()


@pytest.mark.parametrize('field', ['task_id', 'attempt_id', 'executor_id', 'fence', 'runtime_epoch'])
def test_proposal_cannot_substitute_any_producer_coordinate(action, field):
    f = action
    f.proposal['producer'][field] = 888 if field in {'fence', 'runtime_epoch'} else 'inner-speech'
    with pytest.raises(ValueError, match='trusted outer claim'):
        invoke(f)
    assert not list(f.request.out.iterdir())
    assert_closed()


def test_proposal_target_cannot_replace_admitted_base(action):
    f = action
    f.proposal['admitted_target']['base_revision_id'] = 'newer-head'
    with pytest.raises(ValueError, match='trusted outer claim'):
        invoke(f)
    assert not list(f.request.out.iterdir())
    assert_closed()


def test_caller_identity_is_never_an_action_input(action):
    f = action
    request = replace(f.request, inputs={**f.request.inputs,
                                         'producer': f.client.trusted_execution_context})
    with pytest.raises(TypeError, match='unexpected keyword argument'):
        invoke(f, request=request)
    assert not f.calls and not list(f.request.out.iterdir())
    assert_closed()


@pytest.mark.parametrize('status', ['planned', 'unchanged'])
def test_advisory_shared_result_settles_positive_report(action, monkeypatch, status):
    f = action
    monkeypatch.setattr(draft_voiceover, 'sync_draft_voiceover',
                        lambda *a, **k: pytest.fail('public sync path must not run'))
    advisory = {'status': status, 'published': False, 'plan': {'jobs': [], 'statuses': []}}
    monkeypatch.setattr(draft_voiceover, '_sync_draft_voiceover_proposal',
                        lambda *a, **k: copy.deepcopy(advisory))
    result = invoke(f)
    assert result.ok and result.payload == {'action_result': {'report': advisory}}
    assert json.loads((f.request.out / 'report.json').read_text()) == advisory
    assert not (f.request.out / 'authoring-proposal.json').exists()
    assert len(result.outputs) == 1 and result.outputs[0]['name'] == 'report'
    assert result.outputs[0]['path'] == str(f.request.out / 'report.json')
    manifest = json.loads((f.request.out / 'manifest.json').read_text())
    assert manifest['outputs'][0]['name'] == 'report'
    assert manifest['outputs'][0]['artifact_type'] == 'application/json'
    assert result.outputs[0]['content_hash'] == manifest['outputs'][0]['content_hash']
    assert 'authoring_proposal' not in result.payload['action_result']
    assert 'receipt' not in result.payload['action_result']
    assert_closed()


@pytest.mark.parametrize('damage', ['source', 'definition', 'public-bypass'])
def test_existing_source_and_definition_fences_run_before_action(action, damage):
    f = action
    admission = dict(f.bound)
    if damage == 'source':
        admission['source_digest'] = 'forged'
    elif damage == 'definition':
        admission['capability_digest'] = 'forged'
    else:
        with pytest.raises(ExecutorRunnerError, match='admitted internal host worker'):
            run_executor(f.request, ExecutorRegistry([f.definition]))
        assert not f.calls
        assert_closed()
        return
    with pytest.raises(HostError, match='digest'):
        invoke(f, admission=admission)
    assert not f.calls and not list(f.request.out.iterdir())
    assert_closed()


def test_failed_shared_work_releases_context_and_pack_modules(action, monkeypatch):
    f = action
    captured = []
    def failed(*args, **kwargs):
        captured.append(_require_action_context())
        raise RuntimeError('speech failed')
    monkeypatch.setattr(draft_voiceover, '_sync_draft_voiceover_proposal', failed)
    with pytest.raises(RuntimeError, match='speech failed'):
        invoke(f)
    assert not list(f.request.out.iterdir())
    assert_closed()
    with pytest.raises(ValueError, match='lifetime'):
        _ = captured[0].producer


def test_shared_helper_cannot_reach_legacy_publish(action, monkeypatch):
    f = action
    published = []
    target = type('Target', (), {'publish': lambda *a, **k: published.append(True)})()
    monkeypatch.setattr(f.client, 'open_authoring_target', lambda *a, **k: target, raising=False)
    def legacy(client, *args, **kwargs):
        client.open_authoring_target({}).publish({'candidate': 'legacy'})
    monkeypatch.setattr(draft_voiceover, '_sync_draft_voiceover_proposal', legacy)
    with pytest.raises(ValueError, match='preparation cannot publish'):
        invoke(f)
    assert not published and not list(f.request.out.iterdir())
    assert_closed()


def test_private_client_view_expires_without_changing_caller_client(action):
    f = action
    original = copy.deepcopy(f.client.trusted_execution_context)
    invoke(f)
    retained = f.calls[0][0]
    assert f.client.trusted_execution_context == original
    with pytest.raises(ValueError, match='lifetime'):
        _ = retained.trusted_execution_context


def test_underlying_client_identity_is_never_read(action, monkeypatch):
    f = action
    class PoisonClient:
        @property
        def trusted_execution_context(self):
            pytest.fail('caller identity must never be read')
    monkeypatch.setattr(AstridClient, 'open_from_launcher', lambda: nullcontext(PoisonClient()))
    def sync(client, *args, **kwargs):
        assert client.trusted_execution_context == _require_action_context().producer
        return {'authoring_proposal': f.proposal}
    monkeypatch.setattr(draft_voiceover, '_sync_draft_voiceover_proposal', sync)
    assert invoke(f).payload['action_result']['authoring_proposal'] == f.proposal
    assert_closed()


def test_request_output_overrides_cannot_redirect_managed_proposal(action, tmp_path):
    f = action
    destination = tmp_path / 'caller-proposal.json'
    request = replace(f.request, outputs={'authoring_proposal': str(destination)},
                       project_run_metadata={'producer': f.client.trusted_execution_context})
    result = invoke(f, request=request)
    assert result.outputs[0]['path'] == str(f.request.out / 'authoring-proposal.json')
    assert not destination.exists()
    assert_closed()
