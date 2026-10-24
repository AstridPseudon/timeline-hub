## P2 catalog/params/inverse + owner-readiness review — FAIL

Reviewed `1227b3e92f` against base `672127b534`. No tracked files changed; worktree remains clean.

Findings:

- Readiness helper accepts an unscoped fresh owner because `!owner.scope` passes the filter (`p2-original-owner-ready.ts:18-19`). Diagnostic result: `unscoped owner accepted: true`. This violates matching-scope readiness.
- Oracle controls do not exercise required wrong-read value/path/state or extra metadata negatives.
- Catalog insert/value and inverse step/source assertions retain permissive nested `toMatchObject`/`objectContaining` checks, so extra or malformed metadata can pass.
- Current producer source confirms the catalog/params patch shapes and inverse metadata; those source facts were not altered.
- Original request/reply/history/reload/undo tails remain present in the diff.

Checks:

- Helper/readiness tests: 16/16 passed.
- TypeScript: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` — all passed.
- Scoped ESLint — passed with `--max-warnings 0`.
- Playwright list-only: 3 tests collected, no execution.
- `git diff --check` — passed.
- No browser, backend, HTTP, service, full-suite, or request-body evidence run.

Hashes:

- Base: `672127b534842ce3a92b9d8caf7c55ffb59602fd`
- Reviewed head: `1227b3e92fc4138585a2b5a5f33c9e73f35480da`
- Diff SHA-256: `1b0767e3a01fa4832789c4cbe4b96c8d9613f1bf4892eb165f9a1c0193286951`

Inherited semantic-672 packet remains HOLD and was not qualified. Recommended next step: require scoped-owner rejection and add explicit wrong-read/state/path, extra metadata, and strict nested-shape negative controls.