# Validation

Status: **FAIL** due solely to F-001 (unscoped superseded pending statements).

- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141hh-P1-P3-notes-1249/evidence/check_notes.py` — PASS (`PASS_PRIVATE_D141HH_P1_P3_CANDIDATES`); no `--write`.
- `python3 -m json.tool /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141hh-P1-P3-notes-1249/evidence/source-manifest.json` — PASS.
- Independent SHA-256/size recomputation — PASS for the four source publications and all 32 declared originals.
- Independent candidate checks — PASS: README 43,978-byte prefix plus 3,026-byte suffix once; gate-results 39,916-byte prefix plus 3,276-byte suffix once; 32 numbered IDs, balanced fences, and placeholders conserved.
- Controlled production `render_readme` function-only check — PASS with four repository records and missing-gate fallback; caller SHA `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`.

No product/full/browser/live-socket/build/service/main/ZIP/pin/diagnostic action was run. The reviewer’s first probe lacked available-byte samples; the later six-sample trace is separately disclosed and not substituted for first-tool coverage.
