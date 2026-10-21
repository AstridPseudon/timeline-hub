"""Ordinary pinned CLI/Python/sheet commands on authenticated Runtime HTTP.

Run only through the central test service. This uses the existing injected
transport, unmodified generated client and startup-loaded semantic provider.
"""
from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from astrid.core.timeline.duration import clip_end_frame, clip_start_frame
from astrid.packs.timeline.cli import build_parser
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._track_commands import capture_track_set
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.document_diff import DocumentDiffError, document_diff_to_commands
from astrid.sdk.timeline.sync import CommitConflict, TimelineSession
from astrid.sdk.timeline_sheet import NativeSheet
from astrid.sdk.workspace_client import WorkspaceClientError
from tests.editing_conformance import test_native_batch_ingress
from tests.editing_conformance.test_native_batch_ingress import command, label
from tests.editing_conformance.test_native_sheet_current import property_cell
from tests.editing_conformance.test_recipe_clip_scalar_fields import app_closure
from tests.helpers.trusted_seed import seed_trusted_parent
from tests.sdk.test_timeline_sheet_native import edit_cell, remove_row

pytestmark = pytest.mark.integration
runtime = test_native_batch_ingress.runtime
REF = 'parent/clip:title'
RATIONAL_FPS = {'numerator': 30000, 'denominator': 1001}
RATIONAL_FPS_VALUE = Fraction(30000, 1001)
RATIONAL_LATTICE_SECONDS = 1.001
RATIONAL_TARGET = 'parent/clip:b-plate'
OCCURRENCE_TARGET = 'occurrence:f2-occurrence/clip:f2-agent-clip'
OCCURRENCE_CLEAR = 'occurrence:f2-occurrence/clip:f2-agent-clear-clip'
OCCURRENCE_SIBLING = 'occurrence:shared-sibling/clip:f2-agent-clip'
OCCURRENCE_GLOBAL_ON = 9


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


def tiny_cut_parent(service, project):
    """Build the saved cut-owned parent from the existing tiny sheet fixture."""
    source = json.loads((Path(__file__).parents[1] / 'fixtures' / 'timeline_editing' / 'tiny.json').read_text())
    timeline = source['shots']['B']['internal_timeline']
    media_ids = {}
    for asset in ('P', 'Q'):
        result = service.ingest(
            project, f'native-sheet-cut-{asset}'.encode(), media_type='application/octet-stream',
            original_name=f'native-sheet-cut-{asset}', idempotency_key=f'native-sheet-cut-media-{asset}',
        )
        media_ids[asset] = result['data']['object_id']

    clips = copy.deepcopy(timeline['clips'])
    registry = copy.deepcopy(timeline['registry'])
    for asset, entry in registry['assets'].items():
        if asset in media_ids:
            entry['media_id'] = media_ids[asset]
    tracks = copy.deepcopy(timeline['tracks'])
    payload = {
        'config': {
            'clips': copy.deepcopy(clips),
            'tracks': tracks,
            'output': {'fps': {'numerator': 30000, 'denominator': 1001}},
        },
        'clips': clips,
        'occurrences': [],
        'registry': registry,
    }
    return {
        'project_id': project,
        'timeline_id': 'film',
        'parent_revision_id': 'native-sheet-cut-parent-v1',
        'parent_composition': payload,
        'shot_revisions': [],
        'internal_timeline_revisions': [],
        'expected_head': None,
    }


def seed_tiny_cut_parent(runtime):
    document = tiny_cut_parent(runtime.service(), runtime.project)
    target = copy.deepcopy(next(row for row in document['parent_composition']['clips']
                               if row['id'] == 'b-type'))
    receipt = seed_trusted_parent(runtime.service(), document, idempotency_key='native-sheet-cut-parent')
    return document, target, receipt


def seed_labeled_tiny_cut_parent(runtime):
    """Use the real tiny closure while giving the label-clear edit a prior value."""
    document = tiny_cut_parent(runtime.service(), runtime.project)
    payload = document['parent_composition']
    track = next(row for row in payload['config']['tracks'] if row['id'] == 'plate')
    track['label'] = 'Source'
    clip = next(row for row in payload['clips'] if row['id'] == 'b-plate')
    clip['opaque'] = {'source_token': ['fixture', None, False, 7]}
    payload['config']['clips'] = copy.deepcopy(payload['clips'])
    receipt = seed_trusted_parent(runtime.service(), document, idempotency_key='native-sheet-label-parent')
    return document, receipt


def seed_rational_tiny_cut_parent(runtime):
    """Create a retained media-bearing closure whose move is exactly frame-aligned."""
    document = tiny_cut_parent(runtime.service(), runtime.project)
    payload = document['parent_composition']
    payload['config']['output'] = copy.deepcopy(RATIONAL_FPS)
    target = next(row for row in payload['clips'] if row['id'] == 'b-plate')
    target['hold'] = RATIONAL_LATTICE_SECONDS
    target['opaque'] = {'retained_source': ['fixture', None, False, 7]}
    payload['config']['clips'] = copy.deepcopy(payload['clips'])
    receipt = seed_trusted_parent(runtime.service(), document, idempotency_key='native-sheet-rational-parent')
    return document, receipt


def _replace_media_ids(value, replacements):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ('media_id', 'content_sha256', 'object_id') and child in replacements:
                value[key] = replacements[child]
            else:
                _replace_media_ids(child, replacements)
    elif isinstance(value, list):
        for child in value:
            _replace_media_ids(child, replacements)


def seed_shared_occurrence_parent(runtime, *, prepare=None, identity_scope=None):
    """Seed the existing shared-source App closure at the real Runtime boundary."""
    parent, shots, internals = app_closure()
    project = runtime.project
    media_ids = set()

    def collect(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ('media_id', 'object_id') and isinstance(child, str):
                    media_ids.add(child)
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect([parent, *shots, *internals])
    replacements = {}
    for index, source_id in enumerate(sorted(media_ids)):
        ingested = runtime.service().ingest(
            project, f'connected-occurrence-source-{index}'.encode(),
            media_type='application/octet-stream',
            original_name=f'connected-occurrence-source-{index}',
            idempotency_key=f'connected-occurrence-source-{index}',
        )
        replacements[source_id] = ingested['data']['object_id']
    _replace_media_ids(parent, replacements)
    _replace_media_ids(shots, replacements)
    _replace_media_ids(internals, replacements)

    parent_revision_id = 'native-sheet-connected-occurrence-parent'
    if identity_scope is not None:
        shot = shots[0]
        old_shot_id = shot['shot_id']
        old_shot_revision_id = shot['revision_id']
        old_internal_revision_id = shot['internal_timeline_revision_id']
        shot_id = f'{identity_scope}-shot'
        shot_revision_id = f'{identity_scope}-shot-revision'
        internal_revision_id = f'{identity_scope}-internal-revision'
        for occurrence in parent['payload']['occurrences']:
            if occurrence['shot_id'] == old_shot_id:
                occurrence['shot_id'] = shot_id
            if occurrence['shot_revision_id'] == old_shot_revision_id:
                occurrence['shot_revision_id'] = shot_revision_id
        shot['shot_id'] = shot_id
        shot['revision_id'] = shot_revision_id
        shot['internal_timeline_revision_id'] = internal_revision_id
        shot['payload']['internal_timeline_revision_id'] = internal_revision_id
        internal = next(item for item in internals if item['revision_id'] == old_internal_revision_id)
        internal['revision_id'] = internal_revision_id
        parent_revision_id = f'{identity_scope}-parent-revision'

    if prepare is not None:
        prepare(parent, shots, internals)

    parent['project_id'] = project
    parent['timeline_id'] = 'film'
    for image in [*shots, *internals]:
        image['project_id'] = project
    for image in internals:
        image['timeline_id'] = 'film'
    document = {
        'project_id': project,
        'timeline_id': 'film',
        'expected_head': None,
        'parent_revision_id': parent_revision_id,
        'parent_composition': parent['payload'],
        'shot_revisions': shots,
        'internal_timeline_revisions': internals,
    }
    seed_key = (f'{identity_scope}-seed' if identity_scope is not None
                else 'native-sheet-connected-occurrence-parent')
    receipt = seed_trusted_parent(runtime.service(), document, idempotency_key=seed_key)
    return document, receipt


def seed_document_diff_parent(runtime):
    """Seed real App-shaped rows with the native document-diff scalar carriers."""
    def prepare(parent, shots, internals):
        parent_rows = parent['payload']['clips']
        for rows in (parent_rows, parent['payload']['config']['clips']):
            next(row for row in rows if row['id'] == 'f2-app-clip').update(hold=3)
        child = next(row for row in internals[0]['payload']['clips']
                     if row['id'] == 'f2-agent-clip')
        child.update({'clipType': 'am-type', 'from': 0, 'to': 3, 'params': {'text': 'hello'}})
        child.pop('asset', None)

    return seed_shared_occurrence_parent(
        runtime, prepare=prepare, identity_scope=f'document-diff-{runtime.project}',
    )


def test_http_document_diff_null_presence_and_track_roundtrip_is_authenticated(runtime):
    _document, setup = seed_document_diff_parent(runtime)
    runtime.restart()
    session = runtime.session(name='document-diff')
    loaded = session.client.timelines.open_bundle(runtime.project, 'film')
    assert loaded.ok
    before = loaded.data['bundle']
    assert setup['data']['accepted_revision_id'] == runtime.history()['head']['revision_id']
    source = occurrence_source_pin(before, OCCURRENCE_TARGET)
    assert source['text_bindings'] == [{'slot': 'voiceover', 'text': 'hello'}]

    def child(candidate):
        shot = next(iter(candidate['shots'].values()))
        return next(row for row in shot['internal_timeline']['clips']
                    if row['id'] == 'f2-agent-clip')

    unsupported = copy.deepcopy(before)
    child(unsupported)['params']['null'] = None
    head_before_refusal = copy.deepcopy(runtime.history()['head'])
    calls_before_refusal = len(runtime.calls)
    with pytest.raises(DocumentDiffError, match='undeclared params'):
        document_diff_to_commands(unsupported, before)
    assert runtime.history()['head'] == head_before_refusal
    assert len(runtime.calls) == calls_before_refusal

    candidate = copy.deepcopy(before)
    for rows in (candidate['parent']['clips'], candidate['parent']['config']['clips']):
        next(row for row in rows if row['id'] == 'f2-app-clip').pop('hold')
    edited_child = child(candidate)
    edited_child.pop('hold')
    edited_child['params'] = {}
    candidate['parent']['config']['tracks'][0]['label'] = 'Renamed'

    native = document_diff_to_commands(candidate, before)
    assert [command['op'] for command in native['commands']] == [
        'track.set', 'clip.set', 'clip.set-params', 'clip.set',
    ]
    result = session.commit_many(native['commands'], idempotency_key='document-diff-roundtrip')
    assert result['data']['commands'] == native['commands']
    body = json.loads(runtime.calls[-1][0])
    assert body['commands'] == native['commands']
    assert body['source'] == {'via': 'python'}

    # ``open_bundle`` and the native diff result are intentionally detached.
    # The accepted setup document is the exact original base/publication and
    # carries the private compilation context required by the pure projector.
    original_document = setup['data']['canonical_document']
    original = bundle_from_document(original_document)
    assert persisted_bundle(original) == persisted_bundle(before)
    expected_input = copy.deepcopy(native['bundle'])
    expected_input['source_mapping']['_runtime_document'] = copy.deepcopy(
        original['source_mapping']['_runtime_document'])
    expected_document = document_from_bundle(expected_input)
    assert result['data']['canonical_document'] == expected_document
    accepted = bundle_from_document(result['data']['canonical_document'])
    expected = bundle_from_document(expected_document)
    assert persisted_bundle(accepted) == persisted_bundle(expected)
    accepted_parent = next(row for row in accepted['parent']['clips'] if row['id'] == 'f2-app-clip')
    accepted_child = State(accepted).entity(OCCURRENCE_TARGET)
    assert 'hold' not in accepted_parent and accepted_parent['from'] == 0 and accepted_parent['to'] == 3
    assert 'hold' not in accepted_child and accepted_child['from'] == 0 and accepted_child['to'] == 3
    assert accepted_child['params'] == {}
    assert accepted_child['app'] == {'f2Opaque': {'owner': 'f2', 'nested': [1, {'k': 'v'}]}}
    assert accepted['parent']['config']['tracks'][0]['label'] == 'Renamed'
    assert accepted['parent']['config']['x_f2_opaque'] == before['parent']['config']['x_f2_opaque']
    # Compile materialization gives only the edited occurrence its fresh expected source pin.
    assert occurrence_source_pin(accepted, OCCURRENCE_TARGET) == occurrence_source_pin(
        expected, OCCURRENCE_TARGET)
    target_pin = occurrence_source_pin(accepted, OCCURRENCE_TARGET)
    sibling_pin = occurrence_source_pin(accepted, OCCURRENCE_SIBLING)
    assert target_pin['shot_id'] != source['shot_id']
    assert target_pin['revision_id'] != source['revision_id']
    assert target_pin['internal_timeline_revision_id'] != source['internal_timeline_revision_id']
    assert sibling_pin == occurrence_source_pin(before, OCCURRENCE_SIBLING)
    assert State(accepted).entity(OCCURRENCE_SIBLING) == State(before).entity(OCCURRENCE_SIBLING)
    before_occurrences = {row['occurrence_id']: row for row in before['placements']}
    for row in accepted['placements']:
        original = before_occurrences[row['occurrence_id']]
        assert {key: row[key] for key in ('placement', 'source_offset', 'duration_ms', 'speed', 'track')} == {
            key: original[key] for key in ('placement', 'source_offset', 'duration_ms', 'speed', 'track')
        }

    history = runtime.history()
    assert history['head']['revision_id'] == result['data']['accepted_revision_id']
    entry = next(item for item in history['items']
                 if item['publication_id'] == result['receipt']['receipt_id'])
    assert entry['records']['commands'] == result['data']['records']['commands']

    runtime.restart()
    reloaded = runtime.session(name='document-diff-reloaded')
    stored = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=result['data']['accepted_revision_id'],
    )
    assert stored.ok
    assert persisted_bundle(stored.data['bundle']) == persisted_bundle(accepted)
    # Reload preserves the accepted materialized source pin for the edited occurrence.
    assert occurrence_source_pin(stored.data['bundle'], OCCURRENCE_TARGET) == target_pin

    undone = reloaded.undo([result['receipt']['receipt_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert State(restored).entity(OCCURRENCE_TARGET) == State(before).entity(OCCURRENCE_TARGET)
    assert State(restored).entity(OCCURRENCE_SIBLING) == State(before).entity(OCCURRENCE_SIBLING)
    assert occurrence_source_pin(restored, OCCURRENCE_TARGET) == source
    assert restored['parent']['config']['x_f2_opaque'] == before['parent']['config']['x_f2_opaque']
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    assert redone['data']['canonical_document'] == result['data']['canonical_document']


def occurrence_source_pin(bundle, ref):
    owner = ref.rsplit('/', 1)[0]
    occurrence = next(row for row in bundle['placements']
                      if 'occurrence:' + row['occurrence_id'] == owner)
    shot_id = occurrence['shot_id']
    source = bundle['source_mapping']['shots'][shot_id]
    return {
        'shot_id': source['shot_id'],
        'revision_id': source['revision_id'],
        'internal_timeline_revision_id': source['internal_timeline_revision_id'],
        'internal_timeline_id': source['internal_timeline_id'],
        'text_bindings': copy.deepcopy(bundle['shots'][shot_id]['payload']['text_bindings']),
    }


def persisted_bundle(bundle):
    """Drop the in-memory Runtime document hint before comparing persisted closure state."""
    value = copy.deepcopy(bundle)
    value.get('source_mapping', {}).pop('_runtime_document', None)
    return value


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


def test_http_cut_owned_native_sheet_hold_reloads_and_undoes(runtime):
    document, original_target, setup = seed_tiny_cut_parent(runtime)

    # The seed is setup-only. The edit starts after a normal Runtime restart and
    # reads the accepted closure through the authenticated public client.
    runtime.restart()
    session = runtime.session(name='cut-owned-native')
    admitted = session.client.timelines.open_bundle(runtime.project, 'film')
    assert admitted.ok
    admitted_bundle = admitted.data['bundle']
    assert State(admitted_bundle).entity('parent/clip:b-type') == original_target
    assert admitted_bundle['parent']['config']['clips'] == document['parent_composition']['clips']
    assert runtime.history()['head']['revision_id'] == setup['data']['accepted_revision_id']
    assert len(runtime.history()['items']) == 2

    sheet = NativeSheet.export(session)
    target = 'parent/clip:b-type'
    edited = property_cell(sheet.text, target, 'hold', '1.5')
    plan = sheet.preview(edited)
    assert plan.commands == [capture_clip_set(sheet._bundle, target, values={'hold': 1.5})]
    assert State(plan.bundle).entity(target)['app'] == {
        'cut': 'c2', 'layer': 'card', 'for': 1.5,
    }

    peer = runtime.session(name='cut-owned-peer')
    peer.commit(label('Peer', track='type'))
    result = sheet.apply(edited, session=session, dry_run=False)
    assert result['data']['status'] == 'rebased'
    assert json.loads(runtime.calls[-1][0])['commands'] == plan.commands
    accepted = bundle_from_document(result['data']['canonical_document'])
    assert State(accepted).entity(target)['app'] == {
        'cut': 'c2', 'layer': 'card', 'for': 1.5,
    }
    assert State(accepted).entity('parent/track:type')['label'] == 'Peer'

    runtime.restart()
    reloaded = runtime.session(name='cut-owned-native-reloaded')
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


@pytest.mark.parametrize('entry', ['python', 'cli', 'sheet'])
def test_http_connected_label_clear_is_lossless_across_native_frontends(
        runtime, capsys, entry, monkeypatch):
    _document, setup = seed_labeled_tiny_cut_parent(runtime)
    runtime.restart()
    session = runtime.session(name=entry)
    loaded = session.client.timelines.open_bundle(runtime.project, 'film')
    assert loaded.ok
    before = loaded.data['bundle']
    track_ref = 'parent/track:plate'
    clip_ref = 'parent/clip:b-plate'
    original_clip = copy.deepcopy(State(before).entity(clip_ref))
    original_registry = copy.deepcopy(before['parent']['registry'])
    assert State(before).entity(track_ref)['label'] == 'Source'
    assert original_clip['asset'] == 'Q'
    assert original_clip['opaque'] == {'source_token': ['fixture', None, False, 7]}
    assert setup['data']['accepted_revision_id'] == runtime.history()['head']['revision_id']

    def forbidden_legacy_publish(*args, **kwargs):
        pytest.fail('connected frontend used retired publish_parent_composition')

    # The guard applies to the restarted RuntimeService instances too.
    monkeypatch.setattr(type(runtime.service()), 'publish_parent_composition', forbidden_legacy_publish)

    clear = capture_track_set(before, track_ref, clear=['label'])
    if entry == 'python':
        result = session.commit(clear)
    elif entry == 'cli':
        assert run(runtime, 'edit', 'track-label', 'film', '--track', track_ref, '--clear') == 0
        result = json.loads(capsys.readouterr().out)
    else:
        sheet = NativeSheet.export(session)
        edited = edit_cell(sheet.text, track_ref, 'clear', label=True)
        assert sheet.preview(edited).commands == [clear]
        result = sheet.apply(edited, session=session, dry_run=False)

    body = json.loads(runtime.calls[-1][0])
    assert body['commands'] == [clear]
    assert body['source'] == {'via': entry}
    accepted = bundle_from_document(result['data']['canonical_document'])
    assert State(accepted).entity(track_ref).get('label') is None
    assert State(accepted).entity(clip_ref) == original_clip
    assert accepted['parent']['registry'] == original_registry
    assert len(runtime.calls) == 1

    runtime.restart()
    reloaded = runtime.session(name=f'{entry}-reloaded')
    stored = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=result['data']['accepted_revision_id'])
    assert stored.ok
    stored_bundle = stored.data['bundle']
    assert State(stored_bundle).entity(track_ref).get('label') is None
    assert State(stored_bundle).entity(clip_ref) == original_clip
    assert stored_bundle['parent']['registry'] == original_registry

    undone = reloaded.undo([result['receipt']['receipt_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert State(restored).entity(track_ref)['label'] == 'Source'
    assert State(restored).entity(clip_ref) == original_clip
    assert restored['parent']['registry'] == original_registry
    assert len(runtime.calls) == 2


@pytest.mark.parametrize('entry', ['python', 'cli', 'sheet'])
def test_http_connected_rational_move_is_lossless_across_native_frontends(
        runtime, capsys, entry, monkeypatch):
    _document, setup = seed_rational_tiny_cut_parent(runtime)
    runtime.restart()
    session = runtime.session(name=entry)
    loaded = session.client.timelines.open_bundle(runtime.project, 'film')
    assert loaded.ok
    before = loaded.data['bundle']
    target = State(before).entity(RATIONAL_TARGET)
    original_target = copy.deepcopy(target)
    original_registry = copy.deepcopy(before['parent']['registry'])
    expected = capture_move(before, RATIONAL_TARGET, RATIONAL_LATTICE_SECONDS)
    assert before['parent']['config']['output'] == RATIONAL_FPS
    assert setup['data']['accepted_revision_id'] == runtime.history()['head']['revision_id']
    assert target['asset'] == 'Q'
    assert target['opaque'] == {'retained_source': ['fixture', None, False, 7]}

    def forbidden_legacy_publish(*args, **kwargs):
        pytest.fail('connected frontend used retired publish_parent_composition')

    monkeypatch.setattr(type(runtime.service()), 'publish_parent_composition', forbidden_legacy_publish)

    if entry == 'python':
        result = session.move(RATIONAL_TARGET, RATIONAL_LATTICE_SECONDS)
    elif entry == 'cli':
        assert run(runtime, 'edit', 'film', '--clip', RATIONAL_TARGET,
                   '--on', str(RATIONAL_LATTICE_SECONDS)) == 0
        result = json.loads(capsys.readouterr().out)
    else:
        sheet = NativeSheet.export(session)
        edited = edit_cell(sheet.text, RATIONAL_TARGET, str(RATIONAL_LATTICE_SECONDS))
        assert sheet.preview(edited).commands == [expected]
        result = sheet.apply(edited, session=session, dry_run=False)

    body = json.loads(runtime.calls[-1][0])
    assert body['commands'] == [expected]
    assert result['data']['commands'] == [expected]
    assert body['source'] == {'via': entry}
    assert len(runtime.calls) == 1

    accepted = bundle_from_document(result['data']['canonical_document'])
    moved = State(accepted).entity(RATIONAL_TARGET)
    assert moved['at'] == pytest.approx(RATIONAL_LATTICE_SECONDS)
    assert moved['hold'] == pytest.approx(RATIONAL_LATTICE_SECONDS)
    assert moved['asset'] == original_target['asset']
    assert moved['opaque'] == original_target['opaque']
    assert moved['app']['cut'] == original_target['app']['cut']
    assert moved['app']['layer'] == original_target['app']['layer']
    assert moved['app']['why'] == original_target['app']['why']
    assert accepted['parent']['config']['output'] == RATIONAL_FPS
    assert accepted['parent']['registry'] == original_registry

    start_frame = clip_start_frame(moved, float(RATIONAL_FPS_VALUE))
    end_frame = clip_end_frame(moved, float(RATIONAL_FPS_VALUE))
    assert (start_frame, end_frame) == (30, 60)
    assert list(range(start_frame, end_frame))[-1] == 59
    assert end_frame not in range(start_frame, end_frame)

    history_entry = next(item for item in runtime.history()['items']
                         if item['publication_id'] == result['receipt']['receipt_id'])
    assert [row['command'] for row in history_entry['records']['commands']] == [expected]

    runtime.restart()
    reloaded = runtime.session(name=f'{entry}-reloaded')
    stored = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=result['data']['accepted_revision_id'])
    assert stored.ok
    assert persisted_bundle(stored.data['bundle']) == persisted_bundle(accepted)

    undone = reloaded.undo([result['receipt']['receipt_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert persisted_bundle(restored) == persisted_bundle(before)
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    assert redone['data']['canonical_document'] == result['data']['canonical_document']
    assert len(runtime.calls) == 3


@pytest.mark.parametrize('entry', ['python', 'cli', 'sheet'])
def test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends(
        runtime, capsys, entry, monkeypatch):
    _document, setup = seed_shared_occurrence_parent(runtime)
    runtime.restart()
    session = runtime.session(name=entry)
    loaded = session.client.timelines.open_bundle(runtime.project, 'film')
    assert loaded.ok
    before = loaded.data['bundle']
    original_target = copy.deepcopy(State(before).entity(OCCURRENCE_TARGET))
    original_clear = copy.deepcopy(State(before).entity(OCCURRENCE_CLEAR))
    original_sibling = copy.deepcopy(State(before).entity(OCCURRENCE_SIBLING))
    source_pin = occurrence_source_pin(before, OCCURRENCE_TARGET)
    expected = capture_move(before, OCCURRENCE_TARGET, OCCURRENCE_GLOBAL_ON)
    assert setup['data']['accepted_revision_id'] == runtime.history()['head']['revision_id']
    assert source_pin['shot_id'] == 'shot-shared'
    assert source_pin['text_bindings'] == [{'slot': 'voiceover', 'text': 'hello'}]
    assert original_target['app'] == {
        'f2Opaque': {'owner': 'f2', 'nested': [1, {'k': 'v'}]},
    }

    def forbidden_legacy_publish(*args, **kwargs):
        pytest.fail('connected occurrence frontend used retired publish_parent_composition')

    monkeypatch.setattr(type(runtime.service()), 'publish_parent_composition', forbidden_legacy_publish)

    if entry == 'python':
        result = session.move(OCCURRENCE_TARGET, OCCURRENCE_GLOBAL_ON)
    elif entry == 'cli':
        assert run(runtime, 'edit', 'film', '--clip', OCCURRENCE_TARGET,
                   '--on', str(OCCURRENCE_GLOBAL_ON)) == 0
        result = json.loads(capsys.readouterr().out)
    else:
        sheet = NativeSheet.export(session, occurrence='f2-occurrence')
        edited = edit_cell(sheet.text, OCCURRENCE_TARGET, str(OCCURRENCE_GLOBAL_ON))
        assert sheet.preview(edited).commands == [expected]
        result = sheet.apply(edited, session=session, dry_run=False)

    body = json.loads(runtime.calls[-1][0])
    assert body['commands'] == [expected]
    assert result['data']['commands'] == [expected]
    assert body['source'] == {'via': entry}
    assert len(runtime.calls) == 1

    accepted = bundle_from_document(result['data']['canonical_document'])
    moved = State(accepted).entity(OCCURRENCE_TARGET)
    clear = State(accepted).entity(OCCURRENCE_CLEAR)
    sibling = State(accepted).entity(OCCURRENCE_SIBLING)
    assert moved['at'] == OCCURRENCE_GLOBAL_ON
    assert moved['hold'] == original_target['hold']
    assert moved['asset'] == original_target['asset']
    assert moved['app']['f2Opaque'] == original_target['app']['f2Opaque']
    assert clear == original_clear
    assert sibling == original_sibling
    assert occurrence_source_pin(accepted, OCCURRENCE_TARGET)['text_bindings'] == source_pin['text_bindings']
    assert occurrence_source_pin(accepted, OCCURRENCE_SIBLING) == occurrence_source_pin(
        before, OCCURRENCE_SIBLING)

    start_frame = clip_start_frame(moved, 30)
    end_frame = clip_end_frame(moved, 30)
    assert (start_frame, end_frame) == (270, 360)
    assert list(range(start_frame, end_frame))[-1] == 359
    assert end_frame not in range(start_frame, end_frame)

    history_entry = next(item for item in runtime.history()['items']
                         if item['publication_id'] == result['receipt']['receipt_id'])
    record = history_entry['records']['commands'][0]
    source_dependency = next(dep for dep in record['dependencies'] if dep['key'] == 'move.images')
    assert source_dependency['pin']['source']['shot_id'] == source_pin['shot_id']
    assert source_dependency['pin']['source']['revision_id'] == source_pin['revision_id']
    assert source_dependency['pin']['source']['internal_timeline_revision_id'] == (
        source_pin['internal_timeline_revision_id'])

    runtime.restart()
    reloaded = runtime.session(name=f'{entry}-reloaded')
    stored = reloaded.client.timelines.open_bundle(
        runtime.project, 'film', revision_id=result['data']['accepted_revision_id'])
    assert stored.ok
    stored_bundle = stored.data['bundle']
    assert State(stored_bundle).entity(OCCURRENCE_TARGET) == moved
    assert State(stored_bundle).entity(OCCURRENCE_CLEAR) == original_clear
    assert State(stored_bundle).entity(OCCURRENCE_SIBLING) == original_sibling
    assert occurrence_source_pin(stored_bundle, OCCURRENCE_TARGET)['text_bindings'] == (
        source_pin['text_bindings'])

    undone = reloaded.undo([result['receipt']['receipt_id']])
    restored = bundle_from_document(undone['data']['canonical_document'])
    assert State(restored).entity(OCCURRENCE_TARGET) == original_target
    assert State(restored).entity(OCCURRENCE_CLEAR) == original_clear
    assert State(restored).entity(OCCURRENCE_SIBLING) == original_sibling
    assert occurrence_source_pin(restored, OCCURRENCE_TARGET) == source_pin
    redone = reloaded.undo([undone['receipt']['receipt_id']])
    assert redone['data']['canonical_document'] == result['data']['canonical_document']
    assert len(runtime.calls) == 3


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
