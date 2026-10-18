"""Isolated metadata-copy transactions; no server or consumer acceptance claim."""
import copy
import json
import time
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor

import pytest

from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import AuthorizationError, ForbiddenError, ConflictError, NotFoundError, ValidationError
from runtime_protocol.paired_session import PairedSessionAuthority
from runtime_protocol.util import canonical_json
from test_shot_composition_runtime import _service
from test_captured_output_media_selection import settled, capture


def snapshot(service):
    return '\n'.join(service.store.conn.iterdump())


@pytest.fixture
def copy_source(tmp_path):
    service, project = _service(tmp_path)
    credentials = CredentialStore(tmp_path / 'test-credentials')
    owner = PairedSessionAuthority()
    service.bind_task_authority(owner, credentials)
    token, _ = credentials.provision('copy-writer', ['projects:read', 'projects:write'])
    identity = {**credentials.require(token, 'projects:write'),
                '_credential_binding': credentials._sha256(token.encode())}
    # Synthetic registered image catalogue only. Supported import/settlement
    # consumer proof is separate; this fixture claims neither decoder nor task.
    with service.store._transaction():
        service.store.conn.execute('INSERT INTO objects VALUES (?,4,?,?,?)',
                                   ('a' * 64, 'image/png', 'picture.png', 'fixture'))
        service.store.conn.execute("INSERT INTO project_objects VALUES (?,?,'managed',?)",
                                   (project, 'a' * 64, 'fixture'))
        service.store.conn.execute("INSERT INTO generations VALUES (?,?,NULL,'image','completed',?,1,?,?)",
            ('source-generation', project, canonical_json({'params': {'width': 16, 'height': 8}}), 'fixture', 'fixture'))
        # The displayed variant is deliberately not primary.
        for variant, primary in [('displayed', False), ('primary', True)]:
            service.store.conn.execute("INSERT INTO generation_variants(id,generation_id,object_id,variant_type,metadata_json,created_at) VALUES (?,?,?,'original',?,?)",
                (variant, 'source-generation', 'a' * 64, canonical_json({'is_primary': primary}), 'fixture'))
    source = service.get_project_media_selection(project, asset='picture', generation_id='source-generation', variant_id='displayed')
    try:
        yield service, project, source, identity, credentials, token
    finally:
        service.close()


def acquire(fixture, *, source=None, key='copy-1', identity=None, **extra):
    s, p, selected, principal, *_ = fixture
    return s.duplicate_project_generation(p, {'source': source or selected, **extra},
        idempotency_key=key, identity=principal if identity is None else identity)


def test_copy_distinct_ids_same_object_immediate_lineage_and_lost_response(copy_source):
    s, p, source, *_ = copy_source
    before = snapshot(s)
    result = acquire(copy_source)
    data = result['data']
    assert data['generation']['generation_id'] != source['generation_id']
    assert data['variant']['variant_id'] != source['variant_id']
    assert data['variant']['generation_id'] == data['generation']['generation_id']
    assert data['variant']['object_id'] == source['object_id'] == data['entry']['object_id']
    assert data['generation']['source_task_id'] is None
    assert data['generation']['metadata']['runtime_metadata_copy']['source'] == source
    assert data['entry'] == {'object_id': source['object_id'], 'media_type': 'image/png',
                             'size': 4, 'filename': 'picture.png', 'width': 16, 'height': 8}
    selected = data['selection']
    assert selected == s.get_project_media_selection(p, asset=selected['asset'],
        generation_id=selected['generation_id'], variant_id=selected['variant_id'])
    assert selected['catalog_digest'] != source['catalog_digest']
    assert snapshot(s) != before
    committed = snapshot(s)
    assert acquire(copy_source) == result
    assert snapshot(s) == committed
    assert s.store.conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0] == 0
    assert s.store.conn.execute("SELECT COUNT(*) FROM command_idempotency WHERE command_kind='generation.duplicate'").fetchone()[0] == 1
    second = acquire(copy_source, source=selected, key='copy-2')['data']
    assert second['generation']['metadata']['runtime_metadata_copy']['source'] == selected


def test_concurrent_retry_one_generation_variant_receipt(copy_source):
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda _: acquire(copy_source), range(12)))
    assert all(value == results[0] for value in results)
    s = copy_source[0]
    assert s.store.conn.execute('SELECT COUNT(*) FROM generations').fetchone()[0] == 2
    assert s.store.conn.execute('SELECT COUNT(*) FROM generation_variants').fetchone()[0] == 3


def test_durable_retry_survives_reopen_and_receipt_pruning_window(copy_source):
    from runtime_protocol.service import RuntimeService
    s, p, source, identity, credentials, _ = copy_source
    # Startup admission checks actual CAS closure. Materialize disposable test
    # bytes rather than reopening the other tests' deliberately synthetic row.
    ingested = s.ingest(p, b'isolated-copy-fixture', media_type='image/png',
        original_name='picture.png', idempotency_key='reopen-object')['data']
    with s.store._transaction():
        s.store.conn.execute('UPDATE generation_variants SET object_id=?', (ingested['object_id'][7:],))
        s.store.conn.execute('DELETE FROM project_objects WHERE digest=?', ('a' * 64,))
        s.store.conn.execute('DELETE FROM objects WHERE digest=?', ('a' * 64,))
    source = s.get_project_media_selection(p, asset=source['asset'],
        generation_id=source['generation_id'], variant_id=source['variant_id'])
    first = acquire(copy_source, source=source)
    with s.store._transaction():
        s.store.conn.execute("UPDATE command_idempotency SET created_at='2000-01-01T00:00:00+00:00' WHERE command_kind='generation.duplicate'")
    # Exercise the existing receipt-pruning boundary with another mutation.
    s.store._last_idempotency_prune = 0
    acquire(copy_source, source=source, key='copy-2')
    root = s.store.root
    s.close()
    reopened = RuntimeService(root)
    try:
        reopened.bind_task_authority(PairedSessionAuthority(), credentials)
        before = snapshot(reopened)
        replay = reopened.duplicate_project_generation(p, {'source': source}, idempotency_key='copy-1', identity=identity)
        assert replay['data'] == first['data']
        assert replay['receipt']['receipt_id'] == first['receipt']['receipt_id']
        assert snapshot(reopened) == before
    finally:
        reopened.close()


@pytest.mark.parametrize('field,value', [
    ('generation_id', 'missing'), ('variant_id', 'primary'), ('object_id', 'sha256:' + 'b' * 64),
    ('catalog_digest', 'sha256:' + '0' * 64), ('asset', ''), ('object_id', 'url'), ('catalog_digest', None),
])
def test_invalid_source_is_whole_operation_no_effect(copy_source, field, value):
    s, _, selected, *_ = copy_source
    selected = {**selected, field: value}
    before = snapshot(s)
    with pytest.raises((ValidationError, ConflictError, NotFoundError)):
        acquire(copy_source, source=selected)
    assert snapshot(s) == before


@pytest.mark.parametrize('field', ['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'])
def test_missing_selector(copy_source, field):
    s, _, selected, *_ = copy_source
    selected = dict(selected)
    del selected[field]
    before = snapshot(s)
    with pytest.raises(ValidationError):
        acquire(copy_source, source=selected)
    assert snapshot(s) == before


@pytest.mark.parametrize('extra', [
    {'generation_id': 'chosen'}, {'variant_id': 'chosen'}, {'url': 'https://invalid'},
    {'source_task_id': 'task'}, {'metadata': {'runtime_metadata_copy': {}}}, {'object_id': 'replacement'},
])
def test_caller_destination_and_provenance_refused(copy_source, extra):
    before = snapshot(copy_source[0])
    with pytest.raises(ValidationError):
        acquire(copy_source, **extra)
    assert snapshot(copy_source[0]) == before


@pytest.mark.parametrize('sql', [
    "UPDATE generations SET status='failed'",
    "UPDATE generation_variants SET object_id=NULL WHERE id='displayed'",
    "DELETE FROM project_objects",
    "UPDATE objects SET size=5",
    "UPDATE generations SET metadata_json='{\"params\":{\"width\":-1}}'",
    "UPDATE generation_variants SET metadata_json='{\"runtime_managed_output_association_id\":\"forged\"}' WHERE id='displayed'",
    "UPDATE generations SET metadata_json='{\"runtime_metadata_copy\":{}}'",
])
def test_stale_or_forged_catalogue_no_effect(copy_source, sql):
    s = copy_source[0]
    with s.store._transaction():
        s.store.conn.execute(sql)
    before = snapshot(s)
    with pytest.raises((ValidationError, ConflictError, NotFoundError)):
        acquire(copy_source)
    assert snapshot(s) == before


def test_injected_failure_rolls_back_generation_variant_and_receipt(copy_source, monkeypatch):
    s = copy_source[0]
    before = snapshot(s)
    original = s._command_record
    def fail(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError('injected after receipt')
    monkeypatch.setattr(s, '_command_record', fail)
    with pytest.raises(RuntimeError, match='injected'):
        acquire(copy_source)
    assert snapshot(s) == before


def test_changed_body_conflict_and_direct_create_refusals(copy_source):
    s, p, source, *_ = copy_source
    acquire(copy_source)
    before = snapshot(s)
    with pytest.raises(ConflictError):
        acquire(copy_source, source={**source, 'asset': 'changed'})
    for call in (lambda: s.create_generation(p, {}, idempotency_key='direct'),
                 lambda: s.create_variant(source['generation_id'], {}, idempotency_key='direct')):
        with pytest.raises(ConflictError, match='direct'):
            call()
    assert snapshot(s) == before


@pytest.mark.parametrize('mode', ['read', 'disabled', 'rotated', 'expired', 'forged-binding'])
def test_authentication_before_catalogue_lookup_or_replay(copy_source, mode, monkeypatch):
    s, _, _, identity, credentials, token = copy_source
    acquire(copy_source)
    identity = dict(identity)
    if mode == 'read':
        identity['scopes'] = ['projects:read']
    elif mode == 'disabled':
        credentials.disable_actor(identity['actor'])
    elif mode == 'rotated':
        credentials.provision(identity['actor'], ['projects:write'], rotate=True)
    elif mode == 'expired':
        identity['expires_at'] = time.time() - 1
    else:
        identity['_credential_binding'] = 'wrong'
    before = snapshot(s)
    def lookup(*args):
        pytest.fail('lookup before authorization')
    monkeypatch.setattr(s.store, 'get_project', lookup)
    with pytest.raises((AuthorizationError, ForbiddenError)):
        acquire(copy_source, identity=identity)
    assert snapshot(s) == before


def paired_identity(fixture):
    s, p, _, _, credentials, _ = fixture
    s.select_project('paired-copy', p)
    token, _ = credentials.provision_connector('paired-copy', ['handshake', 'projects:read', 'projects:write'],
        connector_id='test-connector', realm_id=s.realm['id'], expires_at=time.time() + 120)
    identity = {**credentials.require(token, 'projects:write'), '_credential_binding': credentials._sha256(token.encode())}
    context = dict(pair_id='copy-session', connector_id='test-connector', generation=1,
        realm_id=s.realm['id'], expires_at=int((time.time() + 90) * 1000))
    owner = s._task_authority_owner
    grant = owner.authenticate(identity, json.dumps(context), s)
    return {**identity, '_paired_session': grant}, context, token


def test_actual_paired_grant_allows_only_bound_project_copy(copy_source):
    identity, _, _ = paired_identity(copy_source)
    result = acquire(copy_source, identity=identity)
    assert acquire(copy_source, identity=identity) == result
    assert result['receipt']['command_kind'] == 'generation.duplicate'


@pytest.mark.parametrize('mode', ['project', 'realm', 'actor', 'binding', 'session', 'expired', 'revoked', 'operation', 'read'])
def test_paired_authority_rechecked_before_replay_and_lookup(copy_source, mode, monkeypatch):
    s, p, source, *_ = copy_source
    identity, _, _ = paired_identity(copy_source)
    acquire(copy_source, identity=identity)
    identity = dict(identity)
    grant, owner = identity['_paired_session'], s._task_authority_owner
    project = p
    if mode == 'project':
        project = 'another-project'
    elif mode == 'realm':
        identity['_paired_session'] = replace(grant, realm_id='another-realm')
    elif mode == 'actor':
        identity['actor'] = 'another-actor'
    elif mode == 'binding':
        identity['_credential_binding'] = 'another-binding'
    elif mode == 'session':
        identity['_paired_session'] = replace(grant, pair_id='another-session')
    elif mode == 'expired':
        owner.clock = lambda: time.time() + 600
    elif mode == 'revoked':
        owner.revoke(grant)
    elif mode == 'read':
        identity['scopes'] = ['projects:read']
    else:
        # Model an already-issued old timeline-only grant. The new closed
        # operation declaration must not expand the immutable old handle.
        handle = grant.authority.issue(dict(realm=grant.realm_id, browser_session=grant.pair_id,
            projects=[p], operations=['timeline.update'], expiry=grant.expiry))
        old = replace(grant, handle=handle)
        owner._sessions[grant.pair_id] = old
        identity['_paired_session'] = old
    before = snapshot(s)
    monkeypatch.setattr(s.store, 'get_project', lambda *_: pytest.fail('lookup before exact grant decision'))
    with pytest.raises((AuthorizationError, ForbiddenError)):
        s.duplicate_project_generation(project, {'source': source}, idempotency_key='copy-1', identity=identity)
    assert snapshot(s) == before


@pytest.mark.parametrize('mutation', [None, 'unavailable', 'version', 'attempt', 'forged-owner'])
def test_settled_lineage_retains_original_owner_and_lifecycle(settled, tmp_path, mutation):
    s, p, associations, *_ = settled
    credentials = CredentialStore(tmp_path / 'lineage-test-credentials')
    owner = PairedSessionAuthority()
    s.bind_task_authority(owner, credentials)
    token, _ = credentials.provision('lineage-writer', ['projects:write'])
    identity = {**credentials.require(token, 'projects:write'), '_credential_binding': credentials._sha256(token.encode())}
    source = capture(s, p, associations['second'])
    acquired = s.duplicate_project_generation(p, {'source': source}, idempotency_key='lineage-copy', identity=identity)['data']
    assert 'runtime_managed_output_association_id' not in acquired['variant']['metadata']
    with s.store._mutex:
        record = s._selected_project_media(p, acquired['selection'])
    original = record['variant']['copy_source']
    assert original['variant']['managed_output']['association_id'] == associations['second']['association_id']
    assert original['generation_id'] == source['generation_id']
    assert acquired['generation']['source_task_id'] is None
    if mutation is None:
        return
    association = associations['second']['association_id']
    with s.store._transaction():
        if mutation == 'unavailable':
            s.store.conn.execute("UPDATE managed_output_lifecycle SET state='reclaimed' WHERE association_id=?", (association,))
        elif mutation == 'version':
            s.store.conn.execute('UPDATE managed_output_lifecycle SET version=version+1 WHERE association_id=?', (association,))
        elif mutation == 'attempt':
            s.store.conn.execute('UPDATE attempts SET settled=0')
        else:
            s.store.conn.execute('UPDATE generation_variants SET metadata_json=json_set(metadata_json, ?, ?) WHERE id=?',
                ('$.runtime_managed_output_association_id', association, acquired['variant']['variant_id']))
    before = snapshot(s)
    with pytest.raises((ValidationError, ConflictError, NotFoundError)):
        s.duplicate_project_generation(p, {'source': acquired['selection']}, idempotency_key='next-copy', identity=identity)
    assert snapshot(s) == before


def test_generated_python_client_actual_handler_and_paired_auth_without_socket(copy_source):
    import io
    from email.message import Message
    from types import SimpleNamespace
    from runtime_protocol.server import RuntimeHandler
    from banodoco_workspace_client.generated import WorkspaceClient
    s, p, source, _, credentials, _ = copy_source
    identity, context, token = paired_identity(copy_source)
    # Tokens are generated only by this private fixture, never inspected from a
    # real Runtime. The handler authenticates the actual test credential.
    wire = []
    def transport(method, path, headers, body):
        request = RuntimeHandler.__new__(RuntimeHandler)
        request.command, request.path = method, path
        request.headers = Message()
        for key, value in {**headers, 'Content-Length': str(len(body or b'')),
                           'X-Reigh-Paired-Session': json.dumps(context)}.items():
            request.headers[key] = value
        request.rfile = io.BytesIO(body or b'')
        request.server = SimpleNamespace(runtime=s, credentials=credentials, paired_sessions=s._task_authority_owner)
        request._send = lambda status, payload, **_: (status, {}, json.dumps(payload).encode())
        wire.append((method, path, headers['Idempotency-Key'], body))
        return request._route()
    client = WorkspaceClient('http://in-memory.invalid', token, transport=transport)
    first = client.duplicate_project_generation(p, source, idempotency_key='generated-copy')
    assert client.duplicate_project_generation(p, source, idempotency_key='generated-copy') == first
    assert wire[0] == wire[1]
    assert first['selection']['object_id'] == source['object_id']
    assert first.receipt['command_kind'] == 'generation.duplicate'


def test_duplicate_request_result_and_lineage_follow_owning_closed_schema(copy_source):
    from pathlib import Path
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    root = Path(__file__).parents[1] / 'contract/schemas'
    generation, selection = [json.loads((root / name).read_text()) for name in ('generation.json', 'project-media-selection.json')]
    registry = Registry().with_resources([(value['$id'], Resource.from_contents(value)) for value in (generation, selection)])
    def validate(name, value):
        Draft202012Validator({'$ref': generation['$id'] + '#/definitions/' + name}, registry=registry).validate(value)
    result = acquire(copy_source)['data']
    validate('DuplicateRequest', {'source': copy_source[2]})
    validate('DuplicateResult', result)
    validate('CopyLineage', result['generation']['metadata']['runtime_metadata_copy'])
    for extra in ('generation_id', 'variant_id', 'url', 'source_task_id', 'metadata'):
        with pytest.raises(Exception) as failure:
            validate('DuplicateRequest', {'source': copy_source[2], extra: 'caller'})
        assert failure.type.__module__.startswith('jsonschema')
