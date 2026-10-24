"""Offline source controls for authenticated same-alias inverse observations."""
from __future__ import annotations

import copy
import json
import sys

import pytest
import runtime_protocol
from runtime_protocol.timeline_commit_auth import location, validate_sequential_capture

from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    create_runtime_commit_service,
)
from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_swap_media
from tests.editing_conformance.test_doc_patch_v2 import submit
from tests.editing_conformance.test_provider_step_undo_v2 import undo
from tests.editing_conformance.test_recipe_occurrence_media import OWNER, TARGET, MediaRealm, inputs
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedPort
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


@pytest.fixture
def source_control():
    baseline, old, new, verified = inputs()
    parent = baseline['parent_revision']
    parent['payload']['occurrences'] = parent['payload']['occurrences'][:1]
    parent['content_digest'] = _digest(parent['payload'])
    new['asset'] = old['asset']
    verified[1]['selection']['asset'] = old['asset']
    realm = MediaRealm(baseline, verified)
    command = capture_occurrence_swap_media(bundle_from_document(baseline), TARGET, old, new,
                                            verified_media=verified)
    context = realm.context([command])
    context['request']['reads'] = []
    context['invocation']['body'] = copy.deepcopy(context['request'])
    context['request_hash'] = _digest(context['invocation'])

    class MediaPort(DetachedPort):
        def selected_media(self, pin):
            selected, = [value for value in verified if value['selection'] == pin]
            return copy.deepcopy(selected)

    created = create_runtime_commit_service().commit(context, MediaPort(realm, context))
    return realm, baseline, created


@pytest.mark.parametrize('dry_run', [False, True])
def test_same_alias_inverse_observations_validate(source_control, monkeypatch, tmp_path, dry_run):
    realm, baseline, created = source_control
    captures = []
    original = DetachedPort.preview if dry_run else DetachedPort.accept

    def capture(port, packet):
        # Newly generated offline values; no custody of original11466 is claimed.
        (tmp_path / 'capture.json').write_text(json.dumps(packet, allow_nan=False))
        captures.append(copy.deepcopy(packet))

    def finish(port, prepared):
        (tmp_path / 'prepared.json').write_text(json.dumps(prepared, allow_nan=False))
        (tmp_path / 'history.json').write_text(json.dumps(realm.entries, allow_nan=False))
        with monkeypatch.context() as modules:
            modules.setitem(sys.modules, 'runtime_protocol', runtime_protocol)
            source = created['data']['canonical_document']
            try:
                validate_sequential_capture(port.context['request'], prepared, captures[-1], source, source,
                                            history={row['publication_id']: row for row in realm.entries
                                                     if row['intent'] == 'recorded'})
            except CommitRejected as error:
                assert error.failure['details']['reason'] == 'invalid_records'
                assert error.failure['message'] == 'provider observation has an ambiguous item path'
                raise
        return original(port, prepared)

    monkeypatch.setattr(DetachedPort, 'capture_sequential_execution', capture, raising=False)
    monkeypatch.setattr(DetachedPort, 'preview' if dry_run else 'accept', finish)
    result = submit(realm, undo(created['receipt']['receipt_id']), reads=[], dry_run=dry_run)
    assert result['data']['canonical_document'] == baseline


def test_source_control_has_one_item_and_a_changed_native_observation(source_control):
    realm, _, _ = source_control
    record, = realm.entries[-1]['records']['commands']
    write, = [write for write in record['writes']
              if write['ref'] == OWNER + '/shot' and write['path'][:2] == ['payload', 'items']]
    assert write['path'] == ['payload', 'items', 'item_id:item-1', 'media_id']
    assert write['before'] != write['after']
    output = realm.entries[-1]['receipt']['result']['canonical_document']
    occurrence = next(row for row in output['parent_revision']['payload']['occurrences']
                      if row['occurrence_id'] == 'occ-a')
    shot, = [image for image in output['shot_revisions']
             if image['revision_id'] == occurrence['shot_revision_id']]
    assert len(shot['payload']['items']) == 1
    original = bundle_from_document(source_control[1])
    local = State(original).occurrence(OWNER)['shot_id']
    assert shot['payload']['items'][0]['item_id'] == original['shots'][local]['payload']['items'][0]['item_id']


def test_collection_candidate_requires_source_to_authoring_item_projection():
    baseline, _, _, _ = inputs()
    bundle = bundle_from_document(baseline)
    state = State(bundle)
    shot = state.occurrence(OWNER)['shot_id']
    source = bundle['source_mapping']['shots'][shot]
    observed = state.get(OWNER + '/shot', ['payload', 'items'])['value']
    authored = bundle['shots'][shot]['payload']['items']
    # A published item and its placement-local item have distinct identities.
    assert observed[0]['item_id'] == 'item-1'
    assert source['item_id_map'][observed[0]['item_id']] == authored[0]['item_id']
    assert authored[0]['item_id'] != observed[0]['item_id']
    # Published aggregate values must preserve placement-local stored IDs.
    state.set(OWNER + '/shot', ['payload', 'items'], {'state': 'present', 'value': observed})
    assert bundle['shots'][shot]['payload']['items'] == authored
    assert bundle['shots'][shot]['payload']['items'] != observed


@pytest.mark.parametrize('reversed_order', [False, True])
def test_runtime_item_identity_uses_published_binding_not_position(monkeypatch, reversed_order):
    baseline, old, _, _ = inputs()
    state = State(bundle_from_document(baseline))
    shot = state.occurrence(OWNER)['shot_id']
    source = state.bundle['source_mapping']['shots'][shot]
    observed = state.get(OWNER + '/shot', ['payload', 'items'])['value']
    identity = observed[0]['item_id']
    authored = state.bundle['shots'][shot]['payload']['items'][0]['item_id']
    assert source['item_id_map'][identity] == authored
    assert identity != authored
    other = copy.deepcopy(observed[0])
    other.update(item_id='other:item', media_id='sha256:' + '3' * 64)
    rows = [other, *observed] if reversed_order else [*observed, other]
    monkeypatch.setitem(sys.modules, 'runtime_protocol', runtime_protocol)
    assert location({'items': rows}, ['items', 'item_id:' + identity, 'media_id']) == {
        'state': 'present', 'value': old['object_id']}
    assert location({'items': rows}, ['items', 'item_id:other:item', 'media_id']) == {
        'state': 'present', 'value': other['media_id']}
    with pytest.raises(CommitRejected, match='provider observation has an ambiguous item path'):
        location({'items': rows}, ['items', 'item_id:' + authored, 'media_id'])


@pytest.mark.parametrize('rows, token', [
    ([{'item_id': 'a'}], '0'),
    ([{'item_id': 'a'}], 'item_id:missing'),
    ([{'item_id': 'a'}, {'item_id': 'a'}], 'item_id:a'),
])
def test_runtime_strict_item_path_rejects_numeric_missing_and_duplicate(rows, token, monkeypatch):
    monkeypatch.setitem(sys.modules, 'runtime_protocol', runtime_protocol)
    with pytest.raises(CommitRejected, match='provider observation has an ambiguous item path'):
        location({'items': rows}, ['items', token, 'media_id'])


def item_state():
    document, _, _, _ = inputs()
    shot = document['shot_revisions'][0]
    other = copy.deepcopy(shot['payload']['items'][0])
    other['item_id'] = 'other:item'
    shot['payload']['items'].append(other)
    shot['content_digest'] = _digest(shot['payload'])
    document['dependency_manifest'] = _manifest(document['shot_revisions'],
        document['internal_timeline_revisions'], document['dependency_manifest']['media'], [])
    return State(bundle_from_document(document))


@pytest.mark.parametrize('reverse', [False, True])
def test_state_item_path_storage_and_aggregate_projection(reverse):
    state = item_state()
    ref = OWNER + '/shot'
    shot = state.occurrence(OWNER)['shot_id']
    stored = state.bundle['shots'][shot]['payload']['items']
    original_ids = [row['item_id'] for row in stored]
    published = state.get(ref, ['payload', 'items'])['value']
    if reverse:
        state.set(ref, ['payload', 'items'], present(list(reversed(published))))
    path = ['payload', 'items', 'item_id:other:item', 'media_id']
    state.set(ref, path, present('changed'))
    assert state.get(ref, path) == present('changed')
    assert state.get(ref, ['payload', 'items', 'item_id:item-1', 'media_id']) == present(published[0]['media_id'])
    assert [row['item_id'] for row in stored] == original_ids
    actual = state.bundle['shots'][shot]['payload']['items']
    assert [row['item_id'] for row in actual] == (list(reversed(original_ids)) if reverse else original_ids)
    assert next(row for row in actual if row['item_id'] == original_ids[1])['media_id'] == 'changed'
    with pytest.raises(CommandError):
        state.get(ref, ['payload', 'items', 'item_id:' + original_ids[1], 'media_id'])
    before = copy.deepcopy(state.bundle)
    with pytest.raises(CommandError):
        state.set(ref, [*path[:-1], 'missing', 'child'], present('no container'))
    assert state.bundle == before
    with pytest.raises(CommandError):
        state.set(ref, [*path[:-1], 'item_id'], present('another'))
    assert state.bundle == before


@pytest.mark.parametrize('damage', ['missing-map', 'empty-map', 'nonbijective', 'extra-map',
    'missing-item', 'duplicate-item', 'foreign-map', 'wrong-owner', 'revision', 'digest', 'internal-revision'])
@pytest.mark.parametrize('access', ['leaf', 'aggregate', 'set'])
def test_item_mapping_refuses_unverified_correspondence(damage, access):
    state = item_state()
    ref = OWNER + '/shot'
    shot = state.occurrence(OWNER)['shot_id']
    source = state.bundle['source_mapping']['shots'][shot]
    mapping = source['item_id_map']
    rows = state.bundle['shots'][shot]['payload']['items']
    if damage == 'missing-map':
        source.pop('item_id_map')
    elif damage == 'empty-map':
        source['item_id_map'] = {}
    elif damage == 'nonbijective':
        mapping['other:item'] = mapping['item-1']
    elif damage == 'extra-map':
        mapping['foreign'] = 'unbound'
    elif damage == 'missing-item':
        rows.pop()
    elif damage == 'duplicate-item':
        rows[1]['item_id'] = rows[0]['item_id']
    elif damage == 'wrong-owner':
        state.occurrence(OWNER)['shot_id'] = state.bundle['placements'][1]['shot_id']
    elif damage == 'foreign-map':
        source['item_id_map'] = copy.deepcopy(state.bundle['source_mapping']['shots'][
            state.bundle['placements'][1]['shot_id']]['item_id_map'])
    else:
        source[{'revision': 'revision_id', 'digest': 'content_digest',
                'internal-revision': 'internal_timeline_revision_id'}[damage]] = 'unverified'
    before = copy.deepcopy(state.bundle)
    path = ['payload', 'items', 'item_id:item-1', 'media_id']
    with pytest.raises(CommandError):
        if access == 'set':
            state.set(ref, path, present('changed'))
        else:
            state.get(ref, ['payload', 'items'] if access == 'aggregate' else path)
    assert state.bundle == before


@pytest.mark.parametrize('accepted_boundary', [False, True])
@pytest.mark.parametrize('aggregate_first', [False, True])
@pytest.mark.parametrize('aggregate_path', [[], ['payload'], ['payload', 'items']])
def test_inverse_folds_item_leaf_with_local_and_published_aggregates(accepted_boundary, aggregate_first, aggregate_path):
    from astrid.sdk.timeline._recording import Recording
    from astrid.sdk.timeline.inverse import coalesce

    state = item_state()
    shot = state.occurrence(OWNER)['shot_id']
    ref = 'shot:' + shot if not aggregate_path else OWNER + '/shot'
    before = state.get(ref, aggregate_path)
    original = copy.deepcopy(state.bundle)
    recording = Recording(state.bundle, {'op': 'clip.set_params'}, 0)
    path = ['payload', 'items', 'item_id:other:item', 'media_id']
    if aggregate_first:
        recording.assign(ref, aggregate_path, before)
    recording.write(OWNER + '/shot', path, 'changed')
    if not aggregate_first:
        recording.assign(ref, aggregate_path, recording.state.get(ref, aggregate_path))
    if accepted_boundary:
        from astrid.sdk.timeline._collections import AcceptedRecords

        entry = {'records': {'commands': [recording.record]}}
        records = AcceptedRecords([entry], [recording.record], lambda entry: (original, recording.state.bundle))
        folded, = coalesce(records)
    else:
        folded, = coalesce([recording.record], recording.state)
    assert folded['before'] == before
    assert folded['after'] == recording.state.get(ref, aggregate_path)
    assert folded['ref'] == ref and folded['path'] == aggregate_path


@pytest.mark.parametrize('site', ['leaf', 'aggregate'])
def test_item_inverse_preserves_intervening_equal_value_write_guard(source_control, site):
    from tests.editing_conformance.test_occurrence_media_manifest_inverse import accepted_records
    from tests.editing_conformance.test_recipe_m1_commands import inverse, later

    realm, _, created = source_control
    records = accepted_records(realm, realm.entries[-1])
    bundle = bundle_from_document(created['data']['canonical_document'])
    state = State(bundle)
    ref = OWNER + '/shot'
    path = ['payload', 'items']
    if site == 'leaf':
        path += ['item_id:item-1', 'media_id']
    value = state.get(ref, path)['value']
    before = copy.deepcopy(bundle)
    # Even a value-equal tail is an intervening write; final bytes grant no undo authority.
    with pytest.raises(CommandError, match='intervening'):
        inverse(bundle, records, [later(ref, path, value)])
    assert bundle == before


@pytest.mark.parametrize('reverse_order', [False, True])
def test_native_item_inverse_preserves_sequential_observations(reverse_order):
    from astrid.sdk.timeline._recording import Recording
    from astrid.sdk.timeline.native_occurrence_media_commands import _replace_payload_media
    from tests.editing_conformance.test_recipe_m1_commands import inverse

    state = item_state()
    original = copy.deepcopy(state.bundle)
    old = state.get(OWNER + '/shot', ['payload', 'items', 'item_id:item-1', 'media_id'])['value']
    recording = Recording(state.bundle, {'op': 'clip.set_params'}, 0)
    _replace_payload_media(recording, OWNER, old, 'changed')
    _replace_payload_media(recording, OWNER, 'changed', old)
    assert recording.state.bundle == original
    writes = recording.record['writes']
    assert len(writes) == 4
    assert writes[0]['after'] == writes[2]['before'] == present('changed')
    assert writes[0]['before'] == writes[2]['after'] == present(old)
    if reverse_order:
        shot = state.occurrence(OWNER)['shot_id']
        recording.state.bundle['shots'][shot]['payload']['items'].reverse()
        with pytest.raises(CommandError):
            inverse(recording.state.bundle, [recording.record])
    else:
        result = inverse(recording.state.bundle, [recording.record])
        assert result.bundle == original
        assert len(result.records[0]['writes']) == 4


def test_item_inverse_rejects_equal_bytes_on_unproven_revision(source_control):
    from tests.editing_conformance.test_occurrence_media_manifest_inverse import accepted_records
    from tests.editing_conformance.test_recipe_m1_commands import inverse

    realm, _, created = source_control
    records = accepted_records(realm, realm.entries[-1])
    document = copy.deepcopy(created['data']['canonical_document'])
    shot, = document['shot_revisions']
    shot['revision_id'] += ':unproven'
    parent = document['parent_revision']
    parent['payload']['occurrences'][0]['shot_revision_id'] = shot['revision_id']
    parent['revision_id'] += ':unproven'
    parent['content_digest'] = _digest(parent['payload'])
    document['dependency_manifest'] = _manifest(document['shot_revisions'],
        document['internal_timeline_revisions'], document['dependency_manifest']['media'], [])
    bundle = bundle_from_document(document)
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match='binding changed'):
        inverse(bundle, records)
    assert bundle == before
