# D118d independent protected review

Verdict: **FAIL — exact-unapplied setup seam**

- Exact 9-node run: **9 setup errors**, exit 1. First failure: `tests/sdk/test_timeline_capture_projection.py:303`, `KeyError: 'revision_id'`.
- `source_shot` lacks `revision_id`; the identity is under `source_mapping`. The registered `doc.patch` was never reached.
- Canonical field projection and source conservation pass. All 43 original test assertions/ASTs, inputs, goldens, pins, and ordering remain unchanged.
- Runtime pin is clean and D120 target absence was confirmed.
- Ruff, mypy, py_compile, and `git diff --check`: **PASS**.
- This is the second FAIL: escalate to **HARDSol**; no further Luna author.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-final-review-1558/evidence/`

No source or product files were modified. `DONE` and commit message were created.