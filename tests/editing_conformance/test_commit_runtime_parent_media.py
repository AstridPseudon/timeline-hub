"""Ordinary parent media edits through managed custody and the real Agent provider.

No daemon, schema substitution, prepared provider, or synthetic accepted history.
Existing-film tests restore Runtime's approved pre-cut film backup.
Generation settlement qualifies selection custody, not the assembler proposal lifecycle.
"""
from __future__ import annotations

import copy
import hashlib
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.native_parent_media_commands import (
    capture_clip_replace_media,
)
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


class ParentMediaSeamBlocked(RuntimeError):
    """Only the specifically observed seam failure may satisfy a strict xfail."""


def call(op, args, select='parent'):
    return {'schema_version': 1, 'op': op, 'version': '1', 'select': select, 'args': args}


def body(editing, calls, *, dry_run=False):
    head = editing.service.get_project_timeline(editing.project, 'film')
    return {'api_version': 1, 'project_id': editing.project, 'timeline_id': 'film',
            'base_revision_id': head['head_revision_id'],
            'base_publication_id': head['head_publication_id'], 'commands': calls,
            'dry_run': dry_run, 'source': {'via': 'python'}}


def commit(editing, request, key):
    from runtime_protocol.timeline_commit_port import route_path

    return editing.service.commit_timeline(
        editing.project, 'film', request, idempotency_key=key, publisher='parent-editor',
        invocation_path=route_path(editing.project, 'film'), authorize=editing.authorize)


def current(editing):
    head = editing.service.get_project_timeline(editing.project, 'film')
    return editing.service._timeline_commits()[0].revision_closure(
        editing.project, 'film', head['head_revision_id'])


def rows(editing):
    return tuple(editing.service.store.conn.iterdump())


def row(editing, identity='reserved-row', *, asset=None, track='visual'):
    value = {'id': identity, 'clipType': editing.kind, 'track': track,
             'asset': asset or editing.pins['new']['asset'], 'at': .125,
             'hold': 4 if editing.kind == 'video' else 1.25, 'params': None,
             'opaque': {'values': [None, False, {}, []], 'literal': 'target'}}
    if editing.kind == 'video':
        value.update({'from': 2, 'to': 6, 'speed': 2})
    else:
        value['speed'] = None
    return value


def birth(editing, value=None, pin=None):
    return call('clip.add-media', {'row': value or row(editing), 'media': pin or editing.pins['new']})


def undo(editing, result, key):
    return commit(editing, body(editing, [call('timeline.inverse', {
        'publications': [result['receipt']['receipt_id']]}, None)]), key)


def clip_ids(document):
    return [clip['id'] for clip in document['parent_revision']['payload']['clips']]


def literal_replacement(editing):
    # The captured film has a transition in occurrence-2. clip.delete currently
    # rejects *any* transition anywhere. Prepare the supported literal case
    # through a real accepted scalar edit; never change a stored input image.
    clear = capture_clip_set(bundle_from_document(current(editing)),
        'occurrence:occurrence-2/clip:clip-2', clear=['transition'])
    commit(editing, body(editing, [clear]), 'clear-transition')
    for identity in ('A', 'target', 'C'):
        commit(editing, body(editing, [birth(editing, row(editing, identity, asset='old-' + identity),
                                            editing.pins['old'])]), 'old-' + identity)


def media_realm(tmp_path, monkeypatch, kind, *, historical):
    runtime = use_runtime()
    monkeypatch.syspath_prepend(str(runtime / 'tests'))
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_port import RequestCommitPort
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_validation import validate_commit_value
    from test_generation_publish_v1_settlement import (
        CAPABILITY,
        _effect,
        _fixture,
        _output,
        _settle,
    )

    def effect(project):
        value = _effect(project, groups=[{'group_key': 'main', 'selectors': [
            {'selector': name, 'ordinal': index, 'variant_key': name, 'output_port': kind}
            for index, name in enumerate(('old', 'new', 'unrelated'))]}])
        value['payload']['metadata'] = {'prompt': 'parent media source',
                                       'params': {'duration_seconds': 6} if kind == 'video' else {}}
        return value

    if historical:
        from timeline_commit_film_fixture import build_film_fixture

        film = build_film_fixture(tmp_path)
        root = film.duplicate_root
        service = RuntimeService(root)
        project = {'id': film.project_id}
        service.register_executor({'executor_id': 'publish-worker', 'capabilities': [CAPABILITY]},
                                  idempotency_key='publish-executor')
        admitted = effect(project['id'])
        task = service.create_task({
            'capability_id': CAPABILITY, 'capability_digest': 'sha256:' + hashlib.sha256(CAPABILITY.encode()).hexdigest(),
            'project': project['id'], 'settlement_effect': admitted, 'idempotency_key': 'publish-task'})
        attempt = service.claim_next({'executor_id': 'publish-worker', 'capability_ids': [CAPABILITY],
            'runtime_epoch': service.health()['runtime_epoch']}, idempotency_key='publish-claim')
    else:
        service, project, task, attempt, admitted = _fixture(tmp_path, effect_factory=effect)
        root = tmp_path / 'publish'
    credentials = CredentialStore(tmp_path / 'credentials')
    token, _ = credentials.provision('parent-editor', ['projects:read', 'projects:write'])
    editing = SimpleNamespace(service=service, project=project['id'], root=root,
                              kind=kind, effect=effect, task=task, selected=[], candidates=[])
    editing.authorize = lambda: credentials.require(token, 'projects:write')
    selected_media, accept = RequestCommitPort.selected_media, RequestCommitPort.accept

    def selected(port, pin):
        value = selected_media(port, pin)
        validate_commit_value(value, 'VerifiedMedia')
        editing.selected.append(copy.deepcopy(value))
        return value

    def accepted(port, prepared):
        editing.candidates.append(copy.deepcopy(prepared))
        return accept(port, prepared)

    monkeypatch.setattr(RequestCommitPort, 'selected_media', selected)
    monkeypatch.setattr(RequestCommitPort, 'accept', accepted)
    try:
        outputs = [_output(name.encode(), output_port=kind, group_key='main', variant_key=name,
                           ordinal=index, filename=name + ('.mp4' if kind == 'video' else '.png'),
                           media_type=kind + ('/mp4' if kind == 'video' else '/png'))
                   for index, name in enumerate(('old', 'new', 'unrelated'))]
        _settle(service, attempt, outputs, effect=admitted)
        editing.associations = service.managed_outputs(task['task']['id'])
        editing.pins = {association['variant_key']: service.get_project_media_selection(editing.project, {
            'association_id': association['association_id'], 'object_id': association['object_id'],
            'version': association['lifecycle']['version']}, authorize=editing.authorize)
            for association in editing.associations}
        service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
        if not historical:
            service.create_timeline(editing.project, 'film', idempotency_key='empty-film')
        else:
            # Install only the verified legacy baseline from the committed,
            # authenticated pre-cut backup, through the normal history read.
            service.list_timeline_commits(editing.project, 'film', authorize=editing.authorize)
        tracked = capture_track_create(bundle_from_document(current(editing)), 'parent', {
            'id': 'visual', 'kind': 'visual', 'role': 'output', 'opaque': [None, False]})
        commit(editing, body(editing, [tracked]), 'visual-track')
        editing.selected.clear()
        editing.candidates.clear()
        yield editing
    finally:
        editing.service.close()


@pytest.fixture(params=['image', 'video'])
def custody(request, tmp_path, monkeypatch):
    yield from media_realm(tmp_path, monkeypatch, request.param, historical=False)


@pytest.fixture(params=['image', 'video'])
def editing(request, tmp_path, monkeypatch):
    yield from media_realm(tmp_path, monkeypatch, request.param, historical=True)


# Restore when the parent recipe can record creation of absent bootstrap assets
# without replacing null/opaque containers, including exact inverse to registry:{}.
@pytest.mark.xfail(strict=True, raises=ParentMediaSeamBlocked,
                   reason='Empty Runtime bootstrap registry:{} has no authored assets container')
def test_fresh_film_first_media_birth_and_exact_inverse(custody):
    from runtime_protocol.errors import RuntimeErrorBase

    baseline = current(custody)
    before = rows(custody)
    try:
        created = commit(custody, body(custody, [birth(custody)]), 'first-media')
    except RuntimeErrorBase as error:
        assert error.message == 'media edit requires an authored asset registry'
        assert rows(custody) == before and custody.candidates == []
        raise ParentMediaSeamBlocked(error.message) from error
    assert clip_ids(current(custody)) == ['reserved-row']
    assert undo(custody, created, 'undo-first-media')['data']['canonical_document'] == baseline


@pytest.mark.parametrize('replace', [False, True])
def test_ordinary_birth_or_ordered_replacement_accept_reload_inverse_redo_retry(editing, monkeypatch, replace):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_producer import request_pin
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    from astrid.sdk.timeline import commands

    if replace:
        literal_replacement(editing)
    baseline = current(editing)
    value = row(editing)
    calls = [birth(editing, value)]
    if replace:
        # Public dry-run performs the exact custody read; the ordinary capture
        # builder consumes those real VerifiedMedia values, never a substitute.
        commit(editing, body(editing, calls, dry_run=True), 'selection-preview')
        calls = capture_clip_replace_media(bundle_from_document(baseline), 'parent/clip:target',
                                            value, editing.pins['new'], verified_media=editing.selected)
        assert [item['op'] for item in calls] == ['timeline.assembled-target', 'clip.add-media', 'clip.delete']
    request = body(editing, calls)
    assert request_pin(request) is None
    validate_commit_value(request, 'CommitRequest')
    before = rows(editing)
    preview = commit(editing, dict(request, dry_run=True), 'preview')
    assert preview['receipt'] is None and rows(editing) == before
    created = commit(editing, request, 'birth')
    document = created['data']['canonical_document']
    assert document == current(editing) == preview['data']['canonical_document']
    assert clip_ids(document) == (['music-bed', 'A', 'reserved-row', 'C'] if replace
                                 else ['music-bed', 'reserved-row'])
    parent = document['parent_revision']['payload']
    assert parent['clips'] == parent['config'].get('clips', parent['clips'])
    assert next(clip for clip in parent['clips'] if clip['id'] == value['id']) == value
    assert parent['registry']['assets'][value['asset']] == {
        'media_id': editing.pins['new']['object_id'], 'type': editing.kind,
        'generationId': editing.pins['new']['generation_id'], 'variantId': editing.pins['new']['variant_id']}
    for alias, entry in baseline['parent_revision']['payload']['registry']['assets'].items():
        assert parent['registry']['assets'][alias] == entry
    assert parent['config']['playback'] == baseline['parent_revision']['payload']['config']['playback']
    assert document['shot_revisions'] == baseline['shot_revisions']
    assert document['internal_timeline_revisions'] == baseline['internal_timeline_revisions']
    assert all(pin in document['dependency_manifest']['media'] for pin in baseline['dependency_manifest']['media'])
    assert document['dependency_manifest']['documents'] == baseline['dependency_manifest']['documents']
    record = next(record for record in editing.candidates[-1]['records']['commands']
                  if record['command']['op'] == 'clip.add-media')
    assert record['command']['created'] == ['parent/asset:' + value['asset'], 'parent/clip:reserved-row']
    assert record['dependencies'][-1]['pin'] == editing.pins['new']
    assert all(not dependency['key'].startswith('producer_attempt:')
               for record in editing.candidates[-1]['records']['commands'] for dependency in record['dependencies'])
    history = editing.service.list_timeline_commits(editing.project, 'film', authorize=editing.authorize)
    editing.service.close()
    editing.service = RuntimeService(editing.root)
    editing.service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
    assert current(editing) == document
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', lambda *a, **kw: pytest.fail('exact retry executed semantics'))
        assert commit(editing, request, 'birth') == created
    assert editing.service.list_timeline_commits(editing.project, 'film', authorize=editing.authorize) == history
    undo_request = body(editing, [call('timeline.inverse', {
        'publications': [created['receipt']['receipt_id']]}, None)])
    undone = commit(editing, undo_request, 'undo')
    assert current(editing) == undone['data']['canonical_document'] == baseline
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, body(editing, [birth(editing, value)]), 'retired-id')
    assert error.value.details['reason'] == 'identity_collision'
    assert rows(editing) == before
    redo_request = body(editing, [call('timeline.inverse', {
        'publications': [undone['receipt']['receipt_id']]}, None)])
    redone = commit(editing, redo_request, 'redo')
    assert current(editing) == redone['data']['canonical_document'] == document
    before = rows(editing)
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', lambda *a, **kw: pytest.fail('exact retry executed semantics'))
        for saved_request, key, expected in ((request, 'birth', created), (undo_request, 'undo', undone),
                                             (redo_request, 'redo', redone)):
            assert commit(editing, saved_request, key) == expected
    changed = copy.deepcopy(request)
    changed['source'] = {'via': 'cli'}
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, changed, 'birth')
    assert error.value.status == 409 and rows(editing) == before
    assert undo(editing, redone, 'undo-again')['data']['canonical_document'] == baseline
    assert editing.service.store.integrity_report()['ok']


def foreign_pin(editing):
    from test_generation_publish_v1_settlement import CAPABILITY, _output, _settle

    service = editing.service
    project = service.create_project({'slug': 'foreign', 'name': 'Foreign'})['id']
    effect = editing.effect(project)
    task = service.create_task({
        'capability_id': CAPABILITY, 'capability_digest': 'sha256:' + hashlib.sha256(CAPABILITY.encode()).hexdigest(),
        'project': project, 'settlement_effect': effect, 'idempotency_key': 'foreign-task'})
    attempt = service.claim_next({'executor_id': 'publish-worker', 'capability_ids': [CAPABILITY],
        'runtime_epoch': service.health()['runtime_epoch']}, idempotency_key='foreign-claim')
    _settle(service, attempt, [_output(('foreign-' + name).encode(), output_port=editing.kind,
        group_key='main', variant_key=name, ordinal=index,
        filename=name + ('.mp4' if editing.kind == 'video' else '.png'),
        media_type=editing.kind + ('/mp4' if editing.kind == 'video' else '/png'))
        for index, name in enumerate(('old', 'new', 'unrelated'))], effect=effect, key='foreign-settle')
    association = service.managed_outputs(task['task']['id'])[0]
    return service.get_project_media_selection(project, {
        'association_id': association['association_id'], 'object_id': association['object_id'],
        'version': association['lifecycle']['version']}, authorize=editing.authorize)


@pytest.mark.parametrize('damage', ['foreign', 'binding', 'fingerprint', 'stale', 'occupied-row', 'occupied-alias'])
def test_invalid_media_or_reserved_identity_refuses_before_accept_and_writes(editing, damage):
    from runtime_protocol.errors import RuntimeErrorBase

    request = body(editing, [birth(editing)])
    args = request['commands'][0]['args']
    if damage == 'foreign':
        args['media'] = foreign_pin(editing)
    elif damage == 'binding':
        args['media'] = dict(args['media'], object_id=editing.pins['old']['object_id'])
    elif damage == 'fingerprint':
        args['media'] = dict(args['media'], catalog_digest=args['media']['object_id'])
    elif damage == 'stale':
        association = next(item for item in editing.associations if item['variant_key'] == 'new')
        editing.service.update_managed_output_lifecycle(association['association_id'], {
            'operation': 'promote', 'expected_version': association['lifecycle']['version']},
            idempotency_key='promote-before-capture')
    elif damage == 'occupied-row':
        args['row']['id'] = 'music-bed'
    else:
        args['row']['asset'] = 'music-bed'
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, request, 'invalid')
    expected = {
        'foreign': 'selected media is not a managed project generation/variant/object',
        'binding': 'selected media is not a managed project generation/variant/object',
        'fingerprint': 'selected media catalog digest changed',
        'stale': 'selected media catalog digest changed',
        'occupied-row': 'created identity is occupied',
        'occupied-alias': 'existing registry binding differs from exact selection',
    }
    assert error.value.message == expected[damage]
    assert editing.candidates == []
    assert rows(editing) == before


def test_runtime_generic_envelope_does_not_admit_the_obsolete_scalar_shape(editing):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.timeline_commit_validation import validate_commit_value

    value = row(editing)
    scalar = {key: value[key] for key in ('id', 'track', 'at', 'hold', 'speed')}
    if editing.kind == 'video':
        scalar.update({key: value[key] for key in ('from', 'to')})
    scalar['media'] = editing.pins['new']
    request = body(editing, [call('clip.add-media', scalar)])
    validate_commit_value(request, 'CommitRequest')
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, request, 'obsolete-scalar-shape')
    assert error.value.details['reason'] == 'invalid_edit_command'
    assert editing.selected == editing.candidates == []
    assert rows(editing) == before


def test_stale_explicit_replacement_membership_refuses_before_accept_and_writes(editing):
    from runtime_protocol.errors import RuntimeErrorBase

    literal_replacement(editing)
    commit(editing, body(editing, [birth(editing)], dry_run=True), 'selection')
    calls = capture_clip_replace_media(bundle_from_document(current(editing)), 'parent/clip:target',
                                        row(editing), editing.pins['new'], verified_media=editing.selected)
    request = body(editing, calls)
    pin = editing.pins['unrelated']
    commit(editing, body(editing, [birth(editing, row(editing, 'later', asset=pin['asset']), pin)]), 'later')
    editing.candidates.clear()
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase) as error:
        commit(editing, request, 'stale-order')
    assert error.value.details['reason'] == 'selection_changed'
    assert editing.candidates == []
    assert rows(editing) == before


@pytest.mark.parametrize('replace', [False, True])
@pytest.mark.parametrize('interference', ['dependent', 'ABA'])
def test_actual_accepted_dependents_and_aba_refuse_inverse_before_writes(editing, replace, interference):
    from runtime_protocol.errors import RuntimeErrorBase

    if replace:
        literal_replacement(editing)
    calls = [birth(editing)]
    if replace:
        commit(editing, body(editing, calls, dry_run=True), 'selection')
        calls = capture_clip_replace_media(bundle_from_document(current(editing)), 'parent/clip:target',
                                            row(editing), editing.pins['new'], verified_media=editing.selected)
    created = commit(editing, body(editing, calls), 'create')
    if interference == 'dependent':
        dependent = commit(editing, body(editing, [birth(editing, row(editing, 'dependent'))]), 'dependent')
        state = State(bundle_from_document(dependent['data']['canonical_document']))
        assert state.entity('parent/clip:dependent')['asset'] == state.entity('parent/clip:reserved-row')['asset']
    else:
        before = copy.deepcopy(State(bundle_from_document(current(editing))).entity('parent/clip:reserved-row'))
        for index, hold in enumerate((before['hold'] / 2, before['hold'])):
            change = capture_clip_set(bundle_from_document(current(editing)),
                'parent/clip:reserved-row', values={'hold': hold})
            commit(editing, body(editing, [change]), 'aba-' + str(index))
        assert State(bundle_from_document(current(editing))).entity('parent/clip:reserved-row') == before
    editing.candidates.clear()
    before = rows(editing)
    with pytest.raises(RuntimeErrorBase) as error:
        undo(editing, created, 'unsafe-undo')
    # Accepted suffix guards also cover the later creation's collection write;
    # refusal can precede the structural surviving-dependent check.
    assert error.value.details['reason'] == 'intervening_write'
    assert editing.candidates == []
    assert rows(editing) == before


def promote_latest_variant(editing):
    from test_generation_publish_v1_settlement import CAPABILITY, _output, _settle

    old = editing.pins['old']
    service = editing.service
    effect = {'effect_type': 'generation.variant.append', 'target_id': old['generation_id'],
              'expected_version': service.get_generation(old['generation_id'])['version'],
              'payload': {'source_variant_id': old['variant_id'], 'source_object_id': old['object_id'],
                          'variant_type': 'latest', 'output_name': editing.kind,
                          'output_ordinal': 0, 'primary_policy': 'promote'}}
    service.create_task({
        'capability_id': CAPABILITY, 'capability_digest': 'sha256:' + hashlib.sha256(CAPABILITY.encode()).hexdigest(),
        'project': editing.project, 'input_object_ids': [old['object_id']],
        'settlement_effect': effect, 'idempotency_key': 'latest-task'})
    attempt = service.claim_next({'executor_id': 'publish-worker', 'capability_ids': [CAPABILITY],
        'runtime_epoch': service.health()['runtime_epoch']}, idempotency_key='latest-claim')
    output = _output(b'latest-variant', output_port=editing.kind, group_key='main', variant_key='latest', ordinal=0,
                     filename='latest' + ('.mp4' if editing.kind == 'video' else '.png'),
                     media_type=editing.kind + ('/mp4' if editing.kind == 'video' else '/png'))
    settled = _settle(service, attempt, [output], effect=effect, key='latest-settle')
    result = settled['data']['result']['generation_variant']
    assert result['previous_primary_variant_id'] == old['variant_id']
    assert result['new_primary_variant_id'] == result['variant_id'] != old['variant_id']
    assert result['new_primary_object_id'] != old['object_id']
    return result


def test_exact_old_source_tuple_survives_new_primary_variant_and_replacement_inverse(editing):
    literal_replacement(editing)
    baseline = current(editing)
    old = copy.deepcopy(editing.pins['old'])
    old_binding = copy.deepcopy(baseline['parent_revision']['payload']['registry']['assets']['old-target'])
    old_variant = editing.service.get_variant(old['variant_id'])
    promote_latest_variant(editing)
    assert editing.service.get_variant(old['variant_id'])['object_id'] == old_variant['object_id']
    assert editing.service.get_project_media_selection(editing.project, {
        key: old[key] for key in ('asset', 'generation_id', 'variant_id')}, authorize=editing.authorize) == old
    assert current(editing) == baseline
    commit(editing, body(editing, [birth(editing)], dry_run=True), 'selection')
    calls = capture_clip_replace_media(bundle_from_document(baseline), 'parent/clip:target', row(editing),
                                        editing.pins['new'], verified_media=editing.selected)
    created = commit(editing, body(editing, calls), 'replace-after-primary-change')
    document = created['data']['canonical_document']
    assert document['parent_revision']['payload']['registry']['assets']['old-target'] == old_binding
    assert old_binding == {'media_id': old['object_id'], 'type': editing.kind,
                           'generationId': old['generation_id'], 'variantId': old['variant_id']}
    assert {'media_id': old['object_id'], 'content_digest': old['object_id']} in document['dependency_manifest']['media']
    undone = undo(editing, created, 'undo-after-primary-change')
    assert current(editing) == undone['data']['canonical_document'] == baseline
    assert undo(editing, undone, 'redo-after-primary-change')['data']['canonical_document'] == document


# Restore when ordinary deletion resolves unrelated occurrence transitions rather
# than refusing the entire film; no weakening/removal of the original expectation.
@pytest.mark.xfail(strict=True, raises=ParentMediaSeamBlocked,
                   reason='clip.delete globally rejects the captured film occurrence-2 transition')
def test_ordered_replacement_preserves_unrelated_historical_transition(editing):
    from runtime_protocol.errors import RuntimeErrorBase

    for identity in ('A', 'target', 'C'):
        commit(editing, body(editing, [birth(editing, row(editing, identity, asset='old-' + identity),
                                            editing.pins['old'])]), 'old-' + identity)
    baseline = current(editing)
    refs = ['parent/clip:' + identity for identity in clip_ids(baseline)]
    calls = [call('timeline.assembled-target', {'replace_clips': refs}, 'parent/clip:target'),
             dict(birth(editing), select='parent/clip:target'), call('clip.delete', {}, 'parent/clip:target')]
    editing.candidates.clear()
    before = rows(editing)
    try:
        created = commit(editing, body(editing, calls), 'replace-with-transition')
    except RuntimeErrorBase as error:
        assert error.details['reason'] == 'unsupported_dependency'
        assert error.details['conflicts'] == []
        assert error.message == 'clip.delete cannot prove declared semantic dependencies safe'
        assert rows(editing) == before and editing.candidates == []
        raise ParentMediaSeamBlocked(error.message) from error
    assert clip_ids(current(editing)) == ['music-bed', 'A', 'reserved-row', 'C']
    assert created['data']['canonical_document']['internal_timeline_revisions'] == baseline['internal_timeline_revisions']
    assert undo(editing, created, 'undo-with-transition')['data']['canonical_document'] == baseline
