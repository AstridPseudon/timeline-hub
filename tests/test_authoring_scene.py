"""Production COMMIT port/auth/transaction with an explicit synthetic relay.

No renderer/native source admission witness is claimed by this fixture.
"""
import copy
from types import SimpleNamespace

import pytest

from runtime_protocol import authoring_scene as scene
from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import AuthorizationError
from runtime_protocol.timeline_commit import digest
from test_timeline_accept import fixture, wire, acceptance, count  # noqa: F401


def projection():
    return dict(timeline=dict(theme='banodoco-default', clips=[], tracks=[], theme_overrides={}),
                assets={'assets': {}}, fps=24, width=320, height=180, roles={})


@pytest.mark.parametrize('edge', [None, 'path', 'url', 'extra', 'type', 'divergent', 'identity'])
def test_checkout_display_registry_is_projected_to_strict_cas_without_location_authority(edge):
    from astrid.core.execution import authoring_scene_protocol as wire
    from astrid.core.execution.remotion_frame_owner import FrameOwnerError
    value = projection(); oid = 'sha256:' + 'a' * 64
    entry = dict(media_id=oid, file=oid, type='video', width=16, height=16)
    if edge == 'path': entry['file'] = '/unadmitted/location'
    elif edge == 'url': entry['file'] = 'https://unadmitted.invalid/media'
    elif edge == 'extra': entry['url'] = oid
    elif edge == 'type': entry['type'] = 'callback'
    elif edge == 'divergent': entry['object_id'] = 'sha256:' + 'b' * 64
    elif edge == 'identity': entry['media_id'] = 'not-cas'
    value['assets']['assets']['picture'] = entry
    original = copy.deepcopy(value)
    if edge is not None:
        with pytest.raises(FrameOwnerError): scene._scene_cas_projection(value)
    else:
        projected = scene._scene_cas_projection(value)
        assert wire.assets(projected) == {oid}
        assert projected['assets']['assets']['picture'] == dict(media_id=oid, width=16, height=16)
    assert value == original


@pytest.fixture
def bound(fixture, tmp_path, monkeypatch):
    from astrid.core.execution import authoring_scene_protocol as protocol
    s, p = fixture
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('fixture-writer', ['projects:write', 'projects:read', 'objects:read'])
    identity = dict(actor='fixture-writer', scopes=['projects:write', 'objects:read'],
                    _credential_binding=credentials._sha256(token.encode()))
    s._task_credentials = credentials
    calls = []
    class Relay:
        def __init__(self):
            self.config = SimpleNamespace(binding={k: (1 if k == 'owner_generation' else 'astrid-v1' if k == 'provider_id'
                else 'sha256:' + 'a' * 64 if k.endswith('digest') or k == 'renderer_closure' else k)
                for k in protocol.CONTEXT_FIELDS})
            self.on_reply = lambda: None
            self.closed = False
        def check_live(self):
            if self.closed: raise AuthorizationError('relay revoked')
        def exchange(self, request, *, guard, cancelled):
            guard()
            protocol.validate_request(request, self.config.binding)
            calls.append(copy.deepcopy(request))
            self.on_reply()
            return [dict(frame=f, layers=[], coverage='GAP', content=None, findings=[]) for f in request['frames']]
        def close(self): self.closed = True
    relay = s._authoring_scene_relay = Relay()
    # Narrow trusted admission/transport fixture; actual request port/session/
    # credential rechecks and the existing atomic acceptance boundary stay real.
    monkeypatch.setattr(scene, 'check_binding', lambda service, selected: selected.check_live())
    s._timeline_commit_provider = SimpleNamespace(requires_scene_evaluation=True)
    return SimpleNamespace(s=s, p=p, identity=identity, credentials=credentials, relay=relay, calls=calls)


def evaluate(w, port, candidate):
    from astrid.core.execution import authoring_scene_protocol as protocol
    client = port.scene_evaluator(candidate)
    value = projection()
    client.query_scene(revision_digest=protocol.digest(value)[7:], scene=value, frames=[0])
    client.complete()
    client.close()
    return client


def test_private_refusal_keeps_source_frames_without_exception_text(bound, monkeypatch, capsys):
    from astrid.core.execution import authoring_scene_protocol as protocol
    from astrid.core.execution.remotion_frame_owner import FrameOwnerError
    w = bound; port = scene.RequestSceneEvaluation(w.s, wire(w.p), w.identity)
    client = port.evaluator({'candidate': 'bound'})
    def failed(*args, **kwargs): raise TypeError('secret-credential /private/untrusted-path')
    monkeypatch.setattr(w.relay, 'exchange', failed)
    value = projection()
    with pytest.raises(FrameOwnerError, match='authoring_evaluation_refused'):
        client.query_scene(revision_digest=protocol.digest(value)[7:], scene=value, frames=[0])
    captured = capsys.readouterr().err
    assert 'TypeError' in captured and 'test_authoring_scene.py' in captured
    assert 'secret-credential' not in captured and '/private/untrusted-path' not in captured
    port.close()


def test_authenticated_port_binds_complete_candidate_at_atomic_accept(bound):
    w = bound
    body = wire(w.p)
    prepared = acceptance(w.s, w.p, request=body)
    port = w.s._request_commit_port(body, w.identity)
    evaluate(w, port, prepared['result']['canonical_document'])
    result = port.accept(prepared)
    assert result['stored_result']['status'] == 'accepted'
    binding = w.calls[0]['invocation']
    assert binding['request_hash'] == digest(body)
    assert binding['candidate_digest'] == digest(prepared['result']['canonical_document'])
    assert binding['actor'] == w.identity['actor'] and binding['actor_session'] != body['session_id']
    port.close()
    # Replay is durable and precedes owner evaluation, even after relay loss.
    w.s._authoring_scene_relay = None
    w.s._timeline_commit_provider = SimpleNamespace(commit=lambda *a: pytest.fail('replayed provider invoked'))
    assert w.s.commit_timeline(w.p, 'main', body, idempotency_key=body['request_id'], identity=w.identity) == result['stored_result']


@pytest.mark.parametrize('phase', ['before', 'after_reply', 'accept'])
def test_credential_loss_refuses_without_publication(bound, phase):
    from astrid.core.execution.remotion_frame_owner import FrameOwnerError
    w = bound
    body = wire(w.p)
    prepared = acceptance(w.s, w.p, request=body)
    port = w.s._request_commit_port(body, w.identity)
    before = count(w.s, 'parent_composition_publications')
    if phase == 'before': w.credentials.disable_actor(w.identity['actor'])
    elif phase == 'after_reply': w.relay.on_reply = lambda: w.credentials.disable_actor(w.identity['actor'])
    if phase == 'accept':
        evaluate(w, port, prepared['result']['canonical_document'])
        w.credentials.disable_actor(w.identity['actor'])
    with pytest.raises((AuthorizationError, FrameOwnerError)):
        if phase == 'accept': port.accept(prepared)
        else: evaluate(w, port, prepared['result']['canonical_document'])
    assert count(w.s, 'parent_composition_publications') == before
    assert w.s.lookup_request(w.p, 'main', body['request_id']) is None
    if phase == 'before': assert w.calls == []
    port.close()


@pytest.mark.parametrize('case', ['missing', 'candidate', 'request', 'revoked', 'source', 'new_retry'])
def test_atomic_candidate_and_lifecycle_fences(bound, case):
    w = bound
    body = wire(w.p)
    prepared = acceptance(w.s, w.p, request=body)
    port = w.s._request_commit_port(body, w.identity)
    if case != 'missing': evaluate(w, port, prepared['result']['canonical_document'])
    if case == 'candidate':
        prepared['result']['canonical_document']['foreign'] = True
        # Keep all ordinary digest validation coherent to reach scene fence.
        prepared['result']['document_digest'] = digest(prepared['result']['canonical_document'])
        prepared['evidence']['digests']['after'] = prepared['result']['document_digest']
    elif case == 'request': prepared['request_hash'] = digest({'foreign': True})
    elif case == 'revoked': port.close()
    elif case == 'source': w.relay.closed = True
    elif case == 'new_retry': port.scene_evaluator({'different post-rebase candidate': True})
    before = count(w.s, 'parent_composition_publications')
    with pytest.raises(Exception): port.accept(prepared)
    assert count(w.s, 'parent_composition_publications') == before
    assert w.s.lookup_request(w.p, 'main', body['request_id']) is None
    port.close()


def test_dry_run_cannot_accept_or_reserve_even_with_scene_completion(bound):
    w = bound
    body = wire(w.p, dry_run=True)
    port = w.s._request_commit_port(body, w.identity)
    evaluate(w, port, {'candidate': True})
    with pytest.raises(AuthorizationError, match='dry-run'):
        port.accept({})
    assert w.s.lookup_request(w.p, 'main', body['request_id']) is None
    port.close()


def test_worker_credential_and_missing_session_never_reach_relay(bound):
    w = bound
    for identity in (dict(actor='fixture-writer', scopes=['projects:write']),
                     {**w.identity, 'execution_binding': {'worker': True}}):
        port = w.s._request_commit_port(wire(w.p), identity)
        with pytest.raises(AuthorizationError): port.scene_evaluator({'candidate': True})
        port.close()
    assert w.calls == []


_REAL_CHECK_BINDING = scene.check_binding


@pytest.mark.parametrize('change', [None, 'epoch', 'source', 'dependency', 'capability', 'session'])
def test_real_registered_source_binding_checks_exact_catalog_tuple(bound, change):
    from astrid.core.execution.authoring_scene_startup import provider_digest
    w = bound
    s, c = w.s, w.relay.config.binding
    s.runtime_instance_id = 'selected-instance'
    c.update(runtime_realm_id=s.realm['id'], runtime_instance_id=s.runtime_instance_id,
             runtime_session_id=s.runtime_session_id, provider_digest=provider_digest())
    descriptor = dict(capability_id='rendering.timeline_visualize', definition_digest=c['capability_digest'],
                      status='ready', required_resource_keys=[])
    s.store.upsert_executor(c['executor_id'], [descriptor], runtime_epoch=s.store._current_runtime_epoch(),
        source_epoch=c['source_epoch'], source_digest=c['executor_source_digest'][7:],
        dependency_digest=c['executor_dependency_digest'][7:])
    if change == 'epoch': c['source_epoch'] = 'foreign'
    elif change == 'source': c['executor_source_digest'] = 'sha256:' + '0' * 64
    elif change == 'dependency': c['executor_dependency_digest'] = 'sha256:' + '0' * 64
    elif change == 'capability': c['capability_digest'] = 'sha256:' + '0' * 64
    elif change == 'session': c['runtime_session_id'] = 'foreign'
    if change is None: _REAL_CHECK_BINDING(s, w.relay)
    else:
        with pytest.raises(Exception): _REAL_CHECK_BINDING(s, w.relay)


@pytest.mark.parametrize('phase', ['reply', 'accept'])
def test_project_dependency_custody_rechecked_before_reply_and_accept(bound, monkeypatch, phase):
    from astrid.core.execution import authoring_scene_protocol as protocol
    from astrid.core.execution.remotion_frame_owner import FrameOwnerError
    w = bound
    oid = w.s.ingest(w.p, b'synthetic media', media_type='image/png', idempotency_key='asset')['data']['object_id']
    body = wire(w.p)
    prepared = acceptance(w.s, w.p, request=body)
    port = w.s._request_commit_port(body, w.identity)
    client = port.scene_evaluator(prepared['result']['canonical_document'])
    value = projection()
    value['assets']['assets']['x'] = {'media_id': oid}
    def revoke():
        w.s.store.conn.execute('DELETE FROM project_objects WHERE project_id=? AND digest=?', (w.p, oid[7:]))
    if phase == 'reply': w.relay.on_reply = revoke
    if phase == 'reply':
        with pytest.raises(FrameOwnerError):
            client.query_scene(revision_digest=protocol.digest(value)[7:], scene=value, frames=[0])
    else:
        client.query_scene(revision_digest=protocol.digest(value)[7:], scene=value, frames=[0])
        client.complete()
        revoke()
        with pytest.raises(Exception): port.accept(prepared)
    assert w.s.lookup_request(w.p, 'main', body['request_id']) is None
    port.close()


@pytest.mark.parametrize('dry_run', [True, False])
def test_installed_provider_uses_request_port_without_global_scene_client(bound, monkeypatch, dry_run):
    from astrid.sdk.timeline.commit import create_runtime_commit_service
    from astrid.core.timeline import scene_answers
    w = bound
    # Prove the ordinary scene_answers implementation consumes the provider's
    # explicit request client; no caller installs a private thread-local client.
    assert getattr(scene_answers._local, 'client', None) is None
    w.s._timeline_commit_provider = create_runtime_commit_service()
    body = wire(w.p, dry_run=dry_run)
    before = count(w.s, 'parent_composition_publications')
    result = w.s.commit_timeline(w.p, 'main', body, idempotency_key=body['request_id'], identity=w.identity)
    assert result['status'] in ({'preview'} if dry_run else {'accepted', 'no_change'}), result
    assert w.calls
    assert {v['invocation']['candidate_digest'] for v in w.calls} == {digest(result['canonical_document'])}
    assert getattr(scene_answers._local, 'client', None) is None
    if dry_run:
        assert count(w.s, 'parent_composition_publications') == before
        assert w.s.lookup_request(w.p, 'main', body['request_id']) is None
    else:
        assert w.s.lookup_request(w.p, 'main', body['request_id'])['result'] == result


@pytest.mark.parametrize('failure', ['unknown', 'malformed', 'oversize', 'revoked'])
def test_real_provider_refusals_never_preview_or_accept(bound, monkeypatch, failure):
    from astrid.sdk.timeline.commit import create_runtime_commit_service
    from astrid.core.timeline import scene_answers
    w = bound
    w.s._timeline_commit_provider = create_runtime_commit_service()
    original = w.relay.exchange
    def failed(request, **kw):
        value = original(request, **kw)
        if failure == 'unknown': value[0]['coverage'] = 'UNKNOWN'
        elif failure == 'malformed': value[0]['frame'] = True
        elif failure == 'oversize': value[0]['findings'] = ['x' * (1024 * 1024)]
        elif failure == 'revoked': w.credentials.disable_actor(w.identity['actor'])
        return value
    monkeypatch.setattr(w.relay, 'exchange', failed)
    before = count(w.s, 'parent_composition_publications')
    body = wire(w.p, dry_run=True)
    result = w.s.commit_timeline(w.p, 'main', body, idempotency_key=body['request_id'], identity=w.identity)
    assert result['status'] in {'refused', 'error'}, result
    assert count(w.s, 'parent_composition_publications') == before
    assert w.s.lookup_request(w.p, 'main', body['request_id']) is None
    assert getattr(scene_answers._local, 'client', None) is None


def test_superseded_candidate_cannot_complete_late(bound):
    from astrid.core.execution import authoring_scene_protocol as protocol
    from astrid.core.execution.remotion_frame_owner import FrameOwnerError
    w = bound
    port = w.s._request_commit_port(wire(w.p), w.identity)
    value = projection()
    client = port.scene_evaluator({'candidate': 'old'})
    client.query_scene(revision_digest=protocol.digest(value)[7:], scene=value, frames=[0])
    port.scene_evaluator({'candidate': 'new'})
    with pytest.raises(FrameOwnerError): client.complete()
    port.close()


def test_authority_loss_after_staged_publication_rolls_back_atomic_accept(bound, monkeypatch):
    w = bound
    body = wire(w.p)
    prepared = acceptance(w.s, w.p, request=body)
    port = w.s._request_commit_port(body, w.identity)
    evaluate(w, port, prepared['result']['canonical_document'])
    original = w.s.publish_parent_composition
    def lose_after_staging(*args, **kwargs):
        result = original(*args, **kwargs)
        w.credentials.disable_actor(w.identity['actor'])
        return result
    monkeypatch.setattr(w.s, 'publish_parent_composition', lose_after_staging)
    before = count(w.s, 'parent_composition_publications')
    with pytest.raises(AuthorizationError): port.accept(prepared)
    assert count(w.s, 'parent_composition_publications') == before
    assert w.s.lookup_request(w.p, 'main', body['request_id']) is None
    port.close()


def test_installed_astrid_provider_cannot_silently_omit_scene_port_contract():
    from runtime_protocol.timeline_commit import validate_timeline_commit_provider
    from runtime_protocol.contract_metadata import SCHEMA_DIGEST
    from runtime_protocol.errors import ValidationError
    provider = SimpleNamespace(provider_id='astrid-v1', interface_version=1, contract_digest=SCHEMA_DIGEST,
                               commit=lambda *args: None)
    for marker in (None, False, 1):
        provider.requires_scene_evaluation = marker
        with pytest.raises(ValidationError): validate_timeline_commit_provider(provider)
    provider.requires_scene_evaluation = True
    validate_timeline_commit_provider(provider)


@pytest.mark.parametrize('dry_run', [True, False])
def test_empty_timeline_preserves_existing_shared_completeness_semantics(bound, dry_run):
    from astrid.sdk.timeline.commit import create_runtime_commit_service
    from test_shot_composition_runtime import _publication
    w = bound
    head = w.s.head(w.p, 'main')
    publication = _publication(w.p, expected_head=head['revision_id'], parent_revision_id='empty-scene')
    publication['parent_composition']['occurrences'] = []
    publication['shot_revisions'] = []
    publication['internal_timeline_revisions'] = []
    w.s.publish_parent_composition(w.p, 'main', publication, idempotency_key='empty-scene')
    w.s._timeline_commit_provider = create_runtime_commit_service()
    body = wire(w.p, dry_run=dry_run)
    head = w.s.head(w.p, 'main')
    body.update(base_revision_id=head['revision_id'], base_publication_id=head['publication_id'])
    result = w.s.commit_timeline(w.p, 'main', body, idempotency_key=body['request_id'], identity=w.identity)
    assert result['status'] in ({'preview'} if dry_run else {'accepted', 'no_change'}), result
    assert not w.calls  # zero sampled frames; no manufactured answer
