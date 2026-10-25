#!/usr/bin/env python3
"""Private D141 Runtime full-suite route preparation.

This module only validates and renders candidate service rows.  It does not
import Runtime or Agent, mutate the service registry, or launch a product
test.  The final Agent bindings must arrive in a reviewed checkout receipt.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "route-config.json"
HEX40 = set("0123456789abcdef")
FORBIDDEN = ("41ad", "9521", "placeholder", "assumed")


class RouteError(ValueError):
    """A candidate route is not safe to install or launch."""


def load_config(path: Path = CONFIG) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise RouteError("unsupported route configuration")
    routes = data.get("routes")
    if not isinstance(routes, list) or len(routes) != 2:
        raise RouteError("exactly two D141 routes are required")
    names = [route.get("name") for route in routes]
    if names != ["full-d141-cut", "full-d141-pristine"]:
        raise RouteError("route names or order changed")
    if len(set(names)) != len(names):
        raise RouteError("duplicate route key")
    for route in routes:
        _validate_route(route)
    pytest = data.get("pytest")
    if pytest != {
        "interpreter": "/home/user/work/venv-runtime/bin/python",
        "arguments": ["-m", "pytest", "-q", "-n3"],
        "junit_name": "runtime-full.xml",
    }:
        raise RouteError("normal Runtime pytest command changed")
    required = data.get("required")
    if not isinstance(required, list) or len(required) != 4 or len(set(required)) != 4:
        raise RouteError("required input manifest is incomplete or duplicated")
    encoded = path.read_text()
    if any(token in encoded.lower() for token in FORBIDDEN):
        raise RouteError("forbidden assumed or placeholder source marker")
    return data


def _validate_hex(value: Any, length: int, label: str) -> None:
    if not isinstance(value, str) or len(value) != length or set(value) - HEX40:
        raise RouteError(f"{label} must be a lowercase {length}-character hash")


def _validate_route(route: dict[str, Any]) -> None:
    if not isinstance(route, dict) or route.get("kind") not in {"cut", "pristine"}:
        raise RouteError("invalid route entry")
    runtime = route.get("runtime")
    if not isinstance(runtime, dict):
        raise RouteError("runtime identity is missing")
    _validate_hex(runtime.get("commit"), 40, f"{route['name']} runtime commit")
    _validate_hex(runtime.get("tree"), 40, f"{route['name']} runtime tree")
    agent = route.get("agent")
    if not isinstance(agent, dict) or agent.get("status") not in {"pending", "qualified"}:
        raise RouteError(f"{route['name']} Agent status is invalid")
    if agent["status"] == "pending":
        if any(
            agent.get(key) is not None
            for key in (
                "commit",
                "tree",
                "checkout",
                "receipt",
                "provider_origin",
                "client_origin",
                "schema_digest",
                "lock_values",
            )
        ):
            raise RouteError(f"{route['name']} pending Agent has partial binding")
    else:
        _validate_hex(agent.get("commit"), 40, f"{route['name']} Agent commit")
        _validate_hex(agent.get("tree"), 40, f"{route['name']} Agent tree")
        checkout = agent.get("checkout")
        receipt = agent.get("receipt")
        if not isinstance(checkout, str) or not checkout.startswith("/"):
            raise RouteError(f"{route['name']} Agent checkout is not absolute")
        if not isinstance(receipt, str) or not receipt.startswith("/"):
            raise RouteError(f"{route['name']} Agent receipt is not absolute")
        for key in ("provider_origin", "client_origin"):
            if not isinstance(agent.get(key), str) or not agent[key].startswith("/"):
                raise RouteError(f"{route['name']} {key} is not an absolute origin")
        if not isinstance(agent.get("schema_digest"), str) or not agent["schema_digest"].startswith("sha256:"):
            raise RouteError(f"{route['name']} schema digest is missing")
        if not isinstance(agent.get("lock_values"), dict) or not agent["lock_values"]:
            raise RouteError(f"{route['name']} actual lock values are missing")


def route_status(config: dict[str, Any]) -> tuple[str, list[str]]:
    missing: list[str] = []
    for route in config["routes"]:
        agent = route["agent"]
        if agent["status"] != "qualified":
            missing.append(f"{route['name']}: Agent cut checkout receipt")
    if missing:
        return "NOT_READY", missing
    return "READY", missing


def _verify_checkout(path: str, commit: str, tree: str, label: str) -> None:
    root = Path(path)
    if not root.is_absolute() or not root.is_dir() or root.is_symlink():
        raise RouteError(f"{label} checkout is not a regular absolute directory")
    try:
        actual_commit = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True, timeout=10
        ).strip()
        actual_tree = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], text=True, timeout=10
        ).strip()
        dirty = subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain"], text=True, timeout=10
        ).strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise RouteError(f"{label} checkout cannot be inspected: {error}") from error
    if (actual_commit, actual_tree, dirty) != (commit, tree, ""):
        raise RouteError(
            f"{label} source mismatch: commit={actual_commit} tree={actual_tree} dirty={bool(dirty)}"
        )


def _source_guard(route: dict[str, Any], agent: dict[str, Any]) -> str:
    runtime = route["runtime"]
    checkout = shlex.quote(agent["checkout"])
    runtime_commit = shlex.quote(runtime["commit"])
    runtime_tree = shlex.quote(runtime["tree"])
    agent_commit = shlex.quote(agent["commit"])
    agent_tree = shlex.quote(agent["tree"])
    return (
        "test \"$(git rev-parse HEAD)\" = "
        + runtime_commit
        + " && test \"$(git rev-parse HEAD^{tree})\" = "
        + runtime_tree
        + " && test -z \"$(git status --porcelain)\""
        + " && test \"$(git -C "
        + checkout
        + " rev-parse HEAD)\" = "
        + agent_commit
        + " && test \"$(git -C "
        + checkout
        + " rev-parse HEAD^{tree})\" = "
        + agent_tree
        + " && test -z \"$(git -C "
        + checkout
        + " status --porcelain)\""
    )


def render_rows(config: dict[str, Any]) -> list[str]:
    status, missing = route_status(config)
    if status != "READY":
        raise RouteError("pending tuple: " + "; ".join(missing))
    rows: list[str] = []
    for route in config["routes"]:
        agent = route["agent"]
        _verify_checkout(
            agent["checkout"], agent["commit"], agent["tree"], f"{route['name']} Agent"
        )
        checkout = shlex.quote(agent["checkout"])
        command = " ".join(shlex.quote(part) for part in config["pytest"]["arguments"])
        junit = f'"$D66_OUTPUT_DIR/{config["pytest"]["junit_name"]}"'
        body = (
            f"{_source_guard(route, agent)} && env ASTRID_CHECKOUT={checkout} "
            f"{shlex.quote(config['pytest']['interpreter'])} {command} "
            f"--junitxml={junit}"
        )
        rows.append(f"runtime {route['name']} {body}")
    return rows


def install_candidate(config: dict[str, Any], destination: Path) -> None:
    """CAS-install rows into an explicit private directory only.

    The central service registry is intentionally not a valid destination.
    """
    if destination.resolve() == ROOT or not destination.is_absolute():
        raise RouteError("installer destination must be a separate absolute directory")
    rows = render_rows(config)
    destination.mkdir(parents=True, exist_ok=True)
    row_text = "\n".join(rows) + "\n"
    row_path = destination / "suites.conf"
    if row_path.exists() and row_path.read_text() != row_text:
        raise RouteError("private CAS destination already contains different rows")
    row_path.write_text(row_text)
    for route in config["routes"]:
        env_path = destination / f"{route['name']}.env"
        env_text = (
            f"D141_ROUTE={route['name']}\n"
            f"D141_RUNTIME_COMMIT={route['runtime']['commit']}\n"
            f"D141_RUNTIME_TREE={route['runtime']['tree']}\n"
            f"D141_AGENT_COMMIT={route['agent']['commit']}\n"
            f"D141_AGENT_TREE={route['agent']['tree']}\n"
        )
        if env_path.exists() and env_path.read_text() != env_text:
            raise RouteError(f"private CAS destination already contains {env_path.name}")
        env_path.write_text(env_text)


def run_stub(config: dict[str, Any], output: Path) -> int:
    """Exercise the normal pytest argv against a harmless one-test stub.

    This is a route control, never a Runtime or Agent import/collection.
    """
    output.mkdir(parents=True, exist_ok=True)
    stub = output / "test_stub.py"
    stub.write_text("def test_d141_route_stub():\n    assert True\n")
    junit = output / "stub.xml"
    command = [
        "/home/user/work/venv-agent/bin/python",
        *config["pytest"]["arguments"],
        f"--junitxml={junit}",
        str(stub),
    ]
    environment = os.environ.copy()
    environment["D66_OUTPUT_DIR"] = str(output)
    completed = subprocess.run(command, cwd=output, env=environment, check=False)
    if completed.returncode != 0 or not junit.is_file():
        raise RouteError(f"stub route failed with exit {completed.returncode}")
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("status", "render", "install", "stub"))
    parser.add_argument("path", nargs="?", type=Path)
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
    return run_stub(config, args.path)


if __name__ == "__main__":
    raise SystemExit(main())
