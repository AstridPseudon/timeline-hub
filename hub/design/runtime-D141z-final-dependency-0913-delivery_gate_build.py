#!/usr/bin/env python3
"""Stage a frozen Timeline gate on fresh upstream, then call delivery-build.

The gate tuple is immutable input.  For each repository this wrapper starts a
private Git repository at the source checkout's current ``origin/main`` and
applies only the recorded ``upstream_base`` -> ``gated_tip`` tree delta.  The
resulting private commit is exposed as ``tl/integration`` to the existing
delivery builder.  Source worktrees and refs are read-only throughout.

Builder arguments follow ``--`` and are passed unchanged, for example::

    delivery_gate_build.py --gate-tuple gate.json --gate-tuple-sha SHA \
      --builder /path/to/delivery-build --builder-sha SHA --stage-parent /tmp/x \
      --receipt /tmp/x/receipt.json -- --dry-run --repos "agent runtime"

The staging directory is deliberately retained, including a conflicted
staging tree, so a normal owner resolver can inspect it.  No conflict side is
discarded by this wrapper.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Any

REPOS = ("agent", "runtime", "app", "composition")
BASE_REF = "origin/main"
GATE_REF = "tl/integration"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TREE_RE = SHA_RE
GIT_ENV = {
    **os.environ,
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_AUTHOR_NAME": "timeline-gate-stager",
    "GIT_AUTHOR_EMAIL": "timeline-gate-stager@localhost",
    "GIT_COMMITTER_NAME": "timeline-gate-stager",
    "GIT_COMMITTER_EMAIL": "timeline-gate-stager@localhost",
}


class CandidateError(RuntimeError):
    """A refused gate or staging operation."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular_file(path: Path, label: str) -> bytes:
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise CandidateError(f"{label} must be an absolute regular non-symlink file: {path}")
    return path.read_bytes()


def git(root: Path, *args: str, input_data: bytes | None = None) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            input=input_data,
            capture_output=True,
            env=GIT_ENV,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = ""
        if isinstance(exc, subprocess.CalledProcessError):
            detail = (exc.stderr or exc.stdout or b"").decode(errors="replace").strip()
        raise CandidateError(f"git {' '.join(args[:3])} failed in {root}: {detail}") from exc
    return proc.stdout.decode().strip()


def git_bytes(root: Path, *args: str) -> bytes:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            env=GIT_ENV,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = ""
        if isinstance(exc, subprocess.CalledProcessError):
            detail = (exc.stderr or exc.stdout or b"").decode(errors="replace").strip()
        raise CandidateError(f"git {' '.join(args[:3])} failed in {root}: {detail}") from exc
    return proc.stdout


def sha(value: Any, label: str, pattern: re.Pattern[str] = SHA_RE) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise CandidateError(f"{label} must be a lowercase 40-character Git object id")
    return value


def load_gate(path: Path, expected_sha: str) -> dict[str, dict[str, str]]:
    raw = regular_file(path, "gate tuple")
    sha(expected_sha, "gate tuple SHA256", re.compile(r"^[0-9a-f]{64}$"))
    actual = digest(raw)
    if actual != expected_sha:
        raise CandidateError(f"gate tuple hash mismatch: {actual} != {expected_sha}")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CandidateError(f"invalid gate tuple JSON: {exc}") from exc
    if not isinstance(value, dict) or value.get("version") != 1:
        raise CandidateError("gate tuple version must be 1")
    repos = value.get("repos")
    if not isinstance(repos, dict) or set(repos) != set(REPOS):
        raise CandidateError("gate tuple must name exactly agent, runtime, app, composition")
    result: dict[str, dict[str, str]] = {}
    required = {
        "root",
        "base_ref",
        "gate_ref",
        "upstream_base",
        "upstream_base_tree",
        "gated_tip",
        "gated_tree",
    }
    for name in REPOS:
        item = repos[name]
        if not isinstance(item, dict) or set(item) != required:
            raise CandidateError(f"gate tuple entry {name} has unexpected fields")
        if item["base_ref"] != BASE_REF or item["gate_ref"] != GATE_REF:
            raise CandidateError(f"gate tuple {name} must use {BASE_REF} and {GATE_REF}")
        root = item["root"]
        if not isinstance(root, str) or not Path(root).is_absolute() or Path(root).is_symlink():
            raise CandidateError(f"gate tuple {name}.root must be an absolute non-symlink path")
        result[name] = {
            "root": root,
            "base_ref": BASE_REF,
            "gate_ref": GATE_REF,
            "upstream_base": sha(item["upstream_base"], f"{name}.upstream_base"),
            "upstream_base_tree": sha(item["upstream_base_tree"], f"{name}.upstream_base_tree", TREE_RE),
            "gated_tip": sha(item["gated_tip"], f"{name}.gated_tip"),
            "gated_tree": sha(item["gated_tree"], f"{name}.gated_tree", TREE_RE),
        }
    return result


def source_snapshot(name: str, item: dict[str, str]) -> dict[str, str]:
    root = Path(item["root"])
    if not root.is_dir() or root.is_symlink():
        raise CandidateError(f"{name} source root is not a real directory: {root}")
    if git(root, "rev-parse", "--is-inside-work-tree") != "true":
        raise CandidateError(f"{name} source root is not a Git worktree: {root}")
    if git(root, "status", "--porcelain"):
        raise CandidateError(f"{name} source root is dirty: {root}")
    values = {
        "base": git(root, "rev-parse", f"{item['upstream_base']}^{{commit}}"),
        "base_tree": git(root, "rev-parse", f"{item['upstream_base']}^{{tree}}"),
        "upstream_tip": git(root, "rev-parse", item["base_ref"]),
        "upstream_tip_tree": git(root, "rev-parse", f"{item['base_ref']}^{{tree}}"),
        "gated_tip": git(root, "rev-parse", item["gate_ref"]),
        "gated_tree": git(root, "rev-parse", f"{item['gate_ref']}^{{tree}}"),
    }
    if values["gated_tip"] != item["gated_tip"] or values["gated_tree"] != item["gated_tree"]:
        raise CandidateError(f"{name} frozen gate ref drifted from the gate tuple")
    if item["upstream_base"] != values["base"] or item["upstream_base_tree"] != values["base_tree"]:
        raise CandidateError(f"{name} recorded upstream base object changed")
    return values


def stage_repo(name: str, item: dict[str, str], before: dict[str, str], stage: Path) -> dict[str, Any]:
    source = Path(item["root"])
    stage.mkdir(parents=True)
    git(stage, "init", "-q", "--initial-branch=main")
    git(
        stage,
        "fetch",
        "-q",
        "--no-tags",
        str(source),
        f"{before['upstream_tip']}:refs/remotes/origin/main",
        f"{item['upstream_base']}:refs/gate/base",
        f"{item['gated_tip']}:refs/gate/tip",
    )
    git(stage, "checkout", "-q", "-B", "main", "refs/remotes/origin/main")
    patch = git_bytes(source, "diff", "--no-ext-diff", "--binary", "--full-index", item["upstream_base"], item["gated_tip"])
    patch_sha = digest(patch)
    common_base = subprocess.run(
        ["git", "-C", str(stage), "merge-base", "--is-ancestor", "refs/gate/base", "refs/gate/tip"],
        env=GIT_ENV,
        check=False,
    ).returncode == 0
    if common_base:
        try:
            git(stage, "merge", "--no-commit", "--no-ff", "refs/gate/tip")
        except CandidateError as exc:
            raise CandidateError(
                f"{name} frozen gate delta conflicts on fresh upstream; retained staging: {stage}: {exc}"
            ) from exc
    elif patch:
        try:
            git(stage, "apply", "--index", "--3way", "-", input_data=patch)
        except CandidateError as exc:
            raise CandidateError(
                f"{name} frozen gate delta conflicts on fresh upstream; retained staging: {stage}: {exc}"
            ) from exc
    applied_tree = git(stage, "write-tree")
    git(stage, "commit", "-q", "--allow-empty", "-m", f"Stage frozen Timeline gate for {name} on fresh upstream")
    applied_commit = git(stage, "rev-parse", "HEAD")
    git(stage, "update-ref", f"refs/heads/{GATE_REF}", applied_commit)
    if git(stage, "rev-parse", f"{GATE_REF}^{{tree}}") != applied_tree:
        raise CandidateError(f"{name} staged integration ref does not point at the applied tree")
    return {
        "source_root": str(source),
        "upstream_base": item["upstream_base"],
        "upstream_base_tree": item["upstream_base_tree"],
        "fresh_upstream": before["upstream_tip"],
        "fresh_upstream_tree": before["upstream_tip_tree"],
        "gated_tip": item["gated_tip"],
        "gated_tree": item["gated_tree"],
        "delta_sha256": patch_sha,
        "applied_commit": applied_commit,
        "applied_tree": applied_tree,
        "staged_root": str(stage),
    }


def load_builder(path: Path, expected_sha: str):
    raw = regular_file(path, "builder")
    sha(expected_sha, "builder SHA256", re.compile(r"^[0-9a-f]{64}$"))
    actual = digest(raw)
    if actual != expected_sha:
        raise CandidateError(f"builder hash mismatch: {actual} != {expected_sha}")
    loader = SourceFileLoader("timeline_frozen_gate_delivery_builder", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None or spec.loader is None:
        raise CandidateError(f"cannot load builder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_builder(
    builder_path: Path,
    builder_sha: str,
    stage_parent: Path,
    staged_root: Path,
    builder_args: list[str],
) -> tuple[int, str]:
    builder = load_builder(builder_path, builder_sha)
    output = stage_parent / "delivery-output"
    output.mkdir()
    builder.WORK = str(staged_root)
    builder.DELIVERY = str(output)
    builder.TEMPLATE = str(Path(builder_path).parent / "README.template.md")
    if not Path(builder.TEMPLATE).is_file():
        builder.TEMPLATE = str(Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md"))
    builder.GATE_RESULTS = str(Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md"))
    os.environ["TIMELINE_DELIVERY_SCRIPT_SHA"] = builder_sha
    os.environ["TMPDIR"] = str(stage_parent)
    os.environ["TMP"] = str(stage_parent)
    os.environ["TEMP"] = str(stage_parent)
    tempfile.tempdir = None
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        try:
            code = int(builder.main_with_args(builder_args))
        except AttributeError:
            # The installed f25d builder exposes only main(), so temporarily
            # present its expected argv without changing the process caller.
            previous = sys.argv
            sys.argv = [str(builder_path), *builder_args]
            try:
                code = int(builder.main())
            finally:
                sys.argv = previous
        except SystemExit as exc:
            code = int(exc.code or 0)
    return code, captured.getvalue()


def write_receipt(path: Path, value: dict[str, Any]) -> None:
    if not path.is_absolute() or path.is_symlink():
        raise CandidateError(f"receipt must be an absolute non-symlink path: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate-tuple", type=Path, required=True)
    parser.add_argument("--gate-tuple-sha", required=True)
    parser.add_argument("--builder", type=Path, required=True)
    parser.add_argument("--builder-sha", required=True)
    parser.add_argument("--stage-parent", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("builder_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if args.builder_args[:1] == ["--"]:
        args.builder_args = args.builder_args[1:]

    gate = load_gate(args.gate_tuple, args.gate_tuple_sha)
    stage_parent = args.stage_parent.absolute()
    if not stage_parent.is_dir() or stage_parent.is_symlink():
        raise CandidateError(f"stage parent must be an existing real directory: {stage_parent}")
    stage_root = Path(tempfile.mkdtemp(prefix="timeline-frozen-gate-", dir=stage_parent))
    receipt: dict[str, Any] = {
        "version": 1,
        "gate_tuple_sha256": args.gate_tuple_sha,
        "builder_sha256": args.builder_sha,
        "stage_root": str(stage_root),
        "status": "staging",
        "repos": {},
    }
    before: dict[str, dict[str, str]] = {}
    try:
        for name in REPOS:
            before[name] = source_snapshot(name, gate[name])
            receipt["repos"][name] = stage_repo(name, gate[name], before[name], stage_root / name)
        receipt["status"] = "staged"
        write_receipt(args.receipt, receipt)
        code, output = run_builder(args.builder, args.builder_sha, stage_root, stage_root, args.builder_args)
        receipt["builder_exit"] = code
        receipt["builder_output"] = output
        receipt["status"] = "PASS" if code == 0 else "FAIL"
        for name in REPOS:
            after = source_snapshot(name, gate[name])
            if after != before[name]:
                raise CandidateError(f"{name} source identity changed during private delivery")
        write_receipt(args.receipt, receipt)
        print(output, end="")
        print(f"frozen-gate staging: {stage_root}")
        print(f"receipt: {args.receipt}")
        return code
    except Exception as exc:
        receipt["status"] = "FAIL"
        receipt["error"] = str(exc)
        try:
            write_receipt(args.receipt, receipt)
        except (CandidateError, OSError):
            pass
        raise


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CandidateError as exc:
        print(f"delivery gate refused: {exc}", file=sys.stderr)
        raise SystemExit(2)
