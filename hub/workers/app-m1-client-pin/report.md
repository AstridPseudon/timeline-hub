Implemented the Runtime DTO artifact pin.

Changed:

- Added `timeline-commit-types.ts` to `runtime.lock.json`; coverage 12→13.
- Pinned Runtime commit `c423544de3b7a1090649bf32e4c82514c4c7a641`.
- Updated `vendorLock.test.ts` expectation.
- Generated files were already byte-identical; no content changes.

Passed:

- Vendor-lock update/check
- 13-entry hash and byte audit
- `npm run test:contracts`
- File-scoped ESLint
- `git diff --check`

Targeted Vitest: `timelineCommit.test.ts` passed (41 tests). Vendor-lock fixture tests were blocked by sandbox `spawnSync git EPERM` during fixture setup.

Handoff files written:

- `commit-msg`
- `report`

No full/browser/install suites run.