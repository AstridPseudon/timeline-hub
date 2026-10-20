"""Native ingress with the official client and Runtime handlers, without sockets."""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
from contextlib import contextmanager
from urllib.parse import parse_qs, urlsplit

import pytest
import yaml

from astrid.core.element import project_packs as packs
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.core import test_project_packs
from tests.editing_conformance.test_native_batch_ingress import cli, command
from tests.editing_conformance.test_native_batch_ingress import runtime as memory_runtime
from tests.helpers.runtime import use_runtime

pytestmark = [pytest.mark.integration, pytest.mark.parametrize('runtime', ['unpublished'], indirect=True)]
configured_project_pack = test_project_packs.configured
runtime = memory_runtime
OWNER = 'occurrence:occ-a'
REF = OWNER + '/clip:added'


@pytest.fixture(params=['image', 'video'])
def media(runtime, request, tmp_path, monkeypatch):
    root = use_runtime()
    monkeypatch.syspath_prepend(str(root / 'tests'))
    from test_generation_publish_v1_settlement import _effect, _output, _settle
    from timeline_commit_film_fixture import _binding_descriptor

    from tests.sdk.test_timeline_commit_provider_document import MEDIA, document_fixture

    service, project, kind = runtime.service(), runtime.project, request.param
    effect = _effect(project, groups=[{'group_key': 'main', 'selectors': [
        {'selector': name, 'ordinal': index, 'variant_key': name, 'output_port': kind}
        for index, name in enumerate(('old', 'new'))]}])
    effect['payload']['metadata']['params'] = {'duration_seconds': 6} if kind == 'video' else {}
    service.register_executor({'executor_id': 'media', 'capabilities': ['generation.publish.v1']},
                              idempotency_key='executor')
    task = service.create_task({'capability_id': 'generation.publish.v1',
                               'capability_digest': 'sha256:' + hashlib.sha256(b'generation.publish.v1').hexdigest(),
                               'project': project, 'settlement_effect': effect, 'idempotency_key': 'media-task'})
    attempt = service.claim_next({'executor_id': 'media', 'capability_ids': ['generation.publish.v1'],
                                  'runtime_epoch': service.health()['runtime_epoch']}, idempotency_key='claim')
    _settle(service, attempt, [_output(name.encode(), output_port=kind, group_key='main',
                                     variant_key=name, ordinal=index, filename=name + '.png',
                                     media_type=kind + ('/png' if kind == 'image' else '/mp4'))
                              for index, name in enumerate(('old', 'new'))], effect=effect)
    pins = [service.get_project_media_selection(project, {
        'association_id': a['association_id'], 'object_id': a['object_id'], 'version': a['lifecycle']['version']},
        authorize=lambda: None) for a in service.managed_outputs(task['task']['id'])]
    runtime.media_associations = service.managed_outputs(task['task']['id'])
    old, new = pins
    # A real authored occurrence with exact source revisions, not a client registry upsert.
    document = json.loads(json.dumps(document_fixture()).replace(MEDIA, old['object_id']))
    internal = document['internal_timeline_revisions'][0]
    internal['timeline_id'] = 'film'
    internal['payload'].pop('source_window')
    internal['payload']['output']['fps'] = 24
    internal['payload']['registry']['assets']['picture']['type'] = kind
    parent = document['parent_revision']['payload']
    parent['config']['output']['fps'] = 24
    for row in parent['occurrences']:
        row.update(source_offset=0, speed=1)
    service.create_project_shot(project, {'shot_id': 'chapter-shot', 'name': 'Chapter One'},
                                idempotency_key='chapter-shot')
    binding = service.set_project_shot_text_binding(project, {
        'shot_id': 'chapter-shot', 'kind': 'transcript', 'text': 'Chapter', 'expected_head': 0},
        idempotency_key='chapter-text')['data']
    document['shot_revisions'][0]['payload']['text_bindings'] = [_binding_descriptor(binding, 'Chapter')]
    service.publish_parent_composition(project, 'film', {
        'project_id': project, 'timeline_id': 'film', 'expected_head': None,
        'parent_revision_id': 'media-source', 'parent_composition': parent,
        'shot_revisions': [{k: v for k, v in row.items() if k != 'content_digest'}
                           for row in document['shot_revisions']],
        'internal_timeline_revisions': [{k: v for k, v in internal.items() if k != 'content_digest'}]},
        idempotency_key='media-source')
    runtime.restart()
    head = runtime.history()['head']
    runtime.base = {'base_revision_id': head['revision_id'], 'base_publication_id': head['publication_id']}
    row = {'id': 'added', 'clipType': kind, 'track': 'visual', 'asset': old['asset'], 'at': 0, 'hold': 1}
    if kind == 'video':
        row.update({'from': 0, 'to': 1})
    # Use the raw child track identity installed by the real source fixture.
    row['track'] = internal['payload']['tracks'][0]['id']
    runtime.media_commands = [command('occurrence.add-media', OWNER, {'row': row, 'media': old}),
                              command('occurrence.swap-media', REF, {'old_media': old, 'media': new})]
    runtime.media_pins = pins
    return runtime


def original(case):
    return case.client().timelines.open_bundle(case.project, 'film',
                                               revision_id=case.base['base_revision_id']).data['bundle']


def media_plan(case):
    transport = case.client()._remote._transport
    inputs = [transport.get_project_verified_media(case.project, pin) for pin in case.media_pins]
    return execute(original(case), case.media_commands, verified_media=inputs)


@pytest.mark.parametrize('entry', ['queue', 'commit', 'cli'])
@pytest.mark.parametrize('captured', [False, True])
def test_media_batch_raw_and_captured(media, tmp_path, capsys, entry, captured):
    plan = media_plan(media)
    calls = copy.deepcopy(plan.commands if captured else media.media_commands)
    frozen, count = copy.deepcopy(calls), len(media.history()['items'])
    media.input_reads.clear()
    if entry == 'cli':
        path = tmp_path / 'commands.json'
        path.write_text(json.dumps(calls))
        before = path.read_bytes()
        code, accepted = cli(media, capsys, path)
        assert code == 0, accepted
        assert path.read_bytes() == before
    else:
        session = media.session(base=media.base)
        if entry == 'queue':
            assert session.queue_many(calls) == plan.commands
            accepted = session.flush()
        else:
            accepted = session.commit_many(calls)
    assert calls == frozen
    assert accepted['data']['commands'] == plan.commands
    assert len(media.history()['items']) == count + 1
    assert [parse_qs(urlsplit(p).query) for p in media.input_reads] == [
        {k: [str(v)] for k, v in pin.items()} for pin in media.media_pins]
    state = State(bundle_from_document(accepted['data']['canonical_document']))
    assert state.entity(REF)['asset'] == media.media_pins[1]['asset']
    media.restart()
    undone = media.session(name='undo').undo([accepted['receipt']['receipt_id']])
    assert State(bundle_from_document(undone['data']['canonical_document'])).entity(REF, optional=True) is None


def test_media_pending_created_dependency_exact_retry_and_restart(media, tmp_path, monkeypatch):
    session = media.session(base=media.base)
    media.lost.add('media-A')
    with pytest.raises(WorkspaceClientError):
        session.commit(media.media_commands[0], idempotency_key='media-A')
    flight = copy.deepcopy(media.calls[-1])
    suffix = session.queue_many([media.media_commands[1]])
    assert suffix[0]['select'] == REF
    pending = json.loads(media.path.read_bytes())
    media.restart()
    session = media.session()

    def tripwire(*args, **kwargs):
        raise AssertionError('retry read capture inputs')

    with monkeypatch.context() as patch:
        transport = session.client._remote._transport
        patch.setattr(transport, 'get_project_verified_media', tripwire)
        patch.setattr(transport, 'get_document', tripwire)
        patch.setattr(transport, 'get_object', tripwire)
        patch.setattr(session, '_bundle', tripwire)
        session.commit(media.media_commands[0], idempotency_key='media-A')
    assert media.calls[-1] == flight
    assert json.loads(media.path.read_bytes())['pending'] == suffix
    assert json.loads(media.path.read_bytes())['flight'] is None
    assert pending['pending'][1:] == suffix
    accepted = session.flush()
    assert accepted['data']['commands'] == suffix


@pytest.mark.parametrize('failure', ['digest', 'missing', 'race', 'guard'])
def test_media_capture_refusal_preserves_pending_and_file(media, tmp_path, capsys, monkeypatch, failure):
    session = media.session(base=media.base)
    session.queue(media.media_commands[0])
    before = media.path.read_bytes()
    calls = [copy.deepcopy(media.media_commands[1])]
    if failure == 'digest':
        calls[0]['args']['media']['catalog_digest'] = 'sha256:' + '0' * 64
    elif failure == 'missing':
        calls[0]['args']['media']['object_id'] = 'sha256:' + '0' * 64
    elif failure == 'guard':
        calls = [media_plan(media).commands[1]]
        calls[0]['reads'][0]['state'] = {'state': 'present', 'value': 'changed-owner'}
    else:
        transport = session.client._remote._transport
        read = transport.get_project_verified_media

        def racing(*args):
            value = read(*args)
            if not media.calls:
                session.flush()  # One ACK while capture is outside the lock.
            return value

        monkeypatch.setattr(transport, 'get_project_verified_media', racing)
    with pytest.raises((TimelineEditError, WorkspaceClientError),
                       match='outbox changed during capture' if failure == 'race' else None):
        session.queue_many(calls)
    if failure == 'race':
        assert json.loads(media.path.read_bytes())['pending'] == []
    else:
        assert media.path.read_bytes() == before
    assert len(media.calls) == (1 if failure == 'race' else 0)


@pytest.fixture
def pack(runtime, configured_project_pack, monkeypatch):
    @contextmanager
    def connected():
        yield runtime.client()

    monkeypatch.setattr(packs, '_open_client', connected)
    service = runtime.service()
    service.create_timeline(runtime.project, 'film', idempotency_key='bootstrap')
    head = runtime.history()['head']
    runtime.base = {'base_revision_id': head['revision_id'], 'base_publication_id': head['publication_id']}
    root, directory, manifest = test_project_packs.seed(runtime.project)
    definition = yaml.safe_load((directory / 'element.yaml').read_text())
    definition['schema']['properties']['seed']['maximum'] = 10
    definition['defaults']['seed'] = 4
    (directory / 'element.yaml').write_text(yaml.safe_dump(definition))
    test_project_packs.add_second_element(root, directory, manifest)
    result = packs.admit_project_pack('realm', runtime.project)
    selected = next(row['descriptor'] for row in result['elements'] if row['descriptor']['id'] == 'reveal')
    selected = {k: selected[k] for k in ('id', 'kind', 'packId', 'revision')}
    transport = runtime.client()._remote._transport
    source = transport.get_document(runtime.project, result['documentId'])
    pin = {'document_id': source['document_id'], 'version': source['version'],
           'content_digest': _digest(source['content'])}
    runtime.pin, runtime.source, runtime.selected = pin, source, selected
    runtime.pack_commands = [
        command('track.create', 'parent', {'row': {'id': 'picture', 'kind': 'visual'}}),
        command('clip.add', 'parent', {'row': {
            'id': 'effect', 'clipType': 'reveal', 'elementRef': selected, 'track': 'picture', 'at': 0,
            'hold': 1, 'params': {'seed': 4, 'unknown': [None, False, {}]}}}),
        command('clip.set-params', 'parent/clip:effect', {
            'values': {'seed': 8, 'future': {'keep': [None, False]}}, 'clear': [], 'schema_source': pin})]
    runtime.descriptor = next(a['snapshot_object'] for a in source['content']['admissions']
                              if a['id'] == selected['id'])
    # Deleting workstation inputs cannot affect native capture authority.
    shutil.rmtree(root)
    shutil.rmtree(packs.artifact_root())
    return runtime


def pack_plan(case):
    import base64

    transport = case.client()._remote._transport
    data = transport.get_object(case.descriptor['object_id'])['data']
    snapshots = {case.descriptor['object_id']: {
        **case.descriptor, 'bytes_base64': base64.b64encode(data).decode('ascii')}}
    return execute(original(case), case.pack_commands, realm_id='realm',
                   schema_inputs=[({'pin': case.pin, 'document': case.source}, snapshots)])


@pytest.mark.parametrize('entry', ['queue', 'commit', 'cli'])
@pytest.mark.parametrize('captured', [False, True])
def test_exact_pack_param_batch(pack, tmp_path, capsys, entry, captured):
    plan = pack_plan(pack)
    supplied = copy.deepcopy(plan.commands if captured else pack.pack_commands)
    frozen = copy.deepcopy(supplied)
    pack.input_reads.clear()
    if entry == 'cli':
        path = tmp_path / 'commands.json'
        path.write_text(json.dumps(supplied))
        before = path.read_bytes()
        code, accepted = cli(pack, capsys, path)
        assert code == 0, accepted
        assert path.read_bytes() == before
    else:
        session = pack.session(base=pack.base)
        if entry == 'queue':
            assert session.queue_many(supplied) == plan.commands
            accepted = session.flush()
        else:
            accepted = session.commit_many(supplied)
    assert supplied == frozen
    assert accepted['data']['commands'] == plan.commands
    assert len(pack.input_reads) == 2
    assert '/documents/' in pack.input_reads[0]
    assert pack.input_reads[1].endswith('/objects/' + pack.descriptor['object_id'].replace(':', '%3A'))
    state = State(bundle_from_document(accepted['data']['canonical_document']))
    assert state.entity('parent/clip:effect')['params'] == {
        'seed': 8, 'unknown': [None, False, {}], 'future': {'keep': [None, False]}}
    record = accepted['data']['commands'][-1]
    assert any(read['path'] == ['elementRef'] and read['state']['value'] == pack.selected
               for read in record['reads'])
    pack.restart()
    undone = pack.session(name='undo').undo([accepted['receipt']['receipt_id']])
    assert State(bundle_from_document(undone['data']['canonical_document'])).entity(
        'parent/clip:effect', optional=True) is None


@pytest.mark.parametrize('failure', ['invalid-value', 'old-version', 'digest', 'missing-admission', 'missing-object', 'guard'])
def test_pack_input_refusal_is_atomic(pack, tmp_path, capsys, failure):
    calls = copy.deepcopy(pack.pack_commands)
    if failure == 'invalid-value':
        calls[-1]['args']['values']['seed'] = 16
    elif failure == 'digest':
        calls[-1]['args']['schema_source']['content_digest'] = 'sha256:' + '0' * 64
    elif failure == 'guard':
        calls = copy.deepcopy(pack_plan(pack).commands)
        calls[-1]['reads'][0]['state'] = {'state': 'present', 'value': 'wrong'}
    elif failure == 'missing-object':
        pack.service().cas.path_for(pack.descriptor['object_id'].removeprefix('sha256:')).unlink()
        pack.restart()
    else:
        content = copy.deepcopy(pack.source['content'])
        if failure == 'missing-admission':
            content['admissions'] = [a for a in content['admissions'] if a['id'] != 'reveal']
        updated = pack.client().documents.update(
            pack.pin['document_id'], project=pack.project, expected_version=pack.pin['version'],
            content=content, idempotency_key='replace-source')
        assert updated.ok
        if failure != 'old-version':
            calls[-1]['args']['schema_source'] = {
                'document_id': pack.pin['document_id'], 'version': updated.data['version'],
                'content_digest': _digest(content)}
        pack.restart()
    path = tmp_path / 'commands.json'
    path.write_text(json.dumps(calls))
    before = path.read_bytes()
    session = TimelineSession.open(pack.project, 'film', client=pack.client(),
                                    base_revision_id=pack.base['base_revision_id'],
                                    base_publication_id=pack.base['base_publication_id'])
    pending_path = session.outbox.path
    outbox = pending_path.read_bytes()
    code, refused = cli(pack, capsys, path)
    assert code == 1 and not refused['ok']
    assert path.read_bytes() == before and pending_path.read_bytes() == outbox
    assert pack.calls == [] and len(pack.history()['items']) == 1


def test_pack_pending_source_dependency_retry_never_reads(pack, monkeypatch):
    session = pack.session(base=pack.base)
    pack.lost.add('params-A')
    with pytest.raises(WorkspaceClientError):
        session.commit_many(pack.pack_commands, idempotency_key='params-A')
    flight = copy.deepcopy(pack.calls[-1])
    suffix = copy.deepcopy(pack.pack_commands[-1])
    suffix['args']['values']['seed'] = 9
    queued = session.queue_many([suffix])
    assert queued[0]['args']['schema_source'] == pack.pin
    source = copy.deepcopy(pack.source['content'])
    source['admissions'] = []
    result = pack.client().documents.update(pack.pin['document_id'], project=pack.project, content=source,
                                             expected_version=pack.pin['version'], idempotency_key='revoke')
    assert result.ok
    pack.restart()
    session = pack.session()

    def tripwire(*args, **kwargs):
        raise AssertionError('exact retry read capture inputs')

    with monkeypatch.context() as patch:
        transport = session.client._remote._transport
        for name in ('get_document', 'get_object', 'get_project_verified_media'):
            patch.setattr(transport, name, tripwire)
        patch.setattr(session, '_bundle', tripwire)
        session.commit_many(pack.pack_commands, idempotency_key='params-A')
    assert pack.calls[-1] == flight
    assert json.loads(pack.path.read_bytes())['pending'] == queued
    accepted = session.flush()
    # Runtime's retained port can still validate the original accepted source.
    assert accepted['data']['commands'] == queued
    assert State(bundle_from_document(accepted['data']['canonical_document'])).entity(
        'parent/clip:effect')['params']['seed'] == 9


@pytest.mark.parametrize('captured', [False, True])
def test_media_file_retry_after_lifecycle_change(media, tmp_path, capsys, monkeypatch, captured):
    from astrid.sdk.workspace_client import WorkspaceClient

    calls = media_plan(media).commands if captured else media.media_commands
    path = tmp_path / 'commands.json'
    path.write_text(json.dumps(calls))
    before = path.read_bytes()
    media.lost.add('media-file')
    code, failure = cli(media, capsys, path, '--idempotency-key', 'media-file')
    assert code == 1 and not failure['ok']
    flight = copy.deepcopy(media.calls[-1])
    association = next(row for row in media.media_associations
                       if row['object_id'] == media.media_pins[1]['object_id'])
    media.service().update_managed_output_lifecycle(association['association_id'], {
        'operation': 'pin', 'expected_version': association['lifecycle']['version']}, idempotency_key='change-lifecycle')
    media.restart()

    def tripwire(*args, **kwargs):
        raise AssertionError('file retry read capture inputs')

    for name in ('get_document', 'get_object', 'get_project_verified_media'):
        monkeypatch.setattr(WorkspaceClient, name, tripwire)
    monkeypatch.setattr(TimelineSession, '_bundle', tripwire)
    code, accepted = cli(media, capsys, path, '--idempotency-key', 'media-file')
    assert code == 0, accepted
    assert media.calls[-1] == flight and path.read_bytes() == before


def test_media_lifecycle_change_before_capture_keeps_file(media, tmp_path, capsys):
    association = next(row for row in media.media_associations
                       if row['object_id'] == media.media_pins[1]['object_id'])
    media.service().update_managed_output_lifecycle(association['association_id'], {
        'operation': 'pin', 'expected_version': association['lifecycle']['version']}, idempotency_key='revoke-selection')
    path = tmp_path / 'commands.json'
    path.write_text(json.dumps(media.media_commands))
    before = path.read_bytes()
    count = len(media.history()['items'])
    code, refused = cli(media, capsys, path)
    assert code == 1 and not refused['ok']
    assert path.read_bytes() == before and media.calls == []
    assert len(media.history()['items']) == count


def test_pack_unchanged_known_and_unknown_params_need_no_schema_read(pack, monkeypatch):
    session = pack.session(base=pack.base)
    session.commit_many(pack.pack_commands[:2])
    call = command('clip.set-params', 'parent/clip:effect', {
        'values': {'seed': 4, 'unknown': [None, False, {}]}, 'clear': []})

    def tripwire(*args, **kwargs):
        raise AssertionError('unchanged params read schema inputs')

    transport = session.client._remote._transport
    monkeypatch.setattr(transport, 'get_document', tripwire)
    monkeypatch.setattr(transport, 'get_object', tripwire)
    accepted = session.commit(call)
    assert State(bundle_from_document(accepted['data']['canonical_document'])).entity(
        'parent/clip:effect')['params'] == {'seed': 4, 'unknown': [None, False, {}]}


def test_missing_verified_media_method_refuses_only_media(media, monkeypatch):
    from astrid_runtime_client.generated import WorkspaceClient

    monkeypatch.delattr(WorkspaceClient, 'get_project_verified_media')
    session = media.session(base=media.base)
    session.queue(command('track.create', 'parent', {'row': {'id': 'audio', 'kind': 'audio'}}))
    before = media.path.read_bytes()
    with pytest.raises(WorkspaceClientError, match='does not provide'):
        session.queue_many(media.media_commands)
    assert media.path.read_bytes() == before


def test_media_selection_rechecked_by_server_after_capture(media):
    session = media.session(base=media.base)
    queued = session.queue_many(media.media_commands)
    association = next(row for row in media.media_associations
                       if row['object_id'] == media.media_pins[1]['object_id'])
    media.service().update_managed_output_lifecycle(association['association_id'], {
        'operation': 'pin', 'expected_version': association['lifecycle']['version']}, idempotency_key='after-capture')
    with pytest.raises(WorkspaceClientError, match='catalog digest changed'):
        session.flush()
    state = json.loads(media.path.read_bytes())
    assert state['pending'] == queued
    assert json.loads(state['flight']['body'])['commands'] == queued
    assert media.calls[-1][2] == 409
