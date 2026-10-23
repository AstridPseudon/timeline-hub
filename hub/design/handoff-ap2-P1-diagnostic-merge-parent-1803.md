# P1 diagnostic merge union report — ap2-P1-diagnostic-merge-parent-1803

## Result

PASS for the bounded first-return merge slice. The worktree began clean at App integration base `3a0d76503a11451f91a5c9b18f9fcb74d009b247`. Exactly the three authorized diagnostic files were replaced with raw bytes from App commit `10390cb9ca7333693168dac2e0904281ef45744f`. No implementation, transport, authority, product, generated, pin, lockfile, suite-row, process, kit, or unrelated test changes were made.

## Exact union and identities

Base: `3a0d76503a11451f91a5c9b18f9fcb74d009b247`

Donor: `10390cb9ca7333693168dac2e0904281ef45744f`

Changed paths, and only changed paths:

- `tests/e2e/local/three-products.p1-chain.spec.ts`
  - worktree Git blob: `feb26946d62db9a4a02dab8dca1c0dc7320f2681`
  - required donor Git blob: `feb26946d62db9a4a02dab8dca1c0dc7320f2681`
- `tests/e2e/local/p1-diagnostic-safety.ts`
  - worktree Git blob: `a49f6bfb20c21b01bc709db79d3fa3cd47b216c3`
  - required donor Git blob: `a49f6bfb20c21b01bc709db79d3fa3cd47b216c3`
- `tests/e2e/local/p1-diagnostic-safety.test.ts`
  - worktree Git blob: `3b72ee8fff59b6d7e9919aa936f0ac3e6d9a4ff5`
  - required donor Git blob: `3b72ee8fff59b6d7e9919aa936f0ac3e6d9a4ff5`

The approved first-case identity remains `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`; the approved original second suffix remains `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`.

## Evidence commands and results

Node toolchain:

`N=/home/user/work/runtimes/agent-remotion-ap2-current-079-2a9-1743/.toolchain/node-v20.19.4-linux-x64/bin/node`

Read-only dependency graph:

`D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules`

- `N --import D/tsx/dist/loader.mjs tests/e2e/local/p1-diagnostic-safety.test.ts` — PASS, 12/12 named tests.
- `N node_modules/typescript/bin/tsc --noEmit` — PASS.
- `N node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit` — PASS.
- `N node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit` — PASS.
- `N node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p1-chain.spec.ts tests/e2e/local/p1-diagnostic-safety.ts tests/e2e/local/p1-diagnostic-safety.test.ts --max-warnings 0` — PASS.
- `N node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list` — PASS, exactly 2 tests listed.
- `git diff --check 3a0d76503a11451f91a5c9b18f9fcb74d009b247` — PASS.
- Changed-path audit against the base — exactly the three paths listed above.
- Changed-diff conflict-marker audit — none.

## Decisions and limits

- Applied the settled plan and the full correlated-sol review as written; no design decisions were revisited.
- Used the available exact handoff at `ORCH/design/handoff-ap2-P1-correlated-sol-review-1741.md`; the older `scratchpad/luna/reports` path named in the brief was absent.
- Preserved the existing mounted persisted funnel and all current product/outbox, first lost-ACK/body/key/owner/scope/restart/history/drain/refusal assertions.
- P1 remains source/targeted diagnostic-safety evidence only: NO-GO for the original mounted journey and product cause UNKNOWN. No source-only behavioral GO is claimed.
- No full suite, live browser journey, HTTP/body/live socket service run, global setup, seed/provisioning/install, bench, or full e2e was run.
- No Git mutation, commit, merge, rebase, reset, fetch, push, branch/ref deletion, shared dependency mutation, or cache mutation was performed by this worker. The harness owns the designed merge-parent commit step after exit.

