"""Native PARAM meanings through the normal paired Runtime service and real admission."""
from __future__ import annotations

import base64
import copy
import json
import shutil
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from astrid.core.element import project_packs as packs
from astrid.sdk.contracts import DomainResult, ErrorObject
from astrid.sdk.timeline import commands, commit
from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params, capture_track_set
from astrid.sdk.timeline.capture import capture_track_create
from tests.core import test_project_packs
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration
REF = 'parent/clip:effect'
configured_project_pack = test_project_packs.configured


@pytest.fixture
def retained_pack(configured_project_pack, tmp_path, monkeypatch):
    use_runtime()
    from runtime_protocol.errors import NotFoundError
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    from runtime_protocol.timeline_commit_port import route_path

    root = tmp_path / 'realm'
    RealmStore.initialize(root, realm_id='realm').close()
    service = RuntimeService(root)
    service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    project = service.create_project({'slug': 'selected-schema', 'name': 'Selected schema'})['id']
    service.create_timeline(project, 'film', idempotency_key='create-film')
    case = SimpleNamespace(service=service, project=project, root=root)

    class Documents:
        def _identity(self):
            return {'realm_id': 'realm'}

        def show(self, document, *, project):
            try:
                return DomainResult.success(case.service.get_document(project, document))
            except NotFoundError:
                return DomainResult.failure(ErrorObject('not_found', 'missing', {}))

        def create(self, *, project, kind, document_id, content, idempotency_key):
            return DomainResult.success(case.service.create_document(
                project, {'kind': kind, 'document_id': document_id, 'content': content},
                idempotency_key=idempotency_key)['data'])

        def update(self, document, *, project, content, expected_version, idempotency_key):
            return DomainResult.success(case.service.update_document(
                project, document, {'content': content, 'expected_version': expected_version},
                idempotency_key=idempotency_key)['data'])

    class Media:
        def import_bytes(self, *, project, data, filename, media_type, idempotency_key):
            return DomainResult.success(case.service.ingest(
                project, data, media_type=media_type, idempotency_key=idempotency_key)['data'])

        def read_bytes(self, object_id):
            return case.service.cas.read(object_id.removeprefix('sha256:'))

    client = SimpleNamespace(documents=Documents(), media=Media())

    @contextmanager
    def connected():
        yield client

    monkeypatch.setattr(packs, '_open_client', connected)

    def head():
        resource = case.service.get_project_timeline(project, 'film')
        return {'revision_id': resource['head_revision_id'],
                'publication_id': resource['head_publication_id']}

    def bundle():
        closure = case.service._timeline_commits()[0].revision_closure(
            project, 'film', head()['revision_id'])
        return commit.bundle_from_document(closure)

    def request(calls, base=None):
        current = base or head()
        return {'api_version': 1, 'project_id': project, 'timeline_id': 'film',
                'base_revision_id': current['revision_id'],
                'base_publication_id': current['publication_id'], 'commands': calls}

    def submit(body, key, authorize=lambda: None):
        return case.service.commit_timeline(
            project, 'film', body, idempotency_key=key, publisher='author',
            invocation_path=route_path(project, 'film'), authorize=authorize)

    case.head, case.bundle, case.request, case.submit = head, bundle, request, submit
    try:
        source_root, directory, _ = test_project_packs.seed(project)
        path = directory / 'element.yaml'
        definition = yaml.safe_load(path.read_text())
        definition['schema']['properties']['seed']['maximum'] = 10
        definition['defaults']['seed'] = 4
        # Only changed declared properties are validated, never this whole object.
        definition['schema']['required'] = ['unrelated']
        definition['schema']['additionalProperties'] = False
        path.write_text(yaml.safe_dump(definition))
        result = packs.admit_project_pack('realm', project)
        selected = {key: result['elements'][0]['descriptor'][key]
                    for key in ('id', 'kind', 'packId', 'revision')}
        document = service.get_document(project, result['documentId'])
        pin = {'document_id': document['document_id'], 'version': document['version'],
               'content_digest': commit._digest(document['content'])}
        objects = {}
        for admission in document['content']['admissions']:
            descriptor = admission['snapshot_object']
            data = service.cas.read(descriptor['object_id'].removeprefix('sha256:'))
            objects[descriptor['object_id']] = {
                **descriptor, 'bytes_base64': base64.b64encode(data).decode('ascii')}
        case.options = {'schema_source': pin, 'realm_id': 'realm',
                        'schema_inputs': [({'pin': pin, 'document': document}, objects)]}
        case.selected, case.pin = selected, pin
        case.source_root, case.path, case.definition = source_root, path, definition
        case.artifact_root = Path(result['elements'][0]['snapshot']['root']).parents[3]
        submit(request([capture_track_create(bundle(), 'parent',
                                             {'id': 'picture', 'kind': 'visual'})]), 'track')
        row = {'id': 'effect', 'clipType': selected['id'], 'elementRef': selected,
               'at': 0, 'hold': 2, 'track': 'picture',
               'params': {'seed': 4, 'future': {'keep': [None, False, {}]}}}
        submit(request([capture_clip_add(bundle(), 'parent', row)]), 'effect')
        yield case
    finally:
        case.service.close()


def inverse(publication):
    return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1',
            'select': None, 'args': {'publications': [publication]}}


def raw_params(case, values, clear=()):
    # Deliberately bypass the capture helper; only the provider can authorize values.
    return {'schema_version': 1, 'op': 'clip.set-params', 'version': '1', 'select': REF,
            'args': {'values': values, 'clear': list(clear), 'schema_source': case.pin}}


def test_native_retained_schema_replay_inverse_reload_and_exact_retry(retained_pack, monkeypatch):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService

    case = retained_pack
    original = State(case.bundle()).entity(REF)
    base = case.head()
    command = capture_clip_set_params(case.bundle(), REF, values={'seed': 8}, **case.options)
    # Stale-base submission must replay its original exact admission input.
    case.submit(case.request([capture_track_set(case.bundle(), 'parent/track:picture',
                                               values={'label': 'Concurrent'})]), 'concurrent')
    body = case.request([command], base)
    accepted = case.submit(body, 'original-params')
    assert accepted['data']['canonical_document']['dependency_manifest']['documents'] == [case.pin]
    assert State(commit.bundle_from_document(json.loads(json.dumps(
        accepted['data']['canonical_document'])))).entity(REF)['params']['seed'] == 8
    before = case.head()
    with pytest.raises(RuntimeErrorBase, match='10|16'):
        case.submit(case.request([raw_params(case, {'seed': 16})]), 'raw-invalid')
    assert case.head() == before
    case.definition['schema']['properties']['seed']['maximum'] = 20
    case.path.write_text(yaml.safe_dump(case.definition))
    newer = packs.admit_project_pack('realm', case.project)
    assert newer['elements'][0]['descriptor']['revision'] != case.selected['revision']
    current = case.service.get_document(case.project, case.pin['document_id'])
    removed_selection = {**current['content'], 'admissions': []}
    case.service.update_document(
        case.project, current['document_id'],
        {'expected_version': current['version'], 'content': removed_selection},
        idempotency_key='remove-current-selection')
    shutil.rmtree(case.source_root)
    shutil.rmtree(case.artifact_root)
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())

    def forbidden(*args, **kwargs):
        raise AssertionError('retained PARAM used launcher, source, cache, or renderer')

    monkeypatch.setattr(packs, '_open_client', forbidden)
    monkeypatch.setattr(packs, 'resolve_admitted_element', forbidden)
    monkeypatch.setattr(packs, 'artifact_root', forbidden)
    monkeypatch.setattr(packs, 'authoring_root', forbidden)
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', forbidden)
        assert case.submit(body, 'original-params') == accepted
    # The current admission permits 16, but this history's captured V1 does not.
    with pytest.raises(RuntimeErrorBase, match='10|16'):
        case.submit(case.request([raw_params(case, {'seed': 16})]), 'retained-invalid')
    undone = case.submit(case.request([inverse(accepted['receipt']['receipt_id'])]), 'undo')
    assert State(commit.bundle_from_document(undone['data']['canonical_document'])).entity(REF) == original
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'redo')
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']
    opaque = {'literal': [None, False, {}, 'ƒ(keep literal)']}
    cleared = case.submit(case.request([raw_params(case, {'other': opaque}, ['seed'])]), 'clear-opaque')
    params = State(commit.bundle_from_document(cleared['data']['canonical_document'])).entity(REF)['params']
    assert params == {'other': opaque, 'future': original['params']['future']}


@pytest.mark.parametrize('damage', ['stale', 'owner', 'id', 'kind', 'revision', 'revoked',
                                   'legacy', 'missing', 'corrupt', 'foreign', 'authorization'])
def test_native_provider_refuses_unavailable_or_wrong_retained_basis(retained_pack, damage):
    from runtime_protocol.errors import ForbiddenError, RuntimeErrorBase

    case = retained_pack
    call = raw_params(case, {'seed': 8})
    def authorize():
        return None
    if damage in {'owner', 'id', 'kind', 'revision'}:
        row = copy.deepcopy(State(case.bundle()).entity(REF))
        row['id'] = 'damaged'
        row['elementRef']['packId' if damage == 'owner' else damage] = 'wrong'
        case.submit(case.request([capture_clip_add(case.bundle(), 'parent', row)]), 'damaged-ref')
        call['select'] = 'parent/clip:damaged'
    elif damage in {'stale', 'revoked', 'legacy'}:
        row = case.service.get_document(case.project, case.pin['document_id'])
        content = copy.deepcopy(row['content'])
        if damage == 'revoked':
            content['admissions'] = []
        elif damage == 'legacy':
            for admission in content['admissions']:
                del admission['snapshot_object']
        updated = case.service.update_document(
            case.project, row['document_id'], {'expected_version': row['version'], 'content': content},
            idempotency_key='changed-admission')['data']
        if damage != 'stale':
            call['args']['schema_source'] = {
                'document_id': updated['document_id'], 'version': updated['version'],
                'content_digest': commit._digest(updated['content'])}
    elif damage in {'missing', 'corrupt'}:
        objects = case.options['schema_inputs'][0][1]
        path = case.service.cas.path_for(next(iter(objects)).removeprefix('sha256:'))
        if damage == 'missing':
            path.unlink()
        else:
            path.write_bytes(b'corrupt')
    elif damage == 'foreign':
        foreign = case.service.create_project({'slug': 'foreign', 'name': 'Foreign'})['id']
        test_project_packs.seed(foreign)
        result = packs.admit_project_pack('realm', foreign)
        row = case.service.get_document(foreign, result['documentId'])
        call['args']['schema_source'] = {'document_id': row['document_id'], 'version': row['version'],
                                         'content_digest': commit._digest(row['content'])}
    else:
        def authorize():
            raise ForbiddenError('actor revoked')
    before = case.head()
    with pytest.raises(RuntimeErrorBase) as error:
        case.submit(case.request([call]), 'refused-' + damage, authorize=authorize)
    if damage == 'legacy':
        assert 'pack snapshot unavailable; re-admit pack' in str(error.value)
    assert case.head() == before


def test_paired_provider_requires_exact_installed_contract_digest():
    use_runtime()
    from runtime_protocol.errors import ValidationError
    from runtime_protocol.timeline_commit_provider import validate_timeline_commit_provider

    assert validate_timeline_commit_provider(commit.create_runtime_commit_service())
    with pytest.raises(ValidationError, match='interface/contract mismatch'):
        validate_timeline_commit_provider(commit.RuntimeCommitService('sha256:' + '0' * 64))
