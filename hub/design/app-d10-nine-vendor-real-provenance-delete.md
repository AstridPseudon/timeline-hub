# D10 App nine-vendor real-provenance deletion

## Result

DELETED in the worker tree. Applied
`handoff-vw-m3-d10-final-real-central-owner-ready.patch` to App HEAD
`180d2aaea`, excluding only its Home hunk because the current tree already
contains that hunk (the Composition public registry bridge and retained custom
asset adapters). The patch deletes exactly nine package-owned vendor
implementations and adds the manifest-driven exclusion/provenance seam.

The App harness commit SHA is intentionally not claimed yet; the harness will
create it after this worker exits. The exact source authority remains Astrid
commit `680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1`, tree
`07ce61f24ec38a1a60c4a981b6bd666f4971bd67`.

## Evidence

- Central normal-refresh proof already recorded in
  `handoff-vw-m3-d10-final-real-central-REPORT.md`: result
  `vw-m3-d10-final-central-without-preload-integration-viewing-pack-wrapper-unit-1020183621-31017`, PASS. It used real `git`, the exact Astrid commit, no preload/interception, and byte-compared the normal generator output. It verified 146 recorded vendor files and exactly nine exclusions.
- `node scripts/build/verify-astrid-vendor-sources.mjs` — PASS: 65 pinned source files, 146 vendor files, 11 Home imports.
- `node --test scripts/quality/astrid-public-boundary.test.mjs` — PASS.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/runtime/publicCompositionElementRegistry.test.ts` — PASS: 2 tests.
- Combined targeted run including `src/pages/Home/PublicAstridEditorProvider.test.tsx` — Home provider 2 tests passed; the unchanged mixed `TimelineRenderer.public-host.qualification.test.tsx` control retained 2 installed-host failures because it still expects the deleted vendor implementations. This control was not changed or requalified.
- `node --check scripts/astrid-landing/refresh-vendor.mjs`, exact nine-path static exclusion/import/provenance guard, and `git diff --check` — PASS.

No full suite, project TypeScript check, install, build, browser, live socket,
or shared dependency/cache write was run. The local normal refresh command was
attempted with the exact checkout but sandbox Node `spawnSync('git')` returned
EPERM; the central no-preload result above is the qualifying normal-refresh
evidence.

## Preserved boundary

The public catalog, descriptors, schema, revisions, custom `audio-reactive-colour`,
local end-spanning/frame-overlay adapters, assets, and both Vite checkout seams
remain intact. No Agent source-wrapper investigation or generator/provenance
hand edit was performed.
