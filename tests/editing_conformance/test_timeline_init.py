"""Guarded one-time initialization of a pristine empty parent (timeline.init v1)."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
from astrid.sdk.timeline._command_state import ABSENT, CommandError, State, present
from astrid.sdk.timeline._init_commands import capture_timeline_init
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.commands import _SCHEMA, execute, operations
from astrid.sdk.timeline.inverse import check_intervening
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse, later
from tests.timeline.test_authoring_bundle import _digest

GOLDEN = Path(__file__).parent / 'fixtures' / 'recipe_m2_timeline_init.json'
OUTPUT = {'resolution': '1280x720', 'fps': 30, 'file': 'output.mp4',
          'background': None, 'background_scale': None}
INIT = {'name': 'My Timeline', 'slug': 'my-timeline', 'output': OUTPUT}
V1 = {'id': 'V1', 'kind': 'visual', 'label': 'V1', 'scale': 1, 'fit': 'contain',
      'opacity': 1, 'blendMode': 'normal'}
A1 = {**V1, 'id': 'A1', 'kind': 'audio', 'label': 'A1'}


def empty_bundle():
    payload = {'config': {'clips': [], 'tracks': []}, 'registry': {}, 'clips': [], 'occurrences': []}
    parent = {'revision_id': 'parent-0', 'project_id': 'project-1', 'timeline_id': 'main',
              'content_digest': _digest(payload), 'payload': payload}
    return open_authoring_bundle(parent, shot_revisions=[], internal_timeline_revisions=[])


def call(**args):
    return {'schema_version': 1, 'op': 'timeline.init', 'version': '1', 'select': 'parent',
            'args': {**copy.deepcopy(INIT), **args}}


def test_init_writes_exact_authored_defaults_and_roundtrips():
    original = empty_bundle()
    snapshot = copy.deepcopy(original)
    command = capture_timeline_init(original, **INIT)
    plan = execute(original, [command])
    assert original == snapshot
    assert plan.bundle['parent'] == {
        'config': {'clips': [], 'tracks': [], 'output': OUTPUT},
        'registry': {'assets': {}}, 'clips': [],
        'name': 'My Timeline', 'slug': 'my-timeline'}
    # Explicit null is a present value and never the same as absence.
    assert State(plan.bundle).get('parent', ['config', 'output', 'background']) == present(None)
    assert State(plan.bundle).get('parent', ['config', 'theme']) == ABSENT
    assert command['expect'] == {
        'parent::config.output': ABSENT, 'parent::name': ABSENT, 'parent::slug': ABSENT,
        'parent::registry': present({})}
    assert [(w['path']) for w in plan.records[0]['writes']] == [
        ['config', 'output'], ['name'], ['slug'], ['registry']]
    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == original
    assert inverse(undone.bundle, undone.records).bundle == plan.bundle
    assert replay(plan, original).records == plan.records
    assert execute(original, [command]).records == plan.records
    assert compile_authoring_candidate(plan.bundle)


def test_golden_capture_matches_frozen_fixture():
    original = empty_bundle()
    command = capture_timeline_init(original, **INIT)
    plan = execute(original, [command])
    actual = {'bundle': original, 'command': command, 'after_bundle': plan.bundle,
              'records': plan.records}
    assert json.loads(json.dumps(actual)) == json.loads(GOLDEN.read_text())


def test_init_then_tracks_keep_command_order_and_unwind_lifo():
    original = empty_bundle()
    init = execute(original, [capture_timeline_init(original, **INIT)])
    a = capture_track_create(init.bundle, 'parent', V1)
    after_a = execute(init.bundle, [a])
    b = capture_track_create(after_a.bundle, 'parent', A1)
    result = execute(init.bundle, [a, b])
    assert [row['id'] for row in State(result.bundle).collection('parent', 'track')] == ['V1', 'A1']
    undone = inverse(result.bundle, result.records)
    assert undone.bundle == init.bundle
    assert inverse(undone.bundle, init.records).bundle == original
    # Init's writes are disjoint from the tracks, so undoing it keeps them.
    without_init = inverse(result.bundle, init.records).bundle
    assert State(without_init).get('parent', ['config', 'output']) == ABSENT
    assert [row['id'] for row in State(without_init).collection('parent', 'track')] == ['V1', 'A1']


@pytest.mark.parametrize('mutate', [
    lambda p: p['config'].__setitem__('output', {}),
    lambda p: p.__setitem__('name', 'Old'),
    lambda p: p.__setitem__('slug', ''),
    lambda p: p.__setitem__('registry', {'assets': {}}),
    lambda p: p['config']['tracks'].append({'id': 'V1', 'kind': 'visual'}),
    lambda p: p['config'].__setitem__('theme', None),
    lambda p: p.__setitem__('opaque_parent', {'keep': True}),
])
def test_init_refuses_any_non_pristine_parent(mutate):
    original = empty_bundle()
    mutate(original['parent'])
    with pytest.raises(CommandError) as error:
        execute(original, [call()])
    assert error.value.kind == 'not_pristine'


def test_init_refuses_established_timelines_and_second_init():
    with pytest.raises(CommandError) as error:
        execute(bundle(), [call()])
    assert error.value.kind == 'not_pristine'
    original = empty_bundle()
    initialized = execute(original, [call()])
    with pytest.raises(CommandError) as error:
        execute(initialized.bundle, [call()])
    assert error.value.kind == 'not_pristine'
    # Replaying onto a head that already carries the defaults, or that was
    # edited and undone, never applies them a second time.
    with pytest.raises(CommandError):
        replay(initialized, initialized.bundle)


def test_init_replay_refuses_intervening_writes():
    plan = execute(empty_bundle(), [call()])
    for ref, path in (('parent', ['config', 'output']), ('parent', ['name']),
                      ('parent', ['registry']), ('parent', ['clips'])):
        with pytest.raises(CommandError) as error:
            check_intervening(plan.records, [later(ref, path, None)])
        assert error.value.kind == 'intervening_write'
    check_intervening(plan.records, [later('parent/track:V1', [], {})])


@pytest.mark.parametrize('args', [
    {'extra': 1},
    {'output': {**OUTPUT, 'extra': 1}},
    {'output': {k: v for k, v in OUTPUT.items() if k != 'background'}},
    {'output': {k: v for k, v in OUTPUT.items() if k != 'background_scale'}},
    {'output': {**OUTPUT, 'resolution': '1280*720'}},
    {'output': {**OUTPUT, 'resolution': '0x720'}},
    {'output': {**OUTPUT, 'fps': 0}},
    {'output': {**OUTPUT, 'fps': True}},
    {'output': {**OUTPUT, 'fps': 29.97}},
    {'output': {**OUTPUT, 'file': ''}},
    {'output': {**OUTPUT, 'background': 3}},
    {'name': ''},
    {'slug': None},
])
def test_init_args_are_closed(args):
    with pytest.raises(CommandError):
        execute(empty_bundle(), [call(**args)])


@pytest.mark.parametrize('patch', [
    {'version': '2'}, {'select': 'parent/track:V1'}, {'select': None},
    {'intent': {'ripple': 'none'}}, {'op': 'timeline.init-all'}, {'op': 'timeline.root'}])
def test_init_envelope_is_exact(patch):
    command = {**call(), **patch}
    with pytest.raises(CommandError):
        execute(empty_bundle(), [command])


def test_init_is_registered_and_schema_validates_goldens():
    assert 'timeline.init' in operations()
    assert not list(Draft202012Validator(_SCHEMA).iter_errors(call()))
    assert list(Draft202012Validator(_SCHEMA).iter_errors({**call(), 'version': '2'}))
