#!/usr/bin/env python3
"""Prepare and validate the private D141 P5 cut row.

The module is deliberately a route validator, not a test runner.  It only
renders a row after a reviewed Agent custody receipt binds a clean checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "route-config.json"
HEX40 = set("0123456789abcdef")
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
    fields = ("commit", "tree", "checkout", "receipt", "provider_origin",
              "client_origin", "schema_digest", "lock_values")
    if agent["status"] == "pending":
        if any(agent.get(field) is not None for field in fields):
            raise RouteError("pending Agent has a partial custody tuple")
        return
    _hash(agent.get("commit"), "Agent commit")
    _hash(agent.get("tree"), "Agent tree")
    for field in ("checkout", "receipt", "provider_origin", "client_origin"):
        _absolute(agent.get(field), f"Agent {field}")
    if not isinstance(agent.get("schema_digest"), str) or not agent["schema_digest"].startswith("sha256:"):
        raise RouteError("Agent schema digest is missing")
    if not isinstance(agent.get("lock_values"), dict) or not agent["lock_values"]:
        raise RouteError("Agent lock values are missing")


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
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise RouteError(f"cannot read route configuration: {error}") from error
    return _validate_config(data)


def route_status(config: dict[str, Any]) -> tuple[str, list[str]]:
    agent = config["route"]["agent"]
    if agent["status"] != "qualified":
        return "NOT_READY", ["genuine final Agent cut receipt is pending"]
    return "READY", []


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=10).strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise RouteError(f"cannot inspect source checkout {root}: {error}") from error


def _verify_checkout(path: str, commit: str, tree: str, label: str) -> Path:
    root = Path(path)
    if not root.is_absolute() or not root.is_dir() or root.is_symlink():
        raise RouteError(f"{label} checkout is not a regular absolute directory")
    actual = (_git(root, "rev-parse", "HEAD"), _git(root, "rev-parse", "HEAD^{tree}"), _git(root, "status", "--porcelain"))
    if actual != (commit, tree, ""):
        raise RouteError(f"{label} source mismatch: commit={actual[0]} tree={actual[1]} dirty={bool(actual[2])}")
    return root


def _verify_source_membership(runtime: Path) -> None:
    for relative, expected in EXPECTED_FILES.items():
        path = runtime / relative
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RouteError(f"source membership hash mismatch: {relative}")


def _verify_receipt(agent: dict[str, Any]) -> None:
    receipt_path = Path(agent["receipt"])
    if not receipt_path.is_file() or receipt_path.is_symlink():
        raise RouteError("Agent cut receipt is not a regular file")
    try:
        receipt = json.loads(receipt_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise RouteError(f"Agent cut receipt is unreadable: {error}") from error
    for key in ("commit", "tree", "checkout", "provider_origin", "client_origin", "schema_digest", "lock_values"):
        if receipt.get(key) != agent[key]:
            raise RouteError(f"Agent cut receipt does not bind {key}")


def _source_guard(config: dict[str, Any], runtime: Path, agent: dict[str, Any]) -> str:
    agent_checkout = shlex.quote(agent["checkout"])
    runtime_checkout = shlex.quote(str(runtime))
    return (
        f"test \"$(git -C {runtime_checkout} rev-parse HEAD)\" = {shlex.quote(EXPECTED_RUNTIME['commit'])}"
        f" && test \"$(git -C {runtime_checkout} rev-parse HEAD^{{tree}})\" = {shlex.quote(EXPECTED_RUNTIME['tree'])}"
        f" && test -z \"$(git -C {runtime_checkout} status --porcelain)\""
        f" && test \"$(git -C {agent_checkout} rev-parse HEAD)\" = {shlex.quote(agent['commit'])}"
        f" && test \"$(git -C {agent_checkout} rev-parse HEAD^{{tree}})\" = {shlex.quote(agent['tree'])}"
        f" && test -z \"$(git -C {agent_checkout} status --porcelain)\""
    )


def render_rows(config: dict[str, Any]) -> list[str]:
    status, missing = route_status(config)
    if status != "READY":
        raise RouteError("pending tuple: " + "; ".join(missing))
    route = config["route"]
    agent = route["agent"]
    runtime = _verify_checkout(route["runtime"]["checkout"], EXPECTED_RUNTIME["commit"], EXPECTED_RUNTIME["tree"], "Runtime")
    _verify_source_membership(runtime)
    _verify_checkout(agent["checkout"], agent["commit"], agent["tree"], "Agent")
    _verify_receipt(agent)
    command = " ".join(shlex.quote(part) for part in config["pytest"]["arguments"])
    unset = " ".join(f"-u {name}" for name in config["pytest"]["environment_unset"])
    junit = f'"$D141_OUTPUT_DIR/{config["pytest"]["junit_name"]}"'
    body = (
        f"env {unset} ASTRID_CHECKOUT={shlex.quote(agent['checkout'])} "
        f"PYTHONPATH={shlex.quote(str(runtime) + ':' + agent['checkout'])} "
        f"{shlex.quote(config['pytest']['interpreter'])} {command} --junitxml={junit}"
    )
    return [f"d141-p5-cut cwd={shlex.quote(str(runtime))} guard={_source_guard(config, runtime, agent)} run={body}"]


def install_candidate(config: dict[str, Any], destination: Path) -> None:
    if not destination.is_absolute() or destination.resolve() == ROOT:
        raise RouteError("CAS destination must be a separate absolute directory")
    rows = render_rows(config)
    row_text = "\n".join(rows) + "\n"
    if destination.exists() and not destination.is_dir():
        raise RouteError("CAS destination is not a directory")
    if destination.exists() and any(destination.iterdir()):
        expected = destination / "suites.conf"
        if not expected.is_file() or expected.read_text() != row_text:
            raise RouteError("CAS destination already contains different rows")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "suites.conf").write_text(row_text)
    (destination / "d141-p5-cut.env").write_text(
        "D141_ROUTE=d141-p5-cut\n"
        f"D141_RUNTIME_COMMIT={EXPECTED_RUNTIME['commit']}\n"
        f"D141_RUNTIME_TREE={EXPECTED_RUNTIME['tree']}\n"
        f"D141_AGENT_COMMIT={config['route']['agent']['commit']}\n"
        f"D141_AGENT_TREE={config['route']['agent']['tree']}\n"
    )


def run_control(output: Path, *, poison: bool = False) -> int:
    """Run one harmless named-row control, never the P5 body."""
    if poison:
        raise RouteError("poison control refused before subprocess and artifacts")
    if not output.is_absolute() or output.exists():
        raise RouteError("control output must be a new absolute path")
    command = [sys.executable, "-c", "print('D141_P5_CONTROL_ONCE')"]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if completed.returncode != 0 or completed.stdout != "D141_P5_CONTROL_ONCE\n":
        raise RouteError("harmless control did not complete exactly once")
    output.mkdir(parents=True)
    (output / "exit").write_text(f"{completed.returncode}\n")
    (output / "argv.json").write_text(json.dumps(command) + "\n")
    (output / "module-origin.json").write_text(json.dumps({"route": str(ROOT)}) + "\n")
    (output / "source-hashes.json").write_text(json.dumps(EXPECTED_FILES, sort_keys=True) + "\n")
    (output / "start.json").write_text('{"started": true}\n')
    (output / "stop.json").write_text('{"stopped": true}\n')
    (output / "disk.json").write_text('{"artifacts": "control-only"}\n')
    (output / "d141-p5-cut.xml").write_text('<?xml version="1.0"?><testsuite tests="1" failures="0"/>\n')
    (output / "KEEP").write_text("retain D141 P5 control evidence\n")
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
