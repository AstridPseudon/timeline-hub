#!/usr/bin/env python3
"""Submit one Timeline gate request against one captured four-repository tuple.

This is a private D73 handoff. It captures the integration SHAs once, queues the
existing exact-checkout requests, waits for their receipts, then invokes the
installed request-test syntax. It never looks up a current home after capture.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any

REPOS = ("agent", "runtime", "app", "composition")
ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
DEFAULT_CHECKOUT = ORCH / "bin/request-checkout"
DEFAULT_TEST = ORCH / "bin/request-test"
CHECKOUT_LINE = re.compile(
    r"^created (?P<path>/\S+) \(detached at (?P<sha>[0-9a-f]{40}), KEEP\)$"
)


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_path(path: Path, label: str) -> Path:
    path = path.absolute()
    if path.is_symlink() or not path.exists():
        raise ValueError(f"{label} must exist and not be a symlink: {path}")
    return path


def capture_once(work_root: Path) -> dict[str, dict[str, str]]:
    captured: dict[str, dict[str, str]] = {}
    for name in REPOS:
        root = work_root / name
        if git(root, "status", "--porcelain"):
            raise ValueError(f"{name} home is dirty at capture")
        sha = git(root, "rev-parse", "tl/integration^{commit}")
        tree = git(root, "rev-parse", "tl/integration^{tree}")
        captured[name] = {"root": str(root), "sha": sha, "tree": tree}
    return captured


def await_receipt(done: Path, repo: str, sha: str, tree: str, timeout: float) -> tuple[Path, str]:
    receipt = done / f"checkout-{repo}-{sha}"
    deadline = time.monotonic() + timeout
    while not receipt.is_file():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"checkout receipt did not arrive: {receipt}")
        time.sleep(0.1)
    raw = receipt.read_text(encoding="utf-8").strip()
    match = CHECKOUT_LINE.fullmatch(raw)
    if match is None or match.group("sha") != sha:
        raise ValueError(f"invalid checkout receipt for {repo}: {raw!r}")
    path = Path(match.group("path"))
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        raise ValueError(f"checkout receipt path is not a real directory: {path}")
    if git(path, "rev-parse", "HEAD") != sha:
        raise ValueError(f"selected {repo} checkout moved from captured SHA")
    if git(path, "rev-parse", "HEAD^{tree}") != tree:
        raise ValueError(f"selected {repo} checkout tree drifted")
    if git(path, "status", "--porcelain"):
        raise ValueError(f"selected {repo} checkout is dirty")
    return path, raw


def write_tuple(path: Path, entries: dict[str, dict[str, str]]) -> str:
    payload = {name: entries[name] for name in REPOS}
    path = regular_path(path.parent, "tuple parent") / path.name
    if path.exists() or path.is_symlink():
        raise ValueError(f"tuple output already exists: {path}")
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return digest(path)


def submit(args: argparse.Namespace) -> int:
    work_root = regular_path(Path(args.work_root), "work root")
    checkout = regular_path(Path(args.request_checkout), "request-checkout")
    request_test = regular_path(Path(args.request_test), "request-test")
    done = regular_path(Path(args.done_root), "checkout receipt directory")
    receipt_out = Path(args.receipt).absolute()
    if receipt_out.exists() or receipt_out.is_symlink():
        raise ValueError(f"submit receipt already exists: {receipt_out}")

    captured = capture_once(work_root)
    events: list[dict[str, Any]] = [{"event": "capture", "repos": captured}]
    selected: dict[str, dict[str, str]] = {}
    for name in REPOS:
        sha = captured[name]["sha"]
        subprocess.run(
            [str(checkout), name, sha, args.reason],
            check=True,
            text=True,
        )
        events.append({"event": "request-checkout", "repo": name, "sha": sha})
        selected_root, raw = await_receipt(
            done, name, sha, captured[name]["tree"], args.checkout_timeout
        )
        selected[name] = {
            "root": str(selected_root),
            "sha": sha,
            "tree": captured[name]["tree"],
        }
        events.append({
            "event": "checkout-receipt",
            "repo": name,
            "sha": sha,
            "path": str(selected_root),
            "receipt": raw,
        })

    tuple_sha = write_tuple(Path(args.tuple), selected)
    events.append({"event": "tuple", "path": str(Path(args.tuple).absolute()), "sha256": tuple_sha})

    command = [str(request_test), args.target, args.suite]
    if args.files:
        command.extend(["--files", args.files])
    if args.no_cache:
        command.append("--no-cache")
    events.append({"event": "request-test", "argv": command})
    receipt_out.parent.mkdir(parents=True, exist_ok=True)
    receipt_out.write_text(json.dumps({
        "version": 1,
        "status": "submitted",
        "tuple_sha256": tuple_sha,
        "tuple": selected,
        "events": events,
        "request_test": command,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    completed = subprocess.run(command, check=False, text=True, capture_output=True)
    sys.stdout.write(completed.stdout)
    sys.stderr.write(completed.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    print(f"D73 submitted after four checkout receipts: {tuple_sha}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root", default="/home/user/work")
    parser.add_argument("--request-checkout", default=str(DEFAULT_CHECKOUT))
    parser.add_argument("--request-test", default=str(DEFAULT_TEST))
    parser.add_argument("--done-root", default=str(ORCH / "queue/done"))
    parser.add_argument("--tuple", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--suite", required=True)
    parser.add_argument("--files")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--reason", default="D73 exact four-repository gate tuple")
    parser.add_argument("--checkout-timeout", type=float, default=300.0)
    return submit(parser.parse_args())


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError, TimeoutError, ValueError) as exc:
        print(f"D73 submit refused: {exc}", file=sys.stderr)
        raise SystemExit(2)

