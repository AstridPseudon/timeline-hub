"""Explicit group migration followed by one parent track birth and retrack."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.group_view import project_group_view
from astrid.sdk.timeline.new_group_commands import capture_migrate_groups
from astrid.sdk.timeline.occurrence_commands import capture_occurrence_move
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.editing_conformance.test_recipe_m2_group_migration import legacy_document, rehash

OWNER = 'occurrence:new-occ'
GROUPS = [{'legacy_shot_id': 'legacy', 'shot_id': 'new-shot', 'occurrence_id': 'new-occ'}]
NEW_PARENT_TRACK = {
    'id': 'V3', 'kind': 'visual', 'role': 'output', 'active': True, 'opaque': [None],
}


def migrated_without_v3():
    document = legacy_document(opaque_variant=True)
    parent = document['parent_revision']['payload']
    parent['config']['output']['fps'] = 30
    parent['config']['tracks'].append(
        {'id': 'V2', 'kind': 'visual', 'role': 'output', 'active': True, 'opaque': None}
    )
    parent['config']['clips'] = copy.deepcopy(parent['clips'])
    rehash(document)

    migration = capture_migrate_groups(document, GROUPS)
    original = bundle_from_document(document, migration_command=migration)
    accepted = execute(original, [migration])
    return original, bundle_from_document(document_from_bundle(accepted.bundle))


def capture_new_parent_track_batch(bundle):
    """Reserve V3, then capture the move against the sequentially staged head."""
    create = capture_track_create(bundle, 'parent', NEW_PARENT_TRACK)
    staged = execute(bundle, [create])
    move = capture_occurrence_move(
        staged.bundle,
        OWNER,
        1,
        track='parent/track:V3',
        child_track=OWNER + '/track:V2',
    )[0]
    return [create, move]


def test_new_parent_track_batch_has_one_capture_golden_and_exact_group_view():
    original, bundle = migrated_without_v3()
    before = copy.deepcopy(bundle)
    commands = capture_new_parent_track_batch(bundle)
    plan = execute(bundle, commands)

    assert bundle == before
    assert [command['op'] for command in plan.commands] == ['track.create', 'occurrence.move']
    assert plan.commands == commands
    assert plan.commands[0]['created'] == ['parent/track:V3']
    assert plan.commands[1]['created'] == []
    assert plan.commands[1]['bindings']['move.track'] == 'parent/track:V3'
    assert plan.commands[1]['bindings']['move.child-track'] == OWNER + '/track:V2'
    assert any(dependency['key'] == 'move.images' for dependency in plan.records[1]['dependencies'])
    assert plan.records[0]['created'] == [
        {'ref': 'parent/track:V3', 'kind': 'track', 'owner': 'parent'}
    ]

    view = project_group_view(plan.bundle)
    children = [clip for clip in view['clips'] if clip['id'] in ('c1', 'c2')]
    assert [(clip['id'], clip['at'], clip['hold'], clip['track']) for clip in children] == [
        ('c1', 1, 2, 'V3'), ('c2', 3, 2, 'V3')
    ]
    expected_group = copy.deepcopy(
        original['parent']['config']['pinnedShotGroups'][0]
    )
    expected_group['trackId'] = 'V3'
    assert view['pinnedShotGroups'][0] == expected_group
    assert [binding for binding in view['bindings'] if binding['occurrence']] == [
        {'occurrence': OWNER, 'clip': OWNER + '/clip:c1',
         'raw_child_track': OWNER + '/track:V2', 'parent_track': 'parent/track:V3'},
        {'occurrence': OWNER, 'clip': OWNER + '/clip:c2',
         'raw_child_track': OWNER + '/track:V2', 'parent_track': 'parent/track:V3'},
    ]
    assert 'pinnedShotGroups' not in plan.bundle['parent']['config']


def test_new_parent_track_batch_reload_inverse_redo_and_retry_are_exact():
    _, bundle = migrated_without_v3()
    commands = capture_new_parent_track_batch(bundle)
    plan = execute(bundle, commands)
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))

    assert document_from_bundle(reloaded) == document_from_bundle(plan.bundle)
    undone = inverse(reloaded, plan.records)
    assert document_from_bundle(undone.bundle) == document_from_bundle(bundle)
    redone = inverse(undone.bundle, undone.records)
    assert document_from_bundle(redone.bundle) == document_from_bundle(plan.bundle)

    retry = execute(bundle, plan.commands)
    assert retry.records == plan.records
    assert document_from_bundle(retry.bundle) == document_from_bundle(plan.bundle)


def test_new_parent_track_refuses_later_dependent_clip_before_removing_track():
    _, bundle = migrated_without_v3()
    plan = execute(bundle, capture_new_parent_track_batch(bundle))
    dependent = execute(plan.bundle, [capture_clip_add(
        plan.bundle, 'parent', {'id': 'dependent', 'track': 'V3', 'at': 6, 'hold': 1,
                                'clipType': 'hold'})
    ])

    before = copy.deepcopy(dependent.bundle)
    with pytest.raises(CommandError, match='intervening'):
        inverse(dependent.bundle, plan.records, dependent.records)
    assert dependent.bundle == before
