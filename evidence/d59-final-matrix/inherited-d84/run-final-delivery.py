"""Run the private final delivery through the reviewed D68 staging wrapper.

The core service runner is a separate joined candidate with the 87-target selector.  This
caller only owns delivery: it validates the final source receipt, validates the
frozen gate tuple, derives path overlap from the pinned trees, and passes the
builder arguments unchanged to the reviewed wrapper.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SOURCE_REPOS = ("agent", "runtime", "app", "composition")
CORE_RUNNER = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
    "/workers/rt-F-final-D84-core-prep-2207/evidence/candidate/run-final-services.py"
)
CORE_RUNNER_SHA256 = "05c5662aa14c3bb288f672421d448335a0b10df659fd58439e6abd296c4c3a97"
REVIEWED_WRAPPER = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
    "/workers/rt-F-final-D68-review-1554/evidence/delivery_gate_build.py"
)
REVIEWED_WRAPPER_SHA256 = "bae840fad6ea496457a3d6138609ce9d89b0b10825827c94f855257bce6c6779"
REVIEWED_BUILDER_SHA256 = (
    "f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708"
)
BASE_REF = "origin/main"
GATE_REF = "tl/integration"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular_file(path: Path, label: str) -> bytes:
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise ValueError(f"{label} must be an absolute regular non-symlink file: {path}")
    return path.read_bytes()


def checked_file(path: Path, expected: str, label: str) -> bytes:
    raw = regular_file(path, label)
    actual = digest(raw)
    if actual != expected:
        raise ValueError(f"{label} hash mismatch: {actual} != {expected}")
    return raw


def git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args], text=True, stderr=subprocess.STDOUT
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "output", "")
        raise ValueError(f"git {' '.join(args[:3])} failed in {root}: {detail}") from exc


def source_identity(path: Path, expected_sha: str) -> dict[str, dict[str, str]]:
    raw = checked_file(path, expected_sha, "final source tuple")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid final source tuple: {path}") from exc
    if not isinstance(value, dict) or set(value) != set(SOURCE_REPOS):
        raise ValueError("final source tuple must name exactly the four delivery repositories")
    result: dict[str, dict[str, str]] = {}
    for name in SOURCE_REPOS:
        item = value[name]
        if not isinstance(item, dict) or set(item) != {"root", "sha", "tree"}:
            raise ValueError(f"final source tuple entry {name} must contain root, sha, tree")
        root = Path(item["root"])
        if (
            not root.is_absolute()
            or root.is_symlink()
            or not root.is_dir()
            or len(item["sha"]) != 40
            or len(item["tree"]) != 40
            or any(c not in "0123456789abcdef" for c in item["sha"] + item["tree"])
        ):
            raise ValueError(f"invalid final source tuple identity for {name}")
        if git(root, "rev-parse", "--is-inside-work-tree") != "true":
            raise ValueError(f"source tuple root is not a Git worktree: {root}")
        if git(root, "status", "--porcelain"):
            raise ValueError(f"source tuple source is dirty: {root}")
        if git(root, "rev-parse", "HEAD") != item["sha"]:
            raise ValueError(f"source tuple checkout drift for {name}")
        if git(root, "rev-parse", f"{GATE_REF}^{{tree}}") != item["tree"]:
            raise ValueError(f"source tuple integration tree drift for {name}")
        result[name] = {"root": str(root), "sha": item["sha"], "tree": item["tree"]}
    return result


def gate_identity(path: Path, expected_sha: str) -> tuple[bytes, dict[str, dict[str, str]]]:
    raw = checked_file(path, expected_sha, "frozen gate tuple")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid frozen gate tuple: {path}") from exc
    if not isinstance(value, dict) or value.get("version") != 1:
        raise ValueError("frozen gate tuple version must be 1")
    repos = value.get("repos")
    if not isinstance(repos, dict) or set(repos) != set(SOURCE_REPOS):
        raise ValueError("frozen gate tuple must name exactly the four delivery repositories")
    required = {
        "root", "base_ref", "gate_ref", "upstream_base", "upstream_base_tree",
        "gated_tip", "gated_tree",
    }
    result: dict[str, dict[str, str]] = {}
    for name in SOURCE_REPOS:
        item = repos[name]
        if not isinstance(item, dict) or set(item) != required:
            raise ValueError(f"frozen gate tuple entry {name} has unexpected fields")
        root = Path(item["root"])
        if (
            not root.is_absolute() or root.is_symlink() or not root.is_dir()
            or item["base_ref"] != BASE_REF or item["gate_ref"] != GATE_REF
        ):
            raise ValueError(f"invalid frozen gate tuple root or refs for {name}")
        for field in ("upstream_base", "upstream_base_tree", "gated_tip", "gated_tree"):
            value_id = item[field]
            if not isinstance(value_id, str) or len(value_id) != 40 or any(
                c not in "0123456789abcdef" for c in value_id
            ):
                raise ValueError(f"invalid frozen gate tuple {name}.{field}")
        if git(root, "rev-parse", f"{item['upstream_base']}^{{commit}}") != item["upstream_base"]:
            raise ValueError(f"frozen upstream base is unavailable for {name}")
        if git(root, "rev-parse", f"{item['upstream_base']}^{{tree}}") != item["upstream_base_tree"]:
            raise ValueError(f"frozen upstream base tree drift for {name}")
        if git(root, "rev-parse", f"{GATE_REF}^{{commit}}") != item["gated_tip"]:
            raise ValueError(f"frozen gate ref drift for {name}")
        if git(root, "rev-parse", f"{GATE_REF}^{{tree}}") != item["gated_tree"]:
            raise ValueError(f"frozen gate tree drift for {name}")
        if git(root, "status", "--porcelain"):
            raise ValueError(f"frozen gate source is dirty: {root}")
        result[name] = {key: str(value) for key, value in item.items()}
    return raw, result


def path_names(root: Path, left: str, right: str) -> list[str]:
    output = git(root, "diff", "--name-only", "--no-renames", left, right)
    return sorted({line for line in output.splitlines() if line})


def overlap_identity(gate: dict[str, dict[str, str]]) -> dict[str, dict[str, list[str]]]:
    result: dict[str, dict[str, list[str]]] = {}
    for name, item in gate.items():
        root = Path(item["root"])
        delta = path_names(root, item["upstream_base"], item["gated_tip"])
        later = path_names(root, item["upstream_base"], BASE_REF)
        result[name] = {
            "frozen_gate_delta_paths": delta,
            "later_upstream_paths": later,
            "overlap_paths": sorted(set(delta) & set(later)),
        }
    return result


def run_wrapper(command: list[str], service_tmp: Path) -> tuple[int, str]:
    service_tmp = service_tmp.absolute()
    if not service_tmp.is_dir() or service_tmp.is_symlink():
        raise ValueError(f"service TMPDIR must be a real directory: {service_tmp}")
    stage_parent = Path(tempfile.mkdtemp(prefix="timeline-d68-delivery-", dir=service_tmp))
    env = os.environ.copy()
    env.update(
        TMPDIR=str(stage_parent),
        TMP=str(stage_parent),
        TEMP=str(stage_parent),
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_CONFIG_SYSTEM="/dev/null",
        GIT_CONFIG_NOSYSTEM="1",
        GIT_COMMIT_GPGSIGN="false",
        GIT_OPTIONAL_LOCKS="0",
    )
    process: subprocess.Popen[str] | None = None
    previous: dict[signal.Signals, Any] = {}
    code: int = 1

    def interrupt(signum: int, _frame: Any) -> None:
        raise InterruptedError(signum)

    try:
        for signum in (signal.SIGTERM, signal.SIGINT):
            previous[signum] = signal.signal(signum, interrupt)
        process = subprocess.Popen(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            output, _ = process.communicate(timeout=30 * 60)
            code = process.returncode
        except (subprocess.TimeoutExpired, InterruptedError) as exc:
            code = 124 if isinstance(exc, subprocess.TimeoutExpired) else 128 + int(exc.args[0])
            for signum in previous:
                signal.signal(signum, signal.SIG_IGN)
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                output, _ = process.communicate(timeout=45)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                output, _ = process.communicate()
        return int(code), output
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        shutil.rmtree(stage_parent)


def write_receipt(path: Path, value: dict[str, Any]) -> None:
    if not path.is_absolute() or path.is_symlink():
        raise ValueError(f"receipt must be an absolute non-symlink path: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-tuple", type=Path, required=True)
    parser.add_argument("--tuple-sha", required=True)
    parser.add_argument("--gate-tuple", type=Path, required=True)
    parser.add_argument("--gate-tuple-sha", required=True)
    parser.add_argument("--wrapper", type=Path, default=REVIEWED_WRAPPER)
    parser.add_argument("--wrapper-sha", default=REVIEWED_WRAPPER_SHA256)
    parser.add_argument("--builder", type=Path, required=True)
    parser.add_argument("--builder-sha", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("builder_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if args.builder_args[:1] == ["--"]:
        args.builder_args = args.builder_args[1:]
    if not args.builder_args:
        raise ValueError("delivery builder arguments must be non-empty")
    if args.builder_sha != REVIEWED_BUILDER_SHA256:
        raise ValueError("delivery builder SHA is not the reviewed f25d builder")
    checked_file(CORE_RUNNER, CORE_RUNNER_SHA256, "core runner")
    checked_file(args.wrapper, args.wrapper_sha, "reviewed D68 wrapper")
    checked_file(args.builder, args.builder_sha, "delivery builder")
    source = source_identity(args.source_tuple, args.tuple_sha)
    _, gate = gate_identity(args.gate_tuple, args.gate_tuple_sha)
    overlap = overlap_identity(gate)
    before = {name: (git(Path(item["root"]), "status", "--porcelain"), git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{commit}}"), git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{tree}}")) for name, item in source.items()}
    stage_parent = Path(os.environ.get("TMPDIR", tempfile.gettempdir())).absolute()
    wrapper_receipt = Path(tempfile.mkdtemp(prefix="timeline-d68-receipt-", dir=stage_parent)) / "wrapper.json"
    command = [sys.executable, str(args.wrapper), "--gate-tuple", str(args.gate_tuple), "--gate-tuple-sha", args.gate_tuple_sha,
               "--builder", str(args.builder), "--builder-sha", args.builder_sha, "--stage-parent", str(wrapper_receipt.parent),
               "--receipt", str(wrapper_receipt), "--", *args.builder_args]
    code, output = run_wrapper(command, stage_parent)
    wrapper_value: dict[str, Any] = {}
    if wrapper_receipt.is_file():
        wrapper_value = json.loads(wrapper_receipt.read_text())
    after = {name: (git(Path(item["root"]), "status", "--porcelain"), git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{commit}}"), git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{tree}}")) for name, item in source.items()}
    if before != after:
        raise ValueError("final source identity changed during private delivery")
    receipt = {
        "version": 1,
        "status": "PASS" if code == 0 else "FAIL",
        "service": "delivery",
        "source_tuple_sha256": args.tuple_sha,
        "source": source,
        "frozen_gate_tuple_sha256": args.gate_tuple_sha,
        "frozen_gate": gate,
        "overlap": overlap,
        "wrapper": {"path": str(args.wrapper), "sha256": args.wrapper_sha, "receipt": wrapper_value},
        "builder": {"path": str(args.builder), "sha256": args.builder_sha},
        "builder_args": args.builder_args,
        "exit": code,
        "output": output,
    }
    write_receipt(args.receipt, receipt)
    print(output, end="")
    print(f"D68 delivery status: {receipt['status']}")
    print(f"receipt: {args.receipt}")
    return code


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"final delivery refused: {exc}", file=sys.stderr)
        raise SystemExit(2)

