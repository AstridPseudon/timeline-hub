"""Exact canonical occurrence clock, separate from frame-based group retracking."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.occurrence_commands import capture_occurrence_start
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse, later
from tests.sdk.test_timeline_commit_provider_document import document_fixture

OWNER = 'occurrence:occ-2'


@pytest.mark.parametrize('materialize', [False, True])
def test_exact_ms_preserves_multilane_children_and_canonical_materialized_source(materialize):
    document = document_fixture()
    rows = document['parent_revision']['payload']['occurrences']
    for index, row in enumerate(rows):
        row.update(source_offset=0, speed=1)
        row['placement']['start_ms'] = 10000 + 10000 * index
    rows[0]['duration_ms'] = 4150
    rows[1]['at_ms'] = 20000
    internal = document['internal_timeline_revisions'][0]['payload']
    internal.pop('source_window')
    internal['tracks'].append({'id': 'voice', 'kind': 'audio'})
    internal['clips'].append({'id': 'voice', 'track': 'voice', 'at': 0, 'hold': 1})
    for image in [document['parent_revision'], *document['internal_timeline_revisions']]:
        image['content_digest'] = _digest(image['payload'])
    document['dependency_manifest'] = _manifest(document['shot_revisions'],
        document['internal_timeline_revisions'], document['dependency_manifest']['media'], [])
    owner = 'occurrence:occ-b'
    # Opening the verified closure exercises the same source identity path as
    # provider admission. Editing one child then reloading materializes its root.
    original = bundle_from_document(document)
    if materialize:
        edit = capture_clip_set(original, owner + '/clip:clip-a', values={'hold': .75})
        assert edit['version'] == '2'
        original = bundle_from_document(document_from_bundle(execute(original, [edit]).bundle))
    before = copy.deepcopy(original)
    command = capture_occurrence_start(original, owner, 14150)
    validate_command(command)
    plan = execute(original, [command])
    assert original == before
    occurrence = State(plan.bundle).occurrence(owner)
    assert occurrence['placement']['start_ms'] == occurrence['at_ms'] == 14150
    assert plan.bundle['shots'] == before['shots']
    assert [write['path'] for write in plan.records[0]['writes']] == [
        ['placement', 'start_ms'], ['at_ms']]
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))
    assert State(reloaded).occurrence(owner)['placement']['start_ms'] == 14150
    assert replay(plan, original).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later(owner, ['placement', 'start_ms'], 14150)])


def test_exact_start_preserves_disjoint_metadata_and_guards_membership_source_and_children():
    original = bundle()
    original['placements'][0]['duration_ms'] = 4150
    plan = execute(original, [capture_occurrence_start(original, OWNER, 14150)])
    head = copy.deepcopy(original)
    head['parent']['opaque_parent']['concurrent'] = True
    assert replay(plan, head).bundle['parent']['opaque_parent']['concurrent'] is True
    for damage in ('membership', 'source', 'child'):
        head = copy.deepcopy(original)
        if damage == 'membership':
            head['placements'].reverse()
        elif damage == 'source':
            head['placements'][1]['shot_revision_id'] = 'other'
        else:
            State(head).entity(OWNER + '/clip:picture-1')['hold'] = .5
        with pytest.raises(CommandError):
            replay(plan, head)


@pytest.mark.parametrize('args', [
    {'start_ms': True}, {'start_ms': -1}, {'start_ms': 14150.5}, {'start_ms': None},
    {'start_ms': 14150, 'on': 14.15, 'track': 'parent/track:picture', 'child_track': OWNER + '/track:picture'},
])
def test_exact_start_closed_units_and_mutually_exclusive_args(args):
    with pytest.raises(CommandError):
        execute(bundle(), [{'schema_version': 1, 'op': 'occurrence.move', 'version': '1',
                            'select': OWNER, 'args': args}])


@pytest.mark.parametrize('damage', ['overlap', 'owner', 'mirror', 'speed', 'source_offset', 'map'])
def test_exact_start_refuses_unsafe_translation_atomically(damage):
    original = bundle()
    original['placements'][0]['duration_ms'] = 4150
    row = original['placements'][1]
    if damage == 'overlap':
        original['placements'][0]['duration_ms'] = 10000
    elif damage == 'owner':
        original['placements'].append(dict(row, occurrence_id='alias'))
    elif damage == 'mirror':
        row['at_ms'] = 19999
    elif damage == 'map':
        row['time_map'] = {}
    else:
        row[damage] = 2
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        capture_occurrence_start(original, OWNER, 14150)
    assert original == before
