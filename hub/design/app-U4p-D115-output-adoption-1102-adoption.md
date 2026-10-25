# U4p D115 tool-only adoption

Adopted the released normal Runtime output projection through the existing
sync and installer tools. App base is `7e92cd9468b883b009e8840786e832301479c3ed`
(tree `d7d1d8877dd226acef2d442275428c566fae4de0`).

Runtime `/home/user/work/runtime` is clean at
`42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree
`085a5be70b56353deb41ae7d743336a4ccb7f29c`, exactly matching reviewed author
`e65422348314084a1a3cb6687fcdc520c73347e8`. Agent remains the genuine pinned
checkout `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, tree
`6056414359ae9fce08d999d54cbecf719fda33c3`.

Changed only:

- `runtime.lock.json`: Runtime `source_commit` advanced from `369ffa7c00bd3d45c610fac7651ff79e7a283a1a` to `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`.
- `public/install-manifest.json`: Runtime SHA advanced to `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`; Agent SHA and schema digest preserved.

Verification passed:

- Vendor lock check against the exact Runtime checkout.
- Installer updater `2/2`, manifest `2/2`, and schema guard `2/2`.
- Vitest: 2 files, `17/17` tests.
- Runtime generator/artifact controls: generator PASS, artifact-manifest PASS, artifact tests `3/3`.
- Exact producer mappings `14/14`; canonical Runtime files `15/15`; source/protected hash checks match the release evidence.
- Node syntax `3/3`, JSON `2/2`, scoped ESLint with zero warnings/errors, and `git diff --check` PASS.

The release evidence documents one retained parent-identical
`SimpleNamespace`/`db_path` authentication failure; it is not attributed to
D115. No source/security review, product/test/generated/kit/package/pin edits,
full/native/browser/service run, D111b/tags adoption, or wire change was made.
