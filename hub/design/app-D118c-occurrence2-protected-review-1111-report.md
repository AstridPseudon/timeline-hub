## Review report — FAIL / unapplied

Reviewed candidate `2f9c56bb...` against authorbase `942855e5...`.

Findings:

- Only the allowed test file changed.
- Added metadata is not proven necessary: C0 permits omitted `label`/`steps`, defaults `merge=fields`, and preserves native semantic dependencies.
- The additions force `CommitPatch.v2`, changing recorder/effect-boundary behavior.
- Recorded failure remains at line 70; prior authentic output reached `_prove_birth` line 173 with status `1` instead of expected `409`. The candidate does not affect that error path.
- `reads: []` and authored metadata do not establish fixture validity or repair causality.

Conservation passed: 29/29 Assert ASTs, full target test-function AST, semantic inputs, IDs, timing, media, history, inverse/redo/retry, and no-write behavior preserved.

Checks passed:

- Ruff
- Mypy, including parent comparison
- Python compilation
- `git diff --check`
- Source/hash and AST conservation

Behavioral tests were not run per brief; no GREEN or functional-closure claim is made.

Evidence: [review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118c-occurrence2-protected-review-1111/evidence/review.json)

Created the requested commit message and `DONE` marker.