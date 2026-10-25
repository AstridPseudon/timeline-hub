# PASS_SOURCE — F-D86/R2

Reviewed exact commit `72a5e5333171bed4221865329ab48eb233b1bbda` (`_step_undo.py` only, 10 lines). Candidate source SHA-256: `7a90a66a...`; parent: `a38bb078...`.

Findings: the branch is bounded to authenticated, step-bearing singleton `timeline.restore` records without parent clip `at`/`hold` caches. Shallow copying does not affect accepted history, cache/order identity paths, bindings, materialization, compiler causality, or existing guards. `finish()` still performs independent effect-multiset comparison with complete fields and duplicate multiplicity before retaining source order.

Call trace reviewed: `TimelineSession.undo` → `_flush`/registered `commitTimeline` provider → authenticated history → `inverse_stages` → `apply_inverse` → `CommitPatch.finish` → Runtime auth/store.

Static checks:

- AST parse/in-memory compile parent and candidate: PASS; all 42 raise nodes conserved.
- Scoped Ruff: PASS.
- Scoped mypy: PASS.
- `git diff --check`: PASS.

No pytest, imports, function execution, fixtures, probes, services, or full suites ran.

Applicability is only established for historical ID5 `test_last_write_clear_undo_restore_and_restore_inverse`. The other three retained selectors remain unproved; no claim is made that all four are fixed. Candidate remains HELD pending unchanged MAIN proof and the separate regression test.

Evidence: `workers/agt-R2-restore-order-review-0415/evidence/source-review.md`. Worktree remains clean.