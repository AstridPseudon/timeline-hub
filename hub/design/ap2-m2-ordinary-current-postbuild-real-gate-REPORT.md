# AP2 M2 ordinary current post-build real gate

## Dependency hold (2026-10-20 23:06 UTC)

The worker is based on `b1887f206` (`tl/ap2-m2-ordinary-reviewed-current-delivery-packet`),
with a clean App worktree. The reviewed ordinary packet and the approved `966472b6`
undo-oracle conversion are present. The prior central run `30322` is retained as a
build-only failure: hosted Vite stopped before Playwright because the deleted
`src/tools/video-editor/lib/theme-api.fallback.tsx` was still referenced. It is not
journey evidence and has not been rerun.

HOME's existing public-export setup repair is the required prerequisite. It is not
published in the orchestration records yet; current App status still identifies
`gate35-retired-alias-setup-causal-fix` as HOME-owned and says no fallback restoration
or unchanged rerun is allowed.

Requested handoff from HOME: publish the exact committed setup-repair source identity
(commit/tree and report) once available. The worker will incorporate only that exact
test-local/current-compatible delta, preserving the deleted fallback boundary and the
existing ordinary driver/wrapper. No schema, pin, dependency, cache, Viewing/shared
harness, or product-writer changes are authorized.

HOME subsequently published the repair in current integration `ce6deafa3`; the exact
repair commit is `e401af7215e9adf54b1cb4c5bce8d386721bec7d`. Its only changed path is
`config/vite/vite.config.ts`, and its 22-line deletion removes the stale
`@banodoco/timeline-composition/{registry.generated,theme-api}` aliases plus the two
deleted fallback paths. The worktree copy matches that commit's file byte-for-byte.

Preflight after applying the exact delta:

```text
node --check .../chromium-env-smoke.mjs                         PASS
sh -n .../run-central-m2-ordinary.sh                           PASS
vitest run --no-cache ... genericPatchCapture ordinaryRealBatch threeProductsAuthoring
  3 files, 21 tests passed
eslint --no-warn-ignored --max-warnings 0 config/vite/vite.config.ts  PASS
git diff --check                                                   PASS
```

## Planned evidence after the hold clears

Run one `--no-cache` central named ordinary gate through the existing
`e2e-m2-ordinary-committed-driver-gate` driver/wrapper, after its exact-source
preflight. The gate must retain the ten complete SDK `8130` command/record equality,
disjoint `S1` Agent versus `V1` App intent, independent pre-edit plus literal-C undo
oracle, raw/opaque/order/closure/manifest/credentials/zero-legacy/conflict guards,
lost acknowledgement, restart/retry, and guarded undo assertions. No full suite and no
repeated unchanged build will be requested.
