"""The paired product carrier, including replay and read-only source bindings."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline import commands
from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline._materialization import source_entity
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_materialization_identity import source
from tests.editing_conformance.test_materialization_map_spike import allocation, moved, physical
from tests.editing_conformance.test_recipe_m1_commands import inverse


def test_product_capture_json_recovery_and_exact_source_pin_across_stale_heads():
    original = bundle_from_document(source())
    plan = moved(original)
    mapping, bindings, dependencies = allocation(original, document_from_bundle(plan.bundle))
    assert plan.id_map == mapping
    assert plan.records[0]['bindings'][-len(bindings):] == bindings
    assert plan.records[0]['dependencies'][-len(dependencies):] == dependencies
    assert all(plan.commands[0]['bindings'][binding['key']] == binding['ref'] for binding in bindings)
    recovered = commands.execute(original, json.loads(json.dumps(plan.commands)))
    assert recovered.records == plan.records and recovered.id_map == mapping
    parent = copy.deepcopy(original)
    parent['parent']['name'] = 'Intervening parent'
    sibling = moved(original, 'occ-b', 12.012)
    for head in (bundle_from_document(document_from_bundle(parent)),
                 bundle_from_document(document_from_bundle(sibling.bundle))):
        actual = replay(recovered, head)
        assert actual.id_map == mapping
        assert [dep for dep in actual.records[0]['dependencies']
                if dep['key'].startswith('materialization.source:')] == dependencies
        assert physical(document_from_bundle(actual.bundle), 'occ-a') == physical(
            document_from_bundle(plan.bundle), 'occ-a')
    assert recovered.records == plan.records


@pytest.mark.parametrize('damage', ['missing', 'extra', 'wrong', 'unbound', 'source', 'owner', 'pin', 'scope'])
def test_product_rejects_unverified_allocation_without_mutating_inputs(damage):
    original = bundle_from_document(source())
    plan = moved(original)
    before = copy.deepcopy(original)
    supplied = copy.deepcopy(plan.commands)
    mapping = copy.deepcopy(plan.id_map)
    if damage == 'missing':
        mapping.pop(next(iter(mapping)))
    elif damage == 'extra':
        mapping['shot:extra/item:extra'] = 'extra'
    elif damage == 'wrong':
        mapping[next(iter(mapping))] = 'wrong'
    elif damage == 'unbound':
        supplied[0]['bindings'].pop(next(key for key in mapping if '/item:' in key))
    elif damage in ('source', 'owner'):
        key = next(key for key in supplied[0]['bindings'] if key.startswith(
            'materialization.owner:' if damage == 'owner' else 'shot:'))
        supplied[0]['bindings'][key] = 'occurrence:occ-b' if damage == 'owner' else 'shot:wrong'
    elif damage == 'pin':
        next(dep for dep in plan.records[0]['dependencies'] if dep['key'].startswith(
            'materialization.source:'))['pin']['source']['revision_id'] = 'wrong'
    else:
        original = bundle_from_document(source(project='other-project'))
    with pytest.raises(CommandError):
        if damage == 'pin':
            replay(plan, original)
        else:
            commands.execute(original, supplied, id_map=mapping)
    if damage != 'scope':
        assert original == before


def test_source_binding_resolves_raw_identity_read_only_without_writable_source_alias():
    original = bundle_from_document(source())
    plan = moved(original)
    pin = next(dep['pin'] for dep in plan.records[0]['dependencies']
               if dep['key'].startswith('materialization.source:'))
    state = State(plan.bundle)
    assert state.entity('shot:chapter-shot', optional=True) is None
    assert state.entity('shot:chapter-shot/item:item-1', optional=True) is None
    item = source_entity(state, 'shot:chapter-shot/item:item-1', pin)
    assert item['item_id'] == 'item-1'
    item['metadata']['opaque_literal'] = 'changed'
    assert source_entity(state, 'shot:chapter-shot/item:item-1', pin)['metadata']['opaque_literal'] == 'item-1'
    assert source_entity(state, 'shot:chapter-shot', pin)['items'][0]['item_id'] == 'item-1'
    assert original == bundle_from_document(source())


@pytest.mark.parametrize('codec', ['id', 'item_id', 'both', 'opaque-id'])
def test_item_access_preserves_actual_codec_source_windows_and_opaque_fields(codec):
    document = source()
    shot = document['shot_revisions'][0]
    item = shot['payload']['items'][0]
    if codec != 'item_id':
        item['id'] = 'opaque-secondary' if codec == 'opaque-id' else 'item-1'
    if codec == 'id':
        item.pop('item_id')
    item['opaque'] = {'id': 'item-1', 'literal': ['item-1', None, {}]}
    shot['content_digest'] = _digest(shot['payload'])
    document['dependency_manifest'] = _manifest([shot], document['internal_timeline_revisions'],
                                               document['dependency_manifest']['media'], [])
    original = bundle_from_document(document)
    plan = moved(original)
    destination = original['placements'][0]['shot_id']
    identity = original['source_mapping']['shots'][destination]['item_id_map']['item-1']
    ref = 'shot:' + destination + '/item:' + identity
    raw = State(plan.bundle).entity(ref)
    assert raw.get('item_id', raw.get('id')) == identity
    assert ('item_id' in raw) == (codec != 'id')
    if 'id' in raw:
        assert raw['id'] == ('opaque-secondary' if codec == 'opaque-id' else identity)
    assert raw['opaque'] == item['opaque'] and raw['metadata'] == item['metadata']
    internal = document_from_bundle(plan.bundle)['internal_timeline_revisions']
    assert all(row['payload']['source_window'] == {'start': 4, 'end': 9} for row in internal)
    assert inverse(plan.bundle, plan.records).bundle == original


@pytest.fixture
def item_ops(monkeypatch):
    def create(ctx, command):
        ctx.create_entity(command['select'], kind='item', owner=command['select'].split('/')[0],
                          value=command['args']['row'])
    original = commands.operations()
    monkeypatch.setattr(commands, 'operations', lambda: {
        **original, 'test.item-create': commands.Operation({'type': 'object'}, create, {})})


def test_semantic_item_birth_is_typed_and_separate_from_derived_allocations(item_ops):
    original = bundle_from_document(source())
    owner = 'shot:' + original['placements'][0]['shot_id']
    ref = owner + '/item:new-item'
    call = {'schema_version': 1, 'op': 'test.item-create', 'version': '1', 'select': ref,
            'args': {'row': {'id': 'new-item', 'opaque': {'item-1': None}}}}
    plan = commands.execute(original, [call])
    assert plan.records[0]['created'] == [{'ref': ref, 'kind': 'item', 'owner': owner}]
    assert State(original).get(ref, []) == ABSENT
    assert State(plan.bundle).get(ref, []) == present(call['args']['row'])
    assert ref not in plan.id_map
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    sibling = 'shot:' + original['placements'][1]['shot_id'] + '/item:new-item'
    with pytest.raises(CommandError, match='occupied'):
        commands.execute(plan.bundle, [{**call, 'select': sibling}])


def test_stale_disjoint_child_edit_keeps_original_map_on_an_already_materialized_owner():
    from astrid.sdk.timeline.capture import capture_move

    original = bundle_from_document(source())
    plan = moved(original)
    other = commands.execute(original, [capture_move(original, 'occurrence:occ-a/clip:clip-b', 6.006)])
    head = bundle_from_document(document_from_bundle(other.bundle))
    actual = replay(plan, head, intervening_records=other.records)
    assert actual.id_map == plan.id_map
    assert actual.commands == plan.commands
    for record in (actual.records[0], plan.records[0]):
        dependency = next(dep for dep in record['dependencies']
                          if dep['key'].startswith('materialization.source:'))
        assert dependency['pin']['parent'] == original['base_parent']
    config = State(actual.bundle).config('occurrence:occ-a')
    assert next(row for row in config['clips'] if row['id'] == 'clip-b')['at'] == 6.006



def test_whole_shot_write_cannot_smuggle_an_untyped_semantic_item_birth(monkeypatch):
    def write(ctx, command):
        root = ctx.read(command['select'])
        root['payload']['items'].append({'id': 'unrecorded-item'})
        ctx.write(command['select'], [], root)

    registered = commands.operations()
    monkeypatch.setattr(commands, 'operations', lambda: {
        **registered, 'test.untyped-item': commands.Operation({'type': 'object'}, write, {})})
    original = bundle_from_document(source())
    before = copy.deepcopy(original)
    call = {'schema_version': 1, 'op': 'test.untyped-item', 'version': '1',
            'select': 'shot:' + original['placements'][0]['shot_id'], 'args': {}}
    with pytest.raises(CommandError, match='requires create_entity'):
        commands.execute(original, [call])
    assert original == before



def test_sdk_source_capture_matches_provider_carrier_without_changing_legacy_bundles():
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle

    document = source()
    arguments = {'parent_revision': {**document['parent_revision'], 'project_id': document['project_id'],
                                     'timeline_id': document['timeline_id']},
                 'shot_revisions': [{**row, 'project_id': document['project_id']}
                                    for row in document['shot_revisions']],
                 'internal_timeline_revisions': [{**row, 'project_id': document['project_id']}
                                                 for row in document['internal_timeline_revisions']]}
    legacy = open_authoring_bundle(**arguments)
    original = open_authoring_bundle(**arguments, capture_sources=True)
    before = copy.deepcopy(original)
    sdk = moved(original)
    provider = moved(bundle_from_document(document))
    assert sdk.commands == provider.commands and sdk.id_map == provider.id_map
    assert sdk.records == provider.records
    assert inverse(sdk.bundle, sdk.records).bundle == original
    assert original == before
    assert moved(legacy).id_map == {}


@pytest.mark.parametrize('damage', ['duplicate-key', 'extra-binding', 'bad-item', 'duplicate-item', 'bool-pin'])
def test_allocation_join_rejects_ambiguous_or_noncanonical_facts(damage):
    from astrid.sdk.timeline._materialization import id_map

    original = bundle_from_document(source())
    records = moved(original).records
    record = records[0]
    dep = next(dep for dep in record['dependencies'] if dep['key'].startswith('materialization.source:'))
    binding = next(binding for binding in record['bindings'] if binding['key'].startswith('shot:'))
    if damage == 'duplicate-key':
        record['bindings'].append({**binding, 'ref': 'shot:other'})
    elif damage == 'extra-binding':
        record['bindings'].append({**binding, 'key': binding['key'] + '/item:extra'})
    elif damage in ('bad-item', 'duplicate-item'):
        items = dep['pin']['source']['item_id_map']
        raw, target = next(iter(items.items()))
        items[raw + '-duplicate' if damage == 'duplicate-item' else raw] = (
            target if damage == 'duplicate-item' else target + '/invalid')
    else:
        dep['pin']['source']['opaque'] = 1
        other = copy.deepcopy(record)
        next(dep for dep in other['dependencies'] if dep['key'].startswith(
            'materialization.source:'))['pin']['source']['opaque'] = True
        records.append(other)
    with pytest.raises(CommandError):
        id_map(records)


@pytest.mark.parametrize('ref', ['shot:chapter-shot/item:', 'shot:chapter-shot/item:item-1/extra',
                                'shot:chapter-shot/item:item-1::'])
def test_source_entity_requires_a_canonical_reference(ref):
    original = bundle_from_document(source())
    pin = next(dep['pin'] for dep in moved(original).records[0]['dependencies']
               if dep['key'].startswith('materialization.source:'))
    with pytest.raises(CommandError):
        source_entity(State(original), ref, pin)


def test_boolean_item_edit_materializes_instead_of_reusing_numeric_source():
    original = bundle_from_document(source())
    destination = original['placements'][0]['shot_id']
    shot = original['shots'][destination]
    # JSON numbers compare by value, but true is a different authored value.
    shot['base_payload']['items'][0]['opaque'] = 1
    shot['payload']['items'][0]['opaque'] = True
    output = document_from_bundle(original)
    owner = output['parent_revision']['payload']['occurrences'][0]
    assert owner['shot_id'] == destination
    physical = next(row for row in output['shot_revisions'] if row['shot_id'] == destination)
    assert physical['payload']['items'][0]['opaque'] is True


@pytest.mark.parametrize('codec', ['item_id', 'id', 'both'])
def test_sibling_first_replay_uses_the_same_codec_remapper_without_touching_opaque_values(codec):
    from tests.editing_conformance.test_commit_runtime_opaque_items import opaque

    document = source()
    shot = document['shot_revisions'][0]
    item = shot['payload']['items'][0]
    item['metadata'].update(source_item_id='item-1', source_item='item-1', data=opaque())
    item['data'] = opaque()
    if codec in ('id', 'both'):
        item['id'] = item['item_id']
    if codec == 'id':
        del item['item_id']
    shot['content_digest'] = _digest(shot['payload'])
    document['dependency_manifest'] = _manifest([shot], document['internal_timeline_revisions'],
                                               document['dependency_manifest']['media'], [])
    original = bundle_from_document(document)
    before = copy.deepcopy(original)
    plan = moved(original)
    sibling = moved(original, 'occ-b', 12.012)
    actual = replay(plan, bundle_from_document(document_from_bundle(sibling.bundle)))
    assert actual.id_map == plan.id_map
    assert actual.commands == plan.commands
    assert physical(document_from_bundle(actual.bundle), 'occ-a') == physical(
        document_from_bundle(plan.bundle), 'occ-a')
    destination = actual.bundle['placements'][0]['shot_id']
    row = actual.bundle['shots'][destination]['payload']['items'][0]
    identity = row.get('item_id', row.get('id'))
    assert row['metadata']['source_item_id'] == row['metadata']['source_item'] == identity
    assert row['metadata']['data'] == row['data'] == opaque()
    assert original == before


def test_item_birth_without_an_existing_items_collection_is_typed(item_ops):
    document = source()
    shot = document['shot_revisions'][0]
    del shot['payload']['items']
    shot['content_digest'] = _digest(shot['payload'])
    document['dependency_manifest'] = _manifest([shot], document['internal_timeline_revisions'],
                                               document['dependency_manifest']['media'], [])
    original = bundle_from_document(document)
    owner = 'shot:' + original['placements'][0]['shot_id']
    ref = owner + '/item:new-item'
    call = {'schema_version': 1, 'op': 'test.item-create', 'version': '1', 'select': ref,
            'args': {'row': {'id': 'new-item'}}}
    plan = commands.execute(original, [call])
    assert plan.records[0]['created'] == [{'ref': ref, 'kind': 'item', 'owner': owner}]
    assert State(plan.bundle).entity(ref) == {'id': 'new-item'}
    assert 'items' not in original['shots'][owner[5:]]['payload']


def test_item_identity_cannot_be_allocated_twice_inside_one_recipe(monkeypatch):
    def duplicate(ctx, command):
        owner = command['select'].split('/')[0]
        ctx.create_entity(command['select'], kind='item', owner=owner, value={'id': 'new-item'})
        ctx.clear(command['select'], [])
        ctx.create_entity(command['select'], kind='item', owner=owner, value={'id': 'new-item'})

    registered = commands.operations()
    monkeypatch.setattr(commands, 'operations', lambda: {
        **registered, 'test.item-duplicate': commands.Operation({'type': 'object'}, duplicate, {})})
    original = bundle_from_document(source())
    ref = 'shot:' + original['placements'][0]['shot_id'] + '/item:new-item'
    with pytest.raises(CommandError, match='occupied'):
        commands.execute(original, [{'schema_version': 1, 'op': 'test.item-duplicate', 'version': '1',
                                     'select': ref, 'args': {}}])


@pytest.mark.parametrize('field', ['schema_version', 'ordinal'])
def test_history_recorder_indices_require_integers(field):
    from astrid.sdk.timeline.commit import _records

    records = moved(bundle_from_document(source())).records
    recorder = {'schema_version': 1, 'commands': records}
    if field == 'ordinal':
        records[0]['ordinal'] = False
    else:
        recorder['schema_version'] = True
    with pytest.raises(ValueError):
        _records([{'intent': 'recorded', 'records': recorder}], ValueError, {}, {})
