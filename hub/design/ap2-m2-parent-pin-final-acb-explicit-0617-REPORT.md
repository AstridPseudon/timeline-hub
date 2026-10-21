# App2 M2 parent final source pin

## Result

The final parent source is bound to:

- HEAD: `acb582c2c3b08481d43853b8526894ac60d074bc`
- tree: `141724b56736be40a269f60aa8bfc060914ebd29`
- helper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh`
- final helper SHA-256: `d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`
- worker gate SHA-256: `515931b8700aba3bf7b1a98e5013ecbe3c5769925b9ce21e44f4fb03b1a4a1e5`
- unchanged driver SHA-256: `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`

The helper changed only the `final95:parent` pair from
`a304dce02a185a4774ff514d5aa451c9702aa46f` /
`a3c82aa91f1336b86491191acf857d88c56179b2` to the final HEAD/tree
above. Replacing the final pair with the old pair in memory only (the old
text was never written) reproduced the required old helper SHA
`af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.
The worker gate is a private copy of the 0609 gate; its only byte change is
`HELPER_SHA`.

## Generated registrations

Two rows were generated from recomputed gate/driver SHA values and appended
to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`:

- `ap2-m2-parent-pin-final-acb-explicit-0617-preflight`
- `ap2-m2-parent-pin-final-acb-explicit-0617-actual`

Both rows pin the worker gate and driver hashes, use
`NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1`,
and invoke the existing gate. The actual row was registered but not run.

## Verification

- Helper profile command:
  `env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh -c '. "$1"; printf ...' sh normal014-source-common.sh`
  — PASS; returned the final HEAD/tree.
- In-memory reverse helper hash — PASS; reproduced `af83e829...`.
- Wrong old helper digest and wrong old keeper tuple — PASS; both refused.
- Final keeper clean status, required `KEEP`, normal
  `node_modules -> /home/user/work/app/node_modules` link, required
  ancestry, and driver hash — PASS.
- `sh -n` on helper and gate — PASS.
- Playwright collection with the three-products config — PASS; exactly one
  test, `three-products.spec.ts:1440`.
- Central command:
  `request-test ap2-m2-parent-pin-final-acb-explicit-0617 ap2-m2-parent-pin-final-acb-explicit-0617-preflight`, followed by
  `wait-test ap2-m2-parent-pin-final-acb-explicit-0617-ap2-m2-parent-pin-final-acb-explicit-0617-preflight-1021062025-31285`
  — PASS in 10s. The source preflight verified 76 artifacts, and the gate
  recorded refusals for wrong captured tree, wrong keeper, wrong helper
  digest, and wrong argv; list collection remained 1.
- App worktree status — clean; no App product/test/body edits.

No actual, browser replay, build, full suite, install, or native retry was
run. No decision was pending or changed. Recommended next step is the
independent body-conversion/binding review requested by the plan; only after
that review should the separately registered actual lane be considered.
