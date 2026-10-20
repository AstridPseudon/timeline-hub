"""Canonical equivalent of the two pinned App group gestures; no legacy writer."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import _digest, _manifest, bundle_from_document, document_from_bundle
from astrid.sdk.timeline.occurrence_commands import capture_occurrence_move
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse, later
from tests.sdk.test_timeline_commit_provider_document import document_fixture

FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_occurrence_move.json'
OWNER = 'occurrence:occ-a'


def group_document():
    doc = document_fixture()
    parent = doc['parent_revision']['payload']
    parent['clips'] = parent['config']['clips'] = []
    parent['config']['tracks'] = [{'id': name, 'kind': 'visual', 'opaque': [None, name]}
                                  for name in ('V1', 'V2')]
    parent['config']['output']['fps'] = 30
    for i, row in enumerate(parent['occurrences']):
        row.update(source_offset=0, speed=1, duration_ms=4000, track='V1',
                   provenance={'group_migration': {'legacy_group': {
                       'shotId': 'shot-1', 'clipIds': ['clip-1', 'clip-2'], 'mode': 'images',
                       'opaque': [None]}, 'members': [
                           {'legacy_clip_id': c, 'clip_id': c} for c in ('clip-1', 'clip-2')]}})
        row['placement'] = {'start_ms': i * 10000, 'track': 'V1'}
    child = doc['internal_timeline_revisions'][0]['payload']
    child['output']['fps'] = 30
    child['tracks'] = [copy.deepcopy(parent['config']['tracks'][0])]
    for i, clip in enumerate(child['clips']):
        clip.update(id=f'clip-{i + 1}', at=i * 2, track='V1')
    for image in (doc['parent_revision'], *doc['shot_revisions'], *doc['internal_timeline_revisions']):
        image['content_digest'] = _digest(image['payload'])
    doc['dependency_manifest'] = _manifest(doc['shot_revisions'], doc['internal_timeline_revisions'],
                                         doc['dependency_manifest']['media'], [])
    return doc


def capture(bundle, on=1, track='parent/track:V2', owner=OWNER):
    return capture_occurrence_move(bundle, owner, on, track=track)


def test_portable_golden_both_gestures_roundtrip_reload_inverse_redo():
    for case in json.loads(FIXTURE.read_text())['cases']:
        original = bundle_from_document(case['input'])
        before = copy.deepcopy(original)
        calls = []
        staged = original
        if 'create_track' in case:
            calls.append(capture_track_create(original, 'parent', case['create_track']))
            staged = execute(original, calls).bundle
        calls.append(capture_occurrence_move(staged, **case['request']))
        for command in calls:
            command['group_id'] = 'group-drag'
        assert calls == case['commands']
        for command in calls:
            validate_command(command)
        plan = execute(original, json.loads(json.dumps(calls)))
        assert plan.records == case['records']
        output = document_from_bundle(plan.bundle)
        assert output == case['output']
        assert original == before
        assert replay(plan, original).commands == calls
        assert inverse(plan.bundle, plan.records).bundle == original
        reloaded = bundle_from_document(output)
        undone = inverse(reloaded, plan.records)
        assert document_from_bundle(undone.bundle, source_bundles=[original]) == case['input']
        redone = inverse(undone.bundle, undone.records)
        assert document_from_bundle(redone.bundle) == output
        state = State(reloaded)
        children = state.collection(OWNER, 'clip')
        assert [(c['id'], c['at'], c['hold'], c['track']) for c in children] == [
            ('clip-1', 0, 2, case['request']['track'].split(':')[-1]),
            ('clip-2', 2, 2, case['request']['track'].split(':')[-1])]
        assert state.occurrence(OWNER)['provenance'] == State(original).occurrence(OWNER)['provenance']
        # The sibling keeps its original shared shot and revision.
        assert output['parent_revision']['payload']['occurrences'][1] == case['input']['parent_revision']['payload']['occurrences'][1]
        assert case['input']['shot_revisions'][0] in output['shot_revisions']


def test_placement_only_reuses_shared_images_and_preserves_windows_opaque_and_children():
    original = bundle_from_document(group_document())
    before = copy.deepcopy(original)
    plan = execute(original, [capture(original, on=0, track=None)])
    assert State(plan.bundle).collection(OWNER, 'clip') == State(before).collection(OWNER, 'clip')
    output = document_from_bundle(plan.bundle)
    assert output['shot_revisions'] == group_document()['shot_revisions']
    assert output['internal_timeline_revisions'] == group_document()['internal_timeline_revisions']
    assert all(w['ref'] == OWNER for w in plan.records[0]['writes'])
    assert inverse(plan.bundle, plan.records).bundle == before


def test_independent_occurrences_and_lanes_rebase_without_global_row_guards():
    original = bundle_from_document(group_document())
    # B is on the other lane in both parent and raw child authoring.
    state = State(original)
    b = 'occurrence:occ-b'
    state.occurrence(b)['track'] = state.occurrence(b)['placement']['track'] = 'V2'
    state.collection(b, 'track').append(copy.deepcopy(state.entity('parent/track:V2')))
    for clip in state.collection(b, 'clip'):
        clip['track'] = 'V2'
    a = execute(original, [capture(original, on=1, track=None)])
    other = execute(original, [capture(original, on=12, track=None, owner=b)])
    rebased = replay(a, other.bundle, intervening_records=other.records)
    assert State(rebased.bundle).occurrence(b)['placement']['start_ms'] == 12000
    assert inverse(rebased.bundle, rebased.records).bundle == other.bundle


@pytest.mark.parametrize('kind', ['occurrence', 'parent-clip'])
def test_half_open_contact_and_complete_output_extent(kind):
    original = bundle_from_document(group_document())
    if kind == 'occurrence':
        blocker = State(original).occurrence('occurrence:occ-b')
        blocker['track'] = blocker['placement']['track'] = 'V2'
        blocker['placement']['start_ms'] = 5000
    else:
        clip = {'id': 'blocker', 'track': 'V2', 'at': 5, 'hold': 4, 'clipType': 'text'}
        original['parent']['clips'] = [clip]
        original['parent']['config']['clips'] = copy.deepcopy([clip])
    assert execute(original, [capture(original, on=1)])
    with pytest.raises(CommandError, match='overlaps'):
        capture(original, on=1 + 1 / 30)
    with pytest.raises(CommandError, match='overlaps'):
        capture(original, on=5)
    assert execute(original, [capture(original, on=9)])


@pytest.mark.parametrize('damage', ['member-add', 'member-order', 'raw-track', 'extent', 'map',
    'parent-track', 'source-pin', 'missing-pin', 'occupied-child-track', 'shared-owner', 'legacy'])
def test_relevant_changes_refuse_atomically(damage):
    original = bundle_from_document(group_document())
    command = capture(original)
    head = copy.deepcopy(original)
    state = State(head)
    if damage == 'member-add':
        state.collection(OWNER, 'clip').append(dict(state.collection(OWNER, 'clip')[0], id='extra'))
    elif damage == 'member-order':
        state.collection(OWNER, 'clip').reverse()
    elif damage == 'raw-track':
        state.collection(OWNER, 'clip')[1]['track'] = 'V2'
    elif damage == 'extent':
        state.occurrence(OWNER)['duration_ms'] = 3000
    elif damage == 'map':
        state.occurrence(OWNER)['speed'] = 2
    elif damage == 'parent-track':
        state.entity('parent/track:V2')['role'] = 'source'
    elif damage in ('source-pin', 'missing-pin'):
        pin = state.entity(OWNER + '/registry')['assets']['picture']
        pin['media_id'] = 'sha256:' + '2' * 64
        if damage == 'missing-pin':
            pin.clear()
    elif damage == 'occupied-child-track':
        state.collection(OWNER, 'track').append({'id': 'V2', 'kind': 'audio'})
    elif damage == 'shared-owner':
        state.occurrence('occurrence:occ-b')['shot_id'] = state.occurrence(OWNER)['shot_id']
    else:
        head['parent']['config']['pinnedShotGroups'] = [{'shotId': 'unknown'}]
    before = copy.deepcopy(head)
    with pytest.raises(CommandError):
        execute(head, [command])
    assert head == before


@pytest.mark.parametrize('path,value', [(['track'], 'V1'), (['at'], 0), ([], None)])
def test_member_and_geometry_aba_refuse_rebase_and_inverse(path, value):
    original = bundle_from_document(group_document())
    plan = execute(original, [capture(original)])
    ref = OWNER + '/clip:clip-1'
    if not path:
        value = State(original).entity(ref)
    writes = [later(ref, path, value)]
    with pytest.raises(CommandError, match='intervening'):
        replay(plan, original, intervening_records=writes)
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, writes)


@pytest.mark.parametrize('kind', ['occurrence', 'parent-clip'])
def test_lane_membership_aba_and_other_lane_activity_exclusion(kind):
    original = bundle_from_document(group_document())
    state = State(original)
    if kind == 'occurrence':
        ref = 'occurrence:occ-b'
        row = state.entity(ref)
        row.pop('placement')
        row['track'] = 'V1'
    else:
        ref = 'parent/clip:blocker'
        row = {'id': 'blocker', 'track': 'V1', 'at': 10, 'hold': 2}
        original['parent']['clips'] = [row]
        original['parent']['config']['clips'] = copy.deepcopy([row])
    plan = execute(original, [capture(original)])
    events = [{'writes': [{'ref': ref, 'path': ['track'], 'before': present('V1'), 'after': present('V2')}]},
              {'writes': [{'ref': ref, 'path': ['track'], 'before': present('V2'), 'after': present('V1')}]}]
    for baseline, operation in ((original, lambda h: replay(plan, h, intervening_records=events)),
                                (plan.bundle, lambda h: inverse(h, plan.records, events))):
        with pytest.raises(CommandError, match='intervening'):
            operation(baseline)
    harmless = [later(ref, ['active'], True)]
    assert replay(plan, original, intervening_records=harmless).bundle == plan.bundle


def test_created_child_track_reverses_own_consumers_but_refuses_later_dependents_and_collision():
    original = bundle_from_document(group_document())
    plan = execute(original, [capture(original)])
    assert plan.commands[0]['created'] == [OWNER + '/track:V2']
    assert inverse(plan.bundle, plan.records).bundle == original
    head = copy.deepcopy(plan.bundle)
    State(head).config(OWNER)['effects'] = [{'track_ref': OWNER + '/track:V2', 'opaque': None}]
    with pytest.raises(CommandError) as error:
        inverse(head, plan.records)
    assert error.value.kind == 'surviving_dependents'
    occupied = copy.deepcopy(original)
    State(occupied).collection(OWNER, 'track').append(copy.deepcopy(State(occupied).entity('parent/track:V2')))
    with pytest.raises(CommandError) as error:
        execute(occupied, plan.commands)
    assert error.value.kind == 'identity_collision'


@pytest.mark.parametrize('field,value', [('args', {'on': 1, 'track': None}),
    ('args', {'on': 1, 'track': 'V2'}), ('args', {'on': 1, 'track': 'occurrence:occ-a/track:V2'}),
    ('args', {'on': -1}), ('args', {'on': float('nan')}), ('args', {'on': True}),
    ('intent', {'ownership': 'shared'}), ('select', OWNER + '/clip:clip-1'),
    ('resolved', []), ('reads', []), ('selections', []), ('bindings', {}), ('created', [])])
def test_closed_contract_and_authoritative_capture(field, value):
    original = bundle_from_document(group_document())
    command = capture(original)
    command[field] = value
    with pytest.raises(CommandError):
        execute(original, [command])


@pytest.mark.parametrize('kind', ['occurrence', 'parent-clip', 'raw-parent-array'])
@pytest.mark.parametrize('field,excluded,included', [
    ('enabled', False, True), ('active', False, True), ('disabled', True, False),
    ('hidden', True, False), ('deleted', True, False)])
def test_excluded_destination_membership_aba_refuses_without_guarding_other_lanes(
        kind, field, excluded, included):
    original = bundle_from_document(group_document())
    if kind == 'occurrence':
        ref = 'occurrence:occ-b'
        row = State(original).entity(ref)
        row['track'] = row['placement']['track'] = 'V2'
    else:
        ref = 'parent/clip:blocker'
        row = {'id': 'blocker', 'track': 'V2', 'at': 20, 'hold': 2}
        original['parent']['clips'] = [row]
    row[field] = excluded
    original['parent']['config']['clips'] = copy.deepcopy(original['parent']['clips'])
    plan = execute(original, [capture(original)])
    events = [{'writes': [{'ref': ref, 'path': [field], 'before': present(excluded),
                          'after': present(included)}]},
              {'writes': [{'ref': ref, 'path': [field], 'before': present(included),
                          'after': present(excluded)}]}]
    if kind == 'raw-parent-array':
        included_rows = [dict(row, **{field: included})]
        events = [{'writes': [{'ref': 'parent', 'path': ['config', 'clips'],
                              'before': present([row]), 'after': present(included_rows)}]},
                  {'writes': [{'ref': 'parent', 'path': ['clips'],
                              'before': present(included_rows), 'after': present([row])}]}]
    with pytest.raises(CommandError, match='intervening'):
        replay(plan, original, intervening_records=events)
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, events)
    # A write which leaves the exclusion predicate false is independent.
    assert replay(plan, original, intervening_records=[later(ref, ['at'], 20)]).bundle == plan.bundle


@pytest.mark.parametrize('field', ['at', 'start', 'start_ms', 'from_ms', 'to_ms', 'children', 'clips'])
def test_unsupported_occurrence_alias_absence_is_a_recorded_aba_guard(field):
    original = bundle_from_document(group_document())
    plan = execute(original, [capture(original)])
    assert any(read['ref'] == OWNER and read['path'] == [field]
               and read['state'] == {'state': 'absent'} for read in plan.records[0]['reads'])
    with pytest.raises(CommandError, match='intervening'):
        replay(plan, original, intervening_records=[later(OWNER, [field], None)])


def test_copied_destination_definition_is_captured_in_full():
    original = bundle_from_document(group_document())
    command = capture(original)
    head = copy.deepcopy(original)
    State(head).entity('parent/track:V2')['opaque'].append('new definition')
    with pytest.raises(CommandError, match='guard changed'):
        execute(head, [command])
    with pytest.raises(CommandError, match='intervening'):
        replay(execute(original, [command]), original,
               intervening_records=[later('parent/track:V2', ['opaque'], [None, 'V2'])])


@pytest.mark.parametrize('fps', [30, {'numerator': 30000, 'denominator': 1001}])
def test_trimmed_speed_two_members_keep_windows_order_and_opaque_data(fps):
    original = bundle_from_document(group_document())
    state = State(original)
    state.bundle['parent']['config']['output']['fps'] = fps
    for shot in state.bundle['shots'].values():
        shot['internal_timeline']['output']['fps'] = fps
    for clip in state.collection(OWNER, 'clip'):
        clip.pop('hold')
        clip.update({'from': 4, 'to': 8, 'speed': 2})
    before = copy.deepcopy(state.collection(OWNER, 'clip'))
    plan = execute(original, [capture(original, on=3)])
    assert State(plan.bundle).collection(OWNER, 'clip') == [dict(row, track='V2') for row in before]
    start = State(plan.bundle).occurrence(OWNER)['placement']['start_ms'] / 1000
    assert start == pytest.approx(3 if fps == 30 else 90 * 1001 / 30000)
    assert inverse(plan.bundle, plan.records).bundle == original


def test_compatible_existing_child_lane_is_reused_without_creation():
    original = bundle_from_document(group_document())
    state = State(original)
    state.collection(OWNER, 'track').append(copy.deepcopy(state.entity('parent/track:V2')))
    plan = execute(original, [capture(original)])
    assert plan.commands[0]['created'] == []
    assert len(State(plan.bundle).collection(OWNER, 'track')) == 2
    assert inverse(plan.bundle, plan.records).bundle == original


def test_explicit_shared_ownership_refuses_without_mutation():
    original = bundle_from_document(group_document())
    before = copy.deepcopy(original)
    with pytest.raises(CommandError) as error:
        capture_occurrence_move(original, OWNER, 1, ownership='shared')
    assert error.value.kind == 'unsupported_ownership'
    assert original == before


@pytest.mark.integration
@pytest.mark.parametrize('on,target', [(1, 'V2'), (3, 'V3')])
def test_actual_runtime_group_gesture_restart_retry_inverse_redo(tmp_path, monkeypatch, on, target):
    from tests.helpers.runtime import use_runtime

    use_runtime()
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    from astrid.sdk.timeline.commit import create_runtime_commit_service

    root = tmp_path / 'realm'
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({'slug': 'group', 'name': 'Group'})['id']
    service.create_timeline(project, 'film', idempotency_key='film')
    media = service.ingest(project, b'group-picture', media_type='image/png',
                           original_name='picture.png', idempotency_key='media')['data']['object_id']
    document = group_document()
    parent = document['parent_revision']['payload']
    parent['registry']['assets']['picture'] = {'object_id': media, 'type': 'image'}
    internal = document['internal_timeline_revisions'][0]
    internal['timeline_id'] = 'film'
    internal['payload']['registry']['assets']['picture'] = {'object_id': media, 'type': 'image'}
    shot = document['shot_revisions'][0]
    shot['payload']['items'][0]['media_id'] = media
    service.create_project_shot(project, {'shot_id': shot['shot_id'], 'name': 'Group'},
                                idempotency_key='shot')
    try:
        binding = service.set_project_shot_text_binding(project, {
            'shot_id': shot['shot_id'], 'kind': 'transcript', 'text': 'A chapter', 'expected_head': 0,
        }, idempotency_key='text')['data']
        shot['payload']['text_bindings'] = [{
            **{key: binding[key] for key in ('binding_id', 'project_id', 'shot_id', 'kind', 'slot',
                'event_stream_id', 'head', 'media_id', 'content_hash', 'mime_type', 'byte_size')},
            'text': 'A chapter',
        }]
        service.publish_parent_composition(project, 'film', {
            'project_id': project, 'timeline_id': 'film', 'expected_head': None,
            'parent_revision_id': 'group-baseline', 'parent_composition': parent,
            'internal_timeline_revisions': [{key: internal[key] for key in
                                            ('timeline_id', 'revision_id', 'payload')}],
            'shot_revisions': [{key: shot[key] for key in
                                ('shot_id', 'revision_id', 'internal_timeline_revision_id', 'payload')}],
        }, idempotency_key='baseline')

        def renderer_off(*args, **kwargs):
            raise AssertionError('commit evaluated a scene')

        monkeypatch.setattr('runtime_protocol.service.evaluate_closure', renderer_off)
        monkeypatch.setattr('runtime_protocol.visual_seam.evaluate_closure', renderer_off)
        service.register_timeline_commit_provider(create_runtime_commit_service())

        def head():
            current = service.get_project_timeline(project, 'film')
            return {'revision_id': current['head_revision_id'],
                    'publication_id': current['head_publication_id']}

        def body(calls):
            current = head()
            return {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                    'base_revision_id': current['revision_id'],
                    'base_publication_id': current['publication_id'], 'commands': calls}

        def submit(request, key):
            return service.commit_timeline(project, 'film', request, idempotency_key=key,
                publisher='group-editor', invocation_path=route_path(project, 'film'), authorize=lambda: None)

        def undo(publication):
            return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
                    'select': None, 'args': {'publications': [publication]}}

        original = service._timeline_commits()[0].revision_closure(project, 'film', head()['revision_id'])
        bundle = bundle_from_document(original)
        calls = []
        staged = bundle
        if target == 'V3':
            calls.append(capture_track_create(bundle, 'parent', {'id': 'V3', 'kind': 'visual'}))
            staged = execute(bundle, calls).bundle
        calls.append(capture_occurrence_move(staged, OWNER, on, track='parent/track:' + target))
        for command in calls:
            command['group_id'] = 'group-drag'
        request = body(calls)
        accepted = submit(request, 'drag')
        output = accepted['data']['canonical_document']
        assert output == document_from_bundle(execute(bundle, calls).bundle)
        assert output['parent_revision']['payload']['occurrences'][1] == original['parent_revision']['payload']['occurrences'][1]
        service.close()
        service = RuntimeService(root)
        service.register_timeline_commit_provider(create_runtime_commit_service())
        assert service._timeline_commits()[0].revision_closure(project, 'film', head()['revision_id']) == output
        with monkeypatch.context() as retry:
            retry.setattr('astrid.sdk.timeline.commands.execute', renderer_off)
            assert submit(request, 'drag') == accepted
        undone = submit(body([undo(accepted['receipt']['receipt_id'])]), 'undo')
        assert undone['data']['canonical_document'] == original
        retired = head()
        with pytest.raises(RuntimeErrorBase) as error:
            submit(body(calls), 'ordinary-reuse')
        assert error.value.details['reason'] == 'identity_collision'
        assert head() == retired
        redone = submit(body([undo(undone['receipt']['receipt_id'])]), 'redo')
        assert redone['data']['canonical_document'] == output
    finally:
        service.close()


def test_other_lane_atomic_retrack_rebases_and_does_not_observe_transient_aliases():
    original = bundle_from_document(group_document())
    state = State(original)
    state.collection('parent', 'track').append({'id': 'V3', 'kind': 'visual'})
    a = execute(original, [capture(original)])
    b = execute(original, [capture(original, on=12, track='parent/track:V3', owner='occurrence:occ-b')])
    rebased = replay(a, b.bundle, intervening_records=b.records)
    assert State(rebased.bundle).occurrence('occurrence:occ-b')['placement'] == {
        'start_ms': 12000, 'track': 'V3'}
    assert inverse(rebased.bundle, rebased.records).bundle == b.bundle


def test_actual_group_retrack_membership_aba_refuses_even_when_final_lane_matches():
    original = bundle_from_document(group_document())
    state = State(original)
    state.collection('parent', 'track').append({'id': 'V3', 'kind': 'visual'})
    a = execute(original, [capture(original)])
    b1 = execute(original, [capture(original, on=12, track='parent/track:V2', owner='occurrence:occ-b')])
    b2 = execute(b1.bundle, [capture(b1.bundle, on=10, track='parent/track:V3', owner='occurrence:occ-b')])
    with pytest.raises(CommandError, match='intervening'):
        replay(a, b2.bundle, intervening_records=[*b1.records, *b2.records])


@pytest.mark.xfail(strict=True, reason='M2 canonical-A shared-source shot/item creation reservations')
def test_shared_source_materialization_records_exact_shot_and_item_creations():
    # The shared root/item reservation slice must record main's exact mapping
    # before repeated-source retrack can be declared safe for integration.
    original = bundle_from_document(group_document())
    plan = execute(original, [capture(original)])
    output = document_from_bundle(plan.bundle)
    owner = output['parent_revision']['payload']['occurrences'][0]
    shot = next(row for row in output['shot_revisions'] if row['shot_id'] == owner['shot_id'])
    assert shot['shot_id'] != group_document()['shot_revisions'][0]['shot_id']
    required = {'shot:' + shot['shot_id'], *(
        'shot:' + shot['shot_id'] + '/item:' + item['item_id'] for item in shot['payload']['items'])}
    assert required <= {item['ref'] for record in plan.records for item in record['created']}
