"""Real-process merge gate for a stopped film workspace (``astrid dev journey``).

Run only on a machine allowed to start Runtime, Remotion and process groups.
No Runtime or renderer layer is mocked here.  The reference is never opened for
writing; workspace adoption receives a private filesystem clone.

``--tier smoke`` renders a short excerpt and proves the host-lifecycle fixes keep
holding: an outdated idle host replaces itself, a host started inside a capacity job
outlives it, duplicate PATH entries reuse the host, a kill -9 of the idle host recovers
by itself, and a kill -9 mid-render leaves no orphaned render group.  ``--tier full``
adds the real user journey (Codex image, sprites, timeline edit/publish, full render).

``--reference generated`` builds a small stopped reference (``reference_realm.py``) instead of using a film.
``--backend rendering.ffmpeg`` renders with ffmpeg where the film is media-only.  After the crash-recovery
phases ``runtime_restart`` restarts the Runtime and admits a render with the App's exact request.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from astrid.core.dev import reference_realm
from astrid.core.rendering.remotion_runtime import _INTERACTIVE_GIT_ENV, _UNSUPPORTED_PYTHON_STARTUP

# No phase is judged by how long it takes: durations and machine load are recorded for information.
# A command is stopped only when it is genuinely hung, with no exit within a ceiling many times its
# usual duration on a loaded Mac (renders: ~1-2 min usual, 30 min ceiling).
HANG_SECONDS = {
    "reference": 60, "adopt": 900, "up": 300, "first_open": 900, "doctor": 300,
    "render_1": 1800, "source_change": 60, "replace_host": 1800, "heavy_survival": 120,
    "render_2": 1800, "path_reuse": 600, "kill_idle": 900, "kill_render": 1800, "runtime_restart": 1800,
    "render_after": 1800, "down": 300, "cleanup": 120, "generate_reference": 300,
    # full tier only
    "image": 3600, "sprites": 1800, "edit": 1800, "render_full": 7200,
}
SMOKE_PHASES = ("reference", "adopt", "up", "first_open", "doctor", "render_1", "source_change",
                "replace_host", "heavy_survival", "render_2", "path_reuse", "kill_idle", "kill_render",
                "runtime_restart", "render_after", "down", "cleanup")
TERMINAL_TASK_STATES = {"succeeded", "completed", "failed", "cancelled", "canceled", "expired"}
# Resource growth is behaviour (a leak), not time: these stay assertions.
DISK_BUDGET = 4 * 1024**3
RECEIPT_BUDGET = 20 * 1024**2
LOG_BUDGET = 100 * 1024**2
# The Runtime refuses work when free disk minus the task's estimate falls below this floor
# (runtime_protocol/store.py, ASTRID_RUNTIME_FREE_DISK_FLOOR_BYTES); the journey must not start below it.
DISK_FLOOR_ENV = "ASTRID_RUNTIME_FREE_DISK_FLOOR_BYTES"
DEFAULT_DISK_FLOOR = 4 * 1024**3
REMOTION_BACKEND, FFMPEG_BACKEND = "rendering.remotion", "rendering.ffmpeg"
BACKENDS = (REMOTION_BACKEND, FFMPEG_BACKEND)
# Expected scratch per second of the longest full-size render.  Remotion writes a frame sequence (the old
# comment here measured ~10 GiB for a 32 s full-HD window); ffmpeg streams.  These are estimates, not Runtime
# figures: the real ones come from the capability, which cannot be read before the Runtime is up.
SCRATCH_BYTES_PER_SECOND = {REMOTION_BACKEND: 10 * 1024**3 // 32, FFMPEG_BACKEND: 32 * 1024**2}
# Runtime lease length (runtime_protocol/store.py LEASE_SECONDS): a killed worker's task is given back only after it.
LEASE_SECONDS = 30
LEASE_MARGIN_SECONDS = 5
END_EVENTS = {"task.completed": {"completed", "succeeded"}, "task.failed": {"failed"},
              "task.cancelled": {"cancelled", "canceled"}}
GENERATED = "generated"
GENERATED_RANGE = (2.0, 6.0)  # inside the generated 12 s media-only timeline


class JourneyFailure(RuntimeError):
    """A phase failed.  ``kind`` is the outcome it reports: ``failure``, or ``hung`` (no exit within the ceiling)."""

    def __init__(self, phase: str, message: str, kind: str = "failure") -> None:
        super().__init__(f"{phase}: {message}")
        self.phase, self.kind = phase, kind


def _interrupt_journey(signum, _frame) -> None:
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, signal.SIG_IGN)
    raise JourneyFailure("interrupted", f"received {signal.Signals(signum).name}")


@contextmanager
def _journey_signals():
    previous = {sig: signal.signal(sig, _interrupt_journey) for sig in (signal.SIGTERM, signal.SIGINT)}
    try:
        yield
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def select_reference_realm(reference: Path) -> tuple[str, Path]:
    """Validate the stopped reference and return its realm; never copy it.

    `workspace adopt` clones the realm itself while holding the source's
    owner fence, so the journey doesn't clone a second time.
    """
    catalog = json.loads((reference / "runtime" / "catalog.json").read_text())
    realm_id = catalog.get("selected_realm_id")
    rows = catalog.get("realms") or []
    if not isinstance(realm_id, str) or len(rows) != 1 or rows[0].get("realm_id") != realm_id:
        raise JourneyFailure("reference", "reference must select exactly one realm")
    source = reference / "runtime" / "realms" / realm_id
    if (source.is_symlink() or not source.resolve().is_relative_to(reference)
            or source.resolve() != Path(rows[0]["data_root"]).resolve()
            or not (source / "realm.sqlite3").is_file()):
        raise JourneyFailure("reference", "catalog realm is outside the reference or has no database")
    return realm_id, source


def _ps_rows() -> list[dict[str, Any]]:
    ps = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,command="], capture_output=True, text=True, timeout=8)
    if ps.returncode:
        raise JourneyFailure("cleanup", f"ps failed: {ps.stderr.strip()}")
    result: list[dict[str, Any]] = []
    for line in ps.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) != 4:
            continue
        pid, ppid, pgid, command = parts
        if pid.isdigit() and ppid.isdigit() and pgid.isdigit():
            result.append({"pid": int(pid), "ppid": int(ppid), "pgid": int(pgid), "command": command})
    return result


def _processes(root: Path) -> list[dict[str, Any]]:
    rows = _ps_rows()
    owned = {row["pid"] for row in rows if str(root) in row["command"] and
             any(token in row["command"] for token in ("runtime_protocol", "generic_host", "node"))}
    while True:
        expanded = owned | {row["pid"] for row in rows if row["ppid"] in owned}
        if expanded == owned:
            break
        owned = expanded
    return [row for row in rows if row["pid"] in owned]


def _reap_owned_groups(root: Path) -> list[dict[str, Any]]:
    """Signal only groups whose every listed member is rooted in our temp realm."""
    for signum in (signal.SIGTERM, signal.SIGKILL):
        rows = _processes(root)
        if not rows:
            return []
        all_ps = _ps_rows()
        groups = {row["pgid"] for row in rows}
        safe = set(groups)
        owned_pids = {row["pid"] for row in rows}
        for row in all_ps:
            if row["pgid"] in groups and row["pid"] not in owned_pids:
                safe.discard(row["pgid"])
        for group in safe:
            if group != os.getpgrp():
                try:
                    os.killpg(group, signum)
                except ProcessLookupError:
                    pass
        if wait_for(lambda: not _processes(root), 5):
            return []
    return _processes(root)


def _files(root: Path):
    """Files under root; directories the host removes while we walk (attempt scratch) are skipped, not errors."""
    for folder, _dirs, names in os.walk(root):
        for name in names:
            path = Path(folder) / name
            if path.is_file():
                yield path


def _tree_bytes(root: Path, predicate) -> int:
    total = 0
    for path in _files(root):
        if predicate(path):
            try:
                total += path.stat().st_size
            except FileNotFoundError:
                pass
    return total


def machine_load() -> dict[str, Any]:
    """1-minute load and (macOS) memory pressure, recorded beside each phase's duration."""
    load = round(os.getloadavg()[0], 2)
    pressure = None
    if sys.platform == "darwin":
        try:
            level = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"], capture_output=True,
                                   text=True, timeout=5, check=False).stdout.strip()
            pressure = {"1": "normal", "2": "warn", "4": "critical"}.get(level, level or None)
        except (OSError, subprocess.SubprocessError):
            pressure = None
    return {"load_1m": load, "memory_pressure": pressure}


# -- child environment ------------------------------------------------------------------------
# Variables the journey must not hand to any child: the ones it replaces itself, plus the loader and
# interpreter overrides Remotion validation refuses (remotion_runtime.probe_context lists them inline;
# the Python-startup set and the interactive-Git allowlist are imported from there).
_STRIPPED_ENV = frozenset({"ASTRID_NODE_EXECUTABLE", "ASTRID_TIMELINE_SCHEMA_PYTHONPATH", "OTTO_HEAVY_LEASE"})
_OVERRIDE_ENV = frozenset({"NODE_OPTIONS", "NODE_PATH", "NODE_ICU_DATA", "OPENSSL_CONF", "PYTHONHOME",
                           "PYTHONEXECUTABLE", "__PYVENV_LAUNCHER__"}) | _UNSUPPORTED_PYTHON_STARTUP
_STRIPPED_PREFIXES = ("ASTRID_REMOTION_", "ASTRID_RENDER_", "LD_", "DYLD_")


def scrub_child_env(environ: Mapping[str, str]) -> dict[str, str]:
    """``environ`` without anything Remotion validation would fail closed on (used for every child)."""
    def keep(key: str) -> bool:
        if key in _STRIPPED_ENV or key in _OVERRIDE_ENV or key.startswith(_STRIPPED_PREFIXES):
            return False
        return not (key.startswith("GIT_") and key not in _INTERACTIVE_GIT_ENV)
    return {key: value for key, value in environ.items() if keep(key)}


# -- render backend -------------------------------------------------------------------------
def review_supported(backend: str) -> bool:
    """Only the Remotion backend renders ``--review`` (the ffmpeg backend takes ``--range`` but not review)."""
    return backend == REMOTION_BACKEND


def render_argv(astrid: Sequence[str], timeline: str, project: str, name: str, *, backend: str,
                window: tuple[float, float] | None = None, review: bool = False, detach: bool = False,
                timeout: float | None = None) -> list[str]:
    argv = [*astrid, "timelines", "render", timeline, "--project", project]
    if window is not None:
        argv += ["--range", str(window[0]), str(window[1])]
    argv += ["--backend", backend, "--output-name", name]
    if review and review_supported(backend):
        argv.append("--review")
    if detach:
        argv.append("--detach")
    else:
        argv += ["--wait", *(["--timeout-seconds", str(timeout)] if timeout else [])]
    return [*argv, "--json"]


# -- disk preflight -------------------------------------------------------------------------
def runtime_disk_floor(environ: Mapping[str, str]) -> int:
    """The Runtime's free-disk floor, read the way the Runtime reads it."""
    raw = environ.get(DISK_FLOOR_ENV)
    if raw is None:
        return DEFAULT_DISK_FLOOR
    try:
        floor = int(raw)
    except ValueError:
        floor = -1
    if floor < 0:
        raise JourneyFailure("preflight", f"{DISK_FLOOR_ENV} must be a nonnegative integer, got {raw!r}")
    return floor


def expected_render_scratch(backend: str, seconds: float) -> int:
    return int(SCRATCH_BYTES_PER_SECOND[backend] * max(0.0, seconds))


def _gib(count: int) -> str:
    return f"{count / 1024**3:.2f} GiB"


def disk_preflight(free: int, floor: int, scratch: int, where: Path) -> dict[str, Any]:
    """Refuse to start when free disk cannot hold the Runtime floor plus one render's scratch."""
    report = {"path": str(where), "free_bytes": free, "runtime_floor_bytes": floor,
              "expected_render_scratch_bytes": scratch, "required_bytes": floor + scratch}
    if free < floor + scratch:
        raise JourneyFailure("preflight", f"free disk {_gib(free)} at {where} is below the Runtime floor {_gib(floor)} "
                                          f"+ expected render scratch {_gib(scratch)} = {_gib(floor + scratch)}")
    return report


# -- revisions ------------------------------------------------------------------------------
def git_revision(path: Path) -> dict[str, Any]:
    """HEAD (and whether the tree has uncommitted changes) of a checkout; never raises."""
    env = scrub_child_env(os.environ)
    def git(*args: str) -> str:
        done = subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True, timeout=30, env=env, check=False)
        if done.returncode:
            raise OSError(done.stderr.strip() or f"git {args[0]} exit {done.returncode}")
        return done.stdout.strip()
    try:
        return {"path": str(path), "head": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain"))}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"path": str(path), "head": None, "error": str(exc)[:300]}


def manifest_version(path: Path) -> str | None:
    """The ``version`` of an artifacts.json manifest, or None when absent or unreadable."""
    try:
        version = json.loads(path.read_text()).get("version")
    except (OSError, ValueError, AttributeError):
        return None
    return version if isinstance(version, str) else None


def runtime_checkout_path() -> Path:
    spec = importlib.util.find_spec("runtime_protocol")
    if spec is None or spec.origin is None:
        raise JourneyFailure("reference", "runtime_protocol is not importable from this environment")
    return Path(spec.origin).resolve().parents[1]


def collect_revisions(astrid: Path, runtime: Path, app: Path | None) -> dict[str, Any]:
    """Every revision the run depends on, so a result can be tied to the exact trees it tested."""
    return {
        "astrid": {**git_revision(astrid), "manifest_version": manifest_version(astrid / "artifacts.json")},
        "runtime": {**git_revision(runtime), "manifest_version": manifest_version(runtime / "contract" / "artifacts.json")},
        "app": git_revision(app) if app is not None else None,
    }


# -- the Runtime's HTTP surface (what the App talks to) ---------------------------------------
def read_runtime_access(data_root: Path) -> tuple[str, str]:
    """Endpoint from ``runtime/discovery.json`` and the Astrid token from ``credentials/astrid.json``."""
    try:
        endpoint = json.loads((data_root / "runtime" / "discovery.json").read_text())["endpoint"]
        token = json.loads((data_root / "credentials" / "astrid.json").read_text())["token"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise JourneyFailure("runtime_access", f"no running Runtime endpoint/credential under {data_root}: {exc}") from exc
    return str(endpoint).rstrip("/"), str(token)


def runtime_request(endpoint: str, method: str, path: str, *, token: str | None = None, body: Any = None,
                    headers: Mapping[str, str] | None = None, timeout: float = 30.0) -> Any:
    """One JSON request to the Runtime; any non-2xx answer is a failure that carries its body."""
    sent = dict(headers or {})
    if token and "Authorization" not in sent:
        sent["Authorization"] = f"Bearer {token}"
    data = None if body is None else json.dumps(body, separators=(",", ":")).encode()
    request = urllib.request.Request(endpoint + path, data=data, headers=sent, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - loopback endpoint from discovery.json
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise JourneyFailure("runtime_request", f"{method} {path}: HTTP {exc.code}: {exc.read()[:500].decode(errors='replace')}") from exc
    except (urllib.error.URLError, OSError) as exc:
        raise JourneyFailure("runtime_request", f"{method} {path}: {exc}") from exc
    return json.loads(raw) if raw else None


def find_ready_capability(items: Iterable[Mapping[str, Any]], capability_id: str) -> Mapping[str, Any] | None:
    return next((c for c in items if c.get("capability_id") == capability_id and c.get("status") == "ready"), None)


def build_app_render_admission(*, project: str, timeline_id: str, output_name: str, capability: Mapping[str, Any],
                               token: str, backend: str = REMOTION_BACKEND, expected_version: int | None = None,
                               destination: str = "download") -> dict[str, Any]:
    """The request the App sends to render a timeline (astrid-app ``enqueueAstridRuntimeRenderTimeline``).

    ``capability`` is the ``rendering.render`` row from ``GET /v1/capabilities``: the App takes both the
    digest and the storage estimate from it and invents neither.
    """
    version = "head" if expected_version is None else expected_version
    params = {"timeline_ref": timeline_id, **({} if expected_version is None else {"expected_version": expected_version}),
              "selector": backend, "output_name": output_name}
    return {
        "method": "POST", "path": "/v1/tasks",
        "headers": {"Content-Type": "application/json",
                    "Idempotency-Key": f"astrid.render:v1:{timeline_id}:{version}:{destination}:{output_name}",
                    "Authorization": f"Bearer {token}"},
        "body": {
            "project": project, "capability_id": capability["capability_id"],
            "capability_digest": capability["definition_digest"], "schema_version": "1", "input_object_ids": [],
            "spec": {"family": capability["capability_id"], "params": params,
                     "output_policy": {"format": "mp4", "destination": destination, "filename": output_name}},
            "storage_estimate": {"scratch_bytes": capability["estimated_scratch_bytes"],
                                 "output_bytes": capability["estimated_output_bytes"]},
            "settlement_effect": {},
        },
    }


def task_events(endpoint: str, token: str, task_id: str) -> list[dict[str, Any]]:
    """Every event of a task's run, oldest first (``GET /v1/tasks/{id}/events``, paged)."""
    events: list[dict[str, Any]] = []
    cursor = None
    while True:
        query = "?limit=200" + (f"&cursor={cursor}" if cursor else "")
        page = runtime_request(endpoint, "GET", f"/v1/tasks/{task_id}/events{query}", token=token)
        events += page["items"]
        cursor = page.get("next_cursor")
        if not cursor:
            return events


def evaluate_killed_task_events(events: Sequence[Mapping[str, Any]], *, task_id: str | None = None,
                                final_state: str | None = None) -> dict[str, Any]:
    """Judge a task whose worker was killed mid-attempt: its lease must have expired, and it must
    then have reached exactly one end state (completed, failed or cancelled), after that expiry."""
    mine = sorted((e for e in events if task_id is None or e.get("aggregate_id") in (task_id, None)),
                  key=lambda e: int(e["sequence"]))
    kinds = [e["event_type"] for e in mine]
    expired = [e for e in mine if e["event_type"] == "task.lease_expired"]
    ends = [e for e in mine if e["event_type"] in END_EVENTS]
    if not expired:
        raise JourneyFailure("kill_render", f"killed task has no task.lease_expired event: {kinds}")
    if len(ends) != 1:
        raise JourneyFailure("kill_render", f"killed task must reach exactly one end state, saw {len(ends)}: {kinds}")
    if int(ends[0]["sequence"]) < int(expired[0]["sequence"]):
        raise JourneyFailure("kill_render", f"killed task ended before its lease expired: {kinds}")
    end = ends[0]["event_type"]
    if final_state is not None and final_state not in END_EVENTS[end]:
        raise JourneyFailure("kill_render", f"task state {final_state!r} contradicts its end event {end}")
    return {"lease_expired": len(expired), "end_event": end, "events": kinds}


def lease_snapshot(task: Mapping[str, Any]) -> dict[str, Any]:
    """What a task document exposes of its current attempt (the lease id itself is a worker secret)."""
    return {key: task.get(key) for key in ("state", "attempt_id", "lease_fence", "lease_expires_at")}



def tree_bytes(path: Path) -> int:
    """Bytes the journey's own tree occupies (lstat sizes; files that vanish mid-walk count as gone)."""
    total = 0
    for directory, _names, files in os.walk(path):
        for name in files:
            try:
                total += os.lstat(os.path.join(directory, name)).st_size
            except OSError:
                pass
    return total


class Runner:
    def __init__(self, root: Path, summary: Path, tier: str = "smoke") -> None:
        self.root, self.summary, self.tier = root, summary, tier
        self.started = time.monotonic()
        self.loads: dict[str, dict[str, Any]] = {}
        self.disk_high_water = 0
        self.phases: dict[str, float] = {}
        self.details: dict[str, Any] = {}

    def sample(self) -> None:
        # The journey's own footprint, not the volume's free-space delta: that also counts every other
        # process on a shared Mac (builds, other suites) over a run of many minutes.
        used = tree_bytes(self.root)
        self.disk_high_water = max(self.disk_high_water, used)
        if self.disk_high_water > DISK_BUDGET:
            raise JourneyFailure("disk_budget", f"high water {self.disk_high_water} > {DISK_BUDGET} bytes")

    def phase(self, name: str, operation):
        started = time.monotonic()
        try:
            result = operation()
            self.sample()
        except JourneyFailure:
            raise
        except Exception as exc:
            raise JourneyFailure(name, str(exc)) from exc
        finally:
            elapsed = time.monotonic() - started
            self.phases[name] = round(elapsed, 3)
            self.loads[name] = machine_load()
        return result

    def command(self, phase: str, argv: list[str], env: dict[str, str], *, json_result: bool = True):
        process = subprocess.Popen(argv, cwd=Path(__file__).resolve().parents[3], env=scrub_child_env(env),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   start_new_session=True)
        hang_limit = HANG_SECONDS[phase]
        deadline = time.monotonic() + hang_limit
        try:
            while True:
                try:
                    out, err = process.communicate(timeout=min(1, max(0.1, deadline - time.monotonic())))
                    break
                except subprocess.TimeoutExpired:
                    self.sample()
                    if time.monotonic() >= deadline:
                        raise JourneyFailure(phase, f"command hung (no exit after {hang_limit}s): {argv!r}", kind="hung")
        finally:
            if process.poll() is None:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
        if process.returncode:
            # Both streams: stderr may hold only progress diagnostics while the refusal is on stdout.
            told = [f"{label}: {text.strip()[-1500:]}" for label, text in (("stderr", err), ("stdout", out)) if text and text.strip()]
            raise JourneyFailure(phase, f"exit {process.returncode}: " + (" | ".join(told) or "no output"))
        if not json_result:
            return out
        try:
            value = parse_json_output(out)
        except json.JSONDecodeError as exc:
            raise JourneyFailure(phase, f"invalid JSON: {out[-1000:]}") from exc
        if isinstance(value, dict) and value.get("ok") is False:
            raise JourneyFailure(phase, str(value.get("error") or value))
        return value

    def write_summary(self, *, error: str | None = None, outcome: str | None = None) -> None:
        elapsed = round(time.monotonic() - self.started, 3)
        outcome = outcome or ("success" if error is None else "failure")
        payload = {"ok": error is None, "outcome": outcome, "error": error, "phase_seconds": self.phases, "phase_load": self.loads,
                   "total_seconds": elapsed, "disk_high_water_bytes": self.disk_high_water,
                   "limits": {"hang_seconds": HANG_SECONDS, "tier": self.tier,
                               "disk_bytes": DISK_BUDGET, "receipts_bytes": RECEIPT_BUDGET,
                               "logs_bytes": LOG_BUDGET}, **self.details}
        self.summary.parent.mkdir(parents=True, exist_ok=True)
        self.summary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        lines = [f"astrid dev journey ({self.tier}): {'PASS' if error is None else 'FAIL'} ({outcome})", f"Total: {elapsed}s"]
        for name, seconds in self.phases.items():
            load = self.loads.get(name) or {}
            lines.append(f"{name}: {seconds}s (load {load.get('load_1m', '?')}, memory {load.get('memory_pressure', '?')})")
        lines += [f"Disk high water: {self.disk_high_water} / {DISK_BUDGET} bytes",
                  f"Receipts: {self.details.get('receipts_bytes', '?')} / {RECEIPT_BUDGET} bytes",
                  f"Logs: {self.details.get('logs_bytes', '?')} / {LOG_BUDGET} bytes"]
        for name, revision in (self.details.get("revisions") or {}).items():
            if revision:
                lines.append(f"{name}: {revision.get('head')}{' (dirty)' if revision.get('dirty') else ''}"
                             + (f" manifest {revision['manifest_version']}" if revision.get("manifest_version") else ""))
        if error:
            lines.append(error)
        self.summary.with_suffix(".txt").write_text("\n".join(lines) + "\n")


def renderer_install_problem(project: Path) -> str | None:
    """Why the checkout's Remotion project cannot render yet, or ``None``.

    The source launcher only binds installed projects. Check before starting the
    journey so a missing install is reported before Runtime and the host launch.
    """
    from astrid.core.rendering.remotion_runtime import remotion_install_problem

    return remotion_install_problem(project)


def _doctor_ready(value: dict[str, Any]) -> bool:
    """Doctor must call the runtime healthy and the pack host's renderer Node usable."""
    if value.get("ok") is False or value.get("healthy") is False:
        return False
    return (value.get("renderer_node") or {}).get("status") == "ok"


def parse_json_output(out: str) -> Any:
    """Parse stdout as one JSON document, tolerating a text preamble (output may be large)."""
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        starts = [0] + [i + 1 for i, ch in enumerate(out) if ch == "\n" and out[i + 1:i + 2] == "{"]
        for start in starts:
            try:
                return json.JSONDecoder().raw_decode(out[start:])[0]
            except json.JSONDecodeError:
                continue
        raise


def find_run_id(value: Any) -> str | None:
    """First 32-hex ``run_id`` anywhere in a result document."""
    stack = [value]
    while stack:
        item = stack.pop(0)
        if isinstance(item, dict):
            run_id = item.get("run_id")
            if isinstance(run_id, str) and len(run_id) == 32 and all(c in "0123456789abcdef" for c in run_id):
                return run_id
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return None


def descendants(rows: list[dict[str, Any]], pid: int) -> list[dict[str, Any]]:
    """Every process below ``pid`` in the ps table."""
    owned = {pid}
    while True:
        grown = owned | {row["pid"] for row in rows if row["ppid"] in owned}
        if grown == owned:
            break
        owned = grown
    return [row for row in rows if row["pid"] in owned and row["pid"] != pid]


RENDER_MARKERS = ("remotion", "chrome", "ffmpeg")


def render_processes(rows: list[dict[str, Any]], host_pid: int) -> list[dict[str, Any]]:
    """The host's render work: descendants that are Remotion, a headless browser or ffmpeg."""
    return [row for row in descendants(rows, host_pid)
            if any(marker in row["command"].lower() for marker in RENDER_MARKERS)]


def with_duplicate_path(path: str) -> str:
    """A PATH whose every entry appears twice (what a nested shell profile produces)."""
    return os.pathsep.join([path, path]) if path else path


def read_host(root: Path) -> dict[str, Any]:
    try:
        return json.loads((root / "data" / "runtime" / "generic-host.json").read_text())
    except (OSError, ValueError):
        return {}


def pid_alive(pid: int | None) -> bool:
    if not isinstance(pid, int):
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    state = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return bool(state) and not state.startswith("Z")


def wait_for(predicate, seconds: float, interval: float = 0.2):
    deadline = time.monotonic() + seconds
    while True:
        value = predicate()
        if value:
            return value
        if time.monotonic() >= deadline:
            return value
        time.sleep(interval)


def _find_output(root: Path, name: str, *, exclude: set[Path] | None = None) -> Path:
    matches = [path for path in _files(root) if path.name.endswith(name) and path not in (exclude or set())]
    if len(matches) != 1:
        raise JourneyFailure("render", f"expected one {name} under temp root, found {len(matches)}")
    return matches[0]


def _duration(path: Path, runner: Runner, env: dict[str, str], phase: str) -> float:
    out = runner.command(phase, ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=noprint_wrappers=1:nokey=1", str(path)], env, json_result=False)
    return float(out.strip())




OPEN_CLIENT = "from astrid.sdk import AstridClient\nwith AstridClient.open_from_launcher():\n    pass\n"
IMAGE_PROMPT = (
    "A single pixel-art sticker: a small handheld bug-catching net that has just caught one tiny, friendly "
    "glowing beetle. Retro 16-bit game sprite, about 44 pixels wide, every pixel a perfect square of identical "
    "size, crisp 1-pixel dark charcoal (#22211E) outline, limited palette: warm cream #F3EEE4, bright orange "
    "#FF7A2E, a little soft yellow for the beetle's glow. No anti-aliasing, no gradients, no text. "
    "Centered on a flat, perfectly uniform pure magenta (#FF00FF) background for chroma keying."
)
HEAVY_LAUNCHER = Path.home() / "Developer" / "otto-claude-host" / "bin" / "otto-heavy"


def _sdk_script(body: str) -> str:
    return "import json\nfrom astrid.sdk import AstridClient\n" + body


def _invoke_script(capability: str, kind: str, project: str, inputs: dict[str, Any]) -> str:
    return _sdk_script(
        "with AstridClient.open_from_launcher() as client:\n"
        f"    result = client.invoke_result({capability!r}, kind={kind!r}, project={project!r}, inputs={inputs!r}, wait=True)\n"
        "    print(json.dumps({'ok': result.ok, 'run_id': getattr(result, 'run_id', None), "
        "'error': str(getattr(result, 'error', None) or '')}, default=str))\n")


class Journey:
    """One disposable-realm journey; each method is a phase body or a pure helper for it."""

    def __init__(self, *, runner: Runner, root: Path, env: dict[str, str], project: str, timeline: str,
                 start: float, end: float, kill_start: float, checkout: Path, backend: str = REMOTION_BACKEND,
                 restart_argv: list[str] | None = None, app_render: bool = True) -> None:
        self.r, self.root, self.env, self.project, self.timeline = runner, root, env, project, timeline
        self.start, self.end, self.kill_start, self.checkout = start, end, kill_start, checkout
        self.backend, self.restart_argv, self.app_render = backend, restart_argv or [], app_render
        self.astrid = [sys.executable, "-m", "astrid"]

    # -- helpers --------------------------------------------------------------------------
    def open_client(self, phase: str, *, env: dict[str, str] | None = None, heavy: bool = False) -> None:
        argv = [sys.executable, "-c", OPEN_CLIENT]
        use = dict(env or self.env)
        if heavy:
            # A fresh capacity lease around the client: the host it starts must outlive the job.
            use.pop("OTTO_HEAVY_LEASE", None)
            use.pop("OTTO_HEAVY_CAPACITY", None)
            lease_root = self.root / "heavy-lease"
            lease_root.mkdir(exist_ok=True)
            (lease_root / "capacity").write_text("1\n")
            use["OTTO_HEAVY_DIR"] = str(lease_root)
            argv = [str(HEAVY_LAUNCHER), "--weight", "1", "--purpose", "astrid dev journey: host start inside a job",
                    "--max-minutes", "3", "--"] + argv
        self.r.command(phase, argv, use, json_result=False)

    def host_pid(self, phase: str) -> int:
        pid = read_host(self.root).get("pid")
        if not isinstance(pid, int):
            raise JourneyFailure(phase, f"no pack host recorded in {self.root / 'data' / 'runtime' / 'generic-host.json'}")
        return pid

    def rooted_host(self, phase: str) -> int:
        """The pid our private Runtime recorded, only if it is alive and really a pack host."""
        pid = self.host_pid(phase)
        if not any(row["pid"] == pid and "generic_host" in row["command"] for row in _ps_rows()):
            raise JourneyFailure(phase, f"recorded host pid {pid} is not a running pack host; refusing to signal it")
        return pid

    def render(self, phase: str, tag: str, start: float, end: float, *, detach: bool = False,
               review: bool = False) -> tuple[Any, str]:
        name = f"v6-{tag}-{uuid.uuid4().hex[:8]}.mp4"
        argv = render_argv(self.astrid, self.timeline, self.project, name, backend=self.backend, window=(start, end),
                           review=review, detach=detach, timeout=None if detach else HANG_SECONDS[phase])
        return self.r.command(phase, argv, self.env), name

    def excerpt(self, phase: str, tag: str, ids: list[str]) -> None:
        result, name = self.render(phase, tag, self.start, self.end)
        data = result.get("data") or {}
        task_id = data.get("kernel_task_id")
        if not task_id or task_id in ids or data.get("state") not in ("completed", "succeeded"):
            raise JourneyFailure(phase, f"no distinct completed task: {data}")
        ids.append(task_id)
        output = _find_output(self.root / "data", name)
        seconds = _duration(output, self.r, self.env, phase)
        want = self.end - self.start
        if abs(seconds - want) > 0.5:
            raise JourneyFailure(phase, f"{output} duration {seconds}s, expected {want}s +-0.5")
        # The task scope removes its attempt scratch just after the task settles, so allow it a moment.
        def frames() -> list[Path]:
            return [p for p in _files(self.root / "tmp") if p.suffix in (".png", ".jpg")]
        if not wait_for(lambda: not frames(), 10):
            raise JourneyFailure(phase, f"frame-sequence files remain in TMPDIR: {[str(p) for p in frames()[:3]]}")
        self.r.details[phase] = {"task_id": task_id, "output_bytes": output.stat().st_size, "duration_seconds": seconds}

    # -- recovery phases ------------------------------------------------------------------
    def replace_host(self, old: int) -> int:
        """After a source change the idle outdated host is replaced by the next client open, unattended."""
        if HEAVY_LAUNCHER.exists():
            self.open_client("replace_host", heavy=True)
            self.r.details["replace_host_in_heavy_job"] = True
        else:
            self.open_client("replace_host")
            self.r.details["replace_host_in_heavy_job"] = False
        new = self.host_pid("replace_host")
        if new == old:
            raise JourneyFailure("replace_host", f"outdated host {old} was not replaced after a source change")
        if not wait_for(lambda: not pid_alive(old), 15):
            raise JourneyFailure("replace_host", f"outdated host {old} is still running")
        if not pid_alive(new):
            raise JourneyFailure("replace_host", f"replacement host {new} is not running")
        return new

    def survives_job(self, new: int) -> None:
        time.sleep(3)  # an end-of-job sweep would run about now
        if not pid_alive(new) or read_host(self.root).get("pid") != new:
            raise JourneyFailure("heavy_survival", f"host {new} did not outlive the capacity job that started it")

    def path_reuse(self, host: int) -> None:
        env = dict(self.env, PATH=with_duplicate_path(self.env.get("PATH", "")))
        self.open_client("path_reuse", env=env)
        if read_host(self.root).get("pid") != host or not pid_alive(host):
            raise JourneyFailure("path_reuse", f"a duplicated PATH made the client replace or refuse host {host}")

    def kill_idle(self) -> int:
        old = self.rooted_host("kill_idle")
        os.kill(old, signal.SIGKILL)
        if not wait_for(lambda: not pid_alive(old), 10):
            raise JourneyFailure("kill_idle", f"host {old} survived SIGKILL")
        self.open_client("kill_idle")
        new = self.host_pid("kill_idle")
        if new == old or not pid_alive(new):
            raise JourneyFailure("kill_idle", f"client open did not recover with a new host (old {old}, now {new})")
        return new

    def runtime_get(self, path: str) -> Any:
        endpoint, token = read_runtime_access(self.root / "data")
        return runtime_request(endpoint, "GET", path, token=token)

    def kill_render(self) -> int:
        host = self.rooted_host("kill_render")
        # A review-size render (Remotion only; ffmpeg has no review mode): this phase proves crash custody,
        # not output fidelity, and a full-HD 32 s window needs ~10 GiB of scratch (the Runtime rightly
        # refuses it on a nearly full disk).
        result, _name = self.render("kill_render", "killed", self.kill_start, self.end, detach=True, review=True)
        task_id = (result.get("data") or {}).get("kernel_task_id") if isinstance(result, dict) else None
        if not task_id:
            raise JourneyFailure("kill_render", f"the killed render returned no task id: {result}")
        found = wait_for(lambda: render_processes(_ps_rows(), host), 90)
        if not found:
            raise JourneyFailure("kill_render", f"no render processes appeared under host {host} (render finished too early or never started): {result}")
        pids = sorted({row["pid"] for row in found} | {row["pid"] for row in descendants(_ps_rows(), host)})
        before_kill = lease_snapshot(self.runtime_get(f"/v1/tasks/{task_id}"))
        os.kill(host, signal.SIGKILL)
        killed_at = time.monotonic()
        if not wait_for(lambda: not pid_alive(host), 10):
            raise JourneyFailure("kill_render", f"host {host} survived SIGKILL")
        journal = self.root / "data" / "runtime" / "generic-host.task-scopes.json"
        self.r.details["task_scope_journal_bytes"] = journal.stat().st_size if journal.exists() else None
        self.open_client("kill_render")
        new = self.host_pid("kill_render")
        if new == host or not pid_alive(new):
            raise JourneyFailure("kill_render", f"no new host after killing {host}")
        survivors = wait_for(lambda: not [p for p in pids if pid_alive(p) and p != new], 20)
        if not survivors:
            raise JourneyFailure("kill_render", f"orphaned render processes survived the next host start: {[p for p in pids if pid_alive(p)]}")
        self.r.details["reaped_orphan_pids"] = pids
        # The killed task must not be stranded: once its 30 s lease has run out, a read gives it back
        # (task.lease_expired, requeued, maybe re-run by the new host).  Then cancel it if it is still open
        # and see it settle, so later phases start from an idle realm.
        lease_wait = killed_at + LEASE_SECONDS + LEASE_MARGIN_SECONDS - time.monotonic()
        if lease_wait > 0:
            time.sleep(lease_wait)
        self.runtime_get(f"/v1/tasks/{task_id}")  # reads reap overdue leases
        self.r.details["killed_task_after_recovery"] = self.task_state(task_id)
        if self.r.details["killed_task_after_recovery"] not in TERMINAL_TASK_STATES:
            self.r.command("kill_render", self.astrid + ["tasks", "cancel", task_id, "--project", self.project, "--json"], self.env)
        if not wait_for(lambda: self.task_state(task_id) in TERMINAL_TASK_STATES, HANG_SECONDS["kill_render"], interval=2):
            raise JourneyFailure("kill_render", f"killed task {task_id} never settled: {self.task_state(task_id)}", kind="hung")
        final = self.task_state(task_id)
        self.r.details["killed_task_final"] = final
        endpoint, token = read_runtime_access(self.root / "data")
        self.r.details["killed_task_events"] = evaluate_killed_task_events(
            task_events(endpoint, token, task_id), task_id=task_id, final_state=final)
        # A publication under the pre-kill fence would be refused, but it needs the lease id, which only the
        # worker holds (the task document exposes attempt id and fence): record both fences instead.
        self.r.details["killed_task_lease"] = {
            "before_kill": before_kill, "after_settle": lease_snapshot(self.runtime_get(f"/v1/tasks/{task_id}")),
            "stale_fence_publication": "not exercised: the lease id is not readable through the task API"}
        return new

    def runtime_restart(self) -> None:
        """Restart the Runtime under a running pack host, then render as the App does, with no client open."""
        self.r.details["runtime_restart"] = {"host_before": read_host(self.root).get("pid")}
        self.r.command("runtime_restart", self.restart_argv, self.env)
        if not self.app_render:
            self.r.details["runtime_restart"]["app_render"] = "skipped"
            return
        endpoint, token = read_runtime_access(self.root / "data")
        def ready():
            try:
                return find_ready_capability(runtime_request(endpoint, "GET", "/v1/capabilities?limit=200", token=token)["items"], "rendering.render")
            except JourneyFailure:
                return None  # the restarted Runtime is not answering yet
        capability = wait_for(ready, 120, interval=2)
        if not capability:
            raise JourneyFailure("runtime_restart", "rendering.render is not ready 120s after the Runtime restart")
        name = f"v6-app-{uuid.uuid4().hex[:8]}.mp4"
        admission = build_app_render_admission(project=self.project, timeline_id=self.timeline, output_name=name,
                                               capability=capability, token=token, backend=self.backend)
        admitted = runtime_request(endpoint, admission["method"], admission["path"], headers=admission["headers"], body=admission["body"])
        task_id = (admitted.get("data") or {}).get("task_id")
        if not task_id:
            raise JourneyFailure("runtime_restart", f"App-shaped admission returned no task: {admitted}")
        last: dict[str, Any] = {}
        def settled():
            last.update(runtime_request(endpoint, "GET", f"/v1/tasks/{task_id}", token=token))
            return last.get("state") in TERMINAL_TASK_STATES
        if not wait_for(settled, HANG_SECONDS["runtime_restart"], interval=2):
            raise JourneyFailure("runtime_restart", f"App-admitted render {task_id} did not settle (state {last.get('state')}); command hung", kind="hung")
        if last.get("state") not in ("completed", "succeeded"):
            raise JourneyFailure("runtime_restart", f"App-admitted render {task_id} ended {last.get('state')}: {last.get('result')}")
        self.r.details["runtime_restart"].update({"app_render_task": task_id, "app_render_state": last["state"],
                                                  "host_after": read_host(self.root).get("pid")})

    def task_state(self, task_id: str) -> str | None:
        shown = self.r.command("kill_render", self.astrid + ["tasks", "show", task_id, "--project", self.project, "--json"], self.env)
        data = shown.get("data") if isinstance(shown, dict) else None
        if isinstance(data, dict) and isinstance(data.get("task"), dict):
            data = data["task"]
        return data.get("state") if isinstance(data, dict) else None

    # -- full tier ------------------------------------------------------------------------
    def full(self, replace_slot: str, expect_duration: float | None) -> None:
        r = self.r
        image = r.phase("image", lambda: self._run_id(
            "image", _invoke_script("generation.generate_image", "executor", self.project,
                                    {"model": "flux-dev", "mode": "t2i", "execution": "codex", "prompt": IMAGE_PROMPT, "count": 1})))
        sprites = r.phase("sprites", lambda: self._run_id(
            "sprites", _invoke_script("pixel.sprites", "action", self.project,
                                      {"image": f"run:{image}/generated_images#0", "mode": "chroma", "scale": 5})))
        key = f"v6-{uuid.uuid4().hex[:8]}"
        def edit():
            base = self.astrid + ["timelines"]
            tl = ["--project", self.project]
            r.command("edit", base + ["checkout", self.timeline, *tl, "--draft", key, "--fresh", "--json"], self.env)
            r.command("edit", base + ["edit", self.timeline, *tl, "--replace-asset", f"{replace_slot}=run:{sprites}/sprites#0", "--json"], self.env)
            r.command("edit", base + ["check", self.timeline, *tl, "--no-sweep", "--json"], self.env)
            r.command("edit", base + ["publish", self.timeline, *tl, "-m", f"journey {key}", "--idempotency-key", key, "--json"], self.env)
        r.phase("edit", edit)
        def full_render():
            name = f"v6-full-{key}.mp4"
            r.command("render_full", render_argv(self.astrid, self.timeline, self.project, name, backend=self.backend,
                                                 review=True, timeout=HANG_SECONDS["render_full"]), self.env)
            output = _find_output(self.root / "data", name)
            seconds = _duration(output, r, self.env, "render_full")
            if seconds < 10 or (expect_duration is not None and abs(seconds - expect_duration) > 1.0):
                raise JourneyFailure("render_full", f"full render is {seconds}s (expected {expect_duration or '>= 10'})")
            r.details["render_full"] = {"output_bytes": output.stat().st_size, "duration_seconds": seconds,
                                        "image_run": image, "sprites_run": sprites}
        r.phase("render_full", full_render)

    def _run_id(self, phase: str, script: str) -> str:
        result = self.r.command(phase, [sys.executable, "-c", script], self.env)
        run_id = find_run_id(result)
        if not result.get("ok") or not run_id:
            raise JourneyFailure(phase, f"no successful run: {str(result)[:600]}")
        return run_id


@_journey_signals()
def run(reference: Path | None, timeline: str, summary: Path, *, tier: str = "smoke", start: float = 144.0, end: float = 152.0,
        replace_slot: str = "BUGNET", expect_duration: float | None = None, backend: str = REMOTION_BACKEND,
        app_checkout: Path | None = None, app_render: bool = True) -> int:
    """Run the journey; ``reference=None`` generates a small reference (``--reference generated``)."""
    if backend not in BACKENDS:
        raise JourneyFailure("preflight", f"backend must be one of {', '.join(BACKENDS)}")
    if reference is not None:
        reference = reference.resolve(strict=True)
    summary = summary.resolve()
    if reference is not None and summary.is_relative_to(reference):
        raise JourneyFailure("preflight", "summary must be outside the reference")
    if "/" not in timeline:
        raise JourneyFailure("preflight", "timeline must be PROJECT/TIMELINE")
    project, source_timeline = timeline.split("/", 1)
    if not project or not source_timeline:
        raise JourneyFailure("preflight", "timeline must be PROJECT/TIMELINE")
    if not 0 <= start < end:
        raise JourneyFailure("preflight", "excerpt needs 0 <= start < end")
    if app_checkout is not None and not app_checkout.is_dir():
        raise JourneyFailure("preflight", f"--app-checkout {app_checkout} is not a directory")
    checkout = Path(__file__).resolve().parents[3]
    if backend == REMOTION_BACKEND:
        # The pack host needs the renderer's pinned Node; find out now, not after a 40 s adopt.
        # (The journey drops ASTRID_NODE_EXECUTABLE below, so the host searches exactly as this does.)
        from astrid.core.rendering.node_pin import resolve_pinned_node
        node = resolve_pinned_node(checkout / "remotion", search_path=os.environ.get("PATH", ""))
        if not node.ok:
            raise JourneyFailure("preflight", node.problem or "no Node for the renderer")
        problem = renderer_install_problem(checkout / "remotion")
        if problem:
            raise JourneyFailure("preflight", problem)
    tmp_parent = Path(tempfile.gettempdir())
    disk = disk_preflight(shutil.disk_usage(tmp_parent).free, runtime_disk_floor(os.environ),
                          expected_render_scratch(backend, end - start), tmp_parent)
    # This module sits in the host's measured core source closure: appending a comment changes the
    # closure identity (an outdated host) without changing renderer behavior.
    source_probe = Path(__file__)
    original = source_probe.read_bytes()
    probe_bytes = original + b"\n# journey source-change probe\n"
    # macOS temp dirs live under /var -> /private/var; the Runtime refuses symlinked support paths.
    root = Path(tempfile.mkdtemp(prefix="astrid-v6-")).resolve()
    runner = Runner(root, summary, tier)
    runner.details.update({"backend": backend, "disk_preflight": disk})
    env = scrub_child_env(os.environ)
    env["ASTRID_RUNTIME_DATA_ROOT"] = str(root / "data")
    env["TMPDIR"] = str(root / "tmp")
    (root / "tmp").mkdir()
    changed = False
    adopt_attempted = False
    failure: str | None = None
    hung = False
    try:
        runtime_checkout = runtime_checkout_path()
        runner.details["revisions"] = collect_revisions(checkout, runtime_checkout, app_checkout)
        if reference is None:
            from astrid.core.dev.reference_realm import build_reference
            reference = runner.phase("generate_reference", lambda: build_reference(
                root / "generated", env=env, source_checkout=checkout, runtime_checkout=runtime_checkout,
                runtime_environment=sys.prefix).resolve())
        realm_id, reference_realm = runner.phase("reference", lambda: select_reference_realm(reference))
        manifest = json.loads((reference / "runtime" / "source-profiles" / "astrid.json").read_text())
        manifest["source_checkout"] = str(checkout)
        # Test the Runtime this interpreter imports, not the one the reference was adopted with.
        manifest["runtime_checkout"] = str(runtime_checkout)
        manifest["runtime_environment"] = sys.prefix
        manifest_path = root / "source-profile.json"
        manifest_path.write_text(json.dumps(manifest))
        env["ASTRID_RUNTIME_SOURCE_MANIFEST"] = str(manifest_path)
        local = [sys.executable, "-m", "astrid_runtime"]
        common = ["--profile", "astrid", "--data-root", str(root / "data"), "--json"]
        adopt_attempted = True
        runner.phase("adopt", lambda: runner.command("adopt", local + ["workspace", "adopt", "--from", str(reference_realm), "--realm-id", realm_id, "--source-manifest", str(manifest_path)] + common, env))
        runner.phase("up", lambda: runner.command("up", local + ["up", "--source-manifest", str(manifest_path)] + common, env))
        j = Journey(runner=runner, root=root, env=env, project=project, timeline=source_timeline,
                    start=start, end=end, kill_start=max(0.0, end - 32), checkout=checkout, backend=backend,
                    restart_argv=local + ["restart", "--source-manifest", str(manifest_path)] + common, app_render=app_render)
        # The render killed mid-way is a 32 s window ending where the excerpt ends: long enough to be
        # caught running, and inside the film (a window past the end is refused, as it should be).
        # The first client open starts the pack host, which resolves the renderer (no separate setup step).
        runner.phase("first_open", lambda: j.open_client("first_open"))
        doctor = runner.phase("doctor", lambda: runner.command("doctor", j.astrid + ["doctor", "--json"], env))
        if not _doctor_ready(doctor):
            raise JourneyFailure("doctor", f"not healthy: healthy={doctor.get('healthy')} issues={doctor.get('issues')} renderer_node={doctor.get('renderer_node')}")
        ids: list[str] = []
        runner.phase("render_1", lambda: j.excerpt("render_1", "1", ids))
        old_host = j.host_pid("source_change")
        def touch():
            nonlocal changed
            if source_probe.read_bytes() != original:
                raise JourneyFailure("source_change", "journey source changed concurrently; refusing to overwrite it")
            changed = True
            source_probe.write_bytes(probe_bytes)
        runner.phase("source_change", touch)
        host = runner.phase("replace_host", lambda: j.replace_host(old_host))
        runner.phase("heavy_survival", lambda: j.survives_job(host))
        runner.phase("render_2", lambda: j.excerpt("render_2", "2", ids))
        runner.phase("path_reuse", lambda: j.path_reuse(host))
        runner.phase("kill_idle", j.kill_idle)
        runner.phase("kill_render", j.kill_render)
        runner.phase("runtime_restart", j.runtime_restart)
        runner.phase("render_after", lambda: j.excerpt("render_after", "after", ids))
        runner.details["task_ids"] = ids
        if tier == "full":
            j.full(replace_slot, expect_duration)
    except Exception as exc:
        failure = str(exc)
        hung = getattr(exc, "kind", None) == "hung"
    finally:
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, signal.SIG_IGN)
        if changed:
            try:
                current = source_probe.read_bytes()
                if current == probe_bytes:
                    source_probe.write_bytes(original)
                elif current != original:
                    raise OSError("journey source changed concurrently; manual restore required")
            except OSError as exc:
                failure = (failure + "; " if failure else "") + f"source_change: {exc}"
        if adopt_attempted:
            try:
                runner.phase("down", lambda: runner.command("down", [sys.executable, "-m", "astrid_runtime", "down", "--source-manifest", str(manifest_path)] + common, env))
            except Exception as exc:
                failure = (failure + "; " if failure else "") + str(exc)
        try:
            leftovers = runner.phase("cleanup", lambda: _reap_owned_groups(root))
            if leftovers:
                failure = (failure + "; " if failure else "") + f"cleanup: rooted processes remain: {leftovers}"
        except Exception as exc:
            failure = (failure + "; " if failure else "") + str(exc)
        runner.details["receipts_bytes"] = _tree_bytes(root, lambda p: "receipt" in p.name.lower())
        runner.details["logs_bytes"] = _tree_bytes(root, lambda p: ".log" in p.name)
        if runner.details["receipts_bytes"] > RECEIPT_BUDGET or runner.details["logs_bytes"] > LOG_BUDGET:
            failure = (failure + "; " if failure else "") + "growth_budget: receipts or logs exceeded budget"
        if failure is not None:
            runner.details["evidence"] = _keep_failure_logs(root, summary)
        runner.write_summary(error=failure, outcome="hung" if failure is not None and hung else None)
        shutil.rmtree(root, ignore_errors=True)
    return 0 if failure is None else 1


EVIDENCE_TAIL_BYTES = 256 * 1024


def _keep_failure_logs(root: Path, summary: Path) -> str | None:
    """Before the disposable root goes, keep the tail of each runtime/host log beside the summary.

    Only ``*.log`` files under the data root's ``runtime`` directory are kept (never credentials or
    the realm), each cut to its last 256 KiB, so a failed run can still be diagnosed.
    """
    logs = sorted((root / "data" / "runtime").glob("*.log"))
    if not logs:
        return None
    target = summary.with_name(summary.stem + "-evidence")
    target.mkdir(parents=True, exist_ok=True)
    for log in logs:
        with log.open("rb") as stream:
            stream.seek(max(0, log.stat().st_size - EVIDENCE_TAIL_BYTES))
            (target / log.name).write_bytes(stream.read())
    return str(target)


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="astrid dev journey", description="Real-film journey in a disposable realm")
    parser.add_argument("--tier", choices=["smoke", "full"], required=True,
                        help="smoke: excerpt + host-lifecycle recovery (~4 min); full: smoke + Codex image, sprites, edit/publish, full render (~20 min)")
    parser.add_argument("--reference", required=True,
                        help=f"a stopped data root holding the film realm, or '{GENERATED}' to build a small one "
                             "(one project, 3 test clips, a media-only timeline; needs ffmpeg)")
    parser.add_argument("--timeline", default=None, help=f"PROJECT/TIMELINE (default for '{GENERATED}': journey/main)")
    parser.add_argument("--summary", type=Path, required=True, help="JSON summary path; adjacent .txt is also written")
    parser.add_argument("--range", nargs=2, type=float, metavar=("START", "END"), default=None,
                        help=f"excerpt window in seconds (default 144 152; {GENERATED_RANGE[0]:g} {GENERATED_RANGE[1]:g} for '{GENERATED}')")
    parser.add_argument("--backend", choices=BACKENDS, default=REMOTION_BACKEND,
                        help="renderer for every render; rendering.ffmpeg handles media-only timelines and skips the Node pin check and --review")
    parser.add_argument("--app-checkout", type=Path, default=None, help="astrid-app checkout whose HEAD is recorded in the summary")
    parser.add_argument("--skip-app-render", action="store_true",
                        help="runtime_restart restarts the Runtime but does not admit the App-shaped render (a full-film render on a real film)")
    parser.add_argument("--replace-slot", default="BUGNET", help="full tier: asset slot the generated sprite replaces")
    parser.add_argument("--expect-duration", type=float, default=None, help="full tier: expected full-film seconds (+-1)")
    parsed = parser.parse_args(args)
    generated = parsed.reference == GENERATED
    timeline = parsed.timeline or (f"{reference_realm.PROJECT_SLUG}/{reference_realm.TIMELINE_ID}" if generated else None)
    if timeline is None:
        parser.error("--timeline is required unless --reference generated")
    start, end = parsed.range or (GENERATED_RANGE if generated else (144.0, 152.0))
    try:
        status = run(None if generated else Path(parsed.reference), timeline, parsed.summary, tier=parsed.tier, start=start,
                     end=end, replace_slot=parsed.replace_slot, expect_duration=parsed.expect_duration,
                     backend=parsed.backend, app_checkout=parsed.app_checkout, app_render=not parsed.skip_app_render)
    except Exception as exc:
        summary = parsed.summary.resolve()
        summary.parent.mkdir(parents=True, exist_ok=True)
        summary.write_text(json.dumps({"ok": False, "outcome": "failure", "error": str(exc), "phase_seconds": {}}, indent=2) + "\n")
        summary.with_suffix(".txt").write_text(f"astrid dev journey ({parsed.tier}): FAIL (failure)\n{exc}\n")
        print(f"journey: {exc}", file=sys.stderr)
        return 1
    report = json.loads(parsed.summary.read_text())
    print(json.dumps(report, sort_keys=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
