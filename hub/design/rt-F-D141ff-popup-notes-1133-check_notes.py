#!/usr/bin/env python3
"""Generate and validate the private D141ff popup known-gap note candidates."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import stat
import sys
from pathlib import Path


EVIDENCE = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/rt-F-D141ff-popup-notes-1133/evidence"
)
CANONICAL = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/delivery"
)
HUB_DESIGN = Path("/home/user/timeline-hub/hub/design")
PUBLICATION = HUB_DESIGN / "app-D141cc-popup-terminal-publication-1122.json"
RESULTS = HUB_DESIGN / "app-P-D141cc-popup-controller-next-results.json"
SOURCE_MANIFEST = HUB_DESIGN / "app-P-D141cc-popup-controller-next-source-manifest.json"
CUSTODY_PUBLICATION = HUB_DESIGN / "app-D141ff-popup-custody-publication-1127.json"
RENDER_SOURCE = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/design/runtime-final-unit-notes-input-0849-delivery-build.py"
)

EXPECTED_PREIMAGES = {
    "README.template.md": "48013c7fbcb8f72a7d4371540b50a4abcc43dd8c6274d90726beec82b8f9fc02",
    "gate-results.md": "506e4461b63e81af490e4b43c5eb7fe2717ebb07825c77d216a59967d863a55d",
}

README_SUFFIX = """

## D141ff popup ADD known gap (bounded documentary note)

D141ff records the popup ADD as a documented known gap on the frozen final tuple, alongside SWAP and Element. The genuine normal service result `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-popup-retry-1-1026111307-27026` exited 1 in 207 s: readiness **PASS**, popup **FAIL**, because the `f2-occurrence-copy` shared-occurrence label was absent within 5 s. Cause: **UNKNOWN**. The retained original pointer is `app-pin-867cb273-d141-p2-popup-add-867cb273-submit-1026014140-1368`; this note does not reconstruct it.

The cancelled operational attempts `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-1026102149-13234` and `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-1026102155-20413` remain custody failures with no functional verdict and are not credited. Independent actual custody review remains pending unless its genuine published verdict arrives; neither source publication nor author receipts establish custodyPASS. The owner wording is: "failing since the freeze-1 upstream merge (4de era); cause under diagnosis".

This is our own non-REG P2 known gap and is non-blocking for ZIP. Diagnostic is **NOTRUN** and non-blocking; D141j permits it only after the six selectors and first four-field visibility proof. No diagnostic action is taken here. Final pins, installation, and build remain separately gated.
"""

GATE_SUFFIX = """

## D141ff popup ADD known gap (bounded documentary note)

The genuine normal service result `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-popup-retry-1-1026111307-27026` is a functional FAIL: exit 1 in 207 s, readiness PASS, popup FAIL, and the `f2-occurrence-copy` shared-occurrence label was absent within 5 s. Cause is UNKNOWN. Retain the original pointer `app-pin-867cb273-d141-p2-popup-add-867cb273-submit-1026014140-1368`; do not reconstruct it. Cancelled operational attempts `...13234` and `...20413` have no functional verdict and are not credited. No source or author receipt establishes custodyPASS; independent actual custody review remains pending unless its genuine published verdict arrives.

Owner wording: "failing since the freeze-1 upstream merge (4de era); cause under diagnosis". This is our own non-REG P2 known gap, non-blocking for ZIP, alongside SWAP and Element. Diagnostic is NOTRUN and non-blocking, allowed only after the six selectors and first four-field visibility proof; no diagnostic action is included here. Final pins, installation, and build remain separately gated.
"""


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"{label}: expected regular non-symlink: {path}")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode != 0o644:
        raise AssertionError(f"{label}: expected mode 0644, got {mode:04o}: {path}")
    return path.read_bytes()


def json_file(path: Path, label: str) -> object:
    return json.loads(regular(path, label))


def source_hashes() -> dict[str, object]:
    publication = json_file(PUBLICATION, "popup terminal publication")
    assert isinstance(publication, dict)
    originals = []
    for index, item in enumerate(publication["files"], 1):
        published = HUB_DESIGN / Path(item["published"]).name
        raw = regular(published, f"hash-exact original {index}")
        actual = sha256_bytes(raw)
        expected = item["sha256"]
        if actual != expected:
            raise AssertionError(
                f"hash-exact original {index}: {published}: {actual} != {expected}"
            )
        originals.append(
            {
                "index": index,
                "path": str(published),
                "sha256": actual,
                "bytes": len(raw),
                "mode": "0644",
                "regular_non_symlink": True,
            }
        )
    return {
        "publication": {
            "path": str(PUBLICATION),
            "sha256": sha256_bytes(PUBLICATION.read_bytes()),
            "status": publication["status"],
        },
        "eight_hash_exact_originals": originals,
        "results": {
            "path": str(RESULTS),
            "sha256": sha256_bytes(RESULTS.read_bytes()),
        },
        "source_manifest": {
            "path": str(SOURCE_MANIFEST),
            "sha256": sha256_bytes(SOURCE_MANIFEST.read_bytes()),
        },
        "custody_publication": {
            "path": str(CUSTODY_PUBLICATION),
            "sha256": sha256_bytes(CUSTODY_PUBLICATION.read_bytes()),
            "verdict": json_file(CUSTODY_PUBLICATION, "custody publication")["verdict"],
        },
    }


def controlled_results() -> list[dict[str, object]]:
    rows = []
    for index, name in enumerate(("agent", "runtime", "app", "composition"), 1):
        rows.append(
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
        )
    return rows


def render_function_only(template: Path, gates: Path) -> dict[str, object]:
    spec = importlib.util.spec_from_file_location("delivery_build_render_only", RENDER_SOURCE)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load render source: {RENDER_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rendered = module.render_readme(controlled_results(), str(template), str(gates))
    if any(token in rendered for token in ("{{UTC}}", "{{REPO_SUMMARY}}", "{{REPO_SECTIONS}}", "{{GATE_RESULTS}}")):
        raise AssertionError("controlled render left a template placeholder")
    if rendered.count("```") % 2:
        raise AssertionError("controlled render has unbalanced fences")
    if rendered.count("D141ff popup ADD known gap") != 2:
        raise AssertionError("controlled render did not include each disclosure exactly once")
    missing_gate = EVIDENCE / "missing-gate-results-for-fallback.md"
    fallback = module.render_readme(controlled_results(), str(template), str(missing_gate))
    if "_Not recorded yet." not in fallback:
        raise AssertionError("render fallback did not retain missing-gate notice")
    return {
        "function_only": True,
        "function": "render_readme",
        "caller": str(RENDER_SOURCE),
        "caller_sha256": sha256_bytes(RENDER_SOURCE.read_bytes()),
        "controlled_inputs": ["agent", "runtime", "app", "composition"],
        "placeholders_resolved": True,
        "balanced_fences": True,
        "disclosure_occurrences": rendered.count("D141ff popup ADD known gap"),
        "fallback_placeholder_behavior": True,
        "rendered_sha256": sha256_bytes(rendered.encode()),
        "fallback_sha256": sha256_bytes(fallback.encode()),
    }


def verify() -> dict[str, object]:
    preimages: dict[str, bytes] = {}
    for name, expected in EXPECTED_PREIMAGES.items():
        raw = regular(CANONICAL / name, f"canonical preimage {name}")
        actual = sha256_bytes(raw)
        if actual != expected:
            raise AssertionError(f"canonical preimage drift at {CANONICAL / name}: {actual} != {expected}")
        preimages[name] = raw

    candidates = {
        "README.template.md": EVIDENCE / "candidate-README.template.md",
        "gate-results.md": EVIDENCE / "candidate-gate-results.md",
    }
    expected_suffixes = {"README.template.md": README_SUFFIX.encode(), "gate-results.md": GATE_SUFFIX.encode()}
    candidate_meta = {}
    for name, path in candidates.items():
        raw = regular(path, f"candidate {name}")
        prefix = preimages[name]
        suffix = expected_suffixes[name]
        if not raw.startswith(prefix):
            raise AssertionError(f"candidate {name}: preimage prefix is not byte-exact")
        if raw[len(prefix):] != suffix:
            raise AssertionError(f"candidate {name}: suffix differs from the sole intended D141ff suffix")
        if raw.count(suffix) != 1:
            raise AssertionError(f"candidate {name}: intended suffix occurs other than once")
        candidate_meta[name] = {"path": str(path), "sha256": sha256_bytes(raw), "bytes": len(raw), "suffix_bytes": len(suffix)}

    readme = candidates["README.template.md"].read_text()
    gate = candidates["gate-results.md"].read_text()
    for text, label in ((readme, "README"), (gate, "gate-results")):
        if text.count("```") % 2:
            raise AssertionError(f"{label}: unbalanced fenced blocks")
    for token in ("{{UTC}}", "{{REPO_SUMMARY}}", "{{REPO_SECTIONS}}", "{{GATE_RESULTS}}"):
        if readme.count(token) != 1:
            raise AssertionError(f"README: placeholder {token!r} count is not one")
    if len(re.findall(r"^\d+\. ", gate, flags=re.MULTILINE)) != 32:
        raise AssertionError("gate-results: complete 32-ID table is not conserved")
    for text, label in ((readme, "README"), (gate, "gate-results")):
        for marker in ("# D141 documented known gaps", "**SWAP.**", "**Element.**", "Idempotency-Key", "D139a installed schema input"):
            if marker not in text:
                raise AssertionError(f"{label}: conserved marker missing: {marker}")
    render = render_function_only(candidates["README.template.md"], candidates["gate-results.md"])
    return {
        "status": "PASS_PRIVATE_D141FF_CANDIDATES",
        "preimages": {name: {"sha256": sha256_bytes(raw), "bytes": len(raw), "mode": "0644", "regular_non_symlink": True} for name, raw in preimages.items()},
        "candidates": candidate_meta,
        "source_hashes": source_hashes(),
        "render": render,
        "conservation": {
            "full_preimage_prefix": True,
            "only_intended_suffix_once_per_document": True,
            "previous_known_gaps_and_32_ids": True,
            "balanced_fences_and_placeholders": True,
        },
        "scope": "private documentary candidates only; no canonical write, install, build, service, diagnostic, or product test",
    }


def write_candidates() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for name, suffix in (("README.template.md", README_SUFFIX), ("gate-results.md", GATE_SUFFIX)):
        raw = regular(CANONICAL / name, f"canonical preimage {name}")
        expected = EXPECTED_PREIMAGES[name]
        if sha256_bytes(raw) != expected:
            raise AssertionError(f"canonical preimage drift at {CANONICAL / name}")
        (EVIDENCE / f"candidate-{name}").write_bytes(raw + suffix.encode())
    note = """# D141ff popup ADD known-gap note

The genuine normal service result `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-popup-retry-1-1026111307-27026` exited 1 in 207 s: readiness PASS, popup FAIL, and the `f2-occurrence-copy` shared-occurrence label was absent within 5 s. Cause is UNKNOWN. Retain original pointer `app-pin-867cb273-d141-p2-popup-add-867cb273-submit-1026014140-1368`. Cancelled operational attempts `...13234` and `...20413` have no functional verdict. The owner wording is: "failing since the freeze-1 upstream merge (4de era); cause under diagnosis".

This is our own non-REG P2 known gap, non-blocking for ZIP, alongside SWAP and Element. Independent custody review is not claimed as custodyPASS. Diagnostic is NOTRUN and non-blocking, allowed only after the six selectors and four-field visibility proof; no diagnostic action is included.
"""
    (EVIDENCE / "popup-note.md").write_text(note)


def write_receipts(result: dict[str, object]) -> None:
    (EVIDENCE / "source-manifest.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (EVIDENCE / "validation.md").write_text(
        "# D141ff popup note validation\n\n"
        "Status: **PASS_PRIVATE_D141FF_CANDIDATES**.\n\n"
        "- Canonical README and gate-results preimages matched the required hashes and remained regular `0644` non-symlinks.\n"
        "- Both candidates conserve the complete preimage byte prefix and add only the bounded D141ff popup suffix once.\n"
        "- The previous known gaps, 32-ID table, ledger/witness/limits, and C0 prose remain in the conserved prefix.\n"
        "- All eight hash-exact D141cc originals matched their published SHA-256 bindings.\n"
        "- Controlled `delivery-build.render_readme` was exercised as a function only with four controlled repository records; placeholders resolved, fences balanced, and the fallback was checked.\n"
        "- Popup result 27026 is retained as genuine service FAIL (readiness PASS, popup FAIL, missing shared-occurrence label within 5 s, cause UNKNOWN). Original 1368 is retained as a pointer; cancelled 13234/20413 have no functional verdict. No custodyPASS is claimed.\n"
        "- The first-tool sampler coverage gap is recorded in `sampler-lifecycle.json`; the restarted sampler records its own PID and terminal lifecycle.\n\n"
        "No canonical write, installation, build, service, diagnostic, product test, or full suite was run.\n"
    )
    (EVIDENCE / "handoff.md").write_text(
        "# D141ff popup note handoff\n\n"
        "Prepared private README and gate-results successor candidates with only the authorized D141ff popup ADD known-gap suffix.\n\n"
        "The note preserves the original 1368 pointer and actual 27026 result, records cancelled 13234/20413 as operational failures without functional verdicts, and does not claim custodyPASS. The exact owner wording is retained: `failing since the freeze-1 upstream merge (4de era); cause under diagnosis`. Diagnostic remains NOTRUN and non-blocking, with no diagnostic action.\n\n"
        "Canonical delivery files were not written or installed. Final pins, installation, and build remain separately gated.\n"
    )


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--write":
        write_candidates()
        result = verify()
        write_receipts(result)
        print(json.dumps({"status": result["status"], "candidates": result["candidates"]}, sort_keys=True))
        return 0
    if len(sys.argv) != 1:
        raise SystemExit("usage: check_notes.py [--write]")
    result = verify()
    print(json.dumps({"status": result["status"], "candidates": result["candidates"], "render": result["render"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
