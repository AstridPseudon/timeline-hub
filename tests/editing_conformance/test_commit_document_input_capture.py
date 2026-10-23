"""Hydrated sources enter sequential closure manifests at consumption."""
from __future__ import annotations

import copy

import pytest

from astrid.core.timeline.authoring_bundle import AuthoringBundleError
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _hydrate, document_from_bundle
from astrid.sdk.timeline.native_word_anchor import capture_anchor
from tests.editing_conformance.test_native_word_anchor_vectors import fixture


def inputs():
    bundle, pin, content = fixture()
    verified = bundle['source_mapping'].pop('pinned_documents')[0]
    choice = {'source': 'occurrence:occ-a/clip:voice', 'document': pin,
              'word_ids': [content['segments'][0]['words'][0]['id']]}
    captured = copy.deepcopy(bundle)
    captured['source_mapping']['pinned_documents'] = [verified]
    track = capture_track_create(captured, 'parent', {'id': 'extra', 'kind': 'audio'})
    staged = execute(captured, [track]).bundle
    anchor = capture_anchor(staged, 'parent/clip:clip-a', 'on', 'again', choice)
    return bundle, verified, [track, anchor]


class Sources:
    def __init__(self, verified):
        self.verified = verified

    def transcript_source(self, pin):
        return copy.deepcopy(self.verified)


@pytest.mark.parametrize('separate_steps', [False, True])
def test_verified_transcript_is_added_only_at_its_consuming_command(separate_steps):
    bundle, verified, calls = inputs()
    immutable = copy.deepcopy(bundle['source_mapping']['_runtime_document'])
    _hydrate(Sources(verified), bundle, calls)
    assert document_from_bundle(bundle) == immutable
    request = {'reads': [], 'label': 'Causal transcript'}
    if separate_steps:
        request['steps'] = [{'id': str(i), 'label': 'Step', 'intent': '', 'tags': [],
                             'command_ordinals': [i], 'patch': []} for i in range(2)]
    plan = execute(bundle, calls, commit_request=request)
    first, consuming = plan._sequential_execution
    assert first['input'] == immutable
    assert first['output'] == consuming['input']
    assert first['output']['dependency_manifest']['documents'] == []
    assert consuming['output']['dependency_manifest']['documents'] == [verified['pin']]
    assert document_from_bundle(plan.bundle) == consuming['output']
    assert any(dep['key'] == 'anchor.transcript' and dep['pin'] == verified['pin']
               for dep in plan.records[1]['dependencies'])
    assert all(dep['kind'] != 'transcript' for dep in plan.records[0]['dependencies'])
    assert bundle['source_mapping']['_runtime_document'] == immutable


@pytest.mark.parametrize('damage', ['digest', 'project', 'version'])
def test_hydration_still_rejects_forged_or_foreign_transcript_before_staging(damage):
    bundle, verified, calls = inputs()
    original = copy.deepcopy(bundle)
    if damage == 'digest':
        verified['document']['content']['segments'][0]['text'] = 'forged'
    elif damage == 'project':
        verified['document']['project_id'] = 'foreign'
    else:
        verified['document']['version'] += 1
    with pytest.raises(AuthoringBundleError, match='exact scoped pin'):
        _hydrate(Sources(verified), bundle, calls)
    assert bundle == original


@pytest.mark.parametrize('source', ['requested', 'retained', 'unconsumed'])
def test_hydration_replaces_caller_manifest_with_authenticated_closure(source):
    bundle, verified, calls = inputs()
    document = bundle['source_mapping']['_runtime_document']
    if source == 'retained':
        document['dependency_manifest']['documents'] = [copy.deepcopy(verified['pin'])]
    elif source == 'unconsumed':
        calls = calls[:1]
    immutable = copy.deepcopy(document)
    forged = {'document_id': 'transcript:foreign-project:media:source',
              'version': 99, 'content_digest': 'sha256:' + 'f' * 64}
    bundle['source_mapping']['_copy_manifest'] = {
        **copy.deepcopy(document['dependency_manifest']), 'documents': [forged],
        'media': [{'media_id': 'sha256:' + 'f' * 64,
                   'content_digest': 'sha256:' + 'f' * 64}]}
    _hydrate(Sources(verified), bundle, calls)
    assert document_from_bundle(bundle) == immutable
    plan = execute(bundle, calls, commit_request={'reads': [], 'label': 'Manifest boundary'})
    result = document_from_bundle(plan.bundle)
    expected = [] if source == 'unconsumed' else [verified['pin']]
    assert result['dependency_manifest']['documents'] == expected
    assert result['dependency_manifest']['media'] == immutable['dependency_manifest']['media']
    assert bundle['source_mapping']['_runtime_document'] == immutable


@pytest.mark.parametrize('damage', ['digest', 'project', 'version'])
def test_forged_manifest_cannot_bypass_source_validation_or_mutate_input(damage):
    bundle, verified, calls = inputs()
    bundle['source_mapping']['_copy_manifest'] = {
        **copy.deepcopy(bundle['source_mapping']['_runtime_document']['dependency_manifest']),
        'documents': [copy.deepcopy(verified['pin'])]}
    original = copy.deepcopy(bundle)
    if damage == 'digest':
        verified['document']['content']['segments'][0]['text'] = 'forged'
    elif damage == 'project':
        verified['document']['project_id'] = 'foreign'
    else:
        verified['document']['version'] += 1
    with pytest.raises(AuthoringBundleError, match='exact scoped pin'):
        _hydrate(Sources(verified), bundle, calls)
    assert bundle == original
