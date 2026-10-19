"""Portable candidate semantics; these fixtures do not qualify Runtime authority."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import _digest, bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_media_commands import capture_swap_media
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse, later
from tests.sdk.test_timeline_commit_provider_document import MEDIA, document_fixture

FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_media_swap.json'
NEW = 'sha256:' + '2' * 64
TARGET = 'parent/clip:clip-a'


def inputs(kind='image'):
    document = json.loads(json.dumps(document_fixture()))
    payload = document['parent_revision']['payload']
    payload['registry']['assets']['replacement'] = {
        'media_id': NEW, 'type': kind, 'opaque': {'nullable': None, 'ordered': [False, 0, {}]}}
    payload['registry']['assets']['picture']['type'] = kind
    old = {'asset': 'picture', 'generation_id': 'generation-old', 'variant_id': 'variant-old',
           'object_id': MEDIA, 'catalog_digest': 'sha256:' + 'a' * 64}
    new = {'asset': 'replacement', 'generation_id': 'generation-new', 'variant_id': 'variant-new',
           'object_id': NEW, 'catalog_digest': 'sha256:' + 'b' * 64}
    verified = [{'selection': copy.deepcopy(pin), 'media_type': kind + '/fixture', 'size': 123,
                 **({'duration_seconds': 10} if kind == 'video' else {})} for pin in (old, new)]
    if kind == 'video':
        for rows in (payload['clips'], payload['config']['clips']):
            rows[0].update({'from': 2, 'to': 6, 'speed': 2})
    document['parent_revision']['content_digest'] = _digest(payload)
    document['dependency_manifest']['media'].append({'media_id': NEW, 'content_digest': NEW})
    return document, old, new, verified


def captured(kind='image'):
    document, old, new, verified = inputs(kind)
    bundle = bundle_from_document(document)
    return bundle, capture_swap_media(bundle, TARGET, old, new, verified_media=verified), verified


def test_portable_golden_exact_capture_candidate_reload_inverse_and_replay():
    golden = json.loads(FIXTURE.read_text())
    original = bundle_from_document(golden['input'])
    bundle, command, verified = captured()
    assert bundle == original
    assert golden['commands'] == [command]
    plan = execute(original, golden['commands'], verified_media=golden['verified_media'])
    assert plan.records == golden['records']
    assert document_from_bundle(plan.bundle) == golden['output']
    reloaded = bundle_from_document(json.loads(json.dumps(golden['output'])))
    assert document_from_bundle(inverse(reloaded, plan.records).bundle,
                                source_bundles=[original]) == golden['input']
    assert replay(plan, original, verified_media=verified).records == plan.records
    assert plan.records[0]['created'] == []
    assert plan.records[0]['writes'] == [{'ref': TARGET, 'path': ['asset'],
        'before': present('picture'), 'after': present('replacement')}]
    before = copy.deepcopy(State(original).entity(TARGET))
    before['asset'] = 'replacement'
    assert State(reloaded).entity(TARGET) == before
    assert reloaded['parent']['registry'] == original['parent']['registry']
    assert golden['output']['shot_revisions'] == golden['input']['shot_revisions']
    assert golden['output']['internal_timeline_revisions'] == golden['input']['internal_timeline_revisions']
    assert original == bundle_from_document(golden['input'])


def test_video_keeps_nonzero_source_window_speed_and_half_open_end():
    original, command, verified = captured('video')
    verified[1]['duration_seconds'] = 6
    plan = execute(original, [command], verified_media=verified)
    target = State(plan.bundle).entity(TARGET)
    assert (target['from'], target['to'], target['speed'], target['hold'], target['at']) == (2, 6, 2, 2, 1)
    assert document_from_bundle(inverse(plan.bundle, plan.records).bundle) == document_from_bundle(original)
    verified[1]['duration_seconds'] = 5.999
    with pytest.raises(CommandError, match='window exceeds'):
        execute(original, [command], verified_media=verified)


def test_disjoint_other_clip_edit_survives_rebase_reload_and_inverse():
    original, command, verified = captured()
    ours = execute(original, [command], verified_media=verified)
    other = capture_clip_set_params(original, 'parent/clip:clip-b', values={'opaque': [None, False]})
    theirs = execute(original, [other])
    result = replay(ours, theirs.bundle, intervening_records=theirs.records, verified_media=verified)
    reloaded = bundle_from_document(document_from_bundle(result.bundle))
    assert State(reloaded).entity('parent/clip:clip-b')['params'] == {'opaque': [None, False]}
    assert document_from_bundle(inverse(reloaded, result.records).bundle) == document_from_bundle(theirs.bundle)


def test_unchanged_swap_is_recorded_and_later_unchanged_writes_and_aba_block_undo():
    document, old, _, verified = inputs()
    original = bundle_from_document(document)
    command = capture_swap_media(original, TARGET, old, old, verified_media=verified)
    plan = execute(original, [command], verified_media=verified)
    assert document_from_bundle(plan.bundle) == document
    write = plan.records[0]['writes'][0]
    assert write['before'] == write['after'] == present('picture')
    unchanged = later(TARGET, ['asset'], 'picture')
    aba = {'writes': [{'ref': TARGET, 'path': ['asset'], 'before': present('picture'),
                      'after': present('replacement')}, unchanged['writes'][0]]}
    for intervening in ([unchanged], [aba]):
        with pytest.raises(CommandError, match='intervening'):
            inverse(plan.bundle, plan.records, intervening)


def test_move_then_swap_preserves_literal_intent_and_staged_inverse_restores_both():
    document, old, new, verified = inputs()
    original = bundle_from_document(document)
    move = capture_move(original, TARGET, 3.003)
    moved = execute(original, [move])
    swap = capture_swap_media(moved.bundle, TARGET, old, new, verified_media=verified)
    combined = execute(original, [move, swap], verified_media=verified)
    expected = copy.deepcopy(State(moved.bundle).entity(TARGET))
    expected['asset'] = new['asset']
    assert State(combined.bundle).entity(TARGET) == expected
    assert inverse(combined.bundle, combined.records).bundle == original


def test_registry_unchanged_write_blocks_inverse_and_disjoint_param_clear_survives():
    original, command, verified = captured()
    plan = execute(original, [command], verified_media=verified)
    entry = original['parent']['registry']['assets']['replacement']
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later('parent', ['registry', 'assets', 'replacement'], entry)])
    State(original).entity('parent/clip:clip-b')['params'] = {'clear-me': None, 'keep': False}
    other = capture_clip_set_params(original, 'parent/clip:clip-b', clear=['clear-me'])
    theirs = execute(original, [other])
    rebased = replay(plan, theirs.bundle, intervening_records=theirs.records, verified_media=verified)
    assert State(rebased.bundle).entity('parent/clip:clip-b')['params'] == {'keep': False}
    assert inverse(rebased.bundle, rebased.records).bundle == theirs.bundle


def test_mixed_batch_refusal_discards_earlier_supported_work():
    original, command, verified = captured()
    other = capture_clip_set_params(original, 'parent/clip:clip-b', values={'pending': True})
    before = copy.deepcopy(original)
    with pytest.raises(CommandError, match='exact Runtime-verified'):
        execute(original, [other, command], verified_media=verified[:1])
    assert original == before


@pytest.mark.parametrize('value', [None, 'missing', 'replacement'])
def test_original_asset_cleared_or_changed_refuses_without_mutating_input(value):
    original, command, verified = captured()
    for rows in (original['parent']['clips'], original['parent']['config']['clips']):
        if value is None:
            rows[0].pop('asset')
        else:
            rows[0]['asset'] = value
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(original, [command], verified_media=verified)
    assert original == before


@pytest.mark.parametrize('damage', ['missing', 'object', 'catalog', 'generation', 'variant', 'alias'])
def test_exact_verified_pin_required_and_not_guessed_from_display_or_object(damage):
    original, command, verified = captured()
    if damage == 'missing':
        verified.pop()
    else:
        key = {'object': 'object_id', 'catalog': 'catalog_digest', 'generation': 'generation_id',
               'variant': 'variant_id', 'alias': 'asset'}[damage]
        verified[1]['selection'][key] = 'different'
    before = copy.deepcopy(original)
    with pytest.raises(CommandError, match='exact Runtime-verified'):
        execute(original, [command], verified_media=verified)
    assert original == before


@pytest.mark.parametrize('damage', ['missing-slot', 'wrong-object', 'generation', 'locator', 'null-slot'])
def test_registry_binding_never_allocated_or_repaired_implicitly(damage):
    original, command, verified = captured()
    assets = original['parent']['registry']['assets']
    if damage == 'missing-slot':
        assets.pop('replacement')
    elif damage == 'null-slot':
        assets['replacement'] = None
    elif damage == 'wrong-object':
        assets['replacement']['media_id'] = MEDIA
    elif damage == 'generation':
        assets['replacement']['generationId'] = 'foreign'
    else:
        assets['replacement']['file'] = '/tmp/display-name.png'
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(original, [command], verified_media=verified)
    assert original == before


@pytest.mark.parametrize('field,value', [('asset_id', None), ('time_map', {}), ('from', 0),
    ('source_uuid', 'transcript-old'), ('app', {'astrid': {'on': 'word:old:0'}}),
    ('app', {'astrid': {'words': [[0, 1, 'old']]}}), ('speed', 2), ('hold', 0)])
def test_unsupported_source_and_timing_semantics_refuse_atomically(field, value):
    original, _, verified = captured()
    State(original).entity(TARGET)[field] = value
    before = copy.deepcopy(original)
    old, new = (row['selection'] for row in verified)
    with pytest.raises(CommandError):
        capture_swap_media(original, TARGET, old, new, verified_media=verified)
    assert original == before


def test_closed_args_owner_and_media_clear_are_not_generic_replacement():
    _, command, _ = captured()
    for key, value in [('select', 'occurrence:occ-a/clip:clip-a'), ('select', 'clip-a'),
                       ('select', 'parent/clip:display::id')]:
        invalid = copy.deepcopy(command)
        invalid[key] = value
        with pytest.raises(CommandError):
            validate_command(invalid)
    for args in ({**command['args'], 'media_record': {}}, {**command['args'], 'media': None},
                 {**command['args'], 'clear': ['asset']}):
        invalid = copy.deepcopy(command)
        invalid['args'] = args
        with pytest.raises(CommandError):
            validate_command(invalid)


@pytest.mark.parametrize('nested', [False, True])
def test_existing_parent_registry_codecs_are_read_exactly(nested):
    document, old, new, verified = inputs()
    parent = document['parent_revision']['payload']
    parent['config']['registry'] = copy.deepcopy(parent['registry'])
    if nested:
        parent.pop('registry')
    document['parent_revision']['content_digest'] = _digest(parent)
    original = bundle_from_document(document)
    call = capture_swap_media(original, TARGET, old, new, verified_media=verified)
    result = execute(original, [call], verified_media=verified)
    assert document_from_bundle(inverse(result.bundle, result.records).bundle) == document
