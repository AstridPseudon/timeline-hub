# Verdict: DEFECT

## Scope and source

- Target: Composition `tl/vw-m4-main-api-smoke`, source SHA `1ffb8d7de57da393c2678a5361b2e9e4471b6475`.
- Comparison base: `5e06f40146573a529896cc812229eb890c53c81a`.
- Target diff: only `scripts/smoke-package.mjs`, `8 insertions / 3 deletions`.
- Product/package source, `package.json`, `package-lock.json`, and the published 0.0.12 bytes are unchanged by this commit.

## Ledger replacement coverage

The exact legacy ledger names are:

- Theme API: `composeAnimations`, `useTheme`, `EffectProps`, `AnimationReferenceList`, `RuntimeTheme`.
- Generated registry: `THEME_PACKAGE_REGISTRY`, `THEME_PACKAGE_CLIP_TYPES`.

The current replacement test names are `scripts/gen-registry.test.mjs`, `typescript/tests/registries.test.ts`, `typescript/tests/theme.test.ts`, and the package consumer probe in `scripts/smoke-package.mjs`.

The 08:20 change correctly adds all five theme API names and both registry names to the strict NodeNext consumer probe at `scripts/smoke-package.mjs:168-197`. The runtime smoke already exercises `composeAnimations` and `useTheme` and checks the theme API/root identity at lines 76-81 and 107/153-158.

## Concrete defect

The runtime smoke does not assert either legacy generated-registry export. It dynamically imports the namespace at `scripts/smoke-package.mjs:78`, but only uses `themes.BUNDLED_THEMES` and `themes.BUNDLED_THEME_VERSIONS` at lines 102 and 160. The two legacy exports appear only in the compile-only consumer at lines 171 and 197, where `void` proves declaration availability but cannot detect a declaration/runtime mismatch.

The current registry tests do not close this gap: `typescript/tests/registries.test.ts:12` imports only `BUNDLED_THEMES` and `BUNDLED_THEME_VERSIONS`; `scripts/gen-registry.test.mjs` verifies generated-file stability/drift but does not directly assert either `THEME_PACKAGE_*` export. Therefore a package could publish declarations containing both names while omitting or changing their runtime exports and this replacement coverage would still pass.

Required repair: add runtime assertions against `themes.THEME_PACKAGE_CLIP_TYPES` and `themes.THEME_PACKAGE_REGISTRY` in the package smoke (preferably exact expected clip-type/key coverage), then run the qualified package smoke and current registry tests. Do not treat the existing strict type probe as runtime proof.

## Evidence run

Passed:

- `node --check scripts/smoke-package.mjs`.
- `git diff --check 5e06f401..HEAD`.
- Read-only static audit of the target smoke, current registry tests, and generator test: strict consumer coverage `5/5` theme names and `2/2` registry names; runtime `THEME_PACKAGE_*` assertions `0/2`; runtime bundled-registry assertions `2/2`; current `registries.test.ts` direct `THEME_PACKAGE_*` assertions `0/2`.
- Read-only Python `tarfile` inspection of the immutable 0.0.12 archive confirmed the shipped `registry.generated.js/.d.ts` contain both `THEME_PACKAGE_CLIP_TYPES` and `THEME_PACKAGE_REGISTRY`, and `theme-api.js/.d.ts` contain the legacy runtime/type surface. Archive size/hash: 58,444 bytes, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

Not run:

- `scripts/smoke-package.mjs` / `npm run test:package`: the prior worker report records its initial `spawnSync('tar')` as sandbox `EPERM`; this review did not retry or mislabel that blocked command as passing.
- `npm test` or the current TypeScript registry tests: this worktree has no local `node_modules`; the shared Composition graph is explicitly disqualified/read-only pending repair, so no environment qualification was claimed.
- No full, browser, socket, render, install, merge, push, or product/script edit.

The worktree remains unchanged. The 0.0.12 archive and all immutable package bytes were only read.
