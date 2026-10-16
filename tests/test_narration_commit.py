"""Disposable managed settlement + real atomic narration acceptance, no provider calls."""
import copy
import hashlib
import json

import pytest

from runtime_protocol.errors import AuthorizationError, ConflictError, NotFoundError, ValidationError
from runtime_protocol.narration import narration_projection
from runtime_protocol.timeline_commit import digest
from test_generic_output_publication import _filmstrip_attempt, _descriptor, _settle_body
from test_timeline_accept import IDENTITY, fixture, wire, acceptance, valid
from test_selected_media_commit import snapshot, mutate


def managed_take(s, p, *, text='Hello world!', bad=None, manifest_ref=False):
    task, attempt = _filmstrip_attempt(s, p)
    audio = b'synthetic speech, no acoustic claim'
    audio_sha = hashlib.sha256(audio).hexdigest()
    manifest = dict(schema_version=1, text=text, text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                    settings={'voice':'fixture-voice','rate':'+0%'}, audio_sha256=audio_sha, duration_seconds=1.25)
    words = dict(schema_version=1, source='fixture', boundary='WordBoundary', audio_sha256=audio_sha,
                 duration_seconds=1.25, words=[{'word':'Hello','start_s':0.0,'end_s':0.4},
                                              {'word':'world!','start_s':0.5,'end_s':1.2}])
    if bad:
        bad(manifest, words)
    payloads = {'speech':audio, 'speech_manifest':json.dumps(manifest).encode(), 'speech_words':json.dumps(words).encode()}
    outputs=[]
    for port, data in payloads.items():
        output=_descriptor(data, name=port, filename=port+'.bin', output_port=port,
                           primary=port=='speech', media_type='audio/wav' if port=='speech' else 'application/json')
        output.update(durability='durable', data_base64=__import__('base64').b64encode(data).decode())
        outputs.append(output)
    body=_settle_body(attempt, outputs)
    if manifest_ref:
        extra=s.ingest(p,b'{"settlement":"provenance"}',media_type='application/json',original_name='settlement.json',idempotency_key='extra-manifest')['data']
        body['result']={'manifest_ref':{'object_id':extra['object_id'],'size':len(b'{"settlement":"provenance"}')}}
    s.settle_attempt(attempt['attempt_id'],body,idempotency_key='speech-settle',
                     identity={'actor':'filmstrip-worker','scopes':['objects:write','worker:execute']})
    refs={v['output_port']:{k:v[k] for k in ('association_id','object_id')} for v in s.managed_outputs(attempt['task_id'])}
    return refs, manifest, words


def request_for(p, refs, *, key='narration-1'):
    request=wire(p,key=key)
    request['change']['commands']=[{'op':'timeline.apply-script','args':{'lines':[{'take':copy.deepcopy(refs)}]}}]
    return request


def prepared(s,p,request,refs,manifest,words, *, repeat=False):
    value=acceptance(s,p,request=request)
    pub=value['publication']
    internal=pub['internal_timeline_revisions'][0]
    internal['revision_id']='narrated-internal'
    shot=pub['shot_revisions'][0]
    shot['revision_id']='narrated-shot';shot['internal_timeline_revision_id']=internal['revision_id']
    pub['parent_composition']['occurrences'][0]['shot_revision_id']=shot['revision_id']
    clip={'id':'voice','clipType':'media','asset':'speech-asset','at':0,'from':0,'to':1.25,'track':'audio-1',
          'app':{'astrid':{'segment':'line-1','text':manifest['text'],
                           'words':[{**w,'id':f'w{i}'} for i,w in enumerate(words['words'])],
                           'take':copy.deepcopy(refs)}}}
    internal['payload']['clips'].append(clip)
    internal['payload']['registry']={'assets':{'speech-asset':{'object_id':refs['speech']['object_id'],'type':'audio','duration':1.25}}}
    if repeat:
        second=copy.deepcopy(pub['parent_composition']['occurrences'][0]);second['occurrence_id']='occurrence-2'
        pub['parent_composition']['occurrences'].append(second)
    closure={'parent_revision':{'payload':pub['parent_composition']},'shot_revisions':[shot],
             'internal_timeline_revisions':[internal]}
    value['narration']=narration_projection(closure)
    value['evidence']['commands']=copy.deepcopy(request['change']['commands'])
    return value


def setup(s,p,**options):
    refs,manifest,words=managed_take(s,p,**options)
    request=request_for(p,refs)
    port=s._request_commit_port(request,IDENTITY)
    take=port.narration_take(refs)
    value=prepared(s,p,request,refs,manifest,words)
    return refs,request,port,take,value


def test_scoped_projection_dependency_pins_and_detached_reads(fixture):
    s,p=fixture
    refs,manifest,words=managed_take(s,p,manifest_ref=True)
    request=request_for(p,refs);port=s._request_commit_port(request,IDENTITY)
    take=port.narration_take(refs);take['manifest']['settings']['voice']='detached'
    assert port.narration_take(refs)['manifest']['settings']['voice']=='fixture-voice'
    value=prepared(s,p,request,refs,manifest,words,repeat=True)
    result=port.accept(value)
    valid(result,'AcceptResponse')
    state=result['receipt']['narration_state']
    assert state['projection']==value['narration']
    assert state['digest']==digest(value['narration'])
    assert [v['segment'] for v in state['projection']['lines']]==['line-1','line-1']
    closure=port.revision_closure(result['revision_id'])
    assert narration_projection(closure)==state['projection']
    deps={r[0] for r in s.store.conn.execute("SELECT dependency_id FROM composition_revision_dependencies WHERE parent_revision_id=? AND dependency_kind='media'",(result['revision_id'],))}
    assert set(port.narration_take(refs)['dependency_objects'])==deps
    assert len(deps)==4
    report=s.store.integrity_report()
    assert report['checks']['revisions']['ok'], report['checks']['revisions']['errors']
    assert report['checks']['event_chain']['ok']
    assert s.store.conn.execute('SELECT count(*) FROM shot_text_bindings').fetchone()[0]==0


@pytest.mark.parametrize('mode',['unknown','malformed','wrong-object','cross-project','unsettled','reclaimed','temporary','port','wrong-task','altered-bytes','unowned'])
def test_ref_and_authority_refusal_without_publication(fixture,mode):
    s,p=fixture
    refs,manifest,words=managed_take(s,p)
    request=request_for(p,refs)
    port=s._request_commit_port(request,IDENTITY)
    if mode=='unknown': request['change']['commands']=[];port=s._request_commit_port(request,IDENTITY)
    elif mode=='malformed': refs['speech']['path']='/tmp/no';request=request_for(p,refs)
    elif mode=='wrong-object': refs['speech']['object_id']='sha256:'+'0'*64;port=s._request_commit_port(request_for(p,refs),IDENTITY)
    elif mode=='cross-project':
        other=s.create_project({'slug':'other','name':'Other'},idempotency_key='other')['id']
        p=other;port=s._request_commit_port(request_for(p,refs),IDENTITY)
    elif mode=='unsettled':mutate(s,'UPDATE attempts SET settled=0')
    elif mode=='reclaimed':mutate(s,"UPDATE managed_output_lifecycle SET state='reclaimed'")
    elif mode=='temporary':mutate(s,"UPDATE managed_output_associations SET durability='temporary'")
    elif mode=='port':mutate(s,"UPDATE managed_output_associations SET output_port='other' WHERE output_port='speech_words'")
    elif mode=='wrong-task':mutate(s,"UPDATE tasks SET status='failed'")
    elif mode=='altered-bytes':s.cas.path_for(refs['speech']['object_id'][7:]).write_bytes(b'X'*len(b'synthetic speech, no acoustic claim'))
    elif mode=='unowned':mutate(s,'DELETE FROM project_objects WHERE digest=?',(refs['speech']['object_id'][7:],))
    before=snapshot(s)
    with pytest.raises((AuthorizationError,ConflictError,NotFoundError,ValidationError)):
        port.narration_take(refs)
    assert snapshot(s)==before


@pytest.mark.parametrize('mode',['omit','extra','revision','digest','refs','text','words','asset','duplicate','unread','missing-take','bool-version','unbound'])
def test_candidate_projection_refusals_rollback_actual_publication(fixture,mode):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    clip=value['publication']['internal_timeline_revisions'][0]['payload']['clips'][-1]
    if mode=='omit':value.pop('narration')
    elif mode=='extra':value['narration']['lines'].append(copy.deepcopy(value['narration']['lines'][0]))
    elif mode=='revision':value['narration']['lines'][0]['internal_revision_id']='wrong'
    elif mode=='digest':value['narration']['lines'][0]['line_digest']='sha256:'+'0'*64
    elif mode=='refs':value['narration']['lines'][0]['take']['speech']['association_id']='wrong'
    elif mode=='text':clip['app']['astrid']['text']='changed'
    elif mode=='words':clip['app']['astrid']['words'][0]['end_s']=0.45
    elif mode=='asset':clip['asset']='missing'
    elif mode=='duplicate':value['publication']['internal_timeline_revisions'][0]['payload']['clips'].append(copy.deepcopy(clip))
    elif mode=='unread':port=s._request_commit_port(request,IDENTITY)
    elif mode=='missing-take':
        clip['app']['astrid'].pop('take');value['narration']={'version':1,'lines':[]}
    elif mode=='bool-version':value['narration']['version']=True
    elif mode=='unbound':
        before=snapshot(s)
        with pytest.raises(ValidationError):s.accept(value,identity=IDENTITY)
        assert snapshot(s)==before
        return
    # Recompute projection in text/word cases to exercise artifact validation.
    if mode in ('text','words'):
        value['narration']['lines'][0]['line_digest']=digest(clip)
    before=snapshot(s)
    with pytest.raises((ConflictError,ValidationError,NotFoundError)):
        port.accept(value)
    assert snapshot(s)==before


@pytest.mark.parametrize('change',[
    lambda m,w:m.update(audio_sha256='0'*64),
    lambda m,w:m.update(text_sha256='0'*64),
    lambda m,w:w.update(duration_seconds=2),
    lambda m,w:w['words'][0].update(start_s=-1),
    lambda m,w:w['words'][1].update(start_s=0.1),
    lambda m,w:w['words'][1].update(end_s=2),
    lambda m,w:w['words'][0].update(end_s=float('nan')),
])
def test_invalid_immutable_artifacts(fixture,change):
    s,p=fixture
    refs,m,w=managed_take(s,p,bad=change)
    before=snapshot(s)
    with pytest.raises(ValidationError):s._request_commit_port(request_for(p,refs),IDENTITY).narration_take(refs)
    assert snapshot(s)==before


@pytest.mark.parametrize('identity',[None,{'actor':'reader','scopes':['projects:read']},
    {**IDENTITY,'connector_assertion':{'realm_id':'foreign'}},{**IDENTITY,'_paired_session':True}])
def test_auth_fences(fixture,identity):
    s,p=fixture
    refs,m,w=managed_take(s,p);port=s._request_commit_port(request_for(p,refs),identity)
    before=snapshot(s)
    with pytest.raises(AuthorizationError):port.narration_take(refs)
    assert snapshot(s)==before


@pytest.mark.parametrize('race',['lifecycle','settlement','bytes','head','membership'])
def test_accept_revalidates_after_capture_and_exact_rollback(fixture,monkeypatch,race):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    if race=='lifecycle':mutate(s,"UPDATE managed_output_lifecycle SET state='reclaimed'")
    elif race=='settlement':mutate(s,'UPDATE attempts SET settled=0')
    elif race=='bytes':s.cas.path_for(refs['speech_words']['object_id'][7:]).write_bytes(b'corrupt')
    elif race=='membership':mutate(s,'DELETE FROM project_objects WHERE digest=?',(refs['speech']['object_id'][7:],))
    else:s.accept(acceptance(s,p,key='concurrent'),identity=IDENTITY)
    assert port.narration_take(refs)==take
    original=s._managed_narration_take
    inside=[]
    def checked(*args):inside.append(s.store.conn.in_transaction);return original(*args)
    monkeypatch.setattr(s,'_managed_narration_take',checked)
    before=snapshot(s)
    with pytest.raises((ConflictError,ValidationError,NotFoundError)):port.accept(value)
    assert snapshot(s)==before
    if race not in ('head','bytes','membership'):assert inside and all(inside)


def test_rebase_replay_pinned_base_and_undo(fixture):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    s.accept(acceptance(s,p,key='concurrent'),identity=IDENTITY)
    with pytest.raises(ConflictError,match='StaleHead'):port.accept(value)
    value['expected_head_revision_id']=s.head(p,'main')['revision_id']
    accepted=port.accept(value)
    # A later request reads only its pinned base's immutable take (no take in body).
    later=wire(p,key='later');later['base_revision_id']=accepted['revision_id']
    later_port=s._request_commit_port(later,IDENTITY)
    assert later_port.narration_take(refs)==take
    # Undo via the same publication mechanism pins the exact older children;
    # semantic undo command generation is D's responsibility.
    restore=acceptance(s,p,key='restore')
    restore['narration']={'version':1,'lines':[]}
    s.accept(restore,identity=IDENTITY)
    undo_request=request_for(p,refs,key='undo-restore')
    undo_request['base_revision_id']=s.head(p,'main')['revision_id']
    undo_port=s._request_commit_port(undo_request,IDENTITY)
    assert undo_port.narration_take(refs)==take
    undo=acceptance(s,p,request=undo_request)
    undo['publication']=copy.deepcopy(value['publication'])
    undo['narration']=copy.deepcopy(value['narration'])
    undone=undo_port.accept(undo)
    assert narration_projection(undo_port.revision_closure(undone['revision_id']))==value['narration']
    assert narration_projection(later_port.revision_closure(accepted['revision_id']))==value['narration']
    mutate(s,"UPDATE managed_output_lifecycle SET state='reclaimed'")
    mutate(s,'UPDATE attempts SET settled=0')
    s.cas.path_for(refs['speech']['object_id'][7:]).write_bytes(b'changed')
    before=snapshot(s)
    assert port.accept(value)['stored_result']==accepted['stored_result']
    assert s.commit_timeline(p,'main',request,idempotency_key=request['request_id'],identity=IDENTITY)==accepted['stored_result']
    assert snapshot(s)==before
    conflicting=copy.deepcopy(request);conflicting['label']='conflicting'
    with pytest.raises(ConflictError):s.commit_timeline(p,'main',conflicting,idempotency_key=request['request_id'],identity=IDENTITY)


def test_failure_before_receipt_persistence_rolls_back_everything(fixture,monkeypatch):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    original=s._command_record
    def fail(kind,*a,**kw):
        if kind=='timeline.commit':raise RuntimeError('injected after narration validation')
        return original(kind,*a,**kw)
    monkeypatch.setattr(s,'_command_record',fail)
    before=snapshot(s)
    with pytest.raises(RuntimeError,match='injected'):port.accept(value)
    assert snapshot(s)==before


def test_canonical_array_words_and_no_change_receipt(fixture):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    clip=value['publication']['internal_timeline_revisions'][0]['payload']['clips'][-1]
    clip['app']['astrid']['words']=[[w['start_s'],w['end_s'],w['word'],f'word-{i}'] for i,w in enumerate(take['words']['words'])]
    value['narration']['lines'][0]['line_digest']=digest(clip)
    first=port.accept(value)
    request=wire(p,key='no-change-narration');request['base_revision_id']=first['revision_id']
    port=s._request_commit_port(request,IDENTITY)
    assert port.narration_take(refs)==take
    nochange=acceptance(s,p,request=request,no_change=True)
    nochange['narration']=value['narration']
    result=port.accept(nochange)
    assert result['outcome']=='no_change'
    assert result['revision_id'] is None
    assert result['receipt']['narration_state']['parent_revision_id']==first['revision_id']
    assert result['receipt']['narration_state']['projection']==value['narration']


def test_sqlite_fences_lifecycle_and_head_during_narration_validation(fixture,monkeypatch):
    import sqlite3
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    original=s._managed_narration_take
    calls=[]
    def checked(*args):
        assert s.store.conn.in_transaction
        with sqlite3.connect(s.store.db_path,timeout=0) as competitor:
            for sql in ("UPDATE managed_output_lifecycle SET state='reclaimed'", "UPDATE parent_composition_heads SET updated_at='race'"):
                with pytest.raises(sqlite3.OperationalError,match='locked'):competitor.execute(sql)
        calls.append(True)
        return original(*args)
    monkeypatch.setattr(s,'_managed_narration_take',checked)
    assert port.accept(value)['outcome']=='accepted'
    assert calls


def test_realm_fence_and_unknown_pinned_base_ref(fixture,monkeypatch):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    unrelated=s._request_commit_port(wire(p),IDENTITY)
    before=snapshot(s)
    with pytest.raises(AuthorizationError):unrelated.narration_take(refs)
    monkeypatch.setattr(s,'realm',{**s.realm,'id':'foreign'})
    with pytest.raises(AuthorizationError):s._request_commit_port(request,IDENTITY).narration_take(refs)
    with pytest.raises(AuthorizationError):port.accept(value)
    assert snapshot(s)==before


def test_lost_response_after_commit_replays_before_provider_or_dependency_reads(fixture,monkeypatch):
    from runtime_protocol.contract_metadata import SCHEMA_DIGEST
    s,p=fixture
    refs,m,w=managed_take(s,p)
    request=request_for(p,refs)
    observed=[]
    class Provider:
        interface_version=1
        contract_digest=SCHEMA_DIGEST
        def commit(self,request,port):
            observed.append('provider')
            port.narration_take(refs)
            return port.accept(prepared(s,p,request,refs,m,w))['stored_result']
    s.register_timeline_commit_provider(Provider())
    durable=[]
    def lose_response(result):
        assert not s.store.conn.in_transaction
        durable.append(result)
        raise TimeoutError('lost response after durable narration commit')
    monkeypatch.setattr(s,'_after_timeline_commit',lose_response,raising=False)
    with pytest.raises(TimeoutError):s.commit_timeline(p,'main',request,idempotency_key=request['request_id'],identity=IDENTITY)
    assert len(durable)==1
    mutate(s,"UPDATE managed_output_lifecycle SET state='reclaimed'")
    def never_read(*args):raise AssertionError('replay reopened narration dependency')
    monkeypatch.setattr(s,'_managed_narration_take',never_read)
    assert s.commit_timeline(p,'main',request,idempotency_key=request['request_id'],identity=IDENTITY)==durable[0]
    assert observed==['provider']


def test_opaque_unrelated_take_metadata_survives(fixture):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    clip=value['publication']['internal_timeline_revisions'][0]['payload']['clips'][-1]
    clip['app']['other']={'take':'opaque foreign metadata','extra':[None,{'v':False}]}
    value['narration']['lines'][0]['line_digest']=digest(clip)
    result=port.accept(value)
    internal=port.revision_closure(result['revision_id'])['internal_timeline_revisions'][0]['payload']
    assert internal['clips'][-1]['app']['other']==clip['app']['other']


def test_parent_and_occurrence_lines_have_distinct_scopes(fixture):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    pub=value['publication'];internal=pub['internal_timeline_revisions'][0]
    pub['parent_composition']['clips']=[copy.deepcopy(internal['payload']['clips'][-1])]
    pub['parent_composition']['registry']=copy.deepcopy(internal['payload']['registry'])
    closure={'parent_revision':{'payload':pub['parent_composition']},
             'shot_revisions':pub['shot_revisions'],'internal_timeline_revisions':pub['internal_timeline_revisions']}
    value['narration']=narration_projection(closure)
    assert [v['occurrence_id'] for v in value['narration']['lines']]==[None,'occurrence-1']
    result=port.accept(value)
    valid(result,'AcceptResponse')
    assert result['receipt']['narration_state']['projection']==value['narration']
    assert narration_projection(port.revision_closure(result['revision_id']))==value['narration']


def test_parent_take_cannot_bypass_candidate_validation(fixture):
    s,p=fixture
    refs,request,port,take,value=setup(s,p)
    pub=value['publication'];internal=pub['internal_timeline_revisions'][0]
    clip=internal['payload']['clips'].pop()
    pub['parent_composition']['clips']=[clip]
    pub['parent_composition']['registry']=copy.deepcopy(internal['payload']['registry'])
    value['narration']={'version':1,'lines':[]}
    before=snapshot(s)
    with pytest.raises(ValidationError,match='projection'):port.accept(value)
    assert snapshot(s)==before
