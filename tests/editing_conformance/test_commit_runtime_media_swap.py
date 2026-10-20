"""Held existing-slot swap through real Runtime reads, provider and acceptance.

Run with ASTRID_RUNTIME_CHECKOUT set and pytest -m integration. No sockets,
synthetic accepted records, direct SQL writes or generated schema overrides.
"""
from __future__ import annotations

import copy
import hashlib
from types import SimpleNamespace

import pytest

from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration
TARGET = 'parent/clip:picture'


@pytest.fixture(params=['image', 'video'])
def editing(request, tmp_path, monkeypatch):
    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / 'tests'))
    from runtime_protocol import timeline_commit_port
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.timeline_commit_port import RequestCommitPort
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_validation import validate_commit_value
    from test_generation_publish_v1_settlement import _effect, _fixture, _output, _settle

    kind = request.param

    def effect(project):
        value = _effect(project, groups=[{'group_key': 'main', 'selectors': [
            {'selector': name, 'ordinal': index, 'variant_key': name, 'output_port': kind}
            for index, name in enumerate(('old', 'new'))]}])
        value['payload']['metadata'] = {'prompt': 'bounded swap source',
                                       'params': {'duration_seconds': 6} if kind == 'video' else {}}
        return value

    # Observe the real public read's fingerprint input without replacing it.
    fingerprint_inputs = []
    real_digest = timeline_commit_port.digest

    def digest(value):
        result = real_digest(value)
        if isinstance(value, dict) and {'generation', 'variant', 'entry'} <= value.keys():
            fingerprint_inputs.append((copy.deepcopy(value), result))
        return result

    monkeypatch.setattr(timeline_commit_port, 'digest', digest)
    service, project, task, attempt, admitted = _fixture(tmp_path, effect_factory=effect)
    project = project['id']
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('media-editor', ['projects:read', 'projects:write'])

    def authorize():
        return credentials.require(token, 'projects:write')

    try:
        outputs = [
            _output(name.encode(), output_port=kind, group_key='main', variant_key=name,
                    ordinal=index, filename=name + ('.mp4' if kind == 'video' else '.png'),
                    media_type=kind + ('/mp4' if kind == 'video' else '/png'))
            for index, name in enumerate(('old', 'new'))]
        _settle(service, attempt, outputs, effect=admitted)
        associations = service.managed_outputs(task['task']['id'])
        pins = []
        for association in associations:
            pin = service.get_project_media_selection(project, {
                'association_id': association['association_id'],
                'object_id': association['object_id'], 'version': association['lifecycle']['version'],
            }, authorize=authorize)
            validate_commit_value(pin, 'MediaSelection')
            pins.append(pin)
        by_name = {row['variant_key']: pin for row, pin in zip(associations, pins)}
        old, new = by_name['old'], by_name['new']
        parent = {
            'config': {'output': {'fps': 24}, 'tracks': [{'id': 'visual', 'kind': 'visual'}]},
            'registry': {'assets': {pin['asset']: {
                'media_id': pin['object_id'], 'type': kind,
                'generationId': pin['generation_id'], 'variantId': pin['variant_id'],
                'opaque': [None, False, {'keep': 0}],
            } for pin in pins}},
            'clips': [{'id': 'picture', 'clipType': kind, 'asset': old['asset'],
                       'track': 'visual', 'at': 1, 'hold': 2,
                       'opaque': {'ordered': [None, False, {}]},
                       **({'from': 2, 'to': 6, 'speed': 2} if kind == 'video' else {})}],
            'occurrences': [], 'opaque': [None, {'keep': True}],
        }
        service.publish_parent_composition(project, 'film', {
            'project_id': project, 'timeline_id': 'film', 'expected_head': None,
            'parent_revision_id': 'swap-baseline', 'parent_composition': parent,
        }, idempotency_key='swap-baseline')
        service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))

        selected, closures, candidates = [], [], []
        real_selected = RequestCommitPort.selected_media
        real_closure = RequestCommitPort.revision_closure
        real_accept = RequestCommitPort.accept

        def selected_media(port, pin):
            value = real_selected(port, pin)
            validate_commit_value(value, 'VerifiedMedia')
            selected.append(copy.deepcopy(value))
            return value

        def revision_closure(port, revision):
            value = real_closure(port, revision)
            closures.append(copy.deepcopy(value))
            return value

        state = SimpleNamespace(service=service, project=project, old=old, new=new,
                                associations=associations, selected=selected, closures=closures,
                                candidates=candidates, before_accept=None, credentials=credentials,
                                authorize=authorize, effect=effect, outputs=outputs,
                                fingerprint_inputs=fingerprint_inputs)

        def accept(port, prepared):
            candidates.append(copy.deepcopy(prepared))
            if state.before_accept:
                state.before_accept()
            return real_accept(port, prepared)

        monkeypatch.setattr(RequestCommitPort, 'selected_media', selected_media)
        monkeypatch.setattr(RequestCommitPort, 'revision_closure', revision_closure)
        monkeypatch.setattr(RequestCommitPort, 'accept', accept)
        yield state
    finally:
        service.close()


def body(editing, commands=None, *, dry_run=False):
    head = editing.service.get_project_timeline(editing.project, 'film')
    return {'api_version': 1, 'project_id': editing.project, 'timeline_id': 'film',
            'base_revision_id': head['head_revision_id'], 'base_publication_id': head['head_publication_id'],
            'commands': commands or [{'schema_version': 1, 'op': 'clip.swap-media', 'version': '1',
                                     'select': TARGET, 'args': {'old_media': editing.old, 'media': editing.new}}],
            'dry_run': dry_run, 'source': {'via': 'python'}}


def commit(editing, request, key):
    return editing.service.commit_timeline(
        editing.project, 'film', request, idempotency_key=key, publisher='media-editor',
        invocation_path=f'/v1/projects/{editing.project}/timelines/film/commit', authorize=editing.authorize,
    )


def rows(editing):
    return tuple(editing.service.store.conn.iterdump())


def foreign_pin(editing):
    from test_generation_publish_v1_settlement import CAPABILITY, _output, _settle

    service = editing.service
    project = service.create_project({'slug': 'foreign', 'name': 'Foreign'})['id']
    effect = editing.effect(project)
    task = service.create_task({
        'capability_id': CAPABILITY, 'capability_digest': 'sha256:' + hashlib.sha256(CAPABILITY.encode()).hexdigest(),
        'project': project, 'settlement_effect': effect, 'idempotency_key': 'foreign-task',
    })
    attempt = service.claim_next({'executor_id': 'publish-worker', 'capability_ids': [CAPABILITY],
                                 'runtime_epoch': service.health()['runtime_epoch']}, idempotency_key='foreign-claim')
    outputs = [_output(b'foreign-' + row['variant_key'].encode(), **{
        key: row[key] for key in ('output_port', 'group_key', 'variant_key', 'ordinal', 'filename', 'media_type')
    }) for row in editing.outputs]
    _settle(service, attempt, outputs, effect=effect, key='foreign-settle')
    association = service.managed_outputs(task['task']['id'])[0]
    return service.get_project_media_selection(project, {
        'association_id': association['association_id'], 'object_id': association['object_id'],
        'version': association['lifecycle']['version'],
    }, authorize=editing.authorize)


def test_real_selection_candidate_readback_and_inverse(editing):
    from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
    from astrid.sdk.timeline.native_media_commands import capture_swap_media

    before = rows(editing)
    preview = commit(editing, body(editing, dry_run=True), 'preview')
    assert preview['receipt'] is None
    assert rows(editing) == before
    original = editing.closures[0]
    baseline = editing.service.get_project_parent_composition_revision(editing.project, 'film', 'swap-baseline')
    assert {key: baseline[key] for key in original['parent_revision']} == original['parent_revision']
    command = capture_swap_media(bundle_from_document(original), TARGET, editing.old, editing.new,
                                 verified_media=editing.selected)
    assert preview['data']['commands'] == [command]
    assert [value['selection'] for value in editing.selected] == [editing.old, editing.new]
    if editing.selected[0]['media_type'] == 'video/mp4':
        assert [value['duration_seconds'] for value in editing.selected] == [6, 6]
        for pin in (editing.old, editing.new):
            generation = editing.service.get_generation(pin['generation_id'])
            assert generation['metadata']['params']['duration_seconds'] == 6
    request = body(editing, [command])
    accepted = commit(editing, request, 'swap')
    document = accepted['data']['canonical_document']
    assert document == preview['data']['canonical_document']
    assert document == editing.candidates[-1]['canonical_document']
    expected = copy.deepcopy(original['parent_revision']['payload'])
    expected['clips'][0]['asset'] = editing.new['asset']
    if 'clips' in expected['config']:
        expected['config']['clips'][0]['asset'] = editing.new['asset']
    assert document['parent_revision']['payload'] == expected
    record = editing.candidates[-1]['records']['commands'][0]
    assert record['command'] == command
    assert [dep['pin'] for dep in record['dependencies']] == [editing.old, editing.new]
    assert record['created'] == []
    stored = editing.service.get_project_parent_composition_revision(
        editing.project, 'film', accepted['data']['accepted_revision_id'])
    assert {key: stored[key] for key in document['parent_revision']} == document['parent_revision']
    assert stored['dependency_manifest'] == document['dependency_manifest']
    history = editing.service.list_timeline_commits(editing.project, 'film', authorize=lambda: None)
    edge = history['items'][-1]
    assert edge['receipt'] == accepted['receipt']
    assert accepted['receipt']['result'] == accepted['data']
    assert edge['records']['commands'] == [record]
    durable = rows(editing)
    assert commit(editing, request, 'swap') == accepted
    assert rows(editing) == durable
    undo = {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
            'args': {'publications': [accepted['receipt']['receipt_id']]}}
    restored = commit(editing, body(editing, [undo]), 'undo')
    assert restored['data']['canonical_document'] == original
    assert document_from_bundle(bundle_from_document(restored['data']['canonical_document'])) == original
    stored = editing.service.get_project_parent_composition_revision(
        editing.project, 'film', restored['data']['accepted_revision_id'])
    assert {key: stored[key] for key in original['parent_revision']} == original['parent_revision']
    head = editing.service.get_project_timeline(editing.project, 'film')
    assert head['head_revision_id'] == original['parent_revision']['revision_id']
    assert head['head_publication_id'] == restored['receipt']['receipt_id']


@pytest.mark.parametrize('side', ['old_media', 'media'])
@pytest.mark.parametrize('damage', ['stale', 'foreign', 'fingerprint'])
def test_invalid_exact_selection_refuses_without_any_writes(editing, side, damage):
    from runtime_protocol.errors import RuntimeErrorBase

    request = copy.deepcopy(body(editing))
    pin = request['commands'][0]['args'][side]
    if damage == 'stale':
        association = next(row for row in editing.associations if row['object_id'] == pin['object_id'])
        editing.service.update_managed_output_lifecycle(association['association_id'], {
            'operation': 'promote', 'expected_version': association['lifecycle']['version'],
        }, idempotency_key='promote-before-capture')
    elif damage == 'foreign':
        foreign = foreign_pin(editing)
        request['commands'][0]['args'][side] = foreign
        with pytest.raises(RuntimeErrorBase):
            editing.service.get_project_media_selection(editing.project, {
                key: foreign[key] for key in ('asset', 'generation_id', 'variant_id')
            }, authorize=editing.authorize)
    else:
        # Bytes alone are not the metadata/authority fingerprint, even for the
        # correct project, alias, generation, variant and immutable object.
        pin['catalog_digest'] = pin['object_id']
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, request, 'invalid-selection')
    if damage != 'foreign':
        assert error.value.message == 'selected media catalog digest changed'
    else:
        assert error.value.message == 'selected media is not a managed project generation/variant/object'
    assert editing.candidates == []
    assert rows(editing) == before


def test_source_metadata_is_part_of_the_exact_selection_fingerprint(editing):
    from runtime_protocol.errors import ConflictError
    from runtime_protocol.timeline_commit_port import digest

    pin = editing.new
    source, fingerprint = next((source, fingerprint) for source, fingerprint in editing.fingerprint_inputs
                               if source['variant_id'] == pin['variant_id'])
    metadata = editing.service.get_generation(pin['generation_id'])['metadata']
    assert source['generation']['metadata'] == metadata
    assert fingerprint == pin['catalog_digest'] == digest(source)
    # Corrupt only the source metadata in an observed hash input. The resulting
    # bad request pin must never authorize a different snapshot or any write.
    changed = copy.deepcopy(source)
    if 'duration_seconds' in metadata['params']:
        changed['generation']['metadata']['params']['duration_seconds'] = 5.999
    else:
        changed['generation']['metadata']['prompt'] = 'different source'
    wrong_fingerprint = digest(changed)
    assert wrong_fingerprint != fingerprint
    request = copy.deepcopy(body(editing))
    request['commands'][0]['args']['media']['catalog_digest'] = wrong_fingerprint
    before = rows(editing)
    with pytest.raises(ConflictError, match='selected media catalog digest changed'):
        commit(editing, request, 'source-fingerprint')
    assert editing.candidates == []
    assert rows(editing) == before


@pytest.mark.parametrize('side', ['old_media', 'media'])
@pytest.mark.parametrize('race', ['lifecycle', 'revocation'])
def test_capture_to_accept_races_refuse_atomically(editing, side, race):
    from runtime_protocol.errors import RuntimeErrorBase

    request = body(editing)
    pin = request['commands'][0]['args'][side]
    before_accept = None
    def interfere():
        nonlocal before_accept
        if race == 'lifecycle':
            association = next(row for row in editing.associations if row['object_id'] == pin['object_id'])
            editing.service.update_managed_output_lifecycle(association['association_id'], {
                'operation': 'promote', 'expected_version': association['lifecycle']['version'],
            }, idempotency_key='promote-at-accept')
        else:
            editing.credentials.revoke('media-editor')
        before_accept = rows(editing)

    editing.before_accept = interfere
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, request, 'race')
    assert error.value.message == ('selected media catalog digest changed' if race == 'lifecycle'
                                   else 'invalid bearer credential')
    assert [row['selection'] for row in editing.selected] == [editing.old, editing.new]
    assert len(editing.candidates) == 1
    assert before_accept == rows(editing)
