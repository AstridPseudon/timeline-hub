# P3 corrected review handoff

Reviewed App base `tl/ap2-P3-assertion-first-return-0400` at
`206d5f30c22b68975d94942430278a581140a0a4` (tree `36b9938e`) against original
`7116a8e28`, the settled PLAN §3 P3 scope, contract §§1/3/4/5/7, and the 0355
and 0400 handoffs.

## Disposition

**FAIL / request changes.** The source correction is not ready for merge. No
worktree files were changed by this reviewer.

## Findings

- **Blocking:** `recordedSite()` in `tests/e2e/local/three-products.spec.ts:997-1002`
  converts native recorder refs `parent/clip:<id>` to
  `parent/config/clips/id:<id>`, while the contract's authoritative native
  step patch uses `parent/clip:<id>` plus the leaf path. The `matchingEffects`
  assertion at `:982-990` therefore cannot match the normal Gate-5 App
  `clip.move` write. The fixture's parent clips are also top-level `clips`, not
  `config.clips`.
- **Secondary:** the dependency loop at `:975-980` projects only recorder
  `reads` by ref/path and permits a broad timeline dependency; it does not
  prove recorder `dependencies`, `selections`, `bindings`, or their observed
  state/boundary contents against the authoritative step dependency union.
- **Secondary:** the submitted-patch check at `:956-960` uses
  `expect.arrayContaining`, so it does not prove the contract's exact ordered
  `doc.patch` step-patch equality.

## Preserved behavior/source scope

The one-file delta changes only the v2 history helper. Original A/C/B ordering,
lost ACK, reload/restart, exact retry, complete immutable closure/component
readback, opaque/C preservation, mounted undo, history counts, and zero legacy
traffic assertions are still present and unweakened. The helper is called from
the real mounted App/outbox posts for accepted A, merged B, and mounted undo;
the Agent C remains the real intervening writer. Conflict, invalid, preview,
and unrelated reply families are not claimed by this Gate-5 journey.

The digest assertion recomputes the complete `data.canonical_document` using
the documented sorted compact JSON/SHA-256 algorithm. This source review found
no TypeScript semantic executor or hand-authored expected digest.

## Static evidence

- Exact Gate-5 title collection with explicit isolated ports: **PASS**, 1 test.
- `npm exec tsc -- --noEmit`: **PASS**.
- `npx eslint tests/e2e/local/three-products.spec.ts --max-warnings 0`: **PASS**.
- `git diff --check`: **PASS**.

The service `29980` setup attempt failed before behavioral execution because
`TIMELINE_BUNDLE_AGENT_HEAD` was missing after the repaired hosted build. Do not
call that a behavioral failure or PASS. Gate-5 remains **UNQUALIFIED** until the
native-path assertions are repaired and the same central service case runs.
