"""Prepare the final integrated Timeline caller without executing it.

This is a bounded preparation artifact.  It authenticates the current App,
Agent, and Runtime checkouts, reads the installed P2/P3 rows as templates,
rebinds their source and target guards to those authenticated identities, and
syntax-checks the decoded and wrapped candidates.  It never starts a service,
allocates a port, opens HTTP, launches a browser, installs a package, or
submits a request. D59 authorizes current-head runs. Actual environment inputs
remain bounded by the supported caller; service snapshots are checked only
after a request exists. This artifact makes no live execution claim.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import stat
import subprocess
import tempfile
from typing import Any


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
SUITES = ORCH / "tests/suites.conf"
ARTIFACT = Path(__file__).resolve().parent
APP = Path("/home/user/work/app")
AGENT = Path("/home/user/work/agent")
RUNTIME = Path("/home/user/work/runtime")
NORMAL_REF = "tl/integration"
# These are populated once, from the clean normal refs selected by `prepare`.
# Keeping them unset until then prevents a stale handoff tuple from becoming
# the source of a newly generated candidate.
APP_COMMIT = ""
APP_TREE = ""
APP_PARENTS: tuple[str, ...] = ()
AGENT_COMMIT = ""
AGENT_TREE = ""
AGENT_PARENTS: tuple[str, ...] = ()
RUNTIME_COMMIT = ""
RUNTIME_TREE = ""
RUNTIME_PARENTS: tuple[str, ...] = ()
SOURCE_BINDINGS: dict[str, dict[str, str]] = {}
# Fixed installed inputs from the independently reviewed 1238 snapshot.
REGISTRY_SHA256 = "52f556f8dfd4fcdb29443ac84db0f33ee9252bb808c92de4ab660871ec73db93"
APPROVED_ROWS = {
    "full-e2e-three-products": (
        "6a45d0567f7dea7a3c15fbcaf687f9dd62debf4527464529d8a4faf8f8e48fee",
        "f6042b33d35229f47fe74cbd2a575b5984422d2209ed664b996fe1b590656d43",
        "0839e6b5f6454e9a3101dbb7280b201052b5166e1836749b68d28717c22e1f58",
    ),
    "ap2-P3-gate5-h6-0348": (
        "1b7c7996f9d296aab985a0a9466de89bb71cc816d7796facc8bc79fa0b23c6e7",
        "6366048bf89533fa450a4575288ac2de004696bab49db6d32f1869783ae493f3",
        "47deb73f184acc27b701572b1378f2bf4ad70b75de546963647bc94cf6a8da7b",
    ),
}
LEGACY_AGENT_TREE = "1094bf3662c785e4b21eddf7e3ae980da79b1af1"
LEGACY_AGENT_TREE_P3 = "2deab1a1494fbccfce5e9235412bacb8a949c0cd"
LEGACY_RUNTIME_TREE = "be4114705127f9ee9e86b26cd6de3f467e771c01"
LEGACY_P3_CHILD = "venv-agent-child-app-ready-079-37eb-0256"
LEGACY_P3_PARENT = "2e3c8f65a8628127cd283ed26116f7bcb2977b83 2357df925a660dde6624149b8e8a6e1dbf09da98"

_DRY_PREFLIGHT_SPEC = importlib.util.spec_from_file_location(
    "caller_dry_preflight", ARTIFACT / "caller-dry-preflight.py"
)
if _DRY_PREFLIGHT_SPEC is None or _DRY_PREFLIGHT_SPEC.loader is None:
    raise RuntimeError("PREPARED: dry preflight helper is unavailable")
_DRY_PREFLIGHT = importlib.util.module_from_spec(_DRY_PREFLIGHT_SPEC)
_DRY_PREFLIGHT_SPEC.loader.exec_module(_DRY_PREFLIGHT)


def _local_module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ARTIFACT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"PREPARED: {filename} is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# These modules are the independently qualified normal working-service route.
# Loading them here keeps the production caller's construction path identical
# to the offline controls while leaving all execution stages in the retained
# suite rows untouched.
_WORKING_BINDING = _local_module("working-service-binding.py", "working_service_binding")
_SERVICE_CONTROL = _local_module("working-service-binding-control.py", "working_service_binding_control")
_SERVICE_RECIPE = _local_module("current-service-inputs.py", "current_service_inputs")

P2_SUITE = "full-e2e-three-products"
P3_SUITE = "ap2-P3-gate5-h6-0348"
PURE_TARGET_META = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/app-P2-P3-e68-current-pure-target-1409/meta"
)
PURE_TARGET_NAME = "app-P2-P3-e68-current-pure-target-1409"
PURE_TARGET_BRANCH = "tl/app-P2-P3-e68-current-pure-target-1409"
CUSTODY_PREFIX = (
    'test -n "${TIMELINE_AGENT_CHECKOUT:-}" && test -n "${TIMELINE_RUNTIME_CHECKOUT:-}" && '
    'test -n "${TIMELINE_CHILD_NAME:-}" && test -n "${TIMELINE_REMOTION_NAME:-}" || '
    '{ echo "current caller environment inputs are required; original-body-NOTRUN '
    'following-stages-NOTRUN" >&2; exit 2; }; '
)
NATIVE_SHA256 = "c96b2a484a3ba6ffbb7ea84e6013a8a77840782067f2469f771ecf07b74d0f13"
ENCODED_SHA256 = {
    P2_SUITE: "76107a62e6e6cc6180cd43cbc1c9620ad32244898943e329cdf1dad51f86479c",
    P3_SUITE: "9c67cf12699f2f9153d88b92491795b8a559f24fac0824a34f4d258e72177523",
}

# Generated wire-property inventories.  The source-derived closure below must
# equal these advertised sets; headers and enum values are metadata, not JSON
# properties.  Never project, truncate or rewrite an envelope.
REQUEST_FIELDS = [
    "after_id", "anchor", "api_version", "args", "authorship",
    "base_publication_id", "base_revision_id", "before", "bindings",
    "boundaries", "command_ordinals", "commands", "created", "detail",
    "dry_run", "expect", "group_id", "id", "intent", "key", "kind",
    "label", "members", "merge", "op", "order", "order_before", "owner",
    "ownership", "patch", "path", "policy", "position", "project_id",
    "query_version", "rationale", "reads", "ref", "resolved", "ripple",
    "schema_version", "select", "selections", "source", "state", "steps",
    "tags", "timeline_id", "value", "version", "via",
]
REPLY_FIELDS = [
    "accepted_revision_id", "after", "after_id", "anchor", "args", "authorship",
    "base", "base_publication_id", "base_revision_id", "before", "bindings",
    "boundaries", "boundary", "canonical_document", "cause", "change",
    "change_ordinal", "choices", "code", "command", "command_kind",
    "command_ordinal", "command_ordinals", "commands", "compiler_version",
    "conflicts", "content_digest", "created", "created_at", "current", "data",
    "dependencies", "dependency", "dependency_manifest", "derived_writes", "detail",
    "details", "document_digest", "document_id", "documents", "edge_after",
    "edge_before", "effect_ordinal", "evaluated_head", "event_ids", "expect",
    "group_id", "head", "hint", "http_status", "id", "id_map", "idempotency_key",
    "intent", "internal_timeline_revision_id", "internal_timeline_revisions",
    "internal_timelines", "items", "key", "kind", "label", "media", "media_id",
    "members", "merge", "merge_mode", "message", "next_cursor", "op", "order",
    "order_before", "ordinal", "ours", "owner", "owners", "ownership",
    "parent_revision", "patch", "path", "payload", "phase", "physical_ref",
    "pin", "policy", "position", "previous", "previous_publication_id",
    "previous_revision_id", "project_id", "project_seq", "provider_version",
    "publication_id", "publisher", "query_version", "rationale", "reads", "reason",
    "rebased_onto", "receipt", "receipt_id", "records", "ref", "request_hash",
    "resolved", "restored_from", "result", "revision_id", "ripple", "schema_version",
    "select", "selections", "shot_id", "shot_revisions", "shots", "side", "source",
    "state", "status", "step_id", "steps", "successor", "suggested_command", "tags",
    "theirs", "timeline_id", "undo_of", "undo_steps", "value", "version", "via",
    "would_status", "write_range", "writes",
]
WIRE_TYPE_PATH = "packages/typescript/src/timeline-commit-types.ts"
APP_WIRE_TYPE_PATH = "src/integrations/runtime/timeline-commit-types.ts"
WIRE_ROOTS = {"request": ("CommitRequest",), "reply_history": ("CommitOutcome", "HistoryPage")}
WIRE_METADATA = {
    "request_headers": ["Idempotency-Key"],
    "request_enum_values": {"merge": ["fields", "atomic"]},
    "reply_status_values": ["accepted", "merged", "rebased", "preview", "conflict", "refused", "invalid"],
}


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


def physical(path: Path) -> None:
    require(path.is_absolute() and path.resolve() == path and not path.is_symlink(), f"nonphysical path: {path}")


def identity(path: Path) -> tuple[int, ...]:
    physical(path)
    value = path.lstat()
    return (value.st_dev, value.st_ino, value.st_mode, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def regular_bytes(path: Path) -> bytes:
    before = identity(path)
    require(stat.S_ISREG(before[2]) and path.stat().st_nlink == 1, f"not a single regular file: {path}")
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        require((opened.st_dev, opened.st_ino) == before[:2], f"path substituted while opening: {path}")
        data = stream.read()
    require(identity(path) == before, f"file changed while reading: {path}")
    return data


def file_sha(path: Path) -> str:
    return sha256(regular_bytes(path))


def exact_record(path: Path, expected: str) -> bytes:
    data = regular_bytes(path)
    require(sha256(data) == expected, f"record digest mismatch: {path}")
    return data


def facts(root: Path, commit: str | None = None, tree: str | None = None, label: str = "source", *, parents: tuple[str, ...] | None = None) -> dict[str, Any]:
    expected_path = {"App": APP, "Agent": AGENT, "Runtime": RUNTIME}.get(label)
    require(expected_path is not None and root == expected_path, f"unexpected {label} checkout: {root}")
    physical(root)
    require(root.is_dir() and root != ARTIFACT, f"{label} checkout is unavailable or is the caller artifact")
    before = identity(root)[:2]
    require(git(root, "rev-parse", "--show-toplevel") == str(root), f"{label} is not the checkout root")
    require(git(root, "symbolic-ref", "--short", "HEAD") == NORMAL_REF, f"{label} is not on {NORMAL_REF}")
    actual = git(root, "rev-parse", "HEAD")
    require(git(root, "rev-parse", "refs/heads/" + NORMAL_REF) == actual, f"{label} normal ref changed")
    actual_tree = git(root, "show", "-s", "--format=%T", actual)
    actual_parents = tuple(git(root, "show", "-s", "--format=%P", actual).split())
    require(bool(re.fullmatch(r"[0-9a-f]{40}", actual)) and bool(actual_parents), f"{label} invalid commit identity")
    if commit is not None:
        require(actual == commit, f"{label} source mismatch: {actual} != {commit}")
    if tree is not None:
        require(actual_tree == tree, f"{label} tree mismatch: {actual_tree} != {tree}")
    if parents is not None:
        require(actual_parents == parents, f"{label} parent mismatch: {actual_parents} != {parents}")
    require(not git(root, "status", "--porcelain=v1", "--untracked-files=all"), f"{label} checkout is dirty")
    require(git(root, "rev-parse", "HEAD") == actual and identity(root)[:2] == before, f"{label} checkout changed during observation")
    return {
        "checkout": str(root), "source": actual, "tree": actual_tree,
        "parents": list(actual_parents), "ref": NORMAL_REF, "directory_identity": list(before),
    }


def freeze_tuple(source: dict[str, Any], agent: dict[str, Any], runtime: dict[str, Any]) -> None:
    """Freeze the exact normal-ref tuple used by every later guard check."""
    global APP_COMMIT, APP_TREE, APP_PARENTS
    global AGENT_COMMIT, AGENT_TREE, AGENT_PARENTS
    global RUNTIME_COMMIT, RUNTIME_TREE, RUNTIME_PARENTS
    APP_COMMIT, APP_TREE, APP_PARENTS = source["source"], source["tree"], tuple(source["parents"])
    AGENT_COMMIT, AGENT_TREE, AGENT_PARENTS = agent["source"], agent["tree"], tuple(agent["parents"])
    RUNTIME_COMMIT, RUNTIME_TREE, RUNTIME_PARENTS = runtime["source"], runtime["tree"], tuple(runtime["parents"])
    SOURCE_BINDINGS.clear()


def app_facts() -> dict[str, Any]:
    for label, root in (("APP", APP), ("AGENT", AGENT), ("RUNTIME", RUNTIME)):
        value = os.environ.get(f"TIMELINE_{label}_CHECKOUT", str(root))
        require(value == str(root), f"{label} checkout substitution is refused: {value}")
    return {**facts(APP, label="App"), "orch": str(ORCH)}


def read_lock(root: Path) -> dict[str, Any]:
    path = root / "runtime.lock.json"
    require(path.is_file() and not path.is_symlink(), f"missing runtime lock: {path}")
    try:
        value = json.loads(regular_bytes(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid runtime lock: {path}: {exc}")
    require(isinstance(value, dict), f"runtime lock is not an object: {path}")
    return value


def check_runtime_lock() -> dict[str, Any]:
    app_lock = read_lock(APP)
    agent_lock = read_lock(AGENT)
    for label, lock in (("App", app_lock), ("Agent", agent_lock)):
        require(lock.get("source_commit") == RUNTIME_COMMIT, f"{label} runtime lock producer is not {RUNTIME_COMMIT}")
    producer_files: dict[str, str] = {}
    consumers: dict[str, Any] = {}
    for label, root, lock, count in (("app", APP, app_lock, 14), ("agent", AGENT, agent_lock, 15)):
        files = lock.get("files")
        require(isinstance(files, dict) and len(files) == count, f"{label} runtime lock file inventory changed")
        mappings = {}
        for destination, entry in files.items():
            require(isinstance(entry, dict), f"invalid {label} lock entry: {destination}")
            source_path = entry.get("from")
            digest = entry.get("sha256", "")
            require(isinstance(digest, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is not None,
                    f"invalid {label} lock digest: {destination}")
            for path in (destination, source_path):
                require(isinstance(path, str) and bool(path) and not PurePosixPath(path).is_absolute()
                        and ".." not in PurePosixPath(path).parts and str(PurePosixPath(path)) == path,
                        f"invalid {label} mapping path: {path}")
            expected = digest[len("sha256:"):]
            require(file_sha(root / destination) == expected, f"{label} runtime consumer hash mismatch: {destination}")
            if source_path not in producer_files:
                producer_files[source_path] = sha256(git_bytes(RUNTIME, RUNTIME_COMMIT, source_path))
            require(producer_files[source_path] == expected, f"Runtime producer mismatch: {label} {source_path}")
            mappings[destination] = {"from": source_path, "sha256": expected}
        consumers[label + "_consumer"] = {
            "source": lock["source_commit"], "file_count": len(files),
            "lock_sha256": file_sha(root / "runtime.lock.json"), "mappings": mappings,
        }
    return {
        "producer": {"source": RUNTIME_COMMIT, "tree": RUNTIME_TREE, "ref": NORMAL_REF,
                     "parents": list(RUNTIME_PARENTS), "files": producer_files},
        **consumers,
    }


def git_bytes(root: Path, commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "-C", str(root), "show", f"{commit}:{path}"], stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"producer blob unavailable: {root} {commit}:{path}: {exc}")


def _type_aliases(source: str) -> dict[str, str]:
    """Read the bounded generated TypeScript type-alias surface.

    This deliberately handles only the generated file grammar: exported type
    aliases terminated by a top-level semicolon.  It does not execute or
    import TypeScript, and it treats index signatures and JSON/Record values as
    open payloads with no advertised property names.
    """
    aliases: dict[str, str] = {}
    declaration = re.compile(r"^export\s+type\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*", re.MULTILINE)
    for match in declaration.finditer(source):
        depth = 0
        quote = ""
        escaped = False
        end = match.end()
        while end < len(source):
            char = source[end]
            if quote:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = ""
            elif char in "'\"":
                quote = char
            elif char in "({[":
                depth += 1
            elif char in ")}]":
                depth -= 1
            elif char == ";" and depth == 0:
                break
            end += 1
        require(end < len(source), f"unterminated generated type alias: {match.group(1)}")
        aliases[match.group(1)] = source[match.end():end]
    require(aliases, "generated wire type source has no exported type aliases")
    return aliases


def _object_regions(expression: str) -> list[str]:
    regions: list[str] = []
    starts: list[int] = []
    quote = ""
    escaped = False
    for index, char in enumerate(expression):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
        elif char in "'\"":
            quote = char
        elif char == "{":
            starts.append(index)
        elif char == "}" and starts:
            regions.append(expression[starts.pop() + 1:index])
    require(not starts, "unbalanced generated wire type object")
    return regions


def _top_level_members(region: str) -> list[str]:
    members: list[str] = []
    start = 0
    depth = 0
    quote = ""
    escaped = False
    for index, char in enumerate(region):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = ""
        elif char in "'\"":
            quote = char
        elif char in "({[":
            depth += 1
        elif char in ")}]":
            depth -= 1
        elif char == ";" and depth == 0:
            members.append(region[start:index])
            start = index + 1
    members.append(region[start:])
    return members


def _generated_closure(source: str, roots: tuple[str, ...]) -> tuple[set[str], set[str]]:
    aliases = _type_aliases(source)
    types: set[str] = set()
    fields: set[str] = set()
    pending = list(roots)
    while pending:
        name = pending.pop()
        if name in types:
            continue
        require(name in aliases, f"generated wire root is missing: {name}")
        types.add(name)
        expression = aliases[name]
        for region in _object_regions(expression):
            for member in _top_level_members(region):
                property_match = re.match(
                    r"(?:readonly\s+)?([A-Za-z_$][A-Za-z0-9_$-]*)(?:\?)?\s*:",
                    member.strip(),
                )
                if property_match:
                    fields.add(property_match.group(1))
        for reference in re.findall(r"\b[A-Z][A-Za-z0-9_]*\b", expression):
            if reference in aliases and reference not in types:
                pending.append(reference)
    return types, fields


def _wire_source(root: Path, commit: str, path: str) -> str:
    source = git_bytes(root, commit, path).decode("utf-8")
    require(regular_bytes(root / path).decode("utf-8") == source,
            f"generated wire type source differs from frozen {root}: {path}")
    return source


def wire_inventory() -> dict[str, Any]:
    """Derive and authenticate the complete request/reply property closures."""
    sources = {
        "Runtime": _wire_source(RUNTIME, RUNTIME_COMMIT, WIRE_TYPE_PATH),
        "App": _wire_source(APP, APP_COMMIT, APP_WIRE_TYPE_PATH),
    }
    derived: dict[str, dict[str, Any]] = {}
    for owner, source in sources.items():
        for name, roots in WIRE_ROOTS.items():
            types, fields = _generated_closure(source, roots)
            derived.setdefault(name, {})[owner] = {
                "type_count": len(types), "types": sorted(types), "fields": sorted(fields),
            }
    for name, advertised in (("request", REQUEST_FIELDS), ("reply_history", REPLY_FIELDS)):
        runtime = derived[name]["Runtime"]
        app = derived[name]["App"]
        require(runtime["types"] == app["types"], f"App/Runtime generated {name} type closure differs")
        require(runtime["fields"] == app["fields"], f"App/Runtime generated {name} property closure differs")
        actual = set(runtime["fields"])
        expected = set(advertised)
        missing = sorted(actual - expected)
        extra = sorted(expected - actual)
        require(not missing and not extra,
                f"{name} advertised inventory mismatch: missing={missing} extra={extra}")
        require(len(advertised) == len(expected), f"{name} advertised inventory contains duplicates")
    return {
        "provenance": {
            "Runtime": {"checkout": str(RUNTIME), "commit": RUNTIME_COMMIT, "path": WIRE_TYPE_PATH,
                         "roots": {key: list(value) for key, value in WIRE_ROOTS.items()}},
            "App": {"checkout": str(APP), "commit": APP_COMMIT, "path": APP_WIRE_TYPE_PATH,
                     "roots": {key: list(value) for key, value in WIRE_ROOTS.items()}},
        },
        "request": {"count": len(REQUEST_FIELDS), "fields": REQUEST_FIELDS,
                     "generated_type_count": derived["request"]["Runtime"]["type_count"]},
        "reply_history": {"count": len(REPLY_FIELDS), "fields": REPLY_FIELDS,
                           "generated_type_count": derived["reply_history"]["Runtime"]["type_count"]},
        "metadata": WIRE_METADATA,
        "reply_shape": "complete authoritative {data,receipt}; inventory only, never a projection",
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
    before = identity(SUITES)
    whole = exact_record(SUITES, REGISTRY_SHA256)
    rows: dict[str, str] = {}
    outside = bytearray()
    for line in whole.splitlines(keepends=True):
        fields = line.split(None, 2)
        if len(fields) >= 2 and fields[0] == b"app" and fields[1].decode() in APPROVED_ROWS:
            name = fields[1].decode()
            require(name not in rows, f"duplicate registry row: {name}")
            require(sha256(line) == APPROVED_ROWS[name][0], f"unapproved registry row: {name}")
            outer, body, tail = extract_row(line.decode())
            require(sha256(body.encode()) == APPROVED_ROWS[name][1], f"unapproved decoded body: {name}")
            require(sha256(tail.encode()) == APPROVED_ROWS[name][2], f"unapproved tail: {name}")
            rows[name] = line.decode()
        else:
            outside.extend(line)
    require(set(rows) == set(APPROVED_ROWS), "current P2/P3 registry rows are not both present")
    require(identity(SUITES) == before, "concurrent registry change")
    snapshot = {
        "path": str(SUITES), "identity": list(before), "line_count": len(whole.splitlines()),
        "byte_count": len(whole), "sha256": sha256(whole), "outside_row_count": len(outside.splitlines()),
        "outside_bytes": len(outside), "outside_sha256": sha256(outside),
        "rows": {name: {"sha256": sha256(line.encode()), "bytes": len(line.encode()),
                           "decoded_sha256": APPROVED_ROWS[name][1], "tail_sha256": APPROVED_ROWS[name][2]}
                 for name, line in rows.items()},
    }
    return snapshot, rows


def unchanged_registry(snapshot: dict[str, Any]) -> None:
    require(list(identity(SUITES)) == snapshot["identity"], "concurrent registry replacement or write")
    require(file_sha(SUITES) == snapshot["sha256"] == REGISTRY_SHA256, "concurrent registry byte change")


def assignment(body: str, key: str) -> str:
    match = re.search(rf"(?:^|;)\s*{re.escape(key)}=([^;]*)", body)
    require(match is not None, f"suite row lacks {key} assignment")
    return match.group(1)


def literal_edits(text: str, before: str, after: str, count: int) -> list[tuple[int, int, str]]:
    matches = list(re.finditer(re.escape(before), text))
    require(len(matches) == count, f"binding occurrence count changed: {before}")
    return [(match.start(), match.end(), after) for match in matches]


def selected_file(path: str) -> dict[str, str]:
    require(not PurePosixPath(path).is_absolute() and ".." not in PurePosixPath(path).parts,
            f"unbounded App binding path: {path}")
    data = git_bytes(APP, APP_COMMIT, path)
    require(regular_bytes(APP / path) == data, f"App binding differs from frozen source: {path}")
    result = {"blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
              "sha256": sha256(data)}
    require(path not in SOURCE_BINDINGS or SOURCE_BINDINGS[path] == result, f"App binding changed during checks: {path}")
    SOURCE_BINDINGS[path] = result
    return result


def binding_edits(name: str, template: str, *, tail: bool = False) -> list[tuple[int, int, str]]:
    """Only binding value spans in the pinned template may change.

    Source digests bind whole tracked files at the frozen App commit. Expectations
    such as the retained awk case digests, native assertions, selectors and waits
    are outside these spans and must remain byte-identical.
    """
    require(name in APPROVED_ROWS and bool(APP_COMMIT), "unfrozen or unknown candidate")
    require(sha256(template.encode()) == APPROVED_ROWS[name][2 if tail else 1],
            f"unapproved {'tail' if tail else 'body'} template: {name}")
    p2 = name == P2_SUITE
    if tail and p2:
        return []
    prefix = "P2" if p2 else "P3"
    # Literal source/ref slots, with exact multiplicities from approved rows.
    slots = [
        ("333b44b1a1b8be72d4d101391b7636c508419109" if p2 else "079580ca46af77e0292d49dc34386b25c8391f99",
         AGENT_COMMIT, 3 if tail else 1),
        ("37eb6c7bdb79dcae2523883e66b5cea5be721ffd", RUNTIME_COMMIT, 3 if tail else 1),
        (LEGACY_AGENT_TREE if p2 else LEGACY_AGENT_TREE_P3, AGENT_TREE, 1),
        (LEGACY_RUNTIME_TREE, RUNTIME_TREE, 1),
    ]
    if tail:
        slots.extend([
            (LEGACY_P3_CHILD, '"${TIMELINE_CHILD_NAME:?}"', 1),
            ("/home/user/work/wt/rt-pin-34eac004", '"${TIMELINE_RUNTIME_CHECKOUT:?}"', 1),
        ])
    else:
        slots.extend([
            ("d6ed8cbda122d810d5836ebfce3c56c10e76e9b4" if p2 else "602f8b1f58593302829fb449d0ded62a91462a22",
             APP_COMMIT, 1 if p2 else 4),
            ("542b772e6deed676b917f857708445b7d37a5aa8" if p2 else "a38844975865110cd2c026dc10fd7aa1ea488e71",
             APP_TREE, 1 if p2 else 2),
            ("cad736828b4890a4df5fff42a22bfa4851a0ecfc 01ea81395a9bb8f091262a9d8275407675188fe6" if p2 else LEGACY_P3_PARENT,
             " ".join(APP_PARENTS), 1 if p2 else 2),
        ])
    edits = [edit for before, after, count in slots for edit in literal_edits(template, before, after, count)]
    if tail:
        return sorted(edits)
    for key, value in ((prefix + "AG", '"${TIMELINE_AGENT_CHECKOUT:?}"'),
                       (prefix + "RT", '"${TIMELINE_RUNTIME_CHECKOUT:?}"'),
                       ("CN", '"${TIMELINE_CHILD_NAME:?}"'), ("RN", '"${TIMELINE_REMOTION_NAME:?}"')):
        matches = list(re.finditer(rf"(?:^|;)\s*{key}=([^;]*)", template))
        require(len(matches) == 1, f"nonunique environment binding: {key}")
        edits.append((*matches[0].span(1), value))
    for algorithm, width, expected_count in (("git hash-object", 40, 67 if p2 else 84),
                                              ("sha256sum", 64, 4 if p2 else 57)):
        pattern = rf"{algorithm} -- (?P<path>[^ )|]+)[^;\n]*?=\s*(?P<digest>[0-9a-f]{{{width}}})(?![0-9a-f])"
        matches = list(re.finditer(pattern, template))
        require(len(matches) == expected_count, f"source binding inventory changed: {name} {algorithm}")
        for match in matches:
            path = match.group("path")
            if path == '"$P3BODY"':
                require(assignment(template, "P3BODY") == "tests/e2e/local/three-products.spec.ts", "P3 source path changed")
                path = "tests/e2e/local/three-products.spec.ts"
            value = selected_file(path)["blob" if width == 40 else "sha256"]
            edits.append((*match.span("digest"), value))
    return sorted(edits)


def render_bindings(template: str, edits: list[tuple[int, int, str]]) -> str:
    parts = []
    end = 0
    for start, stop, value in edits:
        require(end <= start < stop <= len(template), "overlapping or unbounded binding edits")
        parts.extend((template[end:start], value))
        end = stop
    return "".join(parts) + template[end:]


def bind_runtime_launches(text: str, name: str) -> str:
    """Route Runtime launches through the adapter's distinct interpreter."""

    literal = 'ASTRID_RUNTIME_PYTHON="$CPY"'
    expected = 1 if name == P2_SUITE else 2
    require(text.count(literal) == expected, f"{name} Runtime launch binding inventory changed")
    export_literal = 'ASTRID_RUNTIME_PYTHON "$CPY"'
    require(text.count(export_literal) == 1, f"{name} Runtime export binding inventory changed")
    return text.replace(literal, 'ASTRID_RUNTIME_PYTHON="$RCPY"').replace(
        export_literal, 'ASTRID_RUNTIME_PYTHON "$RCPY"'
    )


def compare_bindings(template: str, candidate: str, edits: list[tuple[int, int, str]], label: str) -> None:
    """Compare every unchanged span and each exact authenticated replacement."""
    require(len(candidate) == len(template) + sum(len(value) - (stop - start) for start, stop, value in edits),
            f"{label} protected length changed")
    original_at = candidate_at = 0
    for start, stop, value in edits:
        require(original_at <= start < stop <= len(template), f"{label} unbounded binding")
        unchanged = template[original_at:start]
        require(candidate[candidate_at:candidate_at + len(unchanged)] == unchanged, f"{label} protected bytes changed")
        candidate_at += len(unchanged)
        require(candidate[candidate_at:candidate_at + len(value)] == value, f"{label} unauthenticated binding")
        candidate_at += len(value)
        original_at = stop
    require(candidate[candidate_at:] == template[original_at:], f"{label} protected final bytes changed")


def native_stage(body: str) -> str:
    matches = list(re.finditer(r"node --import tsx --input-type=module -e '(.*?)' >", body, re.S))
    require(len(matches) == 1, "native stage boundary changed")
    return matches[0].group(0)


def authenticate_candidate(name: str, row: str, outer: str, body: str, *, environment: dict[str, Any] | None = None) -> dict[str, Any]:
    require(sha256(row.encode()) == APPROVED_ROWS[name][0], f"unapproved original row: {name}")
    original_outer, original, tail = extract_row(row)
    candidate_outer, decoded, candidate_tail = extract_row(f"app {name} {outer}\n")
    require(decoded == body and candidate_outer == outer, f"{name} wrapped payload differs")
    seam = "$(bash -c "
    require(outer[:outer.index(seam)] == original_outer[:original_outer.index(seam)], f"{name} outer prefix changed")
    require(body.startswith(CUSTODY_PREFIX), f"{name} missing bounded environment guard")
    body_edits = binding_edits(name, original)
    tail_edits = binding_edits(name, tail, tail=True)
    joined = body[len(CUSTODY_PREFIX):]
    if environment is None:
        compare_bindings(original, joined, body_edits, name + " body")
    else:
        stage = "2" if name == P2_SUITE else "3"
        start, end = _WORKING_BINDING._region(original, stage)
        expected = bind_runtime_launches(render_bindings(original, body_edits), name)
        replacement = environment.get("joined_environment_region")
        if replacement is None:
            replacement = environment["body"][start:start + environment["environment_region_bytes"]]
        marker = f'if test -n "$P{stage}FAIL"; then'
        expected_start = expected.find("STORE_ROOT=")
        expected_end = expected.find(marker, expected_start)
        require(expected_start >= 0 and expected_end - expected_start == end - start,
                f"{name} authenticated environment boundary moved")
        expected = expected[:expected_start] + replacement + expected[expected_end:]
        require(joined == expected, f"{name} joined source/environment bindings changed")
        require(environment["launch_bindings"] == {"Agent": "CPY", "Runtime": "RCPY"},
                f"{name} launch binding contract changed")
    compare_bindings(tail, candidate_tail, tail_edits, name + " tail")
    original_native, candidate_native = native_stage(original), native_stage(body)
    require(sha256(original_native.encode()) == NATIVE_SHA256 and candidate_native == original_native,
            f"{name} native/protected stage changed")
    encoded = re.findall(r'base64\.b64decode\(\\?"([A-Za-z0-9+/=]+)\\?"\)', body)
    require(len(encoded) == 1 and sha256(base64.b64decode(encoded[0], validate=True)) == ENCODED_SHA256[name],
            f"{name} encoded custody stage changed")
    return {"status": "PASS", "body_sha256": sha256(body.encode()), "tail_sha256": sha256(candidate_tail.encode()),
            "native_stage_sha256": NATIVE_SHA256, "encoded_stage_sha256": ENCODED_SHA256[name],
            "body_binding_spans": len(body_edits), "tail_binding_spans": len(tail_edits)}


def rebind(name: str, body: str) -> tuple[str, dict[str, str]]:
    edits = binding_edits(name, body)
    rebound = CUSTODY_PREFIX + render_bindings(body, edits)
    return rebound, {"binding_spans": str(len(edits))}


def refresh_wrapper_bindings(name: str, tail: str) -> str:
    return render_bindings(tail, binding_edits(name, tail, tail=True))


def normal_service_facts(source: dict[str, Any], agent: dict[str, Any], runtime: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], dict[str, Any]]:
    """Read and authenticate the actual normal working-service inputs."""

    recipe = _SERVICE_CONTROL.recipe()
    pending = recipe.get("status") == "pending_agent_runtime_adoption"
    pending_bindings = recipe.get("runtime_bindings", {}).get("pending", [])
    if pending:
        require(isinstance(pending_bindings, list) and pending_bindings,
                "pending service recipe has no recorded adoption dependency")
        dependency = pending_bindings[0]
        fail(
            "normal caller environment is not ready: Agent U4a adoption is pending; "
            f"{dependency.get('lock')} still names {dependency.get('observed_source_commit')} "
            f"instead of Runtime {dependency.get('required_source_commit')}; "
            "run the normal sync tool in the Agent integration worktree and refresh again"
        )
    for name, facts_value in (("app", source), ("agent", agent), ("runtime", runtime)):
        expected = recipe["source"][name]
        require(expected["checkout"] == facts_value["checkout"], f"normal recipe checkout mismatch: {name}")
        require(expected["ref"] == NORMAL_REF, f"normal recipe ref mismatch: {name}")
        require(expected["head"] == facts_value["source"], f"normal recipe head mismatch: {name}")
        require(expected["tree"] == facts_value["tree"], f"normal recipe tree mismatch: {name}")
        require(tuple(expected["parents"]) == tuple(facts_value["parents"]), f"normal recipe parents mismatch: {name}")

    probes = {
        "agent": _SERVICE_RECIPE.check_probe(
            recipe,
            "agent",
            ["astrid", "astrid_runtime_client", "banodoco_timeline_schema", "astrid_runtime", "runtime_protocol"],
            ["astrid", "banodoco-timeline-schema"],
        ),
        "runtime": _SERVICE_RECIPE.check_probe(
            recipe,
            "runtime",
            ["astrid_runtime", "runtime_protocol", "astrid", "astrid_runtime_client", "banodoco_timeline_schema"],
            ["astrid-runtime"],
        ),
    }
    checks = {
        "probes": probes,
        "client": _SERVICE_RECIPE.check_client(recipe),
        "remotion": _SERVICE_RECIPE.check_remotion(recipe),
        "composition": _SERVICE_RECIPE.check_graph(recipe),
    }
    bindings = _WORKING_BINDING.authenticated_bindings(recipe)
    return recipe, bindings, checks


def pure_target_facts(source: dict[str, Any]) -> dict[str, Any]:
    """Authenticate the separate read-only pure target without using it as a checkout."""

    require(PURE_TARGET_META.is_file() and not PURE_TARGET_META.is_symlink(),
            f"pure target metadata is unavailable: {PURE_TARGET_META}")
    fields = {}
    for line in regular_bytes(PURE_TARGET_META).decode("utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            fields[key] = value
    require(fields.get("name") == PURE_TARGET_NAME, "pure target metadata name changed")
    require(fields.get("base") == source["source"], "pure target metadata does not name the current App source")
    require(fields.get("base_sha") == source["source"][:10], "pure target metadata base abbreviation changed")
    return {
        "name": PURE_TARGET_NAME,
        "branch": PURE_TARGET_BRANCH,
        "metadata": str(PURE_TARGET_META),
        "checkout": source["checkout"],
        "source": source["source"],
        "tree": source["tree"],
        "parents": source["parents"],
        "target_use": "read-only source identity; never a product checkout or service target",
    }


def source_preflight() -> dict[str, Any]:
    """Run only the source/target phases while Agent U4a adoption is pending."""

    source = app_facts()
    agent = facts(AGENT, label="Agent")
    runtime = facts(RUNTIME, label="Runtime")
    freeze_tuple(source, agent, runtime)
    target = pure_target_facts(source)
    registry, rows = installed_rows()
    wire = wire_inventory()
    tmp = Path(tempfile.mkdtemp(prefix="timeline-source-preflight-", dir=os.environ.get("TMPDIR", "/tmp")))
    candidates: dict[str, Any] = {}
    for name in (P2_SUITE, P3_SUITE):
        outer, body, suffix = extract_row(rows[name])
        rebound, _ = rebind(name, body)
        dry = _DRY_PREFLIGHT.dry_source_preflight(
            rebound,
            app=source,
            agent=agent,
            runtime=runtime,
            target=APP,
            stage="2" if name == P2_SUITE else "3",
        )
        candidate_outer = (
            outer[: outer.index("$(bash -c ") + len("$(bash -c ")]
            + shlex.quote(rebound)
            + refresh_wrapper_bindings(name, suffix)
        )
        preservation = authenticate_candidate(name, rows[name], candidate_outer, rebound)
        syntax = syntax_check(candidate_outer, rebound, tmp, "source-" + name)
        candidates[name] = {
            "source_row_sha256": registry["rows"][name]["sha256"],
            "decoded_template_sha256": registry["rows"][name]["decoded_sha256"],
            "candidate_body_sha256": sha256(rebound.encode()),
            "candidate_outer_sha256": sha256(candidate_outer.encode()),
            "preservation": preservation,
            "syntax": syntax,
            "wrapper": {
                "status": "NOT_RUN_PENDING_ADOPTION",
                "reason": "The real wrapper/export seam is checked only after the normal Agent environment adapter can authenticate the e68 lock mapping.",
            },
            "dry_preflight": dry,
        }
    unchanged_registry(registry)
    require(app_facts() == source, "App normal tuple changed during source preflight")
    require(facts(AGENT, AGENT_COMMIT, AGENT_TREE, "Agent", parents=AGENT_PARENTS) == agent,
            "Agent normal tuple changed during source preflight")
    require(facts(RUNTIME, RUNTIME_COMMIT, RUNTIME_TREE, "Runtime", parents=RUNTIME_PARENTS) == runtime,
            "Runtime normal tuple changed during source preflight")
    result = {
        "status": "SOURCE_PREPARED_AGENT_ADOPTION_PENDING",
        "execution": "NOT_RUN",
        "source": source,
        "agent": agent,
        "runtime": runtime,
        "pure_target": target,
        "wire_fields": wire,
        "registry": registry,
        "candidates": candidates,
        "pending_dependency": {
            "lock": str(AGENT / "runtime.lock.json"),
            "observed_source_commit": json.loads(regular_bytes(AGENT / "runtime.lock.json")).get("source_commit"),
            "required_source_commit": RUNTIME_COMMIT,
            "reason": "Agent U4a must adopt Runtime e68 through the normal sync tool; the old lock is not relabeled.",
        },
        "preflight_scope": "source_identity_tree_target_bindings only; child/import/native/build/browser/backend/provision/schema/HTTP/original not run",
        "prepare_commands": {
            "refresh": "PYTHONDONTWRITEBYTECODE=1 python3 current-service-inputs.py --refresh",
            "source": "PYTHONDONTWRITEBYTECODE=1 python3 caller-publication.py --dry-source",
            "source_optimized": "PYTHONDONTWRITEBYTECODE=1 python3 -O caller-publication.py --dry-source",
            "full_prepare_after_adoption": "PYTHONDONTWRITEBYTECODE=1 python3 caller-publication.py",
            "full_prepare_after_adoption_optimized": "PYTHONDONTWRITEBYTECODE=1 python3 -O caller-publication.py",
        },
        "positive_baseline": "NOT_ESTABLISHED; normal environment adoption is pending",
        "service_execution": "NOT_RUN",
        "tmpdir": str(tmp),
    }
    (ARTIFACT / "caller-custody.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def join_environment(name: str, template: str, stage: str, recipe: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Join the reviewed environment block to the source-bound candidate."""

    adapted = _WORKING_BINDING.adapt_environment_block(template, stage=stage, recipe=recipe)
    edits = binding_edits(name, template)
    rendered = bind_runtime_launches(render_bindings(template, edits), name)
    start, end = _WORKING_BINDING._region(template, stage)
    marker = f'if test -n "$P{stage}FAIL"; then'
    rendered_start = rendered.find("STORE_ROOT=")
    rendered_end = rendered.find(marker, rendered_start)
    require(rendered_start >= 0 and rendered_end - rendered_start == end - start,
            f"{name} source binding moved the environment boundary")
    replacement = adapted["body"][start:start + adapted["environment_region_bytes"]]
    region = template[start:end]
    encoded_end = region.find('; if test "$STORE_STATUS"')
    require(encoded_end > 0 and region.count("STORE_INFO=$(python3 -c") == 1,
            f"{name} encoded custody boundary changed")
    encoded_prefix = region[:encoded_end]
    joined_replacement = encoded_prefix + "; " + replacement
    adapted["joined_environment_region"] = joined_replacement
    adapted["joined_environment_region_sha256"] = sha256(joined_replacement.encode())
    candidate = CUSTODY_PREFIX + rendered[:rendered_start] + joined_replacement + rendered[rendered_end:]
    require('ASTRID_AGENT_PYTHON="$CPY"' in candidate, f"{name} Agent interpreter binding was not consumed")
    require('ASTRID_RUNTIME_PYTHON="$RCPY"' in candidate, f"{name} Runtime interpreter binding was not consumed")
    return candidate, adapted


def syntax_check(outer: str, body: str, directory: Path, label: str) -> dict[str, Any]:
    decoded = directory / f"{label}.decoded.sh"
    wrapped = directory / f"{label}.wrapped.sh"
    decoded.write_text(body)
    wrapped.write_text(outer)
    for path in (decoded, wrapped):
        result = subprocess.run(["bash", "-n", str(path)], text=True, capture_output=True)
        require(result.returncode == 0, f"bash -n failed for {label} {path.name}: {result.stderr.strip()}")
    return {"decoded": str(decoded), "wrapped": str(wrapped), "decoded_sha256": file_sha(decoded), "wrapped_sha256": file_sha(wrapped)}


def wrapper_check(outer: str, body: str, label: str) -> dict[str, Any]:
    """Exercise the actual wrapper seam with only its final export statements."""
    marker = "$(bash -c "
    start = outer.index(marker) + len(marker)
    end = outer.index(')" && eval', start)
    argv = shlex.split(outer[start:end])
    require(len(argv) == 1 and argv[0] == body, f"{label} wrapper changed bash-c argv")
    prefix = "P2" if label == P2_SUITE else "P3"
    seam_end = end + len(f')" && eval "${prefix}_ENV"')
    require(outer[end:seam_end] == f')" && eval "${prefix}_ENV"', f"{label} wrapper lost eval suffix")
    exports = re.findall(r'printf "export %s=%q\\n" [^;]*;', body)
    require(len(exports) == (1 if prefix == "P2" else 2), f"{label} export inventory changed")
    variables = sorted(set(re.findall(r'\$([A-Za-z_][A-Za-z0-9_]*)', " ".join(exports))))
    # The shell function inspects the real wrapped argv without executing its
    # payload, then emits the candidate's unchanged export statements.
    probe = "\n".join([
        'set -eu',
        f'EXPECTED={shlex.quote(body)}',
        *[f'{key}={shlex.quote("probe " + key + "; literal $value")}' for key in variables],
        'bash(){ test "$#" = 2 && test "$1" = -c && test "$2" = "$EXPECTED" || return 9;',
        *exports, '}', outer[:seam_end],
        f'test "$TIMELINE_BUNDLE_AGENT_HEAD" = "${prefix}A"',
        f'test "$TIMELINE_BUNDLE_RUNTIME_HEAD" = "${prefix}R"',
        f'test "$ASTRID_CHECKOUT" = "${prefix}AG"',
        f'test "$ASTRID_RUNTIME_CHECKOUT" = "${prefix}RT"',
        'test "$ASTRID_PYTHON" = "$CPY" && test "$ASTRID_RUNTIME_PYTHON" = "$RCPY"',
        'test "${PLAYWRIGHT_OUTPUT_DIR+x}" = x',
        'printf "%s\\n" wrapper-argv-export-PASS',
    ])
    result = subprocess.run(["/bin/bash", "-c", probe], text=True, capture_output=True, timeout=10, check=False,
                            env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"})
    require(result.returncode == 0 and result.stdout.strip() == "wrapper-argv-export-PASS",
            f"{label} wrapped argv/export probe failed: {result.stderr}")
    # Empty environment inputs force the authenticated prefix to exit before
    # any original stage; the real outer && chain must propagate that failure.
    require(body.startswith(CUSTODY_PREFIX), f"{label} failure prefix changed")
    failure = subprocess.run(["/bin/bash", "-c", outer], text=True, capture_output=True, timeout=10, check=False,
                             env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"})
    require(failure.returncode == 2 and not failure.stdout and "original-body-NOTRUN" in failure.stderr
            and "following-stages-NOTRUN" in failure.stderr, f"{label} wrapped failure did not stop safely")
    return {"argv_count": len(argv), "eval_suffix": True, "export_probe": "PASS", "failure_returncode": 2,
            "failure_proof": failure.stderr.strip(), "probe_sha256": sha256(probe.encode())}


def custody_requirements() -> list[dict[str, str]]:
    # These are facts used by the retained template route.  The normal recipe
    # and working-service adapter authenticate them before candidate creation;
    # they are not a live-service or readiness claim.
    return [
        {"name": "caller_environment", "status": "AUTHENTICATED",
         "required": "Current refs, all parents, interpreter/import origins, Runtime client/artifact mappings, Remotion, and Composition graph must match the normal recipe.",
         "owner": "current-service-inputs.py/json and working-service-binding.py"},
    ]


def negative(mode: str) -> int:
    global SUITES, REGISTRY_SHA256, read_lock
    try:
        source = app_facts()
        agent = facts(AGENT, label="Agent")
        runtime = facts(RUNTIME, label="Runtime")
        freeze_tuple(source, agent, runtime)
        if mode in {"wrong-source", "stale", "app"}:
            facts(APP, "0" * 40, APP_TREE, "App", parents=APP_PARENTS)
        elif mode == "agent":
            facts(AGENT, "0" * 40, AGENT_TREE, "Agent", parents=AGENT_PARENTS)
        elif mode == "runtime":
            facts(RUNTIME, "0" * 40, RUNTIME_TREE, "Runtime", parents=RUNTIME_PARENTS)
        elif mode == "tree":
            facts(APP, APP_COMMIT, "0" * 40, "App", parents=APP_PARENTS)
        elif mode == "target":
            facts(Path("/tmp"), AGENT_COMMIT, AGENT_TREE, "negative target")
        elif mode == "body":
            _, body, _ = extract_row(next(line for line in SUITES.read_text().splitlines(True) if line.startswith(f"app {P2_SUITE} ")))
            rebound, _ = rebind(P2_SUITE, body)
            rebound = rebound.replace(AGENT_TREE, "0" * 40, 1)
            try:
                _DRY_PREFLIGHT.dry_source_preflight(rebound, app=source, agent=agent, runtime=runtime, target=APP, stage="2")
            except _DRY_PREFLIGHT.DryPreflightError as exc:
                raise PreparedError(str(exc)) from exc
        elif mode == "receipt":
            exact_record(ARTIFACT / "caller-custody.json", "0" * 64)
        elif mode in {"native", "protected", "tail", "encoded", "binding"}:
            _, rows = installed_rows()
            for name, row in rows.items():
                outer, template, suffix = extract_row(row)
                body, _ = rebind(name, template)
                tail = refresh_wrapper_bindings(name, suffix)
                seam = outer[:outer.index("$(bash -c ") + len("$(bash -c ")]
                wrapped = seam + shlex.quote(body) + tail
                authenticate_candidate(name, row, wrapped, body)
                if mode == "native":
                    before, after = "expect(seed.headRevisionId).toBeTruthy();", "expect(seed.headRevisionId).toBeFalsy();"
                elif mode == "protected":
                    # Fixed P1 expectation, unlike a source-file digest slot.
                    if name == P2_SUITE:
                        continue
                    before = "eecdb2b41f66ecfe16a3d564f701c3138e39dd214b473c98635c6f7da51cbd72"
                    after = "0" * 64
                elif mode == "binding":
                    before, after = APP_TREE, "0" * 40
                elif mode == "encoded":
                    match = re.search(r'base64\.b64decode\(\\?"([A-Za-z0-9+/=]+)\\?"\)', body)
                    require(match is not None, "negative encoded boundary unavailable")
                    before = match.group(1)
                    decoded = base64.b64decode(before).replace(b"!= 1", b"== 1", 1)
                    after = base64.b64encode(decoded).decode()
                else:
                    before, after = "npm run test:e2e:three-products", "npm run test:e2e:three-products --list"
                victim = tail if mode == "tail" else body
                require(before in victim and before != after, f"negative {mode} mutation not applied")
                if mode == "tail":
                    tail = tail.replace(before, after, 1)
                else:
                    body = body.replace(before, after, 1)
                wrapped = seam + shlex.quote(body) + tail
                try:
                    authenticate_candidate(name, row, wrapped, body)
                except PreparedError as exc:
                    require("protected" in str(exc) or "unauthenticated binding" in str(exc),
                            f"negative {mode} refused for unrelated reason: {exc}")
                    print(f"NEGATIVE {mode} {name}: REFUSED: {exc}")
                else:
                    raise SystemExit(f"negative {mode} unexpectedly accepted: {name}")
            return 0
        elif mode in {"app-mapping", "agent-mapping"}:
            check_runtime_lock()
            root = APP if mode == "app-mapping" else AGENT
            original_reader = read_lock
            lock = original_reader(root)
            for destination, entry in lock["files"].items():
                altered = json.loads(json.dumps(lock))
                other = next(value for value in lock["files"].values() if value["sha256"] != entry["sha256"])
                altered["files"][destination]["from"] = other["from"]
                read_lock = lambda checkout: altered if checkout == root else original_reader(checkout)
                try:
                    check_runtime_lock()
                except PreparedError as exc:
                    require(f"Runtime producer mismatch: {'app' if root == APP else 'agent'} {other['from']}" in str(exc),
                            f"negative {mode} refused for unrelated reason: {exc}")
                else:
                    raise SystemExit(f"negative {mode} unexpectedly accepted: {destination}")
                finally:
                    read_lock = original_reader
            print(f"NEGATIVE {mode}: REFUSED all {len(lock['files'])} cross-source mappings with unchanged consumer bytes/digests")
            return 0
        elif mode in {"inventory-missing", "inventory-extra"}:
            advertised = REQUEST_FIELDS[:]
            if mode == "inventory-missing":
                REQUEST_FIELDS.pop()
            else:
                REQUEST_FIELDS.append("unexpected_advertised_field")
            try:
                wire_inventory()
            except PreparedError as exc:
                require("advertised inventory mismatch" in str(exc),
                        f"negative {mode} refused for unrelated reason: {exc}")
                print(f"NEGATIVE {mode}: REFUSED: {exc}")
            else:
                raise SystemExit(f"negative {mode} unexpectedly accepted")
            finally:
                REQUEST_FIELDS[:] = advertised
            return 0
        elif mode == "registry":
            snapshot, _ = installed_rows()
            require(snapshot["outside_sha256"] == "0" * 64, "registry outsider bytes changed")
        elif mode == "path":
            _, body, _ = extract_row(next(line for line in SUITES.read_text().splitlines(True) if line.startswith(f"app {P2_SUITE} ")))
            rebound, _ = rebind(P2_SUITE, body)
            with tempfile.TemporaryDirectory(prefix="caller-negative-path-") as directory:
                alias = Path(directory) / "app-alias"
                alias.symlink_to(APP, target_is_directory=True)
                try:
                    _DRY_PREFLIGHT.dry_source_preflight(rebound, app=source, agent=agent, runtime=runtime, target=alias, stage="2")
                except _DRY_PREFLIGHT.DryPreflightError as exc:
                    raise PreparedError(str(exc)) from exc
        elif mode in {"duplicate", "concurrency"}:
            original_path, original_digest = SUITES, REGISTRY_SHA256
            with tempfile.TemporaryDirectory(prefix="caller-negative-registry-") as directory:
                candidate = Path(directory) / "suites.conf"
                original = original_path.read_bytes()
                p3_line = next(line for line in original.splitlines(keepends=True) if line.startswith(b"app " + P3_SUITE.encode() + b" "))
                candidate.write_bytes(original + p3_line if mode == "duplicate" else original)
                SUITES = candidate
                REGISTRY_SHA256 = sha256(candidate.read_bytes())
                snapshot, _ = installed_rows()
                if mode == "duplicate":
                    raise SystemExit("duplicate control unexpectedly accepted")
                candidate.write_bytes(candidate.read_bytes() + b"\n")
                try:
                    unchanged_registry(snapshot)
                except PreparedError as exc:
                    raise PreparedError(str(exc)) from exc
                raise SystemExit("concurrency control unexpectedly accepted")
            SUITES, REGISTRY_SHA256 = original_path, original_digest
        else:
            fail(f"unknown negative control: {mode}")
    except PreparedError as exc:
        if mode in {"native", "protected", "tail", "encoded", "binding", "app-mapping", "agent-mapping"}:
            raise SystemExit(f"negative {mode} baseline or mutation setup failed: {exc}") from exc
        print(f"NEGATIVE {mode}: REFUSED: {exc}")
        return 0
    raise SystemExit(f"negative control unexpectedly accepted: {mode}")


def prepare() -> dict[str, Any]:
    source = app_facts()
    agent = facts(AGENT, label="Agent")
    runtime = facts(RUNTIME, label="Runtime")
    freeze_tuple(source, agent, runtime)
    service_recipe, service_bindings, service_checks = normal_service_facts(source, agent, runtime)
    registry, rows = installed_rows()
    tmp = Path(tempfile.mkdtemp(prefix="timeline-final-tuple-", dir=os.environ.get("TMPDIR", "/tmp")))
    candidates: dict[str, Any] = {}
    prepared: dict[str, tuple[str, str, dict[str, str], dict[str, Any]]] = {}
    # Execute both bounded source phases before deeper binding/wrapper checks.
    for name in (P2_SUITE, P3_SUITE):
        outer, body, suffix = extract_row(rows[name])
        rebound, environment = join_environment(
            name,
            body,
            "2" if name == P2_SUITE else "3",
            service_recipe,
        )
        dry = _DRY_PREFLIGHT.dry_source_preflight(
            rebound,
            app=source,
            agent=agent,
            runtime=runtime,
            target=APP,
            stage="2" if name == P2_SUITE else "3",
        )
        candidate_outer = (
            outer[: outer.index("$(bash -c ") + len("$(bash -c ")]
            + shlex.quote(rebound)
            + refresh_wrapper_bindings(name, suffix)
        )
        prepared[name] = candidate_outer, rebound, environment, dry
    wire = wire_inventory()
    for name, (candidate_outer, rebound, environment, dry) in prepared.items():
        preservation = authenticate_candidate(name, rows[name], candidate_outer, rebound, environment=environment)
        syntax = syntax_check(candidate_outer, rebound, tmp, name)
        candidates[name] = {
            "source_row_sha256": registry["rows"][name]["sha256"],
            "rebound": rebound,
            "preservation": preservation,
            "syntax": syntax,
            "wrapper": wrapper_check(candidate_outer, rebound, name),
            "dry_preflight": dry,
        }
    bindings = check_runtime_lock()
    for path in tuple(SOURCE_BINDINGS):
        selected_file(path)
    unchanged_registry(registry)
    require(app_facts() == source, "App normal tuple changed during checks")
    require(facts(AGENT, AGENT_COMMIT, AGENT_TREE, "Agent", parents=AGENT_PARENTS) == agent,
            "Agent normal tuple changed during checks")
    require(facts(RUNTIME, RUNTIME_COMMIT, RUNTIME_TREE, "Runtime", parents=RUNTIME_PARENTS) == runtime,
            "Runtime normal tuple changed during checks")
    custody = custody_requirements()
    result = {
        "status": "PREPARED",
        "run_authorization": "D59_CURRENT_HEADS",
        "authority": "D59 authorizes existing-bench current-head runs; no separate coordinator permission, future snapshot, or final terminal receipt is a pre-run requirement.",
        "execution": "NOT_RUN",
        "commands": {
            "refresh": "PYTHONDONTWRITEBYTECODE=1 python3 current-service-inputs.py --refresh",
            "prepare": "PYTHONDONTWRITEBYTECODE=1 python3 caller-publication.py",
            "prepare_optimized": "PYTHONDONTWRITEBYTECODE=1 python3 -O caller-publication.py",
        },
        "source": source,
        "agent": agent,
        "runtime": runtime,
        "bindings": bindings,
        "service_recipe": {
            "status": service_recipe["status"],
            "source": service_recipe["source"],
            "environment": service_recipe["environment"],
            "interpreters": service_recipe["interpreters"],
            "client_contract": service_recipe["client_contract"],
            "remotion": service_recipe["remotion"],
            "composition": service_recipe["composition"],
            "checks": service_checks,
        },
        "service_bindings": service_bindings,
        "source_bindings": dict(SOURCE_BINDINGS),
        "registry": registry,
        "candidates": candidates,
        "preservation": {
            "p2_cases": 8,
            "p3": "strict D53 request/reply, reads, receipts, history, undo, restart, stage-output, wait, and failure guards retained",
            "live_traffic": "NOT_MEASURED; no journey executed",
            "registry_unchanged": True,
            "outside_rows_unchanged": True,
            "native_and_encoded_stage_bytes": "authenticated unchanged against approved templates",
        },
        "wire_fields": wire,
        "counts": {
            "request_fields": wire["request"]["count"],
            "reply_history_fields": wire["reply_history"]["count"],
            "runtime_app_mappings": bindings["app_consumer"]["file_count"],
            "runtime_agent_mappings": bindings["agent_consumer"]["file_count"],
            "p2_cases": 8,
            "p3_stages": 1,
        },
        "required_custody": custody,
        "readiness": {"status": "SOURCE_PREPARED_ENVIRONMENT_AUTHENTICATED", "owner": "normal existing-service recipe 1304",
                      "reason": "The actual normal working-service inputs are authenticated read-only; this artifact does not start or execute the service.",
                      "prior_refusals": "STOPPED; no alternate acquisition, new child/schema, install, preload, overlay, or historical receipt relabel"},
        "post_request_checks": ["authenticate the actual service snapshot against the frozen source/tree/parents/target/bindings", "retain the full terminal run result; it is evidence after execution"],
        "full_run": {
            "id": "app-U3b-F-reviewed-join-1146-full-1024120556-16138",
            "status": "HISTORICAL_FAIL_NOT_CURRENT_TUPLE",
            "retained_exit_code": 1,
            "claim": "no current-tuple terminal result claimed",
            "source_authentication": "not used for final source authentication; authenticate any service snapshot only after it exists",
        },
        "tmpdir": str(tmp),
    }
    (tmp / "caller-custody.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (ARTIFACT / "caller-custody.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-source", action="store_true", help="run only source/target preflight; never prepare service bindings")
    parser.add_argument("--negative", choices=("wrong-source", "stale", "app", "agent", "runtime", "tree", "target", "path", "body", "receipt", "registry", "duplicate", "concurrency", "native", "protected", "tail", "encoded", "binding", "app-mapping", "agent-mapping", "inventory-missing", "inventory-extra"))
    args = parser.parse_args()
    try:
        if args.negative:
            return negative(args.negative)
        return (source_preflight() if args.dry_source else prepare()) and 0
    except (PreparedError, _DRY_PREFLIGHT.DryPreflightError, _WORKING_BINDING.BindingError) as exc:
        print(str(exc), file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
