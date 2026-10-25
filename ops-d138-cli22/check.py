"""Read-only D138 CLI22 source admission and central-row controls."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
AGENT = Path("/home/user/work/agent")
RUNTIME = Path("/home/user/work/runtime")
APP = Path("/home/user/work/app")
COMPOSITION = Path("/home/user/work/composition")
AGENT_SHA = "cd63be424d62226e3ee5c26fc5ce03227f5394a5"
AGENT_TREE = "e9167d50ce30659772f7ef16912cfea3fd20815c"
AGENT_PARENTS = (
    "cd63be424d62226e3ee5c26fc5ce03227f5394a5 "
    "4c4ee35d5687c4cd40a0e5395efda53aa56f939d "
    "0dbfb4e7f05430f7efbb32226d6260e258ad0a93"
)
RUNTIME_SHA = "f103bb46866999c961a8865636f2e66d544e0c9b"
RUNTIME_TREE = "5d0cedf2e5134acf895e8d43191cc5fdc09f9883"
RUNTIME_PARENTS = (
    "f103bb46866999c961a8865636f2e66d544e0c9b "
    "cf0b82dd47452a7a34fc63eb233e9b1dc0532806 "
    "0bb3bc45cef22bc317398d79e1617da3eb430df2"
)
LOCK_RUNTIME_SHA = "ab1e4f6141987706132916e2da16477f5a019464"
LOCK_RUNTIME_TREE = "7d8e77b2f5a4af79305c9212ce5174d3ea9fd657"
APP_SHA = "5696769dfca056676cde1ab46d8bc94354b3a44a"
APP_TREE = "0748df404125114a0f68b701fa76f43abd3fc79a"
APP_PARENTS = (
    "5696769dfca056676cde1ab46d8bc94354b3a44a "
    "b5c9eadfa1950f46feac50d7d6a89c47f27f4881 "
    "79699d23f0cabef17eaa68463618132556c47902"
)
COMPOSITION_SHA = "635f4de06fda22a85fc2e4cfc764d0153a4c9f40"
COMPOSITION_TREE = "5ab5191a296980a0a6bcd1178ab6902d6478a148"
COMPOSITION_PARENTS = (
    "635f4de06fda22a85fc2e4cfc764d0153a4c9f40 "
    "7a95a40b07ea0d273e17afb69dbc3456b603f2bc "
    "c05fdb171fe37c1d5817a060ecb716a329ee821a"
)
COMPOSITION_TASK_BASE = "afda6c66a11608d8cb012df1a54bf2489d8c20b3"
COMPOSITION_TASK_TREE = "67bd2d4ee1d50bd95ebb8b0de55d4d1ed1e3e87f"
ORIGINS = {
    "agent": "https://github.com/peteromallet/astrid-agent",
    "runtime": "https://github.com/banodoco/banodoco-workspace-runtime",
    "app": "https://github.com/banodoco/reigh-app",
    "composition": "https://github.com/peteromallet/timeline-composition",
}
LAUNCHER = AGENT / "tools/p4-d73-pinned-launch.sh"
TEST_SOURCE = AGENT / "tests/editing_conformance/test_native_batch_ingress.py"
RUNTIME_HELPER = AGENT / "tests/helpers/runtime.py"
SYNC_SOURCE = AGENT / "astrid/sdk/timeline/sync.py"
LOCK = AGENT / "runtime.lock.json"
LAUNCHER_SHA = "9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd"
TEST_SOURCE_SHA = "8bff12b06be10a5b08597dc6c0bf6566b1ffe409f479a6b7d49ac3285dfb845e"
RUNTIME_HELPER_SHA = "4d084450df4d8e9dbdef934bf19ab9d909a8caecdd2646a21b758955e07a883f"
SYNC_SOURCE_SHA = "e0b9aa8815623299aaf24547f0f6bcff9178c2db59ed5cc178a1bdc18a58c254"
LOCK_SHA = "ad818e99cb0759d1742d9f67b5bb3367b03fd3e88d8f65846253169272b8b6ce"
CLIENT_VERSION = "0.2.14"
SCHEMA_DIGEST = "sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b"
PROTOCOL = "workspace.v1"
SCHEMA_ORIGIN = "https://github.com/banodoco/ArtAgents.git@242f9c4306bf3b501222cb041a9eb246ef47bc85#packages/timeline-schema/python"
SUITE = "d138-cli22-current-merged-exact22"
SELECTORS = (
    "tests/editing_conformance/test_native_batch_ingress.py::test_batch_original_claims_one_publication_reload_inverse[cli-False]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_batch_original_claims_one_publication_reload_inverse[cli-True]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-False]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[aba-True]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-False]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[delete-recreate-True]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-False]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[disjoint-True]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-False]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_lost_ack_restart_exact_retry_before_original_suffix[relevant-True]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-False]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[disjoint-True]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-False]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_uses_original_pair_after_peer_advances_head[relevant-True]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[claims]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[empty]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[envelope]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[late-invalid]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_refusal_is_atomic_and_keeps_file[media]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_captured_file_retry_refuses_boolean_to_number_claim[expect]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_captured_file_retry_refuses_boolean_to_number_claim[reads]",
    "tests/editing_conformance/test_native_batch_ingress.py::test_file_preview_keeps_batch_for_one_real_publication",
)
RETIRED_SENTINEL = (
    "tests/editing_conformance/test_native_batch_ingress.py::"
    "test_file_parser_requires_both_original_pins_and_describes_registry"
)
PYTEST = ("-m", "pytest", "-q", "-o", "addopts=", "-m", "integration", "-p", "no:cacheprovider", "--timeout=180")
REQUIRED = """format route agent_sha agent_tree agent_parents agent_path agent_origin runtime_sha runtime_tree runtime_parents runtime_path runtime_origin lock_runtime_sha lock_runtime_tree lock_path lock_sha app_sha app_tree app_parents app_path app_origin composition_sha composition_tree composition_parents composition_path composition_origin python node profile schema schema_origin node_version profile_lock_sha profile_archive_sha profile_registry_sha composition_version client_version schema_digest protocol launcher_path launcher_sha256 test_source_path test_source_sha256 lock_sha256 service_versions junit_paths""".split()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(text: str) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    errors: list[str] = []
    for number, line in enumerate(text.splitlines(), 1):
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
        errors.append("unsupported manifest format: existing launcher accepts p4-d73-v1")
    for key in ("agent_sha", "runtime_sha", "app_sha", "composition_sha", "lock_runtime_sha"):
        if values.get(key) and not re.fullmatch(r"[0-9a-f]{40}", values[key]):
            errors.append(f"invalid {key}")
    for key in ("agent_tree", "runtime_tree", "app_tree", "composition_tree", "lock_runtime_tree"):
        if values.get(key) and not re.fullmatch(r"[0-9a-f]{40}", values[key]):
            errors.append(f"invalid {key}")
    for key in ("profile_lock_sha", "profile_archive_sha", "profile_registry_sha", "launcher_sha256", "test_source_sha256", "lock_sha256"):
        if values.get(key) and not re.fullmatch(r"[0-9a-f]{64}", values[key]):
            errors.append(f"invalid {key}")
    return values, errors


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def git_file(path: Path, revision: str, relative: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "show", f"{revision}:{relative}"], text=True
    )


def checkout_errors(name: str, path: Path, sha: str, tree: str, parents: str) -> list[str]:
    if not path.is_absolute() or path.resolve() != path or not path.is_dir():
        return [f"{name}: missing or noncanonical checkout {path}"]
    try:
        errors = []
        if git(path, "rev-parse", "HEAD") != sha:
            errors.append(f"{name}: commit mismatch")
        if git(path, "rev-parse", "HEAD^{tree}") != tree:
            errors.append(f"{name}: tree mismatch")
        if git(path, "rev-list", "--parents", "-n", "1", "HEAD") != parents:
            errors.append(f"{name}: parent mismatch")
        if git(path, "status", "--porcelain", "--untracked-files=all"):
            errors.append(f"{name}: dirty checkout")
        if git(path, "remote", "get-url", "origin") != ORIGINS[name]:
            errors.append(f"{name}: origin mismatch")
        return errors
    except (OSError, subprocess.CalledProcessError):
        return [f"{name}: git inspection failed"]


def source_errors() -> list[str]:
    errors: list[str] = []
    for name, path, sha, tree, parents in (
        ("agent", AGENT, AGENT_SHA, AGENT_TREE, AGENT_PARENTS),
        ("runtime", RUNTIME, RUNTIME_SHA, RUNTIME_TREE, RUNTIME_PARENTS),
        ("app", APP, APP_SHA, APP_TREE, APP_PARENTS),
        ("composition", COMPOSITION, COMPOSITION_SHA, COMPOSITION_TREE, COMPOSITION_PARENTS),
    ):
        errors.extend(checkout_errors(name, path, sha, tree, parents))
    for path, expected, label in (
        (LAUNCHER, LAUNCHER_SHA, "launcher"),
        (TEST_SOURCE, TEST_SOURCE_SHA, "test source"),
        (RUNTIME_HELPER, RUNTIME_HELPER_SHA, "runtime helper"),
        (SYNC_SOURCE, SYNC_SOURCE_SHA, "TimelineSession source"),
        (LOCK, LOCK_SHA, "runtime lock"),
    ):
        if not path.is_file() or digest(path) != expected:
            errors.append(f"agent: {label} hash mismatch")
    try:
        lock = json.loads(LOCK.read_text())
        if lock.get("source_commit") != LOCK_RUNTIME_SHA:
            errors.append("agent: runtime lock source is not preserved ab1e")
        if lock.get("producer") != "astrid-runtime" or len(lock.get("files", {})) != 15:
            errors.append("agent: runtime lock producer/file count mismatch")
        for relative, entry in lock["files"].items():
            if digest(AGENT / relative) != entry["sha256"].removeprefix("sha256:"):
                errors.append(f"agent: runtime lock file hash mismatch {relative}")
    except (OSError, ValueError, KeyError, TypeError):
        errors.append("agent: runtime lock unreadable")
    try:
        candidate_test = git_file(AGENT, AGENT_SHA, "tests/editing_conformance/test_native_batch_ingress.py")
        tree = ast.parse(candidate_test)
        marker = any(
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets)
            and isinstance(node.value, ast.Attribute)
            and node.value.attr == "integration"
            and isinstance(node.value.value, ast.Attribute)
            and node.value.value.attr == "mark"
            and isinstance(node.value.value.value, ast.Name)
            and node.value.value.value.id == "pytest"
            for node in tree.body
        )
        if not marker:
            errors.append("test source: exact pytestmark=pytest.mark.integration missing")
        names = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        required_names = {selector.split("::", 1)[1].split("[", 1)[0] for selector in SELECTORS}
        if not required_names <= names:
            errors.append("test source: one or more exact22 test functions missing")
        if RETIRED_SENTINEL.split("::", 1)[1] not in names:
            errors.append("test source: retired parser-only sentinel missing from source")
        candidate_lock = json.loads(git_file(AGENT, AGENT_SHA, "runtime.lock.json"))
        if "use_runtime(vendored_runtime_commit())" in candidate_test and candidate_lock.get("source_commit") != RUNTIME_SHA:
            errors.append(
                "test source: use_runtime(vendored_runtime_commit()) selects preserved Agent lock "
                f"{candidate_lock.get('source_commit')}, not manifest Runtime {RUNTIME_SHA}"
            )
    except (OSError, SyntaxError, subprocess.CalledProcessError, ValueError, TypeError):
        errors.append("test source: AST inspection failed")
    try:
        helper = git_file(AGENT, AGENT_SHA, "tests/helpers/runtime.py")
        if 'json.loads(lock.read_text(encoding="utf-8"))["source_commit"]' not in helper:
            errors.append("runtime helper: vendored_runtime_commit source binding changed")
        if "git archive" not in helper or "runtime_checkout(commit" not in helper:
            errors.append("runtime helper: pinned commit does not archive the selected Runtime source")
        sync = git_file(AGENT, AGENT_SHA, "astrid/sdk/timeline/sync.py")
        for field in (
            '"api_version"', '"project_id"', '"timeline_id"', '"base_revision_id"',
            '"base_publication_id"', '"commands"', '"source"', '"dry_run"',
            "commit_options", "idempotency_key",
        ):
            if field not in sync:
                errors.append(f"TimelineSession source: request field guard missing {field}")
        launcher = LAUNCHER.read_text()
        if 'pin["$key"]=${line#*=}' in launcher and "duplicate" not in launcher.lower():
            errors.append("launcher: duplicate manifest keys are silently last-write-wins")
    except (OSError, subprocess.CalledProcessError):
        errors.append("runtime helper or TimelineSession source unreadable")
    return errors


def manifest_errors(values: dict[str, str]) -> list[str]:
    errors: list[str] = []
    fixed = {
        "route": "d138-cli22",
        "agent_path": str(AGENT),
        "agent_sha": AGENT_SHA,
        "agent_tree": AGENT_TREE,
        "agent_parents": AGENT_PARENTS,
        "agent_origin": ORIGINS["agent"],
        "runtime_path": str(RUNTIME),
        "runtime_sha": RUNTIME_SHA,
        "runtime_tree": RUNTIME_TREE,
        "runtime_parents": RUNTIME_PARENTS,
        "runtime_origin": ORIGINS["runtime"],
        "lock_runtime_sha": LOCK_RUNTIME_SHA,
        "lock_runtime_tree": LOCK_RUNTIME_TREE,
        "lock_path": str(LOCK),
        "app_path": str(APP),
        "app_sha": APP_SHA,
        "app_tree": APP_TREE,
        "app_parents": APP_PARENTS,
        "app_origin": ORIGINS["app"],
        "composition_path": str(COMPOSITION),
        "composition_sha": COMPOSITION_SHA,
        "composition_tree": COMPOSITION_TREE,
        "composition_parents": COMPOSITION_PARENTS,
        "composition_origin": ORIGINS["composition"],
        "schema_origin": SCHEMA_ORIGIN,
        "client_version": CLIENT_VERSION,
        "schema_digest": SCHEMA_DIGEST,
        "protocol": PROTOCOL,
        "launcher_path": str(LAUNCHER),
        "launcher_sha256": LAUNCHER_SHA,
        "test_source_path": str(TEST_SOURCE),
        "test_source_sha256": TEST_SOURCE_SHA,
        "lock_sha256": LOCK_SHA,
    }
    for key, expected in fixed.items():
        if values.get(key) != expected:
            errors.append(f"manifest {key}: must bind {expected}")
    if values.get("lock_runtime_sha") and values.get("runtime_sha") and values.get("lock_runtime_sha") == values.get("runtime_sha"):
        errors.append("manifest: normal Runtime must not relabel the preserved Agent lock source")
    for name, path, sha, tree, parents in (
        ("agent", AGENT, AGENT_SHA, AGENT_TREE, AGENT_PARENTS),
        ("runtime", RUNTIME, RUNTIME_SHA, RUNTIME_TREE, RUNTIME_PARENTS),
        ("app", APP, APP_SHA, APP_TREE, APP_PARENTS),
        ("composition", COMPOSITION, COMPOSITION_SHA, COMPOSITION_TREE, COMPOSITION_PARENTS),
    ):
        if values.get(f"{name}_path") == str(path):
            errors.extend(checkout_errors(name, path, sha, tree, parents))
    for key in ("python", "node", "schema", "profile"):
        if values.get(key) and (not Path(values[key]).is_absolute() or not Path(values[key]).exists()):
            errors.append(f"manifest {key}: missing absolute input")
    if values.get("schema"):
        module = Path(values["schema"]) / "banodoco_timeline_schema/__init__.py"
        if not module.is_file():
            errors.append("manifest schema: pinned source/module missing; dependency owner must supply it")
    if values.get("profile"):
        profile = Path(values["profile"])
        if not (profile / "node_modules").is_dir() or (profile / "node_modules").is_symlink():
            errors.append("manifest profile: requires existing nonsymlink node_modules")
        for relative, key in (("package-lock.json", "profile_lock_sha"), (".astrid-registry-state.json", "profile_registry_sha")):
            if not (profile / relative).is_file() or digest(profile / relative) != values.get(key):
                errors.append(f"manifest profile: hash mismatch or missing {relative}")
    return errors


def suite_command() -> str:
    for row in (HERE / "suites.conf").read_text().splitlines():
        fields = row.split(None, 2)
        if fields[:2] == ["agent", SUITE]:
            return fields[2] if len(fields) == 3 else ""
    return ""


def artifact_paths(output: Path) -> dict[str, Path]:
    request_id = output.parent.name
    return {suffix: output / f"{request_id}.{suffix}" for suffix in ("xml", "manifest", "runmanifest", "command", "preflight.log", "preflight.exit", "body.log", "body.exit", "request-id")}


def census(environ: dict[str, str]) -> dict:
    errors = source_errors()
    manifest = environ.get("D138_MANIFEST")
    values, parser_errors = parse_manifest("")
    if manifest and Path(manifest).is_file():
        values, parser_errors = parse_manifest(Path(manifest).read_text())
    else:
        errors.append("D138_MANIFEST: receipt-rendered key=value manifest missing")
    errors.extend(parser_errors)
    errors.extend(manifest_errors(values))
    receiving_needs = [
        f"central agent {SUITE}: row not installed",
        "receipt-rendered D138 manifest with real interpreter/schema/profile/origin inputs",
        "supported launcher seam: p4-d73 launcher requires runtime_sha == Agent lock source ab1e; normal Runtime is f103",
        "fresh central request/snapshot/per-ID XML, launcher logs, body result and submit/end disk witnesses NOTRUN",
        "no actual pytest collection, provider, 22-case body or full-suite evidence is claimed",
    ]
    return {
        "status": "NOT_READY",
        "source_errors": errors,
        "receiving_needs": receiving_needs,
        "source_ready": not errors,
        "body": "NOTRUN",
        "preflight": "NOTRUN",
    }


HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    result = census(dict(os.environ))
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result["source_errors"] else 0)
