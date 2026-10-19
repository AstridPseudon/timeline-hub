"""Matched host/relay ABI negatives; disposable native children only."""
import copy
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
from types import SimpleNamespace
import pytest
from banodoco_local import hosted_contract as contract
from banodoco_local import custody_broker as custody


@pytest.fixture
def launch(tmp_path):
    broker=SimpleNamespace(role='host',owner_epoch='epoch',run_id='run',custody_generation=1,authority_scope_root=tmp_path)
    preparation={'owner_epoch':'epoch','operation_id':'operation','channel_id':'channel',
                 'profile':{'host_executable':sys.executable},'custody_scope':str(tmp_path)}
    launch=contract.HostedLaunch(broker,preparation)
    argv=[sys.executable,'-m','astrid.core.execution.generic_host','run',
          '--host-control-fd',str(launch.children['control'].fileno()),
          '--activation-fd',str(launch.children['activation'].fileno()),
          '--activation-operation-id','operation','--activation-channel-id','channel']
    environment=launch.environment(argv)
    try:yield launch,argv,environment
    finally:launch.close()


@pytest.fixture
def verified_launch(tmp_path):
    broker = SimpleNamespace(role='host', owner_epoch='epoch', run_id='run',
        custody_generation=1, authority_scope_root=tmp_path)
    preparation = {'owner_epoch': 'epoch', 'operation_id': 'operation', 'channel_id': 'channel',
        'profile': {'host_executable': sys.executable}, 'custody_scope': str(tmp_path)}
    selected = contract.HostedLaunch(broker, preparation)
    try:
        with contract.readonly_payload(b'verified binding') as binding:
            argv = [sys.executable, '-I', '-S', '-B', str(tmp_path / 'selected-launcher.py'),
                '--binding-fd', str(binding.fileno())]
            yield selected, binding, argv
    finally:
        selected.close()


def test_verified_binding_launch_is_exact_and_digest_bound(verified_launch):
    selected, binding, argv = verified_launch
    selected.environment(argv, launch_binding=binding)
    assert binding.fileno() in contract.validate(selected.value, role='host', argv=argv)
    assert selected.value['launch_binding']['identity'] == contract.file_identity(binding.fileno())
    substituted = list(argv)
    substituted[4] = str(Path(argv[4]).with_name('other-launcher.py'))
    with pytest.raises(contract.HostedContractError):
        contract.validate(selected.value, role='host', argv=substituted)
    with pytest.raises(contract.HostedContractError):
        selected.environment(argv, launch_binding=binding)


@pytest.mark.parametrize('change', [
    'interpreter', 'legacy-six', 'missing-isolation', 'missing-no-site', 'reordered-flags',
    'relative-launcher', 'wrong-binding-flag', 'missing-binding-flag', 'missing-descriptor',
    'extra-binding-arg', 'wrong-descriptor', 'negative-descriptor',
])
def test_verified_binding_launch_refuses_changed_shape(verified_launch, change):
    selected, binding, original = verified_launch
    argv = list(original)
    if change == 'interpreter': argv[0] += '-other'
    elif change == 'legacy-six': argv.remove('-B')
    elif change == 'missing-isolation': argv.remove('-I')
    elif change == 'missing-no-site': argv.remove('-S')
    elif change == 'reordered-flags': argv[1:4] = ['-B', '-I', '-S']
    elif change == 'relative-launcher': argv[4] = 'selected-launcher.py'
    elif change == 'wrong-binding-flag': argv[5] = '--other-fd'
    elif change == 'missing-binding-flag': del argv[5]
    elif change == 'missing-descriptor': argv.pop()
    elif change == 'extra-binding-arg': argv.append('extra')
    elif change == 'wrong-descriptor': argv[6] = str(binding.fileno() + 1)
    elif change == 'negative-descriptor': argv[6] = '-1'
    with pytest.raises(contract.HostedContractError):
        selected.environment(argv, launch_binding=binding)
    assert selected.value is None


def test_verified_binding_launch_refuses_nonprivate_writable_descriptor(verified_launch, tmp_path):
    selected, _, argv = verified_launch
    with (tmp_path / 'writable-binding').open('w+b') as writable:
        writable.write(b'untrusted binding')
        writable.flush()
        argv[-1] = str(writable.fileno())
        with pytest.raises(contract.HostedContractError):
            selected.environment(argv, launch_binding=writable)


def test_verifier_claimed_argv_enters_hosted_contract_without_launch(tmp_path, monkeypatch):
    from test_verified_host_launch import fixture_authority
    monkeypatch.setattr(subprocess, 'Popen', lambda *a, **kw: pytest.fail('seam must not spawn'))
    fixture = fixture_authority(tmp_path)
    preparation = fixture.args['preparation']
    broker = SimpleNamespace(role='host', owner_epoch=preparation['owner_epoch'], run_id='run',
        custody_generation=1, authority_scope_root=Path(preparation['custody_scope']))
    selected = contract.HostedLaunch(broker, preparation)
    try:
        proof = fixture.verifier.verify(**fixture.args)
        with contract.readonly_payload(b'pending') as binding:
            argv, payload = fixture.verifier.claim(proof, **fixture.args, binding_fd=binding.fileno())
            with contract.readonly_payload(payload) as replacement:
                os.dup2(replacement.fileno(), binding.fileno(), inheritable=False)
            selected.environment(argv, launch_binding=binding)
            contract.validate(selected.value, role='host', argv=argv)
            assert contract.read_payload(binding.fileno(), selected.value['launch_binding']['digest']) == payload
    finally:
        selected.close()


@pytest.mark.parametrize('field,value',[('role','engine'),('purpose','runtime-relay-control/v1'),
    ('generation',False),('generation',0),('argv_digest','sha256:'+'0'*64),('owner_epoch','')])
def test_hosted_binding_refuses_wrong_role_purpose_and_launch(launch,field,value):
    selected,argv,_=launch
    forged=copy.deepcopy(selected.value);forged[field]=value
    with pytest.raises(contract.HostedContractError):contract.validate(forged,role='host',argv=argv)


@pytest.mark.parametrize('change',['missing','extra','reversed','inode','pipe','file'])
def test_hosted_binding_refuses_descriptor_substitution(launch,change):
    selected,argv,_=launch;forged=copy.deepcopy(selected.value);owned=[]
    try:
        if change=='missing':del forged['sockets']['activation']
        elif change=='extra':forged['sockets']['extra']=forged['sockets']['control']
        elif change=='reversed':forged['sockets']['control']['fd']=forged['sockets']['activation']['fd']
        elif change=='inode':forged['sockets']['control']['inode']+=1
        elif change=='pipe':
            owned.extend(os.pipe());forged['sockets']['control']['fd']=owned[0]
        elif change=='file':
            with contract.readonly_payload(b'fake') as file:
                forged['sockets']['control']['fd']=file.fileno()
                with pytest.raises(contract.HostedContractError):contract.validate(forged,role='host')
            return
        with pytest.raises(contract.HostedContractError):contract.validate(forged,role='host')
    finally:
        for fd in owned:os.close(fd)


def test_hosted_binding_is_digest_bound_readonly_consumed_and_unlinked(launch):
    selected,argv,_=launch
    fd=selected.binding.fileno()
    assert contract.read_payload(fd,contract.digest(contract.canonical(selected.value)))==contract.canonical(selected.value)
    with pytest.raises(OSError):os.write(fd,b'changed')
    with pytest.raises(contract.HostedContractError):contract.read_payload(fd,'sha256:'+'0'*64)
    assert os.fstat(fd).st_nlink==0
    assert set(selected.pass_fds)=={fd,*(c.fileno() for c in selected.children.values())}


@pytest.mark.parametrize('mutation',['owner','generation','operation','profile'])
def test_hosted_preparation_fences_before_dispatch(launch,mutation):
    selected,_,_=launch;value=copy.deepcopy(selected.value);request=copy.deepcopy(selected.preparation)
    if mutation=='owner':request['owner_epoch']='foreign'
    if mutation=='generation':value['generation']=3
    if mutation=='operation':request['operation_id']='foreign'
    if mutation=='profile':request['profile']['changed']=True
    authority=SimpleNamespace(reference=lambda:{'generation':1,'target':{'pid':os.getpid()}},
        verify_reference=lambda *a,**kw:pytest.fail('invalid preparation reached authority verification'))
    with pytest.raises(contract.HostedContractError):contract.verify_preparation(value,request,authority,actor=None)


@pytest.mark.skipif(sys.platform!='darwin',reason='native trusted host bootstrap is Darwin only')
@pytest.mark.parametrize('mutation',['wrong-role','stale-generation','missing','extra'])
def test_actual_trampoline_refuses_before_generic_host_entry(tmp_path,mutation):
    scope=tmp_path/'scope';scope.mkdir(mode=0o700)
    broker=custody.RoleBoundCustodyBroker(role='host',identity_provider=custody.default_process_identity,
        ledger_root=scope/'host-admission',authority_scope_root=scope,authority_journal=scope/'admissions.jsonl',owner_epoch='epoch',timeout=1)
    preparation={'owner_epoch':'epoch','operation_id':'operation','channel_id':'channel',
        'profile':{'host_executable':sys.executable},'custody_scope':str(scope)}
    selected=broker.create_hosted_launch(preparation)
    ready=tmp_path/'must-not-enter.json'
    argv=[sys.executable,'-m','astrid.core.execution.generic_host','run','--pack-root',str(tmp_path),
        '--host-control-fd',str(selected.children['control'].fileno()),
        '--activation-fd',str(selected.children['activation'].fileno()),
        '--activation-operation-id','operation','--activation-channel-id','channel','--ready-file',str(ready)]
    environment={'PATH':'/usr/bin:/bin'}
    environment.update(selected.environment(argv));environment.update(broker.child_environment(argv,start_new_session=True))
    fds=selected.pass_fds;forged=None;extra=[]
    try:
        if mutation=='wrong-role':environment['ASTRID_RUNTIME_CUSTODY_ROLE']='engine'
        elif mutation=='stale-generation':
            value=copy.deepcopy(selected.value);value['generation']+=1
            payload=contract.canonical(value);forged=contract.readonly_payload(payload)
            environment[contract.FD_KEY]=str(forged.fileno());environment[contract.DIGEST_KEY]=contract.digest(payload)
            fds=tuple(fd for fd in fds if fd!=selected.binding.fileno())+(forged.fileno(),)
        elif mutation=='missing':fds=tuple(fd for fd in fds if fd!=selected.children['activation'].fileno())
        else:extra.extend(os.pipe());fds+=tuple(extra)
        child=subprocess.Popen(custody.custody_wrapper_argv(sys.executable),env=environment,stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,pass_fds=fds,close_fds=True)
        code=child.wait(timeout=4)
        assert code!=0 and not ready.exists()
        broker._thread.join(2)
        assert not broker._thread.is_alive() and broker.registration is None
        assert not broker.socket_path.exists() and custody.default_process_identity(child.pid) is None
    finally:
        selected.close()
        if forged is not None:forged.close()
        for fd in extra:os.close(fd)
        broker.abort_before_spawn()


@pytest.mark.skipif(sys.platform!='darwin',reason='native process incarnation is Darwin only')
def test_actual_consumer_rejects_inherited_other_process_incarnation(launch,tmp_path):
    selected,_,_=launch
    proof,environment=contract.publish_consumer(selected.value,contract.incarnation(os.getpid()))
    marker=tmp_path/'untrusted-entry'
    program="import runpy,sys; m=runpy.run_path(sys.argv[1]); m['consume']('host',{'control':int(sys.argv[2]),'activation':int(sys.argv[3])}); open(sys.argv[4],'w').write('untrusted')"
    try:
        child=subprocess.Popen([sys.executable,'-I','-S','-c',program,contract.__file__,
            str(selected.children['control'].fileno()),str(selected.children['activation'].fileno()),str(marker)],
            env={'PATH':'/usr/bin:/bin',**environment},stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
            close_fds=True,pass_fds=tuple(c.fileno() for c in selected.children.values())+(proof.fileno(),))
        assert child.wait(timeout=4)!=0 and not marker.exists()
        assert custody.default_process_identity(child.pid) is None
    finally:proof.close()

@pytest.mark.skipif(sys.platform!='darwin',reason='native relay bootstrap is Darwin only')
def test_actual_relay_consumer_fences_operation_before_host_launch(tmp_path):
    from runtime_protocol.local_execution_supervisor import send_frame,receive_frame,CONTROL_VERSION,RetainedProcess
    from test_local_execution_supervisor import _prepare_case
    import runtime_protocol.local_execution_supervisor as supervisor
    preparation,_=_prepare_case();scope=tmp_path/'scope';scope.mkdir(mode=0o700)
    from runtime_protocol.local_worker_composition import _actual_executable
    executable=str(_actual_executable(os.getpid()))
    preparation['custody_scope']=str(scope);preparation['profile']['worker_executable']=executable
    broker=custody.RoleBoundCustodyBroker(role='relay',identity_provider=custody.default_process_identity,
        ledger_root=scope/'relay-admission',authority_scope_root=scope,authority_journal=scope/'admissions.jsonl',
        owner_epoch=preparation['owner_epoch'],timeout=5)
    selected=broker.create_hosted_launch(preparation)
    argv=[executable,'-I','-S',supervisor.__file__,'--prepared-control-fd',str(selected.children['control'].fileno())]
    environment={'PATH':'/usr/bin:/bin'};environment.update(selected.environment(argv));environment.update(broker.child_environment(argv,start_new_session=True))
    retained=None
    try:
        child=subprocess.Popen(custody.custody_wrapper_argv(executable),env=environment,stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True,pass_fds=selected.pass_fds)
        retained=RetainedProcess(child);selected.close_children();broker.wait_until_sealed();retained.bind_actor()
        forged=copy.deepcopy(preparation);forged['operation_id']='foreign-operation'
        control=selected.parents['control'];control.settimeout(5)
        send_frame(control,{'version':CONTROL_VERSION,'command':'prepare','preparation':forged,'config':{}})
        reply=receive_frame(control)
        assert reply=={'version':CONTROL_VERSION,'status':'unresolved','error_code':'operation_unresolved'}
        assert not (scope/'host-admission').exists() and retained.verify()['pid']==child.pid
        import signal
        broker.signal(signal.SIGTERM,expected_pid=child.pid)
        assert retained.wait(5)==-signal.SIGTERM
        assert custody.default_process_identity(child.pid) is None and not broker.socket_path.exists()
    finally:
        if retained is not None and retained.poll() is None:
            import signal
            try:
                broker.signal(signal.SIGKILL,expected_pid=retained.child.pid)
            except custody.CustodyError:
                # Closing our own control invokes the relay's existing EOF
                # lifecycle; positive retained wait remains mandatory.
                selected.close()
            retained.wait(5)
        selected.close()
