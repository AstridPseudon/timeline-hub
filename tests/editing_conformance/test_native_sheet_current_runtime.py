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
from astrid.sdk.timeline.sync import TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet
from tests.editing_conformance import test_native_batch_ingress
from tests.editing_conformance.test_native_batch_ingress import command, label
from tests.editing_conformance.test_native_sheet_current import property_cell
from tests.sdk.test_timeline_sheet_native import edit_cell

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
