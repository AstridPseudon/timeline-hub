#!/usr/bin/env python3
"""Private D141 Runtime full-suite route preparation.

This module only validates and renders candidate service rows.  It does not
import Runtime or Agent, mutate the service registry, or launch a product
test.  The final Agent bindings must arrive in a reviewed checkout receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "route-config.json"
HEX40 = set("0123456789abcdef")
FORBIDDEN = ("41ad", "9521", "placeholder", "assumed", "fallback")
DONE_CREATED = re.compile(
    r"^created (?P<path>/home/user/work/wt/agt-pin-[0-9a-f]{8}) "
    r"\(detached at (?P<commit>[0-9a-f]{40}), KEEP\)$"
)
DONE_EXISTS = re.compile(
    r"^exists: (?P<path>/home/user/work/wt/agt-pin-[0-9a-f]{8}) "
    r"at (?P<commit>[0-9a-f]{40})$"
)
SCHEMA_DIGEST = re.compile(r"SCHEMA_DIGEST\s*=\s*['\"](sha256:[0-9a-f]{64})['\"]")


class RouteError(ValueError):
    """A candidate route is not safe to install or launch."""


def load_config(path: Path = CONFIG) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise RouteError("unsupported route configuration")
    routes = data.get("routes")
    if not isinstance(routes, list) or len(routes) != 2:
        raise RouteError("exactly two D141 routes are required")
    names = [route.get("name") if isinstance(route, dict) else None for route in routes]
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
    name = route.get("name")
    if name != f"full-d141-{route['kind']}":
        raise RouteError("route name and kind disagree")
    runtime = route.get("runtime")
    if not isinstance(runtime, dict):
        raise RouteError("runtime identity is missing")
    _validate_hex(runtime.get("commit"), 40, f"{name} runtime commit")
    _validate_hex(runtime.get("tree"), 40, f"{name} runtime tree")
    agent = route.get("agent")
    if not isinstance(agent, dict) or agent.get("status") not in {"pending", "qualified"}:
        raise RouteError(f"{name} Agent status is invalid")
    expected_commit = agent.get("expected_commit")
    expected_tree = agent.get("expected_tree")
    if expected_commit is not None:
        _validate_hex(expected_commit, 40, f"{name} expected Agent commit")
    if expected_tree is not None:
        _validate_hex(expected_tree, 40, f"{name} expected Agent tree")
    if route["kind"] == "pristine" and (
        expected_commit != "8b6ed2116fd1803d24b2be5bc08bd9490407fe4a"
        or expected_tree != "0a3691a49b63fd7b0c22fb3478e9cf1947f266ed"
    ):
        raise RouteError("pristine Agent frozen identity is not exact")
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
            raise RouteError(f"{name} pending Agent has partial binding")
    else:
        _validate_hex(agent.get("commit"), 40, f"{name} Agent commit")
        _validate_hex(agent.get("tree"), 40, f"{name} Agent tree")
        if expected_commit is not None:
            if agent["commit"] != expected_commit:
                raise RouteError(f"{name} Agent commit is not the expected frozen tip")
        if expected_tree is not None:
            if agent["tree"] != expected_tree:
                raise RouteError(f"{name} Agent tree is not the expected frozen tree")
        checkout = agent.get("checkout")
        receipt = agent.get("receipt")
        if not isinstance(checkout, str) or not checkout.startswith("/"):
            raise RouteError(f"{name} Agent checkout is not absolute")
        if not isinstance(receipt, str) or not receipt.startswith("/"):
            raise RouteError(f"{name} Agent receipt is not absolute")
        for key in ("provider_origin", "client_origin"):
            if not isinstance(agent.get(key), str) or not agent[key].startswith("/"):
                raise RouteError(f"{name} {key} is not an absolute origin")
        if not isinstance(agent.get("schema_digest"), str) or not agent["schema_digest"].startswith("sha256:"):
            raise RouteError(f"{name} schema digest is missing")
        if not isinstance(agent.get("lock_values"), dict) or not agent["lock_values"]:
            raise RouteError(f"{name} actual lock values are missing")


def _regular_file(path: Path, label: str) -> None:
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise RouteError(f"{label} is not a regular file")


def _inside(root: Path, path: Path, label: str) -> None:
    try:
        path.relative_to(root)
    except ValueError as error:
        raise RouteError(f"{label} is outside its bound checkout") from error


def _read_checkout_done(receipt: Path, expected_commit: str | None) -> tuple[Path, str]:
    _regular_file(receipt, "checkout done receipt")
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
        raise RouteError("checkout done receipt commit is not the expected frozen tip")
    return checkout, commit


def route_status(config: dict[str, Any]) -> tuple[str, list[str]]:
    missing: list[str] = []
    for route in config["routes"]:
        agent = route["agent"]
        if agent["status"] != "qualified":
            label = "pristine Agent request-checkout receipt" if route["kind"] == "pristine" else "Agent cut checkout receipt"
            missing.append(f"{route['name']}: {label}")
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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def _verify_agent_binding(route: dict[str, Any]) -> tuple[Path, str, str]:
    agent = route["agent"]
    if agent["status"] != "qualified":
        raise RouteError(f"{route['name']} Agent receipt is pending")
    expected_commit = agent.get("expected_commit")
    checkout, receipt_commit = _read_checkout_done(Path(agent["receipt"]), expected_commit)
    if receipt_commit != agent["commit"] or str(checkout) != agent["checkout"]:
        raise RouteError(f"{route['name']} checkout identity disagrees with its done receipt")
    _verify_checkout(str(checkout), agent["commit"], agent["tree"], f"{route['name']} Agent")
    keep = Path(agent["receipt"]).parents[2] / "workers" / checkout.name / "KEEP"
    _regular_file(keep, f"{route['name']} checkout KEEP witness")

    root = checkout.resolve()
    for key in ("provider_origin", "client_origin"):
        origin = Path(agent[key])
        _regular_file(origin, f"{route['name']} {key}")
        _inside(root, origin.resolve(), f"{route['name']} {key}")
    metadata = root / "astrid_runtime_client" / "contract_metadata.py"
    _regular_file(metadata, f"{route['name']} client metadata")
    schema_match = SCHEMA_DIGEST.search(metadata.read_text(encoding="utf-8"))
    if schema_match is None or schema_match[1] != agent["schema_digest"]:
        raise RouteError(f"{route['name']} schema digest is not derived from the checkout")
    client_text = Path(agent["client_origin"]).read_text(encoding="utf-8")
    client_match = SCHEMA_DIGEST.search(client_text)
    if client_match is None or client_match[1] != agent["schema_digest"]:
        raise RouteError(f"{route['name']} client metadata digest disagrees")
    for lock_path, expected_hash in agent["lock_values"].items():
        candidate = Path(lock_path)
        if not candidate.is_absolute():
            candidate = root / candidate
        _regular_file(candidate, f"{route['name']} lock metadata")
        _inside(root, candidate.resolve(), f"{route['name']} lock metadata")
        if not isinstance(expected_hash, str) or expected_hash != _sha256(candidate):
            raise RouteError(f"{route['name']} lock metadata is not derived from the checkout")
    return checkout, agent["commit"], agent["tree"]


def _source_guard(route: dict[str, Any], agent: dict[str, Any]) -> str:
    runtime = route["runtime"]
    checkout = shlex.quote(agent["checkout"])
    runtime_commit = shlex.quote(runtime["commit"])
    runtime_tree = shlex.quote(runtime["tree"])
    agent_commit = shlex.quote(agent["commit"])
    agent_tree = shlex.quote(agent["tree"])
    return (
        "( test \"$(git rev-parse HEAD)\" = "
        + runtime_commit
        + " || test \"$(git rev-parse HEAD^)\" = "
        + runtime_commit
        + " )"
        + " && test \"$(git rev-parse HEAD^{tree})\" = "
        + runtime_tree
        + " && test -z \"$(git status --porcelain)\""
        + " && test -d "
        + checkout
        + " && test ! -L "
        + checkout
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
    bindings: list[tuple[Path, str, str]] = []
    for route in config["routes"]:
        bindings.append(_verify_agent_binding(route))
    if len({str(binding[0]) for binding in bindings}) != len(bindings):
        raise RouteError("cut and pristine Agent bindings must be distinct")
    if len({binding[1] for binding in bindings}) != len(bindings):
        raise RouteError("cut and pristine Agent commits must be distinct")
    if len({binding[2] for binding in bindings}) != len(bindings):
        raise RouteError("cut and pristine Agent trees must be distinct")
    rows: list[str] = []
    for route, _binding in zip(config["routes"], bindings):
        agent = route["agent"]
        checkout = shlex.quote(agent["checkout"])
        command = " ".join(shlex.quote(part) for part in config["pytest"]["arguments"])
        junit = f'"$D66_OUTPUT_DIR/{config["pytest"]["junit_name"]}"'
        output_setup = (
            'test -n "${D66_OUTPUT_DIR:-}" && '
            'case "$D66_OUTPUT_DIR" in /*) ;; *) false ;; esac && '
            'test "$D66_OUTPUT_DIR" != / && '
            'if test -L "$D66_OUTPUT_DIR"; then '
            'false; '
            'elif test -e "$D66_OUTPUT_DIR"; then '
            'test -d "$D66_OUTPUT_DIR"; '
            'else '
            '( umask 077 && mkdir -- "$D66_OUTPUT_DIR" ); '
            'fi && '
            'test -d "$D66_OUTPUT_DIR" && test ! -L "$D66_OUTPUT_DIR"'
        )
        body = (
            f"{_source_guard(route, agent)} && "
            f"{output_setup} && {{ "
            f"df -B1 --output=avail /home/user > \"$D66_OUTPUT_DIR/disk-start\" && "
            f"env ASTRID_CHECKOUT={checkout} "
            f"{shlex.quote(config['pytest']['interpreter'])} {command} "
            f"--junitxml={junit}; rc=$?; "
            f"df -B1 --output=avail /home/user > \"$D66_OUTPUT_DIR/disk-stop\"; "
            f"printf '%s\\n' \"$rc\" > \"$D66_OUTPUT_DIR/runner-exit\"; "
            f"printf '%s\\n' 'KEEP before service cleanup' > \"$D66_OUTPUT_DIR/KEEP\"; "
            f"exit \"$rc\"; }}"
        )
        rows.append(f"runtime {route['name']} {body}")
    return rows


def install_candidate(config: dict[str, Any], destination: Path) -> None:
    """CAS-install rows into an explicit private directory only.

    The central service registry is intentionally not a valid destination.
    """
    if not destination.is_absolute() or any(part in {".", ".."} for part in destination.parts):
        raise RouteError("installer destination has unsafe path components")
    if destination == ROOT or ROOT in destination.parents:
        raise RouteError("installer destination must be a separate absolute directory")
    rows = render_rows(config)
    _check_install_path(destination)
    row_text = "\n".join(rows) + "\n"
    row_path = destination / "suites.conf"
    _check_install_file(row_path)
    if row_path.exists() and row_path.read_text() != row_text:
        raise RouteError("private CAS destination already contains different rows")
    env_paths: list[tuple[Path, str]] = []
    for route in config["routes"]:
        env_path = destination / f"{route['name']}.env"
        env_text = (
            f"D141_ROUTE={route['name']}\n"
            f"D141_RUNTIME_COMMIT={route['runtime']['commit']}\n"
            f"D141_RUNTIME_TREE={route['runtime']['tree']}\n"
            f"D141_AGENT_COMMIT={route['agent']['commit']}\n"
            f"D141_AGENT_TREE={route['agent']['tree']}\n"
        )
        _check_install_file(env_path)
        if env_path.exists() and env_path.read_text() != env_text:
            raise RouteError(f"private CAS destination already contains {env_path.name}")
        env_paths.append((env_path, env_text))
    destination.mkdir(parents=True, exist_ok=True)
    if not row_path.exists():
        row_path.write_text(row_text)
    for env_path, env_text in env_paths:
        if not env_path.exists():
            env_path.write_text(env_text)


def _check_install_path(destination: Path) -> None:
    # Inspect from the root so an existing child cannot hide a symlink above it.
    for parent in (*reversed(destination.parents), destination):
        if parent.is_symlink():
            raise RouteError("installer parent is a symlink")
        if parent.exists():
            if not parent.is_dir():
                raise RouteError("installer parent is not a directory")
            _check_parent_mode(parent, "installer parent")
    if destination.exists():
        if destination.is_symlink() or not destination.is_dir():
            raise RouteError("installer destination must be a regular directory")
        _check_owner_mode(destination, "installer destination")


def _check_install_file(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or not path.is_file():
        raise RouteError(f"installer target {path.name} is unsafe")
    _check_owner_mode(path, f"installer target {path.name}")


def _check_owner_mode(path: Path, label: str) -> None:
    stat = path.stat()
    if stat.st_uid != os.getuid() or stat.st_mode & 0o022:
        raise RouteError(f"{label} has unsafe owner or mode")


def _check_parent_mode(path: Path, label: str) -> None:
    stat = path.stat()
    writable = stat.st_mode & 0o022
    if stat.st_uid != os.getuid() or writable and not (path.is_dir() and stat.st_mode & 0o1000):
        raise RouteError(f"{label} has unsafe owner or mode")


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
