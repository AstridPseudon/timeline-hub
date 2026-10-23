"""Attach a reachable child, retaining canonical sharing and guarded history."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _manifest, bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_occurrence_attach import capture_occurrence_attach
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse, later
from tests.editing_conformance.test_recipe_occurrence_create import birth, empty_bundle
from tests.editing_conformance.test_recipe_occurrence_duplicate import accepted

OWNER = 'occurrence:first-occurrence'


def attach(bundle, **changes):
    return capture_occurrence_attach(bundle, OWNER, **{
        'occurrence_id': 'again', 'track': 'picture', 'on': 12, 'duration': 4, **changes})


def test_sequential_attach_creates_only_occurrence_and_retains_exact_closure():
    original = empty_bundle()
    first = birth(original)
    born = execute(original, [first]).bundle
    born['shots']['first-shot']['internal_timeline']['opaque'] = [None, False, {'order': [2, 1]}]
    born['shots']['first-shot']['payload']['opaque'] = {'shot_id': 'first-shot', 'raw': None}
    before = copy.deepcopy(born)
    command = attach(born)
    plan = execute(born, [command])
    assert born == before
    assert command['created'] == ['occurrence:again']
    assert plan.records[0]['created'] == [{'ref': 'occurrence:again', 'kind': 'occurrence', 'owner': 'parent'}]
    assert [write['ref'] for write in plan.records[0]['writes']] == ['occurrence:again']
    assert plan.bundle['shots'] == born['shots']
    assert [row['occurrence_id'] for row in plan.bundle['placements']] == ['first-occurrence', 'again']
    assert plan.bundle['placements'][-1]['placement'] == {'start_ms': 12000, 'track': 'picture'}
    document = document_from_bundle(plan.bundle)
    rows = document['parent_revision']['payload']['occurrences']
    assert rows[0]['shot_id'] == rows[1]['shot_id'] == 'first-shot'
    assert rows[0]['shot_revision_id'] == rows[1]['shot_revision_id']
    assert len(document['shot_revisions']) == len(document['internal_timeline_revisions']) == 1
    assert document['shot_revisions'][0]['payload']['opaque'] == born['shots']['first-shot']['payload']['opaque']
    assert document['internal_timeline_revisions'][0]['payload'] == born['shots']['first-shot']['internal_timeline']
    assert replay(plan, born).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == born
    assert inverse(undone.bundle, accepted(undone.records, plan.bundle, undone.bundle)).bundle == plan.bundle


def test_attach_verified_destination_reload_inverse_redo_preserves_shared_siblings():
    born = execute(empty_bundle(), [birth(empty_bundle())]).bundle
    original = bundle_from_document(document_from_bundle(born))
    plan = execute(original, [attach(original)])
    document = document_from_bundle(plan.bundle)
    reloaded = bundle_from_document(document)
    undone = inverse(reloaded, accepted(plan.records, original, reloaded))
    assert document_from_bundle(undone.bundle, source_bundles=(original, reloaded)) == document_from_bundle(original)
    redone = inverse(undone.bundle, accepted(undone.records, reloaded, undone.bundle))
    assert document_from_bundle(redone.bundle, source_bundles=(original, reloaded)) == document
    assert State(plan.bundle).entity(OWNER) == State(original).entity(OWNER)


@pytest.mark.parametrize('damage', ['missing', 'source', 'child', 'track', 'order', 'occupied', 'physical', 'shot-pin'])
def test_attach_captured_source_and_destination_guards_are_atomic(damage):
    born = execute(empty_bundle(), [birth(empty_bundle())]).bundle
    original = bundle_from_document(document_from_bundle(born))
    command = attach(original)
    head = copy.deepcopy(original)
    if damage == 'missing':
        head['placements'] = []
    elif damage == 'source':
        head['placements'][0]['duration_ms'] = 9000
    elif damage == 'child':
        next(iter(head['shots'].values()))['internal_timeline']['opaque'] = True
    elif damage == 'track':
        head['parent']['config']['tracks'][0]['opaque'] = True
    elif damage == 'order':
        head['parent']['config']['tracks'].append({'id': 'extra', 'kind': 'visual'})
    elif damage == 'occupied':
        head['placements'].append({**copy.deepcopy(head['placements'][0]), 'occurrence_id': 'again'})
    elif damage == 'physical':
        document = document_from_bundle(head)
        document['parent_revision']['revision_id'] = 'equal-bytes-other-revision'
        head = bundle_from_document(document)
    else:
        document = document_from_bundle(head)
        document['shot_revisions'][0]['revision_id'] = 'equal-bytes-other-shot-revision'
        document['parent_revision']['payload']['occurrences'][0]['shot_revision_id'] = 'equal-bytes-other-shot-revision'
        from astrid.sdk.timeline.commit import _digest

        document['parent_revision']['content_digest'] = _digest(document['parent_revision']['payload'])
        document['dependency_manifest'] = _manifest(document['shot_revisions'], document['internal_timeline_revisions'], [], [])
        head = bundle_from_document(document)
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        execute(head, [command])
    assert head == before


@pytest.mark.parametrize('damage', ['foreign', 'shot', 'media', 'created', 'read', 'selection', 'managed-edge'])
def test_attach_rejects_forged_authority(damage):
    original = execute(empty_bundle(), [birth(empty_bundle())]).bundle
    command = attach(original)
    if damage == 'foreign':
        command['select'] = 'occurrence:foreign'
    elif damage in ('shot', 'media'):
        command['args'][damage] = 'guessed'
    elif damage == 'created':
        command['created'] = ['shot:forged', 'occurrence:again']
    elif damage == 'read':
        command['reads'][0]['state'] = {'state': 'absent'}
    elif damage == 'selection':
        command['selections'][0]['members'] = []
    else:
        command = {'schema_version': 1, 'op': 'doc.patch', 'version': '1', 'select': None,
                   'args': {'changes': [{'op': 'set', 'ref': 'parent',
                       'path': ['occurrences', 'occurrence_id:first-occurrence', 'shot_id'],
                       'before': {'state': 'present', 'value': 'first-shot'}, 'value': 'forged'}]}}
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(original, [command])
    assert original == before


def test_attach_undo_rejects_later_dependency_write():
    original = execute(empty_bundle(), [birth(empty_bundle())]).bundle
    plan = execute(original, [attach(original)])
    with pytest.raises(CommandError):
        inverse(plan.bundle, plan.records, [later(OWNER, ['duration_ms'], 10000)])
