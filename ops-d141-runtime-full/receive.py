#!/usr/bin/env python3
"""Validate the existing normal test-service result and retain its witnesses."""

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


HEX40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_SERVICE = ("exit", "log.txt", "request", "snap", "summary")
REQUIRED_D66 = ("runtime-full.xml", "disk-start", "disk-stop", "runner-exit", "KEEP")


def _regular(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} is not a regular file")


def _directory(path: Path, label: str) -> None:
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        raise ValueError(f"{label} must be an absolute regular directory")


def _read_int(path: Path, label: str) -> int:
    _regular(path, label)
    value = path.read_text(encoding="utf-8").strip()
    if not value.isdigit() or not 0 <= int(value) <= 255:
        raise ValueError(f"{label} is not a numeric byte")
    return int(value)


def _parse_key_file(path: Path, label: str) -> dict[str, str]:
    _regular(path, label)
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition("=")
        if not separator or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError(f"{label} is malformed")
        if key in result:
            raise ValueError(f"{label} contains duplicate keys")
        result[key] = value
    return result


def _xml_cases(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    _regular(path, "JUnit")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as error:
        raise ValueError("JUnit is malformed XML") from error
    suites = list(root.iter("testsuite")) if root.tag == "testsuites" else [root]
    if root.tag not in {"testsuite", "testsuites"} or not suites:
        raise ValueError("JUnit root is not a testsuite")
    suite_names: list[str] = []
    cases: list[dict[str, str]] = []
    for suite in suites:
        name = suite.attrib.get("name")
        if not name:
            raise ValueError("JUnit testsuite has no name")
        suite_names.append(name)
        for case in suite.findall("testcase"):
            classname = case.attrib.get("classname", "")
            test_name = case.attrib.get("name")
            if not test_name:
                raise ValueError("JUnit testcase has no name")
            outcome = "passed"
            if case.find("failure") is not None:
                outcome = "failed"
            elif case.find("error") is not None:
                outcome = "error"
            elif case.find("skipped") is not None:
                outcome = "skipped"
            cases.append({"id": f"{classname}::{test_name}", "outcome": outcome})
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("JUnit has no cases or duplicate testcase IDs")
    declared = sum(int(suite.attrib.get("tests", "-1")) for suite in suites)
    if declared != len(cases):
        raise ValueError("JUnit testsuite count does not match its testcases")
    return suite_names, cases


def _git_identity(root: Path, label: str) -> dict[str, Any]:
    _directory(root, f"{label} checkout")
    if (root / ".git").is_symlink():
        raise ValueError(f"{label} checkout has a symlinked git directory")
    try:
        commit = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True, timeout=10
        ).strip()
        tree = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], text=True, timeout=10
        ).strip()
        dirty = subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain"], text=True, timeout=10
        ).strip()
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


def _source_witnesses(snap: dict[str, str], summary: str) -> dict[str, Any]:
    worktree = Path(snap.get("worktree", ""))
    runtime = _git_identity(worktree, "Runtime")
    command_line = next(
        (line[5:] for line in summary.splitlines() if line.startswith("cmd: ")), None
    )
    if not command_line:
        raise ValueError("normal service summary has no command provenance")
    argv = shlex.split(command_line)
    if "-m" not in argv or "pytest" not in argv or "-q" not in argv or "-n3" not in argv:
        raise ValueError("normal service command is not the unchanged full pytest command")
    command_text = " ".join(argv)
    if any(
        witness not in command_text
        for witness in ("disk-start", "disk-stop", "runner-exit", "KEEP")
    ):
        raise ValueError("normal service command does not produce all D66 witnesses")
    if not any(
        token.startswith("--junitxml=$D66_OUTPUT_DIR/runtime-full.xml") for token in argv
    ):
        raise ValueError("normal service command does not retain the D66 JUnit path")
    checkout_value = next(
        (item.split("=", 1)[1] for item in argv if item.startswith("ASTRID_CHECKOUT=")), None
    )
    if not checkout_value:
        raise ValueError("normal service command has no Agent checkout binding")
    agent = _git_identity(Path(checkout_value), "Agent")
    if snap.get("tree") != runtime["tree"]:
        raise ValueError("normal service snapshot tree disagrees with its checkout")
    origins: dict[str, str] = {}
    hashes: dict[str, str] = {}
    candidates = {
        "runtime_protocol": worktree / "runtime_protocol" / "__init__.py",
        "runtime_metadata": worktree / "runtime_protocol" / "contract_metadata.py",
        "runtime_contract": worktree / "contract" / "artifacts.json",
        "agent_provider": Path(checkout_value) / "astrid" / "__init__.py",
        "agent_client": Path(checkout_value) / "astrid_runtime_client" / "generated.py",
        "agent_metadata": Path(checkout_value)
        / "astrid_runtime_client"
        / "contract_metadata.py",
    }
    for name, path in candidates.items():
        _regular(path, f"source origin {name}")
        origins[name] = str(path)
        hashes[str(path)] = _sha256(path)
    return {
        "argv": argv,
        "source": {"runtime": runtime, "agent": agent},
        "origins": origins,
        "hashes": hashes,
        "snapshot_tree": snap["tree"],
    }


def _validate_keep(path: Path) -> None:
    _regular(path, "KEEP witness")
    if not path.read_text(encoding="utf-8").strip():
        raise ValueError("KEEP witness is empty")


def receive(output: Path, receipt: Path) -> None:
    _directory(output, "service output")
    missing = [name for name in REQUIRED_SERVICE if not (output / name).is_file()]
    if missing:
        raise ValueError("missing normal service artifacts: " + ", ".join(missing))
    d66 = output / "d66" if (output / "d66").exists() else output
    _directory(d66, "D66 output")
    missing = [name for name in REQUIRED_D66 if not (d66 / name).is_file()]
    if missing:
        raise ValueError("missing D66 witnesses: " + ", ".join(missing))
    runner_exit = _read_int(output / "exit", "raw service runner exit")
    wrapped_exit = _read_int(d66 / "runner-exit", "raw pytest runner exit")
    if runner_exit != wrapped_exit:
        raise ValueError("service exit and raw pytest exit disagree")
    suite_names, cases = _xml_cases(d66 / "runtime-full.xml")
    request = _parse_key_file(output / "request", "normal service request")
    if request.get("repo") != "runtime" or request.get("suite") not in {
        "full-d141-cut",
        "full-d141-pristine",
    }:
        raise ValueError("normal service request is not a named D141 full route")
    snap = _parse_key_file(output / "snap", "normal service snapshot")
    if not HEX40.fullmatch(snap.get("tree", "")):
        raise ValueError("normal service snapshot has no valid tree")
    summary = (output / "summary").read_text(encoding="utf-8")
    provenance = _source_witnesses(snap, summary)
    _validate_keep(d66 / "KEEP")
    for witness in (d66 / "disk-start", d66 / "disk-stop"):
        value = witness.read_text(encoding="utf-8").strip().splitlines()
        if len(value) != 2 or not value[1].strip().isdigit():
            raise ValueError(f"disk witness {witness.name} is malformed")
    if receipt.exists() or receipt.is_symlink():
        raise ValueError("receipt destination already exists")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(
        json.dumps(
            {
                "output": str(output),
                "runner_exit": runner_exit,
                "suite": suite_names,
                "testcases": cases,
                "provenance": provenance,
                "keep": str(d66 / "KEEP"),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receive(args.output, args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
