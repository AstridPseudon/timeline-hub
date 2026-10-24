"""Offline landing/prepared parity through the mounted Agent commit caller."""
from __future__ import annotations

import copy
import json

import pytest

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, bundle_from_document, document_from_bundle
from tests.editing_conformance.test_doc_patch_v2 import submit
from tests.editing_conformance.test_occurrence_media_manifest_inverse import accepted_records
from tests.editing_conformance.test_provider_step_undo_v2 import undo
from tests.editing_conformance.test_recipe_occurrence_media import (
    same_alias_realm as same_alias_realm,
)
from tests.sdk.test_timeline_commit_provider import DetachedPort
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


@pytest.mark.parametrize('dry_run', [False, True])
def test_same_alias_inverse_landing_matches_prepared_document(
    request, monkeypatch, tmp_path, dry_run,
):
    # These are generated offline fixture values, not the missing 13559 packet.
    realm, baseline, created = request.getfixturevalue('same_alias_realm')
    before = copy.deepcopy((realm.head, realm.documents, realm.entries))
    captures = []
    prepared_values = []

    def capture(port, value):
        packet = copy.deepcopy(value)
        (tmp_path / 'private-capture.json').write_text(json.dumps(packet, allow_nan=False))
        captures.append(packet)

    method = DetachedPort.preview if dry_run else DetachedPort.accept

    def finish(port, prepared):
        # Retain complete values before applying Runtime's exact comparison.
        (tmp_path / 'prepared.json').write_text(json.dumps(prepared, allow_nan=False))
        prepared_values.append(copy.deepcopy(prepared))
        packet, = captures
        assert set(packet) == {'schema_version', 'context', 'original', 'landing',
                               'replay_bindings', 'prepared_digest'}
        assert packet['prepared_digest'] == _digest(prepared)
        assert packet['landing']['records'] == prepared['records']
        assert prepared['canonical_document'] == baseline
        for execution in (packet['landing'], packet['original']):
            command, = execution['commands']
            assert command['input'] == created['data']['canonical_document']
            bundle_from_document(command['output'])
            assert command['output'] == prepared['canonical_document']
        return method(port, prepared)

    monkeypatch.setattr(DetachedPort, 'capture_sequential_execution', capture, raising=False)
    monkeypatch.setattr(DetachedPort, 'preview' if dry_run else 'accept', finish)
    result = submit(realm, undo(created['receipt']['receipt_id']), reads=[], dry_run=dry_run)
    assert len(captures) == len(prepared_values) == 1
    assert result['data']['canonical_document'] == baseline
    if dry_run:
        assert result['receipt'] is None
        assert (realm.head, realm.documents, realm.entries) == before
    else:
        assert result['receipt']['result'] == result['data']


def test_same_alias_final_projection_requires_selected_accepted_records(request):
    realm, baseline, created = request.getfixturevalue('same_alias_realm')
    records = accepted_records(realm, realm.entries[-1])
    sources = [source for entry in records.entries for source in records.load_boundary(entry)]
    plan = execute(bundle_from_document(created['data']['canonical_document']),
                   [undo(created['receipt']['receipt_id'])], inverse_records=records,
                   commit_request={'reads': []}, evaluated_head=copy.deepcopy(realm.head))
    assert document_from_bundle(plan.bundle, source_bundles=sources,
                                inverse_records=records) == baseline
    # Historical closures or an unbound list of recorder rows cannot grant the
    # manifest-removal authority that the final production compiler requires.
    with pytest.raises(CommandError, match='media inverse needs accepted boundaries'):
        document_from_bundle(plan.bundle, source_bundles=sources, inverse_records=list(records))
