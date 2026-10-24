"""Prepare the exact final Timeline P3 caller for offline qualification.

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
import subprocess


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
APP = Path(__file__).resolve().parent
SUITES_FILE = ORCH / "tests/suites.conf"
SUITES = ("full-e2e-three-products", "ap2-P3-gate5-h6-0348")
P2_SUITE = "full-e2e-three-products"
P3_SUITE = "ap2-P3-gate5-h6-0348"

QUALIFIED_APP = "66354161950d1e747965c095ea97b881d2592708"
QUALIFIED_TREE = "9a37265f0286128df7e6240a9df9877d959474af"
QUALIFIED_PARENT = "b2380539c5545661954d2794976631312ee1d939"
P3_SOURCE = "82cb5c0005df7abe0fcb8673f7be192a6c9e9183"
P3_TREE = "6fa0a0f32b212dbdae7c2ecaca1813de68907e67"
P3_PARENTS = (
    "182c65242d8228232cde32961fd1948056dd841a",
    "f56128d540ff96013c9532d79f3f4e767beba820",
)
P3_PARENT = " ".join(P3_PARENTS)
SOURCE_BASE = "f90e708b379145ac456924742cc51c187ed6e0c6"
AGENT = "079580ca46af77e0292d49dc34386b25c8391f99"
RUNTIME = "37eb6c7bdb79dcae2523883e66b5cea5be721ffd"
RUNTIME_TREE = "be4114705127f9ee9e86b26cd6de3f467e771c01"
AGENT_CHECKOUT = Path("/home/user/work/wt/agt-pin-079580ca")
RUNTIME_CHECKOUT = Path("/home/user/work/wt/rt-pin-37eb6c7b")
CHILD = "venv-agent-child-app-ready-079-37eb-0256"
REMOTION = "agent-remotion-app-ready-079-37eb-0258"
CHILD_KEY = "5464e85332660e8d6d133653d0600709f2aac5a6c9a0ff0e0bc1fb18312d7f2f"
CHILD_ROOT = Path("/home/user/work/bench-store/entries") / f"child-{CHILD_KEY}"
REMOTION_ROOT = Path("/home/user/work/bench-store/entries/runtime-5ca5c561b7be7069051ac8769432cc1edf29060bed39384cd3c4ecab1736e690")
PROVISION_RECEIPT = ORCH / "tests/provision" / f"{CHILD}.txt"
CHILD_RECEIPT = ORCH / "queue/done" / f"childvenv-{CHILD}"
REMOTION_RECEIPT = ORCH / "queue/done" / f"runtime-{REMOTION}"

WIRE_FIELDS = (
    "api_version", "project_id", "timeline_id", "base_revision_id", "base_publication_id",
    "commands", "schema_version", "op", "version", "select", "args", "created", "label", "steps",
    "id", "intent", "tags", "command_ordinals", "patch", "reads", "merge", "fields", "atomic",
    "Idempotency-Key", "dry_run", "source", "rationale", "group_id", "data", "receipt", "status",
    "canonical_document", "document_digest", "id_map", "authoritative_commands", "base", "previous",
    "previous_revision_id", "previous_publication_id", "accepted_ids", "accepted_revision_id",
    "publisher", "provider_version", "compiler_version", "merge_mode", "rebased_onto", "accepted",
    "merged", "conflict", "invalid", "rebased", "evaluated_head", "would_status", "receipt_id",
    "command_kind", "idempotency_key", "request_hash", "project_seq", "event_ids", "result", "created_at",
    "http_status", "message", "details", "reason", "head", "base", "current", "conflicts", "kind", "ref",
    "theirs", "ours", "choices", "code", "path", "hint", "suggested_command",
)

REQUIRED_FINAL_SOURCE_PATHS = (
    "tests/e2e/local/three-products.spec.ts",
    "tests/e2e/local/support/gate5-reset-precondition.ts",
    "tests/e2e/local/support/gate5-reset-precondition.test.mjs",
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


def receipt_parents(receipt: dict[str, object]) -> tuple[str, ...]:
    value = receipt.get("parents")
    if isinstance(value, list):
        return tuple(str(parent) for parent in value)
    parent = receipt_value(receipt, "parent")
    return tuple(str(parent).split()) if parent is not None else ()


def validate_receipt(
    manifest: dict[str, object],
    manifest_name: Path,
    identity: dict[str, object],
    role: str,
) -> tuple[Path, dict[str, object]]:
    candidate = Path(str(manifest["source_receipt"]))
    if candidate.is_symlink():
        raise RuntimeError(f"PREPARED: {role} receipt must not be a symlink")
    path = candidate.resolve()
    try:
        path.relative_to(ORCH)
    except ValueError as exc:
        raise RuntimeError(f"PREPARED: {role} receipt is outside the dispatcher area") from exc
    if path == manifest_name.resolve() or not path.is_file():
        raise RuntimeError(f"PREPARED: {role} receipt is unavailable")
    expected_hash = manifest["source_receipt_sha256"]
    if digest(path.read_bytes()) != expected_hash:
        raise RuntimeError(f"PREPARED: {role} receipt hash does not match explicit input")
    receipt = source_receipt(path)
    for key, expected in identity.items():
        if key == "parent" and isinstance(receipt.get("parents"), list):
            observed = " ".join(receipt_parents(receipt))
        else:
            observed = str(receipt_value(receipt, key))
        if observed != str(expected):
            raise RuntimeError(f"PREPARED: {role} receipt identity mismatch: {key}")
    if receipt_parents(receipt) != tuple(str(parent) for parent in str(identity["parent"]).split()):
        raise RuntimeError(f"PREPARED: {role} receipt parent list mismatch")
    if receipt_value(receipt, "review") not in (None, "PASS"):
        raise RuntimeError(f"PREPARED: {role} receipt review is not PASS")
    return path, receipt


def validate_dispatcher_checkout(
    manifest: dict[str, object],
    manifest_name: Path,
    *,
    role: str,
    expected_source: str,
    expected_tree: str,
    expected_parent: str,
    require_single_parent: bool,
) -> tuple[Path, dict[str, str], Path]:
    worker = str(manifest["worker"])
    if not worker or "/" in worker or worker in {".", ".."}:
        raise RuntimeError(f"PREPARED: {role} worker identity is invalid")
    meta_path = ORCH / "workers" / worker / "meta"
    if not meta_path.is_file() or meta_path.is_symlink():
        raise RuntimeError(f"PREPARED: {role} dispatcher metadata is unavailable")
    meta = key_value_file(meta_path)
    branch = str(manifest["branch"])
    if (
        meta.get("name") != worker
        or meta.get("repo") != "app"
        or meta.get("base") != manifest["base"]
        or meta.get("base_sha") != manifest["base_sha"]
        or branch != f"tl/{worker}"
    ):
        raise RuntimeError(f"PREPARED: {role} does not match dispatcher branch/base identity")
    checkout_path = Path(str(manifest["checkout"]))
    if checkout_path.is_symlink():
        raise RuntimeError(f"PREPARED: {role} checkout must not be a symlink")
    root = checkout_path.resolve()
    if root == APP or not root.is_dir():
        raise RuntimeError(f"PREPARED: {role} must be a separate proof worker")
    if Path(meta.get("worktree", "")).resolve() != root:
        raise RuntimeError(f"PREPARED: {role} checkout is not the dispatched worker")
    if any((root / name).exists() for name in ("caller-publication.py", "caller-custody.json")):
        raise RuntimeError(f"refusing caller-artifact {role}")
    if git(root, "status", "--porcelain=v1", "--untracked-files=all").strip():
        raise RuntimeError(f"PREPARED: {role} target is not clean")
    if git(root, "symbolic-ref", "--quiet", "--short", "HEAD").decode().strip() != branch:
        raise RuntimeError(f"PREPARED: {role} checkout is not on the dispatched branch")
    base_commit = git(root, "rev-parse", f"{manifest['base']}^{{commit}}").decode().strip()
    if not base_commit.startswith(str(manifest["base_sha"])):
        raise RuntimeError(f"PREPARED: {role} base does not match dispatcher identity")
    if git(root, "rev-parse", "HEAD").decode().strip() != expected_source:
        raise RuntimeError(f"PREPARED: {role} HEAD does not match selected source")
    if git(root, "show", "-s", "--format=%T", expected_source).decode().strip() != expected_tree:
        raise RuntimeError(f"PREPARED: {role} tree does not match selected source")
    parent = git(root, "show", "-s", "--format=%P", expected_source).decode().strip()
    if parent != expected_parent:
        raise RuntimeError(f"PREPARED: {role} parent list does not match selected source")
    if require_single_parent and len(parent.split()) != 1:
        raise RuntimeError(f"PREPARED: {role} must be a single-parent snapshot")
    receipt_path, _ = validate_receipt(
        manifest,
        manifest_name,
        {
            "worker": worker,
            "branch": branch,
            "base": manifest["base"],
            "base_sha": manifest["base_sha"],
            "source": expected_source,
            "tree": expected_tree,
            "parent": expected_parent,
            "checkout": root,
        },
        role,
    )
    return root, meta, receipt_path


def final_source_input() -> dict[str, object]:
    manifest_name = os.environ.get("TIMELINE_FINAL_SOURCE_MANIFEST")
    if not manifest_name:
        raise RuntimeError("PREPARED: final reviewed source tuple is not available")
    manifest = json.loads(Path(manifest_name).read_text())
    required = (
        "checkout", "source", "tree", "parent", "review", "proof_release", "worker", "branch",
        "base", "base_sha", "source_receipt", "source_receipt_sha256", "service_snapshot",
    )
    if any(key not in manifest for key in required):
        raise RuntimeError("PREPARED: final source manifest is incomplete")
    if manifest["review"] != "PASS":
        raise RuntimeError("PREPARED: independent final-source review is not PASS")
    if manifest["proof_release"] != "PASS":
        raise RuntimeError("PREPARED: P3 proof release is not PASS")
    if manifest["source"] != P3_SOURCE or manifest["tree"] != P3_TREE:
        raise RuntimeError("PREPARED: selected P3 source is not the exact integrated source")
    if str(manifest["parent"]) != P3_PARENT:
        raise RuntimeError("PREPARED: selected P3 source parent list is not exact")
    source_root, source_meta, source_receipt_path = validate_dispatcher_checkout(
        manifest,
        Path(manifest_name),
        role="selected P3 source",
        expected_source=P3_SOURCE,
        expected_tree=P3_TREE,
        expected_parent=P3_PARENT,
        require_single_parent=False,
    )
    snapshot = manifest["service_snapshot"]
    if not isinstance(snapshot, dict):
        raise RuntimeError("PREPARED: authenticated service snapshot is incomplete")
    snapshot_required = (
        "checkout", "source", "tree", "parent", "worker", "branch", "base", "base_sha",
        "source_receipt", "source_receipt_sha256", "review",
    )
    if any(key not in snapshot for key in snapshot_required):
        raise RuntimeError("PREPARED: authenticated service snapshot is incomplete")
    if snapshot["review"] != "PASS":
        raise RuntimeError("PREPARED: authenticated service snapshot review is not PASS")
    snapshot_parent = str(snapshot["parent"])
    if snapshot["source"] == P3_SOURCE or snapshot_parent != P3_SOURCE:
        raise RuntimeError("PREPARED: service snapshot must be a distinct single-parent child")
    snapshot_root, snapshot_meta, snapshot_receipt_path = validate_dispatcher_checkout(
        snapshot,
        Path(manifest_name),
        role="authenticated service snapshot",
        expected_source=str(snapshot["source"]),
        expected_tree=P3_TREE,
        expected_parent=P3_SOURCE,
        require_single_parent=True,
    )
    manifest["parents"] = list(P3_PARENTS)
    manifest["source_checkout"] = str(source_root)
    manifest["service_snapshot"] = {
        **snapshot,
        "checkout": str(snapshot_root),
        "parents": [P3_SOURCE],
        "source_receipt": {"path": str(snapshot_receipt_path), "sha256": snapshot["source_receipt_sha256"]},
        "dispatcher_meta": {key: snapshot_meta[key] for key in ("name", "repo", "base", "base_sha", "worktree")},
    }
    manifest["dispatcher_meta"] = {key: source_meta[key] for key in ("name", "repo", "base", "base_sha", "worktree")}
    manifest["source_receipt"] = {"path": str(source_receipt_path), "sha256": manifest["source_receipt_sha256"]}
    return manifest


def source_custody(final: dict[str, object]) -> dict[str, object]:
    root = Path(str(final.get("source_checkout", final["checkout"]))).resolve()
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
    parents = tuple(parent.split())
    if parents != P3_PARENTS:
        raise RuntimeError("PREPARED: selected P3 parent list changed")
    anchors = {}
    anchors[source] = {"tree": tree, "parents": list(parents)}
    return {"source": source, "tree": tree, "parent": parent, "checkout": str(root),
            "parents": list(parents),
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
) -> dict[str, object]:
    """Check the retained caller's controls without running any stage."""
    required = (
        f"P{n}_ALLOCATED_PORT", f"P{n}A={AGENT}", f"P{n}R={RUNTIME}",
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
    }


def prepare(out: Path) -> dict[str, object]:
    final = final_source_input()
    source = source_custody(final)
    custody = custody_facts()
    raw, rows = selected_rows()
    outside = b"".join(line for i, line in enumerate(raw.splitlines(keepends=True), 1) if i != rows[P3_SUITE][0])
    assert len(raw.splitlines(keepends=True)) - 1 == 249
    assert len(outside) == 509969 and digest(outside) == "1340ef479d7f0b850f71f149347806146a4686f7b195b8d6fca3184667fce9d7"
    p2_line = rows[P2_SUITE][1]
    p2_line_sha256 = digest(p2_line)
    binding_replacements = {
        QUALIFIED_APP: str(final["source"]),
        QUALIFIED_TREE: str(final["tree"]),
        QUALIFIED_PARENT: str(final["parent"]),
    }
    replacements = dict(binding_replacements)
    drafts = {}
    stage_records = {}
    for n, name in enumerate(SUITES, 2):
        line = rows[name][1]
        if name == P2_SUITE:
            drafts[name] = line.decode().rstrip("\n")
            stage_records[name] = {"installed_sha256": p2_line_sha256, "unchanged": True}
            continue
        assert name == P3_SUITE
        text = line.decode()
        current_app = f"P{n}APP={QUALIFIED_APP}"
        current_tree = f"P{n}TREE={QUALIFIED_TREE}"
        assert text.count(current_app) == 1 and text.count(current_tree) == 1
        assert QUALIFIED_PARENT in text
        outer, inner, tail = extract_inner(line)
        row_replacements = dict(binding_replacements)
        # Recompute this row's guards from the actual installed command, rather
        # than assuming its fingerprints came from the qualified commit tree.
        final_root = Path(str(final["source_checkout"]))
        for path, kind, before in row_fingerprints(inner, n):
            data = source_bytes(final_root, str(final["source"]), path)
            after = git_blob(data) if kind == "blob" else digest(data)
            row_replacements[before] = after
            replacements[before] = after
        updated = inner
        for before, after in row_replacements.items():
            count = updated.count(before)
            if count == 0:
                raise RuntimeError(f"mounted source token is missing: {before}")
            updated = updated.replace(before, after)
            if before != after and updated.count(before):
                raise RuntimeError(f"mounted source token was not fully rebound: {before}")
        if (
            f"P{n}APP={final['source']}" not in updated
            or f"P{n}TREE={final['tree']}" not in updated
            or str(final["parent"]) not in updated
            or QUALIFIED_APP in updated
            or QUALIFIED_TREE in updated
            or QUALIFIED_PARENT in updated
        ):
            raise RuntimeError("decoded mounted caller retained stale source identity")
        # Lock every changed final source file before any production stage.
        guarded_paths = set(re.findall(r"git hash-object -- ([^ ]+) 2>/dev/null", inner))
        extra = " ".join(
            f'test "$(git hash-object -- {shlex.quote(path)} 2>/dev/null)" = {info["blob"]} || p{n}fail final-source-blob;'
            for path, info in source["fingerprints"].items() if path not in guarded_paths
        )
        marker = f"if ! P{n}_ALLOCATED_PORT="
        assert updated.count(marker) == 1
        if extra:
            updated = updated.replace(marker, extra + " " + marker, 1)
        assert f"P{n}A={AGENT}" in updated and f"P{n}R={RUNTIME}" in updated
        assert CHILD in updated and REMOTION in updated
        native_start = inner.index("import { expect }")
        native_end = inner.index("finally { await harness.stop(); }")
        before_native = inner[native_start:native_end]
        # Keep the installed P3 shell byte-for-byte intact; this pass only
        # refreshes its App identity and source guards for the reviewed source.
        assert updated.count("PLAYWRIGHT_OUTPUT_DIR=") >= 2
        assert "original-body-NOTRUN" in updated
        updated_native_start = updated.index("import { expect }")
        updated_native_end = updated.index("finally { await harness.stop(); }")
        assert updated[updated_native_start:updated_native_end] == before_native
        assert f"P{n}_ALLOCATED_PORT" in updated and "original-body-NOTRUN" in updated
        controls = mechanical_controls(updated, n, source["fingerprints"], final)
        new_outer = outer[:outer.index("$(bash -c ") + len("$(bash -c ")] + shlex.quote(updated) + tail
        for label, data in ((f"p{n}-inner.sh", inner), (f"p{n}-new-inner.sh", updated), (f"p{n}-outer.sh", outer), (f"p{n}-new-outer.sh", new_outer)):
            (out / label).write_text(data)
            subprocess.run(["/bin/bash", "-n", str(out / label)], check=True)
        drafts[name] = f"app {name} {new_outer}"
        stage_records[name] = {**controls, "native_body_preserved": True, "output_stages": ["native-history", "mounted-readiness", "gate5"]}

    manifest = {
        "status": "REVIEWABLE",
        "replacements": replacements,
        "run_authorization": "NOT_GRANTED",
        "qualified_caller": {"commit": "d54582a08c6ad0453742523a3ec374dd321ce477", "app_source": QUALIFIED_APP, "app_tree": QUALIFIED_TREE, "app_parent": QUALIFIED_PARENT},
        "source_base": SOURCE_BASE, "final_source": source, "custody": custody,
        "live_row_sha256": {name: digest(rows[name][1]) for name in SUITES},
        "draft_row_sha256": {name: digest((drafts[name] + "\n").encode()) for name in SUITES},
        "p2_row_unchanged": p2_line_sha256 == digest(rows[P2_SUITE][1]),
        "outside_row_count": 249, "outside_bytes": len(outside), "outside_sha256": digest(outside),
        "wire_fields": WIRE_FIELDS,
        "stage_records": stage_records,
        "door_port": {"allocation": ["P2_ALLOCATED_PORT", "P3_ALLOCATED_PORT"], "propagates_before_every_stage": True, "changed": False},
        "tool_versions": {"node": "not-read", "npm": "not-read", "playwright": "not-read"},
        "final_inputs": {"catalog_source": "PENDING", "p3_source": "PENDING", "source_manifest": "PENDING"},
        "missing_inputs": ["integrated P3 execution and daemon identity"],
        "negative_context": {"source_target_0644": "retained as source-only context", "wrong_artifacts": ["20674", "10144"], "wrong_artifacts_status": "preflight-only, originals NOTRUN; never reuse or relabel"},
        "retention_reuse": {"allowed": True, "condition": "decoded caller logic byte-identical after audited bindings/fingerprints/body hashes/log identity", "otherwise": "bounded real execution controls required", "qualified_stages": 60},
        "selected_source_snapshot": {"required": "normal service must recreate the separate read-only final proof-worker branch and authorize one single-parent same-tree snapshot", "daemon_identity": "uninferred", "source_parents": list(P3_PARENTS), "service_parent": P3_SOURCE},
    }
    (out / "before.json").write_text(json.dumps({name: rows[name][1].decode().rstrip("\n") for name in SUITES}, indent=2) + "\n")
    (out / "after.json").write_text(json.dumps(drafts, indent=2) + "\n")
    (out / "current-draft.rows").write_text("".join(drafts[name] + "\n" for name in SUITES))
    (out / "outside.before").write_bytes(outside)
    (out / "prepared.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (out / "custody-receipt.json").write_text(json.dumps({
        "status": "REVIEWABLE",
        "run_authorization": "NOT_GRANTED",
        "source": source,
        "service_snapshot": final["service_snapshot"],
        "custody": custody,
        "p2_row_sha256": p2_line_sha256,
        "p3_row_sha256": manifest["draft_row_sha256"][P3_SUITE],
        "outside_rows": {"count": 249, "bytes": len(outside), "sha256": digest(outside)},
    }, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(prepare(Path(os.environ["TMPDIR"]).resolve()), indent=2))
