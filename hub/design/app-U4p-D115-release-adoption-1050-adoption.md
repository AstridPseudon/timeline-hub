# U4p D115 tool-only adoption

Adopted the released Runtime D115 source through the existing normal tools. App base is `96d4754b4eef0591a208d6b51b60c30fc44b6915` (tree `3f9da34c4f116026ec21022421850e0608ba653b`).

Runtime `/home/user/work/runtime` is `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`, tree `9bf331d68df8c966e8927a3f083ba03687803c99`, exactly matching reviewed `274bbf7d73c543d72058ce3563eba2af5cdc4bd1`. The Runtime store hash is `f0867b6bf083aef2ca280c3f1bcbbbc926c7dfc448c519836e286022f5e3d59a`; the history source hash remains `788e1280c61cbee6817595544495ba462365d956d0cd85499923328dedba838b`. Agent is `/home/user/work/wt/agt-pin-070dfc5e` at `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, tree `6056414359ae9fce08d999d54cbecf719fda33c3`.

The Runtime release is the qualified intermediate-image-auth release: strict-neighbor `321` and native smoke `2` passed, with the documented parent RED and baseline diagnostics preserved. Current App `15203` was not retargeted and no SWAP fix/GO is inferred.

Changed only:

- `runtime.lock.json`: `source_commit` updated from `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e` to `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`; producer version preserved.
- `public/install-manifest.json`: `runtime.sha` updated to `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`; Agent SHA and schema digest preserved.

Verification passed:

- Vendor lock check against the exact Runtime checkout.
- Installer updater `2/2`, manifest `2/2`, and schema guard `2/2`.
- Isolated Runtime skew/vendor Vitest: 2 files, `17/17`.
- Runtime generator/artifact controls: generator PASS, artifact-manifest PASS, artifact tests `3/3`.
- Exact producer mappings `14/14`; released canonical Runtime files `15/15`; protected six plus D113/D115 `8/8`.
- Runtime store/history source hashes, producer version, and schema digest match the release record.
- Node syntax `3/3`, JSON `2/2`, scoped ESLint zero warnings/errors, and `git diff --check` PASS.

The first suggested `--configLoader=runner --no-cache` Vitest command was not usable with the existing config because `__dirname` is undefined; the repository’s normal bundled loader with `--no-cache` passed all 17 tests. No workaround, dependency install, generated-byte edit, test weakening, full suite, browser/service body, native proof, D119 work, or SWAP decision was performed.
