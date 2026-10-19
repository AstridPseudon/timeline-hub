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


def test_host_inspection_pipes_require_cpu_selection_and_bind_exact_endpoints(tmp_path):
    reads = os.pipe(); writes = os.pipe()
    selected = None
    try:
        pipes = [custody._pipe_identity(reads[0], os.O_RDONLY),
                 custody._pipe_identity(writes[1], os.O_WRONLY)]
        broker = SimpleNamespace(role='host', owner_epoch='epoch', run_id='run', custody_generation=1,
                                 authority_scope_root=tmp_path, child_pipe_binding=pipes)
        preparation = {'owner_epoch':'epoch', 'operation_id':'op', 'channel_id':'channel',
                       'profile':{'host_executable':sys.executable}, 'custody_scope':str(tmp_path)}
        selected = contract.HostedLaunch(broker, preparation)
        argv = [sys.executable, '-m', 'astrid.core.execution.generic_host', 'run',
                '--host-control-fd', str(selected.children['control'].fileno()),
                '--activation-fd', str(selected.children['activation'].fileno()),
                '--activation-operation-id', 'op', '--activation-channel-id', 'channel']
        with pytest.raises(contract.HostedContractError, match='selected CPU Host'):
            selected.environment(argv)
        selected.close(); selected = contract.HostedLaunch(broker, preparation)
        preparation['profile'].update(execution_mode='host_only_cpu', host_launch={'renderer_selection':{'selected':True}})
        # Rebuild argv for the newly owned socket pair.
        argv[5] = str(selected.children['control'].fileno())
        argv[7] = str(selected.children['activation'].fileno())
        selected.environment(argv)
        assert {reads[0], writes[1]} <= set(selected.pass_fds)
        # The native trampoline imports this stdlib module without a package.
        import runpy
        standalone = runpy.run_path(contract.__file__)
        assert standalone['validate'](selected.value, role='host') == contract.validate(selected.value, role='host')

        forged = copy.deepcopy(selected.value)
        forged['inspection_pipes'][0]['inode'] += 1
        with pytest.raises((contract.HostedContractError, custody.CustodyError)):
            contract.validate(forged, role='host')
    finally:
        if selected is not None: selected.close()
        for descriptor in (*reads, *writes): os.close(descriptor)


@pytest.mark.parametrize('launch_fixture', ['launch', 'cpu_launch'])
@pytest.mark.parametrize('mutation',['owner','generation','operation','channel','profile'])
def test_hosted_preparation_fences_before_dispatch(request,launch_fixture,mutation):
    case = request.getfixturevalue(launch_fixture)
    if launch_fixture == 'cpu_launch':
        selected = case.selected
        selected.environment(case.argv)
    else:
        selected,_,_ = case
    value=copy.deepcopy(selected.value);request=copy.deepcopy(selected.preparation)
    if mutation=='owner':request['owner_epoch']='foreign'
    if mutation=='generation':value['generation']=3
    if mutation=='operation':request['operation_id']='foreign'
    if mutation=='channel':request['channel_id']='foreign'
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
        # These negatives deliberately exported a launch and waited their
        # actual rejected child. They cannot claim never-spawned retirement.
        with pytest.raises(custody.CustodyError, match="never-exported"):
            broker.abort_before_spawn()
        broker._release_authority_scope()


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


@pytest.fixture
def cpu_launch(tmp_path, monkeypatch):
    """The real SDK HostedLaunch owns real sockets and anonymous pipes."""
    from astrid.core.execution import host_renderer_selection, generic_host
    from astrid.core.rendering import remotion_runtime
    def forbidden(*args, **kwargs):
        pytest.fail('CPU static inspection activated renderer or executed a probe')
    monkeypatch.setattr(host_renderer_selection, 'activate_renderer_selection', forbidden)
    monkeypatch.setattr(remotion_runtime, 'prepare_remotion_validation', forbidden)
    monkeypatch.setattr(generic_host.subprocess, 'run', forbidden)
    packs = tmp_path/'packs'; packs.mkdir()
    extra = tmp_path/'extra'; extra.mkdir()
    manifest = {'schema_version': 1, 'id': 'test.cpu', 'name': 'CPU', 'kind': 'external', 'version': '1.0',
        'command': {'argv': ['{python_exec}', '-c', 'pass']}, 'outputs': [],
        'isolation': {'mode': 'subprocess', 'network': False, 'binaries': ['missing-optional']}}
    manifest_path = packs/'executor.yaml'; manifest_path.write_text(json.dumps(manifest))
    pipes = [os.pipe(), os.pipe()]
    broker = SimpleNamespace(role='host', owner_epoch='epoch', run_id='run', custody_generation=1,
        authority_scope_root=tmp_path, child_pipe_binding=[contract._pipe_identity(pipes[0][0], os.O_RDONLY),
                                                         contract._pipe_identity(pipes[1][1], os.O_WRONLY)])
    launch = {'pack_root': str(packs), 'capability_matrix': None}
    profile = {'host_executable': sys.executable, 'execution_mode': 'host_only_cpu', 'host_launch': launch,
               'session_config_digest': contract.digest(contract.canonical(launch))}
    request = {'owner_epoch': 'epoch', 'operation_id': 'op', 'channel_id': 'channel',
               'profile': profile, 'custody_scope': str(tmp_path)}
    selected = contract.HostedLaunch(broker, request)
    argv = [sys.executable, '-m', 'astrid.core.execution.generic_host', 'run',
            '--host-control-fd', str(selected.children['control'].fileno()),
            '--activation-fd', str(selected.children['activation'].fileno()),
            '--activation-operation-id', 'op', '--activation-channel-id', 'channel']
    try:
        yield SimpleNamespace(selected=selected, argv=argv, profile=profile, launch=launch,
                              manifest=manifest, manifest_path=manifest_path, packs=packs, extra=extra)
    finally:
        selected.close()
        for pair in pipes:
            for fd in pair: os.close(fd)


@pytest.mark.parametrize('selection', ['root', 'additional', 'matrix'])
def test_cpu_binary_declarations_admit_real_pipes_without_renderer(cpu_launch, selection, tmp_path):
    case = cpu_launch
    if selection == 'additional':
        case.manifest_path.rename(case.extra/'executor.yaml')
        case.launch['additional_pack_roots'] = [{'path': str(case.extra), 'files': {}}]
    elif selection == 'matrix':
        case.manifest['isolation']['binaries'] = []
        case.manifest_path.write_text(json.dumps(case.manifest))
        matrix = tmp_path/'matrix.json'
        matrix.write_text(json.dumps({'schema_version': 1, 'capabilities': [{'id': 'test.cpu',
            'disposition': 'required', 'evidence_reason': 'offline test', 'required_binaries': ['missing-optional']}]}))
        case.launch['capability_matrix'] = str(matrix)
    case.profile['session_config_digest'] = contract.digest(contract.canonical(case.launch))
    env = case.selected.environment(case.argv)
    assert 'renderer_selection' not in case.launch
    assert case.selected.value['profile_digest'] == contract.digest(contract.canonical(case.profile))
    assert case.selected.value['inspection_pipes'] == case.selected.broker.child_pipe_binding
    assert {p['fd'] for p in case.selected.value['inspection_pipes']} <= set(case.selected.pass_fds)
    assert contract.read_payload(int(env[contract.FD_KEY]), env[contract.DIGEST_KEY]) == contract.canonical(case.selected.value)
    # Loading the bootstrap standalone must never need package discovery.
    import runpy
    import builtins
    original_import = builtins.__import__
    def stdlib_only(name, *args, **kwargs):
        assert name != 'astrid' and not name.startswith('astrid.')
        return original_import(name, *args, **kwargs)
    with pytest.MonkeyPatch.context() as standalone_imports:
        standalone_imports.setattr(builtins, '__import__', stdlib_only)
        standalone = runpy.run_path(contract.__file__)
    assert standalone['validate'](case.selected.value, role='host') == contract.validate(case.selected.value, role='host')


@pytest.mark.parametrize('fault', ['mode', 'role', 'no-needs', 'unselected-matrix', 'profile-launch', 'argv', 'executable'])
def test_cpu_inspection_refuses_unselected_or_changed_authority(cpu_launch, fault, tmp_path):
    case = cpu_launch
    if fault == 'mode': case.profile['execution_mode'] = 'engine'
    elif fault == 'role':
        case.selected.broker.role = 'relay'
        case.profile['worker_executable'] = sys.executable
        case.argv = [sys.executable, '-I', '-S', '/offline/local_execution_supervisor.py',
                     '--prepared-control-fd', str(case.selected.children['control'].fileno())]
    elif fault in {'no-needs', 'unselected-matrix'}:
        case.manifest['isolation']['binaries'] = []
        case.manifest_path.write_text(json.dumps(case.manifest))
        if fault == 'unselected-matrix':
            matrix = tmp_path/'matrix.json'
            matrix.write_text(json.dumps({'schema_version': 1, 'capabilities': [{'id': 'foreign.cpu',
                'disposition': 'required', 'evidence_reason': 'offline test', 'required_binaries': ['helper']}]}))
            case.launch['capability_matrix'] = str(matrix)
        case.profile['session_config_digest'] = contract.digest(contract.canonical(case.launch))
    elif fault == 'profile-launch': case.launch['additional_pack_roots'] = [{'path': str(case.extra)}]
    elif fault == 'argv': case.argv[-1] = 'foreign-channel'
    elif fault == 'executable': case.argv[0] = '/foreign/python'
    with pytest.raises(contract.HostedContractError): case.selected.environment(case.argv)
    assert case.selected.binding is None


@pytest.mark.parametrize('fault', ['inode', 'substituted', 'direction', 'collision', 'socket'])
def test_cpu_inspection_rejects_pipe_tampering(cpu_launch, fault):
    case = cpu_launch
    case.selected.environment(case.argv)
    forged = copy.deepcopy(case.selected.value)
    pipes = forged['inspection_pipes']
    other = os.pipe()
    try:
        if fault == 'inode': pipes[0]['inode'] += 1
        elif fault == 'substituted': pipes[0]['fd'] = other[0]
        elif fault == 'direction': pipes[0]['direction'] = os.O_WRONLY
        elif fault == 'collision': pipes[1] = dict(pipes[0])
        elif fault == 'socket': pipes[0]['fd'] = case.selected.children['control'].fileno()
        with pytest.raises(contract.HostedContractError): contract.validate(forged, role='host')
    finally:
        for fd in other: os.close(fd)
