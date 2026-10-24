## Result: PASS — partial A4 cut only

Reviewed commit `fb27e554a9` against PLAN A4/U3/A2.

- Exactly `media.ts` and `media.test.ts` changed: `148+ / 14−`.
- Prepared preview no longer calls `mediaCommandRunner.apply`.
- Direct builder/duplication path preserves refusal ordering, config validation, history, metadata, and output parity with the retained runner.
- All 53 prior media assertions remain; six refusal cases and descriptor-method bypass coverage pass.
- Remaining runner/provider/state/history imports are expected and explicitly outside this partial cut.

Tests:

```text
11 targeted files: 152 passed
tsconfig.json: passed
tsconfig.app.json: passed
tsconfig.node.json: passed
scoped ESLint: passed
git diff --check: passed
```

Tests used a private TMPDIR Vitest config/preload with Node 20 and the existing dependency graph. No fixture overlay was used. Known persistence-fixture failures were not rerun.

No source or tracked test edits were made. `DONE` and the required commit message were written.