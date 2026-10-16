"""Real provider -> request-bound port -> durable Runtime group publication."""
import copy
import hashlib
import json
import os
from pathlib import Path

import pytest
from test_timeline_graph_runtime import runtime, body, commit  # noqa: F401
from test_timeline_graph_commands import closure  # noqa: F401
from test_timeline_shot_groups import call, remove, GROUP, MEMBERS
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


def snapshot(service):
    return '\n'.join(service.store.conn.iterdump())


@pytest.fixture
def scene(runtime):
    s, p = runtime
    hashes = {key: hashlib.sha256(key.encode()).hexdigest() for key in ('img', 'vid', 'new')}
    for key in hashes:
        s.cas.put(key.encode())
    with s.store._transaction():
        for digest, kind in [(hashes['img'], 'image/png'), (hashes['vid'], 'video/mp4'), (hashes['new'], 'video/mp4')]:
            s.store.conn.execute('INSERT INTO objects VALUES (?,3,?,?,?)', (digest, kind, 'fixture', 'fixture'))
            s.store.conn.execute("INSERT INTO project_objects VALUES (?,?,'managed',?)", (p, digest, 'fixture'))
        for gen, var, digest in [('g1', 'v1', hashes['vid']), ('g2', 'v2', hashes['new'])]:
            s.store.conn.execute("INSERT INTO generations VALUES (?,?,NULL,'video','completed',?,1,?,?)", (gen, p, json.dumps({'params': {'duration_seconds': 2}}), 'fixture', 'fixture'))
            s.store.conn.execute("INSERT INTO generation_variants(id,generation_id,object_id,variant_type,metadata_json,created_at) VALUES (?,?,?,'original','{}','fixture')", (var, gen, digest))
    parent = copy.deepcopy(s._commit_revision_closure(p, 't', 'rev-0')['parent_revision']['payload'])
    parent.update(tracks=[dict(id='picture', kind='visual')], clips=[dict(id='i1', clipType='media', track='picture', at=0, hold=.5, asset='image', params={}, keyframes=[{'at':0,'x':3}], anchors={'a':None}, opaque=[None,7]), dict(id='i2', clipType='media', track='picture', at=.5, hold=.5, asset='image', params={}), dict(id='other', clipType='media', track='picture', at=1, hold=1, params={})], registry=dict(assets=dict(image=dict(media_id='sha256:'+hashes['img'], type='image/png'))))
    s.publish_parent_composition(p, 't', dict(project_id=p, timeline_id='t', expected_head='rev-0', parent_revision_id='group-base', parent_composition=parent, shot_revisions=[], internal_timeline_revisions=[]), idempotency_key='group-fixture')
    return s, p


def load(s, p, revision):
    request = body(s,p,'read',[],base=revision)
    return RuntimeCommitService._load_revision(s._request_commit_port(request,dict(actor='fixture',scopes=['projects:write'])),request,revision)


def selection(s,p,gen='g1',var='v1',asset='video'):
    return s.get_project_media_selection(p, asset=asset,generation_id=gen,variant_id=var)


def test_durable_all_intents_inverse_replay_and_executable_vectors(scene, monkeypatch):
    s,p=scene
    vectors=[]
    def execute(key, command):
        request=body(s,p,key,[command]); result=commit(s,p,request)
        assert result['status']=='accepted',result
        assert commit(s,p,request)==result
        vectors.append(dict(name=key,request=request,result=result))
        return result
    pin=execute('pin',call(name='Retain'))
    before=load(s,p,pin['accepted_revision_id'])
    selected=selection(s,p)
    request=body(s,p,'video',[call('video',media=selected,identities={'clip_id':'video-output'})])
    delivered=[]
    def lose(result):
        delivered.append(result);raise TimeoutError('accepted response lost')
    monkeypatch.setattr(s,'_after_timeline_commit',lose,raising=False)
    with pytest.raises(TimeoutError):commit(s,p,request)
    monkeypatch.delattr(s,'_after_timeline_commit')
    video=commit(s,p,request)
    assert video==delivered[0]
    vectors.append(dict(name='video-response-loss',request=request,result=video))
    assert video['shot_groups']==[dict(operation_index=0,group=GROUP,created=['parent/clip:video-output'],reused=[],restored=[])]
    after=load(s,p,video['accepted_revision_id'])
    inverse=inverse_command(video['change']['commands'],before,after,video['accepted_publication_id'])
    inverse_result=execute('inverse-video',inverse)
    exact=load(s,p,inverse_result['accepted_revision_id'])
    assert exact['parent']==before['parent']
    execute('video-again',call('video',media=selected,identities={'clip_id':'video-output-2'}))
    replacement=execute('replace-video',call('replace-video',media=selection(s,p,'g2','v2','replacement')))
    assert replacement['shot_groups'][0]['reused']==['parent/clip:video-output-2']
    restored=execute('images',call('images'))
    assert restored['shot_groups'][0]['restored']==MEMBERS
    assert load(s,p,restored['accepted_revision_id'])['parent']['clips']==before['parent']['clips']
    execute('unpin',remove())
    execute('repin',call())
    execute('delete',remove(MEMBERS[0]))
    assert [c['id'] for c in load(s,p,s.head(p,'t')['revision_id'])['parent']['clips']]==['i2','other']
    target=os.environ.get('ASTRID_SHOT_GROUP_VECTORS')
    if target:
        Path(target).write_text(json.dumps(dict(schema_version=1,vectors=vectors),indent=2,sort_keys=True)+'\n')


def test_acceptance_selected_metadata_stale_wrong_project_and_nested_refs_atomic(scene,monkeypatch):
    s,p=scene
    pinned=commit(s,p,body(s,p,'pin',[call()]))
    assert pinned['status']=='accepted',pinned
    selected=selection(s,p)
    original=s._selected_project_media
    reads=[]
    def changed(project,media):
        result=original(project,media);reads.append(result)
        if len(reads)==1:
            with s.store._transaction():
                s.store.conn.execute("UPDATE generation_variants SET metadata_json=? WHERE id='v1'",(json.dumps({'opaque':'changed'}),))
        return result
    monkeypatch.setattr(s,'_selected_project_media',changed)
    from runtime_protocol.errors import ConflictError, ValidationError, NotFoundError
    request=body(s,p,'stale',[call('video',media=selected,identities={'clip_id':'reserved'})])
    before_head=s.head(p,'t');before_revisions=s.revisions(p,'t',{})
    with pytest.raises(ConflictError):commit(s,p,request)
    assert s.head(p,'t')==before_head and s.revisions(p,'t',{})==before_revisions
    monkeypatch.setattr(s,'_selected_project_media',original)
    # Actual publication checks named nested references even when they do not
    # contain generic asset/media fields. Failed publication changes no row.
    base=s._commit_revision_closure(p,'t',before_head['revision_id'])['parent_revision']['payload']
    for field in ('videoAssetKey','assetKey'):
        parent=copy.deepcopy(base);row=parent['config']['pinnedShotGroups'][0]
        if field=='videoAssetKey':row[field]='missing'
        else:row['imageClipSnapshot']=[dict(assetKey='missing')]
        previous=snapshot(s)
        with pytest.raises(ValidationError):
            s.publish_parent_composition(p,'t',dict(project_id=p,timeline_id='t',expected_head=before_head['revision_id'],parent_composition=parent,shot_revisions=[],internal_timeline_revisions=[]),idempotency_key='bad-'+field)
        assert snapshot(s)==previous


def test_unrelated_head_rebase_conflict_and_fixed_generation(scene,monkeypatch):
    s,p=scene
    result=commit(s,p,body(s,p,'pin',[call()]))
    assert result['status']=='accepted',result
    selected=selection(s,p)
    pending=body(s,p,'pending',[call('video',media=selected,identities={'clip_id':'reserved'})])
    other=dict(op='clip.set',select='parent/clip:other',args=dict(opacity=.5))
    advanced=commit(s,p,body(s,p,'other',[other]));assert advanced['status']=='accepted',advanced
    accepted=commit(s,p,pending);assert accepted['status']=='accepted',accepted
    assert accepted['rebased_onto']==advanced['accepted_revision_id']
    assert accepted['canonical_document']['parent']['registry']['assets']['video']['generationId']=='g1'
    conflict=commit(s,p,dict(pending,request_id='conflict'))
    assert conflict['status']=='conflict',conflict
    assert s.head(p,'t')['revision_id']==accepted['accepted_revision_id']
