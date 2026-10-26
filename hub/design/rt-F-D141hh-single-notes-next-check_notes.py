#!/usr/bin/env python3
"""Build and verify private D141hh single-note successors."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141hh-single-notes-next")
EVIDENCE = ROOT / "evidence"
BASE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141gg-parent-notes-1148/evidence")
DESIGN = Path("/home/user/timeline-hub/hub/design")
BOARD = DESIGN / "BOARD-HEADER.md"
TERMINAL = DESIGN / "app-D141gg-single-terminal-publication-1157.json"
CUSTODY = DESIGN / "app-D141gg-single-custody-publication-1159.json"
RENDERER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-final-unit-notes-input-0849-delivery-build.py")
INPUTS = {"candidate-README.template.md": "90f8bab9d056eecc04ce390d996ab3dd03782200ce83e8b6c67f4b1e103e7b84", "candidate-gate-results.md": "ddebb463b95df97f077236a8e6cbfe5c560dcb7effc8d48af4efcaa22e500bc1"}
PUBLICATION_HASHES = {TERMINAL: "08d6573b2d1c00223ac306b8caf9caaaa8e047803d51f202e4e97a330515af97", CUSTODY: "c67e717facfc968a584a489e86b1e24b49840a1dc10f029c62187568255ff928"}
RENDERER_HASH = "ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{label}: expected regular non-symlink: {path}")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode != 0o644:
        raise AssertionError(f"{label}: expected mode 0644, got {mode:04o}: {path}")
    return path.read_bytes()


def read_json(path: Path, label: str) -> object:
    try:
        return json.loads(regular(path, label))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{label}: invalid JSON: {path}") from exc


def publication(path: Path) -> dict[str, object]:
    raw = regular(path, f"publication {path.name}")
    actual = digest(raw)
    if actual != PUBLICATION_HASHES[path]:
        raise AssertionError(f"publication drift at {path}: {actual}")
    data = json.loads(raw)
    if not isinstance(data, dict) or not isinstance(data.get("files"), list):
        raise AssertionError(f"{path}: missing files list")
    files = []
    seen = set()
    for number, item in enumerate(data["files"], 1):
        if not isinstance(item, dict) or not all(k in item for k in ("published", "bytes", "sha256")):
            raise AssertionError(f"{path}: malformed file binding {number}")
        name = Path(item["published"]).name
        if name in seen:
            raise AssertionError(f"{path}: duplicate basename {name}")
        seen.add(name)
        local = DESIGN / name
        raw_original = regular(local, f"published original {number}")
        actual_original = digest(raw_original)
        if len(raw_original) != item["bytes"] or actual_original != item["sha256"]:
            raise AssertionError(f"published original {number}: declared binding does not match {local}")
        files.append({"basename": name, "declared_path": item["published"], "path": str(local), "bytes": len(raw_original), "sha256": actual_original})
    return {"path": str(path), "bytes": len(raw), "sha256": actual, "publication": data, "files": files}


def file_map(source: dict[str, object]) -> dict[str, Path]:
    return {item["basename"]: Path(item["path"]) for item in source["files"]}


def verify_sources() -> dict[str, object]:
    terminal = publication(TERMINAL)
    custody = publication(CUSTODY)
    tf = file_map(terminal)
    cf = file_map(custody)
    receipt = read_json(tf["app-P-D141gg-single-scoped-controller-1145-controller-receipt.json"], "terminal receipt")
    results = read_json(tf["app-P-D141gg-single-scoped-controller-1145-results.json"], "terminal results")
    review = read_json(cf["app-P-D141gg-single-custody-review-1156-review.json"], "custody review")
    tp = terminal["publication"]
    cp = custody["publication"]
    if tp.get("body_verdict") != "PASS pending independent custody" or tp.get("actual_worker_exit") != 0:
        raise AssertionError("terminal publication verdict/exit drifted")
    if tp.get("normal_short_id") != 24271 or tp.get("preflight_short_id") != 9320:
        raise AssertionError("terminal short IDs drifted")
    if "future paths relocated" not in tp.get("packet_path_deviation", "") or "prospective" not in tp.get("raw_KEEP", ""):
        raise AssertionError("terminal procedural disclosures drifted")
    if cp.get("verdict") != "FAIL_CUSTODY" or cp.get("normal_result") != "PASS0/257s" or cp.get("original_preserved") is not True:
        raise AssertionError("custody publication verdict/result/preservation drifted")
    source = review["source"]
    tuple_expected = {"app": ("82e9e13ddf1d7ec6c736521b2eb091dca9877598", "6a6e49eb4461b5ca1a7fa1247653bc794f26d710"), "agent": ("ecdc242ed9b673f641759ecf029f95e89a2c6f92", "d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735"), "runtime": ("95d98f038320d5d46bd679ac000ab3e15825c935", "78df31d62c5b9ba4c84dee4ea346e43a767718c1"), "composition": ("635f4de06fda22a85fc2e4cfc764d0153a4c9f40", "5ab5191a296980a0a6bcd1178ab6902d6478a148")}
    for name, (head, tree) in tuple_expected.items():
        if (source[name]["head"], source[name]["tree"]) != (head, tree):
            raise AssertionError(f"{name} tuple drifted")
    if source["all_four_detached_clean"] is not True or source["product_sources_changed"] is not False:
        raise AssertionError("source cleanliness facts drifted")
    preflight = results["requests"]["preflight"]
    normal = results["requests"]["normal"]
    if (preflight["status"], preflight["exit_code"]) != ("pass", 0) or (normal["status"], normal["exit_code"]) != ("pass", 0):
        raise AssertionError("single-scope-2 request result drifted")
    if results["body_verdict"] != "PASS" or results["test_status"] != "PASS" or results["attempt_scope"] != "single-scope-2":
        raise AssertionError("single terminal result drifted")
    if results["wait"]["same_id_only"] is not True or results["wait"]["exit_code"] != 0 or results["no_retry_or_resubmit"] is not True:
        raise AssertionError("single wait/retry facts drifted")
    if results["summary"]["normal_duration_seconds"] != 257 or results["summary"]["normal_passed_tests"] != ["D28 mounted readiness", "P2 mounted transition None single"]:
        raise AssertionError("single summary facts drifted")
    if results["native_submit"]["invocations"] != 1 or results["native_submit"]["exit_code"] != 0:
        raise AssertionError("native submit facts drifted")
    predicate = review["predicate"]
    for key in ("v2_request", "raw_transition_absence", "opaque_fields_preserved", "order_preserved", "reload", "guarded_undo", "history"):
        if predicate[key] is not True:
            raise AssertionError(f"predicate {key} is not PASS")
    if predicate["legacy_writes"] != 0 or predicate["test_source_sha256"] != "83948c53c7990824fce81be7f0db2b4f947837c66a827abf2ffb08492f09bee4":
        raise AssertionError("predicate source/facts drifted")
    custody_facts = review["custody"]
    raw_keep = custody_facts["raw_keep"]
    if any(raw_keep[key] is not False for key in ("preflight_preexisting", "normal_preexisting", "retroactive_claim")):
        raise AssertionError("late raw KEEP facts drifted")
    if custody_facts["recipe_path_relocation_only"] is not True or custody_facts["retry_or_resubmit"] is not False or review["verdict"] != "FAIL_CUSTODY":
        raise AssertionError("custody finding facts drifted")
    if "earlier wrong-SHA attempt remains distinct NOTRUN" not in review["decision"] or "No rerun or repair is authorized" not in review["decision"]:
        raise AssertionError("original NOTRUN/no-reproof limit drifted")
    board = regular(BOARD, "BOARD-HEADER").decode()
    for marker in ("- D141hh (12:00Z): **SINGLE 24271 PASS ACCEPTED** with both procedural gaps disclosed", "the raw KEEP was added after the request, and only the future output paths were relocated", "- D141hh-a (12:05Z): root fix in the kit. bin/request-test now honours TEST_KEEP=<reason>", "BEFORE the request is queued"):
        if marker not in board:
            raise AssertionError(f"BOARD-HEADER marker missing: {marker}")
    return {"terminal": terminal, "custody": custody, "receipt": receipt, "results": results, "review": review, "board_sha256": digest(board.encode())}


def controlled_results() -> list[dict[str, object]]:
    return [{"name": n, "tip": f"{i:040x}", "base": f"{i + 4:040x}", "shortstat": "", "split": {"product": [0, 0, 0], "tests": [0, 0, 0]}, "ranged": True, "ahead": 0, "applied": 0, "status": "PASS", "seconds": 0.0, "applied_tree": f"{i + 8:040x}", "bundle_tree": f"{i + 12:040x}", "want_tree": f"{i + 16:040x}", "problems": []} for i, n in enumerate(("agent", "runtime", "app", "composition"), 1)]


def render_only(template: Path, gates: Path) -> dict[str, object]:
    source = regular(RENDERER, "delivery-build renderer")
    if digest(source) != RENDERER_HASH:
        raise AssertionError("delivery-build renderer hash drifted")
    spec = importlib.util.spec_from_file_location("d141hh_delivery_build", RENDERER)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load delivery-build renderer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rendered = module.render_readme(controlled_results(), str(template), str(gates))
    if any(token in rendered for token in ("{{UTC}}", "{{REPO_SUMMARY}}", "{{REPO_SECTIONS}}", "{{GATE_RESULTS}}")) or rendered.count("```") % 2 or rendered.count("D141hh single PASS accepted") != 2:
        raise AssertionError("controlled render placeholders/fences/disclosures drifted")
    missing = Path(tempfile.mkdtemp(prefix="rt-F-D141hh-render-", dir="/tmp")) / "missing-gates.md"
    fallback = module.render_readme(controlled_results(), str(template), str(missing))
    if "_Not recorded yet. Paste the gate results here before handing over" not in fallback:
        raise AssertionError("render fallback changed")
    return {"function_only": True, "function": "render_readme", "caller": str(RENDERER), "caller_sha256": digest(source), "controlled_inputs": ["agent", "runtime", "app", "composition"], "placeholders_resolved": True, "balanced_fences": True, "disclosure_occurrences": 2, "fallback_placeholder_behavior": True, "rendered_sha256": digest(rendered.encode()), "fallback_sha256": digest(fallback.encode())}


def suffixes(sources: dict[str, object]) -> tuple[str, str]:
    r = sources["results"]
    v = sources["review"]
    p = v["source"]
    tuple_text = ", ".join(f"{name.title()} `{p[name]['head']}` (tree `{p[name]['tree']}`)" for name in ("app", "agent", "runtime")) + f", and Composition `{p['composition']['head']}` (tree `{p['composition']['tree']}`)"
    preflight = r["requests"]["preflight"]["id"]
    normal = r["requests"]["normal"]["id"]
    duration = r["summary"]["normal_duration_seconds"]
    raw_at = v["custody"]["raw_keep"]["added_at"]
    trace = v["trace"]
    common = (f"the exact four-repository tuple {tuple_text}; preflight `{preflight}` PASS/exit 0 and normal `{normal}` PASS/exit 0 in {duration} s, with D28 mounted readiness and the exact P2 mounted transition-None single predicate PASS. "
              f"The accepted service PASS retains both procedural gaps: the raw KEEP was added prospectively at `{raw_at}` after the request/body window, and only the future output, plan, lock, stdout and stderr paths were relocated; the custody review found no product-affecting deviation and the raw evidence is intact. "
              "Independent custody remains `FAIL_CUSTODY` with CUSTODY-RAW-KEEP and CUSTODY-RECIPE-PATH, so the author result, custody findings and Main disposition remain distinct; this is not a custody PASS. "
              "The original first single no-body attempt from 1135 remains NOTRUN, was not retargeted or reproofed, and is not claimed repaired; D141hh-a TEST_KEEP applies to future submits only and does not backfill historical custody. "
              f"Native custody recorded {trace['native_samples']} samples (`{trace['native_min_available_bytes']}`–`{trace['native_max_available_bytes']}` bytes, maximum gap {trace['native_max_gap_seconds']} s, no 4 GB stop); author sampling is session-only ({trace['author_samples']} samples, `{trace['author_min_available_bytes']}`–`{trace['author_max_available_bytes']}` bytes). ")
    return ("\n\n## D141hh single PASS accepted with both procedural gaps (bounded documentary note)\n\nMain D141hh at 12:00 accepts the author result for " + common + "Main accepts this bounded service PASS with both gaps disclosed and no reproof, and makes no final REG0, build, ZIP or selector claim.\n", "\n\n## D141hh single PASS accepted with both procedural gaps (bounded documentary note)\n\nAuthor result: on " + common + "Main's accepted disposition is bounded to this service result, with no final REG0, build, ZIP or selector claim.\n")


def verify_candidates(sources: dict[str, object]) -> dict[str, object]:
    readme_suffix, gate_suffix = suffixes(sources)
    expected = {"candidate-README.template.md": readme_suffix.encode(), "candidate-gate-results.md": gate_suffix.encode()}
    candidates = {}
    for name, input_hash in INPUTS.items():
        base = regular(BASE / name, f"immutable accepted base {name}")
        if digest(base) != input_hash:
            raise AssertionError(f"immutable accepted base drifted: {name}")
        raw = regular(EVIDENCE / name, f"candidate {name}")
        if not raw.startswith(base) or raw[len(base):] != expected[name] or raw.count(expected[name]) != 1:
            raise AssertionError(f"candidate {name} does not conserve its sole bounded suffix")
        candidates[name] = {"path": str(EVIDENCE / name), "bytes": len(raw), "sha256": digest(raw), "input_sha256": input_hash, "suffix_bytes": len(expected[name])}
    readme = (EVIDENCE / "candidate-README.template.md").read_text()
    gates = (EVIDENCE / "candidate-gate-results.md").read_text()
    if readme.count("```") % 2 or gates.count("```") % 2 or len(re.findall(r"^\d+\. ", gates, re.M)) != 32:
        raise AssertionError("candidate fences or 32-ID table changed")
    for token in ("{{UTC}}", "{{REPO_SUMMARY}}", "{{REPO_SECTIONS}}", "{{GATE_RESULTS}}"):
        if readme.count(token) != 1:
            raise AssertionError(f"README placeholder count changed: {token}")
    markers = ("# D141 documented known gaps", "**SWAP.**", "**Element.**", "Idempotency-Key", "D139a installed schema input", "D141ff popup ADD known gap", "D141gg parent move PASS accepted", "FAIL_CUSTODY_NATIVE_TEST_PASS", "D141hh single PASS accepted with both procedural gaps", "CUSTODY-RAW-KEEP", "CUSTODY-RECIPE-PATH", "TEST_KEEP", "original first single no-body attempt from 1135 remains NOTRUN")
    for text, label in ((readme, "README"), (gates, "gate-results")):
        for marker in markers:
            if marker not in text:
                raise AssertionError(f"{label}: marker missing: {marker}")
    return {"status": "PASS_PRIVATE_D141HH_CANDIDATES", "inputs": {n: {"sha256": h, "path": str(BASE / n)} for n, h in INPUTS.items()}, "candidates": candidates, "publications": {"terminal": sources["terminal"], "custody": sources["custody"]}, "board_header_sha256": sources["board_sha256"], "render": render_only(EVIDENCE / "candidate-README.template.md", EVIDENCE / "candidate-gate-results.md"), "conservation": {"full_input_prefix": True, "only_intended_suffix_once_per_document": True, "prior_lineage": True, "32_ids_ledgers_witnesses_limits": True, "balanced_fences_and_placeholders": True, "published_originals_resolved_by_local_basename": True}, "scope": "private documentary candidates only; no canonical write, product merge, build, service, diagnostic, REG0, or ZIP"}


def private_sampler() -> dict[str, object]:
    trace = EVIDENCE / "disk-trace.txt"
    lifecycle = EVIDENCE / "sampler-lifecycle.json"
    code = "import json,shutil,sys,time\nfrom datetime import datetime,timezone\npath,stop,interval,mount=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),sys.argv[4]\nstart=time.monotonic()\nwith open(path,'w',encoding='utf-8') as out:\n    while True:\n        available=shutil.disk_usage(mount).free\n        out.write(json.dumps({'timestamp':datetime.now(timezone.utc).isoformat(),'available_bytes':available,'stop_free_bytes':stop},sort_keys=True)+'\\n'); out.flush()\n        if available<=stop or time.monotonic()-start>=interval: break\n        time.sleep(interval)\n"
    started = datetime.now(timezone.utc).isoformat()
    process = subprocess.Popen([sys.executable, "-c", code, str(trace), "4000000000", "5.0", str(ROOT)])
    waited = False
    try:
        exit_code = process.wait(timeout=12)
        waited = True
    finally:
        if not waited:
            exit_code = process.wait()
            waited = True
    rows = [json.loads(line) for line in regular(trace, "private disk trace").splitlines() if line.strip()]
    if len(rows) < 2 or any(row["available_bytes"] <= row["stop_free_bytes"] for row in rows):
        raise AssertionError("private sampler did not produce a safe durable 5-second trace")
    data = {"schema": "d141hh-private-sampler-v1", "pid": process.pid, "started_at": started, "interval_seconds": 5, "stop_free_bytes": 4000000000, "status": "completed", "worker_first_tool_trace": False, "first_tool_gap": {"status": "FAIL", "reason": "The first-tool trace target could not be created because the pre-existing tmpdir path was a regular file.", "path": str(ROOT / "tmpdir")}, "samples": len(rows), "last_sample_at": rows[-1]["timestamp"], "last_available_bytes": rows[-1]["available_bytes"], "exit_code": exit_code, "waited": waited, "reaped": waited, "gap_disclosure": "This later private sampler is not substituted for first-tool coverage; the first-tool path error is disclosed."}
    lifecycle.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return data


def write() -> dict[str, object]:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    sampler = private_sampler()
    sources = verify_sources()
    readme_suffix, gate_suffix = suffixes(sources)
    for name, suffix in (("candidate-README.template.md", readme_suffix), ("candidate-gate-results.md", gate_suffix)):
        base = regular(BASE / name, f"immutable accepted base {name}")
        if digest(base) != INPUTS[name]:
            raise AssertionError(f"immutable accepted base drifted: {name}")
        (EVIDENCE / name).write_bytes(base + suffix.encode())
    result = verify_candidates(sources)
    result["sampler"] = sampler
    (EVIDENCE / "source-manifest.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (EVIDENCE / "single-note.md").write_text("# D141hh single documentary note\n\nThe private README and gate-results successors append one bounded accepted single PASS paragraph to the immutable D141gg parent-note lineage. The exact tuple, IDs, predicates, trace facts, late raw KEEP, future-output-only relocation, independent custody FAIL, and earlier no-body NOTRUN limit are bound to the two local publication packets. Main D141hh accepts the service PASS with both procedural gaps disclosed; D141hh-a TEST_KEEP applies only to future submits.\n\nThe first tool's requested trace target was a pre-existing regular tmpdir file; the later sampler's PID, exit, wait and reap are recorded separately and no first-tool coverage is claimed. No canonical or product write was made.\n")
    (EVIDENCE / "validation.md").write_text("# D141hh single-note validation\n\nStatus: **PASS_PRIVATE_D141HH_CANDIDATES**.\n\n- Immutable bases matched `90f8bab9...` and `ddebb463...`; both successors conserve the complete byte prefixes and append one bounded D141hh paragraph.\n- Prior popup/parent paragraphs, SWAP/Element, 32 IDs, ledgers, witness, custody limit, C0 examples, placeholders and fences remain intact.\n- Publications `08d6573b...` and `c67e717f...` and every locally resolved declared original matched exact bytes/hashes.\n- The single-scope-2 author PASS is retained as preflight `9320`, normal `24271`, exit 0/257 s, with exact predicates; custody remains FAIL_CUSTODY with late KEEP and path-relocation findings.\n- Original 1135 remains NOTRUN; no retarget/reproof or repaired historical custody claim is made. TEST_KEEP is future-only.\n- Production `render_readme` was exercised function-only with four controlled records and a missing-gate fallback; renderer hash, placeholders and fences passed.\n- The later private sampler recorded a durable 5-second trace above the 4 GB stop with PID, exit, wait and reap; the first-tool regular-file path failure is disclosed and not backfilled.\n\nNo canonical write, installation, product test, service submission, diagnostic, REG0, full suite, browser journey, build, or ZIP was run.\n")
    (EVIDENCE / "handoff.md").write_text("# D141hh single-note handoff\n\nPrepared private README and gate-results successors from the immutable D141gg parent-note bases, each with one bounded accepted single PASS paragraph. The service PASS, two procedural gaps, independent custody FAIL, and earlier NOTRUN remain distinct; Main's accepted disposition and TEST_KEEP future-only scope are preserved.\n\nNo canonical delivery file, installer pin, product source, service state, or merge request was changed.\n")
    return result


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--write":
        result = write()
        print(json.dumps({"status": result["status"], "candidates": result["candidates"]}, sort_keys=True))
        return 0
    if len(sys.argv) != 1:
        raise SystemExit("usage: check_notes.py [--write]")
    sources = verify_sources()
    result = verify_candidates(sources)
    print(json.dumps({"status": result["status"], "candidates": result["candidates"], "render": result["render"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
