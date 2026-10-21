"""Pinned trim/clear/params batch through the real provider and durable Session.

The existing injected HTTP transport avoids sockets; only the central service
runs this integration lane. The frozen main API builds the original film before the current Runtime opens it.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys

import pytest

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_clip_set_params
from astrid.sdk.timeline.commit import _json, bundle_from_document
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance import test_native_batch_ingress
from tests.editing_conformance.test_native_batch_ingress import command, label
from tests.editing_conformance.test_native_sheet_current import property_cell
from tests.helpers.runtime import runtime_checkout

pytestmark = pytest.mark.integration
runtime = test_native_batch_ingress.runtime
MEDIA = 'parent/clip:video'
TITLE = 'parent/clip:title'


def _preflight_detached_fixture(root, project_id):
    """Prove the historical seed is a readable current Runtime closure."""
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    failures = []

    def check(name, condition):
        if not condition:
            failures.append(name)

    service = RuntimeService(root)
    try:
        try:
            service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
        except Exception as exc:  # noqa: BLE001  (report all setup failures together)
            failures.append(f'current provider registration: {type(exc).__name__}: {exc}')

        try:
            timeline = service.get_project_timeline(project_id, 'film')
        except Exception as exc:  # noqa: BLE001  (report all setup failures together)
            timeline = None
            failures.append(f'current timeline read: {type(exc).__name__}: {exc}')
        try:
            parent = service.get_project_parent_composition_revision(project_id, 'film', 'sheet-baseline')
        except Exception as exc:  # noqa: BLE001  (report all setup failures together)
            parent = None
            failures.append(f'current parent read: {type(exc).__name__}: {exc}')
        try:
            closure = service._timeline_commits()[0].revision_closure(project_id, 'film', 'sheet-baseline')
        except Exception as exc:  # noqa: BLE001  (report all setup failures together)
            closure = None
            failures.append(f'current closure read: {type(exc).__name__}: {exc}')
        try:
            head = service._timeline_commits()[0].head(project_id, 'film')
        except Exception as exc:  # noqa: BLE001  (report all setup failures together)
            head = None
            failures.append(f'current head read: {type(exc).__name__}: {exc}')

        check('project/timeline identity', isinstance(timeline, dict)
              and timeline.get('project_id') == project_id and timeline.get('timeline_id') == 'film')
        check('head revision/publication pair', isinstance(head, dict)
              and head.get('revision_id') == 'sheet-baseline'
              and isinstance(head.get('publication_id'), str) and head['publication_id'])
        check('public head mirrors pair', isinstance(timeline, dict)
              and timeline.get('head_revision_id') == 'sheet-baseline'
              and timeline.get('head_publication_id') == (head or {}).get('publication_id'))

        if parent is not None and closure is not None:
            parent_image = closure['parent_revision']
            check('parent revision identity mirror', parent.get('revision_id') == parent_image.get('revision_id')
                  and parent.get('content_digest') == parent_image.get('content_digest'))
            check('parent payload mirror', parent.get('payload') == parent_image.get('payload'))
            check('manifest mirror', parent.get('dependency_manifest') == closure.get('dependency_manifest'))
            check('closure project/timeline identity', closure.get('project_id') == project_id
                  and closure.get('timeline_id') == 'film')

            payload = parent_image['payload']
            occurrences = payload.get('occurrences')
            check('parent container shape', isinstance(payload.get('config'), dict)
                  and payload.get('clips') == [] and isinstance(occurrences, list)
                  and len(occurrences) == 1)
            occurrence = occurrences[0] if isinstance(occurrences, list) and len(occurrences) == 1 else {}
            check('occurrence ownership/track shape', occurrence.get('occurrence_id') == 'occ'
                  and occurrence.get('shot_id') == 'shot'
                  and occurrence.get('shot_revision_id') == 'shot-rev'
                  and occurrence.get('track') == 'picture'
                  and occurrence.get('placement', {}).get('track') == 'picture')
            check('occurrence timing shape', occurrence.get('placement', {}).get('start_ms') == 0
                  and occurrence.get('duration_ms') == 10000
                  and occurrence.get('source_offset') == 0 and occurrence.get('speed') == 1)

            internal_image = closure['internal_timeline_revisions'][0] if closure['internal_timeline_revisions'] else {}
            internal_payload = internal_image.get('payload', {})
            clips = internal_payload.get('clips', [])
            check('internal container/track order', [track.get('id') for track in internal_payload.get('tracks', [])]
                  == ['plate', 'type'])
            check('clip order and source window', [clip.get('id') for clip in clips] == ['video', 'title']
                  and clips[0].get('asset') == 'source' and clips[0].get('from') == 1
                  and clips[0].get('to') == 11 and clips[0].get('hold') == 10
                  and clips[1].get('at') == 1 and clips[1].get('hold') == 1)
            check('opaque fields', clips[0].get('params', {}).get('opaque') == [None, False, 1, 1.0]
                  and clips[1].get('params', {}).get('opaque') == {'keep': [None, False, 1, 1.0]})
            check('source registry mirror', internal_payload.get('registry') == payload.get('registry')
                  and payload.get('registry', {}).get('assets', {}).get('source', {}).get('type') == 'video'
                  and payload.get('registry', {}).get('assets', {}).get('source', {}).get('duration') == 12)

            manifest = closure.get('dependency_manifest', {})
            check('manifest shot/internal pins', manifest.get('shots') == [{
                key: closure['shot_revisions'][0][key]
                for key in ('shot_id', 'revision_id', 'internal_timeline_revision_id', 'content_digest')
            }] and manifest.get('internal_timelines') == [{
                key: closure['internal_timeline_revisions'][0][key]
                for key in ('timeline_id', 'revision_id', 'content_digest')
            }])
            source = payload.get('registry', {}).get('assets', {}).get('source', {})
            media_id = source.get('media_id')
            media_pins = manifest.get('media', [])
            check('manifest/source media mirror', isinstance(media_id, str)
                  and len(media_pins) == 1 and media_pins[0].get('media_id') == media_id
                  and media_pins[0].get('content_digest') == media_id)
            if isinstance(media_id, str):
                bare = media_id.removeprefix('sha256:')
                owned = service.store.conn.execute(
                    'SELECT 1 FROM objects o JOIN project_objects po ON po.digest=o.digest '
                    'WHERE o.digest=? AND po.project_id=?', (bare, project_id),
                ).fetchone()
                check('source object ownership', owned is not None)
                try:
                    check('source bytes/digest', 'sha256:' + hashlib.sha256(service.cas.read(bare)).hexdigest() == media_id)
                except Exception as exc:  # noqa: BLE001  (report all setup failures together)
                    failures.append(f'source read: {type(exc).__name__}: {exc}')

            shot = closure['shot_revisions'][0] if closure['shot_revisions'] else {}
            check('shot ownership/internal pin', shot.get('shot_id') == 'shot'
                  and shot.get('internal_timeline_revision_id') == 'internal-rev')
            shot_row = service.store.conn.execute(
                'SELECT project_id FROM shot_revisions WHERE id=? AND shot_id=?', ('shot-rev', 'shot'),
            ).fetchone()
            internal_row = service.store.conn.execute(
                'SELECT project_id, timeline_id FROM internal_timeline_revisions WHERE id=?', ('internal-rev',),
            ).fetchone()
            check('child revision ownership', shot_row is not None and shot_row['project_id'] == project_id)
            check('internal revision ownership', internal_row is not None
                  and internal_row['project_id'] == project_id and internal_row['timeline_id'] == 'film')
    finally:
        service.close()

    if failures:
        raise AssertionError('WC8 detached fixture preflight failed:\n- ' + '\n- '.join(failures))


@pytest.fixture
def historical_sheet_film(tmp_path, request):
    # Use PLAN's frozen Runtime main, through its real APIs in another process.
    # Current Runtime then performs its normal migration and history adoption.
    old_runtime = runtime_checkout('8c1830d1ca64a3934c37611a28ffe8db7df879ea')
    clips = [
        {'id': 'video', 'clipType': 'media', 'track': 'picture', 'at': 0,
         'asset': 'source', 'from': 1, 'to': 5.0, 'hold': 4, 'speed': 2,
         'params': {'opaque': [None, False, 1, 1.0]},
         'transition': {'type': 'crossfade', 'duration': .25},
         'app': {'org.example': {'literal': 'video', 'value': None}}},
        {'id': 'title', 'clipType': 'am-type', 'track': 'picture', 'at': 6, 'hold': 1.013,
         'params': {'text': 'Before', 'size': 32, 'font': 'display', 'color': '#25241F',
                   'opaque': {'keep': [None, False, 1, 1.0]}},
         'org.example/data': {'float': 1.0}},
    ]
    # Main's publication evaluator only accepts numeric FPS; rational-object
    # preservation is covered by the direct ordinary-sheet conformance tests.
    payload = {'config': {'output': {'fps': 30000 / 1001},
                         'tracks': [{'id': 'picture', 'kind': 'visual', 'label': 'Before'}],
                         'clips': copy.deepcopy(clips), 'org.example/data': {'null': None}},
               'clips': clips, 'occurrences': [], 'registry': {'assets': {}}}
    if getattr(request, 'param', None) == 'detached':
        clips[0].update(track='plate', at=0, hold=10, speed=1, **{'from': 1, 'to': 11},
                        app={'astrid': {'cut': 'c1', 'layer': 'plate'}})
        clips[1].update(track='type', at=1, hold=1,
                        app={'astrid': {'cut': 'c1', 'layer': 'card', 'for': 1}})
        payload['config']['clips'] = payload['clips'] = []
        payload['occurrences'] = [{'occurrence_id': 'occ', 'shot_id': 'shot',
            'shot_revision_id': 'shot-rev',
            'placement': {'start_ms': 0, 'track': 'picture'}, 'track': 'picture',
            'duration_ms': 10000, 'source_offset': 0, 'speed': 1}]
        payload['_internal'] = {'tracks': [{'id': 'plate', 'kind': 'visual'}, {'id': 'type', 'kind': 'visual'}],
                                'output': copy.deepcopy(payload['config']['output']), 'clips': clips}
    root = tmp_path / 'historical-realm'
    script = """
import json
import sys
from pathlib import Path
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
root = Path(sys.argv[1])
RealmStore.initialize(root).close()
service = RuntimeService(root)
try:
    project = service.create_project({'slug': 'ordinary-sheet', 'name': 'Ordinary sheet'})['id']
    service.create_timeline(project, 'film', idempotency_key='create-film')
    media = service.ingest(project, b'ordinary sheet source', media_type='video/mp4',
                           original_name='source.mp4', idempotency_key='source')['data']['object_id']
    payload = json.load(sys.stdin)
    internal = payload.pop('_internal', None)
    payload['registry']['assets']['source'] = {'media_id': media, 'type': 'video', 'duration': 12}
    shots, internals = [], []
    if internal is not None:
        internal['registry'] = payload['registry']
        shots = [{'shot_id': 'shot', 'revision_id': 'shot-rev',
                  'internal_timeline_revision_id': 'internal-rev', 'payload': {'name': 'Opening', 'items': []}}]
        internals = [{'timeline_id': 'film', 'revision_id': 'internal-rev', 'payload': internal}]
    service.publish_parent_composition(project, 'film', {
        'project_id': project, 'timeline_id': 'film', 'expected_head': None,
        'parent_revision_id': 'sheet-baseline', 'parent_composition': payload,
        'shot_revisions': shots, 'internal_timeline_revisions': internals,
    }, idempotency_key='seed-sheet')
    print(json.dumps({'project_id': project, 'realm_id': service.store.realm['id']}))
finally:
    service.close()
"""
    result = subprocess.run([sys.executable, '-c', script, str(root)], input=json.dumps(payload),
        cwd=tmp_path, env={**os.environ, 'PYTHONPATH': str(old_runtime)},
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    facts = json.loads(result.stdout)
    from runtime_protocol.upgrade import migrate_canonical_to_current

    migration = migrate_canonical_to_current(root, expected_realm_id=facts['realm_id'],
        confirmation='MIGRATE CANONICAL ' + facts['realm_id'])
    assert migration['ok']
    _preflight_detached_fixture(root, facts['project_id'])
    return root, facts['project_id']


def draft(runtime, tmp_path):
    session = runtime.session()
    sheet = NativeSheet.export(session)
    text = property_cell(sheet.text, MEDIA, 'trim', '2.000001..8.000002')
    for key in ('asset', 'hold', 'transition'):
        text = property_cell(text, MEDIA, key, 'clear')
    text = property_cell(text, TITLE, 'hold', '2.013')
    text = property_cell(text, TITLE, 'text', '""')
    text = property_cell(text, TITLE, 'size', 'clear')
    path = tmp_path / 'ordinary.sheet'
    path.write_text(text)
    return session, sheet, path


@pytest.mark.parametrize('runtime', ['historical'], indirect=True)
@pytest.mark.parametrize('peer', ['none', 'disjoint', 'trim', 'params'])
def test_http_trim_clear_params_original_basis_reload_undo_retry_or_kept_conflict(
        runtime, tmp_path, monkeypatch, peer):
    session, sheet, path = draft(runtime, tmp_path)
    original = copy.deepcopy(runtime.history()['head'])
    expected = sheet.preview(path.read_text())
    assert [c['op'] for c in expected.commands] == ['clip.trim', 'clip.set', 'clip.set', 'clip.set-params']
    assert sheet.preview(sheet.text).commands == []
    if peer != 'none':
        other = runtime.session(name='peer')
        if peer == 'disjoint':
            other.commit(label('Concurrent label'))
        elif peer == 'trim':
            other.commit(command('clip.trim', MEDIA, {'in_s': 1, 'out_s': 6}))
        else:
            other.commit(command('clip.set-params', TITLE, {'values': {'text': 'Concurrent text'}, 'clear': []}))
    before = session.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=runtime.history()['head']['revision_id']).data['bundle']
    draft_bytes = path.read_bytes()
    if peer in ('trim', 'params'):
        head = copy.deepcopy(runtime.history()['head'])
        with pytest.raises(CommitConflict):
            sheet.apply(path.read_text(), session=session, dry_run=False)
        state = json.loads(session.outbox.path.read_bytes())
        assert state['pending'] == expected.commands and state['flight'] and state['conflict']
        assert state['base'] == original and state['sheet']['basis'] == original
        assert runtime.history()['head'] == head and path.read_bytes() == draft_bytes
        return

    runtime.lost.add('ordinary-sheet')
    with pytest.raises(WorkspaceClientError):
        sheet.apply(path.read_text(), session=session, dry_run=False, idempotency_key='ordinary-sheet')
    first = copy.deepcopy(runtime.calls[-1][:2])
    body = json.loads(first[0])
    assert body['base_revision_id'] == original['revision_id']
    assert body['base_publication_id'] == original['publication_id']
    assert body['commands'] == expected.commands and body['source'] == {'via': 'sheet'}
    accepted_head = copy.deepcopy(runtime.history()['head'])
    history_count = len(runtime.history()['items'])
    runtime.restart()
    restarted = runtime.session()
    loaded = NativeSheet.load(restarted)
    assert loaded.text == sheet.text

    def forbidden(*args, **kwargs):
        pytest.fail('retry must retain the original capture without refetching')

    with monkeypatch.context() as retry_patch:
        retry_patch.setattr(TimelineSession, '_bundle', forbidden)
        result = loaded.apply(path.read_text(), session=restarted, dry_run=False)
    assert runtime.calls[-1][:2] == first
    assert runtime.history()['head'] == accepted_head and len(runtime.history()['items']) == history_count
    assert result['data']['status'] == ('rebased' if peer == 'disjoint' else 'accepted')
    actual = bundle_from_document(result['data']['canonical_document'])
    assert _json(State(actual).entity(MEDIA)) == _json(State(expected.bundle).entity(MEDIA))
    assert _json(State(actual).entity(TITLE)) == _json(State(expected.bundle).entity(TITLE))
    stored = restarted.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted_head['revision_id']).data['bundle']
    assert _json(State(stored).entity(MEDIA)) == _json(State(actual).entity(MEDIA))
    undone = restarted.undo([result['receipt']['receipt_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    for ref in (MEDIA, TITLE, 'parent/track:picture'):
        assert _json(State(restored).entity(ref)) == _json(State(before).entity(ref))
    assert restored['parent']['config']['output'] == before['parent']['config']['output']
    redone = restarted.undo([undone['receipt']['receipt_id']])
    assert _json(redone['data']['canonical_document']) == _json(result['data']['canonical_document'])
    assert path.read_bytes() == draft_bytes
    assert NativeSheet.load(restarted).text == sheet.text


@pytest.mark.parametrize('runtime', ['historical'], indirect=True)
@pytest.mark.parametrize('historical_sheet_film', ['detached'], indirect=True)
@pytest.mark.parametrize('peer', ['none', 'disjoint', 'same'])
def test_detached_duration_author_time_basis_through_original_save_and_runtime(
        runtime, historical_sheet_film, tmp_path, monkeypatch, peer):
    from astrid.sdk.timeline.checkout import _sheet_session
    from astrid.sdk.timeline_checkout import Checkout
    from astrid.sdk.timeline_sheet import apply_sheet, render_sheet

    client = runtime.client()
    assert historical_sheet_film[1] == runtime.project
    # Use the normal local draft entrypoint; the export retains native context.
    tl = Checkout.draft(runtime.project, 'film', client=client)
    text = render_sheet(tl, cuts=['c1'])
    edited = text.replace('for 1s', 'for 2s')
    assert edited != text
    path = tmp_path / 'detached.sheet'
    path.write_text(edited)
    session = _sheet_session(tl)
    original = json.loads(session.outbox.path.read_bytes())['sheet']
    ref = original['detached']['bindings']['c1.card']
    basis = original['basis']
    if peer != 'none':
        other = runtime.session(name='peer')
        other.commit(command('clip.set', ref, {'values': {'hold': 3}, 'clear': []})
                     if peer == 'same' else label('Concurrent'))
    before = client.timelines.open_bundle(runtime.project, 'film',
        revision_id=runtime.history()['head']['revision_id']).data['bundle']
    tl = Checkout.load(tl.path)
    assert apply_sheet(tl, path.read_text(), client=client)
    pending = json.loads(session.outbox.path.read_bytes())['pending']
    assert len(pending) == 1 and pending[0]['op'] == 'clip.set' and pending[0]['select'] == ref
    head = copy.deepcopy(runtime.history()['head'])
    if peer == 'same':
        with pytest.raises(CommitConflict):
            tl.save(quiet=True)
        state = json.loads(session.outbox.path.read_bytes())
        assert state['base'] == basis and state['sheet']['bundle'] == original['bundle']
        assert state['flight'] and state['pending'] == pending and state['conflict']
        assert Checkout.load(tl.path).clip('c1.card').duration == 2
        assert runtime.history()['head'] == head and path.read_text() == edited
        return
    # The save owns the ordinary flight key; lose its response after acceptance.
    from astrid.sdk import workspace_client
    real_commit = workspace_client.WorkspaceClient.commit_timeline
    lost = []
    def lose_ack(transport, *args, **kwargs):
        response = real_commit(transport, *args, **kwargs)
        if not lost:
            lost.append(True)
            raise WorkspaceClientError(0, 'unavailable', 'lost detached ACK', {})
        return response
    monkeypatch.setattr(workspace_client.WorkspaceClient, 'commit_timeline', lose_ack)
    with pytest.raises(WorkspaceClientError):
        tl.save(quiet=True)
    first = runtime.calls[-1][:2]
    assert json.loads(first[0])['base_revision_id'] == basis['revision_id']
    assert json.loads(first[0])['base_publication_id'] == basis['publication_id']
    accepted = runtime.history()['head']
    count = len(runtime.history()['items'])
    runtime.restart()
    tl = Checkout.load(tl.path)
    assert apply_sheet(tl, path.read_text(), client=runtime.client())
    with monkeypatch.context() as retry:
        retry.setattr(TimelineSession, '_bundle', lambda *a: pytest.fail('retry fetched a basis'))
        tl.save(quiet=True)
    assert runtime.calls[-1][:2] == first
    assert runtime.history()['head'] == accepted and len(runtime.history()['items']) == count
    after = runtime.client().timelines.open_bundle(runtime.project, 'film',
        revision_id=accepted['revision_id']).data['bundle']
    assert State(after).entity(ref)['hold'] == 2
    session = _sheet_session(tl)
    undone = session.undo([accepted['publication_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert _json(State(restored).entity(ref)) == _json(State(before).entity(ref))
    assert restored['parent'] == before['parent']
    redone = session.undo([undone['receipt']['receipt_id']])
    assert _json(State(bundle_from_document(redone['data']['canonical_document'])).entity(ref)) == _json(State(after).entity(ref))
    with pytest.raises(CommitConflict):
        session.undo([accepted['publication_id']])
    assert path.read_text() == edited


@pytest.mark.parametrize('runtime', ['historical'], indirect=True)
@pytest.mark.parametrize('historical_sheet_film', ['detached'], indirect=True)
def test_current014_detached_text_literal_uses_native_http_and_guarded_inverse(
        runtime, historical_sheet_film):
    from astrid.sdk.timeline.checkout import _sheet_session
    from astrid.sdk.timeline_checkout import Checkout
    from astrid.sdk.timeline_sheet import apply_sheet, render_sheet

    client = runtime.client()
    assert historical_sheet_film[1] == runtime.project
    tl = Checkout.draft(runtime.project, 'film', client=client)
    original_text = render_sheet(tl, cuts=['c1'])
    value = 'line\nnext C:\\tmp\\file \\1 — café "quoted"'
    edited = original_text.replace('"Before"', json.dumps(value, ensure_ascii=False), 1)
    assert edited != original_text and edited.count(json.dumps(value, ensure_ascii=False)) == 1

    session = _sheet_session(tl)
    artifact = json.loads(session.outbox.path.read_bytes())['sheet']
    bundle = artifact['bundle']
    ref = artifact['detached']['bindings']['c1.card']
    sibling = 'occurrence:occ/clip:video'
    before = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=runtime.history()['head']['revision_id']).data['bundle']
    expected = [capture_clip_set_params(bundle, ref, values={'text': value})]
    assert apply_sheet(tl, edited, client=client)
    pending = json.loads(session.outbox.path.read_bytes())['pending']
    assert pending == expected

    tl.save(quiet=True)
    request = json.loads(runtime.calls[-1][0])
    assert request['base_revision_id'] == artifact['basis']['revision_id']
    assert request['base_publication_id'] == artifact['basis']['publication_id']
    assert request['commands'] == expected and request['source'] == {'via': 'sheet'}
    accepted = copy.deepcopy(runtime.history()['head'])
    after = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    after_state = State(after)
    assert after_state.entity(ref)['params']['text'] == value
    assert after_state.entity(ref)['params']['opaque'] == {'keep': [None, False, 1, 1.0]}
    assert after_state.entity(sibling) == State(before).entity(sibling)

    runtime.restart()
    reloaded = runtime.session(name='current014-text-reloaded')
    reloaded_bundle = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    assert State(reloaded_bundle).entity(ref)['params']['text'] == value
    undone = reloaded.undo([accepted['publication_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert _json(State(restored).entity(ref)) == _json(State(before).entity(ref))
    assert State(restored).entity(sibling) == State(before).entity(sibling)
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    redone_bundle = bundle_from_document(redone['data']['canonical_document'])
    assert _json(State(redone_bundle).entity(ref)) == _json(State(after).entity(ref))


@pytest.mark.parametrize('runtime', ['historical'], indirect=True)
@pytest.mark.parametrize('historical_sheet_film', ['detached'], indirect=True)
def test_current014_detached_mixed_text_duration_uses_one_native_http_batch_and_guarded_inverse(
        runtime, historical_sheet_film):
    from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
    from astrid.sdk.timeline.checkout import _sheet_session
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline_checkout import Checkout
    from astrid.sdk.timeline_sheet import NativeSheet, apply_sheet, render_sheet

    client = runtime.client()
    assert historical_sheet_film[1] == runtime.project
    tl = Checkout.draft(runtime.project, 'film', client=client)
    original_text = render_sheet(tl, cuts=['c1'])
    value = 'line\nnext C:\\tmp\\file \\1 — café "quoted"'
    edited = original_text.replace('for 1s', 'for 2s').replace(
        '"Before"', json.dumps(value, ensure_ascii=False), 1)
    assert edited != original_text

    session = _sheet_session(tl)
    artifact = json.loads(session.outbox.path.read_bytes())['sheet']
    native = NativeSheet.load(session)
    bundle = artifact['bundle']
    ref = artifact['detached']['bindings']['c1.card']
    sibling = 'occurrence:occ/clip:video'
    basis = artifact['basis']
    assert native._bundle == bundle and native._basis == basis
    before = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=runtime.history()['head']['revision_id']).data['bundle']
    expected = execute(bundle, [
        capture_clip_set(bundle, ref, values={'hold': 2.0}),
        capture_clip_set_params(bundle, ref, values={'text': value}),
    ])
    assert expected.commands[0]['op'] == 'clip.set'
    assert expected.commands[1]['op'] == 'clip.set-params'

    assert apply_sheet(tl, edited, client=client)
    state = json.loads(session.outbox.path.read_bytes())
    assert state['sheet']['bundle'] == bundle and state['sheet']['basis'] == basis
    assert state['pending'] == expected.commands

    tl.save(quiet=True)
    request = json.loads(runtime.calls[-1][0])
    assert request['base_revision_id'] == basis['revision_id']
    assert request['base_publication_id'] == basis['publication_id']
    assert request['commands'] == expected.commands and request['source'] == {'via': 'sheet'}
    accepted = copy.deepcopy(runtime.history()['head'])
    after = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    after_state = State(after)
    assert after_state.entity(ref)['hold'] == 2.0
    assert after_state.entity(ref)['params']['text'] == value
    assert after_state.entity(ref)['params']['opaque'] == {'keep': [None, False, 1, 1.0]}
    assert after_state.entity(sibling) == State(before).entity(sibling)

    runtime.restart()
    reloaded = runtime.session(name='current014-mixed-reloaded')
    reloaded_bundle = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    reloaded_state = State(reloaded_bundle)
    assert reloaded_state.entity(ref)['hold'] == 2.0
    assert reloaded_state.entity(ref)['params']['text'] == value
    undone = reloaded.undo([accepted['publication_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert _json(State(restored).entity(ref)) == _json(State(before).entity(ref))
    assert State(restored).entity(sibling) == State(before).entity(sibling)
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    redone_bundle = bundle_from_document(redone['data']['canonical_document'])
    assert _json(State(redone_bundle).entity(ref)) == _json(State(after).entity(ref))
    assert State(redone_bundle).entity(sibling) == State(after).entity(sibling)
    with pytest.raises(CommitConflict):
        reloaded.undo([accepted['publication_id']])


@pytest.mark.parametrize('runtime', ['historical'], indirect=True)
@pytest.mark.parametrize('historical_sheet_film', ['detached'], indirect=True)
def test_current014_detached_size_clear_uses_one_native_http_commit_and_guarded_inverse(
        runtime, historical_sheet_film):
    from astrid.sdk.timeline.checkout import _sheet_session
    from astrid.sdk.timeline_checkout import Checkout
    from astrid.sdk.timeline_sheet import apply_sheet, render_sheet

    client = runtime.client()
    assert historical_sheet_film[1] == runtime.project
    tl = Checkout.draft(runtime.project, 'film', client=client)
    original_text = render_sheet(tl, cuts=['c1'])
    edited = original_text.replace('size=32', 'size=clear', 1)
    assert edited != original_text

    session = _sheet_session(tl)
    native = NativeSheet.load(session)
    artifact = json.loads(session.outbox.path.read_bytes())['sheet']
    bundle = artifact['bundle']
    basis = artifact['basis']
    ref = artifact['detached']['bindings']['c1.card']
    sibling = 'occurrence:occ/clip:video'
    before = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=runtime.history()['head']['revision_id']).data['bundle']
    expected = [capture_clip_set_params(bundle, ref, values={}, clear=['size'])]
    assert native._bundle == bundle and native._basis == basis and 'size=32' in native.text
    assert apply_sheet(tl, edited, client=client)
    assert json.loads(session.outbox.path.read_bytes())['pending'] == expected

    tl.save(quiet=True)
    assert len(runtime.calls) == 1
    request = json.loads(runtime.calls[-1][0])
    assert request['base_revision_id'] == basis['revision_id']
    assert request['base_publication_id'] == basis['publication_id']
    assert request['commands'] == expected and request['source'] == {'via': 'sheet'}
    accepted = copy.deepcopy(runtime.history()['head'])
    after = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    target = State(after).entity(ref)
    assert target['clipType'] == 'am-type' and target['track'] == 'type'
    assert target['params']['text'] == 'Before'
    assert target['params']['opaque'] == {'keep': [None, False, 1, 1.0]}
    assert target['hold'] == 1 and 'size' not in target['params']
    assert 'asset' not in target and 'from' not in target and 'to' not in target
    internal_clips = [clip for shot in after['shots'].values()
                      for clip in shot['internal_timeline']['clips']]
    assert [clip['id'] for clip in internal_clips] == ['video', 'title']
    assert State(after).entity(sibling) == State(before).entity(sibling)
    assert after['parent']['config']['org.example/data'] == {'null': None}

    runtime.restart()
    reloaded = runtime.session(name='current014-size-reloaded')
    reloaded_bundle = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    assert State(reloaded_bundle).entity(ref) == target
    undone = reloaded.undo([accepted['publication_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    restored_target = State(restored).entity(ref)
    assert restored_target['params']['size'] == 32
    assert _json(restored_target) == _json(State(before).entity(ref))
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    redone_bundle = bundle_from_document(redone['data']['canonical_document'])
    assert _json(State(redone_bundle).entity(ref)) == _json(target)


@pytest.mark.parametrize('runtime', ['historical'], indirect=True)
@pytest.mark.parametrize('historical_sheet_film', ['detached'], indirect=True)
def test_current014_detached_font_color_uses_one_native_http_commit_and_guarded_inverse(
        runtime, historical_sheet_film):
    from astrid.sdk.timeline.checkout import _sheet_session
    from astrid.sdk.timeline_checkout import Checkout
    from astrid.sdk.timeline_sheet import apply_sheet, render_sheet

    client = runtime.client()
    assert historical_sheet_film[1] == runtime.project
    tl = Checkout.draft(runtime.project, 'film', client=client)
    original_text = render_sheet(tl, cuts=['c1'])
    card_line = next(line for line in original_text.splitlines() if 'card' in line)
    assert 'color=#25241F font=display opaque={"keep":[null,false,1,1.0]} size=32' in card_line
    edited = (original_text.replace('size=32', 'size=48', 1)
              .replace('font=display', 'font=label', 1)
              .replace('color=#25241F', 'color="#FF6B23"', 1))
    assert edited != original_text
    assert b'font=label' in edited.encode() and b'color="#FF6B23"' in edited.encode()

    session = _sheet_session(tl)
    native = NativeSheet.load(session)
    artifact = json.loads(session.outbox.path.read_bytes())['sheet']
    bundle, basis = artifact['bundle'], artifact['basis']
    ref = artifact['detached']['bindings']['c1.card']
    sibling = 'occurrence:occ/clip:video'
    before = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=runtime.history()['head']['revision_id']).data['bundle']
    expected = [capture_clip_set_params(bundle, ref,
                                        values={'size': 48, 'font': 'label', 'color': '#FF6B23'})]
    assert native._bundle == bundle and native._basis == basis
    assert apply_sheet(tl, edited, client=client)
    assert json.loads(session.outbox.path.read_bytes())['pending'] == expected

    tl.save(quiet=True)
    request = json.loads(runtime.calls[-1][0])
    assert request['base_revision_id'] == basis['revision_id']
    assert request['base_publication_id'] == basis['publication_id']
    assert request['commands'] == expected and request['source'] == {'via': 'sheet'}
    accepted = copy.deepcopy(runtime.history()['head'])
    after = client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    target = State(after).entity(ref)
    before_target = State(before).entity(ref)
    assert list(target['params']) == list(before_target['params'])
    assert target['params']['size'] == 48 and target['params']['font'] == 'label'
    assert target['params']['color'] == '#FF6B23'
    assert target['params']['opaque'] == {'keep': [None, False, 1, 1.0]}
    assert 'asset' not in target and 'from' not in target and 'to' not in target
    assert [clip['id'] for shot in after['shots'].values()
            for clip in shot['internal_timeline']['clips']] == ['video', 'title']
    assert State(after).entity(sibling) == State(before).entity(sibling)
    assert after['parent']['config']['org.example/data'] == {'null': None}

    runtime.restart()
    reloaded = runtime.session(name='current014-font-color-reloaded')
    reloaded_bundle = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=accepted['revision_id']).data['bundle']
    assert State(reloaded_bundle).entity(ref) == target
    undone = reloaded.undo([accepted['publication_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert _json(State(restored).entity(ref)) == _json(State(before).entity(ref))
    assert State(restored).entity(sibling) == State(before).entity(sibling)
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    redone_bundle = bundle_from_document(redone['data']['canonical_document'])
    assert _json(State(redone_bundle).entity(ref)) == _json(target)
