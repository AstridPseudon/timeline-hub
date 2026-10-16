"""Authenticated selection reads on disposable synthetic managed media only."""
import json
from pathlib import Path
import threading
import time
from urllib.parse import urlencode

import pytest
from jsonschema import Draft202012Validator
import yaml

from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import ConflictError, NotFoundError
from runtime_protocol.server import RuntimeHTTPServer, RuntimeHandler
from runtime_protocol.timeline_commit import digest
from packages.python.banodoco_workspace_client.generated import WorkspaceClient
from http_helpers import Api
from test_timeline_accept import fixture, IDENTITY
from test_selected_media_commit import media, mutate, snapshot, request_for, prepare

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'contract/schemas/project-media-selection.json').read_text())
SELECTORS = dict(asset='sound-1', generation_id='g1', variant_id='v1')


@pytest.fixture
def http(fixture, tmp_path):
    service, project = fixture
    selected = media(service, project)
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('reader', ['projects:read'])
    server = RuntimeHTTPServer(('127.0.0.1', 0), RuntimeHandler)
    server.runtime, server.credentials = service, credentials
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=0.01), daemon=True)
    thread.start()
    try:
        yield service, project, selected, server, token
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        assert not thread.is_alive()


def path(project, **selectors):
    return f'/v1/projects/{project}/media-selection?' + urlencode(selectors or SELECTORS)


def api(server, token):
    return Api(f'http://127.0.0.1:{server.server_port}', token)


def test_exact_five_fields_c006_digest_and_no_database_writes(http):
    service, project, expected, server, token = http
    before = snapshot(service)
    changes = service.store.conn.total_changes
    statements = []
    service.store.conn.set_trace_callback(statements.append)
    try:
        result = api(server, token).request('GET', path(project))
    finally:
        service.store.conn.set_trace_callback(None)
    assert result == expected
    assert set(result) == set(SCHEMA['required'])
    Draft202012Validator(SCHEMA).validate(result)
    request = request_for(project, result)
    record = service._request_commit_port(request, IDENTITY).selected_media(result)
    assert result['catalog_digest'] == digest({k: v for k, v in record.items() if k != 'catalog_digest'})
    assert snapshot(service) == before
    assert service.store.conn.total_changes == changes
    assert all(sql.lstrip().split()[0].upper() == 'SELECT' for sql in statements)


def test_url_encoding_asset_preservation_and_all_three_fields_bound(http):
    service, project, _, server, token = http
    asset = '  owner/音 + &?#=% key  '
    # Encoded selectors are decoded once, never interpreted as identity URLs.
    media(service, project, generation='g /音+&', variant='v ?#+%')
    result = api(server, token).request('GET', path(project, asset=asset, generation_id='g /音+&', variant_id='v ?#+%'))
    assert result['asset'] == asset
    assert result['generation_id'] == 'g /音+&'
    assert result['variant_id'] == 'v ?#+%'
    first = api(server, token).request('GET', path(project))
    renamed = api(server, token).request('GET', path(project, **{**SELECTORS, 'asset': asset}))
    same_object = api(server, token).request('GET', path(project, asset='sound-1', generation_id='g /音+&', variant_id='v ?#+%'))
    assert first['object_id'] == renamed['object_id'] == same_object['object_id']
    assert len({first['catalog_digest'], renamed['catalog_digest'], same_object['catalog_digest']}) == 3


@pytest.mark.parametrize('query', [
    '', 'asset=x', 'asset=x&generation_id=g1', 'asset=x&variant_id=v1',
    'generation_id=g1&variant_id=v1',
    *[urlencode({**SELECTORS, key: ''}) for key in SELECTORS],
    *[urlencode({**SELECTORS, key: ' \t\n'}) for key in SELECTORS],
    *[urlencode(SELECTORS) + '&' + key + '=' + value for key, value in SELECTORS.items()],
    *[urlencode(SELECTORS) + '&' + key + '=forbidden' for key in (
        'object_id', 'catalog_digest', 'url', 'path', 'cas', 'catalog', 'realm_id', 'project_id',
    )],
    'asset=%ZZ&generation_id=g1&variant_id=v1',
    'asset=%FF&generation_id=g1&variant_id=v1',
    'asset=%&generation_id=g1&variant_id=v1',
    'asset=x&generation_id=g1&variant_id=v1&flag',
    'asset=x&generation_id=g1&variant_id=v1&&',
    'asset=x&generation_id=g1&variant_id=v1&%61sset=x',
])
def test_malformed_duplicate_unknown_selectors_refused_without_writes(http, query):
    service, project, _, server, token = http
    before = snapshot(service)
    with pytest.raises(RuntimeError) as exc:
        api(server, token).request('GET', f'/v1/projects/{project}/media-selection?' + query)
    assert exc.value.status == 400
    assert snapshot(service) == before


@pytest.mark.parametrize('scope', [None, 'objects:read', 'projects:write', 'worker:execute'])
def test_existing_credential_read_scope_required(http, scope):
    service, project, _, server, _ = http
    token = None if scope is None else server.credentials.provision('wrong-scope', [scope])[0]
    before = snapshot(service)
    with pytest.raises(RuntimeError) as exc:
        api(server, token).request('GET', path(project))
    assert exc.value.status == 401
    assert snapshot(service) == before


@pytest.mark.parametrize('selectors', [
    {**SELECTORS, 'generation_id': 'missing'}, {**SELECTORS, 'variant_id': 'missing'},
    {**SELECTORS, 'generation_id': 'g2'}, {**SELECTORS, 'variant_id': 'v2'},
])
def test_missing_or_mismatched_generation_variant(http, selectors):
    service, project, _, server, token = http
    media(service, project, generation='g2', variant='v2')
    before = snapshot(service)
    with pytest.raises(RuntimeError) as exc:
        api(server, token).request('GET', path(project, **selectors))
    assert exc.value.status == 404
    assert snapshot(service) == before


@pytest.mark.parametrize('sql,status', [
    ("UPDATE generation_variants SET object_id=NULL WHERE id='v1'", 404),
    ("DELETE FROM project_objects", 404),
    ("UPDATE project_objects SET relation='external'", 404),
    ("UPDATE generations SET status='created'", 409),
    ("UPDATE generations SET status='running'", 409),
    ("UPDATE generations SET status='failed'", 409),
    ("UPDATE generations SET metadata_json='[]'", 422),
    ("UPDATE generation_variants SET metadata_json='not-json'", 422),
    ("UPDATE generation_variants SET metadata_json='{\"duration_seconds\":-1}'", 422),
    ("UPDATE objects SET size=0", 422),
    ("UPDATE objects SET original_name='/private/media.wav'", 422),
])
def test_incomplete_unmanaged_uncompleted_invalid_candidates(http, sql, status):
    service, project, _, server, token = http
    mutate(service, sql)
    before = snapshot(service)
    with pytest.raises(RuntimeError) as exc:
        api(server, token).request('GET', path(project))
    assert exc.value.status == status
    assert snapshot(service) == before


def test_project_and_realm_membership_refuse(http, monkeypatch):
    service, project, _, server, token = http
    other = service.create_project({'slug': 'other', 'name': 'Other'}, idempotency_key='other')['id']
    media(service, other, generation='other-g', variant='other-v')
    before = snapshot(service)
    for request in (path(other), path(project, asset='sound-1', generation_id='other-g', variant_id='other-v')):
        with pytest.raises(RuntimeError) as exc:
            api(server, token).request('GET', request)
        assert exc.value.status == 404
    monkeypatch.setattr(service, 'realm', {**service.realm, 'id': 'foreign-realm'})
    with pytest.raises(RuntimeError) as exc:
        api(server, token).request('GET', path(project))
    assert exc.value.status == 401
    assert snapshot(service) == before


@pytest.fixture
def paired_selection(http):
    """Requires the runner's explicit Astrid installation/source binding.

    The standalone Runtime distribution does not install Astrid. Do not discover
    sibling checkouts or replace the real policy authority with an allow stub.
    A missing authority is a setup failure, never a passing negative control.
    """
    from astrid.core.execution.provider_route_grant import ProjectGrantAuthority

    service, project, _, server, _ = http
    other = service.create_project({'slug': 'other', 'name': 'Other'}, idempotency_key='other')['id']
    media(service, other, generation='other-g', variant='other-v')
    service.select_project('connector-reader', project)
    token, _ = server.credentials.provision_connector('connector-reader', ['projects:read'],
        connector_id='connector', realm_id=service.realm['id'], expires_at=time.time() + 1200)
    context = dict(pair_id='selection-session', connector_id='connector', realm_id=service.realm['id'],
                   generation=1, expires_at=int((time.time() + 600) * 1000))
    headers = {'X-Reigh-Paired-Session': json.dumps(context)}
    caller = api(server, token)
    return service, project, other, server, token, context, headers, caller, ProjectGrantAuthority


def test_real_paired_grant_project_realm_and_expiry_binding(paired_selection):
    service, project, other, server, _, context, headers, caller, authority_type = paired_selection
    before = snapshot(service)
    changes = service.store.conn.total_changes
    assert caller.request('GET', path(project), headers=headers)['variant_id'] == 'v1'
    grant = server.paired_sessions._sessions[context['pair_id']]
    assert type(grant.authority) is authority_type
    assert (grant.actor, grant.connector_id, grant.realm_id, grant.project_id, grant.generation) == (
        'connector-reader', 'connector', service.realm['id'], project, 1)
    assert time.time() < grant.expiry <= min(
        context['expires_at'] / 1000, server.credentials.actor_metadata(grant.actor)['expires_at'])
    assert grant.authority.decide(
        grant.handle, realm=grant.realm_id, browser_session=grant.pair_id,
        actor_id=grant.actor, project_id=project,
        operation='rendering.render')['code'] == 'project_grant_allowed'
    for request, header, expected in [
        (path(other, asset='x', generation_id='other-g', variant_id='other-v'), headers,
         'project_grant_project_denied'),
        (path(project), {}, 'paired_session_required'),
        (path(project), {'X-Reigh-Paired-Session': json.dumps({**context, 'realm_id': 'foreign'})},
         'paired_realm_mismatch'),
        (path(project), {'X-Reigh-Paired-Session': json.dumps({**context, 'expires_at': 1})},
         'paired_session_expired'),
    ]:
        with pytest.raises(RuntimeError) as exc:
            caller.request('GET', request, headers=header)
        assert exc.value.status == 403
        assert exc.value.detail['details']['decision'] == {
            'status': 'deny', 'allowed': False, 'code': expected}
    assert snapshot(service) == before
    assert service.store.conn.total_changes == changes


@pytest.mark.parametrize('mutation,expected,status', [
    ('actor', 'project_grant_actor_mismatch', 403),
    ('connector', 'paired_connector_mismatch', 403),
    ('grant-expired', 'project_grant_expired', 403),
    ('credential-expired', 'paired_credential_expired', 401),
    ('revoked', 'project_grant_revoked', 403),
    ('ordinary-credential', 'paired_connector_assertion_required', 403),
    ('credential-binding', 'paired_credential_mismatch', 403),
    ('session-binding', 'paired_session_binding_changed', 403),
])
def test_real_paired_selection_named_denials_before_resolution(
        paired_selection, monkeypatch, mutation, expected, status):
    service, project, _, server, token, context, headers, caller, _ = paired_selection
    assert caller.request('GET', path(project), headers=headers)['variant_id'] == 'v1'
    authority = server.paired_sessions
    grant = authority._sessions[context['pair_id']]
    if mutation == 'actor':
        other_token, _ = server.credentials.provision_connector(
            'other-reader', ['projects:read'], connector_id='connector',
            realm_id=service.realm['id'], expires_at=time.time() + 1200)
        service.select_project('other-reader', project)
        caller = api(server, other_token)
    elif mutation == 'connector':
        headers = {'X-Reigh-Paired-Session': json.dumps({**context, 'connector_id': 'foreign'})}
    elif mutation == 'grant-expired':
        monkeypatch.setattr(authority, 'clock', lambda: grant.expiry)
    elif mutation == 'credential-expired':
        metadata = server.credentials.actor_metadata(grant.actor)
        server.credentials._publish(grant.actor, token, {**metadata, 'expires_at': time.time() - 1})
    elif mutation == 'revoked':
        authority.revoke(grant)
    elif mutation == 'ordinary-credential':
        ordinary, _ = server.credentials.provision('ordinary-reader', ['projects:read'])
        caller = api(server, ordinary)
    elif mutation == 'credential-binding':
        replacement, _ = server.credentials.provision_connector(
            grant.actor, ['projects:read'], connector_id=grant.connector_id,
            realm_id=grant.realm_id, expires_at=time.time() + 1200, rotate=True)
        caller = api(server, replacement)
    elif mutation == 'session-binding':
        headers = {'X-Reigh-Paired-Session': json.dumps(
            {**context, 'expires_at': context['expires_at'] - 1000})}
    before = snapshot(service)
    changes = service.store.conn.total_changes
    def forbidden_resolution(*args, **kwargs):
        pytest.fail('denied paired request reached media resolution')
    monkeypatch.setattr(service, 'get_project_media_selection', forbidden_resolution)
    with pytest.raises(RuntimeError) as exc:
        caller.request('GET', path(project), headers=headers)
    assert exc.value.status == status
    assert exc.value.detail['details']['decision'] == {
        'status': 'deny', 'allowed': False, 'code': expected}
    assert snapshot(service) == before
    assert service.store.conn.total_changes == changes


def test_real_paired_selection_missing_authority_stays_setup_denial(paired_selection, monkeypatch):
    import builtins

    service, project, _, server, _, context, headers, caller, _ = paired_selection
    assert caller.request('GET', path(project), headers=headers)['variant_id'] == 'v1'
    original_import = builtins.__import__
    def unavailable(name, *args, **kwargs):
        if name == 'astrid.core.execution.provider_route_grant':
            raise ImportError('synthetic unavailable authority')
        return original_import(name, *args, **kwargs)
    monkeypatch.setattr(builtins, '__import__', unavailable)
    before = snapshot(service)
    changes = service.store.conn.total_changes
    sessions = dict(server.paired_sessions._sessions)
    with pytest.raises(RuntimeError) as exc:
        caller.request('GET', path(project), headers={
            'X-Reigh-Paired-Session': json.dumps({**context, 'pair_id': 'fresh-pair'})})
    assert exc.value.status == 403
    assert exc.value.detail['details']['decision'] == {
        'status': 'deny', 'allowed': False, 'code': 'paired_grant_authority_unavailable'}
    assert server.paired_sessions._sessions == sessions
    assert snapshot(service) == before
    assert service.store.conn.total_changes == changes


@pytest.mark.parametrize('mutation,args', [
    ("UPDATE generations SET metadata_json=? WHERE id='g1'", ('{"params":{"duration_seconds":2}}',)),
    ("UPDATE generation_variants SET metadata_json=? WHERE id='v1'", ('{"authoring":{"changed":true}}',)),
    ("UPDATE generation_variants SET object_id=? WHERE id='v1'", ('b' * 64,)),
])
def test_later_selected_change_changes_read_digest_and_atomic_accept_refuses(fixture, mutation, args):
    service, project = fixture
    media(service, project)
    media(service, project, generation='g2', variant='v2', object_digest='b' * 64)
    selected = service.get_project_media_selection(project, **SELECTORS)
    request = request_for(project, selected)
    port = service._request_commit_port(request, IDENTITY)
    captured = port.selected_media(selected)
    prepared = prepare(service, project, request)
    mutate(service, mutation, args)
    current = service.get_project_media_selection(project, **SELECTORS)
    assert current['catalog_digest'] != selected['catalog_digest']
    assert port.selected_media(selected) == captured
    before = snapshot(service)
    with pytest.raises((ConflictError, NotFoundError)):
        port.accept(prepared)
    assert snapshot(service) == before


def test_primary_ui_and_unrelated_rows_do_not_change_selection(http):
    service, project, expected, server, token = http
    media(service, project, generation='g2', variant='v2', object_digest='b' * 64)
    mutate(service, "UPDATE generation_variants SET metadata_json='{\"is_primary\":true}' WHERE id='v2'")
    mutate(service, "UPDATE generation_variants SET viewed_at='now' WHERE id='v1'")
    assert api(server, token).request('GET', path(project)) == expected


def test_generated_python_client_actual_http_and_encoded_transport(http):
    _, project, expected, server, token = http
    client = WorkspaceClient(f'http://127.0.0.1:{server.server_port}', token)
    assert client.get_project_media_selection(project, **SELECTORS) == expected
    calls = []
    def transport(method, request_path, headers, body):
        calls.append((method, request_path, headers, body))
        return 200, {}, json.dumps(expected).encode()
    client = WorkspaceClient('http://unused', token, transport=transport)
    client.get_project_media_selection('p/ +', asset='音/&+?% ', generation_id='g/ +', variant_id='v?#')
    from urllib.parse import parse_qs, urlsplit
    assert calls[0][0] == 'GET' and calls[0][3] is None
    assert urlsplit(calls[0][1]).path == '/v1/projects/p%2F%20%2B/media-selection'
    assert parse_qs(urlsplit(calls[0][1]).query) == dict(asset=['音/&+?% '], generation_id=['g/ +'], variant_id=['v?#'])
    assert calls[0][2]['Authorization'] == 'Bearer ' + token


def test_canonical_schema_and_operation_are_exact():
    Draft202012Validator.check_schema(SCHEMA)
    contract = yaml.safe_load((ROOT / 'contract/openapi/workspace-v1.yaml').read_text())
    route = contract['paths']['/v1/projects/{project_id}/media-selection']['get']
    assert route['operationId'] == 'getProjectMediaSelection'
    assert route['x-required-scopes'] == ['projects:read']
    assert {p['name'] for p in route['parameters'] if p.get('in') == 'query'} == set(SELECTORS)
    assert route['responses']['200']['content']['application/json']['schema']['$ref'] == './schemas/project-media-selection.json'
    assert SCHEMA['additionalProperties'] is False
    assert set(SCHEMA['required']) == {*SELECTORS, 'object_id', 'catalog_digest'}
