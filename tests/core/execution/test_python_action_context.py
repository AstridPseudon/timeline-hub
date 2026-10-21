"""Direct custody tests; no worker launch, sockets, or Runtime acceptance claim."""
from __future__ import annotations

import copy
import hashlib
import json
from contextvars import copy_context
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from astrid.core.execution.executor import _action_context as context_module
from astrid.core.execution.executor._action_context import (
    _action_context_scope,
    _managed_read_client,
    _producer_action_admission,
    _require_action_context,
)
from astrid.core.execution.executor.actions import action_executor_definition
from astrid.core.execution.executor.runner import ExecutorRunRequest
from astrid.core.execution.generic_host import (
    HostError,
    _capability_digest,
    _source_digest_for_roots,
)


@pytest.fixture
def managed_invocation(tmp_path):
    root = Path(__file__).resolve().parents[3] / 'astrid/packs/video_editing'
    declaration = yaml.safe_load((root / 'pack.yaml').read_text())['actions']['sync_draft_voiceover']
    definition = action_executor_definition(
        SimpleNamespace(root=root, id='video_editing', version='1.0.0'),
        'sync_draft_voiceover', declaration)
    target = dict(project_id='project', timeline_id='timeline', base_revision_id='revision',
                  base_publication_id='publication')
    task = dict(id='outer-task', attempt_id='outer-attempt', executor_id='host-worker',
                fence=4, runtime_epoch=7, project_id='project', capability=definition.id,
                spec={'spec': {'runtime_dependencies': {'publication': {'admitted_target': target}}}})
    admission = dict(task_id=task['id'], attempt_id=task['attempt_id'], fence=task['fence'],
                     capability_digest=_capability_digest(definition.to_dict()),
                     source_digest=_source_digest_for_roots((root,)), source_root=str(root),
                     source_roots=[str(root)])
    bound = _producer_action_admission(definition, admission, task,
                                       executor_id='host-worker', runtime_epoch=7)
    (tmp_path / 'outputs').mkdir()
    request = ExecutorRunRequest(definition.id, tmp_path / 'outputs', project='project',
        inputs={'project': 'project', 'timeline_ref': 'timeline', 'timing_policy': 'preserve'},
        invocation='runtime', run_id='outer-task', run_root=tmp_path, project_was_auto_resolved=True)
    return SimpleNamespace(definition=definition, task=task, admission=admission, bound=bound,
                           target=target, request=request)


def test_claim_is_copied_from_outer_host_only(managed_invocation):
    f = managed_invocation
    assert f.bound['executor_id'] == 'host-worker' != f.definition.id
    assert not {'executor_id', 'runtime_epoch', 'admitted_target'} & f.admission.keys()
    f.task['spec']['spec']['runtime_dependencies']['publication']['admitted_target']['timeline_id'] = 'changed'
    assert f.bound['admitted_target']['timeline_id'] == 'timeline'
    assert f.bound['fence'] == 4 and f.bound['runtime_epoch'] == 7


@pytest.mark.parametrize('field', ['id', 'attempt_id', 'executor_id', 'fence', 'runtime_epoch'])
def test_missing_outer_claim_coordinate_refuses(managed_invocation, field):
    f = managed_invocation
    task = copy.deepcopy(f.task)
    task.pop(field)
    with pytest.raises(HostError, match='live claim'):
        _producer_action_admission(f.definition, f.admission, task,
                                   executor_id='host-worker', runtime_epoch=7)


@pytest.mark.parametrize('field,value', [('id', 'inner-speech'), ('attempt_id', 'other'),
    ('executor_id', 'caller-worker'), ('fence', 5), ('fence', True), ('runtime_epoch', 8),
    ('runtime_epoch', True), ('capability', 'generation.generate_speech')])
def test_claim_disagreement_cannot_become_producer_identity(managed_invocation, field, value):
    f = managed_invocation
    task = {**f.task, field: value}
    with pytest.raises(HostError, match='live claim'):
        _producer_action_admission(f.definition, f.admission, task,
                                   executor_id='host-worker', runtime_epoch=7)


@pytest.mark.parametrize('target', [None, {}, {'project_id': 'caller-project'}])
def test_missing_or_forged_admitted_target_refuses(managed_invocation, target):
    f = managed_invocation
    task = copy.deepcopy(f.task)
    task['spec']['spec']['runtime_dependencies']['publication']['admitted_target'] = target
    with pytest.raises(HostError, match='admitted publication target'):
        _producer_action_admission(f.definition, f.admission, task,
                                   executor_id='host-worker', runtime_epoch=7)


def test_unrelated_actions_do_not_require_producer_context(managed_invocation):
    f = managed_invocation
    ordinary = replace(f.definition, outputs=())
    assert _producer_action_admission(ordinary, f.admission, {}, executor_id=None,
                                      runtime_epoch=None) is f.admission
    with _action_context_scope(f.request, f.admission):
        with pytest.raises(ValueError, match='managed host invocation'):
            _require_action_context()


def test_context_has_read_only_identity_and_expires_even_in_copied_context(managed_invocation):
    f = managed_invocation
    with _action_context_scope(f.request, f.bound):
        context = _require_action_context()
        retained = copy_context()
        assert dict(context.producer) == {key: f.bound[key] for key in context_module._PRODUCER_FIELDS}
        assert context.admitted_target == f.target and context.out == f.request.out
        with pytest.raises(TypeError):
            context.producer['task_id'] = 'caller'
        with pytest.raises(TypeError):
            context.admitted_target['project_id'] = 'caller'
        with pytest.raises(TypeError):
            json.dumps(context)
        with pytest.raises(ValueError, match='nested or reused'):
            with _action_context_scope(f.request, f.bound):
                pass
    with pytest.raises(ValueError, match='managed host invocation'):
        _require_action_context()
    with pytest.raises(ValueError, match='lifetime'):
        retained.run(_require_action_context)
    with pytest.raises(ValueError, match='lifetime'):
        _ = context.out


def test_managed_read_client_uses_host_identity_and_read_scopes(managed_invocation, monkeypatch):
    f = managed_invocation
    monkeypatch.setenv('ASTRID_RUNTIME_ENDPOINT', 'http://127.0.0.1:8765')
    monkeypatch.setenv('ASTRID_RUNTIME_CREDENTIAL', 'worker-token')
    requested = []

    class Transport:
        def __init__(self, endpoint, credential):
            self.endpoint, self.credential, self.actor_id = endpoint, credential, None

        def handshake(self, name, version, scopes):
            requested.append((name, version, tuple(scopes)))
            return {'actor_id': 'host-worker', 'scopes': list(scopes)}

    monkeypatch.setattr('astrid.sdk.workspace_client.WorkspaceClient', Transport)
    with _action_context_scope(f.request, f.bound):
        with _managed_read_client(_require_action_context()) as client:
            transport = client._remote._transport
            assert transport.endpoint == 'http://127.0.0.1:8765'
            assert transport.credential == 'worker-token'
            assert transport.actor_id == f.bound['executor_id']
    assert requested == [('astrid-managed-python', 'stage1',
                          ('worker:execute', 'projects:read', 'tasks:read', 'objects:read'))]


def test_managed_read_client_refuses_actor_substitution(managed_invocation, monkeypatch):
    f = managed_invocation
    monkeypatch.setenv('ASTRID_RUNTIME_ENDPOINT', 'http://127.0.0.1:8765')
    monkeypatch.setenv('ASTRID_RUNTIME_CREDENTIAL', 'worker-token')

    class Transport:
        def __init__(self, endpoint, credential):
            self.endpoint, self.credential = endpoint, credential

        def handshake(self, *args):
            return {'actor_id': 'inner-speech', 'scopes': list(args[-1])}

    monkeypatch.setattr('astrid.sdk.workspace_client.WorkspaceClient', Transport)
    with _action_context_scope(f.request, f.bound):
        with pytest.raises(ValueError, match='identity or scopes'):
            with _managed_read_client(_require_action_context()):
                pass


def test_settled_input_materializes_under_attempt_blob_root(tmp_path):
    from astrid.core.execution.generic_host import GenericPackHost

    payload = b'{"entries": []}\n'
    object_id = 'sha256:' + hashlib.sha256(payload).hexdigest()

    class Runtime:
        def get_object(self, digest):
            assert digest == object_id.removeprefix('sha256:')
            return payload

    host = GenericPackHost(pack_roots=[], client=Runtime())
    values = host._materialize_inputs(
        {'inputs': {'settled_speech_input': {
            'name': 'settled_speech_input', 'object_id': object_id,
            'digest': object_id, 'filename': 'settled-speech.json', 'required': True,
        }}, 'input_object_ids': [object_id]},
        tmp_path / 'attempt', authorized_input_object_ids=[object_id],
        file_input_names=frozenset({'settled_speech_input'}),
    )
    materialized = Path(values['settled_speech_input'])
    assert materialized.is_relative_to(tmp_path / 'attempt' / 'inputs')
    assert materialized.read_bytes() == payload


@pytest.mark.parametrize('field,value', [('out', None), ('run_root', None),
    ('run_id', 'inner-speech'), ('project', 'caller-project'), ('invocation', 'cli')])
def test_request_cannot_replace_host_context(managed_invocation, field, value):
    f = managed_invocation
    with pytest.raises(ValueError, match='missing or inconsistent'):
        with _action_context_scope(replace(f.request, **{field: value}), f.bound):
            pytest.fail('invalid request reached action')


def test_output_spool_and_process_thread_identity_are_fenced(managed_invocation, tmp_path, monkeypatch):
    f = managed_invocation
    other = tmp_path / 'caller-output'
    other.mkdir()
    with pytest.raises(ValueError, match='output root'):
        with _action_context_scope(replace(f.request, out=other), f.bound):
            pass
    with _action_context_scope(f.request, f.bound):
        with monkeypatch.context() as patch:
            patch.setattr(context_module.os, 'getpid', lambda: -1)
            with pytest.raises(ValueError, match='lifetime'):
                _require_action_context()
        with monkeypatch.context() as patch:
            patch.setattr(context_module.threading, 'get_ident', lambda: -1)
            with pytest.raises(ValueError, match='lifetime'):
                _require_action_context()
        f.request.out.rename(tmp_path / 'retired-output')
        f.request.out.mkdir()
        with pytest.raises(ValueError, match='directory changed'):
            _require_action_context()


def test_context_cleanup_on_exception_and_next_invocation_isolated(managed_invocation):
    f = managed_invocation
    with pytest.raises(RuntimeError, match='failed action'):
        with _action_context_scope(f.request, f.bound):
            old = _require_action_context()
            raise RuntimeError('failed action')
    with pytest.raises(ValueError, match='managed host invocation'):
        _require_action_context()
    with _action_context_scope(replace(f.request, run_id='next-task'),
                               {**f.bound, 'task_id': 'next-task'}):
        assert _require_action_context().producer['task_id'] == 'next-task'
        with pytest.raises(ValueError, match='lifetime'):
            _ = old.producer


def test_generic_host_binds_retained_claim_at_existing_dispatch(tmp_path, monkeypatch):
    from astrid.core.execution.generic_host import GenericPackHost
    from tests.test_generic_host import FakeRuntime

    root = tmp_path / 'fixture'
    (root / 'actions').mkdir(parents=True)
    (root / 'actions/run.py').write_text('def run():\n    return {}\n')
    (root / 'pack.yaml').write_text(yaml.safe_dump({
        'schema_version': 3, 'id': 'fixture', 'name': 'Fixture', 'version': '1.0.0',
        'actions': {'producer': {'name': 'Producer', 'description': 'Managed producer fixture.',
            'invocation': {'kind': 'python', 'path': 'actions/run.py', 'function': 'run'},
            'inputs': [], 'outputs': [{'name': 'authoring_proposal', 'type': 'file',
                'path_template': '{out}/authoring-proposal.json', 'artifact_type': 'timeline/authoring-proposal'}],
            'isolation': {'mode': 'subprocess', 'network': False},
            'metadata': {'adapter_family': 'cpu', 'resource_keys': ['cpu'], 'project_scope': 'optional'}}}}))
    runtime = FakeRuntime()
    host = GenericPackHost(pack_roots=[root], client=runtime, executor_id='host-worker',
                           attempt_root=tmp_path / 'attempt')
    host.register()
    task = {'id': 'outer', 'capability': 'fixture.producer', 'project_id': 'p',
            'attempt_id': 'attempt', 'executor_id': 'host-worker', 'fence': 2, 'runtime_epoch': 1,
            'spec': {'spec': {'inputs': {}, 'runtime_dependencies': {'publication': {'admitted_target': {
                'project_id': 'p', 'timeline_id': 't', 'base_revision_id': 'r', 'base_publication_id': 'pub'}}}}}}
    runtime.tasks['outer'] = {'task': task}
    dispatched = []
    def dispatch(**kwargs):
        dispatched.append(kwargs)
        raise RuntimeError('dispatch observed without launching a worker')
    monkeypatch.setattr(host, 'invoke_capability', dispatch)
    with pytest.raises(RuntimeError, match='dispatch observed'):
        host.run_task({'task': task}, lease_token='lease')
    assert len(dispatched) == 1
    call = dispatched[0]
    assert {key: call['admission'][key] for key in context_module._PRODUCER_FIELDS} == {
        'task_id': 'outer', 'attempt_id': 'attempt', 'executor_id': 'host-worker',
        'fence': 2, 'runtime_epoch': 1}
    assert call['request']['out'] == str(tmp_path / 'attempt/outputs')
    assert call['admission']['admitted_target']['base_publication_id'] == 'pub'
    assert 'producer' not in call['request']['inputs']
    assert not runtime.settlements and not runtime.uploaded_objects



def test_ordinary_python_action_keeps_effective_kwargs_and_json_return(tmp_path, monkeypatch):
    from astrid.core.env_vars import ASTRID_INTERNAL_INVOCATION
    from astrid.core.execution.executor.registry import ExecutorRegistry
    from astrid.core.execution.executor.runner import run_executor

    root = tmp_path / 'ordinary'
    (root / 'actions').mkdir(parents=True)
    (root / 'actions/run.py').write_text('''
from astrid.core.execution.executor._action_context import _require_action_context

def run(value):
    try:
        _require_action_context()
    except ValueError:
        return {'value': value, 'proposal_context': False}
    raise AssertionError('ordinary action acquired producer context')
''')
    declaration = {'description': 'Ordinary Python action.',
        'invocation': {'kind': 'python', 'path': 'actions/run.py', 'function': 'run'},
        'inputs': [{'name': 'value', 'type': 'string', 'required': False, 'default': 'existing-default'}],
        'outputs': [], 'metadata': {'project_scope': 'optional'}}
    definition = action_executor_definition(SimpleNamespace(root=root, id='ordinary', version='1.0.0'),
                                             'run', declaration)
    admission = {'capability_digest': _capability_digest(definition.to_dict()),
                 'source_digest': _source_digest_for_roots((root,)),
                 'source_root': str(root), 'source_roots': [str(root)]}
    monkeypatch.setenv(ASTRID_INTERNAL_INVOCATION, '1')
    (tmp_path / 'outputs').mkdir()
    request = ExecutorRunRequest(definition.id, tmp_path / 'outputs', project='p',
                                 project_was_auto_resolved=True)
    result = run_executor(request, ExecutorRegistry([definition]), _admission=admission)
    assert result.ok and result.outputs == []
    assert result.payload == {'action_result': {'value': 'existing-default', 'proposal_context': False}}
    with pytest.raises(ValueError, match='managed host invocation'):
        _require_action_context()
