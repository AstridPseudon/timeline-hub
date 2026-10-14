"""Read-only dev identity and clean, owner-bound source promotion."""
from __future__ import annotations

import json
import os
import fcntl
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Mapping

PROFILE_NAME = "astrid"
TERMINAL_TASK_STATES = frozenset({"completed", "succeeded", "cancelled", "canceled", "expired", "failed"})
GIT_TIMEOUT_SECONDS = 30.0
READY_WAIT_SECONDS = 60.0
READY_POLL_SECONDS = 0.5


class DevOperatorError(RuntimeError):
    """A refused or failed operator action, with the one next step to take."""

    def __init__(self, message: str, *, next_action: str | None = None, state: str = "refused") -> None:
        super().__init__(message)
        self.next_action = next_action
        self.state = state


def dev_checkout() -> Path:
    """The checkout this client's ``astrid`` package was imported from (the dev tree)."""
    import astrid

    return Path(astrid.__file__).resolve().parents[1]


def _git(repo: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DevOperatorError(f"git {' '.join(args)} failed in {repo}: {exc}", state="error") from exc
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()[-300:]
        raise DevOperatorError(f"git {' '.join(args)} failed in {repo}: {detail}", state="error")
    return proc.stdout.strip()


def _git_branch(repo: Path) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "symbolic-ref", "--short", "-q", "HEAD"],
            capture_output=True, text=True, timeout=GIT_TIMEOUT_SECONDS, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:  # detached HEAD: symbolic-ref exits 1
        return None
    return proc.stdout.strip() or None


def _git_state(repo: Path) -> dict[str, Any]:
    status = _git(repo, "status", "--porcelain")
    return {
        "checkout": str(repo),
        "head": _git(repo, "rev-parse", "HEAD"),
        "branch": _git_branch(repo),
        "dirty": bool(status),
        "dirty_paths": len(status.splitlines()) if status else 0,
    }


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def served_profile(data_root: Path) -> dict[str, Any]:
    """The source profile the runtime boots the pack host from."""
    path = Path(data_root) / "runtime" / "source-profiles" / f"{PROFILE_NAME}.json"
    value = _read_json(path)
    if value is None or not value.get("source_checkout"):
        raise DevOperatorError(
            f"no readable source profile at {path}",
            next_action="banodoco-local up --profile astrid --source-manifest <profile.json>",
            state="unavailable",
        )
    return {
        "profile_path": str(path),
        "source_checkout": str(Path(str(value["source_checkout"])).expanduser().resolve()),
        "runtime_checkout": value.get("runtime_checkout"),
    }


def host_state(runtime_dir: Path) -> dict[str, Any]:
    """The pack host recorded by the runtime, with pid identity and readiness."""
    from astrid.sdk.host_bootstrap import _host_identity_matches, _host_pid_alive

    state = _read_json(runtime_dir / "generic-host.json")
    ready = _read_json(runtime_dir / "generic-host.ready.json")
    if state is None:
        return {"recorded": False, "pid": None, "alive": False, "identity_verified": False, "ready": False,
                "ready_status": None, "source_checkout": None, "source_checkout_digest": None,
                "source_closure_digest": None}
    pid = state.get("pid")
    alive = bool(_host_pid_alive(pid))
    verified = bool(alive and _host_identity_matches(state))
    ready_ok = bool(verified and ready and ready.get("status") == "ready"
                    and str(ready.get("pid")) == str(pid)
                    and ready.get("process_birth_id") == state.get("process_birth_id")
                    and ready.get("source_closure_digest") == state.get("source_closure_digest")
                    and ready.get("runtime_instance_id") == state.get("runtime_instance_id"))
    return {
        "recorded": True,
        "pid": pid,
        "alive": alive,
        "identity_verified": verified,
        "ready": ready_ok,
        "ready_status": (ready or {}).get("status"),
        "ready_file": state.get("ready_file"),
        "source_checkout": state.get("source_checkout"),
        "source_checkout_digest": state.get("source_checkout_digest"),
        "source_closure_digest": state.get("source_closure_digest"),
    }


def _default_digests() -> tuple[Callable[[Path], str], Callable[[Path], str]]:
    from astrid.core.execution.generic_host import (
        source_checkout_closure_digest,
        source_checkout_digest,
    )

    return source_checkout_digest, source_checkout_closure_digest


def pair_report(
    *,
    served: Path,
    client: Path,
    host: Mapping[str, Any],
    digest_fn: Callable[[Path], str] | None = None,
    closure_fn: Callable[[Path], str] | None = None,
) -> dict[str, Any]:
    """Compare this client's code with the served tree and with the host's attestation.

    ``paired`` only when the client's tree and the served tree have the same pack
    digest and closure digest, and the running host attested that same served
    digest. Anything else is ``drift``; a tree that cannot be measured is ``unknown``.
    """
    default_digest, default_closure = _default_digests()
    digest_fn = digest_fn or default_digest
    closure_fn = closure_fn or default_closure
    try:
        served_digest, served_closure = digest_fn(served), closure_fn(served)
        client_digest, client_closure = digest_fn(client), closure_fn(client)
    except (OSError, ValueError) as exc:
        return {"status": "unknown", "reason": f"cannot measure a checkout: {exc}",
                "client_checkout": str(client), "served_checkout": str(served)}
    same_tree = client_digest == served_digest and client_closure == served_closure
    host_attested = host.get("source_checkout_digest")
    host_matches = host_attested == served_digest if host.get("recorded") else None
    if same_tree and host_matches is not False:
        status, reason = "paired", "client code matches the served tree"
        if host_matches is None:
            reason += "; no host recorded yet"
    elif not same_tree:
        status = "drift"
        reason = ("dev tree differs from the served tree (uncommitted or unpromoted work); "
                  "commit, then `python -m astrid dev promote`")
    else:
        status = "drift"
        reason = "the running host attested a different served tree than the one now on disk; restart it"
    return {
        "status": status,
        "reason": reason,
        "client_checkout": str(client),
        "served_checkout": str(served),
        "client_digest": client_digest,
        "served_digest": served_digest,
        "client_closure_digest": client_closure,
        "served_closure_digest": served_closure,
        "host_attested_digest": host_attested,
        "host_matches_served": host_matches,
    }


def run_status(*, data_root: Path, client: Path | None = None,
               digest_fn: Callable[[Path], str] | None = None,
               closure_fn: Callable[[Path], str] | None = None) -> dict[str, Any]:
    """Read-only report: served checkout, dev tree, host state, and the pair check."""
    client = Path(client).resolve() if client is not None else dev_checkout()
    profile = served_profile(data_root)
    served = Path(profile["source_checkout"])
    dev = _git_state(client)
    served_state = _git_state(served) if served.is_dir() else None
    host = host_state(Path(data_root) / "runtime")
    pair = pair_report(served=served, client=client, host=host, digest_fn=digest_fn, closure_fn=closure_fn)
    same_head = bool(served_state and served_state["head"] == dev["head"])
    return {
        "ok": True,
        "state": "reported",
        "profile": profile,
        "served": served_state,
        "dev": dev,
        "dev_matches_served_head": same_head,
        "host": host,
        "pair": pair,
    }


def _flatten_rows(value: Any) -> list[dict[str, Any]]:
    """Collect dict rows from the nested ``data`` lists a Runtime listing returns."""
    if isinstance(value, Mapping):
        return [dict(value)] if ("state" in value or "task_id" in value or "slug" in value or "project_id" in value) else []
    if isinstance(value, (list, tuple)):
        rows: list[dict[str, Any]] = []
        for item in value:
            rows.extend(_flatten_rows(item))
        return rows
    return []


def _listing_data(result: Any) -> Any:
    if isinstance(result, Mapping):
        if result.get("ok") is False:
            raise DevOperatorError(f"runtime listing failed: {result.get('error')}", state="unavailable")
        return result.get("data")
    if getattr(result, "ok", True) is False:
        raise DevOperatorError(f"runtime listing failed: {getattr(result, 'error', None)}", state="unavailable")
    return getattr(result, "data", result)


def _page_cursor(result: Any) -> str | None:
    """The next-page cursor a Runtime listing carries as a string item in its data."""
    data = _listing_data(result)
    if isinstance(data, (list, tuple)):
        for item in data:
            if isinstance(item, str) and item:
                return item
    return None


def _all_pages(fetch: Callable[[str | None], Any], *, max_pages: int = 1000) -> list[dict[str, Any]]:
    """Follow a Runtime listing to its last page. A listing that stops early can hide live work."""
    rows: list[dict[str, Any]] = []
    cursor: str | None = None
    seen: set[str] = set()
    for _ in range(max_pages):
        result = fetch(cursor)
        rows.extend(_flatten_rows(_listing_data(result)))
        cursor = _page_cursor(result)
        if cursor is None or cursor in seen:
            return rows
        seen.add(cursor)
    raise DevOperatorError("runtime listing did not end; cannot prove the host is idle", state="unavailable")


def in_flight_tasks(client: Any) -> list[str]:
    """Task ids the Runtime reports as not yet terminal, across every project and page."""
    projects = _all_pages(lambda cursor: client.projects.list(cursor=cursor) if cursor else client.projects.list())
    busy: list[str] = []
    for project in projects:
        project_ref = project.get("slug") or project.get("project_id")
        if not project_ref:
            continue
        tasks = _all_pages(
            lambda cursor, ref=str(project_ref): client.tasks.list(ref, cursor=cursor) if cursor
            else client.tasks.list(ref)
        )
        for task in tasks:
            if str(task.get("state", "")).lower() not in TERMINAL_TASK_STATES:
                busy.append(str(task.get("task_id") or task.get("id") or task.get("state")))
    return busy


def _last_error_line(log: Path) -> str | None:
    try:
        with log.open("rb") as handle:
            handle.seek(max(0, log.stat().st_size - 200_000))
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return None
    errors = [line for line in lines if "Error" in line]
    return errors[-1][-400:] if errors else None


def _require_linked_serve_worktree(dev: Path, serve: Path) -> None:
    if serve == dev:
        raise DevOperatorError(
            "the runtime serves the dev tree itself; promote needs a separate serve worktree",
            next_action="git -C <dev> worktree add --detach ../Astrid-serve HEAD, then re-point the source profile",
            state="unavailable",
        )
    common_dev = Path(_git(dev, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    try:
        common_serve = Path(_git(serve, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    except DevOperatorError as exc:
        raise DevOperatorError(f"served checkout {serve} is not a git worktree: {exc}", state="unavailable") from exc
    if common_dev != common_serve:
        raise DevOperatorError(
            f"served checkout {serve} belongs to a different repository than the dev tree {dev}",
            state="unavailable",
        )


def run_promote(*, data_root: Path, ref: str | None = None, force: bool = False,
                client: Path | None = None, open_client=None, terminate_host=None,
                digest_fn=None, closure_fn=None, ready_wait_seconds: float = READY_WAIT_SECONDS):
    """Promote only a clean linked source tree after an owned stop proves absent.

    A new CLI has no retained process graph: it refuses safely and asks the
    resident owner to perform the transition. Marker/PID possession is never
    cleanup authority, and force abandonment is unsupported.
    """
    if force:
        raise DevOperatorError("force abandonment is unsupported; wait for owned work to settle")
    from astrid.sdk.host_bootstrap import _terminate_old_host
    from astrid.sdk.client import AstridClient
    terminate_host = terminate_host or _terminate_old_host
    open_client = open_client or AstridClient.open_from_launcher
    default_digest, default_closure = _default_digests()
    digest_fn, closure_fn = digest_fn or default_digest, closure_fn or default_closure
    dev = Path(client).resolve() if client else dev_checkout()
    profile = served_profile(data_root)
    serve = Path(profile["source_checkout"])
    _require_linked_serve_worktree(dev, serve)
    if _git(dev, "status", "--porcelain", "--untracked-files=all") or _git(serve, "status", "--porcelain", "--untracked-files=all"):
        raise DevOperatorError("source or served tree has local changes; promotion preserves dirty work and refuses")
    target = _git(dev, "rev-parse", "--verify", f"{ref or 'HEAD'}^{{commit}}")
    old = _git(serve, "rev-parse", "HEAD")
    runtime_dir = Path(data_root) / "runtime"
    with open_client(start_pack_host=False) as connection:
        if in_flight_tasks(connection):
            raise DevOperatorError("Runtime reports active work; promotion refused", state="busy")
    state_path = runtime_dir / "generic-host.json"
    before = _read_json(state_path)
    if before is None:
        raise DevOperatorError("resident host custody is unavailable; use the supported owner stop/relaunch", state="unavailable")
    with (runtime_dir / "generic-host.lock").open("a+") as lock:
        os.fchmod(lock.fileno(), 0o600)
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if _read_json(state_path) != before or served_profile(data_root) != profile:
            raise DevOperatorError("service/profile identity changed before promotion")
        if _git(serve, "rev-parse", "HEAD") != old or _git(serve, "status", "--porcelain", "--untracked-files=all"):
            raise DevOperatorError("served tree changed before the owned stop")
        # This helper retains the exact graph, stops it and proves it absent.
        # Any uncertainty exits before Git mutates the served source.
        try:
            terminate_host(before)
        except Exception as exc:
            raise DevOperatorError("resident owner could not prove host cleanup; served tree remains unchanged",
                                   next_action="use the supported owner stop/relaunch; never kill a numeric PID") from exc
        if _read_json(state_path) != before or served_profile(data_root) != profile:
            raise DevOperatorError("service/profile changed during owned cleanup; no checkout mutation")
        if _git(serve, "rev-parse", "HEAD") != old or _git(serve, "status", "--porcelain", "--untracked-files=all"):
            raise DevOperatorError("served tree changed during owned cleanup; no checkout mutation")
        _git(serve, "checkout", "--quiet", "--detach", target)
    try:
        with open_client(start_pack_host=True):
            pass
    except Exception as exc:
        raise DevOperatorError("source promoted after owned stop, but activation failed; retain state and retry supported relaunch",
                               state="activation_failed") from exc
    after = host_state(runtime_dir)
    deadline = time.monotonic() + min(60.0, max(0.0, ready_wait_seconds))
    while not after["ready"] and time.monotonic() < deadline:
        time.sleep(READY_POLL_SECONDS)
        after = host_state(runtime_dir)
    observed = _read_json(state_path) or {}
    if (not after["ready"] or observed.get("process_birth_id") == before.get("process_birth_id")
            or observed.get("runtime_instance_id") != before.get("runtime_instance_id")
            or after.get("source_checkout_digest") != digest_fn(serve)
            or after.get("source_closure_digest") != closure_fn(serve)):
        raise DevOperatorError("promoted host readiness/source/service identity is unproved", state="activation_failed")
    return {"ok": True, "state": "promoted", "old_sha": old, "new_sha": target,
            "served_checkout": str(serve), "pair": pair_report(served=serve, client=dev, host=after,
                                                               digest_fn=digest_fn, closure_fn=closure_fn)}


def main(args: list[str]) -> int:
    import argparse
    from astrid.sdk.storage_root import resolve_runtime_data_root
    parser = argparse.ArgumentParser(prog="astrid dev", description="Read source/served identity; promote only through retained owner custody.")
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status"); status.add_argument("--json", action="store_true")
    promote = sub.add_parser("promote"); promote.add_argument("--ref"); promote.add_argument("--json", action="store_true")
    promote.add_argument("--force", action="store_true", help="rejected: abandonment is unsupported")
    parsed = parser.parse_args(args)
    try:
        payload = run_status(data_root=resolve_runtime_data_root()) if parsed.command == "status" else run_promote(
            data_root=resolve_runtime_data_root(), ref=parsed.ref, force=parsed.force)
    except (DevOperatorError, OSError, ValueError) as exc:
        payload = {"ok": False, "state": getattr(exc, "state", "error"), "error": str(exc),
                   "next_action": getattr(exc, "next_action", None)}
    print(json.dumps(payload, sort_keys=True, indent=2))
    return 0 if payload["ok"] else 1
