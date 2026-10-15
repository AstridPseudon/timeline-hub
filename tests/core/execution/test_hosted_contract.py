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
from astrid.core.execution import hosted_contract as contract
from astrid.core.execution import custody_broker as custody


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
