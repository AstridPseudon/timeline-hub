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

    def create(**body):
        calls.append(copy.deepcopy(body))
        return DomainResult.success({'task_id': 'assembler'})

    client.tasks = SimpleNamespace(create=create)
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
