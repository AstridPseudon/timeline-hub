#!/usr/bin/env python3
"""Private final-service runner retained outside disposable Runtime worktrees.

Source: joined F-final private candidate; D117 core lineage, D117 core-inventory successor to the reviewed D84 candidate.
The service rows verify this file's SHA256 before executing it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile

REQUIRED_TUPLE_REPOS = {"agent", "runtime", "app", "composition"}
REVIEWED_BUILDER_SHA256 = "ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca"
BUILDER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build")
PYTHON = "/home/user/work/venv-runtime/bin/python"
SOURCE_ROOTS = {name: Path("/home/user/work") / name for name in REQUIRED_TUPLE_REPOS}
CORE_INVENTORY = Path(__file__).resolve().with_name("core-inventory.json")
CORE_INVENTORY_SHA256 = "e6a1fa17796e493532c3927e2ec6fc8fdb4e1928b7540be8c6644b3d0894bb14"
AGENT_RUNTIME_FILES = {
    "astrid/core/timeline/schema/timeline-config.schema.json": "contract/schemas/timeline-config.schema.json",
    **{f"astrid_runtime_client/{name}.py": f"packages/python/astrid_runtime_client/{name}.py"
       for name in ("__init__", "contract_metadata", "generated", "timeline_commit_types")},
    **{f"tests/fixtures/runtime-responses/{name}.json": f"conformance/responses/{name}.json"
       for name in ("events_page_1_200", "events_page_2_200", "invalid_cursor_400",
                    "managed_outputs_200", "not_found_404", "task_admission_201",
                    "task_read_200", "validation_error_422")},
    "tests/fixtures/runtime-responses/publish_conflict_409.json": "conformance/responses/commit_conflict_409.json",
    "tests/fixtures/visual-boundary-v1.json": "conformance/fixtures/visual-boundary-v1.json",
}

def load_core_test_files(path: Path = CORE_INVENTORY) -> list[str]:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"core inventory is not a regular file: {path}")
    try:
        raw = path.read_bytes()
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid core inventory: {path}: {exc}") from exc
    selector = value.get("core_selector") if isinstance(value, dict) else None
    targets = selector.get("python_targets") if isinstance(selector, dict) else None
    expected_count = selector.get("python_target_count") if isinstance(selector, dict) else None
    if (
        not isinstance(targets, list)
        or type(expected_count) is not int
        or expected_count != 101
        or len(targets) != expected_count
        or any(
            not isinstance(target, str)
            or re.fullmatch(r"tests/test_[a-z0-9_]+\.py", target) is None
            for target in targets
        )
        or len(targets) != len(set(targets))
    ):
        raise ValueError("core inventory Python selector is invalid")
    if hashlib.sha256(raw).hexdigest() != CORE_INVENTORY_SHA256:
        raise ValueError("core inventory hash mismatch")
    return targets


CORE_TEST_FILES = load_core_test_files()
CORE_COMMAND = (
    PYTHON + " -m pytest -q -o addopts= -p no:cacheprovider "
    + " ".join(CORE_TEST_FILES)
    + ' && cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test'
    + ' && cd "$ASTRID_RUNTIME_CHECKOUT"'
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_builder(path: Path, expected: str) -> None:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"builder is not a regular file: {path}")
    actual = digest(path.read_bytes())
    if actual != expected:
        raise ValueError(f"reviewed builder hash mismatch: {actual} != {expected}")


def git_value(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot inspect source tuple repository {root}: {exc}") from exc


def git_parents(root: Path, ref: str) -> list[str]:
    value = git_value(root, "rev-list", "--parents", "-n", "1", ref)
    values = value.split()
    if not values or values[0] != git_value(root, "rev-parse", ref):
        raise ValueError(f"cannot establish commit identity for {root}")
    return values[1:]


def git_subject(root: Path, ref: str) -> str:
    return git_value(root, "show", "-s", "--format=%s", ref)


def git_status(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain"],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"cannot inspect source status {root}: {exc}") from exc


def validate_source_tuple(
    path: Path,
    expected_sha: str | None = None,
    *,
    runtime_root: Path | None = None,
) -> dict[str, dict[str, str]]:
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise ValueError(f"final source tuple must be an absolute regular file: {path}")
    raw = path.read_bytes()
    if expected_sha is not None and digest(raw) != expected_sha:
        raise ValueError("final source tuple file hash changed")
    try:
        value = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid final source tuple: {path}: {exc}") from exc
    if not isinstance(value, dict) or set(value) != REQUIRED_TUPLE_REPOS:
        raise ValueError("final source tuple must name exactly agent, runtime, app, composition")
    for name, item in value.items():
        if not isinstance(item, dict) or set(item) != {"root", "sha", "tree"}:
            raise ValueError(f"final source tuple entry {name} must contain root, sha, tree")
        if not isinstance(item["root"], str) or not Path(item["root"]).is_absolute():
            raise ValueError(f"final source tuple {name}.root must be an absolute path")
        declared_root = Path(item["root"])
        if declared_root.is_symlink():
            raise ValueError(f"final source tuple {name}.root must not be a symlink")
        root = declared_root.resolve()
        if name == "runtime" and runtime_root is not None:
            root = runtime_root.resolve()
        sha = item["sha"]
        tree = item["tree"]
        if not isinstance(sha, str) or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError(f"final source tuple {name}.sha is not a lowercase Git SHA")
        if not isinstance(tree, str) or len(tree) != 40 or any(c not in "0123456789abcdef" for c in tree):
            raise ValueError(f"final source tuple {name}.tree is not a lowercase Git tree")
        if git_value(root, "rev-parse", "--is-inside-work-tree") != "true":
            raise ValueError(f"final source tuple root is not a Git worktree: {root}")
        actual_head = git_value(root, "rev-parse", "HEAD")
        actual_tree = git_value(root, "rev-parse", "HEAD^{tree}")
        if actual_tree != tree:
            raise ValueError(f"final source tuple tree drift for {name}: {actual_tree} != {tree}")
        if actual_head != sha:
            # bin/test-run creates a synthetic commit with the
            # exact tested tree and the selected source commit as its only
            # parent.  The packet records that original source parent, not the
            # service-owned snapshot commit, so HEAD must not be required to
            # equal the packet SHA in this one approved form.
            parents = git_parents(root, "HEAD")
            if (
                name != "runtime"
                or runtime_root is None
                or len(parents) != 1
                or parents[0] != sha
                or not git_subject(root, "HEAD").startswith("test snapshot ")
            ):
                raise ValueError(f"final source tuple commit drift for {name}: {actual_head} != {sha}")
        if git_status(root):
            raise ValueError(f"final source tuple source is dirty: {root}")
    return value


def _owned_tmp_root(service_tmp: Path) -> Path:
    service_tmp = service_tmp.absolute()
    if not service_tmp.is_dir() or service_tmp.is_symlink():
        raise ValueError(f"service TMPDIR must be a real directory: {service_tmp}")
    return Path(tempfile.mkdtemp(prefix="timeline-delivery-", dir=service_tmp))


def _remove_owned_tmp(root: Path, service_tmp: Path) -> None:
    root = root.absolute()
    service_tmp = service_tmp.absolute()
    if root.parent != service_tmp or root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"refusing to clean non-owned delivery TMPDIR: {root}")
    shutil.rmtree(root)


def run_private_command(
    command: list[str],
    *,
    cwd: Path | None = None,
    service_tmp: Path | None = None,
    timeout_seconds: int = 30 * 60,
    kill_grace_seconds: int = 45,
) -> int:
    """Run a final service under an owned TMPDIR and clean only that root."""
    if not command or any(not isinstance(value, str) or not value for value in command):
        raise ValueError("private delivery command must be a non-empty argv")
    if timeout_seconds <= 0 or kill_grace_seconds < 0:
        raise ValueError("private delivery timeout values must be positive")
    service_tmp = Path(os.environ.get("TMPDIR", tempfile.gettempdir())) if service_tmp is None else service_tmp
    service_tmp = service_tmp.absolute()
    root = _owned_tmp_root(service_tmp)
    env = os.environ.copy()
    env.update(TMPDIR=str(root), TMP=str(root), TEMP=str(root))
    process: subprocess.Popen[bytes] | None = None
    result = 1
    previous_handlers = {}

    def interrupted(signum, frame):
        raise InterruptedError(signum)

    try:
        for signum in (signal.SIGTERM, signal.SIGINT):
            previous_handlers[signum] = signal.signal(signum, interrupted)
        process = subprocess.Popen(command, cwd=cwd, env=env, start_new_session=True)
        try:
            result = process.wait(timeout=timeout_seconds)
        except (subprocess.TimeoutExpired, InterruptedError) as exc:
            result = 124 if isinstance(exc, subprocess.TimeoutExpired) else 128 + exc.args[0]
            # Repeated cancellation must not interrupt termination and cleanup.
            for signum in previous_handlers:
                signal.signal(signum, signal.SIG_IGN)
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=kill_grace_seconds)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
        return result if result >= 0 else 128 - result
    finally:
        for signum in previous_handlers:
            signal.signal(signum, signal.SIG_IGN)
        try:
            if process is not None:
                # A child may leave descendants even after its own exit.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
            _remove_owned_tmp(root, service_tmp)
        finally:
            for signum, handler in previous_handlers.items():
                signal.signal(signum, handler)


def validate_roots(value: dict[str, dict[str, str]]) -> None:
    for name, item in value.items():
        root = Path(item["root"])
        if not root.is_absolute() or root.is_symlink() or not root.is_dir():
            raise ValueError(f"final source tuple {name}.root is not a pinned checkout")


def validate_agent_lock(value: dict[str, dict[str, str]], env: dict[str, str] | None = None) -> dict:
    agent = Path(value["agent"]["root"])
    producer = Path(value["runtime"]["root"])
    path = agent / "runtime.lock.json"
    if not path.is_file() or path.is_symlink():
        raise ValueError("Agent runtime lock must be a regular file")
    raw = path.read_bytes()
    lock = json.loads(raw)
    if (
        not isinstance(lock, dict)
        or lock.get("producer") != "astrid-runtime"
        or lock.get("manifest") != "contract/artifacts.json"
        or lock.get("source_commit") != value["runtime"]["sha"]
    ):
        raise ValueError("Agent runtime lock does not select the final Runtime producer")
    version = lock.get("producer_version")
    if (
        not isinstance(version, str) or not version.startswith("sha256:")
        or len(version) != 71 or any(c not in "0123456789abcdef" for c in version[7:])
    ):
        raise ValueError("Agent runtime lock producer_version must be a SHA256 digest")
    files = lock.get("files")
    if not isinstance(files, dict) or set(files) != set(AGENT_RUNTIME_FILES):
        raise ValueError("Agent runtime lock must contain all 15 canonical files")
    for consumer, source in AGENT_RUNTIME_FILES.items():
        entry = files[consumer]
        if not isinstance(entry, dict) or set(entry) != {"from", "sha256"} or entry["from"] != source:
            raise ValueError(f"Agent runtime lock canonical mapping changed: {consumer}")
        sha = entry["sha256"]
        if (
            not isinstance(sha, str) or not sha.startswith("sha256:")
            or len(sha) != 71 or any(c not in "0123456789abcdef" for c in sha[7:])
        ):
            raise ValueError(f"Agent runtime lock hash is invalid: {consumer}")
    # Use the normal consumer/producer checks against the selected integration
    # source, whose identity is checked separately from the service snapshot.
    # This preserves vendor_lock's committed-manifest and all artifact checks
    # while allowing the approved same-tree Runtime snapshot/source-parent form.
    try:
        subprocess.check_output(
            [PYTHON, str(agent / "scripts/vendor_lock.py"), "check", str(path),
             "--producer", str(producer)],
            env=env, text=True, stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise ValueError(f"Agent Runtime vendor check failed: {exc.output}") from exc
    return {"lock_sha256": digest(raw), "files": {name: digest((agent / name).read_bytes()) for name in files}}


def source_identity(path: Path, expected_sha: str, runtime: Path, env: dict[str, str]) -> dict:
    value = validate_source_tuple(path, expected_sha)
    validate_roots(value)
    validate_source_tuple(path, expected_sha, runtime_root=runtime)
    # delivery-build reads tl/integration, rather than HEAD. Check both.
    for name, item in value.items():
        root = Path(item["root"])
        if git_value(root, "rev-parse", "HEAD") != item["sha"]:
            raise ValueError(f"final source tuple checkout drift for {name}")
    probe = '''import importlib,json,pathlib
modules = ("runtime_protocol", "astrid", "astrid_runtime_client", "astrid.sdk.timeline.commit")
print(json.dumps({name: str(pathlib.Path(importlib.import_module(name).__file__).resolve()) for name in modules}, sort_keys=True))'''
    origins = json.loads(subprocess.check_output([PYTHON, "-c", probe], env=env, text=True))
    agent = SOURCE_ROOTS["agent"]
    expected = {
        "runtime_protocol": str(runtime / "runtime_protocol/__init__.py"),
        "astrid": str(agent / "astrid/__init__.py"),
        "astrid_runtime_client": str(agent / "astrid_runtime_client/__init__.py"),
        "astrid.sdk.timeline.commit": str(agent / "astrid/sdk/timeline/commit.py"),
    }
    if origins != expected:
        raise ValueError(f"final service imported different source modules: {origins}")
    return {"tuple": value, "runtime_head": git_value(runtime, "rev-parse", "HEAD"),
            "origins": origins, "agent_runtime_lock": validate_agent_lock(value, env)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-tuple", type=Path, required=True)
    parser.add_argument("--tuple-sha", required=True)
    parser.add_argument("service", choices=("core", "delivery", "delivery-dryrun"))
    args = parser.parse_args()
    selected = validate_source_tuple(args.source_tuple, args.tuple_sha)
    runtime = Path(selected["runtime"]["root"]).resolve()
    env = os.environ.copy()
    env.update(
        PYTHONDONTWRITEBYTECODE="1",
        ASTRID_CHECKOUT=str(SOURCE_ROOTS["agent"]),
        ASTRID_RUNTIME_CHECKOUT=str(runtime),
        PYTHONPATH=f"{runtime}:{SOURCE_ROOTS['agent']}:{runtime / 'packages/python'}",
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_OPTIONAL_LOCKS="0",
        TIMELINE_DELIVERY_SCRIPT_SHA=REVIEWED_BUILDER_SHA256,
    )
    # One environment covers the source probe, every test/build phase, and recheck.
    os.environ.update(env)
    before = source_identity(args.source_tuple, args.tuple_sha, runtime, env)
    if args.service == "core":
        print("Runtime source-mode v2 commit door preflight PASS", flush=True)
        command = ["/bin/bash", "-Eeuo", "pipefail", "-c", CORE_COMMAND]
    else:
        validate_builder(BUILDER, REVIEWED_BUILDER_SHA256)
        command = ["python3", str(BUILDER)]
        if args.service == "delivery-dryrun":
            command.append("--dry-run")
        command.extend(["--repos", "agent runtime app composition"])
    result = run_private_command(command, cwd=runtime)
    after = source_identity(args.source_tuple, args.tuple_sha, runtime, env)
    if before != after:
        raise ValueError("final service source identity changed during execution")
    if args.service != "core":
        validate_builder(BUILDER, REVIEWED_BUILDER_SHA256)
    return result


if __name__ == "__main__":
    raise SystemExit(main())

