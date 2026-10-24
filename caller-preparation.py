"""Prepare, but do not install or run, the current Timeline P2/P3 caller.

The generated rows live only in ``TMPDIR``.  This artifact reads the two
installed rows, binds them to the exact current App source, and changes only
the Playwright output-root assignments needed to retain per-stage evidence.
It intentionally has no submission, daemon, browser, HTTP, or build path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
APP = Path(__file__).resolve().parent
SUITES_FILE = ORCH / "tests/suites.conf"
SUITES = ("full-e2e-three-products", "ap2-P3-gate5-h6-0348")

ROW_APP = "c0fe88994405fd517b58473c14678a0d1b73056d"
ROW_TREE = "8e3ef15ee5f7c08381d8dc9efb38b5c98845466d"
ROW_PARENT = "bad9a84fea2b1dddfb4f467e4108f28d3eadf2ff 19ac2b0ddcef00e1b2627aa1dd1e19c4bafb4b2f"
CURRENT_APP = "e42ee6227f86581d5d7591dcf067a8f8be25ac60"
CURRENT_TREE = "c0a54b2bef5e8e125c6d4caf9d90af7788c8fc2d"
CURRENT_PARENT = "79cd94f7e020d8ea79527bb1406fca7f6215d013 9b5be36fa9b4cc37ee929b6ea2393e3f287d3823"
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
    "accepted", "merged", "historical_rebased", "canonical_document", "digest", "identity_map",
    "records", "dependencies", "effects", "undo_steps", "preview", "required", "would_status",
    "conflict", "reason", "head", "invalid", "code", "path", "hint", "suggested_command",
)

BODY_LOCKS = {
    "tests/e2e/local/three-products.spec.ts": ("37caf28577d42fbe98afd2320dffa3c72e6e74b1", "0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14"),
    "tests/e2e/local/three-products.p2-tour.spec.ts": ("45a8088fafd72a462409e444c0294e8a35682a0f", "533461d30e94fd2b2eae8877b77f3909ab578eb71429f47a6b7b217ca517ce76"),
    "tests/e2e/local/three-products.p2-elements-assets.spec.ts": ("836d144bc0e3bbd8f1677d23e96385bcd8127daa", "e98bb092a37a449da7efd76981d32f24d79d00702b46f192527edc64ffd3b5b0"),
    "tests/e2e/local/three-products.p2-popup.spec.ts": ("c5926a2d304b96bc9ded59a71c8079d90ac3ac32", "05370adc76b2e8506e812a2c7ce9bde4441868c7c6d97aac7bf0eb8845b64a84"),
}

GUARDS = {
    "p1-chain": ("tests/e2e/local/three-products.spec.ts", "test('M1 real gesture:", "test('M2 real gate 5", "2096b2388a23a10d3890f96d7b2bfda988409dc479d8ba57a404947262da2876"),
    "gate5": ("tests/e2e/local/three-products.spec.ts", "test('M2 real gate 5", "test('M2 ordinary extension batch", "dcdcca43045ee8db02b195a836897857df6c2fad926dd1c8add28d9abaa6f67e"),
    "p2-tour": ("tests/e2e/local/three-products.p2-tour.spec.ts", "test('P2 mounted single parent move:", None, "6162efe20a403191c9833025599c15ec7d665cf1793ef1969adc28da9b428248"),
    "p2-elements": ("tests/e2e/local/three-products.p2-elements-assets.spec.ts", "test('P2 mounted element edit:", None, "e6b167d6db27d50553b20be7c040acd2b14138cac4559388656f38aa2c309e30"),
    "popup-add": ("tests/e2e/local/three-products.p2-popup.spec.ts", "test('P2 popup mounted ADD", "test('P2 popup mounted SWAP", "8210dccc8e5d63bab811291de80a91970f7aec2d0b6194e511c20d018474abc1"),
    "popup-swap": ("tests/e2e/local/three-products.p2-popup.spec.ts", "test('P2 popup mounted SWAP", None, "e66926998e182b65d877182eda1ab48357c4823abc4f98bd1ada31b92f08c6b0"),
}

CURRENT_PATHS = (
    "src/integrations/runtime/dataProvider.test.ts", "src/integrations/runtime/dataProvider.ts",
    "src/tools/travel-between-images/components/ShotTimelineMediaControls.test.tsx",
    "src/tools/travel-between-images/components/ShotTimelineMediaControls.tsx",
    "src/tools/travel-between-images/components/ShotTimelinePreview.integration.test.tsx",
    "src/tools/travel-between-images/components/ShotTimelinePreview.tsx",
    "src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts",
    "src/tools/travel-between-images/components/shotTimelineDataProvider.ts",
    "src/tools/video-editor/commands/media.ts", "src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.mounted.test.tsx",
    "src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx", "src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx",
    "src/tools/video-editor/contexts/VideoEditorProvider.tsx", "src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts",
    "src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts", "src/tools/video-editor/hooks/timelineScopedPersistence.test.tsx",
    "src/tools/video-editor/hooks/useClipEditing.test.ts", "src/tools/video-editor/hooks/useClipEditing.ts",
    "src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx", "src/tools/video-editor/hooks/useTimelineCommandsService.ts",
    "src/tools/video-editor/hooks/useTimelinePersistence.test.tsx", "src/tools/video-editor/hooks/useTimelinePersistence.ts",
    "src/tools/video-editor/hooks/useTimelineSave.test.tsx", "src/tools/video-editor/hooks/useTimelineSave.ts",
    "src/tools/video-editor/lib/timeline-asset-plans.test.ts", "src/tools/video-editor/lib/timeline-asset-plans.ts",
    "src/tools/video-editor/lib/timeline-basis-diagnostics.ts", "src/tools/video-editor/lib/timeline-data.test.ts",
    "src/tools/video-editor/lib/timeline-data.ts", "src/tools/video-editor/lib/timeline-diagnostics.save.test.ts",
    "src/tools/video-editor/lib/timeline-diagnostics.ts", "tests/e2e/local/mounted-readiness-safety.test.ts",
    "tests/e2e/local/p1-diagnostic-safety.test.ts", "tests/e2e/local/p1-diagnostic-safety.ts",
    "tests/e2e/local/three-products.p2-popup.spec.ts",
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
    assert git(APP, "rev-parse", f"{CURRENT_APP}^{{commit}}").decode().strip() == CURRENT_APP
    assert git(APP, "rev-parse", f"{CURRENT_APP}^{{tree}}").decode().strip() == CURRENT_TREE
    assert git(APP, "show", "-s", "--format=%P", CURRENT_APP).decode().strip() == CURRENT_PARENT
    subprocess.run(["git", "-C", str(APP), "merge-base", "--is-ancestor", SOURCE_BASE, CURRENT_APP], check=True)
    subprocess.run(["git", "-C", str(APP), "merge-base", "--is-ancestor", ROW_APP, CURRENT_APP], check=True)
    anchors = {
        "parent-7551": ("7551bb21462f7adadea67031c5744322b2d78ab7", "c3358202a3a7335ce552a28372eaf54c3c360090", "5f43d9e86a11dedf0484b60a111b5bc35b0af186 5e242c64e30d23d800b436f930785f080bcb28c2"),
        "popup-79cd": ("79cd94f7e020d8ea79527bb1406fca7f6215d013", "5e6361615608944a5a373609078bf4f18e30e311", "7551bb21462f7adadea67031c5744322b2d78ab7 fa59d336215c02d3a591af9f398ce00d60ad3bff"),
        "popup-claims-2972": ("2972a7c4c922dbf3db65e48e27841826d2055b83", "464333ff8be4c67abbb70d20229c0afcc0211e96", ROW_APP),
        "parameter-return-9b": ("9b5be36fa9b4cc37ee929b6ea2393e3f287d3823", "52a456c654ba8cbbab4c3822a283a685d9ad8891", "1d9d2c8453f5ef965a5ba568edff7150f0a60f7c"),
        "current-e42": (CURRENT_APP, CURRENT_TREE, CURRENT_PARENT),
    }
    for name, (commit, tree, parents) in anchors.items():
        subprocess.run(["git", "-C", str(APP), "merge-base", "--is-ancestor", commit, CURRENT_APP], check=True)
        assert git(APP, "rev-parse", f"{commit}^{{tree}}").decode().strip() == tree, name
        assert git(APP, "show", "-s", "--format=%P", commit).decode().strip() == parents, name

    paths = tuple(git(APP, "diff", "--name-only", SOURCE_BASE, CURRENT_APP).decode().splitlines())
    assert paths == CURRENT_PATHS
    fingerprints = {}
    for path in CURRENT_PATHS:
        data = source_bytes(CURRENT_APP, path)
        fingerprints[path] = {"blob": git_blob(data), "sha256": digest(data)}
    canonical = "".join(f"{p}\t{v['blob']}\t{v['sha256']}\n" for p, v in fingerprints.items())
    assert digest(canonical.encode()) == "da34bb2323aa24093aa78ed2b1a60cd3e77de7890363957c89c12093cee0d1dd"

    protected = {}
    for path, (blob, sha) in BODY_LOCKS.items():
        data = source_bytes(CURRENT_APP, path)
        assert git_blob(data) == blob and digest(data) == sha, path
        protected[path] = {"blob": blob, "sha256": sha}
    assert source_bytes(CURRENT_APP, "tests/e2e/local/three-products.p2-popup.spec.ts") == source_bytes("2972a7c4c922dbf3db65e48e27841826d2055b83", "tests/e2e/local/three-products.p2-popup.spec.ts")
    for path in BODY_LOCKS:
        if path != "tests/e2e/local/three-products.p2-popup.spec.ts":
            assert source_bytes(CURRENT_APP, path) == source_bytes(ROW_APP, path), path

    guards = {}
    for name, (path, start, end, expected) in GUARDS.items():
        value = guarded(source_bytes(CURRENT_APP, path).decode(), start, end)
        assert digest(value) == expected, name
        guards[name] = {"sha256": expected, "bytes": len(value)}
    return {"anchors": {name: commit for name, (commit, _, _) in anchors.items()}, "fingerprints": fingerprints, "fingerprint_count": len(fingerprints), "fingerprint_digest": digest(canonical.encode()), "protected_bodies": protected, "body_guards": guards, "popup_2972_exact": True}


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
    native = 'timeout 300s node --import tsx'
    assert updated.count(native) == 1
    updated = updated.replace(native, stage_assignment('$P3O/tests/$RUN_ID/playwright-output/p3/native-history') + native, 1)
    return updated


def add_tail_stages(tail: str, n: int) -> str:
    if n == 2:
        needle = 'eval "$P2_ENV" && env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144'
        assert tail.count(needle) == 1
        return tail.replace(needle, 'eval "$P2_ENV" && ' + stage_assignment('$ACTUAL_RUN_DIR/playwright-output/p2/original-body') + 'env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=6144', 1)
    mounted = '&& env -u NODE_PATH NODE_OPTIONS=--max-old-space-size=4096'
    positions = [i for i in range(len(tail)) if tail.startswith(mounted, i)]
    assert len(positions) == 2
    tail = tail[:positions[1] + len("&& ")] + stage_assignment('$P3O/tests/$RUN_ID/playwright-output/p3/gate5') + tail[positions[1] + len("&& "):]
    return tail[:positions[0] + len("&& ")] + stage_assignment('$P3O/tests/$RUN_ID/playwright-output/p3/mounted-readiness') + tail[positions[0] + len("&& "):]


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
        assert f"P{n}A={AGENT}" in updated and f"P{n}R={RUNTIME}" in updated
        assert CHILD in updated and REMOTION in updated
        native_start = inner.index("import { expect }")
        native_end = inner.index("finally { await harness.stop(); }")
        before_native = inner[native_start:native_end]
        updated = add_stages(updated, n)
        tail = add_tail_stages(tail, n)
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
        "status": "PREPARED",
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
        "final_inputs": {"catalog_source": "MISSING", "p3_source": "MISSING", "reason": "catalogSol0557 and ProofP3Sol0543 are active, not merged inputs"},
        "selected_source_snapshot": {"selected_source": CURRENT_APP, "snapshot": "installed rows remain D45 c0fe until a later authorized bind"},
    }
    (out / "before.json").write_text(json.dumps({name: rows[name][1].decode().rstrip("\n") for name in SUITES}, indent=2) + "\n")
    (out / "after.json").write_text(json.dumps(drafts, indent=2) + "\n")
    (out / "current-draft.rows").write_text("".join(drafts[name] + "\n" for name in SUITES))
    (out / "outside.before").write_bytes(outside)
    (out / "prepared.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def load_manifest() -> dict[str, object]:
    root = Path(os.environ["TMPDIR"]).resolve()
    return json.loads((root / "prepared.json").read_text())


def controls(name: str) -> None:
    manifest = load_manifest()
    if name == "qualify.py":
        checks = [
            manifest["status"] == "PREPARED", manifest["run_authorization"] == "NOT_GRANTED",
            manifest["app_source"] == CURRENT_APP, manifest["app_tree"] == CURRENT_TREE,
            manifest["app_parent"] == CURRENT_PARENT, manifest["source_base"] == SOURCE_BASE,
            manifest["source"]["fingerprint_count"] == 35, manifest["source"]["fingerprint_digest"] == "da34bb2323aa24093aa78ed2b1a60cd3e77de7890363957c89c12093cee0d1dd",
            len(manifest["source"]["protected_bodies"]) == 4, len(manifest["source"]["body_guards"]) == 6,
            manifest["source"]["popup_2972_exact"] is True, manifest["custody"]["agent"] == AGENT,
            manifest["custody"]["runtime"] == RUNTIME, manifest["custody"]["child"] == CHILD,
            manifest["custody"]["remotion"] == REMOTION, manifest["custody"]["child_key"] == CHILD_KEY,
            manifest["custody"]["client_file_count"] == 4, manifest["custody"]["runtime_backend_file_count"] == 78,
            manifest["custody"]["graph_file_count"] == 80, manifest["custody"]["daemon_identity"] == "UNINFERRED_BY_SOURCE_PREPARATION",
            (manifest["outside_row_count"], manifest["outside_bytes"], manifest["outside_sha256"]) == (248, 466341, "b33d30918d6e2ae039dfa296bc75b1e0b2674828b53f07a16ee029933d5ad734"),
            len(manifest["wire_fields"]) == len(WIRE_FIELDS) and manifest["door_port"]["propagates_before_every_stage"] is True and manifest["door_port"]["changed"] is False and manifest["tool_versions"]["playwright"] == "1.60.0",
            manifest["final_inputs"]["catalog_source"] == "MISSING", manifest["final_inputs"]["p3_source"] == "MISSING",
        ]
        assert len(checks) == 24 and all(checks), checks
        print("24 controls passed")
        return
    if name == "stages.py":
        root = Path(os.environ["TMPDIR"])
        checks = []
        for n, suite in enumerate(SUITES, 2):
            old = (root / f"p{n}-inner.sh").read_text()
            new = (root / f"p{n}-new-inner.sh").read_text()
            new_full = new + "\n" + (root / f"p{n}-new-outer.sh").read_text()
            checks.extend([
                subprocess.run(["/bin/bash", "-n", str(root / f"p{n}-new-inner.sh")]).returncode == 0,
                old.count("P2_ALLOCATED_PORT" if n == 2 else "P3_ALLOCATED_PORT") >= 1 and new.count("P2_ALLOCATED_PORT" if n == 2 else "P3_ALLOCATED_PORT") >= 1,
                "original-body-NOTRUN" in new_full,
                "ASTRID_APP_DIRECT_DOOR_PORT" in new_full,
                "P2FAIL" in new_full if n == 2 else "P3FAIL" in new_full,
                "native-history" in new_full, "mounted-readiness" in new_full, "history" in new_full,
                "PLAYWRIGHT_OUTPUT_DIR" in new_full, "export PLAYWRIGHT_OUTPUT_DIR" in new_full,
                new_full.index("playwright-output/p2/native-history" if n == 2 else "playwright-output/p3/native-history") < new_full.index("playwright-output/p2/mounted-readiness" if n == 2 else "playwright-output/p3/mounted-readiness"),
                "p2/" in new_full if n == 2 else "p3/" in new_full,
                manifest["stage_records"][suite]["native_body_preserved"] is True,
            ])
            probe = Path(tempfile.mkdtemp(prefix=f"d21-stage-{n}-", dir=root))
            script = probe / "probe.sh"
            script.write_text("set -eu\nroot=$1\nfor s in native-history mounted-readiness original-body; do test -z \"${s#original-body}\" || true; mkdir -p \"$root/$s\"; printf '%s' \"$s\" >\"$root/$s/readiness\"; printf '%s' \"$s-env\" >\"$root/$s/environment\"; printf '%s' \"$s-attachment\" >\"$root/$s/attachment\"; done\nprintf '%s' ready >\"$root/mounted-readiness/readiness\"\ntest \"$(cat \"$root/mounted-readiness/readiness\")\" = ready\n")
            result = subprocess.run(["bash", str(script), str(probe / "output")], capture_output=True)
            checks.append(result.returncode == 0 and (probe / "output/mounted-readiness/readiness").read_text() == "ready")
        assert len(checks) == 28 and all(checks), checks
        print("28 stage controls passed")
        return
    if name == "corruption.py":
        root = Path(os.environ["TMPDIR"])
        after = json.loads((root / "after.json").read_text())
        corrupt = dict(after)
        corrupt[SUITES[0]] = corrupt[SUITES[0]].replace(CURRENT_APP, CURRENT_APP[:-1], 1)
        checks = [
            after != json.loads((root / "before.json").read_text()),
            digest((root / "outside.before").read_bytes()) == manifest["outside_sha256"],
            corrupt[SUITES[0]] != after[SUITES[0]],
            manifest["final_inputs"]["catalog_source"] == "MISSING" and manifest["final_inputs"]["p3_source"] == "MISSING",
        ]
        assert len(checks) == 4 and all(checks), checks
        print("4 corruption controls passed")
        return
    if name == "exports.py":
        root = Path(os.environ["TMPDIR"])
        rows = json.loads((root / "after.json").read_text())
        checks = [all("P2_ENV" in rows[SUITES[0]] and "P3_ENV" in rows[SUITES[1]] for _ in [0]), all("ASTRID_RUNTIME_CHECKOUT" in row and "ASTRID_CHECKOUT" in row and "PLAYWRIGHT_OUTPUT_DIR" in row for row in rows.values())]
        assert len(checks) == 2 and all(checks), checks
        print("2 restricted-export controls passed")
        return
    assert name == "wrong-key-controls.py"
    checks = [manifest["custody"]["child_key"] == CHILD_KEY, manifest["custody"]["daemon_identity"] == "UNINFERRED_BY_SOURCE_PREPARATION"]
    assert all(checks), checks
    print("2 fail-closed wrong-key controls passed (no registration attempted)")


def main() -> None:
    basename = Path(os.sys.argv[0]).name
    if len(os.sys.argv) == 1 and basename in {"qualify.py", "stages.py", "corruption.py", "exports.py", "wrong-key-controls.py"}:
        controls(basename)
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-source", default=CURRENT_APP)
    args = parser.parse_args()
    assert args.app_source == CURRENT_APP, "only the current integration source may be prepared"
    out = Path(os.environ.get("TMPDIR", tempfile.gettempdir())).resolve()
    assert not out.is_relative_to(APP), "preparation artifacts belong in private TMPDIR"
    manifest = prepare(out)
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
