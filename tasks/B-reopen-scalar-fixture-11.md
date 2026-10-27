Goal

Repair the 34 B-only setup failures in `src/tools/video-editor/commands/commitSession.clipScalar.test.ts`. The tests fail before their scalar-contract assertions because the shared shot-layering fixture now has non-empty shot placement opacity/transform, which B intentionally refuses. Give these scalar-contract tests a supported transform-free placement fixture or equivalent local setup while preserving every scalar assertion and test intent.

Files

- `src/tools/video-editor/commands/commitSession.clipScalar.test.ts`
- Any narrowly necessary test-only fixture helper used exclusively by that suite.

Exact acceptance tests

- `npx vitest run src/tools/video-editor/commands/commitSession.clipScalar.test.ts`
- Request the central targeted lane for the changed test file(s) and report the exact result.
- `git diff --check`.

All 34 previously setup-blocked tests must reach and pass their original scalar assertions. Do not weaken or delete assertions, bypass the projection, disable placement validation, or mark tests expected-to-fail. Compare the pristine staging setup if needed to ensure this is a test-fixture compatibility fix, not a behavior change.

Out of scope

- No production projection changes, no C-owned files, no full suite, browser suite, or render.
- Do not alter shared canonical fixture bytes or its digest.

Evidence

Put evidence files in `$ORCH/workers/B-reopen-scalar-fixture-11/evidence/`, never inside the worktree. Finish with `DONE` and a conventional commit message as usual.
