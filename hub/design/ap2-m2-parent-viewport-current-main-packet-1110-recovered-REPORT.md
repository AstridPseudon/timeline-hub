# App2 parent viewport packet report

## Result

Composed the original parent mounted ADD journey onto current HOME in
`tests/e2e/local/three-products.spec.ts`.

- Ported only donor `9018c733c429f3ad176bebf26c6351fce0414da1`'s geometry setup:
  rendered V1/anchor waits, one existing `Zoom out timeline` click, measured
  wrapper containment, centered-pointer math, and noncollision assertion.
- Restored/preserved the strict full 404 body from parent0939:
  `not_found`, exact refusal message, and safe request-id matcher.
- Preserved pointer `22.5`, native target `V1`, left `20`, both original drop
  calls, File/DataTransfer dispatch, native ADD, retry/restart/undo, opaque,
  order/source/epoch/ACK/raw/hold, and zero-legacy assertions.
- No live callers changed: `NONE` (source/test-only).

The resulting spec is byte-identical to donor `9018c733c429f3ad176bebf26c6351fce0414da1`'s
`tests/e2e/local/three-products.spec.ts` blob
`e612c18cac2a651e855e75388498762f034dc63a`.

## Checks run

- `git diff --check` — PASS.
- `./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --ext ts --max-warnings 0` — PASS (about 123s; no output).
- `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=/tmp ./node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts:1410 --list` — PASS; exactly 1 intended test/title listed.
- `cmp <(git show 9018c733c429f3ad176bebf26c6351fce0414da1:tests/e2e/local/three-products.spec.ts) tests/e2e/local/three-products.spec.ts` — PASS.
- Existing 0939 helper/driver/final-gate SHA checks — PASS; shared helper and driver were not modified.
- Current source ancestry from pointer fix `44e9a83bcc155e713da56b1e0aaed8c2f88dd1e0` — PASS.
- Current source: HEAD `0cc2583aaf07e89190b9344b5ac82849d6279586`, tree
  `320e74a93676c781e83885b86ec237b4a1465d80` before this worker commit.

No browser, socket/service, central actual, build, install, full suite, or
targeted mounted execution was run. The real strict refusal, ADD, retry,
restart, undo, and zero-legacy qualification therefore remains unverified.

## Handoff/blockers

The durable handoff is [run-on-main-app2-parent-viewport.md](run-on-main-app2-parent-viewport.md).
It contains the exact frozen R4 branch/source SHAs, existing guarded command,
sanitized `env -i` invocation, required paths, short socket roots, Remotion
renderer-off environment, disk/toolchain/graph/argv/list/retention preflight,
and the combined main portability failures.

The harness final commit is unavailable in this worker. Pending fields are:

```text
parent_role_sha=PENDING_HARNESS_FINAL_COMMIT
parent_role_tree=PENDING_HARNESS_FINAL_TREE
```

Exact remaining step: harness commits the worktree, then the orchestrator
resolves the final 40-hex SHA/tree, data-binds those fields in a private copy
of the existing 0939 gate, runs the aggregate preflight, and schedules one
fresh actual. This packet is not READY and makes no execution claim.

Decision: keep the donor's existing UI zoom operation and full geometry
preconditions; do not change the pointer, placement, timeout, viewport, or
production code because parent0939 diagnosed the failure specifically at the
mounted viewport guard.
