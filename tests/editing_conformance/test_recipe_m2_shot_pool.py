"""shot.pool: ordered pool membership on the shot, exact capture, inverse, rebase and refusals."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute, operations, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_auto_placement import auto_place_shared, unplace_shared
from astrid.sdk.timeline.native_shot_pool_commands import POOL, capture_shot_pool
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm, inputs
from tests.sdk.test_timeline_commit_provider import (
    inverse as inverse_call,
)
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi,  # noqa: F401 -- autouse detached ABI fixture
)

OWNER = 'occurrence:occ-a'
SOURCE = OWNER + '/source'
FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_shot_pool.json'
SCHEMA = Path(__file__).parents[2] / 'astrid/core/timeline/schema/edit-command.schema.json'


def pins():
    document, old, new, verified = inputs('image')
    others = [{'asset': 'pool-' + name, 'generation_id': 'generation-' + name, 'variant_id': 'variant-' + name,
               'object_id': 'sha256:' + digit * 64, 'catalog_digest': 'sha256:' + digit * 64}
              for name, digit in (('b', '3'), ('c', '4'))]
    verified += [{'selection': copy.deepcopy(pin), 'media_type': 'image/fixture', 'size': 123} for pin in others]
    return document, old, [new, *others], verified


def step(bundle, action, pin, verified):
    command = capture_shot_pool(bundle, OWNER, action, pin, ownership='occurrence', verified_media=verified)
    return command, execute(bundle, [command], verified_media=verified)


def pool(bundle):
    return State(bundle).config(OWNER)['app']['astrid']['pool']


def build(name):
    document, _, [a, b, c], verified = pins()
    bundle = bundle_from_document(document)
    if name == 'add-first':
        return document, bundle, 'add', a, verified
    for pin in (a, b, c)[:3 if name == 'remove-middle' else 1]:
        bundle = step(bundle, 'add', pin, verified)[1].bundle
    if name == 'add-second':
        return document, bundle, 'add', b, verified
    return document, bundle, 'remove', b, verified


CASES = ['add-first', 'add-second', 'remove-middle']


@pytest.mark.parametrize('name', CASES)
def test_portable_goldens(name):
    _, bundle, action, pin, verified = build(name)
    command, plan = step(bundle, action, pin, verified)
    assert json.loads(FIXTURE.read_text())[name] == {
        'commands': [command], 'records': plan.records, 'pool': pool(plan.bundle)}


@pytest.mark.parametrize('name', CASES)
def test_exact_capture_replay_inverse_and_redo(name):
    _, bundle, action, pin, verified = build(name)
    before = copy.deepcopy(bundle)
    command, plan = step(bundle, action, pin, verified)
    validate_command(command)
    assert json.loads(json.dumps(command, allow_nan=False)) == command
    assert bundle == before
    assert plan.commands == [command]
    assert replay(plan, bundle, verified_media=verified).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    redone = inverse(undone.bundle, accepted_boundaries(undone.records, plan.bundle, undone.bundle))
    assert redone.bundle == plan.bundle


def test_add_appends_in_order_and_binds_the_exact_media_without_touching_the_rest():
    document, bundle, _, pin, verified = build('add-second')
    plan = execute(bundle, [step(bundle, 'add', pin, verified)[0]], verified_media=verified)
    assert pool(plan.bundle) == ['reserved-new', 'pool-b']
    binding = State(plan.bundle).entity(OWNER + '/registry')['assets']['pool-b']
    assert (binding['generationId'], binding['variantId']) == ('generation-b', 'variant-b')
    assert plan.bundle['parent'] == bundle['parent']
    assert State(plan.bundle).collection(OWNER, 'clip') == State(bundle).collection(OWNER, 'clip')
    assert State(plan.bundle).config('occurrence:occ-b') == State(bundle).config('occurrence:occ-b')
    assert 'sha256:' + '3' * 64 in {row['media_id'] for row in
                                     document_from_bundle(plan.bundle)['dependency_manifest']['media']}


def test_remove_keeps_the_binding_and_undo_restores_the_original_position():
    _, bundle, _, pin, verified = build('remove-middle')
    assert pool(bundle) == ['reserved-new', 'pool-b', 'pool-c']
    _, plan = step(bundle, 'remove', pin, verified)
    assert pool(plan.bundle) == ['reserved-new', 'pool-c']
    assert 'pool-b' in State(plan.bundle).entity(OWNER + '/registry')['assets']
    assert pool(inverse(plan.bundle, plan.records).bundle) == ['reserved-new', 'pool-b', 'pool-c']


def test_absent_and_empty_pools_are_distinct_and_removing_the_last_member_keeps_an_empty_list():
    document, _, [a, *_], verified = pins()
    bundle = bundle_from_document(document)
    assert 'pool' not in (State(bundle).config(OWNER).get('app') or {}).get('astrid', {})
    added = step(bundle, 'add', a, verified)[1]
    emptied = step(added.bundle, 'remove', a, verified)[1]
    assert pool(emptied.bundle) == []
    assert inverse(emptied.bundle, emptied.records).bundle == added.bundle
    assert inverse(added.bundle, added.records).bundle == bundle


def test_the_first_add_keeps_existing_siblings_of_the_astrid_namespace():
    document, _, [a, *_], verified = pins()
    bundle = bundle_from_document(document)
    State(bundle).config(OWNER)['app'] = {'theme': 1, 'astrid': {'keep': [1]}}
    before = copy.deepcopy(bundle)
    plan = step(bundle, 'add', a, verified)[1]
    assert State(plan.bundle).config(OWNER)['app'] == {'theme': 1, 'astrid': {'keep': [1], 'pool': ['reserved-new']}}
    assert inverse(plan.bundle, plan.records).bundle == before


def test_legacy_group_pool_ids_in_provenance_are_never_rewritten():
    document, _, [a, *_], verified = pins()
    bundle = bundle_from_document(document)
    legacy = {'group_migration': {'legacy_group': {'shotId': 'g', 'poolGenerationIds': ['generation-new']}}}
    bundle['placements'][0]['provenance'] = copy.deepcopy(legacy)
    plan = step(bundle, 'add', a, verified)[1]
    assert plan.bundle['placements'][0]['provenance'] == legacy
    assert all(write['ref'] != OWNER for record in plan.records for write in record['writes'])


@pytest.mark.parametrize('damage', ['duplicate', 'not-a-member', 'placed', 'unverified', 'shared', 'bad-pool',
                                    'bad-list', 'bad-app'])
def test_refusals_preserve_input(damage):
    document, old, [a, b, _], verified = pins()
    bundle = bundle_from_document(document)
    action, pin, kind = 'add', a, None
    if damage == 'duplicate':
        bundle = step(bundle, 'add', a, verified)[1].bundle
        kind = 'identity_collision'
    elif damage == 'not-a-member':
        action, kind = 'remove', 'identity_conflict'
        bundle = step(bundle, 'add', b, verified)[1].bundle
    elif damage == 'placed':
        pin, kind = old, 'identity_conflict'
    elif damage == 'unverified':
        verified, kind = verified[:1], 'dependency_changed'
    elif damage == 'shared':
        bundle['placements'][1]['shot_id'] = bundle['placements'][0]['shot_id']
        kind = 'unsupported_ownership'
    elif damage == 'bad-pool':
        State(bundle).config(OWNER)['app'] = {'astrid': {'pool': 'reserved-new'}}
        kind = 'unsupported_pool'
    elif damage == 'bad-list':
        State(bundle).config(OWNER)['app'] = {'astrid': {'pool': ['pool-b', 3]}}
        kind = 'unsupported_pool'
    else:
        State(bundle).config(OWNER)['app'] = ['not', 'an', 'object']
    before = copy.deepcopy(bundle)
    command = {'schema_version': 1, 'op': 'shot.pool', 'version': '1', 'select': OWNER,
               'args': {'action': action, 'media': copy.deepcopy(pin)}, 'intent': {'ownership': 'occurrence'}}
    with pytest.raises(CommandError) as error:
        execute(bundle, [command], verified_media=verified)
    assert kind is None or error.value.kind == kind
    assert bundle == before


def test_args_are_closed_and_the_selector_must_be_an_explicit_occurrence():
    _, bundle, action, pin, verified = build('add-first')
    command = capture_shot_pool(bundle, OWNER, action, pin, ownership='occurrence', verified_media=verified)
    plain = {key: command[key] for key in ('schema_version', 'op', 'version', 'select', 'args', 'intent')}
    validator = Draft202012Validator(json.loads(SCHEMA.read_text()))
    assert not list(validator.iter_errors(plain))
    for changes in ({'args': {**plain['args'], 'extra': 1}}, {'args': {'action': 'add'}},
                    {'args': {**plain['args'], 'action': 'toggle'}}, {'select': 'parent'},
                    {'select': OWNER + '/clip:clip-a'}, {'version': '2'}, {'intent': {'ownership': 'shared'}}):
        assert list(validator.iter_errors({**plain, **changes}))
        with pytest.raises(CommandError):
            validate_command({**plain, **changes})
    for owner, ownership in [('parent', 'occurrence'), (OWNER + '::display', 'occurrence'), (OWNER, 'shared')]:
        with pytest.raises(CommandError) as error:
            capture_shot_pool(bundle, owner, action, pin, ownership=ownership, verified_media=verified)
        assert error.value.kind == 'unsupported_ownership'


def test_schema_registration_is_additive_and_complete():
    schema = json.loads(SCHEMA.read_text())
    constrained = {branch['if']['properties']['op']['const'] for branch in schema['$defs']['EditCommand']['allOf']}
    assert 'shot.pool' in constrained
    assert {'placement.create', 'placement.unplace', 'occurrence.add-media', 'clip.delete'} <= constrained
    assert 'shot.pool' in operations()
    assert operations()['shot.pool'].parameters == schema['$defs']['ShotPoolArgs']


def test_undo_refuses_after_any_intervening_write_to_the_pool_and_replay_refuses_a_changed_pool():
    _, bundle, action, pin, verified = build('add-second')
    _, plan = step(bundle, action, pin, verified)
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later(SOURCE, POOL, ['reserved-new', 'pool-b'])])
    head = copy.deepcopy(bundle)
    State(head).config(OWNER)['app']['astrid']['pool'].append('pool-c')
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        replay(plan, head, verified_media=verified)
    assert head == before


def test_disjoint_edits_rebase_and_retain_the_original_capture():
    _, bundle, action, pin, verified = build('add-second')
    command, plan = step(bundle, action, pin, verified)
    head = copy.deepcopy(bundle)
    State(head).entity('occurrence:occ-b/clip:clip-a')['at'] = 3
    head['parent']['name'] = 'Someone else renamed this'
    State(head).config('occurrence:occ-b')['app'] = {'astrid': {'pool': ['pool-c']}}
    rebased = replay(plan, head, verified_media=verified)
    assert rebased.commands == [command]
    assert pool(rebased.bundle) == ['reserved-new', 'pool-b']
    assert State(rebased.bundle).config('occurrence:occ-b')['app']['astrid']['pool'] == ['pool-c']
    assert inverse(rebased.bundle, rebased.records).bundle == head


def test_provider_accepts_add_and_remove_with_exact_undo_and_redo():
    document, _, [a, *_], verified = pins()
    realm = MediaRealm(document, verified)
    added = realm.call([capture_shot_pool(bundle_from_document(document), OWNER, 'add', a,
                                          ownership='occurrence', verified_media=verified)])
    after = added['data']['canonical_document']
    assert pool(bundle_from_document(after)) == ['reserved-new']
    removal = capture_shot_pool(bundle_from_document(after), OWNER, 'remove', a, ownership='occurrence',
                                verified_media=verified)
    removed = realm.call([removal])
    assert pool(bundle_from_document(removed['data']['canonical_document'])) == []
    undo = realm.call([inverse_call([removed['receipt']['receipt_id']])])
    assert undo['data']['canonical_document'] == after
    redo = realm.call([inverse_call([undo['receipt']['receipt_id']])])
    assert redo['data']['canonical_document'] == removed['data']['canonical_document']


def pooled_case():
    document, _, [a, *_], verified = pins()
    bundle = bundle_from_document(document)
    State(bundle).occurrence(OWNER)['duration_ms'] = 20000
    result = auto_place_shared(bundle, OWNER, 'placed', a, ownership='occurrence', verified_media=verified,
                               pooled=True)
    return document, execute(bundle, result['commands'], verified_media=verified).bundle, a, verified


def test_a_null_frame_pools_without_a_clip_and_refuses_a_frame_or_anchor():
    document, pooled, a, verified = pooled_case()
    assert pool(pooled) == ['reserved-new']
    assert State(pooled).collection(OWNER, 'clip') == State(bundle_from_document(document)).collection(OWNER, 'clip')
    for extra in ({'frame': 3}, {'anchor': 'clip-a'}):
        with pytest.raises(CommandError) as error:
            auto_place_shared(pooled, OWNER, 'placed', a, ownership='occurrence', verified_media=verified,
                              pooled=True, **extra)
        assert error.value.kind == 'unsupported_timing'


def test_placing_pooled_media_promotes_it_in_one_batch_that_undoes_as_one():
    _, pooled, a, verified = pooled_case()
    before = copy.deepcopy(pooled)
    result = auto_place_shared(pooled, 'occurrence:occ-a', 'placed', a, ownership='occurrence',
                               verified_media=verified, frame=None)
    assert [command['op'] for command in result['commands']] == ['placement.create', 'shot.pool']
    assert result['capture']['promoted'] is True
    plan = execute(pooled, result['commands'], verified_media=verified)
    assert pooled == before
    assert pool(plan.bundle) == []
    assert 'placed' in {row['id'] for row in State(plan.bundle).collection(OWNER, 'clip')}
    assert replay(plan, pooled, verified_media=verified).records == plan.records
    assert inverse(plan.bundle, plan.records).bundle == before


def test_promotion_and_keep_as_pooled_round_trip_through_the_provider():
    _, pooled, a, verified = pooled_case()
    realm = MediaRealm(document_from_bundle(pooled), verified)
    promoted = realm.call(auto_place_shared(pooled, OWNER, 'placed', a, ownership='occurrence',
                                            verified_media=verified)['commands'])
    placed = bundle_from_document(promoted['data']['canonical_document'])
    assert pool(placed) == []
    kept = realm.call(unplace_shared(placed, OWNER, 'placed', ownership='occurrence', keep_as_pooled=True,
                                     media=a, verified_media=verified)['commands'])
    assert pool(bundle_from_document(kept['data']['canonical_document'])) == ['reserved-new']
    undo = realm.call([inverse_call([kept['receipt']['receipt_id']])])
    assert undo['data']['canonical_document'] == promoted['data']['canonical_document']


def test_keep_as_pooled_needs_the_exact_media_of_the_placed_clip():
    _, pooled, a, verified = pooled_case()
    placed = execute(pooled, auto_place_shared(pooled, OWNER, 'placed', a, ownership='occurrence',
                                               verified_media=verified)['commands'], verified_media=verified).bundle
    for media in (None, verified[2]['selection']):
        with pytest.raises(CommandError) as error:
            unplace_shared(placed, OWNER, 'placed', ownership='occurrence', keep_as_pooled=True, media=media,
                           verified_media=verified)
        assert error.value.kind == 'identity_conflict'
