"""Astra110 owner preservation through the existing runner and inverse."""
import copy
import json
from pathlib import Path

import pytest
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline import commands
from astrid.sdk.timeline._common import TimelineEditError
from astrid.sdk.timeline.inverse import inverse_command


def checkout():
    bundle = json.loads((Path(__file__).parents[1] / 'fixtures/timeline_editing/tiny_publishable.json').read_text())
    bundle['parent']['config']['tracks'] = copy.deepcopy(bundle['shots']['A']['internal_timeline']['tracks'])
    return Checkout(bundle)


def call(sid='parent/clip:caption', at=1):
    return dict(op='timeline.add', select=None, args=dict(element='am-type', at=at, hold=.5,
        clip_id='caption', params=dict(text='Café captions'), track='type'),
        created=[sid], expect={sid+'::':dict(state='absent')})


def apply(tl, value):
    from astrid.sdk.timeline.transaction import edit_transaction
    with edit_transaction(tl, 'caption', quiet=True, persist=False) as tx:
        commands.execute(tl, value)
    return tx.plan


@pytest.mark.parametrize('sid,shot,start', [('parent/clip:caption', None, 1),
    ('occurrence:occ-B/clip:caption', 'B', 4.5)])
def test_explicit_owner_text_timing_and_inverse_preserve_unrelated_parent(sid,shot,start):
    tl=checkout()
    before=copy.deepcopy(tl.document())
    plan=apply(tl,call(sid,start))
    clip=commands.authored_owner(tl,sid,selected=True)
    assert clip.shot_id == shot
    assert clip.text == 'Café captions'
    assert clip.start == start
    assert clip.duration == .5
    assert {(w['id'],w['path']) for w in plan.direct_writes} == {(sid,'')}
    assert not any(w['id']=='parent' for w in plan.direct_writes)
    after=copy.deepcopy(tl.document())
    inverse=inverse_command(plan.calls,before,after,'caption')
    tl.bundle['parent']['opaque']={'keep':[None,7]}
    unrelated=dict(id='unrelated',clipType='am-type',track='type',at=0,hold=.5,params={})
    tl.bundle['parent']['clips'].append(unrelated)
    undo=apply(tl,inverse)
    assert tl.bundle['parent']['opaque']=={'keep':[None,7]}
    assert unrelated in tl.bundle['parent']['clips']
    assert sid not in commands.entity_states(tl)
    undone=copy.deepcopy(tl.document())
    redo=inverse_command(undo.calls,after,undone,'undo-caption')
    apply(tl,redo)
    assert commands.authored_owner(tl,sid,selected=True).id=='caption'
    assert unrelated in tl.bundle['parent']['clips']


def test_chapter_empty_tracks_are_references():
    tl=checkout()
    tl.bundle['shots']['B']['internal_timeline']['tracks']=[]
    apply(tl,call('occurrence:occ-B/clip:caption',4.5))
    assert tl.bundle['shots']['B']['internal_timeline']['tracks']==[]


def test_legacy_sdk_records_owner_and_replays_after_placement_moves():
    tl=checkout()
    before=copy.deepcopy(tl.document())
    plan=apply(tl,dict(op='timeline.add',select=None,args=dict(element='am-type',at=4.5,hold=.5,clip_id='caption')))
    recorded=plan.calls[0]
    assert commands.EditCommand.coerce(recorded).resolved==('occurrence:occ-B/clip:caption',)
    other=Checkout(before)
    other.bundle['placements'][1]['placement']['start_ms']=5000
    apply(other,recorded)
    assert commands.authored_owner(other,'occurrence:occ-B/clip:caption',selected=True).shot_id=='B'


@pytest.mark.parametrize('case', ['clip-id','resolved','expect-id','expect-present','duplicate','missing-owner','shared-owner','missing-track','conflicting-track','stale'])
def test_strict_refusal_is_atomic(case):
    tl=checkout(); value=call()
    if case=='clip-id': value['args']['clip_id']='contradiction'
    if case=='resolved': value['resolved']=['occurrence:occ-A/clip:caption']
    if case=='expect-id': value['expect']={'parent/clip:other::':dict(state='absent')}
    if case=='expect-present': value['expect']={'parent/clip:caption::':dict(state='present',value={})}
    if case=='duplicate':
        apply(tl,value)
    if case=='missing-owner': value=call('occurrence:missing/clip:caption')
    if case=='shared-owner':
        value=call('occurrence:occ-B/clip:caption',4.5)
        tl.bundle['placements'].append(dict(copy.deepcopy(tl.bundle['placements'][1]),occurrence_id='shared'))
    if case=='missing-track': value['args']['track']='absent'
    if case=='conflicting-track': tl.bundle['shots']['A']['internal_timeline']['tracks'][0]['kind']='audio'
    if case=='stale': value['expect']['parent::opaque']=dict(state='present',value=9)
    before=copy.deepcopy(tl.document())
    with pytest.raises((ValueError,TimelineEditError)):
        apply(tl,value)
    assert tl.document()==before


@pytest.mark.parametrize('change',['delete','replace'])
def test_recorded_owner_conflicts_without_mutation(change):
    tl=checkout(); before=copy.deepcopy(tl.document())
    plan=apply(tl,call('occurrence:occ-B/clip:caption',4.5))
    other=Checkout(before)
    if change=='delete': other.bundle['placements'].pop()
    else: other.bundle['placements'][1]['shot_id']='A'
    original=copy.deepcopy(other.document())
    with pytest.raises((ValueError,TimelineEditError)):
        apply(other,plan.calls[0])
    assert other.document()==original


def test_parent_only_word_caption_uses_original_null_binding_and_exact_anchors():
    from test_timeline_transcript_parent_binding_f102 import checkout_original
    from astrid.core.timeline import moments as mo
    from astrid.sdk import timeline_intent as intent
    tl,binding,reference=checkout_original()
    tl.bundle['placements']=[]
    tl.bundle['shots']={}
    tl.bundle['parent']['config']['tracks']=[dict(id='type',kind='visual')]
    word=tl.words()[0]
    value=call(at=mo.format_moment(mo.word_moment(word,(word,))))
    before=copy.deepcopy(tl.document())
    plan=apply(tl,value)
    caption=commands.authored_owner(tl,'parent/clip:caption')
    apply(tl,dict(op='clip.until',select='parent/clip:caption',args=dict(moment=mo.format_moment(mo.Moment('word', source=word.source, word_id=word.id, edge='end')))))
    assert caption.shot_id is None
    assert caption.start==0
    assert caption.duration==.5
    assert tl.bundle['parent']['clips'][0]['app']['transcript']['binding']==binding
    assert binding['occurrence_id'] is None
    assert mo.parse(intent.on(caption.data)).source==word.source
    assert reference['snapshot']['sha256'] in intent.on(caption.data)
    recorded=commands.EditCommand.coerce(plan.calls[0])
    assert set(recorded.bindings.values())=={'parent/clip:'+word.clip_id}
    apply(tl,dict(op='clip.set',select='parent/clip:caption',args=dict(text='Edited caption',size=64)))
    assert caption.text=='Edited caption'
    assert caption.get('size')==64


def test_parent_creation_rebase_keeps_unrelated_parent_changes():
    tl=checkout(); base=copy.deepcopy(tl.document())
    plan=apply(tl,call())
    current=Checkout(base)
    current.bundle['parent']['opaque']={'independent':True}
    other=dict(id='other',clipType='am-type',track='type',at=2,hold=.5,params={})
    current.bundle['parent']['clips'].append(other)
    apply(current,plan.calls[0])
    assert other in current.bundle['parent']['clips']
    assert current.bundle['parent']['opaque']=={'independent':True}
