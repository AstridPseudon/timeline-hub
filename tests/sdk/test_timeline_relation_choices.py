"""Exact authored relation choices: real recorder/compiler/rebase, synthetic inputs."""
import copy
import json
from pathlib import Path

import pytest

from astrid.core.timeline import moments as mo
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands, inverse, relations
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.transaction import edit_transaction

SID = 'occurrence:occ-A/clip:a-rocket'
NEIGHBOUR = 'occurrence:occ-A/clip:a-vo'


def base():
    from astrid.sdk.timeline.identity import retain_cut_reservations
    tl = Checkout(json.loads((Path(__file__).parents[1] / 'fixtures/timeline_editing/tiny_publishable.json').read_text()))
    retain_cut_reservations(tl.bundle)
    return tl.document()


def apply(bundle, *calls):
    tl = Checkout(copy.deepcopy(bundle))
    with edit_transaction(tl, 'relation gesture', quiet=True, persist=False) as tx:
        tx.canonical = True
        for call in calls:
            commands.execute(tl, call)
    return tl.document(), tx.plan


def call(op='clip.nudge', target=SID, **args):
    return dict(op=op, select=target, args=args)


def choice(action, *, edge='start', target=SID, **fields):
    return dict(target=target, edge=edge, choice=action, **fields)


@pytest.fixture(params=['word', 'music', 'neighbour', 'sequence'])
def tied(request):
    tl = Checkout(base())
    clip = tl.clip('a-rocket')
    if request.param == 'word':
        text = '"viral"'
    elif request.param == 'music':
        intent.set_beats(tl.clip('a-music').data, dict(beats=[0, 1, 2, 3], downbeats=[0, 2]))
        text = 'beat 1 after "went"'
    elif request.param == 'neighbour':
        text = f'clip-end "{NEIGHBOUR}"'
    else:
        data = copy.deepcopy(tl.clip('a-plate').data)
        data.update(id='step-one', at=.2, hold=.4)
        data['app'] = {'astrid': {'v': 2}}
        intent.set_sequence(data, 'synthetic-steps', 0)
        second = copy.deepcopy(data)
        second.update(id='step-two', at=.6)
        intent.set_sequence(second, 'synthetic-steps', 1)
        tl._internal('A')['clips'].extend([data, second])
        text = 'clip-start "occurrence:occ-A/clip:step-two"'
    intent.set_on(clip.data, text)
    clip._set_start(tl._moment_time(text, clip))
    tl._command_depth = 1
    tl.resolve()
    return tl.document(), text


@pytest.mark.parametrize('action', relations.CHOICES)
def test_choices_across_authored_relation_kinds(tied, action):
    bundle, text = tied
    old = Checkout(bundle).clip(SID).start
    fields = {'offset_frames': 9} if action == 'adjust-offset' else {}
    if action == 're-anchor':
        fields = dict(anchor=f'clip-start "{NEIGHBOUR}"', offset_frames=9)
    frames = 0 if action in {'keep', 'cancel'} else 9
    after, plan = apply(bundle, call(frames=frames, relation_choices=[choice(action, **fields)]))
    clip = Checkout(after).clip(SID)
    if action == 'cancel':
        assert after == bundle and not plan.calls and not plan.changed
        return
    assert len(plan.calls) == 1
    assert plan.calls[0].args['relation_affected']
    if action == 'keep':
        assert intent.on(clip.data) == text and clip.start == old
    elif action == 'detach':
        assert intent.on(clip.data) is None and clip.start == pytest.approx(old + .3)
    elif action == 'adjust-offset':
        assert mo.parse(intent.on(clip.data)) == mo.parse(text).with_offset(frames=9)
    else:
        assert intent.on(clip.data) == f'clip-start "{NEIGHBOUR}" +9f'
    replay, _ = apply(bundle, *plan.calls)
    assert replay == after


def test_keep_conflicts_atomically_and_plain_drag_retains_nine_frames(tied):
    bundle, text = tied
    with pytest.raises(commands.SemanticConflict, match='intent.on'):
        apply(bundle, call(frames=9, relation_choices=[choice('keep')]))
    after, plan = apply(bundle, call(frames=9))
    assert plan.calls[0].op == 'clip.on'
    assert mo.parse(intent.on(Checkout(after).clip(SID).data)).offset_frames == 9
    assert mo.parse(text).offset_frames == 0


@pytest.mark.parametrize('text', ['clip-start "occurrence:occ-A/clip:a-vo" +9f -0.1s',
                                  'clip-end "parent/clip:overlay" -2f',
                                  'beat 1 after clip-start "occurrence:occ-A/clip:a-vo" +2f'])
def test_reserved_parser_roundtrip(text):
    assert mo.parse(mo.format_moment(mo.parse(text))) == mo.parse(text)


@pytest.mark.parametrize('text', ['clip-start a-vo', 'clip-end "a-vo"', 'clip-start "occurrence:x/clip:y',
                                  'clip-start "occurrence:x/clip:y" rubbish',
                                  'clip-end "occurrence:x/clip:y" in s1', 'clip-start',
                                  'beat 1 after clip-start \"occurrence:x/clip:y\"\"',
                                  'clip-start "occurrence:x/clip:y" +2', 'clip-end "occurrence:x/clip:y" "oops"'])
def test_reserved_parser_never_falls_back_to_speech(text):
    with pytest.raises(mo.MomentError):
        mo.parse(text)


def test_exact_edge_binding_missing_and_cycle_are_atomic():
    bundle = base()
    text = f'clip-end "{NEIGHBOUR}" +9f'
    after, plan = apply(bundle, call('clip.on', moment=text))
    assert plan.calls[0].bindings[text] == NEIGHBOUR
    assert Checkout(after).clip(SID).start == pytest.approx(2.8)
    for text in ['clip-start "occurrence:gone/clip:a-vo"', f'clip-start "{SID}"']:
        with pytest.raises(commands.TimelineEditError):
            apply(bundle, call('clip.on', moment=text))
    cycle = Checkout(base())
    intent.set_on(cycle.clip('a-vo').data, f'clip-start "{SID}"')
    with pytest.raises(commands.TimelineEditError, match='CYCLE'):
        apply(cycle.document(), call('clip.on', moment=f'clip-end "{NEIGHBOUR}"'))


def test_ambiguous_occurrence_and_duplicate_clip_identity_refuse():
    for damage in ['occurrence', 'clip']:
        tl = Checkout(base())
        if damage == 'occurrence':
            tl.bundle['placements'].append(copy.deepcopy(tl.bundle['placements'][0]))
        else:
            tl._internal('A')['clips'].append(copy.deepcopy(tl.clip('a-vo').data))
        with pytest.raises(commands.TimelineEditError):
            apply(tl.document(), call('clip.on', moment=f'clip-start "{NEIGHBOUR}"'))


def media_end():
    tl = Checkout(base())
    clip = tl.clip('a-music')
    clip.data['hold'] = 4
    tl._registry('A')[clip.asset]['duration'] = 12
    intent.set_until(clip.data, 'end of c1')
    return tl.document(), commands.scoped_clip(tl, clip)


@pytest.mark.parametrize('action', ['keep', 'detach', 'adjust-offset', 're-anchor', 'cancel'])
def test_trim_end_choices_preserve_or_deliberately_replace_rule(action):
    bundle, sid = media_end()
    fields = dict(offset_seconds=-1) if action == 'adjust-offset' else {}
    if action == 're-anchor':
        fields = dict(anchor='end of c1', offset_seconds=-1)
    args = dict(out_s=4 if action == 'keep' else 3,
                relation_choices=[choice(action, edge='end', target=sid, **fields)])
    after, plan = apply(bundle, call('clip.trim', sid, **args))
    clip = Checkout(after).clip(sid)
    if action == 'cancel':
        assert after == bundle and not plan.calls
    elif action == 'keep':
        assert intent.until(clip.data) == 'end of c1'
    elif action == 'detach':
        assert intent.until(clip.data) is None and clip.duration == 3
    else:
        assert intent.until(clip.data) == 'end of c1 -1s' and clip.duration == 3
    assert apply(bundle, *plan.calls)[0] == after


def test_trim_and_duration_cannot_incidentally_clear_ties():
    bundle, sid = media_end()
    for op, args in [('clip.trim', dict(out_s=3)), ('clip.set-duration', dict(seconds=3))]:
        with pytest.raises(commands.SemanticConflict, match='intent.until'):
            apply(bundle, call(op, sid, **args))


@pytest.mark.parametrize('action', ['keep', 'detach', 'adjust-offset', 're-anchor', 'cancel'])
def test_duplicate_explicit_choices_preserve_source_and_replay_identity(action):
    bundle = base()
    old = Checkout(bundle).clip(SID).data
    fields = dict(offset_frames=9) if action == 'adjust-offset' else {}
    if action == 're-anchor':
        fields = dict(anchor=f'clip-start "{NEIGHBOUR}"', offset_frames=9)
    after, plan = apply(bundle, dict(op='timeline.add', select=None,
        args={'from': SID, 'at': 1.3 if action == 'keep' else 1.6,
              'relation_choices': [choice(action, **fields)]}))
    assert Checkout(after).clip(SID).data == old
    if action == 'cancel':
        assert after == bundle and not plan.calls
    else:
        assert plan.calls[0].created
        assert apply(bundle, *plan.calls)[0] == after


def test_newly_affected_relation_conflicts_on_rebase(tied):
    bundle, _ = tied
    _, plan = apply(bundle, call(frames=9, relation_choices=[choice('adjust-offset', offset_frames=9)]))
    head = Checkout(copy.deepcopy(bundle))
    intent.set_on(head.clip('b-type').data, f'clip-start "{SID}" +1s')
    result = rebase(plan.calls, head.document())
    assert result.document is None and result.conflicts[0]['path'] == 'relation_affected'


def test_late_failure_rolls_back_and_one_inverse_restores_gesture(tied):
    bundle, _ = tied
    tl = Checkout(copy.deepcopy(bundle))
    with pytest.raises(commands.TimelineEditError):
        with edit_transaction(tl, 'compound', quiet=True, persist=False):
            commands.execute(tl, call(frames=9, relation_choices=[choice('adjust-offset', offset_frames=9)]))
            commands.execute(tl, call('clip.set-duration', seconds=-1))
    assert tl.document() == bundle
    after, plan = apply(bundle, call(frames=9, relation_choices=[choice('adjust-offset', offset_frames=9)]))
    back = inverse.inverse_command(plan.calls, bundle, after, 'synthetic-publication', consequences=plan.consequences)
    assert apply(after, back)[0] == bundle


def test_closed_choice_fields_and_duplicate_edges_refuse():
    for rows in [[choice('guess')], [choice('keep', offset_frames=9)], [choice('adjust-offset')],
                 [choice('re-anchor', offset_frames=0)], [choice('keep'), choice('keep')],
                 [choice('adjust-offset', offset_frames=float('inf'))]]:
        with pytest.raises((commands.CommandError, mo.MomentError)):
            apply(base(), call(frames=9, relation_choices=rows))


def sequence_bundle():
    tl = Checkout(base())
    for i, name in enumerate(['actual-head', 'actual-tail']):
        data = copy.deepcopy(tl.clip('a-plate').data)
        data.update(id=name, at=.2 + i * .4, hold=.4, app={'astrid': {'v': 2}})
        intent.set_sequence(data, 'choice-sequence', i)
        tl._internal('A')['clips'].append(data)
    head = tl.clip('actual-head')
    intent.set_sequence_fit(head.data, dict(land='"viral"', weights=[12, 12]))
    tl._command_depth = 1
    tl.resolve()
    return tl.document(), 'occurrence:occ-A/clip:actual-head', 'occurrence:occ-A/clip:actual-tail'


@pytest.mark.parametrize('action', relations.CHOICES)
def test_sequence_land_uses_exact_head_identity(action):
    bundle, head, tail = sequence_bundle()
    fields = dict(offset_frames=9) if action == 'adjust-offset' else {}
    if action == 're-anchor':
        fields = dict(anchor=f'clip-end "{NEIGHBOUR}"', offset_frames=0)
    after, plan = apply(bundle, call('sequence.fit', 'choice-sequence',
        relation_choices=[choice(action, target=head, edge='sequence-land', **fields)]))
    if action == 'cancel':
        assert not plan.calls and after == bundle
    else:
        assert {head, tail} <= set(plan.calls[0].resolved)
        recipe = intent.sequence_fit(Checkout(after).clip(head).data)
        assert ('land' in (recipe or {})) == (action != 'detach')
        assert apply(bundle, *plan.calls)[0] == after


def test_sequence_step_membership_detach_and_keep():
    bundle, head, tail = sequence_bundle()
    # Make this a stable resolved captured base before attempting the gesture.
    bundle, _ = apply(bundle, call('sequence.fit', 'choice-sequence'))
    after, plan = apply(bundle, call(target=tail, frames=9,
        relation_choices=[choice('detach', target=tail, edge='sequence')]))
    assert intent.sequence(Checkout(after).clip(tail).data) is None
    assert intent.sequence(Checkout(after).clip(head).data)[1] == 0
    assert apply(bundle, *plan.calls)[0] == after
    with pytest.raises(commands.SemanticConflict):
        apply(bundle, call(target=tail, frames=9, relation_choices=[choice('keep', target=tail, edge='sequence')]))


def test_timing_clear_is_explicit_and_cancel_batch_is_no_write():
    bundle = base()
    after, _ = apply(bundle, call('clip.clear', keys=['on'], relation_choices=[choice('detach')]))
    assert intent.on(Checkout(after).clip(SID).data) is None
    with pytest.raises(commands.TimelineEditError, match='detach'):
        apply(bundle, call('clip.clear', keys=['on']))
    after, plan = apply(bundle, dict(op='timeline.batch', select=None, args=dict(commands=[
        call('clip.set', x=240), call(frames=9, relation_choices=[choice('cancel')]) ])))
    assert after == bundle and not plan.calls


def test_one_final_resolution_and_one_saved_undo(tmp_path, monkeypatch):
    monkeypatch.setenv('BANODOCO_LOCAL_DATA_ROOT', str(tmp_path / 'data'))
    tl = Checkout(base())
    tl.save(tmp_path / 'gesture.checkout.json', quiet=True)
    before = tl.document()
    original = Checkout.resolve
    resolutions = []
    def resolve(self, *args, **kwargs):
        if self is tl:
            resolutions.append(1)
        return original(self, *args, **kwargs)
    monkeypatch.setattr(Checkout, 'resolve', resolve)
    tl.batch([call(frames=9, relation_choices=[choice('adjust-offset', offset_frames=9)]), call('clip.set', x=120)])
    assert len(resolutions) == 1
    tl.save(quiet=True)
    tl.undo()
    assert tl.document() == before


def test_word_retiming_keeps_nine_frame_offset():
    after, _ = apply(base(), call(frames=9))
    tl = Checkout(after)
    words = intent.words(tl.clip('a-vo').data)
    words[2][0] += .2
    intent.set_line(tl.clip('a-vo').data, 's1', words)
    tl._command_depth = 1
    tl.resolve()
    assert intent.on(tl.clip(SID).data) == '"viral" +9f'
    assert tl.clip(SID).start == pytest.approx(1.8)


def test_relation_schema_matches_closed_producer():
    from jsonschema import Draft202012Validator
    validator = Draft202012Validator(relations.RELATION_CHOICE_SCHEMA)
    for action in relations.CHOICES:
        fields = dict(offset_frames=0) if action in {'adjust-offset', 're-anchor'} else {}
        if action == 're-anchor':
            fields['anchor'] = f'clip-start "{NEIGHBOUR}"'
        row = choice(action, **fields)
        validator.validate(row)
        assert relations.validate([row]) == [row]


def test_structural_ripple_captures_authored_affected_set_and_missing_choices():
    bundle = base()
    # Open time beyond narration: only B's authored duration is moved.
    b = 'occurrence:occ-B/clip:b-type'
    tl = Checkout(bundle)
    intent.set_until(tl.clip(b).data, 'end of c2')
    # A later authored dependent is part of the set even without screen overlap.
    intent.set_on(tl.clip(b).data, f'clip-start "{SID}" +3s')
    bundle = tl.document()
    rows = [choice('detach', target=b), choice('detach', target=b, edge='end')]
    value = dict(op='timeline.insert-time', select=None, args=dict(at=4.5, seconds=.3, relation_choices=rows))
    after, plan = apply(bundle, value)
    assert any(r['target'] == b for r in plan.calls[0].args['relation_affected'])
    assert apply(bundle, *plan.calls)[0] == after
    bad = copy.deepcopy(value)
    bad['args']['relation_choices'] = rows[:1]
    with pytest.raises(commands.SemanticConflict):
        apply(bundle, bad)


@pytest.mark.parametrize('action', relations.CHOICES)
def test_authored_bed_owner_choices_never_select_generated_span(action):
    from astrid.sdk.timeline import music_beds
    from tests.sdk.test_music_beds import tiny
    tl = tiny()
    tl.clip('a-music').on('"viral"')
    tl.insert_time(2, 1)
    owner = 'occurrence:occ-A/clip:a-music'
    before = tl.document()
    fields = dict(offset_frames=9) if action == 'adjust-offset' else {}
    if action == 're-anchor':
        fields = dict(anchor='"viral"', offset_frames=9)
    after, plan = apply(before, call(target=owner, frames=0,
        relation_choices=[choice(action, target=owner, **fields)]))
    if action == 'cancel':
        assert after == before and not plan.calls
        return
    assert plan.calls[0].resolved == (owner,)
    assert apply(before, *plan.calls)[0] == after
    generated = next(x for x in music_beds.sources(Checkout(after))[owner]['outputs'] if x != 'a-music')
    with pytest.raises(commands.TimelineEditError):
        apply(after, call(target='occurrence:occ-A/clip:' + generated, frames=9,
            relation_choices=[choice('detach', target='occurrence:occ-A/clip:' + generated)]))


def test_cancel_rolls_back_prior_commands_and_writes_no_saved_journal(tmp_path, monkeypatch):
    monkeypatch.setenv('BANODOCO_LOCAL_DATA_ROOT', str(tmp_path / 'data'))
    tl = Checkout(base())
    tl.save(tmp_path / 'cancel.checkout.json', quiet=True)
    before = tl.document()
    files = {str(p): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    plan = commands.run(tl, call(relation_choices=[choice('cancel')], frames=9))
    assert not plan.calls and not plan.changed
    assert files == {str(p): p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    after, plan = apply(before, call('clip.set', x=240), call(frames=9, relation_choices=[choice('cancel')]))
    assert after == before and not plan.calls and not plan.changed


def test_detached_start_stays_fixed_on_later_plain_drag_and_legacy_null_is_unchanged():
    after, _ = apply(base(), call(frames=9, relation_choices=[choice('detach')]))
    assert intent.fixed_start(Checkout(after).clip(SID).data)
    dragged, _ = apply(after, call(frames=9))
    clip = Checkout(dragged).clip(SID)
    assert intent.on(clip.data) is None and clip.start == pytest.approx(1.9)
    tl = Checkout(base())
    intent._app_w(tl.clip(SID).data)['on'] = None
    tl._command_depth = 1
    tl.resolve()
    assert tl.clip(SID).start == 0


@pytest.mark.parametrize('action', relations.CHOICES)
def test_trim_explicit_duration_end_rule(action):
    bundle, sid = media_end()
    tl = Checkout(bundle)
    intent.set_until(tl.clip(sid).data, None)
    intent.set_for(tl.clip(sid).data, 4)
    bundle = tl.document()
    fields = dict(offset_seconds=3) if action == 'adjust-offset' else {}
    if action == 're-anchor':
        fields = dict(anchor='end of c1', offset_seconds=-1)
    after, plan = apply(bundle, call('clip.trim', sid, out_s=4 if action == 'keep' else 3,
        relation_choices=[choice(action, target=sid, edge='end', **fields)]))
    if action == 'cancel':
        assert after == bundle and not plan.calls
    else:
        clip = Checkout(after).clip(sid)
        assert clip.duration == (4 if action == 'keep' else 3)
        assert apply(bundle, *plan.calls)[0] == after


def test_rebase_rewrites_exact_clip_edge_in_choice_anchor():
    bundle = base()
    _, plan = apply(bundle, call(frames=0, relation_choices=[choice('re-anchor',
        anchor=f'clip-end "{NEIGHBOUR}"', offset_frames=9)]))
    head = Checkout(copy.deepcopy(bundle))
    head.clip(NEIGHBOUR).data['id'] = 'renamed-voice'
    renamed = 'occurrence:occ-A/clip:renamed-voice'
    result = rebase(plan.calls, head.document(), id_map={NEIGHBOUR: renamed})
    assert not result.conflicts
    text = intent.on(Checkout(result.document).clip(SID).data)
    assert text == f'clip-end "{renamed}" +9f'
