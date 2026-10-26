#!/usr/bin/env python3
"""Build and verify the private D141hh P1/P3 return candidates.

The immutable 1249 checker remains the source of the publication, byte,
render, and source-fact checks.  This wrapper retargets those checks to this
worker's private output root and makes the one approved time-scope correction.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path

WORKER = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/rt-F-D141hh-P1-P3-return-1307"
)
EVIDENCE = WORKER / "evidence"
BASE = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/rt-F-D141hh-single-notes-next/evidence"
)
SOURCE_CHECKER = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/rt-F-D141hh-P1-P3-notes-1249/evidence/check_notes.py"
)
DESIGN = Path("/home/user/timeline-hub/hub/design")
DECISION = DESIGN / "owner-decision-20261026T1250Z-D141ii.md"
BOARD = DESIGN / "BOARD-HEADER.md"
INPUTS = {
    "candidate-README.template.md": "715a92af643749be18e92391a7c6793790ceb9dd38301808eee95ca2048e9071",
    "candidate-gate-results.md": "d0016975dc18212d40f3e53359f0606611e28f4f600109bd6be2f66fee45ef5d",
}


def load_source_checker():
    spec = importlib.util.spec_from_file_location("immutable_d141hh_checker", SOURCE_CHECKER)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load immutable checker: {SOURCE_CHECKER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.EVIDENCE = EVIDENCE
    module.BASE = BASE
    module.DESIGN = DESIGN
    module.BOARD = BOARD
    # The legacy renderer test creates only a missing-gates control fixture.
    # Keep that scratch under the harness-owned temporary directory.
    old_mkdtemp = tempfile.mkdtemp

    def safe_mkdtemp(*, prefix="tmp", **_kwargs):
        return old_mkdtemp(prefix=prefix, dir=os.environ.get("TMPDIR", "/tmp"))

    module.tempfile.mkdtemp = safe_mkdtemp
    return module


LEGACY = load_source_checker()
OLD_SUFFIXES = LEGACY.p13_suffixes


def corrected_suffixes(sources):
    readme, gates = OLD_SUFFIXES(sources)
    old = "Agent's 55-test owner decision and the App upstream choice remain pending."
    current = (
        "The Main 12:30 pending statements are historical: at that snapshot, the "
        "Agent 55-test owner decision and the App upstream choice were pending. "
        "D141ii is now recorded: inverse38 is an additive upstream-module restore; "
        "installer2 is exact retirement of the two npm-schema tests; writers15 are "
        "protected migration to the commit path with force still refused; and App "
        "must catch up once to latest upstream (tip 00a014e2a393). Actual repairs, "
        "REG0, App new-head qualification, and the final D141v pin pass remain "
        "required; no build or ZIP claim is made."
    )
    for label, text in (("README", readme), ("gate-results", gates)):
        if text.count(old) != 1:
            raise AssertionError(f"{label}: expected exactly one stale pending sentence")
    return readme.replace(old, current), gates.replace(old, current)


LEGACY.p13_suffixes = corrected_suffixes


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{label}: expected regular non-symlink: {path}")
    if stat.S_IMODE(path.stat().st_mode) != 0o644:
        raise AssertionError(f"{label}: expected mode 0644: {path}")
    return path.read_bytes()


def verify_d141ii() -> dict[str, object]:
    decision = regular(DECISION, "D141ii owner decision").decode()
    board = regular(BOARD, "BOARD-HEADER").decode()
    required_decision = (
        "Inverse, 38 tests", "Put back the upstream module", "Installer, 2 tests",
        "Retire the two tests", "Writers, 15 tests", "Migrate them to the commit path",
        "App's upstream target: the latest upstream",
    )
    if any(marker not in decision for marker in required_decision):
        raise AssertionError("D141ii owner decision markers drifted")
    required_board = (
        "D141ii (12:55Z 26 Oct)", "Inverse 38 — RESTORE", "Installer 2 — RETIRE",
        "Writers 15 — PROTECTED MIGRATION", "App target = latest upstream",
        "D141ii(4) note (12:56Z)", "00a014e2a393", "D141v pin pass",
    )
    if any(marker not in board for marker in required_board):
        raise AssertionError("BOARD-HEADER D141ii markers drifted")
    return {
        "decision_path": str(DECISION),
        "decision_sha256": hashlib.sha256(decision.encode()).hexdigest(),
        "board_path": str(BOARD),
        "board_sha256": hashlib.sha256(board.encode()).hexdigest(),
        "historical_pending_scope": "Main12:30",
        "current_disposition": {
            "inverse38": "additive upstream-module restore",
            "installer2": "exact retirement of the two npm-schema tests",
            "writers15": "protected migration to the commit path with force refused",
            "app": "latest-upstream catch-up, then new-head qualification",
        },
        "outstanding": ["actual repairs", "REG0", "App new-head qualification", "final D141v pin pass", "build"],
    }


def trace_lifecycle() -> dict[str, object]:
    path = EVIDENCE / "disk-trace.txt"
    lines = regular(path, "worker disk trace").decode().splitlines()
    samples = []
    pid = None
    exit_code = None
    waited = False
    reaped = False
    for line in lines:
        match = re.match(r"([^ ]+) available_bytes=(\d+)$", line)
        if match:
            samples.append({"timestamp": match[1], "available_bytes": int(match[2])})
        elif line.startswith("sampler_pid="):
            pid = int(line.split("=", 1)[1])
        elif line.startswith("sampler_exit="):
            exit_code = int(line.split("=", 1)[1])
        elif line == "sampler_waited=true":
            waited = True
        elif line == "sampler_reaped=true":
            reaped = True
    if len(samples) < 2 or pid is None:
        raise AssertionError("worker sampler trace is missing durable samples or PID")
    if min(row["available_bytes"] for row in samples) <= 4000000000:
        raise AssertionError("worker trace crossed the 4 GB stop threshold")
    return {
        "schema": "d141hh-p1-p3-worker-sampler-v2",
        "trace_path": str(path),
        "sampler_pid": pid,
        "interval_seconds": 5,
        "stop_free_bytes": 4000000000,
        "sample_count": len(samples),
        "minimum_available_bytes": min(row["available_bytes"] for row in samples),
        "first_sample_at": samples[0]["timestamp"],
        "last_sample_at": samples[-1]["timestamp"],
        "exit_code": exit_code,
        "waited": waited,
        "reaped": reaped,
        "stop_reached": False,
        "worker_first_tool_trace": False,
        "first_tool_gap": {
            "status": "FAIL",
            "reason": "The initial sampler launch could not create disk-trace.txt because the evidence directory did not yet exist; the later retained sampler is not backfilled as first-tool coverage.",
        },
        "tmpdir_metadata": "regular file pointer; no mkdir performed",
    }


def verify_handoff() -> None:
    handoff = regular(EVIDENCE / "handoff.md", "handoff").decode()
    stale = "Agent55 owner decision and App upstream pending choice remain explicit."
    if stale in handoff or "remain pending" in handoff:
        raise AssertionError("handoff retains unscoped superseded pending wording")
    for marker in ("historical Main12:30", "D141ii is recorded", "inverse38", "installer2", "writers15", "latest-upstream", "D141v", "no build"):
        if marker not in handoff:
            raise AssertionError(f"handoff missing corrected disposition marker: {marker}")


def verify() -> dict[str, object]:
    facts = LEGACY.verify_p13_sources()
    sampler = trace_lifecycle()
    result = LEGACY.verify_p13_candidates(facts, sampler)
    verify_handoff()
    result["d141ii"] = verify_d141ii()
    return result


def write() -> dict[str, object]:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    facts = LEGACY.verify_p13_sources()
    sampler = trace_lifecycle()
    readme_suffix, gate_suffix = corrected_suffixes(facts)
    for name, suffix in (("candidate-README.template.md", readme_suffix), ("candidate-gate-results.md", gate_suffix)):
        base = regular(BASE / name, f"immutable accepted base {name}")
        if hashlib.sha256(base).hexdigest() != INPUTS[name]:
            raise AssertionError(f"immutable accepted base drifted: {name}")
        (EVIDENCE / name).write_bytes(base + suffix.encode())
    d141ii = verify_d141ii()
    result = LEGACY.verify_p13_candidates(facts, sampler)
    result["d141ii"] = d141ii
    (EVIDENCE / "source-manifest.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (EVIDENCE / "sampler-lifecycle.json").write_text(json.dumps(sampler, indent=2, sort_keys=True) + "\n")
    (EVIDENCE / "P1-P3-note.md").write_text(
        "# D141hh P1/P3 documentary note\n\n"
        "Private successors preserve the accepted single-note prefixes and append one bounded P1/P3 actual PASS plus independent custody disclosure. The corrected suffix scopes Main12:30 pending statements historically and records D141ii's inverse38 additive restore, installer2 exact retirement, writers15 protected migration, App latest-upstream catch-up, and the outstanding repair/REG0, new-head qualification, final D141v, and no-build limits.\n"
    )
    (EVIDENCE / "validation.md").write_text(
        "# D141hh P1/P3 notes validation\n\n"
        "Status: **PASS_PRIVATE_D141HH_P1_P3_CANDIDATES**.\n\n"
        "- Immutable 715a92af and d0016975 prefixes, all prior gaps, 32 IDs, originals, ledgers, witnesses, limits, fences and placeholders are conserved; each corrected suffix occurs once.\n"
        "- Four publication schemas and all 32 declared originals match exact bytes and hashes; P1/P3 tuple, IDs, counts, TEST_KEEP ordering, predicates, builder and monitor limitations derive from the originals.\n"
        "- D141ii is checked from the owner decision and BOARD-HEADER; the only new wording change scopes the superseded Main12:30 pending snapshot and states the current disposition and outstanding limits.\n"
        "- Production `render_readme` was exercised function-only with controlled four-repository inputs and missing-gate fallback; renderer SHA is ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca.\n"
        "- The initial sampler launch gap is disclosed and not backfilled; the retained sampler trace remains above 4 GB.\n\n"
        "No product, test, generated, pin, canonical install, service, build, REG0, final D141v, diagnostic or ZIP action was taken.\n"
    )
    (EVIDENCE / "handoff.md").write_text(
        "# D141hh P1/P3 notes handoff\n\n"
        "Prepared private successors from the accepted single-note lineage. The historical Main12:30 pending statements are explicitly scoped as historical; D141ii is recorded with inverse38 additive restore, installer2 exact retirement, writers15 protected migration, and App latest-upstream catch-up. Actual repairs/REG0, App new-head qualification and final D141v remain required; no build or ZIP claim is made. P1/P3 facts, custody limits, TEST_KEEP ordering and monitor gaps remain unchanged.\n\n"
        "No canonical/product/repo state or hub was changed.\n"
    )
    # Publish this worker-local checker with the private evidence so the
    # author and protected return reviewer run the identical program.
    (EVIDENCE / "check_notes.py").write_text(Path(__file__).read_text())
    verify_handoff()
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2 and sys.argv[1] == "--write":
        print(json.dumps(write(), sort_keys=True))
    elif len(sys.argv) == 1:
        print(json.dumps(verify(), sort_keys=True))
    else:
        raise SystemExit("usage: check_notes.py [--write]")
