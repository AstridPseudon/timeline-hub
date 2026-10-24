"""Ordinary Runtime port capture/commit/reload/undo/retry, with no schema override."""
from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.commit import (
    bundle_from_document,
)
from astrid.sdk.timeline.native_auto_placement import unplace_shared
from tests.editing_conformance.test_recipe_occurrence_media import inputs
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration
OWNER = 'occurrence:occ-a'
CHILD = OWNER + '/clip:placed'


@pytest.fixture(params=['image', 'video'])
def editing(request, tmp_path, monkeypatch):
    import tests

    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / 'tests'))
    monkeypatch.setattr(tests, '__path__', [*tests.__path__, str(runtime / 'tests')])
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.timeline_commit_port import RequestCommitPort
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_store import TimelineCommitStore
    from test_generation_publish_v1_settlement import _effect, _fixture, _output, _settle
    from test_timeline_commit_acceptance import validate_prepared

    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_add_media

    kind = request.param

    def effect(project):
        value = _effect(project, groups=[{'group_key': 'main', 'selectors': [
            {'selector': 'new', 'ordinal': 0, 'variant_key': 'new', 'output_port': kind}]}])
        value['payload']['metadata']['params'] = {'duration_seconds': 6} if kind == 'video' else {}
        return value

    service, project, task, attempt, admitted = _fixture(tmp_path, effect_factory=effect)
    project = project['id']
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('media-editor', ['projects:read', 'projects:write'])

    def authorize():
        return credentials.require(token, 'projects:write')

    state = SimpleNamespace(service=service, project=project, authorize=authorize,
                            root=tmp_path / 'publish', kind=kind, selected=[])
    try:
        output = _output(b'new', output_port=kind, group_key='main', variant_key='new', ordinal=0,
                         filename='new.' + ('mp4' if kind == 'video' else 'png'),
                         media_type=kind + ('/mp4' if kind == 'video' else '/png'))
        _settle(service, attempt, [output], effect=admitted)
        association = service.managed_outputs(task['task']['id'])[0]
        state.new = service.get_project_media_selection(project, {
            'association_id': association['association_id'], 'object_id': association['object_id'],
            'version': association['lifecycle']['version']}, authorize=authorize)
        state.verified = service.get_project_verified_media(project, state.new, authorize=authorize)
        document, _, _, _ = inputs(kind)
        input_parent = document['parent_revision']['payload']
        input_occurrences = input_parent['occurrences']
        input_internal = document['internal_timeline_revisions'][0]['payload']
        old_result = service.import_media(
            project, b'old-' + kind.encode(),
            media_type='video/mp4' if kind == 'video' else 'image/png',
            original_name='old.' + ('mp4' if kind == 'video' else 'png'),
            actor_id='media-editor',
            **({'duration_seconds': 6} if kind == 'video' else {}),
            idempotency_key='old-media',
        )['data']
        old = service.get_project_media_selection(project, {
            'asset': old_result['variant_id'], 'generation_id': old_result['generation_id'],
            'variant_id': old_result['variant_id']}, authorize=authorize)
        old_verified = service.get_project_verified_media(project, old, authorize=authorize)
        service.create_timeline(project, 'main', idempotency_key='timeline')
        TimelineCommitStore(service.store, validate_prepared=validate_prepared).bootstrap(
            project, 'main', authorize=authorize)
        service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
        head = service.get_project_timeline(project, 'main')
        initial = service._timeline_commits()[0].revision_closure(
            project, 'main', head['head_revision_id'])
        bundle = bundle_from_document(initial)
        commands = []

        def append(command):
            nonlocal bundle
            commands.append(command)
            bundle = execute(bundle, [command]).bundle

        append(capture_track_create(bundle, 'parent', input_parent['config']['tracks'][0]))
        for index, occurrence in enumerate(input_occurrences):
            shot_id = occurrence['shot_id'] if index == 0 else 'chapter-shot-b'
            append(capture_occurrence_create(
                bundle, occurrence['occurrence_id'], shot_id, name='Chapter One',
                track=occurrence['track'], on=occurrence['placement']['start_ms'] / 1000,
                duration=occurrence['duration_ms'] / 1000,
            ))
            for track in input_internal['tracks']:
                append(capture_track_create(bundle, 'occurrence:' + occurrence['occurrence_id'], track))
            for row in input_internal['clips'] if index == 0 else input_internal['clips'][:1]:
                old_row = copy.deepcopy(row)
                old_row['asset'] = old['asset']
                append(capture_occurrence_add_media(
                    bundle, 'occurrence:' + occurrence['occurrence_id'], old_row, old,
                    verified_media=[old_verified],
                ))
        placed = {'id': 'placed', 'clipType': kind, 'track': 'picture', 'asset': state.new['asset'],
                  'at': 1, 'hold': 4, 'opaque': {'clear': None},
                  **({'from': 0, 'to': 4, 'speed': 1} if kind == 'video' else {})}
        append(capture_occurrence_add_media(
            bundle, OWNER, placed, state.new, verified_media=[state.verified],
        ))
        setup = commit(state, body(state, commands), 'setup')
        state.baseline = setup['data']['canonical_document']
        real_selected = RequestCommitPort.selected_media

        def selected(port, pin):
            value = real_selected(port, pin)
            state.selected.append(copy.deepcopy(value))
            return value

        monkeypatch.setattr(RequestCommitPort, 'selected_media', selected)
        yield state
    finally:
        state.service.close()


def body(editing, commands, *, dry_run=False):
    head = editing.service.get_project_timeline(editing.project, 'main')
    label = 'Video unplace'
    return {'api_version': 1, 'project_id': editing.project, 'timeline_id': 'main',
            'base_revision_id': head['head_revision_id'], 'base_publication_id': head['head_publication_id'],
            'commands': commands, 'label': label, 'merge': 'fields', 'reads': [],
            'dry_run': dry_run, 'source': {'via': 'python'},
            'rationale': 'Authenticate occurrence-owned video unplacement',
            'group_id': 'video-unplace',
            'steps': [{'id': 'video-unplace', 'label': label, 'intent': label,
                       'tags': ['integration', 'video-unplace'],
                       'command_ordinals': list(range(len(commands))), 'patch': [], 'reads': []}]}


def commit(editing, request, key):
    return editing.service.commit_timeline(editing.project, 'main', request, idempotency_key=key,
        publisher='media-editor', invocation_path=f'/v1/projects/{editing.project}/timelines/main/commit',
        authorize=editing.authorize)


def rows(editing):
    return tuple(editing.service.store.conn.iterdump())


def inverse(result):
    return {'schema_version': 1, 'op': 'timeline.inverse', 'version': '1', 'select': None,
            'args': {'publications': [result['receipt']['receipt_id']]}}


@pytest.mark.parametrize('keep', [False, True])
def test_capture_commit_reload_undo_redo_and_restart_safe_retry(editing, monkeypatch, keep):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    from astrid.sdk.timeline import commands

    baseline = editing.baseline
    bundle = bundle_from_document(baseline)
    row = State(bundle).entity(CHILD)
    if editing.kind == 'video':
        assert (row['clipType'], row['from'], row['to'], row['hold'], row['speed']) == ('video', 0, 4, 4, 1)
    removal = unplace_shared(bundle, OWNER, 'placed', ownership='occurrence', keep_as_pooled=keep,
                              media=editing.new, verified_media=[editing.verified])['commands']
    # Actual preview and acceptance retain the original authoritative capture.
    before = rows(editing)
    preview = commit(editing, body(editing, removal, dry_run=True), 'unplace-preview')
    assert rows(editing) == before
    request = body(editing, removal)
    removed = commit(editing, request, 'unplace')
    assert removed['data']['commands'] == removal
    output = removed['data']['canonical_document']
    assert preview['data']['canonical_document'] == output
    if keep:
        assert editing.selected == [editing.verified, editing.verified]
    state = State(bundle_from_document(output))
    assert state.entity(CHILD, optional=True) is None
    assert state.entity(OWNER + '/registry') == State(bundle).entity(OWNER + '/registry')
    assert state.config('occurrence:occ-b') == State(bundle).config('occurrence:occ-b')
    if keep:
        assert state.config(OWNER)['app']['astrid']['pool'] == [editing.new['asset']]
    history = editing.service.list_timeline_commits(editing.project, 'main', authorize=editing.authorize)
    editing.service.close()
    editing.service = RuntimeService(editing.root)
    editing.service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
    head = editing.service.get_project_timeline(editing.project, 'main')
    reloaded = editing.service.get_project_parent_composition_revision(
        editing.project, 'main', head['head_revision_id'])
    assert reloaded['payload'] == output['parent_revision']['payload']
    assert reloaded['dependency_manifest'] == output['dependency_manifest']
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', lambda *a, **kw: pytest.fail('retry executed semantics'))
        assert commit(editing, request, 'unplace') == removed
    assert editing.service.list_timeline_commits(editing.project, 'main', authorize=editing.authorize) == history
    changed = copy.deepcopy(request)
    changed['source'] = {'via': 'cli'}
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, changed, 'unplace')
    assert error.value.status == 409 and rows(editing) == before
    undone = commit(editing, body(editing, [inverse(removed)]), 'undo-unplace')
    assert undone['data']['canonical_document'] == baseline
    redone = commit(editing, body(editing, [inverse(undone)]), 'redo-unplace')
    assert redone['data']['canonical_document'] == output
    assert editing.service.store.integrity_report()['ok']
