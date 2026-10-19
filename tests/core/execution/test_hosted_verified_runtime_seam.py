"""Matched Runtime preparation routes stop after private binding, before spawn."""
import hashlib
import json
import subprocess
import sys
from types import SimpleNamespace

import pytest

from astrid.core.execution import custody_broker as sdk_custody
from astrid.core.execution import generic_host
from astrid.core.execution import hosted_contract as sdk_contract


@pytest.mark.skipif(sys.platform != 'darwin', reason='real retained custody is Darwin only')
@pytest.mark.parametrize('inspection_required', [True, False], ids=['sdk-inspection', 'runtime-fallback'])
@pytest.mark.parametrize('change', ['valid', 'six-item', 'wrong-binding-descriptor'])
def test_actual_runtime_preparation_selects_matched_hosted_contract(tmp_path, monkeypatch, inspection_required, change):
    composition = pytest.importorskip('runtime_protocol.local_worker_composition')
    from runtime_protocol import verified_host_launch as gate
    from runtime_protocol.local_worker import LocalWorkerProfile, _digest, _selected_profile_payload
    from banodoco_local import custody_broker as runtime_custody
    from banodoco_local import hosted_contract as runtime_contract

    def forbidden(*args, **kwargs):
        pytest.fail('private binding seam must not spawn or probe')
    monkeypatch.setattr(subprocess, 'Popen', forbidden)
    monkeypatch.setattr(subprocess, 'run', forbidden)
    source = tmp_path / 'source'
    for relative in ('astrid/__init__.py', 'astrid/version.py', 'astrid/__main__.py',
                     'astrid/runtime_cli.py', 'astrid/omp_agent.py', 'astrid/core/__init__.py',
                     'astrid/core/execution/__init__.py', 'astrid/core/execution/generic_host.py',
                     'astrid/sdk/__init__.py', 'banodoco_workspace_client/__init__.py'):
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('# offline selected source; never imported\n')
    packs = source / 'astrid/packs'; packs.mkdir()
    (packs / 'executor.yaml').write_text(json.dumps({
        'schema_version': 1, 'id': 'test.cpu', 'name': 'CPU', 'kind': 'external', 'version': '1.0',
        'command': {'argv': ['{python_exec}', '-c', 'pass']}, 'outputs': [],
        'isolation': {'mode': 'subprocess', 'network': False,
                      'binaries': ['offline-optional'] if inspection_required else []}}))
    assert generic_host._launch_needs_command_inspection((packs,)) is inspection_required

    interpreter = tmp_path / 'runtime/bin/python'
    interpreter.parent.mkdir(parents=True)
    interpreter.write_bytes(b'OFFLINE NONEXECUTABLE INTERPRETER')
    launcher = tmp_path / 'selected-launcher.py'
    launcher.write_text('# offline selected launcher; never executed\n')
    support = tmp_path / 'support'; support.mkdir(mode=0o700)
    realm = tmp_path / 'realm'; realm.mkdir(mode=0o700)
    boot = support / 'boot.json'; boot.write_text('{}')
    closure = gate.source_checkout_closure(source)
    protocol = {'version': gate.CURRENT_ROLES_VERSION, 'module': gate.HOST_MODULE,
                'source_closure_digest': closure['digest']}
    launch = {'source_checkout': str(source), 'pack_root': str(packs),
              'boot_manifest_path': str(boot), 'boot_manifest_hash': _digest({}),
              'capability_matrix': None, 'environment': {}, 'max_concurrency': 1,
              'selected_actions': {}}
    profile = LocalWorkerProfile('offline', 'workspace', realm, support, 'machine',
        None, interpreter, None, None, '', '', 'sha256:' + hashlib.sha256(interpreter.read_bytes()).hexdigest(),
        '', '', _digest(launch), 'revision', _digest('profile'), _digest('release'),
        host_protocol=protocol, execution_mode='host_only_cpu', host_launch=launch)
    config = {**launch, 'runtime_endpoint': 'http://127.0.0.1:1',
              'runtime_instance_id': 'offline-epoch', 'support_root': str(support),
              'credential_file': str(support / 'unused-credential'), 'ready_file': str(support / 'ready.json')}

    def inventory(root):
        return {'root': str(root), 'files': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                                           for p in root.rglob('*') if p.is_file()}}
    inventories = [inventory(source), inventory(interpreter.parent.parent)]
    pins = {gate.raw_digest(value): value for value in inventories}
    def authority(selected):
        return {'selected_profile_digest': gate.raw_digest(selected), 'profile_digest': profile.profile_digest,
            'release_digest': profile.release_digest, 'host_protocol': protocol, 'source_checkout': str(source),
            'source_components': closure['components'], 'inventories': pins,
            'import_binding': {'schema_version': 1, 'mode': gate.MODE,
                'launcher': {'path': str(launcher), 'sha256': hashlib.sha256(launcher.read_bytes()).hexdigest()},
                'python_runtime_inventory_digest': gate.raw_digest(inventories[1]),
                'import_roots': [{'path': item['root'], 'inventory_digest': gate.raw_digest(item)}
                                 for item in inventories]}}
    # Only installed release/materialization authority is synthetic. The actual
    # verifier, claim builder, static selector, brokers and contracts run below.
    class OfflineVerifier(gate.TrustedLocalHostLaunchVerifier):
        _mode = gate.MODE
        def _observation(self, record, selected):
            return SimpleNamespace(verify=lambda: None)
        def _validate_inventory_selection(self, record, selected, config):
            return None
    verifier = OfflineVerifier(installed_release=authority(_selected_profile_payload(profile)))
    monkeypatch.setattr(composition, '_installed_host_release', lambda *args: None)
    monkeypatch.setattr(gate, 'TrustedLocalHostLaunchVerifier', lambda **kwargs: verifier)

    expected_contract = sdk_contract if inspection_required else runtime_contract
    expected_broker = sdk_custody.RoleBoundCustodyBroker if inspection_required else runtime_custody.RoleBoundCustodyBroker
    observations = []
    original = expected_contract.HostedLaunch.environment
    class BindingReached(Exception):
        pass
    def validate_then_stop(selected, argv, *, launch_binding=None):
        assert type(selected.broker) is expected_broker
        assert type(selected) is expected_contract.HostedLaunch
        assert argv == [str(interpreter), '-I', '-S', '-B', str(launcher), '--binding-fd', str(launch_binding.fileno())]
        observations.append(selected)
        argv = list(argv)
        if change == 'six-item': argv.remove('-B')
        elif change == 'wrong-binding-descriptor': argv[-1] = str(launch_binding.fileno() + 1)
        environment = original(selected, argv, launch_binding=launch_binding)
        assert change == 'valid', 'invalid producer shape passed private binding validation'
        expected_contract.validate(selected.value, role='host', argv=argv)
        assert expected_contract.read_payload(int(environment[expected_contract.FD_KEY]),
            environment[expected_contract.DIGEST_KEY]) == expected_contract.canonical(selected.value)
        changed = list(argv); changed[4] = str(tmp_path / 'unselected-launcher.py')
        with pytest.raises(expected_contract.HostedContractError):
            expected_contract.validate(selected.value, role='host', argv=changed)
        raise BindingReached
    monkeypatch.setattr(expected_contract.HostedLaunch, 'environment', validate_then_stop)
    preparer = composition.CrossProcessWorkerPreparer(profile=profile, config=config, environment={}, timeout_seconds=1)
    expected_error = BindingReached if change == 'valid' else expected_contract.HostedContractError
    with pytest.raises(expected_error):
        preparer.prepare(profile, operation_id='offline-operation', channel_id='offline-channel')
    assert len(observations) == 1 and preparer.current_handle() is None
    assert preparer.cleanup_uncertain is None
    assert observations[0].broker.hosted_launch is observations[0]
