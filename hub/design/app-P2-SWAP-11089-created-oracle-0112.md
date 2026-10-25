# Report

Implemented the source-first SWAP `created` expectation in [three-products.p2-popup.spec.ts](/home/user/work/wt/app-P2-SWAP-11089-created-oracle-0112/tests/e2e/local/three-products.p2-popup.spec.ts:523).

- Derives replacement asset from deterministic PNG bytes and pre-save registry.
- Strictly asserts exact ADD/SWAP command envelopes and creation claims.
- Added new/reused alias and malformed-claim controls in [p2-popup-oracle.test.mjs](/home/user/work/wt/app-P2-SWAP-11089-created-oracle-0112/tests/e2e/local/support/p2-popup-oracle.test.mjs:71).
- Production caller remains unchanged.

Tests passed:

- Popup oracle: 4/4.
- A3 producer controls: 37/37.
- `tsc` root/app/node `--noEmit`: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- Playwright list: exactly 2 protected tests.
- `git diff --check` and reverse-apply check: passed.

Final hashes:

- Popup spec SHA: `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`; blob `d7da4c234fb921c448bc18e9ac174b1a11dbc4a6`.
- Oracle SHA: `e166d1b62e4db1fb468d5737049ad126eadc5117a6790166ab1a982e4f6a35a6`; blob `d77ecc3c116453e3b0c1106580f7c5dd905114ea`.
- Production caller unchanged: blob `53550b81f0c10322ca360f7205878d602549ae92`.

Retained browser run `11089` remains the original NO-GO caused by the missing SWAP claim; no browser/service/full-suite rerun was performed. Independent protected diff review remains for the orchestrator.

Commit message and `DONE` marker are ready.