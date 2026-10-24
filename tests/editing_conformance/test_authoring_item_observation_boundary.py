"""Offline source controls for authenticated same-alias inverse observations."""
from __future__ import annotations

import copy
import json
import sys

import pytest
import runtime_protocol
from runtime_protocol.timeline_commit_auth import location, validate_sequential_capture

from astrid.sdk.timeline.commit import _digest, bundle_from_document, create_runtime_commit_service
from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_swap_media
from tests.editing_conformance.test_doc_patch_v2 import submit
from tests.editing_conformance.test_provider_step_undo_v2 import undo
from tests.editing_conformance.test_recipe_occurrence_media import OWNER, TARGET, MediaRealm, inputs
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedPort
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


@pytest.fixture
def source_control():
    baseline, old, new, verified = inputs()
    parent = baseline['parent_revision']
    parent['payload']['occurrences'] = parent['payload']['occurrences'][:1]
    parent['content_digest'] = _digest(parent['payload'])
    new['asset'] = old['asset']
    verified[1]['selection']['asset'] = old['asset']
    realm = MediaRealm(baseline, verified)
    command = capture_occurrence_swap_media(bundle_from_document(baseline), TARGET, old, new,
                                            verified_media=verified)
    context = realm.context([command])
    context['request']['reads'] = []
    context['invocation']['body'] = copy.deepcopy(context['request'])
    context['request_hash'] = _digest(context['invocation'])

    class MediaPort(DetachedPort):
        def selected_media(self, pin):
            selected, = [value for value in verified if value['selection'] == pin]
            return copy.deepcopy(selected)

    created = create_runtime_commit_service().commit(context, MediaPort(realm, context))
    return realm, baseline, created


# The reserved native media seam must restore acceptance without relaxing Runtime paths.
@pytest.mark.xfail(strict=True, raises=CommitRejected,
                   reason='F-authoring-ABA requires native media collection captures that Runtime can authenticate')
@pytest.mark.parametrize('dry_run', [False, True])
def test_same_alias_inverse_observations_validate(source_control, monkeypatch, tmp_path, dry_run):
    realm, baseline, created = source_control
    captures = []
    original = DetachedPort.preview if dry_run else DetachedPort.accept

    def capture(port, packet):
        # Newly generated offline values; no custody of original11466 is claimed.
        (tmp_path / 'capture.json').write_text(json.dumps(packet, allow_nan=False))
        captures.append(copy.deepcopy(packet))

    def finish(port, prepared):
        (tmp_path / 'prepared.json').write_text(json.dumps(prepared, allow_nan=False))
        (tmp_path / 'history.json').write_text(json.dumps(realm.entries, allow_nan=False))
        with monkeypatch.context() as modules:
            modules.setitem(sys.modules, 'runtime_protocol', runtime_protocol)
            source = created['data']['canonical_document']
            try:
                validate_sequential_capture(port.context['request'], prepared, captures[-1], source, source,
                                            history={row['publication_id']: row for row in realm.entries
                                                     if row['intent'] == 'recorded'})
            except CommitRejected as error:
                assert error.failure['details']['reason'] == 'invalid_records'
                assert error.failure['message'] == 'provider observation has an ambiguous item path'
                raise
        return original(port, prepared)

    monkeypatch.setattr(DetachedPort, 'capture_sequential_execution', capture, raising=False)
    monkeypatch.setattr(DetachedPort, 'preview' if dry_run else 'accept', finish)
    result = submit(realm, undo(created['receipt']['receipt_id']), reads=[], dry_run=dry_run)
    assert result['data']['canonical_document'] == baseline


def test_source_control_has_one_item_and_a_changed_native_observation(source_control):
    realm, _, _ = source_control
    record, = realm.entries[-1]['records']['commands']
    write, = [write for write in record['writes']
              if write['ref'] == OWNER + '/shot' and write['path'][:2] == ['payload', 'items']]
    assert write['before'] != write['after']
    shot, = realm.entries[-1]['receipt']['result']['canonical_document']['shot_revisions']
    assert len(shot['payload']['items']) == 1
    assert shot['payload']['items'][0]['item_id'] == 'item-1'


@pytest.mark.parametrize('rows, token', [
    ([{'item_id': 'a'}], '0'),
    ([{'item_id': 'a'}], 'item_id:missing'),
    ([{'item_id': 'a'}, {'item_id': 'a'}], 'item_id:a'),
])
def test_runtime_strict_item_path_rejects_numeric_missing_and_duplicate(rows, token):
    with pytest.raises(CommitRejected, match='provider observation has an ambiguous item path'):
        location({'items': rows}, ['items', token, 'media_id'])
