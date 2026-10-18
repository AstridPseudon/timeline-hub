"""Reserved new profile tests: fake selections only; no native authority."""
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
import pytest
from runtime_protocol.errors import ValidationError
from runtime_protocol.local_worker import LocalWorkerProfile, LocalWorkerLauncher, _selected_profile_payload
from runtime_protocol.local_execution_supervisor import CURRENT_ROLES_VERSION, digest, RelayError
from test_local_execution_supervisor import _prepare_case


def profile_case():
    selected=_prepare_case()[0]['profile']
    paths={'realm_root','support_root','worker_executable','host_executable','engine_executable','engine_listener_executable'}
    return LocalWorkerProfile(**{k:Path(v) if k in paths else v for k,v in selected.items()})


def declaration():
    return {'version':CURRENT_ROLES_VERSION,'module':'astrid.core.execution.generic_host','source_closure_digest':'a'*64}


def test_profile_absence_preserves_historical_projection_exactly():
    profile=profile_case()
    assert _selected_profile_payload(profile)==_prepare_case()[0]['profile']
    assert 'host_protocol' not in _selected_profile_payload(profile)


def test_profile_protocol_survives_projection_and_changes_existing_binding_digest():
    profile=profile_case();base=_selected_profile_payload(profile)
    selected=replace(profile,host_protocol=declaration())
    payload=_selected_profile_payload(selected)
    assert payload['host_protocol']==declaration() and digest(payload)!=digest(base)
    changed=replace(profile,host_protocol={**declaration(),'source_closure_digest':'b'*64})
    assert digest(_selected_profile_payload(changed))!=digest(payload)
    # Canonical projection owns a copy; caller mutation cannot edit a prior binding.
    payload['host_protocol']['source_closure_digest']='c'*64
    assert selected.host_protocol==declaration()


def test_legacy_profile_cannot_bypass_protocol_validation():
    profile=replace(profile_case(),engine_launch=None,host_protocol=declaration())
    launcher=SimpleNamespace(profiles={profile.profile_id:profile},workspace_uuid=profile.workspace_uuid,
        realm_root=profile.realm_root,support_root=profile.support_root)
    with pytest.raises(ValidationError,match='requires.*engine_launch'):
        LocalWorkerLauncher._profile(launcher,profile.profile_id,profile.workspace_uuid)


@pytest.mark.parametrize('change',[{'version':'unsupported'},{'module':'shadow'},{'source_closure_digest':'sha256:'+'a'*64},{'extra':True}])
def test_profile_validator_does_not_omit_or_accept_malformed_protocol(change):
    profile=replace(profile_case(),host_protocol={**declaration(),**change})
    with pytest.raises(RelayError):_selected_profile_payload(profile)


def host_only_profile_case():
    from runtime_protocol.local_worker import _digest
    profile = profile_case()
    launch = {"source_checkout": "/installed", "pack_root": "/installed/astrid/packs", "boot_manifest_path": "/support/boot.json",
        "boot_manifest_hash": "sha256:" + "b" * 64, "capability_matrix": None, "environment": {}, "max_concurrency": 4}
    return replace(profile, worker_executable=None, worker_artifact_digest="", engine_executable=None,
        engine_listener_executable=None, engine_endpoint="", engine_artifact_digest="", engine_listener_artifact_digest="",
        engine_launch=None, execution_mode="host_only_cpu", host_launch=launch, host_protocol=declaration(),
        session_config_digest=_digest(launch))


def test_host_only_explicit_profile_has_no_invented_roles_and_is_secure():
    from runtime_protocol.local_worker import _secure_profile
    profile = host_only_profile_case()
    payload = _selected_profile_payload(profile)
    assert _secure_profile(profile) and payload['execution_mode'] == 'host_only_cpu'
    assert not set(payload) & {'worker_executable', 'engine_launch', 'engine_executable', 'engine_listener_executable', 'engine_endpoint'}
    launcher = SimpleNamespace(profiles={profile.profile_id:profile}, workspace_uuid=profile.workspace_uuid,
        realm_root=profile.realm_root, support_root=profile.support_root)
    assert LocalWorkerLauncher._profile(launcher, profile.profile_id, profile.workspace_uuid) is profile


@pytest.mark.parametrize('change', [{'engine_launch': {}}, {'engine_executable': Path('/fake')}, {'worker_executable':Path('/fake')}, {'execution_mode':'unknown'}])
def test_host_only_rejects_undeclared_roles_or_mode(change):
    profile = replace(host_only_profile_case(), **change)
    launcher = SimpleNamespace(profiles={profile.profile_id:profile}, workspace_uuid=profile.workspace_uuid,
        realm_root=profile.realm_root, support_root=profile.support_root)
    with pytest.raises(ValidationError):
        LocalWorkerLauncher._profile(launcher, profile.profile_id, profile.workspace_uuid)


@pytest.mark.parametrize("reporter_fails,cleanup_fails", [(False, False), (True, False), (False, True), (True, True)])
def test_start_diagnostics_and_cleanup_never_replace_first_error(monkeypatch, reporter_fails, cleanup_fails):
    import threading
    from runtime_protocol import local_worker as module
    primary = RuntimeError("private-primary-value")
    events = []
    launcher = LocalWorkerLauncher.__new__(LocalWorkerLauncher)
    launcher._operation_lock = threading.Lock()
    launcher._state_lock = threading.RLock()
    launcher._shutdown = threading.Event()
    launcher._watch_stop = threading.Event()
    launcher._startup_receipt_rejection = launcher._cleanup_uncertain = None
    launcher._preparing_handle = launcher._active_handle = None
    launcher.preparer = SimpleNamespace()
    launcher._profile = lambda *_: (_ for _ in ()).throw(primary)
    def report(error, **kwargs):
        assert error is primary
        events.append("reported")
        if reporter_fails:
            raise OSError("private-reporter-value")
    def cleanup(handle):
        events.append("cleanup")
        if cleanup_fails:
            raise TimeoutError("private-cleanup-value")
    monkeypatch.setattr(module, "_report_start_failure", report)
    launcher._abort = cleanup
    with pytest.raises(RuntimeError) as caught:
        launcher.start("fixture", "workspace")
    assert caught.value is primary and events == ["reported", "cleanup"]
    assert launcher._active_handle is None and not launcher._operation_lock.locked()


@pytest.mark.parametrize("fault", ["control", "observation"])
@pytest.mark.parametrize("reporter_fails", [False, True])
def test_liveness_failure_reports_before_fencing_without_weakening_guard(monkeypatch, capsys, fault, reporter_fails):
    import json
    import threading
    from runtime_protocol import local_worker as module
    launcher = LocalWorkerLauncher.__new__(LocalWorkerLauncher)
    launcher._state_lock = threading.RLock()
    handle = SimpleNamespace(preparation={"operation_id": "a" * 32})
    launcher._active_handle = handle
    launcher._active_profile = object()
    launcher._active_identity = {}
    primary = ValueError("private-liveness-value")
    launcher._control_alive = lambda _: fault != "control"
    launcher.inspector = SimpleNamespace(observe=lambda _: (_ for _ in ()).throw(primary))
    observed = []
    def fence(selected, *, abort):
        assert selected is handle and abort is True
        assert handle.cleanup_context["phase"] == "liveness"
        assert handle.cleanup_context["initiating_error"]["exception_type"] == (
            "ConflictError" if fault == "control" else "ValueError")
        observed.append(capsys.readouterr().err)
        return True
    launcher._fence_generation = fence
    if reporter_fails:
        monkeypatch.setattr(module, "_report_start_failure", lambda *_a, **_k: (_ for _ in ()).throw(OSError("private-sink-value")))
    assert launcher.check_liveness(handle) is False
    assert len(observed) == 1
    if not reporter_fails:
        row = json.loads(observed[0])
        assert row["phase"] == "liveness" and row["operation_id"] == "a" * 32
        assert row["exception_type"] == ("ConflictError" if fault == "control" else "ValueError")
        assert "private-liveness-value" not in observed[0]


@pytest.mark.parametrize("initiator", ["watcher", "start"])
@pytest.mark.parametrize("marker_error", [None, "os_error", "enospc", "after_write"])
@pytest.mark.parametrize("logger_fails", [False, True])
def test_cleanup_watcher_abort_start_retains_terminal_refusal(tmp_path, monkeypatch, initiator, marker_error, logger_fails):
    import errno
    import json
    import weakref
    from runtime_protocol import local_worker as module, local_worker_composition as composition
    from runtime_protocol.errors import ConflictError
    from test_local_worker_composition import _host_only_cleanup_case
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, "terminal120")
    handle.preparation["operation_id"] = "a" * 32
    handle.inspection_owner = SimpleNamespace(finish=lambda **kw: calls.append("inspection"))
    credentials = SimpleNamespace(actor_metadata=lambda _: None, disable_actor=lambda _: calls.append("disable"),
        revoke=lambda _: calls.append("revoke"))
    primary = ValueError("private-initiator-value")
    phase = "liveness" if initiator == "watcher" else "observation"
    launcher = LocalWorkerLauncher(credentials=credentials, profiles={}, preparer=preparer,
        inspector=SimpleNamespace(observe=lambda _: (_ for _ in ()).throw(primary)),
        workspace_uuid="workspace", realm_root=tmp_path, support_root=tmp_path, runtime_pid=77, actor="worker", scopes=())
    launcher._active_handle = handle
    launcher._active_profile = preparer.profile
    launcher._active_identity = {}
    launcher._control_alive = lambda _: True
    thread_errors = []
    monkeypatch.setattr(module.threading, "excepthook", thread_errors.append)
    def log(*args):
        assert handle.cleanup_context == {"phase": phase, "operation_id": "a" * 32,
            "initiating_error": {"exception_type": "ValueError", "code": "error"}}
        assert handle.cleanup_outcome["original_host_wait"] == 120
        if logger_fails: raise OSError("private-logger-value")
    monkeypatch.setattr(composition._LOGGER, "warning", log)
    original_write = module.atomic_json_write
    def write(path, value):
        assert launcher._cleanup_uncertain is not None
        assert value["diagnostic"]["reason"] == "child_cleanup_acknowledgement_unresolved"
        assert value["diagnostic"]["outcome"]["logging_status"] == ("failed" if logger_fails else "written")
        if marker_error == "after_write":
            original_write(path, value)
            raise OSError(errno.EIO, "private-post-write-value")
        if marker_error:
            raise OSError(errno.ENOSPC if marker_error == "enospc" else errno.EIO, "private-marker-value")
        original_write(path, value)
    monkeypatch.setattr(module, "atomic_json_write", write)
    if initiator == "watcher":
        waits = iter([False, True])
        launcher._watch_liveness(weakref.ref(launcher), SimpleNamespace(wait=lambda _: next(waits)), handle)
        assert launcher._active_handle is None and launcher._watch_stop.is_set()
        assert calls.index("disable") < calls.index("poll")
    else:
        launcher._active_handle = launcher._active_profile = launcher._active_identity = None
        launcher._profile = lambda *_: preparer.profile
        preparer.prepare = lambda *a, **kw: handle
        preparer.report = lambda _: (_ for _ in ()).throw(primary)
        # Bind the deterministic operation id used by this original owner.
        monkeypatch.setattr(module.uuid, "uuid4", lambda: SimpleNamespace(hex="a" * 32))
        with pytest.raises(ValueError) as caught:
            launcher.start("fixture", "workspace")
        assert caught.value is primary
        assert launcher._active_handle is None
    before = list(calls)
    launcher._abort(handle)
    assert calls == before and launcher._cleanup_handles == [handle]
    launcher._profile = lambda *_: pytest.fail("fenced start reached profile/preparation")
    with pytest.raises(ConflictError, match="graph cleanup is uncertain") as caught:
        launcher.start("fixture", "workspace")
    details = caught.value.details
    assert details["reason"] == "child_cleanup_acknowledgement_unresolved"
    assert details["phase"] == phase and details["operation_id"] == "a" * 32
    assert details["initiating_error"] == {"exception_type": "ValueError", "code": "error"}
    assert details["outcome"]["original_host_wait"] == 120
    assert details["outcome"]["child_cleanup_acknowledged"] is False
    assert details["outcome"]["inspection_owner_settled"] is True
    assert details["outcome"]["complete_graph"] is False
    assert details["marker_persistence"] == ("failed" if marker_error else "written")
    assert details["marker_error"] == ("os_error" if marker_error == "after_write" else marker_error)
    marker = tmp_path / "orderly-handoff-cleanup-uncertain.json"
    # A write may publish bytes before a subsequent durability failure. Its
    # existence does not turn that failed persistence attempt into success.
    assert marker.exists() == (marker_error in {None, "after_write"})
    if marker.exists():
        assert json.loads(marker.read_text())["diagnostic"]["outcome"] == details["outcome"]
    assert "private-" not in json.dumps(details)
    assert not thread_errors


@pytest.mark.parametrize("late_failure", [False, True])
def test_cleanup_deadline_late_completion_reconciles_only_original_success(tmp_path, monkeypatch, late_failure):
    import json
    import threading
    from runtime_protocol.errors import ConflictError
    from test_local_worker_composition import _host_only_cleanup_case
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, "terminal120" if late_failure else "ack")
    entered, release, finished = threading.Event(), threading.Event(), threading.Event()
    threads = []
    original_abort = preparer.abort
    def delayed(selected):
        threads.append(threading.current_thread())
        entered.set()
        assert release.wait(3)
        try: original_abort(selected)
        finally: finished.set()
    preparer.abort = delayed
    credentials = SimpleNamespace(actor_metadata=lambda _: None)
    launcher = LocalWorkerLauncher(credentials=credentials, profiles={}, preparer=preparer, inspector=None,
        workspace_uuid="workspace", realm_root=tmp_path, support_root=tmp_path, runtime_pid=77, actor="worker", scopes=())
    handle.cleanup_context = {"phase": "liveness", "operation_id": "a" * 32,
        "initiating_error": {"exception_type": "ValueError", "code": "error"}}
    try:
        launcher._abort(handle, timeout=0)
        assert entered.wait(1)
        launcher._abort(handle, timeout=0)
        assert launcher._cleanup_handles == [handle]
        with pytest.raises(ConflictError, match="cleanup is uncertain"):
            launcher.start("fixture", "workspace")
    finally:
        release.set()
    assert finished.wait(3)
    # Join the actual cleanup thread so its latch has finished after the adapter.
    for thread in threads:
        thread.join(3)
        assert not thread.is_alive()
    if late_failure:
        with pytest.raises(ConflictError) as caught:
            launcher.start("fixture", "workspace")
        assert caught.value.details["reason"] == "cleanup_deadline_exceeded"
        assert caught.value.details["outcome"]["complete_graph"] is False
        assert launcher._cleanup_uncertain == "cleanup_deadline_exceeded"
    else:
        _assert_offline_successor_admitted(launcher, preparer, tmp_path)
        marker = json.loads((tmp_path / "orderly-handoff-cleanup-uncertain.json").read_text())
        assert marker["diagnostic"]["phase"] == "liveness"
        assert marker["diagnostic"]["initiating_error"] == handle.cleanup_context["initiating_error"]
        restarted = LocalWorkerLauncher(credentials=credentials, profiles={"fixture": preparer.profile},
            preparer=preparer, inspector=None, workspace_uuid="workspace", realm_root=tmp_path,
            support_root=tmp_path, runtime_pid=77, actor="worker", scopes=())
        with pytest.raises(ConflictError, match="cleanup is uncertain"):
            # Even a durable settled JSON record cannot reconstruct an owner.
            restarted.start("fixture", "workspace")
    assert handle.closed == (not late_failure)


def _assert_offline_successor_admitted(launcher, preparer, tmp_path):
    """Exercise start through its next prepare boundary, without a native start."""
    import json
    primary = ValueError("offline successor preparation boundary")
    prepared = []
    launcher._profile = lambda *_: preparer.profile
    def prepare(*args, **kwargs):
        marker = json.loads((tmp_path / "orderly-handoff-cleanup-uncertain.json").read_text())
        assert marker["state"] == "cleanup_settled"
        assert marker["reason"] == "cleanup_deadline_exceeded"
        assert marker["diagnostic"]["outcome"]["owner_settled"] is True
        assert marker["diagnostic"]["settlement"] == "original_adapter_completed"
        assert launcher._cleanup_uncertain is None
        prepared.append(kwargs["operation_id"])
        raise primary
    preparer.prepare = prepare
    with pytest.raises(ValueError) as caught:
        launcher.start("fixture", "workspace")
    assert caught.value is primary and len(prepared) == 1
    assert not launcher._operation_lock.locked()


@pytest.mark.parametrize("fault", [
    "none", "kill", "ack_false", "missing_wait", "inspection", "channel_close",
    "adapter_failure", "forged_outcome", "wrong_handle", "foreign_preparer",
    "owner_epoch", "operation_id", "channel_id", "retained_waiter", "inspection_owner",
    "restarted_owner_epoch", "generation", "generation_after_fence", "active_handle",
    "preparing_handle", "other_obligation", "preparer_obligation", "preparer_uncertain",
    "wait_lost_after_completion", "ack_lost_after_completion", "closed_lost_after_completion",
    "marker_deadline", "marker_settlement", "marker_after_write", "restarted_launcher",
])
def test_late_cleanup_settlement_requires_all_original_owner_obligations(tmp_path, monkeypatch, fault):
    import errno
    import json
    import threading
    from runtime_protocol import local_worker as module
    from runtime_protocol.errors import ConflictError
    from test_local_worker_composition import _host_only_cleanup_case
    case = {"ack_false": "terminal120", "missing_wait": "missing_wait", "kill": "kill"}.get(fault, "ack")
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, case)
    entered, release = threading.Event(), threading.Event()
    handle.inspection_owner = SimpleNamespace(finish=lambda **kw: calls.append("inspection"))
    if fault == "inspection":
        handle.inspection_owner.finish = lambda **kw: (_ for _ in ()).throw(OSError("private-inspection"))
    if fault == "channel_close":
        handle.control.close = lambda: (_ for _ in ()).throw(OSError("private-close"))
    original_abort = preparer.abort
    def delayed(selected):
        entered.set()
        assert release.wait(3)
        if fault == "forged_outcome":
            # Diagnostic booleans and a normal adapter return cannot substitute
            # for the original adapter's private terminal settlement record.
            selected.cleanup_acknowledged = selected.closed = True
            selected.original_host_wait = 0
            selected.cleanup_outcome = {"owner_settled": True, "complete_graph": True,
                "child_cleanup_acknowledged": True, "inspection_owner_settled": True,
                "original_host_wait": 0, "reason": "cleanup_complete"}
            preparer._active = None
            return
        original_abort(selected)
        if fault == "adapter_failure":
            raise OSError("private-adapter-failure-after-close")
    preparer.abort = delayed
    credentials = SimpleNamespace(actor_metadata=lambda _: None)
    launcher = LocalWorkerLauncher(credentials=credentials, profiles={}, preparer=preparer, inspector=None,
        workspace_uuid="workspace", realm_root=tmp_path, support_root=tmp_path,
        runtime_pid=77, actor="worker", scopes=())
    real_write = module.atomic_json_write
    writes = []
    def write(path, value):
        writes.append(value["state"])
        fail = (fault == "marker_deadline" and value["state"] == "cleanup_uncertain" or
                fault in {"marker_settlement", "marker_after_write"} and value["state"] == "cleanup_settled")
        if fail:
            if fault == "marker_after_write":
                real_write(path, value)
            raise OSError(errno.ENOSPC, "private-write")
        real_write(path, value)
    monkeypatch.setattr(module, "atomic_json_write", write)
    if fault == "wrong_handle":
        preparer._active = object()
    launcher._abort(handle, timeout=0)
    thread = launcher._cleanup_attempts[0].thread
    try:
        assert entered.wait(1)
        with pytest.raises(ConflictError, match="cleanup is uncertain"):
            launcher.start("fixture", "workspace")
        if fault == "generation":
            launcher._install_active(object(), preparer.profile, {}, {})
        if fault == "generation_after_fence":
            # Even a replacement that has already been fenced is a successor.
            replacement = object()
            launcher._install_active(replacement, preparer.profile, {}, {})
            launcher._revoke_actor = lambda: None
            assert launcher._fence_generation(replacement, abort=False)
    finally:
        release.set()
        thread.join(3)
        assert not thread.is_alive()
    if fault == "foreign_preparer":
        from runtime_protocol.local_worker_composition import CrossProcessWorkerPreparer
        launcher.preparer = CrossProcessWorkerPreparer(profile=preparer.profile, config={}, environment={})
    if fault in {"owner_epoch", "operation_id", "channel_id"}:
        handle.preparation[fault] = "changed"
    if fault == "retained_waiter": handle.retained = object()
    if fault == "inspection_owner": handle.inspection_owner = object()
    if fault == "restarted_owner_epoch": preparer.config["runtime_instance_id"] = "new-owner"
    if fault == "active_handle": launcher._active_handle = object()
    if fault == "preparing_handle": launcher._preparing_handle = object()
    if fault == "other_obligation": launcher._cleanup_handles.append(object())
    if fault == "preparer_obligation": preparer._active = object()
    if fault == "preparer_uncertain": preparer.cleanup_uncertain = "other obligation"
    if fault == "wait_lost_after_completion": handle.original_host_wait = None
    if fault == "ack_lost_after_completion": handle.cleanup_acknowledged = False
    if fault == "closed_lost_after_completion": handle.closed = False
    if fault == "restarted_launcher":
        launcher = LocalWorkerLauncher(credentials=credentials, profiles={"fixture": preparer.profile},
            preparer=preparer, inspector=None, workspace_uuid="workspace", realm_root=tmp_path,
            support_root=tmp_path, runtime_pid=77, actor="worker", scopes=())
    if fault in {"none", "kill"}:
        _assert_offline_successor_admitted(launcher, preparer, tmp_path)
        if fault == "kill": assert handle.original_host_wait == -9
    else:
        launcher._profile = lambda *_: pytest.fail("unsettled cleanup admitted a successor")
        with pytest.raises(ConflictError, match="cleanup is uncertain"):
            launcher.start("fixture", "workspace")
        assert launcher._cleanup_uncertain is not None
        if fault.startswith("marker_"):
            assert launcher._cleanup_failure["marker_persistence"] == "failed"
        if fault != "restarted_launcher":
            assert launcher._cleanup_failure["reason"] == "cleanup_deadline_exceeded"
        if fault == "marker_after_write":
            # Published bytes without successful durability never authorize.
            assert json.loads((tmp_path / "orderly-handoff-cleanup-uncertain.json").read_text())["state"] == "cleanup_settled"


def test_completed_graph_does_not_admit_start_until_original_adapter_returns(tmp_path, monkeypatch):
    import threading
    from runtime_protocol.errors import ConflictError
    from test_local_worker_composition import _host_only_cleanup_case
    preparer, handle, *_ = _host_only_cleanup_case(tmp_path, monkeypatch, "ack")
    entered, release = threading.Event(), threading.Event()
    abort = preparer.abort
    def delayed(selected):
        abort(selected)
        entered.set()
        assert release.wait(3)
    preparer.abort = delayed
    launcher = LocalWorkerLauncher(credentials=SimpleNamespace(actor_metadata=lambda _: None), profiles={},
        preparer=preparer, inspector=None, workspace_uuid="workspace", realm_root=tmp_path,
        support_root=tmp_path, runtime_pid=77, actor="worker", scopes=())
    launcher._abort(handle, timeout=0)
    thread = launcher._cleanup_attempts[0].thread
    try:
        assert entered.wait(1)
        assert handle.closed and handle._cleanup_settlement is not None
        with pytest.raises(ConflictError, match="cleanup is uncertain"):
            launcher.start("fixture", "workspace")
    finally:
        release.set()
        thread.join(3)
        assert not thread.is_alive()
    _assert_offline_successor_admitted(launcher, preparer, tmp_path)


def test_later_cleanup_generation_retains_previous_settlement_history(tmp_path, monkeypatch):
    import json
    import threading
    from test_local_worker_composition import _host_only_cleanup_case
    preparer, first, *_ = _host_only_cleanup_case(tmp_path, monkeypatch, "ack")
    launcher = LocalWorkerLauncher(credentials=SimpleNamespace(actor_metadata=lambda _: None), profiles={},
        preparer=preparer, inspector=None, workspace_uuid="workspace", realm_root=tmp_path,
        support_root=tmp_path, runtime_pid=77, actor="worker", scopes=())
    abort = preparer.abort
    for generation in range(2):
        if generation == 0:
            handle = first
        else:
            _, handle, *_ = _host_only_cleanup_case(tmp_path, monkeypatch, "ack")
            preparer._active = handle
            handle.preparation["operation_id"] = "second"
        entered, release = threading.Event(), threading.Event()
        def delayed(selected):
            entered.set()
            assert release.wait(3)
            abort(selected)
        preparer.abort = delayed
        launcher._abort(handle, timeout=0)
        thread = launcher._cleanup_attempts[-1].thread
        try:
            assert entered.wait(1)
        finally:
            release.set()
            thread.join(3)
            assert not thread.is_alive()
        _assert_offline_successor_admitted(launcher, preparer, tmp_path)
    marker = json.loads((tmp_path / "orderly-handoff-cleanup-uncertain.json").read_text())
    assert len(marker["history"]) == 1 and len(launcher._cleanup_history) == 2
    assert marker["history"][0]["reason"] == "cleanup_deadline_exceeded"
    assert launcher._cleanup_failure_handle is handle


@pytest.mark.parametrize("logger_fails", [False, True])
def test_cleanup_deadline_during_logging_refreshes_late_outcome(tmp_path, monkeypatch, logger_fails):
    import threading
    from runtime_protocol import local_worker_composition as composition
    from runtime_protocol.errors import ConflictError
    from test_local_worker_composition import _host_only_cleanup_case
    preparer, handle, calls, sent, state = _host_only_cleanup_case(tmp_path, monkeypatch, "terminal120")
    entered, release = threading.Event(), threading.Event()
    threads = []
    def log(*args):
        threads.append(threading.current_thread())
        entered.set()
        assert release.wait(3)
        if logger_fails:
            raise OSError("private-late-log-value")
    monkeypatch.setattr(composition._LOGGER, "warning", log)
    launcher = LocalWorkerLauncher(credentials=SimpleNamespace(actor_metadata=lambda _: None),
        profiles={}, preparer=preparer, inspector=None, workspace_uuid="workspace", realm_root=tmp_path,
        support_root=tmp_path, runtime_pid=77, actor="worker", scopes=())
    try:
        launcher._abort(handle, timeout=0.05)
        assert entered.wait(1)
        with pytest.raises(ConflictError) as caught:
            launcher.start("fixture", "workspace")
        assert caught.value.details["reason"] == "cleanup_deadline_exceeded"
        assert caught.value.details["outcome"]["logging_status"] == "pending"
    finally:
        release.set()
        for thread in threads:
            thread.join(3)
            assert not thread.is_alive()
    with pytest.raises(ConflictError) as caught:
        launcher.start("fixture", "workspace")
    assert caught.value.details["reason"] == "cleanup_deadline_exceeded"
    assert caught.value.details["outcome"]["logging_status"] == ("failed" if logger_fails else "written")
    assert caught.value.details["outcome"]["original_host_wait"] == 120
    assert caught.value.details["outcome"]["complete_graph"] is False
