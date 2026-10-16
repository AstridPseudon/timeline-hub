"""Canonical commit acceptance revalidates after semantic preparation."""
import json
import threading
import time

import pytest

from http_helpers import Api
from runtime_protocol.contract_metadata import SCHEMA_DIGEST
from runtime_protocol.errors import AuthorizationError, ForbiddenError
from test_narration_commit import managed_take, prepared as narration_prepared, request_for
from test_selected_media_commit import mutate, snapshot
from test_timeline_accept import acceptance, count, fixture, http_server, wire


@pytest.mark.parametrize('narrated', [False, True])
@pytest.mark.parametrize('mutation',['revoke','rotation','scope','expiry'])
def test_paired_canonical_accept_rechecks_current_authority_after_preparation(fixture,tmp_path,mutation,narrated):
    s,p=fixture
    if narrated:
        refs,manifest,words=managed_take(s,p)
    server,thread,unused=http_server(s,tmp_path)
    s.select_project('connector',p)
    token,_=server.credentials.provision_connector('connector',
        ['handshake','projects:read','projects:write'],connector_id='c',realm_id=s.realm['id'],expires_at=time.time()+120)
    context=dict(pair_id='pair',connector_id='c',realm_id=s.realm['id'],generation=1,expires_at=int((time.time()+90)*1000))
    headers={'X-Reigh-Paired-Session':json.dumps(context)}
    api=Api(unused.endpoint,token)
    prepared=threading.Event();resume=threading.Event()
    calls=[]
    class Provider:
        interface_version=1
        contract_digest=SCHEMA_DIGEST
        def commit(self,request,port):
            if narrated:
                port.narration_take(refs)
                template=narration_prepared(s,p,request,refs,manifest,words)
            else:
                template=acceptance(s,p,request=request)
            calls.append(port.head()['revision_id'])
            prepared.set()
            assert resume.wait(5)
            return port.accept(template)['stored_result']
    s.register_timeline_commit_provider(Provider())
    request=request_for(p,refs) if narrated else wire(p)
    request['asserted_actor']['id']='connector'
    outcome=[]
    def save():
        try:
            outcome.append(api.request('POST',f'/astrid/v1/projects/{p}/timelines/main/commit',request,
                headers={**headers,'Idempotency-Key':request['request_id'],'X-Astrid-Session':request['session_id']}))
        except RuntimeError as exc:outcome.append(exc)
    try:
        api.request('GET','/v1/handshake',headers=headers)
        baseline=s.store.conn.total_changes
        before=snapshot(s)
        worker=threading.Thread(target=save);worker.start();assert prepared.wait(5)
        grant=server.paired_sessions._sessions['pair']
        if mutation=='revoke':server.paired_sessions.revoke(grant)
        elif mutation=='rotation':server.credentials.provision_connector('connector',
            ['handshake','projects:read','projects:write'],connector_id='c',realm_id=s.realm['id'],expires_at=time.time()+120,rotate=True)
        else:
            meta=server.credentials.actor_metadata('connector')
            if mutation=='scope':meta['scopes']=['handshake','projects:read']
            else:meta['expires_at']=time.time()-1
            server.credentials._publish('connector',token,meta)
        resume.set();worker.join(5);assert not worker.is_alive()
        assert len(outcome)==1 and isinstance(outcome[0],RuntimeError)
        assert outcome[0].status in (401,403)
        assert calls==['parent-1']
        assert s.store.conn.total_changes==baseline
        assert count(s,'parent_composition_revisions')==1
        assert s.lookup_request(p,'main',request['request_id']) is None
        assert snapshot(s)==before
    finally:
        resume.set();server.shutdown();server.server_close();thread.join()


def test_live_paired_narration_replay_keeps_pins_and_rechecks_revocation(fixture,tmp_path,monkeypatch):
    s,p=fixture
    refs,manifest,words=managed_take(s,p)
    server,thread,unused=http_server(s,tmp_path)
    s.select_project('connector',p)
    token,_=server.credentials.provision_connector('connector',
        ['handshake','projects:read','projects:write'],connector_id='c',realm_id=s.realm['id'],expires_at=time.time()+120)
    context=dict(pair_id='pair',connector_id='c',realm_id=s.realm['id'],generation=1,expires_at=int((time.time()+90)*1000))
    request=request_for(p,refs);request['asserted_actor']['id']='connector'
    headers={'X-Reigh-Paired-Session':json.dumps(context),
             'Idempotency-Key':request['request_id'],'X-Astrid-Session':request['session_id']}
    api=Api(unused.endpoint,token)
    calls=[]
    ports=[]
    class Provider:
        interface_version=1
        contract_digest=SCHEMA_DIGEST
        def commit(self,request,port):
            calls.append('prepare')
            ports.append(port)
            unknown={name:dict(ref) for name,ref in refs.items()}
            unknown['speech']['association_id']='outside-request'
            with pytest.raises(AuthorizationError):
                port.narration_take(unknown)
            port.narration_take(refs)
            return port.accept(narration_prepared(s,p,request,refs,manifest,words))['stored_result']
    s.register_timeline_commit_provider(Provider())
    path=f'/astrid/v1/projects/{p}/timelines/main/commit'
    try:
        api.request('GET','/v1/handshake',headers=headers)
        first=api.request('POST',path,request,headers=headers)
        assert first['status']=='accepted', first
        stored=s.lookup_request(p,'main',request['request_id'])
        assert stored['result']['runtime_receipt']['narration_state']['projection']['lines'][0]['take']==refs
        mutate(s,"UPDATE managed_output_lifecycle SET state='reclaimed'")
        def never_read(*args):
            raise AssertionError('accepted replay reopened immutable take')
        monkeypatch.setattr(s,'_managed_narration_take',never_read)
        assert api.request('POST',path,request,headers=headers)==first
        assert calls==['prepare']
        server.paired_sessions.revoke(server.paired_sessions._sessions['pair'])
        before=snapshot(s)
        with pytest.raises(RuntimeError) as error:
            api.request('POST',path,request,headers=headers)
        assert error.value.status==403
        assert snapshot(s)==before
        with pytest.raises(ForbiddenError):
            ports[0].narration_take(refs)
        assert s.lookup_request(p,'main',request['request_id'])==stored
        assert calls==['prepare']
    finally:
        server.shutdown();server.server_close();thread.join()
