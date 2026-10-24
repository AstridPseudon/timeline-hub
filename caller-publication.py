"""Prepare the exact final Timeline P3 caller for offline qualification.

The generated rows live only in ``TMPDIR``. This artifact reads the two
installed rows, binds the P3 source/body guards to the reviewed final App,
and assigns independent Playwright output children to each stage.
It intentionally has no submission, daemon, browser, HTTP, or build path. The
source is the existing dispatcher-qualified checkout; a later test-run owns
its service snapshot, so preparation must not invent a pre-request receipt.
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
P3_SOURCE_WORKER = "app-P3-current-integrated-0900"
P3_SOURCE_CHECKOUT = Path("/home/user/work/wt/app-pin-82cb5c00")
P3_SOURCE_META = ORCH / "workers" / P3_SOURCE_WORKER / "meta"
P3_SOURCE_REPORT = ORCH / "workers" / P3_SOURCE_WORKER / "report.md"
P3_SOURCE_QUEUE = ORCH / "queue" / "done" / P3_SOURCE_WORKER
P3_SOURCE_CHECKOUT_QUEUE = ORCH / "queue" / "done" / f"checkout-app-{P3_SOURCE}"
RETAINED_OUTSIDE_BEFORE = Path("/tmp/w-8922952ec4/app-P3-solo-return-1011/outside.before")
EXPECTED_REMOVED_ROW = "agent venv-agent-child-app-p3-079-2a9-2147-full"
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
    "id", "intent", "tags", "command_ordinals", "patch", "reads", "dependencies", "merge", "fields", "atomic",
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


def final_source_input() -> dict[str, object]:
    """Read actual dispatcher evidence; a service snapshot is a later fact."""
    if os.environ.get("TIMELINE_FINAL_SOURCE_MANIFEST"):
        raise RuntimeError("PREPARED: generic final source manifests are unsupported")
    for path in (P3_SOURCE_META, P3_SOURCE_REPORT, P3_SOURCE_QUEUE, P3_SOURCE_CHECKOUT_QUEUE):
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"PREPARED: selected P3 evidence is unavailable: {path.name}")
    meta = key_value_file(P3_SOURCE_META)
    if meta.get("name") != P3_SOURCE_WORKER or meta.get("repo") != "app":
        raise RuntimeError("PREPARED: selected P3 dispatcher metadata is not for the App worker")
    if meta.get("base") != P3_SOURCE or meta.get("base_sha") != P3_SOURCE[:10]:
        raise RuntimeError("PREPARED: selected P3 dispatcher base is not exact")
    report = P3_SOURCE_REPORT.read_text()
    if not report.startswith("PASS — P3 integrated source qualification."):
        raise RuntimeError("PREPARED: selected P3 source report is not PASS")
    if P3_SOURCE not in report or P3_TREE not in report or any(parent not in report for parent in P3_PARENTS):
        raise RuntimeError("PREPARED: selected P3 report identity is not exact")
    if P3_SOURCE not in P3_SOURCE_QUEUE.read_text() or P3_SOURCE not in P3_SOURCE_CHECKOUT_QUEUE.read_text():
        raise RuntimeError("PREPARED: selected P3 queue facts do not name the exact source")
    root = P3_SOURCE_CHECKOUT
    if root.is_symlink() or root == APP or not root.is_dir():
        raise RuntimeError("PREPARED: selected P3 checkout is unavailable")
    if any((root / name).exists() for name in ("caller-publication.py", "caller-custody.json")):
        raise RuntimeError("PREPARED: selected P3 checkout contains caller artifacts")
    if git(root, "status", "--porcelain=v1", "--untracked-files=all").strip():
        raise RuntimeError("PREPARED: selected P3 checkout is not clean")
    if git(root, "rev-parse", "HEAD").decode().strip() != P3_SOURCE:
        raise RuntimeError("PREPARED: selected P3 checkout HEAD is not exact")
    if git(root, "show", "-s", "--format=%T", P3_SOURCE).decode().strip() != P3_TREE:
        raise RuntimeError("PREPARED: selected P3 checkout tree is not exact")
    if git(root, "show", "-s", "--format=%P", P3_SOURCE).decode().strip() != P3_PARENT:
        raise RuntimeError("PREPARED: selected P3 checkout parents are not exact")
    return {
        "checkout": str(root), "source_checkout": str(root), "source": P3_SOURCE, "tree": P3_TREE, "parent": P3_PARENT,
        "parents": list(P3_PARENTS), "worker": P3_SOURCE_WORKER,
        "dispatcher_meta": {"path": str(P3_SOURCE_META), "name": meta["name"], "repo": meta["repo"], "base": meta["base"], "base_sha": meta["base_sha"]},
        "source_report": str(P3_SOURCE_REPORT), "source_queue": str(P3_SOURCE_QUEUE),
        "checkout_queue": str(P3_SOURCE_CHECKOUT_QUEUE),
        "service_snapshot": "UNKNOWN — created by the normal test-run after request",
    }


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
    observed_hashes = {path: digest(source_bytes(root, source, path)) for path in required_paths}
    reviewed_hashes = observed_hashes
    spec = source_bytes(root, source, "tests/e2e/local/three-products.spec.ts")
    tail = spec[spec.index(b"  const resetResponse = page.waitForResponse", spec.index(b"test('M2 real gate 5")):spec.index(b"\n", spec.index(b"test('M2 ordinary extension batch")) + 1]
    if digest(tail) != "5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912":
        raise RuntimeError("D50/P3 protected tail does not match final source")
    p3 = guarded(spec.decode(), "test('M2 real gate 5", "test('M2 ordinary extension batch").rstrip() + b"\n"
    if digest(p3) != "e6cf20b09e412df16f82265b0b855c426123e93b44861bd0b7770dcf82d751d4":
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
            "protected_hashes": {
                "d50_tail_sha256": digest(tail), "p3_gate5_sha256": digest(p3),
            }}

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


def registry_row_key(line: bytes) -> str:
    fields = line.split(None, 2)
    if len(fields) < 2:
        raise RuntimeError("PREPARED: suites registry row has no stable key")
    return " ".join(field.decode() for field in fields[:2])


def keyed_registry_lines(raw: bytes) -> list[tuple[str, bytes]]:
    return [
        (registry_row_key(line), line)
        for line in raw.splitlines(keepends=True)
        if line.strip() and not line.lstrip().startswith(b"#")
    ]


def registry_snapshot(raw: bytes, p3_line_number: int) -> tuple[dict[str, object], bytes]:
    lines = raw.splitlines(keepends=True)
    outside = b"".join(line for i, line in enumerate(lines, 1) if i != p3_line_number)
    return {
        "line_count": len(lines),
        "byte_count": len(raw),
        "sha256": digest(raw),
        "outside_row_count": len(lines) - 1,
        "outside_bytes": len(outside),
        "outside_sha256": digest(outside),
    }, outside


def retained_registry_evidence(outside: bytes) -> dict[str, object]:
    """Compare the live retained rows with the prior run when that evidence exists."""
    path = RETAINED_OUTSIDE_BEFORE
    if path.is_symlink() or not path.is_file():
        return {
            "status": "UNAVAILABLE",
            "path": str(path),
            "evidence_limit": "retained-before registry bytes were unavailable; only the live snapshot is authoritative",
        }
    previous = path.read_bytes()
    previous_keyed = keyed_registry_lines(previous)
    current_keyed = keyed_registry_lines(outside)
    previous_rows = dict(previous_keyed)
    current_rows = dict(current_keyed)
    if len(previous_rows) != len(previous_keyed):
        raise RuntimeError("PREPARED: retained-before registry has duplicate row keys")
    if len(current_rows) != len(current_keyed):
        raise RuntimeError("PREPARED: current registry has duplicate retained row keys")
    common = set(previous_rows) & set(current_rows)
    changed = sorted(key for key in common if previous_rows[key] != current_rows[key])
    removed = sorted(set(previous_rows) - set(current_rows))
    added = sorted(set(current_rows) - set(previous_rows))
    if changed or added or removed != [EXPECTED_REMOVED_ROW]:
        raise RuntimeError(
            "PREPARED: retained-before registry comparison is broader than the known retirement: "
            f"removed={removed!r}, added={added!r}, changed={changed!r}"
        )
    previous_without_removed = b"".join(
        line for line in previous.splitlines(keepends=True)
        if not (line.strip() and not line.lstrip().startswith(b"#") and registry_row_key(line) == EXPECTED_REMOVED_ROW)
    )
    if previous_without_removed != outside:
        raise RuntimeError("PREPARED: retained-before registry has changed common bytes")
    return {
        "status": "VERIFIED",
        "path": str(path),
        "sha256": digest(previous),
        "row_count": len(previous.splitlines(keepends=True)),
        "bytes": len(previous),
        "removed_keys": removed,
        "added_keys": added,
        "changed_common_keys": changed,
    }


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
    fingerprint_count: int,
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
    argv = bash_c_argument_proof()
    return {
        "argv": argv,
        "source_guard_count": fingerprint_count,
        "source_guarded_paths_before_refresh": len(guarded),
        "changed_input": "refused unless every reviewed source fingerprint matches",
        "wrong_artifact": "refused unless final target is clean and has no caller artifacts",
        "bash_n": True,
        "mounted_source": str(final["source"]),
        "mounted_tree": str(final["tree"]),
        "mounted_parent": str(final["parent"]),
    }


def bash_c_argument_proof() -> dict[str, object]:
    """Prove the supported ``bash -c`` contract without invoking the caller."""
    zero = subprocess.run(
        ["/bin/bash", "-c", 'test "$#" -eq 0'], check=False,
    )
    one = subprocess.run(
        ["/bin/bash", "-c", 'test "$#" -eq 0', "caller", "child-arg"], check=False,
    )
    if zero.returncode != 0 or one.returncode == 0:
        raise RuntimeError("bash -c positional-argument proof failed")
    return {
        "invocation": "bash -c <payload>",
        "payload_positional_argc": 0,
        "positive_zero_arg": True,
        "negative_one_arg": True,
    }


def prepare(out: Path) -> dict[str, object]:
    final = final_source_input()
    source = source_custody(final)
    custody = custody_facts()
    raw, rows = selected_rows()
    registry, outside = registry_snapshot(raw, rows[P3_SUITE][0])
    retained_evidence = retained_registry_evidence(outside)
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
            _, p2_inner, _ = extract_inner(line)
            stage_records[name] = {
                "installed_sha256": p2_line_sha256,
                "source_guard_count": len(row_fingerprints(p2_inner, n)),
                "unchanged": True,
            }
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
        controls = mechanical_controls(updated, n, len(row_fingerprints(inner, n)), final)
        new_outer = outer[:outer.index("$(bash -c ") + len("$(bash -c ")] + shlex.quote(updated) + tail
        for label, data in ((f"p{n}-inner.sh", inner), (f"p{n}-new-inner.sh", updated), (f"p{n}-outer.sh", outer), (f"p{n}-new-outer.sh", new_outer)):
            (out / label).write_text(data)
            subprocess.run(["/bin/bash", "-n", str(out / label)], check=True)
        drafts[name] = f"app {name} {new_outer}"
        stage_records[name] = {**controls, "native_body_preserved": True, "output_stages": ["native-history", "mounted-readiness", "gate5"]}

    # The registry is a live input. Re-read it after decoding and rebinding so
    # a concurrent edit cannot produce a candidate from a stale snapshot.
    current_raw, current_rows = selected_rows()
    current_registry, _ = registry_snapshot(current_raw, current_rows[P3_SUITE][0])
    if current_raw != raw or current_registry != registry:
        raise RuntimeError("PREPARED: suites registry changed during candidate preparation")
    if current_rows[P2_SUITE][1] != p2_line:
        raise RuntimeError("PREPARED: installed P2 row changed during candidate preparation")

    manifest = {
        "status": "REVIEWABLE",
        "replacements": replacements,
        "run_authorization": "NOT_GRANTED",
        "qualified_caller": {"commit": "d54582a08c6ad0453742523a3ec374dd321ce477", "app_source": QUALIFIED_APP, "app_tree": QUALIFIED_TREE, "app_parent": QUALIFIED_PARENT},
        "source_base": SOURCE_BASE, "final_source": source, "custody": custody,
        "live_row_sha256": {name: digest(rows[name][1]) for name in SUITES},
        "draft_row_sha256": {name: digest((drafts[name] + "\n").encode()) for name in SUITES},
        "p2_row_unchanged": current_rows[P2_SUITE][1] == p2_line,
        "p2_row_sha256": p2_line_sha256,
        "registry_snapshot": registry,
        "registry_evidence": retained_evidence,
        "registry_installation_guard": {
            "path": str(SUITES_FILE),
            "line_count": registry["line_count"],
            "byte_count": registry["byte_count"],
            "sha256": registry["sha256"],
            "outside_row_count": registry["outside_row_count"],
            "outside_bytes": registry["outside_bytes"],
            "outside_sha256": registry["outside_sha256"],
            "p2_row_sha256": p2_line_sha256,
        },
        "outside_row_count": registry["outside_row_count"], "outside_bytes": registry["outside_bytes"], "outside_sha256": registry["outside_sha256"],
        "wire_fields": WIRE_FIELDS,
        "stage_records": stage_records,
        "door_port": {"allocation": ["P2_ALLOCATED_PORT", "P3_ALLOCATED_PORT"], "propagates_before_every_stage": True, "changed": False},
        "tool_versions": {"node": "not-read", "npm": "not-read", "playwright": "not-read"},
        "final_inputs": {
            "catalog_source": "dispatcher metadata/report/queue facts",
            "p3_source": source,
            "source_manifest": "not used; immutable selected checkout is authoritative",
        },
        "missing_inputs": ["integrated P3 execution and daemon identity"],
        "negative_context": {"source_target_0644": "retained as source-only context", "wrong_artifacts": ["20674", "10144"], "wrong_artifacts_status": "preflight-only, originals NOTRUN; never reuse or relabel"},
        "retention_reuse": {"allowed": True, "condition": "decoded caller logic byte-identical after audited bindings/fingerprints/body hashes/log identity", "otherwise": "bounded real execution controls required", "qualified_stages": 60},
        "selected_source": {
            "dispatcher_worker": P3_SOURCE_WORKER,
            "checkout": str(final["checkout"]),
            "source_parents": list(P3_PARENTS),
            "service_snapshot": final["service_snapshot"],
            "daemon_identity": "UNKNOWN",
        },
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
        "service_snapshot_status": final["service_snapshot"],
        "custody": custody,
        "p2_row_sha256": p2_line_sha256,
        "p3_row_sha256": manifest["draft_row_sha256"][P3_SUITE],
        "registry_snapshot": manifest["registry_snapshot"],
        "registry_evidence": retained_evidence,
        "outside_rows": {"count": registry["outside_row_count"], "bytes": registry["outside_bytes"], "sha256": registry["outside_sha256"]},
    }, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(prepare(Path(os.environ["TMPDIR"]).resolve()), indent=2))
