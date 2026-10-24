## P2 verdict

- Actual run: `app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933`
- Result: **FAIL**, exit `1`, duration `469s`
- Live gate: **NO-GO**
- Original body: **8 selected, 3 executed, 0 passed, 3 failed, 5 not run**
- Preflight/readiness: door, build (`1m48s`), native seed/history, selector collection (`8`), and mounted readiness passed. Readiness process scope was `39.4s`; the readiness test itself was reported as `19s`.

Failures:

1. Element Apply — reported at declaration `three-products.p2-elements-assets.spec.ts:377`; exact earliest assertion is **UNKNOWN** because the direct result log is unavailable. Retained producer diagnostic only shows Apply click/request-start/retained, response `UNKNOWN`, terminal `pending`.
2. Popup ADD — `three-products.p2-popup.spec.ts:811`, canonical-document equality; expected added row track `V2`, received `plate`.
3. Parent move — `three-products.p2-tour.spec.ts:299`, receipt ID assertion inside `assertReplyShape` (invoked by the test at line 690); receipt mismatch.

Not run: registerAsset, automatic child placement, popup SWAP, transition-none single, transition-none bulk.

## Custody and source

- App source verified at `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`.
- Tree: `542b772e6deed676b917f857708445b7d37a5aa8`.
- Parents: `cad736828b4890a4df5fff42a22bfa4851a0ecfc`, `01ea81395a9bb8f091262a9d8275407675188fe6`.
- Four protected original spec bodies matched the exact base SHA-256 values.
- Selected Agent `333b44…` → tree `1094bf…`; Runtime `37eb6c…` → tree `be4114…`; Composition `c82eb7…` → tree `49975e…`.
- Same-ID snapshot reportedly retained the App tree/path, but full snapshot commit/parents, daemon/provider identity, and direct result files are **UNKNOWN**. The referenced result directory is absent here.
- Producer-reported Apply artifact: 1260 bytes, SHA-256 `08509524d5fd04f181b3fac8d0cdd211a32e2f4a107c4e78807ae4713e8533a`; no direct-file custody credit granted.

Source retains C0 request/reply, idempotency, zero-old-route, canonical, history, reload, and guarded-undo assertions. The failed/not-run body did not establish those obligations live.

## Checks

- `git diff --check` — PASS
- Exact base object/tree/parent checks — PASS
- Four protected spec SHA checks — PASS
- Reused unchanged validation:
  - Vitest semantic oracle — `7 passed`
  - Node oracle suite — `10 passed`
  - Three TypeScript checks — PASS
  - Scoped ESLint — PASS
  - Playwright list — exactly `8` tests in `3` files
  - Prior pure-source qualification — `695/695`, popup controls `67/67`, controls `30/30`, diagnostics `11/11`

No tracked files, tests, generated files, pins, or source were changed. Commit message and `DONE` marker were created. Recommended next step: retain/authenticate the missing same-ID packet and address the demonstrated live failures before any new original run.