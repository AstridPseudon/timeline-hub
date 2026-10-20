"""Ordinary pinned CLI/Python/sheet commands on authenticated Runtime HTTP.

Run only through the central test service. This uses the existing injected
transport, unmodified generated client and startup-loaded semantic provider.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from astrid.packs.timeline.cli import build_parser
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, _manifest, bundle_from_document
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline_sheet import NativeSheet
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance import test_native_batch_ingress
from tests.editing_conformance.test_native_batch_ingress import command, label
from tests.editing_conformance.test_native_sheet_current import property_cell
from tests.sdk.test_timeline_sheet_native import edit_cell, remove_row

pytestmark = pytest.mark.integration
runtime = test_native_batch_ingress.runtime
REF = 'parent/clip:title'
LEGACY_HELPER_COMMIT = '382f523ef957afb2bd299c5e21424ca821b23f05'
LEGACY_HELPER_SHA256 = '5e152bfa716b9003b831648cad16f6adb9c334cd18a6a7cf32a31accefe82617'


def run(runtime, *args):
    parsed = build_parser(runtime.client()).parse_args([*args, '--project', runtime.project, '--json'])
    return parsed.handler(parsed)


def export(runtime, capsys, tmp_path):
    assert run(runtime, 'show', 'film', '--as', 'sheet', '--native') == 0
    text = json.loads(capsys.readouterr().out)['data']['text']
    session = TimelineSession.open(runtime.project, 'film', client=runtime.client())
    sheet = NativeSheet.load(session)
    assert text == sheet.text
    text = edit_cell(text, REF, '3.017')
    text = property_cell(text, REF, 'hold', '2.013')
    text = property_cell(text, REF, 'transition', 'clear')
    text = property_cell(text, REF, 'text', '""')
    text = edit_cell(text, 'parent/track:picture', '""', label=True)
    path = tmp_path / 'sheet.txt'
    path.write_text(text)
    return session, sheet, path


def seed(runtime):
    runtime.session().commit_many([
        command('track.create', 'parent', {'row': {'id': 'picture', 'kind': 'visual', 'opaque': [None, True, 1]}}),
        label('Old'),
        command('clip.add', 'parent', {'row': {'id': 'title', 'clipType': 'am-type', 'track': 'picture',
            'at': .017, 'hold': 1.013, 'params': {'text': 'Original', 'opaque': {'keep': [None, False]}},
            'opaque': [None, False, 1], 'transition': {'type': 'crossfade', 'duration': .25}}}),
    ])


def raw():
    return [command('clip.move', REF, {'on': 3.017}),
            command('clip.set', REF, {'values': {'hold': 2.013}, 'clear': ['transition']}),
            command('clip.set-params', REF, {'values': {'text': ''}, 'clear': []}), label('')]


def trusted_legacy_parent(service, document):
    """Load Runtime's reviewed test-only storage seed without copying its code."""
    from tests.helpers.runtime import runtime_checkout

    helper_path = runtime_checkout(LEGACY_HELPER_COMMIT) / 'tests' / 'timeline_trusted_bootstrap.py'
    helper_bytes = helper_path.read_bytes()
    assert hashlib.sha256(helper_bytes).hexdigest() == LEGACY_HELPER_SHA256
    spec = importlib.util.spec_from_file_location('_runtime_trusted_bootstrap', helper_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.seed_trusted_legacy_parent(
        service, document, idempotency_key='native-sheet-legacy-cut-fixture')


def tiny_legacy_document(service, project):
    """Bind the existing Main tiny fixture to real Runtime media and Documents."""
    fixture_path = Path(__file__).parents[1] / 'fixtures' / 'timeline_editing' / 'tiny.json'
    source = json.loads(fixture_path.read_text())
    timeline = source['shots']['B']['internal_timeline']
    media_ids = {}
    for asset in ('P', 'Q', 'R'):
        result = service.ingest(
            project, f'timeline-tiny-{asset}'.encode(),
            media_type='application/octet-stream', original_name=f'tiny-{asset}',
            idempotency_key=f'native-sheet-legacy-media-{asset}')
        media_ids[asset] = result['data']['object_id']

    transcript_content = {
        'schema': 'media.transcript/v1',
        'media_id': media_ids['P'],
        'source_id': 'whisper',
        'segments': [{
            'id': 's2', 'start': 0.0, 'end': 1.0, 'text': 'Live now.',
            'words': [
                {'id': 'w-live', 'start': 0.1, 'end': 0.4, 'text': 'Live'},
                {'id': 'w-now', 'start': 0.5, 'end': 0.8, 'text': 'now'},
            ],
        }],
    }
    document_id = service._transcript_document_id(project, media_ids['P'], 'whisper')
    source_result = service.create_document(
        project,
        {'document_id': document_id, 'kind': 'media.transcript', 'content': transcript_content},
        idempotency_key='native-sheet-legacy-transcript',
    )
    transcript_pin = {
        'document_id': document_id,
        'version': source_result['data']['version'],
        'content_digest': _digest(transcript_content),
    }

    clips = copy.deepcopy(timeline['clips'])
    tracks = copy.deepcopy(timeline['tracks'])
    registry = copy.deepcopy(timeline['registry'])
    for asset, entry in registry['assets'].items():
        entry['media_id'] = media_ids[asset]
    group_clips = [row for row in clips if row['id'] == 'b-type']
    group = {
        'shotId': 'legacy-c2', 'trackId': 'type',
        'clipIds': [row['id'] for row in group_clips], 'mode': 'images',
        'items': [], 'imageClipSnapshot': copy.deepcopy(group_clips),
    }
    payload = {
        'config': {
            'clips': copy.deepcopy(clips), 'tracks': tracks,
            'output': {'fps': {'numerator': 30000, 'denominator': 1001}, 'opaque': None},
            'pinnedShotGroups': [group], 'parent_only': {'audio': [None]},
        },
        'clips': clips, 'occurrences': [], 'opaque': {'fixture': 'timeline_editing/tiny.json'},
        'registry': registry,
    }
    return {
        'schema_version': 1, 'project_id': project, 'timeline_id': 'film',
        'parent_revision': {
            'revision_id': 'legacy-tiny-parent', 'payload': payload,
            'content_digest': _digest(payload),
        },
        'shot_revisions': [], 'internal_timeline_revisions': [],
        'dependency_manifest': _manifest(
            [], [],
            [{'media_id': media_ids[asset], 'content_digest': media_ids[asset]}
             for asset in ('P', 'Q', 'R')],
            [transcript_pin],
        ),
    }


def test_http_omitted_native_clip_row_delete_retries_rebases_and_refuses_changed_selection(
        runtime, capsys):
    target, sibling = 'parent/clip:title-a', 'parent/clip:title-b'
    runtime.session().commit_many([
        command('track.create', 'parent', {'row': {'id': 'picture', 'kind': 'visual', 'opaque': [None, True, 1]}}),
        label('Old'),
        command('clip.add', 'parent', {'row': {
            'id': 'title-a', 'clipType': 'am-type', 'track': 'picture', 'at': .017, 'hold': 1.013,
            'params': {'text': 'Same title'}, 'opaque': {'a': [None, False, 1]}}}),
        command('clip.add', 'parent', {'row': {
            'id': 'title-b', 'clipType': 'am-type', 'track': 'picture', 'at': 2.017, 'hold': 1.013,
            'params': {'text': 'Same title'}, 'opaque': {'b': [None, False, 2]}}}),
    ])
    assert run(runtime, 'show', 'film', '--as', 'sheet', '--native') == 0
    text = json.loads(capsys.readouterr().out)['data']['text']
    session = TimelineSession.open(runtime.project, 'film', client=runtime.client())
    sheet = NativeSheet.load(session)
    assert text == sheet.text and f'"{target}"' in text and f'"{sibling}"' in text
    original = copy.deepcopy(sheet._bundle)
    edited = remove_row(sheet.text, target)
    assert [row['id'] for row in original['parent']['clips']] == ['title-a', 'title-b']
    assert State(original).entity(target)['params'] == State(original).entity(sibling)['params']
    expected = sheet.preview(edited)
    assert [item['op'] for item in expected.commands] == ['clip.delete']

    runtime.lost.add('delete-once')
    with pytest.raises(WorkspaceClientError):
        sheet.apply(edited, session=session, dry_run=False, idempotency_key='delete-once')
    first = copy.deepcopy(runtime.calls[-1][:2])
    runtime.restart()
    reloaded = TimelineSession.open(runtime.project, 'film', client=runtime.client())
    result = NativeSheet.load(reloaded).apply(edited, session=reloaded, dry_run=False)
    assert runtime.calls[-1][:2] == first
    stored = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=result['data']['accepted_revision_id']).data['bundle']
    assert [row['id'] for row in stored['parent']['clips']] == ['title-b']
    assert State(stored).entity(sibling) == State(original).entity(sibling)
    undone = reloaded.undo([result['receipt']['receipt_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert [row['id'] for row in restored['parent']['clips']] == ['title-a', 'title-b']
    assert State(restored).entity(sibling) == State(original).entity(sibling)
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    assert redone['data']['canonical_document'] == result['data']['canonical_document']
    reloaded.undo([redone['receipt']['receipt_id']])

    old = NativeSheet.export(reloaded)
    old_edit = remove_row(old.text, target)
    runtime.session(name='peer').commit(command('clip.set-params', sibling,
                                                {'values': {'text': 'Peer edit'}, 'clear': []}))
    rebased = old.apply(old_edit, session=reloaded, dry_run=False)
    rebased_bundle = bundle_from_document(rebased['data']['canonical_document'])
    assert rebased['data']['status'] == 'rebased'
    assert State(rebased_bundle).entity(sibling)['params']['text'] == 'Peer edit'
    reloaded.undo([rebased['receipt']['receipt_id']])

    membership = runtime.session(name='membership')
    membership_sheet = NativeSheet.export(membership)
    runtime.session(name='membership-peer').commit(command('clip.add', 'parent', {'row': {
        'id': 'title-c', 'clipType': 'am-type', 'track': 'picture', 'at': 4.017, 'hold': 1.013,
        'params': {'text': 'Another title'}}}))
    head = copy.deepcopy(runtime.history()['head'])
    count = len(runtime.history()['items'])
    with pytest.raises(CommitConflict):
        membership_sheet.apply(remove_row(membership_sheet.text, target), session=membership, dry_run=False)
    assert runtime.history()['head'] == head and len(runtime.history()['items']) == count

    selected = runtime.session(name='selected')
    selected_sheet = NativeSheet.export(selected)
    runtime.session(name='selected-peer').commit(command('clip.delete', target, {}))
    head = copy.deepcopy(runtime.history()['head'])
    count = len(runtime.history()['items'])
    with pytest.raises(CommitConflict):
        selected_sheet.apply(remove_row(selected_sheet.text, target), session=selected, dry_run=False)
    assert runtime.history()['head'] == head and len(runtime.history()['items']) == count


def test_http_legacy_cut_native_for_admits_rebases_reads_and_undoes(runtime, monkeypatch):
    service = runtime.service()
    document = tiny_legacy_document(service, runtime.project)
    original_target = copy.deepcopy(
        next(row for row in document['parent_revision']['payload']['clips'] if row['id'] == 'b-type'))
    setup = trusted_legacy_parent(service, document)

    # Restart and open through the authenticated public SDK before making any edit.
    runtime.restart()
    session = runtime.session(name='legacy-native')
    admitted = session.client.timelines.open_bundle(runtime.project, 'film')
    assert admitted.ok
    admitted_target = State(admitted.data['bundle']).entity('parent/clip:b-type')
    assert admitted_target == original_target
    assert admitted.data['bundle']['parent']['config']['clips'] == document['parent_revision']['payload']['clips']
    assert runtime.history()['head']['revision_id'] == setup['data']['accepted_revision_id']
    assert len(runtime.history()['items']) == 2

    monkeypatch.setattr(Checkout, 'save', lambda *args, **kwargs: pytest.fail('legacy save'))
    monkeypatch.setattr(Checkout, '__init__', lambda *args, **kwargs: pytest.fail('legacy projection'))
    sheet = NativeSheet.export(session)
    target = 'parent/clip:b-type'
    edited = property_cell(sheet.text, target, 'hold', '1.5')
    plan = sheet.preview(edited)
    assert plan.commands == [
        capture_clip_set(sheet._bundle, target, values={'hold': 1.5}),
    ]
    assert State(plan.bundle).entity(target)['app'] == {
        'cut': 'c2', 'layer': 'card', 'for': 1.5,
    }

    peer = runtime.session(name='legacy-native-peer')
    peer.commit(label('Peer', track='type'))
    result = sheet.apply(edited, session=session, dry_run=False)
    assert result['data']['status'] == 'rebased'
    assert len(runtime.calls) == 2
    request = json.loads(runtime.calls[-1][0])
    assert request['commands'] == plan.commands
    accepted = bundle_from_document(result['data']['canonical_document'])
    assert State(accepted).entity(target)['app'] == {
        'cut': 'c2', 'layer': 'card', 'for': 1.5,
    }
    assert State(accepted).entity('parent/track:type')['label'] == 'Peer'

    runtime.restart()
    reloaded = runtime.session(name='legacy-native-reloaded')
    stored = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=result['data']['accepted_revision_id'])
    assert stored.ok
    stored_state = State(stored.data['bundle'])
    assert stored_state.entity(target)['app'] == {
        'cut': 'c2', 'layer': 'card', 'for': 1.5,
    }
    assert stored_state.entity('parent/track:type')['label'] == 'Peer'

    undone = reloaded.undo([result['receipt']['receipt_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert State(restored).entity(target) == original_target
    assert State(restored).entity('parent/track:type')['label'] == 'Peer'


@pytest.mark.parametrize('entry', ['python', 'cli', 'sheet-python', 'sheet-cli'])
def test_http_semantic_batch_original_pins_reload_inverse_redo(runtime, tmp_path, capsys, entry):
    seed(runtime)
    session, sheet, path = export(runtime, capsys, tmp_path)
    head = copy.deepcopy(runtime.history()['head'])
    before = session.client.timelines.open_bundle(runtime.project, 'film', revision_id=head['revision_id']).data['bundle']
    expected = execute(before, raw())
    assert sheet.preview(path.read_text()).commands == expected.commands
    if entry == 'python':
        result = session.commit_many(raw())
    elif entry == 'cli':
        path = tmp_path / 'commands.json'
        path.write_text(json.dumps(raw()))
        assert run(runtime, 'edit', 'commands-file', 'film', str(path),
                   '--base-revision-id', head['revision_id'], '--base-publication-id', head['publication_id']) == 0
        result = json.loads(capsys.readouterr().out)
    elif entry == 'sheet-python':
        result = sheet.apply(path.read_text(), session=session, dry_run=False)
    else:
        assert run(runtime, 'apply', 'film', str(path), '--native') == 0
        result = json.loads(capsys.readouterr().out)
    body = json.loads(runtime.calls[-1][0])
    assert body['base_revision_id'] == head['revision_id'] and body['base_publication_id'] == head['publication_id']
    assert body['commands'] == expected.commands
    actual = bundle_from_document(result['data']['canonical_document'])
    assert State(actual).entity(REF) == State(expected.bundle).entity(REF)
    assert len(runtime.history()['items']) == 3
    runtime.restart()
    reloaded = TimelineSession.open(runtime.project, 'film', client=runtime.client())
    stored = reloaded.client.timelines.open_bundle(runtime.project, 'film', revision_id=result['data']['accepted_revision_id'])
    assert State(stored.data['bundle']).entity(REF) == State(expected.bundle).entity(REF)
    undone = reloaded.undo([result['receipt']['receipt_id']])
    assert State(bundle_from_document(undone['data']['canonical_document'])).entity(REF) == State(before).entity(REF)
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    assert redone['data']['canonical_document'] == result['data']['canonical_document']


def test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba(runtime, tmp_path, capsys, monkeypatch):
    seed(runtime)
    session, sheet, path = export(runtime, capsys, tmp_path)
    runtime.lost.add('sheet-once')
    assert run(runtime, 'apply', 'film', str(path), '--native', '--idempotency-key', 'sheet-once') == 1
    assert 'edited sheet kept' in capsys.readouterr().out
    first = copy.deepcopy(runtime.calls[-1][:2])
    durable = session.outbox.path.read_bytes()
    runtime.restart()
    assert run(runtime, 'apply', 'film', str(path), '--native', '--idempotency-key', 'changed') == 1
    assert 'immutable' in capsys.readouterr().out
    assert session.outbox.path.read_bytes() == durable
    before = path.read_text()
    path.write_text(property_cell(before, REF, 'hold', '4.013'))
    assert run(runtime, 'apply', 'film', str(path), '--native') == 1
    assert 'pending intent' in capsys.readouterr().out
    assert session.outbox.path.read_bytes() == durable
    path.write_text(before)

    def no_read(*args, **kwargs):
        pytest.fail('retry must not recapture or read the bundle')

    with monkeypatch.context() as retry_patch:
        retry_patch.setattr(TimelineSession, '_bundle', no_read)
        assert run(runtime, 'apply', 'film', str(path), '--native') == 0
        accepted = json.loads(capsys.readouterr().out)
        assert runtime.calls[-1][:2] == first and len(runtime.history()['items']) == 3
    peer = runtime.session(name='peer')
    peer.commit(label('away'))
    peer.commit(label(''))
    current = copy.deepcopy(runtime.history()['head'])
    assert run(runtime, 'undo', 'film', '--publication', accepted['receipt']['receipt_id']) == 1
    assert 'intervening' in capsys.readouterr().out
    assert runtime.history()['head'] == current
    assert path.read_text() == before
    assert sheet.preview(path.read_text()).commands == json.loads(first[0])['commands']
