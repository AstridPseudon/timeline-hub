"""Prepared-video parent birth over the existing clip.add-media carrier."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.native_parent_media_commands import capture_clip_add_media
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance import test_commit_runtime_parent_media as parent_runtime
from tests.editing_conformance.test_recipe_m1_commands import later
from tests.editing_conformance.test_recipe_m2_parent_media import ordered_parent


def _video_case(hold=4):
    bundle, media, verified = ordered_parent('video')
    for rows in (bundle['parent']['clips'], bundle['parent']['config']['clips']):
        source = next(row for row in rows if row['id'] == 'target')
        source.update({'clipType': 'video', 'at': 1, 'from': 2, 'to': 6, 'speed': 2,
                       'transition': {'type': 'crossfade', 'duration': .5},
                       'nullable': None, 'opaque': {'values': [None, False, [], {}]}})
        source['hold'] = hold
        next(row for row in rows if row['id'] == 'C')['at'] = 5
    return bundle, media, verified


def _birth(bundle, media, verified):
    return capture_clip_add_media(
        bundle, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
        after='parent/clip:target', verified_media=verified)


def test_prepared_video_birth_matches_normalized_production_and_schema():
    bundle, media, verified = _video_case()
    before = copy.deepcopy(bundle)
    command = _birth(bundle, media, verified)

    # This is the exact public carrier shape; schema validation happens before
    # the provider is entered and must not rewrite the request.
    validate_command(command)
    row = command['args']['row']
    assert row == {
        'id': 'born', 'clipType': 'video', 'track': 'overlay', 'asset': media['asset'],
        'at': 3, 'hold': 2, 'transition': {'type': 'crossfade', 'duration': .5},
        'nullable': None, 'opaque': {'values': [None, False, [], {}]},
    }
    assert all(key not in row for key in ('from', 'to', 'speed', 'at_ms'))
    assert bundle == before

    plan = execute(bundle, [command], verified_media=verified)
    created = State(plan.bundle).entity('parent/clip:born')
    assert created == row
    assert State(plan.bundle).entity('parent/clip:C')['at'] == pytest.approx(7)
    assert State(plan.bundle).entity('parent/clip:A')['at'] == 0
    assert plan.bundle['parent']['clips'] == plan.bundle['parent']['config']['clips']
    assert any(item['key'] == 'collection.clips.after'
               for item in plan.records[0]['command']['selections'])
    assert plan.records[0]['command']['bindings']['parent.after-clip'] == 'parent/clip:target'


def test_prepared_video_birth_uses_production_duration_floor():
    bundle, media, verified = _video_case(.01)
    command = _birth(bundle, media, verified)
    validate_command(command)
    assert command['args']['row']['hold'] == .05
    plan = execute(bundle, [command], verified_media=verified)
    assert State(plan.bundle).entity('parent/clip:born')['at'] == pytest.approx(1.05)
    assert State(plan.bundle).entity('parent/clip:C')['at'] == pytest.approx(5.05)


@pytest.mark.parametrize('field, value', [('hold', None), ('hold', 'missing'), ('clipType', None)])
def test_prepared_video_request_controls_are_schema_strict(field, value):
    bundle, media, verified = _video_case()
    before = copy.deepcopy(bundle)
    command = _birth(bundle, media, verified)
    if value == 'missing':
        del command['args']['row'][field]
    else:
        command['args']['row'][field] = value
    with pytest.raises(CommandError):
        validate_command(command)
    assert bundle == before


def test_prepared_video_provider_refuses_a_nonproducer_row_without_write():
    bundle, media, verified = _video_case()
    command = _birth(bundle, media, verified)
    command['args']['row']['hold'] = 1
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError, match='captured source clone'):
        execute(bundle, [command], verified_media=verified)
    assert bundle == before


def test_prepared_video_birth_refuses_stale_anchor_membership_order_or_peer():
    bundle, media, verified = _video_case()
    command = _birth(bundle, media, verified)
    plan = execute(bundle, [command], verified_media=verified)
    for damage in ('anchor', 'peer', 'membership', 'order', 'aba'):
        head = copy.deepcopy(bundle)
        if damage == 'anchor':
            for rows in (head['parent']['clips'], head['parent']['config']['clips']):
                next(row for row in rows if row['id'] == 'target')['at'] = 2
            changed = later('parent/clip:target', ['at'], 2)
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


def test_prepared_video_birth_refuses_bad_source_and_foreign_anchor_without_write():
    bundle, media, verified = _video_case()
    malformed = copy.deepcopy(bundle)
    for rows in (malformed['parent']['clips'], malformed['parent']['config']['clips']):
        source = next(row for row in rows if row['id'] == 'target')
        source.pop('hold')
        source['from'], source['to'] = 3, 2
    with pytest.raises(CommandError):
        _birth(malformed, media, verified)

    foreign = copy.deepcopy(bundle)
    before = copy.deepcopy(foreign)
    with pytest.raises(CommandError):
        capture_clip_add_media(
            foreign, {'id': 'born', 'track': 'overlay', 'asset': media['asset']}, media,
            after='occurrence:occ-a', verified_media=verified)
    assert foreign == before


def test_ordinary_birth_and_image_after_insert_keep_strict_existing_rules():
    bundle, media, verified = _video_case()
    ordinary = {'id': 'born', 'clipType': 'video', 'track': 'overlay', 'asset': media['asset'],
                'at': 0, 'hold': 2, 'from': 2, 'to': 4, 'speed': 1,
                'transition': {'type': 'crossfade', 'duration': .5}}
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        capture_clip_add_media(bundle, ordinary, media, verified_media=verified)
    assert bundle == before

    image_bundle, image, image_verified = ordered_parent('image')
    image_before = copy.deepcopy(image_bundle)
    command = capture_clip_add_media(
        image_bundle, {'id': 'born', 'track': 'overlay', 'asset': image['asset']}, image,
        after='parent/clip:target', verified_media=image_verified)
    validate_command(command)
    assert command['args']['row']['at'] == 4 and command['args']['row']['hold'] == 4
    assert image_bundle == image_before
    plan = execute(image_bundle, [command], verified_media=image_verified)
    assert [row['id'] for row in State(plan.bundle).collection('parent', 'clip')] == [
        'A', 'target', 'born', 'C']


@pytest.mark.integration
def test_prepared_video_public_preview_accept_retry_and_undo(tmp_path, monkeypatch):
    """The normalized carrier survives Runtime preview, acceptance, retry and undo."""
    editing = next(parent_runtime.media_realm(
        tmp_path, monkeypatch, 'video', historical=False, pristine=False))
    try:
        old = editing.pins['old']
        new = editing.pins['new']

        def call(row, pin):
            return {'schema_version': 1, 'op': 'clip.add-media', 'version': '1',
                    'select': 'parent', 'args': {'row': row, 'media': pin}}

        source = {'id': 'target', 'clipType': 'video', 'track': 'visual',
                  'asset': old['asset'], 'at': 1, 'from': 2, 'to': 6,
                  'hold': 4, 'speed': 2, 'nullable': None,
                  'opaque': {'source': ['managed', None, False]}}
        sibling = {'id': 'C', 'clipType': 'video', 'track': 'visual',
                   'asset': old['asset'], 'at': 5, 'from': 0, 'to': 2,
                   'hold': 2, 'speed': 1}
        parent_runtime.commit(editing, parent_runtime.body(editing, [call(source, old)]), 'video-source')
        parent_runtime.commit(editing, parent_runtime.body(editing, [call(sibling, old)]), 'video-sibling')

        baseline = parent_runtime.current(editing)
        row = {'id': 'born', 'clipType': 'video', 'track': 'visual', 'asset': new['asset'],
               'at': 3, 'hold': 2, 'nullable': None,
               'opaque': {'source': ['managed', None, False]}}
        command = {**call(row, new), 'select': 'parent/clip:target'}

        before_preview = parent_runtime.rows(editing)
        preview = parent_runtime.commit(
            editing, parent_runtime.body(editing, [command], dry_run=True), 'video-preview')
        assert preview['receipt'] is None
        assert parent_runtime.current(editing) == baseline
        assert parent_runtime.rows(editing) == before_preview

        request = parent_runtime.body(editing, [command])
        accepted = parent_runtime.commit(editing, request, 'video-accept')
        retry = parent_runtime.commit(editing, request, 'video-accept')
        assert retry == accepted
        after = parent_runtime.current(editing)
        born = next(row for row in after['parent_revision']['payload']['clips']
                    if row['id'] == 'born')
        assert born == row
        assert next(row for row in after['parent_revision']['payload']['clips']
                    if row['id'] == 'C')['at'] == pytest.approx(7)

        undone = parent_runtime.undo(editing, accepted, 'video-undo')
        assert undone['data']['canonical_document'] == baseline
        assert parent_runtime.current(editing) == baseline
    finally:
        editing.service.close()
