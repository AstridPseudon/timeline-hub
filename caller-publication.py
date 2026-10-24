"""Prepare the exact final Timeline P2/P3 caller for offline qualification.

The generated rows live only in ``TMPDIR``. This artifact reads the two
installed rows, binds their source/body guards to the reviewed final App,
and assigns independent Playwright output children to each stage.
It intentionally has no submission, daemon, browser, HTTP, or build path.
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

ROW_APP = "b2380539c5545661954d2794976631312ee1d939"
ROW_TREE = "eab53458e86b210b050673bdcd039d29b0a511ca"
ROW_PARENT = "ae7acc1c2e1ae802b15110b9a7b099c77c9186da 172033a677472b0435498310babdbf1524b74bfd"
ROW_SOURCE = "c0fe88994405fd517b58473c14678a0d1b73056d"
CURRENT_APP = "66354161950d1e747965c095ea97b881d2592708"
CURRENT_TREE = "9a37265f0286128df7e6240a9df9877d959474af"
CURRENT_PARENT = "b2380539c5545661954d2794976631312ee1d939"
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
    "commands", "label", "steps", "id", "intent", "tags", "command_ordinals", "patch", "reads",
    "merge", "Idempotency-Key", "dry_run", "source", "rationale", "group_id", "data", "receipt",
    "accepted", "merged", "rebased", "canonical_document", "digest", "identity_map",
    "records", "dependencies", "effects", "history", "undo_steps", "preview", "required", "would_status",
    "conflict", "reason", "head", "invalid", "code", "path", "hint", "suggested_command",
)


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def source_bytes(commit: str, path: str) -> bytes:
    return git(APP, "show", f"{commit}:{path}")


def guarded(text: str, start: str, end: str | None) -> bytes:
    a = text.index(start)
    b = text.index(end, a) if end else len(text)
    return text[a:b].encode()


def source_custody() -> dict[str, object]:
    assert git(APP, "rev-parse", "HEAD").decode().strip() == CURRENT_APP
    assert git(APP, "rev-parse", f"{CURRENT_APP}^{{tree}}").decode().strip() == CURRENT_TREE
    assert git(APP, "show", "-s", "--format=%P", CURRENT_APP).decode().strip() == CURRENT_PARENT
    paths = git(APP, "diff", "--name-only", SOURCE_BASE, CURRENT_APP).decode().splitlines()
    fingerprints = {}
    for path in paths:
        data = source_bytes(CURRENT_APP, path)
        assert (APP / path).read_bytes() == data, path
        fingerprints[path] = {"blob": git_blob(data), "sha256": digest(data)}
    canonical = "".join(f"{p}\t{v['blob']}\t{v['sha256']}\n" for p, v in fingerprints.items())
    spec = source_bytes(CURRENT_APP, "tests/e2e/local/three-products.spec.ts")
    original = source_bytes(ROW_SOURCE, "tests/e2e/local/three-products.spec.ts")
    assert git_blob(spec).startswith("9091d36f") and digest(spec) == "741bcfb986fe0e80bbf81a40f741418991ed7e59cda59e578060b818e7d7cd94"
    import_line = b"import { assertGate5ResetPrecondition } from './support/gate5-reset-precondition.ts';\n"
    start = spec.index(b"  const preconditionBase = await history(harness, seed3);", spec.index(b"test('M2 real gate 5"))
    end = spec.index(b"  const resetResponse = page.waitForResponse", start)
    assert spec[:start].replace(import_line, b"") + spec[end:] == original
    tail = spec[spec.index(b"  const resetResponse = page.waitForResponse", start):spec.index(b"\n", spec.index(b"test('M2 ordinary extension batch")) + 1]
    assert digest(tail) == "f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67"
    gate = guarded(spec.decode(), "test('M2 real gate 5", "test('M2 ordinary extension batch").rstrip() + b"\n"
    assert digest(gate) == "c7735569a90ec9acdc2d66feed8747d3480c3b6d0e5acd3e22316ba84f9489e8"
    p1 = source_bytes(CURRENT_APP, "tests/e2e/local/three-products.p1-chain.spec.ts")
    assert p1 == source_bytes(ROW_APP, "tests/e2e/local/three-products.p1-chain.spec.ts")
    assert digest(p1).startswith("50960dd2")
    for path in ("tests/e2e/local/three-products.p2-tour.spec.ts", "tests/e2e/local/three-products.p2-elements-assets.spec.ts"):
        assert source_bytes(CURRENT_APP,path) == source_bytes(ROW_APP,path)
    assert source_bytes(CURRENT_APP,"tests/e2e/local/three-products.p2-popup.spec.ts") == source_bytes("2972a7c4c922dbf3db65e48e27841826d2055b83","tests/e2e/local/three-products.p2-popup.spec.ts")
    anchors = {}
    for commit in (ROW_SOURCE, ROW_APP, "e42ee6227f86581d5d7591dcf067a8f8be25ac60", "172033a677472b0435498310babdbf1524b74bfd", CURRENT_APP):
        subprocess.run(["git", "-C", str(APP), "merge-base", "--is-ancestor", commit, CURRENT_APP], check=True)
        anchors[commit] = {"tree": git(APP,"show","-s","--format=%T",commit).decode().strip(), "parents":git(APP,"show","-s","--format=%P",commit).decode().strip()}
    return {"anchors":anchors,"fingerprints":fingerprints,"fingerprint_count":len(fingerprints),"fingerprint_digest":digest(canonical.encode()),"p3_whole": {"blob":git_blob(spec),"sha256":digest(spec)},"gate5_sha256":digest(gate),"reset_and_tail_sha256":digest(tail),"p1_sha256":digest(p1),"reviewed_setup_removed_equals_original":True}

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


def prepare(out: Path) -> dict[str, object]:
    source = source_custody()
    custody = custody_facts()
    raw, rows = selected_rows()
    outside = b"".join(line for i, line in enumerate(raw.splitlines(keepends=True), 1) if i not in {rows[name][0] for name in SUITES})
    assert len(raw.splitlines(keepends=True)) - 2 == 248 and len(outside) == 466341 and digest(outside) == "b33d30918d6e2ae039dfa296bc75b1e0b2674828b53f07a16ee029933d5ad734"
    replacements = {ROW_APP: CURRENT_APP, ROW_TREE: CURRENT_TREE, ROW_PARENT: CURRENT_PARENT}
    # Recompute guards from genuine Git blobs, including previously unchanged files.
    for path in git(APP,"ls-tree","-r","--name-only",ROW_APP).decode().splitlines():
        if any(path in rows[name][1].decode() for name in SUITES):
            old = source_bytes(ROW_APP,path)
            new = source_bytes(CURRENT_APP,path)
            replacements[git_blob(old)] = git_blob(new)
            replacements[digest(old)] = digest(new)
    drafts = {}
    stage_records = {}
    for n, name in enumerate(SUITES, 2):
        line = rows[name][1]
        text = line.decode()
        assert ROW_APP in text and ROW_TREE in text and ROW_PARENT in text
        outer, inner, tail = extract_inner(line)
        updated = inner
        for before, after in replacements.items():
            updated = updated.replace(before, after)
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
        # The selected rows are the already-installed, qualified 0609 callers.
        # Keep their six-stage shell byte-for-byte intact; this pass only refreshes
        # the App identity and the source guards for the reviewed successor.
        assert updated.count("PLAYWRIGHT_OUTPUT_DIR=") >= 2
        assert "original-body-NOTRUN" in updated
        updated_native_start = updated.index("import { expect }")
        updated_native_end = updated.index("finally { await harness.stop(); }")
        assert updated[updated_native_start:updated_native_end] == before_native
        assert f"P{n}_ALLOCATED_PORT" in updated and "original-body-NOTRUN" in updated
        new_outer = outer[:outer.index("$(bash -c ") + len("$(bash -c ")] + shlex.quote(updated) + tail
        for label, data in ((f"p{n}-inner.sh", inner), (f"p{n}-new-inner.sh", updated), (f"p{n}-outer.sh", outer), (f"p{n}-new-outer.sh", new_outer)):
            (out / label).write_text(data)
            subprocess.run(["/bin/bash", "-n", str(out / label)], check=True)
        drafts[name] = f"app {name} {new_outer}"
        stage_records[name] = {"argv": "argc=2", "native_body_preserved": True, "output_stages": ["native-history", "mounted-readiness", "original-body" if n == 2 else "gate5"]}

    node = subprocess.check_output(["node", "--version"], text=True).strip()
    npm = subprocess.check_output(["npm", "--version"], text=True).strip()
    playwright = json.loads((APP / "node_modules/@playwright/test/package.json").read_text())["version"]

    manifest = {
        "status": "QUALIFIABLE",
        "replacements": replacements,
        "run_authorization": "NOT_GRANTED",
        "app_source": CURRENT_APP, "app_tree": CURRENT_TREE, "app_parent": CURRENT_PARENT,
        "source_base": SOURCE_BASE, "source": source, "custody": custody,
        "live_row_sha256": {name: digest(rows[name][1]) for name in SUITES},
        "draft_row_sha256": {name: digest((drafts[name] + "\n").encode()) for name in SUITES},
        "outside_row_count": 248, "outside_bytes": len(outside), "outside_sha256": digest(outside),
        "wire_fields": WIRE_FIELDS,
        "stage_records": stage_records,
        "door_port": {"allocation": ["P2_ALLOCATED_PORT", "P3_ALLOCATED_PORT"], "propagates_before_every_stage": True, "changed": False},
        "tool_versions": {"node": node, "npm": npm, "playwright": playwright},
        "final_inputs": {"catalog_source": CURRENT_APP, "p3_source": CURRENT_APP},
        "selected_source_snapshot": {"selected_source": CURRENT_APP, "snapshot": "service may select exact source or a synthetic same-tree commit with exactly one parent equal to selected_source; daemon identity is uninferred"},
    }
    (out / "before.json").write_text(json.dumps({name: rows[name][1].decode().rstrip("\n") for name in SUITES}, indent=2) + "\n")
    (out / "after.json").write_text(json.dumps(drafts, indent=2) + "\n")
    (out / "current-draft.rows").write_text("".join(drafts[name] + "\n" for name in SUITES))
    (out / "outside.before").write_bytes(outside)
    (out / "prepared.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(prepare(Path(os.environ["TMPDIR"]).resolve()), indent=2))

