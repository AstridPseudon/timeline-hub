#!/usr/bin/env python3
"""Private final-service runner retained outside disposable Runtime worktrees.

Source: tl/rt-F-final-service-sol-1244, based on candidate 1e1f32dd0.
The service rows verify this file's SHA256 before executing it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile

REQUIRED_TUPLE_REPOS = {"agent", "runtime", "app", "composition"}
REVIEWED_BUILDER_SHA256 = "f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708"
BUILDER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build")
PYTHON = "/home/user/work/venv-runtime/bin/python"
SOURCE_ROOTS = {name: Path("/home/user/work") / name for name in REQUIRED_TUPLE_REPOS}

CORE_TEST_FILES = """
tests/test_timeline_absent_head_repair_integration.py
tests/test_timeline_authority_door.py
tests/test_timeline_bundle2_contract.py
tests/test_timeline_catalog_history_integration.py
tests/test_timeline_clip_replacement.py
tests/test_timeline_commit_acceptance.py
tests/test_timeline_commit_archive_replay.py
tests/test_timeline_commit_authentication.py
tests/test_timeline_commit_baseline.py
tests/test_timeline_commit_closure_invariants.py
tests/test_timeline_commit_contract.py
tests/test_timeline_commit_crash.py
tests/test_timeline_commit_execution.py
tests/test_timeline_commit_film_fixture.py
tests/test_timeline_commit_input_integration.py
tests/test_timeline_commit_inputs.py
tests/test_timeline_commit_integration.py
tests/test_timeline_commit_port.py
tests/test_timeline_commit_producer.py
tests/test_timeline_commit_provider.py
tests/test_timeline_commit_read_basis.py
tests/test_timeline_commit_restore_integration.py
tests/test_timeline_commit_restore_port.py
tests/test_timeline_commit_routes.py
tests/test_timeline_commit_sequential_verifier.py
tests/test_timeline_commit_type_generator.py
tests/test_timeline_commit_validation.py
tests/test_timeline_current_union_contract.py
tests/test_timeline_cutover.py
tests/test_timeline_dispatch_context.py
tests/test_timeline_document_authority.py
tests/test_timeline_document_object_contract.py
tests/test_timeline_effect_authority.py
tests/test_timeline_empty_shell_repair.py
tests/test_timeline_fresh_bootstrap_scope.py
tests/test_timeline_headless_overwrite_refused.py
tests/test_timeline_history_authenticated_read.py
tests/test_timeline_history_boundaries.py
tests/test_timeline_internal_nesting.py
tests/test_timeline_inverse_historical_image.py
tests/test_timeline_inverse_occurrence_retirement.py
tests/test_timeline_inverse_stage_authentication.py
tests/test_timeline_legacy_authority.py
tests/test_timeline_legacy_occupancy.py
tests/test_timeline_media_completion_fence.py
tests/test_timeline_media_selection.py
tests/test_timeline_names.py
tests/test_timeline_native_inspection.py
tests/test_timeline_null_speed_retained.py
tests/test_timeline_ordinary_http.py
tests/test_timeline_pack_document_read.py
tests/test_timeline_pack_inputs.py
tests/test_timeline_pack_param_retained_read.py
tests/test_timeline_portable_pack_integration.py
tests/test_timeline_producer_checkpoint.py
tests/test_timeline_producer_guards.py
tests/test_timeline_producer_record_boundary.py
tests/test_timeline_projection_occupancy.py
tests/test_timeline_public_s2_mixed_cli_journey.py
tests/test_timeline_raw_capture.py
tests/test_timeline_raw_payload_contract.py
tests/test_timeline_reads_after_cut.py
tests/test_timeline_reference_authority.py
tests/test_timeline_render_publication.py
tests/test_timeline_render_publication_authority.py
tests/test_timeline_shared_inverse_authority.py
tests/test_timeline_shot_authority.py
tests/test_timeline_source_document_boundary.py
tests/test_timeline_source_duplicate_authority.py
tests/test_timeline_text_binding_clear.py
tests/test_timeline_text_legacy_custody.py
tests/test_timeline_text_selection.py
tests/test_timeline_unplaced_reference_projection.py
tests/test_timeline_verified_media.py
tests/test_timeline_verified_media_http.py
tests/test_timeline_view_png.py
tests/test_timeline_visibility_generated_http.py
tests/test_door_transport.py
tests/test_http_response_lock.py
tests/test_generated_client.py
tests/test_client_parity.py
""".split()
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
        process = subprocess.Popen(command, env=env, start_new_session=True)
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
        if Path(item["root"]) != SOURCE_ROOTS[name]:
            raise ValueError(f"final source tuple {name}.root differs from the service source")


def source_identity(path: Path, expected_sha: str, runtime: Path, env: dict[str, str]) -> dict:
    value = validate_source_tuple(path, expected_sha)
    validate_roots(value)
    validate_source_tuple(path, expected_sha, runtime_root=runtime)
    # delivery-build reads tl/integration, rather than HEAD. Check both.
    for name, item in value.items():
        root = Path(item["root"])
        if git_value(root, "rev-parse", "tl/integration^{commit}") != item["sha"]:
            raise ValueError(f"final source tuple integration ref drift for {name}")
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
    return {"tuple": value, "runtime_head": git_value(runtime, "rev-parse", "HEAD"), "origins": origins}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-tuple", type=Path, required=True)
    parser.add_argument("--tuple-sha", required=True)
    parser.add_argument("service", choices=("core", "delivery", "delivery-dryrun"))
    args = parser.parse_args()
    runtime = Path.cwd().resolve()
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
    result = run_private_command(command)
    after = source_identity(args.source_tuple, args.tuple_sha, runtime, env)
    if before != after:
        raise ValueError("final service source identity changed during execution")
    if args.service != "core":
        validate_builder(BUILDER, REVIEWED_BUILDER_SHA256)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
