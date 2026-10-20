"""RT02 carrier probes, not replacements for the two Runtime promotion positives.

These use the existing pure closure fixture and recorder only. A project-shot
promotion cannot be registered until its global head authority is represented.
"""
from __future__ import annotations

import copy

import pytest

from astrid.core.timeline.authoring_bundle import AuthoringBundleError, open_authoring_bundle
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline.commit import bundle_from_document
from tests.editing_conformance.test_recipe_m1_commands import inverse, later
from tests.sdk.test_timeline_commit_provider_document import document_fixture
from tests.timeline.test_authoring_bundle import NEW, _closure, _digest


def source_bundle(*, shared=False):
    parent, shots, internals = _closure(shared=shared)
    items = shots[0]['payload']['items']
    items[0]['metadata']['status'] = 'primary'
    items.append({'item_id': 'candidate', 'media_id': NEW, 'metadata': {
        'role': 'primary_visual', 'status': 'candidate',
        'provenance': {'project_id': parent['project_id'], 'shot_id': shots[0]['shot_id']}}})
    shots[0]['content_digest'] = _digest(shots[0]['payload'])
    return open_authoring_bundle(parent, shot_revisions=shots,
                                 internal_timeline_revisions=internals)


def test_shared_shot_carrier_is_occurrence_owned_and_remaps_item_identity():
    bundle = source_bundle(shared=True)
    assert 'shot-shared' not in bundle['shots']
    for placement in bundle['placements']:
        identity = placement['shot_id']
        source = bundle['source_mapping']['shots'][identity]
        assert source['shot_id'] == 'shot-shared'
        assert source['item_id_map']['candidate'] != 'candidate'
        items = bundle['shots'][identity]['payload']['items']
        assert source['item_id_map']['candidate'] in {item['item_id'] for item in items}
        # Provenance continues to name the project shot; rewriting it to the
        # materialized copy would change the producer's assertion.
        assert items[-1]['metadata']['provenance']['shot_id'] == 'shot-shared'
    with pytest.raises(CommandError, match='missing shot root'):
        State(bundle).entity('shot:shot-shared')


def test_existing_aggregate_recorder_restores_exact_status_writes_and_guards_aba():
    original = source_bundle()
    candidate = copy.deepcopy(original)
    ref = 'shot:shot-shared'
    # This is an isolated recorder experiment, not an accepted promotion
    # command: no provenance/media authority or project-head CAS is claimed.
    ctx = Recording(candidate, {'schema_version': 1, 'op': 'shot.promote-candidate',
                               'version': '1', 'select': ref, 'args': {}}, 0)
    authored = ctx.read(ref)
    items = {item['item_id']: item for item in authored['payload']['items']}
    items['item-1']['metadata']['status'] = 'superseded'
    items['candidate']['metadata']['status'] = 'primary'
    ctx.write(ref, [], authored)
    record = ctx.finish(capture=True)
    assert len(record['writes']) == 1
    assert record['reads'][0]['state']['value'] == State(original).entity(ref)
    assert record['writes'][0]['after']['value'] == State(candidate).entity(ref)
    undone = inverse(candidate, [record])
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == candidate
    # Publication-level same-value writes remain authoritative (F1).
    with pytest.raises(CommandError, match='intervening'):
        inverse(candidate, [record], [later(ref, [], authored)])
    assert original == source_bundle()


def test_canonical_document_cannot_carry_an_unplaced_project_shot():
    document = document_fixture(shared=False)
    before = copy.deepcopy(document)
    payload = document['parent_revision']['payload']
    payload['occurrences'] = []
    document['parent_revision']['content_digest'] = _digest(payload)
    with pytest.raises(AuthoringBundleError, match='orphans'):
        bundle_from_document(document)
    assert document['shot_revisions'] == before['shot_revisions']
    assert document['internal_timeline_revisions'] == before['internal_timeline_revisions']
