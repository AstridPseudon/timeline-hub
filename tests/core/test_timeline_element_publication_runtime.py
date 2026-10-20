"""Native element batches against the actual retained-schema Runtime provider.

The public helper remains on its compatibility publisher until paired migration.
These tests exercise explicit native requests, not helper retry recovery.
"""
from __future__ import annotations

import copy
import shutil
from pathlib import Path

import pytest
import yaml

from astrid.core.element import project_packs as packs
from astrid.core.receipts.contract import CommandReceipt
from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline import commands, commit
from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_track_set
from tests.helpers.runtime import use_runtime, vendored_runtime_commit
from tests.sdk import test_timeline_selected_schema_runtime as selected_schema

REF = selected_schema.REF
inverse = selected_schema.inverse
configured_project_pack = selected_schema.configured_project_pack
retained_pack = selected_schema.retained_pack

pytestmark = pytest.mark.integration
use_runtime(commit=vendored_runtime_commit())


def native_submitter(case):
    requests = []

    def submit(*, element, clip_id, expected_head, idempotency_key, duration=None, params=None):
        head = case.head()
        assert head['revision_id'] == expected_head
        source = case.service.get_document(case.project, case.pin['document_id'])
        pin = {'document_id': source['document_id'], 'version': source['version'],
               'content_digest': commit._digest(source['content'])}
        target = f'parent/clip:{clip_id}'
        calls = [{'schema_version': 1, 'op': 'clip.set-element', 'version': '1', 'select': target,
                  'args': {'elementRef': copy.deepcopy(element), 'schema_source': pin}}]
        if duration is not None:
            calls.append({'schema_version': 1, 'op': 'clip.set', 'version': '1', 'select': target,
                          'args': {'values': {'hold': duration}, 'clear': []}})
        if params:
            calls.append({'schema_version': 1, 'op': 'clip.set-params', 'version': '1', 'select': target,
                          'args': {'values': copy.deepcopy(params), 'clear': [], 'schema_source': pin}})
        body = case.request(calls, head)
        requests.append(copy.deepcopy(body))
        result = case.submit(body, idempotency_key)
        return DomainResult.success(result['data'], receipt=CommandReceipt.from_dict(result['receipt']),
                                    idempotency_key=idempotency_key)

    return submit, requests


@pytest.mark.parametrize('same_revision', [False, True])
def test_native_element_update_reload_guarded_inverse_and_exact_retry(retained_pack, monkeypatch,
                                                                     same_revision):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService

    case = retained_pack
    original = copy.deepcopy(case.bundle()['source_mapping']['_runtime_document'])
    before = copy.deepcopy(State(case.bundle()).entity(REF))
    selected = case.selected
    if not same_revision:
        case.definition['schema']['properties']['seed']['maximum'] = 20
        case.path.write_text(yaml.safe_dump(case.definition))
        admitted = packs.admit_project_pack('realm', case.project)
        selected = {key: admitted['elements'][0]['descriptor'][key]
                    for key in ('id', 'kind', 'packId', 'revision')}
        assert selected['revision'] != before['elementRef']['revision']
    # Source and build-cache availability never establish save-time authority.
    shutil.rmtree(case.source_root)
    shutil.rmtree(case.artifact_root)

    def forbidden(*args, **kwargs):
        raise AssertionError('element save used launcher, local source, cache, or renderer')

    monkeypatch.setattr(packs, '_open_client', forbidden)
    monkeypatch.setattr(packs, 'resolve_admitted_element', forbidden)
    monkeypatch.setattr(packs, 'artifact_root', forbidden)
    monkeypatch.setattr(packs, 'authoring_root', forbidden)
    submit, requests = native_submitter(case)
    result = submit(clip_id='effect',
        element=selected, expected_head=case.head()['revision_id'], duration=6,
        params={'seed': 8 if same_revision else 16, 'opaque': {'keep': [None, False, {}]}},
        idempotency_key='native-element-update')
    assert result.ok, result.error
    accepted = case.submit(requests[0], 'native-element-update')
    document = accepted['data']['canonical_document']
    row = State(commit.bundle_from_document(document)).entity(REF)
    assert result.data['accepted_revision_id'] == accepted['data']['accepted_revision_id']
    assert result.receipt.as_dict() == accepted['receipt']
    assert row['elementRef'] == selected and row['hold'] == 6
    assert row['params'] == {**before['params'], 'seed': 8 if same_revision else 16,
                             'opaque': {'keep': [None, False, {}]}}
    assert row['params']['future'] == before['params']['future']
    assert document['shot_revisions'] == original['shot_revisions']
    assert document['internal_timeline_revisions'] == original['internal_timeline_revisions']
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    assert case.bundle()['source_mapping']['_runtime_document'] == document
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', forbidden)
        assert case.submit(requests[0], 'native-element-update') == accepted
    undone = case.submit(case.request([inverse(result.receipt.receipt_id)]), 'undo-element-update')
    restored = undone['data']['canonical_document']
    assert restored['parent_revision']['payload'] == original['parent_revision']['payload']
    assert restored['shot_revisions'] == original['shot_revisions']
    assert restored['internal_timeline_revisions'] == original['internal_timeline_revisions']
    # The native provider retains immutable schema provenance for redo.
    assert restored['dependency_manifest'] == {
        **original['dependency_manifest'],
        'documents': document['dependency_manifest']['documents']}
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'redo-element-update')
    assert redone['data']['canonical_document'] == document
    # A newer disjoint label survives the guarded inverse.
    case.submit(case.request([capture_track_set(case.bundle(), 'parent/track:picture',
                                               values={'label': 'Newer'})]), 'newer-label')
    disjoint = case.submit(case.request([inverse(redone['receipt']['receipt_id'])]), 'undo-after-label')
    restored_state = State(commit.bundle_from_document(disjoint['data']['canonical_document']))
    assert restored_state.entity(REF) == before
    assert restored_state.entity('parent/track:picture')['label'] == 'Newer'
    # The redo wrote the same element again; its history edge guards old undo.
    head = case.head()
    with pytest.raises(RuntimeErrorBase) as error:
        case.submit(case.request([inverse(result.receipt.receipt_id)]), 'refuse-element-aba')
    assert error.value.details['reason'] == 'intervening_write'
    assert case.head() == head


@pytest.mark.parametrize('damage', ['params', 'revision', 'element-only-revision'])
def test_native_element_batch_refusal_is_atomic(retained_pack, monkeypatch, damage):
    from runtime_protocol.errors import RuntimeErrorBase

    case = retained_pack
    submit, requests = native_submitter(case)
    original, head = copy.deepcopy(case.bundle()), case.head()
    selected = case.selected if damage == 'params' else {
        **case.selected, 'revision': 'sha256:' + '0' * 64}
    with pytest.raises(RuntimeErrorBase):
        submit(clip_id='effect',
            element=selected, expected_head=head['revision_id'], duration=6,
            params=(None if damage == 'element-only-revision' else
                    {'seed': 11 if damage == 'params' else 8}), idempotency_key='refused-element')
    assert len(requests) == 1
    assert case.head() == head and case.bundle() == original


@pytest.mark.parametrize('existing', [None, {}])
@pytest.mark.parametrize('params', [None, {}])
def test_element_only_retained_declaration_survives_removal_restart_and_replay(
        retained_pack, monkeypatch, existing, params):
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    case = retained_pack
    row = copy.deepcopy(State(case.bundle()).entity(REF))
    row.update(id='empty-effect', at=3, opaque={'keep': [None, {}, False]})
    row.pop('params')
    if existing is not None:
        row['params'] = existing
    ref = 'parent/clip:empty-effect'
    case.submit(case.request([capture_clip_add(case.bundle(), 'parent', row)]), 'empty-effect')
    before = copy.deepcopy(case.bundle()['source_mapping']['_runtime_document'])
    case.definition['schema']['properties']['seed']['maximum'] = 20
    case.path.write_text(yaml.safe_dump(case.definition))
    admitted = packs.admit_project_pack('realm', case.project)
    selected = {key: admitted['elements'][0]['descriptor'][key]
                for key in ('id', 'kind', 'packId', 'revision')}
    assert selected['revision'] != row['elementRef']['revision']
    source = case.service.get_document(case.project, admitted['documentId'])
    pin = {'document_id': source['document_id'], 'version': source['version'],
           'content_digest': commit._digest(source['content'])}
    snapshot = next(item['snapshot_object'] for item in source['content']['admissions']
                    if item['revision'] == selected['revision'])
    reads = []
    original_object = RequestCommitPort.document_object

    def read(port, source_pin, object_id):
        reads.append((copy.deepcopy(source_pin), object_id))
        return original_object(port, source_pin, object_id)

    monkeypatch.setattr(RequestCommitPort, 'document_object', read)
    submit, requests = native_submitter(case)
    result = submit(clip_id='empty-effect',
        element=selected, expected_head=case.head()['revision_id'], params=params,
        idempotency_key='element-only')
    assert result.ok, result.error
    assert [call['op'] for call in requests[0]['commands']] == ['clip.set-element']
    assert requests[0]['commands'][0]['args']['schema_source'] == pin
    assert reads == [(pin, snapshot['object_id'])]
    accepted = case.submit(requests[0], 'element-only')
    document = accepted['data']['canonical_document']
    assert State(commit.bundle_from_document(document)).entity(ref) == {**row, 'elementRef': selected}
    assert document['dependency_manifest']['documents'] == [pin]
    entry = case.service._timeline_commits()[0].history_entry(
        case.project, 'film', accepted['receipt']['receipt_id'])
    record = entry['records']['commands'][0]
    assert [write['path'] for write in record['writes']] == [['elementRef']]
    assert next(dep['pin'] for dep in record['dependencies'] if dep['key'] == 'params.snapshot') == {
        'source': pin, 'element': selected, 'object': snapshot}
    # A later declaration and removal of current selection cannot retarget history.
    case.definition['schema']['properties']['seed']['maximum'] = 30
    case.path.write_text(yaml.safe_dump(case.definition))
    newer = packs.admit_project_pack('realm', case.project)
    assert newer['elements'][0]['descriptor']['revision'] != selected['revision']
    current = case.service.get_document(case.project, source['document_id'])
    case.service.update_document(case.project, current['document_id'], {
        'expected_version': current['version'], 'content': {**current['content'], 'admissions': []}},
        idempotency_key='remove-current-selection')
    shutil.rmtree(case.source_root)
    shutil.rmtree(case.artifact_root)
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    assert case.bundle()['source_mapping']['_runtime_document'] == document

    def forbidden(*args, **kwargs):
        raise AssertionError('element-only used launcher, local source, cache, or renderer')

    monkeypatch.setattr(packs, '_open_client', forbidden)
    monkeypatch.setattr(packs, 'resolve_admitted_element', forbidden)
    monkeypatch.setattr(packs, 'artifact_root', forbidden)
    monkeypatch.setattr(packs, 'authoring_root', forbidden)
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', forbidden)
        assert case.submit(requests[0], 'element-only') == accepted
    reads.clear()
    undone = case.submit(case.request([inverse(result.receipt.receipt_id)]), 'undo-element-only')
    restored = undone['data']['canonical_document']
    assert restored['parent_revision']['payload'] == before['parent_revision']['payload']
    assert restored['dependency_manifest']['documents'] == [pin]
    assert reads == [(pin, snapshot['object_id'])]
    # A fresh intent is based on a closure that authorizes this retained pin.
    replay_body = case.request(requests[0]['commands'])
    case.submit(case.request([capture_track_set(case.bundle(), 'parent/track:picture',
                                               values={'label': 'Newer'})]), 'concurrent-label')
    reads.clear()
    replayed = case.submit(replay_body, 'replay-element-only')
    assert replayed['data']['status'] == 'rebased'
    replayed_document = replayed['data']['canonical_document']
    replayed_state = State(commit.bundle_from_document(replayed_document))
    assert replayed_state.entity(ref) == {**row, 'elementRef': selected}
    assert replayed_state.entity('parent/track:picture')['label'] == 'Newer'
    assert replayed_document['dependency_manifest']['documents'] == [pin]
    assert reads and all(item == (pin, snapshot['object_id']) for item in reads)
    undone = case.submit(case.request([inverse(replayed['receipt']['receipt_id'])]), 'undo-replay')
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'redo-element-only')
    assert redone['data']['canonical_document'] == replayed_document


def raw_element(case):
    return {'schema_version': 1, 'op': 'clip.set-element', 'version': '1',
            'select': 'parent/clip:effect',
            'args': {'elementRef': copy.deepcopy(case.selected), 'schema_source': copy.deepcopy(case.pin)}}


@pytest.mark.parametrize('damage', ['missing-pin', 'inline-schema', 'pin-version', 'pin-digest',
    'id', 'kind', 'owner', 'revision', 'revoked', 'legacy', 'missing-object', 'corrupt-object',
    'foreign-project', 'authorization'])
def test_raw_element_only_refusal_is_atomic(retained_pack, damage):
    from runtime_protocol.errors import ForbiddenError, RuntimeErrorBase

    case = retained_pack
    command = raw_element(case)
    def authorize():
        pass
    if damage == 'missing-pin':
        del command['args']['schema_source']
    elif damage == 'inline-schema':
        command['args']['schema_source']['schema'] = {'type': 'object'}
    elif damage == 'pin-version':
        command['args']['schema_source']['version'] += 1
    elif damage == 'pin-digest':
        command['args']['schema_source']['content_digest'] = 'sha256:' + '0' * 64
    elif damage == 'revision':
        command['args']['elementRef']['revision'] = 'sha256:' + '0' * 64
    elif damage in ('id', 'kind', 'owner'):
        command['args']['elementRef'][{'owner': 'packId'}.get(damage, damage)] = (
            'transition' if damage == 'kind' else 'wrong')
    elif damage in ('revoked', 'legacy'):
        row = case.service.get_document(case.project, case.pin['document_id'])
        content = copy.deepcopy(row['content'])
        if damage == 'revoked':
            content['admissions'] = []
        else:
            for admission in content['admissions']:
                del admission['snapshot_object']
        updated = case.service.update_document(case.project, row['document_id'],
            {'expected_version': row['version'], 'content': content}, idempotency_key='damage')['data']
        command['args']['schema_source'] = {'document_id': updated['document_id'],
            'version': updated['version'], 'content_digest': commit._digest(updated['content'])}
    elif damage in ('missing-object', 'corrupt-object'):
        obj = next(iter(case.options['schema_inputs'][0][1]))
        path = case.service.cas.path_for(obj.removeprefix('sha256:'))
        if damage == 'missing-object':
            path.unlink()
        else:
            path.write_bytes(b'corrupt')
    elif damage == 'foreign-project':
        foreign = case.service.create_project({'slug': 'foreign', 'name': 'Foreign'})['id']
        from tests.core.test_project_packs import seed
        seed(foreign)
        admitted = packs.admit_project_pack('realm', foreign)
        row = case.service.get_document(foreign, admitted['documentId'])
        command['args']['schema_source'] = {'document_id': row['document_id'],
            'version': row['version'], 'content_digest': commit._digest(row['content'])}
    else:
        def authorize():
            raise ForbiddenError('Element authorization refusal')
    head, bundle = case.head(), copy.deepcopy(case.bundle())
    history = case.service.list_timeline_commits(case.project, 'film', authorize=lambda: None)
    with pytest.raises(RuntimeErrorBase):
        case.submit(case.request([command]), 'raw-element-refusal', authorize=authorize)
    assert case.head() == head and case.bundle() == bundle
    assert case.service.list_timeline_commits(
        case.project, 'film', authorize=lambda: None) == history


def test_another_actually_admitted_owner_cannot_replace_selected_owner(retained_pack):
    from runtime_protocol.errors import RuntimeErrorBase

    case = retained_pack
    location = packs.init_project_pack('realm', case.project, collection='other_owner')
    root = Path(location['packRoot'])
    shutil.copytree(case.source_root / 'rendering', root / 'rendering', dirs_exist_ok=True)
    definition = copy.deepcopy(case.definition)
    definition['pack_id'] = 'other_owner'
    (root / 'rendering/elements/effects/reveal/element.yaml').write_text(yaml.safe_dump(definition))
    manifest = yaml.safe_load((root / 'pack.yaml').read_text())
    manifest['rendering'] = yaml.safe_load((case.source_root / 'pack.yaml').read_text())['rendering']
    (root / 'pack.yaml').write_text(yaml.safe_dump(manifest))
    admitted = packs.admit_project_pack('realm', case.project, collection='other_owner')
    selected = {key: admitted['elements'][0]['descriptor'][key]
                for key in ('id', 'kind', 'packId', 'revision')}
    assert selected['id'] == case.selected['id'] and selected['kind'] == case.selected['kind']
    assert selected['packId'] != case.selected['packId']
    row = case.service.get_document(case.project, admitted['documentId'])
    command = raw_element(case)
    command['args'] = {'elementRef': selected, 'schema_source': {'document_id': row['document_id'],
        'version': row['version'], 'content_digest': commit._digest(row['content'])}}
    head, bundle = case.head(), copy.deepcopy(case.bundle())
    history = case.service.list_timeline_commits(case.project, 'film', authorize=lambda: None)
    with pytest.raises(RuntimeErrorBase, match='pack owner'):
        case.submit(case.request([command]), 'other-admitted-owner')
    assert case.head() == head and case.bundle() == bundle
    assert case.service.list_timeline_commits(
        case.project, 'film', authorize=lambda: None) == history

