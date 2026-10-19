"""Native empty-track deletion, exact restoration and selective dependency proof."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline._command_state import ABSENT, CommandError, State
from astrid.sdk.timeline._track_commands import capture_track_delete
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.editing_conformance.test_recipe_m2_clip_add import empty_document
from tests.sdk.test_timeline_commit_provider_document import document_fixture

FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_track_delete.json'
TARGET = 'parent/track:empty'


def deletion_document():
    bundle = bundle_from_document(document_fixture())
    bundle['parent']['config']['tracks'] = [
        {'id': 'before', 'kind': 'visual'},
        {'id': 'empty', 'kind': 'visual', 'nullable': None,
         'opaque': {'keep': [None, False, 0, {}, []], 'track_ref': TARGET}},
        {'id': 'picture', 'kind': 'visual'}]
    return document_from_bundle(bundle)


def test_portable_golden_and_exact_position_opaque_presence_reload_undo_redo():
    golden = json.loads(FIXTURE.read_text())
    original = bundle_from_document(golden['input'])
    command = capture_track_delete(original, TARGET)
    assert golden['commands'] == [command]
    plan = execute(original, golden['commands'])
    assert plan.records == golden['records']
    assert document_from_bundle(plan.bundle) == golden['output']
    record = plan.records[0]
    assert record['writes'] == [{'ref': TARGET, 'path': [],
                                'before': {'state': 'present', 'value': State(original).entity(TARGET)},
                                'after': ABSENT}]
    assert record['created'] == []
    reloaded = bundle_from_document(golden['output'])
    undone = inverse(reloaded, plan.records)
    assert document_from_bundle(undone.bundle) == golden['input']
    accepted = accepted_boundaries(undone.records, reloaded, undone.bundle)
    redone = inverse(undone.bundle, accepted)
    assert document_from_bundle(redone.bundle) == golden['output']
    assert inverse(redone.bundle, redone.records).bundle == undone.bundle
    assert replay(plan, original).records == plan.records


def add_dependency(bundle, kind):
    state = State(bundle)
    if kind == 'clip':
        for rows in (bundle['parent']['clips'], bundle['parent']['config']['clips']):
            rows[0]['track'] = 'empty'
    elif kind == 'child-clip':
        state.collection('occurrence:occ-a', 'clip')[0]['track_ref'] = TARGET
    elif kind in ('audio', 'effects'):
        state.config('parent')[kind] = [{'track_id': 'empty'}]
    elif kind in ('child-audio', 'child-effects'):
        state.config('occurrence:occ-a')[kind.removeprefix('child-')] = [{'owner_ref': TARGET}]
    elif kind in ('placement', 'occurrence'):
        row = state.occurrence('occurrence:occ-a')
        (row['placement'] if kind == 'placement' else row)['track'] = 'empty'
    else:
        for shot in bundle['shots'].values():
            shot['payload']['audio_bindings'] = [{'track_ref': TARGET}]


@pytest.mark.parametrize('kind', ['clip', 'child-clip', 'audio', 'effects', 'child-audio',
                                 'child-effects', 'placement', 'occurrence', 'shot-audio'])
def test_surviving_or_new_declared_dependency_refuses_atomically(kind):
    original = bundle_from_document(deletion_document())
    plan = execute(original, [capture_track_delete(original, TARGET)])
    head = copy.deepcopy(original)
    add_dependency(head, kind)
    before = copy.deepcopy(head)
    with pytest.raises(CommandError) as error:
        capture_track_delete(head, TARGET)
    assert error.value.kind == 'surviving_dependents'
    with pytest.raises(CommandError):
        replay(plan, head)
    assert head == before


def test_disjoint_clip_timing_other_track_label_and_opaque_strings_survive_replay_and_inverse():
    original = bundle_from_document(deletion_document())
    plan = execute(original, [capture_track_delete(original, TARGET)])
    head = copy.deepcopy(original)
    for rows in (head['parent']['clips'], head['parent']['config']['clips']):
        rows[0]['at'] = 2
        rows[0]['opaque'] = {'track_ref': TARGET}
    State(head).entity('parent/track:picture')['label'] = 'Another author'
    intervening = [later('parent/clip:clip-a', ['at'], 2),
                   later('parent/clip:clip-a', ['opaque'], {'track_ref': TARGET}),
                   later('parent/track:picture', ['label'], 'Another author')]
    rebased = replay(plan, head, intervening_records=intervening)
    assert inverse(rebased.bundle, rebased.records).bundle == head
    deleted_head = copy.deepcopy(plan.bundle)
    deleted_head['parent'] = copy.deepcopy(rebased.bundle['parent'])
    assert inverse(deleted_head, plan.records, intervening).bundle == head


@pytest.mark.parametrize('ref,path,value', [
    (TARGET, ['id'], 'empty'), (TARGET, ['nullable'], None),
    ('parent/clip:clip-a', ['track'], 'picture'),
    ('occurrence:occ-a/clip:clip-a', ['track_ref'], None),
    ('parent/source', ['effects'], []), ('occurrence:occ-a/source', ['audio'], []),
    ('occurrence:occ-a', ['placement', 'track'], 'picture'),
    ('occurrence:occ-a', ['shot_id'], 'chapter-shot'),
    ('shot:chapter-shot', ['payload', 'audio_bindings'], []),
    ('parent', ['config', 'clips'], []), ('parent', ['config', 'tracks'], []),
    ('occurrence:new', [], {}), ('shot:new', [], {}),
])
def test_identity_exclusions_population_and_order_aba_conflict(ref, path, value):
    original = bundle_from_document(deletion_document())
    plan = execute(original, [capture_track_delete(original, TARGET)])
    intervening = [later(ref, path, value)]
    with pytest.raises(CommandError) as error:
        replay(plan, original, intervening_records=intervening)
    assert error.value.kind == 'intervening_write'
    with pytest.raises(CommandError):
        inverse(plan.bundle, plan.records, intervening)


@pytest.mark.parametrize('change', ['identity', 'order', 'new-clip', 'new-occurrence', 'new-shot'])
def test_current_identity_and_population_changes_conflict(change):
    original = bundle_from_document(deletion_document())
    plan = execute(original, [capture_track_delete(original, TARGET)])
    head = copy.deepcopy(original)
    if change == 'identity':
        State(head).entity(TARGET)['id'] = 'different'
    elif change == 'order':
        State(head).collection('parent', 'track').reverse()
    elif change == 'new-clip':
        for rows in (head['parent']['clips'], head['parent']['config']['clips']):
            rows.append({**copy.deepcopy(rows[0]), 'id': 'new'})
    elif change == 'new-occurrence':
        head['placements'].append({**copy.deepcopy(head['placements'][0]), 'occurrence_id': 'new'})
    else:
        shot = copy.deepcopy(next(iter(head['shots'].values())))
        shot['shot_id'] = 'new'
        head['shots']['new'] = shot
    with pytest.raises(CommandError):
        replay(plan, head)


def test_canonical_schema_closes_args_identity_version_and_intentions():
    schema = json.loads((Path(__file__).parents[2] / 'astrid/core/timeline/schema/edit-command.schema.json').read_text())
    validator = Draft202012Validator(schema)
    original = bundle_from_document(deletion_document())
    valid = capture_track_delete(original, TARGET)
    validator.validate(valid)
    for field, value in [('args', {'cascade': True}), ('version', '2'),
                         ('select', 'occurrence:occ-a/track:picture'),
                         ('select', 'parent'), ('select', 'parent/track:bad::id'),
                         ('select', 'parent/track:missing'), ('intent', {'ripple': 'none'})]:
        command = {**copy.deepcopy(valid), field: value}
        with pytest.raises(CommandError):
            execute(original, [command])
        if value != 'parent/track:missing':
            assert list(validator.iter_errors(command))
    forged = copy.deepcopy(valid)
    forged['reads'] = []
    with pytest.raises(CommandError, match='reads'):
        execute(original, [forged])


@pytest.mark.parametrize('position', [0, 1, 2])
def test_first_middle_last_exact_order_restoration(position):
    original = bundle_from_document(deletion_document())
    tracks = State(original).collection('parent', 'track')
    target = tracks.pop(1)
    tracks.insert(position, target)
    original = bundle_from_document(document_from_bundle(original))
    plan = execute(original, [capture_track_delete(original, TARGET)])
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))
    undone = inverse(reloaded, plan.records)
    assert document_from_bundle(undone.bundle) == document_from_bundle(original)
    accepted = accepted_boundaries(undone.records, reloaded, undone.bundle)
    assert document_from_bundle(inverse(undone.bundle, accepted).bundle) == document_from_bundle(plan.bundle)


@pytest.mark.parametrize('layout', ['both', 'payload', 'config', 'absent'])
def test_last_track_and_empty_or_absent_clip_populations_preserve_presence(layout):
    original = bundle_from_document(empty_document())
    original['parent']['config']['tracks'] = [{'id': 'empty', 'kind': 'visual'}]
    if layout in ('payload', 'absent'):
        original['parent']['config'].pop('clips')
    if layout in ('config', 'absent'):
        original['parent'].pop('clips')
    original = bundle_from_document(document_from_bundle(original))
    plan = execute(original, [capture_track_delete(original, TARGET)])
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))
    assert reloaded['parent']['config']['tracks'] == []
    undone = inverse(reloaded, plan.records)
    assert document_from_bundle(undone.bundle) == document_from_bundle(original)
    assert State(undone.bundle).entity(TARGET) == {'id': 'empty', 'kind': 'visual'}
    assert 'nullable' not in State(undone.bundle).entity(TARGET)
    accepted = accepted_boundaries(undone.records, reloaded, undone.bundle)
    assert document_from_bundle(inverse(undone.bundle, accepted).bundle) == document_from_bundle(plan.bundle)


@pytest.mark.parametrize('key', ['track_ref', 'owner_ref', 'track', 'track_id'])
def test_all_existing_declared_edge_spellings_refuse(key):
    original = bundle_from_document(deletion_document())
    original['parent']['config']['effects'] = [{key: TARGET if key.endswith('_ref') else 'empty'}]
    with pytest.raises(CommandError) as error:
        capture_track_delete(original, TARGET)
    assert error.value.kind == 'surviving_dependents'


def test_unplaced_shot_audio_reference_is_also_guarded():
    original = bundle_from_document(deletion_document())
    # The shared scanner also visits shot payloads outside an occurrence.
    original['placements'] = []
    plan = execute(original, [capture_track_delete(original, TARGET)])
    head = copy.deepcopy(original)
    shot_id = next(iter(head['shots']))
    head['shots'][shot_id]['payload']['audio_bindings'] = [{'owner_ref': TARGET}]
    with pytest.raises(CommandError):
        replay(plan, head)
    with pytest.raises(CommandError) as error:
        capture_track_delete(head, TARGET)
    assert error.value.kind == 'surviving_dependents'
    with pytest.raises(CommandError) as error:
        replay(plan, original, intervening_records=[
            later('shot:' + shot_id, ['payload', 'audio_bindings'], [])])
    assert error.value.kind == 'intervening_write'
