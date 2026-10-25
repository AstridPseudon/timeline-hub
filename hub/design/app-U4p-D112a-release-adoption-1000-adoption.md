# U4p D112a release adoption

Adopted the released normal Runtime provenance through the existing tools. App base is `28660e72fabcc72baeda158b5088bfae00caaa2f` (tree `59f8bdd20ebfec9850f90f3b428d230589f0f11d`).

Runtime is `/home/user/work/wt/rt-pin-d23a8e0d` at `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e`, tree `6283b5fbb128447f1b333e0e6af334d35637cf69`, exactly matching reviewed commit `32c22795de890818eb8abeae6e644685098cbf30` and its tree. The approved store source hash is `f0867b6bf083aef2ca280c3f1bcbbbc926c7dfc448c519836e286022f5e3d59a`; the history-state source hash remains `788e1280c61cbee6817595544495ba462365d956d0cd85499923328dedba838b`. The canonical 15 paths are unchanged from be828. Agent is `/home/user/work/wt/agt-pin-070dfc5e` at `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, tree `6056414359ae9fce08d999d54cbecf719fda33c3`.

Changed only:

- `runtime.lock.json`: Runtime source commit updated to `d23a8e…`; producer version and all 14 mappings preserved.
- `public/install-manifest.json`: Runtime SHA updated to `d23a8e…`; Agent SHA and schema digest preserved.

Verification passed:

- Node20 updater: `update-manifest.test.mjs` 2/2; manifest 2/2; schema guard 2/2.
- Isolated Node20 Vitest skew/vendor lane: 2 files, 17/17.
- Runtime generator and artifact controls: generator check PASS, artifact manifest check PASS, `test_artifact_manifest.py` 3/3.
- Runtime vendor lock: PASS; exact producer mappings 14/14; protected six plus D113/D115 8/8.
- Canonical 15 comparison and reviewed-tree equality: PASS; source/diff checks PASS.
- Node syntax 3/3, JSON syntax 2/2, scoped ESLint zero warnings/errors, `git diff --check` PASS.

The release packet authorizes ordinary adoption and immediate later full P2; D111b was neither adopted nor awaited. No full suite, browser/service run, native proof, dependency installation, product/test change, or unrelated candidate was used.
