"""DirectHarness adapter for the production launcher's ensure_pack_host seam.

The caller owns the Runtime and selected render environment. This helper owns
only a fresh host; it never provisions credentials or changes source closure.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from astrid.core.execution.generic_host import RuntimeProtocolClient
from astrid.sdk import host_bootstrap
from astrid.sdk.upgrade import _pack_host_lock
from astrid.sdk.workspace_client import _safe_local_path


@contextmanager
def _termination_guard(*, launching: bool = False, before_delivery=None):
    """Defer launch signals without passing a blocked mask to the child.

    Retirement keeps signals blocked through waitpid. Restore/replay only
    inside the caller's ownership guard, preserving any cleanup failure.
    """
    signals = (signal.SIGINT, signal.SIGTERM, signal.SIGALRM)
    previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, signals)
    handlers = {}
    pending = set()
    failure = None

    def deliver(signum, _frame):
        if handlers[signum] != signal.SIG_IGN:
            before_delivery()
        signal.signal(signum, handlers[signum])
        signal.raise_signal(signum)

    try:
        if launching:
            for sig in signals:
                handlers[sig] = signal.signal(sig, lambda signum, _frame: pending.add(signum))
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        yield
    except BaseException as exc:
        failure = exc
        raise
    finally:
        signal.pthread_sigmask(signal.SIG_BLOCK, signals)
        for sig in handlers:
            signal.signal(sig, deliver)
        for sig in pending:
            os.kill(os.getpid(), sig)
        try:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        except BaseException:
            if failure is not None:
                raise failure
            raise
        finally:
            for sig, handler in handlers.items():
                signal.signal(sig, handler)


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
        with _termination_guard(), _pack_host_lock(self.support_dir):
            current = host_bootstrap._read_object(self.support_dir / "generic-host.json")
            if current != self.state:
                raise RuntimeError("host registration changed; refusing to stop another host")
            if host_bootstrap._registered_host_status(self.state) in ("foreign", "reused"):
                raise RuntimeError("host process identity changed; refusing cleanup")
            host_bootstrap._retire_host_locked(self.state)
            if host_bootstrap._group_survivors(
                    self.state["pid"], leader_birth=self.state["process_birth_id"]):
                raise RuntimeError("owned host group survived cleanup")
            try:
                os.waitpid(self.state["pid"], 0)
            except ChildProcessError:
                pass  # The production Popen/custody observer may already have reaped it.
            self.closed = True

    def __enter__(self) -> RealPackHost:
        return self

    def __exit__(self, *_exc) -> None:
        self.close()


@contextmanager
def start_real_pack_host(*, realm_dir: Path, support_dir: Path, discovery_file: Path,
                         source_checkout: Path, runtime_instance_id: str):
    """Own a fresh production host, yielding only after real catalog readiness.

    DirectHarness uses runtime_protocol.cli rather than the neutral launcher's
    catalog layout. Feed its actual discovery into the same ensure_pack_host
    call as ensure_runtime, without acquiring or restarting a Runtime.
    """
    value = _handoff(realm_dir, support_dir, discovery_file, source_checkout, runtime_instance_id)
    support = Path(value["worker_credential_file"]).parent.parent
    if any((support / name).exists() for name in ("generic-host.json", "generic-host.ready.json")):
        raise RuntimeError("helper requires a fresh host registration")
    client = RuntimeProtocolClient(value["endpoint"], Path(value["worker_credential_file"]).read_text().strip())
    health = client.health()
    if health["runtime_instance_id"] != runtime_instance_id:
        raise RuntimeError("live Runtime differs from supplied discovery")
    realm_id = client._authenticate_worker(host_bootstrap.PACK_HOST_ACTOR)
    if realm_id != value["active_realm"]:
        raise RuntimeError("worker credential belongs to another realm")
    handle = None
    try:
        with _termination_guard(
                launching=True, before_delivery=lambda: handle.close() if handle else None):
            result = host_bootstrap.ensure_pack_host(
                value, reconfigure_action="inspect the DirectHarness Runtime and selected render environment",
                startup_idle_seconds=30,
            )
            with _pack_host_lock(support):
                pid = result["host_pid"]
                state = host_bootstrap._read_object(support / "generic-host.json")
                birth = host_bootstrap._host_birth_identity(pid)
                if (state.get("pid") != pid or not birth
                        or state.get("process_birth_id") != birth):
                    raise RuntimeError("host registration differs from launched host identity")
                try:
                    # WNOHANG returns zero only for our still-live child.
                    child, _ = os.waitpid(pid, os.WNOHANG)
                except ChildProcessError as exc:
                    raise RuntimeError("returned host is not this helper's child") from exc
                if child:
                    raise RuntimeError("returned host child already exited")
                handle = RealPackHost(support, state, result)
            if (result["host_status"] != "ready"
                    or "rendering.render" not in result["host_ready_capabilities"]):
                raise RuntimeError("rendering.render is not ready in the production host")
            cursor = None
            while True:
                page, cursor = client.generated.list_capabilities(cursor=cursor)
                if any(item.capability_id == "rendering.render" and item.status == "ready" for item in page):
                    break
                if not cursor:
                    raise RuntimeError("rendering.render is not ready in the Runtime capability catalog")
        yield handle
    finally:
        if handle is not None:
            handle.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("realm-dir", "support-dir", "discovery-file", "source-checkout"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--runtime-instance-id", required=True)
    args = parser.parse_args()

    def interrupted(_signum, _frame):
        raise SystemExit(1)

    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGALRM):
        signal.signal(sig, interrupted)
    try:
        signal.alarm(180)
        with start_real_pack_host(**vars(args)) as host:
            signal.alarm(0)
            print(json.dumps({"status": "ready", **host.ready}), flush=True)
            # A pipe held by the App wrapper is the lifetime handshake. EOF
            # also cleans up when the wrapper exits unexpectedly.
            command = sys.stdin.readline()
            if command not in ("stop\n", ""):
                raise ValueError("expected stop or EOF")
        print(json.dumps({"status": "stopped", "host_pid": host.state["pid"]}), flush=True)
        return 0
    except Exception as exc:  # noqa: BLE001 - secret-free CLI error boundary
        # Product exceptions may contain diagnostics: expose only their type,
        # never a credential-bearing object or arbitrary exception text.
        frames = traceback.extract_tb(exc.__traceback__)
        print(json.dumps({"status": "failed", "error_type": type(exc).__name__,
                          "error_location": f"{frames[-1].filename}:{frames[-1].lineno}"}), flush=True)
        return 1
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
