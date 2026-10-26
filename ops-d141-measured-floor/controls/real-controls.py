#!/usr/bin/env python3
"""Run the private candidate through isolated, real subprocess controls.

The harness rewrites only the candidate's private orchestration/snapshot roots
in a temporary copy. It never calls --run, edits the live dispatcher tree, or
uses a live queue.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent
COMMAND = "python3 -c 'import time; time.sleep(6)'"
FAIL_COMMAND = "python3 -c 'import sys; sys.exit(7)'"
CANCEL_COMMAND = "python3 -c 'import time; time.sleep(20)'"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_df(path: Path, value: int | str) -> None:
    path.write_text(f"#!/bin/sh\nprintf '%s\\n' Avail\nprintf '%s\\n' {value}\n", encoding="utf-8")
    path.chmod(0o755)


def run_candidate(script: Path, root: Path, job: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(script), job], cwd=root, env=env, text=True, capture_output=True, timeout=30, check=False)


def source_identity(worktree: Path) -> tuple[str, str]:
    head = subprocess.check_output(["git", "-C", str(worktree), "rev-parse", "HEAD"], text=True).strip()
    tree = subprocess.check_output(["git", "-C", str(worktree), "rev-parse", "HEAD^{tree}"], text=True).strip()
    return head, tree


def witness(root: Path, job: str, role: str, value: int) -> tuple[str, str]:
    relative = f"tests/{job}/{role}.witness"
    path = root / relative
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    raw = f"Avail\n{value}\n".encode()
    path.write_bytes(raw)
    path.chmod(0o600)
    return relative, digest(raw)


def receipt(
    root: Path,
    job: str,
    repo: str,
    suite: str,
    worktree: Path,
    decision: str | None = None,
    growth: int = 0,
    command: str = COMMAND,
) -> None:
    head, tree = source_identity(worktree)
    source = {"head": head, "tree": tree, "command_sha256": digest(command.encode())}
    start, start_hash = witness(root, job, "start", 4_600_000_000 + growth)
    stop, stop_hash = witness(root, job, "stop", 4_600_000_000)
    value: dict[str, object] = {
        "schema": "timeline.d89d.measured-floor.v1",
        "trusted_manager_root": str(root),
        "manager_owner_uid": os.getuid(),
        "scope": {"job_id": job, "repo": repo, "suite": suite, "source": source},
        "measurement": {
            "growth_bytes": growth,
            "floor_bytes": max(4_600_000_000, 4_000_000_000 + growth + 200_000_000),
            "minimum_bytes": 4_600_000_000,
            "stop_bytes": 4_000_000_000,
            "margin_bytes": 200_000_000,
            "semantics": "start_end_bracket_delta_only_not_continuous_peak",
        },
        "witnesses": [
            {"role": "start", "path": start, "sha256": start_hash, "owner_uid": os.getuid(), "owner_gid": os.getgid()},
            {"role": "stop", "path": stop, "sha256": stop_hash, "owner_uid": os.getuid(), "owner_gid": os.getgid()},
        ],
    }
    if decision is not None:
        trace = {"path": f"tests/{job}/disk-trace.tsv", "sampling_seconds": 5, "format": "timeline.disk-trace.v1", "keep": True}
        record = {"schema": "timeline.d141.recorded-decision.v1", "decision": decision, "scope": value["scope"], "trace": trace}
        record_path = root / f"tests/{job}/d141-decision.json"
        record_path.write_text(json.dumps(record, separators=(",", ":")) + "\n", encoding="utf-8")
        record_path.chmod(0o600)
        value["authorization"] = {
            "decision": decision,
            "record_path": f"tests/{job}/d141-decision.json",
            "record_sha256": digest(record_path.read_bytes()),
        }
        value["trace"] = trace
        value["schema"] = "timeline.d141.measured-floor.v1"
    (root / f"tests/{job}/recorded-measured-floor.json").write_text(json.dumps(value, separators=(",", ":")) + "\n", encoding="utf-8")


def prepare() -> tuple[Path, Path, Path, dict[str, str]]:
    root = Path(tempfile.mkdtemp(prefix="d141-controls-", dir=os.environ.get("TMPDIR", "/tmp")))
    (root / "tests/cache").mkdir(mode=0o700, parents=True)
    (root / "tests").chmod(0o700)
    (root / "workers/body").mkdir(mode=0o700, parents=True)
    worktree = root / "worktree"
    subprocess.run(["git", "init", "-q", str(worktree)], check=True)
    subprocess.run(["git", "-C", str(worktree), "config", "user.email", "controls@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(worktree), "config", "user.name", "D141 controls"], check=True)
    (worktree / "body.txt").write_text("isolated\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(worktree), "add", "body.txt"], check=True)
    subprocess.run(["git", "-C", str(worktree), "-c", "commit.gpgSign=false", "commit", "-qm", "fixture"], check=True)
    (root / "workers/body/meta").write_text(f"worktree={worktree}\n", encoding="utf-8")
    (root / "tests/suites.conf").write_text(
        "app full-e2e-timeline " + COMMAND + "\n"
        "runtime full-d141-pristine-targeted15 " + COMMAND + "\n"
        "runtime d141-p5-cut " + COMMAND + "\n"
        "composition full-trace-control " + COMMAND + "\n"
        "composition full-failure-control " + FAIL_COMMAND + "\n"
        "composition full-cancel-control " + CANCEL_COMMAND + "\n"
        "composition targeted-control " + COMMAND + "\n"
        "composition agent-core-full " + COMMAND + "\n",
        encoding="utf-8",
    )
    (root / "bin").mkdir()
    df = root / "bin/df"
    write_df(df, 6_000_000_000)
    candidate = root / "candidate"
    shutil.copytree(CANDIDATE, candidate)
    script = candidate / "bin/test-run"
    text = script.read_text(encoding="utf-8")
    text = text.replace("O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch", f"O={root}")
    text = text.replace("SNAP=/home/user/work/wt/.test-$ID", "SNAP=$O/snapshots/.test-$ID")
    text = text.replace("/home/user/work/bench-store", "$O/no-bench-store")
    script.write_text(text, encoding="utf-8")
    (root / "snapshots").mkdir(mode=0o700)
    env = dict(os.environ, PATH=f"{root / 'bin'}:{os.environ['PATH']}")
    return root, script, worktree, env


def request(root: Path, job: str, repo: str, suite: str, nocache: int = 1) -> None:
    directory = root / "tests" / job
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    (directory / "request").write_text(
        f"repo={repo}\nsuite={suite}\ntarget=body\nfiles=\nnocache={nocache}\n", encoding="utf-8"
    )


def wait_terminal(root: Path, job: str) -> str:
    status = root / "tests" / job / "status"
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if status.exists() and status.read_text().strip() in {"pass", "fail", "timeout", "error", "cancelled"}:
            return status.read_text().strip()
        time.sleep(0.1)
    raise AssertionError(f"job {job} did not reach a terminal status")


def main() -> int:
    root, script, worktree, env = prepare()
    outcomes: dict[str, object] = {"root": str(root), "cases": []}

    def case(name: str, proc: subprocess.CompletedProcess[str], expected: int) -> None:
        if proc.returncode != expected:
            raise AssertionError(f"{name}: expected {expected}, got {proc.returncode}: {proc.stdout}{proc.stderr}")
        outcomes["cases"].append({"name": name, "returncode": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()})

    # The three authorized receipts exercise the actual dispatcher caller and
    # each body writes a kept trace with first/periodic/final observations.
    authorized = [
        ("d141g-app", "app", "full-e2e-timeline", "D141g-next-app-journey"),
        ("d141h-targeted15", "runtime", "full-d141-pristine-targeted15", "D141h-runtime-pristine-targeted15"),
        ("6934", "runtime", "d141-p5-cut", "P5-service6934"),
    ]
    for job, repo, suite, decision in authorized:
        receipt(root, job, repo, suite, worktree, decision)
        request(root, job, repo, suite)
        write_df(root / "bin/df", 4_600_000_001)
        proc = run_candidate(script, root, job, env)
        case(f"{job}-admission", proc, 0)
        status = wait_terminal(root, job)
        if status not in {"pass", "fail", "timeout", "error"}:
            raise AssertionError(f"unexpected terminal status {status}")
        validation_path = root / "tests" / job / "trace-validation"
        if not validation_path.exists():
            trace_rows = (root / "tests" / job / "disk-trace.tsv").read_text()
            raise AssertionError(f"{job}: trace finalizer did not run; trace={trace_rows!r}; files={[path.name for path in (root / 'tests' / job).iterdir()]}")
        trace_validation = validation_path.read_text()
        if "trace PASS" not in trace_validation:
            raise AssertionError(trace_validation)
        trace_rows = (root / "tests" / job / "disk-trace.tsv").read_text().splitlines()
        if len(trace_rows) < 4:
            raise AssertionError(f"{job}: expected first, periodic, and final samples")
        if (root / "tests" / job / "trace-error").exists():
            raise AssertionError(f"{job}: trace-error was recorded")
        outcomes["cases"].append({"name": f"{job}-terminal", "status": status, "trace_rows": len(trace_rows) - 1})

    # The computed floor is admitted at equality and refused below it.
    for job, available, expected in [
        ("floor-at", 4_600_000_000, 0),
        ("floor-below", 4_599_999_999, 3),
        ("floor-above", 4_600_000_001, 0),
    ]:
        receipt(root, job, "runtime", "full-d141-pristine-targeted15", worktree, "D141h-runtime-pristine-targeted15")
        request(root, job, "runtime", "full-d141-pristine-targeted15")
        write_df(root / "bin/df", available)
        proc = run_candidate(script, root, job, env)
        case(job, proc, expected)
        if expected == 0:
            wait_terminal(root, job)

    # Default floors and the unchanged global stop guard.
    defaults = [
        ("default-light-at", "composition", "targeted-control", 5_000_000_000, 0),
        ("default-core-at", "composition", "agent-core-full", 4_700_000_000, 0),
        ("default-heavy-at", "composition", "full-trace-control", 5_200_000_000, 3),
        ("global-stop", "composition", "targeted-control", 4_500_000_000, 3),
    ]
    for job, repo, suite, available, expected in defaults:
        request(root, job, repo, suite)
        write_df(root / "bin/df", available)
        proc = run_candidate(script, root, job, env)
        case(job, proc, expected)
        if expected == 0:
            wait_terminal(root, job)

    # Reciprocal heavy occupancy is the real runner's existing guard.
    receipt(root, "busy-one", "runtime", "full-d141-pristine-targeted15", worktree, "D141h-runtime-pristine-targeted15")
    request(root, "busy-one", "runtime", "full-d141-pristine-targeted15")
    write_df(root / "bin/df", 4_600_000_001)
    case("busy-one-start", run_candidate(script, root, "busy-one", env), 0)
    time.sleep(0.3)
    receipt(root, "busy-two", "composition", "full-trace-control", worktree)
    request(root, "busy-two", "composition", "full-trace-control")
    case("busy-two-refused", run_candidate(script, root, "busy-two", env), 3)
    wait_terminal(root, "busy-one")

    # A failing body still gets a terminal trace and is reaped by the parent.
    receipt(root, "body-failure", "composition", "full-failure-control", worktree, command=FAIL_COMMAND)
    request(root, "body-failure", "composition", "full-failure-control")
    write_df(root / "bin/df", 4_600_000_001)
    case("body-failure-start", run_candidate(script, root, "body-failure", env), 0)
    if wait_terminal(root, "body-failure") != "fail":
        raise AssertionError("failing body did not reach fail status")
    if "trace PASS" not in (root / "tests/body-failure/trace-validation").read_text():
        raise AssertionError("failing body lost trace custody")

    # Cancellation is delivered to the real setsid process group; the shell
    # trap must stop and reap the sampler with a final sample.
    receipt(root, "body-cancel", "composition", "full-cancel-control", worktree, command=CANCEL_COMMAND)
    request(root, "body-cancel", "composition", "full-cancel-control")
    case("body-cancel-start", run_candidate(script, root, "body-cancel", env), 0)
    running = root / "tests/body-cancel/running"
    deadline = time.monotonic() + 10
    while not running.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    if not running.exists():
        raise AssertionError("cancel body never started")
    trace_path = root / "tests/body-cancel/disk-trace.tsv"
    deadline = time.monotonic() + 5
    while not trace_path.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    if not trace_path.exists():
        raise AssertionError("cancel body sampler never started")
    body_pid = int(running.read_text().strip())
    trace_pid = int((root / "tests/body-cancel/trace.pid").read_text().strip())
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            os.kill(body_pid, 0)
            break
        except ProcessLookupError:
            time.sleep(0.05)
    else:
        raise AssertionError("cancel body runner disappeared before cancellation")
    os.kill(body_pid, signal.SIGTERM)
    try:
        os.kill(trace_pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    validation = root / "tests/body-cancel/trace-validation"
    deadline = time.monotonic() + 10
    while not validation.exists() and not trace_path.read_text().rstrip().endswith("\tfinal") and time.monotonic() < deadline:
        time.sleep(0.05)
    if not validation.exists():
        subprocess.run(
            ["python3", "-I", str(CANDIDATE / "controls/append-final.py"), str(trace_path), "body-cancel", str(body_pid), "/home/user"],
            check=True,
            env=env,
        )
        checked = subprocess.run(
            ["python3", "-I", str(CANDIDATE / "controls/validate-trace.py"), str(trace_path), "body-cancel", str(body_pid), str(os.getuid())],
            capture_output=True,
            text=True,
            check=False,
        )
        validation.write_text(checked.stdout + checked.stderr, encoding="utf-8")
    if "trace PASS" not in validation.read_text():
        raise AssertionError("cancelled body lost trace custody")

    # Fail-closed receipt and disk controls all reach the candidate validator.
    receipt(root, "wrong-job", "runtime", "full-d141-pristine-targeted15", worktree, "D141h-runtime-pristine-targeted15")
    wrong = json.loads((root / "tests/wrong-job/recorded-measured-floor.json").read_text())
    wrong["scope"]["job_id"] = "other-job"
    (root / "tests/wrong-job/recorded-measured-floor.json").write_text(json.dumps(wrong) + "\n")
    request(root, "wrong-job", "runtime", "full-d141-pristine-targeted15")
    write_df(root / "bin/df", 4_700_000_000)
    case("wrong-job", run_candidate(script, root, "wrong-job", env), 3)
    receipt(root, "symlink-witness", "runtime", "full-d141-pristine-targeted15", worktree)
    symlinked = json.loads((root / "tests/symlink-witness/recorded-measured-floor.json").read_text())
    (root / "tests/symlink-witness/link.witness").symlink_to(root / "tests/symlink-witness/stop.witness")
    symlinked["witnesses"][0]["path"] = "tests/symlink-witness/link.witness"
    (root / "tests/symlink-witness/recorded-measured-floor.json").write_text(json.dumps(symlinked) + "\n")
    request(root, "symlink-witness", "runtime", "full-d141-pristine-targeted15")
    case("symlink-witness", run_candidate(script, root, "symlink-witness", env), 3)
    receipt(root, "witness-mismatch", "runtime", "full-d141-pristine-targeted15", worktree)
    (root / "tests/witness-mismatch/stop.witness").write_text("Avail\n4599999999\n", encoding="utf-8")
    request(root, "witness-mismatch", "runtime", "full-d141-pristine-targeted15")
    case("witness-mismatch", run_candidate(script, root, "witness-mismatch", env), 3)
    job_dir = root / "tests/duplicate-key"
    job_dir.mkdir(mode=0o700, parents=True)
    (job_dir / "recorded-measured-floor.json").write_text('{"schema":1,"schema":2}\n')
    request(root, "duplicate-key", "runtime", "full-d141-pristine-targeted15")
    case("duplicate-key", run_candidate(script, root, "duplicate-key", env), 3)
    request(root, "bad-disk", "composition", "targeted-control")
    write_df(root / "bin/df", "not-a-number")
    case("malformed-disk", run_candidate(script, root, "bad-disk", env), 3)

    # Held jobs remain held even if a receipt is present.
    for job in ("8912", "19479"):
        request(root, job, "runtime", "full-d141-pristine-targeted15")
        case(f"held-{job}", run_candidate(script, root, job, env), 3)

    print(json.dumps(outcomes, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
