"""Disposable real NativeHostSession -> GenericHost receipt proof, no service/GPU.

Run with the exact assigned Astrid checkout. This uses the real launch verifier,
brokers, trampoline, host preparation, Runtime receipt publisher and activation
consumers. It supplies a measured, disposable dependency mapping, not installed
release or whole-workload acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import sysconfig
import tempfile
import signal
import subprocess
import socket


def run(astrid_source, result):
    sys.path.insert(0, str(astrid_source))
    from astrid.core.execution import generic_host
    from astrid.core._shared.boot_manifest import stamp_boot_manifest, manifest_hash
    from runtime_protocol import verified_host_launch as gate
    from runtime_protocol.local_execution_supervisor import NativeHostSession, host_prepare_request, selected_host_argv, RetainedProcess, send_frame, receive_frame
    from runtime_protocol.local_worker import LocalWorkerLauncher, LocalWorkerProfile, LocalWorkerObservation, _selected_profile_payload, _digest
    from runtime_protocol.local_worker_composition import CrossProcessWorkerPreparer, OSProcessInspector, _owner_machine_id, _PreparedWorker, _actual_executable
    from runtime_protocol.auth import CredentialStore
    from banodoco_local.custody_broker import default_process_identity, AuthenticatedCleanupActor, RoleCustodyAuthority, _read_owner_file
    from banodoco_local import hosted_contract
    evidence = {'phase': 'fixture', 'actual_consumers': [], 'network': False}
    initial_descriptors = hosted_contract.descriptor_set()
    session = None
    with tempfile.TemporaryDirectory(prefix='matched-hosted-') as temporary:
        root = Path(temporary).resolve()
        try:
            support = root/'support'; support.mkdir(mode=0o700)
            realm = root/'realm'; realm.mkdir(mode=0o700)
            scope = support/'custody'; scope.mkdir(mode=0o700)
            # Reuse the current kernel interpreter and link existing dependency
            # bytes. No installation or second environment is created.
            executable = _actual_executable(os.getpid())
            runtime = executable.parent
            imports = root/'imports'; imports.mkdir()
            extensions = root/'extensions'; extensions.mkdir()
            def link_tree(source, target):
                if source.is_dir():
                    target.mkdir(exist_ok=True)
                    for child in source.iterdir():
                        if child.name not in {'__pycache__', 'site-packages', 'lib-dynload'} and child.suffix not in {'.pyc','.pyo'}:
                            link_tree(child, target/child.name)
                elif source.is_file():
                    target.symlink_to(source.resolve())
            stdlib = Path(sysconfig.get_path('stdlib'))
            link_tree(stdlib, imports)
            link_tree(Path(sysconfig.get_config_var('DESTSHARED')), extensions)
            # GenericHost's already imported dependency roots, selected by module
            # origin. No ambient environment data is read or serialized.
            packages = {}
            for name, module in list(sys.modules.items()):
                origin = getattr(module, '__file__', None)
                if not origin or 'site-packages' not in Path(origin).parts: continue
                top = name.split('.')[0]
                if top.startswith('__editable') or top == '_distutils_hack': continue
                spec = importlib.util.find_spec(top)
                if spec and spec.origin:
                    source = Path(spec.origin)
                    packages[top] = source.parent if spec.submodule_search_locations is not None else source
            for name, source in packages.items():
                link_tree(source, imports/(name if source.is_dir() else source.name))
            boot = support/'boot-manifest.json'
            from astrid.core.gateway.dispatch import compose_profile_handoff
            boot_hash = 'sha256:' + compose_profile_handoff(boot, support_root=support)['sha256']
            closure = gate.source_checkout_closure(astrid_source)
            protocol = {'version': gate.CURRENT_ROLES_VERSION, 'module': gate.HOST_MODULE, 'source_closure_digest': closure['digest']}
            launch = {'source_checkout':str(astrid_source), 'pack_root':str(astrid_source/'astrid/packs'),
                'boot_manifest_path':str(boot), 'boot_manifest_hash':boot_hash, 'capability_matrix':None,
                'environment':{}, 'max_concurrency':1}
            pin = 'sha256:' + hashlib.sha256(executable.read_bytes()).hexdigest()
            profile = LocalWorkerProfile('disposable', 'disposable-workspace', realm, support, _owner_machine_id(),
                None, executable, None, None, '', '', pin, '', '', _digest(launch), 'disposable-revision',
                _digest('disposable-profile'), _digest('disposable-release'), host_protocol=protocol,
                execution_mode='host_only_cpu', host_launch=launch)
            selected = _selected_profile_payload(profile)
            owner = default_process_identity(os.getpid()); owner.pop('parent_pid', None)
            owner.update(runtime_instance_id='disposable-epoch', coordinator_epoch='disposable-epoch')
            preparation = host_prepare_request(operation_id='disposable-operation', channel_id='disposable-channel',
                owner_epoch='disposable-epoch', runtime_owner=owner, profile=selected, custody_scope=str(scope))
            config = {'host_python':str(executable), 'source_checkout':str(astrid_source), 'pack_root':launch['pack_root'],
                'runtime_endpoint':'disposable://no-network', 'credential_file':str(support/'credentials/host.token'),
                'support_root':str(support), 'runtime_instance_id':'disposable-epoch', 'ready_file':str(support/'ready.json'),
                'state_file':str(support/'state.json'), 'boot_manifest_path':str(boot), 'boot_manifest_hash':boot_hash,
                'capability_matrix':None, 'readiness_profile_path':None, 'readiness_profile_hash':None}
            inventories = [gate.installed_inventory(path) for path in [astrid_source, runtime, imports, extensions]]
            pins = {gate.raw_digest(value):value for value in inventories}
            record = {'selected_profile_digest':gate.raw_digest(selected), 'profile_digest':profile.profile_digest,
                'release_digest':profile.release_digest, 'host_protocol':protocol, 'source_checkout':str(astrid_source),
                'source_components':closure['components'], 'inventories':pins,
                'import_binding':{'schema_version':1, 'mode':gate.TRUSTED_LOCAL_MODE,
                    'launcher':{'path':str(Path(gate.__file__)), 'sha256':hashlib.sha256(Path(gate.__file__).read_bytes()).hexdigest()},
                    'python_runtime_inventory_digest':gate.raw_digest(inventories[1]),
                    'import_roots':[{'path':v['root'],'inventory_digest':gate.raw_digest(v)} for v in inventories]}}
            verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=record)
            evidence.update(phase='NativeHostSession.create', input_digest=gate.raw_digest(record),
                source_paths={'Runtime':str(Path(gate.__file__).resolve().parents[1]), 'Astrid':str(astrid_source)},
                hosted_contract_digest=hashlib.sha256(Path(hosted_contract.__file__).read_bytes()).hexdigest(),
                dependency_names=sorted(packages), environment_keys=['PATH','PYTHONDONTWRITEBYTECODE','PYTHONPATH'])
            def retain(value):
                nonlocal session
                session = value
            session = NativeHostSession.create(preparation, config, retain=retain, timeout=15, launch_verifier=verifier)
            evidence['actual_consumers'].append('NativeHostSession.create/RoleBoundCustodyBroker/trampoline')
            child_identity = session.retained.verify()
            evidence['pid'] = session.retained.child.pid
            evidence['phase'] = 'GenericHost.prepare'
            prepared = session.exchange(preparation)
            evidence['preparation_reply'] = prepared
            assert prepared == {'version':preparation['version'],'status':'prepared','execution_mode':'host_only_cpu',
                'operation_id':preparation['operation_id'],'channel_id':preparation['channel_id'],
                'owner_epoch':preparation['owner_epoch'],'session_config_digest':profile.session_config_digest,
                'processes':{'host':{'pid':child_identity['pid'],'birth_id':child_identity['birth_id']}}}
            evidence['actual_consumers'].append('GenericHost.LocalExecutionPreparation.prepare_local_execution')
            ref = session.broker.role_authority.reference()
            report = {'version':'runtime.local-worker-preparation/v3','execution_mode':'host_only_cpu',
                'operation_id':preparation['operation_id'],'channel_id':preparation['channel_id'],
                'processes':{'host':{'pid':child_identity['pid'],'birth_id':child_identity['birth_id']}},
                'session_config_digest':profile.session_config_digest,'owner_epoch':preparation['owner_epoch'],
                'custody_scope':str(scope),'custody_capabilities':{'host':ref},'profile_binding_digest':_digest(selected)}
            handle = _PreparedWorker(session.retained.child, child_identity['birth_id'], session.control, report,
                support/'config.json', retained=session.retained, broker=session.broker, host_only=True,
                activation=session.activation, preparation=preparation, owner_epoch=preparation['owner_epoch'], custody_scope=str(scope))
            class ObservedNativeSession:
                # These facts are measured from the real child. This fixture
                # selects a source mapping instead of claiming installed RECORD
                # admission; no broker or consumer method is replaced.
                def observe(self, handle):
                    session._verify_launch_host()
                    RoleCustodyAuthority(scope,'host').verify_reference(ref,
                        expected_actor=AuthenticatedCleanupActor.current().verify(), owner_epoch=preparation['owner_epoch'])
                    host = OSProcessInspector(profile)._identity(handle.worker.pid, handle.birth_id,
                        executable, pin, parent_pid=os.getpid(), session_owner=True)
                    return LocalWorkerObservation(profile.machine_id, os.getuid(), profile.workspace_uuid,
                        realm,support,None,host,None,None,0,'',profile.session_config_digest,
                        preparation['owner_epoch'],str(scope),{'host':ref})
            preparer = CrossProcessWorkerPreparer(profile=profile, config=config, environment={})
            credentials = CredentialStore(support/'credentials')
            launcher = LocalWorkerLauncher(credentials=credentials, profiles={profile.profile_id:profile},
                preparer=preparer, inspector=ObservedNativeSession(), workspace_uuid=profile.workspace_uuid,
                realm_root=realm,support_root=support,runtime_pid=os.getpid(),actor='host',scopes=('worker',))
            launcher._preparing_handle = handle
            identity = launcher._validate_observation(profile,launcher.inspector.observe(handle),report=report,
                operation_id=preparation['operation_id'],channel_id=preparation['channel_id'])
            receipt = {**identity,'executor_incarnation':'disposable-executor'}
            _, credential_path = credentials.provision('host',['worker'],metadata={'local_launch_receipt':receipt},enabled=False)
            grant = {'version':'runtime.local-worker-activation/v1','operation_id':preparation['operation_id'],
                'channel_id':preparation['channel_id'],'credential_file':str(credential_path),
                'executor_incarnation':receipt['executor_incarnation'],'evidence_digest':identity['evidence_digest'],
                'acceptance_mode':'runtime-owner-receipt/v1','activation_id':'disposable-activation'}
            accept = launcher._activation_acceptor(handle=handle,profile=profile,report=report,identity=identity,
                receipt=receipt,grant=grant,credential_path=credential_path)
            evidence['phase'] = 'receipt -> half-close -> final ACK'
            request = session.begin_activation(grant)
            recorded = accept(request)
            stored = json.loads(_read_owner_file(scope/'activation-record.json')[0])
            assert stored['receipt'] == recorded and stored['state'] == 'recorded'
            # Observe EOF on the same kernel endpoint after the real consumer
            # has read the ACK and closed its own handle. No exchange is mocked.
            eof_observer = socket.socket(fileno=os.dup(session.activation.fileno()))
            try:
                eof_observer.settimeout(5)
                ack = session.finish_activation(recorded)
                assert eof_observer.recv(1) == b''
                evidence['final_eof_observed'] = True
            finally:
                eof_observer.close()
            assert ack == session.activation_accepted and session.activation.fileno() == -1
            evidence.update(receipt_stored_before_ack=True, receipt_digest=_digest(stored), final_ack=ack,
                activation_closed=True, phase='owned cancellation')
            evidence['actual_consumers'] += ['LocalWorkerLauncher._activation_acceptor','NativeHostSession.begin_activation/finish_activation','GenericHost._await_worker_activation']
            # The private credential stays disabled. Stop this admitted host
            # before workload/registration acceptance; no service is started.
            abort = {'version':preparation['version'],'command':'abort_local_execution',
                **{k:preparation[k] for k in ('operation_id','channel_id','owner_epoch')},
                'profile_digest':profile.profile_digest,'profile_binding_digest':_digest(selected),
                'custody_scope':str(scope),'custody_capabilities':{'host':ref}}
            reply = session.exchange(abort)
            assert reply['status'] == 'cleaned'
            exit_code = session.reap_host()
            evidence.update(phase='complete', exit_code=exit_code, owned_cleanup=True,
                broker_socket_absent=not session.broker.socket_path.exists(), process_absent=default_process_identity(evidence['pid']) is None)
            assert evidence['process_absent'] and evidence['broker_socket_absent']
            session = None
            evidence['phase'] = 'Astrid broker owned cancellation'
            from astrid.core.execution import custody_broker as astrid_custody
            cancel_scope = support/'cancel-custody'; cancel_scope.mkdir(mode=0o700)
            cancel_preparation = {**preparation, 'operation_id':'disposable-cancel', 'custody_scope':str(cancel_scope)}
            broker = astrid_custody.RoleBoundCustodyBroker(role='host', identity_provider=astrid_custody.default_process_identity,
                ledger_root=cancel_scope/'host-admission', authority_scope_root=cancel_scope,
                authority_journal=cancel_scope/'admissions.jsonl', owner_epoch=preparation['owner_epoch'], timeout=15)
            endpoints = broker.create_hosted_launch(cancel_preparation)
            binding = hosted_contract.readonly_payload(b'pending')
            retained = None
            try:
                argv = selected_host_argv(config,cancel_preparation,
                    activation_fd=endpoints.children['activation'].fileno(),host_control_fd=endpoints.children['control'].fileno(),timeout=15)
                environment = {'PATH':os.defpath,'ASTRID_OUTPUT_ROOT':str(support/'host-output'),'BANODOCO_LOCAL_DATA_ROOT':str(realm)}
                selection = verifier.verify(preparation=cancel_preparation,config=config,host_argv=argv,environment=environment)
                mapped,payload = verifier.claim(selection,preparation=cancel_preparation,config=config,host_argv=argv,
                    environment=environment,binding_fd=binding.fileno())
                replacement = hosted_contract.readonly_payload(payload)
                os.dup2(replacement.fileno(),binding.fileno(),inheritable=False); replacement.close()
                environment.update(endpoints.environment(mapped,launch_binding=binding))
                environment.update(broker.child_environment(mapped,start_new_session=True))
                child = subprocess.Popen(astrid_custody.custody_wrapper_argv(str(executable)),env=environment,
                    stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                    close_fds=True,pass_fds=endpoints.pass_fds)
                retained = RetainedProcess(child)
                endpoints.close_children();binding.close()
                broker.wait_until_sealed()
                broker.release_suspended_launch(expected_pid=child.pid)
                assert broker.bind_resumed_token(expected_pid=child.pid)
                retained.bind_actor()
                verifier.bind_child(selection,child=child,identity=retained.verify())
                control=endpoints.parents['control'];control.settimeout(15)
                send_frame(control,cancel_preparation); reply=receive_frame(control)
                assert reply['status']=='prepared'
                try: broker.signal(signal.SIGTERM,expected_pid=child.pid+1)
                except astrid_custody.CustodyError: pass
                else: raise AssertionError('wrong process identity reached cancellation')
                broker.custody_generation+=1
                try:
                    try: broker.signal(signal.SIGTERM,expected_pid=child.pid)
                    except astrid_custody.CustodyError: pass
                    else: raise AssertionError('wrong generation reached cancellation')
                finally: broker.custody_generation-=1
                assert retained.verify()['pid']==child.pid
                broker.signal(signal.SIGTERM,expected_pid=child.pid)
                cancel_code=retained.wait(5)
                evidence.update(phase='complete',cancel_pid=child.pid,cancel_exit_code=cancel_code,
                    wrong_pid_cancel_rejected=True,wrong_generation_cancel_rejected=True,
                    cancel_process_absent=astrid_custody.default_process_identity(child.pid) is None,
                    cancel_broker_socket_absent=not broker.socket_path.exists())
                assert evidence['cancel_process_absent'] and evidence['cancel_broker_socket_absent']
                evidence['actual_consumers'].append('Astrid.RoleBoundCustodyBroker/trampoline/GenericHost/native owned SIGTERM')
            finally:
                if retained is not None and retained.poll() is None:
                    broker.signal(signal.SIGKILL,expected_pid=retained.child.pid)
                    retained.wait(5)
                endpoints.close();binding.close()
            evidence['parent_descriptors_restored'] = hosted_contract.descriptor_set() == initial_descriptors
            assert evidence['parent_descriptors_restored']
        except BaseException as error:
            evidence.update(error_type=type(error).__name__, error=str(error)[:500])
            raise
        finally:
            if session is not None and getattr(session,'retained',None) is not None:
                try:
                    evidence['cleanup_exit_code'] = session.reap_host()
                    evidence['cleanup_process_absent'] = default_process_identity(session.retained.child.pid) is None
                except BaseException as error:
                    evidence['cleanup_error'] = type(error).__name__ + ': ' + str(error)[:300]
            result.write_text(json.dumps(evidence,sort_keys=True,indent=2)+'\n')
    evidence['temporary_inputs_removed'] = not root.exists()
    result.write_text(json.dumps(evidence,sort_keys=True,indent=2)+'\n')
    return evidence


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--astrid-source',type=Path,required=True)
    parser.add_argument('--result',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.astrid_source.resolve(),args.result.resolve()),sort_keys=True))
