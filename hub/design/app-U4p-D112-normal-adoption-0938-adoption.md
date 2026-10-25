# U4p D112 normal adoption

Adopted the authorized normal Runtime identity-recovery merge through the existing tools. The App base is `7841a946197b5312d79b594ffec0e5f7a937b6c0` (tree `8f7124205d42305944a8c772c398639bcae5761e`).

Runtime provenance is `/home/user/work/runtime` at `8b3895cf141f5b7359cceacefde62c9a9475eabf` (tree `5b39e3bcce3ecaa8e184c82e30335ba881b6a3d2`), the normal two-parent merge of integration `e6b669b98d8eeb349c311741cdfd8cfbfe5e5486` and reviewed D112 candidate `be828d92cba9200a6ae0ded3a2e968dc3f6ac383`. The reviewed source tree is `08ea7479d3709a915a51e17ade13453eee914da5`; source hashes match the D112a receipt. The disjoint `tests/test_timeline_render_publication.py` snapshot test remains present. Runtime contract version is `0.2.14`.

Agent provenance is `/home/user/work/wt/agt-pin-070dfc5e` at `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, tree `6056414359ae9fce08d999d54cbecf719fda33c3`. Schema digest remains `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`; the producer version and all 14 mappings are unchanged.

Changed only:

- `runtime.lock.json`: Runtime source commit updated; SHA256 `715f1bff5407c8cceba27dac5b135efb07468b4fa7c8a2899669eefc516d1b4b`.
- `public/install-manifest.json`: Runtime SHA updated; Agent SHA and schema unchanged; SHA256 `c96a2a69a43de1efb34d390e13df201134cd418bd48ec5759fda16e4048b5172`.

The D112 security PASS344, native recovery/seed/SWAP positives, and D112a warm release PASS53 are recorded in the existing receipts `rt-D112-security-review-0827.md`, `rt-D112-acceptance-return-0850-report.md`, and `rt-D112a-warm-release-check-0927.md`. The D112a header authorizes release on that PASS; no new App security/source review or timing gate was added. D111b was not adopted or awaited.

Checks:

- Vendor-lock producer check: PASS.
- Central targeted Vitest: 17/17 (2 install-manifest skew, 15 vendor-lock).
- Installer manifest: 2/2; schema guard: 2/2.
- Runtime artifact manifest: current; artifact tests: 3/3.
- Exact producer mappings: 14/14; protected six plus D113/D115: 8/8.
- Node syntax: 3/3; scoped ESLint: 0 warnings/errors; JSON syntax and `git diff --check`: PASS.

The direct updater test was attempted but its two fixture-repository tests are sandbox-blocked by `spawnSync git EPERM`. The central Vitest runner does not collect that `.mjs` file even when passed as a filter; this limitation is recorded without weakening or changing tests. No full suite, browser/service run, Runtime/Agent native proof, dependency install, or unrelated candidate was used.
