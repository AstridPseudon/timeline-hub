"""D13 design experiment: real recipe primitives, test-local operations only.

No Runtime acceptance, registered-output custody or render recovery is simulated.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess

import pytest

from astrid.packs.rendering.actions.assemble_timeline.run import (
    build_authoring_proposal,
    derive_asset_key,
    derive_clip_id,
)
from astrid.sdk.timeline import build_producer_batch, commands
from astrid.sdk.timeline._collections import AcceptedRecords
from astrid.sdk.timeline._command_state import CommandError, State, equal
from astrid.sdk.timeline._media_inputs import _verified
from astrid.sdk.timeline.commit import _digest, _json, bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_occurrence_media_commands import _clip, _registry
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_clip_delete import delete_document
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.editing_conformance.test_settled_proposal_contract import check_forwarding
from tests.packs.rendering.test_assemble_timeline import _payload
from tests.sdk import test_timeline_sync as session_fixtures
from tests.sdk.test_timeline_commit_provider_document import document_fixture
from tests.sdk.test_timeline_sync import open_session

MEDIA = 'sha256:' + '2' * 64
connected = session_fixtures.connected


def call(op, args, select='parent'):
    return {'schema_version': 1, 'op': op, 'version': '1', 'select': select, 'args': args}


@pytest.fixture(autouse=True)
def spike_operations(monkeypatch):
    from astrid.sdk.timeline import _collections, _command_state
    from astrid.sdk.timeline import inverse as inverse_module

    config, address = State.config, _command_state.logical_address
    dependents = inverse_module._asset_dependents

    def parent_registry_view(state, owner):
        value = config(state, owner)
        # Existing asset primitives address config.registry; main's parent uses
        # a direct registry. Prototype only the missing accessor, never relocate it.
        if owner == 'parent' and 'registry' in state.bundle['parent']:
            if 'registry' in value:
                raise CommandError('dual registry storage is outside this spike')
            return {**value, 'registry': state.bundle['parent']['registry']}
        return value

    def registry_address(ref, path):
        if ref == 'parent' and tuple(path[:1]) == ('registry',):
            path = ('config', *path)
        return address(ref, path)

    def parent_asset_dependents(state, ref):
        # Reversal removes canonical parent rows before compile_mirrors runs.
        # Dependency checks must consume that current collection, not its mirror.
        snapshot = State(copy.deepcopy(state.bundle))
        snapshot.bundle['parent']['config']['clips'] = copy.deepcopy(state.collection('parent', 'clip'))
        return dependents(snapshot, ref)

    monkeypatch.setattr(State, 'config', parent_registry_view)
    monkeypatch.setattr(inverse_module, '_asset_dependents', parent_asset_dependents)
    for module in (_command_state, _collections, inverse_module):
        monkeypatch.setattr(module, 'logical_address', registry_address)

    def target(ctx, command):
        if command['select'] != 'parent' or ctx.select('collection.occurrences', 'parent'):
            raise CommandError('assembled replacement requires flat parent ownership')
        members = ctx.select('collection.clips', 'parent')
        if members != command['args']['replace_clips']:
            raise CommandError('explicit prior populated target required', kind='selection_changed')
        for ref in members:
            ctx.read(ref)

    def add(ctx, command):
        if command['select'] != 'parent':
            raise CommandError('parent media add requires raw parent ownership')
        row, pin = command['args']['row'], command['args']['media']
        value, kind = _verified(ctx, pin)
        # Same literal media checks as Bundle2, without an occurrence boundary.
        _clip(ctx, 'parent', row, float('inf'), kind, [value])
        _registry(ctx, 'parent', pin, kind, create=True, alias=row['asset'])
        ctx.create('parent', 'clip', row)

    registered = commands.operations()
    registered['spike.assembled-target'] = commands.Operation({
        'type': 'object', 'required': ['replace_clips'], 'additionalProperties': False,
        'properties': {'replace_clips': {'type': 'array', 'uniqueItems': True,
            'items': {'type': 'string', 'pattern': r'^parent/clip:(?!.*::)[^/]+$'}}}}, target, {})
    registered['spike.add-media'] = commands.Operation(
        commands._SCHEMA['$defs']['OccurrenceAddMediaArgs'], add, {})
    monkeypatch.setattr(commands, 'operations', lambda: registered)


def assembled_inputs():
    payload = _payload()
    payload['spec']['runtime_dependencies']['aggregation']['order'] = [MEDIA, MEDIA]
    for child in payload['resolved_children']:
        child['outputs'][0].update(object_id=MEDIA, media_id=MEDIA, content_sha256=MEDIA)
    assembled = build_authoring_proposal(payload)
    # Fixture inputs stand in for detached selected_media results, never for CAS custody.
    pins = [{'asset': 'variant-' + str(i), 'generation_id': 'generation-' + str(i),
             'variant_id': 'variant-' + str(i), 'object_id': MEDIA,
             'catalog_digest': 'sha256:' + str(i + 3) * 64} for i in (0, 1)]
    verified = [{'selection': pin, 'media_type': 'video/mp4', 'size': 123,
                 'duration_seconds': 2.5} for pin in pins]
    return assembled, pins, verified


def target_bundle(populated=False):
    document = delete_document()
    parent = document['parent_revision']['payload']
    parent['occurrences'] = []
    parent['config']['tracks'][0]['id'] = 'visual'
    parent['config']['tracks'][0]['opaque'] = [None, False, 'keep track']
    rows = parent['clips'] if populated else []
    for row in rows:
        row['track'] = 'visual'
    parent['clips'] = rows
    parent['config']['clips'] = copy.deepcopy(rows)
    document['shot_revisions'] = []
    document['internal_timeline_revisions'] = []
    document['dependency_manifest']['shots'] = []
    document['dependency_manifest']['internal_timelines'] = []
    document['parent_revision']['content_digest'] = _digest(parent)
    return bundle_from_document(document)


def lower(bundle, *, replace_clips=(), guarded=True):
    """Normalize legacy assembly ONCE, before capturing/hashing the settled proposal."""
    assembled, pins, verified = assembled_inputs()
    calls = [call('spike.assembled-target', {'replace_clips': list(replace_clips)})] if guarded else []
    calls.extend(call('clip.delete', {}, ref) for ref in replace_clips)
    if not any(row['id'] == 'visual' for row in State(bundle).config('parent')['tracks']):
        calls.append(call('track.create', {'row': assembled['timeline']['tracks'][0]}))
    for row, pin in zip(assembled['timeline']['clips'], pins):
        # Legacy assembly emits [from,to); native media recipes also require hold.
        row = {**row, 'hold': row['to'] - row['from']}
        calls.append(call('spike.add-media', {'row': row, 'media': pin}))
    return commands.execute(bundle, calls, verified_media=verified), verified


@pytest.mark.parametrize('populated', [False, True])
def test_assembled_insert_or_explicit_replace_exact_inverse_redo(populated):
    before = target_bundle(populated)
    old = copy.deepcopy(before)
    refs = ['parent/clip:' + row['id'] for row in before['parent']['clips']]
    plan, verified = lower(before, replace_clips=refs)
    assert before == old
    assert replay(plan, before, verified_media=verified).records == plan.records
    result = document_from_bundle(plan.bundle)
    reloaded = bundle_from_document(json.loads(json.dumps(result)))
    undone = inverse(reloaded, plan.records)
    # Pure immutable boundary fixture exercises existing manifest restoration;
    # it is not an acceptance receipt or a provider-acceptance simulation.
    entry = {'revision_id': result['parent_revision']['revision_id'],
             'previous': {'revision_id': before['source_mapping']['_runtime_document']['parent_revision']['revision_id']},
             'records': {'commands': plan.records}}
    history = AcceptedRecords([entry], plan.records, lambda _: (before, reloaded))
    assert document_from_bundle(undone.bundle, source_bundles=(before,), inverse_records=history) == document_from_bundle(before)
    accepted = accepted_boundaries(undone.records, reloaded, undone.bundle)
    assert document_from_bundle(inverse(undone.bundle, accepted).bundle) == result
    parent = result['parent_revision']['payload']
    assert parent['config']['tracks'] == old['parent']['config']['tracks']
    assert parent['config']['output'] == old['parent']['config']['output']
    assert parent['unknown'] == old['parent']['unknown']
    assert parent['registry']['assets']['picture'] == old['parent']['registry']['assets']['picture']
    assert document_from_bundle(before)['dependency_manifest']['media'][0] in result['dependency_manifest']['media']
    assert [row['id'] for row in parent['clips']] == [derive_clip_id('stitch-task-42', i) for i in (0, 1)]
    assert [row['asset'] for row in parent['clips']] == [derive_asset_key('stitch-task-42', i) for i in (0, 1)]
    assert [(row['at'], row['from'], row['to'], row['hold']) for row in parent['clips']] == [
        (0, 0, 1.5, 1.5), (1.5, 0, 2.5, 2.5)]
    media_records = plan.records[-2:]
    for i, record in enumerate(media_records):
        assert record['dependencies'] == [{'key': 'media.new', 'kind': 'media', 'policy': 'exact',
                                            'pin': verified[i]['selection']}]
        alias = derive_asset_key('stitch-task-42', i)
        assert alias != verified[i]['selection']['asset']
        assert {item['ref'] for item in record['created']} == {
            'parent/asset:' + alias, 'parent/clip:' + derive_clip_id('stitch-task-42', i)}
    assert plan.records[0]['writes'] == []
    assert all(write['ref'] != 'parent' for record in plan.records for write in record['writes'])


def test_parent_media_append_creates_visual_track_and_keeps_shared_closure_pins():
    document = document_fixture()
    before = bundle_from_document(document)
    # Generic parent add also composes without replacing existing occurrences.
    plan, _ = lower(before, guarded=False)
    after = document_from_bundle(plan.bundle)
    assert plan.records[0]['command']['op'] == 'track.create'
    for key in ('shot_revisions', 'internal_timeline_revisions'):
        assert after[key] == document[key]
    for key in ('shots', 'internal_timelines', 'documents'):
        assert after['dependency_manifest'][key] == document['dependency_manifest'][key]
    assert after['parent_revision']['payload']['occurrences'] == document['parent_revision']['payload']['occurrences']
    assert inverse(plan.bundle, plan.records).bundle == before


def test_empty_target_creates_first_track_without_overwriting_parent():
    before = target_bundle()
    before['parent']['config']['tracks'] = []
    plan, _ = lower(before)
    assert [record['command']['op'] for record in plan.records] == [
        'spike.assembled-target', 'track.create', 'spike.add-media', 'spike.add-media']
    assert inverse(plan.bundle, plan.records).bundle == before


def test_ordinary_add_collision_never_becomes_replacement():
    plan, verified = lower(target_bundle())
    before = copy.deepcopy(plan.bundle)
    with pytest.raises(CommandError) as error:
        commands.execute(plan.bundle, plan.commands[-2:], verified_media=verified)
    assert error.value.kind == 'identity_collision'
    assert plan.bundle == before


def test_parent_source_window_and_disjoint_opaque_edit_survive_replay_and_inverse():
    before = target_bundle()
    assembled, pins, verified = assembled_inputs()
    row = {**assembled['timeline']['clips'][0], 'from': .5, 'to': 2, 'hold': 1.5, 'speed': 1.25}
    plan = commands.execute(before, [call('spike.add-media', {'row': row, 'media': pins[0]})],
                            verified_media=verified)
    head = copy.deepcopy(before)
    head['parent']['unknown']['later'] = {'asset': row['asset'], 'literal': None}
    rebased = replay(plan, head, verified_media=verified)
    assert rebased.bundle['parent']['clips'] == [row]
    # Opaque values on the parent are neither normalized nor treated as edges.
    assert inverse(rebased.bundle, rebased.records).bundle == head
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later('parent',
            ['registry', 'assets', row['asset'], 'type'], 'video')])


def test_explicit_replacement_refuses_occurrence_ownership():
    before = bundle_from_document(document_fixture())
    refs = ['parent/clip:' + row['id'] for row in before['parent']['clips']]
    with pytest.raises(CommandError, match='flat parent ownership'):
        lower(before, replace_clips=refs)


def test_populated_target_requires_explicit_observed_replacement():
    before = target_bundle(True)
    with pytest.raises(CommandError, match='explicit prior populated target'):
        lower(before)
    assert before == target_bundle(True)


@pytest.mark.parametrize('damage', ['clip-collision', 'asset-collision', 'missing-media',
    'wrong-variant', 'wrong-catalog', 'target-value', 'target-order', 'target-member', 'track'])
def test_original_capture_refuses_collisions_missing_media_and_target_change(damage):
    before = target_bundle(True)
    refs = ['parent/clip:' + row['id'] for row in before['parent']['clips']]
    plan, verified = lower(before, replace_clips=refs)
    head = copy.deepcopy(before)
    if damage == 'clip-collision':
        row = copy.deepcopy(plan.commands[-1]['args']['row'])
        head['parent']['clips'].append(row)
    elif damage == 'asset-collision':
        State(head).config('parent')['registry']['assets'][derive_asset_key('stitch-task-42', 0)] = None
    elif damage == 'missing-media':
        verified.pop()
    elif damage in ('wrong-variant', 'wrong-catalog'):
        verified[0]['selection']['variant_id' if damage == 'wrong-variant' else 'catalog_digest'] = 'other'
    elif damage == 'target-value':
        head['parent']['clips'][0]['opaque']['values'].append('changed')
    elif damage == 'target-order':
        head['parent']['clips'].reverse()
    elif damage == 'target-member':
        head['parent']['clips'].pop()
    else:
        State(head).config('parent')['tracks'][0]['hidden'] = True
    head['parent']['config']['clips'] = copy.deepcopy(head['parent']['clips'])
    immutable = copy.deepcopy(head)
    with pytest.raises(CommandError):
        replay(plan, head, verified_media=verified)
    assert head == immutable


def test_registry_create_or_require_never_upserts_or_removes_reused_binding():
    before = target_bundle()
    alias = derive_asset_key('stitch-task-42', 0)
    pin = assembled_inputs()[1][0]
    binding = {'media_id': MEDIA, 'type': 'video',
               'generationId': pin['generation_id'], 'variantId': pin['variant_id']}
    State(before).config('parent')['registry']['assets'][alias] = binding
    plan, _ = lower(before)
    assert 'parent/asset:' + alias not in plan.commands[-2]['created']
    assert inverse(plan.bundle, plan.records).bundle == before
    binding['opaque'] = None
    with pytest.raises(CommandError, match='existing registry binding'):
        lower(before)


def test_intervening_aba_and_later_created_asset_dependents_refuse_undo():
    before = target_bundle()
    plan, _ = lower(before)
    ref = 'parent/asset:' + derive_asset_key('stitch-task-42', 0)
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later(ref, ['type'], 'video')])
    head = copy.deepcopy(plan.bundle)
    row = {**head['parent']['clips'][0], 'id': 'later-clip'}
    head['parent']['clips'].append(row)
    head['parent']['config']['clips'] = copy.deepcopy(head['parent']['clips'])
    with pytest.raises(CommandError):
        inverse(head, plan.records)


@pytest.mark.parametrize('args', [{'replace_clips': [], 'extra': None}, {'replace_clips': ['parent/clip:x'] * 2},
    {'replace_clips': ['occurrence:x/clip:y']}, {}])
def test_target_guard_args_are_closed(args):
    with pytest.raises(CommandError):
        commands.execute(target_bundle(), [call('spike.assembled-target', args)])


def test_settled_assembly_normalization_numeric_forwarding_and_normal_outbox(connected):
    plan, verified = lower(target_bundle())
    proposal = {'schema_version': 1, 'producer': {'task_id': 'stitch-task-42', 'attempt_id': 'attempt',
        'executor_id': 'worker', 'fence': 1, 'runtime_epoch': 2},
        'admitted_target': {'project_id': 'p', 'timeline_id': 't',
            'base_revision_id': 'r0', 'base_publication_id': 'pub0'},
        'commands': plan.commands, 'rationale': 'Review café assembly'}
    proposal['proposal_digest'] = _digest(proposal)
    raw = _json(proposal).encode()
    forwarded = subprocess.run(['node', '-e',
        "process.stdout.write(JSON.stringify(JSON.parse(require('fs').readFileSync(0,'utf8'))))"],
        input=raw, capture_output=True, check=True, timeout=15)
    forwarded = json.loads(forwarded.stdout)
    assert type(proposal['commands'][-2]['args']['row']['at']) is float
    assert type(forwarded['commands'][-2]['args']['row']['at']) is int
    batch = build_producer_batch(forwarded)
    descriptor = {'size': len(raw), 'digest': 'sha256:' + hashlib.sha256(raw).hexdigest()}
    check_forwarding(batch, descriptor, raw=raw)
    assert equal(batch['commands'][1:], plan.commands)
    assert commands.execute(target_bundle(), batch['commands'], verified_media=verified).bundle == plan.bundle
    session = open_session(connected)
    assert session.queue_proposal(forwarded) == batch['commands']
    state = session.outbox.read()
    assert state['base'] == {'revision_id': 'r0', 'publication_id': 'pub0'}
    assert state['pending'] == batch['commands']
    assert state['rationale'] == proposal['rationale']
    changed = copy.deepcopy(batch)
    changed['commands'][-2]['args']['row']['at'] = True
    with pytest.raises(ValueError, match='forwarded commands'):
        check_forwarding(changed, descriptor, raw=raw)
