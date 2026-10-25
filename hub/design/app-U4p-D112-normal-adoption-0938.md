# U4p D112 report

Adopted Runtime `8b3895cf141f5b7359cceacefde62c9a9475eabf` through normal tooling.

Changed only:

- `runtime.lock.json`
- `public/install-manifest.json`

Provenance:

- Runtime tree: `5b39e3bcce3ecaa8e184c82e30335ba881b6a3d2`
- Agent: `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`
- Schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`
- Reviewed D112 source hashes matched exactly.
- 14/14 producer mappings and protected six plus D113/D115 hashes 8/8.
- D112a PASS53 receipt and release authorization consumed. D111b was not adopted or awaited.

Checks:

- Vendor lock: PASS
- Central targeted Vitest: 17/17
- Manifest tests: 2/2
- Schema guard: 2/2
- Runtime artifact controls: 3/3 and manifest current
- Node syntax: 3/3
- ESLint: 0 warnings/errors
- JSON and `git diff --check`: PASS

Known limitation: direct `update-manifest.test.mjs` fixture tests hit sandbox `spawnSync git EPERM`; no workaround or test weakening was made. The central Vitest runner does not collect that `.mjs` file.

Created `notes/adoption.json`, `notes/adoption.md`, commit message, and `DONE`. No full suite, browser/service run, dependency install, or unrelated candidate was used.