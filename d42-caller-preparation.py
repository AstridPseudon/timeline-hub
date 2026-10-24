"""Render an exact App caller draft without installing rows or submitting work.

This is a preparation artifact only.  It refreshes the retained P2/P3 caller
from the current merged App source and leaves the shared suite configuration
untouched.  Runtime is intentionally an old D41 preparation input here; a
qualified D42 Runtime source, checkout, child and Remotion receipts are still
required before the manager may bind or submit the pair.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess


ORCH = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch")
APP = Path(__file__).resolve().parent
SUITES = ("full-e2e-three-products", "ap2-P3-gate5-h6-0348")

# The live rows still carry this prior caller.  Current App is the exact
# preparation base; later exact App descendants are accepted only after their
# source/tree/parent and every changed-file fingerprint pass below.
ROW_APP = "804134d74782d40855146aa568ff289200b79142"
ROW_TREE = "8437e47666853b62e03a58af3716235346316fba"
ROW_PARENT = "22efcda3da4005f8663c078439ff0edbfade69be 42db156ede0d0192ec4176a2edd29b366b552a8d"
CURRENT_APP = "c0fe88994405fd517b58473c14678a0d1b73056d"
CURRENT_TREE = "8e3ef15ee5f7c08381d8dc9efb38b5c98845466d"
CURRENT_PARENT = "bad9a84fea2b1dddfb4f467e4108f28d3eadf2ff 19ac2b0ddcef00e1b2627aa1dd1e19c4bafb4b2f"
ELEMENT_BASE = "f90e708b379145ac456924742cc51c187ed6e0c6"
AGENT = "079580ca46af77e0292d49dc34386b25c8391f99"
D41_RUNTIME = "37eb6c7bdb79dcae2523883e66b5cea5be721ffd"
D41_RUNTIME_TREE = "be4114705127f9ee9e86b26cd6de3f467e771c01"
AGENT_CHECKOUT = Path("/home/user/work/wt/agt-pin-079580ca")

WIRE_FIELDS = (
    "api_version", "project_id", "timeline_id", "base_revision_id", "base_publication_id",
    "commands", "label", "steps", "id", "intent", "tags", "command_ordinals", "patch",
    "reads", "merge", "Idempotency-Key", "dry_run", "source", "rationale", "group_id",
    "data", "receipt", "accepted", "merged", "historical_rebased", "canonical_document",
    "digest", "identity_map", "records", "dependencies", "effects", "undo_steps", "preview",
    "required", "would_status", "conflict", "reason", "head", "invalid", "code", "path",
    "hint", "suggested_command",
)

# These are the reviewed cumulative source anchors that must remain in the
# actual App ancestry.  The full identities are deliberate custody guards.
SOURCE_ANCHORS = {
    "element-join-e492": ("e492d963ba51e037d25ad667b857c1fe592ef384", "77ff7e42c24ba6913ed98bf12bb66e20f1ef7947", "f90e708b379145ac456924742cc51c187ed6e0c6 6cd7eca303c49bb31ecd0abc0382cb3d2682dfe3"),
    "element-handoff-f90": (ELEMENT_BASE, "afc357e3a2f4d7e0de6c51a8d36081fd450a1c87", "a64587176d4132bf2ad3a05ab0fe656913625c8d 2c786c161f81bf658ebdc8c3e8472d532d195e66"),
    "parent-current-19c": ("19c4839d81f83aa6b6ef2a9f2d895d10140a27a6", "ccea4662586596ffb8af699644226b6edda0475c", "c768058cd0687bde91666c8265a6b9e5063a8e4d 6bd1eb0d04004ad291cd0de5bea23c01892b3eeb"),
    "popup-binding-bad9": ("bad9a84fea2b1dddfb4f467e4108f28d3eadf2ff", "8847a53dd7bd5220673e2486dc286454800de722", "19c4839d81f83aa6b6ef2a9f2d895d10140a27a6 0267ed4f03ff1a9e4766b2e69e94726b80825ade"),
    "single-child-c0fe": (CURRENT_APP, CURRENT_TREE, CURRENT_PARENT),
}

CURRENT_CHANGED_FINGERPRINTS = {
    "src/integrations/runtime/dataProvider.test.ts": ("fa2e0d79a564a0f3087b9f345f844459d08fba4d", "ed3dbb4d817778b44ca5ab86430165ee13175ff5e11767d4ec0479e3f58e2780"),
    "src/integrations/runtime/dataProvider.ts": ("5c830fe2b4661c9722ad22960f752c968604acd1", "9213ed6694cef931fe84fa3c83fda0b06ed02532c1b9b6271ef48c32d38f8988"),
    "src/tools/travel-between-images/components/ShotTimelinePreview.integration.test.tsx": ("38e5de7dfd34cb9b1c17ad577280ce433cfabdb0", "f8025fa4e436b0b7c23700b577bee7a796e45b1ce7513384d60426d7038ca65d"),
    "src/tools/travel-between-images/components/ShotTimelinePreview.tsx": ("857f3a3f4d54b67fb90103177c2087a97f757371", "9e3c6a5e98a27e8c1b03e17043fe00a48a2ef1efa179d7f6584bab2de402500c"),
    "src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts": ("04d7f622d470a55b9cafe93157436943b271c89a", "65b2ed02c202e607999c89b1b94b6f4cb8d83828b2418a09016fa9fbc5bd7d2a"),
    "src/tools/travel-between-images/components/shotTimelineDataProvider.ts": ("210560a10c69147f8b12694dfa2abf68f42763e7", "2e483a4a367427da9b1a64e5da7105c8b81901676298570b6fde60eedb438881"),
    "src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts": ("23326c55ce994ce549d89c92e4d4e26b00abf1bd", "bd1aed1551ccc682b48459c56c1a8b12de43d8e1c9df246459251ec30e20d347"),
    "src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts": ("bf167a51aae200cc313e6093bb5ed272439d83f0", "33b7a69528014bb91263fa42a79a08e75f9b33ea679baad8a7870839bb51bb58"),
    "src/tools/video-editor/hooks/timelineScopedPersistence.test.tsx": ("2c91758bb91e0c9a229f236b8fac6aa3ddea515d", "e01f3fefc240bdbf9cdd3d96f0063c9f4f298904204bc7c42cacfa41b9ffca15"),
    "src/tools/video-editor/hooks/useClipEditing.test.ts": ("c3ddd87a3a56b67d210a8849a900fb5abf3a41bc", "d6383588fe6200214e7fe408ecdc6e2dc992856d21ab0fb253e838dc7048d4be"),
    "src/tools/video-editor/hooks/useClipEditing.ts": ("c9f28f5de9bc9434c1cbf7e482a645f1dfe61be3", "778d1782da0077b4d5c8637ab17edbb4798c51bdf4c127a5caeee46f2645e025"),
    "src/tools/video-editor/hooks/useTimelinePersistence.test.tsx": ("421b672231941d8054f18cc7f628bf8fd6cb2273", "bc0187f72f5f2b6d9895d767090635e9d1ecce5ff2837540df44fb9ae4f17281"),
    "src/tools/video-editor/hooks/useTimelinePersistence.ts": ("db10176d1325b5f4b5a65dab29892d2163174381", "c572fef3399d9e306c0826609b6dfb77fcd869dd2ce1f1cdd09b708187d13154"),
    "src/tools/video-editor/hooks/useTimelineSave.test.tsx": ("131512cfabcf7f9230f865fe22fa4be1fd89fb6b", "864b0362025e25b207c6f77a120d397857d51e8b7355aef01f53918295599e86"),
    "src/tools/video-editor/hooks/useTimelineSave.ts": ("454e4f930dc5d938df5fbc40144ca4684cf51c1e", "42c03078fab6a141c7044966b59e1244b3c3fd636ed848715a6c382996b0e0b8"),
    "src/tools/video-editor/lib/timeline-basis-diagnostics.ts": ("1009c855a1432d1406670a474a1c755c3569dd76", "133598aa93892ce18c1a914025e5e90e1b2bb1dc4b3e37f24e09eaefc6f3bb3a"),
    "src/tools/video-editor/lib/timeline-diagnostics.save.test.ts": ("c21a8f5f0792cf009aac8bcb1cd7246652f5ef4c", "07b0fb4c278cba0b822fd16b6f9d3ac7d99594438dccdac45a1d5cb061ec49dc"),
    "src/tools/video-editor/lib/timeline-diagnostics.ts": ("2965696d89b6206a1aa4b9d9941f401ffd3aa021", "78e3c9692029461aa09d9c387ea6d1de406ec13dcd49326d10c3af34ea443066"),
    "tests/e2e/local/mounted-readiness-safety.test.ts": ("4db4bc28b0187af9d07839072c4727c05018835b", "da722beae0271285626e7d4212d171bc2f33e6b46da1a85e48c2d64fef4cc107"),
    "tests/e2e/local/p1-diagnostic-safety.test.ts": ("0c7e076d7d4984b612f9e95c14489cba0e75d3cc", "78a9fdc396bc30078ac1567164cfb89366369aaf7af9701e43d2e24b38337247"),
    "tests/e2e/local/p1-diagnostic-safety.ts": ("33ececd04952772d39700ec97ccebf273cadb9ff", "5b04016e6c76a40479662ff97fd2ea48e708c4a69e366108a74a770cfb4b137c"),
    "tests/e2e/local/three-products.p2-popup.spec.ts": ("8072fcee4da01fc5dc39852c645af959251ae153", "722b7e9f938cefe0dfe625fabc89b4486b6968a56e6bc727e28c73b3883f8b8e"),
}

PROTECTED = {
    "tests/e2e/local/three-products.spec.ts": {"blob": "37caf28577d42fbe98afd2320dffa3c72e6e74b1", "sha256": "0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14"},
    "tests/e2e/local/three-products.p2-tour.spec.ts": {"blob": "45a8088fafd72a462409e444c0294e8a35682a0f", "sha256": "533461d30e94fd2b2eae8877b77f3909ab578eb71429f47a6b7b217ca517ce76"},
    "tests/e2e/local/three-products.p2-elements-assets.spec.ts": {"blob": "836d144bc0e3bbd8f1677d23e96385bcd8127daa", "sha256": "e98bb092a37a449da7efd76981d32f24d79d00702b46f192527edc64ffd3b5b0"},
    "tests/e2e/local/three-products.p2-popup.spec.ts": {"blob": "8072fcee4da01fc5dc39852c645af959251ae153", "sha256": "722b7e9f938cefe0dfe625fabc89b4486b6968a56e6bc727e28c73b3883f8b8e"},
}

GUARDS = {
    "p1-chain": ("tests/e2e/local/three-products.spec.ts", "test('M1 real gesture:", "test('M2 real gate 5", "2096b2388a23a10d3890f96d7b2bfda988409dc479d8ba57a404947262da2876"),
    "gate5": ("tests/e2e/local/three-products.spec.ts", "test('M2 real gate 5", "test('M2 ordinary extension batch", "dcdcca43045ee8db02b195a836897857df6c2fad926dd1c8add28d9abaa6f67e"),
    "p2-tour": ("tests/e2e/local/three-products.p2-tour.spec.ts", "test('P2 mounted single parent move:", None, "6162efe20a403191c9833025599c15ec7d665cf1793ef1969adc28da9b428248"),
    "p2-elements": ("tests/e2e/local/three-products.p2-elements-assets.spec.ts", "test('P2 mounted element edit:", None, "e6b167d6db27d50553b20be7c040acd2b14138cac4559388656f38aa2c309e30"),
    "popup-add": ("tests/e2e/local/three-products.p2-popup.spec.ts", "test('P2 popup mounted ADD", "test('P2 popup mounted SWAP", "8210dccc8e5d63bab811291de80a91970f7aec2d0b6194e511c20d018474abc1"),
    "popup-swap": ("tests/e2e/local/three-products.p2-popup.spec.ts", "test('P2 popup mounted SWAP", None, "e66926998e182b65d877182eda1ab48357c4823abc4f98bd1ada31b92f08c6b0"),
}


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


def assert_source_custody(app_source: str) -> dict[str, object]:
    assert git(APP, "rev-parse", f"{app_source}^{{commit}}").decode().strip() == app_source
    subprocess.run(["git", "-C", str(APP), "merge-base", "--is-ancestor", CURRENT_APP, app_source], check=True)
    subprocess.run(["git", "-C", str(APP), "merge-base", "--is-ancestor", ROW_APP, app_source], check=True)
    assert git(APP, "rev-parse", f"{CURRENT_APP}^{{tree}}").decode().strip() == CURRENT_TREE
    assert git(APP, "show", "-s", "--format=%P", CURRENT_APP).decode().strip() == CURRENT_PARENT

    for name, (commit, tree, parents) in SOURCE_ANCHORS.items():
        subprocess.run(["git", "-C", str(APP), "merge-base", "--is-ancestor", commit, app_source], check=True)
        assert git(APP, "rev-parse", f"{commit}^{{tree}}").decode().strip() == tree, name
        assert git(APP, "show", "-s", "--format=%P", commit).decode().strip() == parents, name

    current_paths = git(APP, "diff", "--name-only", ELEMENT_BASE, CURRENT_APP).decode().splitlines()
    assert set(current_paths) == set(CURRENT_CHANGED_FINGERPRINTS), (set(current_paths) ^ set(CURRENT_CHANGED_FINGERPRINTS))
    fingerprints: dict[str, dict[str, str]] = {}
    for path, (expected_blob, expected_sha) in CURRENT_CHANGED_FINGERPRINTS.items():
        data = source_bytes(CURRENT_APP, path)
        assert git_blob(data) == expected_blob, path
        assert digest(data) == expected_sha, path
        fingerprints[path] = {"blob": expected_blob, "sha256": expected_sha}

    final_fingerprints: dict[str, dict[str, str]] = {}
    for path in git(APP, "diff", "--name-only", CURRENT_APP, app_source).decode().splitlines():
        data = source_bytes(app_source, path)
        final_fingerprints[path] = {"blob": git_blob(data), "sha256": digest(data)}

    for path, expected in PROTECTED.items():
        data = source_bytes(CURRENT_APP, path)
        assert git_blob(data) == expected["blob"], path
        assert digest(data) == expected["sha256"], path
        if path != "tests/e2e/local/three-products.p2-popup.spec.ts":
            assert data == source_bytes(ROW_APP, path), path
        assert data == source_bytes(app_source, path), path

    old_popup = source_bytes(ROW_APP, "tests/e2e/local/three-products.p2-popup.spec.ts").decode()
    current_popup = source_bytes(CURRENT_APP, "tests/e2e/local/three-products.p2-popup.spec.ts").decode()
    old_line = '    await dialog.locator(`.clip-action[data-clip-id="${TARGET_CLIP_ID}"]`).click();'
    new_line = '    await dialog.locator(`.clip-action[data-clip-id="${popup.sharedOccurrenceId}:${TARGET_CLIP_ID}"]`).click();'
    assert old_popup.count(old_line) == 2 and current_popup.count(new_line) == 2
    assert current_popup == old_popup.replace(old_line, new_line)
    reviewed_popup = source_bytes("adf39c533adec77e55e11a61ca79a821a9752c59", "tests/e2e/local/three-products.p2-popup.spec.ts").decode()
    assert reviewed_popup == current_popup
    diff = list(difflib.unified_diff(old_popup.splitlines(), current_popup.splitlines(), lineterm=""))
    assert sum(line.startswith(("+", "-")) and not line.startswith(("+++", "---")) for line in diff) == 4

    guard_hashes = {}
    for name, (path, start, end, expected) in GUARDS.items():
        value = guarded(source_bytes(CURRENT_APP, path).decode(), start, end)
        assert digest(value) == expected, name
        guard_hashes[name] = {"sha256": expected, "bytes": len(value)}
    return {"current_changed_files": fingerprints, "final_changed_files": final_fingerprints, "body_guards": guard_hashes, "popup_diff": "two reviewed ADD/SWAP selectors"}


def main() -> None:
    if len(os.sys.argv) == 1 and Path(os.sys.argv[0]).name in {"qualify.py", "stages.py", "extra.py", "exports.py", "wrong-key-controls.py"}:
        run_control(Path(os.sys.argv[0]).name)
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-source", required=True)
    parser.add_argument("--runtime-source", required=True)
    parser.add_argument("--runtime-checkout", required=True, type=Path)
    parser.add_argument("--child", required=True)
    parser.add_argument("--remotion", required=True)
    args = parser.parse_args()
    out = Path(os.environ["TMPDIR"]).resolve()
    assert out != APP and not out.is_relative_to(APP), "drafts belong in private TMPDIR"
    assert re.fullmatch(r"[0-9a-f]{40}", args.app_source)
    assert re.fullmatch(r"[0-9a-f]{40}", args.runtime_source)
    assert re.fullmatch(r"[a-z0-9-]+", args.child) and re.fullmatch(r"[a-z0-9-]+", args.remotion)
    runtime = args.runtime_checkout.resolve()
    assert runtime == args.runtime_checkout and git(runtime, "rev-parse", "HEAD").decode().strip() == args.runtime_source
    assert not git(runtime, "status", "--porcelain=v1", "--untracked-files=all").strip()
    subprocess.run(["git", "-C", str(runtime), "merge-base", "--is-ancestor", D41_RUNTIME, args.runtime_source], check=True)
    runtime_changes = git(runtime, "diff", "--name-only", D41_RUNTIME, args.runtime_source).decode().splitlines()
    assert all(path == "runtime_protocol/timeline_commit_store.py" or path.startswith("tests/") for path in runtime_changes)
    client_paths = git(runtime, "ls-tree", "-r", "--name-only", args.runtime_source, "packages/python/astrid_runtime_client/").decode().splitlines()
    assert len(client_paths) == 4
    client_tuple = {}
    for path in client_paths:
        data = git(runtime, "show", f"{args.runtime_source}:{path}")
        assert data == git(runtime, "show", f"{D41_RUNTIME}:{path}")
        agent_path = path.removeprefix("packages/python/")
        assert data == git(AGENT_CHECKOUT, "show", f"{AGENT}:{agent_path}")
        client_tuple[path] = digest(data)
    custody = assert_source_custody(args.app_source)

    replacements = {ROW_APP: args.app_source, ROW_TREE: git(APP, "rev-parse", f"{args.app_source}^{{tree}}").decode().strip(), ROW_PARENT: git(APP, "show", "-s", "--format=%P", args.app_source).decode().strip(), D41_RUNTIME: args.runtime_source, D41_RUNTIME_TREE: git(runtime, "rev-parse", "HEAD^{tree}").decode().strip(), "/home/user/work/wt/rt-pin-37eb6c7b": str(runtime), "venv-agent-child-app-ready-079-37eb-0256": args.child, "agent-remotion-app-ready-079-37eb-0258": args.remotion}
    rows = {}
    lines = (ORCH / "tests/suites.conf").read_bytes().splitlines(keepends=True)
    for line in lines:
        fields = line.split(None, 2)
        if len(fields) >= 2 and fields[0] == b"app" and fields[1].decode() in SUITES:
            rows[fields[1].decode()] = line
    assert tuple(rows) == SUITES
    outside = b"".join(line for line in lines if line not in rows.values())
    result = {}
    for index, (name, line) in enumerate(rows.items(), 2):
        outer = line.decode().split(None, 2)[2].rstrip("\n")
        a = outer.index("$(bash -c ") + len("$(bash -c ")
        b = outer.index(")\" && eval", a)
        decoded = shlex.split(outer[a:b])
        assert len(decoded) == 1
        inner = decoded[0]
        updated = inner
        tail = outer[b:]
        for before, after in replacements.items():
            updated = updated.replace(before, after)
            tail = tail.replace(before, after)
        assert f"P{index}_ALLOCATED_PORT" in updated
        native_start = inner.index("import { expect }")
        native_end = inner.index("finally { await harness.stop(); }")
        assert inner[native_start:native_end] == updated[native_start:native_end]
        new_outer = outer[:a] + shlex.quote(updated) + tail
        for label, data in (("inner", inner), ("outer", outer), ("new-inner", updated), ("new-outer", new_outer)):
            path = out / f"p{index}-{label}.sh"
            path.write_text(data)
            subprocess.run(["/bin/bash", "-n", str(path)], check=True)
        result[name] = "app " + name + " " + new_outer

    child_key = digest(json.dumps(["child", AGENT, args.runtime_source, client_tuple], sort_keys=True, separators=(",", ":")).encode())
    manifest = {"status": "PREPARED_ONLY", "app_source": args.app_source, "app_tree": replacements[ROW_TREE], "app_parent": replacements[ROW_PARENT], "runtime_source": args.runtime_source, "runtime_tree": replacements[D41_RUNTIME_TREE], "runtime_input": "old-D41-preparation" if args.runtime_source == D41_RUNTIME else "unreleased-D42-candidate-input", "agent_source": AGENT, "source_anchors": {k: v[0] for k, v in SOURCE_ANCHORS.items()}, "wire_fields": WIRE_FIELDS, "client_tuple": client_tuple, "planned_child_key": child_key, "child_key_is_deferred": True, **custody, "live_row_sha256": {name: digest(row) for name, row in rows.items()}, "draft_row_sha256": {name: digest((row + "\n").encode()) for name, row in result.items()}, "outside_sha256": digest(outside), "outside_lines": len(lines) - len(rows)}
    (out / "before.json").write_text(json.dumps({k: v.decode().rstrip("\n") for k, v in rows.items()}))
    (out / "after.json").write_text(json.dumps(result))
    (out / "d42-draft.rows").write_text("".join(row + "\n" for row in result.values()))
    (out / "outside.before").write_bytes(outside)
    (out / "prepared.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


def run_control(name: str) -> None:
    """Run the finite, source/argv-only controls from an isolated TMPDIR copy."""
    root = Path(os.environ["TMPDIR"]).resolve()
    prepared = root / "prepared.json"
    if not prepared.is_file():
        prepared = root.parent / "prepared.json"
    manifest = json.loads(prepared.read_text())
    if name == "qualify.py":
        checks = [
            manifest["status"] == "PREPARED_ONLY",
            manifest["app_source"] == CURRENT_APP,
            manifest["app_tree"] == CURRENT_TREE,
            manifest["runtime_source"] == D41_RUNTIME,
            len(manifest["source_anchors"]) == 5,
            len(manifest["current_changed_files"]) == 22,
            len(manifest["body_guards"]) == 6,
            manifest["popup_diff"] == "two reviewed ADD/SWAP selectors",
            manifest["body_guards"]["p1-chain"]["sha256"] == GUARDS["p1-chain"][3],
            manifest["body_guards"]["gate5"]["sha256"] == GUARDS["gate5"][3],
            manifest["body_guards"]["p2-tour"]["sha256"] == GUARDS["p2-tour"][3],
            manifest["body_guards"]["p2-elements"]["sha256"] == GUARDS["p2-elements"][3],
            manifest["body_guards"]["popup-add"]["sha256"] == GUARDS["popup-add"][3],
            manifest["body_guards"]["popup-swap"]["sha256"] == GUARDS["popup-swap"][3],
            manifest["current_changed_files"]["tests/e2e/local/three-products.p2-popup.spec.ts"]["blob"] == PROTECTED["tests/e2e/local/three-products.p2-popup.spec.ts"]["blob"],
            manifest["current_changed_files"]["src/tools/video-editor/hooks/useTimelineSave.ts"]["sha256"] == CURRENT_CHANGED_FINGERPRINTS["src/tools/video-editor/hooks/useTimelineSave.ts"][1],
            manifest["agent_source"] == AGENT,
            manifest["child_key_is_deferred"] is True,
            isinstance(manifest["live_row_sha256"], dict),
            isinstance(manifest["draft_row_sha256"], dict),
            manifest["outside_lines"] == 248,
            manifest["app_parent"] == CURRENT_PARENT,
            len(PROTECTED) == 4,
            manifest["source_anchors"]["single-child-c0fe"] == CURRENT_APP,
        ]
        assert len(checks) == 24 and all(checks), checks
        print("24 controls passed")
        return
    if name == "stages.py":
        checks = []
        for n in (2, 3):
            before = (prepared.parent / f"p{n}-inner.sh").read_text()
            after = (prepared.parent / f"p{n}-new-inner.sh").read_text()
            checks.extend([
                subprocess.run(["/bin/bash", "-n", str(prepared.parent / f"p{n}-new-inner.sh")]).returncode == 0,
                f"P{n}_ALLOCATED_PORT" in after,
                before[before.index("import { expect }"):before.index("finally { await harness.stop(); }")] == after[after.index("import { expect }"):after.index("finally { await harness.stop(); }")],
                len(after) > 1000,
                (prepared.parent / f"p{n}-outer.sh").is_file(),
                (prepared.parent / f"p{n}-new-outer.sh").is_file(),
                f"P{n}FAIL" in after,
                f"P{n}O" in after,
                "history" in after,
                "undo" in after,
                "harness" in after,
                "node" in after,
                "python" in after,
                "export" in after,
            ])
        assert len(checks) == 28 and all(checks), checks
        print("28 controls passed")
        return
    if name == "extra.py":
        rows = json.loads((prepared.parent / "after.json").read_text())
        checks = [
            tuple(rows) == SUITES,
            (prepared.parent / "d42-draft.rows").read_text().count("app ") == 2,
            digest((ORCH / "tests/suites.conf").read_bytes()) != digest((prepared.parent / "d42-draft.rows").read_bytes()),
            manifest["outside_sha256"] == "b33d30918d6e2ae039dfa296bc75b1e0b2674828b53f07a16ee029933d5ad734",
        ]
        assert all(checks), checks
        print("4 controls passed")
        return
    if name == "exports.py":
        rows = json.loads((prepared.parent / "after.json").read_text())
        checks = [
            all("P2_ENV=" in row or "P3_ENV=" in row for row in rows.values()),
            all("ASTRID_RUNTIME_CHECKOUT" in row and "ASTRID_CHECKOUT" in row for row in rows.values()),
        ]
        assert all(checks), checks
        print("2 restricted-export controls passed")
        return
    assert name == "wrong-key-controls.py"
    checks = [
        manifest["child_key_is_deferred"] is True,
        not any("c0fe" in path.name for directory in ("pending", "done") for path in (ORCH / "queue" / directory).iterdir()),
    ]
    assert all(checks), checks
    print("2 fail-closed wrong-key controls passed (no registration attempted)")


if __name__ == "__main__":
    main()
