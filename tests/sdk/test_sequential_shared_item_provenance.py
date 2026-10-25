"""Sequential shared placement keeps authenticated physical item identities."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from tests.sdk.test_timeline_commit_provider_document import MEDIA, document_fixture


def shared_birth():
    return {'schema_version': 1, 'op': 'occurrence.place-shared', 'version': '1',
            'select': 'occurrence:occ-a', 'created': ['occurrence:repeated-third'],
            'args': {'occurrence_id': 'repeated-third', 'on': 20}}


def item_patch(before, after, *, ref='shot-revision:shot-1'):
    return {'schema_version': 1, 'op': 'doc.patch', 'version': '1', 'select': None,
            'args': {'changes': [{'op': 'set', 'ref': ref, 'path': ['items'],
                                  'before': present(before), 'value': copy.deepcopy(after)}]}}


def source_document(*, empty=False, shared=False):
    document = document_fixture(shared=shared)
    # The full host window has no source shift. Express the existing clip
    # spans as internal trims so a new placement uses supported source timing.
    parent = document['parent_revision']
    for occurrence in parent['payload']['occurrences']:
        occurrence['source_offset'] = 0
    parent['content_digest'] = _digest(parent['payload'])
    for internal in document['internal_timeline_revisions']:
        for clip in internal['payload']['clips']:
            clip.update({'from': 0, 'to': clip['hold']})
        internal['content_digest'] = _digest(internal['payload'])
    if empty:
        shot = document['shot_revisions'][0]
        shot['payload']['items'] = []
        shot['content_digest'] = _digest(shot['payload'])
    document['dependency_manifest'] = _manifest(
        document['shot_revisions'], document['internal_timeline_revisions'],
        document['dependency_manifest']['media'], [])
    return document


@pytest.fixture
def runtime_realm(monkeypatch):
    from tests.sdk import test_timeline_commit_graph_roots as roots

    seed = roots.seed_trusted_parent

    def registered_seed(service, publication, *, idempotency_key):
        # Consume the registered child root created by RuntimeRealm, adding
        # only a genuinely missing scope through the normal timeline API.
        scopes = {image['timeline_id'] for image in publication['internal_timeline_revisions']}
        existing = {row['timeline_id'] for row in service.list_timelines(publication['project_id'])['items']}
        for timeline in sorted(scopes - {publication['timeline_id']} - existing):
            service.create_timeline(publication['project_id'], timeline,
                                    idempotency_key='shared-internal-' + timeline)
        return seed(service, publication, idempotency_key=idempotency_key)

    monkeypatch.setattr(roots, 'seed_trusted_parent', registered_seed)
    return roots.RuntimeRealm


def runtime_commit(realm, commands, key):
    head = realm.head
    body = {'api_version': 1, 'project_id': realm.project, 'timeline_id': realm.timeline,
            'base_revision_id': head['revision_id'], 'base_publication_id': head['publication_id'],
            'commands': copy.deepcopy(commands), 'label': 'Sequential shared items',
            'steps': [{'id': str(ordinal), 'label': command['op'], 'intent': 'Shared physical edit',
                       'tags': ['integration'], 'command_ordinals': [ordinal],
                       'patch': copy.deepcopy(command['args']['changes'])
                       if command['op'] == 'doc.patch' else []}
                      for ordinal, command in enumerate(commands)],
            'merge': 'fields', 'reads': [{'kind': 'scope', 'ref': 'timeline', 'path': []}],
            'dry_run': False, 'source': {'via': 'python'}, 'rationale': 'Sequential source provenance'}
    return realm.service.commit_timeline(
        realm.project, realm.timeline, body, idempotency_key=key, publisher='actor-1',
        invocation_path=f'/v1/projects/{realm.project}/timelines/{realm.timeline}/commit',
        authorize=lambda: None)


@pytest.mark.parametrize('shared', [False, True])
def test_registered_shared_birth_reads_original_physical_item_map(shared):
    document = source_document(shared=shared)
    original = bundle_from_document(document)
    snapshot = copy.deepcopy(original)
    plan = execute(original, [shared_birth()])
    state = State(plan.bundle)
    assert state.shot_item_map('occurrence:repeated-third/shot') == {'item-1': 'item-1'}
    assert state.get('occurrence:repeated-third/shot',
                     ['payload', 'items', 'item_id:item-1', 'media_id']) == present(MEDIA)
    assert document_from_bundle(plan.bundle)['shot_revisions'] == document['shot_revisions']
    assert original == snapshot
    assert plan.bundle['source_mapping']['_runtime_document'] == document
    for local, source in original['source_mapping']['shots'].items():
        assert plan.bundle['source_mapping']['shots'][local] == source


@pytest.mark.parametrize('empty', [False, True])
def test_registered_birth_then_item_consumer_in_one_batch(empty):
    document = source_document(empty=empty)
    bundle = bundle_from_document(document)
    snapshot = copy.deepcopy(bundle)
    before = document['shot_revisions'][0]['payload']['items']
    after = [{'item_id': 'shared-source-item', 'media_id': MEDIA,
              'metadata': {'literal': 'shared-source-item', 'keep': [None, False]}}]
    plan = execute(bundle, [shared_birth(), item_patch(before, after)])
    state = State(plan.bundle)
    for owner in ('occ-a', 'repeated-third'):
        assert state.shot_item_map('occurrence:' + owner + '/shot') == {
            'shared-source-item': 'shared-source-item'}
        assert state.get('occurrence:' + owner + '/shot', ['payload', 'items']) == present(after)
    result = document_from_bundle(plan.bundle)
    assert len(result['shot_revisions']) == 1
    assert result['shot_revisions'][0]['payload']['items'] == after
    assert {row['shot_id'] for row in result['parent_revision']['payload']['occurrences']} == {'chapter-shot'}
    assert len({row['shot_revision_id'] for row in result['parent_revision']['payload']['occurrences']}) == 1
    assert bundle == snapshot
    for key in ('shots', 'placements', '_runtime_document'):
        assert plan.bundle['source_mapping'][key] == bundle['source_mapping'][key]


def test_shared_input_birth_then_consumer_keeps_all_original_owners():
    document = source_document(shared=True)
    bundle = bundle_from_document(document)
    before = document['shot_revisions'][0]['payload']['items']
    after = copy.deepcopy(before)
    after[0]['metadata']['note'] = [None, False, 'item-1']
    plan = execute(bundle, [shared_birth(), item_patch(before, after)])
    result = document_from_bundle(plan.bundle)
    assert len(result['shot_revisions']) == 1
    assert result['shot_revisions'][0]['payload']['items'] == after
    rows = result['parent_revision']['payload']['occurrences']
    assert [row['occurrence_id'] for row in rows] == ['occ-a', 'occ-b', 'repeated-third']
    assert len({row['shot_revision_id'] for row in rows}) == 1
    assert {row['shot_id'] for row in rows} == {'chapter-shot'}
    assert State(plan.bundle).shot_item_map('occurrence:repeated-third/shot') == {'item-1': 'item-1'}
    assert plan.bundle['source_mapping']['_runtime_document'] == document
    for local, source in bundle['source_mapping']['shots'].items():
        assert plan.bundle['source_mapping']['shots'][local] == source


@pytest.mark.parametrize('damage', ['unknown-item', 'ambiguous-owner', 'map', 'pin',
                                  'malformed-source', 'missing-source'])
def test_sequential_physical_item_correspondence_still_refuses_without_writes(damage):
    bundle = execute(bundle_from_document(source_document()), [shared_birth()]).bundle
    state = State(bundle)
    if damage == 'ambiguous-owner':
        bundle['placements'].append(copy.deepcopy(bundle['placements'][-1]))
    elif damage == 'map':
        bundle['source_mapping']['shots']['chapter-shot']['item_id_map'] = {'item-1': 'foreign'}
    elif damage == 'pin':
        bundle['source_mapping']['shots']['chapter-shot']['revision_id'] = 'foreign'
    elif damage == 'malformed-source':
        bundle['source_mapping']['shots']['chapter-shot'] = []
    elif damage == 'missing-source':
        bundle['source_mapping']['shots'].pop('chapter-shot')
    snapshot = copy.deepcopy(bundle)
    with pytest.raises(CommandError) as error:
        if damage == 'malformed-source':
            state.shot_item_map('occurrence:repeated-third/shot')
        else:
            state.get('occurrence:repeated-third/shot',
                      ['payload', 'items', 'item_id:unknown' if damage == 'unknown-item' else 'item_id:item-1'])
    assert error.value.kind == ('history_unavailable' if damage == 'missing-source' else 'identity_conflict')
    assert bundle == snapshot


def test_existing_owner_cannot_retarget_another_genuinely_created_physical_image():
    original = bundle_from_document(source_document())
    created = execute(original, [{'schema_version': 1, 'op': 'occurrence.create', 'version': '1',
                                 'select': 'parent', 'args': {
                                     'occurrence_id': 'other', 'shot_id': 'other-shot',
                                     'name': 'Other', 'track': 'picture', 'on': 30, 'duration': 10}}])
    bundle = bundle_from_document(document_from_bundle(created.bundle))
    bundle['placements'][0]['shot_id'] = 'other-shot'
    snapshot = copy.deepcopy(bundle)
    with pytest.raises(CommandError) as error:
        State(bundle).shot_item_map('occurrence:occ-a/shot')
    assert error.value.kind == 'identity_conflict'
    assert bundle == snapshot


@pytest.mark.parametrize('damage', ['ambiguous-map', 'wrong-owner', 'missing-id', 'duplicate-id'])
def test_existing_alias_correspondence_remains_strict(damage):
    bundle = bundle_from_document(source_document(shared=True))
    local = bundle['placements'][0]['shot_id']
    if damage == 'ambiguous-map':
        mapping = bundle['source_mapping']['shots'][local]['item_id_map']
        mapping['foreign'] = next(iter(mapping.values()))
    elif damage == 'wrong-owner':
        bundle['placements'][0]['shot_id'] = bundle['placements'][1]['shot_id']
    elif damage == 'missing-id':
        bundle['shots'][local]['payload']['items'][0].pop('item_id')
    else:
        bundle['shots'][local]['payload']['items'].append(
            copy.deepcopy(bundle['shots'][local]['payload']['items'][0]))
    snapshot = copy.deepcopy(bundle)
    with pytest.raises(CommandError) as error:
        State(bundle).shot_item_map('occurrence:occ-a/shot')
    assert error.value.kind == 'identity_conflict'
    assert bundle == snapshot


@pytest.mark.integration
@pytest.mark.parametrize('empty', [False, True])
def test_registered_runtime_shared_birth_and_consumer_keep_one_physical_image(empty, runtime_realm):
    realm = runtime_realm(source_document(empty=empty))
    # Prepare through the registered provider, then use its canonical source.
    prepared = runtime_commit(realm, [{'schema_version': 1, 'op': 'shot.set', 'version': '1',
                                     'select': 'occurrence:occ-a/shot',
                                     'args': {'values': {'name': 'Published source'}, 'clear': []}}], 'source')
    source = prepared['data']['canonical_document']
    shot = source['shot_revisions'][0]
    before = shot['payload']['items']
    media = source['dependency_manifest']['media'][0]['media_id']
    after = [{'item_id': 'shared-source-item', 'media_id': media,
              'metadata': {'literal': 'shared-source-item', 'keep': [None, False]}}]
    accepted = runtime_commit(realm, [shared_birth(), item_patch(before, after,
                              ref='shot-revision:' + shot['revision_id'])], 'birth-and-consume')
    assert accepted['data']['status'] == 'accepted'
    result = accepted['data']['canonical_document']
    assert len(result['shot_revisions']) == 1
    image = result['shot_revisions'][0]
    assert image['shot_id'] == shot['shot_id']
    assert image['payload']['items'] == after
    assert image['payload']['unknown'] == shot['payload']['unknown']
    rows = result['parent_revision']['payload']['occurrences']
    assert [row['occurrence_id'] for row in rows] == ['occ-a', 'repeated-third']
    assert {row['shot_revision_id'] for row in rows} == {image['revision_id']}
    assert {row['shot_id'] for row in rows} == {shot['shot_id']}
    assert rows[1]['placement']['start_ms'] == 20000
    assert realm.documents[realm.head['revision_id']] == result
    assert realm._commits.revision_closure(
        realm.project, realm.timeline, source['parent_revision']['revision_id']) == source


@pytest.mark.integration
@pytest.mark.parametrize('damage', ['before', 'unknown-ref', 'duplicate-item', 'missing-item-id'])
def test_registered_runtime_failed_consumer_rolls_back_shared_birth(damage, runtime_realm):
    realm = runtime_realm(source_document())
    from runtime_protocol.errors import RuntimeErrorBase

    source = copy.deepcopy(realm.document)
    before = source['shot_revisions'][0]['payload']['items']
    after = copy.deepcopy(before)
    if damage == 'duplicate-item':
        after.append(copy.deepcopy(after[0]))
    elif damage == 'missing-item-id':
        after[0].pop('item_id')
    call = item_patch(before, after)
    if damage == 'before':
        call['args']['changes'][0]['before'] = present([])
    elif damage == 'unknown-ref':
        call['args']['changes'][0]['ref'] = 'shot-revision:unknown'
    snapshot = tuple(realm.service.store.conn.iterdump())
    head, entries = copy.deepcopy(realm.head), copy.deepcopy(realm.entries)
    with pytest.raises(RuntimeErrorBase):
        runtime_commit(realm, [shared_birth(), call], 'invalid-batch')
    assert realm.head == head
    assert realm.entries == entries
    assert tuple(realm.service.store.conn.iterdump()) == snapshot
    assert realm._commits.revision_closure(realm.project, realm.timeline, head['revision_id']) == source
