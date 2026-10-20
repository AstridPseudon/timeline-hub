"""Direct adapter for the production pack-host handoff.

This helper owns only a fresh host. Runtime discovery, worker credentials, and
the selected source checkout remain authoritative inputs from the caller.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

from astrid.core.execution.generic_host import RuntimeProtocolClient
from astrid.sdk import host_bootstrap
from astrid.sdk.upgrade import _pack_host_lock
from astrid.sdk.workspace_client import _safe_local_path


def _handoff(realm_dir: Path, support_dir: Path, discovery_file: Path,
             source_checkout: Path, runtime_instance_id: str) -> dict:
    realm = _safe_local_path(realm_dir, field="realm")
    support = _safe_local_path(support_dir, field="support")
    discovery = _safe_local_path(discovery_file, field="discovery")
    source = _safe_local_path(source_checkout, field="source checkout")
    if discovery != support / "discovery.json":
        raise ValueError("discovery must belong to the supplied support directory")
    value = json.loads(discovery.read_text(encoding="utf-8"))
    if (not runtime_instance_id or value.get("runtime_instance_id") != runtime_instance_id
            or value.get("realm_root") != str(realm)):
        raise ValueError("discovery does not identify the supplied Runtime and realm")
    worker = _safe_local_path(value["worker_credential_file"], field="worker credential")
    if worker.parent != support / "credentials":
        raise ValueError("worker credential must belong to the supplied support directory")
    if (value.get("worker_actor") != host_bootstrap.PACK_HOST_ACTOR
            or tuple(value.get("worker_scopes", ())) != host_bootstrap.PACK_HOST_SCOPES):
        raise ValueError("discovery does not declare the production pack-host credential")
    return {**value, "source_checkout": str(source)}


@dataclass
class RealPackHost:
    support_dir: Path
    state: dict
    ready: dict
    closed: bool = False

    def close(self) -> None:
        if self.closed:
            return
        with _pack_host_lock(self.support_dir):
            current = host_bootstrap._read_object(self.support_dir / "generic-host.json")
            if current != self.state:
                raise RuntimeError("host registration changed; refusing to stop another host")
            if host_bootstrap._registered_host_status(self.state) == "foreign":
                raise RuntimeError("host process identity changed; refusing cleanup")
            host_bootstrap._retire_host_locked(self.state)
            if host_bootstrap._group_survivors(self.state["pid"]):
                raise RuntimeError("owned host group survived cleanup")
            try:
                os.waitpid(self.state["pid"], 0)
            except ChildProcessError:
                pass
        self.closed = True

    def __enter__(self) -> "RealPackHost":
        return self

    def __exit__(self, *_exc) -> None:
        self.close()


def start_real_pack_host(*, realm_dir: Path, support_dir: Path, discovery_file: Path,
                         source_checkout: Path, runtime_instance_id: str) -> RealPackHost:
    value = _handoff(realm_dir, support_dir, discovery_file, source_checkout, runtime_instance_id)
    support = Path(value["worker_credential_file"]).parent.parent
    if any((support / name).exists() for name in ("generic-host.json", "generic-host.ready.json")):
        raise RuntimeError("helper requires a fresh host registration")
    token = Path(value["worker_credential_file"]).read_text(encoding="utf-8").strip()
    client = RuntimeProtocolClient(value["endpoint"], token)
    health = client.health()
    if health["runtime_instance_id"] != runtime_instance_id:
        raise RuntimeError("live Runtime differs from supplied discovery")
    if client._authenticate_worker(host_bootstrap.PACK_HOST_ACTOR) != value["active_realm"]:
        raise RuntimeError("worker credential belongs to another realm")
    result = host_bootstrap.ensure_pack_host(
        value, reconfigure_action="inspect the selected render environment", startup_idle_seconds=60,
    )
    try:
        os.waitpid(result["host_pid"], os.WNOHANG)
    except ChildProcessError as exc:
        raise RuntimeError("returned host is not this helper's child") from exc
    state = host_bootstrap._read_object(support / "generic-host.json")
    if state.get("pid") != result["host_pid"]:
        raise RuntimeError("host registration differs from launched host")
    if (result["host_status"] != "ready"
            or "rendering.timeline_visualize" not in result["host_ready_capabilities"]):
        raise RuntimeError("timeline visualization is not ready in the production host")
    return RealPackHost(support, state, result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("realm-dir", "support-dir", "discovery-file", "source-checkout"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--runtime-instance-id", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(SystemExit(1)))
    signal.signal(signal.SIGINT, lambda *_: (_ for _ in ()).throw(SystemExit(1)))
    try:
        with start_real_pack_host(**vars(args)) as host:
            print(json.dumps({"status": "ready", **host.ready}), flush=True)
            command = sys.stdin.readline()
            if command not in ("stop\n", ""):
                raise ValueError("expected stop or EOF")
        print(json.dumps({"status": "stopped", "host_pid": host.state["pid"]}), flush=True)
        return 0
    except Exception as exc:  # noqa: BLE001 - secret-free helper boundary
        frames = traceback.extract_tb(exc.__traceback__)
        print(json.dumps({"status": "failed", "error_type": type(exc).__name__,
                          "error_location": f"{frames[-1].filename}:{frames[-1].lineno}"}), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
