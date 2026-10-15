"""Actual pipe/executor source checks; no Chrome, Node or renderer proof."""
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
from types import SimpleNamespace

import pytest

from astrid.core.execution import generic_host as gh
from astrid.core.execution import remotion_host_session as hs
from astrid.core.execution import remotion_pipe as pipe


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setenv('ASTRID_SOURCE_STATE', str(tmp_path/'absent-state.json'))
    monkeypatch.delenv('ASTRID_PACKS_PATH', raising=False)
    project=tmp_path/'remotion'; (project/'src').mkdir(parents=True)
    (project/'src/astrid-frame-worker.mjs').write_text('// no native launch')
    cli=project/'node_modules/@remotion/cli/remotion-cli.js';cli.parent.mkdir(parents=True);cli.write_text('// fixture')
    (tmp_path/'props.json').write_text('{}')
    env={'ASTRID_REMOTION_PROJECT_DIR':str(project),'ASTRID_NODE_EXECUTABLE':str(Path(sys.executable).resolve())}
    manager=hs.HostRemotionSession(track=lambda p:None,untrack=lambda p:None)
    monkeypatch.setattr(hs,'_host_browser_executable',lambda:None)
    calls=[]
    monkeypatch.setattr(manager,'_start',lambda *a:None)
    def exchange(request):
        calls.append(request)
        return {'ok':True,'evaluation':[{'frame':0,'layers':[]}], 'primary':'original-reply'}
    monkeypatch.setattr(manager,'_exchange',exchange)
    def frame():
        return {'type':'evaluate','projectDir':str(project),'compositionId':'AstridTrackEvaluation',
                'nodeExecutable':str(Path(sys.executable).resolve()),'remotionCli':str(cli),
                'propsPath':str(tmp_path/'props.json'),'outputDir':str(tmp_path/'unused'),
                'frames':[0],'resolution':None,'port':31500,'environment':{}}
    yield tmp_path,env,manager,calls,frame
    for lease in tuple(manager._leases):lease.close()
    manager.close()


def stop(process):
    if process.poll() is None:process.terminate()
    process.wait(timeout=10)


def child(code):
    root=str(Path(gh.__file__).resolve().parents[3])
    return [sys.executable,'-I','-S','-B','-c',f'import sys;sys.path[:0]={[root,*sys.path[1:]]!r};'+code]


def launch_bridge(setup, code):
    tmp,env,manager,calls,frame=setup
    process=subprocess.Popen(child(code),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
    lease=manager.lease(env,attempt=tmp)
    bridge=pipe.HostPipeBridge(lease,process,admission={'capability_id':'rendering.timeline_visualize',
                 'capability_digest':'fixture-admitted','version':'1','source':{'source_digest':'fixture-source'}},launch_digest='selected-launch')
    return process,lease,bridge


def test_actual_standard_pipes_preserve_original_reply_and_exclude_parent_socket(setup):
    tmp,env,manager,calls,frame=setup
    parent,peer=socket.socketpair();parent.set_inheritable(True)
    code='''import os,stat,json
from astrid.core.execution.remotion_pipe import install_executor_client
from astrid.core.execution.remotion_host_session import _read
c=install_executor_client()
sockets=[]
for fd in range(256):
 try:
  if stat.S_ISSOCK(os.fstat(fd).st_mode):sockets.append(fd)
 except OSError:pass
assert not sockets,sockets
reply=c.request('same-original-owner',REQUEST,_read)
assert reply['primary']=='original-reply'
reply['pid']=os.getpid();reply['sockets']=sockets
from pathlib import Path
Path(OUTPUT).write_text(json.dumps(reply))
c.close()
'''.replace('REQUEST',repr(frame())).replace('OUTPUT',repr(str(tmp/'reply.json')))
    process,lease,bridge=launch_bridge(setup,code)
    try:
        assert process.wait(timeout=20)==0
        stdout,stderr=bridge.finish()
        reply=json.loads((tmp/'reply.json').read_text())
        assert reply['pid']==process.pid and reply['sockets']==[]
        assert reply['primary']=='original-reply'
        assert len(calls)==1 and calls[0]['type']=='evaluate'
        assert bridge.binding['admission']['source']['source_digest']=='fixture-source'
        assert bridge.binding['generation']==manager.frame_owner.generation
        assert lease.child.fileno()>=0 # remains only in trusted parent
        assert not stdout and not stderr
    finally:
        stop(process);lease.close();parent.close();peer.close()
    assert not bridge.thread.is_alive() and not bridge.stderr_thread.is_alive()
    assert all(stream.closed for stream in (process.stdin,process.stdout,process.stderr))
    print('PIPE_BOUNDARY_EVIDENCE',json.dumps({'pid':process.pid,'returncode':process.returncode,'pipe_streams_closed':True,'threads_joined':True}))


@pytest.mark.parametrize('mutation',['binding','sequence','sequence-bool','generation','oversize'])
def test_refuse_bad_bound_pipe_requests_without_native_exchange(setup,mutation):
    tmp,env,manager,calls,frame=setup
    code='''import json,os,sys
from astrid.core.execution.remotion_pipe import _line,_decode,PREFIX,_encode
b=_decode(_line(0)); frame={'identity':'fixture','request':REQUEST,'_rendererPipe':{'binding':b['digest'],'sequence':1}}
MUTATION
os.write(1,PREFIX+_encode(frame))
'''.replace('REQUEST',repr(frame()))
    code=code.replace('MUTATION',{'binding':"frame['_rendererPipe']['binding']='wrong'",'sequence':"frame['_rendererPipe']['sequence']=2",'sequence-bool':"frame['_rendererPipe']['sequence']=True",'generation':'import time;time.sleep(0.2)', 'oversize':"frame['padding']='x'*(8*1024*1024)"}[mutation])
    process,lease,bridge=launch_bridge(setup,code)
    try:
        if mutation=='generation':manager.frame_owner.generation+=1
        process.wait(timeout=20)
        if mutation=='oversize':
            assert process.returncode!=0
            bridge.finish(cancelled=True)
        else:
            with pytest.raises(RuntimeError,match='relay failed'):bridge.finish(cancelled=True)
        assert calls==[]
    finally:
        stop(process);lease.close()


def test_executor_bootstrap_wrong_incarnation_refused_before_code(setup):
    process=subprocess.Popen(child('from astrid.core.execution.remotion_pipe import install_executor_client;install_executor_client();raise AssertionError("untrusted marker")'),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
    binding={'purpose':'rendering.timeline_visualize','pid':process.pid+1,'birth':'wrong','executable':str(Path(sys.executable).resolve())}
    raw=pipe._encode({'protocol':pipe.VERSION,'binding':binding,'digest':hashlib.sha256(pipe._encode(binding)).hexdigest()})
    out,err=process.communicate(raw,timeout=20)
    assert process.returncode!=0 and b'incarnation' in err and b'AssertionError: untrusted marker' not in err


def test_cancel_original_pipe_child_waits_and_releases_original_owner(setup):
    tmp,env,manager,calls,frame=setup
    process,lease,bridge=launch_bridge(setup,"from astrid.core.execution.remotion_pipe import install_executor_client;install_executor_client();import time;time.sleep(30)")
    try:
        stop(process)
        bridge.finish(cancelled=True)
        assert bridge._released and process.poll() is not None
        assert manager.process is None and manager.uncertain is None
    finally:
        stop(process);lease.close()
    assert not bridge.thread.is_alive() and not bridge.stderr_thread.is_alive()
    assert all(stream.closed for stream in (process.stdin,process.stdout,process.stderr))
    print('PIPE_BOUNDARY_EVIDENCE',json.dumps({'pid':process.pid,'returncode':process.returncode,'pipe_streams_closed':True,'threads_joined':True}))


def test_legacy_renderer_socket_installer_is_refused():
    with pytest.raises(ValueError,match='socket inheritance is not admitted'):
        hs.install_host_remotion_client(-1)


def configure_host(setup, monkeypatch):
    tmp,env,manager,calls,frame=setup
    h=gh.GenericPackHost(pack_roots=[],attempt_base=tmp)
    h._remotion_host_session=manager
    launches=[]
    h._pipe_test_payloads=[]
    def plan(argv,**kw):
        assert kw.get('inherited_fds',())==()
        launches.append(list(argv))
        for arg in argv:
            if str(arg).endswith('.astrid-capability-request.json'):
                h._pipe_test_payloads.append(json.loads(Path(arg).read_text()))
        return SimpleNamespace(argv=tuple(argv),cwd=tmp,environment=tuple(sorted(env.items())),
                  subprocess_options=lambda:{'cwd':str(tmp),'env':{**os.environ,**env},'stdin':subprocess.PIPE,
                      'stdout':subprocess.PIPE,'stderr':subprocess.PIPE,'close_fds':True,'pass_fds':()})
    monkeypatch.setattr(h,'_workload_launch_plan',plan)
    monkeypatch.setattr(gh,'popen_owned_group',lambda argv,**options:subprocess.Popen(argv,**options))
    monkeypatch.setattr(gh,'observe_tree',lambda p:None)
    monkeypatch.setattr(gh,'_terminate_process_group',stop)
    monkeypatch.setattr(gh,'_release_owned_group',stop)
    monkeypatch.setattr(gh,'_dependency_pythonpath',lambda:[])
    return h,launches


def test_command_entry_uses_actual_stdio_worker_without_inherited_fds(setup,monkeypatch):
    tmp,env,manager,calls,frame=setup
    h,launches=configure_host(setup,monkeypatch)
    code="from astrid.core.execution.remotion_host_session import host_remotion_client,_read;assert host_remotion_client().request('command',"+repr(frame())+",_read)['ok']"
    record=SimpleNamespace(id='rendering.timeline_visualize',source_root=tmp,capability_digest='command-admitted',
            definition=SimpleNamespace(command=object(),metadata={},inputs=[],outputs=[],version='1'))
    monkeypatch.setattr(gh,'_bind_host_owned_command_values',lambda r,v,**kw:v)
    monkeypatch.setattr(gh,'_bind_host_owned_command_outputs',lambda r,v,**kw:(v,None))
    monkeypatch.setattr(gh,'assert_provided_inputs_bound',lambda *a:None)
    monkeypatch.setattr(gh,'harvest_staged_outputs',lambda *a,**kw:[])
    monkeypatch.setattr(gh,'_command_worker_pythonpath',lambda r,p:p)
    monkeypatch.setattr(gh,'expand_command',lambda *a:SimpleNamespace(argv=[sys.executable,'-c',code],env={},cwd=str(tmp)))
    monkeypatch.setattr(h,'_child_environment',lambda *a,**kw:({**os.environ,**env},{}))
    output=tmp/'outputs';output.mkdir()
    result=h._run_command_definition(record,{},output,tmp)
    assert result.returncode==0 and len(calls)==1
    assert '--renderer-command-stdio' in launches[0]
    assert not h._active_processes and not manager._leases
    print('COMMAND_PIPE_EVIDENCE',json.dumps({'pid':result.process_id,'returncode':result.returncode,'active_processes':0,'active_leases':0}))


def test_registry_entry_preserves_real_action_admission_and_pipe_client(setup,monkeypatch):
    tmp,env,manager,calls,frame=setup
    h,launches=configure_host(setup,monkeypatch)
    root=tmp/'rendering';(root/'actions').mkdir(parents=True)
    code="def run():\n from astrid.core.execution.remotion_host_session import host_remotion_client,_read\n return host_remotion_client().request('registry',"+repr(frame())+",_read)\n"
    (root/'actions/query.py').write_text(code)
    (root/'pack.yaml').write_text(json.dumps({'schema_version':3,'id':'rendering','name':'fixture','version':'1.0.0','actions':{'timeline_visualize':{'description':'disposable pipe query fixture','invocation':{'kind':'python','path':'actions/query.py','function':'run'},'inputs':[],'outputs':{},'metadata':{'adapter_family':'cpu','resource_keys':['cpu'],'project_scope':'optional'}}}}))
    h.pack_roots=(root,);h.discover()
    definition,admission=h.admit('executor','rendering.timeline_visualize')
    private=tmp/'private';private.mkdir()
    monkeypatch.setattr(h,'_required_confinement_policy',lambda a:SimpleNamespace(private_write_root=private))
    monkeypatch.setattr(gh,'_confined_launch_plan',lambda *a,**kw:None)
    result=h.invoke_capability(capability_kind='executor',capability_id='rendering.timeline_visualize',
             request={'inputs':{},'out':str(tmp),'project':'fixture','project_was_auto_resolved':True,'invocation':'runtime'},
             attempt=tmp,definition=definition,admission=admission,child_env=env)
    assert result.ok and result.payload['action_result']['primary']=='original-reply'
    assert len(calls)==1 and not h._active_processes and not manager._leases
    print('REGISTRY_PIPE_EVIDENCE',json.dumps({'pid':result.process_id,'returncode':result.returncode,'active_processes':0,'active_leases':0,'admission_digest':admission['capability_digest']}))
    payload=h._pipe_test_payloads[0]
    assert payload['remotion_pipe'] is True and 'remotion_host_fd' not in payload
    assert payload['admission']==admission and payload['definition']==definition
    # The original fence refuses changed source before any next launch.
    (root/'actions/query.py').write_text(code+'# changed\n')
    with pytest.raises(gh.HostError,match='source digest changed'):
        h.invoke_capability(capability_kind='executor',capability_id='rendering.timeline_visualize',request={},
                  attempt=tmp,definition=definition,admission=admission,child_env=env)
    assert len(launches)==1


def test_cancel_native_uncertainty_forbids_new_owner_lease(setup,monkeypatch):
    tmp,env,manager,calls,frame=setup
    process,lease,bridge=launch_bridge(setup,"from astrid.core.execution.remotion_pipe import install_executor_client;install_executor_client();import time;time.sleep(30)")
    try:
        stop(process)
        manager.uncertain=RuntimeError('original native cleanup uncertain')
        with pytest.raises(RuntimeError,match='cancellation cleanup unproved'):
            bridge.finish(cancelled=True)
        with pytest.raises(RuntimeError,match='cleanup is unresolved'):
            manager.lease(env,attempt=tmp)
        assert not bridge._released
    finally:
        stop(process);lease.close()
        # This is a no-native fixture; retain uncertainty through the assertions.
        manager.uncertain=None
