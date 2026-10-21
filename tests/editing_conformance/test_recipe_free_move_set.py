"""The first preserved App drag expressed as one native free-selection move."""
from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline._move_set import capture_move_set
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, bundle_from_document, document_from_bundle
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_add_delete_composition import authored
from tests.editing_conformance.test_recipe_clip_delete import reload
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.editing_conformance.test_recipe_m2_clip_add import empty_document

FIXTURE = Path(__file__).parent / 'fixtures/recipe_m2_free_move_set.json'
MEMBERS = [{'clip': 'parent/clip:clip-2', 'track': 'parent/track:V3'},
           {'clip': 'parent/clip:clip-1', 'track': 'parent/track:V2'}]


def source_document():
    document = empty_document()
    parent = document['parent_revision']['payload']
    parent['config']['output'] = {'resolution': '1920x1080', 'fps': 30, 'file': 'out.mp4'}
    parent['config']['tracks'] = [{'id': lane, 'kind': 'visual'} for lane in ('V1', 'V2')]
    parent['clips'] = [{'id': 'clip-1', 'at': 0, 'track': 'V1', 'clipType': 'hold', 'hold': 2},
                       {'id': 'clip-2', 'at': 2, 'track': 'V2', 'clipType': 'hold', 'hold': 2}]
    parent['config']['clips'] = copy.deepcopy(parent['clips'])
    document['parent_revision']['content_digest'] = _digest(parent)
    return document


def basis(*, new_track=True):
    bundle = bundle_from_document(source_document())
    if new_track:
        bundle['parent']['config']['tracks'].append({'id': 'V3', 'kind': 'visual'})
    return bundle


def capture(bundle, members=MEMBERS, on=3):
    return capture_move_set(bundle, members, 'parent/clip:clip-2', on)


def change(bundle, ref, path, value):
    state = State(bundle)
    before = state.get(ref, path)
    state.set(ref, path, present(value))
    bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
    return {'writes': [{'ref': ref, 'path': path, 'before': before, 'after': present(value)}]}


def staged_drag():
    original = basis(new_track=False)
    create = capture_track_create(original, 'parent', {'id': 'V3', 'kind': 'visual'})
    staged = execute(original, [create]).bundle
    move = capture(staged)
    create['group_id'] = move['group_id'] = 'free-drag-1'
    return original, execute(original, [create, move])


def portable_golden():
    original, plan = staged_drag()
    return {'input': source_document(), 'commands': plan.commands, 'records': plan.records,
            'output': document_from_bundle(plan.bundle)}


def test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit():
    golden = json.loads(FIXTURE.read_text())
    assert portable_golden() == golden
    original = bundle_from_document(golden['input'])
    before = copy.deepcopy(original)
    plan = execute(original, json.loads(json.dumps(golden['commands'])))
    assert plan.records == golden['records']
    assert document_from_bundle(plan.bundle) == golden['output']
    assert original == before
    parent = plan.bundle['parent']
    assert [row['id'] for row in parent['config']['tracks']] == ['V1', 'V2', 'V3']
    assert [(row['id'], row['track'], row['at'], row['hold']) for row in parent['clips']] == [
        ('clip-1', 'V2', 1, 2), ('clip-2', 'V3', 3, 2)]
    assert 'pinnedShotGroups' not in parent['config']
    assert plan.commands[1]['resolved'] == [member['clip'] for member in MEMBERS]
    assert plan.commands[1]['args']['members'] == MEMBERS
    assert plan.records[0]['created'] == [{'ref': 'parent/track:V3', 'kind': 'track', 'owner': 'parent'}]
    assert plan.records[1]['created'] == []
    assert replay(plan, original).records == plan.records
    assert document_from_bundle(reload(plan.bundle)) == golden['output']
    undone = inverse(reload(plan.bundle), plan.records)
    assert authored(undone.bundle) == authored(original)
    redone = inverse(reload(undone.bundle), accepted_boundaries(undone.records, plan.bundle, undone.bundle))
    assert document_from_bundle(redone.bundle) == golden['output']


@pytest.mark.parametrize('codec', ['at', 'at_ms', 'both'])
def test_shared_rational_quantized_delta_preserves_windows_holds_and_opaque(codec):
    check_rational_move(codec, {'numerator': 30000, 'denominator': 1001})


def check_rational_move(codec, fps):
    original = basis()
    original['parent']['config']['output']['fps'] = fps
    for row in original['parent']['clips']:
        row.update(at=row['at'] + .0123, hold=4, speed=2, **{'from': 7, 'to': 11},
                   opaque={'ordered': [None, False, {}, []]}, app={'opaque': None})
        if codec in ('at_ms', 'both'):
            row['at_ms'] = row['at'] * 1000
        if codec == 'at_ms':
            del row['at']
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    plan = execute(original, [capture(original, on=3.004)])
    rows = plan.bundle['parent']['clips']
    def start(row):
        return row.get('at', row.get('at_ms', 0) / 1000)
    assert start(rows[1]) == pytest.approx(90 * 1001 / 30000)
    assert start(rows[1]) - start(rows[0]) == pytest.approx(2)
    assert start(rows[1]) == 90 * 1001 / 30000
    assert start(rows[0]) == float(Fraction(90 * 1001, 30000) - 2)
    for row, prior in zip(rows, original['parent']['clips']):
        for key in ('from', 'to', 'hold', 'speed', 'opaque'):
            assert row[key] == prior[key]
        assert row['app']['opaque'] is None
        assert row['app']['astrid']['for'] == 2
    assert inverse(reload(plan.bundle), plan.records).bundle['parent'] == original['parent']
    assert next(d for d in plan.records[0]['dependencies'] if d['key'] == 'move.quantization')['pin'] == {
        'numerator': 30000, 'denominator': 1001, 'rounding': 'half-toward-positive-infinity'}
    return plan


@pytest.mark.parametrize('codec', ['at', 'at_ms', 'both'])
def test_shared_rational_quantized_delta_accepts_main_list_rate_spelling(codec):
    plan = check_rational_move(codec, [30000, 1001])
    mapping = check_rational_move(codec, {'numerator': 30000, 'denominator': 1001})
    assert plan.bundle['parent']['clips'] == mapping.bundle['parent']['clips']
    for field in ('writes', 'dependencies', 'bindings', 'selections', 'created'):
        assert plan.records[0][field] == mapping.records[0][field]


def test_literal_zero_and_whole_candidate_excludes_moving_old_locations():
    original = basis()
    # First clip lands directly over clip-2's old location; clip-2 is moving away.
    plan = execute(original, [capture(original, on=4)])
    assert State(plan.bundle).entity('parent/clip:clip-1')['at'] == 2
    members = [{'clip': 'parent/clip:clip-1', 'track': 'parent/track:V1'},
               {'clip': 'parent/clip:clip-2', 'track': 'parent/track:V2'}]
    command = capture_move_set(original, members, 'parent/clip:clip-1', 0)
    assert State(execute(original, [command]).bundle).entity('parent/clip:clip-1')['at'] == 0
    with pytest.raises(CommandError, match='zero'):
        capture(original, on=0)


@pytest.mark.parametrize('at,passes', [(0, True), (5, True), (3, False), (4.99, False)])
def test_half_open_destination_contacts_and_real_blockers(at, passes):
    original = basis()
    blocker = {'id': 'blocker', 'at': at, 'hold': 1, 'track': 'V3', 'clipType': 'hold'}
    change(original, 'parent/clip:blocker', [], blocker)
    before = copy.deepcopy(original)
    if passes:
        execute(original, [capture(original)])
    else:
        with pytest.raises(CommandError) as error:
            capture(original)
        assert error.value.kind == 'lane_conflict'
    assert original == before


def test_new_overlap_between_members_refuses_before_any_writes():
    original = basis()
    change(original, 'parent/clip:clip-2', ['at'], 1)
    members = [dict(member, track='parent/track:V3') for member in MEMBERS]
    before = copy.deepcopy(original)
    with pytest.raises(CommandError, match='member overlap'):
        capture(original, members)
    assert original == before


@pytest.mark.parametrize('edit', ['at', 'opaque', 'new-member'])
def test_disjoint_lane_changes_rebase_and_survive_inverse(edit):
    original = basis()
    row = {'id': 'other', 'at': 10, 'hold': 1, 'track': 'V1', 'clipType': 'hold'}
    if edit != 'new-member':
        change(original, 'parent/clip:other', [], row)
    plan = execute(original, [capture(original)])
    head = copy.deepcopy(original)
    path, value = ([], row) if edit == 'new-member' else ([edit], 20 if edit == 'at' else {'new': None})
    intervening = [change(head, 'parent/clip:other', path, value)]
    rebased = replay(plan, head, intervening_records=intervening)
    assert State(rebased.bundle).entity('parent/clip:other') == State(head).entity('parent/clip:other')
    undone = inverse(rebased.bundle, plan.records, intervening)
    assert undone.bundle['parent'] == head['parent']


@pytest.mark.parametrize('kind', ['lane-entry-aba', 'lane-root-aba', 'source', 'member', 'order'])
def test_membership_predicates_sources_and_aba_refuse_atomically(kind):
    original = basis()
    row = {'id': 'other', 'at': 10, 'hold': 1, 'track': 'V1', 'clipType': 'hold'}
    change(original, 'parent/clip:other', [], row)
    plan = execute(original, [capture(original)])
    head = copy.deepcopy(original)
    intervening = []
    if kind == 'lane-entry-aba':
        intervening = [change(head, 'parent/clip:other', ['track'], 'V3'),
                       change(head, 'parent/clip:other', ['track'], 'V1')]
    elif kind == 'lane-root-aba':
        intervening = [change(head, 'parent/clip:other', [], dict(row, track='V3')),
                       change(head, 'parent/clip:other', [], row)]
    elif kind == 'source':
        change(head, 'parent/clip:clip-1', ['speed'], 2)
    elif kind == 'member':
        State(head).set('parent/clip:clip-1', [], ABSENT)
        head['parent']['config']['clips'] = copy.deepcopy(head['parent']['clips'])
    elif kind == 'order':
        head['parent']['clips'].reverse()
        head['parent']['config']['clips'] = copy.deepcopy(head['parent']['clips'])
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        replay(plan, head, intervening_records=intervening)
    assert head == before
    if intervening:
        with pytest.raises(CommandError) as error:
            inverse(plan.bundle, plan.records, intervening)
        assert error.value.kind == 'intervening_write'


@pytest.mark.parametrize('staged', [False, True])
@pytest.mark.parametrize('values', [(2,), (3, 2)], ids=['same-value', 'aba'])
def test_forward_equal_value_aba_accepts_original_guards(staged, values):
    if staged:
        original, plan = staged_drag()
    else:
        original = basis()
        row = {'id': 'other', 'at': 10, 'hold': 1, 'track': 'V1', 'clipType': 'hold'}
        change(original, 'parent/clip:other', [], row)
        plan = execute(original, [capture(original)])
    head = copy.deepcopy(original)
    before, records, commands = copy.deepcopy((head, plan.records, plan.commands))
    intervening = [later('parent/clip:clip-1', ['hold'], value) for value in values]
    rebased = replay(plan, head, intervening_records=intervening)
    assert rebased.bundle == plan.bundle
    assert rebased.records == records
    assert rebased.commands == commands
    assert plan.records == records
    assert head == before
    with pytest.raises(CommandError) as error:
        inverse(plan.bundle, plan.records, intervening)
    assert error.value.kind == 'intervening_write'


def test_forward_changed_membership_refuses_atomically():
    original = basis()
    plan = execute(original, [capture(original)])
    head = copy.deepcopy(original)
    change(head, 'parent/clip:blocker', [],
           {'id': 'blocker', 'at': 3, 'hold': 1, 'track': 'V3', 'clipType': 'hold'})
    before, records = copy.deepcopy((head, plan.records))
    with pytest.raises(CommandError) as error:
        replay(plan, head)
    assert error.value.kind == 'selection_changed'
    assert head == before
    assert plan.records == records


@pytest.mark.parametrize('site', ['clip-root', 'track-root', 'asset', 'registry-source', 'rate'])
def test_forward_source_and_identity_aba_remain_guarded(site):
    original = basis()
    change(original, 'parent/clip:clip-1', ['asset'], 'picture')
    original['parent']['registry']['assets']['picture'] = {'media_id': 'media-1'}
    plan = execute(original, [capture(original)])
    head = copy.deepcopy(original)
    if site in ('clip-root', 'track-root'):
        ref = 'parent/clip:clip-1' if site == 'clip-root' else 'parent/track:V3'
        value = copy.deepcopy(State(head).entity(ref))
        intervening = [change(head, ref, [], value)]
    else:
        ref, path, value = {
            'asset': ('parent/clip:clip-1', ['asset'], 'other-picture'),
            'registry-source': ('parent/registry', ['assets', 'picture', 'media_id'], 'media-2'),
            'rate': ('parent', ['config', 'output', 'fps'], 25),
        }[site]
        prior = State(head).get(ref, path)['value']
        intervening = [change(head, ref, path, value), change(head, ref, path, prior)]
    assert head == original
    before, records = copy.deepcopy((head, plan.records))
    with pytest.raises(CommandError) as error:
        replay(plan, head, intervening_records=intervening)
    assert error.value.kind == 'intervening_write'
    assert head == before
    assert plan.records == records


@pytest.mark.parametrize('field', ['expect', 'reads', 'selections', 'bindings', 'resolved', 'created'])
def test_capture_is_portable_and_claims_cannot_be_replaced(field):
    original = basis()
    command = json.loads(json.dumps(capture(original)))
    command[field] = {} if field in ('expect', 'bindings') else []
    if field == 'created':
        command[field] = ['parent/track:invented']
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(original, [command])
    assert original == before


@pytest.mark.parametrize('mutation', [
    {'on': -1}, {'on': True}, {'on': None}, {'on': float('nan')}, {'on': float('inf')},
    {'extra': True}, {'members': []}, {'members': [MEMBERS[0], MEMBERS[0]]},
    {'anchor': 'parent/clip:missing'},
    {'members': [dict(MEMBERS[0], clip='occurrence:o/clip:clip-2'), MEMBERS[1]]},
    {'members': [dict(MEMBERS[0], track='occurrence:o/track:V3'), MEMBERS[1]]},
    {'members': [dict(MEMBERS[0], extra=None), MEMBERS[1]]},
])
def test_closed_args_refuse_without_mutation(mutation):
    original = basis()
    command = {'schema_version': 1, 'op': 'clip.move-set', 'version': '1', 'select': 'parent',
               'args': {'members': MEMBERS, 'anchor': 'parent/clip:clip-2', 'on': 3, **mutation}}
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(original, [command])
    assert original == before


@pytest.mark.parametrize('changes', [
    {'time_map': {}}, {'timeMap': []}, {'children': []}, {'from_ms': 0},
    {'on': 'word:x:0'}, {'anchor': 'cut:x'}, {'clipType': 'shot'}, {'active': False},
    {'app': {'astrid': {'on': 'word:x:0'}}}, {'app': {'until': 'end'}},
    {'app': {'astrid': {'sequence': {}}}}, {'app': {'astrid': {'formulas': {}}}},
    {'app': {'astrid': {'for': 'word:x:0'}}}, {'app': {'astrid': {'fixed_start': False}}},
])
def test_unsupported_clips_refuse_unchanged(changes):
    original = basis()
    row = State(original).entity('parent/clip:clip-1')
    change(original, 'parent/clip:clip-1', [], dict(row, **changes))
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        capture(original)
    assert original == before


@pytest.mark.parametrize('changes', [{'role': 'source'}, {'role': None}, {'kind': 'audio'},
                                     {'active': False}, {'id': 'other'}])
def test_lane_identity_role_kind_activity_are_bound(changes):
    original = basis()
    plan = execute(original, [capture(original)])
    head = copy.deepcopy(original)
    State(head).entity('parent/track:V3').update(changes)
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        replay(plan, head)
    with pytest.raises(CommandError):
        capture(head)
    assert head == before


def test_groups_intents_and_occupied_created_ids_refuse_whole_batch():
    original, plan = staged_drag()
    for shape in ([{'shotId': 'legacy', 'clipIds': ['clip-1', 'clip-2']}], {}, False):
        head = copy.deepcopy(original)
        head['parent']['config']['pinnedShotGroups'] = shape
        with pytest.raises(CommandError):
            execute(head, plan.commands)
    for intent in ({'ownership': 'shared'}, {'ripple': 'insert'}, {'anchor': 'follow'}):
        calls = copy.deepcopy(plan.commands)
        calls[1]['intent'] = intent
        with pytest.raises(CommandError):
            execute(original, calls)
    for occupied in (basis(), plan.bundle):
        before = copy.deepcopy(occupied)
        with pytest.raises(CommandError) as error:
            execute(occupied, plan.commands)
        assert error.value.kind == 'identity_collision'
        assert occupied == before
    assert [row['id'] for row in original['parent']['config']['tracks']] == ['V1', 'V2']


def test_created_track_surviving_dependent_refuses_after_own_moves_are_reversed():
    original, plan = staged_drag()
    head = copy.deepcopy(plan.bundle)
    # A later declared audio reference survives scratch reversal of our own clips.
    head['parent']['config']['audio'] = [{'id': 'later', 'track': 'V3'}]
    before = copy.deepcopy(head)
    with pytest.raises(CommandError) as error:
        inverse(head, plan.records)
    assert error.value.kind == 'surviving_dependents'
    assert head == before
    with pytest.raises(CommandError) as error:
        inverse(plan.bundle, plan.records, [later('parent/track:V3', ['id'], 'V3')])
    assert error.value.kind == 'intervening_write'


def test_create_and_two_own_move_stages_have_exact_inverse_and_redo():
    original, first = staged_drag()
    second = capture(first.bundle, on=4)
    plan = execute(original, [*first.commands, second])
    undone = inverse(reload(plan.bundle), plan.records)
    assert authored(undone.bundle) == authored(original)
    redone = inverse(reload(undone.bundle), accepted_boundaries(undone.records, plan.bundle, undone.bundle))
    assert authored(redone.bundle) == authored(plan.bundle)


def test_source_registry_reads_and_same_value_assignments_remain_guarded():
    original = basis()
    change(original, 'parent/clip:clip-1', ['asset'], 'picture')
    original['parent']['registry']['assets']['picture'] = {
        'media_id': 'media-1', 'object_id': 'object-1', 'digest': 'sha256:' + '1' * 64,
        'opaque': {'keep': None}}
    plan = execute(original, [capture(original)])
    dependencies = plan.records[0]['dependencies']
    assert next(d for d in dependencies if d['key'] == 'move.member:1.source')['pin']['source']['media_id'] == 'media-1'
    head = copy.deepcopy(original)
    head['parent']['registry']['assets']['picture']['media_id'] = 'media-2'
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        replay(plan, head)
    assert head == before
    # An authored unchanged lane assignment is still an ABA conflict site.
    members = [dict(member, track='parent/track:V2') if member['clip'].endswith('clip-2')
               else dict(member, track='parent/track:V1') for member in MEMBERS]
    same = execute(original, [capture(original, members, on=2)])
    ref = 'parent/clip:clip-1'
    assert {'ref': ref, 'path': ['track'], 'before': present('V1'),
            'after': present('V1')} in same.records[0]['writes']
    with pytest.raises(CommandError) as error:
        inverse(same.bundle, same.records, [later(ref, ['track'], 'V1')])
    assert error.value.kind == 'intervening_write'


def test_inactive_lane_members_do_not_block_but_their_activity_is_guarded():
    original = basis()
    row = {'id': 'inactive', 'at': 3, 'hold': 2, 'track': 'V3', 'clipType': 'hold', 'active': False}
    change(original, 'parent/clip:inactive', [], row)
    plan = execute(original, [capture(original)])
    head = copy.deepcopy(original)
    intervening = [change(head, 'parent/clip:inactive', ['active'], True),
                   change(head, 'parent/clip:inactive', ['active'], False)]
    with pytest.raises(CommandError) as error:
        replay(plan, head, intervening_records=intervening)
    assert error.value.kind == 'intervening_write'


@pytest.mark.parametrize('changes', [{'hold': -1}, {'hold': 'unknown'}, {'speed': 0},
                                     {'at_ms': 123}, {'from': 4, 'to': 2, 'hold': None}])
def test_invalid_source_timing_is_a_command_refusal(changes):
    original = basis()
    row = State(original).entity('parent/clip:clip-1')
    change(original, 'parent/clip:clip-1', [], dict(row, **changes))
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        capture(original)
    assert original == before


def test_schema_closes_args_select_intent_and_member_refs():
    schema = json.loads((Path(__file__).parents[2] / 'astrid/core/timeline/schema/edit-command.schema.json').read_text())
    validator = Draft202012Validator(schema)
    command = capture(basis())
    validator.validate(command)
    for key, value in [('select', 'occurrence:o'), ('intent', {'ownership': 'shared'}),
                       ('args', dict(command['args'], extra=None))]:
        assert list(validator.iter_errors(dict(command, **{key: value})))
