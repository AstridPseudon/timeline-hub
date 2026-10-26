#!/usr/bin/env python3
"""Author/reviewer shared source-only check for F D141l command return."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_STUB = "38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0"
TUPLE = {
    "/home/user/work/agent": ("8585ed9c0404d0187b2ce70242d25114a32747c2", "92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c"),
    "/home/user/work/runtime": ("6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d", "ac5b862744bece65b2e30565db1777bacd60da28"),
    "/home/user/work/composition": ("635f4de06fda22a85fc2e4cfc764d0153a4c9f40", "5ab5191a296980a0a6bcd1178ab6902d6478a148"),
    "/home/user/work/wt/agt-pin-64197afa": ("64197afa297f86f1e738238d5e80aff6d33e303a", "6c0488b3efdfa47479b0ad1b7bd20608383be26e"),
    "/home/user/work/wt/rt-pin-fa9cd546": ("fa9cd5464a8b37b02f971de375e56be846cd69e2", "124e10dbcd54fb90219e783ec11aa34f8c91590c"),
}
errors: list[str] = []

def need(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_json(name: str):
    path = ROOT / name
    try:
        return json.loads(path.read_bytes())
    except Exception as exc:
        errors.append(f"{name}: JSON parse failed: {exc}")
        return {}

def git_guard(path: str, sha: str, tree: str) -> None:
    # The command itself performs the live exact-path/clean guard. This shared
    # source-only checker must remain stable when a manager advances an
    # integration worktree after this packet; it verifies the frozen objects
    # without checking out or mutating any ref.
    commit = subprocess.run(["git", "-C", path, "cat-file", "-e", sha + "^{commit}"], text=True, capture_output=True)
    actual_tree = subprocess.run(["git", "-C", path, "rev-parse", sha + "^{tree}"], text=True, capture_output=True)
    need(commit.returncode == 0, f"{path}: frozen SHA object is absent")
    need(actual_tree.returncode == 0 and actual_tree.stdout.strip() == tree, f"{path}: frozen tree object mismatch")

for command in (ROOT / "command-cut.sh", ROOT / "command-pristine.sh", ROOT / "positive-stub.sh"):
    result = subprocess.run(["bash", "-n", str(command)], text=True, capture_output=True)
    need(result.returncode == 0, f"{command.name}: bash -n failed: {result.stderr}")

for name in ("controls.json", "admission-derivation.json", "source-manifest.json", "readiness.json"):
    load_json(name)

source = load_json("source-manifest.json")
derivation = load_json("admission-derivation.json")
controls = load_json("controls.json")
readiness = load_json("readiness.json")
need(digest(ROOT / "positive-stub.sh") == EXPECTED_STUB, "positive-stub SHA changed")
positive = (ROOT / "positive.manifest").read_text()
poison = (ROOT / "poison.manifest").read_text()
def manifest_map(text: str) -> dict[str, str]:
    return dict(line.split("=", 1) for line in text.splitlines() if "=" in line)
pmap = manifest_map(positive)
qmap = manifest_map(poison)
need(set(pmap) == set(qmap), "positive/poison manifest key sets differ")
need([key for key in pmap if pmap[key] != qmap[key]] == ["agent_sha"], "poison differs by more than agent_sha")
need(pmap.get("app_sha") == source["app_owner_receipt"]["sha"], "manifest App SHA is not the actual owner receipt")
need("APP_FREEZE2_SHA_RECEIPT_REQUIRED" not in positive + poison + (ROOT / "command-cut.sh").read_text(), "App sentinel remains")
need(source["pristine"]["agent"]["sha"].endswith("303a"), "authoritative pristine SHA is not 303a")
need(source["selection"]["cut_roots"] == 22 and source["selection"]["pristine_roots"] == 17, "resolved selection counts changed")
need(derivation["derivation"]["x_bytes"] == 514564096 and derivation["derivation"]["floor_bytes"] == 4714564096, "D89d arithmetic changed")
need(controls["custody"]["continuous_interval_seconds"] == 5, "continuous interval is not five seconds")
need(controls["custody"]["continuous_stop_bytes"] == 4000000000, "continuous stop floor changed")
need(readiness["status"] == "NOT_READY_RECEIVING", "future receiving was incorrectly claimed ready")
need("303e" in source["provenance_correction"]["original0500_claim"], "new 303e correction is missing")
need("F009" in (ROOT / "validation.md").read_text(), "F009 disclosure missing")
need("substring" in (ROOT / "handoff.md").read_text() or "substring" in (ROOT / "validation.md").read_text(), "substring policy is not disclosed")

for path, (sha, tree) in TUPLE.items():
    git_guard(path, sha, tree)

cut = (ROOT / "command-cut.sh").read_text()
pristine = (ROOT / "command-pristine.sh").read_text()
for text, label in ((cut, "cut"), (pristine, "pristine")):
    for token in ("4714564096", "4000000000", "source-before", "source-after", "custody", "flock", "monitor_disk", "sleep 5", "raw-stdout", "raw-stderr", "junit", "manager_dispatch_witness", "manifest_sha256", "brief_sha256", "request_id"):
        need(token.lower() in text.lower(), f"{label}: required control token missing: {token}")
    need("-n3" in text and "addopts=" in text and "no:cacheprovider" in text and "--timeout=45" in text, f"{label}: pytest settings changed")
need("p4-d73-pinned-launch.sh" in cut, "cut no longer uses production launcher")
need("p4-d73-pinned-launch.sh" not in pristine, "pristine unexpectedly uses D73 launcher")
need("positive.manifest" not in pristine and "poison.manifest" not in pristine, "pristine uses manifest controls")
need("17-root-selector" not in pristine and "22-root-selector" not in cut, "placeholder selector remains")
roots = re.findall(r"^\s+tests/[A-Za-z0-9_./-]+$", pristine, re.MULTILINE)
need(len(roots) == 17, f"pristine root count is {len(roots)}, expected 17")

for xml in ROOT.glob("private/**/*.xml"):
    try:
        ET.parse(xml)
    except ET.ParseError as exc:
        errors.append(f"{xml}: XML parse failed: {exc}")

if errors:
    print("FAIL")
    for error in errors:
        print(error)
    raise SystemExit(1)
print("PASS")
print("bash-n, stdlib JSON/hash/XML, read-only Git tuple guards, selection, arithmetic, custody, receipt-binding tokens: PASS")

