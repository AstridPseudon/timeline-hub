"""Nested structural slices restore their own authenticated collection order."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._collections import AcceptedRecords, arrange
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._step_undo import inverse_stages, validate_nested_history
from astrid.sdk.timeline.capture import capture_clip_delete
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.inverse import _stage_restoration_orders
from astrid.sdk.timeline.native_parent_media_commands import capture_clip_replace_media
from tests.editing_conformance.test_recipe_m2_parent_media import args, clip_ids, ordered_parent
from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm
from tests.sdk.test_timeline_commit_provider import inverse
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


@pytest.fixture
def chain():
    bundle, media, verified = ordered_parent('image')
    document = document_from_bundle(bundle)
    bundle = bundle_from_document(document)
    realm = MediaRealm(document, verified)
    calls = capture_clip_replace_media(bundle, 'parent/clip:A',
        args(media, 'image', at=0)['row'], media, verified_media=verified)
    first = realm.call(calls)
    landed = bundle_from_document(first['data']['canonical_document'])
    second = realm.call([capture_clip_delete(landed, 'parent/clip:C')])
    undone = realm.call([inverse([first['receipt']['receipt_id'], second['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == document
    return realm, document, second['data']['canonical_document'], undone


@pytest.mark.parametrize('selected', [False, True], ids=['whole', 'selected'])
def test_structural_partial_stages_restore_each_order_across_repeated_inverses(chain, selected):
    realm, document, landed, undone = chain
    entry = realm.entries[-1]
    original = copy.deepcopy(entry)
    records = AcceptedRecords([entry], entry['records']['commands'], None)
    groups = list(inverse_stages(records))
    assert len(groups) == 2
    orders = [_stage_restoration_orders(records, commands[0])['parent', 'clip']
              for _, _, commands in groups]
    assert orders == [(['parent/clip:born', 'parent/clip:target', 'parent/clip:C'],
                       ['parent/clip:A', 'parent/clip:target', 'parent/clip:C']),
                      (['parent/clip:born', 'parent/clip:target'],
                       ['parent/clip:born', 'parent/clip:target', 'parent/clip:C'])]
    assert all(commands[0]['ordinal'] == 0 and publication == entry['publication_id']
               for publication, _, commands in groups)
    command = inverse([undone['receipt']['receipt_id']])
    if selected:
        command['args']['steps'] = {entry['publication_id']: [entry['records']['steps'][0]['id']]}
    result = realm.call([command])
    assert result['data']['canonical_document'] == landed
    assert clip_ids(bundle_from_document(landed)) == ['born', 'target']
    assert entry == original
    for expected in (document, landed, document):
        result = realm.call([inverse([result['receipt']['receipt_id']])])
        assert result['data']['canonical_document'] == expected
    assert entry == original


@pytest.mark.parametrize('damage', [
    'source', 'step', 'boundary', 'native', 'effect', 'mirror', 'ordinal', 'command', 'owner',
])
def test_stage_order_requires_exact_accepted_source_partition(chain, damage):
    realm, _, _, _ = chain
    entry = realm.entries[-1]
    records = AcceptedRecords([entry], entry['records']['commands'], None)
    record = list(inverse_stages(records))[0][2][0]
    source, step, boundary = record['_inverse_stage']
    record = {**record}
    if damage == 'source':
        record['_inverse_stage'] = (copy.deepcopy(source), step, boundary)
    elif damage == 'step':
        record['_inverse_stage'] = (source, copy.deepcopy(step), boundary)
    elif damage == 'boundary':
        record['_inverse_stage'] = (source, step, copy.deepcopy(boundary))
    elif damage == 'native':
        record['writes'] = record['writes'][1:]
    elif damage == 'effect':
        record['_inverse_effects'] = []
    elif damage == 'ordinal':
        record['ordinal'] = 1
    elif damage == 'command':
        record['command'] = {**record['command'], 'select': 'foreign'}
    elif damage == 'owner':
        record['selections'] = []
    else:
        record['derived_writes'] = []
    original = copy.deepcopy(realm.entries)
    with pytest.raises(CommandError) as error:
        _stage_restoration_orders(records, record)
    assert error.value.kind == 'history_unavailable'
    assert realm.entries == original


@pytest.mark.parametrize('damage', ['missing', 'foreign', 'duplicate'])
def test_stage_order_never_recreates_members_from_mirror_images(chain, damage):
    realm, document, _, _ = chain
    entry = realm.entries[-1]
    records = AcceptedRecords([entry], entry['records']['commands'], None)
    stage = list(inverse_stages(records))[0][2][0]
    expected, _ = _stage_restoration_orders(records, stage)['parent', 'clip']
    bundle = bundle_from_document(document)
    rows = bundle['parent']['clips']
    rows[0]['id'] = 'born'
    if damage == 'missing':
        rows.pop()
    elif damage == 'foreign':
        rows[1]['id'] = 'foreign'
    else:
        rows.append(copy.deepcopy(rows[0]))
    bundle['parent']['config']['clips'] = copy.deepcopy(rows)
    original = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        arrange(State(bundle), 'parent', 'clip', expected)
    assert bundle == original


def test_partial_stage_mirror_chain_rejects_a_broken_previous_image(chain):
    realm, _, _, _ = chain
    history = copy.deepcopy(realm.entries)
    entry = history[-1]
    record = entry['records']['commands'][0]
    record['derived_writes'][1]['before']['value'].reverse()
    original = copy.deepcopy(history)
    with pytest.raises(CommandError) as error:
        validate_nested_history(entry, {item['publication_id']: item for item in history}.__getitem__)
    assert error.value.kind == 'history_unavailable'
    assert history == original
