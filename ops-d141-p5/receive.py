#!/usr/bin/env python3
"""Validate a normal D66 P5 result and retain its durable witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import route


HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")
REQUIRED_SERVICE = ("exit", "log.txt", "request", "snap", "summary")
REQUIRED_D66 = (
    "d141-p5-cut.xml", "argv.json", "module-origin.json", "source-hashes.json",
    "disk-start", "disk-stop", "runner-exit", "KEEP",
)


def _regular(path: Path, label: str) -> None:
    _parents(path, label)
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} is not a regular file")


def _directory(path: Path, label: str) -> None:
    _parents(path, label)
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        raise ValueError(f"{label} must be an absolute regular directory")


def _parents(path: Path, label: str) -> None:
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must be an absolute path without traversal")
    for parent in reversed(path.parents):
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise ValueError(f"{label} has an unsafe parent")


def _read_int(path: Path, label: str) -> int:
    _regular(path, label)
    value = path.read_text(encoding="utf-8").strip()
    if value not in {str(number) for number in range(256)}:
        raise ValueError(f"{label} is not a numeric byte")
    return int(value)


def _parse_key_file(path: Path, label: str) -> dict[str, str]:
    _regular(path, label)
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition("=")
        if not separator or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key) or key in result:
            raise ValueError(f"{label} is malformed")
        result[key] = value
    return result


def _xml_cases(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    _regular(path, "JUnit")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as error:
        raise ValueError("JUnit is malformed XML") from error
    suites = list(root) if root.tag == "testsuites" else [root]
    if root.tag not in {"testsuite", "testsuites"} or len(suites) != 1 or suites[0].tag != "testsuite":
        raise ValueError("JUnit root is not a testsuite")
    names: list[str] = []
    cases: list[dict[str, str]] = []
    for suite in suites:
        name = suite.attrib.get("name")
        if name != "pytest":
            raise ValueError("JUnit testsuite is not the normal pytest suite")
        names.append(name)
        counts = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
        for case in suite.findall("testcase"):
            test_name = case.attrib.get("name")
            classname = case.attrib.get("classname", "")
            if not test_name or not test_name.strip() or not classname.strip():
                raise ValueError("JUnit testcase has no name")
            if any(child.tag not in {"failure", "error", "skipped", "properties", "system-out", "system-err"} for child in case):
                raise ValueError("JUnit testcase has malformed children")
            outcomes = [child.tag for child in case if child.tag in {"failure", "error", "skipped"}]
            if len(outcomes) > 1:
                raise ValueError("JUnit testcase has contradictory outcomes")
            outcome = "passed"
            if case.find("failure") is not None:
                outcome = "failed"
            elif case.find("error") is not None:
                outcome = "error"
            elif case.find("skipped") is not None:
                outcome = "skipped"
            cases.append({"id": f"{classname}::{test_name}", "outcome": outcome})
            counts["tests"] += 1
            if outcomes:
                counts[{"failure": "failures", "error": "errors", "skipped": "skipped"}[outcomes[0]]] += 1
        if any(suite.attrib.get(key) != str(value) for key, value in counts.items()):
            raise ValueError("JUnit testsuite counts do not match its testcases")
        if any(child.tag not in {"testcase", "properties", "system-out", "system-err"} for child in suite):
            raise ValueError("JUnit testsuite has malformed children")
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("JUnit has no cases or duplicate testcase IDs")
    return names, cases


def _git_identity(root: Path, label: str) -> dict[str, Any]:
    _directory(root, f"{label} checkout")
    if (root / ".git").is_symlink():
        raise ValueError(f"{label} checkout has a symlinked git directory")
    try:
        commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, timeout=10).strip()
        tree = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], text=True, timeout=10).strip()
        dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True, timeout=10).strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise ValueError(f"{label} checkout cannot be inspected") from error
    if not HEX40.fullmatch(commit) or not HEX40.fullmatch(tree) or dirty:
        raise ValueError(f"{label} checkout is not a clean Git source")
    return {"root": str(root), "commit": commit, "tree": tree, "dirty": False}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _parse_json(path: Path, label: str) -> Any:
    _regular(path, label)
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except json.JSONDecodeError as error:
        raise ValueError(f"{label} is malformed JSON") from error


def _source_witnesses(snap: dict[str, str], summary: str, d66: Path) -> dict[str, Any]:
    worktree = Path(snap.get("worktree", ""))
    runtime = _git_identity(worktree, "Runtime")
    if any(runtime[key] != value for key, value in route.EXPECTED_RUNTIME.items()):
        raise ValueError("Runtime source is not the frozen P5 checkout")
    command_lines = [line[5:] for line in summary.splitlines() if line.startswith("cmd: ")]
    if len(command_lines) != 1 or not command_lines[0]:
        raise ValueError("normal service summary has no command provenance")
    command_line = command_lines[0]
    shell_argv = shlex.split(command_line)
    checkouts = [item.split("=", 1)[1] for item in shell_argv if item.startswith("ASTRID_CHECKOUT=")]
    if len(checkouts) != 1 or not checkouts[0]:
        raise ValueError("normal service command has no Agent checkout binding")
    checkout_value = checkouts[0]
    agent = _git_identity(Path(checkout_value), "Agent")
    config = route.load_config()
    if str(worktree) != config["route"]["runtime"]["checkout"]:
        raise ValueError("Runtime source path is not the bound P5 checkout")
    bound_agent = {"checkout": checkout_value, "commit": agent["commit"], "tree": agent["tree"]}
    if command_line != route._command_body(config, bound_agent):
        raise ValueError("normal service command disagrees with the bound P5 row")
    if snap.get("tree") != runtime["tree"]:
        raise ValueError("normal service snapshot tree disagrees with its checkout")
    argv = _parse_json(d66 / "argv.json", "durable argv")
    expected_argv = [config["pytest"]["interpreter"], *route.EXPECTED_ARGS, f"--junitxml={d66}/d141-p5-cut.xml"]
    if argv != expected_argv:
        raise ValueError("durable argv is not the unchanged P5 pytest command")
    origins = _parse_json(d66 / "module-origin.json", "module origins")
    hashes = _parse_json(d66 / "source-hashes.json", "source hashes")
    if not isinstance(origins, dict) or not isinstance(hashes, dict) or not origins:
        raise ValueError("durable provenance witnesses are malformed")
    expected_origins = route._origins(worktree, Path(checkout_value))
    if origins != expected_origins:
        raise ValueError("module origins are not bound to the clean Runtime and Agent checkouts")
    if set(origins.values()) != set(hashes):
        raise ValueError("source origin and hash witnesses disagree")
    for role, raw_path in origins.items():
        if not isinstance(role, str) or not isinstance(raw_path, str) or not raw_path.startswith("/"):
            raise ValueError("module origin is not an absolute path")
        path = Path(raw_path)
        _regular(path, f"source origin {role}")
        digest = hashes[raw_path]
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            raise ValueError(f"source hash for {role} is malformed")
        if _sha256(path) != digest.removeprefix("sha256:"):
            raise ValueError(f"source hash for {role} does not match the checkout")
    return {
        "argv": argv,
        "source": {"runtime": runtime, "agent": agent},
        "origins": origins,
        "hashes": hashes,
        "snapshot_tree": snap["tree"],
    }


def _validate_keep(path: Path) -> None:
    _regular(path, "KEEP witness")
    if path.read_text(encoding="utf-8") != "KEEP before service cleanup\n":
        raise ValueError("KEEP witness is empty or malformed")


def _validate_disk(path: Path) -> None:
    _regular(path, path.name)
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if len(lines) != 2 or lines[0].strip() != "Avail" or not re.fullmatch(r"[0-9]+", lines[1].strip()):
        raise ValueError(f"disk witness {path.name} is malformed")


def receive(output: Path, receipt: Path) -> None:
    _directory(output, "service output")
    missing = [name for name in REQUIRED_SERVICE if not (output / name).is_file()]
    if missing:
        raise ValueError("missing normal service artifacts: " + ", ".join(missing))
    for name in REQUIRED_SERVICE:
        _regular(output / name, f"normal service {name}")
    if not (output / "log.txt").read_text(encoding="utf-8").strip():
        raise ValueError("normal service log is empty")
    d66 = output / "d66"
    _directory(d66, "D66 output")
    missing = [name for name in REQUIRED_D66 if not (d66 / name).is_file()]
    if missing:
        raise ValueError("missing D66 witnesses: " + ", ".join(missing))
    for name in REQUIRED_D66:
        _regular(d66 / name, f"D66 witness {name}")
    runner_exit = _read_int(output / "exit", "raw service runner exit")
    wrapped_exit = _read_int(d66 / "runner-exit", "raw pytest runner exit")
    if runner_exit != wrapped_exit:
        raise ValueError("service exit and raw pytest exit disagree")
    suite_names, cases = _xml_cases(d66 / "d141-p5-cut.xml")
    failed = any(case["outcome"] in {"failed", "error"} for case in cases)
    if (runner_exit == 0 and failed) or (runner_exit == 1 and not failed):
        raise ValueError("JUnit outcomes and raw pytest exit disagree")
    request = _parse_key_file(output / "request", "normal service request")
    if request.get("repo") != "runtime" or request.get("suite") != "d141-p5-cut":
        raise ValueError("normal service request is not the named D141 P5 route")
    snap = _parse_key_file(output / "snap", "normal service snapshot")
    if not HEX40.fullmatch(snap.get("tree", "")):
        raise ValueError("normal service snapshot has no valid tree")
    provenance = _source_witnesses(snap, (output / "summary").read_text(encoding="utf-8"), d66)
    _validate_keep(d66 / "KEEP")
    _validate_disk(d66 / "disk-start")
    _validate_disk(d66 / "disk-stop")
    _parents(receipt, "receipt destination")
    if receipt.exists() or receipt.is_symlink():
        raise ValueError("receipt destination already exists")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({
        "output": str(output),
        "runner_exit": runner_exit,
        "suite": suite_names,
        "testcases": cases,
        "provenance": provenance,
        "keep": str(d66 / "KEEP"),
    }, indent=2, sort_keys=True) + "\n"
    try:
        with receipt.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    except FileExistsError as error:
        raise ValueError("receipt destination already exists") from error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receive(args.output, args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
