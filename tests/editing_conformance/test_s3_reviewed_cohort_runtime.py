"""Reviewed native recipes compose from a pristine head without legacy writes."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.media_transcript import build_transcript, transcript_document_id
from astrid.sdk.timeline import commands
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
from tests.editing_conformance import test_commit_runtime_parent_media as parent
from tests.editing_conformance.test_next_command_cohort_runtime import reopen
from tests.editing_conformance.test_pristine_initialize import batch
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


def test_init_occurrence_media_parent_swap_word_grouped_inverse_reload_restart(tmp_path, monkeypatch):
    use_runtime()
    from runtime_protocol.errors import RuntimeErrorBase

    realm = parent.media_realm(tmp_path, monkeypatch, 'video', historical=False, pristine=True)
    case = next(realm)
    accepted, requests = [], []

    def submit(calls, key):
        request = parent.body(case, calls)
        result = parent.commit(case, request, key)
        accepted.append(result)
        requests.append((request, key, result))
        return result

    def bundle():
        return bundle_from_document(parent.current(case))

    try:
        original = parent.current(case)
        submit(batch(bundle()), 's3-init')
        occurrence = capture_occurrence_create(bundle(), 'born-occ', 'born-shot', name='Chapter',
                                              track='V1', on=2, duration=8)
        submit([occurrence], 's3-occurrence')
        submit([capture_track_create(bundle(), 'occurrence:born-occ', {
            'id': 'picture', 'kind': 'visual'})], 's3-child-track')
        source = {'id': 'voice', 'clipType': 'video', 'track': 'picture',
                  'asset': case.pins['new']['asset'], 'at': 0, 'hold': 4,
                  'from': 0, 'to': 4, 'speed': 1, 'opaque': [None, False, 0.0]}
        submit([parent.call('occurrence.add-media', {'row': source, 'media': case.pins['new']},
                            'occurrence:born-occ')], 's3-child-media')
        submit([capture_track_create(bundle(), 'parent', {'id': 'overlay', 'kind': 'visual'})],
               's3-overlay')
        row = parent.row(case, 'parent-media', asset='raw-old-alias', track='overlay')
        submit([parent.birth(case, row, case.pins['old'])], 's3-parent-add')
        submit([parent.call('clip.swap-media', {'old_media': case.pins['old'],
            'media': case.pins['new']}, 'parent/clip:parent-media')], 's3-parent-swap')
        swapped = next(row for row in parent.current(case)['parent_revision']['payload']['clips']
                       if row['id'] == 'parent-media')
        assert swapped == {**row, 'asset': case.pins['new']['asset']}
        submit([parent.call('clip.delete', {}, 'parent/clip:parent-media')], 's3-parent-delete')
        submit([parent.call('clip.add', {'row': {'id': 'caption', 'clipType': 'am-type',
            'track': 'overlay', 'at': 0, 'hold': .5, 'opaque': [None, False, 0.0]}})], 's3-caption')
        content = build_transcript(case.pins['new']['object_id'], 'line', 'again again',
                                   [[0, .25, 'again'], [.5, .75, 'again']])
        identity = transcript_document_id(case.project, content['media_id'], content['source_id'])
        case.service.create_document(case.project, {'document_id': identity,
            'kind': 'media.transcript', 'content': content}, idempotency_key='s3-transcript')
        pin = {'document_id': identity, 'version': 1, 'content_digest': _digest(content)}
        choice = {'source': 'occurrence:born-occ/clip:voice', 'document': pin,
                  'word_ids': [content['segments'][0]['words'][1]['id']]}
        submit([parent.call('clip.anchor', {'field': 'on', 'declaration': 'again', 'choice': choice},
                            'parent/clip:caption')], 's3-anchor')
        final = copy.deepcopy(parent.current(case))
        caption = next(row for row in final['parent_revision']['payload']['clips'] if row['id'] == 'caption')
        assert caption['app']['astrid']['word_anchors']['on'] == choice
        assert caption['at'] == 2.5
        assert final['dependency_manifest']['documents'] == [pin]
        # A source with a surviving stable reference cannot be removed on its own.
        before = parent.rows(case)
        with pytest.raises(RuntimeErrorBase):
            parent.undo(case, accepted[1], 's3-referenced-birth')
        assert parent.rows(case) == before
        inverse_request = parent.body(case, [parent.call('timeline.inverse', {
            'publications': [result['receipt']['receipt_id'] for result in accepted]}, None)])
        undone = parent.commit(case, inverse_request, 's3-group-undo')
        assert undone['data']['canonical_document'] == original
        redone = parent.undo(case, undone, 's3-group-redo')
        assert redone['data']['canonical_document'] == final
        reopen(case)
        assert parent.current(case) == final
        for result in (undone, redone):
            stored = case.service.get_project_parent_composition_revision(
                case.project, 'film', result['data']['accepted_revision_id'])
            assert stored['payload'] == result['data']['canonical_document']['parent_revision']['payload']
        with monkeypatch.context() as retry:
            retry.setattr(commands, 'execute', lambda *a, **kw: pytest.fail('retry executed semantics'))
            for request, key, result in requests:
                assert parent.commit(case, request, key) == result
            assert parent.commit(case, inverse_request, 's3-group-undo') == undone
        assert case.service.store.integrity_report()['ok']
    finally:
        realm.close()
