"""Ordinary pinned CLI/Python/sheet commands on authenticated Runtime HTTP.

Run only through the central test service. This uses the existing injected
transport, unmodified generated client and startup-loaded semantic provider.
"""
from __future__ import annotations

import copy
import json

import pytest

from astrid.packs.timeline.cli import build_parser
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance import test_native_batch_ingress
from tests.editing_conformance.test_native_batch_ingress import command, label
from tests.editing_conformance.test_native_sheet_current import property_cell
from tests.sdk.test_timeline_sheet_native import edit_cell, remove_row

pytestmark = pytest.mark.integration
runtime = test_native_batch_ingress.runtime
REF = 'parent/clip:title'


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


@pytest.mark.parametrize('entry', ['python', 'cli', 'sheet-python', 'sheet-cli', 'sheet-cli-default'])
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
    elif entry == 'sheet-cli':
        assert run(runtime, 'apply', 'film', str(path), '--native') == 0
        result = json.loads(capsys.readouterr().out)
    else:
        assert run(runtime, 'apply', 'film', str(path)) == 0
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


def test_http_unbound_legacy_sheet_refuses_without_legacy_save(runtime, tmp_path, capsys):
    path = tmp_path / 'legacy.sheet'
    text = 'film "p" · "film"\nlines\n  s1  "draft"\n'
    path.write_text(text)
    before_calls = copy.deepcopy(runtime.calls)

    assert run(runtime, 'apply', 'film', str(path)) == 1
    output = json.loads(capsys.readouterr().out)
    assert 'no original native sheet export' in output['error']['message']
    assert 'edited sheet kept' in output['error']['message']
    assert path.read_text() == text
    assert runtime.calls == before_calls


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
