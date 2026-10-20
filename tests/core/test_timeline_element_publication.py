import base64
import copy
import hashlib
import json
from unittest.mock import Mock

import pytest

from astrid.core.element import project_packs as packs
from astrid.core.receipts.contract import CommandReceipt
from astrid.core.timeline.authoring_bundle import open_authoring_bundle
from astrid.sdk.contracts import DomainResult, ErrorObject
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline_elements import update_parent_element
from tests.core import test_project_packs

configured = test_project_packs.configured


def setup_owner(monkeypatch, configured):
    test_project_packs.seed()
    admitted = packs.admit_project_pack('realm', 'project')
    ref = {key: admitted['elements'][0]['descriptor'][key]
           for key in ('id', 'kind', 'packId', 'revision')}
    row = configured.rows[('project', admitted['documentId'])]
    row['project_id'] = 'project'
    pin = {'document_id': row['document_id'], 'version': row['version'],
           'content_digest': packs._json_digest(row['content'])}
    objects = {}
    for admission in row['content']['admissions']:
        descriptor = admission['snapshot_object']
        objects[descriptor['object_id']] = {
            **descriptor, 'bytes_base64': base64.b64encode(
                configured.media.read_bytes(descriptor['object_id'])).decode()}
    inputs = [({'pin': pin, 'document': {**row, 'project_id': 'project'}}, objects)]
    monkeypatch.setattr('astrid.sdk.timeline_elements.Documents', lambda client: configured)
    monkeypatch.setattr('astrid.sdk.timeline_elements.RemoteMedia', lambda client: configured.media)
    monkeypatch.setenv('ASTRID_RUNTIME_DATA_ROOT', str(packs.authoring_root().parent / 'outbox'))
    # Ack validation is covered by sync and the actual-service helper tests.
    monkeypatch.setattr('astrid.sdk.timeline.sync._ack',
                        lambda result, *args: (result['data'], result['receipt']))
    effect = {'id': 'effect', 'at': 0, 'track': 'V1', 'hold': 2, 'clipType': 'reveal',
              'elementRef': {'id': 'reveal', 'kind': 'effect', 'revision': 'draft-reveal'},
              'params': {'color': '#ff6b6b', 'seed': 15}, 'opaque': {'keep': [None, False]}}
    media = {'id': 'media', 'at': 0, 'track': 'V1', 'hold': 10, 'opaque': {'preserve': True}}
    clips = [effect, media]
    payload = {'clips': copy.deepcopy(clips), 'config': {
        'clips': copy.deepcopy(clips), 'output': {'fps': 30},
        'app': {'elements': {'reveal': {'source': 'legacy recovery bytes'}}, 'other': 'keep'},
        'bundle': {'transcriptReferences': {'associations': [{'id': 'saved'}]}}},
        'registry': {'assets': {}}, 'occurrences': []}
    digest = 'sha256:' + hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    bundle = open_authoring_bundle({'project_id': 'project', 'timeline_id': 'timeline',
        'revision_id': 'head', 'payload': payload, 'content_digest': digest},
        shot_revisions=[], internal_timeline_revisions=[])
    owner = Mock()
    owner._client._last_handshake = {'realm_id': 'realm', 'actor_id': 'author'}
    owner.open_composition.return_value = DomainResult.success({
        'native_inspection': {'project_id': 'project', 'timeline_id': 'timeline'},
        'summary': {'head_revision_id': 'head'}})
    owner.open_bundle.return_value = DomainResult.success({
        'bundle': bundle, 'project_id': 'project', 'timeline_id': 'timeline',
        'head_revision_id': 'head', 'revision_id': 'head'})
    owner.history.return_value = DomainResult.success({
        'head': {'revision_id': 'head', 'publication_id': 'publication'},
        'items': [], 'next_cursor': None})

    def commit(project, timeline, body, **kwargs):
        plan = execute(bundle, body['commands'], schema_inputs=inputs, realm_id='realm')
        data = {'accepted_revision_id': 'committed', 'canonical_document': {
            'parent_revision': {'payload': plan.bundle['parent']}}}
        receipt = CommandReceipt('accepted-receipt', 'timeline.commit', kwargs['idempotency_key'],
                                 'hash', project, (1, 1), (), data, '2026-10-20T00:00:00Z')
        return DomainResult.success(data, receipt=receipt, idempotency_key=kwargs['idempotency_key'])

    owner.schema_inputs = inputs
    owner.commit.side_effect = commit
    return owner, bundle, ref


def update(owner, ref, **kwargs):
    return update_parent_element(owner, 'project', 'timeline', realm='realm', clip_id='effect',
                                 element=ref, expected_head='head', **kwargs)


def test_sameclip_exacthead_publication_preserves_closure_and_user_params(monkeypatch, configured):
    owner, bundle, ref = setup_owner(monkeypatch, configured)
    original = copy.deepcopy(bundle)
    result = update(owner, ref, duration=6, params={'chaos': .8}, idempotency_key='edit-element')
    assert result.ok, result.error
    body = owner.commit.call_args.args[2]
    assert body['base_revision_id'] == 'head' and body['base_publication_id'] == 'publication'
    assert [c['op'] for c in body['commands']] == ['clip.set-element', 'clip.set', 'clip.set-params']
    assert body['commands'][0]['args'] == {
        'elementRef': ref, 'schema_source': body['commands'][2]['args']['schema_source']}
    assert body['commands'][1]['args'] == {'values': {'hold': 6}, 'clear': []}
    assert body['commands'][2]['args']['values'] == {'chaos': .8}
    assert body['commands'][2]['args']['schema_source']['document_id'] in {
        document for project, document in configured.rows}
    assert owner.commit.call_args.kwargs == {'idempotency_key': 'edit-element'}
    assert result.data == {
        'project_id': 'project', 'timeline_id': 'timeline', 'expected_head': 'head',
        'new_head': 'committed', 'clip_id': 'effect', 'element': ref, 'duration': 6,
        'params': {'color': '#ff6b6b', 'seed': 15, 'chaos': .8}, 'before': {
            'element': original['parent']['clips'][0]['elementRef'], 'duration': 2,
            'params': {'color': '#ff6b6b', 'seed': 15}}}
    assert result.receipt.receipt_id == 'accepted-receipt'
    assert result.idempotency_key == 'edit-element'
    # Mirrors are compiler projections. This helper never patches or prunes them.
    plan = execute(bundle, body['commands'][:2], schema_inputs=owner.schema_inputs, realm_id='realm')
    assert plan.bundle['parent']['clips'][1] == bundle['parent']['clips'][1]
    assert plan.bundle['parent']['clips'][0]['opaque'] == {'keep': [None, False]}
    config = plan.bundle['parent']['config']
    assert config['clips'] == plan.bundle['parent']['clips']
    assert {k: v for k, v in config.items() if k != 'clips'} == {
        k: v for k, v in bundle['parent']['config'].items() if k != 'clips'}
    assert plan.bundle['parent']['registry'] == bundle['parent']['registry']
    assert bundle == original
    owner._typed.assert_not_called()


def test_stale_head_and_concurrent_cas_reject_without_rebase(monkeypatch, configured):
    owner, _, ref = setup_owner(monkeypatch, configured)
    stale = update_parent_element(owner, 'project', 'timeline', realm='realm', clip_id='effect',
                                  element=ref, expected_head='stale')
    assert not stale.ok and stale.error.code == 'conflict'
    owner.commit.assert_not_called()
    owner.commit.return_value = DomainResult.failure(ErrorObject('conflict', 'CAS rejected', {}))
    owner.commit.side_effect = None
    rejected = update(owner, ref, duration=6)
    assert not rejected.ok and rejected.error.code == 'conflict'
    assert owner.commit.call_count == 1
    owner._typed.assert_not_called()


@pytest.mark.parametrize('duration', [0, -1, float('inf'), float('nan'), True])
def test_bad_duration_never_publishes(monkeypatch, configured, duration):
    owner, _, ref = setup_owner(monkeypatch, configured)
    result = update(owner, ref, duration=duration)
    assert not result.ok
    owner.commit.assert_not_called()


def test_unadmitted_owner_and_sourceclip_reject(monkeypatch, configured):
    owner, bundle, ref = setup_owner(monkeypatch, configured)
    result = update(owner, {**ref, 'packId': 'unadmitted'})
    assert not result.ok
    owner.commit.assert_not_called()
    bundle['parent']['clips'][0]['asset'] = 'source'
    result = update(owner, ref)
    assert not result.ok
    owner.commit.assert_not_called()


@pytest.mark.parametrize('field', ['elementRef', 'element_ref'])
def test_element_only_and_same_revision_keep_unknown_props(monkeypatch, configured, field):
    owner, bundle, ref = setup_owner(monkeypatch, configured)
    clip = bundle['parent']['clips'][0]
    clip.pop('elementRef')
    clip[field] = ref
    clip['params']['future'] = {'literal': [None, {}, False]}
    result = update(owner, ref)
    assert result.ok, result.error
    assert result.data['duration'] == 2 and result.data['params'] == clip['params']
    calls = owner.commit.call_args.args[2]['commands']
    assert [c['op'] for c in calls] == ['clip.set-element']
    assert calls[0]['args']['schema_source']
    plan = execute(bundle, calls, schema_inputs=owner.schema_inputs, realm_id='realm')
    assert all(write['path'][0] != 'params' for record in plan.records for write in record['writes'])


@pytest.mark.parametrize('params', [{'seed': float('nan')}, {'seed': object()}, [], {'large': 'x' * 16385}])
def test_invalid_json_params_refuse_before_commit(monkeypatch, configured, params):
    owner, _, ref = setup_owner(monkeypatch, configured)
    result = update(owner, ref, params=params)
    assert not result.ok and result.error.code == 'validation_error'
    owner.commit.assert_not_called()


@pytest.mark.parametrize('params', [None, {}])
@pytest.mark.parametrize('existing', [None, {}])
def test_element_only_without_existing_params(monkeypatch, configured, params, existing):
    owner, bundle, ref = setup_owner(monkeypatch, configured)
    clip = bundle['parent']['clips'][0]
    clip.pop('params')
    if existing is not None:
        clip['params'] = existing
    result = update(owner, ref, params=params)
    assert result.ok, result.error
    assert result.data['params'] == {}
    calls = owner.commit.call_args.args[2]['commands']
    assert [call['op'] for call in calls] == ['clip.set-element']
    plan = execute(bundle, calls, schema_inputs=owner.schema_inputs, realm_id='realm')
    assert ('params' in plan.bundle['parent']['clips'][0]) == (existing is not None)
    assert all(write['path'][0] != 'params' for record in plan.records for write in record['writes'])


def test_invalid_known_param_is_validated_in_native_commit(monkeypatch, configured):
    owner, _, ref = setup_owner(monkeypatch, configured)
    result = update(owner, ref, params={'seed': 'invalid number'})
    assert not result.ok and result.error.code == 'validation_error'
    owner.commit.assert_not_called()
    owner._typed.assert_not_called()


@pytest.mark.parametrize('params', [None, {}, {'seed': 8}])
def test_wrong_revision_cannot_use_an_admitted_sibling_schema(monkeypatch, configured, params):
    owner, _, ref = setup_owner(monkeypatch, configured)
    result = update(owner, {**ref, 'revision': 'sha256:' + '0' * 64}, params=params)
    assert not result.ok and result.error.code == 'validation_error'
    owner.commit.assert_not_called()


def test_history_head_race_never_submits(monkeypatch, configured):
    owner, _, ref = setup_owner(monkeypatch, configured)
    owner.history.return_value = DomainResult.success({
        'head': {'revision_id': 'new-head', 'publication_id': 'new-publication'},
        'items': [], 'next_cursor': None})
    result = update(owner, ref, params={'seed': 8})
    assert not result.ok and result.error.code == 'conflict'
    owner.commit.assert_not_called()


@pytest.mark.parametrize('clear_params', [['seed', 'seed'], ['seed'], [None], 'seed'])
def test_invalid_clear_params_never_submits(monkeypatch, configured, clear_params):
    owner, _, ref = setup_owner(monkeypatch, configured)
    result = update(owner, ref, params={'seed': 8}, clear_params=clear_params)
    assert not result.ok and result.error.code == 'validation_error'
    owner.commit.assert_not_called()


def test_snapshot_read_failure_preserves_public_error(monkeypatch, configured):
    from astrid.sdk.exceptions import ServiceNotFoundError

    owner, _, ref = setup_owner(monkeypatch, configured)
    error = ServiceNotFoundError('Snapshot unavailable', details={'reason': 'missing_object'})
    monkeypatch.setattr(configured.media, 'read_bytes', Mock(side_effect=error))
    result = update(owner, ref, idempotency_key='missing-snapshot')
    assert not result.ok and result.error == error.to_error_object()
    assert result.idempotency_key == 'missing-snapshot'
    owner.commit.assert_not_called()
