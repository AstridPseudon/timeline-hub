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

# D53 was independently reviewed on this exact author commit.  It is the
# source of the new helper and the strict retry guard, not the final HOME
# source used for a run.
D53_BASE = "d6ed8cbda122d810d5836ebfce3c56c10e76e9b4"
P3_SOURCE = "2357df925a660dde6624149b8e8a6e1dbf09da98"
P3_TREE = "50070be219d9d16954aaaf237b1e7287b76187c1"
P3_PARENTS = (D53_BASE,)
P3_PARENT = D53_BASE
P3_SOURCE_WORKER = "ap2-P3-D53-clean-apply-1123"
P3_SOURCE_BRANCH = f"tl/{P3_SOURCE_WORKER}"
P3_SOURCE_REPO = Path("/home/user/work/app")
P3_SOURCE_META = ORCH / "workers" / P3_SOURCE_WORKER / "meta"
P3_SOURCE_AUTHOR_REPORT = ORCH / "design/handoff-ap2-P3-D53-clean-apply-1123.md"
P3_SOURCE_REVIEW = ORCH / "design/handoff-ap2-P3-D53-final-review-1126.md"
P3_SOURCE_QUEUE = ORCH / "queue" / f".remote-app-{P3_SOURCE_WORKER}"
P3_SOURCE_META_SHA256 = "c39086db5e4f60ea4f046bcfaa98c0ac459d12929b773f1d375a95af8a022c3f"
P3_SOURCE_AUTHOR_REPORT_SHA256 = "5ae31800903dfa5f7652b912e78d99307b421890740afd8f0fd508d196e73b6d"
P3_SOURCE_REVIEW_SHA256 = "88b3aff6c159990e8950bf257e4ce98d2b821ebb65a6e91b79c540e798fe09f8"
P3_SOURCE_QUEUE_SHA256 = "a27d4266d4a6ed1068f064703cab5811c5816bc38986bc535081d0fea541d840"

P3_PURE_WORKER = "app-P3-D53-pure-integrated-1143"
P3_PURE_BRANCH = f"tl/{P3_PURE_WORKER}"
P3_PURE_REPORT = ORCH / "workers" / P3_PURE_WORKER / "report.md"
P3_PURE_META = ORCH / "workers" / P3_PURE_WORKER / "meta"
P3_PURE_ENDED = ORCH / "workers" / P3_PURE_WORKER / "ended"
P3_PURE_QUEUE = ORCH / "queue" / "done" / P3_PURE_WORKER
P3_PURE_DONE = ORCH / "workers" / P3_PURE_WORKER / "DONE"
P3_PURE_REPORT_SHA256 = "7ddf4f5759a12f6dad7e6ff7b58c768843848e311ef71ba15ce5788d228de5fc"
P3_PURE_META_SHA256 = "a62684c39634490ecd65105debd23e7f8bf20cd092bd20e1c7762ba1f645ffda"
P3_PURE_ENDED_SHA256 = "ffcdfc4efc8536b92bbeabc7895e530f441891040c3d7978d6c9199e46a831c4"
P3_PURE_QUEUE_SHA256 = "6085d793604d8b744a937d3bd54f041243f88106f0537d08c511897b85e645af"
P3_PURE_DONE_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# The merged HOME is an observed input.  Its full identity is captured at
# preparation time and must still match at the final CAS read.  Pure
# qualification is a separate fixed worker record, never caller input.
FINAL_HOME = Path("/home/user/work/app")
FINAL_SOURCE_MANIFEST_ENV = "TIMELINE_P3_FINAL_SOURCE_MANIFEST"
PURE_PROOF_MANIFEST_ENV = "TIMELINE_P3_PURE_PROOF_MANIFEST"
FINAL_HOME_BASE = "2e3c8f65a8628127cd283ed26116f7bcb2977b83"
FINAL_HOME_REQUIRED_PARENTS = (FINAL_HOME_BASE, P3_SOURCE)
FINAL_HOME_SOURCE = "602f8b1f58593302829fb449d0ded62a91462a22"
FINAL_HOME_TREE = "a38844975865110cd2c026dc10fd7aa1ea488e71"
FINAL_HOME_CHECKOUT_RECEIPT = ORCH / "queue" / "done" / "checkout-app-602f8b1f58593302829fb449d0ded62a91462a22"
FINAL_HOME_CHECKOUT_RECEIPT_SHA256 = "bb462c89a7679a43dfcd855fe36c47c97c2d37dd0be8a674508ace8ed9223327"
RETAINED_OUTSIDE_BEFORE = Path("/tmp/w-8922952ec4/app-P3-solo-return-1011/outside.before")
EXPECTED_REMOVED_ROW = "agent venv-agent-child-app-p3-079-2a9-2147-full"
P2_INSTALLED_ROW_SHA256 = "6a45d0567f7dea7a3c15fbcaf687f9dd62debf4527464529d8a4faf8f8e48fee"
P3_INSTALLED_ROW_SHA256 = "23226c274dbdbb8750f009cb89d7920db40eb49513af906df7b4f76d9a7a3bf0"
REGISTRY_OUTSIDE_SHA256 = "b9c97fbbfd26fa4d6d2ed3fac150196fc3fbae24deade990624196f0c5423fee"
SOURCE_BASE = D53_BASE
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
    "tests/e2e/local/support/gate5-fault-order.ts",
    "tests/e2e/local/support/gate5-fault-order.test.mjs",
)

D53_FULL_SPEC_SHA256 = "95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c"
D53_GATE5_BODY_SHA256 = "d47d55265b3905a1882ffb370df033cf92b35c3492d4bec366d8da0272b9fb20"
D53_RESET_BLOCK_SHA256 = "980b4cbe2c1d7a05840c8419fd55991ff73783784c89df6c717e2721a212fe62"
D53_CANONICAL_TAIL_SHA256 = "5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912"
D53_DOWNSTREAM_TAIL_SHA256 = "6bfdd99dfddf9608d24da81345884e4d32329b3414bd43eeb55ffe3bdde18f74"
D53_FAULT_HELPER_SHA256 = "3e896066737d9e8f07eccfdcb25f88f16d6e8e48457281f1b986af0b1cab7434"
D53_GUARD_SHA256 = "1c080595fbb1dd5fb6ecc7387e9bf01744e0b08e61473d3994383e226b60a9e0"


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"PREPARED: {message}")


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def source_bytes(root: Path, commit: str, path: str) -> bytes:
    return git(root, "show", f"{commit}:{path}")


def guarded(text: str, start: str, end: str | None) -> bytes:
    if not start or text.count(start) != 1:
        raise RuntimeError(f"PREPARED: source anchor is not unique: {start!r}")
    if end is not None and text.count(end) != 1:
        raise RuntimeError(f"PREPARED: source end anchor is not unique: {end!r}")
    a = text.index(start)
    b = text.index(end, a) if end else len(text)
    value = text[a:b].encode()
    if not value.strip():
        raise RuntimeError("PREPARED: source anchor selected an empty region")
    return value


def key_value_file(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text().splitlines():
        key, separator, value = line.partition("=")
        if separator:
            values[key] = value
    return values


def exact_record(path: Path, expected_sha256: str, label: str) -> bytes:
    """Read only a fixed, recorded evidence file with its full immutable hash."""
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"PREPARED: {label} evidence is unavailable")
    data = path.read_bytes()
    if digest(data) != expected_sha256:
        raise RuntimeError(f"PREPARED: {label} evidence hash is not authentic")
    return data


def reviewed_d53_source() -> dict[str, object]:
    """Authenticate the reviewed author branch and independent final review."""
    exact_record(P3_SOURCE_META, P3_SOURCE_META_SHA256, "D53 dispatcher metadata")
    author_report = exact_record(P3_SOURCE_AUTHOR_REPORT, P3_SOURCE_AUTHOR_REPORT_SHA256, "D53 author report")
    review_bytes = exact_record(P3_SOURCE_REVIEW, P3_SOURCE_REVIEW_SHA256, "D53 independent review")
    queue_bytes = exact_record(P3_SOURCE_QUEUE, P3_SOURCE_QUEUE_SHA256, "D53 normal dispatch record")
    meta = key_value_file(P3_SOURCE_META)
    if meta.get("name") != P3_SOURCE_WORKER or meta.get("repo") != "app":
        raise RuntimeError("PREPARED: D53 dispatcher metadata is not for the App worker")
    if meta.get("base") != "tl/integration" or meta.get("base_sha") != D53_BASE:
        raise RuntimeError("PREPARED: D53 dispatcher base is not exact")
    if queue_bytes.decode() != f"{P3_SOURCE[:9]}\n":
        raise RuntimeError("PREPARED: D53 remote source marker is not exact")
    if not author_report.startswith(b"Implemented P3 D53 in the three allowed paths:\n"):
        raise RuntimeError("PREPARED: D53 author report is not the fixed worker report")
    review = review_bytes.decode()
    required_review = (
        "## Result: PASS", P3_SOURCE, "sole parent", D53_BASE,
        "Full spec: `26c1ae", "D53 guard: `15b580",
        "No browser, live service, original journey, or full suite was run",
    )
    if any(marker not in review for marker in required_review):
        raise RuntimeError("PREPARED: independent D53 review evidence is incomplete")
    root = P3_SOURCE_REPO
    if root.is_symlink() or root == APP or not root.is_dir():
        raise RuntimeError("PREPARED: D53 source repository is unavailable or is a caller target")
    if git(root, "rev-parse", P3_SOURCE_BRANCH).decode().strip() != P3_SOURCE:
        raise RuntimeError("PREPARED: D53 author branch does not point to the reviewed source")
    if git(root, "show", "-s", "--format=%T", P3_SOURCE).decode().strip() != P3_TREE:
        raise RuntimeError("PREPARED: D53 source tree is not exact")
    if git(root, "show", "-s", "--format=%P", P3_SOURCE).decode().strip() != P3_PARENT:
        raise RuntimeError("PREPARED: D53 source parent is not exact")
    return {
        "checkout": str(root), "source": P3_SOURCE, "tree": P3_TREE, "parent": P3_PARENT,
        "parents": list(P3_PARENTS), "worker": P3_SOURCE_WORKER, "branch": P3_SOURCE_BRANCH,
        "dispatcher_meta": {"path": str(P3_SOURCE_META), "sha256": P3_SOURCE_META_SHA256, "name": meta["name"], "repo": meta["repo"], "base": meta["base"], "base_sha": meta["base_sha"]},
        "author_report": {"path": str(P3_SOURCE_AUTHOR_REPORT), "sha256": P3_SOURCE_AUTHOR_REPORT_SHA256},
        "source_review": {"path": str(P3_SOURCE_REVIEW), "sha256": P3_SOURCE_REVIEW_SHA256},
        "source_queue": {"path": str(P3_SOURCE_QUEUE), "sha256": P3_SOURCE_QUEUE_SHA256},
    }


def pure_proof_input(final: dict[str, object]) -> dict[str, object] | None:
    if os.environ.get(PURE_PROOF_MANIFEST_ENV):
        raise RuntimeError("PREPARED: caller-supplied pure proof manifests are unsupported")
    report = exact_record(P3_PURE_REPORT, P3_PURE_REPORT_SHA256, "pure D53 qualification report")
    exact_record(P3_PURE_META, P3_PURE_META_SHA256, "pure D53 worker metadata")
    ended_bytes = exact_record(P3_PURE_ENDED, P3_PURE_ENDED_SHA256, "pure D53 worker completion")
    queue_bytes = exact_record(P3_PURE_QUEUE, P3_PURE_QUEUE_SHA256, "pure D53 normal dispatch record")
    exact_record(P3_PURE_DONE, P3_PURE_DONE_SHA256, "pure D53 completion marker")
    meta = key_value_file(P3_PURE_META)
    if meta != {
        "name": P3_PURE_WORKER,
        "repo": "app",
        "base": "602f8b1f58593302829fb449d0ded62a91462a22",
        "base_sha": final["source"][:10],
        "model": "gpt-5.6-luna",
        "effort": "high",
        "heavy": "0",
        "worktree": f"/home/user/work/wt/{P3_PURE_WORKER}",
        "started": "2026-10-24T11:43:08Z",
    }:
        raise RuntimeError("PREPARED: pure D53 worker metadata facts are not exact")
    if queue_bytes.decode() != f"dispatched {P3_PURE_WORKER} in /home/user/work/wt/{P3_PURE_WORKER} (base {final['source']})\n":
        raise RuntimeError("PREPARED: pure D53 dispatch record is not exact")
    if ended_bytes != b"2026-10-24T11:49:28Z\n":
        raise RuntimeError("PREPARED: pure D53 worker completion is not exact")
    root = Path(str(final["source_checkout"]))
    if git(root, "rev-parse", P3_PURE_BRANCH).decode().strip() != final["source"]:
        raise RuntimeError("PREPARED: pure D53 worker branch is not the final source")
    report_text = report.decode()
    required_report = (
        "## PASS — P3/A2 D53 integrated qualification",
        f"HEAD={final['source']}", f"tree `{final['tree']}`",
        f"parents `{final['parents'][0]}` and `{final['parents'][1]}`",
        "D53 contains exactly three paths, byte-identical to `2357`",
        "23/23 passed", "Worker-authored D53 ledger:", "MERGED602f; integrated PASS.",
        "live GO remains unverified",
    )
    if any(marker not in report_text for marker in required_report):
        raise RuntimeError("PREPARED: pure D53 report facts are not exact")
    return {
        "status": "PASS", "worker": P3_PURE_WORKER, "branch": P3_PURE_BRANCH,
        "source": final["source"], "tree": final["tree"], "parents": final["parents"],
        "report": {"path": str(P3_PURE_REPORT), "sha256": P3_PURE_REPORT_SHA256},
        "meta": {"path": str(P3_PURE_META), "sha256": P3_PURE_META_SHA256},
        "ended": {"path": str(P3_PURE_ENDED), "sha256": P3_PURE_ENDED_SHA256, "at": ended_bytes.decode().strip()},
        "dispatch_queue": {"path": str(P3_PURE_QUEUE), "sha256": P3_PURE_QUEUE_SHA256},
    }


def final_source_input() -> dict[str, object]:
    """Capture final HOME by full SHA and fixed pure-proof provenance."""
    if os.environ.get(FINAL_SOURCE_MANIFEST_ENV):
        raise RuntimeError("PREPARED: generic final source manifests are unsupported")
    root = FINAL_HOME
    if root.is_symlink() or root == APP or not root.is_dir():
        raise RuntimeError("PREPARED: final HOME is unavailable or is a caller target")
    if any((root / name).exists() for name in ("caller-publication.py", "caller-custody.json")):
        raise RuntimeError("PREPARED: final HOME contains caller artifacts")
    if git(root, "status", "--porcelain=v1", "--untracked-files=all").strip():
        raise RuntimeError("PREPARED: final HOME is not clean")
    source = git(root, "rev-parse", "HEAD").decode().strip()
    tree = git(root, "show", "-s", "--format=%T", source).decode().strip()
    parents = tuple(git(root, "show", "-s", "--format=%P", source).decode().strip().split())
    if source != FINAL_HOME_SOURCE or tree != FINAL_HOME_TREE or parents != FINAL_HOME_REQUIRED_PARENTS:
        raise RuntimeError("PREPARED: final HOME is not the reviewed D52 plus D53 merge")
    checkout_receipt = exact_record(
        FINAL_HOME_CHECKOUT_RECEIPT,
        FINAL_HOME_CHECKOUT_RECEIPT_SHA256,
        "final HOME checkout receipt",
    )
    expected_checkout_receipt = (
        f"created /home/user/work/wt/app-pin-602f8b1f "
        f"(detached at {source}, KEEP)\n"
    ).encode()
    if checkout_receipt != expected_checkout_receipt:
        raise RuntimeError("PREPARED: final HOME checkout receipt identity is not exact")
    final = {
        "checkout": str(root), "source_checkout": str(root), "source": source, "tree": tree,
        "parent": " ".join(parents), "parents": list(parents), "worker": "final-home",
        "branch": "tl/integration", "service_snapshot": "UNKNOWN — created by the normal test-run after request",
        "checkout_receipt": {"path": str(FINAL_HOME_CHECKOUT_RECEIPT), "sha256": FINAL_HOME_CHECKOUT_RECEIPT_SHA256},
    }
    proof = pure_proof_input(final)
    final["pure_proof"] = proof
    final["pure_proof_status"] = "PRESENT" if proof else "MISSING — normal pure qualification receipt is not an input yet"
    return final


def source_custody(final: dict[str, object]) -> dict[str, object]:
    reviewed = reviewed_d53_source()
    root = Path(str(final.get("source_checkout", final["checkout"]))).resolve()
    source = str(final["source"])
    tree = str(final["tree"])
    parent = str(final["parent"])
    d53_paths = git(root, "diff", "--name-only", D53_BASE, P3_SOURCE).decode().splitlines()
    expected_d53_paths = sorted((
        "tests/e2e/local/support/gate5-fault-order.test.mjs",
        "tests/e2e/local/support/gate5-fault-order.ts",
        "tests/e2e/local/three-products.spec.ts",
    ))
    if d53_paths != expected_d53_paths:
        raise RuntimeError(f"PREPARED: D53 changed paths differ: {d53_paths!r}")
    spec = source_bytes(root, source, "tests/e2e/local/three-products.spec.ts")
    text = spec.decode()
    d53_spec = source_bytes(root, P3_SOURCE, "tests/e2e/local/three-products.spec.ts").decode()
    if digest(d53_spec.encode()) != D53_FULL_SPEC_SHA256:
        raise RuntimeError("PREPARED: reviewed D53 full spec hash is not authentic")

    def regions(value: str) -> dict[str, bytes]:
        gate5_start = "test('M2 real gate 5 (M1 real mounted path):"
        ordinary_start = "test('M2 ordinary extension batch"
        reset_start = "  const resetResponse = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);"
        reset_end = "  const recordedA = await expectV2History"
        gate5_offset = value.index(gate5_start)
        reset_offset = value.index(reset_start, gate5_offset)
        recorded_offset = value.index(reset_end, reset_offset)
        tail_end = value.index("\n", value.index(ordinary_start)) + 1
        return {
            "gate5_body": guarded(value, gate5_start, ordinary_start),
            "reset_block": value[reset_offset:recorded_offset].encode(),
            "canonical_tail": value[reset_offset:tail_end].encode(),
            "downstream_tail": guarded(value, reset_end, ordinary_start),
            "fault_helper": guarded(value, "async function faultFirstCommit(page: Page) {", "function accepted(post: CommitPost)"),
            "d53_guard": guarded(value, "    expect(wire.observed).toHaveLength(2);", "  });\n  const owner = await ownerWithTwoMountedDocuments(page, seed);"),
        }

    reviewed_regions = regions(d53_spec)
    final_regions = regions(text)
    expected_regions = {
        "gate5_body": D53_GATE5_BODY_SHA256,
        "reset_block": D53_RESET_BLOCK_SHA256,
        "canonical_tail": D53_CANONICAL_TAIL_SHA256,
        "downstream_tail": D53_DOWNSTREAM_TAIL_SHA256,
        "fault_helper": D53_FAULT_HELPER_SHA256,
        "d53_guard": D53_GUARD_SHA256,
    }
    for name, expected in expected_regions.items():
        if digest(reviewed_regions[name]) != expected or digest(final_regions[name]) != expected:
            raise RuntimeError(f"PREPARED: D53 {name} region is not exact")

    fingerprints = {}
    for path in REQUIRED_FINAL_SOURCE_PATHS:
        data = source_bytes(root, source, path)
        fingerprints[path] = {"blob": git_blob(data), "sha256": digest(data)}
    canonical = "".join(f"{p}\t{v['blob']}\t{v['sha256']}\n" for p, v in sorted(fingerprints.items()))
    required_paths = tuple(final.get("required_paths", REQUIRED_FINAL_SOURCE_PATHS))
    if not required_paths:
        raise RuntimeError("PREPARED: final reviewed source path set is empty")
    missing = []
    for path in required_paths:
        try:
            git(root, "cat-file", "-e", f"{source}:{path}")
        except subprocess.CalledProcessError:
            missing.append(path)
    if missing:
        raise RuntimeError(f"final source missing required reviewed paths: {missing}")
    observed_hashes = {path: digest(source_bytes(root, source, path)) for path in required_paths}
    reviewed_hashes = {
        path: digest(source_bytes(root, P3_SOURCE, path))
        for path in required_paths
    }
    if observed_hashes != reviewed_hashes:
        raise RuntimeError("PREPARED: final reviewed source bodies differ from the authenticated D53 source")
    tail = final_regions["canonical_tail"]
    p3 = final_regions["gate5_body"]
    parents = tuple(parent.split())
    if parents != tuple(FINAL_HOME_REQUIRED_PARENTS):
        raise RuntimeError("PREPARED: final HOME parent list changed")
    anchors = {P3_SOURCE: {"tree": P3_TREE, "parents": list(P3_PARENTS)}, source: {"tree": tree, "parents": list(parents)}}
    return {"source": source, "tree": tree, "parent": parent, "checkout": str(root),
            "parents": list(parents),
            "checkout_receipt": final.get("checkout_receipt"),
            "pure_proof": final.get("pure_proof"),
            "pure_proof_status": final.get("pure_proof_status"),
            "reviewed_source": reviewed, "anchors": anchors, "fingerprints": fingerprints, "fingerprint_count": len(fingerprints),
            "fingerprint_digest": digest(canonical.encode()), "required_paths": list(required_paths), "p3_whole": {"blob": git_blob(spec), "sha256": digest(spec)},
            "gate5_sha256": digest(p3), "reset_and_tail_sha256": digest(tail), "reviewed_hashes": reviewed_hashes,
            "protected_hashes": {
                "d50_tail_sha256": digest(tail), "p3_gate5_sha256": digest(p3),
                "d53": {name: digest(value) for name, value in final_regions.items()},
            }}

def custody_facts() -> dict[str, object]:
    provision_receipt = ORCH / "tests/provision" / f"{CHILD}.txt"
    child_receipt = ORCH / "queue/done" / f"childvenv-{CHILD}"
    remotion_receipt = ORCH / "queue/done" / f"runtime-{REMOTION}"
    child_root = Path("/home/user/work/bench-store/entries") / f"child-{CHILD_KEY}"
    require(git(AGENT_CHECKOUT, "rev-parse", "HEAD").decode().strip() == AGENT, "Agent checkout identity changed")
    require(git(AGENT_CHECKOUT, "show", "-s", "--format=%T", "HEAD").decode().strip() == "2deab1a1494fbccfce5e9235412bacb8a949c0cd", "Agent checkout tree changed")
    require(not git(AGENT_CHECKOUT, "status", "--porcelain=v1", "--untracked-files=all").strip(), "Agent checkout is dirty")
    require(git(RUNTIME_CHECKOUT, "rev-parse", "HEAD").decode().strip() == RUNTIME, "Runtime checkout identity changed")
    require(git(RUNTIME_CHECKOUT, "show", "-s", "--format=%T", "HEAD").decode().strip() == RUNTIME_TREE, "Runtime checkout tree changed")
    require(not git(RUNTIME_CHECKOUT, "status", "--porcelain=v1", "--untracked-files=all").strip(), "Runtime checkout is dirty")
    for receipt in (provision_receipt, child_receipt, remotion_receipt):
        require(receipt.is_file() and not receipt.is_symlink(), f"custody receipt is unavailable: {receipt}")
    provision = provision_receipt.read_text()
    child = child_receipt.read_text()
    remotion = remotion_receipt.read_text()
    require(f"agent_sha={AGENT}" in provision and f"runtime_sha={RUNTIME}" in provision, "Agent/Runtime provision receipt is not authentic")
    require(f"requested_name={CHILD}" in child and f"actual_agent={AGENT}" in child and f"actual_runtime={RUNTIME}" in child, "child receipt is not authentic")
    require(f"requested_name={REMOTION}" in remotion and f"requested_runtime_sha={RUNTIME}" in remotion, "Remotion receipt is not authentic")
    require("reuse=verified" in remotion, "Remotion receipt does not prove verified reuse")

    paths = git(RUNTIME_CHECKOUT, "ls-tree", "-r", "--name-only", RUNTIME, "packages/python/astrid_runtime_client/").decode().splitlines()
    require(len(paths) == 4, "runtime client file set changed")
    client_hashes = {}
    require(child_root.is_dir() and not child_root.is_symlink(), "child environment root is unavailable")
    child_site = child_root / "lib/python3.13/site-packages"
    for path in paths:
        runtime_bytes = git(RUNTIME_CHECKOUT, "show", f"{RUNTIME}:{path}")
        agent_path = path.removeprefix("packages/python/")
        require(runtime_bytes == git(AGENT_CHECKOUT, "show", f"{AGENT}:{agent_path}"), f"Agent/Runtime client differs: {path}")
        installed = child_site / agent_path
        require(installed.is_file() and installed.read_bytes() == runtime_bytes, f"installed client differs: {path}")
        client_hashes[path] = digest(runtime_bytes)

    backend_hashes = {}
    backend_paths = git(RUNTIME_CHECKOUT, "ls-tree", "-r", "--name-only", RUNTIME, "astrid_runtime/", "runtime_protocol/").decode().splitlines()
    for path in backend_paths:
        if path.endswith(".py"):
            data = git(RUNTIME_CHECKOUT, "show", f"{RUNTIME}:{path}")
            installed = child_site / path
            require(installed.is_file() and installed.read_bytes() == data, f"installed runtime backend differs: {path}")
            backend_hashes[path] = digest(data)
    require(len(backend_hashes) == 78, "runtime backend file set changed")
    require(digest(json.dumps(backend_hashes, sort_keys=True, separators=(",", ":")).encode()) == "d70ce25e13e02c1b805e682e7e098fba78cc6732f90c482a84bf074ab98ef2bb", "runtime backend digest changed")

    graph_root = REMOTION_ROOT / "node_modules/@banodoco/timeline-composition"
    graph_files = sorted(path for path in graph_root.rglob("*") if path.is_file())
    graph_hashes = {str(path.relative_to(graph_root)): digest(path.read_bytes()) for path in graph_files}
    require(len(graph_hashes) == 80, "Composition graph file set changed")
    return {"agent": AGENT, "agent_tree": "2deab1a1494fbccfce5e9235412bacb8a949c0cd", "runtime": RUNTIME, "runtime_tree": RUNTIME_TREE, "child": CHILD, "child_key": CHILD_KEY, "remotion": REMOTION, "remotion_tree": "b01dca9b3b24f54093c20b7c5657316f997725db", "provision_receipt_sha256": digest(provision_receipt.read_bytes()), "child_receipt_sha256": digest(child_receipt.read_bytes()), "remotion_receipt_sha256": digest(remotion_receipt.read_bytes()), "client_file_count": len(client_hashes), "client_hashes": client_hashes, "runtime_backend_file_count": len(backend_hashes), "runtime_backend_digest": digest(json.dumps(backend_hashes, sort_keys=True, separators=(",", ":")).encode()), "graph_file_count": len(graph_hashes), "graph_digest": digest(json.dumps(graph_hashes, sort_keys=True, separators=(",", ":")).encode()), "daemon_identity": "UNINFERRED_BY_SOURCE_PREPARATION"}


def selected_rows() -> tuple[bytes, dict[str, tuple[int, bytes]]]:
    raw = SUITES_FILE.read_bytes()
    lines = raw.splitlines(keepends=True)
    found = {}
    for index, line in enumerate(lines, 1):
        fields = line.split(None, 2)
        if len(fields) >= 2 and fields[0] == b"app" and fields[1].decode() in SUITES:
            require(fields[1].decode() not in found, "suite registry has duplicate selected rows")
            found[fields[1].decode()] = (index, line)
    require(set(found) == set(SUITES), "suite registry does not contain the exact selected rows")
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
    p2_key = f"app {P2_SUITE}"
    if len(previous_rows) != len(previous_keyed):
        raise RuntimeError("PREPARED: retained-before registry has duplicate row keys")
    if len(current_rows) != len(current_keyed):
        raise RuntimeError("PREPARED: current registry has duplicate retained row keys")
    common = set(previous_rows) & set(current_rows)
    changed = sorted(key for key in common if previous_rows[key] != current_rows[key] and key != p2_key)
    removed = sorted(set(previous_rows) - set(current_rows))
    added = sorted(set(current_rows) - set(previous_rows))
    if changed or added or removed != [EXPECTED_REMOVED_ROW]:
        raise RuntimeError(
            "PREPARED: retained-before registry comparison is broader than the known retirement: "
            f"removed={removed!r}, added={added!r}, changed={changed!r}"
        )
    previous_without_removed = b"".join(
        line for line in previous.splitlines(keepends=True)
        if not (
            line.strip()
            and not line.lstrip().startswith(b"#")
            and registry_row_key(line) in (EXPECTED_REMOVED_ROW, p2_key)
        )
    )
    current_without_p2 = b"".join(
        line for line in outside.splitlines(keepends=True)
        if not (
            line.strip()
            and not line.lstrip().startswith(b"#")
            and registry_row_key(line) == p2_key
        )
    )
    if previous_without_removed != current_without_p2:
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
        "parallel_p2_change": previous_rows.get(p2_key) != current_rows.get(p2_key),
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
            require(updated.count(marker) == 1, f"P{n} stage marker is not unique")
            updated = updated.replace(marker, assignment + marker, 1)
        return updated

    updated = inner
    native = 'if test "$SETUP_OK" = 1 && test "$P3FAIL" = ""; then "${ENV_BASE[@]}" timeout 300s node --import tsx'
    require(updated.count(native) == 1, f"P{n} native stage is not unique")
    updated = updated.replace(native, stage_assignment('$P3O/tests/$RUN_ID/playwright-output/p3/native-history') + native, 1)
    return updated


def add_tail_stages(tail: str, n: int) -> str:
    def select(root: str) -> str:
        return '{ PLAYWRIGHT_OUTPUT_DIR="' + root + '" && mkdir -p "$PLAYWRIGHT_OUTPUT_DIR" && export PLAYWRIGHT_OUTPUT_DIR; } && '
    if n == 2:
        needle = 'eval "$P2_ENV" && env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144'
        require(tail.count(needle) == 1, "P2 tail stage is not unique")
        return tail.replace(needle, 'eval "$P2_ENV" && ' + select('${PLAYWRIGHT_OUTPUT_DIR%/*}/original-body') + 'env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144', 1)
    mounted = '&& env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=4096'
    positions = [i for i in range(len(tail)) if tail.startswith(mounted, i)]
    require(len(positions) == 2, "P3 mounted stages are not unique")
    tail = tail[:positions[1] + 3] + select('${PLAYWRIGHT_OUTPUT_DIR%/*}/gate5') + tail[positions[1] + 3:]
    return tail[:positions[0] + 3] + select('$PLAYWRIGHT_OUTPUT_DIR/p3/mounted-readiness') + tail[positions[0] + 3:]


def extract_inner(line: bytes) -> tuple[str, str, str]:
    outer = line.decode().split(None, 2)[2].rstrip("\n")
    start = outer.index("$(bash -c ") + len("$(bash -c ")
    end = outer.index(")\" && eval", start)
    decoded = shlex.split(outer[start:end])
    require(len(decoded) == 1, "caller bash payload is not a single decoded argument")
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
    require(p2_line_sha256 == P2_INSTALLED_ROW_SHA256, "installed P2 row is not the authenticated current row")
    require(digest(rows[P3_SUITE][1]) == P3_INSTALLED_ROW_SHA256, "installed P3 row/body is not the authenticated current row")
    require(registry["outside_row_count"] == 248, "suite registry outside-row count changed")
    require(registry["outside_sha256"] == REGISTRY_OUTSIDE_SHA256, "suite registry outside rows are not the authenticated current snapshot")
    replacements = {}
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
        require(name == P3_SUITE, "unexpected selected suite row")
        text = line.decode()
        outer, inner, tail = extract_inner(line)
        app_match = re.search(rf"\bP{n}APP=([0-9a-f]{{40}})", inner)
        tree_match = re.search(rf"\bP{n}TREE=([0-9a-f]{{40}})", inner)
        parent_match = re.search(
            r"format=%P .*? = '([0-9a-f]{40} [0-9a-f]{40})'",
            inner,
        )
        if not app_match or not tree_match or not parent_match:
            raise RuntimeError("PREPARED: installed P3 source identity controls are incomplete")
        current_app = app_match.group(1)
        current_tree = tree_match.group(1)
        current_parent = parent_match.group(1)
        row_replacements = {
            current_app: str(final["source"]),
            current_tree: str(final["tree"]),
            current_parent: str(final["parent"]),
        }
        replacements.update(row_replacements)
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
            or current_app in updated
            or current_tree in updated
            or current_parent in updated
        ):
            raise RuntimeError("decoded mounted caller retained stale source identity")
        # Lock every changed final source file before any production stage.
        guarded_paths = set(re.findall(r"git hash-object -- ([^ ]+) 2>/dev/null", inner))
        extra = " ".join(
            f'test "$(git hash-object -- {shlex.quote(path)} 2>/dev/null)" = {info["blob"]} || p{n}fail final-source-blob;'
            for path, info in source["fingerprints"].items() if path not in guarded_paths
        )
        marker = f"if ! P{n}_ALLOCATED_PORT="
        require(updated.count(marker) == 1, "P3 allocated-port guard is not unique")
        if extra:
            updated = updated.replace(marker, extra + " " + marker, 1)
        require(f"P{n}A={AGENT}" in updated and f"P{n}R={RUNTIME}" in updated, "P3 Agent/Runtime identity controls changed")
        require(CHILD in updated and REMOTION in updated, "P3 retained child identities changed")
        native_start = inner.index("import { expect }")
        native_end = inner.index("finally { await harness.stop(); }")
        before_native = inner[native_start:native_end]
        # Keep the installed P3 shell byte-for-byte intact; this pass only
        # refreshes its App identity and source guards for the reviewed source.
        require(updated.count("PLAYWRIGHT_OUTPUT_DIR=") >= 2, "P3 output stage controls were removed")
        require("original-body-NOTRUN" in updated, "P3 original-body refusal marker was removed")
        updated_native_start = updated.index("import { expect }")
        updated_native_end = updated.index("finally { await harness.stop(); }")
        require(updated[updated_native_start:updated_native_end] == before_native, "P3 native body changed")
        require(f"P{n}_ALLOCATED_PORT" in updated and "original-body-NOTRUN" in updated, "P3 stage refusal controls changed")
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
        "status": "PREPARED",
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
            "final_home": source,
            "source_manifest": "not used; clean merged HOME identity is authoritative",
            "pure_proof": final.get("pure_proof_status"),
        },
        "missing_inputs": ["integrated P3 execution and daemon identity"],
        "negative_context": {"source_target_0644": "retained as source-only context", "wrong_artifacts": ["20674", "10144"], "wrong_artifacts_status": "preflight-only, originals NOTRUN; never reuse or relabel"},
        "retention_reuse": {"allowed": True, "condition": "decoded caller logic byte-identical after audited bindings/fingerprints/body hashes/log identity", "otherwise": "bounded real execution controls required", "qualified_stages": 60},
        "selected_source": {
            "dispatcher_worker": P3_SOURCE_WORKER,
            "checkout": str(final["checkout"]),
            "source_parents": list(final["parents"]),
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
        "status": "PREPARED",
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
