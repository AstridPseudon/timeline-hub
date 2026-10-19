"""Offline guard provenance and unchanged public refusals; no F consumer inputs."""
import json
import logging
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from http_helpers import Api
from runtime_protocol import authoring_scene, timeline_commit
from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import (AuthoringInvocationRevocationReason as Reason,
                                     AuthorizationError, AuthorizationGuard as Guard)
from test_timeline_accept import IDENTITY, fixture, fixture_provider, http_server, wire
from test_selected_media_commit import snapshot

SECRET = 'private-token-session-actor-project-body-canary'
EXPECTED = {
    'unknown': 'unknown',
    'credential': 'format_unsupported bearer_invalid bearer_required expired scope_required binding_scope_required disabled binding_changed binding_unavailable metadata_invalid',
    'publisher': 'required actor_mismatch',
    'commit_capture': 'media_realm narration_realm narration_project duplicate_provenance media_selection dry_run_accept acceptance_identity dry_run_result revision_closure duplicate_bootstrap narration_take',
    'authoring_invocation': 'owner_unavailable validation_missing evaluation_missing session_required worker_denied project_realm candidate_proof issuer_unavailable binding_changed revoked owner_changed dependency_scope host_changed asset_scope',
    'transcript_capture': 'request_identity issuer_unavailable scope_required',
    'identity': 'runtime_closed bearer_required commit_scope_required',
    'commit_authority': 'paired_session_required',
}


def test_guard_vocabulary_is_stable_and_source_is_assigned_receiver():
    assert {g.value for g in Guard} == {(stage, reason) for stage, reasons in EXPECTED.items()
                                       for reason in reasons.split()}
    assert len(Guard.__members__) == 45  # No aliases silently merge guards.
    assert Path(timeline_commit.__file__).resolve() == Path(__file__).resolve().parents[1] / 'runtime_protocol/timeline_commit.py'


def diagnostic(caplog, invocation_reason=None):
    records = [r for r in caplog.records if r.name == timeline_commit.__name__]
    assert len(records) == 1
    record = records[0]
    assert record.exc_info is None and record.stack_info is None
    assert SECRET not in record.getMessage()
    prefix = 'timeline_commit_failure '
    assert record.getMessage().startswith(prefix)
    value = json.loads(record.getMessage()[len(prefix):])
    expected_keys = {'stage', 'guard', 'exception_class'}
    if invocation_reason is not None:
        expected_keys.add('invocation_reason')
        assert value['invocation_reason'] == invocation_reason
    assert set(value) == expected_keys
    return value


@pytest.mark.parametrize('guard', list(Guard))
def test_only_closed_guard_data_is_logged(caplog, guard):
    exc = AuthorizationError(SECRET, details={'secret': SECRET}, guard=guard)
    exc.code = SECRET
    with caplog.at_level(logging.ERROR, logger=timeline_commit.__name__):
        timeline_commit._record_commit_authorization_failure(exc)
    assert diagnostic(caplog) == dict(stage=guard.value[0], guard=guard.value[1], exception_class='AuthorizationError')
    assert exc.as_dict() == dict(code=SECRET, message=SECRET, details={'secret': SECRET})
    assert '_authorization_guard' not in exc.as_dict()  # Internal metadata never changes the public envelope.


@pytest.mark.parametrize('kind', ['text', 'details', 'subclass'])
def test_untrusted_values_cannot_spoof_guard(caplog, kind):
    if kind == 'subclass':
        class PrivateError(AuthorizationError):
            def __getattribute__(self, key):
                if key == '_authorization_guard':
                    pytest.fail('Do not inspect custom exception attributes')
                return super().__getattribute__(key)
        PrivateError.__name__ = SECRET
        exc = PrivateError(SECRET, guard=Guard.PUBLISHER_REQUIRED)
    else:
        exc = AuthorizationError(SECRET, details={'guard': Guard.PUBLISHER_REQUIRED, 'secret': SECRET},
                                 guard=SECRET if kind == 'text' else {'stage': SECRET})
    with caplog.at_level(logging.ERROR, logger=timeline_commit.__name__):
        timeline_commit._record_commit_authorization_failure(exc)
    assert diagnostic(caplog) == dict(stage='unknown', guard='unknown',
        exception_class='OtherException' if kind == 'subclass' else 'AuthorizationError')


@pytest.mark.parametrize('case, expected_guard, message', [
    ('closed', Guard.IDENTITY_RUNTIME_CLOSED, 'runtime is not accepting authenticated requests'),
    ('no-bearer', Guard.IDENTITY_BEARER_REQUIRED, 'bearer credential required'),
    ('invalid', Guard.CREDENTIAL_BEARER_INVALID, 'invalid bearer credential'),
    ('scope', Guard.CREDENTIAL_SCOPE_REQUIRED, 'credential lacks required scope'),
    ('admin', Guard.IDENTITY_COMMIT_SCOPE_REQUIRED, 'credential lacks explicit commit scope'),
    ('actor', Guard.PUBLISHER_ACTOR_MISMATCH, 'asserted actor does not match authenticated publisher'),
    ('transcript', Guard.TRANSCRIPT_CAPTURE_REQUEST_IDENTITY, 'transcript capture changed request identity'),
    ('scene', Guard.AUTHORING_INVOCATION_REVOKED, 'authoring invocation revoked or unavailable'),
])
@pytest.mark.parametrize('sink_fails', [False, True])
def test_real_commit_route_guard_refusal_is_unchanged_and_redacted(
        fixture, tmp_path, monkeypatch, caplog, case, expected_guard, message, sink_fails):
    service, project = fixture
    fixture_provider(service, project)
    server, thread, api = http_server(service, tmp_path)
    body = wire(project, dry_run=True)
    body['source']['detail'] = SECRET
    if case == 'closed': server.accepting_authenticated_requests = False
    elif case == 'no-bearer': api = Api(api.endpoint, None)
    elif case == 'invalid': api = Api(api.endpoint, SECRET)
    elif case in ('scope', 'admin'):
        token, _ = server.credentials.provision(SECRET, ['projects:read'] if case == 'scope' else ['admin'])
        api = Api(api.endpoint, token)
    elif case == 'actor': body['asserted_actor']['id'] = SECRET
    elif case in ('transcript', 'scene'):
        def commit(request, port):
            if case == 'transcript': return port.resolve_transcript_source({'canary': SECRET}, object())
            return port.scene_evaluator({})
        service._timeline_commit_provider = SimpleNamespace(commit=commit)
    if sink_fails:
        def fail(*args, **kwargs): raise OSError(SECRET)
        monkeypatch.setattr(timeline_commit._LOGGER, 'error', fail)
    before = snapshot(service)
    headers = {'Idempotency-Key': body['request_id'], 'X-Astrid-Session': body['session_id'],
               'X-Request-ID': 'fixed-offline-request'}
    try:
        with caplog.at_level(logging.ERROR, logger=timeline_commit.__name__), pytest.raises(RuntimeError) as error:
            api.request('POST', f'/astrid/v1/projects/{project}/timelines/main/commit', body, headers=headers)
        assert error.value.status == 401
        expected = dict(code='unauthorized', message=message, request_id='fixed-offline-request')
        if case == 'scope': expected['details'] = {'scope': 'projects:write'}
        if case == 'admin': expected['details'] = dict(scope='projects:write', decision=dict(
            status='deny', allowed=False, code='credential_scope_denied'))
        assert error.value.detail == expected
        assert SECRET not in json.dumps(error.value.detail)
        if sink_fails: assert not caplog.records
        else:
            expected_diagnostic = dict(stage=expected_guard.value[0], guard=expected_guard.value[1],
                                       exception_class='AuthorizationError')
            invocation_reason = 'captured_relay_absent' if case == 'scene' else None
            if invocation_reason is not None:
                expected_diagnostic['invocation_reason'] = invocation_reason
            assert diagnostic(caplog, invocation_reason) == expected_diagnostic
            assert project not in caplog.text and body['session_id'] not in caplog.text
            assert IDENTITY['actor'] not in caplog.text
        assert snapshot(service) == before
        assert service.lookup_request(project, 'main', body['request_id']) is None
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.mark.parametrize('case, expected', [
    ('absent', Guard.CREDENTIAL_BEARER_REQUIRED), ('invalid', Guard.CREDENTIAL_BEARER_INVALID),
    ('expired', Guard.CREDENTIAL_EXPIRED), ('format', Guard.CREDENTIAL_FORMAT_UNSUPPORTED),
    ('metadata', Guard.CREDENTIAL_METADATA_INVALID), ('disabled', Guard.CREDENTIAL_DISABLED),
    ('missing-binding', Guard.CREDENTIAL_BINDING_UNAVAILABLE), ('binding', Guard.CREDENTIAL_BINDING_CHANGED),
    ('scope', Guard.CREDENTIAL_BINDING_SCOPE_REQUIRED),
])
def test_credential_guard_is_carried_from_real_site(tmp_path, case, expected):
    store = CredentialStore(tmp_path / 'synthetic-credentials')
    token, _ = store.provision(SECRET, ['projects:read'])
    binding = store._sha256(token.encode())
    if case in ('format', 'metadata', 'expired'):
        metadata = store.actor_metadata(SECRET)
        if case == 'format': metadata['credential_format'] = 'unsupported'
        elif case == 'metadata': metadata['scopes'] = 'invalid'
        else: metadata['expires_at'] = time.time() - 60
        store._publish(SECRET, token, metadata)
    if case == 'disabled': store.disable_actor(SECRET)
    with pytest.raises(AuthorizationError) as error:
        if case == 'absent': store.load('')
        elif case == 'invalid': store.load('unknown-token')
        elif case in ('format', 'metadata', 'expired'): store.load(token)
        else: store.validate_binding('absent' if case == 'missing-binding' else SECRET,
                                     'changed' if case == 'binding' else binding, 'projects:write')
    assert error.value._authorization_guard is expected


def test_commit_authority_and_scene_guards_remain_authorization(fixture):
    service, project = fixture
    with pytest.raises(AuthorizationError) as error:
        service._assert_commit_authority({'connector_assertion': {'canary': SECRET}}, project)
    assert error.value._authorization_guard is Guard.COMMIT_AUTHORITY_PAIRED_SESSION_REQUIRED
    with pytest.raises(AuthorizationError) as error:
        authoring_scene._session({'actor': SECRET})
    assert error.value._authorization_guard is Guard.AUTHORING_INVOCATION_SESSION_REQUIRED


def test_session_validation_is_not_authorization(fixture, tmp_path, caplog):
    service, project = fixture
    server, thread, api = http_server(service, tmp_path)
    body = wire(project, dry_run=True)
    try:
        with pytest.raises(RuntimeError) as error:
            api.request('POST', f'/astrid/v1/projects/{project}/timelines/main/commit', body,
                headers={'Idempotency-Key': body['request_id'], 'X-Astrid-Session': SECRET})
        assert error.value.status == 400
        assert error.value.detail['error']['code'] == 'bad_request'
        assert SECRET not in json.dumps(error.value.detail)
        assert not caplog.records
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_logging_failure_rethrows_same_original_refusal(monkeypatch):
    from runtime_protocol.server import RuntimeHandler
    original = AuthorizationError('bearer credential required', guard=Guard.IDENTITY_BEARER_REQUIRED)
    handler = RuntimeHandler.__new__(RuntimeHandler)
    def refuse(*args): raise original
    def fail(*args, **kwargs): raise OSError(SECRET)
    monkeypatch.setattr(handler, '_authorized_timeline_commit', refuse)
    monkeypatch.setattr(timeline_commit._LOGGER, 'error', fail)
    with pytest.raises(AuthorizationError) as error:
        handler._timeline_commit(SECRET, SECRET)
    assert error.value is original


def test_diagnostic_never_reads_message_args_or_details(caplog):
    class Unreadable:
        def __str__(self): pytest.fail('message/args/details must not be stringified')
        def __repr__(self): pytest.fail('message/args/details must not be represented')
        def __iter__(self): pytest.fail('details must not be inspected')
    value = Unreadable()
    exc = AuthorizationError(value, details=value, guard=Guard.CREDENTIAL_BINDING_CHANGED)
    with caplog.at_level(logging.ERROR, logger=timeline_commit.__name__):
        timeline_commit._record_commit_authorization_failure(exc)
    assert diagnostic(caplog) == dict(stage='credential', guard='binding_changed', exception_class='AuthorizationError')


@pytest.mark.parametrize('case, expected', [
    ('scope', Guard.TRANSCRIPT_CAPTURE_SCOPE_REQUIRED),
    ('issuer', Guard.TRANSCRIPT_CAPTURE_ISSUER_UNAVAILABLE),
])
def test_transcript_capture_carries_actual_authority_guard(fixture, case, expected):
    from astrid.sdk.timeline.transcripts import TranscriptSourceSelection
    from test_transcript_commit import source
    service, project = fixture
    descriptor = source(service, project)
    body = wire(project, dry_run=True)
    identity = dict(actor=IDENTITY['actor'], scopes=['projects:write'])
    if case == 'issuer':
        identity['scopes'].append('objects:read')
        identity['_credential_binding'] = SECRET
    selection = TranscriptSourceSelection.from_reference(project, descriptor)
    before = snapshot(service)
    port = service._request_commit_port(body, identity)
    try:
        with pytest.raises(AuthorizationError) as error:
            port.resolve_transcript_source(body, selection)
        assert error.value._authorization_guard is expected
        assert snapshot(service) == before
    finally:
        port.close()


def test_invocation_reason_vocabulary_is_closed():
    assert {reason.value for reason in Reason} == {
        'evaluation_cancelled', 'captured_relay_absent', 'current_relay_replaced'}
    assert len(Reason.__members__) == 3


@pytest.mark.parametrize('guard, value', [
    (Guard.AUTHORING_INVOCATION_REVOKED, SECRET),
    (Guard.AUTHORING_INVOCATION_REVOKED, {'reason': SECRET}),
    (Guard.IDENTITY_BEARER_REQUIRED, Reason.EVALUATION_CANCELLED),
])
def test_untrusted_or_unrelated_invocation_reason_is_not_logged(caplog, guard, value):
    exc = AuthorizationError(SECRET, guard=guard, invocation_reason=value)
    # Also defend the sink if trusted code later overwrites the private field.
    exc._authoring_invocation_reason = value
    with caplog.at_level(logging.ERROR, logger=timeline_commit.__name__):
        timeline_commit._record_commit_authorization_failure(exc)
    assert diagnostic(caplog) == dict(stage=guard.value[0], guard=guard.value[1],
                                      exception_class='AuthorizationError')


@pytest.mark.parametrize('reason', list(Reason))
@pytest.mark.parametrize('sink_fails', [False, True])
def test_real_commit_invocation_reason_stays_internal(
        fixture, tmp_path, monkeypatch, caplog, reason, sink_fails):
    service, project = fixture
    fixture_provider(service, project)
    relay = SimpleNamespace(config=SimpleNamespace(binding={'canary': SECRET}))
    service._authoring_scene_relay = None if reason is Reason.CAPTURED_RELAY_ABSENT else relay
    monkeypatch.setattr(authoring_scene, 'check_binding', lambda *args: None)

    def commit(request, port):
        if reason is not Reason.CAPTURED_RELAY_ABSENT:
            port.scene_evaluator({})  # Capture the synthetic relay through the real port.
            if reason is Reason.EVALUATION_CANCELLED:
                port.close()
            else:
                service._authoring_scene_relay = SimpleNamespace(canary=SECRET)
        return port.scene_evaluator({})

    service._timeline_commit_provider = SimpleNamespace(commit=commit)
    if sink_fails:
        def fail(*args, **kwargs): raise OSError(SECRET)
        monkeypatch.setattr(timeline_commit._LOGGER, 'error', fail)
    server, thread, api = http_server(service, tmp_path)
    body = wire(project, dry_run=True)
    before = snapshot(service)
    try:
        with caplog.at_level(logging.ERROR, logger=timeline_commit.__name__), pytest.raises(RuntimeError) as error:
            api.request('POST', f'/astrid/v1/projects/{project}/timelines/main/commit', body,
                        headers={'Idempotency-Key': body['request_id'],
                                 'X-Astrid-Session': body['session_id'],
                                 'X-Request-ID': 'fixed-offline-request'})
        assert error.value.status == 401
        assert error.value.detail == dict(code='unauthorized',
            message='authoring invocation revoked or unavailable', request_id='fixed-offline-request')
        if sink_fails:
            assert not caplog.records
        else:
            assert diagnostic(caplog, reason.value) == dict(stage='authoring_invocation',
                guard='revoked', exception_class='AuthorizationError', invocation_reason=reason.value)
            assert project not in caplog.text and body['session_id'] not in caplog.text
            assert IDENTITY['actor'] not in caplog.text
        assert snapshot(service) == before
        assert service.lookup_request(project, 'main', body['request_id']) is None
    finally:
        # The synthetic relay has no lifecycle/transport authority.
        service._authoring_scene_relay = None
        server.shutdown()
        server.server_close()
        thread.join()
