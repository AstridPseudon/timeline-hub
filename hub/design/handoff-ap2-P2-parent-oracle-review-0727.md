## P2 parent oracle review — FAIL

Parent source/helper shape is correct and source-derived:

- Exact `doc.patch`, `created: []`, `merge: fields`
- Exact `Move <clip> on <track>` metadata
- Exact ordered guarded changes and reads from `timelineLocalSaveHandoff.ts:517–558`
- Full request shape enforced with `toEqual`

However, the parent control suite is incomplete. It does not exercise required rejection cases for:

- Wrong read path/value/state
- Extra command/step/select/args keys
- Altered base metadata

Therefore the parent delta is not qualified, despite the helper itself being strict.

Inherited transition `d17cd19ee3` remains separate HOLD/known FAIL; its broad matching and missing wrong-read controls are not attributed to this parent delta.

Checks, all exit 0:

- `/opt/node20/bin/node --test tests/e2e/local/support/p2-parent-oracle.test.mjs` — 2/2 passed
- Three serialized TypeScript checks: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`
- ESLint on touched files
- Playwright list-only with `playwright.three-products.config.ts` — exactly 3 tests collected
- `git diff --check` — passed

No browser journey, backend/HTTP/service call, or original run was performed. Worktree remained clean.

Reviewed parent delta: `d17cd19ee3 → 0b431ac439`  
Hashes:

- `three-products.p2-tour.spec.ts`: `2eb041e18711db0e9e81966604fd8616ad3819e75e3798ed1c1f2c32cfff0b8e`
- `p2-parent-oracle.test.mjs`: `58e121cba2245d697cc00a4338bef76b9e72d1ca752a51071e20dfacf89e8cb8`

Recommended next step: add the missing explicit negative variants, then rerun the narrow controls.