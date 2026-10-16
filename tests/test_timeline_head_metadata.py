"""Public head observation from disposable project timelines; no acceptance claim."""
import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
import yaml

from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import NotFoundError
from runtime_protocol.server import RuntimeHTTPServer, RuntimeHandler
from test_shot_composition_runtime import _service, _publication
from test_timeline_accept import acceptance, IDENTITY

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('head_revision_id', 'head_publication_id', 'head_updated_at')
SCHEMA = json.loads((ROOT / 'contract/schemas/timeline.json').read_text())


@pytest.fixture
def timeline(tmp_path):
    service, project = _service(tmp_path)
    try:
        yield service, project
    finally:
        service.close()


def observed(resource):
    Draft202012Validator(SCHEMA).validate(resource)
    return tuple(resource[key] for key in FIELDS)


def test_headless_timeline_returns_three_nulls_including_empty_head_row(timeline):
    service, project = timeline
    assert observed(service.get_project_timeline(project, 'main')) == (None, None, None)
    # The canonical store permits an initialized row with no revision. Its row
    # timestamp is not a committed head timestamp.
    service.store.conn.execute('INSERT INTO parent_composition_heads(project_id,timeline_id,revision_id,publication_id,updated_at) VALUES (?,?,NULL,NULL,?)', (project, 'main', 'empty-row-timestamp'))
    assert observed(service.get_project_timeline(project, 'main')) == (None, None, None)


def test_same_row_publication_time_and_next_poll_without_revision_change(timeline, monkeypatch):
    service, project = timeline
    monkeypatch.setattr(service, 'inspect_timeline', lambda *a, **k: pytest.fail('metadata must not inspect'))
    first = service.publish_parent_composition(project, 'main', _publication(project), idempotency_key='initial')
    statements = []
    service.store.conn.set_trace_callback(statements.append)
    try:
        resource = service.get_project_timeline(project, 'main')
    finally:
        service.store.conn.set_trace_callback(None)
    head_queries = [query for query in statements if 'FROM parent_composition_heads' in query]
    assert len(head_queries) == 1
    head = service.head(project, 'main')
    assert observed(resource) == (head['revision_id'], head['publication_id'], head['updated_at'])
    assert resource['head_publication_id'] == first['receipt']['receipt_id']
    service.publish_parent_composition(project, 'main', _publication(project, expected_head='parent-1'), idempotency_key='republish-same-revision')
    latest = service.get_project_timeline(project, 'main')
    actual = service.head(project, 'main')
    assert observed(latest) == (actual['revision_id'], actual['publication_id'], actual['updated_at'])
    assert latest['head_revision_id'] == resource['head_revision_id']
    assert latest['head_publication_id'] != resource['head_publication_id']
    # A later observation never changes the earlier exact accepted receipt.
    assert first['receipt']['receipt_id'] == resource['head_publication_id']


def test_observed_new_head_does_not_replace_exact_accepted_receipt(timeline):
    service, project = timeline
    service.publish_parent_composition(project, 'main', _publication(project), idempotency_key='initial')
    accepted = service.accept(acceptance(service, project), identity=IDENTITY)
    receipt = copy.deepcopy(accepted)
    later = _publication(project, expected_head=accepted['revision_id'], parent_revision_id='later-head')
    service.publish_parent_composition(project, 'main', later, idempotency_key='later')
    assert service.get_project_timeline(project, 'main')['head_revision_id'] == 'later-head'
    assert accepted == receipt
    assert accepted['revision_id'] != 'later-head'
    assert service.lookup_request(project, 'main', 'save-1')['result']['accepted_revision_id'] == accepted['revision_id']


def test_wrong_project_and_unknown_timeline_refuse(timeline):
    service, project = timeline
    foreign = service.create_project({'slug': 'foreign', 'name': 'Foreign'}, idempotency_key='foreign')['id']
    for p, t in [(foreign, 'main'), (project, 'missing')]:
        with pytest.raises(NotFoundError):
            service.get_project_timeline(p, t)


def test_existing_route_preserves_auth_and_exact_response(timeline, tmp_path):
    """Exercise the unchanged HTTP route and credential dispatch on a tmp realm."""
    service, project = timeline
    service.publish_parent_composition(project, 'main', _publication(project), idempotency_key='initial')
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('head-reader', ['projects:read'])
    # Route dispatch delegates authorization to the existing _identity method.
    from http_helpers import Api
    import threading
    server = RuntimeHTTPServer(('127.0.0.1', 0), RuntimeHandler)
    server.runtime, server.credentials = service, credentials
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    endpoint = f'http://127.0.0.1:{server.server_port}'
    path = f'/v1/projects/{project}/timelines/main'
    try:
        resource = Api(endpoint, token).request('GET', path)
        assert observed(resource) == observed(service.get_project_timeline(project, 'main'))
        assert not {'config', 'registry', 'config_version', 'revision_id', 'content_digest'} & set(resource)
        with pytest.raises(RuntimeError) as error:
            Api(endpoint, None).request('GET', path)
        assert error.value.status == 401
        denied, _ = credentials.provision('worker-only', ['worker:execute'])
        with pytest.raises(RuntimeError) as error:
            Api(endpoint, denied).request('GET', path)
        assert error.value.status == 401
        foreign = service.create_project({'slug': 'other', 'name': 'Other'}, idempotency_key='other')['id']
        with pytest.raises(RuntimeError) as error:
            Api(endpoint, token).request('GET', path.replace(project, foreign))
        assert error.value.status == 404
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=5)


def test_openapi_response_contract_uses_existing_route_and_requires_head_fields():
    contract = yaml.safe_load((ROOT / 'contract/openapi/workspace-v1.yaml').read_text())
    route = contract['paths']['/v1/projects/{project_id}/timelines/{timeline_id}']['get']
    assert route['operationId'] == 'getProjectTimeline'
    assert route['responses']['200']['content']['application/json']['schema']['$ref'] == './schemas/timeline.json'
    assert 'observation is not acceptance' in route['responses']['200']['description']
    assert set(FIELDS) <= set(SCHEMA['required'])
    for key in FIELDS:
        assert SCHEMA['properties'][key]['type'] == ['string', 'null']
