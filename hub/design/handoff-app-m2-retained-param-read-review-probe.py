"""Bounded pure native capture probe; synthetic inputs are not Runtime authority.

Read frozen source with git archive, never checkout or install. No build, Runtime,
service, browser or sockets. The temporary source copy is removed on exit.
"""
import base64
import copy
import hashlib
import importlib.abc
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile

AGENT_REPO = '/home/user/peteromallet/astrid-agent'
AGENT = '027bd16d96010544331c953c0e1014e161786e71'
RUNTIME_REPO = '/home/user/banodoco/banodoco-workspace-runtime'
RUNTIME = '8308cb9c153df3d7a5fdaf492af075be5b18e670'


def show(repo, commit, path):
    return subprocess.check_output(['git', '-C', repo, 'show', f'{commit}:{path}'])


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


class NoRuntimeOrRenderer(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname.startswith(('runtime_protocol', 'composition', 'remotion',
                                'astrid.packs.rendering', 'astrid.sdk.authoring_render_preview')):
            raise AssertionError(f'forbidden import: {fullname}')


sys.meta_path.insert(0, NoRuntimeOrRenderer())
with tempfile.TemporaryDirectory(prefix='native-source-', dir=Path(__file__).parent) as directory:
    archive = subprocess.check_output(['git', '-C', AGENT_REPO, 'archive', AGENT, 'astrid'])
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(directory, filter='data')
    sys.path.insert(0, directory)
    from astrid.core.element import project_packs as packs
    from astrid.core.element.catalog import _element_descriptor
    from astrid.core.element.schema import element_definition_from_payload
    from astrid.sdk.timeline._command_state import CommandError, State
    from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
    from astrid.sdk.timeline.commands import execute

    assert Path(packs.__file__).is_relative_to(directory)
    fixture = json.loads(show(AGENT_REPO, AGENT,
        'tests/editing_conformance/fixtures/recipe_m2_scalar_params_object.json'))
    bundle = fixture['bundle']
    ref = fixture['command']['select']
    realm, project = 'realm', bundle['project_id']
    content = packs._content(realm, project)
    owner = content['pack_id']
    root = PurePosixPath('rendering/elements/effects/reveal')
    definition = {
        'schema_version': 1, 'id': 'reveal', 'kind': 'effect', 'pack_id': owner,
        'short_description': 'Pure test declaration.', 'defaults': {'seed': 4},
        'schema': {'type': 'object', 'properties': {'seed': {'type': 'number', 'maximum': 10}}},
        'runtime': {'adapter': 'remotion'},
    }
    files = {
        'pack.yaml': canonical({'id': owner, 'rendering': {'effects/reveal': {
            'type': 'element', 'path': str(root / 'element.json')}}}),
        str(root / 'element.json'): canonical(definition),
        str(root / 'component.tsx'): b'export default function Reveal(){return null;}\n',
    }
    element = element_definition_from_payload(definition, root=root, kind='effect',
        source=f'pack:{owner}', editable=True, priority=100,
        manifest_path=root / 'element.json', files=files)
    descriptor = _element_descriptor(element, files=files)
    selected = {key: descriptor[key] for key in ('id', 'kind', 'packId', 'revision')}
    # A synthetic build receipt exercises the published pure validator only.
    receipt = canonical({'schema': 'astrid.element-build/v1',
        'selectionDigest': 'sha256:' + '0' * 64, 'elements': [{'projectId': project, **selected}]})
    data = packs._portable_snapshot(files, receipt)
    digest = 'sha256:' + hashlib.sha256(data).hexdigest()
    obj = {'object_id': digest, 'digest': digest, 'size': len(data), 'media_type': 'application/json'}
    value = {**obj, 'bytes_base64': base64.b64encode(data).decode()}
    content['admissions'] = [{**{key: selected[key] for key in ('id', 'kind', 'revision')},
        'snapshot_digest': packs._closure_digest([
            {'path': name, 'sha256': hashlib.sha256(raw).hexdigest()} for name, raw in sorted(files.items())]),
        'snapshot_object': obj}]
    document = {'document_id': packs.stable_document_id(project, packs.DOCUMENT_KIND, 'default'),
        'project_id': project, 'kind': packs.DOCUMENT_KIND, 'version': 1, 'content': content,
        'created_at': '2026-10-20T00:00:00Z', 'updated_at': '2026-10-20T00:00:00Z'}
    pin = {'document_id': document['document_id'], 'version': 1,
           'content_digest': packs._json_digest(content)}
    verified = {'pin': pin, 'document': document}
    objects = {digest: value}
    row = State(bundle).entity(ref)
    row.update(clipType=selected['id'], elementRef=selected, params={'seed': 4, 'opaque': [None, False, {}]})
    before = copy.deepcopy(bundle)

    def capture(inputs, seed=8):
        return capture_clip_set_params(bundle, ref, values={'seed': seed},
            schema_source=pin, schema_inputs=inputs, realm_id=realm)

    def refuses(label, inputs, message, seed=8):
        try:
            capture(inputs, seed)
        except CommandError as exc:
            assert message in str(exc), (label, str(exc))
            assert bundle == before
            print(f'PASS {label}: {exc}')
        else:
            raise AssertionError(f'{label} unexpectedly captured')

    complete = [(verified, objects)]
    command = capture(complete)
    result = execute(bundle, [command], schema_inputs=complete, realm_id=realm)
    assert State(result.bundle).entity(ref)['params'] == {'seed': 8, 'opaque': [None, False, {}]}
    assert bundle == before
    assert result.bundle['source_mapping']['pinned_documents'] == [verified]
    dependencies = result.records[0]['dependencies']
    assert {item['key'] for item in dependencies} >= {'params.schema', 'params.snapshot'}
    assert next(item for item in dependencies if item['key'] == 'params.snapshot')['pin']['object'] == obj
    print('PASS complete native shape: 4 -> 8, exact source and selected object dependencies, opaque preserved')
    refuses('complete V1 rejects 16', complete, '10', seed=16)
    refuses('object available but VerifiedDocument absent', [], 'selected pack snapshot input unavailable')
    refuses('pin plus public object is not VerifiedDocument', [({'pin': pin, **value}, objects)],
            'Unsupported project pack payload schema/source binding')
    refuses('VerifiedDocument without selected object', [(verified, {})], 'Invalid verified pack snapshot object')
    removed = copy.deepcopy(document)
    removed['version'] = 3
    removed['content']['admissions'] = []
    current_pin = {'document_id': removed['document_id'], 'version': 3,
                   'content_digest': packs._json_digest(removed['content'])}
    refuses('current removed declaration does not match V1',
            [({'pin': current_pin, 'document': removed}, objects)], 'selected pack snapshot input unavailable')
    refuses('relabelling current removal with old pin cannot restore admission',
            [({'pin': pin, 'document': removed}, objects)], 'Element owner/revision is not admitted')

    generated = show(RUNTIME_REPO, RUNTIME, 'packages/typescript/src/generated.ts').decode()
    method = next(line for line in generated.splitlines() if 'async getProjectVerifiedDocumentObject(' in line)
    assert 'objectId: string): Promise<VerifiedDocumentObject>' in method
    assert 'Promise<VerifiedDocument>' not in generated
    print('PASS candidate generated public read returns object only; no Promise<VerifiedDocument> method')
    print('8 bounded checks passed; no Runtime acceptance/public-read execution or golden qualification claimed')
