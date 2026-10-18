"""Isolated children keep their selected interpreter's stdlib ahead of packages."""
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.execution import generic_host as host
from tests.core.execution import test_confinement_launch_integration as confinement
from tests.test_generic_host import _write_manifest

launch = confinement.launch


@pytest.fixture(scope='module')
def action_installation(tmp_path_factory):
    runtime = os.environ.get('ACTION_CLOSURE_TEST_RUNTIME')
    if not runtime:
        pytest.skip('select admitted Runtime test helpers for coupled offline proof')
    import importlib.util
    tests = Path(runtime)/'tests'
    sys.path.insert(0,str(tests))
    try:
        spec=importlib.util.spec_from_file_location('action_closure_test_helpers',tests/'test_verified_host_launch.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module.selected_action_installation.__wrapped__(tmp_path_factory)
    finally:
        sys.path.remove(str(tests))


@pytest.fixture
def selected_command(action_installation,tmp_path,monkeypatch):
    import copy
    from runtime_protocol import verified_host_launch as gate
    from astrid.core.execution import custody_broker,hosted_contract
    from astrid.core.execution.network_broker import ObservableNetworkBroker
    f=action_installation
    h=host.GenericPackHost(pack_roots=[f.root/'astrid/packs/generation'],capability_matrix=f.matrix)
    h.discover();record=h.capabilities['generation.generate_speech']
    retained=copy.deepcopy(f.retained)
    profile={'host_launch':{'selected_actions':retained['actions']},'profile_digest':'sha256:'+'b'*64}
    retained['profile_digest']=gate.raw_digest(profile)
    monkeypatch.setattr(host,'_RETAINED_ACTION_LAUNCH',retained,raising=False)
    preparation=host.LocalExecutionPreparation(operation_id='prepare',channel_id='channel')
    owner={'pid':123,'uid':os.getuid(),'birth_id':'runtime-owner'}
    preparation._request={'profile':profile,'runtime_owner':dict(owner),'custody_scope':str(tmp_path/'custody'),
        'owner_epoch':'epoch','operation_id':'prepare','channel_id':'channel'}
    preparation._activation_grant={'operation_id':'prepare','channel_id':'channel'}
    preparation._hosted_binding={'generation':1}
    preparation._retained_relay_actor=SimpleNamespace(verify=lambda:dict(owner))
    preparation._claim_host=h;preparation.result={'status':'prepared'}
    h._selected_action_preparation=preparation
    reference={'generation':1,'target':{'pid':os.getpid(),'birth_id':host.process_birth_identity()}}
    class Authority:
        def __init__(self,*args):pass
        def reference(self):return reference
        def verify_reference(self,ref,*,expected_actor,owner_epoch):
            assert expected_actor == owner
            if owner_epoch != 'epoch':raise host.HostError('owner epoch differs')
    monkeypatch.setattr(custody_broker,'RoleCustodyAuthority',Authority)
    monkeypatch.setattr(hosted_contract,'verify_preparation',lambda *a,**kw:None)
    fields=dict(task_id='task',attempt_id='attempt',lease_id='lease',fence=1,runtime_epoch=1,
        project_id=None,operation=record.id,executor_id=h.executor_id)
    authority=host._AuthenticatedAttempt(tuple(sorted(fields.items())))
    h._attempt_claim_authority=authority
    h.client=SimpleNamespace(confirm_claim_authority=lambda **kw:authority)
    attempt=tmp_path/'attempt';inputs=attempt/'inputs';outputs=attempt/'outputs'
    for p in (inputs,outputs):p.mkdir(parents=True)
    policy=host._ConfinementPolicy(attempt,outputs,host._SandboxProjectScope(inputs,(inputs,)),
        (Path(sys.executable),), (f.root,), host._SandboxEnvironmentPolicy(),claim_binding=authority.fields)
    h._confinement_policy=policy
    admission=dict(task_id='task',attempt_id='attempt',fence=1,network_nonce='nonce',capability_digest=record.capability_digest,
        source_digest=record.source_digest,dependency_digest=record.dependency_digest)
    broker=ObservableNetworkBroker().register_admission(admission,allowed_routes=host._provider_routes(record),
        evidence_path=attempt/'broker-evidence.json',evidence_key='evidence-key',auth_token='task-only-token')
    # An offline retained-object seam; no listener/thread/service starts.
    broker._server=SimpleNamespace(server_address=('127.0.0.1',43210))
    broker._thread=SimpleNamespace(is_alive=lambda:True)
    declared=host._network_policy(record)
    policy_network={**declared,'proxy':broker.endpoint,'allowed_destinations':[broker.endpoint],
        'broker':{**declared['broker'],'evidence_path':str(broker.evidence_path)}}
    context=host._NetworkBrokerContext(broker,policy_network,'evidence-key','task-only-token',attempt,authority.fields)
    return SimpleNamespace(host=h,record=record,retained=retained,preparation=preparation,owner=owner,
        reference=reference,authority=authority,fields=fields,attempt=attempt,outputs=outputs,broker=context,policy=policy)


@pytest.mark.parametrize('edge',['profile','owner','epoch','generation','operation','channel','capability','declaration','entrypoint',
    'task','attempt','lease','fence','runtime-epoch','claim-operation','claim-executor','aborted'])
def test_selected_action_dispatch_refuses_stale_authenticated_inputs(selected_command,edge):
    import copy
    f=selected_command;h=f.host
    if edge=='profile':f.preparation._request['profile']['profile_digest']='sha256:'+'0'*64
    elif edge=='owner':f.preparation._request['runtime_owner']['birth_id']='other'
    elif edge=='epoch':f.preparation._request['owner_epoch']='other'
    elif edge=='generation':f.reference['generation']=2
    elif edge=='operation':f.preparation.operation_id='other'
    elif edge=='channel':f.preparation.channel_id='other'
    elif edge=='capability':f.record=replace(f.record,capability_digest='sha256:'+'0'*64)
    elif edge=='declaration':
        metadata=copy.deepcopy(f.record.definition.metadata);metadata['execution_dependencies']={'python':['edge-tts==0']}
        f.record=replace(f.record,definition=replace(f.record.definition,metadata=metadata))
    elif edge=='entrypoint':
        command=replace(f.record.definition.command,argv=(sys.executable,'-m','other.action'))
        f.record=replace(f.record,definition=replace(f.record.definition,command=command))
    elif edge=='aborted':f.preparation._aborted=True
    else:
        key={'task':'task_id','attempt':'attempt_id','lease':'lease_id','fence':'fence',
             'runtime-epoch':'runtime_epoch','claim-operation':'operation','claim-executor':'executor_id'}[edge]
        changed={**f.fields,key:2 if isinstance(f.fields[key],int) else 'other'}
        h.client.confirm_claim_authority=lambda **kw:host._AuthenticatedAttempt(tuple(sorted(changed.items())))
    with pytest.raises((host.HostError,RuntimeError,ValueError)):
        h._prepare_selected_action_command(f.record,[sys.executable,'-m','astrid.packs.generation.actions.generate_speech.run','--help'],
            attempt=f.attempt,network_broker=f.broker)


@pytest.mark.parametrize('edge',['endpoint','routes','token','nonce','attempt','claim','redirects','direct-egress'])
def test_selected_action_broker_projection_refuses_substitution(selected_command,edge):
    f=selected_command;context=f.broker
    if edge=='endpoint':context.policy['proxy']='http://127.0.0.1:1'
    elif edge=='routes':context.broker.allowed_routes=('other.invalid:443',)
    elif edge=='token':context.auth_token='foreign'
    elif edge=='nonce':context.broker.expected_nonce='foreign'
    elif edge=='attempt':context.attempt_root=f.attempt.parent
    elif edge=='claim':context.claim_binding=()
    elif edge=='redirects':context.policy['allow_redirects']=True
    else:context.policy['allowed_destinations']=['api.msedgeservices.com:443']
    with pytest.raises(host.HostError):
        f.host._owned_action_broker(context,attempt=f.attempt,record=f.record)


def test_selected_action_readiness_uses_child_selection_without_host_find_spec(selected_command,monkeypatch):
    f=selected_command
    f.host._executable_admission.require=lambda names:()
    monkeypatch.setattr(host.importlib.util,'find_spec',lambda name:(_ for _ in ()).throw(AssertionError('Host find_spec used')))
    record=f.host.preflight(f.record.id)[0]
    assert record.preflight['action_child']['ok'] is True
    assert record.preflight['packages']['ok'] is True


def test_selected_action_real_command_preparation_confines_exact_files_and_broker(selected_command,monkeypatch):
    f=selected_command;captured=[]
    monkeypatch.setattr(host.sys,'platform','darwin')
    monkeypatch.setattr(host.shutil,'which',lambda _: '/usr/bin/sandbox-exec')
    prepare=f.host._prepare_selected_action_command
    def binding(*args,**kwargs):
        command,payload=prepare(*args,**kwargs)
        captured.append(json.loads(payload))
        return command,payload
    monkeypatch.setattr(f.host,'_prepare_selected_action_command',binding)
    class Prepared(Exception):pass
    def spawn(argv,**options):
        assert argv[:2]==['/usr/bin/sandbox-exec','-f']
        policy=Path(argv[2]).read_text()
        assert sum(len(arg.encode()) for arg in argv) < 16384
        proof_root=Path(f.retained['source_root']).parent
        (proof_root/'compiled-sandbox-profile.sb').write_text(policy)
        (proof_root/'compiled-launch-proof.json').write_text(json.dumps({
            'argv':argv,'cwd':options['cwd'],'pass_fds':options['pass_fds'],
            'environment_keys':sorted(options['env']), 'argv_bytes':sum(len(a.encode()) for a in argv),
            'profile_bytes':len(policy.encode()),'profile_sha256':hashlib.sha256(policy.encode()).hexdigest()},indent=2)+'\n')
        assert f'(allow file-read* (subpath "{f.retained["source_root"]}"))' not in policy
        assert f'(allow file-read* (literal "{f.retained["source_root"]}/edge_tts/__init__.py"))' in policy
        assert '(allow network-outbound (remote tcp "127.0.0.1:43210"))' in policy
        assert 'remote tcp "api.msedgeservices.com' not in policy
        assert 'BANODOCO_RUNTIME_CREDENTIAL' not in options['env']
        assert 'ASTRID_NETWORK_BROKER_TOKEN' not in options['env']
        assert options['pass_fds']==()
        assert options['stdin']==subprocess.PIPE
        payload=captured[0]
        assert payload['network_environment']['ASTRID_NETWORK_BROKER_TOKEN']=='task-only-token'
        assert payload['network_environment']['ASTRID_BROKER_PROXY']=='http://127.0.0.1:43210'
        assert payload['context']['task_id']=='task'
        assert payload['context']['channel_id']=='channel'
        assert payload['action']['module']=='astrid.packs.generation.actions.generate_speech.run'
        assert not any(name.startswith('astrid.packs.rendering') for name in payload['mapping'])
        raise Prepared
    monkeypatch.setattr(host,'popen_owned_group',spawn)
    # The action binder/preparation and final confinement are production code;
    # only process creation and retained external authorities are offline seams.
    with pytest.raises(Prepared):
        f.host._run_command_definition(f.record,{'text':'offline','voice':'en-US-ChristopherNeural','rate':'+0%'},
            f.outputs,f.attempt,network_broker=f.broker,allow_runtime_connection=False)
    assert len(captured)==1


def test_selected_action_dispatch_bootstrap_and_speech_output_offline_seams(selected_command,monkeypatch):
    """Actual command/pipe/bootstrap/action with offline external boundaries."""
    f=selected_command
    monkeypatch.setattr(host.sys,'platform','darwin')
    monkeypatch.setattr(host.shutil,'which',lambda _: '/usr/bin/sandbox-exec')
    monkeypatch.setattr(host,'observe_tree',lambda process:None)
    monkeypatch.setattr(host,'_terminate_process_group',lambda process:process.wait())
    program=r'''
import importlib.util,json,os,socket,subprocess,sys,shutil,wave
from pathlib import Path
from types import SimpleNamespace
launcher=sys.argv[1];arguments=sys.argv[2:]
spec=importlib.util.spec_from_file_location('offline_launch',launcher);gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
handshakes=[]
class Handshake:
 def __enter__(self):return self
 def __exit__(self,*args):pass
 def sendall(self,data):
  assert data.decode().startswith('ASTRID-BROKER/1 HELLO ')
  assert data.decode().endswith(' nonce task-only-token\n')
  handshakes.append(data)
 def recv(self,n):return b'ASTRID-BROKER/1 OK\n'
socket.create_connection=lambda address,**kw:Handshake() if address==('127.0.0.1',43210) else (_ for _ in ()).throw(AssertionError('unexpected endpoint'))
shutil.which=lambda name:'/offline/'+name if name in ('ffmpeg','ffprobe') else None
commands=[]
def media_run(argv,**kwargs):
 commands.append(argv)
 if Path(argv[0]).name=='ffmpeg':
  assert argv[1:6]==['-nostdin','-v','error','-y','-i']
  assert argv[-3:-1]==['-acodec','pcm_s16le']
  with wave.open(argv[-1],'wb') as stream:
   stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(8000);stream.writeframes(b'\0'*4000)
  return SimpleNamespace(returncode=0,stdout='',stderr='')
 assert Path(argv[0]).name=='ffprobe'
 return SimpleNamespace(returncode=0,stdout=json.dumps({'format':{'duration':'0.25'},'streams':[{'codec_type':'audio','codec_name':'pcm_s16le','sample_rate':'8000','channels':1}]}),stderr='')
subprocess.run=media_run
original=gate._SourceLoader.exec_module
def loaded(self,module):
 original(self,module)
 if module.__name__=='edge_tts':
  assert len(handshakes)==1
  assert sys.modules['astrid.core.execution.network_policy']._INSTALLED
  assert os.environ['ASTRID_BROKER_PROXY']=='http://127.0.0.1:43210'
  assert 'BANODOCO_RUNTIME_CREDENTIAL' not in os.environ
  class Communicate:
   def __init__(self,text,voice,**kw):
    assert text=='offline' and voice=='en-US-ChristopherNeural'
    assert kw['rate']=='+0%' and kw['proxy']=='http://127.0.0.1:43210'
   async def stream(self):
    yield {'type':'audio','data':b'offline-provider-fixture'}
    yield {'type':'WordBoundary','offset':0,'duration':1000000,'text':'offline'}
  module.Communicate=Communicate
gate._SourceLoader.exec_module=loaded
sys.argv[:]=[launcher,*arguments]
try:gate._main()
except SystemExit as exc:
 assert exc.code==0
assert [Path(c[0]).name for c in commands].count('ffmpeg')==1
assert any(Path(c[0]).name=='ffprobe' for c in commands)
print('OFFLINE_SELECTED_DISPATCH_OK',json.dumps(commands))
'''
    def spawn(argv,**options):
        assert argv[:2]==['/usr/bin/sandbox-exec','-f']
        selected=argv[3:]
        assert selected[:4]==[sys.executable,'-I','-S','-B']
        # Retain the real binding FD and command arguments. These replacements
        # are explicit process/security/provider/native seams, never live proof.
        selected=[*selected[:4],'-c',program,*selected[4:]]
        assert options['pass_fds']==()
        return subprocess.Popen(selected,**options,start_new_session=True)
    monkeypatch.setattr(host,'popen_owned_group',spawn)
    result=f.host._run_command_definition(f.record,{'text':'offline','voice':'en-US-ChristopherNeural','rate':'+0%'},
        f.outputs,f.attempt,network_broker=f.broker,allow_runtime_connection=False)
    assert result.returncode==0
    manifest=json.loads((f.outputs/'manifest.json').read_text())
    provenance=json.loads((f.outputs/'speech-provenance.json').read_text())
    words=json.loads((f.outputs/'speech-words.json').read_text())
    wav=f.outputs/'audio/speech.wav'
    assert manifest['duration_seconds']==provenance['duration_seconds']==words['duration_seconds']==0.25
    assert manifest['audio_sha256']==hashlib.sha256(wav.read_bytes()).hexdigest()
    assert manifest['settings']['voice']=='en-US-ChristopherNeural'
    assert [o['name'] for o in manifest['outputs']]==['speech','speech_manifest','speech_words']
    assert not (f.outputs/'audio/speech.mp3').exists()
    assert not f.host._active_processes
    (Path(f.retained['source_root']).parent/'offline-speech-proof.json').write_text(json.dumps({
        'manifest':manifest,'provenance':provenance,'words':words,'wav_bytes':wav.stat().st_size,
        'wav_sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),'mp3_exists':False,
        'returncode':result.returncode,'live_children_after_test':False,
        'external_boundaries':'socket/provider/media/custody are offline seams'},indent=2)+'\n')


PROBE = '''
import dataclasses, json, sys
from pathlib import Path
@dataclasses.dataclass(slots=True)
class Value:
    number: int = 7
print(json.dumps(dict(origin=dataclasses.__file__, slots=Value.__slots__,
                     value=Value().number, path=sys.path, executable=sys.executable)))
'''


def isolated_paths():
    result = subprocess.run([sys.executable, '-I', '-S', '-B', '-c',
                             'import json,sys; print(json.dumps(sys.path))'],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


@pytest.fixture
def bootstrap(tmp_path, launch, monkeypatch):
    policy, _, _, outside = launch
    purelib = tmp_path / 'legacy-purelib'
    purelib.mkdir()
    # Model the pre-3.10 backport's signature, which rejects slots=True.
    (purelib / 'dataclasses.py').write_text(
        'def dataclass(cls=None, *, frozen=False):\n    return cls\n'
        'def asdict(value):\n    return vars(value)\n'
        'def is_dataclass(value):\n    return False\n')
    dependency = tmp_path / 'dependency'
    dependency.mkdir()
    get_path = host.sysconfig.get_path
    monkeypatch.setattr(host.sysconfig, 'get_path',
                        lambda name: str(purelib) if name == 'purelib' else get_path(name))
    monkeypatch.setattr(host, '_dependency_pythonpath', lambda: (str(dependency),))
    pack = tmp_path / 'pack'
    manifest = _write_manifest(pack)
    definition = json.loads(manifest.read_text())
    # Avoid braces in the command's format-template text.
    code = PROBE + '\nPath(sys.argv[1]).write_text(json.dumps(dict(origin=dataclasses.__file__, slots=Value.__slots__, value=Value().number, path=sys.path, executable=sys.executable)))\n'
    definition['command']['argv'] = ['{python_exec}', '-c', code, '{out}/answer.txt']
    manifest.write_text(json.dumps(definition))
    checkout = Path(host.__file__).resolve().parents[3]
    policy = replace(policy,
        bootstrap_files=(*policy.bootstrap_files,
            Path('/opt/homebrew/opt/libb2/lib/libb2.1.dylib'),
            Path('/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib'),
            Path('/opt/homebrew/opt/openssl@3/lib/libssl.3.dylib')),
        bootstrap_roots=(*policy.bootstrap_roots, checkout, pack, purelib, dependency))
    h = host.GenericPackHost(pack_roots=[pack], confinement_policy=policy)
    h.discover()
    return SimpleNamespace(host=h, record=h.capabilities['test.echo'], policy=policy,
                           purelib=purelib, dependency=dependency, pack=pack,
                           checkout=checkout, outside=outside)


def assert_stdlib(observed):
    assert Path(observed['origin']).resolve() == (
        Path(host.sysconfig.get_path('stdlib')) / 'dataclasses.py').resolve()
    assert observed['slots'] == ['number'] and observed['value'] == 7
    assert Path(observed['executable']).resolve() == Path(sys.executable).resolve()


@pytest.mark.parametrize('entry', ['command', 'executor'])
def test_declared_startup_ignores_legacy_purelib_dataclasses(bootstrap, entry):
    f = bootstrap
    h, policy = f.host, f.policy
    definition, admission = h.admit('executor', 'test.echo')
    if entry == 'command':
        result = h._run_command_definition(f.record, {}, policy.private_write_root,
                                          policy.attempt_root, admission=admission)
        assert result.returncode == 0, result
    else:
        result = h.invoke_capability(capability_kind='executor', capability_id='test.echo',
            request=dict(out=str(policy.private_write_root), inputs={}, project='synthetic',
                         project_was_auto_resolved=True), attempt=policy.attempt_root,
            definition=definition, admission=admission)
        assert result.ok, result
    observed = json.loads((policy.private_write_root / 'answer.txt').read_text())
    assert_stdlib(observed)
    assert not h._active_processes


@pytest.mark.parametrize('entry', ['command', 'worker', 'renderer'])
def test_isolated_bootstrap_exact_path_order(bootstrap, monkeypatch, entry):
    f = bootstrap
    captured = []
    class Captured(Exception):
        pass
    def capture(argv, **kwargs):
        # Still compile/validate the real confinement plan before stopping.
        plan = compile_plan(argv, **kwargs)
        assert '(deny default)' in plan.argv[2]
        assert f'(allow file-read* (subpath "{f.outside.parent}"))' not in plan.argv[2]
        captured.append(list(argv))
        raise Captured
    compile_plan = f.host._workload_launch_plan
    monkeypatch.setattr(f.host, '_workload_launch_plan', capture)
    lease = SimpleNamespace(close=lambda: None)
    monkeypatch.setattr(f.host, '_renderer_task_lease', lambda *a, **kw: lease)
    with pytest.raises(Captured):
        if entry == 'worker':
            f.host.invoke_capability(capability_kind='executor', capability_id='test.echo',
                request={}, attempt=f.policy.attempt_root)
        else:
            record = replace(f.record, definition=replace(f.record.definition,
                id='rendering.timeline_visualize')) if entry == 'renderer' else f.record
            f.host._run_command_definition(record, {}, f.policy.private_write_root,
                                            f.policy.attempt_root)
    argv, = captured
    assert argv[:5] == [sys.executable, '-I', '-S', '-B', '-c']
    imports = [str(f.checkout), str(f.purelib), host.sysconfig.get_path('platlib')]
    if entry == 'command':
        imports += [str(f.pack), str(f.pack.parent)]
    imports += [str(f.dependency)]
    imports = list(dict.fromkeys(str(Path(p).resolve()) if entry == 'command' else p for p in imports))
    assert json.loads(argv[6]) == imports
    # Stop at the worker entry point: exercise the emitted startup verbatim,
    # without launching a renderer or giving the probe a provider protocol.
    if entry != 'command':
        argv[5] = 'import runpy; runpy.run_module=lambda *a, **kw: exec(' + repr(PROBE) + '); ' + argv[5]
    result = subprocess.run(argv, capture_output=True, text=True, check=True)
    observed = json.loads(result.stdout)
    assert_stdlib(observed)
    assert observed['path'] == [*isolated_paths(), *imports]


@pytest.mark.parametrize('corruption', [None, 'changed-hook', 'changed-policy', 'shadow-hook'])
def test_network_bootstrap_keeps_interpreter_paths_first(tmp_path, corruption):
    hook = tmp_path / '.astrid-network-hook/sitecustomize.py'
    hook.parent.mkdir()
    hook.write_text(host._STRICT_NETWORK_HOOK_SOURCE)
    policy = tmp_path / 'policy.py'
    policy.write_text('def install_from_environment(**kwargs):\n    return True\n')
    dependency = tmp_path / 'dependency'
    dependency.mkdir()
    (dependency / 'dataclasses.py').write_text('raise RuntimeError("legacy dataclasses")\n')
    (dependency / 'probe.py').write_text(PROBE)
    argv = host._network_startup_argv(
        [sys.executable, '-m', 'astrid.core.execution.generic_host_worker'], tmp_path,
        {'PYTHONPATH': os.pathsep.join((str(hook.parent), str(dependency)))}, broker_required=False)
    config = json.loads(argv[-1])
    config.update(policy=str(policy), policy_sha256=hashlib.sha256(policy.read_bytes()).hexdigest(), module='probe')
    argv[-1] = json.dumps(config)
    if corruption == 'changed-hook':
        hook.write_text('raise RuntimeError("changed hook")\n')
    elif corruption == 'changed-policy':
        policy.write_text('raise RuntimeError("changed policy")\n')
    elif corruption == 'shadow-hook':
        (tmp_path / 'sitecustomize.py').write_text('raise RuntimeError("shadow hook")\n')
    result = subprocess.run(argv, cwd=tmp_path, capture_output=True, text=True)
    if corruption:
        assert result.returncode == 78 and result.stdout == ''
        assert result.stderr == 'astrid network startup failed\n'
        return
    assert result.returncode == 0, result.stderr
    observed = json.loads(result.stdout)
    assert_stdlib(observed)
    stdlib = isolated_paths()
    assert observed['path'][:len(stdlib) + 3] == [*stdlib, str(tmp_path), str(hook.parent), str(dependency)]
    assert len(observed['path']) == len(set(observed['path']))


def test_render_backend_bootstrap_exact_path_order(bootstrap, monkeypatch):
    from astrid.core.execution import render_command_pipe as relay
    from astrid.core.execution.renderer_transport import QualifiedRendererReads

    f = bootstrap
    owner = relay.HostRenderCommandBridge.__new__(relay.HostRenderCommandBridge)
    owner.policy, owner.environment = f.policy, {}
    owner.closure = object()
    # This fixture stops before a renderer launch and owns only startup/path
    # assertions. Real renderer admission has its separate closure controls.
    def admitted_reads(cls, *, closure, environment, policy):
        assert closure is owner.closure and policy is f.policy
        return None
    monkeypatch.setattr(QualifiedRendererReads, 'admit', classmethod(admitted_reads))
    owner.imports = [str(f.checkout), str(f.purelib),
                     host.sysconfig.get_path('platlib'), str(f.dependency)]
    captured = []
    compile_plan = host._confined_launch_plan
    class Captured(Exception):
        pass
    def capture(argv, **kwargs):
        plan = compile_plan(argv, **kwargs)
        assert '(deny default)' in plan.argv[2]
        captured.append(list(argv))
        raise Captured
    monkeypatch.setattr(host, '_confined_launch_plan', capture)
    with pytest.raises(Captured):
        owner._launch_locked([sys.executable, 'probe.py'],
                             cwd=str(f.policy.private_write_root), _backend=True)
    argv, = captured
    assert argv[:5] == [sys.executable, '-I', '-S', '-B', '-c']
    assert json.loads(argv[6]) == owner.imports
    # Substitute only the private pipe installer and backend entry point;
    # the emitted interpreter/path/environment setup still executes.
    argv[5] = (
        'import runpy,sys,types; '
        'pipe=types.ModuleType("astrid.core.execution.render_command_pipe"); '
        'pipe.install_render_command_client=lambda: None; '
        'sys.modules[pipe.__name__]=pipe; '
        'runpy.run_path=lambda *a, **kw: exec(' + repr(PROBE) + '); ' + argv[5])
    result = subprocess.run(argv, capture_output=True, text=True, check=True)
    observed = json.loads(result.stdout)
    assert_stdlib(observed)
    assert observed['path'] == [*isolated_paths(), *owner.imports]
