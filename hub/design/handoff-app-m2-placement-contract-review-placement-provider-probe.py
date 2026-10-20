"""Read-only diagnostics against archived a6c2db3d; detached port, NOT Runtime admission."""
import copy
import json

import pytest

from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.native_placement_commands import (
    capture_placement_create,
    capture_placement_unplace,
)
from tests.editing_conformance.test_recipe_m2_placement_create_unplace import create_case, OWNER
from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm
from tests.sdk.test_timeline_commit_provider import CommitRejected, inverse, runtime_abi


def unchanged_on_refusal(realm, calls, reason):
    before = copy.deepcopy((realm.head, realm.entries, realm.documents, realm.accepted, realm.prepared))
    try:
        realm.call(calls)
    except CommitRejected as exc:
        assert exc.failure['details']['reason'] == reason, exc.failure
        assert (realm.head, realm.entries, realm.documents, realm.accepted, realm.prepared) == before
        return exc.failure
    raise AssertionError('expected diagnostic refusal: ' + reason)


with pytest.MonkeyPatch.context() as patch:
    runtime_abi.__wrapped__(patch)  # candidate's existing two-exception/metadata ABI fixture
    document, _, command, verified = create_case()
    realm = MediaRealm(document, verified)
    created = realm.call([command])
    after_create = created['data']['canonical_document']
    bundle = bundle_from_document(after_create)
    remove = capture_placement_unplace(bundle, OWNER, 'placed', ownership='occurrence')
    removed_plan = execute(bundle, [remove], verified_media=verified)
    args = command['args']
    recreate = capture_placement_create(removed_plan.bundle, OWNER, args['id'], args['media'],
        args['on'], args['hold'], ownership='occurrence', verified_media=verified)
    execute(bundle, [remove, recreate], verified_media=verified)
    same_batch = unchanged_on_refusal(realm, [remove, recreate], 'identity_collision')
    removed = realm.call([remove])
    separate = unchanged_on_refusal(realm, [recreate], 'identity_collision')
    undo_removed = realm.call([inverse([removed['receipt']['receipt_id']])])
    assert undo_removed['data']['canonical_document'] == after_create
    lifo = unchanged_on_refusal(realm, [inverse([created['receipt']['receipt_id']])], 'intervening_write')
    print(json.dumps({
        'candidate': 'a6c2db3d14c14da3be61c7e28b615c0e4202e619',
        'scope': 'real Agent RuntimeCommitService, detached MediaRealm/ABI, no real Runtime',
        'pure_batch_execution': 'succeeds',
        'same_batch_provider': same_batch,
        'separate_recreate_provider': separate,
        'undo_remove': 'accepted, exact post-create document restored',
        'undo_create_after_undo_remove': lifo,
        'all_refusals': 'head/history/documents/accepted/prepared unchanged',
    }, indent=2))
