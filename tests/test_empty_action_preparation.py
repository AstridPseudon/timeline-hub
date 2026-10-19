"""Offline exact verifier -> SDK dispatch regression; no process is started."""
import copy
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from runtime_protocol import local_worker_composition as composition
from runtime_protocol import verified_host_launch as gate
from test_selected_python_inventory import selected_case


def selected_launch(tmp_path, monkeypatch, *, selection):
    f = selected_case(tmp_path, monkeypatch)
    profile = f.args['preparation']['profile']
    launch = dict(source_checkout=str(f.source), pack_root=str(f.source/'astrid/packs'),
                  boot_manifest_path=str(tmp_path/'boot.json'), boot_manifest_hash='sha256:'+'3'*64,
                  capability_matrix=None, environment={}, max_concurrency=1)
    if selection != 'absent':
        launch['selected_actions'] = selection
    profile.update(workspace_uuid='offline-workspace', machine_id='offline-machine',
                   profile_revision='offline-revision', host_launch=launch,
                   session_config_digest='sha256:'+gate.raw_digest(launch))
    f.record = composition._installed_host_release(SimpleNamespace(**profile), f.args['config'])
    f.verifier = gate.TrustedLocalHostLaunchVerifier(installed_release=f.record)
    return f


def claimed_payload(f):
    proof = f.verifier.verify(**f.args)
    _, data = f.verifier.claim(proof, **f.args, binding_fd=3)
    return json.loads(data)


@pytest.mark.parametrize('selection', ['absent', {}])
def test_verified_launch_preserves_explicit_empty_action_selection(tmp_path, monkeypatch, selection):
    f = selected_launch(tmp_path, monkeypatch, selection=selection)
    payload = claimed_payload(f)
    if selection == 'absent':
        assert 'action_launch' not in payload
    else:
        assert payload['action_launch']['actions'] == {}
        assert payload['action_launch']['profile_digest'] == gate.raw_digest(f.args['preparation']['profile'])
        with pytest.raises(gate.HostLaunchError, match='no selected'):
            gate.prepare_action_binding(payload['action_launch'], action_id='unselected.action',
                                       context={}, network_environment={})


@pytest.mark.parametrize('selection', [None, [], {'unselected.action': {}}])
def test_verified_launch_refuses_malformed_action_selection(tmp_path, monkeypatch, selection):
    with pytest.raises(gate.HostLaunchError):
        f = selected_launch(tmp_path, monkeypatch, selection=selection)
        claimed_payload(f)


@pytest.mark.parametrize('edge', ['exact', 'missing', 'wrong-profile', 'foreign-actions'])
def test_empty_action_launch_reaches_real_sdk_host_preparation(tmp_path, monkeypatch, edge):
    source = os.environ.get('HOST_LAUNCH_TEST_ASTRID_SOURCE')
    if not source:
        pytest.skip('select admitted SDK source for exact Host dispatch')
    from astrid.core.execution import generic_host as host
    from astrid.core._shared import boot_manifest
    assert Path(host.__file__).is_relative_to(Path(source))
    f = selected_launch(tmp_path, monkeypatch, selection={})
    profile = f.args['preparation']['profile']
    payload = claimed_payload(f)
    owner = dict(pid=17, uid=0, birth_id='offline-runtime',
                 runtime_instance_id='epoch', coordinator_epoch='epoch')
    request = dict(version=host._LOCAL_PREPARATION_VERSION, command='prepare_local_execution',
                   operation_id='op', channel_id='channel', owner_epoch='epoch', runtime_owner=owner,
                   profile=profile, custody_scope=str(tmp_path/'custody'))
    preparation = host.LocalExecutionPreparation(operation_id='op', channel_id='channel')
    preparation._retained_relay_actor = SimpleNamespace(verify=lambda: dict(owner))
    journals = []
    monkeypatch.setattr(preparation, '_acquire_handoff_journal', lambda scope: journals.append(scope) or True)
    monkeypatch.setattr(host, 'source_checkout_closure_digest', lambda root: profile['host_protocol']['source_closure_digest'])
    monkeypatch.setattr(boot_manifest, 'load_boot_manifest_hash', lambda *args, **kwargs: profile['host_launch']['boot_manifest_hash'])
    monkeypatch.setattr(host, 'process_birth_identity', lambda: 'offline-host')
    retained = copy.deepcopy(payload['action_launch'])
    if edge == 'missing':
        monkeypatch.delattr(host, '_RETAINED_ACTION_LAUNCH', raising=False)
    else:
        if edge == 'wrong-profile':
            retained['profile_digest'] = '0'*64
        elif edge == 'foreign-actions':
            retained['actions'] = {'unselected.action': {}}
        monkeypatch.setattr(host, '_RETAINED_ACTION_LAUNCH', retained, raising=False)
    if edge == 'exact':
        reply = preparation.dispatch(request)
        assert reply['status'] == 'prepared'
        assert reply['execution_mode'] == 'host_only_cpu'
        assert reply['session_config_digest'] == profile['session_config_digest']
        assert set(reply['processes']) == {'host'}
        assert preparation._request == request and len(journals) == 1
    else:
        with pytest.raises(host.HostError, match='selected actions differ from verified launch'):
            preparation.dispatch(request)
        assert preparation.result is None and not journals
