"""Synthetic BED-CLOCK witnesses; these are not the named v9/v11 or film proof."""
import copy

import pytest

from astrid.core.timeline.audio_envelope import compile_legacy, evaluate
from astrid.core.timeline.cuts import clip_duration
from astrid.sdk.timeline.bed_adoption import adopt_music_bed
from astrid.sdk.timeline.compiler import compile_timing
from astrid.sdk.timeline.music_beds import adopted, project, sources, validate
from astrid.sdk.timeline_checkout import Checkout, describe_changes
from tests.sdk.test_music_beds import tiny

REFERENCE = 'occurrence:occ-A/clip:a-music'
OTHER = 'occurrence:occ-A/clip:synthetic-arrangement'


def synthetic_bed(*, reference_length=8., other_length=8., other_start=0.):
    tl = tiny()
    reference = tl.clip('a-music').data
    reference.update(speed=2., **{'from': 2., 'to': 2. + 2. * reference_length})
    reference.setdefault('app', {}).setdefault('astrid', {})['beats'] = dict(
        beats=[2., 6., 10., 14., 18., 22., 26.],
        downbeats=[2., 6., 10., 14., 18., 22., 26.], time='cue_seconds')
    second = copy.deepcopy(reference)
    second.update(id='synthetic-arrangement', at=other_start, speed=3., **{'from': 39.06, 'to': 39.06 + 3. * other_length})
    # A contradictory beat grid must never select a second seam plan.
    second['app']['astrid']['beats'] = dict(beats=[40.56, 43.56, 46.56],
                                          downbeats=[40.56, 43.56, 46.56], time='cue_seconds')
    tl._internal('A')['clips'].append(second)
    return Checkout(adopt_music_bed(tl.document(), [REFERENCE, OTHER],
        switches=[dict(id='synthetic-switch', on='4s', duration=2., curve='equal-power')],
        alignment={REFERENCE: dict(confidence=1., source_offset_s=2.),
                   OTHER: dict(confidence=1., source_offset_s=39.06 - 3. * other_start)}))


def pieces(tl, owner):
    entry = sources(tl)[owner]
    return [copy.deepcopy(c) for c in tl._internal('A')['clips'] if c['id'] in entry['outputs']]


@pytest.mark.parametrize('delta', [-1., 1.])
@pytest.mark.parametrize('other_start', [0., 2.])
def test_synthetic_shared_u_skip_repeat_and_existing_envelope(delta, other_start):
    tl = synthetic_bed(other_start=other_start)
    original = {o: copy.deepcopy(e['source']) for o, e in sources(tl).items()}
    if delta > 0:
        tl.insert_time(5, delta)
    else:
        tl.ripple_delete(5, 6)
    bed = adopted(tl)
    assert bed['ripple_basis'] == [dict(at_s=5., delta_s=delta)]
    for owner, offset, rate in [(REFERENCE, 2., 2.), (OTHER, 39.06 - 3. * other_start, 3.)]:
        left, right = pieces(tl, owner)
        # The reference chooses u=4, regardless of the other source's beats/rate.
        assert left['to'] == pytest.approx(offset + rate * 4.125)
        assert right['at'] == 3.875
        assert right['from'] == pytest.approx(offset + rate * (3.875 - delta))
        assert right['at'] + clip_duration(right) == pytest.approx(8. + delta + (other_start if owner == OTHER else 0.))
        assert left['params']['fadeOut'] == right['params']['fadeIn'] == .25
        # Consume the actual generated fade fields through the existing compiler.
        # The envelope wins over params when forwarded to the consumer: once only.
        for clip, incoming in [(left, False), (right, True)]:
            envelope = compile_legacy(clip, tl.fps)
            assert envelope is not None and len(envelope['multiply']) == 1
            curve = envelope['multiply'][0]['keyframes']
            middle = (curve[0]['at'] + curve[1]['at']) / 2
            assert evaluate(envelope, middle) == pytest.approx(.5)
            assert evaluate(envelope, curve[0]['at']) == (0 if incoming else 1)
            assert evaluate(envelope, curve[1]['at']) == (1 if incoming else 0)
            forwarded = dict(clip, audio=dict(envelope=envelope))
            assert compile_legacy(forwarded, tl.fps) == envelope
        assert sources(tl)[owner]['source'] == original[owner]
        assert sources(tl)[owner]['ripple_basis'] is bed['ripple_basis']
    validate(tl)


@pytest.mark.parametrize('delta', [-1., 1.])
def test_synthetic_edit_after_reference_end_updates_the_one_basis(delta):
    tl = synthetic_bed(reference_length=6., other_length=12.)
    if delta > 0:
        tl.insert_time(7, 1)
    else:
        tl.ripple_delete(7, 8)
    assert adopted(tl)['ripple_basis'] == [dict(at_s=7., delta_s=delta)]
    left, right = pieces(tl, OTHER)
    assert left['to'] == pytest.approx(39.06 + 3. * 6.125)
    assert right['at'] == 5.875
    assert right['from'] == pytest.approx(39.06 + 3. * (5.875 - delta))
    assert right['at'] + clip_duration(right) == pytest.approx(12. + delta)
    validate(tl)


def test_synthetic_repeated_edits_reorder_reload_and_compile_are_deterministic(tmp_path):
    tl = synthetic_bed()
    original = copy.deepcopy(adopted(tl)['arrangements'])
    tl.insert_time(5, 1)
    tl.insert_time(5, 1)
    assert adopted(tl)['ripple_basis'] == [dict(at_s=5., delta_s=2.)]
    assert adopted(tl)['arrangements'] == original
    outputs = {o: pieces(tl, o) for o in sources(tl)}
    assert all(len(clips) == 2 for clips in outputs.values())
    ids = [c['id'] for clips in outputs.values() for c in clips]
    assert len(ids) == len(set(ids))
    adopted(tl)['arrangements'].reverse()
    project(tl)
    assert adopted(tl)['owner'] == REFERENCE
    assert {o: pieces(tl, o) for o in sources(tl)} == outputs
    # Generated clips can be absent: their dictionaries are never new inputs.
    tl._internal('A')['clips'][:] = [c for c in tl._internal('A')['clips'] if c['id'] not in ids]
    project(tl)
    assert {o: pieces(tl, o) for o in sources(tl)} == outputs
    path = tmp_path / 'synthetic-bed.json'
    tl.save(path, quiet=True)
    loaded = Checkout.load(path)
    before = loaded.document()
    assert compile_timing(before).bundle == before
    loaded.resolve()
    loaded.resolve()
    assert loaded.document() == before
    assert {o: pieces(loaded, o) for o in sources(loaded)} == outputs


def test_synthetic_temporary_plays_on_preserves_shared_mapping():
    tl = synthetic_bed()
    tl.insert_time(5, 1)
    before = copy.deepcopy(adopted(tl))
    outputs = {o: pieces(tl, o) for o in sources(tl)}
    prior = Checkout(tl.document())
    tl.insert_time(5, 1, music='plays_on')
    assert adopted(tl) == before
    assert {o: pieces(tl, o) for o in sources(tl)} == outputs
    assert tl.music == 'keep_end'
    assert any('plays on' in note and 'end' in note for note in describe_changes(prior, tl))


def test_synthetic_reference_bar_clustering_uses_timeline_seconds():
    tl = synthetic_bed()
    tl.insert_time(2.5, .5)
    tl.insert_time(5.5, .5)
    assert adopted(tl)['ripple_basis'] == [dict(at_s=2.5, delta_s=.5), dict(at_s=5.5, delta_s=.5)]
    # Reference bars are 4 source seconds / rate 2 = 2 timeline seconds.
    # Three seconds between edits must remain two seams for every arrangement.
    for owner in sources(tl):
        output = pieces(tl, owner)
        assert len(output) == 3
        assert len({c['id'] for c in output}) == 3
    before = tl.document()
    tl.resolve()
    assert tl.document() == before
    validate(tl)


def test_synthetic_second_identical_reflow_is_an_exact_no_op():
    tl = synthetic_bed(reference_length=10., other_length=10.)
    tl.reflow(gaps={'a-vo': 1.})
    assert adopted(tl)['ripple_basis']
    before = tl.document()
    tl.reflow(gaps={'a-vo': 1.})
    assert tl.document() == before
    assert compile_timing(before).bundle == before
