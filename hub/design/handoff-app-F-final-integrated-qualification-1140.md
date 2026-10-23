# F-App final integrated residual qualification — PASS

## Identity and scope

- App HEAD: `ad96a4cac58771baf5fbe2b07f30cccce4340040`
- App tree: `f7ae7964edfb4a6152e9e693fd443656aa6ab601`
- Worktree: clean after restoring the original `node_modules` symlink; no product, test, generated, pin, or lock files were changed.
- Delta after retained qualification base `eed7e6006`: exactly three reviewed paths:
  - `src/tools/travel-between-images/components/shotTimelineDataProvider.ts` (`8fdf0a1ef` correction)
  - `tests/e2e/local/auto-real-proxy.spec.ts` (`be8f4296c` reviewed P2 proof)
  - `tests/e2e/local/three-products.p1-chain.spec.ts` (`bb29559b6` reviewed P1 proof)
- Both e2e commits and `8fdf0a1ef` are ancestors of `ad96a4cac`; no other post-`eed7e6006` product/test delta exists.

## Tests and checks

- Exact farm residual command from the brief, with the worker-owned private dependency graph: **exit 0, 20 files, 353/353 tests**.
- Focused changed-provider command: `src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts`: **exit 0, 25/25 tests**.
- `./node_modules/.bin/tsc --noEmit -p tsconfig.json --pretty false`: **exit 0**.
- `node ./node_modules/.bin/tsc --noEmit -p tsconfig.node.json --pretty false`: **exit 0**.
- `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false`: **exit 0**.
- `./node_modules/.bin/eslint src/tools/travel-between-images/components/shotTimelineDataProvider.ts --max-warnings 0`: **exit 0**.
- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=2 src/integrations/runtime/vendorLock.test.ts`: **exit 0, 13/13 tests**.
- `node scripts/build/verify-astrid-vendor-sources.mjs`: **exit 0**; 65 pinned Astrid closure files, 159 browser vendor files, 11 public imports.
- `node --test scripts/quality/check-no-remote-hosts.test.mjs`: **exit 0, 6/6 tests**.
- `git diff --check HEAD`: **exit 0**.

The retained 1129 evidence remains **223/223 neighbor tests PASS**; those unchanged checks were not duplicated. No browser, localhost, host-script, full, or heavy journey was run.

## Dependency/source identity

- Pinned archive: `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`.
- Archive size: 73,451 bytes; members: 80; SHA-256/SRI: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Private qualification overlay resolved package `@banodoco/timeline-composition` version `0.0.14` and only its declared public exports (`.`, `evaluation`, `theme-api`, generated registries/effects/animations/transitions, `registries`, `package.json`). The shared install was never modified and was restored after testing; its stale `0.0.10` identity is not qualification evidence.
- Production/test import graph was inspected: App consumers use the package public subpaths (`theme-api`, `registry.generated`, `animations.generated`, `effects.generated`, `transitions.generated`); Vite/Vitest map the public package and `@workspace-*` renderer aliases to the vendored source graph.
- Reviewed source commits are all ancestors of HEAD: `a6b5de025`, `b0bdd9a01`, `be07d53e3`, `f5eb35117`, `305b40ac0`, `8fd6f4e23`, `f07f5c876`, `514ab7235`, `19eb6b08a`, `04fb90b34`, `666dc54ee`. Their touched paths and final HEAD blobs were checked; the expected later provider correction is the sole intentional source evolution in that set.

## Locks and inherited gates

- Read-only comparison against exact pinned Runtime producer commit `34eac0041b0891e9011966b39bcbd26053fde5bc`: **13/13 runtime.lock.json source/hash mappings plus manifest metadata PASS**.
- Read-only comparison against exact pinned Agent producer commit `5dec5dc6a4eb6683cd8a9a7e7f2048fbb18d9681`: **7/7 boundary mappings plus manifest metadata PASS**.
- The mutable `/home/user/work/runtime` and `/home/user/work/agent` integration checkouts are at different heads, so `scripts/vendor-lock.mjs check ... --producer` correctly rejects them. No sync updater was run and no lock was changed.
- `npm run typecheck:strict-islands` remains the inherited nonzero gate. Diagnostics are unchanged missing Astrid/virtual identities: `@astrid/packs/rendering/shared/managed-media-policy`, `managed-media`, `readiness-image`, `@astrid/packs/rendering/elements/catalog.ts`, `virtual:astrid-element-admissions`, local end-spanning/frame-overlay components, plus existing implicit-`any` diagnostics in `ReadinessVideo.tsx` and `astrid-element-catalog.ts`. The gate was not weakened.

## Behaviour coverage and handoff

The passing 353-test residual farm plus focused 25-test provider proof preserve the corrected raw opaque recovery draft and the prior outbox, guarded undo, D13 declared-read, metadata, canonical-reply, idempotency, dry-run/preview, history/effects/bindings, conflict/invalid, and accepted/merged semantics. The two reviewed e2e source blobs retain the full v2 request/reply assertions and P1/P2 source identity; their browser execution remains farm-owned and was not run here.

Qualification verdict: **PASS for the requested targeted residual gate; ready for the farm's single full rerun on this exact SHA.**

Private dependency recipe from the actual worker execution: create a worker-owned private node_modules directory with its own .vite and .vite-temp directories. Symlink the ordinary shared top-level dependencies into it; for @banodoco, create a private scope directory and symlink each existing package except timeline-composition. Extract the pinned archive into the private @banodoco/timeline-composition directory with --strip-components=1. Verify realpath remains private, version0.0.14, archive SHA256819acf/73451bytes/80members, and the declared package exports. Replace ONLY the worker worktree node_modules symlink with the private graph for the run; restore that worktree symlink afterward. No shared dependency file/link/cache is mutated. Run Vitest with --no-cache and worker-owned TMPDIR; no package-root source shims, patched tarball or pin changes. This recipe was executed successfully for all353+25+13 tests.
