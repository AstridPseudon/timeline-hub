"""Read-only D73 own-node source admission; never runs a product preflight."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
AGENT = Path("/home/user/work/wt/agt-pin-2eca9a1d")
AGENT_SHA = "2eca9a1da94eb35bb969540e150192ff920ce326"
AGENT_TREE = "888c16e3dbbff2d6827e7ffcfea64208b0e2a5e4"
RUNTIME = Path("/home/user/work/wt/rt-pin-ab1e4f61")
RUNTIME_SHA = "ab1e4f6141987706132916e2da16477f5a019464"
RUNTIME_TREE = "7d8e77b2f5a4af79305c9212ce5174d3ea9fd657"
HASHES = {
    "tools/p4-d73-pinned-launch.sh": "9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd",
    "tests/sdk/test_timeline_selected_schema_runtime.py": "8243f3b9fe71b218b3b6a402c10d099e15c848b91b82770383e91a2dd3a72b86",
    "tests/editing_conformance/test_occurrence_fork_source_baseline.py": "3fef15b5862e044942f2d0164b37f6f9281f86d378345d8a0b262c64870af8a4",
    "tests/sdk/test_p4_d73_pinned_launcher.py": "0c2c70bd5e26598beebd31f4c7a0a3c1bf48bdc5e9f32ff93c6b54bf15b4b600",
}
ORIGINS = {
    "agent": "https://github.com/peteromallet/astrid-agent",
    "runtime": "https://github.com/banodoco/banodoco-workspace-runtime",
    "app": "https://github.com/banodoco/reigh-app",
    "composition": "https://github.com/peteromallet/timeline-composition",
}
REQUIRED = (
    "format agent_sha agent_tree agent_parents agent_path runtime_sha runtime_tree runtime_path "
    "app_sha app_tree app_path composition_sha composition_tree composition_path python node "
    "profile schema node_version profile_lock_sha profile_archive_sha profile_registry_sha "
    "composition_version original_p4_test_hash service_versions junit_paths"
).split()
SELECTED = (
    "tests/sdk/test_timeline_selected_schema_runtime.py::"
    "test_native_rebase_after_v2_and_selection_removal_uses_original_object",
    "tests/sdk/test_timeline_selected_schema_runtime.py::"
    "test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin]",
    "tests/sdk/test_timeline_selected_schema_runtime.py::"
    "test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element]",
    "tests/sdk/test_timeline_selected_schema_runtime.py::"
    "test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart",
)
FORK = (
    "tests/editing_conformance/test_occurrence_fork_source_baseline.py::"
    "test_current_runtime_retained_fork_then_emitter",
)
PYTEST = (
    "-m",
    "pytest",
    "-q",
    "-o",
    "addopts=",
    "-m",
    "integration",
    "-p",
    "no:cacheprovider",
    "--timeout=45",
)
SUITES = ("d73-ab1e-selected4-exact-nodes", "d73-ab1e-fork-exact-nodes")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(text: str) -> tuple[dict[str, str], list[str]]:
    # The launcher splits on the first '=' and does not source/eval the values.
    values: dict[str, str] = {}
    errors = []
    for number, line in enumerate(text.split("\n"), 1):
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            errors.append(f"manifest line {number}: malformed key=value")
        elif key in values:
            errors.append(f"manifest line {number}: duplicate {key}")
        else:
            values[key] = value
    errors.extend(f"manifest missing {key}" for key in REQUIRED if not values.get(key))
    if values.get("format") and values["format"] != "p4-d73-v1":
        errors.append("unsupported manifest format")
    for repo in ORIGINS:
        for suffix in ("sha", "tree"):
            key = f"{repo}_{suffix}"
            if values.get(key) and not re.fullmatch(r"[0-9a-f]{40}", values[key]):
                errors.append(f"invalid {key}")
    for key in (
        "profile_lock_sha",
        "profile_archive_sha",
        "profile_registry_sha",
        "original_p4_test_hash",
    ):
        if values.get(key) and not re.fullmatch(r"[0-9a-f]{64}", values[key]):
            errors.append(f"invalid {key}")
    return values, errors


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def checkout_errors(
    repo: str, path: Path, sha: str, tree: str, parents: str | None = None
) -> list[str]:
    errors = []
    if not path.is_absolute() or path.resolve() != path or not path.is_dir():
        return [f"{repo}: missing or noncanonical checkout {path}"]
    try:
        if git(path, "rev-parse", "HEAD") != sha:
            errors.append(f"{repo}: commit mismatch")
        if git(path, "rev-parse", "HEAD^{tree}") != tree:
            errors.append(f"{repo}: tree mismatch")
        if git(path, "status", "--porcelain", "--untracked-files=all"):
            errors.append(f"{repo}: dirty checkout")
        if git(path, "remote", "get-url", "origin") != ORIGINS[repo]:
            errors.append(f"{repo}: origin mismatch")
        if parents is not None and git(path, "rev-list", "--parents", "-n", "1", "HEAD") != parents:
            errors.append(f"{repo}: parent mismatch")
    except subprocess.CalledProcessError:
        errors.append(f"{repo}: git inspection failed")
    return errors


def agent_errors() -> list[str]:
    errors = checkout_errors("agent", AGENT, AGENT_SHA, AGENT_TREE)
    for relative, expected in HASHES.items():
        path = AGENT / relative
        if not path.is_file() or digest(path) != expected:
            errors.append(f"agent: reviewed source hash mismatch: {relative}")
    syntax = subprocess.run(
        ["bash", "-n", str(AGENT / "tools/p4-d73-pinned-launch.sh")], capture_output=True, text=True
    )
    if syntax.returncode:
        errors.append("agent: launcher shell syntax failed")
    return errors


def receipt_errors(repo: str, sha: str, path: Path) -> list[str]:
    receipt = ORCH / f"queue/done/checkout-{repo}-{sha}"
    expected = f"created {path} (detached at {sha}, KEEP)"
    if not receipt.is_file() or receipt.read_text().strip() != expected:
        return [f"{repo}: missing matching checkout receipt {receipt}"]
    return []


def manifest_errors(values: dict[str, str]) -> list[str]:
    errors = []
    fixed = {
        "agent_path": str(AGENT),
        "agent_sha": AGENT_SHA,
        "agent_tree": AGENT_TREE,
        "runtime_path": str(RUNTIME),
        "runtime_sha": RUNTIME_SHA,
        "runtime_tree": RUNTIME_TREE,
    }
    for key, expected in fixed.items():
        if values.get(key) != expected:
            errors.append(f"manifest {key}: must bind own-node receipt {expected}")
    for repo in ORIGINS:
        if all(values.get(f"{repo}_{key}") for key in ("path", "sha", "tree")):
            errors.extend(
                checkout_errors(
                    repo,
                    Path(values[f"{repo}_path"]),
                    values[f"{repo}_sha"],
                    values[f"{repo}_tree"],
                    values.get(f"{repo}_parents"),
                )
            )
            if repo in ("app", "composition"):
                errors.extend(
                    receipt_errors(repo, values[f"{repo}_sha"], Path(values[f"{repo}_path"]))
                )
        elif repo in ("app", "composition"):
            errors.append(f"{repo}: checkout receipt binding missing without manifest identity")
    if values.get("original_p4_test_hash"):
        originals = [
            AGENT / f"tests/editing_conformance/{name}.py"
            for name in (
                "test_p4_cli_sheet_v2_runtime",
                "test_p4_ten_note_v2_runtime",
                "test_p4_note_rerun_v2_runtime",
            )
        ]
        if not all(path.is_file() for path in originals):
            errors.append("agent: original P4 source missing")
        else:
            combined = subprocess.check_output(["sha256sum", *map(str, originals)])
            if hashlib.sha256(combined).hexdigest() != values["original_p4_test_hash"]:
                errors.append("manifest: original P4 source hash mismatch")
    for key in ("python", "node", "schema", "profile"):
        if not values.get(key):
            continue
        path = Path(values[key])
        if not path.is_absolute() or not path.exists():
            errors.append(f"manifest {key}: missing absolute input {path}")
        elif key in ("python", "node") and (not path.is_file() or not os.access(path, os.X_OK)):
            errors.append(f"manifest {key}: not executable {path}")
    if values.get("schema"):
        module = Path(values["schema"]) / "banodoco_timeline_schema/__init__.py"
        if not module.is_file():
            errors.append(f"schema: pinned source missing {module}; D139 owns dependency recipe")
    if values.get("profile"):
        profile = Path(values["profile"])
        modules = profile / "node_modules"
        if not modules.is_dir() or modules.is_symlink():
            errors.append("profile: requires existing nonsymlink node_modules")
        for relative, key in (
            ("package-lock.json", "profile_lock_sha"),
            (".astrid-registry-state.json", "profile_registry_sha"),
        ):
            path = profile / relative
            if not path.is_file() or digest(path) != values.get(key):
                errors.append(f"profile: hash mismatch or missing {relative}")
        try:
            package = json.loads((profile / "package.json").read_text())
            archive = profile / package["dependencies"][
                "@banodoco/timeline-composition"
            ].removeprefix("file:")
            if not archive.is_file() or digest(archive) != values.get("profile_archive_sha"):
                errors.append("profile: composition archive hash mismatch or missing")
            installed = json.loads(
                (modules / "@banodoco/timeline-composition/package.json").read_text()
            )
            if installed["version"] != values.get("composition_version"):
                errors.append("profile: composition version mismatch")
        except (OSError, ValueError, KeyError, TypeError):
            errors.append("profile: package/archive/version inputs unreadable")
    return errors


def census(environ: dict[str, str]) -> dict:
    errors = agent_errors()
    errors.extend(checkout_errors("runtime", RUNTIME, RUNTIME_SHA, RUNTIME_TREE))
    for repo, sha, path in (("agent", AGENT_SHA, AGENT), ("runtime", RUNTIME_SHA, RUNTIME)):
        errors.extend(receipt_errors(repo, sha, path))
    try:
        lock = json.loads((AGENT / "runtime.lock.json").read_text())
        if (
            lock["source_commit"] != RUNTIME_SHA
            or lock["producer"] != "astrid-runtime"
            or len(lock["files"]) != 15
        ):
            errors.append("agent: runtime lock tuple/producer/count mismatch")
        for relative, entry in lock["files"].items():
            path = AGENT / relative
            if not path.is_file() or digest(path) != entry["sha256"].removeprefix("sha256:"):
                errors.append(f"agent: runtime lock hash mismatch {relative}")
    except (OSError, ValueError, KeyError, TypeError):
        errors.append("agent: unreadable runtime lock")
    manifest = environ.get("D73_MANIFEST")
    values, parser_errors = parse_manifest("")
    if manifest and Path(manifest).is_file():
        values, parser_errors = parse_manifest(Path(manifest).read_text())
    else:
        errors.append("D73_MANIFEST: receipt-rendered key=value manifest missing")
    errors.extend(parser_errors)
    errors.extend(manifest_errors(values))
    rows = (ORCH / "tests/suites.conf").read_text().splitlines()
    receiving_needs = [
        f"central agent {suite}: row not installed"
        for suite in SUITES
        if not any(row.split()[:2] == ["agent", suite] for row in rows)
    ]
    receiving_needs.extend(
        [
            "selected4: fresh central per-ID XML/raw logs/submit and end disk witnesses NOTRUN",
            "fork: fresh central per-ID XML/raw logs/submit and end disk witnesses NOTRUN",
            "manifest interpreter/schema: genuine import/distribution readiness unqualified here; "
            "D139 owns dependency recipe, no Main-only schema overlay permitted",
        ]
    )
    return {
        "status": "NOT_READY",
        "source_errors": errors,
        "receiving_needs": receiving_needs,
        "source_ready": not errors,
        "body": "NOTRUN",
        "preflight": "NOTRUN",
    }


if __name__ == "__main__":
    result = census(dict(os.environ))
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result["source_errors"] else 0)
