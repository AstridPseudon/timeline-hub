# AP2 M2 ordinary current post-build real gate

## Result (2026-10-20 23:10 UTC)

The worker is based on `b1887f206` (`tl/ap2-m2-ordinary-reviewed-current-delivery-packet`),
with a clean App worktree. The reviewed ordinary packet and the approved `966472b6`
undo-oracle conversion are present. The prior central run `30322` is retained as a
build-only failure: hosted Vite stopped before Playwright because the deleted
`src/tools/video-editor/lib/theme-api.fallback.tsx` was still referenced. It is not
journey evidence and has not been rerun.

HOME's existing public-export setup repair was published in current integration
`ce6deafa3`; the exact repair commit is `e401af7215e9adf54b1cb4c5bce8d386721bec7d`.

The exact repair's only changed path is
`config/vite/vite.config.ts`, and its 22-line deletion removes the stale
`@banodoco/timeline-composition/{registry.generated,theme-api}` aliases plus the two
deleted fallback paths. The worktree copy matches that commit's file byte-for-byte.

No schema, pin, dependency, cache, Viewing/shared harness, or product-writer changes
were made. The existing ordinary driver/wrapper was used unchanged.

Preflight after applying the exact delta:

```text
node --check .../chromium-env-smoke.mjs                         PASS
sh -n .../run-central-m2-ordinary.sh                           PASS
vitest run --no-cache ... genericPatchCapture ordinaryRealBatch threeProductsAuthoring
  3 files, 21 tests passed
eslint --no-warn-ignored --max-warnings 0 config/vite/vite.config.ts  PASS
git diff --check                                                   PASS
```

## Central gate

Submitted exactly once:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-current-postbuild-real-gate e2e-m2-ordinary-committed-driver-gate --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: **FAIL**, exit 1, 104 seconds. Hosted build, Chromium smoke, exact source
preflight, and the one-test collection all passed. The mounted journey reached the
final guarded ordinary undo oracle after the ten complete SDK `8130` records, the
disjoint `S1` Agent / `V1` App intent, lost acknowledgement, restart, exact retry,
rebase, and prior inverse assertions.

First product failure:

```text
tests/e2e/local/three-products.spec.ts:1311
expect(undoOrdinary.data.canonical_document.shot_revisions)
  .toEqual(beforeDocument.shot_revisions)
Expected: undefined
Received: one sanitized f2-shot revision record
```

The failure is an oracle/fixture-shape mismatch to hand back for diagnosis: the
pre-edit composition response exposed `beforeDocument.shot_revisions` as undefined,
while the accepted undo response exposed one `f2-shot` record. The test therefore
does not establish that the Runtime inverse lost a pre-edit shot; it establishes that
the independent oracle's source response and the post-undo closure differ at this
field. The failure was retained as-is; the positive expectation was not changed.

The retained response excerpt contains one `f2-shot` revision with the original
opaque payload and materialized revision IDs; it is not copied into this report. The
central result directory retains the exact log/summary/request/snapshot:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-ordinary-current-postbuild-real-gate-e2e-m2-ordinary-committed-driver-gate-1020230758-12181/`

Sanitized source identity from the run: App snapshot tree
`1a62ab67be6f61834d92fdacaf9ec383dc10f3a`; runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`;
Agent `8130a401bf44a518d5a40ae274d398b8c560be55`; Composition archive SHA
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

No writer cut was prepared: the ordinary gate failed, so no deletion claim is
authorized. No rerun, local browser/socket run, full suite, assertion weakening, or
fallback restoration was performed.
