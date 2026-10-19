"""Canonical provider compilation and local typed reservations, without acceptance."""
from __future__ import annotations

import copy

import pytest
from jsonschema import Draft202012Validator

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.timeline import commit
from astrid.sdk.timeline._command_state import CommandError, State, present
from astrid.sdk.timeline.commands import _SCHEMA, execute
from tests.editing_conformance.test_recorded_graph_roots import (
    create_command,
    root_values,
)
from tests.editing_conformance.test_recorded_graph_roots import (
    root_ops as root_ops,
)
from tests.sdk.test_timeline_commit_provider_document import document_fixture

pytestmark = pytest.mark.usefixtures('root_ops')


def test_new_roots_close_exact_content_once_and_retain_original_closure():
    source = document_fixture()
    bundle = commit.bundle_from_document(source)
    plan = execute(bundle, [create_command()])
    compilation = compile_authoring_candidate(plan.bundle)
    document = commit.document_from_bundle(plan.bundle)
    new_shot = next(row for row in document['shot_revisions'] if row['shot_id'] == 'new-shot')
    new_internal = next(row for row in document['internal_timeline_revisions']
                        if row['revision_id'] == new_shot['internal_timeline_revision_id'])
    assert new_internal['timeline_id'] == source['timeline_id']
    assert new_internal['payload'] == root_values()[0]['value']['internal_timeline']
    assert new_shot['payload'] == {**root_values()[0]['value']['payload'],
                                  'internal_timeline_revision_id': new_internal['revision_id']}
    assert new_internal['content_digest'] == commit._digest(new_internal['payload'])
    assert new_shot['content_digest'] == commit._digest(new_shot['payload'])
    assert new_shot in compilation.publication['shot_revisions']
    assert new_internal in compilation.publication['internal_timeline_revisions']
    assert document['parent_revision']['payload']['occurrences'][-1] == {
        **root_values()[1]['value'], 'shot_revision_id': new_shot['revision_id']}
    assert source['shot_revisions'][0] in document['shot_revisions']
    assert source['internal_timeline_revisions'][0] in document['internal_timeline_revisions']
    assert compilation.identity_mapping['shots']['new-shot']['source_shot_id'] is None
    assert compilation.identity_mapping['shots']['new-shot']['source_revision_id'] is None
    assert plan.bundle['source_mapping'] == bundle['source_mapping']
    reopened = commit.bundle_from_document(document)
    assert commit.document_from_bundle(reopened) == document
    assert State(reopened).get('occurrence:new-occ/shot', ['shot_id']) == present('new-shot')


@pytest.mark.parametrize('definition,value', [
    ('ScopedId', 'shot:new-shot'), ('EntityRef', 'shot:new-shot'),
    ('TargetKey', 'shot:new-shot::'), ('TargetKey', 'shot:new-shot::payload.metadata'),
    ('AnchorIdentity', 'shot:new-shot'), ('ScopedId', 'occurrence:new-occ'),
])
def test_root_schema_addresses(definition, value):
    Draft202012Validator({'$defs': _SCHEMA['$defs'], '$ref': '#/$defs/' + definition}).validate(value)


@pytest.mark.parametrize('value', ['shot:', 'shot:new/other', 'shot:a::b'])
def test_invalid_shot_root_schema_addresses(value):
    validator = Draft202012Validator({'$defs': _SCHEMA['$defs'], '$ref': '#/$defs/ScopedId'})
    assert not validator.is_valid(value)


class HistoryRejected(Exception):
    def __init__(self, failure):
        self.failure = failure


def reservation_check(monkeypatch, plan, history_records=()):
    # Only the local scan's trusted history input is stubbed. No receipt or
    # Runtime acceptance is constructed; official atomic admission is separate.
    monkeypatch.setattr(commit, '_history', lambda *args: [{
        'intent': 'recorded', 'records': {'schema_version': 1, 'commands': history_records},
    }] if history_records else [])
    commit._check_reservations(None, plan, None, HistoryRejected, None)


def test_typed_roots_are_valid_local_creations_and_retired_roots_are_reserved(monkeypatch):
    original = commit.bundle_from_document(document_fixture())
    plan = execute(original, [create_command()])
    reservation_check(monkeypatch, plan)
    for index in (0, 1):
        history = copy.deepcopy(plan.records)
        root = history[0]['created'][index]
        history[0]['created'] = [root]
        history[0]['command']['created'] = [root['ref']]
        with pytest.raises(CommandError, match='already reserved'):
            reservation_check(monkeypatch, plan, history)


@pytest.mark.parametrize('damage', ['shot-owner', 'occurrence-owner', 'kind', 'ref', 'claim'])
def test_bad_typed_creation_history_refuses(monkeypatch, damage):
    plan = execute(commit.bundle_from_document(document_fixture()), [create_command()])
    history = copy.deepcopy(plan.records)
    items = history[0]['created']
    if damage == 'shot-owner':
        items[0]['owner'] = 'parent'
    elif damage == 'occurrence-owner':
        items[1]['owner'] = None
    elif damage == 'kind':
        items[0]['kind'] = 'track'
    elif damage == 'ref':
        items[0]['ref'] = 'shot:a/b'
    else:
        history[0]['command']['created'] = []
    with pytest.raises(HistoryRejected) as error:
        reservation_check(monkeypatch, plan, history)
    assert error.value.failure['details']['reason'] == 'history_unavailable'


def test_duplicate_batch_and_invalid_new_facts_refuse(monkeypatch):
    plan = execute(commit.bundle_from_document(document_fixture()), [create_command()])
    duplicate = copy.deepcopy(plan)
    duplicate.records.append(copy.deepcopy(plan.records[0]))
    with pytest.raises(CommandError, match='already reserved'):
        reservation_check(monkeypatch, duplicate)
    invalid = copy.deepcopy(plan)
    invalid.records[0]['created'][0]['owner'] = 'parent'
    with pytest.raises(CommandError, match='invalid created identity scope'):
        reservation_check(monkeypatch, invalid)


def test_trusted_inverse_recreation_keeps_identity_reservation(monkeypatch):
    plan = execute(commit.bundle_from_document(document_fixture()), [create_command()])
    # Authenticated inverse dispatch is tested by the existing provider suites;
    # here only its exemption from ordinary fresh allocation is exercised.
    restored = copy.deepcopy(plan)
    restored.records[0]['command']['op'] = 'timeline.inverse'
    reservation_check(monkeypatch, restored, plan.records)
