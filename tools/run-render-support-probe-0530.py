#!/usr/bin/env python3
"""One bounded, observational renderer support diagnostic.

This harness intentionally imports the managed child installation, not the
checkout.  It calls the public SDK support caller once with the transition
payload copied from the existing test, while wrappers only observe calls and
return the original values, exceptions, and process objects unchanged.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHILD = Path(
    "/home/user/work/bench-store/entries/child-3b5cb98c4f2dfc20ce8747f68bf2e1124ff47b9dd5f04dabaada3a22278fdfc9"
)
RUNTIME = Path("/home/user/work/wt/rt-pin-f3208b26")
PROFILE = Path("/home/user/work/runtimes/agent-remotion-v3-819acf-1110")
NODE_BIN = Path("/home/user/work/toolchain/node-v20.19.4-linux-x64/bin")
EVIDENCE = Path(
    os.environ.get(
        "EVIDENCE",
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-support-probe-0530/evidence",
    )
    or "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-support-probe-0530/evidence"
)
TMPROOT = Path(
    os.environ.get(
        "TMPROOT",
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-support-probe-0530/tmpdir",
    )
    or "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-support-probe-0530/tmpdir"
)
RECEIPT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-d40-ba8f-f320.txt"
)
TARGET = ROOT / "tests/packs/rendering/test_threejs_backend.py"
RELEVANT = (
    "astrid/sdk/rendering.py",
    "astrid/core/rendering/transport.py",
    "astrid/core/rendering/registry.py",
    "astrid/packs/rendering/rendering/renderers/threejs/run.py",
    "astrid/packs/rendering/rendering/renderers/threejs/renderer.yaml",
)
MODULES = (
    "astrid",
    "astrid.sdk.rendering",
    "astrid.core.rendering.registry",
    "astrid.core.rendering.transport",
    "astrid.sdk.host_bootstrap",
    "astrid.packs.rendering.rendering.renderers.threejs.run",
    "astrid_runtime_client",
    "runtime_protocol",
)
SECRET_VALUE = re.compile(
    r"(?i)\b((?:api[_-]?key|auth(?:orization)?|credential|password|secret|token)\s*[:=]\s*)[^\s,;]+"
)
SECRET_TOKEN = re.compile(r"(?i)\b(?:Bearer\s+|sk-|gh[pousr]_)[A-Za-z0-9._~+/=-]+")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def compact_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def scrub_text(value: str) -> str:
    value = SECRET_VALUE.sub(r"\1[redacted]", value.replace("\x00", "\ufffd"))
    return SECRET_TOKEN.sub("[redacted]", value)


def scrub_stream(value: Any) -> dict[str, Any]:
    if value is None:
        raw = b""
    elif isinstance(value, bytes):
        raw = value
    else:
        raw = str(value).encode("utf-8", "replace")
    text = scrub_text(raw.decode("utf-8", "replace"))
    return {"bytes": len(raw), "sha256": sha_bytes(raw), "text": text[:65536]}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def status() -> list[str]:
    return [line for line in git("status", "--porcelain").splitlines() if line]


def body_facts(path: Path) -> dict[str, Any]:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(
        node
        for node in ast.walk(module)
        if isinstance(node, ast.FunctionDef)
        and node.name == "test_threejs_support_rejects_unsupported_timelines_with_clip_reasons"
    )
    assertions = [node for node in ast.walk(function) if isinstance(node, ast.Assert)]
    return {
        "file_sha256": sha(path),
        "function_ast_sha256": sha_bytes(
            ast.dump(function, annotate_fields=True, include_attributes=False).encode()
        ),
        "assertions_ast_sha256": sha_bytes(
            ast.dump(
                ast.Module(body=assertions, type_ignores=[]),
                annotate_fields=True,
                include_attributes=False,
            ).encode()
        ),
        "assertion_count": len(assertions),
        "line_start": function.lineno,
        "line_end": function.end_lineno,
    }


def proc_state(pid: int | None) -> dict[str, Any]:
    if not pid or pid <= 0:
        return {"pid": pid, "present": False}
    root = Path(f"/proc/{pid}")
    state: dict[str, Any] = {"pid": pid, "present": root.exists()}
    try:
        status_lines = (root / "status").read_text(encoding="utf-8").splitlines()
        wanted = {"Name", "State", "PPid", "NSpid", "Threads", "VmRSS"}
        state["status"] = {
            line.split(":", 1)[0]: line.split(":", 1)[1].strip()
            for line in status_lines
            if ":" in line and line.split(":", 1)[0] in wanted
        }
    except (OSError, UnicodeDecodeError):
        state["status"] = None
    try:
        state["cwd"] = os.readlink(root / "cwd")
    except OSError:
        state["cwd"] = None
    try:
        state["cmdline"] = [
            scrub_text(part.decode("utf-8", "replace"))
            for part in (root / "cmdline").read_bytes().split(b"\0")
            if part
        ]
    except (OSError, UnicodeDecodeError):
        state["cmdline"] = None
    try:
        state["environment_keys"] = sorted(
            part.split(b"=", 1)[0].decode("utf-8", "replace")
            for part in (root / "environ").read_bytes().split(b"\0")
            if b"=" in part
        )
    except (OSError, UnicodeDecodeError):
        state["environment_keys"] = None
    return state


def result_state(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return {"path": str(path), "present": False, "bytes": 0, "sha256": None}
    except OSError as exc:
        return {"path": str(path), "present": "error", "error_type": type(exc).__name__}
    return {"path": str(path), "present": True, "bytes": len(data), "sha256": sha_bytes(data)}


def argv_value(argv: Any) -> list[str]:
    if isinstance(argv, (str, bytes)):
        return [os.fsdecode(argv)]
    return [os.fsdecode(value) for value in (argv or ())]


def target_argv(argv: list[str]) -> bool:
    return "rendering/renderers/threejs/run.py" in " ".join(argv)


def extract_result(argv: list[str]) -> Path | None:
    try:
        return Path(argv[argv.index("--result") + 1])
    except (ValueError, IndexError):
        return None


class DiagnosticDeadline(BaseException):
    pass


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    TMPROOT.mkdir(parents=True, exist_ok=True)
    # The harness is executed from ``-c`` so its file path cannot add the
    # checkout to sys.path. Keep the managed child site package explicit when
    # the isolated interpreter omits its normal venv site path.
    installed_site = str(CHILD / "lib/python3.13/site-packages")
    if installed_site not in sys.path:
        sys.path.insert(0, installed_site)
    evidence: dict[str, Any] = {
        "diagnostic": {
            "label": "synthetic diagnostic, not original credit",
            "original_credit": False,
            "target_probe_count": 1,
            "body_runs": 0,
            "render_or_browser": False,
            "outer_bound_seconds": 45,
            "original_test_watchdog_seconds": 45,
            "original_test_body_invoked": False,
        },
        "preflight": {},
        "trace": {"events": [], "popen": [], "communicates": []},
    }
    pre_status = status()
    before_body = body_facts(TARGET)
    evidence["preflight"].update(
        {
            "host": {
                "commit": git("rev-parse", "HEAD"),
                "tree": git("rev-parse", "HEAD^{tree}"),
                "status": pre_status,
            },
            "installed_child": str(CHILD),
            "runtime": {
                "checkout": str(RUNTIME),
                "commit": git("-C", str(RUNTIME), "rev-parse", "HEAD"),
            },
            "profile": {
                "path": str(PROFILE),
                "node": str(NODE_BIN / "node"),
                "node_version": subprocess.check_output(
                    [str(NODE_BIN / "node"), "--version"], text=True
                ).strip(),
                "package_lock_sha256": sha(PROFILE / "package-lock.json"),
                "composition_archive_sha256": sha(
                    PROFILE
                    / "artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
                ),
            },
            "receipt": {
                "path": str(RECEIPT),
                "sha256": sha(RECEIPT),
            },
            "target_body_before": before_body,
        }
    )
    site = CHILD / "lib/python3.13/site-packages"
    source_installed = {}
    for rel in RELEVANT:
        source = ROOT / rel
        installed = site / rel
        source_installed[rel] = {
            "source": str(source),
            "source_sha256": sha(source),
            "installed": str(installed),
            "installed_sha256": sha(installed),
            "byte_equal": source.read_bytes() == installed.read_bytes(),
        }
    evidence["preflight"]["source_vs_installed"] = source_installed
    if not all(item["byte_equal"] for item in source_installed.values()):
        raise RuntimeError("relevant source/installed bytes differ")

    import_origins = {}
    for name in MODULES:
        try:
            module = __import__(name, fromlist=["*"])
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                f"installed import failed for {name}: {exc}; sys.path={sys.path}"
            ) from exc
        spec = importlib.util.find_spec(name)
        if spec is None:
            spec = getattr(module, "__spec__", None)
        import_origins[name] = None if spec is None else str(spec.origin)
    evidence["preflight"]["import_origins"] = import_origins
    if any(
        not value or not value.startswith(str(site) + os.sep)
        for value in import_origins.values()
    ):
        raise RuntimeError(f"installed import origin escaped site-packages: {import_origins}")
    evidence["preflight"]["bootstrap_sha256"] = sha(site / "astrid/sdk/host_bootstrap.py")
    evidence["preflight"]["renderer_support_sha256"] = sha(
        site / "astrid/packs/rendering/rendering/renderers/threejs/run.py"
    )

    # This is exactly the transition case at source line 229, serialized as a
    # one-case synthetic diagnostic input. It is not a rerun of the test body.
    payload = {
        "theme": "banodoco-default",
        "theme_overrides": {"visual": {"canvas": {"width": 320, "height": 180, "fps": 24}}},
        "tracks": [{"id": "v1", "kind": "visual", "label": "V"}],
        "clips": [
            {
                "id": "c",
                "at": 0,
                "track": "v1",
                "clipType": "text",
                "hold": 1,
                "transition": {"id": "cross-fade", "duration": 0.2},
                "text": {"content": "x"},
            }
        ],
    }
    timeline_path = TMPROOT / "synthetic-transition-diagnostic.timeline.json"
    timeline_bytes = (json.dumps(payload) + "\n").encode("utf-8")
    timeline_path.write_bytes(timeline_bytes)
    evidence["input"] = {
        "kind": "synthetic diagnostic input",
        "source": "tests/packs/rendering/test_threejs_backend.py:229 transition case",
        "payload_sha256": sha_bytes(timeline_bytes),
        "timeline_path": str(timeline_path),
        "clip": payload["clips"][0],
    }

    from astrid.core.rendering import transport as transport_module
    from astrid.core.rendering.transport import CommandTransport
    from astrid.sdk import rendering as sdk_rendering

    start = time.monotonic()

    def mark(name: str, **fields: Any) -> None:
        evidence["trace"]["events"].append(
            {"event": name, "monotonic_seconds": time.monotonic() - start, **fields}
        )

    original_support_report = sdk_rendering._support_report
    original_run = CommandTransport.run
    original_owned = transport_module.popen_owned_process
    original_popen_init = subprocess.Popen.__init__
    original_communicate = subprocess.Popen.communicate
    processes: dict[int, dict[str, Any]] = {}
    target_process: list[subprocess.Popen] = []

    def observed_support_report(*args: Any, **kwargs: Any) -> Any:
        mark("_support_report.entry")
        try:
            result = original_support_report(*args, **kwargs)
        except BaseException as exc:
            mark("_support_report.exception", type=type(exc).__name__)
            raise
        mark("_support_report.return", result_type=type(result).__name__)
        return result

    def observed_run(self: Any, *args: Any, **kwargs: Any) -> Any:
        mark(
            "CommandTransport.run.entry",
            backend=self.backend,
            verb=args[0] if args else kwargs.get("verb"),
            timeout=kwargs.get("timeout"),
            request_path=str(kwargs.get("request_path")),
            result_path=str(kwargs.get("result_path")),
            cwd=str(kwargs.get("cwd")),
        )
        try:
            result = original_run(self, *args, **kwargs)
        except BaseException as exc:
            mark("CommandTransport.run.exception", type=type(exc).__name__)
            raise
        mark("CommandTransport.run.return", result_type=type(result).__name__)
        return result

    def observed_owned(argv: list[str], **kwargs: Any) -> Any:
        row = {
            "entry_seconds": time.monotonic() - start,
            "argv": argv_value(argv),
            "cwd": str(kwargs.get("cwd")),
            "environment_keys": sorted(str(key) for key in (kwargs.get("env") or {})),
            "stdin": repr(kwargs.get("stdin")),
            "stdout": repr(kwargs.get("stdout")),
            "stderr": repr(kwargs.get("stderr")),
            "start_new_session": kwargs.get("start_new_session"),
        }
        mark("popen_owned_process.entry", argv=row["argv"], cwd=row["cwd"], environment_keys=row["environment_keys"])
        try:
            process = original_owned(argv, **kwargs)
        except BaseException as exc:
            row["exception"] = type(exc).__name__
            row["exit_seconds"] = time.monotonic() - start
            evidence["trace"]["popen"].append(row)
            mark("popen_owned_process.exception", type=type(exc).__name__)
            raise
        row.update(
            {
                "exit_seconds": time.monotonic() - start,
                "pid": process.pid,
                "process_object_identity": id(process),
                "process_birth": getattr(process, "_astrid_process_birth", None),
            }
        )
        processes[id(process)] = row
        target_process.append(process)
        evidence["trace"]["popen"].append(row)
        mark("popen_owned_process.return", pid=process.pid, object_identity=id(process))
        return process

    def observed_popen_init(self: subprocess.Popen, *args: Any, **kwargs: Any) -> Any:
        argv = argv_value(kwargs.get("args", args[0] if args else ()))
        row = {
            "entry_seconds": time.monotonic() - start,
            "argv": argv,
            "cwd": str(kwargs.get("cwd")),
            "environment_keys": sorted(str(key) for key in (kwargs.get("env") or {})),
        }
        result = original_popen_init(self, *args, **kwargs)
        if target_argv(argv):
            row.update({"pid": self.pid, "object_identity": id(self)})
            processes[id(self)] = row
            target_process.append(self)
            evidence["trace"]["popen"].append(row)
            mark("subprocess.Popen.return", pid=self.pid, argv=argv)
        return result

    def observed_communicate(self: subprocess.Popen, *args: Any, **kwargs: Any) -> Any:
        row = processes.get(id(self))
        if row is None:
            return original_communicate(self, *args, **kwargs)
        call: dict[str, Any] = {
            "entry_seconds": time.monotonic() - start,
            "pid": self.pid,
            "object_identity": id(self),
            "timeout": kwargs.get("timeout"),
        }
        try:
            result = original_communicate(self, *args, **kwargs)
        except BaseException as exc:
            call.update(
                {
                    "exception": type(exc).__name__,
                    "returncode_before_cleanup": self.returncode,
                    "exit_seconds": time.monotonic() - start,
                }
            )
            if isinstance(exc, subprocess.TimeoutExpired):
                call["timeout_partial_stdout"] = scrub_stream(exc.output)
                call["timeout_partial_stderr"] = scrub_stream(exc.stderr)
                call["state_before_cleanup"] = proc_state(self.pid)
                call["result_before_cleanup"] = result_state(extract_result(row["argv"]))
                mark("communicate.timeout.before_cleanup", pid=self.pid)
            evidence["trace"]["communicates"].append(call)
            raise
        call.update(
            {
                "returned": True,
                "returncode_after": self.returncode,
                "exit_seconds": time.monotonic() - start,
                "stdout": scrub_stream(result[0] if isinstance(result, tuple) else None),
                "stderr": scrub_stream(result[1] if isinstance(result, tuple) else None),
                "result_after_communicate": result_state(extract_result(row["argv"])),
            }
        )
        evidence["trace"]["communicates"].append(call)
        return result

    sdk_rendering._support_report = observed_support_report
    CommandTransport.run = observed_run
    transport_module.popen_owned_process = observed_owned
    subprocess.Popen.__init__ = observed_popen_init
    subprocess.Popen.communicate = observed_communicate

    def deadline_handler(_signum: int, _frame: Any) -> None:
        mark("diagnostic.deadline", bound_seconds=45)
        if target_process:
            process = target_process[-1]
            row = processes.get(id(process), {})
            row["deadline_state_before_cleanup"] = proc_state(process.pid)
            row["deadline_result_before_cleanup"] = result_state(extract_result(row.get("argv", [])))
            try:
                stdout, stderr = transport_module._terminate_process_group(process, grace=0.5)
                row["deadline_cleanup"] = "owned_process_group_terminated"
                row["deadline_stdout_after_cleanup"] = scrub_stream(stdout)
                row["deadline_stderr_after_cleanup"] = scrub_stream(stderr)
            except BaseException as exc:
                row["deadline_cleanup_exception"] = type(exc).__name__
            row["deadline_state_after_cleanup"] = proc_state(process.pid)
        raise DiagnosticDeadline("diagnostic bound reached")

    old_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, deadline_handler)
    signal.setitimer(signal.ITIMER_REAL, 45.0)
    try:
        mark("support.entry", backend="rendering.threejs", timeline_path=str(timeline_path))
        evidence["diagnostic"]["body_runs"] = 0
        try:
            report = sdk_rendering.support("rendering.threejs", timeline_path=timeline_path)
        except BaseException as exc:
            evidence["outcome"] = {
                "status": "exception",
                "exception_type": type(exc).__name__,
                "exception_text": scrub_text(str(exc))[:4096],
            }
            mark("support.exception", type=type(exc).__name__)
        else:
            evidence["outcome"] = {
                "status": "returned",
                "report_type": type(report).__name__,
                "supported": report.supported,
                "reasons": list(report.reasons),
            }
            mark("support.return", report_type=type(report).__name__, supported=report.supported)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
        sdk_rendering._support_report = original_support_report
        CommandTransport.run = original_run
        transport_module.popen_owned_process = original_owned
        subprocess.Popen.__init__ = original_popen_init
        subprocess.Popen.communicate = original_communicate

    after_body = body_facts(TARGET)
    evidence["postflight"] = {
        "target_body_after": after_body,
        "target_body_unchanged": before_body == after_body,
        "receipt_sha256": sha(RECEIPT),
        "host_status": status(),
        "git_diff_check": subprocess.run(
            ["git", "diff", "--check"], cwd=ROOT, check=False
        ).returncode,
    }
    child_env_keys = set()
    for row in evidence["trace"]["popen"]:
        if row.get("pid"):
            child_env_keys.update(row.get("environment_keys", []))
    evidence["profile_delivery"] = {
        "required_existing_profile_keys": [
            "ASTRID_HOST_EXECUTION_PROFILE",
            "ASTRID_REMOTION_PROJECT_DIR",
            "ASTRID_NODE_EXECUTABLE",
            "ASTRID_TEST_NODE_MODULES",
        ],
        "child_environment_keys": sorted(child_env_keys),
        "missing_required_keys": sorted(
            {
                "ASTRID_HOST_EXECUTION_PROFILE",
                "ASTRID_REMOTION_PROJECT_DIR",
                "ASTRID_NODE_EXECUTABLE",
                "ASTRID_TEST_NODE_MODULES",
            }
            - child_env_keys
        ),
        "transport_timeout_observed": next(
            (
                event.get("timeout")
                for event in evidence["trace"]["events"]
                if event.get("event") == "CommandTransport.run.entry"
            ),
            None,
        ),
    }
    evidence["diagnostic"]["elapsed_seconds"] = time.monotonic() - start
    (EVIDENCE / "diagnostic.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": evidence.get("outcome"), "evidence": str(EVIDENCE / "diagnostic.json"), "elapsed_seconds": evidence["diagnostic"]["elapsed_seconds"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except BaseException as exc:
        print(json.dumps({"harness_exception": type(exc).__name__, "text": scrub_text(str(exc))[:4096]}), file=sys.stderr)
        raise
