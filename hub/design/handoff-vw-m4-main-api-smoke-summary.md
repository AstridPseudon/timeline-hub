# Handoff: vw-m4-main-api-smoke

## Change

Extended the existing `scripts/smoke-package.mjs` consumer type probe only:

- imported `useTheme` and `AnimationReferenceList` from the public `theme-api` export;
- type-checked both legacy references through `typeof`/declaration use;
- imported and referenced both meaningful registry exports, `THEME_PACKAGE_CLIP_TYPES` and `THEME_PACKAGE_REGISTRY`, through public `registry.generated`.

The scaffold test's constant-equals-itself literal assertion was not carried forward. No package version, dependency, public source, or archive content changed.

## Evidence

- `npm run build` — passed using the preinstalled qualified dependency tree.
- `npm pack --pack-destination <temporary directory>` — passed; generated 0.0.12 archive SHA-256 matched the qualified published archive: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- Strict NodeNext declaration probe against the actual 0.0.12 archive, with qualified peer symlinks and no install/network — passed.
- Runtime public-seam import probe against the actual 0.0.12 archive — passed.
- `node --check scripts/smoke-package.mjs` and `git diff --check` — passed.

The existing package smoke runner was attempted against the same archive with offline cache, but the sandbox rejected its initial `spawnSync('tar')` with `EPERM` before any assertion. No browser, socket, full suite, or network test was run.

## Handoff

Worktree change: `scripts/smoke-package.mjs`. Generated `dist` and temporary dependency/build files were removed. The harness should commit with the worker's commit message and merge through the orchestrator's normal path.
