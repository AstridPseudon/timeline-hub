"""Detached real Runtime service probe; no Door, sockets, provider or renderer."""
import copy
import json
from pathlib import Path
import tempfile
from runtime_protocol.store import RealmStore
from runtime_protocol.service import RuntimeService
from runtime_protocol.util import canonical_json

fixture = json.loads(Path(__file__).with_name('bootstrap-candidate.json').read_text())
with tempfile.TemporaryDirectory(prefix='opaque-bootstrap-') as temp:
    root = Path(temp) / 'realm'
    RealmStore.initialize(root).close()
    runtime = RuntimeService(root)
    try:
        project = runtime.create_project({'slug': 'opaque-probe', 'name': 'Opaque probe'})['id']
        runtime.create_timeline(project, 'headless-shell', idempotency_key='create-shell')
        # Historical authored shell material, hidden by the ordinary public resource.
        content = {'slug': 'edited', 'config': fixture['hiddenAuthored'], 'registry': {'assets': {}}}
        with runtime.store.conn:
            runtime.store.conn.execute('INSERT INTO project_documents VALUES (?, ?, ?, ?, 1, ?, ?)',
                ('timeline:headless-shell', project, 'timeline', canonical_json(content), '2026-10-20T00:00:00Z', '2026-10-20T00:00:00Z'))
        public = runtime.get_project_timeline(project, 'headless-shell')
        assert public['head_revision_id'] is None and 'config' not in public
        body = copy.deepcopy(fixture['submitted'])
        body['project_id'] = project
        runtime.publish_parent_composition(project, 'headless-shell', body, idempotency_key='repair-shell')
        head = runtime.get_project_timeline(project, 'headless-shell')['head_revision_id']
        accepted = json.loads(runtime.store.conn.execute('SELECT payload_json FROM parent_composition_revisions WHERE id=?', (head,)).fetchone()['payload_json'])
        assert accepted['config']['clips'] == [] and 'opaque' not in accepted['config']
        retained = json.loads(runtime.store.conn.execute('SELECT content_json FROM project_documents WHERE id=?', ('timeline:headless-shell',)).fetchone()['content_json'])
        assert retained == content
        print(json.dumps({'result': 'DETACHED SERVICE ACCEPTED EMPTY PARENT OVER HIDDEN NONEMPTY SHELL',
            'accepted_config': accepted['config'], 'legacy_recovery_bytes_retained': True,
            'limitation': 'Current integration Runtime service without provider; no HTTP/Door or deployed paired-tuple acceptance claimed.'}, indent=2))
    finally:
        runtime.close()
