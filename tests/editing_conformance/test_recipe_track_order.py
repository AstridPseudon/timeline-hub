"""Small source-level proof for the native parent track order recipe."""
from __future__ import annotations

import copy
import json
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline._collections import arrange, order
from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline._track_commands import (
    capture_track_reorder,
    track_reorder_with_data_lane_placement_candidate,
)
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse


def parent_tracks(timeline):
    return State(timeline).config('parent')['tracks']


def media_track_bundle():
    timeline = bundle()
    parent_tracks(timeline).extend([
        {'id': 'audio', 'kind': 'audio', 'label': None,
         'opaque': {'null': None, 'false': False, 'zero': 0}},
        {'id': 'overlay', 'kind': 'visual', 'label': 'Overlay',
         'opaque': {'keep': [None, False, 0]}},
    ])
    timeline['parent']['config']['app'] = {
        'timelineDataLanePlacement': {'data-1': 'between'},
        'opaque': {'keep': None},
    }
    return timeline


def mixed_lane_bundle():
    timeline = media_track_bundle()
    timeline['parent']['config']['app'] = {
        'timelineDataLanePlacement': {
            'version': 1,
            'lanes': [
                {'laneId': 'astrid.transcript', 'beforeTrackId': 'overlay'},
                {'laneId': 'opaque:custom/v1', 'beforeTrackId': None},
            ],
        },
        'opaque': {'keep': None, 'false': False, 'zero': 0},
    }
    return timeline


def mixed_lane_command(original, desired_order, desired_placement):
    old_order = order(State(original), 'parent', 'track')
    old_placement = original['parent']['config']['app']['timelineDataLanePlacement']
    return {
        'schema_version': 1,
        'op': 'track.reorder',
        'version': '2',
        'select': 'parent',
        'args': {
            'order': copy.deepcopy(desired_order),
            'expected_order': copy.deepcopy(old_order),
            'data_lane_placement': copy.deepcopy(desired_placement),
            'expected_data_lane_placement': copy.deepcopy(old_placement),
        },
        'intent': {},
    }


def execute_mixed_lane_candidate(original, command):
    candidate = copy.deepcopy(original)
    ctx = Recording(candidate, command, 0)
    track_reorder_with_data_lane_placement_candidate(ctx, command)
    ctx.compile_inputs()
    ctx.compile_mirrors()
    record = ctx.finish(capture=True)
    return SimpleNamespace(bundle=ctx.state.bundle, records=[record], commands=[record['command']])


def test_parent_reorder_is_raw_lossless_and_reloadable_inverse_recipe():
    original = media_track_bundle()
    before = copy.deepcopy(original)
    old = order(State(original), 'parent', 'track')
    desired = [old[2], old[0], old[1]]

    command = capture_track_reorder(original, desired)
    plan = execute(original, [command])

    assert original == before
    assert order(State(plan.bundle), 'parent', 'track') == desired
    assert {row['id']: row for row in parent_tracks(plan.bundle)} == {
        row['id']: row for row in parent_tracks(before)
    }
    assert plan.bundle['parent']['clips'] == before['parent']['clips']
    assert plan.bundle['parent']['config']['clips'] == before['parent']['config']['clips']
    assert plan.bundle['parent']['opaque_parent'] == before['parent']['opaque_parent']
    assert plan.bundle['parent']['config']['app'] == before['parent']['config']['app']
    assert 'track_order' not in plan.bundle['parent']
    assert 'track_order' not in plan.bundle['parent']['config']
    assert plan.bundle['parent']['config']['tracks'] == [
        next(row for row in parent_tracks(before) if row['id'] == ref.rsplit(':', 1)[1])
        for ref in desired
    ]
    assert command['expect'] == {'parent::track_order': present(old)}
    assert command['authorship'] == {'parent::track_order': 'direct'}
    assert command['reads'][0]['ref'] == 'parent/collection:track'
    assert command['selections'][0] == {
        'key': 'collection.tracks',
        'query_version': 1,
        'owner': 'parent',
        'members': old,
        'order': old,
        'boundaries': old,
        'policy': 'guard-membership',
    }

    reloaded = json.loads(json.dumps(plan.bundle))
    assert replay(plan, json.loads(json.dumps(before))).bundle == reloaded
    reloaded_records = json.loads(json.dumps(plan.records))
    undone = inverse(reloaded, reloaded_records)
    assert undone.bundle == before
    redone = inverse(undone.bundle, json.loads(json.dumps(undone.records)))
    assert redone.bundle == reloaded

    equal_state = execute(original, [capture_track_reorder(original, old)])
    assert equal_state.bundle == original
    assert equal_state.records[0]['writes'][0]['before'] == equal_state.records[0]['writes'][0]['after']
    assert replay(equal_state, json.loads(json.dumps(original))).bundle == original


def test_reorder_allows_disjoint_track_leaf_rebase_but_guards_order_and_aba():
    original = media_track_bundle()
    old = order(State(original), 'parent', 'track')
    reorder = execute(original, [capture_track_reorder(original, old[::-1])])
    label = execute(original, [capture_track_set(original, 'parent/track:picture',
                                                  values={'label': 'Picture'})])

    rebased = replay(label, reorder.bundle, intervening_records=reorder.records)
    assert order(State(rebased.bundle), 'parent', 'track') == old[::-1]
    assert State(rebased.bundle).entity('parent/track:picture')['label'] == 'Picture'

    stale = copy.deepcopy(original)
    arrange(State(stale), 'parent', 'track', [old[1], old[0], old[2]])
    with pytest.raises(CommandError, match='selection|guard'):
        replay(reorder, stale)

    identity_changed = copy.deepcopy(original)
    parent_tracks(identity_changed)[0]['id'] = 'renamed'
    with pytest.raises(CommandError, match='selection|guard'):
        replay(reorder, identity_changed)

    undo = inverse(reorder.bundle, reorder.records)
    away = old[1:] + old[:1]
    with pytest.raises(CommandError, match='intervening'):
        inverse(reorder.bundle, reorder.records, [
            {'writes': [
                {'ref': 'parent', 'path': ['track_order'],
                 'before': present(reorder.commands[0]['args']['order']),
                 'after': present(away)},
            ]},
            {'writes': [
                {'ref': 'parent', 'path': ['track_order'],
                 'before': present(away),
                 'after': present(reorder.commands[0]['args']['order'])},
            ]},
        ])
    assert undo.commands[0]['op'] == 'timeline.inverse'

    away_plan = execute(reorder.bundle, [capture_track_reorder(reorder.bundle, away)])
    back_plan = execute(away_plan.bundle, [capture_track_reorder(away_plan.bundle,
                                                                   reorder.commands[0]['args']['order'])])
    assert back_plan.bundle == reorder.bundle
    with pytest.raises(CommandError, match='intervening'):
        inverse(reorder.bundle, reorder.records,
                [*away_plan.records, *back_plan.records])


def test_reorder_refuses_cross_owner_or_incomplete_membership_without_writing():
    original = media_track_bundle()
    old = order(State(original), 'parent', 'track')
    snapshot = copy.deepcopy(original)

    with pytest.raises(CommandError, match='parent/track|permutation'):
        capture_track_reorder(original, [old[0], 'occurrence:occ-1/track:picture', old[2]])
    assert original == snapshot

    command = capture_track_reorder(original, old[::-1])
    command['args']['order'] = old[:-1]
    with pytest.raises(CommandError, match='permutation|array'):
        execute(original, [command])
    assert original == snapshot

    command = capture_track_reorder(original, old[::-1])
    command['args']['order'] = [old[0], old[0], old[2]]
    with pytest.raises(CommandError, match='permutation|unique|array'):
        execute(original, [command])
    assert original == snapshot

    command = capture_track_reorder(original, old[::-1])
    command['args']['lanes'] = {'data-1': 'between'}
    with pytest.raises(CommandError, match='[Aa]dditional properties'):
        execute(original, [command])
    assert original == snapshot


def test_mixed_lane_candidate_is_closed_atomic_and_preserves_app_opaque_data():
    original = mixed_lane_bundle()
    before = copy.deepcopy(original)
    old = order(State(original), 'parent', 'track')
    desired_order = [old[2], old[0], old[1]]
    desired_placement = {
        'version': 1,
        'lanes': [
            {'laneId': 'opaque:custom/v1', 'beforeTrackId': 'picture'},
            {'laneId': 'astrid.transcript', 'beforeTrackId': 'audio'},
        ],
    }

    plan = execute_mixed_lane_candidate(
        original, mixed_lane_command(original, desired_order, desired_placement))

    assert original == before
    assert order(State(plan.bundle), 'parent', 'track') == desired_order
    assert plan.bundle['parent']['config']['app']['timelineDataLanePlacement'] == desired_placement
    assert plan.bundle['parent']['config']['app']['opaque'] == before['parent']['config']['app']['opaque']
    assert plan.bundle['parent']['config']['clips'] == before['parent']['config']['clips']
    assert {row['id']: row for row in plan.bundle['parent']['config']['tracks']} == {
        row['id']: row for row in before['parent']['config']['tracks']
    }

    record = plan.records[0]
    assert record['command']['version'] == '2'
    assert [write['path'] for write in record['writes']] == [
        ['track_order'], ['config', 'app', 'timelineDataLanePlacement']]
    assert record['command']['authorship'] == {
        'parent::track_order': 'direct',
        'parent::config.app.timelineDataLanePlacement': 'direct',
    }
    assert record['command']['reads'][-1] == {
        'ref': 'parent',
        'path': ['config', 'app', 'timelineDataLanePlacement'],
        'state': present(before['parent']['config']['app']['timelineDataLanePlacement']),
    }

    rebased_head = copy.deepcopy(original)
    State(rebased_head).entity('parent/track:picture')['label'] = 'Picture edited elsewhere'
    rebased = execute_mixed_lane_candidate(
        rebased_head, mixed_lane_command(original, desired_order, desired_placement))
    assert order(State(rebased.bundle), 'parent', 'track') == desired_order
    assert State(rebased.bundle).entity('parent/track:picture')['label'] == 'Picture edited elsewhere'

    # The existing inverse machinery consumes the two recorded authored writes
    # even while the candidate operation itself remains unregistered.
    undone = inverse(plan.bundle, json.loads(json.dumps(plan.records)))
    assert undone.bundle == before
    assert inverse(undone.bundle, json.loads(json.dumps(undone.records))).bundle == plan.bundle


def test_mixed_lane_candidate_guards_lane_identity_and_both_carriers_before_writing():
    original = mixed_lane_bundle()
    old = order(State(original), 'parent', 'track')
    desired_order = [old[2], old[0], old[1]]
    desired = {
        'version': 1,
        'lanes': [
            {'laneId': 'astrid.transcript', 'beforeTrackId': 'audio'},
            {'laneId': 'opaque:custom/v1', 'beforeTrackId': None},
        ],
    }

    command = mixed_lane_command(original, desired_order, desired)
    command['args']['data_lane_placement']['lanes'][0]['laneId'] = 'new-derived-display-id'
    with pytest.raises(CommandError, match='membership'):
        execute_mixed_lane_candidate(original, command)
    assert original == mixed_lane_bundle()

    command = mixed_lane_command(original, desired_order, desired)
    command['args']['expected_data_lane_placement']['lanes'][0]['beforeTrackId'] = 'picture'
    with pytest.raises(CommandError, match='placement changed'):
        execute_mixed_lane_candidate(original, command)
    assert original == mixed_lane_bundle()

    command = mixed_lane_command(original, desired_order, desired)
    changed = copy.deepcopy(original)
    changed['parent']['config']['app']['timelineDataLanePlacement']['lanes'].reverse()
    with pytest.raises(CommandError, match='placement changed'):
        execute_mixed_lane_candidate(changed, command)
