"""Lossless explicit legacy admission and native migration, without Runtime writes."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.core.timeline.authoring_bundle import AuthoringBundleError
from astrid.sdk.timeline._command_state import ABSENT, CommandError
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.new_group_commands import capture_migrate_groups
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.sdk.test_timeline_commit_provider import source_fixture
from tests.sdk.test_timeline_commit_provider_document import MEDIA

FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_group_migration.json'
GROUPS = [{'legacy_shot_id': 'legacy', 'shot_id': 'new-shot', 'occurrence_id': 'new-occ'}]


def legacy_document(*, opaque_variant=False, project_id='project-1', media_id=MEDIA,
                    transcript_pin=None):
    clips = [{'id': 'before', 'track': 'V1', 'at': 10, 'hold': 1, 'text': 'ungrouped'},
             {'id': 'c1', 'track': 'V1', 'at': 0, 'hold': 2, 'asset': 'image',
              'clipType': 'media', 'params': None, 'app': {'astrid': None},
              'opaque': {'pinnedShotGroups': None, 'clipType': 'shot', 'order': [None, False, 0]}},
             {'id': 'c2', 'track': 'V1', 'at': 2, 'hold': 2, 'asset': 'image',
              'clipType': 'media', 'unknown': {'id': 'c1', 'empty': {}}},
             {'id': 'after', 'track': 'V1', 'at': 12, 'hold': 1, 'opaque': None}]
    group = {'shotId': 'legacy', 'trackId': 'V1', 'clipIds': ['c1', 'c2'], 'mode': 'images',
             'items': [], 'nullable': None, 'unknown': {'pinnedShotGroups': [None], 'clipType': 'shot'},
             'imageClipSnapshot': copy.deepcopy(clips[1:3])}
    if opaque_variant:
        group['unknown'].update({
            'provenance': {'group_migration': {'legacy_group': {
                'pinnedShotGroups': [None, [], {'clipType': 'shot'}]}}},
            'occurrences[0].provenance.group_migration.legacy_group': {
                'clipType': 'shot', 'ordered': [False, None, {}, ['c2', 'c1']]},
            'absent_sibling': None,
        })
    payload = {'config': {'clips': copy.deepcopy(clips), 'tracks': [
                   {'id': 'V1', 'kind': 'visual', 'label': 'Picture', 'unknown': [None]},
                   {'id': 'A1', 'kind': 'audio', 'label': 'Audio', 'opaque': False}],
               'output': {'fps': {'numerator': 30000, 'denominator': 1001}, 'opaque': None},
               'pinnedShotGroups': [group], 'parent_only': {'audio': [None]}},
               'clips': clips, 'occurrences': [], 'opaque': {'keep': None},
               'registry': {'assets': {'image': {'media_id': media_id, 'type': 'image', 'unknown': None}},
                            'unknown': [False, None]}}
    pin = source_fixture('transcript')['pin'] if transcript_pin is None else copy.deepcopy(transcript_pin)
    return {'schema_version': 1, 'project_id': project_id, 'timeline_id': 'film',
            'parent_revision': {'revision_id': 'legacy-parent', 'payload': payload,
                                'content_digest': _digest(payload)},
            'shot_revisions': [], 'internal_timeline_revisions': [],
            'dependency_manifest': _manifest([], [], [{'media_id': media_id, 'content_digest': media_id}], [pin])}


def plan_for(document=None):
    document = legacy_document() if document is None else document
    command = capture_migrate_groups(document, GROUPS)
    bundle = bundle_from_document(document, migration_command=command)
    return bundle, execute(bundle, [command])


def rehash(document):
    document['parent_revision']['content_digest'] = _digest(document['parent_revision']['payload'])
    return document


def test_first_group_canonical_roots_full_provenance_pins_and_portable_golden():
    _, generated = plan_for()
    golden = {'input': legacy_document(), 'commands': generated.commands,
              'records': generated.records, 'output': document_from_bundle(generated.bundle)}
    assert golden['input'] == legacy_document()
    original, plan = plan_for(golden['input'])
    assert plan.commands == golden['commands']
    assert plan.records == golden['records']
    assert document_from_bundle(plan.bundle) == golden['output']
    assert replay(plan, original).records == plan.records
    assert original == bundle_from_document(golden['input'], migration_command=plan.commands[0])
    parent = plan.bundle['parent']
    assert [r['id'] for r in parent['clips']] == ['before', 'after']
    assert parent['clips'] == parent['config']['clips']
    assert 'pinnedShotGroups' not in parent['config']
    assert parent['opaque'] == original['parent']['opaque']
    assert parent['config']['parent_only'] == original['parent']['config']['parent_only']
    occurrence = plan.bundle['placements'][0]
    assert occurrence['duration_ms'] == 4000
    assert occurrence['placement'] == {'start_ms': 0, 'track': 'V1'}
    assert occurrence['provenance']['group_migration'] == {
        'legacy_group': legacy_document()['parent_revision']['payload']['config']['pinnedShotGroups'][0],
        'members': [{'legacy_clip_id': i, 'clip_id': i} for i in ('c1', 'c2')]}
    child = plan.bundle['shots']['new-shot']
    assert child['payload'] == {'items': []}
    assert child['_created'] is True
    assert child['internal_timeline']['tracks'] == original['parent']['config']['tracks']
    assert child['internal_timeline']['registry'] == original['parent']['registry']
    assert child['internal_timeline']['clips'] == original['parent']['clips'][1:3]
    assert plan.bundle['source_mapping'] == original['source_mapping']
    output = document_from_bundle(plan.bundle)
    assert output['dependency_manifest']['media'] == golden['input']['dependency_manifest']['media']
    assert output['dependency_manifest']['documents'] == golden['input']['dependency_manifest']['documents']
    assert document_from_bundle(bundle_from_document(output)) == output
    record = plan.records[0]
    assert [s['key'] for s in record['selections']] == [
        'migration.groups', 'collection.clips', 'collection.occurrences', 'collection.shots', 'collection.tracks']
    assert record['created'] == [{'ref': 'shot:new-shot', 'kind': 'shot', 'owner': None},
                                 {'ref': 'occurrence:new-occ', 'kind': 'occurrence', 'owner': 'parent'}]
    assert all(w['path'] == [] or w['path'] == ['config', 'pinnedShotGroups'] for w in record['writes'])
    assert record['writes'][-1]['after'] == ABSENT
    validate_command(plan.commands[0])


def test_legacy_read_requires_explicit_valid_migration_command():
    document = legacy_document()
    before = copy.deepcopy(document)
    with pytest.raises(AuthoringBundleError, match='explicit timeline.migrate-groups'):
        bundle_from_document(document)
    command = {'schema_version': 1, 'op': 'track.create', 'version': '1', 'select': 'parent',
               'args': {'row': {'id': 'x', 'kind': 'visual'}}}
    with pytest.raises(AuthoringBundleError, match='legacy admission'):
        bundle_from_document(document, migration_command=command)
    capture_migrate_groups(document, GROUPS)
    assert document == before


@pytest.mark.parametrize('damage', ['interleaved', 'reordered', 'missing', 'duplicate-group',
    'duplicate-member', 'duplicate-clip', 'overlap', 'items', 'map', 'fractional-duration',
    'alias', 'lanes', 'mirrors', 'registry', 'follow', 'nested-shot', 'track-alias'])
def test_unsupported_inputs_refuse_atomically(damage):
    document = legacy_document()
    parent = document['parent_revision']['payload']
    groups, clips = parent['config']['pinnedShotGroups'], parent['clips']
    if damage == 'interleaved':
        clips.insert(2, clips.pop())
    elif damage == 'reordered':
        groups[0]['clipIds'].reverse()
    elif damage == 'missing':
        groups[0]['clipIds'].append('missing')
    elif damage == 'duplicate-group':
        groups.append(copy.deepcopy(groups[0]))
    elif damage == 'duplicate-member':
        groups[0]['clipIds'].append('c1')
    elif damage == 'duplicate-clip':
        clips.append(copy.deepcopy(clips[1]))
    elif damage == 'overlap':
        groups.append(dict(copy.deepcopy(groups[0]), shotId='other'))
    elif damage == 'items':
        groups[0]['items'] = [{'item_id': 'already-owned', 'unknown': None}]
    elif damage == 'map':
        clips[1]['time_map'] = {'source': 0}
    elif damage == 'fractional-duration':
        clips[2]['hold'] = 2.0001
    elif damage == 'alias':
        clips[1]['at_ms'] = 1
    elif damage == 'lanes':
        clips[2]['track'] = 'A1'
    elif damage == 'registry':
        parent['config']['registry'] = {'assets': {}}
    elif damage == 'follow':
        clips[1]['app'] = {'astrid': {'on': 'word:x:1'}}
    elif damage == 'nested-shot':
        clips[1]['clipType'] = 'shot'
    elif damage == 'track-alias':
        groups[0]['trackId'] = 'A1'
    parent['config']['clips'] = copy.deepcopy(clips)
    if damage == 'mirrors':
        parent['config']['clips'][1]['hold'] = 3
    rehash(document)
    before = copy.deepcopy(document)
    with pytest.raises((CommandError, AuthoringBundleError)):
        capture_migrate_groups(document, GROUPS)
    assert document == before


@pytest.mark.parametrize('damage', ['unknown-args', 'unknown-mapping', 'omitted-id', 'empty',
                                    'bad-id', 'intent', 'owner', 'resolved'])
def test_closed_contract(damage):
    command = {'schema_version': 1, 'op': 'timeline.migrate-groups', 'version': '1',
               'select': 'parent', 'args': {'groups': copy.deepcopy(GROUPS)}, 'intent': {}}
    if damage == 'unknown-args':
        command['args']['repair'] = True
    elif damage == 'unknown-mapping':
        command['args']['groups'][0]['items'] = []
    elif damage == 'omitted-id':
        del command['args']['groups'][0]['shot_id']
    elif damage == 'empty':
        command['args']['groups'] = []
    elif damage == 'bad-id':
        command['args']['groups'][0]['shot_id'] = 'bad/id'
    elif damage == 'intent':
        command['intent'] = {'ownership': 'shared'}
    elif damage == 'owner':
        command['select'] = 'occurrence:other'
    else:
        command['resolved'] = ['occurrence:new-occ']
    with pytest.raises(CommandError):
        validate_command(command)


@pytest.mark.parametrize('opaque_variant', [False, True])
def test_compiled_reload_guarded_inverse_restores_exact_legacy_then_redo_same_ids(opaque_variant):
    document = legacy_document(opaque_variant=opaque_variant)
    original, plan = plan_for(document)
    canonical = document_from_bundle(plan.bundle)
    reloaded = bundle_from_document(canonical)
    undone = inverse(reloaded, plan.records)
    assert undone.bundle['parent'] == original['parent']
    assert undone.bundle['placements'] == [] and undone.bundle['shots'] == {}
    restored = document_from_bundle(undone.bundle, source_bundles=[original])
    assert restored == document
    assert json.dumps(restored, sort_keys=True) == json.dumps(document, sort_keys=True)
    assert json.dumps(restored['parent_revision']['payload']['config']['pinnedShotGroups']) == json.dumps(
        document['parent_revision']['payload']['config']['pinnedShotGroups'])
    accepted = accepted_boundaries(undone.records, reloaded, undone.bundle)
    redone = inverse(undone.bundle, accepted)
    assert document_from_bundle(redone.bundle, source_bundles=[plan.bundle]) == canonical


def test_inverse_refuses_overlapping_aba_without_mutation():
    _, plan = plan_for()
    before = copy.deepcopy(plan.bundle)
    with pytest.raises(CommandError, match='intervening publication'):
        inverse(plan.bundle, plan.records, [later('parent', ['config', 'pinnedShotGroups'], None)])
    assert plan.bundle == before


@pytest.mark.parametrize('opaque_variant', [False, True])
def test_canonical_graph_accepts_complete_opaque_migration_provenance(opaque_variant):
    from astrid.core.timeline.shot_composition import parse_shot_composition
    from tests.timeline.test_shot_composition import load_fixture

    _, plan = plan_for(legacy_document(opaque_variant=opaque_variant))
    graph = load_fixture()
    provenance = copy.deepcopy(plan.bundle['placements'][0]['provenance'])
    graph['occurrences'][0]['provenance'] = provenance
    assert parse_shot_composition(graph)['occurrences'][0]['provenance'] == provenance
    assert json.dumps(parse_shot_composition(graph)['occurrences'][0]['provenance']) == json.dumps(provenance)


def test_captured_legacy_basis_cannot_be_used_for_ordinary_edits_or_batches():
    original, plan = plan_for()
    ordinary = {'schema_version': 1, 'op': 'track.create', 'version': '1', 'select': 'parent',
                'args': {'row': {'id': 'another', 'kind': 'visual'}}}
    for commands in ([ordinary], [plan.commands[0], ordinary]):
        with pytest.raises(CommandError, match='sole recorded migration'):
            execute(original, commands)


@pytest.mark.parametrize('damage', ['group', 'track', 'output', 'registry', 'clip', 'order'])
def test_capture_guards_full_consumed_values_and_original_membership(damage):
    original, plan = plan_for()
    head = copy.deepcopy(original)
    if damage == 'group':
        head['parent']['config']['pinnedShotGroups'][0]['nullable'] = False
    elif damage == 'track':
        head['parent']['config']['tracks'][1]['opaque'] = None
    elif damage == 'output':
        head['parent']['config']['output']['opaque'] = False
    elif damage == 'registry':
        head['parent']['registry']['unknown'].reverse()
    else:
        for rows in (head['parent']['clips'], head['parent']['config']['clips']):
            if damage == 'clip':
                rows[1]['params'] = {}
            else:
                rows.reverse()
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        replay(plan, head)
    assert head == before


def test_destination_collisions_and_forged_capture_are_atomic():
    original, plan = plan_for()
    head = copy.deepcopy(original)
    # A concurrent canonical root with either allocated identity must refuse.
    head['shots'] = copy.deepcopy(plan.bundle['shots'])
    head['placements'] = copy.deepcopy(plan.bundle['placements'])
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        execute(head, plan.commands)
    assert head == before
    for field, value in [('created', []), ('bindings', {}), ('selections', [])]:
        forged = copy.deepcopy(plan.commands[0])
        forged[field] = value
        with pytest.raises(CommandError, match=field):
            execute(original, [forged])
