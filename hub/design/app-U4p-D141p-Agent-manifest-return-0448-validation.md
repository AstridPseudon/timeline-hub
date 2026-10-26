# U4p D141p validation

Source qualification:

- Agent checkout `/home/user/work/wt/agt-pin-8585ed9c` was initially absent, then appeared before updater use.
- Exact Agent tuple: `8585ed9c0404d0187b2ce70242d25114a32747c2`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`, clean.
- Exact Runtime tuple: `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, tree `ac5b862744bece65b2e30565db1777bacd60da28`, clean.
- `astrid/installer/tools.py` contains the required `User-Agent: astrid-installer/{ASTRID_VERSION}` behavior; requirement commit `e1c751def40f8fde59277226b6c190354d22744c` is an ancestor.

Generation and conservation:

- Private `refresh-vendor.mjs --destination ...` comparison: 160 payload paths and contents exact to the App baseline.
- Normal default `refresh-vendor.mjs` updated provenance only.
- `update-manifest.mjs --plan`: proposed only the qualified Agent pin; Runtime and schema pins remained exact.
- `update-manifest.mjs --write`: exit 0.
- Repeat `update-manifest.mjs --plan`: idempotent qualified pins.
- `node scripts/build/verify-astrid-vendor-sources.mjs`: exit 0; 65 closure files, 160 vendor files, and 11 public imports verified.
- Direct Git tree/blob comparison: every non-allowed path exact to `8f278b91...`; all 160 vendor payloads exact; only the two authorized metadata paths differ.
- `git diff --check`: exit 0.

Tests:

- `PATH=/opt/node20/bin:$PATH node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs`: manifest test passed; update-manifest test could not complete because nested Node subprocesses in this sandbox returned empty stdout despite exit 0. No test files were changed or weakened.
- Repeated with the temporary outside-worktree child-process compatibility preload and isolated Git config: the same update-manifest test remained environment-blocked by nested Node output suppression. The direct updater invocations and generated outputs passed independently.
- No full, browser, journey, or live-socket suite was run.
