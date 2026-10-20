"""Popup foundation probe; test-only handlers are not a published media contract."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline import commands
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from tests.editing_conformance.test_recipe_m1_commands import inverse
from tests.sdk.test_timeline_commit_provider_document import document_fixture

OWNER = 'occurrence:occ-a'
NEW = 'sha256:' + '2' * 64


def popup_document():
    document = document_fixture()
    internal = document['internal_timeline_revisions'][0]
    internal['payload'].pop('source_window')
    internal['payload']['registry'] = copy.deepcopy(internal['payload']['registry'])
    internal['payload']['registry']['assets']['picture'].update(
        generationId='generation-old', variantId='variant-old', opaque=[None, False])
    internal['content_digest'] = _digest(internal['payload'])
    parent = document['parent_revision']
    parent['payload']['occurrences'][0]['placement']['start_ms'] = 8000
    parent['content_digest'] = _digest(parent['payload'])
    document['dependency_manifest'] = _manifest(
        document['shot_revisions'], document['internal_timeline_revisions'],
        document['dependency_manifest']['media'], [])
    return document


@pytest.fixture(params=['add', 'swap'])
def popup_edit(request, monkeypatch):
    """Use actual recorder writes to isolate compilation from media admission.

    The detached IDs are unit-fixture values. This deliberately makes no claim
    about Runtime selection, provider acceptance or an installed popup opcode.
    """
    operation = request.param

    def handler(ctx, command):
        ctx.read(OWNER + '/source')
        ctx.write(OWNER + '/source', ['registry', 'assets', 'new'],
                  {'media_id': NEW, 'type': 'image', 'generationId': 'generation-new',
                   'variantId': 'variant-new', 'opaque': [None, False, {}]})
        if operation == 'add':
            ctx.create(OWNER, 'clip', {
                'id': 'reserved-child', 'track': 'picture', 'asset': 'new',
                'clipType': 'image', 'at': .125, 'hold': 1.25, 'params': None})
        else:
            ctx.read(OWNER + '/clip:clip-a')
            ctx.write(OWNER + '/clip:clip-a', ['asset'], 'new')

    installed = commands.operations()
    installed['test.popup-media'] = commands.Operation(
        {'type': 'object', 'additionalProperties': False}, handler,
        {'ownership': 'occurrence'})
    monkeypatch.setattr(commands, 'operations', lambda: installed)
    document = popup_document()
    original = bundle_from_document(document)
    call = {'schema_version': 1, 'op': 'test.popup-media', 'version': '1',
            'select': OWNER, 'args': {}}
    plan = commands.execute(original, [call])
    return document, original, plan


def test_recorded_registry_creation_and_child_inverse_preserve_authored_state(popup_edit):
    document, original, plan = popup_edit
    assert commands.execute(original, plan.commands).records == plan.records
    assert original == bundle_from_document(document)
    assert plan.bundle['parent'] == original['parent']
    sibling = original['placements'][1]['shot_id']
    assert plan.bundle['shots'][sibling] == original['shots'][sibling]
    assert inverse(plan.bundle, plan.records).bundle == original
    assert document_from_bundle(inverse(plan.bundle, plan.records).bundle) == document
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))
    undone = inverse(reloaded, plan.records)
    restored = document_from_bundle(undone.bundle, source_bundles=(original,))
    assert State(undone.bundle).config(OWNER)['registry'] == State(original).config(OWNER)['registry']
    assert restored['parent_revision']['payload'] == document['parent_revision']['payload']
    assert restored['shot_revisions'] == document['shot_revisions']
    assert restored['internal_timeline_revisions'] == document['internal_timeline_revisions']


@pytest.mark.xfail(
    strict=True,
    reason='PLAN 4.1 / popup bundle2 requires media-manifest provenance for exact inverse',
)
def test_compiled_popup_inverse_restores_exact_original_document(popup_edit):
    # Restore this expectation through the shared recipe; do not preseed NEW in
    # the baseline, drop the manifest comparison or accept a different revision.
    document, original, plan = popup_edit
    reloaded = bundle_from_document(document_from_bundle(plan.bundle))
    undone = inverse(reloaded, plan.records)
    assert document_from_bundle(undone.bundle, source_bundles=(original,)) == document


def test_unselected_retained_media_pins_cannot_be_globally_pruned():
    document = popup_document()
    # Retained media can belong to immutable sources rather than selected clips.
    # The current converter explicitly preserves such pins; fixing popup undo by
    # pruning all unselected media would silently lose this existing behavior.
    document['dependency_manifest']['media'].append({'media_id': NEW, 'content_digest': NEW})
    assert document_from_bundle(bundle_from_document(document)) == document
