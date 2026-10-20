import json
from pathlib import Path
from tempfile import TemporaryDirectory
from runtime_protocol.store import RealmStore
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
from runtime_protocol.errors import RuntimeErrorBase

root = Path(__file__).parent
with TemporaryDirectory(dir=root, prefix='native-realm-') as temporary:
    realm = Path(temporary) / 'realm'
    RealmStore.initialize(realm).close()
    service = RuntimeService(realm)
    project_id = service.create_project({'slug': 'admission', 'name': 'Admission'}, idempotency_key='project')['id']
    timeline_id = 'main'
    service.create_timeline(project_id, timeline_id, idempotency_key='timeline')
    config = {'output': {'fps': 30, 'resolution': '1280x720', 'file': 'out.mp4'}, 'tracks': [{'id': 'V1', 'kind': 'visual', 'label': 'V1'}], 'clips': []}
    body = {'project_id': project_id, 'timeline_id': timeline_id, 'expected_head': None, 'parent_revision_id': 'seed-r1',
            'parent_composition': {'slug': 'main', 'name': 'Main', 'config': config, 'registry': {'assets': {}}, 'clips': [], 'occurrences': []},
            'shot_revisions': [], 'internal_timeline_revisions': []}
    accepted = service.publish_parent_composition(project_id, timeline_id, body, idempotency_key='seed')
    scopes = ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write']
    def state(label):
        head = dict(service.store.conn.execute('SELECT revision_id, publication_id FROM parent_composition_heads WHERE project_id=? AND timeline_id=?', (project_id, timeline_id)).fetchone())
        health = service.health()
        handshake = service.handshake({'authenticated_actor': 'astrid-browser', 'requested_scopes': scopes, 'authenticated_scopes': scopes})
        try:
            history = {'status': 200, 'body': service.list_timeline_commits(project_id, timeline_id, authorize=lambda: None)}
        except RuntimeErrorBase as error:
            history = {'status': error.status, 'body': error.as_dict()}
        return {'label': label, 'health': health, 'handshake': handshake, 'realm': service.realm_resource(), 'head': head, 'history': history}
    neutral = state('neutral')
    assert neutral['health']['status'] == 'ok'
    assert neutral['head'] == {'revision_id': 'seed-r1', 'publication_id': None}
    assert neutral['history']['status'] == 409
    assert neutral['history']['body']['details']['reason'] == 'history_unavailable'
    service.close()
    service = RuntimeService(realm)
    provider = load_timeline_commit_provider('astrid')
    service.register_timeline_commit_provider(provider)
    authoring = state('astrid')
    assert authoring['history']['status'] == 200
    assert authoring['head']['revision_id'] == neutral['head']['revision_id']
    assert authoring['head']['publication_id'] == accepted['receipt']['receipt_id']
    parent = service.get_project_parent_composition_revision(project_id, timeline_id, 'seed-r1')
    result = {'projectId': project_id, 'timelineId': timeline_id, 'neutral': neutral, 'authoring': authoring,
              'parent': parent, 'provider': {'id': provider.provider_id, 'digest': provider.contract_digest}}
    (root / 'native-admission.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({mode: {'health': value['health']['status'], 'head': value['head'], 'history': value['history']['status']} for mode, value in [('neutral', neutral), ('astrid', authoring)]}, indent=2))
    service.close()
