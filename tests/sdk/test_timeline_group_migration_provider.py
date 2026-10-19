"""Provider-only capture and explicit legacy load admission; no fake Runtime proof."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params, capture_track_set
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.new_group_commands import capture_migrate_groups
from tests.editing_conformance.test_recipe_m2_group_migration import GROUPS, legacy_document
from tests.editing_conformance.test_recorded_graph_roots import (
    create_command,
)
from tests.editing_conformance.test_recorded_graph_roots import (
    root_ops as root_ops,
)
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    inverse,
    source_fixture,
)
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi as runtime_abi,
)

pytestmark = pytest.mark.usefixtures('runtime_abi')


def migration_realm(document=None):
    document = legacy_document() if document is None else document
    realm = DetachedRealm(document)
    transcript = source_fixture('transcript')
    realm.live_sources[_digest(transcript['pin'])] = transcript
    return realm


@pytest.mark.parametrize('opaque_variant', [False, True])
def test_provider_migration_reload_inverse_restores_raw_legacy_and_redo_same_ids(opaque_variant):
    realm = migration_realm(legacy_document(opaque_variant=opaque_variant))
    original = copy.deepcopy(realm.documents[realm.head['revision_id']])
    migrated = realm.call([capture_migrate_groups(original, GROUPS)])
    canonical = copy.deepcopy(migrated['data']['canonical_document'])
    undone = realm.call([inverse([migrated['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == original
    assert json.dumps(undone['data']['canonical_document'], sort_keys=True) == json.dumps(original, sort_keys=True)
    before = copy.deepcopy((realm.documents, realm.entries, realm.accepted, realm.head))
    with pytest.raises(CommitRejected, match='explicit timeline.migrate-groups'):
        realm.call([{'schema_version': 1, 'op': 'track.create', 'version': '1',
                     'select': 'parent', 'args': {'row': {'id': 'ordinary', 'kind': 'visual'}}}])
    assert (realm.documents, realm.entries, realm.accepted, realm.head) == before
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == canonical
    assert redone['data']['commands'][0]['created'] == ['shot:new-shot', 'occurrence:new-occ']


def test_provider_migration_inverse_preserves_disjoint_work_and_retained_pins():
    realm = migration_realm()
    original = realm.documents[realm.head['revision_id']]
    migrated = realm.call([capture_migrate_groups(original, GROUPS)])
    basis = copy.deepcopy(realm.head)
    canonical = copy.deepcopy(migrated['data']['canonical_document'])
    command = capture_clip_set_params(bundle_from_document(canonical), 'parent/clip:before',
                                      values={'custom': None})
    realm.call([command])
    undone = realm.call([inverse([migrated['receipt']['receipt_id']])], base=basis)
    expected = copy.deepcopy(original)
    expected['parent_revision']['payload']['clips'][0]['params'] = {'custom': None}
    expected['parent_revision']['payload']['config']['clips'][0]['params'] = {'custom': None}
    document = undone['data']['canonical_document']
    assert undone['data']['status'] == 'rebased'
    assert document['parent_revision']['payload'] == expected['parent_revision']['payload']
    assert document['dependency_manifest'] == expected['dependency_manifest']
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])['data']['canonical_document']
    canonical['parent_revision']['payload']['clips'][0]['params'] = {'custom': None}
    canonical['parent_revision']['payload']['config']['clips'][0]['params'] = {'custom': None}
    assert redone['parent_revision']['payload'] == canonical['parent_revision']['payload']
    assert redone['dependency_manifest'] == canonical['dependency_manifest']


@pytest.mark.parametrize('damage', ['destination-aba', 'source-aba', 'later-dependent'])
@pytest.mark.usefixtures('root_ops')
def test_provider_migration_inverse_refuses_later_dependency_and_aba(damage):
    realm = migration_realm()
    migrated = realm.call([capture_migrate_groups(legacy_document(), GROUPS)])
    canonical = migrated['data']['canonical_document']
    bundle = bundle_from_document(canonical)
    if damage == 'later-dependent':
        occurrence = copy.deepcopy(bundle['placements'][0])
        occurrence['occurrence_id'] = 'dependent'
        realm.call([create_command([{'ref': 'occurrence:dependent', 'kind': 'occurrence',
                                    'owner': 'parent', 'value': occurrence}])])
    else:
        ref = 'occurrence:new-occ/track:V1' if damage == 'destination-aba' else 'parent/track:V1'
        label = State(bundle).entity(ref)['label']
        realm.call([capture_track_set(bundle, ref, values={'label': 'Later label'})])
        current = bundle_from_document(realm.documents[realm.head['revision_id']])
        realm.call([capture_track_set(current, ref, values={'label': label})])
        assert State(bundle_from_document(realm.documents[realm.head['revision_id']])).entity(ref)['label'] == label
    before = copy.deepcopy((realm.documents, realm.entries, realm.accepted, realm.head))
    with pytest.raises(CommitRejected) as error:
        realm.call([inverse([migrated['receipt']['receipt_id']])])
    assert error.value.failure['details']['reason'] == 'intervening_write'
    assert (realm.documents, realm.entries, realm.accepted, realm.head) == before


@pytest.mark.parametrize('damage', ['beforeimage', 'missing-boundary'])
def test_provider_migration_inverse_cannot_take_caller_images_or_missing_history(damage):
    realm = migration_realm()
    migrated = realm.call([capture_migrate_groups(legacy_document(), GROUPS)])
    command = inverse([migrated['receipt']['receipt_id']])
    if damage == 'beforeimage':
        command['writes'] = [{'ref': 'parent', 'path': [], 'before': {'forged': True}}]
    else:
        del realm.documents['legacy-parent']
    before = copy.deepcopy((realm.documents, realm.entries, realm.accepted, realm.head))
    with pytest.raises(CommitRejected) as error:
        realm.call([command])
    expected = 'invalid_edit_command' if damage == 'beforeimage' else 'history_unavailable'
    assert error.value.failure['details']['reason'] == expected
    assert (realm.documents, realm.entries, realm.accepted, realm.head) == before


def test_provider_migration_preview_reads_exact_retained_transcript_and_media():
    document = legacy_document()
    transcript = source_fixture('transcript')
    document['dependency_manifest']['documents'] = [transcript['pin']]
    realm = DetachedRealm(document)
    realm.live_sources[_digest(transcript['pin'])] = transcript
    command = capture_migrate_groups(document, GROUPS)
    result = realm.call([command], dry_run=True)
    assert result['receipt'] is None
    assert realm.accepted == [] and realm.prepared == []
    assert ('transcript', transcript['pin']) in realm.reads
    canonical = result['data']['canonical_document']
    assert canonical['dependency_manifest']['documents'] == [transcript['pin']]
    assert canonical['dependency_manifest']['media'] == document['dependency_manifest']['media']
    assert canonical['parent_revision']['payload']['occurrences'][0]['duration_ms'] == 4000
    assert realm.documents[realm.head['revision_id']] == document


def test_provider_ordinary_edit_on_legacy_is_refused_before_preview():
    document = legacy_document()
    realm = DetachedRealm(document)
    before = copy.deepcopy(realm.documents)
    with pytest.raises(CommitRejected, match='explicit timeline.migrate-groups'):
        realm.call([{'schema_version': 1, 'op': 'track.create', 'version': '1',
                     'select': 'parent', 'args': {'row': {'id': 'x', 'kind': 'visual'}}}], dry_run=True)
    assert realm.documents == before and realm.prepared == []
