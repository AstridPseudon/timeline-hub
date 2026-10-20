"""Offline handoff checks and centrally run real startup/catalog/cleanup smoke."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from astrid.core._shared.boot_manifest import load_boot_manifest_hash
from astrid.core.execution.generic_host import (
    RuntimeProtocolClient,
    source_checkout_closure_digest,
    source_checkout_digest,
)
from astrid.sdk import host_bootstrap
from tests.packs.rendering.real_pack_host import RealPackHost, _handoff


@pytest.mark.parametrize("change", ["instance", "realm", "credential", "scopes", "symlink"])
def test_handoff_rejects_foreign_inputs_before_launch(tmp_path, change):
    support = tmp_path / "support"
    support.mkdir()
    value = {
        "runtime_instance_id": "instance", "realm_root": str(tmp_path / "realm"),
        "worker_credential_file": str(support / "credentials" / "astrid-pack-host.token"),
        "worker_actor": host_bootstrap.PACK_HOST_ACTOR,
        "worker_scopes": list(host_bootstrap.PACK_HOST_SCOPES),
    }
    if change == "instance":
        value["runtime_instance_id"] = "another"
    elif change == "realm":
        value["realm_root"] = str(tmp_path / "another")
    elif change == "credential":
        value["worker_credential_file"] = str(tmp_path / "foreign.token")
    elif change == "scopes":
        value["worker_scopes"] = ["admin"]
    discovery = support / "discovery.json"
    discovery.write_text(json.dumps(value))
    if change == "symlink":
        discovery.rename(support / "original.json")
        discovery.symlink_to(support / "original.json")
    with pytest.raises((ValueError, RuntimeError)):
        _handoff(tmp_path / "realm", support, discovery, Path(__file__).resolve().parents[3], "instance")


def test_cleanup_refuses_replaced_registration(tmp_path):
    original = {"pid": 123, "process_birth_id": "original"}
    replacement = {"pid": os.getpid(), "process_birth_id": "replacement"}
    marker = tmp_path / "generic-host.json"
    marker.write_text(json.dumps(replacement))
    host = RealPackHost(tmp_path, original, {})
    with pytest.raises(RuntimeError, match="registration changed"):
        host.close()
    assert json.loads(marker.read_text()) == replacement
    assert not host.closed


@pytest.mark.integration
@pytest.mark.timeout(240)
def test_real_host_cli_catalog_and_owned_group_cleanup(tmp_path, real_runtime, owned_process_groups):
    # Match DirectHarness.start(), which creates private support before the daemon.
    (tmp_path / "support").mkdir(mode=0o700)
    daemon = real_runtime(production_worker_credentials=True)
    source = Path(__file__).resolve().parents[3]
    discovery = daemon.support_root / "discovery.json"
    value = json.loads(discovery.read_text())
    command = [sys.executable, "-m", "tests.packs.rendering.real_pack_host",
               "--realm-dir", str(daemon.root), "--support-dir", str(daemon.support_root),
               "--discovery-file", str(discovery), "--source-checkout", str(source),
               "--runtime-instance-id", value["runtime_instance_id"]]
    child_env = {**os.environ, "PYTHONPATH": str(source)}
    # conftest adds a pytest bytecode cache override, which authentic launch
    # validation correctly rejects. DirectHarness does not use that override.
    child_env.pop("PYTHONPYCACHEPREFIX", None)
    process = owned_process_groups.popen(
        command, cwd=source, env=child_env,
        start_new_session=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    try:
        line = process.stdout.readline()
        ready = json.loads(line)
        assert ready["status"] == "ready", ready
        pid = ready["host_pid"]
        assert pid != os.getpid() and os.getpgid(pid) == pid
        assert ready["host_runtime_instance_id"] == daemon.instance_id
        assert ready["host_source_checkout_digest"] == source_checkout_digest(source)
        assert ready["host_source_closure_digest"] == source_checkout_closure_digest(source)
        assert ready["host_boot_manifest_hash"] == load_boot_manifest_hash(
            Path(ready["host_boot_manifest_path"]), support_root=daemon.support_root)
        assert "rendering.render" in ready["host_ready_capabilities"]
        state = json.loads((daemon.support_root / "generic-host.json").read_text())
        assert state["remotion_validation"]
    finally:
        stdout, stderr = process.communicate("stop\n", timeout=40)
    assert process.returncode == 0, stderr
    assert json.loads(stdout)["status"] == "stopped"
    assert not host_bootstrap._group_survivors(pid)
    assert not (daemon.support_root / "generic-host.json").exists()
    assert not (daemon.support_root / "generic-host.ready.json").exists()
    assert RuntimeProtocolClient(daemon.endpoint, daemon.worker_token).health().status == "ok"
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
