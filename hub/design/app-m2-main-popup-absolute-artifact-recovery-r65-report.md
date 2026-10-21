# App artifact recovery delivery

Delivered both requested documents to the absolute shared `ORCH/design` path:

- `run-on-main-app-automatic-current.md`
- `peer-app-to-app2-popup-add-caller-1030.md`

Recovery and verification:

- r53’s document was recovered exactly from its logged `apply_patch` source;
  blob hash `f01b37bf0ef7e5ede374f678cf35733ac4408657`, 261 lines / 14,941
  bytes. No automatic proof result is claimed; the packet remains a one-run
  handoff.
- r63’s document was extracted from
  `tl/app-m2-popup-shared-port-caller-handoff-r63` with `git show`; blob hash
  `1c82c0c29c49a9126de19894e73aa165ed05ec42`, 159 lines / 9,515 bytes. The
  source branch commit is `3b6b492d514a067f26f4ab49f819698690db7969`.
- The source tuple in the r53 packet is verified: App
  `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf`, tree
  `8e242d1497841f391b6152ecd8d204143fa03b52`; approved R51 and readiness
  commits `02ac224cd3c0d376f08b6129f58ded624f3e400d` and
  `da5d6d564af58ad06f126188c25e9a47f4e45be4` are ancestors.
- The packet preserves concrete prerequisites: Node v20.19.4, Chromium
  `141.0.7390.37` at the recorded executable/path, private public13 graph,
  Agent/Runtime pinned checkouts and read-only venvs, physical mode-0700
  private paths with resolved temp/profile/socket paths under 100 characters,
  and native port allocation with fixed door 17340. It explicitly rejects
  Node v20.20.0, the stale c497 source, shared public10 dependencies, and
  inherited `NODE_OPTIONS`, `NODE_PATH`, `LD_*`, or `PYTHONHOME`.

Tests/runs: no product tests, browser, install, build, full suite, graph
build, or automatic actual were run. Hash and ancestry checks above passed.
No repository `.gitignore` or repository design file was changed.

Recovery limit: r53’s original worktree was recycled, so its exact document
was recovered from the worker log’s complete patch source and verified against
the logged blob hash; its proof itself remains unexecuted.
