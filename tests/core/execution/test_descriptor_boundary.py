"""Actual fake-only Darwin bootstrap/SETEXEC proof; no Runtime or Wan enablement."""
from dataclasses import replace
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys

import pytest

from astrid.core.execution import custody_broker as cb, generic_host as host, process_group as groups
from tests.core.execution.test_confinement_launch_integration import launch  # noqa: F401
from tests.core.execution.test_wan_custody_limits import (
    WORKER, private_socket_transport, assert_denied_work,  # noqa: F401
)


PROBE = WORKER.split("if role=='descendant':")[0] + r'''
import runpy,socket
value=probe()
value['env']=dict(os.environ)
try:
    s=socket.socket();s.settimeout(.2)
    try:s.connect(('127.0.0.1',9));value['network']='allowed'
    finally:s.close()
except OSError as exc:value['network']=exc.errno
(project/('inside-'+role)).write_text('synthetic-inside-write')
if role=='worker':
    if len(sys.argv)>5:raise RuntimeError('unexpected arguments')
    channel=os.environ.get('ASTRID_COMMAND_CONTROL_FD')
    if channel:
        m=runpy.run_path(str(project/'custody_broker.py'),run_name='fake_inventory_worker')
        results=[]
        for operation in m['_COMMAND_GIT_OPERATIONS'].values():
            result=m['command_inventory_git'](['-C',str(project),*operation],cwd=project)
            results.append({'code':result.returncode,'stdout':result.stdout})
        value['operations']=results
        for client in m['_COMMAND_CLIENTS'].values():client.channel.close()
    child=subprocess.run([sys.executable,'-I','-S','-B',__file__,inside,outside,str(project),'descendant'],
                         stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                         close_fds=True,start_new_session=True,check=True)
    value['descendant']=json.loads(child.stdout)
print(json.dumps(value),flush=True)
'''


@pytest.fixture
def setup(tmp_path, launch, private_socket_transport):
    policy, _, inside, outside = launch
    project = policy.project.project_root
    (project/'custody_broker.py').write_bytes(Path(cb.__file__).read_bytes())
    probe = tmp_path/'probe.py'; probe.write_text(PROBE)
    # The same enumerated interpreter closure as WP2 native workers.
    policy = replace(policy, bootstrap_files=(*policy.bootstrap_files, probe,
        Path('/opt/homebrew/opt/libb2/lib/libb2.1.dylib'),
        Path('/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib'),
        Path('/opt/homebrew/opt/openssl@3/lib/libssl.3.dylib')))
    plan = host._confined_launch_plan([str(Path(sys.executable).resolve()),'-I','-S','-B',str(probe),
        str(inside),str(outside),str(project),'worker'], policy=policy, cwd=project,
        parent_environment={'ASTRID_DISABLE_SANDBOX':'1','ASTRID_COMMAND_CONTROL_FD':'0',
                            'ASTRID_RUNTIME_CUSTODY_PIPES':'[]','SECRET':'synthetic'})
    private_socket_transport[0] = plan.cwd
    return policy, plan


def fake_inventory(monkeypatch, policy, plan):
    """Only host discovery is synthetic; real auth/framing/validation/helper custody run."""
    project=policy.project.project_root
    state=policy.private_write_root/'fake-state.json';state.write_text('{}')
    git=policy.private_write_root/'git'
    git.write_text('#!'+str(Path(sys.executable).resolve())+' -I\n'
        'import json,sys\nfrom pathlib import Path\n'
        'p=Path(sys.argv[2])/"helper-operations.jsonl"\n'
        'with p.open("a") as f:f.write(json.dumps(sys.argv[3:])+"\\n")\n'
        'print("synthetic-inventory-result")\n')
    git.chmod(0o700)
    selected={'state_path':str(state),'state_sha256':cb._digest_bytes(state.read_bytes()),
        'roots':{str(project):[str(project)]},'git':str(git),'git_sha256':cb._digest_bytes(git.read_bytes()),
        'cwd':str(plan.cwd),'environment':dict(plan.environment)}
    monkeypatch.setattr(cb,'_inventory_launch_policy',lambda environment,cwd:selected)
    original=cb.shutil.which
    monkeypatch.setattr(cb.shutil,'which',lambda command,*a,**k:str(git) if command=='git' else original(command,*a,**k))


@pytest.mark.parametrize('inventory',[False,True])
def test_actual_trampoline_worker_exec_session_policy_environment_and_full_fds(setup,tmp_path,monkeypatch,inventory):
    policy,plan=setup
    if inventory:fake_inventory(monkeypatch,policy,plan)
    else:monkeypatch.setattr(cb,'_inventory_launch_policy',lambda *args:None)
    fake_files=[]
    for name in ('fake-owner.lock','unrelated-host-file'):
        stream=(tmp_path/name).open('w+');stream.write('synthetic');stream.flush()
        os.set_inheritable(stream.fileno(),True);fake_files.append(stream)
    forbidden={(os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino) for f in fake_files}
    process=None
    try:
        process=groups.popen_owned_group(list(plan.argv),**plan.subprocess_options())
        output,error=process.communicate(timeout=15)
        assert process.returncode==0,error.decode()
        custody=process._astrid_custody
        custody.finish_inventory_owner()
        groups.verify_tree_absent(process)
        observed=json.loads(output)
        broker=custody._launch_broker
        approved={item['fd']:item for item in broker.child_pipe_binding}
        for role,value in [('worker',observed),('descendant',observed['descendant'])]:
            assert_denied_work(value)
            assert value['network'] in {1,13}
            assert (policy.project.project_root/('inside-'+role)).read_text()=='synthetic-inside-write'
            assert not forbidden.intersection((f['device'],f['inode']) for f in value['fds'])
            extra=[f for f in value['fds'] if f['fd']>2]
            assert {f['fd'] for f in value['fds']} == {0,1,2} | (set(approved) if inventory and role=='worker' else set())
            for f in extra:
                assert f['type']==stat.S_IFIFO
                assert (f['device'],f['inode'])==(approved[f['fd']]['device'],approved[f['fd']]['inode'])
            expected=dict(plan.environment)
            if inventory:expected[cb._COMMAND_INVENTORY_FD]=cb._canonical(broker.child_pipe_binding).decode()
            if '__CF_USER_TEXT_ENCODING' in value['env']:expected['__CF_USER_TEXT_ENCODING']=f'0x{os.getuid():X}:0x0:0x0'
            assert value['env']==expected
        assert observed['pid']==process.pid==broker.registration['pid']
        assert custody._handles[process.pid][0]==broker.registration['identity']['birth_id']
        assert observed['descendant']['sid']==observed['descendant']['pid']!=observed['sid']
        if inventory:
            assert observed['operations']==[{'code':0,'stdout':'synthetic-inventory-result\n'}]*4
            operations=[json.loads(line) for line in (policy.project.project_root/'helper-operations.jsonl').read_text().splitlines()]
            assert operations==[list(tail) for tail in cb._COMMAND_GIT_OPERATIONS.values()]
            assert custody._inventory_owner.pending is None and custody._inventory_owner.error is None
        else:assert custody._inventory_owner is None
        print('DESCRIPTOR_ACTUAL',json.dumps({'inventory':inventory,'approved':broker.child_pipe_binding,
              'launch_argv':plan.argv,'launch_environment':dict(plan.environment),
              'launch_cwd':str(plan.cwd),'initial_pass_fds':plan.pass_fds,
              'registration':broker.registration,'observed':observed,'cleanup':process._astrid_cleanup_semantics}))
    finally:
        if process is not None:
            if process.poll() is None:groups.terminate_tree(process)
            process.wait(timeout=5)
            for stream in (process.stdin,process.stdout,process.stderr):
                if stream is not None:stream.close()
        for stream in fake_files:stream.close()


def test_no_channel_provisioning_semantics(monkeypatch):
    monkeypatch.delenv(cb._COMMAND_INVENTORY_FD,raising=False)
    assert cb.command_inventory_git(['-C','/synthetic','rev-parse','HEAD']) is None


@pytest.mark.parametrize('fault',['missing','closed','file','socket','substituted','mismatched','direction','unsupported_role','ack','registration','authentication','task-pin','exec'])
def test_actual_failed_bootstrap_never_executes_workload(setup,tmp_path,monkeypatch,fault):
    policy,plan=setup
    marker=policy.project.project_root/'UNTRUSTED-EXECUTED'
    target=[str(Path(sys.executable).resolve()),'-I','-S','-B','-c',f'from pathlib import Path;Path({str(marker)!r}).touch()']
    broker=cb.RoleBoundCustodyBroker(role='command',retain_channel=True,identity_provider=cb.default_process_identity,
        ledger_root=tmp_path/'failed-ledger',timeout=.4)
    environment={**dict(plan.environment),**broker.child_environment(target,start_new_session=True),
                 'ASTRID_COMMAND_CUSTODY_ENABLED':'1'}
    pipes=json.loads(environment[cb._BOOTSTRAP_PIPES]);pass_fds=list(broker.child_pipe_fds)
    extra=[]
    if fault=='missing':environment.pop(cb._BOOTSTRAP_PIPES)
    elif fault=='closed':pass_fds=[]
    elif fault in {'file','socket','substituted','mismatched'}:
        if fault=='file':
            fd=os.open(tmp_path/'fake-substitute',os.O_CREAT|os.O_RDONLY,0o600);extra=[fd]
        elif fault=='socket':
            import socket
            left,right=socket.socketpair();fd=left.detach();extra=[fd,right.detach()]
        else:
            fd,write=os.pipe();extra=[fd,write]
        pipes[0]['fd']=fd
        if fault in {'file','socket','mismatched'}:pipes[0].update(device=os.fstat(fd).st_dev,inode=os.fstat(fd).st_ino)
        environment[cb._BOOTSTRAP_PIPES]=json.dumps(pipes);pass_fds+=extra
    elif fault=='direction':pipes.reverse();environment[cb._BOOTSTRAP_PIPES]=json.dumps(pipes)
    elif fault=='unsupported_role':environment['ASTRID_RUNTIME_CUSTODY_ROLE']='unsupported'
    elif fault=='ack':
        original=cb._send_frame
        def send(channel,frame):
            if frame.get('status')=='registered':frame={**frame,'registration_digest':'wrong'}
            original(channel,frame)
        monkeypatch.setattr(cb,'_send_frame',send)
    elif fault=='registration':environment['ASTRID_RUNTIME_CUSTODY_RUN_ID']='wrong'
    elif fault=='authentication':
        monkeypatch.setattr(cb,'_peer_token',lambda channel:{'pid':1,'uid':-1})
    elif fault=='task-pin':
        original_peer=cb._peer_token
        monkeypatch.setattr(cb,'_peer_token',lambda channel:{**original_peer(channel),'sha256':'wrong'})
    elif fault=='exec':
        # A valid executable-format check is not an exec-success guarantee.
        executable=tmp_path/'invalid-executable';executable.write_text('synthetic invalid executable');executable.chmod(0o700)
        environment.update(broker.child_environment([str(executable)],start_new_session=True))
    process=None
    try:
        process=subprocess.Popen(cb.custody_wrapper_argv(sys.executable),env=environment,cwd=plan.cwd,
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True,pass_fds=tuple(pass_fds))
        broker.close_child_pipes()
        out,err=process.communicate(timeout=5)
        assert process.returncode!=0 and not marker.exists()
        with pytest.raises(cb.CustodyError):broker.wait_until_sealed()
        assert not broker._release_sent and not broker._post_exec_authority_validated
        assert broker.registration is None or broker.registration['pid']==process.pid
        assert not cb.default_process_identity(process.pid)
        print('DESCRIPTOR_REFUSAL',json.dumps({'fault':fault,'pid':process.pid,'exit':process.returncode,
              'stage':broker._observation_phase,'registered':broker.registration is not None,'workload_marker':marker.exists()}))
    finally:
        if process is not None:
            if process.poll() is None:process.kill()
            process.wait(timeout=5)
        for fd in extra:os.close(fd)
        broker.close_child_pipes();broker.listener.close();broker._thread.join(2)
        if broker.operation_channel is not None:broker.operation_channel.close()
        broker.socket_path.unlink(missing_ok=True)
        if broker.socket_root.exists():broker.socket_root.rmdir()


@pytest.mark.parametrize('cancel',[False,True])
def test_actual_suspended_launch_failure_or_cancellation_has_original_waiter(setup,tmp_path,monkeypatch,cancel):
    policy,plan=setup
    monkeypatch.setattr(cb,'_inventory_launch_policy',lambda *args:None)
    if not cancel:
        def fail(_self):raise cb.CustodyError('synthetic failure before release')
        monkeypatch.setattr(cb.ProcessCustody,'start_inventory_owner',fail)
        with pytest.raises(cb.CustodyError,match='synthetic failure') as error:
            groups.popen_owned_group(list(plan.argv),**plan.subprocess_options())
        process=error.value.process
        assert process.returncode==-signal.SIGKILL
        assert not (policy.project.project_root/'inside-worker').exists()
    else:
        process=groups.popen_owned_group([*list(plan.argv[:3]),str(Path(sys.executable).resolve()),'-I','-S','-B','-c',
            'import time;print("ready",flush=True);time.sleep(30)'],**plan.subprocess_options())
        assert process.stdout.readline()==b'ready\n'
        groups.terminate_tree(process)
        process.wait(timeout=5)
        groups.verify_tree_absent(process)
    assert process._astrid_custody.process is process
    assert process.returncode is not None
    assert cb.default_process_identity(process.pid) is None
    for stream in (process.stdin,process.stdout,process.stderr):stream.close()
    print('DESCRIPTOR_REAP',json.dumps({'cancel':cancel,'pid':process.pid,'original_wait':process.returncode}))


def test_actual_inventory_operation_denial_is_sticky_without_helper_fallback(setup,tmp_path,monkeypatch):
    policy,plan=setup
    fake_inventory(monkeypatch,policy,plan)
    probe=next(path for path in policy.bootstrap_files if path.name=='probe.py')
    probe.write_text(PROBE.replace("['-C',str(project),*operation]","['-C',str(project.parent),*operation]"))
    process=groups.popen_owned_group(list(plan.argv),**plan.subprocess_options())
    try:
        output,error=process.communicate(timeout=10)
        assert process.returncode!=0
        owner=process._astrid_custody._inventory_owner
        with pytest.raises(cb.CustodyError,match='uncertain'):owner.finish()
        assert owner.error is not None and not owner.helpers
        assert not (policy.project.project_root/'helper-operations.jsonl').exists()
        assert not (policy.project.project_root/'inside-descendant').exists()
        assert cb.default_process_identity(process.pid) is None
        print('DESCRIPTOR_OPERATION_DENIED',json.dumps({'pid':process.pid,'exit':process.returncode,
              'stage':owner.failure_stage,'helpers':list(owner.helpers),'first_failure':owner.first_failure}))
    finally:
        if process.poll() is None:groups.terminate_tree(process)
        process.wait(timeout=5)
        for stream in (process.stdin,process.stdout,process.stderr):stream.close()


def test_actual_engine_pipe_matches_control_client_and_retained_host_consumer(setup,tmp_path):
    from types import SimpleNamespace
    from astrid.core.execution import vibecomfy_engine_adapter as adapter
    policy,plan=setup
    project=policy.project.project_root
    (project/'engine_adapter.py').write_bytes(Path(adapter.__file__).read_bytes())
    script=next(path for path in policy.bootstrap_files if path.name=='probe.py')
    script.write_text(WORKER.split("if role=='descendant':")[0]+r'''
import runpy,types
value=probe()
m=runpy.run_path(str(project/'custody_broker.py'),run_name='fake_engine_custody')
a=runpy.run_path(str(project/'engine_adapter.py'),run_name='fake_engine_adapter')
channel=m['_PipeChannel'].from_binding(os.environ.pop('ASTRID_ENGINE_CONTROL_FD'))
client=a['EngineControlClient'](channel=channel,custody=types.SimpleNamespace(**m),
    reference_reader=lambda:None,custody_scope=str(project),operation_id='fake-operation',
    channel_id='fake-channel',owner_epoch='fake-epoch',source_pins_digest=m['_digest_bytes'](m['_canonical']({})))
value['source_fact']=client.observe_source_fact('current_source_revision')
print(json.dumps(value),flush=True)
sys.stdin.readline()
channel.close()
''')
    custody=cb.ProcessCustody(scope_root=tmp_path/'engine-custody',owner_epoch='fake-epoch')
    broker=cb.RoleBoundCustodyBroker(role='engine',retain_channel=True,identity_provider=cb.default_process_identity,
        ledger_root=tmp_path/'engine-ledger',owner_epoch='fake-epoch')
    custody._launch_broker=broker
    environment={**dict(plan.environment),**broker.child_environment(plan.argv,start_new_session=True)}
    graph=host._NativeEngineGraph(request={'profile':{'engine_launch':{'source_revision':'synthetic-revision'}},
        'operation_id':'fake-operation','channel_id':'fake-channel','owner_epoch':'fake-epoch'})
    graph.engine=broker;graph.custody=custody
    graph._source_observer=SimpleNamespace(pins={},observe=lambda fact,pid:'synthetic-revision')
    graph._engine_parent=SimpleNamespace(actor=None)
    graph._engine_parent.verify=lambda:graph._engine_parent.actor.verify()
    process=subprocess.Popen(cb.custody_wrapper_argv(sys.executable),env=environment,cwd=plan.cwd,
        stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True,pass_fds=broker.child_pipe_fds)
    process._astrid_custody=custody;process._astrid_process_group_id=process.pid
    graph.process=process
    try:
        custody.bind_launch(process)
        process._astrid_process_birth=custody._handles[process.pid][0]
        groups.observe_tree(process);custody.start_observer()
        graph._start_native_control();custody.release_launch();graph._engine_released.set()
        # The real matched client and host parser exchange a bound narrow fact.
        result=json.loads(process.stdout.readline())
        assert result['source_fact']=='synthetic-revision'
        assert_denied_work(result)
        expected={0,1,2,*broker.child_pipe_fds}
        assert {item['fd'] for item in result['fds']}==expected
        assert all(item['type']==stat.S_IFIFO for item in result['fds'])
        assert graph._native_error is None
        assert graph._engine_parent.verify()['pid']==process.pid
        process.communicate(b'exit\n',timeout=5)
        assert process.returncode==0
        groups.verify_tree_absent(process)
        graph._native_thread.join(2)
        assert not graph._native_thread.is_alive()
        print('DESCRIPTOR_ENGINE_CONTROL',json.dumps({'approved':broker.child_pipe_binding,
              'launch_argv':plan.argv,'launch_environment':dict(plan.environment),'launch_cwd':str(plan.cwd),
              'result':result,'pid':process.pid,'wait':process.returncode}))
    finally:
        if process.poll() is None:groups.terminate_tree(process)
        process.wait(timeout=5)
        for stream in (process.stdin,process.stdout,process.stderr):stream.close()
        broker.operation_channel.close()


def test_unmatched_caller_pipe_is_refused_before_spawn_or_custody(monkeypatch):
    read_fd,write_fd=os.pipe()
    monkeypatch.setattr(groups,'ProcessCustody',lambda **kw:pytest.fail('custody allocation for unmatched channels'))
    monkeypatch.setattr(groups.subprocess,'Popen',lambda *a,**kw:pytest.fail('unmatched channel spawn'))
    try:
        with pytest.raises(cb.CustodyError,match='admitted pipe consumer'):
            groups.popen_owned_group([sys.executable],pass_fds=(read_fd,))
    finally:os.close(read_fd);os.close(write_fd)


@pytest.mark.parametrize('fault',['ack','registration'])
def test_actual_launch_path_registration_failure_retains_original_child_obligation(setup,monkeypatch,fault):
    policy,plan=setup
    monkeypatch.setattr(cb,'_inventory_launch_policy',lambda *args:None)
    original=cb.RoleBoundCustodyBroker.child_environment
    def environment(broker,*args,**kwargs):
        broker.timeout=.4
        result=original(broker,*args,**kwargs)
        if fault=='registration':result['ASTRID_RUNTIME_CUSTODY_RUN_ID']='wrong'
        return result
    monkeypatch.setattr(cb.RoleBoundCustodyBroker,'child_environment',environment)
    if fault=='ack':
        original_send=cb._send_frame
        def send(channel,frame):
            if frame.get('status')=='registered':frame={**frame,'registration_digest':'wrong'}
            original_send(channel,frame)
        monkeypatch.setattr(cb,'_send_frame',send)
    with pytest.raises(cb.CustodyError) as error:
        groups.popen_owned_group(list(plan.argv),**plan.subprocess_options())
    process=error.value.process
    try:
        assert process._astrid_custody is error.value.custody
        assert process._astrid_custody.process is process
        assert process._astrid_custody._uncertain is not None
        assert not process._astrid_custody._launch_broker._release_sent
        assert process.wait(timeout=5)!=0
        assert not (policy.project.project_root/'inside-worker').exists()
        assert cb.default_process_identity(process.pid) is None
        print('DESCRIPTOR_RETAINED_FAILURE',json.dumps({'fault':fault,'pid':process.pid,'wait':process.returncode,
              'uncertain':True,'released':False}))
    finally:
        if process.poll() is None:process.kill()
        process.wait(timeout=5)
        for stream in (process.stdin,process.stdout,process.stderr):stream.close()


@pytest.mark.parametrize('phase',['before','during'])
def test_bootstrap_token_capture_refuses_same_wall_birth_with_different_native_incarnation(monkeypatch,phase):
    start={'pid':123,'uid':501,'start_abstime':100,'start_sec':1,'start_usec':2,'status':2}
    changed={**start,'start_abstime':101}
    samples=iter([changed] if phase=='before' else [start,changed])
    monkeypatch.setattr(cb,'_darwin_process_start',lambda pid:next(samples))
    captures=[]
    monkeypatch.setattr(cb,'current_process_audit_token',lambda pid:captures.append(pid) or {'pid':pid})
    with pytest.raises(cb.CustodyError,match='incarnation changed'):
        cb._bootstrap_anchored_token(123,cb._start_anchor(start))
    assert captures==([] if phase=='before' else [123])


@pytest.mark.parametrize('fault',['peer','birth','clock'])
def test_bootstrap_birth_fence_refuses_unauthenticated_or_ambiguous_initial_pin(monkeypatch,fault):
    start={'pid':123,'uid':501,'start_abstime':100,'start_sec':1,'start_usec':2,'status':2}
    calls=[]
    def native(pid):
        calls.append(pid)
        return {**start,'start_abstime':101} if fault=='birth' and len(calls)>1 else start
    monkeypatch.setattr(cb,'_darwin_process_start',native)
    monkeypatch.setattr(cb,'current_process_audit_token',lambda pid:{'pid':124 if fault=='peer' else pid})
    monkeypatch.setattr(cb,'_darwin_absolute_time',lambda:100 if fault=='clock' else 102)
    with pytest.raises(cb.CustodyError,match='start anchor differs'):
        cb._authenticated_bootstrap_anchor(123,{'pid':123})
