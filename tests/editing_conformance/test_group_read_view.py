"""Read-only group compatibility over canonical owners, without new wire operations."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.group_view import project_group_view
from astrid.sdk.timeline.new_group_commands import _geometry
from astrid.sdk.timeline.occurrence_commands import occurrence_move
from tests.sdk.test_timeline_commit_provider_document import document_fixture


def canonical_group(*, shared=False):
    bundle = bundle_from_document(document_fixture(shared=shared))
    for placement in bundle['placements']:
        placement.update(source_offset=0, speed=1)
        placement['provenance'] = {'group_migration': {'legacy_group': {
            'shotId': 'display-only', 'trackId': 'stale', 'clipIds': ['stale'],
            'mode': 'images', 'opaque': {'pinnedShotGroups': [None], 'clipType': 'shot'},
            'nullable': None}, 'members': []}}
    return bundle


def test_view_preserves_metadata_source_windows_and_current_order_without_mutation():
    bundle = canonical_group()
    owner = 'occurrence:occ-a'
    rows = State(bundle).collection(owner, 'clip')
    rows.reverse()
    rows[0].update(hold=4, speed=2, **{'from': 7, 'to': 11})
    before = copy.deepcopy(bundle)
    view = project_group_view(bundle)
    assert bundle == before
    group = view['pinnedShotGroups'][0]
    assert group == {'shotId': 'display-only', 'trackId': 'picture',
                     'clipIds': ['clip-b', 'clip-a'], 'mode': 'images',
                     'opaque': {'pinnedShotGroups': [None], 'clipType': 'shot'}, 'nullable': None}
    assert [(clip['id'], clip['at']) for clip in view['clips'][-2:]] == [('clip-b', 5), ('clip-a', 1)]
    assert {key: view['clips'][-2][key] for key in ('hold', 'speed', 'from', 'to')} == {
        'hold': 4, 'speed': 2, 'from': 7, 'to': 11}
    assert view['output']['fps'] == {'numerator': 30000, 'denominator': 1001}
    assert view['clips'][:2] == bundle['parent']['clips']
    view['pinnedShotGroups'][0]['opaque']['pinnedShotGroups'].append(False)
    assert bundle == before


def test_duplicate_display_ids_have_distinct_explicit_canonical_owner_bindings():
    bundle = canonical_group(shared=True)
    view = project_group_view(bundle)
    bindings = [binding for binding in view['bindings'] if binding['occurrence']]
    assert [binding['clip'] for binding in bindings] == [
        owner + '/clip:' + identity for owner in ('occurrence:occ-a', 'occurrence:occ-b')
        for identity in ('clip-a', 'clip-b')]
    assert [binding['raw_child_track'] for binding in bindings] == [
        owner + '/track:picture' for owner in ('occurrence:occ-a', 'occurrence:occ-b') for _ in range(2)]
    assert [clip['at'] for clip in view['clips'][2:]] == [1, 5, 11, 15]
    assert len(view['pinnedShotGroups']) == 2
    assert all(group['shotId'] == 'display-only' for group in view['pinnedShotGroups'])


@pytest.mark.parametrize('key,value', [('source_offset', 1), ('speed', True), ('time_map', {}), ('sourceMap', {})])
def test_unsupported_source_maps_refuse_without_mutating_bundle(key, value):
    bundle = canonical_group()
    bundle['placements'][0][key] = value
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match='translation-only'):
        project_group_view(bundle)
    assert bundle == before


def test_legacy_groups_require_migration_before_compatibility_projection():
    bundle = canonical_group()
    bundle['parent']['config']['pinnedShotGroups'] = [{'shotId': 'unmigrated'}]
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError) as error:
        project_group_view(bundle)
    assert error.value.kind == 'migration_needed'
    assert bundle == before


def test_nonlegacy_occurrence_contributes_children_without_inventing_group_metadata():
    bundle = canonical_group()
    del bundle['placements'][0]['provenance']
    view = project_group_view(bundle)
    assert view['pinnedShotGroups'] == []
    assert [binding['clip'] for binding in view['bindings'][-2:]] == [
        'occurrence:occ-a/clip:clip-a', 'occurrence:occ-a/clip:clip-b']


def test_geometry_keeps_source_speed_and_half_open_span():
    assert _geometry({'at': 2, 'hold': 4, 'speed': 2, 'from': 7, 'to': 11}) == (2, 4)
    with pytest.raises(CommandError, match='fixed timing'):
        _geometry({'at': 2, 'hold': 2, 'app': {'astrid': {'on': 'word:unknown'}}})


def test_shared_source_cannot_silently_become_a_semantic_shot_birth():
    bundle = canonical_group(shared=True)
    before = copy.deepcopy(bundle)
    command = {'op': 'occurrence.move', 'select': 'occurrence:occ-a', 'args': {
        'on': 1, 'track': 'parent/track:picture', 'child_track': 'occurrence:occ-a/track:picture'}}
    ctx = Recording(copy.deepcopy(bundle), command, 0)
    with pytest.raises(CommandError) as error:
        occurrence_move(ctx, command)
    assert error.value.kind == 'unsupported_ownership'
    assert ctx.record['created'] == ctx.record['writes'] == []
    assert bundle == before
