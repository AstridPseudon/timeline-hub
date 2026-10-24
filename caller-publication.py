"""Prepare the final integrated Timeline caller without executing it.

This is a bounded preparation artifact.  It authenticates the current App,
Agent, and Runtime checkouts, reads the installed P2/P3 rows as templates,
rebinds their source and target guards to those authenticated identities, and
syntax-checks the decoded and wrapped candidates.  It never starts a service,
allocates a port, opens HTTP, launches a browser, installs a package, or
submits a request.  Final child, backend, Remotion, graph, and coordinator
receipts are custody inputs and the absence of any of them keeps the result
PREPARED rather than READY.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
from typing import Any


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
SUITES = ORCH / "tests/suites.conf"
ARTIFACT = Path(__file__).resolve().parent
APP = Path(os.environ.get("TIMELINE_APP_CHECKOUT", "/home/user/work/app"))
AGENT = Path(os.environ.get("TIMELINE_AGENT_CHECKOUT", "/home/user/work/agent"))
RUNTIME = Path(os.environ.get("TIMELINE_RUNTIME_CHECKOUT", "/home/user/work/runtime"))

APP_COMMIT = "cca3deb361e8fbbc62ddf491d5fd09c7e542b99f"
APP_TREE = "911956d49c42021f11d21e9cf69e9e9478ab569a"
APP_PARENTS = (
    "d99396bca7c3853435cfa5a5991f5b1073187be4",
    "8a712d39c74e92ff10886007ae5135d4f316e92e",
)
AGENT_COMMIT = "cba425b61958f380f25b7bdea83d23c92f627761"
AGENT_TREE = "d19ce2e55ce9f29e18a504fb9c97178764272bbe"
AGENT_PARENTS = (
    "de2d1aadbec1b9f4bfb76dcc70c62d2f192cb0a5",
    "9746c9254ad288945e01ecad25f71689a6231a42",
)
RUNTIME_COMMIT = "becfe6db88b2cc034dba3fafa6c050117cdf2b06"
RUNTIME_TREE = "7edc08e3fe94edcbc8ef695c479f4de301789b89"
LEGACY_AGENT_TREE = "1094bf3662c785e4b21eddf7e3ae980da79b1af1"
LEGACY_AGENT_TREE_P3 = "2deab1a1494fbccfce5e9235412bacb8a949c0cd"
LEGACY_RUNTIME_TREE = "be4114705127f9ee9e86b26cd6de3f467e771c01"
LEGACY_CHILD_NAMES = (
    "venv-agent-child-app-popup-333b-37eb-1016",
    "venv-agent-child-app-ready-079-37eb-0256",
)
LEGACY_REMOTION_NAMES = ("agent-remotion-app-ready-079-37eb-0258",)
LEGACY_P3_PARENT = "2e3c8f65a8628127cd283ed26116f7bcb2977b83 2357df925a660dde6624149b8e8a6e1dbf09da98"

_DRY_PREFLIGHT_SPEC = importlib.util.spec_from_file_location(
    "caller_dry_preflight", ARTIFACT / "caller-dry-preflight.py"
)
if _DRY_PREFLIGHT_SPEC is None or _DRY_PREFLIGHT_SPEC.loader is None:
    raise RuntimeError("PREPARED: dry preflight helper is unavailable")
_DRY_PREFLIGHT = importlib.util.module_from_spec(_DRY_PREFLIGHT_SPEC)
_DRY_PREFLIGHT_SPEC.loader.exec_module(_DRY_PREFLIGHT)

P2_SUITE = "full-e2e-three-products"
P3_SUITE = "ap2-P3-gate5-h6-0348"
SOURCE_PATHS = (
    "tests/e2e/local/three-products.spec.ts",
    "tests/e2e/local/support/gate5-reset-precondition.ts",
    "tests/e2e/local/support/gate5-reset-precondition.test.mjs",
    "tests/e2e/local/support/gate5-fault-order.ts",
    "tests/e2e/local/support/gate5-fault-order.test.mjs",
)

REQUEST_FIELDS = [
    "api_version", "project_id", "timeline_id", "base_revision_id",
    "base_publication_id", "commands", "schema_version", "op", "version",
    "select", "args", "created", "label", "steps", "id", "intent", "tags",
    "command_ordinals", "patch", "reads", "dependencies", "merge", "fields",
    "atomic", "Idempotency-Key", "dry_run", "source", "rationale", "group_id",
]
REPLY_FIELDS = [
    "data", "receipt", "canonical_document", "document_digest", "id_map", "commands",
    "authoritative_commands", "authoritative_steps", "dependencies", "merge_mode", "base",
    "base_revision_id", "base_publication_id", "previous", "previous_revision_id",
    "previous_publication_id", "accepted_ids", "accepted_revision_id", "publisher", "provider",
    "durable_receipt", "accepted", "merged", "rebased", "conflict", "invalid", "code", "path",
    "hint", "suggested_command", "head", "current", "result", "request_hash", "event_ids",
    "dry_run", "would_status", "reason", "http_status",
]


class PreparedError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise PreparedError("PREPARED: " + message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"git check failed for {root}: {exc}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    require(path.is_file() and not path.is_symlink(), f"missing regular file: {path}")
    return sha256(path.read_bytes())


def facts(root: Path, commit: str, tree: str, label: str, *, parents: tuple[str, ...] = ()) -> dict[str, Any]:
    require(root.is_dir() and not root.is_symlink(), f"{label} checkout is unavailable: {root}")
    actual = git(root, "rev-parse", "HEAD")
    actual_tree = git(root, "show", "-s", "--format=%T", "HEAD")
    actual_parents = tuple(git(root, "show", "-s", "--format=%P", "HEAD").split())
    require(actual == commit, f"{label} source mismatch: {actual} != {commit}")
    require(actual_tree == tree, f"{label} tree mismatch: {actual_tree} != {tree}")
    if parents:
        require(actual_parents == parents, f"{label} parent mismatch: {actual_parents} != {parents}")
    dirty = [line for line in git(root, "status", "--porcelain=v1", "--untracked-files=all").splitlines() if line]
    require(not dirty, f"{label} checkout is dirty: {dirty[:3]}")
    return {
        "checkout": str(root), "source": actual, "tree": actual_tree,
        "parents": list(actual_parents), "ref": git(root, "branch", "--show-current") or "HEAD",
    }


def app_facts() -> dict[str, Any]:
    # The production source is the clean normal integration checkout, never
    # this caller-artifact worktree.  A later harness commit may advance the
    # artifact branch without changing the product source target.
    require(APP != ARTIFACT, "App source checkout must not be the caller artifact")
    source = git(APP, "rev-parse", "HEAD")
    tree = git(APP, "show", "-s", "--format=%T", "HEAD")
    parents = tuple(git(APP, "show", "-s", "--format=%P", "HEAD").split())
    require(source == APP_COMMIT, f"App source is not the approved integrated commit: {source}")
    require(tree == APP_TREE, f"App tree is not the approved integrated tree: {tree}")
    require(parents == APP_PARENTS, f"App parents are not exact: {parents}")
    require(not git(APP, "status", "--porcelain=v1", "--untracked-files=all"), "App source checkout is dirty")
    return {
        "checkout": str(APP), "source": source, "tree": tree, "parents": list(parents),
        "ref": git(APP, "branch", "--show-current") or "HEAD", "orch": str(ORCH),
    }


def read_lock(root: Path) -> dict[str, Any]:
    path = root / "runtime.lock.json"
    require(path.is_file() and not path.is_symlink(), f"missing runtime lock: {path}")
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid runtime lock: {path}: {exc}")
    require(isinstance(value, dict), f"runtime lock is not an object: {path}")
    return value


def check_runtime_lock() -> dict[str, Any]:
    app_lock = read_lock(APP)
    agent_lock = read_lock(AGENT)
    for label, lock in (("App", app_lock), ("Agent", agent_lock)):
        require(lock.get("source_commit") == RUNTIME_COMMIT, f"{label} runtime lock producer is not {RUNTIME_COMMIT}")
    app_files = app_lock.get("files", {})
    agent_files = agent_lock.get("files", {})
    require(isinstance(app_files, dict) and isinstance(agent_files, dict), "runtime lock files are not objects")
    producer_files: dict[str, str] = {}
    for destination, entry in app_files.items():
        if not isinstance(entry, dict) or not str(entry.get("sha256", "")).startswith("sha256:"):
            fail(f"invalid App lock entry: {destination}")
        source_path = str(entry.get("from", ""))
        expected = str(entry["sha256"])[len("sha256:"):]
        actual = file_sha(APP / destination)
        require(actual == expected, f"App runtime consumer hash mismatch: {destination}")
        if source_path.startswith("packages/"):
            source_bytes = subprocess.check_output(["git", "-C", str(RUNTIME), "show", f"{RUNTIME_COMMIT}:{source_path}"])
            producer_files[source_path] = sha256(source_bytes)
            require(producer_files[source_path] == expected, f"Runtime producer mismatch: {source_path}")
    for destination, entry in agent_files.items():
        if not isinstance(entry, dict) or not str(entry.get("sha256", "")).startswith("sha256:"):
            fail(f"invalid Agent lock entry: {destination}")
        expected = str(entry["sha256"])[len("sha256:"):]
        actual = file_sha(AGENT / destination)
        require(actual == expected, f"Agent runtime consumer hash mismatch: {destination}")
    return {
        "producer": {"source": RUNTIME_COMMIT, "tree": RUNTIME_TREE, "ref": "HEAD", "files": producer_files},
        "app_consumer": {"source": app_lock["source_commit"], "file_count": len(app_files), "lock_sha256": file_sha(APP / "runtime.lock.json")},
        "agent_consumer": {"source": agent_lock["source_commit"], "file_count": len(agent_files), "lock_sha256": file_sha(AGENT / "runtime.lock.json")},
    }


def extract_row(line: str) -> tuple[str, str, str]:
    outer = line.split(None, 2)[2].rstrip("\n")
    start_marker = "$(bash -c "
    start = outer.index(start_marker) + len(start_marker)
    end = outer.index(")\" && eval", start)
    decoded = shlex.split(outer[start:end])
    require(len(decoded) == 1, "suite row bash payload is not one quoted argument")
    return outer, decoded[0], outer[end:]


def installed_rows() -> tuple[dict[str, Any], dict[str, str]]:
    rows: dict[str, str] = {}
    for line in SUITES.read_text().splitlines(True):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split(None, 2)
        if len(fields) >= 2 and fields[0] == "app" and fields[1] in {P2_SUITE, P3_SUITE}:
            rows[fields[1]] = line
    require(set(rows) == {P2_SUITE, P3_SUITE}, "current P2/P3 registry rows are not both present")
    whole = SUITES.read_bytes()
    outside = b"".join(line.encode() for line in SUITES.read_text().splitlines(True) if not any(line.startswith(f"app {name} ") for name in rows))
    snapshot = {
        "path": str(SUITES), "line_count": len(whole.splitlines()), "byte_count": len(whole), "sha256": sha256(whole),
        "outside_row_count": len(outside.splitlines()), "outside_bytes": len(outside), "outside_sha256": sha256(outside),
        "rows": {name: {"sha256": sha256(line.encode()), "bytes": len(line.encode())} for name, line in rows.items()},
    }
    return snapshot, rows


def assignment(body: str, key: str) -> str:
    match = re.search(rf"(?:^|;)\s*{re.escape(key)}=([^;]*)", body)
    require(match is not None, f"suite row lacks {key} assignment")
    return match.group(1)


def set_assignment(body: str, key: str, value: str) -> str:
    pattern = rf"((?:^|;)\s*{re.escape(key)}=)[^;]*"
    result, count = re.subn(pattern, rf"\g<1>{value}", body, count=1)
    require(count == 1, f"suite row lacks unique {key} assignment")
    return result


def refresh_source_guards(body: str, variables: dict[str, str]) -> tuple[str, int]:
    """Recompute every App blob/digest guard in the installed row template."""
    count = 0

    def git_guard(match: re.Match[str]) -> str:
        nonlocal count
        path = match.group("path").strip("'\"")
        if path.startswith("$"):
            variable = path.removeprefix("$").strip("{}")
            path = variables.get(variable, path)
        require((APP / path).is_file(), f"source guard path is missing from integrated App: {path}")
        value = git(APP, "hash-object", "--", path)
        count += 1
        return match.group("prefix") + value

    def sha_guard(match: re.Match[str]) -> str:
        nonlocal count
        path = match.group("path").strip("'\"")
        if path.startswith("$"):
            variable = path.removeprefix("$").strip("{}")
            path = variables.get(variable, path)
        require((APP / path).is_file(), f"digest guard path is missing from integrated App: {path}")
        value = file_sha(APP / path)
        count += 1
        return match.group("prefix") + value

    body = re.sub(
        r"(?P<prefix>git hash-object -- (?P<path>[^ )|]+)[^;\n]*?=\s*)[0-9a-f]{40}(?![0-9a-f])",
        git_guard,
        body,
    )
    body = re.sub(
        r"(?P<prefix>sha256sum -- (?P<path>[^ )|]+)[^;\n]*?=\s*)[0-9a-f]{64}(?![0-9a-f])",
        sha_guard,
        body,
    )
    require(count > 0, "no source guards were found in the installed rows")
    return body, count


def rebind(name: str, body: str) -> tuple[str, dict[str, str]]:
    for marker in ("original-body-NOTRUN", "following-stages-NOTRUN"):
        require(marker in body, f"{name} lost required failure guard: {marker}")
    for marker in ("PLAYWRIGHT_OUTPUT_DIR", "mkdir -p"):
        require(marker in body, f"{name} lost required output guard: {marker}")
    prefix = "P2" if name == P2_SUITE else "P3"
    old = {key: assignment(body, key) for key in (f"{prefix}A", f"{prefix}R", f"{prefix}APP", f"{prefix}TREE")}
    old_parent = assignment(body, f"{prefix}PARENT") if name == P2_SUITE else None
    for key, value in ((f"{prefix}A", AGENT_COMMIT), (f"{prefix}R", RUNTIME_COMMIT), (f"{prefix}APP", APP_COMMIT), (f"{prefix}TREE", APP_TREE)):
        body = set_assignment(body, key, value)
    if name == P2_SUITE:
        body = set_assignment(body, "P2PARENT", repr(" ".join(APP_PARENTS)))
    else:
        body = body.replace(LEGACY_P3_PARENT, " ".join(APP_PARENTS))
    body = set_assignment(body, f"{prefix}AG", "${TIMELINE_AGENT_CHECKOUT:?}")
    body = set_assignment(body, f"{prefix}RT", "${TIMELINE_RUNTIME_CHECKOUT:?}")
    body = set_assignment(body, "CN", "${TIMELINE_CHILD_NAME:?}")
    body = set_assignment(body, "RN", "${TIMELINE_REMOTION_NAME:?}")
    replacements = {
        old[f"{prefix}A"]: AGENT_COMMIT,
        old[f"{prefix}R"]: RUNTIME_COMMIT,
        old[f"{prefix}APP"]: APP_COMMIT,
        old[f"{prefix}TREE"]: APP_TREE,
        LEGACY_AGENT_TREE: AGENT_TREE,
        LEGACY_AGENT_TREE_P3: AGENT_TREE,
        LEGACY_RUNTIME_TREE: RUNTIME_TREE,
    }
    if old_parent:
        replacements[old_parent.strip("'\"")] = " ".join(APP_PARENTS)
    for before, after in replacements.items():
        body = body.replace(before, after)
    variables = {}
    for key in ("P2BODY", "P3BODY"):
        match = re.search(rf"(?:^|;)\s*{key}=([^;]*)", body)
        if match:
            variables[key] = match.group(1).strip("'\"")
    body, guard_count = refresh_source_guards(body, variables)
    body = refresh_encoded_guards(body)
    for forbidden in (
        old[f"{prefix}A"], old[f"{prefix}R"], old[f"{prefix}APP"], old[f"{prefix}TREE"],
        LEGACY_AGENT_TREE, LEGACY_AGENT_TREE_P3, LEGACY_RUNTIME_TREE,
    ):
        require(forbidden not in body, f"{name} candidate retained stale source identity {forbidden}")
    body = (
        'test -n "${TIMELINE_AGENT_CHECKOUT:-}" && test -n "${TIMELINE_RUNTIME_CHECKOUT:-}" && '
        'test -n "${TIMELINE_CHILD_NAME:-}" && test -n "${TIMELINE_REMOTION_NAME:-}" || '
        '{ echo "final tuple custody inputs are required" >&2; exit 2; }; '
        + body
    )
    return body, {"agent_old": old[f"{prefix}A"], "runtime_old": old[f"{prefix}R"], "app_old": old[f"{prefix}APP"], "tree_old": old[f"{prefix}TREE"], "source_guard_count": str(guard_count)}


def refresh_wrapper_bindings(text: str, old: dict[str, str]) -> str:
    replacements = {
        old["agent_old"]: AGENT_COMMIT,
        old["runtime_old"]: RUNTIME_COMMIT,
        old["app_old"]: APP_COMMIT,
        old["tree_old"]: APP_TREE,
        LEGACY_AGENT_TREE: AGENT_TREE,
        LEGACY_AGENT_TREE_P3: AGENT_TREE,
        LEGACY_RUNTIME_TREE: RUNTIME_TREE,
        LEGACY_CHILD_NAMES[0]: "${TIMELINE_CHILD_NAME:?}",
        LEGACY_CHILD_NAMES[1]: "${TIMELINE_CHILD_NAME:?}",
        LEGACY_REMOTION_NAMES[0]: "${TIMELINE_REMOTION_NAME:?}",
        LEGACY_P3_PARENT: " ".join(APP_PARENTS),
    }
    for before, after in replacements.items():
        text = text.replace(before, after)
    return text


def refresh_encoded_guards(text: str) -> str:
    """Re-encode retained custody code with the current tuple identities."""
    legacy = {
        "079580ca46af77e0292d49dc34386b25c8391f99": AGENT_COMMIT,
        "333b44b1a1b8be72d4d101391b7636c508419109": AGENT_COMMIT,
        "37eb6c7bdb79dcae2523883e66b5cea5be721ffd": RUNTIME_COMMIT,
        LEGACY_AGENT_TREE: AGENT_TREE,
        LEGACY_AGENT_TREE_P3: AGENT_TREE,
        LEGACY_RUNTIME_TREE: RUNTIME_TREE,
    }

    def replace(match: re.Match[str]) -> str:
        encoded = match.group("encoded")
        decoded = base64.b64decode(encoded, validate=True).decode()
        for before, after in legacy.items():
            decoded = decoded.replace(before, after)
        return match.group("prefix") + base64.b64encode(decoded.encode()).decode() + match.group("suffix")

    return re.sub(
        r'(?P<prefix>base64\.b64decode\(\\?")(?P<encoded>[A-Za-z0-9+/=]+)(?P<suffix>\\?"\))',
        replace,
        text,
    )


def syntax_check(outer: str, body: str, directory: Path, label: str) -> dict[str, Any]:
    decoded = directory / f"{label}.decoded.sh"
    wrapped = directory / f"{label}.wrapped.sh"
    decoded.write_text(body)
    wrapped.write_text(outer)
    for path in (decoded, wrapped):
        result = subprocess.run(["bash", "-n", str(path)], text=True, capture_output=True)
        require(result.returncode == 0, f"bash -n failed for {label} {path.name}: {result.stderr.strip()}")
    return {"decoded": str(decoded), "wrapped": str(wrapped), "decoded_sha256": file_sha(decoded), "wrapped_sha256": file_sha(wrapped)}


def custody_requirements() -> list[dict[str, str]]:
    required = [
        ("tuple_coordinator_admission", "normal coordinator admission for the exact App/Agent/Runtime tuple"),
        ("app_checkout_receipt", "normal exact App checkout receipt for the approved source"),
        ("agent_checkout_receipt", "normal exact Agent checkout receipt for the approved source"),
        ("runtime_checkout_receipt", "normal exact Runtime checkout receipt for the approved source"),
        ("genuine_child_identity", "genuine current child identity and client import receipt"),
        ("runtime_backend_identity", "genuine current Runtime backend identity and receipt"),
        ("remotion_identity", "genuine current Remotion environment identity and receipt"),
        ("graph_receipt", "genuine current graph receipt tied to the exact tuple"),
        ("service_snapshot", "normal service snapshot created after custody admission"),
        ("full_16138_terminal", "terminal result for the integrated 16138 run"),
    ]
    return [{"name": name, "status": "MISSING", "required": description} for name, description in required]


def negative(mode: str) -> int:
    try:
        if mode in {"wrong-source", "stale", "app"}:
            facts(APP, "0" * 40, APP_TREE, "negative App", parents=APP_PARENTS)
        elif mode == "agent":
            facts(AGENT, "0" * 40, AGENT_TREE, "negative Agent", parents=AGENT_PARENTS)
        elif mode == "runtime":
            facts(RUNTIME, "0" * 40, RUNTIME_TREE, "negative Runtime")
        elif mode == "tree":
            facts(APP, APP_COMMIT, "0" * 40, "negative App", parents=APP_PARENTS)
        elif mode == "target":
            facts(Path("/tmp"), AGENT_COMMIT, AGENT_TREE, "negative target")
        elif mode == "body":
            source = app_facts()
            agent = facts(AGENT, AGENT_COMMIT, AGENT_TREE, "Agent", parents=AGENT_PARENTS)
            runtime = facts(RUNTIME, RUNTIME_COMMIT, RUNTIME_TREE, "Runtime")
            _, body, _ = extract_row(next(line for line in SUITES.read_text().splitlines(True) if line.startswith(f"app {P2_SUITE} ")))
            rebound, _ = rebind(P2_SUITE, body)
            rebound = rebound.replace(AGENT_TREE, "0" * 40, 1)
            try:
                _DRY_PREFLIGHT.dry_source_preflight(rebound, app=source, agent=agent, runtime=runtime, target=APP)
            except _DRY_PREFLIGHT.DryPreflightError as exc:
                raise PreparedError(str(exc)) from exc
        elif mode == "receipt":
            require(False, "exact normal tuple receipt is absent")
        elif mode == "registry":
            snapshot, _ = installed_rows()
            require(snapshot["outside_sha256"] == "0" * 64, "registry outsider bytes changed")
        else:
            fail(f"unknown negative control: {mode}")
    except PreparedError as exc:
        print(f"NEGATIVE {mode}: REFUSED: {exc}")
        return 0
    raise SystemExit(f"negative control unexpectedly accepted: {mode}")


def prepare() -> dict[str, Any]:
    source = app_facts()
    agent = facts(AGENT, AGENT_COMMIT, AGENT_TREE, "Agent", parents=AGENT_PARENTS)
    runtime = facts(RUNTIME, RUNTIME_COMMIT, RUNTIME_TREE, "Runtime")
    bindings = check_runtime_lock()
    registry, rows = installed_rows()
    tmp = Path(tempfile.mkdtemp(prefix="timeline-final-tuple-", dir=os.environ.get("TMPDIR", "/tmp")))
    candidates: dict[str, Any] = {}
    for name in (P2_SUITE, P3_SUITE):
        outer, body, suffix = extract_row(rows[name])
        rebound, old = rebind(name, body)
        dry = None
        if name == P2_SUITE:
            dry = _DRY_PREFLIGHT.dry_source_preflight(
                rebound,
                app=source,
                agent=agent,
                runtime=runtime,
                target=APP,
            )
        candidate_outer = (
            outer[: outer.index("$(bash -c ") + len("$(bash -c ")]
            + shlex.quote(rebound)
            + refresh_wrapper_bindings(suffix, old)
        )
        syntax = syntax_check(candidate_outer, rebound, tmp, name)
        candidates[name] = {"source_row_sha256": registry["rows"][name]["sha256"], "rebound": old, "syntax": syntax}
        if dry is not None:
            candidates[name]["dry_preflight"] = dry
    custody = custody_requirements()
    result = {
        "status": "PREPARED",
        "run_authorization": "NOT_GRANTED",
        "execution": "NOT_RUN",
        "source": source,
        "agent": agent,
        "runtime": runtime,
        "bindings": bindings,
        "registry": registry,
        "candidates": candidates,
        "preservation": {
            "p2_cases": 8,
            "p3": "strict D53 request/reply, reads, receipts, history, undo, restart, stage-output, wait, and failure guards retained",
            "legacy_route_traffic": 0,
            "registry_mutation": False,
        },
        "wire_fields": {"request": REQUEST_FIELDS, "reply": REPLY_FIELDS, "reply_shape": "full {data,receipt}"},
        "required_custody": custody,
        "blocked": {"owner": "tuple coordinator / Agent and Runtime owners", "reason": "current normal custody and coordinator receipts are absent; admissions refusal remains STOPPED", "bypass": "none; no alternate fetch, child, preload, receipt patch, or historical reuse"},
        "full_run": {
            "id": "app-U3b-F-reviewed-join-1146-full-1024120556-16138",
            "status": "RUNNING_OR_UNVERIFIED",
            "claim": "no terminal result claimed",
            "source_authentication": "not used for final source authentication; authenticate any service snapshot only after it exists",
        },
        "tmpdir": str(tmp),
    }
    (tmp / "caller-custody.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", choices=("wrong-source", "stale", "app", "agent", "runtime", "tree", "target", "body", "receipt", "registry"))
    args = parser.parse_args()
    try:
        return negative(args.negative) if args.negative else (prepare() and 0)
    except PreparedError as exc:
        print(str(exc), file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
