"""Native parent replacement with retained, decodable task media and real storage.

Run against a normally generated private S2 Runtime containing clip.swap-media.
No schema patching, synthetic accepted records, sockets or SQL writes.
"""
from __future__ import annotations

import copy
import io
import json
import os
import subprocess
import sys
from types import SimpleNamespace

import pytest
from PIL import Image

from tests.editing_conformance.test_commit_runtime_occurrence_media import (
    body,
    commit,
    foreign_pin,
    inverse,
    rows,
)

pytestmark = pytest.mark.integration
TARGET = 'parent/clip:clip-a'


@pytest.fixture
def operation():
    return 'swap'


@pytest.fixture
def media_owner():
    return 'parent'


@pytest.fixture
def source_bytes(tmp_path):
    def source(kind, name):
        color = 'red' if name == 'old' else 'blue'
        if kind == 'image':
            output = io.BytesIO()
            Image.new('RGB', (16, 16), color).save(output, format='PNG')
            return output.getvalue()
        output = tmp_path / (name + '.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                        f'color=c={color}:s=16x16:r=1:d=6', '-c:v', 'mpeg4', str(output)],
                       check=True, capture_output=True)
        return output.read_bytes()
    return source


@pytest.fixture(params=['image', 'video'])
def editing(request, tmp_path, monkeypatch):
    from tests.helpers.runtime import runtime_checkout, use_runtime

    current = use_runtime()
    # Build through the genuine historical APIs in a separate interpreter,
    # then exercise current acceptance after the normal realm migration.
    seed_runtime = os.environ.get('ASTRID_PARENT_MEDIA_SEED_RUNTIME')
    if not seed_runtime:
        seed_runtime = str(runtime_checkout(commit='b2a1d9fd82121a5509769531a2e91aece97d78b9'))
    script = r'''
import json, sys
from pathlib import Path
from types import SimpleNamespace
import pytest
from tests.helpers.runtime import use_runtime
use_runtime()
from tests.editing_conformance.test_commit_runtime_occurrence_media import editing
from tests.editing_conformance.test_commit_runtime_parent_media_swap import source_bytes
root, kind = Path(sys.argv[1]), sys.argv[2]
with pytest.MonkeyPatch.context() as patch:
    fixture = editing.__wrapped__(SimpleNamespace(param=kind), root, patch, 'swap',
                                  'parent', source_bytes.__wrapped__(root))
    state = next(fixture)
    try:
        fields = ('project', 'old', 'new', 'associations', 'outputs', 'kind', 'operation')
        value = {key: getattr(state, key) for key in fields}
        value['effect_template'] = state.effect(state.project)
        (root / 'seed.json').write_text(json.dumps(value))
    finally:
        fixture.close()
'''
    seeded = subprocess.run([sys.executable, '-c', script, str(tmp_path), request.param],
                            env={**os.environ, 'ASTRID_RUNTIME_CHECKOUT': seed_runtime},
                            capture_output=True, text=True)
    assert seeded.returncode == 0, seeded.stdout + seeded.stderr
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import RequestCommitPort
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    state = SimpleNamespace(**json.loads((tmp_path / 'seed.json').read_text()),
                            root=tmp_path / 'publish', selected=[], closures=[], candidates=[],
                            before_accept=None)
    state.effect = lambda project: {**copy.deepcopy(state.effect_template), 'target_id': project}
    state.service = RuntimeService(state.root)
    state.service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
    state.credentials = CredentialStore(tmp_path / 'current-credentials')
    token, _ = state.credentials.provision('media-editor', ['projects:read', 'projects:write'])
    state.authorize = lambda: state.credentials.require(token, 'projects:write')
    real_selected = RequestCommitPort.selected_media
    real_closure = RequestCommitPort.revision_closure
    real_accept = RequestCommitPort.accept

    def selected_media(port, pin):
        value = real_selected(port, pin)
        validate_commit_value(value, 'VerifiedMedia')
        state.selected.append(copy.deepcopy(value))
        return value

    def revision_closure(port, revision):
        value = real_closure(port, revision)
        state.closures.append(copy.deepcopy(value))
        return value

    def accept(port, prepared):
        state.candidates.append(copy.deepcopy(prepared))
        if state.before_accept:
            state.before_accept()
        return real_accept(port, prepared)

    monkeypatch.setattr(RequestCommitPort, 'selected_media', selected_media)
    monkeypatch.setattr(RequestCommitPort, 'revision_closure', revision_closure)
    monkeypatch.setattr(RequestCommitPort, 'accept', accept)
    monkeypatch.syspath_prepend(str(current / 'tests'))
    try:
        yield state
    finally:
        state.service.close()


def command(editing):
    return {'schema_version': 1, 'op': 'clip.swap-media', 'version': '1', 'select': TARGET,
            'args': {'old_media': editing.old, 'media': editing.new},
            'intent': {'ownership': 'parent'}}


def test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo(editing, monkeypatch):
    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    from astrid.sdk.remote import RemoteTimelines
    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_media_commands import (
        capture_parent_swap_media,
    )

    def renderer_unavailable(*args, **kwargs):
        pytest.fail('media replacement called the renderer')

    monkeypatch.setattr(service_module, 'evaluate_closure', renderer_unavailable)
    monkeypatch.setattr(visual_seam, 'evaluate_closure', renderer_unavailable)
    before = rows(editing)
    preview = commit(editing, body(editing, [command(editing)], dry_run=True), 'preview')
    assert preview['receipt'] is None and rows(editing) == before
    baseline = editing.closures[0]
    original = bundle_from_document(baseline)
    captured = capture_parent_swap_media(original, TARGET, editing.old, editing.new,
                                         verified_media=editing.selected)
    assert preview['data']['commands'] == [captured]
    request = body(editing, [captured])
    created = commit(editing, request, 'selected-swap')
    output = created['data']['canonical_document']
    assert output == preview['data']['canonical_document']
    expected = copy.deepcopy(State(original).entity(TARGET))
    expected['asset'] = editing.new['asset']
    assert State(bundle_from_document(output)).entity(TARGET) == expected
    assert output['shot_revisions'] == baseline['shot_revisions']
    assert output['internal_timeline_revisions'] == baseline['internal_timeline_revisions']
    assert output['parent_revision']['payload']['occurrences'] == baseline['parent_revision']['payload']['occurrences']
    assert editing.new['object_id'] not in {pin['media_id'] for pin in baseline['dependency_manifest']['media']}
    assert editing.new['object_id'] in {pin['media_id'] for pin in output['dependency_manifest']['media']}
    editing.service.close()
    editing.service = RuntimeService(editing.root)
    editing.service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
    stored = editing.service.get_project_parent_composition_revision(
        editing.project, 'film', output['parent_revision']['revision_id'])
    for key, value in output['parent_revision'].items():
        assert stored[key] == value
    assert stored['dependency_manifest'] == output['dependency_manifest']
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', lambda *a, **kw: pytest.fail('retry re-executed semantics'))
        assert commit(editing, request, 'selected-swap') == created
    changed = copy.deepcopy(request)
    changed['source'] = {'via': 'cli'}
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, changed, 'selected-swap')
    assert error.value.status == 409
    undone = commit(editing, body(editing, [inverse(created)]), 'undo')
    assert undone['data']['canonical_document'] == baseline
    redone = commit(editing, body(editing, [inverse(undone)]), 'redo')
    assert redone['data']['canonical_document'] == output
    assert editing.service.store.integrity_report()['ok']

    # The WC3 SDK adapter submits the original head pair and selected pins.
    # Use an already existing alias after redo: no new allocation is needed.
    from astrid.sdk.contracts import DomainResult
    class Transport:
        _last_handshake = {'realm_id': 'realm-1', 'actor_id': 'media-editor'}

        def list_timelines(self, project, *, cursor=None, limit=50):
            return ([{'project_id': project, 'timeline_id': 'film', 'slug': 'film'}], None)

        def get_project_parent_composition_revision(self, project_id, timeline_id, revision):
            return editing.service.get_project_parent_composition_revision(
                project_id, timeline_id, revision)

        def get_project_shot_revision(self, project_id, shot_id, revision):
            return editing.service.get_project_shot_revision(project_id, shot_id, revision)

        def get_project_timeline_revision(self, project_id, timeline_id, revision):
            return editing.service.get_project_timeline_revision(project_id, timeline_id, revision)

        def get_project_media_selection(self, project_id, selector):
            for pin in (editing.old, editing.new):
                if all(pin.get(key) == selector.get(key) for key in (
                        'asset', 'generation_id', 'variant_id')):
                    return copy.deepcopy(pin)
            raise KeyError(selector)

        def get_project_verified_media(self, project_id, selection):
            return editing.service.get_project_verified_media(
                project_id, selection, authorize=editing.authorize)

        def publish_parent_composition(self, *args, **kwargs):
            pytest.fail('selected SDK adapter published a whole closure')

        def commit_timeline(self, project, timeline, request, *, idempotency_key):
            assert (project, timeline) == (editing.project, 'film')
            return commit(editing, request, idempotency_key)

    head = body(editing)
    monkeypatch.setattr(RemoteTimelines, 'open_composition', lambda self, *args, **kwargs: DomainResult.success({
        'native_inspection': {'project_id': editing.project, 'timeline_id': 'film',
                              'head_revision_id': head['base_revision_id']},
        'summary': {'head_revision_id': head['base_revision_id']},
    }))
    result = RemoteTimelines(Transport()).replace_parent_media(
        editing.project, 'film', occurrence_id=None, clip_id='clip-a',
        source_object_id=editing.old['object_id'], expected_head=head['base_revision_id'],
        expected_publication=head['base_publication_id'], old_media=editing.new,
        media=editing.old, idempotency_key='sdk-swap-back')
    assert result.ok, result.error
    assert State(bundle_from_document(result.data['canonical_document'])).entity(TARGET)['asset'] == editing.old['asset']


def test_public_parent_swap_real_http_lost_ack_restart_exact_retry_and_guards(
        editing, real_runtime, tmp_path, monkeypatch,
):
    """Qualify the public adapter against the real generated client and door."""
    import json

    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.sync import TimelineSession
    from tests.editing_conformance import test_commit_runtime_m1 as m1

    from runtime_protocol.server import RuntimeHandler

    initial = editing.service._timeline_commits()[0].revision_closure(
        editing.project, 'film', editing.service.get_project_timeline(
            editing.project, 'film')['head_revision_id']
    )
    source_target = State(bundle_from_document(initial)).entity('parent/clip:clip-a')
    TARGET = 'parent/clip:wc3-http'
    old = editing.service.get_project_media_selection(
        editing.project,
        {
            'asset': 'wc3-old',
            'generation_id': editing.old['generation_id'],
            'variant_id': editing.old['variant_id'],
        },
        authorize=editing.authorize,
    )
    new = editing.new
    media_fields = {'asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'}
    assert set(old) == set(new) == media_fields

    # Add one fresh parent row through the existing native command builder so
    # the HTTP proof starts from a real immutable five-field old selection;
    # the captured historical row itself predates that binding.
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.native_parent_media_commands import capture_clip_add_media

    bundle = bundle_from_document(initial)
    parent_track = {'id': 'wc3-http-track', 'kind': 'visual', 'role': 'output'}
    commit(
        editing,
        body(editing, [capture_track_create(bundle, 'parent', parent_track)]),
        'wc3-fixture-track',
    )
    initial = editing.service._timeline_commits()[0].revision_closure(
        editing.project, 'film', editing.service.get_project_timeline(
            editing.project, 'film')['head_revision_id']
    )
    bundle = bundle_from_document(initial)
    row = copy.deepcopy(source_target)
    row['id'], row['asset'] = 'wc3-http', old['asset']
    row['track'] = parent_track['id']
    row['opaque'] = {'values': [None, False, {}, []], 'literal': TARGET}
    verified_old = editing.service.get_project_verified_media(
        editing.project, old, authorize=editing.authorize,
    )
    add = capture_clip_add_media(
        bundle, row, old, verified_media=[verified_old],
    )
    commit(editing, body(editing, [add]), 'wc3-fixture-add')
    baseline = editing.service._timeline_commits()[0].revision_closure(
        editing.project, 'film', editing.service.get_project_timeline(
            editing.project, 'film')['head_revision_id']
    )
    head = editing.service.get_project_timeline(editing.project, 'film')
    baseline_target = copy.deepcopy(State(bundle_from_document(baseline)).entity(TARGET))
    assert baseline_target['asset'] == old['asset']
    expected_base = (head['head_revision_id'], head['head_publication_id'])

    # The fixture service holds the same realm that the HTTP daemon opens.
    # Close that read connection before handing the realm to RuntimeDaemon.
    editing.service.close()
    monkeypatch.setenv('ASTRID_RUNTIME_DATA_ROOT', str(tmp_path / 'client-data'))
    support = tmp_path / 'support'
    daemon = real_runtime(editing.root, support_root=support, authoring_profile='astrid')
    client = m1.open_client(daemon)
    original_send = RuntimeHandler._send
    commits = []
    lost = False

    def observe_send(handler, status, payload=None, **kwargs):
        nonlocal lost
        if handler.command == 'POST' and handler.path.endswith('/commit'):
            commits.append({
                'body': bytes(handler._prefetched_body),
                'key': handler.headers['Idempotency-Key'],
                'path': handler.path,
                'request_id': handler._request_id(),
                'response': copy.deepcopy(payload),
            })
            if not lost and status == 200:
                lost = True
                raise ConnectionError('parent media acknowledgement lost after durable acceptance')
        return original_send(handler, status, payload, **kwargs)

    monkeypatch.setattr(RuntimeHandler, '_send', observe_send)
    first_key = 'parent-media-real-http'
    first = client.timelines.replace_parent_media(
        editing.project, 'film', occurrence_id=None, clip_id='wc3-http',
        source_object_id=new['object_id'], expected_head=expected_base[0],
        expected_publication=expected_base[1], old_media=old, media=new,
        idempotency_key=first_key,
    )
    assert not first.ok
    assert len(commits) == 1, first.as_dict()
    first_wire = copy.deepcopy(commits[0])
    first_body = json.loads(first_wire['body'])
    assert first_wire['path'] == f'/v1/projects/{editing.project}/timelines/film/commit'
    assert first_wire['key'] == first_key
    assert first_wire['request_id']
    assert (first_body['base_revision_id'], first_body['base_publication_id']) == expected_base
    command = first_body['commands'][0]
    assert command['select'] == TARGET
    assert command['args'] == {'old_media': old, 'media': new}
    assert set(command['args']['old_media']) == set(command['args']['media']) == media_fields
    accepted = first_wire['response']
    assert accepted['receipt']['idempotency_key'] == first_key
    outbox = TimelineSession.open(editing.project, 'film', client=client).outbox.path
    lost_state = json.loads(outbox.read_bytes())
    assert lost_state['flight']['key'] == first_key
    assert lost_state['flight']['body'].encode() == first_wire['body']
    assert lost_state['pending'] == [command]

    port = daemon.httpd.server_port
    daemon.stop()
    daemon = real_runtime(editing.root, support_root=support, port=port, authoring_profile='astrid')
    client = m1.open_client(daemon)
    retried = client.timelines.replace_parent_media(
        editing.project, 'film', occurrence_id=None, clip_id='wc3-http',
        source_object_id=new['object_id'], expected_head=expected_base[0],
        expected_publication=expected_base[1], old_media=old, media=new,
    )
    assert retried.ok, retried.as_dict()
    assert {key: value for key, value in retried.data.items()
            if key not in {'accepted_publication_id', 'show_command'}} == accepted['data']
    assert retried.data['accepted_publication_id'] == accepted['receipt']['receipt_id']
    assert retried.receipt.as_dict() == accepted['receipt']
    retry_count = len(commits) - 1
    assert retry_count >= 1
    assert all({key: entry[key] for key in ('path', 'key', 'body')} == {
        key: first_wire[key] for key in ('path', 'key', 'body')
    } for entry in commits[1:])
    assert json.loads(outbox.read_bytes())['flight'] is None
    assert json.loads(outbox.read_bytes())['pending'] == []
    replaced = State(bundle_from_document(accepted['data']['canonical_document'])).entity(TARGET)
    assert replaced == {**baseline_target, 'asset': new['asset']}
    parent = accepted['data']['canonical_document']['parent_revision']['payload']
    assert [clip['id'] for clip in parent['clips']] == [clip['id'] for clip in baseline['parent_revision']['payload']['clips']]
    assert parent['config']['clips'] == parent['clips']
    assert replaced['opaque'] == baseline_target['opaque']

    # Advance the real head through a separate outbox, then replay the already
    # acknowledged request at its original base and key. Runtime must return
    # the original receipt without accepting a new revision.
    later = TimelineSession.open(
        editing.project, 'film', client=client, outbox_path=tmp_path / 'later.json',
    )
    later_result = later.move('parent/clip:clip-b', 1, idempotency_key='parent-media-later')
    later_head = later_result['data']['accepted_revision_id']
    assert later_head != accepted['data']['accepted_revision_id']
    before_replay = len(commits)
    replayed = client.timelines.replace_parent_media(
        editing.project, 'film', occurrence_id=None, clip_id='wc3-http',
        source_object_id=new['object_id'], expected_head=expected_base[0],
        expected_publication=expected_base[1], old_media=old, media=new,
        idempotency_key=first_key,
    )
    assert replayed.ok
    assert {key: value for key, value in replayed.data.items()
            if key not in {'accepted_publication_id', 'show_command'}} == accepted['data']
    assert replayed.data['accepted_publication_id'] == accepted['receipt']['receipt_id']
    assert replayed.receipt.as_dict() == accepted['receipt']
    assert len(commits) > before_replay  # keyed replay A
    assert all({key: entry[key] for key in ('path', 'key', 'body')} == {
        key: first_wire[key] for key in ('path', 'key', 'body')
    } for entry in commits[before_replay:])
    assert client.timelines.history(editing.project, 'film').data['head']['revision_id'] == later_head

    reloaded = client.timelines.open_bundle(editing.project, 'film', revision_id=accepted['data']['accepted_revision_id'])
    assert reloaded.ok, reloaded.as_dict()
    reloaded_bundle = reloaded.data['bundle']
    reloaded_target = State(reloaded_bundle).entity(TARGET)
    assert reloaded_target == replaced
    assert State(reloaded_bundle).collection('parent', 'clip') == State(bundle_from_document(accepted['data']['canonical_document'])).collection('parent', 'clip')
    assert reloaded_bundle['parent']['clips'] == reloaded_bundle['parent']['config']['clips']

    guarded = TimelineSession.open(
        editing.project, 'film', client=client, outbox_path=tmp_path / 'guarded.json',
    )
    undone = guarded.undo([accepted['receipt']['receipt_id']], idempotency_key='parent-media-undo')
    undone_target = State(bundle_from_document(undone['data']['canonical_document'])).entity(TARGET)
    assert undone_target == baseline_target
    assert State(bundle_from_document(undone['data']['canonical_document'])).entity('parent/clip:clip-b')['at'] == 1
    redone = guarded.undo([undone['receipt']['receipt_id']], idempotency_key='parent-media-redo')
    assert State(bundle_from_document(redone['data']['canonical_document'])).entity(TARGET) == replaced
    assert State(bundle_from_document(redone['data']['canonical_document'])).entity('parent/clip:clip-b')['at'] == 1

    # A malformed or unrelated persisted intent must fail before a POST and
    # preserve the exact durable outbox bytes.
    for pending, kwargs in (
        ({**command, 'select': 'parent/clip:clip-b'}, {'old_media': old, 'media': new}),
        (command, {'old_media': True, 'media': False}),
    ):
        invalid_state = copy.deepcopy(lost_state)
        invalid_state['pending'] = [pending]
        outbox.write_bytes(json.dumps(invalid_state, sort_keys=True).encode())
        before = outbox.read_bytes()
        sent = len(commits)
        refused = client.timelines.replace_parent_media(
            editing.project, 'film', occurrence_id=None, clip_id='wc3-http',
            source_object_id=new['object_id'], expected_head=expected_base[0],
            expected_publication=expected_base[1], idempotency_key=first_key,
            **kwargs,
        )
        assert not refused.ok
        assert len(commits) == sent
        assert outbox.read_bytes() == before


@pytest.mark.parametrize('side', ['old_media', 'media'])
@pytest.mark.parametrize('damage', ['stale', 'foreign', 'fingerprint'])
def test_invalid_selected_media_refuses_without_writes(editing, side, damage):
    from runtime_protocol.errors import RuntimeErrorBase

    request = copy.deepcopy(body(editing, [command(editing)]))
    pin = request['commands'][0]['args'][side]
    if damage == 'stale':
        association = next(row for row in editing.associations if row['object_id'] == pin['object_id'])
        editing.service.update_managed_output_lifecycle(association['association_id'], {
            'operation': 'promote', 'expected_version': association['lifecycle']['version'],
        }, idempotency_key='stale')
    elif damage == 'foreign':
        request['commands'][0]['args'][side] = foreign_pin(editing)
    else:
        pin['catalog_digest'] = pin['object_id']
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase):
        commit(editing, request, 'invalid')
    assert editing.candidates == []
    assert rows(editing) == before


@pytest.mark.parametrize('side', ['old_media', 'media'])
def test_lifecycle_race_refuses_at_acceptance(editing, side):
    from runtime_protocol.errors import RuntimeErrorBase

    request = body(editing, [command(editing)])
    pin = request['commands'][0]['args'][side]
    observed = []

    def interfere():
        association = next(row for row in editing.associations if row['object_id'] == pin['object_id'])
        editing.service.update_managed_output_lifecycle(association['association_id'], {
            'operation': 'promote', 'expected_version': association['lifecycle']['version'],
        }, idempotency_key='accept-race')
        observed.append(rows(editing))

    editing.before_accept = interfere
    with pytest.raises(RuntimeErrorBase, match='selected media catalog digest changed'):
        commit(editing, request, 'race')
    assert rows(editing) == observed[0]
    assert len(editing.candidates) == 1


@pytest.mark.parametrize('intervention', ['disjoint', 'aba'])
def test_accepted_history_rebase_and_guarded_aba_undo(editing, intervention):
    from runtime_protocol.errors import RuntimeErrorBase

    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline.commit import bundle_from_document

    request = body(editing, [command(editing)])
    if intervention == 'disjoint':
        sibling = {'schema_version': 1, 'op': 'clip.set', 'version': '1',
                   'select': 'parent/clip:clip-b', 'args': {'values': {'hold': 2.5}, 'clear': []}}
        side = commit(editing, body(editing, [sibling]), 'intervening-sibling')
        swapped = commit(editing, request, 'stale-swap')
        assert State(bundle_from_document(swapped['data']['canonical_document'])).entity('parent/clip:clip-b')['hold'] == 2.5
        undone = commit(editing, body(editing, [inverse(swapped)]), 'undo-rebased')
        assert undone['data']['canonical_document'] == side['data']['canonical_document']
    else:
        swapped = commit(editing, request, 'swap')
        again = copy.deepcopy(command(editing))
        again['args']['old_media'] = editing.new
        repeated = commit(editing, body(editing, [again]), 'same-asset-write')
        assert repeated['data']['canonical_document'] == swapped['data']['canonical_document']
        before = rows(editing)
        with pytest.raises(RuntimeErrorBase) as error:
            commit(editing, body(editing, [inverse(swapped)]), 'guarded-undo')
        assert error.value.details['reason'] == 'intervening_write'
        assert rows(editing) == before
