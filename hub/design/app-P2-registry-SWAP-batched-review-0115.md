## Diff A — registry0064: FAIL

- Exact author: `4b633d09a796f4c14a2a388c28c46dfc52b055c5`
- Tree: `e248c6fee6c5f6a2008848737a5474e8bb7f7beb`
- Protected blobs matched:
  - Spec `b7ad889b5e492062e70c5fbad6b04cd76758488a`
  - Helper `ac6ecb7f3dc6256d6a4a2099f0aadf889a6e1dc1`
  - Test `f5f9da29dda417a5eeadd2f665dc1c7221871b89`

Finding: lines 518–524 of the spec derive `generationId`/`variantId` from `/media-selection`, then use them as canonical expectations. The authoritative `/media-imports` producer’s generation/variant pair is never cross-checked. A producer swapping those IDs would pass. This violates the requirement for independently source-derived values.

Preserved predicates statically: raw four-field ABI, object/digest/type checks, top-level registry, config absence, old-asset preservation, one-new-asset closure, manifest identity, history/reload/Undo.

Evidence:

- Node20 controls: 25/25
- Vitest semantic/geometry: 18/18
- `tsc --noEmit`: root, app, node passed
- Scoped ESLint: passed
- `git diff --check`: passed
- No browser/service/full-suite run; historical 32587 remains NO-GO

No merge requested for Diff A.

## Diff B — SWAP-11089: PASS

- Exact author: `adf067549915325d5d5c862d59c7e994d8dcd18f`
- Tree: `3091238a3f2afff1002915c9f8f86d4368e49342`
- Blobs:
  - Popup spec `d7da4c234fb921c448bc18e9ac174b1a11dbc4a6`
  - Oracle test `d77ecc3c116453e3b0c1106580f7c5dd905114ea`
  - Unchanged producer `53550b81f0c10322ca360f7205878d602549ae92`

Evidence:

- Popup oracle: 4/4
- A3 producer controls: 37/37
- Playwright list: exactly original ADD and SWAP tests
- Root/app/node TypeScript no-emit: passed
- Scoped ESLint: passed
- Diff and reverse-apply checks: passed

Claims are independently derived from uploaded bytes and pre-save registry, including new/reused aliases and exact occurrence-scoped `created` arrays.

Merge completed: `tl/integration` at `3a2d6067b4`.

No browser/service/full-suite run; original 11089 browser result remains NO-GO.