"""Public paired inspect admission is read-only and exact-route bounded."""
import time
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from types import SimpleNamespace

import pytest

from test_paired_session_grants import call, code
from test_selected_media_commit import snapshot
from test_timeline_accept import fixture, http_server


@pytest.fixture
def inspector(fixture, tmp_path, monkeypatch):
    service, project = fixture
    other = service.create_project({'slug': 'outside', 'name': 'Outside'}, idempotency_key='outside')['id']
    server, thread, api = http_server(service, tmp_path)
    service.select_project('reader', project)
    token, _ = server.credentials.provision_connector('reader', ['handshake', 'projects:read'],
        connector_id='connector', realm_id=service.realm['id'], expires_at=time.time()+1000)
    context = dict(pair_id='inspection', connector_id='connector', realm_id=service.realm['id'],
                   generation=1, expires_at=int((time.time()+600)*1000))
    endpoint = SimpleNamespace(endpoint=api.endpoint)
    assert call(endpoint, token, context=context)[0] == 200
    calls = []
    inspect = service.inspect_timeline
    def observed(*args, **kwargs):
        calls.append(args)
        return inspect(*args, **kwargs)
    monkeypatch.setattr(service, 'inspect_timeline', observed)
    def forbidden(*args, **kwargs):
        raise AssertionError('inspect opened content or entered a write provider')
    monkeypatch.setattr(service, 'create_timeline_view', forbidden)
    monkeypatch.setattr(service.cas, 'open', forbidden)
    try:
        yield service, server, endpoint, token, context, project, other, calls
    finally:
        server.shutdown(); server.server_close(); thread.join()


def test_paired_inspect_reads_exact_immutable_head_without_persistence(inspector):
    service, server, endpoint, token, context, project, other, calls = inspector
    before, changes = snapshot(service), service.store.conn.total_changes
    status, result = call(endpoint, token, f'/v1/projects/{project}/timelines/main/inspect', context=context, body={})
    assert status == 200, result
    assert (result['project_id'], result['timeline_id'], result['revision_id'], result['head_revision_id']) == (project, 'main', 'parent-1', 'parent-1')
    assert result['source_pixels'] == result['waveforms'] == 'not_requested'
    assert len(calls) == 1
    assert snapshot(service) == before and service.store.conn.total_changes == changes


@pytest.mark.parametrize('denial', ['project', 'scope', 'context', 'actor', 'connector', 'realm', 'expiry', 'revocation', 'generation', 'credential-expiry'])
def test_inspect_denied_before_content_or_provider(inspector, denial):
    service, server, endpoint, token, context, project, other, calls = inspector
    expected = None
    if denial == 'project': project, expected = other, 'project_grant_project_denied'
    elif denial == 'scope':
        metadata = server.credentials.actor_metadata('reader'); metadata['scopes'] = ['handshake']
        server.credentials._publish('reader', token, metadata)
    elif denial == 'context': context, expected = None, 'paired_session_required'
    elif denial == 'actor':
        service.select_project('other-reader', project)
        token, _ = server.credentials.provision_connector('other-reader', ['projects:read'], connector_id='connector', realm_id=service.realm['id'], expires_at=time.time()+1000)
        expected = 'project_grant_actor_mismatch'
    elif denial in ('connector', 'realm'):
        context = {**context, denial+'_id': 'foreign'}; expected = 'paired_'+denial+'_mismatch'
    elif denial == 'expiry':
        server.paired_sessions.clock = lambda: time.time()+301; expected = 'project_grant_expired'
    elif denial == 'revocation':
        server.paired_sessions.revoke(server.paired_sessions._sessions['inspection']); expected = 'project_grant_revoked'
    elif denial == 'generation':
        fresh = {**context, 'pair_id': 'new-generation', 'generation': 2}
        assert call(endpoint, token, context=fresh)[0] == 200
        expected = 'paired_generation_stale'
    elif denial == 'credential-expiry':
        metadata = server.credentials.actor_metadata('reader'); metadata['expires_at'] = time.time()-1
        server.credentials._publish('reader', token, metadata); expected = 'paired_credential_expired'
    before, changes = snapshot(service), service.store.conn.total_changes
    result = call(endpoint, token, f'/v1/projects/{project}/timelines/main/inspect', context=context, body={})
    assert result[0] in (401, 403), result
    if expected: assert code(result) == expected
    assert calls == []
    assert snapshot(service) == before and service.store.conn.total_changes == changes


@pytest.mark.parametrize('method,suffix', [('POST', 'views'), ('PATCH', 'inspect'), ('PUT', 'inspect'), ('DELETE', 'inspect'), ('GET', 'inspect'), ('HEAD', 'inspect'), ('POST', 'inspect/extra'), ('POST', 'inspect%2Fextra'), ('POST', 'inspect-more')])
def test_inspect_exception_does_not_admit_neighbors(inspector, method, suffix):
    service, server, endpoint, token, context, project, other, calls = inspector
    before, changes = snapshot(service), service.store.conn.total_changes
    if method == 'HEAD':
        request = Request(endpoint.endpoint+f'/v1/projects/{project}/timelines/main/{suffix}', method='HEAD',
            headers={'Authorization': 'Bearer '+token, 'X-Reigh-Paired-Session': json.dumps(context)})
        with pytest.raises(HTTPError) as error:
            urlopen(request, timeout=5)
        assert error.value.code == 404
    else:
        result = call(endpoint, token, f'/v1/projects/{project}/timelines/main/{suffix}', context=context, body={}, method=method)
        assert result[0] in (400, 403, 404, 405), result
    assert calls == []
    assert snapshot(service) == before and service.store.conn.total_changes == changes


def test_inspect_still_validates_options(inspector):
    service, server, endpoint, token, context, project, other, calls = inspector
    before = snapshot(service)
    status, result = call(endpoint, token, f'/v1/projects/{project}/timelines/main/inspect', context=context, body={'unexpected': True})
    assert status == 422, result
    assert snapshot(service) == before
