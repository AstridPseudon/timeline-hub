# P4 rerun base-key review handoff — 0813

**PASS — source/delta review; corrected live body not run.**

## Identity

- Final target SHA: `d3696bbf84e88705fdf825f2b51d74cabe4d316d`
- Final tree: `ecb4e61423cc87a68359c86546fe51c3f7537041`
- Base reviewed against: `f5ec9ed242c6b84aa35743e9e3741088c3e96a87`
- One-file blob: `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py` → `244d6569747824ba77e52645dc8845066b79335e`
- Original rerun blob: `72d11a2a8f9f8915a22e325bc15f2edadbae96ff`
- Unchanged ten-note blob: `b8876628d100897a9dcda6750fc5395a3b5b41f3`

## Finding

The only delta is the explicit mapping of the original `revision_id` and
`publication_id` values to wire keys `base_revision_id` and
`base_publication_id`. The exact base values are preserved. The original
seed/ten-note/shared-closure/restart/undo/redo/show/history/real-peer/conflict
and callback-rerun assertions remain unchanged. The original service run
`3610` recorded `[200, 409, 200]` before the stale old-key assertion failed.

Source qualification is PASS. The target includes `68d54e15a8d...` canonical
hydration and the normal public `timeline.open` → `command`/`commit` →
Runtime/provider route. Runtime pin `a5d4258312c979024865ee704da2d632ca5b2730`
and tree `f74b016ea837f8148db4a602c972073a226ed177` are clean. The existing
`p4-v2-http-nodes` row is unique and unchanged (row SHA-256
`fafc5fa04275856881cb8188f782f00b73caf9492640a34369799738bd0af948`).

## Evidence

- Named node collect-only: **PASS**, 1 collected.
- Scoped Ruff: **PASS**.
- Private-cache mypy: **PASS**, 2 files.
- Exact one-file substitution, `git diff --check`, outside-target scope:
  **PASS**.
- Offline exact pair accepted; independently tampered revision and publication
  each rejected: **PASS**.
- Runtime clean/tree/module-origin preflight and normal `34eac004` vendor-lock:
  **PASS**.

## Body limit

No actual corrected HTTP/body, socket, localhost, browser, service, full,
build, or test-service request was made. Corrected live acceptance remains
unverified; the historical 3610 sequence is retained as evidence only, not a
passing result for this target.

Detailed evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P4-rerun-keys-review-0813/WORKERreport.md`.

