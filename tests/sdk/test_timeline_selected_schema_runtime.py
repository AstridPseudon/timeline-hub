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


def test_element_first_use_retains_declaration_without_param_writes(retained_pack):
    from runtime_protocol.service import RuntimeService

    case = retained_pack
    before = copy.deepcopy(case.bundle()['parent']['clips'][0])
    assert case.bundle()['source_mapping']['_runtime_document']['dependency_manifest']['documents'] == []
    call = {'schema_version': 1, 'op': 'clip.set-element', 'version': '1', 'select': REF,
            'args': {'elementRef': case.selected, 'schema_source': case.pin}}
    accepted = case.submit(case.request([call]), 'element-first-use')
    assert accepted['data']['canonical_document']['dependency_manifest']['documents'] == [case.pin]
    assert case.bundle()['parent']['clips'][0] == before
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    undone = case.submit(case.request([inverse(accepted['receipt']['receipt_id'])]), 'element-inverse')
    assert case.bundle()['parent']['clips'][0] == before
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'element-redo')
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']


def raw_params(case, values, clear=()):
    # Deliberately bypass the capture helper; only the provider can authorize values.
    return {'schema_version': 1, 'op': 'clip.set-params', 'version': '1', 'select': REF,
            'args': {'values': values, 'clear': list(clear), 'schema_source': case.pin}}


def test_mixed_pack_readmission_keeps_old_and_new_native_param_sources(retained_pack, monkeypatch):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    case = retained_pack
    manifest = yaml.safe_load((case.source_root / 'pack.yaml').read_text())
    other = test_project_packs.add_second_element(case.source_root, case.path.parent, manifest)
    component = case.path.parent / 'component.tsx'
    component.write_text(component.read_text() + '\n// Initial mixed A revision\n')
    first = packs.admit_project_pack('realm', case.project)
    records = {e['descriptor']['id']: e for e in first['elements']}
    old_document = case.service.get_document(case.project, first['documentId'])
    old_objects = {a['snapshot_object']['object_id']: case.service.cas.read(
        a['snapshot_object']['object_id'].removeprefix('sha256:'))
        for a in old_document['content']['admissions']}
    old_pin = {'document_id': old_document['document_id'], 'version': old_document['version'],
               'content_digest': commit._digest(old_document['content'])}
    case.pin = old_pin
    params = []
    for element, identity in [('reveal', 'mixed-a'), ('fade', 'old-b')]:
        selected = {key: records[element]['descriptor'][key]
                    for key in ('id', 'kind', 'packId', 'revision')}
        add = capture_clip_add(case.bundle(), 'parent', {
            'id': identity, 'clipType': element, 'elementRef': selected,
            'at': 3 if element == 'reveal' else 6, 'hold': 2, 'track': 'picture',
            'params': {'seed': 4, 'opaque': [None, False, {}]}})
        case.submit(case.request([add]), 'mixed-add-' + identity)
        params.append({**raw_params(case, {'seed': 8}), 'select': 'parent/clip:' + identity})
    original_body = case.request(params)
    original = case.submit(original_body, 'mixed-first')

    definition = yaml.safe_load((other / 'element.yaml').read_text())
    definition['schema']['properties']['seed']['maximum'] = 20
    (other / 'element.yaml').write_text(yaml.safe_dump(definition))
    second = packs.admit_project_pack('realm', case.project)
    current = {e['descriptor']['id']: e for e in second['elements']}
    assert current['reveal'] == records['reveal']
    assert current['fade']['descriptor']['revision'] != records['fade']['descriptor']['revision']
    document = case.service.get_document(case.project, second['documentId'])
    assert document['content']['admissions'][:-1] == old_document['content']['admissions']
    assert all(case.service.cas.read(identity.removeprefix('sha256:')) == raw
               for identity, raw in old_objects.items())
    case.pin = {'document_id': document['document_id'], 'version': document['version'],
                'content_digest': commit._digest(document['content'])}
    assert packs.admit_project_pack('realm', case.project)['documentVersion'] == second['documentVersion']
    shutil.rmtree(case.source_root)
    shutil.rmtree(case.artifact_root)
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    captured = []
    original_source = RequestCommitPort.config_source

    def source(port, pin):
        verified = original_source(port, pin)
        captured.append(copy.deepcopy(verified))
        return verified

    monkeypatch.setattr(RequestCommitPort, 'config_source', source)
    selected = {key: current['fade']['descriptor'][key]
                for key in ('id', 'kind', 'packId', 'revision')}
    add = capture_clip_add(case.bundle(), 'parent', {
        'id': 'new-b', 'clipType': 'fade', 'elementRef': selected,
        'at': 9, 'hold': 2, 'track': 'picture', 'params': {'seed': 4}})
    a = {**raw_params(case, {'seed': 9}), 'select': 'parent/clip:mixed-a'}
    a['args']['schema_source'] = old_pin
    b = {**raw_params(case, {'seed': 9}), 'select': 'parent/clip:old-b'}
    new_b = {**raw_params(case, {'seed': 16}), 'select': 'parent/clip:new-b'}
    accepted = case.submit(case.request([a, b, add, new_b]), 'mixed-after-reopen')
    assert {'pin': old_pin, 'document': old_document} in captured
    assert {'pin': case.pin, 'document': document} in captured
    state = State(commit.bundle_from_document(accepted['data']['canonical_document']))
    assert state.entity('parent/clip:mixed-a')['params'] == {'seed': 9, 'opaque': [None, False, {}]}
    assert state.entity('parent/clip:old-b')['params'] == {'seed': 9, 'opaque': [None, False, {}]}
    assert state.entity('parent/clip:new-b')['params'] == {'seed': 16}
    before = case.head()
    with pytest.raises(RuntimeErrorBase, match='10|16'):
        case.submit(case.request([{**raw_params(case, {'seed': 16}),
                                   'select': 'parent/clip:old-b'}]), 'mixed-old-b-invalid')
    assert case.head() == before
    assert case.submit(original_body, 'mixed-first') == original
    undone = case.submit(case.request([inverse(accepted['receipt']['receipt_id'])]), 'mixed-undo')
    restored = State(commit.bundle_from_document(undone['data']['canonical_document']))
    prior = State(commit.bundle_from_document(original['data']['canonical_document']))
    for reference in (REF, 'parent/clip:mixed-a', 'parent/clip:old-b'):
        assert restored.entity(reference) == prior.entity(reference)
    assert restored.entity('parent/clip:new-b', optional=True) is None
    # Undo retains both consumed source pins for the subsequent redo.
    assert undone['data']['canonical_document']['dependency_manifest'] == accepted['data']['canonical_document']['dependency_manifest']
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'mixed-redo')
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']


@pytest.fixture
def multi_pack(retained_pack, monkeypatch):
    """Real admissions with two elements and multiple historical revisions."""
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    case = retained_pack
    case.initial_pin = copy.deepcopy(case.pin)
    case.submit(case.request([raw_params(case, {'seed': 4})]), 'retain-initial')
    other = case.path.parent.parent / 'other'
    shutil.copytree(case.path.parent, other)
    definition = copy.deepcopy(case.definition)
    definition['id'] = 'other'
    (other / 'element.yaml').write_text(yaml.safe_dump(definition))
    manifest_path = case.source_root / 'pack.yaml'
    manifest = yaml.safe_load(manifest_path.read_text())
    entry = copy.deepcopy(manifest['rendering']['effects/reveal'])
    entry['path'] = entry['path'].replace('/reveal/', '/other/')
    for resource in entry['resources']:
        resource['path'] = resource['path'].replace('/reveal/', '/other/')
    manifest['rendering']['effects/other'] = entry
    manifest_path.write_text(yaml.safe_dump(manifest))
    for maximum in (20, 30):
        case.definition['schema']['properties']['seed']['maximum'] = maximum
        definition['schema']['properties']['seed']['maximum'] = maximum
        (other / 'element.yaml').write_text(yaml.safe_dump(definition))
        case.path.write_text(yaml.safe_dump(case.definition))
        result = packs.admit_project_pack('realm', case.project)
    case.other_selected = next({key: item['descriptor'][key]
                                for key in ('id', 'kind', 'packId', 'revision')}
                               for item in result['elements'] if item['descriptor']['id'] == 'other')
    document = case.service.get_document(case.project, case.pin['document_id'])
    case.pin = {'document_id': document['document_id'], 'version': document['version'],
                'content_digest': commit._digest(document['content'])}
    admissions = document['content']['admissions']
    assert len(admissions) >= 4
    case.object_id = next(item['snapshot_object']['object_id'] for item in admissions
                          if all(item[key] == case.selected[key]
                                 for key in ('id', 'kind', 'revision')))
    case.other_object_id = next(item['snapshot_object']['object_id'] for item in admissions
                                if all(item[key] == case.other_selected[key]
                                       for key in ('id', 'kind', 'revision')))
    case.document = copy.deepcopy(document)
    case.object_reads = []
    original = RequestCommitPort.document_object

    def read(port, pin, object_id):
        case.object_reads.append((copy.deepcopy(pin), object_id))
        return original(port, pin, object_id)

    monkeypatch.setattr(RequestCommitPort, 'document_object', read)
    return case


def test_native_params_reads_only_the_exact_selected_object(multi_pack):
    case = multi_pack
    pin = copy.deepcopy(case.pin)
    accepted = case.submit(case.request([raw_params(case, {'seed': 8})]), 'selected-only')
    assert case.object_reads == [(pin, case.object_id)]
    assert accepted['data']['canonical_document']['dependency_manifest']['documents'] == [
        case.initial_pin, pin]
    assert case.service.get_document(case.project, pin['document_id']) == case.document


@pytest.mark.parametrize('damage', ['missing', 'corrupt'])
def test_native_params_does_not_consume_unselected_bytes(multi_pack, damage):
    case = multi_pack
    path = case.service.cas.path_for(case.other_object_id.removeprefix('sha256:'))
    if damage == 'missing':
        path.unlink()
    else:
        path.write_bytes(b'corrupt unselected snapshot')
    accepted = case.submit(case.request([raw_params(case, {'seed': 8})]), 'unselected-' + damage)
    assert State(commit.bundle_from_document(accepted['data']['canonical_document'])).entity(
        REF)['params']['seed'] == 8
    assert case.object_reads == [(case.pin, case.object_id)]


def test_native_staged_params_different_refs_and_pins_inverse_redo_restore(multi_pack):
    case = multi_pack
    first = raw_params(case, {'seed': 8})
    first['args']['schema_source'] = case.initial_pin
    other_ref = 'parent/clip:other'
    row = {'id': 'other', 'clipType': 'other', 'elementRef': case.other_selected,
           'at': 3, 'hold': 2, 'track': 'picture', 'params': {'seed': 4}}
    add = capture_clip_add(case.bundle(), 'parent', row)
    second = raw_params(case, {'seed': 25})
    second['select'] = other_ref
    accepted = case.submit(case.request([add, first, second]), 'different-pins')
    document = accepted['data']['canonical_document']
    assert State(commit.bundle_from_document(document)).entity(other_ref)['params'] == {'seed': 25}
    expected = [(case.initial_pin, case.object_id), (case.pin, case.other_object_id)]
    assert case.object_reads == expected
    entry = case.service._timeline_commits()[0].history_entry(
        case.project, 'film', accepted['receipt']['receipt_id'])
    for record, (pin, object_id) in zip(entry['records']['commands'][1:], expected):
        source = next(dep for dep in record['dependencies'] if dep['key'] == 'params.schema')
        snapshot = next(dep for dep in record['dependencies'] if dep['key'] == 'params.snapshot')
        assert source['pin'] == snapshot['pin']['source'] == pin
        assert snapshot['pin']['object']['object_id'] == object_id
    case.object_reads.clear()
    undone = case.submit(case.request([inverse(accepted['receipt']['receipt_id'])]), 'undo-multi')
    assert case.object_reads == expected
    assert State(case.bundle()).entity(other_ref, optional=True) is None
    case.object_reads.clear()
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'redo-multi')
    assert redone['data']['canonical_document'] == document
    assert case.object_reads == expected
    case.object_reads.clear()
    case.submit(case.request([capture_track_set(case.bundle(), 'parent/track:picture',
                                               values={'label': 'Unrelated'})]), 'track-only')
    from astrid.sdk.timeline.capture import capture_move
    case.submit(case.request([capture_move(case.bundle(), REF, 1)]), 'move-only')
    assert case.object_reads == []
    image = document['parent_revision']
    restore = {'schema_version': 1, 'op': 'timeline.restore', 'version': '1', 'select': None,
               'args': {key: image[key] for key in ('revision_id', 'content_digest')}}
    restored = case.submit(case.request([restore]), 'restore-multi')
    assert restored['data']['canonical_document'] == document
    assert case.object_reads == []


def test_native_rebase_after_v2_and_selection_removal_uses_original_object(multi_pack):
    case = multi_pack
    case.submit(case.request([raw_params(case, {'seed': 4})]), 'retain-multi')
    base = case.head()
    body = case.request([raw_params(case, {'seed': 8})], base)
    # A later source version cannot change the accepted declaration's meaning.
    current = case.service.get_document(case.project, case.pin['document_id'])
    case.service.update_document(
        case.project, current['document_id'],
        {'expected_version': current['version'], 'content': {**current['content'], 'admissions': []}},
        idempotency_key='remove-multi-selection')
    case.submit(case.request([capture_track_set(case.bundle(), 'parent/track:picture',
                                               values={'label': 'After V2'})]), 'after-v2')
    case.object_reads.clear()
    accepted = case.submit(body, 'rebase-after-v2')
    assert accepted['data']['status'] == 'rebased'
    assert case.object_reads == [(case.pin, case.object_id)] * 2
    case.object_reads.clear()
    undone = case.submit(case.request([inverse(accepted['receipt']['receipt_id'])]), 'undo-after-v2')
    assert case.object_reads == [(case.pin, case.object_id)]
    case.object_reads.clear()
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'redo-after-v2')
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']
    assert case.object_reads == [(case.pin, case.object_id)]


def test_native_multiple_params_share_only_the_needed_object(multi_pack):
    case = multi_pack
    first = raw_params(case, {'seed': 8})
    second = raw_params(case, {'seed': 9})
    accepted = case.submit(case.request([first, second]), 'shared-object')
    assert case.object_reads == [(case.pin, case.object_id)]
    assert State(commit.bundle_from_document(accepted['data']['canonical_document'])).entity(
        REF)['params']['seed'] == 9


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
