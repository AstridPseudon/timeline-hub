#!/usr/bin/env python3
"""One source-derived support call, with the actual qualified test fixture.

No installed files or launch arguments are patched. Python tracing observes
parent calls/returns/exceptions; child internals are limited to /proc snapshots
and the unchanged result-file protocol. The 45s timer is a diagnostic watchdog,
not the manifest's 600s transport deadline or original test qualification.
"""

from __future__ import annotations

import ast
import hashlib
import importlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
WORKER = ORCH / "workers/agt-F-render-qualified-probe-sol-0603"
EVIDENCE = WORKER / "evidence"
ORIGINAL = ORCH / "workers/agt-F-render-timeout-qualify-0509/evidence/preflight.json"
TARGET = ROOT / "tests/packs/rendering/test_threejs_backend.py"
START = time.monotonic()
DECLARED = (
    "HOME",
    "LANG",
    "LC_ALL",
    "PATH",
    "TMPDIR",
    "PYTHONPATH",
    "PYTHONDONTWRITEBYTECODE",
    "ASTRID_HOST_EXECUTION_PROFILE",
    "ASTRID_RUNTIME_CHECKOUT",
    "ASTRID_RUNTIME_SOURCE_ROOT",
    "ASTRID_REMOTION_PROJECT_DIR",
    "ASTRID_NODE_EXECUTABLE",
    "ASTRID_TEST_NODE_MODULES",
    "ASTRID_TIMELINE_SCHEMA_PYTHONPATH",
    "ASTRID_REMOTION_VALIDATION_PATH",
    "ASTRID_REMOTION_VALIDATION_SHA256",
    "ASTRID_REMOTION_VALIDATION_LAUNCH",
    "ASTRID_REMOTION_VALIDATION_ROLE",
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(name, data):
    (EVIDENCE / name).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def event(stage, **data):
    row = {
        "stage": stage,
        "monotonic": time.monotonic(),
        "elapsed": time.monotonic() - START,
        "observer_pid": os.getpid(),
        **data,
    }
    with (EVIDENCE / "events.jsonl").open("a") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")


def declared(env):
    return {key: env.get(key) for key in DECLARED}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def function(tree, name):
    return next(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == name
    )


def snapshot(pid):
    result = {"pid": pid}
    for name in ("status", "stat", "wchan", "cmdline"):
        try:
            result[name] = (Path(f"/proc/{pid}") / name).read_text().replace("\x00", " ")
        except OSError as exc:
            result[name] = type(exc).__name__
    return result


def file_state(path):
    if not path:
        return None
    path = Path(path)
    if not path.exists():
        return {"path": str(path), "exists": False}
    data = path.read_bytes()
    return {
        "path": str(path),
        "exists": True,
        "bytes": len(data),
        "sha256": sha(data),
        "text": data.decode("utf-8", "replace"),
    }


def launch():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if (EVIDENCE / "launch.json").exists():
        raise RuntimeError("this diagnostic already launched; no second invocation")
    old = json.loads(ORIGINAL.read_text())
    tmp = Path(os.environ["TMPDIR"]) / "qualified-render-probe-0603"
    tmp.mkdir(parents=True, exist_ok=False)
    shim = tmp / "import-shim"
    shim.mkdir()
    for name in ("tests", "scripts"):
        (shim / name).symlink_to(ROOT / name, target_is_directory=True)
    child = Path(old["installed_child"]["path"])
    node_bin = str(Path(old["profile"]["node"]).parent)
    env = {
        "HOME": "/root",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "TMPDIR": str(tmp),
        "PYTHONPATH": str(shim),
        "PATH": f"{child}/bin:{node_bin}:/usr/bin:/bin",
        "ASTRID_HOST_EXECUTION_PROFILE": "installed",
        "ASTRID_RUNTIME_CHECKOUT": old["runtime"]["checkout"],
        "ASTRID_RUNTIME_SOURCE_ROOT": old["runtime"]["checkout"],
        "ASTRID_REMOTION_PROJECT_DIR": old["profile"]["path"],
        "ASTRID_NODE_EXECUTABLE": old["profile"]["node"],
        "ASTRID_TEST_NODE_MODULES": old["profile"]["node_modules"],
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": "/home/user/work/venv-agent/lib/python3.13/site-packages",
    }
    for ref, filename, dest in (
        (
            "tl/agt-F-render-timeout-qualify-0509",
            "tools/run-render-timeout-qualify-0509.sh",
            "original-0509-runner.sh",
        ),
        (
            "tl/agt-F-render-support-probe-0530",
            "tools/run-render-support-probe-0530.py",
            "wrong-env-0530-harness.py",
        ),
    ):
        (EVIDENCE / dest).write_text(git("show", f"{ref}:{filename}") + "\n")
    source = Path(__file__).read_bytes()
    (EVIDENCE / "harness-before-execution.py").write_bytes(source)
    argv = [str(child / "bin/python"), "-P", str(Path(__file__).resolve()), "--child"]
    write(
        "launch.json",
        {
            "argv": argv,
            "cwd": str(ROOT),
            "declared_env": declared(env),
            "harness_sha256": sha(source),
            "monotonic": time.monotonic(),
            "original_preflight_sha256": sha(ORIGINAL.read_bytes()),
            "durable_source_before_execution": True,
        },
    )
    with (EVIDENCE / "stdout.txt").open("w") as out, (EVIDENCE / "stderr.txt").open("w") as err:
        process = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=out, stderr=err)
        event("harness.spawn", pid=process.pid, argv=argv, cwd=str(ROOT))
        code = process.wait()
    write(
        "launcher-result.json",
        {"returncode": code, "pid": process.pid, "monotonic": time.monotonic()},
    )
    return code


def preflight():
    old = json.loads(ORIGINAL.read_text())
    site = Path(old["installed_child"]["site_packages"])
    assert Path(sys.prefix) == Path(old["installed_child"]["path"])
    facts = {
        "declared_launch_env": declared(os.environ),
        "sys_path": sys.path,
        "original_global_watchdog": 45,
        "original_failure_seconds": 45.65,
        "runtime_validation": "absent in original runner and actual fixture; not fabricated",
    }
    write("preflight-start.json", facts)
    assert (site.parents[2] / ".astrid-source-commit").read_text().strip() == old[
        "installed_child"
    ]["recorded_source_commit"]
    assert (site.parents[2] / ".astrid-runtime-source-commit").read_text().strip() == old[
        "installed_child"
    ]["recorded_runtime_commit"]
    assert sha(Path(old["receipt"]["path"]).read_bytes()) == old["receipt"]["sha256"]
    for rel, expected in old["source_vs_installed"].items():
        assert sha((site / rel).read_bytes()) == expected["installed_sha256"], rel
        assert (ROOT / rel).read_bytes() == (site / rel).read_bytes(), rel
    for rel in (
        "tests/packs/conftest.py",
        "tests/packs/rendering/_helpers.py",
        "astrid/core/subprocess_env.py",
        "astrid/sdk/host_bootstrap.py",
    ):
        assert (ROOT / rel).read_bytes() == subprocess.check_output(
            ["git", "show", f"ba8f0bc8be:{rel}"], cwd=ROOT
        ), rel
    tree = ast.parse(TARGET.read_text())
    fn = function(tree, "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons")
    assert (
        sha(ast.dump(fn, annotate_fields=True, include_attributes=False).encode())
        == old["original_test"]["body_before"]["function_ast_sha256"]
    )
    assert sum(isinstance(n, ast.Assert) for n in ast.walk(fn)) == 9
    for filename, key in (
        ("package-lock.json", "package_lock_sha256"),
        (
            "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz",
            "composition_archive_sha256",
        ),
    ):
        assert sha((Path(old["profile"]["path"]) / filename).read_bytes()) == old["profile"][key]
    assert Path(old["profile"]["node"]).is_file()
    assert Path(old["profile"]["node_modules"]).is_dir()
    from astrid.core.rendering import transport
    from astrid.core.subprocess_env import build_child_subprocess_env
    from astrid.sdk import host_bootstrap
    from tests.packs.conftest import renderer_execution_environment

    facts["origins"] = {}
    for name in (
        "astrid",
        "astrid_runtime",
        "runtime_protocol",
        "astrid_runtime_client",
        "astrid.sdk.rendering",
        "astrid.core.rendering.registry",
        "astrid.core.rendering.transport",
        "astrid.sdk.host_bootstrap",
    ):
        module = importlib.import_module(name)
        origin = Path(module.__file__)
        assert origin.is_relative_to(site), name
        facts["origins"][name] = str(origin)
    assert host_bootstrap._execution_profile() == "installed"
    facts["installed_authority_origins"] = host_bootstrap._installed_execution_origins(
        site, sys.executable
    )
    fixture = renderer_execution_environment.__wrapped__()
    next(fixture)
    facts["fixture_environment"] = declared(os.environ)
    projected = build_child_subprocess_env(base=dict(os.environ), parent=dict(os.environ))
    actual = transport._build_environment(None)
    assert actual == projected
    expected_path = f"{sys.prefix}/bin:{Path(old['profile']['node']).parent}:{sys.prefix}/bin:{Path(old['profile']['node']).parent}:/usr/bin:/bin"
    assert os.environ["PATH"] == expected_path
    dropped = {
        "ASTRID_HOST_EXECUTION_PROFILE",
        "ASTRID_TEST_NODE_MODULES",
        "ASTRID_RUNTIME_CHECKOUT",
        "ASTRID_RUNTIME_SOURCE_ROOT",
        "PYTHONPATH",
        "PYTHONDONTWRITEBYTECODE",
    }
    for key in DECLARED:
        expected = None if key in dropped else os.environ.get(key)
        assert actual.get(key) == expected, key
    facts["actual_build_child_subprocess_env"] = declared(projected)
    facts["actual_transport_environment"] = declared(actual)
    facts["intentional_dropped_caller_profile"] = "ASTRID_HOST_EXECUTION_PROFILE" not in actual
    facts["profile_authority"] = (
        "installed caller validated by existing bootstrap; child selector intentionally absent"
    )
    facts["node_version"] = {
        "original_recorded": old["profile"]["node_version"],
        "executed_here": False,
    }
    facts["status"] = "passed"
    write("preflight.json", facts)
    return fixture, fn, actual


def probe(fn, expected_env):
    from astrid.sdk.rendering import support

    tmp = Path(os.environ["TMPDIR"])
    # Compile only the existing helper and transition assignment. Never execute
    # the enclosing test, its assertions, loops, or the other nine support calls.
    helper = function(fn, "reasons_for")
    transition = next(
        node
        for node in fn.body
        if isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "reasons_for"
        and any(isinstance(n, ast.Constant) and n.value == "transition" for n in ast.walk(node))
    )
    writer = function(ast.parse(TARGET.read_text()), "_write_timeline")
    canvas = next(
        n.value
        for n in ast.parse(TARGET.read_text()).body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "CANVAS" for t in n.targets)
    )
    code = ast.Module(body=[writer, helper, transition], type_ignores=[])
    namespace = {
        "Path": Path,
        "json": json,
        "support": support,
        "THREEJS_ID": "rendering.threejs",
        "CANVAS": ast.literal_eval(canvas),
        "tmp_path": tmp,
    }
    write(
        "source-derived-call.json",
        {
            "source_path": str(TARGET),
            "helper_line": helper.lineno,
            "transition_line": transition.lineno,
            "ast_sha256": sha(ast.dump(code).encode()),
            "source": ast.unparse(code),
            "body_runs": 0,
            "support_calls": 1,
        },
    )
    processes = {}
    result_paths = set()
    selected = {
        "support",
        "_support_report",
        "_resolve_registries",
        "_resolve_candidate",
        "load_default_registries",
        "discover_pack_metadata",
        "discover_packs",
        "_execution_profile",
        "_installed_execution_origins",
        "_host_render_environment",
        "_build_environment",
        "build_child_subprocess_env",
        "popen_owned_process",
        "observe_tree",
        "verify_tree_absent",
        "run",
        "_resolve_executable",
    }

    def capture(stage):
        for proc in processes.values():
            buffers = getattr(proc, "_fileobj2output", {})
            event(
                stage,
                pid=proc.pid,
                returncode=proc.returncode,
                state=snapshot(proc.pid),
                streams={
                    str(fd): b"".join(parts).decode("utf-8", "replace")
                    for fd, parts in buffers.items()
                },
                results=[file_state(path) for path in sorted(result_paths)],
            )

    def trace(frame, kind, value):
        name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        local = frame.f_locals
        process = local.get("self")
        popen = filename == subprocess.__file__ and name in {"__init__", "communicate"}
        product = "/site-packages/astrid/" in filename and name in selected
        if not (popen or product):
            return None
        frame.f_trace_lines = False
        if kind == "call":
            fields = {}
            if name == "run" and "result_path" in local:
                result_paths.add(str(local["result_path"]))
                fields = {
                    key: str(local.get(key))
                    for key in ("verb", "command", "cwd", "timeout", "request_path", "result_path")
                }
                fields["request"] = file_state(local["request_path"])
            event(f"{name}.call", file=filename, **fields)
        elif kind == "return":
            if popen and name == "__init__" and getattr(process, "pid", None):
                argv = local.get("args")
                if isinstance(argv, list) and any("threejs/run.py" in str(arg) for arg in argv):
                    processes[id(process)] = process
                    env = local.get("env") or {}
                    event(
                        "owned_child.setup",
                        argv=argv,
                        cwd=str(local.get("cwd")),
                        pid=process.pid,
                        process_identity=id(process),
                        declared_env=declared(env),
                        environment_keys=sorted(env),
                        matches_preflight=env == expected_env,
                        state=snapshot(process.pid),
                    )
            if popen and name == "communicate" and id(process) in processes:
                event(
                    "owned_child.reply",
                    pid=process.pid,
                    returncode=process.returncode,
                    result_identity=id(value),
                    streams=[str(item) for item in value] if isinstance(value, tuple) else None,
                    results=[file_state(path) for path in sorted(result_paths)],
                )
            event(
                f"{name}.return",
                file=filename,
                result_type=type(value).__name__,
                result_identity=id(value),
            )
        elif kind == "exception":
            event(
                f"{name}.exception",
                file=filename,
                exception_type=value[0].__name__,
                exception_identity=id(value[1]),
            )
            capture("exception.before_cleanup")
        return trace

    def deadline(_signum, _frame):
        capture("watchdog.before_cleanup")
        event("watchdog", seconds=45)
        raise KeyboardInterrupt("single-probe diagnostic 45s watchdog")

    marker = EVIDENCE / "probe-started"
    with marker.open("x") as stream:
        stream.write(str(time.monotonic()) + "\n")
    old_handler = signal.signal(signal.SIGALRM, deadline)
    started = time.monotonic()
    sys.settrace(trace)
    signal.setitimer(signal.ITIMER_REAL, 45)
    try:
        exec(compile(code, str(TARGET), "exec"), namespace)
    except BaseException as exc:  # noqa: BLE001 - retain diagnostic watchdog and original failures
        outcome = {
            "status": "exception",
            "type": type(exc).__name__,
            "text": str(exc),
            "identity": id(exc),
        }
    else:
        outcome = {"status": "returned", "reasons": namespace["reasons"]}
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        sys.settrace(None)
        signal.signal(signal.SIGALRM, old_handler)
    outcome.update(
        elapsed=time.monotonic() - started,
        child_count=len(processes),
        diagnostic_only=True,
        original_body_run=False,
        child_internal_python_trace=False,
    )
    write("result.json", outcome)
    print(json.dumps(outcome, sort_keys=True))
    return 0 if outcome["status"] == "returned" else 1


def main():
    if "--child" not in sys.argv:
        return launch()
    event("preflight.start")
    try:
        fixture, fn, expected_env = preflight()
    except BaseException as exc:
        write(
            "preflight-failure.json",
            {"status": "failed", "type": type(exc).__name__, "text": str(exc), "support_calls": 0},
        )
        raise
    event("preflight.passed")
    try:
        return probe(fn, expected_env)
    finally:
        fixture.close()


if __name__ == "__main__":
    raise SystemExit(main())
