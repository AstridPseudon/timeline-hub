"""Native parent media trim: main source-unit semantics and exact preservation."""
from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

from astrid.core.timeline.duration import clip_timeline_duration
from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline._trim_commands import capture_clip_trim
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline_checkout import Clip
from tests.sdk.test_timeline_commit_provider_document import document_fixture

REF = 'parent/clip:clip-a'


def media_bundle(*, source_type='image', app=None):
    document = document_fixture(shared=False)
    payload = document['parent_revision']['payload']
    for rows in (payload['clips'], payload['config']['clips']):
        rows[0].update(at=1, **{'from': 2, 'to': 6, 'speed': 2, 'hold': 17})
        rows[0]['app'] = copy.deepcopy(app or {'astrid': {'for': 19, 'until': None},
                                               'org.example': {'literal': 'clip-a'}})
    payload['registry'] = copy.deepcopy(payload['registry'])
    payload['registry']['assets']['picture'].update(type=source_type, duration=10)
    document['parent_revision']['content_digest'] = _digest(payload)
    return bundle_from_document(document)


def clip(bundle):
    return State(bundle).entity(REF)


def test_trim_matches_main_model_and_keeps_hold_in_source_units(monkeypatch):
    original = media_bundle()
    row = copy.deepcopy(clip(original))
    monkeypatch.setattr(Clip, '_source_duration', lambda self: 10)
    Clip(SimpleNamespace(_is_audio=lambda *args: False), None, row).trim(in_s=1, out_s=5)
    plan = execute(original, [capture_clip_trim(original, REF, in_s=1, out_s=5)])
    assert clip(plan.bundle) == row
    assert clip(plan.bundle)['hold'] == 4
    assert clip_timeline_duration(clip(plan.bundle)) == pytest.approx(2)


def test_trim_accepts_static_move_intent_but_refuses_dynamic_follow():
    original = media_bundle(app={'astrid': {'fixed_start': True, 'for': 2}})
    plan = execute(original, [capture_clip_trim(original, REF, in_s=1, out_s=5)])
    assert clip(plan.bundle)['app']['astrid']['fixed_start'] is True
    assert 'for' not in clip(plan.bundle)['app']['astrid']
    dynamic = media_bundle(app={'astrid': {'on': 'word:one'}})
    with pytest.raises(CommandError, match='does not support'):
        capture_clip_trim(dynamic, REF, in_s=1, out_s=5)
    transitioned = media_bundle()
    clip(transitioned)['transition'] = 'crossfade'
    with pytest.raises(CommandError, match='does not support transition'):
        capture_clip_trim(transitioned, REF, in_s=1, out_s=5)
