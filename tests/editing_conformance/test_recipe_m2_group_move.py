"""Recorded legacy migration → existing lane → pure App view; no Runtime writes."""
from __future__ import annotations

import copy
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.group_view import project_group_view
from astrid.sdk.timeline.new_group_commands import capture_migrate_groups
from astrid.sdk.timeline.occurrence_commands import capture_occurrence_move
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.editing_conformance.test_recipe_m2_group_migration import legacy_document, rehash

FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_group_move.json'
OWNER = 'occurrence:new-occ'
GROUPS = [{'legacy_shot_id': 'legacy', 'shot_id': 'new-shot', 'occurrence_id': 'new-occ'}]


def migrated(*, fps=30, child_target=True, second=False):
    document = legacy_document(opaque_variant=True)
    parent = document['parent_revision']['payload']
    parent['config']['output']['fps'] = fps
    parent['config']['tracks'] += [
        {'id': 'V2', 'kind': 'visual', 'role': 'output', 'active': True, 'opaque': None},
        {'id': 'V3', 'kind': 'visual', 'label': 'Other'}]
    groups = copy.deepcopy(GROUPS)
    if second:
        parent['config']['tracks'].append({'id': 'V4', 'kind': 'visual', 'opaque': [None]})
        for identity, at in [('d1', 20), ('d2', 22)]:
            parent['clips'].append({'id': identity, 'track': 'V3', 'at': at, 'hold': 2})
        parent['config']['pinnedShotGroups'].append({
            'shotId': 'other-display', 'trackId': 'V3', 'clipIds': ['d1', 'd2'],
            'mode': 'images', 'nullable': None, 'opaque': [False]})
        groups.append({'legacy_shot_id': 'other-display', 'shot_id': 'other-shot', 'occurrence_id': 'other-occ'})
    parent['config']['clips'] = copy.deepcopy(parent['clips'])
    rehash(document)
    command = capture_migrate_groups(document, groups)
    original = bundle_from_document(document, migration_command=command)
    migration = execute(original, [command])
    # Reload proves operation uses the accepted canonical shape, not _created state.
    bundle = bundle_from_document(document_from_bundle(migration.bundle))
    if not child_target:
        bundle['shots']['new-shot']['internal_timeline']['tracks'] = [
            r for r in bundle['shots']['new-shot']['internal_timeline']['tracks'] if r['id'] != 'V2']
    return original, migration, bundle


def capture(bundle, on=1, *, owner=OWNER, track='V2', raw=None, new=None):
    return capture_occurrence_move(bundle, owner, on, track='parent/track:' + track,
                                   child_track=owner + '/track:' + (raw or track), new_child_track=new)


def test_existing_lane_exact_app_view_capture_and_portable_golden():
    original, migration, bundle = migrated()
    before = copy.deepcopy(bundle)
    commands = capture(bundle)
    plan = execute(bundle, commands)
    view = project_group_view(plan.bundle)
    assert bundle == before
    assert view == project_group_view(bundle_from_document(document_from_bundle(plan.bundle)))
    children = [r for r in view['clips'] if r['id'] in ('c1', 'c2')]
    assert [(r['id'], r['track'], r['at'], r['hold']) for r in children] == [
        ('c1', 'V2', 1, 2), ('c2', 'V2', 3, 2)]
    assert [(r['at'], r['at'] + r['hold']) for r in children] == [(1, 3), (3, 5)]
    group = view['pinnedShotGroups'][0]
    assert {k: group[k] for k in ('shotId', 'trackId', 'clipIds', 'mode')} == {
        'shotId': 'legacy', 'trackId': 'V2', 'clipIds': ['c1', 'c2'], 'mode': 'images'}
    legacy = original['parent']['config']['pinnedShotGroups'][0]
    assert group['unknown'] == legacy['unknown'] and group['nullable'] is None
    assert [b for b in view['bindings'] if b['occurrence']] == [
        {'occurrence': OWNER, 'clip': OWNER + '/clip:' + identity,
         'raw_child_track': OWNER + '/track:V2', 'parent_track': 'parent/track:V2'} for identity in ('c1', 'c2')]
    assert plan.bundle['parent'] == before['parent']
    assert plan.bundle['shots']['new-shot']['internal_timeline']['tracks'] == before['shots']['new-shot']['internal_timeline']['tracks']
    assert plan.records[0]['created'] == []
    assert all(w['path'] and w['ref'] != 'parent' for w in plan.records[0]['writes'])
    assert replay(plan, before).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    # Both gestures remain individually undoable, down to exact raw legacy bytes.
    reversed_migration = inverse(undone.bundle, migration.records)
    assert document_from_bundle(reversed_migration.bundle, source_bundles=[original]) == document_from_bundle(original)
    migration_redo = inverse(reversed_migration.bundle, accepted_boundaries(
        reversed_migration.records, undone.bundle, reversed_migration.bundle))
    assert document_from_bundle(migration_redo.bundle, source_bundles=[migration.bundle]) == document_from_bundle(migration.bundle)
    for command in commands:
        validate_command(command)
    generated = execute(before, commands)
    golden = {'input': before, 'commands': generated.commands, 'records': generated.records,
              'output': document_from_bundle(generated.bundle), 'view': project_group_view(generated.bundle)}
    assert golden == {'input': before, 'commands': plan.commands, 'records': plan.records,
                      'output': document_from_bundle(plan.bundle), 'view': view}


def test_child_track_birth_is_typed_and_in_the_same_batch_and_undo():
    _, _, bundle = migrated(child_target=False)
    row = {'id': 'raw-picture-2', 'kind': 'visual', 'role': 'output', 'active': True, 'opaque': [None]}
    commands = capture(bundle, raw=row['id'], new=row)
    assert [c['op'] for c in commands] == ['track.create', 'occurrence.move']
    assert commands[0]['created'] == [OWNER + '/track:' + row['id']]
    plan = execute(bundle, commands)
    assert [r['created'] for r in plan.records] == [[{'ref': OWNER + '/track:' + row['id'], 'kind': 'track', 'owner': OWNER}], []]
    assert all(b['raw_child_track'] == OWNER + '/track:' + row['id']
               for b in project_group_view(plan.bundle)['bindings'] if b['occurrence'])
    assert inverse(plan.bundle, plan.records).bundle == bundle
    assert inverse(inverse(plan.bundle, plan.records).bundle, inverse(plan.bundle, plan.records).records).bundle == plan.bundle
    # A later temporal gesture uses explicit raw ownership even when IDs differ.
    repeated = execute(plan.bundle, capture(plan.bundle, 2, raw=row['id']))
    assert [r['at'] for r in project_group_view(repeated.bundle)['clips'][-2:]] == [2, 4]


def test_view_uses_current_membership_order_and_source_geometry_not_provenance():
    _, _, bundle = migrated()
    child = bundle['shots']['new-shot']['internal_timeline']
    child['clips'].reverse()
    child['clips'][0].update(hold=4, speed=2, **{'from': 7, 'to': 11})
    row = bundle['placements'][0]
    row['provenance']['group_migration']['legacy_group']['clipIds'] = ['stale', 'missing']
    row['provenance']['group_migration']['members'] = []
    before = copy.deepcopy(bundle)
    view = project_group_view(bundle)
    assert view['pinnedShotGroups'][0]['clipIds'] == ['c2', 'c1']
    assert [(c['id'], c['at'], c['hold']) for c in view['clips'][-2:]] == [('c2', 2, 4), ('c1', 0, 2)]
    assert {k: view['clips'][-2][k] for k in ('from', 'to', 'hold', 'speed')} == {'from': 7, 'to': 11, 'hold': 4, 'speed': 2}
    assert bundle == before


def test_rational_fps_quantization_and_half_open_adjacent_boundary():
    _, _, bundle = migrated(fps={'numerator': 30000, 'denominator': 1001})
    plan = execute(bundle, capture(bundle))
    view = project_group_view(plan.bundle)
    assert [r['at'] for r in view['clips'][-2:]] == [1.001, 3.001]
    assert view['output']['fps'] == {'numerator': 30000, 'denominator': 1001}
    # Half-open adjacency on the target lane is legal.
    _, _, adjacent = migrated()
    adjacent['parent']['clips'].append({'id': 'edge', 'track': 'V2', 'at': 5, 'hold': 1})
    adjacent['parent']['config']['clips'] = copy.deepcopy(adjacent['parent']['clips'])
    execute(adjacent, capture(adjacent))
    with pytest.raises(CommandError, match='overlaps'):
        capture(adjacent, 2)


def test_independent_groups_rebase_and_undo_preserve_other_group_and_opaque_state():
    _, _, bundle = migrated(second=True)
    first = execute(bundle, capture(bundle))
    other = execute(bundle, capture(bundle, 21, owner='occurrence:other-occ', track='V4'))
    rebased = replay(first, other.bundle, intervening_records=other.records)
    undone = inverse(rebased.bundle, first.records, other.records)
    assert undone.bundle == other.bundle
    assert inverse(undone.bundle, undone.records).bundle == rebased.bundle
    assert project_group_view(rebased.bundle)['pinnedShotGroups'][1] == project_group_view(other.bundle)['pinnedShotGroups'][1]
    assert State(rebased.bundle).config('occurrence:other-occ') == State(other.bundle).config('occurrence:other-occ')


@pytest.mark.parametrize('ref,path,value', [(OWNER, ['placement', 'start_ms'], 1000),
    (OWNER + '/clip:c1', ['track'], 'V2'), (OWNER + '/clip:c1', ['hold'], 2),
    ('parent/track:V2', ['active'], True), (OWNER + '/track:V1', ['role'], 'output')])
def test_equal_value_intervening_writes_are_guarded(ref, path, value):
    _, _, bundle = migrated()
    plan = execute(bundle, capture(bundle))
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later(ref, path, value)])


def test_membership_aba_and_destination_lane_aba_replay_by_final_state():
    _, _, bundle = migrated(second=True)
    plan = execute(bundle, capture(bundle))
    for records in ([later(OWNER + '/clip:extra', [], {})], [
        {'writes': [{'ref': 'occurrence:other-occ', 'path': ['track'],
                     'before': {'state': 'present', 'value': 'V3'}, 'after': {'state': 'present', 'value': 'V2'}}]},
        {'writes': [{'ref': 'occurrence:other-occ', 'path': ['track'],
                     'before': {'state': 'present', 'value': 'V2'}, 'after': {'state': 'present', 'value': 'V3'}}]}]):
        assert replay(plan, bundle, intervening_records=records).bundle == plan.bundle


@pytest.mark.parametrize('damage', ['missing-parent', 'wrong-owner', 'inactive-child', 'role', 'kind',
    'map', 'source-offset', 'relation', 'malformed-app', 'multi-lane', 'outside', 'shared', 'new-child-mismatch', 'extra-arg'])
def test_unsupported_shapes_refuse_atomically(damage):
    _, _, bundle = migrated()
    kwargs = {}
    child = State(bundle).config(OWNER)
    if damage == 'missing-parent':
        kwargs['track'] = 'absent'
    elif damage == 'wrong-owner':
        with pytest.raises(CommandError):
            capture_occurrence_move(bundle, OWNER, 1, track='parent/track:V2', child_track='occurrence:other/track:V2')
        return
    elif damage == 'inactive-child':
        child['clips'][0]['active'] = False
    elif damage == 'role':
        child['tracks'][2]['role'] = 'source'
    elif damage == 'kind':
        child['tracks'][2]['kind'] = 'audio'
    elif damage == 'map':
        bundle['placements'][0]['time_map'] = {}
    elif damage == 'source-offset':
        bundle['placements'][0]['source_offset'] = 1
    elif damage == 'relation':
        bundle['placements'][0]['app'] = {'astrid': {'on': 'next'}}
    elif damage == 'malformed-app':
        bundle['placements'][0]['app'] = True
    elif damage == 'multi-lane':
        child['clips'][1]['track'] = 'A1'
    elif damage == 'outside':
        child['clips'][1]['hold'] = 3
    elif damage == 'shared':
        bundle['placements'].append(dict(bundle['placements'][0], occurrence_id='shared'))
    elif damage == 'new-child-mismatch':
        kwargs['new'] = {'id': 'wrong', 'kind': 'visual'}
    elif damage == 'extra-arg':
        command = capture(bundle)[0]
        command['args']['unexpected'] = True
        with pytest.raises(CommandError, match='Additional properties'):
            validate_command(command)
        return
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        capture(bundle, **kwargs)
    assert bundle == before



def test_source_hold_speed_survive_move_and_group_view_preserves_unrelated_canonical_children():
    _, _, bundle = migrated(second=True)
    child = State(bundle).config(OWNER)['clips'][0]
    child.update(hold=4, speed=2, **{'from': 5, 'to': 9})
    other = copy.deepcopy(bundle['shots']['other-shot'])
    plan = execute(bundle, capture(bundle))
    view = project_group_view(plan.bundle)
    assert {k: next(c for c in view['clips'] if c['id'] == 'c1')[k]
            for k in ('at', 'hold', 'speed', 'from', 'to')} == {
                'at': 1, 'hold': 4, 'speed': 2, 'from': 5, 'to': 9}
    assert plan.bundle['shots']['other-shot'] == other
    assert view['pinnedShotGroups'][1] == project_group_view(bundle)['pinnedShotGroups'][1]
    assert inverse(plan.bundle, plan.records).bundle == bundle
    # A canonical occurrence without legacy provenance still contributes its children.
    del plan.bundle['placements'][1]['provenance']
    assert [c['id'] for c in project_group_view(plan.bundle)['clips'][-2:]] == ['d1', 'd2']


def test_failed_child_lane_birth_batch_leaves_original_untouched():
    _, _, bundle = migrated()
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match='incompatible'):
        capture(bundle, raw='caller-audio', new={'id': 'caller-audio', 'kind': 'audio'})
    assert bundle == before


def test_unrelated_lane_activity_rebases_and_inactive_destination_members_use_final_state():
    _, _, bundle = migrated(second=True)
    plan = execute(bundle, capture(bundle))
    head = copy.deepcopy(bundle)
    head['placements'][1]['active'] = False
    records = [later('occurrence:other-occ', ['active'], False)]
    assert replay(plan, head, intervening_records=records).bundle['placements'][1]['active'] is False
    bundle['parent']['clips'].append({'id': 'inactive', 'track': 'V2', 'at': 1, 'hold': 2, 'active': False})
    bundle['parent']['config']['clips'] = copy.deepcopy(bundle['parent']['clips'])
    plan = execute(bundle, capture(bundle))
    assert replay(plan, bundle,
                  intervening_records=[later('parent/clip:inactive', ['active'], False)]).bundle == plan.bundle


def test_original_app_pinned_fixture_exact_existing_lane_visible_values():
    # Authored portion of makePinnedGroupData in App useClipDrag.test.tsx:191.
    document = legacy_document()
    parent = document['parent_revision']['payload']
    parent['config']['tracks'] = [{'id': identity, 'kind': 'visual'} for identity in ('V1', 'V2')]
    parent['config']['output']['fps'] = 30
    parent['clips'] = [{'id': 'clip-1', 'at': 0, 'track': 'V1', 'clipType': 'hold', 'hold': 2},
                       {'id': 'clip-2', 'at': 2, 'track': 'V1', 'clipType': 'hold', 'hold': 2}]
    parent['config']['clips'] = copy.deepcopy(parent['clips'])
    parent['config']['pinnedShotGroups'] = [{
        'shotId': 'shot-1', 'trackId': 'V1', 'clipIds': ['clip-1', 'clip-2'], 'mode': 'images'}]
    rehash(document)
    groups = [dict(GROUPS[0], legacy_shot_id='shot-1')]
    migration_command = capture_migrate_groups(document, groups)
    migration = execute(bundle_from_document(document, migration_command=migration_command), [migration_command])
    bundle = bundle_from_document(document_from_bundle(migration.bundle))
    move = execute(bundle, capture(bundle))
    view = project_group_view(bundle_from_document(document_from_bundle(move.bundle)))
    assert [c for c in view['clips'] if c['track'] == 'V1'] == []
    assert [(c['id'], c['at'], c['at'] + c['hold'], c['track']) for c in view['clips']] == [
        ('clip-1', 1, 3, 'V2'), ('clip-2', 3, 5, 'V2')]
    assert view['pinnedShotGroups'] == [{
        'shotId': 'shot-1', 'trackId': 'V2', 'clipIds': ['clip-1', 'clip-2'], 'mode': 'images'}]
    assert inverse(move.bundle, move.records).bundle == bundle
