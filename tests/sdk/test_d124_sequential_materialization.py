"""Sequential child edits through the registered production provider."""
from __future__ import annotations

import pytest

from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from tests.sdk.test_timeline_commit_native_boundary_runtime import (
    child_tracks,
)
from tests.sdk.test_timeline_commit_native_boundary_runtime import (
    native_child as native_child,
)

pytestmark = pytest.mark.integration


def test_materialization_keeps_step_source_and_complete_successor_edges(request):
    _, document, _ = request.getfixturevalue('native_child')
    before = document()
    bundle = bundle_from_document(before)
    calls = child_tracks(before)
    intermediate = document_from_bundle(execute(bundle, calls[:1]).bundle)
    plan = execute(bundle, calls, commit_request={})
    after = document_from_bundle(plan.bundle)
    first, middle, last = [value['shot_revisions'][0] for value in (before, intermediate, after)]
    assert len({first['revision_id'], middle['revision_id'], last['revision_id']}) == 3
    assert len({value['internal_timeline_revision_id'] for value in (first, middle, last)}) == 3
    step, = plan.steps
    assert step['command_ordinals'] == [0, 1]
    assert not any(binding['key'] == 'commit.materialization' for binding in plan.records[0]['bindings'])
    bindings = [binding for binding in plan.records[1]['bindings'] if binding['key'] == 'commit.materialization']
    expected = {
        ('shot-revision:' + first['revision_id'], 'shot-revision:' + last['revision_id'],
         'internal-revision:' + first['internal_timeline_revision_id'],
         'internal-revision:' + last['internal_timeline_revision_id']),
        ('internal-revision:' + first['internal_timeline_revision_id'],
         'internal-revision:' + last['internal_timeline_revision_id'],
         'shot-revision:' + first['revision_id'], 'shot-revision:' + last['revision_id']),
    }
    assert len(bindings) == 2
    assert {(binding['physical_ref'], binding['successor'], binding['edge_before'], binding['edge_after'])
            for binding in bindings} == expected
    for binding in bindings:
        assert binding['boundary']['command_ordinal'] == 1
        assert binding['boundary']['step_id'] == step['id'] == binding['step_id']
        assert binding['owners'] == [binding['owner']] == ['occurrence:child/shot']


def test_grouped_child_materialization_uses_the_complete_step_input(request):
    _, document, submit = request.getfixturevalue('native_child')
    before = document()
    accepted = submit(child_tracks(before), 'grouped-tracks')
    assert accepted['data']['status'] == 'accepted'
    assert [row['id'] for row in document()['internal_timeline_revisions'][0]['payload']['tracks']] == ['one', 'two']
    inverse = {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
               'args': {'publications': [accepted['receipt']['receipt_id']]}}
    assert submit([inverse], 'undo-grouped-tracks')['data']['canonical_document'] == before
