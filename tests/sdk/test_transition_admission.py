"""Actual SDK transaction → existing evaluator → admitted shared planner."""
import copy
import json
import os
from pathlib import Path

import pytest

from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline.transitions import TransitionAuthoringError
from astrid.packs.rendering.actions.timeline_visualize.motion import element_motion

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def runtime(tmp_path, monkeypatch):
    # A disposable package-context link to exact admitted source, not an install.
    package = Path(os.environ.get('TRANSITIONS_TEST_EVALUATION_PACKAGE',
        str(ROOT / 'remotion/vendor/timeline-composition')))
    assert package.is_dir(), 'Provide the admitted evaluation package for this focused test'
    project = tmp_path / 'renderer'
    (project / 'node_modules/@banodoco').mkdir(parents=True)
    (project / 'package.json').write_text('{"private":true}')
    (project / 'node_modules/@banodoco/timeline-composition').symlink_to(package, target_is_directory=True)
    esbuild = Path(os.environ.get('TRANSITIONS_TEST_ESBUILD', str(ROOT / 'remotion/node_modules/esbuild')))
    assert esbuild.is_dir(), 'Provide the existing renderer esbuild for this focused test'
    (project / 'node_modules/esbuild').symlink_to(esbuild, target_is_directory=True)
    node = os.environ.get('TRANSITIONS_TEST_NODE', 'node')
    monkeypatch.setattr(element_motion, '_runtime', lambda: (node, project))
    return project


def checkout(start=1):
    bundle = json.loads((ROOT / 'tests/fixtures/timeline_editing/tiny.json').read_text())
    internal = bundle['shots']['A']['internal_timeline']
    internal['tracks'].append({'id': 'transition-test', 'kind': 'visual'})
    internal['clips'].extend([
        {'id': 'transition-a', 'at': 0, 'hold': 1, 'track': 'transition-test', 'clipType': 'media'},
        {'id': 'transition-b', 'at': start, 'hold': 1, 'track': 'transition-test', 'clipType': 'media'},
    ])
    return Checkout(bundle)


@pytest.mark.parametrize('start', [1, 1.5])
def test_sdk_normal_look_edit_admits_touching_and_gaps(runtime, start):
    tl = checkout(start)
    tl.clip('transition-a').look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    assert tl.clip('transition-a').data['transition'] == {'id': 'cross-fade', 'durationFrames': 9}
    assert tl.clip('transition-b').at == start
    assert len(tl._journal) == 1


def test_sdk_overlap_refuses_with_next_step_and_rolls_back(runtime):
    tl = checkout(0.9)
    before = copy.deepcopy(tl.document())
    with pytest.raises(TransitionAuthoringError, match='Move or trim') as error:
        tl.clip('transition-a').look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    assert error.value.code == 'transition/same-track-overlap'
    assert error.value.next_step
    assert tl.document() == before
    assert tl._journal == []


def test_sdk_unsupported_renderer_refuses_and_rolls_back(runtime, monkeypatch):
    def missing():
        raise element_motion.Unavailable('evaluation export absent')
    monkeypatch.setattr(element_motion, '_runtime', missing)
    tl = checkout()
    before = copy.deepcopy(tl.document())
    with pytest.raises(TransitionAuthoringError, match='Next step') as error:
        tl.clip('transition-a').look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    assert error.value.code == 'transition/unsupported-host'
    assert tl.document() == before


def test_sdk_legacy_load_and_unrelated_edit_do_not_reinterpret_transition(monkeypatch):
    tl = checkout(0.9)
    clip = tl.clip('transition-a')
    clip.data['transition'] = {'id': 'cross-fade'}  # legacy implicit default
    original = copy.deepcopy(clip.data['transition'])
    monkeypatch.setattr(element_motion, 'admit_transitions', lambda _: pytest.fail('legacy path invoked admission'))
    clip.look.set(opacity=0.5)
    assert clip.data['transition'] == original
    assert tl.clip('transition-b').at == 0.9


def test_sdk_new_implicit_duration_refuses_explicitly_before_host_lookup(monkeypatch):
    tl = checkout()
    monkeypatch.setattr(element_motion, 'admit_transitions', lambda _: pytest.fail('no duration should reach host'))
    before = copy.deepcopy(tl.document())
    with pytest.raises(TransitionAuthoringError, match='explicit duration'):
        tl.clip('transition-a').look.set(transition='crossfade')
    assert tl.document() == before


def test_existing_evaluator_refuses_unknown_host_with_shared_next_step(runtime):
    request = {'trackIds': ['v'], 'clips': [], 'authored': [], 'fps': 30, 'host': 'browser-export'}
    result = element_motion.admit_transitions([request])
    assert not result['ok']
    assert result['error']['code'] == 'transition/unsupported-host'
    assert result['error']['nextStep']


def test_sdk_invalid_renderer_configuration_is_explicit_and_rolls_back(monkeypatch):
    def invalid():
        raise ValueError('renderer directory must be absolute')
    monkeypatch.setattr(element_motion, '_runtime', invalid)
    tl = checkout()
    before = copy.deepcopy(tl.document())
    with pytest.raises(TransitionAuthoringError, match='Next step') as error:
        tl.clip('transition-a').look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    assert error.value.code == 'transition/unsupported-host'
    assert tl.document() == before


def test_sdk_later_timing_edit_cannot_create_overlap_on_transition_track(runtime):
    tl = checkout()
    tl.clip('transition-a').look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    before = copy.deepcopy(tl.document())
    count = len(tl._journal)
    with pytest.raises(TransitionAuthoringError, match='Move or trim'):
        tl.clip('transition-b').on(0.9)
    assert tl.document() == before
    assert len(tl._journal) == count


def test_raw_patch_params_and_duration_reach_shared_admission(runtime, monkeypatch):
    seen = []
    original = element_motion.admit_transitions

    def capture(requests):
        seen.extend(copy.deepcopy(requests))
        return original(requests)

    monkeypatch.setattr(element_motion, 'admit_transitions', capture)
    tl = checkout()
    raw = {'type': 'crossfade', 'duration': 0.317123456789, 'params': {'opaque': [None, {}]}}
    tl.clip('transition-a').look.set(transition=raw)
    assert seen[0]['authored'][0]['transition'] == raw
    # The established codec still owns persisted legacy shape.
    assert tl.clip('transition-a').data['transition'] == {'id': 'cross-fade', 'durationFrames': 10}


def test_resolver_cannot_erase_raw_authored_overlap_before_admission(runtime, monkeypatch):
    tl = checkout(0.9)
    before = copy.deepcopy(tl.document())
    resolve = tl.resolve

    def clear_transition(*args, **kwargs):
        result = resolve(*args, **kwargs)
        tl.clip('transition-a').data.pop('transition', None)
        return result

    monkeypatch.setattr(tl, 'resolve', clear_transition)
    from astrid.sdk.timeline.commands import CommandError
    with pytest.raises(CommandError, match='timing replaced an explicit write'):
        tl.clip('transition-a').look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    assert tl.document() == before
    assert tl._journal == []


def test_refusal_restores_retained_clip_view(runtime):
    tl = checkout(0.9)
    clip = tl.clip('transition-a')
    data = clip.data
    before = copy.deepcopy(data)
    with pytest.raises(TransitionAuthoringError):
        clip.look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    assert clip.data is data and data == before


def test_transition_removal_remains_a_recovery_without_host(monkeypatch):
    tl = checkout(0.9)
    tl.clip('transition-a').data['transition'] = {'id': 'cross-fade'}
    monkeypatch.setattr(element_motion, 'admit_transitions', lambda _: pytest.fail('removal invoked host'))
    tl.clip('transition-a').look.set(transition=None)
    assert not tl.clip('transition-a').data.get('transition')


# Reuse the existing current DFI declaration fixtures and real public transaction path.
from test_timeline_composite_effects import baseline, bundle, ref  # noqa: E402,F401
from test_timeline_composite_effects import apply, transition  # noqa: E402


def test_pinned_incoming_transition_keeps_destination_payload(runtime, bundle, ref):
    raw = transition(ref, params={'opaque': [None, {}]})
    after, plan = apply(bundle, raw)
    clip = Checkout(after).clip('a-next')
    assert clip.data['transition'] == raw['args']['transition']
    assert clip.data['elementRef'] == raw['args']['elementRef']
    assert len(plan.calls) == 1


def test_pinned_transition_refuses_nonadjacent_peer_overlap(runtime, bundle, ref):
    rows = bundle['shots']['A']['internal_timeline']['clips']
    template = copy.deepcopy(next(r for r in rows if r['id'] == 'a-next'))
    rows.extend([{**copy.deepcopy(template), 'id': 'extra-a', 'at': 4, 'hold': 1},
                 {**copy.deepcopy(template), 'id': 'extra-b', 'at': 4.5, 'hold': 1}])
    before = copy.deepcopy(bundle)
    with pytest.raises(TransitionAuthoringError, match='Move or trim') as error:
        apply(bundle, transition(ref))
    assert error.value.code == 'transition/same-track-overlap'
    assert bundle == before


def test_pinned_transition_immediate_overlap_has_next_step(runtime, bundle, ref):
    next(row for row in bundle['shots']['A']['internal_timeline']['clips']
         if row['id'] == 'a-next')['at'] = 1.9
    with pytest.raises(TransitionAuthoringError, match='Move or trim') as error:
        apply(bundle, transition(ref))
    assert error.value.code == 'transition/same-track-overlap'


def test_pinned_transition_later_timing_overlap_rolls_back(runtime, bundle, ref):
    after, _ = apply(bundle, transition(ref))
    tl = Checkout(after)
    before = copy.deepcopy(tl.document())
    clip = tl.clip('a-next')
    with pytest.raises(TransitionAuthoringError, match='Move or trim'):
        clip.on(1.9)
    assert tl.document() == before
    assert tl._journal == []


@pytest.mark.parametrize('payload', [[], {'admission': {'ok': False}}, {'admission': {'ok': True}}])
def test_malformed_evaluator_result_is_typed_and_atomic(runtime, monkeypatch, payload):
    from types import SimpleNamespace
    monkeypatch.setattr(element_motion.subprocess, 'run', lambda *a, **k:
                        SimpleNamespace(returncode=0, stdout=json.dumps(payload)))
    tl = checkout()
    before = copy.deepcopy(tl.document())
    with pytest.raises(TransitionAuthoringError, match='Next step') as error:
        tl.clip('transition-a').look.set(transition={'id': 'cross-fade', 'durationFrames': 9})
    assert error.value.code == 'transition/unsupported-host'
    assert tl.document() == before
    assert tl._journal == []


def test_inverse_in_batch_does_not_exempt_new_authoring(runtime, bundle, ref):
    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline.inverse import inverse_command
    from astrid.sdk.timeline.transaction import edit_transaction
    next(row for row in bundle['shots']['A']['internal_timeline']['clips']
         if row['id'] == 'a-next')['transition'] = {'id': 'fade', 'durationFrames': 8}
    after, plan = apply(bundle, transition(ref))
    inverse = inverse_command(plan.calls, bundle, after, 'test-publication', consequences=plan.consequences)
    tl = Checkout(after)
    before = copy.deepcopy(tl.document())
    with pytest.raises(TransitionAuthoringError) as error:
        with edit_transaction(tl, 'inverse then new authoring', persist=False, quiet=True):
            commands.execute(tl, inverse)
            commands.execute(tl, {'op': 'clip.set-look', 'select': 'occurrence:occ-A/clip:a-next',
                                 'args': {'transition': {'id': 'cross-fade', 'durationFrames': 9}}})
    assert error.value.code == 'transition/invalid-owner'
    assert tl.document() == before
    assert tl._journal == []


def test_same_frame_legacy_timing_edit_does_not_reinterpret(monkeypatch):
    tl = checkout(0.9)
    clip = tl.clip('transition-b')
    tl.clip('transition-a').data['transition'] = {'id': 'cross-fade'}
    monkeypatch.setattr(element_motion, 'admit_transitions', lambda _: pytest.fail('same frame invoked host'))
    clip.on(0.901)
    assert clip.start_frame == 27


def test_pinned_invalid_destination_owner_rolls_back(runtime, bundle, ref):
    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline.transaction import edit_transaction
    tl = Checkout(bundle)
    before = copy.deepcopy(tl.document())
    value = transition(ref)
    value['select'] = 'occurrence:occ-A/clip:a-transition-from'
    with pytest.raises(commands.TimelineEditError, match='adjacent predecessor'):
        with edit_transaction(tl, 'invalid owner', persist=False, quiet=True):
            commands.execute(tl, value)
    assert tl.document() == before
    assert tl._journal == []


def test_pinned_authoring_refuses_unavailable_host(runtime, bundle, ref, monkeypatch):
    def missing():
        raise element_motion.Unavailable('evaluation export absent')
    monkeypatch.setattr(element_motion, '_runtime', missing)
    with pytest.raises(TransitionAuthoringError, match='Next step') as error:
        apply(bundle, transition(ref))
    assert error.value.code == 'transition/unsupported-host'
