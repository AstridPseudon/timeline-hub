# Handoff: AP2 P1 refusal schedule correction

Source: App base `fa5ab71db1be57fd9a531a882090179e012153b8`; final worktree has one modified path, `tests/e2e/local/three-products.p1-chain.spec.ts`.

This is the concrete proposal implementation. The second case holds the authentic normal trim POST after the split is accepted and the request is observed, verifies the accepted split revision/publication pair plus `merge: 'fields'` and the real `at`/`from` reads, executes the real Agent move, and releases the unchanged request through the existing route/outbox path. Its required refusal is `value_conflict` at `parent/config/clips/id:<rightId>/app/astrid`, with the existing tagged conflict-state checks and all original recovery/no-write assertions retained.

Delta: 33 insertions, 14 deletions, confined to the second test. The first case and all helpers are byte-identical. No product or contract behavior was changed, and no fabricated request, read, provider, base, manual commit, or alternate executor was added.

Evidence:

- Existing `playwright.three-products.config.ts` `--list`: exactly 2 tests; no browser/body execution.
- Scoped ESLint: pass.
- Root, Node, and App TypeScript configs: all pass with `--noEmit --incremental false`.
- `git diff --check`: pass.
- Causal-unit1049 independent review: pass within unit scope (16/16), with live Runtime 409 explicitly unproven; that limitation remains applicable here.

Next step: independent no-weakening review, then the orchestrator may request the single existing service/browser run. Do not claim P1 live qualification from these source-only checks.
