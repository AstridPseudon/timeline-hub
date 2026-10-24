## Completed

- Routed genuine unshared popup media additions through the existing `occurrence.add-media` carrier.
- Preserved shared ADD/SWAP fork behavior.
- Added owner, shot, internal timeline, source-pin, and selection-authority guards.
- Added focused A3 regression coverage.

## Tests

- A3 provider: **28 passed**
- Neighbor popup/provider tests: **341 passed**
- TypeScript checks: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` — **passed**
- ESLint changed files with `--max-warnings 0` — **passed**
- `git diff --check` — **passed**

Only the two permitted files were modified. No full suite, browser, backend, or live P2 tests were run per instructions.

Commit message and `DONE` marker written.