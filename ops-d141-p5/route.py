#!/usr/bin/env python3
"""Prepare and validate the private D141 P5 cut route.

This module validates route inputs and renders the existing Runtime test
service row. It does not import Runtime or Agent, register a suite, or run
the P5 product tests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "route-config.json"
HEX40 = set("0123456789abcdef")
DONE_CREATED = re.compile(
    r"^created (?P<path>/home/user/work/wt/agt-pin-[0-9a-f]{8}) "
    r"\(detached at (?P<commit>[0-9a-f]{40}), KEEP\)$"
)
DONE_EXISTS = re.compile(
    r"^exists: (?P<path>/home/user/work/wt/agt-pin-[0-9a-f]{8}) "
    r"at (?P<commit>[0-9a-f]{40})$"
)
SCHEMA_DIGEST = re.compile(r"SCHEMA_DIGEST\s*=\s*['\"](sha256:[0-9a-f]{64})['\"]")
PROVIDER_RELATIVE = Path("astrid/sdk/timeline/api.py")
CLIENT_RELATIVE = Path("astrid_runtime_client/generated.py")
METADATA_RELATIVE = Path("astrid_runtime_client/contract_metadata.py")
LOCK_RELATIVES = (Path("runtime.lock.json"),)
EXPECTED_RUNTIME = {
    "commit": "6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d",
    "tree": "ac5b862744bece65b2e30565db1777bacd60da28",
}
EXPECTED_FILES = {
    "tests/test_timeline_commit_integration.py":
    "867a33c5c1cda39e1cb540d1fb378b3987eaacc8ceb89d67c3f23711ec400534",
    "tests/test_timeline_commit_crash.py":
    "9a7d201f6d3e2d66898ab6f901a5567c9808bf23520be5b50d06a148813f1e63",
}
EXPECTED_ARGS = [
    "-m", "pytest", "-q", "-n3", "-p", "no:cacheprovider", "-m", "integration",
    "tests/test_timeline_commit_integration.py", "tests/test_timeline_commit_crash.py",
]


class RouteError(ValueError):
    """A route input is incomplete, mismatched, or unsafe to install."""


def _hash(value: Any, label: str) -> None:
    if not isinstance(value, str) or len(value) != 40 or set(value) - HEX40:
        raise RouteError(f"{label} must be a lowercase 40-character hash")


def _absolute(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.startswith("/"):
        raise RouteError(f"{label} must be an absolute path")


def _validate_agent(agent: Any) -> None:
    if not isinstance(agent, dict) or agent.get("status") not in {"pending", "qualified"}:
        raise RouteError("Agent status is invalid")
    if agent["status"] == "pending":
        fields = (
            "commit", "tree", "checkout", "receipt", "expected_commit",
            "provider_origin", "client_origin", "schema_digest", "lock_values",
        )
        if any(agent.get(field) is not None for field in fields):
            raise RouteError("pending Agent has a partial custody tuple")
        return
    _absolute(agent.get("receipt"), "Agent make-checkout receipt")
    expected = agent.get("expected_commit")
    if expected is not None:
        _hash(expected, "expected Agent commit")
    derived = (
        "commit", "tree", "checkout", "provider_origin", "client_origin",
        "schema_digest", "lock_values",
    )
    if any(agent.get(field) is not None for field in derived):
        raise RouteError("qualified Agent provenance must be derived from its checkout")


def _validate_config(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise RouteError("unsupported route configuration")
    route = data.get("route")
    if not isinstance(route, dict) or route.get("name") != "d141-p5-cut" or route.get("kind") != "cut":
        raise RouteError("route name or kind changed")
    runtime = route.get("runtime")
    if not isinstance(runtime, dict) or {key: runtime.get(key) for key in EXPECTED_RUNTIME} != EXPECTED_RUNTIME:
        raise RouteError("frozen Runtime identity changed")
    _absolute(runtime.get("checkout"), "Runtime checkout")
    if runtime.get("origin") != "https://github.com/banodoco/banodoco-workspace-runtime":
        raise RouteError("Runtime origin changed")
    _validate_agent(route.get("agent"))
    pytest_config = data.get("pytest")
    if not isinstance(pytest_config, dict):
        raise RouteError("pytest route is missing")
    if pytest_config.get("interpreter") != "/home/user/work/venv-runtime/bin/python":
        raise RouteError("canonical Runtime interpreter changed")
    if pytest_config.get("environment_unset") != ["NODE_OPTIONS", "NODE_PATH"]:
        raise RouteError("required environment guard changed")
    if pytest_config.get("arguments") != EXPECTED_ARGS or pytest_config.get("junit_name") != "d141-p5-cut.xml":
        raise RouteError("P5 selector or pytest arguments changed")
    source = data.get("source")
    if not isinstance(source, dict) or source.get("membership_only") is not True:
        raise RouteError("source must be membership-only")
    files = source.get("files")
    if not isinstance(files, list) or len(files) != 2:
        raise RouteError("P5 requires exactly two source files")
    seen: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict) or entry.get("path") not in EXPECTED_FILES:
            raise RouteError("source membership changed")
        path = entry["path"]
        if path in seen or entry.get("sha256") != EXPECTED_FILES[path]:
            raise RouteError("source membership or hash changed")
        seen.add(path)
    if seen != set(EXPECTED_FILES):
        raise RouteError("source membership is incomplete")
    required = data.get("required")
    if not isinstance(required, list) or len(required) != 4 or len(set(required)) != 4:
        raise RouteError("required input manifest is incomplete")
    return data


def load_config(path: Path = CONFIG) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RouteError(f"cannot read route configuration: {error}") from error
    return _validate_config(data)


def route_status(config: dict[str, Any]) -> tuple[str, list[str]]:
    agent = config["route"]["agent"]
    if agent["status"] != "qualified":
        return "NOT_READY", ["genuine final Agent cut receipt is pending"]
    return "READY", []


def _regular(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise RouteError(f"{label} is not a regular file")


def _directory(path: Path, label: str) -> None:
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        raise RouteError(f"{label} must be an absolute regular directory")


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise RouteError(f"cannot inspect source checkout {root}: {error}") from error


def _verify_checkout(path: Path, commit: str, tree: str, label: str) -> None:
    _directory(path, f"{label} checkout")
    if (path / ".git").is_symlink():
        raise RouteError(f"{label} checkout has a symlinked git directory")
    actual = (_git(path, "rev-parse", "HEAD"), _git(path, "rev-parse", "HEAD^{tree}"), _git(path, "status", "--porcelain"))
    if actual != (commit, tree, ""):
        raise RouteError(f"{label} source mismatch: commit={actual[0]} tree={actual[1]} dirty={bool(actual[2])}")


def _read_checkout_done(receipt: Path, expected_commit: str | None) -> tuple[Path, str]:
    _regular(receipt, "checkout done receipt")
    if receipt.parent.name != "done" or not receipt.name.startswith("checkout-agent-"):
        raise RouteError("checkout receipt is not an existing make-checkout done file")
    pending = receipt.parent.parent / "pending" / receipt.name
    if pending.exists() or pending.is_symlink():
        raise RouteError("checkout still has a pending request")
    lines = receipt.read_text(encoding="utf-8").splitlines()
    if len(lines) != 1:
        raise RouteError("checkout done receipt is malformed")
    match = DONE_CREATED.fullmatch(lines[0]) or DONE_EXISTS.fullmatch(lines[0])
    if match is None:
        raise RouteError("checkout done receipt is not from make-checkout")
    checkout = Path(match["path"])
    commit = match["commit"]
    if receipt.name != f"checkout-agent-{commit}":
        raise RouteError("checkout done receipt name does not match its commit")
    if expected_commit is not None and commit != expected_commit:
        raise RouteError("checkout done receipt commit is not the expected Agent tip")
    return checkout, commit


def _inside(root: Path, path: Path, label: str) -> None:
    try:
        path.relative_to(root)
    except ValueError as error:
        raise RouteError(f"{label} is outside its bound checkout") from error


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _derive_agent(agent: dict[str, Any]) -> dict[str, Any]:
    checkout, commit = _read_checkout_done(Path(agent["receipt"]), agent.get("expected_commit"))
    tree = _git(checkout, "rev-parse", "HEAD^{tree}")
    _verify_checkout(checkout, commit, tree, "Agent")
    root = checkout.resolve()
    keep = Path(agent["receipt"]).parents[2] / "workers" / checkout.name / "KEEP"
    _regular(keep, "Agent checkout KEEP witness")
    provider = root / PROVIDER_RELATIVE
    client = root / CLIENT_RELATIVE
    metadata = root / METADATA_RELATIVE
    for path, label in ((provider, "Agent provider origin"), (client, "Agent client origin"), (metadata, "Agent client metadata")):
        _regular(path, label)
        _inside(root, path.resolve(), label)
    schema_match = SCHEMA_DIGEST.search(metadata.read_text(encoding="utf-8"))
    client_match = SCHEMA_DIGEST.search(client.read_text(encoding="utf-8"))
    if schema_match is None or client_match is None or schema_match[1] != client_match[1]:
        raise RouteError("Agent schema digest is not derived consistently from the checkout")
    lock_values: dict[str, str] = {}
    for relative in LOCK_RELATIVES:
        path = root / relative
        _regular(path, "Agent lock metadata")
        _inside(root, path.resolve(), "Agent lock metadata")
        lock_values[str(relative)] = "sha256:" + _sha256(path)
    return {
        "commit": commit,
        "tree": tree,
        "checkout": str(checkout),
        "receipt": str(Path(agent["receipt"])),
        "provider_origin": str(provider),
        "client_origin": str(client),
        "schema_digest": schema_match[1],
        "lock_values": lock_values,
    }


def _source_guard(runtime: dict[str, Any], agent: dict[str, Any]) -> str:
    checkout = shlex.quote(agent["checkout"])
    return (
        "( test \"$(git rev-parse HEAD)\" = " + shlex.quote(runtime["commit"])
        + " || test \"$(git rev-parse HEAD^)\" = " + shlex.quote(runtime["commit"])
        + " ) && test \"$(git rev-parse HEAD^{tree})\" = " + shlex.quote(runtime["tree"])
        + " && test -z \"$(git status --porcelain)\""
        + " && test \"$(git -C " + checkout + " rev-parse HEAD)\" = " + shlex.quote(agent["commit"])
        + " && test \"$(git -C " + checkout + " rev-parse HEAD^{tree})\" = " + shlex.quote(agent["tree"])
        + " && test -z \"$(git -C " + checkout + " status --porcelain)\""
    )


def _verify_runtime(runtime: dict[str, Any]) -> Path:
    root = Path(runtime["checkout"])
    _verify_checkout(root, EXPECTED_RUNTIME["commit"], EXPECTED_RUNTIME["tree"], "Runtime")
    return root


def _verify_source_membership(runtime: Path) -> None:
    for relative, expected in EXPECTED_FILES.items():
        path = runtime / relative
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RouteError(f"source membership hash mismatch: {relative}")


def render_rows(config: dict[str, Any]) -> list[str]:
    status, missing = route_status(config)
    if status != "READY":
        raise RouteError("pending tuple: " + "; ".join(missing))
    route = config["route"]
    agent = _derive_agent(route["agent"])
    runtime = _verify_runtime(route["runtime"])
    _verify_source_membership(runtime)
    command = " ".join(shlex.quote(part) for part in config["pytest"]["arguments"])
    unset = " ".join(f"-u {name}" for name in config["pytest"]["environment_unset"])
    junit = f'"$D66_OUTPUT_DIR/{config["pytest"]["junit_name"]}"'
    body = (
        f"{_source_guard(route['runtime'], agent)} && "
        f"df -B1 --output=avail /home/user > \"$D66_OUTPUT_DIR/disk-start\" && "
        f"env {unset} ASTRID_CHECKOUT={shlex.quote(agent['checkout'])} "
        f"{shlex.quote(config['pytest']['interpreter'])} {command} --junitxml={junit}; rc=$?; "
        f"df -B1 --output=avail /home/user > \"$D66_OUTPUT_DIR/disk-stop\"; "
        f"printf '%s\\n' \"$rc\" > \"$D66_OUTPUT_DIR/runner-exit\"; "
        f"printf '%s\\n' 'KEEP before service cleanup' > \"$D66_OUTPUT_DIR/KEEP\"; exit \"$rc\""
    )
    return [f"runtime d141-p5-cut {body}"]


def _check_owner_mode(path: Path, label: str, *, directory: bool = False) -> None:
    stat = path.stat()
    if stat.st_uid != os.getuid() or stat.st_mode & 0o022:
        raise RouteError(f"{label} has unsafe owner or mode")
    expected = 0o700 if directory else 0o600
    if not directory and (stat.st_mode & 0o777) != expected:
        raise RouteError(f"{label} has unsafe mode")


def _check_install_path(destination: Path) -> None:
    if not destination.is_absolute() or any(part in {".", ".."} for part in destination.parts):
        raise RouteError("installer destination has unsafe path components")
    if destination == ROOT or ROOT in destination.parents:
        raise RouteError("installer destination must be separate from the route")
    if destination.is_symlink():
        raise RouteError("installer destination is a symlink")
    parent = destination.parent
    if not parent.is_dir() or parent.is_symlink():
        raise RouteError("installer parent is not a regular directory")
    current = parent
    while True:
        if current.is_symlink() or not current.is_dir():
            raise RouteError("installer parent is unsafe")
        parent_stat = current.stat()
        writable = parent_stat.st_mode & 0o022
        if parent_stat.st_uid != os.getuid() or (writable and not (parent_stat.st_mode & 0o1000)):
            raise RouteError("installer parent has unsafe owner or mode")
        if current.parent == current:
            break
        current = current.parent
    if destination.exists():
        if not destination.is_dir():
            raise RouteError("installer destination is not a directory")
        _check_owner_mode(destination, "installer destination", directory=True)


def _expected_files(config: dict[str, Any], rows: str) -> dict[str, str]:
    agent = _derive_agent(config["route"]["agent"])
    return {
        "suites.conf": rows,
        "d141-p5-cut.env": (
            "D141_ROUTE=d141-p5-cut\n"
            f"D141_RUNTIME_COMMIT={EXPECTED_RUNTIME['commit']}\n"
            f"D141_RUNTIME_TREE={EXPECTED_RUNTIME['tree']}\n"
            f"D141_AGENT_COMMIT={agent['commit']}\n"
            f"D141_AGENT_TREE={agent['tree']}\n"
        ),
    }


def install_candidate(config: dict[str, Any], destination: Path) -> None:
    """Atomically publish a private candidate directory after full preflight."""
    rows = render_rows(config)
    row_text = "\n".join(rows) + "\n"
    _check_install_path(destination)
    expected = _expected_files(config, row_text)
    if destination.exists():
        entries = {path.name for path in destination.iterdir()}
        if entries != set(expected):
            raise RouteError("private CAS destination has unexpected files")
        for name, text in expected.items():
            path = destination / name
            if path.is_symlink() or not path.is_file():
                raise RouteError(f"installer target {name} is unsafe")
            _check_owner_mode(path, f"installer target {name}")
            if path.read_text(encoding="utf-8") != text:
                raise RouteError("private CAS destination already contains different rows")
        return
    with tempfile.TemporaryDirectory(prefix=f".{ROOT.name}-", dir=destination.parent) as staging_name:
        staging = Path(staging_name)
        _check_owner_mode(staging, "installer staging", directory=True)
        for name, text in expected.items():
            path = staging / name
            path.write_text(text, encoding="utf-8")
            os.chmod(path, 0o600)
            _check_owner_mode(path, f"installer staging target {name}")
        os.replace(staging, destination)
        _check_owner_mode(destination, "installer destination", directory=True)


def run_control(output: Path, *, poison: bool = False) -> int:
    """Run one harmless subprocess and retain normal D66-shaped evidence."""
    if poison:
        raise RouteError("poison control refused before subprocess and artifacts")
    if not output.is_absolute() or output.exists():
        raise RouteError("control output must be a new absolute path")
    command = [sys.executable, "-c", "print('D141_P5_CONTROL_ONCE')"]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if completed.returncode != 0 or completed.stdout != "D141_P5_CONTROL_ONCE\n":
        raise RouteError("harmless control did not complete exactly once")
    output.mkdir(parents=True)
    d66 = output / "d66"
    d66.mkdir()
    runtime = Path("/home/user/work/runtime")
    agent = Path("/home/user/work/agent")
    source_paths = {
        "runtime_protocol": runtime / "runtime_protocol" / "__init__.py",
        "runtime_metadata": runtime / "runtime_protocol" / "contract_metadata.py",
        "runtime_contract": runtime / "contract" / "artifacts.json",
        "agent_provider": agent / PROVIDER_RELATIVE,
        "agent_client": agent / CLIENT_RELATIVE,
        "agent_metadata": agent / METADATA_RELATIVE,
    }
    argv = ["/home/user/work/venv-runtime/bin/python", *EXPECTED_ARGS, "--junitxml=$D66_OUTPUT_DIR/d141-p5-cut.xml"]
    shell = "env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=" + str(agent) + " " + " ".join(shlex.quote(value) for value in argv)
    (output / "exit").write_text(f"{completed.returncode}\n")
    (output / "log.txt").write_text(completed.stdout)
    (output / "request").write_text("repo=runtime\nsuite=d141-p5-cut\n")
    tree = _git(runtime, "rev-parse", "HEAD^{tree}")
    (output / "snap").write_text(f"tree={tree}\nworktree={runtime}\n")
    (output / "summary").write_text(f"cmd: {shell}; df -B1 --output=avail /home/user > $D66_OUTPUT_DIR/disk-start; rc=$?; df -B1 --output=avail /home/user > $D66_OUTPUT_DIR/disk-stop; printf '%s' $rc > $D66_OUTPUT_DIR/runner-exit; printf KEEP > $D66_OUTPUT_DIR/KEEP\n")
    (d66 / "argv.json").write_text(json.dumps(argv) + "\n")
    (d66 / "module-origin.json").write_text(json.dumps({key: str(path) for key, path in source_paths.items()}, sort_keys=True) + "\n")
    (d66 / "source-hashes.json").write_text(json.dumps({str(path): _sha256(path) for path in source_paths.values()}, sort_keys=True) + "\n")
    (d66 / "disk-start").write_text("Filesystem\n9000000000\n")
    (d66 / "disk-stop").write_text("Filesystem\n8999999999\n")
    (d66 / "runner-exit").write_text(f"{completed.returncode}\n")
    (d66 / "d141-p5-cut.xml").write_text('<?xml version="1.0"?><testsuite name="d141-p5-cut" tests="1"><testcase classname="control" name="D141_P5_CONTROL_ONCE"/></testsuite>\n')
    (d66 / "KEEP").write_text("retain D141 P5 control evidence\n")
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("status", "render", "install", "control"))
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--poison", action="store_true")
    args = parser.parse_args(argv)
    config = load_config()
    if args.command == "status":
        status, missing = route_status(config)
        print(json.dumps({"status": status, "missing": missing}, sort_keys=True))
        return 0
    if args.command == "render":
        print("\n".join(render_rows(config)))
        return 0
    if args.path is None:
        parser.error(f"{args.command} requires a path")
    if args.command == "install":
        install_candidate(config, args.path)
        return 0
    return run_control(args.path, poison=args.poison)


if __name__ == "__main__":
    raise SystemExit(main())
