#!/usr/bin/env python3
"""Build and verify the private D141gg parent-move documentary candidates.

The default invocation is read-only.  ``--write`` is the only mode that
creates this worker's candidate and receipt files.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import stat
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path


EVIDENCE = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141gg-parent-notes-1148/evidence"
)
IMMUTABLE_BASE = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/rt-F-D141ff-popup-notes-1133/evidence"
)
HUB_DESIGN = Path("/home/user/timeline-hub/hub/design")
BOARD_HEADER = HUB_DESIGN / "BOARD-HEADER.md"
TERMINAL_PUBLICATION = HUB_DESIGN / "app-D141cc-parent-terminal-publication-1130.json"
CUSTODY_PUBLICATION = HUB_DESIGN / "app-D141cc-parent-custody-publication-1135.json"
RENDER_SOURCE = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/design/runtime-final-unit-notes-input-0849-delivery-build.py"
)

EXPECTED_INPUTS = {
    "candidate-README.template.md":
        "599d0e3f2d82b8cef50238966ce45f37d766f6e3e6d907ecd8502bc9c1b0205a",
    "candidate-gate-results.md":
        "6175f480aebc8daf5e48f8db510c40137317ba11a937f04d0caffdd8e2cfd4ec",
}
EXPECTED_PUBLICATIONS = {
    TERMINAL_PUBLICATION: "0825fdad333871a350e65b87fa4b0342d1c3028515e8fe3483a31de548f4c0bb",
    CUSTODY_PUBLICATION: "1b8ac7717542e52a1527a8f42431ea44707b1931a815221fa99db77fca39868b",
}
EXPECTED_RENDER_SHA = "ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca"

README_SUFFIX = """

## D141gg parent move PASS accepted with first-tool trace gap (bounded documentary note)

Author result: the original qualified parent-move attempt used the exact four-repository tuple App `82e9e13ddf1d7ec6c736521b2eb091dca9877598` (tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`), Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92` (tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`), Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` (tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`), and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` (tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`). The paired preflight `app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-preflight-1026112242-25487` was PASS, exit 0. The original normal service result `app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-1026112312-16601` was PASS, exit 0 in 237 s.

The author result records D28 mounted readiness PASS and the original `P2 mounted single parent move: v2 commit, exact field delta, reload and guarded Undo` predicate PASS. The service body is therefore a bounded parent-move PASS: one readiness check and one parent-move journey passed. Native submit session `59630` exited 0 and was reaped; the same normal result was waited through session `51172`, which exited 0 and was reaped. The author's 72-sample trace genuinely covers the service body, but not the worker's first-tool window.

Independent custody result: publication `app-D141cc-parent-custody-publication-1135.json` remains `FAIL_CUSTODY_NATIVE_TEST_PASS`, with review verdict `FAIL_CUSTODY` and finding F-001. The first sampler command failed because `mkdir .../tmpdir` found a regular file, so no trace was written by that first tool. The later 72 samples are genuine and cover the whole body, but the first-tool window before the sampler started is uncovered and cannot be backfilled. This is not custodyPASS and is not a whole-worker trace; no retry or reproof is claimed.

Main disposition: BOARD-HEADER D141gg at 11:35 accepts the parent-move PASS with this trace gap disclosed and calls for no re-proof. That disposition keeps the author service result, the independent custody failure, and the disclosed first-tool limit distinct. It makes no final-build, REG0, ZIP, or other selector claim.
"""

GATE_SUFFIX = """

## D141gg parent move PASS accepted with first-tool trace gap (bounded documentary note)

Author result: on App `82e9e13ddf1d7ec6c736521b2eb091dca9877598` / `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`, Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92` / `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`, Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` / `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`, preflight `app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-preflight-1026112242-25487` passed exit 0 and normal `app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-1026112312-16601` passed exit 0 in 237 s. Mounted readiness and the original parent-move predicate passed; the 72 author samples cover the service body.

Independent custody remains `FAIL_CUSTODY_NATIVE_TEST_PASS`: the first sampler command failed before writing a trace because `tmpdir` was a regular file. The later 72 samples are genuine but cannot backfill the uncovered first-tool window, so no custodyPASS or whole-worker trace is claimed. Main D141gg accepts the service PASS with this gap disclosed and requires no re-proof; the original custody failure is unchanged.
"""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{label}: expected regular non-symlink: {path}")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode != 0o644:
        raise AssertionError(f"{label}: expected mode 0644, got {mode:04o}: {path}")
    return path.read_bytes()


def json_file(path: Path, label: str) -> object:
    try:
        return json.loads(regular(path, label))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{label}: invalid JSON: {path}") from exc


def publication_sources(path: Path, expected_sha: str) -> dict[str, object]:
    raw = regular(path, f"publication {path.name}")
    if sha256(raw) != expected_sha:
        raise AssertionError(f"publication drift at {path}: {sha256(raw)} != {expected_sha}")
    publication = json.loads(raw)
    if not isinstance(publication, dict) or not isinstance(publication.get("files"), list):
        raise AssertionError(f"{path}: missing files list")
    originals = []
    for index, item in enumerate(publication["files"], 1):
        if not isinstance(item, dict) or not all(key in item for key in ("published", "bytes", "sha256")):
            raise AssertionError(f"{path}: malformed file binding {index}")
        original = Path(item["published"])
        original_raw = regular(original, f"published original {index}")
        actual_sha = sha256(original_raw)
        if len(original_raw) != item["bytes"] or actual_sha != item["sha256"]:
            raise AssertionError(
                f"published original {index}: declared bytes/hash do not match {original}"
            )
        originals.append({
            "index": index,
            "path": str(original),
            "bytes": len(original_raw),
            "sha256": actual_sha,
            "mode": "0644",
            "regular_non_symlink": True,
        })
    return {
        "path": str(path),
        "bytes": len(raw),
        "sha256": sha256(raw),
        "status": publication.get("status"),
        "files": originals,
    }


def verify_parent_publications() -> dict[str, object]:
    terminal = publication_sources(
        TERMINAL_PUBLICATION, EXPECTED_PUBLICATIONS[TERMINAL_PUBLICATION]
    )
    custody = publication_sources(
        CUSTODY_PUBLICATION, EXPECTED_PUBLICATIONS[CUSTODY_PUBLICATION]
    )
    terminal_review = json_file(
        Path(terminal["files"][0]["path"]), "terminal controller receipt"
    )
    terminal_results = json_file(
        Path(terminal["files"][1]["path"]), "terminal results"
    )
    custody_review = json_file(
        Path(custody["files"][0]["path"]), "custody review"
    )
    if terminal["status"] != "SERVICE_PASS_PENDING_CUSTODY":
        raise AssertionError(f"unexpected terminal publication status: {terminal['status']}")
    if custody["status"] != "FAIL_CUSTODY_NATIVE_TEST_PASS":
        raise AssertionError(f"unexpected custody publication status: {custody['status']}")
    if terminal_results["normal"]["id"] != "app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-1026112312-16601":
        raise AssertionError("normal service ID drifted")
    if terminal_results["normal"]["status"] != "pass" or terminal_results["normal"]["exit"] != "0":
        raise AssertionError("normal service result is not PASS/exit 0")
    if terminal_results["normal"]["duration_seconds"] != 237:
        raise AssertionError("normal duration drifted from 237 seconds")
    if terminal_results["preflight"]["id"] != "app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-preflight-1026112242-25487":
        raise AssertionError("preflight service ID drifted")
    if terminal_results["preflight"]["status"] != "pass" or terminal_results["preflight"]["exit"] != "0":
        raise AssertionError("preflight is not PASS/exit 0")
    checks = terminal_results["checks"]
    if [check["status"] for check in checks] != ["pass", "pass", "pass"]:
        raise AssertionError("mounted readiness or parent predicate is not PASS")
    if custody_review["verdict"] != "FAIL_CUSTODY":
        raise AssertionError("independent custody verdict changed")
    if custody_review["custody"]["first_tool_sampler"] != "FAIL":
        raise AssertionError("first-tool custody failure is not retained")
    if custody_review["custody"]["later_sampler"] != "PASS_AS_LATER_TRACE_ONLY":
        raise AssertionError("later trace disposition changed")
    return {"terminal": terminal, "custody": custody}


def controlled_results() -> list[dict[str, object]]:
    return [
        {
            "name": name,
            "tip": f"{index:040x}",
            "base": f"{index + 4:040x}",
            "shortstat": "",
            "split": {"product": [0, 0, 0], "tests": [0, 0, 0]},
            "ranged": True,
            "ahead": 0,
            "applied": 0,
            "status": "PASS",
            "seconds": 0.0,
            "applied_tree": f"{index + 8:040x}",
            "bundle_tree": f"{index + 12:040x}",
            "want_tree": f"{index + 16:040x}",
            "problems": [],
        }
        for index, name in enumerate(("agent", "runtime", "app", "composition"), 1)
    ]


def render_function_only(template: Path, gates: Path) -> dict[str, object]:
    source = regular(RENDER_SOURCE, "delivery-build render source")
    if sha256(source) != EXPECTED_RENDER_SHA:
        raise AssertionError("delivery-build render source hash drifted")
    spec = importlib.util.spec_from_file_location("d141gg_delivery_build", RENDER_SOURCE)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load render source: {RENDER_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rendered = module.render_readme(controlled_results(), str(template), str(gates))
    for token in ("{{UTC}}", "{{REPO_SUMMARY}}", "{{REPO_SECTIONS}}", "{{GATE_RESULTS}}"):
        if token in rendered:
            raise AssertionError(f"controlled render left placeholder {token}")
    if rendered.count("```") % 2:
        raise AssertionError("controlled render has unbalanced fences")
    if rendered.count("D141gg parent move PASS accepted") != 2:
        raise AssertionError("controlled render did not retain one D141gg note per document")
    fallback = EVIDENCE / "missing-gate-results-for-fallback.md"
    fallback_rendered = module.render_readme(controlled_results(), str(template), str(fallback))
    if "_Not recorded yet. Paste the gate results here before handing over" not in fallback_rendered:
        raise AssertionError("render fallback did not retain missing-gate notice")
    return {
        "function_only": True,
        "function": "render_readme",
        "caller": str(RENDER_SOURCE),
        "caller_sha256": sha256(source),
        "controlled_inputs": ["agent", "runtime", "app", "composition"],
        "placeholders_resolved": True,
        "balanced_fences": True,
        "disclosure_occurrences": rendered.count("D141gg parent move PASS accepted"),
        "fallback_placeholder_behavior": True,
        "rendered_sha256": sha256(rendered.encode()),
        "fallback_sha256": sha256(fallback_rendered.encode()),
    }


def verify_candidates(parent_sources: dict[str, object]) -> dict[str, object]:
    expected_suffixes = {
        "candidate-README.template.md": README_SUFFIX.encode(),
        "candidate-gate-results.md": GATE_SUFFIX.encode(),
    }
    candidates = {}
    for name, expected_input_sha in EXPECTED_INPUTS.items():
        source = IMMUTABLE_BASE / name
        source_raw = regular(source, f"immutable accepted base {name}")
        if sha256(source_raw) != expected_input_sha:
            raise AssertionError(f"immutable accepted base drifted: {source}")
        candidate = EVIDENCE / name
        raw = regular(candidate, f"candidate {name}")
        suffix = expected_suffixes[name]
        if not raw.startswith(source_raw):
            raise AssertionError(f"candidate {name} does not conserve its full input prefix")
        if raw[len(source_raw):] != suffix:
            raise AssertionError(f"candidate {name} has bytes outside its sole bounded suffix")
        if raw.count(suffix) != 1:
            raise AssertionError(f"candidate {name} suffix is not present exactly once")
        candidates[name] = {
            "path": str(candidate),
            "bytes": len(raw),
            "sha256": sha256(raw),
            "input_sha256": expected_input_sha,
            "suffix_bytes": len(suffix),
        }

    readme = (EVIDENCE / "candidate-README.template.md").read_text()
    gates = (EVIDENCE / "candidate-gate-results.md").read_text()
    if readme.count("```") % 2 or gates.count("```") % 2:
        raise AssertionError("candidate fenced blocks are unbalanced")
    for token in ("{{UTC}}", "{{REPO_SUMMARY}}", "{{REPO_SECTIONS}}", "{{GATE_RESULTS}}"):
        if readme.count(token) != 1:
            raise AssertionError(f"README placeholder {token!r} count is not one")
    if len(re.findall(r"^\d+\. ", gates, flags=re.MULTILINE)) != 32:
        raise AssertionError("complete conserved 32-ID table is not present")
    for text, label in ((readme, "README"), (gates, "gate-results")):
        for marker in (
            "# D141 documented known gaps",
            "**SWAP.**",
            "**Element.**",
            "Idempotency-Key",
            "D139a installed schema input",
            "D141ff popup ADD known gap",
            "D141gg parent move PASS accepted",
            "FAIL_CUSTODY_NATIVE_TEST_PASS",
            "app-pin-82e9e13d-full-d141-p2-parent-move-82e9e13d-submit-1026112312-16601",
        ):
            if marker not in text:
                raise AssertionError(f"{label}: conserved or new marker missing: {marker}")
    render = render_function_only(
        EVIDENCE / "candidate-README.template.md",
        EVIDENCE / "candidate-gate-results.md",
    )
    return {
        "status": "PASS_PRIVATE_D141GG_CANDIDATES",
        "inputs": {
            name: {"sha256": digest, "path": str(IMMUTABLE_BASE / name)}
            for name, digest in EXPECTED_INPUTS.items()
        },
        "candidates": candidates,
        "parent_sources": parent_sources,
        "render": render,
        "conservation": {
            "full_input_prefix": True,
            "only_intended_suffix_once_per_document": True,
            "previous_popup_and_historical_paragraphs": True,
            "32_ids_ledgers_witnesses_limits": True,
            "balanced_fences_and_placeholders": True,
        },
        "scope": "private documentary candidates only; no canonical write, product merge, build, service, diagnostic, REG0, or ZIP",
    }


def run_private_sampler() -> dict[str, object]:
    trace = EVIDENCE / "disk-trace.txt"
    lifecycle = EVIDENCE / "sampler-lifecycle.json"
    sampler_code = textwrap.dedent(
        """
        import json, shutil, sys, time
        from datetime import datetime, timezone
        path, stop, interval = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
        started = time.monotonic()
        with open(path, "w", encoding="utf-8") as out:
            while True:
                available = shutil.disk_usage("/home/user/work/wt/rt-F-D141gg-parent-notes-1148").free
                row = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "available_bytes": available,
                    "stop_free_bytes": stop,
                }
                out.write(json.dumps(row, sort_keys=True) + "\\n")
                out.flush()
                if available <= stop or time.monotonic() - started >= interval:
                    break
                time.sleep(interval)
        """
    )
    command = [sys.executable, "-c", sampler_code, str(trace), "4000000000", "5.0"]
    started_at = datetime.now(timezone.utc).isoformat()
    process = subprocess.Popen(command)
    process_id = process.pid
    waited = False
    return_code = None
    try:
        return_code = process.wait(timeout=12)
        waited = True
    finally:
        if not waited:
            return_code = process.wait()
            waited = True
    trace_raw = regular(trace, "worker-local disk trace")
    rows = [json.loads(line) for line in trace_raw.splitlines() if line.strip()]
    if len(rows) < 2:
        raise AssertionError("worker-local sampler did not produce a durable 5-second trace")
    if any(row["available_bytes"] <= row["stop_free_bytes"] for row in rows):
        raise AssertionError("worker-local sampler crossed the 4 GB stop threshold")
    lifecycle_data = {
        "schema": "d141gg-private-sampler-v1",
        "pid": process_id,
        "started_at": started_at,
        "interval_seconds": 5,
        "stop_free_bytes": 4000000000,
        "status": "completed",
        "worker_first_tool": False,
        "first_action_of_write_mode": True,
        "samples": len(rows),
        "last_sample_at": rows[-1]["timestamp"],
        "last_available_bytes": rows[-1]["available_bytes"],
        "exit_code": return_code,
        "waited": waited,
        "reaped": waited,
        "gap_disclosure": "This private sampler began with --write after worker inspection; parent acceptance relies on the published D141cc evidence and retains its first-tool custody gap.",
    }
    lifecycle.write_text(json.dumps(lifecycle_data, indent=2, sort_keys=True) + "\n")
    return lifecycle_data


def write_candidates() -> dict[str, object]:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    sampler = run_private_sampler()
    parent_sources = verify_parent_publications()
    for name, suffix in (
        ("candidate-README.template.md", README_SUFFIX),
        ("candidate-gate-results.md", GATE_SUFFIX),
    ):
        source = IMMUTABLE_BASE / name
        source_raw = regular(source, f"immutable accepted base {name}")
        if sha256(source_raw) != EXPECTED_INPUTS[name]:
            raise AssertionError(f"immutable accepted base drifted: {source}")
        (EVIDENCE / name).write_bytes(source_raw + suffix.encode())
    result = verify_candidates(parent_sources)
    result["sampler"] = sampler
    (EVIDENCE / "source-manifest.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    (EVIDENCE / "parent-note.md").write_text(
        "# D141gg parent-move documentary note\n\n"
        "The private delivery candidates append one bounded D141gg note to the accepted D141ff README and gate-results bases.\n\n"
        "Author result: the exact four-repository tuple produced preflight `...-25487` PASS and normal `...-16601` PASS, exit 0 in 237 s, with mounted readiness and the original parent-move predicate PASS.\n\n"
        "Independent custody remains `FAIL_CUSTODY_NATIVE_TEST_PASS`: the first sampler command failed before writing a trace because `tmpdir` was a regular file. Later 72 samples genuinely cover the service body, but cannot backfill the uncovered first-tool window. This is not custodyPASS or a whole-worker trace.\n\n"
        "Main D141gg accepts the service PASS with the gap disclosed and no re-proof. The author result, custody failure, and Main disposition remain distinct; no canonical or product write was made.\n"
    )
    (EVIDENCE / "validation.md").write_text(
        "# D141gg parent-note validation\n\n"
        "Status: **PASS_PRIVATE_D141GG_CANDIDATES**.\n\n"
        "- The accepted D141ff README and gate-results inputs matched their declared immutable SHA-256 values.\n"
        "- Both successors conserve their complete input byte prefix and append only the bounded D141gg suffix once.\n"
        "- The prior popup note, historical paragraphs, 32 IDs, ledgers, witnesses, limits, final pins, build gates, placeholders, and fenced blocks remain intact.\n"
        "- Both D141cc parent publications matched their declared SHA-256 values; every published original matched its declared bytes and SHA-256 binding.\n"
        "- The author service result remains the exact four-repository tuple: preflight `...-25487` PASS/exit 0 and normal `...-16601` PASS/exit 0/237 s, with mounted readiness and the original parent-move predicate PASS.\n"
        "- Independent custody remains `FAIL_CUSTODY_NATIVE_TEST_PASS`; the first sampler command failed, while later 72 samples genuinely cover the body but not the first-tool window. Main accepts PASS with this gap disclosed and no re-proof.\n"
        "- The production `render_readme` function was exercised only with four controlled repository records and a missing-gate fallback; placeholders resolved and fences remained balanced.\n"
        "- A private sampler recorded a durable 5-second available-byte trace, stayed above the 4,000,000,000-byte stop, and recorded its own PID, exit, wait, and reap state. Its later start is disclosed and is not substituted for the published custody evidence.\n\n"
        "No canonical write, installation, product test, service submission, diagnostic, REG0, full suite, browser journey, build, or ZIP was run.\n"
    )
    (EVIDENCE / "handoff.md").write_text(
        "# D141gg parent-note handoff\n\n"
        "Prepared private README and gate-results successor candidates from the accepted D141ff immutable bases. The single bounded suffix records the parent-move service PASS and the first-tool trace gap.\n\n"
        "The exact tuple, preflight `...-25487`, normal `...-16601`, native exit 0/237 s, mounted readiness, and original parent predicate are retained. Independent custody remains `FAIL_CUSTODY_NATIVE_TEST_PASS`; no custodyPASS or whole-worker trace is claimed. Main D141gg accepts PASS with the gap disclosed and no re-proof.\n\n"
        "No canonical delivery files, installer pins, product source, service state, or merge request were changed.\n"
    )
    return result


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--write":
        result = write_candidates()
        print(json.dumps({"status": result["status"], "candidates": result["candidates"]}, sort_keys=True))
        return 0
    if sys.argv:
        if len(sys.argv) != 1:
            raise SystemExit("usage: check_notes.py [--write]")
    parent_sources = verify_parent_publications()
    result = verify_candidates(parent_sources)
    print(json.dumps({"status": result["status"], "candidates": result["candidates"], "render": result["render"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

