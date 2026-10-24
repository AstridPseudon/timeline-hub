"""Run the private final delivery through the reviewed D68 staging wrapper.

The core service runner is a separate joined candidate with the 92-target selector. This
caller only owns delivery input: it validates the immutable source and gate tuples, repairs
the shallow App input in a private TMPDIR source view, derives path overlap from the pinned
trees, and passes the builder arguments unchanged to the reviewed wrapper.
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
MIN_SOURCE_VIEW_FREE_BYTES = 8_500_000_000


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


def _git_without_root(*args: str, cwd: Path | None = None) -> str:
    env = os.environ.copy()
    env.update(
        GIT_CONFIG_GLOBAL="/dev/null",
        GIT_CONFIG_SYSTEM="/dev/null",
        GIT_CONFIG_NOSYSTEM="1",
        GIT_OPTIONAL_LOCKS="0",
        GIT_TERMINAL_PROMPT="0",
    )
    try:
        process = subprocess.run(
            ["git", *args],
            cwd=str(cwd) if cwd is not None else None,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = ""
        if isinstance(exc, subprocess.CalledProcessError):
            detail = (exc.stderr or exc.stdout or "").strip()
        raise ValueError(f"git {' '.join(args[:3])} failed: {detail}") from exc
    return process.stdout.strip()


def _git_dir(root: Path) -> Path:
    value = Path(git(root, "rev-parse", "--git-dir"))
    return value if value.is_absolute() else root / value


def _missing_objects(root: Path, tip: str) -> list[str]:
    output = git(root, "rev-list", "--missing=print", "--objects", tip)
    return [line for line in output.splitlines() if line.startswith("?")]


def prepare_private_app_source_view(
    source_item: dict[str, str],
    gate_item: dict[str, str],
    parent: Path,
    *,
    min_free_bytes: int = MIN_SOURCE_VIEW_FREE_BYTES,
) -> tuple[Path, Path, dict[str, Any]]:
    """Make a self-contained App Git input without changing the source checkout.

    The source repository can contain every object while still being marked shallow. Git's
    local upload-pack refuses to traverse such a repository. Removing the shallow marker is
    therefore done only in this private copy, after its objects have been copied, and never
    in a shared source repository.
    """

    root = Path(source_item["root"])
    if gate_item["root"] != source_item["root"]:
        raise ValueError("App source and gate roots differ")
    if source_item["sha"] != gate_item["gated_tip"] or source_item["tree"] != gate_item["gated_tree"]:
        raise ValueError("App source tuple is not the immutable gate tip/tree")
    if git(root, "rev-parse", BASE_REF + "^{commit}") != gate_item["upstream_base"]:
        raise ValueError("App origin/main is not the immutable gate upstream base")
    if git(root, "rev-parse", "--is-shallow-repository") != "true":
        raise ValueError("private App source view requested for a non-shallow source")
    if not parent.is_dir() or parent.is_symlink():
        raise ValueError(f"source-view parent must be a real directory: {parent}")
    free_bytes = shutil.disk_usage(parent).free
    if free_bytes < min_free_bytes:
        raise ValueError(
            "App source view pending: free TMPDIR space is below the 8.5 GB heavy-work floor "
            f"({free_bytes} < {min_free_bytes} bytes)"
        )

    holder = Path(tempfile.mkdtemp(prefix="timeline-app-source-view-", dir=parent))
    view = holder / "app"
    try:
        _git_without_root(
            "clone", "--no-local", "--no-hardlinks", "--no-checkout", str(root), str(view)
        )
        if view.is_symlink() or not view.is_dir():
            raise ValueError("private App source view is not a real directory")
        shallow = _git_dir(view) / "shallow"
        if git(view, "rev-parse", "--is-shallow-repository") == "true":
            if not shallow.is_file() or shallow.is_symlink():
                raise ValueError("private App source view has an unexpected shallow boundary")
            shallow.unlink()
        _git_without_root("update-ref", "refs/remotes/origin/main", gate_item["upstream_base"], cwd=view)
        _git_without_root("update-ref", GATE_REF, gate_item["gated_tip"], cwd=view)
        _git_without_root("checkout", "--detach", gate_item["gated_tip"], cwd=view)
        if git(view, "rev-parse", "HEAD") != source_item["sha"]:
            raise ValueError("private App source view tip differs from immutable input")
        if git(view, "rev-parse", "HEAD^{tree}") != source_item["tree"]:
            raise ValueError("private App source view tree differs from immutable input")
        if git(view, "rev-parse", BASE_REF + "^{commit}") != gate_item["upstream_base"]:
            raise ValueError("private App source view origin/main differs from immutable input")
        if git(view, "rev-parse", BASE_REF + "^{tree}") != gate_item["upstream_base_tree"]:
            raise ValueError("private App source view origin/main tree differs from immutable input")
        if git(view, "rev-parse", GATE_REF + "^{commit}") != gate_item["gated_tip"]:
            raise ValueError("private App source view integration tip differs from immutable input")
        if git(view, "rev-parse", GATE_REF + "^{tree}") != gate_item["gated_tree"]:
            raise ValueError("private App source view integration tree differs from immutable input")
        if not git(view, "remote", "get-url", "origin"):
            raise ValueError("private App source view has no origin remote")
        missing = _missing_objects(view, gate_item["gated_tip"])
        if missing:
            raise ValueError(f"private App source view has missing objects: {missing[:3]}")
        if git(view, "status", "--porcelain"):
            raise ValueError("private App source view is dirty")
        return holder, view, {
            "repo": "app",
            "root": str(view),
            "tip": source_item["sha"],
            "tree": source_item["tree"],
            "origin_main": gate_item["upstream_base"],
            "origin_main_tree": gate_item["upstream_base_tree"],
            "missing_objects": 0,
            "source": str(root),
        }
    except Exception:
        shutil.rmtree(holder)
        raise


def _write_derived_inputs(
    source_raw: bytes, gate_raw: bytes, view: Path, parent: Path
) -> tuple[Path, str, Path, str]:
    try:
        source_value = json.loads(source_raw)
        gate_value = json.loads(gate_raw)
    except json.JSONDecodeError as exc:
        raise ValueError("immutable delivery input is not valid JSON") from exc
    if not isinstance(source_value, dict) or not isinstance(gate_value, dict):
        raise TypeError("immutable delivery input must contain JSON objects")
    if not isinstance(source_value.get("app"), dict) or not isinstance(gate_value.get("repos"), dict):
        raise TypeError("immutable delivery input has no App entry")
    app_gate = gate_value["repos"].get("app")
    if not isinstance(app_gate, dict):
        raise TypeError("immutable gate input has no App entry")
    source_value["app"]["root"] = str(view)
    app_gate["root"] = str(view)
    source_path = parent / "source-tuple.json"
    gate_path = parent / "gate-tuple.json"
    source_path.write_text(json.dumps(source_value, indent=2, sort_keys=True) + "\n")
    gate_path.write_text(json.dumps(gate_value, indent=2, sort_keys=True) + "\n")
    return source_path, digest(source_path.read_bytes()), gate_path, digest(gate_path.read_bytes())


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
    stage_parent = Path(os.environ.get("TMPDIR", tempfile.gettempdir())).absolute()
    if not stage_parent.is_dir() or stage_parent.is_symlink():
        raise ValueError(f"service TMPDIR must be a real directory: {stage_parent}")
    source_raw = checked_file(args.source_tuple, args.tuple_sha, "final source tuple")
    gate_raw = checked_file(args.gate_tuple, args.gate_tuple_sha, "frozen gate tuple")
    source = source_identity(args.source_tuple, args.tuple_sha)
    _, gate = gate_identity(args.gate_tuple, args.gate_tuple_sha)
    input_holder: Path | None = None
    effective_source_path = args.source_tuple
    effective_source_sha = args.tuple_sha
    effective_gate_path = args.gate_tuple
    effective_gate_sha = args.gate_tuple_sha
    source_view: dict[str, Any] = {"status": "not-needed"}
    try:
        app_root = Path(source["app"]["root"])
        if git(app_root, "rev-parse", "--is-shallow-repository") == "true":
            input_holder, view, source_view = prepare_private_app_source_view(
                source["app"], gate["app"], stage_parent
            )
            effective_source_path, effective_source_sha, effective_gate_path, effective_gate_sha = (
                _write_derived_inputs(source_raw, gate_raw, view, input_holder)
            )
            source = source_identity(effective_source_path, effective_source_sha)
            _, gate = gate_identity(effective_gate_path, effective_gate_sha)
        overlap = overlap_identity(gate)
        before = {
            name: (
                git(Path(item["root"]), "status", "--porcelain"),
                git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{commit}}"),
                git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{tree}}"),
            )
            for name, item in source.items()
        }
        wrapper_receipt = Path(tempfile.mkdtemp(prefix="timeline-d68-receipt-", dir=stage_parent)) / "wrapper.json"
        command = [
            sys.executable,
            str(args.wrapper),
            "--gate-tuple",
            str(effective_gate_path),
            "--gate-tuple-sha",
            effective_gate_sha,
            "--builder",
            str(args.builder),
            "--builder-sha",
            args.builder_sha,
            "--stage-parent",
            str(wrapper_receipt.parent),
            "--receipt",
            str(wrapper_receipt),
            "--",
            *args.builder_args,
        ]
        code, output = run_wrapper(command, stage_parent)
        wrapper_value: dict[str, Any] = {}
        if wrapper_receipt.is_file():
            wrapper_value = json.loads(wrapper_receipt.read_text())
        after = {
            name: (
                git(Path(item["root"]), "status", "--porcelain"),
                git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{commit}}"),
                git(Path(item["root"]), "rev-parse", f"{GATE_REF}^{{tree}}"),
            )
            for name, item in source.items()
        }
        if before != after:
            raise ValueError("final source identity changed during private delivery")
        receipt = {
            "version": 1,
            "status": "PASS" if code == 0 else "FAIL",
            "service": "delivery",
            "source_tuple_sha256": args.tuple_sha,
            "effective_source_tuple_sha256": effective_source_sha,
            "source": source,
            "frozen_gate_tuple_sha256": args.gate_tuple_sha,
            "effective_gate_tuple_sha256": effective_gate_sha,
            "frozen_gate": gate,
            "overlap": overlap,
            "source_view": source_view,
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
    finally:
        if input_holder is not None and input_holder.exists():
            shutil.rmtree(input_holder)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"final delivery refused: {exc}", file=sys.stderr)
        raise SystemExit(2)


