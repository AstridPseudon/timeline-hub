#!/usr/bin/env python3
"""Private D127a diagnostic; exact pinned predicates, never a registration gate.

Run with python3.13 -I -B. No installed child code is imported or executed.
Successful subchecks are observations, not a COMPLETE ownership verdict.
"""

import argparse
import ast
import base64
import contextlib
import csv
import fnmatch
import hashlib
import importlib.machinery
import importlib.metadata
import importlib.util
import io
import json
import marshal
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
import time
import tomllib
import types
import uuid
from urllib.parse import unquote, urlparse


TASK = "rt-OPS-Farm-census-sol-1530"
PINS = {
    "make-child-venv": "e62f89eaf226897a36bd4c7f715d43a7a1d4206ff371432296c01de6bdd52dc3",
    "bench_store.py": "7d5870433a76b7a611703f47a385cba9584f7213fe4b8a27005317f27bf26495",
    "verify_dependency_seed.py": "116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2",
}
AGENT = "a4e016b6a9f91fbe372672bdcf382c630bf59186"
RUNTIME = "5e9ad1c6f74241d8771d3284fdd2ce7a214fd344"
SCHEMA = "242f9c4306bf3b501222cb041a9eb246ef47bc85:packages/timeline-schema/python"
MAX_REPORT = 1024 * 1024


class Incomplete(BaseException):
    pass


def message(error):
    value = str(error)
    if "://" in value or "\n" in value:
        return type(error).__name__ + " (detail withheld)"
    return value[:300]


class Bounds:
    """Audit file opens and directory scans; alarm also bounds blocked syscalls."""

    def __init__(self, seconds):
        self.end = time.monotonic() + seconds
        self.bytes = 0
        self.operations = 0
        self.events = 0
        self.active = True
        self.executed = set()
        self.code_files = set()
        self.refusal_calls = []

    def tick(self):
        if time.monotonic() >= self.end:
            raise Incomplete("deadline exhausted")
        self.operations += 1
        if self.operations > 100_000:
            raise Incomplete("filesystem operation budget exhausted")

    def trace(self, frame, event, arg):
        self.events += 1
        if self.events > 10_000_000:
            raise Incomplete("execution event budget exhausted")
        if self.events % 1000 == 0:
            self.tick()
        if event == "call" and frame.f_code.co_filename in self.code_files:
            self.executed.add((frame.f_code.co_filename, frame.f_code.co_name,
                               frame.f_code.co_firstlineno))
            if frame.f_code.co_name == "fail" or (frame.f_code.co_name == "check" and
                                                 frame.f_locals.get("ok") is False):
                caller = frame.f_back
                paths = {}
                if caller is not None:
                    for key in ("path", "installed", "carrier", "source", "root"):
                        value = caller.f_locals.get(key)
                        if isinstance(value, Path) and value.is_absolute():
                            paths[key] = str(value)
                if len(self.refusal_calls) >= 128:
                    raise Incomplete("production refusal trace budget exhausted")
                self.refusal_calls.append({"source": frame.f_code.co_filename,
                                           "line": caller.f_lineno if caller else None,
                                           "reason": message(frame.f_locals.get("message", "")),
                                           "caller_paths": paths})
        return self.trace

    def audit(self, event, args):
        if not self.active:
            return
        if event == "open":
            self.tick()
            path, mode, flags = args
            if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                raise Incomplete("read-only boundary: writable open")
            info = os.fstat(path) if isinstance(path, int) else os.stat(path)
            if not stat.S_ISREG(info.st_mode):
                raise Incomplete("read budget requires a regular file")
            self.bytes += info.st_size
            if info.st_size > 32 * 1024 * 1024 or self.bytes > 256 * 1024 * 1024:
                raise Incomplete("file/read byte budget exhausted")
        elif event in {"os.scandir", "os.listdir"}:
            self.tick()
        elif (event.startswith(("subprocess.", "socket.", "os.exec", "os.spawn"))
              or event in {"os.system", "os.fork", "os.forkpty", "os.mkdir", "os.remove",
                           "os.rmdir", "os.rename", "os.link", "os.symlink", "os.chmod",
                           "os.chown", "os.truncate", "os.utime", "fcntl.flock", "fcntl.fcntl"}):
            raise Incomplete("read-only/no-process boundary: " + event)
        elif event == "exec":
            filename = args[0].co_filename
            # Only authenticated kit snippets and trusted host libraries execute.
            # Child bytecode may be decoded for comparison, never executed.
            if filename not in self.code_files and not any(
                filename.startswith(prefix) for prefix in HOST_LIBRARIES
            ):
                raise Incomplete("untrusted code execution boundary")


HOST_LIBRARIES = tuple(str(Path(p).resolve()) + "/" for p in sys.path
                       if p and Path(p).is_dir() and "/lib/python" in str(Path(p).resolve()))


def physical(path):
    if not path.is_absolute() or ".." in path.parts or path != path.resolve():
        raise ValueError("absolute physical path required")
    return path


def safe_output(output, inputs):
    physical(output)
    physical(output.parent)
    if not output.parent.is_dir() or output.exists() or output.is_symlink():
        raise ValueError("output must be a new file in an existing physical directory")
    # Reject both ancestor and descendant overlaps, including symlink aliases.
    for item in inputs:
        item = item.resolve()
        if output.is_relative_to(item) or item.is_relative_to(output):
            raise ValueError("output overlaps an input/source")


def definitions(text, filename):
    tree = ast.parse(text, filename)
    selected = [node for node in tree.body
                if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef))]
    namespace = {"__name__": "pinned_diagnostic", "__file__": filename}
    exec(compile(ast.Module(body=selected, type_ignores=[]), filename, "exec"), namespace)
    return tree, namespace


def root_guards(root, tree, namespace, bounds, record, staging):
    """Evaluate the unchanged readonly() predicates independently per path.

    This is deliberately specific to pinned e62f, not a general AST executor.
    The original fail() still raises; one failing node never authorizes another.
    """
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "readonly")
    first, loop = function.body
    ownership, internal_link, unsafe = loop.body[2:]
    if not (isinstance(first, ast.If) and isinstance(loop, ast.For)
            and all(isinstance(n, ast.If) for n in (ownership, internal_link, unsafe))
            and isinstance(internal_link.body[0], ast.Continue)):
        raise ValueError("pinned readonly AST layout mismatch")
    namespace.update(root=root, staging=staging)

    def predicate(node):
        return eval(compile(ast.Expression(node.test), namespace["__file__"], "eval"), namespace)

    if predicate(first):
        record("root-physical", "REFUSED", path=str(root), reason="missing or symlinked root")
        return
    pending = [root]
    seen = 0
    while pending:
        bounds.tick()
        path = pending.pop()
        try:
            info = path.lstat()
            namespace.update(path=path, info=info, mode=info.st_mode)
            for name, node in (("ownership/hardlink", ownership),):
                if predicate(node):
                    record(name, "REFUSED", path=str(path), source_line=node.lineno)
            if not predicate(internal_link) and predicate(unsafe):
                record("type/symlink/writable", "REFUSED", path=str(path), source_line=unsafe.lineno)
            seen += 1
            if stat.S_ISDIR(info.st_mode):
                with os.scandir(path) as children:
                    for child in children:
                        bounds.tick()
                        pending.append(Path(child.path))
        except Exception as error:
            record("root-node", "ERROR", path=str(path), exception=type(error).__name__)
    record("root-predicates", "OBSERVED", nodes=seen, staging=staging,
           note="only exact readonly predicates; no RECORD/source/dependency coverage")


def run(args, bounds):
    rows = []

    def record(check, status, **detail):
        if len(rows) >= 2048:
            raise Incomplete("diagnostic row budget exhausted")
        rows.append(dict(check=check, status=status, **detail))

    def attempt(check, fn):
        try:
            value = fn()
        except Incomplete as error:
            record(check, "SKIPPED", reason=message(error))
        except SystemExit as error:
            record(check, "REFUSED", reason=message(error))
        except Exception as error:
            if type(error).__name__ == "Refused" and type(error).__module__ == "pinned_store":
                record(check, "REFUSED", reason=message(error))
            else:
                record(check, "ERROR", exception=type(error).__name__)
        else:
            record(check, "OBSERVED", note="function returned; not full coverage")
            return value
        return None

    report = {"task": TASK, "result": "INCOMPLETE", "checks": rows,
              "diagnostic_fitness": "PARTIAL_SOURCE_DIAGNOSTIC_REVIEW_REQUIRED",
              "schema_tree": SCHEMA, "source_hashes": {}, "missing": [],
              "coverage": "Exact predicates/calls only. OBSERVED is not a PASS or COMPLETE verdict."}
    try:
        sources = {}
        for name, expected in PINS.items():
            path = physical(args.maker if name == "make-child-venv" else args.maker.parent / name)
            data = path.read_bytes()
            actual = hashlib.sha256(data).hexdigest()
            report["source_hashes"][name] = actual
            if actual != expected:
                raise ValueError("installed source pin mismatch: " + name)
            sources[name] = data.decode()
            bounds.code_files.add(str(path))
        if args.agent_sha != AGENT or args.runtime_sha != RUNTIME:
            raise ValueError("only the exact a4e016/5e9ad caller is supported")
        client_rows = args.client.splitlines()
        if not client_rows or len(set(client_rows)) != len(client_rows) or any(
            re.fullmatch(r"packages/python/astrid_runtime_client/[A-Za-z0-9_/.]+=[0-9a-f]{64}", row) is None
            or ".." in row.split("=", 1)[0].split("/") for row in client_rows
        ):
            raise ValueError("client must be the original caller's path=SHA256 lines")
        if len({row.split("=", 1)[0] for row in client_rows}) != len(client_rows):
            raise ValueError("duplicate client path")
        required = {"retained staged child": args.root, "Store root": args.work_root / "bench-store",
                    "physical Agent checkout": args.agent_checkout,
                    "physical Runtime checkout": args.runtime_checkout,
                    "Farm schema checkout": args.farm_source,
                    "Store tests directory": args.tests}
        invalid = False
        for name, path in required.items():
            bounds.tick()
            if not path.exists() and not path.is_symlink():
                report["missing"].append({"input": name, "path": str(path)})
            elif path.is_symlink() or not path.is_dir():
                invalid = True
                record("prerequisite:" + name, "REFUSED", path=str(path), reason="physical directory required")
            else:
                physical(path)
        if report["missing"] or invalid:
            report["result"] = "INCOMPLETE" if invalid else "EXACTMISSING"
            for check in ("STORE_VERIFY including RECORD/license/source/manifest",
                          "Store caller/constructor/index/locks/registration/projection",
                          "dependency retained-bootstrap/Farm/wheel/installed binding"):
                record(check, "SKIPPED", reason="required input absent or invalid; see prerequisites")
            return report

        maker = sources["make-child-venv"]
        begin = maker.index("# STORE_VERIFY_BEGIN\n") + len("# STORE_VERIFY_BEGIN\n")
        verifier = "\n" * maker[:begin].count("\n") + maker[begin:].split("# STORE_VERIFY_END", 1)[0]
        filename = str(args.maker)
        tree, namespace = definitions(verifier, filename)
        namespace["__file__"] = filename
        attempt("independent retained path predicates", lambda: root_guards(
            args.root, tree, namespace, bounds, record, args.staging))

        saved_argv = sys.argv
        inventory_output = io.StringIO()
        try:
            sys.argv = ["verifier", str(args.root), args.client, str(args.agent_checkout), AGENT,
                        str(args.runtime_checkout), RUNTIME, str(args.work_root), args.python,
                        "--farm-source", str(args.farm_source)] + (["--staging"] if args.staging else [])
            def embedded():
                with contextlib.redirect_stdout(inventory_output):
                    exec(compile(verifier, filename, "exec"), {"__file__": filename})
                return json.loads(inventory_output.getvalue())
            inventory = attempt("exact full STORE_VERIFY (first-refusal semantics)", embedded)
        finally:
            sys.argv = saved_argv
        if inventory is None:
            record("STORE_VERIFY downstream RECORD/license/sourcecarrier/sourcehash/retained manifest",
                   "SKIPPED", reason="full embedded verifier did not return authenticated inventory; no downstream coverage inferred")

        # These Store reads are independently callable on the real metadata.
        # No Store.ensure(), mutex(), recovery, journal, publication or installer runs.
        store_path = str(args.maker.parent / "bench_store.py")
        module = types.ModuleType("pinned_store")
        module.__file__ = store_path
        exec(compile(sources["bench_store.py"], store_path, "exec"), module.__dict__)
        store = attempt("Store.__init__", lambda: module.Store(args.work_root / "bench-store", args.tests))
        if store is not None:
            index = attempt("Store._load/_validate_index/_validate_entry/_owned_dir", store._load)
            if index is not None:
                attempt("Store._verify_projection", lambda: store._verify_projection(index))
            else:
                record("Store._verify_projection", "SKIPPED", reason="valid index prerequisite unavailable")
        else:
            record("Store index/ownership/projection", "SKIPPED", reason="Store constructor prerequisite unavailable")
        record("Store mutex/lease ownership guards", "SKIPPED",
               reason="exact production context requires writable lock handles/locking; Store reads lack transactional lock consistency")
        record("Store._registration candidate binding", "SKIPPED",
               reason="candidate requires successful full verify()/report_bytes()/registration callback; authenticated candidate unavailable")
        record("Store mutation bodies", "OUT_OF_SCOPE",
               reason="ensure journal/build/eviction/publication/projection writes are excluded actions, not missing census coverage to pad a static count")

        # main(local_inventory=...) is reached only after successful STORE_VERIFY.
        # Farm mode precedes it with retained_farm(), which calls farm_inputs()
        # and writes a temporary wheel extraction. Never execute that write path.
        record("dependency retained_farm/farm_inputs/schema_archive", "SKIPPED",
               reason="Farm authority requires pinned component plus exact source/bootstrap inputs; farm_inputs performs temporary writes")
        record("dependency main(--installed, local_inventory=...)", "SKIPPED",
               reason=("authenticated embedded local_inventory prerequisite unavailable" if inventory is None else
                       "Farm authority prerequisite not executed read-only"))
        record("dependency store_metadata retained staging key/owner/bootstrap binding", "SKIPPED",
               reason="requires authenticated bootstrap identity and Farm authority; a staging tree is not an indexed published entry")
        record("maker verify() child freeze-identity/registration callback", "SKIPPED",
               reason="production executes child Python/imports; forbidden installed-code execution; registration is not authorized")
        record("source authentication via committed_files/git archive", "SKIPPED",
               reason="no subprocess/Git allowed; canonical schema argument retained exactly, never replaced with whole commit")
    except Incomplete as error:
        rows.append(dict(check="global budget/read-only boundary", status="SKIPPED", reason=message(error)))
    except Exception as error:
        record("diagnostic unexpected exception", "ERROR", exception=type(error).__name__, reason=message(error))
    finally:
        for name, expected in PINS.items():
            try:
                current = hashlib.sha256((args.maker if name == "make-child-venv" else
                                          args.maker.parent / name).read_bytes()).hexdigest()
                if current != expected:
                    report["result"] = "INCOMPLETE"
                    rows.append(dict(check="final source pin", status="ERROR", source=name))
            except BaseException as error:
                report["result"] = "INCOMPLETE"
                rows.append(dict(check="final source pin", status="SKIPPED", source=name,
                                 exception=type(error).__name__))
        report["executed_functions"] = [{"source": path, "function": name, "line": line}
                                         for path, name, line in sorted(bounds.executed)]
        report["limits_used"] = {"file_bytes_charged": bounds.bytes, "operations": bounds.operations,
                                 "trace_events": bounds.events}
        report["production_refusal_calls"] = bounds.refusal_calls
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("maker", "root", "agent-checkout", "runtime-checkout", "work-root", "tests", "farm-source", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--client", required=True)
    parser.add_argument("--agent-sha", default=AGENT)
    parser.add_argument("--runtime-sha", default=RUNTIME)
    parser.add_argument("--python", default="python3.13")
    parser.add_argument("--staging", action="store_true")
    parser.add_argument("--deadline-seconds", type=int, default=180)
    args = parser.parse_args()
    output_fd = None
    bounds = None
    try:
        if not sys.flags.isolated or not sys.dont_write_bytecode:
            raise ValueError("invoke with -I -B")
        if not 1 <= args.deadline_seconds <= 900:
            raise ValueError("deadline must be 1..900 seconds")
        def alarm(signum, frame):
            raise Incomplete("hard wall-clock deadline exhausted")
        signal.signal(signal.SIGALRM, alarm)
        signal.setitimer(signal.ITIMER_REAL, args.deadline_seconds)
        bounds = Bounds(args.deadline_seconds)
        resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
        inputs = [args.root, args.agent_checkout, args.runtime_checkout, args.work_root,
                  args.tests, args.farm_source, args.maker.parent, Path(__file__),
                  Path(sys.executable), *[Path(p) for p in HOST_LIBRARIES]]
        interpreter = shutil.which(args.python)
        if interpreter:
            inputs.append(Path(interpreter))
        safe_output(args.output, inputs)
        # Exclusive creation, never truncation. Inputs cannot alias a preexisting
        # output via hardlink, and all symlink ancestors were rejected above.
        output_fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        sys.addaudithook(bounds.audit)
        sys.settrace(bounds.trace)
        report = run(args, bounds)
    except BaseException as error:
        report = {"task": TASK, "result": "INCOMPLETE", "fatal": type(error).__name__,
                  "reason": message(error)}
    finally:
        sys.settrace(None)
        signal.setitimer(signal.ITIMER_REAL, 0)
        if bounds is not None:
            bounds.active = False
    data = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    if len(data) > MAX_REPORT:
        data = (json.dumps({"task": TASK, "result": "INCOMPLETE", "reason": "report budget exhausted"}) + "\n").encode()
    if output_fd is None:
        sys.stderr.write(data.decode())
    else:
        try:
            with os.fdopen(output_fd, "wb") as stream:
                stream.write(data)
        except BaseException as error:
            sys.stderr.write(json.dumps({"task": TASK, "result": "INCOMPLETE",
                                         "fatal": "output write failed", "exception": type(error).__name__}) + "\n")
            return 2
    return 3 if report["result"] == "EXACTMISSING" else 2


if __name__ == "__main__":
    raise SystemExit(main())
