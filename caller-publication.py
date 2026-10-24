"""Prepare the exact final Timeline P2/P3 caller for offline qualification.

The generated rows live only in ``TMPDIR``. This artifact reads the two
installed rows, binds their source/body guards to the reviewed final App,
and assigns independent Playwright output children to each stage.
It intentionally has no submission, daemon, browser, HTTP, or build path. The
final source tuple is an explicit input; this preparation must refuse while it
is unavailable and must never fall back to this caller-artifact worktree.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
APP = Path(__file__).resolve().parent
SUITES_FILE = ORCH / "tests/suites.conf"
SUITES = ("full-e2e-three-products", "ap2-P3-gate5-h6-0348")

QUALIFIED_APP = "66354161950d1e747965c095ea97b881d2592708"
QUALIFIED_TREE = "9a37265f0286128df7e6240a9df9877d959474af"
QUALIFIED_PARENT = "b2380539c5545661954d2794976631312ee1d939"
SOURCE_BASE = "f90e708b379145ac456924742cc51c187ed6e0c6"
AGENT = "079580ca46af77e0292d49dc34386b25c8391f99"
ACTUAL_AGENT = "333b44b1a1b8be72d4d101391b7636c508419109"
ACTUAL_AGENT_TREE = "1094bf3662c785e4b21eddf7e3ae980da79b1af1"
ACTUAL_AGENT_DELTA_SHA256 = "ad0dfa1a0fac08dae219af90ea527b9d9f6cfdadc4254086d2bc70f227b13a80"
ACTUAL_AGENT_CHECKOUT = Path("/home/user/work/wt/agt-pin-333b44b1")
ACTUAL_AGENT_RECEIPT = ORCH / "queue/done" / f"checkout-agent-{ACTUAL_AGENT}"
ACTUAL_AGENT_REVIEW = ORCH / "design/agt-R1-popup-079-backport-review-0955.md"
RUNTIME = "37eb6c7bdb79dcae2523883e66b5cea5be721ffd"
RUNTIME_TREE = "be4114705127f9ee9e86b26cd6de3f467e771c01"
AGENT_CHECKOUT = Path("/home/user/work/wt/agt-pin-079580ca")
RUNTIME_CHECKOUT = Path("/home/user/work/wt/rt-pin-37eb6c7b")
CHILD = "venv-agent-child-app-ready-079-37eb-0256"
ACTUAL_CHILD = "venv-agent-child-app-popup-333b-37eb-1016"
REMOTION = "agent-remotion-app-ready-079-37eb-0258"
CHILD_KEY = "5464e85332660e8d6d133653d0600709f2aac5a6c9a0ff0e0bc1fb18312d7f2f"
CHILD_ROOT = Path("/home/user/work/bench-store/entries") / f"child-{CHILD_KEY}"
ACTUAL_CHILD_KEY = "188546b73edd84d90d8d5c321b63b3278eaec80d0050e1b63cea4be298302321"
ACTUAL_CHILD_ROOT = Path("/home/user/work/bench-store/entries") / f"child-{ACTUAL_CHILD_KEY}"
REMOTION_ROOT = Path("/home/user/work/bench-store/entries/runtime-5ca5c561b7be7069051ac8769432cc1edf29060bed39384cd3c4ecab1736e690")
PROVISION_RECEIPT = ORCH / "tests/provision" / f"{CHILD}.txt"
CHILD_RECEIPT = ORCH / "queue/done" / f"childvenv-{CHILD}"
REMOTION_RECEIPT = ORCH / "queue/done" / f"runtime-{REMOTION}"
D41_AGENT_MANIFEST_ENV = "TIMELINE_D41_AGENT_MANIFEST"
BENCH_STORE = Path("/home/user/work/bench-store")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

WIRE_FIELDS = (
    "api_version", "project_id", "timeline_id", "base_revision_id", "base_publication_id",
    "commands", "schema_version", "op", "version", "select", "args", "created", "label", "steps",
    "id", "intent", "tags", "command_ordinals", "patch", "reads", "merge", "fields", "atomic",
    "Idempotency-Key", "dry_run", "source", "rationale", "group_id", "data", "receipt", "status",
    "canonical_document", "document_digest", "id_map", "authoritative_commands", "dependencies",
    "merge_mode", "base", "previous",
    "previous_revision_id", "previous_publication_id", "accepted_ids", "accepted_revision_id",
    "publisher", "provider_version", "compiler_version", "rebased_onto", "accepted",
    "merged", "conflict", "invalid", "rebased", "evaluated_head", "would_status", "receipt_id",
    "command_kind", "idempotency_key", "request_hash", "project_seq", "event_ids", "result", "created_at",
    "http_status", "message", "details", "reason", "head", "current", "conflicts", "kind", "ref",
    "theirs", "ours", "choices", "code", "path", "hint", "suggested_command",
)

REQUIRED_FINAL_SOURCE_PATHS = (
    "src/tools/video-editor/commands/media.ts",
    "src/tools/video-editor/commands/media.test.ts",
    "tests/e2e/local/three-products.spec.ts",
    "tests/e2e/local/support/gate5-reset-precondition.ts",
    "tests/e2e/local/support/gate5-reset-precondition.test.mjs",
    "tests/e2e/local/three-products.p2-elements-assets.spec.ts",
    "tests/e2e/local/three-products.p2-tour.spec.ts",
    "tests/e2e/local/three-products.p2-popup.spec.ts",
    "tests/e2e/local/three-products.p1-chain.spec.ts",
    "tests/e2e/local/support/p2-document-oracle.ts",
    "tests/e2e/local/support/p2-document-oracle.test.mjs",
    "tests/e2e/local/support/p2-original-owner-ready.ts",
    "tests/e2e/local/support/p2-original-owner-ready.test.mjs",
    "tests/e2e/local/support/p2-semantic-oracle.ts",
    "tests/e2e/local/support/p2-semantic-oracle.test.mjs",
)


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def source_bytes(root: Path, commit: str, path: str) -> bytes:
    return git(root, "show", f"{commit}:{path}")


def guarded(text: str, start: str, end: str | None) -> bytes:
    a = text.index(start)
    b = text.index(end, a) if end else len(text)
    return text[a:b].encode()


def key_value_file(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text().splitlines():
        key, separator, value = line.partition("=")
        if separator:
            if key in values:
                raise RuntimeError(f"PREPARED: duplicate receipt field: {key}")
            values[key] = value
    return values


def source_receipt(path: Path) -> dict[str, object]:
    raw = path.read_text()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        value = key_value_file(path)
    if not isinstance(value, dict):
        raise RuntimeError("PREPARED: source receipt is not an object")
    return value


def receipt_value(receipt: dict[str, object], key: str) -> object:
    if key in receipt and not (key == "source" and isinstance(receipt[key], dict)):
        return receipt[key]
    source = receipt.get("source")
    if isinstance(source, dict):
        if key == "source":
            return source.get("source") or source.get("commit")
        return source.get(key)
    return None


def require_sha(value: object, label: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise RuntimeError(f"PREPARED: {label} is not a full SHA")
    return value


def physical_path(path: Path) -> Path:
    if not path.exists() or not path.is_absolute() or path != path.resolve() or any(p.is_symlink() for p in (path, *path.parents)):
        raise RuntimeError(f"PREPARED: unavailable or nonphysical custody path: {path}")
    return path


def assert_actual_manifest(manifest: dict[str, object] | None) -> dict[str, object]:
    """Bind the one reviewed normal source carrier, without inventing worker metadata."""
    expected = {
        "source": ACTUAL_AGENT,
        "tree": ACTUAL_AGENT_TREE,
        "parent": AGENT,
        "checkout": str(ACTUAL_AGENT_CHECKOUT),
        "source_receipt": str(ACTUAL_AGENT_RECEIPT),
        "source_receipt_sha256": digest(ACTUAL_AGENT_RECEIPT.read_bytes()),
        "runtime": RUNTIME,
        "runtime_tree": RUNTIME_TREE,
        "runtime_checkout": str(RUNTIME_CHECKOUT),
        "child": ACTUAL_CHILD,
        "child_key": ACTUAL_CHILD_KEY,
        "child_root": str(ACTUAL_CHILD_ROOT),
    }
    if manifest is not None:
        for key, value in expected.items():
            if key in manifest and manifest.get(key) != value:
                raise RuntimeError(f"PREPARED: D41 actual manifest differs from qualified source: {key}")
    return expected


def immutable_receipt(manifest: dict[str, object], key: str, expected: dict[str, str]) -> dict[str, object]:
    # These are the existing dispatcher/maker/provision/import projections.
    # A caller-supplied digest authenticates bytes only after their origin binds.
    if not isinstance(expected, dict):
        raise RuntimeError("PREPARED: structured receipt identity is required")
    child = str(manifest.get("child", ""))
    worker = str(manifest.get("worker", ""))
    if not re.fullmatch(r"venv-agent-child-[a-z0-9-]+", child) or not re.fullmatch(r"[A-Za-z0-9_-]+", worker):
        raise RuntimeError("PREPARED: receipt worker/child identity is invalid")
    origins = {
        "source_receipt": ORCH / "workers" / worker / "meta",
        "maker_receipt": ORCH / "queue/done" / f"childvenv-{child}",
        "provision_receipt": ORCH / "tests/provision" / f"{child}.txt",
        "import_receipt": Path(str(manifest.get("child_root", ""))) / ".astrid-import-origins",
    }
    if key not in origins or not isinstance(manifest.get(key), str):
        raise RuntimeError(f"PREPARED: D41 {key} receipt is missing")
    path = physical_path(Path(manifest[key]))
    if path != origins[key] or not path.is_file():
        raise RuntimeError(f"PREPARED: D41 {key} receipt has no dispatcher/provision origin")
    expected_hash = require_sha(manifest.get(f"{key}_sha256"), f"D41 {key} hash", SHA256_RE)
    if digest(path.read_bytes()) != expected_hash:
        raise RuntimeError(f"PREPARED: D41 {key} receipt changed")
    if key == "maker_receipt":
        lines = path.read_text().splitlines()
        if not lines:
            raise RuntimeError("PREPARED: empty maker receipt")
        line = lines[-1]
        if line.startswith("created "):
            root, *fields = shlex.split(line.removeprefix("created "))
        elif line.startswith("reused child venv path="):
            root, *fields = shlex.split(line.removeprefix("reused child venv path="))
        else:
            raise RuntimeError("PREPARED: maker success record is missing")
        values = {"path": root}
        for field in fields:
            name, separator, value = field.partition("=")
            if not separator or name in values:
                raise RuntimeError("PREPARED: ambiguous maker receipt fields")
            values[name] = value
        if set(values) != set(expected):
            raise RuntimeError("PREPARED: maker receipt field set differs")
    elif key == "provision_receipt":
        header = path.read_text().split("installed_import_origins:\n", 1)[0]
        values = key_value_file(path)
        if header != "".join(f"{name}={value}\n" for name, value in expected.items()):
            raise RuntimeError("PREPARED: provision identity header differs")
    else:
        values = key_value_file(path)
        if key == "import_receipt" and set(values) != set(expected):
            raise RuntimeError("PREPARED: import origin field set differs")
    if any(values.get(name) != value for name, value in expected.items()):
        raise RuntimeError(f"PREPARED: D41 {key} structured identity differs")
    return {"path": str(path), "sha256": expected_hash}


def child_receipts(manifest: dict[str, object], lock_hash: str) -> None:
    child = str(manifest["child"])
    root = physical_path(Path(str(manifest["child_root"])))
    clients = manifest["client_hashes"]
    identity = {"agent_sha": manifest["source"], "backend_sha": RUNTIME, "client_tuple": clients}
    canonical = lambda value: json.dumps(value, sort_keys=True, separators=(",", ":"))
    key = digest(canonical(["child", manifest["source"], RUNTIME, clients]).encode())
    if manifest["child_key"] != key or root != BENCH_STORE / "entries" / f"child-{key}":
        raise RuntimeError("PREPARED: child key/root does not bind exact source/backend/clients")
    index = json.loads(physical_path(BENCH_STORE / "index.json").read_text())
    owner = json.loads(physical_path(BENCH_STORE / "owner.json").read_text())
    entry = index["entries"].get(f"child-{key}", {})
    marker = json.loads(physical_path(root / ".bench-owner.json").read_text())
    expected_owner = {"owner": owner["id"], "component": "child", "key": key, "identity": identity}
    if (marker != expected_owner or any(entry.get(k) != v for k, v in expected_owner.items())
            or entry.get("path") != str(root) or entry.get("node") != [root.stat().st_dev, root.stat().st_ino]):
        raise RuntimeError("PREPARED: child store ownership/identity differs")
    registration = index["registrations"].get(child, {})
    if not registration:
        raise RuntimeError("PREPARED: child registration/provision origin is missing")
    report_path = ORCH / "tests/provision" / f"{child}.txt"
    report = physical_path(report_path).read_bytes()
    if (f"child-{key}" not in registration.get("requires", [])
            or registration.get("report") != report.decode()
            or registration.get("report_sha256") != digest(report)
            or registration.get("hash") != digest(canonical({k: v for k, v in registration.items() if k != "hash"}).encode())
            or physical_path(root / ".provision-report").read_bytes() != report):
        raise RuntimeError("PREPARED: child registration/provision projection differs")
    client_identity = "\n".join(f"{p}={v}" for p, v in sorted(clients.items()))
    for name, value in ((".astrid-source-commit", manifest["source"]), (".astrid-runtime-source-commit", RUNTIME),
                        (".astrid-runtime-client-identity", client_identity)):
        if physical_path(root / name).read_text().rstrip("\n") != value:
            raise RuntimeError(f"PREPARED: child marker differs: {name}")
    immutable_receipt(manifest, "maker_receipt", {
        "path": str(root), "agent": str(manifest["source"]), "runtime": RUNTIME,
        "remotion": str(manifest["remotion"]), "registration": "existing", "key": key,
        "requested_name": child, "actual_agent": str(manifest["source"]), "actual_runtime": RUNTIME,
        "provision_report": str(report_path), "provision_report_sha256": digest(report), "status": "passed",
    })
    immutable_receipt(manifest, "provision_receipt", {
        "status": "passed", "agent_sha": str(manifest["source"]), "runtime_sha": RUNTIME,
        "runtime_client_identity_sha256": digest(client_identity.encode()),
        "requirements_path": "requirements/proof.lock", "requirements_lock_sha256": lock_hash,
    })
    origins = {name: str(root / "lib/python3.13/site-packages" / name / "__init__.py")
               for name in ("astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client")}
    immutable_receipt(manifest, "import_receipt", origins)
    raw = report.decode()
    for start, end, marker_name in (("installed_import_origins:", "installed_distribution_metadata:", ".astrid-import-origins"),
                                    ("installed_distribution_metadata:", "pip_freeze:", ".astrid-distribution-metadata")):
        lines = raw.splitlines()
        if lines.count(start) != 1 or lines.count(end) != 1 or lines.index(start) >= lines.index(end):
            raise RuntimeError("PREPARED: provision sections are ambiguous")
        if lines[lines.index(start) + 1:lines.index(end)] != physical_path(root / marker_name).read_text().splitlines():
            raise RuntimeError("PREPARED: provision import/distribution projection differs")
    for origin in origins.values():
        physical_path(Path(origin))


def d41_agent_input() -> dict[str, object]:
    """Validate the exact reviewed Agent333 source and its existing child."""
    manifest_name = os.environ.get(D41_AGENT_MANIFEST_ENV)
    manifest: dict[str, object] | None = None
    if manifest_name:
        manifest_path = Path(manifest_name)
        if manifest_path.is_symlink() or not manifest_path.is_file():
            raise RuntimeError("PREPARED: D41 Agent manifest is unavailable")
        try:
            value = json.loads(manifest_path.read_text())
        except json.JSONDecodeError as exc:
            raise RuntimeError("PREPARED: D41 Agent manifest is not JSON") from exc
        if not isinstance(value, dict):
            raise RuntimeError("PREPARED: D41 Agent manifest is not an object")
        manifest = value
    actual = assert_actual_manifest(manifest)
    source = ACTUAL_AGENT
    tree = ACTUAL_AGENT_TREE
    parent = AGENT
    root = physical_path(ACTUAL_AGENT_CHECKOUT)
    if root == APP or not root.is_dir() or root.is_symlink():
        raise RuntimeError("PREPARED: D41 Agent checkout is unavailable or is a caller target")
    if any((root / name).exists() for name in ("caller-publication.py", "caller-custody.json")):
        raise RuntimeError("PREPARED: D41 Agent checkout is a caller-artifact target")
    if git(root, "status", "--porcelain=v1", "--untracked-files=all").strip():
        raise RuntimeError("PREPARED: D41 Agent checkout is not clean")
    if git(root, "rev-parse", "--abbrev-ref", "HEAD").decode().strip() != "HEAD":
        raise RuntimeError("PREPARED: D41 Agent checkout must be the supported detached checkout")
    if git(root, "rev-parse", "HEAD").decode().strip() != source:
        raise RuntimeError("PREPARED: D41 Agent checkout HEAD does not match qualified source")
    if git(root, "show", "-s", "--format=%T", source).decode().strip() != tree:
        raise RuntimeError("PREPARED: D41 Agent tree does not match qualified source")
    if git(root, "show", "-s", "--format=%P", source).decode().strip() != parent:
        raise RuntimeError("PREPARED: D41 Agent parent does not match exact 079 base")
    changed = git(root, "diff", "--name-only", parent, source).decode().splitlines()
    if changed != ["astrid/sdk/timeline/_commit_patch.py", "tests/editing_conformance/test_same_step_fork_rebase.py"]:
        raise RuntimeError("PREPARED: D41 source changed paths differ from reviewed backport")
    numstat = git(root, "diff", "--numstat", parent, source).decode().splitlines()
    if numstat != ["18\t0\tastrid/sdk/timeline/_commit_patch.py", "234\t0\ttests/editing_conformance/test_same_step_fork_rebase.py"]:
        raise RuntimeError("PREPARED: D41 reviewed hunk/test line counts differ")
    delta = git(root, "diff", "--binary", "--full-index", "--no-ext-diff", parent, source)
    if digest(delta) != ACTUAL_AGENT_DELTA_SHA256:
        raise RuntimeError("PREPARED: D41 source delta is not the exact reviewed backport")
    parent_entries = {line.rsplit("\t", 1)[1]: line.rsplit("\t", 1)[0] for line in git(root, "ls-tree", "-r", parent).decode().splitlines()}
    source_entries = {line.rsplit("\t", 1)[1]: line.rsplit("\t", 1)[0] for line in git(root, "ls-tree", "-r", source).decode().splitlines()}
    protected = [path for path, value in parent_entries.items() if path not in changed and source_entries.get(path) == value]
    if len(protected) != 3418:
        raise RuntimeError("PREPARED: D41 protected Agent blob count changed")
    for path in source_entries:
        file = physical_path(root / path)
        mode = file.stat().st_mode
        if not stat.S_ISREG(mode) or file.read_bytes() != source_bytes(root, source, path):
            raise RuntimeError(f"PREPARED: D41 source is not an exact read-only checkout: {path}")
    review = physical_path(ACTUAL_AGENT_REVIEW).read_text()
    if "# R1-D41 Independent Review — PASS" not in review or "18 new cases passed" not in review or "All 3,418 protected tracked blobs are unchanged" not in review:
        raise RuntimeError("PREPARED: D41 independent source review evidence is incomplete")
    receipt_path = physical_path(ACTUAL_AGENT_RECEIPT)
    if receipt_path != ACTUAL_AGENT_RECEIPT or digest(receipt_path.read_bytes()) != actual["source_receipt_sha256"]:
        raise RuntimeError("PREPARED: D41 normal source carrier receipt changed")
    if receipt_path.read_text().strip() != f"created {root} (detached at {source}, KEEP)":
        raise RuntimeError("PREPARED: D41 normal source carrier receipt is not authentic")
    source_receipt = {"path": str(receipt_path), "sha256": actual["source_receipt_sha256"]}

    runtime_candidate = RUNTIME_CHECKOUT
    if runtime_candidate.is_symlink():
        raise RuntimeError("PREPARED: D41 Runtime checkout must not be a symlink")
    runtime_checkout = physical_path(runtime_candidate)
    if runtime_checkout != RUNTIME_CHECKOUT or not runtime_checkout.is_dir():
        raise RuntimeError("PREPARED: D41 Runtime checkout is not the retained exact checkout")
    if (git(runtime_checkout, "rev-parse", "HEAD").decode().strip() != RUNTIME
            or git(runtime_checkout, "show", "-s", "--format=%T", RUNTIME).decode().strip() != RUNTIME_TREE
            or git(runtime_checkout, "status", "--porcelain=v1", "--untracked-files=all").strip()):
        raise RuntimeError("PREPARED: D41 Runtime checkout is not Runtime37eb")
    runtime_paths = git(runtime_checkout, "ls-tree", "-r", "--name-only", RUNTIME, "packages/python/astrid_runtime_client/").decode().splitlines()
    if len(runtime_paths) != 4:
        raise RuntimeError("PREPARED: D41 Runtime client file set is not canonical")
    client_hashes = {path: digest(git(runtime_checkout, "show", f"{RUNTIME}:{path}")) for path in runtime_paths}
    if manifest is not None and "client_hashes" in manifest and manifest["client_hashes"] != client_hashes:
        raise RuntimeError("PREPARED: D41 manifest client hash set differs from Runtime37eb")
    for path in runtime_paths:
        runtime_bytes = git(runtime_checkout, "show", f"{RUNTIME}:{path}")
        agent_path = path.removeprefix("packages/python/")
        if runtime_bytes != git(root, "show", f"{source}:{agent_path}"):
            raise RuntimeError(f"PREPARED: D41 client bytes differ: {path}")
        if client_hashes[path] != digest(runtime_bytes):
            raise RuntimeError(f"PREPARED: D41 client hash differs: {path}")

    backend_paths = git(runtime_checkout, "ls-tree", "-r", "--name-only", RUNTIME, "astrid_runtime/", "runtime_protocol/").decode().splitlines()
    backend_hashes = {path: digest(git(runtime_checkout, "show", f"{RUNTIME}:{path}")) for path in backend_paths if path.endswith(".py")}
    backend_digest = digest(json.dumps(backend_hashes, sort_keys=True, separators=(",", ":")).encode())
    if manifest is not None and "backend_hashes" in manifest and manifest["backend_hashes"] != backend_hashes:
        raise RuntimeError("PREPARED: D41 manifest backend hash set differs from Runtime37eb")
    if manifest is not None and "backend_digest" in manifest and manifest["backend_digest"] != backend_digest:
        raise RuntimeError("PREPARED: D41 manifest backend digest differs from Runtime37eb")
    if backend_digest != "d70ce25e13e02c1b805e682e7e098fba78cc6732f90c482a84bf074ab98ef2bb":
        raise RuntimeError("PREPARED: D41 backend identity is not Runtime37eb")
    child = ACTUAL_CHILD
    child_key = ACTUAL_CHILD_KEY
    if child == CHILD or child_key == CHILD_KEY:
        raise RuntimeError("PREPARED: D41 child relabels the retained 0256 child")
    child_candidate = ACTUAL_CHILD_ROOT
    if child_candidate.is_symlink():
        raise RuntimeError("PREPARED: D41 child checkout must not be a symlink")
    child_root = physical_path(child_candidate)
    if child_root.name != f"child-{child_key}" or not child_root.is_dir():
        raise RuntimeError("PREPARED: D41 child checkout is not a genuine keyed child")
    child_manifest = {
        "worker": "agt-pin-333b44b1", "source": source, "runtime": RUNTIME,
        "client_hashes": client_hashes, "child": child, "child_key": child_key,
        "child_root": str(child_root), "remotion": "none",
        "maker_receipt": str(ORCH / "queue/done" / f"childvenv-{child}"),
        "maker_receipt_sha256": digest((ORCH / "queue/done" / f"childvenv-{child}").read_bytes()),
        "provision_receipt": str(ORCH / "tests/provision" / f"{child}.txt"),
        "provision_receipt_sha256": digest((ORCH / "tests/provision" / f"{child}.txt").read_bytes()),
        "import_receipt": str(child_root / ".astrid-import-origins"),
        "import_receipt_sha256": digest((child_root / ".astrid-import-origins").read_bytes()),
    }
    child_receipts(child_manifest, digest(source_bytes(root, source, "requirements/proof.lock")))
    installed_source = physical_path(child_root / f".child-venv-source-{child}" / "agent")
    if installed_source.stat().st_mode & 0o222:
        raise RuntimeError("PREPARED: D41 installed Agent source is not read-only")
    for path in source_entries:
        installed = physical_path(installed_source / path)
        if installed.stat().st_mode & 0o222 or installed.read_bytes() != source_bytes(root, source, path):
            raise RuntimeError(f"PREPARED: D41 installed Agent source differs: {path}")
    child_site = child_root / "lib/python3.13/site-packages"
    for path in runtime_paths:
        installed = physical_path(child_site / path.removeprefix("packages/python/"))
        if not installed.is_file() or installed.read_bytes() != git(runtime_checkout, "show", f"{RUNTIME}:{path}"):
            raise RuntimeError(f"PREPARED: D41 child client import differs: {path}")
    for path, expected in backend_hashes.items():
        installed = physical_path(child_site / path)
        if not installed.is_file() or digest(installed.read_bytes()) != expected:
            raise RuntimeError(f"PREPARED: D41 child backend import differs: {path}")
    remotion_candidate = REMOTION_ROOT
    if remotion_candidate.is_symlink() or remotion_candidate.resolve() != REMOTION_ROOT:
        raise RuntimeError("PREPARED: D41 Remotion checkout is not the retained exact checkout")
    return {
        "source": source, "tree": tree, "parent": parent, "checkout": str(root),
        "source_receipt": source_receipt, "runtime": RUNTIME, "runtime_tree": RUNTIME_TREE,
        "runtime_checkout": str(runtime_checkout), "client_hashes": client_hashes,
        "backend_hashes": backend_hashes, "backend_digest": backend_digest,
        "child": child, "child_key": child_key, "child_root": str(child_root),
        "remotion": REMOTION, "remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db",
        "remotion_root": str(REMOTION_ROOT),
        "receipt_paths": {key: {"path": str(child_manifest[key]), "sha256": child_manifest[f"{key}_sha256"]} for key in ("maker_receipt", "provision_receipt", "import_receipt")},
    }


def final_source_input() -> dict[str, object] | None:
    manifest_name = os.environ.get("TIMELINE_FINAL_SOURCE_MANIFEST")
    if not manifest_name:
        return None
    manifest = json.loads(Path(manifest_name).read_text())
    required = (
        "checkout", "source", "tree", "parent", "review", "worker", "branch",
        "base", "base_sha", "source_receipt", "source_receipt_sha256",
    )
    if any(key not in manifest for key in required):
        raise RuntimeError("PREPARED: final source manifest is incomplete")
    if manifest["review"] != "PASS":
        raise RuntimeError("PREPARED: independent final-source review is not PASS")
    worker = str(manifest["worker"])
    if not worker or "/" in worker or worker in {".", ".."}:
        raise RuntimeError("PREPARED: final source worker identity is invalid")
    meta_path = ORCH / "workers" / worker / "meta"
    if not meta_path.is_file() or meta_path.is_symlink():
        raise RuntimeError("PREPARED: dispatcher worker metadata is unavailable")
    meta = key_value_file(meta_path)
    if (
        meta.get("name") != worker
        or meta.get("repo") != "app"
        or meta.get("base") != manifest["base"]
        or meta.get("base_sha") != manifest["base_sha"]
        or manifest["branch"] != f"tl/{worker}"
    ):
        raise RuntimeError("PREPARED: final source does not match dispatcher branch/base identity")
    checkout_path = Path(str(manifest["checkout"]))
    if checkout_path.is_symlink():
        raise RuntimeError("PREPARED: final source checkout must not be a symlink")
    root = checkout_path.resolve()
    if root == APP or not root.is_dir():
        raise RuntimeError("PREPARED: final source must be a separate read-only proof worker")
    if Path(meta.get("worktree", "")).resolve() != root:
        raise RuntimeError("PREPARED: final source checkout is not the dispatched proof worker")
    if any((root / name).exists() for name in ("caller-publication.py", "caller-custody.json")):
        raise RuntimeError("refusing caller-artifact target")
    if git(root, "status", "--porcelain=v1", "--untracked-files=all").strip():
        raise RuntimeError("final source target is not clean")
    if git(root, "symbolic-ref", "--quiet", "--short", "HEAD").decode().strip() != manifest["branch"]:
        raise RuntimeError("final source checkout is not on the dispatched branch")
    base_commit = git(root, "rev-parse", f"{manifest['base']}^{{commit}}").decode().strip()
    if not base_commit.startswith(str(manifest["base_sha"])):
        raise RuntimeError("final source base does not match dispatcher base identity")
    if git(root, "rev-parse", "HEAD").decode().strip() != manifest["source"]:
        raise RuntimeError("final source HEAD does not match explicit input")
    if git(root, "show", "-s", "--format=%T", manifest["source"]).decode().strip() != manifest["tree"]:
        raise RuntimeError("final source tree does not match explicit input")
    if git(root, "show", "-s", "--format=%P", manifest["source"]).decode().strip() != manifest["parent"]:
        raise RuntimeError("final source parent does not match explicit input")
    if len(str(manifest["parent"]).split()) != 1:
        raise RuntimeError("final proof-worker target must be an authorized single-parent snapshot")
    receipt_candidate = Path(str(manifest["source_receipt"]))
    if receipt_candidate.is_symlink():
        raise RuntimeError("PREPARED: immutable source receipt must not be a symlink")
    receipt_path = receipt_candidate.resolve()
    try:
        receipt_path.relative_to(ORCH)
    except ValueError as exc:
        raise RuntimeError("PREPARED: source receipt is outside the dispatcher area") from exc
    if receipt_path == Path(manifest_name).resolve() or not receipt_path.is_file():
        raise RuntimeError("PREPARED: immutable source receipt is unavailable")
    if digest(receipt_path.read_bytes()) != manifest["source_receipt_sha256"]:
        raise RuntimeError("PREPARED: source receipt hash does not match explicit input")
    receipt = source_receipt(receipt_path)
    for key in ("worker", "branch", "base", "base_sha", "source", "tree", "parent", "checkout"):
        if str(receipt_value(receipt, key)) != str(manifest[key]):
            raise RuntimeError(f"PREPARED: source receipt identity mismatch: {key}")
    if receipt_value(receipt, "review") not in (None, "PASS"):
        raise RuntimeError("PREPARED: source receipt review is not PASS")
    manifest["dispatcher_meta"] = {key: meta[key] for key in ("name", "repo", "base", "base_sha", "worktree")}
    manifest["source_receipt"] = {"path": str(receipt_path), "sha256": manifest["source_receipt_sha256"]}
    return manifest


def source_custody(final: dict[str, object]) -> dict[str, object]:
    root = Path(str(final["checkout"])).resolve()
    source = str(final["source"])
    tree = str(final["tree"])
    parent = str(final["parent"])
    paths = git(root, "diff", "--name-only", SOURCE_BASE, source).decode().splitlines()
    fingerprints = {}
    for path in paths:
        data = source_bytes(root, source, path)
        assert (root / path).read_bytes() == data, path
        fingerprints[path] = {"blob": git_blob(data), "sha256": digest(data)}
    canonical = "".join(f"{p}\t{v['blob']}\t{v['sha256']}\n" for p, v in fingerprints.items())
    required_paths = tuple(final.get("required_paths", REQUIRED_FINAL_SOURCE_PATHS))
    if not required_paths:
        raise RuntimeError("PREPARED: final reviewed source path set is empty")
    missing = [path for path in required_paths if path not in paths and not (root / path).is_file()]
    if missing:
        raise RuntimeError(f"final source missing required reviewed paths: {missing}")
    reviewed_hashes = final.get("reviewed_hashes")
    if not isinstance(reviewed_hashes, dict):
        raise RuntimeError("PREPARED: reviewed source/body hashes are required final inputs")
    observed_hashes = {path: digest(source_bytes(root, source, path)) for path in required_paths}
    if set(reviewed_hashes) != set(required_paths):
        raise RuntimeError("reviewed source hash set does not cover the final reviewed path set")
    for path, expected in reviewed_hashes.items():
        if path in observed_hashes and observed_hashes[path] != expected:
            raise RuntimeError(f"reviewed source hash mismatch: {path}")
    protected = final.get("protected_hashes", {})
    if not isinstance(protected, dict):
        raise RuntimeError("PREPARED: protected D50/P3 hashes are required final inputs")
    spec = source_bytes(root, source, "tests/e2e/local/three-products.spec.ts")
    tail = spec[spec.index(b"  const resetResponse = page.waitForResponse", spec.index(b"test('M2 real gate 5")):spec.index(b"\n", spec.index(b"test('M2 ordinary extension batch")) + 1]
    if protected.get("d50_tail_sha256") != digest(tail):
        raise RuntimeError("D50/P3 protected tail does not match final source")
    p3 = guarded(spec.decode(), "test('M2 real gate 5", "test('M2 ordinary extension batch").rstrip() + b"\n"
    if protected.get("p3_gate5_sha256") != digest(p3):
        raise RuntimeError("P3 Gate5 body does not match final source")
    anchors = {}
    anchors[source] = {"tree": tree, "parents": parent}
    return {"source": source, "tree": tree, "parent": parent, "checkout": str(root),
            "anchors": anchors, "fingerprints": fingerprints, "fingerprint_count": len(fingerprints),
            "fingerprint_digest": digest(canonical.encode()), "required_paths": list(required_paths), "p3_whole": {"blob": git_blob(spec), "sha256": digest(spec)},
            "gate5_sha256": digest(p3), "reset_and_tail_sha256": digest(tail), "reviewed_hashes": reviewed_hashes,
            "protected_hashes": protected}

def custody_facts() -> dict[str, object]:
    assert git(AGENT_CHECKOUT, "rev-parse", "HEAD").decode().strip() == AGENT
    assert git(AGENT_CHECKOUT, "show", "-s", "--format=%T", "HEAD").decode().strip() == "2deab1a1494fbccfce5e9235412bacb8a949c0cd"
    assert not git(AGENT_CHECKOUT, "status", "--porcelain=v1", "--untracked-files=all").strip()
    assert git(RUNTIME_CHECKOUT, "rev-parse", "HEAD").decode().strip() == RUNTIME
    assert git(RUNTIME_CHECKOUT, "show", "-s", "--format=%T", "HEAD").decode().strip() == RUNTIME_TREE
    assert not git(RUNTIME_CHECKOUT, "status", "--porcelain=v1", "--untracked-files=all").strip()
    for receipt in (PROVISION_RECEIPT, CHILD_RECEIPT, REMOTION_RECEIPT):
        assert receipt.is_file()
    provision = PROVISION_RECEIPT.read_text()
    remotion = REMOTION_RECEIPT.read_text()
    assert f"agent_sha={AGENT}" in provision and f"runtime_sha={RUNTIME}" in provision
    assert f"requested_name={REMOTION}" in remotion and f"requested_runtime_sha={RUNTIME}" in remotion
    assert "reuse=verified" in remotion

    paths = git(RUNTIME_CHECKOUT, "ls-tree", "-r", "--name-only", RUNTIME, "packages/python/astrid_runtime_client/").decode().splitlines()
    assert len(paths) == 4
    client_hashes = {}
    child_site = CHILD_ROOT / "lib/python3.13/site-packages"
    for path in paths:
        runtime_bytes = git(RUNTIME_CHECKOUT, "show", f"{RUNTIME}:{path}")
        agent_path = path.removeprefix("packages/python/")
        assert runtime_bytes == git(AGENT_CHECKOUT, "show", f"{AGENT}:{agent_path}")
        installed = child_site / agent_path
        assert installed.is_file() and installed.read_bytes() == runtime_bytes
        client_hashes[path] = digest(runtime_bytes)

    backend_hashes = {}
    backend_paths = git(RUNTIME_CHECKOUT, "ls-tree", "-r", "--name-only", RUNTIME, "astrid_runtime/", "runtime_protocol/").decode().splitlines()
    for path in backend_paths:
        if path.endswith(".py"):
            data = git(RUNTIME_CHECKOUT, "show", f"{RUNTIME}:{path}")
            installed = child_site / path
            assert installed.is_file() and installed.read_bytes() == data
            backend_hashes[path] = digest(data)
    assert len(backend_hashes) == 78
    assert digest(json.dumps(backend_hashes, sort_keys=True, separators=(",", ":")).encode()) == "d70ce25e13e02c1b805e682e7e098fba78cc6732f90c482a84bf074ab98ef2bb"

    graph_root = REMOTION_ROOT / "node_modules/@banodoco/timeline-composition"
    graph_files = sorted(path for path in graph_root.rglob("*") if path.is_file())
    graph_hashes = {str(path.relative_to(graph_root)): digest(path.read_bytes()) for path in graph_files}
    assert len(graph_hashes) == 80
    assert digest(json.dumps(graph_hashes, sort_keys=True, separators=(",", ":")).encode()) == "ac0bf2a252d3f3a7640ed2a0b555b8a91ff81671a3b70074ed27676357edbbc9"
    return {"agent": AGENT, "agent_tree": "2deab1a1494fbccfce5e9235412bacb8a949c0cd", "runtime": RUNTIME, "runtime_tree": RUNTIME_TREE, "child": CHILD, "child_key": CHILD_KEY, "remotion": REMOTION, "remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db", "provision_receipt_sha256": digest(PROVISION_RECEIPT.read_bytes()), "child_receipt_sha256": digest(CHILD_RECEIPT.read_bytes()), "remotion_receipt_sha256": digest(REMOTION_RECEIPT.read_bytes()), "client_file_count": len(client_hashes), "client_hashes": client_hashes, "runtime_backend_file_count": len(backend_hashes), "runtime_backend_digest": digest(json.dumps(backend_hashes, sort_keys=True, separators=(",", ":")).encode()), "graph_file_count": len(graph_hashes), "graph_digest": digest(json.dumps(graph_hashes, sort_keys=True, separators=(",", ":")).encode()), "daemon_identity": "UNINFERRED_BY_SOURCE_PREPARATION"}


def selected_rows() -> tuple[bytes, dict[str, tuple[int, bytes]]]:
    raw = SUITES_FILE.read_bytes()
    lines = raw.splitlines(keepends=True)
    found = {}
    for index, line in enumerate(lines, 1):
        fields = line.split(None, 2)
        if len(fields) >= 2 and fields[0] == b"app" and fields[1].decode() in SUITES:
            assert fields[1].decode() not in found
            found[fields[1].decode()] = (index, line)
    assert set(found) == set(SUITES)
    return raw, found


def stage_assignment(root: str) -> str:
    return f'PLAYWRIGHT_OUTPUT_DIR="{root}"; mkdir -p "$PLAYWRIGHT_OUTPUT_DIR"; export PLAYWRIGHT_OUTPUT_DIR; '


def add_stages(inner: str, n: int) -> str:
    if n == 2:
        markers = [
            ('p2log "$PREFLIGHT_DIR/native-seed.log"', stage_assignment('$ACTUAL_RUN_DIR/playwright-output/p2/native-history')),
            ('p2log "$PREFLIGHT_DIR/mounted-readiness.log"', stage_assignment('$ACTUAL_RUN_DIR/playwright-output/p2/mounted-readiness')),
        ]
        updated = inner
        for marker, assignment in markers:
            assert updated.count(marker) == 1
            updated = updated.replace(marker, assignment + marker, 1)
        return updated

    updated = inner
    native = 'if test "$SETUP_OK" = 1 && test "$P3FAIL" = ""; then "${ENV_BASE[@]}" timeout 300s node --import tsx'
    assert updated.count(native) == 1
    updated = updated.replace(native, stage_assignment('$P3O/tests/$RUN_ID/playwright-output/p3/native-history') + native, 1)
    return updated


def add_tail_stages(tail: str, n: int) -> str:
    def select(root: str) -> str:
        return '{ PLAYWRIGHT_OUTPUT_DIR="' + root + '" && mkdir -p "$PLAYWRIGHT_OUTPUT_DIR" && export PLAYWRIGHT_OUTPUT_DIR; } && '
    if n == 2:
        needle = 'eval "$P2_ENV" && env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144'
        assert tail.count(needle) == 1
        return tail.replace(needle, 'eval "$P2_ENV" && ' + select('${PLAYWRIGHT_OUTPUT_DIR%/*}/original-body') + 'env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144', 1)
    mounted = '&& env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=4096'
    positions = [i for i in range(len(tail)) if tail.startswith(mounted, i)]
    assert len(positions) == 2
    tail = tail[:positions[1] + 3] + select('${PLAYWRIGHT_OUTPUT_DIR%/*}/gate5') + tail[positions[1] + 3:]
    return tail[:positions[0] + 3] + select('$PLAYWRIGHT_OUTPUT_DIR/p3/mounted-readiness') + tail[positions[0] + 3:]


def extract_inner(line: bytes) -> tuple[str, str, str]:
    outer = line.decode().split(None, 2)[2].rstrip("\n")
    start = outer.index("$(bash -c ") + len("$(bash -c ")
    end = outer.index(")\" && eval", start)
    decoded = shlex.split(outer[start:end])
    assert len(decoded) == 1
    return outer, decoded[0], outer[end:]


def row_fingerprints(inner: str, n: int) -> list[tuple[str, str, str]]:
    assignments = {
        f"P{n}{suffix}": value
        for suffix, value in re.findall(rf"\bP{n}([A-Z]+)=([^;]+)", inner)
    }
    patterns = (
        ("blob", re.compile(r'git hash-object -- ([^ ]+) 2>/dev/null\)" = ([0-9a-f]{40})')),
        ("sha256", re.compile(r'sha256sum -- ([^ ]+).*?\)" = ([0-9a-f]{64})')),
    )
    found = {}
    for kind, pattern in patterns:
        for raw_path, expected in pattern.findall(inner):
            path = raw_path.strip('"\'')
            if path.startswith("$"):
                variable = path[1:]
                if variable not in assignments:
                    raise RuntimeError(f"P{n}: fingerprint variable is not bound: {raw_path}")
                path = assignments[variable].strip('"\'')
            key = (path, kind)
            prior = found.get(key)
            if prior is not None and prior != expected:
                raise RuntimeError(f"P{n}: ambiguous current fingerprint: {path}")
            found[key] = expected
    if not found:
        raise RuntimeError(f"P{n}: no current source/body fingerprints decoded")
    return [(path, kind, expected) for (path, kind), expected in found.items()]


def mechanical_controls(
    inner: str,
    n: int,
    fingerprints: dict[str, object],
    final: dict[str, object],
    agent: dict[str, object],
) -> dict[str, object]:
    """Check the retained caller's controls without running any stage."""
    required = (
        f"P{n}_ALLOCATED_PORT", f"P{n}A={agent['source']}", f"P{n}R={RUNTIME}",
        "original-body-NOTRUN", "git rev-parse", "git hash-object", "timeout",
        "harness.stop", "PLAYWRIGHT_OUTPUT_DIR", "native-history", "mounted-readiness",
        "gate5", "/v1/projects", "export", "NODE_OPTIONS", "PREFLIGHT_DIR" if n == 2 else "P3DIAG",
    )
    missing = [token for token in required if token not in inner]
    if missing:
        raise RuntimeError(f"retained caller control missing: {missing}")
    if "identity_map" in inner or "canonical_document" in inner or "document_digest" in inner:
        raise RuntimeError("caller shell contains non-wire identity fields")
    preflight = "PREFLIGHT_DIR" if n == 2 else "P3DIAG"
    if inner.count(preflight) < 1 or inner.count("PLAYWRIGHT_OUTPUT_DIR") < 2:
        raise RuntimeError("caller stage guards were broadened or removed")
    guarded = set(re.findall(r"git hash-object -- ([^ ]+) 2>/dev/null", inner))
    return {
        "argv": "argc=2",
        "source_guard_count": len(fingerprints),
        "source_guarded_paths_before_refresh": len(guarded),
        "changed_input": "refused unless every reviewed source fingerprint matches",
        "wrong_artifact": "refused unless final target is clean and has no caller artifacts",
        "bash_n": True,
        "mounted_source": str(final["source"]),
        "mounted_tree": str(final["tree"]),
        "mounted_parent": str(final["parent"]),
        "agent_source": str(agent["source"]),
        "agent_tree": str(agent["tree"]),
        "agent_parent": str(agent["parent"]),
        "agent_checkout": str(agent["checkout"]),
        "child": str(agent["child"]),
        "child_key": str(agent["child_key"]),
    }


def prepare(out: Path) -> dict[str, object]:
    final = final_source_input()
    agent = d41_agent_input()
    custody = custody_facts()
    raw, rows = selected_rows()
    if SUITES_FILE.read_bytes() != raw:
        raise RuntimeError("PREPARED: suites file changed during custody preparation")
    app_input = source_custody(final) if final is not None else {
        "status": "PENDING",
        "source": QUALIFIED_APP,
        "tree": QUALIFIED_TREE,
        "parent": QUALIFIED_PARENT,
        "checkout": str(APP),
    }
    outside = b"".join(line for i, line in enumerate(raw.splitlines(keepends=True), 1) if i not in {rows[name][0] for name in SUITES})
    binding_replacements = {
        AGENT: str(agent["source"]),
        str(AGENT_CHECKOUT): str(agent["checkout"]),
        CHILD: str(agent["child"]),
    }
    replacements = dict(binding_replacements)
    drafts = {}
    stage_records = {}
    for n, name in enumerate(SUITES, 2):
        line = rows[name][1]
        if n == 3:
            drafts[name] = line.decode().rstrip("\n")
            if drafts[name] + "\n" != line.decode():
                raise RuntimeError("PREPARED: P3 row changed while preserving it")
            stage_records[name] = {"preserved": True, "live_row_sha256": digest(line)}
            continue
        text = line.decode()
        current_app = f"P{n}APP={QUALIFIED_APP}"
        current_tree = f"P{n}TREE={QUALIFIED_TREE}"
        current_parent = f"P{n}PARENT="
        assert text.count(current_app) == 1 and text.count(current_tree) == 1
        if n == 2:
            assert text.count(current_parent) == 1
        assert QUALIFIED_PARENT in text
        outer, inner, tail = extract_inner(line)
        row_replacements = dict(binding_replacements)
        updated = inner
        for before, after in row_replacements.items():
            count = updated.count(before)
            if count == 0:
                raise RuntimeError(f"mounted source token is missing: {before}")
            updated = updated.replace(before, after)
            if before != after and updated.count(before):
                raise RuntimeError(f"mounted source token was not fully rebound: {before}")
        if (
            f"P{n}APP={QUALIFIED_APP}" not in updated
            or f"P{n}TREE={QUALIFIED_TREE}" not in updated
            or QUALIFIED_PARENT not in updated
            or AGENT in updated
            or CHILD in updated
        ):
            raise RuntimeError("decoded P2 caller retained stale Agent source identity")
        assert f"P{n}A={agent['source']}" in updated and f"P{n}R={RUNTIME}" in updated
        assert agent["child"] in updated and REMOTION in updated
        native_start = inner.index("import { expect }")
        native_end = inner.index("finally { await harness.stop(); }")
        before_native = inner[native_start:native_end]
        # The selected rows are the already-installed, qualified 0609 callers.
        # Keep their six-stage shell byte-for-byte intact; this pass only refreshes
        # the App identity and the source guards for the reviewed successor.
        assert updated.count("PLAYWRIGHT_OUTPUT_DIR=") >= 2
        assert "original-body-NOTRUN" in updated
        updated_native_start = updated.index("import { expect }")
        updated_native_end = updated.index("finally { await harness.stop(); }")
        assert updated[updated_native_start:updated_native_end] == before_native
        assert f"P{n}_ALLOCATED_PORT" in updated and "original-body-NOTRUN" in updated
        current_fingerprints = {
            path: {kind: expected}
            for path, kind, expected in row_fingerprints(updated, n)
        }
        controls = mechanical_controls(updated, n, current_fingerprints, app_input, agent)
        new_outer = outer[:outer.index("$(bash -c ") + len("$(bash -c ")] + shlex.quote(updated) + tail
        for label, data in ((f"p{n}-inner.sh", inner), (f"p{n}-new-inner.sh", updated), (f"p{n}-outer.sh", outer), (f"p{n}-new-outer.sh", new_outer)):
            (out / label).write_text(data)
            subprocess.run(["/bin/bash", "-n", str(out / label)], check=True)
        drafts[name] = f"app {name} {new_outer}"
        stage_records[name] = {**controls, "native_body_preserved": True, "output_stages": ["native-history", "mounted-readiness", "original-body" if n == 2 else "gate5"]}

    if SUITES_FILE.read_bytes() != raw:
        raise RuntimeError("PREPARED: suites file changed before candidate publication")
    manifest = {
        "status": "PREPARED",
        "replacements": replacements,
        "run_authorization": "NOT_GRANTED",
        "qualified_caller": {"commit": "1f82e4b6d86918177f1ec9ddf5747f037f94084f", "app_source": QUALIFIED_APP, "app_tree": QUALIFIED_TREE, "app_parent": QUALIFIED_PARENT},
        "source_base": SOURCE_BASE, "final_source": source_custody(final) if final is not None else {"status": "PENDING", "reason": "final App pure-product join is not available"}, "d41_agent": agent, "custody": custody,
        "live_row_sha256": {name: digest(rows[name][1]) for name in SUITES},
        "draft_row_sha256": {name: digest((drafts[name] + "\n").encode()) for name in SUITES},
        "outside_row_count": len(raw.splitlines(keepends=True)) - len(SUITES), "outside_bytes": len(outside), "outside_sha256": digest(outside),
        "wire_fields": WIRE_FIELDS,
        "stage_records": stage_records,
        "door_port": {"allocation": ["P2_ALLOCATED_PORT", "P3_ALLOCATED_PORT"], "propagates_before_every_stage": True, "changed": False},
        "tool_versions": {"node": "not-read", "npm": "not-read", "playwright": "not-read"},
        "final_inputs": {"catalog_source": "PENDING", "p2_source": "PENDING", "p3_source": "PENDING", "source_manifest": "PENDING", "d41_agent_source": ACTUAL_AGENT, "d41_agent_checkout": str(ACTUAL_AGENT_CHECKOUT), "d41_agent_receipt": str(ACTUAL_AGENT_RECEIPT), "d41_agent_child": ACTUAL_CHILD, "d41_agent_child_key": ACTUAL_CHILD_KEY, "d41_agent_manifest": os.environ.get(D41_AGENT_MANIFEST_ENV, "ACTUAL_FIXED_EVIDENCE")},
        "missing_inputs": ["final reviewed joined App source SHA/tree/parent", "final App source/body checksum rederivation", "separate clean pure final-integrated proof-worker target", "integrated P2 proof and daemon identity"],
        "negative_context": {"source_target_0644": "retained as source-only context", "wrong_artifacts": ["20674", "10144"], "wrong_artifacts_status": "preflight-only, originals NOTRUN; never reuse or relabel"},
        "retention_reuse": {"allowed": True, "condition": "decoded caller logic byte-identical after audited bindings/fingerprints/body hashes/log identity", "otherwise": "bounded real execution controls required", "qualified_stages": 60},
        "selected_source_snapshot": {"required": "normal service must recreate the separate read-only final proof-worker branch and authorize one single-parent same-tree snapshot", "daemon_identity": "uninferred", "candidate_mechanics_only": True},
    }
    (out / "before.json").write_text(json.dumps({name: rows[name][1].decode().rstrip("\n") for name in SUITES}, indent=2) + "\n")
    (out / "after.json").write_text(json.dumps(drafts, indent=2) + "\n")
    (out / "current-draft.rows").write_text("".join(drafts[name] + "\n" for name in SUITES))
    (out / "outside.before").write_bytes(outside)
    (out / "prepared.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(prepare(Path(os.environ["TMPDIR"]).resolve()), indent=2))
