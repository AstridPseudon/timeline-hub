"""clip.add-media v1: parent-owned media birth, replacement, guarded inverse and replay."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import _digest, _manifest, bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_auto_placement import auto_place_completion
from astrid.sdk.timeline.native_parent_media_commands import capture_clip_add_media
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse, later
from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm, inputs
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
)
from tests.sdk.test_timeline_commit_provider import (
    inverse as inverse_call,
)
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi,  # noqa: F401 -- autouse detached ABI fixture
)

FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_parent_media.json'
CHILD = 'parent/clip:born'
ASSET = 'parent/asset:reserved-new'


def parent_inputs(kind='image'):
    """The occurrence fixture plus a free parent lane 'overlay' holding one media clip."""
    document, old, new, verified = inputs(kind)
    payload = document['parent_revision']['payload']
    payload['config']['tracks'].append({'id': 'overlay', 'kind': 'visual', 'role': 'output'})
    for identity, at in (('ov-a', 0), ('ov-b', 5)):
        clip = {'id': identity, 'track': 'overlay', 'asset': 'picture', 'clipType': 'media', 'at': at, 'hold': 2}
        payload['config']['clips'].append(copy.deepcopy(clip))
        payload['clips'].append(copy.deepcopy(clip))
    document['parent_revision']['content_digest'] = _digest(payload)
    document['dependency_manifest'] = _manifest(document['shot_revisions'],
        document['internal_timeline_revisions'], document['dependency_manifest']['media'], [])
    return document, old, new, verified


def args(new, kind, **changes):
    value = {'id': 'born', 'track': 'overlay', 'at': 3, 'hold': 4 if kind == 'video' else 1.25, 'media': new}
    if kind == 'video':
        value.update({'from': 2, 'to': 6, 'speed': 2})
    return {**value, **changes}


def captured(kind='image', **changes):
    document, old, new, verified = parent_inputs(kind)
    bundle = bundle_from_document(document)
    command = capture_clip_add_media(bundle, args(new, kind, **changes), verified_media=verified)
    return document, bundle, command, verified


def plain(command):
    return {key: command[key] for key in ('schema_version', 'op', 'version', 'select', 'args', 'intent')}


def edit(bundle, ref, **values):
    """Write both parent clip mirrors, as every accepted edit does."""
    State(bundle).entity(ref).update(values)
    other = bundle['parent']['clips'] if State(bundle).parent_clip_path == ('config', 'clips') else (
        State(bundle).config('parent')['clips'])
    other[:] = copy.deepcopy(State(bundle).collection('parent', 'clip'))


def clip_ids(bundle):
    return [row['id'] for row in State(bundle).collection('parent', 'clip')]


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_exact_capture_replay_scoped_birth_and_inverse(kind):
    document, bundle, command, verified = captured(kind)
    before = copy.deepcopy(bundle)
    validate_command(command)
    plan = execute(bundle, [command], verified_media=verified)
    assert plan.commands == [command]
    assert bundle == before
    assert replay(plan, bundle, verified_media=verified).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    redone = inverse(undone.bundle, accepted_boundaries(undone.records, plan.bundle, undone.bundle))
    assert redone.bundle == plan.bundle
    assert command['created'] == [ASSET, CHILD]
    assert plan.bundle['placements'] == before['placements'] and plan.bundle['shots'] == before['shots']
    row = State(plan.bundle).entity(CHILD)
    assert (row['asset'], row['track'], row['clipType']) == ('reserved-new', 'overlay', kind)
    assert row['at'] == pytest.approx(round(3 * 30000 / 1001) * 1001 / 30000)
    if kind == 'video':
        assert (row['from'], row['to'], row['hold'], row['speed']) == (2, 6, 4, 2)
    assert State(plan.bundle).entity(ASSET)['media_id'] == command['args']['media']['object_id']
    assert clip_ids(plan.bundle)[-1] == 'born'
    output = document_from_bundle(plan.bundle)
    assert command['args']['media']['object_id'] in {pin['media_id'] for pin in output['dependency_manifest']['media']}


def test_portable_golden():
    golden = json.loads(FIXTURE.read_text())
    document, bundle, command, verified = captured('video')
    plan = execute(bundle, [command], verified_media=verified)
    assert golden == {'input': document, 'verified_media': verified, 'commands': [command],
                      'records': plan.records, 'output': document_from_bundle(plan.bundle)}


def test_existing_binding_is_required_exactly_without_birth():
    _, bundle, command, verified = captured()
    assets = State(bundle).registry_holder('parent')['registry']['assets']
    pin = command['args']['media']
    assets['reserved-new'] = {'media_id': pin['object_id'], 'type': 'image',
                              'generationId': pin['generation_id'], 'variantId': pin['variant_id']}
    plan = execute(bundle, [plain(command)], verified_media=verified)
    assert plan.commands[0]['created'] == [CHILD]
    assert inverse(plan.bundle, plan.records).bundle == bundle
    assets['reserved-new']['opaque'] = None
    with pytest.raises(CommandError, match='existing registry binding'):
        execute(bundle, [plain(command)], verified_media=verified)


@pytest.mark.parametrize('damage', ['missing-input', 'wrong-object', 'wrong-catalog', 'intent', 'occurrence',
    'no-track', 'occurrence-lane', 'hidden-track', 'audio-track', 'occupied-id', 'image-window', 'image-speed',
    'window', 'past-media', 'zero-hold', 'negative-at', 'boolean-speed', 'extra-arg', 'two-registries',
    'occupied-alias', 'birth', 'membership'])
def test_refusals_preserve_input(damage):
    kind = 'image' if damage.startswith('image') else 'video'
    _, bundle, command, verified = captured(kind)
    command = plain(command)
    if damage == 'missing-input':
        verified.pop()
    elif damage in ('wrong-object', 'wrong-catalog'):
        command['args']['media']['object_id' if damage == 'wrong-object' else 'catalog_digest'] = 'sha256:' + '9' * 64
    elif damage == 'intent':
        command['intent'] = {'ownership': 'occurrence'}
    elif damage == 'occurrence':
        command['select'] = 'occurrence:occ-a'
    elif damage == 'no-track':
        command['args']['track'] = 'nowhere'
    elif damage == 'occurrence-lane':
        command['args']['track'] = 'picture'
    elif damage == 'hidden-track':
        State(bundle).entity('parent/track:overlay')['hidden'] = True
    elif damage == 'audio-track':
        State(bundle).entity('parent/track:overlay')['kind'] = 'audio'
    elif damage == 'occupied-id':
        command['args']['id'] = 'ov-a'
    elif damage == 'image-window':
        command['args'].update({'from': 0, 'to': 1.25})
    elif damage == 'image-speed':
        command['args']['speed'] = 2
    elif damage == 'window':
        command['args']['to'] = 7
    elif damage == 'past-media':
        command['args'].update({'from': 4, 'to': 8})
    elif damage == 'zero-hold':
        command['args']['hold'] = 0
    elif damage == 'negative-at':
        command['args']['at'] = -1
    elif damage == 'boolean-speed':
        command['args']['speed'] = True
    elif damage == 'extra-arg':
        command['args']['row'] = {}
    elif damage == 'two-registries':
        State(bundle).config('parent')['registry'] = copy.deepcopy(bundle['parent']['registry'])
    elif damage == 'occupied-alias':
        State(bundle).registry_holder('parent')['registry']['assets']['reserved-new'] = None
    elif damage == 'birth':
        command['created'] = []
    else:
        State(bundle).config('parent')['clips'].insert(0, {'id': 'other', 'track': 'overlay'})
        bundle['parent']['clips'].insert(0, {'id': 'other', 'track': 'overlay'})
        command['selections'] = captured('video')[2]['selections']
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        execute(bundle, [command], verified_media=verified)
    assert bundle == before


def replaced(**changes):
    return captured('video', replace='ov-a', **changes)


def test_replace_removes_the_populated_clip_and_inverse_restores_its_slot():
    _, bundle, command, verified = replaced()
    plan = execute(bundle, [command], verified_media=verified)
    assert clip_ids(bundle) == ['clip-a', 'clip-b', 'ov-a', 'ov-b']
    assert clip_ids(plan.bundle) == ['clip-a', 'clip-b', 'ov-b', 'born']
    assert command['created'] == [ASSET, CHILD]
    assert replay(plan, bundle, verified_media=verified).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == bundle
    redone = inverse(undone.bundle, accepted_boundaries(undone.records, plan.bundle, undone.bundle))
    assert redone.bundle == plan.bundle


@pytest.mark.parametrize('damage', ['missing', 'other-track', 'not-media', 'unrelated-dependency', 'self'])
def test_replace_refuses_without_a_populated_same_track_target(damage):
    _, bundle, command, verified = replaced()
    command = plain(command)
    if damage == 'missing':
        command['args']['replace'] = 'gone'
    elif damage == 'other-track':
        command['args']['replace'] = 'clip-a'
    elif damage == 'not-media':
        del State(bundle).entity('parent/clip:ov-a')['asset']
    elif damage == 'unrelated-dependency':
        State(bundle).entity('parent/clip:ov-b')['app'] = {'astrid': {'on': 'word:x:0'}}
    else:
        command['args']['replace'] = 'born'
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        execute(bundle, [command], verified_media=verified)
    assert bundle == before


def test_asset_alias_inverse_is_guarded_by_dependents_and_aba():
    _, bundle, command, verified = captured()
    plan = execute(bundle, [command], verified_media=verified)
    edit(plan.bundle, 'parent/clip:ov-b', asset='reserved-new')
    with pytest.raises(CommandError, match='surviving dependents'):
        inverse(plan.bundle, plan.records)
    for ref, path in ((CHILD, ['hold']), (ASSET, ['type'])):
        value = State(plan.bundle).entity(ref)[path[0]]
        with pytest.raises(CommandError, match='intervening'):
            inverse(plan.bundle, plan.records, [later(ref, path, value)])


def test_disjoint_edit_rebases_and_a_taken_id_conflicts():
    _, bundle, command, verified = captured()
    plan = execute(bundle, [command], verified_media=verified)
    head = copy.deepcopy(bundle)
    edit(head, 'parent/clip:ov-b', at=6)
    rebased = replay(plan, head, verified_media=verified,
                     intervening_records=[later('parent/clip:ov-b', ['at'], 6)])
    assert State(rebased.bundle).entity('parent/clip:ov-b')['at'] == 6
    taken = copy.deepcopy(bundle)
    for rows in (State(taken).config('parent')['clips'], taken['parent']['clips']):
        rows.append({'id': 'born', 'track': 'overlay', 'clipType': 'text', 'at': 0, 'hold': 1})
    with pytest.raises(CommandError):
        replay(plan, taken, verified_media=verified)


def test_provider_exact_reload_inverse_redo_and_retired_ids():
    document, _, command, verified = captured('video')
    realm = MediaRealm(document, verified)
    created = realm.call([command])
    undo = realm.call([inverse_call([created['receipt']['receipt_id']])])
    assert undo['data']['canonical_document'] == document
    with pytest.raises(CommitRejected) as error:
        realm.call([command])
    assert error.value.failure['details']['reason'] == 'identity_collision'
    redo = realm.call([inverse_call([undo['receipt']['receipt_id']])])
    assert redo['data']['canonical_document'] == created['data']['canonical_document']


@pytest.mark.parametrize('kind, anchor, resolution, frame',
                         [('image', 'ov-a', 'anchor-after', 60), ('video', None, 'lane-end', 210),
                          ('image', 'gone', 'lane-end', 210)])
def test_completion_builder_places_a_parent_clip_after_the_anchor_or_at_the_track_end(
        kind, anchor, resolution, frame):
    document, _, new, verified = parent_inputs(kind)
    bundle = bundle_from_document(document)
    result = auto_place_completion(bundle, 'parent', 'born', new, ownership='parent',
                                   verified_media=verified, anchor=anchor, track='overlay')
    capture = result['capture']
    assert (capture['resolution'], capture['start_frame'], capture['seconds']) == (resolution, frame, 5)
    [command] = result['commands']
    assert (command['op'], command['args']['track']) == ('clip.add-media', 'overlay')
    plan = execute(bundle, result['commands'], verified_media=verified)
    assert inverse(plan.bundle, plan.records).bundle == bundle


def test_completion_builder_needs_a_parent_track_and_matching_ownership():
    document, _, new, verified = parent_inputs()
    bundle = bundle_from_document(document)
    with pytest.raises(CommandError):
        auto_place_completion(bundle, 'parent', 'born', new, ownership='parent', verified_media=verified)
    with pytest.raises(CommandError):
        auto_place_completion(bundle, 'parent', 'born', new, ownership='occurrence',
                              verified_media=verified, track='overlay')
