"""Execute only a candidate caller's read-only source identity phase."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shlex
import subprocess
import time
from typing import Any


class DryPreflightError(RuntimeError):
    """The candidate source phase refused or was not safely bounded."""


BOUNDARY = ": TIMELINE_SOURCE_ENVIRONMENT_COMPLETE; "
LAUNCH_ARGV = ["timeout", "-k", "60", "90m", "nice", "-n", "5", "bash", "-c"]


def bounded_outer(outer: str, body: str) -> str:
    """Retain the real outer argv/assignment/eval and every admission guard."""
    start = outer.index("$(bash -c ") + len("$(bash -c ")
    end = outer.index(')" && eval', start)
    if shlex.split(outer[start:end]) != [body] or body.count(BOUNDARY) != 1:
        raise DryPreflightError("actual launch argv/admission boundary changed")
    prefix = body[:body.index(BOUNDARY) + len(BOUNDARY)]
    if any(token in prefix for token in ("mkdir -p", "_ALLOCATED_PORT=", "unlink ", "ln -s ", "npm ", "node --import")):
        raise DryPreflightError("bounded admission includes an output or socket stage")
    stage = "2" if 'P2_ENV="$(' in outer[:start] else "3"
    seam = f')" && eval "$P{stage}_ENV"'
    if outer[end:end + len(seam)] != seam:
        raise DryPreflightError("actual launch eval boundary changed")
    return outer[:start] + shlex.quote(prefix + "exit 0;") + seam + ' && printf "%s\\n" bounded-launch-PASS'


def dry_launch_preflight(outer: str, body: str, *, target: Path, inherited: dict[str, str] | None = None) -> dict[str, Any]:
    """Execute every real admission guard, with only the subsequent work cut."""
    bounded = bounded_outer(outer, body)
    env = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
    env.update(inherited or {})
    started = time.monotonic()
    result = subprocess.run([*LAUNCH_ARGV, bounded], cwd=target, env=env,
                            text=True, capture_output=True, timeout=60, check=False)
    if result.returncode or result.stdout.strip() != "bounded-launch-PASS" or "source/environment admission PASS" not in result.stderr:
        raise DryPreflightError(f"actual launch admission refused ({result.returncode}): {result.stderr.strip()}")
    return {
        "status": "PASS", "returncode": result.returncode,
        "phase": "actual_outer_source_environment_admission",
        "service_argv": [*LAUNCH_ARGV, outer],
        "bounded_argv": [*LAUNCH_ARGV, bounded],
        "environment": env, "duration_seconds": round(time.monotonic() - started, 3),
        "target": str(target), "stdout": result.stdout, "stderr": result.stderr,
        "not_run": ["native", "build", "browser", "backend", "provision", "schema", "HTTP", "original"],
    }


def _guard(body: str, stage: str) -> str:
    marker = f'printf "%s\\n" "$P{stage}APP"'
    start = body.find(marker)
    if start < 0 and stage == "3":
        # P3's retained source phase starts with the checked-out HEAD rather
        # than a printf of P3APP; P3APP is supplied by the frozen prefix.
        start = body.find("APP_HEAD=$(git rev-parse HEAD")
    if start < 0:
        raise DryPreflightError("decoded candidate has no App identity guard")
    end_marker = f'test -f "$P{stage}O/queue/done'
    end = body.find(end_marker, start)
    if end < 0:
        raise DryPreflightError("decoded candidate has no bounded custody boundary")
    guard = body[start:end]
    forbidden = (
        "mkdir ", "npm ", "node ", "python", "pytest", "playwright",
        "curl ", "nc ", "listen(", "import ", "build", "native", "browser",
        "backend", "provision", "http", "original-body",
    )
    if any(token in guard.lower() for token in forbidden):
        raise DryPreflightError("source phase contains setup, execution, or external custody work")
    return guard + f'if test -n "$P{stage}FAIL"; then printf "source guard refusals:%s\\n" "$P{stage}FAIL" >&2; exit 2; fi;'


def dry_source_preflight(
    body: str,
    *,
    app: dict[str, Any],
    agent: dict[str, Any],
    runtime: dict[str, Any],
    target: Path,
    stage: str,
) -> dict[str, Any]:
    """Run the decoded candidate's actual source/target/binding guard.

    The extracted prefix ends before child, import, backend, graph, service,
    and original-body custody.  Missing later custody therefore remains a
    PREPARED blocker and cannot turn this read-only source PASS into READY.
    """
    if stage not in {"2", "3"}:
        raise DryPreflightError(f"unsupported source stage: {stage}")
    guard = _guard(body, stage)
    body_match = re.search(rf"(?:^|;)\s*P{stage}BODY=([^;]+)", body)
    source_body = body_match.group(1).strip("'\"") if body_match else ""
    if (target != Path(app["checkout"]) or not target.is_absolute() or target.is_symlink()
            or target.resolve() != target or not target.is_dir()):
        raise DryPreflightError(f"source target is unavailable: {target}")
    prefix = "\n".join(
        (
            "set -u",
            f'P{stage}O={app["orch"]!s}',
            f'P{stage}A={agent["source"]}',
            f'P{stage}R={runtime["source"]}',
            f'P{stage}APP={app["source"]}',
            f'P{stage}TREE={app["tree"]}',
            f'P{stage}PARENT={" ".join(app["parents"])!r}',
            f'P{stage}AG={agent["checkout"]}',
            f'P{stage}RT={runtime["checkout"]}',
            f'P{stage}BODY={shlex.quote(source_body)}' if source_body else ':',
            f'P{stage}FAIL=""',
            f'p{stage.lower()}fail(){{ P{stage}FAIL="$P{stage}FAIL $1"; }};',
            guard,
        )
    )
    started = time.monotonic()
    result = subprocess.run(
        ["/bin/bash", "-c", prefix],
        cwd=target,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C"},
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    elapsed = round(time.monotonic() - started, 3)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip().splitlines()[-1:]
        raise DryPreflightError(f"candidate source guard refused: {detail}")
    return {
        "status": "PASS",
        "duration_seconds": elapsed,
        "returncode": result.returncode,
        "phase": "source_identity_tree_target_bindings",
        "command": f"actual decoded P{stage} source guard via caller-dry-preflight.py",
        "argv": ["/bin/bash", "-c", prefix],
        "script_sha256": hashlib.sha256(prefix.encode()).hexdigest(),
        "target": {"checkout": str(target), "source": app["source"], "tree": app["tree"], "parents": app["parents"]},
        "refusals": [],
        "not_run": ["child", "import", "native", "build", "browser", "backend", "provision", "schema", "HTTP", "original"],
    }
