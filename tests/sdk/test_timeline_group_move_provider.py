"""Detached provider acceptance proves capture/guard integration, not Runtime storage."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.group_view import project_group_view
from astrid.sdk.timeline.new_group_commands import capture_migrate_groups
from tests.editing_conformance.test_recipe_m2_group_move import GROUPS, capture, migrated
from tests.sdk.test_timeline_commit_provider import CommitRejected, inverse
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi
from tests.sdk.test_timeline_group_migration_provider import migration_realm

pytestmark = pytest.mark.usefixtures('runtime_abi')


def canonical_realm():
    original, _, _ = migrated()
    document = original['source_mapping']['_runtime_document']
    realm = migration_realm(document)
    accepted = realm.call([capture_migrate_groups(document, GROUPS)])
    return realm, accepted


def test_provider_migration_move_reload_exact_inverse_redo_and_unrelated_edit():
    realm, migration = canonical_realm()
    canonical = migration['data']['canonical_document']
    bundle = bundle_from_document(canonical)
    commands = capture(bundle)
    moved = realm.call(commands)
    assert moved['data']['commands'] == commands
    accepted = moved['data']['canonical_document']
    view = project_group_view(bundle_from_document(accepted))
    assert [(c['track'], c['at'], c['hold']) for c in view['clips'][-2:]] == [('V2', 1, 2), ('V2', 3, 2)]
    basis = copy.deepcopy(realm.head)
    independent = capture_clip_set_params(bundle_from_document(accepted), 'parent/clip:before', values={'opaque': None})
    realm.call([independent])
    undone = realm.call([inverse([moved['receipt']['receipt_id']])], base=basis)
    assert undone['data']['status'] == 'rebased'
    reverted = bundle_from_document(undone['data']['canonical_document'])
    assert project_group_view(reverted)['clips'][-2:] == project_group_view(bundle)['clips'][-2:]
    assert reverted['parent']['clips'][0]['params'] == {'opaque': None}
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert project_group_view(bundle_from_document(redone['data']['canonical_document']))['clips'][-2:] == view['clips'][-2:]


def test_provider_typed_child_lane_birth_same_batch_inverse_redo():
    realm, migration = canonical_realm()
    bundle = bundle_from_document(migration['data']['canonical_document'])
    commands = capture(bundle, raw='caller-child', new={'id': 'caller-child', 'kind': 'visual'})
    moved = realm.call(commands)
    undone = realm.call([inverse([moved['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == migration['data']['canonical_document']
    redone = realm.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == moved['data']['canonical_document']


def test_provider_captured_move_refuses_source_change_without_any_partial_move():
    realm, migration = canonical_realm()
    bundle = bundle_from_document(migration['data']['canonical_document'])
    commands = capture(bundle)
    basis = copy.deepcopy(realm.head)
    changed = capture_clip_set_params(bundle, 'occurrence:new-occ/clip:c1', values={'other': True})
    realm.call([changed])
    before = copy.deepcopy((realm.documents, realm.entries, realm.accepted, realm.head))
    with pytest.raises(CommitRejected):
        realm.call(commands, base=basis)
    assert (realm.documents, realm.entries, realm.accepted, realm.head) == before
