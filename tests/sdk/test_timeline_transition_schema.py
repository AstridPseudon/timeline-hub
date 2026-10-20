"""The ordinary provider resolves and retains the exact transition declaration."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline.commit import _digest
from tests.editing_conformance.test_recipe_clip_scalar_fields import PARENT
from tests.editing_conformance.test_recipe_scalar_commands import schema_options
from tests.editing_conformance.test_recipe_transition_set import admitted_transition
from tests.sdk.test_timeline_clip_scalar_provider import app_document, current
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedRealm, inverse
from tests.sdk.test_timeline_selected_schema import (  # noqa: F401
    commit,
    configured_project_pack,
    runtime_abi,
)


def test_provider_selected_transition_validates_new_schema_and_retains_undo_inputs(
        configured_project_pack):  # noqa: F811 - shared admission fixture
    _, selected = admitted_transition(configured_project_pack)
    realm = DetachedRealm(app_document())
    options = schema_options(configured_project_pack, selected)
    verified, realm.snapshot_objects = options['schema_inputs'][0]
    realm.live_sources[_digest(verified['pin'])] = verified
    values = {'elementRef': selected, 'transition': {'type': selected['id'], 'duration': .5,
              'revision': selected['revision'], 'params': {'seed': 8, 'future': [None, False]}}}
    before = copy.deepcopy(realm.documents[realm.head['revision_id']])
    command = capture_clip_set(current(realm), PARENT, values=values, **options)
    accepted = commit(realm, [command])
    assert accepted['data']['commands'] == [command]
    document = accepted['data']['canonical_document']
    assert document['dependency_manifest']['documents'] == [options['schema_source']]
    assert _digest(options['schema_source']) in realm.retained_sources
    assert current(realm)['parent']['clips'][1]['elementRef'] == selected
    # New authored value under the selected schema must refuse atomically;
    # the other retained revision would permit 16, but is not authoritative.
    invalid = copy.deepcopy(values)
    invalid['transition']['params']['seed'] = 16
    request = {'schema_version': 1, 'op': 'clip.set', 'version': '1', 'select': PARENT,
               'args': {'values': invalid, 'clear': [], 'schema_source': options['schema_source']}}
    snapshot = copy.deepcopy((realm.head, realm.entries, realm.documents))
    with pytest.raises(CommitRejected, match='maximum'):
        commit(realm, [request])
    assert snapshot == (realm.head, realm.entries, realm.documents)
    realm.live_sources.clear()
    undone = commit(realm, [inverse([accepted['receipt']['receipt_id']])])
    restored = undone['data']['canonical_document']
    assert restored['parent_revision']['payload'] == before['parent_revision']['payload']
    assert restored['shot_revisions'] == before['shot_revisions']
    assert restored['internal_timeline_revisions'] == before['internal_timeline_revisions']
    redone = commit(realm, [inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == document


@pytest.mark.xfail(strict=True, reason='Exact inverse must remove newly introduced DocumentPins when no later dependent needs them')
def test_first_selected_transition_exact_document_inverse(configured_project_pack):  # noqa: F811
    _, selected = admitted_transition(configured_project_pack)
    realm = DetachedRealm(app_document())
    options = schema_options(configured_project_pack, selected)
    verified, realm.snapshot_objects = options['schema_inputs'][0]
    realm.live_sources[_digest(verified['pin'])] = verified
    before = copy.deepcopy(realm.documents[realm.head['revision_id']])
    values = {'elementRef': selected, 'transition': {'type': selected['id'], 'duration': .5,
              'revision': selected['revision'], 'params': {'seed': 8}}}
    accepted = commit(realm, [capture_clip_set(current(realm), PARENT, values=values, **options)])
    undone = commit(realm, [inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == before
