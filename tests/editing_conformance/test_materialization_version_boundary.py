"""Public v1 capture compatibility and explicit source-bound v2 authoring."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_placement_commands import capture_placement
from tests.editing_conformance.fixture_loader import load_fixture
from tests.editing_conformance.test_recipe_m2_placement import FIXTURE as PLACEMENT
from tests.editing_conformance.test_recipe_occurrence_media import FIXTURE as MEDIA
from tests.editing_conformance.test_recipe_occurrence_media import MATERIALIZATION_FIXTURE


@pytest.mark.parametrize('kind', ['placement', 'add', 'swap'])
def test_complete_public_s2_v1_keeps_original_capture_records_output_and_map(kind):
    if kind == 'placement':
        case = next(case for case in load_fixture(PLACEMENT)['cases']
                    if case['command']['select'].startswith('occurrence:'))
        commands, verified = [case['command']], []
    else:
        case = load_fixture(MEDIA)[kind]
        commands, verified = case['commands'], case['verified_media']
    original = copy.deepcopy(commands)
    # Default provider ingress opens the full verified closure, unlike legacy
    # golden setup. It must still accept the original public S2 v1 bytes.
    plan = execute(bundle_from_document(case['input']), commands, verified_media=verified)
    assert plan.commands == original and commands == original
    assert plan.records == case['records'] and plan.id_map == {}
    assert document_from_bundle(plan.bundle) == case['output']


def test_v1_placement_version_flip_cannot_supply_source_proof_and_v2_reauthor_succeeds():
    # legacy-capture-counterexamples.json: old_sealed_placement.command.
    case = next(case for case in load_fixture(PLACEMENT)['cases']
                if case['command']['select'].startswith('occurrence:'))
    command = copy.deepcopy(case['command'])
    bundle = bundle_from_document(case['input'])
    assert (len(command['reads']), len(command['selections'])) == (103, 3)
    with pytest.raises(CommandError, match='explicitly re-author'):
        execute(bundle, [{**command, 'version': '2'}])
    current = capture_placement(bundle, 'occurrence:occ-a', 'clip-a', command['args']['on'],
                                ownership='occurrence')
    assert current['version'] == '2'
    plan = execute(bundle, [current])
    assert document_from_bundle(plan.bundle) == case['output']
    assert plan.id_map and plan.commands == [current]
    # A v1 request without the carrier cannot claim v2 allocation mappings.
    with pytest.raises(CommandError, match='verified allocations'):
        execute(bundle, [command], id_map=plan.id_map)
    assert command == case['command']


@pytest.mark.parametrize('missing', ['resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'])
def test_sealed_v2_missing_original_proof_fails_closed(missing):
    case = next(case for case in load_fixture(PLACEMENT)['cases']
                if case['command']['select'].startswith('occurrence:'))
    bundle = bundle_from_document(case['input'])
    command = capture_placement(bundle, 'occurrence:occ-a', 'clip-a', case['command']['args']['on'],
                                ownership='occurrence')
    original = copy.deepcopy(command)
    del command[missing]
    with pytest.raises(CommandError, match='incomplete v2 capture'):
        execute(bundle, [command])
    assert command == {key: value for key, value in original.items() if key != missing}


@pytest.mark.parametrize('version', [None, False, True, 2, '0', '02', '2.0', '3'])
def test_malformed_or_unknown_operation_version_fails_closed(version):
    case = load_fixture(MATERIALIZATION_FIXTURE)['add']
    command = {**case['commands'][0], 'version': version}
    with pytest.raises(CommandError):
        validate_command(command)


def test_source_bound_v2_cannot_use_an_unverified_legacy_bundle():
    case = next(case for case in load_fixture(PLACEMENT)['cases']
                if case['command']['select'].startswith('occurrence:'))
    bundle = bundle_from_document(case['input'], capture_sources=False)
    with pytest.raises(CommandError, match='verified original closure'):
        execute(bundle, [{**case['command'], 'version': '2'}])


@pytest.mark.parametrize('kind', ['placement', 'add', 'swap'])
def test_accepted_private_v1_history_survives_json_reload_inverse_redo_restore(monkeypatch, kind):
    import json

    from astrid.sdk.timeline._materialization import id_map
    from astrid.sdk.timeline.commit import _digest
    from tests.editing_conformance.test_recipe_m2_placement import (
        MATERIALIZATION_FIXTURE as PRIVATE_PLACEMENT,
    )
    from tests.sdk.test_timeline_commit_provider import (
        DetachedPort,
        DetachedRealm,
        inverse,
        restore,
        runtime_abi,
    )

    runtime_abi.__wrapped__(monkeypatch)
    if kind == 'placement':
        case = next(case for case in load_fixture(PRIVATE_PLACEMENT)['cases']
                    if case['command']['select'].startswith('occurrence:'))
        commands = [case['command']]
    else:
        case = load_fixture(MATERIALIZATION_FIXTURE)[kind]
        commands = case['commands']
    realm = DetachedRealm(case['input'])
    context = realm.context(commands)
    # Model already accepted, authenticated history at the existing port. This
    # exercises provider semantics only, never Runtime admission or its ledger.
    accepted = DetachedPort(realm, context).accept({
        'expected_head': copy.deepcopy(realm.head), 'canonical_document': case['output'],
        'document_digest': _digest(case['output']),
        'records': {'schema_version': 1, 'commands': case['records'], 'undo_of': [], 'restored_from': None},
        'id_map': id_map(case['records']), 'semantic_events': [], 'provider_version': 'astrid-v1',
        'compiler_version': 'authoring-bundle-1'})
    snapshot = json.loads(json.dumps({'documents': realm.documents, 'entries': realm.entries, 'head': realm.head}))
    reloaded = DetachedRealm(case['input'])
    for key, value in snapshot.items():
        setattr(reloaded, key, value)
    undone = reloaded.call([inverse([accepted['receipt']['receipt_id']])])
    assert undone['data']['canonical_document'] == case['input']
    redone = reloaded.call([inverse([undone['receipt']['receipt_id']])])
    assert redone['data']['canonical_document'] == case['output']
    restored = reloaded.call([restore(case['input'])])
    assert restored['data']['canonical_document'] == case['input']
    assert reloaded.entries[1]['records']['commands'] == case['records']


def test_obsolete_add_refuses_before_provider_prepare_with_original_draft(monkeypatch):
    from tests.sdk.test_timeline_commit_provider import DetachedPort, DetachedRealm, runtime_abi

    runtime_abi.__wrapped__(monkeypatch)
    from runtime_protocol.timeline_commit import CommitRejected

    case = load_fixture(MATERIALIZATION_FIXTURE)['add']
    monkeypatch.setattr(DetachedPort, 'selected_media', lambda self, pin: copy.deepcopy(next(
        value for value in case['verified_media'] if value['selection'] == pin)))
    realm = DetachedRealm(case['input'])
    command = copy.deepcopy(case['commands'][0])
    original = copy.deepcopy((command, realm.head, realm.documents, realm.entries))
    with pytest.raises(CommitRejected) as error:
        realm.call([command])
    assert error.value.failure['details']['reason'] == 'capture_mismatch'
    assert 'keep the draft and explicitly re-author' in error.value.failure['message']
    assert (command, realm.head, realm.documents, realm.entries) == original
    assert realm.prepared == realm.accepted == []


def test_obsolete_capture_refusal_keeps_exact_durable_outbox_across_restart(tmp_path, monkeypatch):
    from types import SimpleNamespace

    from astrid.sdk.timeline.outbox import Outbox, request_bytes
    from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
    from astrid.sdk.workspace_client import WorkspaceClientError
    from tests.sdk.test_timeline_commit_provider import DetachedPort, DetachedRealm, runtime_abi

    runtime_abi.__wrapped__(monkeypatch)
    from runtime_protocol.timeline_commit import CommitRejected

    case = load_fixture(MATERIALIZATION_FIXTURE)['add']
    monkeypatch.setattr(DetachedPort, 'selected_media', lambda self, pin: copy.deepcopy(next(
        value for value in case['verified_media'] if value['selection'] == pin)))
    realm = DetachedRealm(case['input'])
    identity = {'realm_id': 'realm-1', 'actor_id': 'actor-1'}
    outbox = Outbox(tmp_path / 'obsolete.json')
    # Exact persisted draft from the old client, never re-captured by the new one.
    outbox.write({'scope': {**identity, 'project_id': 'project-1', 'timeline_id': 'film'},
                  'base': copy.deepcopy(realm.head), 'pending': copy.deepcopy(case['commands']), 'flight': None})
    sent = []

    def commit(project, timeline, body, *, idempotency_key):
        sent.append((request_bytes(body), idempotency_key))
        try:
            return realm.call(body['commands'])
        except CommitRejected as exc:
            failure = exc.failure
            raise WorkspaceClientError(failure['http_status'], failure['code'], failure['message'],
                                       failure['details']) from exc

    client = SimpleNamespace(
        _remote=SimpleNamespace(_transport=SimpleNamespace(_last_handshake=identity)),
        timelines=SimpleNamespace(commit=commit))
    first_flight = None
    for _ in range(2):
        session = TimelineSession(client, Outbox(outbox.path), identity, 'project-1', 'film')
        with pytest.raises(CommitConflict) as error:
            session.flush(idempotency_key='original-obsolete-request')
        state = outbox.read()
        assert 'explicitly re-author' in str(error.value)
        assert state['pending'] == case['commands'] and state['base'] == realm.head
        if first_flight is None:
            first_flight = copy.deepcopy(state['flight'])
        assert state['flight'] == first_flight and state['conflict']['details']['reason'] == 'capture_mismatch'
    assert sent[0] == sent[1] and realm.prepared == realm.accepted == []
