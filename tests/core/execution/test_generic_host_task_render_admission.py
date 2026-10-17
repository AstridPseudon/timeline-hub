"""Source-only run_task admission to V3 command guard regression.

Observe the real producer before its first Runtime heartbeat. No Runtime or
renderer response, readiness receipt, process, or successful task is fabricated.
"""
import inspect
import os
from dataclasses import replace
from pathlib import Path

import pytest

from astrid.core.execution import generic_host


@pytest.mark.parametrize("corruption", [None, "wrong-root", "missing-roots"])
def test_run_task_python_roots_reach_v3_command_guard(tmp_path, monkeypatch, corruption):
    # Set every state location before constructing either real SDK object.
    for name, suffix in {
        "HOME": "home", "ASTRID_HOME": "astrid", "XDG_CONFIG_HOME": "config",
        "XDG_DATA_HOME": "data", "XDG_CACHE_HOME": "cache", "TMPDIR": "tmp",
        "ASTRID_WORKSPACE_CONFIG_DIR": "workspace", "ASTRID_RUNTIME_DATA_ROOT": "runtime",
    }.items():
        directory = tmp_path / suffix
        directory.mkdir(exist_ok=True)
        monkeypatch.setenv(name, str(directory))

    pack = Path(generic_host.__file__).resolve().parents[2] / "packs" / "rendering"
    # This real client is never contacted: stop at the internal producer
    # boundary, before heartbeat, rather than substituting a Runtime service.
    client = generic_host.RuntimeProtocolClient("http://127.0.0.1:1", "unused-boundary-token")
    host = generic_host.GenericPackHost(pack_roots=[pack], client=client, attempt_base=tmp_path / "attempts")
    host.discover()
    record = host.capabilities["rendering.render"]
    _, canonical = host.admit("executor", record.id)
    # Readiness is outside this source-only check. This local prerequisite
    # does not produce a readiness receipt or advertise/register a capability.
    host.capabilities[record.id] = replace(record, ready=True)
    monkeypatch.setattr(host, "preflight", lambda _capability_id: None)
    # No authenticated attempt/policy is issued in this source fixture. The
    # real command guard below must stop before requesting one or spawning.
    monkeypatch.setattr(host, "_attempt_policy_factory", None)

    class ObservedAdmission(BaseException):
        pass

    observed = {}

    def observe_producer(_cancel_signal, **_kwargs):
        # _ManagedTaskAdapter is the first internal call after the producer.
        # Observe actual run_task locals without copying/reimplementing it or
        # replacing any Runtime operation. Stop before lease/worker activity.
        frame = inspect.currentframe().f_back
        try:
            assert frame.f_code is host._run_task_impl.__func__.__code__
            observed.update(admission=dict(frame.f_locals["network_admission"]),
                            attempt=frame.f_locals["root"])
        finally:
            del frame
        raise ObservedAdmission

    try:
        with monkeypatch.context() as producer_observation:
            producer_observation.setattr(generic_host, "_ManagedTaskAdapter", observe_producer)
            with pytest.raises(ObservedAdmission):
                host.run_task({"id": "boundary-task", "capability": record.id,
                               "project_id": "boundary-project", "attempt_id": "boundary-attempt",
                               "fence": 7, "spec": {}}, lease_token="unused-boundary-lease")

        admission = observed["admission"]
        assert {key: admission[key] for key in canonical} == canonical
        assert admission["python_path_roots"] == []  # explicit empty builtin roots
        assert (admission["task_id"], admission["attempt_id"], admission["fence"]) == (
            "boundary-task", "boundary-attempt", 7)
        assert admission["network_nonce"] and admission["allowed_routes"] == []
        if corruption == "wrong-root":
            admission["python_path_roots"] = [str(tmp_path / "unadmitted")]
        elif corruption == "missing-roots":
            del admission["python_path_roots"]

        class ReachedConfinement(Exception):
            pass

        def observe_confinement(attempt):
            assert attempt == observed["attempt"]
            observed["passed_guard"] = True
            raise ReachedConfinement

        monkeypatch.setattr(host, "_required_confinement_policy", observe_confinement)
        monkeypatch.setattr(host, "_child_environment", lambda *args, **kwargs: (
            {"HOME": str(tmp_path / "home"), "PATH": os.environ.get("PATH", "")}, {}))
        monkeypatch.setattr(generic_host, "popen_owned_group", lambda *args, **kwargs:
                            pytest.fail("admission boundary must stop before spawn"))
        attempt = observed["attempt"]
        output = attempt / "outputs"
        output.mkdir()
        timeline = tmp_path / "timeline.json"
        timeline.write_text('{"tracks": [], "clips": []}', encoding="utf-8")
        error = ReachedConfinement if corruption is None else generic_host.HostError
        message = None if corruption is None else "exact admitted source and capability"
        with pytest.raises(error, match=message):
            host._run_command_definition(record, {"timeline": str(timeline)}, output,
                                         attempt, admission=admission)
        assert observed.get("passed_guard", False) is (corruption is None)
        assert not host._active_processes
    finally:
        # The observation deliberately exits before run_task's workload
        # finally begins. Its private empty attempt remains fixture-owned.
        host.shutdown()
