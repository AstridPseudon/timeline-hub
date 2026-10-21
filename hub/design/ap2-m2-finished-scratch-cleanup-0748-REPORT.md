# App2 finished scratch cleanup — 2026-10-21

Finished App2-only recovery is complete. No App product files, tests, Git metadata, shared dependencies, or active test sources were changed.

Free space on `/home/user` was 14,750,367,744 bytes before cleanup and 15,719,424,000 bytes immediately after cleanup: 969,056,256 bytes recovered net of the lossless archives. A later read-only verification measured 15,403,737,088 bytes; this 315,686,912-byte decrease occurred after cleanup with no further write action by this worker, so it is recorded as concurrent machine-level disk drift rather than attributed to this recovery.

Packed and removed after `tar --compare` passed:

- `workers/ap2-m2-bootstrap-currentroot-consumer-patch/private-currentroot` → `private-currentroot.tgz`, 257,018,533 bytes, SHA-256 `b47bd5fa23aa263bd8d39d116a4138f7b0f20db99f7cd53d3de1901ea2d5c28d`
- `workers/ap2-m2-bootstrap-currentroot-consumer-patch/private-applycheck` → `private-applycheck.tgz`, 257,019,491 bytes, SHA-256 `c23fb2916859b505d1b2348c5b1cfd6c99f2ce096029bf24c4eb6e870697e428`
- `workers/ap2-m2-bootstrap-currentroot-consumer-patch/private-applycheck-final` → `private-applycheck-final.tgz`, 257,021,900 bytes, SHA-256 `91edc9135b8b219bac0df71d3ef69971561894589c3fa03b11ccccb1f7618eb4`
- `workers/ap2-m2-element-transition-native-recipe/app-55e7` → `app-55e7.tgz`, 256,795,663 bytes, SHA-256 `1f3cca35a70a9a7848c5bb50a3553e0425f617f780662a19c0496ccd70d2da0d`
- `workers/ap2-m2-element-transition-native-recipe/app-90f` → `app-90f.tgz`, 256,802,404 bytes, SHA-256 `fdee4d89d1966454f0dcbc733b05474a116947af71d24c160fc060bdb30e761f`
- `workers/ap2-m2-element-concrete-session-patch/private-currentroot.32KMQR` → `private-currentroot.32KMQR.tgz`, 256,759,143 bytes, SHA-256 `a9dd76b16ac453ba1b1d47e2b98ac6fadc933cb770e231e84569287de3ad61bc`
- `workers/ap2-m2-element-concrete-session-patch/private-currentroot.plsch4` → `private-currentroot.plsch4.tgz`, 127 bytes, SHA-256 `94d9d1f7cd752cd6c4c98bf97c9ae3e85694e0d45d504d2985b54530f0a3a874`

Each archive listed successfully with `tar -tzf`; no temporary archive remains. Symlinks were archived as symlinks, so shared `/home/user/work/app/node_modules` was not copied, changed, or removed.

The transition worker's private Agent copy (`agent-48b`, 112M), the hub-repair artifact directory (`artifacts`, 598M), and all worker logs, reports, commit messages, `DONE`, and `recycled` records remain in place. Historical log references to packed paths remain historical evidence.

Worktree recycle result: none eligible. The finished existing worktrees were all clean, but each had `KEEP`; each candidate HEAD was not an ancestor of `hub/tl/integration`, so no KEEP was released and `bin/recycle` was not invoked. The blocked/protected set is:

- parent proof/current worktrees: `ap2-m2-parent-complete-current-proof-source-0455`, `ap2-m2-parent404-current-envelope-exact-source-0556`, `ap2-m2-parent404-door-body-exact-correction-0604` (the last is current `acb` material);
- producer source/tool worktrees: `ap2-m2-producer-final-external-hash-binding-0416`, `ap2-m2-producer-frozen-delta-luna-resume-0453`, `ap2-m2-producer-helper-expect-import-0717`, `ap2-m2-producer-physical-keeper-startup-preflight-0545`, `ap2-m2-producer-realm-physical-path-diagnosis-0538`;
- selected source/tool worktrees: `ap2-m2-selected-actual-path-four-custody-fixes-0707`, `ap2-m2-selected-final95-owned-driver-source-0658`, `ap2-m2-selected-normal-dev-frozen-source-0651`.

The explicit active/queued producer, selected, parent, and central temporary paths named in App2 STATUS were not touched. No browser, install, full, localhost, or socket test was run; this was disk recovery only.

