"""Provider input wiring only: no fake acceptance, receipt or Runtime qualification."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import (
    RuntimeCommitService,
    bundle_from_document,
    document_from_bundle,
)
from tests.editing_conformance.test_recipe_m2_media_swap import captured, inputs
from tests.sdk.test_timeline_commit_provider import CommitRejected, refusal
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


class CandidatePort:
    """Portable ABI fixture: selected_media values and preview, never persistence."""

    def __init__(self, document, verified):
        self.document = copy.deepcopy(document)
        self.verified = copy.deepcopy(verified)
        self.base = {'revision_id': document['parent_revision']['revision_id'],
                     'publication_id': 'fixture-base'}
        self.current = copy.deepcopy(self.base)
        self.selections = []
        self.candidate = None
        self.intervening = None

    def head(self):
        return copy.deepcopy(self.current)

    def revision_closure(self, revision):
        if revision == self.base['revision_id']:
            return copy.deepcopy(self.document)
        assert revision == self.current['revision_id']
        return copy.deepcopy(self.intervening['document'])

    def history_entry(self, publication):
        assert publication == self.base['publication_id']
        return {'revision_id': self.base['revision_id']}

    def history(self, through, after_publication_id=None, cursor=None, limit=100):
        assert through == self.current and after_publication_id == self.base['publication_id']
        assert cursor is None
        return {'head': self.head(), 'next_cursor': None, 'items': [{
            **self.current, 'previous': copy.deepcopy(self.base), 'intent': 'recorded',
            'records': {'schema_version': 1, 'commands': copy.deepcopy(self.intervening['records'])}}]}

    def selected_media(self, pin):
        self.selections.append(copy.deepcopy(pin))
        matches = [value for value in self.verified if value['selection'] == pin]
        if not matches:
            raise refusal('dependency_unavailable')
        return copy.deepcopy(matches[0])

    def preview(self, prepared):
        self.candidate = copy.deepcopy(prepared)
        return copy.deepcopy(prepared)

    def accept(self, prepared):
        raise AssertionError('Runtime acceptance is deliberately unqualified in this held slice')


def context(port, commands):
    return {'request': {'project_id': 'project-1', 'timeline_id': 'film',
                       'base_revision_id': port.base['revision_id'],
                       'base_publication_id': port.base['publication_id'],
                       'commands': commands, 'dry_run': True}}


def test_provider_consumes_exact_official_selected_media_shape_and_prepares_candidate():
    document, old, new, verified = inputs()
    _, command, _ = captured()
    port = CandidatePort(document, verified)
    supplied = context(port, [command])
    before = copy.deepcopy(supplied)
    prepared = RuntimeCommitService('fixture-only').commit(supplied, port)
    assert port.selections == [old, new]
    assert supplied == before
    assert prepared['records']['commands'][0]['command'] == command
    assert prepared['canonical_document']['parent_revision']['payload']['clips'][0]['asset'] == new['asset']
    assert [dep['pin'] for dep in prepared['records']['commands'][0]['dependencies']] == [old, new]
    assert 'receipt' not in prepared
    assert document_from_bundle(bundle_from_document(prepared['canonical_document'])) == prepared['canonical_document']


def test_provider_replays_original_verified_pins_on_disjoint_head():
    document, old, new, verified = inputs()
    original, command, _ = captured()
    other = capture_clip_set_params(original, 'parent/clip:clip-b', values={'other': None})
    plan = execute(original, [other])
    port = CandidatePort(document, verified)
    head = document_from_bundle(plan.bundle)
    port.current = {'revision_id': head['parent_revision']['revision_id'], 'publication_id': 'fixture-other'}
    port.intervening = {'document': head, 'records': plan.records}
    prepared = RuntimeCommitService('fixture-only').commit(context(port, [command]), port)
    assert prepared['expected_head'] == port.current
    assert port.selections == [old, new]
    clips = prepared['canonical_document']['parent_revision']['payload']['clips']
    assert clips[0]['asset'] == 'replacement'
    assert clips[1]['params'] == {'other': None}


@pytest.mark.parametrize('side', [0, 1])
def test_provider_port_refusal_of_either_input_never_prepares_any_candidate(side):
    document, _, _, verified = inputs()
    _, command, _ = captured()
    # Runtime owns foreign project, revocation, missing object and stale catalog
    # decisions. Here we only prove its refusal propagates before candidate I/O.
    verified.pop(side)
    port = CandidatePort(document, verified)
    before = copy.deepcopy(document)
    with pytest.raises(CommitRejected) as exc:
        RuntimeCommitService('fixture-only').commit(context(port, [command]), port)
    assert exc.value.failure['details']['reason'] == 'dependency_unavailable'
    assert port.candidate is None
    assert port.document == before
