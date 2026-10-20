"""Original requester inputs reach the registered assembler, with no worker authority."""
from __future__ import annotations

import copy
import json
from types import SimpleNamespace

import pytest

from astrid.core.execution.generic_host import GenericPackHost, HostError
from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.sdk.test_timeline_sync import Client, Generated

DIGEST = 'sha256:' + 'a' * 64


def requester(tmp_path, *, duplicate_cas=False):
    generated = Generated(tmp_path / 'outbox.json')
    client = Client(generated)
    outputs, associations, media, verified = [], {}, {}, {}
    calls = []
    for index in range(2):
        object_id = 'sha256:' + str(1 if duplicate_cas else index + 1) * 64
        selector = {'association_id': f'assoc-{index}', 'object_id': object_id, 'version': 1}
        outputs.append(selector)
        associations[selector['association_id']] = {
            **selector, 'task_id': f'child-{index}', 'project_id': 'p', 'durability': 'durable',
            'role': 'primary', 'lifecycle': {'state': 'available', 'version': 1},
            'media_type': 'video/mp4', 'size': 12}
        pin = {'asset': f'v-{index}', 'generation_id': f'g-{index}', 'variant_id': f'v-{index}',
               'object_id': object_id, 'catalog_digest': DIGEST}
        media[selector['association_id']] = pin
        verified[pin['variant_id']] = {'selection': pin, 'media_type': 'video/mp4',
                                     'size': 12, 'duration_seconds': index + 1.0}

    generated.get_managed_output = lambda association_id: copy.deepcopy(associations[association_id])
    generated.get_project_media_selection = lambda project, selector: copy.deepcopy(media[selector['association_id']])
    generated.get_project_verified_media = lambda project, selection: copy.deepcopy(verified[selection['variant_id']])

    def prepare(**body):
        return DomainResult.success({
            'capability_id': body['capability'], 'capability_digest': body['capability_digest'],
            'project_id': body['project_id'], 'schema_version': '1', 'spec': body['spec'],
            'input_object_ids': body['input_manifest'], 'storage_estimate': body['storage_estimate'],
            'idempotency_key': body['idempotency_key']})

    def dispatch(arguments):
        body = {'capability': arguments['capability_id'], 'input_manifest': arguments['input_object_ids'],
                **{key: arguments[key] for key in ('project_id', 'capability_digest', 'spec',
                                                  'storage_estimate', 'idempotency_key')}}
        flight = json.loads(generated.path.read_bytes())['flight']
        assert flight['kind'] == 'assembly-admission' and flight['key'] == body['idempotency_key']
        calls.append(copy.deepcopy(body))
        return DomainResult.success({'task_id': 'assembler'})

    client.tasks = SimpleNamespace(prepare_admission=prepare, dispatch_admission=dispatch)
    session = TimelineSession.open('p', 't', client=client, outbox_path=generated.path)
    return session, generated, outputs, associations, calls


def admit(session, outputs):
    return session.admit_assembly(outputs, replace_clips=['parent/clip:a', 'parent/clip:b'],
                                 assembler_digest=DIGEST, idempotency_key='assembly')


@pytest.mark.parametrize('duplicate_cas', [False, True])
def test_registered_admission_freezes_original_pair_closure_and_ordered_associations(tmp_path, duplicate_cas):
    session, generated, outputs, associations, calls = requester(tmp_path, duplicate_cas=duplicate_cas)
    # Peer advances after the authorized session selected its original base.
    generated.head = {'revision_id': 'peer', 'publication_id': 'peer-publication'}
    before = generated.path.read_bytes()
    assert admit(session, outputs)['data']['task_id'] == 'assembler'
    body, = calls
    assert body['capability'] == 'rendering.assemble_timeline'
    assert body['input_manifest'] == []
    spec = body['spec']
    assert spec['outputs'] == {'authoring_proposal': {'type': 'file', 'artifact_type': 'timeline/authoring-proposal'}}
    capture = spec['inputs']['resolved_children']
    target = {'project_id': 'p', 'timeline_id': 't', 'base_revision_id': 'r0', 'base_publication_id': 'pub0'}
    assert spec['runtime_dependencies']['publication']['admitted_target'] == capture['admitted_target'] == target
    assert capture['bundle'] == generated.bundles['r0']
    assert capture['replace_clips'] == ['parent/clip:a', 'parent/clip:b']
    assert [child['association'] for child in capture['children']] == outputs
    assert [child['media']['variant_id'] for child in capture['children']] == ['v-0', 'v-1']
    assert spec['runtime_dependencies']['aggregation']['order'] == [row['object_id'] for row in outputs]
    assert [edge['from_task_id'] for edge in spec['runtime_dependencies']['edges']] == ['child-0', 'child-1']
    assert generated.path.read_bytes() == before
    assert session.client.reads == ['r0']
    # Response/fixture edits cannot mutate the detached task body.
    outputs[0]['version'] = 2
    associations['assoc-0']['object_id'] = DIGEST
    generated.bundles['r0']['parent']['clips'][0]['hold'] = 20
    assert capture['children'][0]['association']['version'] == 1
    assert capture['bundle']['parent']['clips'][0]['hold'] == 1
    assert 'actor' not in json.dumps(spec) and 'credential' not in json.dumps(spec)


@pytest.mark.parametrize('change', ['foreign', 'object', 'version', 'role', 'durability', 'state', 'same_child'])
def test_admission_refuses_inexact_child_without_admitting(tmp_path, change):
    session, generated, outputs, associations, calls = requester(tmp_path)
    association = associations['assoc-1']
    if change == 'foreign':
        association['project_id'] = 'other'
    elif change == 'object':
        association['object_id'] = DIGEST
    elif change == 'version':
        association['lifecycle']['version'] = 2
    elif change == 'state':
        association['lifecycle']['state'] = 'superseded'
    elif change == 'same_child':
        association['task_id'] = 'child-0'
    else:
        association[change] = 'ineligible'
    before = generated.path.read_bytes()
    with pytest.raises((TimelineEditError, ValueError)):
        admit(session, outputs)
    assert not calls and generated.path.read_bytes() == before


def test_missing_registered_variant_refuses_without_fabricating_media(tmp_path):
    session, generated, outputs, _, calls = requester(tmp_path)

    def unavailable(*args):
        from astrid_runtime_client import ApiError
        raise ApiError(404, 'not_found', 'output has no authoritative registered variant')

    generated.get_project_media_selection = unavailable
    with pytest.raises(WorkspaceClientError, match='registered variant'):
        admit(session, outputs)
    assert not calls


def test_changed_outbox_during_capture_refuses_original_admission(tmp_path):
    session, generated, outputs, _, calls = requester(tmp_path)
    read = generated.get_project_verified_media

    def changed(*args):
        session.queue_move('parent/clip:a', 5)
        return read(*args)

    generated.get_project_verified_media = changed
    with pytest.raises(TimelineEditError, match='outbox changed'):
        admit(session, outputs)
    assert not calls
    assert json.loads(generated.path.read_bytes())['pending']


@pytest.mark.parametrize('replacement', [[], ['parent/clip:b', 'parent/clip:a']])
def test_replacement_is_explicit_original_membership(tmp_path, replacement):
    session, _, outputs, _, calls = requester(tmp_path)
    with pytest.raises(TimelineEditError, match='explicit original'):
        session.admit_assembly(outputs, replace_clips=replacement, assembler_digest=DIGEST, idempotency_key='assembly')
    assert not calls


def test_pending_intent_prevents_assembly_admission(tmp_path):
    session, _, outputs, _, calls = requester(tmp_path)
    session.queue_move('parent/clip:a', 5)
    with pytest.raises(TimelineEditError, match='flush pending'):
        admit(session, outputs)
    assert not calls


@pytest.mark.parametrize('duplicate_cas', [False, True])
def test_owned_host_materializes_detached_capture_beside_runtime_children(tmp_path, duplicate_cas):
    session, _, outputs, _, calls = requester(tmp_path, duplicate_cas=duplicate_cas)
    admit(session, outputs)
    body, = calls
    public = body['spec']
    public['runtime_dependencies']['resolved_children'] = [
        {'task_id': f'child-{index}', 'ordinal': index, 'outputs': [
            {'digest': selector['object_id'], 'role': 'primary', 'is_primary': True,
             'media_type': 'video/mp4', 'duration_seconds': index + 1.0}]}
        for index, selector in reversed(list(enumerate(outputs)))]
    spec = {'spec': public, 'input_object_ids': list(dict.fromkeys(row['object_id'] for row in outputs))}
    host = GenericPackHost(pack_roots=[])
    try:
        values = host._materialize_inputs(spec, tmp_path / 'attempt', continuation_id='assembler')
        materialized = json.loads(open(values['resolved_children']).read())
        assert materialized['capture'] == public['inputs']['resolved_children']
        assert materialized['resolved_children'] == public['runtime_dependencies']['resolved_children']
        assert materialized['aggregation']['order'] == [row['object_id'] for row in outputs]
        from astrid.packs.rendering.actions.assemble_timeline.run import build_authoring_proposal
        assembled = build_authoring_proposal(materialized)
        assert [row['task_id'] for row in assembled['children']] == ['child-0', 'child-1']
        assert len({row['id'] for row in assembled['timeline']['clips']}) == 2
        assert len({row['asset'] for row in assembled['timeline']['clips']}) == 2
        public['inputs']['resolved_children']['admitted_target']['base_revision_id'] = 'peer'
        assert materialized['capture']['admitted_target']['base_revision_id'] == 'r0'
        with pytest.raises(HostError, match='immutable admitted target'):
            host._materialize_inputs(spec, tmp_path / 'other-attempt', continuation_id='assembler')
    finally:
        host.shutdown()


def test_native_protocol_requires_immutable_declaration_and_keeps_stitch_aliases(tmp_path):
    from astrid.core.contracts.runtime_orchestration import (
        STITCH_CAPABILITIES,
        OrchestrationContractError,
        is_native_assembler_spec,
    )

    session, _, outputs, _, calls = requester(tmp_path)
    session.admit_assembly(outputs, replace_clips=['parent/clip:a', 'parent/clip:b'],
                           assembler_digest=DIGEST, idempotency_key='assembly', rationale='Café 1.0')
    spec = calls[0]['spec']
    assert spec['inputs']['resolved_children']['rationale'] == 'Café 1.0'
    assert is_native_assembler_spec(spec)
    assert STITCH_CAPABILITIES == {'travel_stitch': 'rendering.render', 'join_final_stitch': 'rendering.render'}
    assert not is_native_assembler_spec({'capability_id': 'rendering.render'})
    assert not is_native_assembler_spec({'capability_id': 'rendering.assemble_timeline'})
    del spec['outputs']['authoring_proposal']
    with pytest.raises(OrchestrationContractError, match='proposal declaration'):
        is_native_assembler_spec(spec)


def test_native_host_owns_attempt_identity_and_reads_exact_associations(tmp_path):
    from dataclasses import make_dataclass

    session, _, outputs, associations, calls = requester(tmp_path, duplicate_cas=True)
    admit(session, outputs)
    public = calls[0]['spec']
    # Admitted user JSON cannot supply the host's producer identity.
    public['inputs']['resolved_children']['producer'] = {'task_id': 'forged'}
    public['runtime_dependencies']['resolved_children'] = []
    reads = []

    def read(association_id):
        reads.append(association_id)
        row = copy.deepcopy(associations[association_id])
        # The generated client returns dataclasses, rather than JSON mappings.
        return make_dataclass('Association', list(row))(**row)

    host = GenericPackHost(pack_roots=[], client=SimpleNamespace(child_output=read))
    producer = {'task_id': 'assembler', 'attempt_id': 'attempt', 'executor_id': 'host',
                'fence': 2, 'runtime_epoch': 3}
    try:
        values = host._materialize_inputs({'spec': public}, tmp_path / 'attempt',
                                         continuation_id='assembler', producer_identity=producer)
        envelope = json.loads(open(values['resolved_children']).read())
        assert envelope['producer'] == producer
        assert envelope['associations'] == [associations[row['association_id']] for row in outputs]
        assert reads == ['assoc-0', 'assoc-1']
    finally:
        host.shutdown()


def test_registered_admission_lost_ack_restart_retries_original_body_without_recapture(tmp_path, monkeypatch):
    session, generated, outputs, _, calls = requester(tmp_path)
    dispatch = session.client.tasks.dispatch_admission

    def lose_ack(arguments):
        result = dispatch(arguments)
        if len(calls) == 1:
            raise WorkspaceClientError(0, 'transport_error', 'lost admission acknowledgement')
        return result

    session.client.tasks.dispatch_admission = lose_ack
    with pytest.raises(WorkspaceClientError, match='lost admission'):
        admit(session, outputs)
    original = copy.deepcopy(calls[0])
    generated.bundles['peer'] = copy.deepcopy(generated.bundles['r0'])
    generated.bundles['peer']['base_parent']['revision_id'] = 'peer'
    generated.bundles['peer']['parent']['clips'][0]['params']['text'] = 'Peer edit'
    generated.head = {'revision_id': 'peer', 'publication_id': 'peer-publication'}

    def no_recapture(*args, **kwargs):
        raise AssertionError('admission recovery reread the head or child media')

    monkeypatch.setattr(session.client.timelines, 'open_composition', no_recapture)
    monkeypatch.setattr(session.client.timelines, 'history', no_recapture)
    monkeypatch.setattr(session.client.tasks, 'prepare_admission', no_recapture)
    for name in ('get_managed_output', 'get_project_media_selection', 'get_project_verified_media'):
        monkeypatch.setattr(generated, name, no_recapture)
    restarted = TimelineSession.open('p', 't', client=session.client, outbox_path=generated.path)
    assert admit(restarted, outputs)['data']['task_id'] == 'assembler'
    assert calls == [original, original]
    assert session.client.reads == ['r0']


@pytest.mark.parametrize('change', ['key', 'digest', 'children', 'version_type', 'order', 'replacement', 'rationale'])
def test_admission_retry_refuses_changed_intent_without_losing_flight(tmp_path, change):
    session, generated, outputs, _, calls = requester(tmp_path)
    dispatch = session.client.tasks.dispatch_admission

    def lose_ack(arguments):
        dispatch(arguments)
        raise WorkspaceClientError(0, 'transport_error', 'lost admission acknowledgement')

    session.client.tasks.dispatch_admission = lose_ack
    with pytest.raises(WorkspaceClientError):
        admit(session, outputs)
    saved = generated.path.read_bytes()
    args = {'replace_clips': ['parent/clip:a', 'parent/clip:b'],
            'assembler_digest': DIGEST, 'idempotency_key': 'assembly'}
    if change == 'key':
        args['idempotency_key'] = 'other'
    elif change == 'digest':
        args['assembler_digest'] = 'sha256:' + 'b' * 64
    elif change == 'children':
        outputs[0]['version'] = 2
    elif change == 'version_type':
        outputs[0]['version'] = 1.0
    elif change == 'order':
        outputs.reverse()
    elif change == 'replacement':
        args['replace_clips'].reverse()
    else:
        args['rationale'] = 'Other intent'
    restarted = TimelineSession.open('p', 't', client=session.client, outbox_path=generated.path)
    with pytest.raises(TimelineEditError, match='immutable'):
        restarted.admit_assembly(outputs, **args)
    assert generated.path.read_bytes() == saved and len(calls) == 1
    assert session.client.reads == ['r0']


def test_admission_fsync_failure_prevents_post(tmp_path, monkeypatch):
    from astrid.sdk.timeline import outbox

    session, generated, outputs, _, calls = requester(tmp_path)
    before = generated.path.read_bytes()

    def fail(descriptor):
        raise OSError('fsync failed')

    monkeypatch.setattr(outbox.os, 'fsync', fail)
    with pytest.raises(OSError, match='fsync failed'):
        admit(session, outputs)
    assert not calls and generated.path.read_bytes() == before
    assert not list(generated.path.parent.glob('.outbox-*'))


def test_admission_ack_cleanup_failure_retains_original_flight_and_base(tmp_path, monkeypatch):
    session, generated, outputs, _, calls = requester(tmp_path)
    before = session.outbox.read()
    write = session.outbox.write

    def fail_cleanup(state):
        if state['flight'] is None:
            raise OSError('crash before cleanup')
        write(state)

    monkeypatch.setattr(session.outbox, 'write', fail_cleanup)
    with pytest.raises(OSError, match='crash before cleanup'):
        admit(session, outputs)
    flight = session.outbox.read()['flight']
    saved = generated.path.read_bytes()
    for operation in (lambda: session.undo(['pub0']), lambda: session.flush()):
        with pytest.raises(TimelineEditError, match='original assembly admission'):
            operation()
        assert generated.path.read_bytes() == saved
    pending = session.queue_move('parent/clip:a', 5)
    assert session.outbox.read()['flight'] == flight
    assert session.outbox.read()['base'] == before['base']
    # Neither changed credentials for the same actor nor an instance restart is
    # local authority; only the authenticated realm/actor scope owns this file.
    transport = session.client._remote._transport
    handshake = transport._last_handshake
    transport._last_handshake = {**handshake, 'actor_id': 'other'}
    with pytest.raises(TimelineEditError):
        TimelineSession.open('p', 't', client=session.client, outbox_path=generated.path)
    transport._last_handshake = handshake
    restarted = TimelineSession.open('p', 't', client=session.client, outbox_path=generated.path)

    def no_recapture(*args, **kwargs):
        raise AssertionError('retry rebuilt admission')

    monkeypatch.setattr(restarted.client.tasks, 'prepare_admission', no_recapture)
    monkeypatch.setattr(restarted, '_bundle', no_recapture)
    assert admit(restarted, outputs)['data']['task_id'] == 'assembler'
    assert calls[0] == calls[1]
    assert restarted.outbox.read() == {**before, 'pending': [pending]}
    assert flight['key'] == 'assembly'
