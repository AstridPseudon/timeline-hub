#!/usr/bin/env python3
"""Create and verify the private D141jj documentary successors."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

WORKER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-notes-1345")
EVIDENCE = WORKER / "evidence"
BASE = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141hh-P1-P3-return-1307/evidence")
SOURCE = BASE / "check_notes.py"
BOARD = Path("/home/user/timeline-hub/hub/design/BOARD-HEADER.md")
INBOX = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/runtime/INBOX.md")
INPUTS = {
    "candidate-README.template.md": "3c32a426cd21947dfe8a29cec38d9830831b8bbdcd533e3884b7ab762c90ddd4",
    "candidate-gate-results.md": "c610ccb16859599dde480ea3ffde40803ca4347b10914d501b762ec1af8c81eb",
}
APP_UPSTREAM = "fc24f84994dc36cfae9349112782ab4d91dbc73b"
APP_TREE = "faf477adef3ec24c9cc359486ac16866500ab219"
APP_PROVEN = "82e9e13ddf1d7ec6c736521b2eb091dca9877598"
APP_PROVEN_TREE = "6a6e49eb4461b5ca1a7fa1247653bc794f26d710"
CATCHUP = "eac97ea5"
CATCHUP_BASE = "00a014e2a393"


def load_source():
    spec = importlib.util.spec_from_file_location("d141hh_source", SOURCE)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load immutable source checker: {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.EVIDENCE = EVIDENCE
    module.BASE = BASE
    module.LEGACY.EVIDENCE = EVIDENCE
    module.LEGACY.BASE = BASE
    old_mkdtemp = tempfile.mkdtemp

    def safe_mkdtemp(*, prefix="tmp", **_kwargs):
        return old_mkdtemp(prefix=prefix, dir=os.environ.get("TMPDIR", "/tmp"))

    module.tempfile.mkdtemp = safe_mkdtemp
    module.LEGACY.tempfile.mkdtemp = safe_mkdtemp
    return module


SOURCE_WRAPPER = load_source()
SOURCE_CHECKER = SOURCE_WRAPPER.LEGACY


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file() or stat.S_IMODE(path.stat().st_mode) != 0o644:
        raise AssertionError(f"{label}: expected regular mode-0644 file: {path}")
    return path.read_bytes()


def owner_facts() -> dict[str, object]:
    board = regular(BOARD, "BOARD-HEADER").decode()
    inbox = regular(INBOX, "Runtime INBOX").decode()
    for marker in ("D141jj (13:42Z 26 Oct)", "option B", "fc24f849", "REMOVAL of the Elements panel", "AgentChat.test.tsx", "00a014e2a393"):
        if marker not in board:
            raise AssertionError(f"BOARD-HEADER D141jj marker missing: {marker}")
    for marker in ("2026-10-26T13:42:13Z — OWNER DECISION D141jj", "option B", "upstream **fc24f849", "82e9e13d", "eac97ea5", "00a014e2", "Elements panel removal, AgentChat test, the Runtime pin", "F-final's apply check runs against", "App's D141v pin pass uses"):
        if marker not in inbox:
            raise AssertionError(f"Runtime INBOX D141jj marker missing: {marker}")
    return {
        "decision": "option B",
        "board_path": str(BOARD), "board_sha256": sha(BOARD),
        "inbox_path": str(INBOX), "inbox_sha256": sha(INBOX),
        "app_upstream": {"head": APP_UPSTREAM, "tree": APP_TREE},
        "app_proven": {"head": APP_PROVEN, "tree": APP_PROVEN_TREE},
        "catchup": {"head": CATCHUP, "onto": CATCHUP_BASE, "merged_into_zip": False},
        "later_conflicts": ["Elements panel removal", "AgentChat test", "Runtime pin"],
        "f_final_app_base": APP_UPSTREAM,
        "f_final_other_repositories": "actual current tips",
        "d141v_app_base": APP_PROVEN,
        "d141v_gate": "after Agent definitive REG0",
        "claims_excluded": ["final head", "current pin", "build", "ZIP"],
        "shot_layering": "catch-up retained uninstalled as first step after ZIP",
    }


def suffixes(_sources: dict[str, object]) -> tuple[str, str]:
    text = (
        "The owner’s 13:42Z D141jj decision is option B. App ships against "
        f"upstream App `{APP_UPSTREAM}` (tree `{APP_TREE}`) with the fully proven "
        f"App `{APP_PROVEN}` (tree `{APP_PROVEN_TREE}`). Existing 82e9e13d "
        "measured receipts remain bound to that actual tuple and are not retargeted "
        "to prospective metadata. The catch-up candidate "
        f"`{CATCHUP}` onto `{CATCHUP_BASE}` is not merged in the ZIP; it remains "
        "uninstalled and is the first shot-layering step after the ZIP lands. The "
        "later upstream conflicts are named exactly: Elements panel removal, "
        "AgentChat test, Runtime pin. F-final’s App apply check uses "
        f"`{APP_UPSTREAM}`; its other three repositories use their actual current "
        "tips. App’s D141v pin pass uses the fully proven "
        f"`{APP_PROVEN}` base after Agent definitive REG0. This suffix makes no "
        "final-head, current-pin, build, or ZIP claim. Older upstream-choice-pending "
        "wording in the prefix is historical; this suffix controls D141jj and leaves "
        "the remaining Agent, proof, and pin gates. No new App full-pair or journey "
        "rerun requirement is invented: the owner selected the retained fully proved "
        "82e9e13d."
    )
    suffix = "\n\n## D141jj App upstream-base decision (bounded documentary note)\n\n" + text + "\n"
    return suffix, suffix


def start_sampler() -> dict[str, object]:
    trace = EVIDENCE / "disk-trace.txt"
    code = ("import shutil,sys,time\nfrom datetime import datetime,timezone\n"
            "p,stop,interval=sys.argv[1],int(sys.argv[2]),float(sys.argv[3])\n"
            "start=time.monotonic()\nwith open(p,'w',encoding='utf-8') as out:\n"
            "    while True:\n        now=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')\n"
            "        free=shutil.disk_usage('/').free\n        out.write(f'{now} available_bytes={free}\\n'); out.flush()\n"
            "        if free <= stop or time.monotonic()-start >= interval: break\n        time.sleep(interval)\n")
    proc = subprocess.Popen([sys.executable, "-c", code, str(trace), "4000000000", "5"])
    exit_code = proc.wait(timeout=15)
    with trace.open("a", encoding="utf-8") as out:
        out.write(f"sampler_pid={proc.pid}\nsampler_exit={exit_code}\nsampler_waited=true\nsampler_reaped=true\n")
    return {"schema": "d141jj-worker-sampler-v1", "trace_path": str(trace), "sampler_pid": proc.pid, "interval_seconds": 5, "stop_free_bytes": 4000000000, "exit_code": exit_code, "waited": True, "reaped": True, "worker_first_tool_trace": False, "first_tool_gap": {"status": "FAIL", "reason": "The worker's first tool was source inspection rather than sampler launch; this trace is not backfilled as first-tool coverage."}, "tmpdir_metadata": "regular file pointer; no mkdir performed"}


def read_sampler() -> dict[str, object]:
    lines = regular(EVIDENCE / "disk-trace.txt", "disk trace").decode().splitlines()
    values = [int(m.group(2)) for line in lines if (m := re.match(r"([^ ]+) available_bytes=(\d+)$", line))]
    fields = {line.split("=", 1)[0]: line.split("=", 1)[1] for line in lines if "=" in line and not " available_bytes=" in line}
    if len(values) < 2 or int(fields.get("sampler_pid", "0")) <= 0 or int(fields.get("sampler_exit", "1")) != 0 or fields.get("sampler_waited") != "true" or fields.get("sampler_reaped") != "true":
        raise AssertionError("sampler PID/exit/wait/reap trace incomplete")
    if min(values) <= 4000000000:
        raise AssertionError("sampler crossed 4 GB stop")
    return {"schema": "d141jj-worker-sampler-v1", "trace_path": str(EVIDENCE / "disk-trace.txt"), "sampler_pid": int(fields["sampler_pid"]), "interval_seconds": 5, "stop_free_bytes": 4000000000, "sample_count": len(values), "minimum_available_bytes": min(values), "exit_code": 0, "waited": True, "reaped": True, "stop_reached": False, "worker_first_tool_trace": False, "first_tool_gap": "own source-inspection tool preceded sampler; no backfill claimed", "tmpdir_metadata": "regular file pointer; no mkdir performed"}


def verify_candidates(facts: dict[str, object], sampler: dict[str, object], source_facts: dict[str, object]) -> dict[str, object]:
    SOURCE_CHECKER.INPUTS = INPUTS
    SOURCE_CHECKER.p13_suffixes = suffixes
    result = SOURCE_CHECKER.verify_p13_candidates(source_facts, sampler)
    result.update({"status": "PASS_PRIVATE_D141JJ_CANDIDATES", "d141jj": facts, "sampler": sampler})
    return result


def write() -> dict[str, object]:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    sampler = start_sampler()
    facts = owner_facts()
    source_facts = SOURCE_CHECKER.verify_p13_sources()
    readme, gates = suffixes(source_facts)
    for name, suffix in (("candidate-README.template.md", readme), ("candidate-gate-results.md", gates)):
        base = regular(BASE / name, f"immutable base {name}")
        if sha(BASE / name) != INPUTS[name]:
            raise AssertionError(f"immutable base drifted: {name}")
        (EVIDENCE / name).write_bytes(base + suffix.encode())
    result = verify_candidates(facts, sampler, source_facts)
    (EVIDENCE / "source-manifest.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (EVIDENCE / "sampler-lifecycle.json").write_text(json.dumps(sampler, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (EVIDENCE / "D141jj-note.md").write_text("# D141jj App upstream disclosure\n\n" + f"Option B selects App upstream `{APP_UPSTREAM}` / tree `{APP_TREE}` with proven App `{APP_PROVEN}`. Catch-up `{CATCHUP}` onto `{CATCHUP_BASE}` is uninstalled and first after ZIP for shot-layering. Later conflicts are Elements panel removal, AgentChat test, Runtime pin. No final-head/current-pin/build/ZIP claim or canonical install is made.\n", encoding="utf-8")
    (EVIDENCE / "validation.md").write_text("# D141jj notes validation\n\nStatus: **PASS_PRIVATE_D141JJ_CANDIDATES**.\n\n" + f"Immutable prefixes `{INPUTS['candidate-README.template.md']}` and `{INPUTS['candidate-gate-results.md']}` are conserved; each suffix occurs once. All inherited 32 IDs, prior paragraphs, JSON/fences/placeholders, originals, custody limits and C0 examples remain checked. Exact App base `{APP_UPSTREAM}` / `{APP_TREE}`, proven `{APP_PROVEN}`, catch-up `{CATCHUP}` onto `{CATCHUP_BASE}`, and later conflicts are recorded. `render_readme` ran function-only with the inherited renderer SHA `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`. The sampler PID/exit/wait/reap and 4 GB stop are recorded; first-tool coverage is not claimed.\n\nNo canonical install, product/test/generated/pin/schema change, service request, build, rehearsal, or ZIP was performed.\n", encoding="utf-8")
    (EVIDENCE / "handoff.md").write_text("# D141jj notes handoff\n\nPrepared two private successors in the existing final-notes lineage. Option B selects App upstream `" + APP_UPSTREAM + "` / `" + APP_TREE + "` with proven App `" + APP_PROVEN + "`; catch-up `" + CATCHUP + "` onto `" + CATCHUP_BASE + "` is uninstalled and first after ZIP. Later conflicts are Elements panel removal, AgentChat test, Runtime pin. No final-head/current-pin/build/ZIP claim or canonical install is included.\n", encoding="utf-8")
    (EVIDENCE / "check_notes.py").write_text(Path(__file__).read_text(), encoding="utf-8")
    return result


def verify() -> dict[str, object]:
    facts = owner_facts()
    sampler = read_sampler()
    source_facts = SOURCE_CHECKER.verify_p13_sources()
    return verify_candidates(facts, sampler, source_facts)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--write":
        print(json.dumps(write(), sort_keys=True))
    elif len(sys.argv) == 1:
        print(json.dumps(verify(), sort_keys=True))
    else:
        raise SystemExit("usage: check_notes.py [--write]")
