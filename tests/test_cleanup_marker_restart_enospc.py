"""Offline restart fault injection; no Runtime server or native child launch."""
import json
import os
from pathlib import Path
import subprocess
import sys
import pytest


DRIVER = r'''
import errno, hashlib, json, sys, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from dataclasses import replace
import pytest
from runtime_protocol import local_worker as module
from runtime_protocol.auth import CredentialStore
from runtime_protocol.errors import ConflictError
from runtime_protocol.errors import AuthorizationError
from runtime_protocol.daemon import RuntimeDaemon, WORKER_ACTOR
from runtime_protocol.local_worker_composition import _create_host_custody_scope
from runtime_protocol.local_execution_handoff import write_protected
from test_local_worker import host_only_profile_case
from test_local_worker_composition import _host_only_cleanup_case

root = Path(sys.argv[2])
credentials = CredentialStore(root / 'credentials')
profile = replace(host_only_profile_case(), support_root=root, realm_root=root)
marker = root / 'orderly-handoff-cleanup-uncertain.json'
scope = root / 'local-execution-custody' / 'offline-operation'
def generation():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in credentials._paths(WORKER_ACTOR) if p.exists()}
def no_space(path, value):
    assert path == marker
    with pytest.raises(AuthorizationError):
        credentials.load(credentials.path_for(WORKER_ACTOR).read_text())
    raise OSError(errno.ENOSPC, 'injected marker failure')
if sys.argv[1] == 'depart':
    patch = pytest.MonkeyPatch()
    preparer, handle, calls, sent, state = _host_only_cleanup_case(root, patch, 'terminal120')
    preparer.profile = profile
    _create_host_custody_scope(scope)
    # Retained ordinary custody input, never a fabricated cleanup ACK.
    write_protected(scope / 'owner-session-config.json', profile.host_launch)
    launcher = module.LocalWorkerLauncher(credentials=credentials, profiles={'fixture':profile},
        preparer=preparer, inspector=SimpleNamespace(observe=lambda _: (_ for _ in ()).throw(ValueError('offline-primary'))),
        workspace_uuid='workspace', realm_root=root, support_root=root, runtime_pid=77, actor=WORKER_ACTOR, scopes=())
    credentials.provision(WORKER_ACTOR, [], metadata={'local_launch_receipt':{
        'execution_mode':'host_only_cpu', 'profile_id':'fixture', 'operation_id':'offline-operation'}})
    before = generation()
    launcher._active_handle, launcher._active_profile, launcher._active_identity = handle, profile, {}
    launcher._control_alive = lambda _: True
    patch.setattr(module, 'atomic_json_write', no_space)
    if sys.argv[3] == 'liveness_abort_error':
        launcher._abort = lambda _: (_ for _ in ()).throw(OSError('offline abort entry failure'))
    if sys.argv[3].startswith('liveness'):
        assert launcher.check_liveness(handle) is False
    else:
        with pytest.raises(ConflictError, match='cleanup is uncertain'):
            launcher.finish_shutdown(launcher.begin_shutdown())
    failure = launcher._cleanup_refusal_details()
    if sys.argv[3].startswith('liveness'):
        assert failure['initiating_error'] == {'exception_type':'ValueError','code':'error'}
    assert failure['marker_error'] == 'enospc' and failure['marker_persistence'] == 'failed'
    assert not marker.exists() and generation() == before
    def forbidden(*args):
        raise AssertionError('same owner reached successor boundary')
    launcher._profile = forbidden
    try: launcher.start('fixture', 'workspace')
    except ConflictError: pass
    else: raise AssertionError('same owner did not refuse')
    assert not handle.cleanup_acknowledged
    print(json.dumps({'same_owner_refused':True,'marker_absent':True,
        'generation':before,'primary_retained':True,'old_ack_recovered':False}))
else:
    assert scope.is_dir() and (scope / 'owner-session-config.json').is_file()
    assert not marker.exists() and credentials.actor_metadata(WORKER_ACTOR) is not None
    before = generation()
    preparer = SimpleNamespace(control_alive=lambda _:False, current_handle=lambda:None,
        abort=lambda _:None, cleanup_uncertain=None)
    # Actual daemon credential provisioning and launcher ordering, stopping
    # before HTTP/server setup. No database, listener or native process.
    daemon = RuntimeDaemon(root, support_root=root, local_worker_profiles={'fixture':profile},
        local_worker_preparer=preparer, local_worker_inspector=object())
    daemon.service = SimpleNamespace(realm={'id':'workspace'})
    daemon._has_unrevoked_remote_activation = lambda: False
    daemon._provision_credentials()
    credentials = daemon.credentials
    if sys.argv[1] == 'restart':
        module.atomic_json_write = no_space
    launcher = daemon._create_local_worker_launcher()
    if sys.argv[1] == 'persist':
        assert marker.is_file() and json.loads(marker.read_text())['state'] == 'cleanup_uncertain'
        assert credentials.actor_metadata(WORKER_ACTOR) is None
        assert not any(p.exists() for p in credentials._paths(WORKER_ACTOR))
    else:
        assert not marker.exists() and generation() == before
    entered, release = threading.Event(), threading.Event()
    reached = []
    class SuccessorBoundary(Exception): pass
    def boundary(*args):
        reached.append('profile')
        entered.set()
        assert release.wait(3)
        raise SuccessorBoundary()
    launcher._profile = boundary
    def start():
        try: launcher.start('fixture', 'workspace')
        except ConflictError: return 'refused'
        except SuccessorBoundary: return 'reached_successor_boundary'
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(start)
        entered.wait(0.2)
        second = pool.submit(start)
        second_result = second.result(timeout=3)
        release.set()
        first_result = first.result(timeout=3)
    print(json.dumps({'restart_results':[first_result,second_result],
        'successor_boundary_count':len(reached),'old_ack_recovered':False,
        'generation_retained':generation() == before,'generation':generation()}))
'''


@pytest.mark.parametrize('initiator', ['liveness', 'shutdown', 'liveness_abort_error'])
def test_liveness_marker_enospc_process_exit_missing_marker_restart_stays_fenced(tmp_path, initiator):
    """Both restart callers must refuse before profile/preparation, even without marker."""
    root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
           "PYTHONPATH": os.pathsep.join((str(root), str(root / "tests")))}
    def child(mode):
        result = subprocess.run([sys.executable, "-B", "-c", DRIVER, mode, str(tmp_path), initiator],
                                env=env, cwd=root, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout.splitlines()[-1])
    departed = child("depart")
    assert departed['same_owner_refused'] and departed['marker_absent'] and departed['primary_retained']
    assert len(departed['generation']) == 3 and departed['old_ack_recovered'] is False
    for _ in range(2):
        restarted = child("restart")
        assert restarted["old_ack_recovered"] is False
        assert restarted["restart_results"] == ["refused", "refused"], restarted
        assert restarted["successor_boundary_count"] == 0 and restarted['generation_retained']
        assert restarted['generation'] == departed['generation']
    persisted = child('persist')
    assert persisted['restart_results'] == ['refused', 'refused']
    assert persisted['successor_boundary_count'] == 0 and not persisted['generation_retained']


@pytest.mark.parametrize('changed_generation', [False, True])
def test_exact_original_cleanup_still_revokes_host_receipt(tmp_path, monkeypatch, changed_generation):
    from types import SimpleNamespace
    from runtime_protocol.auth import CredentialStore
    from runtime_protocol.daemon import WORKER_ACTOR
    from runtime_protocol.errors import AuthorizationError
    from runtime_protocol.local_worker import LocalWorkerLauncher
    from test_local_worker_composition import _host_only_cleanup_case

    preparer, handle, *_ = _host_only_cleanup_case(tmp_path, monkeypatch, 'ack')
    credentials = CredentialStore(tmp_path / 'credentials')
    primary = ValueError('offline-primary')
    launcher = LocalWorkerLauncher(credentials=credentials, profiles={}, preparer=preparer,
        inspector=SimpleNamespace(observe=lambda _: (_ for _ in ()).throw(primary)),
        workspace_uuid='workspace', realm_root=tmp_path, support_root=tmp_path,
        runtime_pid=77, actor=WORKER_ACTOR, scopes=())
    token, _ = credentials.provision(WORKER_ACTOR, [], metadata={'local_launch_receipt':{
        'execution_mode':'host_only_cpu', 'operation_id':'offline-operation'}})
    launcher._active_handle, launcher._active_profile, launcher._active_identity = handle, preparer.profile, {}
    launcher._control_alive = lambda _: True
    abort = preparer.abort
    def original_cleanup(selected):
        # Bearer is disabled before the first cleanup operation; the existing
        # generation remains the restart fence while cleanup is in flight.
        with pytest.raises(AuthorizationError):
            credentials.load(token)
        assert credentials.actor_metadata(WORKER_ACTOR) is not None
        abort(selected)
        if changed_generation:
            # Even identical metadata can belong to a newer committed bearer.
            metadata = credentials.actor_metadata(WORKER_ACTOR)
            credentials.provision(WORKER_ACTOR, [], metadata={k:v for k,v in metadata.items()
                if k not in {'credential_format','actor','scopes'}}, rotate=True)
    preparer.abort = original_cleanup
    assert launcher.check_liveness(handle) is False
    assert handle.closed and handle.cleanup_acknowledged and handle._cleanup_settlement
    assert handle.cleanup_context['initiating_error'] == {'exception_type':'ValueError','code':'error'}
    assert (credentials.actor_metadata(WORKER_ACTOR) is not None) == changed_generation
    assert any(p.exists() for p in credentials._paths(WORKER_ACTOR)) == changed_generation
    assert launcher._cleanup_uncertain is None
