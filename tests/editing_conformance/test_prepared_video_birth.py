"""Focused prepared-video parent birth coverage over the existing carrier."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.native_parent_media_commands import capture_clip_add_media
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import later
from tests.editing_conformance.test_recipe_m2_parent_media import ordered_parent


def _video_case(hold):
    bundle, media, verified = ordered_parent('video')
    for rows in (bundle['parent']['clips'], bundle['parent']['config']['clips']):
        source = next(row for row in rows if row['id'] == 'target')
        source.update({'clipType': 'video', 'from': 2, 'to': 2.01, 'speed': 2,
                       'transition': {'type': 'crossfade', 'duration': .5},
                       'opaque': {'values': [None, False, [], {}]}})
        if hold == 'missing':
            source.pop('hold', None)
        else:
            source['hold'] = hold
    return bundle, media, verified


@pytest.mark.parametrize('hold', ['missing', None])
def test_prepared_video_birth_clones_raw_row_and_ripples_same_track(hold):
    bundle, media, verified = _video_case(hold)
    before = copy.deepcopy(bundle)
    command = capture_clip_add_media(
        bundle, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
        after='parent/clip:target', verified_media=verified)

    row = command['args']['row']
    assert row['id'] == 'born' and row['asset'] == media['asset']
    assert row['track'] == 'overlay' and row['from'] == 2 and row['to'] == 2.01
    assert row['speed'] == 2 and row['transition']['type'] == 'crossfade'
    assert row['opaque'] == {'values': [None, False, [], {}]}
    if hold == 'missing':
        assert 'hold' not in row
    else:
        assert row['hold'] is None
    assert bundle == before

    plan = execute(bundle, [command], verified_media=verified)
    created = State(plan.bundle).entity('parent/clip:born')
    assert created == row
    assert created['at'] == pytest.approx(.05)
    assert State(plan.bundle).entity('parent/clip:C')['at'] == pytest.approx(.05)
    assert State(plan.bundle).entity('parent/clip:A')['at'] == 0
    assert plan.bundle['parent']['clips'] == plan.bundle['parent']['config']['clips']
    assert any(item['key'] == 'collection.clips.after'
               for item in plan.records[0]['command']['selections'])
    assert plan.records[0]['command']['bindings']['parent.after-clip'] == 'parent/clip:target'


def test_prepared_video_birth_preserves_subminimum_source_duration_but_ripples_floor():
    bundle, media, verified = _video_case(.01)
    for rows in (bundle['parent']['clips'], bundle['parent']['config']['clips']):
        source = next(row for row in rows if row['id'] == 'target')
        source.pop('from', None)
        source.pop('to', None)
    command = capture_clip_add_media(
        bundle, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
        after='parent/clip:target', verified_media=verified)
    plan = execute(bundle, [command], verified_media=verified)
    assert plan.records[0]['command']['args']['row']['hold'] == .01
    assert State(plan.bundle).entity('parent/clip:born')['at'] == pytest.approx(.05)
    assert State(plan.bundle).entity('parent/clip:C')['at'] == pytest.approx(.05)


@pytest.mark.parametrize('hold', ['missing', None])
def test_prepared_video_shape_is_opt_in_and_nonvideo_or_ordinary_birth_stays_strict(hold):
    bundle, media, verified = _video_case(hold)
    ordinary = {'id': 'born', 'clipType': 'video', 'track': 'overlay', 'asset': media['asset'],
                'at': 0, 'from': 2, 'to': 2.01, 'speed': 2}
    if hold is None:
        ordinary['hold'] = None
    with pytest.raises(CommandError):
        capture_clip_add_media(bundle, ordinary, media, verified_media=verified)

    nonvideo = copy.deepcopy(bundle)
    for rows in (nonvideo['parent']['clips'], nonvideo['parent']['config']['clips']):
        source = next(row for row in rows if row['id'] == 'target')
        source['clipType'] = 'image'
    with pytest.raises(CommandError):
        capture_clip_add_media(
            nonvideo, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
            after='parent/clip:target', verified_media=[{**verified[0], 'media_type': 'image/fixture'}])


@pytest.mark.parametrize('damage', ['anchor', 'peer', 'membership', 'order', 'aba'])
def test_prepared_video_birth_refuses_stale_anchor_membership_order_or_peer(damage):
    bundle, media, verified = _video_case('missing')
    command = capture_clip_add_media(
        bundle, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
        after='parent/clip:target', verified_media=verified)
    plan = execute(bundle, [command], verified_media=verified)
    head = copy.deepcopy(bundle)
    if damage == 'anchor':
        next(row for row in head['parent']['clips'] if row['id'] == 'target')['at'] = 1
        next(row for row in head['parent']['config']['clips'] if row['id'] == 'target')['at'] = 1
        changed = later('parent/clip:target', ['at'], 1)
    elif damage == 'peer':
        for rows in (head['parent']['clips'], head['parent']['config']['clips']):
            next(row for row in rows if row['id'] == 'C')['at'] = 6
        changed = later('parent/clip:C', ['at'], 6)
    elif damage == 'membership':
        for rows in (head['parent']['clips'], head['parent']['config']['clips']):
            rows.append({'id': 'foreign', 'track': 'overlay', 'asset': 'picture',
                         'clipType': 'video', 'at': 9, 'hold': 1})
        changed = later('parent', ['clips'], head['parent']['clips'])
    else:
        for rows in (head['parent']['clips'], head['parent']['config']['clips']):
            rows.reverse()
        changed = later('parent', ['clips'], head['parent']['clips'])
        if damage == 'aba':
            for rows in (head['parent']['clips'], head['parent']['config']['clips']):
                rows.reverse()
    with pytest.raises(CommandError):
        replay(plan, head, verified_media=verified, intervening_records=[changed])


def test_prepared_video_birth_refuses_malformed_window_nonfinite_rate_and_foreign_anchor():
    bundle, media, verified = _video_case('missing')
    malformed = copy.deepcopy(bundle)
    for rows in (malformed['parent']['clips'], malformed['parent']['config']['clips']):
        source = next(row for row in rows if row['id'] == 'target')
        source['from'], source['to'] = 3, 2
    with pytest.raises(CommandError):
        capture_clip_add_media(
            malformed, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
            after='parent/clip:target', verified_media=verified)

    foreign = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        capture_clip_add_media(
            foreign, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
            after='occurrence:occ-a', verified_media=verified)

    invalid_rate = copy.deepcopy(bundle)
    invalid_rate['parent']['config']['output']['fps'] = 0
    with pytest.raises(CommandError):
        capture_clip_add_media(
            invalid_rate, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
            after='parent/clip:target', verified_media=verified)

    command = capture_clip_add_media(
        bundle, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
        after='parent/clip:target', verified_media=verified)
    command['args']['row']['from'] = float('inf')
    with pytest.raises(CommandError):
        execute(bundle, [command], verified_media=verified)


def test_ordinary_parent_birth_keeps_transition_refusal_even_for_negative_duration():
    bundle, media, verified = _video_case('missing')
    row = {'id': 'born', 'clipType': 'video', 'track': 'overlay', 'asset': media['asset'],
           'at': 0, 'hold': .01, 'from': 2, 'to': 2.01, 'speed': 2,
           'transition': {'type': 'crossfade', 'duration': -1}}
    with pytest.raises(CommandError):
        capture_clip_add_media(bundle, row, media, verified_media=verified)

