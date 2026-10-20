"""Shared-shot auto-placement: append, lane inheritance, start-frame shift over existing birth ops."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import bundle_from_document, document_from_bundle
from astrid.sdk.timeline.native_auto_placement import auto_place_shared, unplace_shared
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import accepted_boundaries, inverse
from tests.editing_conformance.test_recipe_occurrence_media import MediaRealm, inputs
from tests.sdk.test_timeline_commit_provider import (
    inverse as inverse_call,
)
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi,  # noqa: F401 -- autouse detached ABI fixture
)

OWNER = 'occurrence:occ-a'
CHILD = OWNER + '/clip:placed'
FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_shared_auto_placement.json'
# occ-a starts at 8 s at 30000/1001 fps (global frame 240). clip-a covers frames 270..330 and
# clip-b 390..450 on 'picture'; 'overlay' carries clip-c 270..510 (wider than the picture lane).
CLIP_A_START, CLIP_B_START, PICTURE_END, SHOT_END = 270, 390, 450, 510
CASES = {'image-append': ('image', None, None), 'video-append': ('video', None, None),
         'image-shift': ('image', CLIP_B_START, None), 'video-overlay-anchor': ('video', None, 'clip-c')}


def build(kind, *, frame=None, anchor=None, wide=True, **kwargs):
    document, _, new, verified = inputs(kind)
    bundle = bundle_from_document(document)
    state = State(bundle)
    if wide:
        state.occurrence(OWNER)['duration_ms'] = 20000
    internal = state.config(OWNER)
    internal['tracks'].append({'id': 'overlay', 'kind': 'visual'})
    internal['clips'].append({'id': 'clip-c', 'track': 'overlay', 'asset': 'picture', 'clipType': 'media',
                              'at': 1, 'hold': 8})
    result = auto_place_shared(bundle, OWNER, 'placed', new, ownership='occurrence',
                               verified_media=verified, frame=frame, anchor=anchor, **kwargs)
    return document, bundle, result, verified


def case(name):
    kind, frame, anchor = CASES[name]
    return build(kind, frame=frame, anchor=anchor)


@pytest.mark.parametrize('name', CASES)
def test_portable_goldens(name):
    _, bundle, result, verified = case(name)
    plan = execute(bundle, result['commands'], verified_media=verified)
    golden = json.loads(FIXTURE.read_text())[name]
    assert golden == {'commands': result['commands'], 'capture': result['capture'],
                      'child': State(plan.bundle).entity(CHILD)}


@pytest.mark.parametrize('name', CASES)
def test_exact_capture_replay_inverse_and_redo(name):
    _, bundle, result, verified = case(name)
    before = copy.deepcopy(bundle)
    [command] = result['commands']
    validate_command(command)
    assert json.loads(json.dumps(result, allow_nan=False)) == result
    plan = execute(bundle, [command], verified_media=verified)
    assert bundle == before
    assert plan.commands == [command]
    assert replay(plan, bundle, verified_media=verified).records == plan.records
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    redone = inverse(undone.bundle, accepted_boundaries(undone.records, plan.bundle, undone.bundle))
    assert redone.bundle == plan.bundle


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_append_goes_after_the_greatest_end_over_every_lane_with_the_four_second_hold(kind):
    _, bundle, result, verified = build(kind)
    capture = result['capture']
    assert (capture['resolution'], capture['start_frame'], capture['seconds']) == ('append', SHOT_END, 4)
    child = State(execute(bundle, result['commands'], verified_media=verified).bundle).entity(CHILD)
    assert child['at'] == pytest.approx(SHOT_END * 1001 / 30000 - 8)
    assert (child['clipType'], child['hold'], child['track']) == (kind, 4, 'picture')
    if kind == 'video':
        assert (child['from'], child['to'], child['speed']) == (0, 4, 1)


def test_append_to_an_empty_shot_starts_at_the_occurrence_start():
    _, bundle, _, verified = build('image')
    State(bundle).config(OWNER)['clips'].clear()
    result = auto_place_shared(bundle, OWNER, 'placed', verified[1]['selection'], ownership='occurrence',
                               verified_media=verified)
    assert result['capture']['start_frame'] == 240


def test_append_past_the_occurrence_window_is_refused_by_the_existing_boundary():
    # The window is fixed at migration; growing it needs an extent writer (see the design note).
    with pytest.raises(CommandError) as error:
        build('image', wide=False)
    assert error.value.kind == 'occurrence_boundary'


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_lane_is_the_anchor_lane_when_the_anchor_is_in_the_shot_else_the_occurrence_lane(kind):
    _, bundle, result, verified = build(kind, anchor='clip-c')
    assert result['capture']['lane'] == 'overlay'
    assert State(execute(bundle, result['commands'], verified_media=verified).bundle).entity(CHILD)['track'] == 'overlay'
    for anchor in ('gone', None, 'clip-a'):
        other = build(kind, anchor=anchor)[2]['capture']
        assert (other['lane'], other['anchor']['state']) == (
            'picture', 'absent' if anchor in ('gone', None) else 'present')


def test_the_anchor_never_moves_the_start():
    assert build('image', anchor='clip-a')[2]['capture']['start_frame'] == SHOT_END


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_an_occupied_start_frame_shifts_by_one_while_interval_overlap_is_allowed(kind):
    _, bundle, result, verified = build(kind, frame=CLIP_B_START)
    capture = result['capture']
    assert (capture['resolution'], capture['requested_frame'], capture['skipped'], capture['start_frame']) == (
        'explicit', CLIP_B_START, [CLIP_B_START], CLIP_B_START + 1)
    # A start inside clip-b's interval but not equal to any start is kept (legacy allows overlap).
    assert build(kind, frame=CLIP_B_START + 5)[2]['capture']['start_frame'] == CLIP_B_START + 5


def test_the_shift_chains_over_consecutive_taken_starts_and_clamps_negative_frames():
    _, bundle, first, verified = build('image', frame=CLIP_B_START)
    taken = execute(bundle, first['commands'], verified_media=verified).bundle
    again = auto_place_shared(taken, OWNER, 'second', first['capture']['media'], ownership='occurrence',
                              verified_media=verified, frame=CLIP_B_START)
    assert (again['capture']['skipped'], again['capture']['start_frame']) == (
        [CLIP_B_START, CLIP_B_START + 1], CLIP_B_START + 2)
    # A negative frame clamps to 0, which is before the occurrence start, so the boundary refuses.
    with pytest.raises(CommandError) as error:
        auto_place_shared(bundle, OWNER, 'early', first['capture']['media'], ownership='occurrence',
                          verified_media=verified, frame=-7)
    assert error.value.kind == 'occurrence_boundary'


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_the_exact_completed_variant_is_bound_and_the_other_occurrence_is_untouched(kind):
    _, bundle, result, verified = build(kind)
    plan = execute(bundle, result['commands'], verified_media=verified)
    binding = State(plan.bundle).entity(OWNER + '/registry')['assets']['reserved-new']
    assert (binding['generationId'], binding['variantId']) == ('generation-new', 'variant-new')
    assert plan.bundle['parent'] == bundle['parent']
    assert State(plan.bundle).config('occurrence:occ-b') == State(bundle).config('occurrence:occ-b')


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_an_unowned_shared_legacy_or_display_owner_is_refused_without_touching_input(kind):
    _, bundle, _, verified = build(kind)
    pin = verified[1]['selection']
    shared = copy.deepcopy(bundle)
    shared['placements'][1]['shot_id'] = shared['placements'][0]['shot_id']
    legacy = copy.deepcopy(bundle)
    legacy['parent']['config']['pinnedShotGroups'] = [{'shotId': 'g', 'clipIds': [], 'poolGenerationIds': []}]
    for head, owner, ownership, refusal in [
            (shared, OWNER, 'occurrence', 'unsupported_ownership'),
            (bundle, 'parent', 'occurrence', 'unsupported_ownership'),
            (bundle, OWNER + '::display', 'occurrence', 'unsupported_ownership'),
            (bundle, OWNER, 'shared', 'unsupported_ownership'),
            (legacy, OWNER, 'occurrence', 'migration_needed')]:
        before = copy.deepcopy(head)
        with pytest.raises(CommandError) as error:
            auto_place_shared(head, owner, 'placed', pin, ownership=ownership, verified_media=verified)
        assert error.value.kind == refusal
        assert head == before


def test_unverified_unsupported_or_too_short_media_is_refused():
    _, bundle, _, verified = build('image')
    pin = verified[1]['selection']
    with pytest.raises(CommandError):
        auto_place_shared(bundle, OWNER, 'placed', pin, ownership='occurrence', verified_media=[])
    audio = copy.deepcopy(verified)
    audio[1]['media_type'] = 'audio/fixture'
    with pytest.raises(CommandError) as error:
        auto_place_shared(bundle, OWNER, 'placed', pin, ownership='occurrence', verified_media=audio)
    assert error.value.kind == 'unsupported_media'
    # The legacy hold ignored media length; a native video row authors a 0..4 window, so it refuses.
    _, vbundle, result, vverified = build('video')
    short = copy.deepcopy(vverified)
    short[1]['duration_seconds'] = 3
    with pytest.raises(CommandError):
        execute(vbundle, result['commands'], verified_media=short)


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_replay_keeps_the_recorded_start_when_the_anchor_moved_or_the_shot_grew(kind):
    _, bundle, result, verified = build(kind, anchor='clip-c')
    plan = execute(bundle, result['commands'], verified_media=verified)
    head = copy.deepcopy(bundle)
    State(head).entity(OWNER + '/clip:clip-c')['at'] = 0.5
    rebased = replay(plan, head, verified_media=verified)
    assert rebased.commands == plan.commands
    assert State(rebased.bundle).entity(CHILD)['at'] == State(plan.bundle).entity(CHILD)['at']
    assert inverse(rebased.bundle, rebased.records).bundle == head


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_replay_refuses_when_a_shot_clip_was_deleted_meanwhile_and_a_rebuild_appends_after_the_rest(kind):
    _, bundle, result, verified = build(kind, anchor='clip-c')
    plan = execute(bundle, result['commands'], verified_media=verified)
    head = copy.deepcopy(bundle)
    rows = State(head).config(OWNER)['clips']
    rows[:] = [row for row in rows if row['id'] != 'clip-c']
    with pytest.raises(CommandError):
        replay(plan, head, verified_media=verified)
    rebuilt = auto_place_shared(head, OWNER, 'placed', verified[1]['selection'], ownership='occurrence',
                                verified_media=verified, anchor='clip-c')
    assert (rebuilt['capture']['anchor']['state'], rebuilt['capture']['lane'], rebuilt['capture']['start_frame']) == (
        'absent', 'picture', PICTURE_END)


def test_unplace_removes_the_image_expression_keeps_the_binding_and_is_guarded():
    _, bundle, result, verified = build('image')
    placed = execute(bundle, result['commands'], verified_media=verified).bundle
    plan = execute(placed, unplace_shared(placed, OWNER, 'placed', ownership='occurrence')['commands'])
    assert 'placed' not in {row['id'] for row in State(plan.bundle).collection(OWNER, 'clip')}
    assert 'reserved-new' in State(plan.bundle).entity(OWNER + '/registry')['assets']
    assert inverse(plan.bundle, plan.records).bundle == placed


@pytest.mark.parametrize('kind', ['image', 'video'])
def test_provider_accepts_shared_placement_with_exact_undo_and_redo(kind):
    _, bundle, result, verified = build(kind)
    document = document_from_bundle(bundle)
    realm = MediaRealm(document, verified)
    created = realm.call(result['commands'])
    undo = realm.call([inverse_call([created['receipt']['receipt_id']])])
    assert undo['data']['canonical_document'] != created['data']['canonical_document']
    redo = realm.call([inverse_call([undo['receipt']['receipt_id']])])
    assert redo['data']['canonical_document'] == created['data']['canonical_document']
    assert document_from_bundle(bundle_from_document(created['data']['canonical_document'])) == (
        created['data']['canonical_document'])


# Pool membership has no canonical representation or writer (design/m2-auto-placement.md, BLOCKED).
# Each test keeps the legacy expectation and flips to passing when `shot.pool` lands.
POOL_REQUIREMENT = 'needs shot.pool (design/m2-auto-placement.md BLOCKED)'


@pytest.mark.xfail(strict=True, reason=POOL_REQUIREMENT)
def test_a_null_frame_records_pool_membership_without_a_clip():
    _, bundle, _, verified = build('image')
    result = auto_place_shared(bundle, OWNER, 'placed', verified[1]['selection'], ownership='occurrence',
                               verified_media=verified, pooled=True)
    plan = execute(bundle, result['commands'], verified_media=verified)
    assert State(plan.bundle).collection(OWNER, 'clip') == State(bundle).collection(OWNER, 'clip')
    assert result['capture']['resolution'] == 'pooled'


@pytest.mark.xfail(strict=True, reason=POOL_REQUIREMENT)
def test_keep_as_pooled_removes_the_clip_and_keeps_membership():
    _, bundle, result, verified = build('image')
    placed = execute(bundle, result['commands'], verified_media=verified).bundle
    unplaced = unplace_shared(placed, OWNER, 'placed', ownership='occurrence', keep_as_pooled=True)
    plan = execute(placed, unplaced['commands'])
    assert 'placed' not in {row['id'] for row in State(plan.bundle).collection(OWNER, 'clip')}
