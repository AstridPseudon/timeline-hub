"""Public duplicate through generated transport and the admitted real receiver.

Scene answers are synthetic; no native render or film acceptance is claimed.
"""
import copy
import io
import json
from email.message import Message
from types import SimpleNamespace

import pytest
from test_timeline_graph_commands import closure  # noqa: F401
from test_timeline_graph_runtime import runtime  # noqa: F401
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.sdk.remote import RemoteAstridClient
from astrid.sdk.timeline import commands, journal, saved_publish
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.saved_intent import read_saved_calls
from astrid.sdk.timeline_duplicate import duplicate_timeline
from astrid.sdk.workspace_client import WorkspaceClient
from banodoco_workspace_client import WorkspaceClient as GeneratedClient

pytestmark = pytest.mark.usefixtures('synthetic_scene_answers')


@pytest.fixture
def public(runtime, tmp_path, monkeypatch):  # noqa: F811 - imported shared pytest fixture
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.paired_session import PairedSessionAuthority
    from runtime_protocol.server import RuntimeHandler
    s, p = runtime
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('owner', ['admin', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'])
    server = SimpleNamespace(runtime=s, credentials=credentials, accepting_authenticated_requests=True, paired_sessions=PairedSessionAuthority(), daemon_runtime=SimpleNamespace(instance_id="duplicate-test"))
    traffic = []
    faults = {}
    def transport(method, path, headers, body=None):
        h = object.__new__(RuntimeHandler)
        h.server, h.command, h.path, h.headers = server, method, path, Message()
        for key, value in headers.items():
            h.headers.add_header(key, value)
        payload = bytes(body or b'')
        if h.headers.get('Content-Length') is None:
            h.headers.add_header('Content-Length', str(len(payload)))
        h.rfile = io.BytesIO(payload)
        reply = {}
        def send(status, value=None, **kwargs):
            raw = kwargs.get('body')
            if raw is None:
                raw = json.dumps(kwargs.get('error', value)).encode()
            reply.update(status=status, headers=kwargs.get('headers', {}), body=raw)
        h._send = send
        if path.endswith('/archive') and faults.get('archive_fail'):
            raise TimeoutError('archive transport unavailable')
        if path.endswith('/commit') and faults.get('before'):
            faults['before'](json.loads(payload))
        try:
            h._route()
        except RuntimeErrorBase as exc:
            send(exc.status, exc.as_dict())
        except Exception:
            import traceback
            traceback.print_exc()
            raise
        traffic.append((method, path, json.loads(payload) if payload else None, copy.deepcopy(reply)))
        if path.endswith('/commit') and faults.get('lose'):
            faults['lose'] -= 1
            raise TimeoutError('lost accepted response')
        if path.endswith('/commit') and faults.get('unknown'):
            raise TimeoutError('unknown transport outcome')
        return reply['status'], reply['headers'], reply['body']
    w = WorkspaceClient('http://127.0.0.1:1', token)
    w._generated = GeneratedClient(w.endpoint, token, transport=transport)
    client = RemoteAstridClient(w)
    monkeypatch.setenv('BANODOCO_LOCAL_DATA_ROOT', str(tmp_path / 'data'))
    monkeypatch.setattr(Checkout, 'SAY_SAVED', False)
    # Meaningful parent config, registry sentinels and a parent clip. Multiple
    # occurrences deliberately share one source shot; outputs must not share.
    parent = copy.deepcopy(s._commit_revision_closure(p, 't', 'rev-0')['parent_revision']['payload'])
    parent['config'].update(tracks=[dict(id='picture', kind='visual')], opaque={'literal': 's', 'null': None})
    parent['registry'] = {'opaque': {'literal': 's', 'nested': ['a', None]}}
    parent['clips'] = [dict(id='parent-clip', clipType='media', track='picture', at=0, hold=1, opaque='s')]
    s.publish_parent_composition(p, 't', dict(project_id=p, timeline_id='t', expected_head='rev-0', parent_composition=parent,
        shot_revisions=[], internal_timeline_revisions=[]), idempotency_key='source-parent')
    return s, p, client, traffic, faults


def history(s, p, timeline):
    return s.list_project_parent_composition_revisions(p, timeline, limit=200)['items']


def test_public_complete_copy_one_commit_undo_and_independence(public):
    s, p, client, traffic, faults = public
    source_head = s.head(p, 't')
    source = s._commit_revision_closure(p, 't', source_head['revision_id'])
    source_history = history(s, p, 't')
    result = duplicate_timeline(p, 't', slug='copy', client=client)
    assert result['status'] == 'accepted', result
    assert result['old_head'] == result['previous_revision_id'] == result['base_revision_id']
    assert result['new_head'] == result['accepted_revision_id']
    assert result['publication_id']
    copy_closure = s._commit_revision_closure(p, 'copy', result['new_head'])
    for key in ('config', 'registry', 'clips'):
        assert copy_closure['parent_revision']['payload'][key] == source['parent_revision']['payload'][key]
    occurrences = copy_closure['parent_revision']['payload']['occurrences']
    assert len(occurrences) == 2
    assert len({r['shot_id'] for r in occurrences}) == 2
    assert not {r['shot_id'] for r in occurrences} & {r['shot_id'] for r in source['shot_revisions']}
    assert len(history(s, p, 'copy')) == 2  # bootstrap + copy-content
    commits = [r for r in traffic if r[1].endswith('/commit')]
    assert len(commits) == 1
    assert commits[0][2]['change']['commands'][0]['op'] == 'timeline.duplicate'
    path = result['draft_path']
    rows = [json.loads(line) for line in journal.journal_path(p, 'copy').read_text().splitlines()]
    saves = [row for row in rows if row['kind'] == 'save' and any(c['op'] == 'timeline.duplicate' for c in row.get('calls', []))]
    assert len(saves) == 1 and len(saves[0]['calls']) == 1
    # A changed destination shot is a second ordinary saved publication.
    draft = Checkout.load(path)
    row = draft.bundle['placements'][0]
    pin = draft.bundle['source_mapping']['shots'][row['shot_id']]
    commands.run(draft, dict(op='shot.set', select='occurrence:'+row['occurrence_id']+'/shot', args=dict(
        source=dict(parent_revision_id=draft.base_revision, occurrence_id=row['occurrence_id'], shot_id=pin['shot_id'],
                    shot_revision_id=pin['revision_id'], internal_revision_id=pin['internal_timeline_revision_id']), values=dict(name='destination take'))))
    changed = draft.publish('changed destination shot', client=client)
    assert changed['status'] == 'accepted', changed
    assert s.head(p, 't') == source_head
    assert history(s, p, 't') == source_history
    assert s._commit_revision_closure(p, 't', source_head['revision_id']) == source
    # The later child edit blocks undoing the original duplicate.
    with pytest.raises(Exception, match='conflict|same-property|delete-vs-edit'):
        Checkout.load(path).undo(client=client, publication=result['publication_id'])


def test_public_duplicate_undo_restores_empty_parent(public):
    s, p, client, traffic, faults = public
    result = duplicate_timeline(p, 't', slug='undo-copy', client=client)
    assert result['status'] == 'accepted', result
    draft = Checkout.load(result['draft_path'])
    before = s.get_project_parent_composition_revision(p, 'undo-copy', result['old_head'])['payload']
    assert len(draft.undo(client=client)) == 1
    assert len(read_saved_calls(Checkout.load(draft.path))) == 1
    undone = Checkout.load(draft.path).publish('undo duplicate', client=client)
    assert undone['status'] == 'accepted', undone
    assert s.get_project_parent_composition_revision(p, 'undo-copy', undone['accepted_revision_id'])['payload'] == before


@pytest.mark.parametrize('failure', ['lost', 'finalize', 'unknown'])
def test_public_duplicate_recovers_same_request(public, monkeypatch, failure):
    s, p, client, traffic, faults = public
    if failure == 'lost':
        faults['lose'] = 1
    elif failure == 'unknown':
        faults['unknown'] = True
    else:
        original = saved_publish._replace
        calls = []
        def interrupted(*args):
            calls.append(1)
            if len(calls) == 1:
                raise OSError('interrupted local finalization')
            return original(*args)
        monkeypatch.setattr(saved_publish, '_replace', interrupted)
    result = duplicate_timeline(p, 't', slug='recover', client=client)
    if failure == 'unknown':
        assert result['status'] == 'pending' and result['request_id'], result
        assert not s._timeline_resource('recover')['archived']
        faults['unknown'] = False
        accepted = Checkout.load(result['draft_path']).publish('recover', client=client)
        assert accepted['status'] == 'accepted' and accepted['request_id'] == result['request_id']
    else:
        assert result['status'] == 'accepted', result
    assert len(history(s, p, 'recover')) == 2
    commits = [r for r in traffic if r[1].endswith('/commit')]
    assert len({json.dumps(r[2], sort_keys=True) for r in commits}) == 1
    assert not s._timeline_resource('recover')['archived']
    assert not any('archive' in r[1] for r in traffic)


@pytest.mark.parametrize('cleanup', ['archive', 'archive-fails', 'intervening'])
def test_conclusive_refusal_guarded_rollback_and_retention(public, cleanup):
    s, p, client, traffic, faults = public
    once = []
    changed_head = []
    def before(body):
        if once:
            return
        once.append(True)
        if cleanup == 'intervening':
            head = s.head(p, 'refusal')
            parent = copy.deepcopy(s.get_project_parent_composition_revision(p, 'refusal', head['revision_id'])['payload'])
            parent['config']['intervening'] = 'keep me'
            changed_head.append(s.publish_parent_composition(p, 'refusal', dict(project_id=p, timeline_id='refusal',
                expected_head=head['revision_id'], parent_composition=parent, shot_revisions=[], internal_timeline_revisions=[]), idempotency_key='intervening'))
        else:
            # Storage corruption after saved verification, before receiver read.
            with s.store._transaction():
                s.store.conn.execute("UPDATE internal_timeline_revisions SET content_digest='sha256:tampered' WHERE id='int-1'")
    faults['before'] = before
    if cleanup == 'archive-fails':
        faults['archive_fail'] = True
    with pytest.raises(Exception, match='nothing kept' if cleanup == 'archive' else "retained destination 'refusal'"):
        duplicate_timeline(p, 't', slug='refusal', client=client)
    if cleanup == 'archive':
        assert s._timeline_resource('refusal')['archived']
        with pytest.raises(Exception):
            s.head(p, 'refusal')
    else:
        assert not s._timeline_resource('refusal')['archived']
        if cleanup == 'intervening':
            head = s.head(p, 'refusal')
            assert s.get_project_parent_composition_revision(p, 'refusal', head['revision_id'])['payload']['config']['intervening'] == 'keep me'
        else:
            assert len(history(s, p, 'refusal')) == 1
    assert not s.store.conn.execute("SELECT 1 FROM command_idempotency WHERE command_kind='timeline.commit'").fetchall()


def test_invalid_source_before_creation_creates_nothing(public):
    s, p, client, traffic, faults = public
    with s.store._transaction():
        s.store.conn.execute("UPDATE internal_timeline_revisions SET content_digest='tampered' WHERE id='int-1'")
    with pytest.raises(Exception):
        duplicate_timeline(p, 't', slug='absent', client=client)
    assert s.store.conn.execute("SELECT 1 FROM timelines WHERE id='absent'").fetchone() is None
    # Native inspection uses POST too; the refused copy never addresses or
    # creates its destination, and never sends a content COMMIT.
    assert not any('/timelines/absent' in row[1] or row[1].endswith('/commit') for row in traffic)
