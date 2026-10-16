"""Synthetic frozen-input evidence through the existing Checkout/compiler path.

These inputs model accepted history; no publisher authentication is claimed.
"""
import copy
import json
from pathlib import Path

import pytest
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401
from test_timeline_transcript_binding_f101 import pinned, source

from astrid.core.timeline import moments as mo
from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.compiler import TimingInputs, compile_timing
from astrid.sdk.timeline.transcript_binding import FrozenTranscript, follow_bound_anchors


def setup(content=None):
    binding, reference, raw = pinned(content)
    binding['word_ids'] = ['opaque-alpha', 'opaque-beta']
    bundle = json.loads((Path(__file__).parents[1]/'fixtures/timeline_editing/tiny_publishable.json').read_text())
    for shot, oid, cid in [('A', 'occ-A', 'a-vo'), ('B', 'occ-B', 'b-vo')]:
        clip = next(c for c in bundle['shots'][shot]['internal_timeline']['clips'] if c['id'] == cid)
        clip.update(at=.5, speed=2, **{'from': .5, 'to': 1.25})
        clip.setdefault('app', {})['transcript'] = dict(v=1, binding=dict(copy.deepcopy(binding), occurrence_id=oid))
        # This deliberately conflicting compiler cache is not source identity.
        intent.set_line(clip, 'cached', [[0, .01, 'WRONG', 'forged-id']])
    return Checkout(bundle, transcript_dependencies=[FrozenTranscript(reference, raw)])


def vo(tl, shot='A'):
    return next(c for c in tl.clips() if c.id == ('a-vo' if shot == 'A' else 'b-vo'))


def picture(tl):
    return next(c for c in tl.clips() if c.id == 'a-rocket')


def word(tl, shot='A'):
    return next(w for w in tl.words() if w.shot_id == shot)


def formula(w, **kwargs):
    return dict(word=w.id, source=list(w.source), text='stale display spelling', **kwargs)


def rebind(tl, content, mapping=(), *, selected=None):
    old = copy.deepcopy(vo(tl).data['app']['transcript']['binding'])
    binding, reference, raw = pinned(content)
    binding['document']['version'] = reference['document']['version'] = old['document']['version'] + 1
    if content['source']['source_id'] != old['source']['source_id']:
        binding['document']['id'] = reference['document']['id'] = 'synthetic-new-take-document'
    binding['word_ids'] = selected if selected is not None else [r['id'] for r in content['words']]
    tl._transcript_dependencies += (FrozenTranscript(reference, raw),)
    vo(tl).data['app']['transcript']['binding'] = binding
    follow_bound_anchors(tl, clip_id='a-vo', occurrence_id='occ-A', previous_binding=old,
                         next_binding=binding, correspondence=mapping)


def correspondence(a='opaque-beta', b='opaque-beta', old='synthetic-lineage-A', new='synthetic-lineage-A'):
    return {'from': dict(lineage_id=old, word_id=a),
                                           'to': dict(lineage_id=new, word_id=b)}


def correction():
    content = source()
    content['source'].update(revision_id='revision-corrected', parent_revision_id='synthetic-revision-A')
    content['words'][1].update(text='corrected', start_s=.75, end_s=1.25)
    content['segments'] = [dict(id='new-1', word_ids=['opaque-alpha']), dict(id='new-2', word_ids=['opaque-beta'])]
    return content


def test_source_rows_project_once_and_repeat_without_identity_collapse():
    tl = setup()
    before = copy.deepcopy(tl.bundle)
    tl.resolve()
    words = list(tl.words())
    assert [(w.id, w.text, w.start, w.end) for w in words] == [
        ('opaque-beta', 'again', .5625, .8125), ('opaque-beta', 'again', 4.5625, 4.8125)]
    assert words[0].source != words[1].source
    assert tl.word('opaque-beta', source=words[1].source) == words[1]
    with pytest.raises(TimelineEditError, match='ambiguous'):
        tl.word('opaque-beta')
    assert intent.words(vo(tl).data) == intent.words(next(c for c in before['shots']['A']['internal_timeline']['clips'] if c['id']=='a-vo'))
    p = picture(tl)
    intent.set_formula(p.data, 'params.x', formula(words[0], **{'as': 'timeline_seconds'}))
    intent.set_formula(p.data, 'params.y', formula(words[1], **{'as': 'timeline_seconds'}))
    intent.set_formula(p.data, 'params.frame', formula(words[0], **{'as': 'clip_frame'}))
    tl.resolve()
    assert p.data['params']['x'] == .5625
    assert p.data['params']['y'] == 4.5625
    assert p.data['params']['frame'] == round((.5625-p.start)*tl.fps)


def test_word_moment_and_runner_binding_preserve_opaque_identity_and_occurrence():
    tl = setup()
    w = word(tl, 'B')
    text = mo.format_moment(mo.word_moment(w, tl.words()))
    parsed = mo.parse(text)
    assert parsed.source == w.source and parsed.word_id == w.id
    assert tl.time(text) == pytest.approx(136/30, abs=1e-6)
    bindings = {}
    commands.capture_binding(tl, text, picture(tl), bindings)
    assert bindings == {text: 'occurrence:occ-B/clip:b-vo'}
    picture(tl).on(w)
    assert intent.on(picture(tl).data) == text
    assert picture(tl).start == pytest.approx(136/30, abs=1e-6)


def test_exact_word_grammar_roundtrips_opaque_strings_and_nested_beat():
    m = mo.Moment('word', source=('doc " é', 'line age', 'rev\\ision', 'occurrence:one/clip:vo', 'a'*64), word_id='id "\\ é')
    assert mo.parse(mo.format_moment(m)) == m
    end = mo.parse('after ' + mo.format_moment(m) + ' +2f')
    assert end.source == m.source and end.edge == 'end' and end.offset_frames == 2
    beat = mo.parse('beat 2 after ' + mo.format_moment(m))
    assert beat.base.source == m.source


@pytest.mark.parametrize('failure', ['missing', 'bytes', 'digest', 'identity', 'selection', 'occurrence'])
def test_dependency_refusal_precedes_timing_and_never_mutates_input(failure):
    tl = setup()
    deps = list(tl._transcript_dependencies)
    d = deps[0]
    if failure == 'missing':
        deps = []
    elif failure == 'bytes':
        deps = [FrozenTranscript(d.reference, d.snapshot_bytes+b' ')]
    elif failure in ('digest', 'identity'):
        reference = copy.deepcopy(d.reference)
        reference['snapshot' if failure == 'digest' else 'subject']['sha256' if failure == 'digest' else 'media_object_id'] = 'wrong'
        deps = [FrozenTranscript(reference, d.snapshot_bytes)]
    elif failure == 'selection':
        vo(tl).data['app']['transcript']['binding']['word_ids'] = ['opaque-beta', 'opaque-alpha']
    else:
        vo(tl).data['app']['transcript']['binding']['occurrence_id'] = 'wrong'
    before = copy.deepcopy(tl.bundle)
    with pytest.raises(TimelineEditError):
        compile_timing(TimingInputs(tl.bundle, {'_transcript_dependencies': deps}))
    assert tl.bundle == before


def test_correction_and_resegmentation_follow_only_explicit_retained_identity():
    tl = setup()
    p = picture(tl)
    p.on(word(tl))
    intent.set_formula(p.data, 'params.x', formula(word(tl), **{'as':'timeline_seconds'}))
    rebind(tl, correction(), [correspondence()])
    tl.resolve()
    assert p.start == pytest.approx(18/30, abs=1e-6)
    assert p.data['params']['x'] == .625
    assert mo.parse(intent.on(p.data)).word_id == 'opaque-beta'
    assert mo.parse(intent.on(p.data)).source[2] == 'revision-corrected'
    assert next(w for w in tl.words() if w.shot_id=='B').source[2] == 'synthetic-revision-A'


@pytest.mark.parametrize('kind', ['missing-map', 'removed', 'new-take', 'reused-id'])
def test_unmatched_bound_anchors_keep_last_position_length_and_formula(kind):
    tl = setup()
    p = picture(tl)
    p.on(word(tl))
    intent.set_formula(p.data, 'params.x', formula(word(tl), **{'as': 'timeline_seconds'}))
    tl.resolve()
    prior = p.start, p.duration, p.data['params']['x']
    content = correction()
    if kind == 'removed':
        content['words'] = content['words'][:1]
        content['segments'] = [dict(id='remaining', word_ids=['opaque-alpha'])]
    if kind == 'new-take':
        content['source'].update(source_id='new-take', lineage_id='new-lineage')
    if kind == 'reused-id':
        # Skip continuity hook as a defensive replay case: revision-qualified
        # identity still cannot bind to the same spelling/ID in different bytes.
        old = copy.deepcopy(vo(tl).data['app']['transcript']['binding'])
        binding, reference, raw = pinned(content)
        binding['document']['version'] = reference['document']['version'] = old['document']['version']+1
        vo(tl).data['app']['transcript']['binding'] = binding
        tl._transcript_dependencies += (FrozenTranscript(reference,raw),)
    else:
        rebind(tl, content)
    tl.resolve()
    assert (p.start, p.duration, p.data['params']['x']) == prior
    assert 'ORPHAN' in intent.orphan(p.data)
    assert 'ORPHAN' in intent.formulas(p.data)['params.x']['orphan']
    assert intent.on(p.data)  # retained for explicit rehome


def test_new_take_one_to_one_provenance_mapping_preserves_new_ids():
    tl = setup()
    p = picture(tl)
    p.on(word(tl))
    content = correction()
    content['source'].update(source_id='new-take', lineage_id='new-lineage')
    content['words'][1]['id'] = 'new-opaque'
    content['segments'][1]['word_ids'] = ['new-opaque']
    rebind(tl, content, [correspondence(b='new-opaque', new='new-lineage')])
    tl.resolve()
    m = mo.parse(intent.on(p.data))
    assert m.word_id == 'new-opaque' and m.source[1] == 'new-lineage'
    assert p.start == pytest.approx(18/30, abs=1e-6)


@pytest.mark.parametrize('kind', ['duplicate-from','duplicate-to','missing-endpoint','wrong-lineage','no-parent','changed-retained-id'])
def test_invalid_correspondence_refuses_before_anchor_writes(kind):
    tl = setup()
    p = picture(tl)
    p.on(word(tl))
    before = copy.deepcopy(p.data)
    content = correction()
    mapping = [correspondence()]
    if kind == 'duplicate-from':
        mapping += [correspondence(b='opaque-alpha')]
    elif kind == 'duplicate-to':
        mapping += [correspondence(a='opaque-alpha')]
    elif kind == 'missing-endpoint':
        mapping = [correspondence(b='missing')]
    elif kind == 'wrong-lineage':
        mapping = [correspondence(old='forged')]
    elif kind == 'no-parent':
        del content['source']['parent_revision_id']
    else:
        mapping = [correspondence(b='opaque-alpha')]
    with pytest.raises(TimelineEditError):
        rebind(tl, content, mapping)
    assert p.data == before


def test_ambiguous_repeated_text_never_authorizes_continuity():
    tl = setup()
    with pytest.raises(TimelineEditError, match='matches 2'):
        tl.time('"again"')
    p = picture(tl)
    p.on(word(tl))
    content = correction()
    content['words'][1].update(id='replacement', text='again')
    content['segments'][1]['word_ids'] = ['replacement']
    rebind(tl, content)
    tl.resolve()
    assert intent.orphan(p.data)
    assert mo.parse(intent.on(p.data)).word_id == 'opaque-beta'


def test_untimed_cache_cannot_supply_bound_source_identity():
    tl = setup()
    tl._transcript_dependencies = ()
    with pytest.raises(TimelineEditError, match='frozen dependency'):
        tl.words()


def test_offline_snapshot_undo_redo_preserves_explicit_dependencies(tmp_path):
    tl = setup()
    path = tmp_path/'synthetic.checkout.json'
    tl.save(path, quiet=True)
    picture(tl).on(word(tl))
    tl.save(quiet=True)
    accepted = copy.deepcopy(tl._transcript_dependencies)
    tl.undo()
    tl.resolve()
    assert tl._transcript_dependencies == accepted
    tl.redo()
    tl.resolve()
    assert tl._transcript_dependencies == accepted
    assert picture(tl).start == pytest.approx(16/30, abs=1e-6)
    # Reload has no implicit latest/sidecar dependency discovery.
    detached = Checkout.load(path)
    with pytest.raises(TimelineEditError, match='frozen dependency'):
        detached.resolve()
    detached._transcript_dependencies = accepted
    detached.resolve()
    detached._transcript_dependencies = (FrozenTranscript(accepted[0].reference,b'corrupt'),)
    with pytest.raises(TimelineEditError, match='digest'):
        detached.resolve()


@pytest.mark.parametrize('redo', [False, True])
@pytest.mark.parametrize('failure', ['missing', 'corrupt'])
def test_undo_redo_refuses_missing_or_altered_dependency_before_disk_write(tmp_path, redo, failure):
    tl = setup()
    path = tmp_path/'synthetic.checkout.json'
    tl.save(path, quiet=True)
    picture(tl).on(word(tl))
    tl.save(quiet=True)
    if redo:
        tl.undo()
    prior = path.read_bytes()
    d = tl._transcript_dependencies[0]
    tl._transcript_dependencies = () if failure == 'missing' else (FrozenTranscript(d.reference,b'corrupt'),)
    with pytest.raises(TimelineEditError):
        (tl.redo if redo else tl.undo)()
    assert path.read_bytes() == prior
    assert not path.with_name('.'+path.name+'.replay.json').exists()


@pytest.mark.usefixtures("synthetic_scene_answers")
def test_exact_source_identity_survives_recorded_rebase_and_detached_apply():
    from astrid.sdk.timeline.commit import RuntimeCommitService
    from astrid.sdk.timeline.rebase import rebase
    tl = setup()
    base = copy.deepcopy(tl.bundle)
    picture(tl).on(word(tl))
    calls = [call.to_json() for call in tl._pending_calls]
    replayed = rebase(calls, base, transcript_dependencies=tl._transcript_dependencies)
    assert not replayed.conflicts, replayed
    out = Checkout(replayed.document, transcript_dependencies=tl._transcript_dependencies)
    assert mo.parse(intent.on(picture(out).data)).source == word(tl).source
    assert picture(out).start == picture(tl).start
    result, _, _ = RuntimeCommitService._apply(base, calls, transcript_dependencies=tl._transcript_dependencies)
    assert picture(Checkout(result)).start == picture(tl).start
    refused = rebase(calls, base)
    assert refused.conflicts


def test_explicit_text_word_moment_is_pinned_before_correction():
    tl = setup()
    p = picture(tl)
    p.on('"again" #1')
    assert mo.parse(intent.on(p.data)).source == word(tl).source
    rebind(tl, correction())
    tl.resolve()
    assert intent.orphan(p.data)


def test_missing_until_freezes_both_edges_even_when_on_would_move():
    tl = setup()
    p = picture(tl)
    p.on(word(tl))
    p.until(mo.word_moment(word(tl, 'B'), tl.words()))
    prior = p.start, p.duration
    # Old on remains available and moves; until's exact occurrence loses its word.
    vo(tl).data['at'] = 1.5
    vo(tl,'B').data['app']['transcript']['binding']['word_ids'] = []
    tl.resolve()
    assert (p.start,p.duration) == prior
    assert intent.orphan(p.data)


def test_correction_dependencies_survive_snapshot_undo_and_redo(tmp_path):
    tl = setup()
    path = tmp_path/'synthetic.checkout.json'
    p = picture(tl)
    p.on(word(tl))
    tl.save(path, quiet=True)
    rebind(tl, correction(), [correspondence()])
    tl.resolve()
    tl.save(quiet=True)
    deps = tl._transcript_dependencies
    tl.undo()
    tl.resolve()
    assert mo.parse(intent.on(picture(tl).data)).source[2] == 'synthetic-revision-A'
    tl.redo()
    tl.resolve()
    assert mo.parse(intent.on(picture(tl).data)).source[2] == 'revision-corrected'
    assert tl._transcript_dependencies == deps


def test_same_revision_with_different_snapshot_cannot_reuse_anchor_identity():
    tl = setup()
    p = picture(tl)
    p.on(word(tl))
    old_source = word(tl).source
    content = source()
    content['words'][1]['start_s'] = 1
    b, ref, raw = pinned(content)
    b['document']['version'] = ref['document']['version'] = 4
    vo(tl).data['app']['transcript']['binding'] = b
    tl._transcript_dependencies += (FrozenTranscript(ref,raw),)
    tl.resolve()
    assert intent.orphan(p.data)
    assert old_source[4] != word(tl).source[4]


def test_qualified_word_lookup_preserves_opaque_whitespace_and_source_order():
    content = source()
    content['words'][0].update(id=' opaque one ', start_s=.8, end_s=.9)
    content['words'][1].update(start_s=.6)
    content['segments'][0]['word_ids'] = [' opaque one ', 'opaque-beta']
    b, ref, raw = pinned(content)
    b['word_ids'] = [' opaque one ', 'opaque-beta']
    tl = setup()
    for clip in [vo(tl), vo(tl,'B')]:
        oid = clip.data['app']['transcript']['binding']['occurrence_id']
        clip.data['app']['transcript']['binding'] = dict(copy.deepcopy(b),occurrence_id=oid)
    tl._transcript_dependencies = (FrozenTranscript(ref,raw),)
    words = [w for w in tl.words() if w.shot_id == 'A']
    assert [w.id for w in words] == [' opaque one ', 'opaque-beta']
    assert tl.word(' opaque one ',source=words[0].source) == words[0]


def test_explicit_clear_orphans_bound_anchor_without_erasing_it():
    tl = setup()
    p = picture(tl)
    p.on(word(tl))
    prior = p.start,p.duration,intent.on(p.data)
    old = copy.deepcopy(vo(tl).data['app']['transcript'].pop('binding'))
    follow_bound_anchors(tl, clip_id='a-vo', occurrence_id='occ-A', previous_binding=old,next_binding=None)
    tl.resolve()
    assert (p.start,p.duration,intent.on(p.data)) == prior
    assert intent.orphan(p.data)


def test_duplicate_frozen_dependencies_refuse_instead_of_picking_one():
    tl = setup()
    tl._transcript_dependencies *= 2
    with pytest.raises(TimelineEditError, match='one exact frozen dependency'):
        tl.resolve()


def test_malformed_legacy_formula_retains_existing_cache_diagnostics():
    tl = setup()
    p = picture(tl)
    before = p.data['params']['x']
    intent.set_formula(p.data,'params.x',{'moment':'"again" nonsense-offset'})
    tl.resolve()
    assert p.data['params']['x'] == before
    assert not intent.formulas(p.data)['params.x'].get('orphan')
    assert any('kept its last value' in note for note in tl.notes)
