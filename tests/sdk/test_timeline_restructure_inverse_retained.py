"""Lossless retained G5 inverse input distinguishes native and physical rows."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._collections import AcceptedRecords
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._commit_patch import inverse_address_resolver
from astrid.sdk.timeline._step_undo import select_inverse_records
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document


def retained():
    return json.loads((Path(__file__).parent / 'fixtures/g5_inverse_retained.json').read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def test_retained_inverse_orientation_matches_actual_accepted_input():
    evidence = retained()
    snapshot = copy.deepcopy(evidence)
    source, previous = evidence['source'], evidence['previous']
    assert len(source['parent_revision']['payload']['occurrences']) == 3
    assert len(previous['parent_revision']['payload']['occurrences']) == 1
    assert digest(source['parent_revision']['payload']['config']) == (
        'e6d3e22782252ab1f325c0013214ad30cd9669bcae8b7502321717371fbff4a9')
    assert digest(previous['parent_revision']['payload']['config']) == (
        '3261318905a6bb014857b56b1705960454c99ae9b3e7266dd898cb4867f56115')
    request = evidence['context']['request']
    entry = evidence['history'][request['base_publication_id']]
    before, after = bundle_from_document(previous), bundle_from_document(source)

    def boundary(_entry):
        assert _entry == entry
        return copy.deepcopy((before, after))

    accepted = AcceptedRecords([entry], entry['records']['commands'], boundary)
    resolver = inverse_address_resolver([entry], after, load_boundary=boundary)
    records = select_inverse_records(accepted, address_resolver=resolver)
    plan = execute(after, request['commands'], inverse_records=records, commit_request=request,
                   evaluated_head=evidence['prepared']['expected_head'])
    writes = plan.records[0]['writes']
    assert writes == evidence['prepared']['records']['commands'][0]['writes']
    assert plan.steps == evidence['prepared']['records']['steps']
    assert writes[0]['ref'] == 'parent' and writes[0]['path'] == ['config']
    assert writes[0]['before']['value'] == source['parent_revision']['payload']['config']
    assert writes[0]['after']['value'] == previous['parent_revision']['payload']['config']
    order = next(write for write in writes if write['path'] == ['occurrences'])
    physical = source['parent_revision']['payload']['occurrences']
    assert order['before']['value'] == [
        {key: value for key, value in row.items() if key != 'shot_revision_id'} for row in physical]
    # Pins are compiler output. Adding them to a native order capture violates
    # the existing state setter's requirement to preserve every authored row.
    with pytest.raises(CommandError, match='preserve every authored row'):
        State(copy.deepcopy(after)).set('parent', ['occurrences'],
                                       {'state': 'present', 'value': physical})
    assert evidence == snapshot


@pytest.mark.integration
def test_retained_native_inverse_authenticates_without_changing_authored_rows():
    # R2/G5 requires native order authentication without treating compiler
    # shot_revision_id pins as authored fields. Keep the intended success.
    from tests.helpers.runtime import use_runtime

    use_runtime()
    from runtime_protocol.timeline_commit_auth import validate

    evidence = retained()
    validate(evidence['context']['request'], evidence['prepared'], evidence['source'],
             history=evidence['history'])
