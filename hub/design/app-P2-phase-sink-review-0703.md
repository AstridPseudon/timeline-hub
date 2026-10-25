# P2 phase-sink startup review — FAIL

Reviewed `4ec66d0d0d` against `f7201e02dc`. No source changes made; only the four assigned files differ.

Finding: D105 does not prove two ordinal-2 harness starts. It loads the “old” harness with `git show HEAD`, which is the current new harness, so the required old-red/new-green control fails with `secondError === undefined`. The parent implementation would collide on the original sink.

The actual caller can start multiple Playwright-stage harnesses: three P2 files, worker-scoped fixtures, and a separate placement fixture pool. All use the same `output/runtime-private` and ordinal `2`; subsequent starts collide on `p2-commit-phase-2.jsonl` and `runtime.*-2.log`. Existing fail-closed collision and `wx` protections remain intact.

Tests/checks:

- Node20 D66 suite: 27 total, 26 passed, 1 failed (D105 control).
- Node20 targeted bootstrap: 1 passed, 2 failed due the known pre-existing Runtime helper ABI mismatch.
- `tsc` app and node projects: PASS.
- Scoped ESLint on all four files: PASS, 0 warnings.
- Node20 syntax checks and `git diff --check`: PASS.
- Diff: 4 files only; no product, protected-original, generated, pin, or source changes.

`DONE` and commit message were written. The final response is the report; no direct `report.md`/design sidecar was created per worker reporting rules.