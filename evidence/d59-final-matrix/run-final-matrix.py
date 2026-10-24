#!/usr/bin/env python3
"""Dispatch the final Timeline venues from one already-captured tuple.

This is a private D59 preparation runner.  It never captures integration heads,
requests a checkout, edits a registry, or silently substitutes a newer home.
The D73/D84 submit and core runners remain the custody authority; this file only
validates their durable inputs and dispatches the normal request-test seam.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REPOS = ("agent", "runtime", "app", "composition")
ORCH = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
)
REQUEST_TEST = ORCH / "bin/request-test"
D84 = Path(__file__).resolve().parent / "inherited-d84"
INHERITED = {
    "run-final-services.py": "05c5662aa14c3bb288f672421d448335a0b10df659fd58439e6abd296c4c3a97",
    "submit-final.py": "345c8663dde1379264f913e0b72657dbe0d326aac13571dd5cc1e0700087bcca",
    "acceptance-d73.py": "08d69d10a58c8b65ded99165054e6f11e42fcaf9c9c9471b57cdaa2d2d81d8f8",
    "core-inventory.json": "9705979776ebb9182d986e9364a29911fafd04227e817f5f19346e8fd116bb97",
    "runtime-final-service-rows.txt": "be2572c2b4ea888237a8696c15e68505010da4453df93aba9ff876b724e2553a",
    "install-final-services.py": "6e7eafca3f31c559e07d85a69ef9ac1f785679f727dad831b005a9cb9c6e01f1",
    "run-final-delivery.py": "cf714b7d6105ddf1bd752f311bb2982896e5b67e4988b4096417e6b30f8237f8",
    "submit-packet.md": "450f67c20acbf5dee1ec229a150ca35e1ea438e432145f66a1c6e9958cd7ca93",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file(path: Path, label: str) -> Path:
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} must be an absolute regular file: {path}")
    return path


def route_table() -> list[dict[str, Any]]:
    files = {
        "p1": "tests/e2e/local/three-products.p1-chain.spec.ts",
        "p2": "tests/e2e/local/three-products.p2-tour.spec.ts tests/e2e/local/three-products.p2-elements-assets.spec.ts tests/e2e/local/three-products.p2-popup.spec.ts",
        "p3": "tests/e2e/local/three-products.spec.ts",
    }
    return [
        {"id": "app-p1", "venue": "app", "target": "app", "suite": "full-e2e-three-products", "files": files["p1"], "kind": "request-test"},
        {"id": "app-p2", "venue": "app", "target": "app", "suite": "full-e2e-three-products", "files": files["p2"], "kind": "request-test", "requires": {"p2_isolated_passes": 8}},
        {"id": "app-p3", "venue": "app", "target": "app", "suite": "full-e2e-three-products", "files": files["p3"], "kind": "request-test"},
        {"id": "app-core", "venue": "app", "target": "app", "suite": "full", "files": None, "kind": "request-test"},
        {
            "id": "agent-p4", "venue": "agent", "target": "integration:agent", "suite": "p4-current-becfe-http-3legs",
            "files": None,
            "kind": "request-test", "availability": "PENDING_OWNER_REGISTRATION",
            "missing_input": "owner must publish the existing p4-current-becfe-http-3legs row in the installed suites.conf; final P4 remains the separate three-original-selector handoff",
        },
        {"id": "agent-core", "venue": "agent", "target": "agent", "suite": "full", "files": None, "kind": "request-test"},
        {"id": "agent-d77-render", "venue": "agent", "target": "agent", "suite": "m3-public13-bounded-files-gate", "files": None, "kind": "request-test", "availability": "PENDING_AUTHENTIC_ENVIRONMENT", "missing_input": "genuine installed D77 render environment and its received receipt"},
        {"id": "runtime-p5", "venue": "runtime", "target": "integration:runtime", "suite": "core-v2-final-integration", "files": None, "kind": "d84-core-runner"},
        {"id": "runtime-core", "venue": "runtime", "target": "runtime", "suite": "full", "files": None, "kind": "request-test"},
        {"id": "composition-full", "venue": "composition", "target": "composition", "suite": "full", "files": None, "kind": "request-test"},
    ]


def tuple_error(message: str) -> ValueError:
    return ValueError(f"final tuple refused: {message}")


def validate_d73_manifest(manifest: Any, repos: dict[str, Any]) -> None:
    required = {
        "format",
        *(f"{name}_{field}" for name in REPOS for field in ("sha", "tree", "path")),
        "agent_parents",
        "python",
        "node",
        "profile",
        "schema",
        "node_version",
        "profile_lock_sha",
        "profile_archive_sha",
        "profile_registry_sha",
        "composition_version",
        "original_p4_test_hash",
        "service_versions",
        "junit_paths",
    }
    if not isinstance(manifest, dict) or not required.issubset(manifest):
        raise tuple_error("D73 manifest fields are incomplete")
    if manifest["format"] != "p4-d73-v1":
        raise tuple_error("D73 manifest format is unsupported")
    for name in REPOS:
        if manifest[f"{name}_sha"] != repos[name]["sha"] or manifest[f"{name}_tree"] != repos[name]["tree"]:
            raise tuple_error(f"D73 {name} SHA/tree does not match the final tuple")
        if manifest[f"{name}_path"] != repos[name]["checkout_path"]:
            raise tuple_error(f"D73 {name} path does not match the selected checkout")
    for key in ("agent_parents", "python", "node", "profile", "schema", "node_version", "composition_version", "service_versions", "junit_paths"):
        if not isinstance(manifest[key], str) or not manifest[key]:
            raise tuple_error(f"D73 {key} is missing")
    for key in ("python", "node", "profile", "schema"):
        if not manifest[key].startswith("/"):
            raise tuple_error(f"D73 {key} is not an absolute path")
    for key in ("profile_lock_sha", "profile_archive_sha", "profile_registry_sha", "original_p4_test_hash"):
        if not isinstance(manifest[key], str) or not HEX64.fullmatch(manifest[key]):
            raise tuple_error(f"D73 {key} is not a lowercase SHA-256")


def validate_tuple_data(value: Any, *, expected_sha: str, check_git: bool) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("version") != 1:
        raise tuple_error("version must be 1")
    if value.get("status") != "READY":
        raise tuple_error("status is not READY; final tuple remains PENDING")
    repos = value.get("repos")
    if not isinstance(repos, dict) or set(repos) != set(REPOS):
        raise tuple_error("repos must contain exactly agent, runtime, app, composition")
    validate_d73_manifest(value.get("d73_manifest"), repos)
    if value.get("final_tuple_sha256") not in (expected_sha, "FINAL_TUPLE_SHA256_PENDING"):
        raise tuple_error("final_tuple_sha256 does not match the supplied tuple")
    schema = value.get("schema")
    if not isinstance(schema, dict) or not isinstance(schema.get("digest"), str) or not schema["digest"].startswith("sha256:") or not HEX64.fullmatch(schema["digest"][7:]):
        raise tuple_error("schema digest is missing or invalid")
    bindings = value.get("manifest_bindings")
    if not isinstance(bindings, dict) or not bindings:
        raise tuple_error("manifest_bindings is missing")
    receipts = value.get("test_receipts")
    if not isinstance(receipts, list) or not receipts:
        raise tuple_error("test_receipts is missing")
    readiness = value.get("route_readiness")
    if not isinstance(readiness, dict) or set(readiness) != {route["id"] for route in route_table()}:
        raise tuple_error("route_readiness is missing")
    d73_path = value.get("d73_source_tuple")
    d73_sha = value.get("d73_tuple_sha256")
    if not isinstance(d73_path, str) or not isinstance(d73_sha, str) or not HEX64.fullmatch(d73_sha):
        raise tuple_error("original D73 source tuple path/hash is missing")
    d73_file = Path(d73_path)
    if d73_file.is_symlink() or not d73_file.is_absolute() or not d73_file.is_file() or sha256(d73_file) != d73_sha:
        raise tuple_error("original D73 source tuple is unavailable or changed")
    for name in REPOS:
        item = repos[name]
        required = {"sha", "tree", "source_path", "checkout_path", "checkout_receipt", "checkout_receipt_sha256", "checkout_head", "checkout_tree"}
        if not isinstance(item, dict) or not required.issubset(item):
            raise tuple_error(f"{name} lacks pinned SHA/tree/path/receipt fields")
        for field in ("sha", "tree", "checkout_head", "checkout_tree"):
            if not isinstance(item[field], str) or not HEX40.fullmatch(item[field]):
                raise tuple_error(f"{name}.{field} is not a lowercase Git identity")
        if item["checkout_head"] != item["sha"] or item["checkout_tree"] != item["tree"]:
            raise tuple_error(f"{name} checkout identity is stale")
        if not isinstance(item["checkout_receipt_sha256"], str) or not HEX64.fullmatch(item["checkout_receipt_sha256"]):
            raise tuple_error(f"{name} checkout receipt hash is invalid")
        checkout = Path(item["checkout_path"])
        receipt = Path(item["checkout_receipt"])
        source = Path(item["source_path"])
        if not source.is_absolute() or source.is_symlink():
            raise tuple_error(f"{name} source path is not an absolute non-symlink path")
        if not checkout.is_absolute() or checkout.is_symlink() or not checkout.is_dir():
            raise tuple_error(f"{name} checkout path is unavailable or symlinked")
        if not receipt.is_absolute() or receipt.is_symlink() or not receipt.is_file():
            raise tuple_error(f"{name} checkout receipt is unavailable or symlinked")
        if sha256(receipt) != item["checkout_receipt_sha256"]:
            raise tuple_error(f"{name} checkout receipt changed")
        if check_git:
            def git(*args: str) -> str:
                return subprocess.check_output(["git", "-C", str(checkout), *args], text=True).strip()
            try:
                if git("rev-parse", "HEAD") != item["sha"] or git("rev-parse", "HEAD^{tree}") != item["tree"] or git("status", "--porcelain"):
                    raise tuple_error(f"{name} selected checkout drifted or is dirty")
            except (OSError, subprocess.CalledProcessError) as exc:
                raise tuple_error(f"{name} checkout cannot be inspected: {exc}") from exc
    return value


def load_tuple(path: Path, expected_sha: str, *, check_git: bool = True) -> dict[str, Any]:
    regular_file(path, "final tuple")
    actual = sha256(path)
    if actual != expected_sha:
        raise tuple_error(f"file SHA256 {actual} != {expected_sha}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise tuple_error(f"invalid JSON: {exc}") from exc
    return validate_tuple_data(value, expected_sha=expected_sha, check_git=check_git)


def inherited_paths() -> dict[str, str]:
    result = {}
    for name, expected in INHERITED.items():
        path = D84 / name
        regular_file(path, f"inherited D84 {name}")
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"inherited D84 {name} hash mismatch: {actual} != {expected}")
        result[name] = str(path)
    return result


def request_argv(route: dict[str, Any], request_test: Path) -> list[str]:
    command = [str(request_test), route["target"], route["suite"]]
    if route.get("files"):
        command.extend(["--files", route["files"]])
    command.append("--no-cache")
    return command


def route_plan(
    route: dict[str, Any],
    tuple_path: Path,
    tuple_sha: str,
    runner: Path,
    tuple_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if route["kind"] == "request-test":
        command = request_argv(route, REQUEST_TEST)
    else:
        source_tuple = tuple_value.get("d73_source_tuple") if tuple_value else "<d73_source_tuple>"
        source_sha = tuple_value.get("d73_tuple_sha256") if tuple_value else "<d73_tuple_sha256>"
        command = [sys.executable, str(runner), "--source-tuple", str(source_tuple), "--tuple-sha", str(source_sha), "core"]
    result = {"id": route["id"], "venue": route["venue"], "kind": route["kind"], "argv": command, "budget_seconds": 45, "availability": route.get("availability", "READY")}
    for field in ("missing_input", "requires"):
        if field in route:
            result[field] = route[field]
    return result


def route_missing_input(route: dict[str, Any], tuple_value: dict[str, Any]) -> str | None:
    status = tuple_value.get("route_readiness", {}).get(route["id"])
    if status == "READY":
        return None
    if status and status != "PENDING":
        return f"invalid route readiness {status!r}"
    if route.get("availability"):
        return route["missing_input"]
    return None


def dispatch(route: dict[str, Any], tuple_value: dict[str, Any], tuple_path: Path, tuple_sha: str, receipt_path: Path, request_test: Path, runner: Path) -> dict[str, Any]:
    missing = route_missing_input(route, tuple_value)
    if missing:
        raise ValueError(f"{route['id']} is pending: {missing}")
    command = request_argv(route, request_test) if route["kind"] == "request-test" else [sys.executable, str(runner), "--source-tuple", tuple_value["d73_source_tuple"], "--tuple-sha", tuple_value["d73_tuple_sha256"], "core"]
    env = {
        "TIMELINE_FINAL_TUPLE_PATH": str(tuple_path),
        "TIMELINE_FINAL_TUPLE_SHA256": tuple_sha,
        "TIMELINE_FINAL_REPO_SHAS": ",".join(f"{name}={tuple_value['repos'][name]['sha']}" for name in REPOS),
    }
    completed = subprocess.run(command, cwd=tuple_value["repos"]["runtime"]["checkout_path"], env={**os.environ, **env}, text=True, capture_output=True, check=False)
    output = completed.stdout + completed.stderr
    request_match = re.search(r"\bTEST ([^\s/]+)", output)
    result = {"id": route["id"], "request_id": request_match.group(1) if request_match else None, "argv": command, "env": env, "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
    receipt_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("plan", "submit"), default="plan")
    parser.add_argument("--tuple", type=Path, required=True)
    parser.add_argument("--tuple-sha", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--venue", choices=[route["id"] for route in route_table()])
    parser.add_argument("--request-test", type=Path, default=REQUEST_TEST)
    parser.add_argument("--d84-runner", type=Path, default=D84 / "run-final-services.py")
    args = parser.parse_args(argv)
    tuple_path = args.tuple.absolute()
    if args.mode == "plan":
        regular_file(tuple_path, "final tuple")
        actual = sha256(tuple_path)
        try:
            value = json.loads(tuple_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"final tuple is not JSON: {exc}") from exc
        pending = not isinstance(value, dict) or value.get("status") != "READY"
        if not pending:
            value = validate_tuple_data(value, expected_sha=args.tuple_sha, check_git=True)
        routes = [route for route in route_table() if args.venue is None or route["id"] == args.venue]
        result = {"version": 1, "status": "PENDING" if pending else "READY", "tuple_sha256": actual, "tuple_path": str(tuple_path), "inherited": inherited_paths(), "venues": [route_plan(route, tuple_path, args.tuple_sha, args.d84_runner, value if not pending else None) for route in routes], "dispatched": 0, "note": "No request-test or checkout was invoked." if pending else "Plan only; use --mode submit for the captured tuple."}
        args.receipt.absolute().parent.mkdir(parents=True, exist_ok=True)
        args.receipt.absolute().write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if not args.request_test.is_file() or args.request_test.is_symlink():
        raise ValueError(f"request-test is unavailable: {args.request_test}")
    value = load_tuple(tuple_path, args.tuple_sha)
    inherited_paths()
    routes = [route for route in route_table() if args.venue is None or route["id"] == args.venue]
    for route in routes:
        missing = route_missing_input(route, value)
        if missing:
            raise ValueError(f"{route['id']} is pending: {missing}")
    if args.receipt.exists() or args.receipt.is_symlink():
        raise ValueError(f"receipt already exists: {args.receipt}")
    outputs = []
    for route in routes:
        child = args.receipt.absolute().with_name(f"{args.receipt.stem}-{route['id']}.json")
        outputs.append(dispatch(route, value, tuple_path, args.tuple_sha, child, args.request_test, args.d84_runner))
    receipt = {"version": 1, "status": "PASS" if all(item["returncode"] == 0 for item in outputs) else "FAIL", "tuple_sha256": args.tuple_sha, "tuple_path": str(tuple_path), "venues": outputs, "dispatched": len(outputs)}
    args.receipt.absolute().parent.mkdir(parents=True, exist_ok=True)
    args.receipt.absolute().write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"D59 final matrix refused: {exc}", file=sys.stderr)
        raise SystemExit(2)
