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
        _last_handshake = {'realm_id': 'realm-1', 'actor_id': 'parent-editor'}

        def list_timelines(self, project, *, cursor=None, limit=50):
            return ([{'project_id': project, 'timeline_id': 'film', 'slug': 'film'}], None)

        def get_project_parent_composition_revision(self, project_id, timeline_id, revision):
            return editing.service._timeline_commits()[0].revision_closure(
                project_id, timeline_id, revision)['parent_revision']

        def get_project_shot_revision(self, project_id, shot_id, revision):
            closure = editing.service._timeline_commits()[0].revision_closure(
                project_id, 'film', head['base_revision_id'])
            return next(row for row in closure['shot_revisions']
                        if row['shot_id'] == shot_id and row['revision_id'] == revision)

        def get_project_timeline_revision(self, project_id, timeline_id, revision):
            closure = editing.service._timeline_commits()[0].revision_closure(
                project_id, timeline_id, head['base_revision_id'])
            return next(row for row in closure['internal_timeline_revisions']
                        if row['revision_id'] == revision)

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
