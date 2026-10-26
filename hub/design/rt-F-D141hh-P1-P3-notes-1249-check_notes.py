#!/usr/bin/env python3
"""Build and verify private D141hh P1/P3 documentary-note successors."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import stat
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141hh-P1-P3-notes-1249")
EVIDENCE = ROOT / "evidence"
BASE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141hh-single-notes-next/evidence")
DESIGN = Path("/home/user/timeline-hub/hub/design")
BOARD = DESIGN / "BOARD-HEADER.md"
RENDERER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-final-unit-notes-input-0849-delivery-build.py")
INPUTS = {"candidate-README.template.md": "715a92af643749be18e92391a7c6793790ceb9dd38301808eee95ca2048e9071", "candidate-gate-results.md": "d0016975dc18212d40f3e53359f0606611e28f4f600109bd6be2f66fee45ef5d"}
PUBLICATION_HASHES = {
    DESIGN / "app-D141hh-p1-terminal-publication-1218.json": "37dc94953e61ecea458864795a124992296ef483c399adb82e6f17df074b278f",
    DESIGN / "app-D141hh-p1-custody-publication-1223.json": "489148bf489d4cc9b2fafe9f70372a961f7dc33aa0aa527805f8241d94eedd1d",
    DESIGN / "app-D141hh-p3-terminal-publication-1232.json": "d010df5ca02ffde7967e731228c831a2af1cba7c75049e7393bf4a8e95142888",
    DESIGN / "app-D141hh-p3-custody-publication-1231.json": "bd26ce90d90f2699f26449479e3db2daf3a236d619c6c5a47b998232b5659483",
}
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
        result = write_p13()
        print(json.dumps({"status": result["status"], "candidates": result["candidates"]}, sort_keys=True))
        return 0
    if len(sys.argv) != 1:
        raise SystemExit("usage: check_notes.py [--write]")
    sources = verify_p13_sources()
    sampler = trace_lifecycle()
    result = verify_p13_candidates(sources, sampler)
    print(json.dumps({"status": result["status"], "candidates": result["candidates"], "render": result["render"], "source_count": result["source_count"]}, sort_keys=True))
    return 0


def verify_p13_sources() -> dict[str, object]:
    specs = {
        "p1_terminal": DESIGN / "app-D141hh-p1-terminal-publication-1218.json",
        "p1_custody": DESIGN / "app-D141hh-p1-custody-publication-1223.json",
        "p3_terminal": DESIGN / "app-D141hh-p3-terminal-publication-1232.json",
        "p3_custody": DESIGN / "app-D141hh-p3-custody-publication-1231.json",
    }
    packets = {name: publication(path) for name, path in specs.items()}
    maps = {name: file_map(packet) for name, packet in packets.items()}
    p1t, p1c = packets["p1_terminal"]["publication"], packets["p1_custody"]["publication"]
    p3t, p3c = packets["p3_terminal"]["publication"], packets["p3_custody"]["publication"]
    if p1t.get("actual_worker_exit") != 0 or not str(p1t.get("normal_result", "")).startswith("32161 PASS0/200s") or p1t.get("preflight") != "31121 PASS":
        raise AssertionError("P1 terminal schema/result drifted")
    if (p1c.get("verdict"), p1c.get("normal")) != ("PASS_CUSTODY_TEST_PASS", "32161 PASS0/200s"):
        raise AssertionError("P1 custody schema/result drifted")
    if p3t.get("actual_worker_exit") != 0 or not str(p3t.get("normal_result", "")).startswith("6447 PASS0/206s") or p3t.get("preflight") != "29473 PASS":
        raise AssertionError("P3 terminal schema/result drifted")
    if p3c.get("verdict") != "PASS_CUSTODY_TEST_PASS":
        raise AssertionError("P3 custody schema/result drifted")

    p1r = read_json(maps["p1_terminal"]["app-P-D141cc-p1-controller-next-results.json"], "P1 results")
    p1source = read_json(maps["p1_terminal"]["app-P-D141cc-p1-controller-next-source-manifest.json"], "P1 source")
    p1custodysource = read_json(maps["p1_custody"]["app-P-D141hh-p1-custody-review-1218-source-manifest.json"], "P1 custody source")
    p1receipt = read_json(maps["p1_terminal"]["app-P-D141cc-p1-controller-next-controller-receipt.json"], "P1 receipt")
    p1progress = read_json(maps["p1_terminal"]["app-P-D141cc-p1-controller-next-progress.json"], "P1 progress")
    p1validation = regular(maps["p1_terminal"]["app-P-D141cc-p1-controller-next-validation.md"], "P1 validation").decode()
    p1review = read_json(maps["p1_custody"]["app-P-D141hh-p1-custody-review-1218-review.json"], "P1 custody")
    p1admission = read_json(DESIGN / "app-D141hh-p1-controller-admission-1210.json", "P1 admission")
    readback = read_json(DESIGN / "app-D141hh-p1-p3-KEEP-source-readback-1209.json", "KEEP readback")
    p1rows = p1r["raw_results"]
    if (p1r["selector"], p1r["attempt_scope"], p1r["verdict"]) != ("p1", "original", "PASS") or len(p1rows) != 2:
        raise AssertionError("P1 result scope/count drifted")
    if any(row["status"] != "pass" or row["exit"] != "0" for row in p1rows):
        raise AssertionError("P1 raw statuses drifted")
    p1pre, p1normal = p1rows[0]["id"], p1rows[1]["id"]
    if p1pre != "app-pin-82e9e13d-full-d141-p1-82e9e13d-submit-preflight-1026121110-31121" or p1normal != "app-pin-82e9e13d-full-d141-p1-82e9e13d-submit-1026121140-32161":
        raise AssertionError("P1 full IDs drifted")
    if p1r["same_id_wait"]["id"] != p1normal or p1r["same_id_wait"]["exit_code"] != 0 or p1r["same_id_wait"]["invocations"] != 1:
        raise AssertionError("P1 same-ID wait drifted")
    if p1r["native_submit"]["invocations"] != 1 or p1r["native_submit"]["exit_code"] != 0:
        raise AssertionError("P1 submit drifted")
    if p1review["verdict"] != "PASS_CUSTODY_TEST_PASS" or p1review["tests"]["p1_cases"] != 2 or p1review["tests"]["readiness"] != 1 or p1review["tests"]["p1_xml"] != {"errors": 0, "failures": 0, "skipped": 0, "tests": 2}:
        raise AssertionError("P1 custody/counts drifted")
    if p1custodysource["request_test"]["keep_order_source_line"] != "KEEP is written before the request is queued" or p1progress["raw_keep_policy"] != "TEST_KEEP=D141hh p1 inherited; native request-test creates KEEP before queue":
        raise AssertionError("P1 TEST_KEEP source fact drifted")
    if len(p1r["service_test_lines"]) < 2:
        raise AssertionError("P1 predicate lines missing")
    if p1admission["TEST_KEEP"] != "D141hh p1" or any(row["keep"]["exists"] is not True for row in p1receipt["custody"]["raw_ids"]):
        raise AssertionError("P1 KEEP marker fact drifted")
    if not all(row["created_before_controller"] is True for row in readback["future_parent_markers"]):
        raise AssertionError("parent KEEP ordering drifted")

    p3r = read_json(maps["p3_terminal"]["app-P-D141cc-p3-controller-next-results.json"], "P3 results")
    p3receipt = read_json(maps["p3_terminal"]["app-P-D141cc-p3-controller-next-controller-receipt.json"], "P3 receipt")
    p3source = read_json(maps["p3_terminal"]["app-P-D141cc-p3-controller-next-source-manifest.json"], "P3 source")
    p3review = read_json(maps["p3_custody"]["app-P-D141hh-p3-custody-review-1226-review.json"], "P3 custody")
    p3reviewsampler = read_json(maps["p3_custody"]["app-P-D141hh-p3-custody-review-1226-sampler-lifecycle.json"], "P3 reviewer sampler")
    p3validation = regular(maps["p3_terminal"]["app-P-D141cc-p3-controller-next-validation.md"], "P3 validation").decode()
    p3admission = read_json(DESIGN / "app-D141hh-p3-controller-admission-1217.json", "P3 admission")
    if p3r["selector"] != "p3" or p3r["native_submit"]["status"] != "pass" or p3r["native_submit"]["exit_code"] != 0:
        raise AssertionError("P3 result scope/status drifted")
    p3pre, p3normal = p3r["preflight"]["id"], p3r["normal"]["id"]
    if p3pre != "app-pin-82e9e13d-full-d141-p3-82e9e13d-submit-preflight-1026121859-29473" or p3normal != "app-pin-82e9e13d-full-d141-p3-82e9e13d-submit-1026121929-6447":
        raise AssertionError("P3 full IDs drifted")
    if p3r["preflight"]["status"] != "pass" or p3r["normal"]["status"] != "pass" or p3r["normal"]["wait_test"]["duration_seconds"] != 206:
        raise AssertionError("P3 wait facts drifted")
    if p3r["normal"]["journey"] != {"gate5_failed": 0, "gate5_passed": 1, "readiness_passed": 1}:
        raise AssertionError("P3 counts drifted")
    if p3r["qualification"]["reg0"] is not False or p3review["trace"]["outside_row_conservation"] != "not_claimed_without_genuine_preimage":
        raise AssertionError("P3 limits drifted")
    if p3review["verdict"] != "PASS_CUSTODY_TEST_PASS" or p3review["body"]["gate5_tests"] != 1 or p3review["body"]["gate5_failures"] != 0 or p3review["body"]["gate5_skipped"] != 0 or p3review["body"]["readiness_tests"] != 1:
        raise AssertionError("P3 custody/body counts drifted")
    if p3review["lifecycle"]["author_initial_observer"] != "parse failure before native spawn; no request or artifact side effect":
        raise AssertionError("P3 observer lifecycle drifted")
    if p3admission["TEST_KEEP"] != "D141hh p3" or p3receipt["procedural_notes"][1] != "Native request-test created both raw KEEP markers before queueing; no fallback marker write was needed.":
        raise AssertionError("P3 TEST_KEEP queue fact drifted")
    if not p3r["preflight"]["keep_content"].startswith("2026-10-26T12:18:59Z KEEP at creation") or not p3r["normal"]["keep_content"].startswith("2026-10-26T12:19:29Z KEEP at creation"):
        raise AssertionError("P3 KEEP creation fact drifted")
    if p3reviewsampler["review"]["first_attempt"]["result"] != "failed_before_sample" or p3reviewsampler["review"]["corrected_attempt"]["sample_count"] != 6:
        raise AssertionError("P3 sampler limitation drifted")
    p3_predicate_line = "The native log reports the lost-ACK/newer-local-gesture/restart/undo journey passed."
    if p3_predicate_line not in p3validation:
        raise AssertionError("P3 predicate line missing")

    tuple_one = {name: (p1source["pins"][name]["head"], p1source["pins"][name]["tree"]) for name in ("app", "agent", "runtime", "composition")}
    tuple_three = {name: (p3source["selected_execution_sources"][name]["head"], p3source["selected_execution_sources"][name]["tree"]) for name in tuple_one}
    if tuple_one != tuple_three or tuple_one["composition"][0] != "635f4de06fda22a85fc2e4cfc764d0153a4c9f40":
        raise AssertionError("P1/P3 tuple drifted")
    builder = {"git_blob": "59b65214bc74c1ca118b097bc3b13c0ffe480a93", "path": "/home/user/work/app/scripts/testing/d66-plain-stack.mjs", "sha256": "2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f"}
    if p1source["builder"] != builder or p3source["builder"].get("path") != builder["path"] or p3source["builder"]["sha256"] != builder["sha256"]:
        raise AssertionError("native builder drifted")
    board = regular(BOARD, "BOARD-HEADER").decode()
    if "GATE (12:30Z): **App journeys on 82e9e13d all terminal.** Placement, parent move, bulk, single, register-asset, P1 and P3 all PASS." not in board or "owner's decision on Agent's 55 tests" not in board:
        raise AssertionError("Main12:30/Agent55 marker missing")
    installed = read_json(DESIGN / "runtime-D141hh-single-notes-installed-publication-1234.json", "installed publication")
    installed_names = {"README.template.md": INPUTS["candidate-README.template.md"], "gate-results.md": INPUTS["candidate-gate-results.md"]}
    if installed.get("status") != "PASS_BOUNDED_CAS" or any(installed["canonical"][name]["sha256"] != sha for name, sha in installed_names.items()):
        raise AssertionError("installed publication drifted")
    p1_duration = int(re.search(r"PASS0/(\d+)s", p1t["normal_result"]).group(1))
    return {"p1": {"results": p1r, "review": p1review, "source": p1source, "preflight_id": p1pre, "normal_id": p1normal, "duration": p1_duration, "custody_source": p1custodysource, "validation": p1validation, "predicates": p1r["service_test_lines"][:2]}, "p3": {"results": p3r, "review": p3review, "source": p3source, "preflight_id": p3pre, "normal_id": p3normal, "duration": p3r["normal"]["wait_test"]["duration_seconds"], "custody_sampler": p3reviewsampler, "validation": p3validation, "predicate": p3_predicate_line}, "publications": packets, "tuple": tuple_one, "board_sha256": digest(board.encode()), "source_count": sum(len(packet["files"]) for packet in packets.values()), "installed": {"status": installed["status"], "sha256": digest((DESIGN / "runtime-D141hh-single-notes-installed-publication-1234.json").read_bytes())}}


def trace_lifecycle() -> dict[str, object]:
    path = EVIDENCE / "disk-trace.txt"
    lines = regular(path, "worker disk trace").decode().splitlines()
    samples, pid, wait_status = [], None, None
    for line in lines:
        match = re.match(r"sample=(\d+) utc=([^ ]+) available_bytes=(\d+)", line)
        if match:
            samples.append({"index": int(match[1]), "timestamp": match[2], "available_bytes": int(match[3])})
        elif line.startswith("sampler_pid="):
            pid = int(line.split("=", 1)[1])
        elif line.startswith("wait_status="):
            wait_status = int(line.split("=", 1)[1])
    if len(samples) != 5 or pid is None or wait_status != 0 or "sampler_reaped=true" not in lines:
        raise AssertionError("worker sampler lifecycle incomplete")
    if min(row["available_bytes"] for row in samples) <= 4000000000:
        raise AssertionError("worker trace crossed stop threshold")
    started = datetime.fromisoformat(next(line.split("=", 1)[1] for line in lines if line.startswith("trace_started_utc=")).replace("Z", "+00:00"))
    finished = datetime.fromisoformat(next(line.split("=", 1)[1] for line in lines if line.startswith("trace_finished_utc=")).replace("Z", "+00:00"))
    return {"schema": "d141hh-p1-p3-worker-sampler-v1", "first_tool": True, "trace_path": str(path), "stop_bytes": 4000000000, "sample_count": len(samples), "minimum_available_bytes": min(row["available_bytes"] for row in samples), "started_at": started.isoformat(), "finished_at": finished.isoformat(), "span_seconds": (finished - started).total_seconds(), "sampler_pid": pid, "exit_code": wait_status, "waited": True, "reaped": True, "stop_reached": False, "tmpdir_metadata": "regular file pointer; no mkdir performed", "duration_disclosure": "The first tool recorded five one-second samples over a four-second wall span; a full five-second span is not claimed."}

def p13_suffixes(sources: dict[str, object]) -> tuple[str, str]:
    p1, p3 = sources["p1"], sources["p3"]
    tuple_text = ", ".join(f"{name.title()} {sources['tuple'][name][0]} / {sources['tuple'][name][1]}" for name in ("app", "agent", "runtime", "composition"))
    p1trace, p3trace = p1["review"]["traces"], p3["review"]["trace"]
    p1tests, p1xml = p1["review"]["tests"]["p1_cases"], p1["review"]["tests"]["p1_xml"]
    p3body = p3["review"]["body"]
    common = (f"The measured four-way tuple is {tuple_text} (head / tree); it is Composition-635f context, not a final pin or installation claim. "
              f"P1 original service: preflight {p1['preflight_id']} PASS; actual {p1['normal_id']} PASS/exit 0 in {p1['duration']} s. It contains both original P1 cases plus readiness: {p1tests} tests, {p1['review']['tests']['readiness']} readiness case, and {p1xml['failures']} failures, {p1xml['skipped']} skips, or {p1xml['errors']} errors. P1 predicates, derived from the original service lines, are: {'; '.join(p1['predicates'])}. "
              f"P1 independent custody is {p1['review']['verdict']}; {p1['custody_source']['request_test']['keep_order_source_line']}, with no body rerun. "
              f"P3 original service: preflight {p3['preflight_id']} PASS; actual {p3['normal_id']} PASS/exit 0 in {p3['duration']} s. The complete original Gate-5 tail and readiness each passed: {p3body['gate5_tests']} Gate-5, {p3body['readiness_tests']} readiness, {p3body['gate5_failures']} failures, {p3body['gate5_skipped']} skips, or {p3body.get('gate5_errors', 0)} errors. The P3 predicate derived from the original validation is: {p3['predicate']} "
              f"P3 independent custody is {p3['review']['verdict']}; native request-test creation-before-queueing is retained by the original markers {p3['results']['preflight']['keep_content'].strip()} and {p3['results']['normal']['keep_content'].strip()}, with no body rerun. "
              f"P1 monitor coverage is bounded to native preflight {p1trace['native_preflight']['samples']} samples, native normal {p1trace['native_normal']['samples']} samples, and author {p1trace['author_sampler']['samples']} samples; the independent reviewer disclosed an initial parse error and corrected short sampler. "
              f"P3 retained {p3trace['native_5s_trace']['samples']} native samples and {p3trace['author_trace']['samples']} author five-second samples; the author observer parse failure was before native spawn, and the independent reviewer disclosed a path typo before a corrected {p3['custody_sampler']['review']['corrected_attempt']['sample_count']}-sample trace. Neither native trace reached the 4 GB stop. Outside-row conservation is not claimed without a genuine preimage. "
              "Main's 12:30 recorded disposition is all seven App journeys PASS; this suffix adds only bounded P1/P3 measurements, makes no new cumulative App verdict, and does not requalify another selector. Agent's 55-test owner decision and the App upstream choice remain pending. No REG0, final pin, upstream basis, build activation, or ZIP claim is made.")
    readme = "\n\n## D141hh P1/P3 actual PASS and independent custody disclosure (bounded documentary suffix)\n\nMain's 12:30 recorded disposition is consumed as a disposition only. " + common + "\n"
    gates = "\n\n## D141hh P1/P3 actual PASS and independent custody disclosure (bounded documentary suffix)\n\nThis bounded current-measurement suffix preserves the historical PENDING table and every earlier paragraph. " + common + " The P3 complete Gate-5 tail remains bounded to the original validation and results; the P3 observer parse failure and independent sampler typo/corrected short trace remain disclosed, not repaired or backfilled.\n"
    return readme, gates

def verify_p13_candidates(sources: dict[str, object], sampler: dict[str, object]) -> dict[str, object]:
    readme_suffix, gate_suffix = p13_suffixes(sources)
    expected = {"candidate-README.template.md": readme_suffix.encode(), "candidate-gate-results.md": gate_suffix.encode()}
    candidates = {}
    for name, input_hash in INPUTS.items():
        base = regular(BASE / name, f"immutable base {name}")
        if digest(base) != input_hash:
            raise AssertionError(f"immutable base drifted: {name}")
        raw = regular(EVIDENCE / name, f"candidate {name}")
        if not raw.startswith(base) or raw[len(base):] != expected[name] or raw.count(expected[name]) != 1:
            raise AssertionError(f"candidate {name}: exact prefix/suffix conservation failed")
        candidates[name] = {"path": str(EVIDENCE / name), "bytes": len(raw), "sha256": digest(raw), "input_sha256": input_hash, "prefix_bytes": len(base), "suffix_bytes": len(expected[name]), "suffix_occurrences": raw.count(expected[name])}
    readme = regular(EVIDENCE / "candidate-README.template.md", "candidate README").decode()
    gates = regular(EVIDENCE / "candidate-gate-results.md", "candidate gate-results").decode()
    if readme.count(chr(96) * 3) % 2 or gates.count(chr(96) * 3) % 2 or len(re.findall(r"^\d+\. ", gates, re.M)) != 32:
        raise AssertionError("fences or complete 32-ID table changed")
    for token in ("{{UTC}}", "{{REPO_SUMMARY}}", "{{REPO_SECTIONS}}", "{{GATE_RESULTS}}"):
        if readme.count(token) != 1:
            raise AssertionError(f"placeholder count changed: {token}")
    markers = ("# D141 documented known gaps", "**SWAP.**", "**Element.**", "D141ff popup ADD known gap", "D141gg parent move PASS accepted", "D141hh single PASS accepted with both procedural gaps", "D141hh P1/P3 actual PASS and independent custody disclosure", "FAIL_CUSTODY_NATIVE_TEST_PASS", "CUSTODY-RAW-KEEP", "CUSTODY-RECIPE-PATH", "TEST_KEEP", "Idempotency-Key")
    for text, label in ((readme, "README"), (gates, "gate-results")):
        for marker in markers:
            if marker not in text:
                raise AssertionError(f"{label}: missing conserved marker: {marker}")
    render = render_only(EVIDENCE / "candidate-README.template.md", EVIDENCE / "candidate-gate-results.md")
    return {"status": "PASS_PRIVATE_D141HH_P1_P3_CANDIDATES", "candidates": candidates, "inputs": {n: {"sha256": h, "path": str(BASE / n)} for n, h in INPUTS.items()}, "publications": sources["publications"], "tuple": sources["tuple"], "source_count": sources["source_count"], "board_header_sha256": sources["board_sha256"], "installed_publication": sources["installed"], "render": render, "sampler": sampler, "conservation": {"exact_immutable_prefix": True, "bounded_suffix_once_per_document": True, "all32_originals_resolved_and_hashed": True, "complete32_ids": True, "historical_prefix_unchanged": True, "outside_row_conservation_claim": False}, "scope": "private documentary candidates only; no canonical write, product merge, final build, service submission, diagnostic, REG0, final pin, or ZIP"}


def write_p13() -> dict[str, object]:
    facts = verify_p13_sources()
    sampler = trace_lifecycle()
    readme_suffix, gate_suffix = p13_suffixes(facts)
    for name, suffix in (("candidate-README.template.md", readme_suffix), ("candidate-gate-results.md", gate_suffix)):
        base = regular(BASE / name, f"immutable base {name}")
        if digest(base) != INPUTS[name]:
            raise AssertionError(f"immutable base drifted: {name}")
        (EVIDENCE / name).write_bytes(base + suffix.encode())
    result = verify_p13_candidates(facts, sampler)
    (EVIDENCE / "source-manifest.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (EVIDENCE / "sampler-lifecycle.json").write_text(json.dumps(sampler, indent=2, sort_keys=True) + "\n")
    (EVIDENCE / "P1-P3-note.md").write_text("# D141hh P1/P3 documentary note\n\nThe private successors preserve the accepted installed single-note prefixes and append one bounded current P1/P3 actual PASS plus independent custody disclosure each. The checker reads the four publication schemas, resolves all 32 originals, derives IDs, tuple, counts, predicates and monitor limitations, and exercises delivery-build.render_readme function-only.\n")
    (EVIDENCE / "validation.md").write_text("# D141hh P1/P3 notes validation\n\nStatus: PASS_PRIVATE_D141HH_P1_P3_CANDIDATES.\n\n- Immutable bases matched 715a92af and d0016975; exact prefixes and one bounded suffix per document pass.\n- Four publication schemas and all 32 declared originals match exact bytes and hashes; JSON originals parse.\n- P1 and P3 actual PASS and independent PASS_CUSTODY_TEST_PASS facts, full IDs, counts, tuple, TEST_KEEP ordering, native builder and monitor limitations are derived from originals.\n- P3 observer/sampler limits and no-preimage outside-row limit remain explicit. Fences, placeholders, 32 IDs, historical limits and function-only render controls pass.\n- The first-tool trace records PID, exit, wait and reap, stays above 4 GB, and discloses five samples over a four-second wall span; no full five-second coverage is claimed.\n\nNo product, test, generated, pin, canonical install, service, build, REG0 or ZIP action was taken.\n")
    (EVIDENCE / "handoff.md").write_text("# D141hh P1/P3 notes handoff\n\nPrepared private successors from the accepted installed single-note lineage. Each adds one bounded P1/P3 actual PASS plus independent PASS_CUSTODY_TEST_PASS disclosure and preserves all historical text. The exact tuple, IDs, predicates, counts, TEST_KEEP ordering and monitor limits are source-derived. Main12:30, Agent55 owner decision and App upstream pending choice remain explicit.\n\nNo canonical/product/repo state or hub was changed.\n")
    return result


if __name__ == "__main__":
    raise SystemExit(main())


