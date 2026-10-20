"""Named effect subset through the real Agent provider; no Runtime socket claim."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_recipe_clip_scalar_fields import CHILD, PARENT, clip
from tests.editing_conformance.test_recipe_effect_fields import inspector_requests
from tests.sdk.test_timeline_clip_scalar_provider import app_document, current
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    inverse,
    runtime_abi,  # noqa: F401 (shared autouse Runtime ABI fixture)
)


@pytest.mark.parametrize('ref', [PARENT, CHILD])
def test_effect_add_edit_remove_accepted_reload_and_exact_inverse_redo(ref):
    realm = DetachedRealm(app_document())
    initial = copy.deepcopy(realm.documents[realm.head['revision_id']])
    for request in inspector_requests():
        before = copy.deepcopy(realm.documents[realm.head['revision_id']])
        command = capture_clip_set(current(realm), ref, **request)
        accepted = realm.call([command])
        document = accepted['data']['canonical_document']
        reloaded = bundle_from_document(json.loads(json.dumps(document)))
        assert accepted['data']['commands'] == [command]
        assert clip(reloaded, ref) == clip(current(realm), ref)
        sibling = 'occurrence:shared-sibling/clip:f2-agent-clip'
        assert clip(reloaded, sibling) == clip(bundle_from_document(initial), sibling)
        undone = realm.call([inverse([accepted['receipt']['receipt_id']])])
        assert undone['data']['canonical_document'] == before
        redone = realm.call([inverse([undone['receipt']['receipt_id']])])
        assert redone['data']['canonical_document'] == document


def test_effect_disjoint_rebase_keeps_original_capture_and_inverse_preserves_other_author():
    realm = DetachedRealm(app_document())
    base = copy.deepcopy(realm.head)
    command = capture_clip_set(current(realm), CHILD, values={'entrance': {'type': 'fade', 'duration': 0.4}})
    realm.call([capture_track_set(current(realm), 'parent/track:V1', values={'label': 'other author'})])
    intervening = copy.deepcopy(realm.documents[realm.head['revision_id']])
    accepted = realm.call([command], base=base)
    assert accepted['data']['commands'] == [command]
    undone = realm.call([inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == intervening


@pytest.mark.parametrize('aba', [False, True])
def test_effect_unchanged_write_and_aba_guard_undo_by_publication(aba):
    realm = DetachedRealm(app_document())
    request = {'values': {'entrance': {'type': 'fade', 'duration': 0.4}}}
    realm.call([capture_clip_set(current(realm), CHILD, **request)])
    first = realm.call([capture_clip_set(current(realm), CHILD, **request)])
    if aba:
        realm.call([capture_clip_set(current(realm), CHILD, values={'entrance': {'type': 'fade', 'duration': 0.9}})])
    realm.call([capture_clip_set(current(realm), CHILD, **request)])
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected) as error:
        realm.call([inverse([first['receipt']['receipt_id']])])
    assert error.value.failure['details']['reason'] == 'intervening_write'
    assert (realm.head, realm.entries, realm.documents) == before
